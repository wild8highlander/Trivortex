#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
PLANETVORTEX — TESTS: THE P-LADDER AND THE COMMITTED PROTOCOLS
============================================================================
The guard of the guard: the quick ladder passes end-to-end, the
committed protocols carry the stable schema, the anchor literals match
the committed files, the exact stage stays exact, and the heptagon
register is cross-pinned against the sibling polyvortex bench (the
N = 7 row of its own W-ladder) — two ladders, no shared code, only the
committed numbers.

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import json
import math
import os

import numpy as np
import pytest

from planetvortex import classical as cl
from planetvortex import fano as fn
from planetvortex import ladder as ld

HERE = os.path.dirname(os.path.abspath(__file__))
MINIROOT = os.path.normpath(os.path.join(HERE, ".."))
PROTOCOL_DIR = os.path.join(MINIROOT, "results", "protocols")

SLUGS = {
    "P1": "P1_anchor",
    "P2": "P2_kepler_register",
    "P3": "P3_planetary_nbody",
    "P4": "P4_fano_algebra",
    "P5": "P5_heptagon_lattice",
    "P6": "P6_seven_cells",
    "P7": "P7_gravity_bridge",
}


def test_quick_ladder_all_pass() -> None:
    """The whole quick ladder is green end-to-end (CI's smoke)."""
    checks = ld.run_ladder("quick")
    assert len(checks) == 7
    for check in checks:
        assert check["passed"], check["check"]


def test_committed_protocols_schema() -> None:
    """Every committed default protocol carries the stable envelope:
    suite, version, stage, preset, date_utc, check.passed = true."""
    for stage, slug in SLUGS.items():
        path = os.path.join(PROTOCOL_DIR, f"{slug}_default.json")
        assert os.path.exists(path), path
        with open(path, encoding="utf-8") as fh:
            report = json.load(fh)
        assert report["suite"] == "planetvortex-ladder"
        assert report["version"] == "2.0.0"
        assert report["stage"] == stage
        assert report["preset"] == "default"
        assert "date_utc" in report
        assert report["check"]["passed"] is True


def test_p1_anchor_literals_pinned() -> None:
    """The committed anchor literals reproduce: the exact chords, the
    (pi/7, 2pi/7, 4pi/7) angle ladder and the Kepler-Earth anchor."""
    path = os.path.join(PROTOCOL_DIR, "P1_anchor_default.json")
    with open(path, encoding="utf-8") as fh:
        committed = json.load(fh)["check"]
    fresh = ld.check_p1_anchor(dps=30)
    assert fresh["exact_literals"]["s1"] == committed["exact_literals"]["s1"]
    assert fresh["exact_literals"]["omega7"] == committed["exact_literals"]["omega7"]
    assert fresh["kepler_earth_relative_error"] <= ld.TOLERANCES["kepler_earth_si"]
    # the heptagon rate literal of the parent framework
    assert abs(fn.ring_omega(1.0, 1.0) - 0.477464829275686) < 1e-15


def test_p4_exactness_is_stable() -> None:
    """The algebra register is deterministic and exact: 168, 24/24,
    the pair axiom, the isomorphism, the conjugacy."""
    fresh = ld.check_p4_algebra()
    assert fresh["group_order_cyclic"] == 168
    assert fresh["group_order_binary"] == 168
    assert fresh["stabilizer_point"] == 24
    assert fresh["stabilizer_line"] == 24
    assert fresh["pair_axiom"] is True
    assert fresh["isomorphism_found"] is True
    assert fresh["groups_conjugate_in_s7"] is True
    assert fresh["congruence_max_abs_error"] <= 1e-12
    assert fresh["passed"] is True


def test_p6_shape_cycle_congruence() -> None:
    """The seven measured shape periods agree to 1e-6 (the dynamical
    PSL(2,7) register) and the Hamiltonians coincide exactly."""
    fresh = ld.check_p6_cells(cell_tmax=60.0, cell_dt=0.01, cell_sample_every=4)
    assert fresh["T_shape_relative_spread"] <= 1e-6
    assert fresh["hamiltonian_spread"] <= 1e-14
    assert fresh["max_shape_deviation"] >= ld.TOLERANCES["not_re_min"]


def test_cross_pin_polyvortex_heptagon() -> None:
    """The sibling oracle: the heptagon rotation of this bench equals
    polyvortex's analytic omega_N at N = 7 bit-for-bit, and the two
    independent Kirchhoff layers assign the same Hamiltonian to the
    same ring — two ladders, no shared code, only committed numbers."""
    from planetvortex import model as md

    pv = pytest.importorskip("polyvortex")
    import polyvortex.classical as pv_classical
    import polyvortex.model as pv_model

    omega_here = fn.ring_omega(1.0, 1.0)
    omega_there = pv_classical.ngon_omega(1.0, 1.0, 7)
    assert omega_here == omega_there
    inv_here = md.invariants(md.ring_state(1.0), np.ones(7))
    inv_there = pv_model.invariants(pv_classical.ngon_initial(7, 1.0), np.ones(7))
    assert abs(inv_here["H"] - inv_there["H"]) < 1e-12
    assert abs(inv_here["I"] - inv_there["I"]) < 1e-12


def test_gravity_bridge_registers() -> None:
    """The bridge: Hill margins above 3, the Schwarzschild arithmetic
    exact, the figure dimensions committed."""
    fresh = ld.check_p7_bridge(dps=30)
    assert fresh["hill_min_margin"] >= ld.TOLERANCES["hill_margin_min"]
    assert fresh["schwarzschild_worst_relative_error"] <= ld.TOLERANCES["schwartz_rel"]
    assert abs(fresh["figure_dimensions_au"]["cell_area_sqrt7_over_4"] - math.sqrt(7) / 4) < 1e-15
    sun_row = fresh["schwarzschild_ladder"][0]
    assert abs(sun_row["r_s_m"] - 2953.25) < 1e-2
