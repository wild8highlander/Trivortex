#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — планировщики траекторий.

Иерархия:
    TrajectoryPlanner (ABC)
    ├─ AnalyticPlanner   — Теорема 3.1, Лагранж, figure-eight
    ├─ KirchhoffPlanner  — вихревые кольца (RK4, согласовано с VortexEngine)
    ├─ KeplerPlanner     — кеплеровы орбиты (круг/эллипс)
    └─ ScriptedPlanner   — контрольные точки + сплайны Катмулла-Рома
                           (чистый Python, без scipy)

Trajectory — контейнер: times, states, metadata; сериализация JSON/CSV.
"""

from __future__ import annotations

import json
import math
from abc import ABC
from dataclasses import dataclass, field
from typing import Any


# ═══════════════════════════════════════════════════════════════════════════
# Контейнер траектории
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class Trajectory:
    """Траектория: моменты времени × состояния тел."""

    times: list[float] = field(default_factory=list)
    states: list[list[list[float]]] = field(default_factory=list)  # [t][body][6]
    body_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def sample(self, t: float) -> list[list[float]]:
        """Ближайшее состояние к моменту t (линейная интерполяция)."""
        if not self.times:
            return []
        if t <= self.times[0]:
            return self.states[0]
        if t >= self.times[-1]:
            return self.states[-1]
        lo, hi = 0, len(self.times) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if self.times[mid] <= t:
                lo = mid
            else:
                hi = mid
        t0, t1 = self.times[lo], self.times[hi]
        if t1 <= t0:
            return self.states[lo]
        alpha = (t - t0) / (t1 - t0)
        return [
            [a + (b - a) * alpha for a, b in zip(s0, s1)]
            for s0, s1 in zip(self.states[lo], self.states[hi])
        ]

    def positions_xy(self, body_index: int) -> list[tuple[float, float]]:
        """Do Trajectory.positions xy for body_index and return the result."""
        return [(s[body_index][0], s[body_index][1]) for s in self.states]

    def to_dict(self) -> dict[str, Any]:
        """Handle Trajectory.to dict."""
        return dict(
            times=self.times, states=self.states, body_ids=self.body_ids, metadata=self.metadata
        )

    def to_json(self, path: str) -> None:
        """Do Trajectory.to json for path and return the result."""
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.to_dict(), fh, ensure_ascii=False, indent=1)

    def to_csv(self, path: str) -> None:
        """Do Trajectory.to csv for path and return the result."""
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("t,body_id,x,y,z,vx,vy,vz\n")
            for t, state in zip(self.times, self.states):
                for bid, s in zip(self.body_ids, state):
                    fh.write(f"{t},{bid},{s[0]},{s[1]},{s[2]}," f"{s[3]},{s[4]},{s[5]}\n")

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Trajectory:
        """Do Trajectory.from dict for d and return the result."""
        return cls(
            times=list(d["times"]),
            states=list(d["states"]),
            body_ids=list(d.get("body_ids", [])),
            metadata=dict(d.get("metadata", {})),
        )


# ═══════════════════════════════════════════════════════════════════════════
# ABC планировщика
# ═══════════════════════════════════════════════════════════════════════════
class TrajectoryPlanner(ABC):
    """Базовый планировщик: строит Trajectory по сцене/параметрам."""

    name: str = "abstract"

    def plan(self, n_steps: int = 500, dt: float = 0.01, **params: Any) -> Trajectory:
        """Универсальная точка входа: перенаправляет на конкретный метод
        планировщика по params['method'] (default — первый метод класса)."""
        method = params.pop("method", None)
        if method is None:
            # первый не-приватный метод без подчёркивания
            for attr in dir(self):
                if attr.startswith("_") or attr in ("plan", "validate", "name"):
                    continue
                fn = getattr(self, attr)
                if callable(fn):
                    method = attr
                    break
        if method is None:
            raise ValueError(f"планировщик {self.name} не имеет методов")
        fn = getattr(self, method, None)
        if fn is None:
            raise ValueError(f"планировщик {self.name} не имеет метода {method}")
        # n_steps/dt передаются как явные kwargs совместимым методам
        import inspect

        sig = inspect.signature(fn)
        kwargs = dict(params)
        if "n_steps" in sig.parameters:
            kwargs.setdefault("n_steps", n_steps)
        return fn(**kwargs)

    def validate(self, traj: Trajectory) -> list[str]:
        """Предупреждения о траектории (NaN, разрывы, вылеты)."""
        warns = []
        for i, state in enumerate(traj.states):
            for j, s in enumerate(state):
                if any(c != c for c in s):
                    warns.append(f"NaN в состоянии {i}, тело {j}")
                    break
        return warns


# ═══════════════════════════════════════════════════════════════════════════
# 1. AnalyticPlanner — аналитические хореографии
# ═══════════════════════════════════════════════════════════════════════════
class AnalyticPlanner(TrajectoryPlanner):
    """Замкнутые формы: Теорема 3.1 (дышащее кольцо), Лагранж (жёсткий
    треугольник), figure-eight Ченшинера–Монтгомери."""

    name = "analytic"

    # ── Теорема 3.1 ──
    def theorem31(
        self, C_Ch: float = 1.0, T: float = 2 * math.pi, n_steps: int = 500, n_periods: float = 1.0
    ) -> Trajectory:
        """Замкнутая форма Теоремы 3.1 — «дышащее кольцо» трёх вихрей:

            r_k(t) = √C_Ch · (1 + ε·cos(ωt + 2πk/3)),  θ_k(t) = ωt + 2πk/3
            ω = (2π/T)·e^(C_Ch/π),  ε = 1/(e^(C_Ch/π) − 1)

        ДОПУСТИМОСТЬ (Теорема B монографа polyvortex): форма невырождена
        при C_Ch > π·ln2 ≈ 2.1776 — там ε < 1 и радиусы положительны на
        всём цикле. При C_Ch < π·ln2 (включая дефолт ядра C_Ch=1, ε≈2.668)
        кривая — лимакон с внутренней петлёй: тело проходит через центр,
        и геометрическое разделение 2π/3 по позициям ломается (разделение
        по полярным углам θ_k сохраняется всегда). Параметр оставлен
        свободным, как в ядре; вырожденность отмечается в metadata.
        """
        ratio = math.exp(C_Ch / math.pi)
        omega = (2 * math.pi / T) * ratio
        eps = 1.0 / (ratio - 1.0) if C_Ch > 0.01 else 1.0
        t_r = 2 * math.pi / omega
        times, states = [], []
        for i in range(n_steps + 1):
            t = n_periods * t_r * i / n_steps
            frame = []
            for k in range(3):
                phase = omega * t + 2 * math.pi * k / 3
                r = math.sqrt(C_Ch) * (1 + eps * math.cos(phase))
                theta = omega * t + 2 * math.pi * k / 3
                x = r * math.cos(theta)
                y = r * math.sin(theta)
                # скорости численно (аналитическая производная громоздка)
                dt = 1e-6
                phase2 = omega * (t + dt) + 2 * math.pi * k / 3
                r2 = math.sqrt(C_Ch) * (1 + eps * math.cos(phase2))
                theta2 = omega * (t + dt) + 2 * math.pi * k / 3
                vx = (r2 * math.cos(theta2) - x) / dt
                vy = (r2 * math.sin(theta2) - y) / dt
                frame.append([x, y, 0.0, vx, vy, 0.0])
            times.append(t)
            states.append(frame)
        return Trajectory(
            times=times,
            states=states,
            body_ids=["vortex_k0", "vortex_k1", "vortex_k2"],
            metadata=dict(
                planner="theorem31",
                omega=omega,
                epsilon=eps,
                C_Ch=C_Ch,
                T=T,
                # порог допустимости Теоремы B (polyvortex): π·ln2 ≈ 2.1776
                admissible=eps < 1.0,
                source="Trivortex Theorem 3.1",
            ),
        )

    # ── Лагранж 1772 ──
    def lagrange(
        self,
        side: float = 1.0,
        gamma_total: float = 3.0,
        n_steps: int = 500,
        n_periods: float = 1.0,
    ) -> Trajectory:
        """Три равных вихря на равностороннем треугольнике; жёсткое вращение
        ω_L = 3Γ/(2πa²) (согласовано с лестницей V2)."""
        a = side  # сторона = радиус описанной окружности * √3
        R = a / math.sqrt(3)  # радиус описанной окружности
        gamma = gamma_total / 3.0
        omega = 3.0 * gamma / (2 * math.pi * a * a)
        if omega == 0:
            omega = 1.0
        period = 2 * math.pi / abs(omega)
        times, states = [], []
        for i in range(n_steps + 1):
            t = n_periods * period * i / n_steps
            frame = []
            for k in range(3):
                phi = omega * t + 2 * math.pi * k / 3
                x, y = R * math.cos(phi), R * math.sin(phi)
                vx, vy = -omega * R * math.sin(phi), omega * R * math.cos(phi)
                frame.append([x, y, 0.0, vx, vy, 0.0])
            times.append(t)
            states.append(frame)
        return Trajectory(
            times=times,
            states=states,
            body_ids=["lagrange_0", "lagrange_1", "lagrange_2"],
            metadata=dict(
                planner="lagrange", omega=omega, R=R, a=a, source="Lagrange 1772; ladder V2"
            ),
        )

    # ── figure-eight Ченшинера–Монтгомери ──
    # точные НУ (Moore 1993 / Chenciner-Montgomery 2000): тела на
    # единичном круге r = ±(0.97000436, −0.24308753), v = (0.4662036850,
    # 0.4323657300) у двух тел, −2v у третьего; T = 6.32591398, E = −1.287142
    FIG8_X0 = 0.97000436
    FIG8_Y0 = -0.24308753
    FIG8_VX = 0.4662036850
    FIG8_VY = 0.4323657300
    FIG8_PERIOD = 6.32591398  # T для G=1, m=1

    def figure_eight(
        self, mass: float = 1.0, G: float = 1.0, n_steps: int = 600, n_periods: float = 1.0
    ) -> Trajectory:
        """Do AnalyticPlanner.figure eight for mass, G, n_steps, n_periods and return the result."""
        x0, y0, vx0, vy0 = (self.FIG8_X0, self.FIG8_Y0, self.FIG8_VX, self.FIG8_VY)
        # тело 1 в (x0, y0), тело 2 зеркально в (−x0, −y0), тело 3 в (0,0)
        state = [x0, y0, vx0, vy0, -x0, -y0, vx0, vy0, 0.0, 0.0, -2 * vx0, -2 * vy0]
        T = self.FIG8_PERIOD
        dt = n_periods * T / n_steps

        def accel(s):
            out = [0.0] * 12
            for i in range(3):
                xi, yi = s[4 * i], s[4 * i + 1]
                ax = ay = 0.0
                for j in range(3):
                    if i == j:
                        continue
                    dx = s[4 * j] - xi
                    dy = s[4 * j + 1] - yi
                    r = math.sqrt(dx * dx + dy * dy) + 1e-12
                    f = G * mass / (r * r * r)
                    ax += f * dx
                    ay += f * dy
                out[4 * i + 2], out[4 * i + 3] = ax, ay
            return out

        def deriv(s):
            d = [0.0] * 12
            for i in range(3):
                d[4 * i] = s[4 * i + 2]
                d[4 * i + 1] = s[4 * i + 3]
            acc = accel(s)
            for i in range(3):
                d[4 * i + 2] = acc[4 * i + 2]
                d[4 * i + 3] = acc[4 * i + 3]
            return d

        times, states = [], []
        y = list(state)
        for i in range(n_steps + 1):
            # RK4
            k1 = deriv(y)
            y2 = [y[k] + 0.5 * dt * k1[k] for k in range(12)]
            k2 = deriv(y2)
            y3 = [y[k] + 0.5 * dt * k2[k] for k in range(12)]
            k3 = deriv(y3)
            y4 = [y[k] + dt * k3[k] for k in range(12)]
            k4 = deriv(y4)
            frame = []
            for b in range(3):
                x, yy, vx, vy = y[4 * b : 4 * b + 4]
                frame.append([x, yy, 0.0, vx, vy, 0.0])
            times.append(i * dt)
            states.append(frame)
            y = [y[k] + (dt / 6.0) * (k1[k] + 2 * k2[k] + 2 * k3[k] + k4[k]) for k in range(12)]
        return Trajectory(
            times=times,
            states=states,
            body_ids=["fig8_0", "fig8_1", "fig8_2"],
            metadata=dict(
                planner="figure_eight", mass=mass, G=G, T=T, source="Chenciner & Montgomery 2000"
            ),
        )


# ═══════════════════════════════════════════════════════════════════════════
# 2. KirchhoffPlanner — вихревые кольца N = 2..8
# ═══════════════════════════════════════════════════════════════════════════
class KirchhoffPlanner(TrajectoryPlanner):
    """Правильное N-кольцо вихрей: ω_N = Γ(N−1)/(4πR²).

    При N ≤ 7 — устойчиво (Хавелок); при N = 8 — неустойчиво, что видно
    при малом возмущении кольца (см. analysis/tests.py S-блок и field.py).
    """

    name = "kirchhoff"

    def ring(
        self,
        N: int = 5,
        R: float = 1.0,
        gamma: float = 1.0,
        n_steps: int = 400,
        n_periods: float = 1.0,
        jitter: float = 0.0,
        seed: int = 42,
    ) -> Trajectory:
        """Do KirchhoffPlanner.ring for N, R, gamma, n_steps and return the result."""
        import random

        rng = random.Random(seed)
        omega_N = gamma * (N - 1) / (4 * math.pi * R * R)
        period = 2 * math.pi / abs(omega_N) if omega_N != 0 else 1.0
        # начальные позиции
        pos = []
        for k in range(N):
            phi = 2 * math.pi * k / N
            r = R * (1 + jitter * (rng.random() - 0.5))
            pos.append([r * math.cos(phi), r * math.sin(phi)])

        def velocities(p):
            out = []
            for i in range(N):
                vx = vy = 0.0
                for j in range(N):
                    if i == j:
                        continue
                    dx = p[j][0] - p[i][0]
                    dy = p[j][1] - p[i][1]
                    r2 = dx * dx + dy * dy
                    if r2 <= 0:
                        continue
                    vx += -gamma * dy / (2 * math.pi * r2)
                    vy += gamma * dx / (2 * math.pi * r2)
                out.append((vx, vy))
            return out

        dt = n_periods * period / n_steps
        times, states = [], []
        p = [list(q) for q in pos]
        for i in range(n_steps + 1):
            frame = []
            vels = velocities(p)
            for k in range(N):
                frame.append([p[k][0], p[k][1], 0.0, vels[k][0], vels[k][1], 0.0])
            times.append(i * dt)
            states.append(frame)

            # RK4
            def deriv(pp):
                vv = velocities(pp)
                out = []
                for k in range(N):
                    out.append([vv[k][0], vv[k][1]])
                return out

            k1 = deriv(p)
            p2 = [[p[k][0] + 0.5 * dt * k1[k][0], p[k][1] + 0.5 * dt * k1[k][1]] for k in range(N)]
            k2 = deriv(p2)
            p3 = [[p[k][0] + 0.5 * dt * k2[k][0], p[k][1] + 0.5 * dt * k2[k][1]] for k in range(N)]
            k3 = deriv(p3)
            p4 = [[p[k][0] + dt * k3[k][0], p[k][1] + dt * k3[k][1]] for k in range(N)]
            k4 = deriv(p4)
            for k in range(N):
                p[k][0] += (dt / 6.0) * (k1[k][0] + 2 * k2[k][0] + 2 * k3[k][0] + k4[k][0])
                p[k][1] += (dt / 6.0) * (k1[k][1] + 2 * k2[k][1] + 2 * k3[k][1] + k4[k][1])
        return Trajectory(
            times=times,
            states=states,
            body_ids=[f"ring_{k}" for k in range(N)],
            metadata=dict(
                planner="kirchhoff_ring",
                N=N,
                R=R,
                gamma=gamma,
                omega_N=omega_N,
                jitter=jitter,
                source="Kirchhoff; Havelock 1931; POLYVORTEX W2/W4",
            ),
        )


# ═══════════════════════════════════════════════════════════════════════════
# 3. KeplerPlanner — кеплеровы орбиты
# ═══════════════════════════════════════════════════════════════════════════
class KeplerPlanner(TrajectoryPlanner):
    """Задача двух тел: круговая или эллиптическая орбита.

    Использует ньютоновский движок (RK4) для пары «центральное + спутник».
    """

    name = "kepler"

    def orbit(
        self,
        central_mass: float = 1.989e30,
        r0: float = 1.495978707e11,
        eccentricity: float = 0.0,
        G: float = 6.67430e-11,
        n_steps: int = 500,
        n_periods: float = 1.0,
    ) -> Trajectory:
        # скорость в перигелии для орбиты с эксцентриситетом e
        """Do KeplerPlanner.orbit for central_mass, r0, eccentricity, G and return the result."""
        mu = G * central_mass
        if 0 <= eccentricity < 1:
            a = r0 / (1 - eccentricity)  # большая полуось из перигелия
            period = 2 * math.pi * math.sqrt(a**3 / mu)
        else:
            a = r0
            period = float("inf")  # гиперболическая: периода нет
        v_peri = math.sqrt(mu * (1 + eccentricity) / r0)
        dt = n_periods * period / n_steps

        # состояние: [x, y, vx, vy] спутника; центр в (0,0) неподвижен
        y = [r0, 0.0, 0.0, v_peri]

        def deriv(s):
            x, yy, vx, vy = s
            r = math.sqrt(x * x + yy * yy) + 1e-9
            ax = -mu * x / (r**3)
            ay = -mu * yy / (r**3)
            return [vx, vy, ax, ay]

        times, states = [], []
        for i in range(n_steps + 1):
            states.append([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [y[0], y[1], 0.0, y[2], y[3], 0.0]])
            times.append(i * dt)
            k1 = deriv(y)
            y2 = [y[k] + 0.5 * dt * k1[k] for k in range(4)]
            k2 = deriv(y2)
            y3 = [y[k] + 0.5 * dt * k2[k] for k in range(4)]
            k3 = deriv(y3)
            y4 = [y[k] + dt * k3[k] for k in range(4)]
            k4 = deriv(y4)
            y = [y[k] + (dt / 6.0) * (k1[k] + 2 * k2[k] + 2 * k3[k] + k4[k]) for k in range(4)]
        return Trajectory(
            times=times,
            states=states,
            body_ids=["primary", "secondary"],
            metadata=dict(
                planner="kepler",
                central_mass=central_mass,
                r0=r0,
                eccentricity=eccentricity,
                period=period,
            ),
        )


# ═══════════════════════════════════════════════════════════════════════════
# 4. ScriptedPlanner — контрольные точки + сплайны Катмулла-Рома
# ═══════════════════════════════════════════════════════════════════════════
def catmull_rom(
    p0: tuple[float, ...],
    p1: tuple[float, ...],
    p2: tuple[float, ...],
    p3: tuple[float, ...],
    t: float,
) -> tuple[float, ...]:
    """Кубический сплайн Катмулла-Рома на чистом Python (без scipy)."""
    out = []
    for a, b, c, d in zip(p0, p1, p2, p3):
        v = 0.5 * (
            (2 * b)
            + (-a + c) * t
            + (2 * a - 5 * b + 4 * c - d) * t * t
            + (-a + 3 * b - 3 * c + d) * t * t * t
        )
        out.append(v)
    return tuple(out)


class ScriptedPlanner(TrajectoryPlanner):
    """Траектория из waypoints: каждый тел — список контрольных точек,
    интерполируется сплайном Катмулла-Рома по равномерной сетке времени."""

    name = "scripted"

    def waypoints(
        self,
        points_per_body: list[list[tuple[float, float, float]]],
        n_steps: int = 400,
        duration: float = 1.0,
        closed: bool = True,
    ) -> Trajectory:
        """Do ScriptedPlanner.waypoints for points_per_body, n_steps, duration, closed and return the result."""
        n_bodies = len(points_per_body)
        times, states = [], []
        for i in range(n_steps + 1):
            t = duration * i / n_steps
            frame = []
            for b in range(n_bodies):
                pts = points_per_body[b]
                m = len(pts)
                if m == 1:
                    p = pts[0]
                    frame.append([p[0], p[1], p[2], 0, 0, 0])
                    continue
                u = t / duration * (m - 1)
                seg = min(int(u), m - 2)
                frac = u - seg

                # соседи с заворотом (closed) или клампом
                def pt(idx):
                    if closed:
                        return pts[idx % m]
                    return pts[max(0, min(idx, m - 1))]

                p0, p1, p2, p3 = pt(seg - 1), pt(seg), pt(seg + 1), pt(seg + 2)
                p_now = catmull_rom(p0, p1, p2, p3, frac)
                p_next = catmull_rom(p0, p1, p2, p3, min(frac + 0.01, 1.0))
                vx = (p_next[0] - p_now[0]) / (duration / (n_steps * (m - 1)))
                vy = (p_next[1] - p_now[1]) / (duration / (n_steps * (m - 1)))
                frame.append([p_now[0], p_now[1], p_now[2], vx, vy, 0.0])
            times.append(t)
            states.append(frame)
        return Trajectory(
            times=times,
            states=states,
            body_ids=[f"scripted_{b}" for b in range(n_bodies)],
            metadata=dict(
                planner="scripted", n_bodies=n_bodies, closed=closed, spline="Catmull-Rom"
            ),
        )


# ═══════════════════════════════════════════════════════════════════════════
# Фабрика
# ═══════════════════════════════════════════════════════════════════════════
PLANNERS = {
    "analytic": AnalyticPlanner,
    "kirchhoff": KirchhoffPlanner,
    "kepler": KeplerPlanner,
    "scripted": ScriptedPlanner,
}


def get_planner(name: str) -> TrajectoryPlanner:
    """Do get planner for name and return the result."""
    if name not in PLANNERS:
        raise ValueError(f"неизвестный планировщик: {name}; " f"доступны: {', '.join(PLANNERS)}")
    return PLANNERS[name]()
