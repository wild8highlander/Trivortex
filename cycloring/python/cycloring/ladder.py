#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
CYCLORING — THE VERIFICATION-AND-RESEARCH LADDER W1..W7
============================================================================
Seven stages; every stage returns the check-dictionary discipline
{"check": ..., numeric registers..., "params": {...}, "passed": bool}
and is bound by the runner to a deterministic JSON protocol.

    W1  The period core: the reflection register + P(1,1) = 1 + symmetry
    W2  The algebraic boundary: Omega(a, N-a) = pi/sin(pi a/N), sine product
    W3  The root system: prod(z - z_k) = z^N - sigma, moments, impulse
    W4  The polygon flow: rigid rotation, shape and invariants (RK4)
    W5  The transport identity: M[(1+eps cos u)^{-2}] = (1-eps^2)^{-3/2}
        and the exact phase advance 2 pi per closure period
    W6  The synchronous closure: rosettes return after T_c = 2 pi / nu
    W7  The transducer table: the four levels 7, 9, 15, 30

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import math
from typing import Dict, List

import mpmath as mp
import numpy as np

from . import chain as ch
from . import dynamics as dyn
from . import periods as per
from . import ring as rg

TOLERANCES = {
    "mp_identity": 1e-30,  # W1/W2: mpmath identities (50 working digits)
    "float_identity": 1e-12,  # W5/W7: float algebraic identities
    "root_system": 1e-10,  # W3: the binomial identity (scale-normalized)
    "moments": 1e-12,  # W3: the roots-of-unity filter (scale-normalized)
    "omega_rel_err": 1e-9,  # W4: measured vs analytic rotation rate
    "radius_drift": 1e-10,  # W4: shape of the free ring
    "invariant_drift": 1e-12,  # W4: relative drifts of H, P, Q, I
    "phase_advance": 1e-12,  # W5: 2 pi per closure period
    "closure": 1e-9,  # W6: the rosette return register
    "roundtrip": 1e-15,  # W7: eps <-> Delta round trip
}

LEVELS = (7, 9, 15, 30)

PRESETS = {
    "quick": {"rotations": 1, "steps_per_period": 1600, "eps_grid": 8},
    "default": {"rotations": 2, "steps_per_period": 2400, "eps_grid": 16},
    "full": {"rotations": 4, "steps_per_period": 6000, "eps_grid": 32},
}


# ---------------------------------------------------------------------------
# W1 — the period core
# ---------------------------------------------------------------------------


def check_w1_period_core(levels: tuple = LEVELS) -> dict:
    """W1 — the reflection register and the normalization of the periods.

    (a) Gamma(a/N) Gamma(1 - a/N) = pi / sin(pi a / N) at every level,
        every a = 1..N-1 (mpmath, 50 working digits);
    (b) P(1, 1) = 1 exactly (the normalization of the witness);
    (c) the symmetry Omega_{a,b} = Omega_{b,a}.
    """
    max_reflection = mp.mpf(0)
    for n in levels:
        for _, _, _, res in per.boundary_periods_mp(n):
            max_reflection = max(max_reflection, res)
    norm_err = max(abs(per.normalized_p_mp(1, 1, n) - 1) for n in levels)
    sym_err = max(
        abs(per.omega_mp(a, b, n) - per.omega_mp(b, a, n))
        for n in levels
        for a in (1, 2)
        for b in (3, n - 1)
        if a != b
    )
    return {
        "check": "W1 period core: reflection register + P(1,1)=1 + symmetry",
        "max_reflection_residual": float(max_reflection),
        "normalization_error": float(norm_err),
        "symmetry_error": float(sym_err),
        "params": {"levels": list(levels), "mp_dps": per.MP_DPS},
        "passed": (
            float(max_reflection) <= TOLERANCES["mp_identity"]
            and float(norm_err) <= TOLERANCES["mp_identity"]
            and float(sym_err) <= TOLERANCES["mp_identity"]
        ),
    }


# ---------------------------------------------------------------------------
# W2 — the algebraic boundary
# ---------------------------------------------------------------------------


def check_w2_algebraic_boundary(levels: tuple = LEVELS) -> dict:
    """W2 — the boundary of the period domain is algebraic (times pi).

    (a) Omega(a, N - a) = pi / sin(pi a / N) exactly, all levels;
    (b) the sine product prod_m 2 sin(pi m / N) = N exactly.
    """
    max_boundary = mp.mpf(0)
    for n in levels:
        for _, _, _, res in per.boundary_periods_mp(n):
            max_boundary = max(max_boundary, res)
    max_sine = max(float(per.sine_product_residual_mp(n)) for n in levels)
    return {
        "check": "W2 algebraic boundary: Omega(a,N-a)=pi/sin + sine product",
        "max_boundary_residual": float(max_boundary),
        "max_sine_product_residual": max_sine,
        "params": {"levels": list(levels), "mp_dps": per.MP_DPS},
        "passed": (
            float(max_boundary) <= TOLERANCES["mp_identity"]
            and max_sine <= TOLERANCES["mp_identity"]
        ),
    }


# ---------------------------------------------------------------------------
# W3 — the root system
# ---------------------------------------------------------------------------


def _root_registers(n: int) -> Dict[str, float]:
    zs = rg.polygon_positions(n, 1.0, 0.3)
    root_res = rg.root_system_residual(zs)
    sums = rg.moment_sums(zs)
    mom_err = 0.0
    for m, s in enumerate(sums[: n - 1], start=1):
        mom_err = max(mom_err, abs(s) / (1.0**m))
    sigma = (-1) ** (n - 1) * complex(np.prod(zs))  # = r^N exp(i N theta0)
    sn_err = abs(sums[n - 1] - n * sigma) / (n * 1.0**n)
    imp_err = abs(rg.impulse(zs))
    return {
        "root_system_residual": root_res,
        "moment_residual": mom_err,
        "s_n_residual": sn_err,
        "impulse_residual": imp_err,
    }


def check_w3_root_system(levels: tuple = (7, 9, 15)) -> dict:
    """W3 — the ring is the root system of z^N = sigma (Theorem 1)."""
    per_level = {str(n): _root_registers(n) for n in levels}
    worst_root = max(v["root_system_residual"] for v in per_level.values())
    worst_mom = max(v["moment_residual"] for v in per_level.values())
    worst_sn = max(v["s_n_residual"] for v in per_level.values())
    worst_imp = max(v["impulse_residual"] for v in per_level.values())
    return {
        "check": "W3 root system: z^N - sigma identity + moments + impulse",
        "per_level": per_level,
        "worst_root_system_residual": worst_root,
        "worst_moment_residual": worst_mom,
        "worst_s_n_residual": worst_sn,
        "worst_impulse_residual": worst_imp,
        "params": {"levels": list(levels)},
        "passed": (
            worst_root <= TOLERANCES["root_system"]
            and worst_mom <= TOLERANCES["moments"]
            and worst_sn <= TOLERANCES["moments"]
            and worst_imp <= TOLERANCES["moments"]
        ),
    }


# ---------------------------------------------------------------------------
# W4 — the polygon flow
# ---------------------------------------------------------------------------


def check_w4_polygon_flow(
    n: int = 7,
    gamma: float = 1.0,
    big_r: float = 1.0,
    rotations: int = 2,
    steps_per_period: int = 2400,
) -> dict:
    """W4 — the free ring rotates rigidly at omega_L; shape and invariants held.

    The polygon invariance register: the Kirchhoff flow from the frozen
    polygon keeps |z_k| = R to solver accuracy and transports the phase at
    exactly omega_L = Gamma (N - 1) / (4 pi R^2).
    """
    omega_l = rg.frozen_rate(n, gamma, big_r)
    t_period = 2.0 * math.pi / omega_l
    dt = t_period / steps_per_period
    n_steps = int(rotations * steps_per_period)

    gamma_vec = np.full(n, gamma)
    state0 = rg.polygon_positions_xy(n, big_r, 0.0)
    inv0 = dyn.invariants(state0, gamma_vec)

    state = state0.copy()
    traj_last = state0
    max_radius_drift = 0.0
    for step in range(1, n_steps + 1):
        state = dyn.rk4_step(state, gamma_vec, dt)
        xy = state.reshape(n, 2)
        radii = np.hypot(xy[:, 0], xy[:, 1])
        max_radius_drift = max(max_radius_drift, float(np.max(np.abs(radii - big_r))))
        if step == n_steps:
            traj_last = state.copy()

    # measured rate via the unwrapped angle of vortex 0
    xy = traj_last.reshape(n, 2)
    ang = math.atan2(xy[0, 1], xy[0, 0])
    t_total = n_steps * dt
    # the ring made floor(omega t_total / 2pi) full turns
    full_turns = int(math.floor((omega_l * t_total + math.pi) / (2.0 * math.pi)))
    measured = (ang + 2.0 * math.pi * full_turns) / t_total
    omega_rel_err = abs(measured - omega_l) / omega_l

    inv1 = dyn.invariants(traj_last, gamma_vec)
    drifts = dyn.relative_drifts(inv0, inv1)
    worst_drift = max(drifts.values())

    # the closed-form Hamiltonian register (Theorem 5)
    h_closed = dyn.hamiltonian_closed_form(n, big_r, gamma)
    h_err = abs(inv0["H"] - h_closed) / max(abs(h_closed), 1.0)
    prod_err = abs(
        dyn.distance_product(n, big_r) - _distance_product_measured(state0, n)
    ) / dyn.distance_product(n, big_r)

    return {
        "check": "W4 polygon flow: rigid rotation + shape + invariants + H form",
        "omega_analytic": omega_l,
        "omega_measured": measured,
        "omega_relative_error": omega_rel_err,
        "max_radius_drift": max_radius_drift,
        "invariant_drifts": drifts,
        "worst_invariant_drift": worst_drift,
        "h_closed_form_error": h_err,
        "distance_product_error": prod_err,
        "params": {
            "N": n,
            "Gamma": gamma,
            "R": big_r,
            "rotations": rotations,
            "steps_per_period": steps_per_period,
        },
        "passed": (
            omega_rel_err <= TOLERANCES["omega_rel_err"]
            and max_radius_drift <= TOLERANCES["radius_drift"]
            and worst_drift <= TOLERANCES["invariant_drift"]
            and h_err <= TOLERANCES["float_identity"]
            and prod_err <= TOLERANCES["float_identity"]
        ),
    }


def _distance_product_measured(state: np.ndarray, n: int) -> float:
    """Direct pairwise distance product of the polygon state."""
    xy = np.asarray(state, dtype=float).reshape(n, 2)
    diff = xy[np.newaxis, :, :] - xy[:, np.newaxis, :]
    dist = np.sqrt(np.sum(diff * diff, axis=2))
    iu = np.triu_indices(n, k=1)
    return float(np.prod(dist[iu]))


# ---------------------------------------------------------------------------
# W5 — the transport identity
# ---------------------------------------------------------------------------


def check_w5_transport_identity(eps_grid: int = 16) -> dict:
    """W5 — M[(1+eps cos u)^{-2}] = (1-eps^2)^{-3/2} and the 2 pi advance.

    (a) the mean-transport identity at mpmath precision over the eps grid;
    (b) the float scan of the quadrature mean against the closed form;
    (c) the exact phase advance 2 pi per closure period for the
        synchronous frequency.
    """
    eps_values = [0.05 + 0.55 * i / max(eps_grid - 1, 1) for i in range(eps_grid)]
    with mp.workdps(per.MP_DPS):
        worst_mp = mp.mpf(0)
        for eps in eps_values:
            e = mp.mpf(eps)
            mean = mp.quad(lambda u: 1 / (1 + e * mp.cos(u)) ** 2, [0, 2 * mp.pi]) / (2 * mp.pi)
            worst_mp = max(worst_mp, abs(mean - (1 - e * e) ** (-mp.mpf("1.5"))))
    worst_float = 0.0
    for eps in eps_values:
        worst_float = max(
            worst_float,
            abs(rg.mean_transport_ratio(eps) - 1.0 / (1.0 - eps * eps) ** 1.5),
        )
    # the phase advance register: exactly 2 pi over T_c
    phase_err = 0.0
    for eps in (eps_values[0], eps_values[len(eps_values) // 2], eps_values[-1]):
        n, big_r, gamma = 7, 1.0, 1.0
        nu = rg.synchronous_frequency(big_r, eps, gamma, n)
        t_c = rg.closure_time(eps, nu)
        phase = rg.transport_phase(t_c, big_r, eps, gamma, n)
        phase_err = max(phase_err, abs(phase - 2.0 * math.pi))
    return {
        "check": "W5 transport identity: mean law + exact 2 pi phase advance",
        "max_mp_residual": float(worst_mp),
        "max_float_residual": worst_float,
        "max_phase_advance_error": phase_err,
        "params": {
            "eps_grid": eps_values[:3] + ["..."] + eps_values[-1:],
            "n_eps": len(eps_values),
        },
        "passed": (
            float(worst_mp) <= TOLERANCES["mp_identity"]
            and worst_float <= TOLERANCES["float_identity"]
            and phase_err <= TOLERANCES["phase_advance"]
        ),
    }


# ---------------------------------------------------------------------------
# W6 — the synchronous closure
# ---------------------------------------------------------------------------


def check_w6_synchronous_closure(n: int = 7, gamma: float = 1.0, big_r: float = 1.0) -> dict:
    """W6 — the synchronous program closes: z_k(T_c) = z_k(0), shape rigid.

    The modulation amplitude is the transducer output eps_7 of the level;
    the frequency is the synchronous law. Registers:
    (a) the closure residual max_k |z_k(T_c) - z_k(0)|;
    (b) the shape rigidity |z_k| identical along the program;
    (c) the breathing is real: the radial excursion equals 2 R eps.
    """
    row = ch.defect_chain(n, gamma, big_r)
    eps = row["eps"]
    nu = rg.synchronous_frequency(big_r, eps, gamma, n)
    t_c = rg.closure_time(eps, nu)
    clos = rg.closure_residual(n, big_r, eps, nu)
    shape_err = 0.0
    for frac in (0.13, 0.37, 0.61, 0.89):
        zs = rg.pumped_positions(frac * t_c, n, big_r, eps, nu)
        radii = np.abs(zs)
        shape_err = max(shape_err, float(np.max(radii) - np.min(radii)))
    excursion = 2.0 * big_r * eps
    return {
        "check": "W6 synchronous closure: rosette return + shape rigidity",
        "eps_level": eps,
        "nu_synchronous": nu,
        "closure_time": t_c,
        "closure_residual": clos,
        "shape_rigidity_residual": shape_err,
        "radial_excursion": excursion,
        "params": {"N": n, "Gamma": gamma, "R": big_r},
        "passed": (
            clos <= TOLERANCES["closure"]
            and shape_err <= TOLERANCES["closure"]
            and excursion > 1e-3
        ),
    }


# ---------------------------------------------------------------------------
# W7 — the transducer table
# ---------------------------------------------------------------------------


def check_w7_transducer(levels: tuple = LEVELS) -> dict:
    """W7 — the transducer table of the four cyclotomic levels.

    Registers:
    (a) the full chain rows delta, k, gamma, delta_eff, W_N, Delta_Ch,
        eps, nu/omega_L, C_N for N = 7, 9, 15, 30;
    (b) the stiffness ordering eps_7 > eps_9 > eps_15 > eps_30 and
        C_7 < C_9 < C_15 < C_30;
    (c) the exact round trip Delta = eps / (1 - eps);
    (d) the frequency consistency ((1+D)/(1+2D))^{3/2} = (1-eps^2)^{-3/2};
    (e) the classical limit: Delta -> 0 gives eps -> 0, nu -> omega_L.
    """
    rows = ch.level_table(levels)
    eps_seq = [row["eps"] for row in rows]
    c_seq = [row["c_log"] for row in rows]
    monotone = all(eps_seq[i] > eps_seq[i + 1] for i in range(len(eps_seq) - 1))
    monotone_c = all(c_seq[i] < c_seq[i + 1] for i in range(len(c_seq) - 1))
    roundtrip_err = 0.0
    freq_err = 0.0
    for row in rows:
        d = row["Delta_Ch"]
        roundtrip_err = max(roundtrip_err, abs(ch.inverse_transducer(row["eps"]) - d) / d)
        freq_err = max(freq_err, abs(row["nu_ratio"] - 1.0 / (1.0 - row["eps"] ** 2) ** 1.5))
    eps_small, nu_small, _ = ch.transducer(1e-9)
    classical_ok = eps_small <= 2e-9 and abs(nu_small - 1.0) <= 2e-9
    table = [
        {
            "N": int(row["N"]),
            "k": int(row["k"]),
            "delta": row["delta"],
            "gamma": row["gamma"],
            "delta_eff": row["delta_eff"],
            "W": row["W"],
            "Delta_Ch": row["Delta_Ch"],
            "eps": row["eps"],
            "nu_ratio": row["nu_ratio"],
            "C_N": row["c_log"],
        }
        for row in rows
    ]
    return {
        "check": "W7 transducer: level table + ordering + round trip + limit",
        "table": table,
        "eps_monotone": monotone,
        "c_log_monotone": monotone_c,
        "max_roundtrip_error": roundtrip_err,
        "max_frequency_identity_error": freq_err,
        "classical_limit_ok": classical_ok,
        "params": {"levels": list(levels)},
        "passed": (
            monotone
            and monotone_c
            and roundtrip_err <= TOLERANCES["roundtrip"]
            and freq_err <= TOLERANCES["float_identity"]
            and classical_ok
        ),
    }


# ---------------------------------------------------------------------------
# The ladder driver
# ---------------------------------------------------------------------------

STAGES = {
    "W1": lambda preset: check_w1_period_core(),
    "W2": lambda preset: check_w2_algebraic_boundary(),
    "W3": lambda preset: check_w3_root_system(),
    "W4": lambda preset: check_w4_polygon_flow(
        rotations=preset["rotations"], steps_per_period=preset["steps_per_period"]
    ),
    "W5": lambda preset: check_w5_transport_identity(eps_grid=preset["eps_grid"]),
    "W6": lambda preset: check_w6_synchronous_closure(),
    "W7": lambda preset: check_w7_transducer(),
}


def run_stage(stage: str, preset_name: str = "default") -> dict:
    """Run one stage of the ladder on the given preset."""
    if stage not in STAGES:
        raise KeyError(f"unknown stage {stage}")
    return STAGES[stage](PRESETS[preset_name])


def run_all(preset_name: str = "default") -> Dict[str, dict]:
    """Run the whole ladder W1..W7."""
    out: Dict[str, dict] = {}
    for stage in STAGES:
        out[stage] = run_stage(stage, preset_name)
    return out
