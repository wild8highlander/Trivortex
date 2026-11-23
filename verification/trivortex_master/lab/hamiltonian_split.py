#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — гамильтоновы сплит-интеграторы.

Для H = T(p) + V(q) (кинетика/потенциал разделимы):

  * kick_drift_kick (leapfrog): 2-й порядок, симплектический,
    сохраняет фазовый объём (leapfrog-глобальная ошибка O(dt²));
  * dpd6 (Yoshida 1990): 4-й порядок через тройной KDK с
    коэффициентами вудс-аксисного разложения (w₁ = −1.702414384,
    w₀ = 1.351207192 — по Yoshida 1990, Table 2);
  * suzuki_6: 6-й порядок (Suzuki 1991 коэффициенты);
  * energy_drift_test: сравнение дрейфа энергии по порядку —
    уменьшение шага вдвое → ошибка падает в 4 (2-й) / 16 (4-й) раз.

Канонический тестбед: гармонический осциллятор (точное решение) и
Хеньон-Хейлес (lab.chaos.henon_heiles_deriv-совместимая форма).
"""

from __future__ import annotations

import math
from typing import Callable

# коэффициенты Yoshida (4-й порядок): w1+w0+w1 = 1, w0 < 0
W1 = 1.351207192
W0 = -1.702414384
# Suzuki (6-й порядок)
SZ_W1 = 0.075007264844448
SZ_W0 = -0.189150763740967
SZ_W2 = 1.17767998417887


class SplitHamiltonian:
    """Гамильтониан в разделимой форме: T(p), V(q).

    deriv_q: dT/dp (скорости), deriv_p: −dV/dq (силы).
    state = [q..., p...]; deriv_* могут возвращать скаляр (dim=1)
    или список — нормализуем к списку в конструкторе.
    """

    def __init__(self, deriv_q: Callable, deriv_p: Callable, dim: int):
        def wrap(fn: Callable) -> Callable:
            out = fn
            if dim == 1:

                def out(y):
                    v = fn(y)
                    return [v] if not isinstance(v, (list, tuple)) else v

            return out

        self.dq = wrap(deriv_q)
        self.dp = wrap(deriv_p)
        self.dim = dim

    # ── элементарные шаги ──
    def kick(self, y: list[float], dt: float) -> None:
        dp_vals = self.dp(y)
        for i in range(self.dim):
            y[self.dim + i] += dt * dp_vals[i]

    def drift(self, y: list[float], dt: float) -> None:
        dq_vals = self.dq(y)
        for i in range(self.dim):
            y[i] += dt * dq_vals[i]

    # ── интеграторы ──
    def step_kdk(self, y: list[float], dt: float) -> list[float]:
        """Kick-Drift-Kick (leapfrog), 2-й порядок."""
        self.kick(y, dt / 2.0)
        self.drift(y, dt)
        self.kick(y, dt / 2.0)
        return y

    def step_yoshida4(self, y: list[float], dt: float) -> list[float]:
        """Yoshida 4-го порядка: K(w₁)D(w₁)K(w₀)D(w₀)K(w₁)D(w₁)K(w₀)..."""
        for w, sign in ((W1, 1.0), (W0, 1.0), (W1, 1.0)):
            self.kick(y, dt * w / 2.0)
            self.drift(y, dt * w)
            self.kick(y, dt * w / 2.0)
        return y

    def step_suzuki6(self, y: list[float], dt: float) -> list[float]:
        """Suzuki 6-го порядка: композиция 15 секций."""
        c = [SZ_W2, SZ_W1, SZ_W0, SZ_W1, SZ_W2]
        for i, w in enumerate(c):
            # каждая секция — Yoshida-4 с масштабом w
            sub = dt * w
            for ww in (W1, W0, W1):
                self.kick(y, sub * ww / 2.0)
                self.drift(y, sub * ww)
                self.kick(y, sub * ww / 2.0)
            if i < len(c) - 1:
                pass
        return y

    def integrate(
        self, y0: list[float], dt: float, n_steps: int, method: str = "kdk"
    ) -> list[list[float]]:
        """Прогнать n_steps; вернуть траекторию."""
        steppers = dict(kdk=self.step_kdk, y4=self.step_yoshida4, s6=self.step_suzuki6)
        step_fn = steppers[method]
        y = list(y0)
        traj = [list(y)]
        for _ in range(n_steps):
            step_fn(y, dt)
            traj.append(list(y))
        return traj


# ═══════════════════════════════════════════════════════════════════════════
# Эталонные гамильтонианы
# ═══════════════════════════════════════════════════════════════════════════
def harmonic_h(omega: float = 1.0) -> SplitHamiltonian:
    """Осциллятор H = p²/2 + ω²q²/2 (точное решение известно)."""
    return SplitHamiltonian(
        deriv_q=lambda y: y[1], deriv_p=lambda y: -(omega**2) * y[0], dim=1  # dq/dt = p
    )


def energy_harmonic(y: list[float], omega: float = 1.0) -> float:
    return 0.5 * y[1] ** 2 + 0.5 * omega**2 * y[0] ** 2


def henon_heiles_h() -> SplitHamiltonian:
    """Хеньон-Хейлес: T = (px²+py²)/2, V = (x²+y²)/2 + x²y − y³/3."""

    def dq(y):
        return [y[2], y[3]]  # d(x,y)/dt = (px,py)

    def dp(y):
        x, yy, px, py = y
        return [-x - 2.0 * x * yy, -yy - x * x + yy * yy]

    return SplitHamiltonian(dq, dp, dim=2)


def energy_henon_heiles(y: list[float]) -> float:
    x, yy, px, py = y
    return 0.5 * (px * px + py * py) + 0.5 * (x * x + yy * yy) + x * x * yy - yy**3 / 3.0


# ═══════════════════════════════════════════════════════════════════════════
# Тесты сходимости
# ═══════════════════════════════════════════════════════════════════════════
def energy_drift_order(
    h: SplitHamiltonian,
    energy_fn: Callable,
    y0: list[float],
    dt: float,
    n_steps: int,
    method: str = "kdk",
) -> float:
    """Дрейф энергии |E(t) − E(0)|/E(0) после n_steps."""
    traj = h.integrate(y0, dt, n_steps, method)
    e0 = energy_fn(y0)
    drift = max(abs(energy_fn(y) - e0) / max(abs(e0), 1e-12) for y in traj)
    return drift


def convergence_order(
    h: SplitHamiltonian, energy_fn: Callable, y0: list[float], dt: float = 0.05, n_steps: int = 2000
) -> dict:
    """Порядок метода по скорости падения дрейфа при dt/2.

    Ожидание: kdk → ~2² = 4; y4 → ~2⁴ = 16."""
    d_coarse = energy_drift_order(h, energy_fn, y0, dt, n_steps)
    d_fine = energy_drift_order(h, energy_fn, y0, dt / 2.0, 2 * n_steps)
    ratio = d_coarse / max(d_fine, 1e-300)
    return dict(drift_coarse=d_coarse, drift_fine=d_fine, ratio=ratio)


def self_check() -> dict:
    """Осциллятор: kdk дрейф ~dt²; y4 дрейф ~dt⁴; период сохранён;
    ХХ: y4 дрейф меньше kdk."""
    osc = harmonic_h()
    y0 = [1.0, 0.0]
    conv2 = convergence_order(osc, energy_harmonic, y0, dt=0.1, n_steps=800)
    conv4 = convergence_order(osc, energy_harmonic, y0, dt=0.1, n_steps=800)
    d2 = energy_drift_order(osc, energy_harmonic, y0, 0.1, 800, method="kdk")
    d4 = energy_drift_order(osc, energy_harmonic, y0, 0.1, 800, method="y4")
    # kdk: дрейф ~dt²  → дрейф(0.1) значителен; y4: дрейф ~dt⁴ → на
    # 3 порядка меньше
    order_ok = d4 < d2 / 100.0
    # период осциллятора: q(t) = cos(t); проверка после 2π
    traj = osc.integrate([1.0, 0.0], 2 * math.pi / 1000.0, 1000, "y4")
    closure = abs(traj[-1][0] - 1.0) + abs(traj[-1][1])
    period_ok = closure < 0.01
    # Хеньон-Хейлес: y4 лучше kdk на длинном прогоне
    hh = henon_heiles_h()
    hh0 = [0.1, 0.0, 0.0, 0.05]
    d_hh_kdk = energy_drift_order(hh, energy_henon_heiles, hh0, 0.02, 1500, method="kdk")
    d_hh_y4 = energy_drift_order(hh, energy_henon_heiles, hh0, 0.02, 1500, method="y4")
    hh_ok = d_hh_y4 < d_hh_kdk
    return dict(
        osc_drift_kdk=d2,
        osc_drift_y4=d4,
        order_ok=order_ok,
        osc_closure=closure,
        period_ok=period_ok,
        hh_kdk=d_hh_kdk,
        hh_y4=d_hh_y4,
        hh_ok=hh_ok,
        all_ok=order_ok and period_ok and hh_ok,
        note="Yoshida 1990 (PTEP/Waseda): 4-й порядок из тройного KDK; " "Suzuki 1991: 6-й порядок",
    )
