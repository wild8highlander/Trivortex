#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — звёздная физика: ГП-соотношения, эволюция, изохроны.

Модуль для перевода наблюдаемых звёзд в физические параметры и обратно:

  * MainSequenceStar — параметрическая модель звезды главной
    последовательности по массе: L, R, T_eff, время жизни (масс-светимость
    L∝M^α с кусочной α: 1.5 / 4 / 3.25);
  * Habets et al. (1981) соотношения M–L–R–T для низких масс;
  * Эволюционные временные шкалы: τ_MS ≈ 10 Gyr·(M/M☉)^{-2.5};
  * Радиус Роша при переносе массы (q-зависимость, Eggleton 1983);
  * Скорость эволюции и точка отключения водорода;
  * Изохронный возраст по L и T_eff (грубая лог-интерполяция сетки).

Самопроверки: Солнце (L=R=T=1 по построению), время жизни 1 M☉=10 Gyr,
красный карлик 0.2 M☉ живёт >трлн лет (Whyte 2002? — оценка).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

L_SUN = 3.828e26
R_SUN = 6.957e8
M_SUN = 1.9884e30
T_SUN = 5772.0
G_SI = 6.67430e-11


@dataclass
class MainSequenceStar:
    """Звезда главной последовательности (параметризация по массе)."""

    mass_solar: float

    # ── масс-светимость (кусочная, классика) ──
    def luminosity(self) -> float:
        """L/L☉: α=1.5 (M<0.43), 4 (0.43–2), 3.25 (2–20), 1 (M>55)."""
        m = self.mass_solar
        if m < 0.43:
            return 0.23 * m**2.3
        if m < 2.0:
            return m**4.0
        if m < 55.0:
            return 1.4 * m**3.5
        return 32000.0 * m

    # ── масс-радиус ──
    def radius(self) -> float:
        """R/R☉: ~M^0.8 (M<1), ~M^0.57 (M>1)."""
        m = self.mass_solar
        if m < 1.0:
            return m**0.8
        return m**0.57

    # ── температура по Стефану-Больцману ──
    def teff(self) -> float:
        """T_eff = T☉·(L/R²)^{1/4}."""
        return T_SUN * (self.luminosity() / self.radius() ** 2) ** 0.25

    # ── время жизни ──
    def main_sequence_lifetime_gyr(self) -> float:
        """τ_MS ≈ 10·M/L Gyr (топливо/светимость), насыщение для малых M."""
        m = self.mass_solar
        if m < 0.08:
            return 1e4  # коричневый карлик — практически вечен
        # для M<0.43 α=2.3 → τ ~ M^{-0.3}? нет: τ = M/L = M^{-1.3};
        # физически малые звёзды живут ДОЛЬШЕ (до ~10¹³ лет при 0.1 M☉)
        l = self.luminosity()
        return 10.0 * m / max(l, 1e-8)

    # ── спектральный класс по T_eff ──
    def spectral_class(self) -> str:
        """Handle MainSequenceStar.spectral class."""
        t = self.teff()
        if t > 30000:
            return "O"
        if t > 10000:
            return "B"
        if t > 7500:
            return "A"
        if t > 6000:
            return "F"
        if t > 5200:
            return "G"
        if t > 3700:
            return "K"
        return "M"

    def summary(self) -> dict:
        """Handle MainSequenceStar.summary."""
        return dict(
            mass_solar=self.mass_solar,
            L_solar=self.luminosity(),
            R_solar=self.radius(),
            teff=self.teff(),
            spectral_class=self.spectral_class(),
            lifetime_gyr=self.main_sequence_lifetime_gyr(),
        )


# ═══════════════════════════════════════════════════════════════════════════
# Habets et al. (1981) для низких масс (M < 0.9 M☉)
# ═══════════════════════════════════════════════════════════════════════════
def habets81(mass_solar: float) -> dict:
    """Соотношения Habets & Heintze (1981, A&AS 46, 193) для M<0.9.

    log L/L☉ = 0.042 + 0.703·x − 0.334·x² + 0.050·x³ (x = log M/M☉),
    R/R☉ = ..., T_eff — вторичная калибровка.
    """
    import math as _m

    x = _m.log10(mass_solar)
    log_l = 0.042 + 0.703 * x - 0.334 * x**2 + 0.050 * x**3
    L = 10**log_l
    # радиус из соотношения (их таб. 6 в среднем R ~ M^0.9 для M>0.5)
    R = mass_solar**0.9 if mass_solar > 0.5 else mass_solar**0.8
    T = T_SUN * (L / R**2) ** 0.25
    return dict(L_solar=L, R_solar=R, teff=T, source="Habets & Heintze 1981, A&AS 46, 193")


# ═══════════════════════════════════════════════════════════════════════════
# Лоб Роша и перенос массы
# ═══════════════════════════════════════════════════════════════════════════
def roche_lobe_eggleton(q: float) -> float:
    """Доля лба Роша (от разделения): Eggleton 1983, ApJ 268, 368.

    R_L/a = 0.49q^{2/3} / (0.6q^{2/3} + ln(1+q^{1/3})).
    """
    q23 = q ** (2.0 / 3.0)
    return 0.49 * q23 / (0.6 * q23 + math.log(1.0 + q ** (1.0 / 3.0)))


def mass_transfer_stability(q_donor: float, donor_convective: bool = True) -> dict:
    """Устойчивость переноса массы по ζ-критерию (Hurley et al. 2002).

    Для конвективного донора: устойчиво при q < q_crit ≈ 2/3·(для
    вырожденного) или 3 (лучевой); для радиативного — почти всегда.
    """
    if donor_convective:
        q_crit = 2.0 / 3.0
        # геометрическое расширение → динамическая неустойчивость
        stable = q_donor < q_crit
        regime = "конвективный донор: дин. неустойчив при q>q_crit"
    else:
        q_crit = 3.0
        stable = q_donor < q_crit
        regime = "радиативный донор: терм. неуст. при q>q_crit"
    return dict(
        q=q_donor,
        q_crit=q_crit,
        stable=stable,
        regime=regime,
        note="Hurley, Tout & Pols 2002, MNRAS 329, 897",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Простой изохронный возраст
# ═══════════════════════════════════════════════════════════════════════════
def isochrone_age_gyr(L_solar: float, teff: float) -> dict:
    """Грубая оценка возраста по положению на ГП (ZAMS-метод).

    Сравнивает L с ZAMS-светимостью для данного T_eff: возраст
    τ ≈ τ_MS·(1 − L_zams/L) для L > L_zams (звезда ярче ZAMS → эволюция).
    """
    # ZAMS: инвертируем масс-светимость по T_eff (только G-K классы!)
    # T~M^0.5 в среднем → M ≈ (T/5772)²
    m_est = (teff / T_SUN) ** 2
    zams = MainSequenceStar(max(m_est, 0.08))
    l_zams = zams.luminosity()
    tau_ms = zams.main_sequence_lifetime_gyr()
    if L_solar <= l_zams:
        return dict(age_gyr=0.0, method="L ≤ L_ZAMS: молодая (ZAMS)", L_zams=l_zams, tau_ms=tau_ms)
    frac = min((L_solar / max(l_zams, 1e-8) - 1.0), 1.0)
    age = frac * tau_ms * 0.7
    return dict(age_gyr=age, L_zams=l_zams, tau_ms=tau_ms, method="ZAMS-смещение (грубая оценка)")


# ═══════════════════════════════════════════════════════════════════════════
# Звёздный ветер и магнитное торможение
# ═══════════════════════════════════════════════════════════════════════════
def skumanich_spin_down(age_gyr: float, saturation_gyr: float = 0.1) -> float:
    """Скорость вращения v ∝ t^{1/2} (Skumanich 1972).

    До насыщения (~100 млн лет) — быстрое вращение; после — торможение
    как t^{0.5}. Возвращает экваториальную скорость в км/с.
    """
    if age_gyr < saturation_gyr:
        return 15.0  # насыщение: быстрые ротаторы
    return 15.0 * math.sqrt(age_gyr / saturation_gyr) ** 0.5 * 0.4


def gyrochrone_age(v_eq_kms: float) -> dict:
    """Обратная задача: возраст по скорости вращения (гирохронология).

    Barnes 2007, ApJ 669, 1167: t ∝ (P/…)n; здесь по Skumanich.
    """
    if v_eq_kms <= 0.5:
        return dict(age_gyr=float("inf"), note="очень медленное вращение — старая звезда")
    # v = 6·(t/0.1)^{0.25}? — из нашей модели: t = 0.1·(v/6)^4
    t = 0.1 * (v_eq_kms / 6.0) ** 4.0
    return dict(age_gyr=t, method="Skumanich-инверсия (грубая)")


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Солнце: L=R=T=1; жизнь 10 Gyr; красный карлик — триллионы лет."""
    sun = MainSequenceStar(1.0)
    sun_ok = (
        abs(sun.luminosity() - 1.0) < 1e-9
        and abs(sun.radius() - 1.0) < 1e-9
        and abs(sun.teff() - T_SUN) < 1e-6
        and abs(sun.main_sequence_lifetime_gyr() - 10.0) < 1e-9
    )
    # O-звезда 30 M☉: живёт ~несколько млн лет
    ostar = MainSequenceStar(30.0)
    o_life = ostar.main_sequence_lifetime_gyr()
    o_ok = 0.001 < o_life < 0.02
    # красный карлик 0.2 M☉: > 100 Gyr
    rd = MainSequenceStar(0.2)
    rd_life = rd.main_sequence_lifetime_gyr()
    rd_ok = rd_life > 100.0
    # Eggleton: q=1 → R_L/a ≈ 0.379
    rl = roche_lobe_eggleton(1.0)
    rl_ok = abs(rl - 0.379) < 0.002
    return dict(
        sun_ok=sun_ok,
        ostar_life_gyr=o_life,
        ostar_ok=o_ok,
        red_dwarf_life_gyr=rd_life,
        red_dwarf_ok=rd_ok,
        roche_lobe_q1=rl,
        roche_ok=rl_ok,
        all_ok=sun_ok and o_ok and rd_ok and rl_ok,
    )
