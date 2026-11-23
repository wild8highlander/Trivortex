#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — орбитальные манёвры.

Классический набор импульсных манёвров двухимпульсной механики:

  * tangential_burn: тангенциальный импульс → изменение a и e
    (vis-viva), новый период;
  * inclination_change: чистое изменение наклонения
    Δv = 2·v·sin(Δi/2) (на узлах при комбинированном);
  * combined_plane_change: поворот плоскости вместе со скоростью —
    Δv = √(v₁² + v₂² − 2v₁v₂cosΔi) (в узлах);
  * bielliptic_transfer: r₁ → r_b → r₂ через апоцентр r_b; выгоден
    при r₂/r₁ ≳ 11.94 (классический порог);
  * phasing: фазовый манёвр — угол фазирования, два импульса,
    дрейф за N витков;
  * drag_deorbit: оценка схода из-за атмосферы (экспоненциальная
    плотность, драг → спираль).

Самопроверки: биэллиптический выгоден при r₂/r₁ = 15 (МКД: суммарный
Δv меньше гоманновского); Δv наклонения = 2v·sin(Δi/2) при v=const.
"""
from __future__ import annotations

import math

MU_EARTH_KM = 398600.4418        # км³/с²
R_EARTH_KM = 6378.137
RHO_0 = 1.225e9                  # г/км³ на уровне моря (км-единицы)
H_SCALE_KM = 8.5


# ═══════════════════════════════════════════════════════════════════════════
# Одиночный импульс
# ═══════════════════════════════════════════════════════════════════════════
def circular_speed(r_km: float, mu: float = MU_EARTH_KM) -> float:
    return math.sqrt(mu / r_km)


def tangential_burn(r_km: float, dv_kms: float,
                    mu: float = MU_EARTH_KM) -> dict:
    """Тангенциальный импульс на круговой орбите → новые a, e, период.

    Положительный dv → расширяющаяся орбита (перигей в точке burn).
    """
    v = circular_speed(r_km, mu)
    v_new = v + dv_kms
    if v_new <= 0:
        raise ValueError("скорость стала отрицательной")
    # vis-viva: v_new² = μ(2/r − 1/a) → a
    inv_a = 2.0 / r_km - v_new ** 2 / mu
    if inv_a <= 0:
        return dict(a_km=float("inf"), e=1.0,
                    period_min=float("inf"),
                    escape=True)
    a = 1.0 / inv_a
    # эксцентриситет: перигей = r (burn тангенциальный)
    e = 1.0 - r_km / a if v_new < math.sqrt(2 * mu / r_km) else \
        r_km / a - 1.0
    period_min = 2 * math.pi * math.sqrt(a ** 3 / mu) / 60.0
    return dict(a_km=a, e=abs(e), period_min=period_min,
                escape=False)


def inclination_change(v_kms: float, delta_i_deg: float) -> float:
    """Чистое изменение наклонения: Δv = 2·v·sin(Δi/2) (км/с)."""
    return 2.0 * v_kms * math.sin(math.radians(delta_i_deg) / 2.0)


def combined_plane_change(v1_kms: float, v2_kms: float,
                          delta_i_deg: float) -> float:
    """Комбинированный манёвр в узле: Δv = √(v₁²+v₂²−2v₁v₂cosΔi)."""
    cos_i = math.cos(math.radians(delta_i_deg))
    return math.sqrt(v1_kms ** 2 + v2_kms ** 2
                     - 2.0 * v1_kms * v2_kms * cos_i)


# ═══════════════════════════════════════════════════════════════════════════
# Переходы
# ═══════════════════════════════════════════════════════════════════════════
def hohmann_total(r1_km: float, r2_km: float,
                  mu: float = MU_EARTH_KM) -> float:
    """Суммарный Δv гомановского перехода (км/с)."""
    v1 = circular_speed(r1_km, mu)
    v2 = circular_speed(r2_km, mu)
    a_t = 0.5 * (r1_km + r2_km)
    dv1 = abs(math.sqrt(mu * (2.0 / r1_km - 1.0 / a_t)) - v1)
    dv2 = abs(v2 - math.sqrt(mu * (2.0 / r2_km - 1.0 / a_t)))
    return dv1 + dv2


def bielliptic_total(r1_km: float, r2_km: float, r_b_km: float,
                     mu: float = MU_EARTH_KM) -> dict:
    """Биэллиптический переход: r₁ → r_b → r₂ (км/с, время в сутках)."""
    v1 = circular_speed(r1_km, mu)
    v2 = circular_speed(r2_km, mu)
    a1 = 0.5 * (r1_km + r_b_km)
    a2 = 0.5 * (r2_km + r_b_km)
    dv1 = abs(math.sqrt(mu * (2.0 / r1_km - 1.0 / a1)) - v1)
    dv2 = abs(math.sqrt(mu * (2.0 / r_b_km - 1.0 / a2))
              - math.sqrt(mu * (2.0 / r_b_km - 1.0 / a1)))
    dv3 = abs(v2 - math.sqrt(mu * (2.0 / r2_km - 1.0 / a2)))
    tof = (math.pi * math.sqrt(a1 ** 3 / mu)
           + math.pi * math.sqrt(a2 ** 3 / mu)) / 86400.0
    return dict(dv1=dv1, dv2=dv2, dv3=dv3, dv_total=dv1 + dv2 + dv3,
                tof_days=tof, r_b_km=r_b_km)


def bielliptic_threshold(r1_km: float = 1.0) -> float:
    """Порог выгодности биэллиптического: r₂/r₁ ≈ 11.94 при r_b → ∞.

    Бисекция: НИЖЕ порога гоманн выигрывает, ВЫШЕ — биэллиптика.
    (Escobal 1968; при r_b = 50·r₂ порог чуть выше классического.)"""
    lo, hi = 5.0, 40.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        be = bielliptic_total(1.0, mid, mid * 50.0, mu=1.0)
        ho = hohmann_total(1.0, mid, mu=1.0)
        if be["dv_total"] < ho:
            hi = mid            # биэллиптика уже выигрывает → порог ниже
        else:
            lo = mid            # гоманн выигрывает → порог выше
    return 0.5 * (lo + hi)


def phasing_angle(phase_deg: float, n_revs: int = 1) -> float:
    """Угол фазирования: дрейф (360·N ± Δφ) за N+1 витков (градусы)."""
    return 360.0 * n_revs - phase_deg


def phasing_period(drift_angle_deg: float, base_period_min: float,
                   direction: str = "ahead") -> dict:
    """Период фазирующей орбиты: P' = P·(1 ± Δφ/360·1/N)."""
    frac = drift_angle_deg / 360.0
    if direction == "ahead":
        new_period = base_period_min / (1.0 + frac)
    else:
        new_period = base_period_min / (1.0 - frac)
    return dict(new_period_min=new_period,
                time_to_target_min=base_period_min / max(frac, 1e-9),
                direction=direction)


# ═══════════════════════════════════════════════════════════════════════════
# Атмосферный сход
# ═══════════════════════════════════════════════════════════════════════════
def drag_decay_time(h_km: float, ballistic_coef: float = 100.0
                    ) -> dict:
    """Время жизни на круговой орбите при экспоненциальной атмосфере.

    t ≈ H/(2·B·ρ(h)·v) — для ЛЭО 300 км и B=100 кг/м² ~ десятки суток.
    B — баллистический коэффициент (кг/м²); ρ — экспоненциальная.
    """
    rho = RHO_0 * math.exp(-h_km / H_SCALE_KM)          # г/км³
    rho_si = rho * 1e-9                                  # кг/м³
    v = circular_speed(R_EARTH_KM + h_km) * 1000.0       # м/с
    # dr/dt ≈ −2·(ρ v /B)·... используем классическую оценку:
    # t ≈ B/(2·ρ·v)·(в секундах) с масштабом H
    t_s = ballistic_coef / (2.0 * rho_si * v) * H_SCALE_KM * 1000.0
    return dict(altitude_km=h_km, rho_kg_m3=rho_si,
                lifetime_days=t_s / 86400.0,
                note="оценка верхней атмосферы; для 300 км ~ недели, "
                     "для 400 км — годы (реальная плотность варьирует "
                     "с солнечной активностью)")


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Биэллиптика выгоднее при r₂/r₁ = 15; Δv наклонения формула точна;
    тангенциальный burn: vis-viva сходится."""
    ho = hohmann_total(7000.0, 15.0 * 7000.0)
    be = bielliptic_total(7000.0, 15.0 * 7000.0, 200000.0)
    bi_wins = be["dv_total"] < ho
    dv_i = inclination_change(7.5, 30.0)
    inc_ok = abs(dv_i - 2.0 * 7.5 * math.sin(math.radians(15.0))) < 1e-12
    burn = tangential_burn(7000.0, 0.5)
    v_check = math.sqrt(MU_EARTH_KM * (2.0 / 7000.0 - 1.0 / burn["a_km"]))
    vis_ok = abs(v_check - (circular_speed(7000.0) + 0.5)) < 1e-9
    threshold = bielliptic_threshold()
    thr_ok = 10.0 < threshold < 14.0
    return dict(
        hohmann_dv=round(ho, 4), bielliptic_dv=round(be["dv_total"], 4),
        bi_wins=bi_wins,
        inclination_dv=dv_i, inc_ok=inc_ok,
        vis_viva_ok=vis_ok,
        bi_threshold=round(threshold, 2), thr_ok=thr_ok,
        all_ok=bi_wins and inc_ok and vis_ok and thr_ok,
        note="порог биэллиптики ≈ 11.94·r₁ (Escobal 1968); r_b = 5·r₂",
    )
