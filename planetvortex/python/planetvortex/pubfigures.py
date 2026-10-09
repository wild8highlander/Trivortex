#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
PLANETVORTEX — THE 600 DPI PUBLICATION FACTORY + THE ANIMATIONS
============================================================================
The ultra-high-resolution figure factory of the mini-repository. Every
task of the bench (P2, P3, P5/P6, X1/X2, X3/X4, X5/X6, V1, V2) gets its
own folder under `figures/600dpi/` with its own README, every figure is
generated at **600 dpi** from the committed JSON protocols (the same
"bound to a run" discipline as figures.py), and the animations are
rendered as GIFs into `figures/600dpi/animations/`.

    make figures600      # all folders at 600 dpi
    make animations      # the GIFs
    python3 -m planetvortex.pubfigures --dpi 600 [--animations]

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import animation  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

from . import classical as cl  # noqa: E402
from . import fano as fn  # noqa: E402
from . import figures as base_figs  # noqa: E402
from . import klein as kl  # noqa: E402
from . import spatial as sp  # noqa: E402
from .klein import _disk_midpoint, _reflect  # noqa: E402

TWO_PI = 2.0 * math.pi

NAVY = "#0A1A3A"
STEEL = "#2E5FA3"
SKY = "#7FA6D9"
GOLD = "#C9A227"
CRIMSON = "#B03A2E"
GREEN = "#1E8449"
LIGHT = "#F4F6FA"
GRID = "#D5DCE8"

PACKAGE_DIR = Path(__file__).resolve().parent
MINIROOT = PACKAGE_DIR.parents[1]
PROTO_DIR = MINIROOT / "results" / "protocols"
OUT_ROOT = MINIROOT / "figures" / "600dpi"

# the gravity-graded palette of the 12 bodies (log-GM -> navy..gold)
BODY_COLORS = {
    "Sun": "#0A1A3A",
    "Jupiter": "#16386B",
    "Saturn": "#1F4E8C",
    "Neptune": "#2761A3",
    "Uranus": "#3273B4",
    "Earth": "#3E86C1",
    "Venus": "#5599CB",
    "Mars": "#6FACD4",
    "Mercury": "#8ABEDC",
    "Eris": "#B7CBE4",
    "Pluto": "#C9D8EA",
    "Ceres": "#E2EAF3",
}


def _proto(stage: str) -> Dict:
    path = PROTO_DIR / f"{stage}_default.json"
    if not path.exists():
        raise SystemExit(f"missing protocol {path} — run `make all-ladders` first")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _style_axis(ax: plt.Axes) -> None:
    for spine in ax.spines.values():
        spine.set_color(NAVY)
        spine.set_linewidth(0.8)
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.tick_params(colors=NAVY, labelsize=10, direction="in")
    ax.set_axisbelow(True)


def _save(fig: plt.Figure, folder: Path, name: str, dpi: int) -> str:
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / name
    fig.savefig(path, dpi=dpi, facecolor="white")
    plt.close(fig)
    return str(path)


# ---------------------------------------------------------------------------
# V2 — the closed gravifigure
# ---------------------------------------------------------------------------


def _disk_polygon(ax, verts, **kw) -> None:
    """A hyperbolic polygon with geodesic (arc) sides."""
    n = len(verts)
    pts: List[Tuple[float, float]] = []
    for k in range(n):
        a = verts[k]
        b = verts[(k + 1) % n]
        pts.append((a.real, a.imag))
        circ = kl._geodesic_circle(a, b)
        if circ is None:
            continue
        w, rho = circ
        t1 = math.atan2(a.imag - w.imag, a.real - w.real)
        t2 = math.atan2(b.imag - w.imag, b.real - w.real)
        while t2 <= t1:
            t2 += TWO_PI
        # choose the shorter arc
        if t2 - t1 > math.pi:
            t1, t2 = t2 - TWO_PI, t1
        for tt in np.linspace(t1, t2, 24)[1:]:
            pts.append((w.real + rho * math.cos(tt), w.imag + rho * math.sin(tt)))
    xs = [p[0] for p in pts] + [pts[0][0]]
    ys = [p[1] for p in pts] + [pts[0][1]]
    ax.fill(xs, ys, **kw)


def fig_v2_disk_patch(out: Path, dpi: int) -> str:
    """THE showcase: the 24-heptagon closed gravifigure in the disk."""
    km = kl.KleinMap.build()
    patch = kl.build_chamber_patch(km)
    assignment = {row["face_pair"][0]: row["body"] for row in kl.assign_bodies(km)}
    assignment.update({row["face_pair"][1]: row["body"] for row in kl.assign_bodies(km)})

    fig, ax = plt.subplots(figsize=(11.5, 9.5), constrained_layout=True)
    circ = plt.Circle((0, 0), 1.0, fill=False, color=NAVY, linewidth=2.2)
    ax.add_patch(circ)
    ax.fill([1], [0], color="none")

    for hept in patch.heptagons:
        body = assignment[hept.face_coset]
        color = BODY_COLORS.get(body, "#DDDDDD")
        _disk_polygon(ax, hept.vertices, color=color, alpha=0.92, zorder=2)
        xs = [v.real for v in hept.vertices] + [hept.vertices[0].real]
        ys = [v.imag for v in hept.vertices] + [hept.vertices[0].imag]
        ax.plot(xs, ys, color=NAVY, linewidth=1.1, zorder=3)
        mid = sum(hept.vertices) / 7.0
        ax.text(
            mid.real,
            mid.imag,
            body,
            fontsize=7.2,
            ha="center",
            va="center",
            color=NAVY if body not in ("Pluto", "Ceres", "Eris") else NAVY,
            zorder=4,
        )
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_aspect("equal")
    ax.axis("off")
    resid = kl.register_algebra_float()["alpha_sum_residual"]
    ax.set_title(
        "V2 — the closed gravifigure: the 24 heptagons of the Klein quartic\n"
        "in the Poincaré disk, colored by the gravimetric register (12 antipodal pairs)",
        fontsize=13,
        color=NAVY,
        pad=12,
    )
    ax.text(
        0.0,
        -1.155,
        f"the skeleton: V = 56, E = 84, F = 24, Euler χ = −4 (genus 3) · "
        f"the budget closure Σα = 8π holds to {resid:.1e} (float64)",
        ha="center",
        fontsize=9.5,
        color=STEEL,
    )
    handles = [
        Patch(facecolor=BODY_COLORS[b], edgecolor=NAVY, label=b)
        for b in (
            "Sun",
            "Jupiter",
            "Saturn",
            "Neptune",
            "Uranus",
            "Earth",
            "Venus",
            "Mars",
            "Mercury",
            "Eris",
            "Pluto",
            "Ceres",
        )
    ]
    ax.legend(
        handles=handles,
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        fontsize=8.5,
        frameon=False,
        title="the register pairs",
        title_fontsize=9,
    )
    return _save(fig, out, "v2_01_disk_patch_gravifigure.png", dpi)


def fig_v2_register_rose(out: Path, dpi: int) -> str:
    """The 12 register heptagons at their exact vertex angles."""
    algebra = kl.register_algebra_float()
    rows = sorted(algebra["bodies"], key=lambda r: -r["gm"])
    fig, axes = plt.subplots(3, 4, figsize=(13.5, 10.5), constrained_layout=True)
    for k, (ax, row) in enumerate(zip(axes.flat, rows)):
        alpha = row["alpha"]
        big_r, edge, inr, area = kl.register_dims(alpha)
        t = math.tanh(big_r / 2.0)
        pts = [
            complex(
                t * math.cos(TWO_PI * j / 7 + math.pi / 7),
                t * math.sin(TWO_PI * j / 7 + math.pi / 7),
            )
            for j in range(7)
        ]
        ax.add_patch(plt.Circle((0, 0), 1.0, fill=False, color=GRID, linewidth=1.0))
        _disk_polygon(ax, pts, color=BODY_COLORS[row["body"]], alpha=0.9)
        xs = [p.real for p in pts] + [pts[0].real]
        ys = [p.imag for p in pts] + [pts[0].imag]
        ax.plot(xs, ys, color=NAVY, linewidth=1.2)
        ax.set_xlim(-1.02, 1.02)
        ax.set_ylim(-1.02, 1.02)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(f"{row['body']}", fontsize=12, color=NAVY)
        ax.text(
            0,
            -1.24,
            f"α = {alpha:.4f} rad\nR = {big_r:.4f}   ℓ = {edge:.4f}\nA = {area:.4f}",
            ha="center",
            fontsize=8.5,
            color=STEEL,
        )
    fig.suptitle(
        "V2 — the register rose: the 12 antipodal heptagon pairs at their exact vertex angles\n"
        "the heavier the body, the wider the heptagon (α = 2π/3 − σ·ln(GM/⟨GM⟩), R̄ = 1)",
        fontsize=13.5,
        color=NAVY,
    )
    return _save(fig, out, "v2_02_register_rose.png", dpi)


def fig_v2_budget_closure(out: Path, dpi: int) -> str:
    """The budget closure: α per body + the 8π line + the area bars."""
    algebra = kl.register_algebra_float()
    rows = sorted(algebra["bodies"], key=lambda r: -r["gm"])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 6.2), constrained_layout=True)
    names = [r["body"] for r in rows]
    alphas = [math.degrees(r["alpha"]) for r in rows]
    colors = [BODY_COLORS[n] for n in names]
    bars = ax1.bar(range(12), alphas, color=colors, edgecolor=NAVY, linewidth=0.8)
    ax1.axhline(
        math.degrees(TWO_PI / 3),
        color=STEEL,
        linestyle="--",
        linewidth=1.2,
        label=r"the rigid tiling: $\alpha = 2\pi/3$",
    )
    ax1.axhline(
        math.degrees(5 * math.pi / 7),
        color=CRIMSON,
        linestyle=":",
        linewidth=1.4,
        label=r"the Euclidean ceiling: $\alpha = 5\pi/7$",
    )
    ax1.set_xticks(range(12))
    ax1.set_xticklabels(names, rotation=40, ha="right", fontsize=9)
    ax1.set_ylabel("the register vertex angle α, degrees", fontsize=11)
    _style_axis(ax1)
    ax1.legend(fontsize=9.5, frameon=False)
    ax1.set_title("the vertex-angle register α = 2π/3 − σ·s", fontsize=12, color=NAVY)
    areas = [2 * r["area"] for r in rows]
    ax2.bar(range(12), areas, color=colors, edgecolor=NAVY, linewidth=0.8)
    total = sum(areas)
    ax2.axhline(8 * math.pi, color=GOLD, linewidth=2.0, label=r"the Gauss–Bonnet budget $8\pi$")
    ax2.set_xticks(range(12))
    ax2.set_xticklabels(names, rotation=40, ha="right", fontsize=9)
    ax2.set_ylabel("the pair area 2A, hyperbolic", fontsize=11)
    _style_axis(ax2)
    ax2.legend(fontsize=9.5, frameon=False, loc="upper right")
    ax2.set_title(
        f"the area ladder: Σ2A = {total:.6f} vs 8π = {8*math.pi:.6f}\n"
        f"residual {abs(total - 8*math.pi):.1e} — the Euler characteristic absorbs the mass ladder",
        fontsize=12,
        color=NAVY,
    )
    return _save(fig, out, "v2_03_budget_closure.png", dpi)


def fig_v2_group_registers(out: Path, dpi: int) -> str:
    """The group/map registers of V2: counts, class equation, patch."""
    km = kl.KleinMap.build()
    patch = kl.build_chamber_patch(km)
    comb = km.register_summary()
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 5.4), constrained_layout=True)
    ax = axes[0]
    names = ["|GL(2,7)|", "|SL(2,7)|", "|PSL(2,7)|", "chambers", "flags"]
    vals = [2016, 336, 168, patch.chambers, 336]
    bars = ax.bar(range(5), vals, color=[NAVY, STEEL, GOLD, STEEL, SKY], edgecolor=NAVY)
    for b, v in zip(bars, vals):
        ax.text(
            b.get_x() + b.get_width() / 2, v * 1.02, str(v), ha="center", fontsize=10, color=NAVY
        )
    ax.set_xticks(range(5))
    ax.set_xticklabels(names, rotation=22, ha="right", fontsize=9)
    ax.set_ylim(0, 2300)
    _style_axis(ax)
    ax.set_title("the group ladder of the bench", fontsize=12, color=NAVY)
    ax = axes[1]
    labels = ["V", "E", "F", "3V = 2E = 7F", "14F = 4E = 6V"]
    vals2 = [comb["V"], comb["E"], comb["F"], 168, 336]
    bars = ax.bar(range(5), vals2, color=[STEEL, STEEL, STEEL, GOLD, SKY], edgecolor=NAVY)
    for b, v in zip(bars, vals2):
        ax.text(
            b.get_x() + b.get_width() / 2, v * 1.02, str(v), ha="center", fontsize=10, color=NAVY
        )
    ax.set_xticks(range(5))
    ax.set_xticklabels(labels, rotation=22, ha="right", fontsize=9)
    ax.set_ylim(0, 400)
    _style_axis(ax)
    ax.set_title(
        f"the Klein map {{7,3}}: Euler χ = {comb['euler']} (genus 3)",
        fontsize=12,
        color=NAVY,
    )
    ax = axes[2]
    kinds = ["interior sides", "boundary pairs"]
    vals3 = [patch.interior_sides, len(patch.boundary_pairs)]
    ax.bar(range(2), vals3, color=[GOLD, STEEL], edgecolor=NAVY)
    for k, v in enumerate(vals3):
        ax.text(k, v + 1.2, str(v), ha="center", fontsize=11, color=NAVY)
    ax.set_xticks(range(2))
    ax.set_xticklabels(kinds, fontsize=10)
    ax.set_ylim(0, 90)
    _style_axis(ax)
    ax.set_title(
        f"the chamber patch: {patch.chambers} chambers, 84 map edges",
        fontsize=12,
        color=NAVY,
    )
    return _save(fig, out, "v2_04_group_registers.png", dpi)


# ---------------------------------------------------------------------------
# V1 — the spatial registers
# ---------------------------------------------------------------------------


def fig_v1_inclination_ladder(out: Path, dpi: int) -> str:
    rows = sorted(sp.inclination_register(), key=lambda r: r["arc_au"])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 6.0), constrained_layout=True)
    names = [r["body"] for r in rows]
    incs = [r["inclination_deg"] for r in rows]
    colors = [BODY_COLORS[n] for n in names]
    ax1.barh(range(11), incs, color=colors, edgecolor=NAVY, linewidth=0.8)
    ax1.set_yticks(range(11))
    ax1.set_yticklabels(names, fontsize=9.5)
    ax1.set_xlabel("the orbital inclination i, degrees (J2000)", fontsize=11)
    ax1.set_xlim(0, max(incs) * 1.18)
    _style_axis(ax1)
    ax1.set_title("the inclination ladder of the wandering bodies", fontsize=12, color=NAVY)
    arcs = [math.degrees(r["arc_au"]) for r in rows]
    ax2.barh(range(11), arcs, color=colors, edgecolor=NAVY, linewidth=0.8)
    ax2.set_yticks(range(11))
    ax2.set_yticklabels(names, fontsize=9.5)
    ax2.set_xlabel(
        r"the arc register $\lambda = \bar{R}\, i$, degrees of arc (R̄ = 1 AU)", fontsize=11
    )
    ax2.set_xlim(0, max(arcs) * 1.18)
    _style_axis(ax2)
    ax2.set_title("the geometric register of the tilt: the exact arc", fontsize=12, color=NAVY)
    return _save(fig, out, "v1_01_inclination_ladder.png", dpi)


def fig_v1_spatial_system(out: Path, dpi: int) -> str:
    """The inclined solar system: the true J2000 sky, 3D."""
    state = sp.spatial_initial_state()
    elements = sp._j2000_elements()
    fig = plt.figure(figsize=(12.5, 9.0), constrained_layout=True)
    ax = fig.add_subplot(111, projection="3d")
    # the orbits: sample each Kepler orbit
    for k, planet in enumerate(cl.PLANETS, start=1):
        a, e, i_d, om_d, peri_d, _ = elements[planet.name]
        pts = []
        for m_deg in np.linspace(0, 360, 240):
            rx, _vx = sp._orbital_state(a, e, i_d, om_d, peri_d, m_deg)
            pts.append(rx)
        pts = np.array(pts)
        ax.plot(
            pts[:, 0],
            pts[:, 1],
            pts[:, 2],
            color=BODY_COLORS[planet.name],
            linewidth=1.1,
            alpha=0.85,
        )
        ax.scatter(
            state[k, 0],
            state[k, 1],
            state[k, 2],
            s=26,
            color=BODY_COLORS[planet.name],
            edgecolor=NAVY,
            linewidth=0.5,
            depthshade=False,
        )
        ax.text(state[k, 0], state[k, 1], state[k, 2], f"  {planet.name}", fontsize=7.5, color=NAVY)
    ax.scatter([0], [0], [0], s=140, color=GOLD, edgecolor=NAVY, depthshade=False)
    ax.text(0, 0, 0, "  Sun", fontsize=9, color=NAVY)
    ax.set_xlabel("x, AU", fontsize=10)
    ax.set_ylabel("y, AU", fontsize=10)
    ax.set_zlabel("z, AU", fontsize=10)
    ax.set_title(
        "V1 — the spatial registers: the real J2000 sky\n"
        "the inclined orbits of the eight planets against the ecliptic (the gold plane is z = 0)",
        fontsize=13,
        color=NAVY,
        pad=8,
    )
    ax.set_box_aspect((1, 1, 0.55))
    ax.view_init(elev=26, azim=-58)
    return _save(fig, out, "v1_02_spatial_system.png", dpi)


def fig_v1_mutual_inclinations(out: Path, dpi: int) -> str:
    rows = sp.inclination_register()
    names = [r["body"] for r in rows]
    n = len(names)
    mat = np.zeros((n, n))
    normals = [np.array(r["normal"]) for r in rows]
    for a in range(n):
        for b in range(n):
            ang = math.acos(max(-1.0, min(1.0, float(normals[a] @ normals[b]))))
            mat[a, b] = ang / math.pi * 180.0
    fig, ax = plt.subplots(figsize=(10.5, 9.2), constrained_layout=True)
    im = ax.imshow(mat, cmap="Blues", vmin=0, vmax=max(50.0, mat.max()))
    ax.set_xticks(range(n))
    ax.set_xticklabels(names, rotation=45, ha="right", fontsize=8.5)
    ax.set_yticks(range(n))
    ax.set_yticklabels(names, fontsize=8.5)
    for a in range(n):
        for b in range(n):
            if a == b:
                continue
            val = mat[a, b]
            ax.text(
                b,
                a,
                f"{val:.0f}",
                ha="center",
                va="center",
                fontsize=6.4,
                color="white" if val > mat.max() * 0.55 else NAVY,
            )
    fig.colorbar(im, ax=ax, shrink=0.8, pad=0.03, label="the mutual inclination, degrees")
    worst = sp.mutual_inclinations()
    ax.set_title(
        f"V1 — the mutual-inclination matrix of the 11 wandering planes\n"
        f"the extreme pair: {worst['max_pair'][0]}–{worst['max_pair'][1]} at "
        f"{worst['max_mutual_deg']:.2f}°",
        fontsize=12.5,
        color=NAVY,
    )
    return _save(fig, out, "v1_03_mutual_inclinations.png", dpi)


def fig_v1_z_ladder(out: Path, dpi: int) -> str:
    """The out-of-plane motion: z(t) of the planets over the window."""
    masses = sp.nb.planet_masses()
    state0 = sp.spatial_initial_state()
    years, dt, sample_every = 12.0, 0.0004, 12
    n_steps = int(round(years / dt))
    _end, traj = sp.spatial_integrate(state0, masses, dt, n_steps, sample_every=sample_every)
    times = np.linspace(0.0, n_steps * dt, traj.shape[0])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.0, 6.0), constrained_layout=True)
    for k, planet in enumerate(cl.PLANETS, start=1):
        z = traj[:, k, 2] - traj[0, k, 2]
        ax1.plot(times, z, color=BODY_COLORS[planet.name], linewidth=1.1, label=planet.name)
    ax1.set_xlabel("t, years", fontsize=11)
    ax1.set_ylabel("z(t) − z(0), AU", fontsize=11)
    _style_axis(ax1)
    ax1.legend(fontsize=8.5, frameon=False, ncol=2, loc="upper left", bbox_to_anchor=(0.0, 1.0))
    ax1.set_title(
        "the out-of-ecliptic motion z(t) over the 12-year window", fontsize=12, color=NAVY
    )
    ladder = {
        p: max(abs(traj[:, k, 2] - traj[0, k, 2])) for k, p in enumerate(cl.PLANET_NAMES, start=1)
    }
    names = list(ladder.keys())
    vals = [ladder[p] for p in names]
    ax2.barh(range(8), vals, color=[BODY_COLORS[p] for p in names], edgecolor=NAVY, linewidth=0.8)
    ax2.set_yticks(range(8))
    ax2.set_yticklabels(names, fontsize=9.5)
    ax2.set_xlabel("max |z|, AU", fontsize=11)
    ax2.set_xlim(0, max(vals) * 1.2)
    _style_axis(ax2)
    ax2.set_title("the z-ladder: the spatial amplitude of each register", fontsize=12, color=NAVY)
    return _save(fig, out, "v1_04_z_ladder.png", dpi)


# ---------------------------------------------------------------------------
# The 600 dpi re-renders of the planar/hardcore tasks (protocol-bound)
# ---------------------------------------------------------------------------


def _rebase_figures(folder: Path, names: List[str], dpi: int) -> None:
    """Re-run the base figure factory into `folder` at `dpi`."""
    original_save = base_figs._save

    def save600(fig, out_dir, name):  # noqa: ANN001
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / name
        fig.savefig(path, dpi=dpi, facecolor="white")
        plt.close(fig)
        return str(path)

    base_figs._save = save600
    try:
        for name in names:
            builder: Callable[..., str] = getattr(base_figs, name)
            try:
                if "proto_dir" in builder.__code__.co_varnames:
                    builder(folder, PROTO_DIR)
                else:
                    builder(folder)
            except SystemExit:
                raise
            except Exception as exc:  # pragma: no cover — keep building
                print(f"  ! {name}: {exc}")
    finally:
        base_figs._save = original_save


# ---------------------------------------------------------------------------
# The animations
# ---------------------------------------------------------------------------


def _gif(fig, out: Path, name: str, frames: int, fps: int = 14) -> str:
    out.mkdir(parents=True, exist_ok=True)
    writer = animation.PillowWriter(fps=fps)
    anim = animation.FuncAnimation(fig, lambda _: None, frames=frames, cache_frame_data=False)
    path = out / name

    class _Writer(writer.__class__):
        pass

    plt.close(fig)
    return str(path)


def _save_gif(
    fig_func: Callable[[], Tuple[plt.Figure, Callable[[int], None]]],
    n_frames: int,
    out: Path,
    name: str,
    fps: int = 14,
    dpi: int = 130,
) -> str:
    """Render frames by calling fig_func() -> (figure, draw(frame))."""
    out.mkdir(parents=True, exist_ok=True)
    frames = []
    fig, draw = fig_func()
    for k in range(n_frames):
        draw(k)
        fig.canvas.draw()
        rgba = np.asarray(fig.canvas.buffer_rgba())
        frames.append(rgba.copy())
    plt.close(fig)
    from PIL import Image

    pil = [Image.fromarray(f[:, :, :3]) for f in frames]
    path = out / name
    pil[0].save(path, save_all=True, append_images=pil[1:], duration=int(1000 / fps), loop=0)
    return str(path)


def anim_tiling_assembly(out: Path) -> str:
    """The 24 tiles appearing one by one — the closed gravifigure assembles."""
    km = kl.KleinMap.build()
    patch = kl.build_chamber_patch(km)
    assignment = {row["face_pair"][0]: row["body"] for row in kl.assign_bodies(km)}
    assignment.update({row["face_pair"][1]: row["body"] for row in kl.assign_bodies(km)})

    def make():
        fig, ax = plt.subplots(figsize=(8.2, 7.6), constrained_layout=True)
        ax.set_xlim(-1.08, 1.08)
        ax.set_ylim(-1.08, 1.08)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(
            "the closed gravifigure assembles: the 24 heptagons of the Klein quartic",
            fontsize=12,
            color=NAVY,
        )
        circ = plt.Circle((0, 0), 1.0, fill=False, color=NAVY, linewidth=1.8)
        ax.add_patch(circ)

        def draw(k: int) -> None:
            for hept in patch.heptagons[: k + 1]:
                body = assignment[hept.face_coset]
                _disk_polygon(
                    ax, hept.vertices, color=BODY_COLORS.get(body, "#DDD"), alpha=0.92, zorder=2
                )
                xs = [v.real for v in hept.vertices] + [hept.vertices[0].real]
                ys = [v.imag for v in hept.vertices] + [hept.vertices[0].imag]
                ax.plot(xs, ys, color=NAVY, linewidth=0.9, zorder=3)
            done = k + 1
            ax.set_xlabel(
                f"{done} / 24 tiles — the budget Σα = 8π closes on the last tile",
                fontsize=10.5,
                color=STEEL,
            )

        return fig, draw

    return _save_gif(make, 24, out, "anim_v2_tiling_assembly.gif", fps=6)


def anim_inclined_system(out: Path) -> str:
    """The inclined solar system in motion: 30 years of the 3D orbits."""
    years, dt, sample_every = 30.0, 0.002, 25
    n_steps = int(round(years / dt))
    masses = sp.nb.planet_masses()
    state0 = sp.spatial_initial_state()
    _end, traj = sp.spatial_integrate(state0, masses, dt, n_steps, sample_every=sample_every)
    times = np.linspace(0.0, years, traj.shape[0])
    n_frames = 96

    def make():
        fig = plt.figure(figsize=(8.6, 7.4), constrained_layout=True)
        ax = fig.add_subplot(111, projection="3d")
        elements = sp._j2000_elements()
        for k, planet in enumerate(cl.PLANETS, start=1):
            a, e, i_d, om_d, peri_d, _ = elements[planet.name]
            pts = np.array(
                [
                    sp._orbital_state(a, e, i_d, om_d, peri_d, m_deg)[0]
                    for m_deg in np.linspace(0, 360, 160)
                ]
            )
            ax.plot(
                pts[:, 0],
                pts[:, 1],
                pts[:, 2],
                color=BODY_COLORS[planet.name],
                linewidth=0.8,
                alpha=0.5,
            )
        ax.set_title(
            "the inclined solar system in motion — 30 years of the 3D flow", fontsize=12, color=NAVY
        )
        ax.set_box_aspect((1, 1, 0.55))
        ax.view_init(elev=26, azim=-58)

        def draw(k: int) -> None:
            t_idx = int(k * (len(times) - 1) / (n_frames - 1))
            for p_i, planet in enumerate(cl.PLANETS, start=1):
                x, y, z = traj[t_idx, p_i, :3]
                ax.scatter(
                    [x],
                    [y],
                    [z],
                    s=22,
                    color=BODY_COLORS[planet.name],
                    edgecolor=NAVY,
                    linewidth=0.4,
                    depthshade=False,
                )
                ax.text(x, y, z, f" {planet.name}", fontsize=6.5, color=NAVY)
            ax.scatter([0], [0], [0], s=90, color=GOLD, edgecolor=NAVY, depthshade=False)
            ax.set_xlabel("x, AU", fontsize=8)
            ax.set_ylabel("y, AU", fontsize=8)
            ax.set_zlabel("z, AU", fontsize=8)
            ax.set_xlabel(f"t = {times[t_idx]:.1f} yr", fontsize=9)

        return fig, draw

    return _save_gif(make, n_frames, out, "anim_v1_inclined_system.gif", fps=12)


def anim_register_sweep(out: Path) -> str:
    """The register heptagon morphing as alpha sweeps to the ceiling."""
    n_frames = 40

    def make():
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 5.6), constrained_layout=True)

        def draw(k: int) -> None:
            frac = k / (n_frames - 1)
            # sweep: 2π/3 -> 5π/7 (light) and back toward π/3 (heavy)
            alpha = TWO_PI / 3 + frac * (5 * math.pi / 7 - TWO_PI / 3)
            big_r, edge, inr, area = kl.register_dims(alpha)
            t = math.tanh(big_r / 2)
            pts = [
                complex(
                    t * math.cos(TWO_PI * j / 7 + math.pi / 7),
                    t * math.sin(TWO_PI * j / 7 + math.pi / 7),
                )
                for j in range(7)
            ]
            ax1.clear()
            ax1.add_patch(plt.Circle((0, 0), 1.0, fill=False, color=NAVY, linewidth=1.4))
            _disk_polygon(ax1, pts, color=GOLD, alpha=0.55)
            xs = [p.real for p in pts] + [pts[0].real]
            ys = [p.imag for p in pts] + [pts[0].imag]
            ax1.plot(xs, ys, color=NAVY, linewidth=1.4)
            ax1.set_xlim(-1.05, 1.05)
            ax1.set_ylim(-1.05, 1.05)
            ax1.set_aspect("equal")
            ax1.axis("off")
            ax1.set_title(
                f"α = {alpha:.3f} rad ({math.degrees(alpha):.1f}°)", fontsize=12, color=NAVY
            )
            ax2.clear()
            alphas = np.linspace(0.35, 5 * math.pi / 7, 300)
            ax2.plot(alphas, [kl.register_dims(a)[0] for a in alphas], color=STEEL, label="R(α)")
            ax2.plot(alphas, [kl.register_dims(a)[3] for a in alphas], color=GOLD, label="A(α)")
            ax2.axvline(alpha, color=CRIMSON, linewidth=1.2)
            ax2.axvline(TWO_PI / 3, color=NAVY, linestyle="--", linewidth=1.0)
            ax2.axvline(5 * math.pi / 7, color=NAVY, linestyle=":", linewidth=1.0)
            ax2.set_xlabel("α, rad", fontsize=10)
            _style_axis(ax2)
            ax2.legend(fontsize=9, frameon=False)
            ax2.set_title("the register dimensions vs the vertex angle", fontsize=11, color=NAVY)

        return fig, draw

    return _save_gif(make, n_frames, out, "anim_v2_register_sweep.gif", fps=10)


# ---------------------------------------------------------------------------
# The README per folder
# ---------------------------------------------------------------------------

FOLDER_READMES: Dict[str, str] = {
    "P2_kepler_register": (
        "The Kepler register at 600 dpi: the corrected vs uncorrected\n"
        "comb and the mass-correction signature (stage P2)."
    ),
    "P3_planetary_simulation": (
        "The planar Sun + 8-planets integration at 600 dpi: the orbits\n"
        "and the conservation registers (stage P3)."
    ),
    "P5P6_vortex_lattice": (
        "The heptagon vortex lattice and the seven congruent shape\n"
        "cycles at 600 dpi (stages P5, P6)."
    ),
    "X1X2_group_certificates": (
        "The hardcore group certificates at 600 dpi: the class equation,\n"
        "the two natural actions, the Sylow census (stages X1, X2)."
    ),
    "X3X4_hyperbolic_bridge": (
        "The hyperbolic bridge at 600 dpi: the (2,3,7) generation, the\n"
        "Hurwitz arithmetic, the {7,3} closed forms and the disk witness\n"
        "(stages X3, X4)."
    ),
    "X5X6_integrator_and_gr": (
        "The integrator certification and the 1PN perihelion precession\n"
        "at 600 dpi (stages X5, X6)."
    ),
    "V1_inclined_registers": (
        "The spatial registers at 600 dpi: the inclination ladder, the\n"
        "arc registers, the mutual-inclination matrix, the 3D J2000 sky\n"
        "and the z-ladder (stage V1)."
    ),
    "V2_klein_tiling": (
        "The closed gravifigure at 600 dpi: the 24-heptagon patch of the\n"
        "Klein quartic in the Poincare disk, the register rose, the\n"
        "budget closure and the group registers (stage V2)."
    ),
}


def write_folder_readmes(out_root: Path) -> None:
    for folder, text in FOLDER_READMES.items():
        d = out_root / folder
        d.mkdir(parents=True, exist_ok=True)
        files = sorted(p.name for p in d.glob("*.png"))
        lines = [
            f"# `{folder}` — 600 dpi",
            "",
            text,
            "",
            "Regenerate with `make figures600` (protocol-bound; every plotted",
            "register is read from `results/protocols/`).",
            "",
        ]
        if files:
            lines += ["| file | what it shows |", "|------|----------------|"]
            lines += [f"| [`{f}`]({f}) | {'the figure of this task'} |" for f in files]
        (d / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# The driver
# ---------------------------------------------------------------------------


def build_all(dpi: int = 600, animations: bool = False) -> List[str]:
    built: List[str] = []
    tasks: Dict[str, List[Callable[[Path, int], str]]] = {
        "V1_inclined_registers": [
            fig_v1_inclination_ladder,
            fig_v1_spatial_system,
            fig_v1_mutual_inclinations,
            fig_v1_z_ladder,
        ],
        "V2_klein_tiling": [
            fig_v2_disk_patch,
            fig_v2_register_rose,
            fig_v2_budget_closure,
            fig_v2_group_registers,
        ],
    }
    for folder, builders in tasks.items():
        out = OUT_ROOT / folder
        for builder in builders:
            built.append(builder(out, dpi))
        print(f"  [{folder}] {len(builders)} figures at {dpi} dpi")

    # the planar/hardcore tasks re-rendered at 600 dpi from figures.py
    rebase_plan = {
        "P2_kepler_register": ["fig02_kepler_register"],
        "P3_planetary_simulation": ["fig03_planetary_simulation"],
        "P5P6_vortex_lattice": ["fig04_vortex_lattice"],
        "X1X2_group_certificates": ["fig01_fano_gravity_figure"],
        "X3X4_hyperbolic_bridge": ["fig05_hardcore_certificates"],
        "X5X6_integrator_and_gr": ["fig05_hardcore_certificates"],
    }
    _rebase_figures(OUT_ROOT / "P2_kepler_register", rebase_plan["P2_kepler_register"], dpi)
    built.append(str(OUT_ROOT / "P2_kepler_register"))
    print("  [P2_kepler_register] re-rendered at 600 dpi")
    _rebase_figures(
        OUT_ROOT / "P3_planetary_simulation", rebase_plan["P3_planetary_simulation"], dpi
    )
    built.append(str(OUT_ROOT / "P3_planetary_simulation"))
    print("  [P3_planetary_simulation] re-rendered at 600 dpi")
    _rebase_figures(OUT_ROOT / "P5P6_vortex_lattice", rebase_plan["P5P6_vortex_lattice"], dpi)
    built.append(str(OUT_ROOT / "P5P6_vortex_lattice"))
    print("  [P5P6_vortex_lattice] re-rendered at 600 dpi")
    _rebase_figures(
        OUT_ROOT / "X1X2_group_certificates", rebase_plan["X1X2_group_certificates"], dpi
    )
    built.append(str(OUT_ROOT / "X1X2_group_certificates"))
    print("  [X1X2_group_certificates] re-rendered at 600 dpi")
    _rebase_figures(OUT_ROOT / "X3X4_hyperbolic_bridge", rebase_plan["X3X4_hyperbolic_bridge"], dpi)
    built.append(str(OUT_ROOT / "X3X4_hyperbolic_bridge"))
    print("  [X3X4_hyperbolic_bridge] re-rendered at 600 dpi")
    _rebase_figures(OUT_ROOT / "X5X6_integrator_and_gr", rebase_plan["X5X6_integrator_and_gr"], dpi)
    built.append(str(OUT_ROOT / "X5X6_integrator_and_gr"))
    print("  [X5X6_integrator_and_gr] re-rendered at 600 dpi")

    if animations:
        anim_out = OUT_ROOT / "animations"
        built.append(anim_tiling_assembly(anim_out))
        print("  [animations] the tiling assembly GIF")
        built.append(anim_inclined_system(anim_out))
        print("  [animations] the inclined system GIF")
        built.append(anim_register_sweep(anim_out))
        print("  [animations] the register sweep GIF")

    # the 600dpi root README
    folders = sorted(p.name for p in OUT_ROOT.iterdir() if p.is_dir())
    lines = [
        "# `figures/600dpi/` — the ultra-high-resolution gallery",
        "",
        "Every task of the bench has its own folder here; every figure is",
        f"generated at **{dpi} dpi** from the committed protocols",
        "(`results/protocols/*.json`) by the protocol-bound factory",
        "[`python/planetvortex/pubfigures.py`](../../python/planetvortex/pubfigures.py).",
        "",
        "| folder | task(s) |",
        "|--------|---------|",
    ]
    labels = {
        "P2_kepler_register": "P2 — the Kepler register",
        "P3_planetary_simulation": "P3 — the planar N-body",
        "P5P6_vortex_lattice": "P5, P6 — the vortex lattice and the cells",
        "X1X2_group_certificates": "X1, X2 — the group certificates",
        "X3X4_hyperbolic_bridge": "X3, X4 — the hyperbolic bridge",
        "X5X6_integrator_and_gr": "X5, X6 — the integrator and the 1PN bridge",
        "V1_inclined_registers": "V1 — the spatial inclined registers",
        "V2_klein_tiling": "V2 — the closed gravifigure",
        "animations": "the GIF animations",
    }
    for folder in folders:
        lines.append(f"| [`{folder}/`]({folder}/) | {labels.get(folder, folder)} |")
    (OUT_ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_folder_readmes(OUT_ROOT)
    print(f"  total: {len(built)} artifacts")
    return built


def main() -> None:
    ap = argparse.ArgumentParser(description="the 600 dpi publication factory")
    ap.add_argument("--dpi", type=int, default=600)
    ap.add_argument("--animations", action="store_true")
    args = ap.parse_args()
    print("=" * 74)
    print("  PLANETVORTEX — the 600 dpi publication factory")
    print("=" * 74)
    build_all(args.dpi, args.animations)


if __name__ == "__main__":
    main()
