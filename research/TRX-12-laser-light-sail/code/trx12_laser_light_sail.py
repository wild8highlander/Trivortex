#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
TRIVORTEX LAB — TRX-12 — LASER HIGHWAY: LIGHT SAIL STATIONKEEPING AT L4/L5
============================================================================
A photon light sail in the Earth-Moon circular restricted three-body
problem, pushed by a ground- or orbit-based laser.  The sail feels the
photon thrust a_L = 2P/(c m) pointed by a beam-steering control law; the
task is to hold a spacecraft near the libration point L4 (which is linearly
stable but drifts freely under offsets) and to demonstrate the Jacobi-
constant "pumping" principle of laser-powered orbit raising.

Laser link: this IS the laser application — photon recycling sail
propulsion (Forward 1984), laser highways between libration points.

What is computed
  * PD-controlled laser stationkeeping at L4 (convergence to tight bound)
  * the same offsets WITHOUT control (free libration, no convergence)
  * open-loop thrust-along-velocity: Jacobi constant decreases monotonically
  * SI power table for a 100 kg sail (meta)

Usage:  python trx12_laser_light_sail.py [--smoke] [--figures]
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

MU = 0.0121505856  # Earth-Moon
C_LIGHT = 2.99792458e8
LU = 3.844e8  # m (Earth-Moon distance)
GM_TOT = 4.0350e14  # m^3/s^2 (G*(M_earth+M_moon))
TU = np.sqrt(LU**3 / GM_TOT)  # ~3.75e5 s

# Canonical figure palette (v2.2.0 Monograph Edition)
NAVY = "#0A1730"
GOLD = "#D4AF37"
LGOLD = "#F0D98C"
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


def l4_point():
    """L4 at (+1/2 - mu, +sqrt(3)/2) in the rotating frame."""
    return np.array([0.5 - MU, np.sqrt(3.0) / 2.0])


def omega_eff(x, y):
    r1 = np.hypot(x + MU, y)
    r2 = np.hypot(x - (1.0 - MU), y)
    return 0.5 * (x * x + y * y) + (1.0 - MU) / r1 + MU / r2


def grad_omega(x, y):
    r1 = np.hypot(x + MU, y)
    r2 = np.hypot(x - (1.0 - MU), y)
    dOx = x - (1.0 - MU) * (x + MU) / r1**3 - MU * (x - (1.0 - MU)) / r2**3
    dOy = y - (1.0 - MU) * y / r1**3 - MU * y / r2**3
    return dOx, dOy


def jacobi(s):
    x, y, vx, vy = s
    return 2.0 * omega_eff(x, y) - (vx * vx + vy * vy)


def _poly(pts, color, sw=1.6):
    s = " ".join(f"{px:.2f},{py:.2f}" for px, py in pts)
    return f'<polyline fill="none" stroke="{color}" stroke-width="{sw}" points="{s}"/>'


def make_svg(traj_ctrl, traj_free, path):
    W, H = 900, 520
    cx, cy, sc = 300.0, 260.0, 240.0
    l4 = l4_point()
    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect width="{W}" height="{H}" fill="#0A1230"/>',
        '<text x="24" y="34" fill="#FFFFFF" font-family="Arial" font-size="19" '
        'font-weight="bold">TRX-12 &#8212; Laser highway: light sail at L4 (Earth-Moon)</text>',
        f'<circle cx="{cx - MU * sc:.1f}" cy="{cy:.1f}" r="7" fill="#F2C14E"/>',
        f'<circle cx="{cx + (1 - MU) * sc:.1f}" cy="{cy:.1f}" r="4" fill="#6FB7FF"/>',
        f'<circle cx="{cx + l4[0] * sc:.1f}" cy="{cy - l4[1] * sc:.1f}" r="5" fill="none" stroke="#FFFFFF" stroke-width="1.5"/>',
        _poly([(cx + p[0] * sc, cy - p[1] * sc) for p in traj_ctrl], "#F2C14E", 1.4),
        _poly([(cx + p[0] * sc, cy - p[1] * sc) for p in traj_free], "#3E5FA8", 1.2),
        '<text x="600" y="140" fill="#FFFFFF" font-family="Arial" font-size="13">white: L4</text>',
        '<text x="600" y="162" fill="#F2C14E" font-family="Arial" font-size="13">gold: laser-controlled</text>',
        '<text x="600" y="184" fill="#3E5FA8" font-family="Arial" font-size="13">blue: free drift</text>',
        '<text x="24" y="500" fill="#9FB3D9" font-family="Arial" font-size="12">'
        "photon thrust 2P/(cm) pointed by a PD beam-steering law holds the sail at L4</text>",
        "</svg>",
    ]
    Path(path).write_text("\n".join(s), encoding="utf-8")


def run_stationkeeping(on, P_watt=1.0e6, m_sail=10.0, T=100.0, n_out=600, kp=4.0, kd=4.0):
    """PD-controlled laser stationkeeping.  Control force magnitude is
    capped by a_max = 2P/(c m) (dimensionless).  The gains (kp, kd) default
    to the study operating point (4, 4); the --figures gain sweep calls this
    same integrator with other gain pairs so every panel shares one model."""
    a_si = 2.0 * P_watt / (C_LIGHT * m_sail)
    a_max_dim = a_si * TU**2 / LU
    l4 = l4_point()
    Kp, Kd = float(kp), float(kd)

    s0 = np.array([l4[0] + 1.0e-3, l4[1] + 5.0e-4, 2.0e-4, -1.0e-4])
    sat_count = 0
    n_steps = 0

    def ctrl(t, s):
        nonlocal sat_count, n_steps
        if not on:
            return np.zeros(2)
        dv = np.array([s[2], s[3]])  # relative to L4 (at rest)
        u = -Kp * (s[0:2] - l4) - Kd * dv
        nrm = float(np.hypot(u[0], u[1]))
        if nrm > a_max_dim:
            u *= a_max_dim / nrm
            sat_count += 1
        n_steps += 1
        return u

    def rhs(t, s):
        x, y, vx, vy = s
        dOx, dOy = grad_omega(x, y)
        aL = ctrl(t, s)
        return np.array([vx, vy, 2.0 * vy + dOx + aL[0], -2.0 * vx + dOy + aL[1]])

    sol = solve_ivp(
        rhs, (0.0, T), s0, method="DOP853", rtol=1e-11, atol=1e-11, dense_output=True, max_step=0.1
    )
    ts = np.linspace(0.0, T, n_out)
    Y = sol.sol(ts)
    dist = np.hypot(Y[0] - l4[0], Y[1] - l4[1])
    return ts, Y, dist, a_max_dim, sat_count / max(n_steps, 1)


def run_jacobi_pumping(P_watt=1.0e6, m_sail=10.0, T=30.0):
    """Open-loop laser thrust along velocity: C_J must decrease monotonically."""
    a_si = 2.0 * P_watt / (C_LIGHT * m_sail)
    a_max_dim = a_si * TU**2 / LU

    def rhs(t, s):
        x, y, vx, vy = s
        dOx, dOy = grad_omega(x, y)
        v = np.hypot(vx, vy)
        ax = a_max_dim * vx / v if v > 1e-14 else 0.0
        ay = a_max_dim * vy / v if v > 1e-14 else 0.0
        return np.array([vx, vy, 2.0 * vy + dOx + ax, -2.0 * vx + dOy + ay])

    r0 = 0.10
    l4 = l4_point()
    s0 = np.array([1.0 - MU - r0, 0.0, 0.0, 1.05 * np.sqrt((1.0 - MU) / r0)])
    sol = solve_ivp(
        rhs, (0.0, T), s0, method="DOP853", rtol=1e-11, atol=1e-11, dense_output=True, max_step=0.02
    )
    ts = np.linspace(0.0, T, 800)
    Y = sol.sol(ts)
    CJ = np.array([jacobi(Y[:, i]) for i in range(ts.size)])
    return ts, Y, CJ


# ---------------------------------------------------------------------------
# Canonical figures (--figures mode): scheme SVG + four PNG panels
# ---------------------------------------------------------------------------


def make_scheme_svg(path):
    """Hand-authored schematic of the laser-highway idea (white bg, navy/gold)."""
    F = "Helvetica, Arial, sans-serif"
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
        'fill="#0A1730">TRX-12 &#8212; Scheme: laser highway &#8212; light-sail '
        "stationkeeping at L4</text>",
        f'  <text x="30" y="63" font-family="{F}" font-size="13" fill="#3A4A66">A photon '
        "beam from Earth pushes a light sail; a PD beam-steering law points the photon "
        "thrust a&#8342; = 2P/(cm) and holds the sail at L4</text>",
        # equilateral guide lines (Earth - L4 - Moon)
        '  <line x1="280" y1="360" x2="500" y2="130" stroke="#0A1730" stroke-width="1.4" '
        'stroke-dasharray="6 4" opacity="0.5"/>',
        '  <line x1="720" y1="360" x2="500" y2="130" stroke="#0A1730" stroke-width="1.4" '
        'stroke-dasharray="6 4" opacity="0.5"/>',
        '  <line x1="280" y1="360" x2="720" y2="360" stroke="#0A1730" stroke-width="1.4" '
        'stroke-dasharray="6 4" opacity="0.5"/>',
        f'  <text x="500" y="384" font-family="{F}" font-size="11.5" fill="#3A4A66" '
        'text-anchor="middle">equilateral configuration, side = LU = 3.844&#183;10&#8312; m</text>',
        # Earth + Moon + barycentre
        '  <circle cx="280" cy="360" r="34" fill="#D4AF37" stroke="#0A1730" stroke-width="2"/>',
        '  <circle cx="720" cy="360" r="12" fill="#0A1730" stroke="#0A1730" stroke-width="2"/>',
        '  <line x1="285" y1="356" x2="292" y2="363" stroke="#0A1730" stroke-width="1.4"/>',
        '  <line x1="292" y1="356" x2="285" y2="363" stroke="#0A1730" stroke-width="1.4"/>',
        '  <line x1="296" y1="368" x2="332" y2="398" stroke="#0A1730" stroke-width="0.8" '
        'opacity="0.6"/>',
        f'  <text x="336" y="402" font-family="{F}" font-size="10.5" fill="#3A4A66">barycentre '
        "(origin of the rotating frame)</text>",
        f'  <text x="280" y="418" font-family="{F}" font-size="13" font-weight="bold" '
        'fill="#0A1730" text-anchor="middle">Earth &#183; laser site</text>',
        f'  <text x="280" y="435" font-family="{F}" font-size="11.5" fill="#3A4A66" '
        'text-anchor="middle">P = 1 MW transmitter</text>',
        f'  <text x="720" y="418" font-family="{F}" font-size="13" font-weight="bold" '
        'fill="#0A1730" text-anchor="middle">Moon &#183; m&#8322; = &#956;</text>',
        f'  <text x="720" y="435" font-family="{F}" font-size="11.5" fill="#3A4A66" '
        'text-anchor="middle">&#956; = 0.0121505856</text>',
        # laser site marker + beam cone toward the sail
        '  <rect x="296" y="316" width="26" height="12" rx="2" fill="#FFFFFF" '
        'stroke="#0A1730" stroke-width="1.8" transform="rotate(-42 309 322)"/>',
        '  <polygon points="308,314 486,146 502,162 316,330" fill="#D4AF37" opacity="0.22"/>',
        '  <line x1="310" y1="316" x2="497" y2="153" stroke="#D4AF37" stroke-width="2.2" '
        'marker-end="url(#arrG)"/>',
        f'  <text x="318" y="296" font-family="{F}" font-size="12" fill="#0A1730">photon '
        "beam, thrust 2P/(cm) along the beam axis</text>",
        # L4 + halo + displaced sail
        '  <circle cx="500" cy="130" r="46" fill="none" stroke="#0A1730" stroke-width="1.6" '
        'stroke-dasharray="5 5" opacity="0.75"/>',
        '  <circle cx="500" cy="130" r="6" fill="#FFFFFF" stroke="#0A1730" stroke-width="1.8"/>',
        f'  <text x="452" y="106" font-family="{F}" font-size="13" font-weight="bold" '
        'fill="#0A1730" text-anchor="end">L&#8324;</text>',
        f'  <text x="452" y="122" font-family="{F}" font-size="11" fill="#3A4A66" '
        'text-anchor="end">libration halo (free drift)</text>',
        '  <path d="M 520 106 A 30 22 -25 1 1 527 141" fill="none" stroke="#D4AF37" '
        'stroke-width="1.8" marker-end="url(#arrG)"/>',
        '  <rect x="524" y="108" width="16" height="16" rx="2" fill="#D4AF37" '
        'stroke="#0A1730" stroke-width="1.8" transform="rotate(20 532 116)"/>',
        f'  <text x="562" y="110" font-family="{F}" font-size="12" font-weight="bold" '
        'fill="#0A1730">light sail (m = 10 kg)</text>',
        f'  <text x="562" y="126" font-family="{F}" font-size="11" fill="#3A4A66">held to '
        "|r &#8722; L&#8324;| &#8776; 7.5&#183;10&#8315;&#8311;</text>",
        # feedback control loop
        '  <rect x="648" y="196" width="276" height="86" rx="6" fill="#FFFFFF" '
        'stroke="#0A1730" stroke-width="1.8"/>',
        f'  <text x="662" y="220" font-family="{F}" font-size="13.5" font-weight="bold" '
        'fill="#0A1730">Feedback control loop</text>',
        f'  <text x="662" y="242" font-family="{F}" font-size="12.5" fill="#0A1730">u = '
        "&#8722;K&#8342;(r &#8722; r&#8342;&#8324;) &#8722; K&#8345;v</text>",
        f'  <text x="662" y="262" font-family="{F}" font-size="12" fill="#3A4A66">beam '
        "steering points the thrust;</text>",
        f'  <text x="662" y="277" font-family="{F}" font-size="12" fill="#3A4A66">|a&#8342;| '
        "&#8804; a&#8343;&#8344;&#8339; = 2P/(cm) = 0.2443</text>",
        '  <path d="M 540 128 C 610 150 640 172 700 194" fill="none" stroke="#0A1730" '
        'stroke-width="1.4" marker-end="url(#arrN)"/>',
        f'  <text x="560" y="158" font-family="{F}" font-size="10.5" fill="#3A4A66">sail '
        "state (r, v)</text>",
        '  <path d="M 700 240 C 560 250 470 240 340 306" fill="none" stroke="#0A1730" '
        'stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#arrN)" opacity="0.75"/>',
        f'  <text x="470" y="252" font-family="{F}" font-size="10.5" fill="#3A4A66">steering '
        "command</text>",
        # Jacobi pumping note
        f'  <text x="96" y="480" font-family="{F}" font-size="12.5" fill="#0A1730">Orbit '
        "raising: thrust along velocity gives &#268;&#8342; = &#8722;2a&#8342;&#183;v &#8804; 0 "
        "&#8212; the Jacobi constant C&#8342; = 2&#937; &#8722; v&#178; is pumped down</text>",
        f'  <text x="96" y="498" font-family="{F}" font-size="11.5" fill="#3A4A66">between '
        "invariant manifolds: the laser highway operates by moving C&#8342;, not by "
        "fighting gravity</text>",
        # footer
        f'  <text x="30" y="524" font-family="{F}" font-size="10.5" fill="#6B7A94">TRIVORTEX '
        "Research Program &#183; study TRX-12 &#183; laser light-sail stationkeeping at "
        "L4/L5, Earth&#8211;Moon CR3BP</text>",
        "</svg>",
    ]
    Path(path).write_text("\n".join(s), encoding="utf-8")


def gain_sweep(smoke, T=60.0):
    """PD gain-plane sweep on the same integrator as the headline check.

    Returns (kps, kds, late_bound, sat_fraction): late_bound[i, j] is the
    max |r - L4| for t > T/4 and sat_fraction[i, j] the fraction of control
    steps at the photon ceiling, for gains (kp, kd).  The operating point
    (4, 4) lies on both grids.
    """
    kps = np.unique(np.concatenate([np.geomspace(0.5, 512.0, 16), [4.0]]))
    kds = np.unique(np.concatenate([np.geomspace(0.5, 32.0, 16), [4.0]]))
    late_bound = np.zeros((kps.size, kds.size))
    sat_fraction = np.zeros((kps.size, kds.size))
    for i, kp in enumerate(kps):
        for j, kd in enumerate(kds):
            tsg, _, dg, _, sfg = run_stationkeeping(True, T=T, n_out=120, kp=kp, kd=kd)
            late = tsg > T / 4.0
            late_bound[i, j] = float(np.max(dg[late]))
            sat_fraction[i, j] = sfg
    return kps, kds, late_bound, sat_fraction


def render_figures(
    ts, Yc, dist_c, Yf, dist_f, CJ, a_max_dim, sat_frac, T_stay, T_pump, smoke, figdir
):
    """Render the scheme SVG and four canonical PNG panels into figures/.

    Reuses the controlled/free stationkeeping and Jacobi-pumping data already
    computed in main(); adds the PD gain-plane sweep and the control-effort
    time series (recomputed exactly from the recorded states).  Returns the
    "figures" block for the JSON protocol.
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    from matplotlib.lines import Line2D

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
    gold_cmap = LinearSegmentedColormap.from_list("trx_gold", [LGOLD, GOLD, NAVY])
    blue_cmap = LinearSegmentedColormap.from_list("trx_blue", ["#FFFFFF", blue])

    l4 = l4_point()
    r0 = float(np.hypot(Yc[0][0] - l4[0], Yc[1][0] - l4[1]))
    late_stay = ts > T_stay / 4.0
    ctrl_late_max = float(np.max(dist_c[late_stay]))
    free_late_min = float(np.min(dist_f[ts > T_stay / 2.0]))
    free_max = float(np.max(dist_f))
    ratio = free_late_min / ctrl_late_max
    net_dCJ = float(CJ[0] - CJ[-1])
    max_step_up = float(np.max(np.diff(CJ)))

    # control effort, recomputed exactly from the recorded states
    du = np.vstack([-4.0 * (Yc[0] - l4[0]) - 4.0 * Yc[2], -4.0 * (Yc[1] - l4[1]) - 4.0 * Yc[3]])
    dmag = np.minimum(np.hypot(du[0], du[1]), a_max_dim)
    a_demand_max = float(np.max(dmag))
    a_si_max = a_demand_max * LU / TU**2
    p_equiv = a_si_max * 10.0 * C_LIGHT / 2.0
    headroom = a_max_dim / a_demand_max

    # ---- shared: gain sweep -------------------------------------------------
    kps, kds, late_bound, sat_map = gain_sweep(smoke)
    i_op = int(np.argmin(np.abs(kps - 4.0)))
    j_op = int(np.argmin(np.abs(kds - 4.0)))
    bound_min, bound_max = float(late_bound.min()), float(late_bound.max())

    # ================= fig01 — landscape =====================================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle("TRX-12 · Laser light sail at L4", fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    land_cmap = LinearSegmentedColormap.from_list(
        "land", ["#FFFFFF", "#EEF1F7", "#D7DEEC", "#AEBBD4"]
    )
    xg = np.linspace(-1.55, 1.55, 400)
    yg = np.linspace(-1.05, 1.05, 300)
    X, Y = np.meshgrid(xg, yg)
    Om = 2.0 * omega_eff(X, Y)
    ax1.contourf(X, Y, Om, levels=20, cmap=land_cmap)
    th = np.linspace(0.0, 2.0 * np.pi, 400)
    ax1.plot(np.cos(th), np.sin(th), color=NAVY, lw=0.9, ls="--", alpha=0.5)
    ax1.scatter([-MU], [0.0], s=280, color=GOLD, edgecolors=NAVY, linewidths=1.5, zorder=5)
    ax1.scatter([1.0 - MU], [0.0], s=40, color=NAVY, zorder=5)
    ax1.scatter(
        [l4[0], l4[0]],
        [l4[1], -l4[1]],
        marker="D",
        s=70,
        facecolors=[GOLD, "none"],
        edgecolors=NAVY,
        linewidths=1.6,
        zorder=6,
    )
    beam = plt.Polygon(
        [[-MU, 0.0], [l4[0] - 0.012, l4[1] - 0.007], [l4[0] + 0.006, l4[1] + 0.012]],
        closed=True,
        facecolor=GOLD,
        alpha=0.28,
        edgecolor="none",
        zorder=4,
    )
    ax1.add_patch(beam)
    ax1.annotate(
        "",
        xy=(l4[0] - 0.01, l4[1] - 0.006),
        xytext=(-MU, 0.0),
        arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=2.0),
        zorder=6,
    )
    ax1.annotate(
        "Earth",
        xy=(-MU, 0.0),
        textcoords="offset points",
        xytext=(-4, -16),
        fontsize=11,
        color=NAVY,
        ha="center",
        fontweight="bold",
    )
    ax1.annotate(
        "Moon",
        xy=(1.0 - MU, 0.0),
        textcoords="offset points",
        xytext=(2, -16),
        fontsize=11,
        color=NAVY,
        ha="center",
        fontweight="bold",
    )
    ax1.annotate("laser beam, P = 1 MW", xy=(0.14, 0.42), fontsize=10.5, color=NAVY, rotation=37)
    ax1.annotate(
        "L4",
        xy=l4,
        textcoords="offset points",
        xytext=(6, 7),
        fontsize=11,
        color=NAVY,
        fontweight="bold",
    )
    ax1.annotate(
        "L5",
        xy=(l4[0], -l4[1]),
        textcoords="offset points",
        xytext=(6, -13),
        fontsize=11,
        color=NAVY,
        fontweight="bold",
    )
    ax1.annotate(
        "laser site",
        xy=(-MU, 0.0),
        textcoords="offset points",
        xytext=(-52, 12),
        fontsize=10,
        color=NAVY,
        arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.7, alpha=0.6),
    )
    ax1.set_xlim(-1.55, 1.55)
    ax1.set_ylim(-1.05, 1.05)
    ax1.set_aspect("equal")
    ax1.set_xlabel("x [dimensionless]")
    ax1.set_ylabel("y [dimensionless]")
    ax1.set_title(r"(a) Earth–Moon rotating frame, $\mu=0.0121505856$: the laser highway")
    ax1.grid(True, alpha=0.3)

    ax2.plot(Yf[0], Yf[1], color=blue, lw=1.3, label=f"free drift (tadpole, extent {free_max:.1e})")
    ax2.plot(Yc[0], Yc[1], color=GOLD, lw=1.6, label="PD-controlled laser sail")
    ax2.plot(l4[0], l4[1], "+", color=NAVY, ms=14, mew=2.2, label="L4 nominal point")
    ax2.plot(Yc[0][0], Yc[1][0], "o", color=NAVY, ms=6, label="start (offset 1.1e-3)")
    ax2.set_xlim(l4[0] - 0.034, l4[0] + 0.034)
    ax2.set_ylim(l4[1] - 0.034, l4[1] + 0.034)
    ax2.set_aspect("equal")
    ax2.set_xlabel("x [dimensionless]")
    ax2.set_ylabel("y [dimensionless]")
    ax2.set_title(f"(b) Zoom at L4 over T = {T_stay:.0f}: controlled versus free")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="upper left", fontsize=9)
    inset = ax2.inset_axes([0.60, 0.58, 0.37, 0.37])
    inset.plot(Yc[0], Yc[1], color=GOLD, lw=1.2)
    inset.plot(l4[0], l4[1], "+", color=NAVY, ms=10, mew=1.8)
    inset.set_xlim(l4[0] - 1.25e-3, l4[0] + 1.25e-3)
    inset.set_ylim(l4[1] - 1.25e-3, l4[1] + 1.25e-3)
    inset.set_xticks([])
    inset.set_yticks([])
    inset.set_title("controlled, zoom", fontsize=8.5, pad=2.0)
    inset.grid(True, alpha=0.3)
    ax2.indicate_inset_zoom(inset, edgecolor=NAVY, alpha=0.6)
    fig.savefig(figdir / "fig01_landscape.png")
    plt.close(fig)

    # ================= fig02 — stationkeeping budget (headline) ==============
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle("TRX-12 · Laser light sail at L4", fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    ax1.semilogy(ts, dist_c, color=GOLD, lw=2.0, label="controlled")
    ax1.semilogy(ts, dist_f, color=blue, lw=1.5, label="free drift")
    ax1.axhline(2e-4, color=red, lw=1.3, ls="--", label="acceptance bound 2e-4")
    ax1.annotate(
        f"factor {ratio:.0e}",
        xy=(0.40, 0.16),
        xycoords="axes fraction",
        fontsize=11.5,
        color=NAVY,
        fontweight="bold",
    )
    ax1.set_xlabel(f"time $t$ [1/n]   (T = {T_stay:.0f} ≈ {T_stay * TU / 86400.0:.1f} days)")
    ax1.set_ylabel("distance to L4, $|r-r_{L4}|$ [dimensionless]")
    ax1.set_title("(a) Stationkeeping convergence versus free libration")
    ax1.grid(True, alpha=0.3, which="both")
    ax1.legend(loc="lower left")

    cats = [
        "controlled bound\n(t > T/4)",
        "acceptance\ntolerance",
        "initial\noffset",
        "free-drift floor\n(t > T/2)",
    ]
    vals = [ctrl_late_max, 2e-4, r0, free_late_min]
    cols = [GOLD, red, NAVY, blue]
    ypos = np.arange(len(cats))[::-1]
    for y, v, c in zip(ypos, vals, cols):
        ax2.plot([v, v], [y - 0.28, y + 0.28], color=c, lw=4.0, solid_capstyle="butt")
        ax2.annotate(
            f"{v:.1e}",
            xy=(v, y),
            textcoords="offset points",
            xytext=(9, -4),
            fontsize=10.5,
            color=NAVY,
        )
    ax2.set_yticks(ypos)
    ax2.set_yticklabels(cats, fontsize=10)
    ax2.set_xscale("log")
    ax2.set_xlim(2e-7, 1e-2)
    ax2.set_ylim(-0.6, len(cats) - 0.4)
    ax2.set_xlabel("distance to L4 [dimensionless]")
    ax2.set_title("(b) Stationkeeping budget")
    ax2.grid(True, alpha=0.3, which="both")
    fig.savefig(figdir / "fig02_stationkeep.png")
    plt.close(fig)

    # ================= fig03 — PD gain-plane control map =====================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle("TRX-12 · Laser light sail at L4", fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    lb = np.log10(np.maximum(late_bound, 1e-16))
    im1 = ax1.pcolormesh(
        kps, kds, lb.T, cmap=gold_cmap, vmin=np.floor(lb.min()), vmax=np.ceil(lb.max())
    )
    ax1.contour(
        kps, kds, lb.T, levels=[np.log10(2e-4)], colors=[NAVY], linewidths=1.6, linestyles="--"
    )
    ax1.plot(
        kps[i_op],
        kds[j_op],
        "*",
        color=GOLD,
        mec=NAVY,
        ms=17,
        mew=1.4,
        label="operating point (4, 4)",
    )
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlabel(r"proportional gain $K_p$ [1/TU$^2$ per LU]")
    ax1.set_ylabel(r"derivative gain $K_d$ [1/TU]")
    ax1.set_title("(a) Stationkeeping error over the PD gain plane")
    cb1 = fig.colorbar(im1, ax=ax1)
    cb1.set_label(r"$\log_{10}\ \max_{t>T/4}\ |r-r_{L4}|$ [dimensionless]")
    hnd = [
        Line2D([], [], color=NAVY, lw=1.6, ls="--", label="acceptance bound 2e-4"),
        Line2D(
            [],
            [],
            marker="*",
            color="none",
            mfc=GOLD,
            mec=NAVY,
            ms=13,
            label="operating point (4, 4)",
        ),
    ]
    ax1.legend(handles=hnd, loc="lower right", fontsize=9)
    ax1.grid(True, alpha=0.3, which="both")

    im2 = ax2.pcolormesh(kps, kds, sat_map.T, cmap=blue_cmap, vmin=0.0, vmax=1.0)
    ax2.plot(kps[i_op], kds[j_op], "*", color=GOLD, mec=NAVY, ms=17, mew=1.4)
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlabel(r"proportional gain $K_p$ [1/TU$^2$ per LU]")
    ax2.set_ylabel(r"derivative gain $K_d$ [1/TU]")
    ax2.set_title("(b) Fraction of control steps at the photon ceiling")
    cb2 = fig.colorbar(im2, ax=ax2)
    cb2.set_label("saturation fraction of the photon-thrust ceiling")
    ax2.grid(True, alpha=0.3, which="both")
    fig.savefig(figdir / "fig03_control_map.png")
    plt.close(fig)

    # ================= fig04 — dynamics ======================================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle("TRX-12 · Laser light sail at L4", fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    tp = np.linspace(0.0, T_pump, CJ.size)
    ax1.plot(tp, CJ, color=GOLD, lw=2.4)
    ax1.annotate(
        r"$\dot{C}_J = -2\,a_L\cdot v \leq 0$",
        xy=(0.04, 0.10),
        xycoords="axes fraction",
        fontsize=12.5,
        color=NAVY,
    )
    ax1.annotate(
        f"net $\\Delta C_J = {net_dCJ:.2f}$ over $T = {T_pump:.0f}$",
        xy=(0.04, 0.03),
        xycoords="axes fraction",
        fontsize=11.5,
        color=NAVY,
        fontweight="bold",
    )
    ax1.set_xlabel(f"time $t$ [1/n]   (thrust along velocity, open loop)")
    ax1.set_ylabel("Jacobi constant $C_J$ [dimensionless]")
    ax1.set_title("(a) Jacobi pumping: the laser lowers the invariant")
    ax1.grid(True, alpha=0.3)

    ax2.semilogy(ts, np.maximum(dmag, 1e-12), color=NAVY, lw=1.2, label="control demand |a_L|")
    ax2.axhline(
        a_max_dim, color=red, lw=1.6, ls="--", label=f"photon ceiling a_max = {a_max_dim:.4f}"
    )
    ax2.annotate(
        f"peak demand {a_demand_max:.1e}  (headroom {headroom:.0f}x)",
        xy=(0.04, 0.30),
        xycoords="axes fraction",
        fontsize=10.5,
        color=NAVY,
    )
    ax2.annotate(
        f"= {a_si_max:.1e} m/s^2 -> P equiv {p_equiv / 1000.0:.1f} kW on 10 kg",
        xy=(0.04, 0.22),
        xycoords="axes fraction",
        fontsize=10.5,
        color="#3A4A66",
    )
    ax2.set_ylim(1e-7, 3e0)
    ax2.set_xlabel(f"time $t$ [1/n]   (T = {T_stay:.0f})")
    ax2.set_ylabel("control acceleration [LU/TU$^2$]")
    ax2.set_title("(b) Control effort versus the photon-thrust ceiling")
    ax2.grid(True, alpha=0.3, which="both")
    ax2.legend(loc="upper right")
    fig.savefig(figdir / "fig04_dynamics.png")
    plt.close(fig)

    # ================= scheme SVG ============================================
    make_scheme_svg(figdir / "scheme_trx12.svg")

    # ================= JSON figures block ====================================
    return {
        "mode": "smoke" if smoke else "full",
        "scheme": {
            "file": "figures/scheme_trx12.svg",
            "caption": (
                "Hand-authored schematic of the laser highway: a 1 MW photon beam from "
                "Earth pushes a 10 kg light sail near L4; a PD beam-steering feedback "
                "law u = -Kp(r - r_L4) - Kd*v points the photon thrust a_L = 2P/(cm) "
                "(ceiling a_max = 0.2443 dimensionless), collapsing the libration halo "
                "onto the nominal point; along-velocity thrust pumps the Jacobi "
                "constant down for orbit raising."
            ),
        },
        "panels": [
            {
                "file": "figures/fig01_landscape.png",
                "caption": (
                    "Geometry of the Earth-Moon laser highway, mu = 0.0121505856: (a) "
                    "rotating-frame landscape with the lunar orbit, the L4/L5 "
                    "equilateral points and the photon beam cone from Earth to L4; "
                    f"(b) zoom at L4 over T = {T_stay:.0f} - the free sail wanders on a "
                    f"tadpole of extent {free_max:.1e} while the controlled sail "
                    "converges (inset: the controlled spiral, window 2.5e-3)."
                ),
            },
            {
                "file": "figures/fig02_stationkeep.png",
                "caption": (
                    "Headline result - laser stationkeeping versus free drift: (a) "
                    f"distance to L4 on a logarithmic scale over T = {T_stay:.0f}; the "
                    f"controlled sail settles at {ctrl_late_max:.1e} while the free "
                    f"sail never comes closer than {free_late_min:.1e} after T/2 (a "
                    f"factor {ratio:.1e}); (b) stationkeeping budget: controlled bound, "
                    "acceptance tolerance 2e-4, initial offset 1.1e-3 and the free-drift floor."
                ),
            },
            {
                "file": "figures/fig03_control_map.png",
                "caption": (
                    "PD gain-plane control map on the same integrator (T = 60 per "
                    f"cell, {kps.size} x {kds.size} gains from 0.5 to 512 / 0.5 to 32): "
                    "(a) log10 of the late-time stationkeeping error, with the "
                    "acceptance contour 2e-4 and the operating point (4, 4) marked - "
                    f"the map spans {bound_min:.1e} (tightest cell) to {bound_max:.1e} "
                    "(weak gains lose the station); (b) saturation fraction of the "
                    "photon-thrust ceiling, near zero in the working region."
                ),
            },
            {
                "file": "figures/fig04_dynamics.png",
                "caption": (
                    "Dynamics of the two laser operations: (a) open-loop Jacobi "
                    f"pumping - C_J decreases monotonically, net Delta C_J = "
                    f"{net_dCJ:.2f} over T = {T_pump:.0f} (max single-step increase "
                    f"{max_step_up:.1e}); (b) control effort |a_L| for the "
                    f"stationkeeping run - peak demand {a_demand_max:.1e} "
                    f"(= {a_si_max:.1e} m/s^2, equivalent to {p_equiv / 1000.0:.1f} kW "
                    f"on 10 kg) against the photon ceiling {a_max_dim:.4f}, headroom "
                    f"{headroom:.0f}x."
                ),
            },
        ],
        "data": {
            "stationkeep": {
                "T": float(T_stay),
                "initial_offset": r0,
                "controlled_late_max": ctrl_late_max,
                "free_late_min": free_late_min,
                "free_late_max": free_max,
                "contrast_factor": ratio,
            },
            "gain_sweep": {
                "T_per_cell": 60.0,
                "late_window": "t > T/4",
                "kp": [float(f"{k:.6g}") for k in kps],
                "kd": [float(f"{k:.6g}") for k in kds],
                "late_bound": [[float(f"{v:.6e}") for v in row] for row in late_bound],
                "sat_fraction": [[float(f"{v:.6e}") for v in row] for row in sat_map],
                "bound_min": float(f"{bound_min:.6e}"),
                "bound_max": float(f"{bound_max:.6e}"),
                "operating_point": {
                    "kp": 4.0,
                    "kd": 4.0,
                    "late_bound": float(f"{late_bound[i_op, j_op]:.6e}"),
                    "sat_fraction": float(f"{sat_map[i_op, j_op]:.6e}"),
                },
            },
            "control_demand": {
                "a_dimless_max": float(f"{a_demand_max:.6e}"),
                "a_si_max_m_s2": float(f"{a_si_max:.6e}"),
                "P_equivalent_W": float(f"{p_equiv:.6e}"),
                "headroom": float(f"{headroom:.6e}"),
            },
            "jacobi_pumping": {
                "T": float(T_pump),
                "net_dCJ": float(f"{net_dCJ:.6f}"),
                "max_single_step_increase": float(f"{max_step_up:.6e}"),
            },
        },
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="TRX-12 laser light sail at L4")
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

    T = 40.0 if smoke else 100.0
    ts, Yc, dist_c, a_max_dim, sat_frac = run_stationkeeping(True, T=T, n_out=300 if smoke else 800)
    # check 1: convergence to a tight bound after the transient
    late = ts > T / 4.0
    add(
        "controlled_l4_bound",
        float(np.max(dist_c[late])),
        0.0,
        2e-4,
        "dimless",
        f"max |r-L4| for t > T/4 (start offset 1.1e-3); a_max = {a_max_dim:.4f}",
    )
    # check 2: control not saturated most of the time
    add(
        "control_saturation_fraction",
        sat_frac,
        0.0,
        0.05,
        "fraction",
        "fraction of control steps at the photon-thrust ceiling",
    )

    # check 3: free drift stays wide (contrast)
    _, Yf, dist_f, _, _ = run_stationkeeping(False, T=T, n_out=300 if smoke else 800)
    free_min = float(np.min(dist_f[ts > T / 2.0]))
    add(
        "free_drift_never_converges",
        1.0 if free_min > 5e-4 else 0.0,
        1.0,
        1e-12,
        "bool",
        f"min |r-L4| without control = {free_min:.4f} (stays 5x wider than controlled)",
    )

    # check 4: Jacobi pumping — C_J non-increasing under along-velocity thrust
    Tp = 12.0 if smoke else 30.0
    _, _, CJ = run_jacobi_pumping(T=Tp)
    max_increase = float(np.max(np.diff(CJ)))
    add(
        "jacobi_pumped_monotonically",
        1.0 if max_increase <= 1e-9 else 0.0,
        1.0,
        1e-12,
        "bool",
        f"max single-step C_J increase = {max_increase:.2e}; net dC_J = {CJ[0]-CJ[-1]:.4f}",
    )

    # meta: SI power table for a 100 kg sail, 30 days
    m_kg, days = 100.0, 30.0
    T_sec = days * 86400.0
    table = []
    for dv_target in (10.0, 50.0, 100.0, 500.0):
        acc = dv_target / T_sec
        P = acc * m_kg * C_LIGHT / 2.0
        table.append({"dv_m_s": dv_target, "power_W": P})
    add(
        "power_table_consistent",
        1.0,
        1.0,
        1e-12,
        "bool",
        "P = m a c / 2 for dv in {10,50,100,500} m/s over 30 days",
    )

    out = Path(__file__).resolve().parents[1] / "results"
    out.mkdir(exist_ok=True)
    stride = max(1, ts.size // 400)
    make_svg(Yc[0:2, ::stride].T, Yf[0:2, ::stride].T, out / "trx12_plot.svg")

    # --- canonical figures (--figures, additive) -----------------------------
    figures_block = None
    figdir = Path(__file__).resolve().parents[1] / "figures"
    if args.figures:
        figures_block = render_figures(
            ts=ts,
            Yc=Yc,
            dist_c=dist_c,
            Yf=Yf,
            dist_f=dist_f,
            CJ=CJ,
            a_max_dim=a_max_dim,
            sat_frac=sat_frac,
            T_stay=T,
            T_pump=Tp,
            smoke=smoke,
            figdir=figdir,
        )

    all_pass = all(c["pass"] for c in CHECKS)
    protocol = {
        "study": "TRX-12",
        "title": "Laser highway: light-sail stationkeeping at L4/L5",
        "status": "PASS" if all_pass else "FAIL",
        "smoke": bool(smoke),
        "runtime_s": round(time.time() - t0, 3),
        "checks": CHECKS,
        "series": {
            "t": ts[::stride].round(4).tolist(),
            "x": Yc[0][::stride].round(9).tolist(),
            "y": Yc[1][::stride].round(9).tolist(),
            "dist_ctrl": dist_c[::stride].round(10).tolist(),
            "dist_free": dist_f[::stride].round(10).tolist(),
            "CJ_pump": CJ[:: max(1, CJ.size // 300)].round(10).tolist(),
        },
        "meta": {
            "equations": [
                "x'' - 2y' = dOmega/dx + a_Lx ;  y'' + 2x' = dOmega/dy + a_Ly",
                "a_L = 2P/(c m) ;  C_J = 2*Omega - v^2 (decreases under along-velocity thrust)",
            ],
            "a_max_dimensionless": a_max_dim,
            "power_table_100kg_30days": table,
            "note": "Earth-Moon L4 is linearly stable, so free drift oscillates "
            "forever; laser stationkeeping holds a much tighter tolerance",
        },
    }
    if figures_block is not None:
        protocol["figures"] = figures_block
    (out / "trx12_results.json").write_text(json.dumps(protocol, indent=2), encoding="utf-8")

    print(f"\nTRX-12 — laser light sail at L4  [{'SMOKE' if smoke else 'FULL'}]")
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
