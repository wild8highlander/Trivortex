#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
POLYVORTEX — THE CLASSICAL LAYER: RELATIVE EQUILIBRIA OF THE N-GON
============================================================================
The classical layer of the polyvortex mini-repository: the regular
N-gon relative equilibrium of equal point vortices (Kirchhoff 1876),
its rigid rotation rate

    omega_N = Gamma * (N - 1) / (4 * pi * R^2),

the chord table used by the shape register, and the Havelock stability
classification realized through the co-rotating spectrum of
`model.corotating_spectrum`.

For N = 3 with circumradius R = a/sqrt(3) the formula reduces to the
parent ladder's omega = 3*Gamma/(2*pi*a^2) — pinned by the tests.

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import math

import numpy as np


def ngon_initial(n: int, big_r: float, phase: float = 0.0) -> np.ndarray:
    """N equal vortices at the vertices of a regular N-gon, radius big_r."""
    out = np.zeros(2 * n)
    for k in range(n):
        ang = phase + 2.0 * math.pi * k / n
        out[2 * k] = big_r * math.cos(ang)
        out[2 * k + 1] = big_r * math.sin(ang)
    return out


def ngon_omega(gamma: float, big_r: float, n: int) -> float:
    """omega_N = Gamma*(N-1)/(4*pi*R^2) — the Kirchhoff rotation rate."""
    return gamma * (n - 1) / (4.0 * math.pi * big_r * big_r)


def chord_table(n: int, big_r: float) -> np.ndarray:
    """Expected pairwise distances of the regular N-gon, indexed by
    the cyclic separation m = 1..N-1: c_m = 2*R*sin(pi*m/N)."""
    return np.array([2.0 * big_r * math.sin(math.pi * m / n) for m in range(1, n)])


def shape_deviation(state: np.ndarray, gamma: np.ndarray, big_r: float) -> float:
    """Max deviation of the pairwise distances from the regular N-gon
    chord table (the N-generic shape register of stage W2)."""
    n = len(gamma)
    xy = np.asarray(state, dtype=float).reshape(n, 2)
    chords = chord_table(n, big_r)
    worst = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            m = min(j - i, n - (j - i))
            d = float(np.linalg.norm(xy[i] - xy[j]))
            worst = max(worst, abs(d - chords[m - 1]))
    return worst


def unwrap_angle_delta(ang_start: float, ang_end: float, expected_total: float) -> float:
    """Lift the raw angle difference to the branch nearest the expected
    total rotation (the parent ladder's unwrap discipline)."""
    raw = ang_end - ang_start
    return raw + 2.0 * math.pi * round((expected_total - raw) / (2.0 * math.pi))


def measured_rotation_rate(
    state0: np.ndarray, gamma: np.ndarray, dt: float, n_steps: int, omega_ref: float
) -> float:
    """Integrate n_steps RK4 steps and measure the rotation rate of
    vortex k = 0 from the unwrapped polar angle."""
    from .model import integrate

    n = len(gamma)
    xy0 = np.asarray(state0, dtype=float).reshape(n, 2)
    ang_start = math.atan2(xy0[0, 1], xy0[0, 0])
    state = integrate(state0, gamma, dt, n_steps)
    xy = state.reshape(n, 2)
    ang_end = math.atan2(xy[0, 1], xy[0, 0])
    expected = omega_ref * n_steps * dt
    total = unwrap_angle_delta(ang_start, ang_end, expected)
    return total / (n_steps * dt)
