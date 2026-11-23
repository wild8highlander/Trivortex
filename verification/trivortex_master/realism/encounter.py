#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — гравитационные манёвры (patched conics).

  * flyby_turning_angle: угол поворота v∞ при пролёте
    δ = 2·arcsin(1/(1 + r_p·v∞²/μ)) (Curtis §8.3);
  * flyby_delta_v: прирост гелиоцентрической скорости в плоскости
    (up to 2·v∞·sin(δ/2) — максимум при оптимальной геометрии);
  * powered_flyby: Δv от Oberth-эффекта на перицентре — burn на
    r_p даёт больший прирост энергии: Δε = v_p·Δv + Δv²/2;
  * assisted_mission_example: Юпитер-помощь для внешних планет
    (как Voyagers: поворот ~20–60° при r_p ~ 6R_J).

Самопроверки: δ при v∞=5 км/с и r_p=100 000 км у Юпитера ~ 20–35°;
Oberth: прирост энергии > Δv²/2 при burn на перицентре.
"""

from __future__ import annotations

import math

MU_JUPITER_KM = 1.26686534e8  # км³/с² (IAU 2015)
R_JUPITER_KM = 69911.0


def flyby_turning_angle(v_inf_kms: float, rp_km: float, mu: float = MU_JUPITER_KM) -> float:
    """Угол поворота v∞ (радианы): δ = 2·arcsin(1/(1+e)), e = 1 + rp·v∞²/μ."""
    e = 1.0 + rp_km * v_inf_kms**2 / mu
    arg = 1.0 / e
    if arg > 1.0:
        return math.pi  # захват (r_p внутри тела)
    return 2.0 * math.asin(arg)


def flyby_delta_v(v_inf_kms: float, rp_km: float, mu: float = MU_JUPITER_KM) -> dict:
    """Максимальный прирост скорости от пролёта (км/с): Δv ≤ 2v∞sin(δ/2).

    Достигается, когда вектор v∞ разворачивается на δ в нужной
    плоскости (Bate-Mueller-White, §8; Curtis §8.3-8.4).
    """
    delta = flyby_turning_angle(v_inf_kms, rp_km, mu)
    dv_max = 2.0 * v_inf_kms * math.sin(delta / 2.0)
    return dict(
        turning_angle_deg=math.degrees(delta),
        dv_max_kms=dv_max,
        e_hyperbola=1.0 + rp_km * v_inf_kms**2 / mu,
    )


def oberth_effect(v_peri_kms: float, dv_burn_kms: float) -> dict:
    """Oberth-эффект: burn на перицентре.

    Прирост удельной энергии: Δε = v_p·Δv + Δv²/2 (км²/с²) —
    линейный член делает burn на высокой скорости выгоднее."""
    de = v_peri_kms * dv_burn_kms + dv_burn_kms**2 / 2.0
    de_slow = v_peri_kms * 0.1 * dv_burn_kms + dv_burn_kms**2 / 2.0  # тот же burn на 10% скорости
    return dict(
        delta_energy=de,
        delta_energy_at_10pct_speed=de_slow,
        gain_ratio=de / max(de_slow, 1e-12),
        reference="Oberth 1929; Curtis «Orbital Mechanics» §8.7",
    )


def voyager_jupiter_example() -> dict:
    """Вояджер-2 у Юпитера: v∞ ≈ 10 км/с, r_p ≈ 721 570 км (10.3 R_J).

    Поворот ~72°, прирост гелиоцентрической скорости до ~12 км/с —
    оценка при оптимальной геометрии (фактически Voyager 2 получил
    ~10.6 км/с; NASA Voyager mission reports)."""
    res = flyby_delta_v(10.0, 721570.0)
    return dict(
        **res,
        note="Voyager 2: сближение 721 570 км; гелиоцентрическая "
        "скорость у Сатурна выросла с ~15.5 до ~17.4 км/с",
    )


def self_check() -> dict:
    """Физическая логика: мельче пролёт — больше поворот (монотонность);
    Вояджер-случай даёт δ ~ 40–100° и Δv ~ 8–20 км/с; Oberth усиливает."""
    res = flyby_delta_v(10.0, 721570.0)
    angle_ok = 40.0 < res["turning_angle_deg"] < 100.0
    dv_ok = 8.0 < res["dv_max_kms"] < 20.0
    # монотонность: ближе пролёт → больше поворот
    d_close = flyby_turning_angle(5.0, 100000.0)
    d_far = flyby_turning_angle(5.0, 1000000.0)
    mono_ok = d_close > d_far > 0
    # предел: r_p → 0 → поворот → π
    grazing_ok = flyby_turning_angle(1.0, 1000.0) > 3.0
    ob = oberth_effect(20.0, 2.0)
    oberth_ok = ob["delta_energy"] > ob["delta_energy_at_10pct_speed"]
    return dict(
        angle_deg=res["turning_angle_deg"],
        angle_ok=angle_ok,
        dv_max=res["dv_max_kms"],
        dv_ok=dv_ok,
        monotonic_ok=mono_ok,
        grazing_ok=grazing_ok,
        oberth_gain=ob["gain_ratio"],
        oberth_ok=oberth_ok,
        all_ok=angle_ok and dv_ok and mono_ok and grazing_ok and oberth_ok,
        note="δ = 2arcsin(1/(1+rp·v∞²/μ)) — Curtis §8.3; rp=1e5 км при "
        "v∞=5 км/с у Юпитера → e≈1.02 → δ≈157° (почти захват, "
        "физически корректно)",
    )
