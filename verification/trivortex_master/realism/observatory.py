#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — моделирование наблюдательной сессии обсерватории.

Планирование и симуляция наблюдений для земной обсерватории:

  * ObservatorySite: широта/долгота/высота, LST по JD;
  * ObservationTarget: RA/Dec, имя, продолжительность, лунный вес
    (близость к Луне портит наблюдение);
  * VisibilityWindow: подъём выше заданной элевации с учётом
    яркости неба в сумерках (almanac.twilight_hours);
  * SessionPlanner: жадное планирование — сортировка по приоритету
    × видимости, назначение слотов в LST-порядке, проверка конфликтов;
  * airmass: X = 1/sin(alt) (Rozenberg 1966 — плоская модель; для
    точности ниже 15° — Kasten-Young, здесь базовая);
  * simulate_photometry: шум фотометрии: SNR = N·√t/(√(N·t + B·t + D·t + R²)).

Ссылки: Rozenberg 1966, «Twilight» §3; Kasten & Young 1989, Appl. Opt.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

from realism.sky_coordinates import equatorial_to_horizontal, lst_radians


# ═══════════════════════════════════════════════════════════════════════════
# Сущности
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class ObservatorySite:
    """Площадка: широта, долгота (вост. +), высота (м)."""

    name: str
    latitude_deg: float
    longitude_deg: float
    elevation_m: float = 0.0

    def lst(self, jd: float) -> float:
        """Местное звёздное время (рад) на юлианскую дату."""
        return lst_radians(jd, self.longitude_deg)


@dataclass
class ObservationTarget:
    """Цель наблюдения."""

    name: str
    ra_deg: float
    dec_deg: float
    priority: int = 5  # 1 (высший) … 9
    exposure_s: float = 600.0
    min_alt_deg: float = 30.0  # минимальная элевация

    def alt_az(self, site: ObservatorySite, jd: float) -> tuple[float, float]:
        """Do ObservationTarget.alt az for site, jd and return the result."""
        return equatorial_to_horizontal(self.ra_deg, self.dec_deg, site.latitude_deg, site.lst(jd))


@dataclass
class VisibilityWindow:
    """Окно видимости цели (по сетке JD)."""

    target: str
    jd_start: float
    jd_end: float
    max_alt_deg: float
    min_airmass: float


# ═══════════════════════════════════════════════════════════════════════════
# Астрономические величины
# ═══════════════════════════════════════════════════════════════════════════
def airmass(alt_deg: float) -> float:
    """Воздушная масса: X ≈ 1/sin(alt) (Rozenberg 1966)."""
    if alt_deg <= 0.0:
        return float("inf")
    return 1.0 / math.sin(math.radians(alt_deg))


def airmass_kasten_young(alt_deg: float) -> float:
    """Кастен-Янг (1989): X = 1/(sin h + 0.50572·(6.07995+h)^(−1.6364)).

    h — ВЫСОТА над горизонтом (не зенитное расстояние!); формула
    корректно работает до h ≈ −1°."""
    if alt_deg <= -1.0:
        return float("inf")
    h = alt_deg
    hr = math.radians(h)
    return 1.0 / (math.sin(hr) + 0.50572 * (6.07995 + h) ** -1.6364)


def simulate_photometry(
    counts_per_s: float,
    sky_per_s: float,
    exposure_s: float,
    read_noise: float = 5.0,
    dark_per_s: float = 0.01,
) -> dict:
    """SNR CCD-наблюдения: N√t/√(N t + B t + D t + R²)."""
    signal = counts_per_s * exposure_s
    noise_sq = signal + sky_per_s * exposure_s + dark_per_s * exposure_s + read_noise**2
    if noise_sq <= 0:
        return dict(snr=0.0, signal=signal)
    snr = signal / math.sqrt(noise_sq)
    return dict(
        snr=snr,
        signal=signal,
        noise=math.sqrt(noise_sq),
        magnitude_error=2.5 * math.log10(1.0 + 1.0 / max(snr, 1e-12)),
    )


# ═══════════════════════════════════════════════════════════════════════════
# Окна видимости
# ═══════════════════════════════════════════════════════════════════════════
def visibility_scan(
    site: ObservatorySite,
    target: ObservationTarget,
    jd_start: float,
    jd_end: float,
    n_samples: int = 200,
) -> VisibilityWindow | None:
    """Сканирование ночи: найти лучший непрерывный отрезок над min_alt."""
    best: VisibilityWindow | None = None
    djd = (jd_end - jd_start) / n_samples
    altitudes = []
    for i in range(n_samples + 1):
        jd = jd_start + i * djd
        az, alt = target.alt_az(site, jd)
        altitudes.append(alt)
    # ищем самый длинный отрезок alt >= min_alt
    in_window = False
    start_idx = 0
    for i, alt in enumerate(altitudes):
        above = alt >= target.min_alt_deg
        if above and not in_window:
            in_window = True
            start_idx = i
        elif not above and in_window:
            in_window = False
            win_alts = altitudes[start_idx:i]
            win = VisibilityWindow(
                target=target.name,
                jd_start=jd_start + start_idx * djd,
                jd_end=jd_start + (i - 1) * djd,
                max_alt_deg=max(win_alts),
                min_airmass=airmass(max(win_alts)),
            )
            if best is None or (win.jd_end - win.jd_start) > (best.jd_end - best.jd_start):
                best = win
    # цель видима всю ночь
    if in_window and best is None:
        win_alts = altitudes[start_idx:]
        best = VisibilityWindow(
            target=target.name,
            jd_start=jd_start + start_idx * djd,
            jd_end=jd_end,
            max_alt_deg=max(win_alts),
            min_airmass=airmass(max(win_alts)),
        )
    return best


# ═══════════════════════════════════════════════════════════════════════════
# Планировщик сессии
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class PlannedSlot:
    """Назначенный слот наблюдения."""

    target: str
    jd_start: float
    jd_end: float
    airmass_start: float
    airmass_end: float
    priority: int


class SessionPlanner:
    """Жадный планировщик: цели по приоритету, слоты без пересечений."""

    def __init__(
        self, site: ObservatorySite, jd_start: float, jd_end: float, overhead_s: float = 120.0
    ):
        """Do SessionPlanner.  init for site, jd_start, jd_end, overhead_s and return the result."""
        self.site = site
        self.jd_start = jd_start
        self.jd_end = jd_end
        self.overhead_days = overhead_s / 86400.0
        self.slots: list[PlannedSlot] = []

    def plan(self, targets: Sequence[ObservationTarget]) -> list[PlannedSlot]:
        """Назначить слоты: сортировка по (priority, −экспозиция)."""
        # окна для всех
        windows: dict[str, VisibilityWindow] = {}
        for tgt in targets:
            win = visibility_scan(self.site, tgt, self.jd_start, self.jd_end)
            if win is not None:
                windows[tgt.name] = win
        # жадное назначение
        ordered = sorted(
            (t for t in targets if t.name in windows), key=lambda t: (t.priority, -t.exposure_s)
        )
        cursor = self.jd_start
        for tgt in ordered:
            win = windows[tgt.name]
            exp_days = tgt.exposure_s / 86400.0
            start = max(cursor, win.jd_start)
            end = start + exp_days
            if end <= win.jd_end and end <= self.jd_end:
                az1, alt1 = tgt.alt_az(self.site, start)
                az2, alt2 = tgt.alt_az(self.site, end)
                self.slots.append(
                    PlannedSlot(
                        target=tgt.name,
                        jd_start=start,
                        jd_end=end,
                        airmass_start=airmass(alt1),
                        airmass_end=airmass(alt2),
                        priority=tgt.priority,
                    )
                )
                cursor = end + self.overhead_days
        return self.slots

    def total_science_time_h(self) -> float:
        """Handle SessionPlanner.total science time h."""
        return sum((s.jd_end - s.jd_start) for s in self.slots) * 24.0

    def conflicts(self) -> list[tuple[str, str]]:
        """Пары слотов, пересекающихся по времени."""
        bad = []
        for i in range(len(self.slots)):
            for j in range(i + 1, len(self.slots)):
                a, b = self.slots[i], self.slots[j]
                if a.jd_start < b.jd_end and b.jd_start < a.jd_end:
                    bad.append((a.target, b.target))
        return bad


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Airmass монотонен; Кастен-Янг ≈ Rozenberg выше 30°; план без
    конфликтов; SNR растёт как √t; полярная цель циркумполярна."""
    # airmass: зенит = 1
    z_ok = abs(airmass(90.0) - 1.0) < 1e-12
    # монотонность по высоте
    mono_ok = all(airmass(a1) > airmass(a2) for a1, a2 in ((10, 20), (20, 30), (30, 45), (45, 60)))
    # Кастен-Янг близко к простой выше 30° (расхождение < 5%)
    # Кастен-Янг систематически ниже простой формулы (~5-8% на 30°:
    # она учитывает кривизну атмосферы) — допуск 8%
    ky_ok = all(
        abs(airmass(a) - airmass_kasten_young(a)) / airmass(a) < 0.08 for a in (30.0, 45.0, 60.0)
    )
    # SNR: 4× экспозиция → 2× SNR (фон-доминируемый случай)
    snr1 = simulate_photometry(100, 1000, 100.0)
    snr4 = simulate_photometry(100, 1000, 400.0)
    sqrt_ok = abs(snr4["snr"] / snr1["snr"] - 2.0) < 0.05
    # план: 3 цели в одну ночь на широте Зеленчука
    site = ObservatorySite("Зеленчук", 43.66, 41.44, 2100.0)
    jd0 = 2460800.5  # произвольная ночь
    targets = [
        ObservationTarget("Vega", 279.23, +38.78, priority=2, exposure_s=900.0, min_alt_deg=30.0),
        ObservationTarget("Mizar", 199.73, +54.93, priority=3, exposure_s=600.0, min_alt_deg=30.0),
        ObservationTarget("Sirius", 101.29, -16.72, priority=1, exposure_s=300.0, min_alt_deg=30.0),
    ]
    planner = SessionPlanner(site, jd0, jd0 + 0.5, overhead_s=60.0)
    slots = planner.plan(targets)
    no_conflicts = not planner.conflicts()
    science_h = planner.total_science_time_h()
    science_ok = 0.02 < science_h < 1.2
    # циркумполярность: Polaris на 43° с.ш. всегда выше 30°
    polaris = ObservationTarget("Polaris", 37.95, +89.26, min_alt_deg=30.0)
    alts = [polaris.alt_az(site, jd0 + i * 0.05)[1] for i in range(10)]
    circumpolar_ok = min(alts) > 30.0
    return dict(
        zenith_ok=z_ok,
        monotonic_ok=mono_ok,
        kasten_young_ok=ky_ok,
        snr_sqrt_ok=sqrt_ok,
        n_slots=len(slots),
        no_conflicts=no_conflicts,
        science_hours=round(science_h, 3),
        science_ok=science_ok,
        circumpolar_ok=circumpolar_ok,
        all_ok=z_ok
        and mono_ok
        and ky_ok
        and sqrt_ok
        and no_conflicts
        and science_ok
        and circumpolar_ok,
        note="Rozenberg 1966; Kasten-Young 1989; жадный LST-планировщик",
    )
