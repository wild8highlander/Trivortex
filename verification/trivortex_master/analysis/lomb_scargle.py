#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — периодограмма Ломба-Скаргла на чистом stdlib.

Классический метод поиска периодов в неравномерных рядах:

  * lomb_scargle(t, y, dy, f_grid): нормированная LS-статистика
    (Lomb 1976, ApSS 39, 447; Scargle 1982, ApJ 263, 835) с
    ортогональной подгонкой фазы τ;
  * автоматическая сетка частот: от 1/T (oversample×) до Найквиста;
  * false alarm probability: FAP_single = e^{−z} (экспоненциальное
    распределение мощности белого шума), глобальная ≈ M·e^{−z}
    (M — эффективное число независимых частот);
  * phase_fold: складывание ряда по периоду (для кривой блеска);
  * alias_report: боковые пики ±1/T_day и их отличие от истинного.

Самопроверка: синусоида 7.4 сут с пропусками и шумом восстанавливается
с ошибкой < 0.5%; шумовой ряд — FAP > 5% (ложных открытий нет).
"""

from __future__ import annotations

import math
from typing import Sequence


# ═══════════════════════════════════════════════════════════════════════════
# Статистика Ломба-Скаргла
# ═══════════════════════════════════════════════════════════════════════════
def _tau_offset(omega: float, t: Sequence[float], w: Sequence[float]) -> float:
    """Сдвиг фазы τ = atan2(ΣW sin2ωt, ΣW cos2ωt)/(2ω) — LS-вариант."""
    num = sum(wi * math.sin(2 * omega * ti) for wi, ti in zip(w, t))
    den = sum(wi * math.cos(2 * omega * ti) for wi, ti in zip(w, t))
    if abs(den) < 1e-300 and abs(num) < 1e-300:
        return 0.0
    return math.atan2(num, den) / (2.0 * omega)


def lomb_scargle_at(
    t: Sequence[float], y: Sequence[float], dy: Sequence[float], omega: float
) -> float:
    """Мощность LS на одной частоте (Press et al., Numerical Recipes §13.8).

    Веса W = 1/dy² (dy — истинные погрешности точек). Нормировка /2:
    для белого шума E[num²/den] = 1 при каждом члене → мощность
    распределена экспоненциально со средним 1 (Scargle 1982).
    """
    weights = [1.0 / (d * d) for d in dy]
    y_mean = sum(wi * yi for wi, yi in zip(weights, y)) / sum(weights)
    yc = [yi - y_mean for yi in y]
    tau = _tau_offset(omega, t, weights)
    ct = [math.cos(omega * (ti - tau)) for ti in t]
    st = [math.sin(omega * (ti - tau)) for ti in t]
    num_c = sum(wi * yi * ci for wi, yi, ci in zip(weights, yc, ct))
    num_s = sum(wi * yi * si for wi, yi, si in zip(weights, yc, st))
    den_c = sum(wi * ci * ci for wi, ci in zip(weights, ct))
    den_s = sum(wi * si * si for wi, si in zip(weights, st))
    if den_c < 1e-300 or den_s < 1e-300:
        return 0.0
    return (num_c * num_c / den_c + num_s * num_s / den_s) / 2.0


def frequency_grid(
    t: Sequence[float], oversample: float = 5.0, f_max: float | None = None
) -> list[float]:
    """Сетка частот: [oversample/T, f_max] с шагом 1/(oversample·T)."""
    t_span = max(t) - min(t)
    f_min = oversample / t_span
    if f_max is None:
        # Найквист по среднему шагу
        dt_mean = t_span / max(len(t) - 1, 1)
        f_max = 0.5 / dt_mean
    n = max(int((f_max - f_min) / (1.0 / (oversample * t_span))), 2)
    return [f_min + (f_max - f_min) * i / n for i in range(n + 1)]


def lomb_scargle(
    t: Sequence[float],
    y: Sequence[float],
    dy: Sequence[float],
    oversample: float = 5.0,
    f_max: float | None = None,
) -> dict:
    """Полный LS-периодограмм: сетка, мощности, пик, FAP."""
    if len(t) != len(y) or len(t) != len(dy):
        raise ValueError("t, y, dy должны быть одной длины")
    freqs = frequency_grid(t, oversample, f_max)
    powers = [lomb_scargle_at(t, y, dy, 2 * math.pi * f) for f in freqs]
    z_max = max(powers)
    f_max_idx = powers.index(z_max)
    # глобальная FAP: 1 − (1 − e^{−z})^M ≈ M·e^{−z}; порог детекции
    # по экстремальным значениям: z_max > ln(M_eff) (максимум M
    # экспоненциальных величин ~ ln M)
    m_eff = len(freqs)
    fap = min(1.0, m_eff * math.exp(-z_max))
    threshold = math.log(m_eff)
    return dict(
        freqs=freqs,
        powers=powers,
        best_freq=freqs[f_max_idx],
        best_period=1.0 / freqs[f_max_idx],
        peak_power=z_max,
        false_alarm_prob=fap,
        threshold=threshold,
        n_eff_freqs=m_eff,
        detected=(z_max > threshold and fap < 0.05),
    )


# ═══════════════════════════════════════════════════════════════════════════
# Фазовая свёртка и алиасы
# ═══════════════════════════════════════════════════════════════════════════
def phase_fold(
    t: Sequence[float], y: Sequence[float], period: float, t0: float = 0.0, n_bins: int = 20
) -> list[dict]:
    """Сложить ряд по периоду; вернуть среднее y по фазовым бинам."""
    phases = [((ti - t0) / period) % 1.0 for ti in t]
    bins = [[] for _ in range(n_bins)]
    for ph, yi in zip(phases, y):
        idx = min(int(ph * n_bins), n_bins - 1)
        bins[idx].append(yi)
    out = []
    for i, vals in enumerate(bins):
        if vals:
            out.append(dict(phase=(i + 0.5) / n_bins, mean=sum(vals) / len(vals), n=len(vals)))
    return out


def alias_report(t: Sequence[float], ls: dict, base_unit: float = 1.0) -> list[dict]:
    """Сильнейшие боковые пики: кандидаты в алиасы (f ± k·f_window).

    Окно наблюдений 1/T_span; алиасы на f ± 1/base_unit (сутки →
    типичный наземный алиас).
    """
    span = max(t) - min(t)
    f_win = 1.0 / span
    out = []
    # топ-пики вне главного
    pairs = sorted(zip(ls["freqs"], ls["powers"]), key=lambda fp: -fp[1])
    f_best = ls["best_freq"]
    for f, p in pairs[1:]:
        near_alias = abs(abs(f - f_best) - f_win) < 0.1 * f_win
        near_daily = any(abs(abs(f - f_best) - k / base_unit) < 0.02 for k in (1, 2))
        if near_alias or near_daily:
            out.append(dict(freq=f, power=p, kind="alias-candidate"))
        if len(out) >= 3:
            break
    return out


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Синусоида с пропусками: период восстановлен; шум не детектируется."""
    import random

    rng = random.Random(12)
    # ряд с пропусками: 120 точек на 100 сут, 7.4-суточный сигнал
    t = sorted(rng.uniform(0, 100) for _ in range(120))
    period_true = 7.4
    amp = 1.0
    noise = 0.25
    y = [amp * math.sin(2 * math.pi * ti / period_true) + rng.gauss(0, noise) for ti in t]
    dy = [noise] * len(t)
    ls = lomb_scargle(t, y, dy)
    err = abs(ls["best_period"] - period_true) / period_true
    # шумовой ряд
    y_noise = [rng.gauss(0, noise) for _ in t]
    ls_noise = lomb_scargle(t, y_noise, dy)
    # фазовая свёртка по истинному периоду: амплитуда сохранена
    folded = phase_fold(t, y, period_true)
    fold_amp = max(f["mean"] for f in folded) - min(f["mean"] for f in folded)
    return dict(
        period_est=ls["best_period"],
        period_err=err,
        peak_power=ls["peak_power"],
        fap=ls["false_alarm_prob"],
        detected=ls["detected"],
        noise_power=ls_noise["peak_power"],
        noise_fap=ls_noise["false_alarm_prob"],
        fold_amplitude=fold_amp,
        ok=(
            err < 0.005
            and ls["detected"]
            and ls_noise["false_alarm_prob"] > 0.05
            and fold_amp > 0.8
        ),
    )
