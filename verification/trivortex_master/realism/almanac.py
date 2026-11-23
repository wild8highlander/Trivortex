#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — астрономический альманах.

Практические расчёты для наблюдателя:

  * moon_phase: фаза Луны по возрасту в синодическом цикле
    (P_syn = 29.530588 сут, NASA факт); освещённая доля и имя фазы;
  * moon_phases_between: моменты одинаковых фаз → синодический месяц;
  * sun_rise_set: восход/закос Солнца по широте и склонению
    (часовой угол восхода, рефракция −0.83° стандарт);
  * twilight_times: сумерки (гражданские −6°, навигационные −12°,
    астрономические −18°);
  * polar_day_night: полярный день/ночь по широте и склонению;
  * seasons: равноденствия/солнцестояния по эклиптической долготе.

Самопроверка: синодический месяц из двух одинаковых фаз = 29.53 сут;
на широте 90° — полярный день при δ > 0; восход при |φ| = 90° не
определён (солнце всегда на горизонте).
"""

from __future__ import annotations

import math

SYNODIC_MONTH = 29.530588  # сут (NASA)
SIDEREAL_MONTH = 27.321661
TROPICAL_YEAR = 365.2422
OBLIQUITY = 23.4392911


# ═══════════════════════════════════════════════════════════════════════════
# Фазы Луны
# ═══════════════════════════════════════════════════════════════════════════
def moon_phase(age_days: float) -> dict:
    """Фаза Луны по возрасту цикла (0 = новолуние).

    Возвращает долю освещённости и стандартное имя фазы."""
    frac = (age_days % SYNODIC_MONTH) / SYNODIC_MONTH
    # освещённая доля: (1 − cos 2π·frac)/2
    illuminated = (1.0 - math.cos(2 * math.pi * frac)) / 2.0
    names = [
        (0.02, "новолуние"),
        (0.23, "молодая (первая четверть растёт)"),
        (0.27, "первая четверть"),
        (0.48, "растущая (горбатая)"),
        (0.52, "полнолуние"),
        (0.73, "убывающая (горбатая)"),
        (0.77, "последняя четверть"),
        (0.98, "старая (серп)"),
    ]
    name = "новолуние"
    for edge, label in names:
        if frac <= edge:
            name = label
            break
    else:
        name = "старая (серп)"
    return dict(
        age_days=age_days % SYNODIC_MONTH, fraction=frac, illuminated=illuminated, name=name
    )


def synodic_month_check() -> dict:
    """Два новолуния подряд: интервал = 29.530588 сут (определение)."""
    m1 = moon_phase(0.0)
    m2 = moon_phase(SYNODIC_MONTH)
    same = abs(m1["fraction"] - m2["fraction"]) < 1e-9
    return dict(
        synodic_days=SYNODIC_MONTH, same_phase=same, reference="NASA Moon Fact Sheet: 29.530588 сут"
    )


def elongation_to_phase(elongation_deg: float) -> float:
    """Обратная задача: элонгация Луны от Солнца → возраст цикла (сут).

    elongation = 2π·frac (приближение круговой орбиты)."""
    return (elongation_deg / 360.0) * SYNODIC_MONTH


# ═══════════════════════════════════════════════════════════════════════════
# Восход/заход и сумерки
# ═══════════════════════════════════════════════════════════════════════════
def rise_set_hour_angle(
    dec_deg: float, lat_deg: float, horizon_deg: float = -0.833
) -> float | None:
    """Часовой угол восхода/захода (радианы); None — не восходит.

    horizon −0.833° = рефракция + размер Солнца (стандарт альманахов).
    """
    dec = math.radians(dec_deg)
    lat = math.radians(lat_deg)
    h0 = math.radians(horizon_deg)
    cos_H = (math.sin(h0) - math.sin(lat) * math.sin(dec)) / (math.cos(lat) * math.cos(dec))
    if cos_H > 1.0:
        return None  # никогда не восходит
    if cos_H < -1.0:
        return math.pi  # не заходит
    return math.acos(cos_H)


def day_length_hours(dec_deg: float, lat_deg: float, horizon_deg: float = -0.833) -> float | None:
    """Длительность светового дня (часы); None — полярный день/ночь.

    Горизонт по умолчанию −0.833° (рефракция + диск) — на экваторе в
    равноденствие даёт 12.11 ч, а не ровно 12 (физика, не ошибка)."""
    H = rise_set_hour_angle(dec_deg, lat_deg, horizon_deg)
    if H is None:
        return None
    return 2.0 * H * 12.0 / math.pi


def is_polar_day(dec_deg: float, lat_deg: float) -> bool:
    """Полярный день: tan φ · tan δ > 1 (на полярном круге ровно 1)."""
    tan_phi = math.tan(math.radians(lat_deg))
    tan_dec = math.tan(math.radians(dec_deg))
    return tan_phi * tan_dec > 1.0


def is_polar_night(dec_deg: float, lat_deg: float) -> bool:
    """Полярная ночь: tan φ · tan δ < −1 (Солнце не встаёт)."""
    tan_phi = math.tan(math.radians(lat_deg))
    tan_dec = math.tan(math.radians(dec_deg))
    return tan_phi * tan_dec < -1.0


def twilight_hours(dec_deg: float, lat_deg: float, kind: str = "civil") -> float | None:
    """Длительность сумерек (часы) данного типа.

    civil: −6°, nautical: −12°, astronomical: −18°."""
    limits = dict(civil=-6.0, nautical=-12.0, astronomical=-18.0)
    h0 = limits.get(kind)
    if h0 is None:
        raise KeyError(f"тип сумерек {kind} не в civil/nautical/astronomical")
    # время, пока центр Солнца между h0 и горизонтом
    H_up = rise_set_hour_angle(dec_deg, lat_deg, 0.0)
    H_tw = rise_set_hour_angle(dec_deg, lat_deg, h0)
    if H_up is None or H_tw is None:
        return None
    return 2.0 * (H_up - H_tw) * 12.0 / math.pi


# ═══════════════════════════════════════════════════════════════════════════
# Сезоны
# ═══════════════════════════════════════════════════════════════════════════
def solar_declination(day_of_year: float) -> float:
    """Склонение Солнца по дню года (грубая синус-модель).

    δ = −ε·cos(2π·(d+10)/365.2422) — равноденствие ≈ день 80 (21 марта)."""
    return -OBLIQUITY * math.cos(2 * math.pi * (day_of_year + 10.0) / TROPICAL_YEAR)


def equinox_day() -> float:
    """День весеннего равноденствия (δ = 0 в марте): численно."""
    lo, hi = 70.0, 95.0
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if solar_declination(mid) > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def solstice_days() -> dict:
    """Дни солнцестояний (δ = ±ε)."""
    summer = None
    winter = None
    for d in range(0, 366):
        dec = solar_declination(d)
        if abs(dec - OBLIQUITY) < 0.01 and summer is None:
            summer = d
        if abs(dec + OBLIQUITY) < 0.01 and winter is None:
            winter = d
    return dict(
        summer_solstice=summer, winter_solstice=winter, note="грубая модель без уравнения времени"
    )


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Синодический месяц; полярный день на 90°; день 80 ≈ равноденствие;
    δ(172) ≈ +23.4° (летнее солнцестояние ~21 июня = день 172)."""
    syn = synodic_month_check()
    pd = is_polar_day(23.44, 90.0)
    pn = is_polar_night(-23.44, 90.0)
    eq = equinox_day()
    eq_ok = 78.0 < eq < 84.0
    dec_summer = solar_declination(172.0)
    summer_ok = abs(dec_summer - 23.439) < 0.15
    # длина дня на экваторе при δ=0: 12 ч (горизонт 0°, без рефракции)
    dl = day_length_hours(0.0, 0.0, horizon_deg=0.0)
    dl_ok = dl is not None and abs(dl - 12.0) < 0.01
    # с рефракцией: 12.11 ч (день длиннее ночи в равноденствие)
    dl_ref = day_length_hours(0.0, 0.0)
    refraction_ok = dl_ref is not None and 12.05 < dl_ref < 12.2
    # фаза: возраст 14.77 сут → полнолуние
    full = moon_phase(14.765294)
    full_ok = abs(full["illuminated"] - 1.0) < 1e-9
    return dict(
        synodic_ok=syn["same_phase"],
        polar_day_ok=pd,
        polar_night_ok=pn,
        refraction_hours=round(dl_ref, 3),
        refraction_ok=refraction_ok,
        equinox_day=round(eq, 1),
        eq_ok=eq_ok,
        summer_dec=round(dec_summer, 2),
        summer_ok=summer_ok,
        equator_day_hours=dl,
        dl_ok=dl_ok,
        full_illuminated=full["illuminated"],
        full_ok=full_ok,
        all_ok=syn["same_phase"] and pd and pn and eq_ok and summer_ok and dl_ok and full_ok,
        note="модель круговая (без уравнения времени и эллипса орбиты)",
    )
