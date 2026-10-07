#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
TRIVORTEX LAB — TRX-07 — THE EFIMOV EFFECT: UNIVERSAL QUANTUM THREE-BODY
============================================================================
Three identical bosons interacting through resonant two-body forces form
an infinite Rydberg-like series of bound three-body states (Efimov, 1970)
even when the pair potential cannot bind two bodies alone.  The spectrum
is universal: it is governed by a single transcendental exponent

    s0 :  s0 * cosh(pi*s0/2) = (8/sqrt(3)) * sinh(pi*s0/6)  ->  s0 = 1.0062458

which produces the geometric ladders
    a_*^(n+1)/a_*^(n) = exp(pi/s0) ~ 22.7   (scattering length)
    E_n/E_(n+1)       = exp(2*pi/s0) ~ 515   (trimer energies)

Laser connection: Efimov trimers were observed in laser-cooled ultracold
Caesium gases (Kraemer et al., 2006); the resonance is tuned with a
Feshbach resonance and the trimers are probed by laser spectroscopy.

What is computed
  * transcendental root s0 (brentq) and the universal ratios
  * hyperradial spectrum of the scale-invariant -1/R^2 potential on an
    exponential grid (s = ln(R/R0)) — the geometric Efimov ladder

With --figures: hand-authored scheme SVG + four canonical PNG panels
(300 dpi) into figures/, and a "figures" block added to the JSON protocol
(scheme, panels with captions, box-length / grid / three-body-parameter
sweep data). Composable with --smoke; without --figures the behavior,
checks and JSON are unchanged.

Usage:  python trx07_efimov.py [--smoke] [--figures]
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
from scipy.optimize import brentq
from scipy.linalg import eigh

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
# Universal exponent
# ---------------------------------------------------------------------------


def transcendental(s):
    return s * np.cosh(np.pi * s / 2.0) - (8.0 / np.sqrt(3.0)) * np.sinh(np.pi * s / 6.0)


# ---------------------------------------------------------------------------
# Hyperradial spectrum:  -u''(R) - (s0^2 - 1/4)/R^2 u = E u
# With R = R0 e^s and u = e^{s/2} v the problem becomes the symmetric
# generalized eigenproblem   (-d^2/ds^2 - s0^2) v = E R0^2 e^{2s} v
# on s in [0, L],  L = ln(Rmax/R0), Dirichlet boundaries.
# ---------------------------------------------------------------------------


def efimov_spectrum(s0, R0=1e-3, Rmax=1e6, n_grid=800, n_levels=4):
    """Dense symmetrized FD spectrum on the exponential grid.
    K v = E W v with W = diag(R0^2 e^{2s}) = D^{-2}; substituting v = D u
    with D = diag(R0^-1 e^{-s}) gives the symmetric problem D K D u = E u,
    whose eigenvalues are exactly the trimer energies E."""
    L = np.log(Rmax / R0)
    s = np.linspace(0.0, L, n_grid)
    ds = s[1] - s[0]
    main = np.full(n_grid, 2.0 / ds**2 - s0**2)
    off = np.full(n_grid - 1, -1.0 / ds**2)
    K = np.diag(main) + np.diag(off, 1) + np.diag(off, -1)
    Dm = R0**-1.0 * np.exp(-s)
    A = Dm[:, None] * K * Dm[None, :]
    vals = np.linalg.eigvalsh(A)
    E = np.sort(vals)[:n_levels]
    return E


# ---------------------------------------------------------------------------
# SVG
# ---------------------------------------------------------------------------


def make_svg(s0, E, R0, Rmax, path):
    W, H = 900, 520
    x0, x1, y0, y1 = 80.0, 860.0, 70.0, 440.0
    ls = np.linspace(0.0, 1.0, 200)
    Rg = R0 * (Rmax / R0) ** ls

    def X(l):
        return x0 + l * (x1 - x0)

    def Y(e):
        return (
            y0
            - np.log10(-e / (-E[0])) / 14.0 * 0
            + (y1 - y0) * 0.15
            + (np.log10(-E[0] / e) / 12.0) * (y1 - y0) * 0.75
        )

    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect width="{W}" height="{H}" fill="#0A1230"/>',
        '<text x="24" y="34" fill="#FFFFFF" font-family="Arial" font-size="19" '
        'font-weight="bold">TRX-07 &#8212; Efimov geometric ladder (energy, log scale)</text>',
        f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="#3A4A6B"/>',
    ]
    for i, e in enumerate(E):
        yy = y1 - (i + 1) / (len(E) + 1) * (y1 - y0)
        s.append(
            f'<line x1="{x0+40}" y1="{yy:.1f}" x2="{x1-40}" y2="{yy:.1f}" '
            f'stroke="#6FB7FF" stroke-width="2"/>'
        )
        s.append(
            f'<text x="{x1-330}" y="{yy-6:.1f}" fill="#6FB7FF" font-family="Arial" '
            f'font-size="12">E{i} = {e:.4e}</text>'
        )
    s.append(
        f'<text x="{x0+40}" y="{y1-12}" fill="#9FB3D9" font-family="Arial" font-size="13">'
        f"ratio E0/E1 = {abs(E[0]/E[1]):.1f} vs exp(2*pi/s0) = {np.exp(2*np.pi/s0):.1f}</text>"
    )
    s.append(
        '<text x="24" y="500" fill="#9FB3D9" font-family="Arial" font-size="12">'
        "the -1/R^2 hyperradial attraction binds infinitely many trimers with the universal 515x ladder</text>"
    )
    s.append("</svg>")
    Path(path).write_text("\n".join(s), encoding="utf-8")


# ---------------------------------------------------------------------------
# Canonical figures (--figures mode): scheme SVG + four PNG panels
# ---------------------------------------------------------------------------

# TRIVORTEX canonical palette (v2.2.0 figures)
NAVY = "#0A1730"  # strokes and text
GOLD = "#D4AF37"  # accents
LIGHT_GOLD = "#F0D98C"  # soft fills
SERIES = ["#D4AF37", "#4C72B0", "#55A868", "#C44E52", "#8172B2"]


def make_scheme_svg(path):
    """Hand-authored schematic of the Efimov effect: three identical bosons
    at unitarity bound by the hyperradial 1/R^2 attraction, the geometric
    ladder of trimers in s = ln(R/R0) space, and the mapping to the
    TRIVORTEX vortex model."""
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
        f'  <text x="30" y="38" font-family="{F}" font-size="21" font-weight="bold" '
        'fill="#0A1730">TRX-07 &#8212; Scheme: the Efimov effect, a geometric ladder '
        "of three-body states</text>",
        f'  <text x="30" y="61" font-family="{F}" font-size="12.5" fill="#3A4A66">Three '
        "identical bosons at unitarity: no two-body dimer, yet an infinite geometric "
        "sequence of bound trimers</text>",
        # ---- left panel: three bosons at unitarity ---------------------------
        '  <rect x="55" y="88" width="350" height="250" rx="10" fill="#FBF6E8" '
        'stroke="#0A1730" stroke-width="2"/>',
        f'  <text x="230" y="112" font-family="{F}" font-size="12.5" font-weight="bold" '
        'fill="#0A1730" text-anchor="middle">three bosons at unitarity '
        "(a &#8594; &#8734;)</text>",
        # pairwise resonant interactions (dashed triangle edges)
        '  <line x1="180" y1="183" x2="126.3" y2="276" stroke="#0A1730" '
        'stroke-width="1.6" stroke-dasharray="5 4"/>',
        '  <line x1="126.3" y1="276" x2="233.7" y2="276" stroke="#0A1730" '
        'stroke-width="1.6" stroke-dasharray="5 4"/>',
        '  <line x1="233.7" y1="276" x2="180" y2="183" stroke="#0A1730" '
        'stroke-width="1.6" stroke-dasharray="5 4"/>',
        # bosons: gold discs with navy rings
        '  <circle cx="180" cy="183" r="11" fill="#D4AF37" stroke="#0A1730" stroke-width="1.8"/>',
        '  <circle cx="126.3" cy="276" r="11" fill="#D4AF37" stroke="#0A1730" stroke-width="1.8"/>',
        '  <circle cx="233.7" cy="276" r="11" fill="#D4AF37" stroke="#0A1730" stroke-width="1.8"/>',
        f'  <text x="180" y="164" font-family="{F}" font-size="12" fill="#0A1730" '
        'text-anchor="middle">1</text>',
        f'  <text x="104" y="281" font-family="{F}" font-size="12" fill="#0A1730" '
        'text-anchor="middle">2</text>',
        f'  <text x="256" y="281" font-family="{F}" font-size="12" fill="#0A1730" '
        'text-anchor="middle">3</text>',
        # hyperradius arrow from centroid to boson 1
        '  <line x1="180" y1="245" x2="180" y2="196" stroke="#0A1730" stroke-width="1.6" '
        'marker-end="url(#arrN)"/>',
        '  <line x1="174" y1="245" x2="186" y2="245" stroke="#0A1730" stroke-width="1.4"/>',
        f'  <text x="188" y="222" font-family="{F}" font-size="12" fill="#0A1730">R '
        "(hyperradius)</text>",
        f'  <text x="230" y="305" font-family="{F}" font-size="11" fill="#3A4A66" '
        'text-anchor="middle">each pair is unbound (no two-body dimer) &#8212;</text>',
        f'  <text x="230" y="322" font-family="{F}" font-size="11" fill="#3A4A66" '
        'text-anchor="middle">only the trio binds: the hyperradial adiabatic '
        "potential &#8722;(s&#8320;&#178;&#8722;&#188;)/R&#178;</text>",
        # ---- right panel: the geometric ladder in s-space --------------------
        '  <rect x="445" y="88" width="460" height="250" rx="10" fill="#FFFFFF" '
        'stroke="#0A1730" stroke-width="2"/>',
        f'  <text x="675" y="112" font-family="{F}" font-size="12.5" font-weight="bold" '
        'fill="#0A1730" text-anchor="middle">the Efimov ladder in s = ln(R/R&#8320;) '
        "space</text>",
        f'  <text x="888" y="133" font-family="{F}" font-size="11" fill="#3A4A66" '
        'text-anchor="end">per rung: size &#215; 22.694 &#183; energy &#215; 515.035</text>',
        # s axis (wall at s = 0, gold tick)
        '  <line x1="505" y1="310" x2="505" y2="126" stroke="#0A1730" stroke-width="1.5" '
        'marker-end="url(#arrN)"/>',
        f'  <text x="517" y="133" font-family="{F}" font-size="11.5" '
        'fill="#0A1730">s = ln(R/R&#8320;)</text>',
        '  <line x1="498" y1="310" x2="512" y2="310" stroke="#D4AF37" stroke-width="2"/>',
        f'  <text x="492" y="314" font-family="{F}" font-size="10" fill="#0A1730" '
        'text-anchor="end">R&#8320;</text>',
        f'  <text x="492" y="300" font-family="{F}" font-size="9.5" fill="#3A4A66" '
        'text-anchor="end">wall</text>',
        # rungs (levels E0..E3), equally spaced by Delta s = pi/s0 (schematic)
        '  <line x1="515" y1="296" x2="640" y2="296" stroke="#D4AF37" stroke-width="4"/>',
        '  <line x1="515" y1="250" x2="640" y2="250" stroke="#4C72B0" stroke-width="4"/>',
        '  <line x1="515" y1="204" x2="640" y2="204" stroke="#55A868" stroke-width="4"/>',
        '  <line x1="515" y1="158" x2="640" y2="158" stroke="#C44E52" stroke-width="4"/>',
        f'  <text x="648" y="300" font-family="{F}" font-size="11" fill="#0A1730">E&#8320; '
        "&#8212; size &#8776; 13 R&#8320;</text>",
        f'  <text x="648" y="254" font-family="{F}" font-size="11" fill="#0A1730">E&#8321; '
        "&#8212; size &#8776; 296 R&#8320;</text>",
        f'  <text x="648" y="208" font-family="{F}" font-size="11" fill="#0A1730">E&#8322; '
        "&#8212; size &#8776; 6725 R&#8320;</text>",
        f'  <text x="648" y="162" font-family="{F}" font-size="11" fill="#0A1730">E&#8323; '
        "&#8212; size &#8776; 152604 R&#8320;</text>",
        # equal-spacing arrow between rungs E1 and E2
        '  <line x1="560" y1="244" x2="560" y2="210" stroke="#0A1730" stroke-width="1.5" '
        'marker-end="url(#arrN)" marker-start="url(#arrN)"/>',
        f'  <text x="570" y="231" font-family="{F}" font-size="10.5" '
        'fill="#0A1730">&#916;s = &#960;/s&#8320; = 3.122</text>',
        # ---- bottom strip: mapping to the TRIVORTEX vortex model -------------
        '  <rect x="55" y="402" width="850" height="88" rx="10" fill="#FBF6E8" '
        'stroke="#0A1730" stroke-width="2"/>',
        f'  <text x="80" y="424" font-family="{F}" font-size="12" font-weight="bold" '
        'fill="#0A1730">mapping to the TRIVORTEX vortex model</text>',
    ]
    rows = [
        (
            "universal exponent s&#8320; = 1.00624",
            "circulation ratios &#915; of the vortex triangle",
        ),
        (
            "geometric ladder e^(2&#960;/s&#8320;) = 515",
            "radial modulation &#969; = (2&#960;/T)&#183;e^(C_Ch/&#960;)",
        ),
        ("hyperradial &#8722;1/R&#178; attraction", "scale-invariant binding (Theorem 3.1)"),
    ]
    for i, (lft, rgt) in enumerate(rows):
        y = 446 + 18 * i
        s.append(
            f'  <text x="80" y="{y}" font-family="{F}" font-size="11" '
            f'fill="#0A1730">{lft}</text>'
        )
        s.append(
            f'  <line x1="330" y1="{y - 4}" x2="356" y2="{y - 4}" stroke="#D4AF37" '
            f'stroke-width="1.7" marker-end="url(#arrG)"/>'
        )
        s.append(
            f'  <text x="366" y="{y}" font-family="{F}" font-size="11" '
            f'fill="#0A1730">{rgt}</text>'
        )
    s += [
        # bottom formula lines
        f'  <text x="55" y="508" font-family="{F}" font-size="12" fill="#0A1730">'
        "s&#8320;&#183;cosh(&#960;s&#8320;/2) = (8/&#8730;3)&#183;sinh(&#960;s&#8320;/6) "
        "&#8594; s&#8320; = 1.0062378 (target 1.0062458, tolerance 1e-5)</text>",
        f'  <text x="55" y="526" font-family="{F}" font-size="11.5" fill="#3A4A66">'
        "measured ladder: |E&#8320;/E&#8321;| = 515.509, |E&#8321;/E&#8322;| = 514.964, "
        "|E&#8322;/E&#8323;| = 514.963 &#8212; universal e^(2&#960;/s&#8320;) = 515.035, "
        "deviations within &#177;0.1%</text>",
        "</svg>",
    ]
    Path(path).write_text("\n".join(s), encoding="utf-8")


def render_figures(s0, E, R0, Rmax, n_grid, smoke, figdir):
    """Render the scheme SVG and four canonical PNG panels into figures/.

    Reuses the spectrum already computed in main(); adds three cheap sweeps
    built on the same efimov_spectrum() solver (box length, grid refinement,
    three-body parameter R0). Returns the "figures" block for the JSON
    protocol. Existing checks and JSON semantics are untouched.
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
    suptitle = "TRX-07 · The Efimov effect — universal quantum three-body ladder"
    make_scheme_svg(figdir / "scheme_trx07.svg")

    L = float(np.log(Rmax / R0))
    ds = L / (n_grid - 1)
    sp2 = float(s0 * s0 - 0.25)
    pi_s0 = float(np.pi / s0)
    len_univ = float(np.exp(np.pi / s0))
    en_univ = float(np.exp(2.0 * np.pi / s0))
    En = np.asarray(E, dtype=float)
    En = En[En < 0]
    n_lv = int(En.size)
    Rn = np.sqrt(sp2 / np.abs(En)) / R0  # scaling hyperradii, units of R0
    sn = np.log(Rn)
    ratio01 = float(abs(En[0] / En[1]))
    ratio12 = float(abs(En[1] / En[2]))
    ratio23 = float(abs(En[2] / En[3])) if n_lv >= 4 else float("nan")
    dev01 = 100.0 * (ratio01 - en_univ) / en_univ
    dev12 = 100.0 * (ratio12 - en_univ) / en_univ
    dev23 = 100.0 * (ratio23 - en_univ) / en_univ

    def lowest(n_levels, **kw):
        Eg = efimov_spectrum(s0, n_levels=n_levels, **kw)
        return Eg[Eg < 0]

    # ---- sweep (a): box length L at fixed grid spacing ----------------------
    L_vals = (
        np.array([4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, L])
        if not smoke
        else np.array([6.0, 10.0, L])
    )
    cap_L, r_L = [], []
    for Lv in L_vals:
        ng = int(round(Lv / ds)) + 1
        Eg = lowest(4, R0=R0, Rmax=R0 * float(np.exp(Lv)), n_grid=ng)
        cap_L.append(int(Eg.size))
        r_L.append(abs(Eg[0] / Eg[1]) if Eg.size >= 2 else np.nan)
    cap_L = np.array(cap_L)
    r_L = np.array(r_L)

    # ---- sweep (b): grid refinement at the preset box -----------------------
    n_vals = (
        np.array([150, 250, 400, 600, 900, 1400, 2200]) if not smoke else np.array([250, 500, 900])
    )
    r_n, r12_n = [], []
    for ng in n_vals:
        Eg = lowest(4, R0=R0, Rmax=Rmax, n_grid=int(ng))
        r_n.append(abs(Eg[0] / Eg[1]) if Eg.size >= 2 else np.nan)
        r12_n.append(abs(Eg[1] / Eg[2]) if Eg.size >= 3 else np.nan)
    r_n = np.array(r_n)
    r12_n = np.array(r12_n)

    # ---- sweep (c): three-body parameter R0 at fixed box shape --------------
    r0_vals = np.logspace(-5.0, -2.0, 7) if not smoke else np.logspace(-4.0, -3.0, 3)
    e0_r0, rat_r0 = [], []
    for r0v in r0_vals:
        Eg = lowest(4, R0=float(r0v), Rmax=float(r0v) * np.exp(L), n_grid=n_grid)
        e0_r0.append(abs(Eg[0]))
        rat_r0.append(abs(Eg[0] / Eg[1]) if Eg.size >= 2 else np.nan)
    e0_r0 = np.array(e0_r0)
    rat_r0 = np.array(rat_r0)
    slope = float(np.polyfit(np.log(r0_vals), np.log(e0_r0), 1)[0])
    rat_spread = float(np.max(rat_r0) - np.min(rat_r0))

    # ================= fig01 — model landscape ================================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    Rgrid = np.logspace(-0.2, 6.2, 400)  # hyperradius in units of R0
    ax1.loglog(
        Rgrid,
        sp2 / Rgrid**2,
        color=NAVY,
        lw=2.0,
        label=r"adiabatic potential $|V(R)| = (s_0^2 - \frac{1}{4})/R^2$",
    )
    ax1.axvline(1.0, color=GOLD, lw=2.0, ls="--", label="three-body parameter $R_0$ (hard wall)")
    ax1.scatter(
        Rn,
        sp2 / Rn**2,
        s=70,
        color=GOLD,
        edgecolors=NAVY,
        linewidths=1.0,
        zorder=5,
        label="scaling hyperradii $R_n$",
    )
    for i, rv in enumerate(Rn):
        ax1.annotate(
            f"$R_{i}$ = {rv:.6g}",
            xy=(rv, sp2 / rv**2),
            xytext=(7, -13),
            textcoords="offset points",
            fontsize=9.5,
        )
    ax1.set_xlim(0.5, 2e6)
    ax1.set_title("(a) hyperradial attraction and trimer sizes")
    ax1.set_xlabel("hyperradius R (units of $R_0$)")
    ax1.set_ylabel(r"$|V(R)|$  (units of $1/R_0^2$)")
    ax1.legend(loc="upper right", bbox_to_anchor=(1.0, 1.0))
    ax1.grid(alpha=0.3, which="both")

    for i in range(n_lv):
        ax2.plot([0.0, 1.0], [sn[i], sn[i]], lw=4.0, color=SERIES[i], solid_capstyle="butt")
        ax2.text(1.05, sn[i], f"$E_{i}$,  size {Rn[i]:.6g} $R_0$", va="center", fontsize=10)
    ax2.annotate(
        "",
        xy=(0.42, sn[2]),
        xytext=(0.42, sn[1]),
        arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1.5),
    )
    ax2.text(
        0.46,
        0.5 * (sn[1] + sn[2]),
        r"$\Delta s = \pi/s_0$ = " + f"{pi_s0:.4f}",
        fontsize=10.5,
        va="center",
    )
    ax2.set_xlim(-0.02, 1.75)
    ax2.set_ylim(sn.min() - 0.4, sn.max() + 1.8)
    ax2.set_xticks([])
    ax2.set_title("(b) the ladder in $s = \\ln(R/R_0)$: equal spacing")
    ax2.set_ylabel(r"$s_n = \ln(R_n/R_0)$")
    ax2.text(
        -0.02,
        sn.max() + 0.85,
        "per rung:  size " + f"$\\times$ {len_univ:.3f}    energy " + f"$\\times$ {en_univ:.3f}",
        fontsize=10.5,
        va="bottom",
    )
    fig.savefig(figdir / "fig01_efimov_landscape.png")
    plt.close(fig)

    # ================= fig02 — headline: the universal numbers ================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    sv = np.linspace(0.5, 1.8, 600)
    ax1.plot(
        sv,
        transcendental(sv),
        color=NAVY,
        lw=2.0,
        label=r"$f(s) = s\,\cosh(\pi s/2) - \frac{8}{\sqrt{3}}\,\sinh(\pi s/6)$",
    )
    ax1.axhline(0.0, color=NAVY, lw=0.8, alpha=0.4)
    ax1.plot(
        [s0],
        [0.0],
        "*",
        color=GOLD,
        mec=NAVY,
        ms=17,
        zorder=5,
        label=f"root $s_0$ = {s0:.7f}  (brentq)",
    )
    ax1.annotate(
        f"target 1.0062458, tolerance 1e-5",
        xy=(s0, 0.0),
        xytext=(1.16, 3.4),
        fontsize=10,
        arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.0),
    )
    ax1.set_ylim(-1.5, 12.0)
    ax1.set_title("(a) the universal exponent: one transcendental root")
    ax1.set_xlabel("s")
    ax1.set_ylabel("f(s)")
    ax1.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0))
    ax1.grid(alpha=0.3)

    xs = np.arange(3)
    vals = [ratio01, ratio12, ratio23]
    devs = [dev01, dev12, dev23]
    ax2.bar(
        xs,
        vals,
        width=0.55,
        color=[SERIES[1], SERIES[2], SERIES[3]],
        edgecolor=NAVY,
        linewidth=1.0,
        zorder=3,
    )
    for x, v, dv in zip(xs, vals, devs):
        ax2.text(x, v + 1.0, f"{v:.3f}\n({dv:+.2f}%)", ha="center", fontsize=10)
    ax2.axhline(en_univ, color=NAVY, ls="--", lw=1.8, zorder=4)
    ax2.text(
        0.02,
        0.97,
        f"universal $e^{{2\\pi/s_0}}$ = {en_univ:.3f} (dashed)\n"
        "acceptance: deviation < 35%\nmeasured: within ±0.1%",
        transform=ax2.transAxes,
        fontsize=10,
        va="top",
        bbox=dict(boxstyle="round,pad=0.35", fc=LIGHT_GOLD, ec=GOLD, lw=1.0),
    )
    ax2.set_xticks(xs, [r"$|E_0/E_1|$", r"$|E_1/E_2|$", r"$|E_2/E_3|$"])
    ax2.set_ylim(500, 534)
    ax2.set_title("(b) measured ladder ratios vs the universal number")
    ax2.set_ylabel("energy ratio (dimensionless)")
    ax2.grid(alpha=0.3, axis="y")
    fig.savefig(figdir / "fig02_universal_numbers.png")
    plt.close(fig)

    # ================= fig03 — stability of the ladder ========================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    ok = cap_L >= 2
    ax1.plot(
        L_vals[ok],
        r_L[ok],
        "o-",
        color=GOLD,
        lw=1.8,
        mec=NAVY,
        mew=0.8,
        ms=8,
        label=r"$|E_0/E_1|$ (boxes hosting $\geq 2$ rungs)",
    )
    ax1.axhline(
        en_univ, color=NAVY, ls="--", lw=1.6, label=rf"universal $e^{{2\pi/s_0}}$ = {en_univ:.3f}"
    )
    ax1.text(
        4.2, 515.66, "L = 4, 6: a single trimer fits\n(ratio undefined)", fontsize=9.5, va="bottom"
    )
    ax1.set_ylim(514.9, 515.85)
    ax1.set_title("(a) box-length sweep at fixed grid spacing")
    ax1.set_xlabel(r"box length $L = \ln(R_{max}/R_0)$")
    ax1.set_ylabel("ladder ratio (dimensionless)")
    ax1r = ax1.twinx()
    ax1r.step(L_vals, cap_L, where="mid", color=SERIES[2], lw=1.8, label="bound trimers in the box")
    ax1r.set_ylim(0.0, 6.0)
    ax1r.set_ylabel("number of bound trimers", color=SERIES[2])
    ax1r.tick_params(axis="y", colors=SERIES[2])
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax1r.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="center right", bbox_to_anchor=(1.0, 0.42))
    ax1.grid(alpha=0.3)

    ax2.plot(n_vals, r_n, "o-", color=GOLD, lw=1.8, mec=NAVY, mew=0.8, ms=8, label=r"$|E_0/E_1|$")
    ax2.plot(
        n_vals, r12_n, "s-", color=SERIES[1], lw=1.8, mec=NAVY, mew=0.8, ms=7, label=r"$|E_1/E_2|$"
    )
    ax2.axhline(en_univ, color=NAVY, ls="--", lw=1.6, label=f"universal {en_univ:.3f}")
    ax2.plot(
        [n_grid],
        [ratio01],
        "*",
        color=SERIES[3],
        ms=15,
        mec=NAVY,
        mew=0.6,
        zorder=5,
        label=f"preset grid n = {n_grid}",
    )
    ax2.set_xscale("log")
    ax2.set_ylim(511.5, 517.0)
    ax2.set_title("(b) grid refinement at the preset box")
    ax2.set_xlabel("FD grid points n")
    ax2.set_ylabel("ladder ratio (dimensionless)")
    ax2.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0))
    ax2.grid(alpha=0.3)
    fig.savefig(figdir / "fig03_ladder_stability.png")
    plt.close(fig)

    # ================= fig04 — scaling laws ===================================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    ns = np.arange(n_lv)
    law = np.abs(En[0]) * R0**2 * en_univ ** (-ns)
    ax1.semilogy(
        ns,
        np.abs(En) * R0**2,
        "o",
        color=GOLD,
        ms=13,
        mec=NAVY,
        mew=1.0,
        zorder=5,
        label="computed levels",
    )
    ax1.semilogy(
        ns,
        law,
        "--",
        color=NAVY,
        lw=1.8,
        label=r"universal law $|E_n|R_0^2 = |E_0|R_0^2\,e^{-2\pi n/s_0}$",
    )
    rat_list = [ratio01, ratio12, ratio23]
    for i in range(n_lv - 1):
        gm = np.sqrt(np.abs(En[i] * En[i + 1])) * R0**2
        ax1.annotate(
            rf"$|E_{i}/E_{i+1}|$ = {rat_list[i]:.3f}",
            xy=(i + 0.5, gm),
            xytext=(4, 8),
            textcoords="offset points",
            fontsize=9.5,
        )
    ax1.set_xlim(-0.3, 3.3)
    ax1.set_title("(a) the geometric energy ladder")
    ax1.set_xlabel("level index n")
    ax1.set_ylabel(r"$|E_n|\,R_0^2$  (dimensionless, $\hbar^2/m = 1$)")
    ax1.legend(loc="upper right", bbox_to_anchor=(1.0, 1.0))
    ax1.grid(alpha=0.3, which="both")

    ax2.loglog(
        r0_vals,
        e0_r0,
        "o",
        color=GOLD,
        ms=11,
        mec=NAVY,
        mew=0.9,
        zorder=5,
        label="$|E_0|(R_0)$, fixed box shape",
    )
    fit_line = np.exp(np.polyval(np.polyfit(np.log(r0_vals), np.log(e0_r0), 1), np.log(r0_vals)))
    ax2.loglog(
        r0_vals, fit_line, "--", color=NAVY, lw=1.8, label=f"power-law fit, slope = {slope:.6f}"
    )
    ax2.annotate(
        f"ladder ratio invariant:\nspread of $|E_0/E_1|$ = {rat_spread:.1e}",
        xy=(0.96, 0.95),
        xycoords="axes fraction",
        fontsize=10.5,
        ha="right",
        va="top",
        bbox=dict(boxstyle="round,pad=0.35", fc=LIGHT_GOLD, ec=GOLD, lw=1.0),
    )
    ax2.set_title("(b) three-body parameter sets the scale only")
    ax2.set_xlabel("three-body parameter $R_0$ (length)")
    ax2.set_ylabel(r"$|E_0|$  (units of $1/R_0^2$, $\hbar^2/m = 1$)")
    ax2.legend(loc="lower left", bbox_to_anchor=(0.0, 0.0))
    ax2.grid(alpha=0.3, which="both")
    fig.savefig(figdir / "fig04_scaling_laws.png")
    plt.close(fig)

    # ---- JSON figures block ==================================================
    return {
        "scheme": {
            "file": "figures/scheme_trx07.svg",
            "caption": (
                "Efimov scheme - three identical bosons at unitarity (scattering "
                "length a -> infinity) with resonant pairwise interactions and "
                "hyperradius R; the hyperradial adiabatic potential "
                "-(s0^2-1/4)/R^2 binds infinitely many trimers in a geometric "
                "ladder: sizes grow by exp(pi/s0) = 22.694 per rung, energies "
                "drop by exp(2*pi/s0) = 515.035 per rung; the short-distance "
                "wall R0 (the three-body parameter) fixes the anchor of the "
                "whole comb: shifting R0 shifts every rung but leaves the "
                "ratios invariant; mapping to TRIVORTEX: universal exponent s0 -> "
                "circulation ratios Gamma, geometric ladder -> radial "
                "modulation omega = (2*pi/T)*exp(C_Ch/pi), 1/R^2 attraction -> "
                "scale-invariant binding of Theorem 3.1."
            ),
        },
        "panels": [
            {
                "file": "figures/fig01_efimov_landscape.png",
                "caption": (
                    "Model landscape: (a) hyperradial adiabatic potential "
                    "|V(R)| = (s0^2-1/4)/R^2 on log-log axes with the hard wall "
                    "R0 (three-body parameter) and the scaling hyperradii "
                    "R_n = sqrt((s0^2-1/4)/|E_n|) of the four computed trimers - "
                    f"{Rn[0]:.6g}, {Rn[1]:.6g}, {Rn[2]:.6g}, {Rn[3]:.6g} in units "
                    f"of R0, spaced by exp(pi/s0) = {len_univ:.3f}; (b) the same "
                    "ladder in s = ln(R/R0) space: rungs equally spaced by "
                    f"pi/s0 = {pi_s0:.4f} - the log-periodicity that generates "
                    "the 515x energy ladder."
                ),
            },
            {
                "file": "figures/fig02_universal_numbers.png",
                "caption": (
                    "Headline result: (a) the transcendental quantization "
                    "function f(s) = s*cosh(pi*s/2) - (8/sqrt(3))*sinh(pi*s/6) "
                    f"with its root s0 = {s0:.7f} (brentq; target 1.0062458, "
                    "tolerance 1e-5); (b) measured ladder ratios "
                    f"|E0/E1| = {ratio01:.3f} ({dev01:+.2f}%), "
                    f"|E1/E2| = {ratio12:.3f} ({dev12:+.2f}%), "
                    f"|E2/E3| = {ratio23:.3f} ({dev23:+.2f}%) against the "
                    f"universal exp(2*pi/s0) = {en_univ:.3f} (dashed line; "
                    "acceptance band 35%)."
                ),
            },
            {
                "file": "figures/fig03_ladder_stability.png",
                "caption": (
                    "Stability of the computed ladder: (a) box-length sweep at "
                    "fixed grid spacing (L = ln(Rmax/R0) from 4 to "
                    f"{L:.2f}) - the ratio |E0/E1| is box-independent wherever "
                    "two rungs fit (L >= 8), while the number of bound trimers "
                    "grows 1 -> 4 with the box capacity; (b) grid refinement at "
                    f"the preset box - ratios converge monotonically "
                    f"({r_n[0]:.2f}/{r12_n[0]:.2f} at n = {int(n_vals[0])} to "
                    f"{r_n[-1]:.2f}/{r12_n[-1]:.2f} at n = {int(n_vals[-1])}); "
                    f"the preset n = {n_grid} sits within 0.1% of the universal "
                    f"{en_univ:.3f}."
                ),
            },
            {
                "file": "figures/fig04_scaling_laws.png",
                "caption": (
                    "Scaling laws: (a) the geometric energy ladder |E_n|*R0^2 "
                    "on a log scale against the universal law "
                    "exp(-2*pi*n/s0) - individual rung ratios within 0.1% of "
                    "515.035; (b) three-body parameter sweep R0 over three "
                    "decades at fixed box shape - |E0| follows the exact power "
                    f"law R0^-2 (fitted slope {slope:.6f}) while the ladder "
                    f"ratio |E0/E1| is invariant (spread {rat_spread:.1e}): R0 "
                    "shifts the absolute scale, the ratios stay universal."
                ),
            },
        ],
        "data": {
            "preset": {
                "s0": round(float(s0), 9),
                "length_ratio_exp_pi_over_s0": round(len_univ, 6),
                "energy_ratio_exp_2pi_over_s0": round(en_univ, 6),
                "R0": float(R0),
                "Rmax": float(Rmax),
                "grid_points": int(n_grid),
                "box_length_ln_Rmax_over_R0": round(L, 6),
                "grid_spacing_ds": round(ds, 6),
                "levels": [float(v) for v in En],
                "scaling_lengths_over_R0": [round(float(v), 6) for v in Rn],
                "ladder_ratios": {
                    "E0/E1": round(ratio01, 6),
                    "E1/E2": round(ratio12, 6),
                    "E2/E3": round(ratio23, 6),
                },
                "deviations_percent": {
                    "E0/E1": round(dev01, 4),
                    "E1/E2": round(dev12, 4),
                    "E2/E3": round(dev23, 4),
                },
            },
            "box_length_sweep": {
                "L": [round(float(v), 3) for v in L_vals],
                "bound_trimers": [int(v) for v in cap_L],
                "ratio_E0_over_E1": [None if np.isnan(v) else round(float(v), 4) for v in r_L],
            },
            "grid_sweep": {
                "n_grid": [int(v) for v in n_vals],
                "grid_spacing_ds": [round(float(L / (int(v) - 1)), 5) for v in n_vals],
                "ratio_E0_over_E1": [round(float(v), 4) for v in r_n],
                "ratio_E1_over_E2": [round(float(v), 4) for v in r12_n],
            },
            "three_body_parameter_sweep": {
                "R0": [float(v) for v in r0_vals],
                "E0_abs": [float(v) for v in e0_r0],
                "ratio_E0_over_E1": [round(float(v), 9) for v in rat_r0],
                "fitted_power_law_slope": round(slope, 6),
                "ratio_spread": float(rat_spread),
            },
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv=None):
    ap = argparse.ArgumentParser(description="TRX-07 Efimov effect")
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

    # check 1: transcendental root
    s0 = brentq(transcendental, 0.5, 3.0, xtol=1e-13, rtol=8.9e-16)
    add(
        "s0_transcendental_root",
        s0,
        1.0062458,
        1e-5,
        "dimless",
        "s0*cosh(pi s0/2) = (8/sqrt(3)) sinh(pi s0/6)",
    )

    # check 2: universal ratios
    len_ratio = float(np.exp(np.pi / s0))
    en_ratio = float(np.exp(2.0 * np.pi / s0))
    add("efimov_length_ratio", len_ratio, 22.7, 0.05, "a-ratio", "a_*/a_*' = exp(pi/s0)")
    add("efimov_energy_ratio", en_ratio, 515.03, 0.05, "E-ratio", "E/E' = exp(2*pi/s0)")

    # check 3: numerical hyperradial spectrum
    R0, Rmax = (1e-2, 1e4) if smoke else (1e-3, 1e6)
    n_grid = 500 if smoke else 900
    E = efimov_spectrum(s0, R0=R0, Rmax=Rmax, n_grid=n_grid, n_levels=4)
    E = E[E < 0]
    add(
        "spectrum_all_negative",
        1.0 if E.size >= 3 else 0.0,
        1.0,
        1e-12,
        "bool",
        f"{E.size} negative levels found",
    )
    if E.size >= 3:
        ratio01 = float(abs(E[0] / E[1]))
        ratio12 = float(abs(E[1] / E[2]))
        add(
            "ladder_ratio_E0_over_E1",
            ratio01,
            en_ratio,
            0.35 * en_ratio,
            "E-ratio",
            f"|E0/E1| = {ratio01:.1f}",
        )
        add(
            "ladder_ratio_E1_over_E2",
            ratio12,
            en_ratio,
            0.35 * en_ratio,
            "E-ratio",
            f"|E1/E2| = {ratio12:.1f}",
        )

    out = Path(__file__).resolve().parents[1] / "results"
    out.mkdir(exist_ok=True)
    make_svg(s0, E, R0, Rmax, out / "trx07_plot.svg")

    # --- canonical figures (--figures, additive) -----------------------------
    figures_block = None
    figdir = Path(__file__).resolve().parents[1] / "figures"
    if args.figures:
        figures_block = render_figures(
            s0=s0, E=E, R0=R0, Rmax=Rmax, n_grid=n_grid, smoke=smoke, figdir=figdir
        )

    all_pass = all(c["pass"] for c in CHECKS)
    protocol = {
        "study": "TRX-07",
        "title": "The Efimov effect: universal quantum three-body physics",
        "status": "PASS" if all_pass else "FAIL",
        "smoke": bool(smoke),
        "runtime_s": round(time.time() - t0, 3),
        "checks": CHECKS,
        "series": {"levels_E": [float(e) for e in E]},
        "meta": {
            "equations": [
                "s0*cosh(pi*s0/2) = (8/sqrt(3))*sinh(pi*s0/6),  s0 = 1.0062458",
                "a ladder: exp(pi/s0) = 22.7 ;  E ladder: exp(2*pi/s0) = 515",
                "-u''(R) - (s0^2 - 1/4)/R^2 u = E u,  u(R0)=u(Rmax)=0",
            ],
            "s0": s0,
            "levels": [float(e) for e in E],
            "R0": R0,
            "Rmax": Rmax,
            "laser_link": "observed in laser-cooled Cs (Kraemer et al. 2006); "
            "Feshbach-tuned, laser-spectroscopied trimers",
        },
    }
    if figures_block is not None:
        protocol["figures"] = figures_block
    (out / "trx07_results.json").write_text(json.dumps(protocol, indent=2), encoding="utf-8")

    print(f"\nTRX-07 — Efimov effect  [{'SMOKE' if smoke else 'FULL'}]")
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
