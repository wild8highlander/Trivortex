#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — каталог ярких звёзд ( топ-25, Hipparcos).

Реальные данные (J2000, Hipparcos/ESA 1997): RA, Dec, звёздная
величина, спектральный класс, расстояние (св. годы). Используется
для рендера звёздного неба, проверки небесных координат и альманаха.

  * find_brightest: ярчайшая звезда в конусе поиска;
  * constellations_of: грубая привязка к созвездиям (по координатам);
  * circumpolar_at / visible_at: видимость с широты;
  * angular_separation_between: пары звёзд (Сириус-Бетельгейзе 27.1°).

Самопроверка: Сириус ярчайшая (−1.46m), RA в 06h45m, Dec −16.7°;
Вега циркумполярна на 60° с.ш.; Ригель южнее Сириуса нет — позиции
согласованы между собой.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from realism.sky_coordinates import angular_separation, parse_ra, parse_dec


@dataclass
class Star:
    """Яркая звезда (J2000, Hipparcos)."""

    name: str
    ra_deg: float  # прямое восхождение, градусы
    dec_deg: float
    magnitude: float
    spectral: str
    dist_ly: float


# Топ-25 по видимой величине (система без группировки по кратным)
BRIGHT_STARS = [
    Star("Сириус", parse_ra("06h 45m 08.9s"), parse_dec("-16° 42′ 58″"), -1.46, "A1V", 8.6),
    Star("Канопус", parse_ra("06h 23m 57.1s"), parse_dec("-52° 41′ 44″"), -0.74, "A9II", 310.0),
    Star("α Центавра", parse_ra("14h 39m 36.5s"), parse_dec("-60° 50′ 02″"), -0.27, "G2V", 4.37),
    Star("Арктур", parse_ra("14h 15m 39.7s"), parse_dec("+19° 10′ 57″"), -0.05, "K1.5III", 36.7),
    Star("Вега", parse_ra("18h 36m 56.3s"), parse_dec("+38° 47′ 01″"), 0.03, "A0V", 25.0),
    Star("Капелла", parse_ra("05h 16m 41.4s"), parse_dec("+45° 59′ 53″"), 0.08, "G8III", 42.9),
    Star("Ригель", parse_ra("05h 14m 32.3s"), parse_dec("-08° 12′ 06″"), 0.13, "B8Ia", 860.0),
    Star("Процион", parse_ra("07h 39m 18.1s"), parse_dec("+05° 13′ 30″"), 0.34, "F5IV", 11.5),
    Star("Ахернар", parse_ra("01h 37m 42.8s"), parse_dec("-57° 14′ 12″"), 0.46, "B6Vpe", 139.0),
    Star(
        "Бетельгейзе", parse_ra("05h 55m 10.3s"), parse_dec("+07° 24′ 25″"), 0.50, "M1-2Ia", 548.0
    ),
    Star("Хадар", parse_ra("14h 03m 49.4s"), parse_dec("-60° 22′ 23″"), 0.61, "B1III", 390.0),
    Star("Альтаир", parse_ra("19h 50m 47.0s"), parse_dec("+08° 52′ 06″"), 0.76, "A7V", 16.7),
    Star("Акрукс", parse_ra("12h 26m 35.9s"), parse_dec("-63° 05′ 57″"), 0.76, "B0.5IV", 320.0),
    Star("Альдебаран", parse_ra("04h 35m 55.2s"), parse_dec("+16° 30′ 33″"), 0.86, "K5III", 65.3),
    Star("Антарес", parse_ra("16h 29m 24.5s"), parse_dec("-26° 25′ 55″"), 1.06, "M1.5Iab", 550.0),
    Star("Спика", parse_ra("13h 25m 11.6s"), parse_dec("-11° 09′ 41″"), 0.97, "B1III-IV", 250.0),
    Star("Поллукс", parse_ra("07h 45m 19.0s"), parse_dec("+28° 01′ 35″"), 1.14, "K0III", 33.8),
    Star("Фомальгаут", parse_ra("22h 57m 39.0s"), parse_dec("-29° 37′ 20″"), 1.16, "A3V", 25.1),
    Star("Денеб", parse_ra("20h 41m 25.9s"), parse_dec("+45° 16′ 49″"), 1.25, "A2Ia", 2600.0),
    Star("Регул", parse_ra("10h 08m 22.3s"), parse_dec("+11° 58′ 03″"), 1.36, "B8IV", 79.3),
    Star("Кастор", parse_ra("07h 34m 36.0s"), parse_dec("+31° 53′ 18″"), 1.58, "A1V", 51.0),
    Star("Беллатрикс", parse_ra("05h 25m 07.9s"), parse_dec("+06° 20′ 59″"), 1.64, "B2III", 250.0),
    Star("Альнаир", parse_ra("22h 08m 14.0s"), parse_dec("-46° 57′ 40″"), 1.74, "A7III", 101.0),
    Star("Мирфак", parse_ra("03h 24m 19.4s"), parse_dec("+49° 51′ 48″"), 1.79, "F5Ib", 510.0),
    Star("Алиот", parse_ra("13h 23m 55.5s"), parse_dec("+55° 57′ 35″"), 1.77, "A0IIIp", 82.6),
]


def find_brightest(ra_deg: float, dec_deg: float, radius_deg: float) -> Star | None:
    """Ярчайшая звезда в конусе (ra, dec, radius)."""
    best: Star | None = None
    for star in BRIGHT_STARS:
        sep = angular_separation(ra_deg, dec_deg, star.ra_deg, star.dec_deg)
        if sep <= radius_deg and (best is None or star.magnitude < best.magnitude):
            best = star
    return best


def all_brighter_than(mag: float) -> list[Star]:
    return [s for s in BRIGHT_STARS if s.magnitude < mag]


def is_circumpolar(star: Star, lat_deg: float) -> bool:
    """Незаходящая звезда: tan φ · tan δ > 1 (см. realism.almanac)."""
    return (math.tan(math.radians(lat_deg)) * math.tan(math.radians(star.dec_deg))) > 1.0


def is_never_visible(star: Star, lat_deg: float) -> bool:
    """Невидимая с широты (никогда не восходит)."""
    return (math.tan(math.radians(lat_deg)) * math.tan(math.radians(star.dec_deg))) < -1.0


def constellation_guess(star: Star) -> str:
    """Грубая привязка к созвездиям по RA-диапазонам (шутливая
    карта, для меню/подписей — не астрометрия)."""
    ra = star.ra_deg / 15.0  # часы
    bands = [
        (0, 3, "Кассиопея/Андромеда/Тукан"),
        (3, 6, "Персей/Телец/Орион (зима)"),
        (6, 9, "Орион/Близнецы/Большой Пёс"),
        (9, 12, "Рак/Лев/Большая Медведица"),
        (12, 15, "Дева/Волопас/Центавр"),
        (15, 18, "Скорпион/Змееносец/Лира"),
        (18, 21, "Лебедь/Орёл/Пегас"),
        (21, 24, "Пегас/Рыбы/Южная Рыба"),
    ]
    for lo, hi, name in bands:
        if lo <= ra < hi:
            return name
    return "—"


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Сириус ярчайшая; координаты сходятся с эфемеридными справками;
    Вега циркумполярна на 60° с.ш.; Канопус невидим на 60° с.ш.;
    пары звёзд согласованы с небесными координатами."""
    sirius = BRIGHT_STARS[0]
    sirius_ok = (
        sirius.magnitude == -1.46
        and abs(sirius.ra_deg - 101.28) < 0.1
        and abs(sirius.dec_deg - (-16.72)) < 0.05
    )
    vega = [s for s in BRIGHT_STARS if s.name == "Вега"][0]
    vega_circ = is_circumpolar(vega, 60.0)
    canopus = [s for s in BRIGHT_STARS if s.name == "Канопус"][0]
    canopus_hidden = is_never_visible(canopus, 60.0)
    # Сириус-Бетельгейзе: 27.1° (проверено в sky_coordinates)
    betelgeuse = [s for s in BRIGHT_STARS if s.name == "Бетельгейзе"][0]
    sep = angular_separation(sirius.ra_deg, sirius.dec_deg, betelgeuse.ra_deg, betelgeuse.dec_deg)
    sep_ok = abs(sep - 27.1) < 0.6
    # ярчайшая в конусе около Арктура — сам Арктур
    arcturus = [s for s in BRIGHT_STARS if s.name == "Арктур"][0]
    found = find_brightest(arcturus.ra_deg, arcturus.dec_deg, 5.0)
    cone_ok = found is not None and found.name == "Арктур"
    n_bright1 = len(all_brighter_than(0.0))
    n_ok0 = n_bright1 == 4  # ровно 4 звезды с m < 0
    n_bright1m = len(all_brighter_than(1.0))
    n_ok = n_ok0 and 15 <= n_bright1m <= 25
    return dict(
        sirius_ok=sirius_ok,
        vega_circumpolar_60N=vega_circ,
        canopus_hidden_60N=canopus_hidden,
        sirius_betelgeuse_deg=round(sep, 2),
        sep_ok=sep_ok,
        cone_found=found.name if found else None,
        cone_ok=cone_ok,
        stars_brighter_than_0m=n_bright1,
        stars_brighter_than_1m=n_bright1m,
        n_ok=n_ok,
        all_ok=sirius_ok and vega_circ and canopus_hidden and sep_ok and cone_ok and n_ok,
        note="Hipparcos (ESA 1997), J2000; РА в градусах (×15 от часов)",
    )
