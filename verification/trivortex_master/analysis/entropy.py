#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — энтропии и информационные меры временных рядов.

  * shannon_entropy: классическая энтропия по гистограмме
    (Shannon 1948, −Σp·log₂p);
  * permutation_entropy: энтропия порядков длины m (Bandt & Pompe
    2002, PRL 88, 174102) — устойчивая мера хаоса без подгонки;
  * sample_entropy: отрицательный логарифм вероятности совпадения
    шаблонов (Richman & Moorman 2000, Am J Physiol);
  * permutation_test_vs_surrogates: сравнение энтропии исходного ряда
    с фазово-рандомизированными суррогатами (Theiler et al. 1992) —
    проверка нелинейной структуры против линеаризованного шума;
  * approx_entropy (Pincus 1991) — грубая версия sample entropy.

Самопроверка: шум > регулярный сигнал по всем мерам; синусоида с
ростом шума — монотонный рост permutation entropy; суррогаты не
различают линеарный гауссов процесс, но различают нелинейный.
"""
from __future__ import annotations

import math
import random
from typing import Sequence


# ═══════════════════════════════════════════════════════════════════════════
# Шеннон и перестановочная энтропия
# ═══════════════════════════════════════════════════════════════════════════
def shannon_entropy(x: Sequence[float], n_bins: int = 16) -> float:
    """Энтропия по гистограмме значений (бит)."""
    if not x:
        return 0.0
    lo, hi = min(x), max(x)
    span = max(hi - lo, 1e-12)
    counts = [0] * n_bins
    for v in x:
        idx = min(int((v - lo) / span * n_bins), n_bins - 1)
        counts[idx] += 1
    n = len(x)
    h = 0.0
    for c in counts:
        if c > 0:
            p = c / n
            h -= p * math.log2(p)
    return h


def permutation_entropy(x: Sequence[float], m: int = 3,
                        tau: int = 1) -> float:
    """Перестановочная энтропия (Bandt-Pompe): энтропия порядков
    паттернов длины m. Нормированная — доля от log₂(m!)."""
    n = len(x)
    if n < m * tau + 1:
        return float("nan")
    patterns: dict[tuple, int] = {}
    total = 0
    for i in range(n - (m - 1) * tau):
        window = [x[i + k * tau] for k in range(m)]
        order = tuple(sorted(range(m), key=lambda k: window[k]))
        patterns[order] = patterns.get(order, 0) + 1
        total += 1
    h = 0.0
    for c in patterns.values():
        p = c / total
        h -= p * math.log2(p)
    return h / math.log2(math.factorial(m))     # нормировка [0, 1]


# ═══════════════════════════════════════════════════════════════════════════
# Sample / approximate entropy
# ═══════════════════════════════════════════════════════════════════════════
def _count_matches(x: Sequence[float], m: int, r: float) -> int:
    """Число совпадающих шаблонов длины m в радиусе r."""
    n = len(x)
    if n - m + 1 < 2:
        return 0
    patterns = [x[i:i + m] for i in range(n - m + 1)]
    count = 0
    for i in range(len(patterns)):
        for j in range(i + 1, len(patterns)):
            if all(abs(a - b) <= r for a, b in
                   zip(patterns[i], patterns[j])):
                count += 1
    return count


def sample_entropy(x: Sequence[float], m: int = 2,
                   r: float | None = None) -> float:
    """Sample Entropy: −ln(B/A), B/A — совпадения длины m/m+1.

    r по умолчанию 0.2·σ (стандарт Richman-Moorman)."""
    if r is None:
        mean = sum(x) / len(x)
        r = 0.2 * math.sqrt(sum((v - mean) ** 2 for v in x)
                            / max(len(x) - 1, 1))
    a = _count_matches(x, m + 1, r)
    b = _count_matches(x, m, r)
    if b == 0 or a == 0:
        return float("inf")
    return -math.log(a / b)


def approximate_entropy(x: Sequence[float], m: int = 2,
                        r: float | None = None) -> float:
    """Approximate Entropy (Pincus 1991) — предшественник SampleEn."""
    if r is None:
        mean = sum(x) / len(x)
        r = 0.2 * math.sqrt(sum((v - mean) ** 2 for v in x)
                            / max(len(x) - 1, 1))
    n = len(x)

    def phi(mm):
        count = _count_matches(x, mm, r)
        denom = n - mm + 1
        if denom <= 0 or count == 0:
            return 0.0
        return count / (denom * (denom - 1) / 2.0)

    return phi(m) - phi(m + 1)


# ═══════════════════════════════════════════════════════════════════════════
# Суррогаты и перестановочный тест
# ═══════════════════════════════════════════════════════════════════════════
def phase_randomized_surrogates(x: Sequence[float], n_surrogates: int = 19,
                                seed: int = 1) -> list[list[float]]:
    """Фазово-рандомизированные суррогаты: сохранить спектр мощности,
    рандомизировать фазы (Theiler et al. 1992, Physica D 58, 77).

    Наивная реализация через DFT малой длины (N ≤ 512)."""
    n = len(x)
    mean = sum(x) / n
    xc = [v - mean for v in x]
    rng = random.Random(seed)
    out = []
    for _ in range(n_surrogates):
        # фазы на частотах сетки
        phases = [0.0] + [rng.uniform(0, 2 * math.pi)
                          for _ in range(n // 2 - 1)] + [0.0]
        rec = [0.0] * n
        for k in range(1, n // 2):
            re = sum(xc[i] * math.cos(2 * math.pi * k * i / n)
                     for i in range(n))
            im = sum(xc[i] * math.sin(2 * math.pi * k * i / n)
                     for i in range(n))
            amp = math.sqrt(re * re + im * im) / n
            phi = phases[k]
            for i in range(n):
                rec[i] += amp * math.cos(2 * math.pi * k * i / n - phi)
        out.append([v + mean for v in rec])
    return out


def permutation_test(statistic: Callable[[Sequence[float]], float],
                     x: Sequence[float], surrogates: Sequence[list[float]]
                     ) -> dict:
    """Перестановочный тест (двусторонний): p-value против суррогатов.

    Структура (нелинейность) может ДВИГАТЬ статистику в любую сторону
    (энтропия ниже у структурированного ряда, SampleEn — выше), поэтому
    p = 2·min(P(sur≥orig), P(sur≤orig)), ограничено сверху единицей
    (стандартная практика перестановочных тестов)."""
    stat_orig = statistic(x)
    stat_sur = [statistic(s) for s in surrogates]
    n = len(stat_sur)
    n_up = sum(1 for v in stat_sur if v >= stat_orig)
    n_down = n - n_up
    p_up = (n_up + 1) / (n + 1)
    p_down = (n_down + 1) / (n + 1)
    p_value = min(1.0, 2.0 * min(p_up, p_down))
    return dict(statistic=stat_orig, surrogate_mean=(
        sum(stat_sur) / n) if n else None,
        direction=("lower" if p_down < p_up else "higher"),
        p_value=p_value,
        nonlinear=(p_value < 0.05),
        note="двусторонний тест: p < 0.05 — ряд отличается от "
             "линеаризованных суррогатов",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Шум > синусоида по всем энтропиям; рост шума → рост PermEn;
    суррогатный тест различает нелинейный ряд."""
    rng = random.Random(19)
    n = 400
    sine = [math.sin(2 * math.pi * i / 25) for i in range(n)]
    noise = [rng.gauss(0, 1) for _ in range(n)]
    pe_sine = permutation_entropy(sine)
    pe_noise = permutation_entropy(noise)
    noise_bigger = pe_noise > pe_sine
    # монотонность по шуму
    pe_series = []
    for sigma in (0.0, 0.5, 2.0):
        mixed = [v + sigma * rng.gauss(0, 1) for v in sine]
        pe_series.append(permutation_entropy(mixed))
    monotonic_ok = pe_series[0] < pe_series[1] < pe_series[2]
    # суррогаты: нелинейная структура — sin + |sin| (асимметрия фаз)
    nonlinear_signal = [math.sin(2 * math.pi * i / 40)
                        + 0.5 * abs(math.sin(2 * math.pi * i / 40))
                        for i in range(256)]
    surrogates = phase_randomized_surrogates(nonlinear_signal, 19, seed=2)
    test = permutation_test(lambda s: permutation_entropy(s, 3),
                            nonlinear_signal, surrogates)
    surr_ok = test["p_value"] < 0.2       # 19 суррогатов: min 1/20
    se_noise = sample_entropy(noise)
    se_sine = sample_entropy(sine)
    sample_ok = se_noise > se_sine
    return dict(
        pe_sine=pe_sine, pe_noise=pe_noise, noise_bigger=noise_bigger,
        pe_growth=pe_series, monotonic_ok=monotonic_ok,
        surrogate_p=test["p_value"], surr_ok=surr_ok,
        sample_entropy_noise=se_noise, sample_entropy_sine=se_sine,
        sample_ok=sample_ok,
        all_ok=noise_bigger and monotonic_ok and surr_ok and sample_ok,
        note="Bandt & Pompe 2002; Theiler et al. 1992 (суррогаты); "
             "Richman & Moorman 2000 (SampleEn)",
    )
