#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — динамика космического аппарата: ориентация, маховики.

Модель малых угловых движений жёсткого КА с электроприводами:

  * Quaternion — единичная кватернионная ориентация (гамильтоново
    умножение, поворот вектора, из оси-угла; норма сохраняется);
  * PIDController — ПИД-регулятор ориентации с анти-виндапом
    (ограничение интеграла);
  * ReactionWheel / ReactionWheelArray — маховики: обмен моментом
    между корпусом и колесами (суммарный H сохраняется при нулевом
    внешнем моменте);
  * Spacecraft — тензор инерции (диагональ), угловая скорость,
    уравнения Эйлера жёсткого тела с внутренними колесами;
  * AttitudePropagator — интегрирование кватернионной кинематики
    ω̇ из уравнений Эйлера (RK4, нормировка кватерниона на шаге).

Контроль: 90° разворот rest-to-rest по одной оси сходится ПИДом;
|H_total| без внешних моментов сохраняется до численной точности.

Ссылки: Wertz, «Spacecraft Attitude Determination and Control»,
§16; Sidi, «Spacecraft Dynamics and Control», гл. 4.
"""

from __future__ import annotations

import math
from typing import Sequence


# ═══════════════════════════════════════════════════════════════════════════
# Кватернион
# ═══════════════════════════════════════════════════════════════════════════
class Quaternion:
    """Единичный кватернион ориентации (w, x, y, z)."""

    __slots__ = ("w", "x", "y", "z")

    def __init__(self, w: float = 1.0, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        """Do Quaternion.  init for w, x, y, z and return the result."""
        self.w, self.x, self.y, self.z = w, x, y, z
        self.normalize()

    # ── алгебра ──
    def __mul__(self, other: Quaternion) -> Quaternion:
        """Do Quaternion.  mul for other and return the result."""
        w1, x1, y1, z1 = self.w, self.x, self.y, self.z
        w2, x2, y2, z2 = other.w, other.x, other.y, other.z
        return Quaternion(
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
        )

    def conjugate(self) -> Quaternion:
        """Handle Quaternion.conjugate."""
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def norm(self) -> float:
        """Handle Quaternion.norm."""
        return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)

    def normalize(self) -> None:
        """Handle Quaternion.normalize."""
        n = self.norm()
        if n < 1e-18:
            self.w, self.x, self.y, self.z = 1.0, 0.0, 0.0, 0.0
            return
        self.w /= n
        self.x /= n
        self.y /= n
        self.z /= n

    # ── геометрия ──
    @classmethod
    def from_axis_angle(cls, axis: Sequence[float], angle_rad: float) -> Quaternion:
        """Do Quaternion.from axis angle for axis, angle_rad and return the result."""
        n = math.sqrt(sum(c * c for c in axis)) or 1.0
        s = math.sin(angle_rad / 2.0)
        return cls(math.cos(angle_rad / 2.0), s * axis[0] / n, s * axis[1] / n, s * axis[2] / n)

    def rotate(self, v: Sequence[float]) -> tuple[float, float, float]:
        """Повернуть вектор: v' = q ⊗ v ⊗ q*."""
        qv = Quaternion(0.0, v[0], v[1], v[2])
        qr = self * qv * self.conjugate()
        return (qr.x, qr.y, qr.z)

    def angle_to(self, other: Quaternion) -> float:
        """Угловое расстояние между ориентациями (рад)."""
        dot = abs(self.w * other.w + self.x * other.x + self.y * other.y + self.z * other.z)
        return 2.0 * math.acos(max(-1.0, min(1.0, dot)))

    def to_dict(self) -> dict:
        """Handle Quaternion.to dict."""
        return dict(w=self.w, x=self.x, y=self.y, z=self.z)


# ═══════════════════════════════════════════════════════════════════════════
# Регуляторы
# ═══════════════════════════════════════════════════════════════════════════
class PIDController:
    """ПИД с анти-виндапом (clamping интегральной части)."""

    def __init__(
        self,
        kp: float,
        ki: float = 0.0,
        kd: float = 0.0,
        i_limit: float = 1.0,
        out_limit: float | None = None,
    ):
        """Do PIDController.  init for kp, ki, kd, i_limit and return the result."""
        self.kp, self.ki, self.kd = kp, ki, kd
        self.i_limit = i_limit
        self.out_limit = out_limit
        self._integral = 0.0
        self._prev_error: float | None = None

    def update(self, error: float, dt: float) -> float:
        """Do PIDController.update for error, dt and return the result."""
        self._integral += error * dt
        # анти-виндап: интеграл не выходит за предел
        self._integral = max(-self.i_limit, min(self.i_limit, self._integral))
        d = 0.0 if self._prev_error is None else (error - self._prev_error) / max(dt, 1e-12)
        self._prev_error = error
        out = self.kp * error + self.ki * self._integral + self.kd * d
        if self.out_limit is not None:
            out = max(-self.out_limit, min(self.out_limit, out))
        return out

    def reset(self) -> None:
        """Handle PIDController.reset."""
        self._integral = 0.0
        self._prev_error = None


# ═══════════════════════════════════════════════════════════════════════════
# Исполнительные органы
# ═══════════════════════════════════════════════════════════════════════════
class ReactionWheel:
    """Маховик: ось (в СК корпуса), макс. момент, макс. кинет. момент."""

    def __init__(self, axis: Sequence[float], max_torque: float = 0.05, max_momentum: float = 1.0):
        """Do ReactionWheel.  init for axis, max_torque, max_momentum and return the result."""
        n = math.sqrt(sum(c * c for c in axis)) or 1.0
        self.axis = tuple(c / n for c in axis)
        self.max_torque = max_torque
        self.max_momentum = max_momentum
        self.momentum = 0.0  # кинетический момент колеса

    def apply_torque(self, torque_body: float, dt: float) -> float:
        """Запросить момент вдоль оси; вернуть фактический."""
        t = max(-self.max_torque, min(self.max_torque, torque_body))
        new_momentum = self.momentum + t * dt
        if abs(new_momentum) > self.max_momentum:
            # насыщение колеса: момент физически не может поддерживаться
            new_momentum = math.copysign(self.max_momentum, new_momentum)
            t = (new_momentum - self.momentum) / max(dt, 1e-12)
        self.momentum = new_momentum
        return t


class ReactionWheelArray:
    """Набор маховиков: распределение 3-осевого запроса по осям колёс."""

    def __init__(self, wheels: list[ReactionWheel]):
        """Do ReactionWheelArray.  init for wheels and return the result."""
        if not wheels:
            raise ValueError("нужен хотя бы один маховик")
        self.wheels = wheels

    def apply_torque(self, torque_body: Sequence[float], dt: float) -> tuple[float, float, float]:
        """Спроецировать запрос на оси колёс (псевдоинверсия 3×N)."""
        # для ортогональной тройки — простое скалярное произведение
        applied = [0.0, 0.0, 0.0]
        for wheel in self.wheels:
            request = sum(t * a for t, a in zip(torque_body, wheel.axis))
            granted = wheel.apply_torque(request, dt)
            for i in range(3):
                applied[i] += granted * wheel.axis[i]
        return tuple(applied)

    def total_momentum(self) -> tuple[float, float, float]:
        """Handle ReactionWheelArray.total momentum."""
        return tuple(
            sum(w.momentum * a for w in self.wheels for a in [w.axis[i]]) for i in range(3)
        )

    def saturation_fraction(self) -> float:
        """Handle ReactionWheelArray.saturation fraction."""
        return max(abs(w.momentum) / w.max_momentum for w in self.wheels)


# ═══════════════════════════════════════════════════════════════════════════
# Космический аппарат
# ═══════════════════════════════════════════════════════════════════════════
class Spacecraft:
    """Жёсткий КА: инерции (диагональ), кватернион, ω, маховики."""

    def __init__(
        self,
        inertia_diag: Sequence[float],
        wheels: ReactionWheelArray,
        q0: Quaternion | None = None,
        omega: Sequence[float] = (0.0, 0.0, 0.0),
    ):
        """Do Spacecraft.  init for inertia_diag, wheels, q0, omega and return the result."""
        if len(inertia_diag) != 3 or min(inertia_diag) <= 0:
            raise ValueError("инерции: три положительных числа")
        self.I = tuple(inertia_diag)
        self.wheels = wheels
        self.q = q0 if q0 is not None else Quaternion()
        self.omega = list(omega)

    def angular_momentum_total(self) -> tuple[float, float, float]:
        """H корпуса + H колёс (сохраняется без внешних моментов)."""
        h_body = tuple(self.I[i] * self.omega[i] for i in range(3))
        h_wheels = self.wheels.total_momentum()
        return tuple(h_body[i] + h_wheels[i] for i in range(3))

    def derivatives(
        self,
        state: Sequence[float],
        ext_torque: Sequence[float],
        wheel_torque: Sequence[float] = (0.0, 0.0, 0.0),
    ) -> list[float]:
        """Правая часть: [ω̇, q̇] из уравнений Эйлера + кинематики.

        ext_torque — внешний момент (гравитационный и т.п.);
        wheel_torque — момент, переданный корпусу колёсами
        (реакция: колесо раскручивается на −wheel_torque).
        """
        wx, wy, wz = state[0], state[1], state[2]
        Ix, Iy, Iz = self.I
        # уравнения Эйлера (диагональный тензор)
        dwx = (ext_torque[0] + wheel_torque[0] + (Iy - Iz) * wy * wz) / Ix
        dwy = (ext_torque[1] + wheel_torque[1] + (Iz - Ix) * wz * wx) / Iy
        dwz = (ext_torque[2] + wheel_torque[2] + (Ix - Iy) * wx * wy) / Iz
        # кинематика кватерниона: q̇ = ½ q ⊗ (0, ω)
        wq = Quaternion(0.0, wx, wy, wz)
        q = Quaternion(*state[3:7])
        dq = q * wq
        return [dwx, dwy, dwz, 0.5 * dq.w, 0.5 * dq.x, 0.5 * dq.y, 0.5 * dq.z]


class AttitudePropagator:
    """Интегратор ориентации: RK4 по (ω, q) с перенормировкой q.

    Колёса непрерывно участвуют: их момент реакции входит в уравнения
    Эйлера на каждом подшаге RK4 (через callback колесного момента).
    """

    def __init__(self, sc: Spacecraft, dt: float = 0.05, wheel_torque_fn=None):
        """Do AttitudePropagator.  init for sc, dt, wheel_torque_fn and return the result."""
        self.sc = sc
        self.dt = dt
        # постоянный момент колёс на шаг (обновляет slew-контроллер)
        self.wheel_torque: list[float] = [0.0, 0.0, 0.0]
        self.wheel_torque_fn = wheel_torque_fn

    def step(self, ext_torque: Sequence[float] = (0.0, 0.0, 0.0)) -> None:
        """Do AttitudePropagator.step for ext_torque and return the result."""
        sc = self.sc
        if self.wheel_torque_fn is not None:
            self.wheel_torque = list(self.wheel_torque_fn())
        wt = tuple(self.wheel_torque)
        state = list(sc.omega) + [sc.q.w, sc.q.x, sc.q.y, sc.q.z]

        def f(s):
            return sc.derivatives(s, ext_torque, wt)

        dt = self.dt
        k1 = f(state)
        s2 = [state[i] + 0.5 * dt * k1[i] for i in range(7)]
        k2 = f(s2)
        s3 = [state[i] + 0.5 * dt * k2[i] for i in range(7)]
        k3 = f(s3)
        s4 = [state[i] + dt * k3[i] for i in range(7)]
        k4 = f(s4)
        new = [state[i] + dt / 6.0 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(7)]
        sc.omega = new[0:3]
        sc.q = Quaternion(*new[3:7])  # конструктор нормирует


# ═══════════════════════════════════════════════════════════════════════════
# Управление: разворот по одной оси
# ═══════════════════════════════════════════════════════════════════════════
def slew_single_axis(
    sc: Spacecraft,
    prop: AttitudePropagator,
    target: Quaternion,
    kp: float = 0.8,
    kd: float = 2.2,
    max_time: float = 60.0,
) -> dict:
    """Разворот к целевой ориентации (момент только колёсами).

    Закон: u = kp·v_err − kd·ω, где v_err — векторная часть
    q_err = q⁻¹ ⊗ q_target после флипа знака (q_err.w ≥ 0 —
    кратчайший поворот); Sidi §9.4 (знак ошибки уже в флипе w,
    поэтому на v_err — ПЛЮС). Колёса получают −u (реакция на
    корпус +u); насыщение колёс ограничивает фактический момент.
    """
    t = 0.0
    history = []
    while t < max_time:
        q_err = sc.q.conjugate() * target
        # знак: кратчайший поворот
        if q_err.w < 0:
            q_err = Quaternion(-q_err.w, -q_err.x, -q_err.y, -q_err.z)
        err_vec = (q_err.x, q_err.y, q_err.z)
        # желаемый момент КОРПУСА (kp·v_err: флип w уже дал знак)
        u_body = tuple(kp * err_vec[i] - kd * sc.omega[i] for i in range(3))
        # колёса получают −u_body; granted — их фактический момент
        granted = sc.wheels.apply_torque(tuple(-c for c in u_body), prop.dt)
        # корпус получает реакцию −granted (третий закон Ньютона)
        prop.wheel_torque = [-c for c in granted]
        prop.step()
        t += prop.dt
        history.append(sc.q.angle_to(target))
        if history[-1] < 1e-3 and max(abs(w) for w in sc.omega) < 1e-3:
            break
    return dict(
        final_error_deg=math.degrees(history[-1]),
        settle_time_s=t,
        n_steps=len(history),
        wheel_saturation=sc.wheels.saturation_fraction(),
    )


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """90° разворот сходится; |q| = 1; H сохраняется при свободном
    вращении без внешних моментов; кватернионная алгебра корректна."""
    # ── алгебра кватернионов ──
    q1 = Quaternion.from_axis_angle((0, 0, 1), math.pi / 2)
    v = q1.rotate((1.0, 0.0, 0.0))
    rot_ok = abs(v[0]) < 1e-9 and abs(v[1] - 1.0) < 1e-9 and abs(v[2]) < 1e-9
    norm_ok = abs(q1.norm() - 1.0) < 1e-12
    # поворот на 2π = тождество
    q2 = Quaternion.from_axis_angle((0, 0, 1), 2 * math.pi)
    ident_ok = q2.angle_to(Quaternion()) < 1e-9
    # ── 90° разворот с ПИД ──
    wheels = ReactionWheelArray(
        [
            ReactionWheel((1, 0, 0), max_torque=0.2, max_momentum=5.0),
            ReactionWheel((0, 1, 0), max_torque=0.2, max_momentum=5.0),
            ReactionWheel((0, 0, 1), max_torque=0.2, max_momentum=5.0),
        ]
    )
    sc = Spacecraft((2.0, 3.0, 4.0), wheels)
    prop = AttitudePropagator(sc, dt=0.01)
    target = Quaternion.from_axis_angle((0, 0, 1), math.pi / 2)
    res = slew_single_axis(sc, prop, target, kp=1.0, kd=4.0, max_time=60.0)
    slew_ok = res["final_error_deg"] < 0.5
    # ── сохранение момента при свободном вращении ──
    wheels2 = ReactionWheelArray(
        [
            ReactionWheel((1, 0, 0), 0.2, 5.0),
            ReactionWheel((0, 1, 0), 0.2, 5.0),
            ReactionWheel((0, 0, 1), 0.2, 5.0),
        ]
    )
    sc2 = Spacecraft((2.0, 3.0, 4.0), wheels2, omega=(0.05, -0.03, 0.02))
    prop2 = AttitudePropagator(sc2, dt=0.02)
    h0 = sc2.angular_momentum_total()
    for _ in range(500):
        prop2.step()  # без внешних моментов, без колёс
    h1 = sc2.angular_momentum_total()
    # ИНВАРИАНТ — модуль H: в корпусных осях компоненты вращаются
    # (dH/dt_корп = −ω×H), а |H| сохраняется при нулевом внешнем моменте
    h0_mag = math.sqrt(sum(h * h for h in h0))
    h1_mag = math.sqrt(sum(h * h for h in h1))
    h_drift = abs(h1_mag - h0_mag) / max(h0_mag, 1e-12)
    momentum_ok = h_drift < 1e-9
    # свободное вращение вокруг главной оси: ω постоянно (осевой случай)
    sc3 = Spacecraft(
        (2.0, 2.0, 4.0), ReactionWheelArray([ReactionWheel((0, 0, 1))]), omega=(0.0, 0.0, 0.1)
    )
    prop3 = AttitudePropagator(sc3, dt=0.05)
    for _ in range(200):
        prop3.step()
    axis_spin_ok = abs(sc3.omega[2] - 0.1) < 1e-9
    return dict(
        rotation_ok=rot_ok,
        quaternion_norm_ok=norm_ok,
        identity_ok=ident_ok,
        slew_error_deg=round(res["final_error_deg"], 4),
        settle_time_s=round(res["settle_time_s"], 1),
        slew_ok=slew_ok,
        momentum_drift=h_drift,
        momentum_ok=momentum_ok,
        axis_spin_ok=axis_spin_ok,
        all_ok=rot_ok and norm_ok and ident_ok and slew_ok and momentum_ok and axis_spin_ok,
        note="кватернионная ОС (Sidi §9.4); уравнения Эйлера жёсткого "
        "тела; H сохраняется при нулевом внешнем моменте",
    )
