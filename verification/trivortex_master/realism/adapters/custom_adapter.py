#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — пользовательский движок: произвольные силы.

Пользователь задаёт ускорение как функцию состояния в песочнице:
компилируется в изолированном пространстве имён, где доступны только
math и параметры (без импортов, без open/exec/eval/__) — безопасность
по построению.

    from realism.adapters.custom_adapter import CustomEngine
    eng = CustomEngine(scene, force_expr="-0.1*vx")
    eng.step(dt)
"""
from __future__ import annotations

import math
from typing import Any

from lab.engine_base import BodyState, PhysicsEngine

# что доступно пользовательскому выражению
SANDBOX_GLOBALS = {
    name: getattr(math, name)
    for name in ("sin", "cos", "tan", "asin", "acos", "atan", "atan2",
                 "sinh", "cosh", "tanh", "exp", "log", "log10", "log2",
                 "sqrt", "pow", "hypot", "floor", "ceil", "fabs",
                 "pi", "e", "tau", "degrees", "radians", "fmod", "copysign",
                 "isfinite", "isnan")
}
SANDBOX_GLOBALS["abs"] = abs
SANDBOX_GLOBALS["min"] = min
SANDBOX_GLOBALS["max"] = max

# запрещённые токены в исходнике выражения
_FORBIDDEN = ("import", "open(", "exec", "eval", "__", "lambda",
              "globals", "locals", "compile", "getattr", "setattr",
              "delattr", "input", "yield", "await", "async")


def compile_force(force_expr: str):
    """Скомпилировать выражение ускорения ax, ay, az (или словарь)."""
    if not force_expr or not force_expr.strip():
        raise ValueError("пустое выражение силы")
    for token in _FORBIDDEN:
        if token in force_expr:
            raise ValueError(f"запрещённый токен в выражении силы: {token!r}")
    try:
        code = compile(force_expr, "<force_expr>", "eval")
    except SyntaxError as exc:
        raise ValueError(f"синтаксическая ошибка в выражении: {exc}") from exc
    # проверка допустимых имён
    allowed = set(SANDBOX_GLOBALS) | {"x", "y", "z", "vx", "vy", "vz",
                                      "t", "m", "q", "G", "r"}
    for name in code.co_names:
        if name not in allowed:
            raise ValueError(f"имя {name!r} недоступно в песочнице; "
                             f"разрешены: {sorted(allowed)}")
    return code


class CustomEngine(PhysicsEngine):
    """Ньютоновская гравитация + пользовательское ускорение.

    force_expr — выражение Python (возвращается ускорение по x; для
    векторного варианта задайте dict {"ax": ..., "ay": ..., "az": ...}).
    """

    def __init__(self, scene, force_expr: str = "0.0"):
        super().__init__(scene)
        if isinstance(force_expr, dict):
            self._codes = {axis: compile_force(expr)
                           for axis, expr in force_expr.items()}
        else:
            self._codes = {"ax": compile_force(force_expr),
                           "ay": compile_force("0.0"),
                           "az": compile_force("0.0")}
        self._expr_src = force_expr

    def name(self) -> str:
        return "custom"

    def _user_accel(self, body, t: float) -> tuple[float, float, float]:
        env = dict(SANDBOX_GLOBALS)
        env.update(x=body.position[0], y=body.position[1],
                   z=body.position[2],
                   vx=body.velocity[0], vy=body.velocity[1],
                   vz=body.velocity[2],
                   t=t, m=body.mass, q=body.charge, G=self.cfg.G,
                   r=math.sqrt(sum(c * c for c in body.position)) or 1e-12)
        out = []
        for axis in ("ax", "ay", "az"):
            code = self._codes.get(axis)
            if code is None:
                out.append(0.0)
                continue
            try:
                out.append(float(eval(code, {"__builtins__": {}}, env)))
            except Exception as exc:
                raise ValueError(f"ошибка вычисления {axis}: {exc}") from exc
        return tuple(out)

    def _grav_accel(self) -> list[tuple[float, float, float]]:
        bodies = self.scene.bodies
        n = len(bodies)
        G = self.cfg.G
        eps2 = self.cfg.softening ** 2
        acc = []
        for i in range(n):
            ax = ay = az = 0.0
            for j in range(n):
                if i == j:
                    continue
                dx = bodies[j].position[0] - bodies[i].position[0]
                dy = bodies[j].position[1] - bodies[i].position[1]
                dz = bodies[j].position[2] - bodies[i].position[2]
                r2 = dx * dx + dy * dy + dz * dz + eps2
                r = math.sqrt(r2)
                f = G * bodies[j].mass / (r2 * r)
                ax += f * dx
                ay += f * dy
                az += f * dz
            acc.append((ax, ay, az))
        return acc

    def step(self, dt: float) -> None:
        bodies = self.scene.bodies
        if not bodies:
            return
        t = self.scene.t
        grav = self._grav_accel()
        user = [self._user_accel(b, t) for b in bodies]
        # полунеявный Эйлер (просто и устойчиво для демо-сил)
        for b, g, u in zip(bodies, grav, user):
            ax, ay, az = g[0] + u[0], g[1] + u[1], g[2] + u[2]
            vx = b.velocity[0] + ax * dt
            vy = b.velocity[1] + ay * dt
            vz = b.velocity[2] + az * dt
            b.velocity = (vx, vy, vz)
            b.position = (b.position[0] + vx * dt,
                          b.position[1] + vy * dt,
                          b.position[2] + vz * dt)
        self.scene.t += dt

    def get_states(self) -> list[BodyState]:
        return [BodyState(b.id, b.position, b.velocity)
                for b in self.scene.bodies]

    def energy(self) -> float:
        return self.scene.total_energy()

    def to_dict(self) -> dict[str, Any]:
        return dict(engine="custom", force_expr=str(self._expr_src)[:500],
                    sandbox="math-only, без импортов")
