#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The period core: reflection register, normalization, the sine product."""

from __future__ import annotations

import math

import pytest

from cycloring import periods as per

LEVELS = (7, 9, 15, 30)


def test_reflection_identity_float() -> None:
    """Gamma(a/N) Gamma(1-a/N) = pi/sin(pi a/N) in float arithmetic."""
    worst = 0.0
    for n in LEVELS:
        for a in range(1, n):
            worst = max(worst, per.reflection_residual_float(a, n))
    assert worst <= 1e-12


def test_reflection_identity_high_precision() -> None:
    """The mpmath register: residuals at 50 working digits."""
    worst = max(float(res) for n in LEVELS for _, _, _, res in per.boundary_periods_mp(n))
    assert worst <= 1e-30


def test_normalization_p11() -> None:
    """P(1, 1) = 1 exactly at every level."""
    for n in LEVELS:
        assert abs(per.normalized_p_mp(1, 1, n) - 1.0) <= 1e-40


def test_period_symmetry() -> None:
    """Omega_{a,b} = Omega_{b,a}."""
    for n in LEVELS:
        for a in range(1, min(4, n)):
            for b in range(1, min(4, n)):
                assert per.omega(a, b, n) == pytest.approx(per.omega(b, a, n), rel=1e-12)


def test_sine_product() -> None:
    """prod_m 2 sin(pi m / N) = N — the algebraic backbone of Theorem 5."""
    worst = max(float(per.sine_product_residual_mp(n)) for n in LEVELS)
    assert worst <= 1e-30


def test_boundary_values_known_levels() -> None:
    """Spot checks of the exact boundary values."""
    assert per.boundary_period(1, 3) == pytest.approx(2.0 * math.pi / math.sqrt(3.0), rel=1e-12)
    assert per.boundary_period(1, 4) == pytest.approx(math.pi * math.sqrt(2.0), rel=1e-12)
    assert per.boundary_period(2, 4) == pytest.approx(math.pi, rel=1e-12)
    assert per.boundary_period(3, 6) == pytest.approx(math.pi, rel=1e-12)


def test_period_witness_positive_increasing() -> None:
    """W_N > 1 and grows with the level on the registered set."""
    witness = {n: per.period_witness(n) for n in LEVELS}
    for n, w in witness.items():
        assert w > 1.0, f"W_{n} must exceed 1"
    seq = [witness[n] for n in LEVELS]
    assert seq == sorted(seq)
