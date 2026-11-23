#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — метрики: ляпуновский показатель, контроль интегралов,
расстояния между траекториями, спектральные характеристики, сравнение
сценариев.
"""

from __future__ import annotations

import math
from typing import Any, Sequence

from core.config import MasterConfig
from lab.body import Body
from lab.physics import NewtonianEngine, VortexEngine, run_simulation
from lab.scene import Scene


# ═══════════════════════════════════════════════════════════════════════════
# 1. Ляпуновский показатель (двухтраекторная схема)
# ═══════════════════════════════════════════════════════════════════════════
def lyapunov_exponent(
    scene: Scene,
    n_steps: int = 300,
    dt: float | None = None,
    perturbation: float = 1e-8,
    renorm_every: int = 10,
) -> dict[str, Any]:
    """Классическая схема Бенеттина: рядом с опорной траекторией живёт
    возмущённая; периодически перенормируем расхождение и копим логарифмы.

    Возвращает показатель λ (1/единицы времени) и диагностику.
    """
    dt = dt if dt is not None else scene.dt
    base = scene.clone()
    pert = scene.clone()
    # возмущение первого тела
    if pert.bodies:
        b = pert.bodies[0]
        b.position = (b.position[0] + perturbation, b.position[1], b.position[2])
    if base.engine is None:
        base.apply_engine(base.config.physics_engine)
    pert.engine = None
    pert.apply_engine(base.engine_name or base.config.physics_engine)

    log_sum = 0.0
    dist = perturbation
    diverged = False
    history: list[float] = []
    for i in range(n_steps):
        base.engine.step(dt)
        pert.engine.step(dt)
        if i % renorm_every == renorm_every - 1 or i == n_steps - 1:
            d = math.sqrt(
                sum(
                    (a - c) ** 2
                    for ba, bb in zip(base.bodies, pert.bodies)
                    for a, c in zip(ba.position, bb.position)
                )
            )
            if d <= 0:
                diverged = True
                break
            log_sum += math.log(d / max(dist, 1e-300))
            history.append(d)
            dist = d
            # перенормировка возмущённой траектории к базовой
            if pert.bodies and base.bodies:
                k = perturbation / d
                for bb, pb in zip(base.bodies, pert.bodies):
                    pb.position = tuple(c + (pc - c) * k for c, pc in zip(bb.position, pb.position))
    lam = log_sum / (n_steps * dt) if not diverged else float("inf")
    return dict(
        lyapunov=lam,
        n_steps=n_steps,
        dt=dt,
        perturbation=perturbation,
        divergence_history=history[-20:],
        chaotic=lam > 0.05,
        note=(
            "положительный λ — экспоненциальное разбегание близких "
            "траекторий (хаос); вблизи нуля/отрицательный — "
            "регулярное движение"
        ),
    )


# ═══════════════════════════════════════════════════════════════════════════
# 2. Контроль интегралов движения
# ═══════════════════════════════════════════════════════════════════════════
def integral_drifts(scene: Scene) -> dict[str, Any]:
    """Дрейф интегралов вдоль записанной истории сцены.

    Для ньютоновского движка: энергия, импульс, момент импульса.
    Для вихревого: интегралы Кирхгофа H, P, Q, I (критерий лестницы V3/V4:
    дрейф ≤ 1e-10).
    """
    if not scene.trajectory_history:
        return dict(error="у сцены нет истории")
    engine_name = scene.engine_name or ""
    out: dict[str, Any] = dict(engine=engine_name)
    if "vortex" in engine_name:
        # интегралы Кирхгофа по кадрам
        H, P, Q, I = [], [], [], []
        for state in scene.trajectory_history:
            bodies = [
                Body(
                    id=str(i),
                    name="",
                    mass=1.0,
                    radius=1.0,
                    position=tuple(s[:3]),
                    velocity=tuple(s[3:]),
                    circulation=scene.bodies[i].circulation if i < len(scene.bodies) else 0.0,
                )
                for i, s in enumerate(state)
            ]
            h = p = q = it = 0.0
            n = len(bodies)
            for i in range(n):
                p += bodies[i].circulation * bodies[i].position[0]
                q += bodies[i].circulation * bodies[i].position[1]
                it += bodies[i].circulation * (
                    bodies[i].position[0] ** 2 + bodies[i].position[1] ** 2
                )
                for j in range(n):
                    if i == j:
                        continue
                    dx = bodies[i].position[0] - bodies[j].position[0]
                    dy = bodies[i].position[1] - bodies[j].position[1]
                    r2 = dx * dx + dy * dy
                    if r2 > 0:
                        h -= (
                            (bodies[i].circulation * bodies[j].circulation / (4 * math.pi))
                            * 0.5
                            * math.log(r2)
                        )
            H.append(h)
            P.append(p)
            Q.append(q)
            I.append(it)

        def rel_drift(vals: list[float]) -> float:
            if not vals:
                return 0.0
            v0, v1 = vals[0], vals[-1]
            if isinstance(v0, list):  # защита от вложенных списков
                v0, v1 = v0[0], v1[-1]
            return abs(v1 - v0) / max(abs(v0), 1e-12)

        out.update(
            H_drift=rel_drift(H),
            P_drift=abs(P[-1] - P[0]),
            Q_drift=abs(Q[-1] - Q[0]),
            I_drift=rel_drift(I),
            H0=H[0],
            ladder_criterion="V3/V4: дрейф ≤ 1e-10",
            passed=(
                rel_drift(H) <= 1e-10
                and rel_drift(I) <= 1e-10
                and abs(P[-1] - P[0]) <= 1e-10
                and abs(Q[-1] - Q[0]) <= 1e-10
            ),
        )
    else:
        # ньютоновские интегралы по кадрам
        energies = scene.energy_history
        e0 = energies[0] if energies else 0.0
        out["energy_drift_rel"] = abs(energies[-1] - e0) / max(abs(e0), 1e-30) if energies else 0.0

        # импульс/момент по первому и последнему кадру
        def momentum(state):
            px = py = pz = 0.0
            for i, s in enumerate(state):
                m = scene.bodies[i].mass if i < len(scene.bodies) else 1.0
                px += m * s[3]
                py += m * s[4]
                pz += m * s[5]
            return (px, py, pz)

        def angular(state):
            lx = ly = lz = 0.0
            for i, s in enumerate(state):
                m = scene.bodies[i].mass if i < len(scene.bodies) else 1.0
                x, y, z, vx, vy, vz = s
                lx += m * (y * vz - z * vy)
                ly += m * (z * vx - x * vz)
                lz += m * (x * vy - y * vx)
            return (lx, ly, lz)

        if scene.trajectory_history:
            p0 = momentum(scene.trajectory_history[0])
            p1 = momentum(scene.trajectory_history[-1])
            l0 = angular(scene.trajectory_history[0])
            l1 = angular(scene.trajectory_history[-1])
            out["momentum_drift"] = math.dist(p0, p1)
            out["angular_drift"] = math.dist(l0, l1)
    return out


# ═══════════════════════════════════════════════════════════════════════════
# 3. Расстояние между траекториями (сравнение сценариев)
# ═══════════════════════════════════════════════════════════════════════════
def trajectory_distance(traj_a, traj_b) -> dict[str, Any]:
    """L2/Hausdorff-расстояния между двумя Trajectory (по общим временам)."""
    if not traj_a.times or not traj_b.times:
        return dict(error="пустые траектории")
    n_common = min(len(traj_a.times), len(traj_b.times))
    l2 = 0.0
    max_d = 0.0
    for i in range(n_common):
        sa, sb = traj_a.states[i], traj_b.states[i]
        d = math.sqrt(sum((x - y) ** 2 for ra, rb in zip(sa, sb) for x, y in zip(ra[:3], rb[:3])))
        l2 += d * d
        max_d = max(max_d, d)
    return dict(
        frames_compared=n_common,
        l2=math.sqrt(l2),
        max_separation=max_d,
        mean_separation=math.sqrt(l2 / max(n_common, 1)),
    )


# ═══════════════════════════════════════════════════════════════════════════
# 4. Спектральные характеристики последовательности
# ═══════════════════════════════════════════════════════════════════════════
def dominant_periods(
    times: Sequence[float], values: Sequence[float], top: int = 3
) -> list[dict[str, float]]:
    """Доминирующие периоды через дискретное преобразование Фурье (простое,
    без numpy — годится для диагностики)."""
    n = len(values)
    if n < 8 or len(times) < n:
        return []
    dt = (times[-1] - times[0]) / max(n - 1, 1)
    mean_v = sum(values) / n
    centered = [v - mean_v for v in values]
    out = []
    for k in range(1, min(n // 2, 64)):
        re = sum(centered[i] * math.cos(2 * math.pi * k * i / n) for i in range(n))
        im = sum(centered[i] * math.sin(2 * math.pi * k * i / n) for i in range(n))
        power = (re * re + im * im) / (n * n)
        period = n * dt / k
        out.append(dict(freq=1.0 / period if period else 0.0, period=period, power=power))
    out.sort(key=lambda d: -d["power"])
    return out[:top]


def scene_summary_metrics(scene: Scene) -> dict[str, Any]:
    """Сводный пакет метрик сцены для отчёта."""
    out: dict[str, Any] = dict(n_bodies=scene.n, t_final=scene.t)
    out["integral_drifts"] = integral_drifts(scene)
    # межтелные расстояния: min/max/mean на последнем кадре
    if scene.trajectory_history:
        last = scene.trajectory_history[-1]
        ds = []
        for i in range(len(last)):
            for j in range(i + 1, len(last)):
                ds.append(math.dist(last[i][:3], last[j][:3]))
        if ds:
            out["distances"] = dict(min=min(ds), max=max(ds), mean=sum(ds) / len(ds))
    return out
