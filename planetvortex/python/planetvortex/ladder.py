#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
PLANETVORTEX — THE P-LADDER: SEVEN REGISTERED STAGES (P1..P7)
============================================================================
The verification ladder of the planetary bench. Every stage carries a
registered tolerance committed BEFORE the recorded run, and every run
writes a deterministic JSON protocol (runner.py) into
results/protocols/ — the same "every number is bound to a run"
discipline as the parent framework and the polyvortex bench.

    P1  the anchor: the exact figure literals + the Kepler-Earth anchor
    P2  the Kepler register: T^2/a^3 (1 + m/M) uniform over the 8 planets
    P3  the planetary N-body: conservation + osculating elements + periods
    P4  the PSL(2,7) algebra: 168 automorphisms, incidence, congruence
    P5  the heptagon lattice: rigid rotation, invariants, Havelock N = 7
    P6  the seven cells: integrable Fano triads, congruent shape cycles
    P7  the gravity bridge: Schwarzschild ladder, Hill margins, the
        mass-ladder deficit diagnostics

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import math
from typing import Any, Dict, List

import numpy as np

from . import classical as cl
from . import fano as fn
from . import model as md
from . import nbody as nb

TWO_PI = 2.0 * math.pi

# ---------------------------------------------------------------------------
# Registered tolerances (committed before the recorded runs)
# ---------------------------------------------------------------------------

TOLERANCES: Dict[str, float] = {
    "float_literal": 1e-15,  # float64 against the mpmath closed forms
    "kepler_earth_si": 1e-4,  # the data-bound Kepler anchor (P1)
    "kepler_spread": 1e-4,  # the corrected register spread (P2)
    "nbody_energy": 1e-9,  # relative energy drift (P3)
    "nbody_am": 1e-10,  # relative angular-momentum drift (P3)
    "element_a_rel": 1e-2,  # osculating a against the committed table
    "element_e_abs": 1e-2,  # osculating e against the committed table
    "period_dyn_rel": 1e-4,  # Kepler III of the integrated motion
    "stability_tol": 1e-7,  # the Havelock classifier (P5)
    "kepler_dynamic": 1e-9,  # the two-body Kepler register (P2)
    "omega_rel": 1e-9,  # heptagon rotation measured vs analytic
    "inv_drift": 1e-12,  # vortex invariants along the ring (P5)
    "hamiltonian_literal": 1e-13,  # H_ring against the sqrt(7) closed form
    "cell_inv_drift": 1e-12,  # the cells' H, I along the shape cycle
    "cell_period_rel": 1e-6,  # pairwise congruence of the shape periods
    "shape_return_residual": 1e-3,  # the descriptor at the shape return
    "not_re_min": 0.2,  # the cells are NOT relative equilibria
    "chord_congruence": 1e-12,  # the 7 line-triangles are congruent (P4)
    "schwartz_rel": 1e-12,  # the Schwarzschild arithmetic (P7)
    "hill_margin_min": 3.0,  # min adjacent Hill margin (P7)
}

# ---------------------------------------------------------------------------
# Presets: integration effort against wall time
# ---------------------------------------------------------------------------

PRESETS: Dict[str, Dict[str, Any]] = {
    "quick": {
        "dps": 25,
        "nbody_years": 4.0,
        "nbody_dt": 0.001,
        "nbody_sample_every": 4,
        "p2_revolutions": 2,
        "p2_steps_per_revolution": 1800,
        "vortex_rotations": 1.0,
        "ring_steps_per_rotation": 1200,
        "cell_tmax": 120.0,
        "cell_dt": 0.008,
        "cell_sample_every": 4,
    },
    "default": {
        "dps": 30,
        "nbody_years": 12.0,
        "nbody_dt": 0.0002,
        "nbody_sample_every": 8,
        "p2_revolutions": 2,
        "p2_steps_per_revolution": 3600,
        "vortex_rotations": 2.0,
        "ring_steps_per_rotation": 2400,
        "cell_tmax": 240.0,
        "cell_dt": 0.004,
        "cell_sample_every": 4,
    },
    "full": {
        "dps": 50,
        "nbody_years": 40.0,
        "nbody_dt": 0.0001,
        "nbody_sample_every": 20,
        "p2_revolutions": 4,
        "p2_steps_per_revolution": 7200,
        "vortex_rotations": 4.0,
        "ring_steps_per_rotation": 4800,
        "cell_tmax": 480.0,
        "cell_dt": 0.002,
        "cell_sample_every": 2,
    },
}


# ---------------------------------------------------------------------------
# P1 — the anchor: exact figure literals + the Kepler-Earth anchor
# ---------------------------------------------------------------------------


def check_p1_anchor(dps: int = 30) -> Dict[str, Any]:
    """P1: the exact dimensions of the figure, pinned; Earth's Kepler
    register against the SI Kepler constant of the committed data."""
    exact = fn.exact_literals(dps)
    s1, s2, s3 = fn.chord_classes(1.0)
    geom = fn.line_triangle_geometry(fn.cyclic_line_triples()[0], 1.0)

    def rel(a: float, b: float) -> float:
        return abs(a - b) / max(abs(b), 1e-300)

    chord_errors = {
        "s1": rel(s1, float(exact["s1"])),
        "s2": rel(s2, float(exact["s2"])),
        "s3": rel(s3, float(exact["s3"])),
    }
    angle_errors = [
        rel(a, float(e))
        for a, e in zip(geom["angles"], (exact["angle1"], exact["angle2"], exact["angle3"]))
    ]
    area_error = rel(geom["area"], float(exact["cell_area"]))
    omega_error = rel(fn.ring_omega(1.0, 1.0), float(exact["omega7"]))

    earth = cl.PLANETS[cl.EARTH_INDEX]
    # the SI Kepler anchor: T^2/a^3 (1 + m/M) against 4*pi^2/GM_sun
    t_s = earth.period_days * 86400.0
    a_m = earth.a_au * cl.AU_M
    k_earth = t_s * t_s / a_m**3 * (1.0 + cl.solar_mass_ratio(earth))
    k_constant = 4.0 * math.pi * math.pi / cl.GM_SUN
    kepler_err = abs(k_earth - k_constant) / k_constant

    tol = TOLERANCES
    passed = (
        max(chord_errors.values()) <= tol["float_literal"]
        and max(angle_errors) <= tol["float_literal"]
        and area_error <= tol["float_literal"]
        and omega_error <= tol["float_literal"]
        and kepler_err <= tol["kepler_earth_si"]
    )
    return {
        "check": (
            "P1 anchor: exact figure literals (s1, s2, s3, angles pi/7 : 2pi/7 : 4pi/7, "
            "area sqrt(7)/4, omega7 = 3/2pi) + the Kepler-Earth anchor vs 4pi^2/GM_sun"
        ),
        "exact_literals": exact,
        "chord_relative_errors": chord_errors,
        "angle_relative_errors": angle_errors,
        "area_relative_error": area_error,
        "omega_relative_error": omega_error,
        "kepler_earth_si_value": k_earth,
        "kepler_earth_si_constant": k_constant,
        "kepler_earth_relative_error": kepler_err,
        "params": {"dps": dps, "big_r": 1.0, "au_m": cl.AU_M, "gm_sun": cl.GM_SUN},
        "passed": bool(passed),
    }


# ---------------------------------------------------------------------------
# P2 — the Kepler register: Kepler III certified in the two-body dynamics
# ---------------------------------------------------------------------------


def _two_body_rhs(state: np.ndarray, mu: float) -> np.ndarray:
    """Planar relative two-body RHS: state = [x, y, vx, vy]."""
    r = math.hypot(state[0], state[1])
    acc = -mu * state[:2] / (r * r * r)
    return np.array([state[2], state[3], acc[0], acc[1]])


def _two_body_rk4(state: np.ndarray, mu: float, dt: float) -> np.ndarray:
    k1 = _two_body_rhs(state, mu)
    k2 = _two_body_rhs(state + 0.5 * dt * k1, mu)
    k3 = _two_body_rhs(state + 0.5 * dt * k2, mu)
    k4 = _two_body_rhs(state + dt * k3, mu)
    return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def _two_body_period(
    planet: cl.Planet, mu: float, n_revolutions: int, steps_per_revolution: int
) -> float:
    """Measure the two-body period from perihelion-passage minima.

    The body starts at perihelion; the (parabolically interpolated)
    times of the first n_revolutions+1 perihelion minima of r give
    T = (t_N - t_0)/n_revolutions. The systematic bias of the parabolic
    fit cancels between minima to (n*dt)^4 — far below the register.
    """
    a, e = planet.a_au, planet.e
    mu_loc = mu
    state = np.array([a * (1.0 - e), 0.0, 0.0, math.sqrt(mu_loc * (1.0 + e) / (a * (1.0 - e)))])
    t_analytic = TWO_PI * math.sqrt(a**3 / mu_loc)
    dt = t_analytic / steps_per_revolution
    r_prev = float(np.hypot(state[0], state[1]))
    t_prev = 0.0
    minima: List[float] = []
    total_steps = int(round((n_revolutions + 1.2) * steps_per_revolution))
    r_values = [r_prev]
    t_values = [t_prev]
    for step in range(1, total_steps + 1):
        state = _two_body_rk4(state, mu_loc, dt)
        r = float(np.hypot(state[0], state[1]))
        t = step * dt
        r_values.append(r)
        t_values.append(t)
        if len(r_values) >= 3 and r_values[-2] < r_values[-3] and r_values[-2] < r_values[-1]:
            # parabolic vertex through the last three samples
            r0, r1, r2 = r_values[-3], r_values[-2], r_values[-1]
            denom = r0 - 2.0 * r1 + r2
            frac = 0.5 * (r0 - r2) / denom if denom != 0 else 0.0
            minima.append(t_values[-2] + frac * dt)
            if len(minima) > n_revolutions:
                break
    if len(minima) <= n_revolutions:
        raise RuntimeError(f"perihelion minima not found for {planet.name}")
    return (minima[n_revolutions] - minima[0]) / n_revolutions


def check_p2_kepler(n_revolutions: int = 2, steps_per_revolution: int = 3600) -> Dict[str, Any]:
    """P2: Kepler III certified in the two-body dynamics of every planet.

    For each planet the pure two-body orbit (Sun + planet, mu_i =
    4pi^2 (1 + m_i/M_sun)) is integrated from perihelion and the period
    measured from interpolated perihelion passages. Registers: the
    corrected deviation |T_meas - T_analytic(mu_i)|/T is at integration
    precision; the UNCORRECTED comparison (mu_0 = 4pi^2) shows the
    physical signature m_i/2M_sun of the mass correction (Lemma D).
    The fact-sheet periods of the committed table are recorded as a
    provenance diagnostic (they are rounded and epoch-mixed).
    """
    rows: List[Dict[str, Any]] = []
    worst_corr = 0.0
    worst_uncorr = 0.0
    worst_sheet = 0.0
    worst_sheet_name = ""
    for p in cl.PLANETS:
        m_ratio = cl.solar_mass_ratio(p)
        t_meas = _two_body_period(p, cl.mu_planet(p), n_revolutions, steps_per_revolution)
        t_corr = cl.kepler_period_years(p)
        t_uncorr = TWO_PI * math.sqrt(p.a_au**3 / cl.MU_SUN)
        dev_corr = abs(t_meas - t_corr) / t_corr
        dev_uncorr = abs(t_meas - t_uncorr) / t_uncorr
        t_sheet = p.period_days / 365.25
        dev_sheet = abs(t_sheet - t_corr) / t_corr
        worst_corr = max(worst_corr, dev_corr)
        worst_uncorr = max(worst_uncorr, dev_uncorr)
        if dev_sheet > worst_sheet:
            worst_sheet = dev_sheet
            worst_sheet_name = p.name
        rows.append(
            {
                "planet": p.name,
                "a_au": p.a_au,
                "mass_ratio": m_ratio,
                "T_measured_years": t_meas,
                "T_kepler_corrected_years": t_corr,
                "T_kepler_uncorrected_years": t_uncorr,
                "deviation_corrected_relative": dev_corr,
                "deviation_uncorrected_relative": dev_uncorr,
                "mass_signature_predicted": m_ratio / 2.0,
                "T_factsheet_years": t_sheet,
                "factsheet_deviation_relative": dev_sheet,
            }
        )
    improvement = worst_uncorr / worst_corr if worst_corr > 0 else float("inf")
    passed = worst_corr <= TOLERANCES["kepler_dynamic"]
    return {
        "check": (
            "P2 Kepler register: the two-body period of every planet matches "
            "2*pi*sqrt(a^3/(4pi^2(1+m/M))) at integration precision; the "
            "uncorrected formula misses by m_i/2M_sun (Jupiter ~4.8e-4); the "
            "fact-sheet periods are a recorded provenance diagnostic"
        ),
        "per_planet": rows,
        "worst_deviation_corrected": worst_corr,
        "worst_deviation_uncorrected": worst_uncorr,
        "correction_improvement_factor": improvement,
        "factsheet_worst_deviation": worst_sheet,
        "factsheet_worst_planet": worst_sheet_name,
        "params": {
            "n_revolutions": n_revolutions,
            "steps_per_revolution": steps_per_revolution,
            "integrator": "RK4, perihelion minima, parabolic interpolation",
        },
        "passed": bool(passed),
    }


# ---------------------------------------------------------------------------
# P3 — the planetary N-body simulation
# ---------------------------------------------------------------------------


def check_p3_nbody(
    years: float = 12.0, dt: float = 0.0002, sample_every: int = 15
) -> Dict[str, Any]:
    """P3: the full Newtonian Sun + 8 planets integration.

    Registers: energy and angular-momentum conservation; the osculating
    (a, e) of every planet at the end of the window against the
    committed table; Kepler III measured from the integrated motion
    around the secular mean element; the perturbation hierarchy.
    """
    masses = nb.planet_masses()
    state0 = nb.initial_state()
    n_steps = int(round(years / dt))
    state_end, traj = nb.integrate(state0, masses, dt, n_steps, sample_every=sample_every)

    e0 = nb.total_energy(state0, masses)
    e1 = nb.total_energy(state_end, masses)
    l0 = nb.total_angular_momentum(state0, masses)
    l1 = nb.total_angular_momentum(state_end, masses)
    energy_drift = abs(e1 - e0) / max(abs(e0), 1e-30)
    am_drift = abs(l1 - l0) / max(abs(l0), 1e-30)

    t_total = n_steps * dt
    times = np.linspace(0.0, t_total, traj.shape[0])
    planet_rows: List[Dict[str, Any]] = []
    worst_a = 0.0
    worst_e = 0.0
    worst_dyn = 0.0
    for k, p in enumerate(cl.PLANETS):
        a_end, e_end = nb.osculating_elements(state_end, k)
        dev_a = abs(a_end - p.a_au) / p.a_au
        dev_e = abs(e_end - p.e)
        worst_a = max(worst_a, dev_a)
        worst_e = max(worst_e, dev_e)
        # the secular mean element and the measured mean motion over
        # INTEGER revolutions (the partial-revolution bias excluded)
        sun_xy = traj[:, 0, :2]
        rel_xy = traj[:, k + 1, :2] - sun_xy
        rel_v = traj[:, k + 1, 2:] - traj[:, 0, 2:]
        angles = np.arctan2(rel_xy[:, 1], rel_xy[:, 0])
        unwrapped = np.unwrap(angles)
        total_angle = float(unwrapped[-1] - unwrapped[0])
        revolutions = total_angle / TWO_PI
        period_dyn: Dict[str, Any] = {
            "measured": False,
            "revolutions": revolutions,
        }
        if revolutions >= 1.05:
            k_rev = int(math.floor(revolutions))
            target = float(unwrapped[0]) + k_rev * TWO_PI
            cross = np.where(unwrapped >= target)[0]
            i_cross = int(cross[0])
            u0, u1 = float(unwrapped[i_cross - 1]), float(unwrapped[i_cross])
            frac = (target - u0) / (u1 - u0)
            t_cross = times[i_cross - 1] + frac * (times[i_cross] - times[i_cross - 1])
            n_meas = k_rev * TWO_PI / t_cross
            mu = cl.mu_planet(p)
            a_window = []
            for i in range(i_cross + 1):
                a_t, _ = cl.osculating_a_e(
                    float(rel_xy[i, 0]),
                    float(rel_xy[i, 1]),
                    float(rel_v[i, 0]),
                    float(rel_v[i, 1]),
                    mu,
                )
                a_window.append(a_t)
            a_mean = float(np.mean(a_window))
            dyn_dev = abs(n_meas**2 * a_mean**3 / mu - 1.0)
            worst_dyn = max(worst_dyn, dyn_dev)
            period_dyn = {
                "measured": True,
                "revolutions_used": k_rev,
                "a_mean_au": a_mean,
                "n_measured": n_meas,
                "n_kepler_mean_element": math.sqrt(mu / a_mean**3),
                "kepler3_dynamic_deviation": dyn_dev,
                "T_measured_days": TWO_PI / n_meas * 365.25,
                "T_committed_days": p.period_days,
            }
        planet_rows.append(
            {
                "planet": p.name,
                "a_end_au": a_end,
                "e_end": e_end,
                "a_deviation_relative": dev_a,
                "e_deviation": dev_e,
                "kepler_dynamic": period_dyn,
            }
        )
    hierarchy = nb.perturbation_hierarchy(state_end)
    measured = [r for r in planet_rows if r["kepler_dynamic"]["measured"]]
    tol = TOLERANCES
    passed = (
        energy_drift <= tol["nbody_energy"]
        and am_drift <= tol["nbody_am"]
        and worst_a <= tol["element_a_rel"]
        and worst_e <= tol["element_e_abs"]
        and worst_dyn <= tol["period_dyn_rel"]
        and len(measured) >= 3
    )
    return {
        "check": (
            "P3 planetary N-body: energy + angular-momentum conservation, osculating "
            "elements within the secular band, Kepler III of the integrated motion "
            "over integer revolutions around the secular mean element, the "
            "perturbation hierarchy"
        ),
        "energy_drift_relative": energy_drift,
        "angular_momentum_drift_relative": am_drift,
        "worst_a_deviation_relative": worst_a,
        "worst_e_deviation": worst_e,
        "worst_kepler3_dynamic_deviation": worst_dyn,
        "max_perturbation_ratio": hierarchy["max_perturbation_ratio"],
        "per_planet": planet_rows,
        "params": {
            "years": years,
            "dt": dt,
            "n_steps": n_steps,
            "sample_every": sample_every,
            "bodies": 9,
        },
        "passed": bool(passed),
    }


# ---------------------------------------------------------------------------
# P4 — the PSL(2,7) algebra register (exact, tolerance zero)
# ---------------------------------------------------------------------------


def check_p4_algebra() -> Dict[str, Any]:
    """P4: the exact combinatorics of the structure.

    The cyclic model: 168 line-preserving permutations of Z_7, closure,
    inverses, transitivity, stabilizer orders, the pair axiom. The
    binary model: |GL(3,2)| = 168. The bridge: an explicit
    line-preserving bijection Z_7 -> F_2^3 and the conjugacy of the two
    group copies inside S_7. The geometry: the seven line-triangles are
    congruent with angles (pi/7, 2pi/7, 4pi/7) and area sqrt(7)/4.
    """
    lines = fn.fano_lines()
    group = fn.automorphism_group()
    group_set = set(group)
    order = len(group)
    identity = tuple(range(7))
    has_identity = identity in group_set
    # closure + inverses (exhaustive: 168^2 compositions)
    closed = True
    inverses = True
    for a in group:
        found_inv = False
        for b in group:
            comp = tuple(a[b[i]] for i in range(7))
            if comp not in group_set:
                closed = False
            if comp == identity:
                found_inv = True
        inverses = inverses and found_inv
    # transitivity on points
    orbit = {perm[0] for perm in group}
    transitive = orbit == set(range(7))
    # stabilizer orders (orbit-stabilizer: 168/7 = 24)
    stab_point = sum(1 for perm in group if perm[0] == 0)
    stab_line = sum(1 for perm in group if tuple(sorted(perm[i] for i in lines[0])) == lines[0])
    # the pair axiom: every pair of points on exactly one line
    pair_ok = True
    for i in range(7):
        for j in range(i + 1, 7):
            cnt = sum(1 for line in lines if i in line and j in line)
            if cnt != 1:
                pair_ok = False
    # the binary model: 168 invertible matrices over F_2
    group_b = fn.gl3_2()
    order_b = len(group_b)
    labels_b = fn.binary_labels()
    # GL(3,2) as permutations of the label indices 0..6
    label_idx = {lab: u for u, lab in enumerate(labels_b)}
    perms_b = set()
    for m in group_b:
        perm = tuple(label_idx[fn.gl3_2_action(m, lab)] for lab in labels_b)
        perms_b.add(perm)
    # the explicit isomorphism and its conjugacy
    phi = fn.find_isomorphism()
    isomorphism_found = phi is not None
    conjugate = False
    if isomorphism_found:
        phi_map = phi
        assert phi_map is not None
        inv_phi = {lab: z for z, lab in phi_map.items()}
        conj = set()
        for perm in group:
            # phi o sigma o phi^{-1}, as a permutation of the label indices
            imgs = []
            for u, lab in enumerate(labels_b):
                z = inv_phi[lab]
                zp = perm[z]
                imgs.append(label_idx[phi_map[zp]])
            conj.add(tuple(imgs))
        conjugate = conj == perms_b
        # the induced map on lines is a bijection of line sets
        idx_of_label = {lab: u for u, lab in enumerate(labels_b)}
        lines_b_idx = {
            tuple(sorted(idx_of_label[lab] for lab in line)) for line in fn.binary_lines()
        }
        mapped = {tuple(sorted(idx_of_label[phi_map[z]] for z in line)) for line in lines}
        lines_map_onto_lines = mapped == lines_b_idx
    else:
        lines_map_onto_lines = False
    # geometric congruence of the seven line-triangles
    sides_ref = None
    angles_ref = None
    congruence_err = 0.0
    area_err = 0.0
    ref_area = fn.exact_literals(30)["cell_area"]
    ref_angles = (
        float(fn.exact_literals(30)["angle1"]),
        float(fn.exact_literals(30)["angle2"]),
        float(fn.exact_literals(30)["angle3"]),
    )
    angles_ladder_err = 0.0
    for line in fn.fano_lines():
        geom = fn.line_triangle_geometry(line, 1.0)
        if sides_ref is None:
            sides_ref = geom["sides"]
            angles_ref = geom["angles"]
        else:
            for a, b in zip(geom["sides"], sides_ref):
                congruence_err = max(congruence_err, abs(a - b))
            for a, b in zip(geom["angles"], angles_ref):
                congruence_err = max(congruence_err, abs(a - b))
        area_err = max(area_err, abs(geom["area"] - float(ref_area)))
        for a, b in zip(geom["angles"], sorted(ref_angles)):
            angles_ladder_err = max(angles_ladder_err, abs(a - b))
    exact = bool(
        order == 168
        and has_identity
        and closed
        and inverses
        and transitive
        and stab_point == 24
        and stab_line == 24
        and pair_ok
        and order_b == 168
        and isomorphism_found
        and conjugate
        and lines_map_onto_lines
    )
    congruent = (
        congruence_err <= TOLERANCES["chord_congruence"]
        and area_err <= TOLERANCES["chord_congruence"]
        and angles_ladder_err <= TOLERANCES["chord_congruence"]
    )
    return {
        "check": (
            "P4 PSL(2,7) algebra: 168 line-preserving permutations of Z_7 (closure, "
            "inverses, transitivity, stabilizers 24/24, the pair axiom), |GL(3,2)| = "
            "168, an explicit isomorphism Z_7 -> F_2^3 conjugating the two group "
            "copies in S_7, and the congruent line-triangles (angles pi/7 : 2pi/7 : "
            "4pi/7, area sqrt(7)/4)"
        ),
        "group_order_cyclic": order,
        "group_order_binary": order_b,
        "n_lines": len(lines),
        "n_flags": sum(len(line) for line in lines),
        "has_identity": has_identity,
        "closed_under_product": closed,
        "inverses_present": inverses,
        "point_transitive": transitive,
        "stabilizer_point": stab_point,
        "stabilizer_line": stab_line,
        "pair_axiom": pair_ok,
        "isomorphism_found": isomorphism_found,
        "isomorphism_maps_lines_to_lines": lines_map_onto_lines,
        "groups_conjugate_in_s7": conjugate,
        "congruence_max_abs_error": congruence_err,
        "area_max_abs_error": area_err,
        "angle_ladder_max_abs_error": angles_ladder_err,
        "params": {"tolerances": "integers exact; chords/angles/area <= 1e-12"},
        "passed": bool(exact and congruent),
    }


# ---------------------------------------------------------------------------
# P5 — the heptagon lattice: rigid rotation, invariants, Havelock N = 7
# ---------------------------------------------------------------------------


def check_p5_heptagon(rotations: float = 2.0, steps_per_rotation: int = 2400) -> Dict[str, Any]:
    """P5: the seven-vortex heptagon ring is a Havelock-stable relative
    equilibrium; measured rotation, invariant drift, spectrum floor."""
    gamma = np.ones(7)
    state0 = md.ring_state(1.0)
    omega_analytic = fn.ring_omega(1.0, 1.0)
    t_rot = TWO_PI / omega_analytic
    dt = t_rot / steps_per_rotation
    n_steps = int(round(rotations * steps_per_rotation))

    omega_measured = md.unwrap_rotation(state0, 1.0, n_steps * dt, dt, gamma)
    omega_err = abs(omega_measured - omega_analytic) / omega_analytic

    inv0 = md.invariants(state0, gamma)
    state1 = md.integrate(state0, gamma, dt, n_steps)
    drifts = md.relative_drifts(inv0, md.invariants(state1, gamma))

    growth = md.max_growth_rate(state0, gamma, omega_analytic)

    # the exact Hamiltonian of the ring against the sqrt(7) closed form
    h_exact = fn.ring_hamiltonian(1.0, 1.0)
    h_err = abs(inv0["H"] - h_exact) / max(abs(h_exact), 1e-30)

    tol = TOLERANCES
    passed = (
        omega_err <= tol["omega_rel"]
        and max(drifts.values()) <= tol["inv_drift"]
        and growth <= tol["stability_tol"]
        and h_err <= tol["hamiltonian_literal"]
    )
    return {
        "check": (
            "P5 heptagon lattice: the N=7 ring rotates rigidly at 3/2pi, the "
            "invariants hold, the co-rotating spectrum is Havelock-stable "
            "(the last stable level, cross-pinned to polyvortex W4)"
        ),
        "omega_analytic": omega_analytic,
        "omega_measured": omega_measured,
        "omega_relative_error": omega_err,
        "invariant_drifts": drifts,
        "hamiltonian_exact": h_exact,
        "hamiltonian_relative_error": h_err,
        "max_Re_lambda": growth,
        "havelock_stable": bool(growth <= tol["stability_tol"]),
        "params": {
            "gamma": 1.0,
            "big_r": 1.0,
            "rotations": rotations,
            "steps_per_rotation": steps_per_rotation,
        },
        "passed": bool(passed),
    }


# ---------------------------------------------------------------------------
# P6 — the seven cells: integrable Fano triads, congruent shape cycles
# ---------------------------------------------------------------------------


def _cell_rhs_batch(pos: np.ndarray) -> np.ndarray:
    """Batched Kirchhoff RHS for C concurrent 3-vortex cells.

    pos: shape (C, 3, 2); returns the velocities, shape (C, 3, 2).
    Equal unit circulations — the congruent-cell experiment of P6.
    """
    diff = pos[:, :, np.newaxis, :] - pos[:, np.newaxis, :, :]  # (C, 3, 3, 2)
    r2 = np.sum(diff * diff, axis=3)
    c = diff.shape[1]
    diag = np.arange(c)
    r2[:, diag, diag] = 1.0
    inv = 1.0 / r2
    inv[:, diag, diag] = 0.0
    vx = -np.sum(diff[..., 1] * inv, axis=2) / TWO_PI
    vy = +np.sum(diff[..., 0] * inv, axis=2) / TWO_PI
    return np.stack([vx, vy], axis=2)


def _shape_descriptor(pos: np.ndarray) -> np.ndarray:
    """The rotation- and scale-invariant shape descriptor of a cell.

    Sorted side ratios (a/c, b/c) of the triangle — invariant under
    rigid motions and permutation of the three vortices.
    """
    sides = []
    for a, b in ((0, 1), (1, 2), (2, 0)):
        sides.append(float(np.hypot(*(pos[a] - pos[b]))))
    sides.sort()
    return np.array([sides[0] / sides[2], sides[1] / sides[2]])


def _rk4_cell(pos: np.ndarray, dt: float) -> np.ndarray:
    """One RK4 step of a single 3-vortex cell (equal unit circulations)."""
    k1 = _cell_rhs_batch(pos[None, :, :])[0]
    k2 = _cell_rhs_batch((pos + 0.5 * dt * k1)[None, :, :])[0]
    k3 = _cell_rhs_batch((pos + 0.5 * dt * k2)[None, :, :])[0]
    k4 = _cell_rhs_batch((pos + dt * k3)[None, :, :])[0]
    return pos + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def check_p6_cells(cell_tmax: float = 240.0, cell_dt: float = 0.004, cell_sample_every: int = 4):
    """P6: the seven Fano line-cells are integrable Trivortex cells.

    All seven cells are integrated CONCURRENTLY (one batched RK4 over
    the (7, 3, 2) position array). Registers: the exact equality of the
    seven Hamiltonians (the sqrt(7) product identity), the invariant
    conservation along the shape cycle, the pairwise congruence of the
    seven shape periods (the dynamical shadow of PSL(2,7)), and the
    honest obstruction — a scalene triad is NOT a relative equilibrium.
    """
    xy = fn.heptagon_coordinates(1.0)
    cells0 = np.array([xy[list(line)] for line in fn.fano_lines()])  # (7, 3, 2)

    def batch_h(cells: np.ndarray) -> tuple:
        diff = cells[:, :, np.newaxis, :] - cells[:, np.newaxis, :, :]
        r2 = np.sum(diff * diff, axis=3)
        d = np.sqrt([r2[:, 0, 1], r2[:, 0, 2], r2[:, 1, 2]])  # (3, 7)
        h = -np.sum(np.log(d), axis=0) / TWO_PI
        imp = np.sum(cells * cells, axis=(1, 2))
        return h, imp

    h0, i0 = batch_h(cells0)
    d0 = _shape_descriptor_batch(cells0)  # (7, 2)
    n_steps = int(round(cell_tmax / cell_dt))
    cells = cells0.copy()
    desc_times = [0.0]
    descs = [d0.copy()]
    states = [cells0.copy()]
    drift_h = 0.0
    drift_i = 0.0
    for step in range(1, n_steps + 1):
        k1 = _cell_rhs_batch(cells)
        k2 = _cell_rhs_batch(cells + 0.5 * cell_dt * k1)
        k3 = _cell_rhs_batch(cells + 0.5 * cell_dt * k2)
        k4 = _cell_rhs_batch(cells + cell_dt * k3)
        cells = cells + (cell_dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        h, imp = batch_h(cells)
        drift_h = max(drift_h, float(np.max(np.abs(h - h0))))
        drift_i = max(drift_i, float(np.max(np.abs(imp - i0))))
        if step % cell_sample_every == 0:
            desc_times.append(step * cell_dt)
            descs.append(_shape_descriptor_batch(cells))
            states.append(cells.copy())
    descs_arr = np.array(descs)  # (S, 7, 2)
    dists = np.linalg.norm(descs_arr - d0[None, :, :], axis=2)  # (S, 7)
    per_cell: List[Dict[str, Any]] = []
    for c, line in enumerate(fn.fano_lines()):
        dc = dists[:, c]
        d_max = float(np.max(dc))
        depart = int(np.argmax(dc > 0.5 * d_max))
        candidates = np.where(dc[depart:] <= 1e-3)[0]
        entry: Dict[str, Any] = {
            "line": list(line),
            "H": float(h0[c]),
            "I": float(i0[c]),
            "shape_max_deviation": d_max,
            "drift_H": drift_h,
            "drift_I": drift_i,
        }
        if len(candidates) == 0:
            entry.update({"T_shape": None, "residual": None})
        else:
            idx = depart + int(candidates[0])
            j_lo = max(idx - 1, 0)
            t_lo = desc_times[j_lo]
            t_hi = desc_times[min(idx + 1, len(desc_times) - 1)]
            span = t_hi - t_lo
            fine_steps = 160
            dt_fine = span / fine_steps
            probe = states[j_lo][c].copy()
            best_t = t_lo
            best_d = float("inf")
            for f in range(fine_steps + 1):
                tf = t_lo + f * dt_fine
                if f > 0:
                    probe = _rk4_cell(probe, dt_fine)
                d = float(np.linalg.norm(_shape_descriptor(probe) - d0[c]))
                if d < best_d:
                    best_d = d
                    best_t = tf
            entry.update({"T_shape": best_t, "residual": best_d})
        per_cell.append(entry)
    h_spread = float(np.max(h0) - np.min(h0))
    h_exact_err = abs(float(h0[0]) - fn.cell_hamiltonian(1.0, 1.0)) / max(
        abs(fn.cell_hamiltonian(1.0, 1.0)), 1e-30
    )
    periods = [c["T_shape"] for c in per_cell]
    residuals = [c["residual"] for c in per_cell]
    if all(p is not None for p in periods):
        p_arr = np.array(periods, dtype=float)
        period_spread = float((p_arr.max() - p_arr.min()) / p_arr.mean())
        mean_period = float(p_arr.mean())
    else:
        period_spread = float("inf")
        mean_period = float("nan")
    max_dev = max(c["shape_max_deviation"] for c in per_cell)
    tol = TOLERANCES
    passed = (
        h_spread <= 1e-14
        and h_exact_err <= tol["hamiltonian_literal"]
        and drift_h <= tol["cell_inv_drift"]
        and drift_i <= tol["cell_inv_drift"]
        and period_spread <= tol["cell_period_rel"]
        and max(r for r in residuals if r is not None) <= tol["shape_return_residual"]
        and max_dev >= tol["not_re_min"]
    )
    return {
        "check": (
            "P6 seven cells: every Fano line is an integrable 3-vortex cell with "
            "the same Hamiltonian -(1/2pi)ln(sqrt(7)); the seven shape cycles are "
            "congruent (the dynamical PSL(2,7)); scalene triads are NOT relative "
            "equilibria"
        ),
        "per_cell": per_cell,
        "hamiltonian_spread": h_spread,
        "hamiltonian_exact_relative_error": h_exact_err,
        "T_shape_mean": mean_period,
        "T_shape_relative_spread": period_spread,
        "worst_return_residual": max(r for r in residuals if r is not None),
        "worst_invariant_drift": max(drift_h, drift_i),
        "max_shape_deviation": max_dev,
        "params": {
            "t_max": cell_tmax,
            "dt": cell_dt,
            "sample_every": cell_sample_every,
            "gamma": 1.0,
            "big_r": 1.0,
            "integrator": "batched RK4 over the (7,3,2) cell array",
        },
        "passed": bool(passed),
    }


def _shape_descriptor_batch(cells: np.ndarray) -> np.ndarray:
    """Rotation/scale-invariant sorted-side descriptors for a cell batch.

    cells: (C, 3, 2); returns (C, 2): the sorted side ratios (a/c, b/c).
    """
    diff = cells[:, :, np.newaxis, :] - cells[:, np.newaxis, :, :]
    r2 = np.sum(diff * diff, axis=3)
    sides = np.sqrt(np.stack([r2[:, 0, 1], r2[:, 1, 2], r2[:, 2, 0]], axis=1))  # (C, 3)
    sides.sort(axis=1)
    return np.stack([sides[:, 0] / sides[:, 2], sides[:, 1] / sides[:, 2]], axis=1)


# ---------------------------------------------------------------------------
# P7 — the gravity bridge: Schwarzschild ladder, Hill margins, diagnostics
# ---------------------------------------------------------------------------


def check_p7_bridge(dps: int = 30) -> Dict[str, Any]:
    """P7: gravity as exact geometry — the Schwarzschild ladder against
    its closed form, the adjacent Hill margins, and the recorded
    diagnostics of the mass-ladder deficit (Lemma E)."""
    from mpmath import mp, mpf

    mp.dps = dps
    c2 = mpf(cl.C_LIGHT) ** 2
    schwartz_rows = []
    worst_rel = 0.0
    bodies = [("Sun", cl.GM_SUN)] + [(p.name, p.gm) for p in cl.PLANETS]
    for name, gm in bodies:
        val = cl.schwarzschild_radius_m(gm)
        exact = 2 * mpf(gm) / c2
        rel = abs(mpf(val) - exact) / exact
        worst_rel = max(worst_rel, float(rel))
        schwartz_rows.append({"body": name, "r_s_m": val, "r_s_au": cl.au_of(val)})
    # adjacent Hill margins (ordered by a)
    ordered = sorted(cl.PLANETS, key=lambda p: p.a_au)
    hill_rows = []
    min_margin = float("inf")
    for p1, p2 in zip(ordered[:-1], ordered[1:]):
        h1 = cl.hill_radius_au(p1)
        h2 = cl.hill_radius_au(p2)
        gap = p2.a_au - p1.a_au
        margin = gap / (h1 + h2)
        min_margin = min(min_margin, margin)
        hill_rows.append(
            {
                "pair": f"{p1.name}-{p2.name}",
                "gap_au": gap,
                "r_H_sum_au": h1 + h2,
                "margin": margin,
            }
        )
    # diagnostics (recorded, no pass/fail role): Lemma E
    ladder = cl.gravity_ladder()
    line_sums = {}
    for tri in fn.cyclic_line_triples():
        names = [fn.STATION_NAMES[i] for i in tri]
        line_sums["+".join(names)] = round(sum(ladder[n] for n in names), 6)
    sums = list(line_sums.values())
    line_spread = max(sums) - min(sums)
    chord = fn.chord_classes(1.0)
    n_span = cl.PLANETS[7].period_days / cl.PLANETS[0].period_days
    # the vortex register of the mass ladder (dynamics, 1 rotation):
    # the equal-circulation heptagon stays rigid; the gravity-weighted
    # one deforms — the mass ladder breaks the mass-blind symmetry.
    gamma_eq = np.ones(7)
    gamma_w = cl.gravity_weights()
    gamma_w = 1.0 + 0.1 * (gamma_w - 1.0)  # the mild 10% ladder
    state0 = md.ring_state(1.0)
    omega7 = fn.ring_omega(1.0, 1.0)
    t_rot = TWO_PI / omega7
    dt_w = t_rot / 2400
    n_w = int(round(t_rot / dt_w))
    dev_eq = 0.0
    dev_w = 0.0
    cur_eq = state0.copy()
    cur_w = state0.copy()
    for _ in range(n_w):
        cur_eq = md.rk4_step(cur_eq, gamma_eq, dt_w)
        cur_w = md.rk4_step(cur_w, gamma_w, dt_w)
        r_eq = np.linalg.norm(cur_eq.reshape(7, 2), axis=1)
        r_w = np.linalg.norm(cur_w.reshape(7, 2), axis=1)
        dev_eq = max(dev_eq, float(np.max(np.abs(r_eq - 1.0))))
        dev_w = max(dev_w, float(np.max(np.abs(r_w - 1.0))))
    tol = TOLERANCES
    passed = worst_rel <= tol["schwartz_rel"] and min_margin >= tol["hill_margin_min"]
    return {
        "check": (
            "P7 gravity bridge: the Schwarzschild ladder r_s = 2GM/c^2 exact against "
            "the closed form; adjacent Hill spheres never overlap (min margin >= 3); "
            "the exact figure dimensions in AU and the mass-ladder deficit diagnostics"
        ),
        "schwarzschild_ladder": schwartz_rows,
        "schwarzschild_worst_relative_error": worst_rel,
        "hill_margins": hill_rows,
        "hill_min_margin": min_margin,
        "figure_dimensions_au": {
            "side_s1": chord[0],
            "short_diagonal_s2": chord[1],
            "long_diagonal_s3": chord[2],
            "cell_area_sqrt7_over_4": math.sqrt(7.0) / 4.0,
        },
        "diagnostics": {
            "mass_ladder_line_sums": line_sums,
            "mass_ladder_line_spread_dex": line_spread,
            "mean_motion_span_mercury_neptune": n_span,
            "chord_ladder_span_s3_over_s1": chord[2] / chord[0],
            "vortex_mass_ladder": {
                "equal_ring_radius_drift": dev_eq,
                "weighted_ring_radius_drift": dev_w,
                "weight_ladder": [round(float(g), 6) for g in gamma_w],
                "window_rotations": 1.0,
                "note": (
                    "recorded only: the equal-circulation heptagon stays rigid "
                    "(drift at machine zero) while the gravity-weighted heptagon "
                    "deforms within a single rotation — the mass ladder breaks "
                    "the mass-blind symmetry of the figure dynamically as well"
                ),
            },
            "note": (
                "recorded only: the real mass ladder breaks the mass-blind "
                "PSL(2,7) symmetry of the figure by ~5.3 dex of line sums"
            ),
        },
        "params": {"dps": dps, "tolerances": {"hill_margin_min": tol["hill_margin_min"]}},
        "passed": bool(passed),
    }


# ---------------------------------------------------------------------------
# The ladder driver
# ---------------------------------------------------------------------------

CHECK_FUNCS = {
    "P1": lambda cfg: check_p1_anchor(dps=cfg["dps"]),
    "P2": lambda cfg: check_p2_kepler(
        n_revolutions=cfg["p2_revolutions"],
        steps_per_revolution=cfg["p2_steps_per_revolution"],
    ),
    "P3": lambda cfg: check_p3_nbody(
        years=cfg["nbody_years"],
        dt=cfg["nbody_dt"],
        sample_every=cfg["nbody_sample_every"],
    ),
    "P4": lambda cfg: check_p4_algebra(),
    "P5": lambda cfg: check_p5_heptagon(
        rotations=cfg["vortex_rotations"],
        steps_per_rotation=cfg["ring_steps_per_rotation"],
    ),
    "P6": lambda cfg: check_p6_cells(
        cell_tmax=cfg["cell_tmax"],
        cell_dt=cfg["cell_dt"],
        cell_sample_every=cfg["cell_sample_every"],
    ),
    "P7": lambda cfg: check_p7_bridge(dps=cfg["dps"]),
}


def run_ladder(preset: str = "default") -> List[Dict[str, Any]]:
    """Run the whole P-ladder at the given preset; returns the checks."""
    cfg = PRESETS[preset]
    return [CHECK_FUNCS[stage](cfg) for stage in sorted(CHECK_FUNCS)]
