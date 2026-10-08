#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
POLYVORTEX — THE FIGURE FACTORY (300 dpi PNG + the scheme SVG)
============================================================================
Generates the publication figures of the mini-repository from the committed
JSON protocols in `results/protocols/` — the same "bound to a run"
discipline as the monograph: every plotted register is read from a
protocol file, never re-invented. The two illustrative panels of fig01
(trajectories of the two layers) are recomputed from the model modules,
which is by design: they are pictures of solutions, not registers.

    make figures                       # from the mini-repository root
    python3 -m polyvortex.figures     # equivalent, PYTHONPATH=python

Outputs into `polyvortex/figures/`:

    fig01_two_layers.png             Layer G rosette vs Layer K rigid ring
    fig02_ring_rotation.png          W2: omega_N analytic vs measured + band
    fig03_stability_scan.png         W4: Havelock threshold N<=7 / N>=8
    fig04_admissibility_bridge.png   W5/W7: the pi*ln2 boundary + T_comp
    scheme_polyvortex.svg            the mini-repository architecture

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from . import ansatz as an  # noqa: E402
from . import classical as cl  # noqa: E402
from . import model as md  # noqa: E402

# The mini-repository palette (matches the parent TRIVORTEX brand)
NAVY = "#0A1A3A"
STEEL = "#2E5FA3"
SKY = "#7FA6D9"
CRIMSON = "#B03A2E"
GREEN = "#1E8449"
LIGHT = "#F4F6FA"
GRID = "#D5DCE8"

PACKAGE_DIR = Path(__file__).resolve().parent
MINIROOT = PACKAGE_DIR.parents[1]
DEFAULT_PROTOS = MINIROOT / "results" / "protocols"
DEFAULT_OUT = MINIROOT / "figures"


def _proto(stage: str, proto_dir: Path) -> Dict:
    """Load a committed W-protocol JSON (the figure's numeric oracle)."""
    path = proto_dir / f"{stage}_default.json"
    if not path.exists():
        raise SystemExit(
            f"missing protocol {path} — run `make ladder` first "
            "(the figures are bound to the committed protocols)"
        )
    with path.open("r", encoding="utf-8") as fh:
        data: Dict = json.load(fh)
    return data


def _style_axis(ax: plt.Axes) -> None:
    """The common look: navy spines, soft grid, tick direction in."""
    for spine in ax.spines.values():
        spine.set_color(NAVY)
        spine.set_linewidth(0.8)
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.tick_params(colors=NAVY, labelsize=9, direction="in")
    ax.set_axisbelow(True)


def _save(fig: plt.Figure, out_dir: Path, name: str) -> str:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / name
    fig.savefig(path, dpi=300)
    plt.close(fig)
    return str(path)


# ---------------------------------------------------------------------------
# fig01 — the two layers (illustrative trajectories)
# ---------------------------------------------------------------------------


def fig01_two_layers(out_dir: Path) -> str:
    """Left: the Layer-G closed form (N=3, C_Ch=3 — admissible).
    Right: the Layer-K rigid ring (N=7) rotating at the Theorem-A rate."""
    fig, (axg, axk) = plt.subplots(1, 2, figsize=(10.0, 4.4), constrained_layout=True)

    # --- Layer G: the generalized closed form, N = 3, C_Ch = 3 ---
    # Along H1 the radius and the angle share one phase, r_k = sqrt(C_Ch)
    # (1 + eps cos theta_k): every vortex rides the SAME limacon curve,
    # phase-shifted along it — the honest picture of the choreography.
    c_ch, t_period, n = 3.0, 2.0 * math.pi, 3
    omega = an.ansatz_frequency(c_ch, t_period)
    t_r = 2.0 * math.pi / omega
    eps = an.ansatz_amplitude(c_ch)
    r0 = math.sqrt(c_ch)
    th_grid = np.linspace(0.0, 2.0 * math.pi, 720)
    r_grid = r0 * (1.0 + eps * np.cos(th_grid))
    axg.plot(
        r_grid * np.cos(th_grid),
        r_grid * np.sin(th_grid),
        color=SKY,
        lw=6.0,
        alpha=0.45,
        label="shared orbit r(θ)",
    )
    for rad, ls in ((r0 * (1.0 + eps), ":"), (r0 * (1.0 - eps), ":")):
        circ = np.linspace(0.0, 2.0 * math.pi, 200)
        axg.plot(
            rad * np.cos(circ),
            rad * np.sin(circ),
            ls=ls,
            color=NAVY,
            lw=0.8,
            alpha=0.6,
        )
    colors = (STEEL, CRIMSON, GREEN)
    frac = np.linspace(0.0, 0.22, 60)  # short initial trails
    for k in range(n):
        xs: List[float] = []
        ys: List[float] = []
        for f in frac:
            st = an.ansatz_state(float(f * t_r), c_ch, t_period, n)
            xs.append(float(st[2 * k]))
            ys.append(float(st[2 * k + 1]))
        axg.plot(xs, ys, color=colors[k], lw=1.8, alpha=0.85, label=f"vortex {k}")
        st0 = an.ansatz_state(0.0, c_ch, t_period, n)
        axg.plot(
            [float(st0[2 * k])],
            [float(st0[2 * k + 1])],
            "o",
            color=colors[k],
            ms=8,
            mec=NAVY,
            mew=0.9,
            zorder=5,
        )
    axg.text(
        0.02,
        0.02,
        "one limacon r(θ)=√C(1+ε·cosθ), three riders at 2π/3;\n"
        "dotted circles: r_min=√C(1−ε)>0, r_max=√C(1+ε)",
        transform=axg.transAxes,
        fontsize=7.6,
        color=NAVY,
        va="bottom",
    )
    axg.set_title(
        f"(a) Layer G — the closed form (N=3, $C_{{Ch}}$=3, $\\varepsilon$={eps:.3f})",
        fontsize=10.5,
        color=NAVY,
    )
    axg.set_xlabel("x")
    axg.set_ylabel("y")
    axg.set_aspect("equal")
    axg.legend(loc="upper left", fontsize=8, framealpha=0.9, edgecolor=GRID)

    # --- Layer K: the rigid ring, N = 7, R = 1, Gamma = 1 ---
    n_k, big_r, gamma = 7, 1.0, 1.0
    om_k = cl.ngon_omega(gamma, big_r, n_k)
    gamma_vec = np.full(n_k, gamma)
    dt = (2.0 * math.pi / om_k) / 1200.0
    n_steps = int(2 * 1200)
    state = cl.ngon_initial(n_k, big_r)
    trail = np.zeros((n_steps + 1, 2 * n_k))
    trail[0] = state
    for i in range(n_steps):
        state = md.rk4_step(state, gamma_vec, dt)
        trail[i + 1] = state
    for k in range(n_k):
        axk.plot(trail[:, 2 * k], trail[:, 2 * k + 1], color=SKY, lw=1.0)
    start = cl.ngon_initial(n_k, big_r)
    xy0 = start.reshape(n_k, 2)
    poly = plt.Polygon(xy0, closed=True, facecolor=LIGHT, edgecolor=STEEL, lw=1.2)
    axk.add_patch(poly)
    axk.plot(xy0[:, 0], xy0[:, 1], "o", color=STEEL, ms=5, mec=NAVY, mew=0.6)
    axk.set_title(
        "(b) Layer K — the rigid $N$-gon ring (N=7, $\\omega_N$=6/4$\\pi$)",
        fontsize=10.5,
        color=NAVY,
    )
    axk.set_xlabel("x")
    axk.set_ylabel("y")
    axk.set_aspect("equal")

    for ax in (axg, axk):
        _style_axis(ax)
    return _save(fig, out_dir, "fig01_two_layers.png")


# ---------------------------------------------------------------------------
# fig02 — W2: the rigid rotation register
# ---------------------------------------------------------------------------


def fig02_ring_rotation(out_dir: Path, proto_dir: Path) -> str:
    """(a) omega_N analytic vs measured for N=2..8; (b) the relative-error
    band against the parent tolerance 1e-6."""
    data = _proto("W2_ring_rotation", proto_dir)["check"]
    per_n = data["per_N"]
    ns = [int(row["N"]) for row in per_n]
    analytic = [float(row["omega_analytic"]) for row in per_n]
    measured = [float(row["omega_measured"]) for row in per_n]
    rel = [float(row["omega_relative_error"]) for row in per_n]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 4.2), constrained_layout=True)

    n_fine = np.linspace(2, 8, 200)
    ax1.plot(
        n_fine,
        [float(x - 1.0) / (4.0 * math.pi) for x in n_fine],
        color=STEEL,
        lw=1.8,
        label=r"analytic $\omega_N=\Gamma(N-1)/(4\pi R^2)$",
    )
    ax1.plot(
        ns,
        measured,
        "o",
        color=CRIMSON,
        ms=7,
        mec=NAVY,
        mew=0.8,
        label="measured (RK4, 2 rotations)",
    )
    ax1.set_title("(a) rigid rotation rate of the N-gon", fontsize=10.5, color=NAVY)
    ax1.set_xlabel("N")
    ax1.set_ylabel(r"$\omega_N$")
    ax1.set_xticks(list(ns))
    ax1.legend(fontsize=8, framealpha=0.9, edgecolor=GRID)

    floor = 1e-17
    vals = [max(v, floor) for v in rel]
    ax2.semilogy(ns, vals, "s", color=STEEL, ms=7, mec=NAVY, mew=0.8)
    ax2.axhline(1e-6, color=CRIMSON, ls="--", lw=1.2)
    ax2.text(
        2.1,
        2.2e-6,
        "parent tolerance band 1e-6",
        fontsize=8.5,
        color=CRIMSON,
    )
    ax2.axhline(2.9e-12, color=GREEN, ls=":", lw=1.2)
    ax2.text(
        4.4,
        1.1e-12,
        "registered worst case 2.9e-12",
        fontsize=8.5,
        color=GREEN,
    )
    ax2.set_ylim(1e-14, 1e-4)
    ax2.set_title("(b) measured vs analytic: relative error", fontsize=10.5, color=NAVY)
    ax2.set_xlabel("N")
    ax2.set_ylabel(r"$|\omega_{meas}-\omega_N|/\omega_N$")
    ax2.set_xticks(list(ns))

    for ax in (ax1, ax2):
        _style_axis(ax)
    return _save(fig, out_dir, "fig02_ring_rotation.png")


# ---------------------------------------------------------------------------
# fig03 — W4: the Havelock stability threshold
# ---------------------------------------------------------------------------


def fig03_stability_scan(out_dir: Path, proto_dir: Path) -> str:
    """(a) max Re(lambda) vs N with the 1e-7 classifier; (b) the co-rotating
    spectra of the boundary pair N=7 / N=8 in the complex plane."""
    data = _proto("W4_stability", proto_dir)["check"]
    per_n = {int(row["N"]): row for row in data["per_N"]}
    ns = sorted(per_n)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 4.4), constrained_layout=True)

    floor = 1e-17
    xs: List[int] = []
    ys: List[float] = []
    for n in ns:
        v = float(per_n[n]["max_Re_lambda"])
        xs.append(n)
        ys.append(max(v, floor))
    colors = [STEEL if n <= 7 else CRIMSON for n in xs]
    ax1.bar(xs, ys, color=colors, edgecolor=NAVY, linewidth=0.6, width=0.62)
    ax1.set_yscale("log")
    ax1.axhline(1e-7, color=NAVY, ls="--", lw=1.2)
    ax1.text(2.05, 2.4e-7, "stability classifier 1e-7", fontsize=8.5, color=NAVY)
    ax1.annotate(
        "N=8: +0.4502\n(unstable, Havelock)",
        xy=(8, 0.4502),
        xytext=(5.6, 0.02),
        fontsize=8.5,
        color=CRIMSON,
        arrowprops={"arrowstyle": "->", "color": CRIMSON, "lw": 1.0},
    )
    ax1.text(
        2.0,
        2.5e-4,
        "stable cases (N≤7) sit on the\ndefective-zero noise floor",
        fontsize=8.5,
        color=STEEL,
    )
    ax1.set_ylim(1e-18, 3.0)
    ax1.set_xticks(xs)
    ax1.set_title("(a) max Re$\\,\\lambda$ of the co-rotating spectrum", fontsize=10.5, color=NAVY)
    ax1.set_xlabel("N")
    ax1.set_ylabel(r"$\max\,\mathrm{Re}\,\lambda$")

    for n, marker, color, label in (
        (7, "o", STEEL, "N=7 (stable)"),
        (8, "x", CRIMSON, "N=8 (unstable)"),
    ):
        spec = per_n[n]["spectrum_re_im"]
        re_part = [float(z[0]) for z in spec]
        im_part = [float(z[1]) for z in spec]
        ax2.scatter(re_part, im_part, s=46, marker=marker, color=color, label=label, alpha=0.85)
    ax2.axvline(0.0, color=GRID, lw=1.0)
    ax2.set_title("(b) spectra at the threshold pair", fontsize=10.5, color=NAVY)
    ax2.set_xlabel("Re $\\lambda$")
    ax2.set_ylabel("Im $\\lambda$")
    ax2.legend(fontsize=8, framealpha=0.9, edgecolor=GRID, loc="upper left")

    for ax in (ax1, ax2):
        _style_axis(ax)
    return _save(fig, out_dir, "fig03_stability_scan.png")


# ---------------------------------------------------------------------------
# fig04 — W5/W7: admissibility and the D1 bridge
# ---------------------------------------------------------------------------


def fig04_admissibility_bridge(out_dir: Path, proto_dir: Path) -> str:
    """(a) the amplitude law eps(C_Ch) with the exact boundary pi*ln(2);
    (b) the D1 compatibility periods T_comp(N, C_Ch) from the W7 protocol."""
    data_w7 = _proto("W7_bridge", proto_dir)["check"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 4.2), constrained_layout=True)

    star = an.C_CH_STAR
    grid = np.linspace(0.5, 10.0, 600)
    eps_vals = np.array([an.ansatz_amplitude(float(c)) for c in grid])
    ax1.plot(grid, eps_vals, color=STEEL, lw=1.8, label=r"$\varepsilon(C_{Ch})$")
    ax1.axhline(1.0, color=NAVY, ls="--", lw=1.1)
    ax1.axvline(star, color=CRIMSON, ls="-", lw=1.3)
    ax1.axvspan(0.5, star, color=CRIMSON, alpha=0.07)
    ax1.axvspan(star, 10.0, color=GREEN, alpha=0.06)
    ax1.plot([star], [1.0], "o", color=CRIMSON, ms=7, mec=NAVY, mew=0.8)
    ax1.plot([1.0], [an.ansatz_amplitude(1.0)], "s", color=NAVY, ms=6)
    ax1.annotate(
        "parent default\n$C_{Ch}=1$ (below)",
        xy=(1.0, an.ansatz_amplitude(1.0)),
        xytext=(1.9, 3.4),
        fontsize=8.5,
        color=NAVY,
        arrowprops={"arrowstyle": "->", "color": NAVY, "lw": 0.9},
    )
    ax1.annotate(
        r"$C_{Ch}^{*}=\pi\ln 2$" + f"\n= {star:.9f}",
        xy=(star, 1.0),
        xytext=(3.6, 1.7),
        fontsize=8.5,
        color=CRIMSON,
        arrowprops={"arrowstyle": "->", "color": CRIMSON, "lw": 0.9},
    )
    ax1.text(0.75, 0.42, "degenerate:\nr crosses 0", fontsize=8.5, color=CRIMSON)
    ax1.text(6.4, 1.55, "admissible:\n$\\varepsilon<1$", fontsize=8.5, color=GREEN)
    ax1.set_xlim(0.5, 10.0)
    ax1.set_ylim(0.0, 4.2)
    ax1.set_title("(a) admissibility of the closed form (Theorem B)", fontsize=10.5, color=NAVY)
    ax1.set_xlabel(r"$C_{Ch}$")
    ax1.set_ylabel(r"$\varepsilon$")
    ax1.legend(loc="upper right", fontsize=8, framealpha=0.9, edgecolor=GRID)

    series: Dict[int, List[Tuple[float, float]]] = {}
    for row in data_w7["compatibility_table"]:
        if not row.get("admissible") or "T_comp" not in row:
            continue
        n = int(row["N"])
        series.setdefault(n, []).append((float(row["C_Ch"]), float(row["T_comp"])))
    shades = [STEEL, SKY, GREEN, CRIMSON, NAVY, "#8E44AD"]
    for (n, pts), color in zip(sorted(series.items()), shades):
        pts.sort()
        ax2.plot(
            [p[0] for p in pts],
            [p[1] for p in pts],
            "o-",
            color=color,
            lw=1.4,
            ms=5,
            mec=NAVY,
            mew=0.5,
            label=f"N={n}",
        )
    ax2.set_yscale("log")
    ax2.set_title(
        "(b) the D1 compatibility periods $T_{comp}(N, C_{Ch})$", fontsize=10.5, color=NAVY
    )
    ax2.set_xlabel(r"$C_{Ch}$")
    ax2.set_ylabel(r"$T_{comp}$")
    ax2.legend(fontsize=8, ncol=2, framealpha=0.9, edgecolor=GRID)

    for ax in (ax1, ax2):
        _style_axis(ax)
    return _save(fig, out_dir, "fig04_admissibility_bridge.png")


# ---------------------------------------------------------------------------
# scheme — the mini-repository architecture (hand-authored SVG)
# ---------------------------------------------------------------------------

SCHEME_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="940" height="470" viewBox="0 0 940 470">
  <defs>
    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{navy}"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="940" height="470" fill="#FFFFFF"/>
  <text x="470" y="30" text-anchor="middle" font-family="Liberation Sans, Arial" font-size="19" font-weight="bold" fill="{navy}">POLYVORTEX — the N-vortex extension bench (mini-repository)</text>

  <rect x="30" y="60" width="200" height="120" rx="8" fill="{light}" stroke="{steel}" stroke-width="1.4"/>
  <text x="130" y="86" text-anchor="middle" font-family="Liberation Sans, Arial" font-size="13" font-weight="bold" fill="{navy}">Inputs</text>
  <text x="130" y="108" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="12" fill="{navy}">N, Γ, R — the ring</text>
  <text x="130" y="128" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="12" fill="{navy}">C_Ch, T — the gauge pair</text>
  <text x="130" y="148" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="12" fill="{navy}">q_k — topological charges</text>
  <text x="130" y="168" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11" fill="{steel}">presets: quick / default / full</text>

  <rect x="330" y="52" width="280" height="66" rx="8" fill="#FFFFFF" stroke="{steel}" stroke-width="1.4"/>
  <text x="470" y="76" text-anchor="middle" font-family="Liberation Sans, Arial" font-size="13" font-weight="bold" fill="{navy}">Layer K — model.py</text>
  <text x="470" y="98" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">Kirchhoff RHS · RK4 · H, P, Q, I · Jacobian</text>

  <rect x="330" y="128" width="280" height="62" rx="8" fill="#FFFFFF" stroke="{steel}" stroke-width="1.4"/>
  <text x="470" y="151" text-anchor="middle" font-family="Liberation Sans, Arial" font-size="13" font-weight="bold" fill="{navy}">Layer G — ansatz.py · classical.py</text>
  <text x="470" y="173" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">closed form (H1) · ω_N · chords · unwrap</text>

  <rect x="660" y="60" width="250" height="120" rx="8" fill="{light}" stroke="{steel}" stroke-width="1.4"/>
  <text x="785" y="86" text-anchor="middle" font-family="Liberation Sans, Arial" font-size="13" font-weight="bold" fill="{navy}">W-ladder — ladder.py</text>
  <text x="785" y="107" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">W1 anchor · W2 rotation · W3 invariants</text>
  <text x="785" y="126" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">W4 stability · W5 admissibility</text>
  <text x="785" y="145" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">W6 obstruction · W7 bridge (D1)</text>
  <text x="785" y="166" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11" fill="{steel}">tolerances: 1e-12 … 1e-6</text>

  <rect x="240" y="230" width="460" height="64" rx="8" fill="#FFFFFF" stroke="{navy}" stroke-width="1.6"/>
  <text x="470" y="254" text-anchor="middle" font-family="Liberation Sans, Arial" font-size="13" font-weight="bold" fill="{navy}">results/protocols/W1..W7_*.json — committed, deterministic</text>
  <text x="470" y="276" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">"every number is bound to a run" — re-derived by the 26-test guard</text>

  <rect x="60" y="330" width="380" height="100" rx="8" fill="{light}" stroke="{steel}" stroke-width="1.4"/>
  <text x="250" y="356" text-anchor="middle" font-family="Liberation Sans, Arial" font-size="13" font-weight="bold" fill="{navy}">figures/ — this module</text>
  <text x="250" y="378" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">fig01 two layers · fig02 rotation · fig03 stability</text>
  <text x="250" y="397" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">fig04 admissibility + D1 · scheme_polyvortex.svg</text>
  <text x="250" y="416" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11" fill="{steel}">300 dpi PNG, bound to the protocols</text>

  <rect x="500" y="330" width="380" height="100" rx="8" fill="{light}" stroke="{steel}" stroke-width="1.4"/>
  <text x="690" y="356" text-anchor="middle" font-family="Liberation Sans, Arial" font-size="13" font-weight="bold" fill="{navy}">docs/ — the publication stack</text>
  <text x="690" y="378" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">monograph/ (RU+EN, md+docx+pdf) — the big monograph</text>
  <text x="690" y="397" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11.5" fill="{navy}">monographs/ — Theorems A, B, E · Lemmas C, D (RU+EN)</text>
  <text x="690" y="416" text-anchor="middle" font-family="Liberation Serif, Georgia" font-size="11" fill="{steel}">Theorems B, C-proof, D-proof feed TB1–TW5 / T1, T3, T5</text>

  <line x1="230" y1="120" x2="322" y2="90" stroke="{navy}" stroke-width="1.3" marker-end="url(#arr)"/>
  <line x1="230" y1="130" x2="322" y2="155" stroke="{navy}" stroke-width="1.3" marker-end="url(#arr)"/>
  <line x1="610" y1="90" x2="652" y2="110" stroke="{navy}" stroke-width="1.3" marker-end="url(#arr)"/>
  <line x1="610" y1="160" x2="652" y2="135" stroke="{navy}" stroke-width="1.3" marker-end="url(#arr)"/>
  <line x1="785" y1="180" x2="700" y2="228" stroke="{navy}" stroke-width="1.3" marker-end="url(#arr)"/>
  <line x1="470" y1="116" x2="470" y2="126" stroke="{navy}" stroke-width="0"/>
  <line x1="380" y1="294" x2="250" y2="326" stroke="{navy}" stroke-width="1.3" marker-end="url(#arr)"/>
  <line x1="560" y1="294" x2="690" y2="326" stroke="{navy}" stroke-width="1.3" marker-end="url(#arr)"/>
</svg>
"""


def scheme_svg(out_dir: Path) -> str:
    """Write the architecture scheme (SVG, vector)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "scheme_polyvortex.svg"
    svg = SCHEME_TEMPLATE.format(navy=NAVY, steel=STEEL, light=LIGHT)
    path.write_text(svg, encoding="utf-8")
    return str(path)


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------

FIGNAMES = (
    "fig01_two_layers.png",
    "fig02_ring_rotation.png",
    "fig03_stability_scan.png",
    "fig04_admissibility_bridge.png",
    "scheme_polyvortex.svg",
)


def build_all(out_dir: Path = DEFAULT_OUT, proto_dir: Path = DEFAULT_PROTOS) -> List[str]:
    """Generate every figure; returns the list of written paths."""
    made: List[str] = []
    made.append(fig01_two_layers(out_dir))
    made.append(fig02_ring_rotation(out_dir, proto_dir))
    made.append(fig03_stability_scan(out_dir, proto_dir))
    made.append(fig04_admissibility_bridge(out_dir, proto_dir))
    made.append(scheme_svg(out_dir))
    return made


def main() -> None:
    parser = argparse.ArgumentParser(description="POLYVORTEX figure factory")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="output directory")
    parser.add_argument(
        "--protocols", type=Path, default=DEFAULT_PROTOS, help="protocols directory"
    )
    args = parser.parse_args()
    for path in build_all(args.out, args.protocols):
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
