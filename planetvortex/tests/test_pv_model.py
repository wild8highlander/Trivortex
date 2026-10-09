#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
PLANETVORTEX — TESTS: THE KIRCHHOFF VORTEX LATTICE LAYER (Layer V)
============================================================================
The vortex-dynamics registers: the vectorized RHS against the explicit
pairwise sum, the invariants, the analytic Jacobian against finite
differences, the rigid rotation of the heptagon, the Havelock
stability of N = 7 and the exact Hamiltonian identities.

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import math

import numpy as np

from planetvortex import fano as fn
from planetvortex import model as md

TWO_PI = 2.0 * math.pi


def _rhs_explicit(state: np.ndarray, gamma: np.ndarray) -> np.ndarray:
    """The un-vectorized Kirchhoff RHS — the independent reference."""
    n = len(gamma)
    xy = state.reshape(n, 2)
    out = np.zeros((n, 2))
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx = xy[i, 0] - xy[j, 0]
            dy = xy[i, 1] - xy[j, 1]
            r2 = dx * dx + dy * dy
            out[i, 0] += -gamma[j] * dy / (TWO_PI * r2)
            out[i, 1] += +gamma[j] * dx / (TWO_PI * r2)
    return out.ravel()


def test_rhs_matches_explicit_pairwise() -> None:
    """The vectorized RHS equals the explicit pairwise sum on a random
    configuration (deterministic seed, unequal circulations)."""
    rng = np.random.default_rng(2026)
    state = rng.uniform(-1.5, 1.5, 14)
    gamma = np.array([1.0, -0.5, 2.0, 0.75, -1.25, 0.5, 1.5])
    fast = md.vortex_rhs(state, gamma)
    slow = _rhs_explicit(state, gamma)
    assert np.max(np.abs(fast - slow)) < 1e-12


def test_invariants_conserved_on_ring_flow() -> None:
    """H, P, Q, I drift below 1e-12 over half a ring rotation."""
    gamma = np.ones(7)
    state = md.ring_state(1.0)
    inv0 = md.invariants(state, gamma)
    t_rot = TWO_PI / fn.ring_omega(1.0, 1.0)
    state1 = md.integrate(state, gamma, t_rot / 2400.0, 1200)
    drifts = md.relative_drifts(inv0, md.invariants(state1, gamma))
    assert max(drifts.values()) < 1e-12
    # the impulses of the centred ring vanish identically
    assert abs(inv0["P"]) < 1e-12 and abs(inv0["Q"]) < 1e-12


def test_jacobian_matches_finite_differences() -> None:
    """The analytic Jacobian against a central-difference reference on
    a perturbed heptagon (relative error below 1e-7)."""
    rng = np.random.default_rng(7)
    state = md.ring_state(1.0) + 0.04 * rng.uniform(-1.0, 1.0, 14)
    gamma = np.ones(7)
    jac = md.jacobian(state, gamma)
    eps = 1e-6
    for col in range(14):
        e = np.zeros(14)
        e[col] = eps
        d_num = (md.vortex_rhs(state + e, gamma) - md.vortex_rhs(state - e, gamma)) / (2 * eps)
        assert np.max(np.abs(d_num - jac[:, col])) < 1e-7


def test_heptagon_rigid_rotation_measured() -> None:
    """The ring's measured rotation matches 3/(2pi) to 1e-11 (one
    rotation, 2400 steps)."""
    gamma = np.ones(7)
    state = md.ring_state(1.0)
    omega = fn.ring_omega(1.0, 1.0)
    t_rot = TWO_PI / omega
    measured = md.unwrap_rotation(state, 1.0, t_rot, t_rot / 2400.0, gamma)
    assert abs(measured - omega) / omega < 1e-11


def test_havelock_stability_n7() -> None:
    """N = 7 is the last Havelock-stable level: max Re(lambda) sits on
    the numerically-zero noise floor (below the 1e-7 classifier)."""
    gamma = np.ones(7)
    state = md.ring_state(1.0)
    growth = md.max_growth_rate(state, gamma, fn.ring_omega(1.0, 1.0))
    assert growth < 1e-7
    assert growth > -1e-6  # the defective-zero band, as in the sibling bench


def test_ring_state_exact_geometry() -> None:
    """The ring state is the heptagon: every radius exactly R, the
    first vertex at angle 0, station order counter-clockwise."""
    state = md.ring_state(1.0).reshape(7, 2)
    radii = np.linalg.norm(state, axis=1)
    assert np.max(np.abs(radii - 1.0)) < 1e-15
    assert state[0, 1] < 1e-15 and state[0, 0] > 0.99
    angles = np.mod(np.arctan2(state[:, 1], state[:, 0]), TWO_PI)
    assert np.allclose(angles, fn.heptagon_angles(), atol=1e-15)
