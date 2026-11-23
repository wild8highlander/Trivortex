#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — Scene: сцена лаборатории.

Сцена — набор тел + движок + время + границы. Ключевая механика — лимит тел
(порог Хавелока): add_body() при N=8 требует allow_unphysical, ставит
unphysical_flag и красную плашку в HUD/отчёты.
"""
from __future__ import annotations

import dataclasses
import datetime as _dt
import json
import math
import os
import uuid
from dataclasses import dataclass, field
from typing import Any

from core.config import MasterConfig, UnphysicalConfiguration
from lab.body import Body


@dataclass
class BoundingBox:
    """Границы сцены (м или единицы модели)."""
    half: float = 1e12

    @classmethod
    def from_scene(cls, bodies: list[Body], margin: float = 1.5) -> "BoundingBox":
        if not bodies:
            return cls()
        m = max(max(abs(c) for c in b.position) for b in bodies)
        return cls(half=m * margin)

    def contains(self, p: tuple[float, float, float]) -> bool:
        return all(abs(c) <= self.half for c in p)


@dataclass
class ValidationReport:
    """Отчёт валидации сцены."""
    ok: bool = True
    problems: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    unphysical: bool = False

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


class Scene:
    """Сцена N тел."""

    def __init__(self, config: MasterConfig, name: str = ""):
        self.config = config
        self.id = uuid.uuid4().hex[:10]
        self.name = name or f"scene_{self.id}"
        self.created = _dt.datetime.now().isoformat(timespec="seconds")
        self.bodies: list[Body] = []
        self.engine = None                # PhysicsEngine (лаб/физика)
        self.engine_name: str = ""
        self.t: float = 0.0
        self.dt: float = config.dt
        self.bounds = BoundingBox()
        self.scale_mode: str = config.scale_mode
        self.unphysical_flag: bool = False
        self.events: list[dict[str, Any]] = []   # столкновения, вылеты, потери энергии
        self.trajectory_history: list[list[list[float]]] = []
        self.time_history: list[float] = []
        self.energy_history: list[float] = []

    # ══════════════════ управление телами ══════════════════
    def add_body(self, body: Body) -> Body:
        """Добавить тело; здесь живёт механика порога Хавелока."""
        n = len(self.bodies)
        cfg = self.config
        if n + 1 > cfg.hard_max_bodies:
            raise UnphysicalConfiguration(
                f"N={n + 1} > hard_max_bodies={cfg.hard_max_bodies}: "
                "конфигурация не поддерживается ни в каком режиме "
                "(жёсткий лимит 8)", n_bodies=n + 1)
        if n + 1 > cfg.max_bodies:
            if not cfg.allow_unphysical:
                raise UnphysicalConfiguration(
                    f"N={n + 1} вне физической вселенной модели: порог Хавелока "
                    "(POLYVORTEX W4) — кольцо устойчиво при N≤7, при N=8 "
                    "max Re λ = +0.4502 (резкий скачок неустойчивости). "
                    "Включите allow_unphysical=True, чтобы продолжить с пометкой.",
                    n_bodies=n + 1)
            self.unphysical_flag = True
            self.events.append(dict(
                kind="unphysical",
                detail=(f"N={n + 1}: конфигурация вне физической вселенной модели "
                        f"(порог Хавелока, max Re λ = +0.4502)"),
                t=self.t))
        # дубликат id
        if any(b.id == body.id for b in self.bodies):
            body.id = f"{body.id}_{n + 1}"
        self.bodies.append(body)
        return body

    def remove_body(self, body_id: str) -> bool:
        before = len(self.bodies)
        self.bodies = [b for b in self.bodies if b.id != body_id]
        return len(self.bodies) < before

    def body(self, body_id: str) -> Body | None:
        for b in self.bodies:
            if b.id == body_id:
                return b
        return None

    @property
    def n(self) -> int:
        return len(self.bodies)

    # ══════════════════ валидация ══════════════════
    def validate(self) -> ValidationReport:
        rep = ValidationReport()
        if self.n < self.config.min_bodies:
            rep.ok = False
            rep.problems.append(
                f"тел в сцене {self.n} < минимально допустимых "
                f"{self.config.min_bodies}")
        ids = [b.id for b in self.bodies]
        if len(ids) != len(set(ids)):
            rep.ok = False
            rep.problems.append("дубликаты id тел")
        for b in self.bodies:
            for p in b.validate():
                (rep.problems if "должна" in p or "NaN" in p else rep.warnings).append(p)
        # мгновенные столкновения
        for i in range(self.n):
            for j in range(i + 1, self.n):
                d = self.bodies[i].distance_to(self.bodies[j])
                rsum = self.bodies[i].radius + self.bodies[j].radius
                if d < rsum * 0.5:
                    rep.warnings.append(
                        f"тела {self.bodies[i].id} и {self.bodies[j].id} "
                        f"перекрываются: d={d:.3g} < Σr/2={rsum * 0.5:.3g}")
        if self.n > self.config.max_bodies:
            rep.unphysical = True
            rep.warnings.append(
                f"N={self.n} > {self.config.max_bodies}: вне физической "
                "вселенной модели (порог Хавелока)")
        return rep

    # ══════════════════ физика сцены ══════════════════
    def total_mass(self) -> float:
        return sum(b.mass for b in self.bodies)

    def total_energy(self, G: float | None = None) -> float:
        G = G if G is not None else self.config.G
        ke = sum(b.kinetic_energy() for b in self.bodies)
        pe = 0.0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                pe += self.bodies[i].potential_energy(
                    self.bodies[j], G=G, softening=self.config.softening)
        return ke + pe

    def total_momentum(self) -> tuple[float, float, float]:
        px = sum(b.momentum()[0] for b in self.bodies)
        py = sum(b.momentum()[1] for b in self.bodies)
        pz = sum(b.momentum()[2] for b in self.bodies)
        return (px, py, pz)

    def total_angular_momentum(self) -> tuple[float, float, float]:
        lx = sum(b.angular_momentum_origin()[0] for b in self.bodies)
        ly = sum(b.angular_momentum_origin()[1] for b in self.bodies)
        lz = sum(b.angular_momentum_origin()[2] for b in self.bodies)
        return (lx, ly, lz)

    def center_of_mass(self) -> tuple[float, float, float]:
        m = self.total_mass()
        if m <= 0:
            return (0.0, 0.0, 0.0)
        x = sum(b.mass * b.position[0] for b in self.bodies) / m
        y = sum(b.mass * b.position[1] for b in self.bodies) / m
        z = sum(b.mass * b.position[2] for b in self.bodies) / m
        return (x, y, z)

    def apply_engine(self, name: str):
        """Выбор и инициализация физического движка (лениво, чтобы не тянуть
        адаптеры при импорте)."""
        from lab.physics import get_engine
        self.engine = get_engine(name, self)
        self.engine_name = self.engine.name()

    # ══════════════════ служебное ══════════════════
    def clone(self) -> "Scene":
        sc = Scene(self.config, name=self.name + "_copy")
        for b in self.bodies:
            sc.bodies.append(Body.from_dict(b.to_dict()))
        sc.t = self.t
        sc.dt = self.dt
        sc.unphysical_flag = self.unphysical_flag
        sc.scale_mode = self.scale_mode
        sc.bounds = dataclasses.replace(self.bounds)
        return sc

    def summary(self) -> dict[str, Any]:
        return dict(
            id=self.id, name=self.name, n=self.n,
            bodies=[dict(id=b.id, name=b.name, mass=b.mass, radius=b.radius,
                         type=b.type, source=b.source, speed=b.speed())
                    for b in self.bodies],
            t=self.t, dt=self.dt, scale_mode=self.scale_mode,
            engine=self.engine_name,
            unphysical=self.unphysical_flag,
            total_mass=self.total_mass(),
            total_energy=self.total_energy(),
            momentum=list(self.total_momentum()),
            center_of_mass=list(self.center_of_mass()),
            events=len(self.events),
        )

    def record_frame(self) -> None:
        self.trajectory_history.append([b.state_vector() for b in self.bodies])
        self.time_history.append(self.t)
        self.energy_history.append(self.total_energy())

    # ══════════════════ сериализация ══════════════════
    def to_dict(self, include_history: bool = False) -> dict[str, Any]:
        d = dict(
            id=self.id, name=self.name, created=self.created,
            t=self.t, dt=self.dt, scale_mode=self.scale_mode,
            unphysical_flag=self.unphysical_flag,
            engine=self.engine_name,
            config=self.config.to_dict(),
            bounds=self.bounds.half,
            bodies=[b.to_dict() for b in self.bodies],
            events=self.events[-50:],
        )
        if include_history:
            d["trajectory"] = self.trajectory_history
            d["times"] = self.time_history
            d["energy"] = self.energy_history
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Scene":
        cfg = MasterConfig.from_dict(d["config"])
        sc = cls(cfg, name=d.get("name", ""))
        sc.id = d.get("id", sc.id)
        sc.created = d.get("created", sc.created)
        sc.t = float(d.get("t", 0.0))
        sc.dt = float(d.get("dt", cfg.dt))
        sc.scale_mode = d.get("scale_mode", cfg.scale_mode)
        sc.unphysical_flag = bool(d.get("unphysical_flag", False))
        sc.engine_name = d.get("engine", "")
        sc.bounds = BoundingBox(half=float(d.get("bounds", 1e12)))
        sc.bodies = [Body.from_dict(bd) for bd in d.get("bodies", [])]
        sc.events = list(d.get("events", []))
        hist = d.get("trajectory")
        if hist:
            sc.trajectory_history = hist
            sc.time_history = list(d.get("times", []))
            sc.energy_history = list(d.get("energy", []))
        return sc

    def save(self, path: str) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.to_dict(include_history=True), fh,
                      ensure_ascii=False, indent=1)

    @classmethod
    def load(cls, path: str) -> "Scene":
        with open(path, "r", encoding="utf-8") as fh:
            return cls.from_dict(json.load(fh))
