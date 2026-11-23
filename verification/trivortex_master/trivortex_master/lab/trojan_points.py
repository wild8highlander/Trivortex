#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — троянские астероиды: точки L4/L5 и критерий Рабе.

  * rabe_criterion: линейная устойчивость L4/L5 — μ < μ_R ≈ 0.03852
    (Rabe 1961, строго: (μ₁μ₂)/(μ₁+μ₂)² < 1/27, что даёт
    μ = m₂/(m₁+m₂) < 0.03852);
  * trojan_amplitude: амплитуда длиннопериодической либрации вокруг
    L4 — тангенциальные колебания с периодом T_lib ≈ T_orb/√(27μ/4)
    (Murray & Dermott §8.5... точнее: ω_lib = n·√(27μ/4));
  * trojan_zone_width: типичная ширина зоны троянцев Юпитера (~±12°
    по долготе, астероиды 1–40° от L4);
  * population_check: наблюдаемое неравенство L4/L5 Юпитера
    (L4 ~ 1.5-2× больше L5 — не объяснено до конца, Szabó 2007).

Самопроверки: порог Рабе 0.03852; Юпитер устойчив, Земля устойчива,
Солнце-планета с μ > 0.03852 неустойчива (синтетическая пара);
частота либрации Троянцев Юпитера ~ 1/150 лет.
"""
from __future__ import annotations

import math

RABE_THRESHOLD = 0.03852        # μ_max для устойчивости L4/L5
MU_JUPITER = 1.898e27 / 1.9884e30        # ≈ 9.54e-4
MU_EARTH = 5.9722e24 / 1.9884e30         # ≈ 3.0e-6
JUPITER_PERIOD_Y = 11.862


def rabe_mu(mu_ratio: float) -> dict:
    """Проверка критерия Рабе для массовой доли μ = m₂/(m₁+m₂)."""
    # строгая форма: μ(1−μ) < 1/27
    mu_product = mu_ratio * (1.0 - mu_ratio)
    stable = mu_product < 1.0 / 27.0
    return dict(mu=mu_ratio, mu_product=mu_product,
                threshold=1.0 / 27.0, stable=stable,
                rabe_threshold=RABE_THRESHOLD,
                reference="Rabe 1961; Murray & Dermott §4.3")


def libration_frequency(mu: float, orbital_period_years: float
                        ) -> float:
    """Период длиннопериодической либрации (лет): T/√(27μ/4)."""
    return orbital_period_years / math.sqrt(27.0 * mu / 4.0)


def jupiter_trojans_check() -> dict:
    """Троянцы Юпитера: устойчивость, либрация ~150 лет, зона ±12°."""
    rabe = rabe_mu(MU_JUPITER)
    t_lib = libration_frequency(MU_JUPITER, JUPITER_PERIOD_Y)
    # наблюдаемое: период либрации Троянцев ~ 147-150 лет (Europy data)
    lib_ok = 100.0 < t_lib < 220.0
    return dict(stable=rabe["stable"], libration_years=t_lib,
                libration_ok=lib_ok,
                zone_degrees=12.0,
                reference="Szabó et al. 2007 (L4/L5 inequality); "
                          "космический телескоп WISE — популяция ~10⁵")


def earth_trojans_check() -> dict:
    """Земные троянцы (2010 TK₇): μ Земли мала → устойчивость есть.

    2010 TK₇ — первый известный троянец Земли (Connors 2011, Nature),
    либрация с большой амплитудой."""
    rabe = rabe_mu(MU_EARTH)
    t_lib = libration_frequency(MU_EARTH, 1.0)
    return dict(stable=rabe["stable"],
                libration_years=t_lib,
                note="2010 TK₇: L4 Земли, большая амплитуда качания "
                     "(Connors et al. 2011, Nature 475, 456)")


def unstable_pair_check() -> dict:
    """Контрпример: пара с μ > 0.03852 → L4/L5 неустойчивы.

    Искусственная пара: m₂/m₁ = 0.05 → μ ≈ 0.0476 > порога."""
    mu = 0.05 / 1.05
    rabe = rabe_mu(mu)
    return dict(mu=mu, stable=rabe["stable"],
                expected_unstable=(not rabe["stable"]))


def trojan_zone_report(l4_count: int = 1.6, l5_count: float = 1.0
                       ) -> dict:
    """Наблюдательное неравенство L4/L5 (Szabó 2007): L4 ≈ 1.6×L5."""
    return dict(L4_relative=l4_count, L5_relative=l5_count,
                ratio=l4_count / l5_count,
                note="причина неравенства до конца не объяснена — "
                     "возможные механизмы: захват при миграции, "
                     "взаимные возмущения, наблюдательная селекция")


def self_check() -> dict:
    """Порог Рабе; Юпитер/Земля устойчивы; контрпример неустойчив;
    либрация Троянцев ~150 лет."""
    jup = jupiter_trojans_check()
    earth = earth_trojans_check()
    un = unstable_pair_check()
    threshold = rabe_mu(RABE_THRESHOLD)
    # порог: μ = 0.03852 → на границе устойчивости
    border_ok = abs(threshold["mu_product"] - 1.0 / 27.0) < 1e-4
    return dict(
        jupiter_stable=jup["stable"], jupiter_lib_years=jup["libration_years"],
        jupiter_lib_ok=jup["libration_ok"],
        earth_stable=earth["stable"],
        counterexample_unstable=un["expected_unstable"],
        rabe_border_ok=border_ok,
        all_ok=jup["stable"] and jup["libration_ok"]
        and earth["stable"] and un["expected_unstable"] and border_ok,
        note="μ_J = 9.54e-4 << 0.03852; период либрации n·√(4/27μ)",
    )
