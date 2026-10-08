#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The Kirchhoff N-vortex dynamics layer: cross-validation against the
parent ladder, the analytic Jacobian, the integrals, the transport."""

from __future__ import annotations

import math

import numpy as np
import pytest

import polyvortex.classical as cl
import polyvortex.model as md

verify = pytest.importorskip("verify")  # the parent ladder (cross-checks only)


def test_rhs_matches_parent_ladder_n3() -> None:
    """The vectorized N-vortex RHS must reproduce the parent's loop
    implementation bit-for-bit up to floating-point reordering."""
    rng = np.random.default_rng(2026)
    state = rng.normal(size=6)
    gamma = np.array([1.0, 2.0, 3.0])
    ours = md.vortex_rhs(state, gamma)
    theirs = verify.vortex_rhs(state, gamma)
    assert float(np.max(np.abs(ours - theirs))) <= 1e-12


def test_rhs_symmetric_reduction_lagrange() -> None:
    """The equilateral triangle must rotate exactly per the parent's
    analytic omega = 3*Gamma/(2*pi*a^2)."""
    state = cl.ngon_initial(3, 1.0 / math.sqrt(3.0))
    gamma = np.full(3, 1.0)
    vel = md.vortex_rhs(state, gamma)
    xy = state.reshape(3, 2)
    omega_expected = 3.0 / (2.0 * math.pi)
    for k in range(3):
        r = float(np.linalg.norm(xy[k]))
        speed = float(np.linalg.norm(vel[2 * k : 2 * k + 2]))
        assert abs(speed - omega_expected * r) <= 1e-12
        # purely tangential: v . e_r = 0 (the Lemma C certificate at eps = 0)
        e_r = xy[k] / r
        assert abs(float(vel[2 * k : 2 * k + 2] @ e_r)) <= 1e-14


def test_jacobian_matches_finite_differences() -> None:
    rng = np.random.default_rng(7)
    n = 5
    state = rng.normal(size=2 * n)
    gamma = rng.uniform(0.5, 2.0, size=n)
    jac = md.jacobian(state, gamma)
    h = 1e-6
    for col in range(2 * n):
        sp = state.copy()
        sm = state.copy()
        sp[col] += h
        sm[col] -= h
        fd = (md.vortex_rhs(sp, gamma) - md.vortex_rhs(sm, gamma)) / (2.0 * h)
        assert float(np.max(np.abs(fd - jac[:, col]))) <= 1e-5


def test_invariants_match_parent_ladder() -> None:
    state = cl.ngon_initial(3, 1.0)
    gamma = np.full(3, 1.0)
    ours = md.invariants(state, gamma)
    theirs = verify.invariants(state, gamma)
    for key in ("H", "P", "Q", "I"):
        assert abs(ours[key] - theirs[key]) <= 1e-12


def test_invariants_conserved_n4() -> None:
    state = cl.ngon_initial(4, 1.0)
    gamma = np.full(4, 1.0)
    omega = cl.ngon_omega(1.0, 1.0, 4)
    dt = (2.0 * math.pi / omega) / 500
    inv0 = md.invariants(state, gamma)
    state = md.integrate(state, gamma, dt, 500)
    drifts = md.relative_drifts(inv0, md.invariants(state, gamma))
    assert max(drifts.values()) <= 1e-10


def test_corotating_spectrum_has_neutral_mode() -> None:
    """The circle of rotated polygons is a continuum of equilibria of the
    co-rotating system: J must own a (numerically) zero eigenvalue. The
    zero is algebraically double and geometrically simple (the rotational
    orbit), so rounding splits it into a +-real pair of size
    sqrt(eps_mach * ||J||) ~ 1e-9 — the classic defective-splitting
    scaling; the test band reflects that, not a plain 1e-15."""
    for n in (3, 4, 5):
        state = cl.ngon_initial(n, 1.0)
        gamma = np.full(n, 1.0)
        omega = cl.ngon_omega(1.0, 1.0, n)
        spec = md.corotating_spectrum(state, gamma, omega)
        assert float(np.min(np.abs(spec))) <= 1e-7
        # every non-neutral eigenvalue sits on the imaginary axis to rounding
        assert float(np.max(np.abs(np.real(spec)))) <= 1e-7
