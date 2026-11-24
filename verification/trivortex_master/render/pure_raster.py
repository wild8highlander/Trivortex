#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — собственный программный растеризатор на stdlib.

Никаких numpy/PIL/OpenGL: только Python и байты.

Конвейер:
  1. Матрицы 4×4 (умножение, транспонирование, модель–вид–проекция);
  2. Сетки: UV-сфера (сегменты×кольца) и icosphere-подобная аппроксимация;
  3. Бэкул-фейс culling + нормали по вершинам;
  4. Освещение: Ламберт + ambient (+ опц. спекуляр Блинна-Фонга);
  5. Scanline-растеризация треугольников с z-буфером и интерполяцией цвета;
  6. Линии Брезенхэма (орбиты, оси, сетка);
  7. Вывод: PNG (собственный кодер) и PPM.

Производительность: кадр 320×240 с 3–8 сферами ~0,5–2 с — осознанный
выбор в пользу полного отсутствия зависимостей ( mpl включён опционально).
"""

from __future__ import annotations

import math

from render.png_codec import write_png, write_ppm

# ═══════════════════════════════════════════════════════════════════════════
# 1. Матрицы 4×4 (row-major)
# ═══════════════════════════════════════════════════════════════════════════
Mat4 = list[list[float]]
Vec3 = tuple[float, float, float]
Vec4 = tuple[float, float, float, float]


def mat_identity() -> Mat4:
    """Handle mat identity."""
    return [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]


def mat_mul(a: Mat4, b: Mat4) -> Mat4:
    """Do mat mul for a, b and return the result."""
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def mat_translate(tx: float, ty: float, tz: float) -> Mat4:
    """Do mat translate for tx, ty, tz and return the result."""
    m = mat_identity()
    m[0][3], m[1][3], m[2][3] = tx, ty, tz
    return m


def mat_scale(sx: float, sy: float, sz: float) -> Mat4:
    """Do mat scale for sx, sy, sz and return the result."""
    m = mat_identity()
    m[0][0], m[1][1], m[2][2] = sx, sy, sz
    return m


def mat_rotate_x(deg: float) -> Mat4:
    """Do mat rotate x for deg and return the result."""
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return [[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]]


def mat_rotate_y(deg: float) -> Mat4:
    """Do mat rotate y for deg and return the result."""
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return [[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]]


def mat_rotate_z(deg: float) -> Mat4:
    """Do mat rotate z for deg and return the result."""
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return [[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]


def mat_look_at(eye: Vec3, target: Vec3, up: Vec3) -> Mat4:
    """Видовая матрица (правосторонняя, смотрим вдоль -z)."""
    ex, ey, ez = eye
    cx, cy, cz = target
    fx, fy, fz = cx - ex, cy - ey, cz - ez
    fl = math.sqrt(fx * fx + fy * fy + fz * fz) or 1.0
    fx, fy, fz = fx / fl, fy / fl, fz / fl
    # right = forward × up
    ux, uy, uz = up
    rx = fy * uz - fz * uy
    ry = fz * ux - fx * uz
    rz = fx * uy - fy * ux
    rl = math.sqrt(rx * rx + ry * ry + rz * rz) or 1.0
    rx, ry, rz = rx / rl, ry / rl, rz / rl
    # up' = right × forward
    ux2 = ry * fz - rz * fy
    uy2 = rz * fx - rx * fz
    uz2 = rx * fy - ry * fx
    return [
        [rx, ry, rz, -(rx * ex + ry * ey + rz * ez)],
        [ux2, uy2, uz2, -(ux2 * ex + uy2 * ey + uz2 * ez)],
        [-fx, -fy, -fz, (fx * ex + fy * ey + fz * ez)],
        [0, 0, 0, 1],
    ]


def mat_perspective(fov_y_deg: float, aspect: float, near: float, far: float) -> Mat4:
    """Перспективная проекция (OpenGL-стиль, z в [-1,1])."""
    f = 1.0 / math.tan(math.radians(fov_y_deg) / 2.0)
    nf = 1.0 / (near - far)
    return [
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) * nf, 2 * far * near * nf],
        [0, 0, -1, 0],
    ]


def mat_apply(m: Mat4, v: Vec4) -> Vec4:
    """Do mat apply for m, v and return the result."""
    return tuple(
        m[i][0] * v[0] + m[i][1] * v[1] + m[i][2] * v[2] + m[i][3] * v[3] for i in range(4)
    )  # type: ignore


# ═══════════════════════════════════════════════════════════════════════════
# 2. Геометрия: UV-сфера
# ═══════════════════════════════════════════════════════════════════════════
def uv_sphere(
    radius: float, seg: int = 12, rings: int = 8
) -> tuple[list[Vec3], list[tuple[int, int, int]]]:
    """Вершины и треугольники UV-сферы (полюса по y)."""
    verts: list[Vec3] = []
    for r in range(rings + 1):
        phi = math.pi * r / rings
        for s in range(seg):
            theta = 2 * math.pi * s / seg
            x = radius * math.sin(phi) * math.cos(theta)
            y = radius * math.cos(phi)
            z = radius * math.sin(phi) * math.sin(theta)
            verts.append((x, y, z))
    tris: list[tuple[int, int, int]] = []
    for r in range(rings):
        for s in range(seg):
            a = r * seg + s
            b = r * seg + (s + 1) % seg
            c = (r + 1) * seg + s
            d = (r + 1) * seg + (s + 1) % seg
            if r != 0:
                tris.append((a, b, d))
            if r != rings - 1:
                tris.append((a, d, c))
    return verts, tris


# ═══════════════════════════════════════════════════════════════════════════
# 3. Кадр: z-буфер + попиксельная запись
# ═══════════════════════════════════════════════════════════════════════════
def _hex_to_rgb(color: str) -> tuple[int, int, int]:
    """Do hex to rgb for color and return the result."""
    h = color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


class Frame:
    """RGB-кадр с z-буфером."""

    def __init__(self, width: int, height: int, bg: tuple[int, int, int] = (13, 22, 40)):
        """Do Frame.  init for width, height, bg and return the result."""
        self.w = width
        self.h = height
        self.bg = bg
        self.pixels = bytearray(bytes(bg) * (width * height))
        self.zbuf = [float("inf")] * (width * height)

    def clear(self) -> None:
        """Handle Frame.clear."""
        self.pixels = bytearray(bytes(self.bg) * (self.w * self.h))
        self.zbuf = [float("inf")] * (self.w * self.h)

    def set_pixel(self, x: int, y: int, z: float, color: tuple[int, int, int]) -> None:
        """Do Frame.set pixel for x, y, z, color and return the result."""
        if 0 <= x < self.w and 0 <= y < self.h:
            idx = y * self.w + x
            if z < self.zbuf[idx]:
                self.zbuf[idx] = z
                o = idx * 3
                self.pixels[o] = color[0]
                self.pixels[o + 1] = color[1]
                self.pixels[o + 2] = color[2]

    def draw_line(
        self, x0: int, y0: int, x1: int, y1: int, color: tuple[int, int, int], z: float = 0.0
    ) -> None:
        """Линия Брезенхэма."""
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        x, y = x0, y0
        while True:
            self.set_pixel(x, y, z, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    # ── освещение ──
    def shade(
        self,
        normal: Vec3,
        base: tuple[int, int, int],
        light_dir: Vec3,
        ambient: float = 0.25,
        specular: float = 0.0,
        view_dir: Vec3 = (0.0, 0.0, 1.0),
    ) -> tuple[int, int, int]:
        """Ламберт + ambient (+ Блинн-Фонг опционально)."""
        nl = normal[0] * light_dir[0] + normal[1] * light_dir[1] + normal[2] * light_dir[2]
        nl = max(0.0, min(1.0, nl))
        # свет «сверху-спереди», если направленный не задан явно
        intensity = ambient + (1.0 - ambient) * nl
        if specular > 0 and nl > 0:
            # half-vector
            hx = light_dir[0] + view_dir[0]
            hy = light_dir[1] + view_dir[1]
            hz = light_dir[2] + view_dir[2]
            hl = math.sqrt(hx * hx + hy * hy + hz * hz) or 1.0
            nh = normal[0] * hx / hl + normal[1] * hy / hl + normal[2] * hz / hl
            nh = max(0.0, nh)
            intensity += specular * (nh**32)
        intensity = min(1.0, intensity)
        return (int(base[0] * intensity), int(base[1] * intensity), int(base[2] * intensity))

    # ── треугольник: scanline с z-интерполяцией ──
    def draw_triangle(
        self,
        p0: tuple[float, float, float],
        p1: tuple[float, float, float],
        p2: tuple[float, float, float],
        c0: tuple[int, int, int],
        c1: tuple[int, int, int],
        c2: tuple[int, int, int],
    ) -> None:
        """Вершины в экранных координатах (x, y, z-глубина)."""
        # сортировка по y
        pts = sorted([p0, p1, p2], key=lambda p: p[1])
        (xa, ya, za), (xb, yb, zb), (xc, yc, zc) = pts
        ca, cb, cc = c0, c1, c2
        # сопоставление цветов после сортировки
        order = sorted([(p0, c0), (p1, c1), (p2, c2)], key=lambda t: t[0][1])
        ca, cb, cc = order[0][1], order[1][1], order[2][1]

        if yc - ya < 1e-9:
            # вырожденный: весь на одной строке
            for x, z, c in self._span(ya, xa, za, ca, xc, zc, cc):
                self.set_pixel(int(x), int(ya), z, c)
            return

        def lerp(a, b, t):
            return a + (b - a) * t

        y_start = max(0, int(math.ceil(ya)))
        y_end = min(self.h - 1, int(math.floor(yc)))

        for y in range(y_start, y_end + 1):
            # длинная сторона a→c
            t_long = (y - ya) / (yc - ya)
            xl, zl = lerp(xa, xc, t_long), lerp(za, zc, t_long)
            cl = tuple(int(lerp(ca[k], cc[k], t_long)) for k in range(3))
            # короткая: a→b или b→c
            if y < yb and yb - ya > 1e-9:
                t = (y - ya) / (yb - ya)
                xs, zs = lerp(xa, xb, t), lerp(za, zb, t)
                cs = tuple(int(lerp(ca[k], cb[k], t)) for k in range(3))
            elif yc - yb > 1e-9:
                t = (y - yb) / (yc - yb)
                xs, zs = lerp(xb, xc, t), lerp(zb, zc, t)
                cs = tuple(int(lerp(cb[k], cc[k], t)) for k in range(3))
            else:
                continue
            x_left, x_right = (xl, xs) if xl <= xs else (xs, xl)
            z_left, z_right = (zl, zs) if xl <= xs else (zs, zl)
            c_left, c_right = (cl, cs) if xl <= xs else (cs, cl)
            if x_right - x_left < 1e-9:
                self.set_pixel(int(x_left), y, z_left, c_left)
                continue
            x_i = max(0, int(math.ceil(x_left)))
            x_f = min(self.w - 1, int(math.floor(x_right)))
            for x in range(x_i, x_f + 1):
                t = (x - x_left) / (x_right - x_left)
                z = z_left + (z_right - z_left) * t
                c = (
                    int(c_left[0] + (c_right[0] - c_left[0]) * t),
                    int(c_left[1] + (c_right[1] - c_left[1]) * t),
                    int(c_left[2] + (c_right[2] - c_left[2]) * t),
                )
                self.set_pixel(x, y, z, c)

    def _span(self, y, xa, za, ca, xb, zb, cb):
        """Do Frame. span for y, xa, za, ca and return the result."""
        if abs(xb - xa) < 1e-9:
            yield xa, za, ca
            return
        x0, x1 = (xa, xb) if xa < xb else (xb, xa)
        z0, z1 = (za, zb) if xa < xb else (zb, za)
        c0, c1 = (ca, cb) if xa < xb else (cb, ca)
        for x in range(int(math.ceil(x0)), int(math.floor(x1)) + 1):
            t = (x - x0) / (x1 - x0)
            yield x, z0 + (z1 - z0) * t, c0

    # ── сохранение ──
    def save_png(self, path: str) -> int:
        """Do Frame.save png for path and return the result."""
        return write_png(path, self.pixels, self.w, self.h)

    def save_ppm(self, path: str) -> int:
        """Do Frame.save ppm for path and return the result."""
        return write_ppm(path, self.pixels, self.w, self.h)


# ═══════════════════════════════════════════════════════════════════════════
# 4. Рендер сцены тел: сферы + трейлы + подсветка
# ═══════════════════════════════════════════════════════════════════════════
def render_bodies(
    bodies_state: list[dict],
    width: int = 320,
    height: int = 240,
    trails: list[list[Vec3]] | None = None,
    eye: Vec3 | None = None,
    target: Vec3 = (0.0, 0.0, 0.0),
    fov: float = 50.0,
    seg: int = 10,
    rings: int = 6,
    bg: tuple[int, int, int] = (13, 22, 40),
    show_axes: bool = True,
    title: str = "",
) -> Frame:
    """
    bodies_state: [{position: (x,y,z), radius: float, color: '#rrggbb',
                    label: str, glow: bool}]
    trails: список трейлов (list[(x,y,z)]) по телам — рисуются линиями.
    """
    frame = Frame(width, height, bg=bg)

    # авто-габарит сцены
    if bodies_state:
        max_r = max(max(abs(c) for c in b["position"]) for b in bodies_state) or 1.0
    else:
        max_r = 1.0
    scale = 2.2 / max_r
    # авто-камера: дистанция так, чтобы вся сцена (радиус max_r) влезала
    # в конус fov: d >= max_r / sin(fov/2), с запасом ×1.35
    if eye is None:
        half = math.radians(fov) / 2.0
        need = max_r / max(math.sin(half), 1e-3)
        d = need * 1.35
        eye = (d * 0.55, d * 0.4, d * 0.75)
        # нормировать до длины d
        el = math.sqrt(sum(c * c for c in eye)) or 1.0
        eye = tuple(c * d / el for c in eye)

    view = mat_look_at(eye, target, (0.0, 1.0, 0.0))
    proj = mat_perspective(fov, width / height, 0.05, 100.0)

    def to_screen(p: Vec3) -> tuple[float, float, float] | None:
        v = mat_apply(proj, mat_apply(view, (*p, 1.0)))
        if v[3] <= 1e-9:
            return None
        sx = (v[0] / v[3] * 0.5 + 0.5) * width
        sy = (1.0 - (v[1] / v[3] * 0.5 + 0.5)) * height
        return (sx, sy, v[3])

    light_dir = (0.4, 0.7, 0.6)
    ll = math.sqrt(sum(c * c for c in light_dir))
    light_dir = tuple(c / ll for c in light_dir)

    # оси
    if show_axes:
        origin = to_screen((0.0, 0.0, 0.0))
        if origin:
            for axis, color, vec in (
                ("x", (120, 60, 60), (0.8 / scale, 0, 0)),
                ("y", (60, 120, 60), (0, 0.8 / scale, 0)),
                ("z", (60, 60, 120), (0, 0, 0.8 / scale)),
            ):
                tip = to_screen(vec)
                if tip:
                    frame.draw_line(
                        int(origin[0]), int(origin[1]), int(tip[0]), int(tip[1]), color, z=-1e-6
                    )

    # трейлы
    if trails:
        for trail in trails:
            if len(trail) < 2:
                continue
            prev = to_screen(trail[0])
            for p in trail[1:]:
                cur = to_screen(p)
                if prev and cur:
                    frame.draw_line(
                        int(prev[0]),
                        int(prev[1]),
                        int(cur[0]),
                        int(cur[1]),
                        (90, 120, 160),
                        z=-1e-6,
                    )
                prev = cur

    # сферы (от дальних к ближним — сортировка по глубине вида)
    order = sorted(bodies_state, key=lambda b: -math.dist(eye, b["position"]))  # type: ignore
    verts, tris = uv_sphere(1.0, seg=seg, rings=rings)
    for b in order:
        pos: Vec3 = b["position"]
        r_screen = max(b["radius"] * scale, 0.02)
        base = _hex_to_rgb(b.get("color", "#4fd1c5"))
        model = mat_mul(mat_translate(*pos), mat_scale(r_screen, r_screen, r_screen))
        mv = mat_mul(view, model)
        # экранные вершины
        scr = []
        for v in verts:
            clip = mat_apply(proj, mat_apply(mv, (*v, 1.0)))
            if clip[3] <= 1e-9:
                scr = []
                break
            scr.append(
                (
                    (clip[0] / clip[3] * 0.5 + 0.5) * width,
                    (1.0 - (clip[1] / clip[3] * 0.5 + 0.5)) * height,
                    clip[3],
                )
            )
        if not scr:
            continue
        for i0, i1, i2 in tris:
            # бэкул-фейс culling в экранных координатах
            ax, ay = scr[i0][0], scr[i0][1]
            bx, by = scr[i1][0], scr[i1][1]
            cx, cy = scr[i2][0], scr[i2][1]
            if (bx - ax) * (cy - ay) - (cx - ax) * (by - ay) >= 0:
                continue
            # нормаль из модельных вершин (сфера — нормаль = вершина)
            # интерполируем цвет по вершинам через освещение
            colors = []
            for idx in (i0, i1, i2):
                n = verts[idx]
                colors.append(frame.shade(n, base, light_dir, ambient=0.3, specular=0.25))
            frame.draw_triangle(scr[i0], scr[i1], scr[i2], colors[0], colors[1], colors[2])

    return frame
