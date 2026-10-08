#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The generalized closed form (Layer G): pinned literals, the
admissibility threshold (Theorem B), periodicity, kinematics."""

from __future__ import annotations

import math

import numpy as np

import polyvortex.ansatz as an

# the parent ladder's registered literal (verify.analytical_frequency(1, 2pi))
OMEGA_N3_LITERAL = 1.3748022274393588


def test_frequency_pinned_literal() -> None:
    assert an.ansatz_frequency(1.0, 2.0 * math.pi) == OMEGA_N3_LITERAL


def test_amplitude_matches_parent_formula() -> None:
    expected = 1.0 / (math.exp(1.0 / math.pi) - 1.0)
    assert abs(an.ansatz_amplitude(1.0) - expected) <= 1e-15


def test_threshold_value() -> None:
    """C_Ch* = pi*ln(2): exp(C_Ch*/pi) = 2 exactly in real arithmetic."""
    assert abs(an.C_CH_STAR - math.pi * math.log(2.0)) <= 1e-18
    assert abs(an.ansatz_amplitude(an.C_CH_STAR) - 1.0) <= 1e-15


def test_admissibility_boundary_flips() -> None:
    delta = 1e-3
    assert not an.is_admissible(an.C_CH_STAR - delta)
    assert an.is_admissible(an.C_CH_STAR + delta)
    # the equivalence itself, on a mixed grid (Theorem B register)
    for c in (0.5, 1.0, 2.0, 2.1776, 2.1775, 3.0, 7.0, 20.0):
        assert an.is_admissible(c) == (an.ansatz_amplitude(c) < 1.0)


def test_min_radius_admissible() -> None:
    for c in (3.0, 5.0, 10.0):
        eps = an.ansatz_amplitude(c)
        exact = math.sqrt(c) * (1.0 - eps)
        for k in range(3):
            sampled = an.min_radius(c, 2.0 * math.pi, k, 3)
            assert abs(sampled - exact) <= 1e-6


def test_radius_sign_crossing_below_threshold() -> None:
    """Below the threshold the radius changes sign twice per period —
    the degenerate (polar-singular) zone of Theorem B."""
    c = 1.0
    grid = np.linspace(0.0, 2.0 * math.pi / an.ansatz_frequency(c, 2.0 * math.pi), 20000)
    vals = 1.0 + an.ansatz_amplitude(c) * np.cos(an.ansatz_frequency(c, 2.0 * math.pi) * grid)
    assert float(np.min(vals)) < 0.0  # crossing exists


def test_periodicity_of_closed_form() -> None:
    c_ch, t_period = 1.0, 2.0 * math.pi
    omega = an.ansatz_frequency(c_ch, t_period)
    t_r = 2.0 * math.pi / omega
    for k in range(3):
        for t in (0.0, 0.137, 0.5, 0.811):
            diff = abs(
                an.ansatz_radius(t * t_r + t_r, c_ch, t_period, k, 3)
                - an.ansatz_radius(t * t_r, c_ch, t_period, k, 3)
            )
            assert diff <= 1e-12


def test_state_velocity_finite_difference() -> None:
    """d/dt of the closed form must equal the analytic velocity."""
    c_ch, t_period, n = 5.0, 2.0 * math.pi, 4
    h = 1e-6
    t = 0.123 * 2.0 * math.pi / an.ansatz_frequency(c_ch, t_period)
    fd = (an.ansatz_state(t + h, c_ch, t_period, n) - an.ansatz_state(t - h, c_ch, t_period, n)) / (
        2.0 * h
    )
    vel = an.ansatz_velocity(t, c_ch, t_period, n)
    assert float(np.max(np.abs(fd - vel))) <= 1e-9


def test_chaplygin_diagnostic_matches_parent() -> None:
    """The gauge diagnostic mirrors verify.compute_chaplygin."""
    verify = __import__("verify")
    for r, td in ((0.7, 1.3), (2.5, 0.4), (1.0, 1.0)):
        assert (
            abs(an.chaplygin_diagnostic(r, td, 1.0) - verify.compute_chaplygin(r, td, 1.0)) <= 1e-15
        )
