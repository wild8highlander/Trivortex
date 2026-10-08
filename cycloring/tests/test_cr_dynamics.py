#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The root system, the Kirchhoff layer and the synchronous program."""

from __future__ import annotations

import math

import numpy as np
import pytest

from cycloring import dynamics as dyn
from cycloring import ring as rg


def test_root_system_identity() -> None:
    """prod(z - z_k) = z^N - sigma for the polygon (Theorem 1)."""
    for n in (5, 7, 9):
        zs = rg.polygon_positions(n, 1.0, 0.3)
        assert rg.root_system_residual(zs) <= 1e-10


def test_moments_roots_of_unity_filter() -> None:
    """S_m = 0 for m < N and S_N = N sigma."""
    n = 7
    zs = rg.polygon_positions(n, 1.0, 0.3)
    sums = rg.moment_sums(zs)
    for m in range(1, n):
        assert abs(sums[m - 1]) <= 1e-12
    sigma = (-1) ** (n - 1) * complex(np.prod(zs))
    assert abs(sums[n - 1] - n * sigma) <= 1e-12 * n


def test_impulse_vanishes() -> None:
    """L = Gamma sum z_k = 0 identically."""
    zs = rg.polygon_positions(9, 1.3, 0.7)
    assert abs(rg.impulse(zs)) <= 1e-12


def test_character_modes_polygon() -> None:
    """The polygon populates only the master character mode m = 1."""
    n = 7
    zs = rg.polygon_positions(n, 1.0, 0.3)
    modes = rg.character_amplitudes(zs)
    assert abs(modes[1]) == pytest.approx(1.0, rel=1e-10)
    for m in range(n):
        if m != 1:
            assert abs(modes[m]) <= 1e-10


def test_jacobian_finite_differences() -> None:
    """The analytic Jacobian against central differences."""
    rng = np.random.default_rng(11)
    n = 6
    state = rng.normal(size=2 * n)
    gamma_vec = np.ones(n)
    jac = dyn.jacobian(state, gamma_vec)
    eps = 1e-6
    worst = 0.0
    for i in range(2 * n):
        plus = state.copy()
        minus = state.copy()
        plus[i] += eps
        minus[i] -= eps
        col = (dyn.vortex_rhs(plus, gamma_vec) - dyn.vortex_rhs(minus, gamma_vec)) / (2 * eps)
        worst = max(worst, float(np.max(np.abs(col - jac[:, i]))))
    assert worst <= 1e-6


def test_rigid_rotation_rate() -> None:
    """The free polygon rotates at omega_L; the radius is held."""
    n, big_r = 7, 1.0
    omega_l = rg.frozen_rate(n, 1.0, big_r)
    t_period = 2.0 * math.pi / omega_l
    dt = t_period / 1200
    gamma_vec = np.ones(n)
    state = rg.polygon_positions_xy(n, big_r, 0.0)
    steps = 1200
    for _ in range(steps):
        state = dyn.rk4_step(state, gamma_vec, dt)
    xy = state.reshape(n, 2)
    radii = np.hypot(xy[:, 0], xy[:, 1])
    assert float(np.max(np.abs(radii - big_r))) <= 1e-11
    ang = math.atan2(xy[0, 1], xy[0, 0])
    measured = (ang + 2.0 * math.pi) / (steps * dt)
    assert measured == pytest.approx(omega_l, rel=1e-8)


def test_hamiltonian_closed_form() -> None:
    """H(R) = -(Gamma^2/2 pi)[(N(N-1)/2) ln R + (N/2) ln N]."""
    for n in (3, 7, 9):
        for big_r in (0.7, 1.0, 1.35):
            zs = rg.polygon_positions(n, big_r, 0.2)
            xy = np.stack([zs.real, zs.imag], axis=1).ravel()
            gamma_vec = np.ones(n)
            measured = dyn.invariants(xy, gamma_vec)["H"]
            closed = dyn.hamiltonian_closed_form(n, big_r, 1.0)
            assert measured == pytest.approx(closed, rel=1e-12, abs=1e-12)


def test_distance_product() -> None:
    """prod_{i<j} |z_i - z_j| = R^{N(N-1)/2} N^{N/2}."""
    n, big_r = 7, 1.1
    zs = rg.polygon_positions(n, big_r, 0.0)
    xy = np.stack([zs.real, zs.imag], axis=1).ravel()
    diff = xy.reshape(n, 2)[np.newaxis, :, :] - xy.reshape(n, 2)[:, np.newaxis, :]
    dist = np.sqrt(np.sum(diff * diff, axis=2))
    iu = np.triu_indices(n, k=1)
    measured = float(np.prod(dist[iu]))
    assert measured == pytest.approx(dyn.distance_product(n, big_r), rel=1e-10)


def test_mean_transport_identity() -> None:
    """M[(1+eps cos u)^{-2}] = (1-eps^2)^{-3/2} (float quadrature)."""
    for eps in (0.05, 0.2, 0.4, 0.6):
        assert rg.mean_transport_ratio(eps) == pytest.approx(
            1.0 / (1.0 - eps * eps) ** 1.5, rel=1e-10
        )


def test_synchronous_phase_advance() -> None:
    """The synchronous program advances the phase by exactly 2 pi per T_c."""
    n, big_r, eps = 7, 1.0, 0.2
    nu = rg.synchronous_frequency(big_r, eps, 1.0, n)
    t_c = rg.closure_time(eps, nu)
    phase = rg.transport_phase(t_c, big_r, eps, 1.0, n)
    assert phase == pytest.approx(2.0 * math.pi, rel=1e-10)


def test_closure_residual() -> None:
    """z_k(T_c) = z_k(0) — the rosettes close."""
    n, big_r, eps = 7, 1.0, 0.25
    nu = rg.synchronous_frequency(big_r, eps, 1.0, n)
    assert rg.closure_residual(n, big_r, eps, nu) <= 1e-9


def test_synchronous_frequency_matches_transducer() -> None:
    """The transducer frequency law is the synchronous law."""
    n = 7
    row = None
    from cycloring import chain as ch

    row = ch.defect_chain(n)
    nu_chain = row["nu_ratio"] * rg.frozen_rate(n, 1.0, 1.0)
    nu_sync = rg.synchronous_frequency(1.0, row["eps"], 1.0, n)
    assert nu_chain == pytest.approx(nu_sync, rel=1e-12)
