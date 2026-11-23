#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — проектирование межпланетных миссий.

  * hohmann_delta_v: двухимпульсный переход между круговыми орбитами
    (Δv₁ = √(μ/r₁)·(√(2r₂/(r₁+r₂)) − 1), Δv₂ аналог при r₂);
  * porkchop_grid: матрица Δv по сетке (дата вылета × дата прилёта)
    через Ламберт-решатель (lab.kepler.lambert) — данные для
    классического «porkchop»-графика;
  * delta_v_budget: бюджет миссии (rocket equation Циолковского
    Isp·ln(m₀/m_f), многоступенчатость);
  * launch_window_c3: характеристическая энергия C3 = v∞² для
    оптимального окна (Hohmann-оценка Земля→цель).

Самопроверки: Земля→Марс Hohmann Δv ≈ 5.6 км/с (литература:
2.94 + 2.65); Циолковский: при Isp=450 с и Δv=9.4 км/с масса ≈ e^{−2.13}.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

AU_M = 1.495978707e11
MU_SUN = 1.32712440018e11        # км³/с²
G0 = 9.80665                     # м/с²


def hohmann_delta_v(r1_km: float, r2_km: float,
                    mu: float = MU_SUN) -> dict:
    """Δv двухимпульсного гоманова перехода (км/с)."""
    v1 = math.sqrt(mu / r1_km)
    v2 = math.sqrt(mu / r2_km)
    a_t = 0.5 * (r1_km + r2_km)
    v_peri = math.sqrt(mu * (2.0 / r1_km - 1.0 / a_t))
    v_apo = math.sqrt(mu * (2.0 / r2_km - 1.0 / a_t))
    dv1 = abs(v_peri - v1)
    dv2 = abs(v2 - v_apo)
    tof_days = math.pi * math.sqrt(a_t ** 3 / mu) / 86400.0
    return dict(dv1=dv1, dv2=dv2, dv_total=dv1 + dv2,
                transfer_time_days=tof_days, a_transfer_km=a_t)


def earth_to_mars_check() -> dict:
    """Классика: Земля→Марс Hohmann Δv ≈ 5.6 км/с, полёт ~259 сут."""
    r_earth = 1.496e8          # км
    r_mars = 1.524 * 1.496e8
    res = hohmann_delta_v(r_earth, r_mars)
    return dict(dv1=res["dv1"], dv2=res["dv2"], dv_total=res["dv_total"],
                tof_days=res["transfer_time_days"],
                expected_dv=5.6, expected_tof=259,
                dv_ok=abs(res["dv_total"] - 5.6) < 0.25,
                tof_ok=abs(res["transfer_time_days"] - 259) < 12)


def launch_window_c3(r_earth_km: float = 1.496e8,
                     r_target_km: float = 1.524 * 1.496e8,
                     mu: float = MU_SUN) -> float:
    """C3 = v∞² (км²/с²) на выходе из сферы действия Земли.

    v∞ = |v_transfer(peri) − v_earth| для гоманова окна."""
    res = hohmann_delta_v(r_earth_km, r_target_km, mu)
    v_inf = res["dv1"]
    return v_inf * v_inf


def porkchop_grid(r_earth_km: float, r_target_km: float,
                  launch_offsets_days: list[float],
                  tof_days_list: list[float],
                  phase_rate_deg_day: float,
                  mu: float = MU_SUN) -> dict:
    """Матрица Δv (км/с) по (смещение вылета × время полёта).

    Позиции планет: Земля на 0°, цель на phase0 + rate·t; угол
    переноса Δθ = φ_target(t_launch+tof) − φ_earth(t_launch+tof).
    Ламберт-решатель даёт v1, v2 → Δv = |v1 − v_earth| + |v2 − v_target|
    (без учёта v∞ гравитации планет — гелиоцентрическая оценка).
    """
    from lab.kepler import lambert

    def position(r_km, angle_deg):
        ang = math.radians(angle_deg)
        return (r_km * math.cos(ang), r_km * math.sin(ang))

    def circular_speed(r_km):
        return math.sqrt(mu / r_km)

    grid = []
    best = dict(dv=float("inf"), launch=0.0, tof=0.0)
    for dl in launch_offsets_days:
        for tof in tof_days_list:
            t_dep = dl
            t_arr = dl + tof
            phi_e_dep = 360.0 * t_dep / 365.256      # Земля от 0°
            phi_t_dep = phase_rate_deg_day * t_dep    # цель в t=0 на 0°
            phi_e_arr = 360.0 * t_arr / 365.256
            phi_t_arr = phase_rate_deg_day * t_arr
            d_theta = (phi_t_arr - phi_e_arr) % 360.0
            r1v = position(r_earth_km, phi_e_dep)
            r2v = position(r_target_km, phi_t_arr)
            dt_s = tof * 86400.0
            sol = lambert((r1v[0], r1v[1], 0.0), (r2v[0], r2v[1], 0.0),
                          dt_s, mu)
            if sol is None:
                grid.append(dict(launch=dl, tof=tof, dv=None))
                continue
            v1, v2 = sol
            v_e = circular_speed(r_earth_km)
            v_t = circular_speed(r_target_km)
            v_e_vec = (-v_e * math.sin(math.radians(phi_e_dep)),
                       v_e * math.cos(math.radians(phi_e_dep)))
            v_t_vec = (-v_t * math.sin(math.radians(phi_t_arr)),
                       v_t * math.cos(math.radians(phi_t_arr)))
            dv1 = math.sqrt((v1[0] - v_e_vec[0]) ** 2
                            + (v1[1] - v_e_vec[1]) ** 2)
            dv2 = math.sqrt((v2[0] - v_t_vec[0]) ** 2
                            + (v2[1] - v_t_vec[1]) ** 2)
            dv = dv1 + dv2
            grid.append(dict(launch=dl, tof=tof, dv=dv))
            if dv < best["dv"]:
                best = dict(dv=dv, launch=dl, tof=tof)
    return dict(grid=grid, best=best, n_cells=len(grid),
                note="гелиоцентрическая оценка без гравитации планет; "
                     "классический porkchop (Berlin 1967)")


@dataclass
class Stage:
    """Ступень ракеты."""
    isp_s: float               # удельный импульс, с
    mass_ratio: float          # m0/mf (полная/сухая)


def tsiolkovsky(isp_s: float, mass_ratio: float) -> float:
    """Δv ступени: Isp·g₀·ln(m₀/m_f) (м/с)."""
    if mass_ratio <= 1.0:
        raise ValueError("m₀/m_f должно быть > 1")
    return isp_s * G0 * math.log(mass_ratio)


def multi_stage_delta_v(stages: list[Stage]) -> float:
    """Суммарный Δv многоступенчатой ракеты (м/с)."""
    return sum(tsiolkovsky(s.isp_s, s.mass_ratio) for s in stages)


def delta_v_budget(dv_required_m_s: float, isp_s: float = 450.0
                   ) -> dict:
    """Доля топлива: m_f/m₀ = exp(−Δv/(Isp·g₀))."""
    frac = math.exp(-dv_required_m_s / (isp_s * G0))
    return dict(mass_fraction=frac,
                propellant_percent=100.0 * (1.0 - frac),
                isp_s=isp_s,
                note="Циолковский: при Isp 450 с и Δv 9.4 км/с "
                     "сухой остаток ≈ 12%")


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Гоманн Земля→Марс (5.6 км/с, 259 сут); Циолковский; C3."""
    em = earth_to_mars_check()
    # Циолковский: Δv=9.4 км/с при Isp=450 с → m_f/m₀ ≈ e^(-9400/4413)
    frac = delta_v_budget(9400.0, isp_s=450.0)["mass_fraction"]
    tsio_ok = abs(frac - math.exp(-9400.0 / (450.0 * G0))) < 1e-12
    c3 = launch_window_c3()
    c3_ok = 6.0 < c3 < 12.0      # литература: C3 Марса ~8-12 км²/с²
    return dict(
        dv_total=em["dv_total"], dv_ok=em["dv_ok"],
        tof_days=em["tof_days"], tof_ok=em["tof_ok"],
        tsiolkovsky_ok=tsio_ok,
        c3_kms2=c3, c3_ok=c3_ok,
        all_ok=em["dv_ok"] and em["tof_ok"] and tsio_ok and c3_ok,
        note="Hohmann: классика; C3 = v∞² на оптимальном окне",
    )
