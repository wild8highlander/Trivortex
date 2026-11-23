#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — физические движки: нативные реализации + диспетчер.

Интерфейс (PhysicsEngine/BodyState/EngineUnavailable) живёт в
lab/engine_base.py — его импортируют и адаптеры realism/adapters/*,
поэтому петли lab ↔ realism нет.

Реализации здесь:
  * NewtonianEngine — N тел, RK4 на чистом Python (+1PN-поправка опц.);
  * VortexEngine   — точечные вихри Кирхгофа (интегралы H, P, Q, I).

Диспетчер get_engine(name, scene) ловит EngineUnavailable и откатывается
на нативный движок, фиксируя смену в events сцены.
"""
from __future__ import annotations

import math
from typing import Any

from lab.engine_base import (BodyState, EngineUnavailable,
                             PhysicsEngine as PhysicsEngineBase,
                             Vector3)


# ═══════════════════════════════════════════════════════════════════════════
# Базовый класс
# ═══════════════════════════════════════════════════════════════════════════
class PhysicsEngine(PhysicsEngineBase):
    """Нативный движок: общая логика для реализаций этого пакета.

    (Интерфейс — lab/engine_base.PhysicsEngine; здесь добавлено
    apply_states для записи состояний обратно в тела сцены.)
    """

    def apply_states(self) -> None:
        """Записать состояния обратно в тела сцены."""
        for st in self.get_states():
            body = self.scene.body(st.id)
            if body is not None:
                body.position = tuple(st.position)
                body.velocity = tuple(st.velocity)


# ═══════════════════════════════════════════════════════════════════════════
# Ньютоновский движок (RK4, чистый Python)
# ═══════════════════════════════════════════════════════════════════════════
class NewtonianEngine(PhysicsEngine):
    """N тел, гравитация Ньютона, интегратор RK4.

    Опции конфигурации: G, softening, enable_relativity (1PN),
    enable_dissipation (скоростное трение, для демо-режимов).
    """

    def name(self) -> str:
        return "native_newton"

    # ── правая часть: y = [x,y,z,vx,vy,vz]*N → dy/dt ──
    def _accelerations(self, pos: list[Vector3],
                       vel: list[Vector3]) -> list[Vector3]:
        n = len(pos)
        masses = [b.mass for b in self.scene.bodies]
        G = self.cfg.G
        eps2 = self.cfg.softening ** 2
        acc = [[0.0, 0.0, 0.0] for _ in range(n)]
        for i in range(n):
            xi, yi, zi = pos[i]
            ax = ay = az = 0.0
            for j in range(n):
                if i == j:
                    continue
                dx = pos[j][0] - xi
                dy = pos[j][1] - yi
                dz = pos[j][2] - zi
                r2 = dx * dx + dy * dy + dz * dz + eps2
                r = math.sqrt(r2)
                inv_r3 = 1.0 / (r2 * r)
                # 1PN-поправка (упрощённая, Einstein-Infeld-Hoffmann low-velocity)
                if self.cfg.enable_relativity:
                    v2 = vel[i][0] ** 2 + vel[i][1] ** 2 + vel[i][2] ** 2
                    c2 = 8.9875517873681764e16  # c^2
                    pn = 1.0 + 3.0 * G * masses[j] / (r * c2) + v2 / c2
                    factor = G * masses[j] * inv_r3 * pn
                else:
                    factor = G * masses[j] * inv_r3
                ax += factor * dx
                ay += factor * dy
                az += factor * dz
            if self.cfg.enable_dissipation:
                # слабое скоростное трение (демо диссипации)
                k = 1e-4
                ax -= k * vel[i][0]
                ay -= k * vel[i][1]
                az -= k * vel[i][2]
            acc[i] = [ax, ay, az]
        return acc

    def _deriv(self, y: list[float]) -> list[float]:
        n = len(self.scene.bodies)
        pos = [(y[6 * i], y[6 * i + 1], y[6 * i + 2]) for i in range(n)]
        vel = [(y[6 * i + 3], y[6 * i + 4], y[6 * i + 5]) for i in range(n)]
        acc = self._accelerations(pos, vel)
        out = []
        for i in range(n):
            out.extend(vel[i])
            out.extend(acc[i])
        return out

    def step(self, dt: float) -> None:
        n = len(self.scene.bodies)
        if n == 0:
            return
        y = []
        for b in self.scene.bodies:
            y.extend(b.state_vector())
        # RK4
        k1 = self._deriv(y)
        y2 = [y[i] + 0.5 * dt * k1[i] for i in range(len(y))]
        k2 = self._deriv(y2)
        y3 = [y[i] + 0.5 * dt * k2[i] for i in range(len(y))]
        k3 = self._deriv(y3)
        y4 = [y[i] + dt * k3[i] for i in range(len(y))]
        k4 = self._deriv(y4)
        for i in range(len(y)):
            y[i] += (dt / 6.0) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
        for i, b in enumerate(self.scene.bodies):
            b.position = (y[6 * i], y[6 * i + 1], y[6 * i + 2])
            b.velocity = (y[6 * i + 3], y[6 * i + 4], y[6 * i + 5])
        self.scene.t += dt

    def get_states(self) -> list[BodyState]:
        return [BodyState(b.id, b.position, b.velocity) for b in self.scene.bodies]

    def energy(self) -> float:
        return self.scene.total_energy()


# ═══════════════════════════════════════════════════════════════════════════
# Вихревой движок Кирхгофа
# ═══════════════════════════════════════════════════════════════════════════
class VortexEngine(PhysicsEngine):
    """Точечные вихри Кирхгофа в плоскости xy (z игнорируется).

    Уравнения: Γ_k·ẋ_k = ∂H/∂y_k, Γ_k·ẏ_k = −∂H/∂x_k, где
    H = −(1/4π)·Σ_{i≠j} Γ_i Γ_j ln|r_i − r_j|.
    Интегралы: H, P = ΣΓx, Q = ΣΓy, I = ΣΓ|x|² (лестница V3/V4).
    """

    def name(self) -> str:
        return "native_vortex"

    # ── интегралы Кирхгофа ──
    def hamiltonian(self) -> float:
        bodies = self.scene.bodies
        H = 0.0
        for i in range(len(bodies)):
            for j in range(len(bodies)):
                if i == j:
                    continue
                dx = bodies[i].position[0] - bodies[j].position[0]
                dy = bodies[i].position[1] - bodies[j].position[1]
                r2 = dx * dx + dy * dy
                if r2 > 0:
                    H -= (bodies[i].circulation * bodies[j].circulation
                          / (4.0 * math.pi)) * 0.5 * math.log(r2)
        return H

    def integrals(self) -> dict[str, float]:
        bodies = self.scene.bodies
        P = sum(b.circulation * b.position[0] for b in bodies)
        Q = sum(b.circulation * b.position[1] for b in bodies)
        I = sum(b.circulation * (b.position[0] ** 2 + b.position[1] ** 2)
                for b in bodies)
        return dict(H=self.hamiltonian(), P=P, Q=Q, I=I)

    # ── правая часть ──
    def _velocities(self) -> list[Vector3]:
        bodies = self.scene.bodies
        n = len(bodies)
        out = []
        for i in range(n):
            vx = vy = 0.0
            for j in range(n):
                if i == j:
                    continue
                dx = bodies[j].position[0] - bodies[i].position[0]
                dy = bodies[j].position[1] - bodies[i].position[1]
                r2 = dx * dx + dy * dy
                if r2 <= 0:
                    continue
                # поле скорости вихря j в точке i
                vx += -bodies[j].circulation * dy / (2 * math.pi * r2)
                vy += bodies[j].circulation * dx / (2 * math.pi * r2)
            out.append((vx, vy, 0.0))
        return out

    def step(self, dt: float) -> None:
        bodies = self.scene.bodies
        if not bodies:
            return
        # RK4 по (x, y) с массами-«циркуляциями» в знаменателе
        def deriv(state: list[float]) -> list[float]:
            saved = [(b.position[0], b.position[1]) for b in bodies]
            for i, b in enumerate(bodies):
                b.position = (state[2 * i], state[2 * i + 1], b.position[2])
            vels = self._velocities()
            for i, b in enumerate(bodies):
                b.position = saved[i] + (b.position[2],)
            out = []
            for i in range(len(bodies)):
                g = bodies[i].circulation
                if abs(g) < 1e-15:
                    out.extend((0.0, 0.0))   # невихревое тело неподвижно
                else:
                    out.extend((vels[i][0], vels[i][1]))
            return out

        y = []
        for b in bodies:
            y.extend((b.position[0], b.position[1]))
        k1 = deriv(y)
        y2 = [y[i] + 0.5 * dt * k1[i] for i in range(len(y))]
        k2 = deriv(y2)
        y3 = [y[i] + 0.5 * dt * k2[i] for i in range(len(y))]
        k3 = deriv(y3)
        y4 = [y[i] + dt * k3[i] for i in range(len(y))]
        k4 = deriv(y4)
        for i in range(len(y)):
            y[i] += (dt / 6.0) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
        for i, b in enumerate(bodies):
            b.position = (y[2 * i], y[2 * i + 1], b.position[2])
            b.velocity = (0.0, 0.0, 0.0)
        self.scene.t += dt

    def get_states(self) -> list[BodyState]:
        return [BodyState(b.id, b.position, b.velocity,
                          extra=dict(circulation=b.circulation))
                for b in self.scene.bodies]

    def energy(self) -> float:
        return self.hamiltonian()


# ═══════════════════════════════════════════════════════════════════════════
# Диспетчер движков
# ═══════════════════════════════════════════════════════════════════════════
# Инъекция адаптеров: realism регистрирует свои движки сюда при первом
# импорте (см. realism/__init__.py). Так lab не импортирует realism —
# петли зависимостей нет, адаптеры подключаются снаружи.
_EXTRA_ENGINES: dict[str, type[PhysicsEngine]] = {}


def register_engine(name: str, cls: type[PhysicsEngine]) -> None:
    """Регистрация стороннего движка (вызывается realism/)."""
    _EXTRA_ENGINES[name] = cls


def engine_registry() -> dict[str, type[PhysicsEngine]]:
    """Все известные движки: нативные + инжектированные адаптеры."""
    engines: dict[str, type[PhysicsEngine]] = {
        "native_newton": NewtonianEngine,
        "native_vortex": VortexEngine,
    }
    engines.update(_EXTRA_ENGINES)
    return engines


AUTO_ORDER = ["rebound", "native_newton", "native_vortex"]


def resolve_auto(scene) -> str:
    """Авто-выбор движка: REBOUND при наличии, иначе native."""
    reg = engine_registry()
    for cand in AUTO_ORDER:
        if cand in reg:
            return cand
    return "native_newton"


def get_engine(name: str, scene) -> PhysicsEngine:
    """Получить движок с fallback-цепочкой при недоступности."""
    if name == "auto":
        name = resolve_auto(scene)
    reg = engine_registry()
    if name not in reg:
        raise ValueError(f"неизвестный движок: {name}; "
                         f"доступны: {', '.join(reg)}")
    try:
        eng = reg[name](scene)
        # прогрев (адаптеры могут упасть здесь)
        if hasattr(eng, "warmup"):
            eng.warmup()
        return eng
    except EngineUnavailable as exc:
        fallback = exc.fallback if exc.fallback in reg else "native_newton"
        scene.events.append(dict(
            kind="engine_fallback",
            detail=f"движок {exc.name} недоступен ({exc.reason}); "
                   f"переключение на {fallback}"))
        return reg[fallback](scene)


# ═══════════════════════════════════════════════════════════════════════════
# Прогон симуляции с детекторами событий
# ═══════════════════════════════════════════════════════════════════════════
def run_simulation(scene: Scene, n_steps: int | None = None,
                   dt: float | None = None, record_every: int = 1,
                   progress=None, stop_on_collision: bool = False) -> dict[str, Any]:
    """
    Прогнать сцену вперёд. Возвращает сводку: шаги, время, энергия-дрейф,
    события (столкновения, вылеты, потеря энергии).

    progress: объект с update(i, tag) — прогресс-бар HUD (если включён).
    """
    if scene.engine is None:
        scene.apply_engine(scene.config.physics_engine)
    n_steps = n_steps or scene.config.n_steps
    dt = dt if dt is not None else scene.dt
    from lab.scene import BoundingBox
    scene.bounds = BoundingBox.from_scene(scene.bodies)
    # граница с запасом ×4: орбиты могут выходить за стартовый габарит
    scene.bounds.half = max(scene.bounds.half, 1.0) * 4.0

    e0 = scene.total_energy() if scene.engine.name() == "native_newton" \
        else scene.engine.energy()
    energy_drift = 0.0
    n_events0 = len(scene.events)

    for i in range(n_steps):
        scene.engine.step(dt)
        # детекторы раз в 10 шагов (быстро)
        if i % 10 == 0 or i == n_steps - 1:
            _run_detectors(scene, dt)
        if i % record_every == 0:
            scene.record_frame()
        if progress is not None:
            progress.update(i + 1, tag=f"шаг {i + 1}/{n_steps}")
        # предохранитель по времени
        if i % 500 == 0 and (scene.events[-1]["kind"] == "wall_limit"
                             if scene.events else False):
            break
        if stop_on_collision and any(
                ev["kind"] == "collision" for ev in scene.events[n_events0:]):
            break

    e1 = scene.total_energy() if scene.engine.name() == "native_newton" \
        else scene.engine.energy()
    if abs(e0) > 1e-30:
        energy_drift = abs(e1 - e0) / abs(e0)
    elif abs(e1) > 1e-30:
        energy_drift = float("inf")

    return dict(
        engine=scene.engine_name or (scene.engine.name() if scene.engine else ""),
        n_steps=n_steps, dt=dt,
        t_final=scene.t,
        energy_start=e0, energy_end=e1, energy_drift_rel=energy_drift,
        new_events=scene.events[n_events0:],
        total_events=len(scene.events),
        unphysical=scene.unphysical_flag,
    )


def _run_detectors(scene: Scene, dt: float) -> None:
    """Детекторы: столкновения, вылет за границы, потеря энергии."""
    bodies = scene.bodies
    # столкновения
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            d = bodies[i].distance_to(bodies[j])
            rsum = bodies[i].radius + bodies[j].radius
            if d < rsum:
                scene.events.append(dict(
                    kind="collision",
                    detail=(f"{bodies[i].id} ↔ {bodies[j].id}: "
                            f"d={d:.3g} < Σr={rsum:.3g} при t={scene.t:.3g}"),
                    t=scene.t, pair=(bodies[i].id, bodies[j].id)))
    # вылет за границы
    for b in bodies:
        if not scene.bounds.contains(b.position):
            scene.events.append(dict(
                kind="escape",
                detail=f"{b.id} покинул границы сцены (|r|>{scene.bounds.half:.3g})",
                t=scene.t, body=b.id))
    # потеря энергии (только для ньютоновского)
    if scene.engine and scene.engine.name() == "native_newton" \
            and len(scene.energy_history) >= 2:
        e_prev = scene.energy_history[-2]
        e_now = scene.energy_history[-1] if scene.energy_history else e_prev
        if abs(e_prev) > 1e-30 and abs(e_now - e_prev) / abs(e_prev) > 0.10:
            scene.events.append(dict(
                kind="energy_loss",
                detail=(f"потеря энергии >10% за шаг "
                        f"({(e_now - e_prev) / e_prev * 100:.1f}%)"),
                t=scene.t))
