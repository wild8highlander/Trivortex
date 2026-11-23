#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — matplotlib-бэкенд: 2D-орбиты, 3D-траектории, 4D-срезы.

Стили: neon_dark (тёмный фон, неоновые линии — по умолчанию),
scientific (светлый, для публикаций), minimal (ч/б).

Загружается только при установленном matplotlib; иначе движок render.engine
откатывается на pure/ascii.
"""
from __future__ import annotations

import math
import os
from typing import Any, Sequence

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    HAVE_MPL = True
except ImportError:
    HAVE_MPL = False
    plt = None  # type: ignore

STYLES = {
    "neon_dark": dict(
        facecolor="#0A1120", axes_facecolor="#0E1B2E", text="#E6F0FA",
        grid="#22344E", spine="#3A5068",
        body_colors=["#37DCF2", "#E8C766", "#A78BFA", "#34D399",
                     "#FB7185", "#7DD3FC", "#FF9A76", "#C8D8D8"],
    ),
    "scientific": dict(
        facecolor="#FFFFFF", axes_facecolor="#FFFFFF", text="#1A2B40",
        grid="#D0D8E0", spine="#8B9BB4",
        body_colors=["#1B6B7A", "#B08030", "#6B5CA5", "#2E8B57",
                     "#C25B6A", "#5A8FBF", "#C87A3F", "#7A8B99"],
    ),
    "minimal": dict(
        facecolor="#FFFFFF", axes_facecolor="#FFFFFF", text="#000000",
        grid="#CCCCCC", spine="#999999",
        body_colors=["#000000", "#444444", "#777777", "#222222",
                     "#555555", "#888888", "#333333", "#666666"],
    ),
}


def _apply_style(ax, style: str) -> None:
    s = STYLES.get(style, STYLES["neon_dark"])
    ax.set_facecolor(s["axes_facecolor"])
    ax.tick_params(colors=s["text"])
    for spine in ax.spines.values():
        spine.set_color(s["spine"])
    ax.grid(True, alpha=0.35, color=s["grid"])


def _fig_style(fig, style: str) -> None:
    s = STYLES.get(style, STYLES["neon_dark"])
    fig.patch.set_facecolor(s["facecolor"])


def _color_for(body_color: str | None, index: int, style: str) -> str:
    if body_color:
        return body_color
    s = STYLES.get(style, STYLES["neon_dark"])
    return s["body_colors"][index % len(s["body_colors"])]


# ═══════════════════════════════════════════════════════════════════════════
# 2D: орбиты в проекции
# ═══════════════════════════════════════════════════════════════════════════
def plot_2d(traj, output: str, style: str = "neon_dark",
            plane: str = "xy", title: str = "", dpi: int = 150,
            body_names: Sequence[str] | None = None,
            body_colors: Sequence[str] | None = None) -> str:
    """traj: lab.trajectory.Trajectory (или dict с times/states)."""
    if not HAVE_MPL:
        raise ImportError("matplotlib не установлен")
    s = STYLES.get(style, STYLES["neon_dark"])
    fig, ax = plt.subplots(figsize=(9, 7), constrained_layout=True)
    _fig_style(fig, style)
    _apply_style(ax, style)
    idx = {"xy": (0, 1), "xz": (0, 2), "yz": (1, 2)}[plane]
    n_bodies = len(traj.body_ids)
    for b in range(n_bodies):
        xs = [st[b][idx[0]] for st in traj.states]
        ys = [st[b][idx[1]] for st in traj.states]
        color = _color_for(body_colors[b] if body_colors else None, b, style)
        name = body_names[b] if body_names else traj.body_ids[b]
        ax.plot(xs, ys, color=color, lw=1.4, label=name, alpha=0.95)
        # конечная точка
        ax.scatter([xs[-1]], [ys[-1]], color=color, s=42, zorder=5,
                   edgecolors=s["facecolor"], linewidths=0.8)
    ax.set_xlabel(f"{plane[0]} (м)" if plane else "", color=s["text"])
    ax.set_ylabel(f"{plane[1]} (м)", color=s["text"])
    ax.set_title(title or f"Проекция {plane}: {n_bodies} тел",
                 color=s["text"], fontsize=12)
    ax.legend(frameon=False, labelcolor=s["text"], fontsize=9)
    ax.set_aspect("equal", adjustable="datalim")
    fig.savefig(output, dpi=dpi, facecolor=s["facecolor"])
    plt.close(fig)
    return output


# ═══════════════════════════════════════════════════════════════════════════
# 3D: траектории
# ═══════════════════════════════════════════════════════════════════════════
def plot_3d(traj, output: str, style: str = "neon_dark",
            title: str = "", dpi: int = 150, elev: int = 22, azim: int = 36,
            body_names: Sequence[str] | None = None,
            body_colors: Sequence[str] | None = None,
            sphere_scale: float | None = None) -> str:
    if not HAVE_MPL:
        raise ImportError("matplotlib не установлен")
    s = STYLES.get(style, STYLES["neon_dark"])
    fig = plt.figure(figsize=(9.5, 7.5), constrained_layout=True)
    _fig_style(fig, style)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor(s["axes_facecolor"])
    n_bodies = len(traj.body_ids)
    for b in range(n_bodies):
        xs = [st[b][0] for st in traj.states]
        ys = [st[b][1] for st in traj.states]
        zs = [st[b][2] for st in traj.states]
        color = _color_for(body_colors[b] if body_colors else None, b, style)
        name = body_names[b] if body_names else traj.body_ids[b]
        ax.plot(xs, ys, zs, color=color, lw=1.2, label=name)
        ax.scatter([xs[-1]], [ys[-1]], [zs[-1]], color=color, s=48,
                   depthshade=False)
    ax.set_xlabel("x", color=s["text"])
    ax.set_ylabel("y", color=s["text"])
    ax.set_zlabel("z", color=s["text"])
    ax.tick_params(colors=s["text"])
    ax.set_title(title or f"3D-траектории: {n_bodies} тел",
                 color=s["text"], fontsize=12)
    ax.view_init(elev=elev, azim=azim)
    ax.xaxis.pane.set_alpha(0.05)
    ax.yaxis.pane.set_alpha(0.05)
    ax.zaxis.pane.set_alpha(0.05)
    ax.legend(frameon=False, labelcolor=s["text"], fontsize=9)
    fig.savefig(output, dpi=dpi, facecolor=s["facecolor"])
    plt.close(fig)
    return output


# ═══════════════════════════════════════════════════════════════════════════
# 4D: четвёртая координата — цветом, глубина гиперсцены — размером
# ═══════════════════════════════════════════════════════════════════════════
def plot_4d(traj, w_values: list[list[float]], output: str,
            style: str = "neon_dark", title: str = "", dpi: int = 150,
            body_names: Sequence[str] | None = None) -> str:
    """w_values[t][body] — четвёртая координата каждого тела в каждый момент.

    Кодировка: x-y проекция + цвет по w (viridis) + размер маркера по |w|.
    """
    if not HAVE_MPL:
        raise ImportError("matplotlib не установлен")
    s = STYLES.get(style, STYLES["neon_dark"])
    fig, ax = plt.subplots(figsize=(9, 7), constrained_layout=True)
    _fig_style(fig, style)
    _apply_style(ax, style)
    n_bodies = len(traj.body_ids)
    cmap = plt.get_cmap("viridis")
    all_w = [abs(w) for frame in w_values for w in frame] or [1.0]
    w_max = max(all_w) or 1.0
    for b in range(n_bodies):
        xs = [st[b][0] for st in traj.states]
        ys = [st[b][1] for st in traj.states]
        ws = [frame[b] for frame in w_values]
        name = body_names[b] if body_names else traj.body_ids[b]
        sc = ax.scatter(xs, ys, c=ws, cmap=cmap, vmin=-w_max, vmax=w_max,
                        s=[14 + 46 * abs(w) / w_max for w in ws],
                        alpha=0.85, label=name, edgecolors="none")
    cbar = fig.colorbar(sc, ax=ax, shrink=0.85)
    cbar.set_label("w (4-я координата)", color=s["text"])
    cbar.ax.tick_params(colors=s["text"])
    ax.set_xlabel("x", color=s["text"])
    ax.set_ylabel("y", color=s["text"])
    ax.set_title(title or f"4D-гиперсцена: {n_bodies} тел (цвет/размер = w)",
                 color=s["text"], fontsize=12)
    ax.legend(frameon=False, labelcolor=s["text"], fontsize=9,
              markerscale=0.5)
    fig.savefig(output, dpi=dpi, facecolor=s["facecolor"])
    plt.close(fig)
    return output


# ═══════════════════════════════════════════════════════════════════════════
# Служебные графики для отчётов
# ═══════════════════════════════════════════════════════════════════════════
def plot_energy(times: Sequence[float], energies: Sequence[float],
                output: str, style: str = "neon_dark",
                title: str = "Сохранение энергии", dpi: int = 150) -> str:
    if not HAVE_MPL:
        raise ImportError("matplotlib не установлен")
    s = STYLES.get(style, STYLES["neon_dark"])
    fig, ax = plt.subplots(figsize=(8, 4.6), constrained_layout=True)
    _fig_style(fig, style)
    _apply_style(ax, style)
    e0 = energies[0] if energies else 0.0
    rel = [(e - e0) / (abs(e0) if e0 else 1.0) for e in energies]
    ax.plot(times, rel, color=s["body_colors"][0], lw=1.4)
    ax.axhline(0, color=s["spine"], lw=0.8, alpha=0.6)
    ax.set_xlabel("t", color=s["text"])
    ax.set_ylabel("ΔE/E₀", color=s["text"])
    ax.set_title(title, color=s["text"], fontsize=11)
    fig.savefig(output, dpi=dpi, facecolor=s["facecolor"])
    plt.close(fig)
    return output


def plot_distances(traj, output: str, style: str = "neon_dark",
                   reference_index: int = 0, dpi: int = 150,
                   names: Sequence[str] | None = None) -> str:
    """Расстояния всех тел до опорного (индекс) по времени."""
    if not HAVE_MPL:
        raise ImportError("matplotlib не установлен")
    s = STYLES.get(style, STYLES["neon_dark"])
    fig, ax = plt.subplots(figsize=(8, 4.6), constrained_layout=True)
    _fig_style(fig, style)
    _apply_style(ax, style)
    n = len(traj.body_ids)
    for b in range(n):
        if b == reference_index:
            continue
        ds = [math.dist(st[reference_index][:3], st[b][:3])
              for st in traj.states]
        name = names[b] if names else traj.body_ids[b]
        ax.plot(traj.times, ds, lw=1.2,
                color=_color_for(None, b, style), label=name)
    ref = names[reference_index] if names else traj.body_ids[reference_index]
    ax.set_xlabel("t", color=s["text"])
    ax.set_ylabel(f"расстояние до {ref}", color=s["text"])
    ax.set_title("Эволюция межтелных расстояний", color=s["text"], fontsize=11)
    ax.legend(frameon=False, labelcolor=s["text"], fontsize=9)
    fig.savefig(output, dpi=dpi, facecolor=s["facecolor"])
    plt.close(fig)
    return output


def plot_havelock_scan(output: str, style: str = "neon_dark",
                       dpi: int = 150) -> str:
    """Иллюстрация порога Хавелока N≤7/N=8 (значения POLYVORTEX W4)."""
    if not HAVE_MPL:
        raise ImportError("matplotlib не установлен")
    s = STYLES.get(style, STYLES["neon_dark"])
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    _fig_style(fig, style)
    _apply_style(ax, style)
    ns = [2, 3, 4, 5, 6, 7, 8]
    lam = [6.9e-10, 1.7e-17, 3.8e-9, 1e-9, 1e-9, 7.0e-9, 0.4502]
    colors = [s["body_colors"][3] if v < 1e-6 else s["body_colors"][4]
              for v in lam]
    ax.bar([str(n) for n in ns], [max(v, 3e-10) for v in lam], color=colors)
    ax.set_yscale("log")
    ax.set_ylim(1e-11, 3)
    ax.axhline(1e-6, color=s["body_colors"][1], ls="--", lw=1.1)
    ax.text(0.02, 1.6e-6, "порог классификатора 1e-6",
            color=s["body_colors"][1], fontsize=8.5)
    ax.set_xlabel("N вихрей в кольце", color=s["text"])
    ax.set_ylabel("max Re λ", color=s["text"])
    ax.set_title("Порог Хавелока (POLYVORTEX W4): устойчиво N≤7, "
                 "неустойчиво N=8 (+0.4502)",
                 color=s["text"], fontsize=11)
    fig.savefig(output, dpi=dpi, facecolor=s["facecolor"])
    plt.close(fig)
    return output
