#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pytest suite for the TRIVORTEX verification ladder.

Runs the four checks of verification/trivortex/python/verify.py in a
CI-friendly 'quick' configuration and additionally pins the analytic
building blocks of Theorem 3.1 against hard reference values.

Run from the repository root:
    python -m pytest verification/tests/ -v
"""

import importlib.util
import math
import os
import sys

import numpy as np
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
VERIFY_PATH = os.path.join(HERE, "..", "trivortex", "python", "verify.py")

_spec = importlib.util.spec_from_file_location("trivortex_verify", VERIFY_PATH)
tv = importlib.util.module_from_spec(_spec)
sys.modules["trivortex_verify"] = tv
_spec.loader.exec_module(tv)


# ---------------------------------------------------------------------------
# Analytic layer — Theorem 3.1 building blocks (hard reference values)
# ---------------------------------------------------------------------------


class TestTheorem31:
    def test_frequency_reference_value(self):
        # omega = (2*pi/T) * exp(C_Ch/pi), C_Ch = 1, T = 2*pi
        expected = (2.0 * math.pi / (2.0 * math.pi)) * math.exp(1.0 / math.pi)
        assert tv.analytical_frequency(1.0, 2.0 * math.pi) == pytest.approx(expected, rel=1e-15)
        assert expected == pytest.approx(1.3748022274393588, rel=1e-12)

    def test_amplitude_reference_value(self):
        # eps = 1/(exp(C_Ch/pi) - 1)
        expected = 1.0 / (math.exp(1.0 / math.pi) - 1.0)
        assert tv.analytical_amplitude(1.0) == pytest.approx(expected, rel=1e-15)

    def test_amplitude_small_cch_guard(self):
        # for C_Ch <= 0.01 the document's guard returns eps = 1
        assert tv.analytical_amplitude(0.005) == 1.0

    def test_closed_form_periodicity(self):
        omega = tv.analytical_frequency(1.0, 2.0 * math.pi)
        t_r = 2.0 * math.pi / omega
        for k in range(3):
            r1 = tv.analytical_radius(1.234, 1.0, 2.0 * math.pi, k)
            r2 = tv.analytical_radius(1.234 + t_r, 1.0, 2.0 * math.pi, k)
            assert r1 == pytest.approx(r2, abs=1e-12)

    def test_chaplygin_formula_shape(self):
        # C_Ch = r^2 * (theta_dot - q * A_theta); with A_theta = 1/r:
        # C_Ch = r^2 * theta_dot - q * r
        r, theta_dot, q = 0.5, 2.0, 1.0
        assert tv.compute_chaplygin(r, theta_dot, q) == pytest.approx(
            r * r * theta_dot - q * r, rel=1e-15
        )


class TestLagrangeSolution:
    def test_analytic_omega_reference(self):
        # omega = 3*Gamma/(2*pi*a^2) — the classical Lagrange value
        assert tv.lagrange_omega(1.0, 1.0) == pytest.approx(3.0 / (2.0 * math.pi), rel=1e-15)
        assert tv.lagrange_omega(2.0, 3.0) == pytest.approx(6.0 / (2.0 * math.pi * 9.0), rel=1e-15)

    def test_equilateral_initial_shape(self):
        state = tv.equilateral_initial(1.0)
        xy = state.reshape(3, 2)
        sides = tv._sides(xy)
        assert sides == pytest.approx([1.0, 1.0, 1.0], abs=1e-14)

    def test_vortex_rhs_rigid_rotation_of_pair(self):
        # two equal vortices at (+1,0) and (-1,0): no radial motion, and the
        # pair rotates counter-clockwise (right vortex up, left vortex down)
        state = np.array([1.0, 0.0, -1.0, 0.0])
        gamma = np.array([1.0, 1.0])
        d = tv.vortex_rhs(state, gamma)
        assert d[0] == pytest.approx(0.0, abs=1e-15)  # dx0: antisymmetry
        assert d[2] == pytest.approx(0.0, abs=1e-15)  # dx1: antisymmetry
        assert d[1] == pytest.approx(0.5 / (2.0 * math.pi), rel=1e-14)  # dy0 > 0
        assert d[3] == pytest.approx(-0.5 / (2.0 * math.pi), rel=1e-14)  # dy1 < 0


# ---------------------------------------------------------------------------
# Numerical ladder — quick preset (CI-friendly)
# ---------------------------------------------------------------------------


class TestVerificationLadder:
    @classmethod
    def setup_class(cls):
        cfg = tv.PRESETS["quick"]
        cls.v1 = tv.check_v1_theorem31(n_points=cfg["n_points_cch"])
        cls.v2 = tv.check_v2_lagrange_rotation(
            rotations=cfg["rotations"], steps_per_period=cfg["steps_per_period"]
        )
        cls.v3 = tv.check_v3_invariants(
            rotations=cfg["rotations"], steps_per_period=cfg["steps_per_period"]
        )
        cls.v4 = tv.check_v4_robustness(
            rotations=max(2, cfg["rotations"] - 2), steps_per_period=cfg["steps_per_period"]
        )

    def test_v1_choreography(self):
        assert self.v1["passed"], self.v1

    def test_v2_lagrange_rotation(self):
        assert self.v2["passed"], self.v2

    def test_v3_invariants(self):
        assert self.v3["passed"], self.v3

    def test_v4_robustness(self):
        assert self.v4["passed"], self.v4


class TestReportGeneration:
    def test_json_report_serializes(self, tmp_path):
        rc = tv.run("quick", str(tmp_path))
        assert rc == 0
        files = list(tmp_path.glob("trivortex_verify_quick_*.json"))
        assert len(files) == 1
        import json

        with open(files[0], encoding="utf-8") as f:
            report = json.load(f)
        assert report["suite"] == "trivortex-verification"
        assert report["all_passed"] is True
        assert report["checks_total"] == 4
