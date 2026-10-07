#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
TRIVORTEX LAB — TRX-04 — PHOTON FLUID: THREE KERR SOLITONS (SPATIAL, 2-D)
============================================================================
Three laser beams propagating through a focusing Kerr medium behave as a
"photon fluid": each beam is a spatial soliton of the focusing nonlinear
Schroedinger equation  i A_z + (1/2) laplacian(A) + |A|^2 A = 0, and pairs
of same-phase solitons attract while opposite-phase solitons repel.  In
the particle approximation the pair potential is

    V_pm(r) = -U exp(-r/w)   (in phase) ,   V_ap(r) = +U exp(-r/w)   (antiphase)

which produces a Lagrange-like rigidly rotating equilateral triangle of
beams — the optical analogue of the three-body Lagrange solution used in
TRIVORTEX Theorem 3.1.

What is computed
  * rigid rotation of an in-phase soliton triangle (omega vs analytic)
  * energy & angular-momentum conservation
  * antiphase expansion, in-phase bound "binary" with precession

With --figures: hand-authored scheme SVG + four canonical PNG panels
(300 dpi) into figures/, and a "figures" block added to the JSON protocol
(scheme, panels with captions, side/velocity sweep data). Composable with
--smoke; without --figures the behavior, checks and JSON are unchanged.

Usage:  python trx04_photon_fluid.py [--smoke] [--figures]
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

U, W, M = 1.0, 1.0, 1.0

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
# Model: N planar bodies, pair potential +/- U exp(-r/w)
# ---------------------------------------------------------------------------


def forces(state, sign):
    """sign=+1: repulsive (+U e^{-r/w}); sign=-1: attractive."""
    n = state.size // 4
    xy = state.reshape(n, 4)[:, 0:2]
    F = np.zeros((n, 2))
    for k in range(n):
        for j in range(n):
            if j == k:
                continue
            d = xy[k] - xy[j]
            r = np.hypot(d[0], d[1])
            Fmag = sign * (U / W) * np.exp(-r / W)  # radial force magnitude on k from j
            F[k] += Fmag * d / r
    return F


def rhs(t, state, sign):
    """Derivative in the SAME interleaved layout as the state:
    [x1,y1,vx1,vy1, ...] -> [vx1,vy1,ax1,ay1, ...]."""
    n = state.size // 4
    s = state.reshape(n, 4)
    F = forces(state, sign) / M
    out = np.empty_like(s)
    out[:, 0:2] = s[:, 2:4]
    out[:, 2:4] = F
    return out.reshape(-1)


def pot_energy(state, sign):
    n = state.size // 4
    xy = state.reshape(n, 4)[:, 0:2]
    Vp = 0.0
    for k in range(n):
        for j in range(k + 1, n):
            r = np.hypot(*(xy[k] - xy[j]))
            # sign=-1: attractive V=-U e^{-r/w}; sign=+1: repulsive V=+U e^{-r/w}
            Vp += sign * U * np.exp(-r / W)
    K = 0.5 * M * float(np.sum(state.reshape(n, 4)[:, 2:4] ** 2))
    return K + Vp


def ang_momentum(state):
    n = state.size // 4
    s = state.reshape(n, 4)
    return float(np.sum(M * (s[:, 0] * s[:, 3] - s[:, 1] * s[:, 2])))


# ---------------------------------------------------------------------------
# SVG
# ---------------------------------------------------------------------------


def _poly(pts, color, sw=1.6, op=1.0):
    s = " ".join(f"{px:.2f},{py:.2f}" for px, py in pts)
    return (
        f'<polyline fill="none" stroke="{color}" stroke-width="{sw}" opacity="{op}" points="{s}"/>'
    )


def make_svg(traj_rot, traj_rep, path):
    W, H = 900, 520
    cx, cy, sc = 230.0, 270.0, 52.0
    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect width="{W}" height="{H}" fill="#0A1230"/>',
        '<text x="24" y="34" fill="#FFFFFF" font-family="Arial" font-size="19" '
        'font-weight="bold">TRX-04 &#8212; Photon fluid: three Kerr solitons</text>',
    ]
    for k in range(3):
        s.append(_poly([(cx + px * sc, cy - py * sc) for px, py in traj_rot[k]], "#F2C14E"))
    cx2, sc2 = 650.0, 20.0
    for k in range(3):
        s.append(_poly([(cx2 + px * sc2, cy - py * sc2) for px, py in traj_rep[k]], "#6FB7FF"))
    s += [
        '<text x="120" y="470" fill="#F2C14E" font-family="Arial" font-size="14">in-phase: rigidly rotating Lagrange triangle</text>',
        '<text x="540" y="470" fill="#6FB7FF" font-family="Arial" font-size="14">anti-phase: mutual repulsion</text>',
        '<text x="120" y="492" fill="#9FB3D9" font-family="Arial" font-size="12">spatial solitons in a focusing Kerr medium (particle approximation)</text>',
        "</svg>",
    ]
    Path(path).write_text("\n".join(s), encoding="utf-8")


# ---------------------------------------------------------------------------
# Canonical figures (--figures mode): scheme SVG + four PNG panels
# ---------------------------------------------------------------------------


def triangle_setup(a):
    """Initial interleaved state and analytic rotation rate of an equilateral
    beam triangle of side a (in-phase attraction)."""
    rc = a / np.sqrt(3.0)
    om = np.sqrt(3.0 * U * np.exp(-a / W) / (M * a * W))
    ang = np.array([np.pi / 2, np.pi / 2 + 2 * np.pi / 3, np.pi / 2 + 4 * np.pi / 3])
    pos = rc * np.stack([np.cos(ang), np.sin(ang)], axis=1)
    vel = om * rc * np.stack([-np.sin(ang), np.cos(ang)], axis=1)
    return np.stack([pos, vel], axis=1).reshape(-1), om


def make_scheme_svg(path):
    """Hand-authored schematic of the photon fluid (white bg, navy/gold)."""
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
        'fill="#0A1730">TRX-04 &#8212; Scheme: photon fluid &#8212; three Kerr solitons</text>',
        f'  <text x="30" y="63" font-family="{F}" font-size="13" fill="#3A4A66">Light in a '
        "focusing Kerr medium behaves as a fluid of photons: in-phase spatial solitons "
        "attract, anti-phase solitons repel</text>",
        # ---- left panel: Kerr medium (top view) with the beam triangle -------
        '  <rect x="70" y="92" width="350" height="308" rx="10" fill="#FBF6E8" '
        'stroke="#0A1730" stroke-width="2"/>',
        f'  <text x="245" y="86" font-family="{F}" font-size="12" fill="#0A1730" '
        'text-anchor="middle">focusing Kerr medium &#8212; top view</text>',
        f'  <text x="245" y="418" font-family="{F}" font-size="11" fill="#3A4A66" '
        'text-anchor="middle">beams propagate along z (out of the page)</text>',
        # triangle edges (in-phase attraction)
        '  <line x1="245" y1="170" x2="172" y2="298" stroke="#0A1730" stroke-width="1.7"/>',
        '  <line x1="172" y1="298" x2="318" y2="298" stroke="#0A1730" stroke-width="1.7"/>',
        '  <line x1="318" y1="298" x2="245" y2="170" stroke="#0A1730" stroke-width="1.7"/>',
        # radius line + centroid
        '  <line x1="245" y1="255" x2="245" y2="170" stroke="#0A1730" stroke-width="1" '
        'stroke-dasharray="3 3" opacity="0.7"/>',
        '  <line x1="239" y1="255" x2="251" y2="255" stroke="#0A1730" stroke-width="1.4"/>',
        '  <line x1="245" y1="249" x2="245" y2="261" stroke="#0A1730" stroke-width="1.4"/>',
        f'  <text x="252" y="212" font-family="{F}" font-size="11.5" fill="#0A1730">'
        "r_c = a/&#8730;3</text>",
        # rotation arrow (CCW as drawn) + rate
        '  <path d="M 321 179 A 108 108 0 0 0 169 179" fill="none" stroke="#0A1730" '
        'stroke-width="1.8" marker-end="url(#arrN)"/>',
        f'  <text x="245" y="132" font-family="{F}" font-size="13" font-weight="bold" '
        'fill="#0A1730" text-anchor="middle">&#969; = 0.2231</text>',
        # attractive pair forces from the top beam along the edges
        '  <line x1="263" y1="202" x2="303" y2="272" stroke="#D4AF37" stroke-width="1.8" '
        'marker-end="url(#arrG)"/>',
        '  <line x1="227" y1="202" x2="187" y2="272" stroke="#D4AF37" stroke-width="1.8" '
        'marker-end="url(#arrG)"/>',
        # beam spots (concentric = beam profile)
        '  <circle cx="245" cy="170" r="15" fill="#D4AF37" fill-opacity="0.22" '
        'stroke="#0A1730" stroke-width="1.5"/>',
        '  <circle cx="245" cy="170" r="9" fill="#D4AF37" fill-opacity="0.5" ' 'stroke="none"/>',
        '  <circle cx="245" cy="170" r="4" fill="#D4AF37" stroke="#0A1730" ' 'stroke-width="1.2"/>',
        '  <circle cx="172" cy="298" r="15" fill="#D4AF37" fill-opacity="0.22" '
        'stroke="#0A1730" stroke-width="1.5"/>',
        '  <circle cx="172" cy="298" r="9" fill="#D4AF37" fill-opacity="0.5" ' 'stroke="none"/>',
        '  <circle cx="172" cy="298" r="4" fill="#D4AF37" stroke="#0A1730" ' 'stroke-width="1.2"/>',
        '  <circle cx="318" cy="298" r="15" fill="#D4AF37" fill-opacity="0.22" '
        'stroke="#0A1730" stroke-width="1.5"/>',
        '  <circle cx="318" cy="298" r="9" fill="#D4AF37" fill-opacity="0.5" ' 'stroke="none"/>',
        '  <circle cx="318" cy="298" r="4" fill="#D4AF37" stroke="#0A1730" ' 'stroke-width="1.2"/>',
        f'  <text x="278" y="160" font-family="{F}" font-size="12" font-weight="bold" '
        'fill="#0A1730">beam 1</text>',
        f'  <text x="172" y="332" font-family="{F}" font-size="12" font-weight="bold" '
        'fill="#0A1730" text-anchor="middle">beam 2</text>',
        f'  <text x="318" y="332" font-family="{F}" font-size="12" font-weight="bold" '
        'fill="#0A1730" text-anchor="middle">beam 3</text>',
        f'  <text x="296" y="222" font-family="{F}" font-size="11.5" fill="#0A1730">'
        "a = 3</text>",
        f'  <text x="245" y="368" font-family="{F}" font-size="12" fill="#0A1730" '
        'text-anchor="middle">in-phase triplet: rigidly rotating</text>',
        f'  <text x="245" y="386" font-family="{F}" font-size="12" fill="#0A1730" '
        'text-anchor="middle">Lagrange beam triangle (optical)</text>',
        # ---- right panel: pair interaction ------------------------------------
        '  <line x1="520" y1="330" x2="925" y2="330" stroke="#0A1730" stroke-width="1.5" '
        'marker-end="url(#arrN)"/>',
        '  <line x1="535" y1="355" x2="535" y2="115" stroke="#0A1730" stroke-width="1.5" '
        'marker-end="url(#arrN)"/>',
        f'  <text x="925" y="348" font-family="{F}" font-size="12" fill="#0A1730" '
        'text-anchor="end">beam separation r [w]</text>',
        f'  <text x="548" y="106" font-family="{F}" font-size="12" fill="#0A1730" '
        'text-anchor="end">pair energy V(r)</text>',
        # ticks
        '  <line x1="631" y1="330" x2="631" y2="335" stroke="#0A1730" stroke-width="1"/>',
        '  <line x1="727" y1="330" x2="727" y2="335" stroke="#0A1730" stroke-width="1"/>',
        '  <line x1="823" y1="330" x2="823" y2="335" stroke="#0A1730" stroke-width="1"/>',
        f'  <text x="631" y="348" font-family="{F}" font-size="10.5" fill="#3A4A66" '
        'text-anchor="middle">2</text>',
        f'  <text x="727" y="348" font-family="{F}" font-size="10.5" fill="#3A4A66" '
        'text-anchor="middle">4</text>',
        f'  <text x="823" y="348" font-family="{F}" font-size="10.5" fill="#3A4A66" '
        'text-anchor="middle">6</text>',
        # zero line
        '  <line x1="535" y1="245" x2="920" y2="245" stroke="#0A1730" stroke-width="0.9" '
        'stroke-dasharray="4 4" opacity="0.5"/>',
        f'  <text x="920" y="239" font-family="{F}" font-size="10.5" fill="#3A4A66" '
        'text-anchor="end">V = 0 (free beams)</text>',
        # attractive curve V = -U exp(-r/w)
        '  <path d="M 535 355 C 555 320 565 300 583 294 C 605 277 615 272 631 270 '
        "C 655 261 665 255 679 250.5 C 700 247.5 715 247 727 247 C 760 245.8 800 245.3 "
        '920 245.2" fill="none" stroke="#D4AF37" stroke-width="2.2"/>',
        f'  <text x="618" y="312" font-family="{F}" font-size="11.5" fill="#0A1730">in phase: '
        "attraction</text>",
        f'  <text x="618" y="327" font-family="{F}" font-size="11" fill="#3A4A66">V = '
        "&#8722;U&#183;exp(&#8722;r/w)</text>",
        # repulsive curve V = +U exp(-r/w)
        '  <path d="M 535 135 C 555 170 565 195 583 204 C 605 222 615 227 631 230 '
        "C 655 235 665 238 679 239.5 C 700 242 715 242.5 727 243 C 760 244 800 244.7 "
        '920 244.9" fill="none" stroke="#C44E52" stroke-width="1.8" '
        'stroke-dasharray="7 5"/>',
        f'  <text x="618" y="172" font-family="{F}" font-size="11.5" fill="#C44E52">anti-phase: '
        "repulsion</text>",
        f'  <text x="618" y="187" font-family="{F}" font-size="11" fill="#C44E52">V = '
        "+U&#183;exp(&#8722;r/w)</text>",
        # operating point a = 3
        '  <line x1="679" y1="330" x2="679" y2="205" stroke="#0A1730" stroke-width="1" '
        'stroke-dasharray="3 3" opacity="0.8"/>',
        '  <circle cx="679" cy="250.5" r="5" fill="#D4AF37" stroke="#0A1730" '
        'stroke-width="1.5"/>',
        f'  <text x="688" y="272" font-family="{F}" font-size="11.5" font-weight="bold" '
        'fill="#0A1730">operating point a = 3:</text>',
        f'  <text x="688" y="288" font-family="{F}" font-size="11" fill="#3A4A66">force '
        "(U/w)&#183;exp(&#8722;3) = 0.0498</text>",
        f'  <text x="688" y="303" font-family="{F}" font-size="11" fill="#3A4A66">supplies the '
        "centripetal balance m&#969;&#178;r_c</text>",
        # info box: rotation law
        '  <rect x="700" y="78" width="222" height="58" rx="6" fill="#FFFFFF" '
        'stroke="#0A1730" stroke-width="1.4"/>',
        f'  <text x="712" y="100" font-family="{F}" font-size="12" font-weight="bold" '
        'fill="#0A1730">rigid rotation (Lagrange analog)</text>',
        f'  <text x="712" y="120" font-family="{F}" font-size="11.5" '
        'fill="#0A1730">&#969;&#178; = 3U exp(&#8722;a/w)/(m a w) = 0.0498</text>',
        # info box: binary note
        '  <rect x="560" y="398" width="364" height="58" rx="6" fill="#FBF6E8" '
        'stroke="#0A1730" stroke-width="1.4"/>',
        f'  <text x="574" y="420" font-family="{F}" font-size="12" font-weight="bold" '
        'fill="#0A1730">in-phase pair (binary)</text>',
        f'  <text x="574" y="440" font-family="{F}" font-size="11" fill="#0A1730">bound while '
        "v_b &lt; &#8730;(U&#183;exp(&#8722;r_c/w)) = 0.2231;  preset v_b = 0.15:</text>",
        f'  <text x="574" y="454" font-family="{F}" font-size="11" fill="#3A4A66">precessing '
        "bound orbit, separation within [0.63, 4.79]</text>",
        # footer
        f'  <text x="30" y="524" font-family="{F}" font-size="10.5" fill="#6B7A94">TRIVORTEX '
        "Research Program &#183; study TRX-04 &#183; the beam triangle is the optical sibling "
        "of the Lagrange solution (Theorem 3.1)</text>",
        "</svg>",
    ]
    Path(path).write_text("\n".join(s), encoding="utf-8")


def render_figures(sol, solr, solb, ts, Y, tsr, tsb, Yb, pos, dev, slope, omega, a, smoke, figdir):
    """Render the scheme SVG and four canonical PNG panels into figures/.

    Reuses the dynamics already integrated in main(); adds the side-length
    sweep of the triangle and the binary launch-velocity sweep for the
    parameter panel. Returns the "figures" block for the JSON protocol.
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
    suptitle = "TRX-04 · Photon fluid: three Kerr solitons"
    make_scheme_svg(figdir / "scheme_trx04.svg")

    # ---- parameter sweeps (fig03) --------------------------------------------
    # (a) rotation rate vs triangle side: analytic law + numeric re-runs
    a_grid = (
        np.array([2.0, 2.5, 3.0, 4.0, 5.0, 6.5, 8.0]) if not smoke else np.array([2.0, 3.0, 5.0])
    )
    om_an = np.sqrt(3.0 * U * np.exp(-a_grid / W) / (M * a_grid * W))
    om_newt_grid = np.sqrt(3.0 / a_grid**3)  # Newtonian 1/r reference
    om_num = []
    for a_i in a_grid:
        st0_i, om_i = triangle_setup(a_i)
        s_i = solve_ivp(
            rhs,
            (0.0, 2.0 * np.pi / om_i),
            st0_i,
            args=(-1.0,),
            method="DOP853",
            rtol=1e-12,
            atol=1e-12,
            max_step=0.1,
        )
        Yi = s_i.y.reshape(3, 4, -1)
        com = Yi[:, 0:2, :].mean(axis=0)
        rel = Yi[0, 0:2, :] - com
        th = np.unwrap(np.arctan2(rel[1], rel[0]))
        om_num.append(float(np.polyfit(s_i.t, th, 1)[0]))
    om_num = np.array(om_num)

    # (b) binary launch-velocity sweep: max separation vs v_b
    r0b = 3.0
    vb_esc = float(np.sqrt(U * np.exp(-r0b / W)))  # escape threshold e^{-3/2}
    vb_grid = (
        np.unique(np.concatenate([np.linspace(0.06, 0.34, 15), [0.15]]))
        if not smoke
        else np.array([0.10, 0.15, 0.22, 0.30])
    )
    T_sw = 40.0 if not smoke else 12.0
    vb_maxsep = []
    for vb_i in vb_grid:
        st0b_i = np.array([-r0b / 2, 0.0, 0.0, -vb_i, +r0b / 2, 0.0, 0.0, +vb_i])
        s_i = solve_ivp(
            rhs,
            (0.0, T_sw),
            st0b_i,
            args=(-1.0,),
            method="DOP853",
            rtol=1e-12,
            atol=1e-12,
            max_step=0.1,
        )
        Yi = s_i.y.reshape(2, 4, -1)
        vb_maxsep.append(float(np.max(np.hypot(Yi[1, 0] - Yi[0, 0], Yi[1, 1] - Yi[0, 1]))))
    vb_maxsep = np.array(vb_maxsep)

    # ================= fig01 — model landscape =================================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    rg = np.linspace(0.02, 8.0, 900)
    ax1.plot(
        rg,
        -U * np.exp(-rg / W),
        color=GOLD,
        lw=2.4,
        label="in phase  $V=-U\\,e^{-r/w}$ (attraction)",
    )
    ax1.plot(
        rg,
        +U * np.exp(-rg / W),
        color=red,
        lw=1.8,
        ls="--",
        label="anti-phase  $V=+U\\,e^{-r/w}$ (repulsion)",
    )
    ax1.axhline(0.0, color=NAVY, lw=0.9, ls="--", alpha=0.5)
    ax1.axvline(a, color=NAVY, lw=1.0, ls=":", alpha=0.8)
    ax1.plot([a], [-U * np.exp(-a / W)], "o", ms=9, mfc=GOLD, mec=NAVY, mew=1.4, zorder=6)
    ax1.annotate(
        rf"operating point $a = {a:.0f}$:\n"
        rf"$F = (U/w)\,e^{{-a/w}} = {(U / W) * np.exp(-a / W):.4f}$",
        xy=(a, -U * np.exp(-a / W)),
        xycoords="data",
        xytext=(0.11, 0.16),
        textcoords="axes fraction",
        fontsize=10.5,
        color=NAVY,
        ha="left",
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none"),
        arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.9, alpha=0.6),
    )
    ax1.annotate(
        "the phase plays the role\nof an attractive/repulsive charge",
        xy=(4.0, 0.52),
        fontsize=10.5,
        color=NAVY,
        ha="center",
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none"),
    )
    ax1.set_xlim(0.0, 8.0)
    ax1.set_ylim(-1.12, 1.12)
    ax1.set_xlabel("beam separation $r$ [beam-waist units $w$]")
    ax1.set_ylabel("pair potential $V(r)$ [energy units $U$]")
    ax1.set_title("(a) Photon-fluid pair interaction landscape")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=2)

    tri = np.vstack([pos, pos[:1]])
    for k in range(3):
        ax2.plot(tri[k : k + 2, 0], tri[k : k + 2, 1], color=NAVY, lw=1.7, zorder=2)
    com = pos.mean(axis=0)
    for k in range(3):
        ax2.plot(
            [com[0], pos[k, 0]],
            [com[1], pos[k, 1]],
            color=NAVY,
            lw=0.9,
            ls="--",
            alpha=0.6,
            zorder=1,
        )
        for dd in (15.0, 9.0, 4.0):
            ax2.add_patch(
                plt.Circle(
                    pos[k],
                    dd / 60.0,
                    color=GOLD,
                    alpha=1.0 if dd == 4.0 else (0.5 if dd == 9.0 else 0.22),
                    ec=NAVY if dd == 15.0 else "none",
                    lw=1.2,
                    zorder=4,
                )
            )
        d = pos[k] - com
        ax2.annotate(
            "",
            xy=com + 0.30 * d,
            xytext=pos[k],
            arrowprops=dict(arrowstyle="-|>", color=green, lw=1.6),
            zorder=3,
        )
    ax2.plot([com[0]], [com[1]], "+", ms=11, color=NAVY, zorder=5)
    ax2.annotate(
        "centroid", xy=com, textcoords="offset points", xytext=(8, -14), fontsize=10, color=NAVY
    )
    rc = a / np.sqrt(3.0)
    ax2.annotate(
        rf"$r_c = a/\sqrt{{3}} = {rc:.4f}$", xy=(0.16, 0.88), fontsize=10.5, color=NAVY, ha="left"
    )
    ax2.annotate(rf"side $a = {a:.0f}$", xy=(0.0, -1.15), fontsize=10.5, color=NAVY, ha="center")
    ax2.annotate(
        rf"rigid rotation $\omega = {omega:.6f}$",
        xy=(0.0, 2.05),
        fontsize=11,
        color=NAVY,
        ha="center",
        fontweight="bold",
    )
    ax2.annotate(
        "pair forces (attractive)\nsupply $m\\omega^2 r_c$",
        xy=(0.0, -2.12),
        fontsize=10,
        color="#8a6d1c",
        ha="center",
    )
    ax2.set_xlim(-2.3, 2.3)
    ax2.set_ylim(-2.3, 2.3)
    ax2.set_aspect("equal")
    ax2.axis("off")
    ax2.set_title("(b) Initial beam triangle (top view)")
    fig.savefig(figdir / "fig01_photon_fluid_landscape.png")
    plt.close(fig)

    # ================= fig02 — rigid rotation (headline) =======================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    for k, lab in ((0, "beam 1"), (1, "beam 2"), (2, "beam 3")):
        ax1.plot(Y[k, 0], Y[k, 1], color=SERIES[k], lw=1.7, label=lab)
        ax1.plot([Y[k, 0, 0]], [Y[k, 1, 0]], "o", ms=7, mfc=SERIES[k], mec=NAVY, mew=1.1, zorder=6)
    ax1.plot([0.0], [0.0], "+", ms=10, color=NAVY, zorder=5)
    ax1.set_aspect("equal")
    ax1.set_xlim(-2.2, 2.2)
    ax1.set_ylim(-2.2, 2.2)
    ax1.set_xlabel("$x$ [beam-waist units $w$]")
    ax1.set_ylabel("$y$ [beam-waist units $w$]")
    ax1.set_title(
        f"(a) Rigid rotation of the beam triangle "
        f"({float(ts[-1]) / (2 * np.pi / omega):.1f} turns)"
    )
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=3)

    sides = []
    for k1, k2 in ((0, 1), (1, 2), (2, 0)):
        d_t = np.hypot(Y[k1, 0] - Y[k2, 0], Y[k1, 1] - Y[k2, 1])
        sides.append(np.abs(d_t - a) / a)
        ax2.plot(
            ts,
            np.clip(np.abs(d_t - a) / a, 1e-18, None),
            color=SERIES[len(sides) - 1],
            lw=1.6,
            label=rf"$|d_{{{k1 + 1}{k2 + 1}}}(t)-a|/a$",
        )
    ax2.axhline(1e-6, color=NAVY, lw=1.3, ls="--", label=r"acceptance tolerance $10^{-6}$")
    ax2.set_yscale("log")
    ax2.set_ylim(1e-17, 1e-5)
    ax2.set_xlabel("time $t$ [1/$\\omega$ units]")
    ax2.set_ylabel("relative side deviation")
    ax2.set_title("(b) Equilateral rigidity over the whole run")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=2)
    ax2.annotate(
        rf"max deviation $= {dev:.1e}$",
        xy=(0.985, 0.90),
        xycoords="axes fraction",
        ha="right",
        fontsize=10.5,
        color=NAVY,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none"),
    )
    fig.savefig(figdir / "fig02_triangle_rotation.png")
    plt.close(fig)

    # ================= fig03 — parameter sweeps ================================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    af = np.linspace(1.6, 8.4, 400)
    ax1.plot(
        af,
        np.sqrt(3.0 * U * np.exp(-af / W) / (M * af * W)),
        color=GOLD,
        lw=2.2,
        label=r"Kerr: $\omega^2 = 3Ue^{-a/w}/(maw)$",
    )
    ax1.plot(
        af,
        np.sqrt(3.0 / af**3),
        color=NAVY,
        lw=1.4,
        ls="--",
        label=r"Newtonian: $\omega^2 = 3Gm/a^3$",
    )
    ax1.plot(
        a_grid,
        om_num,
        "s",
        ms=7,
        mfc=blue,
        mec=NAVY,
        mew=1.1,
        zorder=6,
        label=r"numeric re-runs (DOP853)",
    )
    ax1.plot(
        [a],
        [omega],
        "*",
        ms=16,
        mfc=GOLD,
        mec=NAVY,
        mew=1.3,
        zorder=7,
        label=rf"preset $a = {a:.0f}$",
    )
    ax1.annotate(
        rf"preset: $\omega({a:.0f}) = {omega:.6f}$",
        xy=(a, omega),
        xycoords="data",
        xytext=(0.62, 0.66),
        textcoords="axes fraction",
        fontsize=10.5,
        color=NAVY,
        ha="left",
        arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.9, alpha=0.5),
    )
    ax1.set_xlabel("triangle side $a$ [beam-waist units $w$]")
    ax1.set_ylabel("rotation rate $\\omega$ [1/time]")
    ax1.set_title("(a) Rotation rate vs triangle side")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=2)

    ax2.plot(
        vb_grid,
        vb_maxsep,
        "o-",
        color=blue,
        lw=1.8,
        ms=5,
        mec=NAVY,
        mew=0.9,
        label=r"max separation over $t = %.0f$" % T_sw,
    )
    ax2.axvline(
        vb_esc,
        color=red,
        lw=1.5,
        ls="--",
        label=rf"escape threshold $v_b^* = e^{{-3/2}} = {vb_esc:.6f}$",
    )
    ax2.axhline(6.0, color=NAVY, lw=1.2, ls=":", label="bound window of the check (sep $< 6$)")
    k_pres = int(np.argmin(np.abs(vb_grid - 0.15)))
    ax2.plot(
        [vb_grid[k_pres]],
        [vb_maxsep[k_pres]],
        "*",
        ms=15,
        mfc=GOLD,
        mec=NAVY,
        mew=1.2,
        zorder=7,
        label=rf"preset $v_b = {vb_grid[k_pres]:.2f}$",
    )
    ax2.set_yscale("log")
    ax2.set_xlabel("launch velocity $v_b$ [w/time]")
    ax2.set_ylabel("max beam separation [w]")
    ax2.set_title("(b) Binary bound/unbound map vs launch velocity")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=1, fontsize=9)
    fig.savefig(figdir / "fig03_parameter_sweeps.png")
    plt.close(fig)

    # ================= fig04 — binary dynamics and invariants ==================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    for k, lab in ((0, "beam 1"), (1, "beam 2")):
        ax1.plot(Yb[k, 0], Yb[k, 1], color=SERIES[k], lw=1.2, label=lab)
        ax1.plot(
            [Yb[k, 0, 0]], [Yb[k, 1, 0]], "o", ms=7, mfc=SERIES[k], mec=NAVY, mew=1.1, zorder=6
        )
    ax1.plot([-r0b / 2, r0b / 2], [0.0, 0.0], "x", ms=8, color=NAVY, zorder=5)
    ax1.set_aspect("equal")
    ax1.set_xlabel("$x$ [beam-waist units $w$]")
    ax1.set_ylabel("$y$ [beam-waist units $w$]")
    ax1.set_title(
        f"(a) Precessing bound orbit of an in-phase pair " f"($T = {float(tsb[-1]):.0f}$)"
    )
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=2)

    stride_e = max(1, ts.size // 300)
    ts_e = ts[::stride_e]
    E_rot = np.array([pot_energy(sol.sol(t), -1.0) for t in ts_e])
    tsr_e = tsr[:: max(1, tsr.size // 300)]
    E_rep = np.array([pot_energy(solr.sol(t), +1.0) for t in tsr_e])
    tsb_e = tsb[:: max(1, tsb.size // 300)]
    E_bin = np.array([pot_energy(solb.sol(t), -1.0) for t in tsb_e])
    ax2.semilogy(
        ts_e, np.abs(E_rot - E_rot[0]) + 1e-20, color=GOLD, lw=1.7, label="rotation (triangle)"
    )
    ax2.semilogy(
        tsr_e, np.abs(E_rep - E_rep[0]) + 1e-20, color=blue, lw=1.7, label="anti-phase trio"
    )
    ax2.semilogy(tsb_e, np.abs(E_bin - E_bin[0]) + 1e-20, color=green, lw=1.7, label="binary orbit")
    ax2.axhline(1e-10, color=NAVY, lw=1.3, ls="--", label=r"acceptance tolerance $10^{-10}$")
    ax2.set_xlabel("time $t$ [1/$\\omega$ units]")
    ax2.set_ylabel("energy drift $|E(t)-E(0)|$ [energy units $U$]")
    ax2.set_title("(b) Conservation of the total energy (invariant)")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=2, fontsize=9)
    fig.savefig(figdir / "fig04_binary_dynamics_invariants.png")
    plt.close(fig)

    # ---- JSON figures block ==================================================
    return {
        "scheme": {
            "file": "figures/scheme_trx04.svg",
            "caption": (
                "Photon-fluid scheme - three in-phase Kerr solitons in a focusing "
                "medium (left): the attractive pair forces along the triangle edges "
                "supply the centripetal balance m omega^2 r_c of the rigidly rotating "
                "Lagrange beam triangle; the pair interaction (right): in-phase "
                "attraction V = -U exp(-r/w), anti-phase repulsion V = +U exp(-r/w), "
                "operating point a = 3 and the binary bound-state condition."
            ),
        },
        "panels": [
            {
                "file": "figures/fig01_photon_fluid_landscape.png",
                "caption": (
                    "Model landscape: (a) photon-fluid pair interaction - in-phase "
                    "attraction V = -U exp(-r/w) (gold) against anti-phase repulsion "
                    "V = +U exp(-r/w) (red); the phase acts as an attractive/repulsive "
                    f"charge, operating point a = {a:.0f} with force (U/w) exp(-a/w) = "
                    f"{(U / W) * np.exp(-a / W):.4f}; (b) initial condition of the rotation "
                    f"run: equilateral beam triangle, side a = {a:.0f}, r_c = a/sqrt(3) = "
                    f"{rc:.4f}, pair forces supplying the centripetal balance m omega^2 r_c."
                ),
            },
            {
                "file": "figures/fig02_triangle_rotation.png",
                "caption": (
                    "Headline result - rigid rotation of the photon-fluid triangle: "
                    "(a) worldlines of the three beams over three full turns, circular "
                    "orbits about the common centroid; (b) relative side deviations "
                    f"|d(t) - a|/a stay below {dev:.1e} (acceptance 1e-6), and the measured "
                    f"rotation rate {slope:.9f} matches the analytic omega = {omega:.9f} "
                    "(tolerance 1e-8) - the optical Lagrange configuration."
                ),
            },
            {
                "file": "figures/fig03_parameter_sweeps.png",
                "caption": (
                    "Parameter sweeps: (a) rotation rate vs triangle side - analytic "
                    "Kerr law omega(a) = sqrt(3U exp(-a/w)/(maw)) against the Newtonian "
                    "1/r reference and numeric DOP853 re-runs at each grid side (preset "
                    f"a = {a:.0f}: omega = {omega:.6f} vs Newtonian "
                    f"{float(np.sqrt(3.0 / a ** 3)):.6f}); (b) binary bound/unbound map - "
                    "max separation vs launch velocity v_b with the analytic escape "
                    f"threshold v_b* = exp(-3/2) = {vb_esc:.6f} and the bound window of "
                    "the acceptance check (separation < 6)."
                ),
            },
            {
                "file": "figures/fig04_binary_dynamics_invariants.png",
                "caption": (
                    "Dynamics and invariants: (a) precessing bound orbit of the in-phase "
                    f"binary (launch separation 3, transverse velocity 0.15, E_rel = "
                    "-0.027 < 0, T = 80); (b) energy drift |E(t) - E(0)| of the three runs "
                    "(rotation, anti-phase trio, binary) on a log scale against the "
                    "1e-10 acceptance tolerance - all invariants conserved at machine "
                    "to integrator level."
                ),
            },
        ],
        "data": {
            "side_sweep": {
                "a": [round(float(v), 4) for v in a_grid],
                "omega_analytic": [round(float(v), 9) for v in om_an],
                "omega_numeric": [round(float(v), 9) for v in om_num],
                "omega_newtonian": [round(float(v), 9) for v in om_newt_grid],
            },
            "binary_sweep": {
                "vb": [round(float(v), 4) for v in vb_grid],
                "max_separation": [round(float(v), 4) for v in vb_maxsep],
                "escape_threshold_vb": round(vb_esc, 6),
                "T_sweep": float(T_sw),
            },
            "preset": {
                "a": float(a),
                "omega_triangle": round(float(omega), 9),
                "omega_newtonian_reference": round(float(np.sqrt(3.0 / a**3)), 9),
                "max_side_deviation": float(dev),
                "measured_rotation_rate": float(slope),
                "T_rotation": round(float(ts[-1]), 4),
                "T_repulsion": round(float(tsr[-1]), 4),
                "T_binary": round(float(tsb[-1]), 4),
                "r_c": round(float(a / np.sqrt(3.0)), 6),
                "force_at_operating_point": round(float((U / W) * np.exp(-a / W)), 6),
            },
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv=None):
    ap = argparse.ArgumentParser(description="TRX-04 photon fluid: three Kerr solitons")
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

    a = 3.0  # triangle side
    rc = a / np.sqrt(3.0)
    omega = np.sqrt(3.0 * U * np.exp(-a / W) / (M * a * W))
    ang = np.array([np.pi / 2, np.pi / 2 + 2 * np.pi / 3, np.pi / 2 + 4 * np.pi / 3])
    pos = rc * np.stack([np.cos(ang), np.sin(ang)], axis=1)
    vel = omega * rc * np.stack([-np.sin(ang), np.cos(ang)], axis=1)
    # interleaved per-body layout: [x1,y1,vx1,vy1, x2,y2,vx2,vy2, ...]
    st0 = np.stack([pos, vel], axis=1).reshape(-1)

    T = 3.0 * 2.0 * np.pi / omega  # three rotations
    if smoke:
        T *= 0.25
    sol = solve_ivp(
        rhs,
        (0.0, T),
        st0,
        args=(-1.0,),
        method="DOP853",
        rtol=1e-12,
        atol=1e-12,
        dense_output=True,
        max_step=0.1,
    )
    ts = np.linspace(0.0, T, 600 if smoke else 2400)
    Y = sol.sol(ts).reshape(3, 4, -1)

    sides_t = np.array([np.hypot(*(Y[1, 0:2, i] - Y[0, 0:2, i])) for i in range(ts.size)])
    dev = float(np.max(np.abs(sides_t - a)) / a)
    add(
        "triangle_equilateral_deviation",
        dev,
        0.0,
        1e-6,
        "rel",
        "max side deviation over 3 rotations",
    )

    # measured angular velocity from body-1 polar angle about the centroid
    com = Y[:, 0:2, :].mean(axis=0)
    rel = Y[0, 0:2, :] - com
    theta = np.unwrap(np.arctan2(rel[1], rel[0]))
    slope = float(np.polyfit(ts, theta, 1)[0])
    add(
        "measured_rotation_rate",
        slope,
        omega,
        1e-8,
        "1/time",
        f"analytic omega^2 = 3U e^(-a/w)/(m a w) -> omega = {omega:.9f}",
    )

    E = np.array([pot_energy(sol.sol(t), -1.0) for t in ts[:: max(1, ts.size // 300)]])
    add("energy_conservation_rotation", float(np.max(np.abs(E - E[0]))), 0.0, 1e-10, "energy")
    Lz = np.array([ang_momentum(sol.sol(t)) for t in ts[:: max(1, ts.size // 300)]])
    add("angular_momentum_conservation", float(np.max(np.abs(Lz - Lz[0]))), 0.0, 1e-10, "ang mom")

    # --- anti-phase trio: expansion -------------------------------------------
    st0r = np.stack([pos, np.zeros_like(pos)], axis=1).reshape(-1)
    Tr = 20.0 if smoke else 40.0
    solr = solve_ivp(
        rhs,
        (0.0, Tr),
        st0r,
        args=(+1.0,),
        method="DOP853",
        rtol=1e-12,
        atol=1e-12,
        dense_output=True,
        max_step=0.1,
    )
    tsr = np.linspace(0.0, Tr, 300 if smoke else 1200)
    Yr = solr.sol(tsr).reshape(3, 4, -1)
    d_t = np.array([np.hypot(*(Yr[1, 0:2, i] - Yr[0, 0:2, i])) for i in range(tsr.size)])
    add(
        "antiphase_no_collapse",
        1.0 if d_t.min() >= 0.95 * a else 0.0,
        1.0,
        1e-12,
        "bool",
        f"min pairwise distance {d_t.min():.4f} >= 0.95 a",
    )
    add(
        "antiphase_expands",
        1.0 if d_t[-1] > d_t[0] else 0.0,
        1.0,
        1e-12,
        "bool",
        f"final separation {d_t[-1]:.3f} > initial {d_t[0]:.3f}",
    )
    Er = np.array([pot_energy(solr.sol(t), +1.0) for t in tsr[:: max(1, tsr.size // 300)]])
    add("energy_conservation_repulsion", float(np.max(np.abs(Er - Er[0]))), 0.0, 1e-10, "energy")

    # --- in-phase binary: bound orbit with precession ---------------------------
    r0b, vb = 3.0, 0.15  # E = vb^2 - U e^{-r0b/w} = -0.027 < 0 -> bound
    # body 1: pos (-r0b/2, 0), vel (0, -vb); body 2: pos (+r0b/2, 0), vel (0, +vb)
    st0b = np.array([-r0b / 2, 0.0, 0.0, -vb, +r0b / 2, 0.0, 0.0, +vb])
    Tb = 30.0 if smoke else 80.0
    solb = solve_ivp(
        rhs,
        (0.0, Tb),
        st0b,
        args=(-1.0,),
        method="DOP853",
        rtol=1e-12,
        atol=1e-12,
        dense_output=True,
        max_step=0.1,
    )
    tsb = np.linspace(0.0, Tb, 300 if smoke else 1200)
    Yb = solb.sol(tsb).reshape(2, 4, -1)
    sep = np.array([np.hypot(*(Yb[1, 0:2, i] - Yb[0, 0:2, i])) for i in range(tsb.size)])
    add(
        "binary_stays_bound",
        1.0 if (sep.min() > 0.5 and sep.max() < 6.0) else 0.0,
        1.0,
        1e-12,
        "bool",
        f"separation range [{sep.min():.3f}, {sep.max():.3f}]",
    )
    Eb = np.array([pot_energy(solb.sol(t), -1.0) for t in tsb[:: max(1, tsb.size // 300)]])
    add("binary_energy_conservation", float(np.max(np.abs(Eb - Eb[0]))), 0.0, 1e-10, "energy")

    # --- SVG -----------------------------------------------------------------------
    out = Path(__file__).resolve().parents[1] / "results"
    out.mkdir(exist_ok=True)
    stride = max(1, ts.size // 500)
    traj_rot = [Y[k, 0:2, ::stride].T for k in range(3)]
    stride_r = max(1, tsr.size // 400)
    traj_rep = [Yr[k, 0:2, ::stride_r].T for k in range(3)]
    make_svg(traj_rot, traj_rep, out / "trx04_plot.svg")

    # --- canonical figures (--figures, additive) -----------------------------
    figures_block = None
    figdir = Path(__file__).resolve().parents[1] / "figures"
    if args.figures:
        figures_block = render_figures(
            sol=sol,
            solr=solr,
            solb=solb,
            ts=ts,
            Y=Y,
            tsr=tsr,
            tsb=tsb,
            Yb=Yb,
            pos=pos,
            dev=dev,
            slope=slope,
            omega=omega,
            a=a,
            smoke=smoke,
            figdir=figdir,
        )

    # --- protocol ---------------------------------------------------------------------
    all_pass = all(c["pass"] for c in CHECKS)
    omega_newton = np.sqrt(3.0 * 1.0 / a**3)  # Newtonian 3Gm/a^3 with G=m=1 (reference)
    protocol = {
        "study": "TRX-04",
        "title": "Photon fluid: three Kerr spatial solitons",
        "status": "PASS" if all_pass else "FAIL",
        "smoke": bool(smoke),
        "runtime_s": round(time.time() - t0, 3),
        "checks": CHECKS,
        "series": {
            "t": ts[::stride].round(4).tolist(),
            "x1": Y[0, 0, ::stride].round(8).tolist(),
            "y1": Y[0, 1, ::stride].round(8).tolist(),
            "x2": Y[1, 0, ::stride].round(8).tolist(),
            "y2": Y[1, 1, ::stride].round(8).tolist(),
            "x3": Y[2, 0, ::stride].round(8).tolist(),
            "y3": Y[2, 1, ::stride].round(8).tolist(),
        },
        "meta": {
            "equations": [
                "i A_z + (1/2) laplacian(A) + |A|^2 A = 0   (focusing NLS)",
                "V_pm(r) = -U exp(-r/w) ; V_ap(r) = +U exp(-r/w)",
                "Lagrange triangle: omega^2 = 3 U exp(-a/w) / (m a w)",
            ],
            "omega_triangle_exp": float(omega),
            "omega_triangle_newtonian_reference": float(omega_newton),
            "mapping_note": "Newtonian V=-1/r gives omega^2=3Gm/a^3; the exponential "
            "Kerr force gives omega^2=3U e^{-a/w}/(m a w) — same "
            "choreography class as TRIVORTEX Theorem 3.1",
        },
    }
    if figures_block is not None:
        protocol["figures"] = figures_block
    (out / "trx04_results.json").write_text(json.dumps(protocol, indent=2), encoding="utf-8")

    print(f"\nTRX-04 — photon fluid: three Kerr solitons  [{'SMOKE' if smoke else 'FULL'}]")
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
