#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
CYCLORING — THE FIGURE FACTORY (bilingual: EN primary + RU mirror, 300 dpi)
============================================================================
Generates the publication figures of the mini-repository from the committed
JSON protocols in results/protocols/ — the "bound to a run" discipline:
every plotted register is read from a protocol file, never re-invented.
The trajectory panels are recomputed from the model modules by design:
they are pictures of the program, not registers.

Two language editions are produced in one pass (the repository convention:
English is the primary edition, Russian is the full-fidelity mirror):

    figures/            ← the English primary set (embedded by README.md)
    figures/ru/         ← the Russian mirror set (embedded by README_RU.md)

    make figures                        # from the mini-repository root
    python3 -m cycloring.figures        # equivalent, PYTHONPATH=python
    python3 -m cycloring.figures --lang en   # one edition only

Outputs per edition:

    fig01_periods_lattice.png   W1/W2: the period field of the level N=15
    fig02_transducer.png        W7: the defect chain and the stiffness law
    fig03_breathing.png         W6: the synchronous-breathing rosettes
    fig04_transport_law.png     W5: the mean-transport identity
    fig05_dichotomy.png         W2/W3/W4: algebraic vs transcendental
    scheme_cycloring.svg        the research architecture

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Dict, Tuple

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from . import chain as ch  # noqa: E402
from . import periods as per  # noqa: E402
from . import ring as rg  # noqa: E402

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

# The language editions and their output subdirectories (relative to out_dir).
# English is the primary edition; Russian lives in the ru/ mirror folder.
LANG_DIRS: Dict[str, str] = {"en": "", "ru": "ru"}


def _t(key: str, lang: str) -> str:
    """The bilingual string lookup: TEXTS[key] = (english, russian)."""
    en, ru = TEXTS[key]
    return en if lang == "en" else ru


# ---------------------------------------------------------------------------
# The bilingual string table — every figure label of the factory
# ---------------------------------------------------------------------------

TEXTS: Dict[str, Tuple[str, str]] = {
    # fig01 — the period field
    "f1_annot": (
        "the boundary a + b = N:\nΩ = π/sin(πa/N) — algebraic",
        "граница a + b = N:\nΩ = π/sin(πa/N) — алгебраична",
    ),
    "f1_title_field": (
        "The period field log₁₀ Ω(a, b) at N = {n}",
        "Поле периодов log₁₀ Ω(a, b) при N = {n}",
    ),
    "f1_leg_period": ("Ω(a, N−a) — the period", "Ω(a, N−a) — период"),
    "f1_leg_alg": (
        "π/sin(πa/N) — the algebraic boundary",
        "π/sin(πa/N) — алгебраическая",
    ),
    "f1_ylabel": ("value", "значение"),
    "f1_title_bound": (
        "The boundary of the period domain, N = {n}\nmax identity residual: {res:.1e}",
        "Граница области периодов, N = {n}\nмакс. невязка тождества: {res:.1e}",
    ),
    # fig02 — the transducer
    "f2_leg_chain": (
        "Δ_Ch(N) — the defect chain",
        "Δ_Ch(N) — расчёт цепочки",
    ),
    "f2_leg_law": (
        "power law: Δ ≈ {c:.2e}·N^{p:.2f}",
        "степенной закон: Δ ≈ {c:.2e}·N^{p:.2f}",
    ),
    "f2_leg_levels": (
        "levels N = 7, 9, 15, 30",
        "уровни N = 7, 9, 15, 30",
    ),
    "f2_xlabel": ("N — the cyclotomic level", "N — циклотомический уровень"),
    "f2_title_chain": (
        "The level discriminant: the defect chain",
        "Дискриминант уровня: цепочка дефектов",
    ),
    "f2_leg_eps": (
        "ε_N — the breathing amplitude",
        "ε_N — амплитуда дыхания",
    ),
    "f2_title_amp": (
        "The modulation amplitude and the log-stiffness",
        "Амплитуда модуляции и логарифмическая жёсткость",
    ),
    # fig03 — the breathing rosettes
    "f3_title_ros": (
        "Synchronous-breathing rosettes, N = {n}\n"
        "3 closure periods (ε = {e:.2f} — illustration; level: ε₇ = {el:.2e})",
        "Розетки синхронного дыхания, N = {n}\n"
        "3 периода замыкания (ε = {e:.2f} — иллюстрация; уровень: ε₇ = {el:.2e})",
    ),
    "f3_title_snap": (
        "Snapshots of the program",
        "Моментальные снимки программы",
    ),
    # fig04 — the transport identity
    "f4_leg_closed": (
        "closed form (1−ε²)^(−3/2)",
        "замкнутая форма (1−ε²)^(−3/2)",
    ),
    "f4_leg_meas": (
        "quadrature mean M[(1+ε·cos u)^(−2)]",
        "квадратурное среднее M[(1+ε·cos u)^(−2)]",
    ),
    "f4_xlabel": ("ε — the breathing amplitude", "ε — амплитуда дыхания"),
    "f4_ylabel": (
        "transport ratio over ω_L",
        "отношение переносов к ω_L",
    ),
    "f4_title": (
        "The mean-transport identity (stage W5)\n"
        "mpmath residual: {mp:.1e}; float residual: {fl:.1e}",
        "Тождество среднего переноса (ступень W5)\n"
        "mpmath-невязка: {mp:.1e}; float-невязка: {fl:.1e}",
    ),
    "f4_inset": ("residual", "невязка"),
    # fig05 — the dichotomy
    "f5_leg_bound": (
        "Ω(a, N−a) = π/sin(πa/N) — algebraic",
        "Ω(a, N−a) = π/sin(πa/N) — алгебраична",
    ),
    "f5_leg_diag": (
        "P(a, a) — the normalized period",
        "P(a, a) — нормированный период",
    ),
    "f5_ylabel": ("value", "значение"),
    "f5_title": (
        "The period dichotomy of the level N = {n}\n"
        "the boundary — algebraic, the diagonal — Γ-periods",
        "Дихотомия периодов уровня N = {n}\n" "граница — алгебраична, диагональ — Γ-периоды",
    ),
    "f5_leg_hclosed": (
        "H(R) — the closed form (Theorem 5)",
        "H(R) — замкнутая форма (теорема 5)",
    ),
    "f5_leg_hmeas": (
        "H — the direct pairwise summation",
        "H — прямое попарное суммирование",
    ),
    "f5_xlabel": ("R — the ring radius", "R — радиус кольца"),
    "f5_title_h": (
        "The Hamiltonian of the regular {n}-gon\n"
        "algebraic part × ln R — the transcendental shell",
        "Гамильтониан правильного {n}-угольника\n"
        "алгебраическая часть × ln R — трансцендентная оболочка",
    ),
}


def _proto(stage_slug: str, proto_dir: Path) -> Dict:
    """Load a committed W-protocol JSON (the figure's numeric oracle)."""
    path = proto_dir / f"{stage_slug}_default.json"
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
# fig01 — the period field of the level
# ---------------------------------------------------------------------------


def fig01_periods_lattice(out_dir: Path, proto_dir: Path, lang: str = "en") -> str:
    """Left: log10 Omega(a, b) over the (a, b) grid of the level N = 15.
    Right: the algebraic boundary Omega(a, N-a) = pi / sin(pi a / N)."""
    proto = _proto("W2_algebraic_boundary", proto_dir)
    n = 15
    a_grid = np.arange(1, n)
    om = np.array([[per.omega(int(a), int(b), n) for b in a_grid] for a in a_grid])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.3), constrained_layout=True)

    im = ax1.imshow(
        np.log10(om),
        origin="lower",
        cmap="Blues",
        extent=[0.5, n - 0.5, 0.5, n - 0.5],
        aspect="auto",
    )
    ax1.plot([0.5, n - 0.5], [n - 1.5, 0.5], color=CRIMSON, lw=1.6, ls="--")
    ax1.annotate(
        _t("f1_annot", lang),
        xy=(7.5, 7.0),
        xytext=(2.2, 11.2),
        color=CRIMSON,
        fontsize=8.5,
        arrowprops={"arrowstyle": "->", "color": CRIMSON, "lw": 1.0},
    )
    ax1.set_xlabel("b", fontsize=10, color=NAVY)
    ax1.set_ylabel("a", fontsize=10, color=NAVY)
    ax1.set_title(_t("f1_title_field", lang).format(n=n), fontsize=10.5, color=NAVY)
    fig.colorbar(im, ax=ax1, shrink=0.85)
    _style_axis(ax1)

    rows = per.boundary_periods_mp(n)
    a_vals = [float(r[0]) for r in rows]
    left = [float(r[1]) for r in rows]
    right = [float(r[2]) for r in rows]
    ax2.plot(a_vals, left, "o", ms=5, color=STEEL, label=_t("f1_leg_period", lang))
    ax2.plot(a_vals, right, "--", lw=1.4, color=CRIMSON, label=_t("f1_leg_alg", lang))
    ax2.set_yscale("log")
    ax2.set_xlabel("a", fontsize=10, color=NAVY)
    ax2.set_ylabel(_t("f1_ylabel", lang), fontsize=10, color=NAVY)
    max_res = proto["max_boundary_residual"]
    ax2.set_title(
        _t("f1_title_bound", lang).format(n=n, res=max_res),
        fontsize=10.5,
        color=NAVY,
    )
    ax2.legend(fontsize=8.5, framealpha=0.95)
    _style_axis(ax2)
    return _save(fig, out_dir, "fig01_periods_lattice.png")


# ---------------------------------------------------------------------------
# fig02 — the defect chain and the stiffness law
# ---------------------------------------------------------------------------


def fig02_transducer(out_dir: Path, proto_dir: Path, lang: str = "en") -> str:
    """Left: Delta_Ch(N) across the levels with the fitted power law.
    Right: the amplitude eps_N and the log-stiffness C_N."""
    proto = _proto("W7_transducer", proto_dir)
    n_grid = list(range(3, 31))
    delta_grid = [ch.defect_chain(n)["Delta_Ch"] for n in n_grid]
    eps_grid = [ch.defect_chain(n)["eps"] for n in n_grid]
    c_grid = [ch.defect_chain(n)["c_log"] for n in n_grid]

    # power-law fit Delta ~ c N^p on the scan
    x = np.log(np.array(n_grid, dtype=float))
    y = np.log(np.array(delta_grid))
    slope, intercept = np.polyfit(x, y, 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.1), constrained_layout=True)

    ax1.plot(n_grid, delta_grid, "o", ms=4.5, color=STEEL, label=_t("f2_leg_chain", lang))
    fit_line = np.exp(intercept) * np.array(n_grid, dtype=float) ** slope
    ax1.plot(
        n_grid,
        fit_line,
        "--",
        lw=1.4,
        color=CRIMSON,
        label=_t("f2_leg_law", lang).format(c=math.exp(intercept), p=slope),
    )
    table_n = [int(row["N"]) for row in proto["table"]]
    table_d = [row["Delta_Ch"] for row in proto["table"]]
    ax1.plot(
        table_n,
        table_d,
        "s",
        ms=8,
        mfc="none",
        mec=GREEN,
        mew=1.6,
        label=_t("f2_leg_levels", lang),
    )
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlabel(_t("f2_xlabel", lang), fontsize=10, color=NAVY)
    ax1.set_ylabel("Δ_Ch", fontsize=10, color=NAVY)
    ax1.set_title(_t("f2_title_chain", lang), fontsize=10.5, color=NAVY)
    ax1.legend(fontsize=8, framealpha=0.95)
    _style_axis(ax1)

    ax2.semilogy(n_grid, eps_grid, "o-", ms=4, lw=1.2, color=STEEL, label=_t("f2_leg_eps", lang))
    ax2.set_xlabel("N", fontsize=10, color=NAVY)
    ax2.set_ylabel("ε_N", fontsize=10, color=NAVY)
    ax2b = ax2.twinx()
    ax2b.plot(n_grid, c_grid, "s--", ms=4, lw=1.2, color=CRIMSON, label="C_N = ln(1+1/Δ)")
    ax2b.set_ylabel("C_N", fontsize=10, color=CRIMSON)
    ax2b.tick_params(colors=CRIMSON, labelsize=9)
    ax2b.spines["right"].set_color(CRIMSON)
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2b.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, fontsize=8.5, framealpha=0.95)
    ax2.set_title(_t("f2_title_amp", lang), fontsize=10.5, color=NAVY)
    _style_axis(ax2)
    return _save(fig, out_dir, "fig02_transducer.png")


# ---------------------------------------------------------------------------
# fig03 — the synchronous-breathing rosettes
# ---------------------------------------------------------------------------


def fig03_breathing(out_dir: Path, proto_dir: Path, lang: str = "en") -> str:
    """Left: the rosettes of all seven vortices over three closure periods.
    Right: four snapshots at the quarter phases."""
    proto = _proto("W6_synchronous_closure", proto_dir)
    n = 7
    big_r, eps_ill = 1.0, 0.25  # the raised amplitude: a picture of the program
    nu = rg.synchronous_frequency(big_r, eps_ill, 1.0, n)
    t_c = rg.closure_time(eps_ill, nu)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.8), constrained_layout=True)

    shades = plt.cm.Blues(np.linspace(0.35, 0.95, n))
    for k in range(n):
        xs, ys = rg.rosette_curve(k, n, big_r, eps_ill, nu, 3.0 * t_c)
        ax1.plot(xs, ys, lw=1.0, color=shades[k])
    ring_out = big_r * (1.0 + eps_ill) * np.cos(np.linspace(0, 2 * math.pi, 200))
    ax1.plot(
        ring_out,
        big_r * (1.0 + eps_ill) * np.sin(np.linspace(0, 2 * math.pi, 200)),
        ls=":",
        lw=0.8,
        color=GRID,
    )
    ax1.set_aspect("equal")
    eps_level = proto["eps_level"]
    ax1.set_title(
        _t("f3_title_ros", lang).format(n=n, e=eps_ill, el=eps_level),
        fontsize=10,
        color=NAVY,
    )
    ax1.set_xlabel("x", fontsize=10, color=NAVY)
    ax1.set_ylabel("y", fontsize=10, color=NAVY)
    _style_axis(ax1)

    snap_shades = [SKY, STEEL, NAVY, CRIMSON]
    for j, frac in enumerate((0.0, 0.25, 0.5, 0.75)):
        zs = rg.pumped_positions(frac * t_c, n, big_r, eps_ill, nu)
        ax2.plot(
            zs.real, zs.imag, "o-", ms=5, lw=0.7, color=snap_shades[j], label=f"t = {frac:.2f}·T_c"
        )
    ax2.set_aspect("equal")
    ax2.set_title(_t("f3_title_snap", lang), fontsize=10.5, color=NAVY)
    ax2.set_xlabel("x", fontsize=10, color=NAVY)
    ax2.set_ylabel("y", fontsize=10, color=NAVY)
    ax2.legend(fontsize=8, framealpha=0.9, loc="upper left")
    _style_axis(ax2)
    return _save(fig, out_dir, "fig03_breathing.png")


# ---------------------------------------------------------------------------
# fig04 — the mean-transport identity
# ---------------------------------------------------------------------------


def fig04_transport_law(out_dir: Path, proto_dir: Path, lang: str = "en") -> str:
    """The measured cycle mean of (1+eps cos u)^{-2} against the closed form
    (1-eps^2)^{-3/2}; the inset shows the float residual of the scan."""
    proto = _proto("W5_transport_identity", proto_dir)
    eps_values = np.linspace(0.05, 0.6, 24)
    measured = [rg.mean_transport_ratio(float(e)) for e in eps_values]
    closed = 1.0 / (1.0 - eps_values**2) ** 1.5

    fig, ax = plt.subplots(figsize=(6.8, 4.6), constrained_layout=True)
    ax.plot(
        eps_values,
        closed,
        "-",
        lw=1.8,
        color=CRIMSON,
        label=_t("f4_leg_closed", lang),
    )
    ax.plot(
        eps_values,
        measured,
        "o",
        ms=4.5,
        color=STEEL,
        label=_t("f4_leg_meas", lang),
    )
    ax.set_xlabel(_t("f4_xlabel", lang), fontsize=10, color=NAVY)
    ax.set_ylabel(_t("f4_ylabel", lang), fontsize=10, color=NAVY)
    ax.set_title(
        _t("f4_title", lang).format(mp=proto["max_mp_residual"], fl=proto["max_float_residual"]),
        fontsize=10.5,
        color=NAVY,
    )
    ax.legend(fontsize=8.5, framealpha=0.95)
    _style_axis(ax)

    axins = ax.inset_axes([0.52, 0.12, 0.42, 0.3])
    res = np.abs(np.array(measured) - closed)
    axins.semilogy(eps_values, res + 1e-18, "o-", ms=3, lw=0.9, color=GREEN)
    axins.set_title(_t("f4_inset", lang), fontsize=8, color=NAVY)
    axins.tick_params(labelsize=7, colors=NAVY)
    axins.grid(True, color=GRID, lw=0.4, alpha=0.7)
    return _save(fig, out_dir, "fig04_transport_law.png")


# ---------------------------------------------------------------------------
# fig05 — the algebraicity dichotomy
# ---------------------------------------------------------------------------


def fig05_dichotomy(out_dir: Path, proto_dir: Path, lang: str = "en") -> str:
    """Left: the boundary vs diagonal periods of the level N = 7.
    Right: the closed-form Hamiltonian H(R) against the direct pairwise H."""
    _proto("W4_polygon_flow", proto_dir)
    n = 7
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.3), constrained_layout=True)

    a_vals = list(range(1, n))
    boundary = [per.boundary_period(a, n) for a in a_vals]
    diagonal = [per.normalized_p(a, a, n) for a in a_vals]
    width = 0.38
    pos = np.arange(1, n)
    ax1.bar(
        pos - width / 2,
        boundary,
        width,
        color=STEEL,
        label=_t("f5_leg_bound", lang),
    )
    ax1.plot(pos, diagonal, "o", ms=6, color=CRIMSON, label=_t("f5_leg_diag", lang))
    ax1.set_yscale("log")
    ax1.set_xlabel("a", fontsize=10, color=NAVY)
    ax1.set_ylabel(_t("f5_ylabel", lang), fontsize=10, color=NAVY)
    ax1.set_title(
        _t("f5_title", lang).format(n=n),
        fontsize=10,
        color=NAVY,
    )
    ax1.legend(fontsize=8, framealpha=0.95)
    _style_axis(ax1)

    r_grid = np.linspace(0.55, 1.45, 60)
    h_closed = [dyn_h(n, float(r)) for r in r_grid]
    r_marks = np.array([0.6, 0.8, 1.0, 1.2, 1.4])
    h_meas = [dyn_h_measured(n, float(r)) for r in r_marks]
    ax2.plot(r_grid, h_closed, "-", lw=1.8, color=NAVY, label=_t("f5_leg_hclosed", lang))
    ax2.plot(r_marks, h_meas, "o", ms=6, color=CRIMSON, label=_t("f5_leg_hmeas", lang))
    ax2.set_xlabel(_t("f5_xlabel", lang), fontsize=10, color=NAVY)
    ax2.set_ylabel("H", fontsize=10, color=NAVY)
    ax2.set_title(
        _t("f5_title_h", lang).format(n=n),
        fontsize=10,
        color=NAVY,
    )
    ax2.legend(fontsize=8.5, framealpha=0.95)
    _style_axis(ax2)
    return _save(fig, out_dir, "fig05_dichotomy.png")


def dyn_h(n: int, big_r: float) -> float:
    """The closed-form Hamiltonian (thin wrapper for the figure)."""
    from . import dynamics as dyn

    return dyn.hamiltonian_closed_form(n, big_r, 1.0)


def dyn_h_measured(n: int, big_r: float) -> float:
    """The direct pairwise Hamiltonian of the frozen polygon."""
    from . import dynamics as dyn

    zs = rg.polygon_positions(n, big_r, 0.0)
    xy = np.stack([zs.real, zs.imag], axis=1).ravel()
    gamma_vec = np.ones(n)
    return dyn.invariants(xy, gamma_vec)["H"]


# ---------------------------------------------------------------------------
# The architecture scheme (SVG) — one edition per language
# ---------------------------------------------------------------------------

SCHEME_TEMPLATES: Dict[str, str] = {
    "en": """<svg xmlns="http://www.w3.org/2000/svg" width="980" height="560" viewBox="0 0 980 560">
  <rect x="0" y="0" width="980" height="560" fill="#FFFFFF"/>
  <text x="490" y="38" text-anchor="middle" font-family="DejaVu Sans" font-size="21" font-weight="bold" fill="#0A1A3A">CYCLORING — the research architecture</text>
  <text x="490" y="60" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#5A6472">the level triple (N, B, λ₀) → the defect chain → the discriminant Δ_Ch → the transducer → the synchronous breathing</text>

  <rect x="40" y="95" width="200" height="92" rx="10" fill="#F4F6FA" stroke="#0A1A3A" stroke-width="1.4"/>
  <text x="140" y="120" text-anchor="middle" font-family="DejaVu Sans" font-size="13" font-weight="bold" fill="#0A1A3A">The level triple</text>
  <text x="140" y="143" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">N — the order of μ_N</text>
  <text x="140" y="161" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">B = NΓR₀² — the impulse</text>
  <text x="140" y="179" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">λ₀ = Γ(N−1)/(4πR₀²)</text>

  <rect x="300" y="95" width="200" height="92" rx="10" fill="#F4F6FA" stroke="#2E5FA3" stroke-width="1.4"/>
  <text x="400" y="120" text-anchor="middle" font-family="DejaVu Sans" font-size="13" font-weight="bold" fill="#0A1A3A">The defect chain</text>
  <text x="400" y="143" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">δ = π/N, k = ⌈Bλ₀/Γ²⌉</text>
  <text x="400" y="161" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">γ = δ⁴/k, δ_eff = δ⁵/k</text>
  <text x="400" y="179" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">W_N = Σ P(a,a)</text>

  <rect x="560" y="95" width="200" height="92" rx="10" fill="#F4F6FA" stroke="#B03A2E" stroke-width="1.4"/>
  <text x="660" y="120" text-anchor="middle" font-family="DejaVu Sans" font-size="13" font-weight="bold" fill="#0A1A3A">The discriminant Δ_Ch</text>
  <text x="660" y="143" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">Δ_Ch = γ·W_N/(N−1)</text>
  <text x="660" y="161" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">the Γ-periods of the level</text>
  <text x="660" y="179" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">Ω(a,b) = Γ(a/N)Γ(b/N)/Γ((a+b)/N)</text>

  <rect x="780" y="95" width="160" height="92" rx="10" fill="#F4F6FA" stroke="#1E8449" stroke-width="1.4"/>
  <text x="860" y="120" text-anchor="middle" font-family="DejaVu Sans" font-size="13" font-weight="bold" fill="#0A1A3A">The transducer</text>
  <text x="860" y="143" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">ε = Δ/(1+Δ)</text>
  <text x="860" y="161" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">ν = ω_L(1−ε²)^(−3/2)</text>
  <text x="860" y="179" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">C_N = −ln ε</text>

  <line x1="240" y1="141" x2="300" y2="141" stroke="#0A1A3A" stroke-width="1.6" marker-end="url(#arr)"/>
  <line x1="500" y1="141" x2="560" y2="141" stroke="#0A1A3A" stroke-width="1.6" marker-end="url(#arr)"/>
  <line x1="760" y1="141" x2="780" y2="141" stroke="#0A1A3A" stroke-width="1.6" marker-end="url(#arr)"/>

  <rect x="120" y="255" width="360" height="120" rx="10" fill="#EFF4FB" stroke="#0A1A3A" stroke-width="1.4"/>
  <text x="300" y="282" text-anchor="middle" font-family="DejaVu Sans" font-size="13" font-weight="bold" fill="#0A1A3A">Algebraization of the ring (Theorem 1)</text>
  <text x="300" y="308" text-anchor="middle" font-family="DejaVu Sans" font-size="12.5" fill="#1A2433">z_k = r(t)·ζ_N^k·e^{iνt}  ⟺  the roots of z^N = σ(t)</text>
  <text x="300" y="330" text-anchor="middle" font-family="DejaVu Sans" font-size="12.5" fill="#1A2433">S_m = Σ z_k^m = 0 (m &lt; N),  S_N = Nσ,  L = 0</text>
  <text x="300" y="352" text-anchor="middle" font-family="DejaVu Sans" font-size="12.5" fill="#1A2433">Gal(ℚ(ζ_N)/ℚ) ≅ (ℤ/N)^× — the vortex relabeling</text>

  <rect x="520" y="255" width="340" height="120" rx="10" fill="#EFF4FB" stroke="#1E8449" stroke-width="1.4"/>
  <text x="690" y="282" text-anchor="middle" font-family="DejaVu Sans" font-size="13" font-weight="bold" fill="#0A1A3A">The synchronous breathing (Theorem 4)</text>
  <text x="690" y="308" text-anchor="middle" font-family="DejaVu Sans" font-size="12.5" fill="#1A2433">r(t) = R₀(1+ε·cos νt), θ_k = νt + 2πk/N</text>
  <text x="690" y="330" text-anchor="middle" font-family="DejaVu Sans" font-size="12.5" fill="#1A2433">⟨(1+ε·cos u)^(−2)⟩ = (1−ε²)^(−3/2)</text>
  <text x="690" y="352" text-anchor="middle" font-family="DejaVu Sans" font-size="12.5" fill="#1A2433">the rosette closure: T_c = 2π/ν</text>

  <rect x="40" y="420" width="900" height="100" rx="10" fill="#FFFFFF" stroke="#2E5FA3" stroke-width="1.2"/>
  <text x="490" y="447" text-anchor="middle" font-family="DejaVu Sans" font-size="13" font-weight="bold" fill="#0A1A3A">The W1–W7 ladder (deterministic protocols in results/protocols/)</text>
  <text x="490" y="472" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">W1 the period core · W2 the algebraic boundary · W3 the root system · W4 the polygon flow</text>
  <text x="490" y="492" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">W5 the transport identity · W6 the synchronous closure · W7 the transducer of the levels 7, 9, 15, 30</text>
  <text x="490" y="512" text-anchor="middle" font-family="DejaVu Sans" font-size="11" fill="#5A6472">mpmath 50 digits · RK4 · tolerances 1e−30 / 1e−12 / 1e−9</text>

  <defs>
    <marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 z" fill="#0A1A3A"/>
    </marker>
  </defs>
</svg>
""",
    "ru": """<svg xmlns="http://www.w3.org/2000/svg" width="980" height="560" viewBox="0 0 980 560">
  <rect x="0" y="0" width="980" height="560" fill="#FFFFFF"/>
  <text x="490" y="38" text-anchor="middle" font-family="DejaVu Sans" font-size="21" font-weight="bold" fill="#0A1A3A">CYCLORING — архитектура исследования</text>
  <text x="490" y="60" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#5A6472">тройка (N, B, λ₀) → цепочка дефектов → дискриминант Δ_Ch → трансдьюсер → синхронное дыхание</text>

  <rect x="40" y="95" width="200" height="92" rx="10" fill="#F4F6FA" stroke="#0A1A3A" stroke-width="1.4"/>
  <text x="140" y="120" text-anchor="middle" font-family="DejaVu Sans" font-size="13" font-weight="bold" fill="#0A1A3A">Тройка уровня</text>
  <text x="140" y="143" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">N — порядок μ_N</text>
  <text x="140" y="161" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">B = NΓR₀² — импульс</text>
  <text x="140" y="179" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">λ₀ = Γ(N−1)/(4πR₀²)</text>

  <rect x="300" y="95" width="200" height="92" rx="10" fill="#F4F6FA" stroke="#2E5FA3" stroke-width="1.4"/>
  <text x="400" y="120" text-anchor="middle" font-family="DejaVu Sans" font-size="13" font-weight="bold" fill="#0A1A3A">Цепочка дефектов</text>
  <text x="400" y="143" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">δ = π/N, k = ⌈Bλ₀/Γ²⌉</text>
  <text x="400" y="161" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">γ = δ⁴/k, δ_eff = δ⁵/k</text>
  <text x="400" y="179" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">W_N = Σ P(a,a)</text>

  <rect x="560" y="95" width="200" height="92" rx="10" fill="#F4F6FA" stroke="#B03A2E" stroke-width="1.4"/>
  <text x="660" y="120" text-anchor="middle" font-family="DejaVu Sans" font-size="13" font-weight="bold" fill="#0A1A3A">Дискриминант Δ_Ch</text>
  <text x="660" y="143" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">Δ_Ch = γ·W_N/(N−1)</text>
  <text x="660" y="161" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">Γ-периоды уровня</text>
  <text x="660" y="179" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">Ω(a,b) = Γ(a/N)Γ(b/N)/Γ((a+b)/N)</text>

  <rect x="780" y="95" width="160" height="92" rx="10" fill="#F4F6FA" stroke="#1E8449" stroke-width="1.4"/>
  <text x="860" y="120" text-anchor="middle" font-family="DejaVu Sans" font-size="13" font-weight="bold" fill="#0A1A3A">Трансдьюсер</text>
  <text x="860" y="143" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">ε = Δ/(1+Δ)</text>
  <text x="860" y="161" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">ν = ω_L(1−ε²)^(−3/2)</text>
  <text x="860" y="179" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">C_N = −ln ε</text>

  <line x1="240" y1="141" x2="300" y2="141" stroke="#0A1A3A" stroke-width="1.6" marker-end="url(#arr)"/>
  <line x1="500" y1="141" x2="560" y2="141" stroke="#0A1A3A" stroke-width="1.6" marker-end="url(#arr)"/>
  <line x1="760" y1="141" x2="780" y2="141" stroke="#0A1A3A" stroke-width="1.6" marker-end="url(#arr)"/>

  <rect x="120" y="255" width="360" height="120" rx="10" fill="#EFF4FB" stroke="#0A1A3A" stroke-width="1.4"/>
  <text x="300" y="282" text-anchor="middle" font-family="DejaVu Sans" font-size="13" font-weight="bold" fill="#0A1A3A">Алгебраизация кольца (теорема 1)</text>
  <text x="300" y="308" text-anchor="middle" font-family="DejaVu Sans" font-size="12.5" fill="#1A2433">z_k = r(t)·ζ_N^k·e^{iνt}  ⟺  корни системы z^N = σ(t)</text>
  <text x="300" y="330" text-anchor="middle" font-family="DejaVu Sans" font-size="12.5" fill="#1A2433">S_m = Σ z_k^m = 0 (m &lt; N),  S_N = Nσ,  L = 0</text>
  <text x="300" y="352" text-anchor="middle" font-family="DejaVu Sans" font-size="12.5" fill="#1A2433">Gal(ℚ(ζ_N)/ℚ) ≅ (ℤ/N)^× — релябелинг вихрей</text>

  <rect x="520" y="255" width="340" height="120" rx="10" fill="#EFF4FB" stroke="#1E8449" stroke-width="1.4"/>
  <text x="690" y="282" text-anchor="middle" font-family="DejaVu Sans" font-size="13" font-weight="bold" fill="#0A1A3A">Синхронное дыхание (теорема 4)</text>
  <text x="690" y="308" text-anchor="middle" font-family="DejaVu Sans" font-size="12.5" fill="#1A2433">r(t) = R₀(1+ε·cos νt), θ_k = νt + 2πk/N</text>
  <text x="690" y="330" text-anchor="middle" font-family="DejaVu Sans" font-size="12.5" fill="#1A2433">⟨(1+ε·cos u)^(−2)⟩ = (1−ε²)^(−3/2)</text>
  <text x="690" y="352" text-anchor="middle" font-family="DejaVu Sans" font-size="12.5" fill="#1A2433">замыкание розеток: T_c = 2π/ν</text>

  <rect x="40" y="420" width="900" height="100" rx="10" fill="#FFFFFF" stroke="#2E5FA3" stroke-width="1.2"/>
  <text x="490" y="447" text-anchor="middle" font-family="DejaVu Sans" font-size="13" font-weight="bold" fill="#0A1A3A">Лестница W1–W7 (детерминированные протоколы results/protocols/)</text>
  <text x="490" y="472" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">W1 ядро периодов · W2 алгебраическая граница · W3 корневая система · W4 поток кольца</text>
  <text x="490" y="492" text-anchor="middle" font-family="DejaVu Sans" font-size="12" fill="#1A2433">W5 тождество переноса · W6 синхронное замыкание · W7 трансдьюсер уровней 7, 9, 15, 30</text>
  <text x="490" y="512" text-anchor="middle" font-family="DejaVu Sans" font-size="11" fill="#5A6472">mpmath 50 знаков · RK4 · допуск 1e−30 / 1e−12 / 1e−9</text>

  <defs>
    <marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 z" fill="#0A1A3A"/>
    </marker>
  </defs>
</svg>
""",
}


# ---------------------------------------------------------------------------
# The factory driver — both language editions in one pass
# ---------------------------------------------------------------------------

FIGURES = {
    "fig01_periods_lattice.png": fig01_periods_lattice,
    "fig02_transducer.png": fig02_transducer,
    "fig03_breathing.png": fig03_breathing,
    "fig04_transport_law.png": fig04_transport_law,
    "fig05_dichotomy.png": fig05_dichotomy,
}


def main(
    proto_dir: Path | None = None,
    out_dir: Path | None = None,
    langs: tuple[str, ...] = ("en", "ru"),
) -> None:
    """Generate the figure editions listed by ``langs``.

    English (the primary edition) lands in ``out_dir`` itself; every other
    language lands in its ``LANG_DIRS`` subfolder (Russian → ``ru/``).
    """
    proto_dir = proto_dir if proto_dir is not None else DEFAULT_PROTOS
    out_dir = out_dir if out_dir is not None else DEFAULT_OUT
    for lang in langs:
        lang_dir = out_dir / LANG_DIRS[lang]
        for name, factory in FIGURES.items():
            path = factory(lang_dir, proto_dir, lang)
            print(f"wrote {path} [{lang}]")
        scheme = lang_dir / "scheme_cycloring.svg"
        scheme.parent.mkdir(parents=True, exist_ok=True)
        scheme.write_text(SCHEME_TEMPLATES[lang], encoding="utf-8")
        print(f"wrote {scheme} [{lang}]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CYCLORING figure factory (bilingual: en primary + ru mirror)"
    )
    parser.add_argument(
        "--lang",
        choices=("both", "en", "ru"),
        default="both",
        help="which language edition to generate (default: both)",
    )
    parser.add_argument("--proto-dir", type=Path, default=None)
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()
    _langs = {"both": ("en", "ru"), "en": ("en",), "ru": ("ru",)}[args.lang]
    main(proto_dir=args.proto_dir, out_dir=args.out_dir, langs=_langs)
