#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — композитор кадров: многослойный рендер.

Объединяет выходы всех рендер-бэкендов в один кадр:

  * Layer: изображение (RGB-массив), позиция, альфа, blend-режим
    (normal / additive / multiply), z-порядок;
  * FrameComposer: стоп слоёв → compose() → итоговый RGB;
  * body_layer / particle_layer / grid_layer / label_layer —
    генераторы слоёв из стандартных подсистем;
  * vignette / starfield_background — постэффекты;
  * compose_to_png: экспорт через render.png_codec.

Самопроверка: два слоя смешиваются аддитивно без насыщения; альфа
0.5 даёт полусумму; порядок слоёв определяет видимость.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Sequence

from render.png_codec import write_png


@dataclass
class Layer:
    """Слой кадра."""

    name: str
    pixels: bytearray  # RGB, w*h*3
    w: int
    h: int
    alpha: float = 1.0  # глобальная прозрачность
    blend: str = "normal"  # normal | additive | multiply
    z: int = 0  # порядок наложения (низший снизу)


class FrameComposer:
    """Композитор: стоп слоёв → итоговый кадр."""

    def __init__(self, width: int, height: int, background: tuple[int, int, int] = (10, 17, 32)):
        self.width = width
        self.height = height
        self.layers: list[Layer] = []
        self.background = background

    def add(self, layer: Layer) -> FrameComposer:
        self.layers.append(layer)
        self.layers.sort(key=lambda l: l.z)
        return self

    def _empty(self) -> list[float]:
        bg = self.background
        return [float(c) for c in bg] * (self.width * self.height)

    def compose(self) -> bytearray:
        """Наложить все слои на фон (в порядке z)."""
        out = self._empty()
        for layer in self.layers:
            if layer.w != self.width or layer.h != self.height:
                # масштабирование не поддерживаем — центрируем с обрезкой
                layer = _fit_layer(layer, self.width, self.height)
            for i in range(self.width * self.height):
                j = 3 * i
                a = layer.alpha
                if layer.blend == "additive":
                    for c in range(3):
                        v = out[j + c] + a * layer.pixels[j + c]
                        out[j + c] = min(v, 255.0)
                elif layer.blend == "multiply":
                    for c in range(3):
                        out[j + c] = out[j + c] * (1 - a + a * layer.pixels[j + c] / 255.0)
                else:  # normal (over)
                    for c in range(3):
                        out[j + c] = out[j + c] * (1 - a) + a * layer.pixels[j + c]
        result = bytearray(int(v) for v in out)
        return result


def _fit_layer(layer: Layer, w: int, h: int) -> Layer:
    """Подогнать слой: копия с центрированием/обрезкой до w×h."""
    pix = bytearray(w * h * 3)
    cw, ch = min(layer.w, w), min(layer.h, h)
    ox, oy = (w - cw) // 2, (h - ch) // 2
    for y in range(ch):
        src = 3 * (y * layer.w)
        dst = 3 * ((oy + y) * w + ox)
        pix[dst : dst + 3 * cw] = layer.pixels[src : src + 3 * cw]
    return Layer(
        name=layer.name, pixels=pix, w=w, h=h, alpha=layer.alpha, blend=layer.blend, z=layer.z
    )


# ═══════════════════════════════════════════════════════════════════════════
# Генераторы слоёв
# ═══════════════════════════════════════════════════════════════════════════
def solid_layer(name: str, w: int, h: int, color: tuple[int, int, int], z: int = 0) -> Layer:
    """Сплошной цвет."""
    return Layer(name=name, pixels=bytearray(color) * (w * h), w=w, h=h, z=z)


def body_layer(
    w: int,
    h: int,
    positions: Sequence[tuple[float, float]],
    radius_px: int = 6,
    color: tuple[int, int, int] = (79, 209, 197),
    z: int = 10,
) -> Layer:
    """Слой тел: круги в экранных координатах."""
    pix = bytearray((0, 0, 0)) * (w * h)
    for cx, cy in positions:
        for dy in range(-radius_px, radius_px + 1):
            for dx in range(-radius_px, radius_px + 1):
                if dx * dx + dy * dy <= radius_px * radius_px:
                    x, y = int(cx + dx), int(cy + dy)
                    if 0 <= x < w and 0 <= y < h:
                        j = 3 * (y * w + x)
                        pix[j : j + 3] = bytes(color)
    return Layer(name="bodies", pixels=pix, w=w, h=h, blend="additive", z=z)


def starfield_layer(w: int, h: int, n_stars: int = 120, seed: int = 5, z: int = -10) -> Layer:
    """Слой звёздного фона (детерминированный хэш-рандом)."""
    pix = bytearray((0, 0, 0)) * (w * h)
    state = seed
    for _ in range(n_stars):
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        x = state % w
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        y = state % h
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        bright = 120 + (state % 136)
        j = 3 * (y * w + x)
        pix[j] = min(255, bright)
        pix[j + 1] = min(255, bright)
        pix[j + 2] = min(255, bright + 20)
    return Layer(name="starfield", pixels=pix, w=w, h=h, blend="additive", z=z)


def grid_layer(
    w: int, h: int, spacing: int = 40, color: tuple[int, int, int] = (35, 52, 74), z: int = -5
) -> Layer:
    """Слой координатной сетки."""
    pix = bytearray((0, 0, 0)) * (w * h)
    for x in range(0, w, spacing):
        for y in range(h):
            j = 3 * (y * w + x)
            pix[j : j + 3] = bytes(color)
    for y in range(0, h, spacing):
        for x in range(w):
            j = 3 * (y * w + x)
            pix[j : j + 3] = bytes(color)
    return Layer(name="grid", pixels=pix, w=w, h=h, blend="additive", z=z)


def vignette_layer(w: int, h: int, strength: float = 0.4, z: int = 50) -> Layer:
    """Постэффект: затемнение краёв (multiply)."""
    pix = bytearray(w * h * 3)
    cx, cy = w / 2.0, h / 2.0
    max_r = math.sqrt(cx * cx + cy * cy)
    for y in range(h):
        for x in range(w):
            r = math.sqrt((x - cx) ** 2 + (y - cy) ** 2) / max_r
            v = 1.0 - strength * max(0.0, r - 0.55) / 0.45
            v = max(0.2, min(1.0, v))
            g = int(v * 255)
            j = 3 * (y * w + x)
            pix[j] = pix[j + 1] = pix[j + 2] = g
    return Layer(name="vignette", pixels=pix, w=w, h=h, blend="multiply", z=z)


def compose_to_png(compositor: FrameComposer, path: str) -> int:
    """Собрать кадр и сохранить PNG."""
    pixels = compositor.compose()
    return write_png(path, pixels, compositor.width, compositor.height)


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Аддитивное смешение не насыщается сверх 255; альфа 0.5 = полусумма;
    z-порядок: верхний слой перекрывает нижний."""
    w, h = 64, 48
    # аддитив: 100 + 100 = 200 (не насыщение); blend задаётся явно
    c = FrameComposer(w, h, background=(0, 0, 0))
    la = solid_layer("a", w, h, (100, 100, 100), z=0)
    la.blend = "additive"
    lb = solid_layer("b", w, h, (100, 100, 100), z=1)
    lb.blend = "additive"
    c.add(la)
    c.add(lb)
    pix = c.compose()
    additive_ok = pix[0] == 200

    # альфа 0.5: фон 0 + слой 200 → 100
    c2 = FrameComposer(w, h, background=(0, 0, 0))
    c2.add(solid_layer("s", w, h, (200, 200, 200), z=0))
    c2.layers[-1].alpha = 0.5
    pix2 = c2.compose()
    alpha_ok = pix2[0] == 100

    # z-порядок: верхний перекрывает
    c3 = FrameComposer(w, h, background=(0, 0, 0))
    c3.add(solid_layer("low", w, h, (255, 0, 0), z=0))
    c3.add(solid_layer("high", w, h, (0, 255, 0), z=10))
    pix3 = c3.compose()
    zorder_ok = pix3[1] == 255 and pix3[0] == 0

    # полный кадр со звёздами + телами + виньетка: не пустой
    c4 = FrameComposer(w, h)
    c4.add(starfield_layer(w, h, n_stars=200, seed=3))
    c4.add(body_layer(w, h, [(32, 24), (48, 30)], radius_px=5))
    c4.add(vignette_layer(w, h, strength=0.3))
    path = "/tmp/tv_compositor.png"
    size = compose_to_png(c4, path)
    nonblack = sum(1 for v in c4.compose()[: 3 * 200] if v > 10)
    frame_ok = size > 1000 and nonblack > 30
    return dict(
        additive_ok=additive_ok,
        alpha_ok=alpha_ok,
        zorder_ok=zorder_ok,
        frame_bytes=size,
        nonblack=nonblack,
        frame_ok=frame_ok,
        all_ok=additive_ok and alpha_ok and zorder_ok and frame_ok,
        note="слои: starfield(-10) → grid(-5) → bodies(10) → vignette(50)",
    )
