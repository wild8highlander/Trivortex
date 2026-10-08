#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
CYCLORING — THE KIRCHHOFF POINT-VORTEX LAYER
============================================================================
The classical dynamics of N point vortices, vectorized, with the RK4
integrator, the vortex integrals H, P, Q, I and the analytic Jacobian.

Conventions
-----------
state = flat [x0, y0, x1, y1, ...] — the vortex positions;
    dx_i/dt = -1/(2 pi) * sum_{j != i} G_j (y_i - y_j) / r_ij^2
    dy_i/dt = +1/(2 pi) * sum_{j != i} G_j (x_i - x_j) / r_ij^2
Hamiltonian   H  = -sum_{i<j} G_i G_j ln(r_ij) / (2 pi)
impulses      P  = sum_i G_i x_i,   Q = sum_i G_i y_i
angular impulse I = sum_i G_i |r_i|^2

The closed-form register of Theorem 5 is also provided here:
for the regular N-gon the pair-distance product is

    prod_{i<j} |z_i - z_j| = R^{N(N-1)/2} N^{N/2},

so the Hamiltonian collapses to

    H(R) = -(Gamma^2 / 4 pi) [ (N(N-1)/2) ln R + (N/2) ln N ].

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
# The right-hand side and the integrator
# ---------------------------------------------------------------------------


def vortex_rhs(state: np.ndarray, gamma_vec: np.ndarray) -> np.ndarray:
    """Kirchhoff equations for N point vortices (vectorized over pairs)."""
    n = len(gamma_vec)
    xy = np.asarray(state, dtype=float).reshape(n, 2)
    diff = xy[:, np.newaxis, :] - xy[np.newaxis, :, :]  # diff[i, j] = xy[i] - xy[j]
    r2 = np.sum(diff * diff, axis=2)
    np.fill_diagonal(r2, 1.0)
    inv = 1.0 / r2
    np.fill_diagonal(inv, 0.0)
    gx = gamma_vec[np.newaxis, :]
    vx = -np.sum(gx * diff[:, :, 1] * inv, axis=1) / TWO_PI
    vy = +np.sum(gx * diff[:, :, 0] * inv, axis=1) / TWO_PI
    return np.stack([vx, vy], axis=1).ravel()


def rk4_step(state: np.ndarray, gamma_vec: np.ndarray, dt: float) -> np.ndarray:
    """One classical RK4 step of the vortex dynamics."""
    k1 = vortex_rhs(state, gamma_vec)
    k2 = vortex_rhs(state + 0.5 * dt * k1, gamma_vec)
    k3 = vortex_rhs(state + 0.5 * dt * k2, gamma_vec)
    k4 = vortex_rhs(state + dt * k3, gamma_vec)
    return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def integrate(state: np.ndarray, gamma_vec: np.ndarray, dt: float, n_steps: int) -> np.ndarray:
    """Integrate the Kirchhoff flow for n_steps RK4 steps."""
    out = np.asarray(state, dtype=float).copy()
    for _ in range(int(n_steps)):
        out = rk4_step(out, gamma_vec, dt)
    return out


# ---------------------------------------------------------------------------
# The vortex integrals
# ---------------------------------------------------------------------------


def invariants(state: np.ndarray, gamma_vec: np.ndarray) -> Dict[str, float]:
    """H, P, Q, I — the classical vortex integrals for any N."""
    n = len(gamma_vec)
    xy = np.asarray(state, dtype=float).reshape(n, 2)
    diff = xy[np.newaxis, :, :] - xy[:, np.newaxis, :]
    r2 = np.sum(diff * diff, axis=2)
    iu = np.triu_indices(n, k=1)
    dist = np.sqrt(r2[iu])
    h = -float(np.sum(gamma_vec[iu[0]] * gamma_vec[iu[1]] * np.log(dist))) / TWO_PI
    p = float(np.sum(gamma_vec * xy[:, 0]))
    q = float(np.sum(gamma_vec * xy[:, 1]))
    imp = float(np.sum(gamma_vec * np.sum(xy * xy, axis=1)))
    return {"H": h, "P": p, "Q": q, "I": imp}


def relative_drifts(inv0: Dict[str, float], inv1: Dict[str, float]) -> Dict[str, float]:
    """Relative drifts |I1 - I0| / max(|I0|, 1) — the registered discipline."""
    return {key: abs(inv1[key] - inv0[key]) / max(abs(inv0[key]), 1.0) for key in inv0}


# ---------------------------------------------------------------------------
# The analytic Jacobian (for the spectral registers)
# ---------------------------------------------------------------------------


def jacobian(state: np.ndarray, gamma_vec: np.ndarray) -> np.ndarray:
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
    """
    n = len(gamma_vec)
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
            gj = gamma_vec[j]
            ii, jj = 2 * i, 2 * j
            jac[ii, ii] += gj * dx * dy / (math.pi * r4)
            jac[ii, jj] += -gj * dx * dy / (math.pi * r4)
            jac[ii, ii + 1] += -gj * (r2 - 2.0 * dy * dy) / (2.0 * math.pi * r4)
            jac[ii, jj + 1] += gj * (r2 - 2.0 * dy * dy) / (2.0 * math.pi * r4)
            jac[ii + 1, ii] += gj * (r2 - 2.0 * dx * dx) / (2.0 * math.pi * r4)
            jac[ii + 1, jj] += -gj * (r2 - 2.0 * dx * dx) / (2.0 * math.pi * r4)
            jac[ii + 1, ii + 1] += -gj * dx * dy / (math.pi * r4)
            jac[ii + 1, jj + 1] += gj * dx * dy / (math.pi * r4)
    return jac


# ---------------------------------------------------------------------------
# The closed-form registers of the regular polygon (Theorem 5)
# ---------------------------------------------------------------------------


def hamiltonian_closed_form(n: int, big_r: float, gamma: float = 1.0) -> float:
    """H(R) = -(Gamma^2 / 2 pi) [ (N(N-1)/2) ln R + (N/2) ln N ]."""
    return -(gamma * gamma / (2.0 * math.pi)) * (
        (n * (n - 1) // 2) * math.log(big_r) + (n / 2.0) * math.log(n)
    )


def distance_product(n: int, big_r: float) -> float:
    """prod_{i<j} |z_i - z_j| = R^{N(N-1)/2} N^{N/2} — the algebraic register."""
    return big_r ** (n * (n - 1) // 2) * n ** (n / 2.0)


def discriminant_binomial(n: int, sigma_mod: float) -> float:
    """|disc(z^N - sigma)| = N^N |sigma|^{N-1} — the discriminant register."""
    return (n**n) * (sigma_mod ** (n - 1))


def hamiltonian_measured(state: np.ndarray, gamma_vec: np.ndarray) -> float:
    """The direct pairwise Hamiltonian (the oracle of the closed form)."""
    return invariants(state, gamma_vec)["H"]
