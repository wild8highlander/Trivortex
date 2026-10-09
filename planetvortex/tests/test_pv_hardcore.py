#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
PLANETVORTEX — TESTS: THE HARDCORE X-REGISTER (X1..X6)
============================================================================
The guard of the hardcore layer. Every test re-runs an adversarial
stage at its quick dial: the brute-force group theory (X1, X2), the
(2,3,7) generation and the Hurwitz/Klein arithmetic (X3), the exact
hyperbolic figure with its numerical witness (X4), the integrator
certification (X5) and the 1PN perihelion bridge (X6). The committed
default protocols are schema-pinned like the P-ladder ones.

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import json
import os

import pytest

from planetvortex import hardcore as hc

HERE = os.path.dirname(os.path.abspath(__file__))
MINIROOT = os.path.normpath(os.path.join(HERE, ".."))
PROTOCOL_DIR = os.path.join(MINIROOT, "results", "protocols")

X_SLUGS = {
    "X1": "X1_sl2_enumeration",
    "X2": "X2_group_actions",
    "X3": "X3_triangle_hurwitz",
    "X4": "X4_hyperbolic_figure",
    "X5": "X5_integrator_certification",
    "X6": "X6_pn_perihelion",
}


def test_quick_xregister_all_pass() -> None:
    """The whole quick X-register is green end-to-end (CI's smoke)."""
    checks = hc.run_hardcore("quick")
    assert len(checks) == 6
    for check in checks:
        assert check["passed"], check["check"]


# ---------------------------------------------------------------------------
# X1 — the brute-force PSL(2,7)
# ---------------------------------------------------------------------------


def test_x1_enumeration_exact() -> None:
    """2401 matrices -> |GL| = 2016, |SL| = 336, |PSL| = 168, the quotient
    2-to-1, the centres, the order census and the class equation."""
    check = hc.check_x1_enumeration()
    assert check["passed"]
    assert check["matrices_enumerated"] == 2401
    assert check["group_order_gl"] == 2016
    assert check["group_order_sl"] == 336
    assert check["group_order_psl"] == 168
    assert check["quotient_exactly_2_to_1"] is True
    assert check["element_order_census"] == {1: 1, 2: 21, 3: 56, 4: 42, 7: 48}
    assert check["conjugacy_class_sizes"] == [1, 21, 24, 24, 42, 56]
    assert check["simple"] is True


def test_x1_simplicity_certificate_is_exhaustive() -> None:
    """The simplicity certificate enumerates all 2^5 = 32 unions of the
    nontrivial conjugacy classes; none forms a proper normal subgroup."""
    from planetvortex.hardcore import (
        _conjugacy_classes,
        _psl_mult_table,
        psl_elements,
    )

    elems = psl_elements()
    table = _psl_mult_table(elems)
    classes = _conjugacy_classes(elems, table)
    assert sorted(len(c) for c in classes) == [1, 21, 24, 24, 42, 56]
    nontrivial = len(classes) - 1
    assert 1 << nontrivial == 32  # every union was examined
    check = hc.check_x1_enumeration()
    assert check["normal_subgroup_union_found"] is False


# ---------------------------------------------------------------------------
# X2 — the two actions and the Sylow census
# ---------------------------------------------------------------------------


def test_x2_sylow_census() -> None:
    """n7 = 8, n3 = 28, n2 = 21; the normalizers 21 and 8; the Frobenius-21
    signature (1, 14, 6)."""
    check = hc.check_x2_actions()
    assert check["sylow_7_count"] == 8
    assert check["sylow_3_count"] == 28
    assert check["sylow_2_count"] == 21
    assert check["normalizer_sylow7_order"] == 21
    assert check["normalizer_sylow2_order"] == 8
    assert check["normalizer_sylow7_order_census"] == {1: 1, 3: 14, 7: 6}


def test_x2_seven_point_action_and_bridge() -> None:
    """The action on one S_4 class is faithful and transitive on 7 points;
    its image is conjugate in S_7 to the research model of fano.py; the
    stabilizer carries the S_4 signature (1, 9, 8, 6)."""
    check = hc.check_x2_actions()
    assert check["s4_subgroup_count"] == 7
    assert check["s4_subgroup_count_all_classes"] == 14
    assert check["s4_stabilizer_order_census"] == {1: 1, 2: 9, 3: 8, 4: 6}
    assert check["action7_image_order"] == 168
    assert check["action7_kernel"] == 1
    assert check["action7_transitive"] is True
    assert check["bridge_to_research_model"] is True
    assert check["bridge_sigma"] is not None


def test_x2_eight_point_action_is_2_transitive() -> None:
    """The Sylow-7 action: 168 distinct permutations, one orbit on the 56
    ordered pairs (2-transitive) and one orbit on the 56 triples
    (3-homogeneous) — the natural P^1(F_7) action."""
    check = hc.check_x2_actions()
    assert check["action8_image_order"] == 168
    assert check["action8_2_transitive"] is True
    assert check["action8_ordered_pair_orbit_size"] == 56
    assert check["action8_triple_orbit_size"] == 56


# ---------------------------------------------------------------------------
# X3 — the (2,3,7) generation, Hurwitz, Klein quartic
# ---------------------------------------------------------------------------


def test_x3_all_237_pairs_generate() -> None:
    """All 336 (2,3,7) pairs generate the whole group; the product-order
    distribution over the 1176 involutions-times-order-3 pairs is the
    committed one."""
    check = hc.check_x3_triangle()
    assert check["n_pairs_237"] == 336
    assert check["n_non_generating"] == 0
    assert check["product_order_distribution"] == {
        "2": 168,
        "3": 336,
        "4": 336,
        "7": 336,
    }
    assert all(check["klein_relations"].values())


def test_x3_hurwitz_and_klein_quartic() -> None:
    """84(g-1) = 168 = 42(2g-2) exactly; the orbifold curvature -1/42; the
    Klein quartic smoothness certificate; genus 3."""
    check = hc.check_x3_triangle()
    assert check["hurwitz_bound_84_g_minus_1"] == 168
    assert check["riemann_hurwitz_42_2g_minus_2"] == 168
    assert check["class_equation_cross_check"] == 168
    assert check["orbifold_chi_numerator"] == -1
    assert check["orbifold_chi_denominator"] == 42
    smooth = check["klein_quartic_smoothness"]
    assert smooth["identity_27_xyz3"] is True
    assert smooth["contradiction_28"] is True
    assert smooth["coordinate_cases_trivial"] is True
    assert smooth["genus_of_smooth_quartic"] == 3


# ---------------------------------------------------------------------------
# X4 — the hyperbolic {7,3} figure
# ---------------------------------------------------------------------------


def test_x4_hyperbolic_identities_and_combinatorics() -> None:
    """The closed forms hold at 40 dps (the tolerance scales with the
    precision); the {7,3} combinatorial closure is exact."""
    check = hc.check_x4_hyperbolic(dps=40)
    assert check["identities_at_dps"] is True
    assert check["combinatorial_closure"] is True
    comb = check["combinatorics"]
    assert comb == {"V": 56, "E": 84, "F": 24, "genus": 3}
    lit = check["literals"]
    # cosh R = cosh(ell/2) * cosh r — the hyperbolic Pythagoras
    assert (
        abs(
            float(lit["cosh_circumradius"])
            - float(lit["cosh_half_edge"]) * float(lit["cosh_inradius"])
        )
        < 1e-12
    )


def test_x4_disk_witness_matches_closed_forms() -> None:
    """The Poincare-disk heptagon (angle 2pi/3, bisection) reproduces the
    closed-form circumradius and edge to 1e-9 — two independent routes,
    one number."""
    check = hc.check_x4_hyperbolic(dps=30)
    witness = check["disk_witness"]
    assert 0.29 < witness["t_vertex"] < 0.32
    assert abs(witness["angle_numeric"] - 2.0943951023931953) < 1e-9
    assert check["witness_circumradius_error"] <= hc.X_TOLERANCES["hyper_witness"]
    assert check["witness_edge_error"] <= hc.X_TOLERANCES["hyper_witness"]


# ---------------------------------------------------------------------------
# X5 — the integrator certification
# ---------------------------------------------------------------------------


def test_x5_measured_orders_and_reversibility() -> None:
    """The regression orders: 2 (leapfrog), 4 (Yoshida); forward+backward
    recovers the state to roundoff for both integrators."""
    check = hc.check_x5_integrator(leap_grid=(400, 800), yosh_grid=(150, 300))
    conv = check["convergence"]
    assert abs(conv["leapfrog_slope"] - 2.0) <= hc.X_TOLERANCES["slope_leapfrog"]
    assert abs(conv["yoshida_slope"] - 4.0) <= hc.X_TOLERANCES["slope_yoshida"]
    assert check["reversibility"]["leapfrog"] <= hc.X_TOLERANCES["reversal"]
    assert check["reversibility"]["yoshida4"] <= hc.X_TOLERANCES["reversal"]


def test_x5_bounded_energy_and_two_body_invariants() -> None:
    """No secular energy trend for the symplectic integrators (ratio <= 0.1)
    against the RK4 control (ratio ~ 1); LRL, vis-viva and the orbit
    equation hold along the Yoshida orbit."""
    check = hc.check_x5_integrator(
        leap_grid=(400, 800),
        yosh_grid=(150, 300),
        bounded_periods=30,
        bounded_spp=120,
        inv_spp=8000,
        inv_revolutions=4,
    )
    env = check["energy_envelopes"]
    assert env["leapfrog"]["secular_trend_ratio"] <= hc.X_TOLERANCES["trend_ratio"]
    assert env["yoshida4"]["secular_trend_ratio"] <= hc.X_TOLERANCES["trend_ratio"]
    assert env["rk4_control"]["secular_trend_ratio"] > 0.5
    inv = check["two_body_invariants"]
    assert inv["lrl_drift"] <= hc.X_TOLERANCES["lrl_drift"]
    assert float(inv["vis_viva_relative"]) <= hc.X_TOLERANCES["vis_viva"]
    assert inv["orbit_equation_relative"] <= hc.X_TOLERANCES["orbit_equation"]


# ---------------------------------------------------------------------------
# X6 — the GR bridge
# ---------------------------------------------------------------------------


def test_x6_mercury_textbook_anchor() -> None:
    """Mercury: the measured 1PN advance matches the closed form; the
    Newtonian control advances at integrator zero; the arcsec/century
    hits the textbook 42.98."""
    from planetvortex import classical as cl

    mercury = next(p for p in cl.PLANETS if p.name == "Mercury")
    check = hc.check_x6_pn_perihelion(n_orbits=10, steps_per_orbit=1500, planets=("Mercury",))
    row = check["per_planet"][0]
    assert abs(row["measured_over_formula"] - 1.0) <= hc.X_TOLERANCES["pn_relative"]
    assert row["newtonian_control_rad_per_orbit"] <= hc.X_TOLERANCES["newtonian_advance"]
    assert abs(check["mercury_arcsec_per_century"] - 42.98) / 42.98 <= 1e-3
    assert mercury.a_au == row["a_au"]


def test_x6_formula_ladder_is_ordered() -> None:
    """The 8-planet precession ladder is strictly decreasing from Mercury
    (42.98) to Neptune (~0.0008) — the 1/a(1-e^2) hierarchy."""
    check = hc.check_x6_pn_perihelion(n_orbits=1, steps_per_orbit=100, planets=("Mercury",))
    ladder = [row["arcsec_per_century"] for row in check["formula_ladder_all_planets"]]
    assert ladder[0] == pytest.approx(42.98, abs=0.05)
    assert ladder == sorted(ladder, reverse=True)
    assert ladder[-1] < 0.005


# ---------------------------------------------------------------------------
# The committed X protocols
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("stage,slug", sorted(X_SLUGS.items()))
def test_committed_x_protocols_schema(stage: str, slug: str) -> None:
    """Every committed default X protocol carries the stable envelope."""
    path = os.path.join(PROTOCOL_DIR, f"{slug}_default.json")
    assert os.path.exists(path), path
    with open(path, encoding="utf-8") as fh:
        report = json.load(fh)
    assert report["suite"] == "planetvortex-hardcore"
    assert report["version"] == "2.0.0"
    assert report["stage"] == stage
    assert report["preset"] == "default"
    assert "date_utc" in report
    assert report["check"]["passed"] is True


def test_committed_x_protocol_headlines() -> None:
    """The committed numbers: the class equation, the (2,3,7) census, the
    disk witness and the Mercury anchor are pinned in the protocols."""
    with open(
        os.path.join(PROTOCOL_DIR, "X1_sl2_enumeration_default.json"), encoding="utf-8"
    ) as fh:
        x1 = json.load(fh)["check"]
    assert x1["conjugacy_class_sizes"] == [1, 21, 24, 24, 42, 56]
    with open(
        os.path.join(PROTOCOL_DIR, "X3_triangle_hurwitz_default.json"), encoding="utf-8"
    ) as fh:
        x3 = json.load(fh)["check"]
    assert x3["n_pairs_237"] == 336 and x3["n_non_generating"] == 0
    with open(
        os.path.join(PROTOCOL_DIR, "X4_hyperbolic_figure_default.json"), encoding="utf-8"
    ) as fh:
        x4 = json.load(fh)["check"]
    assert x4["witness_circumradius_error"] <= 1e-9
    with open(os.path.join(PROTOCOL_DIR, "X6_pn_perihelion_default.json"), encoding="utf-8") as fh:
        x6 = json.load(fh)["check"]
    assert abs(x6["mercury_arcsec_per_century"] - 42.98) < 0.05
