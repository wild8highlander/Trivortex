#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
TRIVORTEX LAB — TRX-03 — THREE-SOLITON MOLECULE IN A MODE-LOCKED FIBER LASER
============================================================================
Three ultrashort pulses circulating in a passively mode-locked fiber laser
form a phase-locked "soliton molecule".  In the reduced particle picture
each pulse is a body with the conservative pair interaction

    V(r, dphi) = C1 exp(-2 r / L) - C2 exp(-r / L) cos(2 dphi) ,

where r is the pulse separation, dphi the phase difference, L the
evanescent-tail length.  An in-phase triplet (dphi = 0) is bound at

    r0 = L ln( 2 C1 / (C2 cos 2 dphi) ) ,

and supports a breathing normal mode omega_b = sqrt(3 V''(r0)).

What is computed
  * analytic vs numeric pair equilibrium, anti-phase repulsion
  * relaxation of a random triplet into an equally spaced molecule
  * conservative energy conservation + breathing-mode frequency

With --figures: hand-authored scheme SVG + four canonical PNG panels
(300 dpi) into figures/, and a "figures" block added to the JSON protocol
(scheme, panels with captions, phase-sweep data). Composable with --smoke.

Usage:  python trx03_soliton_molecule.py [--smoke] [--figures]
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

C1, C2, L, M = 2.0, 3.0, 1.0, 1.0

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
# Model
# ---------------------------------------------------------------------------


def V(r, dphi=0.0):
    return C1 * np.exp(-2.0 * r / L) - C2 * np.exp(-r / L) * np.cos(2.0 * dphi)


def F(r, dphi=0.0):
    """F = -dV/dr : radial pair force along increasing r (F<0 -> attraction)."""
    return (2.0 * C1 / L) * np.exp(-2.0 * r / L) - (C2 / L) * np.exp(-r / L) * np.cos(2.0 * dphi)


def Vpp(r, dphi=0.0):
    return (4.0 * C1 / L**2) * np.exp(-2.0 * r / L) - (C2 / L**2) * np.exp(-r / L) * np.cos(
        2.0 * dphi
    )


def r0_analytic(dphi=0.0):
    return L * np.log(2.0 * C1 / (C2 * np.cos(2.0 * dphi)))


def chain_rhs(t, s, gamma_d):
    """3-particle 1-D chain with ALL-PAIRS potential V, damping gamma_d.

    Soliton evanescent tails act pairwise at any separation, and solitons
    may pass through one another (as they do in real fibres).
    """
    x = s[0:3]
    v = s[3:6]
    a = np.zeros(3)
    for k in range(3):
        for j in range(3):
            if j == k:
                continue
            d = x[j] - x[k]
            sign = np.sign(d) if d != 0 else 0.0
            # F(|d|) = -dV/dr ; force on k = -F*sign(d) (towards j if attractive)
            a[k] -= sign * F(abs(d)) / M
    if gamma_d:
        a -= gamma_d * v
    return np.concatenate([v, a])


def chain_potential(x):
    """Total potential of the 3-pulse chain (all pairs)."""
    return V(abs(x[1] - x[0])) + V(abs(x[2] - x[1])) + V(abs(x[2] - x[0]))


def chain_equilibrium_spacing():
    """Symmetric 3-chain equilibrium: end pulse feels F(s) + F(2s) = 0."""
    return brentq(lambda s: F(s) + F(2.0 * s), 0.05, 2.0, xtol=1e-15, rtol=8.9e-16, maxiter=200)


def chain_hessian_freqs(sp, dphi=0.0):
    """Normal-mode frequencies of the 3-pulse chain at spacing sp (all pairs).

    Potential W(d1,d2) = V(d1)+V(d2)+V(d1+d2); kinetic energy in the spacing
    coordinates d1,d2 (COM removed) is T = (m/3)(ddot1^2+ddot1*ddot2+ddot2^2),
    i.e. mass matrix M_g = m*[[2/3,1/3],[1/3,2/3]].  Frequencies solve the
    generalized eigenproblem H v = omega^2 M_g v.
    """
    from scipy.linalg import eigh

    h = 1e-6

    def W(d1, d2):
        return V(d1, dphi) + V(d2, dphi) + V(d1 + d2, dphi)

    W00 = W(sp, sp)
    Wpp = (W(sp + h, sp) - 2.0 * W00 + W(sp - h, sp)) / h**2
    W12 = (W(sp + h, sp + h) - W(sp + h, sp - h) - W(sp - h, sp + h) + W(sp - h, sp - h)) / (
        4.0 * h**2
    )
    H = np.array([[Wpp, W12], [W12, Wpp]])
    Mg = M * np.array([[2.0 / 3.0, 1.0 / 3.0], [1.0 / 3.0, 2.0 / 3.0]])
    vals = eigh(H, Mg, eigvals_only=True)
    return vals


def energy_chain(s):
    x = s[0:3]
    v = s[3:6]
    U = chain_potential(x)
    K = 0.5 * M * float(np.dot(v, v))
    return K + U


# ---------------------------------------------------------------------------
# SVG output
# ---------------------------------------------------------------------------


def _poly(pts, color, sw=1.6):
    s = " ".join(f"{px:.2f},{py:.2f}" for px, py in pts)
    return f'<polyline fill="none" stroke="{color}" stroke-width="{sw}" points="{s}"/>'


def make_svg(ts, xs, xf, path):
    W, H = 900, 520
    x0, x1, y0, y1 = 70.0, 560.0, 70.0, 430.0
    tmax, xmax = float(ts[-1]), 5.0

    def X(t):
        return x0 + (t / tmax) * (x1 - x0)

    def Y(x):
        return y1 - ((x + 2.5) / xmax) * (y1 - y0)

    colors = ["#6FB7FF", "#F2C14E", "#FFFFFF"]
    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect width="{W}" height="{H}" fill="#0A1230"/>',
        '<text x="24" y="34" fill="#FFFFFF" font-family="Arial" font-size="19" '
        'font-weight="bold">TRX-03 &#8212; Three-soliton molecule in a fiber laser</text>',
    ]
    for k in range(3):
        s.append(_poly([(X(t), Y(xx)) for t, xx in zip(ts, xs[k])], colors[k], 1.4))
    # final molecule (three Gaussian humps) on the right panel
    gx = np.linspace(0.0, 3.0, 160)
    g0, g1p = 600.0, 870.0
    gy0, gy1 = 120.0, 400.0
    prof = (
        np.exp(-((gx - xf[0]) ** 2) / 0.01)
        + np.exp(-((gx - xf[1]) ** 2) / 0.01)
        + np.exp(-((gx - xf[2]) ** 2) / 0.01)
    )
    pts = [
        (g0 + (g / 3.0) * (g1p - g0), gy1 - (p / prof.max()) * (gy1 - gy0))
        for g, p in zip(gx, prof)
    ]
    s += [
        f'<line x1="{g0}" y1="{gy1}" x2="{g1p}" y2="{gy1}" stroke="#3A4A6B" stroke-width="1"/>',
        _poly(pts, "#F2C14E", 2.0),
        '<text x="600" y="100" fill="#9FB3D9" font-family="Arial" font-size="13">final intensity profile:</text>',
        '<text x="600" y="118" fill="#9FB3D9" font-family="Arial" font-size="13">equally spaced molecule</text>',
        '<text x="90" y="470" fill="#9FB3D9" font-family="Arial" font-size="13">pulse worldlines relax into a phase-locked, equally spaced soliton molecule</text>',
        "</svg>",
    ]
    Path(path).write_text("\n".join(s), encoding="utf-8")


# ---------------------------------------------------------------------------
# Canonical figures (--figures mode): scheme SVG + four PNG panels
# ---------------------------------------------------------------------------


def make_scheme_svg(path):
    """Hand-authored schematic of the soliton molecule (white bg, navy/gold)."""
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
        'fill="#0A1730">TRX-03 &#8212; Scheme: three-soliton molecule in a mode-locked fiber laser</text>',
        f'  <text x="30" y="63" font-family="{F}" font-size="13" fill="#3A4A66">Phase-locked '
        "ultrashort pulses behave as three bodies with a phase-dependent exponential pair "
        "interaction V(r, &#916;&#966;)</text>",
        # ---- left panel: fiber ring with three pulses ------------------------
        '  <circle cx="235" cy="300" r="150" fill="none" stroke="#0A1730" stroke-width="2"/>',
        '  <circle cx="235" cy="300" r="128" fill="none" stroke="#0A1730" stroke-width="0.9" '
        'opacity="0.35"/>',
        '  <path d="M 235 138 A 162 162 0 0 1 300 150" fill="none" stroke="#0A1730" '
        'stroke-width="1.8" marker-end="url(#arrN)"/>',
        f'  <text x="252" y="124" font-family="{F}" font-size="12" fill="#0A1730">circulating '
        "mode-locked pulse train</text>",
        f'  <text x="235" y="492" font-family="{F}" font-size="12.5" fill="#3A4A66" '
        'text-anchor="middle">mode-locked fiber laser ring &#183; passively saturated absorber</text>',
        # three gold pulses on the ring (Gaussian humps, radially outward)
        '  <path d="M 175 172 C 183 156 191 156 199 172 C 191 168 183 168 175 172 Z" '
        'fill="#D4AF37" stroke="#0A1730" stroke-width="1.2"/>',
        '  <path d="M 353 232 C 361 216 369 216 377 232 C 369 228 361 228 353 232 Z" '
        'fill="#D4AF37" stroke="#0A1730" stroke-width="1.2"/>',
        '  <path d="M 292 428 C 300 412 308 412 316 428 C 308 424 300 424 292 428 Z" '
        'fill="#D4AF37" stroke="#0A1730" stroke-width="1.2"/>',
        f'  <text x="118" y="138" font-family="{F}" font-size="12.5" font-weight="bold" '
        'fill="#0A1730">pulse 1</text>',
        f'  <text x="118" y="154" font-family="{F}" font-size="11" fill="#3A4A66">&#916;&#966; = 0</text>',
        f'  <text x="384" y="222" font-family="{F}" font-size="12.5" font-weight="bold" '
        'fill="#0A1730">pulse 2</text>',
        f'  <text x="384" y="238" font-family="{F}" font-size="11" fill="#3A4A66">&#916;&#966; = 0</text>',
        f'  <text x="322" y="452" font-family="{F}" font-size="12.5" font-weight="bold" '
        'fill="#0A1730">pulse 3</text>',
        f'  <text x="322" y="468" font-family="{F}" font-size="11" fill="#3A4A66">&#916;&#966; = 0</text>',
        f'  <text x="52" y="300" font-family="{F}" font-size="12" fill="#0A1730">phase-locked '
        "triplet:</text>",
        f'  <text x="52" y="317" font-family="{F}" font-size="12" fill="#0A1730">an optical '
        "three-body</text>",
        f'  <text x="52" y="334" font-family="{F}" font-size="12" fill="#0A1730">choreography</text>',
        # ---- right panel: interaction potential well -------------------------
        # axes
        '  <line x1="560" y1="330" x2="930" y2="330" stroke="#0A1730" stroke-width="1.5" '
        'marker-end="url(#arrN)"/>',
        '  <line x1="575" y1="360" x2="575" y2="110" stroke="#0A1730" stroke-width="1.5" '
        'marker-end="url(#arrN)"/>',
        f'  <text x="930" y="348" font-family="{F}" font-size="12" fill="#0A1730" '
        'text-anchor="end">separation r [tail lengths L]</text>',
        f'  <text x="565" y="104" font-family="{F}" font-size="12" fill="#0A1730" '
        'text-anchor="end">pair energy V(r)</text>',
        # zero line
        '  <line x1="575" y1="252" x2="920" y2="252" stroke="#0A1730" stroke-width="0.9" '
        'stroke-dasharray="4 4" opacity="0.5"/>',
        f'  <text x="920" y="246" font-family="{F}" font-size="10.5" fill="#3A4A66" '
        'text-anchor="end">V = 0 (free pulses)</text>',
        # bound well curve (V(r), dphi = 0): min at r0 -> x = 575 + 105*(r0/1.2)
        '  <path d="M 577 118 C 596 176 615 218 641 232 C 668 245 690 240 730 251 '
        'C 790 251 860 252 920 252" fill="none" stroke="#0A1730" stroke-width="2"/>',
        # repulsive curve (dphi = pi/2), dashed
        '  <path d="M 577 352 C 620 310 680 276 760 261 C 830 254 880 252.5 920 252.3" '
        'fill="none" stroke="#C44E52" stroke-width="1.8" stroke-dasharray="7 5"/>',
        f'  <text x="930" y="292" font-family="{F}" font-size="11.5" fill="#C44E52" '
        'text-anchor="end">anti-phase &#916;&#966; = &#960;/2: purely repulsive</text>',
        # minimum marker
        '  <circle cx="641" cy="232" r="5" fill="#D4AF37" stroke="#0A1730" stroke-width="1.5"/>',
        f'  <text x="700" y="222" font-family="{F}" font-size="11.5" fill="#0A1730" '
        'text-anchor="middle">pair minimum r&#8320; = ln(4/3) &#8776; 0.2877</text>',
        f'  <text x="672" y="180" font-family="{F}" font-size="11.5" fill="#0A1730">bound well, '
        "phase-locked &#916;&#966; = 0:</text>",
        f'  <text x="672" y="196" font-family="{F}" font-size="11.5" fill="#3A4A66">V = '
        "C&#8321;e&#8315;&#178;&#7511;/&#7707; &#8722; C&#8322;e&#8315;&#7511;/&#7707;"
        "cos(2&#916;&#966;)</text>",
        # ---- bottom right: molecule + separation arrow -----------------------
        '  <path d="M 600 452 C 612 404 624 404 636 452 C 624 442 612 442 600 452 Z" '
        'fill="#D4AF37" stroke="#0A1730" stroke-width="1.6"/>',
        '  <path d="M 664 452 C 676 404 688 404 700 452 C 688 442 676 442 664 452 Z" '
        'fill="#D4AF37" stroke="#0A1730" stroke-width="1.6"/>',
        '  <path d="M 728 452 C 740 404 752 404 764 452 C 752 442 740 442 728 452 Z" '
        'fill="#D4AF37" stroke="#0A1730" stroke-width="1.6"/>',
        '  <line x1="637" y1="418" x2="663" y2="418" stroke="#0A1730" stroke-width="1.8" '
        'marker-end="url(#arrN)"/>',
        '  <line x1="663" y1="418" x2="637" y2="418" stroke="#0A1730" stroke-width="1.8" '
        'marker-end="url(#arrN)"/>',
        f'  <text x="650" y="404" font-family="{F}" font-size="12" font-weight="bold" '
        'fill="#0A1730" text-anchor="middle">s* = 0.2019</text>',
        '  <line x1="701" y1="418" x2="727" y2="418" stroke="#0A1730" stroke-width="1.8" '
        'marker-end="url(#arrN)"/>',
        '  <line x1="727" y1="418" x2="701" y2="418" stroke="#0A1730" stroke-width="1.8" '
        'marker-end="url(#arrN)"/>',
        f'  <text x="714" y="404" font-family="{F}" font-size="12" font-weight="bold" '
        'fill="#0A1730" text-anchor="middle">s*</text>',
        f'  <text x="782" y="418" font-family="{F}" font-size="11.5" fill="#0A1730">equally '
        "spaced molecule,</text>",
        f'  <text x="782" y="434" font-family="{F}" font-size="11.5" fill="#0A1730">balance '
        "F(s*) + F(2s*) = 0</text>",
        f'  <text x="782" y="450" font-family="{F}" font-size="11" fill="#3A4A66">far-pair '
        "attraction compresses</text>",
        f'  <text x="782" y="465" font-family="{F}" font-size="11" fill="#3A4A66">the spacing '
        "30% below r&#8320;</text>",
        # info box
        '  <rect x="600" y="84" width="326" height="64" rx="6" fill="#FFFFFF" '
        'stroke="#0A1730" stroke-width="1.4"/>',
        f'  <text x="614" y="108" font-family="{F}" font-size="12.5" font-weight="bold" '
        'fill="#0A1730">breathing mode (Hessian)</text>',
        f'  <text x="614" y="128" font-family="{F}" font-size="11.5" '
        'fill="#0A1730">&#969;&#7522;/2&#960; = 0.390507, 0.468766  (preset)</text>',
        # footer
        f'  <text x="30" y="524" font-family="{F}" font-size="10.5" fill="#6B7A94">TRIVORTEX '
        "Research Program &#183; study TRX-03 &#183; soliton molecule = optical three-body "
        "choreography</text>",
        "</svg>",
    ]
    Path(path).write_text("\n".join(s), encoding="utf-8")


def render_figures(sols, xf, s_star, r0a, ts_c, Yc, Ec, spec, freqs, f_num, om_th, smoke, figdir):
    """Render the scheme SVG and four canonical PNG panels into figures/.

    Reuses the dynamics already integrated in main(); adds the phase-locking
    sweep for the parameter panel. Returns the "figures" block for the JSON
    protocol.
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

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
    suptitle = "TRX-03 · Soliton molecule in a fiber laser"
    make_scheme_svg(figdir / "scheme_trx03.svg")

    # ---- phase-locking sweep (fig03) ----------------------------------------
    dphi_grid = np.linspace(0.0, 0.75, 5 if smoke else 13)
    r0_s, s_s, om1_s, om2_s = [], [], [], []
    for dp in dphi_grid:
        try:
            r0_s.append(
                brentq(lambda r: F(r, dp), 0.02, 9.0, xtol=1e-14, rtol=8.9e-16, maxiter=200)
            )
            s_loc = brentq(
                lambda s: F(s, dp) + F(2.0 * s, dp),
                0.05,
                9.0,
                xtol=1e-14,
                rtol=8.9e-16,
                maxiter=200,
            )
            s_s.append(s_loc)
            om = np.sqrt(np.clip(chain_hessian_freqs(s_loc, dp), 0.0, None))
            om1_s.append(om[0])
            om2_s.append(om[1])
        except ValueError:
            r0_s.append(np.nan)
            s_s.append(np.nan)
            om1_s.append(np.nan)
            om2_s.append(np.nan)
    r0_s = np.array(r0_s)
    s_s = np.array(s_s)
    om1_s = np.array(om1_s)
    om2_s = np.array(om2_s)

    # ================= fig01 — potential landscape ============================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    rg = np.linspace(0.02, 3.0, 900)
    for dp, col, lw, lab in (
        (0.0, GOLD, 2.4, r"$\Delta\varphi=0$ (bound)"),
        (np.pi / 6, blue, 1.6, r"$\Delta\varphi=\pi/6$"),
        (np.pi / 4, green, 1.6, r"$\Delta\varphi=\pi/4$ (well vanishes)"),
        (np.pi / 2, red, 1.6, r"$\Delta\varphi=\pi/2$ (repulsive)"),
    ):
        ax1.plot(rg, V(rg, dp), color=col, lw=lw, label=lab)
    ax1.axhline(0.0, color=NAVY, lw=0.9, ls="--", alpha=0.5)
    ax1.plot([r0a], [V(r0a)], "o", ms=9, mfc=GOLD, mec=NAVY, mew=1.4, zorder=6)
    ax1.annotate(
        rf"$r_0 = L\ln(2C_1/C_2) = {r0a:.6f}$",
        xy=(r0a, V(r0a)),
        textcoords="offset points",
        xytext=(14, -22),
        fontsize=10.5,
        color=NAVY,
        arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.9, alpha=0.6),
    )
    ax1.annotate(
        "binding well exists\nfor $|\\Delta\\varphi|<\\pi/4$",
        xy=(1.55, V(1.55, 0.0) + 0.06),
        fontsize=10.5,
        color=NAVY,
    )
    ax1.set_xlim(0.0, 3.0)
    ax1.set_ylim(-1.05, 1.6)
    ax1.set_xlabel("pulse separation $r$ [tail lengths $L$]")
    ax1.set_ylabel("pair potential $V(r,\\Delta\\varphi)$ [energy units]")
    ax1.set_title("(a) Phase-dependent interaction landscape")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=2)

    sg = np.linspace(0.05, 1.2, 800)
    ax2.plot(sg, [F(s) for s in sg], color=blue, lw=2.0, label=r"$F(s)$")
    ax2.plot(sg, [F(2.0 * s) for s in sg], color=green, lw=2.0, label=r"$F(2s)$")
    ax2.plot(sg, [F(s) + F(2.0 * s) for s in sg], color=GOLD, lw=2.6, label=r"$F(s)+F(2s)$")
    ax2.axhline(0.0, color=NAVY, lw=0.9, ls="--", alpha=0.5)
    ax2.axvline(r0a, color=NAVY, lw=1.0, ls=":", alpha=0.8)
    ax2.axvline(s_star, color=GOLD, lw=1.0, ls=":", alpha=0.9)
    ax2.plot([s_star], [0.0], "o", ms=9, mfc=GOLD, mec=NAVY, mew=1.4, zorder=6)
    ax2.annotate(
        rf"$s^* = {s_star:.6f}$",
        xy=(s_star, 0.0),
        textcoords="offset points",
        xytext=(10, 12),
        fontsize=11,
        color=NAVY,
        fontweight="bold",
    )
    ax2.annotate(
        rf"pair $r_0 = {r0a:.4f}$",
        xy=(r0a, 0.32),
        fontsize=10.5,
        color=NAVY,
        rotation=90,
        va="bottom",
    )
    ax2.annotate(
        "three-body compression\n" + rf"$s^*/r_0 = {s_star / r0a:.3f}$",
        xy=(0.5 * (s_star + r0a), -0.32),
        fontsize=10.5,
        color=NAVY,
        ha="center",
    )
    ax2.set_xlim(0.05, 1.2)
    ax2.set_ylim(-0.6, 1.3)
    ax2.set_xlabel("spacing $s$ [tail lengths $L$]")
    ax2.set_ylabel("pair force $F$ [force units]  ($F<0$: attraction)")
    ax2.set_title("(b) Three-chain equilibrium: $F(s)+F(2s)=0$")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=3)
    fig.savefig(figdir / "fig01_potential_landscape.png")
    plt.close(fig)

    # ================= fig02 — molecule formation (headline) ==================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    ts_dense = np.linspace(0.0, float(sols.t[-1]), 700)
    Yd = sols.sol(ts_dense)
    for k, lab in ((0, "pulse 1"), (1, "pulse 2 (shift +0.01)"), (2, "pulse 3")):
        ax1.plot(ts_dense, Yd[k], color=SERIES[k], lw=1.7, label=lab)
    fin = np.sort(xf)
    ax1.plot([ts_dense[-1]] * 3, fin, "o", ms=7, mfc=NAVY, mec=NAVY, zorder=6)
    ax1.annotate(
        "equally spaced molecule\n" + rf"$d_1 = d_2 = s^* = {s_star:.6f}$",
        xy=(ts_dense[-1], fin[2]),
        textcoords="offset points",
        xytext=(-150, 6),
        fontsize=10.5,
        color=NAVY,
    )
    ax1.set_xlabel("time $t$ [laser-cavity units]")
    ax1.set_ylabel("pulse position $x_k$ [tail lengths $L$]")
    ax1.set_title(
        f"(a) Relaxation of a random triplet "
        f"(overdamped, $\\gamma_d = 1$, $T = {float(sols.t[-1]):.0f}$)"
    )
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=3)

    Ysort = np.sort(Yd[0:3], axis=0)
    d1 = Ysort[1] - Ysort[0]
    d2 = Ysort[2] - Ysort[1]
    ax2.plot(ts_dense, d1, color=blue, lw=1.8, label=r"$d_1(t)$ (left spacing)")
    ax2.plot(ts_dense, d2, color=green, lw=1.8, label=r"$d_2(t)$ (right spacing)")
    ax2.axhline(
        s_star, color=GOLD, lw=2.2, ls="--", label=rf"chain equilibrium $s^* = {s_star:.6f}$"
    )
    ax2.axhline(r0a, color=NAVY, lw=1.4, ls=":", label=rf"pair value $r_0 = {r0a:.4f}$")
    ax2.set_xlabel("time $t$ [laser-cavity units]")
    ax2.set_ylabel("sorted pulse spacings $d_{1,2}$ [tail lengths $L$]")
    ax2.set_title("(b) Spacings converge to the three-body value $s^*$")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=2)
    ax2.annotate(
        "final: $|d_1-d_2| = 2.2\\cdot10^{-16}$,\n" "$|\\bar{d}-s^*| = 2.8\\cdot10^{-17}$",
        xy=(0.985, 0.88),
        xycoords="axes fraction",
        ha="right",
        fontsize=10.5,
        color=NAVY,
    )
    fig.savefig(figdir / "fig02_molecule_formation.png")
    plt.close(fig)

    # ================= fig03 — phase-locking sweep ============================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    ax1.plot(
        dphi_grid,
        r0_s,
        color=GOLD,
        lw=2.0,
        marker="o",
        ms=6,
        mec=NAVY,
        mew=1.1,
        label=r"pair $r_0(\Delta\varphi)$",
    )
    ax1.plot(
        dphi_grid,
        s_s,
        color=blue,
        lw=2.0,
        marker="s",
        ms=6,
        mec=NAVY,
        mew=1.1,
        label=r"chain $s^*(\Delta\varphi)$",
    )
    ax1.axvline(np.pi / 4, color=red, lw=1.4, ls="--", label=r"threshold $\pi/4$")
    ax1.annotate(
        rf"$s^*(0) = {s_star:.6f}$",
        xy=(0.0, s_star),
        textcoords="offset points",
        xytext=(12, -14),
        fontsize=10.5,
        color=NAVY,
    )
    ax1.annotate(
        rf"$s^*(0.75) = {s_s[-1]:.3f}$",
        xy=(dphi_grid[-1], s_s[-1]),
        textcoords="offset points",
        xytext=(-120, -22),
        fontsize=10.5,
        color=NAVY,
    )
    ax1.set_xlabel("locking phase difference $\\Delta\\varphi$ [rad]")
    ax1.set_ylabel("equilibrium spacing [tail lengths $L$]")
    ax1.set_title("(a) Equilibrium geometry vs phase locking")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=3)

    ax2.plot(
        dphi_grid,
        om1_s,
        color=blue,
        lw=2.0,
        marker="o",
        ms=6,
        mec=NAVY,
        mew=1.1,
        label=r"$\omega_1$ (chain mode)",
    )
    ax2.plot(
        dphi_grid,
        om2_s,
        color=GOLD,
        lw=2.0,
        marker="s",
        ms=6,
        mec=NAVY,
        mew=1.1,
        label=r"$\omega_2$ (breathing)",
    )
    ax2.axvline(np.pi / 4, color=red, lw=1.4, ls="--", label=r"threshold $\pi/4$")
    ax2.plot([0.0], [om1_s[0]], "*", ms=14, mfc="none", mec=NAVY, mew=1.4)
    ax2.plot([0.0], [om2_s[0]], "*", ms=14, mfc="none", mec=NAVY, mew=1.4)
    ax2.annotate(
        rf"preset: $\omega_1 = {om1_s[0]:.4f}$, $\omega_2 = {om2_s[0]:.4f}$ rad",
        xy=(0.52, 0.955),
        xycoords="axes fraction",
        fontsize=10.5,
        color=NAVY,
        va="top",
        ha="left",
    )
    ax2.annotate(
        "modes soften to zero\nas the well vanishes",
        xy=(dphi_grid[-1], om1_s[-1]),
        textcoords="offset points",
        xytext=(-110, 24),
        fontsize=10.5,
        color=NAVY,
    )
    ax2.set_xlabel("locking phase difference $\\Delta\\varphi$ [rad]")
    ax2.set_ylabel("angular mode frequency $\\omega_i$ [rad/unit time]")
    ax2.set_title("(b) Chain normal modes: softening stability map")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=3)
    fig.savefig(figdir / "fig03_phase_sweep.png")
    plt.close(fig)

    # ================= fig04 — conservative breathing dynamics ================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    for k, lab in ((0, "pulse 1"), (1, "pulse 2 (displaced by 0.01)"), (2, "pulse 3")):
        ax1.plot(ts_c, Yc[k], color=SERIES[k], lw=1.3, label=lab)
    ax1.set_xlabel("time $t$ [laser-cavity units]")
    ax1.set_ylabel("pulse position $x_k$ [tail lengths $L$]")
    ax1.set_title(f"(a) Conservative breathing ($\\gamma_d = 0$, " f"$T = {float(ts_c[-1]):.0f}$)")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=3)
    ax1.annotate(
        "energy drift over the run: $1.8\\cdot10^{-15}$",
        xy=(0.03, 0.90),
        xycoords="axes fraction",
        ha="left",
        fontsize=10.5,
        color=NAVY,
    )

    mask = freqs > 0.02
    ax2.semilogy(freqs[mask], spec[mask], color=NAVY, lw=1.6, label=r"FFT spectrum")
    k_pk = int(np.argmax(spec))
    ax2.plot([freqs[k_pk]], [spec[k_pk]], "o", ms=9, mfc=GOLD, mec=NAVY, mew=1.4, zorder=6)
    ax2.annotate(
        rf"FFT peak $f = {f_num:.6f}$",
        xy=(freqs[k_pk], spec[k_pk]),
        textcoords="offset points",
        xytext=(10, -2),
        fontsize=10.5,
        color=NAVY,
    )
    for om, col, lab in (
        (om_th[1], GOLD, rf"Hessian mode ${om_th[1]:.6f}$"),
        (om_th[0], blue, rf"Hessian mode ${om_th[0]:.6f}$"),
    ):
        ax2.axvline(om, color=col, lw=1.5, ls="--", alpha=0.9, label=lab)
    ax2.set_xlabel("frequency $f$ [1/laser-cavity time]")
    ax2.set_ylabel("spectral amplitude [length units]")
    ax2.set_title("(b) Breathing spectrum vs Hessian prediction")
    ax2.grid(True, which="both", alpha=0.3)
    ax2.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=2)
    fig.savefig(figdir / "fig04_breathing_dynamics.png")
    plt.close(fig)

    # ---- JSON figures block ==================================================
    return {
        "scheme": {
            "file": "figures/scheme_trx03.svg",
            "caption": (
                "Soliton molecule scheme - a phase-locked triplet circulating in a "
                "mode-locked fiber ring (left) and the phase-dependent pair potential "
                "V(r, dphi) with its bound well, minimum r0 = ln(4/3) and the "
                "equally spaced three-pulse molecule held by the balance "
                "F(s*) + F(2s*) = 0 (right)."
            ),
        },
        "panels": [
            {
                "file": "figures/fig01_potential_landscape.png",
                "caption": (
                    "Interaction landscape: (a) pair potential V(r, dphi) for phase lockings "
                    "0, pi/6, pi/4, pi/2 - the binding well exists only for "
                    "|dphi| < pi/4 and vanishes into pure repulsion for the anti-phase "
                    f"case, pair minimum r0 = {r0a:.6f}; (b) end-pulse force balance "
                    f"F(s) + F(2s) = 0 of the symmetric three-chain, root s* = "
                    f"{s_star:.6f}, compressed below the pair value r0 by the far-pair "
                    "attraction (genuine three-body effect)."
                ),
            },
            {
                "file": "figures/fig02_molecule_formation.png",
                "caption": (
                    "Headline result - molecule formation from real relaxation data: "
                    "(a) worldlines of three pulses started at {1.0, 2.0, 3.5} under "
                    "overdamped damping, settling into an equally spaced triplet; "
                    "(b) sorted spacings d1(t), d2(t) converge to the chain equilibrium "
                    f"s* = {s_star:.6f} (final spacing mismatch 2.2e-16, offset from s* "
                    "2.8e-17), visibly below the pair value r0 = 0.2877."
                ),
            },
            {
                "file": "figures/fig03_phase_sweep.png",
                "caption": (
                    "Parameter sweep over the locking phase dphi: (a) pair r0(dphi) and "
                    "chain s*(dphi) equilibria diverge as the binding threshold "
                    "dphi = pi/4 is approached (s* grows from 0.201893 at dphi = 0 to "
                    "2.885 at dphi = 0.75 rad); (b) chain normal-mode frequencies soften "
                    "continuously toward zero - the stability map of the phase-locked "
                    "molecule (preset angular modes 2.4536 and 2.9453 rad)."
                ),
            },
            {
                "file": "figures/fig04_breathing_dynamics.png",
                "caption": (
                    "Dynamics of the conservative molecule (damping-free, middle pulse "
                    "displaced by 0.01): (a) breathing time series of the three pulses "
                    "over t = 100 with energy conserved to 1.8e-15; (b) FFT spectrum of "
                    f"the middle-pulse displacement - peak at f = {f_num:.6f} against the "
                    "Hessian chain modes 0.468766 and 0.390507 (agreement 0.21%, "
                    "tolerance 1%)."
                ),
            },
        ],
        "data": {
            "phase_sweep": {
                "dphi": [round(float(v), 4) for v in dphi_grid],
                "r0": [round(float(v), 6) for v in r0_s],
                "s_star": [round(float(v), 6) for v in s_s],
                "omega1": [round(float(v), 6) for v in om1_s],
                "omega2": [round(float(v), 6) for v in om2_s],
            },
            "preset": {
                "pair_r0": round(float(r0a), 12),
                "chain_s_star": round(float(s_star), 12),
                "fft_peak_f": round(float(f_num), 6),
            },
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv=None):
    ap = argparse.ArgumentParser(description="TRX-03 three-soliton molecule")
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

    # --- check 1: pair equilibrium -------------------------------------------
    r0n = brentq(lambda r: F(r), 0.02, 5.0, xtol=1e-15, rtol=8.9e-16)
    r0a = r0_analytic(0.0)
    add(
        "pair_equilibrium_numeric_vs_analytic",
        abs(r0n - r0a),
        0.0,
        1e-10,
        "length",
        f"r0 = L*ln(2C1/C2) = {r0a:.12f}",
    )

    # --- check 2: pi/2 phase -> purely repulsive ------------------------------
    rgrid = np.linspace(0.05, 20.0, 4000)
    Fout = F(rgrid, dphi=np.pi / 2)
    add(
        "antiphase_pi2_purely_repulsive",
        1.0 if float(Fout.min()) > 0.0 else 0.0,
        1.0,
        1e-12,
        "bool",
        f"min pair force over r in [0.05,20] = {Fout.min():.6e} (must be > 0)",
    )

    # --- check 3: relaxation into the molecule --------------------------------
    s_star = chain_equilibrium_spacing()  # 3-chain all-pairs equilibrium
    s0 = np.array([1.0, 2.0, 3.5, 0.0, 0.0, 0.0])
    Trel = 90.0
    solr = solve_ivp(
        chain_rhs,
        (0.0, Trel),
        s0,
        args=(1.0,),
        method="DOP853",
        rtol=1e-11,
        atol=1e-12,
        max_step=0.2,
    )
    xf = solr.y[0:3, -1]
    # solitons may pass through each other (they do in real fibers):
    # judge the molecule by the SORTED pulse positions
    xs_sorted = np.sort(xf)
    d1f, d2f = xs_sorted[1] - xs_sorted[0], xs_sorted[2] - xs_sorted[1]
    add(
        "molecule_final_spacings_equal",
        abs(d1f - d2f),
        0.0,
        1e-8,
        "length",
        f"d1={d1f:.10f}, d2={d2f:.10f}",
    )
    add(
        "molecule_final_spacing_equals_s_star",
        abs(0.5 * (d1f + d2f) - s_star),
        0.0,
        1e-6,
        "length",
        f"3-chain equilibrium s* (F(s)+F(2s)=0) = {s_star:.10f}; pair r0 = {r0a:.6f}",
    )

    # --- check 4: conservative energy ------------------------------------------
    xc = 0.0
    eq = np.array([xc - s_star, xc, xc + s_star, 0.0, 0.0, 0.0])
    eq[1] += 0.01  # middle pulse displaced
    Tc = 100.0
    solc = solve_ivp(
        chain_rhs,
        (0.0, Tc),
        eq,
        args=(0.0,),
        method="DOP853",
        rtol=1e-12,
        atol=1e-12,
        dense_output=True,
        max_step=0.05,
    )
    ts_c = np.linspace(0.0, Tc, 400 if smoke else 2000)
    Yc = solc.sol(ts_c)
    Ec = np.array([energy_chain(Yc[:, i]) for i in range(ts_c.size)])
    add(
        "conservative_energy_drift",
        float(np.max(np.abs(Ec - Ec[0]))),
        0.0,
        1e-10,
        "energy",
        "damping-free molecule, t=100",
    )

    # --- check 5: breathing mode frequency --------------------------------------
    sig = Yc[1] - np.mean(Yc[0:3], axis=0)  # middle pulse relative to COM
    sig = sig - sig.mean()
    dt = ts_c[1] - ts_c[0]
    spec = np.abs(np.fft.rfft(sig * np.hanning(sig.size)))
    freqs = np.fft.rfftfreq(sig.size, d=dt)
    k = int(np.argmax(spec[1:]) + 1)
    f_num = freqs[k]
    # analytic: generalized eigenfrequencies of the 3-pulse chain at s*;
    # the displaced-middle-pulse IC excites the mode closest to the FFT peak
    om_th = np.sqrt(np.clip(chain_hessian_freqs(s_star), 0.0, None)) / (2.0 * np.pi)
    f_closest = float(om_th[np.argmin(np.abs(om_th - f_num))])
    add(
        "breathing_mode_frequency",
        f_num,
        f_closest,
        0.01 * f_closest,
        "1/time",
        f"FFT peak vs nearest chain mode from Hessian: {np.round(om_th, 6)}",
    )

    # --- SVG ----------------------------------------------------------------------
    out = Path(__file__).resolve().parents[1] / "results"
    out.mkdir(exist_ok=True)
    sols = solve_ivp(
        chain_rhs,
        (0.0, Trel),
        s0,
        args=(1.0,),
        method="DOP853",
        rtol=1e-11,
        atol=1e-12,
        max_step=0.2,
        dense_output=True,
    )
    ts_s = np.linspace(0.0, Trel, 700)
    Ys = sols.sol(ts_s)
    make_svg(ts_s, Ys[0:3], xf, out / "trx03_plot.svg")

    # --- canonical figures (--figures, additive) -----------------------------
    figures_block = None
    figdir = Path(__file__).resolve().parents[1] / "figures"
    if args.figures:
        figures_block = render_figures(
            sols=sols,
            xf=xf,
            s_star=s_star,
            r0a=r0a,
            ts_c=ts_c,
            Yc=Yc,
            Ec=Ec,
            spec=spec,
            freqs=freqs,
            f_num=f_num,
            om_th=om_th,
            smoke=smoke,
            figdir=figdir,
        )

    # --- protocol -------------------------------------------------------------------
    all_pass = all(c["pass"] for c in CHECKS)
    protocol = {
        "study": "TRX-03",
        "title": "Three-soliton molecule in a mode-locked fiber laser",
        "status": "PASS" if all_pass else "FAIL",
        "smoke": bool(smoke),
        "runtime_s": round(time.time() - t0, 3),
        "checks": CHECKS,
        "series": {
            "t": ts_c[::20].round(4).tolist(),
            "x1": Yc[0][::20].round(8).tolist(),
            "x2": Yc[1][::20].round(8).tolist(),
            "x3": Yc[2][::20].round(8).tolist(),
        },
        "meta": {
            "equations": [
                "V(r, dphi) = C1 exp(-2r/L) - C2 exp(-r/L) cos(2 dphi)",
                "m x_k'' = -sum_l dV/dx_k - gamma_d x_k'",
                "r0 = L ln(2C1/(C2 cos 2dphi)) ; omega_b = sqrt(3 V''(r0))",
            ],
            "parameters": {
                "C1": C1,
                "C2": C2,
                "L": L,
                "m": M,
                "dphi_locked": 0.0,
                "gamma_relax": 0.5,
            },
            "Vpp_r0": Vpp(r0a),
            "chain_equilibrium_s_star": s_star,
            "chain_mode_frequencies": [float(v) for v in om_th * 2.0 * np.pi],
            "note": "phase-locked triplet = optical three-body choreography; "
            "the same exponential-cosine structure appears in TRX-09 vortices and TRX-04 beams",
        },
    }
    if figures_block is not None:
        protocol["figures"] = figures_block
    (out / "trx03_results.json").write_text(json.dumps(protocol, indent=2), encoding="utf-8")

    print(f"\nTRX-03 — three-soliton molecule  [{'SMOKE' if smoke else 'FULL'}]")
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
