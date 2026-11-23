#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — сборка data/catalog.json (200+ объектов).

Стратегия:
  1) STATIC_CORE — верифицированное статическое ядро (Солнечная система, луны,
     астероиды, кометы, ближайшие звёзды, абстрактные тела лаборатории).
     Работает без сети; источники — NASA NSSDC Planetary Fact Sheets,
     HEASARC, RECONS/SIMBAD.
  2) TAP-снимок NASA Exoplanet Archive (таблица ps, default_flag=1),
     ближайшие N экзопланет; кэшируется в data/cache/exoplanets_<date>.json.

Запуск:  python3 tools/build_catalog.py [--limit 160] [--offline]
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import os
import sys
import time
import urllib.request
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
CACHE = os.path.join(DATA, "cache")

TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
M_EARTH_KG = 5.9722e24
R_EARTH_KM = 6371.0
AU_KM = 1.495978707e8

NSSDC = "https://nssdc.gsfc.nasa.gov/planetary/factsheet/"
NSSDC_AST = "https://nssdc.gsfc.nasa.gov/planetary/factsheet/asteroidfact.html"
NSSDC_COMET = "https://nssdc.gsfc.nasa.gov/planetary/factsheet/cometfact.html"
NASA_SCI = "https://science.nasa.gov/"
SIMBAD = "https://simbad.cds.unistra.fr/simbad/"
EXOARCH = "https://exoplanetarchive.ipac.caltech.edu/"


def _star(name, mass_kg, radius_km, sptype, dist_ly, color, source=SIMBAD, note=""):
    return dict(
        id=name.lower().replace(" ", "_").replace("α", "alpha"),
        name=name,
        type="star",
        mass_kg=mass_kg,
        radius_km=radius_km,
        orbit_au=None,
        color=color,
        source=source,
        metadata=(
            {"spectral_type": sptype, "distance_ly": dist_ly, "note": note}
            if note
            else {"spectral_type": sptype, "distance_ly": dist_ly}
        ),
    )


def _body(
    id_,
    name,
    type_,
    mass,
    radius,
    orbit_au=None,
    color="#9AA6B2",
    source=NSSDC,
    parent=None,
    orbit_km=None,
    est=False,
    **meta,
):
    rec = dict(
        id=id_,
        name=name,
        type=type_,
        mass_kg=mass,
        radius_km=radius,
        orbit_au=orbit_au,
        color=color,
        source=source,
    )
    if parent is not None:
        rec["parent"] = parent
        rec["orbit_km"] = orbit_km
    if est:
        rec["mass_estimated"] = True
    if meta:
        rec["metadata"] = meta
    return rec


# ═══════════════════════════════════════════════════════════════════════════
# СТАТИЧЕСКОЕ ЯДРО КАТАЛОГА (значения из NASA NSSDC Fact Sheets и SIMBAD)
# ═══════════════════════════════════════════════════════════════════════════
def static_core() -> list[dict]:
    R = []

    # ── Солнце ──
    R.append(
        _body(
            "sun",
            "Sun",
            "star",
            1.9884e30,
            695700.0,
            color="#FDB813",
            source="https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html",
            spectral_type="G2V",
        )
    )

    # ── 8 планет (NSSDC Planetary Fact Sheet) ──
    R += [
        _body("mercury", "Mercury", "planet", 3.301e23, 2439.7, 0.387, "#8C8C8C"),
        _body("venus", "Venus", "planet", 4.867e24, 6051.8, 0.723, "#E6C27A"),
        _body("earth", "Earth", "planet", 5.9722e24, 6371.0, 1.000, "#4FD1C5"),
        _body("mars", "Mars", "planet", 6.417e23, 3389.5, 1.524, "#C1440E"),
        _body("jupiter", "Jupiter", "planet", 1.898e27, 69911.0, 5.203, "#D8A47F"),
        _body("saturn", "Saturn", "planet", 5.683e26, 58232.0, 9.537, "#E3C98F"),
        _body("uranus", "Uranus", "planet", 8.681e25, 25362.0, 19.191, "#A5E3E0"),
        _body("neptune", "Neptune", "planet", 1.024e26, 24622.0, 30.069, "#4B70DD"),
    ]

    # ── Карликовые планеты ──
    R += [
        _body(
            "pluto",
            "Pluto",
            "dwarf_planet",
            1.303e22,
            1188.3,
            39.482,
            "#C9B8A0",
            source="https://nssdc.gsfc.nasa.gov/planetary/factsheet/plutofact.html",
        ),
        _body(
            "ceres", "Ceres", "dwarf_planet", 9.383e20, 473.0, 2.766, "#8A8A8A", source=NSSDC_AST
        ),
        _body(
            "eris",
            "Eris",
            "dwarf_planet",
            1.66e22,
            1163.0,
            67.78,
            "#D3D3D3",
            source=NASA_SCI + "dwarf-planets/eris/",
        ),
        _body(
            "haumea",
            "Haumea",
            "dwarf_planet",
            4.006e21,
            780.0,
            43.13,
            "#E0E0E0",
            source=NASA_SCI + "dwarf-planets/haumea/",
            est=True,
        ),
        _body(
            "makemake",
            "Makemake",
            "dwarf_planet",
            3.1e21,
            715.0,
            45.43,
            "#C0C0C0",
            source=NASA_SCI + "dwarf-planets/makemake/",
            est=True,
        ),
    ]

    # ── Луны: Земля, Марс, Юпитер, Сатурн, Уран, Нептун, Плутон ──
    SAT_SRC = "https://nssdc.gsfc.nasa.gov/planetary/factsheet/saturniansatfact.html"
    URA_SRC = "https://nssdc.gsfc.nasa.gov/planetary/factsheet/uraniansatfact.html"
    JUP_SRC = "https://nssdc.gsfc.nasa.gov/planetary/factsheet/galileanfact_table.html"
    R += [
        _body(
            "moon", "Moon", "moon", 7.342e22, 1737.5, "#B0B0B0", parent="earth", orbit_km=384400.0
        ),
        _body(
            "phobos",
            "Phobos",
            "moon",
            1.0659e16,
            11.27,
            "#7A6A5A",
            parent="mars",
            orbit_km=9376.0,
            source=NSSDC,
            est=True,
        ),
        _body(
            "deimos",
            "Deimos",
            "moon",
            1.4762e15,
            6.2,
            "#8A7A6A",
            parent="mars",
            orbit_km=23463.0,
            source=NSSDC,
            est=True,
        ),
        # галилеевы луны
        _body(
            "io",
            "Io",
            "moon",
            8.932e22,
            1821.6,
            "#F0D040",
            parent="jupiter",
            orbit_km=421700.0,
            source=JUP_SRC,
        ),
        _body(
            "europa",
            "Europa",
            "moon",
            4.8e22,
            1560.8,
            "#D9C7B8",
            parent="jupiter",
            orbit_km=671100.0,
            source=JUP_SRC,
        ),
        _body(
            "ganymede",
            "Ganymede",
            "moon",
            1.4819e23,
            2634.1,
            "#A89F91",
            parent="jupiter",
            orbit_km=1070400.0,
            source=JUP_SRC,
        ),
        _body(
            "callisto",
            "Callisto",
            "moon",
            1.0759e23,
            2410.3,
            "#7A6E5D",
            parent="jupiter",
            orbit_km=1882700.0,
            source=JUP_SRC,
        ),
        _body(
            "amalthea",
            "Amalthea",
            "moon",
            2.08e18,
            83.5,
            "#906040",
            parent="jupiter",
            orbit_km=181400.0,
            source=JUP_SRC,
            est=True,
        ),
        _body(
            "himalia",
            "Himalia",
            "moon",
            4.2e18,
            69.8,
            "#706050",
            parent="jupiter",
            orbit_km=11460000.0,
            source=JUP_SRC,
            est=True,
        ),
        # спутники Сатурна
        _body(
            "mimas",
            "Mimas",
            "moon",
            3.749e19,
            198.2,
            "#B8B8B8",
            parent="saturn",
            orbit_km=185540.0,
            source=SAT_SRC,
        ),
        _body(
            "enceladus",
            "Enceladus",
            "moon",
            1.0802e20,
            252.1,
            "#E8F0F0",
            parent="saturn",
            orbit_km=238040.0,
            source=SAT_SRC,
        ),
        _body(
            "tethys",
            "Tethys",
            "moon",
            6.174e20,
            531.1,
            "#D0D0D0",
            parent="saturn",
            orbit_km=294670.0,
            source=SAT_SRC,
        ),
        _body(
            "dione",
            "Dione",
            "moon",
            1.0955e21,
            561.4,
            "#C8C8C8",
            parent="saturn",
            orbit_km=377420.0,
            source=SAT_SRC,
        ),
        _body(
            "rhea",
            "Rhea",
            "moon",
            2.3065e21,
            763.8,
            "#D8D8D8",
            parent="saturn",
            orbit_km=527070.0,
            source=SAT_SRC,
        ),
        _body(
            "titan",
            "Titan",
            "moon",
            1.3452e23,
            2574.7,
            "#E0A040",
            parent="saturn",
            orbit_km=1221870.0,
            source=SAT_SRC,
        ),
        _body(
            "hyperion",
            "Hyperion",
            "moon",
            5.62e18,
            135.0,
            "#B0A090",
            parent="saturn",
            orbit_km=1501000.0,
            source=SAT_SRC,
            est=True,
        ),
        _body(
            "iapetus",
            "Iapetus",
            "moon",
            1.8056e21,
            734.5,
            "#A0A0A0",
            parent="saturn",
            orbit_km=3560800.0,
            source=SAT_SRC,
        ),
        _body(
            "phoebe",
            "Phoebe",
            "moon",
            8.29e18,
            106.5,
            "#605858",
            parent="saturn",
            orbit_km=12947780.0,
            source=SAT_SRC,
            est=True,
        ),
        # спутники Урана
        _body(
            "miranda",
            "Miranda",
            "moon",
            6.59e19,
            235.8,
            "#B8C0C0",
            parent="uranus",
            orbit_km=129390.0,
            source=URA_SRC,
        ),
        _body(
            "ariel",
            "Ariel",
            "moon",
            1.353e21,
            578.9,
            "#D0D0D0",
            parent="uranus",
            orbit_km=190900.0,
            source=URA_SRC,
        ),
        _body(
            "umbriel",
            "Umbriel",
            "moon",
            1.172e21,
            584.7,
            "#A8A8A8",
            parent="uranus",
            orbit_km=266000.0,
            source=URA_SRC,
        ),
        _body(
            "titania",
            "Titania",
            "moon",
            3.527e21,
            788.9,
            "#C0C0C0",
            parent="uranus",
            orbit_km=436300.0,
            source=URA_SRC,
        ),
        _body(
            "oberon",
            "Oberon",
            "moon",
            3.014e21,
            761.4,
            "#B0B0B0",
            parent="uranus",
            orbit_km=583500.0,
            source=URA_SRC,
        ),
        # Нептун и Плутон
        _body(
            "triton",
            "Triton",
            "moon",
            2.139e22,
            1353.4,
            "#C8D8D8",
            parent="neptune",
            orbit_km=354759.0,
            source=JUP_SRC,
        ),
        _body(
            "proteus",
            "Proteus",
            "moon",
            4.4e19,
            210.0,
            "#707878",
            parent="neptune",
            orbit_km=117646.0,
            source=NSSDC,
            est=True,
        ),
        _body(
            "nereid",
            "Nereid",
            "moon",
            3.1e19,
            170.0,
            "#888E8E",
            parent="neptune",
            orbit_km=5513400.0,
            source=NSSDC,
            est=True,
        ),
        _body(
            "charon",
            "Charon",
            "moon",
            1.586e21,
            606.0,
            "#A0A8B0",
            parent="pluto",
            orbit_km=19591.0,
            source="https://nssdc.gsfc.nasa.gov/planetary/factsheet/plutofact.html",
        ),
        _body(
            "nix",
            "Nix",
            "moon",
            4.5e16,
            19.5,
            "#B8B8B8",
            parent="pluto",
            orbit_km=48694.0,
            source=NSSDC,
            est=True,
        ),
        _body(
            "hydra",
            "Hydra",
            "moon",
            4.8e16,
            20.5,
            "#B0B8B8",
            parent="pluto",
            orbit_km=64738.0,
            source=NSSDC,
            est=True,
        ),
    ]

    # ── Астероиды (NSSDC Asteroid Fact Sheet + JPL SBDB) ──
    JPL = "https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html"
    R += [
        _body("vesta", "4 Vesta", "asteroid", 2.59076e20, 262.7, 2.362, "#A09080", NSSDC_AST),
        _body(
            "pallas", "2 Pallas", "asteroid", 2.04e20, 256.0, 2.773, "#909090", NSSDC_AST, est=True
        ),
        _body("juno", "3 Juno", "asteroid", 2.0e19, 123.0, 2.670, "#808080", NSSDC_AST, est=True),
        _body(
            "lutetia", "21 Lutetia", "asteroid", 1.7e18, 62.0, 2.435, "#707070", NSSDC_AST, est=True
        ),
        _body("eros", "433 Eros", "asteroid", 6.69e18, 8.4, 1.458, "#B0A090", NSSDC_AST, est=True),
        _body(
            "icarus", "1566 Icarus", "asteroid", 1.0e12, 0.7, 1.078, "#606060", NSSDC_AST, est=True
        ),
        _body(
            "geographos",
            "1620 Geographos",
            "asteroid",
            4.0e12,
            1.0,
            1.245,
            "#505050",
            NSSDC_AST,
            est=True,
        ),
        _body(
            "apollo", "1862 Apollo", "asteroid", 2.0e12, 0.8, 1.470, "#585858", NSSDC_AST, est=True
        ),
        _body(
            "mathilde",
            "253 Mathilde",
            "asteroid",
            1.033e20,
            26.5,
            2.647,
            "#404040",
            NSSDC_AST,
            est=True,
        ),
        _body("ida", "243 Ida", "asteroid", 4.2e16, 15.7, 2.861, "#686868", NSSDC_AST, est=True),
        _body("gaspra", "951 Gaspra", "asteroid", 1.0e16, 6.1, 2.210, "#757068", JPL, est=True),
        _body("hygiea", "10 Hygiea", "asteroid", 8.7e19, 217.0, 3.139, "#6A6A6A", JPL, est=True),
        _body(
            "interamnia",
            "704 Interamnia",
            "asteroid",
            3.9e19,
            166.0,
            3.062,
            "#666A6A",
            JPL,
            est=True,
        ),
        _body("davida", "511 Davida", "asteroid", 3.8e19, 156.0, 3.174, "#6A6A72", JPL, est=True),
        _body("eunomia", "15 Eunomia", "asteroid", 3.1e19, 128.0, 2.644, "#70746E", JPL, est=True),
        _body("psyche", "16 Psyche", "asteroid", 2.3e19, 111.0, 2.923, "#8A8E96", JPL, est=True),
        _body("sylvia", "87 Sylvia", "asteroid", 1.5e19, 131.0, 3.490, "#767A80", JPL, est=True),
        _body("hebe", "6 Hebe", "asteroid", 1.3e19, 95.0, 2.425, "#7C7C78", JPL, est=True),
        _body("iris", "7 Iris", "asteroid", 1.3e19, 100.0, 2.386, "#9A9A94", JPL, est=True),
        _body("flora", "8 Flora", "asteroid", 5.0e18, 68.0, 2.202, "#8E8A80", JPL, est=True),
    ]

    # ── Кометы (NSSDC Comet Fact Sheet; массы ядер — литературные оценки) ──
    R += [
        _body(
            "halley",
            "1P/Halley",
            "comet",
            2.2e14,
            5.5,
            17.834,
            "#88CCFF",
            NSSDC_COMET,
            est=True,
            period_years=75.32,
        ),
        _body(
            "encke",
            "2P/Encke",
            "comet",
            7.9e13,
            2.4,
            2.215,
            "#99DDFF",
            NSSDC_COMET,
            est=True,
            period_years=3.30,
        ),
        _body(
            "tempel1",
            "9P/Tempel 1",
            "comet",
            7.9e13,
            3.0,
            3.145,
            "#AADDFF",
            NSSDC_COMET,
            est=True,
            period_years=5.52,
        ),
        _body(
            "churyumov",
            "67P/Churyumov-Gerasimenko",
            "comet",
            9.982e12,
            2.0,
            3.463,
            "#BBDDFF",
            NSSDC_COMET,
            est=True,
            period_years=6.44,
        ),
        _body(
            "wirtanen",
            "46P/Wirtanen",
            "comet",
            1.0e14,
            0.6,
            3.093,
            "#CCDDEE",
            NSSDC_COMET,
            est=True,
            period_years=5.44,
        ),
        _body(
            "hale-bopp",
            "C/1995 O1 Hale-Bopp",
            "comet",
            1.3e16,
            30.0,
            186.0,
            "#B0E0FF",
            NSSDC_COMET,
            est=True,
            period_years=2533.0,
        ),
        _body(
            "hyakutake",
            "C/1996 B2 Hyakutake",
            "comet",
            8.0e13,
            2.0,
            700.0,
            "#A0D8FF",
            NSSDC_COMET,
            est=True,
            period_years=70000.0,
        ),
        _body(
            "swift-tuttle",
            "109P/Swift-Tuttle",
            "comet",
            1.0e14,
            13.0,
            26.09,
            "#C0C8FF",
            NSSDC_COMET,
            est=True,
            period_years=133.28,
        ),
        _body(
            "borrelly",
            "19P/Borrelly",
            "comet",
            2.2e13,
            2.4,
            3.612,
            "#B8D0F0",
            NSSDC_COMET,
            est=True,
            period_years=6.85,
        ),
        _body(
            "wild2",
            "81P/Wild 2",
            "comet",
            2.3e13,
            2.7,
            3.439,
            "#C8D8F8",
            NSSDC_COMET,
            est=True,
            period_years=6.40,
        ),
    ]

    # ── Ближайшие звёзды (SIMBAD / RECONS) ──
    R += [
        _star("Proxima Centauri", 2.446e29, 107300.0, "M5.5V", 4.246, "#FF8C6A"),
        _star("Alpha Centauri A", 2.188e30, 851200.0, "G2V", 4.365, "#FFF4E8"),
        _star("Alpha Centauri B", 1.801e30, 602300.0, "K1V", 4.365, "#FFD9A0"),
        _star("Barnard's Star", 3.128e29, 136400.0, "M4V", 5.963, "#FF9A76"),
        _star("Wolf 359", 1.577e29, 94000.0, "M6V", 7.856, "#FF7B5C"),
        _star("Lalande 21185", 5.263e29, 174100.0, "M2V", 8.307, "#FFA87E"),
        _star("Sirius A", 4.053e30, 1191600.0, "A1V", 8.659, "#EDF3FF"),
        _star("Sirius B", 2.048e30, 5850.0, "DA2", 8.659, "#DDE6F5"),
        _star("Luyten 726-8 A", 2.146e29, 101300.0, "M5.5V", 8.73, "#FF8866"),
        _star("Ross 154", 3.392e29, 118900.0, "M3.5V", 9.71, "#FF9470"),
        _star("Ross 128", 2.861e29, 104000.0, "M4V", 11.01, "#FF9775"),
        _star("Epsilon Eridani", 1.618e30, 466300.0, "K2V", 10.47, "#FFD9A6"),
        _star("Tau Ceti", 1.535e30, 509400.0, "G8V", 11.9, "#FFF0D6"),
        _star("Procyon A", 3.201e30, 1.3566e6, "F5IV-V", 11.46, "#F5F8FF"),
        _star("61 Cygni A", 1.253e30, 438400.0, "K5V", 11.4, "#FFCC8E"),
    ]

    # ── Абстрактные тела лаборатории (synthetic) ──
    SYN = "synthetic"
    R += [
        _body("equal_mass_1", "Equal mass I", "synthetic", 1.0e22, 500.0, None, "#4FD1C5", SYN),
        _body("equal_mass_2", "Equal mass II", "synthetic", 1.0e22, 500.0, None, "#4FD1C5", SYN),
        _body("equal_mass_3", "Equal mass III", "synthetic", 1.0e22, 500.0, None, "#4FD1C5", SYN),
        _body("equal_mass_4", "Equal mass IV", "synthetic", 1.0e22, 500.0, None, "#7DD3FC", SYN),
        _body("equal_mass_5", "Equal mass V", "synthetic", 1.0e22, 500.0, None, "#7DD3FC", SYN),
        _body(
            "vortex_trio_a",
            "Vortex trio A (Γ=+1)",
            "synthetic",
            1.0,
            1.0,
            None,
            "#A78BFA",
            SYN,
            circulation=1.0,
        ),
        _body(
            "vortex_trio_b",
            "Vortex trio B (Γ=+1)",
            "synthetic",
            1.0,
            1.0,
            None,
            "#A78BFA",
            SYN,
            circulation=1.0,
        ),
        _body(
            "vortex_trio_c",
            "Vortex trio C (Γ=+1)",
            "synthetic",
            1.0,
            1.0,
            None,
            "#A78BFA",
            SYN,
            circulation=1.0,
        ),
        _body("test_particle_1", "Test particle I", "synthetic", 1.0e3, 0.1, None, "#E8C766", SYN),
        _body("test_particle_2", "Test particle II", "synthetic", 1.0e3, 0.1, None, "#E8C766", SYN),
    ]
    return R


# ═══════════════════════════════════════════════════════════════════════════
# TAP-слой
# ═══════════════════════════════════════════════════════════════════════════
def _tap_cache_path() -> str:
    stamp = _dt.date.today().isoformat()
    return os.path.join(CACHE, f"exoplanets_{stamp}.json")


def fetch_exoplanets(limit: int = 160, timeout: float = 30.0) -> list[dict]:
    """TAP-запрос к NASA Exoplanet Archive с суточным кэшем."""
    os.makedirs(CACHE, exist_ok=True)
    cache = _tap_cache_path()
    if os.path.exists(cache):
        with open(cache, encoding="utf-8") as fh:
            return json.load(fh)
    query = (
        "select+pl_name,hostname,sy_dist,pl_rade,pl_bmasse,pl_orbsmax,"
        "pl_orbper,disc_year,discoverymethod,st_mass,st_rad+from+ps+"
        "where+default_flag=1+order+by+sy_dist+asc"
    )
    url = f"{TAP_URL}?query={query}&format=json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "trivortex-master/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            rows = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:  # сеть недоступна — работаем на старых снимках
        fallback = sorted(
            (f for f in os.listdir(CACHE) if f.startswith("exoplanets_") and f.endswith(".json")),
            reverse=True,
        )
        if fallback:
            with open(os.path.join(CACHE, fallback[0]), encoding="utf-8") as fh:
                return json.load(fh)
        print(f"[build_catalog] TAP недоступен ({exc}); каталог без экзопланет", file=sys.stderr)
        return []
    with open(cache, "w", encoding="utf-8") as fh:
        json.dump(rows, fh, ensure_ascii=False)
    return rows


def exoplanets_to_records(rows: list[dict], limit: int = 160) -> list[dict]:
    """Трансляция TAP-строк в записи каталога."""
    out, seen = [], set()
    taken = 0
    for row in rows:
        if taken >= limit:
            break
        name = row.get("pl_name") or ""
        if not name or name in seen:
            continue
        # масса: приоритет pl_bmasse, иначе прикидка по радиусу (плотность Земли)
        mass_e = row.get("pl_bmasse")
        rad_e = row.get("pl_rade")
        if mass_e is None and rad_e is None:
            continue
        est = False
        if mass_e is None:
            mass_e = (rad_e or 1.0) ** 3
            est = True
        if rad_e is None:
            rad_e = (mass_e or 1.0) ** (1.0 / 3.0)
        rec = dict(
            id="exo_"
            + name.lower().replace(" ", "_").replace("-", "_").replace("'", "").replace(".", ""),
            name=name,
            type="exoplanet",
            mass_kg=float(mass_e) * M_EARTH_KG,
            radius_km=float(rad_e) * R_EARTH_KM,
            orbit_au=float(row["pl_orbsmax"]) if row.get("pl_orbsmax") else None,
            color="#F4A988",
            source=EXOARCH,
        )
        if est:
            rec["mass_estimated"] = True
        meta = {}
        for key, dst in (
            ("hostname", "host_star"),
            ("sy_dist", "distance_pc"),
            ("pl_orbper", "period_days"),
            ("disc_year", "discovery_year"),
            ("discoverymethod", "discovery_method"),
            ("st_mass", "star_mass_solar"),
            ("st_rad", "star_radius_solar"),
        ):
            if row.get(key) is not None:
                meta[dst] = row[key]
        if meta:
            rec["metadata"] = meta
        seen.add(name)
        out.append(rec)
        taken += 1
    return out


# ═══════════════════════════════════════════════════════════════════════════
# Сборка и валидация
# ═══════════════════════════════════════════════════════════════════════════
def validate(records: list[dict]) -> list[str]:
    errors, ids = [], set()
    for i, rec in enumerate(records):
        rid = rec.get("id")
        if not rid:
            errors.append(f"[{i}] нет id")
            continue
        if rid in ids:
            errors.append(f"[{i}] дубликат id: {rid}")
        ids.add(rid)
        if not rec.get("name"):
            errors.append(f"[{rid}] нет name")
        if not rec.get("type"):
            errors.append(f"[{rid}] нет type")
        if not (rec.get("mass_kg", 0) > 0):
            errors.append(f"[{rid}] mass_kg <= 0")
        if not (rec.get("radius_km", 0) > 0):
            errors.append(f"[{rid}] radius_km <= 0")
        if not rec.get("source"):
            errors.append(f"[{rid}] нет source")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description="Сборка data/catalog.json")
    ap.add_argument(
        "--limit",
        type=int,
        default=160,
        help="сколько экзопланет брать из TAP (по возрастанию дистанции)",
    )
    ap.add_argument(
        "--offline",
        action="store_true",
        help="не ходить в сеть (только статическое ядро и старый кэш)",
    )
    args = ap.parse_args()

    records = static_core()
    n_static = len(records)
    if not args.offline:
        t0 = time.time()
        rows = fetch_exoplanets(limit=args.limit)
        exo = exoplanets_to_records(rows, args.limit)
        print(f"TAP: {len(exo)} экзопланет за {time.time()-t0:.1f} с")
        records += exo

    errors = validate(records)
    if errors:
        print("ОШИБКИ ВАЛИДАЦИИ:")
        for e in errors[:20]:
            print("  -", e)
        return 1

    os.makedirs(DATA, exist_ok=True)
    path = os.path.join(DATA, "catalog.json")
    payload = dict(
        version="1.0.0",
        generated=_dt.datetime.now().isoformat(timespec="seconds"),
        count=len(records),
        static_core=n_static,
        units=dict(
            mass="kg", radius="km", orbit_au="astronomical units", orbit_km="km from parent body"
        ),
        objects=records,
    )
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)

    types = {}
    for r in records:
        types[r["type"]] = types.get(r["type"], 0) + 1
    print(f"catalog.json: {len(records)} объектов " f"(статических {n_static}); по типам: {types}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
