#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — затмения: геометрия, циклы, предсказание.

  * eclipse_conditions: условие затмения — новолуние вблизи узла
    (ширина затменной полосы по β: |β| < β_limit ≈ 1.54° для полного
    солнечного затмения при «близком» Луно-перигее);
  * shadow_cone: длина конуса тени Луны (L = R·D/(R−S), стандартная
    формула из треугольника Солнце-Луна-точка);
  * saros_cycle: Сарос = 223 синодических месяцев = 6585.32 сут
    (повторение геометрии затмений);
  * eclipse_year: 346.62 сут — Солнце возвращается к лунному узлу
    (1/T_ecl = 1/T_trop + 1/T_node);
  * eclipse_season_spacing: затменные сезоны каждые 173.31 сут.

Самопроверки: Сарос из 223 синодических = 6585.32 (точно); затменный
год 346.62; сезон 173.31; конус тени Луны ≈ 375 000 км при среднем
расстоянии (длиннее/короче геоцентрического расстояния → полное или
кольцевое).
"""

from __future__ import annotations


SYNODIC_D = 29.530588  # синодический месяц (сут)
DRACONIC_D = 27.212221  # драконический месяц (сут)
TROPICAL_YEAR_D = 365.2422
NODAL_REGRESSION_Y = 18.61  # прецессия узлов лунной орбиты (лет)
NODE_REGRESSION_D = NODAL_REGRESSION_Y * 365.25


def eclipse_year_days() -> float:
    """Затменный год: 1/T = 1/T_троп + 1/T_узлов → 346.62 сут."""
    rate = 1.0 / TROPICAL_YEAR_D + 1.0 / NODE_REGRESSION_D
    return 1.0 / rate


def saros_days() -> float:
    """Сарос: 223 синодических месяца (6585.32 сут)."""
    return 223.0 * SYNODIC_D


def eclipse_season_spacing() -> float:
    """Интервал между затменными сезонами: половина затменного года."""
    return eclipse_year_days() / 2.0


def shadow_cone_length(r_body_km: float, d_body_sun_km: float, r_sun_km: float = 6.957e5) -> float:
    """Длина конуса тени: L = R_b·D/(R_s − R_b) (км).

    Для Луны (R=1737, D≈149 млн км): L ≈ 375 000 км — сравнение с
    геоцентрическим расстоянием (384 400 км среднее) определяет,
    полное затмение или кольцевое."""
    return r_body_km * d_body_sun_km / (r_sun_km - r_body_km)


def moon_shadow_check() -> dict:
    """Тень Луны при среднем расстоянии: ~375 000 км.

    Меньше среднего расстояния Луны (384 400) → в апогее тень не
    доходит до Земли → кольцевое затмение; в перигее (356 500) —
    доходит (полное/гибридное)."""
    L = shadow_cone_length(1737.4, 1.496e8)
    return dict(
        cone_km=L,
        mean_distance_km=384400.0,
        perigee_km=356500.0,
        apogee_km=406700.0,
        reaches_earth_at_mean=L > 384400.0,
        note="L = R_b·D/(R_s−R_b); доля кольцевых затмений "
        "выше, чем полных, именно из-за этого соотношения",
    )


def eclipse_width_beta(kind: str = "solar") -> dict:
    """Предельная широта Луны от узла для затмения (β-лимит, градусы).

    Солнечное: полоса зависит от параллакса; типичные лимиты:
    центральное ~1.55°, частное ~1.85° (Meeus, «Elements of Solar
    Eclipses»); лунное: полутень до ~1.0° от узла."""
    limits = dict(solar_central=1.55, solar_partial=1.85, lunar=1.00)
    if kind not in limits:
        raise KeyError(f"тип {kind} не в solar/lunar")
    return dict(
        beta_limit_deg=limits[kind], reference="Meeus, Mathematical Astronomy Morsels, гл. 54"
    )


def upcoming_window(days_since_new_moon: float, beta_deg: float) -> dict:
    """Оценка окна затмения: фаза близка к новолунию и |β| в лимите.

    Честная пометка: точное предсказание требует эфемерид
    (VSOP/ELP2000); здесь — геометрический фильтр."""
    phase_frac = (days_since_new_moon % SYNODIC_D) / SYNODIC_D
    near_new = abs(phase_frac) < 0.03 or abs(phase_frac - 1.0) < 0.03
    lim = eclipse_width_beta("solar_partial")["beta_limit_deg"]
    beta_ok = abs(beta_deg) < lim
    return dict(
        phase_frac=phase_frac,
        near_new_moon=near_new,
        beta_ok=beta_ok,
        possible=(near_new and beta_ok),
    )


def self_check() -> dict:
    """Сарос точен; затменный год 346.62; сезон 173.31; тень Луны."""
    sar = saros_days()
    saros_ok = abs(sar - 6585.32) < 0.01
    ey = eclipse_year_days()
    ey_ok = abs(ey - 346.62) < 0.1
    season = eclipse_season_spacing()
    season_ok = abs(season - 173.31) < 0.1
    shadow = moon_shadow_check()
    shadow_ok = 370000.0 < shadow["cone_km"] < 380000.0
    # сарос = 223 синодических = 242 драконических − 239 аномалистических
    # (проверка согласованности драконического месяца)
    draconic_implied = 6585.32 / 242.0
    drac_ok = abs(draconic_implied - DRACONIC_D) < 0.01
    return dict(
        saros_days=sar,
        saros_ok=saros_ok,
        eclipse_year=round(ey, 3),
        ey_ok=ey_ok,
        season_spacing=round(season, 3),
        season_ok=season_ok,
        shadow_km=round(shadow["cone_km"]),
        shadow_ok=shadow_ok,
        draconic_implied=round(draconic_implied, 6),
        drac_ok=drac_ok,
        all_ok=saros_ok and ey_ok and season_ok and shadow_ok and drac_ok,
        note="Сарос: 223 синодич. ≈ 242 драконич. ≈ 239 аномалистич.; "
        "затменный год из регрессии узлов (18.61 лет)",
    )
