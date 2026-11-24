#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Скалярные поля лаборатории: потенциал, джинсов радиус, приливные радиусы.

Грид-вычисления на чистом Python: потенциальные ямы (direct summation
O(N·G)), эквипотенциали для рендера, оценка сферизации Роха для спутников.
"""

from __future__ import annotations

import math


def potential_at(point, bodies, G: float = 6.67430e-11, softening: float = 0.0) -> float:
    """Потенциал Σ −Gm/max(r, soft)."""
    phi = 0.0
    for b in bodies:
        d = math.dist(point, b.position)
        if softening > 0:
            d = math.sqrt(d * d + softening * softening)
        if d > 0:
            phi -= G * b.mass / d
    return phi


def potential_grid(bodies, half: float, n: int = 32, G: float = 6.67430e-11):
    """Сетка n×n потенциала в плоскости xy: [(значение, x, y)]."""
    out = []
    for iy in range(n):
        y = -half + 2 * half * iy / (n - 1)
        for ix in range(n):
            x = -half + 2 * half * ix / (n - 1)
            out.append((potential_at((x, y, 0.0), bodies, G), x, y))
    return out


def roche_radius(primary_mass: float, satellite_mass: float, R_primary: float) -> float:
    """Предел Роха (жидкий спутник): d ≈ 2.44·R·(M/m)^{1/3}."""
    return 2.44 * R_primary * (primary_mass / max(satellite_mass, 1e-30)) ** (1.0 / 3.0)


def hill_sphere(m_primary: float, m_perturber: float, a: float) -> float:
    """Сфера Хилла: r ≈ a·(m/(3M))^{1/3}."""
    return a * (m_perturber / (3.0 * m_primary)) ** (1.0 / 3.0)


def jeans_length(
    temperature: float,
    density: float,
    mass_per_particle: float = 1.67e-27,
    G: float = 6.67430e-11,
    k_B: float = 1.381e-23,
) -> float:
    """Длина Джинса: λ_J = c_s·√(π/(Gρ))."""
    c_s = math.sqrt(k_B * temperature / mass_per_particle)
    return c_s * math.sqrt(math.pi / (G * max(density, 1e-30)))


def escape_speed(mass: float, r: float, G: float = 6.67430e-11) -> float:
    """Return the escape speed at the given distance from the mass."""
    return math.sqrt(2 * G * mass / max(r, 1e-12))


def virial_radius(bodies, G: float = 6.67430e-11) -> float:
    """Оценка вириального радиуса: GM²/|E_pot| (однородная система)."""
    pe = 0.0
    m_tot = sum(b.mass for b in bodies)
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            d = math.dist(bodies[i].position, bodies[j].position)
            if d > 0:
                pe -= G * bodies[i].mass * bodies[j].mass / d
    if pe >= 0:
        return float("inf")
    return G * m_tot * m_tot / abs(pe)
