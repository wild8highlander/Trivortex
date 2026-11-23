#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — небесные координаты: преобразования и время.

Экваториальная ↔ эклиптическая ↔ горизонтальная системы, эпохи,
юлианские даты:

  * equatorial_to_ecliptic / обратно (наклон ε = 23.4393° J2000);
  * equatorial_to_horizontal (RA/Dec → Az/Alt для широты/долготы/LST);
  * julian_date / gmst / lst (модель IAU 1982, точность ~1 с);
  * precession (J2000 → дата, матрица прецессии, z-метод);
  * angular_separation (сферическая теорема косинусов);
  * parse_ra/parse_dec: '10h 23m 45s' / '+12° 34′ 56″' → градусы;
  * hour_angle, rise/set (приближённо, без рефракции по умолчанию).

Самопроверка: Полюс мира (RA любой, Dec +90°) → Alt = широта;
Полярная (RA 02h31m, Dec +89°16′) на широте 55.75° никогда не заходит.
"""

from __future__ import annotations

import datetime as _dt
import math

OBLIQUITY_J2000 = math.radians(23.4392911)  # наклон экватора
AU_M = 1.495978707e11
J2000_JD = 2451545.0


# ═══════════════════════════════════════════════════════════════════════════
# Парсинг форматов
# ═══════════════════════════════════════════════════════════════════════════
def parse_ra(text: str) -> float:
    """'10h 23m 45.6s' | '10 23 45.6' | '10:23:45.6' → градусы."""
    t = text.strip().lower().replace("h", " ").replace("m", " ").replace("s", " ").replace(":", " ")
    parts = t.split()
    if not parts:
        raise ValueError(f"не разобрать RA: {text!r}")
    h = float(parts[0])
    m = float(parts[1]) if len(parts) > 1 else 0.0
    s = float(parts[2]) if len(parts) > 2 else 0.0
    return (h + m / 60.0 + s / 3600.0) * 15.0


def parse_dec(text: str) -> float:
    """'+12d 34m 56s' | '-12° 34′ 56″' | '+12 34 56' → градусы."""
    t = (
        text.strip()
        .lower()
        .replace("d", " ")
        .replace("°", " ")
        .replace("m", " ")
        .replace("'", " ")
        .replace("′", " ")
        .replace('"', " ")
        .replace("″", " ")
        .replace(":", " ")
    )
    sign = 1.0
    if t.startswith("-"):
        sign = -1.0
        t = t[1:]
    elif t.startswith("+"):
        t = t[1:]
    parts = t.split()
    if not parts:
        raise ValueError(f"не разобрать Dec: {text!r}")
    d = float(parts[0])
    m = float(parts[1]) if len(parts) > 1 else 0.0
    s = float(parts[2]) if len(parts) > 2 else 0.0
    return sign * (d + m / 60.0 + s / 3600.0)


# ═══════════════════════════════════════════════════════════════════════════
# Время
# ═══════════════════════════════════════════════════════════════════════════
def julian_date(dt: _dt.datetime) -> float:
    """Юлианская дата (UTC); алгоритм Fliegel-Van Flandern."""
    a = (14 - dt.month) // 12
    y = dt.year + 4800 - a
    m = dt.month + 12 * a - 3
    jdn = dt.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    return (
        jdn
        - 0.5
        + (dt.hour + dt.minute / 60.0 + dt.second / 3600.0 + dt.microsecond / 3.6e9) / 24.0
    )


def gmst_radians(jd: float) -> float:
    """Гринвичское среднее звёздное время (IAU 1982)."""
    T = (jd - J2000_JD) / 36525.0
    gmst_sec = (
        67310.54841 + (876600.0 * 3600 + 8640184.812866) * T + 0.093104 * T * T - 6.2e-6 * T * T * T
    )
    return math.radians((gmst_sec / 240.0) % 360.0)  # 240 с = 1°


def lst_radians(jd: float, longitude_deg: float) -> float:
    """Местное звёздное время (восточная долгота +)."""
    return (gmst_radians(jd) + math.radians(longitude_deg)) % (2 * math.pi)


# ═══════════════════════════════════════════════════════════════════════════
# Преобразования систем
# ═══════════════════════════════════════════════════════════════════════════
def equatorial_to_ecliptic(ra_deg: float, dec_deg: float) -> tuple[float, float]:
    """Экваториальные → эклиптические (λ, β).

    Поворот вокруг оси x на наклон ε: эклиптические = R_x(ε)·экваториальные
    (проверено: Сириус → β ≈ −39.6°, λ ≈ 227°/104° по квадранту).
    """
    ra = math.radians(ra_deg)
    dec = math.radians(dec_deg)
    eps = OBLIQUITY_J2000
    x = math.cos(dec) * math.cos(ra)
    y_eq = math.cos(dec) * math.sin(ra)
    z_eq = math.sin(dec)
    y = y_eq * math.cos(eps) + z_eq * math.sin(eps)
    z = -y_eq * math.sin(eps) + z_eq * math.cos(eps)
    lam = math.degrees(math.atan2(y, x)) % 360.0
    beta = math.degrees(math.asin(max(-1.0, min(1.0, z))))
    return lam, beta


def ecliptic_to_equatorial(lam_deg: float, beta_deg: float) -> tuple[float, float]:
    """Эклиптические → экваториальные (RA, Dec): обратный поворот R_x(−ε)."""
    lam = math.radians(lam_deg)
    beta = math.radians(beta_deg)
    eps = OBLIQUITY_J2000
    x = math.cos(beta) * math.cos(lam)
    y_ecl = math.cos(beta) * math.sin(lam)
    z_ecl = math.sin(beta)
    y = y_ecl * math.cos(eps) - z_ecl * math.sin(eps)
    z = y_ecl * math.sin(eps) + z_ecl * math.cos(eps)
    ra = math.degrees(math.atan2(y, x)) % 360.0
    dec = math.degrees(math.asin(max(-1.0, min(1.0, z))))
    return ra, dec


def equatorial_to_horizontal(
    ra_deg: float, dec_deg: float, latitude_deg: float, lst_r: float
) -> tuple[float, float]:
    """(RA, Dec) → (Az, Alt) для LST в радианах (Восток от севера)."""
    ra = math.radians(ra_deg)
    dec = math.radians(dec_deg)
    lat = math.radians(latitude_deg)
    H = lst_r - ra  # часовой угол
    sin_alt = math.sin(dec) * math.sin(lat) + math.cos(dec) * math.cos(lat) * math.cos(H)
    alt = math.asin(max(-1.0, min(1.0, sin_alt)))
    # азимут: от севера по часовой
    cos_A = (math.sin(dec) - math.sin(alt) * math.sin(lat)) / max(
        math.cos(alt) * math.cos(lat), 1e-12
    )
    cos_A = max(-1.0, min(1.0, cos_A))
    A = math.acos(cos_A)
    if math.sin(H) > 0:
        A = 2 * math.pi - A
    return math.degrees(A), math.degrees(alt)


def angular_separation(ra1: float, dec1: float, ra2: float, dec2: float) -> float:
    """Угловое расстояние (градусы) между двумя точками неба."""
    r1, d1 = math.radians(ra1), math.radians(dec1)
    r2, d2 = math.radians(ra2), math.radians(dec2)
    cos_d = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(r1 - r2)
    return math.degrees(math.acos(max(-1.0, min(1.0, cos_d))))


# ═══════════════════════════════════════════════════════════════════════════
# Прецессия (J2000 → дата, приближение)
# ═══════════════════════════════════════════════════════════════════════════
def precess_ra_dec(ra_deg: float, dec_deg: float, jd: float) -> tuple[float, float]:
    """Прецессия координат от J2000 к эпохе jd (z-метод, точность ~1″)."""
    T = (jd - J2000_JD) / 36525.0
    # скорости прецессии (IAU 1976)
    zeta = math.radians((2306.2181 * T + 0.30188 * T * T + 0.017998 * T**3) / 3600.0)
    z = math.radians((2306.2181 * T + 1.09468 * T * T + 0.018203 * T**3) / 3600.0)
    theta = math.radians((2004.3109 * T - 0.42665 * T * T - 0.041833 * T**3) / 3600.0)
    ra = math.radians(ra_deg)
    dec = math.radians(dec_deg)
    # матрица прецессии (упрощённая форма)
    A = math.cos(dec) * math.sin(ra + zeta)
    B = math.cos(theta) * math.cos(dec) * math.cos(ra + zeta) - math.sin(theta) * math.sin(dec)
    C = math.sin(theta) * math.cos(dec) * math.cos(ra + zeta) + math.cos(theta) * math.sin(dec)
    ra_new = math.atan2(A, B) + z
    dec_new = math.asin(max(-1.0, min(1.0, C)))
    return math.degrees(ra_new) % 360.0, math.degrees(dec_new)


# ═══════════════════════════════════════════════════════════════════════════
# Восход/заход
# ═══════════════════════════════════════════════════════════════════════════
def rise_set_hour_angle(
    dec_deg: float, latitude_deg: float, horizon_deg: float = 0.0
) -> float | None:
    """Часовой угол восхода (радианы); None — незаходящее/невосходящее."""
    dec = math.radians(dec_deg)
    lat = math.radians(latitude_deg)
    h0 = math.radians(horizon_deg)
    cos_H = (math.sin(h0) - math.sin(lat) * math.sin(dec)) / (math.cos(lat) * math.cos(dec))
    if cos_H > 1.0:
        return None  # никогда не восходит
    if cos_H < -1.0:
        return math.pi  # незаходящее (любой H)
    return math.acos(cos_H)


def is_circumpolar(dec_deg: float, latitude_deg: float) -> bool:
    """Незаходящее светило: |φ| + δ > 90° (северное полушарие)."""
    return latitude_deg + dec_deg > 90.0 or latitude_deg + dec_deg < -90.0


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Полюс → Alt=широта; экв.↔экл. roundtrip; Полярная циркумполярна."""
    # JD: 2000-01-01 12:00 UTC = 2451545.0
    jd = julian_date(_dt.datetime(2000, 1, 1, 12, 0, 0))
    jd_ok = abs(jd - 2451545.0) < 1e-6
    # Полюс мира: Alt = широта (в любой момент)
    az, alt = equatorial_to_horizontal(0.0, 90.0, 55.75, lst_r=0.5)
    pole_ok = abs(alt - 55.75) < 0.01
    # roundtrip экв. ↔ экл.
    ra, dec = 101.28, -16.72  # Сириус
    lam, beta = equatorial_to_ecliptic(ra, dec)
    ra2, dec2 = ecliptic_to_equatorial(lam, beta)
    roundtrip_ok = angular_separation(ra, dec, ra2, dec2) < 1e-6
    # Полярная звезда: незаходит в Москве
    polar_dec = parse_dec("+89° 16′ 12″")
    polar_ra = parse_ra("02h 31m 49s")
    circumpolar = is_circumpolar(polar_dec, 55.75)
    # угловое расстояние Сириус–Бетельгейзе ≈ 27°? проверим грубо
    betelgeuse_ra = parse_ra("05h 55m 10s")
    betelgeuse_dec = parse_dec("+07° 24′ 25″")
    sep = angular_separation(101.28, -16.72, betelgeuse_ra, betelgeuse_dec)
    sep_ok = 25.0 < sep < 30.0  # фактическое ≈ 27.3°
    # GMST на J2000.0 полдень ≈ 18.697374558 ч ≈ 280.46°
    gmst = math.degrees(gmst_radians(2451545.0))
    gmst_ok = abs(gmst - 280.46) < 0.1
    return dict(
        jd_ok=jd_ok,
        jd=jd,
        pole_alt=alt,
        pole_ok=pole_ok,
        roundtrip_ok=roundtrip_ok,
        sirius_ecliptic=(round(lam, 2), round(beta, 2)),
        polar_circumpolar=circumpolar,
        sirius_betelgeuse_sep=sep,
        sep_ok=sep_ok,
        gmst_deg=gmst,
        gmst_ok=gmst_ok,
        ok=jd_ok and pole_ok and roundtrip_ok and circumpolar and sep_ok and gmst_ok,
    )
