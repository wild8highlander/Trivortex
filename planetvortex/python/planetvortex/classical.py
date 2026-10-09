#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
PLANETVORTEX — THE CLASSICAL PLANETARY REGISTERS (Layer P)
============================================================================
The data layer of the planetary bench: the NASA fact-sheet register of
the eight planets, the exact constants of the unit system, and the
classical gravity registers — Kepler's third law with its planetary-mass
correction, the Schwarzschild radius ladder, the Hill spheres and the
gravity (mass) ladder that feeds the PSL(2,7) figure.

Unit conventions
----------------
Lengths in AU (exact: 1 AU = 149 597 870 700 m), time in years, mass in
solar masses. In this unit system G*M_sun = 4*pi^2 exactly (the
definition of the astronomical unit system), so the two-body Kepler
constant is mu_i = 4*pi^2*(1 + m_i) for a planet of mass m_i.

Data provenance
---------------
GM, radii, surface gravities: NASA NSSDC planetary fact sheets
(https://nssdc.gsfc.nasa.gov/planetary/factsheet/); semi-major axes and
eccentricities: JPL Keplerian elements for approximate positions,
epoch J2000 (https://ssd.jpl.nasa.gov/planets/approx_pos.html).
Values are committed here verbatim — every register of the bench is
bound to this table.

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import math
from typing import Dict, List, NamedTuple, Tuple

import numpy as np

# ---------------------------------------------------------------------------
# The exact constants of the unit system (and the SI bridges)
# ---------------------------------------------------------------------------

AU_M = 149_597_870_700.0  # the astronomical unit, exact (IAU 2012)
C_LIGHT = 299_792_458.0  # the speed of light, exact (SI)
G_NEWTON = 6.67430e-11  # CODATA 2018 (masses from GM only)
GM_SUN = 1.32712440018e20  # NASA NSSDC Sun fact sheet, m^3/s^2
MU_SUN = 4.0 * math.pi * math.pi  # G*M_sun in AU^3/yr^2 — exact in units

TWO_PI = 2.0 * math.pi


class Planet(NamedTuple):
    """One row of the committed NASA register."""

    name: str
    gm: float  # G*M, m^3/s^2 (NASA NSSDC)
    radius_km: float  # equatorial radius, km (NASA NSSDC)
    a_au: float  # semi-major axis, AU (JPL J2000 mean elements)
    e: float  # orbital eccentricity (JPL J2000)
    period_days: float  # sidereal orbital period, days (NASA NSSDC)
    gravity_ms2: float  # equatorial surface gravity, m/s^2 (NASA NSSDC)


# The committed register — the single numeric oracle of Layer P.
PLANETS: Tuple[Planet, ...] = (
    Planet("Mercury", 2.2032e13, 2439.7, 0.38709927, 0.20563593, 87.9691, 3.70),
    Planet("Venus", 3.24859e14, 6051.8, 0.72333566, 0.00677672, 224.701, 8.87),
    Planet("Earth", 3.986004418e14, 6371.0, 1.00000261, 0.01671123, 365.256, 9.81),
    Planet("Mars", 4.282837e13, 3389.5, 1.52371034, 0.09339412, 686.980, 3.71),
    Planet("Jupiter", 1.26686534e17, 69911.0, 5.20288700, 0.04838624, 4332.589, 24.79),
    Planet("Saturn", 3.7931187e16, 58232.0, 9.53667594, 0.05386179, 10759.22, 10.44),
    Planet("Uranus", 5.793939e15, 25362.0, 19.18916464, 0.04725744, 30688.5, 8.87),
    Planet("Neptune", 6.836529e16, 24622.0, 30.06992276, 0.00859048, 60182.0, 11.15),
)

EARTH_INDEX = 2

PLANET_NAMES: Tuple[str, ...] = tuple(p.name for p in PLANETS)


# ---------------------------------------------------------------------------
# Mass, Kepler and gravity registers (all analytic, all from the table)
# ---------------------------------------------------------------------------


def solar_mass_ratio(planet: Planet) -> float:
    """m_i / M_sun — the planetary mass in solar units (from GM)."""
    return planet.gm / GM_SUN


def mu_planet(planet: Planet) -> float:
    """mu_i = 4*pi^2*(1 + m_i/M_sun) — the two-body constant, AU^3/yr^2."""
    return MU_SUN * (1.0 + solar_mass_ratio(planet))


def kepler_period_years(planet: Planet) -> float:
    """T = 2*pi*sqrt(a^3/mu_i) — the two-body Kepler period, Julian years.

    The period IMPLIED by the committed semi-major axis and the
    mass-corrected constant mu_i. The fact-sheet periods quoted in the
    table (period_days) are an independent, rounded, epoch-mixed
    register — stage P2 records their consistency honestly as a
    diagnostic and certifies Kepler III dynamically instead.
    """
    return TWO_PI * math.sqrt(planet.a_au**3 / mu_planet(planet))


def kepler3_corrected(planet: Planet) -> float:
    """T^2/a^3 * (1 + m_i/M_sun) — the mass-corrected Kepler register.

    Lemma D: n^2 a^3 = G*M_sun*(1 + m_i) exactly for the two-body problem,
    so this quantity is the SAME constant 4*pi^2/GM_sun for every planet.
    In AU-years units the constant is exactly 1 (by construction), which
    makes the register a pure dimensionless spread measurement.
    """
    t_yr = planet.period_days / 365.25
    return t_yr * t_yr / planet.a_au**3 * (1.0 + solar_mass_ratio(planet))


def kepler3_uncorrected(planet: Planet) -> float:
    """T^2/a^3 without the mass correction — the naive register."""
    t_yr = planet.period_days / 365.25
    return t_yr * t_yr / planet.a_au**3


def kepler3_spread(corrected: bool = True) -> Dict[str, float]:
    """The worst pairwise relative spread of the Kepler register.

    Returns the mean, the worst pairwise relative deviation and the
    offending planet names. This is the recorded payload of stage P2.
    """
    vals = (
        [kepler3_corrected(p) for p in PLANETS]
        if corrected
        else [kepler3_uncorrected(p) for p in PLANETS]
    )
    mean = sum(vals) / len(vals)
    worst = 0.0
    worst_pair = ("", "")
    for i, vi in enumerate(vals):
        for j, vj in enumerate(vals):
            rel = abs(vi - vj) / mean
            if rel > worst:
                worst = rel
                worst_pair = (PLANET_NAMES[i], PLANET_NAMES[j])
    return {
        "mean": mean,
        "worst_relative": worst,
        "worst_pair": worst_pair,
        "values": vals,
    }


def schwarzschild_radius_m(gm_si: float) -> float:
    """r_s = 2*G*M/c^2 — the gravitational (Schwarzschild) radius, metres."""
    return 2.0 * gm_si / (C_LIGHT * C_LIGHT)


def gravitational_radius_m(gm_si: float) -> float:
    """r_g = G*M/c^2 — half the Schwarzschild radius, metres."""
    return gm_si / (C_LIGHT * C_LIGHT)


def hill_radius_au(planet: Planet) -> float:
    """r_H = a*(m_i/(3*M_sun))^(1/3) — the Hill sphere, AU."""
    return planet.a_au * (solar_mass_ratio(planet) / 3.0) ** (1.0 / 3.0)


def mean_motion_rad_per_day(planet: Planet) -> float:
    """n_i = 2*pi/T_i — the mean motion, rad/day."""
    return TWO_PI / planet.period_days


# ---------------------------------------------------------------------------
# The gravity ladder — the numeric payload the figure carries
# ---------------------------------------------------------------------------


def gravity_ladder() -> Dict[str, float]:
    """delta_i = log10(GM_i / GM_Earth) for all eight planets.

    The gravity ladder of the solar system: Jupiter stands +2.53 dex
    above Earth, Mercury -1.09 dex below. The ladder is the numeric
    payload carried by the stations of the PSL(2,7) figure (Lemma E).
    """
    gm_earth = PLANETS[EARTH_INDEX].gm
    return {p.name: math.log10(p.gm / gm_earth) for p in PLANETS}


def station_planets() -> Tuple[Planet, ...]:
    """The seven stations of the figure, in orbital-period order.

    The figure is the geocentric septad: the seven wandering planets of
    the Earth observer. Earth itself is the vantage point (the origin of
    the frame) and does not occupy a vertex; the Sun occupies the centre.
    """
    return tuple(p for p in PLANETS if p.name != "Earth")


def gravity_weights() -> np.ndarray:
    """The circulation weights w_i, mean-normalized to 1.

    w_i is built from the gravity ladder: w_i ~ 10^(delta_i - mean(delta)),
    renormalized so that mean(w) = 1 exactly. Mercury carries ~0.07 of the
    mean circulation, Jupiter ~25 — the honest mass-ladder spread.
    """
    stations = station_planets()
    deltas = np.array([gravity_ladder()[p.name] for p in stations])
    raw = 10.0 ** (deltas - deltas.mean())
    return 7.0 * raw / raw.sum()


# ---------------------------------------------------------------------------
# Osculating elements of the heliocentric two-body problem (for the N-body)
# ---------------------------------------------------------------------------


def osculating_a_e(rx: float, ry: float, vx: float, vy: float, mu: float) -> Tuple[float, float]:
    """Semi-major axis and eccentricity from a planar relative state.

    mu = G*(M_sun + m_i) in the working units; the state is
    heliocentric (r, v = v_planet - v_sun). Classical vis-viva +
    eccentricity vector, planar reduction.
    """
    r = math.hypot(rx, ry)
    v2 = vx * vx + vy * vy
    energy = 0.5 * v2 - mu / r
    a = -mu / (2.0 * energy)
    rv = rx * vx + ry * vy
    ex = ((v2 - mu / r) * rx - rv * vx) / mu
    ey = ((v2 - mu / r) * ry - rv * vy) / mu
    return a, math.hypot(ex, ey)


def au_of(metres: float) -> float:
    """Metres to AU (the exact IAU metre definition)."""
    return metres / AU_M


# ---------------------------------------------------------------------------
# The V1 spatial register: inclinations and nodes (J2000, JPL approx_pos)
# and the dwarf-planet rows (NASA NSSDC / JPL SBDB)
# ---------------------------------------------------------------------------


class SpatialRegister(NamedTuple):
    """One row of the V1 inclination register (degrees, JPL J2000)."""

    name: str
    inclination_deg: float  # i — the orbital tilt against the ecliptic
    node_deg: float  # Omega — the longitude of the ascending node


# The committed inclination register of the eight planets. Earth's
# inclination is 0 by definition (the ecliptic IS Earth's plane); the
# JPL value -0.00001531 deg is the reduced element of the Earth-Moon
# barycentre against the J2000 ecliptic.
SPATIAL_REGISTER: Tuple[SpatialRegister, ...] = (
    SpatialRegister("Mercury", 7.00497902, 48.33076593),
    SpatialRegister("Venus", 3.39467605, 76.67984255),
    SpatialRegister("Earth", 0.00001531, -11.26064),
    SpatialRegister("Mars", 1.84969142, 49.55953891),
    SpatialRegister("Jupiter", 1.30439695, 100.47390909),
    SpatialRegister("Saturn", 2.48599187, 113.66242448),
    SpatialRegister("Uranus", 0.77263783, 74.01692503),
    SpatialRegister("Neptune", 1.77004347, 131.78422574),
)

# The three registered dwarfs: GM (m^3/s^2), radii (km), the Keplerian
# rows and the spatial register — the 12-body gravimetric set of stage
# V2 (Sun + 8 planets + Ceres + Pluto + Eris).
DWARFS: Tuple[Planet, ...] = (
    Planet("Ceres", 6.26325e10, 469.7, 2.76750591, 0.07602493, 1681.6, 0.27),
    Planet("Pluto", 8.696e11, 1188.3, 39.48211675, 0.24882730, 90560.0, 0.62),
    Planet("Eris", 1.108e12, 1163.0, 67.864, 0.43607, 203830.0, 0.82),
)

DWARF_SPATIAL: Tuple[SpatialRegister, ...] = (
    SpatialRegister("Ceres", 10.5876, 80.393),
    SpatialRegister("Pluto", 17.14001206, 110.30393684),
    SpatialRegister("Eris", 44.040, 35.951),
)


def spatial_register_by_name(name: str) -> SpatialRegister:
    """The inclination register row of one body (planets + dwarfs)."""
    for row in SPATIAL_REGISTER + DWARF_SPATIAL:
        if row.name == name:
            return row
    raise KeyError(f"no spatial register row for {name!r}")


def all_bodies_with_spatial() -> Tuple[Planet, ...]:
    """The 8 planets + 3 dwarfs — the wandering set of stage V1."""
    return PLANETS + DWARFS
