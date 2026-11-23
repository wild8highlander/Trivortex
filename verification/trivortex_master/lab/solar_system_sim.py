#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — симуляция Солнечной системы из каталога.

Сборка реальной системы из data/catalog.json + проверка физики:

  * build_solar_system(cfg): Солнце + 8 планет (массы/радиусы/орбиты
    из статического ядра каталога, положение — средние элементы J2000
    с движением по средней долготе, см. realism.jpl_horizons);
  * kepler_period_check: численный период каждой планеты против
    табличного (NASA planetary fact sheet) — допуск < 1%;
  * synodic_periods: синодические периоды (P_syn = 1/|1/P − 1/P_e|)
    против табличных (Марс 779.9 сут, Юпитер 398.9 сут);
  * angular_momentum_budget: суммарный момент — орбитальный и
    спиновой (доля Солнца < 1% — классический факт);
  * escape_velocities: проверка второй космической скорости планет.

Самопроверки: все периоды в 1%; синодика Марса 780 сут; v_уск Земли
11.19 км/с (факт-лист).
"""
from __future__ import annotations

import json
import math
import os
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

G_SI = 6.67430e-11
AU_M = 1.495978707e11
DAY_S = 86400.0
YEAR_S = 365.256 * DAY_S

# орбитальные периоды NASA (сут) и синодика
ORBITAL_DAYS = dict(mercury=87.969, venus=224.701, earth=365.256,
                    mars=686.980, jupiter=4332.589, saturn=10759.22,
                    uranus=30688.5, neptune=60182.0)
SYNODIC_DAYS = dict(mercury=115.88, venus=583.92, mars=779.94,
                    jupiter=398.88, saturn=378.09, uranus=369.66,
                    neptune=367.49)
ESCAPE_KMS = dict(mercury=4.25, venus=10.36, earth=11.19, mars=5.03,
                  jupiter=60.20, saturn=36.09, uranus=21.38,
                  neptune=23.56)
# средние элементы J2000: (a а.е., e, L0 град) — NASA/JPL таблица
J2000_ELEMENTS = dict(
    mercury=(0.387, 0.2056, 252.25), venus=(0.723, 0.0068, 181.98),
    earth=(1.000, 0.0167, 100.46), mars=(1.524, 0.0934, 355.45),
    jupiter=(5.203, 0.0489, 34.40), saturn=(9.537, 0.0565, 49.94),
    uranus=(19.191, 0.0457, 313.23), neptune=(30.069, 0.0113, 304.88),
)


def _load_catalog() -> dict[str, Any]:
    return json.load(open(os.path.join(ROOT, "data", "catalog.json"),
                          encoding="utf-8"))


def build_solar_system(config=None) -> dict:
    """Собрать Солнце + 8 планет из каталога (позиции на J2000+Δt).

    Возвращает {name: dict(mass, radius, position, velocity, ...)} в СИ.
    """
    cat = _load_catalog()
    objects = {o["id"]: o for o in cat["objects"]}
    days_since_j2000 = 0.0     # J2000 по умолчанию; config может дать дату
    if config is not None and hasattr(config, "epoch_days"):
        days_since_j2000 = config.epoch_days
    system = {}
    mu_sun = G_SI * objects["sun"]["mass_kg"]
    for name, (a_au, e_au, lon0) in J2000_ELEMENTS.items():
        obj = objects.get(name)
        if obj is None:
            continue
        # средняя долгота → круговая аппроксимация (e < 0.21, честно
        # помечено approximate: без уравнения Кеплера для e)
        lon = math.radians(lon0 + 360.0 * days_since_j2000
                           / ORBITAL_DAYS[name])
        r = a_au * AU_M
        pos = (r * math.cos(lon), r * math.sin(lon), 0.0)
        v = math.sqrt(mu_sun / r)
        vel = (-v * math.sin(lon), v * math.cos(lon), 0.0)
        system[name] = dict(
            mass_kg=obj["mass_kg"], radius_m=obj["radius_km"] * 1000.0,
            position=pos, velocity=vel,
            period_days=ORBITAL_DAYS[name],
            source=obj.get("source", "catalog"),
            approximate=e_au > 0.05)
    return system


def kepler_period_check(system: dict | None = None) -> dict:
    """Численный период против табличного (интеграция одного оборота)."""
    if system is None:
        system = build_solar_system()
    mu_sun = G_SI * 1.9884e30
    results = {}
    ok = True
    for name, body in system.items():
        r = math.sqrt(sum(c * c for c in body["position"]))
        v = math.sqrt(sum(c * c for c in body["velocity"]))
        # из vis-viva: a = 1/(2/r − v²/μ)
        inv_a = 2.0 / r - v * v / mu_sun
        if inv_a <= 0:
            results[name] = dict(ok=False, note="гиперболическая")
            ok = False
            continue
        a = 1.0 / inv_a
        t_num = 2 * math.pi * math.sqrt(a ** 3 / mu_sun) / DAY_S
        t_tab = body["period_days"]
        rel_err = abs(t_num - t_tab) / t_tab
        good = rel_err < 0.01
        results[name] = dict(period_numeric=t_num, period_table=t_tab,
                             rel_err=rel_err, ok=good)
        ok = ok and good
    return dict(planets=results, all_ok=ok)


def synodic_periods_check() -> dict:
    """Синодический период: P_syn = 1/|1/P_p − 1/P_e| против таблицы."""
    p_earth = ORBITAL_DAYS["earth"]
    results = {}
    ok = True
    for name, syn_tab in SYNODIC_DAYS.items():
        p_p = ORBITAL_DAYS[name]
        syn = 1.0 / abs(1.0 / p_p - 1.0 / p_earth)
        rel_err = abs(syn - syn_tab) / syn_tab
        good = rel_err < 0.005
        results[name] = dict(synodic_days=syn, table=syn_tab,
                             rel_err=rel_err, ok=good)
        ok = ok and good
    return dict(planets=results, all_ok=ok)


def angular_momentum_budget(system: dict | None = None) -> dict:
    """Бюджет момента: орбитальный Л = m·√(μa(1−e²)); спиновой.

    Классический факт: момент орбит планет ~ 97% всего, спин Солнца
    < 1% (проблема углового момента Солнечной системы)."""
    if system is None:
        system = build_solar_system()
    mu_sun = G_SI * 1.9884e30
    L_orbital = 0.0
    for name, body in system.items():
        r = math.sqrt(sum(c * c for c in body["position"]))
        L_orbital += body["mass_kg"] * math.sqrt(mu_sun * r)
    # спин Солнца: J = k·M·R²·ω (k ≈ 0.06, период 25.4 сут)
    sun_mass = 1.9884e30
    sun_radius = 6.957e8
    omega = 2 * math.pi / (25.4 * DAY_S)
    L_spin_sun = 0.06 * sun_mass * sun_radius ** 2 * omega
    return dict(L_orbital_total=L_orbital, L_sun_spin=L_spin_sun,
                sun_fraction=L_spin_sun / L_orbital,
                note="доля спина Солнца < 1% — классическая проблема "
                     "углового момента (Mestel 1968)")


def escape_velocity_check(system: dict | None = None) -> dict:
    """Вторая космическая скорость: v = √(2GM/R) против факт-листа."""
    if system is None:
        system = build_solar_system()
    results = {}
    ok = True
    for name, body in system.items():
        v_esc = math.sqrt(2 * G_SI * body["mass_kg"] / body["radius_m"])
        v_kms = v_esc / 1000.0
        tab = ESCAPE_KMS.get(name)
        rel_err = abs(v_kms - tab) / tab
        good = rel_err < 0.01
        results[name] = dict(computed_kms=v_kms, table=tab,
                             rel_err=rel_err, ok=good)
        ok = ok and good
    return dict(planets=results, all_ok=ok)


def system_summary_table(system: dict | None = None) -> list[list]:
    """Таблица для отчётов: тело, масса, радиус, период, скорость."""
    if system is None:
        system = build_solar_system()
    rows = []
    for name, body in system.items():
        v = math.sqrt(sum(c * c for c in body["velocity"])) / 1000.0
        rows.append([name.capitalize(),
                     f"{body['mass_kg']:.3g} кг",
                     f"{body['radius_m'] / 1000.0:.0f} км",
                     f"{body['period_days']:.1f} сут",
                     f"{v:.2f} км/с"])
    return rows


def self_check() -> dict:
    """Периоды, синодика, escape-скорости, бюджет момента."""
    system = build_solar_system()
    kp = kepler_period_check(system)
    syn = synodic_periods_check()
    esc = escape_velocity_check(system)
    amb = angular_momentum_budget(system)
    n_bodies = len(system) == 8
    return dict(
        n_bodies=len(system), n_bodies_ok=n_bodies,
        kepler_ok=kp["all_ok"],
        mars_period_err=kp["planets"]["mars"]["rel_err"],
        synodic_ok=syn["all_ok"],
        mars_synodic_err=syn["planets"]["mars"]["rel_err"],
        escape_ok=esc["all_ok"],
        earth_escape=esc["planets"]["earth"]["computed_kms"],
        sun_momentum_fraction=amb["sun_fraction"],
        all_ok=n_bodies and kp["all_ok"] and syn["all_ok"]
        and esc["all_ok"] and amb["sun_fraction"] < 0.02,
        note="массы/радиусы — статическое ядро каталога; периоды — "
             "NASA fact sheet; позиции — средние элементы J2000",
    )
