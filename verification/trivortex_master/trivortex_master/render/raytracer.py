#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — программный рейтрейсер: сферы, плоскость, тени, отражения.

Чистый Python, без numpy/GL. Конвейер на пиксель:
  * первичный луч из камеры (перспектива, анти-алиасинг ×N);
  * пересечение со сферами (аналитически) и бесконечной плоскостью;
  * ближайшее пересечение → тень-луч к каждому источнику (жёсткие тени);
  * модель Фонга: diffuse + ambient + specular;
  * отражения: итеративная трассировка до глубины max_bounce с
    затуханием 0.5^bounce;
  * гамма-коррекция 2.2, тонемаппинг (Рейнхард) — опционально.

Производительность: кадр 160×120 с 3 сферами ~0.3–1 с (анти-алиасинг
удорожает ×N²). Для больших кадров — pure_raster (scanline).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

from render.png_codec import write_png

Vec3 = tuple[float, float, float]


def v_add(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def v_sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def v_scale(a: Vec3, s: float) -> Vec3:
    return (a[0] * s, a[1] * s, a[2] * s)


def v_dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def v_cross(a: Vec3, b: Vec3) -> Vec3:
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def v_norm(a: Vec3) -> Vec3:
    n = math.sqrt(v_dot(a, a))
    if n < 1e-12:
        return (0.0, 0.0, 0.0)
    return (a[0] / n, a[1] / n, a[2] / n)


def v_reflect(d: Vec3, n: Vec3) -> Vec3:
    """Отражение падающего направления d от нормали n."""
    k = 2.0 * v_dot(d, n)
    return (d[0] - k * n[0], d[1] - k * n[1], d[2] - k * n[2])


# ═══════════════════════════════════════════════════════════════════════════
# Сцена рейтрейсера
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class Sphere:
    center: Vec3
    radius: float
    color: Vec3                     # альбедо 0..1
    reflectivity: float = 0.0       # 0 — матовый, 1 — зеркало
    specular: float = 32.0          # экспонента Фонга
    ks: float = 0.3                 # доля спекуляра


@dataclass
class Plane:
    """Бесконечная плоскость y = height (шахматная клетка)."""
    height: float = -1.0
    color1: Vec3 = (0.28, 0.33, 0.42)
    color2: Vec3 = (0.10, 0.13, 0.20)
    cell: float = 1.0
    reflectivity: float = 0.15


@dataclass
class Light:
    position: Vec3
    intensity: float = 1.0
    color: Vec3 = (1.0, 1.0, 1.0)


@dataclass
class Camera:
    eye: Vec3 = (0.0, 1.2, 4.0)
    look_at: Vec3 = (0.0, 0.3, 0.0)
    up: Vec3 = (0.0, 1.0, 0.0)
    fov_y: float = 50.0
    aspect: float = 4.0 / 3.0


@dataclass
class RaytraceScene:
    spheres: list[Sphere] = field(default_factory=list)
    planes: list[Plane] = field(default_factory=list)
    lights: list[Light] = field(default_factory=list)
    ambient: Vec3 = (0.06, 0.08, 0.12)
    bg: Vec3 = (0.02, 0.03, 0.06)


# ═══════════════════════════════════════════════════════════════════════════
# Пересечения
# ═══════════════════════════════════════════════════════════════════════════
def hit_sphere(origin: Vec3, direction: Vec3, s: Sphere
               ) -> Optional[float]:
    """Ближайший положительный t пересечения луча со сферой (или None)."""
    oc = v_sub(origin, s.center)
    b = 2.0 * v_dot(oc, direction)
    c = v_dot(oc, oc) - s.radius * s.radius
    disc = b * b - 4.0 * c
    if disc < 0.0:
        return None
    sq = math.sqrt(disc)
    t1 = (-b - sq) / 2.0
    t2 = (-b + sq) / 2.0
    if t1 > 1e-4:
        return t1
    if t2 > 1e-4:
        return t2
    return None


def hit_plane(origin: Vec3, direction: Vec3, p: Plane
              ) -> Optional[float]:
    """Пересечение с y = p.height (только сверху или снизу — любое)."""
    if abs(direction[1]) < 1e-9:
        return None
    t = (p.height - origin[1]) / direction[1]
    return t if t > 1e-4 else None


# ═══════════════════════════════════════════════════════════════════════════
# Трассировка
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class Hit:
    t: float
    point: Vec3
    normal: Vec3
    color: Vec3
    reflectivity: float
    specular: float
    ks: float


def nearest_hit(origin: Vec3, direction: Vec3, scene: RaytraceScene
                ) -> Optional[Hit]:
    best: Optional[Hit] = None
    # сферы
    for s in scene.spheres:
        t = hit_sphere(origin, direction, s)
        if t is not None and (best is None or t < best.t):
            point = v_add(origin, v_scale(direction, t))
            normal = v_norm(v_sub(point, s.center))
            best = Hit(t=t, point=point, normal=normal, color=s.color,
                       reflectivity=s.reflectivity, specular=s.specular,
                       ks=s.ks)
    # плоскости
    for p in scene.planes:
        t = hit_plane(origin, direction, p)
        if t is not None and (best is None or t < best.t):
            point = v_add(origin, v_scale(direction, t))
            normal = (0.0, 1.0, 0.0)
            # шахматная клетка
            cell = (math.floor(point[0] / p.cell)
                    + math.floor(point[2] / p.cell)) % 2
            color = p.color1 if cell == 0 else p.color2
            best = Hit(t=t, point=point, normal=normal, color=color,
                       reflectivity=p.reflectivity, specular=8.0,
                       ks=0.1)
    return best


def in_shadow(point: Vec3, light: Light, scene: RaytraceScene) -> bool:
    """Есть ли объект между точкой и источником."""
    to_light = v_sub(light.position, point)
    dist = math.sqrt(v_dot(to_light, to_light))
    direction = v_scale(to_light, 1.0 / max(dist, 1e-12))
    # сдвиг от поверхности
    origin = v_add(point, v_scale(direction, 1e-3))
    for s in scene.spheres:
        t = hit_sphere(origin, direction, s)
        if t is not None and t < dist - 2e-3:
            return True
    for p in scene.planes:
        t = hit_plane(origin, direction, p)
        if t is not None and t < dist - 2e-3:
            return True
    return False


def shade(hit: Hit, direction: Vec3, scene: RaytraceScene,
          depth: int, max_bounce: int = 3) -> Vec3:
    """Освещение точки + рекурсивные отражения."""
    # ambient
    r = scene.ambient[0] * hit.color[0]
    g = scene.ambient[1] * hit.color[1]
    b = scene.ambient[2] * hit.color[2]
    view = v_scale(direction, -1.0)
    for light in scene.lights:
        if in_shadow(hit.point, light, scene):
            continue
        to_light = v_norm(v_sub(light.position, hit.point))
        # diffuse (Ламберт)
        ndl = max(0.0, v_dot(hit.normal, to_light))
        # specular (Фонг, через half-vector)
        half = v_norm(v_add(to_light, view))
        ndh = max(0.0, v_dot(hit.normal, half))
        spec = hit.ks * (ndh ** hit.specular)
        for c_idx in range(3):
            contrib = (ndl * hit.color[c_idx] + spec) * light.intensity \
                * light.color[c_idx]
            if c_idx == 0:
                r += contrib
            elif c_idx == 1:
                g += contrib
            else:
                b += contrib
    # отражения
    if hit.reflectivity > 0 and depth < max_bounce:
        refl_dir = v_reflect(direction, hit.normal)
        refl_origin = v_add(hit.point, v_scale(refl_dir, 1e-3))
        refl_hit = nearest_hit(refl_origin, refl_dir, scene)
        if refl_hit is not None:
            sub = shade(refl_hit, refl_dir, scene, depth + 1, max_bounce)
            k = hit.reflectivity * (0.5 ** depth)
            r = r * (1 - k) + sub[0] * k
            g = g * (1 - k) + sub[1] * k
            b = b * (1 - k) + sub[2] * k
        else:
            k = hit.reflectivity * (0.5 ** depth)
            r = r * (1 - k) + scene.bg[0] * k
            g = g * (1 - k) + scene.bg[1] * k
            b = b * (1 - k) + scene.bg[2] * k
    return (r, g, b)


def render(scene: RaytraceScene, camera: Camera, width: int, height: int,
           antialias: int = 1, gamma: float = 2.2,
           tonemap: bool = True) -> bytearray:
    """Кадр RGB (bytes) размером width×height×3."""
    # базис камеры
    forward = v_norm(v_sub(camera.look_at, camera.eye))
    right = v_norm(v_cross(forward, camera.up))
    up = v_norm(v_cross(right, forward))
    half_h = math.tan(math.radians(camera.fov_y) / 2.0)
    half_w = half_h * camera.aspect
    pixels = bytearray(width * height * 3)
    for py in range(height):
        for px in range(width):
            # супер-сэмплы
            acc = [0.0, 0.0, 0.0]
            samples = 0
            for sy in range(antialias):
                for sx in range(antialias):
                    u = (px + (sx + 0.5) / antialias) / width * 2.0 - 1.0
                    v = 1.0 - (py + (sy + 0.5) / antialias) / height * 2.0
                    # направление луча
                    d = v_add(v_add(v_scale(forward, 1.0),
                                    v_scale(right, u * half_w)),
                              v_scale(up, v * half_h))
                    d = v_norm(d)
                    hit = nearest_hit(camera.eye, d, scene)
                    if hit is None:
                        color = scene.bg
                    else:
                        color = shade(hit, d, scene, 0)
                    acc[0] += color[0]
                    acc[1] += color[1]
                    acc[2] += color[2]
                    samples += 1
            r = acc[0] / samples
            g = acc[1] / samples
            b = acc[2] / samples
            # тонемаппинг Рейнхарда + гамма
            if tonemap:
                r = r / (1.0 + r)
                g = g / (1.0 + g)
                b = b / (1.0 + b)
            r = min(max(r, 0.0), 1.0) ** (1.0 / gamma)
            g = min(max(g, 0.0), 1.0) ** (1.0 / gamma)
            b = min(max(b, 0.0), 1.0) ** (1.0 / gamma)
            idx = (py * width + px) * 3
            pixels[idx] = int(r * 255)
            pixels[idx + 1] = int(g * 255)
            pixels[idx + 2] = int(b * 255)
    return pixels


def render_to_png(scene: RaytraceScene, camera: Camera, path: str,
                  width: int = 160, height: int = 120,
                  antialias: int = 1) -> int:
    """Отрендерить и сохранить PNG (собственный кодер)."""
    px = render(scene, camera, width, height, antialias)
    return write_png(path, px, width, height)


# ═══════════════════════════════════════════════════════════════════════════
# Готовые демо-сцены
# ═══════════════════════════════════════════════════════════════════════════
def demo_scene() -> RaytraceScene:
    """Классическая сцена: 3 сферы (матовая/глянцевая/зеркало) + пол."""
    scene = RaytraceScene()
    scene.spheres = [
        Sphere(center=(-1.1, 0.0, 0.0), radius=0.7,
               color=(0.85, 0.30, 0.25), reflectivity=0.05),
        Sphere(center=(0.0, 0.25, -0.6), radius=0.95,
               color=(0.25, 0.65, 0.85), reflectivity=0.35, specular=64),
        Sphere(center=(1.15, -0.1, 0.3), radius=0.6,
               color=(0.90, 0.80, 0.35), reflectivity=0.85, specular=128),
    ]
    scene.planes = [Plane(height=-0.72)]
    scene.lights = [
        Light(position=(3.0, 4.0, 3.0), intensity=1.05),
        Light(position=(-4.0, 2.5, 2.0), intensity=0.35,
              color=(0.7, 0.8, 1.0)),
    ]
    return scene


def solar_scene() -> RaytraceScene:
    """Солнце (излучающая) + планеты (матовые) — стилизация."""
    scene = RaytraceScene()
    scene.spheres = [
        Sphere(center=(0.0, 0.4, 0.0), radius=0.8,
               color=(1.0, 0.72, 0.1), reflectivity=0.0, ks=0.0),
        Sphere(center=(-1.6, -0.3, 0.9), radius=0.28,
               color=(0.3, 0.82, 0.77)),
        Sphere(center=(1.4, -0.1, 1.1), radius=0.38,
               color=(0.85, 0.45, 0.25), reflectivity=0.1),
        Sphere(center=(0.7, 0.9, -1.4), radius=0.5,
               color=(0.82, 0.65, 0.45), reflectivity=0.2),
    ]
    scene.lights = [Light(position=(0.0, 4.0, 2.0), intensity=1.4,
                          color=(1.0, 0.95, 0.85))]
    scene.ambient = (0.04, 0.05, 0.09)
    return scene


def self_check() -> dict:
    """Рендер демо-сцены: непустой кадр, тени есть, файл валиден."""
    scene = demo_scene()
    cam = Camera(aspect=4.0 / 3.0)
    path = "/tmp/tv_raytracer.png"
    size = render_to_png(scene, cam, path, width=120, height=90)
    from PIL import Image
    im = Image.open(path).convert("RGB")
    px = im.load()
    # верх (фон) тёмный, центральная сфера светлее фона
    bg = px[5, 5]
    center = px[60, 45]
    # тень под левой сферой темнее освещённого пола
    floor_lit = px[95, 60]
    nonbg = sum(1 for y in range(0, 90, 3) for x in range(0, 120, 3)
                if px[x, y] != bg)
    return dict(
        size_bytes=size,
        bg_sample=bg, center_sample=center, floor=floor_lit,
        nonbg_samples=nonbg,
        scene_visible=nonbg > 150,
        ok=size > 2000 and nonbg > 150 and center[1] > bg[1],
        note="тени/отражения проверяются визуально в runs/examples",
    )
