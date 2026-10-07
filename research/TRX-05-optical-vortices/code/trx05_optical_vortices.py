#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
TRIVORTEX LAB — TRX-05 — OPTICAL VORTEXES AND THE POINT-VORTEX ANALOGY
============================================================================
Phase singularities (optical vortices) of a paraxial laser field behave,
to leading order, like point vortices of ideal fluid dynamics (Berry &
Dennis): zeros of a complex field with the same topological charge
circulate around each other exactly as Kirchhoff vortices do.  This study
makes the analogy quantitative:

  (A) three same-sign Kirchhoff vortices on an equilateral triangle rotate
      rigidly with omega = 3*Gamma/(2*pi*a^2) — the vortex Lagrange
      solution that underlies TRIVORTEX Theorem 3.1;
  (B) the complex scalar field psi(z) = exp(-r^2/w^2) * prod_k (z - z_k)
      renders the rotating "three-lobed" optical-vortex pattern: three
      dark cores co-rotating with the point vortices, total winding
      number 3 (the analogue of orbital angular momentum 3*hbar/photon).

What is computed
  * rigid rotation rate vs analytic, angular impulse I and Hamiltonian H
  * intensity rendering with zero tracking and winding number

With --figures: hand-authored scheme SVG + four canonical PNG panels
(300 dpi) into figures/, and a "figures" block added to the JSON protocol
(scheme, panels with captions, side/grid sweep data). Composable with
--smoke; without --figures the behavior, checks and JSON are unchanged.

Usage:  python trx05_optical_vortices.py [--smoke] [--figures]
Author: Isaev Iskhak Khamzatovich (repository owner)
License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

GAMMA, A = 1.0, 1.0

# TRIVORTEX canonical palette (v2.2.0 figures)
NAVY = "#0A1730"  # strokes and text
GOLD = "#D4AF37"  # accents
LIGHT_GOLD = "#F0D98C"  # soft fills
SERIES = ["#D4AF37", "#4C72B0", "#55A868", "#C44E52", "#8172B2"]

CHECKS = []


def add(name, value, target, tol, unit="", note=""):
    ok = abs(value - target) <= tol if isinstance(target, (int, float)) else bool(target)
    CHECKS.append(
        {
            "name": name,
            "value": value,
            "target": target,
            "tol": tol,
            "unit": unit,
            "pass": bool(ok),
            "note": note,
        }
    )
    return ok


# ---------------------------------------------------------------------------
# Kirchhoff point-vortex dynamics (interleaved layout [x1,y1, x2,y2, ...])
# ---------------------------------------------------------------------------


def vortex_rhs(t, s):
    n = s.size // 2
    xy = s.reshape(n, 2)
    d = np.zeros((n, 2))
    for k in range(n):
        for j in range(n):
            if j == k:
                continue
            dx = xy[k, 0] - xy[j, 0]
            dy = xy[k, 1] - xy[j, 1]
            r2 = dx * dx + dy * dy
            # u_k = -1/(2pi) * sum G_j (y_k - y_j)/r^2 ;  v_k = +1/(2pi) * sum G_j (x_k - x_j)/r^2
            d[k, 0] += -GAMMA * dy / (2.0 * np.pi * r2)
            d[k, 1] += +GAMMA * dx / (2.0 * np.pi * r2)
    return d.reshape(-1)


def angular_impulse(s):
    xy = s.reshape(-1, 2)
    return float(np.sum(GAMMA * np.sum(xy**2, axis=1)))


def hamiltonian(s):
    xy = s.reshape(-1, 2)
    n = xy.shape[0]
    H = 0.0
    for k in range(n):
        for j in range(k + 1, n):
            r = np.hypot(*(xy[k] - xy[j]))
            H += -GAMMA * GAMMA * np.log(r) / (2.0 * np.pi)
    return float(H)


# ---------------------------------------------------------------------------
# Complex field rendering
# ---------------------------------------------------------------------------


def field_intensity(xy, grid_x, grid_y, w=3.0):
    X, Y = np.meshgrid(grid_x, grid_y)
    psi = np.exp(-(X**2 + Y**2) / w**2).astype(complex)
    for px, py in xy:
        psi *= (X - px) + 1j * (Y - py)
    return np.abs(psi) ** 2, psi


def winding_number(psi, grid_x, grid_y, radius):
    """Total topological charge on a circle of given radius (grid estimate)."""
    X, Y = np.meshgrid(grid_x, grid_y)
    R = np.hypot(X, Y)
    mask = np.abs(R - radius) < (grid_x[1] - grid_x[0]) * 1.5
    ph = np.angle(psi[mask])
    ys = Y[mask]
    order = np.argsort(np.arctan2(ys, X[mask]))
    ph = ph[order]
    dph = np.diff(np.unwrap(ph))
    return float(np.round(np.sum(dph) / (2.0 * np.pi)))


def worst_minima_offset(intens, xy, grid_x, grid_y):
    """Worst distance from a vortex position to the nearest of the 60 deepest
    intensity pixels (module level so --figures can reuse the check logic)."""
    flat = intens.flatten()
    idx = np.argsort(flat)[:60]
    pts = np.column_stack(np.unravel_index(idx, intens.shape))
    pts_xy = np.column_stack([grid_x[pts[:, 1]], grid_y[pts[:, 0]]])
    worst = 0.0
    for px, py in xy:
        d = np.hypot(pts_xy[:, 0] - px, pts_xy[:, 1] - py)
        worst = max(worst, d.min())
    return worst


# ---------------------------------------------------------------------------
# SVG
# ---------------------------------------------------------------------------


def make_svg(intens, grid_x, grid_y, xy0, xy1, path):
    W, H = 900, 520
    x0, y0, sc = 60.0, 60.0, 170.0
    vmax = intens.max()
    cell_w = (grid_x[1] - grid_x[0]) * sc
    cell_h = (grid_y[1] - grid_y[0]) * sc
    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect width="{W}" height="{H}" fill="#0A1230"/>',
        '<text x="24" y="34" fill="#FFFFFF" font-family="Arial" font-size="19" '
        'font-weight="bold">TRX-05 &#8212; Three optical vortices: rotating 3-lobe pattern</text>',
    ]
    for iy in range(intens.shape[0]):
        for ix in range(intens.shape[1]):
            v = intens[iy, ix] / vmax
            if v < 0.96:
                lev = int(255 * (1.0 - v) ** 0.6)
                fill = f"rgb({lev//3},{lev//2},{min(255, lev)})"
                s.append(
                    f'<rect x="{x0 + ix*cell_w:.2f}" y="{y0 + iy*cell_h:.2f}" '
                    f'width="{cell_w+0.3:.2f}" height="{cell_h+0.3:.2f}" fill="{fill}"/>'
                )
    for px, py in xy0:
        s.append(
            f'<circle cx="{x0 + px*sc:.2f}" cy="{y0 - py*sc:.2f}" r="4" fill="none" stroke="#F2C14E" stroke-width="1.5"/>'
        )
    x02, y02, sc2 = 500.0, 60.0, 170.0
    for px, py in xy1:
        s.append(
            f'<circle cx="{x02 + px*sc2:.2f}" cy="{y02 - py*sc2:.2f}" r="4" fill="none" stroke="#6FB7FF" stroke-width="1.5"/>'
        )
    s += [
        '<text x="70" y="470" fill="#F2C14E" font-family="Arial" font-size="13">t = 0</text>',
        '<text x="510" y="470" fill="#6FB7FF" font-family="Arial" font-size="13">t = T/4 (rigid rotation)</text>',
        '<text x="24" y="500" fill="#9FB3D9" font-family="Arial" font-size="12">'
        "dark cores = phase singularities (optical vortices); circles = Kirchhoff vortex positions</text>",
        "</svg>",
    ]
    Path(path).write_text("\n".join(s), encoding="utf-8")


# ---------------------------------------------------------------------------
# Canonical figures (--figures mode): scheme SVG + four PNG panels
# ---------------------------------------------------------------------------


def make_scheme_svg(path):
    """Hand-authored schematic of the optical-vortex analogy: three phase
    singularities of a paraxial beam on an equilateral triangle, their phase
    windings, and the mapping to the Kirchhoff point-vortex model."""
    import math

    F = "Helvetica, Arial, sans-serif"

    def spiral_arm(cx, cy, phi0_deg, r0=6.0, r1=16.0, r2=27.0):
        """Two semicircular arcs approximating one Archimedean spiral arm."""
        a0 = math.radians(phi0_deg)
        a1 = math.radians(phi0_deg + 180.0)
        a2 = math.radians(phi0_deg + 360.0)
        p0 = (cx + r0 * math.cos(a0), cy + r0 * math.sin(a0))
        p1 = (cx + r1 * math.cos(a1), cy + r1 * math.sin(a1))
        p2 = (cx + r2 * math.cos(a2), cy + r2 * math.sin(a2))
        return (
            f"M {p0[0]:.1f} {p0[1]:.1f} "
            f"A {(r0 + r1) / 2:.1f} {(r0 + r1) / 2:.1f} 0 0 1 {p1[0]:.1f} {p1[1]:.1f} "
            f"A {(r1 + r2) / 2:.1f} {(r1 + r2) / 2:.1f} 0 0 1 {p2[0]:.1f} {p2[1]:.1f}"
        )

    s = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="960" height="540" viewBox="0 0 960 540">',
        "  <defs>",
        '    <marker id="arrN" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto-start-reverse">',
        '      <path d="M0,0 L10,5 L0,10 z" fill="#0A1730"/>',
        "    </marker>",
        '    <marker id="arrG" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto-start-reverse">',
        '      <path d="M0,0 L10,5 L0,10 z" fill="#D4AF37"/>',
        "    </marker>",
        "  </defs>",
        '  <rect width="960" height="540" fill="#FFFFFF"/>',
        # title + subtitle
        f'  <text x="30" y="40" font-family="{F}" font-size="21" font-weight="bold" '
        'fill="#0A1730">TRX-05 &#8212; Scheme: optical vortices and the vortex-triangle '
        "analogy</text>",
        f'  <text x="30" y="63" font-family="{F}" font-size="13" fill="#3A4A66">Phase '
        "singularities of a paraxial laser field move as Kirchhoff point vortices: three "
        "unit charges rotate rigidly as an equilateral triangle</text>",
        # ---- left panel: paraxial beam cross-section with the core triangle --
        '  <rect x="60" y="92" width="380" height="330" rx="10" fill="#FBF6E8" '
        'stroke="#0A1730" stroke-width="2"/>',
        f'  <text x="250" y="86" font-family="{F}" font-size="12" fill="#0A1730" '
        'text-anchor="middle">paraxial laser beam &#8212; transverse (x, y) plane</text>',
        # Gaussian envelope (dashed circles)
        '  <circle cx="250" cy="265" r="138" fill="none" stroke="#0A1730" '
        'stroke-width="1" stroke-dasharray="4 5" opacity="0.35"/>',
        '  <circle cx="250" cy="265" r="96" fill="none" stroke="#0A1730" '
        'stroke-width="1" stroke-dasharray="4 5" opacity="0.3"/>',
        f'  <text x="250" y="415" font-family="{F}" font-size="11" fill="#3A4A66" '
        'text-anchor="middle">Gaussian envelope exp(&#8722;r&#178;/w&#178;), w = 3a</text>',
        # rotation trajectory (dashed gold circle) + rotation arrow
        '  <circle cx="250" cy="265" r="88" fill="none" stroke="#D4AF37" '
        'stroke-width="1.3" stroke-dasharray="5 4" opacity="0.9"/>',
        '  <path d="M 356 214 A 118 118 0 0 0 144 214" fill="none" stroke="#0A1730" '
        'stroke-width="1.8" marker-end="url(#arrN)"/>',
        f'  <text x="250" y="128" font-family="{F}" font-size="13" font-weight="bold" '
        'fill="#0A1730" text-anchor="middle">&#969; = 3&#915;/(2&#960;a&#178;) = 0.4775</text>',
        # radius line to the top core
        '  <line x1="250" y1="265" x2="250" y2="177" stroke="#0A1730" stroke-width="1" '
        'stroke-dasharray="3 3" opacity="0.7"/>',
        f'  <text x="257" y="222" font-family="{F}" font-size="11.5" fill="#0A1730">'
        "r_c = a/&#8730;3</text>",
        # triangle edges
        '  <line x1="250" y1="177" x2="176.4" y2="309" stroke="#0A1730" stroke-width="1.7"/>',
        '  <line x1="176.4" y1="309" x2="323.6" y2="309" stroke="#0A1730" stroke-width="1.7"/>',
        '  <line x1="323.6" y1="309" x2="250" y2="177" stroke="#0A1730" stroke-width="1.7"/>',
        f'  <text x="243" y="304" font-family="{F}" font-size="12" font-weight="bold" '
        'fill="#0A1730" text-anchor="end">a</text>',
        # centroid
        '  <line x1="244" y1="265" x2="256" y2="265" stroke="#0A1730" stroke-width="1.4"/>',
        '  <line x1="250" y1="259" x2="250" y2="271" stroke="#0A1730" stroke-width="1.4"/>',
        # cores: dark centre + gold ring + phase-winding arc (charge +1)
        '  <circle cx="250" cy="177" r="10" fill="none" stroke="#D4AF37" stroke-width="1.8"/>',
        '  <circle cx="250" cy="177" r="5.5" fill="#0A1730" stroke="none"/>',
        '  <path d="M 266 177 A 16 16 0 1 1 239.8 166.8" fill="none" stroke="#0A1730" '
        'stroke-width="1.3" stroke-dasharray="3 3" marker-end="url(#arrN)"/>',
        f'  <text x="226" y="166" font-family="{F}" font-size="11.5" fill="#0A1730" '
        'text-anchor="end">q&#8321; = +1</text>',
        '  <circle cx="176.4" cy="309" r="10" fill="none" stroke="#D4AF37" stroke-width="1.8"/>',
        '  <circle cx="176.4" cy="309" r="5.5" fill="#0A1730" stroke="none"/>',
        '  <path d="M 192.4 309 A 16 16 0 1 1 166.2 298.8" fill="none" stroke="#0A1730" '
        'stroke-width="1.3" stroke-dasharray="3 3" marker-end="url(#arrN)"/>',
        f'  <text x="120" y="292" font-family="{F}" font-size="11.5" fill="#0A1730">q&#8322; = +1</text>',
        '  <circle cx="323.6" cy="309" r="10" fill="none" stroke="#D4AF37" stroke-width="1.8"/>',
        '  <circle cx="323.6" cy="309" r="5.5" fill="#0A1730" stroke="none"/>',
        '  <path d="M 339.6 309 A 16 16 0 1 1 313.4 298.8" fill="none" stroke="#0A1730" '
        'stroke-width="1.3" stroke-dasharray="3 3" marker-end="url(#arrN)"/>',
        f'  <text x="312" y="338" font-family="{F}" font-size="11.5" fill="#0A1730">q&#8323; = +1</text>',
        f'  <text x="250" y="345" font-family="{F}" font-size="11" fill="#3A4A66" '
        'text-anchor="middle">dark cores: intensity zeros = phase singularities,</text>',
        f'  <text x="250" y="361" font-family="{F}" font-size="11" fill="#3A4A66" '
        'text-anchor="middle">phase winds by 2&#960; around each core (charge +1)</text>',
        # ---- right panel (top): mapping optics -> point-vortex model ---------
        '  <rect x="520" y="92" width="380" height="208" rx="10" fill="#FFFFFF" '
        'stroke="#0A1730" stroke-width="2"/>',
        f'  <text x="710" y="86" font-family="{F}" font-size="12" fill="#0A1730" '
        'text-anchor="middle">optical singularity &#8594; point-vortex model</text>',
        f'  <text x="538" y="116" font-family="{F}" font-size="10.5" font-weight="bold" '
        'fill="#0A1730">OPTICS (this study)</text>',
        f'  <text x="722" y="116" font-family="{F}" font-size="10.5" font-weight="bold" '
        'fill="#0A1730">VORTEX MODEL</text>',
    ]
    rows = [
        ("intensity zero (dark core)", "point vortex, Kirchhoff (E1)"),
        ("topological charge q = +1", "circulation &#915; = 1"),
        ("winding number N = 3", "&#931;&#915; = 3, OAM 3&#8463;/photon"),
        ("angular impulse I = &#931;&#915;|r|&#178;", "Chaplygin integral, I = a&#178;"),
        ("rigid rotation of 3 cores", "Theorem 3.1 choreography"),
    ]
    for i, (lft, rgt) in enumerate(rows):
        y = 140 + 30 * i
        s.append(
            f'  <text x="538" y="{y}" font-family="{F}" font-size="11" '
            f'fill="#0A1730">{lft}</text>'
        )
        s.append(
            f'  <line x1="692" y1="{y - 4}" x2="712" y2="{y - 4}" stroke="#D4AF37" '
            f'stroke-width="1.7" marker-end="url(#arrG)"/>'
        )
        s.append(
            f'  <text x="722" y="{y}" font-family="{F}" font-size="11" '
            f'fill="#0A1730">{rgt}</text>'
        )
        if i < len(rows) - 1:
            s.append(
                f'  <line x1="530" y1="{y + 11}" x2="890" y2="{y + 11}" '
                'stroke="#0A1730" stroke-width="0.5" opacity="0.25"/>'
            )
    s += [
        # ---- right panel (bottom): far-field spiral of the charge-3 beam ----
        '  <rect x="520" y="310" width="380" height="112" rx="10" fill="#FBF6E8" '
        'stroke="#0A1730" stroke-width="2"/>',
        '  <circle cx="585" cy="366" r="5.5" fill="#0A1730" stroke="none"/>',
        f'  <path d="{spiral_arm(585, 366, 90)}" fill="none" stroke="#D4AF37" '
        'stroke-width="1.7" marker-end="url(#arrG)"/>',
        f'  <path d="{spiral_arm(585, 366, 210)}" fill="none" stroke="#D4AF37" '
        'stroke-width="1.7" marker-end="url(#arrG)"/>',
        f'  <path d="{spiral_arm(585, 366, 330)}" fill="none" stroke="#D4AF37" '
        'stroke-width="1.7" marker-end="url(#arrG)"/>',
        '  <circle cx="585" cy="366" r="46" fill="none" stroke="#0A1730" '
        'stroke-width="1.2" stroke-dasharray="4 4"/>',
        f'  <text x="656" y="336" font-family="{F}" font-size="11.5" font-weight="bold" '
        'fill="#0A1730">far field: spiral phase front</text>',
        f'  <text x="656" y="356" font-family="{F}" font-size="11" fill="#0A1730">'
        "winding on any circle beyond</text>",
        f'  <text x="656" y="374" font-family="{F}" font-size="11" fill="#0A1730">the '
        "cores: N = 3 = total charge</text>",
        f'  <text x="656" y="392" font-family="{F}" font-size="11" fill="#3A4A66">'
        "(measured exactly on r = 1.55a)</text>",
        # bottom strip
        f'  <text x="60" y="470" font-family="{F}" font-size="12" fill="#0A1730">'
        "&#936;(z) = exp(&#8722;r&#178;/w&#178;) &#183; &#928;k (z &#8722; z_k(t)) — three "
        "unit charges on a triangle of side a</text>",
        f'  <text x="60" y="492" font-family="{F}" font-size="12" fill="#3A4A66">'
        "measured rotation rate 0.477464829 vs analytic 3&#915;/(2&#960;a&#178;) (tolerance "
        "1e-8); invariants I = a&#178; and H conserved to 1e-12</text>",
        "</svg>",
    ]
    Path(path).write_text("\n".join(s), encoding="utf-8")


def render_figures(
    sol,
    ts,
    Y,
    pos0,
    pos_q,
    intens0,
    psi0,
    grid_x,
    grid_y,
    omega_an,
    slope,
    worst_track,
    cell,
    I_vals,
    H_vals,
    wind,
    smoke,
    figdir,
):
    """Render the scheme SVG and four canonical PNG panels into figures/.

    Reuses the dynamics, field renderings and invariants already computed in
    main(); adds the side-length sweep of the triangle (numeric re-runs) and
    the grid-spacing sweep of the core-tracking check. Returns the "figures"
    block for the JSON protocol.
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap, LogNorm

    figdir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": NAVY,
            "axes.labelcolor": NAVY,
            "axes.titlecolor": NAVY,
            "axes.linewidth": 1.2,
            "text.color": NAVY,
            "xtick.color": NAVY,
            "ytick.color": NAVY,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "axes.labelsize": 11.5,
            "axes.titlesize": 12.5,
            "font.size": 11,
            "grid.color": NAVY,
            "grid.alpha": 0.3,
            "grid.linewidth": 0.6,
            "legend.frameon": False,
            "legend.fontsize": 10,
        }
    )
    blue, green, red = SERIES[1], SERIES[2], SERIES[3]
    suptitle = "TRX-05 · Optical vortices and the point-vortex analogy"
    make_scheme_svg(figdir / "scheme_trx05.svg")

    # ---- sweep (a): rotation rate vs triangle side (numeric re-runs) --------
    a_grid = np.array([0.6, 0.8, 1.0, 1.2, 1.5, 2.0]) if not smoke else np.array([0.8, 1.0, 1.5])
    om_grid = 3.0 * GAMMA / (2.0 * np.pi * a_grid**2)
    om_num = []
    for a_i, om_i in zip(a_grid, om_grid):
        rc_i = a_i / np.sqrt(3.0)
        ang_i = np.array([np.pi / 2, np.pi / 2 + 2 * np.pi / 3, np.pi / 2 + 4 * np.pi / 3])
        pos_i = rc_i * np.stack([np.cos(ang_i), np.sin(ang_i)], axis=1)
        T_i = (1.0 if smoke else 2.0) * 2.0 * np.pi / om_i
        s_i = solve_ivp(
            vortex_rhs,
            (0.0, T_i),
            pos_i.reshape(-1),
            method="DOP853",
            rtol=1e-12,
            atol=1e-12,
            dense_output=True,
            max_step=0.1,
        )
        ts_i = np.linspace(0.0, T_i, 400)
        Yi = s_i.sol(ts_i).reshape(3, 2, -1)
        rel_i = Yi[0] - Yi.mean(axis=0)
        th_i = np.unwrap(np.arctan2(rel_i[1], rel_i[0]))
        om_num.append(float(np.polyfit(ts_i, th_i, 1)[0]))
    om_num = np.array(om_num)

    # ---- sweep (b): core-tracking error vs grid spacing ----------------------
    g_grid = (
        np.array([0.012, 0.018, 0.024, 0.030, 0.040, 0.052, 0.064, 0.080])
        if not smoke
        else np.array([0.030, 0.045, 0.060])
    )
    track_err = []
    for g_i in g_grid:
        gx = np.arange(-1.7, 1.7 + g_i, g_i)
        gy = np.arange(-1.7, 1.7 + g_i, g_i)
        it0, _ = field_intensity(pos0, gx, gy)
        itq, _ = field_intensity(pos_q, gx, gy)
        track_err.append(
            max(worst_minima_offset(it0, pos0, gx, gy), worst_minima_offset(itq, pos_q, gx, gy))
        )
    track_err = np.array(track_err)

    extent = [grid_x[0], grid_x[-1], grid_y[0], grid_y[-1]]

    # ================= fig01 — field landscape ================================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    cmap = LinearSegmentedColormap.from_list("triton", [NAVY, "#3A5A8C", LIGHT_GOLD, "#FFFFFF"])
    im1 = ax1.imshow(
        intens0,
        origin="lower",
        extent=extent,
        cmap=cmap,
        norm=LogNorm(vmin=max(intens0.max() * 1e-4, 1e-12), vmax=intens0.max()),
        interpolation="nearest",
    )
    tri = np.vstack([pos0, pos0[:1]])
    ax1.plot(tri[:, 0], tri[:, 1], color=GOLD, lw=1.5, ls="--", label="vortex triangle (a = 1)")
    ax1.scatter(
        pos0[:, 0],
        pos0[:, 1],
        s=140,
        facecolors="none",
        edgecolors=GOLD,
        linewidths=1.6,
        label="phase singularities (charge +1)",
    )
    ax1.set_title("(a) intensity $|\\psi(x,y)|^2$ at $t = 0$ (log scale)")
    ax1.set_xlabel("x (units of a)")
    ax1.set_ylabel("y (units of a)")
    ax1.set_xlim(extent[0], extent[1])
    ax1.set_ylim(extent[2], extent[3])
    ax1.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0))
    fig.colorbar(im1, ax=ax1, shrink=0.85, label="$|\\psi|^2$ (normalized)")

    im2 = ax2.imshow(
        np.angle(psi0),
        origin="lower",
        extent=extent,
        cmap="twilight",
        vmin=-np.pi,
        vmax=np.pi,
        interpolation="nearest",
    )
    th_ring = np.linspace(0.0, 2.0 * np.pi, 200)
    for px, py in pos0:
        ax2.plot(px + 0.35 * np.cos(th_ring), py + 0.35 * np.sin(th_ring), color=GOLD, lw=1.4)
    ax2.plot(
        1.55 * np.cos(th_ring),
        1.55 * np.sin(th_ring),
        color=NAVY,
        lw=1.4,
        ls="--",
        label="winding evaluation circle, r = 1.55",
    )
    ax2.set_title("(b) phase $\\arg\\psi$: $2\\pi$ winding around each core")
    ax2.set_xlabel("x (units of a)")
    ax2.set_ylabel("y (units of a)")
    ax2.set_xlim(extent[0], extent[1])
    ax2.set_ylim(extent[2], extent[3])
    ax2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14))
    fig.colorbar(im2, ax=ax2, shrink=0.85, label="$\\arg\\psi$ (rad)", ticks=[-np.pi, 0, np.pi])
    fig.savefig(figdir / "fig01_field_landscape.png")
    plt.close(fig)

    # ================= fig02 — headline: rigid rotation =======================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    for k in range(3):
        ax1.plot(Y[k, 0], Y[k, 1], color=SERIES[k], lw=1.8, label=f"vortex {k + 1}")
    ax1.scatter(
        pos0[:, 0], pos0[:, 1], s=90, marker="o", color=GOLD, zorder=5, label="start (t = 0)"
    )
    ax1.scatter(
        Y[:, 0, -1],
        Y[:, 1, -1],
        s=90,
        marker=">",
        color=NAVY,
        zorder=5,
        label=f"end (t = {ts[-1]:.2f})",
    )
    ax1.plot(0.0, 0.0, marker="+", color=NAVY, ms=12, mew=1.8, ls="none")
    ax1.set_aspect("equal")
    ax1.set_title("(a) core worldlines over three rotations")
    ax1.set_xlabel("x (units of a)")
    ax1.set_ylabel("y (units of a)")
    ax1.legend(loc="upper right", bbox_to_anchor=(1.0, 1.0))

    rel = Y[0] - Y.mean(axis=0)
    theta = np.unwrap(np.arctan2(rel[1], rel[0]))
    ax2.plot(ts, theta, color=GOLD, lw=2.2, label="measured $\\theta_1(t)$ (DOP853)")
    ax2.plot(
        ts,
        omega_an * ts,
        color=NAVY,
        lw=1.6,
        ls="--",
        label="analytic $\\omega t$, $\\omega = 3\\Gamma/(2\\pi a^2)$",
    )
    ax2.set_title("(b) polar angle of core 1 about the centroid")
    ax2.set_xlabel("time t (units of $a^2/\\Gamma$)")
    ax2.set_ylabel("$\\theta_1$ (rad)")
    ax2.annotate(
        f"fit: $\\omega$ = {slope:.9f}\nanalytic: {omega_an:.9f}"
        f"\n$|\\Delta\\omega|$ within 1e-8",
        xy=(0.04, 0.06),
        xycoords="axes fraction",
        fontsize=10.5,
        color=NAVY,
        bbox=dict(boxstyle="round,pad=0.35", fc=LIGHT_GOLD, ec=GOLD, lw=1.0),
    )
    ax2.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0))
    ax2.grid(alpha=0.3)
    fig.savefig(figdir / "fig02_rigid_rotation.png")
    plt.close(fig)

    # ================= fig03 — parameter sweeps ===============================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    a_dense = np.linspace(0.55, 2.1, 300)
    ax1.loglog(
        a_dense,
        3.0 * GAMMA / (2.0 * np.pi * a_dense**2),
        color=NAVY,
        lw=2.0,
        label="analytic $\\omega(a) = 3\\Gamma/(2\\pi a^2)$",
    )
    ax1.loglog(
        a_grid,
        om_num,
        "o",
        color=GOLD,
        ms=8,
        mec=NAVY,
        mew=0.8,
        label="numeric re-runs (DOP853, 2 rotations)",
    )
    ax1.loglog([1.0], [omega_an], "*", color=red, ms=14, label="preset a = 1")
    ax1.set_title("(a) rotation rate vs triangle side")
    ax1.set_xlabel("triangle side a (units of preset a = 1)")
    ax1.set_ylabel("rotation rate $\\omega$ (1/time)")
    ax1.legend(loc="upper right", bbox_to_anchor=(1.0, 1.0))
    ax1.grid(alpha=0.3, which="both")

    ax2.plot(
        g_grid,
        track_err,
        "o-",
        color=GOLD,
        lw=1.8,
        mec=NAVY,
        mew=0.8,
        label="measured worst core offset",
    )
    ax2.plot(g_grid, 2.0 * g_grid, "--", color=NAVY, lw=1.8, label="acceptance: 2 grid cells")
    ax2.plot([cell], [worst_track], "s", color=red, ms=9, label=f"preset grid (cell = {cell:.3f})")
    ax2.set_title("(b) zero-tracking error vs grid spacing")
    ax2.set_xlabel("grid spacing (units of a)")
    ax2.set_ylabel("worst core offset (units of a)")
    ax2.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0))
    ax2.grid(alpha=0.3)
    fig.savefig(figdir / "fig03_parameter_sweeps.png")
    plt.close(fig)

    # ================= fig04 — dynamics: invariants and rigidity ==============
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    drift_I = np.maximum(np.abs(I_vals - I_vals[0]), 1e-19)
    drift_H = np.maximum(np.abs(H_vals - H_vals[0]), 1e-19)
    ax1.semilogy(
        ts,
        drift_I,
        color=SERIES[0],
        lw=1.6,
        label="$|\\Delta I|$, angular impulse $I = \\sum\\Gamma|r|^2$",
    )
    ax1.semilogy(ts, drift_H, color=blue, lw=1.6, label="$|\\Delta H|$, Kirchhoff Hamiltonian")
    ax1.axhline(1e-12, color=NAVY, ls="--", lw=1.5, label="acceptance tolerance 1e-12")
    ax1.set_ylim(3e-19, 3e-11)
    ax1.set_title("(a) invariant drifts over three rotations")
    ax1.set_xlabel("time t (units of $a^2/\\Gamma$)")
    ax1.set_ylabel("invariant drift (dimensionless)")
    ax1.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0))
    ax1.grid(alpha=0.3, which="both")

    d12 = np.hypot(Y[0, 0] - Y[1, 0], Y[0, 1] - Y[1, 1]) - 1.0
    d23 = np.hypot(Y[1, 0] - Y[2, 0], Y[1, 1] - Y[2, 1]) - 1.0
    d31 = np.hypot(Y[2, 0] - Y[0, 0], Y[2, 1] - Y[0, 1]) - 1.0
    ax2.plot(ts, d12, color=SERIES[0], lw=1.6, label="$d_{12}(t) - a$")
    ax2.plot(ts, d23, color=blue, lw=1.6, label="$d_{23}(t) - a$")
    ax2.plot(ts, d31, color=green, lw=1.6, label="$d_{31}(t) - a$")
    ax2.axhline(0.0, color=NAVY, ls="--", lw=1.0, alpha=0.6)
    ax2.annotate(
        f"max side deviation {max(np.max(np.abs(d12)), np.max(np.abs(d23)), np.max(np.abs(d31))):.2e}"
        f"\n(rigid equilateral rotation, side a = 1)",
        xy=(0.04, 0.06),
        xycoords="axes fraction",
        fontsize=10.5,
        color=NAVY,
        bbox=dict(boxstyle="round,pad=0.35", fc=LIGHT_GOLD, ec=GOLD, lw=1.0),
    )
    ax2.set_title("(b) side-length deviations from the equilateral state")
    ax2.set_xlabel("time t (units of $a^2/\\Gamma$)")
    ax2.set_ylabel("$d_{jk}(t) - a$ (units of a)")
    ax2.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0))
    ax2.grid(alpha=0.3)
    fig.savefig(figdir / "fig04_invariants_rigidity.png")
    plt.close(fig)

    # ---- JSON figures block ==================================================
    return {
        "scheme": {
            "file": "figures/scheme_trx05.svg",
            "caption": (
                "Optical-vortex scheme - three phase singularities (dark cores, "
                "charge +1) of a paraxial beam with Gaussian envelope w = 3a sit "
                "on an equilateral triangle of side a and rotate rigidly with "
                "omega = 3*Gamma/(2*pi*a^2) = 0.4775 (left); mapping to the "
                "Kirchhoff point-vortex model: intensity zero -> point vortex, "
                "charge q -> circulation Gamma, winding N = 3 -> total charge "
                "and OAM 3*hbar per photon, angular impulse I = a^2 -> Chaplygin "
                "integral; far field shows the three-armed spiral phase front."
            ),
        },
        "panels": [
            {
                "file": "figures/fig01_field_landscape.png",
                "caption": (
                    "Field landscape at t = 0: (a) intensity |psi|^2 on a log scale - "
                    "three dark cores sit at the vertices of the equilateral triangle "
                    "(side a = 1) inside the Gaussian envelope; (b) phase arg psi - "
                    "the phase winds by 2*pi around each core and by N = 3 on the "
                    "evaluation circle r = 1.55 (grid spacing 0.018)."
                ),
            },
            {
                "file": "figures/fig02_rigid_rotation.png",
                "caption": (
                    "Headline result - rigid rotation of the vortex-triangle: (a) "
                    "worldlines of the three cores over T = 3 rotations are circles of "
                    "radius r_c = a/sqrt(3) about the common centroid; (b) the polar "
                    f"angle of core 1 grows linearly: measured omega = {slope:.9f} "
                    f"against analytic 3*Gamma/(2*pi*a^2) = {omega_an:.9f} - agreement "
                    "within the 1e-8 acceptance tolerance (optical Lagrange "
                    "choreography)."
                ),
            },
            {
                "file": "figures/fig03_parameter_sweeps.png",
                "caption": (
                    "Parameter sweeps: (a) rotation rate vs triangle side - analytic "
                    "Kirchhoff law omega(a) = 3*Gamma/(2*pi*a^2) against numeric "
                    "DOP853 re-runs at each grid side (preset a = 1: omega = "
                    f"{omega_an:.6f}); (b) core-tracking error vs grid spacing - the "
                    "worst distance from a vortex to the nearest intensity minimum "
                    "stays below the 2-cell acceptance line, at the preset spacing "
                    f"0.018 the offset is {worst_track:.4f}."
                ),
            },
            {
                "file": "figures/fig04_invariants_rigidity.png",
                "caption": (
                    "Dynamics and invariants over T = 3 rotations: (a) drifts of the "
                    "angular impulse I and the Kirchhoff Hamiltonian H on a log scale "
                    "- both conserved below the 1e-12 acceptance tolerance at "
                    "integrator level; (b) side-length deviations d_jk(t) - a of the "
                    "rotating triangle stay at machine level - the configuration "
                    "rotates as a rigid equilateral triangle."
                ),
            },
        ],
        "data": {
            "side_sweep": {
                "a": [round(float(v), 4) for v in a_grid],
                "omega_analytic": [round(float(v), 9) for v in om_grid],
                "omega_numeric": [round(float(v), 9) for v in om_num],
            },
            "grid_sweep": {
                "grid_spacing": [round(float(v), 4) for v in g_grid],
                "worst_core_offset": [round(float(v), 5) for v in track_err],
                "acceptance_two_cells": [round(float(2.0 * v), 4) for v in g_grid],
            },
            "preset": {
                "a": float(A),
                "Gamma": float(GAMMA),
                "omega_analytic": round(float(omega_an), 9),
                "omega_measured": round(float(slope), 9),
                "rotation_period": round(float(2.0 * np.pi / omega_an), 4),
                "T_rotation": round(float(ts[-1]), 4),
                "r_c": round(float(A / np.sqrt(3.0)), 6),
                "grid_spacing": round(float(cell), 4),
                "worst_core_offset": round(float(worst_track), 5),
                "winding_number": float(wind),
                "I0": round(float(I_vals[0]), 12),
                "H0": round(float(H_vals[0]), 12),
            },
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv=None):
    ap = argparse.ArgumentParser(description="TRX-05 optical vortices")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument(
        "--figures",
        action="store_true",
        help="write scheme SVG + four canonical PNG panels into figures/ "
        "and add a figures block to the JSON protocol",
    )
    args = ap.parse_args(argv)
    smoke = args.smoke or bool(os.environ.get("TRX_SMOKE"))
    t0 = time.time()

    # equilateral triangle, side a, centred at origin
    rc = A / np.sqrt(3.0)
    ang = np.array([np.pi / 2, np.pi / 2 + 2 * np.pi / 3, np.pi / 2 + 4 * np.pi / 3])
    pos0 = rc * np.stack([np.cos(ang), np.sin(ang)], axis=1)
    s0 = pos0.reshape(-1)

    omega_an = 3.0 * GAMMA / (2.0 * np.pi * A**2)
    Trot = 2.0 * np.pi / omega_an
    T = (1.0 if smoke else 3.0) * Trot
    sol = solve_ivp(
        vortex_rhs,
        (0.0, T),
        s0,
        method="DOP853",
        rtol=1e-13,
        atol=1e-13,
        dense_output=True,
        max_step=0.05,
    )
    ts = np.linspace(0.0, T, 400 if smoke else 2000)
    Y = sol.sol(ts).reshape(3, 2, -1)

    # check 1: rotation rate from body-1 polar angle about centroid
    rel = Y[0] - Y.mean(axis=0)
    theta = np.unwrap(np.arctan2(rel[1], rel[0]))
    slope = float(np.polyfit(ts, theta, 1)[0])
    add(
        "rotation_rate_vs_analytic",
        slope,
        omega_an,
        1e-8,
        "1/time",
        f"omega = 3*Gamma/(2*pi*a^2) = {omega_an:.9f}",
    )

    # check 2/3: angular impulse I (Chaplygin-type) and Hamiltonian H
    I_vals = np.array([angular_impulse(sol.sol(t)) for t in ts])
    add(
        "angular_impulse_I_conserved",
        float(np.max(np.abs(I_vals - I_vals[0]))),
        0.0,
        1e-12,
        "dimless",
        f"I = sum(Gamma r^2) = {I_vals[0]:.12f} = a^2 (vortex C_Ch)",
    )
    H_vals = np.array([hamiltonian(sol.sol(t)) for t in ts])
    add(
        "kirchhoff_hamiltonian_conserved",
        float(np.max(np.abs(H_vals - H_vals[0]))),
        0.0,
        1e-12,
        "dimless",
        "H = -(G^2/2pi) sum ln r",
    )

    # field rendering at t=0 and t=Trot/4
    t_quarter = 0.25 * Trot
    pos_q = sol.sol([t_quarter]).reshape(3, 2)
    g = 0.03 if smoke else 0.018
    grid_x = np.arange(-1.7, 1.7 + g, g)
    grid_y = np.arange(-1.7, 1.7 + g, g)
    intens0, psi0 = field_intensity(pos0, grid_x, grid_y)
    intensq, psiq = field_intensity(pos_q, grid_x, grid_y)

    # check 4: deepest minima coincide with vortex positions (within 2 cells)
    cell = grid_x[1] - grid_x[0]
    worst0 = worst_minima_offset(intens0, pos0, grid_x, grid_y)
    worstq = worst_minima_offset(intensq, pos_q, grid_x, grid_y)
    add(
        "field_minima_track_vortices",
        max(worst0, worstq),
        0.0,
        2.0 * cell,
        "length",
        f"worst core offset {max(worst0, worstq):.4f} vs 2 grid cells {2*cell:.4f}",
    )

    # check 5: winding number of the field on a large circle = 3 exactly
    wind = winding_number(psi0, grid_x, grid_y, radius=1.55)
    add(
        "total_winding_number_is_3",
        wind,
        3.0,
        1e-12,
        "integer",
        "topological charge = orbital angular momentum 3*hbar/photon analogue",
    )

    # --- SVG ---------------------------------------------------------------------
    out = Path(__file__).resolve().parents[1] / "results"
    out.mkdir(exist_ok=True)
    make_svg(intens0, grid_x, grid_y, pos0, pos_q, out / "trx05_plot.svg")

    # --- canonical figures (--figures, additive) -----------------------------
    figures_block = None
    figdir = Path(__file__).resolve().parents[1] / "figures"
    if args.figures:
        figures_block = render_figures(
            sol=sol,
            ts=ts,
            Y=Y,
            pos0=pos0,
            pos_q=pos_q,
            intens0=intens0,
            psi0=psi0,
            grid_x=grid_x,
            grid_y=grid_y,
            omega_an=omega_an,
            slope=slope,
            worst_track=max(worst0, worstq),
            cell=cell,
            I_vals=I_vals,
            H_vals=H_vals,
            wind=wind,
            smoke=smoke,
            figdir=figdir,
        )

    # --- protocol -----------------------------------------------------------------
    all_pass = all(c["pass"] for c in CHECKS)
    stride = max(1, ts.size // 400)
    protocol = {
        "study": "TRX-05",
        "title": "Optical vortices of laser beams and the point-vortex analogy",
        "status": "PASS" if all_pass else "FAIL",
        "smoke": bool(smoke),
        "runtime_s": round(time.time() - t0, 3),
        "checks": CHECKS,
        "series": {
            "t": ts[::stride].round(4).tolist(),
            "x1": Y[0, 0][::stride].round(8).tolist(),
            "y1": Y[0, 1][::stride].round(8).tolist(),
            "x2": Y[1, 0][::stride].round(8).tolist(),
            "y2": Y[1, 1][::stride].round(8).tolist(),
            "x3": Y[2, 0][::stride].round(8).tolist(),
            "y3": Y[2, 1][::stride].round(8).tolist(),
        },
        "meta": {
            "equations": [
                "u_k = -(1/2pi) sum_j G_j (y_k-y_j)/r^2 ; v_k = +(1/2pi) sum_j G_j (x_k-x_j)/r^2",
                "I = sum_k G_k |r_k|^2 (vortex Chaplygin-type integral) ; H = -(G^2/2pi) sum ln r",
                "psi(z) = exp(-r^2/w^2) * prod_k (z - z_k(t))",
            ],
            "omega_analytic": omega_an,
            "winding_number": wind,
            "note": "zeros of a paraxial complex field move like point vortices (Berry-Dennis); "
            "the equilateral same-sign triangle is the optical Lagrange choreography",
        },
    }
    if figures_block is not None:
        protocol["figures"] = figures_block
    (out / "trx05_results.json").write_text(json.dumps(protocol, indent=2), encoding="utf-8")

    print(f"\nTRX-05 — optical vortices  [{'SMOKE' if smoke else 'FULL'}]")
    for c in CHECKS:
        flag = "PASS" if c["pass"] else "FAIL"
        print(
            f"  [{flag}] {c['name']:<42} value={c['value']:.6e} target={c['target']:.1e} tol={c['tol']:.1e}"
        )
    if figures_block is not None:
        print("  figures: 5 files written to figures/:")
        for entry in [figures_block["scheme"]] + figures_block["panels"]:
            print(f"    - {entry['file']}")
    print(f"  status: {protocol['status']}   runtime: {protocol['runtime_s']} s")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
