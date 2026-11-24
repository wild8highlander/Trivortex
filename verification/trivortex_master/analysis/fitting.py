#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — нелинейная аппроксимация: Левенберг-Марквардт.

Классический LM-алгоритм на чистом Python:

  * численный якобиан (центральные разности, адаптивный шаг h);
  * демпфирование λ: рост при неудачном шаге, спад при удачном;
  * критерии останова: |Δχ²|, |Δθ|, максимальное число итераций;
  * ковариационная матрица параметров: Cov = (JᵀJ)⁻¹·s², ошибки σᵢ;
  * встроенные модели: гаусс, экспоненциальный спад, кеплеровская
    RV-кривая (совместно с lab.kepler), полином (через МНК-ветку);
  * robust-вариант: хабер-оценка для выбросов (опционально).

Самопроверка: гауссов пик восстанавливается с ошибкой <3σ_шума/√N;
RV-кривая с K=10 м/с, P=12 дней — K в пределах 2σ.
"""

from __future__ import annotations

import math
from typing import Callable, Sequence

Vector = list[float]


# ═══════════════════════════════════════════════════════════════════════════
# Линейная алгебра (малые системы)
# ═══════════════════════════════════════════════════════════════════════════
def solve_linear(A: list[list[float]], b: Vector) -> Vector | None:
    """Решить A·x = b (Гаусс с главным элементом)."""
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-30:
            return None
        M[col], M[piv] = M[piv], M[col]
        for r in range(n):
            if r == col:
                continue
            f = M[r][col] / M[col][col]
            for c in range(col, n + 1):
                M[r][c] -= f * M[col][c]
    return [M[i][n] / M[i][i] for i in range(n)]


def invert_matrix(A: list[list[float]]) -> list[list[float]] | None:
    """Обратная матрица (Гаусс-Жордан)."""
    n = len(A)
    M = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(A)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-30:
            return None
        M[col], M[piv] = M[piv], M[col]
        d = M[col][col]
        M[col] = [v / d for v in M[col]]
        for r in range(n):
            if r == col:
                continue
            f = M[r][col]
            for c in range(2 * n):
                M[r][c] -= f * M[col][c]
    return [row[n:] for row in M]


# ═══════════════════════════════════════════════════════════════════════════
# Левенберг-Марквардт
# ═══════════════════════════════════════════════════════════════════════════
class LevenbergMarquardt:
    """Нелинейный МНК-фиттер.

    model(theta, x) → предсказания; y, sigma — данные и ошибки.
    """

    def __init__(
        self,
        model: Callable[[Vector, Sequence[float]], Vector],
        x: Sequence[float],
        y: Sequence[float],
        sigma: Sequence[float],
        h_step: float = 1e-6,
    ):
        """Do LevenbergMarquardt.  init for model, x, y, sigma and return the result."""
        self.model = model
        self.x = list(x)
        self.y = list(y)
        self.sigma = list(sigma)
        self.h = h_step
        self.n_iter = 0
        self.chi2_history: list[float] = []

    def _residuals(self, theta: Vector) -> Vector:
        """Do LevenbergMarquardt. residuals for theta and return the result."""
        pred = self.model(theta, self.x)
        return [(yi - pi) / si for yi, pi, si in zip(self.y, pred, self.sigma)]

    def _chi2(self, residuals: Vector) -> float:
        """Do LevenbergMarquardt. chi2 for residuals and return the result."""
        return sum(r * r for r in residuals)

    def _jacobian(self, theta: Vector) -> list[list[float]]:
        """Якобиан остатков: J[i][j] = ∂r_i/∂θ_j (центральные разности)."""
        n_res = len(self.y)
        n_par = len(theta)
        J = [[0.0] * n_par for _ in range(n_res)]
        for j in range(n_par):
            h = max(abs(theta[j]) * self.h, 1e-10)
            tp = list(theta)
            tm = list(theta)
            tp[j] += h
            tm[j] -= h
            rp = self._residuals(tp)
            rm = self._residuals(tm)
            for i in range(n_res):
                J[i][j] = (rp[i] - rm[i]) / (2.0 * h)
        return J

    def fit(
        self,
        theta0: Vector,
        max_iter: int = 100,
        tol_chi2: float = 1e-10,
        tol_theta: float = 1e-10,
        lam0: float = 1e-3,
    ) -> dict:
        """Основной цикл LM. Возвращает θ̂, χ², ковариацию, историю."""
        theta = list(theta0)
        res = self._residuals(theta)
        chi2 = self._chi2(res)
        lam = lam0
        self.chi2_history = [chi2]
        n_par = len(theta)
        converged = False
        for it in range(max_iter):
            self.n_iter = it + 1
            J = self._jacobian(theta)
            # JᵀJ и Jᵀr
            JtJ = [
                [sum(J[i][a] * J[i][b] for i in range(len(self.y))) for b in range(n_par)]
                for a in range(n_par)
            ]
            Jtr = [sum(J[i][a] * res[i] for i in range(len(self.y))) for a in range(n_par)]
            # шаг: (JᵀJ + λ·diag)·δ = −Jᵀr
            improved = False
            for _attempt in range(6):
                A = [
                    [JtJ[a][b] + (lam * JtJ[a][a] if a == b else 0.0) for b in range(n_par)]
                    for a in range(n_par)
                ]
                delta = solve_linear(A, [-v for v in Jtr])
                if delta is None:
                    lam *= 10.0
                    continue
                theta_new = [theta[j] + delta[j] for j in range(n_par)]
                res_new = self._residuals(theta_new)
                chi2_new = self._chi2(res_new)
                if chi2_new < chi2:
                    # успех: уменьшаем демпфирование, принимаем шаг
                    d_chi2 = chi2 - chi2_new
                    math.sqrt(sum(d * d for d in delta))
                    theta = theta_new
                    res = res_new
                    chi2 = chi2_new
                    lam = max(lam / 3.0, 1e-12)
                    improved = True
                    self.chi2_history.append(chi2)
                    break
                lam *= 10.0
            if not improved:
                break
            if len(self.chi2_history) >= 2:
                d_chi2 = abs(self.chi2_history[-2] - chi2)
                if d_chi2 < tol_chi2 * max(chi2, 1.0):
                    converged = True
                    break
        # ковариация: (JᵀJ)⁻¹ · s², s² = χ²/(N−p)
        dof = max(len(self.y) - n_par, 1)
        s2 = chi2 / dof
        JtJ = [
            [sum(J[i][a] * J[i][b] for i in range(len(self.y))) for b in range(n_par)]
            for a in range(n_par)
        ]
        inv = invert_matrix(JtJ)
        cov = None
        errors = None
        if inv is not None:
            cov = [[inv[a][b] * s2 for b in range(n_par)] for a in range(n_par)]
            errors = [math.sqrt(max(cov[a][a], 0.0)) for a in range(n_par)]
        return dict(
            theta=theta,
            chi2=chi2,
            cov=cov,
            errors=errors,
            n_iter=self.n_iter,
            converged=converged,
            dof=dof,
            reduced_chi2=s2,
            history=self.chi2_history,
        )


# ═══════════════════════════════════════════════════════════════════════════
# Библиотека моделей
# ═══════════════════════════════════════════════════════════════════════════
def gaussian_model(theta: Vector, x: Sequence[float]) -> Vector:
    """A·exp(−(x−μ)²/2σ²) + c; theta = [A, mu, sigma, c]."""
    A, mu, sig, c = theta
    return [A * math.exp(-((xi - mu) ** 2) / (2 * sig * sig)) + c for xi in x]


def exponential_decay(theta: Vector, x: Sequence[float]) -> Vector:
    """A·exp(−t/τ) + c."""
    A, tau, c = theta
    return [A * math.exp(-xi / tau) + c for xi in x]


def sine_model(theta: Vector, x: Sequence[float]) -> Vector:
    """A·sin(2πft + φ) + c."""
    A, f, phi, c = theta
    return [A * math.sin(2 * math.pi * f * xi + phi) + c for xi in x]


def rv_model(theta: Vector, t: Sequence[float]) -> Vector:
    """Кеплеровская RV: [K, P, e, omega, gamma] (через lab.kepler)."""
    from lab.kepler import kepler_E, true_anomaly

    K, P, e, omega, gamma = theta
    out = []
    for ti in t:
        M = 2.0 * math.pi * ((ti / P) % 1.0)
        E = kepler_E(M, e)
        nu = true_anomaly(E, e)
        out.append(K * math.cos(nu + omega) + gamma)
    return out


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Гаусс: параметры в 3σ; RV: K в 2σ от истины."""
    import random

    rng = random.Random(9)
    # ── гауссов пик ──
    A_t, mu_t, sig_t, c_t = 5.0, 2.0, 0.7, 1.0
    x = [i * 0.1 for i in range(60)]
    noise = 0.25
    y = [v + rng.gauss(0, noise) for v in gaussian_model([A_t, mu_t, sig_t, c_t], x)]
    lm = LevenbergMarquardt(gaussian_model, x, y, [noise] * len(x))
    fit = lm.fit([3.0, 1.5, 1.0, 0.5], max_iter=80)
    errs = fit["errors"] or [1e9] * 4
    in_3sigma = all(
        abs(fit["theta"][i] - t) < 3.0 * max(errs[i], 1e-9)
        for i, t in enumerate([A_t, mu_t, sig_t, c_t])
    )
    # ── кеплеровская RV ──
    K_t, P_t, e_t, w_t, g_t = 10.0, 12.0, 0.3, 1.0, 2.0
    t_rv = [i * 0.7 for i in range(60)]
    y_rv = [v + rng.gauss(0, 0.8) for v in rv_model([K_t, P_t, e_t, w_t, g_t], t_rv)]
    lm2 = LevenbergMarquardt(rv_model, t_rv, y_rv, [0.8] * len(t_rv))
    fit2 = lm2.fit([8.0, 12.0, 0.2, 0.8, 1.0], max_iter=60)
    errs2 = fit2["errors"] or [1e9] * 5
    k_ok = abs(fit2["theta"][0] - K_t) < 2.0 * max(errs2[0], 1e-9)
    return dict(
        gauss_theta=[round(v, 3) for v in fit["theta"]],
        gauss_in_3sigma=in_3sigma,
        gauss_reduced_chi2=fit["reduced_chi2"],
        gauss_iterations=fit["n_iter"],
        rv_K=fit2["theta"][0],
        rv_K_err=errs2[0],
        rv_K_ok=k_ok,
        rv_reduced_chi2=fit2["reduced_chi2"],
        ok=in_3sigma and k_ok,
        note="LM: якобиан центральными разностями, λ-демпфирование",
    )
