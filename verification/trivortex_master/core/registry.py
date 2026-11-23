#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — реестр режимов.

Меню главного экрана строится динамически из реестра, а не хардкодом:
добавление новой функции — один декоратор @register_mode.

    @register_mode(name="scene_create", category="Лаборатория",
                   description="Создать сцену", requires=("lab",))
    def scene_create(app): ...

check_requirements() возвращает причины недоступности режима; такие пункты
меню выводятся приглушённо с пояснением.
"""
from __future__ import annotations

import dataclasses
from typing import Any, Callable

# ═══════════════════════════════════════════════════════════════════════════
# Структуры
# ═══════════════════════════════════════════════════════════════════════════

@dataclasses.dataclass
class ModeEntry:
    """Один зарегистрированный режим (пункт меню)."""
    name: str                     # короткое имя-ключ
    title: str                    # текст пункта меню
    category: str                 # категория меню
    callable: Callable            # функция(app) -> None
    description: str = ""         # пояснение (в справке)
    requires: tuple[str, ...] = ()  # ("lab", "mpl", "rebound", ...)
    icon: str = "•"               # иконка пункта
    order: int = 50               # порядок внутри категории
    args_schema: dict[str, Any] = dataclasses.field(default_factory=dict)


class Registry:
    """Хранилище режимов по категориям."""

    def __init__(self):
        self._entries: dict[str, ModeEntry] = {}
        self._category_order: list[str] = []
        self._capability_probes: dict[str, Callable[[], tuple[bool, str]]] = {}

    # ── регистрация ──
    def register(self, entry: ModeEntry) -> None:
        if entry.name in self._entries:
            raise ValueError(f"режим уже зарегистрирован: {entry.name}")
        self._entries[entry.name] = entry
        if entry.category not in self._category_order:
            self._category_order.append(entry.category)

    def capability(self, name: str, probe: Callable[[], tuple[bool, str]]) -> None:
        """Регистрация зонда возможности: (доступно ли, почему нет)."""
        self._capability_probes[name] = probe

    # ── запросы ──
    def get(self, name: str) -> ModeEntry | None:
        return self._entries.get(name)

    def categories(self) -> list[str]:
        return list(self._category_order)

    def modes(self, category: str) -> list[ModeEntry]:
        return sorted((e for e in self._entries.values()
                       if e.category == category),
                      key=lambda e: (e.order, e.name))

    def all_modes(self) -> list[ModeEntry]:
        return list(self._entries.values())

    # ── доступность ──
    def check_requirements(self, entry: ModeEntry) -> list[str]:
        """Список причин недоступности (пустой = доступен)."""
        reasons = []
        for req in entry.requires:
            probe = self._capability_probes.get(req)
            if probe is None:
                continue  # неизвестная возможность не блокирует
            ok, why = probe()
            if not ok:
                reasons.append(why)
        return reasons

    def menu_spec(self) -> list[dict[str, Any]]:
        """Спецификация меню для отрисовки: категории → пункты."""
        spec = []
        for cat in self.categories():
            items = []
            for m in self.modes(cat):
                items.append(dict(
                    name=m.name, title=m.title, icon=m.icon,
                    description=m.description,
                    available=not self.check_requirements(m),
                    blocked_reasons=self.check_requirements(m),
                    requires=list(m.requires),
                ))
            if items:
                spec.append(dict(category=cat, items=items))
        return spec


# ═══════════════════════════════════════════════════════════════════════════
# Глобальный реестр и декоратор
# ═══════════════════════════════════════════════════════════════════════════
REGISTRY = Registry()


def register_mode(name: str, title: str, category: str,
                  description: str = "", requires: tuple[str, ...] = (),
                  icon: str = "•", order: int = 50):
    """Декоратор регистрации режима в глобальном реестре."""
    def deco(fn: Callable) -> Callable:
        REGISTRY.register(ModeEntry(
            name=name, title=title, category=category, callable=fn,
            description=description, requires=requires,
            icon=icon, order=order))
        return fn
    return deco


def register_capabilities() -> None:
    """Стандартные зонды возможностей (движки, пакеты, ядро)."""

    def _have(module: str, label: str):
        def probe():
            try:
                __import__(module)
                return True, ""
            except ImportError:
                return False, f"{label} не установлен (пакет {module})"
        return probe

    REGISTRY.capability("mpl", _have("matplotlib", "matplotlib"))
    REGISTRY.capability("numpy", _have("numpy", "numpy"))
    REGISTRY.capability("rebound", _have("rebound", "REBOUND"))
    REGISTRY.capability("dedalus", _have("dedalus", "Dedalus"))
    REGISTRY.capability("imageio", _have("imageio", "imageio"))
    REGISTRY.capability("psutil", _have("psutil", "psutil"))

    def probe_core():
        try:
            from core import bridge
            st = bridge.health_check()
            if st.available:
                return True, ""
            return False, "локальная копия Trivortex не найдена (автономный режим)"
        except Exception as exc:
            return False, f"мост к ядру недоступен: {exc}"
    REGISTRY.capability("core", probe_core)

    def probe_ffmpeg():
        import shutil as _sh
        if _sh.which("ffmpeg"):
            return True, ""
        return False, "ffmpeg не найден в PATH (MP4 недоступен, GIF работает)"
    REGISTRY.capability("ffmpeg", probe_ffmpeg)


# Сводка для HUD/отчётов
def engine_status_lines() -> list[str]:
    """Строки статуса движков для баннера и меню справки."""
    register_capabilities()
    lines = []
    labels = [("numpy", "numpy"), ("mpl", "matplotlib"), ("rebound", "REBOUND"),
              ("dedalus", "Dedalus"), ("imageio", "imageio"), ("ffmpeg", "ffmpeg"),
              ("core", "ядро Trivortex")]
    for key, label in labels:
        probe = REGISTRY._capability_probes.get(key)
        if probe is None:
            continue
        ok, why = probe()
        mark = "✓" if ok else "✗"
        lines.append((mark, label, why))
    return lines
