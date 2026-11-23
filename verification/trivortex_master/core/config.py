#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — конфигурация: MasterConfig, профили, валидация.

Механика лимита тел (порог Хавелока, POLYVORTEX W4):
  * N < 3            — отказ (нет задачи трёх тел);
  * 3 <= N <= 7      — полный режим (устойчиво по Хавелоку);
  * N = 8            — исключение UnphysicalConfiguration без флага
                       allow_unphysical; с флагом — принудительный режим
                       с пометкой unphysical_flag=True во всех отчётах;
  * N > 8            — жёсткий отказ (hard_max_bodies = 8).
"""

from __future__ import annotations

import copy
import dataclasses
import json
import os
from typing import Any

# Гравитационная постоянная CODATA 2018
G_SI = 6.67430e-11  # м^3 кг^-1 с^-2

# Порог Хавелока: max Re λ = +0.4502 при N=8 (POLYVORTEX, стадия W4)
HAVelock_THRESHOLD_NOTE = (
    "Порог Хавелока (POLYVORTEX W4): вихревое кольцо устойчиво при N<=7, "
    "неустойчиво при N>=8 (max Re λ = +0.4502). Конфигурация N=8 помечена "
    "как нефизическая для модели."
)


class UnphysicalConfiguration(Exception):
    """Попытка создать конфигурацию вне физической вселенной модели."""

    def __init__(self, message: str, n_bodies: int = 0):
        super().__init__(message)
        self.n_bodies = n_bodies


# ═══════════════════════════════════════════════════════════════════════════
# MasterConfig
# ═══════════════════════════════════════════════════════════════════════════


@dataclasses.dataclass
class MasterConfig:
    """Все настраиваемые параметры комплекса."""

    # ── общий профиль ──
    profile: str = "standard"  # quick|standard|realistic|research|cinematic|pure_stdlib

    # ── рендер ──
    render_backend: str = "auto"  # auto|ascii|pure|mpl|gl
    color_scheme: str = "neon_dark"  # neon_dark|scientific|minimal
    image_width: int = 1280  # ширина кадра чистых растровых движков
    image_height: int = 720
    ascii_width: int = 78  # ширина ascii-рендера

    # ── физика ──
    physics_engine: str = "auto"  # auto|native_newton|native_vortex|rebound|dedalus|custom
    G: float = G_SI
    time_scale: float = 1.0  # множитель модельного времени
    enable_relativity: bool = False  # 1PN-поправка
    enable_dissipation: bool = False  # диссипативный член
    softening: float = 0.0  # сглаживание потенциала (м)

    # ── лимиты тел (порог Хавелока) ──
    min_bodies: int = 3
    max_bodies: int = 7
    hard_max_bodies: int = 8
    allow_unphysical: bool = False

    # ── масштаб ──
    scale_mode: str = "macro"  # macro|micro

    # ── интегрирование ──
    dt: float = 1e-3  # шаг (в единицах модели)
    n_steps: int = 2000  # число шагов по умолчанию
    max_wall_seconds: float = 600.0  # предохранитель по времени

    # ── данные и вывод ──
    data_dir: str = "data"
    cache_ttl_seconds: int = 86400  # TTL TAP-кэша: сутки
    output_dir: str = "runs"
    report_formats: list[str] = dataclasses.field(default_factory=lambda: ["md", "html", "json"])
    report_theme: str = "aurora"  # aurora|ice|minimal
    log_level: str = "INFO"
    seed: int = 42

    # ── язык интерфейса ──
    lang: str = "ru"

    # ── мониторы и бары ──
    progress: bool = True
    monitor_inline: bool = True

    # ══════════════════ методы ══════════════════
    def validate(self) -> list[str]:
        """Возвращает список проблем конфигурации (пустой = всё хорошо)."""
        problems = []
        if self.min_bodies < 3:
            problems.append("min_bodies < 3: меньше трёх тел задача не определена")
        if self.max_bodies < self.min_bodies:
            problems.append("max_bodies < min_bodies")
        if self.hard_max_bodies < self.max_bodies:
            problems.append("hard_max_bodies < max_bodies")
        if self.physics_engine not in (
            "auto",
            "native_newton",
            "native_vortex",
            "rebound",
            "dedalus",
            "custom",
        ):
            problems.append(f"неизвестный движок: {self.physics_engine}")
        if self.render_backend not in ("auto", "ascii", "pure", "mpl", "gl"):
            problems.append(f"неизвестный бэкенд рендера: {self.render_backend}")
        if self.profile not in PROFILES:
            problems.append(f"неизвестный профиль: {self.profile}")
        if self.dt <= 0:
            problems.append("dt <= 0")
        if self.n_steps < 1:
            problems.append("n_steps < 1")
        if self.G <= 0:
            problems.append("G <= 0")
        return problems

    def check_bodies(self, n: int) -> None:
        """Лимит тел; кидает UnphysicalConfiguration."""
        if n < self.min_bodies:
            raise UnphysicalConfiguration(
                f"N={n} < min_bodies={self.min_bodies}: меньше трёх тел — "
                "нет ни задачи трёх тел, ни вихревого треугольника Теоремы 3.1",
                n_bodies=n,
            )
        if n > self.hard_max_bodies:
            raise UnphysicalConfiguration(
                f"N={n} > hard_max_bodies={self.hard_max_bodies}: "
                "конфигурация не поддерживается ни в каком режиме",
                n_bodies=n,
            )
        if n > self.max_bodies:
            if not self.allow_unphysical:
                raise UnphysicalConfiguration(
                    f"N={n} вне физической вселенной модели: порог Хавелока "
                    f"(POLYVORTEX W4) — кольцо устойчиво при N<=7, при N=8 "
                    "max Re λ = +0.4502. Включите allow_unphysical=True, "
                    "чтобы принудительно продолжить.",
                    n_bodies=n,
                )
        if n > self.max_bodies and self.allow_unphysical:
            # допустимо, но помечается при сборке сцены
            pass

    def unphysical_note(self) -> str | None:
        """Пометка о нефизичности для шапок отчётов (None если режим обычный)."""
        return HAVelock_THRESHOLD_NOTE

    # ── сериализация ──
    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> MasterConfig:
        valid = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in d.items() if k in valid})

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.to_dict(), fh, ensure_ascii=False, indent=1)

    @classmethod
    def load(cls, path: str) -> MasterConfig:
        with open(path, encoding="utf-8") as fh:
            return cls.from_dict(json.load(fh))

    def diff(self, other: MasterConfig) -> dict[str, tuple[Any, Any]]:
        """Различия между двумя конфигурациями (для отчётов об изменениях)."""
        out = {}
        for f in dataclasses.fields(self.__class__):
            a, b = getattr(self, f.name), getattr(other, f.name)
            if a != b:
                out[f.name] = (a, b)
        return out


# ═══════════════════════════════════════════════════════════════════════════
# Профили
# ═══════════════════════════════════════════════════════════════════════════
PROFILES: dict[str, dict[str, Any]] = {
    "quick": dict(
        render_backend="ascii",
        physics_engine="native_newton",
        n_steps=400,
        progress=True,
        report_formats=["md", "json"],
    ),
    "standard": dict(
        render_backend="auto",
        physics_engine="auto",
        n_steps=2000,
        report_formats=["md", "html", "json"],
    ),
    "realistic": dict(
        render_backend="auto",
        physics_engine="auto",
        G=G_SI,
        enable_relativity=True,
        scale_mode="macro",
        report_formats=["md", "html", "json", "csv"],
    ),
    "research": dict(
        render_backend="mpl",
        physics_engine="auto",
        n_steps=6000,
        report_formats=["txt", "md", "html", "csv", "json", "docx", "pdf"],
        report_theme="aurora",
    ),
    "cinematic": dict(
        render_backend="mpl",
        physics_engine="native_newton",
        time_scale=1e5,
        n_steps=3000,
        image_width=1920,
        image_height=1080,
        report_formats=["html", "pdf"],
    ),
    "pure_stdlib": dict(
        render_backend="pure",
        physics_engine="native_newton",
        n_steps=1500,
        report_formats=["txt", "md", "json"],
    ),
}


def from_profile(name: str, **overrides: Any) -> MasterConfig:
    """Собрать конфигурацию из профиля с переопределениями."""
    if name not in PROFILES:
        raise ValueError(f"неизвестный профиль: {name} " f"(доступны: {', '.join(PROFILES)})")
    cfg = MasterConfig(profile=name)
    for key, val in PROFILES[name].items():
        setattr(cfg, key, val)
    for key, val in overrides.items():
        if not hasattr(cfg, key):
            raise ValueError(f"нет параметра {key} в MasterConfig")
        setattr(cfg, key, val)
    problems = cfg.validate()
    if problems:
        raise ValueError("конфигурация невалидна: " + "; ".join(problems))
    return cfg


def resolve_paths(config: MasterConfig, root: str | None = None) -> MasterConfig:
    """Превращает относительные пути data/output в абсолютные от корня пакета."""
    cfg = copy.deepcopy(config)
    root = root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for attr in ("data_dir", "output_dir"):
        p = getattr(cfg, attr)
        if not os.path.isabs(p):
            setattr(cfg, attr, os.path.join(root, p))
    return cfg
