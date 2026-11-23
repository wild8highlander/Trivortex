#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — полевые исследования: сеточные сканы параметров.

Сканирует: массу третьего тела × начальную скорость; N = 3…7(8) ×
расположение (кольцо/случайное/кластер); jitter вихревого кольца (устойчивость
Хавелока в динамике). Каждый прогон пишет JSON-протокол; итог — таблица
метрик, поиск бифуркаций по смене топологии траектории.
"""

from __future__ import annotations

import json
import math
import os
import random
from typing import Any

from core.config import MasterConfig, from_profile
from lab.body import Body
from lab.physics import run_simulation
from lab.scene import Scene
from render.hud import ProgressBar


# ═══════════════════════════════════════════════════════════════════════════
# Утилиты сцен для сканов
# ═══════════════════════════════════════════════════════════════════════════
def _central_scene(cfg: MasterConfig, m3: float, v_factor: float) -> Scene:
    """Звезда (1 M☉) + две планеты; у второй варьируются масса и скорость."""
    sc = Scene(cfg, name=f"scan_m{m3:.2g}_v{v_factor:.2f}")
    sc.add_body(
        Body(
            id="star",
            name="Star",
            mass=1.989e30,
            radius=6.957e8,
            position=(0, 0, 0),
            color="#FDB813",
            type="star",
            source="NSSDC",
        )
    )
    # планета 1 — на 1 а.е.
    au = 1.495978707e11
    v1 = math.sqrt(6.6743e-11 * 1.989e30 / au)
    sc.add_body(
        Body(
            id="p1",
            name="P1",
            mass=5.9722e24,
            radius=6.371e6,
            position=(au, 0, 0),
            velocity=(0, v1, 0),
            color="#4FD1C5",
            type="planet",
            source="NSSDC",
        )
    )
    # планета 2 — на 1.8 а.е., масса и скорость варьируются
    r2 = 1.8 * au
    v2 = v_factor * math.sqrt(6.6743e-11 * 1.989e30 / r2)
    sc.add_body(
        Body(
            id="p2",
            name="P2",
            mass=m3 * 5.9722e24,
            radius=6.371e6,
            position=(-r2, 0, 0),
            velocity=(0, -v2, 0),
            color="#E8C766",
            type="planet",
            source="scan",
        )
    )
    sc.dt = 3600.0 * 24 * 2
    return sc


def _vortex_ring_scene(cfg: MasterConfig, n: int, jitter: float, seed: int = 42) -> Scene:
    """Вихревое кольцо N вихрей с позиционным шумом (тест Хавелока)."""
    sc = Scene(cfg, name=f"ring_n{n}_j{jitter:.3g}")
    rng = random.Random(seed)
    R = 1.0
    for k in range(n):
        phi = 2 * math.pi * k / n
        rr = R * (1 + jitter * (rng.random() - 0.5))
        sc.add_body(
            Body(
                id=f"v{k}",
                name=f"V{k}",
                mass=1.0,
                radius=0.02,
                position=(rr * math.cos(phi), rr * math.sin(phi), 0.0),
                circulation=1.0,
                color="#A78BFA",
                type="synthetic",
                source="Kirchhoff; Havelock 1931",
            )
        )
    sc.apply_engine("native_vortex")
    gamma = 1.0
    omega_N = gamma * (n - 1) / (4 * math.pi * R * R)
    sc.dt = (2 * math.pi / max(abs(omega_N), 1e-9)) / 240.0
    return sc


# ═══════════════════════════════════════════════════════════════════════════
# Метрика топологии: закрутилась/разлетелась/столкнулась
# ═══════════════════════════════════════════════════════════════════════════
def classify_outcome(scene: Scene) -> dict[str, Any]:
    """Классификация судьбы прогона: escape/collision/regular/chaotic."""
    kinds = {e["kind"] for e in scene.events}
    if not scene.trajectory_history:
        return dict(outcome="empty")
    last = scene.trajectory_history[-1]
    first = scene.trajectory_history[0]
    r_now = max(math.sqrt(sum(c * c for c in s[:3])) for s in last)
    r_start = max(math.sqrt(sum(c * c for c in s[:3])) for s in first)
    spread = r_now / max(r_start, 1e-12)
    outcome = "regular"
    if "collision" in kinds:
        outcome = "collision"
    elif "escape" in kinds or spread > 2.5:
        outcome = "escape"
    else:
        # хаос: оценка ляпунова по самопересечениям трейла — упрощённо
        # по плотности событий детекторов
        if len(scene.events) > 3:
            outcome = "perturbed"
    return dict(outcome=outcome, spread=spread, events=len(scene.events))


# ═══════════════════════════════════════════════════════════════════════════
# Скан 1: масса × скорость (ньютоновский)
# ═══════════════════════════════════════════════════════════════════════════
def scan_mass_velocity(
    masses: list[float] | None = None,
    v_factors: list[float] | None = None,
    n_steps: int = 200,
    progress=None,
    output_json: str | None = None,
) -> dict[str, Any]:
    """Сетка: масса P2 (в M⊕) × множитель круговой скорости P2."""
    masses = masses or [0.1, 1.0, 10.0, 100.0]
    v_factors = v_factors or [0.6, 0.85, 1.0, 1.15, 1.4]
    cfg = from_profile("quick", n_steps=n_steps)
    grid: list[dict[str, Any]] = []
    idx = 0
    total = len(masses) * len(v_factors)
    for m in masses:
        for vf in v_factors:
            idx += 1
            sc = _central_scene(cfg, m, vf)
            sim = run_simulation(sc, n_steps=n_steps)
            outcome = classify_outcome(sc)
            grid.append(
                dict(
                    mass_earth=m,
                    v_factor=vf,
                    energy_drift=sim["energy_drift_rel"],
                    n_events=sim["total_events"],
                    **outcome,
                )
            )
            if progress:
                progress.update(idx, tag=f"скан {idx}/{total}")
    # бифуркации: смена исхода по соседним узлам сетки
    bifurcations = []
    for i in range(len(masses)):
        for j in range(len(v_factors) - 1):
            a = grid[i * len(v_factors) + j]
            b = grid[i * len(v_factors) + j + 1]
            if a["outcome"] != b["outcome"]:
                bifurcations.append(
                    dict(
                        mass_earth=a["mass_earth"],
                        between=(a["v_factor"], b["v_factor"]),
                        outcomes=(a["outcome"], b["outcome"]),
                    )
                )
    result = dict(
        scan="mass_velocity",
        grid=grid,
        bifurcations=bifurcations,
        params=dict(masses=masses, v_factors=v_factors, n_steps=n_steps),
    )
    if output_json:
        os.makedirs(os.path.dirname(output_json) or ".", exist_ok=True)
        with open(output_json, "w", encoding="utf-8") as fh:
            json.dump(result, fh, ensure_ascii=False, indent=1)
    return result


# ═══════════════════════════════════════════════════════════════════════════
# Скан 2: устойчивость вихревых колец N=2..8 (динамика Хавелока)
# ═══════════════════════════════════════════════════════════════════════════
def scan_havelock(
    jitters: list[float] | None = None,
    n_steps: int = 400,
    progress=None,
    output_json: str | None = None,
) -> dict[str, Any]:
    """Кольца N=2..8 при шуме позиций: N≤7 держат форму, N=8 разваливается.

    Численный двойник стадии W4 POLYVORTEX: при малом возмущении кольцо
    N=8 (max Re λ = +0.4502) расходится, N≤7 — нет. N=8 включается с
    allow_unphysical=True: цель скана — именно продемонстрировать порог.
    """
    jitters = jitters or [0.0, 0.02]
    cfg = from_profile(
        "quick", n_steps=n_steps, physics_engine="native_vortex", allow_unphysical=True
    )
    rows: list[dict[str, Any]] = []
    idx = 0
    total = 7 * len(jitters)
    for n in range(2, 9):
        for jit in jitters:
            idx += 1
            # идеальное кольцо N=8 неустойчиво, но экспонента e^(0.45t)
            # растёт медленно — для демонстрации шума даём ему больше шагов
            steps = n_steps if not (n == 8 and jit == 0) else n_steps * 4
            sc = _vortex_ring_scene(cfg, n, jit)
            run_simulation(sc, n_steps=steps)
            # деформация кольца: разброс радиусов в конце
            if sc.trajectory_history:
                last = sc.trajectory_history[-1]
                radii = [math.hypot(s[0], s[1]) for s in last]
                deform = (max(radii) - min(radii)) / max(sum(radii) / len(radii), 1e-12)
            else:
                deform = float("nan")
            rows.append(
                dict(
                    N=n,
                    jitter=jit,
                    deformation=deform,
                    stable=deform < 0.2,
                    # идеальное кольцо N=8 без возмущения — нечему расти:
                    # линейная неустойчивость (max Re λ=+0.4502) проявляется
                    # только при шуме; помечаем честно
                    havelock_prediction=(
                        "unstable*"
                        if (n == 8 and jit == 0)
                        else ("stable" if n <= 7 else "unstable")
                    ),
                )
            )
            if progress:
                progress.update(idx, tag=f"N={n} jit={jit}")
    # проверка прогноза Хавелока (N=8 без шума — маргинальный случай:
    # неустойчивость линейна, но без возмущения не проявляется — исключаем
    # из подсчёта согласия и помечаем отдельно)
    checked = [r for r in rows if r["havelock_prediction"] != "unstable*"]
    marginal = [r for r in rows if r["havelock_prediction"] == "unstable*"]
    matches = sum(1 for r in checked if (r["stable"]) == (r["N"] <= 7))
    result = dict(
        scan="havelock_rings",
        rows=rows,
        havelock_matches=matches,
        havelock_total=len(checked),
        havelock_agreement=matches / max(len(checked), 1),
        marginal_cases=len(marginal),
        note="unstable* = идеальное кольцо N=8 без возмущения: "
        "линейная неустойчивость (max Re λ = +0.4502) требует "
        "начального шума, чтобы проявиться",
        reference="POLYVORTEX W4: N≤7 stable, N=8 max Re λ = +0.4502",
    )
    if output_json:
        os.makedirs(os.path.dirname(output_json) or ".", exist_ok=True)
        with open(output_json, "w", encoding="utf-8") as fh:
            json.dump(result, fh, ensure_ascii=False, indent=1)
    return result


# ═══════════════════════════════════════════════════════════════════════════
# Сводка для отчёта
# ═══════════════════════════════════════════════════════════════════════════
def field_tables(results: list[dict[str, Any]]) -> list[tuple[str, list[str], list[list]]]:
    """Таблицы полевых исследований для ReportData."""
    tables = []
    for res in results:
        if res["scan"] == "mass_velocity":
            headers = ["m (M⊕)", "v/v_circ", "исход", "разлёт", "события", "дрейф E"]
            rows = [
                [
                    f"{g['mass_earth']:g}",
                    f"{g['v_factor']:.2f}",
                    g["outcome"],
                    f"{g['spread']:.2f}",
                    g["n_events"],
                    f"{g['energy_drift']:.0e}",
                ]
                for g in res["grid"]
            ]
            tables.append(("Скан масса × скорость", headers, rows))
            if res["bifurcations"]:
                bheaders = ["m (M⊕)", "между v-факторами", "смена исходов"]
                brows = [
                    [
                        b["mass_earth"],
                        f"{b['between'][0]:.2f}–{b['between'][1]:.2f}",
                        f"{b['outcomes'][0]} → {b['outcomes'][1]}",
                    ]
                    for b in res["bifurcations"]
                ]
                tables.append(("Найденные бифуркации", bheaders, brows))
        elif res["scan"] == "havelock_rings":
            headers = ["N", "шум", "деформация", "устойчиво", "прогноз Хавелока"]
            rows = [
                [
                    r["N"],
                    f"{r['jitter']:g}",
                    f"{r['deformation']:.3f}",
                    "да" if r["stable"] else "НЕТ",
                    r["havelock_prediction"],
                ]
                for r in res["rows"]
            ]
            tables.append(
                (
                    f"Кольца Хавелока (согласие с W4: "
                    f"{res['havelock_matches']}/{res['havelock_total']})",
                    headers,
                    rows,
                )
            )
    return tables
