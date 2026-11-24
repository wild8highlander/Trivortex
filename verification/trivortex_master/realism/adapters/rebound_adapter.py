#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — адаптер REBOUND.

REBOUND: открытый N-body интегратор (Rein & Liu 2012, A&A 537, A128,
DOI 10.1051/0004-6361/201118085; лицензия GPL-3.0). Интеграторы:
IAS15 (Rein & Spiegel 2015), WHFast, MERCURIUS и др.

При ImportError возбуждает EngineUnavailable(fallback="native_newton") —
диспетчер lab.physics.get_engine ловит и переключается, фиксируя смену
в events сцены и HUD.
"""

from __future__ import annotations

from typing import Any

from importlib.util import find_spec

HAVE_REBOUND = find_spec("rebound") is not None  # availability probe

from lab.engine_base import BodyState, EngineUnavailable, PhysicsEngine


class REBOUNDAdapter(PhysicsEngine):
    """N-body через REBOUND (ias15 по умолчанию, whfast для скорости)."""

    def __init__(self, scene, integrator: str = "ias15"):
        """Do REBOUNDAdapter.  init for scene, integrator and return the result."""
        if not HAVE_REBOUND:
            raise EngineUnavailable(
                "rebound",
                fallback="native_newton",
                reason="пакет rebound не установлен (pip install rebound)",
            )
        super().__init__(scene)
        self.integrator = integrator
        self.sim = None
        self._setup()

    def name(self) -> str:
        """Handle REBOUNDAdapter.name."""
        return "rebound"

    def warmup(self) -> None:
        """Handle REBOUNDAdapter.warmup."""
        if self.sim is None:
            self._setup()

    def _setup(self) -> None:
        """Handle REBOUNDAdapter. setup."""
        import rebound

        sim = rebound.Simulation()
        sim.G = self.cfg.G
        sim.integrator = self.integrator
        # единицы: REBOUND работает в симметричных единицах; тела сцены
        # могут быть в СИ — масштабируем массы/расстояния для точности IAS15
        self._scale = 1.0
        max_r = max((max(abs(c) for c in b.position) for b in self.scene.bodies), default=1.0)
        if max_r > 0:
            self._scale = max_r  # нормировка расстояний к ~1
        for b in self.scene.bodies:
            sim.add(
                m=b.mass,
                x=b.position[0] / self._scale,
                y=b.position[1] / self._scale,
                z=b.position[2] / self._scale,
                vx=b.velocity[0],
                vy=b.velocity[1],
                vz=b.velocity[2],
                r=b.radius / self._scale,
            )
        sim.move_to_com()
        self.sim = sim

    def step(self, dt: float) -> None:
        """Do REBOUNDAdapter.step for dt and return the result."""
        if self.sim is None:
            return
        # dt в единицах сцены; REBOUND получает время с учётом масштаба
        # (массы не масштабируем, G уже задан; расстояния нормированы,
        # поэтому времени нужен множитель sqrt(scale) для гравитационной
        # согласованности — при масштабировании только координат)
        self.sim.integrate(self.sim.t + dt / self._time_factor())

    def _time_factor(self) -> float:
        # при делении координат на s и сохранении скоростей в м/с
        # время в нормированных единицах идёт в s раз быстрее
        """Handle REBOUNDAdapter. time factor."""
        return self._scale if self._scale > 0 else 1.0

    def get_states(self) -> list[BodyState]:
        """Handle REBOUNDAdapter.get states."""
        if self.sim is None:
            return []
        out = []
        for p, body in zip(self.sim.particles, self.scene.bodies):
            out.append(
                BodyState(
                    body.id,
                    (p.x * self._scale, p.y * self._scale, p.z * self._scale),
                    (p.vx, p.vy, p.vz),
                )
            )
        return out

    def energy(self) -> float:
        """Handle REBOUNDAdapter.energy."""
        if self.sim is None:
            return 0.0
        return self.sim.energy() * self._energy_factor()

    def _energy_factor(self) -> float:
        # E ~ m v² — масштабирование только координат не меняет v,
        # но potential масштабируется; возвращаем энергию сцены напрямую
        """Handle REBOUNDAdapter. energy factor."""
        return 1.0

    def apply_states(self) -> None:
        """Handle REBOUNDAdapter.apply states."""
        for st in self.get_states():
            body = self.scene.body(st.id)
            if body is not None:
                body.position = tuple(st.position)
                body.velocity = tuple(st.velocity)
        self.scene.t += self.sim.dt if self.sim else 0.0

    def to_dict(self) -> dict[str, Any]:
        """Сериализация для воспроизводимости в отчётах."""
        return dict(
            engine="rebound",
            integrator=self.integrator,
            have_rebound=HAVE_REBOUND,
            G=self.cfg.G,
            n_bodies=len(self.scene.bodies),
            citation="Rein & Liu 2012, A&A 537, A128 " "(doi:10.1051/0004-6361/201118085)",
        )


def availability() -> dict[str, Any]:
    """Статус адаптера для HUD."""
    return dict(
        name="rebound",
        available=HAVE_REBOUND,
        reason="" if HAVE_REBOUND else "pip install rebound — интеграторы IAS15/WHFast/MERCURIUS",
    )
