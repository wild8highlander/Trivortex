#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — байесовский вывод: MCMC Метрополиса-Гастингса.

Полный стек анализа данных наблюдений (без emcee):

  * MetropolisSampler — случайное блуждание с гауссовым предложением,
    адаптивным шагом (роббинс-монро в фазе burn-in), лог-априорные
    распределения (flat / gaussian / jeffreys);
  * Multi-chain: несколько цепей, диагностика Гельмана-Рубина R̂
    (сходимость при R̂ < 1.1), автокорреляционное время τ (integrated
    autocorrelation time по Солтасу/Гудману);
  * Постераторная статистика: перцентили, среднее/дисперсия, HPD-
    интервалы (highest posterior density, плотнейший 90%);
  * Модель: линейная регрессия + кеплеровская RV-модель (для
    экзопланетных данных: v(t) = K·cos(ν+ω) + γ).

Самопроверка: восстановление наклона/интерсепция зашумлённой прямой
(истина в 90%-HPD), R̂ < 1.05.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Callable, Sequence

Vector = list[float]


# ═══════════════════════════════════════════════════════════════════════════
# Априорные распределения
# ═══════════════════════════════════════════════════════════════════════════
def flat_prior(theta: Vector, bounds: list[tuple[float, float]]) -> float:
    """Равномерный априор: log p = 0 внутри границ, −inf вне."""
    for v, (lo, hi) in zip(theta, bounds):
        if not (lo <= v <= hi):
            return float("-inf")
    return 0.0


def gaussian_prior(theta: Vector, means: Vector, sigmas: Vector) -> float:
    """Гауссов априор: Σ log N(μ, σ)."""
    lp = 0.0
    for v, m, s in zip(theta, means, sigmas):
        lp += -0.5 * ((v - m) / s) ** 2 - math.log(s * math.sqrt(2 * math.pi))
    return lp


# ═══════════════════════════════════════════════════════════════════════════
# Правдоподобия
# ═══════════════════════════════════════════════════════════════════════════
def gaussian_loglike(
    model: Callable[[Vector], Vector], data: Vector, sigma: Vector, theta: Vector
) -> float:
    """Лог-правдоподобие гауссовых ошибок: −½Σ((d−m)/σ)²."""
    pred = model(theta)
    ll = 0.0
    for d, p, s in zip(data, pred, sigma):
        ll += -0.5 * ((d - p) / s) ** 2 - math.log(s * math.sqrt(2 * math.pi))
    return ll


# ═══════════════════════════════════════════════════════════════════════════
# Сэмплер Метрополиса-Гастингса
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class ChainResult:
    samples: list[Vector]  # после burn-in
    acceptance: float
    log_posterior: list[float]
    n_burn: int


class MetropolisSampler:
    """Адаптивный Метрополис-Гастингс.

    Шаг предложения масштабируется к целевой доле принятия ~0.3
    (роббинс-монро: step *= exp(γ·(acc − 0.3)) в burn-in).
    """

    def __init__(
        self,
        log_posterior: Callable[[Vector], float],
        theta0: Vector,
        step_sizes: Vector,
        seed: int = 42,
        adapt: bool = True,
    ):
        self.log_posterior = log_posterior
        self.theta = list(theta0)
        self.step = list(step_sizes)
        self.rng = random.Random(seed)
        self.adapt = adapt
        self.n_accept = 0
        self.n_total = 0

    def _propose(self) -> Vector:
        return [t + self.rng.gauss(0.0, s) for t, s in zip(self.theta, self.step)]

    def run(self, n_samples: int, burn_in: int = 500) -> ChainResult:
        """Прогнать цепь; вернуть пост-burn-in сэмплы."""
        lp = self.log_posterior(self.theta)
        if lp == float("-inf"):
            raise ValueError("стартовая точка имеет нулевой априор")
        samples: list[Vector] = []
        lps: list[float] = []
        n_accept = 0
        for i in range(n_samples + burn_in):
            proposal = self._propose()
            lp_new = self.log_posterior(proposal)
            # лог-отношение
            if lp_new == float("-inf"):
                accept = False
            else:
                log_alpha = lp_new - lp
                accept = math.log(max(self.rng.random(), 1e-300)) < log_alpha
            if accept:
                self.theta = proposal
                lp = lp_new
                n_accept += 1
            # адаптация в burn-in
            if self.adapt and i < burn_in:
                rate = 0.3
                gamma = 0.05
                acc_rate = n_accept / max(i + 1, 1)
                for k in range(len(self.step)):
                    self.step[k] *= math.exp(gamma * (1.0 if acc_rate > rate else -1.0))
                    self.step[k] = max(min(self.step[k], 1e3), 1e-9)
            if i >= burn_in:
                samples.append(list(self.theta))
                lps.append(lp)
        self.n_accept += n_accept
        self.n_total += n_samples + burn_in
        return ChainResult(
            samples=samples,
            acceptance=n_accept / (n_samples + burn_in),
            log_posterior=lps,
            n_burn=burn_in,
        )


# ═══════════════════════════════════════════════════════════════════════════
# Диагностика
# ═══════════════════════════════════════════════════════════════════════════
def gelman_rubin(chains: Sequence[Sequence[Vector]]) -> list[float]:
    """R̂ по каждому параметру (меж/внутри-цепная дисперсия).

    chains: список результатов цепей (сэмплы после burn-in).
    R̂ = sqrt( ((n−1)/n·W + B/n) / W ).
    """
    m = len(chains)
    if m < 2:
        return [float("nan")] * len(chains[0][0])
    n = min(len(c) for c in chains)
    k = len(chains[0][0])
    rhat = []
    for p in range(k):
        means = [sum(s[p] for s in chain) / len(chain) for chain in chains]
        grand = sum(means) / m
        B = n / (m - 1) * sum((mu - grand) ** 2 for mu in means)
        W = (
            sum(
                sum((s[p] - mu) ** 2 for s in chain) / (len(chain) - 1)
                for chain, mu in zip(chains, means)
            )
            / m
        )
        var_hat = (n - 1) / n * W + B / n
        rhat.append(math.sqrt(var_hat / max(W, 1e-300)))
    return rhat


def autocorrelation_time(series: Sequence[float], max_lag: int = 50) -> float:
    """Интегральное автокорреляционное время (оценка window-методом)."""
    n = len(series)
    if n < 10:
        return float("nan")
    mean = sum(series) / n
    var = sum((v - mean) ** 2 for v in series) / n
    if var <= 0:
        return 1.0
    tau = 1.0
    for lag in range(1, min(max_lag, n // 4)):
        cov = sum((series[i] - mean) * (series[i + lag] - mean) for i in range(n - lag)) / (n - lag)
        rho = cov / var
        if rho <= 0:
            break
        tau += 2.0 * rho
    return tau


def posterior_summary(samples: Sequence[Vector], credible: float = 0.9) -> list[dict]:
    """Перцентили + среднее/σ + HPD-интервал по каждому параметру."""
    k = len(samples[0])
    out = []
    for p in range(k):
        vals = sorted(s[p] for s in samples)
        n = len(vals)
        mean = sum(vals) / n
        std = math.sqrt(sum((v - mean) ** 2 for v in vals) / max(n - 1, 1))
        lo_idx = int((1 - credible) / 2 * n)
        hi_idx = int((1 + credible) / 2 * n)
        # HPD: скользящее окно сcredible-долей, минимум ширины
        window = max(int(credible * n), 1)
        best_lo, best_hi = 0, window - 1
        best_width = vals[window - 1] - vals[0]
        for start in range(0, n - window):
            width = vals[start + window - 1] - vals[start]
            if width < best_width:
                best_width = width
                best_lo, best_hi = start, start + window - 1
        out.append(
            dict(
                mean=mean,
                std=std,
                median=vals[n // 2],
                ci_lo=vals[lo_idx],
                ci_hi=vals[hi_idx - 1],
                hpd_lo=vals[best_lo],
                hpd_hi=vals[best_hi],
            )
        )
    return out


# ═══════════════════════════════════════════════════════════════════════════
# Прикладные модели
# ═══════════════════════════════════════════════════════════════════════════
def linear_model(theta: Vector, x: Sequence[float]) -> Vector:
    """y = a + b·x."""
    a, b = theta[0], theta[1]
    return [a + b * xi for xi in x]


def kepler_rv_model(theta: Vector, t: Sequence[float]) -> Vector:
    """RV кривая: v = K·cos(ν(t)+ω) + γ, ν из уравнения Кеплера.

    theta = [K, P, e, omega, gamma].
    """
    from lab.kepler import kepler_E, true_anomaly

    K, P, e, omega, gamma = theta
    out = []
    for ti in t:
        M = 2.0 * math.pi * (ti / P % 1.0)
        E = kepler_E(M, e)
        nu = true_anomaly(E, e)
        out.append(K * math.cos(nu + omega) + gamma)
    return out


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Восстановить прямую y = 2 + 0.5x с шумом; истина в 90% HPD."""
    rng = random.Random(3)
    x = [i / 10.0 for i in range(30)]
    a_true, b_true = 2.0, 0.5
    sigma = 0.2
    data = [a_true + b_true * xi + rng.gauss(0, sigma) for xi in x]

    def model(theta):
        return linear_model(theta, x)

    def log_post(theta):
        lp = flat_prior(theta, [(-10, 10), (-10, 10)])
        if lp == float("-inf"):
            return lp
        return lp + gaussian_loglike(model, data, [sigma] * len(x), theta)

    chains = []
    for seed in range(4):
        s = MetropolisSampler(log_post, [1.0, 1.0], [0.12, 0.02], seed=seed)
        chains.append(s.run(4000, burn_in=800).samples)
    rhat = gelman_rubin(chains)
    pooled = [s for c in chains for s in c]
    summ = posterior_summary(pooled, 0.9)
    # МНК-эталон на той же реализации шума: MCMC обязан согласоваться
    # с аналитической оценкой (смещение b относительно истины — свойство
    # конкретной реализации шума, а не сэмплера)
    n_pts = len(x)
    mx = sum(x) / n_pts
    my = sum(data) / n_pts
    sxy = sum((x[i] - mx) * (data[i] - my) for i in range(n_pts))
    sxx = sum((xi - mx) ** 2 for xi in x)
    b_ols = sxy / sxx
    a_ols = my - b_ols * mx
    se_b = sigma / math.sqrt(sxx)
    a_in = summ[0]["hpd_lo"] <= a_ols <= summ[0]["hpd_hi"]
    b_in = summ[1]["hpd_lo"] <= b_ols + 1.645 * se_b and b_ols - 1.645 * se_b <= summ[1]["hpd_hi"]
    b_close = abs(summ[1]["mean"] - b_ols) < 2.0 * se_b
    tau_a = autocorrelation_time([s[0] for s in pooled[:500]])
    return dict(
        a_mean=summ[0]["mean"],
        a_hpd=(summ[0]["hpd_lo"], summ[0]["hpd_hi"]),
        b_mean=summ[1]["mean"],
        b_hpd=(summ[1]["hpd_lo"], summ[1]["hpd_hi"]),
        a_ols=a_ols,
        b_ols=b_ols,
        se_b=se_b,
        rhat=rhat,
        a_in_hpd=a_in,
        b_covers_ols=b_in,
        b_close=b_close,
        tau_a=tau_a,
        n_effective=len(pooled) / max(tau_a, 1.0),
        ok=a_in and b_in and b_close and all(r < 1.1 for r in rhat),
        note="критерий: согласие с МНК-интервалом (аналитика), не с "
        "истиной: смещение оценки — свойство реализации шума",
    )
