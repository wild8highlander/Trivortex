#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
POLYVORTEX — THE GENERALIZED CLOSED FORM (Layer G, Hypothesis H1)
============================================================================
The topological (gauge) layer of the polyvortex mini-repository: the
N-vortex generalization of the parent Theorem 3.1 closed form,

    r_k(t)     = sqrt(C_Ch) * (1 + eps * cos(omega*t + 2*pi*k/N)),
    theta_k(t) = omega*t + 2*pi*k/N,          k = 0..N-1,
    omega      = (2*pi/T) * exp(C_Ch/pi),
    eps        = 1 / (exp(C_Ch/pi) - 1),

together with the admissibility threshold, the periodicity register and
the Section-6-style gauge diagnostic C_Ch(t) = r^2*(theta_dot - q*A_theta)
with A_theta = 1/r (mirroring `verify.compute_chaplygin` of the parent
ladder).

For N = 3 every function here reproduces the parent ladder exactly
(cross-checked by the tests against pinned literals).

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import math

import numpy as np

# ---------------------------------------------------------------------------
# The admissibility threshold (Theorem B of the monograph)
# ---------------------------------------------------------------------------
# eps(C_Ch) = 1/(exp(C_Ch/pi) - 1) < 1  <=>  exp(C_Ch/pi) > 2
#           <=>  C_Ch > pi*ln(2).
# At C_Ch* = pi*ln(2) the amplitude is exactly eps = 1 and the radius
# r_k(t) touches zero once per period; below the threshold the radius
# changes sign (the polar registers degenerate).

C_CH_STAR = math.pi * math.log(2.0)


def ansatz_frequency(c_ch: float, t_period: float) -> float:
    """omega = (2*pi/T) * exp(C_Ch/pi) — the Theorem 3.1 frequency law."""
    return (2.0 * math.pi / t_period) * math.exp(c_ch / math.pi)


def ansatz_amplitude(c_ch: float) -> float:
    """eps = 1/(exp(C_Ch/pi) - 1) — the Theorem 3.1 amplitude law."""
    return 1.0 / (math.exp(c_ch / math.pi) - 1.0)


def is_admissible(c_ch: float) -> bool:
    """The closed form is non-degenerate iff C_Ch > pi*ln(2) (Theorem B)."""
    return c_ch > C_CH_STAR


def ansatz_radius(t: float, c_ch: float, t_period: float, k: int, n: int) -> float:
    """r_k(t) = sqrt(C_Ch) * (1 + eps*cos(omega*t + 2*pi*k/N))."""
    omega = ansatz_frequency(c_ch, t_period)
    eps = ansatz_amplitude(c_ch)
    r0 = math.sqrt(c_ch) if c_ch > 0.0 else 0.0
    return r0 * (1.0 + eps * math.cos(omega * t + 2.0 * math.pi * k / n))


def ansatz_angle(t: float, c_ch: float, t_period: float, k: int, n: int) -> float:
    """theta_k(t) = omega*t + 2*pi*k/N — the uniform phase choreography."""
    omega = ansatz_frequency(c_ch, t_period)
    return omega * t + 2.0 * math.pi * k / n


def ansatz_state(t: float, c_ch: float, t_period: float, n: int) -> np.ndarray:
    """Flat state [x0, y0, ..., y_{N-1}] of the closed form at time t.

    z_k = r_k(t) * exp(i*theta_k(t)); a negative radius r_k is folded
    into the phase (z_k is unchanged by (r, theta) -> (-r, theta + pi)).
    """
    out = np.zeros(2 * n)
    for k in range(n):
        r = ansatz_radius(t, c_ch, t_period, k, n)
        th = ansatz_angle(t, c_ch, t_period, k, n)
        out[2 * k] = r * math.cos(th)
        out[2 * k + 1] = r * math.sin(th)
    return out


def ansatz_velocity(t: float, c_ch: float, t_period: float, n: int) -> np.ndarray:
    """The analytic time derivative d/dt of `ansatz_state`.

    d/dt z_k = exp(i*theta_k) * (r_dot_k + i*r_k*omega) with
    r_dot_k = -sqrt(C_Ch)*eps*omega*sin(omega*t + 2*pi*k/N).
    """
    omega = ansatz_frequency(c_ch, t_period)
    eps = ansatz_amplitude(c_ch)
    r0 = math.sqrt(c_ch) if c_ch > 0.0 else 0.0
    out = np.zeros(2 * n)
    for k in range(n):
        phi = omega * t + 2.0 * math.pi * k / n
        r = r0 * (1.0 + eps * math.cos(phi))
        r_dot = -r0 * eps * omega * math.sin(phi)
        out[2 * k] = r_dot * math.cos(phi) - r * omega * math.sin(phi)
        out[2 * k + 1] = r_dot * math.sin(phi) + r * omega * math.cos(phi)
    return out


def min_radius(c_ch: float, t_period: float, k: int, n: int, n_grid: int = 4096) -> float:
    """min r_k(t) over one modulation period (dense sampling).

    For an admissible C_Ch the exact minimum is sqrt(C_Ch)*(1 - eps);
    the sampled minimum converges to it quadratically in 1/n_grid.
    """
    omega = ansatz_frequency(c_ch, t_period)
    t_r = 2.0 * math.pi / omega
    grid = np.linspace(0.0, t_r, int(n_grid), endpoint=False)
    r0 = math.sqrt(c_ch) if c_ch > 0.0 else 0.0
    eps = ansatz_amplitude(c_ch)
    vals = 1.0 + eps * np.cos(omega * grid + 2.0 * math.pi * k / n)
    return float(r0 * np.min(vals))


# ---------------------------------------------------------------------------
# The gauge diagnostic (the parent ladder's Section-6 combination)
# ---------------------------------------------------------------------------


def chaplygin_diagnostic(r: float, theta_dot: float, q: float = 1.0) -> float:
    """C_Ch(t) = r^2 * (theta_dot - q*A_theta) with A_theta = 1/r.

    Mirrors `verify.compute_chaplygin` of the parent ladder. Along the
    closed form this combination oscillates by construction and is
    window-dependent — it is reported as a diagnostic, never as a
    pass/fail criterion (the same honesty rule as the parent ladder).
    """
    a_theta = 1.0 / r if r != 0.0 else 0.0
    return r * r * (theta_dot - q * a_theta)


def diagnostic_drift(c_ch: float, t_period: float, n: int, n_points: int = 400) -> float:
    """max |C_Ch_diag(t) - C_Ch_diag(0)| of vortex k = 0 over [0, 100*T]."""
    omega = ansatz_frequency(c_ch, t_period)
    t_max = 100.0 * t_period
    t_vals = np.linspace(0.0, t_max, int(n_points))
    vals = []
    for t in t_vals:
        r = ansatz_radius(float(t), c_ch, t_period, 0, n)
        vals.append(chaplygin_diagnostic(r, omega, 1.0))
    arr = np.array(vals)
    return float(np.max(np.abs(arr - arr[0])))
