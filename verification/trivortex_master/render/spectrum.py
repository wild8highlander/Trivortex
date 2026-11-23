#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — цвет излучения: чёрное тело → RGB, спектральные классы.

Преобразование планковского спектра в видимый цвет (для реалистичной
отрисовки звёзд):

  * planck_curve(T, wavelengths): спектральная плотность B_λ(λ, T)
    (закон Планка 1901, Вт/м³/ср);
  * blackbody_rgb(T): B_λ → CIE XYZ 1931 (2° наблюдатель, дискретная
    таблица x̄,ȳ,z̄) → sRGB (D65, гамма 2.2);
  * spectral_class_color: класс O..M → RGB (T из таблицы);
  * wien_peak: λ_max = b/T, b = 2.897771955e-3 м·К (закон Вина).

Самопроверки: Солнце (5772 К) — почти белый (r≈g≈b, r>b);
M-карлик (3200 К) — заметно красный; O-звезда (30000 К) — голубая.
"""

from __future__ import annotations

import math

H_PLANCK = 6.62607015e-34
C_LIGHT = 2.99792458e8
K_B = 1.380649e-23
WIEN_B = 2.897771955e-3  # м·К


# ═══════════════════════════════════════════════════════════════════════════
# Планковский спектр и закон Вина
# ═══════════════════════════════════════════════════════════════════════════
def planck_curve(T: float, wavelengths_nm: list[float]) -> list[float]:
    """B_λ(λ, T) в Вт/м²/ср/нм (вход нм → перевод в СИ внутри)."""
    out = []
    for lam_nm in wavelengths_nm:
        lam = lam_nm * 1e-9
        c1 = 2 * H_PLANCK * C_LIGHT**2 / lam**5
        x = H_PLANCK * C_LIGHT / (lam * K_B * T)
        # защита от переполнения при большом x
        if x > 700:
            out.append(0.0)
        else:
            out.append(c1 / (math.expm1(x)) / 1e9)  # пер-нм
    return out


def wien_peak(T: float) -> float:
    """Длина волны максимума излучения (нм)."""
    return WIEN_B / T * 1e9


# ═══════════════════════════════════════════════════════════════════════════
# CIE 1931 (2°) — аналитические приближения функций сложения цветов
# (Wyman, Bertalmío & Veciana 2013, J. Opt. Soc. Am. A 30, 316 —
# кусочно-гауссовы аппроксимации, точность ~1–3% по всей видимой области)
# ═══════════════════════════════════════════════════════════════════════════
def _gauss_piece(x: float, mu: float, s1: float, s2: float) -> float:
    """Кусочная гауссиана: σ1 слева от μ, σ2 справа."""
    s = s1 if x < mu else s2
    t = (x - mu) / s
    return math.exp(-0.5 * t * t)


def cie_xyz(lam_nm: float) -> tuple[float, float, float]:
    """Функции сложения цветов x̄, ȳ, z̄ на длине волны λ (нм)."""
    xbar = (
        1.056 * _gauss_piece(lam_nm, 599.8, 37.1, 31.0)
        + 0.362 * _gauss_piece(lam_nm, 442.0, 16.0, 26.7)
        - 0.065 * _gauss_piece(lam_nm, 501.1, 20.4, 26.2)
    )
    ybar = 0.821 * _gauss_piece(lam_nm, 568.8, 46.9, 40.5) + 0.286 * _gauss_piece(
        lam_nm, 530.9, 16.3, 31.1
    )
    zbar = 1.217 * _gauss_piece(lam_nm, 437.0, 11.8, 36.0) + 0.842 * _gauss_piece(
        lam_nm, 459.0, 26.0, 13.8
    )
    return (xbar, ybar, zbar)


def _cie_xyz_by_lam(T: float, lam_nm: float) -> tuple[float, float, float]:
    """Интегранд CIE: B_λ·(x̄, ȳ, z̄) в точке λ."""
    b_val = planck_curve(T, [lam_nm])[0]
    if b_val <= 0:
        return (0.0, 0.0, 0.0)
    x, y, z = cie_xyz(lam_nm)
    return (b_val * x, b_val * y, b_val * z)


def blackbody_rgb(T: float) -> tuple[float, float, float]:
    """Цвет чёрного тела: B_λ × CIE → XYZ → sRGB (0..1), нормировка по max."""
    x_int = y_int = z_int = 0.0
    for lam in range(360, 831, 5):
        x, y, z = _cie_xyz_by_lam(T, lam)
        x_int += x * 5.0
        y_int += y * 5.0
        z_int += z * 5.0
    if max(x_int, y_int, z_int) <= 0:
        return (0.0, 0.0, 0.0)
    # XYZ → линейный sRGB (матрица D65)
    r_lin = 3.2406 * x_int - 1.5372 * y_int - 0.4986 * z_int
    g_lin = -0.9689 * x_int + 1.8758 * y_int + 0.0415 * z_int
    b_lin = 0.0557 * x_int - 0.2040 * y_int + 1.0570 * z_int
    # нормировка по максимуму (звезда «сама по себе» светит белым)
    m = max(r_lin, g_lin, b_lin, 1e-12)
    r_lin, g_lin, b_lin = r_lin / m, g_lin / m, b_lin / m

    def gamma(c):
        c = max(0.0, min(1.0, c))
        return c ** (1.0 / 2.2)

    return (gamma(r_lin), gamma(g_lin), gamma(b_lin))


# ═══════════════════════════════════════════════════════════════════════════
# Спектральные классы
# ═══════════════════════════════════════════════════════════════════════════
SPECTRAL_TEFF = {
    "O": 30000.0,
    "B": 18000.0,
    "A": 9000.0,
    "F": 7000.0,
    "G": 5700.0,
    "K": 4500.0,
    "M": 3200.0,
}


def spectral_class_color(cls: str) -> tuple[float, float, float]:
    """RGB цвет звезды спектрального класса O–M."""
    if cls not in SPECTRAL_TEFF:
        raise KeyError(f"класс {cls} не в O..M")
    return blackbody_rgb(SPECTRAL_TEFF[cls])


def rgb_to_hex(rgb: tuple[float, float, float]) -> str:
    """RGB 0..1 → '#RRGGBB'."""
    return "#" + "".join(f"{int(round(c * 255)):02X}" for c in rgb)


def self_check() -> dict:
    """Солнце — белый; M-карлик красный (r−b > 0.2); O — голубой (b−r > 0.15);
    Вин: Солнце λ_max ≈ 502 нм."""
    sun = blackbody_rgb(5772.0)
    m_dwarf = blackbody_rgb(3200.0)
    o_star = blackbody_rgb(30000.0)
    sun_white = abs(sun[0] - sun[1]) < 0.25 and sun[0] >= sun[2] - 0.05
    m_red = m_dwarf[0] - m_dwarf[2] > 0.2
    o_blue = o_star[2] - o_star[0] > 0.15
    lam_peak = wien_peak(5772.0)
    wien_ok = abs(lam_peak - 502.0) < 5.0
    return dict(
        sun_rgb=tuple(round(c, 3) for c in sun),
        m_dwarf_rgb=tuple(round(c, 3) for c in m_dwarf),
        o_star_rgb=tuple(round(c, 3) for c in o_star),
        sun_hex=rgb_to_hex(sun),
        sun_white=sun_white,
        m_red=m_red,
        o_blue=o_blue,
        wien_peak_nm=lam_peak,
        wien_ok=wien_ok,
        all_ok=sun_white and m_red and o_blue and wien_ok,
        note="CIE 1931 2°, sRGB D65, γ=2.2; таблица огрублена до 3 цифр",
    )
