#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The classical layer: the Kirchhoff N-gon formula, its N = 3
reduction, the measured rotation rate, the Havelock threshold."""

from __future__ import annotations

import math

import numpy as np

import polyvortex.classical as cl
import polyvortex.model as md

# the parent ladder's registered Lagrange literal (omega at Gamma=1, a=1)
LAGRANGE_LITERAL = 0.477464829275686


def test_n3_reduction_to_parent_lagrange() -> None:
    """omega_N at (N=3, R=a/sqrt(3)) equals 3*Gamma/(2*pi*a^2)."""
    a = 1.0
    assert abs(cl.ngon_omega(1.0, a / math.sqrt(3.0), 3) - 3.0 / (2.0 * math.pi)) <= 1e-15
    assert abs(cl.ngon_omega(1.0, a / math.sqrt(3.0), 3) - LAGRANGE_LITERAL) <= 1e-14


def test_omega7_numeric_coincidence() -> None:
    """(N=7, R=1, Gamma=1): omega = 6/(4pi) = 3/(2pi) — the parent's
    Lagrange literal reappears as the heptagon rate. A useful
    cross-ladder handshake, recorded in the monograph (Section 3)."""
    assert abs(cl.ngon_omega(1.0, 1.0, 7) - LAGRANGE_LITERAL) <= 1e-14


def test_chord_table_shape_register() -> None:
    state = cl.ngon_initial(5, 2.0)
    gamma = np.full(5, 1.0)
    assert cl.shape_deviation(state, gamma, 2.0) <= 1e-12


def test_measured_rotation_rate() -> None:
    for n in (3, 6):
        state = cl.ngon_initial(n, 1.0)
        gamma = np.full(n, 1.0)
        omega = cl.ngon_omega(1.0, 1.0, n)
        dt = (2.0 * math.pi / omega) / 500
        measured = cl.measured_rotation_rate(state, gamma, dt, 500, omega)
        assert abs(measured - omega) / omega <= 1e-8


def test_havelock_threshold() -> None:
    """Stable for N <= 7, unstable for N >= 8 (Havelock 1931; Khazin)."""
    rates = {}
    for n in range(2, 9):
        state = cl.ngon_initial(n, 1.0)
        gamma = np.full(n, 1.0)
        omega = cl.ngon_omega(1.0, 1.0, n)
        rates[n] = md.max_growth_rate(state, gamma, omega)
    for n in range(2, 8):
        assert rates[n] <= 1e-7, f"N={n} must be stable, got {rates[n]}"
    assert rates[8] > 0.1, "N=8 must be clearly unstable"
