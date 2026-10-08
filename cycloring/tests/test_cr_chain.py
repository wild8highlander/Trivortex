#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The defect chain and the period transducer."""

from __future__ import annotations

import math

import pytest

from cycloring import chain as ch

LEVELS = (7, 9, 15, 30)


def test_stiffness_index_natural_units() -> None:
    """k = ceil(N(N-1)/(4 pi)) in the natural units Gamma = R0 = 1."""
    assert ch.stiffness_index(7) == 4
    assert ch.stiffness_index(9) == 6
    assert ch.stiffness_index(15) == 17
    assert ch.stiffness_index(30) == 70


def test_defect_monotone_decreasing() -> None:
    """gamma = delta^4 / k strictly decreases with the level."""
    gammas = [ch.defect_chain(n)["gamma"] for n in range(4, 31)]
    assert all(gammas[i] > gammas[i + 1] for i in range(len(gammas) - 1))


def test_transducer_amplitude_bounds() -> None:
    """eps = Delta/(1+Delta) lies in (0, 1) and C_N = -ln(eps)."""
    for d in (1e-9, 1e-3, 0.1, 1.0, 10.0):
        eps, nu_ratio, c_log = ch.transducer(d)
        assert 0.0 < eps < 1.0
        assert nu_ratio > 1.0
        assert c_log > 0.0
        assert c_log == pytest.approx(-math.log(eps), rel=1e-12)


def test_transducer_frequency_identity() -> None:
    """nu/omega_L = (1-eps^2)^{-3/2} exactly across the Delta grid."""
    for d in (1e-6, 1e-3, 0.01, 0.1, 1.0):
        eps, nu_ratio, _ = ch.transducer(d)
        assert nu_ratio == pytest.approx(1.0 / (1.0 - eps * eps) ** 1.5, rel=1e-12)


def test_inverse_transducer_round_trip() -> None:
    """Delta = eps/(1-eps) — the exact inverse of the amplitude branch."""
    for d in (1e-7, 1e-3, 0.05, 2.0):
        eps, _, _ = ch.transducer(d)
        assert ch.inverse_transducer(eps) == pytest.approx(d, rel=1e-14)


def test_classical_limit() -> None:
    """Delta -> 0 recovers the rigid ring: eps -> 0, nu -> omega_L."""
    eps, nu_ratio, c_log = ch.transducer(1e-12)
    assert eps <= 2e-12
    assert abs(nu_ratio - 1.0) <= 3e-12
    assert c_log >= math.log(1e12 / 2)


def test_level_table_ordering() -> None:
    """The stiffness ordering of the four registered levels."""
    rows = ch.level_table(LEVELS)
    eps_seq = [row["eps"] for row in rows]
    c_seq = [row["c_log"] for row in rows]
    assert all(eps_seq[i] > eps_seq[i + 1] for i in range(len(eps_seq) - 1))
    assert all(c_seq[i] < c_seq[i + 1] for i in range(len(c_seq) - 1))


def test_inverse_transducer_rejects_bad_input() -> None:
    """eps outside (0, 1) is rejected."""
    with pytest.raises(ValueError):
        ch.inverse_transducer(0.0)
    with pytest.raises(ValueError):
        ch.inverse_transducer(1.0)
    with pytest.raises(ValueError):
        ch.transducer(0.0)
