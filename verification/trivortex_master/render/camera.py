#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — камера: орбитальная, следящая, кинематографические
пути, плавность (damping), тряска.

Единая абстракция камеры для всех рендер-бэкендов:

  * OrbitCamera — вращение вокруг цели (yaw/pitch/dist, инерция);
  * FollowCamera — следование за телом сцены с экспоненциальным
    сглаживанием (позиция и взгляд);
  * PathCamera — ключевые кадры (waypoints) с Катмуллом-Ромом по
    позиции/цели/fov (пролёты, раскадровки);
  * ShakeCamera — наложение затухающей тряски (взрывы, столкновения);
  * cinematic_sequence — готовые движения: орбита-облёт, наезд,
    отъезд с проезжающим фокусом.

Экспортирует view-матрицу в соглашениях pure_raster (совместимо с
mat_look_at), поэтому камера подключается к любому движку рендера.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional, Sequence

Vec3 = tuple[float, float, float]


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def _lerp3(a: Vec3, b: Vec3, t: float) -> Vec3:
    return (_lerp(a[0], b[0], t), _lerp(a[1], b[1], t),
            _lerp(a[2], b[2], t))


def _dist(a: Vec3, b: Vec3) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


# ═══════════════════════════════════════════════════════════════════════════
# Орбитальная камера
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class OrbitCamera:
    """Камера на орбите вокруг цели."""
    target: Vec3 = (0.0, 0.0, 0.0)
    distance: float = 5.0
    yaw: float = 0.6            # рад
    pitch: float = 0.35
    fov: float = 50.0
    # плавность
    damping: float = 0.12       # 0 — мгновенно, 1 — не двигается
    # целевые значения (куда стремимся)
    _target_yaw: float = 0.6
    _target_pitch: float = 0.35
    _target_dist: float = 5.0
    _target_pos: Vec3 = (0.0, 0.0, 0.0)

    def orbit(self, d_yaw: float, d_pitch: float) -> None:
        """Повернуть орбиту (накапливается с плавностью)."""
        self._target_yaw += d_yaw
        self._target_pitch = max(-1.45,
                                 min(1.45, self._target_pitch + d_pitch))

    def zoom(self, factor: float) -> None:
        """Приблизить (factor<1) / отдалить (factor>1)."""
        self._target_dist = max(0.2, self._target_dist * factor)

    def pan(self, dx: float, dy: float) -> None:
        """Сдвиг цели в плоскости экрана."""
        # базис камеры
        cy, sy = math.cos(self.yaw), math.sin(self.yaw)
        right = (cy, 0.0, -sy)
        up = (-sy * math.sin(self.pitch),
              math.cos(self.pitch), -cy * math.sin(self.pitch))
        t = self._target_pos
        self._target_pos = (t[0] - dx * right[0] - dy * up[0],
                            t[1] - dy * up[1],
                            t[2] - dx * right[2] - dy * up[2])

    def update(self, dt: float) -> None:
        """Сглаживание к целевым значениям (кадровая динамика)."""
        k = 1.0 - self.damping ** max(dt / 0.016, 0.01)
        self.yaw = _lerp(self.yaw, self._target_yaw, k)
        self.pitch = _lerp(self.pitch, self._target_pitch, k)
        self.distance = _lerp(self.distance, self._target_dist, k)
        self.target = _lerp3(self.target, self._target_pos, k)

    def eye(self) -> Vec3:
        """Позиция камеры на орбите."""
        cp, sp = math.cos(self.pitch), math.sin(self.pitch)
        cy, sy = math.cos(self.yaw), math.sin(self.yaw)
        return (self.target[0] + self.distance * cp * cy,
                self.target[1] + self.distance * sp,
                self.target[2] + self.distance * cp * sy)

    def view_params(self) -> dict:
        """Параметры для mat_look_at."""
        return dict(eye=self.eye(), target=self.target,
                    up=(0.0, 1.0, 0.0), fov=self.fov)


# ═══════════════════════════════════════════════════════════════════════════
# Следящая камера
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class FollowCamera:
    """Слежение за движущимся телом со сглаживанием."""
    offset: Vec3 = (0.0, 1.5, 4.0)
    look_ahead: float = 0.5       # смотреть вперёд по скорости (сек)
    smoothing: float = 0.15
    fov: float = 55.0
    _pos: Vec3 = field(default=(0.0, 1.5, 4.0))

    def update(self, dt: float, body_pos: Vec3, body_vel: Vec3) -> None:
        """Обновить по позиции/скорости сопровождаемого тела."""
        future = (body_pos[0] + body_vel[0] * self.look_ahead,
                  body_pos[1] + body_vel[1] * self.look_ahead,
                  body_pos[2] + body_vel[2] * self.look_ahead)
        desired = (future[0] + self.offset[0],
                   future[1] + self.offset[1],
                   future[2] + self.offset[2])
        k = 1.0 - self.smoothing ** max(dt / 0.016, 0.01)
        self._pos = _lerp3(self._pos, desired, k)

    def eye(self) -> Vec3:
        return self._pos


# ═══════════════════════════════════════════════════════════════════════════
# Камера на пути (Катмулл-Ром по ключевым кадрам)
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class CameraKey:
    """Ключевой кадр: позиция, цель, fov."""
    t: float
    eye: Vec3
    target: Vec3
    fov: float = 50.0


def _catmull_rom_1d(p0, p1, p2, p3, u):
    return (0.5 * ((2 * p1) + (-p0 + p2) * u
                   + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u
                   + (-p0 + 3 * p1 - 3 * p2 + p3) * u * u * u))


class PathCamera:
    """Кинематографический пролёт по ключевым кадрам."""

    def __init__(self, keys: Sequence[CameraKey]):
        if len(keys) < 2:
            raise ValueError("нужно ≥2 ключевых кадра")
        self.keys = sorted(keys, key=lambda k: k.t)

    def _segment(self, t: float) -> tuple[int, float]:
        """Найти сегмент и локальный параметр u ∈ [0,1)."""
        keys = self.keys
        for i in range(len(keys) - 1):
            if keys[i].t <= t <= keys[i + 1].t:
                span = keys[i + 1].t - keys[i].t
                u = 0.5 if span <= 0 else (t - keys[i].t) / span
                return i, u
        return (len(keys) - 2, 1.0) if t > keys[-1].t else (0, 0.0)

    def sample(self, t: float) -> dict:
        """Состояние камеры в момент t (Катмулл-Ром по всем полям)."""
        keys = self.keys
        i, u = self._segment(t)
        # соседние ключи с клампом
        def k(idx):
            return keys[max(0, min(idx, len(keys) - 1))]
        k0, k1, k2, k3 = k(i - 1), k(i), k(i + 1), k(i + 2)
        eye = tuple(_catmull_rom_1d(k0.eye[d], k1.eye[d], k2.eye[d],
                                    k3.eye[d], u) for d in range(3))
        target = tuple(_catmull_rom_1d(k0.target[d], k1.target[d],
                                       k2.target[d], k3.target[d], u)
                       for d in range(3))
        fov = _catmull_rom_1d(k0.fov, k1.fov, k2.fov, k3.fov, u)
        return dict(eye=eye, target=target, fov=fov)

    def duration(self) -> float:
        return self.keys[-1].t - self.keys[0].t


# ═══════════════════════════════════════════════════════════════════════════
# Тряска
# ═══════════════════════════════════════════════════════════════════════════
class ShakeCamera:
    """Обёртка над любой камерой: затухающая случайная тряска."""

    def __init__(self, base, amplitude: float = 0.0,
                 frequency: float = 20.0, decay: float = 3.0,
                 seed: int = 1):
        self.base = base            # OrbitCamera / PathCamera / ...
        self.amplitude = amplitude
        self.frequency = frequency
        self.decay = decay
        self._t = 0.0
        import random
        self._rng = random.Random(seed)

    def kick(self, strength: float) -> None:
        """Импульс тряски (взрыв/удар)."""
        self.amplitude = max(self.amplitude, strength)

    def update(self, dt: float) -> None:
        self._t += dt
        self.amplitude *= math.exp(-self.decay * dt)
        upd = getattr(self.base, "update", None)
        if upd is not None and not isinstance(self.base, PathCamera):
            upd(dt)

    def eye(self) -> Vec3:
        eye = self.base.eye()
        if self.amplitude < 1e-4:
            return eye
        jitter = self.amplitude
        return (eye[0] + self._rng.uniform(-jitter, jitter),
                eye[1] + self._rng.uniform(-jitter, jitter),
                eye[2] + self._rng.uniform(-jitter, jitter))

    def view_params(self) -> dict:
        vp = self.base.view_params() if hasattr(self.base, "view_params") \
            else dict(eye=self.eye(), target=(0, 0, 0), fov=50.0)
        vp["eye"] = self.eye()
        return vp


# ═══════════════════════════════════════════════════════════════════════════
# Кинематографические последовательности
# ═══════════════════════════════════════════════════════════════════════════
def cinematic_sequence(kind: str = "flyby",
                       radius: float = 3.0) -> PathCamera:
    """Готовые движения камеры (пресеты раскадровки)."""
    if kind == "flyby":
        # облёт: полный круг вокруг цели с лёгким изменением высоты
        keys = []
        for i in range(9):
            ang = 2 * math.pi * i / 8
            keys.append(CameraKey(
                t=i * 0.5,
                eye=(radius * math.cos(ang), 1.2 + 0.4 * math.sin(2 * ang),
                     radius * math.sin(ang)),
                target=(0.0, 0.0, 0.0),
                fov=50.0 + 6.0 * math.sin(ang)))
        return PathCamera(keys)
    if kind == "dolly_in":
        # наезд от общего к крупному
        return PathCamera([
            CameraKey(0.0, (8.0, 3.0, 8.0), (0, 0, 0), 45.0),
            CameraKey(2.0, (4.0, 1.6, 4.0), (0, 0.2, 0), 50.0),
            CameraKey(4.0, (1.8, 0.8, 1.8), (0, 0.3, 0), 58.0),
            CameraKey(5.5, (1.0, 0.5, 1.0), (0, 0.35, 0), 62.0),
        ])
    if kind == "pull_back":
        return PathCamera([
            CameraKey(0.0, (1.2, 0.6, 1.2), (0, 0.3, 0), 60.0),
            CameraKey(2.5, (4.0, 2.0, 4.5), (0, 0, 0), 50.0),
            CameraKey(5.0, (12.0, 5.0, 12.0), (0, 0, 0), 42.0),
        ])
    raise ValueError(f"неизвестная последовательность: {kind}")


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Орбита держит дистанцию; путь проходит через ключи; тряска гаснет."""
    cam = OrbitCamera(distance=5.0)
    cam.orbit(0.5, 0.1)
    for _ in range(120):
        cam.update(1 / 60)
    dist = _dist(cam.eye(), cam.target)
    orbit_ok = abs(dist - 5.0) < 0.2

    path = cinematic_sequence("flyby", radius=3.0)
    mid = path.sample(2.0)
    # в t=2.0 (ключ 4) радиус ≈ 3
    r_mid = math.sqrt(sum(c * c for c in mid["eye"]))
    path_ok = abs(r_mid - 3.0) < 0.35 and path.duration() == 4.0

    shake = ShakeCamera(OrbitCamera(), amplitude=0.8)
    shake.kick(0.5)
    a0 = shake.amplitude
    for _ in range(180):
        shake.update(1 / 60)
    shake_ok = shake.amplitude < a0 * 0.05

    follow = FollowCamera()
    follow.update(1 / 60, (10.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    for _ in range(300):
        follow.update(1 / 60, (10.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    fe = follow.eye()
    follow_ok = abs(fe[0] - 10.0) < 0.3
    return dict(
        orbit_distance=dist, orbit_ok=orbit_ok,
        path_radius_mid=r_mid, path_ok=path_ok,
        shake_amplitude=shake.amplitude, shake_ok=shake_ok,
        follow_x=fe[0], follow_ok=follow_ok,
        ok=orbit_ok and path_ok and shake_ok and follow_ok,
    )
