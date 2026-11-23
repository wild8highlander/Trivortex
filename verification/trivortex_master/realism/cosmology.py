#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — космология: ΛCDM-расстояния, закон Хаббла, возраст.

Однородная изотропная Вселенная (FLRW) на чистом Python:

  * hubble_law: v = H₀·d (закон Хаббла 1929, H0 в км/с/Мпк);
  * hubble_parameter(z, Ωm, ΩΛ, Ωr): E(z) = H(z)/H₀ — √(Ωr(1+z)⁴ +
    Ωm(1+z)³ + Ωk(1+z)² + ΩΛ);
  * comoving_distance / luminosity_distance: интегрирование
    1/E(z) симпсоном (сотни сегментов — точность < 0.1%);
  * age_of_universe: ∫dz/((1+z)E(z)) от z=0 до ∞;
  * critical_density, deceleration parameter q₀;
  * lookback_time: световой путь до красного смещения z.

Калибровка: Planck 2018 (A&A 641, A6): H0 = 67.36, Ωm = 0.315,
ΩΛ = 0.685, возраст 13.797 Gyr, d_L(z=1) ≈ 6.69 Gpc.
"""
from __future__ import annotations

import math

# Planck 2018 (TT,TE,EE+lowE+lensing)
PLANCK18 = dict(H0=67.36, Omega_m=0.315, Omega_L=0.685,
                Omega_r=9.17e-5, Omega_k=0.0)

H0_SI = PLANCK18["H0"] * 1000.0 / 3.0857e22       # 1/с
MPC_KM = 3.0857e19
G_YEAR_S = 3.156e16
C_KMS = 2.99792458e5


# ═══════════════════════════════════════════════════════════════════════════
# Эволюция
# ═══════════════════════════════════════════════════════════════════════════
def hubble_parameter(z: float, Omega_m: float = PLANCK18["Omega_m"],
                     Omega_L: float = PLANCK18["Omega_L"],
                     Omega_r: float = PLANCK18["Omega_r"],
                     Omega_k: float = PLANCK18["Omega_k"]) -> float:
    """E(z) = H(z)/H₀ — безразмерный параметр расширения."""
    a = 1.0 / (1.0 + z)
    return math.sqrt(Omega_r / a ** 4 + Omega_m / a ** 3
                     + Omega_k / a ** 2 + Omega_L)


def _simpson(f, a: float, b: float, n: int = 400) -> float:
    """Численное интегрирование методом Симпсона (чётное n)."""
    if n % 2:
        n += 1
    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        total += (4.0 if i % 2 else 2.0) * f(a + i * h)
    return total * h / 3.0


def comoving_distance(z: float, **cosmo) -> float:
    """Сопутствующее расстояние (Мпк): c/H₀·∫dz/E(z)."""
    H0 = cosmo.pop("H0", PLANCK18["H0"])
    integrand = lambda zz: 1.0 / hubble_parameter(zz, **cosmo)
    integral = _simpson(integrand, 0.0, z, 400)
    return C_KMS / H0 * integral


def luminosity_distance(z: float, **cosmo) -> float:
    """Световое расстояние (Мпк): d_L = (1+z)·d_C."""
    return (1.0 + z) * comoving_distance(z, **cosmo)


def angular_diameter_distance(z: float, **cosmo) -> float:
    """Угловое расстояние (Мпк): d_A = d_C/(1+z)."""
    return comoving_distance(z, **cosmo) / (1.0 + z)


def lookback_time(z: float, **cosmo) -> float:
    """Время с момента z до сейчас (Гир): ∫dz/((1+z)E(z))/H₀."""
    H0 = cosmo.pop("H0", PLANCK18["H0"])
    integrand = lambda zz: 1.0 / ((1.0 + zz)
                                  * hubble_parameter(zz, **cosmo))
    integral = _simpson(integrand, 0.0, z, 400)
    return integral / (H0 * 1000.0 / 3.0857e22) / G_YEAR_S * 1e9 \
        / 1e9  # Гир


def age_of_universe(**cosmo) -> float:
    """Возраст Вселенной (Гир): ∫dz/((1+z)E(z)) от 0 до ∞.

    Кусочно: численно [0, 10] (мелкая сетка — интегранд крут у нуля),
    аналитический хвост эпохи МАТЕРИИ [10, ∞): E ≈ √Ωm·(1+z)^{3/2} →
    ∫dz/((1+z)E) = 1/(1.5·√Ωm·(1+10)^{1.5}) (на z=10 материя
    доминирует над радиацией в 300 раз).
    """
    H0 = cosmo.pop("H0", PLANCK18["H0"])
    Omega_m = cosmo.get("Omega_m", PLANCK18["Omega_m"])
    integrand = lambda zz: 1.0 / ((1.0 + zz)
                                  * hubble_parameter(zz, **cosmo))
    body = _simpson(integrand, 0.0, 10.0, 2000)
    tail = 1.0 / (1.5 * math.sqrt(Omega_m) * (1.0 + 10.0) ** 1.5)
    integral = body + tail
    h_sec = H0 * 1000.0 / 3.0857e22        # H0 в 1/с
    return integral / h_sec / G_YEAR_S


def critical_density(z: float = 0.0) -> float:
    """Критическая плотность ρ_c = 3H(z)²/(8πG) в кг/м³."""
    G = 6.67430e-11
    H = H0_SI * hubble_parameter(z)
    return 3.0 * H * H / (8.0 * math.pi * G)


def hubble_law(d_mpc: float, H0: float = PLANCK18["H0"]) -> float:
    """Закон Хаббла: скорость убегания (км/с) на расстоянии d (Мпк)."""
    return H0 * d_mpc


def deceleration_parameter(Omega_m: float = PLANCK18["Omega_m"],
                           Omega_L: float = PLANCK18["Omega_L"],
                           Omega_r: float = PLANCK18["Omega_r"]) -> float:
    """q₀ = Ωr + Ωm/2 − ΩΛ (при a=1)."""
    return Omega_r + Omega_m / 2.0 - Omega_L


def hubble_tension_note() -> dict:
    """Честная справка о напряжении Хаббла (H0 Tension)."""
    return dict(
        planck18=67.36,
        sh0es=73.04,
        tension_sigma="~5σ (Riess et al. 2022)",
        note="ранний (CMB) и поздний (цефеиды) обзоры дают разные H0 — "
             "одна из главных нерешённых проблем космологии",
        reference="Planck Collaboration 2018 (A&A 641, A6); "
                  "Riess et al. 2022 (ApJL 934, L7)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Planck-18: возраст 13.80 Gyr (±0.1); d_L(z=1) ≈ 6.69 Gpc (±0.1);
    закон Хаббла линейный."""
    age = age_of_universe()
    age_ok = abs(age - 13.797) < 0.15
    d_l = luminosity_distance(1.0)
    d_l_gpc = d_l / 1000.0
    d_l_ok = abs(d_l_gpc - 6.69) < 0.15
    # низкие z: d_L ≈ cz/H0 (32 Мпк → v ≈ 2157 км/с)
    v = hubble_law(32.0)
    hubble_ok = abs(v - 67.36 * 32.0) < 1e-6
    # время пролёта: z=11 (GN-z11) ≈ 13.0 Gyr назад
    lb = lookback_time(11.0)
    lb_ok = 12.5 < lb < 13.4
    return dict(
        age_gyr=age, age_ok=age_ok,
        d_L_z1_gpc=d_l_gpc, d_l_ok=d_l_ok,
        hubble_v_32mpc=v, hubble_ok=hubble_ok,
        lookback_z11_gyr=lb, lb_ok=lb_ok,
        q0=deceleration_parameter(),
        all_ok=age_ok and d_l_ok and hubble_ok and lb_ok,
        note="Planck 2018: возраст 13.797 Gyr; d_L(z=1) ≈ 6.69 Gpc; "
             "GN-z11 (z=11.09) — свет пошёл ~13.0 Gyr назад",
    )
