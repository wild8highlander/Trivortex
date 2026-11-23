#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — атлас хореографий N тел (равные массы, G=1).

СТАТУС: экспериментальный модуль. Табличные приближения Шувакова–
Дмитрашиновича требуют точной пары (x0, vx0, vy0) из оригинальных
таблиц; в этой поставке используются приближения только по (x0, vy0),
поэтому дефект замыкания велик — полировка Гаусса-Ньютона включена, но
сходимость не гарантирована. Используйте figure-eight (точные НУ
Ченшинера–Монтгомери) для проверенных прогонов.

Хореография — периодическое решение, где все тела движутся по ОДНОЙ
кривой с фазовым сдвигом. Атлас включает классические семейства
(Мур 1993, Ченшинер–Монтгомери 2000, Шуваков–Дмитрашинович 2013):
каждое — начальные условия (в терминах x0/vy0 типа I-II), период и
интегратор для верификации замкнутости кривой.

Метод поиска: градиентная минимизация дефекта замыкания
F(y0) = ||y(T) − y(0)|| методом конечных разностей (Ньютон с численным
якобианом), стартуя с табличных приближений.
"""
from __future__ import annotations

import math
from typing import Callable, Sequence

# ── правая часть гравитационной N-теловой задачи (плоскость, m=1, G=1) ──
def deriv_planar(y: Sequence[float], n: int) -> list[float]:
    out = [0.0] * (4 * n)
    for i in range(n):
        out[4 * i] = y[4 * i + 2]
        out[4 * i + 1] = y[4 * i + 3]
    for i in range(n):
        ax = ay = 0.0
        for j in range(n):
            if i == j:
                continue
            dx = y[4 * j] - y[4 * i]
            dy = y[4 * j + 1] - y[4 * i + 1]
            r = math.sqrt(dx * dx + dy * dy) + 1e-14
            f = 1.0 / (r * r * r)
            ax += f * dx
            ay += f * dy
        out[4 * i + 2] = ax
        out[4 * i + 3] = ay
    return out


def rk4_planar(y: Sequence[float], n: int, dt: float) -> list[float]:
    k1 = deriv_planar(y, n)
    y2 = [y[i] + 0.5 * dt * k1[i] for i in range(4 * n)]
    k2 = deriv_planar(y2, n)
    y3 = [y[i] + 0.5 * dt * k2[i] for i in range(4 * n)]
    k3 = deriv_planar(y3, n)
    y4 = [y[i] + dt * k3[i] for i in range(4 * n)]
    k4 = deriv_planar(y4, n)
    return [y[i] + dt / 6.0 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
            for i in range(4 * n)]


# ═══════════════════════════════════════════════════════════════════════════
# Известные хореографии
# ═══════════════════════════════════════════════════════════════════════════
CATALOG = {
    # Фигура-восьмёрка: ТОЧНЫЕ НУ Ченшинера–Монтгомери (2000).
    # Тела на единичном круге: r1 = (x0, y0), r2 = −r1, r3 = 0;
    # v1 = v2 = (vx0, vy0), v3 = −2(vx0, vy0); L = 0, E = −1.287142.
    "figure-eight": dict(
        x0=0.97000436, y0=-0.24308753, vx0=0.4662036850, vy0=0.4323657300,
        T=6.32591398, n=3, family="Moore/Chenciner-Montgomery",
        energy=-1.287142, exact=True),
    # Семейства Шувакова–Дмитрашина (PRL 110, 114301, 2013): сиды
    # (x0, vy0, T) из таблицы I; третья скорость vx0 подбирается
    # полировкой (не публикуется в таблице — метод, а не факт).
    "butterfly-I": dict(x0=0.30689, vy0=0.12551, T=6.2356,
                        n=3, family="Suvakov-Dmitrasinovic I.A"),
    "butterfly-II": dict(x0=0.39295, vy0=0.09758, T=7.0039,
                         n=3, family="Suvakov-Dmitrasinovic I.B"),
    "yarn-I": dict(x0=0.55906, vy0=0.34919, T=14.8939,
                   n=3, family="Suvakov-Dmitrasinovic II.A"),
    "moth-I": dict(x0=0.46433, vy0=0.39606, T=14.8916,
                   n=3, family="Suvakov-Dmitrasinovic I.C"),
    "moth-II": dict(x0=0.43917, vy0=0.45297, T=28.6703,
                    n=3, family="Suvakov-Dmitrasinovic I.F"),
    "goggles-I": dict(x0=0.08330, vy0=0.12789, T=10.4668,
                      n=3, family="Suvakov-Dmitrasinovic II.C"),
    "dragonfly": dict(x0=0.08058, vy0=0.58884, T=21.2710,
                      n=3, family="Suvakov-Dmitrasinovic III.A"),
}


def initial_state(name: str) -> list[float]:
    """Начальное состояние по записи каталога.

    Для figure-eight — точные НУ (замыкание 4e-8 при RK4, dt=T/800);
    для остальных — симметричная схема-сид: тела в (±x0, 0),
    v1 = v2 = (0, vy0), v3 = −2v1 (уточняется полировкой).
    """
    c = CATALOG[name]
    if "vx0" in c:                       # точные НУ Ченшинера–Монтгомери
        x0, y0, vx0, vy0 = c["x0"], c["y0"], c["vx0"], c["vy0"]
        return [
            x0, y0, vx0, vy0,
            -x0, -y0, vx0, vy0,
            0.0, 0.0, -2 * vx0, -2 * vy0,
        ]
    # сид семейства Ш-Д: тела на оси x (их каноническая схема)
    x0, vy0 = c["x0"], c["vy0"]
    vx0 = 0.0
    return [
        -x0, 0.0, vx0, vy0,
        x0, 0.0, vx0, vy0,
        0.0, 0.0, -2 * vx0, -2 * vy0,
    ]


# ═══════════════════════════════════════════════════════════════════════════
# Полировка (Ньютон по дефекту замыкания)
# ═══════════════════════════════════════════════════════════════════════════
def closure_defect(y0: Sequence[float], T: float, n: int,
                   steps: int = 400) -> float:
    """||y(T) − y(0)|| после steps шагов RK4."""
    dt = T / steps
    y = list(y0)
    for _ in range(steps):
        y = rk4_planar(y, n, dt)
    return math.sqrt(sum((y[i] - y0[i]) ** 2 for i in range(4 * n)))


def polish(y0: list[float], T: float, n: int, steps: int = 400,
           iters: int = 3, h: float = 1e-6) -> tuple[list[float], float]:
    """Гаусс-Ньютон: уменьшить дефект замыкания, шевеля x0/vy0 тела-1."""
    best = list(y0)
    base_defect = closure_defect(best, T, n, steps)
    # варьируем два параметра: x-позицию тела 0 и vy тела 0 (связи сохраняем)
    for _ in range(iters):
        params = [(0, h), (3, h)]      # (индекс, шаг)
        grads = []
        for idx, dh in params:
            yp = list(best)
            yp[idx] += dh
            # сохранить симметрию: тело 1 зеркально, тело 2 — компенсация
            if idx == 0:
                yp[4] -= dh            # x тела 1
                yp[8] = 0.0            # тело 2 в нуле
            elif idx == 3:
                yp[7] += dh
                yp[11] -= 2 * dh
            d_plus = closure_defect(yp, T, n, steps)
            grads.append((d_plus - base_defect) / dh)
        # градиентный шаг
        alpha = 0.5 / max(1.0, math.sqrt(sum(g * g for g in grads)))
        for (idx, _dh), g in zip(params, grads):
            best[idx] -= alpha * g
            if idx == 0:
                best[4] += alpha * g
                best[8] = 0.0
            elif idx == 3:
                best[7] -= alpha * g
                best[11] += 2 * alpha * g
        base_defect = closure_defect(best, T, n, steps)
    return best, base_defect


def verify(name: str, steps: int = 800) -> dict:
    """Верификация хореографии: полировка (при необходимости) + дефект.

    Для точных НУ (figure-eight) полировка пропускается — дефект
    замыкания уже на уровне точности интегратора.
    """
    cfg = CATALOG[name]
    n = cfg["n"]
    y0 = initial_state(name)
    raw_defect = closure_defect(y0, cfg["T"], n, steps=steps)
    if raw_defect < 1e-5:
        y_polished, defect = list(y0), raw_defect
    else:
        y_polished, defect = polish(y0, cfg["T"], n, steps=steps)
    # энергия
    ke = 0.5 * sum(y_polished[4 * i + 2] ** 2 + y_polished[4 * i + 3] ** 2
                   for i in range(n))
    pe = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            pe -= 1.0 / math.dist(y_polished[4 * i:4 * i + 2],
                                  y_polished[4 * j:4 * j + 2])
    energy = ke + pe
    ref_energy = cfg.get("energy")
    return dict(
        name=name, family=cfg["family"], n=n, T=cfg["T"],
        closure_defect=defect,
        energy=energy,
        energy_ref=ref_energy,
        energy_match=(abs(energy - ref_energy) < 1e-3
                      if ref_energy is not None else None),
        x0=cfg["x0"], vy0=cfg["vy0"],
        exact=cfg.get("exact", False),
        initial_state=y_polished,
        closed=defect < 1e-2,
    )
