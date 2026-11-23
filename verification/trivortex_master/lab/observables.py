#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Наблюдаемые величины лаборатории: кривые лучевых скоростей, транзиты,
доплер, эффект Доплера, сближения. Для связки «симуляция → наблюдательная
астрономия» в отчётах.
"""

from __future__ import annotations

import math
from typing import Sequence


def radial_velocity(body_state, observer_dir=(1.0, 0.0, 0.0)) -> float:
    """Лучевая скорость: проекция скорости на направление наблюдателя."""
    v = sum(a * b for a, b in zip(body_state[3:6], observer_dir))
    return v


def transit_depth(r_planet: float, r_star: float) -> float:
    """Глубина транзита (r_p/R_*)²."""
    return (r_planet / max(r_star, 1e-12)) ** 2


def doppler_shift(f0: float, v_los: float, c: float = 2.998e8) -> float:
    """Релятивистский (1-й порядок) доплер: Δf/f = v/c."""
    return f0 * v_los / c


def light_curve_transit(phase: float, depth: float, width: float = 0.1) -> float:
    """Простая-box модель кривой блеска: единица вне, 1−depth внутри."""
    ph = phase % 1.0
    if 0.5 - width / 2 <= ph <= 0.5 + width / 2:
        return 1.0 - depth
    return 1.0


def separation_history(traj, body_a: int = 0, body_b: int = 1) -> list[float]:
    """История расстояний между двумя телами по Trajectory."""
    return [math.dist(st[body_a][:3], st[body_b][:3]) for st in traj.states]


def closest_approach(traj, body_a: int = 0, body_b: int = 1) -> tuple[float, int]:
    """(минимальное расстояние, индекс кадра)."""
    ds = separation_history(traj, body_a, body_b)
    if not ds:
        return (float("inf"), -1)
    dmin = min(ds)
    return (dmin, ds.index(dmin))
