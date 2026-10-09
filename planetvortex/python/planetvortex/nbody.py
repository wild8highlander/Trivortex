#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
PLANETVORTEX — THE PLANETARY N-BODY LAYER (Layer N)
============================================================================
The Newtonian planetary simulation of the bench: the Sun and the eight
planets as point masses in the planar heliocentric idealization, the
RK4 integrator, the total energy and angular momentum, the osculating
Kepler elements and the perihelion initial condition.

Unit system
-----------
AU (exact 149 597 870 700 m), years, solar masses. G*M_sun = 4*pi^2
exactly; planet masses m_i = GM_i / GM_sun from the committed NASA
register (classical.py). The integration is fully Newtonian — all
pairwise terms, Sun included — so the planetary perturbations are
physical, not modelled.

Idealization (honesty notes)
----------------------------
Planar (all inclinations zero), all perihelia aligned at angle zero at
t = 0, barycentric momentum nulled by a compensating solar velocity.
The registers of stage P3 test the DYNAMICS against this committed
initial condition, not the ephemeris of the real calendar sky.

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

import numpy as np

from . import classical as cl

TWO_PI = 2.0 * math.pi
N_BODIES = 9  # the Sun + eight planets
SUN_INDEX = 0


def planet_masses() -> np.ndarray:
    """The mass vector [1 (Sun), m_Mercury, ..., m_Neptune] in solar units."""
    masses = np.ones(N_BODIES)
    for i, planet in enumerate(cl.PLANETS, start=1):
        masses[i] = cl.solar_mass_ratio(planet)
    return masses


def initial_state() -> np.ndarray:
    """The committed initial condition: perihelia aligned at angle 0.

    Planet i starts at perihelion r = a(1-e) on the +x axis with the
    perihelion speed v = sqrt(mu (1+e)/(a(1-e))) in +y; the Sun receives
    the compensating velocity so the total momentum is exactly zero.
    Returns the flat state [x, y, vx, vy] per body, shape (9, 4).
    """
    state = np.zeros((N_BODIES, 4))
    m_ratio = planet_masses()
    total_m = float(np.sum(m_ratio))
    # the Sun's compensating velocity keeps the total momentum at zero
    # while every planet keeps its EXACT heliocentric perihelion state
    v_sun = (
        -float(
            np.sum(
                m_ratio[1:]
                * [
                    math.sqrt(
                        cl.MU_SUN
                        * (1.0 + cl.solar_mass_ratio(p))
                        * (1.0 + p.e)
                        / (p.a_au * (1.0 - p.e))
                    )
                    for p in cl.PLANETS
                ]
            )
        )
        / total_m
    )
    for i, planet in enumerate(cl.PLANETS, start=1):
        m = cl.solar_mass_ratio(planet)
        mu = cl.MU_SUN * (1.0 + m)
        r_p = planet.a_au * (1.0 - planet.e)
        v_p = math.sqrt(mu * (1.0 + planet.e) / (planet.a_au * (1.0 - planet.e)))
        state[i, 0] = r_p
        state[i, 1] = 0.0
        state[i, 2] = 0.0  # the frame shift is along y only (the motion axis)
        state[i, 3] = v_p + v_sun
    state[SUN_INDEX, 2] = 0.0
    state[SUN_INDEX, 3] = v_sun
    return state


def rhs(state: np.ndarray, masses: np.ndarray) -> np.ndarray:
    """The Newtonian right-hand side (vectorized over all pairs).

    state: shape (9, 4) rows [x, y, vx, vy]; masses: shape (9,).
    The gravitational constant is absorbed into the units: body j pulls
    with strength 4*pi^2 * m_j (AU^3/yr^2 per solar mass).
    """
    xy = state[:, :2]
    diff = xy[np.newaxis, :, :] - xy[:, np.newaxis, :]  # diff[i, j] = r_j - r_i
    r2 = np.sum(diff * diff, axis=2)
    np.fill_diagonal(r2, 1.0)
    inv_r3 = r2**-1.5
    np.fill_diagonal(inv_r3, 0.0)
    gm = 4.0 * math.pi * math.pi * masses
    acc = np.sum(gm[np.newaxis, :, np.newaxis] * diff * inv_r3[:, :, np.newaxis], axis=1)
    out = np.empty_like(state)
    out[:, :2] = state[:, 2:]
    out[:, 2:] = acc
    return out


def rk4_step(state: np.ndarray, masses: np.ndarray, dt: float) -> np.ndarray:
    """One classical RK4 step of the N-body flow."""
    k1 = rhs(state, masses)
    k2 = rhs(state + 0.5 * dt * k1, masses)
    k3 = rhs(state + 0.5 * dt * k2, masses)
    k4 = rhs(state + dt * k3, masses)
    return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def integrate(
    state: np.ndarray, masses: np.ndarray, dt: float, n_steps: int, sample_every: int = 1
) -> Tuple[np.ndarray, np.ndarray]:
    """Integrate for n_steps; return (final_state, trajectory samples).

    The trajectory has shape (n_samples, 9, 4) with one row every
    `sample_every` steps (the first row is the initial state) — the
    basis for the period and drift registers of stage P3.
    """
    cur = np.asarray(state, dtype=float).copy()
    samples: List[np.ndarray] = [cur.copy()]
    for step in range(1, n_steps + 1):
        cur = rk4_step(cur, masses, dt)
        if step % sample_every == 0:
            samples.append(cur.copy())
    return cur, np.array(samples)


def total_energy(state: np.ndarray, masses: np.ndarray) -> float:
    """Total Newtonian energy (kinetic + pairwise potential), planar."""
    xy = state[:, :2]
    v2 = np.sum(state[:, 2:] ** 2, axis=1)
    kinetic = 0.5 * float(np.sum(masses * v2))
    potential = 0.0
    n = len(masses)
    gm = 4.0 * math.pi * math.pi * masses
    for i in range(n):
        for j in range(i + 1, n):
            r = float(np.hypot(*(xy[j] - xy[i])))
            potential -= gm[i] * masses[j] / r
    return kinetic + potential


def total_angular_momentum(state: np.ndarray, masses: np.ndarray) -> float:
    """The z-component of the total angular momentum (planar)."""
    xy = state[:, :2]
    return float(np.sum(masses * (xy[:, 0] * state[:, 3] - xy[:, 1] * state[:, 2])))


def osculating_elements(state: np.ndarray, planet_index: int) -> Tuple[float, float]:
    """Heliocentric osculating (a, e) of one planet from the full state.

    Uses the two-body constant mu_i = 4*pi^2*(1 + m_i) around the
    ACTUAL (perturbed) Sun position — the standard osculating reduction.
    """
    i = planet_index + 1  # bodies 1..8 are the planets in register order
    rx = state[i, 0] - state[SUN_INDEX, 0]
    ry = state[i, 1] - state[SUN_INDEX, 1]
    vx = state[i, 2] - state[SUN_INDEX, 2]
    vy = state[i, 3] - state[SUN_INDEX, 3]
    mu = 4.0 * math.pi * math.pi * (1.0 + planet_masses()[i])
    return cl.osculating_a_e(float(rx), float(ry), float(vx), float(vy), mu)


def perturbation_hierarchy(state: np.ndarray) -> Dict[str, float]:
    """Max over planets of |a_perturbations| / |a_solar| — the hierarchy.

    The classical smallness parameter of the planetary problem: how much
    of each planet's acceleration comes from everything except the Sun.
    """
    xy = state[:, :2]
    gm = 4.0 * math.pi * math.pi * planet_masses()
    worst = 0.0
    for i in range(1, N_BODIES):
        d = xy[i] - xy[SUN_INDEX]
        a_sun = gm[SUN_INDEX] / float(np.dot(d, d))
        acc_rest = 0.0
        for j in range(N_BODIES):
            if j == i or j == SUN_INDEX:
                continue  # the register excludes the Sun itself
            d = xy[j] - xy[i]
            acc_rest += gm[j] / float(np.dot(d, d))
        worst = max(worst, acc_rest / a_sun)
    return {"max_perturbation_ratio": worst}
