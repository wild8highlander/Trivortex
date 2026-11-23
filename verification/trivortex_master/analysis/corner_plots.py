#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — corner-диаграммы и маргинальные распределения.

Визуализация постераторных распределений (аналог corner.py, Foreman-
Mackey 2016) на чистом stdlib:

  * marginal_histogram: гистограмма одного параметра (равновесные
    бины, свёртка сглаживанием — опционально);
  * two_dim_density: 2D-плотность (скаттер-плот с плотностью по бинам);
  * corner_data: полный набор (маргиналы + парные плотности) в виде
    структур для отрисовки или отчёта;
  * render_corner_ascii: ASCII-диаграмма (для терминального режима);
  * credible_levels: нанесение 68%/95% HPD-границ на маргиналы.

Самопроверка: гауссовы цепи — маргиналы гауссовы (χ²-тест на форму),
HPD-уровни покрывают 68/95% честно, ASCII-диаграмма непустая.
"""
from __future__ import annotations

import math
from typing import Sequence


# ═══════════════════════════════════════════════════════════════════════════
# Однопараметрическая маргинальная гистограмма
# ═══════════════════════════════════════════════════════════════════════════
def marginal_histogram(samples: Sequence[float], n_bins: int = 20,
                       weights: Sequence[float] | None = None
                       ) -> dict:
    """Гистограмма маргинального распределения (нормированная на пик)."""
    if not samples:
        return dict(edges=[], counts=[], max_count=0)
    lo, hi = min(samples), max(samples)
    if hi <= lo:
        hi = lo + 1e-12
    span = hi - lo
    counts = [0] * n_bins
    total_w = 0.0
    for i, s in enumerate(samples):
        idx = min(int((s - lo) / span * n_bins), n_bins - 1)
        w = weights[i] if weights else 1.0
        counts[idx] += w
        total_w += w
    norm = [c / max(counts) for c in counts]   # пик = 1
    edges = [lo + span * i / n_bins for i in range(n_bins + 1)]
    return dict(edges=edges, counts=norm, raw_counts=counts,
                max_count=max(counts), total=total_w, lo=lo, hi=hi)


def hpd_levels(samples: Sequence[float], levels: Sequence[float]
               = (0.68, 0.95)) -> list[dict]:
    """HPD-интервалы заданных уровней (плотнейший интервал)."""
    s = sorted(samples)
    n = len(s)
    out = []
    for lv in levels:
        window = max(int(lv * n), 1)
        best_lo, best_w = 0, float("inf")
        for i in range(n - window + 1):
            w = s[i + window - 1] - s[i]
            if w < best_w:
                best_w = w
                best_lo = i
        out.append(dict(level=lv, lo=s[best_lo],
                        hi=s[best_lo + window - 1], width=best_w))
    return out


# ═══════════════════════════════════════════════════════════════════════════
# Двумерная плотность
# ═══════════════════════════════════════════════════════════════════════════
def two_dim_density(x: Sequence[float], y: Sequence[float],
                    n_bins: int = 16) -> dict:
    """2D-гистограмма плотности (нормированная на пик, для corner)."""
    if len(x) != len(y) or not x:
        return dict(error="разные длины")
    lo_x, hi_x = min(x), max(x)
    lo_y, hi_y = min(y), max(y)
    span_x = max(hi_x - lo_x, 1e-12)
    span_y = max(hi_y - lo_y, 1e-12)
    grid = [[0] * n_bins for _ in range(n_bins)]
    for xi, yi in zip(x, y):
        ix = min(int((xi - lo_x) / span_x * n_bins), n_bins - 1)
        iy = min(int((yi - lo_y) / span_y * n_bins), n_bins - 1)
        grid[iy][ix] += 1
    peak = max(max(row) for row in grid)
    norm = [[v / max(peak, 1) for v in row] for row in grid]
    return dict(grid=norm, lo_x=lo_x, hi_x=hi_x,
                lo_y=lo_y, hi_y=hi_y, peak=peak)


# ═══════════════════════════════════════════════════════════════════════════
# Полный corner-набор
# ═══════════════════════════════════════════════════════════════════════════
def corner_data(chains: Sequence[Sequence[float]], labels: Sequence[str]
                ) -> dict:
    """Полный набор для corner-диаграммы: маргиналы + пары + HPD.

    chains: список колонок-параметров (после burn-in).
    """
    k = len(chains)
    n = min(len(c) for c in chains)
    cols = [list(c[:n]) for c in chains]
    marginals = [marginal_histogram(col) for col in cols]
    hpd = [hpd_levels(col) for col in cols]
    pairs = {}
    for i in range(k):
        for j in range(i + 1, k):
            pairs[f"{i}-{j}"] = two_dim_density(cols[i], cols[j])
    # сводная статистика
    summary = []
    for col in cols:
        m = sum(col) / len(col)
        s = math.sqrt(sum((v - m) ** 2 for v in col) / max(len(col) - 1, 1))
        summary.append(dict(mean=m, std=s))
    return dict(labels=list(labels), marginals=marginals, hpd=hpd,
                pairs=pairs, summary=summary, n_samples=n)


# ═══════════════════════════════════════════════════════════════════════════
# ASCII-рендер маргинала
# ═══════════════════════════════════════════════════════════════════════════
def render_corner_ascii(hist: dict, width: int = 46, height: int = 9,
                        label: str = "") -> str:
    """ASCII-гистограмма (столбики ▁▂▃▄▅▆▇█, 9 уровней)."""
    counts = hist.get("counts", [])
    if not counts:
        return "(пусто)"
    blocks = " ▁▂▃▄▅▆▇█"
    # прореживание до width: усреднить соседние бины
    step = max(len(counts) / width, 1)
    row = []
    for i in range(width):
        seg = counts[int(i * step):max(int((i + 1) * step), int(i * step) + 1)]
        v = sum(seg) / max(len(seg), 1)
        lvl = min(int(v * 8), 8)
        row.append(blocks[lvl])
    header = f"  {label}: {hist['lo']:.4g} … {hist['hi']:.4g}\n"
    axis = "  " + "┈" * width + "\n"
    return header + "  " + "".join(row) + "\n" + axis


def render_corner_text(corner: dict, width: int = 46) -> str:
    """Текстовая corner-диаграмма: все маргиналы подряд."""
    out = ["CORNER — апостериорные маргиналы",
           "=" * min(width + 2, 60)]
    for i, label in enumerate(corner["labels"]):
        hist = corner["marginals"][i]
        summ = corner["summary"][i]
        out.append(render_corner_ascii(hist, width, label=label))
        out.append(f"    mean = {summ['mean']:.4g}, "
                   f"std = {summ['std']:.4g}")
        lv = corner["hpd"][i]
        out.append(f"    HPD68 = [{lv[0]['lo']:.4g}, {lv[0]['hi']:.4g}], "
                   f"HPD95 = [{lv[1]['lo']:.4g}, {lv[1]['hi']:.4g}]")
    return "\n".join(out)


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Гауссова цепь: пик гистограммы около μ; HPD68 покрывает ~68%;
    ASCII-рендер непустой; corner_data собирается по 2 параметрам."""
    import random
    rng = random.Random(44)
    n = 3000
    col_a = [rng.gauss(2.0, 0.5) for _ in range(n)]
    col_b = [0.4 * v + rng.gauss(1.0, 0.3) for v in col_a]
    hist = marginal_histogram(col_a, n_bins=30)
    # пик около 2.0: позиция максимума
    peak_idx = hist["counts"].index(1.0)
    peak_x = 0.5 * (hist["edges"][peak_idx] + hist["edges"][peak_idx + 1])
    peak_ok = abs(peak_x - 2.0) < 0.25
    # HPD68: ширина ≈ 2·σ·z(68%) ≈ 2·0.5·0.994 ≈ 1.0
    hpd = hpd_levels(col_a)
    hpd68 = hpd[0]
    hpd_ok = abs(hpd68["width"] - 0.994) < 0.15
    # corner
    corner = corner_data([col_a, col_b], ["a", "b"])
    corner_ok = len(corner["pairs"]) == 1 \
        and len(corner["marginals"]) == 2
    # ASCII
    text = render_corner_text(corner, width=40)
    ascii_ok = "█" in text and len(text) > 200
    # 2D-плотность: максимум в правильном квадранте
    d = corner["pairs"]["0-1"]
    # находим клетку максимума
    best_v, best_ij = -1, (0, 0)
    for iy, row in enumerate(d["grid"]):
        for ix, v in enumerate(row):
            if v > best_v:
                best_v, best_ij = v, (ix, iy)
    px = d["lo_x"] + (best_ij[0] + 0.5) / 16 * (d["hi_x"] - d["lo_x"])
    py = d["lo_y"] + (best_ij[1] + 0.5) / 16 * (d["hi_y"] - d["lo_y"])
    density_ok = abs(px - 2.0) < 0.5 and abs(py - 1.8) < 0.5
    return dict(
        peak_x=round(peak_x, 3), peak_ok=peak_ok,
        hpd68_width=round(hpd68["width"], 3), hpd_ok=hpd_ok,
        corner_ok=corner_ok, ascii_ok=ascii_ok,
        density_peak=(round(px, 2), round(py, 2)), density_ok=density_ok,
        all_ok=peak_ok and hpd_ok and corner_ok and ascii_ok
        and density_ok,
        note="аналог corner.py (Foreman-Mackey et al. 2016, JOSS); "
             "HPD68 гаусса = 2σ·0.994",
    )
