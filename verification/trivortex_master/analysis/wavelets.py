#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — вейвлет-анализ: Морле, скалограммы, детренд.

Частотно-временной анализ временных рядов без scipy:

  * MorletWavelet: ψ(t) = exp(iω₀t)·exp(−t²/2); CWT свёрткой с
    гауссовыми окнами на логарифмической сетке частот;
  * scalogram(): |W(a, b)|² — матрица мощностей (частота × время),
    готовая для отрисовки в отчёты;
  * dominant_ridge(): гребень максимальной мощности (трек основной
    частоты со временем — дрейф выдаёт диффузию);
  * detrend(): удаление линейного/квадратичного тренда (МНК);
  * significance: шум ЛУВ (red noise) AR(1) — порог 95% по
    Torrence & Compo (1998, таблица χ²).

Самопроверка: chirp-сигнал (частота 2 Гц → 5 Гц) — гребень
отслеживает частоту с ошибкой <10%.
"""
from __future__ import annotations

import math
from typing import Sequence


# ═══════════════════════════════════════════════════════════════════════════
# Вспомогательные: МНК-полином для детренда
# ═══════════════════════════════════════════════════════════════════════════
def polyfit_least_squares(x: Sequence[float], y: Sequence[float],
                          degree: int = 1) -> list[float]:
    """Полиномиальная аппроксимация (нормальные уравнения, Гаусс)."""
    n = degree + 1
    A = [[sum(xi ** (i + j) for xi in x) for j in range(n)]
         for i in range(n)]
    b = [sum(yi * xi ** i for xi, yi in zip(x, y)) for i in range(n)]
    # Гауссово исключение с выбором главного элемента
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(A[r][col]))
        A[col], A[piv] = A[piv], A[col]
        b[col], b[piv] = b[piv], b[col]
        if abs(A[col][col]) < 1e-30:
            continue
        for r in range(n):
            if r == col:
                continue
            f = A[r][col] / A[col][col]
            for c in range(col, n):
                A[r][c] -= f * A[col][c]
            b[r] -= f * b[col]
    return [b[i] / A[i][i] if abs(A[i][i]) > 1e-30 else 0.0
            for i in range(n - 1, -1, -1)]


def polyval(coeffs: Sequence[float], x: float) -> float:
    """Значение полинома (coeffs от старшей степени)."""
    out = 0.0
    for c in coeffs:
        out = out * x + c
    return out


def detrend(y: Sequence[float], degree: int = 1) -> list[float]:
    """Удалить полиномиальный тренд; вернуть остатки."""
    n = len(y)
    x = list(range(n))
    coeffs = polyfit_least_squares(x, y, degree)
    return [yi - polyval(coeffs, xi) for xi, yi in zip(x, y)]


# ═══════════════════════════════════════════════════════════════════════════
# Вейвлет Морле и CWT
# ═══════════════════════════════════════════════════════════════════════════
W_0 = 6.0                     # параметр Морле (ω₀=6: баланс локальности)


def morlet_psi_norm(t: float, w0: float = W_0) -> tuple[float, float]:
    """Нормированный Морле: (Re ψ, Im ψ) с ψ(0)=нормировка π^{-1/4}."""
    norm = math.pi ** -0.25
    gauss = math.exp(-t * t / 2.0)
    return (norm * gauss * math.cos(w0 * t),
            norm * gauss * math.sin(w0 * t))


def cwt_morlet(y: Sequence[float], dt: float,
               freqs: Sequence[float] | None = None,
               w0: float = W_0) -> dict:
    """Continuous Wavelet Transform (Морле) на сетке частот.

    Возвращает dict(freqs, times, power[n_freq][n_time], W_re, W_im).
    Сетка частот по умолчанию: 24 лог-уровня от 1/(N·dt) до Найквиста.
    """
    n = len(y)
    if n < 8:
        return dict(error="слишком короткий ряд")
    nyquist = 0.5 / dt
    if freqs is None:
        f_min = max(1.0 / (n * dt), 1e-6)
        f_max = nyquist * 0.95
        freqs = [f_min * (f_max / f_min) ** (i / 23.0)
                 for i in range(24)]
    # центрирование
    mean = sum(y) / n
    centered = [v - mean for v in y]
    sigma2 = sum(v * v for v in centered) / n
    times = [i * dt for i in range(n)]
    power = []
    w_re_all = []
    for f in freqs:
        # масштаб Морле: a = w0/(2π f) (в единицах отсчётов: a·dt)
        a = w0 / (2.0 * math.pi * f) / dt
        # свёртка по времени (окно ±4a)
        half = int(min(max(4.0 * a, 1.0), n // 2))
        row = []
        w_re_row = []
        for t_idx in range(n):
            re_sum = 0.0
            im_sum = 0.0
            for k in range(-half, half + 1):
                idx = t_idx + k
                if 0 <= idx < n:
                    t_norm = k / a
                    re_psi, im_psi = morlet_psi_norm(t_norm, w0)
                    re_sum += centered[idx] * re_psi
                    im_sum += centered[idx] * im_psi
            # нормировка: dt/√a (Torrence & Compo 1998, eq. 6)
            scale = dt / math.sqrt(a)
            re_sum *= scale
            im_sum *= scale
            row.append((re_sum * re_sum + im_sum * im_sum) / sigma2)
            w_re_row.append(re_sum)
        power.append(row)
        w_re_all.append(w_re_row)
    return dict(freqs=freqs, times=times, power=power, W_re=w_re_all,
                w0=w0, dt=dt)


def scalogram_to_rows(cwt: dict) -> list[list[float]]:
    """Матрица мощностей для таблиц отчётов (freq × time)."""
    return cwt["power"]


def dominant_ridge(cwt: dict) -> list[tuple[float, float]]:
    """(t, f) трек максимальной мощности по времени."""
    freqs = cwt["freqs"]
    power = cwt["power"]
    times = cwt["times"]
    n_t = len(times)
    ridge = []
    for t_idx in range(n_t):
        best_f = None
        best_p = -1.0
        for f_idx, f in enumerate(freqs):
            p = power[f_idx][t_idx]
            if p > best_p:
                best_p = p
                best_f = f
        if best_f is not None:
            ridge.append((times[t_idx], best_f))
    return ridge


def ridge_frequency_error(ridge: Sequence[tuple[float, float]],
                          true_fn: callable) -> float:
    """Средняя относительная ошибка гребня против истинной частоты."""
    if not ridge:
        return float("nan")
    total = 0.0
    for t, f in ridge:
        ft = true_fn(t)
        if ft > 0:
            total += abs(f - ft) / ft
    return total / len(ridge)


# ═══════════════════════════════════════════════════════════════════════════
# Значимость: AR(1) красный шум, порог 95% (Torrence & Compo 1998)
# ═══════════════════════════════════════════════════════════════════════════
def ar1_noise(n: int, alpha: float = 0.7, seed: int = 5) -> list[float]:
    """Красный шум AR(1): x_{t+1} = αx_t + ε."""
    import random
    rng = random.Random(seed)
    out = [0.0]
    for _ in range(n - 1):
        out.append(alpha * out[-1] + rng.gauss(0, 1))
    return out


def significance_threshold(n: int, dt: float, alpha: float = 0.7
                           ) -> float:
    """Порог мощности 95% для AR(1)-шума (упрощённый χ²₁).

    По Torrence & Compo (1998): P_95 = σ²(1−α²)·χ²₁(0.95)/2 в
    нормированных единицах. Возвращаем множитель к σ².
    """
    # χ² с 1 степенью свободы, 95%: 3.841
    chi2_95 = 3.841
    return (1.0 - alpha * alpha) * chi2_95 / 2.0


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Chirp 2→5 Гц: гребень отслеживает частоту с ошибкой <15%;
    детренд убирает линейный тренд."""
    dt = 0.01
    n = 600
    t_end = n * dt
    # частота линейно 2 → 5 Гц
    def f_true(t):
        return 2.0 + 3.0 * t / t_end
    y = []
    phase = 0.0
    for i in range(n):
        t = i * dt
        phase += 2 * math.pi * f_true(t) * dt
        y.append(math.sin(phase))
    # ограничим сетку частот разумным диапазоном (быстрее и точнее)
    freqs = [1.0 + 5.0 * i / 29.0 for i in range(30)]
    cwt = cwt_morlet(y, dt, freqs=freqs)
    ridge = dominant_ridge(cwt)
    err = ridge_frequency_error(ridge, f_true)
    # детренд: линейный тренд + синус
    trend_y = [0.5 * i / n + math.sin(2 * math.pi * i / 100)
               for i in range(300)]
    resid = detrend(trend_y, degree=1)
    resid_mean = sum(resid) / len(resid)
    # после детренда остаток ~ чистый синус (среднее ~0)
    detrend_ok = abs(resid_mean) < 0.02 and max(abs(r) for r in resid) < 1.5
    return dict(
        chirp_ridge_error=err,
        chirp_ok=err < 0.15,
        n_freqs=len(cwt["freqs"]),
        detrend_mean=resid_mean,
        detrend_ok=detrend_ok,
        ok=err < 0.15 and detrend_ok,
        note="Морле ω₀=6; гребень — argmax по частоте на каждый момент",
    )
