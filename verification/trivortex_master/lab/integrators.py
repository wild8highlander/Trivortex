#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — интеграторы: симплектические и адаптивные.

Семейство интеграторов для ньютоновской N-телевой задачи, каждый со своей
нишей и честным контролем ошибки:

  * Leapfrog (kick-drift-kick) — 2-й порядок, симплектический:
    энергия колеблется, но не дрейфует — золотой стандарт орбит;
  * VelocityVerlet — эквивалент leapfrog в другой нумерации;
  * Yoshida4 — 4-й порядок, симплектический (композиция leapfrog c
    коэффициентами Йосиды w1 = 1/(2−2^(1/3)));
  * RK45Adaptive — адаптивный шаг по вложенной паре Рунге–Кутты
    (Dormand–Prince упрощённый): контроль локальной ошибки tol,
    удвоение/деление шага пополам;
  * EnergyGuard — обёртка над любым интегратором: откат шага и
    уменьшение dt при скачке энергии (защита от близких пролётов).

Все интеграторы работают с плоским вектором состояния y = [x,y,z,vx,vy,vz]*N
и правой частью вида deriv(y, t) -> dy/dt — без привязки к конкретной
физике (гравитация подключается снаружи).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Sequence

Deriv = Callable[[Sequence[float], float], list[float]]


# ═══════════════════════════════════════════════════════════════════════════
# Классический RK4 (для сравнения и как внутренний шаг)
# ═══════════════════════════════════════════════════════════════════════════
def rk4_step(deriv: Deriv, y: list[float], t: float, dt: float) -> tuple[list[float], float]:
    """Один шаг RK4; возвращает (новое y, новое t)."""
    n = len(y)
    k1 = deriv(y, t)
    y2 = [y[i] + 0.5 * dt * k1[i] for i in range(n)]
    k2 = deriv(y2, t + 0.5 * dt)
    y3 = [y[i] + 0.5 * dt * k2[i] for i in range(n)]
    k3 = deriv(y3, t + 0.5 * dt)
    y4 = [y[i] + dt * k3[i] for i in range(n)]
    k4 = deriv(y4, t + dt)
    y_new = [y[i] + (dt / 6.0) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(n)]
    return y_new, t + dt


# ═══════════════════════════════════════════════════════════════════════════
# Leapfrog / velocity Verlet (симплектические)
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class LeapfrogStats:
    """Статистика прогона симплектического интегратора."""

    steps: int = 0
    rejected: int = 0
    e_min: float = float("inf")
    e_max: float = float("-inf")

    def energy_span(self) -> float:
        if self.e_max < self.e_min:
            return 0.0
        return self.e_max - self.e_min


class Leapfrog:
    """Kick–Drift–Kick: 2-й порядок, симплектический, энергия не дрейфует.

    Требует правую часть, разделённую на ускорения и скорости:
    для гравитации accel(pos) -> list[(ax,ay,az)].
    """

    name = "leapfrog_kdk"

    def __init__(self, accel: Callable[[list, float], list], n_bodies: int):
        self.accel = accel
        self.n = n_bodies
        self.stats = LeapfrogStats()

    def step(self, y: list[float], t: float, dt: float) -> tuple[list[float], float]:
        """y = [x,y,z,vx,vy,vz]*N; KDK-схема."""
        n6 = self.n * 6
        pos = [y[i] * 1.0 for i in range(n6)]
        # разбить на позиции и скорости
        xs = [y[6 * i + j] for i in range(self.n) for j in range(3)]
        vs = [y[6 * i + 3 + j] for i in range(self.n) for j in range(3)]
        # half-kick по текущим ускорениям
        acc = self.accel(_to_positions(y, self.n), t)
        vs2 = [vs[3 * i + j] + 0.5 * dt * acc[i][j] for i in range(self.n) for j in range(3)]
        # drift
        xs2 = [xs[3 * i + j] + dt * vs2[3 * i + j] for i in range(self.n) for j in range(3)]
        # half-kick по новым ускорениям
        y_mid = _pack(xs2, vs2, self.n)
        acc2 = self.accel(_to_positions(y_mid, self.n), t + dt)
        vs3 = [vs2[3 * i + j] + 0.5 * dt * acc2[i][j] for i in range(self.n) for j in range(3)]
        y_new = _pack(xs2, vs3, self.n)
        self.stats.steps += 1
        return y_new, t + dt


class VelocityVerlet(Leapfrog):
    """Velocity Verlet — переупорядоченный leapfrog (позиции-первыми)."""

    name = "velocity_verlet"

    def step(self, y: list[float], t: float, dt: float) -> tuple[list[float], float]:
        # алгебраически эквивалентен KDK; отдельный класс для ясности API
        return super().step(y, t, dt)


# коэффициенты Йосиды 4-го порядка (композиция симплектических шагов)
_W1 = 1.0 / (2.0 - 2.0 ** (1.0 / 3.0))
_W0 = -(2.0 ** (1.0 / 3.0)) / (2.0 - 2.0 ** (1.0 / 3.0))


class Yoshida4:
    """Симплектический интегратор 4-го порядка (Yoshida 1990).

    Композиция трёх leapfrog-шагов с весами (w1, w0, w1):
    сохраняет структуру гамильтонового потока, ошибка энергии ~dt⁴.
    """

    name = "yoshida4"

    def __init__(self, accel: Callable[[list, float], list], n_bodies: int):
        self.lf = Leapfrog(accel, n_bodies)

    def step(self, y: list[float], t: float, dt: float) -> tuple[list[float], float]:
        # композиция: dt1 = w1*dt, dt2 = w0*dt, dt3 = w1*dt
        y1, t1 = self.lf.step(y, t, _W1 * dt)
        y2, t2 = self.lf.step(y1, t1, _W0 * dt)
        y3, t3 = self.lf.step(y2, t2, _W1 * dt)
        # t3 == t + dt точно (w1+w0+w1 = 1)
        return y3, t + dt


def _to_positions(y: Sequence[float], n: int) -> list[tuple[float, ...]]:
    return [tuple(y[6 * i : 6 * i + 3]) for i in range(n)]


def _pack(xs: Sequence[float], vs: Sequence[float], n: int) -> list[float]:
    out = []
    for i in range(n):
        out.extend(xs[3 * i : 3 * i + 3])
        out.extend(vs[3 * i : 3 * i + 3])
    return out


# ═══════════════════════════════════════════════════════════════════════════
# Адаптивный RK45 (вложенная пара)
# ═══════════════════════════════════════════════════════════════════════════
# Таблица Бутчера вложенной пары (упрощённая Fehlberg-подобная 5(4)):
_A = [
    [],
    [1.0 / 4.0],
    [3.0 / 32.0, 9.0 / 32.0],
    [1932.0 / 2197.0, -7200.0 / 2197.0, 7296.0 / 2197.0],
    [439.0 / 216.0, -8.0, 3680.0 / 513.0, -845.0 / 4104.0],
    [-8.0 / 27.0, 2.0, -3544.0 / 2565.0, 1859.0 / 4104.0, -11.0 / 40.0],
]
_C = [0.0, 1.0 / 4.0, 3.0 / 8.0, 12.0 / 13.0, 1.0, 1.0 / 2.0]
_B5 = [16.0 / 135.0, 0.0, 6656.0 / 12825.0, 28561.0 / 56430.0, -9.0 / 50.0, 2.0 / 55.0]
_B4 = [25.0 / 216.0, 0.0, 1408.0 / 2565.0, 2197.0 / 4104.0, -1.0 / 5.0, 0.0]


@dataclass
class AdaptiveStats:
    accepted: int = 0
    rejected: int = 0
    dt_min: float = float("inf")
    dt_max: float = 0.0

    def update(self, dt: float, ok: bool) -> None:
        if ok:
            self.accepted += 1
            self.dt_min = min(self.dt_min, dt)
            self.dt_max = max(self.dt_max, dt)
        else:
            self.rejected += 1


class RK45Adaptive:
    """Адаптивный Рунге–Кутта 5(4): шаг подбирается под локальную ошибку.

    err = max|y5 - y4| / scale, scale_i = tol*(1+|y_i|);
    шаг умножается на clamp(0.9*err^(-1/5), 0.2, 5).
    """

    name = "rk45_adaptive"

    def __init__(self, deriv: Deriv, tol: float = 1e-9):
        self.deriv = deriv
        self.tol = tol
        self.stats = AdaptiveStats()

    def _stages(self, y: Sequence[float], t: float, dt: float) -> list[list[float]]:
        n = len(y)
        ks: list[list[float]] = []
        for s in range(6):
            if s == 0:
                ys = list(y)
            else:
                ys = [
                    y[i] + dt * sum(_A[s][j] * ks[j][i] for j in range(s) if _A[s][j])
                    for i in range(n)
                ]
            ks.append(self.deriv(ys, t + _C[s] * dt))
        return ks

    def step(self, y: list[float], t: float, dt: float) -> tuple[list[float], float, float]:
        """Возвращает (y_new, t_new, err); err — оценка локальной ошибки."""
        ks = self._stages(y, t, dt)
        n = len(y)
        y5 = [y[i] + dt * sum(_B5[j] * ks[j][i] for j in range(6)) for i in range(n)]
        y4 = [y[i] + dt * sum(_B4[j] * ks[j][i] for j in range(5) if _B4[j]) for i in range(n)]
        err = max(abs(y5[i] - y4[i]) / max(self.tol * (1.0 + abs(y[i])), 1e-30) for i in range(n))
        return y5, t + dt, err

    def integrate(
        self, y: list[float], t: float, dt: float, duration: float, callback=None
    ) -> tuple[list[float], float]:
        """Прогон с адаптацией шага до t+duration."""
        t_end = t + duration
        while t < t_end - 1e-15:
            dt = min(dt, t_end - t)
            y_new, t_new, err = self.step(y, t, dt)
            if err <= 1.0:
                y, t = y_new, t_new
                self.stats.update(dt, True)
                if callback is not None:
                    callback(y, t)
                dt *= max(0.2, min(5.0, 0.9 * err ** (-0.2)))
            else:
                self.stats.update(dt, False)
                dt *= max(0.2, 0.9 * err ** (-0.25))
        return y, t


# ═══════════════════════════════════════════════════════════════════════════
# EnergyGuard — защита от скачков энергии
# ═══════════════════════════════════════════════════════════════════════════
class EnergyGuard:
    """Обёртка: откатывает шаг и режет dt при взрыве энергии.

    Типичный сценарий — тесные сближения: фиксированный шаг даёт
    нефизический скачок; гвард проверяет |ΔE/E| за шаг и при превышении
    порога возвращает состояние до шага и уменьшает dt.
    """

    def __init__(
        self,
        stepper,
        energy_of: Callable[[Sequence[float]], float],
        rel_threshold: float = 0.02,
        dt_min: float = 1e-12,
    ):
        self.stepper = stepper  # любой объект с .step(y, t, dt)
        self.energy_of = energy_of
        self.rel_threshold = rel_threshold
        self.dt_min = dt_min
        self.n_rejected = 0

    def step(self, y: list[float], t: float, dt: float) -> tuple[list[float], float, float]:
        """Возвращает (y_new, t_new, dt_used)."""
        e0 = self.energy_of(y)
        while dt >= self.dt_min:
            y_new, t_new = self.stepper.step(y, t, dt)
            e1 = self.energy_of(y_new)
            denom = max(abs(e0), 1e-30)
            if abs(e1 - e0) / denom <= self.rel_threshold:
                return y_new, t_new, dt
            self.n_rejected += 1
            dt *= 0.5
        # dt исчерпан — принимаем последний шаг (лучше, чем зависнуть)
        y_new, t_new = self.stepper.step(y, t, dt)
        return y_new, t_new, dt


# ═══════════════════════════════════════════════════════════════════════════
# Сравнение интеграторов (для тестов и отчётов)
# ═══════════════════════════════════════════════════════════════════════════
def compare_integrators(
    deriv: Deriv,
    accel: Callable[[list, float], list],
    energy_of,
    y0: list[float],
    t0: float,
    dt: float,
    n_steps: int,
    n_bodies: int,
) -> dict:
    """Прогнать RK4/leapfrog/Yoshida4/RK45 на одной задаче.

    deriv  — полная правая часть (для RK4/RK45);
    accel  — ускорения по списку позиций (для симплектических схем);
    их нужно передавать ОБЕ: адаптер «positions→deriv» невозможен
    (правая часть зависит и от скоростей).
    """
    e0 = energy_of(y0)

    results = {}

    # RK4
    y = list(y0)
    t = t0
    for _ in range(n_steps):
        y, t = rk4_step(deriv, y, t, dt)
    results["rk4"] = dict(energy_drift=abs(energy_of(y) - e0) / max(abs(e0), 1e-30))

    # leapfrog
    lf = Leapfrog(accel, n_bodies)
    y = list(y0)
    t = t0
    for _ in range(n_steps):
        y, t = lf.step(y, t, dt)
    results["leapfrog"] = dict(energy_drift=abs(energy_of(y) - e0) / max(abs(e0), 1e-30))

    # Yoshida4
    yo = Yoshida4(accel, n_bodies)
    y = list(y0)
    t = t0
    for _ in range(n_steps):
        y, t = yo.step(y, t, dt)
    results["yoshida4"] = dict(energy_drift=abs(energy_of(y) - e0) / max(abs(e0), 1e-30))

    # RK45 адаптивный
    rk = RK45Adaptive(deriv, tol=1e-9)
    y, t = rk.integrate(list(y0), t0, dt, n_steps * dt)
    results["rk45"] = dict(
        energy_drift=abs(energy_of(y) - e0) / max(abs(e0), 1e-30),
        accepted=rk.stats.accepted,
        rejected=rk.stats.rejected,
    )
    return results
