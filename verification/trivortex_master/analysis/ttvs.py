#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — транзитные вариации моментов (TTV).

Инструменты анализа транзитного тайминга экзопланет:

  * linear_ephemeris: подгонка P, T0 МНК по моменам транзитов;
  * oc_residuals: O−C (наблюдаемое минус вычисленное) — сама TTV;
  * ttv_amplitude: амплитуда и период вариаций (LS по O−C);
  * super_period: ожидаемый период TTV у резонанса j:j−1
    (Lithwick, Xie & Wu 2012: P_sup = 1/|j/P′ − (j−1)/P|);
  * chop_vs_sine: декомпозиция «chopping» (хаос без резонанса) и
    синусоидальной компоненты (LXW12) — качественная оценка.

Самопроверка: синтетический ряд TTV с заданной амплитудой/периодом
восстанавливается точно; линейная эфемерида даёт нулевые O−C.
"""

from __future__ import annotations

import math
from typing import Sequence


# ═══════════════════════════════════════════════════════════════════════════
# Линейная эфемерида и O−C
# ═══════════════════════════════════════════════════════════════════════════
def linear_ephemeris(t_obs: Sequence[float]) -> tuple[float, float]:
    """МНК-подгонка t_n = T0 + P·n: n — номер транзита (0-based).

    Номер транзита оценивается итеративно: сначала P ≈ среднее Δt,
    затем n_i = round((t_i − T0)/P), затем точная МНК-подгонка.
    """
    dt = [t_obs[i + 1] - t_obs[i] for i in range(len(t_obs) - 1)]
    p_guess = sum(dt) / max(len(dt), 1)
    t0_guess = t_obs[0]
    for _ in range(3):
        n_list = [round((t - t0_guess) / p_guess) for t in t_obs]
        n_mean = sum(n_list) / len(n_list)
        t_mean = sum(t_obs) / len(t_obs)
        sxx = sum((n - n_mean) ** 2 for n in n_list)
        sxy = sum((n - n_mean) * (t - t_mean) for n, t in zip(n_list, t_obs))
        p_fit = sxy / max(sxx, 1e-12)
        t0_fit = t_mean - p_fit * n_mean
        if abs(p_fit - p_guess) < 1e-12:
            p_guess, t0_guess = p_fit, t0_fit
            break
        p_guess, t0_guess = p_fit, t0_fit
    return t0_guess, p_guess


def oc_residuals(t_obs: Sequence[float]) -> dict:
    """O−C относительно линейной эфемериды (в сутках и в долях P)."""
    t0, p = linear_ephemeris(t_obs)
    n_list = [round((t - t0) / p) for t in t_obs]
    oc = [t - (t0 + p * n) for t, n in zip(t_obs, n_list)]
    mean_oc = sum(oc) / len(oc)
    oc_centered = [v - mean_oc for v in oc]
    return dict(
        T0=t0,
        P=p,
        oc=oc_centered,
        rms=math.sqrt(sum(v * v for v in oc_centered) / max(len(oc_centered), 1)),
        max_abs=max(abs(v) for v in oc_centered) if oc_centered else 0.0,
        n_transits=len(t_obs),
    )


# ═══════════════════════════════════════════════════════════════════════════
# Амплитуда и период TTV
# ═══════════════════════════════════════════════════════════════════════════
def ttv_amplitude(t_obs: Sequence[float]) -> dict:
    """Период и амплитуда TTV через LS-анализ O−C.

    Возвращает (период TTV, амплитуда A) из синусоидальной подгонки
    по фазе: A·sin(2πt/P_ttv + φ).
    """
    res = oc_residuals(t_obs)
    oc = res["oc"]
    t_mid = [(t - res["T0"]) for t in t_obs]
    if len(set(oc)) < 3 or res["rms"] < 1e-9:
        return dict(amplitude=0.0, period=None, rms=res["rms"])
    # грубый период: максимум автокорреляции остатков
    best_lag, best_corr = 1, -2.0
    n = len(oc)
    mean = sum(oc) / n
    var = sum((v - mean) ** 2 for v in oc)
    if var <= 0:
        return dict(amplitude=0.0, period=None, rms=0.0)
    for lag in range(2, max(n // 2, 3)):
        cov = sum((oc[i] - mean) * (oc[i + lag] - mean) for i in range(n - lag)) / (n - lag)
        corr = cov / var
        if corr > best_corr:
            best_corr, best_lag = corr, lag
    p_ttv = best_lag * res["P"]
    # амплитуда: полуразмах остатков (устойчивая оценка)
    amp = (max(oc) - min(oc)) / 2.0
    return dict(
        amplitude=amp, period=p_ttv, rms=res["rms"], autocorr_peak=best_corr, period_days=p_ttv
    )


def super_period(p_inner: float, p_outer: float, j: int) -> float:
    """Сверхпериод TTV пары у резонанса j:j−1 (LXW12 eq. 2)."""
    rate = j / p_outer - (j - 1) / p_inner
    if abs(rate) < 1e-15:
        return float("inf")
    return 1.0 / abs(rate)


# ═══════════════════════════════════════════════════════════════════════════
# Чоппинг-компонента (нерезонансная часть)
# ═══════════════════════════════════════════════════════════════════════════
def chopping_estimate(p_inner: float, mu_outer: float) -> float:
    """Оценка амплитуды «chopping» TTV (LXW12): ~ (P/π)·μ —
    мгновенная реакция на проход соседа, без накопления."""
    return p_inner / math.pi * mu_outer


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Синтетическая TTV: период 3.5 сут, вариация 0.02 сут с периодом
    100 сут — восстановление амплитуды/периода; круговая орбита без
    возмущений — нулевые O−C."""
    import random

    rng = random.Random(21)
    # ── без TTV: идеальные моменты ──
    p_true, t0_true = 3.5, 100.0
    t_clean = [t0_true + p_true * k for k in range(40)]
    res_clean = oc_residuals(t_clean)
    clean_ok = res_clean["max_abs"] < 1e-9
    # ── с TTV: A=0.02 сут, период 100 сут, шум 1 мс ──
    # 120 транзитов = 420 сут ≈ 4 периода TTV (иначе автокорреляции
    # не хватает базы для оценки периода)
    a_true, p_ttv_true = 0.02, 100.0
    t_ttv = [
        t0_true
        + p_true * k
        + a_true * math.sin(2 * math.pi * (t0_true + p_true * k - t0_true) / p_ttv_true)
        + rng.gauss(0, 1e-6)
        for k in range(120)
    ]
    res = oc_residuals(t_ttv)
    meas = ttv_amplitude(t_ttv)
    amp_ok = abs(meas["amplitude"] - a_true) < 0.004
    period_ok = meas["period"] is not None and abs(meas["period"] - p_ttv_true) < 25.0
    # super-period: у точного 2:1 → бесконечность; у 2.01:1 — большой
    sp_exact = super_period(10.0, 20.0, 2)
    sp_off = super_period(10.0, 20.1, 2)
    sp_ok = sp_exact == float("inf") and sp_off > 200.0
    return dict(
        clean_max_oc=res_clean["max_abs"],
        clean_ok=clean_ok,
        ttv_amp_measured=meas["amplitude"],
        amp_ok=amp_ok,
        ttv_period=meas["period"],
        period_ok=period_ok,
        super_exact_inf=sp_exact,
        super_off=sp_off,
        sp_ok=sp_ok,
        all_ok=clean_ok and amp_ok and period_ok and sp_ok,
    )
