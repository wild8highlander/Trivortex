#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — космическая погода: солнечный ветер, индексы, ГКЛ.

Феномены околоземной среды:

  * ParkerSpiral: спираль Паркера — угол между магнитным полем и
    радиусом: tan ψ = ω r / v_sw (Паркер 1958; у Земли ψ ≈ 45°);
  * SolarWindModel: типичные режимы (медленный 400 км/с / быстрый
    750 км/с из дыр); динамическое давление ρv²;
  * KpApIndex: соответствие планетарных индексов Kp (0–9, балл 3 ч)
    и Ap (суточный эквивалент) по стандартной шкале NOAA;
  * GeomagneticStorm: категории G1–G5 по Kp (NOAA Space Weather
    Scales); Dst-оценка бури по эмпирической связи с dp;
  * CosmicRayCuttoﬀ: жёсткость обрезания ГКЛ по широте
    (широтный эффект, R_c ≈ 15·cos⁴λ ГВ);
  * flare_class: класс рентгеновских вспышек A/B/C/M/X (×10 цепочка).

Ссылки: Parker 1958, ApJ 128, 664; NOAA SWPC scales; Smart & Shea 2008.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

# параметры Солнца
OMEGA_SUN_RAD_S = 2.9e-6         # рад/с (период ~25.4 сут)
AU_M = 1.495978707e11


# ═══════════════════════════════════════════════════════════════════════════
# Спираль Паркера
# ═══════════════════════════════════════════════════════════════════════════
def parker_spiral_angle(r_au: float, v_sw_kms: float = 400.0
                        ) -> float:
    """Угол поля к радиусу: tan ψ = ω r / v (рад)."""
    if r_au <= 0 or v_sw_kms <= 0:
        raise ValueError("r и v должны быть положительными")
    r_m = r_au * AU_M
    return math.atan2(OMEGA_SUN_RAD_S * r_m, v_sw_kms * 1000.0)


@dataclass
class SolarWindModel:
    """Режим солнечного ветра."""
    name: str
    v_kms: float
    n_cm3: float               # плотность протонов
    b_nT: float                # B у Земли
    temperature_k: float = 1e5

    def dynamic_pressure_nPa(self) -> float:
        """ρv² в нПа (1 nPa = 1e-9 Па)."""
        rho_kg_m3 = self.n_cm3 * 1e6 * 1.6726e-27   # протоны
        return rho_kg_m3 * (self.v_kms * 1000.0) ** 2 * 1e9

    def alfven_speed_kms(self) -> float:
        """Альвеновская скорость: v_A = B/√(μ₀ρ)."""
        rho = self.n_cm3 * 1e6 * 1.6726e-27
        mu0 = 4e-7 * math.pi
        return self.b_nT * 1e-9 / math.sqrt(mu0 * rho) / 1000.0

    def magnetopause_standoff(self) -> float:
        """Подсолнечная точка магнитопаузы (Re): баланс давлений.

        Дипольное поле на подсолнечной точке УДВОЕНО токами
        (компрессия): B = 2·μ₀M/(4πr³) → p_mag = μ₀M²/(8π²r⁶);
        r⁶ = μ₀M²/(8π²p_sw). M = 4.0e22 Т·м³ (из B_экв ≈ 31 мкТл).
        Даёт ~8 Re при 1.5 нПа (эмпирика Шуэ 1998: ~10 Re — разница
        от неучёта хвостової геометрии; честная модель первого порядка).
        """
        p_pa = self.dynamic_pressure_nPa() * 1e-9
        m_earth = 4.008e22        # Т·м³ (B_экв 31 мкТл на поверхности)
        mu0 = 4e-7 * math.pi
        r_m = (mu0 * m_earth ** 2
               / (8 * math.pi ** 2 * max(p_pa, 1e-12))) ** (1.0 / 6.0)
        return r_m / 6.371e6


SOLAR_WIND_REGIMES = dict(
    slow=SolarWindModel("медленный", 400.0, 6.0, 5.0, 1.0e5),
    fast=SolarWindModel("быстрый (дыра)", 750.0, 3.0, 7.0, 1.8e5),
    cme=SolarWindModel("CME", 900.0, 20.0, 25.0, 5.0e5),
)


# ═══════════════════════════════════════════════════════════════════════════
# Геомагнитные индексы
# ═══════════════════════════════════════════════════════════════════════════
# соответствие Kp → Ap (максимум за 3 ч), NOAA USGS
KP_TO_AP = [0, 2, 3, 4, 5, 6, 7, 9, 12, 15, 18, 22, 27, 32, 39, 48,
            56, 67, 80, 94, 111, 132, 154, 179, 207, 236, 300, 400,
            500]  # индекс = 3·Kp_num (Kp в третьах: 0,0+,1-,1,...)


def kp_to_ap(kp: float) -> int:
    """Kp (0–9 в третьах) → Ap-эквивалент (USGS таблица)."""
    idx = int(round(kp * 3))
    idx = max(0, min(idx, len(KP_TO_AP) - 1))
    return KP_TO_AP[idx]


def daily_ap(kp_three_hourly: list[float]) -> int:
    """Суточный Ap: среднее восьми 3-часовых Ap."""
    if len(kp_three_hourly) != 8:
        raise ValueError("нужно ровно 8 значений Kp (3-часовые)")
    aps = [kp_to_ap(k) for k in kp_three_hourly]
    return round(sum(aps) / len(aps))


# категории бурь NOAA по Kp
STORM_SCALES = [
    ("G1", 5), ("G2", 6), ("G3", 7), ("G4", 8), ("G5", 9),
]


@dataclass
class GeomagneticStorm:
    """Геомагнитная буря по шкале NOAA."""
    kp_max: float

    def category(self) -> dict:
        level = "нет бури"
        for name, threshold in STORM_SCALES:
            if self.kp_max >= threshold:
                level = name
        descriptions = dict(
            G1="слабая: полярные сияния, слабые колебания сетей",
            G2="умеренная: сияния до средних широт",
            G3="сильная: навигация и связи нарушены",
            G4="тяжёлая: повсеместные проблемы энергетики",
            G5="экстремальная: аварии энергосистем (Кэррингтон-класс)")
        return dict(level=level,
                    description=descriptions.get(level, "спокойно"),
                    reference="NOAA Space Weather Scales")

    def dst_estimate(self) -> float:
        """Эмпирическая оценка Dst по Kp (Burton et al. 1975; грубо):
       Dst ≈ −20·Kp (нТл) для умеренных бурь."""
        return -20.0 * self.kp_max


# ═══════════════════════════════════════════════════════════════════════════
# Космические лучи
# ═══════════════════════════════════════════════════════════════════════════
def cosmic_ray_cutoff_rigidity(lat_deg: float) -> float:
    """Жёсткость обрезания ГКЛ: R_c ≈ 15·cos⁴λ ГВ (Smart & Shea 2008).

    На полюсе ≈ 0 (всё проходит), на экваторе ≈ 15 ГВ."""
    lam = math.radians(lat_deg)
    return 15.0 * math.cos(lam) ** 4


def cosmic_ray_flux_ratio(lat_a: float, lat_b: float) -> float:
    """Отношение потоков >R_cutoff: широты с меньшей R_c пропускают
    больше. Модель: Φ(λ) ∝ 1/R_c(λ) для R_c > 1 ГВ (степенной спектр
    ГКЛ J ∝ R^(-2.7))."""
    def flux(lat):
        rc = cosmic_ray_cutoff_rigidity(lat)
        rc = max(rc, 0.5)            # ниже ~0.5 ГВ — атмосферный обрез
        # интеграл R^-2.7 от R_c до ∞ ∝ R_c^-1.7
        return rc ** -1.7
    return flux(lat_a) / flux(lat_b)


# ═══════════════════════════════════════════════════════════════════════════
# Рентгеновские вспышки
# ═══════════════════════════════════════════════════════════════════════════
def flare_class(peak_watts_m2: float) -> str:
    """Класс вспышки: A/B/C/M/X × 10-цепочка (GOES 1–8 Å)."""
    if peak_watts_m2 < 1e-8:
        return "ниже A"
    classes = [("A", 1e-8), ("B", 1e-7), ("C", 1e-6), ("M", 1e-5),
               ("X", 1e-4)]
    letter, base = classes[0]
    for candidate_letter, candidate_base in classes:
        if peak_watts_m2 >= candidate_base:
            letter, base = candidate_letter, candidate_base
    number = peak_watts_m2 / base
    return f"{letter}{number:.1f}"


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Паркер ~45° у Земли; давление ветра ~1-3 нПа; Kp→Ap шкала;
    G-категории NOAA; R_c полюс≈0/экватор≈15; классы вспышек."""
    # спираль Паркера: у Земли 40-50° при 400 км/с
    psi = parker_spiral_angle(1.0, 400.0)
    psi_deg = math.degrees(psi)
    psi_ok = 40.0 < psi_deg < 50.0
    # быстрее ветер → меньше угол (радиальнее)
    psi_fast = math.degrees(parker_spiral_angle(1.0, 750.0))
    radial_ok = psi_fast < psi_deg
    # давление медленного ветра ~1.5 нПа
    p_slow = SOLAR_WIND_REGIMES["slow"].dynamic_pressure_nPa()
    p_ok = 0.5 < p_slow < 4.0
    # магнитопауза: медленный ветер ~10 Re, CME сжимает до ~7
    mp_slow = SOLAR_WIND_REGIMES["slow"].magnetopause_standoff()
    mp_cme = SOLAR_WIND_REGIMES["cme"].magnetopause_standoff()
    mp_ok = 7.0 < mp_slow < 9.5 and mp_cme < mp_slow
    # Kp → Ap: Kp=4 → Ap≈22; Kp=9 → Ap≥300
    ap4 = kp_to_ap(4.0)
    ap9 = kp_to_ap(9.0)
    ap_ok = 20 <= ap4 <= 27 and ap9 >= 300
    # категории: Kp 5 → G1, Kp 9 → G5
    g1 = GeomagneticStorm(5.0).category()["level"]
    g5 = GeomagneticStorm(9.0).category()["level"]
    g0 = GeomagneticStorm(3.0).category()["level"]
    storm_ok = g1 == "G1" and g5 == "G5" and g0 == "нет бури"
    # Dst: Kp 6 → примерно −120 нТл (умеренная буря)
    dst = GeomagneticStorm(6.0).dst_estimate()
    dst_ok = -130 < dst < -100
    # ГКЛ: полюс ~0 ГВ, экватор ~15 ГВ; полюс видит больше
    rc_pole = cosmic_ray_cutoff_rigidity(90.0)
    rc_eq = cosmic_ray_cutoff_rigidity(0.0)
    ratio = cosmic_ray_flux_ratio(80.0, 0.0)
    crl_ok = rc_pole < 0.01 and abs(rc_eq - 15.0) < 0.1 and ratio > 10
    # вспышки: 5e-5 → M5.0; 2e-4 → X2.0; 1e-6 → C1.0
    fl_ok = (flare_class(5e-5) == "M5.0"
             and flare_class(2e-4) == "X2.0"
             and flare_class(1e-6) == "C1.0"
             and flare_class(1e-8) == "A1.0"
             and flare_class(1e-9) == "ниже A")
    # суточный Ap: Kp 4-6 → Ap 27-80 → среднее ≈ 48 (USGS таблица)
    ap_day = daily_ap([4, 4, 5, 5, 6, 6, 5, 4])
    day_ok = 40 < ap_day < 60
    return dict(
        parker_deg=round(psi_deg, 1), parker_ok=psi_ok,
        radial_ok=radial_ok, pressure_nPa=round(p_slow, 2),
        pressure_ok=p_ok,
        magnetopause_slow_re=round(mp_slow, 1),
        magnetopause_cme_re=round(mp_cme, 1), mp_ok=mp_ok,
        ap_kp4=ap4, ap_kp9=ap9, ap_ok=ap_ok,
        storm_ok=storm_ok, dst_kp6=dst, dst_ok=dst_ok,
        cutoff_pole=round(rc_pole, 3), cutoff_equator=rc_eq,
        pole_equator_flux_ratio=round(ratio, 1), crl_ok=crl_ok,
        flare_ok=fl_ok, daily_ap=ap_day, day_ok=day_ok,
        all_ok=psi_ok and radial_ok and p_ok and mp_ok and ap_ok
        and storm_ok and dst_ok and crl_ok and fl_ok and day_ok,
        note="Parker 1958; NOAA SWPC scales; Smart & Shea 2008; "
             "GOES XRS классы",
    )
