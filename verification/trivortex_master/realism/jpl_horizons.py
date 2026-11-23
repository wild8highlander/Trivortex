#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — эфемериды JPL Horizons (REST API).

Запрос эфемерид тел Солнечной системы через публичный API
https://ssd.jpl.nasa.gov/api/horizons.api (Giorgini et al. 1996+):

  * fetch_ephemeris(): JSON-запрос с кэшированием (TTLCache);
  * parse_vector_table(): разбор VECTOR-таблиц (позиции/скорости);
  * parse_observer_table(): разбор OBSERVER-таблиц (RA/Dec/топоцентрик);
  * build_bodies(): превращение эфемерид в Body лаборатории;
  * offline-режим: синтетические круговые орбиты при недоступной сети
    (честная помеченная замена, не выдумка «реальных» данных).

Использование: пресет «планеты на сегодняшнюю дату» в лаборатории.
"""
from __future__ import annotations

import datetime as _dt
import json
import math
import os
import urllib.parse
import urllib.request
from typing import Any

AU_M = 1.495978707e11

HORIZONS_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"
SOURCE = "https://ssd.jpl.nasa.gov/api/horizons.api (JPL SSD)"

# id тел в Horizons (major bodies)
BODIES = {
    "mercury": "199", "venus": "299", "earth": "399", "mars": "499",
    "jupiter": "599", "saturn": "699", "uranus": "799", "neptune": "899",
    "sun": "10", "moon": "301",
}

# массы (кг) и радиусы (м) для сборки Body — NSSDC
BODIES_PHYS = {
    "mercury": (3.301e23, 2.4397e6), "venus": (4.867e24, 6.0518e6),
    "earth": (5.9722e24, 6.371e6), "mars": (6.417e23, 3.3895e6),
    "jupiter": (1.898e27, 6.9911e7), "saturn": (5.683e26, 5.8232e7),
    "uranus": (8.681e25, 2.5362e7), "neptune": (1.024e26, 2.4622e7),
    "sun": (1.9884e30, 6.957e8), "moon": (7.342e22, 1.7375e6),
}


def _cache() -> Any:
    from realism.data_fetchers.cache import TTLCache
    root = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    return TTLCache(os.path.join(root, "data", "cache"))


def fetch_ephemeris(body_id: str, start: str, stop: str, step: str = "1d",
                    format: str = "json", use_cache: bool = True,
                    timeout: float = 30.0) -> dict[str, Any]:
    """Запросить вектор состояния тела из Horizons.

    body_id: '599' (Юпитер), '399' (Земля)…; start/stop: 'YYYY-MM-DD'.
    Возвращает dict с 'result' (текстовый блок Horizons) или error.
    """
    cache = _cache()
    key = f"horizons_{body_id}_{start}_{stop}_{step}"
    if use_cache:
        cached = cache.get(key)
        if cached is not None:
            return cached
    params = {
        "format": format, "COMMAND": f"'{body_id}'",
        "EPHEM_TYPE": "VECTORS", "CENTER": "'500@0'",
        "START_TIME": f"'{start}'", "STOP_TIME": f"'{stop}'",
        "STEP_SIZE": f"'{step}'", "REF_PLANE": "ECLIPTIC",
        "REF_SYSTEM": "J2000", "OUT_UNITS": "KM-S",
        "CSV_FORMAT": "'YES'", "VEC_TABLE": "'2'",
    }
    url = HORIZONS_URL + "?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "trivortex-master/2.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        # offline: старый кэш или отказ
        stale = cache.get_stale(key)
        if stale is not None:
            return stale
        return dict(error=f"Horizons недоступен: {exc}")
    if use_cache:
        cache.put(key, payload)
    return payload


def parse_vector_table(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Разобрать CSV VECTOR-блок ответа Horizons.

    Возвращает [{jd, x, y, z, vx, vy, vz (км, км/с)}].
    """
    text = payload.get("result", "")
    rows: list[dict[str, Any]] = []
    in_block = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("$$SOE"):
            in_block = True
            continue
        if stripped.startswith("$$EOE"):
            break
        if not in_block or not stripped or stripped.startswith("#"):
            continue
        parts = [p.strip() for p in stripped.split(",")]
        if len(parts) < 7:
            continue
        try:
            rows.append(dict(
                jd=float(parts[0]),
                x=float(parts[2]), y=float(parts[3]), z=float(parts[4]),
                vx=float(parts[5]), vy=float(parts[6]), vz=float(parts[7])
                if len(parts) > 7 else 0.0))
        except ValueError:
            continue
    return rows


def build_body_from_horizons(name: str, rows: list[dict[str, Any]],
                             at_index: int = 0):
    """Собрать Body лаборатории из строки эфемерид (м, м/с)."""
    from lab.body import Body
    if name not in BODIES_PHYS:
        raise KeyError(f"нет физических параметров для {name}")
    mass, radius = BODIES_PHYS[name]
    if not rows:
        raise ValueError("пустые эфемериды")
    row = rows[min(at_index, len(rows) - 1)]
    return Body(
        id=f"hor_{name}", name=name.capitalize(),
        mass=mass, radius=radius,
        position=(row["x"] * 1000.0, row["y"] * 1000.0,
                  row["z"] * 1000.0),
        velocity=(row["vx"] * 1000.0, row["vy"] * 1000.0,
                  row["vz"] * 1000.0),
        color=dict(mercury="#8C8C8C", venus="#E6C27A", earth="#4FD1C5",
                   mars="#C1440E", jupiter="#D8A47F", saturn="#E3C98F",
                   uranus="#A5E3E0", neptune="#4B70DD", sun="#FDB813",
                   moon="#B0B0B0").get(name, "#4FD1C5"),
        type="planet" if name not in ("sun", "moon") else
             ("star" if name == "sun" else "moon"),
        source=SOURCE,
        metadata=dict(jd=row["jd"], source_system="JPL Horizons"))


def synthetic_circular_orbit(name: str, reference_date=None):
    """Offline-замена: круговая орбита по средним элементам (J2000).

    Честная помеченная аппроксимация для работы без сети: позиция по
    средней долготе на дату; используется в metadata флаг approximate.
    """
    from lab.body import Body
    if reference_date is None:
        reference_date = _dt.date(2000, 1, 1)
    # средние элементы J2000 (a а.е., период лет, L₀ град — NASA fact sheet)
    elems = dict(
        mercury=(0.387, 0.2408, 252.25), venus=(0.723, 0.6152, 181.98),
        earth=(1.000, 1.0000, 100.46), mars=(1.524, 1.8808, 355.45),
        jupiter=(5.203, 11.862, 34.40), saturn=(9.537, 29.457, 49.94),
        uranus=(19.191, 84.017, 313.23), neptune=(30.069, 164.79, 304.88),
    )
    if name not in elems:
        raise KeyError(f"нет элементов для {name}")
    a_au, period_yr, lon0 = elems[name]
    days = (reference_date - _dt.date(2000, 1, 1)).days
    lon = math.radians(lon0 + 360.0 * days / (period_yr * 365.25))
    r = a_au * AU_M
    mu = 6.6743e-11 * BODIES_PHYS["sun"][0]
    v = math.sqrt(mu / r)
    mass, radius = BODIES_PHYS[name]
    return Body(
        id=f"syn_{name}", name=name.capitalize(),
        mass=mass, radius=radius,
        position=(r * math.cos(lon), r * math.sin(lon), 0.0),
        velocity=(-v * math.sin(lon), v * math.cos(lon), 0.0),
        color="#4FD1C5", type="planet",
        source="synthetic (offline-приближение, средние элементы J2000)",
        metadata=dict(approximate=True, a_au=a_au))


def fetch_planets_today(names: list[str] | None = None,
                        use_cache: bool = True) -> dict[str, Any]:
    """Собрать текущие векторы планет: онлайн Horizons или offline-режим.

    Возвращает {name: Body} + флаг режима (online/offline).
    """
    names = names or ["mercury", "venus", "earth", "mars"]
    today = _dt.date.today().isoformat()
    stop = (_dt.date.today() + _dt.timedelta(days=1)).isoformat()
    out: dict[str, Any] = dict(bodies={}, mode=None, date=today)
    online_any = False
    for name in names:
        hid = BODIES.get(name)
        if hid is None:
            continue
        payload = fetch_ephemeris(hid, today, stop, "1d",
                                  use_cache=use_cache)
        if "error" in payload:
            body = synthetic_circular_orbit(name)
        else:
            rows = parse_vector_table(payload)
            if not rows:
                body = synthetic_circular_orbit(name)
            else:
                body = build_body_from_horizons(name, rows, 0)
                online_any = True
        out["bodies"][name] = body
    out["mode"] = "online" if online_any else "offline-synthetic"
    return out


def self_check() -> dict:
    """Онлайн: Земля на ~1 а.е. от Солнца; offline: круговая орбита валидна."""
    today = _dt.date.today()
    res = fetch_planets_today(["earth", "mars"], use_cache=False)
    bodies = res["bodies"]
    checks = {}
    if "earth" in bodies:
        earth = bodies["earth"]
        r = math.sqrt(sum(c * c for c in earth.position))
        checks["earth_r_au"] = r / AU_M
        checks["earth_r_ok"] = 0.98 < r / AU_M < 1.02
        v = earth.speed()
        checks["earth_v_kms"] = v / 1000.0
        checks["earth_v_ok"] = 28.0 < v / 1000.0 < 31.5
    # offline-ветка
    syn = synthetic_circular_orbit("mars", today)
    r_mars = math.sqrt(sum(c * c for c in syn.position))
    checks["mars_syn_r_au"] = r_mars / AU_M
    checks["mars_syn_ok"] = 1.4 < r_mars / AU_M < 1.7
    checks["mode"] = res["mode"]
    checks["date"] = res["date"]
    checks["ok"] = all(v for k, v in checks.items()
                       if k.endswith("_ok")) and len(bodies) == 2
    return checks
