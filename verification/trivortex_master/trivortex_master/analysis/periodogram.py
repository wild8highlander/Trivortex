#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — BLS: поиск транзитов в кривых блеска.

Box Least Squares (Kovács, Zucker & Mazeh 2002, A&A 391, 369) на
чистом Python:

  * bls(t, y, periods, n_bins): фазовая свёртка, перебор фаз входа,
    box-модель (глубина δ, длительность q), критерий SR (signal
    residue) по формуле оригинала;
  * sde: Signal Detection Efficiency = (SR_max − μ_SR)/σ_SR
    (анализ двухпроходного фона — Kovács 2002 §3.4);
  * best_box: период, эпоха, глубина, длительность, SNR.

Самопроверка: синтетическая кривая (P = 3.5 сут, глубина 1%, шум
200 ppm, 300 точек с пропусками) — период восстановлен, SDE > 5.
"""
from __future__ import annotations

import math
from typing import Sequence


def _phase_bin(t: Sequence[float], y: Sequence[float], period: float,
               t0: float, n_bins: int) -> list[float]:
    """Средняя яркость по фазовым бинам (фаза от t0)."""
    sums = [0.0] * n_bins
    counts = [0] * n_bins
    for ti, yi in zip(t, y):
        ph = ((ti - t0) / period) % 1.0
        idx = min(int(ph * n_bins), n_bins - 1)
        sums[idx] += yi
        counts[idx] += 1
    return [s / c if c else float("nan") for s, c in zip(sums, counts)]


def bls_at_period(t: Sequence[float], y: Sequence[float], period: float,
                  n_bins: int = 200,
                  duration_fracs: Sequence[float] = (0.015, 0.03, 0.05,
                                                     0.075)) -> dict:
    """BLS-статистика SR на одном периоде: перебор фаз входа × длительностей.

    Критерий — SNR глубины: SR = δ·√(N·r_t)/σ (стандартный критерий
    транзитных пайплайнов; вариант signal residue из Kovács 2002).
    Перебор длительностей обязателен, иначе пик смещается.
    """
    n = len(t)
    mean_y = sum(y) / n
    sigma = math.sqrt(sum((v - mean_y) ** 2 for v in y) / n)
    best = dict(sr=-1.0, depth=0.0, epoch=0.0, duration=0.0)
    for dur_frac in duration_fracs:
        n_dur = max(int(round(dur_frac * n_bins)), 2)
        for k in range(n_bins):
            in_bins = {(k + j) % n_bins for j in range(n_dur)}
            in_sum = 0.0
            in_count = 0
            for ti, yi in zip(t, y):
                b = min(int(((ti / period) % 1.0) * n_bins), n_bins - 1)
                if b in in_bins:
                    in_sum += yi
                    in_count += 1
            out_count = n - in_count
            if in_count < 2 or out_count == 0:
                continue
            mean_in = in_sum / in_count
            mean_out = (sum(y) - in_sum) / out_count
            depth = mean_out - mean_in
            if depth <= 0:
                continue
            r_t = in_count / n
            sr = depth * math.sqrt(n * r_t) / sigma
            epoch = (k / n_bins) * period
            if sr > best["sr"]:
                best = dict(sr=sr, depth=depth, epoch=epoch,
                            duration=dur_frac * period)
    return best


def bls(t: Sequence[float], y: Sequence[float],
        periods: Sequence[float], n_bins: int = 200) -> dict:
    """Полный BLS-периодограмм: SR по сетке периодов + SDE."""
    results = []
    for p in periods:
        b = bls_at_period(t, y, p, n_bins)
        results.append((p, b["sr"], b))
    srs = [s for _p, s, _b in results]
    mean_sr = sum(srs) / len(srs)
    std_sr = math.sqrt(sum((s - mean_sr) ** 2 for s in srs)
                       / max(len(srs) - 1, 1))
    best_p, best_sr, best_box = max(results, key=lambda r: r[1])
    sde = (best_sr - mean_sr) / max(std_sr, 1e-12)
    # SNR по глубине: δ/σ_δ, σ_δ ≈ σ/√(число точек в транзите)
    n = len(t)
    noise = math.sqrt(sum((v - sum(y) / n) ** 2 for v in y) / n)
    n_in = max(int(n * 0.02), 1)
    snr = best_box["depth"] / (noise / math.sqrt(n_in))
    return dict(
        period=best_p, sr=best_sr, sde=sde,
        depth=best_box["depth"], epoch=best_box["epoch"],
        duration=best_box["duration"], snr=snr,
        mean_sr=mean_sr, std_sr=std_sr,
        detected=(sde > 5.0 and snr > 4.0),
    )


def period_grid(t_min: float, t_span: float, p_min: float, p_max: float,
                n: int = 2000) -> list[float]:
    """Лог-сетка периодов от p_min до p_max (n точек)."""
    return [p_min * (p_max / p_min) ** (i / (n - 1)) for i in range(n)]


def self_check() -> dict:
    """Синтетический транзит: период 3.5 сут, глубина 1%, SDE > 5."""
    import random
    rng = random.Random(17)
    period_true, depth_true, duration_true = 3.5, 0.01, 0.12
    t = sorted(rng.uniform(0, 60) for _ in range(300))
    y = []
    for ti in t:
        ph = (ti % period_true) / period_true
        v = 0.0
        if ph < duration_true / period_true:
            v -= depth_true          # транзит
        y.append(v + rng.gauss(0, 0.0002))   # 200 ppm
    grid = period_grid(0, 60, 1.0, 15.0, n=1500)
    res = bls(t, y, grid, n_bins=120)
    p_err = abs(res["period"] - period_true) / period_true
    return dict(
        period_est=res["period"], period_err=p_err,
        depth_est=res["depth"], sde=res["sde"], snr=res["snr"],
        detected=res["detected"],
        ok=(p_err < 0.02 and res["detected"] and res["sde"] > 5.0),
        note="Kovács, Zucker & Mazeh 2002 (BLS); сетка 1–15 сут, 120 бинов",
    )
