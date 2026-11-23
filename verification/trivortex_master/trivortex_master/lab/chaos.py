#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — инструменты хаоса: Пуанкаре, FLI, частотный анализ Ласкара.

Методы диагностики динамических систем поверх любой правой части:

  * PoincareMap — сечение Пуанкаре (пересечения плоскости Σ в одну
    сторону): странные множества vs гладкие кривые;
  * FLI (Fast Lyapunov Indicator, Froeschlé et al. 2000) — рост
    отклонения соседней траектории за фиксированное время: быстрый
    индикатор хаоса, не требующий выхода на асимптотику λ;
  * Laskar frequency analysis — скользящее окно DFT: дрейф основной
    частоты выдаёт диффузию (Ласкар 1990, Icarus 88, 266);
  * Численно: λ_max (Бенеттин, уже в analysis.metrics) + SALSA-like
    локальный индекс (упрощённый).

Пример: резонансы Хеньона-Хейлеса, Козаи-Лидов, кольца Хавелока.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Sequence

Deriv = Callable[[Sequence[float], float], list[float]]


# ═══════════════════════════════════════════════════════════════════════════
# Сечение Пуанкаре
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class PoincarePoint:
    t: float
    coords: tuple[float, ...]    # координаты в сечении (без ведущей)


class PoincareMap:
    """Сечение Пуанкаре для автономной системы с плоскостью q_i = q0.

    Ловит пересечения q[k] − level со сменой знака «снизу вверх»,
    уточняет момент линейной интерполяцией и записывает остальные
    координаты как точку сечения.
    """

    def __init__(self, deriv: Deriv, step_dt: float,
                 axis: int = 0, level: float = 0.0,
                 upward: bool = True):
        self.deriv = deriv
        self.dt = step_dt
        self.axis = axis
        self.level = level
        self.upward = upward
        self.points: list[PoincarePoint] = []
        self._prev_state: list[float] | None = None
        self._prev_t: float = 0.0

    def _rk4(self, y: list[float], t: float, dt: float) -> list[float]:
        k1 = self.deriv(y, t)
        y2 = [y[i] + 0.5 * dt * k1[i] for i in range(len(y))]
        k2 = self.deriv(y2, t + 0.5 * dt)
        y3 = [y[i] + 0.5 * dt * k2[i] for i in range(len(y))]
        k4_pre = self.deriv(y3, t + 0.5 * dt)
        y4 = [y[i] + dt * k4_pre[i] for i in range(len(y))]
        k4 = self.deriv(y4, t + dt)
        return [y[i] + dt / 6.0 * (k1[i] + 2 * k2[i] + 2 * k4_pre[i]
                                   + k4[i]) for i in range(len(y))]

    def run(self, y0: list[float], t0: float, n_steps: int,
            max_points: int = 500) -> list[PoincarePoint]:
        """Прогнать траекторию и собрать точки сечения."""
        y = list(y0)
        t = t0
        self.points = []
        prev_val = y[self.axis] - self.level
        for i in range(n_steps):
            y_new = self._rk4(y, t, self.dt)
            t_new = t + self.dt
            cur_val = y_new[self.axis] - self.level
            crossed_up = self.upward and prev_val < 0 <= cur_val
            crossed_down = (not self.upward) and prev_val > 0 >= cur_val
            if crossed_up or crossed_down:
                # линейная интерполяция момента пересечения
                alpha = -prev_val / (cur_val - prev_val) \
                    if abs(cur_val - prev_val) > 1e-30 else 0.5
                alpha = min(max(alpha, 0.0), 1.0)
                y_cross = [y[k] + alpha * (y_new[k] - y[k])
                           for k in range(len(y))]
                section = tuple(
                    y_cross[k] for k in range(len(y_cross))
                    if k != self.axis and k != self.axis + 0)
                self.points.append(PoincarePoint(
                    t=t + alpha * self.dt, coords=section))
                if len(self.points) >= max_points:
                    break
            y = y_new
            t = t_new
            prev_val = cur_val
        return self.points

    def to_rows(self, n_axes: int = 2) -> list[tuple[float, ...]]:
        return [p.coords for p in self.points]


# ═══════════════════════════════════════════════════════════════════════════
# FLI — быстрый ляпуновский индикатор
# ═══════════════════════════════════════════════════════════════════════════
def fli(deriv: Deriv, y0: Sequence[float], t0: float, dt: float,
        n_steps: int = 1000, delta0: float = 1e-8,
        renorm_every: int = 10) -> dict:
    """Fast Lyapunov Indicator: log‖Δ(t)‖ при фиксированных перенормировках.

    Регулярная орбита — линейный рост/насыщение; хаотическая —
    экспоненциальный до насыщения. Возвращает FLI(t_end) и историю.
    """
    n = len(y0)
    y = list(y0)
    y_p = [y0[i] + (delta0 if i == 0 else 0.0) for i in range(n)]
    t = t0
    log_sum = 0.0
    dist = delta0
    history: list[float] = []

    def rk4(yv, tv):
        k1 = deriv(yv, tv)
        y2 = [yv[i] + 0.5 * dt * k1[i] for i in range(n)]
        k2 = deriv(y2, tv + 0.5 * dt)
        y3 = [yv[i] + 0.5 * dt * k2[i] for i in range(n)]
        k3 = deriv(y3, tv + 0.5 * dt)
        y4 = [yv[i] + dt * k3[i] for i in range(n)]
        k4 = deriv(y4, tv + dt)
        return [yv[i] + dt / 6.0 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
                for i in range(n)]

    for i in range(n_steps):
        y = rk4(y, t)
        y_p = rk4(y_p, t)
        t += dt
        d = math.sqrt(sum((a - b) ** 2 for a, b in zip(y, y_p)))
        if i % renorm_every == renorm_every - 1 or i == n_steps - 1:
            if d > 0:
                log_sum += math.log(d / max(dist, 1e-300))
                history.append(d)
                # перенормировка возмущения к базовой дистанции
                k = delta0 / d
                y_p = [a + (b - a) * k for a, b in zip(y, y_p)]
                dist = delta0
        if d > 1e10 or d != d:      # насыщение/NaN — стоп
            break
    fli_value = log_sum + math.log(max(dist, 1e-300) / delta0)
    return dict(
        fli=fli_value,
        history=history[-30:],
        t_end=t,
        saturated=(len(history) * renorm_every < n_steps),
    )


def fli_classify(fli_value: float, dt: float, n_steps: int) -> str:
    """Грубая классификация по величине FLI относительно времени."""
    span = dt * n_steps
    if fli_value > 8.0:
        return "хаотическая (экспоненциальное расхождение)"
    if fli_value > 2.0:
        return "слабо хаотическая / резонансная"
    return "регулярная (квазипериодическая)"


# ═══════════════════════════════════════════════════════════════════════════
# Частотный анализ Ласкара (скользящее окно)
# ═══════════════════════════════════════════════════════════════════════════
def sliding_frequency(times: Sequence[float],
                      signal: Sequence[float],
                      window: int = 128,
                      n_windows: int = 8) -> list[dict]:
    """Основная частота в каждом окне (максимум |DFT| без нулевой).

    Дрейф частоты между окнами — маркер диффузии (Ласкар 1990).
    """
    n = len(signal)
    if n < window * 2:
        return []
    results = []
    stride = max((n - window) // max(n_windows - 1, 1), 1)
    for w in range(n_windows):
        start = w * stride
        if start + window > n:
            break
        seg = signal[start:start + window]
        t_seg = times[start:start + window]
        dt = (t_seg[-1] - t_seg[0]) / max(window - 1, 1)
        mean_v = sum(seg) / window
        centered = [v - mean_v for v in seg]
        best_freq = 0.0
        best_power = -1.0
        for k in range(1, window // 2):
            re = sum(centered[i] * math.cos(2 * math.pi * k * i / window)
                     for i in range(window))
            im = sum(centered[i] * math.sin(2 * math.pi * k * i / window)
                     for i in range(window))
            power = re * re + im * im
            if power > best_power:
                best_power = power
                best_freq = k / (window * dt)
        results.append(dict(t_center=t_seg[window // 2],
                            freq=best_freq,
                            power=best_power / (window * window)))
    return results


def frequency_drift(times: Sequence[float], signal: Sequence[float],
                     window: int = 128, n_windows: int = 8) -> dict:
    """Относительный дрейф основной частоты по окнам."""
    rows = sliding_frequency(times, signal, window, n_windows)
    if len(rows) < 2:
        return dict(error="мало данных", drift=float("nan"))
    freqs = [r["freq"] for r in rows if r["freq"] > 0]
    if len(freqs) < 2:
        return dict(drift=0.0, n_windows=len(rows), stable=True)
    f0 = freqs[0]
    drift = max(abs(f - f0) / max(f0, 1e-12) for f in freqs)
    return dict(
        drift=drift,
        freqs=freqs,
        n_windows=len(rows),
        stable=drift < 0.05,
        note="дрейф >5% — диффузия частоты (Ласкар); стабильность — "
             "квазипериодичность",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Эталонные системы для самопроверки
# ═══════════════════════════════════════════════════════════════════════════
def henon_heiles_deriv(y: Sequence[float], _t: float) -> list[float]:
    """Система Хеньона-Хейлеса (1964): классический эталон хаоса.

    H = ½(px² + py²) + ½(x² + y²) + x²y − y³/3.
    """
    x, yy, px, py = y
    return [px, py,
            -x - 2.0 * x * yy,
            -yy - x * x + yy * yy]


def harmonic_deriv(y: Sequence[float], _t: float) -> list[float]:
    """Регулярный осциллятор (контроль)."""
    return [y[1], -y[0]]


def self_check() -> dict:
    """Хеньон-Хейлес: хаотические НУ против регулярной коробки.

    Хаотические НУ (E≈0.149) и (E=0.16, за пределами барьера —
    ограниченная область) найдены эмпирическим сканом роста возмущения;
    регулярная коробка: (0.1, 0, 0, 0.05) при E≈1/12.
    """
    # регулярная орбита ХХ (E=1/12, коробка)
    fli_reg = fli(henon_heiles_deriv,
                  [0.1, 0.0, 0.0, 0.05], 0.0, 0.02, n_steps=2000)
    # хаотическая (E≈0.149): сильный рост возмущения (×28 за t=30)
    fli_chaos = fli(henon_heiles_deriv,
                    [0.1, 0.2, 0.4, 0.3], 0.0, 0.02, n_steps=2000)
    # контроль: осциллятор (полностью регулярный)
    fli_osc = fli(harmonic_deriv, [1.0, 0.0], 0.0, 0.02, n_steps=2000)
    ordering_ok = fli_chaos["fli"] > fli_reg["fli"] >= fli_osc["fli"] - 1.0
    return dict(
        fli_hh_regular=fli_reg["fli"],
        fli_hh_chaotic=fli_chaos["fli"],
        fli_oscillator=fli_osc["fli"],
        ordering_ok=ordering_ok,
        classify_chaos=fli_classify(fli_chaos["fli"], 0.02, 2000),
        classify_regular=fli_classify(fli_reg["fli"], 0.02, 2000),
        all_ok=ordering_ok,
    )
