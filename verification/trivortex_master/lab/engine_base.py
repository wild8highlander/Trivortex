#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — базовые интерфейсы физических движков.

Выделены из lab/physics.py, чтобы разорвать петлю lab ↔ realism:
адаптеры (realism/adapters/*) наследуют EngineUnavailable/BodyState/
PhysicsEngine отсюда и НЕ импортируют lab.physics.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

Vector3 = tuple[float, float, float]


class EngineUnavailable(Exception):
    """Движок недоступен — диспетчер переключается на fallback."""

    def __init__(self, name: str, fallback: str, reason: str = ""):
        super().__init__(f"движок {name} недоступен: {reason}")
        self.name = name
        self.fallback = fallback
        self.reason = reason


class BodyState:
    """Снимок состояния одного тела после шага движка."""

    __slots__ = ("id", "position", "velocity", "extra")

    def __init__(self, id: str, position: Vector3, velocity: Vector3, extra: dict | None = None):
        self.id = id
        self.position = position
        self.velocity = velocity
        self.extra = extra or {}


class PhysicsEngine(ABC):
    """Общий интерфейс всех движков (см. lab/physics.py для реализаций)."""

    def __init__(self, scene):
        self.scene = scene
        from core.config import MasterConfig  # лениво, чтобы не тянуть цикл

        self.cfg: MasterConfig = scene.config

    @abstractmethod
    def step(self, dt: float) -> None: ...

    @abstractmethod
    def get_states(self) -> list[BodyState]: ...

    @abstractmethod
    def energy(self) -> float: ...

    @abstractmethod
    def name(self) -> str: ...

    def apply_states(self) -> None:
        """Записать состояния обратно в тела сцены (по умолчанию — никак)."""
