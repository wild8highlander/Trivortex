#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — валидатор реализма.

Сверяет тела сцены с источниками каталога, проверяет начальные условия
на мгновенные столкновения/вылеты и ставит вердикт is_physical.
"""

from __future__ import annotations

import math
from typing import Any

from lab.body import Body
from lab.scene import Scene


class ValidatorWarning(dict):
    """Предупреждение валидации: severity = info|warn|error."""

    def __init__(self, severity: str, code: str, message: str):
        """Do ValidatorWarning.  init for severity, code, message and return the result."""
        super().__init__(severity=severity, code=code, message=message)


def validate_body(
    body: Body, catalog_record: dict[str, Any] | None = None
) -> list[ValidatorWarning]:
    """Проверка одного тела; при наличии записи каталога — сверка масс."""
    out = []
    if body.mass <= 0:
        out.append(ValidatorWarning("error", "mass", f"[{body.id}] масса <= 0"))
    if body.radius <= 0:
        out.append(ValidatorWarning("error", "radius", f"[{body.id}] радиус <= 0"))
    if body.source == "synthetic" and body.type not in ("synthetic", "generic"):
        out.append(
            ValidatorWarning(
                "warn", "source", f"[{body.id}] тип {body.type}, но источник synthetic"
            )
        )
    if catalog_record is not None:
        ref_mass = float(catalog_record.get("mass_kg", 0))
        if ref_mass > 0:
            rel = abs(body.mass - ref_mass) / ref_mass
            if rel > 0.05:
                out.append(
                    ValidatorWarning(
                        "warn",
                        "mass_mismatch",
                        f"[{body.id}] масса отличается от каталога "
                        f"на {rel * 100:.1f}% "
                        f"({body.mass:.3g} vs {ref_mass:.3g} кг)",
                    )
                )
        ref_radius_m = float(catalog_record.get("radius_km", 0)) * 1000.0
        if ref_radius_m > 0:
            rel = abs(body.radius - ref_radius_m) / ref_radius_m
            if rel > 0.05:
                out.append(
                    ValidatorWarning(
                        "warn",
                        "radius_mismatch",
                        f"[{body.id}] радиус отличается от каталога " f"на {rel * 100:.1f}%",
                    )
                )
    return out


def validate_scene(scene: Scene, catalog: dict[str, Any] | None = None) -> list[ValidatorWarning]:
    """Полная проверка сцены: тела, пересечения, скорости, вылеты."""
    out = []
    by_id = {}
    if catalog:
        for rec in catalog.get("objects", []):
            by_id[rec["id"]] = rec

    for b in scene.bodies:
        rec = by_id.get(b.id)
        out.extend(validate_body(b, rec))

    # мгновенные столкновения
    for i in range(len(scene.bodies)):
        for j in range(i + 1, len(scene.bodies)):
            a, c = scene.bodies[i], scene.bodies[j]
            d = a.distance_to(c)
            rsum = a.radius + c.radius
            if d < rsum:
                out.append(
                    ValidatorWarning(
                        "error",
                        "overlap",
                        f"тела {a.id} и {c.id} пересекаются: " f"d={d:.3g} < Σr={rsum:.3g}",
                    )
                )

    # убегающие скорости относительно самой массивной пары
    if len(scene.bodies) >= 2:
        masses = sorted(scene.bodies, key=lambda b: -b.mass)
        m_big = masses[0]
        G = scene.config.G
        for b in scene.bodies:
            if b is m_big:
                continue
            r = b.distance_to(m_big)
            if r <= 0:
                continue
            v_esc = math.sqrt(2 * G * m_big.mass / r)
            v_rel = math.sqrt(sum((x - y) ** 2 for x, y in zip(b.velocity, m_big.velocity)))
            if v_rel > 1.5 * v_esc:
                out.append(
                    ValidatorWarning(
                        "warn",
                        "hyperbolic",
                        f"{b.id}: скорость {v_rel:.3g} > 1.5·v_esc={1.5 * v_esc:.3g} "
                        f"относительно {m_big.id} — гиперболический вылет",
                    )
                )

    # N=8 без флага — двойная страховка (порог Хавелока)
    if scene.n > scene.config.max_bodies and not scene.config.allow_unphysical:
        out.append(
            ValidatorWarning(
                "error",
                "unphysical",
                f"N={scene.n} > {scene.config.max_bodies} без флага "
                "allow_unphysical (порог Хавелока)",
            )
        )
    return out


def is_physical(scene: Scene) -> bool:
    """True, если нет ошибок уровня error и N в допустимом диапазоне."""
    if scene.n > scene.config.max_bodies and not scene.config.allow_unphysical:
        return False
    for w in validate_scene(scene):
        if w["severity"] == "error":
            return False
    return True


def realism_report(scene: Scene, catalog: dict[str, Any] | None = None) -> dict[str, Any]:
    """Сводка для HUD/отчётов: сколько тел сверено, предупреждения."""
    warns = validate_scene(scene, catalog)
    return dict(
        physical=is_physical(scene),
        n_bodies=scene.n,
        n_warnings=sum(1 for w in warns if w["severity"] == "warn"),
        n_errors=sum(1 for w in warns if w["severity"] == "error"),
        warnings=[dict(w) for w in warns[:30]],
    )
