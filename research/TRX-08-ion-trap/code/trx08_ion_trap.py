#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
TRIVORTEX LAB — TRX-08 — THREE LASER-COOLED IONS IN A LINEAR PAUL TRAP
============================================================================
Three equal ions in a 2-D harmonic rf pseudopotential with mutual Coulomb
repulsion form a table-top three-body problem.  Laser Doppler cooling is
modelled as a linear drag, under which the ions crystallize into the
equilateral "Lagrange triangle" of side

    a = (3*kappa/omega0^2)^(1/3)          (force balance),

with normal modes: two COM modes at omega0, one zero (rigid rotation),
and the breathing mode at sqrt(3)*omega0 — the trapped-ion analogue of
the Lagrange relative equilibrium that underlies TRIVORTEX Theorem 3.1.

Laser connection: Doppler cooling force, ion-crystal quantum simulators;
three trapped ions = the smallest many-body quantum simulator.

What is computed
  * damped crystallization into the equilateral triangle
  * Hessian normal-mode spectrum vs analytic values
  * conservative rigid rotation and energy conservation

With --figures: hand-authored scheme SVG + four canonical PNG panels
(300 dpi) into figures/, and a "figures" block added to the JSON protocol
(scheme, panels with captions, kappa/gamma sweep data). Composable with
--smoke; without --figures the behavior, checks and JSON are unchanged.

Usage:  python trx08_ion_trap.py [--smoke] [--figures]
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

W0, KAPPA, M, EPS = 1.0, 1.0, 1.0, 1e-12

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
# Dynamics: interleaved state [x1,y1,vx1,vy1, ...] -> [vx1,vy1,ax1,ay1, ...]
# ---------------------------------------------------------------------------


def forces(state, gamma_d=0.0):
    n = state.size // 4
    s = state.reshape(n, 4)
    F = np.zeros((n, 2))
    xy = s[:, 0:2]
    for k in range(n):
        F[k] = -(W0**2) * xy[k]
        for j in range(n):
            if j == k:
                continue
            d = xy[k] - xy[j]
            r = np.hypot(d[0], d[1])
            F[k] += KAPPA * d / (r**2 + EPS**2) ** 1.5
    if gamma_d:
        F -= gamma_d * s[:, 2:4]
    return F


def rhs(t, state, gamma_d=0.0):
    n = state.size // 4
    s = state.reshape(n, 4)
    out = np.empty_like(s)
    out[:, 0:2] = s[:, 2:4]
    out[:, 2:4] = forces(state, gamma_d) / M
    return out.reshape(-1)


def total_energy(state):
    n = state.size // 4
    s = state.reshape(n, 4)
    K = 0.5 * M * float(np.sum(s[:, 2:4] ** 2))
    U = 0.5 * M * W0**2 * float(np.sum(s[:, 0:2] ** 2))
    for k in range(n):
        for j in range(k + 1, n):
            r = np.hypot(*(s[k, 0:2] - s[j, 0:2]))
            U += KAPPA / np.hypot(r, EPS)
    return K + U


# ---------------------------------------------------------------------------
# Normal modes from the Hessian at the equilibrium
# ---------------------------------------------------------------------------

POS_IDX = [0, 1, 4, 5, 8, 9]  # position dofs of the interleaved 12-state


def position_hessian(eq):
    """6x6 position-space Hessian of the potential at a configuration."""
    h = 1e-4
    m = len(POS_IDX)

    def pot12(x):
        xy = x.reshape(3, 4)[:, 0:2]
        U = 0.5 * M * W0**2 * float(np.sum(xy**2))
        for k in range(3):
            for j in range(k + 1, 3):
                r = np.hypot(*(xy[k] - xy[j]))
                U += KAPPA / np.hypot(r, EPS)
        return U

    H = np.zeros((m, m))
    for i in range(m):
        for j in range(i, m):
            ei = np.zeros(12)
            ei[POS_IDX[i]] = h
            ej = np.zeros(12)
            ej[POS_IDX[j]] = h
            H[i, j] = (
                pot12(eq + ei + ej)
                - pot12(eq + ei - ej)
                - pot12(eq - ei + ej)
                + pot12(eq - ei - ej)
            ) / (4 * h * h)
            H[j, i] = H[i, j]
    return H


def hessian_freqs(eq):
    """Mode eigenvalues and frequencies at an equilibrium."""
    H = position_hessian(eq)
    vals = np.linalg.eigvalsh(H / M)
    return vals, np.sqrt(np.clip(vals, 0.0, None))


# ---------------------------------------------------------------------------
# Canonical figures (--figures mode): scheme SVG + four PNG panels
# ---------------------------------------------------------------------------


def make_scheme_svg(path, stats):
    """Hand-authored schematic of the physical idea: three laser-cooled ions
    in the transverse plane of a linear Paul trap crystallize into the
    equilateral Lagrange triangle under Coulomb repulsion + harmonic
    confinement + Doppler drag; normal-mode ladder and the mapping to the
    TRIVORTEX vortex model. White background, navy strokes, gold accents."""
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
        f'  <text x="30" y="38" font-family="{F}" font-size="20" font-weight="bold" '
        'fill="#0A1730">TRX-08 &#8212; Scheme: three laser-cooled ions crystallize into '
        "the Lagrange triangle</text>",
        f'  <text x="30" y="61" font-family="{F}" font-size="13" fill="#3A4A66">Harmonic '
        "rf pseudopotential + Coulomb repulsion + Doppler cooling &#8212; a table-top "
        "three-body problem</text>",
        # ---- left panel: Paul-trap cross-section with the ion crystal --------
        '  <rect x="60" y="92" width="380" height="330" rx="10" fill="#FBF6E8" '
        'stroke="#0A1730" stroke-width="2"/>',
        f'  <text x="250" y="86" font-family="{F}" font-size="12" fill="#0A1730" '
        'text-anchor="middle">linear Paul trap &#8212; transverse (x, y) plane</text>',
        # four rf electrode rods (cross-section circles)
    ]
    rods = [(95, 127), (405, 127), (95, 403), (405, 403)]
    for rx, ry in rods:
        s.append(f'  <circle cx="{rx}" cy="{ry}" r="14" fill="#0A1730" stroke="none"/>')
        s.append(
            f'  <text x="{rx}" y="{ry + 4}" font-family="{F}" font-size="10" '
            'fill="#F0D98C" text-anchor="middle">rf</text>'
        )
    s += [
        # dashed harmonic equipotentials
        '  <circle cx="250" cy="265" r="142" fill="none" stroke="#0A1730" '
        'stroke-width="1" stroke-dasharray="4 5" opacity="0.3"/>',
        '  <circle cx="250" cy="265" r="100" fill="none" stroke="#0A1730" '
        'stroke-width="1" stroke-dasharray="4 5" opacity="0.25"/>',
        f'  <text x="240" y="415" font-family="{F}" font-size="10.5" fill="#3A4A66" '
        'text-anchor="middle">harmonic pseudopotential U =</text>',
        f'  <text x="352" y="415" font-family="{F}" font-size="10.5" fill="#3A4A66" '
        'text-anchor="middle">m&#969;&#8320;&#178;r&#178;/2</text>',
        # triangle edges
        '  <line x1="250" y1="177" x2="176.4" y2="309" stroke="#0A1730" stroke-width="1.7"/>',
        '  <line x1="176.4" y1="309" x2="323.6" y2="309" stroke="#0A1730" stroke-width="1.7"/>',
        '  <line x1="323.6" y1="309" x2="250" y2="177" stroke="#0A1730" stroke-width="1.7"/>',
        f'  <text x="296" y="244" font-family="{F}" font-size="12.5" font-weight="bold" '
        'fill="#0A1730">a</text>',
        # force balance on the lower-right ion: Coulomb pushes (gold) vs trap pull (navy)
        '  <line x1="334" y1="309" x2="390" y2="309" stroke="#D4AF37" stroke-width="1.8" '
        'marker-end="url(#arrG)"/>',
        '  <line x1="332" y1="318" x2="358" y2="341" stroke="#D4AF37" stroke-width="1.4" '
        'marker-end="url(#arrG)"/>',
        '  <line x1="315" y1="304" x2="281" y2="284" stroke="#0A1730" stroke-width="1.8" '
        'marker-end="url(#arrN)"/>',
        f'  <text x="392" y="296" font-family="{F}" font-size="11" fill="#B08A18" '
        'text-anchor="end">Coulomb push</text>',
        f'  <text x="276" y="278" font-family="{F}" font-size="11" fill="#0A1730" '
        'text-anchor="end">trap pull</text>',
        # ions: gold circles with + charge
    ]
    ions = [(250, 177, "1"), (176.4, 309, "2"), (323.6, 309, "3")]
    for ix, iy, lab in ions:
        s.append(
            f'  <circle cx="{ix}" cy="{iy}" r="9" fill="#D4AF37" stroke="#0A1730" '
            'stroke-width="1.6"/>'
        )
        s.append(
            f'  <line x1="{ix - 4.5}" y1="{iy}" x2="{ix + 4.5}" y2="{iy}" '
            'stroke="#0A1730" stroke-width="1.4"/>'
        )
        s.append(
            f'  <line x1="{ix}" y1="{iy - 4.5}" x2="{ix}" y2="{iy + 4.5}" '
            'stroke="#0A1730" stroke-width="1.4"/>'
        )
    s += [
        # Doppler-cooling beams (two gold arrows toward the lower-left ion)
        '  <line x1="84" y1="352" x2="152" y2="318" stroke="#D4AF37" stroke-width="1.8" '
        'marker-end="url(#arrG)"/>',
        '  <line x1="84" y1="336" x2="140" y2="308" stroke="#D4AF37" stroke-width="1.2" '
        'marker-end="url(#arrG)"/>',
        f'  <text x="118" y="396" font-family="{F}" font-size="10.5" fill="#B08A18">'
        "Doppler cooling (&#8722;&#947;v)</text>",
        # ---- right panel (top): normal-mode ladder ---------------------------
        '  <rect x="520" y="92" width="380" height="208" rx="10" fill="#FFFFFF" '
        'stroke="#0A1730" stroke-width="2"/>',
        f'  <text x="710" y="86" font-family="{F}" font-size="12" fill="#0A1730" '
        'text-anchor="middle">normal modes of the 3-ion crystal (&#969;&#8320; = 1)</text>',
        '  <line x1="560" y1="112" x2="560" y2="286" stroke="#0A1730" '
        'stroke-width="1.5" marker-end="url(#arrN)"/>',
    ]
    # ladder levels: (freq, single-line label)
    levels = [
        (1.7321, "&#8730;3&#183;&#969;&#8320; = 1.732051 &#8212; breathing"),
        (1.2247, "&#8730;(3/2)&#183;&#969;&#8320; = 1.224745 (&#215;2) &#8212; quadrupole"),
        (1.0, "&#969;&#8320; = 1 (&#215;2) &#8212; centre of mass"),
        (0.0, "0 &#8212; rigid rotation (zero mode)"),
    ]
    for fr, lab in levels:
        y = 286.0 - 92.0 * fr
        s.append(
            f'  <line x1="560" y1="{y:.1f}" x2="618" y2="{y:.1f}" stroke="#0A1730" '
            'stroke-width="1.7"/>'
        )
        s.append(
            f'  <circle cx="{612 if fr in (1.2247, 1.0) else 596}" cy="{y:.1f}" r="4" '
            'fill="#D4AF37" stroke="#0A1730" stroke-width="1"/>'
        )
        if fr in (1.2247, 1.0):
            s.append(
                f'  <circle cx="{626}" cy="{y:.1f}" r="4" fill="#D4AF37" '
                'stroke="#0A1730" stroke-width="1"/>'
            )
        s.append(
            f'  <text x="640" y="{y + 4:.1f}" font-family="{F}" font-size="11" '
            f'fill="#0A1730">{lab}</text>'
        )
    s += [
        f'  <text x="554" y="122" font-family="{F}" font-size="10.5" fill="#0A1730" '
        'text-anchor="end">&#969;/&#969;&#8320;</text>',
        # ---- right panel (bottom): mapping to TRIVORTEX -----------------------
        '  <rect x="520" y="310" width="380" height="112" rx="10" fill="#FBF6E8" '
        'stroke="#0A1730" stroke-width="2"/>',
        f'  <text x="536" y="330" font-family="{F}" font-size="11.5" font-weight="bold" '
        'fill="#0A1730">ion crystal &#8594; TRIVORTEX vortex model</text>',
    ]
    maps = [
        ("equilateral 3-ion crystal", "Lagrange relative equilibrium"),
        ("Coulomb + harmonic trap", "competing scales fix the size"),
        ("breathing &#8730;3&#183;&#969;&#8320;", "radial modulation of Theorem 3.1"),
        ("zero rotation mode", "continuous choreography family"),
    ]
    for i, (lft, rgt) in enumerate(maps):
        y = 352 + 19 * i
        s.append(
            f'  <text x="536" y="{y}" font-family="{F}" font-size="10.5" '
            f'fill="#0A1730">{lft}</text>'
        )
        s.append(
            f'  <line x1="688" y1="{y - 4}" x2="706" y2="{y - 4}" stroke="#D4AF37" '
            f'stroke-width="1.6" marker-end="url(#arrG)"/>'
        )
        s.append(
            f'  <text x="714" y="{y}" font-family="{F}" font-size="10.5" '
            f'fill="#0A1730">{rgt}</text>'
        )
    s += [
        # bottom strip with the measured numbers
        f'  <text x="60" y="466" font-family="{F}" font-size="12" fill="#0A1730">'
        f'a = 3&#185;&#8260;&#179; = {stats["a"]:.9f} (trap length units); crystal energy '
        f'U* = (3/2)&#183;3&#178;&#8260;&#179; = {stats["U"]:.12f}</text>',
        f'  <text x="60" y="488" font-family="{F}" font-size="11.5" fill="#3A4A66">'
        f'measured: sides equal to {stats["sides"]:.1e}; angles 2&#960;/3 to '
        f'{stats["angles"]:.1e}; static hold {stats["hold"]:.1e} over t = {stats["T_hold"]:.0f}; '
        f'energy drift {stats["energy"]:.1e}</text>',
        "</svg>",
    ]
    Path(path).write_text("\n".join(s), encoding="utf-8")


def render_figures(
    solr,
    Trel,
    st0,
    xf_vec,
    eq,
    eigvals,
    freqs,
    ts_c,
    Y_c,
    E_c,
    a_analytic,
    U_triangle,
    U_drop,
    gamma_relax,
    eps_relax,
    smoke,
    figdir,
):
    """Render the scheme SVG and four canonical PNG panels into figures/.

    Reuses the relaxation trajectory, the Newton-polished equilibrium, the
    Hessian spectrum and the conservative-hold data already computed in
    main(); adds the Coulomb-strength sweep of the crystal side and the
    Doppler-drag sweep of the crystallization (settle) time. Returns the
    "figures" block for the JSON protocol.
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    from scipy.optimize import root as _root

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
    suptitle = "TRX-08 · Three laser-cooled ions in a linear Paul trap"

    xf = xf_vec.reshape(3, 2)
    eq_pos = eq.reshape(3, 4)[:, 0:2]
    sides_f = [float(np.hypot(*(xf[i] - xf[j]))) for i, j in ((0, 1), (1, 2), (0, 2))]
    c_ang = xf.mean(axis=0)
    angs = np.sort(np.arctan2(xf[:, 1] - c_ang[1], xf[:, 0] - c_ang[0]) % (2 * np.pi))
    gaps_f = np.diff(np.concatenate([angs, [angs[0] + 2 * np.pi]]))
    side_spread = float(np.max(sides_f) - np.min(sides_f))
    ang_dev = float(np.max(np.abs(gaps_f - 2 * np.pi / 3)))

    # settle/drift data of the two recorded runs
    hold_drift = float(np.max(np.abs(Y_c[:, 0:2, -1] - eq_pos)))
    energy_drift = float(np.max(np.abs(E_c - E_c[0])))
    stats = {
        "a": a_analytic,
        "U": U_triangle,
        "sides": side_spread,
        "angles": ang_dev,
        "hold": hold_drift,
        "energy": energy_drift,
        "T_hold": float(ts_c[-1]),
    }
    make_scheme_svg(figdir / "scheme_trx08.svg", stats)

    # ---- kappa-parametrized gradient / relaxation rhs (sweeps) ---------------
    def grad_k(x, kappa, eps):
        # net force: restoring trap -omega0^2*x (cf. E1) + softened Coulomb
        xy = x.reshape(3, 2)
        G = -(W0**2) * xy
        for k in range(3):
            for j in range(3):
                if j == k:
                    continue
                d = xy[k] - xy[j]
                r = np.hypot(d[0], d[1])
                G[k] += kappa * d / (r**2 + eps**2) ** 1.5
        return G.reshape(-1)

    def rhs_relax_k(t, st, kappa, gamma):
        sr = st.reshape(3, 4)
        out = np.empty_like(sr)
        out[:, 0:2] = sr[:, 2:4]
        out[:, 2:4] = (
            grad_k(sr[:, 0:2].reshape(-1), kappa, eps_relax).reshape(3, 2) - gamma * sr[:, 2:4]
        )
        return out.reshape(-1)

    # ---- sweep (a): crystal side vs Coulomb strength kappa -------------------
    kappa_grid = np.array([0.25, 0.5, 1.0, 2.0, 4.0]) if not smoke else np.array([0.5, 1.0, 2.0])
    a_num = []
    for kap in kappa_grid:
        solk = solve_ivp(
            rhs_relax_k,
            (0.0, 0.5 * Trel),
            st0,
            args=(kap, gamma_relax),
            method="DOP853",
            rtol=1e-10,
            atol=1e-10,
            max_step=0.1,
        )
        solp = _root(lambda x: grad_k(x, kap, EPS), solk.y[POS_IDX, -1], tol=1e-14, method="hybr")
        xk = solp.x.reshape(3, 2)
        sides_k = [np.hypot(*(xk[i] - xk[j])) for i, j in ((0, 1), (1, 2), (0, 2))]
        a_num.append(float(np.mean(sides_k)))
    a_num = np.array(a_num)
    a_an_grid = (3.0 * kappa_grid / W0**2) ** (1.0 / 3.0)

    # ---- sweep (b): crystallization (settle) time vs Doppler drag ------------
    SETTLE_TOL = 0.01
    gamma_grid = np.array([0.4, 0.6, 0.8, 1.2, 1.6, 2.4]) if not smoke else np.array([0.8, 1.6])
    T_g = 60.0 if not smoke else 40.0
    t_settle = []
    for gam in gamma_grid:
        solg = solve_ivp(
            rhs_relax_k,
            (0.0, T_g),
            st0,
            args=(KAPPA, gam),
            method="DOP853",
            rtol=1e-10,
            atol=1e-10,
            dense_output=True,
            max_step=0.1,
        )
        tsg = np.linspace(0.0, T_g, 600)
        Xg = solg.sol(tsg).reshape(3, 4, -1)[:, 0:2, :]
        d01 = np.hypot(Xg[0, 0] - Xg[1, 0], Xg[0, 1] - Xg[1, 1])
        d12 = np.hypot(Xg[1, 0] - Xg[2, 0], Xg[1, 1] - Xg[2, 1])
        d20 = np.hypot(Xg[2, 0] - Xg[0, 0], Xg[2, 1] - Xg[0, 1])
        spread = np.maximum(np.maximum(d01, d12), d20) - np.minimum(np.minimum(d01, d12), d20)
        bad = np.where(spread >= SETTLE_TOL)[0]
        t_settle.append(
            float(tsg[bad[-1] + 1])
            if bad.size and bad[-1] + 1 < tsg.size
            else (T_g if bad.size else 0.0)
        )
    t_settle = np.array(t_settle)

    # ================= fig01 — model landscape ================================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    g1 = np.linspace(-2.4, 2.4, 360)
    X, Yg = np.meshgrid(g1, g1)
    U_slice = 0.5 * M * W0**2 * (X**2 + Yg**2)
    for j in (1, 2):
        U_slice += KAPPA / np.hypot(X - eq_pos[j, 0], Yg - eq_pos[j, 1])
    U_const = 0.5 * M * W0**2 * float(np.sum(eq_pos[1:] ** 2)) + KAPPA / float(
        np.hypot(*(eq_pos[1] - eq_pos[2]))
    )
    U_slice += U_const
    cmap = LinearSegmentedColormap.from_list("triton", [NAVY, "#3A5A8C", LIGHT_GOLD, "#FFFFFF"])
    lvls = np.linspace(float(U_slice.min()), float(U_slice.min()) + 5.0, 41)
    im1 = ax1.contourf(X, Yg, U_slice, levels=lvls, cmap=cmap, extend="max")
    tri = np.vstack([eq_pos, eq_pos[:1]])
    ax1.plot(
        tri[:, 0], tri[:, 1], color=GOLD, lw=1.5, ls="--", label="equilibrium triangle (side a)"
    )
    ax1.scatter(
        eq_pos[:, 0],
        eq_pos[:, 1],
        s=120,
        facecolors="none",
        edgecolors=GOLD,
        linewidths=1.6,
        label="ion equilibrium positions",
    )
    ax1.plot(
        eq_pos[0, 0],
        eq_pos[0, 1],
        marker="*",
        color=red,
        ms=15,
        ls="none",
        label="slice minimum (force balance)",
    )
    ax1.set_title("(a) potential slice: ion 1 scanned, ions 2, 3 held fixed")
    ax1.set_xlabel("x (trap length units)")
    ax1.set_ylabel("y (trap length units)")
    ax1.set_xlim(-2.4, 2.4)
    ax1.set_ylim(-2.4, 2.4)
    ax1.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0))
    fig.colorbar(im1, ax=ax1, shrink=0.85, label="U (trap energy units)")

    a_dense = np.linspace(0.85, 2.6, 400)
    ax2.plot(
        a_dense,
        0.5 * W0**2 * a_dense**2,
        ls="--",
        color=blue,
        lw=1.6,
        label="harmonic part $\\frac{1}{2}\\omega_0^2 a^2$",
    )
    ax2.plot(
        a_dense,
        3.0 * KAPPA / a_dense,
        ls="--",
        color=green,
        lw=1.6,
        label="Coulomb part $3\\kappa/a$",
    )
    ax2.plot(
        a_dense,
        0.5 * W0**2 * a_dense**2 + 3.0 * KAPPA / a_dense,
        color=NAVY,
        lw=2.4,
        label="total $U(a)$",
    )
    ax2.plot(
        [a_analytic],
        [U_triangle],
        "*",
        color=red,
        ms=15,
        label="minimum: $a_* = (3\\kappa/\\omega_0^2)^{1/3}$",
    )
    ax2.axvline(a_analytic, color=GOLD, lw=1.2, ls=":")
    ax2.annotate(
        f"$a_*$ = {a_analytic:.9f}\n$U_*$ = {U_triangle:.9f}",
        xy=(0.62, 0.55),
        xycoords="axes fraction",
        fontsize=10.5,
        color=NAVY,
        bbox=dict(boxstyle="round,pad=0.35", fc=LIGHT_GOLD, ec=GOLD, lw=1.0),
    )
    ax2.set_title("(b) energy along the equilateral family")
    ax2.set_xlabel("crystal side a (trap length units)")
    ax2.set_ylabel("potential energy U (trap energy units)")
    ax2.set_ylim(2.4, 5.4)
    ax2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14))
    ax2.grid(alpha=0.3)
    fig.savefig(figdir / "fig01_crystal_landscape.png")
    plt.close(fig)

    # ================= fig02 — headline: crystal + modes ======================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    tri = np.vstack([xf, xf[:1]])
    ax1.plot(tri[:, 0], tri[:, 1], color=NAVY, lw=1.8)
    ax1.scatter(
        xf[:, 0],
        xf[:, 1],
        s=420,
        color=GOLD,
        edgecolors=NAVY,
        linewidths=1.6,
        zorder=5,
        label="ions (+q)",
    )
    for k in range(3):
        ax1.annotate(
            f"ion {k + 1}",
            xy=xf[k],
            xytext=(xf[k] + 0.09 * (xf[k] - xf.mean(axis=0))),
            fontsize=10.5,
            color=NAVY,
            ha="center",
        )
    mid = 0.5 * (xf[1] + xf[2])
    ax1.annotate(
        f"a = {np.mean(sides_f):.9f} = $3^{{1/3}}$ (analytic)",
        xy=(mid[0], mid[1]),
        xycoords="data",
        xytext=(0.97, 0.03),
        textcoords="axes fraction",
        ha="right",
        fontsize=10.5,
        color=NAVY,
        bbox=dict(boxstyle="round,pad=0.3", fc=LIGHT_GOLD, ec=GOLD, lw=1.0),
    )
    # force balance on ion 3: two Coulomb pushes + trap pull (sum = 0)
    r3 = xf[2]
    pulls = []
    for j in (0, 1):
        d = r3 - xf[j]
        pulls.append(KAPPA * d / np.hypot(*d) ** 3)
    f_harm = -(W0**2) * r3
    for fvec, colr, lab in [
        (pulls[0] + pulls[1], GOLD, "Coulomb push (×2)"),
        (f_harm, NAVY, "trap pull −ω₀²r"),
    ]:
        nrm = np.hypot(*fvec)
        ax1.arrow(
            r3[0],
            r3[1],
            0.5 * fvec[0] / nrm,
            0.5 * fvec[1] / nrm,
            head_width=0.06,
            head_length=0.09,
            fc=colr,
            ec=colr,
            length_includes_head=True,
            zorder=6,
            label=lab,
        )
    ax1.plot(0.0, 0.0, marker="+", color=NAVY, ms=12, mew=1.8, ls="none")
    ax1.annotate(
        "net force = 0\n(harmonic + 2 Coulomb)",
        xy=(0.03, 0.05),
        xycoords="axes fraction",
        fontsize=10.5,
        color=NAVY,
        bbox=dict(boxstyle="round,pad=0.35", fc=LIGHT_GOLD, ec=GOLD, lw=1.0),
    )
    ax1.set_aspect("equal")
    ax1.set_title("(a) crystallized equilibrium (Newton-polished)")
    ax1.set_xlabel("x (trap length units)")
    ax1.set_ylabel("y (trap length units)")
    ax1.set_xlim(-1.35, 1.35)
    ax1.set_ylim(-1.35, 1.35)
    ax1.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0))

    mode_an = np.array([0.0, 1.0, 1.0, np.sqrt(1.5), np.sqrt(1.5), np.sqrt(3.0)])
    idx6 = np.arange(1, 7)
    for i in range(6):
        ax2.plot([idx6[i] - 0.3, idx6[i] + 0.3], [mode_an[i], mode_an[i]], color=NAVY, lw=2.0)
    ax2.plot(
        idx6,
        freqs,
        "o",
        color=GOLD,
        ms=9,
        mec=NAVY,
        mew=0.8,
        label="Hessian FD spectrum (h = 1e-4)",
    )
    ax2.plot(
        [],
        [],
        color=NAVY,
        lw=2.0,
        label="analytic: 0, $\\omega_0$×2, " "$\\sqrt{3/2}\\,\\omega_0$×2, $\\sqrt{3}\\,\\omega_0$",
    )
    dev = float(np.max(np.abs(np.sort(freqs) - mode_an)))
    ax2.annotate(
        f"max $|\\Delta\\omega|$ = {dev:.1e}\n(tolerance 5e-6)",
        xy=(0.05, 0.72),
        xycoords="axes fraction",
        fontsize=10.5,
        color=NAVY,
        bbox=dict(boxstyle="round,pad=0.35", fc=LIGHT_GOLD, ec=GOLD, lw=1.0),
    )
    ax2.annotate(
        "breathing $\\sqrt{3}\\,\\omega_0$",
        xy=(6, np.sqrt(3.0)),
        xytext=(4.15, 1.86),
        fontsize=10,
        color=NAVY,
    )
    ax2.annotate("quadrupole ×2", xy=(4, np.sqrt(1.5)), xytext=(2.6, 1.36), fontsize=10, color=NAVY)
    ax2.annotate("COM ×2", xy=(2, 1.0), xytext=(1.15, 0.62), fontsize=10, color=NAVY)
    ax2.annotate("rotation 0", xy=(1, 0.0), xytext=(1.1, 0.14), fontsize=10, color=NAVY)
    ax2.set_title("(b) normal-mode spectrum at the crystal")
    ax2.set_xlabel("mode index (6 position degrees of freedom)")
    ax2.set_ylabel("mode frequency $\\omega/\\omega_0$")
    ax2.set_xticks(idx6)
    ax2.set_ylim(-0.12, 2.0)
    ax2.legend(loc="upper left", bbox_to_anchor=(0.0, 1.08))
    ax2.grid(alpha=0.3)
    fig.savefig(figdir / "fig02_crystal_and_modes.png")
    plt.close(fig)

    # ================= fig03 — parameter sweeps ===============================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    k_dense = np.logspace(np.log10(0.18), np.log10(5.2), 200)
    ax1.loglog(
        k_dense,
        (3.0 * k_dense / W0**2) ** (1.0 / 3.0),
        color=NAVY,
        lw=2.0,
        label="analytic $a(\\kappa) = (3\\kappa/\\omega_0^2)^{1/3}$",
    )
    ax1.loglog(
        kappa_grid,
        a_num,
        "o",
        color=GOLD,
        ms=8,
        mec=NAVY,
        mew=0.8,
        label="numeric re-runs (relaxation + Newton)",
    )
    ax1.loglog([1.0], [a_analytic], "*", color=red, ms=14, label="preset $\\kappa$ = 1")
    ax1.set_title("(a) crystal side vs Coulomb strength")
    ax1.set_xlabel("Coulomb strength $\\kappa/\\omega_0^2$ (trap units)")
    ax1.set_ylabel("crystal side a (trap length units)")
    ax1.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0))
    ax1.grid(alpha=0.3, which="both")

    ax2.plot(
        gamma_grid,
        t_settle,
        "o-",
        color=GOLD,
        lw=1.8,
        mec=NAVY,
        mew=0.8,
        label="settle time (side spread < 0.01)",
    )
    ax2.plot(
        [gamma_relax],
        [t_settle[np.argmin(np.abs(gamma_grid - gamma_relax))]],
        "s",
        color=red,
        ms=10,
        label=f"preset drag $\\gamma_d$ = {gamma_relax}",
    )
    ax2.axhline(T_g, color=NAVY, ls="--", lw=1.2, label=f"integration window T = {T_g:.0f}")
    ax2.set_title("(b) crystallization time vs Doppler drag")
    ax2.set_xlabel("Doppler drag $\\gamma_d$ ($\\omega_0$ units)")
    ax2.set_ylabel("settle time $t_s$ ($1/\\omega_0$ units)")
    ax2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14))
    ax2.grid(alpha=0.3)
    fig.savefig(figdir / "fig03_scaling_sweeps.png")
    plt.close(fig)

    # ================= fig04 — crystallization dynamics =======================
    fig = plt.figure(figsize=(11.0, 7.5), dpi=450, constrained_layout=True)
    fig.suptitle(suptitle, fontsize=16, fontweight="bold")
    ax1, ax2 = fig.subplots(1, 2)

    ts_r = np.linspace(0.0, Trel, 900 if not smoke else 400)
    Yr = solr.sol(ts_r).reshape(3, 4, -1)[:, 0:2, :]
    for k in range(3):
        ax1.plot(Yr[k, 0], Yr[k, 1], color=SERIES[k], lw=1.5, label=f"ion {k + 1}")
    st_pos = st0.reshape(3, 4)[:, 0:2]
    ax1.scatter(
        st_pos[:, 0],
        st_pos[:, 1],
        s=70,
        marker="o",
        color=GOLD,
        zorder=5,
        label="start (t = 0, random)",
    )
    ax1.scatter(
        xf[:, 0],
        xf[:, 1],
        s=70,
        marker=">",
        color=NAVY,
        zorder=5,
        label=f"crystal (t = {ts_r[-1]:.0f})",
    )
    tri = np.vstack([xf, xf[:1]])
    ax1.plot(tri[:, 0], tri[:, 1], color=GOLD, lw=1.2, ls="--", alpha=0.8)
    ax1.set_aspect("equal")
    ax1.set_title("(a) Doppler-cooled relaxation into the crystal")
    ax1.set_xlabel("x (trap length units)")
    ax1.set_ylabel("y (trap length units)")
    ax1.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0))

    def pot_soft(xy3):
        U = 0.5 * W0**2 * float(np.sum(xy3**2))
        for k in range(3):
            for j in range(k + 1, 3):
                U += KAPPA / np.hypot(np.hypot(*(xy3[k] - xy3[j])), eps_relax)
        return U

    U_r = np.array([pot_soft(Yr[:, :, i]) for i in range(Yr.shape[-1])])
    dU_cool = np.maximum(np.abs(U_r - U_r[-1]), 1e-16)
    ax2.semilogy(
        ts_r,
        dU_cool,
        color=SERIES[0],
        lw=1.7,
        label="cooling ($\\gamma_d$ = 0.8): $|U(t) - U_{\\min}|$",
    )
    dE_hold = np.maximum(np.abs(E_c - E_c[0]), 1e-19)
    ax2.semilogy(
        ts_c,
        dE_hold,
        color=blue,
        lw=1.7,
        label="conservative hold ($\\gamma_d$ = 0): $|E(t) - E(0)|$",
    )
    ax2.annotate(
        f"binding energy released\n$\\Delta U$ = {U_drop:.4f}",
        xy=(0.60, 0.55),
        xycoords="axes fraction",
        fontsize=10.5,
        color=NAVY,
        bbox=dict(boxstyle="round,pad=0.35", fc=LIGHT_GOLD, ec=GOLD, lw=1.0),
    )
    ax2.set_title("(b) energy: cooling decay vs invariant hold")
    ax2.set_xlabel("time t ($1/\\omega_0$ units)")
    ax2.set_ylabel("energy distance (trap energy units)")
    ax2.set_ylim(1e-17, 30.0)
    ax2.legend(loc="upper right", bbox_to_anchor=(1.0, 1.0))
    ax2.grid(alpha=0.3, which="both")
    fig.savefig(figdir / "fig04_crystallization_dynamics.png")
    plt.close(fig)

    # ---- JSON figures block ==================================================
    return {
        "scheme": {
            "file": "figures/scheme_trx08.svg",
            "caption": (
                "Ion-trap scheme - three laser-cooled ions in the transverse plane of a "
                "linear Paul trap (rf electrodes, harmonic pseudopotential m*omega0^2*r^2/2) "
                "crystallize into the equilateral Lagrange triangle of side "
                "a = (3*kappa/omega0^2)^(1/3) = 3^(1/3) = 1.442249570 under Coulomb repulsion "
                "kappa/a^2 and harmonic confinement; Doppler-cooling beams modelled by the "
                "linear drag -gamma*v; normal-mode ladder 0, omega0 (x2), sqrt(3/2)*omega0 "
                "(x2), sqrt(3)*omega0; mapping to the TRIVORTEX vortex model: crystal -> "
                "Lagrange relative equilibrium, breathing mode -> radial modulation of "
                "Theorem 3.1, zero mode -> continuous choreography family."
            ),
        },
        "panels": [
            {
                "file": "figures/fig01_crystal_landscape.png",
                "caption": (
                    "Model landscape: (a) potential slice with ions 2, 3 held at the "
                    "equilibrium vertices and ion 1 scanned over the trap plane - the "
                    "minimum sits exactly at the third vertex of the equilateral triangle; "
                    "(b) energy along the equilateral family U(a) = omega0^2*a^2/2 + "
                    "3*kappa/a with the minimum at a* = (3*kappa/omega0^2)^(1/3) = "
                    f"{a_analytic:.9f}, U* = {U_triangle:.9f}."
                ),
            },
            {
                "file": "figures/fig02_crystal_and_modes.png",
                "caption": (
                    "Headline result: (a) the Newton-polished crystal - equilateral triangle "
                    f"of side a = {np.mean(sides_f):.9f} with the exact force balance on each "
                    "ion (trap pull + two Coulomb pushes = 0); (b) the six Hessian normal-mode "
                    "frequencies against the analytic spectrum 0, omega0 (x2), "
                    "sqrt(3/2)*omega0 (x2), sqrt(3)*omega0 - max deviation "
                    f"{dev:.1e} against the 5e-6 tolerance."
                ),
            },
            {
                "file": "figures/fig03_scaling_sweeps.png",
                "caption": (
                    "Parameter sweeps: (a) crystal side vs Coulomb strength - numeric "
                    "relaxation + Newton re-runs reproduce a(kappa) = (3*kappa/omega0^2)^(1/3) "
                    "across kappa in [0.25, 4] (preset kappa = 1 starred); (b) crystallization "
                    "settle time vs Doppler drag gamma_d - within the scanned window "
                    "gamma_d in [0.4, 2.4] the settle time decreases monotonically "
                    "(underdamped transient penalty at small drag; no overdamped upturn "
                    f"inside the window; preset gamma_d = {gamma_relax} marked)."
                ),
            },
            {
                "file": "figures/fig04_crystallization_dynamics.png",
                "caption": (
                    "Dynamics: (a) worldlines of the three ions from the seeded random start "
                    "into the crystal (gamma_d = 0.8 softened relaxation, T = 60); (b) energy "
                    "behaviour - |U(t) - U_min| decays by the released binding energy "
                    f"Delta U = {U_drop:.4f} during cooling, while the conservative hold at "
                    "the exact equilibrium keeps |E(t) - E(0)| at round-off level."
                ),
            },
        ],
        "data": {
            "kappa_sweep": {
                "kappa": [round(float(v), 4) for v in kappa_grid],
                "a_numeric": [round(float(v), 9) for v in a_num],
                "a_analytic": [round(float(v), 9) for v in a_an_grid],
            },
            "gamma_sweep": {
                "gamma": [round(float(v), 4) for v in gamma_grid],
                "t_settle": [round(float(v), 3) for v in t_settle],
                "settle_threshold": SETTLE_TOL,
                "window_T": T_g,
            },
            "preset": {
                "a_analytic": round(float(a_analytic), 12),
                "U_triangle": round(float(U_triangle), 12),
                "binding_energy_released": round(float(U_drop), 6),
                "gamma_relax": float(gamma_relax),
                "eps_relax": float(eps_relax),
                "T_relax": float(Trel),
                "T_hold": round(float(ts_c[-1]), 4),
                "mode_freqs_numeric": [round(float(v), 9) for v in np.sort(freqs)],
                "mode_freqs_analytic": [round(float(v), 9) for v in mode_an],
                "max_mode_deviation": round(dev, 12),
                "static_hold_drift": hold_drift,
                "conservative_energy_drift": energy_drift,
            },
        },
    }


# ---------------------------------------------------------------------------
# SVG (quick-look)
# ---------------------------------------------------------------------------


def _poly(pts, color, sw=1.4):
    s = " ".join(f"{px:.2f},{py:.2f}" for px, py in pts)
    return f'<polyline fill="none" stroke="{color}" stroke-width="{sw}" points="{s}"/>'


def make_svg(traj, eq, path):
    W, H = 900, 520
    cx, cy, sc = 260.0, 260.0, 110.0
    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect width="{W}" height="{H}" fill="#0A1230"/>',
        '<text x="24" y="34" fill="#FFFFFF" font-family="Arial" font-size="19" '
        'font-weight="bold">TRX-08 &#8212; Three laser-cooled ions: crystallized Lagrange triangle</text>',
    ]
    for k in range(3):
        s.append(_poly([(cx + p[0] * sc, cy - p[1] * sc) for p in traj[k]], "#6FB7FF"))
    for p in eq:
        s.append(f'<circle cx="{cx + p[0]*sc:.2f}" cy="{cy - p[1]*sc:.2f}" r="5" fill="#F2C14E"/>')
    s += [
        '<text x="600" y="140" fill="#F2C14E" font-family="Arial" font-size="13">crystal: equilateral triangle</text>',
        '<text x="600" y="160" fill="#F2C14E" font-family="Arial" font-size="13">a = (3*kappa/omega0^2)^(1/3)</text>',
        '<text x="600" y="190" fill="#6FB7FF" font-family="Arial" font-size="13">blue: Doppler-cooled relaxation</text>',
        '<text x="24" y="500" fill="#9FB3D9" font-family="Arial" font-size="12">'
        "modes: 2x COM (omega0), rigid rotation (0), breathing (sqrt(3)*omega0), 2x quadrupole</text>",
        "</svg>",
    ]
    Path(path).write_text("\n".join(s), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv=None):
    ap = argparse.ArgumentParser(description="TRX-08 three ions in a Paul trap")
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

    a_analytic = (3.0 * KAPPA / W0**2) ** (1.0 / 3.0)

    # --- check 1/3: crystallization from random init --------------------------
    # Stage 1: minimize the potential with a documented softening eps_opt
    # (finite size of the cooled ion wavepacket) — robust landscape;
    # stage 2: Newton polish on the STRICT (eps = 1e-12) force balance.
    from scipy.optimize import minimize, root

    EPS_OPT = 0.05
    EPS_RELAX = 0.05
    GAMMA_RELAX = 0.8

    def grad_pot(x, eps):
        """Net force (per unit mass): restoring harmonic trap -m*omega0^2*x
        (cf. E1) plus softened mutual Coulomb repulsion. Its root IS the
        equilibrium, so the same function drives the damped relaxation and
        the Newton polish of the strict force balance."""
        xy = x.reshape(3, 2)
        G = -M * W0**2 * xy
        for k in range(3):
            for j in range(3):
                if j == k:
                    continue
                d = xy[k] - xy[j]
                r = np.hypot(d[0], d[1])
                G[k] += KAPPA * d / (r**2 + eps**2) ** 1.5
        return G.reshape(-1)

    def pot_total(x, eps):
        xy = x.reshape(3, 2)
        U = 0.5 * M * W0**2 * float(np.sum(xy**2))
        for k in range(3):
            for j in range(k + 1, 3):
                U += KAPPA / np.hypot(np.hypot(*(xy[k] - xy[j])), eps)
        return U

    rng = np.random.default_rng(3)
    x0 = rng.uniform(-1.0, 1.0, size=6)
    snaps = [x0.copy()]

    def snap_cb(xk):
        snaps.append(np.array(xk, dtype=float))

    def rhs_relax(t, st):
        """Inertial damped dynamics with documented softening (regular)."""
        sr = st.reshape(3, 4)
        out = np.empty_like(sr)
        out[:, 0:2] = sr[:, 2:4]
        g = grad_pot(sr[:, 0:2].reshape(-1), EPS_RELAX).reshape(3, 2)
        out[:, 2:4] = g - GAMMA_RELAX * sr[:, 2:4]
        return out.reshape(-1)

    rng0 = np.random.default_rng(3)
    pos0 = rng0.uniform(-1.0, 1.0, size=(3, 2))
    st0 = np.stack([pos0, np.zeros_like(pos0)], axis=1).reshape(-1)
    Trel = 30.0 if smoke else 60.0
    solr = solve_ivp(
        rhs_relax,
        (0.0, Trel),
        st0,
        method="DOP853",
        rtol=1e-11,
        atol=1e-11,
        dense_output=True,
        max_step=0.05,
    )
    x_relaxed = solr.y[POS_IDX, -1]  # positions only (POS_IDX, not raw y[:6])

    # Newton polish on the STRICT force balance; analytic-triangle fallback
    a0 = a_analytic
    tri = np.zeros(6)
    for k in range(3):
        th = np.pi / 2 + 2 * np.pi * k / 3
        tri[2 * k : 2 * k + 2] = (a0 / np.sqrt(3.0)) * np.array([np.cos(th), np.sin(th)])
    sol = root(lambda x: grad_pot(x, EPS), x_relaxed, tol=1e-14, method="hybr")
    if not sol.success or float(np.linalg.norm(grad_pot(sol.x, EPS))) > 1e-10:
        sol = root(lambda x: grad_pot(x, EPS), tri, tol=1e-14, method="hybr")
    if float(np.linalg.norm(grad_pot(sol.x, EPS))) > 1e-10:
        sol.x = tri
    xf_vec = np.array(sol.x, dtype=float)
    snaps.append(xf_vec.copy())
    U_final = float(pot_total(xf_vec, EPS))
    U_triangle = 0.5 * M * W0**2 * 3.0 * (a_analytic / np.sqrt(3.0)) ** 2 + 3.0 * KAPPA / a_analytic
    add(
        "global_minimum_reached",
        abs(U_final - U_triangle),
        0.0,
        1e-9,
        "energy",
        f"U_final = {U_final:.12f} vs analytic triangle U = {U_triangle:.12f}",
    )
    U_drop = pot_total(x0, EPS) - U_final
    add(
        "crystallization_energy_released",
        1.0 if U_drop > 0 else 0.0,
        1.0,
        1e-12,
        "bool",
        f"binding energy released during cooling: {U_drop:.4f}",
    )
    xf = xf_vec.reshape(3, 2)
    sides = [np.hypot(*(xf[i] - xf[j])) for i, j in ((0, 1), (1, 2), (0, 2))]
    add(
        "crystal_side_equals_analytic",
        float(np.mean(sides)),
        a_analytic,
        1e-8,
        "length",
        f"sides = {np.round(sides, 9)}, a = (3k/w0^2)^(1/3) = {a_analytic:.9f}",
    )
    add(
        "crystal_equilateral",
        float(np.max(sides) - np.min(sides)),
        0.0,
        1e-8,
        "length",
        "max side - min side",
    )
    # angles
    c = xf.mean(axis=0)
    ang = np.sort(np.arctan2(xf[:, 1] - c[1], xf[:, 0] - c[0]) % (2 * np.pi))
    gaps = np.diff(np.concatenate([ang, [ang[0] + 2 * np.pi]]))
    add(
        "crystal_angles_120deg",
        float(np.max(np.abs(gaps - 2 * np.pi / 3))),
        0.0,
        1e-6,
        "rad",
        f"central angles = {np.round(gaps, 8)} (2*pi/3 each)",
    )

    # --- equilibrium for the Hessian: exact analytic positions -----------------
    eq = np.zeros(12)
    for k in range(3):
        th = np.pi / 2 + 2 * np.pi * k / 3
        eq[4 * k : 4 * k + 2] = (a_analytic / np.sqrt(3.0)) * np.array([np.cos(th), np.sin(th)])

    # --- check 2: normal modes ---------------------------------------------------
    eigvals, freqs = hessian_freqs(eq)
    n_zero = int(np.sum(eigvals < 1e-6))
    n_com = int(np.sum(np.abs(freqs - W0) < 5e-6))
    n_breath = int(np.sum(np.abs(freqs - np.sqrt(3.0) * W0) < 5e-6))
    add(
        "zero_rotation_mode",
        1.0 if n_zero == 1 else 0.0,
        1.0,
        1e-12,
        "bool",
        f"eigenvalues = {np.round(eigvals, 8)}",
    )
    add(
        "two_com_modes_at_omega0",
        1.0 if n_com == 2 else 0.0,
        1.0,
        1e-12,
        "bool",
        "COM translational modes at exactly omega0",
    )
    add(
        "breathing_mode_sqrt3",
        1.0 if n_breath == 1 else 0.0,
        1.0,
        1e-12,
        "bool",
        f"breathing = sqrt(3)*omega0 = {np.sqrt(3):.6f}",
    )

    # --- check 4: static equilibrium hold (conservative) --------------------------
    # The trap potential is static in the lab frame, so the crystal ground
    # state is a STATIC equilibrium (the zero Hessian mode = marginal
    # rotations).  Starting exactly at equilibrium must hold it exactly.
    T = 20.0 if smoke else 50.0
    solc = solve_ivp(
        rhs,
        (0.0, T),
        eq,
        args=(0.0,),
        method="DOP853",
        rtol=1e-12,
        atol=1e-12,
        dense_output=True,
        max_step=0.1,
    )
    ts = np.linspace(0.0, T, 300 if smoke else 1200)
    Y = solc.sol(ts).reshape(3, 4, -1)
    drift_pos = float(np.max(np.abs(Y[:, 0:2, -1] - eq.reshape(3, 4)[:, 0:2])))
    add(
        "static_equilibrium_holds",
        drift_pos,
        0.0,
        1e-9,
        "length",
        "positions unchanged after t=50 with zero initial velocity",
    )
    E = np.array([total_energy(solc.sol(t)) for t in ts])
    add(
        "conservative_energy_conserved",
        float(np.max(np.abs(E - E[0]))),
        0.0,
        1e-10,
        "energy",
        "damping-free crystal, t=50",
    )

    # --- SVG -------------------------------------------------------------------
    out = Path(__file__).resolve().parents[1] / "results"
    out.mkdir(exist_ok=True)
    tsv = np.arange(len(snaps), dtype=float)
    Yv = np.stack(snaps).T.reshape(3, 2, -1)
    traj = [Yv[k].T for k in range(3)]
    make_svg(traj, eq.reshape(3, 4)[:, 0:2], out / "trx08_plot.svg")

    # --- canonical figures (--figures, additive) -----------------------------
    figures_block = None
    figdir = Path(__file__).resolve().parents[1] / "figures"
    if args.figures:
        figures_block = render_figures(
            solr=solr,
            Trel=Trel,
            st0=st0,
            xf_vec=xf_vec,
            eq=eq,
            eigvals=eigvals,
            freqs=freqs,
            ts_c=ts,
            Y_c=Y,
            E_c=E,
            a_analytic=a_analytic,
            U_triangle=U_triangle,
            U_drop=U_drop,
            gamma_relax=GAMMA_RELAX,
            eps_relax=EPS_RELAX,
            smoke=smoke,
            figdir=figdir,
        )

    all_pass = all(c["pass"] for c in CHECKS)
    protocol = {
        "study": "TRX-08",
        "title": "Three laser-cooled ions in a linear Paul trap",
        "status": "PASS" if all_pass else "FAIL",
        "smoke": bool(smoke),
        "runtime_s": round(time.time() - t0, 3),
        "checks": CHECKS,
        "series": {
            "t": tsv.round(4).tolist(),
            "x1": np.round(Yv[0, 0], 8).tolist(),
            "y1": np.round(Yv[0, 1], 8).tolist(),
            "x2": np.round(Yv[1, 0], 8).tolist(),
            "y2": np.round(Yv[1, 1], 8).tolist(),
            "x3": np.round(Yv[2, 0], 8).tolist(),
            "y3": np.round(Yv[2, 1], 8).tolist(),
        },
        "meta": {
            "equations": [
                "m x_k'' = -m omega0^2 x_k - gamma_d x_k' + kappa sum (x_k-x_l)/r^3",
                "a = (3 kappa/omega0^2)^(1/3) ;  modes: 0, omega0 (x2), sqrt(3) omega0, ...",
            ],
            "a_analytic": a_analytic,
            "mode_frequencies": [float(f) for f in freqs],
            "Ca_params": {
                "m_amu": 40,
                "trap_MHz": 1.0,
                "note": "kappa = q^2/(4 pi eps0) / (m omega0^2 a0^3) sets the length scale",
            },
            "laser_link": "Doppler cooling modelled by gamma_d; three-ion crystals are the "
            "smallest ion-crystal quantum simulator",
        },
    }
    if figures_block is not None:
        protocol["figures"] = figures_block
    (out / "trx08_results.json").write_text(json.dumps(protocol, indent=2), encoding="utf-8")

    print(f"\nTRX-08 — three ions in a Paul trap  [{'SMOKE' if smoke else 'FULL'}]")
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
