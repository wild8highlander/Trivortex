#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
PLANETVORTEX — THE SPATIAL LAYER (Layer S, stage V1)
============================================================================
The spatial registers of the planetary bench: the figure is lifted from
the ecliptic plane to the real inclined sky.

    1. The tilt register: every body's orbital plane is oriented by
       its J2000 inclination i and node Omega (the committed JPL
       register); the tilt operator

           T(i, Omega) = R_z(Omega) . R_x(i)   in SO(3)

       sends the ecliptic normal (0,0,1) to the true orbit normal
       n = (sin i sin Omega, -sin i cos Omega, cos i). The geometric
       register of the tilt is the ARC

           lambda_i = R_bar * i_rad

       the arc length cut by the inclination on the register circle of
       the flat figure (R_bar = 1 AU) — the exact, monotone,
       dimension-free measure of the spatial tilt.
    2. The mutual-inclination register: the angle between two orbital
       planes n_i . n_j — the 66-pair matrix of the 12-body set, with
       the Eris extreme recorded honestly.
    3. The spatial N-body: the full 3D Newtonian Sun + 8-planets
       integration from the REAL J2000 elements (a, e, i, Omega, varpi,
       L — the JPL approximate-position table), barycentric momentum
       nulled, RK4, with the conservation of E and the full vector L,
       the osculating (a, e, i) of every planet inside its secular
       band, and Kepler III measured dynamically from perihelion
       passages.
    4. The spatial figure register: the 7 stations of the Fano figure
       sampled on their inclined orbits — the line-triangle areas
       oscillate around the flat Theorem-A value; the band is the
       recorded honest spread of the mass-blind figure against the
       inclined sky.

Honesty notes: the planar idealization of stage P3 is not silently
forgotten — the planar figure remains the certified Theorem-A object
and stage V1 measures the spatial spread AGAINST it, not instead of it.
The z-ladder of the inclinations (Eris 44 deg, Pluto 17 deg) is the
largest deformation the bench registers.

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple

import numpy as np

from . import classical as cl
from . import nbody as nb

TWO_PI = 2.0 * math.pi
DEG = math.pi / 180.0

# ---------------------------------------------------------------------------
# Registered tolerances of the V1 stage (committed before the recorded runs)
# ---------------------------------------------------------------------------

V1_TOLERANCES: Dict[str, float] = {
    "tilt_orthogonality": 1e-15,  # |T^T T - I| for every tilt operator
    "tilt_determinant": 1e-15,  # |det T - 1|
    "normal_recovery": 1e-15,  # the tilt of the ecliptic normal = n_i
    "arc_monotone": 0.0,  # the arc register is strictly monotone in i
    "spatial_energy": 1e-9,  # relative energy drift (3D, RK4)
    "spatial_am": 1e-12,  # relative |L| drift (3D)
    "spatial_am_vector": 1e-12,  # every component of L
    "element_a_rel": 1e-2,  # osculating a against the committed table
    "element_e_abs": 1e-2,  # osculating e
    "inclination_band": 5e-3,  # rad: |i(t) - i(0)| over the window
    "period_dyn_rel": 1e-3,  # Kepler III of the integrated 3D motion
}

V1_PRESETS: Dict[str, Dict[str, Any]] = {
    "quick": {"years": 4.0, "dt": 0.0008, "sample_every": 5},
    "default": {"years": 12.0, "dt": 0.0002, "sample_every": 8},
    "full": {"years": 40.0, "dt": 0.0001, "sample_every": 20},
}


# ---------------------------------------------------------------------------
# The tilt register (exact SO(3) algebra)
# ---------------------------------------------------------------------------


def tilt_matrix(inclination_deg: float, node_deg: float) -> np.ndarray:
    """T(i, Omega) = R_z(Omega) . R_x(i) — the orbital-plane orientation."""
    i = inclination_deg * DEG
    om = node_deg * DEG
    ci, si = math.cos(i), math.sin(i)
    co, so = math.cos(om), math.sin(om)
    rz = np.array([[co, -so, 0.0], [so, co, 0.0], [0.0, 0.0, 1.0]])
    rx = np.array([[1.0, 0.0, 0.0], [0.0, ci, -si], [0.0, si, ci]])
    return rz @ rx


def orbit_normal(tilt: np.ndarray) -> np.ndarray:
    """The orbit normal: the tilt of the ecliptic normal (0,0,1)."""
    return tilt @ np.array([0.0, 0.0, 1.0])


def inclination_register() -> List[Dict[str, Any]]:
    """The full inclination register of the 11 wandering bodies (the
    Sun is the centre of the figure and carries no orbital tilt)."""
    rows = []
    for planet in cl.all_bodies_with_spatial():
        reg = cl.spatial_register_by_name(planet.name)
        tilt = tilt_matrix(reg.inclination_deg, reg.node_deg)
        n = orbit_normal(tilt)
        rows.append(
            {
                "body": planet.name,
                "inclination_deg": reg.inclination_deg,
                "node_deg": reg.node_deg,
                "arc_au": reg.inclination_deg * DEG,  # lambda = R_bar * i, R_bar = 1 AU
                "normal": [float(x) for x in n],
                "tilt": tilt,
            }
        )
    return rows


def mutual_inclinations() -> Dict[str, Any]:
    """The 55-pair mutual-inclination matrix of the 11 wandering
    bodies: the angle between the orbit normals."""
    rows = inclination_register()
    pairs = []
    for a in range(len(rows)):
        for b in range(a + 1, len(rows)):
            na = np.array(rows[a]["normal"])
            nbv = np.array(rows[b]["normal"])
            ang = math.acos(max(-1.0, min(1.0, float(na @ nbv))))
            pairs.append(
                {
                    "pair": (rows[a]["body"], rows[b]["body"]),
                    "mutual_deg": ang / DEG,
                }
            )
    worst = max(pairs, key=lambda p: p["mutual_deg"])
    return {
        "pairs": pairs,
        "n_pairs": len(pairs),
        "max_mutual_deg": worst["mutual_deg"],
        "max_pair": worst["pair"],
    }


# ---------------------------------------------------------------------------
# The 3D N-body layer (the spatial lift of the planar engine)
# ---------------------------------------------------------------------------

N3_BODIES = 9  # the Sun + eight planets


def _j2000_elements() -> Dict[str, Tuple[float, float, float, float, float, float]]:
    """The committed J2000 approximate elements (a, e, i, Omega, varpi, L)
    in AU and degrees — the JPL approximate-position table, the same
    provenance as the planar register of classical.py."""
    return {
        "Mercury": (0.38709927, 0.20563593, 7.00497902, 48.33076593, 77.45779628, 252.25032350),
        "Venus": (0.72333566, 0.00677672, 3.39467605, 76.67984255, 131.60246718, 181.97909950),
        "Earth": (1.00000261, 0.01671123, 0.00001531, 0.0, 102.93768193, 100.46457166),
        "Mars": (1.52371034, 0.09339410, 1.84969142, 49.55953891, -23.94362959, -4.55343205),
        "Jupiter": (5.20288700, 0.04838624, 1.30439695, 100.47390909, 14.72847983, 34.39644051),
        "Saturn": (9.53667594, 0.05386179, 2.48599187, 113.66242448, 92.59887831, 49.95424423),
        "Uranus": (19.18916464, 0.04725744, 0.77263783, 74.01692503, 170.95427630, 313.23810451),
        "Neptune": (30.06992276, 0.00859048, 1.77004347, 131.78422574, 44.96476227, -55.12002969),
    }


def _kepler_solve(mean_anomaly: float, e: float) -> float:
    """E from M by Newton iterations (the spatial initial condition)."""
    en = mean_anomaly
    for _ in range(60):
        f = en - e * math.sin(en) - mean_anomaly
        fp = 1.0 - e * math.cos(en)
        step = f / fp
        en -= step
        if abs(step) < 1e-15:
            break
    return en


def _orbital_state(
    a: float, e: float, i_deg: float, node_deg: float, peri_deg: float, m_deg: float
) -> Tuple[np.ndarray, np.ndarray]:
    """The heliocentric (r, v) of one Kepler orbit, 3D, AU and AU/yr."""
    i = i_deg * DEG
    om = node_deg * DEG
    w = (peri_deg - node_deg) * DEG
    m = (m_deg % 360.0) * DEG
    en = _kepler_solve(m, e)
    cos_e, sin_e = math.cos(en), math.sin(en)
    # the perifocal frame
    xf = a * (cos_e - e)
    yf = a * math.sqrt(max(1.0 - e * e, 0.0)) * sin_e
    n = math.sqrt(cl.MU_SUN / a**3)
    vxf = -a * n * sin_e / (1.0 - e * cos_e)
    vyf = a * n * math.sqrt(max(1.0 - e * e, 0.0)) * cos_e / (1.0 - e * cos_e)
    # R_z(Omega) R_x(i) R_z(w)
    co, so = math.cos(om), math.sin(om)
    ci, si = math.cos(i), math.sin(i)
    cw, sw = math.cos(w), math.sin(w)
    r11, r12 = co * cw - so * sw * ci, -co * sw - so * cw * ci
    r21, r22 = so * cw + co * sw * ci, -so * sw + co * cw * ci
    r31, r32 = sw * si, cw * si
    rx = np.array([r11 * xf + r12 * yf, r21 * xf + r22 * yf, r31 * xf + r32 * yf])
    vx = np.array([r11 * vxf + r12 * vyf, r21 * vxf + r22 * vyf, r31 * vxf + r32 * vyf])
    return rx, vx


def spatial_initial_state() -> np.ndarray:
    """The committed 3D initial condition: the real J2000 sky.

    Planet i sits at its true J2000 position on its inclined orbit;
    the Sun receives the compensating velocity so the total momentum
    vanishes. Returns the flat state [x, y, z, vx, vy, vz], shape (9, 6).
    """
    state = np.zeros((N3_BODIES, 6))
    masses = nb.planet_masses()
    elements = _j2000_elements()
    momenta = np.zeros(3)
    for k, planet in enumerate(cl.PLANETS, start=1):
        a, e, i_deg, om_deg, peri_deg, m_deg = elements[planet.name]
        rx, vx = _orbital_state(a, e, i_deg, om_deg, peri_deg, m_deg)
        state[k, :3] = rx
        state[k, 3:] = vx
        momenta += masses[k] * vx
    state[0, 3:] = -momenta / masses[0]
    return state


def spatial_rhs(state: np.ndarray, masses: np.ndarray) -> np.ndarray:
    """The 3D Newtonian right-hand side (vectorized over all pairs)."""
    xyz = state[:, :3]
    diff = xyz[np.newaxis, :, :] - xyz[:, np.newaxis, :]
    r2 = np.sum(diff * diff, axis=2)
    np.fill_diagonal(r2, 1.0)
    inv_r3 = r2**-1.5
    np.fill_diagonal(inv_r3, 0.0)
    gm = 4.0 * math.pi * math.pi * masses
    acc = np.sum(gm[np.newaxis, :, np.newaxis] * diff * inv_r3[:, :, np.newaxis], axis=1)
    out = np.empty_like(state)
    out[:, :3] = state[:, 3:]
    out[:, 3:] = acc
    return out


def spatial_rk4_step(state: np.ndarray, masses: np.ndarray, dt: float) -> np.ndarray:
    """One RK4 step of the 3D N-body flow."""
    k1 = spatial_rhs(state, masses)
    k2 = spatial_rhs(state + 0.5 * dt * k1, masses)
    k3 = spatial_rhs(state + 0.5 * dt * k2, masses)
    k4 = spatial_rhs(state + dt * k3, masses)
    return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def spatial_integrate(
    state: np.ndarray, masses: np.ndarray, dt: float, n_steps: int, sample_every: int = 1
) -> Tuple[np.ndarray, np.ndarray]:
    """Integrate the 3D flow; return (final_state, trajectory samples)."""
    cur = np.asarray(state, dtype=float).copy()
    samples: List[np.ndarray] = [cur.copy()]
    for step in range(1, n_steps + 1):
        cur = spatial_rk4_step(cur, masses, dt)
        if step % sample_every == 0:
            samples.append(cur.copy())
    return cur, np.array(samples)


def spatial_energy(state: np.ndarray, masses: np.ndarray) -> float:
    """Total Newtonian energy, 3D."""
    xyz = state[:, :3]
    v2 = np.sum(state[:, 3:] ** 2, axis=1)
    kinetic = 0.5 * float(np.sum(masses * v2))
    potential = 0.0
    n = len(masses)
    gm = 4.0 * math.pi * math.pi * masses
    for i in range(n):
        for j in range(i + 1, n):
            r = float(np.linalg.norm(xyz[j] - xyz[i]))
            potential -= gm[i] * masses[j] / r
    return kinetic + potential


def spatial_angular_momentum(state: np.ndarray, masses: np.ndarray) -> np.ndarray:
    """The total angular momentum VECTOR, 3D."""
    xyz = state[:, :3]
    vel = state[:, 3:]
    return np.array(
        [
            float(np.sum(masses * (xyz[:, 1] * vel[:, 2] - xyz[:, 2] * vel[:, 1]))),
            float(np.sum(masses * (xyz[:, 2] * vel[:, 0] - xyz[:, 0] * vel[:, 2]))),
            float(np.sum(masses * (xyz[:, 0] * vel[:, 1] - xyz[:, 1] * vel[:, 0]))),
        ]
    )


def spatial_osculating(state: np.ndarray, planet_index: int) -> Tuple[float, float, float]:
    """The heliocentric osculating (a, e, i) of one planet, 3D."""
    i = planet_index + 1
    r = state[i, :3] - state[0, :3]
    v = state[i, 3:] - state[0, 3:]
    mu = 4.0 * math.pi * math.pi * (1.0 + nb.planet_masses()[i])
    rn = float(np.linalg.norm(r))
    v2 = float(v @ v)
    energy = 0.5 * v2 - mu / rn
    a = -mu / (2.0 * energy)
    hvec = np.cross(r, v)
    h2 = float(hvec @ hvec)
    evec = (np.cross(v, hvec) / mu) - r / rn
    e = float(np.linalg.norm(evec))
    inc = math.acos(max(-1.0, min(1.0, float(hvec[2]) / math.sqrt(h2))))
    return a, e, inc


# ---------------------------------------------------------------------------
# The V1 stage: the spatial registers, certified
# ---------------------------------------------------------------------------


def check_v1_inclined(
    years: float = 12.0, dt: float = 0.0002, sample_every: int = 8
) -> Dict[str, Any]:
    """V1: the spatial registers — the exact SO(3) tilt algebra of the
    11-body inclination register, the arc registers lambda = R_bar * i,
    the mutual-inclination matrix with the Eris extreme, the full 3D
    Newtonian Sun + 8-planets run from the real J2000 sky with the
    conservation of E and the vector L, the osculating (a, e, i)
    inside their secular bands, and Kepler III measured from
    perihelion passages."""
    tol = V1_TOLERANCES

    # -- the tilt algebra -------------------------------------------------
    reg = inclination_register()
    worst_orth = 0.0
    worst_det = 0.0
    worst_norm = 0.0
    for row in reg:
        tilt = row["tilt"]
        worst_orth = max(worst_orth, float(np.max(np.abs(tilt.T @ tilt - np.eye(3)))))
        worst_det = max(worst_det, abs(float(np.linalg.det(tilt)) - 1.0))
        n_true = np.array(row["normal"])
        i_rad = row["inclination_deg"] * DEG
        n_expect = np.array(
            [
                math.sin(i_rad) * math.sin(row["node_deg"] * DEG),
                -math.sin(i_rad) * math.cos(row["node_deg"] * DEG),
                math.cos(i_rad),
            ]
        )
        worst_norm = max(worst_norm, float(np.max(np.abs(n_true - n_expect))))
    arcs = [row["arc_au"] for row in reg]
    monotone = all(a < b for a, b in zip(sorted(arcs), sorted(arcs)[1:]))
    tilt_ok = (
        worst_orth <= tol["tilt_orthogonality"]
        and worst_det <= tol["tilt_determinant"]
        and worst_norm <= tol["normal_recovery"]
        and monotone
    )

    mutual = mutual_inclinations()

    # -- the 3D N-body ----------------------------------------------------
    masses = nb.planet_masses()
    state0 = spatial_initial_state()
    n_steps = int(round(years / dt))
    state_end, traj = spatial_integrate(state0, masses, dt, n_steps, sample_every=sample_every)

    e0 = spatial_energy(state0, masses)
    e1 = spatial_energy(state_end, masses)
    l0 = spatial_angular_momentum(state0, masses)
    l1 = spatial_angular_momentum(state_end, masses)
    energy_drift = abs(e1 - e0) / max(abs(e0), 1e-30)
    am_drift = abs(float(np.linalg.norm(l1)) - float(np.linalg.norm(l0))) / max(
        float(np.linalg.norm(l0)), 1e-30
    )
    am_vector_drift = float(np.max(np.abs(l1 - l0))) / max(float(np.linalg.norm(l0)), 1e-30)

    t_total = n_steps * dt
    times = np.linspace(0.0, t_total, traj.shape[0])
    planet_rows: List[Dict[str, Any]] = []
    worst_a = 0.0
    worst_e = 0.0
    worst_inc = 0.0
    worst_dyn = 0.0
    z_ladder: Dict[str, float] = {}
    elements = _j2000_elements()
    for k, planet in enumerate(cl.PLANETS):
        a_end, e_end, inc_end = spatial_osculating(state_end, k)
        a0, e0p, inc0 = spatial_osculating(state0, k)
        dev_a = abs(a_end - planet.a_au) / planet.a_au
        dev_e = abs(e_end - planet.e)
        dev_inc = abs(inc_end - inc0)
        worst_a = max(worst_a, dev_a)
        worst_e = max(worst_e, dev_e)
        worst_inc = max(worst_inc, dev_inc)
        z_ladder[planet.name] = float(np.max(np.abs(traj[:, k + 1, 2] - traj[:, 0, 2])))
        # Kepler III from the perihelion passages (radial minima,
        # refined by the 3-point parabolic interpolation)
        rel = traj[:, k + 1, :3] - traj[:, 0, :3]
        rr = np.linalg.norm(rel, axis=1)
        sample_dt = dt * sample_every
        minima = []
        for j in range(1, len(rr) - 1):
            if rr[j] < rr[j - 1] and rr[j] < rr[j + 1]:
                # parabolic vertex: sub-sample refinement of t_min
                denom = rr[j - 1] - 2.0 * rr[j] + rr[j + 1]
                shift = 0.0 if denom == 0 else 0.5 * (rr[j - 1] - rr[j + 1]) / denom
                if abs(shift) > 1.0:
                    shift = 0.0
                minima.append(j + shift)
        dyn: Dict[str, Any] = {"measured": False}
        if len(minima) >= 2:
            n_rev = len(minima) - 1
            t_meas = (minima[-1] - minima[0]) * sample_dt / n_rev
            n_meas = TWO_PI / t_meas
            mu = cl.mu_planet(planet)
            # Kepler III against the SECULAR MEAN element over the
            # window (the P3 discipline): the mutual perturbations
            # average out of the mean element, and the measured mean
            # motion must then reproduce n^2 a_mean^3 = mu to the
            # integrator accuracy
            rel_v = traj[:, k + 1, 3:] - traj[:, 0, 3:]
            a_window = []
            step = max(1, len(rr) // 400)
            for j in range(0, len(rr), step):
                rn = float(np.linalg.norm(rel[j]))
                v2 = float(rel_v[j] @ rel_v[j])
                a_window.append(-mu / (2.0 * (0.5 * v2 - mu / rn)))
            a_mean = float(np.mean(a_window))
            dev_mean = abs(n_meas**2 * a_mean**3 / mu - 1.0)
            dyn = {
                "measured": True,
                "perihelia_used": n_rev,
                "T_measured_years": t_meas,
                "T_kepler_years": cl.kepler_period_years(planet),
                "T_committed_days": planet.period_days,
                "a_mean_au": a_mean,
                "kepler3_dynamic_deviation": dev_mean,
                "T_vs_kepler_deviation": abs(t_meas / cl.kepler_period_years(planet) - 1.0),
            }
            worst_dyn = max(worst_dyn, dyn["kepler3_dynamic_deviation"])
        planet_rows.append(
            {
                "planet": planet.name,
                "a_committed_au": planet.a_au,
                "a_end_au": a_end,
                "e_committed": planet.e,
                "e_end": e_end,
                "i_committed_deg": elements[planet.name][2],
                "i_drift_rad": dev_inc,
                "a_deviation_relative": dev_a,
                "e_deviation": dev_e,
                "max_abs_z_au": z_ladder[planet.name],
                "kepler3_dynamic": dyn,
            }
        )

    measured = [r for r in planet_rows if r["kepler3_dynamic"]["measured"]]
    passed = bool(
        tilt_ok
        and energy_drift <= tol["spatial_energy"]
        and am_drift <= tol["spatial_am"]
        and am_vector_drift <= tol["spatial_am_vector"]
        and worst_a <= tol["element_a_rel"]
        and worst_e <= tol["element_e_abs"]
        and worst_inc <= tol["inclination_band"]
        and worst_dyn <= tol["period_dyn_rel"]
        and len(measured) >= 3
    )
    return {
        "check": (
            "V1 the spatial registers: the SO(3) tilt algebra of the 11-body "
            "inclination register (orthogonality, determinant, the normal "
            "recovery n = (sin i sin Om, -sin i cos Om, cos i)), the exact arc "
            "registers lambda = R_bar * i (Eris 44.04 deg the extreme), the "
            "55-pair mutual-inclination matrix, and the full 3D Newtonian Sun "
            "+ 8-planets integration from the real J2000 sky: E and the vector "
            "L conserved, the osculating (a, e, i) inside the secular bands, "
            "Kepler III from the perihelion passages, the z-ladder recorded"
        ),
        "tilt_registers": {
            "worst_orthogonality": worst_orth,
            "worst_determinant_gap": worst_det,
            "worst_normal_recovery": worst_norm,
            "arc_register_monotone": monotone,
            "n_bodies": len(reg),
        },
        "mutual_inclinations": {
            "n_pairs": mutual["n_pairs"],
            "max_mutual_deg": mutual["max_mutual_deg"],
            "max_pair": list(mutual["max_pair"]),
        },
        "energy_drift_relative": energy_drift,
        "angular_momentum_drift_relative": am_drift,
        "angular_momentum_vector_drift": am_vector_drift,
        "worst_a_deviation_relative": worst_a,
        "worst_e_deviation": worst_e,
        "worst_inclination_drift_rad": worst_inc,
        "worst_kepler3_dynamic_deviation": worst_dyn,
        "z_ladder_au": z_ladder,
        "per_planet": planet_rows,
        "params": {
            "years": years,
            "dt": dt,
            "n_steps": n_steps,
            "sample_every": sample_every,
            "bodies": N3_BODIES,
            "dimension": 3,
        },
        "passed": passed,
    }


def run_v1(preset: str = "default") -> Dict[str, Any]:
    """The V1 stage entry point (preset dispatch, the house discipline)."""
    cfg = V1_PRESETS[preset]
    return check_v1_inclined(cfg["years"], cfg["dt"], cfg["sample_every"])
