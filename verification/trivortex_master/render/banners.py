#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Библиотека баннеров и рамок для PNG-кадров и отчётов.

Рисует в Frame (pure_raster) декоративные элементы стиля AURORA:
титульные плашки, статус-бары, легенды тел. Использует font_5x7.
"""

from __future__ import annotations
from render.font_5x7 import draw_text
from render.pure_raster import Frame

ICE = (125, 211, 252)
GOLD = (232, 199, 102)
GRN = (52, 211, 153)
RED = (255, 95, 110)
VIO = (167, 139, 250)
DARK = (13, 22, 40)
PANEL = (22, 38, 61)


def title_bar(frame: Frame, title: str, width_frac: float = 1.0) -> None:
    """Титульная плашка сверху кадра: тёмная панель + золотой текст."""
    w = int(frame.w * width_frac)
    h = 14
    for y in range(h):
        for x in range(w):
            frame.set_pixel(x, y, -1e-6, PANEL)
    draw_text(frame, 4, 3, title[: (frame.w - 8) // 6], GOLD)


def status_bar(frame: Frame, fraction: float, y: int = None) -> None:
    """Полоса прогресса в кадре: заполнение ICE на тёмном треке."""
    y = frame.h - 10 if y is None else y
    for x in range(frame.w - 8):
        frame.set_pixel(4 + x, y, -1e-6, PANEL)
    fill = int((frame.w - 8) * min(max(fraction, 0), 1))
    for x in range(fill):
        frame.set_pixel(4 + x, y, -1e-6, ICE)


def legend(frame: Frame, bodies, x: int = 6, y: int = 16) -> None:
    """Легенда тел: цветной квадратик + имя (латиницей, шрифт 5×7)."""
    cy = y
    for b in bodies:
        name = b.name.encode("ascii", "replace").decode()[:12]
        for dy in range(6):
            for dx in range(6):
                frame.set_pixel(
                    x + dx,
                    cy + dy,
                    -1e-6,
                    tuple(int(b.color.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)),
                )
        draw_text(frame, x + 10, cy, name, (230, 240, 255))
        cy += 9


def warn_banner(frame: Frame, text: str) -> None:
    """Красная плашка предупреждения (N=8 и т.п.)."""
    h = 12
    for yy in range(frame.h - h - 14, frame.h - 14):
        for xx in range(frame.w):
            frame.set_pixel(xx, yy, -1e-6, (59, 18, 32))
    draw_text(
        frame,
        4,
        frame.h - h - 11,
        ("! " + text.encode("ascii", "replace").decode())[: (frame.w - 8) // 6],
        RED,
    )


def decorate_frame(
    frame: Frame, title: str, bodies, fraction: float = 1.0, warn: str | None = None
) -> Frame:
    """Полный AURORA-декор кадра: титул + легенда + прогресс + плашка."""
    title_bar(frame, title)
    legend(frame, bodies)
    status_bar(frame, fraction)
    if warn:
        warn_banner(frame, warn)
    return frame
