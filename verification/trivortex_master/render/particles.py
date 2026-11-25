#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — система частиц: эмиттеры, интеграция, эффекты.

Движок частиц для визуализаций (взрывы при столкновениях, хвосты комет,
аккреционные диски, джеты):

  * Particle: позиция/скорость/жизнь/размер/цвет/тип;
  * Эмиттеры: точечный (взрыв), конус (джет), кольцо (диск),
    направленный (хвост кометы);
  * Интегратор: Эйлер с drag и гравитацией к опциональному аттрактору;
  * Эффекты: затухание размера/альфы с возрастом, цветовой сдвиг
    (жёлтый→красный для огня, белый→голубой для плазмы);
  * Рендер: аддитивные точки в Frame (pure_raster), GIF-анимации
    через animator.

Чистый Python; 200–500 частиц × 60 кадров — доли секунды.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Callable

from render.png_codec import write_png


@dataclass
class Particle:
    """Handle Particle."""

    x: float
    y: float
    z: float = 0.0
    vx: float = 0.0
    vy: float = 0.0
    vz: float = 0.0
    life: float = 1.0  # 0..1, убывает
    decay: float = 0.02  # скорость убывания жизни
    size: float = 1.0
    color: tuple[int, int, int] = (255, 200, 100)
    kind: str = "spark"  # spark | smoke | gas | debris


@dataclass
class EmitterConfig:
    """Настройки эмиттера."""

    origin: tuple[float, float, float] = (0.0, 0.0, 0.0)
    mode: str = "point"  # point | cone | ring | tail
    rate: int = 20  # частиц за тик
    speed: float = 1.0
    spread: float = math.pi / 4  # полуугол конуса
    direction: tuple[float, float, float] = (0.0, 1.0, 0.0)
    ring_radius: float = 1.0
    decay: float = 0.02
    size0: float = 1.0
    color0: tuple[int, int, int] = (255, 190, 90)
    lifetime_jitter: float = 0.5
    seed: int = 42


class ParticleSystem:
    """Контейнер частиц + обновление."""

    def __init__(
        self,
        gravity: tuple[float, float, float] | None = None,
        drag: float = 0.0,
        attractor: tuple[tuple[float, float, float], float] | None = None,
    ):
        """Do ParticleSystem.  init for gravity, drag, attractor and return the result."""
        self.particles: list[Particle] = []
        self.gravity = gravity or (0.0, 0.0, 0.0)
        self.drag = drag
        self.attractor = attractor  # (центр, GM)
        self._rng = random.Random()

    # ── эмиттеры ──
    def emit(self, cfg: EmitterConfig) -> None:
        """Выбросить cfg.rate частиц по режиму эмиттера."""
        rng = self._rng
        rng.seed(cfg.seed + len(self.particles))
        ox, oy, oz = cfg.origin
        dx, dy, dz = cfg.direction
        d_len = math.sqrt(dx * dx + dy * dy + dz * dz) or 1.0
        dx, dy, dz = dx / d_len, dy / d_len, dz / d_len
        for _ in range(cfg.rate):
            decay = cfg.decay * (1.0 + rng.uniform(-cfg.lifetime_jitter, cfg.lifetime_jitter) * 0.5)
            p = Particle(
                x=ox, y=oy, z=oz, decay=max(decay, 0.002), size=cfg.size0, color=cfg.color0
            )
            speed = cfg.speed * rng.uniform(0.6, 1.4)
            if cfg.mode == "point":
                # изотропный разлёт
                theta = rng.uniform(0, 2 * math.pi)
                cos_phi = rng.uniform(-1, 1)
                sin_phi = math.sqrt(1 - cos_phi * cos_phi)
                p.vx = speed * sin_phi * math.cos(theta)
                p.vy = speed * sin_phi * math.sin(theta)
                p.vz = speed * cos_phi
            elif cfg.mode == "cone":
                # конус вокруг направления
                theta = rng.uniform(0, 2 * math.pi)
                cos_a = 1.0 - rng.uniform(0, 1 - math.cos(cfg.spread))
                sin_a = math.sqrt(max(1 - cos_a * cos_a, 0.0))
                # базис вокруг направления
                ref = (1.0, 0.0, 0.0) if abs(dx) < 0.9 else (0.0, 1.0, 0.0)
                ux = dy * ref[2] - dz * ref[1]
                uy = dz * ref[0] - dx * ref[2]
                uz = dx * ref[1] - dy * ref[0]
                ul = math.sqrt(ux * ux + uy * uy + uz * uz) or 1.0
                ux, uy, uz = ux / ul, uy / ul, uz / ul
                wx = dy * uz - dz * uy
                wy = dz * ux - dx * uz
                wz = dx * uy - dy * ux
                p.vx = speed * (
                    cos_a * dx + sin_a * math.cos(theta) * ux + sin_a * math.sin(theta) * wx
                )
                p.vy = speed * (
                    cos_a * dy + sin_a * math.cos(theta) * uy + sin_a * math.sin(theta) * wy
                )
                p.vz = speed * (
                    cos_a * dz + sin_a * math.cos(theta) * uz + sin_a * math.sin(theta) * wz
                )
            elif cfg.mode == "ring":
                phi = rng.uniform(0, 2 * math.pi)
                rr = cfg.ring_radius * (0.9 + 0.2 * rng.random())
                p.x = ox + rr * math.cos(phi)
                p.y = oy + rr * math.sin(phi) * 0.15
                p.z = oz + rr * math.sin(phi)
                tangential = (-math.sin(phi), 0.0, math.cos(phi))
                p.vx = speed * tangential[0]
                p.vy = speed * 0.02 * rng.uniform(-1, 1)
                p.vz = speed * tangential[2]
            elif cfg.mode == "tail":
                # хвост: назад против направления + разброс
                p.vx = -dx * speed + rng.uniform(-0.2, 0.2) * speed
                p.vy = -dy * speed + rng.uniform(-0.2, 0.2) * speed
                p.vz = -dz * speed + rng.uniform(-0.2, 0.2) * speed
            self.particles.append(p)

    # ── физика ──
    def step(self, dt: float) -> None:
        """Продвинуть все частицы; мёртвые удалить."""
        alive: list[Particle] = []
        for p in self.particles:
            p.life -= p.decay * dt * 60.0
            if p.life <= 0:
                continue
            # ускорения
            ax, ay, az = self.gravity
            if self.attractor is not None:
                (cx, cy, cz), gm = self.attractor
                rx, ry, rz = cx - p.x, cy - p.y, cz - p.z
                r2 = rx * rx + ry * ry + rz * rz + 1e-6
                r = math.sqrt(r2)
                f = gm / (r2 * r)
                ax += f * rx
                ay += f * ry
                az += f * rz
            # drag
            if self.drag > 0:
                damp = math.exp(-self.drag * dt)
                p.vx *= damp
                p.vy *= damp
                p.vz *= damp
            p.vx += ax * dt
            p.vy += ay * dt
            p.vz += az * dt
            p.x += p.vx * dt
            p.y += p.vy * dt
            p.z += p.vz * dt
            alive.append(p)
        self.particles = alive

    @property
    def alive_count(self) -> int:
        """Handle ParticleSystem.alive count."""
        return len(self.particles)

    def total_energy(self) -> float:
        """Суммарная кинетическая энергия (диагностика)."""
        return sum(0.5 * (p.vx**2 + p.vy**2 + p.vz**2) for p in self.particles)


# ═══════════════════════════════════════════════════════════════════════════
# Эффекты старения
# ═══════════════════════════════════════════════════════════════════════════
def fire_palette(life: float) -> tuple[int, int, int]:
    """Жёлтый → оранжевый → красный → тёмный по мере угасания."""
    if life > 0.75:
        t = (life - 0.75) / 0.25
        return (255, int(230 - 60 * (1 - t)), int(120 * t))
    if life > 0.4:
        t = (life - 0.4) / 0.35
        return (int(255 * (0.6 + 0.4 * t)), int(160 * t + 40), 20)
    return (int(200 * life + 40), int(60 * life), 10)


def plasma_palette(life: float) -> tuple[int, int, int]:
    """Белый → голубой → фиолетовый."""
    if life > 0.6:
        t = (life - 0.6) / 0.4
        return (int(120 + 135 * t), int(180 + 75 * t), 255)
    return (int(120 * life + 20), int(140 * life + 30), int(255 * life))


def smoke_palette(life: float) -> tuple[int, int, int]:
    """Светло-серый → тёмный."""
    v = int(40 + 140 * life)
    return (v, v, v)


PALETTES: dict[str, Callable[[float], tuple[int, int, int]]] = {
    "fire": fire_palette,
    "plasma": plasma_palette,
    "smoke": smoke_palette,
}


# ═══════════════════════════════════════════════════════════════════════════
# Рендер частиц
# ═══════════════════════════════════════════════════════════════════════════
def draw_particles(
    frame, ps: ParticleSystem, palette: str = "fire", scale: float = 40.0, size_scale: float = 1.0
) -> None:
    """Нарисовать частицы в Frame (render.pure_raster.Frame), аддитивно.

    Проекция ортографическая: screen_x = cx + x·scale, screen_y =
    cy − y·scale (y вверх).
    """
    pal = PALETTES.get(palette, fire_palette)
    cx = frame.w / 2.0
    cy = frame.h / 2.0
    for p in ps.particles:
        sx = int(cx + p.x * scale)
        sy = int(cy - p.y * scale)
        color = pal(p.life)
        radius = max(1, int(p.size * size_scale * (0.5 + 0.5 * p.life)))
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:
                    px = sx + dx
                    py = sy + dy
                    if 0 <= px < frame.w and 0 <= py < frame.h:
                        idx = (py * frame.w + px) * 3
                        # аддитивное смешивание с насыщением
                        for c in range(3):
                            v = frame.pixels[idx + c] + color[c] // 3
                            frame.pixels[idx + c] = min(v, 255)


def render_frames(
    ps_list: list[ParticleSystem],
    width: int,
    height: int,
    palette: str = "fire",
    bg=(13, 22, 40),
    paths: list[str] | None = None,
) -> list[int]:
    """Сохранить последовательность кадров в PNG (возвращает размеры)."""
    from render.pure_raster import Frame

    sizes = []
    for i, ps in enumerate(ps_list):
        f = Frame(width, height, bg=bg)
        draw_particles(f, ps, palette)
        if paths:
            sizes.append(write_png(paths[i], f.pixels, width, height))
        else:
            tmp = f"/tmp/tv_particles_{i:03d}.png"
            sizes.append(write_png(tmp, f.pixels, width, height))
    return sizes


# ═══════════════════════════════════════════════════════════════════════════
# Готовые пресеты
# ═══════════════════════════════════════════════════════════════════════════
def explosion(origin=(0.0, 0.0, 0.0), n: int = 150, speed: float = 2.0) -> ParticleSystem:
    """Взрыв: изотропный выброс с гравитацией и drag."""
    ps = ParticleSystem(gravity=(0, -0.8, 0), drag=0.4)
    ps.emit(
        EmitterConfig(
            origin=origin,
            mode="point",
            rate=n,
            speed=speed,
            decay=0.03,
            size0=2.2,
            color0=(255, 200, 90),
            seed=7,
        )
    )
    return ps


def comet_tail(comet_pos=(0.0, 0.0, 0.0), velocity=(-1.0, 0.0, 0.0)) -> ParticleSystem:
    """Хвост кометы: эмиттер против скорости + лёгкий отталкивание."""
    ps = ParticleSystem(gravity=(0.05, 0, 0), drag=0.1)
    ps.emit(
        EmitterConfig(
            origin=comet_pos,
            mode="tail",
            rate=60,
            direction=velocity,
            speed=0.8,
            decay=0.02,
            size0=1.6,
            color0=(150, 220, 255),
            seed=11,
        )
    )
    return ps


def accretion_disk(center=(0.0, 0.0, 0.0), gm: float = 3.0) -> ParticleSystem:
    """Аккреционный диск: кольцо частиц с притяжением к центру."""
    ps = ParticleSystem(attractor=(center, gm))
    ps.emit(
        EmitterConfig(
            origin=center,
            mode="ring",
            rate=220,
            ring_radius=1.6,
            speed=1.35,
            decay=0.004,
            size0=1.3,
            color0=(255, 170, 80),
            seed=5,
        )
    )
    return ps


def jet(origin=(0.0, -0.5, 0.0), direction=(0.0, 1.0, 0.0)) -> ParticleSystem:
    """Релятивистский джет: конус вдоль направления."""
    ps = ParticleSystem(drag=0.05)
    ps.emit(
        EmitterConfig(
            origin=origin,
            mode="cone",
            rate=120,
            direction=direction,
            speed=2.4,
            spread=math.radians(12),
            decay=0.02,
            size0=1.8,
            color0=(170, 200, 255),
            seed=3,
        )
    )
    return ps


def self_check() -> dict:
    """Взрыв: частицы рождаются, живут, умирают; энергия падает с drag."""
    ps = explosion()
    n0 = ps.alive_count
    e0 = ps.total_energy()
    for _ in range(30):
        ps.step(1 / 30)
    n30 = ps.alive_count
    # все частицы должны умереть за ~1/0.03/60 с ≈ 0.55 с → 30 тиков хватает
    all_dead = n30 == 0
    # диск: частицы не мгновенно улетают
    disk = accretion_disk()
    disk.step(0.05)
    r_mean = math.sqrt(
        sum(p.x**2 + p.y**2 + p.z**2 for p in disk.particles) / max(disk.alive_count, 1)
    )
    return dict(
        explosion_n0=n0,
        explosion_n_after_30=n30,
        explosion_energy0=e0,
        explosion_ok=n0 == 150 and all_dead,
        disk_alive=disk.alive_count,
        disk_mean_radius=r_mean,
        disk_ok=disk.alive_count > 180 and 0.5 < r_mean < 4.0,
        ok=(n0 == 150 and all_dead and disk.alive_count > 180),
    )
