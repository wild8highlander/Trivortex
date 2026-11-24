#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — терминальный ASCII-рендер.

Программный 3D-рендер прямо в терминал: перспективная проекция, z-буфер
на символах плотности « .:-=+*#%@», truecolor ANSI (при поддержке).
Работает без numpy; ширина адаптируется под терминал.
"""

from __future__ import annotations

import math
from typing import Sequence

from render.pure_raster import (
    mat_look_at,
    mat_perspective,
    mat_apply,
)

# палитра плотности: от пустоты к яркому
DENSITY = " .:-=+*#%@"


# ANSI truecolor
def _fg(r: int, g: int, b: int) -> str:
    """Do fg for r, g, b and return the result."""
    return f"\x1b[38;2;{r};{g};{b}m"


RESET = "\x1b[0m"


def _hex_to_rgb(color: str) -> tuple[int, int, int]:
    """Do hex to rgb for color and return the result."""
    h = color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


class AsciiCanvas:
    """Символьный кадр с z-буфером и цветом."""

    def __init__(self, width: int, height: int):
        """Do AsciiCanvas.  init for width, height and return the result."""
        self.w = width
        self.h = height
        self.chars = [[" "] * width for _ in range(height)]
        self.colors = [[None] * width for _ in range(height)]
        self.zbuf = [[float("inf")] * width for _ in range(height)]

    def plot(self, x: int, y: int, z: float, ch: str, color: tuple[int, int, int] | None) -> None:
        """Do AsciiCanvas.plot for x, y, z, ch and return the result."""
        if 0 <= x < self.w and 0 <= y < self.h and z < self.zbuf[y][x]:
            self.zbuf[y][x] = z
            self.chars[y][x] = ch
            self.colors[y][x] = color

    def line(self, x0, y0, z0, x1, y1, z1, ch: str, color: tuple[int, int, int] | None) -> None:
        """Линия Брезенхэма с z-интерполяцией."""
        steps = int(max(abs(x1 - x0), abs(y1 - y0), 1))
        for i in range(steps + 1):
            t = i / steps
            self.plot(
                int(round(x0 + (x1 - x0) * t)),
                int(round(y0 + (y1 - y0) * t)),
                z0 + (z1 - z0) * t,
                ch,
                color,
            )

    def to_lines(self, use_color: bool = True) -> list[str]:
        """Do AsciiCanvas.to lines for use_color and return the result."""
        out = []
        for row in range(self.h):
            buf = []
            last_color = None
            for col in range(self.w):
                c = self.colors[row][col]
                if use_color and c is not None and c != last_color:
                    buf.append(_fg(*c))
                    last_color = c
                buf.append(self.chars[row][col])
            if use_color and last_color is not None:
                buf.append(RESET)
            out.append("".join(buf).rstrip())
        return out


def render_ascii(
    bodies: list[dict],
    width: int = 78,
    height: int = 28,
    trails: list[list[tuple[float, float, float]]] | None = None,
    eye: tuple[float, float, float] | None = None,
    target: tuple[float, float, float] = (0.0, 0.0, 0.0),
    fov: float = 50.0,
    use_color: bool = True,
    axes: bool = True,
) -> list[str]:
    """
    bodies: [{position, radius, color, label}]. Возвращает строки кадра.

    Радиус кодируется плотностью символа + размером пятна: r_px < 1 — один
    символ плотности; крупнее — диск из символов.
    """
    canvas = AsciiCanvas(width, height)
    aspect = 0.5  # терминальный символ ~ вдвое выше ширины

    if bodies:
        max_r = max(max(abs(c) for c in b["position"]) for b in bodies) or 1.0
    else:
        max_r = 1.0
    half = math.radians(fov) / 2.0
    d = (max_r / max(math.sin(half), 1e-3)) * 1.35
    if eye is None:
        eye = (d * 0.55, d * 0.4, d * 0.75)
        el = math.sqrt(sum(c * c for c in eye)) or 1.0
        eye = tuple(c * d / el for c in eye)

    view = mat_look_at(eye, target, (0.0, 1.0, 0.0))
    proj = mat_perspective(fov, width * aspect / height, 0.05, 100.0)

    def to_screen(p):
        v = mat_apply(proj, mat_apply(view, (*p, 1.0)))
        if v[3] <= 1e-9:
            return None
        return ((v[0] / v[3] * 0.5 + 0.5) * width, (1.0 - (v[1] / v[3] * 0.5 + 0.5)) * height, v[3])

    # оси
    if axes:
        o = to_screen((0.0, 0.0, 0.0))
        if o:
            for vec, ch, color in (
                ((0.7, 0, 0), "x", (120, 60, 60)),
                ((0, 0.7, 0), "y", (60, 120, 60)),
                ((0, 0, 0.7), "z", (60, 60, 120)),
            ):
                t = to_screen(vec)
                if t:
                    canvas.line(o[0], o[1], -1e9, t[0], t[1], -1e9, ch, color)

    # трейлы
    if trails:
        for trail in trails:
            if len(trail) < 2:
                continue
            prev = to_screen(trail[0])
            for p in trail[1:]:
                cur = to_screen(p)
                if prev and cur:
                    canvas.line(prev[0], prev[1], -1e8, cur[0], cur[1], -1e8, "·", (90, 120, 160))
                prev = cur

    # тела: размер в пикселях терминала
    scale_px = height / (2.0 * max_r * 1.35)
    order = sorted(bodies, key=lambda b: -math.dist(eye, b["position"]))  # type: ignore
    for b in order:
        pos = b["position"]
        color = _hex_to_rgb(b.get("color", "#4fd1c5"))
        scr = to_screen(pos)
        if not scr:
            continue
        sx, sy, sz = scr
        r_px = max(b["radius"] * scale_px, 0.6)
        if r_px < 1.2:
            # одна точка плотностью по глубине: ближе — плотнее
            near = 1.0 - min(max((sz / (d * 1.35) - 0.3) / 0.7, 0.0), 1.0)
            dens = 3 + int(near * (len(DENSITY) - 4))
            dens = max(3, min(dens, len(DENSITY) - 1))
            canvas.plot(int(sx), int(sy), sz, DENSITY[dens], color)
            continue
        # диск: по клеткам, яркость — по расстоянию от центра
        ri = int(math.ceil(r_px))
        for dy in range(-ri, ri + 1):
            for dx in range(-ri, ri + 1):
                dist = math.sqrt(dx * dx + dy * dy)
                if dist > r_px:
                    continue
                # псевдо-освещение сверху-слева
                light = max(0.15, 1.0 - (dist / max(r_px, 1e-9)) ** 2)
                level = int(light * (len(DENSITY) - 1))
                level = max(1, min(level, len(DENSITY) - 1))
                z = sz + dist * 0.01
                canvas.plot(int(sx + dx), int(sy + dy), z, DENSITY[level], color)

    lines = canvas.to_lines(use_color=use_color)
    # подписи
    header = f" TRIVORTEX ASCII · N={len(bodies)} · fov={fov:.0f}°"
    lines = [header] + lines
    return lines


def print_ascii(lines: Sequence[str], stream=None) -> None:
    """Do print ascii for lines, stream and return the result."""
    import sys

    stream = stream or sys.stdout
    for ln in lines:
        stream.write(ln + "\n")
