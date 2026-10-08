#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
TRIVORTEX — SCIENTIFIC VERIFICATION LABORATORY (v1.0)
============================================================================
A full-fledged interactive laboratory around the independent verification
ladder `verify.py` (milestone M0). While `verify.py` is the CI workhorse —
one preset, one JSON protocol — the laboratory is the researcher's bench:

  * run the V1–V4 ladder in preset or fully custom configuration
    (C_Ch, T, Gamma, a, rotations, steps/period — editable interactively);
  * analyses: convergence study (measured omega error vs integration grid)
    and a monitored invariant-drift scan along the trajectory;
  * publication-grade figures at 600 dpi (PNG + PDF + SVG variations):
    closed form, Chaplygin diagnostic, Lagrange choreography, convergence,
    unequal-circulation robustness, invariant drifts, one-glance dashboard;
  * machine-readable JSON protocols and CSV data for every run — the same
    "every number is bound to a run" discipline as the whole framework;
  * a bilingual interface (English / Русский), chosen at start or via
    `--lang en|ru`.

The laboratory re-imports the ladder's check functions and never modifies
them: the registered tolerances and criteria of `verification/README.md`
stay authoritative. The only thing added here is optics, ergonomics and
analysis around the same numbers.

Usage
-----
    python3 lab.py                          # interactive session
    python3 lab.py --preset quick --no-menu # CI smoke (no figures)
    python3 lab.py --no-menu --figures      # figures for the default preset
    python3 lab.py --lang ru                # Russian interface

Dependencies: numpy (required), matplotlib (optional, for figures).
Author: Isaev Iskhak Khamzatovich (repository owner)
License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import argparse
import datetime
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from verify import (  # noqa: E402  (the ladder — imported, never modified)
    PRESETS,
    analytical_amplitude,
    analytical_frequency,
    analytical_radius,
    check_v1_theorem31,
    check_v2_lagrange_rotation,
    check_v3_invariants,
    check_v4_robustness,
    compute_chaplygin,
    equilateral_initial,
    invariants,
    lagrange_omega,
    rk4_step,
)

# ---------------------------------------------------------------------------
# Bilingual strings
# ---------------------------------------------------------------------------

STRINGS = {
    "en": {
        "title": "TRIVORTEX — Scientific Verification Laboratory",
        "subtitle": "Theorem 3.1 / Chaplygin integrals — the researcher's bench",
        "menu": "MAIN MENU",
        "m1": "1) Run the verification ladder V1–V4 (preset)",
        "m2": "2) Custom parameters (C_Ch, T, Gamma, a, rotations, steps)",
        "m3": "3) Analysis: convergence study (omega error vs grid)",
        "m4": "4) Analysis: invariant drift scan along the trajectory",
        "m5": "5) Figures: full set at 600 dpi (PNG + PDF + SVG)",
        "m6": "6) Figures: one-glance dashboard (600 dpi)",
        "m7": "7) Reports: JSON protocol + CSV data of the last run",
        "m0": "0) Exit",
        "choice": "choice> ",
        "preset_prompt": "Preset [quick/default/full] (default: default): ",
        "cch_prompt": "C_Ch (> 0) [1.0]: ",
        "t_prompt": "T period [6.283185307179586]: ",
        "gamma_prompt": "Gamma (equal circulations) [1.0]: ",
        "a_prompt": "Triangle side a [1.0]: ",
        "rot_prompt": "Rotations [5]: ",
        "spp_prompt": "Steps per period [4000]: ",
        "running": "Running the ladder ...",
        "result": "RESULT",
        "passed": "checks passed",
        "preset": "preset",
        "wall": "wall time",
        "json_saved": "JSON protocol saved to",
        "csv_saved": "CSV data saved to",
        "fig_saved": "figures saved to",
        "conv_title": "Convergence study: measured omega error vs integration grid",
        "conv_header": "steps/period     omega_rel_err     shape_drift",
        "drift_title": "Invariant drift scan (monitored every 8 snapshots)",
        "drift_header": "   t/T        dH        dP        dQ        dI",
        "invalid": "Invalid choice, try again.",
        "bye": "Goodbye — and keep every number bound to a run.",
        "pass": "PASS",
        "fail": "FAIL",
        "custom_note": "Custom run: the registered tolerances still apply.",
        "custom_refs": "  omega = {omega:.15g}   eps = {eps:.15g}   omega_Lagrange = {lag:.15g}",
        "fig1": "fig1_closed_form — r_k(t) of Theorem 3.1",
        "fig2": "fig2_chaplygin — the Section-6 diagnostic C_Ch(t)",
        "fig3": "fig3_choreography — the Lagrange rigid rotation",
        "fig4": "fig4_convergence — omega error vs grid",
        "fig5": "fig5_robustness — unequal circulations (1, 2, 3)",
        "fig6": "fig6_invariants — drift scan of H, P, Q, I",
        "fig7": "fig7_dashboard — the one-glance summary",
        "lang_set": "Language: English",
    },
    "ru": {
        "title": "TRIVORTEX — Научная лаборатория верификации",
        "subtitle": "Теорема 3.1 / интегралы Чаплыгина — рабочий стол исследователя",
        "menu": "ГЛАВНОЕ МЕНЮ",
        "m1": "1) Запустить лестницу верификации V1–V4 (пресет)",
        "m2": "2) Свои параметры (C_Ch, T, Гамма, a, обороты, шаги)",
        "m3": "3) Анализ: сходимость (ошибка omega от сетки)",
        "m4": "4) Анализ: сканирование дрейфа инвариантов по траектории",
        "m5": "5) Графики: полный набор 600 dpi (PNG + PDF + SVG)",
        "m6": "6) Графики: сводная панель (600 dpi)",
        "m7": "7) Отчёты: JSON-протокол + CSV последнего запуска",
        "m0": "0) Выход",
        "choice": "выбор> ",
        "preset_prompt": "Пресет [quick/default/full] (по умолчанию: default): ",
        "cch_prompt": "C_Ch (> 0) [1.0]: ",
        "t_prompt": "Период T [6.283185307179586]: ",
        "gamma_prompt": "Гамма (одинаковые циркуляции) [1.0]: ",
        "a_prompt": "Сторона треугольника a [1.0]: ",
        "rot_prompt": "Обороты [5]: ",
        "spp_prompt": "Шагов на период [4000]: ",
        "running": "Запускаю лестницу ...",
        "result": "ИТОГ",
        "passed": "проверок пройдено",
        "preset": "пресет",
        "wall": "время",
        "json_saved": "JSON-протокол сохранён в",
        "csv_saved": "CSV-данные сохранены в",
        "fig_saved": "графики сохранены в",
        "conv_title": "Исследование сходимости: ошибка omega от сетки интегрирования",
        "conv_header": "шагов/период    отн.ошибка omega  дрейф формы",
        "drift_title": "Сканирование дрейфа инвариантов (снимок каждые 8 шагов)",
        "drift_header": "   t/T        dH        dP        dQ        dI",
        "invalid": "Неверный пункт, попробуйте ещё раз.",
        "bye": "До встречи — и держите каждое число привязанным к запуску.",
        "pass": "ПРОЙДЕНО",
        "fail": "ПРОВАЛ",
        "custom_note": "Свой запуск: зарегистрированные допуски остаются в силе.",
        "custom_refs": "  omega = {omega:.15g}   eps = {eps:.15g}   omega_Лагранж = {lag:.15g}",
        "fig1": "fig1_closed_form — r_k(t) Теоремы 3.1",
        "fig2": "fig2_chaplygin — диагностикa C_Ch(t) раздела 6",
        "fig3": "fig3_choreography — жёсткое вращение Лагранжа",
        "fig4": "fig4_convergence — ошибка omega от сетки",
        "fig5": "fig5_robustness — неравные циркуляции (1, 2, 3)",
        "fig6": "fig6_invariants — дрейф H, P, Q, I",
        "fig7": "fig7_dashboard — сводная панель",
        "lang_set": "Язык: русский",
    },
}

# The repository's navy-and-gold brand palette
NAVY = "#10243E"
GOLD = "#C9A227"
STEEL = "#4A6FA5"
CRIMSON = "#B0413E"
GREEN = "#3F7E5B"
GRID = "#D8DEE7"

FIG_DPI = 600  # the registered raster resolution of the laboratory


# ---------------------------------------------------------------------------
# Matplotlib bootstrap (late import; brand style)
# ---------------------------------------------------------------------------


def load_plt():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.font_manager as fm

    for font in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ):
        if os.path.exists(font):
            fm.fontManager.addfont(font)
    import matplotlib.pyplot as plt

    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["DejaVu Sans"],
            "axes.unicode_minus": False,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": NAVY,
            "axes.labelcolor": NAVY,
            "axes.grid": True,
            "grid.color": GRID,
            "grid.linewidth": 0.6,
            "axes.linewidth": 1.1,
            "xtick.color": NAVY,
            "ytick.color": NAVY,
            "text.color": NAVY,
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.labelsize": 11,
            "legend.fontsize": 9,
            "figure.dpi": 100,
            "savefig.dpi": FIG_DPI,
        }
    )
    return plt


PALETTE = [STEEL, GOLD, GREEN, CRIMSON, NAVY, "#8C6BB1", "#39A0A0", "#E1772E"]


# ---------------------------------------------------------------------------
# Run helpers
# ---------------------------------------------------------------------------


def ask(prompt: str, default: str) -> str:
    try:
        raw = input(f"{prompt}").strip()
    except EOFError:
        return default
    return raw if raw else default


def ask_f64(prompt: str, default: float) -> float:
    raw = ask(prompt, "")
    try:
        return float(raw) if raw else default
    except ValueError:
        return default


def ask_int(prompt: str, default: int) -> int:
    raw = ask(prompt, "")
    try:
        return int(raw) if raw else default
    except ValueError:
        return default


def fmt(v: float) -> str:
    return f"{v:.6e}"


def print_report(checks, lang: str, wall: float, preset_name: str) -> None:
    s = STRINGS[lang]
    line = "═" * 74
    thin = "─" * 74
    print(line)
    for c in checks:
        mark = s["pass"] if c["passed"] else s["fail"]
        print(f"\n[{mark}] {c['check']}")
        for key, val in c.items():
            if key in ("check", "passed"):
                continue
            if isinstance(val, dict):
                print(f"    {key}:")
                for kk, vv in val.items():
                    print(
                        f"      {kk} = {vv:.6e}" if isinstance(vv, float) else f"      {kk} = {vv}"
                    )
            else:
                print(f"    {key} = {val:.6e}" if isinstance(val, float) else f"    {key} = {val}")
    n_pass = sum(1 for c in checks if c["passed"])
    print(thin)
    print(
        f"  {s['result']}: {n_pass}/{len(checks)} {s['passed']}  "
        f"({s['preset']}={preset_name}, {s['wall']} {wall:.2f}s)"
    )
    print(line)


def out_dir_default() -> str:
    return os.path.normpath(os.path.join(HERE, "..", "..", "outputs", "lab"))


def save_json_report(report: dict, out_dir: str, preset_name: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(out_dir, f"lab_verify_{preset_name}_{stamp}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    return path


def write_csv(path: str, header: list[str], rows) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(",".join(header) + "\n")
        for row in rows:
            f.write(",".join(repr(float(x)) for x in row) + "\n")


# ---------------------------------------------------------------------------
# The ladder wrapper (custom-parameter capable)
# ---------------------------------------------------------------------------


def run_full_ladder(
    lang: str,
    preset_name: str | None,
    custom: dict | None,
    out_dir: str,
) -> tuple[list[dict], dict]:
    """Run V1–V4 with a preset or a custom parameter set; save the protocol."""
    s = STRINGS[lang]
    t0 = time.perf_counter()
    if custom is not None:
        c_ch = custom["C_Ch"]
        t_period = custom["T"]
        gamma = custom["Gamma"]
        a = custom["a"]
        rotations = custom["rotations"]
        spp = custom["steps_per_period"]
        v1 = check_v1_theorem31(c_ch=c_ch, t_period=t_period, n_points=1000)
        v2 = check_v2_lagrange_rotation(gamma=gamma, a=a, rotations=rotations, steps_per_period=spp)
        v3 = check_v3_invariants(gamma=gamma, a=a, rotations=rotations, steps_per_period=spp)
        v4 = check_v4_robustness(
            gammas=(1.0, 2.0, 3.0), a=a, rotations=max(2, rotations - 2), steps_per_period=spp
        )
        preset_label = "custom"
    else:
        cfg = PRESETS[preset_name or "default"]
        v1 = check_v1_theorem31(n_points=cfg["n_points_cch"])
        v2 = check_v2_lagrange_rotation(
            rotations=cfg["rotations"], steps_per_period=cfg["steps_per_period"]
        )
        v3 = check_v3_invariants(
            rotations=cfg["rotations"], steps_per_period=cfg["steps_per_period"]
        )
        v4 = check_v4_robustness(
            rotations=max(2, cfg["rotations"] - 2), steps_per_period=cfg["steps_per_period"]
        )
        preset_label = preset_name or "default"

    checks = [v1, v2, v3, v4]
    wall = time.perf_counter() - t0
    print_report(checks, lang, wall, preset_label)

    report = {
        "suite": "trivortex-verification-lab",
        "version": "1.0",
        "preset": preset_label,
        "date_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "wall_time_s": wall,
        "checks_passed": sum(1 for c in checks if c["passed"]),
        "checks_total": len(checks),
        "all_passed": all(c["passed"] for c in checks),
        "checks": checks,
    }
    path = save_json_report(report, out_dir, preset_label)
    print(f"{s['json_saved']} {path}")
    return checks, report


def convergence_study() -> list[dict]:
    """Measured omega error and shape drift vs integration grid (V2 twin)."""
    rows = []
    for spp in (250, 500, 1000, 2000, 4000, 8000):
        res = check_v2_lagrange_rotation(rotations=2, steps_per_period=spp)
        rows.append(
            {
                "steps_per_period": spp,
                "omega_rel_err": res["omega_relative_error"],
                "shape_drift": res["shape_drift"],
            }
        )
    return rows


def invariant_drift_scan(rotations: int = 3, steps_per_period: int = 4000):
    """Monitor H, P, Q, I along the Lagrange trajectory every 8 steps."""
    gamma_vec = np.full(3, 1.0)
    state = equilateral_initial(1.0)
    omega = lagrange_omega(1.0, 1.0)
    dt = (2.0 * math.pi / omega) / steps_per_period
    inv0 = invariants(state, gamma_vec)
    n_steps = rotations * steps_per_period
    snap_every = 8
    ts, hs, ps, qs, iss = [0.0], [0.0], [0.0], [0.0], [0.0]
    for step in range(1, n_steps + 1):
        state = rk4_step(state, gamma_vec, dt)
        if step % snap_every == 0 or step == n_steps:
            inv = invariants(state, gamma_vec)
            ts.append(step * dt)
            hs.append(abs(inv["H"] - inv0["H"]) / max(abs(inv0["H"]), 1.0))
            ps.append(abs(inv["P"] - inv0["P"]) / max(abs(inv0["P"]), 1.0))
            qs.append(abs(inv["Q"] - inv0["Q"]) / max(abs(inv0["Q"]), 1.0))
            iss.append(abs(inv["I"] - inv0["I"]) / max(abs(inv0["I"]), 1.0))
    return {
        "t": np.array(ts),
        "dH": np.array(hs),
        "dP": np.array(ps),
        "dQ": np.array(qs),
        "dI": np.array(iss),
        "T": 2.0 * math.pi / omega,
    }


def v4_trajectory(rotations: int = 3, steps_per_period: int = 4000):
    """Tracked unequal-circulation trajectory for the figures."""
    a = 1.0
    gammas = np.array([1.0, 2.0, 3.0])
    pts = np.array([[0.0, 0.0], [a, 0.0], [0.5 * a, math.sqrt(3.0) / 2.0 * a]])
    pts = pts - pts.mean(axis=0)
    state = pts.ravel()
    omega_ref = lagrange_omega(2.0, a)
    dt = (2.0 * math.pi / omega_ref) / steps_per_period
    n_steps = rotations * steps_per_period
    snap_every = max(n_steps // 600, 1)
    traj = [(0.0, state.copy())]
    for step in range(1, n_steps + 1):
        state = rk4_step(state, gammas, dt)
        if step % snap_every == 0:
            traj.append((step * dt, state.copy()))
    return traj


# ---------------------------------------------------------------------------
# Figures (600 dpi, three formats: PNG + PDF + SVG)
# ---------------------------------------------------------------------------


def _save_all(fig, out_dir: str, name: str) -> list[str]:
    figdir = os.path.join(out_dir, "figures")
    os.makedirs(figdir, exist_ok=True)
    paths = []
    for ext in ("png", "pdf", "svg"):
        p = os.path.join(figdir, f"{name}.{ext}")
        fig.savefig(p, dpi=FIG_DPI, bbox_inches="tight", facecolor="white")
        paths.append(p)
    return paths


def fig_closed_form(out_dir: str, c_ch: float = 1.0, t_period: float = 2.0 * math.pi):
    plt = load_plt()
    omega = analytical_frequency(c_ch, t_period)
    t_r = 2.0 * math.pi / omega
    t = np.linspace(0.0, 2.0 * t_r, 900)
    fig, ax = plt.subplots(figsize=(8.2, 4.9), constrained_layout=True)
    for k in range(3):
        r = np.array([analytical_radius(x, c_ch, t_period, k) for x in t])
        ax.plot(t, r, lw=1.8, color=PALETTE[k], label=rf"$r_{k}(t)$, $k={k}$")
    ax.axhline(math.sqrt(c_ch), color=NAVY, lw=0.8, ls=":", alpha=0.6)
    ax.set_title("Theorem 3.1 closed form: radial modulation over two periods")
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$r_k(t) = \sqrt{C_{Ch}}\,(1+\varepsilon\cos(\omega t + 2\pi k/3))$")
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False)
    paths = _save_all(fig, out_dir, "fig1_closed_form")
    plt.close(fig)
    return paths


def fig_chaplygin(out_dir: str, c_ch: float = 1.0, t_period: float = 2.0 * math.pi, n: int = 2000):
    plt = load_plt()
    omega = analytical_frequency(c_ch, t_period)
    t = np.linspace(0.0, 100.0 * t_period, n)
    c_t = np.array(
        [compute_chaplygin(analytical_radius(x, c_ch, t_period, 0), omega, 1.0) for x in t]
    )
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.6), constrained_layout=True)
    axes[0].plot(t, c_t, lw=1.0, color=GOLD)
    axes[0].set_title(r"Diagnostic $C_{Ch}(t)$ over the full window $[0,\,100T]$")
    axes[0].set_xlabel(r"$t$")
    axes[0].set_ylabel(r"$C_{Ch}(t) = r^2(\dot\theta - q/r)$")
    axes[1].plot(t[: n // 10], c_t[: n // 10], lw=1.4, color=GOLD)
    axes[1].set_title("Zoom: the first $10T$")
    axes[1].set_xlabel(r"$t$")
    axes[1].set_ylabel(r"$C_{Ch}(t)$")
    for ax in axes:
        ax.grid(True, alpha=0.6)
    paths = _save_all(fig, out_dir, "fig2_chaplygin")
    plt.close(fig)
    return paths


def fig_choreography(out_dir: str):
    plt = load_plt()
    # tracked integration mirroring V2 (kept local so the ladder stays untouched)
    gamma_vec = np.full(3, 1.0)
    state = equilateral_initial(1.0)
    omega = lagrange_omega(1.0, 1.0)
    dt = (2.0 * math.pi / omega) / 2000
    traj = [state.copy()]
    for _ in range(2 * 2000):
        state = rk4_step(state, gamma_vec, dt)
        traj.append(state.copy())
    pts = np.array(traj)

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 5.2), constrained_layout=True)
    for k in range(3):
        axes[0].plot(
            pts[:, 2 * k], pts[:, 2 * k + 1], lw=1.5, color=PALETTE[k], label=f"vortex {k}"
        )
        axes[0].plot(
            pts[0, 2 * k], pts[0, 2 * k + 1], "o", ms=7, mfc="white", mec=PALETTE[k], mew=1.8
        )
    axes[0].set_title("V2 — Lagrange rigid rotation (tracks)")
    axes[0].set_xlabel("$x$")
    axes[0].set_ylabel("$y$")
    axes[0].set_aspect("equal")
    axes[0].legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False)

    t = np.linspace(0.0, 2.0 * math.pi / omega, 400)
    sides = []
    for x in t[1:]:
        th = omega * x + 2.0 * math.pi * np.arange(3) / 3.0
        d = (th[1] - th[0]) % (2.0 * math.pi)
        sides.append(d)
    axes[1].plot(t[1:], sides, lw=1.2, color=NAVY)
    axes[1].axhline(2.0 * math.pi / 3.0, color=GOLD, lw=1.0, ls="--", label=r"exactly $2\pi/3$")
    axes[1].set_ylim(2.0 * math.pi / 3.0 - 1e-9, 2.0 * math.pi / 3.0 + 1e-9)
    axes[1].set_title("V1 — the angular separation stays exactly $2\\pi/3$")
    axes[1].set_xlabel(r"$t$")
    axes[1].set_ylabel(r"$\theta_{k+1}-\theta_k$")
    axes[1].legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False)
    paths = _save_all(fig, out_dir, "fig3_choreography")
    plt.close(fig)
    return paths


def fig_convergence(out_dir: str, rows: list[dict]):
    plt = load_plt()
    x = [r["steps_per_period"] for r in rows]
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.6), constrained_layout=True)
    axes[0].loglog(x, [r["omega_rel_err"] for r in rows], "o-", lw=1.8, color=STEEL, ms=6)
    axes[0].set_title(r"V2 convergence: $\omega$ relative error")
    axes[0].set_xlabel("steps per period")
    axes[0].set_ylabel(r"$|\omega_{meas}-\omega|/\omega$")
    axes[1].loglog(x, [r["shape_drift"] for r in rows], "s-", lw=1.8, color=GOLD, ms=6)
    axes[1].set_title("V2 convergence: shape drift")
    axes[1].set_xlabel("steps per period")
    axes[1].set_ylabel(r"$\max_i |s_i - a|/a$")
    for ax in axes:
        ax.grid(True, which="both", alpha=0.5)
    paths = _save_all(fig, out_dir, "fig4_convergence")
    plt.close(fig)
    return paths


def fig_robustness(out_dir: str):
    plt = load_plt()
    traj = np.array([s for _, s in v4_trajectory()])
    fig, ax = plt.subplots(figsize=(7.6, 6.4), constrained_layout=True)
    for k, g in enumerate((1.0, 2.0, 3.0)):
        ax.plot(
            traj[:, 2 * k],
            traj[:, 2 * k + 1],
            lw=1.4,
            color=PALETTE[k],
            label=rf"$\Gamma_{k+1}={g:.0f}$",
        )
        ax.plot(traj[0, 2 * k], traj[0, 2 * k + 1], "o", ms=7, mfc="white", mec=PALETTE[k], mew=1.8)
    ax.set_title("V4 — unequal circulations on a generic triangle")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_aspect("equal")
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False)
    paths = _save_all(fig, out_dir, "fig5_robustness")
    plt.close(fig)
    return paths


def fig_invariants(out_dir: str, scan: dict):
    plt = load_plt()
    fig, ax = plt.subplots(figsize=(8.6, 4.9), constrained_layout=True)
    tt = scan["t"] / scan["T"]
    for key, color in zip(("dH", "dP", "dQ", "dI"), PALETTE):
        ax.semilogy(tt, np.maximum(scan[key], 1e-18), lw=1.3, color=color, label=f"${key}$")
    ax.set_title("V3 — relative drift of the vortex integrals along the trajectory")
    ax.set_xlabel(r"$t/T$")
    ax.set_ylabel("relative drift")
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False)
    paths = _save_all(fig, out_dir, "fig6_invariants")
    plt.close(fig)
    return paths


def fig_dashboard(out_dir: str, checks: list[dict], conv_rows: list[dict]):
    """The one-glance summary: verdicts + convergence + drift + choreography."""
    plt = load_plt()
    fig = plt.figure(figsize=(12.6, 8.0), constrained_layout=True)
    gs = fig.add_gridspec(2, 3)

    # (0,0) verdict table
    ax = fig.add_subplot(gs[0, 0])
    ax.axis("off")
    ax.set_title("Verdicts", loc="left")
    rows = [("check", "residual", "tolerance", "verdict")]
    if len(checks) == 4:
        v1, v2, v3, v4 = checks
        rows.append(
            (
                "V1 choreography",
                f"{v1['angular_separation_error']:.2e}",
                "1e-12",
                "PASS" if v1["passed"] else "FAIL",
            )
        )
        rows.append(
            (
                "V1 periodicity",
                f"{v1['periodicity_residual']:.2e}",
                "1e-12",
                "PASS" if v1["passed"] else "FAIL",
            )
        )
        rows.append(
            ("V2 shape", f"{v2['shape_drift']:.2e}", "1e-10", "PASS" if v2["passed"] else "FAIL")
        )
        rows.append(
            (
                "V2 omega",
                f"{v2['omega_relative_error']:.2e}",
                "1e-6",
                "PASS" if v2["passed"] else "FAIL",
            )
        )
        rows.append(
            ("V3 drift", f"{v3['worst_drift']:.2e}", "1e-10", "PASS" if v3["passed"] else "FAIL")
        )
        rows.append(
            ("V4 drift", f"{v4['worst_drift']:.2e}", "1e-10", "PASS" if v4["passed"] else "FAIL")
        )
    table = ax.table(cellText=rows[1:], colLabels=rows[0], loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(8.6)
    table.scale(1.0, 1.5)
    for (r, _c), cell in table.get_celld().items():
        if r == 0:
            cell.set_facecolor(NAVY)
            cell.set_text_props(color="white", weight="bold")
        elif rows[r][3] == "PASS":
            cell.set_facecolor("#EDF6EF")
        else:
            cell.set_facecolor("#FBEDEC")

    # (0,1) convergence
    ax = fig.add_subplot(gs[0, 1])
    x = [r["steps_per_period"] for r in conv_rows]
    ax.loglog(x, [r["omega_rel_err"] for r in conv_rows], "o-", color=STEEL, ms=5, lw=1.6)
    ax.set_title(r"Convergence of $\omega$")
    ax.set_xlabel("steps/period")
    ax.grid(True, which="both", alpha=0.5)

    # (0,2) closed form
    ax = fig.add_subplot(gs[0, 2])
    omega = analytical_frequency(1.0, 2.0 * math.pi)
    t = np.linspace(0.0, 4.0 * math.pi / omega, 500)
    for k in range(3):
        ax.plot(
            t, [analytical_radius(x, 1.0, 2.0 * math.pi, k) for x in t], lw=1.4, color=PALETTE[k]
        )
    ax.set_title("Theorem 3.1: $r_k(t)$")
    ax.set_xlabel("$t$")

    # (1,0) choreography tracks
    ax = fig.add_subplot(gs[1, 0])
    gamma_vec = np.full(3, 1.0)
    state = equilateral_initial(1.0)
    om = lagrange_omega(1.0, 1.0)
    dt = (2.0 * math.pi / om) / 1500
    traj = [state.copy()]
    for _ in range(2 * 1500):
        state = rk4_step(state, gamma_vec, dt)
        traj.append(state.copy())
    pts = np.array(traj)
    for k in range(3):
        ax.plot(pts[:, 2 * k], pts[:, 2 * k + 1], lw=1.2, color=PALETTE[k], alpha=0.85)
        # the three vortices share one orbit with a 2*pi/3 phase shift —
        # mark their distinct start positions
        ax.plot(pts[0, 2 * k], pts[0, 2 * k + 1], "o", ms=7, mfc="white", mec=PALETTE[k], mew=1.8)
    ax.set_title("Rigid rotation (V2)")
    ax.set_aspect("equal")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")

    # (1,1) chaplygin diagnostic
    ax = fig.add_subplot(gs[1, 1])
    t2 = np.linspace(0.0, 20.0 * math.pi, 800)
    c_t = [compute_chaplygin(analytical_radius(x, 1.0, 2.0 * math.pi, 0), omega, 1.0) for x in t2]
    ax.plot(t2, c_t, lw=1.1, color=GOLD)
    ax.set_title(r"Diagnostic $C_{Ch}(t)$, $[0,10T]$")
    ax.set_xlabel("$t$")

    # (1,2) invariant drift scan
    ax = fig.add_subplot(gs[1, 2])
    scan = invariant_drift_scan(rotations=2, steps_per_period=2000)
    tt = scan["t"] / scan["T"]
    for key, color in zip(("dH", "dP", "dQ", "dI"), PALETTE):
        ax.semilogy(tt, np.maximum(scan[key], 1e-18), lw=1.1, color=color, label=f"${key}$")
    ax.set_title("Invariant drifts (V3)")
    ax.set_xlabel(r"$t/T$")
    ax.set_ylabel("relative drift")
    ax.legend(fontsize=7.5, ncol=2, frameon=False, loc="lower right")

    fig.suptitle("TRIVORTEX — verification ladder dashboard", fontsize=15, fontweight="bold")
    paths = _save_all(fig, out_dir, "fig7_dashboard")
    plt.close(fig)
    return paths


# ---------------------------------------------------------------------------
# Interactive session
# ---------------------------------------------------------------------------


def box_line(text: str, width: int = 64) -> str:
    return f"│ {text.ljust(width - 3)} │"


def interactive(lang: str, out_dir: str) -> int:
    s = STRINGS[lang]
    print()
    print("╔" + "═" * (len(s["title"]) + 13) + "╗")
    print(f"║   {s['title']}   ║")
    print(f"║   {s['subtitle']}   ║")
    print("╚" + "═" * (len(s["title"]) + 13) + "╝")

    last: dict | None = None
    last_checks: list[dict] | None = None
    conv_rows = convergence_study()

    while True:
        print()
        print("┌" + "─" * (len(s["title"]) + 13) + "┐")
        print(box_line(s["menu"], len(s["title"]) + 14))
        for key in ("m1", "m2", "m3", "m4", "m5", "m6", "m7", "m0"):
            print(box_line(s[key], len(s["title"]) + 14))
        print("└" + "─" * (len(s["title"]) + 13) + "┘")
        pick = ask(s["choice"], "")

        if pick == "1":
            pn = ask(s["preset_prompt"], "default")
            pn = pn if pn in PRESETS else "default"
            last_checks, last = run_full_ladder(lang, pn, None, out_dir)
        elif pick == "2":
            print(s["custom_note"])
            custom = {
                "C_Ch": ask_f64(s["cch_prompt"], 1.0),
                "T": ask_f64(s["t_prompt"], 2.0 * math.pi),
                "Gamma": ask_f64(s["gamma_prompt"], 1.0),
                "a": ask_f64(s["a_prompt"], 1.0),
                "rotations": ask_int(s["rot_prompt"], 5),
                "steps_per_period": ask_int(s["spp_prompt"], 4000),
            }
            print(
                s["custom_refs"].format(
                    omega=analytical_frequency(custom["C_Ch"], custom["T"]),
                    eps=analytical_amplitude(custom["C_Ch"]),
                    lag=lagrange_omega(custom["Gamma"], custom["a"]),
                )
            )
            last_checks, last = run_full_ladder(lang, None, custom, out_dir)
        elif pick == "3":
            print(s["conv_title"])
            print(s["conv_header"])
            for r in conv_rows:
                print(
                    f"  {r['steps_per_period']:>13}   {r['omega_rel_err']:>14.3e}   "
                    f"{r['shape_drift']:>11.3e}"
                )
            write_csv(
                os.path.join(out_dir, "data", "convergence_study.csv"),
                ["steps_per_period", "omega_rel_err", "shape_drift"],
                [[r["steps_per_period"], r["omega_rel_err"], r["shape_drift"]] for r in conv_rows],
            )
            fig_convergence(out_dir, conv_rows)
            print(f"{s['csv_saved']} {os.path.join(out_dir, 'data')}")
            print(f"{s['fig_saved']} {os.path.join(out_dir, 'figures')} (fig4)")
        elif pick == "4":
            print(s["drift_title"])
            print(s["drift_header"])
            scan = invariant_drift_scan()
            for i in range(0, len(scan["t"]), max(len(scan["t"]) // 20, 1)):
                print(
                    f"  {scan['t'][i] / scan['T']:>7.3f}   {scan['dH'][i]:>8.2e}   "
                    f"{scan['dP'][i]:>8.2e}   {scan['dQ'][i]:>8.2e}   {scan['dI'][i]:>8.2e}"
                )
            fig_invariants(out_dir, scan)
            print(f"{s['fig_saved']} {os.path.join(out_dir, 'figures')} (fig6)")
        elif pick == "5":
            fig_closed_form(out_dir)
            fig_chaplygin(out_dir)
            fig_choreography(out_dir)
            fig_convergence(out_dir, conv_rows)
            fig_robustness(out_dir)
            fig_invariants(out_dir, invariant_drift_scan())
            print(f"{s['fig_saved']} {os.path.join(out_dir, 'figures')}")
            for key in ("fig1", "fig2", "fig3", "fig4", "fig5", "fig6"):
                print(f"  • {s[key]}")
        elif pick == "6":
            fig_dashboard(
                out_dir, last_checks or run_full_ladder("en", "quick", None, out_dir)[0], conv_rows
            )
            print(f"{s['fig_saved']} {os.path.join(out_dir, 'figures')}")
            print(f"  • {s['fig7']}")
        elif pick == "7":
            if last is None:
                print(s["invalid"])
            else:
                print(json.dumps(last, indent=2, ensure_ascii=False)[:2000])
        elif pick == "0":
            print(s["bye"])
            return 0
        else:
            print(s["invalid"])


# ---------------------------------------------------------------------------
# CLI entry
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description="TRIVORTEX scientific verification laboratory")
    ap.add_argument("--preset", default=None, choices=sorted(PRESETS))
    ap.add_argument("--out-dir", default=None, help="protocol/data/figures directory")
    ap.add_argument("--lang", default="en", choices=["en", "ru"])
    ap.add_argument("--no-menu", action="store_true", help="run non-interactively (CI)")
    ap.add_argument("--figures", action="store_true", help="generate the full figure set")
    ap.add_argument("--smoke", action="store_true", help="CI smoke: quick ladder, 1 dashboard")
    args = ap.parse_args()

    out_dir = args.out_dir or out_dir_default()
    if args.smoke:
        checks, report = run_full_ladder("en", "quick", None, out_dir)
        conv_rows = convergence_study()
        try:
            fig_dashboard(out_dir, checks, conv_rows)
        except Exception as exc:  # noqa: BLE001 — figures must never break CI
            print(f"(dashboard skipped: {exc})")
        return 0 if report["all_passed"] else 1
    if args.no_menu:
        pn = args.preset or "default"
        checks, report = run_full_ladder(args.lang, pn, None, out_dir)
        if args.figures:
            conv_rows = convergence_study()
            fig_closed_form(out_dir)
            fig_chaplygin(out_dir)
            fig_choreography(out_dir)
            fig_convergence(out_dir, conv_rows)
            fig_robustness(out_dir)
            fig_invariants(out_dir, invariant_drift_scan())
            fig_dashboard(out_dir, checks, conv_rows)
            print(f"{STRINGS[args.lang]['fig_saved']} {os.path.join(out_dir, 'figures')}")
        return 0 if report["all_passed"] else 1
    return interactive(args.lang, out_dir)


if __name__ == "__main__":
    sys.exit(main())
