#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
POLYVORTEX — KIRCHHOFF N-VORTEX DYNAMICS LAYER (Layer K)
============================================================================
The dynamical layer of the polyvortex mini-repository: the classical
Kirchhoff equations for N point vortices, vectorized, with the RK4
integrator, the vortex integrals H, P, Q, I and the analytic Jacobian
used by the stability stage W4.

Everything here is N-generic: the N = 3 reduction reproduces the numbers
of the parent Trivortex ladder (`verification/trivortex/python/verify.py`)
and is cross-checked by the test suite, but nothing in this package
imports the parent ladder at runtime — the mini-repository is
self-contained by design.

Conventions (identical to the parent ladder)
--------------------------------------------
state = flat [x0, y0, x1, y1, ...] — the vortex positions;
    dx_i/dt = -1/(2*pi) * sum_{j!=i} G_j * (y_i - y_j) / r_ij^2
    dy_i/dt = +1/(2*pi) * sum_{j!=i} G_j * (x_i - x_j) / r_ij^2
Hamiltonian   H  = -sum_{i<j} G_i G_j ln(r_ij) / (2*pi)
impulses      P  = sum_i G_i x_i,   Q = sum_i G_i y_i
angular impulse I = sum_i G_i |r_i|^2

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import math

import numpy as np

TWO_PI = 2.0 * math.pi


# ---------------------------------------------------------------------------
# The Kirchhoff right-hand side (vectorized, N vortices)
# ---------------------------------------------------------------------------


def vortex_rhs(state: np.ndarray, gamma: np.ndarray) -> np.ndarray:
    """Kirchhoff equations for N point vortices (vectorized over pairs).

    state = flat [x0, y0, ..., y_{N-1}]; gamma = circulations, shape (N,).
    The diagonal (self-interaction) is excluded by masking.
    """
    n = len(gamma)
    xy = np.asarray(state, dtype=float).reshape(n, 2)
    diff = xy[:, np.newaxis, :] - xy[np.newaxis, :, :]  # diff[i, j] = xy[i] - xy[j]
    r2 = np.sum(diff * diff, axis=2)
    np.fill_diagonal(r2, 1.0)
    inv = 1.0 / r2
    np.fill_diagonal(inv, 0.0)
    gx = gamma[np.newaxis, :]
    vx = -np.sum(gx * diff[:, :, 1] * inv, axis=1) / TWO_PI
    vy = +np.sum(gx * diff[:, :, 0] * inv, axis=1) / TWO_PI
    return np.stack([vx, vy], axis=1).ravel()


def rk4_step(state: np.ndarray, gamma: np.ndarray, dt: float) -> np.ndarray:
    """One classical RK4 step of the vortex dynamics."""
    k1 = vortex_rhs(state, gamma)
    k2 = vortex_rhs(state + 0.5 * dt * k1, gamma)
    k3 = vortex_rhs(state + 0.5 * dt * k2, gamma)
    k4 = vortex_rhs(state + dt * k3, gamma)
    return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def integrate(state: np.ndarray, gamma: np.ndarray, dt: float, n_steps: int) -> np.ndarray:
    """Integrate the Kirchhoff flow for n_steps RK4 steps."""
    out = np.asarray(state, dtype=float).copy()
    for _ in range(int(n_steps)):
        out = rk4_step(out, gamma, dt)
    return out


# ---------------------------------------------------------------------------
# The vortex integrals H, P, Q, I (N-generic)
# ---------------------------------------------------------------------------


def invariants(state: np.ndarray, gamma: np.ndarray) -> dict:
    """H, P, Q, I — the classical vortex integrals for any N."""
    n = len(gamma)
    xy = np.asarray(state, dtype=float).reshape(n, 2)
    diff = xy[np.newaxis, :, :] - xy[:, np.newaxis, :]
    r2 = np.sum(diff * diff, axis=2)
    iu = np.triu_indices(n, k=1)
    dist = np.sqrt(r2[iu])
    h = -float(np.sum(gamma[iu[0]] * gamma[iu[1]] * np.log(dist))) / TWO_PI
    p = float(np.sum(gamma * xy[:, 0]))
    q = float(np.sum(gamma * xy[:, 1]))
    imp = float(np.sum(gamma * np.sum(xy * xy, axis=1)))
    return {"H": h, "P": p, "Q": q, "I": imp}


def relative_drifts(inv0: dict, inv1: dict) -> dict:
    """Relative drifts |I1 - I0| / max(|I0|, 1) — the registered discipline."""
    return {key: abs(inv1[key] - inv0[key]) / max(abs(inv0[key]), 1.0) for key in inv0}


# ---------------------------------------------------------------------------
# The analytic Jacobian and the co-rotating stability spectrum
# ---------------------------------------------------------------------------


def jacobian(state: np.ndarray, gamma: np.ndarray) -> np.ndarray:
    """Analytic Jacobian A = d(vortex_rhs)/d(state) for N vortices.

    For the pair (i, j), i != j, with dx = x_i - x_j, dy = y_i - y_j,
    r2 = dx^2 + dy^2, r4 = r2^2:
        d(vx_i)/d(x_i) = + G_j dx dy / (pi r4)
        d(vx_i)/d(y_i) = - G_j (r2 - 2 dy^2) / (2 pi r4)
        d(vx_i)/d(x_j) = - G_j dx dy / (pi r4)
        d(vx_i)/d(y_j) = + G_j (r2 - 2 dy^2) / (2 pi r4)
        d(vy_i)/d(x_i) = + G_j (r2 - 2 dx^2) / (2 pi r4)
        d(vy_i)/d(y_i) = - G_j dx dy / (pi r4)
        d(vy_i)/d(x_j) = - G_j (r2 - 2 dx^2) / (2 pi r4)
        d(vy_i)/d(y_j) = + G_j dx dy / (pi r4)
    The matrix is validated against central finite differences in the
    test suite (test_model.py).
    """
    n = len(gamma)
    xy = np.asarray(state, dtype=float).reshape(n, 2)
    jac = np.zeros((2 * n, 2 * n))
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx = xy[i, 0] - xy[j, 0]
            dy = xy[i, 1] - xy[j, 1]
            r2 = dx * dx + dy * dy
            r4 = r2 * r2
            g = gamma[j]
            a_xx = +g * dx * dy / (math.pi * r4)
            a_xy = -g * (r2 - 2.0 * dy * dy) / (TWO_PI * r4)
            a_yx = +g * (r2 - 2.0 * dx * dx) / (TWO_PI * r4)
            a_yy = -g * dx * dy / (math.pi * r4)
            # diagonal (i, i) block contribution and the column-j entries
            jac[2 * i, 2 * i] += a_xx
            jac[2 * i, 2 * i + 1] += a_xy
            jac[2 * i + 1, 2 * i] += a_yx
            jac[2 * i + 1, 2 * i + 1] += a_yy
            jac[2 * i, 2 * j] += -a_xx
            jac[2 * i, 2 * j + 1] += -a_xy
            jac[2 * i + 1, 2 * j] += -a_yx
            jac[2 * i + 1, 2 * j + 1] += -a_yy
    return jac


def corotating_spectrum(state: np.ndarray, gamma: np.ndarray, omega: float) -> np.ndarray:
    """Eigenvalues of the co-rotating linearization J = A + omega * S.

    In the frame rotating with angular velocity omega the rigid N-gon is
    a fixed point and the transport term contributes, per vortex,
    omega * [[0, 1], [-1, 0]] (the -i*omega*w term of the complex form).
    A relative equilibrium is spectrally stable iff every eigenvalue of
    J is purely imaginary (the Havelock criterion).
    """
    n = len(gamma)
    jac = jacobian(state, gamma)
    transport = np.zeros((2 * n, 2 * n))
    for i in range(n):
        transport[2 * i, 2 * i + 1] = omega
        transport[2 * i + 1, 2 * i] = -omega
    return np.linalg.eigvals(jac + transport)


def max_growth_rate(state: np.ndarray, gamma: np.ndarray, omega: float) -> float:
    """max Re(lambda) over the co-rotating spectrum (stability gauge)."""
    return float(np.max(np.real(corotating_spectrum(state, gamma, omega))))
