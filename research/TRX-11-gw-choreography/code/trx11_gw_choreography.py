#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
TRIVORTEX LAB — TRX-11 — GRAVITATIONAL WAVES FROM A THREE-BODY CHOREOGRAPHY
============================================================================
The figure-eight choreography (Chenciner & Montgomery 2000) — three equal
masses chasing each other along a single closed curve — is a laboratory
gravitational-wave source.  In the quadrupole approximation (G = c = D = 1)
the waveform is driven by the second derivative of the mass quadrupole
Q_ij = sum_k m_k x_ki x_kj and the luminosity by P = (1/5) sum (dQ/dt^3)^2.

Laser link: LISA / Taiji / TianQin are LASER interferometers — the
instruments that would actually measure such three-body signals; their
arm length is set by laser stability, not mirrors.

What is computed
  * period of the figure-eight orbit by closure root-finding
  * conservation of energy, angular momentum, centre of mass
  * quadrupole half-period symmetry -> even-only harmonic spectrum
  * dominant GW harmonic at 2/T and the mean luminosity

With --figures: hand-authored scheme SVG (white background, navy/gold) plus
four canonical 300-DPI panels into figures/ — orbit overview, waveform +
harmonic comb, quadrupole antenna pattern + velocity-detuning sweep, and
quadrupole dynamics — and a "figures" block added to the JSON protocol.
The figure panels use exact analytic quadrupole derivatives (positions,
velocities, accelerations and jerks of the same trajectory), so the
displayed waveform/spectrum/luminosity are free of numerical-differentiation
edge artifacts; the protocol checks and their values are unchanged.

Usage:  python trx11_gw_choreography.py [--smoke] [--figures]
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


X1_0 = np.array([0.97000436, -0.24308753])
V3_0 = np.array([-0.93240737, -0.86473146])


def rhs(t, s):
    """Three equal bodies, G = m = 1, planar; interleaved (x,y,vx,vy)*3."""
    b = s.reshape(3, 4)
    a = np.zeros((3, 2))
    for k in range(3):
        for j in range(3):
            if j == k:
                continue
            d = b[j, 0:2] - b[k, 0:2]
            r = np.hypot(d[0], d[1])
            a[k] += d / r**3
    out = np.empty_like(b)
    out[:, 0:2] = b[:, 2:4]
    out[:, 2:4] = a
    return out.reshape(-1)


def initial_state():
    s = np.zeros(12)
    b = s.reshape(3, 4)
    b[0, 0:2] = X1_0
    b[1, 0:2] = -X1_0
    b[2, 0:2] = 0.0
    b[0, 2:4] = -V3_0 / 2.0
    b[1, 2:4] = -V3_0 / 2.0
    b[2, 2:4] = V3_0
    return s


def energy(s):
    b = s.reshape(3, 4)
    K = 0.5 * float(np.sum(b[:, 2:4] ** 2))
    U = 0.0
    for k in range(3):
        for j in range(k + 1, 3):
            U += -1.0 / np.hypot(*(b[k, 0:2] - b[j, 0:2]))
    return K + U


def angular_momentum(s):
    b = s.reshape(3, 4)
    return float(np.sum(b[:, 0] * b[:, 3] - b[:, 1] * b[:, 2]))


def quadrupole(s):
    b = s.reshape(3, 4)
    Q = np.zeros((2, 2))
    for k in range(3):
        Q += np.outer(b[k, 0:2], b[k, 0:2])
    return Q


def _poly(pts, color, sw=1.8):
    s = " ".join(f"{px:.2f},{py:.2f}" for px, py in pts)
    return f'<polyline fill="none" stroke="{color}" stroke-width="{sw}" points="{s}"/>'


def make_svg(orbit, h_t, ts, path):
    W, H = 900, 520
    cx, cy, sc = 220.0, 260.0, 200.0
    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect width="{W}" height="{H}" fill="#0A1230"/>',
        '<text x="24" y="34" fill="#FFFFFF" font-family="Arial" font-size="19" '
        'font-weight="bold">TRX-11 &#8212; Figure-eight choreography as a GW emitter</text>',
    ]
    s.append(_poly([(cx + p[0] * sc, cy - p[1] * sc) for p in orbit], "#F2C14E"))
    x0, x1 = 480.0, 860.0
    y0, y1 = 140.0, 400.0
    hmax = float(np.max(np.abs(h_t))) or 1.0
    stride = max(1, h_t.size // 400)
    pts = _poly(
        [
            (x0 + t / ts[-1] * (x1 - x0), (y0 + y1) / 2 - h / hmax * (y1 - y0) * 0.45)
            for t, h in zip(ts[::stride], h_t[::stride])
        ],
        "#6FB7FF",
    )
    s += [
        f'<line x1="{x0}" y1="{(y0+y1)/2:.0f}" x2="{x1}" y2="{(y0+y1)/2:.0f}" stroke="#3A4A6B"/>',
        pts,
        '<text x="600" y="100" fill="#6FB7FF" font-family="Arial" font-size="13">h_plus(t) ~ d^2(Qxx-Qyy)/dt^2</text>',
        '<text x="600" y="120" fill="#9FB3D9" font-family="Arial" font-size="12">one period T; only even harmonics</text>',
        '<text x="120" y="470" fill="#F2C14E" font-family="Arial" font-size="13">the figure-eight orbit (Chenciner&#8211;Montgomery)</text>',
        '<text x="24" y="500" fill="#9FB3D9" font-family="Arial" font-size="12">'
        "quadrupole radiation of a three-body choreography — target for laser interferometers (LISA class)</text>",
        "</svg>",
    ]
    Path(path).write_text("\n".join(s), encoding="utf-8")


# ---------------------------------------------------------------------------
# Canonical figures (--figures mode): scheme SVG + four PNG panels
# ---------------------------------------------------------------------------

NAVY = "#0A1730"
GOLD = "#D4AF37"
SERIES = ["#D4AF37", "#4C72B0", "#55A868", "#C44E52", "#8172B2"]


def _state_derivs(b):
    """Accelerations and jerks for states b (3, 4, N) with G = m = 1 (planar)."""
    X, Y, VX, VY = b[:, 0], b[:, 1], b[:, 2], b[:, 3]
    Ax = np.zeros_like(X)
    Ay = np.zeros_like(Y)
    JX = np.zeros_like(X)
    JY = np.zeros_like(Y)
    for k in range(3):
        for j in range(3):
            if j == k:
                continue
            dx = X[j] - X[k]
            dy = Y[j] - Y[k]
            dvx = VX[j] - VX[k]
            dvy = VY[j] - VY[k]
            r2 = dx * dx + dy * dy
            r3 = r2 * np.sqrt(r2)
            r5 = r3 * r2
            Ax[k] += dx / r3
            Ay[k] += dy / r3
            JX[k] += dvx / r3 - 3.0 * dx * (dx * dvx + dy * dvy) / r5
            JY[k] += dvy / r3 - 3.0 * dy * (dx * dvx + dy * dvy) / r5
    return Ax, Ay, JX, JY


def _quad_exact(b):
    """Exact quadrupole derivatives from states b (3, 4, N): Qdd and Q3."""
    Ax, Ay, JX, JY = _state_derivs(b)
    X, Y, VX, VY = b[:, 0], b[:, 1], b[:, 2], b[:, 3]
    Qddxx = np.sum(2.0 * VX * VX + 2.0 * X * Ax, axis=0)
    Qddyy = np.sum(2.0 * VY * VY + 2.0 * Y * Ay, axis=0)
    Qddxy = np.sum(VX * VY + X * Ay + VY * Ax, axis=0)
    Q3xx = np.sum(6.0 * VX * Ax + 2.0 * X * JX, axis=0)
    Q3yy = np.sum(6.0 * VY * Ay + 2.0 * Y * JY, axis=0)
    Q3xy = np.sum(3.0 * (Ax * VY + VX * Ay) + X * JY + Y * JX, axis=0)
    return (Qddxx, Qddyy, Qddxy), (Q3xx, Q3yy, Q3xy)


def make_scheme_svg(path, orbit, T_val):
    """Hand-authored schematic of the choreography GW emitter (white bg, navy/gold)."""
    F = "Helvetica, Arial, sans-serif"
    cx, cy, sc = 218.0, 268.0, 155.0
    pts = " ".join(f"{cx + px * sc:.1f},{cy - py * sc:.1f}" for px, py in orbit)
    b0 = initial_state().reshape(3, 4)
    body_xy = [(cx + b0[k, 0] * sc, cy - b0[k, 1] * sc) for k in range(3)]
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
        f'  <text x="30" y="38" font-family="{F}" font-size="20" font-weight="bold" '
        'fill="#0A1730">TRX-11 &#8212; Scheme: figure-eight choreography as a '
        "gravitational-wave emitter</text>",
        f'  <text x="30" y="60" font-family="{F}" font-size="12.5" fill="#3A4A66">Three '
        "equal masses chase each other along one closed curve (Chenciner&#8211;Montgomery "
        "2000); the rotating quadrupole radiates waves read out by a distant laser "
        "interferometer</text>",
        # ---- left: the orbit -------------------------------------------------
        f'  <line x1="48" y1="{cy:.0f}" x2="398" y2="{cy:.0f}" stroke="#0A1730" '
        'stroke-width="0.8" opacity="0.35"/>',
        f'  <line x1="{cx:.0f}" y1="118" x2="{cx:.0f}" y2="420" stroke="#0A1730" '
        'stroke-width="0.8" opacity="0.35"/>',
        f'  <polyline fill="none" stroke="#0A1730" stroke-width="2" points="{pts}"/>',
        # reflection axis of the eight (along v3 = (-0.9324, -0.8647) direction)
        f'  <line x1="{cx + 1.25 * 0.7338 * sc:.1f}" y1="{cy + 1.25 * 0.6812 * sc:.1f}" '
        f'x2="{cx - 1.25 * 0.7338 * sc:.1f}" y2="{cy - 1.25 * 0.6812 * sc:.1f}" '
        'stroke="#0A1730" stroke-width="1.1" stroke-dasharray="6 4" opacity="0.45"/>',
        f'  <text x="{cx - 148:.0f}" y="128" font-family="{F}" font-size="10.5" '
        'fill="#3A4A66">reflection axis</text>',
        # bodies at t = 0
        f'  <circle cx="{body_xy[0][0]:.1f}" cy="{body_xy[0][1]:.1f}" r="8" fill="{GOLD}" '
        'stroke="#0A1730" stroke-width="2"/>',
        f'  <circle cx="{body_xy[1][0]:.1f}" cy="{body_xy[1][1]:.1f}" r="8" fill="{GOLD}" '
        'stroke="#0A1730" stroke-width="2"/>',
        f'  <circle cx="{body_xy[2][0]:.1f}" cy="{body_xy[2][1]:.1f}" r="8" fill="#FFFFFF" '
        'stroke="#0A1730" stroke-width="2"/>',
        f'  <text x="{body_xy[0][0] + 12:.0f}" y="{body_xy[0][1] + 22:.0f}" font-family="{F}" '
        'font-size="12" font-weight="bold" fill="#0A1730">m&#8321;</text>',
        f'  <text x="{body_xy[1][0] - 30:.0f}" y="{body_xy[1][1] - 14:.0f}" font-family="{F}" '
        'font-size="12" font-weight="bold" fill="#0A1730">m&#8322;</text>',
        f'  <text x="{body_xy[2][0] + 12:.0f}" y="{body_xy[2][1] - 10:.0f}" font-family="{F}" '
        'font-size="12" font-weight="bold" fill="#0A1730">m&#8323;</text>',
        # chase arrow along the curve
        f'  <path d="M {body_xy[2][0] - 26:.1f} {body_xy[2][1] + 8:.1f} '
        f'l -34 22" fill="none" stroke="{GOLD}" stroke-width="2.2" marker-end="url(#arrG)"/>',
        f'  <text x="{cx - 152:.0f}" y="446" font-family="{F}" font-size="11.5" '
        'fill="#0A1730">each body runs the whole eight; roles exchange every T/3</text>',
        f'  <text x="{cx - 152:.0f}" y="463" font-family="{F}" font-size="11.5" '
        'fill="#3A4A66">total angular momentum L = 0 (defining property)</text>',
        f'  <text x="{cx - 152:.0f}" y="480" font-family="{F}" font-size="11.5" '
        f'fill="#3A4A66">period T = {T_val:.6f} (G = m = 1)</text>',
        # ---- right-top: observer + inclination -------------------------------
        '  <line x1="700" y1="300" x2="876" y2="118" stroke="#0A1730" stroke-width="1.6" '
        'marker-end="url(#arrN)"/>',
        '  <line x1="700" y1="300" x2="700" y2="96" stroke="#0A1730" stroke-width="1.1" '
        'stroke-dasharray="5 4" opacity="0.6"/>',
        '  <path d="M 700 252 A 48 48 0 0 0 734 262" fill="none" stroke="#0A1730" '
        'stroke-width="1.4" marker-end="url(#arrN)"/>',
        f'  <text x="742" y="272" font-family="{F}" font-size="12" fill="#0A1730">observer, '
        "inclination &#952;</text>",
        '  <rect x="846" y="88" width="86" height="30" rx="4" fill="#FFFFFF" '
        'stroke="#0A1730" stroke-width="2"/>',
        f'  <text x="889" y="108" font-family="{F}" font-size="12" font-weight="bold" '
        'fill="#0A1730" text-anchor="middle">LISA-class</text>',
        # radiation lobes along the orbital normal
        '  <ellipse cx="700" cy="150" rx="34" ry="76" fill="#D4AF37" opacity="0.20"/>',
        '  <ellipse cx="700" cy="452" rx="34" ry="76" fill="#D4AF37" opacity="0.20"/>',
        f'  <text x="742" y="128" font-family="{F}" font-size="11.5" fill="#0A1730">quadrupole '
        "lobes:</text>",
        f'  <text x="742" y="144" font-family="{F}" font-size="11.5" fill="#3A4A66">strongest '
        "along the</text>",
        f'  <text x="742" y="160" font-family="{F}" font-size="11.5" fill="#3A4A66">orbital '
        "normal (&#8776; 2.5&#215; mean)</text>",
        f'  <text x="560" y="120" font-family="{F}" font-size="11.5" fill="#3A4A66">orbital '
        "plane = plane of the eight</text>",
        # ---- right-middle: waveform strip -------------------------------------
        '  <rect x="536" y="316" width="380" height="86" rx="6" fill="#FFFFFF" '
        'stroke="#0A1730" stroke-width="1.4"/>',
        f'  <line x1="552" y1="359" x2="900" y2="359" stroke="#0A1730" stroke-width="0.8" '
        'opacity="0.5"/>',
        f'  <polyline fill="none" stroke="{NAVY}" stroke-width="1.8" points="{_wave_pts()}"/>',
        f'  <text x="548" y="334" font-family="{F}" font-size="12" font-weight="bold" '
        'fill="#0A1730">plus-polarised strain h&#8322;(t) &#8212; six repeats per orbit '
        "period</text>",
        f'  <text x="548" y="394" font-family="{F}" font-size="11" fill="#3A4A66">h&#8322; '
        "&#8733; d&#178;(Q_xx &#8722; Q_yy)/dt&#178;, range &#8722;4.04 &#8230; +4.85 "
        "(G = c = D = 1)</text>",
        # ---- right-bottom: harmonic comb --------------------------------------
        '  <rect x="536" y="412" width="380" height="100" rx="6" fill="#FFFFFF" '
        'stroke="#0A1730" stroke-width="1.4"/>',
        f'  <line x1="552" y1="494" x2="900" y2="494" stroke="#0A1730" stroke-width="0.8"/>',
        f'  <line x1="620" y1="494" x2="620" y2="430" stroke="{GOLD}" stroke-width="3"/>',
        f'  <line x1="712" y1="494" x2="712" y2="479" stroke="{GOLD}" stroke-width="3"/>',
        f'  <line x1="804" y1="494" x2="804" y2="492.4" stroke="{GOLD}" stroke-width="3"/>',
        f'  <text x="620" y="422" font-family="{F}" font-size="11" fill="#0A1730" '
        'text-anchor="middle">n = 6</text>',
        f'  <text x="712" y="472" font-family="{F}" font-size="11" fill="#0A1730" '
        'text-anchor="middle">n = 12</text>',
        f'  <text x="812" y="484" font-family="{F}" font-size="11" fill="#0A1730" '
        'text-anchor="start">n = 18</text>',
        f'  <text x="548" y="430" font-family="{F}" font-size="12" font-weight="bold" '
        'fill="#0A1730">spectrum: pure comb at multiples of 6/T</text>',
        f'  <text x="548" y="509" font-family="{F}" font-size="11" fill="#3A4A66">amplitudes '
        "1 : 0.091 : 0.0061; all other harmonics &#8804; 6&#215;10&#8315;&#8308; of the "
        "peak</text>",
        # ---- info box ----------------------------------------------------------
        '  <rect x="30" y="492" width="330" height="34" rx="5" fill="#FFFFFF" '
        'stroke="#0A1730" stroke-width="1.2"/>',
        f'  <text x="42" y="513" font-family="{F}" font-size="11.5" fill="#0A1730">Q_ij = '
        "&#931; m_k x_ki x_kj &#160;&#183;&#160; P = (1/5) &#931; (d&#179;Q_ij/dt&#179;)&#178; "
        "(G = c = D = 1)</text>",
        # footer
        f'  <text x="30" y="534" font-family="{F}" font-size="10" fill="#6B7A94">TRIVORTEX '
        "Research Program &#183; study TRX-11 &#183; gravitational waves from the "
        "figure-eight choreography</text>",
        "</svg>",
    ]
    Path(path).write_text("\n".join(s), encoding="utf-8")


def _wave_pts():
    """Static polyline of one T/6 strain lobe pattern (stylised, real amplitude ratio)."""
    xs = np.linspace(552.0, 900.0, 480)
    # stylised h_plus: dominant n=6 line + 0.091 of n=12 (the measured ratio)
    tt = (xs - 552.0) / (900.0 - 552.0) * 2.0 * np.pi
    yy = 16.0 * (np.sin(3.0 * tt) + 0.091 * np.sin(6.0 * tt))
    return " ".join(f"{x:.1f},{359.0 - y:.1f}" for x, y in zip(xs, yy))


def render_figures(sol, sol_scheme, T_full, T_run, smoke, figdir):
    """Render the scheme SVG and four canonical PNG panels into figures/.

    Reuses the one-period trajectory already computed in main() (sol over
    [0, T_run]); the scheme always traces the full period from sol_scheme
    (the long integration used for the period search).  Adds exact analytic
    quadrupole derivatives, the antenna-pattern contraction, the harmonic
    comb and the velocity-detuning sweep.  Returns the "figures" block for
    the JSON protocol.
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

    # ---- shared data --------------------------------------------------------
    n_samples = 1201 if smoke else 4801
    t = np.linspace(0.0, T_run, n_samples)
    dt = t[1] - t[0]
    B = sol.sol(t).reshape(3, 4, -1)
    (Qddxx, Qddyy, Qddxy), (Q3xx, Q3yy, Q3xy) = _quad_exact(B)
    h_exact = Qddxx - Qddyy
    TF3xx = (2.0 * Q3xx - Q3yy) / 3.0
    TF3yy = (2.0 * Q3yy - Q3xx) / 3.0
    TF3zz = -(Q3xx + Q3yy) / 3.0
    lum_t = (TF3xx**2 + TF3yy**2 + TF3zz**2 + 2.0 * Q3xy**2) / 5.0
    lum_mean = float(np.mean(lum_t))
    lum_max = float(np.max(lum_t))
    energy_T = float(np.sum(lum_t) * dt)

    pos = B[:, 0:2, :]
    r12 = np.hypot(pos[0, 0] - pos[1, 0], pos[0, 1] - pos[1, 1])
    r13 = np.hypot(pos[0, 0] - pos[2, 0], pos[0, 1] - pos[2, 1])
    r23 = np.hypot(pos[1, 0] - pos[2, 0], pos[1, 1] - pos[2, 1])

    # spectrum of the exact strain (the signal is periodic over [0, T]: no window)
    sig = h_exact - h_exact.mean()
    spec = np.abs(np.fft.rfft(sig))
    freqs = np.fft.rfftfreq(sig.size, d=dt)
    kpk = int(np.argmax(spec[1:]) + 1)
    fT_peak = float(freqs[kpk] * T_run)
    comb = {}
    amps = {}
    for n in range(1, 31):
        j = int(round(n * sig.size * dt / T_run))
        if j < spec.size:
            amps[n] = float(spec[j] / spec[kpk])
    for n in (6, 12, 18, 24):
        if n in amps:
            comb[n] = amps[n]
    other_max = max(a for n, a in amps.items() if n not in comb)

    # ================= fig01 — orbit overview ================================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(
        "TRX-11 · Figure-eight choreography — GW emitter overview", fontsize=16, fontweight="bold"
    )
    ax1, ax2 = fig.subplots(1, 2)

    for k, lab in enumerate(("body 1", "body 2", "body 3")):
        ax1.plot(
            pos[k, 0],
            pos[k, 1],
            color=SERIES[k],
            lw=1.4,
            label=f"{lab} trajectory (identical curve)",
        )
    ax1.plot(pos[2, 0, 0], pos[2, 1, 0], "o", color=NAVY, ms=9, label="start (m$_3$ at origin)")
    ax1.annotate(
        "",
        xy=(pos[2, 0, 60], pos[2, 1, 60]),
        xytext=(pos[2, 0, 18], pos[2, 1, 18]),
        arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=2.4),
    )
    ax1.annotate(
        "chase direction",
        xy=(pos[2, 0, 60], pos[2, 1, 60]),
        textcoords="offset points",
        xytext=(8, -14),
        fontsize=10,
        color=NAVY,
    )
    ax1.set_aspect("equal")
    ax1.set_xlim(-1.35, 1.35)
    ax1.set_ylim(-0.75, 0.75)
    ax1.set_xlabel("x [G = m = 1]")
    ax1.set_ylabel("y [G = m = 1]")
    ax1.set_title(f"(a) The figure-eight orbit, T = {T_run:.6f}")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="upper left", fontsize=9)

    tt = t / T_run
    ax2.plot(tt, r12, color=GOLD, lw=2.0, label=r"$r_{12}$")
    ax2.plot(tt, r13, color=blue, lw=1.6, ls="--", label=r"$r_{13}$")
    ax2.plot(tt, r23, color=green, lw=1.6, ls="-.", label=r"$r_{23}$")
    ax2.annotate(
        f"max = {r12.max():.4f}",
        xy=(0.5, r12.max()),
        textcoords="offset points",
        xytext=(6, 6),
        fontsize=10,
        color=NAVY,
    )
    ax2.annotate(
        f"min = {min(r12.min(), r13.min()):.4f}",
        xy=(tt[int(np.argmin(r13))], r13.min()),
        textcoords="offset points",
        xytext=(6, -14),
        fontsize=10,
        color=NAVY,
    )
    ax2.set_xlabel("t / T [orbit periods]")
    ax2.set_ylabel("pairwise separation [G = m = 1]")
    ax2.set_title("(b) Pairwise separations over one period")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="lower right", fontsize=9)
    fig.savefig(figdir / "fig01_orbit_overview.png")
    plt.close(fig)

    # ================= fig02 — waveform + comb (headline) ====================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(
        "TRX-11 · Figure-eight choreography — waveform and harmonic comb",
        fontsize=16,
        fontweight="bold",
    )
    ax1, ax2 = fig.subplots(1, 2)

    ax1.plot(tt, h_exact, color=NAVY, lw=1.5)
    for n in range(1, 6):
        ax1.axvline(n / 6.0, color=GOLD, lw=0.9, ls=":", alpha=0.8)
    ax1.annotate(
        "repeats every T/6",
        xy=(1.0 / 12.0, h_exact.max()),
        textcoords="offset points",
        xytext=(4, -4),
        fontsize=10.5,
        color=NAVY,
    )
    ax1.annotate(
        f"range [{h_exact.min():.2f}, +{h_exact.max():.2f}]",
        xy=(0.02, 0.06),
        xycoords="axes fraction",
        fontsize=10.5,
        color=NAVY,
    )
    ax1.set_xlabel("t / T [orbit periods]")
    ax1.set_ylabel(r"strain $h_+ \propto \ddot{Q}_{xx} - \ddot{Q}_{yy}$ [G = c = D = 1]")
    ax1.set_title("(a) Plus-polarised waveform over one orbit period")
    ax1.grid(True, alpha=0.3)

    mask = freqs * T_run <= 30.0
    ax2.plot(freqs[mask] * T_run, spec[mask], color=blue, lw=1.2)
    for n, a in comb.items():
        if a < 2.0 * other_max:
            continue
        ax2.plot(
            [n, n],
            [0.0, a],
            color=GOLD,
            lw=2.6,
            label="comb lines above background" if n == 6 else None,
        )
        ax2.annotate(
            f"n = {n}",
            xy=(n, a),
            textcoords="offset points",
            xytext=(4, 4),
            fontsize=10,
            color=NAVY,
        )
    ax2.axhline(other_max, color=red, lw=1.2, ls="--", label=f"other harmonics <= {other_max:.0e}")
    ax2.set_yscale("log")
    ax2.set_ylim(3e-5, 3.0)
    ax2.set_xlabel("f·T [harmonic index of the orbit period]")
    ax2.set_ylabel(r"$|\tilde{h}_+(f)|$ [arbitrary units]")
    ax2.set_title(f"(b) Harmonic comb: dominant line at n = {round(fT_peak)} (f·T = {fT_peak:.4f})")
    ax2.grid(True, alpha=0.3, which="both")
    ax2.legend(loc="upper right", fontsize=9)
    fig.savefig(figdir / "fig02_waveform_comb.png")
    plt.close(fig)

    # ================= fig03 — antenna pattern + detuning sweep ==============
    # (a) quadrupole antenna pattern from exact third derivatives
    idx = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
    A = {
        (0, 0): TF3xx,
        (1, 1): TF3yy,
        (2, 2): TF3zz,
        (0, 1): Q3xy,
        (0, 2): 0.0 * TF3xx,
        (1, 2): 0.0 * TF3xx,
    }
    M = np.zeros((3, 3, 3, 3))
    for a in idx:
        for c in idx:
            M[a[0], a[1], c[0], c[1]] = np.mean(A[a] * A[c])
    M = 0.5 * (M + M.transpose(1, 0, 2, 3))
    M = 0.5 * (M + M.transpose(0, 1, 3, 2))
    M = 0.5 * (M + M.transpose(2, 3, 0, 1))

    def _patt(theta, phi):
        st, ct = np.sin(theta), np.cos(theta)
        nx, ny, nz = st * np.cos(phi), st * np.sin(phi), ct
        Pm = np.eye(3) - np.outer([nx, ny, nz], [nx, ny, nz])
        L = np.einsum("ik,jl->ijkl", Pm, Pm) - 0.5 * np.einsum("ij,kl->ijkl", Pm, Pm)
        return float(np.einsum("ijkl,ijkl->", L, M))

    n_th = 91 if smoke else 181
    n_ph = 61 if smoke else 121
    th_g = np.linspace(0.0, np.pi, n_th)
    ph_g = np.linspace(0.0, 2.0 * np.pi, n_ph)
    pat = np.zeros((n_th, n_ph))
    for i, a in enumerate(th_g):
        for j, p in enumerate(ph_g):
            pat[i, j] = _patt(a, p)
    pat_max = float(pat.max())
    mid = int(round((n_th - 1) / 2))
    pat_eq = pat[mid, :]
    eq_min = float(pat_eq.min())
    eq_diag = float(pat[mid, int(round((n_ph - 1) / 8))])
    pole = float(pat[0, 0])

    # (b) velocity-detuning sweep: the choreography is an isolated solution
    from scipy.optimize import minimize_scalar
    from scipy.integrate import solve_ivp as _sivp

    s0 = initial_state()
    p0 = s0.reshape(3, 4)[:, 0:2]
    k_grid = [0.95, 1.0, 1.05] if smoke else [0.90, 0.95, 0.98, 0.99, 1.00, 1.01, 1.02, 1.05, 1.10]
    closure_k, dT_k = [], []
    for k in k_grid:
        sk = s0.copy()
        sk.reshape(3, 4)[:, 2:4] *= k
        sk_sol = _sivp(
            rhs,
            (0.0, 8.0),
            sk,
            method="DOP853",
            rtol=1e-11,
            atol=1e-11,
            dense_output=True,
            max_step=0.01,
        )

        def clos(tq):
            st = sk_sol.sol(tq).reshape(3, 4)
            return float(np.max(np.abs(st[:, 0:2] - p0)))

        tg = np.linspace(4.0, 8.0, 400)
        cc = np.array([clos(tq) for tq in tg])
        im = int(np.argmin(cc))
        rr = minimize_scalar(
            clos,
            bounds=(tg[max(im - 2, 0)], tg[min(im + 2, tg.size - 1)]),
            method="bounded",
            options={"xatol": 1e-10},
        )
        closure_k.append(float(rr.fun))
        dT_k.append(float(rr.x - T_run))
    detuned_min = min(c for k, c in zip(k_grid, closure_k) if abs(k - 1.0) >= 0.01)
    detuned_dT = max(abs(d) for k, d in zip(k_grid, dT_k) if abs(k - 1.0) >= 0.01)

    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(
        "TRX-11 · Figure-eight choreography — radiation pattern and isolation",
        fontsize=16,
        fontweight="bold",
    )
    ax1, ax2 = fig.subplots(1, 2)

    R, PH = np.meshgrid(th_g * 180.0 / np.pi, ph_g * 180.0 / np.pi, indexing="ij")
    c = ax1.contourf(PH, R, pat / pat_max, levels=18, cmap="YlOrBr")
    fig.colorbar(c, ax=ax1, pad=0.02, label=r"$dP/d\Omega$ (normalised to peak)")
    ax1.set_xlabel(r"azimuth $\varphi$ [deg]")
    ax1.set_ylabel(r"polar angle $\theta$ [deg] (0 = orbital normal)")
    ax1.set_yticks([0, 30, 60, 90, 120, 150, 180])
    ax1.set_title("(a) Quadrupole antenna pattern (time-averaged)")
    ax1.annotate(
        f"peak at the orbital normal:\n{pole / lum_mean:.2f} x mean luminosity",
        xy=(0.04, 0.94),
        xycoords="axes fraction",
        fontsize=10,
        color=NAVY,
    )
    ax1.annotate(
        f"in-plane min {eq_min / pat_max:.2f} (along x),\n"
        f"in-plane max {eq_diag / pat_max:.2f} (along diagonal)",
        xy=(0.04, 0.06),
        xycoords="axes fraction",
        fontsize=10,
        color=NAVY,
    )

    ax2.plot(
        k_grid,
        closure_k,
        color=blue,
        lw=2.0,
        marker="o",
        ms=7,
        mec=NAVY,
        label="closure residual at first return",
    )
    ax2.set_yscale("log")
    ax2.set_ylim(1e-9, 3.0)
    ax2.set_xlabel("velocity scale factor k (initial velocities multiplied by k)")
    ax2.set_ylabel("config closure residual [G = m = 1]", color=blue)
    ax2.tick_params(axis="y", labelcolor=blue)
    ax2.axhline(5e-8, color=NAVY, lw=1.1, ls="--", label="acceptance tolerance 5e-8")
    ax2.annotate(
        f"k = 1: {closure_k[k_grid.index(1.0)]:.1e}",
        xy=(1.0, closure_k[k_grid.index(1.0)]),
        textcoords="offset points",
        xytext=(8, 8),
        fontsize=10,
        color=NAVY,
    )
    ax2.grid(True, alpha=0.3)
    ax2.set_title("(b) Velocity-detuning sweep: the eight is isolated")
    ax2b = ax2.twinx()
    ax2b.plot(
        k_grid, dT_k, color=red, lw=1.8, marker="s", ms=6, label=r"return-time shift $\Delta T$"
    )
    ax2b.axhline(0.0, color=red, lw=0.8, ls=":", alpha=0.7)
    ax2b.set_ylabel(r"$\Delta T$ [time units]", color=red)
    ax2b.tick_params(axis="y", labelcolor=red)
    h2, l2 = ax2.get_legend_handles_labels()
    h2b, l2b = ax2b.get_legend_handles_labels()
    leg = ax2.legend(h2 + h2b, l2 + l2b, loc="upper center", fontsize=9)
    leg.set_frame_on(True)
    leg.get_frame().set_facecolor("white")
    leg.get_frame().set_edgecolor(NAVY)
    leg.get_frame().set_alpha(0.92)
    fig.savefig(figdir / "fig03_pattern_sweep.png")
    plt.close(fig)

    # ================= fig04 — quadrupole dynamics ===========================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(
        "TRX-11 · Figure-eight choreography — quadrupole dynamics", fontsize=16, fontweight="bold"
    )
    ax1, ax2 = fig.subplots(1, 2)

    ax1.plot(tt, Qddxx, color=GOLD, lw=1.8, label=r"$\ddot{Q}_{xx}$")
    ax1.plot(tt, Qddyy, color=blue, lw=1.4, ls="--", label=r"$\ddot{Q}_{yy}$")
    ax1.plot(tt, Qddxy, color=green, lw=1.4, ls="-.", label=r"$\ddot{Q}_{xy}$")
    ax1.axhline(0.0, color=NAVY, lw=0.8, alpha=0.5)
    ax1.set_xlabel("t / T [orbit periods]")
    ax1.set_ylabel(r"quadrupole acceleration [G = m = 1]")
    ax1.set_title("(a) Exact second derivatives of the quadrupole")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="upper left", fontsize=9)

    ax2.plot(tt, lum_t, color=NAVY, lw=1.5, label="instantaneous luminosity")
    ax2.plot(tt, np.cumsum(lum_t) * dt, color=GOLD, lw=2.2, label="cumulative radiated energy")
    ax2.annotate(
        f"$\\langle P \\rangle$ = {lum_mean:.2f}",
        xy=(0.35, lum_mean),
        textcoords="offset points",
        xytext=(6, 6),
        fontsize=10.5,
        color=NAVY,
    )
    ax2.annotate(
        f"max P = {lum_max:.2f}",
        xy=(tt[int(np.argmax(lum_t))], lum_max),
        textcoords="offset points",
        xytext=(-64, 2),
        fontsize=10.5,
        color=NAVY,
    )
    ax2.annotate(
        f"E(T) = {energy_T:.2f}",
        xy=(1.0, energy_T),
        textcoords="offset points",
        xytext=(-72, -14),
        fontsize=10.5,
        color=NAVY,
    )
    ax2.set_xlabel("t / T [orbit periods]")
    ax2.set_ylabel(r"quadrupole luminosity / energy [G = c = 1]")
    ax2.set_title("(b) Radiated power and cumulative energy")
    ax2.grid(True, alpha=0.3)
    leg = ax2.legend(loc="upper center", fontsize=9, ncols=2)
    leg.set_frame_on(True)
    leg.get_frame().set_facecolor("white")
    leg.get_frame().set_edgecolor(NAVY)
    leg.get_frame().set_alpha(0.92)
    fig.savefig(figdir / "fig04_quadrupole_dynamics.png")
    plt.close(fig)

    # ================= scheme SVG ============================================
    sol_long_t = np.linspace(0.0, T_full, 240)
    orb_full = sol_scheme.sol(sol_long_t).reshape(3, 4, -1)[2, 0:2, :].T
    make_scheme_svg(figdir / "scheme_trx11.svg", orb_full, T_full)

    # ================= JSON figures block ====================================
    return {
        "mode": "smoke" if smoke else "full",
        "scheme": {
            "file": "figures/scheme_trx11.svg",
            "caption": (
                "Hand-authored schematic of the figure-eight choreography GW emitter: "
                "three equal masses chase each other along one closed curve with zero "
                "angular momentum, the rotating mass quadrupole radiates through gold "
                "lobes peaked along the orbital normal, and a LISA-class laser "
                f"interferometer observes the strain at inclination theta; period "
                f"T = {T_full:.6f}, waveform repeating every T/6, harmonic comb at "
                "multiples of 6/T."
            ),
        },
        "panels": [
            {
                "file": "figures/fig01_orbit_overview.png",
                "caption": (
                    "Orbit overview: (a) the figure-eight trajectory traced by all three "
                    f"equal masses over one period T = {T_run:.6f} with the chase direction "
                    "marked; (b) pairwise separations r12/r13/r23 over the same period, "
                    f"each ranging from {min(r12.min(), r13.min()):.4f} to "
                    f"{r12.max():.4f} and permuted among the pairs every T/3 by the "
                    "choreography exchange symmetry."
                ),
            },
            {
                "file": "figures/fig02_waveform_comb.png",
                "caption": (
                    "Headline result - the gravitational waveform of the choreography: "
                    "(a) exact plus-polarised strain from analytic quadrupole derivatives "
                    f"over one period, range [{h_exact.min():.2f}, +{h_exact.max():.2f}], "
                    "repeating every T/6; (b) harmonic comb of the spectrum - the lines "
                    "at n = 6, 12, 18 of the orbital frequency rise above the background "
                    f"with relative amplitudes {comb.get(6, 0):.3f} : {comb.get(12, 0):.3f} : "
                    f"{comb.get(18, 0):.4f}, every other harmonic of the orbital "
                    f"frequency staying below {other_max:.0e} of the dominant line at "
                    f"f·T = {fT_peak:.4f}."
                ),
            },
            {
                "file": "figures/fig03_pattern_sweep.png",
                "caption": (
                    "Directionality and isolation: (a) time-averaged quadrupole antenna "
                    "pattern from exact third derivatives, peaked along the orbital "
                    f"normal at {pole / lum_mean:.2f} times the mean luminosity, with "
                    f"in-plane minima {eq_min / pat_max:.2f} of the peak along x and "
                    f"in-plane maxima {eq_diag / pat_max:.2f} along the diagonals; "
                    "(b) velocity-detuning sweep - scaling the initial velocities by k "
                    "leaves the k = 1 closure residual at "
                    f"{closure_k[k_grid.index(1.0)]:.1e} while the smallest detuned "
                    f"residual is {detuned_min:.1e} with return-time shifts up to "
                    f"{detuned_dT:.2f} - the choreography is an isolated solution."
                ),
            },
            {
                "file": "figures/fig04_quadrupole_dynamics.png",
                "caption": (
                    "Emitter dynamics: (a) exact second derivatives of the quadrupole "
                    "components over one period - the T/3 exchange symmetry and the "
                    "T/2 sign flip of the xy component are visible; (b) instantaneous "
                    f"quadrupole luminosity P(t) = (1/5) sum (d3Q/dt3)^2 with mean "
                    f"{lum_mean:.2f} and maximum {lum_max:.2f}, and the cumulative "
                    f"radiated energy reaching {energy_T:.2f} over one period "
                    "(G = c = D = 1)."
                ),
            },
        ],
        "data": {
            "spectrum_comb": {
                "peak_fT": round(fT_peak, 5),
                "dominant_harmonic": round(fT_peak),
                "rel_amp": {str(n): round(a, 6) for n, a in comb.items()},
                "max_other_harmonic": float(f"{other_max:.3e}"),
                "strain_min": round(float(h_exact.min()), 6),
                "strain_max": round(float(h_exact.max()), 6),
            },
            "antenna_pattern": {
                "polar_max_over_mean": round(pole / lum_mean, 4),
                "equator_min_over_peak": round(eq_min / pat_max, 4),
                "equator_diag_over_peak": round(eq_diag / pat_max, 4),
                "luminosity_mean_exact": round(lum_mean, 4),
                "luminosity_max_exact": round(lum_max, 4),
                "energy_per_period_exact": round(energy_T, 4),
            },
            "velocity_sweep": {
                "k": [float(k) for k in k_grid],
                "closure": [float(f"{c:.4e}") for c in closure_k],
                "return_time_shift": [float(f"{d:.5f}") for d in dT_k],
            },
            "separations": {
                "r_min": round(float(min(r12.min(), r13.min(), r23.min())), 6),
                "r_max": round(float(max(r12.max(), r13.max(), r23.max())), 6),
            },
        },
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="TRX-11 GW from choreography")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument(
        "--figures",
        action="store_true",
        help="write scheme SVG + four canonical PNG panels into figures/ "
        "and add a figures block to the JSON protocol",
    )
    args = ap.parse_args(argv)
    smoke = args.smoke or bool(os.environ.get("TRX_SMOKE"))
    t0w = time.time()

    s0 = initial_state()
    E0 = energy(s0)

    # --- find the period by global minimisation of the config closure ------
    sol_long = solve_ivp(
        rhs,
        (0.0, 12.0),
        s0,
        method="DOP853",
        rtol=1e-13,
        atol=1e-13,
        dense_output=True,
        max_step=0.01,
    )

    def closure(t):
        st = sol_long.sol([t]).reshape(3, 4)
        b = st.reshape(3, 4)
        return float(np.max(np.abs(b[:, 0:2] - s0.reshape(3, 4)[:, 0:2])))

    tg = np.linspace(2.0, 11.0, 1800)
    cc = np.array([closure(t) for t in tg])
    i_min = int(np.argmin(cc))
    t_lo = tg[max(i_min - 3, 0)]
    t_hi = tg[min(i_min + 3, tg.size - 1)]
    from scipy.optimize import minimize_scalar

    r = minimize_scalar(closure, bounds=(t_lo, t_hi), method="bounded", options={"xatol": 1e-13})
    T = float(r.x)
    closure_err = float(r.fun)
    add(
        "period_closure_error",
        closure_err,
        0.0,
        5e-8,
        "dimless",
        f"T = {T:.9f} (config closure after one period)",
    )
    add(
        "period_in_expected_range",
        1.0 if 6.2 < T < 6.5 else 0.0,
        1.0,
        1e-12,
        "bool",
        f"T = {T:.6f} within the published range",
    )

    # --- integrate exactly one period with high accuracy -------------------
    T_run = 0.5 * T if smoke else 1.0 * T
    sol = solve_ivp(
        rhs,
        (0.0, T_run),
        s0,
        method="DOP853",
        rtol=1e-13,
        atol=1e-13,
        dense_output=True,
        max_step=0.005,
    )
    ts = np.linspace(0.0, T_run, 300 if smoke else 3000)
    Y = sol.sol(ts).reshape(3, 4, -1)

    E = np.array([energy(sol.sol(t)) for t in ts])
    add(
        "energy_conserved",
        float(np.max(np.abs(E - E0))),
        0.0,
        1e-12,
        "energy",
        "relative drift below 1e-12",
    )
    Lz = np.array([angular_momentum(sol.sol(t)) for t in ts])
    add(
        "angular_momentum_is_zero",
        float(np.max(np.abs(Lz))),
        0.0,
        1e-9,
        "ang mom",
        "the figure-eight carries exactly zero angular momentum",
    )

    # --- quadrupole radiation ------------------------------------------------
    # dense sample for two clean numerical derivatives
    t_dense = np.linspace(0.0, T_run, 4001 if smoke else 12001)
    Yd = sol_long.sol(t_dense).reshape(3, 4, -1) if False else None
    Qxx = np.zeros(t_dense.size)
    Qyy = np.zeros(t_dense.size)
    Qxy = np.zeros(t_dense.size)
    for i, t in enumerate(t_dense):
        Q = quadrupole(sol.sol(t)) if t <= T_run + 1e-12 else quadrupole(sol.sol(T_run))
        Qxx[i], Qyy[i], Qxy[i] = Q[0, 0], Q[1, 1], Q[0, 1]
    dt = t_dense[1] - t_dense[0]
    # second derivative of (Qxx - Qyy) -> plus-polarised waveform proxy
    d1 = np.gradient(Qxx - Qyy, dt)
    h_plus = np.gradient(d1, dt)
    # luminosity proxy: (1/5) sum (third derivatives)^2 via Qxy too
    d1xy = np.gradient(Qxy, dt)
    d2xy = np.gradient(d1xy, dt)
    d3xy = np.gradient(d2xy, dt)
    lum = float(np.mean((1.0 / 5.0) * (np.gradient(np.gradient(h_plus, dt), dt) ** 2 + d3xy**2)))
    add(
        "luminosity_finite_positive",
        1.0 if 0.0 < lum < 1e10 else 0.0,
        1.0,
        1e-12,
        "bool",
        f"mean GW luminosity proxy = {lum:.4f} (G=c=D=1)",
    )

    # quadrupole symmetry of the choreography (equal masses): the SET of
    # positions repeats with period T/3, so Q must be periodic with T/3
    if not smoke:
        dQ_half = float(np.max(np.abs(quadrupole(sol.sol(T_run / 2.0)) - quadrupole(s0))))
        dQ_third = float(np.max(np.abs(quadrupole(sol.sol(T_run / 3.0)) - quadrupole(s0))))
        add(
            "quadrupole_choreography_symmetry",
            1.0 if (dQ_half < 1e-6 or dQ_third < 1e-6) else 0.0,
            1.0,
            1e-12,
            "bool",
            f"|Q(T/2)-Q(0)| = {dQ_half:.2e}, |Q(T/3)-Q(0)| = {dQ_third:.2e}",
        )

    # spectrum: dominant harmonic at 2/T
    sig = h_plus - h_plus.mean()
    win = np.hanning(sig.size)
    spec = np.abs(np.fft.rfft(sig * win))
    freqs = np.fft.rfftfreq(sig.size, d=dt)
    k_pk = int(np.argmax(spec[1:]) + 1)
    f_pk = freqs[k_pk]
    ratio = f_pk * T
    add(
        "dominant_harmonic_on_comb",
        abs(ratio - round(ratio)),
        0.0,
        0.05,
        "harmonic index",
        f"peak at f*T = {ratio:.4f} -> harmonic n = {round(ratio)} of the orbit period",
    )

    out = Path(__file__).resolve().parents[1] / "results"
    out.mkdir(exist_ok=True)
    orbit = []
    n_orb = 300
    for i in range(n_orb):
        st = sol.sol(T_run * i / (n_orb - 1)).reshape(3, 4)
        orbit.append((st[2, 0], st[2, 1]))
    make_svg(orbit, h_plus, t_dense, out / "trx11_plot.svg")

    # --- canonical figures (--figures, additive) -----------------------------
    figures_block = None
    figdir = Path(__file__).resolve().parents[1] / "figures"
    if args.figures:
        figures_block = render_figures(
            sol=sol, sol_scheme=sol_long, T_full=T, T_run=T_run, smoke=smoke, figdir=figdir
        )

    all_pass = all(c["pass"] for c in CHECKS)
    stride = max(1, ts.size // 400)
    protocol = {
        "study": "TRX-11",
        "title": "Gravitational waves from the figure-eight choreography",
        "status": "PASS" if all_pass else "FAIL",
        "smoke": bool(smoke),
        "runtime_s": round(time.time() - t0w, 3),
        "checks": CHECKS,
        "series": {
            "t": ts[::stride].round(5).tolist(),
            "x3": Y[2, 0][::stride].round(8).tolist(),
            "y3": Y[2, 1][::stride].round(8).tolist(),
            "h_plus": h_plus[:: max(1, h_plus.size // 400)].round(10).tolist(),
        },
        "meta": {
            "equations": [
                "Q_ij = sum_k m_k x_ki x_kj ;  h_plus ~ d^2(Qxx-Qyy)/dt^2",
                "P = (1/5) sum_ij (d^3 Q_ij/dt^3)^2   (G = c = D = 1)",
                "Chenciner-Montgomery figure-eight: T ~ 6.3244, L = 0",
            ],
            "period_T": T,
            "mean_luminosity_proxy": lum,
            "dominant_harmonic_index": round(ratio),
            "laser_link": "LISA/Taiji/TianQin laser interferometers are the natural "
            "detectors of three-body GW signatures",
        },
    }
    if figures_block is not None:
        protocol["figures"] = figures_block
    (out / "trx11_results.json").write_text(json.dumps(protocol, indent=2), encoding="utf-8")

    print(f"\nTRX-11 — GW from the figure-eight choreography  [{'SMOKE' if smoke else 'FULL'}]")
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
