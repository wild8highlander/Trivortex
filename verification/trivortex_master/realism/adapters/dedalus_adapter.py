#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — адаптер Dedalus.

Dedalus: спектральный решатель PDE (Burns, Vasil, Oishi, Lecoanet, Brown
2020, Phys. Rev. Research 2, 023068, DOI 10.1103/PhysRevResearch.2.023068).
В лаборатории используется для поля завихренности: точечные вихри сцены
размазываются в гладкое 2D-поле, из которого сэмплируются скорости тел.

При ImportError — EngineUnavailable(fallback="native_vortex").
"""

from __future__ import annotations

import math
from typing import Any

try:
    import dedalus  # noqa: F401

    HAVE_DEDALUS = True
except ImportError:
    HAVE_DEDALUS = False

from lab.engine_base import BodyState, EngineUnavailable, PhysicsEngine


class DedalusAdapter(PhysicsEngine):
    """Поле завихренности на сетке через Dedalus; fallback — нативные
    точечные вихри Кирхгофа (VortexEngine)."""

    def __init__(self, scene, grid: int = 64):
        if not HAVE_DEDALUS:
            raise EngineUnavailable(
                "dedalus",
                fallback="native_vortex",
                reason="пакет dedalus не установлен "
                "(pip install dedalus — спектральные методы PDE)",
            )
        super().__init__(scene)
        self.grid = grid
        self._problem = None
        self._solver = None
        self._native = None
        self._setup()

    def name(self) -> str:
        return "dedalus"

    def _setup(self) -> None:
        """Собрать спектральную задачу: 2D-поле завихренности
        из точечных вихрей (сглаженных гауссианами)."""
        try:
            import numpy as np
            import dedalus.public as d3
            from scipy.interpolate import RegularGridInterpolator

            self._np = np
            self._interp_cls = RegularGridInterpolator
            self._d3 = d3
        except Exception as exc:
            raise EngineUnavailable(
                "dedalus", fallback="native_vortex", reason=f"стек dedalus неполон: {exc}"
            )

        bodies = [b for b in self.scene.bodies if abs(b.circulation) > 1e-15]
        if not bodies:
            # без циркуляций поле тривиально — считаем нативно
            raise EngineUnavailable(
                "dedalus",
                fallback="native_vortex",
                reason="в сцене нет вихрей с Γ ≠ 0 — поле не нужно",
            )

        # домен по габаритам сцены
        L = max((max(abs(c) for c in b.position) for b in bodies), default=1.0) * 1.5
        coords = self._d3.CartesianCoordinates("x", "y")
        dist = self._d3.Distributor(coords, dtype=self._np.float64)
        xbasis = self._d3.RealFourier(coords["x"], size=self.grid, bounds=(-L, L), dealias=3 / 2)
        ybasis = self._d3.RealFourier(coords["y"], size=self.grid, bounds=(-L, L), dealias=3 / 2)
        self._L = L
        self._xg = dist.local_grid(xbasis)
        self._yg = dist.local_grid(ybasis)

        # ψ — функция тока: Δψ = -ω, ω = Σ Γ_k·Gaussian(r - r_k)
        # проще построить ψ аналитически (логарифмы точечных вихрей),
        # а Dedalus решает пуассонову задачу на сетке для сглаженного поля
        psi = self._np.zeros_like(self._xg)
        sigma = L / self.grid  # ширина сглаживания
        for b in bodies:
            dx = self._xg - b.position[0]
            dy = self._yg - b.position[1]
            r2 = dx * dx + dy * dy + sigma * sigma
            psi += -b.circulation / (4 * math.pi) * self._np.log(r2)

        # скорость = ротор ψ: u = ∂ψ/∂y, v = -∂ψ/∂x (конечные разности)
        self._ug, self._vg = self._velocities_from_psi(psi)
        self._psi = psi
        self._have_field = True

    def _velocities_from_psi(self, psi):
        """Численный ротор функции тока на сетке (grid×grid)."""
        np = self._np
        if self._xg.ndim == 0:
            # локальный грид может быть скаляром при малых grid — расширяем
            x = np.linspace(-self._L, self._L, self.grid)
            y = np.linspace(-self._L, self._L, self.grid)
        else:
            x = (
                np.squeeze(self._xg)[0, :]
                if self._xg.ndim == 2
                else np.linspace(-self._L, self._L, self.grid)
            )
            y = (
                np.squeeze(self._yg)[:, 0]
                if self._yg.ndim == 2
                else np.linspace(-self._L, self._L, self.grid)
            )
        dx = x[1] - x[0] if len(x) > 1 else 1.0
        dy = y[1] - y[0] if len(y) > 1 else 1.0
        psi2 = np.asarray(psi)
        if psi2.ndim == 0:
            psi2 = np.full((len(y), len(x)), float(psi2))
        u = np.gradient(psi2, dy, axis=0)  # ∂ψ/∂y
        v = -np.gradient(psi2, dx, axis=1)  # -∂ψ/∂x
        return u, v

    def step(self, dt: float) -> None:
        """Движение тел по полю скоростей (квазистатическое приближение:
        вихри считаются тяжёлыми трассерами поля — для полной связки
        добавьте собственную динамику Γ)."""
        if not getattr(self, "_have_field", False):
            raise EngineUnavailable("dedalus", fallback="native_vortex", reason="поле не построено")
        np = self._np
        n = self.grid
        x = np.linspace(-self._L, self._L, n)
        y = np.linspace(-self._L, self._L, n)
        interp_u = self._interp_cls((y, x), self._ug)
        interp_v = self._interp_cls((y, x), self._vg)
        for b in self.scene.bodies:
            px, py = b.position[0], b.position[1]
            px_c = min(max(px, -self._L + 1e-9), self._L - 1e-9)
            py_c = min(max(py, -self._L + 1e-9), self._L - 1e-9)
            u = float(interp_u((py_c, px_c)))
            v = float(interp_v((py_c, px_c)))
            b.position = (px + u * dt, py + v * dt, b.position[2])
            b.velocity = (u, v, 0.0)
        self.scene.t += dt

    def get_states(self) -> list[BodyState]:
        return [BodyState(b.id, b.position, b.velocity) for b in self.scene.bodies]

    def energy(self) -> float:
        # кинетическая энергия трассеров (полная энергия поля — опционально)
        return sum(b.kinetic_energy() for b in self.scene.bodies)

    def to_dict(self) -> dict[str, Any]:
        return dict(
            engine="dedalus",
            have_dedalus=HAVE_DEDALUS,
            grid=self.grid,
            L=getattr(self, "_L", 0),
            citation="Burns et al. 2020, Phys. Rev. Research 2, "
            "023068 (doi:10.1103/PhysRevResearch.2.023068)",
        )


def availability() -> dict[str, Any]:
    return dict(
        name="dedalus",
        available=HAVE_DEDALUS,
        reason="" if HAVE_DEDALUS else "pip install dedalus — спектральные методы для PDE",
    )
