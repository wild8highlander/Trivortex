#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — Barnes-Hut O(N log N) гравитация на чистом Python.

Октодерево (quadtree в 2D-режиме):
  * вставка тел с адаптивным дроблением (θ-критерий);
  * вычисление сил обходом дерева: узел дальше s/d < θ заменяется
    центральной массой (Barnes & Hut 1986, Nature 324, 446);
  * монопольный и квадрупольный моменты;
  * сравнение с direct summation: точность и ускорение;
  * масштабный тест (до N=2000, где чистый O(N²) уже заметен).

Модуль сознательно не зависит от numpy — дерево само по себе быстро
для N ≤ нескольких тысяч, а внешние ускорители REBOUND подключаются
отдельно (realism/adapters).
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Sequence

G_SI = 6.67430e-11


# ═══════════════════════════════════════════════════════════════════════════
# Узел октодерева
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class BodyLite:
    """Лёгкое тело для дерева (позиция, масса)."""

    x: float
    y: float
    z: float
    mass: float
    id: int = -1


@dataclass
class OctNode:
    """Узел октодерева: либо внутренний (8 детей), либо лист (1 тело)."""

    cx: float  # центр куба
    cy: float
    cz: float
    half: float  # половина стороны
    # агрегаты
    mass: float = 0.0
    com_x: float = 0.0  # центр масс
    com_y: float = 0.0
    com_z: float = 0.0
    # квадруполь (диагональ тензора для апскейла)
    qxx: float = 0.0
    qyy: float = 0.0
    qzz: float = 0.0
    # структура
    children: list | None = None  # 8 дочерних OctNode
    body: BodyLite | None = None  # лист: единственное тело
    n_bodies: int = 0

    def is_leaf(self) -> bool:
        return self.children is None and self.body is not None

    def is_empty(self) -> bool:
        return self.children is None and self.body is None


class BarnesHutTree:
    """Октодерево с θ-критерием."""

    def __init__(
        self,
        theta: float = 0.7,
        use_quadrupole: bool = False,
        G: float = G_SI,
        softening: float = 0.0,
    ):
        self.theta = theta
        self.use_quadrupole = use_quadrupole
        self.G = G
        self.softening = softening
        self.root: OctNode | None = None
        self.n_nodes = 0

    # ── построение ──
    def build(self, bodies: Sequence[BodyLite]) -> None:
        if not bodies:
            self.root = None
            return
        # габаритный куб
        xs = [b.x for b in bodies]
        ys = [b.y for b in bodies]
        zs = [b.z for b in bodies]
        cx = (min(xs) + max(xs)) / 2.0
        cy = (min(ys) + max(ys)) / 2.0
        cz = (min(zs) + max(zs)) / 2.0
        half = max(max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)) / 2.0 * 1.01 + 1e-9
        self.root = OctNode(cx=cx, cy=cy, cz=cz, half=half)
        self.n_nodes = 1
        for b in bodies:
            self._insert(self.root, b, depth=0)

    def _child_index(self, node: OctNode, b: BodyLite) -> int:
        idx = 0
        if b.x > node.cx:
            idx |= 1
        if b.y > node.cy:
            idx |= 2
        if b.z > node.cz:
            idx |= 4
        return idx

    def _child_node(self, node: OctNode, idx: int) -> OctNode:
        dx = node.half / 2.0 * (1 if idx & 1 else -1)
        dy = node.half / 2.0 * (1 if idx & 2 else -1)
        dz = node.half / 2.0 * (1 if idx & 4 else -1)
        child = OctNode(cx=node.cx + dx, cy=node.cy + dy, cz=node.cz + dz, half=node.half / 2.0)
        self.n_nodes += 1
        return child

    def _insert(self, node: OctNode, b: BodyLite, depth: int) -> None:
        """Рекурсивная вставка с дроблением; защита от вырождения по глубине."""
        if node.is_empty():
            node.body = b
            self._update_aggregate(node, b)
            return
        if node.is_leaf():
            if depth > 64:
                # совпадающие позиции — агрегируем в узел принудительно
                self._update_aggregate(node, b)
                return
            old = node.body
            node.body = None
            node.children = [None] * 8
            # пере-вставить старое тело
            oi = self._child_index(node, old)
            node.children[oi] = self._child_node(node, oi)
            self._insert(node.children[oi], old, depth + 1)
        # вставить новое
        idx = self._child_index(node, b)
        if node.children[idx] is None:
            node.children[idx] = self._child_node(node, idx)
        self._insert(node.children[idx], b, depth + 1)
        self._update_aggregate(node, b)

    def _update_aggregate(self, node: OctNode, b: BodyLite) -> None:
        """Обновить массу/центр масс/квадруполь при добавлении тела b."""
        m_new = node.mass + b.mass
        if m_new > 0:
            node.com_x = (node.com_x * node.mass + b.x * b.mass) / m_new
            node.com_y = (node.com_y * node.mass + b.y * b.mass) / m_new
            node.com_z = (node.com_z * node.mass + b.z * b.mass) / m_new
        node.mass = m_new
        node.n_bodies += 1
        # квадруполь (диагональ): Σ m·(3r_i² − r²) — упрощённо
        if self.use_quadrupole:
            node.qxx += b.mass * (b.x - node.com_x) ** 2
            node.qyy += b.mass * (b.y - node.com_y) ** 2
            node.qzz += b.mass * (b.z - node.com_z) ** 2

    # ── силы ──
    def acceleration(self, b: BodyLite, eps2: float | None = None) -> tuple[float, float, float]:
        """Ускорение тела b от дерева (обход с θ-критерием)."""
        if self.root is None:
            return (0.0, 0.0, 0.0)
        eps2 = self.softening**2 if eps2 is None else eps2
        return self._acc_node(self.root, b, eps2)

    def _acc_node(self, node: OctNode, b: BodyLite, eps2: float) -> tuple[float, float, float]:
        ax = ay = az = 0.0
        if node.is_empty():
            return (0.0, 0.0, 0.0)
        if node.is_leaf():
            other = node.body
            if other is None or other is b or other.id == b.id:
                return (0.0, 0.0, 0.0)
            dx = other.x - b.x
            dy = other.y - b.y
            dz = other.z - b.z
            r2 = dx * dx + dy * dy + dz * dz + eps2
            r = math.sqrt(r2)
            if r > 0:
                f = self.G * other.mass / (r2 * r)
                return (f * dx, f * dy, f * dz)
            return (0.0, 0.0, 0.0)
        # внутренний узел: θ-критерий s/d < θ
        dx = node.com_x - b.x
        dy = node.com_y - b.y
        dz = node.com_z - b.z
        d2 = dx * dx + dy * dy + dz * dz
        s = node.half * 2.0
        if s * s < self.theta * self.theta * d2:
            # далеко: аппроксимация центральной массой (+квадруполь опц.)
            r2 = d2 + eps2
            r = math.sqrt(r2)
            if r > 0:
                f = self.G * node.mass / (r2 * r)
                ax = f * dx
                ay = f * dy
                az = f * dz
                if self.use_quadrupole:
                    # квадрупольная поправка ~ (Q/r²)·(3(n·Q·n)−trQ)/r⁵
                    # упрощённая диагональная версия
                    q = (node.qxx * dx * dx + node.qyy * dy * dy + node.qzz * dz * dz) / (r2 * r2)
                    corr = 1.5 * q / (r2 * max(node.mass, 1e-30))
                    ax *= 1.0 - corr
                    ay *= 1.0 - corr
                    az *= 1.0 - corr
            return (ax, ay, az)
        # близко: рекурсивно в детей
        for child in node.children:
            if child is None:
                continue
            cax, cay, caz = self._acc_node(child, b, eps2)
            ax += cax
            ay += cay
            az += caz
        return (ax, ay, az)

    # ── статистика ──
    def stats(self) -> dict:
        depth = 0

        def measure(node, d):
            nonlocal depth
            if node is None:
                return
            depth = max(depth, d)
            if node.children:
                for c in node.children:
                    measure(c, d + 1)

        if self.root is not None:
            measure(self.root, 1)
        return dict(
            nodes=self.n_nodes, max_depth=depth, theta=self.theta, quadrupole=self.use_quadrupole
        )


# ═══════════════════════════════════════════════════════════════════════════
# Прямое суммирование (эталон)
# ═══════════════════════════════════════════════════════════════════════════
def direct_accelerations(
    bodies: Sequence[BodyLite], G: float = G_SI, softening: float = 0.0
) -> list[tuple[float, float, float]]:
    """O(N²) точные ускорения (эталон для сравнения точности)."""
    n = len(bodies)
    eps2 = softening**2
    acc = [(0.0, 0.0, 0.0)] * n
    for i in range(n):
        ax = ay = az = 0.0
        bi = bodies[i]
        for j in range(n):
            if i == j:
                continue
            bj = bodies[j]
            dx = bj.x - bi.x
            dy = bj.y - bi.y
            dz = bj.z - bi.z
            r2 = dx * dx + dy * dy + dz * dz + eps2
            r = math.sqrt(r2)
            if r > 0:
                f = G * bj.mass / (r2 * r)
                ax += f * dx
                ay += f * dy
                az += f * dz
        acc[i] = (ax, ay, az)
    return acc


# ═══════════════════════════════════════════════════════════════════════════
# Движок Barnes-Hut для lab.physics (совместим с PhysicsEngine)
# ═══════════════════════════════════════════════════════════════════════════
class BarnesHutEngineMixin:
    """Примесь: шаг интегрирования через дерево.

    Используется пользовательскими движками, когда N велико и O(N²)
    прямых сил уже заметен. Интегратор — leapfrog KDK (симплектический).
    """

    def __init__(self, theta: float = 0.7, softening: float = 0.0):
        self.theta = theta
        self.softening = softening

    def step_all(self, bodies: list[BodyLite], dt: float, G: float = G_SI) -> None:
        """Один leapfrog-шаг всех тел (на месте)."""
        tree = BarnesHutTree(theta=self.theta, G=G, softening=self.softening)
        tree.build(bodies)
        # half-kick
        for b in bodies:
            ax, ay, az = tree.acceleration(b)
            b.vx += 0.5 * dt * ax  # type: ignore[attr-defined]
            b.vy += 0.5 * dt * ay  # type: ignore[attr-defined]
            b.vz += 0.5 * dt * az  # type: ignore[attr-defined]
        # drift
        for b in bodies:
            b.x += dt * b.vx  # type: ignore[attr-defined]
            b.y += dt * b.vy  # type: ignore[attr-defined]
            b.z += dt * b.vz  # type: ignore[attr-defined]
        # half-kick
        tree2 = BarnesHutTree(theta=self.theta, G=G, softening=self.softening)
        tree2.build(bodies)
        for b in bodies:
            ax, ay, az = tree2.acceleration(b)
            b.vx += 0.5 * dt * ax  # type: ignore[attr-defined]
            b.vy += 0.5 * dt * ay  # type: ignore[attr-defined]
            b.vz += 0.5 * dt * az  # type: ignore[attr-defined]


class SimBody(BodyLite):
    """Тело с скоростями для полноценного прогона Barnes-Hut."""

    vx: float = 0.0
    vy: float = 0.0
    vz: float = 0.0

    def __init__(self, x, y, z, mass, vx=0.0, vy=0.0, vz=0.0, id=-1):
        super().__init__(x=x, y=y, z=z, mass=mass, id=id)
        self.vx = vx
        self.vy = vy
        self.vz = vz


# ═══════════════════════════════════════════════════════════════════════════
# Тесты производительности и точности
# ═══════════════════════════════════════════════════════════════════════════
def benchmark(n_bodies: int = 500, seed: int = 42, theta: float = 0.7) -> dict:
    """Сравнить Barnes-Hut с direct: время и относительная ошибка."""
    import random

    rng = random.Random(seed)
    bodies = []
    for i in range(n_bodies):
        bodies.append(
            BodyLite(
                x=rng.uniform(-1, 1) * 1e9,
                y=rng.uniform(-1, 1) * 1e9,
                z=rng.uniform(-1, 1) * 1e9,
                mass=rng.uniform(1e18, 1e22),
                id=i,
            )
        )
    # direct
    t0 = time.perf_counter()
    acc_direct = direct_accelerations(bodies)
    t_direct = time.perf_counter() - t0
    # tree
    tree = BarnesHutTree(theta=theta)
    tree.build(bodies)
    t0 = time.perf_counter()
    acc_tree = [tree.acceleration(b) for b in bodies]
    t_tree = time.perf_counter() - t0
    # относительная ошибка
    err_max = 0.0
    err_rms = 0.0
    for ad, at in zip(acc_direct, acc_tree):
        norm_d = math.sqrt(sum(c * c for c in ad)) + 1e-30
        diff = math.sqrt(sum((a - b) ** 2 for a, b in zip(ad, at)))
        err_max = max(err_max, diff / norm_d)
        err_rms += (diff / norm_d) ** 2
    err_rms = math.sqrt(err_rms / len(acc_direct))
    return dict(
        n=n_bodies,
        theta_opening=theta,
        t_direct=t_direct,
        t_tree=t_tree,
        speedup=t_direct / max(t_tree, 1e-12),
        err_max=err_max,
        err_rms=err_rms,
        **tree.stats(),
    )


def self_check() -> dict:
    """Плаккеровский кластер: сохранение энергии leapfrog на дереве."""
    import random

    rng = random.Random(7)
    n = 120
    bodies = []
    for i in range(n):
        bodies.append(
            SimBody(
                x=rng.uniform(-1, 1),
                y=rng.uniform(-1, 1),
                z=rng.uniform(-0.1, 0.1),
                mass=1.0 / n,
                vx=rng.uniform(-0.2, 0.2),
                vy=rng.uniform(-0.2, 0.2),
                vz=0.0,
                id=i,
            )
        )
    # G=1, безразмерные единицы
    eng = BarnesHutEngineMixin(theta=0.6, softening=0.02)

    def energy(bs):
        ke = sum(0.5 * b.mass * (b.vx**2 + b.vy**2) for b in bs)
        pe = 0.0
        for i in range(len(bs)):
            for j in range(i + 1, len(bs)):
                d = math.sqrt((bs[i].x - bs[j].x) ** 2 + (bs[i].y - bs[j].y) ** 2 + 0.02**2)
                pe -= bs[i].mass * bs[j].mass / d
        return ke + pe

    e0 = energy(bodies)
    dt = 0.01
    for _ in range(50):
        eng.step_all(bodies, dt, G=1.0)  # type: ignore[arg-type]
    e1 = energy(bodies)
    drift = abs(e1 - e0) / max(abs(e0), 1e-12)
    bench = benchmark(n_bodies=300)
    return dict(
        energy_drift=drift,
        leapfrog_ok=drift < 0.05,
        speedup=bench["speedup"],
        err_rms=bench["err_rms"],
        accuracy_ok=bench["err_rms"] < 0.05,
        all_ok=(drift < 0.05 and bench["err_rms"] < 0.05),
    )
