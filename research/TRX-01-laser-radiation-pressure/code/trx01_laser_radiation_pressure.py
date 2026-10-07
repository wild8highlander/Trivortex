#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
TRIVORTEX LAB — TRX-01 — RADIATION-PRESSURE RESTRICTED THREE-BODY PROBLEM
============================================================================
The circular restricted three-body problem (CR3BP) in which primary 1 is
illuminated by an intense laser beam, so that photon radiation pressure
reduces its effective pull on a massless particle by the factor (1-beta),
beta = F_rad / F_grav.  This is the "laser-dressed" CR3BP: the laser acts
as a third physical agent that reshapes the libration-point landscape.

What is computed
  * L1, L2, L3, L4, L5 equilibrium points for beta in {0, 0.01, 0.05, 0.1}
  * linear stability eigenvalues of the L4 analogue
  * Jacobi-integral conservation along an orbit near L4 (beta = 0.05)
  * laser scenario table: beta for a micron dust grain at 1 AU
  * with --figures: hand-authored scheme SVG + four canonical PNG panels
    (300 dpi) into figures/, and a "figures" block added to the JSON protocol

Usage:  python trx01_laser_radiation_pressure.py [--smoke] [--figures]
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
from scipy.optimize import brentq

MU = 0.0121505856  # Earth-Moon mass parameter
BETAS = (0.0, 0.01, 0.05, 0.1)

NAVY = "#0A1730"  # TRIVORTEX palette: strokes and text
GOLD = "#D4AF37"  # TRIVORTEX palette: accents
LIGHT_GOLD = "#F0D98C"  # TRIVORTEX palette: soft fills
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
# Dynamics
# ---------------------------------------------------------------------------


def omega_eff(x, y, beta):
    """Effective potential (incl. centrifugal term) of the laser-dressed CR3BP."""
    r1 = np.hypot(x + MU, y)  # distance to primary 1 at (-mu, 0)
    r2 = np.hypot(x - (1.0 - MU), y)  # distance to primary 2 at (1-mu, 0)
    return 0.5 * (x * x + y * y) + (1.0 - beta) * (1.0 - MU) / r1 + MU / r2


def grad_omega(x, y, beta):
    r1 = np.hypot(x + MU, y)
    r2 = np.hypot(x - (1.0 - MU), y)
    dOx = x - (1.0 - beta) * (1.0 - MU) * (x + MU) / r1**3 - MU * (x - (1.0 - MU)) / r2**3
    dOy = y - (1.0 - beta) * (1.0 - MU) * y / r1**3 - MU * y / r2**3
    return dOx, dOy


def eom(t, s, beta):
    x, y, vx, vy = s
    dOx, dOy = grad_omega(x, y, beta)
    return [vx, vy, 2.0 * vy + dOx, -2.0 * vx + dOy]


def jacobi(s, beta):
    x, y, vx, vy = s
    return 2.0 * omega_eff(x, y, beta) - (vx * vx + vy * vy)


# ---------------------------------------------------------------------------
# Equilibrium points
# ---------------------------------------------------------------------------


def collinear_point(beta, lo, hi):
    """Root of dOmega/dx on the x-axis inside a physically chosen bracket."""
    f = lambda x: grad_omega(x, 0.0, beta)[0]
    return brentq(f, lo, hi, xtol=1e-15, rtol=8.9e-16, maxiter=200)


def triangular_point(beta, sign):
    """2-D root of grad(Omega)=0 near the equilateral Lagrange point."""
    from scipy.optimize import root

    sol = root(
        lambda p: grad_omega(p[0], sign * p[1], beta),
        [0.5 - MU, sign * np.sqrt(3.0) / 2.0],
        tol=1e-13,
    )
    if not sol.success or float(np.max(np.abs(sol.fun))) > 1e-10:
        raise RuntimeError(f"triangular root not found (beta={beta}, sign={sign})")
    return float(sol.x[0]), float(sign * sol.x[1])


def stability_matrix(pt, beta):
    """Linearised CR3BP matrix at an equilibrium point."""
    x, y = pt
    r1 = np.hypot(x + MU, y)
    r2 = np.hypot(x - (1.0 - MU), y)
    g1 = (1.0 - beta) * (1.0 - MU)
    g2 = MU
    Oxx = (
        1.0
        - g1 * (1.0 / r1**3 - 3.0 * (x + MU) ** 2 / r1**5)
        - g2 * (1.0 / r2**3 - 3.0 * (x - (1.0 - MU)) ** 2 / r2**5)
    )
    Oyy = 1.0 - g1 * (1.0 / r1**3 - 3.0 * y**2 / r1**5) - g2 * (1.0 / r2**3 - 3.0 * y**2 / r2**5)
    Oxy = 3.0 * g1 * (x + MU) * y / r1**5 + 3.0 * g2 * (x - (1.0 - MU)) * y / r2**5
    return np.array(
        [[0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0], [Oxx, Oxy, 0.0, 2.0], [Oxy, Oyy, -2.0, 0.0]]
    )


# ---------------------------------------------------------------------------
# Laser scenario (SI units, informational)
# ---------------------------------------------------------------------------


def laser_beta_table():
    GMSUN = 1.32712440018e20  # m^3/s^2
    C = 2.99792458e8  # m/s
    AU = 1.495978707e11  # m
    lam, D, rho, Qpr, R = 1.0e-6, 1.0, 3000.0, 1.3, 1.0e-6
    w = 1.22 * lam * AU / D  # diffraction-limited beam waist at 1 AU
    area = np.pi * w * w
    m_grain = rho * 4.0 / 3.0 * np.pi * R**3
    F_grav = GMSUN * m_grain / AU**2
    table = []
    for P in (1.0e4, 1.0e5, 1.0e7):
        I = P / area
        F_rad = I * np.pi * R**2 * Qpr / C
        table.append(
            {
                "power_W": P,
                "intensity_W_m2": I,
                "F_rad_N": F_rad,
                "F_grav_N": F_grav,
                "beta": F_rad / F_grav,
            }
        )
    return {
        "wavelength_m": lam,
        "aperture_m": D,
        "grain_radius_m": R,
        "beam_waist_m_at_1AU": w,
        "cases": table,
    }


# ---------------------------------------------------------------------------
# SVG output
# ---------------------------------------------------------------------------


def _poly(pts, color, sw=1.6, op=1.0):
    s = " ".join(f"{px:.2f},{py:.2f}" for px, py in pts)
    return (
        f'<polyline fill="none" stroke="{color}" stroke-width="{sw}" opacity="{op}" points="{s}"/>'
    )


def make_svg(orb0, orb1, l4_0, l4_1, path):
    W, H = 900, 520
    cx, cy = W * 0.36, H / 2
    sc = 150.0
    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect width="{W}" height="{H}" fill="#0A1230"/>',
        '<text x="24" y="34" fill="#FFFFFF" font-family="Arial" font-size="19" '
        'font-weight="bold">TRX-01 &#8212; Laser-dressed CR3BP: orbit near L4</text>',
        f'<circle cx="{cx - MU * sc:.1f}" cy="{cy:.1f}" r="6" fill="#F2C14E"/>',
        f'<circle cx="{cx + (1 - MU) * sc:.1f}" cy="{cy:.1f}" r="4" fill="#6FB7FF"/>',
        f'<circle cx="{cx + l4_0[0] * sc:.1f}" cy="{cy - l4_0[1] * sc:.1f}" r="4" fill="none" stroke="#F2C14E" stroke-width="1.5"/>',
        f'<circle cx="{cx + l4_1[0] * sc:.1f}" cy="{cy - l4_1[1] * sc:.1f}" r="4" fill="none" stroke="#6FB7FF" stroke-width="1.5"/>',
        _poly([(cx + px * sc, cy - py * sc) for px, py in orb0], "#F2C14E"),
        _poly([(cx + px * sc, cy - py * sc) for px, py in orb1], "#6FB7FF"),
        '<text x="24" y="470" fill="#F2C14E" font-family="Arial" font-size="14">gold: beta = 0 (classical CR3BP)</text>',
        '<text x="24" y="492" fill="#6FB7FF" font-family="Arial" font-size="14">blue: beta = 0.10 (laser radiation pressure on)</text>',
        '<text x="600" y="120" fill="#9FB3D9" font-family="Arial" font-size="13">open circles: L4 analogue;</text>',
        '<text x="600" y="140" fill="#9FB3D9" font-family="Arial" font-size="13">the equilateral point shifts</text>',
        '<text x="600" y="160" fill="#9FB3D9" font-family="Arial" font-size="13">toward the radiating</text>',
        '<text x="600" y="180" fill="#9FB3D9" font-family="Arial" font-size="13">primary as beta grows</text>',
        "</svg>",
    ]
    Path(path).write_text("\n".join(s), encoding="utf-8")


# ---------------------------------------------------------------------------
# Canonical figures (--figures mode): scheme SVG + four PNG panels
# ---------------------------------------------------------------------------


def make_scheme_svg(path):
    """Hand-authored schematic of the laser-dressed CR3BP (white bg, navy/gold)."""
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
        'fill="#0A1730">TRX-01 &#8212; Scheme: laser-dressed CR3BP</text>',
        f'  <text x="30" y="63" font-family="{F}" font-size="13" fill="#3A4A66">Photon '
        "pressure from a laser aimed at primary 1 renormalizes its pull on a massless "
        "particle: F_grav &#8594; (1 &#8722; &#946;)&#183;F_grav</text>",
        # equilateral triangle (classical configuration)
        f'  <line x1="330" y1="390" x2="620" y2="390" stroke="#0A1730" stroke-width="1.4" '
        'stroke-dasharray="6 4" opacity="0.55"/>',
        f'  <line x1="330" y1="390" x2="475" y2="139" stroke="#0A1730" stroke-width="1.4" '
        'stroke-dasharray="6 4" opacity="0.55"/>',
        f'  <line x1="620" y1="390" x2="475" y2="139" stroke="#0A1730" stroke-width="1.4" '
        'stroke-dasharray="6 4" opacity="0.55"/>',
        f'  <text x="475" y="412" font-family="{F}" font-size="11.5" fill="#3A4A66" '
        'text-anchor="middle">equilateral configuration, side = 1 (canonical unit)</text>',
        # primaries
        '  <circle cx="330" cy="390" r="30" fill="#D4AF37" stroke="#0A1730" stroke-width="2"/>',
        '  <circle cx="620" cy="390" r="11" fill="#0A1730" stroke="#0A1730" stroke-width="2"/>',
        f'  <text x="330" y="444" font-family="{F}" font-size="13" font-weight="bold" '
        'fill="#0A1730" text-anchor="middle">Primary 1 &#183; m&#8321; = 1 &#8722; &#956;</text>',
        f'  <text x="330" y="461" font-family="{F}" font-size="11.5" fill="#3A4A66" '
        'text-anchor="middle">radiating: gravity &#215; (1 &#8722; &#946;)</text>',
        f'  <text x="620" y="444" font-family="{F}" font-size="13" font-weight="bold" '
        'fill="#0A1730" text-anchor="middle">Primary 2 &#183; m&#8322; = &#956;</text>',
        f'  <text x="620" y="461" font-family="{F}" font-size="11.5" fill="#3A4A66" '
        'text-anchor="middle">unperturbed gravity</text>',
        # laser station + beam onto primary 1
        '  <rect x="96" y="118" width="64" height="30" rx="4" fill="#FFFFFF" '
        'stroke="#0A1730" stroke-width="2"/>',
        f'  <text x="128" y="138" font-family="{F}" font-size="12" font-weight="bold" '
        'fill="#0A1730" text-anchor="middle">laser</text>',
        '  <polygon points="160,126 306,356 306,368 160,140" fill="#D4AF37" opacity="0.22"/>',
        '  <line x1="162" y1="133" x2="303" y2="361" stroke="#D4AF37" stroke-width="2.2" '
        'marker-end="url(#arrG)"/>',
        f'  <text x="176" y="116" font-family="{F}" font-size="12" fill="#0A1730">laser '
        "beam (power P, &#955; = 1 &#956;m at &#916; = 1 AU)</text>",
        # classical and displaced L4
        '  <circle cx="475" cy="139" r="8" fill="#FFFFFF" stroke="#0A1730" stroke-width="1.8"/>',
        f'  <text x="492" y="130" font-family="{F}" font-size="12" fill="#0A1730">classical '
        "L&#8324; (&#946; = 0)</text>",
        '  <circle cx="458" cy="168" r="8" fill="#D4AF37" stroke="#0A1730" stroke-width="2"/>',
        '  <line x1="471" y1="149" x2="461" y2="163" stroke="#0A1730" stroke-width="2" '
        'marker-end="url(#arrN)"/>',
        f'  <text x="404" y="150" font-family="{F}" font-size="12" fill="#0A1730" '
        'text-anchor="end">displaced L&#8324; (&#946; &gt; 0)</text>',
        f'  <text x="404" y="168" font-family="{F}" font-size="12" fill="#0A1730" '
        'text-anchor="end">L&#8324; shift grows with &#946;</text>',
        # librational orbit region + massless particle
        '  <circle cx="458" cy="168" r="48" fill="none" stroke="#D4AF37" stroke-width="1.6" '
        'stroke-dasharray="5 5" opacity="0.9"/>',
        '  <circle cx="487" cy="206" r="4.5" fill="#0A1730"/>',
        '  <line x1="492" y1="210" x2="536" y2="228" stroke="#0A1730" stroke-width="0.8" '
        'opacity="0.6"/>',
        f'  <text x="540" y="232" font-family="{F}" font-size="12" fill="#0A1730">massless '
        "particle (dust, m &#8594; 0) on a tadpole libration</text>",
        # barycentre
        '  <line x1="330" y1="386.5" x2="337" y2="393.5" stroke="#0A1730" stroke-width="1.4"/>',
        '  <line x1="337" y1="386.5" x2="330" y2="393.5" stroke="#0A1730" stroke-width="1.4"/>',
        '  <line x1="337" y1="386" x2="362" y2="350" stroke="#0A1730" stroke-width="0.8" '
        'opacity="0.6"/>',
        f'  <text x="365" y="348" font-family="{F}" font-size="10.5" fill="#3A4A66">barycentre '
        "(origin of the rotating frame)</text>",
        # rotating-frame arrow
        '  <path d="M 775 205 A 45 45 0 0 1 820 160" fill="none" stroke="#0A1730" '
        'stroke-width="1.8" marker-end="url(#arrN)"/>',
        f'  <text x="838" y="178" font-family="{F}" font-size="12" fill="#0A1730">rotating '
        "frame</text>",
        f'  <text x="838" y="194" font-family="{F}" font-size="11.5" fill="#3A4A66">angular '
        "rate n = 1</text>",
        # beta info box
        '  <rect x="56" y="434" width="200" height="74" rx="6" fill="#FFFFFF" '
        'stroke="#0A1730" stroke-width="1.4"/>',
        f'  <text x="68" y="458" font-family="{F}" font-size="13.5" font-weight="bold" '
        'fill="#0A1730">&#946; = F_rad / F_grav</text>',
        f'  <text x="68" y="477" font-family="{F}" font-size="12" fill="#0A1730">&#946; = 0 '
        "&#8594; classical CR3BP</text>",
        f'  <text x="68" y="496" font-family="{F}" font-size="12" fill="#0A1730">&#946; &gt; 0 '
        "&#8594; L&#8324; moves toward primary 1</text>",
        # Jacobi invariant notes
        f'  <text x="620" y="492" font-family="{F}" font-size="12.5" fill="#0A1730">Jacobi '
        "invariant: C_J = 2&#937; &#8722; (&#789;&#178; + &#7899;&#178;)</text>",
        f'  <text x="620" y="508" font-family="{F}" font-size="11.5" fill="#3A4A66">with '
        "&#937; containing the (1 &#8722; &#946;)(1 &#8722; &#956;)/r&#8321; term</text>",
        # footer
        f'  <text x="30" y="524" font-family="{F}" font-size="10.5" fill="#6B7A94">TRIVORTEX '
        "Research Program &#183; study TRX-01 &#183; laser-dressed circular restricted "
        "three-body problem</text>",
        "</svg>",
    ]
    Path(path).write_text("\n".join(s), encoding="utf-8")


def _zvc_grid(beta, xn=760, yn=540):
    """Mesh of 2*Omega over the rotating-frame viewport."""
    xg = np.linspace(-1.9, 1.9, xn)
    yg = np.linspace(-1.3, 1.3, yn)
    X, Y = np.meshgrid(xg, yg)
    return X, Y, 2.0 * omega_eff(X, Y, beta)


def render_figures(L, states, ts, C_vals, drift, shifts, smoke, figdir):
    """Render the scheme SVG and the four canonical PNG panels into figures/.

    Reuses the equilibrium and orbit data already computed in main(); adds a
    dense beta scan of the L4 eigenvalues and the zero-velocity-curve grids.
    Returns the "figures" block for the JSON protocol.
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Circle, Patch

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

    # ---- shared data --------------------------------------------------------
    l4_dense = np.linspace(0.0, 0.1, 41)
    l4_path = np.array([triangular_point(b, +1.0) for b in l4_dense])
    l4_0 = np.array(L[0.0]["L4"])
    l4_1 = np.array(L[0.1]["L4"])
    l4_scan = np.array([L[b]["L4"] for b in BETAS])
    dx = l4_scan[:, 0] - l4_0[0]
    dy = l4_scan[:, 1] - l4_0[1]
    mag = np.hypot(dx, dy)

    # ================= fig01 — landscape =====================================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle("TRX-01 · Radiation-pressure CR3BP", fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    def _pt(entry):
        """Equilibrium coordinates; collinear points are stored as abscissae."""
        return (float(entry), 0.0) if np.isscalar(entry) else (float(entry[0]), float(entry[1]))

    keys = ("L1", "L2", "L3", "L4", "L5")
    bx0 = [_pt(L[0.0][k])[0] for k in keys]
    by0 = [_pt(L[0.0][k])[1] for k in keys]
    bx1 = [_pt(L[0.1][k])[0] for k in keys]
    by1 = [_pt(L[0.1][k])[1] for k in keys]
    ax1.add_patch(Circle((-MU, 0.0), 0.052, facecolor=GOLD, edgecolor=NAVY, lw=1.5, zorder=5))
    ax1.add_patch(
        Circle((1.0 - MU, 0.0), 0.052 * MU ** (1.0 / 3.0), facecolor=NAVY, edgecolor=NAVY, zorder=5)
    )
    ax1.scatter(
        bx0,
        by0,
        s=95,
        facecolors="none",
        edgecolors=GOLD,
        linewidths=1.8,
        label=r"$\beta=0$ (classical)",
        zorder=6,
    )
    ax1.scatter(bx1, by1, s=42, color=blue, label=r"$\beta=0.1$ (laser on)", zorder=6)
    for k, x, y in zip(keys, bx0, by0):
        ax1.annotate(k, (x, y), textcoords="offset points", xytext=(6, 6), fontsize=10, color=NAVY)
    ax1.axhline(0.0, color=NAVY, lw=0.7, alpha=0.5)
    ax1.set_xlim(-1.45, 1.45)
    ax1.set_ylim(-1.05, 1.05)
    ax1.set_aspect("equal")
    ax1.set_xlabel("x [dimensionless]")
    ax1.set_ylabel("y [dimensionless]")
    ax1.set_title(r"(a) Libration-point map, $\mu=0.0121505856$")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="upper left")

    l1_0 = L[0.0]["L1"] if np.isscalar(L[0.0]["L1"]) else L[0.0]["L1"][0]
    l1_1 = L[0.1]["L1"] if np.isscalar(L[0.1]["L1"]) else L[0.1]["L1"][0]
    C1_0 = 2.0 * omega_eff(float(l1_0), 0.0, 0.0)
    C1_1 = 2.0 * omega_eff(float(l1_1), 0.0, 0.1)
    X0, Y0, W0 = _zvc_grid(0.0)
    X1, Y1, W1 = _zvc_grid(0.1)
    ax2.contourf(X0, Y0, W0 - C1_0, levels=[-1e9, 0.0], colors=[NAVY], alpha=0.06)
    ax2.contourf(X1, Y1, W1 - C1_1, levels=[-1e9, 0.0], colors=[blue], alpha=0.07)
    ax2.contour(X0, Y0, W0, levels=[C1_0], colors=[GOLD], linewidths=2.0)
    ax2.contour(X1, Y1, W1, levels=[C1_1], colors=[blue], linewidths=1.8, linestyles="--")
    ax2.scatter([-MU, 1.0 - MU], [0.0, 0.0], s=[90, 22], color=[GOLD, NAVY], zorder=5)
    ax2.scatter(
        [l4_0[0], l4_1[0]],
        [l4_0[1], l4_1[1]],
        s=45,
        marker="D",
        c=[GOLD, blue],
        edgecolors=NAVY,
        linewidths=0.8,
        zorder=6,
    )
    handles = [
        Line2D([], [], color=GOLD, lw=2.0, label=r"$\beta=0$: $2\Omega=C_J(\mathrm{L1})$"),
        Line2D(
            [], [], color=blue, lw=1.8, ls="--", label=r"$\beta=0.1$: $2\Omega=C_J(\mathrm{L1})$"
        ),
        Patch(facecolor=NAVY, alpha=0.10, label=r"forbidden region ($2\Omega<C_J$)"),
    ]
    ax2.legend(handles=handles, loc="upper left")
    ax2.set_xlabel("x [dimensionless]")
    ax2.set_ylabel("y [dimensionless]")
    ax2.set_title("(b) Zero-velocity curves at the L1 neck-opening level")
    ax2.set_aspect("equal")
    ax2.grid(True, alpha=0.3)
    fig.savefig(figdir / "fig01_landscape.png")
    plt.close(fig)

    # ================= fig02 — L4 shift (headline) ===========================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle("TRX-01 · Radiation-pressure CR3BP", fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    ax1.plot(l4_path[:, 0], l4_path[:, 1], color=GOLD, lw=2.4, label="L4 migration path")
    for i, b in enumerate(BETAS):
        ax1.plot(
            L[b]["L4"][0], L[b]["L4"][1], "o", ms=9, mfc=SERIES[i], mec=NAVY, mew=1.2, ls="none"
        )
    ax1.annotate(
        r"$\beta=0$", xy=l4_0, textcoords="offset points", xytext=(6, 9), fontsize=10, color=NAVY
    )
    for b, off in ((0.01, (8, -15)), (0.05, (8, -15)), (0.1, (8, -15))):
        ax1.annotate(
            rf"$\beta={b}$",
            xy=L[b]["L4"],
            textcoords="offset points",
            xytext=off,
            fontsize=10,
            color=NAVY,
        )
    ax1.annotate(
        "",
        xy=l4_1,
        xytext=l4_0,
        arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.8, shrinkA=10, shrinkB=10),
    )
    ax1.annotate(
        rf"$|\Delta \mathrm{{L4}}| = {mag[-1]:.3e}$",
        xy=(0.03, 0.93),
        xycoords="axes fraction",
        fontsize=10.5,
        color=NAVY,
    )
    u = np.array([-MU, 0.0]) - l4_0
    u = u / np.linalg.norm(u)
    ax1.plot(
        [l4_0[0], l4_0[0] + 0.025 * u[0]],
        [l4_0[1], l4_0[1] + 0.025 * u[1]],
        color=NAVY,
        lw=1.2,
        ls="--",
        label="toward radiating primary",
    )
    ax1.set_xlim(0.443, 0.499)
    ax1.set_ylim(0.840, 0.872)
    ax1.set_aspect("equal")
    ax1.set_xlabel("x [dimensionless]")
    ax1.set_ylabel("y [dimensionless]")
    ax1.set_title("(a) Migration of L4 toward primary 1")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="lower right")

    ax2.plot(
        BETAS, mag, color=GOLD, lw=2.6, marker="o", ms=7, mec=NAVY, label=r"$|\Delta\mathrm{L4}|$"
    )
    ax2.plot(BETAS, dx, color=blue, lw=1.6, marker="s", ms=5, label=r"$\Delta x$")
    ax2.plot(BETAS, dy, color=green, lw=1.6, marker="^", ms=5, label=r"$\Delta y$")
    ax2.axhline(0.0, color=NAVY, lw=0.8, alpha=0.5)
    ax2.annotate(
        rf"${mag[-1]:.3e}$ at $\beta=0.1$",
        xy=(BETAS[-1], mag[-1]),
        textcoords="offset points",
        xytext=(-86, -16),
        fontsize=10.5,
        color=NAVY,
    )
    ax2.set_xlabel(r"$\beta$ [dimensionless]")
    ax2.set_ylabel("L4 displacement [dimensionless]")
    ax2.set_title("(b) Displacement of L4 vs radiation coefficient")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="upper left")
    fig.savefig(figdir / "fig02_l4_shift.png")
    plt.close(fig)

    # ================= fig03 — stability scan ================================
    betas_d = np.linspace(0.0, 0.12, 25)
    om_s, om_l, mre = [], [], []
    for b in betas_d:
        pt = triangular_point(b, +1.0)
        ev = np.linalg.eigvals(stability_matrix(pt, b))
        ims = np.sort(np.abs(ev.imag))
        om_s.append(float(ims[3]))  # larger |Im| -> shorter period
        om_l.append(float(ims[1]))  # smaller |Im| -> longer period
        mre.append(float(np.max(np.abs(ev.real))))
    om_s, om_l, mre = np.array(om_s), np.array(om_l), np.array(mre)

    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle("TRX-01 · Radiation-pressure CR3BP", fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    ax1.plot(betas_d, om_s, color=blue, lw=2.2, label=r"short-period $\omega_{s}$")
    ax1.plot(betas_d, om_l, color=green, lw=2.2, label=r"long-period $\omega_{l}$")
    ax1.set_xlabel(r"$\beta$ [dimensionless]")
    ax1.set_ylabel(r"eigenvalue frequency $|\mathrm{Im}\,\lambda|$ [1/time]")
    ax1.set_title("(a) L4 eigenvalue frequencies vs radiation coefficient")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="center left")

    ax2.plot(
        betas_d,
        np.maximum(mre, 1e-18),
        color=red,
        lw=1.6,
        marker="o",
        ms=4,
        label=r"$\max|\mathrm{Re}\,\lambda|$",
    )
    ax2.axhline(1e-8, color=NAVY, lw=1.2, ls="--", label="acceptance tolerance 1e-8")
    ax2.set_yscale("log")
    ax2.set_ylim(1e-18, 1e-6)
    ax2.set_xlabel(r"$\beta$ [dimensionless]")
    ax2.set_ylabel(r"$\max|\mathrm{Re}\,\lambda|$ [1/time]")
    ax2.set_title("(b) Real parts of the L4 eigenvalues vs radiation coefficient")
    ax2.grid(True, alpha=0.3, which="both")
    ax2.legend(loc="center right")
    fig.savefig(figdir / "fig03_stability_scan.png")
    plt.close(fig)

    # ================= fig04 — Jacobi drift ==================================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle("TRX-01 · Radiation-pressure CR3BP", fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    l4o = L[0.05]["L4"]
    ax1.plot(states[0], states[1], color=GOLD, lw=1.3, label="orbit near L4")
    ax1.plot(states[0][0], states[1][0], "o", color=NAVY, ms=7, label="start")
    ax1.plot(l4o[0], l4o[1], "D", color=blue, ms=8, mec=NAVY, label=r"displaced L4 ($\beta=0.05$)")
    ax1.set_aspect("equal")
    ax1.set_xlabel("x [dimensionless]")
    ax1.set_ylabel("y [dimensionless]")
    ax1.set_title(rf"(a) Orbit near the displaced L4, $T={float(ts[-1]):.0f}$")
    ax1.grid(True, alpha=0.3)
    h1, l1 = ax1.get_legend_handles_labels()

    dC = C_vals - C_vals[0]
    m = float(np.max(np.abs(dC)))
    m = m if m > 0.0 else 1e-16
    ax2.plot(ts, dC, color=NAVY, lw=1.2)
    ax2.axhline(0.0, color=NAVY, lw=0.8, alpha=0.5)
    ax2.set_ylim(-1.3 * m, 1.3 * m)
    ax2.annotate(
        rf"$\max|\Delta C_J| = {m:.1e}$",
        xy=(0.03, 0.86),
        xycoords="axes fraction",
        fontsize=11,
        color=NAVY,
    )
    ax2.annotate(
        "tolerance 1e-10 (off scale)",
        xy=(0.03, 0.74),
        xycoords="axes fraction",
        fontsize=10,
        color="#3A4A66",
    )
    ax2.set_xlabel(r"time $t$ [1/n]")
    ax2.set_ylabel(r"$\Delta C_J$ [dimensionless]")
    ax2.set_title("(b) Jacobi invariant drift along the orbit")
    ax2.grid(True, alpha=0.3)
    fig.legend(h1, l1, loc="outside right upper")
    fig.savefig(figdir / "fig04_jacobi_drift.png")
    plt.close(fig)

    # ================= scheme SVG ============================================
    make_scheme_svg(figdir / "scheme_trx01.svg")

    # ================= JSON figures block ====================================
    shift_txt = " -> ".join(f"{s:.3e}" for s in shifts)
    t_run = float(ts[-1])
    return {
        "mode": "smoke" if smoke else "full",
        "scheme": {
            "file": "figures/scheme_trx01.svg",
            "caption": (
                "Hand-authored schematic of the laser-dressed CR3BP: a laser beam "
                "illuminates primary 1 (mass 1 - mu), photon pressure renormalizes its "
                "pull on the massless particle to (1 - beta) of gravity, and the "
                "triangular point L4 is displaced toward the radiating primary "
                "(mu = 0.0121505856)."
            ),
        },
        "panels": [
            {
                "file": "figures/fig01_landscape.png",
                "caption": (
                    "Libration-point landscape at mu = 0.0121505856: (a) L1-L5 for "
                    "beta = 0 (open gold) versus beta = 0.1 (filled blue); (b) "
                    "zero-velocity curves 2*Omega = C_J evaluated at the L1 "
                    "neck-opening level for both beta values, forbidden regions "
                    "where 2*Omega < C_J shaded."
                ),
            },
            {
                "file": "figures/fig02_l4_shift.png",
                "caption": (
                    "Headline result - migration of the triangular point toward the "
                    "radiating primary: (a) L4(beta) path in the rotating frame for "
                    "0 <= beta <= 0.1 with the scan points beta in {0, 0.01, 0.05, "
                    "0.1} marked and the shift arrow toward primary 1; (b) "
                    f"displacement components and magnitude versus beta, magnitude "
                    f"{shift_txt} over the scan."
                ),
            },
            {
                "file": "figures/fig03_stability_scan.png",
                "caption": (
                    "Linear-stability scan of the displaced L4: (a) short- and "
                    "long-period eigenvalue frequencies |Im(lambda)| versus beta over "
                    "0 <= beta <= 0.12; (b) largest real part max|Re(lambda)| versus "
                    "beta on a logarithmic scale, held at machine-zero level against "
                    "the 1e-8 acceptance tolerance."
                ),
            },
            {
                "file": "figures/fig04_jacobi_drift.png",
                "caption": (
                    "Dynamics near the displaced L4 at beta = 0.05: (a) rotating-frame "
                    f"orbit over T = {t_run:.0f} (DOP853, rtol = atol = 1e-12); (b) "
                    f"drift of the Jacobi invariant C_J along the orbit, "
                    f"max |Delta C_J| = {drift:.1e} against the 1e-10 tolerance."
                ),
            },
        ],
        "data": {
            "stability_scan": {
                "beta_max": round(float(betas_d[-1]), 3),
                "n_points": int(betas_d.size),
                "omega_short_min": float(f"{om_s.min():.6e}"),
                "omega_short_max": float(f"{om_s.max():.6e}"),
                "omega_long_min": float(f"{om_l.min():.6e}"),
                "omega_long_max": float(f"{om_l.max():.6e}"),
                "max_re_largest": float(f"{mre.max():.6e}"),
            },
            "l4_shift_scan": {
                "beta": [float(b) for b in BETAS],
                "magnitude": [float(f"{m_:.6e}") for m_ in mag],
            },
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv=None):
    ap = argparse.ArgumentParser(description="TRX-01 radiation-pressure CR3BP")
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

    # --- equilibrium points -------------------------------------------------
    L = {}
    for beta in BETAS:
        L1 = collinear_point(beta, 0.70, 0.95)
        L2 = collinear_point(beta, 1.00, 1.30)
        L3 = collinear_point(beta, -1.30, -0.90)
        L4 = triangular_point(beta, +1.0)
        L5 = triangular_point(beta, -1.0)
        L[beta] = {"L1": L1, "L2": L2, "L3": L3, "L4": L4, "L5": L5}

    # check 2: classical L1 for beta = 0
    add(
        "L1_abscissa_beta0",
        L[0.0]["L1"],
        0.8369151,
        5e-6,
        "dimless",
        "Earth-Moon CR3BP reference value",
    )

    # check 3: L4 shift monotone & directed away from primary 1
    shifts = [
        np.hypot(L[b]["L4"][0] - L[0.0]["L4"][0], L[b]["L4"][1] - L[0.0]["L4"][1]) for b in BETAS
    ]
    mono = all(shifts[i + 1] > shifts[i] for i in range(len(shifts) - 1))
    d = np.array(L[0.1]["L4"]) - np.array(L[0.0]["L4"])
    r1_hat = np.array(L[0.0]["L4"]) - np.array([-MU, 0.0])
    r1_hat = r1_hat / np.linalg.norm(r1_hat)
    toward = float(np.dot(d, r1_hat)) < 0.0
    add(
        "L4_shift_monotone_in_beta",
        1.0 if mono else 0.0,
        1.0,
        1e-12,
        "bool",
        "shifts=" + ",".join(f"{s:.3e}" for s in shifts),
    )
    add(
        "L4_shift_toward_radiating_primary",
        1.0 if toward else 0.0,
        1.0,
        1e-12,
        "bool",
        "weakened pull of primary 1 moves the triangular point closer to it",
    )

    # check 4: L4 marginal stability for beta = 0
    ev0 = np.linalg.eigvals(stability_matrix(L[0.0]["L4"], 0.0))
    max_re0 = float(np.max(np.abs(ev0.real)))
    add(
        "L4_max_Re_eigenvalue_beta0",
        max_re0,
        0.0,
        1e-8,
        "1/time",
        "marginally stable for mu < mu_Routh",
    )

    # check 5: L1 moves toward the radiating primary as beta grows
    add(
        "L1_shifts_toward_radiating_primary",
        1.0 if L[0.1]["L1"] < L[0.0]["L1"] else 0.0,
        1.0,
        1e-12,
        "bool",
        f"x_L1: {L[0.0]['L1']:.7f} -> {L[0.1]['L1']:.7f}",
    )

    # --- Jacobi conservation near L4 (beta = 0.05) ---------------------------
    beta = 0.05
    l4 = np.array(L[beta]["L4"])
    s0 = np.array([l4[0] + 0.02, l4[1], 0.01, -0.005])
    T = 5.0 if smoke else 20.0
    sol = solve_ivp(
        eom,
        (0.0, T),
        s0,
        args=(beta,),
        method="DOP853",
        rtol=1e-12,
        atol=1e-12,
        dense_output=True,
        max_step=0.05,
    )
    ts = np.linspace(0.0, T, 400 if smoke else 1600)
    states = sol.sol(ts)
    C_vals = np.array([jacobi(states[:, i], beta) for i in range(ts.size)])
    drift = float(np.max(np.abs(C_vals - C_vals[0])))
    add(
        "Jacobi_drift_L4_orbit_beta0.05",
        drift,
        0.0,
        1e-10,
        "dimless",
        f"T={T}, DOP853 rtol=atol=1e-12",
    )

    # --- laser scenario table (informational) --------------------------------
    laser = laser_beta_table()

    # --- SVG -----------------------------------------------------------------
    beta = 0.1
    l4b = np.array(L[beta]["L4"])
    s0b = np.array([l4b[0] + 0.02, l4b[1], 0.01, -0.005])
    sol0 = solve_ivp(
        eom,
        (0.0, 6.0),
        s0,
        args=(0.0,),
        method="DOP853",
        rtol=1e-12,
        atol=1e-12,
        dense_output=True,
        max_step=0.05,
    )
    sol1 = solve_ivp(
        eom,
        (0.0, 6.0),
        s0b,
        args=(0.1,),
        method="DOP853",
        rtol=1e-12,
        atol=1e-12,
        dense_output=True,
        max_step=0.05,
    )
    tt = np.linspace(0, 6.0, 900)
    orb0 = sol0.sol(tt)[:2].T
    orb1 = sol1.sol(tt)[:2].T
    out = Path(__file__).resolve().parents[1] / "results"
    out.mkdir(exist_ok=True)
    make_svg(orb0, orb1, L[0.0]["L4"], L[0.1]["L4"], out / "trx01_plot.svg")

    # --- canonical figures (--figures, additive) -----------------------------
    figures_block = None
    figdir = Path(__file__).resolve().parents[1] / "figures"
    if args.figures:
        figures_block = render_figures(
            L=L,
            states=states,
            ts=ts,
            C_vals=C_vals,
            drift=drift,
            shifts=shifts,
            smoke=smoke,
            figdir=figdir,
        )

    # --- protocol ------------------------------------------------------------
    all_pass = all(c["pass"] for c in CHECKS)
    protocol = {
        "study": "TRX-01",
        "title": "Radiation-pressure restricted three-body problem (laser on dust)",
        "status": "PASS" if all_pass else "FAIL",
        "smoke": bool(smoke),
        "runtime_s": round(time.time() - t0, 3),
        "checks": CHECKS,
        "series": {"jacobi_CJ": [round(float(v), 12) for v in C_vals[:: max(1, ts.size // 400)]]},
        "meta": {
            "equations": [
                "x'' - 2y' = dOmega/dx ; y'' + 2x' = dOmega/dy",
                "Omega = (x^2+y^2)/2 + (1-beta)(1-mu)/r1 + mu/r2",
                "C_J = 2*Omega - (x'^2 + y'^2)",
            ],
            "mu": MU,
            "beta_scan": list(BETAS),
            "libration_points": {f"beta={b}": L[b] for b in BETAS},
            "laser_scenario": laser,
        },
    }
    if figures_block is not None:
        protocol["figures"] = figures_block
    (out / "trx01_results.json").write_text(json.dumps(protocol, indent=2), encoding="utf-8")

    print(f"\nTRX-01 — radiation-pressure CR3BP  [{'SMOKE' if smoke else 'FULL'}]")
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
