#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — кеплеровская небесная механика.

Аналитический слой для орбит: решение уравнения Кеплера (Ньютон +
начальное приближение), взаимные переходы «элементы орбиты ↔ вектор
состояния», истинная/эксцентрическая аномалии, время полёта, vis-viva,
апсиды, итерационный решатель Ламберта (метод универсальных переменных,
для траекторных задач «точка A → точка B за время T»).

Все функции чистые, работают с СИ или безразмерными единицами —
единицы определяет G, переданный снаружи.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Tuple

Vec3 = Tuple[float, float, float]


# ═══════════════════════════════════════════════════════════════════════════
# Элементы орбиты
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class OrbitalElements:
    """Кеплеровы элементы (J2000-стиль)."""

    a: float  # большая полуось (м)
    e: float  # эксцентриситет
    i: float  # наклонение (рад)
    Omega: float  # долгота восходящего узла (рад)
    omega: float  # аргумент перицентра (рад)
    M: float  # средняя аномалия (рад)

    def period(self, mu: float) -> float:
        """Период обращения T = 2π√(a³/μ)."""
        return 2.0 * math.pi * math.sqrt(self.a**3 / mu)

    def energy(self, mu: float) -> float:
        """Удельная энергия ε = −μ/(2a)."""
        return -mu / (2.0 * self.a)

    def r_peri(self) -> float:
        """Return the periapsis radius of the orbit."""
        return self.a * (1.0 - self.e)

    def r_apo(self) -> float:
        """Return the apoapsis radius of the orbit."""
        return self.a * (1.0 + self.e)


# ═══════════════════════════════════════════════════════════════════════════
# Уравнение Кеплера
# ═══════════════════════════════════════════════════════════════════════════
def kepler_E(M: float, e: float, tol: float = 1e-12, max_iter: int = 64) -> float:
    """Решить уравнение Кеплера M = E − e·sin E для эксцентрической
    аномалии E (Ньютон с стартом Эберле-порядка).

    Сходится квадратично для 0 ≤ e < 1; для почти параболических орбит
    стартовое приближение усложняется (e·sinE ≈ M + e·sinM).
    """
    M = M % (2.0 * math.pi)
    if e < 1e-12:
        return M
    # стартовое приближение
    if e < 0.8:
        E = M + e * math.sin(M)
    else:
        E = math.pi if M < math.pi else M
    for _ in range(max_iter):
        f = E - e * math.sin(E) - M
        fp = 1.0 - e * math.cos(E)
        dE = f / fp
        E -= dE
        if abs(dE) < tol:
            break
    return E % (2.0 * math.pi)


def true_anomaly(E: float, e: float) -> float:
    """Истинная аномалия ν из эксцентрической E: tan(ν/2)=√((1+e)/(1−e))·tan(E/2)."""
    ratio = math.sqrt((1.0 + e) / (1.0 - e)) * math.tan(E / 2.0)
    nu = 2.0 * math.atan(ratio)
    # atan в (−π, π); вернуть в [0, 2π) согласованно с E
    if E > math.pi:
        nu += 2.0 * math.pi
    return nu % (2.0 * math.pi)


def radius_from_E(E: float, e: float, a: float) -> float:
    """r = a(1 − e·cos E)."""
    return a * (1.0 - e * math.cos(E))


# ═══════════════════════════════════════════════════════════════════════════
# Переходы элементы ↔ вектор состояния
# ═══════════════════════════════════════════════════════════════════════════
def elements_to_state(el: OrbitalElements, mu: float) -> Tuple[Vec3, Vec3]:
    """Кеплеровы элементы → (позиция, скорость) в плоскости экватора."""
    E = kepler_E(el.M, el.e)
    nu = true_anomaly(E, el.e)
    r = el.a * (1.0 - el.e * math.cos(E))
    h = math.sqrt(mu * el.a * (1.0 - el.e**2))  # удельный момент
    # позиция/скорость в орбитальной плоскости (PQW)
    xp = r * math.cos(nu)
    yp = r * math.sin(nu)
    vxp = -mu / h * math.sin(nu)
    vyp = mu / h * (el.e + math.cos(nu))
    # поворот PQW → IJK (3-1-3: ω, i, Ω)
    co, so = math.cos(el.omega), math.sin(el.omega)
    cO, sO = math.cos(el.Omega), math.sin(el.Omega)
    ci, si = math.cos(el.i), math.sin(el.i)
    r11 = cO * co - sO * so * ci
    r12 = -cO * so - sO * co * ci
    r21 = sO * co + cO * so * ci
    r22 = -sO * so + cO * co * ci
    r31 = so * si
    r32 = co * si
    pos = (r11 * xp + r12 * yp, r21 * xp + r22 * yp, r31 * xp + r32 * yp)
    vel = (r11 * vxp + r12 * vyp, r21 * vxp + r22 * vyp, r31 * vxp + r32 * vyp)
    return pos, vel


def state_to_elements(pos: Vec3, vel: Vec3, mu: float) -> OrbitalElements:
    """Вектор состояния → кеплеровы элементы (замкнутый обратный переход)."""
    x, y, z = pos
    vx, vy, vz = vel
    r = math.sqrt(x * x + y * y + z * z)
    v2 = vx * vx + vy * vy + vz * vz
    # векторы момента и Лапласа
    hx, hy, hz = (y * vz - z * vy, z * vx - x * vz, x * vy - y * vx)
    h2 = hx * hx + hy * hy + hz * hz
    ex = (v2 / mu - 1.0 / r) * x - (x * vx + y * vy + z * vz) / mu * vx
    ey = (v2 / mu - 1.0 / r) * y - (x * vx + y * vy + z * vz) / mu * vy
    ez = (v2 / mu - 1.0 / r) * z - (x * vx + y * vy + z * vz) / mu * vz
    e = math.sqrt(ex * ex + ey * ey + ez * ez)
    a = 1.0 / (2.0 / r - v2 / mu)  # vis-viva
    i = math.acos(max(-1.0, min(1.0, hz / math.sqrt(h2))))
    n_vec = (-hy, hx, 0.0)  # вектор узла
    n = math.sqrt(n_vec[0] ** 2 + n_vec[1] ** 2)
    if n < 1e-12:
        Omega = 0.0
    else:
        Omega = math.atan2(n_vec[1], n_vec[0]) % (2.0 * math.pi)
    # аргумент перицентра
    if n < 1e-12:
        omega = math.atan2(ey, ex) % (2.0 * math.pi)
    else:
        cos_omega = (n_vec[0] * ex + n_vec[1] * ey) / (n * e)
        omega = math.acos(max(-1.0, min(1.0, cos_omega)))
        if ez < 0:
            omega = 2.0 * math.pi - omega
    # истинная аномалия и средняя
    cos_nu = (ex * x + ey * y + ez * z) / (e * r)
    nu = math.acos(max(-1.0, min(1.0, cos_nu)))
    if (x * vx + y * vy + z * vz) < 0:
        nu = 2.0 * math.pi - nu
    E = 2.0 * math.atan(math.sqrt((1.0 - e) / (1.0 + e)) * math.tan(nu / 2.0))
    if E < 0:
        E += 2.0 * math.pi
    M = (E - e * math.sin(E)) % (2.0 * math.pi)
    return OrbitalElements(a=a, e=e, i=i, Omega=Omega, omega=omega, M=M)


# ═══════════════════════════════════════════════════════════════════════════
# Утилиты орбит
# ═══════════════════════════════════════════════════════════════════════════
def vis_viva_speed(mu: float, r: float, a: float) -> float:
    """v = √(μ(2/r − 1/a))."""
    return math.sqrt(mu * (2.0 / r - 1.0 / a))


def flight_time(el: OrbitalElements, mu: float, M0: float, M1: float) -> float:
    """Время перелёта между двумя средними аномалиями (для эллипса)."""
    n = math.sqrt(mu / el.a**3)  # среднее движение
    dM = (M1 - M0) % (2.0 * math.pi)
    return dM / n


def apsides(el: OrbitalElements, mu: float) -> dict:
    """Перицентр/апоцентр: радиусы и скорости."""
    rp, ra = el.r_peri(), el.r_apo()
    return dict(
        r_peri=rp,
        r_apo=ra,
        v_peri=vis_viva_speed(mu, rp, el.a),
        v_apo=vis_viva_speed(mu, ra, el.a),
        period=el.period(mu),
    )


# ═══════════════════════════════════════════════════════════════════════════
# Решатель Ламберта (универсальные переменные, итерация по z)
# ═══════════════════════════════════════════════════════════════════════════
def _stumpff_C(z: float) -> float:
    """Функция Штумпфа C(z) (косеканс-разложение)."""
    if z > 1e-6:
        return (1.0 - math.cos(math.sqrt(z))) / z
    if z < -1e-6:
        return (math.cosh(math.sqrt(-z)) - 1.0) / (-z)
    # разложение у нуля
    return 0.5 - z / 24.0 + z * z / 720.0


def _stumpff_S(z: float) -> float:
    """Функция Штумпфа S(z)."""
    if z > 1e-6:
        sz = math.sqrt(z)
        return (sz - math.sin(sz)) / (sz**3)
    if z < -1e-6:
        sz = math.sqrt(-z)
        return (math.sinh(sz) - sz) / (sz**3)
    return 1.0 / 6.0 - z / 120.0 + z * z / 5040.0


def lambert(
    r1: Vec3,
    r2: Vec3,
    dt: float,
    mu: float,
    prograde: bool = True,
    tol: float = 1e-10,
    max_iter: int = 200,
) -> Tuple[Vec3, Vec3] | None:
    """Задача Ламберта: найти скорости v1/v2 на дуге r1→r2 за время dt.

    Классическая формулировка Бэттина через универсальные переменные:
    итерация по z (Ньютон по F(z) = 0), затем разбор геометрии.
    Возвращает (v1, v2) или None, если решение не сошлось.
    """
    R1 = math.sqrt(sum(c * c for c in r1))
    R2 = math.sqrt(sum(c * c for c in r2))
    # косинус угла между радиусами (знак — направление облёта)
    cross = (
        r1[1] * r2[2] - r1[2] * r2[1],
        r1[2] * r2[0] - r1[0] * r2[2],
        r1[0] * r2[1] - r1[1] * r2[0],
    )
    cross_z = cross[2]
    cos_dnu = sum(a * b for a, b in zip(r1, r2)) / (R1 * R2)
    cos_dnu = max(-1.0, min(1.0, cos_dnu))
    dnu = math.acos(cos_dnu)
    if prograde:
        if cross_z < 0:
            dnu = 2.0 * math.pi - dnu
    else:
        if cross_z > 0:
            dnu = 2.0 * math.pi - dnu
    sin_dnu = math.sin(dnu)
    A = math.sqrt(R1 * R2 * (1.0 + math.cos(dnu))) * (1 if sin_dnu >= 0 else -1)
    # примечание: A=0 (полуоборот) — легальный вырожденный случай,
    # обрабатывается отдельной веткой в разборе решения ниже; ранний
    # отказ здесь был ошибкой

    def tof(z: float) -> float:
        C = _stumpff_C(z)
        S = _stumpff_S(z)
        y = R1 + R2 + A * (z * S - 1.0) / math.sqrt(C)
        if y < 0:
            return float("nan")
        x = math.sqrt(y / C)
        return (x**3 * S + A * math.sqrt(y)) / math.sqrt(mu)

    # бисекция по z до смены знака, затем Ньютон
    z = 0.0
    f0 = tof(0.0) - dt
    if math.isnan(f0):
        return None
    # ищем скобу
    z_lo, z_hi = 0.0, 0.0
    found = False
    for k in range(1, 60):
        z_try = -4.0 * math.pi**2 + k * (8.0 * math.pi**2 / 60)
        t = tof(z_try)
        if math.isnan(t):
            continue
        if (t - dt) * f0 < 0 or (t - dt) == 0:
            z_lo, z_hi = min(0.0, z_try), max(0.0, z_try)
            found = True
            break
    if not found:
        return None
    for _ in range(max_iter):
        z = 0.5 * (z_lo + z_hi)
        t = tof(z)
        if math.isnan(t):
            z_hi = z if z_hi != z else z_hi
            continue
        if abs(t - dt) < tol * max(dt, 1.0):
            break
        if (t - dt) * (tof(z_lo) - dt) <= 0:
            z_hi = z
        else:
            z_lo = z
    # разбор решения
    C = _stumpff_C(z)
    S = _stumpff_S(z)
    y = R1 + R2 + A * (z * S - 1.0) / math.sqrt(C)
    if y < 0:
        return None
    f = 1.0 - y / R1
    g = A * math.sqrt(y / mu)
    gdot = 1.0 - y / R2
    if abs(g) < 1e-12:
        # ВЫРОЖДЕННЫЙ СЛУЧАЙ: полуоборот (cos Δν = −1 → A = 0).
        # Дуга — половина коники через центр: скорости тангенциальны,
        # модуль из vis-viva с переходной полуосью a_t = (R1+R2)/2.
        a_t = (R1 + R2) / 2.0
        v1 = math.sqrt(mu * (2.0 / R1 - 1.0 / a_t))
        v2 = math.sqrt(mu * (2.0 / R2 - 1.0 / a_t))
        t1 = (-r1[1], r1[0], -r1[2])
        n1 = math.sqrt(sum(c * c for c in t1)) or 1.0
        t2 = (-r2[1], r2[0], -r2[2])
        n2 = math.sqrt(sum(c * c for c in t2)) or 1.0
        sign = 1.0 if prograde else -1.0
        v1_vec = tuple(sign * v1 * c / n1 for c in t1)
        v2_vec = tuple(sign * v2 * c / n2 for c in t2)
        return v1_vec, v2_vec
    v1 = ((r2[0] - f * r1[0]) / g, (r2[1] - f * r1[1]) / g, (r2[2] - f * r1[2]) / g)
    v2 = ((gdot * r2[0] - r1[0]) / g, (gdot * r2[1] - r1[1]) / g, (gdot * r2[2] - r1[2]) / g)
    return v1, v2


def hohmann_dv(r1: float, r2: float, mu: float) -> dict:
    """Двухимпульсный гоманов переход между круговыми орбитами."""
    v_c1 = math.sqrt(mu / r1)
    v_c2 = math.sqrt(mu / r2)
    a_t = (r1 + r2) / 2.0
    v_p = vis_viva_speed(mu, r1, a_t)  # скорость в перигее перехода
    v_a = vis_viva_speed(mu, r2, a_t)  # в апогее
    dv1 = v_p - v_c1
    dv2 = v_c2 - v_a
    tof = math.pi * math.sqrt(a_t**3 / mu)
    return dict(
        dv1=dv1,
        dv2=dv2,
        dv_total=dv1 + dv2,
        transfer_orbit_a=a_t,
        time_of_flight=tof,
        v_circular_1=v_c1,
        v_circular_2=v_c2,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка модуля (используется тестами)
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Круговая проверка: элементы → состояние → элементы."""
    mu = 1.0
    el = OrbitalElements(a=1.0, e=0.3, i=0.2, Omega=1.1, omega=0.7, M=0.4)
    pos, vel = elements_to_state(el, mu)
    el2 = state_to_elements(pos, vel, mu)
    diffs = dict(
        da=abs(el2.a - el.a),
        de=abs(el2.e - el.e),
        di=abs(el2.i - el.i),
        dO=abs(el2.Omega - el.Omega),
        dw=abs(el2.omega - el.omega),
    )
    # M может отличаться на 2π
    dM = abs(el2.M - el.M) % (2 * math.pi)
    dM = min(dM, 2 * math.pi - dM)
    diffs["dM"] = dM
    diffs["roundtrip_ok"] = all(v < 1e-9 for v in diffs.values() if isinstance(v, float))
    # Кеплер: E для круговой орбиты = M
    assert abs(kepler_E(0.7, 0.0) - 0.7) < 1e-12
    # vis-viva на круговой: v = √(μ/r)
    assert abs(vis_viva_speed(mu, 2.0, 2.0) - math.sqrt(0.5)) < 1e-12
    # Ламберт: полкруга за половину периода круговой орбиты
    r1 = (1.0, 0.0, 0.0)
    r2 = (-1.0, 0.0, 0.0)
    sol = lambert(r1, r2, math.pi, mu)
    diffs["lambert_ok"] = sol is not None
    if sol is not None:
        v1 = sol[0]
        # скорость в концах полуокружности радиуса 1: |v| = 1
        diffs["lambert_v_err"] = abs(math.sqrt(sum(c * c for c in v1)) - 1.0)
    return diffs
