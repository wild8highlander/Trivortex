#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — сводные графики для отчётов.

matplotlib при наличии (в стилях neon_dark/scientific/minimal),
иначе — ASCII-таблицы (движок отчётов встраивает их в <pre>).
"""

from __future__ import annotations

from typing import Sequence

try:
    from render.backend_mpl import HAVE_MPL
except Exception:
    HAVE_MPL = False


def summary_bar(
    values: Sequence[float],
    labels: Sequence[str],
    output: str,
    title: str = "",
    style: str = "neon_dark",
    ylabel: str = "",
) -> str | None:
    """Столбчатая сводка (например, метрики по телам)."""
    if not HAVE_MPL:
        return None
    import matplotlib.pyplot as plt
    from render.backend_mpl import STYLES, _apply_style, _fig_style

    s = STYLES.get(style, STYLES["neon_dark"])
    fig, ax = plt.subplots(figsize=(8, 4.4), constrained_layout=True)
    _fig_style(fig, style)
    _apply_style(ax, style)
    colors = s["body_colors"][: len(values)]
    bars = ax.bar(labels, values, color=colors, width=0.62, edgecolor="white", linewidth=0.5)
    for b, v in zip(bars, values):
        ax.text(
            b.get_x() + b.get_width() / 2,
            b.get_height(),
            f"{v:.3g}",
            ha="center",
            va="bottom",
            fontsize=8.5,
            color=s["text"],
        )
    if title:
        ax.set_title(title, color=s["text"], fontsize=11)
    if ylabel:
        ax.set_ylabel(ylabel, color=s["text"])
    fig.savefig(output, dpi=150, facecolor=s["facecolor"])
    plt.close(fig)
    return output


def ascii_table(
    headers: Sequence[str], rows: Sequence[Sequence], widths: Sequence[int] | None = None
) -> str:
    """Текстовая таблица с рамками (fallback без matplotlib)."""
    if not rows:
        rows = [["—"] * len(headers)]
    n = len(headers)
    if widths is None:
        widths = [max(len(str(headers[i])), *(len(str(r[i])) for r in rows)) + 2 for i in range(n)]
    sep = "+" + "+".join("-" * w for w in widths) + "+"
    out = [sep]
    out.append("|" + "|".join(f" {str(headers[i]):<{widths[i] - 1}}" for i in range(n)) + "|")
    out.append(sep)
    for r in rows:
        out.append(
            "|" + "|".join(f" {str(r[i])[:widths[i] - 2]:<{widths[i] - 1}}" for i in range(n)) + "|"
        )
    out.append(sep)
    return "\n".join(out)


def correlation_heatmap(
    matrix: Sequence[Sequence[float]],
    labels: Sequence[str],
    output: str,
    title: str = "Корреляции метрик",
    style: str = "neon_dark",
) -> str | None:
    """Do correlation heatmap for matrix, labels, output, title and return the result."""
    if not HAVE_MPL:
        return None
    import matplotlib.pyplot as plt
    from render.backend_mpl import STYLES, _apply_style, _fig_style

    s = STYLES.get(style, STYLES["neon_dark"])
    fig, ax = plt.subplots(figsize=(6.6, 5.4), constrained_layout=True)
    _fig_style(fig, style)
    _apply_style(ax, style)
    im = ax.imshow(matrix, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=8, color=s["text"])
    ax.set_yticklabels(labels, fontsize=8, color=s["text"])
    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(
                j,
                i,
                f"{matrix[i][j]:.2f}",
                ha="center",
                va="center",
                fontsize=7.5,
                color="#0A1120" if abs(matrix[i][j]) > 0.5 else s["text"],
            )
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.ax.tick_params(colors=s["text"])
    ax.set_title(title, color=s["text"], fontsize=11)
    fig.savefig(output, dpi=150, facecolor=s["facecolor"])
    plt.close(fig)
    return output
