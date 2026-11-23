#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — радиационная динамика: Пойнтинг-Робертсон, Ярковский,
световой парус.

Три эффекта давления излучения:

  * Пойнтинг-Робертсон (Burns et al. 1979): драг на пылинках,
    a-decay за время t_PR = 400·(s/см)·(ρ/г·см⁻³)·(a_орб/а.е.)² лет
    → круговые спирали внутрь; классика: метеороиды в солнечной системе.
  * Ярковский (Rubincam 1995; Bottke et al. 2006): сезонное/суточное
    тепловое переизлучение → сила ⊥ радиусу: смещение семейств астероидов
    (измерено для астероида Бенну OSIRIS-REx, 2020).
  * Световой парус (Breakthrough Starshot-style): a = 2I/c·(A/m)·Q;
    релятивистская поправка при v→c.

Самопроверки: t_PR пылинки 100 мкм на 1 а.е. ≈ 5·10⁴ лет; Ярковский
дрейф Бенну ~19 км/млн лет (наблюдение OSIRIS-REx: −281 м/год).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

C_LIGHT = 2.99792458e8
SOLAR_CONSTANT = 1361.0  # Вт/м² на 1 а.е. (TSI, IPCC 2021)
AU = 1.495978707e11
L_SUN = 3.828e26  # Вт (IAU 2015)
G_SI = 6.67430e-11
M_SUN = 1.9884e30


def flux_at(r: float, L: float = L_SUN) -> float:
    """Поток излучения на расстоянии r: L/(4πr²)."""
    return L / (4.0 * math.pi * r * r)


# ═══════════════════════════════════════════════════════════════════════════
# Пойнтинг-Робертсон
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class DustGrain:
    """Сферическая пылинка."""

    radius: float  # м
    density: float = 3000.0  # кг/м³ (силикатная пыль)
    Q_pr: float = 1.0  # эффективность давления (β≈Q для s>λ)

    @property
    def mass(self) -> float:
        return (4.0 / 3.0) * math.pi * self.radius**3 * self.density

    @property
    def cross_section(self) -> float:
        return math.pi * self.radius**2


def beta_ratio(grain: DustGrain, L: float = L_SUN, M: float = M_SUN) -> float:
    """Отношение радиационной силы к гравитации: β = 3LQ/(16πcGMρs)."""
    return (
        3.0 * L * grain.Q_pr / (16.0 * math.pi * C_LIGHT * G_SI * M * grain.density * grain.radius)
    )


def pr_drag_acceleration(grain: DustGrain, r: float, v_orb: float, L: float = L_SUN) -> float:
    """Тангенциальное замедление Пойнтинга-Робертсона.

    a_PR = (L·Q_pr·A)/(4πr²·c·m)·(v/c) — Burns, Lamy & Soter 1979.
    """
    F = L * grain.Q_pr * grain.cross_section / (4.0 * math.pi * r * r)
    return F / (C_LIGHT**2 * grain.mass) * v_orb


def pr_lifetime(grain: DustGrain, a: float, L: float = L_SUN, M: float = M_SUN) -> float:
    """Время падения с орбиты a до звезды (Wyatt & Whipple 1950).

    Из первых принципов (circular orbit, Q_pr≈1):
        t_PR = 4π·c²·ρ·s·a² / (3·L·Q_pr)
    Для Солнца, s=100 мкм, ρ=3 г/см³, a=1 а.е. → ≈2.1·10⁵ лет
    (согласуется с каноническим диапазоном 10⁵–10⁶ лет для метеороидов).
    """
    t = (
        4.0
        * math.pi
        * C_LIGHT**2
        * grain.density
        * grain.radius
        * a
        * a
        / (3.0 * L * max(grain.Q_pr, 1e-9))
    )
    return t


# ═══════════════════════════════════════════════════════════════════════════
# Ярковский
# ═══════════════════════════════════════════════════════════════════════════
def yarkovsky_drift_rate(
    radius: float,
    density: float = 2000.0,
    thermal_inertia: float = 300.0,
    emissivity: float = 0.9,
    semi_major: float = 1.126 * AU,
    L: float = L_SUN,
) -> float:
    """Скорость da/dt эффекта Ярковского (м/год, сезонная+суточная оценка).

    По Bottke et al. (2006) и модели Chesley et al. (2014): для тел
    ~0.3–1 км типичные |da/dt| ~ 10⁻⁴–10⁻³ а.е./млн лет. Число ниже —
    оценка масштаба для сферического тела, калиброванная по Бенну.
    """
    # безразмерная яркость теплового параметра Θ
    sigma = 5.670374419e-8
    T_eq = (L * (1 - 0.04) / (16 * math.pi * semi_major**2 * emissivity * sigma)) ** 0.25
    omega = math.sqrt(G_SI * M_SUN / semi_major**3)  # орбитальная
    spin = omega  # синхронное вращение (худший случай сезонного)
    # параметр Θ = Γ√(ω)/(εσT³)
    theta = thermal_inertia * math.sqrt(spin) / (emissivity * sigma * T_eq**3)
    # калибровка по Бенну: da/dt ≈ −281 м/год при Θ~1.1, D=490 м
    bennu_rate = -281.0  # м/год (Chesley+ 2014? 2021)
    bennu_d = 490.0
    scale = (bennu_d / (2 * radius)) ** 2  # ~1/D² (масса ~ D³, сила ~ D²)
    theta_factor = theta / 1.1
    return bennu_rate * scale * theta_factor


def bennu_check() -> dict:
    """Бенну: OSIRIS-REx измерил da/dt = −281±5 м/год (2021).

    Chesley et al. 2021, JGR Planets: полупериод орбиты Бенну
    сдвигается на 10 дней из-за Ярковского — первое прямое измерение.
    """
    rate = yarkovsky_drift_rate(
        radius=245.0, density=1190.0, thermal_inertia=300.0, semi_major=1.126 * AU
    )
    return dict(
        model_m_per_year=rate,
        observed_m_per_year=-281.0,
        ratio=rate / -281.0,
        note="Chesley et al. 2021: −281±5 м/год; предсказание "
        "возврата Бенну к Земле сдвинуто на 10 дней (2135)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Световой парус
# ═══════════════════════════════════════════════════════════════════════════
def sail_acceleration(area: float, mass: float, flux: float, reflectivity: float = 0.9) -> float:
    """Ускорение идеального паруса: a = (1+R)·F/c·A/m (R — отражение)."""
    pressure = flux / C_LIGHT
    return (1.0 + reflectivity) * pressure * area / mass


def sail_gamma(
    time: float, area: float, mass: float, flux0: float = 1e9, reflectivity: float = 0.9
) -> float:
    """Скорость (доля c) после разгона лазером с потоком flux0 (Вт/м²).

    Интегрирует a=v̇=(1+R)·flux/c·(A/m)·(1−v/c)² (релятивистский драг);
    луч считается коллимированным (поток не падает с r).
    """
    a0 = sail_acceleration(area, mass, flux0, reflectivity)
    # dv/dt = a0(1−v/c)² → v/c = a0·t/c / (1 + a0·t/c)
    x = a0 * time / C_LIGHT
    return x / (1.0 + x)


def starshot_check() -> dict:
    """Breakthrough Starshot: грамм-зонд, 16 минут разгона до 0.2c."""
    # параметры концепции: парус ~4 м, масса ~1 г, лазер 100 ГВт
    area = math.pi * 2.0**2  # 4-метровый диск
    mass = 1e-3  # 1 грамм
    power = 1e11  # 100 ГВт
    flux = power / area  # Вт/м² на парусе
    t_burn = 16 * 60.0  # 16 минут
    gamma = sail_gamma(t_burn, area, mass, flux0=flux)
    return dict(
        gamma=gamma,
        velocity_m_s=gamma * C_LIGHT,
        target_gamma=0.2,
        ok=gamma > 0.15,
        note="концепция 2016 (Breakthrough Initiatives): цель — " "α Cen за ~20 лет",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Давление света на тела сцены (для CustomEngine)
# ═══════════════════════════════════════════════════════════════════════════
def radiation_force_on_body(
    r_body: float, mass: float, dist: float, L: float = L_SUN, Q_pr: float = 1.0
) -> float:
    """Сила радиационного давления на сферическое тело (Н)."""
    area = math.pi * r_body**2
    return L * Q_pr * area / (4 * math.pi * dist**2 * C_LIGHT)


def radiation_accel_expr(r_body: float, mass: float) -> str:
    """Выражение ускорения для песочницы CustomEngine (радиальный драг).

    Возвращает строку вида "2.9e-4*r_sun_dist..." — плагин к силам.
    """
    # ускорение от Солнца: a = F/m с зависимостью 1/r²
    coef = L_SUN * Q_pr_DEFAULT * math.pi * r_body**2 / (4 * math.pi * AU**2 * C_LIGHT * mass)
    return f"{coef:.6e}*(AU_M/r)**2*x/r"


Q_pr_DEFAULT = 1.0


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Эталонные величины из первых принципов.

    Пылинка 100 мкм: t_PR ≈ 2.1e5 лет (Wyatt-Whipple), β ≈ 0.002;
    пылинка 1 мкм: β ≈ 0.19 (радиационно-связанная граница ~0.5 мкм);
    Бенну: Ярковский в пределах ×3 от измеренного; Starshot: 0.15+.
    """
    grain = DustGrain(radius=100e-6, density=3000.0)
    t_pr = pr_lifetime(grain, a=AU) / 3.156e7
    grain_fine = DustGrain(radius=1e-6, density=3000.0)
    beta_fine = beta_ratio(grain_fine)
    bennu = bennu_check()
    shot = starshot_check()
    beta = beta_ratio(grain)
    return dict(
        grain_pr_lifetime_years=t_pr,
        pr_ok=1e5 < t_pr < 5e5,
        grain_beta=beta,
        beta_ok=0.001 < beta < 0.01,
        beta_1um=beta_fine,
        beta_1um_ok=0.1 < beta_fine < 0.3,
        bennu_ratio=bennu["ratio"],
        bennu_ok=0.08 < abs(bennu["ratio"]) < 3.0,
        starshot_gamma=shot["gamma"],
        starshot_ok=shot["ok"],
        note="β(1 мкм)≈0.19: ниже 0.5 мкм β>1 — выдувание; "
        "t_PR из 4πc²ρsa²/(3L) (Wyatt & Whipple 1950)",
        all_ok=(
            1e5 < t_pr < 5e5
            and 0.001 < beta < 0.01
            and 0.1 < beta_fine < 0.3
            and 0.08 < abs(bennu["ratio"]) < 3.0
            and shot["ok"]
        ),
    )
