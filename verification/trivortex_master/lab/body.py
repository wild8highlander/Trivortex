#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — Body: тело лаборатории.

Помимо стандартных 3D-поля (масса, радиус, позиция, скорость) несёт:
  * четвёртую координату w для гиперсцен (4D-рендер кодирует её цветом/размером);
  * заряд и циркуляцию Γ (для вихревого режима Кирхгофа);
  * источник (URL или DOI) — дисциплина «каждое число привязано к источнику»;
  * полную сериализацию to_dict/from_dict/from_catalog.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Body:
    """Одно тело сцены."""
    id: str
    name: str
    mass: float                     # кг
    radius: float                   # км
    position: tuple[float, float, float] = (0.0, 0.0, 0.0)   # м (или единицы модели)
    velocity: tuple[float, float, float] = (0.0, 0.0, 0.0)   # м/с
    w: float = 0.0                  # 4-я координата гиперсцен
    charge: float = 0.0             # электрический заряд (Кл), для custom-сил
    circulation: float = 0.0        # Γ для вихревого режима Кирхгофа
    color: str = "#4fd1c5"
    type: str = "generic"           # planet|moon|star|asteroid|comet|exoplanet|synthetic|generic
    source: str = "synthetic"       # URL или DOI источника параметров
    metadata: dict[str, Any] = field(default_factory=dict)

    # ══════════════════ валидация ══════════════════
    def validate(self) -> list[str]:
        problems = []
        if not self.id:
            problems.append("пустой id")
        if not self.name:
            problems.append(f"[{self.id}] пустое имя")
        if not (self.mass > 0):
            problems.append(f"[{self.id}] масса должна быть > 0")
        if not (self.radius > 0):
            problems.append(f"[{self.id}] радиус должен быть > 0")
        for label, vec in (("позиция", self.position), ("скорость", self.velocity)):
            if len(vec) != 3:
                problems.append(f"[{self.id}] {label}: нужна 3-компонентная")
            elif any(v != v or v in (float("inf"), float("-inf")) for v in vec):
                problems.append(f"[{self.id}] {label}: NaN/Inf")
        return problems

    # ══════════════════ физика ══════════════════
    def speed(self) -> float:
        return math.sqrt(sum(v * v for v in self.velocity))

    def kinetic_energy(self) -> float:
        return 0.5 * self.mass * self.speed() ** 2

    def potential_energy(self, other: "Body", G: float = 6.67430e-11,
                         softening: float = 0.0) -> float:
        """Ньютоновская взаимная потенциальная энергия (отрицательная)."""
        d = self.distance_to(other)
        denom = math.sqrt(d * d + softening * softening)
        if denom <= 0:
            return float("-inf")
        return -G * self.mass * other.mass / denom

    def distance_to(self, other: "Body") -> float:
        return math.sqrt(sum((a - b) ** 2
                             for a, b in zip(self.position, other.position)))

    def momentum(self) -> tuple[float, float, float]:
        return tuple(m * v for m, v in zip((self.mass,) * 3, self.velocity))

    def angular_momentum_origin(self) -> tuple[float, float, float]:
        rx, ry, rz = self.position
        px, py, pz = self.momentum()
        return (ry * pz - rz * py, rz * px - rx * pz, rx * py - ry * px)

    # ══════════════════ геометрия/проекции ══════════════════
    def project_2d(self, plane: str = "xy") -> tuple[float, float]:
        idx = {"xy": (0, 1), "xz": (0, 2), "yz": (1, 2)}[plane]
        return (self.position[idx[0]], self.position[idx[1]])

    def to_4d(self) -> tuple[float, float, float, float]:
        return (self.position[0], self.position[1], self.position[2], self.w)

    def state_vector(self) -> list[float]:
        """[x, y, z, vx, vy, vz] — для интеграторов."""
        return [*self.position, *self.velocity]

    # ══════════════════ сериализация ══════════════════
    def to_dict(self) -> dict[str, Any]:
        return dict(
            id=self.id, name=self.name, mass=self.mass, radius=self.radius,
            position=list(self.position), velocity=list(self.velocity),
            w=self.w, charge=self.charge, circulation=self.circulation,
            color=self.color, type=self.type, source=self.source,
            metadata=self.metadata,
        )

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Body":
        return cls(
            id=d["id"], name=d.get("name", d["id"]),
            mass=float(d["mass"]), radius=float(d["radius"]),
            position=tuple(float(x) for x in d.get("position", (0, 0, 0))),
            velocity=tuple(float(x) for x in d.get("velocity", (0, 0, 0))),
            w=float(d.get("w", 0.0)),
            charge=float(d.get("charge", 0.0)),
            circulation=float(d.get("circulation", 0.0)),
            color=d.get("color", "#4fd1c5"),
            type=d.get("type", "generic"),
            source=d.get("source", "synthetic"),
            metadata=dict(d.get("metadata", {})),
        )

    @classmethod
    def from_catalog(cls, obj_id: str, catalog: dict[str, Any]) -> "Body":
        """Создать тело из записи data/catalog.json."""
        objects = catalog.get("objects", catalog if isinstance(catalog, list) else [])
        rec = None
        for r in objects:
            if r.get("id") == obj_id:
                rec = r
                break
        if rec is None:
            raise KeyError(f"объект {obj_id} не найден в каталоге")
        meta = dict(rec.get("metadata", {}))
        body = cls(
            id=rec["id"], name=rec.get("name", rec["id"]),
            mass=float(rec["mass_kg"]), radius=float(rec["radius_km"]) * 1000.0,
            color=rec.get("color", "#4fd1c5"),
            type=rec.get("type", "generic"),
            source=rec.get("source", "synthetic"),
            metadata=meta,
        )
        if "circulation" in rec:
            body.circulation = float(rec["circulation"])
        if rec.get("parent"):
            body.metadata["parent"] = rec["parent"]
            body.metadata["orbit_km"] = rec.get("orbit_km")
        elif rec.get("orbit_au") is not None:
            body.metadata["orbit_au"] = float(rec["orbit_au"])
        return body

    def __repr__(self) -> str:  # pragma: no cover
        return (f"Body({self.id!r}, m={self.mass:.3g}, "
                f"r={self.position}, v={self.velocity})")


# ═══════════════════════════════════════════════════════════════════════════
# Вспомогательные конструкторы сцен
# ═══════════════════════════════════════════════════════════════════════════
AU_M = 1.495978707e11


def circular_orbit_velocity(central_mass: float, r: float,
                            G: float = 6.67430e-11) -> float:
    """Скорость круговой орбиты v = √(GM/r)."""
    return math.sqrt(G * central_mass / max(r, 1e-12))


def place_on_orbit(central: Body, satellite: Body, orbit_radius: float,
                   phase_deg: float = 0.0, inclination_deg: float = 0.0,
                   G: float = 6.67430e-11, retrograde: bool = False) -> Body:
    """Поставить satellite на круговую орбиту вокруг central (в плоскости xy,
    с опциональным наклонением), задав ему кеплерову скорость."""
    phase = math.radians(phase_deg)
    incl = math.radians(inclination_deg)
    x = orbit_radius * math.cos(phase)
    y = orbit_radius * math.sin(phase) * math.cos(incl)
    z = orbit_radius * math.sin(phase) * math.sin(incl)
    v = circular_orbit_velocity(central.mass, orbit_radius, G)
    sign = -1.0 if retrograde else 1.0
    # скорость перпендикулярна радиус-вектору, в плоскости орбиты
    vx = -sign * v * math.sin(phase)
    vy = sign * v * math.cos(phase) * math.cos(incl)
    vz = sign * v * math.cos(phase) * math.sin(incl)
    satellite.position = (central.position[0] + x,
                          central.position[1] + y,
                          central.position[2] + z)
    satellite.velocity = (central.velocity[0] + vx,
                          central.velocity[1] + vy,
                          central.velocity[2] + vz)
    return satellite
