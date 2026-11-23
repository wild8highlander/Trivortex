#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — орбитальные резонансы: положения, ширины, сверхпериоды.

Модуль резонансного анализа планетных систем:

  * resonance_location: положение p:q-резонанса по Кеплеру
    a_res = a_p·(q/p)^{2/3} (внутренний p:q — тело с меньшей a);
  * Kirkwood gaps: проверка против опубликованных положений
    (3:1 @ 2.502 а.е., 5:2 @ 2.824, 7:3 @ 2.958, 2:1 @ 3.279);
  * Wisdom overlap: полуширина хаотической зоны
    δa/a ≈ 1.5·(m_p/(3M))^{2/7} (Wisdom 1980, AJ 85, 1122);
  * TTV super-period: для пары у резонанса j:j−1
    P_super = 1/|j/P₂ − (j−1)/P₁| (Lithwick, Xie & Wu 2012, ApJ 761, 122);
  * Laplace-резонанс: отношение периодов Ио-Европа-Ганимед (4:2:1).

Самопроверки против наблюдаемых величин Солнечной системы.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

AU_M = 1.495978707e11
G_SI = 6.67430e-11


# ═══════════════════════════════════════════════════════════════════════════
# Положение резонанса
# ═══════════════════════════════════════════════════════════════════════════
def resonance_location(a_planet: float, p: int, q: int) -> float:
    """Большая полуось p:q-резонанса с планетой (а.е. → та же единица).

    Внутренний p:q (p > q): тело делает p оборотов на q оборотов
    планеты → P = P_p·q/p → a = a_p·(q/p)^{2/3}.
    """
    return a_planet * (q / p) ** (2.0 / 3.0)


KIRKWOOD_GAPS = {
    # имя: (опубликованное положение а.е., p, q) — тело делает p оборотов
    # на q оборотов Юпитера
    "3:1": (2.502, 3, 1),
    "5:2": (2.824, 5, 2),
    "7:3": (2.958, 7, 3),
    "2:1": (3.279, 2, 1),
}


def kirkwood_check(a_jupiter: float = 5.2038) -> dict:
    """Положения промежутков Кирквуда против опубликованных значений."""
    out = {}
    ok = True
    for name, (a_pub, p, q) in KIRKWOOD_GAPS.items():
        a_calc = resonance_location(a_jupiter, p, q)
        out[name] = dict(published_au=a_pub, computed_au=a_calc,
                         err_au=a_calc - a_pub)
        ok = ok and abs(a_calc - a_pub) < 0.015
    return dict(gaps=out, all_ok=ok,
                note="резонанс p:q с Юпитером: a = a_J·(q/p)^{2/3}")


# ═══════════════════════════════════════════════════════════════════════════
# Хаотическая зона (Wisdom 1980)
# ═══════════════════════════════════════════════════════════════════════════
def wisdom_chaotic_zone(m_planet: float, m_star: float,
                        a_planet: float) -> dict:
    """Полуширина хаотической зоны: δa/a ≈ 1.5·μ^{2/7}, μ = m_p/(3M).

    Wisdom 1980 (AJ 85, 1122); для Юпитера даёт ~0.7 а.е. с каждой
    стороны — внутренний край пояса астероидов у 2:1 (3.28 а.е.).
    """
    mu = m_planet / (3.0 * m_star)
    delta_ratio = 1.5 * mu ** (2.0 / 7.0)
    return dict(mu=mu, delta_ratio=delta_ratio,
                delta_au=delta_ratio * a_planet,
                inner_edge_au=a_planet - delta_ratio * a_planet,
                outer_edge_au=a_planet + delta_ratio * a_planet,
                reference="Wisdom 1980, AJ 85, 1122; Murray & Dermott §8.10")


def jupiter_zone_check() -> dict:
    """Хаотическая зона Юпитера: δa ∈ [0.5, 1.3] а.е. — литература."""
    res = wisdom_chaotic_zone(1.898e27, 1.9884e30, 5.2038)
    ok = 0.5 < res["delta_au"] < 1.3
    return dict(delta_au=res["delta_au"], ok=ok)


# ═══════════════════════════════════════════════════════════════════════════
# Лапласов резонанс (Ио-Европа-Ганимед)
# ═══════════════════════════════════════════════════════════════════════════
LAPLACE_PERIODS = dict(
    io=1.769138, europa=3.551181, ganymede=7.154553)   # сутки (NASA)


def laplace_ratios() -> dict:
    """Отношения периодов тройного лапласова резонанса (2:1, 4:1)."""
    p_io, p_eu, p_ga = (LAPLACE_PERIODS["io"],
                        LAPLACE_PERIODS["europa"],
                        LAPLACE_PERIODS["ganymede"])
    r1 = p_eu / p_io      # ≈ 2.008
    r2 = p_ga / p_io      # ≈ 4.044
    return dict(io_europa=r1, io_ganymede=r2,
                near_2_1=abs(r1 - 2.0) < 0.02,
                near_4_1=abs(r2 - 4.0) < 0.05,
                note="Ио-Европа-Ганимед: Лапласов резонанс 4:2:1; "
                     "фаза φ = λ₃ − 3λ₂ + 2λ₁ либрирует (Yoder 1979)")


def resonance_angle(lam_body: float, lam_perturber: float,
                    varpi_body: float, p: int, q: int) -> float:
    """Критический аргумент резонанса p:q: φ = p·λ_q − q·λ_p + (q−p)·ϖ.

    Либрация φ вокруг 0 (или π) — резонанс захвачен; циркуляция — нет.
    """
    return math.degrees((p * lam_perturber - q * lam_body
                         + (q - p) * varpi_body) % (2 * math.pi))


def is_librating(angles_deg: list[float], tol: float = 60.0) -> bool:
    """Грубая проверка либрации: разброс φ меньше tol градусов
    после приведения к ближайшей ветке (0 или 180)."""
    if len(angles_deg) < 3:
        return False
    best_center = None
    best_spread = float("inf")
    for center in (0.0, 180.0):
        wrapped = []
        for a in angles_deg:
            d = ((a - center + 180.0) % 360.0) - 180.0
            wrapped.append(d)
        spread = max(wrapped) - min(wrapped)
        if spread < best_spread:
            best_spread = spread
            best_center = center
    return best_spread < tol


# ═══════════════════════════════════════════════════════════════════════════
# TTV super-period (Lithwick, Xie & Wu 2012)
# ═══════════════════════════════════════════════════════════════════════════
def ttv_super_period(p_inner: float, p_outer: float, j: int) -> float:
    """Сверхпериод TTV пары у резонанса j:j−1.

    P_super = 1/|j/P_outer − (j−1)/P_inner| (LXW12, eq. 2).
    Для точного резонанса → бесконечность (секулярная накопка).
    """
    rate = j / p_outer - (j - 1) / p_inner
    if abs(rate) < 1e-15:
        return float("inf")
    return 1.0 / abs(rate)


def ttv_pair_report(p_inner: float, p_outer: float) -> dict:
    """Диагностика пары: ближайший резонанс и ожидаемый сверхпериод."""
    ratio = p_outer / p_inner
    best = None
    for j in range(2, 8):
        exact = j / (j - 1)
        delta = abs(ratio - exact)
        if best is None or delta < best[1]:
            best = (j, delta)
    j = best[0]
    p_super = ttv_super_period(p_inner, p_outer, j)
    return dict(period_ratio=ratio, resonance=f"{j}:{j - 1}",
                offset=best[1], super_period_days=p_super,
                reference="Lithwick, Xie & Wu 2012, ApJ 761, 122")


def kepler_9_check() -> dict:
    """Kepler-9 b/c (Holman et al. 2010): P=19.24/38.91 сут, у 2:1.

    Сверхпериод по формуле LXW12: 1/|2/38.91 − 1/19.24| ≈ 1730 сут —
    порядок совпадает с модуляцией TTV (~1.7 тыс. сут в модели 2010).
    """
    rep = ttv_pair_report(19.2389, 38.9076)
    return dict(**rep, plausible=1000.0 < rep["super_period_days"] < 4000.0)


# ═══════════════════════════════════════════════════════════════════════════
# Ширина резонанса первого порядка
# ═══════════════════════════════════════════════════════════════════════════
def first_order_width(mu: float, e: float, j: int) -> float:
    """Полуширина резонанса j:j−1 в единицах a (Murray & Dermott 1999).

    δa/a ≈ (16·μ·f(j)·e) для малых e — используем классическую форму
    с f ≈ 1.0 для оценки (точность до фактора 2)."""
    return math.sqrt(16.0 * mu * max(e, 1e-6))


def self_check() -> dict:
    """Кирквуд + Лаплас + Wisdom + LXW12 super-period."""
    kw = kirkwood_check()
    lap = laplace_ratios()
    jz = jupiter_zone_check()
    k9 = kepler_9_check()
    # либрация: синус около 0 распознаётся, тренд — нет
    lib = [math.degrees(math.sin(t * 0.1)) for t in range(20)]
    circ = [t * 7.5 % 360 for t in range(20)]
    ok = (kw["all_ok"] and lap["near_2_1"] and lap["near_4_1"]
          and jz["ok"] and k9["plausible"]
          and is_librating(lib) and not is_librating(circ))
    return dict(
        kirkwood_ok=kw["all_ok"],
        laplace_2_1=lap["io_europa"], laplace_4_1=lap["io_ganymede"],
        wisdom_delta_au=jz["delta_au"],
        k9_super_period=k9["super_period_days"],
        libration_ok=is_librating(lib),
        circulation_ok=not is_librating(circ),
        all_ok=ok,
    )
