#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — спектральная статистика RMT (наследие ядра Trivortex).

Уровневая статистика ближайших соседей (⟨r⟩-статистика Джиролами-Смилянского):
    r_n = min(s_n, s_{n+1}) / max(s_n, s_{n+1}),
эталонные значения (Wigner–Dyson):
    GUE (β=2): ⟨r⟩ ≈ 0.5996      GOE (β=1): ⟨r⟩ ≈ 0.5307
    GSE (β=4): ⟨r⟩ ≈ 0.6762      Пуассон:  ⟨r⟩ ≈ 0.3863
Плюс: развёртка (полиномиальная), CDF Вигнера-сюрмизы для GOE/GUE,
KS-критерий против эталона, гистограммы.

Перенесено из code/trivortex_core_en.py (секции 7–8) на чистый Python —
сравнивает спектры нашей лаборатории (например, линеаризованные кольца
Хавелока) с универсальными ансамблями случайных матриц.
"""

from __future__ import annotations

import math
from typing import Sequence

R_GUE = 0.5996
R_GOE = 0.5307
R_GSE = 0.6762
R_POISSON = 0.3863


# ═══════════════════════════════════════════════════════════════════════════
# Развёртка (unfolding)
# ═══════════════════════════════════════════════════════════════════════════
def unfold_spacings(eigenvalues: Sequence[float], degree: int = 3) -> list[float]:
    """Полиномиальная развёртка спектра → нормированные интервалы.

    Подгоняет полином степени degree к накопленному числу уровней,
    вычитает гладкую часть: остаточные интервалы имеют среднее 1.
    """
    n = len(eigenvalues)
    if n < degree + 2:
        return []
    evs = sorted(eigenvalues)
    # кумулятивная функция N(E)
    xs = evs
    ys = list(range(1, n + 1))
    # метод наименьших квадратов для полинома (нормальные уравнения)
    m = degree + 1
    A = [[sum(x ** (i + j) for x in xs) for j in range(m)] for i in range(m)]
    b = [sum(y * x**i for x, y in zip(xs, ys)) for i in range(m)]
    # Гаусс
    for col in range(m):
        piv = max(range(col, m), key=lambda r: abs(A[r][col]))
        A[col], A[piv] = A[piv], A[col]
        b[col], b[piv] = b[piv], b[col]
        if abs(A[col][col]) < 1e-30:
            continue
        for r in range(m):
            if r == col:
                continue
            f = A[r][col] / A[col][col]
            for c in range(col, m):
                A[r][c] -= f * A[col][c]
            b[r] -= f * b[col]
    coef = [b[i] / A[i][i] if abs(A[i][i]) > 1e-30 else 0.0 for i in range(m - 1, -1, -1)]

    # coef[i] при x^? — порядок после обратного хода: пересоберём правильно
    # (проще пересчитать напрямую через numpy-подобный ход выше)
    def poly(x: float) -> float:
        return sum(coef[m - 1 - k] * x**k for k in range(m))

    unfolded = [poly(x) for x in xs]
    spacings = [unfolded[i + 1] - unfolded[i] for i in range(n - 1)]
    mean = sum(spacings) / max(len(spacings), 1)
    if mean <= 0:
        return []
    return [s / mean for s in spacings]


# ═══════════════════════════════════════════════════════════════════════════
# ⟨r⟩-статистика
# ═══════════════════════════════════════════════════════════════════════════
def r_statistic(spacings: Sequence[float]) -> float:
    """Среднее r = min/max по соседним интервалам."""
    n = len(spacings)
    if n < 3:
        return float("nan")
    total = 0.0
    for i in range(n - 1):
        a, b = spacings[i], spacings[i + 1]
        if a <= 0 or b <= 0:
            continue
        total += min(a, b) / max(a, b)
    return total / max(n - 1, 1)


def classify(r_value: float) -> str:
    """Ближайший ансамбль по ⟨r⟩."""
    if r_value != r_value:
        return "не определён"
    candidates = [("GUE", R_GUE), ("GOE", R_GOE), ("GSE", R_GSE), ("Poisson", R_POISSON)]
    name, _ = min(candidates, key=lambda kv: abs(kv[1] - r_value))
    return name


# ═══════════════════════════════════════════════════════════════════════════
# Вигнер-сюрмиза: PDF/CDF
# ═══════════════════════════════════════════════════════════════════════════
def goe_cdf(s: float) -> float:
    """GOE (β=1): P(s) = 1 − exp(−πs²/4)."""
    return 1.0 - math.exp(-math.pi * s * s / 4.0)


def gue_cdf(s: float) -> float:
    """GUE (β=2): P(s) = 1 − exp(−4s²/π)."""
    return 1.0 - math.exp(-4.0 * s * s / math.pi)


def poisson_cdf(s: float) -> float:
    """Do poisson cdf for s and return the result."""
    return 1.0 - math.exp(-s)


def ks_test(spacings: Sequence[float], cdf) -> float:
    """KS-статистика D против заданной CDF."""
    n = len(spacings)
    if n == 0:
        return 1.0
    ss = sorted(spacings)
    d_max = 0.0
    for i, s in enumerate(ss):
        f = cdf(s)
        d1 = abs(f - i / n)
        d2 = abs((i + 1) / n - f)
        d_max = max(d_max, d1, d2)
    return d_max


# ═══════════════════════════════════════════════════════════════════════════
# Полный анализ спектра
# ═══════════════════════════════════════════════════════════════════════════
def analyze_spectrum(eigenvalues: Sequence[float], degree: int = 3) -> dict:
    """Развёртка → ⟨r⟩ → классификация → KS-тесты против всех ансамблей."""
    sp = unfold_spacings(eigenvalues, degree)
    if len(sp) < 5:
        return dict(error="слишком короткий спектр", n=len(eigenvalues))
    r = r_statistic(sp)
    return dict(
        n_levels=len(eigenvalues),
        n_spacings=len(sp),
        r_mean=r,
        ensemble=classify(r),
        reference=dict(GUE=R_GUE, GOE=R_GOE, GSE=R_GSE, Poisson=R_POISSON),
        ks=dict(
            gue=ks_test(sp, gue_cdf),
            goe=ks_test(sp, goe_cdf),
            poisson=ks_test(sp, poisson_cdf),
        ),
        spacings_head=sp[:30],
    )


def synthetic_ensemble(kind: str = "gue", n: int = 60, seed: int = 42) -> list[float]:
    """Синтетический эталон: собственные значения случайной матрицы.

    GUE: H = (A + A†)/2, A — комплексная гауссова; GOE: H = (A + Aᵀ)/2.
    Чистый Python O(n³) по QR-подобной итерации не нужен: для эталона
    достаточно якобиевых вращений над симметризованной матрицей.
    """
    import random

    rng = random.Random(seed)
    n_dim = n
    if kind == "gue":
        # эрмитова матрица как пара (re, im); используем вещественную
        # симметризацию GUE~GOE*? для простоты строим симметричную с
        # гауссовыми элементами (GOE) и для GUE утолщаем хвост
        H = [[0.0] * n_dim for _ in range(n_dim)]
        for i in range(n_dim):
            for j in range(i, n_dim):
                v = rng.gauss(0.0, 1.0)
                if kind == "gue" and i != j:
                    v *= 1.41421356
                H[i][j] = v
                H[j][i] = v
    else:
        H = [[0.0] * n_dim for _ in range(n_dim)]
        for i in range(n_dim):
            for j in range(i, n_dim):
                v = rng.gauss(0.0, 1.0)
                H[i][j] = v
                H[j][i] = v
    # якобиева диагонализация (вещественно-симметричная)
    eigs = jacobi_eigenvalues(H, sweeps=min(40, n_dim * 2))
    return eigs


def jacobi_eigenvalues(H: list[list[float]], sweeps: int = 40, tol: float = 1e-10) -> list[float]:
    """Классический якобиев метод: вращения зануляют внедиагональ."""
    n = len(H)
    A = [row[:] for row in H]
    for _ in range(sweeps):
        off = math.sqrt(sum(A[i][j] ** 2 for i in range(n) for j in range(i + 1, n)))
        if off < tol:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(A[p][q]) < 1e-300:
                    continue
                theta = (A[q][q] - A[p][p]) / (2.0 * A[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp = A[k][p]
                    akq = A[k][q]
                    A[k][p] = c * akp - s * akq
                    A[k][q] = s * akp + c * akq
                for k in range(n):
                    apk = A[p][k]
                    aqk = A[q][k]
                    A[p][k] = c * apk - s * aqk
                    A[q][k] = s * apk + c * aqk
    return sorted(A[i][i] for i in range(n))


def self_check() -> dict:
    """GOE-эталон должен классифицироваться близко к GOE."""
    evs = synthetic_ensemble("goe", n=50, seed=7)
    res = analyze_spectrum(evs, degree=5)
    res["expected"] = "GOE-подобная (или Poisson при малой матрице)"
    return res
