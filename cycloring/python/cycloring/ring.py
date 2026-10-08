#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
CYCLORING — THE ROOT SYSTEM OF THE RING AND THE BREATHING PROGRAM
============================================================================
The algebraization register: the regular N-vortex ring

    z_k(t) = r(t) exp(i (nu t + 2 pi k / N)),   k = 0..N-1,

is EXACTLY the root system of the binomial

    z^N = sigma(t),   sigma(t) = r(t)^N exp(i N nu t),

so F_t(z) = prod_k (z - z_k) = z^N - sigma(t). The power sums of the
vortex positions are the roots-of-unity filter:

    S_m = sum_k z_k^m = 0              for 1 <= m <= N - 1,
    S_N = N sigma(t),

the impulse vanishes identically (L = Gamma sum_k z_k = 0), and the
Galois group Gal(Q(zeta_N)/Q) acts on the ring by relabeling the vortices:
sigma_a : zeta_N^k -> zeta_N^{a k}.

The breathing program (the pumped ring):

    r(t) = R0 (1 + eps cos(nu t)),   theta_k(t) = nu t + 2 pi k / N,

with the SYNCHRONOUS frequency nu = omega_L (1 - eps^2)^{-3/2} — the
cycle mean of the frozen-ring transport law Lambda_0 / r(t)^2 with
Lambda_0 = Gamma (N - 1) / (4 pi). Every vortex rides a closed rosette;
after the closure time T_c = 2 pi / nu the whole configuration returns.

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import math
from typing import List, Tuple

import numpy as np

TWO_PI = 2.0 * math.pi


# ---------------------------------------------------------------------------
# The polygon and the master coefficient
# ---------------------------------------------------------------------------


def polygon_positions(n: int, big_r: float = 1.0, theta0: float = 0.0) -> np.ndarray:
    """The frozen regular N-gon: complex positions r exp(i(theta0 + 2 pi k/N))."""
    ks = np.arange(n)
    return big_r * np.exp(1j * (theta0 + TWO_PI * ks / n))


def polygon_positions_xy(n: int, big_r: float = 1.0, theta0: float = 0.0) -> np.ndarray:
    """The frozen polygon as the flat [x0, y0, x1, y1, ...] state."""
    zs = polygon_positions(n, big_r, theta0)
    return np.stack([zs.real, zs.imag], axis=1).ravel()


def master_sigma(big_r: float, nu: float, t: float, n: int) -> complex:
    """sigma(t) = r(t)^N exp(i N nu t) — the master coefficient of z^N = sigma."""
    return (big_r**n) * complex(math.cos(n * nu * t), math.sin(n * nu * t))


def frozen_rate(n: int, gamma: float = 1.0, big_r: float = 1.0) -> float:
    """omega_L = Gamma (N - 1) / (4 pi R^2) — the frozen-ring rotation rate."""
    return gamma * (n - 1) / (4.0 * math.pi * big_r * big_r)


def adiabatic_invariant(n: int, gamma: float = 1.0) -> float:
    """Lambda_0 = omega_L R^2 = Gamma (N - 1) / (4 pi) — radius-free by design."""
    return gamma * (n - 1) / (4.0 * math.pi)


# ---------------------------------------------------------------------------
# The root system and the power sums
# ---------------------------------------------------------------------------


def root_system_residual(zs: np.ndarray, n_probes: int = 8) -> float:
    """max_z |prod_k (z - z_k) - (z^N - sigma)| over probe points on |z| = 2R.

    The polynomial identity of Theorem 1 in floating arithmetic: the ring is
    the full root system of the binomial z^N = sigma with the master
    coefficient sigma = r^N exp(i N theta0) = (-1)^(N-1) prod_k z_k.
    """
    n = len(zs)
    sigma = (-1) ** (n - 1) * complex(np.prod(zs))
    scale = max(1.0, float(np.max(np.abs(zs))) ** n)
    worst = 0.0
    for j in range(n_probes):
        z = 2.0 * np.max(np.abs(zs)) * np.exp(1j * TWO_PI * (j + 0.5) / n_probes)
        prod = np.prod(z - zs)
        resid = abs(prod - (z**n - sigma))
        worst = max(worst, resid / scale)
    return worst


def moment_sums(zs: np.ndarray, m_max: int | None = None) -> List[complex]:
    """S_m = sum_k z_k^m for m = 1..m_max — the roots-of-unity filter."""
    n = len(zs)
    mtop = m_max if m_max is not None else n
    return [complex(np.sum(zs.astype(complex) ** m)) for m in range(1, mtop + 1)]


def impulse(zs: np.ndarray, gamma: float = 1.0) -> complex:
    """L = Gamma sum_k z_k — the linear impulse of the ring (zero identically)."""
    return gamma * complex(np.sum(zs))


def character_amplitudes(zs: np.ndarray) -> np.ndarray:
    """The character decomposition c_m = (1/N) sum_k z_k zeta_N^{-m k}.

    For the polygon only the mode m = 1 is populated: c_1 = r e^{i theta0},
    the master coordinate. Any deformation shows up as new modes.
    """
    n = len(zs)
    ks = np.arange(n)
    grid = np.exp(-2j * np.pi * np.outer(ks, ks) / n)  # grid[k, m] = zeta^{-km}
    return (grid @ zs.astype(complex)) / n


# ---------------------------------------------------------------------------
# The synchronous-breathing program (the pumped ring)
# ---------------------------------------------------------------------------


def pumped_radius(t: float, big_r: float, eps: float, nu: float) -> float:
    """r(t) = R0 (1 + eps cos(nu t)) — the radius program of the pump."""
    return big_r * (1.0 + eps * math.cos(nu * t))


def pumped_positions(t: float, n: int, big_r: float, eps: float, nu: float) -> np.ndarray:
    """Complex positions of the pumped ring at time t."""
    r_t = pumped_radius(t, big_r, eps, nu)
    ks = np.arange(n)
    return r_t * np.exp(1j * (nu * t + TWO_PI * ks / n))


def pumped_positions_xy(t: float, n: int, big_r: float, eps: float, nu: float) -> np.ndarray:
    """The pumped ring as the flat [x0, y0, ...] state."""
    zs = pumped_positions(t, n, big_r, eps, nu)
    return np.stack([zs.real, zs.imag], axis=1).ravel()


def synchronous_frequency(big_r: float, eps: float, gamma: float = 1.0, n: int = 7) -> float:
    """nu = omega_L(R0) (1 - eps^2)^{-3/2} — the synchronous breathing rate.

    The cycle mean of the frozen transport Lambda_0 / r(t)^2 equals
    omega_L(R0) (1 - eps^2)^{-3/2}; the synchronous program chooses nu to
    be exactly this mean, which closes every rosette after T_c = 2 pi / nu.
    """
    return frozen_rate(n, gamma, big_r) / (1.0 - eps * eps) ** 1.5


def closure_time(eps: float, nu: float) -> float:
    """T_c = 2 pi / nu — the closure period of the synchronous program."""
    return TWO_PI / nu


def transport_phase(t: float, big_r: float, eps: float, gamma: float, n: int) -> float:
    """The accumulated phase of the pumped ring: int_0^t Lambda_0 / r(s)^2 ds.

    The polygon invariance forces the angular transport of the pumped ring
    to follow the frozen law at the instantaneous radius; the integral is
    the exact phase program.
    """
    lambda0 = adiabatic_invariant(n, gamma)
    nu = synchronous_frequency(big_r, eps, gamma, n)
    # int Lambda_0 / r^2 dt with r = R0 (1 + eps cos nu t):
    # substitution u = nu t, dt = du / nu
    u = nu * t
    return lambda0 / (nu * big_r * big_r) * _mean_inverse_square_integral(0.0, u, eps)


def _mean_inverse_square_integral(u0: float, u1: float, eps: float) -> float:
    """int_{u0}^{u1} du / (1 + eps cos u)^2 by high-resolution Simpson."""
    n_steps = 20000
    grid = np.linspace(u0, u1, n_steps + 1)
    vals = 1.0 / (1.0 + eps * np.cos(grid)) ** 2
    h = (u1 - u0) / n_steps
    return float(
        h / 3.0 * (vals[0] + vals[-1] + 4.0 * np.sum(vals[1:-1:2]) + 2.0 * np.sum(vals[2:-1:2]))
    )


def mean_transport_ratio(eps: float) -> float:
    """M[(1 + eps cos u)^{-2}] = (1 - eps^2)^{-3/2} — the transport identity.

    Returns the quadrature value of the left side (the right side is the
    closed form certified in the ladder W5).
    """
    val = _mean_inverse_square_integral(0.0, TWO_PI, eps) / TWO_PI
    return val


def closure_residual(n: int, big_r: float, eps: float, nu: float) -> float:
    """max_k |z_k(T_c) - z_k(0)| — the rosette closure register of the program."""
    zs0 = pumped_positions(0.0, n, big_r, eps, nu)
    zs1 = pumped_positions(closure_time(eps, nu), n, big_r, eps, nu)
    return float(np.max(np.abs(zs1 - zs0)))


def rosette_curve(
    k: int, n: int, big_r: float, eps: float, nu: float, t_max: float, n_points: int = 2400
) -> Tuple[np.ndarray, np.ndarray]:
    """The trajectory of vortex k over [0, t_max] as (x, y) arrays."""
    ts = np.linspace(0.0, t_max, n_points)
    ph = nu * ts + TWO_PI * k / n
    r_t = big_r * (1.0 + eps * np.cos(nu * ts))
    return r_t * np.cos(ph), r_t * np.sin(ph)
