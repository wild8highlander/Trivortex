#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The W-ladder end-to-end (quick preset) and the "bound to a run"
discipline: the committed default protocols must agree with a fresh
computation of the preset-independent registers."""

from __future__ import annotations

import json
import math
import os

import numpy as np

import polyvortex.ansatz as an
import polyvortex.classical as cl
import polyvortex.ladder as ladder
import polyvortex.model as md

PROTOCOL_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "protocols")
)


def test_quick_ladder_all_pass() -> None:
    checks = ladder.run_ladder("quick")
    assert all(c["passed"] for c in checks), [c["check"] for c in checks if not c["passed"]]


def test_w1_pinned_literals_exact() -> None:
    check = ladder.check_w1_anchor(n_points=100)
    assert check["frequency_anchor_error"] == 0.0
    assert check["amplitude_anchor_error"] == 0.0
    assert check["passed"]


def _load(stage_file: str) -> dict:
    with open(os.path.join(PROTOCOL_DIR, stage_file), encoding="utf-8") as f:
        return json.load(f)["check"]


def test_protocols_bound_to_run_stability() -> None:
    """The committed W4 protocol must equal a fresh spectrum (deterministic
    eigenvalue computation, preset-independent). The agreement band is the
    protocol's own stability_tolerance (1e-7): the register is consumed by
    the W4 stable/unstable classifier, and bit-for-bit LAPACK reproduction
    across BLAS builds is not part of the contract."""
    committed = _load("W4_stability_default.json")
    tol = committed["params"]["stability_tolerance"]
    for row in committed["per_N"]:
        n = row["N"]
        state = cl.ngon_initial(n, 1.0)
        gamma = np.full(n, 1.0)
        omega = cl.ngon_omega(1.0, 1.0, n)
        fresh = md.max_growth_rate(state, gamma, omega)
        assert abs(fresh - row["max_Re_lambda"]) <= tol


def test_protocols_bound_to_run_anchors() -> None:
    """W1/W5 anchors are preset-independent literals."""
    w1 = _load("W1_anchor_default.json")
    assert w1["params"]["omega"] == 1.3748022274393588
    w5 = _load("W5_admissibility_default.json")
    assert abs(w5["threshold_C_Ch_star"] - math.pi * math.log(2.0)) <= 1e-18
    assert w5["equivalence_violations"] == 0


def test_protocols_bound_to_run_bridge() -> None:
    """The W7 integral identity is a preset-independent mathematical fact;
    the committed default run certified it to <= 1e-13."""
    w7 = _load("W7_bridge_default.json")
    assert w7["integral_identity_max_relative_error"] <= 1e-13
    assert w7["bridge_max_relative_error"] <= 1e-13
    assert w7["compatibility_selfcheck_max_relative_error"] <= 1e-13
    # and the bridge register holds for a fresh (N, eps) probe
    eps = 0.5
    numeric = ladder._gauss_legendre(
        lambda phi: cl.ngon_omega(1.0, 1.0, 4) / (1.0 + eps * np.cos(phi)) ** 2, 200
    ) / (2.0 * math.pi)
    exact = cl.ngon_omega(1.0, 1.0, 4) * (1.0 - eps * eps) ** (-1.5)
    assert abs(numeric - exact) / exact <= 1e-13


def test_obstruction_register_from_protocol() -> None:
    """W6: the induced radial velocity of the symmetric pulsation is
    machine-zero; the phase-shifted H1 shape deviates linearly with
    slope sqrt(3)/2 (measured in the committed protocol)."""
    w6 = _load("W6_obstruction_default.json")
    for row in w6["symmetric_pulsation"]:
        assert row["max_abs_induced_radial_velocity"] <= 1e-12
    slopes = [row["max_shape_register_deviation"] / row["eps"] for row in w6["phase_shifted_H1"]]
    for slope in slopes:
        assert abs(slope - math.sqrt(3.0) / 2.0) <= 1e-3
