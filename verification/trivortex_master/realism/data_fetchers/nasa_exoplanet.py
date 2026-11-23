#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — загрузчик экзопланет из NASA Exoplanet Archive.

TAP-сервис (sync): https://exoplanetarchive.ipac.caltech.edu/TAP/sync
Таблица ps (Planetary Systems), default_flag=1, формат json.
Кэш — суточный, через realism.data_fetchers.cache.TTLCache.

Функции:
  fetch_confirmed_planets(limit) -> list[dict]  — сырые TAP-строки;
  to_body(record) -> lab.body.Body               — трансляция в Body;
  validate_schema(rows) -> list[str]             — проверка колонок.
"""

from __future__ import annotations

import json
import os
import urllib.request
from typing import Any

from lab.body import Body

TAP_SYNC = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
M_EARTH_KG = 5.9722e24
R_EARTH_KM = 6371.0
AU_M = 1.495978707e11

# ожидаемые колонки (для validate_schema)
EXPECTED_COLUMNS = (
    "pl_name",
    "hostname",
    "sy_dist",
    "pl_rade",
    "pl_bmasse",
    "pl_orbsmax",
    "pl_orbper",
    "disc_year",
    "discoverymethod",
)

_CACHE = None


def _default_cache_dir() -> str:
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(root, "data", "cache")


def get_cache():
    global _CACHE
    if _CACHE is None:
        from realism.data_fetchers.cache import TTLCache

        _CACHE = TTLCache(_default_cache_dir())
    return _CACHE


def build_query(limit: int) -> str:
    """ADQL-запрос: ближайшие подтверждённые планеты."""
    return (
        "select+pl_name,hostname,sy_dist,pl_rade,pl_bmasse,pl_orbsmax,"
        "pl_orbper,disc_year,discoverymethod,st_mass,st_rad+"
        "from+ps+where+default_flag=1+order+by+sy_dist+asc"
    )


def fetch_confirmed_planets(
    limit: int = 100, timeout: float = 30.0, use_cache: bool = True
) -> list[dict[str, Any]]:
    """Сырые строки TAP; при недоступной сети — последний кэш, иначе []."""
    cache_key = "exoplanets_latest"
    if use_cache:
        cached = get_cache().get(cache_key)
        if cached:
            return cached[:limit]
    url = f"{TAP_SYNC}?query={build_query(limit)}&format=json"
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "trivortex-master/1.0 " "(laboratory N-body suite)"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            rows = json.loads(resp.read().decode("utf-8"))
    except Exception:
        # сеть недоступна: пробуем любой старый снимок
        stale = get_cache().get_stale(cache_key)
        if stale:
            return stale[:limit]
        # отдельные датированные снимки (от tools/build_catalog.py)
        cache_dir = _default_cache_dir()
        snaps = sorted(
            (f for f in os.listdir(cache_dir) if f.startswith("exoplanets_2")), reverse=True
        )
        if snaps:
            with open(os.path.join(cache_dir, snaps[0]), encoding="utf-8") as fh:
                return json.load(fh)[:limit]
        return []
    if use_cache and rows:
        get_cache().put(cache_key, rows)
    return rows[:limit]


def validate_schema(rows: list[dict[str, Any]]) -> list[str]:
    """Проверка ожидаемых колонок в TAP-ответе."""
    if not rows:
        return ["пустой ответ TAP"]
    problems = []
    first = rows[0]
    for col in EXPECTED_COLUMNS:
        if col not in first:
            problems.append(f"нет колонки {col}")
    return problems


def to_body(record: dict[str, Any]) -> Body:
    """TAP-строка → Body (масса кг, радиус м, орбита м)."""
    name = record.get("pl_name", "unnamed")
    mass_e = record.get("pl_bmasse")
    rad_e = record.get("pl_rade")
    est = False
    if mass_e is None:
        mass_e = (rad_e or 1.0) ** 3  # оценка по плотности Земли
        est = True
    if rad_e is None:
        rad_e = (mass_e or 1.0) ** (1.0 / 3.0)
    body = Body(
        id="exo_"
        + name.lower().replace(" ", "_").replace("-", "_").replace("'", "").replace(".", ""),
        name=name,
        mass=float(mass_e) * M_EARTH_KG,
        radius=float(rad_e) * R_EARTH_KM * 1000.0,
        color="#F4A988",
        type="exoplanet",
        source="https://exoplanetarchive.ipac.caltech.edu/",
    )
    if est:
        body.metadata["mass_estimated"] = True
    for src, dst, conv in (
        ("pl_orbsmax", "orbit_au_m", AU_M),
        ("sy_dist", "distance_pc", 1.0),
        ("pl_orbper", "period_days", 1.0),
        ("disc_year", "discovery_year", 1.0),
        ("hostname", "host_star", 1.0),
        ("discoverymethod", "discovery_method", 1.0),
    ):
        val = record.get(src)
        if val is not None:
            body.metadata[dst] = val * conv if isinstance(val, (int, float)) else val
    return body


def fetch_bodies(limit: int = 20) -> list[Body]:
    """Удобная обёртка: сразу список Body."""
    return [to_body(r) for r in fetch_confirmed_planets(limit=limit)]


def nearest_systems(limit: int = 15) -> list[dict[str, Any]]:
    """Ближайшие планетные системы (для меню справки)."""
    rows = fetch_confirmed_planets(limit=500)
    systems: dict[str, dict] = {}
    for r in rows:
        host = r.get("hostname", "?")
        if host not in systems:
            systems[host] = dict(host=host, distance_pc=r.get("sy_dist"), planets=[])
        systems[host]["planets"].append(r.get("pl_name", "?"))
    out = sorted(systems.values(), key=lambda s: s["distance_pc"] or 1e9)
    return out[:limit]
