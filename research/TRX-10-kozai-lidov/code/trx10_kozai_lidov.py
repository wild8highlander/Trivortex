#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
TRIVORTEX LAB — TRX-10 — KOZAI–LIDOV OSCILLATIONS IN HIERARCHICAL TRIPLES
============================================================================
Secular three-body dynamics: the double-averaged quadrupole Hamiltonian of
a test particle perturbed by a distant inclined companion drives the
famous Kozai–Lidov eccentricity–inclination oscillations with

    e_max = sqrt(1 - (5/3) cos^2 i0)     (initially circular orbit)

and conserved z-angular momentum j_z = sqrt(1-e^2) cos i.

Method (no memorised formulas): the double average is BUILT numerically —
the instantaneous quadrupole disturbing potential is averaged over the
inner orbit by quadrature, tabulated on an (e, omega) grid for the fixed
j_z of the run, and turned into a cubic spline whose derivatives drive the
Hamiltonian flow.  An independent DIRECT integration of the full 3-D
restricted problem validates the secular model.

Laser link: laser ranging of binary/ triple asteroids; LISA-type laser
interferometry of compact-object triples (KL cycles channeling mergers).

Usage:  python trx10_kozai_lidov.py [--smoke] [--figures]
        --figures additionally renders the canonical deliverables into figures/:
        scheme_trx10.svg (hand-authored navy-gold schematic) + four 300-dpi PNG
        panels (fig01..fig04) and adds a "figures" block to the JSON protocol.
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
from scipy.interpolate import RectBivariateSpline

CHECKS = []

# Canonical figure palette (v2.2.0 monograph edition)
NAVY = "#0A1730"
GOLD = "#D4AF37"
LIGHT_GOLD = "#F0D98C"
SERIES = ["#D4AF37", "#4C72B0", "#55A868", "#C44E52", "#8172B2"]
I_CRIT_DEG = 39.2315  # arccos(sqrt(3/5)) — critical (Kozai) inclination


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
# Double-averaged quadrupole potential (numerical orbit average)
# units: GM_inner = 1, a_in = 1; outer orbit circular, radius a_out, planar
# ---------------------------------------------------------------------------


def averaged_potential(e, omega, j_z, a_out=20.0, n_quad=240):
    e = min(max(float(e), 0.0), 0.99999)
    j = np.sqrt(max(1.0 - e * e, 1e-12))
    cos_i = np.clip(j_z / j, -1.0, 1.0)
    sin_i = np.sqrt(max(1.0 - cos_i * cos_i, 0.0))
    f = np.linspace(0.0, 2.0 * np.pi, n_quad, endpoint=False)
    r_of = (1.0 - e * e) / (1.0 + e * np.cos(f))
    w = r_of**2
    w = w / np.sum(w)
    xp = r_of * np.cos(f)
    yp = r_of * np.sin(f)
    cw, sw = np.cos(omega), np.sin(omega)
    xa = cw * xp - sw * yp
    ya = sw * xp + cw * yp
    yb = cos_i * ya
    zb = sin_i * ya
    rx2 = float(np.sum(w * xa * xa))
    ry2 = float(np.sum(w * yb * yb))
    rz2 = float(np.sum(w * zb * zb))
    return 0.5 * (rx2 + ry2) - rz2  # in units of G m3 / (2 a_out^3)


def build_averager(j_z, a_out=20.0, n_e=160, n_w=180):
    """Tabulate the averaged potential on an (e, omega) grid and return a
    spline-based Hamiltonian with analytic spline derivatives."""
    e_grid = np.linspace(1e-4, 0.999, n_e)
    w_grid = np.linspace(0.0, 2.0 * np.pi, n_w)
    tab = np.zeros((n_e, n_w))
    for i, e in enumerate(e_grid):
        for k, w in enumerate(w_grid):
            tab[i, k] = averaged_potential(e, w, j_z, a_out=a_out)
    spl = RectBivariateSpline(e_grid, w_grid, tab, kx=3, ky=3)

    def H(e, w):
        return float(spl(e, w)[0, 0])

    dH_de = lambda e, w: float(spl(e, w, dx=1)[0, 0])
    dH_dw = lambda e, w: float(spl(e, w, dy=1)[0, 0])
    return H, dH_de, dH_dw


def build_flow(j_z, m3_ratio, a_out=20.0, n_e=160, n_w=180):
    """Scaled Hamiltonian flow: rates x C2 = (3/8)(m3/M)(a_in/a_out)^3 n_in.
    omega is folded into [0, pi) (H has period pi in omega), which keeps the
    phase bounded and the integrator fast."""
    H, dH_de, dH_dw = build_averager(j_z, a_out=a_out, n_e=n_e, n_w=n_w)
    C2 = 0.375 * m3_ratio / a_out**3

    def flow(t, y):
        e, w = y
        e = min(max(e, 1e-6), 0.99999)
        w = w % np.pi
        j = np.sqrt(1.0 - e * e)
        # canonical: de/dt = (j/e) dH/dw ; dw/dt = -(j/e) dH/de  (L = 1)
        return np.array([C2 * j / e * dH_dw(e, w), -C2 * j / e * dH_de(e, w)])

    return flow


def run_kl(e0, i0_deg, m3_ratio=1.0, a_out=20.0, n_cycles=3, n_out=3000, fast=False):
    j_z = np.sqrt(1.0 - e0 * e0) * np.cos(np.radians(i0_deg))
    flow = build_flow(j_z, m3_ratio, a_out=a_out, n_e=40 if fast else 160, n_w=45 if fast else 180)
    # the unscaled-model KL period is ~100 for a_out=20; physical period
    # P = P_model / C2; integrate n_cycles of it
    C2 = 0.375 * m3_ratio / a_out**3
    T = n_cycles * 100.0 / C2 * 0.375 * 1.0 / a_out**3 * a_out**3 * (4.0 / 3.0)
    T = n_cycles * 105.0 / C2 * 0.375
    sol = solve_ivp(
        flow,
        (0.0, T),
        [e0, np.pi / 2],
        method="DOP853",
        rtol=1e-8,
        atol=1e-9,
        dense_output=True,
        max_step=T / 1500,
    )
    ts = np.linspace(0.0, T, n_out)
    Y = sol.sol(ts)
    return ts, Y[0], Y[1], j_z, T


# ---------------------------------------------------------------------------
# Direct 3-D restricted integration (independent validation)
# ---------------------------------------------------------------------------


def direct_kl_emax(i0_deg=60.0, m3_ratio=0.33, a_out=10.0, t_out_periods=6.0):
    GM = 1.0
    n_out_m = np.sqrt(GM * (1.0 + m3_ratio) / a_out**3)
    T = 2.0 * np.pi / n_out_m * t_out_periods

    def rhs(t, y):
        r = y[:3]
        v = y[3:]
        r3v = np.array([a_out * np.cos(n_out_m * t), a_out * np.sin(n_out_m * t), 0.0])
        d = r - r3v
        a = -GM * r / np.linalg.norm(r) ** 3 - m3_ratio * (
            d / np.linalg.norm(d) ** 3 + r3v / a_out**3
        )
        return np.concatenate([v, a])

    e0, i0, w0 = 0.001, np.radians(i0_deg), np.pi / 2
    a_in = 1.0
    p = a_in * (1.0 - e0 * e0)
    r_vec = np.array([p / (1 + e0), 0.0, 0.0])
    v_vec = np.array([0.0, np.sqrt(GM * (1 + e0) / (a_in * (1 - e0))), 0.0])
    cw, sw = np.cos(w0), np.sin(w0)
    R1 = np.array([[cw, -sw, 0], [sw, cw, 0], [0, 0, 1]])
    ci, si = np.cos(i0), np.sin(i0)
    R2 = np.array([[1, 0, 0], [0, ci, -si], [0, si, ci]])
    R = R2 @ R1
    y0 = np.concatenate([R @ r_vec, R @ v_vec])
    n_cap = 6000 if os.environ.get("TRX_SMOKE") else 60000
    sol = solve_ivp(
        rhs,
        (0.0, T),
        y0,
        method="DOP853",
        rtol=1e-11,
        atol=1e-11,
        dense_output=True,
        max_step=T / n_cap,
    )
    ts = np.linspace(0.0, T, 8000 if os.environ.get("TRX_SMOKE") else 40000)
    Yt = sol.sol(ts)
    r = Yt[:3].T
    v = Yt[3:].T
    h = np.cross(r, v)
    ev = np.cross(v, h) / GM - r / np.linalg.norm(r, axis=1)[:, None]
    ecc = np.linalg.norm(ev, axis=1)
    w_len = max(int(ts.size * (2 * np.pi / n_out_m) / T), 3)
    kernel = np.ones(w_len) / w_len
    sm = np.convolve(ecc, kernel, mode="valid")
    return float(sm.max())


# ---------------------------------------------------------------------------
# SVG
# ---------------------------------------------------------------------------


def make_svg(ts, e_t, path):
    W, H = 900, 520
    x0, x1, y0, y1 = 80.0, 860.0, 70.0, 440.0
    tmax = float(ts[-1])
    emax_e = float(np.max(e_t)) * 1.05
    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect width="{W}" height="{H}" fill="#0A1230"/>',
        '<text x="24" y="34" fill="#FFFFFF" font-family="Arial" font-size="19" '
        'font-weight="bold">TRX-10 &#8212; Kozai&#8211;Lidov oscillations (quadrupole, i0=60&#176;)</text>',
        f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="#3A4A6B"/>',
        f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="#3A4A6B"/>',
    ]
    stride = max(1, ts.size // 600)
    pts = " ".join(
        f"{x0 + t/tmax*(x1-x0):.2f},{y1 - e/emax_e*(y1-y0):.2f}"
        for t, e in zip(ts[::stride], e_t[::stride])
    )
    s.append(f'<polyline fill="none" stroke="#F2C14E" stroke-width="2" points="{pts}"/>')
    s.append(
        '<text x="120" y="100" fill="#9FB3D9" font-family="Arial" font-size="13">'
        "e_max = sqrt(1 - (5/3) cos^2 i0)</text>"
    )
    s.append(
        '<text x="430" y="478" fill="#9FB3D9" font-family="Arial" font-size="13">time (KL units)</text>'
    )
    s.append(
        '<text x="24" y="500" fill="#9FB3D9" font-family="Arial" font-size="12">'
        "eccentricity cycles of the inner test particle under a distant inclined companion</text>"
    )
    s.append("</svg>")
    Path(path).write_text("\n".join(s), encoding="utf-8")


# ---------------------------------------------------------------------------
# Canonical scheme + figures (--figures mode): navy-gold, white background
# ---------------------------------------------------------------------------


def make_scheme_svg(path):
    """Hand-authored schematic of the Kozai–Lidov exchange (white bg, navy/gold).

    Left: hierarchical triple — inner binary (gold primary + test particle on
    an inclined, eccentric orbit) inside the distant companion's orbit.
    Right: inclination diagram with the critical Kozai angle and the
    eccentricity–inclination exchange arrows.
    """
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
        'fill="#0A1730">TRX-10 &#8212; Scheme: Kozai&#8211;Lidov exchange in a hierarchical triple</text>',
        f'  <text x="30" y="63" font-family="{F}" font-size="13" fill="#3A4A66">A distant inclined '
        "companion drives eccentricity&#8211;inclination oscillations; "
        "j_z = &#8730;(1&#8722;e&#178;)&#183;cos i stays constant</text>",
        # ---- left panel: hierarchical triple geometry ------------------------
        f'  <text x="30" y="96" font-family="{F}" font-size="14" font-weight="bold" '
        'fill="#0A1730">Hierarchical triple (inner orbit inclined by i&#8320; = 60&#176;)</text>',
        # KL clock box (top-left)
        '  <rect x="28" y="112" width="190" height="56" rx="6" fill="#FFFFFF" '
        'stroke="#0A1730" stroke-width="1.4"/>',
        f'  <text x="40" y="132" font-family="{F}" font-size="12.5" font-weight="bold" '
        'fill="#0A1730">KL clock: t_KL ~ 1/C&#8322;</text>',
        f'  <text x="40" y="149" font-family="{F}" font-size="10.5" fill="#0A1730">C&#8322; = '
        "(3/8)(m&#8323;/M)(a_in/a_out)&#179;n_in</text>",
        f'  <text x="40" y="163" font-family="{F}" font-size="10.5" fill="#3A4A66">period halves when '
        "m&#8323; doubles</text>",
        # outer orbit (dashed navy circle, not to scale), center = inner primary
        '  <circle cx="215" cy="300" r="128" fill="none" stroke="#0A1730" stroke-width="1.8" '
        'stroke-dasharray="7 5"/>',
        '  <circle cx="279" cy="189.2" r="9" fill="#0A1730" stroke="#0A1730" stroke-width="1.5"/>',
        f'  <text x="291" y="180" font-family="{F}" font-size="12" font-weight="bold" '
        'fill="#0A1730">outer companion (m&#8323;, circular orbit)</text>',
        f'  <text x="291" y="197" font-family="{F}" font-size="11" fill="#3A4A66">a_out = 20 a_in in '
        "the run &#8212; drawn not to scale</text>",
        # inner orbit: eccentric gold ellipse with primary at the focus
        '  <ellipse cx="144.5" cy="321.4" rx="92" ry="50" fill="none" stroke="#D4AF37" '
        'stroke-width="2.2" transform="rotate(-24 144.5 321.4)"/>',
        '  <circle cx="215" cy="290" r="12" fill="#D4AF37" stroke="#0A1730" stroke-width="2"/>',
        '  <circle cx="189.5" cy="262.7" r="5.5" fill="#0A1730"/>',
        '  <line x1="183" y1="257" x2="70" y2="205" stroke="#0A1730" stroke-width="0.9" opacity="0.6"/>',
        f'  <text x="30" y="192" font-family="{F}" font-size="11.5" font-weight="bold" '
        'fill="#0A1730">test particle</text>',
        f'  <text x="30" y="208" font-family="{F}" font-size="10.5" fill="#3A4A66">e: 0.001 &#8594; '
        "0.764 each cycle</text>",
        '  <line x1="108" y1="242" x2="200" y2="281" stroke="#0A1730" stroke-width="0.8" opacity="0.6"/>',
        f'  <text x="30" y="234" font-family="{F}" font-size="11.5" font-weight="bold" '
        'fill="#0A1730">inner primary</text>',
        f'  <text x="30" y="250" font-family="{F}" font-size="10.5" fill="#3A4A66">GM_inner = 1, '
        "a_in = 1</text>",
        f'  <text x="30" y="448" font-family="{F}" font-size="11" fill="#3A4A66">gold ellipse: inner '
        "orbit at e_max = 0.7638 (i&#8320; = 60&#176;)</text>",
        # ---- right panel: inclination ledger ----------------------------------
        f'  <text x="500" y="96" font-family="{F}" font-size="14" font-weight="bold" '
        'fill="#0A1730">Inclination &#8596; eccentricity ledger</text>',
        # outer angular momentum h3 (vertical)
        '  <line x1="800" y1="380" x2="800" y2="130" stroke="#0A1730" stroke-width="2" '
        'marker-end="url(#arrN)"/>',
        f'  <text x="812" y="140" font-family="{F}" font-size="12" font-weight="bold" '
        'fill="#0A1730">h&#8323; (outer orbit)</text>',
        # inner angular momentum h (tilted 60 deg from h3), length 200
        '  <line x1="800" y1="380" x2="626.8" y2="280" stroke="#D4AF37" stroke-width="2.4" '
        'marker-end="url(#arrG)"/>',
        f'  <text x="614" y="272" font-family="{F}" font-size="12.5" font-weight="bold" '
        'fill="#0A1730" text-anchor="end">h (inner orbit)</text>',
        f'  <text x="614" y="288" font-family="{F}" font-size="11.5" fill="#3A4A66" '
        'text-anchor="end">tilted by i&#8320; = 60&#176;</text>',
        # arc between h3 and h (radius 110 about the origin)
        '  <path d="M 800 270 A 110 110 0 0 0 704.7 325" fill="none" stroke="#0A1730" '
        'stroke-width="1.5"/>',
        f'  <text x="812" y="330" font-family="{F}" font-size="12" fill="#0A1730">i&#8320; = '
        "60&#176; &gt; i_crit</text>",
        # critical (Kozai) angle at 39.2315 deg from vertical, length 240
        '  <line x1="800" y1="380" x2="648.1" y2="194.1" stroke="#C44E52" stroke-width="1.4" '
        'stroke-dasharray="5 4"/>',
        f'  <text x="640" y="160" font-family="{F}" font-size="12" fill="#C44E52" '
        'text-anchor="end">i_crit = arccos&#8730;(3/5) = 39.23&#176;</text>',
        f'  <text x="640" y="176" font-family="{F}" font-size="11" fill="#C44E52" '
        'text-anchor="end">(Kozai angle &#8212; exchange threshold)</text>',
        # invariant box (bottom middle-right)
        '  <rect x="500" y="402" width="230" height="96" rx="6" fill="#FFFFFF" '
        'stroke="#0A1730" stroke-width="1.6"/>',
        f'  <text x="514" y="424" font-family="{F}" font-size="12.5" font-weight="bold" '
        'fill="#0A1730">Conserved (quadrupole, test particle):</text>',
        f'  <text x="514" y="446" font-family="{F}" font-size="12" fill="#0A1730">j_z = '
        "&#8730;(1&#8722;e&#178;)&#183;cos i = 0.5</text>",
        f'  <text x="514" y="466" font-family="{F}" font-size="12" fill="#0A1730">at e_max: cos i = '
        "&#8730;(3/5) &#8594; i = i_crit</text>",
        f'  <text x="514" y="486" font-family="{F}" font-size="12" fill="#3A4A66">e_max = '
        "&#8730;(1 &#8722; (5/3)&#183;cos&#178;i&#8320;)</text>",
        # exchange arrows (between the two verticals)
        '  <line x1="770" y1="488" x2="770" y2="418" stroke="#D4AF37" stroke-width="3" '
        'marker-end="url(#arrG)"/>',
        '  <line x1="880" y1="418" x2="880" y2="488" stroke="#0A1730" stroke-width="3" '
        'marker-end="url(#arrN)"/>',
        f'  <text x="825" y="444" font-family="{F}" font-size="12.5" font-weight="bold" '
        'fill="#0A1730" text-anchor="middle">e &#8593; &#183; i &#8595;</text>',
        f'  <text x="825" y="464" font-family="{F}" font-size="11.5" fill="#0A1730" '
        'text-anchor="middle">0.001 &#8594; 0.764</text>',
        f'  <text x="825" y="482" font-family="{F}" font-size="11.5" fill="#0A1730" '
        'text-anchor="middle">60&#176; &#8594; 39.2&#176;</text>',
        # footer
        f'  <text x="30" y="512" font-family="{F}" font-size="10.5" fill="#6B7A94">TRIVORTEX '
        "Research Program &#183; study TRX-10 &#183; Kozai&#8211;Lidov oscillations in hierarchical "
        "triples</text>",
        f'  <text x="30" y="528" font-family="{F}" font-size="10.5" fill="#6B7A94">Laser link: laser '
        "ranging of triple asteroids; LISA-type interferometry of compact-object triples</text>",
        "</svg>",
    ]
    Path(path).write_text("\n".join(s), encoding="utf-8")


def kl_period(ts, e_t):
    """Mean spacing of successive local maxima of e above 0.7*max."""
    emax = float(np.max(e_t))
    idx = [
        i
        for i in range(1, e_t.size - 1)
        if e_t[i] >= e_t[i - 1] and e_t[i] >= e_t[i + 1] and e_t[i] > 0.7 * emax
    ]
    if len(idx) < 2:
        return float("nan")
    return float(np.mean(np.diff(ts[idx])))


# ---------------------------------------------------------------------------
# Canonical PNG panels (--figures mode)
# ---------------------------------------------------------------------------


def render_figures(results, smoke, figdir):
    """Render the scheme SVG and the four canonical PNG panels into figures/.

    Reuses the secular runs already computed in main() (e(t), omega(t), j_z)
    and adds three data products: the e_max(i0) validation sweep, the KL-period
    versus perturber-mass sweep, and the Hamiltonian-drift diagnostic.
    Returns the "figures" block for the JSON protocol.
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

    # ---- data reused from main() -------------------------------------------
    e60, ref60, ts60, et60, wt60, jz60 = results[60.0]
    e70, ref70, ts70, et70, wt70, jz70 = results[70.0]
    it60 = np.degrees(np.arccos(np.clip(jz60 / np.sqrt(1.0 - et60**2), -1.0, 1.0)))
    imax60 = float(
        np.degrees(np.arccos(jz60 / np.sqrt(1.0 - ref60**2)))
    )  # inclination at e_max (== i_crit)

    # ================= fig01 — landscape / geometry ==========================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle("TRX-10 · Kozai–Lidov oscillations — landscape", fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    th = np.linspace(0.0, 2.0 * np.pi, 720)
    e_ell = ref60
    p_ell = 1.0 - e_ell**2
    r_ell = p_ell / (1.0 + e_ell * np.cos(th))
    xo, yo = r_ell * np.cos(th), r_ell * np.sin(th)
    w0, ci = np.pi / 2, np.cos(np.radians(60.0))
    x2 = xo * np.cos(w0) - yo * np.sin(w0)
    y2 = xo * np.sin(w0) + yo * np.cos(w0)
    ax1.plot([-3.1, 3.1], [0.0, 0.0], color=NAVY, lw=1.0, ls=":", alpha=0.6)
    ax1.plot(x2, y2 * ci, color=GOLD, lw=2.2, label="inner orbit at $e_{max}$ (projected)")
    ax1.plot(0.0, 0.0, "o", ms=11, color=GOLD, mec=NAVY, label="inner primary ($GM_{in}=1$)")
    ax1.plot(x2[0], y2[0] * ci, "o", ms=6, color=NAVY)
    ax1.annotate(
        "pericentre", (x2[0], y2[0] * ci), textcoords="offset points", xytext=(8, -14), fontsize=9
    )
    ax1.plot(x2[360], y2[360] * ci, "o", ms=6, color=NAVY)
    ax1.annotate(
        "apastron", (x2[360], y2[360] * ci), textcoords="offset points", xytext=(8, 6), fontsize=9
    )
    circ = np.linspace(0.0, 2.0 * np.pi, 360)
    ax1.plot(
        2.6 * np.cos(circ),
        2.6 * np.sin(circ),
        color=NAVY,
        lw=1.6,
        ls="--",
        label="outer companion orbit, $a_{out}=20\\,a_{in}$ (not to scale)",
    )
    ang = np.radians(47.0)
    ax1.plot(2.6 * np.cos(ang), 2.6 * np.sin(ang), "o", ms=9, color=NAVY)
    ax1.annotate(
        "outer companion $m_3$",
        (2.6 * np.cos(ang), 2.6 * np.sin(ang)),
        textcoords="offset points",
        xytext=(10, 6),
        fontsize=10,
    )
    ax1.set_xlim(-3.1, 3.1)
    ax1.set_ylim(-2.1, 3.1)
    ax1.set_aspect("equal")
    ax1.set_xlabel("x [$a_{in}$] (reference plane = outer orbit)")
    ax1.set_ylabel("projected y [$a_{in}$]")
    ax1.set_title("(a) Hierarchical triple, $i_0=60°$, $\\omega_0=90°$")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="upper left", fontsize=9)

    i_dense = np.linspace(np.radians(I_CRIT_DEG), np.pi / 2, 400)
    ax2.plot(
        np.degrees(i_dense),
        np.sqrt(np.clip(1.0 - (5.0 / 3.0) * np.cos(i_dense) ** 2, 0.0, None)),
        color=GOLD,
        lw=2.4,
        label=r"$e_{max}=\sqrt{1-\frac{5}{3}\cos^2 i_0}$",
    )
    ax2.axvspan(28.0, I_CRIT_DEG, color="0.92", zorder=0)
    ax2.text(33.6, 0.55, "no KL exchange\nbelow $i_{crit}$", ha="center", fontsize=10, color="0.35")
    ax2.axvline(
        I_CRIT_DEG,
        color=red,
        lw=1.6,
        ls="--",
        label=f"$i_{{crit}}$ = {I_CRIT_DEG:.2f}° (Kozai angle)",
    )
    ax2.plot(
        [60.0, 70.0],
        [ref60, ref70],
        "o",
        ms=9,
        color=NAVY,
        mfc=GOLD,
        lw=0,
        label="this study: 60°, 70°",
    )
    ax2.annotate(
        f"0.7638",
        (60.0, ref60),
        textcoords="offset points",
        xytext=(-44, -4),
        fontsize=10,
        fontweight="bold",
    )
    ax2.annotate(
        f"0.8972",
        (70.0, ref70),
        textcoords="offset points",
        xytext=(-46, -4),
        fontsize=10,
        fontweight="bold",
    )
    ax2.set_xlim(28.0, 92.0)
    ax2.set_ylim(0.0, 1.02)
    ax2.set_xlabel("initial inclination $i_0$ [deg]")
    ax2.set_ylabel("maximum eccentricity $e_{max}$")
    ax2.set_title("(b) Kozai landscape (initially circular orbit)")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="lower right", fontsize=9)
    fig.savefig(figdir / "fig01_kl_landscape.png")
    plt.close(fig)

    # ================= fig02 — headline: e–i exchange ========================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(
        "TRX-10 · Headline result — eccentricity–inclination exchange",
        fontsize=16,
        fontweight="bold",
    )
    ax1, ax2 = fig.subplots(1, 2)

    ax1.plot(ts60, et60, color=GOLD, lw=1.8, label="$i_0=60°$")
    ax1.plot(ts70, et70, color=blue, lw=1.8, label="$i_0=70°$")
    ax1.axhline(ref60, color=GOLD, lw=1.2, ls="--")
    ax1.axhline(ref70, color=blue, lw=1.2, ls="--")
    ax1.text(
        ts60[-1] * 0.985,
        ref60 + 0.015,
        f"analytic {ref60:.6f}",
        ha="right",
        fontsize=9,
        color="0.25",
    )
    ax1.text(
        ts60[-1] * 0.985,
        ref70 + 0.015,
        f"analytic {ref70:.6f}",
        ha="right",
        fontsize=9,
        color="0.25",
    )
    ax1.set_xlabel("time [1/$n_{in}$]  ($n_{in}$ = 1: inner mean motion)")
    ax1.set_ylabel("eccentricity e")
    ax1.set_title("(a) KL eccentricity cycles (secular spline flow)")
    ax1.grid(True, alpha=0.3)
    h1, l1 = ax1.get_legend_handles_labels()
    fig.legend(h1, l1, loc="outside right upper", fontsize=10)
    ax1.text(
        0.02,
        0.965,
        f"$j_z=\\sqrt{{1-e^2}}\\,\\cos i$: {jz60:.6f} (60°), {jz70:.6f} (70°) — conserved",
        transform=ax1.transAxes,
        va="top",
        fontsize=9.5,
        bbox=dict(boxstyle="round", fc="white", ec=NAVY, lw=0.8, alpha=0.9),
    )

    peaks = [
        i
        for i in range(1, et60.size - 1)
        if et60[i] >= et60[i - 1] and et60[i] >= et60[i + 1] and et60[i] > 0.7 * e60
    ]
    lo, hi = (peaks[1], peaks[3]) if len(peaks) >= 4 else (0, et60.size - 1)
    ax2.plot(ts60[lo : hi + 1], et60[lo : hi + 1], color=GOLD, lw=2.2, label="eccentricity e")
    ax2.set_xlabel("time [1/$n_{in}$]")
    ax2.set_ylabel("eccentricity e", color=GOLD)
    ax2.tick_params(axis="y", colors=GOLD)
    ax2.set_ylim(0.0, 0.92)
    ax2.grid(True, alpha=0.3)
    ax2b = ax2.twinx()
    ax2b.plot(ts60[lo : hi + 1], it60[lo : hi + 1], color=blue, lw=2.2, label="inclination i")
    ax2b.axhline(I_CRIT_DEG, color=red, lw=1.4, ls="--")
    ax2b.text(ts60[lo], I_CRIT_DEG + 1.2, "$i_{crit}$ = 39.23°", fontsize=9, color=red)
    ax2b.set_ylabel("inclination i [deg]", color=blue)
    ax2b.tick_params(axis="y", colors=blue)
    ax2b.set_ylim(30.0, 68.0)
    ax2b.invert_yaxis()
    ax2.set_title("(b) The exchange: e peaks exactly as i dips to $i_{crit}$")
    h1, l1 = ax2.get_legend_handles_labels()
    h2, l2 = ax2b.get_legend_handles_labels()
    ax2.legend(h1 + h2, l1 + l2, loc="upper right", fontsize=9)
    fig.savefig(figdir / "fig02_kl_exchange.png")
    plt.close(fig)

    # ================= fig03 — parameter sweeps ==============================
    i0_sweep = (
        [30.0, 35.0, 40.0, 50.0, 60.0, 70.0, 80.0]
        if smoke
        else [30.0, 35.0, 38.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0]
    )
    nc_sweep = {40.0: 8}
    sim, ana = [], []
    for i0 in i0_sweep:
        ts_s, e_s, w_s, jz_s, _ = run_kl(
            0.001,
            i0,
            n_cycles=nc_sweep.get(i0, 2),
            n_out=800 if smoke else 2000,
            fast=(smoke or i0 <= 38.0),
        )
        sim.append(float(np.max(e_s)))
        ana.append(
            float(np.sqrt(1.0 - (5.0 / 3.0) * np.cos(np.radians(i0)) ** 2))
            if i0 > I_CRIT_DEG
            else 0.0
        )
    sim, ana = np.array(sim), np.array(ana)
    active = np.array(i0_sweep) > I_CRIT_DEG
    dev_active = float(np.max(np.abs(sim[active] - ana[active])))

    m3_list = [0.5, 1.0, 2.0, 4.0]
    P_list = []
    for m3 in m3_list:
        ts_m, e_m, w_m, jz_m, _ = run_kl(
            0.001, 60.0, m3_ratio=m3, n_cycles=1, n_out=800 if smoke else 2000, fast=True
        )
        P_list.append(kl_period(ts_m, e_m))
    P_list = np.array(P_list)
    Pm = P_list * np.array(m3_list)
    pm_spread_pct = float(100.0 * (Pm.max() - Pm.min()) / Pm.mean())

    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(
        "TRX-10 · Parameter sweeps — e_max(i₀) validation and KL clock scaling",
        fontsize=16,
        fontweight="bold",
    )
    ax1, ax2 = fig.subplots(1, 2)

    ax1.plot(
        np.array(i0_sweep)[active],
        ana[active],
        color=NAVY,
        lw=2.0,
        label=r"analytic $\sqrt{1-\frac{5}{3}\cos^2 i_0}$",
    )
    ax1.plot(
        np.array(i0_sweep)[active],
        sim[active],
        "o",
        ms=7,
        mfc=GOLD,
        mec=NAVY,
        label="secular spline flow (this run)",
    )
    ax1.plot(
        np.array(i0_sweep)[~active],
        sim[~active],
        "s",
        ms=7,
        color="0.55",
        label=f"below $i_{{crit}}$: e stays at $e_0$ = 0.001",
    )
    ax1.axvline(I_CRIT_DEG, color=red, lw=1.4, ls="--")
    ax1.text(I_CRIT_DEG + 0.8, 0.06, "$i_{crit}$", color=red, fontsize=10)
    ax1.set_xlabel("initial inclination $i_0$ [deg]")
    ax1.set_ylabel("$e_{max}$ (simulated)")
    ax1.set_ylim(-0.03, 1.03)
    ax1.set_title(f"(a) Sweep validation: max |sim − analytic| = {dev_active:.1e}")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="upper left", fontsize=9)

    ax2.loglog(m3_list, P_list, "o", ms=8, mfc=GOLD, mec=NAVY, label="measured KL period")
    ref_P = P_list[list(m3_list).index(1.0)] / np.array(m3_list)
    ax2.loglog(
        m3_list, ref_P, "--", color=NAVY, lw=1.8, label=r"$P\propto 1/m_3$ (anchor at $m_3/M=1$)"
    )
    ax2.set_xlabel("perturber mass ratio $m_3/M$")
    ax2.set_ylabel("KL period [1/$n_{in}$]")
    ax2.set_title(f"(b) KL clock vs perturber mass: $P\\,m_3$ spread {pm_spread_pct:.1f}%")
    ax2.grid(True, alpha=0.3, which="both")
    ax2.legend(loc="upper right", fontsize=9)
    for m3, P in zip(m3_list, P_list):
        ax2.annotate(f"{P:.0f}", (m3, P), textcoords="offset points", xytext=(8, 6), fontsize=9)
    fig.savefig(figdir / "fig03_kl_sweeps.png")
    plt.close(fig)

    # ================= fig04 — dynamics: phase portrait + invariant ==========
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(
        "TRX-10 · Dynamics on the j_z manifold — phase portrait and invariant",
        fontsize=16,
        fontweight="bold",
    )
    ax1, ax2 = fig.subplots(1, 2)

    ax1.plot(wt60 % np.pi, et60, color=GOLD, lw=1.4, label=f"$i_0=60°$ ($j_z$={jz60:.6f})")
    ax1.plot(wt70 % np.pi, et70, color=blue, lw=1.4, label=f"$i_0=70°$ ($j_z$={jz70:.6f})")
    ax1.axhline(ref60, color=GOLD, lw=1.1, ls="--")
    ax1.axhline(ref70, color=blue, lw=1.1, ls="--")
    ax1.axvline(np.pi / 2, color="0.6", lw=1.0, ls=":")
    ax1.text(np.pi / 2 + 0.03, 0.06, "$\\omega=\\pi/2$", fontsize=9, color="0.4")
    ax1.set_xlim(0.0, np.pi)
    ax1.set_ylim(0.0, 1.0)
    ax1.set_xlabel("argument of pericentre $\\omega$ (mod $\\pi$) [rad]")
    ax1.set_ylabel("eccentricity e")
    ax1.set_title("(a) Phase portrait: $\\omega$ librates about $\\pi/2$")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="upper left", fontsize=9)

    Hf, dHf_de, dHf_dw = build_averager(
        jz60, a_out=20.0, n_e=40 if smoke else 160, n_w=45 if smoke else 180
    )
    H_t = np.array([Hf(min(max(e, 1e-4), 0.999), w % np.pi) for e, w in zip(et60, wt60)])
    hdrift = float(np.max(np.abs(H_t - H_t[0])))
    ax2.semilogy(ts60, np.abs(H_t - H_t[0]) + 1e-18, color=GOLD, lw=1.6)
    ax2.set_xlabel("time [1/$n_{in}$]")
    ax2.set_ylabel("|ΔH| along the flow [scaled units]")
    ax2.set_title(f"(b) Spline-Hamiltonian residual: max {hdrift:.1e}")
    ax2.grid(True, alpha=0.3, which="both")
    fig.savefig(figdir / "fig04_kl_dynamics.png")
    plt.close(fig)

    # ================= scheme SVG ============================================
    make_scheme_svg(figdir / "scheme_trx10.svg")

    # ================= JSON figures block ====================================
    return {
        "mode": "smoke" if smoke else "full",
        "scheme": {
            "file": "figures/scheme_trx10.svg",
            "caption": (
                "Hand-authored schematic of the Kozai–Lidov exchange: a distant "
                "inclined companion (m3, a_out = 20 a_in, circular) perturbs an "
                "inner test-particle orbit tilted by i0 = 60 deg; eccentricity "
                "grows from 0.001 to e_max = 0.764 while the inclination dips "
                "exactly to the Kozai angle i_crit = arccos(sqrt(3/5)) = 39.23 deg, "
                "with j_z = sqrt(1 - e^2) cos i conserved."
            ),
        },
        "panels": [
            {
                "file": "figures/fig01_kl_landscape.png",
                "caption": (
                    "Landscape of the quadrupole KL problem: (a) geometry of the "
                    "hierarchical triple - inner orbit at e_max = 0.7638 inclined by "
                    "i0 = 60 deg and projected on the outer-orbit plane, with the "
                    "distant companion on its circular orbit a_out = 20 a_in (not to "
                    "scale); (b) analytic Kozai landscape e_max(i0) = "
                    "sqrt(1 - (5/3) cos^2 i0) with the critical inclination 39.23 deg "
                    "and the study points 60 deg (0.7638) and 70 deg (0.8972)."
                ),
            },
            {
                "file": "figures/fig02_kl_exchange.png",
                "caption": (
                    "Headline result - the eccentricity-inclination exchange from the "
                    f"secular spline flow: (a) e(t) cycles at i0 = 60 deg (e_max = "
                    f"{e60:.6f}) and 70 deg (e_max = {e70:.6f}) against the analytic "
                    f"curves, with conserved j_z = {jz60:.6f} / {jz70:.6f}; (b) zoom "
                    "on two cycles at 60 deg showing e peaking exactly when i dips "
                    f"to {imax60:.2f} deg = i_crit (antiphase exchange)."
                ),
            },
            {
                "file": "figures/fig03_kl_sweeps.png",
                "caption": (
                    f"Parameter sweeps: (a) e_max(i0) over {len(i0_sweep)} inclinations "
                    "from 30 to "
                    f"80 deg - below i_crit eccentricity stays at e0 = 0.001, above it "
                    f"the spline flow matches the analytic curve to {dev_active:.1e} "
                    "(40 deg needs an 8x longer span: the KL period diverges at "
                    f"i_crit); (b) KL period versus perturber mass ratio m3/M in "
                    "{0.5, 1, 2, 4} - P proportional to 1/m3, P*m3 spread "
                    f"{pm_spread_pct:.1f}% (period halves when m3 doubles)."
                ),
            },
            {
                "file": "figures/fig04_kl_dynamics.png",
                "caption": (
                    "Dynamics on the fixed-j_z manifold: (a) phase portrait (omega mod "
                    "pi, e) for i0 = 60/70 deg - the argument of pericentre librates "
                    "about pi/2 while e cycles between 0.001 and e_max; (b) residual "
                    f"of the tabulated Hamiltonian H(e, omega) along the i0 = 60 deg "
                    f"trajectory, max |dH| = {hdrift:.1e} over the run - the residual "
                    "reflects the cubic-spline representation of the orbit average "
                    "(grid 160 x 180), not integrator error (DOP853, rtol 1e-8)."
                ),
            },
        ],
        "data": {
            "preset": {
                "e0": 0.001,
                "omega0_deg": 90.0,
                "i0_deg": [60.0, 70.0],
                "m3_ratio": 1.0,
                "a_out": 20.0,
                "secular_grid_e_x_omega": [160, 180],
            },
            "jz_values": {"i0_60": jz60, "i0_70": jz70},
            "inclination_at_emax_deg": imax60,
            "e_max_sweep": {
                "i0_deg": [float(x) for x in i0_sweep],
                "e_max_simulated": [round(v, 8) for v in sim.tolist()],
                "e_max_analytic": [round(v, 8) for v in ana.tolist()],
                "max_abs_dev_active": float(f"{dev_active:.3e}"),
                "note": "i0 = 40 deg run with an 8x longer span (period diverges at i_crit)",
            },
            "m3_period_sweep": {
                "m3_ratio": m3_list,
                "kl_period": [float(f"{P:.6e}") for P in P_list.tolist()],
                "P_times_m3": [float(f"{v:.6e}") for v in Pm.tolist()],
                "pm3_spread_pct": round(pm_spread_pct, 3),
            },
            "hamiltonian_drift": float(f"{hdrift:.3e}"),
        },
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="TRX-10 Kozai-Lidov")
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

    e0 = 0.001
    results = {}
    for i0 in (60.0, 70.0):
        ts, e_t, w_t, j_z, _ = run_kl(e0, i0, m3_ratio=1.0, n_cycles=1 if smoke else 3, fast=smoke)
        e_max = float(np.max(e_t))
        ref = np.sqrt(1.0 - (5.0 / 3.0) * np.cos(np.radians(i0)) ** 2)
        results[i0] = (e_max, ref, ts, e_t, w_t, j_z)
        add(
            f"e_max_i0_{int(i0)}",
            e_max,
            ref,
            2e-3,
            "ecc",
            f"analytic sqrt(1-(5/3)cos^2 i0) = {ref:.6f}",
        )

    ts1, e1, _, _, _ = run_kl(e0, 60.0, m3_ratio=1.0, n_cycles=1 if smoke else 3, fast=smoke)
    ts2, e2, _, _, _ = run_kl(e0, 60.0, m3_ratio=2.0, n_cycles=1 if smoke else 3, fast=smoke)
    P1, P2 = kl_period(ts1, e1), kl_period(ts2, e2)
    add(
        "kl_period_halves_with_m3",
        P2 / P1,
        0.5,
        0.03,
        "ratio",
        f"P(m3) = {P1:.2f}, P(2 m3) = {P2:.2f} (period ~ 1/C2 ~ 1/m3)",
    )

    ref60 = results[60.0][1]
    if not smoke:
        e_direct = direct_kl_emax(60.0, m3_ratio=0.5, a_out=5.0, t_out_periods=200)
        add(
            "direct_3d_emax_validation",
            1.0 if abs(e_direct - ref60) < 0.08 else 0.0,
            1.0,
            1e-12,
            "bool",
            f"direct restricted 3-body smoothed e_max = {e_direct:.4f} vs {ref60:.4f}",
        )

    out = Path(__file__).resolve().parents[1] / "results"
    out.mkdir(exist_ok=True)
    ts60, e60 = results[60.0][2], results[60.0][3]
    make_svg(ts60, e60, out / "trx10_plot.svg")

    # --- canonical figures (--figures, additive) -----------------------------
    figures_block = None
    figdir = Path(__file__).resolve().parents[1] / "figures"
    if args.figures:
        figures_block = render_figures(results, smoke, figdir)

    all_pass = all(c["pass"] for c in CHECKS)
    stride = max(1, ts60.size // 500)
    protocol = {
        "study": "TRX-10",
        "title": "Kozai-Lidov oscillations in hierarchical triples",
        "status": "PASS" if all_pass else "FAIL",
        "smoke": bool(smoke),
        "runtime_s": round(time.time() - t0, 3),
        "checks": CHECKS,
        "series": {"t": ts60[::stride].round(4).tolist(), "e": e60[::stride].round(8).tolist()},
        "meta": {
            "equations": [
                "double-averaged quadrupole Hamiltonian (numerical orbit average, spline flow)",
                "e_max = sqrt(1-(5/3)cos^2 i0) ; j_z = sqrt(1-e^2) cos i = const",
                "t_KL ~ (1/C2) ~ (m_tot/m3)(a_out/a_in)^3 P_in^2",
            ],
            "e_max_60": results[60.0][0],
            "e_max_70": results[70.0][0],
            "e_max_direct": e_direct if not smoke else None,
            "laser_link": "laser ranging of triple asteroids; LISA-type laser "
            "interferometry of compact-object triples",
        },
    }
    if figures_block is not None:
        protocol["figures"] = figures_block
    (out / "trx10_results.json").write_text(json.dumps(protocol, indent=2), encoding="utf-8")

    print(f"\nTRX-10 — Kozai-Lidov oscillations  [{'SMOKE' if smoke else 'FULL'}]")
    for c in CHECKS:
        flag = "PASS" if c["pass"] else "FAIL"
        print(
            f"  [{flag}] {c['name']:<42} value={c['value']:.6e} target={c['target']:.1e} tol={c['tol']:.1e}"
        )
    print(f"  status: {protocol['status']}   runtime: {protocol['runtime_s']} s")
    if figures_block is not None:
        print("  figures: 5 files written to figures/:")
        for entry in [figures_block["scheme"]] + figures_block["panels"]:
            print(f"    {entry['file']}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
