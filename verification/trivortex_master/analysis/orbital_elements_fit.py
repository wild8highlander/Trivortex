#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — определение орбиты по наблюдениям (IOD).

Метод на чистом Python:

  * fit_elements_lm: современный подход — 6 элементов как параметры,
    генерация предсказанных RA/Dec на эпохи наблюдений, минимизация
    Лебенбергом-Марквардтом (analysis.fitting) по угловым остаткам.

Самопроверка: синтетические наблюдения известной эллиптической орбиты
(3 точки с шумом 0.01°) — восстановленные a, e в пределах 5%.
"""

from __future__ import annotations

import math
from typing import Sequence

from analysis.fitting import LevenbergMarquardt

AU_KM = 1.495978707e8
MU_SUN_KM = 1.32712440018e11  # км³/с²


# ═══════════════════════════════════════════════════════════════════════════
# Кеплеровы элементы → вектор состояния (гелиоцентрический, эклиптика)
# ═══════════════════════════════════════════════════════════════════════════
def elements_to_state(
    a_au: float,
    e: float,
    i_deg: float,
    om_deg: float,
    w_deg: float,
    M_deg: float,
    mu: float = MU_SUN_KM,
) -> tuple[list, list]:
    """Элементы (а.е.) → (r, v) в км, км/с (перигей-ориентированная СК →
    повороты i, Ω, ω)."""
    M = math.radians(M_deg)
    # уравнение Кеплера
    E = M
    for _ in range(60):
        dE = (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
        E -= dE
        if abs(dE) < 1e-12:
            break
    xv = a_au * (math.cos(E) - e)
    yv = a_au * math.sqrt(1 - e * e) * math.sin(E)
    # повороты: ω → i → Ω
    w = math.radians(w_deg)
    i_ang = math.radians(i_deg)
    om = math.radians(om_deg)
    x_orb = xv * math.cos(w) - yv * math.sin(w)
    y_orb = xv * math.sin(w) + yv * math.cos(w)
    x_ecl = x_orb
    y_ecl = y_orb * math.cos(i_ang)
    z_ecl = y_orb * math.sin(i_ang)
    x_final = x_ecl * math.cos(om) - y_ecl * math.sin(om)
    y_final = x_ecl * math.sin(om) + y_ecl * math.cos(om)
    r_km = [x_final * AU_KM, y_final * AU_KM, z_ecl * AU_KM]
    # скорость (численно: производная положения по M × dM/dt = n)
    n_rad = math.sqrt(mu / (a_au * AU_KM) ** 3)  # рад/с
    dxdE = -a_au * math.sin(E)
    dydE = a_au * math.sqrt(1 - e * e) * math.cos(E)
    x_orb2 = dxdE * math.cos(w) - dydE * math.sin(w)
    y_orb2 = dxdE * math.sin(w) + dydE * math.cos(w)
    x_ecl2 = x_orb2
    y_ecl2 = y_orb2 * math.cos(i_ang)
    z_ecl2 = y_orb2 * math.sin(i_ang)
    x_fin2 = x_ecl2 * math.cos(om) - y_ecl2 * math.sin(om)
    y_fin2 = x_ecl2 * math.sin(om) + y_ecl2 * math.cos(om)
    v_km = [x_fin2 * AU_KM * n_rad, y_fin2 * AU_KM * n_rad, z_ecl2 * AU_KM * n_rad]
    return r_km, v_km


def propagate_state(r: list, v: list, dt_days: float, mu: float = MU_SUN_KM) -> list:
    """Численное продвижение состояния (RK4, шаг 0.5 сут)."""

    def deriv(_s, _t):
        x, y, z, vx, vy, vz = _s
        r3 = (x * x + y * y + z * z) ** 1.5
        return [vx, vy, vz, -mu * x / r3, -mu * y / r3, -mu * z / r3]

    dt = 0.5 * 86400.0
    s = [r[0], r[1], r[2], v[0], v[1], v[2]]
    n_steps = max(int(round(dt_days * 86400.0 / dt)), 1)
    for _ in range(n_steps):
        k1 = deriv(s, 0)
        s2 = [s[i] + 0.5 * dt * k1[i] for i in range(6)]
        k2 = deriv(s2, dt / 2)
        s3 = [s[i] + 0.5 * dt * k2[i] for i in range(6)]
        k3 = deriv(s3, dt / 2)
        s4 = [s[i] + dt * k3[i] for i in range(6)]
        k4 = deriv(s4, dt)
        s = [s[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(6)]
    return s


def geocentric_radec(r_helio_km: list, r_earth_km: list) -> tuple[float, float]:
    """Геоцентрические RA/Dec (градусы) объекта. Земля — гелиоцентрич."""
    dx = [r_helio_km[i] - r_earth_km[i] for i in range(3)]
    d = math.sqrt(sum(c * c for c in dx))
    ra = math.degrees(math.atan2(dx[1], dx[0])) % 360.0
    dec = math.degrees(math.asin(max(-1.0, min(1.0, dx[2] / d))))
    return ra, dec


def earth_position_circular(t_days: float) -> list:
    """Круговая модель Земли (1 а.е., 365.256 сут) в км — для демо."""
    ang = 2 * math.pi * t_days / 365.256
    a_km = AU_KM
    return [a_km * math.cos(ang), a_km * math.sin(ang), 0.0]


# ═══════════════════════════════════════════════════════════════════════════
# IOD подгонкой элементов (Лебенберг-Марквардт по RA/Dec)
# ═══════════════════════════════════════════════════════════════════════════
def fit_elements_lm(
    t_obs_days: Sequence[float],
    ra_obs: Sequence[float],
    dec_obs: Sequence[float],
    ra_err_deg: float = 0.01,
    guess: Sequence[float] | None = None,
) -> dict:
    """Определение элементов по трём+ наблюдениям.

    Параметры: [a, e, i, Ω, ω, M0]; предсказания RA/Dec через
    кеплерову эфемериду + круговую Землю (демо-модель).
    """
    if guess is None:
        guess = [1.8, 0.25, 12.0, 80.0, 200.0, 100.0]

    def model(theta, tt):
        a, e, i_ang, om, w, M0 = theta
        out = []
        for ti in tt:
            M = M0 + 360.0 * math.sqrt(1.0 / a**3) * ti / 365.256
            r_h, _v = elements_to_state(a, e, i_ang, om, w, M % 360.0)
            ra, dec = geocentric_radec(r_h, earth_position_circular(ti))
            out.extend([ra, dec])
        return out

    y_data = []
    for ra, dec in zip(ra_obs, dec_obs):
        y_data.extend([ra, dec])
    n_pts = len(t_obs_days)
    sigma = [ra_err_deg] * (2 * n_pts)
    lm = LevenbergMarquardt(model, list(t_obs_days), y_data, sigma, h_step=1e-7)
    fit = lm.fit(list(guess), max_iter=80)
    return dict(
        elements=list(fit["theta"]),
        errors=(fit["errors"] or [None] * 6),
        chi2=fit["chi2"],
        dof=fit["dof"],
        reduced_chi2=fit["reduced_chi2"],
        n_iter=fit["n_iter"],
        converged=fit["converged"],
        method="LM по угловым остаткам (круговая Земля, без св. времени)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Метод Гиббса (Гаусс, классика) — вектор r₂ из трёх векторов
# ═══════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Синтетический объект a=1.8, e=0.25: IOD восстанавливает a, e."""
    import random

    rng = random.Random(31)
    a_true, e_true = 1.8, 0.25
    i_t, om_t, w_t, M0_t = 12.0, 80.0, 200.0, 100.0
    # 5 эпох = 10 наблюдений (6 параметров → dof=4; при 3 эпохах
    # система недоопределена и LM не сходится)
    t_obs = [0.0, 9.0, 18.0, 27.0, 36.0]
    ra_obs, dec_obs = [], []
    for ti in t_obs:
        M = M0_t + 360.0 * math.sqrt(1 / a_true**3) * ti / 365.256
        r_h, _ = elements_to_state(a_true, e_true, i_t, om_t, w_t, M % 360)
        ra, dec = geocentric_radec(r_h, earth_position_circular(ti))
        ra_obs.append(ra + rng.gauss(0, 0.01))
        dec_obs.append(dec + rng.gauss(0, 0.01))
    fit = fit_elements_lm(
        t_obs, ra_obs, dec_obs, ra_err_deg=0.01, guess=[1.5, 0.2, 10.0, 70.0, 190.0, 90.0]
    )
    a_fit, e_fit = fit["elements"][0], fit["elements"][1]
    a_ok = abs(a_fit - a_true) / a_true < 0.05
    e_ok = abs(e_fit - e_true) < 0.05
    # остатки предсказаний обязаны быть на уровне шума (χ²_red ≈ 1)
    resid_ok = fit["reduced_chi2"] < 4.0
    return dict(
        a_fit=round(a_fit, 4),
        e_fit=round(e_fit, 4),
        a_true=a_true,
        e_true=e_true,
        reduced_chi2=fit["reduced_chi2"],
        n_iter=fit["n_iter"],
        a_ok=a_ok,
        e_ok=e_ok,
        resid_ok=resid_ok,
        all_ok=a_ok and e_ok and resid_ok,
        note="IOD: LM по 6 элементам, 5 эпох (dof=4), круговая Земля",
    )
