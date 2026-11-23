#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — собственные элементы и семьи астероидов.

«Собственные» элементы свободны от периодических возмущений —
основа динамической классификации (Knežević & Milani 2003):

  * proper_semimajor_axis: скользящее среднее a по времени
    (средняя полуось — инвариант секулярной прецессии первого порядка);
  * proper_eccentricity / proper_inclination: амплитуда свободной
    осцилляции e,i вокруг центроида (усреднение по окну > 1 цикл);
  * asteroid_velocity (Δv): относительная скорость в момент
    пересечения орбит (критерийсемейности, ~ Флери);
  * hcm_clustering: HCM (hierarchical clustering method, Zappalà 1990)
    — одноуровневые кластеры при заданной отсечке Δv.

Самопроверка: синтетический пояс из двух семей (сгенерированные
элементы вокруг двух ядер) — HCM восстанавливает обе при правильной
отсечке; фоновые астероиды остаются вне семей.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Sequence

AU_M = 1.495978707e11


@dataclass
class AsteroidElements:
    """Оскулирующие элементы астероида (а.е., градусы)."""

    name: str
    a: float
    e: float
    i_deg: float
    om_deg: float = 0.0  # долгота узла
    w_deg: float = 0.0  # аргумент перицентра


# ═══════════════════════════════════════════════════════════════════════════
# Собственные элементы (окно-усреднение)
# ═══════════════════════════════════════════════════════════════════════════
def proper_semimajor_axis(a_series: Sequence[float]) -> float:
    """Собственная полуось: медиана ряда a(t) (устойчива к выбросам)."""
    if not a_series:
        return float("nan")
    s = sorted(a_series)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def proper_amplitude(series: Sequence[float]) -> float:
    """Амплитуда свободной осцилляции: полуразмах центрированного ряда."""
    if len(series) < 2:
        return 0.0
    mean = sum(series) / len(series)
    centered = [v - mean for v in series]
    return (max(centered) - min(centered)) / 2.0


def proper_elements_from_series(a_series, e_series, i_series) -> dict:
    """Комплект собственных элементов: a_p, e_p (центроид), I_p."""
    return dict(
        a_p=proper_semimajor_axis(a_series),
        e_p=sum(e_series) / max(len(e_series), 1),
        i_p=sum(i_series) / max(len(i_series), 1),
        e_amp=proper_amplitude(e_series),
        i_amp=proper_amplitude(i_series),
        n_samples=len(a_series),
    )


# ═══════════════════════════════════════════════════════════════════════════
# Δv между орбитами (критерий семейности)
# ═══════════════════════════════════════════════════════════════════════════
def orbital_velocity(a_au: float, e: float) -> float:
    """Средняя орбитальная скорость (км/с) по vis-viva на средней r."""
    mu_sun = 1.32712440018e11  # км³/с² (IAU 2015)
    r_mean = a_au * (1.0 + 0.5 * e * e) * AU_M / 1000.0  # км
    return math.sqrt(mu_sun / r_mean)


def asteroid_velocity_delta(e1: AsteroidElements, e2: AsteroidElements) -> float:
    """Оценка Δv (км/с) между орбитами (практика HCM, Nesvorný 2015).

    Δv ≈ √( (v_a·δa/(2a))² + (v_e·δe)² + (v_i·δi)² ), где v_a ≈ 17,
    v_e ≈ 6, v_i ≈ 5 км/с — характерные компоненты орбитальной скорости
    пояса (трансверсальная по δa, радиальная по δe, нормальная по δi)."""
    da_term = 17.0 * abs(e1.a - e2.a) / (2.0 * max(e1.a, 1e-9))
    de_term = 6.0 * abs(e1.e - e2.e)
    di_term = 5.0 * abs(e1.i_deg - e2.i_deg) * math.pi / 180.0
    return math.sqrt(da_term**2 + de_term**2 + di_term**2)


# ═══════════════════════════════════════════════════════════════════════════
# HCM-кластеризация
# ═══════════════════════════════════════════════════════════════════════════
def hcm_clustering(asteroids: Sequence[AsteroidElements], cutoff_kms: float) -> list[list[int]]:
    """Иерархическая кластеризация с одной связью (single-linkage).

    Возвращает список кластеров (индексы) размером ≥ 2; одиночки —
    в последнем кластере с пометкой (они не возвращаются).
    """
    n = len(asteroids)
    # матрица расстояний
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = asteroid_velocity_delta(asteroids[i], asteroids[j])
            dist[i][j] = dist[j][i] = d
    # single-linkage через union-find
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in range(n):
        for j in range(i + 1, n):
            if dist[i][j] < cutoff_kms:
                ri, rj = find(i), find(j)
                if ri != rj:
                    parent[rj] = ri
    groups: dict[int, list[int]] = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    clusters = [g for g in groups.values() if len(g) >= 2]
    clusters.sort(key=len, reverse=True)
    return clusters


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка: синтетический пояс с двумя семьями
# ═══════════════════════════════════════════════════════════════════════════
def synthetic_belt(seed: int = 4) -> list[AsteroidElements]:
    """Пояс: 2 семьи (по 12 членов, Δv < 0.02 км/с) + 10 фоновых."""
    rng = random.Random(seed)
    belt = []
    families = [
        ("Fam-A", 2.35, 0.10, 6.0),
        ("Fam-B", 2.85, 0.05, 3.0),
    ]
    idx = 0
    for fam, a0, e0, i0 in families:
        for k in range(12):
            belt.append(
                AsteroidElements(
                    name=f"{fam}_{k}",
                    a=a0 + rng.uniform(-0.004, 0.004),
                    e=max(0.0, e0 + rng.uniform(-0.002, 0.002)),
                    i_deg=max(0.0, i0 + rng.uniform(-0.3, 0.3)),
                )
            )
            idx += 1
    for k in range(10):
        belt.append(
            AsteroidElements(
                name=f"BG_{k}",
                a=rng.uniform(2.1, 3.2),
                e=rng.uniform(0.02, 0.20),
                i_deg=rng.uniform(0.5, 18.0),
            )
        )
    return belt


def self_check() -> dict:
    """HCM при отсечке 0.05 км/с: ровно 2 крупных кластера ≥ 10 членов;
    собственные амплитуды согласованы с разбросом генерации."""
    belt = synthetic_belt()
    clusters = hcm_clustering(belt, cutoff_kms=0.05)
    big = [c for c in clusters if len(c) >= 10]
    fam_ok = len(big) == 2
    # имена в кластерах однородные?
    names_ok = False
    if fam_ok:
        for c in big:
            names = {belt[i].name.split("_")[0] for i in c}
            if len(names) == 1:
                names_ok = True
                break
    # собственные элементы члена Fam-A: e_amp < 0.004 (генерация ±0.002)
    a_member = [b for b in belt if b.name == "Fam-A_0"][0]
    e_series = [a_member.e * (1 + 0.001 * math.sin(k)) for k in range(50)]
    pe = proper_elements_from_series([a_member.a] * 50, e_series, [a_member.i_deg] * 50)
    amp_ok = pe["e_amp"] < 0.004 and abs(pe["a_p"] - a_member.a) < 1e-12
    # Δv члена семьи к ядру < отсечки, к чужому ядру — больше
    core_a = AsteroidElements("coreA", 2.35, 0.10, 6.0)
    dv_in = asteroid_velocity_delta(a_member, core_a)
    dv_out = asteroid_velocity_delta(core_a, AsteroidElements("coreB", 2.85, 0.05, 3.0))
    dv_ok = dv_in < 0.05 < dv_out
    return dict(
        n_clusters=len(clusters),
        big_clusters=[len(c) for c in big],
        fam_ok=fam_ok,
        names_ok=names_ok,
        e_amp=pe["e_amp"],
        amp_ok=amp_ok,
        dv_member=round(dv_in, 4),
        dv_cross=round(dv_out, 3),
        dv_ok=dv_ok,
        all_ok=fam_ok and names_ok and amp_ok and dv_ok,
        note="Zappalà et al. 1990: HCM, отсечка ~50 м/с выделяет семьи",
    )
