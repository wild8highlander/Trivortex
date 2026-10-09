#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
PLANETVORTEX — THE FIGURE FACTORY (300 dpi PNG + the scheme SVG)
============================================================================
Generates the publication figures of the mini-repository from the committed
JSON protocols in `results/protocols/` — the same "bound to a run"
discipline as the monograph: every plotted register is read from a
protocol file, never re-invented. The trajectory panels (the planetary
orbits, the ring trails, the shape cycles) are recomputed from the model
modules, which is by design: they are pictures of solutions, not
registers.

    make figures                       # from the mini-repository root
    python3 -m planetvortex.figures   # equivalent, PYTHONPATH=python

Outputs into `planetvortex/figures/`:

    fig01_fano_gravity_figure.png    the gravity figure + the exact cell
    fig02_kepler_register.png        P2: Kepler III, corrected/uncorrected
    fig03_planetary_simulation.png   P3: the integrated solar system
    fig04_vortex_lattice.png         P5/P6: the ring + the seven cycles
    fig05_hardcore_certificates.png  X1/X5/X6: the hardcore certificates
    scheme_planetvortex.svg          the mini-repository architecture

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

from . import classical as cl  # noqa: E402
from . import fano as fn  # noqa: E402
from . import model as md  # noqa: E402
from . import nbody as nb  # noqa: E402
from .ladder import _cell_rhs_batch, _shape_descriptor_batch  # noqa: E402

TWO_PI = 2.0 * math.pi

# The mini-repository palette (matches the parent TRIVORTEX brand)
NAVY = "#0A1A3A"
STEEL = "#2E5FA3"
SKY = "#7FA6D9"
CRIMSON = "#B03A2E"
GREEN = "#1E8449"
LIGHT = "#F4F6FA"
GRID = "#D5DCE8"

PACKAGE_DIR = Path(__file__).resolve().parent
MINIROOT = PACKAGE_DIR.parents[1]
DEFAULT_PROTOS = MINIROOT / "results" / "protocols"
DEFAULT_OUT = MINIROOT / "figures"


def _proto(stage: str, proto_dir: Path) -> Dict:
    """Load a committed P-protocol JSON (the figure's numeric oracle)."""
    path = proto_dir / f"{stage}_default.json"
    if not path.exists():
        raise SystemExit(
            f"missing protocol {path} — run `make ladder` first "
            "(the figures are bound to the committed protocols)"
        )
    with path.open("r", encoding="utf-8") as fh:
        data: Dict = json.load(fh)
    return data


def _style_axis(ax: plt.Axes) -> None:
    """The common look: navy spines, soft grid, tick direction in."""
    for spine in ax.spines.values():
        spine.set_color(NAVY)
        spine.set_linewidth(0.8)
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.tick_params(colors=NAVY, labelsize=9, direction="in")
    ax.set_axisbelow(True)


def _save(fig: plt.Figure, out_dir: Path, name: str) -> str:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / name
    fig.savefig(path, dpi=300)
    plt.close(fig)
    return str(path)


# ---------------------------------------------------------------------------
# fig01 — the gravity figure and the exact line-triangle (Theorem A)
# ---------------------------------------------------------------------------


def fig01_fano_gravity_figure(out_dir: Path) -> str:
    """(a) THE FIGURE: the heptagon of the seven wandering planets with
    the Sun at the centre and the seven Fano lines drawn — one chord of
    each class per line. (b) the exact line-triangle: angles
    (pi/7, 2pi/7, 4pi/7), sides s1, s2, s3, area sqrt(7)/4."""
    fig, (axf, axt) = plt.subplots(1, 2, figsize=(10.4, 4.8), constrained_layout=True)

    xy = fn.heptagon_coordinates(1.0)
    ladder_delta = cl.gravity_ladder()
    # (a) the seven Fano lines, colored by their chord class
    for line in fn.fano_lines():
        pts = xy[list(line)]
        for a, b, color in ((0, 1, STEEL), (1, 2, SKY), (2, 0, CRIMSON)):
            pa, pb = pts[a], pts[b]
            axf.plot([pa[0], pb[0]], [pa[1], pb[1]], color=color, lw=1.3, alpha=0.85)
    circ = np.linspace(0.0, TWO_PI, 400)
    axf.plot(np.cos(circ), np.sin(circ), color=GRID, lw=0.8)
    axf.plot([0.0], [0.0], "o", color=NAVY, ms=14, mec=CRIMSON, mew=1.2, zorder=6)
    axf.text(0.0, -0.13, "Sun", ha="center", fontsize=9, color=NAVY, fontweight="bold")
    for i, name in enumerate(fn.STATION_NAMES):
        axf.plot(xy[i, 0], xy[i, 1], "o", color=STEEL, ms=8, mec=NAVY, mew=0.8, zorder=5)
        r_label = 1.22
        axf.text(
            r_label * xy[i, 0],
            r_label * xy[i, 1],
            f"{name}\n({ladder_delta[name]:+.2f} dex)",
            ha="center",
            va="center",
            fontsize=7.6,
            color=NAVY,
        )
    axf.set_xlim(-1.65, 1.65)
    axf.set_ylim(-1.6, 1.6)
    axf.set_aspect("equal")
    axf.set_title(
        "(a) the gravity figure: PSL(2,7) on the heptagon (R = 1 AU)",
        fontsize=10.5,
        color=NAVY,
    )
    axf.text(
        0.02,
        0.02,
        "lines {i, i+1, i+3}: one chord of each class;\n"
        "vertex labels: log$_{10}$(GM/GM$_\\oplus$) — the gravity ladder",
        transform=axf.transAxes,
        fontsize=7.6,
        color=NAVY,
        va="bottom",
    )
    axf.set_xlabel("x [AU]")
    axf.set_ylabel("y [AU]")

    # (b) the exact line-triangle of the figure
    line0 = fn.fano_lines()[0]
    geom = fn.line_triangle_geometry(line0, 1.0)
    pts = fn.heptagon_coordinates(1.0)[list(line0)]
    tri = plt.Polygon(pts, closed=True, facecolor=LIGHT, edgecolor=NAVY, lw=1.2)
    axt.add_patch(tri)
    axt.plot(fn.heptagon_coordinates(1.0)[:, 0], fn.heptagon_coordinates(1.0)[:, 1], "o")
    circ2 = np.linspace(0.0, TWO_PI, 400)
    axt.plot(np.cos(circ2), np.sin(circ2), color=GRID, lw=0.8)
    for i, (px, py) in enumerate(pts):
        axt.plot(px, py, "o", color=STEEL, ms=9, mec=NAVY, mew=0.8, zorder=5)
    # angle annotations: at each vertex, pulled slightly toward the centroid
    centroid = pts.mean(axis=0)
    labels_ang = [r"$\pi/7$", r"$2\pi/7$", r"$4\pi/7$"]
    for i in range(3):
        pos = pts[i] + 0.16 * (centroid - pts[i])
        axt.text(
            pos[0], pos[1], labels_ang[i], ha="center", va="center", fontsize=8.5, color=CRIMSON
        )
    axt.text(
        centroid[0],
        centroid[1] - 0.02,
        r"$\Delta=\frac{\sqrt{7}}{4}R^2$",
        ha="center",
        va="center",
        fontsize=10,
        color=NAVY,
    )
    s1, s2, s3 = fn.chord_classes(1.0)
    axt.set_title(
        "(b) every line is this triangle (R = 1): "
        + f"$s_1$={s1:.4f}, $s_2$={s2:.4f}, $s_3$={s3:.4f}",
        fontsize=10.5,
        color=NAVY,
    )
    axt.set_aspect("equal")
    axt.set_xlabel("x [R]")
    axt.set_ylabel("y [R]")

    for ax in (axf, axt):
        _style_axis(ax)
    return _save(fig, out_dir, "fig01_fano_gravity_figure.png")


# ---------------------------------------------------------------------------
# fig02 — P2: the Kepler register
# ---------------------------------------------------------------------------


def fig02_kepler_register(out_dir: Path, proto_dir: Path) -> str:
    """(a) the Kepler comb T vs a with the 3/2 slope; (b) the three
    registers per planet: corrected, uncorrected, fact-sheet."""
    data = _proto("P2_kepler_register", proto_dir)["check"]
    rows = data["per_planet"]
    names = [r["planet"] for r in rows]
    a_vals = [r["a_au"] for r in rows]
    t_vals = [r["T_kepler_corrected_years"] for r in rows]
    dev_corr = [max(r["deviation_corrected_relative"], 1e-17) for r in rows]
    dev_uncorr = [r["deviation_uncorrected_relative"] for r in rows]
    dev_sheet = [max(r["factsheet_deviation_relative"], 1e-17) for r in rows]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.2), constrained_layout=True)

    a_fine = np.linspace(0.35, 33.0, 300)
    ax1.loglog(a_fine, a_fine**1.5, color=STEEL, lw=1.6, label=r"$T=a^{3/2}$ (Kepler III)")
    ax1.loglog(a_vals, t_vals, "o", color=CRIMSON, ms=7, mec=NAVY, mew=0.8, label="8 planets")
    for name, a, t in zip(names, a_vals, t_vals):
        if name in ("Mercury", "Earth", "Jupiter", "Neptune"):
            ax1.annotate(name, (a, t), textcoords="offset points", xytext=(6, -3), fontsize=8)
    ax1.set_title("(a) the Kepler comb of the committed register", fontsize=10.5, color=NAVY)
    ax1.set_xlabel("a [AU]")
    ax1.set_ylabel("T [Julian years]")
    ax1.legend(fontsize=8, framealpha=0.9, edgecolor=GRID, loc="upper left")

    xs = np.arange(8)
    ax2.semilogy(
        xs, dev_corr, "o", color=GREEN, ms=7, mec=NAVY, mew=0.7, label="corrected (register)"
    )
    ax2.semilogy(
        xs,
        dev_uncorr,
        "s",
        color=CRIMSON,
        ms=7,
        mec=NAVY,
        mew=0.7,
        label="uncorrected (misses $m/2M_\\odot$)",
    )
    ax2.semilogy(
        xs,
        dev_sheet,
        "^",
        color=SKY,
        ms=7,
        mec=NAVY,
        mew=0.7,
        label="fact-sheet periods (provenance)",
    )
    worst = data["worst_deviation_corrected"]
    ax2.axhline(worst * 3, color=GREEN, ls=":", lw=1.1)
    ax2.text(
        0.1,
        worst * 6,
        f"registered worst {worst:.1e}",
        fontsize=8,
        color=GREEN,
    )
    ax2.set_xticks(xs)
    ax2.set_xticklabels(names, rotation=30, fontsize=7.5)
    ax2.set_title(
        "(b) |T$_{meas}$ - T$_{analytic}$|/T: the mass correction is physical",
        fontsize=10.5,
        color=NAVY,
    )
    ax2.set_ylabel("relative deviation")
    ax2.legend(fontsize=7.8, framealpha=0.9, edgecolor=GRID, loc="center right")

    for ax in (ax1, ax2):
        _style_axis(ax)
    return _save(fig, out_dir, "fig02_kepler_register.png")


# ---------------------------------------------------------------------------
# fig03 — P3: the planetary simulation
# ---------------------------------------------------------------------------


def fig03_planetary_simulation(out_dir: Path, proto_dir: Path) -> str:
    """(a) the integrated inner system (Sun + 4 rocky planets);
    (b) the integrated outer system; the conservation registers are
    quoted in the panel titles from the committed protocol."""
    data = _proto("P3_planetary_nbody", proto_dir)["check"]
    years = float(data["params"]["years"])
    dt = float(data["params"]["dt"])
    sample_every = int(data["params"]["sample_every"])

    masses = nb.planet_masses()
    state0 = nb.initial_state()
    n_steps = int(round(years / dt))
    _, traj = nb.integrate(state0, masses, dt, n_steps, sample_every=sample_every)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.8), constrained_layout=True)
    colors = (STEEL, CRIMSON, GREEN, "#8E44AD")
    for panel, (ax, idxs, title) in enumerate(
        (
            (ax1, (1, 2, 3, 4), "(a) the integrated inner system"),
            (ax2, (5, 6, 7, 8), "(b) the integrated outer system"),
        )
    ):
        ax.plot([0.0], [0.0], "o", color=NAVY, ms=11, mec=CRIMSON, mew=1.1, zorder=6)
        for j, i in enumerate(idxs):
            ax.plot(
                traj[:, i, 0] - traj[:, 0, 0],
                traj[:, i, 1] - traj[:, 0, 1],
                color=colors[j],
                lw=1.0,
                label=cl.PLANETS[i - 1].name,
            )
        ax.plot(0.0, 0.0, "o", color="none")
        ax.set_aspect("equal")
        ax.set_xlabel("x [AU]")
        ax.set_ylabel("y [AU]")
        ax.set_title(title, fontsize=10.5, color=NAVY)
        ax.legend(fontsize=7.5, framealpha=0.9, edgecolor=GRID, loc="upper right")
        if panel == 1:
            ax.set_xlim(-2.0, 2.0)
            ax.set_ylim(-2.0, 2.0)
        else:
            ax.set_xlim(-33.0, 33.0)
            ax.set_ylim(-33.0, 33.0)
        _style_axis(ax)
    e_drift = data["energy_drift_relative"]
    l_drift = data["angular_momentum_drift_relative"]
    fig.suptitle(
        "P3 planetary N-body, "
        + f"{years:.0f} yr — energy drift {e_drift:.1e}, angular-momentum drift {l_drift:.1e}",
        fontsize=9.5,
        color=NAVY,
        y=1.02,
    )
    return _save(fig, out_dir, "fig03_planetary_simulation.png")


# ---------------------------------------------------------------------------
# fig04 — P5/P6: the vortex lattice and the seven shape cycles
# ---------------------------------------------------------------------------


def fig04_vortex_lattice(out_dir: Path, proto_dir: Path) -> str:
    """(a) the heptagon ring over two rigid rotations with one Fano
    triad highlighted; (b) the seven congruent shape cycles d(t) — the
    dynamical shadow of PSL(2,7), with T_shape from the protocol."""
    data6 = _proto("P6_seven_cells", proto_dir)["check"]
    t_shape = float(data6["T_shape_mean"])
    cell_dt = float(data6["params"]["dt"])
    t_max = min(2.6 * t_shape, float(data6["params"]["t_max"]))

    gamma = np.ones(7)
    state0 = md.ring_state(1.0)
    omega7 = fn.ring_omega(1.0, 1.0)
    t_rot = TWO_PI / omega7
    dt = t_rot / 1500.0
    n_steps = int(round(2 * t_rot / dt))
    trail = np.zeros((n_steps + 1, 14))
    cur = state0.copy()
    trail[0] = cur
    for i in range(n_steps):
        cur = md.rk4_step(cur, gamma, dt)
        trail[i + 1] = cur

    # the seven cells, integrated concurrently for the shape cycles
    xy = fn.heptagon_coordinates(1.0)
    cells0 = np.array([xy[list(line)] for line in fn.fano_lines()])
    n_c = int(round(t_max / cell_dt))
    cells = cells0.copy()
    desc_t = [0.0]
    desc_d = [np.zeros(7)]
    d0 = _shape_descriptor_batch(cells0)
    for step in range(1, n_c + 1):
        k1 = _cell_rhs_batch(cells)
        k2 = _cell_rhs_batch(cells + 0.5 * cell_dt * k1)
        k3 = _cell_rhs_batch(cells + 0.5 * cell_dt * k2)
        k4 = _cell_rhs_batch(cells + cell_dt * k3)
        cells = cells + (cell_dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        if step % 6 == 0:
            desc_t.append(step * cell_dt)
            desc_d.append(np.linalg.norm(_shape_descriptor_batch(cells) - d0, axis=1))
    desc_d_arr = np.array(desc_d)  # (S, 7)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.8), constrained_layout=True)

    tri0 = fn.fano_lines()[0]
    tri_pts = xy[list(tri0)]
    poly = plt.Polygon(tri_pts, closed=True, facecolor=LIGHT, edgecolor=CRIMSON, lw=1.1)
    ax1.add_patch(poly)
    for k in range(7):
        ax1.plot(trail[:, 2 * k], trail[:, 2 * k + 1], color=SKY, lw=0.9)
    xy0 = fn.heptagon_coordinates(1.0)
    poly_ring = plt.Polygon(xy0, closed=True, facecolor="none", edgecolor=STEEL, lw=1.2)
    ax1.add_patch(poly_ring)
    ax1.plot(xy0[:, 0], xy0[:, 1], "o", color=STEEL, ms=6, mec=NAVY, mew=0.7)
    for i in tri0:
        ax1.plot(xy0[i, 0], xy0[i, 1], "o", color=CRIMSON, ms=7, mec=NAVY, mew=0.8)
    ax1.set_aspect("equal")
    ax1.set_title(
        "(a) the N=7 lattice: 2 rigid rotations at $\\omega_7=3/2\\pi$", fontsize=10.5, color=NAVY
    )
    ax1.set_xlabel("x [R]")
    ax1.set_ylabel("y [R]")
    ax1.text(
        0.02,
        0.10,
        "crimson: one Fano line-cell {i, i+1, i+3};\nall seven cells ride the ring",
        transform=ax1.transAxes,
        fontsize=7.6,
        color=NAVY,
        va="bottom",
    )

    shades = [STEEL, SKY, GREEN, CRIMSON, NAVY, "#8E44AD", "#B07D2B"]
    for c in range(7):
        ax2.plot(desc_t, desc_d_arr[:, c], color=shades[c], lw=1.0, alpha=0.9)
    ax2.axvline(t_shape, color=CRIMSON, ls="--", lw=1.2)
    ax2.text(
        t_shape * 1.04,
        0.245,
        f"$T_{{shape}}$ = {t_shape:.4f} (all seven, spread 0.0)",
        fontsize=8.5,
        color=CRIMSON,
    )
    ax2.set_xlim(0.0, t_max)
    ax2.set_ylim(0.0, 0.32)
    ax2.set_title(
        "(b) the seven shape cycles $\\|S(t)-S(0)\\|$ — congruent (P6)",
        fontsize=10.5,
        color=NAVY,
    )
    ax2.set_xlabel("time [vortex units]")
    ax2.set_ylabel("shape distance")

    for ax in (ax1, ax2):
        _style_axis(ax)
    return _save(fig, out_dir, "fig04_vortex_lattice.png")


# ---------------------------------------------------------------------------
# fig05 — the hardcore certificates (X1, X5, X6 + the {7,3} witness)
# ---------------------------------------------------------------------------


def fig05_hardcore_certificates(out_dir: Path, proto_dir: Path) -> str:
    """(a) the class equation of PSL(2,7) (X1); (b) the measured
    convergence orders (X5); (c) the 1PN perihelion ladder and the
    measured points (X6); (d) the Poincare-disk {7,3} heptagon whose
    numerically solved angle certifies the closed forms (X4 witness)."""
    x1 = _proto("X1_sl2_enumeration", proto_dir)["check"]
    x5 = _proto("X5_integrator_certification", proto_dir)["check"]
    x6 = _proto("X6_pn_perihelion", proto_dir)["check"]

    fig, axes = plt.subplots(2, 2, figsize=(10.6, 8.2), constrained_layout=True)
    ax_a, ax_b, ax_c, ax_d = axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]

    # (a) the class equation 1 + 21 + 24 + 24 + 42 + 56 = 168
    sizes = x1["conjugacy_class_sizes"]
    bars = ax_a.bar(
        range(len(sizes)),
        sizes,
        color=[NAVY, STEEL, SKY, SKY, CRIMSON, GREEN],
        edgecolor=NAVY,
        linewidth=0.8,
    )
    for rect, s in zip(bars, sizes):
        ax_a.text(
            rect.get_x() + rect.get_width() / 2,
            s + 1.0,
            str(s),
            ha="center",
            fontsize=9,
            color=NAVY,
        )
    ax_a.set_xticks(range(len(sizes)))
    ax_a.set_xticklabels(["1A", "2A", "7A", "7B", "4A", "3A"], fontsize=9)
    ax_a.set_ylim(0, 63)
    ax_a.set_title("(a) the class equation of PSL(2,7) — simple (X1)", fontsize=10, color=NAVY)
    ax_a.set_ylabel("class size")

    # (b) the measured convergence orders
    conv = x5["convergence"]
    leap_dt = [1.0 / k for k in conv["leapfrog_grid"]]
    yosh_dt = [1.0 / k for k in conv["yoshida_grid"]]
    ax_b.loglog(
        leap_dt,
        conv["leapfrog_errors"],
        "o-",
        color=STEEL,
        lw=1.4,
        ms=6,
        label=f"leapfrog, slope {conv['leapfrog_slope']:.3f}",
    )
    ax_b.loglog(
        yosh_dt,
        conv["yoshida_errors"],
        "s-",
        color=CRIMSON,
        lw=1.4,
        ms=6,
        label=f"Yoshida 4, slope {conv['yoshida_slope']:.3f}",
    )
    ax_b.set_title("(b) measured orders 2 and 4 (X5)", fontsize=10, color=NAVY)
    ax_b.set_xlabel("dt [orbital periods]")
    ax_b.set_ylabel("position error")
    ax_b.legend(fontsize=8, framealpha=0.9, edgecolor=GRID, loc="lower right")

    # (c) the precession ladder + the measured points
    ladder_rows = x6["formula_ladder_all_planets"]
    names = [r["planet"] for r in ladder_rows]
    vals = [r["arcsec_per_century"] for r in ladder_rows]
    xs = np.arange(len(names))
    ax_c.bar(
        xs,
        vals,
        color=STEEL,
        edgecolor=NAVY,
        linewidth=0.7,
        alpha=0.85,
        label="closed form",
    )
    first = True
    for row in x6["per_planet"]:
        i = names.index(row["planet"])
        ax_c.plot(
            i,
            row["arcsec_per_century"],
            "o",
            color=CRIMSON,
            ms=9,
            mec=NAVY,
            mew=0.8,
            label="measured 1PN orbit" if first else None,
        )
        first = False
    ax_c.set_yscale("log")
    ax_c.set_ylim(3e-4, 200)
    ax_c.set_xticks(xs)
    ax_c.set_xticklabels(names, rotation=30, fontsize=7.5)
    ax_c.set_title(
        "(c) perihelion precession: Mercury "
        f"{x6['mercury_arcsec_per_century']:.2f}"
        "\u2033/century (X6)",
        fontsize=10,
        color=NAVY,
    )
    ax_c.set_ylabel("arcsec / century")
    ax_c.legend(fontsize=7.5, framealpha=0.9, edgecolor=GRID, loc="lower left")

    # (d) the Poincare-disk heptagon (the X4 witness, recomputed)
    from planetvortex.hardcore import _disk_witness, _hyperbolic_literals

    witness = _disk_witness()
    t = witness["t_vertex"]
    n = 7
    verts = [
        np.array([t * math.cos(TWO_PI * k / n), t * math.sin(TWO_PI * k / n)]) for k in range(n)
    ]
    theta = np.linspace(0, 2 * np.pi, 200)
    ax_d.fill(np.cos(theta), np.sin(theta), color=LIGHT, zorder=0)
    ax_d.plot(np.cos(theta), np.sin(theta), color=NAVY, lw=1.2)
    for k in range(n):
        u, w = verts[k], verts[(k + 1) % n]
        amat = np.array([u, w])
        bvec = np.array([(1 + u @ u) / 2, (1 + w @ w) / 2])
        centre = np.linalg.solve(amat, bvec)
        r = math.sqrt(max(centre @ centre - 1.0, 0.0))
        ang0 = math.atan2(u[1] - centre[1], u[0] - centre[0])
        ang1 = math.atan2(w[1] - centre[1], w[0] - centre[0])
        while ang1 - ang0 > np.pi:
            ang1 -= 2 * np.pi
        while ang0 - ang1 > np.pi:
            ang0 -= 2 * np.pi
        arc = np.linspace(ang0, ang1, 80)
        ax_d.plot(centre[0] + r * np.cos(arc), centre[1] + r * np.sin(arc), color=CRIMSON, lw=1.6)
    ax_d.plot(0, 0, "+", color=NAVY, ms=10, mew=1.4)
    lit = _hyperbolic_literals(30)
    r_err = abs(witness["circumradius_numeric"] - float(lit["circumradius"]))
    e_err = abs(witness["edge_numeric"] - float(lit["edge"]))
    ax_d.set_title(
        "(d) the {7,3} heptagon in the disk: angle 2$\\pi$/3 solved (X4)\n"
        f"R err {r_err:.0e}, edge err {e_err:.0e}",
        fontsize=10,
        color=NAVY,
    )
    ax_d.set_xlim(-1.08, 1.08)
    ax_d.set_ylim(-1.08, 1.08)
    ax_d.set_aspect("equal")
    ax_d.grid(False)

    for ax in (ax_a, ax_b, ax_c, ax_d):
        _style_axis(ax)
    return _save(fig, out_dir, "fig05_hardcore_certificates.png")


# ---------------------------------------------------------------------------
# scheme — the mini-repository architecture (hand-authored SVG)
# ---------------------------------------------------------------------------

SCHEME_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="940" height="470" viewBox="0 0 940 470">
  <defs>
    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{navy}"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="940" height="470" fill="#FFFFFF"/>
  <text x="470" y="30" text-anchor="middle" font-family="Liberation Sans, Arial" font-size="19" font-weight="bold" fill="{navy}">PLANETVORTEX — the planetary gravity-geometry bench (mini-repository)</text>

  <rect x="30" y="60" width="200" height="120" rx="8" fill="{light}" stroke="{steel}" stroke-width="1.4"/>
  <text x="130" y="86" text-anchor="middle" font-family="Liberation Sans, Arial" font-size="13" font-weight="bold" fill="{navy}">Inputs</text>
  <text x="130" y="108" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="12" fill="{navy}">NASA register: GM, a, e, T</text>
  <text x="130" y="128" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="12" fill="{navy}">Γ, R — the vortex figure</text>
  <text x="130" y="148" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="12" fill="{navy}">the Fano lines &#123;i, i+1, i+3&#125;</text>
  <text x="130" y="168" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11" fill="{steel}">presets: quick / default / full</text>

  <rect x="330" y="46" width="280" height="56" rx="8" fill="#FFFFFF" stroke="{steel}" stroke-width="1.4"/>
  <text x="470" y="68" text-anchor="middle" font-family="Liberation Sans, Arial" font-size="13" font-weight="bold" fill="{navy}">Layer N — nbody.py</text>
  <text x="470" y="88" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">Sun + 8 planets · RK4 · E, L · osculating (a, e)</text>

  <rect x="330" y="110" width="280" height="56" rx="8" fill="#FFFFFF" stroke="{steel}" stroke-width="1.4"/>
  <text x="470" y="132" text-anchor="middle" font-family="Liberation Sans, Arial" font-size="13" font-weight="bold" fill="{navy}">Layer F — fano.py · classical.py</text>
  <text x="470" y="152" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">PSL(2,7) · exact figure · Kepler · Schwarzschild · Hill</text>

  <rect x="330" y="174" width="280" height="56" rx="8" fill="#FFFFFF" stroke="{steel}" stroke-width="1.4"/>
  <text x="470" y="196" text-anchor="middle" font-family="Liberation Sans, Arial" font-size="13" font-weight="bold" fill="{navy}">Layer V — model.py</text>
  <text x="470" y="216" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">Kirchhoff RHS · RK4 · H, P, Q, I · Jacobian</text>

  <rect x="660" y="60" width="250" height="120" rx="8" fill="{light}" stroke="{steel}" stroke-width="1.4"/>
  <text x="785" y="86" text-anchor="middle" font-family="Liberation Sans, Arial" font-size="13" font-weight="bold" fill="{navy}">P-ladder — ladder.py</text>
  <text x="785" y="107" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">P1 anchor · P2 Kepler · P3 N-body</text>
  <text x="785" y="126" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">P4 algebra · P5 lattice · P6 cells</text>
  <text x="785" y="145" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">P7 gravity bridge</text>
  <text x="785" y="166" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11" fill="{steel}">tolerances: 1e-16 … 1e-2</text>

  <rect x="240" y="252" width="460" height="64" rx="8" fill="#FFFFFF" stroke="{navy}" stroke-width="1.6"/>
  <text x="470" y="276" text-anchor="middle" font-family="Liberation Sans, Arial" font-size="13" font-weight="bold" fill="{navy}">results/protocols/P1..P7_*.json — committed, deterministic</text>
  <text x="470" y="298" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">"every number is bound to a run" — re-derived by the test guard</text>

  <rect x="60" y="340" width="380" height="100" rx="8" fill="{light}" stroke="{steel}" stroke-width="1.4"/>
  <text x="250" y="366" text-anchor="middle" font-family="Liberation Sans, Arial" font-size="13" font-weight="bold" fill="{navy}">figures/ — this module</text>
  <text x="250" y="388" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">fig01 the figure · fig02 Kepler · fig03 simulation</text>
  <text x="250" y="407" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">fig04 lattice + cycles · scheme_planetvortex.svg</text>
  <text x="250" y="426" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11" fill="{steel}">300 dpi PNG, bound to the protocols</text>

  <rect x="500" y="340" width="380" height="100" rx="8" fill="{light}" stroke="{steel}" stroke-width="1.4"/>
  <text x="690" y="366" text-anchor="middle" font-family="Liberation Sans, Arial" font-size="13" font-weight="bold" fill="{navy}">docs/ — the publication stack</text>
  <text x="690" y="388" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">monograph/ (RU+EN) — the big research monograph</text>
  <text x="690" y="407" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">Theorems A, B, C · Lemmas D, E — the statement editions</text>
  <text x="690" y="426" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11" fill="{steel}">feeds parent roadmap T1, T3 (N=7 register) and R4</text>

  <line x1="230" y1="100" x2="322" y2="74" stroke="{navy}" stroke-width="1.3" marker-end="url(#arr)"/>
  <line x1="230" y1="120" x2="322" y2="136" stroke="{navy}" stroke-width="1.3" marker-end="url(#arr)"/>
  <line x1="230" y1="150" x2="322" y2="202" stroke="{navy}" stroke-width="1.3" marker-end="url(#arr)"/>
  <line x1="610" y1="74" x2="652" y2="100" stroke="{navy}" stroke-width="1.3" marker-end="url(#arr)"/>
  <line x1="610" y1="138" x2="652" y2="122" stroke="{navy}" stroke-width="1.3" marker-end="url(#arr)"/>
  <line x1="610" y1="202" x2="652" y2="150" stroke="{navy}" stroke-width="1.3" marker-end="url(#arr)"/>
  <line x1="785" y1="180" x2="700" y2="250" stroke="{navy}" stroke-width="1.3" marker-end="url(#arr)"/>
  <line x1="380" y1="316" x2="250" y2="336" stroke="{navy}" stroke-width="1.3" marker-end="url(#arr)"/>
  <line x1="560" y1="316" x2="690" y2="336" stroke="{navy}" stroke-width="1.3" marker-end="url(#arr)"/>
</svg>
"""


def scheme_svg(out_dir: Path) -> str:
    """Write the architecture scheme (SVG, vector)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "scheme_planetvortex.svg"
    svg = SCHEME_TEMPLATE.format(navy=NAVY, steel=STEEL, light=LIGHT)
    path.write_text(svg, encoding="utf-8")
    return str(path)


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------

FIGNAMES = (
    "fig01_fano_gravity_figure.png",
    "fig02_kepler_register.png",
    "fig03_planetary_simulation.png",
    "fig04_vortex_lattice.png",
    "fig05_hardcore_certificates.png",
    "scheme_planetvortex.svg",
)


def build_all(out_dir: Path = DEFAULT_OUT, proto_dir: Path = DEFAULT_PROTOS) -> List[str]:
    """Generate every figure; returns the list of written paths."""
    made: List[str] = []
    made.append(fig01_fano_gravity_figure(out_dir))
    made.append(fig02_kepler_register(out_dir, proto_dir))
    made.append(fig03_planetary_simulation(out_dir, proto_dir))
    made.append(fig04_vortex_lattice(out_dir, proto_dir))
    made.append(fig05_hardcore_certificates(out_dir, proto_dir))
    made.append(scheme_svg(out_dir))
    return made


def main() -> None:
    parser = argparse.ArgumentParser(description="PLANETVORTEX figure factory")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="output directory")
    parser.add_argument(
        "--protocols", type=Path, default=DEFAULT_PROTOS, help="protocols directory"
    )
    args = parser.parse_args()
    for path in build_all(args.out, args.protocols):
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
