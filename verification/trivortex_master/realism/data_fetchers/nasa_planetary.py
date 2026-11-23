#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — планетарный факт-шит Солнечной системы.

Статический набор (NSSDC Planetary Fact Sheet) + опциональное обновление
по URL. Значения сверены с https://nssdc.gsfc.nasa.gov/planetary/factsheet/
"""

from __future__ import annotations

import json
import os
from typing import Any

from lab.body import Body

NSSDC_URL = "https://nssdc.gsfc.nasa.gov/planetary/factsheet/"
AU_M = 1.495978707e11

# Статический факт-шит: (id, name, mass_kg, radius_km, orbit_au, color)
PLANETS = [
    ("mercury", "Mercury", 3.301e23, 2439.7, 0.387, "#8C8C8C"),
    ("venus", "Venus", 4.867e24, 6051.8, 0.723, "#E6C27A"),
    ("earth", "Earth", 5.9722e24, 6371.0, 1.000, "#4FD1C5"),
    ("mars", "Mars", 6.417e23, 3389.5, 1.524, "#C1440E"),
    ("jupiter", "Jupiter", 1.898e27, 69911.0, 5.203, "#D8A47F"),
    ("saturn", "Saturn", 5.683e26, 58232.0, 9.537, "#E3C98F"),
    ("uranus", "Uranus", 8.681e25, 25362.0, 19.191, "#A5E3E0"),
    ("neptune", "Neptune", 1.024e26, 24622.0, 30.069, "#4B70DD"),
]

MOONS = [
    # (id, name, parent, mass_kg, radius_km, orbit_km, color)
    ("moon", "Moon", "earth", 7.342e22, 1737.5, 384400.0, "#B0B0B0"),
    ("io", "Io", "jupiter", 8.932e22, 1821.6, 421700.0, "#F0D040"),
    ("europa", "Europa", "jupiter", 4.8e22, 1560.8, 671100.0, "#D9C7B8"),
    ("ganymede", "Ganymede", "jupiter", 1.4819e23, 2634.1, 1070400.0, "#A89F91"),
    ("callisto", "Callisto", "jupiter", 1.0759e23, 2410.3, 1882700.0, "#7A6E5D"),
    ("titan", "Titan", "saturn", 1.3452e23, 2574.7, 1221870.0, "#E0A040"),
    ("titania", "Titania", "uranus", 3.527e21, 788.9, 436300.0, "#C0C0C0"),
    ("triton", "Triton", "neptune", 2.139e22, 1353.4, 354759.0, "#C8D8D8"),
]

SUN = ("sun", "Sun", 1.9884e30, 695700.0, "#FDB813")


def planetary_bodies() -> list[Body]:
    """Солнце + 8 планет + 8 крупных лун как Body (радиусы в метрах)."""
    out = []
    out.append(
        Body(
            id=SUN[0],
            name=SUN[1],
            mass=SUN[2],
            radius=SUN[3] * 1000.0,
            color=SUN[4],
            type="star",
            source=NSSDC_URL + "sunfact.html",
        )
    )
    for pid, name, m, r, a, color in PLANETS:
        out.append(
            Body(
                id=pid,
                name=name,
                mass=m,
                radius=r * 1000.0,
                color=color,
                type="planet",
                source=NSSDC_URL,
                metadata=dict(orbit_au=a),
            )
        )
    for mid, name, parent, m, r, orbit_km, color in MOONS:
        out.append(
            Body(
                id=mid,
                name=name,
                mass=m,
                radius=r * 1000.0,
                color=color,
                type="moon",
                source=NSSDC_URL,
                metadata=dict(parent=parent, orbit_km=orbit_km),
            )
        )
    return out


def update_cache(path: str | None = None) -> bool:
    """Опциональное обновление снимка факт-шита (сеть может быть закрыта —
    тогда молча используем статические значения)."""
    import urllib.request

    path = path or os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "data",
        "cache",
        "planetary_factsheet.json",
    )
    try:
        req = urllib.request.Request(NSSDC_URL, headers={"User-Agent": "trivortex-master/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(
                dict(
                    source=NSSDC_URL, size=len(html), note="HTML-снимок факт-шита; значения в коде"
                ),
                fh,
            )
        return True
    except Exception:
        return False


def fact_sheet_table() -> list[dict[str, Any]]:
    """Таблица факт-шита для отчётов и меню."""
    rows = []
    for pid, name, m, r, a, color in PLANETS:
        rows.append(
            dict(
                id=pid,
                name=name,
                mass_kg=m,
                radius_km=r,
                orbit_au=a,
                period_days=(365.256 * a**1.5),
                color=color,
                source=NSSDC_URL,
            )
        )
    return rows
