#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
POLYVORTEX — THE W-LADDER: SEVEN VERIFICATION/RESEARCH STAGES
============================================================================
The verification-and-research ladder of the mini-repository. Stages
W1–W3 generalize the parent ladder's V1–V3 registers from N = 3 to
arbitrary N; stages W4–W7 are the new research content:

    W1  Theorem 3.1 anchor at N = 3 (cross-ladder compatibility)
    W2  Rigid rotation of the regular N-gon, N = 2..8 (omega_N formula)
    W3  Conservation of H, P, Q, I along the N-gon orbit
    W4  Spectral (in)stability: the Havelock threshold N <= 7 / N >= 8
    W5  Admissibility of the closed form: eps < 1 <=> C_Ch > pi*ln(2)
    W6  The kinematic obstruction for the pulsating ansatz (Lemma C)
    W7  The averaged-frequency bridge + the compatibility table (D1)

Every stage returns the parent ladder's check-dictionary discipline:
{"check": ..., numeric registers..., "passed": bool, "params": {...}}.
The runner (runner.py) binds every number to a JSON protocol file.

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import math

import numpy as np

from . import ansatz as an
from . import classical as cl
from . import model as md

N_VALUES = (2, 3, 4, 5, 6, 7, 8)

TOLERANCES = {
    "angular_sep": 1e-12,  # W1: the 2*pi/N separation register
    "periodicity": 1e-12,  # W1: r(t + T_r) = r(t)
    "anchor": 1e-15,  # W1: pinned literals of the N = 3 reduction
    "shape_drift": 1e-10,  # W2: chord-table deviation after the run
    "omega_rel_err": 1e-6,  # W2: measured vs analytic omega (RK4 band)
    "invariant_drift": 1e-10,  # W3: relative drifts of H, P, Q, I
    "stability_tol": 1e-7,  # W4: max Re(lambda) classifier
    "identity": 1e-12,  # W5/W6/W7: algebraic identities on grids
}

PRESETS = {
    "quick": {
        "rotations": 1,
        "steps_per_period": 600,
        "n_points": 120,
        "cch_grid": 40,
        "quad_nodes": 80,
    },
    "default": {
        "rotations": 2,
        "steps_per_period": 2000,
        "n_points": 400,
        "cch_grid": 200,
        "quad_nodes": 160,
    },
    "full": {
        "rotations": 5,
        "steps_per_period": 6000,
        "n_points": 1200,
        "cch_grid": 500,
        "quad_nodes": 240,
    },
}


# ---------------------------------------------------------------------------
# W1 — Theorem 3.1 anchor at N = 3
# ---------------------------------------------------------------------------


def check_w1_anchor(
    c_ch: float = 1.0, t_period: float = 2.0 * math.pi, n_points: int = 400
) -> dict:
    """W1 — the N = 3 reduction of the generalized closed form must
    reproduce the parent ladder's Theorem 3.1 registers exactly:
    (a) the 2*pi/3 angular separation at all probed times;
    (b) periodicity r(t + T_r) = r(t) with T_r = 2*pi/omega;
    (c) the pinned frequency literal omega = e^(1/pi) = 1.3748022274393588
        (the parent ladder's registered value at C_Ch = 1, T = 2*pi).
    The Section-6 gauge diagnostic drift is reported as a diagnostic.
    """
    n = 3
    omega = an.ansatz_frequency(c_ch, t_period)
    t_r = 2.0 * math.pi / omega
    t_max = 100.0 * t_period

    sep_err = 0.0
    for t in (0.0, 0.25 * t_max, 0.5 * t_max, t_max):
        angles = [an.ansatz_angle(t, c_ch, t_period, k, n) for k in range(n)]
        d = [(angles[(i + 1) % n] - angles[i]) % (2.0 * math.pi) for i in range(n)]
        sep_err = max(sep_err, max(abs(x - 2.0 * math.pi / n) for x in d))

    per_res = 0.0
    for k in range(n):
        for t in (0.0, 0.137 * t_max, 0.5 * t_max, 0.811 * t_max):
            per_res = max(
                per_res,
                abs(
                    an.ansatz_radius(t + t_r, c_ch, t_period, k, n)
                    - an.ansatz_radius(t, c_ch, t_period, k, n)
                ),
            )

    anchor_err = abs(omega - 1.3748022274393588)
    amp_err = abs(an.ansatz_amplitude(c_ch) - 1.0 / (math.exp(1.0 / math.pi) - 1.0))
    diag = an.diagnostic_drift(c_ch, t_period, n, n_points=n_points)

    return {
        "check": "W1 Theorem 3.1 anchor at N=3: separation + periodicity + literals",
        "angular_separation_error": sep_err,
        "periodicity_residual": per_res,
        "frequency_anchor_error": anchor_err,
        "amplitude_anchor_error": amp_err,
        "section6_drift_diagnostic": diag,
        "params": {"C_Ch": c_ch, "T": t_period, "n_points": n_points, "omega": omega},
        "passed": (
            sep_err <= TOLERANCES["angular_sep"]
            and per_res <= TOLERANCES["periodicity"]
            and anchor_err <= TOLERANCES["anchor"]
            and amp_err <= TOLERANCES["anchor"]
        ),
    }


# ---------------------------------------------------------------------------
# W2 — rigid rotation of the regular N-gon
# ---------------------------------------------------------------------------


def check_w2_ring_rotation(
    gamma: float = 1.0,
    big_r: float = 1.0,
    rotations: int = 2,
    steps_per_period: int = 2000,
) -> dict:
    """W2 — for every N the regular N-gon rotates rigidly with the
    Kirchhoff rate omega_N = Gamma*(N-1)/(4*pi*R^2); measured via the
    unwrapped angle of vortex 0 (RK4), shape held to the chord table."""
    per_n = []
    all_pass = True
    for n in N_VALUES:
        state0 = cl.ngon_initial(n, big_r)
        gamma_vec = np.full(n, gamma)
        omega = cl.ngon_omega(gamma, big_r, n)
        period = 2.0 * math.pi / omega
        dt = period / steps_per_period
        n_steps = int(rotations * steps_per_period)
        measured = cl.measured_rotation_rate(state0, gamma_vec, dt, n_steps, omega)
        omega_rel_err = abs(measured - omega) / omega
        state = md.integrate(state0, gamma_vec, dt, n_steps)
        shape = cl.shape_deviation(state, gamma_vec, big_r)
        ok = omega_rel_err <= TOLERANCES["omega_rel_err"] and shape <= TOLERANCES["shape_drift"]
        all_pass = all_pass and ok
        per_n.append(
            {
                "N": n,
                "omega_analytic": omega,
                "omega_measured": measured,
                "omega_relative_error": omega_rel_err,
                "shape_deviation": shape,
                "passed": ok,
            }
        )
    return {
        "check": "W2 regular N-gon rigid rotation: omega_N = G(N-1)/(4 pi R^2), N=2..8",
        "per_N": per_n,
        "params": {
            "Gamma": gamma,
            "R": big_r,
            "rotations": rotations,
            "steps_per_period": steps_per_period,
        },
        "passed": all_pass,
    }


# ---------------------------------------------------------------------------
# W3 — invariants along the N-gon orbit
# ---------------------------------------------------------------------------


def check_w3_invariants(
    gamma: float = 1.0,
    big_r: float = 1.0,
    rotations: int = 2,
    steps_per_period: int = 2000,
) -> dict:
    """W3 — H, P, Q, I conserved along every N-gon trajectory."""
    per_n = []
    all_pass = True
    for n in N_VALUES:
        state = cl.ngon_initial(n, big_r)
        gamma_vec = np.full(n, gamma)
        omega = cl.ngon_omega(gamma, big_r, n)
        dt = (2.0 * math.pi / omega) / steps_per_period
        inv0 = md.invariants(state, gamma_vec)
        state = md.integrate(state, gamma_vec, dt, int(rotations * steps_per_period))
        inv1 = md.invariants(state, gamma_vec)
        drifts = md.relative_drifts(inv0, inv1)
        worst = max(drifts.values())
        ok = worst <= TOLERANCES["invariant_drift"]
        all_pass = all_pass and ok
        per_n.append({"N": n, "relative_drifts": drifts, "worst_drift": worst, "passed": ok})
    return {
        "check": "W3 vortex integrals H, P, Q, I conserved along the N-gon, N=2..8",
        "per_N": per_n,
        "params": {
            "Gamma": gamma,
            "R": big_r,
            "rotations": rotations,
            "steps_per_period": steps_per_period,
        },
        "passed": all_pass,
    }


# ---------------------------------------------------------------------------
# W4 — the Havelock stability threshold
# ---------------------------------------------------------------------------


def check_w4_stability(gamma: float = 1.0, big_r: float = 1.0) -> dict:
    """W4 — spectral stability of the N-gon relative equilibrium from
    the co-rotating spectrum; the classical Havelock threshold (stable
    for N <= 7, unstable for N >= 8) must be reproduced."""
    per_n = []
    threshold_ok = True
    for n in N_VALUES:
        state = cl.ngon_initial(n, big_r)
        gamma_vec = np.full(n, gamma)
        omega = cl.ngon_omega(gamma, big_r, n)
        spec = md.corotating_spectrum(state, gamma_vec, omega)
        max_re = float(np.max(np.real(spec)))
        stable = max_re <= TOLERANCES["stability_tol"]
        expected = n <= 7
        threshold_ok = threshold_ok and (stable == expected)
        per_n.append(
            {
                "N": n,
                "max_Re_lambda": max_re,
                "numerically_stable": stable,
                "havelock_stable": expected,
                "spectrum_re_im": [
                    [float(z.real), float(z.imag)] for z in sorted(spec, key=lambda z: -z.real)
                ],
            }
        )
    return {
        "check": "W4 Havelock threshold: N-gon stable for N<=7, unstable for N>=8",
        "per_N": per_n,
        "params": {"Gamma": gamma, "R": big_r, "stability_tolerance": TOLERANCES["stability_tol"]},
        "passed": threshold_ok,
    }


# ---------------------------------------------------------------------------
# W5 — admissibility of the closed form (Theorem B)
# ---------------------------------------------------------------------------


def check_w5_admissibility(cch_grid: int = 200, c_ch_max: float = 10.0) -> dict:
    """W5 — eps < 1 <=> C_Ch > pi*ln(2) on a dense grid; at C_Ch* the
    amplitude equals exactly 1 (exp(C_Ch*/pi) = 2); for admissible
    C_Ch the sampled minimum radius equals sqrt(C_Ch)*(1 - eps)."""
    grid = np.linspace(0.5, c_ch_max, int(cch_grid))
    equiv_ok = True
    min_r_err = 0.0
    n_admissible = 0
    for c in grid:
        eps = an.ansatz_amplitude(float(c))
        if (float(c) > an.C_CH_STAR) != (eps < 1.0):
            equiv_ok = False
        if eps < 1.0:
            n_admissible += 1
            for k in (0, 1, 2):
                exact = math.sqrt(float(c)) * (1.0 - eps)
                sampled = an.min_radius(float(c), 2.0 * math.pi, k, 3, n_grid=4096)
                min_r_err = max(min_r_err, abs(sampled - exact))  # absolute
    threshold_err = abs(an.ansatz_amplitude(an.C_CH_STAR) - 1.0)
    return {
        "check": "W5 admissibility: eps < 1 iff C_Ch > pi*ln(2) = 2.177586090303602",
        "threshold_C_Ch_star": an.C_CH_STAR,
        "amplitude_at_threshold_error": threshold_err,
        "equivalence_violations": 0 if equiv_ok else 1,
        "grid_points": int(cch_grid),
        "admissible_points": n_admissible,
        "min_radius_max_abs_error": min_r_err,
        "params": {"C_Ch_max": c_ch_max, "min_radius_grid": 4096},
        "passed": (
            equiv_ok
            and threshold_err <= TOLERANCES["identity"]
            and min_r_err <= 1e-6  # uniform-grid sampling resolution bound
        ),
    }


# ---------------------------------------------------------------------------
# W6 — the kinematic obstruction (Lemma C)
# ---------------------------------------------------------------------------


def _pulse_state(t: float, n: int, big_r: float, eps: float, omega: float) -> np.ndarray:
    """Common (phase-free) pulsation: a regular N-gon with r(t) common."""
    r = big_r * (1.0 + eps * math.cos(omega * t))
    return cl.ngon_initial(n, r, phase=omega * t)


def _pulse_radial_speed(t: float, big_r: float, eps: float, omega: float) -> float:
    """dr/dt of the common pulsation."""
    return -big_r * eps * omega * math.sin(omega * t)


def check_w6_obstruction(
    eps_grid: tuple = (0.01, 0.05, 0.1, 0.3), n_grid: int = 200, gamma: float = 1.0
) -> dict:
    """W6 — Lemma C, numerically certified.

    (a) symmetric pulsation: the induced radial velocity of the regular
        N-gon vanishes identically (pair cancellation), so the pulsating
        ansatz violates the radial equation by exactly |dr/dt| — the
        mismatch ratio |v_r - dr/dt| / (R*eps*omega) must equal 1;
    (b) the H1 phase-shifted variant (radii lag the angles by 2*pi*k/N):
        the shape register itself fails (pairwise distances leave the
        chord table) and the induced radial velocity is nonzero — the
        obstruction is recorded, not assumed.
    """
    omega = 1.0
    big_r = 1.0
    t_period = 2.0 * math.pi / omega
    t_vals = np.linspace(0.0, t_period, n_grid, endpoint=False)

    sym = []
    for n_sym in (3, 5):
        for eps in eps_grid:
            worst_vr = 0.0
            worst_ident = 0.0
            for t in t_vals:
                state = _pulse_state(float(t), n_sym, big_r, eps, omega)
                gamma_vec = np.full(n_sym, gamma)
                vel = md.vortex_rhs(state, gamma_vec)
                for k in range(n_sym):
                    th = omega * float(t) + 2.0 * math.pi * k / n_sym
                    e_r = np.array([math.cos(th), math.sin(th)])
                    v_r = float(vel[2 * k : 2 * k + 2] @ e_r)
                    worst_vr = max(worst_vr, abs(v_r))
                    r_dot = _pulse_radial_speed(float(t), big_r, eps, omega)
                    # the radial mismatch must be exactly the prescribed
                    # dr/dt: ||v_r - dr/dt| - |dr/dt|| isolates v_r
                    worst_ident = max(worst_ident, abs(abs(v_r - r_dot) - abs(r_dot)))
            sym.append(
                {
                    "N": n_sym,
                    "eps": eps,
                    "max_abs_induced_radial_velocity": worst_vr,
                    "radial_identity_max_abs_error": worst_ident,
                    "passed": worst_vr <= TOLERANCES["identity"]
                    and worst_ident <= TOLERANCES["identity"],
                }
            )

    shift = []
    for eps in eps_grid:
        worst_shape = 0.0
        worst_vr = 0.0
        for t in t_vals:
            state = np.zeros(2 * 3)
            for k in range(3):
                th = omega * float(t) + 2.0 * math.pi * k / 3.0
                r = big_r * (1.0 + eps * math.cos(th))
                state[2 * k] = r * math.cos(th)
                state[2 * k + 1] = r * math.sin(th)
            gamma_vec = np.full(3, gamma)
            worst_shape = max(worst_shape, cl.shape_deviation(state, gamma_vec, big_r))
            vel = md.vortex_rhs(state, gamma_vec)
            xy = state.reshape(3, 2)
            for k in range(3):
                pos = xy[k]
                e_r = pos / np.linalg.norm(pos)
                worst_vr = max(worst_vr, abs(float(vel[2 * k : 2 * k + 2] @ e_r)))
        shift.append(
            {
                "eps": eps,
                "max_shape_register_deviation": worst_shape,
                "max_abs_induced_radial_velocity": worst_vr,
            }
        )

    return {
        "check": (
            "W6 kinematic obstruction: symmetric pulsation violates the radial "
            "equation by |dr/dt|; the phase-shifted H1 shape is not a polygon"
        ),
        "symmetric_pulsation": sym,
        "phase_shifted_H1": shift,
        "params": {
            "R": big_r,
            "omega": omega,
            "Gamma": gamma,
            "t_grid": n_grid,
            "note": "the tangential register demands omega = G(N-1)/(4 pi r^2(t)), "
            "incompatible with any pulsation; see monograph Lemma C",
        },
        "passed": all(s["passed"] for s in sym),
    }


# ---------------------------------------------------------------------------
# W7 — the averaged-frequency bridge (Lemma D) and the D1 table
# ---------------------------------------------------------------------------


def _gauss_legendre(f, n_nodes: int) -> float:
    """INT_0^2pi f(phi) dphi by Gauss-Legendre on the mapped interval."""
    nodes, weights = np.polynomial.legendre.leggauss(int(n_nodes))
    phi = math.pi * (nodes + 1.0)  # map [-1, 1] -> [0, 2*pi]
    vals = f(phi)
    return float(math.pi * np.sum(weights * vals))


def check_w7_bridge(
    quad_nodes: int = 160, gamma: float = 1.0, cch_list: tuple = (3.0, 5.0, 10.0, 20.0)
) -> dict:
    """W7 — the averaged-frequency bridge.

    (a) integral identity: (1/2pi) * INT_0^2pi dphi/(1+eps cos phi)^2
        = (1 - eps^2)^(-3/2), certified by Gauss-Legendre quadrature;
    (b) the cycle-averaged kinematic frequency of the symmetric
        pulsating N-gon, <omega_kin> = Gamma*(N-1)/(4 pi R^2) *
        (1-eps^2)^(-3/2), independent of the modulation rate;
    (c) the compatibility table D1: the period T_comp(N, C_Ch) at which
        the Theorem 3.1 frequency law omega = (2 pi/T) e^(C_Ch/pi)
        equals <omega_kin> (with R^2 = C_Ch):
            T_comp = 2 pi e^(C_Ch/pi) * 4 pi C_Ch (1-eps^2)^(3/2) / (Gamma (N-1)).
    """
    eps_grid = (0.1, 0.3, 0.5, 0.7, 0.9)
    identity_err = 0.0
    for eps in eps_grid:
        numeric = _gauss_legendre(lambda phi: 1.0 / (1.0 + eps * np.cos(phi)) ** 2, quad_nodes)
        numeric /= 2.0 * math.pi
        exact = (1.0 - eps * eps) ** (-1.5)
        identity_err = max(identity_err, abs(numeric - exact) / exact)

    bridge_err = 0.0
    per_n = []
    for n in N_VALUES:
        freq_rows = []
        for eps in (0.2, 0.5, 0.8):
            big_r = 1.0
            base = cl.ngon_omega(gamma, big_r, n)
            numeric = _gauss_legendre(lambda phi: base / (1.0 + eps * np.cos(phi)) ** 2, quad_nodes)
            numeric /= 2.0 * math.pi
            exact = base * (1.0 - eps * eps) ** (-1.5)
            bridge_err = max(bridge_err, abs(numeric - exact) / exact)
            freq_rows.append({"eps": eps, "numeric": numeric, "exact": exact})
        per_n.append({"N": n, "avg_kinematic_frequency": freq_rows})

    table = []
    self_err = 0.0
    for c_ch in cch_list:
        eps = an.ansatz_amplitude(c_ch)
        if eps >= 1.0:
            table.append({"C_Ch": c_ch, "eps": eps, "admissible": False})
            continue
        for n in (3, 4, 5, 6, 7, 8):
            t_comp = (
                2.0
                * math.pi
                * math.exp(c_ch / math.pi)
                * 4.0
                * math.pi
                * c_ch
                * (1.0 - eps * eps) ** 1.5
                / (gamma * (n - 1))
            )
            omega_ans = an.ansatz_frequency(c_ch, t_comp)
            omega_avg = cl.ngon_omega(gamma, math.sqrt(c_ch), n) * (1.0 - eps * eps) ** (-1.5)
            self_err = max(self_err, abs(omega_ans - omega_avg) / omega_ans)
            table.append(
                {
                    "C_Ch": c_ch,
                    "N": n,
                    "eps": eps,
                    "T_comp": t_comp,
                    "omega_at_T_comp": omega_ans,
                    "admissible": True,
                }
            )
    return {
        "check": (
            "W7 averaged-frequency bridge: <omega_kin> = omega_N (1-eps^2)^(-3/2); "
            "compatibility periods T_comp(N, C_Ch) for the D1 design rule"
        ),
        "integral_identity_max_relative_error": identity_err,
        "bridge_max_relative_error": bridge_err,
        "compatibility_selfcheck_max_relative_error": self_err,
        "per_N": per_n,
        "compatibility_table": table,
        "params": {
            "Gamma": gamma,
            "quad_nodes": quad_nodes,
            "registered_pair_note": "the parent default (C_Ch=1, T=2pi) lies below "
            "the admissibility threshold pi*ln(2); see monograph Section 7",
        },
        "passed": (
            identity_err <= 1e-8  # quadrature resolution at eps = 0.9 (quick nodes)
            and bridge_err <= 1e-12
            and self_err <= TOLERANCES["identity"]
        ),
    }


# ---------------------------------------------------------------------------
# Runner of the whole ladder
# ---------------------------------------------------------------------------


def run_ladder(preset: str = "default") -> list:
    """Run W1..W7 with the named preset; returns the check dicts."""
    cfg = PRESETS[preset]
    return [
        check_w1_anchor(n_points=cfg["n_points"]),
        check_w2_ring_rotation(
            rotations=cfg["rotations"], steps_per_period=cfg["steps_per_period"]
        ),
        check_w3_invariants(rotations=cfg["rotations"], steps_per_period=cfg["steps_per_period"]),
        check_w4_stability(),
        check_w5_admissibility(cch_grid=cfg["cch_grid"]),
        check_w6_obstruction(),
        check_w7_bridge(quad_nodes=cfg["quad_nodes"]),
    ]
