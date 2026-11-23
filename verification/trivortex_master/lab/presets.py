#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — пресеты сцен и каталог объектов.

load_catalog()      — data/catalog.json (258 объектов, источники у каждого);
build_preset()      — сцена из data/presets_scenes.json по id;
catalog_summary()   — сводка по типам для меню справки;
search_catalog()    — поиск по имени/типу/идентификатору.

Орбитальные скорости расставляются кеплеровыми: v = √(GM/r) вокруг
родительского тела (планеты — вокруг Солнца/звезды, луны — вокруг планеты).
"""

from __future__ import annotations

import json
import math
import os
from typing import Any

from core.config import MasterConfig
from lab.body import Body, place_on_orbit
from lab.scene import Scene

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CATALOG_PATH = os.path.join(_ROOT, "data", "catalog.json")
_PRESETS_PATH = os.path.join(_ROOT, "data", "presets_scenes.json")
AU_M = 1.495978707e11


# ═══════════════════════════════════════════════════════════════════════════
# Каталог
# ═══════════════════════════════════════════════════════════════════════════
def load_catalog(path: str | None = None) -> dict[str, Any]:
    path = path or _CATALOG_PATH
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def catalog_objects(catalog: dict[str, Any] | None = None) -> list[dict]:
    cat = catalog or load_catalog()
    return cat.get("objects", [])


def catalog_summary(catalog: dict[str, Any] | None = None) -> dict[str, int]:
    out: dict[str, int] = {}
    for rec in catalog_objects(catalog):
        out[rec["type"]] = out.get(rec["type"], 0) + 1
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


def search_catalog(
    query: str, catalog: dict[str, Any] | None = None, limit: int = 20
) -> list[dict]:
    q = query.strip().lower()
    hits = []
    for rec in catalog_objects(catalog):
        hay = " ".join(
            [
                rec.get("id", ""),
                rec.get("name", ""),
                rec.get("type", ""),
                rec.get("metadata", {}).get("host_star", ""),
            ]
        ).lower()
        if q in hay:
            hits.append(rec)
            if len(hits) >= limit:
                break
    return hits


def validate_catalog(catalog: dict[str, Any] | None = None) -> list[str]:
    errors = []
    ids = set()
    for i, rec in enumerate(catalog_objects(catalog)):
        rid = rec.get("id", f"index_{i}")
        if rid in ids:
            errors.append(f"дубликат id: {rid}")
        ids.add(rid)
        for key in ("id", "name", "type", "mass_kg", "radius_km", "source"):
            if key not in rec:
                errors.append(f"[{rid}] нет поля {key}")
        if rec.get("mass_kg", 0) <= 0:
            errors.append(f"[{rid}] mass_kg <= 0")
        if rec.get("radius_km", 0) <= 0:
            errors.append(f"[{rid}] radius_km <= 0")
    return errors


# ═══════════════════════════════════════════════════════════════════════════
# Пресеты сцен
# ═══════════════════════════════════════════════════════════════════════════
def load_presets(path: str | None = None) -> list[dict[str, Any]]:
    path = path or _PRESETS_PATH
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return data.get("presets", [])


def get_preset(preset_id: str, path: str | None = None) -> dict[str, Any] | None:
    for p in load_presets(path):
        if p["id"] == preset_id:
            return p
    return None


def _orbit_radius_for(
    record: dict[str, Any], parent_record: dict[str, Any], override: float | None = None
) -> float:
    """Радиус орбиты в метрах: override > orbit_au > orbit_km."""
    if override is not None:
        return override
    if record.get("parent") and record.get("orbit_km"):
        return float(record["orbit_km"]) * 1000.0
    if parent_record.get("type") == "star" and record.get("orbit_au"):
        return float(record["orbit_au"]) * AU_M
    # fallback: метаданные самой записи
    meta = record.get("metadata", {})
    if record.get("orbit_au"):
        return float(record["orbit_au"]) * AU_M
    if record.get("orbit_km"):
        return float(record["orbit_km"]) * 1000.0
    if meta.get("orbit_au"):
        return float(meta["orbit_au"]) * AU_M
    return 1e9


def build_preset(
    preset_id: str, config: MasterConfig, catalog: dict[str, Any] | None = None
) -> Scene:
    """Собрать сцену из пресета по id."""
    preset = get_preset(preset_id)
    if preset is None:
        raise KeyError(f"пресет {preset_id} не найден")
    cat = catalog or load_catalog()
    by_id = {r["id"]: r for r in catalog_objects(cat)}

    # пресет с явным planner-ом (figure_eight) строится планировщиком
    if preset.get("planner") == "figure_eight":
        return _build_figure_eight(config, preset)

    # учебные модельные пресеты: безразмерные единицы G=1, m=1
    if preset_id in ("lagrange_triangle", "vortex_ring_5", "vortex_ring_7"):
        return _build_model_preset(preset_id, preset, config)

    scene = Scene(config, name=preset["name"])
    scene.scale_mode = preset.get("scale_mode", config.scale_mode)
    G = config.G

    parent_body: Body | None = None
    central_record: dict | None = None
    # первый элемент с role central/binary — родитель
    orbit_index = 0
    for spec in preset["bodies"]:
        if "catalog" in spec:
            rec = by_id.get(spec["catalog"])
            if rec is None:
                raise KeyError(f"объект {spec['catalog']} отсутствует в каталоге")
            body = Body.from_catalog(spec["catalog"], cat)
        elif "synthetic" in spec:
            rec = by_id.get(spec["synthetic"])
            if rec is None:
                raise KeyError(f"объект {spec['synthetic']} отсутствует в каталоге")
            body = Body.from_catalog(spec["synthetic"], cat)
        else:
            raise ValueError(f"спецификация тела без catalog/synthetic: {spec}")

        role = spec.get("role", "")
        if role in ("central", "binary") and parent_body is None and role == "central":
            body.position = (0.0, 0.0, 0.0)
            body.velocity = (0.0, 0.0, 0.0)
            parent_body = body
            central_record = rec
            scene.add_body(body)
            continue
        if role == "binary" and parent_body is None:
            # первый компонент двойной — на место, второй подтянется
            parent_body = body
            central_record = rec
            # для двойной: компоненты разнесём ниже
            scene.add_body(body)
            continue

        # орбитальное тело
        if parent_body is None:
            # нет центрального — расставляем по убывающей массе сами
            parent_body = scene.bodies[0] if scene.bodies else body
            central_record = by_id.get(parent_body.id)

        r = _orbit_radius_for(
            rec,
            central_record or {},
            override=spec.get("orbit_km")
            or (spec.get("orbit_au", None) and spec["orbit_au"] * AU_M)
            or None,
        )
        phase = spec.get("phase_deg", 30.0 * (orbit_index + 1))
        place_on_orbit(
            parent_body,
            body,
            r,
            phase_deg=phase,
            inclination_deg=spec.get("inclination_deg", 0.0),
            G=G,
        )
        orbit_index += 1
        scene.add_body(body)

    # двойная звезда: второй компонент зеркально
    if preset["id"] == "binary_plus_planet" and len(scene.bodies) >= 2:
        _fix_binary(scene, G)

    # подстройка dt под масштаб
    _autotune_dt(scene)
    return scene


def _build_model_preset(preset_id: str, preset: dict, config: MasterConfig) -> Scene:
    """Учебные пресеты в модельных единицах: G = 1, массы = 1.

    lagrange_triangle — три тела на равностороннем треугольнике (Лагранж 1772);
    vortex_ring_5/7   — вихревые кольца Кирхгофа N=5/7 (движок native_vortex).
    """
    import copy as _copy

    cfg = _copy.deepcopy(config)
    cfg.G = 1.0
    cfg.physics_engine = "native_vortex" if preset_id.startswith("vortex") else "native_newton"
    scene = Scene(cfg, name=preset["name"])
    n = len(preset["bodies"])
    colors = [
        "#4FD1C5",
        "#E8C766",
        "#A78BFA",
        "#7DD3FC",
        "#FB7185",
        "#34D399",
        "#FF9A76",
        "#C8D8D8",
    ]

    if preset_id == "lagrange_triangle":
        side = 1.0
        R = side / math.sqrt(3)
        total_mass = 3.0
        # ω Лагранжа: центростремительная сила от двух соседей компенсируется
        # вращением: m·ω²·R = Σ F_к центру ⇒ ω² = G·M_total/a³
        omega = math.sqrt(total_mass / side**3)
        for k in range(n):
            phi = 2 * math.pi * k / n
            x, y = R * math.cos(phi), R * math.sin(phi)
            vx, vy = -omega * R * math.sin(phi), omega * R * math.cos(phi)
            scene.add_body(
                Body(
                    id=f"lagrange_{k}",
                    name=f"Лагранж {k + 1}",
                    mass=1.0,
                    radius=0.02,
                    position=(x, y, 0.0),
                    velocity=(vx, vy, 0.0),
                    color=colors[k % len(colors)],
                    type="synthetic",
                    source="Lagrange 1772",
                )
            )
        scene.dt = 0.01
        return scene

    # вихревые кольца
    R = 1.0
    gamma = 1.0
    omega_N = gamma * (n - 1) / (4 * math.pi * R * R)
    for k in range(n):
        phi = 2 * math.pi * k / n
        x, y = R * math.cos(phi), R * math.sin(phi)
        # скорость точки на кольце: сумма полей остальных вихрей
        vx = vy = 0.0
        for j in range(n):
            if j == k:
                continue
            phj = 2 * math.pi * j / n
            xj, yj = R * math.cos(phj), R * math.sin(phj)
            dx, dy = x - xj, y - yj
            r2 = dx * dx + dy * dy
            if r2 > 0:
                vx += -gamma * (-dy) / (2 * math.pi * r2)
                vy += gamma * (-dx) / (2 * math.pi * r2)
        scene.add_body(
            Body(
                id=f"ring_{k}",
                name=f"Вихрь {k + 1}",
                mass=1.0,
                radius=0.03,
                position=(x, y, 0.0),
                velocity=(0.0, 0.0, 0.0),
                circulation=gamma,
                color=colors[k % len(colors)],
                type="synthetic",
                source="Kirchhoff; Havelock 1931; POLYVORTEX W2/W4",
                metadata=dict(omega_N=omega_N),
            )
        )
    # период кольца T = 2π/ω_N; dt = T/240
    scene.dt = (2 * math.pi / abs(omega_N)) / 240.0 if omega_N else 0.01
    return scene


def _fix_binary(scene: Scene, G: float) -> None:
    """Компоненты двойной — по круговым орбитам вокруг общего центра масс."""
    a, b = scene.bodies[0], scene.bodies[1]
    total = a.mass + b.mass
    # большая полуось из данных Проксимы ~ 1.3e13 м
    sep = 1.3e13
    omega = math.sqrt(G * total / sep**3)
    ra = sep * b.mass / total
    rb = sep * a.mass / total
    a.position = (-ra, 0.0, 0.0)
    a.velocity = (0.0, -omega * ra, 0.0)
    b.position = (rb, 0.0, 0.0)
    b.velocity = (0.0, omega * rb, 0.0)
    # планета — вокруг центра масс
    if len(scene.bodies) > 2:
        p = scene.bodies[2]
        r = 1.646e12  # 11 а.е.
        v = math.sqrt(G * total / r)
        p.position = (r, 0.0, 0.0)
        p.velocity = (0.0, v, 0.0)


def _build_figure_eight(config: MasterConfig, preset: dict) -> Scene:
    from lab.trajectory import AnalyticPlanner

    scene = Scene(config, name=preset["name"])
    planner = AnalyticPlanner()
    traj = planner.figure_eight(n_steps=8)
    for k, bid in enumerate(traj.body_ids):
        s = traj.states[0][k]
        body = Body(
            id=bid,
            name=f"Figure-eight {k + 1}",
            mass=1.0,
            radius=0.03,
            position=(s[0], s[1], s[2]),
            velocity=(s[3], s[4], s[5]),
            color=("#4FD1C5", "#E8C766", "#A78BFA")[k % 3],
            type="synthetic",
            source="Chenciner & Montgomery 2000",
        )
        scene.add_body(body)
    scene.dt = 0.005
    return scene


def _autotune_dt(scene: Scene) -> None:
    """Подобрать dt по самой короткой орбитальной шкале сцены.

    Критерий: самый быстрый орбитальный период должен покрываться ≥ 200 шагами.
    """
    if not scene.bodies:
        return
    G = scene.config.G
    best = None
    central = max(scene.bodies, key=lambda b: b.mass)
    for b in scene.bodies:
        if b is central:
            continue
        r = b.distance_to(central)
        if r <= 0:
            continue
        v = b.speed()
        if v <= 0:
            continue
        period = 2 * math.pi * r / v
        best = period if best is None else min(best, period)
    if best is not None and best > 0:
        scene.dt = max(best / 200.0, 1e-9)


def preset_list_description() -> list[tuple[str, str, str]]:
    """[(id, имя, N тел)] для меню."""
    out = []
    for p in load_presets():
        n = len(p.get("bodies", []))
        out.append((p["id"], p["name"], f"N={n}" + (" ⚠" if p.get("unphysical") else "")))
    return out
