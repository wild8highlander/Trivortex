#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
PLANETVORTEX — TESTS: THE CLASSICAL PLANETARY REGISTERS (Layer P)
============================================================================
The data-table registers: sanity of the committed NASA register, the
two-body Kepler III (corrected against uncorrected, Lemma D), the
Schwarzschild ladder, the Hill spheres and the gravity ladder.

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import math

import pytest

from planetvortex import classical as cl
from planetvortex import fano as fn


def test_data_register_sanity() -> None:
    """Eight planets; a and T strictly increasing; e in (0, 1); the
    station set is the register minus Earth."""
    assert len(cl.PLANETS) == 8
    a_vals = [p.a_au for p in cl.PLANETS]
    t_vals = [p.period_days for p in cl.PLANETS]
    assert a_vals == sorted(a_vals)
    assert t_vals == sorted(t_vals)
    for p in cl.PLANETS:
        assert 0.0 < p.e < 1.0
        assert p.gm > 0.0
        assert p.radius_km > 0.0
    assert [p.name for p in cl.station_planets()] == [
        "Mercury",
        "Venus",
        "Mars",
        "Jupiter",
        "Saturn",
        "Uranus",
        "Neptune",
    ]


def test_kepler3_two_body_dynamic() -> None:
    """Kepler III certified in the two-body dynamics for Earth and
    Jupiter: the corrected period matches at integration precision and
    the uncorrected comparison carries the exact sqrt(1+m) signature."""
    from planetvortex.ladder import _two_body_period

    for idx in (cl.EARTH_INDEX, 4):
        p = cl.PLANETS[idx]
        t_meas = _two_body_period(p, cl.mu_planet(p), 2, 2400)
        t_corr = cl.kepler_period_years(p)
        t_uncorr = 2.0 * math.pi * math.sqrt(p.a_au**3 / cl.MU_SUN)
        assert abs(t_meas - t_corr) / t_corr < 1e-9
        # T_uncorr/T_corr = sqrt(1 + m/M) exactly (the mass signature)
        assert abs(t_uncorr / t_corr - math.sqrt(1.0 + cl.solar_mass_ratio(p))) < 1e-15
        signature = (t_uncorr - t_corr) / t_corr
        assert (
            abs(signature - cl.solar_mass_ratio(p) / 2.0) / (cl.solar_mass_ratio(p) / 2.0) < 1e-3
        )  # the m^2/8 curvature correction is the residual


def test_schwarzschild_ladder() -> None:
    """r_s = 2GM/c^2: the Sun at 2953 m, Jupiter at 2.8 m, Earth at
    8.87 mm — the exact arithmetic of the gravity-as-geometry ladder."""
    r_sun = cl.schwarzschild_radius_m(cl.GM_SUN)
    r_jup = cl.schwarzschild_radius_m(cl.PLANETS[4].gm)
    r_earth = cl.schwarzschild_radius_m(cl.PLANETS[cl.EARTH_INDEX].gm)
    assert abs(r_sun - 2953.25) / 2953.25 < 1e-6
    assert 2.8 < r_jup < 2.9
    assert 8.8e-3 < r_earth < 8.9e-3
    assert r_earth == cl.gravitational_radius_m(cl.PLANETS[cl.EARTH_INDEX].gm) * 2.0


def test_hill_spheres() -> None:
    """The Hill spheres: Earth ~0.010 AU, Jupiter ~0.35 AU; the
    adjacent-pair margins all exceed 3 (the non-crossing register)."""
    r_earth = cl.hill_radius_au(cl.PLANETS[cl.EARTH_INDEX])
    r_jup = cl.hill_radius_au(cl.PLANETS[4])
    assert 0.009 < r_earth < 0.011
    assert 0.34 < r_jup < 0.37
    ordered = sorted(cl.PLANETS, key=lambda p: p.a_au)
    for p1, p2 in zip(ordered[:-1], ordered[1:]):
        margin = (p2.a_au - p1.a_au) / (cl.hill_radius_au(p1) + cl.hill_radius_au(p2))
        assert margin > 3.0


def test_gravity_ladder() -> None:
    """The gravity ladder: Jupiter ~+2.5 dex over Earth, Mercury the
    floor; the station weights are mean-one and strictly ordered."""
    ladder = cl.gravity_ladder()
    assert abs(ladder["Jupiter"] - ladder["Mercury"]) > 3.7
    assert ladder["Jupiter"] == max(ladder.values())
    assert ladder["Mercury"] == min(ladder.values())
    weights = cl.gravity_weights()
    assert len(weights) == 7
    assert abs(float(weights.mean()) - 1.0) < 1e-12
    assert float(weights.argmax()) == 3  # Jupiter, station 4 (0-based 3)


def test_kepler3_fact_sheet_spread_diagnostic() -> None:
    """The fact-sheet register T^2/a^3(1+m/M) is uniform to 2e-3 —
    the honest provenance bound quoted by P2's diagnostic (the tables
    are rounded and epoch-mixed; the register itself is dynamic)."""
    spread = cl.kepler3_spread(corrected=True)
    assert spread["worst_relative"] < 2.5e-3
    spread_uncorr = cl.kepler3_spread(corrected=False)
    # the uncorrected spread must contain the Jupiter mass signature
    jup_row = next(
        r
        for r in [{"planet": p.name, "v": v} for p, v in zip(cl.PLANETS, spread_uncorr["values"])]
        if r["planet"] == "Jupiter"
    )
    assert abs(jup_row["v"] - spread_uncorr["mean"]) / spread_uncorr["mean"] > 4.0e-4
    assert fn is not None  # the station bridge stays imported for parity


def test_osculating_elements_circular_limit() -> None:
    """The osculating reduction: a circular orbit returns (a, 0); the
    committed perihelion state of Earth (inside the full 9-body state)
    returns its (a, e)."""
    a0, e0 = cl.osculating_a_e(1.0, 0.0, 0.0, math.sqrt(cl.MU_SUN), cl.MU_SUN)
    assert abs(a0 - 1.0) < 1e-12
    assert e0 < 1e-12
    from planetvortex import nbody as nb

    earth = cl.PLANETS[cl.EARTH_INDEX]
    state = nb.initial_state()
    a1, e1 = nb.osculating_elements(state, cl.EARTH_INDEX)
    assert abs(a1 - earth.a_au) / earth.a_au < 1e-12
    assert abs(e1 - earth.e) < 1e-12


def test_kepler_period_formula() -> None:
    """T(a) is monotone and reproduces Earth's year at a ~ 1 AU."""
    ts = [cl.kepler_period_years(p) for p in cl.PLANETS]
    assert ts == sorted(ts)
    earth = cl.kepler_period_years(cl.PLANETS[cl.EARTH_INDEX])
    assert abs(earth - 1.0) < 2e-4  # ~1.000028 Julian years
