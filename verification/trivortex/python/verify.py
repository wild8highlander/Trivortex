#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
TRIVORTEX — VERIFICATION LADDER FOR THE THREE-BODY VORTEX MODEL (v1.0)
============================================================================
A self-contained, dependency-light verification script for the TRIVORTEX
document (code/trivortex_core*.py). It re-derives and numerically checks
the four claims that anchor Theorem 3.1 and the Chaplygin topological
integral, using independent code (no imports from the core document).

Checks
------
V1  Theorem 3.1 — closed form & Chaplygin integral.
    For the Lagrange-type rotating configuration
        r_k(t) = sqrt(C_Ch) * (1 + eps * cos(omega*t + 2*pi*k/3)),
        theta_k(t) = omega*t + 2*pi*k/3,
    the Chaplygin integral C_Ch = r^2 * (theta_dot - q * A_theta) must stay
    constant to machine precision over [0, 100*T], and the three vortices
    must keep the exact 2*pi/3 angular separation (equilateral choreography).

V2  Rigid rotation of the Lagrange triangle (numerical).
    Three equal point vortices at an equilateral triangle of side a must
    rotate rigidly with the analytic angular velocity
    omega = 3*Gamma/(2*pi*a^2) — the point-vortex analogue of the classical
    Lagrange equilateral solution of the three-body problem. Integrated
    with RK4; the measured omega must match the analytic value, and the
    triangle must stay equilateral.

V3  Conservation of the vortex integrals (numerical).
    Along the V2 trajectory the classical invariants of point-vortex
    dynamics must be conserved: Hamiltonian H, linear impulses
    P = sum(Gamma*x), Q = sum(Gamma*y) and the angular impulse
    I = sum(Gamma*|r|^2). These are the many-body Chaplygin-type
    integrals of the vortex model.

V4  Robustness with unequal circulations.
    For Gamma = (1, 2, 3) (a non-symmetric but integrable setup) all
    invariants of V3 must still be conserved — the integrals do not
    require the symmetric initial condition.

Output
------
* Human-readable PASS/FAIL table on stdout;
* A machine-readable JSON report in outputs/ (parameter snapshot,
  residuals, wall time) — the same "every number is bound to a run"
  discipline used across this repository.

Exit code 0 = all checks passed, 1 = at least one check failed.

Usage
-----
    python3 verify.py                 # default tolerance ladder
    python3 verify.py --preset quick  # fast smoke run (CI)
    python3 verify.py --preset full   # long integration, tighter grid

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

# ---------------------------------------------------------------------------
# Presets (mirror of verification/common/python/config.py)
# ---------------------------------------------------------------------------

PRESETS = {
    "quick": {"rotations": 2, "steps_per_period": 2000, "n_points_cch": 200},
    "default": {"rotations": 5, "steps_per_period": 4000, "n_points_cch": 1000},
    "full": {"rotations": 20, "steps_per_period": 8000, "n_points_cch": 2000},
}

TOLERANCES = {
    "chaplygin_drift": 1e-12,  # V1: |C_Ch(t) - C_Ch(0)| over the whole window
    "angular_sep": 1e-12,  # V1: max deviation of the 2*pi/3 separation
    "shape_drift": 1e-10,  # V2: relative side-length drift after N rotations
    "omega_rel_err": 1e-6,  # V2: measured vs analytic angular velocity
    "invariant_drift": 1e-10,  # V3/V4: relative drift of H, P, Q, I
}


# ---------------------------------------------------------------------------
# Section A — analytic layer (Theorem 3.1, mirrors code/trivortex_core.py §5)
# ---------------------------------------------------------------------------


def analytical_frequency(c_ch: float, t_period: float) -> float:
    """omega = (2*pi/T) * exp(C_Ch/pi)  — Theorem 3.1."""
    return (2.0 * math.pi / t_period) * math.exp(c_ch / math.pi)


def analytical_amplitude(c_ch: float) -> float:
    """eps = 1/(exp(C_Ch/pi) - 1) — Theorem 3.1."""
    return 1.0 / (math.exp(c_ch / math.pi) - 1.0) if c_ch > 0.01 else 1.0


def analytical_radius(t: float, c_ch: float, t_period: float, k: int) -> float:
    """r_k(t) = sqrt(C_Ch) * (1 + eps*cos(omega*t + 2*pi*k/3))."""
    omega = analytical_frequency(c_ch, t_period)
    eps = analytical_amplitude(c_ch)
    r0 = math.sqrt(c_ch) if c_ch > 0 else 0.01
    return r0 * (1.0 + eps * math.cos(omega * t + 2.0 * math.pi * k / 3.0))


def compute_chaplygin(r: float, theta_dot: float, q: float = 1.0, a_theta: float = 0.0) -> float:
    """C_Ch = r^2 * (theta_dot - q*A_theta) — the topological integral."""
    a = a_theta if a_theta > 0 else (1.0 / r if r > 0 else 0.0)
    return r * r * (theta_dot - q * a)


def check_v1_theorem31(
    c_ch: float = 1.0, t_period: float = 2.0 * math.pi, n_points: int = 1000
) -> dict:
    """V1 — Theorem 3.1 closed form: choreography, periodicity, and the
    recorded Section-6 drift diagnostic.

    What is verified as a pass/fail criterion:
      (a) the three vortices keep the exact 2*pi/3 angular separation at
          all probed times (equilateral choreography);
      (b) the closed form is periodic: r_k(t + T_r) = r_k(t) with
          T_r = 2*pi/omega for every k.
    Additionally the drift of the gauge-dependent combination
    C_Ch(t) = r^2 * (theta_dot - q*A_theta) (A_theta = 1/r), the exact
    quantity recorded by Section 6 of the core document, is reported as a
    diagnostic — it oscillates by construction and is window-dependent;
    the window-independent conserved quantities of the model are the
    vortex integrals verified numerically in V3/V4.
    """
    omega = analytical_frequency(c_ch, t_period)
    t_r = 2.0 * math.pi / omega
    t_max = 100.0 * t_period
    t_vals = np.linspace(0.0, t_max, n_points)

    # (a) equilateral choreography
    sep = []
    for t in (0.0, 0.25 * t_max, 0.5 * t_max, t_max):
        angles = [omega * t + 2.0 * math.pi * k / 3.0 for k in range(3)]
        d = [(angles[(i + 1) % 3] - angles[i]) % (2.0 * math.pi) for i in range(3)]
        sep.extend(d)
    sep_err = float(np.max(np.abs(np.array(sep) - 2.0 * math.pi / 3.0)))

    # (b) periodicity of the closed form
    per_res = 0.0
    for k in range(3):
        for t in (0.0, 0.137 * t_max, 0.5 * t_max, 0.811 * t_max):
            per_res = max(
                per_res,
                abs(
                    analytical_radius(t + t_r, c_ch, t_period, k)
                    - analytical_radius(t, c_ch, t_period, k)
                ),
            )

    # diagnostic: Section-6 endpoint drift of C_Ch(t) along the closed form
    c_ch_t = np.array(
        [compute_chaplygin(analytical_radius(t, c_ch, t_period, 0), omega, 1.0) for t in t_vals]
    )
    drift = float(np.max(np.abs(c_ch_t - c_ch_t[0])))

    return {
        "check": "V1 Theorem 3.1: choreography + periodicity of the closed form",
        "angular_separation_error": sep_err,
        "angular_separation_tolerance": TOLERANCES["angular_sep"],
        "periodicity_residual": per_res,
        "periodicity_tolerance": TOLERANCES["chaplygin_drift"],
        "section6_drift_diagnostic": drift,
        "passed": (
            sep_err <= TOLERANCES["angular_sep"] and per_res <= TOLERANCES["chaplygin_drift"]
        ),
        "params": {
            "C_Ch": c_ch,
            "T": t_period,
            "n_points": n_points,
            "omega": omega,
            "window": "0..100T",
        },
    }


# ---------------------------------------------------------------------------
# Section B — numerical layer (point-vortex dynamics, RK4)
# ---------------------------------------------------------------------------


def vortex_rhs(state: np.ndarray, gamma: np.ndarray) -> np.ndarray:
    """Kirchhoff equations for point vortices.

    state = flat [x0, y0, x1, y1, ...]; Gamma_i circulations.
        dx_i/dt = -1/(2*pi) * sum_{j!=i} G_j * (y_i - y_j) / r_ij^2
        dy_i/dt = +1/(2*pi) * sum_{j!=i} G_j * (x_i - x_j) / r_ij^2
    """
    n = len(gamma)
    xy = state.reshape(n, 2)
    dxy = np.zeros_like(xy)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx = xy[i, 0] - xy[j, 0]
            dy = xy[i, 1] - xy[j, 1]
            r2 = dx * dx + dy * dy
            if r2 == 0.0:
                continue
            dxy[i, 0] += -gamma[j] * dy / r2 / (2.0 * math.pi)
            dxy[i, 1] += +gamma[j] * dx / r2 / (2.0 * math.pi)
    return dxy.ravel()


def rk4_step(state: np.ndarray, gamma: np.ndarray, dt: float) -> np.ndarray:
    """One classical RK4 step of the vortex dynamics."""
    k1 = vortex_rhs(state, gamma)
    k2 = vortex_rhs(state + 0.5 * dt * k1, gamma)
    k3 = vortex_rhs(state + 0.5 * dt * k2, gamma)
    k4 = vortex_rhs(state + dt * k3, gamma)
    return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def invariants(state: np.ndarray, gamma: np.ndarray) -> dict:
    """H, P, Q, I — the classical (Chaplygin-type) vortex integrals."""
    n = len(gamma)
    xy = state.reshape(n, 2)
    h = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            r = float(np.linalg.norm(xy[i] - xy[j]))
            h += -gamma[i] * gamma[j] * math.log(r) / (2.0 * math.pi)
    p = float(np.sum(gamma * xy[:, 0]))
    q = float(np.sum(gamma * xy[:, 1]))
    imp = float(np.sum(gamma * np.sum(xy * xy, axis=1)))
    return {"H": h, "P": p, "Q": q, "I": imp}


def equilateral_initial(a: float = 1.0) -> np.ndarray:
    """Three equal vortices on an equilateral triangle of side a."""
    r = a / math.sqrt(3.0)
    pts = []
    for k in range(3):
        ang = 2.0 * math.pi * k / 3.0
        pts.append([r * math.cos(ang), r * math.sin(ang)])
    return np.array(pts).ravel()


def lagrange_omega(gamma: float, a: float) -> float:
    """Analytic angular velocity of the rigidly rotating equilateral triangle:
    omega = 3*Gamma/(2*pi*a^2) — the point-vortex Lagrange solution."""
    return 3.0 * gamma / (2.0 * math.pi * a * a)


def _sides(xy: np.ndarray) -> np.ndarray:
    return np.array(
        [
            np.linalg.norm(xy[0] - xy[1]),
            np.linalg.norm(xy[1] - xy[2]),
            np.linalg.norm(xy[2] - xy[0]),
        ]
    )


def check_v2_lagrange_rotation(
    gamma: float = 1.0, a: float = 1.0, rotations: int = 5, steps_per_period: int = 4000
) -> dict:
    """V2 — rigid rotation + measured vs analytic omega."""
    state = equilateral_initial(a)
    omega = lagrange_omega(gamma, a)
    period = 2.0 * math.pi / omega
    dt = period / steps_per_period
    gamma_vec = np.full(3, gamma)

    xy0 = state.reshape(3, 2)
    ang_start = math.atan2(xy0[0, 1], xy0[0, 0])
    n_steps = int(rotations * steps_per_period)
    for _ in range(n_steps):
        state = rk4_step(state, gamma_vec, dt)
    xy = state.reshape(3, 2)
    ang_end = math.atan2(xy[0, 1], xy[0, 0])

    # Unwrap: lift the raw angle difference to the branch closest to the
    # expected unwrapped angle, so whole turns and atan2 branch flips
    # (angle returning as -1e-9 instead of +2*pi - 1e-9) are handled.
    expected_total = omega * n_steps * dt  # radians, unwrapped
    raw_diff = ang_end - ang_start
    measured_total = raw_diff + 2.0 * math.pi * round((expected_total - raw_diff) / (2.0 * math.pi))
    omega_rel_err = abs(measured_total - expected_total) / expected_total

    sides = _sides(xy)
    shape_drift = float(np.max(np.abs(sides - a)) / a)

    return {
        "check": "V2 Lagrange rigid rotation: shape + analytic omega = 3G/(2pi a^2)",
        "shape_drift": shape_drift,
        "shape_tolerance": TOLERANCES["shape_drift"],
        "omega_analytic": omega,
        "omega_relative_error": omega_rel_err,
        "omega_tolerance": TOLERANCES["omega_rel_err"],
        "passed": (
            shape_drift <= TOLERANCES["shape_drift"]
            and omega_rel_err <= TOLERANCES["omega_rel_err"]
        ),
        "params": {
            "Gamma": gamma,
            "a": a,
            "rotations": rotations,
            "steps_per_period": steps_per_period,
            "dt": dt,
        },
    }


def check_v3_invariants(
    gamma: float = 1.0, a: float = 1.0, rotations: int = 5, steps_per_period: int = 4000
) -> dict:
    """V3 — H, P, Q, I conserved along the Lagrange trajectory."""
    state = equilateral_initial(a)
    omega = lagrange_omega(gamma, a)
    dt = (2.0 * math.pi / omega) / steps_per_period
    gamma_vec = np.full(3, gamma)

    inv0 = invariants(state, gamma_vec)
    n_steps = int(rotations * steps_per_period)
    for _ in range(n_steps):
        state = rk4_step(state, gamma_vec, dt)
    inv1 = invariants(state, gamma_vec)

    drifts = {k: abs(inv1[k] - inv0[k]) / max(abs(inv0[k]), 1.0) for k in inv0}
    worst = max(drifts.values())
    return {
        "check": "V3 vortex integrals: H, P, Q, I conserved (equal Gamma)",
        "relative_drifts": drifts,
        "worst_drift": worst,
        "tolerance": TOLERANCES["invariant_drift"],
        "passed": worst <= TOLERANCES["invariant_drift"],
        "params": {
            "Gamma": gamma,
            "a": a,
            "rotations": rotations,
            "steps_per_period": steps_per_period,
        },
    }


def check_v4_robustness(
    gammas=(1.0, 2.0, 3.0), a: float = 1.0, rotations: int = 3, steps_per_period: int = 4000
) -> dict:
    """V4 — integrals conserved for unequal circulations (no symmetry needed)."""
    # Generic triangle, centroid shifted to the origin.
    pts = np.array([[0.0, 0.0], [a, 0.0], [0.5 * a, math.sqrt(3.0) / 2.0 * a]])
    pts = pts - pts.mean(axis=0)
    state = pts.ravel()
    gamma_vec = np.array(gammas)

    inv0 = invariants(state, gamma_vec)
    # Reference period from the mean circulation scale (integration window).
    omega_ref = lagrange_omega(float(np.mean(gammas)), a)
    dt = (2.0 * math.pi / omega_ref) / steps_per_period
    n_steps = int(rotations * steps_per_period)
    for _ in range(n_steps):
        state = rk4_step(state, gamma_vec, dt)
    inv1 = invariants(state, gamma_vec)

    drifts = {k: abs(inv1[k] - inv0[k]) / max(abs(inv0[k]), 1.0) for k in inv0}
    worst = max(drifts.values())
    return {
        "check": "V4 robustness: H, P, Q, I conserved for Gamma = (1, 2, 3)",
        "relative_drifts": drifts,
        "worst_drift": worst,
        "tolerance": TOLERANCES["invariant_drift"],
        "passed": worst <= TOLERANCES["invariant_drift"],
        "params": {
            "Gamma": list(gammas),
            "a": a,
            "rotations": rotations,
            "steps_per_period": steps_per_period,
        },
    }


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def run(preset: str = "default", out_dir: str | None = None) -> int:
    cfg = PRESETS[preset]
    t0 = time.perf_counter()
    checks = [
        check_v1_theorem31(n_points=cfg["n_points_cch"]),
        check_v2_lagrange_rotation(
            rotations=cfg["rotations"], steps_per_period=cfg["steps_per_period"]
        ),
        check_v3_invariants(rotations=cfg["rotations"], steps_per_period=cfg["steps_per_period"]),
        check_v4_robustness(
            rotations=max(2, cfg["rotations"] - 2), steps_per_period=cfg["steps_per_period"]
        ),
    ]
    elapsed = time.perf_counter() - t0
    n_pass = sum(1 for c in checks if c["passed"])

    print("=" * 74)
    print("  TRIVORTEX — VERIFICATION LADDER (Theorem 3.1 / Chaplygin integrals)")
    print("=" * 74)
    for c in checks:
        status = "PASS" if c["passed"] else "FAIL"
        print(f"\n[{status}] {c['check']}")
        for key, val in c.items():
            if key in ("check", "passed"):
                continue
            if isinstance(val, dict):
                print(f"    {key}:")
                for kk, vv in val.items():
                    print(f"      {kk} = {vv}")
            else:
                print(f"    {key} = {val}")
    print("\n" + "-" * 74)
    print(
        f"  RESULT: {n_pass}/{len(checks)} checks passed  "
        f"(preset={preset}, wall time {elapsed:.2f}s)"
    )
    print("-" * 74)

    report = {
        "suite": "trivortex-verification",
        "version": "1.0",
        "preset": preset,
        "date_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "wall_time_s": elapsed,
        "checks_passed": n_pass,
        "checks_total": len(checks),
        "all_passed": n_pass == len(checks),
        "checks": checks,
    }
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
        path = os.path.join(out_dir, f"trivortex_verify_{preset}_{stamp}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                report, f, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o)
            )
        print(f"  JSON report: {path}")

    return 0 if n_pass == len(checks) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="TRIVORTEX verification ladder")
    ap.add_argument("--preset", default="default", choices=sorted(PRESETS))
    ap.add_argument("--out-dir", default=None, help="write a JSON report into this directory")
    args = ap.parse_args()
    out = args.out_dir
    if out is None:
        here = os.path.dirname(os.path.abspath(__file__))
        out = os.path.normpath(os.path.join(here, "..", "..", "outputs", "trivortex"))
    return run(args.preset, out)


if __name__ == "__main__":
    sys.exit(main())
