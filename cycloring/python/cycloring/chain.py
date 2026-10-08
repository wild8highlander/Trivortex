#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
CYCLORING — THE DEFECT CHAIN AND THE PERIOD TRANSDUCER
============================================================================
From the triple (N, B, lambda_0) of the level — the cyclotomic order N,
the angular impulse of the frozen ring B = N * Gamma * R0^2 and the frozen
frequency lambda_0 = Gamma (N - 1) / (4 pi R0^2) — the whole defect chain
is built:

    delta     = pi / N                        (the cyclotomic angle)
    k         = max(1, ceil(B lambda_0 / Gamma^2))
                                              (the stiffness index)
    gamma     = delta^4 / k                   (the relative defect)
    delta_eff = delta^5 / k                   (the effective defect)
    W_N       = sum_a P(a, a)                 (the period witness)
    Delta_Ch  = gamma * W_N / (N - 1)         (the combined discriminant)

and the transducer turns the discriminant into the modulation program:

    eps    = Delta / (1 + Delta)               in (0, 1)
    nu     = omega_L (1 + Delta)^3 / (1 + 2 Delta)^{3/2}
           = omega_L (1 - eps^2)^{-3/2}        (the synchronous frequency)
    C_N    = ln(1 + 1/Delta) = -ln(eps)        (the log-stiffness)

The classical limit Delta -> 0 recovers the rigid ring: eps -> 0, nu -> omega_L.

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import math
from typing import Dict, List

from . import periods

LEVELS = (7, 9, 15, 30)


# ---------------------------------------------------------------------------
# The triple and the stiffness index
# ---------------------------------------------------------------------------


def base_frequency(n: int, gamma: float = 1.0, big_r: float = 1.0) -> float:
    """lambda_0 = Gamma (N - 1) / (4 pi R0^2) — the frozen-ring frequency."""
    return gamma * (n - 1) / (4.0 * math.pi * big_r * big_r)


def angular_impulse(n: int, gamma: float = 1.0, big_r: float = 1.0) -> float:
    """B = N Gamma R0^2 — the angular impulse of the frozen ring."""
    return n * gamma * big_r * big_r


def stiffness_index(n: int, gamma: float = 1.0, big_r: float = 1.0) -> int:
    """k = max(1, ceil(B lambda_0 / Gamma^2)) — the stiffness index of the level.

    In the natural units Gamma = R0 = 1 this is ceil(N (N - 1) / (4 pi)):
    the dimensionless product of the two entries of the triple.
    """
    big_b = angular_impulse(n, gamma, big_r)
    lambda0 = base_frequency(n, gamma, big_r)
    return max(1, int(math.ceil(big_b * lambda0 / (gamma * gamma))))


# ---------------------------------------------------------------------------
# The defect chain
# ---------------------------------------------------------------------------


def defect_chain(n: int, gamma: float = 1.0, big_r: float = 1.0) -> Dict[str, float]:
    """The full defect chain of the level n (natural units by default).

    Returns the dictionary with the entries:
        delta, k, gamma, delta_eff, W, Delta_Ch — the chain itself;
        eps, nu_ratio, c_log — the transducer output.
    """
    delta = math.pi / n
    k_idx = stiffness_index(n, gamma, big_r)
    gamma_def = delta**4 / k_idx
    delta_eff = delta**5 / k_idx
    witness = periods.period_witness(n)
    delta_ch = gamma_def * witness / (n - 1)
    eps, nu_ratio, c_log = transducer(delta_ch)
    return {
        "delta": delta,
        "k": float(k_idx),
        "gamma": gamma_def,
        "delta_eff": delta_eff,
        "W": witness,
        "Delta_Ch": delta_ch,
        "eps": eps,
        "nu_ratio": nu_ratio,
        "c_log": c_log,
    }


# ---------------------------------------------------------------------------
# The transducer: the modulation map
# ---------------------------------------------------------------------------


def transducer(delta_ch: float) -> tuple[float, float, float]:
    """Delta_Ch -> (eps, nu/omega_L, C_N) — the modulation program.

    eps     = Delta / (1 + Delta)
    nu      = omega_L (1 + Delta)^3 / (1 + 2 Delta)^{3/2}
            = omega_L (1 - eps^2)^{-3/2}      (the synchronous frequency)
    C_N     = ln(1 + 1/Delta) = -ln(eps)
    """
    if delta_ch <= 0.0:
        raise ValueError("Delta_Ch must be positive")
    eps = delta_ch / (1.0 + delta_ch)
    nu_ratio = ((1.0 + delta_ch) ** 2 / (1.0 + 2.0 * delta_ch)) ** 1.5
    c_log = math.log(1.0 + 1.0 / delta_ch)
    return eps, nu_ratio, c_log


def inverse_transducer(eps: float) -> float:
    """eps -> Delta_Ch: the exact inverse of the amplitude branch."""
    if not 0.0 < eps < 1.0:
        raise ValueError("eps must lie in (0, 1)")
    return eps / (1.0 - eps)


# ---------------------------------------------------------------------------
# The level table
# ---------------------------------------------------------------------------


def level_table(levels: List[int] | tuple = LEVELS, gamma: float = 1.0) -> List[Dict[str, float]]:
    """The registered table of the four cyclotomic levels 7, 9, 15, 30."""
    rows: List[Dict[str, float]] = []
    for n in levels:
        row = {"N": float(n)}
        row.update(defect_chain(n, gamma))
        rows.append(row)
    return rows
