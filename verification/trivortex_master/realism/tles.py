#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — TLE: разбор, контрольные суммы, кеплерово распространение.

Two-Line Element (NORAD/celestrak формат 1972):

  * parse_tle: строгий разбор фиксированных колонок двух строк
    (номер NORAD, эпоха YYDDD.fraction, ṅ/n̈/B*, i, Ω, e, ω, M, n)
    с проверкой контрольных сумм (спека: сумма цифр + 1 за «−» mod 10);
  * tle_epoch_jd: эпоха → юлианская дата (UTC);
  * mean_motion_to_a: n (об/сут) → большая полуось (Кеплер III, км);
  * propagate_keplerian: средние элементы на Δt → M + n·Δt → решение
    Кеплера → ECI-вектор (честная пометка: упрощение SGP4 без J2/атм);
  * orbital_period_minutes.

Самопроверка: синтетический TLE с валидными контрольными суммами —
разбор туда-обратно; орбитальный период МКС-подобной орбиты ~92.9 мин.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

MU_EARTH_KM = 398600.4418  # км³/с² (EGM2008)


@dataclass
class Tle:
    """Разобранный TLE."""

    name: str
    norad_id: int
    epoch_jd: float
    inclination_deg: float
    raan_deg: float
    eccentricity: float
    argp_deg: float
    mean_anomaly_deg: float
    mean_motion_rev_day: float
    bstar: float
    ndot: float
    nddot: float


def _checksum(line: str) -> int:
    """Контрольная сумма строки TLE: Σцифр + 1 за каждый '−', mod 10."""
    total = 0
    for ch in line:
        if ch.isdigit():
            total += int(ch)
        elif ch == "-":
            total += 1
    return total % 10


def tle_epoch_jd(epoch_str: str) -> float:
    """'YYDDD.fraction' → JD (UTC). 57 → 1957-2057 по конвенции NORAD."""
    yy = int(epoch_str[:2])
    year = 2000 + yy if yy < 57 else 1900 + yy
    ddd = float(epoch_str[2:])
    # JD на 00:00 года (алгоритм Флигеля-Ван Фландерна)
    a = (14 - 1) // 12
    y = year + 4800 - a
    m = 1 + 12 * a - 3
    jdn = 1 + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    jd_midnight = jdn - 0.5
    return jd_midnight + ddd


def mean_motion_to_a(n_rev_day: float) -> float:
    """n (об/сут) → большая полуось (км) по Кеплеру III."""
    n_rad_s = n_rev_day * 2 * math.pi / 86400.0
    return (MU_EARTH_KM / n_rad_s**2) ** (1.0 / 3.0)


def orbital_period_minutes(n_rev_day: float) -> float:
    """Do orbital period minutes for n_rev_day and return the result."""
    return 1440.0 / n_rev_day


def parse_tle(line1: str, line2: str, name: str = "") -> Tle:
    """Разбор TLE с валидацией контрольных сумм (ValueError при сбое)."""
    line1, line2 = line1.rstrip(), line2.rstrip()
    if not line1.startswith("1 ") or not line2.startswith("2 "):
        raise ValueError("строки должны начинаться с '1 '/'2 '")
    if len(line1) < 68 or len(line2) < 68:
        # допускаем строки без контрольной суммы? — нет, спека: 68 симв.
        if len(line1) < 67 or len(line2) < 67:
            raise ValueError(f"длина строк {len(line1)}/{len(line2)} < 68")
    cs1, cs2 = int(line1[68]), int(line2[68])
    if _checksum(line1[:68]) != cs1:
        raise ValueError("контрольная сумма строки 1 не сходится")
    if _checksum(line2[:68]) != cs2:
        raise ValueError("контрольная сумма строки 2 не сходится")
    norad = int(line1[2:7])
    epoch = line1[18:32].strip()
    ndot = float(line1[33:43].strip().replace(" ", "0") or "0.0")
    nddot_exp = line1[44:52].strip()
    nddot = _parse_exp_field(nddot_exp)
    bstar = _parse_exp_field(line1[53:61].strip())
    incl = float(line2[8:16])
    raan = float(line2[17:25])
    ecc = float("0." + line2[26:33])
    argp = float(line2[34:42])
    mean_anom = float(line2[43:51])
    n_motion = float(line2[52:63])
    return Tle(
        name=name,
        norad_id=norad,
        epoch_jd=tle_epoch_jd(epoch),
        inclination_deg=incl,
        raan_deg=raan,
        eccentricity=ecc,
        argp_deg=argp,
        mean_anomaly_deg=mean_anom,
        mean_motion_rev_day=n_motion,
        bstar=bstar,
        ndot=ndot,
        nddot=nddot,
    )


def _parse_exp_field(field: str) -> float:
    """Поле TLE-экспоненты: '30777-4' = 30777·10⁻⁴ (конвенция NORAD:
    целочисленная мантисса × 10^exp)."""
    if not field:
        return 0.0
    field = field.strip()
    sign = -1.0 if field.startswith("-") else 1.0
    field = field.lstrip("+-")
    if "-" in field:
        mant, exp = field.split("-")
        exp_sign = -1
    elif "+" in field:
        mant, exp = field.split("+")
        exp_sign = 1
    else:
        mant, exp, exp_sign = field, "0", 1
    mant = mant.strip() or "0"
    value = float(mant) * 10.0 ** (exp_sign * int(exp))
    return sign * value


def _exp_field_encode(value: float) -> str:
    """Обратное: 3.0777e-4 → '30777-4' (мантисса 5 цифр, знак, эксп.)."""
    if value == 0:
        return " 00000-0"
    sign = " " if value > 0 else "-"
    v = abs(value)
    e = math.floor(math.log10(v))
    mant = int(round(v / 10.0**e * 1e5))
    if mant >= 100000:
        mant //= 10
        e += 1
    return f"{sign}{mant:05d}{'-' if e < 0 else '+'}{abs(e)}"[:8]


def make_tle(
    name: str,
    norad_id: int,
    epoch_yyddd: str,
    incl: float,
    raan: float,
    ecc: float,
    argp: float,
    mean_anom: float,
    n_motion: float,
    bstar: float = 0.0,
    ndot: float = 0.0,
    nddot: float = 0.0,
) -> tuple[str, str]:
    """Собрать две строки TLE по спеке фиксированных колонок (68+контр.сумма)."""
    ndot_f = f"{' ' if ndot >= 0 else '-'}{abs(ndot):.8f}"[:10]
    nddot_f = _exp_field_encode(nddot)
    bstar_f = _exp_field_encode(bstar)
    line1 = (
        f"1 {norad_id:05d}U 24001A  "
        f" {epoch_yyddd:<14.14}"
        f" {ndot_f}"
        f" {nddot_f}"
        f" {bstar_f}"
        f" 0  999"
    )
    line2 = (
        f"2 {norad_id:05d} "
        f"{incl:8.4f} {raan:8.4f} {int(round(ecc * 1e7)):07d} "
        f"{argp:8.4f} {mean_anom:8.4f} {n_motion:11.8f}    0"
    )
    line1 = line1[:68].ljust(68)
    line2 = line2[:68].ljust(68)
    line1 += str(_checksum(line1))
    line2 += str(_checksum(line2))
    return name, (line1, line2)


def propagate_keplerian(tle: Tle, dt_days: float) -> dict:
    """Кеплерово распространение средних элементов (упрощение SGP4).

    M += n·Δt; решение уравнения Кеплера; повороты i, Ω, ω → ECI (км).
    Честная пометка: без J2-дрейфа, без атмосферного торможения —
    точность деградирует ~1°/сут по RAAN для LEO.
    """
    n_rad_s = tle.mean_motion_rev_day * 2 * math.pi / 86400.0
    a_km = (MU_EARTH_KM / n_rad_s**2) ** (1.0 / 3.0)
    M = math.radians(tle.mean_anomaly_deg) + n_rad_s * dt_days * 86400.0
    M = M % (2 * math.pi)
    E = M
    for _ in range(60):
        dE = (E - tle.eccentricity * math.sin(E) - M) / (1 - tle.eccentricity * math.cos(E))
        E -= dE
        if abs(dE) < 1e-12:
            break
    x_orb = a_km * (math.cos(E) - tle.eccentricity)
    y_orb = a_km * math.sqrt(1 - tle.eccentricity**2) * math.sin(E)
    i_ang = math.radians(tle.inclination_deg)
    om = math.radians(tle.raan_deg)
    w = math.radians(tle.argp_deg)
    x1 = x_orb * math.cos(w) - y_orb * math.sin(w)
    y1 = x_orb * math.sin(w) + y_orb * math.cos(w)
    x_e = x1
    y_e = y1 * math.cos(i_ang)
    z_e = y1 * math.sin(i_ang)
    x_eci = x_e * math.cos(om) - y_e * math.sin(om)
    y_eci = x_e * math.sin(om) + y_e * math.cos(om)
    return dict(
        position_km=[x_eci, y_eci, z_e],
        radius_km=math.sqrt(x_eci**2 + y_eci**2 + z_e**2),
        a_km=a_km,
        period_min=orbital_period_minutes(tle.mean_motion_rev_day),
        method="keplerian mean elements (упрощение SGP4)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Синтетический TLE: контрольные суммы, разбор, период ~92.9 мин."""
    # ISS-подобные элементы: i=51.64°, n=15.493 об/сут, e=0.0006
    name, (l1, l2) = make_tle(
        "SYNTH-ISS",
        25544,
        "24001.50000000",
        51.6416,
        247.4627,
        0.0006709,
        130.5362,
        325.0288,
        15.49342877,
        bstar=21440,
        ndot=0.00016711,
        nddot=0.0,
    )
    tle = parse_tle(l1, l2, name)
    parsed_ok = (
        tle.norad_id == 25544
        and abs(tle.inclination_deg - 51.6416) < 1e-3
        and abs(tle.eccentricity - 0.0006709) < 1e-7
        and abs(tle.mean_motion_rev_day - 15.49342877) < 1e-6
    )
    period = orbital_period_minutes(15.49342877)
    period_ok = abs(period - 92.93) < 0.5
    # разлёт контрольной суммы ловится
    bad = l1[:68] + ("0" if l1[68] != "0" else "1")
    checksum_ok = False
    try:
        parse_tle(bad, l2)
    except ValueError as exc:
        checksum_ok = "сумма" in str(exc)
    # распространение на 45 минут: радиус ≈ a
    prop = propagate_keplerian(tle, 45.0 / 1440.0)
    a = mean_motion_to_a(15.49342877)
    radius_ok = abs(prop["radius_km"] - a) / a < 0.001
    return dict(
        parsed_ok=parsed_ok,
        period_min=period,
        period_ok=period_ok,
        checksum_ok=checksum_ok,
        radius_km=prop["radius_km"],
        radius_ok=radius_ok,
        all_ok=parsed_ok and period_ok and checksum_ok and radius_ok,
        note="синтетический TLE (формат NORAD/TLE спеки); n=15.49 "
        "об/сут → период 92.93 мин (типично для МКС)",
    )
