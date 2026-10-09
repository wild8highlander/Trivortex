#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
PLANETVORTEX — THE KIRCHHOFF VORTEX LATTICE LAYER (Layer V)
============================================================================
The dynamical layer of the vortex figure: the classical Kirchhoff
equations for N point vortices, vectorized, with the RK4 integrator,
the vortex integrals H, P, Q, I and the analytic Jacobian used by the
stability register of stage P5.

The conventions are identical to the parent framework and to the
sibling polyvortex bench (the three programs share the same physics by
design, no code):

state = flat [x0, y0, x1, y1, ...] — the vortex positions;
    dx_i/dt = -1/(2*pi) * sum_{j!=i} G_j * (y_i - y_j) / r_ij^2
    dy_i/dt = +1/(2*pi) * sum_{j!=i} G_j * (x_i - x_j) / r_ij^2
Hamiltonian   H  = -sum_{i<j} G_i G_j ln(r_ij) / (2*pi)
impulses      P  = sum_i G_i x_i,   Q = sum_i G_i y_i
angular impulse I = sum_i G_i |r_i|^2

The figure places N = 7 vortices at the heptagon vertices (one per
station); each of the seven Fano lines is then a three-vortex
Trivortex cell — the scalene generalization of the parent's Lagrange
triangle, integrable and shape-periodic (stage P6).

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import math
from typing import Dict

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


def invariants(state: np.ndarray, gamma: np.ndarray) -> Dict[str, float]:
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


def relative_drifts(inv0: Dict[str, float], inv1: Dict[str, float]) -> Dict[str, float]:
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
    Validated against central finite differences in the test suite.
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

    In the frame rotating with angular velocity omega the rigid ring is
    a fixed point and the transport term contributes, per vortex,
    omega * [[0, 1], [-1, 0]]. A relative equilibrium is spectrally
    stable iff every eigenvalue of J is purely imaginary (Havelock).
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


# ---------------------------------------------------------------------------
# The figure's own constructors (heptagon ring, Fano cells)
# ---------------------------------------------------------------------------


def ring_state(big_r: float = 1.0) -> np.ndarray:
    """The flat state of the heptagon ring at R (station order)."""
    from . import fano as fn

    xy = fn.heptagon_coordinates(big_r)
    return xy.ravel().copy()


def cell_state(line_triple: Dict[str, object], big_r: float = 1.0) -> np.ndarray:
    """The flat 3-vortex state of one Fano line-cell (vertex indices)."""
    from . import fano as fn

    xy = fn.heptagon_coordinates(big_r)
    idx = line_triple["verts"]  # type: ignore[index]
    return xy[list(idx)].ravel().copy()


def unwrap_rotation(
    state: np.ndarray, big_r: float, total_time: float, dt: float, gamma: np.ndarray
) -> float:
    """Measured rigid-rotation rate from the integrated ring positions.

    Tracks the first vortex's polar angle over the run and unwraps the
    total accumulated angle — the same register discipline as the
    sibling polyvortex bench (measured_rotation_rate).
    """
    n_steps = int(round(total_time / dt))
    xy = np.asarray(state, dtype=float).reshape(-1, 2)
    ang0 = math.atan2(xy[0, 1], xy[0, 0])
    ang = ang0
    accumulated = 0.0
    cur = np.asarray(state, dtype=float).copy()
    prev = ang0
    for _ in range(n_steps):
        cur = rk4_step(cur, gamma, dt)
        xy = cur.reshape(-1, 2)
        ang = math.atan2(xy[0, 1], xy[0, 0])
        step = ang - prev
        if step > math.pi:
            step -= TWO_PI
        elif step < -math.pi:
            step += TWO_PI
        accumulated += step
        prev = ang
    return accumulated / (n_steps * dt)
