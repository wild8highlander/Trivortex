#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
PLANETVORTEX — TESTS: THE PLANETARY N-BODY LAYER (Layer N)
============================================================================
The Newtonian planetary registers: the two-body closure of a Kepler
orbit, the conservation of energy and angular momentum over the full
Sun + 8 planets integration, the osculating element stability and the
perturbation hierarchy.

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import math

import numpy as np

from planetvortex import classical as cl
from planetvortex import nbody as nb

TWO_PI = 2.0 * math.pi


def test_two_body_orbit_closure() -> None:
    """A single planet integrated for one revolution returns its
    committed (a, e) at the 1e-10 band (RK4, 2000 steps)."""
    p = cl.PLANETS[cl.EARTH_INDEX]
    mu = cl.mu_planet(p)
    state = np.array(
        [
            p.a_au * (1.0 - p.e),
            0.0,
            0.0,
            math.sqrt(mu * (1.0 + p.e) / (p.a_au * (1.0 - p.e))),
        ]
    )
    full = np.zeros((2, 4))  # Sun at rest at the origin (pure two-body check)
    full[1] = state
    t_period = TWO_PI * math.sqrt(p.a_au**3 / mu)
    dt = t_period / 4000.0
    cur = full.copy()
    for _ in range(4000):
        cur = nb.rk4_step(cur, np.array([1.0, cl.solar_mass_ratio(p)]), dt)
    a_end, e_end = cl.osculating_a_e(
        float(cur[1, 0] - cur[0, 0]),
        float(cur[1, 1] - cur[0, 1]),
        float(cur[1, 2] - cur[0, 2]),
        float(cur[1, 3] - cur[0, 3]),
        mu,
    )
    assert abs(a_end - p.a_au) / p.a_au < 1e-12
    assert abs(e_end - p.e) < 1e-12


def test_initial_state_momentum_balance() -> None:
    """The committed initial condition has exactly zero total momentum
    and places every planet at perihelion (r = a(1-e))."""
    state = nb.initial_state()
    masses = nb.planet_masses()
    px = float(np.sum(masses * state[:, 2]))
    py = float(np.sum(masses * state[:, 3]))
    assert abs(px) < 1e-13 and abs(py) < 1e-13
    for k, p in enumerate(cl.PLANETS):
        r = math.hypot(state[k + 1, 0], state[k + 1, 1])
        assert abs(r - p.a_au * (1.0 - p.e)) < 1e-12


def test_full_system_conservation() -> None:
    """Over the quick window (4 yr, dt = 1e-3): energy drift < 1e-9,
    angular-momentum drift < 1e-11 (the P3 conservation registers)."""
    masses = nb.planet_masses()
    state0 = nb.initial_state()
    e0 = nb.total_energy(state0, masses)
    l0 = nb.total_angular_momentum(state0, masses)
    state1, _ = nb.integrate(state0, masses, 1e-3, 4000, sample_every=2000)
    e1 = nb.total_energy(state1, masses)
    l1 = nb.total_angular_momentum(state1, masses)
    assert abs(e1 - e0) / abs(e0) < 1e-9
    assert abs(l1 - l0) / abs(l0) < 1e-11


def test_osculating_elements_secular_band() -> None:
    """After 4 years the osculating (a, e) of every planet stays within
    1% of the committed table — the secular band of stage P3."""
    masses = nb.planet_masses()
    state0 = nb.initial_state()
    state1, _ = nb.integrate(state0, masses, 1e-3, 4000, sample_every=4000)
    for k, p in enumerate(cl.PLANETS):
        a_end, e_end = nb.osculating_elements(state1, k)
        assert abs(a_end - p.a_au) / p.a_au < 1e-2, p.name
        assert abs(e_end - p.e) < 1e-2, p.name


def test_perturbation_hierarchy() -> None:
    """The Newtonian hierarchy: the largest non-solar acceleration on
    any planet is below 1% of its solar acceleration."""
    state = nb.initial_state()
    hierarchy = nb.perturbation_hierarchy(state)
    assert 0.0 < hierarchy["max_perturbation_ratio"] < 1e-2


def test_energy_register_matches_kepler_value() -> None:
    """The two-body energy of Earth's committed orbit equals
    -mu/(2a) at the 1e-12 band — the vis-viva anchor."""
    p = cl.PLANETS[cl.EARTH_INDEX]
    mu = cl.mu_planet(p)
    state = np.array(
        [
            p.a_au * (1.0 - p.e),
            0.0,
            0.0,
            math.sqrt(mu * (1.0 + p.e) / (p.a_au * (1.0 - p.e))),
        ]
    )
    v2 = state[2] ** 2 + state[3] ** 2
    energy = 0.5 * v2 - mu / math.hypot(state[0], state[1])
    assert abs(energy - (-mu / (2.0 * p.a_au))) / (mu / (2.0 * p.a_au)) < 1e-12
