#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — столкновения: resolve, слияние, дробление.

Модели:
  * PerfectMerge — неупругое слияние с сохранением импульса/массы
    (потеря энергии уходит в тепло — фиксируем диссипацию);
  * Bounce — упругое отражение с коэффициентом восстановления ε;
  * MergeFragment — слияние + осколки: при ударной энергии выше
    порога выбрасываются фрагменты с разлётом по изотропному конусу
    (консервативная проверка импульса);
  * Радиус Хилла — минимальный зазор для регистрации близкого пролёта.

Обнаружение: попарный тест O(N²) (N≤8 — достаточно), события пишутся
в формате scene.events.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Optional

from lab.body import Body


@dataclass
class CollisionEvent:
    """Зарегистрированное столкновение/сближение."""

    t: float
    body_a: str
    body_b: str
    kind: str  # merge | bounce | fragment | close_pass
    energy_before: float
    energy_after: float
    detail: str = ""


# ═══════════════════════════════════════════════════════════════════════════
# Слияние
# ═══════════════════════════════════════════════════════════════════════════
def merge_bodies(a: Body, b: Body) -> Body:
    """Идеально неупругое слияние: масса/импульс сохраняются, энергия нет.

    Радиус объединённого тела — по равному объёму (сферическая модель).
    """
    m = a.mass + b.mass
    if m <= 0:
        raise ValueError("нулевая суммарная масса")
    pos = tuple((a.mass * p + b.mass * q) / m for p, q in zip(a.position, b.position))
    vel = tuple((a.mass * u + b.mass * v) / m for u, v in zip(a.velocity, b.velocity))
    # объём: R = (Ra³ + Rb³)^{1/3}
    radius = (a.radius**3 + b.radius**3) ** (1.0 / 3.0)
    merged = Body(
        id=f"{a.id}__{b.id}" if "__" not in a.id else a.id,
        name=f"{a.name}+{b.name}",
        mass=m,
        radius=radius,
        position=pos,
        velocity=vel,
        w=(a.w * a.mass + b.w * b.mass) / m,
        charge=a.charge + b.charge,
        circulation=a.circulation + b.circulation,
        color=a.color if a.mass >= b.mass else b.color,
        type="merged",
        source=f"merge({a.source};{b.source})",
    )
    merged.metadata["merged_from"] = [a.id, b.id]
    return merged


def merge_energy_loss(a: Body, b: Body, G: float = 6.67430e-11) -> float:
    """Потеря кинетической энергии в системе ЦМ при слиянии."""
    m = a.mass + b.mass
    mu = a.mass * b.mass / m
    v_rel_sq = sum((u - v) ** 2 for u, v in zip(a.velocity, b.velocity))
    return 0.5 * mu * v_rel_sq


# ═══════════════════════════════════════════════════════════════════════════
# Упругий отскок
# ═══════════════════════════════════════════════════════════════════════════
def bounce(a: Body, b: Body, restitution: float = 1.0) -> None:
    """Упругий (ε=1) или частично упругий отскок вдоль нормали (на месте).

    Импульс сохраняется точно; при ε<1 нормальная компонента
    относительной скорости гасится.
    """
    if not (0.0 <= restitution <= 1.0):
        raise ValueError("restitution ∈ [0,1]")
    # нормаль
    dx = b.position[0] - a.position[0]
    dy = b.position[1] - a.position[1]
    dz = b.position[2] - a.position[2]
    d = math.sqrt(dx * dx + dy * dy + dz * dz)
    if d <= 0:
        return
    n = (dx / d, dy / d, dz / d)
    # относительная скорость вдоль нормали
    v_rel_n = sum((b.velocity[k] - a.velocity[k]) * n[k] for k in range(3))
    if v_rel_n >= 0:
        return  # уже разлетаются
    # импульс обмена
    mu = a.mass * b.mass / (a.mass + b.mass)
    j = -(1 + restitution) * mu * v_rel_n
    for k in range(3):
        av = list(a.velocity)
        bv = list(b.velocity)
        av[k] -= j * n[k] / a.mass
        bv[k] += j * n[k] / b.mass
        a.velocity = tuple(av)
        b.velocity = tuple(bv)


# ═══════════════════════════════════════════════════════════════════════════
# Дробление с фрагментами
# ═══════════════════════════════════════════════════════════════════════════
def fragment_on_impact(
    a: Body, b: Body, threshold_j_per_kg: float = 1e5, n_fragments: int = 3, seed: int = 42
) -> tuple[Body | None, list[Body]]:
    """Слияние или разрушение: если удельная энергия выше порога —
    меньшее тело разрушается на n_fragments осколков (сохранение
    импульса суммарно), большее сохраняется.

    Возвращает (остаток_крупного | None, список_осколков).
    """
    rng = random.Random(seed)
    impact_e = merge_energy_loss(a, b)
    smaller, larger = (a, b) if a.mass <= b.mass else (b, a)
    specific_e = impact_e / max(smaller.mass, 1e-30)
    if specific_e < threshold_j_per_kg:
        # порог не пробит — обычное слияние
        return merge_bodies(a, b), []
    # разрушение меньшего: осколки равной массы
    frag_mass = smaller.mass / n_fragments
    frag_radius = smaller.radius / n_fragments ** (1.0 / 3.0)
    frags: list[Body] = []
    # изотропные направления разлёта в плоскости, перпендикулярной линии
    dx, dy, dz = (b.position[k] - a.position[k] for k in range(3))
    d = math.sqrt(dx * dx + dy * dy + dz * dz) or 1.0
    # скорость разлёта из энергии разрушения (половина в кинематику)
    v_eject = math.sqrt(2.0 * max(impact_e * 0.5, 0.0) / smaller.mass)
    # базис: нормаль удара + два ортогональных (для конуса разлёта)
    n_vec = (dx / d, dy / d, dz / d)
    ref = (0.0, 1.0, 0.0) if abs(n_vec[1]) < 0.9 else (1.0, 0.0, 0.0)
    u_vec = tuple(n_vec[k] * ref[(k + 1) % 3] - n_vec[(k + 1) % 3] * ref[k] for k in range(3))
    u_len = math.sqrt(sum(c * c for c in u_vec)) or 1.0
    u_vec = tuple(c / u_len for c in u_vec)
    w_vec = (
        n_vec[1] * u_vec[2] - n_vec[2] * u_vec[1],
        n_vec[2] * u_vec[0] - n_vec[0] * u_vec[2],
        n_vec[0] * u_vec[1] - n_vec[1] * u_vec[0],
    )
    # случайные направления в конусе вокруг нормали
    dirs = []
    for i in range(n_fragments):
        theta = rng.uniform(0, 2 * math.pi)
        cos_phi = rng.uniform(0.3, 1.0)
        sin_phi = math.sqrt(1 - cos_phi**2)
        dirs.append(
            tuple(
                sin_phi * math.cos(theta) * u_vec[k]
                + sin_phi * math.sin(theta) * w_vec[k]
                + cos_phi * n_vec[k]
                for k in range(3)
            )
        )
    # АНТИСИММЕТРИЯ: убираем средний дрейф направлений, чтобы
    # Σ m_f·v_f = m_s·v_s точно (осколки наследуют скорость меньшего
    # тела; возмущения разлёта в сумме дают ноль)
    mean_dir = tuple(sum(dd[k] for dd in dirs) / len(dirs) for k in range(3))
    dirs = [tuple(dd[k] - mean_dir[k] for k in range(3)) for dd in dirs]
    v_base = smaller.velocity
    for i, direction in enumerate(dirs):
        vel = tuple(v_base[k] + v_eject * direction[k] for k in range(3))
        frags.append(
            Body(
                id=f"{smaller.id}_frag{i}",
                name=f"{smaller.name} осколок {i}",
                mass=frag_mass,
                radius=frag_radius,
                position=tuple(
                    c + 1.001 * smaller.radius * direction[k]
                    for k, c in enumerate(smaller.position)
                ),
                velocity=vel,
                color=smaller.color,
                type="fragment",
                source=f"fragment({smaller.source})",
            )
        )
    # импульс меньшего тела полностью передан осколкам; большое тело
    # сохраняет свою скорость — полный импульс пары соблюдён
    return larger, frags


# ═══════════════════════════════════════════════════════════════════════════
# Детектор столкновений для сцены
# ═══════════════════════════════════════════════════════════════════════════
def detect_collisions(bodies: list[Body], extra_gap: float = 0.0) -> list[tuple[int, int]]:
    """Индексы пар с перекрытием (d < r1 + r2 + gap)."""
    pairs = []
    n = len(bodies)
    for i in range(n):
        for j in range(i + 1, n):
            d = bodies[i].distance_to(bodies[j])
            rsum = bodies[i].radius + bodies[j].radius + extra_gap
            if d < rsum:
                pairs.append((i, j))
    return pairs


def resolve_all(scene, restitution: float = 0.0, merge: bool = True) -> list[CollisionEvent]:
    """Обработать все столкновения сцены за шаг (события в scene.events)."""
    events: list[CollisionEvent] = []
    bodies = scene.bodies
    changed = True
    guard = 0
    while changed and guard < 10:
        changed = False
        guard += 1
        pairs = detect_collisions(bodies)
        if not pairs:
            break
        i, j = pairs[0]
        a, b = bodies[i], bodies[j]
        e_before = scene.total_energy()
        if merge and restitution == 0.0:
            merged = merge_bodies(a, b)
            bodies.pop(max(i, j))
            bodies.pop(min(i, j))
            bodies.append(merged)
            kind = "merge"
            detail = f"{a.id}+{b.id} → {merged.id}: " f"m={merged.mass:.3g} кг"
        else:
            bounce(a, b, restitution)
            kind = "bounce"
            detail = f"{a.id}↔{b.id}: отскок ε={restitution}"
        e_after = scene.total_energy()
        ev = CollisionEvent(
            t=scene.t,
            body_a=a.id,
            body_b=b.id,
            kind=kind,
            energy_before=e_before,
            energy_after=e_after,
            detail=detail,
        )
        events.append(ev)
        scene.events.append(dict(kind=f"collision_{kind}", t=scene.t, detail=detail))
        changed = True
    return events


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка: законы сохранения
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Слияние сохраняет импульс; отскок — импульс и (ε=1) энергию."""
    a = Body(id="a", name="A", mass=2.0, radius=1.0, position=(0, 0, 0), velocity=(3, -1, 2))
    b = Body(id="b", name="B", mass=3.0, radius=1.0, position=(1.5, 0, 0), velocity=(-1, 4, 0))
    merged = merge_bodies(a, b)
    p_before = tuple(a.mass * u + b.mass * v for u, v in zip(a.velocity, b.velocity))
    p_after = tuple(merged.mass * u for u in merged.velocity)
    momentum_ok = all(abs(x - y) < 1e-12 for x, y in zip(p_before, p_after))

    # отскок: импульс сохраняется, энергия при ε=1 — тоже
    c = Body(id="c", name="C", mass=1.0, radius=1.0, position=(0, 0, 0), velocity=(2, 0, 0))
    d = Body(id="d", name="D", mass=1.0, radius=1.0, position=(1.9, 0, 0), velocity=(-2, 0, 0))
    p0 = tuple(c.mass * u + d.mass * v for u, v in zip(c.velocity, d.velocity))
    e0 = c.kinetic_energy() + d.kinetic_energy()
    bounce(c, d, restitution=1.0)
    p1 = tuple(c.mass * u + d.mass * v for u, v in zip(c.velocity, d.velocity))
    e1 = c.kinetic_energy() + d.kinetic_energy()
    momentum_bounce = all(abs(x - y) < 1e-12 for x, y in zip(p0, p1))
    energy_bounce = abs(e1 - e0) < 1e-9

    # дробление: суммарный импульс осколков ≈ импульсу ЦМ
    big = Body(
        id="big", name="Big", mass=1000.0, radius=5.0, position=(0, 0, 0), velocity=(0, 0, 0)
    )
    small = Body(
        id="sm", name="Small", mass=1.0, radius=0.5, position=(5.4, 0, 0), velocity=(-3000.0, 0, 0)
    )
    rest, frags = fragment_on_impact(big, small, threshold_j_per_kg=1e4, n_fragments=4)
    p_frags = [f.mass * f.velocity[0] for f in frags]
    # импульс сохранён: m_s·v_s + m_b·v_b = Σ m_f·v_f + m_b·v_b'
    p_in = small.mass * small.velocity[0]
    p_out = sum(p_frags) - big.mass * rest.velocity[0]
    fragment_ok = abs(p_out - p_in) / max(abs(p_in), 1e-9) < 1e-9
    return dict(
        merge_momentum_ok=momentum_ok,
        bounce_momentum_ok=momentum_bounce,
        bounce_energy_ok=energy_bounce,
        fragment_momentum_ok=fragment_ok,
        n_fragments=len(frags),
        all_ok=momentum_ok and momentum_bounce and energy_bounce and fragment_ok,
    )
