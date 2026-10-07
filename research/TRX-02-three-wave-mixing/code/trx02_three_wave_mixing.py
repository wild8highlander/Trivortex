#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
TRIVORTEX LAB — TRX-02 — RESONANT THREE-WAVE INTERACTION (MANLEY–ROWE)
============================================================================
Resonant three-wave mixing in a chi(2) nonlinear crystal — the canonical
"three-body problem of nonlinear optics".  A pump wave at omega3 = omega1 +
omega2 exchanges photons with a signal/idler pair.  In the lossless,
phase-matched (Delta k = 0) limit the normalized amplitude equations are

    da1/dt = i a2* a3 ,   da2/dt = i a1* a3 ,   da3/dt = i a1 a2 .

They possess the Manley–Rowe invariants |a1|^2+|a3|^2, |a2|^2+|a3|^2,
|a1|^2-|a2|^2 and are canonically equivalent to the Euler top — the same
integrable family as the Kirchhoff three-vortex problem that underlies
the TRIVORTEX Theorem 3.1.

What is computed
  * Manley–Rowe invariant drift over t in [0, 50]
  * periodic pump depletion & revival (exchange period T_ex)
  * degenerate channel (SHG): numeric vs analytic eta(t) = tanh^2(A t)
  * with --figures: hand-authored scheme SVG + four canonical PNG panels
    (300 dpi) into figures/, and a "figures" block added to the JSON protocol

Usage:  python trx02_three_wave_mixing.py [--smoke] [--figures]
Author: Isaev Iskhak Khamzatovich (repository owner)
License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

CHECKS = []

NAVY = "#0A1730"
GOLD = "#D4AF37"
SERIES = ["#D4AF37", "#4C72B0", "#55A868", "#C44E52", "#8172B2"]


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
# Dynamics (6 real ODEs for 3 complex amplitudes)
# ---------------------------------------------------------------------------


def rhs(t, y):
    a1 = y[0] + 1j * y[1]
    a2 = y[2] + 1j * y[3]
    a3 = y[4] + 1j * y[5]
    da1 = 1j * np.conj(a2) * a3
    da2 = 1j * np.conj(a1) * a3
    da3 = 1j * a1 * a2
    return [da1.real, da1.imag, da2.real, da2.imag, da3.real, da3.imag]


def amps(y):
    return y[0] + 1j * y[1], y[2] + 1j * y[3], y[4] + 1j * y[5]


def invariants(y):
    a1, a2, a3 = amps(y)
    n1, n2, n3 = abs(a1) ** 2, abs(a2) ** 2, abs(a3) ** 2
    return n1 + n3, n2 + n3, n1 - n2


# ---------------------------------------------------------------------------
# SVG output
# ---------------------------------------------------------------------------


def _poly(pts, color, sw=1.8):
    s = " ".join(f"{px:.2f},{py:.2f}" for px, py in pts)
    return f'<polyline fill="none" stroke="{color}" stroke-width="{sw}" points="{s}"/>'


def make_svg(ts, n1, n2, n3, path):
    W, H = 900, 520
    x0, x1, y0, y1 = 70.0, 860.0, 60.0, 440.0
    tmax, nmax = float(ts[-1]), 1.15 * max(n1.max(), n2.max(), n3.max())

    def X(t):
        return x0 + (t / tmax) * (x1 - x0)

    def Y(v):
        return y1 - (v / nmax) * (y1 - y0)

    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect width="{W}" height="{H}" fill="#0A1230"/>',
        '<text x="24" y="34" fill="#FFFFFF" font-family="Arial" font-size="19" '
        'font-weight="bold">TRX-02 &#8212; Resonant three-wave mixing: Manley&#8211;Rowe energy exchange</text>',
        f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="#3A4A6B" stroke-width="1"/>',
        f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="#3A4A6B" stroke-width="1"/>',
        _poly([(X(t), Y(v)) for t, v in zip(ts, n3)], "#F2C14E"),
        _poly([(X(t), Y(v)) for t, v in zip(ts, n1)], "#6FB7FF"),
        _poly([(X(t), Y(v)) for t, v in zip(ts, n2)], "#9FB3D9", 1.4),
        '<text x="90" y="80" fill="#F2C14E" font-family="Arial" font-size="14">|a3|^2 (pump)</text>',
        '<text x="90" y="100" fill="#6FB7FF" font-family="Arial" font-size="14">|a1|^2 (signal)</text>',
        '<text x="90" y="120" fill="#9FB3D9" font-family="Arial" font-size="14">|a2|^2 (idler)</text>',
        '<text x="620" y="470" fill="#9FB3D9" font-family="Arial" font-size="13">time (dimensionless)</text>',
        '<text x="24" y="500" fill="#9FB3D9" font-family="Arial" font-size="13">'
        "Pump periodicity and photon-pair bookkeeping: the optical analogue of three-body choreography.</text>",
        "</svg>",
    ]
    Path(path).write_text("\n".join(s), encoding="utf-8")


# ---------------------------------------------------------------------------
# Canonical figures (--figures mode): scheme SVG + four PNG panels
# ---------------------------------------------------------------------------


def make_scheme_svg(path):
    """Hand-authored schematic of resonant three-wave mixing (white bg, navy/gold)."""
    F = "Helvetica, Arial, sans-serif"

    def wave(x0, x1, y0, amp, periods, color, sw=1.9, phase=0.0):
        n = 140
        pts = []
        for i in range(n + 1):
            x = x0 + (x1 - x0) * i / n
            y = y0 + amp * math.sin(2.0 * math.pi * periods * i / n + phase)
            pts.append((x, y))
        return _poly(pts, color, sw)

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
        '    <marker id="arrB" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto-start-reverse">',
        '      <path d="M0,0 L10,5 L0,10 z" fill="#4C72B0"/>',
        "    </marker>",
        '    <marker id="arrV" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto-start-reverse">',
        '      <path d="M0,0 L10,5 L0,10 z" fill="#55A868"/>',
        "    </marker>",
        "  </defs>",
        '  <rect width="960" height="540" fill="#FFFFFF"/>',
        # title + subtitle
        f'  <text x="30" y="40" font-family="{F}" font-size="21" font-weight="bold" '
        'fill="#0A1730">TRX-02 &#8212; Scheme: resonant three-wave mixing in a '
        "&#967;&#8317;&#178;&#8318; crystal</text>",
        f'  <text x="30" y="63" font-family="{F}" font-size="13" fill="#3A4A66">A pump '
        "photon at &#969;&#8323; = &#969;&#8321; + &#969;&#8322; exchanges photons with a "
        "signal&#8211;idler pair; the Manley&#8211;Rowe relations keep the photon "
        "bookkeeping exact</text>",
        # crystal
        '  <rect x="392" y="150" width="180" height="130" rx="6" fill="#F7F5EE" '
        'stroke="#0A1730" stroke-width="2"/>',
        f'  <text x="482" y="174" font-family="{F}" font-size="13.5" font-weight="bold" '
        'fill="#0A1730" text-anchor="middle">&#967;&#8317;&#178;&#8318; crystal</text>',
        f'  <text x="482" y="192" font-family="{F}" font-size="11" fill="#3A4A66" '
        'text-anchor="middle">lossless &#183; phase-matched &#916;k = 0</text>',
        # photon splitting glyph inside the crystal
        '  <circle cx="482" cy="212" r="7" fill="#D4AF37" stroke="#0A1730" stroke-width="1.6"/>',
        '  <line x1="476" y1="217" x2="460" y2="236" stroke="#0A1730" stroke-width="1.6" '
        'marker-end="url(#arrN)"/>',
        '  <line x1="488" y1="217" x2="504" y2="236" stroke="#0A1730" stroke-width="1.6" '
        'marker-end="url(#arrN)"/>',
        '  <circle cx="457" cy="243" r="5.5" fill="#4C72B0" stroke="#0A1730" stroke-width="1.4"/>',
        '  <circle cx="507" cy="243" r="5.5" fill="#55A868" stroke="#0A1730" stroke-width="1.4"/>',
        f'  <text x="482" y="272" font-family="{F}" font-size="12" font-weight="bold" '
        'fill="#0A1730" text-anchor="middle">&#969;&#8323; &#8594; &#969;&#8321; + '
        "&#969;&#8322;</text>",
        # pump wave (gold) into the crystal
        wave(60, 372, 215, 13, 4.0, "#D4AF37", 2.0),
        '  <line x1="372" y1="215" x2="390" y2="215" stroke="#D4AF37" stroke-width="2.4" '
        'marker-end="url(#arrG)"/>',
        f'  <text x="62" y="182" font-family="{F}" font-size="12.5" font-weight="bold" '
        'fill="#0A1730">pump wave &#183; &#969;&#8323;, k&#8323; &#183; amplitude a&#8323;</text>',
        f'  <text x="62" y="240" font-family="{F}" font-size="11" fill="#3A4A66">photon flux '
        "|a&#8323;|&#178; &#8212; depletes and revives periodically</text>",
        # signal wave (blue) out of the crystal
        wave(574, 876, 185, 11, 3.5, "#4C72B0", 1.9),
        '  <line x1="876" y1="185" x2="894" y2="185" stroke="#4C72B0" stroke-width="2.4" '
        'marker-end="url(#arrB)"/>',
        f'  <text x="600" y="152" font-family="{F}" font-size="12.5" font-weight="bold" '
        'fill="#0A1730">signal wave &#183; &#969;&#8321;, k&#8321; &#183; amplitude '
        "a&#8321;</text>",
        # idler wave (green) out of the crystal
        wave(574, 876, 285, 11, 3.5, "#55A868", 1.9),
        '  <line x1="876" y1="285" x2="894" y2="285" stroke="#55A868" stroke-width="2.4" '
        'marker-end="url(#arrV)"/>',
        f'  <text x="600" y="320" font-family="{F}" font-size="12.5" font-weight="bold" '
        'fill="#0A1730">idler wave &#183; &#969;&#8322;, k&#8322; &#183; amplitude '
        "a&#8322;</text>",
        # exchange note (top right)
        f'  <text x="574" y="108" font-family="{F}" font-size="12" fill="#0A1730">pump '
        "depletes into signal + idler, then revives &#8212;</text>",
        f'  <text x="574" y="124" font-family="{F}" font-size="12" fill="#0A1730">periodic '
        "exchange with period T_ex (choreographic cycle)</text>",
        # box 1: energy matching
        '  <rect x="48" y="356" width="258" height="126" rx="6" fill="#FFFFFF" '
        'stroke="#0A1730" stroke-width="1.4"/>',
        f'  <text x="62" y="380" font-family="{F}" font-size="13.5" font-weight="bold" '
        'fill="#0A1730">Energy matching</text>',
        f'  <text x="177" y="416" font-family="{F}" font-size="16" font-weight="bold" '
        'fill="#D4AF37" text-anchor="middle">&#969;&#8323; = &#969;&#8321; + '
        "&#969;&#8322;</text>",
        f'  <text x="177" y="440" font-family="{F}" font-size="11.5" fill="#0A1730" '
        'text-anchor="middle">one pump photon &#8652; one signal + one idler</text>',
        f'  <text x="177" y="460" font-family="{F}" font-size="11.5" fill="#3A4A66" '
        'text-anchor="middle">down-conversion (OPO/OPA) and its</text>',
        f'  <text x="177" y="475" font-family="{F}" font-size="11.5" fill="#3A4A66" '
        'text-anchor="middle">reverse, sum-frequency generation</text>',
        # box 2: momentum matching
        '  <rect x="326" y="356" width="280" height="126" rx="6" fill="#FFFFFF" '
        'stroke="#0A1730" stroke-width="1.4"/>',
        f'  <text x="340" y="380" font-family="{F}" font-size="13.5" font-weight="bold" '
        'fill="#0A1730">Momentum matching</text>',
        '  <line x1="352" y1="416" x2="430" y2="416" stroke="#4C72B0" stroke-width="2.2" '
        'marker-end="url(#arrB)"/>',
        '  <line x1="432" y1="416" x2="510" y2="416" stroke="#55A868" stroke-width="2.2" '
        'marker-end="url(#arrV)"/>',
        f'  <text x="391" y="404" font-family="{F}" font-size="11.5" fill="#4C72B0" '
        'text-anchor="middle">k&#8321;</text>',
        f'  <text x="471" y="404" font-family="{F}" font-size="11.5" fill="#55A868" '
        'text-anchor="middle">k&#8322;</text>',
        '  <line x1="352" y1="444" x2="510" y2="444" stroke="#D4AF37" stroke-width="2.2" '
        'marker-end="url(#arrG)"/>',
        f'  <text x="431" y="462" font-family="{F}" font-size="11.5" fill="#0A1730" '
        'text-anchor="middle">k&#8323; = k&#8321; + k&#8322;  (co-propagating geometry, '
        "&#916;k = 0)</text>",
        # box 3: Manley–Rowe bookkeeping
        '  <rect x="626" y="356" width="286" height="126" rx="6" fill="#FFFFFF" '
        'stroke="#0A1730" stroke-width="1.4"/>',
        f'  <text x="640" y="380" font-family="{F}" font-size="13.5" font-weight="bold" '
        'fill="#0A1730">Manley&#8211;Rowe bookkeeping</text>',
        f'  <text x="640" y="406" font-family="{F}" font-size="12.5" fill="#0A1730">I&#8321; '
        "= |a&#8321;|&#178; + |a&#8323;|&#178; = const</text>",
        f'  <text x="640" y="426" font-family="{F}" font-size="12.5" fill="#0A1730">I&#8322; '
        "= |a&#8322;|&#178; + |a&#8323;|&#178; = const</text>",
        f'  <text x="640" y="446" font-family="{F}" font-size="12.5" fill="#0A1730">I&#8323; '
        "= |a&#8321;|&#178; &#8722; |a&#8322;|&#178; = const</text>",
        f'  <text x="640" y="468" font-family="{F}" font-size="10.5" fill="#3A4A66">photon-pair '
        "bookkeeping &#8212; the optical twin of</text>",
        f'  <text x="640" y="479" font-family="{F}" font-size="10.5" fill="#3A4A66">vortex '
        "circulation bookkeeping (TRIVORTEX)</text>",
        # footer
        f'  <text x="30" y="524" font-family="{F}" font-size="10.5" fill="#6B7A94">TRIVORTEX '
        "Research Program &#183; study TRX-02 &#183; resonant three-wave interaction &#8212; "
        "Euler-top / Kirchhoff-vortex integrable family</text>",
        "</svg>",
    ]
    Path(path).write_text("\n".join(s), encoding="utf-8")


def render_figures(
    sol, ts, Y, inv, inv0, maxima, Tex1, revival, tg, eta_num, eta_ref, A, smoke, figdir
):
    """Render the scheme SVG and four canonical PNG panels into figures/.

    Reuses the dynamics already integrated in main(); adds a parameter sweep
    of the initial pump amplitude for the stability panel. Returns the
    "figures" block for the JSON protocol.
    """
    from scipy.optimize import minimize_scalar

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
    suptitle = "TRX-02 · Resonant three-wave mixing"

    n1 = np.abs(Y[0] + 1j * Y[1]) ** 2
    n2 = np.abs(Y[2] + 1j * Y[3]) ** 2
    n3 = np.abs(Y[4] + 1j * Y[5]) ** 2
    n10, n20, n30 = float(n1[0]), float(n2[0]), float(n3[0])

    # ---- parameter sweep: initial pump amplitude (fig03) ---------------------
    a10, a20 = 0.2, 0.3
    A3_grid = np.linspace(0.4, 2.0, 7 if smoke else 17)
    T_sweep = 25.0 if smoke else 50.0
    rt_sweep = 1e-8 if smoke else 1e-10
    ms_sweep = 0.2 if smoke else 0.1
    tex_s, dep_s, drift_s = [], [], []
    for A3 in A3_grid:
        y0s = [a10, 0.0, a20, 0.0, 0.0, float(A3)]
        s = solve_ivp(
            rhs,
            (0.0, T_sweep),
            y0s,
            method="DOP853",
            rtol=rt_sweep,
            atol=rt_sweep,
            dense_output=True,
            max_step=ms_sweep,
        )
        td = np.linspace(0.02, T_sweep, 8001)
        Yd = s.sol(td)
        nd = np.abs(Yd[4] + 1j * Yd[5]) ** 2
        mx = []
        for i in range(1, td.size - 1):
            if nd[i] > nd[i - 1] and nd[i] >= nd[i + 1] and td[i] > 0.2:
                mx.append(float(td[i]))
            if len(mx) == 2:
                break

        def neg_n3(t, s=s):
            z = s.sol(np.array([t]))[:, 0]
            return -float(abs(z[4] + 1j * z[5]) ** 2)

        if len(mx) == 2:
            r0 = minimize_scalar(neg_n3, bounds=(mx[0] - 0.02, mx[0] + 0.02), method="bounded")
            r1 = minimize_scalar(neg_n3, bounds=(mx[1] - 0.02, mx[1] + 0.02), method="bounded")
            tex_s.append(abs(float(r1.x) - float(r0.x)))
        else:
            tex_s.append(float("nan"))
        dep_s.append(float(nd.min() / nd.max()))
        tdr = td[::80]
        Yr = s.sol(tdr)
        invs = np.array(
            [
                (np.abs(Yr[0] + 1j * Yr[1]) ** 2 + np.abs(Yr[4] + 1j * Yr[5]) ** 2),
                (np.abs(Yr[2] + 1j * Yr[3]) ** 2 + np.abs(Yr[4] + 1j * Yr[5]) ** 2),
                (np.abs(Yr[0] + 1j * Yr[1]) ** 2 - np.abs(Yr[2] + 1j * Yr[3]) ** 2),
            ]
        )
        drift_s.append(float(np.max(np.abs(invs - invs[:, :1]))))
    tex_s = np.array(tex_s)
    dep_s = np.array(dep_s)
    drift_s = np.array(drift_s)

    # ================= fig01 — resonance geometry =============================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    # (a) photon-energy diagram of the resonant triad
    w1, w2, w3 = 0.35, 0.55, 0.90
    ax1.axhline(0.0, color=NAVY, lw=0.9, alpha=0.5)
    ax1.annotate(
        "",
        xy=(1.22, 0.0),
        xytext=(0.03, 0.0),
        arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.4),
    )
    for w, lab, col, dy in (
        (w1, r"$\omega_1$ (signal)", blue, -0.015),
        (w2, r"$\omega_2$ (idler)", green, -0.095),
        (w3, r"$\omega_3$ (pump)", GOLD, -0.015),
    ):
        ax1.plot([w, w], [0.0, 0.07], color=col, lw=1.8)
        ax1.plot([w, w], [0.0, dy + 0.005], color=col, lw=0.8, ls=":", alpha=0.7)
        ax1.annotate(
            lab, xy=(w, dy), ha="center", va="top", fontsize=10.5, color=NAVY, annotation_clip=False
        )
    # down-conversion: pump photon splits into signal + idler
    ax1.plot([w3, w3], [0.82, 0.44], color=GOLD, lw=2.4)
    ax1.plot([w3, w1 + 0.035], [0.44, 0.44], color=GOLD, lw=2.4)
    ax1.plot([w3, w2 - 0.035], [0.44, 0.44], color=GOLD, lw=2.4)
    ax1.annotate(
        "", xy=(w1, 0.11), xytext=(w1, 0.44), arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=2.4)
    )
    ax1.annotate(
        "", xy=(w2, 0.11), xytext=(w2, 0.44), arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=2.4)
    )
    ax1.annotate(
        "", xy=(w3, 0.44), xytext=(w3, 0.82), arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=2.4)
    )
    # up-conversion (reverse process, dashed navy)
    ax1.annotate(
        "",
        xy=(w3 - 0.035, 0.78),
        xytext=(0.5 * (w1 + w2) + 0.02, 0.34),
        arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.5, ls="--"),
    )
    ax1.annotate(
        "down-conversion (OPO/OPA)\n" r"$\omega_3 \to \omega_1 + \omega_2$",
        xy=(0.30, 0.58),
        ha="right",
        fontsize=10.5,
        color=NAVY,
    )
    ax1.annotate(
        "up-conversion (SFG)\n" r"$\omega_1 + \omega_2 \to \omega_3$",
        xy=(0.66, 0.30),
        ha="left",
        fontsize=10.5,
        color=NAVY,
    )
    ax1.annotate(
        r"energy matching: $\omega_3 = \omega_1 + \omega_2$",
        xy=(0.62, 0.97),
        ha="center",
        fontsize=11.5,
        color=NAVY,
        fontweight="bold",
    )
    ax1.annotate(
        r"momentum matching: $k_3 = k_1 + k_2\ (\Delta k = 0)$",
        xy=(0.62, 0.885),
        ha="center",
        fontsize=10.5,
        color="#3A4A66",
    )
    ax1.set_xlim(-0.06, 1.30)
    ax1.set_ylim(-0.16, 1.02)
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_xlabel("frequency $\\omega$ [normalized units]")
    ax1.set_title("(a) Resonance geometry of the wave triad")

    # (b) initial photon-flux bookkeeping
    ax2.barh(
        [1.0], [n20], height=0.52, color=green, edgecolor=NAVY, lw=1.2, label=r"$|a_2|^2$ (idler)"
    )
    ax2.barh(
        [1.0],
        [n30],
        height=0.52,
        left=[n20],
        color=GOLD,
        edgecolor=NAVY,
        lw=1.2,
        label=r"$|a_3|^2$ (pump)",
    )
    ax2.barh(
        [0.0], [n10], height=0.52, color=blue, edgecolor=NAVY, lw=1.2, label=r"$|a_1|^2$ (signal)"
    )
    ax2.barh([0.0], [n30], height=0.52, left=[n10], color=GOLD, edgecolor=NAVY, lw=1.2)
    ax2.annotate(
        rf"$|a_3|^2 = {n30:.2f}$",
        xy=(n20 + n30 / 2, 1.0),
        ha="center",
        va="center",
        fontsize=10.5,
        color=NAVY,
    )
    ax2.annotate(
        rf"$|a_3|^2 = {n30:.2f}$",
        xy=(n10 + n30 / 2, 0.0),
        ha="center",
        va="center",
        fontsize=10.5,
        color=NAVY,
    )
    ax2.annotate(
        rf"$|a_1|^2 = {n10:.2f}$",
        xy=(n10 / 2, 0.0),
        ha="center",
        va="center",
        fontsize=9,
        color=NAVY,
    )
    ax2.annotate(
        rf"$|a_2|^2 = {n20:.2f}$",
        xy=(n20 / 2, 1.0),
        ha="center",
        va="center",
        fontsize=9,
        color=NAVY,
    )
    ax2.annotate(
        rf"$I_1 = {inv0[0]:.2f}$", xy=(inv0[0] + 0.015, 0.0), va="center", fontsize=11, color=NAVY
    )
    ax2.annotate(
        rf"$I_2 = {inv0[1]:.2f}$", xy=(inv0[1] + 0.015, 1.0), va="center", fontsize=11, color=NAVY
    )
    ax2.set_yticks([0.0, 1.0], [r"$I_1$", r"$I_2$"], fontsize=13)
    ax2.annotate(
        r"$I_1 = |a_1|^2+|a_3|^2$",
        xy=(0.03, 0.965),
        xycoords="axes fraction",
        va="top",
        fontsize=10.5,
        color=NAVY,
    )
    ax2.annotate(
        r"$I_2 = |a_2|^2+|a_3|^2$",
        xy=(0.03, 0.895),
        xycoords="axes fraction",
        va="top",
        fontsize=10.5,
        color=NAVY,
    )
    ax2.set_xlim(0.0, 1.32)
    ax2.set_ylim(-0.62, 1.78)
    ax2.set_xlabel("photon flux $|a_k|^2$ [dimensionless]")
    ax2.set_title("(b) Initial flux bookkeeping (Manley–Rowe pairs)")
    ax2.grid(True, axis="x", alpha=0.3)
    ax2.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=3)
    fig.savefig(figdir / "fig01_resonance_geometry.png")
    plt.close(fig)

    # ================= fig02 — pump depletion & revival (headline) ============
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    ax1.plot(ts, n3, color=GOLD, lw=2.2, label=r"$|a_3|^2$ (pump)")
    ax1.plot(ts, n1, color=blue, lw=1.5, label=r"$|a_1|^2$ (signal)")
    ax1.plot(ts, n2, color=green, lw=1.5, label=r"$|a_2|^2$ (idler)")
    ax1.set_xlabel("time t [dimensionless]")
    ax1.set_ylabel("photon flux $|a_k|^2$ [dimensionless]")
    ax1.set_title(f"(a) Pump depletion and revival over $T = {float(ts[-1]):.0f}$")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=3)

    tz = float(min(2.5 * Tex1, 0.6 * float(ts[-1])))
    td = np.linspace(0.0, tz, 900)
    Yd = sol.sol(td)
    n1d = np.abs(Yd[0] + 1j * Yd[1]) ** 2
    n2d = np.abs(Yd[2] + 1j * Yd[3]) ** 2
    n3d = np.abs(Yd[4] + 1j * Yd[5]) ** 2
    ax2.plot(td, n3d, color=GOLD, lw=2.2, label=r"$|a_3|^2$ (pump)")
    ax2.plot(td, n1d, color=blue, lw=1.5, label=r"$|a_1|^2$ (signal)")
    ax2.plot(td, n2d, color=green, lw=1.5, label=r"$|a_2|^2$ (idler)")
    m0, m1 = maxima[0], maxima[1]

    def _n3_at(t):
        z = sol.sol(np.array([t]))[:, 0]
        return float(np.abs(z[4] + 1j * z[5]) ** 2)

    n3_at = [_n3_at(m0), _n3_at(m1)]
    ax2.plot([m0, m1], n3_at, "o", ms=8, mfc=GOLD, mec=NAVY, mew=1.2, zorder=6, ls="none")
    ax2.annotate(
        "",
        xy=(m1, n3_at[1] * 0.93),
        xytext=(m0, n3_at[0] * 0.93),
        arrowprops=dict(arrowstyle="<|-|>", color=NAVY, lw=1.5),
    )
    mid = 0.5 * (m0 + m1)
    ax2.annotate(
        rf"$T_{{\rm ex,1}} = {Tex1:.9f}$",
        xy=(mid, 0.5 * min(n3_at)),
        ha="center",
        va="center",
        fontsize=11,
        color=NAVY,
    )
    imin = int(np.argmin(n3d))
    ax2.plot([td[imin]], [n3d[imin]], "o", ms=7, mfc=red, mec=NAVY, mew=1.1, zorder=6, ls="none")
    ax2.annotate(
        rf"$\min|a_3|^2 = {n3d[imin]:.3e}$",
        xy=(td[imin], n3d[imin]),
        textcoords="offset points",
        xytext=(10, -4),
        fontsize=10.5,
        color=NAVY,
    )
    ax2.annotate(
        rf"revival error $= {revival:.1e}$",
        xy=(m1, n3_at[1]),
        textcoords="offset points",
        xytext=(8, 6),
        fontsize=10.5,
        color=NAVY,
    )
    ax2.set_xlabel("time t [dimensionless]")
    ax2.set_ylabel("photon flux $|a_k|^2$ [dimensionless]")
    ax2.set_title("(b) One exchange cycle (zoom)")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=3)
    fig.savefig(figdir / "fig02_pump_depletion.png")
    plt.close(fig)

    # ================= fig03 — parameter sweep ================================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    ax1.plot(
        A3_grid,
        tex_s,
        color=blue,
        lw=2.0,
        marker="o",
        ms=6,
        mec=NAVY,
        mew=1.1,
        label=r"$T_{\rm ex}(a_3(0))$",
    )
    ax1.axvline(1.0, color=NAVY, lw=1.2, ls="--", alpha=0.7, label="study preset $a_3(0)=1.0i$")
    i0 = int(np.argmin(np.abs(A3_grid - 1.0)))
    ax1.annotate(
        rf"$T_{{\rm ex}} = {tex_s[i0]:.6f}$ at the preset",
        xy=(A3_grid[i0], tex_s[i0]),
        textcoords="offset points",
        xytext=(10, 10),
        fontsize=10.5,
        color=NAVY,
    )
    ax1.set_xlabel(r"initial pump amplitude $|a_3(0)|$ [dimensionless]")
    ax1.set_ylabel("exchange period $T_{\\rm ex}$ [dimensionless]")
    ax1.set_title("(a) Exchange period vs initial pump amplitude")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="upper right")

    ax2.semilogy(
        A3_grid,
        dep_s,
        color=red,
        lw=2.0,
        marker="s",
        ms=6,
        mec=NAVY,
        mew=1.1,
        label=r"$\min|a_3|^2\,/\,\max|a_3|^2$",
    )
    ax2.axhline(0.05, color=NAVY, lw=1.2, ls="--", label="full-depletion threshold (5%)")
    ax2.axvline(1.0, color=NAVY, lw=1.2, ls="--", alpha=0.7)
    ax2.set_xlabel(r"initial pump amplitude $|a_3(0)|$ [dimensionless]")
    ax2.set_ylabel("pump depletion depth [dimensionless]")
    ax2.set_title("(b) Depletion depth vs initial pump amplitude")
    ax2.grid(True, alpha=0.3, which="both")
    ax2.legend(loc="upper right")
    fig.savefig(figdir / "fig03_parameter_sweep.png")
    plt.close(fig)

    # ================= fig04 — invariants & SHG ===============================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    dI = inv - inv[0:1]
    ax1.plot(ts, dI[:, 0], color=blue, lw=1.1, label=r"$\Delta I_1$")
    ax1.plot(ts, dI[:, 1], color=green, lw=1.1, label=r"$\Delta I_2$")
    ax1.plot(ts, dI[:, 2], color=red, lw=1.1, label=r"$\Delta I_3$")
    m = max(float(np.max(np.abs(dI))), 1e-16)
    ax1.set_ylim(-1.45 * m, 1.45 * m)
    ax1.annotate(
        rf"$\max|\Delta I_1| = {np.max(np.abs(dI[:, 0])):.1e}$",
        xy=(0.97, 0.90),
        xycoords="axes fraction",
        ha="right",
        fontsize=10.5,
        color=NAVY,
    )
    ax1.annotate(
        rf"$\max|\Delta I_2| = {np.max(np.abs(dI[:, 1])):.1e}$",
        xy=(0.97, 0.80),
        xycoords="axes fraction",
        ha="right",
        fontsize=10.5,
        color=NAVY,
    )
    ax1.annotate(
        rf"$\max|\Delta I_3| = {np.max(np.abs(dI[:, 2])):.1e}$",
        xy=(0.97, 0.70),
        xycoords="axes fraction",
        ha="right",
        fontsize=10.5,
        color=NAVY,
    )
    ax1.annotate(
        f"tolerance 1e-10 (off scale)",
        xy=(0.97, 0.60),
        xycoords="axes fraction",
        ha="right",
        fontsize=10,
        color="#3A4A66",
    )
    ax1.set_xlabel("time t [dimensionless]")
    ax1.set_ylabel("Manley–Rowe residuals [dimensionless]")
    ax1.set_title("(a) Invariant residuals along the orbit")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=3)

    eta_err = float(np.max(np.abs(eta_num - eta_ref)))
    ax2.plot(tg, eta_ref, color=NAVY, lw=2.2, label=r"$\tanh^2(At)$ (analytic)")
    ax2.plot(
        tg,
        eta_num,
        "o",
        ms=5.5,
        mfc=GOLD,
        mec=NAVY,
        mew=0.9,
        ls="none",
        label=r"$\eta(t)$ (DOP853, rtol $= 10^{-13}$)",
    )
    ax2.annotate(
        rf"$\max|\Delta\eta| = {eta_err:.1e}$",
        xy=(0.04, 0.90),
        xycoords="axes fraction",
        fontsize=11,
        color=NAVY,
    )
    ax2.set_xlabel(r"time $t\ [1/(\gamma A)]$")
    ax2.set_ylabel("conversion efficiency $\\eta$ [dimensionless]")
    ax2.set_title("(b) Degenerate channel: SHG vs closed form")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="lower right")
    fig.savefig(figdir / "fig04_invariants_shg.png")
    plt.close(fig)

    # ================= scheme SVG =============================================
    make_scheme_svg(figdir / "scheme_trx02.svg")

    # ================= JSON figures block =====================================
    return {
        "mode": "smoke" if smoke else "full",
        "scheme": {
            "file": "figures/scheme_trx02.svg",
            "caption": (
                "Hand-authored schematic of resonant three-wave mixing: a pump wave "
                "(omega3, k3) enters a lossless phase-matched chi(2) crystal and "
                "exchanges photons with the signal (omega1, k1) and idler (omega2, "
                "k2) waves; energy matching omega3 = omega1 + omega2 and momentum "
                "matching k3 = k1 + k2 (Delta k = 0) close the resonance, and the "
                "Manley-Rowe relations give exact photon bookkeeping."
            ),
        },
        "panels": [
            {
                "file": "figures/fig01_resonance_geometry.png",
                "caption": (
                    "Overview of the model: (a) resonance geometry of the triad - "
                    "photon-energy diagram of the down-conversion omega3 -> omega1 + "
                    "omega2 with the reverse sum-frequency channel; (b) initial "
                    "photon-flux bookkeeping as stacked Manley-Rowe bars "
                    f"(|a1|^2 = {n10:.2f}, |a2|^2 = {n20:.2f}, |a3|^2 = {n30:.2f}; "
                    f"I1 = {inv0[0]:.2f}, I2 = {inv0[1]:.2f})."
                ),
            },
            {
                "file": "figures/fig02_pump_depletion.png",
                "caption": (
                    "Headline result - periodic pump depletion and revival: (a) photon "
                    f"fluxes over T = {float(ts[-1]):.0f} (DOP853, rtol = atol = 1e-13); "
                    "(b) one exchange cycle with the refined maxima marking "
                    f"T_ex,1 = {Tex1:.9f}, full depletion to min |a3|^2 = "
                    f"{n3d[imin]:.3e} and revival error {revival:.1e}."
                ),
            },
            {
                "file": "figures/fig03_parameter_sweep.png",
                "caption": (
                    "Parameter sweep over the initial pump amplitude |a3(0)| in "
                    f"[{A3_grid[0]:.1f}, {A3_grid[-1]:.1f}] ({A3_grid.size} points, "
                    f"T = {T_sweep:.0f}, rtol = {rt_sweep:.0e}): (a) exchange period "
                    "T_ex; (b) depletion depth min/max of |a3|^2 against the 5% "
                    "full-depletion threshold; the vertical line marks the study "
                    "preset a3(0) = 1.0i."
                ),
            },
            {
                "file": "figures/fig04_invariants_shg.png",
                "caption": (
                    "Dynamics diagnostics: (a) Manley-Rowe residuals along the orbit, "
                    f"max |dI| = {m:.1e} against the 1e-10 tolerance; (b) degenerate "
                    "channel - numerical conversion eta(t) of second-harmonic "
                    f"generation versus the closed form tanh^2(At), max error "
                    f"{eta_err:.1e}."
                ),
            },
        ],
        "data": {
            "pump_amplitude_sweep": {
                "a3_grid": [round(float(v), 4) for v in A3_grid],
                "exchange_period": [round(float(v), 9) for v in tex_s],
                "depletion_depth_min_over_max": [float(f"{v:.6e}") for v in dep_s],
                "max_invariant_drift": float(f"{np.nanmax(drift_s):.6e}"),
                "integration_span": T_sweep,
                "rtol": rt_sweep,
            },
            "shg_reference": {
                "A": float(A),
                "n_points": int(np.asarray(tg).size),
                "max_error": float(f"{eta_err:.6e}"),
            },
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv=None):
    ap = argparse.ArgumentParser(description="TRX-02 three-wave resonant interaction")
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

    # --- non-degenerate run ---------------------------------------------------
    a10, a20, a30 = 0.2 + 0j, 0.3 + 0j, 1.0j  # pump phase pi/2 -> Im(Z) != 0
    y0 = [a10.real, a10.imag, a20.real, a20.imag, a30.real, a30.imag]
    T = 20.0 if smoke else 50.0
    sol = solve_ivp(
        rhs, (0.0, T), y0, method="DOP853", rtol=1e-13, atol=1e-13, dense_output=True, max_step=0.02
    )
    inv0 = invariants(y0)
    ts = np.linspace(0.0, T, 600 if smoke else 2500)
    Y = sol.sol(ts)
    inv = np.array([invariants(Y[:, i]) for i in range(ts.size)])
    drift = np.max(np.abs(inv - inv[0]), axis=0)
    add("ManleyRowe_I13_drift", drift[0], 0.0, 1e-10, "dimless", "|a1|^2+|a3|^2")
    add("ManleyRowe_I23_drift", drift[1], 0.0, 1e-10, "dimless", "|a2|^2+|a3|^2")
    add("ManleyRowe_I12diff_drift", drift[2], 0.0, 1e-10, "dimless", "|a1|^2-|a2|^2")

    # --- exchange period & revivals -------------------------------------------
    n3 = np.abs(Y[4] + 1j * Y[5]) ** 2
    # find first local maximum of n3 after t>0.2 by dense sampling
    dense_t = np.linspace(0.0, T, 20001)
    n3d = np.abs(sol.sol(dense_t)[4] + 1j * sol.sol(dense_t)[5]) ** 2
    maxima = []
    for i in range(1, dense_t.size - 1):
        if n3d[i] > n3d[i - 1] and n3d[i] >= n3d[i + 1] and dense_t[i] > 0.2:
            maxima.append(float(dense_t[i]))
        if len(maxima) == 3:
            break
    from scipy.optimize import minimize_scalar

    def neg_n3(t):
        z = sol.sol(np.array([t]))[:, 0]
        return -float(abs(z[4] + 1j * z[5]) ** 2)

    refined = [
        minimize_scalar(
            neg_n3, bounds=(t - 0.01, t + 0.01), method="bounded", options={"xatol": 1e-13}
        ).x
        for t in maxima
    ]
    Tex1, Tex2 = refined[1] - refined[0], refined[2] - refined[1]

    def n3_at(t):
        z = sol.sol(np.array([t]))[:, 0]
        return float(np.abs(z[4] + 1j * z[5]) ** 2)

    revival = abs(n3_at(refined[1]) - n3_at(refined[0]))
    add(
        "Pump_period_repeatability",
        abs(Tex2 - Tex1),
        0.0,
        1e-6,
        "dimless",
        f"T_ex1={Tex1:.9f}, T_ex2={Tex2:.9f}",
    )
    add(
        "Pump_revival_error", revival, 0.0, 1e-8, "dimless", "|a3|^2 after one full exchange period"
    )
    add(
        "Pump_full_depletion_occurs",
        1.0 if n3d.min() < 0.05 * n3d.max() else 0.0,
        1.0,
        1e-12,
        "bool",
        "pump drops below 5% of its peak",
    )

    # --- degenerate channel (SHG) vs tanh^2 -----------------------------------
    A = 1.0
    y0g = [A, 0.0, A, 0.0, 0.0, 0.0]  # s = a1 = a2 = A (real), p = a3 = 0
    solg = solve_ivp(
        rhs,
        (0.0, 3.0),
        y0g,
        method="DOP853",
        rtol=1e-13,
        atol=1e-13,
        dense_output=True,
        max_step=0.01,
    )
    tg = np.linspace(0.05, 3.0, 60)
    Yg = solg.sol(tg)
    p_num = np.abs(Yg[4] + 1j * Yg[5]) ** 2  # |p|^2
    eta_num = p_num / (p_num + np.abs(Yg[0] + 1j * Yg[1]) ** 2)
    eta_ref = np.tanh(A * tg) ** 2
    err_shg = float(np.max(np.abs(eta_num - eta_ref)))
    add(
        "SHG_tanh2_conversion_error",
        err_shg,
        0.0,
        1e-8,
        "dimless",
        "eta(t) = tanh^2(A t), plane-wave second-harmonic generation",
    )

    # --- SVG -------------------------------------------------------------------
    out = Path(__file__).resolve().parents[1] / "results"
    out.mkdir(exist_ok=True)
    n1 = np.abs(Y[0] + 1j * Y[1]) ** 2
    n2 = np.abs(Y[2] + 1j * Y[3]) ** 2
    stride = max(1, ts.size // 500)
    make_svg(ts[::stride], n1[::stride], n2[::stride], n3[::stride], out / "trx02_plot.svg")

    # --- canonical figures (--figures, additive) -----------------------------
    figures_block = None
    figdir = Path(__file__).resolve().parents[1] / "figures"
    if args.figures:
        figures_block = render_figures(
            sol=sol,
            ts=ts,
            Y=Y,
            inv=inv,
            inv0=inv0,
            maxima=refined,
            Tex1=Tex1,
            revival=revival,
            tg=tg,
            eta_num=eta_num,
            eta_ref=eta_ref,
            A=A,
            smoke=smoke,
            figdir=figdir,
        )

    # --- protocol ---------------------------------------------------------------
    all_pass = all(c["pass"] for c in CHECKS)
    protocol = {
        "study": "TRX-02",
        "title": "Resonant three-wave interaction (Manley–Rowe, chi(2) optics)",
        "status": "PASS" if all_pass else "FAIL",
        "smoke": bool(smoke),
        "runtime_s": round(time.time() - t0, 3),
        "checks": CHECKS,
        "series": {
            "t": ts[::stride].round(6).tolist(),
            "n1": n1[::stride].round(10).tolist(),
            "n2": n2[::stride].round(10).tolist(),
            "n3": n3[::stride].round(10).tolist(),
        },
        "meta": {
            "equations": [
                "da1/dt = i a2* a3 ; da2/dt = i a1* a3 ; da3/dt = i a1 a2",
                "I1 = |a1|^2+|a3|^2 ; I2 = |a2|^2+|a3|^2 ; I3 = |a1|^2-|a2|^2",
                "SHG degenerate limit: eta(t) = tanh^2(A t)",
            ],
            "initial_state": {"a1": "0.2", "a2": "0.3", "a3": "1.0j"},
            "exchange_period_Tex": Tex1,
            "invariants_initial": inv0,
            "note": "equal-coupling lossless system; canonically equivalent to the Euler top "
            "(hence to the Kirchhoff three-vortex problem used by TRIVORTEX)",
        },
    }
    if figures_block is not None:
        protocol["figures"] = figures_block
    (out / "trx02_results.json").write_text(json.dumps(protocol, indent=2), encoding="utf-8")

    print(f"\nTRX-02 — three-wave resonant mixing  [{'SMOKE' if smoke else 'FULL'}]")
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
