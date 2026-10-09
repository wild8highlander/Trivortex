#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The V-register guard: the spatial registers (V1) and the closed
gravifigure (V2) pinned by the pytest suite."""

from __future__ import annotations

import math

import numpy as np
import pytest

from planetvortex import classical as cl
from planetvortex import klein as kl
from planetvortex import spatial as sp

# ---------------------------------------------------------------------------
# V1 — the tilt algebra
# ---------------------------------------------------------------------------


def test_tilt_matrix_is_orthogonal_for_all_bodies() -> None:
    for row in cl.SPATIAL_REGISTER + cl.DWARF_SPATIAL:
        tilt = sp.tilt_matrix(row.inclination_deg, row.node_deg)
        assert np.max(np.abs(tilt.T @ tilt - np.eye(3))) <= 1e-15
        assert abs(np.linalg.det(tilt) - 1.0) <= 1e-15


def test_tilt_sends_ecliptic_normal_to_orbit_normal() -> None:
    reg = cl.SPATIAL_REGISTER[0]  # Mercury, i = 7.005 deg
    tilt = sp.tilt_matrix(reg.inclination_deg, reg.node_deg)
    n = sp.orbit_normal(tilt)
    i = reg.inclination_deg * math.pi / 180.0
    om = reg.node_deg * math.pi / 180.0
    expected = np.array([math.sin(i) * math.sin(om), -math.sin(i) * math.cos(om), math.cos(i)])
    assert np.max(np.abs(n - expected)) <= 1e-15
    assert abs(float(n @ n) - 1.0) <= 1e-15


def test_arc_register_is_exact_and_monotone() -> None:
    rows = sp.inclination_register()
    assert len(rows) == 11
    arcs = sorted(r["arc_au"] for r in rows)
    assert all(a < b for a, b in zip(arcs, arcs[1:]))  # strictly monotone
    # Earth's arc: the ecliptic is Earth's plane (i ~ 0)
    earth = next(r for r in rows if r["body"] == "Earth")
    assert earth["arc_au"] <= 1e-6
    # Mercury's arc: R_bar * i with R_bar = 1 AU
    mercury = next(r for r in rows if r["body"] == "Mercury")
    expect = math.radians(7.00497902)
    assert abs(mercury["arc_au"] - expect) <= 1e-15


def test_mutual_inclination_extreme_is_eris() -> None:
    mutual = sp.mutual_inclinations()
    assert mutual["n_pairs"] == 55
    assert mutual["max_pair"][0] in ("Eris", "Neptune")
    assert mutual["max_pair"][1] in ("Eris", "Neptune")
    assert mutual["max_mutual_deg"] > 40.0


# ---------------------------------------------------------------------------
# V1 — the 3D two-body sanity and the spatial stage
# ---------------------------------------------------------------------------


def test_kepler_solve_roundtrip() -> None:
    e = 0.2
    en_true = 1.1
    m = en_true - e * math.sin(en_true)
    en = sp._kepler_solve(m, e)
    assert abs(en - en_true) <= 1e-12


def test_orbital_state_radius_matches_conic() -> None:
    a, e = 1.5, 0.1
    rx, _vx = sp._orbital_state(a, e, 10.0, 30.0, 100.0, 0.0)
    r = float(np.linalg.norm(rx))
    assert abs(r - a * (1.0 - e)) <= 1e-12  # at perihelion (M = 0)


def test_spatial_initial_state_has_zero_momentum() -> None:
    state = sp.spatial_initial_state()
    masses = sp.nb.planet_masses()
    p = masses[:, None] * state[:, 3:]
    assert float(np.max(np.abs(p.sum(axis=0)))) <= 1e-12


def test_v1_stage_quick_preset_passes() -> None:
    check = sp.run_v1("quick")
    assert check["passed"]
    assert check["tilt_registers"]["n_bodies"] == 11
    assert check["energy_drift_relative"] <= sp.V1_TOLERANCES["spatial_energy"]


# ---------------------------------------------------------------------------
# V2 — the group and map layers
# ---------------------------------------------------------------------------


def test_pgl2_7_has_336_classes_and_psl_168() -> None:
    pgl = kl.PGLModel()
    assert len(pgl.elements) == 336
    assert sum(pgl.is_psl) == 168


def test_coxeter_triple_satisfies_klein_relations() -> None:
    km = kl.KleinMap.build()
    pgl = kl.PGLModel()
    c_class = pgl.index[kl._pgl_canon(km.elements[km.product_c])]
    x, y, z = pgl.find_coxeter_triple(c_class)
    assert pgl.order(pgl.table[y][z]) == 7
    assert pgl.order(pgl.table[x][z]) == 3
    assert pgl.order(pgl.table[x][y]) == 2
    # the untwisted pin: the radial product generates the witness
    # stabilizer <c> (it is c or its inverse)
    yz = pgl.table[y][z]
    inverse_c = next(j for j in range(336) if pgl.table[c_class][j] == pgl.identity)
    assert yz in (c_class, inverse_c)


def test_flag_certificate_is_simply_transitive() -> None:
    km = kl.KleinMap.build()
    pgl = kl.PGLModel()
    c_class = pgl.index[kl._pgl_canon(km.elements[km.product_c])]
    phi, n = kl.flag_certificate(km, pgl, pgl.find_coxeter_triple(c_class))
    assert phi is not None and n == 336
    assert len(set(phi.values())) == 336


def test_klein_map_registers() -> None:
    km = kl.KleinMap.build()
    summary = km.register_summary()
    assert summary["V"] == 56 and summary["E"] == 84 and summary["F"] == 24
    assert summary["euler"] == -4
    assert summary["vertex_degrees"] == [3]
    assert summary["face_lengths"] == [7]
    assert summary["n_antipodal_pairs"] == 12
    assert km.is_connected() and km.is_orientable()


def test_klein_map_flags_are_336_with_168_white() -> None:
    km = kl.KleinMap.build()
    flags = km.all_flags()
    assert len(flags) == 336
    white = [f for f in flags if km.flag_triple_element(f) is not None]
    assert len(white) == 168


def test_budget_closure_is_exact_at_dps() -> None:
    exact = kl.register_algebra_exact(dps=30)
    assert exact["budget_ok"] and exact["area_ok"]
    assert exact["pythagoras_ok"] and exact["s_sum_ok"]


def test_register_algebra_lightest_register_keeps_margin() -> None:
    algebra = kl.register_algebra_float()
    assert algebra["min_hyperbolicity_margin"] > 0.0
    sun = max(algebra["bodies"], key=lambda r: r["s"])
    ceres = min(algebra["bodies"], key=lambda r: r["s"])
    assert sun["body"] == "Sun" and ceres["body"] == "Ceres"
    assert sun["area"] > ceres["area"]


def test_register_dims_against_x4_regular_case() -> None:
    # at the regular vertex angle 2*pi/3 the X4 literals must return
    big_r, edge, inr, area = kl.register_dims(kl.REGULAR_ANGLE)
    assert (
        abs(math.cosh(big_r) - (1.0 / math.tan(math.pi / 3.0)) * (1.0 / math.tan(math.pi / 7.0)))
        <= 1e-14
    )
    assert abs(area - math.pi / 3.0) <= 1e-14
    # the hyperbolic Pythagoras
    assert abs(math.cosh(big_r) - math.cosh(edge / 2.0) * math.cosh(inr)) <= 1e-12


def test_disk_witness_matches_closed_forms() -> None:
    wit = kl._disk_witness_for(kl.REGULAR_ANGLE)
    big_r, edge, _inr, _area = kl.register_dims(kl.REGULAR_ANGLE)
    assert abs(wit["circumradius"] - big_r) <= 1e-9
    assert abs(wit["edge"] - edge) <= 1e-9
    assert abs(wit["angle"] - kl.REGULAR_ANGLE) <= 1e-12


def test_chamber_patch_closes_at_24_distinct_tiles() -> None:
    km = kl.KleinMap.build()
    patch = kl.build_chamber_patch(km)
    assert not patch.errors
    assert patch.chambers == 336
    assert len(patch.heptagons) == 24
    assert patch.flag_certificate
    assert patch.interior_sides + len(patch.boundary_pairs) == 84
    faces = sorted(h.face_coset for h in patch.heptagons)
    assert faces == list(range(24))


def test_body_assignment_leads_with_the_sun() -> None:
    km = kl.KleinMap.build()
    assignment = kl.assign_bodies(km)
    assert len(assignment) == 12
    assert assignment[0]["body"] == "Sun"
    names = [row["body"] for row in assignment]
    assert set(names) == set(kl.body_names())


def test_v2_stage_default_preset_passes() -> None:
    check = kl.run_v2("default")
    assert check["passed"]
    assert check["chamber_patch"]["chambers"] == 336
    exact = check["exact_registers"]
    assert float(exact["alpha_sum_residual"]) <= 1e-40


def test_v_register_runs_both_stages() -> None:
    from planetvortex import vregister as vr

    report = vr.run_v_register("quick")
    assert report["all_passed"]
    assert report["V1"]["passed"] and report["V2"]["passed"]
