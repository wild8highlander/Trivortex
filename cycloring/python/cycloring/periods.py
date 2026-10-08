#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
CYCLORING — THE GAMMA-PERIOD CORE
============================================================================
The period functional of the level N:

    Omega_{a,b} = Gamma(a/N) Gamma(b/N) / Gamma((a+b)/N),   a, b >= 1,

the reflection register Gamma(z) Gamma(1 - z) = pi / sin(pi z), the sine
product prod_m 2 sin(pi m / N) = N, the normalized periods

    P(a, b) = Omega_{a,b} / Omega_{1,1}

and the period witness of the level

    W_N = sum_{a=1}^{N-1} P(a, a).

All exact registers are certified with mpmath (50 working digits); all
floating-point registers are numpy/plain floats for the dynamics layer.

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

import mpmath as mp

MP_DPS = 50

LEVELS = (7, 9, 15, 30)


# ---------------------------------------------------------------------------
# The period functional (high precision)
# ---------------------------------------------------------------------------


def omega_mp(a: int, b: int, n: int) -> mp.mpf:
    """Omega_{a,b} at level n with mpmath precision (a, b >= 1)."""
    with mp.workdps(MP_DPS):
        val = mp.gamma(mp.mpf(a) / n) * mp.gamma(mp.mpf(b) / n) / mp.gamma(mp.mpf(a + b) / n)
        return +val


def omega(a: int, b: int, n: int) -> float:
    """Omega_{a,b} at level n as a plain float."""
    return float(omega_mp(a, b, n))


def normalized_p_mp(a: int, b: int, n: int) -> mp.mpf:
    """P(a, b) = Omega_{a,b} / Omega_{1,1} — the normalized period."""
    with mp.workdps(MP_DPS):
        val = mp.gamma(mp.mpf(a) / n) * mp.gamma(mp.mpf(b) / n) / mp.gamma(mp.mpf(a + b) / n)
        base = mp.gamma(mp.mpf(1) / n) ** 2 / mp.gamma(mp.mpf(2) / n)
        return +(val / base)


def normalized_p(a: int, b: int, n: int) -> float:
    """P(a, b) as a plain float."""
    return float(normalized_p_mp(a, b, n))


# ---------------------------------------------------------------------------
# The reflection register: the algebraic boundary of the period domain
# ---------------------------------------------------------------------------


def reflection_residual_mp(a: int, n: int) -> mp.mpf:
    """|Gamma(a/N) Gamma(1 - a/N) - pi / sin(pi a/N)| at mpmath precision.

    The boundary period Omega_{a, N-a} = Gamma(a/N) Gamma(1 - a/N) / Gamma(1)
    equals pi / sin(pi a / N) EXACTLY — an algebraic multiple of pi.
    """
    with mp.workdps(MP_DPS):
        left = mp.gamma(mp.mpf(a) / n) * mp.gamma(1 - mp.mpf(a) / n)
        right = mp.pi / mp.sin(mp.pi * mp.mpf(a) / n)
        res = abs(left - right)
    return +res


def boundary_periods_mp(n: int) -> List[Tuple[int, mp.mpf, mp.mpf, mp.mpf]]:
    """[(a, Omega_{a,N-a}, pi/sin(pi a/N), residual)] for a = 1..N-1."""
    rows: List[Tuple[int, mp.mpf, mp.mpf, mp.mpf]] = []
    for a in range(1, n):
        with mp.workdps(MP_DPS):
            left = mp.gamma(mp.mpf(a) / n) * mp.gamma(1 - mp.mpf(a) / n)
            right = mp.pi / mp.sin(mp.pi * mp.mpf(a) / n)
            res = abs(left - right)
            rows.append((a, +left, +right, +res))
    return rows


# ---------------------------------------------------------------------------
# The sine product register
# ---------------------------------------------------------------------------


def sine_product_residual_mp(n: int) -> mp.mpf:
    """|prod_{m=1}^{N-1} 2 sin(pi m / N) - N| at mpmath precision."""
    with mp.workdps(MP_DPS):
        prod = mp.mpf(1)
        for m in range(1, n):
            prod *= 2 * mp.sin(mp.pi * mp.mpf(m) / n)
        res = abs(prod - n)
    return +res


# ---------------------------------------------------------------------------
# The period witness W_N
# ---------------------------------------------------------------------------


def period_witness_mp(n: int) -> mp.mpf:
    """W_N = sum_{a=1}^{N-1} P(a, a) — the diagonal period sum of the level."""
    with mp.workdps(MP_DPS):
        total = mp.mpf(0)
        for a in range(1, n):
            total += normalized_p_mp(a, a, n)
    return +total


def period_witness(n: int) -> float:
    """W_N as a plain float."""
    return float(period_witness_mp(n))


# ---------------------------------------------------------------------------
# Float helpers for the dynamics layer
# ---------------------------------------------------------------------------


def boundary_period(a: int, n: int) -> float:
    """The exact boundary value pi / sin(pi a / N) as a float."""
    return math.pi / math.sin(math.pi * a / n)


def omega_11(n: int) -> float:
    """Omega_{1,1} at level n as a float (the normalization scale)."""
    return omega(1, 1, n)


def level_periods(n: int, a_max: int | None = None) -> Dict[Tuple[int, int], float]:
    """The float period table {(a, b): Omega_{a,b}} for 1 <= a, b <= a_max."""
    amax = a_max if a_max is not None else n - 1
    return {(a, b): omega(a, b, n) for a in range(1, amax + 1) for b in range(1, amax + 1)}


def reflection_residual_float(a: int, n: int) -> float:
    """The reflection residual in float arithmetic (for the fast registers)."""
    return abs(math.gamma(a / n) * math.gamma(1.0 - a / n) - math.pi / math.sin(math.pi * a / n))
