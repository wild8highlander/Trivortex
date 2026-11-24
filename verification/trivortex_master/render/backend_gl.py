#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — опциональный GL-бэкенд (pyrender / moderngl).

Подключается при наличии; иначе движок render.engine предлагает
mpl / pure / ascii. GL даёт аппаратное ускорение и тени, но не является
обязательным: лаборатория полностью работает и без него.
"""

from __future__ import annotations

import math

from importlib.util import find_spec

# availability probes: bind booleans, not module objects
HAVE_MODERNGL = find_spec("moderngl") is not None
HAVE_PYRENDER = find_spec("pyrender") is not None

HAVE_GL = HAVE_MODERNGL or HAVE_PYRENDER


def availability() -> dict:
    """Статус для HUD."""
    reasons = []
    if not HAVE_MODERNGL:
        reasons.append("pip install moderngl")
    if not HAVE_PYRENDER:
        reasons.append("pip install pyrender")
    return dict(name="gl", available=HAVE_GL, reason="" if HAVE_GL else "; ".join(reasons))


# ── шейдеры для moderngl (минимальный Lambert) ──
_VERTEX = """
#version 330
in vec3 in_position;
in vec3 in_normal;
uniform mat4 mvp;
uniform mat4 model;
out vec3 v_normal;
out vec3 v_pos;
void main() {
    gl_Position = mvp * vec4(in_position, 1.0);
    v_normal = mat3(model) * in_normal;
    v_pos = (model * vec4(in_position, 1.0)).xyz;
}
"""

_FRAGMENT = """
#version 330
in vec3 v_normal;
in vec3 v_pos;
uniform vec3 u_color;
uniform vec3 u_light;
out vec4 frag;
void main() {
    vec3 n = normalize(v_normal);
    float diff = max(dot(n, normalize(u_light - v_pos)), 0.0);
    float amb = 0.3;
    vec3 col = u_color * (amb + 0.7 * diff);
    frag = vec4(col, 1.0);
}
"""


def sphere_mesh(radius: float, seg: int = 24, rings: int = 16) -> tuple[list[float], list[int]]:
    """Вершины (x,y,z,nx,ny,nz) и индексы UV-сферы для GL."""
    verts: list[float] = []
    for r in range(rings + 1):
        phi = math.pi * r / rings
        for s in range(seg):
            theta = 2 * math.pi * s / seg
            x = radius * math.sin(phi) * math.cos(theta)
            y = radius * math.cos(phi)
            z = radius * math.sin(phi) * math.sin(theta)
            nx, ny, nz = x / radius, y / radius, z / radius
            verts.extend([x, y, z, nx, ny, nz])
    idx: list[int] = []
    for r in range(rings):
        for s in range(seg):
            a = r * seg + s
            b = r * seg + (s + 1) % seg
            c = (r + 1) * seg + s
            d = (r + 1) * seg + (s + 1) % seg
            if r != 0:
                idx.extend([a, b, d])
            if r != rings - 1:
                idx.extend([a, d, c])
    return verts, idx


def render_gl(
    bodies: list[dict],
    width: int = 640,
    height: int = 480,
    output: str = "frame_gl.png",
    bg: tuple[float, float, float] = (0.05, 0.09, 0.16),
) -> str:
    """Рендер сфер через moderngl (offscreen) → PNG (через собственный кодер).

    bodies: [{position, radius, color:'#rrggbb'}]
    """
    if not HAVE_MODERNGL:
        raise ImportError("moderngl не установлен: " + availability()["reason"])
    import moderngl
    import numpy as np
    from render.pure_raster import (
        mat_look_at,
        mat_perspective,
        mat_mul,
        mat_translate,
        mat_scale,
    )

    ctx = moderngl.create_context(standalone=True, backend="egl")  # offscreen без X-сервера
    prog = ctx.program(vertex_shader=_VERTEX, fragment_shader=_FRAGMENT)
    fbo = ctx.simple_framebuffer((width, height))
    fbo.use()
    fbo.clear(*bg)

    if bodies:
        max_r = max(max(abs(c) for c in b["position"]) for b in bodies) or 1.0
    else:
        max_r = 1.0
    half = math.radians(50.0) / 2
    d = (max_r / max(math.sin(half), 1e-3)) * 1.35
    eye = (d * 0.55, d * 0.4, d * 0.75)
    el = math.sqrt(sum(c * c for c in eye)) or 1.0
    eye = tuple(c * d / el for c in eye)
    view = mat_look_at(eye, (0, 0, 0), (0, 1, 0))
    proj = mat_perspective(50.0, width / height, 0.05, 100.0)
    vp = mat_mul(proj, view)

    light = np.array([eye[0], eye[1] + max_r, eye[2]], dtype="f4")

    for b in bodies:
        verts, idx = sphere_mesh(b["radius"])
        vbo = ctx.buffer(np.array(verts, dtype="f4").tobytes())
        ibo = ctx.buffer(np.array(idx, dtype="i4").tobytes())
        vao = ctx.vertex_array(prog, [(vbo, "3f 3f", "in_position", "in_normal")], ibo)
        model = mat_mul(mat_translate(*b["position"]), mat_scale(1.0, 1.0, 1.0))
        mvp = mat_mul(vp, model)
        mvp_np = np.array(mvp, dtype="f4").T.tobytes()
        model_np = np.array(model, dtype="f4").T.tobytes()
        h = b.get("color", "#4fd1c5").lstrip("#")
        color = (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255)
        prog["mvp"].write(mvp_np)
        prog["model"].write(model_np)
        prog["u_color"].value = tuple(color)
        prog["u_light"].write(light.tobytes())
        vao.render(moderngl.TRIANGLES)

    # читаем пиксели и пишем PNG собственным кодером
    raw = fbo.read(components=3, alignment=1)
    # GL читает снизу вверх — переворачиваем строки
    row = width * 3
    flipped = bytearray()
    for y in range(height - 1, -1, -1):
        flipped += raw[y * row : (y + 1) * row]
    from render.png_codec import write_png

    write_png(output, flipped, width, height)
    return output
