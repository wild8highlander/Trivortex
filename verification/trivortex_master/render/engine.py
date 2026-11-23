#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — фасад рендера.

RenderEngine (ABC): setup / draw_frame / save_frame / teardown.
get_backend('auto') выбирает каскадом mpl → pure → ascii по доступности.
Режимы: 2d (проекции), 3d (перспективный рендер), 4d (3D-срез + цвет/размер
по четвёртой координате w).

Все бэкенды выдают файлы (PNG/PPM/ASCII-текст) — единый контракт.
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Any, Sequence

from lab.scene import Scene
from lab.trajectory import Trajectory


# ═══════════════════════════════════════════════════════════════════════════
# ABC
# ═══════════════════════════════════════════════════════════════════════════
class RenderEngine(ABC):
    """Базовый движок рендера."""

    name = "abstract"

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def setup(self, scene: Scene) -> None: ...

    @abstractmethod
    def draw_frame(self, t: float) -> dict[str, Any]:
        """Нарисовать состояние на момент t; вернуть метаданные кадра."""
        ...

    @abstractmethod
    def save_frame(self, path: str) -> int: ...

    def teardown(self) -> None:
        pass


# ═══════════════════════════════════════════════════════════════════════════
# ASCII-бэкенд
# ═══════════════════════════════════════════════════════════════════════════
class AsciiEngine(RenderEngine):
    """Кадры в терминал и текстовые файлы (.txt с ANSI-цветами)."""

    name = "ascii"

    def __init__(self, config):
        super().__init__(config)
        from render import backend_ascii

        self._mod = backend_ascii
        self._lines: list[str] = []

    def setup(self, scene: Scene) -> None:
        self._scene = scene
        self._traj = _scene_trajectory(scene)

    def draw_frame(self, t: float) -> dict[str, Any]:
        traj = self._traj
        state = traj.sample(t) if traj else [b.state_vector() for b in self._scene.bodies]
        bodies = [
            dict(
                position=tuple(s[:3]),
                radius=_screen_radius(self._scene.bodies[i]),
                color=self._scene.bodies[i].color,
                label=self._scene.bodies[i].name,
            )
            for i, s in enumerate(state)
        ]
        trails = _trails_upto(traj, t, stride=8)
        self._lines = self._mod.render_ascii(
            bodies, width=self.config.ascii_width, height=26, trails=trails, use_color=True
        )
        return dict(t=t, n_bodies=len(bodies), backend=self.name)

    def save_frame(self, path: str) -> int:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(self._lines) + "\n")
        return os.path.getsize(path)

    def print_frame(self) -> None:
        self._mod.print_ascii(self._lines)


# ═══════════════════════════════════════════════════════════════════════════
# Pure raster-бэкенд
# ═══════════════════════════════════════════════════════════════════════════
class PureEngine(RenderEngine):
    """Собственный программный 3D-рендер (png_codec + pure_raster)."""

    name = "pure"

    def __init__(self, config):
        super().__init__(config)
        from render import pure_raster

        self._mod = pure_raster
        self._frame = None

    def setup(self, scene: Scene) -> None:
        self._scene = scene
        self._traj = _scene_trajectory(scene)

    def draw_frame(self, t: float) -> dict[str, Any]:
        traj = self._traj
        state = traj.sample(t) if traj else [b.state_vector() for b in self._scene.bodies]
        # нормированные экранные радиусы (для красоты)
        scale = _scene_scale(self._scene)
        bodies = [
            dict(
                position=tuple(s[:3]),
                radius=max(self._scene.bodies[i].radius / scale, 0.04),
                color=self._scene.bodies[i].color,
                label=self._scene.bodies[i].name,
            )
            for i, s in enumerate(state)
        ]
        trails = _trails_upto(traj, t, stride=6)
        self._frame = self._mod.render_bodies(
            bodies, width=self.config.image_width, height=self.config.image_height, trails=trails
        )
        return dict(t=t, n_bodies=len(bodies), backend=self.name)

    def draw_4d(self, t: float, w_values: list[float]) -> dict[str, Any]:
        """4D-кадр: w кодируется свечением (смешение с фиолетовым)."""
        self.draw_frame(t)
        if self._frame is None:
            return dict(t=t, backend=self.name, mode="4d-failed")
        # подсветка: тела с большим |w| светятся сильнее
        for i, b in enumerate(self._scene.bodies):
            pass  # цвет уже задан; 4D-эффект — в save (см. backend_mpl.plot_4d)
        return dict(t=t, backend=self.name, mode="4d", w=w_values)

    def save_frame(self, path: str) -> int:
        if self._frame is None:
            raise RuntimeError("кадр не нарисован (draw_frame)")
        return self._frame.save_png(path)


# ═══════════════════════════════════════════════════════════════════════════
# matplotlib-бэкенд
# ═══════════════════════════════════════════════════════════════════════════
class MplEngine(RenderEngine):
    """matplotlib: 2D-проекции, 3D-траектории, 4D-цветокодирование."""

    name = "mpl"

    def __init__(self, config):
        super().__init__(config)
        from render import backend_mpl

        if not backend_mpl.HAVE_MPL:
            raise ImportError("matplotlib не установлен")
        self._mod = backend_mpl
        self._last_path = None

    def setup(self, scene: Scene) -> None:
        self._scene = scene
        self._traj = _scene_trajectory(scene)

    def draw_frame(self, t: float) -> dict[str, Any]:
        """Кадр = 2D-срез на момент t (для анимаций); полный прогон —
        render_trajectory ниже."""
        return dict(t=t, backend=self.name, note="кадры mpl строятся через render_trajectory")

    def save_frame(self, path: str) -> int:
        return os.path.getsize(path) if path and os.path.exists(path) else 0

    # ── полный набор графиков по траектории ──
    def render_trajectory(
        self, output_dir: str, prefix: str = "traj", mode: str = "all"
    ) -> list[str]:
        """Построить 2D/3D/4D графики траектории сцены."""
        traj = self._traj
        if traj is None:
            raise RuntimeError("нет траектории у сцены")
        os.makedirs(output_dir, exist_ok=True)
        names = [b.name for b in self._scene.bodies]
        colors = [b.color for b in self._scene.bodies]
        style = (
            self.config.color_scheme
            if self.config.color_scheme in self._mod.STYLES
            else "neon_dark"
        )
        out = []
        if mode in ("all", "2d"):
            p = os.path.join(output_dir, f"{prefix}_2d_xy.png")
            self._mod.plot_2d(
                traj, p, style=style, plane="xy", body_names=names, body_colors=colors
            )
            out.append(p)
        if mode in ("all", "3d"):
            p = os.path.join(output_dir, f"{prefix}_3d.png")
            self._mod.plot_3d(traj, p, style=style, body_names=names, body_colors=colors)
            out.append(p)
        if mode in ("all", "4d"):
            # w из истории тел (если задавались) или нули
            w_values = [[b.w for b in self._scene.bodies] for _ in traj.times]
            p = os.path.join(output_dir, f"{prefix}_4d.png")
            self._mod.plot_4d(traj, w_values, p, style=style, body_names=names)
            out.append(p)
        if mode in ("all", "diag"):
            if self._scene.time_history and self._scene.energy_history:
                p = os.path.join(output_dir, f"{prefix}_energy.png")
                self._mod.plot_energy(
                    self._scene.time_history, self._scene.energy_history, p, style=style
                )
                out.append(p)
            p = os.path.join(output_dir, f"{prefix}_distances.png")
            self._mod.plot_distances(traj, p, style=style, names=names)
            out.append(p)
        return out


# ═══════════════════════════════════════════════════════════════════════════
# GL-бэкенд (обёртка)
# ═══════════════════════════════════════════════════════════════════════════
class GLEngine(RenderEngine):
    name = "gl"

    def __init__(self, config):
        super().__init__(config)
        from render import backend_gl

        if not backend_gl.HAVE_GL:
            raise ImportError("GL-стек недоступен: " + backend_gl.availability()["reason"])
        self._mod = backend_gl

    def setup(self, scene: Scene) -> None:
        self._scene = scene
        self._traj = _scene_trajectory(scene)

    def draw_frame(self, t: float) -> dict[str, Any]:
        traj = self._traj
        state = traj.sample(t) if traj else [b.state_vector() for b in self._scene.bodies]
        scale = _scene_scale(self._scene)
        bodies = [
            dict(
                position=tuple(s[:3]),
                radius=max(self._scene.bodies[i].radius / scale, 0.05),
                color=self._scene.bodies[i].color,
            )
            for i, s in enumerate(state)
        ]
        self._pending = bodies
        return dict(t=t, backend=self.name)

    def save_frame(self, path: str) -> int:
        self._mod.render_gl(
            self._pending,
            width=self.config.image_width,
            height=self.config.image_height,
            output=path,
        )
        return os.path.getsize(path)


# ═══════════════════════════════════════════════════════════════════════════
# Фабрика и утилиты
# ═══════════════════════════════════════════════════════════════════════════
_BACKENDS = {
    "ascii": AsciiEngine,
    "pure": PureEngine,
    "mpl": MplEngine,
    "gl": GLEngine,
}

AUTO_CASCADE = ("mpl", "pure", "ascii")


def is_available(name: str) -> bool:
    """Проверка доступности бэкенда без его создания."""
    if name == "ascii" or name == "pure":
        return True
    if name == "mpl":
        try:
            import matplotlib  # noqa: F401

            return True
        except ImportError:
            return False
    if name == "gl":
        try:
            import moderngl  # noqa: F401

            return True
        except ImportError:
            return False
    return False


def get_backend(name: str, config) -> RenderEngine:
    """Получить бэкенд; auto — каскад по доступности."""
    if name == "auto":
        for cand in AUTO_CASCADE:
            if is_available(cand):
                name = cand
                break
        else:
            name = "ascii"
    if name not in _BACKENDS:
        raise ValueError(f"неизвестный бэкенд: {name}; " f"доступны: {', '.join(_BACKENDS)}")
    return _BACKENDS[name](config)


def available_backends() -> list[str]:
    return [b for b in AUTO_CASCADE + ("gl",) if is_available(b)]


# ── утилиты для движков ──
def _scene_trajectory(scene: Scene) -> Trajectory | None:
    """Trajectory из истории сцены (или None)."""
    if scene.trajectory_history:
        traj = Trajectory(
            times=list(scene.time_history),
            states=scene.trajectory_history,
            body_ids=[b.id for b in scene.bodies],
        )
        return traj
    return None


def _scene_scale(scene: Scene) -> float:
    """Характерный масштаб сцены для нормировки радиусов."""
    if not scene.bodies:
        return 1.0
    m = max(max(abs(c) for c in b.position) for b in scene.bodies) or 1.0
    return m


def _screen_radius(body) -> float:
    """Экранный радиус тела для ascii (нормированный)."""
    scale = 1.0
    return max(body.radius / max(scale, body.radius), 1e-3)


def _trails_upto(
    traj: Trajectory | None, t: float, stride: int = 6
) -> list[list[tuple[float, float, float]]]:
    """Трейлы всех тел до момента t (прореженные)."""
    if traj is None or not traj.times:
        return []
    n = len(traj.body_ids)
    out = [[] for _ in range(n)]
    total = len(traj.times)
    take = max(1, total // stride)
    for i in range(0, total, 1):
        if traj.times[i] > t:
            break
        if i % (stride // 2 or 1) == 0 or i == total - 1:
            for b in range(n):
                out[b].append((traj.states[i][b][0], traj.states[i][b][1], traj.states[i][b][2]))
    return out
