#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — архитектуры планетных систем: резонансы, упаковка,
устойчивость, TEM-классификация.

Модуль отвечает на практические вопросы конструирования систем:

  * Hill stability: критерий Гладмана (1993) для пары планет
    (a2/a1 > критического при данных массах и эксцентриситетах);
  * упаковка (packing): сколько землеподобных планет влезает в ЗЖЗ
    звезды без пересечения сфер Хилла (Chambers et al. 1996);
  * mean-motion резонансы: ближайшие p:q к паре, ширина резонанса
    (MD 1999, eq. 8.76), отстройка от точного резонанса;
  * TRAPPIST-подобные цепочки: проверка лапласовых 3-тельных
    резонансов (как 8:5:3 у TRAPPIST-1, Gillon et al. 2017);
  * температурный режим: равновесная температура, инсоляция в S⊕,
    S_eff для внутреннего края ЗЖЗ (Kopparapu et al. 2013).

Самопроверки: Солнечная система (все пары Hill-stable), TRAPPIST-1
(цепочка резонансов), упаковка ЗЖЗ M-карлика.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

G_SI = 6.67430e-11
AU = 1.495978707e11
SIGMA_SB = 5.670374419e-8
L_SUN = 3.828e26


@dataclass
class PlanetLite:
    """Планета для архитектурного анализа."""

    name: str
    mass: float  # кг
    a: float  # м
    e: float = 0.0
    radius: float = 0.0  # м (для инсоляции не нужен)

    @property
    def mu(self) -> float:
        """Handle PlanetLite.mu."""
        return G_SI * self.mass


# ═══════════════════════════════════════════════════════════════════════════
# Устойчивость по Хиллу
# ═══════════════════════════════════════════════════════════════════════════
def hill_radius(planet: PlanetLite, m_star: float) -> float:
    """r_H = a(1−e)(m/(3M))^{1/3}."""
    return planet.a * (1 - planet.e) * (planet.mass / (3.0 * m_star)) ** (1.0 / 3.0)


def mutual_hill_separation(p1: PlanetLite, p2: PlanetLite, m_star: float) -> float:
    """Δ = (a2−a1)/R_H,mut — разделение в взаимных сфер Хилла."""
    rh1 = hill_radius(p1, m_star)
    rh2 = hill_radius(p2, m_star)
    rh_mutual = (rh1 + rh2) / 2.0
    return (p2.a - p1.a) / rh_mutual


def gladman_hill_stable(p1: PlanetLite, p2: PlanetLite, m_star: float) -> dict:
    """Критерий Гладмана (1993, Icarus 106, 247): пара устойчива, если

    (a2/a1) > 1 + 2.3·(μ1+μ2)^{1/3}·((a1+a2)/(2a2))^{1/3} + ...
    (упрощённая форма для почти круговых орбит).
    Практическое правило: Δ_Hill > 2√3 ≈ 3.46 для долгосрочной
    устойчивости (Smith & Lissauer 2009).
    """
    mu1 = p1.mass / m_star
    mu2 = p2.mass / m_star
    ratio = p2.a / p1.a
    gladman = 1.0 + 2.3 * (mu1 + mu2) ** (1.0 / 3.0) * ((p1.a + p2.a) / (2 * p2.a)) ** (1.0 / 3.0)
    delta = mutual_hill_separation(p1, p2, m_star)
    return dict(
        separation_ratio=ratio,
        gladman_threshold=gladman,
        hill_stable=ratio > gladman,
        mutual_hill_delta=delta,
        long_term_stable=delta > 3.46,
        note="Smith & Lissauer 2009: Δ>2√3 — устойчивость >10¹⁰ орбит",
    )


def solar_system_hill_check() -> dict:
    """Все соседние пары Солнечной системы — Hill-устойчивы."""
    M_sun = 1.9884e30
    earth = 5.9722e24
    jupiter = 1.898e27
    pairs = [
        (
            "Венера-Земля",
            PlanetLite("V", 0.815 * earth, 0.723 * AU, 0.007),
            PlanetLite("E", earth, 1.0 * AU, 0.017),
        ),
        (
            "Земля-Марс",
            PlanetLite("E", earth, 1.0 * AU, 0.017),
            PlanetLite("M", 0.107 * earth, 1.524 * AU, 0.093),
        ),
        (
            "Марс-Юпитер",
            PlanetLite("M", 0.107 * earth, 1.524 * AU, 0.093),
            PlanetLite("J", jupiter, 5.203 * AU, 0.048),
        ),
    ]
    results = {}
    for name, p1, p2 in pairs:
        res = gladman_hill_stable(p1, p2, M_sun)
        results[name] = dict(stable=res["hill_stable"], delta=res["mutual_hill_delta"])
    all_stable = all(r["stable"] for r in results.values())
    return dict(pairs=results, all_stable=all_stable)


# ═══════════════════════════════════════════════════════════════════════════
# Упаковка зоны обитаемости
# ═══════════════════════════════════════════════════════════════════════════
def habitable_zone(m_star: float, L_star: float = None) -> dict:
    """ЗЖЗ по Kopparapu et al. 2013 (упрощённые коэффициенты).

    Возвращает внутренний/внешний край в а.е. и инсоляцию S_eff.
    """
    # Т_eff по массе (главная последовательность, грубо)
    if L_star is None:
        # L ~ M^3.5
        L_star = L_SUN * (m_star / 1.9884e30) ** 3.5
    m_sol = m_star / 1.9884e30
    # S_eff границы (Kopparapu 2013, Table 3; for Teff≈5780):
    s_in = 1.014 if m_sol > 0.8 else 0.88
    s_out = 0.343 if m_sol > 0.8 else 0.28
    # переворот: a = sqrt(L/S_eff)
    a_in = math.sqrt((L_star / L_SUN) / s_in)
    a_out = math.sqrt((L_star / L_SUN) / s_out)
    return dict(
        a_in_au=a_in,
        a_out_au=a_out,
        S_eff_in=s_in,
        S_eff_out=s_out,
        L_star_solar=L_star / L_SUN,
        note="Kopparapu et al. 2013, ApJ 765, 131",
    )


def pack_habitable_zone(
    m_star: float, planet_mass: float, spacing_hill: float = 3.5, L_star: float = None
) -> dict:
    """Сколько планет массы planet_mass помещается в ЗЖЗ звезды.

    Шаг по большим полуосям: a_{i+1} = a_i·(1 + Δ·r_H/a) с r_H,
    вычисленным на текущем радиусе; упаковка от внутреннего края.
    """
    hz = habitable_zone(m_star, L_star)
    a = hz["a_in_au"] * AU
    a_out = hz["a_out_au"] * AU
    count = 0
    semis = []
    while a < a_out:
        semis.append(a / AU)
        count += 1
        p = PlanetLite("tmp", planet_mass, a)
        rh = hill_radius(p, m_star)
        a = a + spacing_hill * rh
    return dict(n_planets=count, semi_major_axes_au=semis, **hz)


# ═══════════════════════════════════════════════════════════════════════════
# Резонансы средних движений
# ═══════════════════════════════════════════════════════════════════════════
def period_ratio(p1: PlanetLite, p2: PlanetLite, m_star: float) -> float:
    """P2/P1 = (a2/a1)^{3/2}."""
    return (p2.a / p1.a) ** 1.5


def nearest_resonances(p1: PlanetLite, p2: PlanetLite, m_star: float, max_q: int = 6) -> list[dict]:
    """Ближайшие p:q-резонансы к отношению периодов (|Δ|<0.05)."""
    pr = period_ratio(p1, p2, m_star)
    out = []
    for q in range(1, max_q + 1):
        for p in range(q + 1, q * 3 + 1):
            val = p / q
            delta = pr - val
            if abs(delta) < 0.05:
                out.append(dict(resonance=f"{p}:{q}", ratio=val, offset=delta))
    out.sort(key=lambda r: abs(r["offset"]))
    return out[:4]


def resonance_width(p1: PlanetLite, p2: PlanetLite, m_star: float, p: int, q: int) -> float:
    """Ширина резонанса p:q в единицах a (Murray & Dermott, упрощ.).

    Для резонанса первого порядка (q=1): δa/a ≈ (16·μ·e·L(e))^{1/2}·...
    Возвращает полуширину Δa/a.
    """
    mu = p2.mass / m_star
    e = max(p2.e, 0.01)
    # порядок q: ширина падает как e^{q/2}
    coef = (mu ** (1.0 / 2.0)) * (e ** (q / 2.0)) * 1.5
    return coef


def trappist_chain_check(
    semis_au: Sequence[float], masses_earth: Sequence[float], m_star: float
) -> dict:
    """Проверка лапласовой цепочки TRAPPIST-1-подобной системы.

    TRAPPIST-1 (Gillon et al. 2017, Nature 542, 456): 7 планет в
    цепочке резонансов ~8:5, 5:3, 3:2, 3:2, 4:3, 3:2 (b–h).
    """
    M_earth = 5.9722e24
    planets = [
        PlanetLite(f"p{i}", m * M_earth, a * AU, 0.0)
        for i, (a, m) in enumerate(zip(semis_au, masses_earth))
    ]
    chain = []
    for i in range(len(planets) - 1):
        near = nearest_resonances(planets[i], planets[i + 1], m_star)
        chain.append(
            dict(
                pair=f"{planets[i].name}-{planets[i + 1].name}",
                period_ratio=period_ratio(planets[i], planets[i + 1], m_star),
                nearest=near[0]["resonance"] if near else "—",
                offset=near[0]["offset"] if near else None,
            )
        )
    in_chain = all(abs(c["offset"]) < 0.02 for c in chain if c["offset"] is not None)
    return dict(
        chain=chain, resonant_chain=in_chain, reference="Gillon et al. 2017; Luger et al. 2017"
    )


# ═══════════════════════════════════════════════════════════════════════════
# Температурный режим
# ═══════════════════════════════════════════════════════════════════════════
def equilibrium_temperature(
    a_m: float, L_star: float, albedo: float = 0.3, emissivity: float = 1.0
) -> float:
    """T_eq = [L(1−A)/(16πεσa²)]^{1/4}."""
    return (L_star * (1 - albedo) / (16.0 * math.pi * emissivity * SIGMA_SB * a_m**2)) ** 0.25


def insolation_in_earth_units(a_m: float, L_star: float) -> float:
    """Инсоляция в единицах земной: S = (L/L☉)/(a/а.е.)²."""
    return (L_star / L_SUN) / (a_m / AU) ** 2


def trappist_like_hz_check() -> dict:
    """TRAPPIST-1e: T_eq ≈ 249 К (Gillon 2017, A=0), S ≈ 0.66 S⊕."""
    L_trappist = 0.000553 * L_SUN  # L≈0.055% L☉ (M8V)
    a_e = 0.02925 * AU
    # Gillon et al. 2017 публикуют T_eq для альбедо = 0 (полное поглощение)
    t_eq = equilibrium_temperature(a_e, L_trappist, albedo=0.0)
    s_eff = insolation_in_earth_units(a_e, L_trappist)
    return dict(
        T_eq_kelvin=t_eq,
        observed_T_eq=249.0,
        T_ok=abs(t_eq - 249.0) < 15.0,
        S_eff=s_eff,
        observed_S=0.66,
        S_ok=abs(s_eff - 0.66) < 0.15,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка модуля
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Солнечная система + TRAPPIST-1 + упаковка ЗЖЗ."""
    solar = solar_system_hill_check()
    trappist_hz = trappist_like_hz_check()
    # TRAPPIST-1: реальные a (Luger et al. 2017) и массы
    semis = [0.01154, 0.01580, 0.02227, 0.02925, 0.03849, 0.04683, 0.06189]
    masses = [1.374, 1.308, 0.388, 0.692, 1.039, 1.321, 0.326]
    m_star = 0.0898 * 1.9884e30
    chain = trappist_chain_check(semis, masses, m_star)
    # упаковка ЗЖЗ M-карлика 0.1 M☉ земными планетами
    packing = pack_habitable_zone(0.1 * 1.9884e30, 5.9722e24)
    return dict(
        solar_stable=solar["all_stable"],
        trappist_T_eq=trappist_hz["T_eq_kelvin"],
        trappist_T_ok=trappist_hz["T_ok"],
        trappist_S=trappist_hz["S_eff"],
        trappist_S_ok=trappist_hz["S_ok"],
        trappist_chain=chain["resonant_chain"],
        trappist_chain_pairs=[c["nearest"] for c in chain["chain"]],
        hz_packing_n=packing["n_planets"],
        all_ok=(
            solar["all_stable"]
            and trappist_hz["T_ok"]
            and trappist_hz["S_ok"]
            and chain["resonant_chain"]
        ),
        note="упаковка ЗЖЗ 0.1M☉: ожидание ~3–5 земель (CHZ узкая)",
    )
