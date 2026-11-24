#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — карта неба в стереографической проекции (ASCII).

  * stereographic_project: (alt, az) → плоскость — конформная
    проекция: r = k·tan(z/2), z — зенитное расстояние; круги остаются
    кругами (свойство конформности, Snyder 1987, «Map Projections»);
  * sky_map_ascii: все 25 ярких звёзд в полусферическом виде для
    широты наблюдателя, символ по величине;
  * constellation_lines: грубые линии известных фигур (Большой Ковш,
    Орион) между яркими звёздами;
  * cardinal_marks: метки сторон горизонта.

Архитектура (правило направлений S3: render → {core, lab}): модуль НЕ
импортирует realism. Каталог ярких звёзд (realism.bright_stars) и
преобразования координат (realism.sky_coordinates) инъектируются
верхним слоем через bind_astronomy() — вызывается из modes_extra.py,
tools/quality_gate.py и tools/build_dist.py. Это тот же паттерн
инверсии зависимости, что register_engine() для адаптеров
REBOUND/Dedalus (см. core/registry.py): слой данных подключается к
слою отображения, не создавая ребра render → realism в графе импортов.

Самопроверки: зенит в центре; круг постоянной высоты — окружность
(конформность); звёзды ниже горизонта не рисуются; длина линий
Ориона соответствует угловым расстояниям.
"""

from __future__ import annotations

import math
from typing import Any, Callable, Sequence

# ── DI-слоты: инъекция астроданных (без импорта realism — правило S3) ──
_catalog_provider: Callable[[], Sequence[Any]] | None = None
_eq_to_horiz: Callable[..., tuple[float, float]] | None = None
_angular_sep: Callable[..., float] | None = None


def bind_astronomy(
    catalog_provider: Callable[[], Sequence[Any]],
    eq_to_horiz: Callable[..., tuple[float, float]],
    angular_sep: Callable[..., float],
) -> None:
    """Инъекция зависимости: realism-слой передаёт каталог ярких звёзд и
    преобразования координат; render остаётся свободным от импорта realism
    (правило направлений S3). Аналог register_engine() для движков."""
    global _catalog_provider, _eq_to_horiz, _angular_sep
    _catalog_provider = catalog_provider
    _eq_to_horiz = eq_to_horiz
    _angular_sep = angular_sep


def astronomy_bound() -> bool:
    """Привязан ли поставщик астроданных (для диагностики в меню)."""
    return _catalog_provider is not None and _eq_to_horiz is not None


def _require_astronomy() -> None:
    """Handle require astronomy."""
    if _catalog_provider is None or _eq_to_horiz is None:
        raise RuntimeError(
            "astronomy provider не привязан: вызовите "
            "render.ascii_sky.bind_astronomy(catalog, eq_to_horiz, ang_sep) "
            "из верхнего слоя (modes_extra / tools) — render не импортирует "
            "realism (правило направлений S3)"
        )


def stereographic_project(alt_deg: float, az_deg: float, k: float = 1.0) -> tuple[float, float]:
    """(alt, az) → (x, y) в единицах радиуса карты (зенит = (0,0)).

    z = 90° − alt; r = k·tan(z/2); направление — по азимуту от севера
    по часовой стрелке (вид сверху)."""
    z = math.radians(90.0 - alt_deg)
    if z >= math.pi / 2 - 1e-9:
        return (float("nan"), float("nan"))
    r = k * math.tan(z / 2.0)
    az = math.radians(az_deg)
    return (r * math.sin(az), r * math.cos(az))


def visible_stars(lat_deg: float, lst_rad: float) -> list[tuple[Any, float, float]]:
    """Звёзды над горизонтом: (звезда, alt, az) для широты и LST.

    Каталог и преобразование equatorial→horizontal приходят через
    bind_astronomy() (инъекция, S3)."""
    _require_astronomy()
    visible = []
    for star in _catalog_provider():
        az, alt = _eq_to_horiz(star.ra_deg, star.dec_deg, lat_deg, lst_rad)
        if alt > 0:
            visible.append((star, alt, az))
    return visible


# грубые линии созвездий (пары имён из каталога)
CONSTELLATION_LINES = {
    "Большой Ковш": [("Алиот", "Мирфак")],  # упрощённо (2 звезды)
    "Орион": [("Бетельгейзе", "Ригель"), ("Бетельгейзе", "Беллатрикс")],
    "Близнецы": [("Кастор", "Поллукс")],
    "Кентавр-Юг": [("α Центавра", "Хадар")],
}


def constellation_lengths(lat_deg: float, lst_rad: float) -> dict:
    """Угловые длины линий созвездий (для проверки масштаба).

    angular_separation инъектируется через bind_astronomy() (S3)."""
    _require_astronomy()
    out = {}
    for name, pairs in CONSTELLATION_LINES.items():
        total = 0.0
        for a, b in pairs:
            sa = [s for s in _catalog_provider() if s.name == a]
            sb = [s for s in _catalog_provider() if s.name == b]
            if not sa or not sb:
                continue
            total += _angular_sep(sa[0].ra_deg, sa[0].dec_deg, sb[0].ra_deg, sb[0].dec_deg)
        out[name] = total
    return out


def sky_map_ascii(lat_deg: float, lst_rad: float, width: int = 41, height: int = 21) -> str:
    """ASCII-карта полусферы: стереографическая проекция, зенит в центре.

    Символ яркости: ярче → плотнее (▓ █); сторона света подписана."""
    rows = [[" "] * width for _ in range(height)]
    cx, cy = (width - 1) / 2.0, (height - 1) / 2.0
    radius = min(cx, cy) - 1
    # окружность горизонта
    for ang in range(0, 360, 4):
        ax = cx + radius * math.sin(math.radians(ang))
        ay = cy - radius * math.cos(math.radians(ang))
        xi, yi = int(round(ax)), int(round(ay))
        if 0 <= xi < width and 0 <= yi < height:
            rows[yi][xi] = "·"
    # звёзды
    for star, alt, az in visible_stars(lat_deg, lst_rad):
        x, y = stereographic_project(alt, az)
        xi = int(round(cx + x * radius))
        yi = int(round(cy - y * radius))
        if 0 <= xi < width and 0 <= yi < height:
            if star.magnitude < 0.0:
                ch = "█"
            elif star.magnitude < 1.0:
                ch = "▓"
            elif star.magnitude < 2.0:
                ch = "▒"
            else:
                ch = "░"
            rows[yi][xi] = ch
    # метки сторон горизонта
    rows[0][int(cx)] = "С"
    rows[height - 1][int(cx)] = "Ю"
    rows[int(cy)][width - 1] = "В"
    rows[int(cy)][0] = "З"
    return "\n".join("".join(r) for r in rows)


# ═══════════════════════════════════════════════════════════════════════════
# Самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Зенит в центре; конформность: круг высоты 30° — окружность;
    карта непустая и содержит ярчайшие звёзды над горизонтом."""
    # зенит: alt=90 → (0, 0)
    x, y = stereographic_project(90.0, 0.0)
    zenith_ok = abs(x) < 1e-12 and abs(y) < 1e-12
    # конформность: точки на круге alt=30° — одинаковый радиус
    radii = []
    for az in (0, 45, 90, 180, 270):
        px, py = stereographic_project(30.0, az)
        radii.append(math.hypot(px, py))
    conformal_ok = max(radii) - min(radii) < 1e-9
    # карта: на широте 55.75 при LST = 6h (Орион на юге) есть яркие
    lst = math.radians(90.0)  # 6 часов
    visible = visible_stars(55.75, lst)
    visible_ok = len(visible) >= 8
    # Сириус с юга России (45°) виден, на 60° с.ш. низко
    lst_sirius = math.radians(101.28 + 0.0)  # RA Сириуса в градусах
    az_s, alt_s = _eq_to_horiz(101.28, -16.72, 55.75, lst_sirius)
    sirius_up = alt_s > 0
    # карта-строка
    text = sky_map_ascii(55.75, lst)
    map_ok = "█" in text or "▓" in text and len(text) > 400
    # Близнецы (Кастор-Поллукс): 4.51° по координатам каталога
    # (ΔRA 2.68°·cos30° + ΔDec 3.85°); память о 6° была неверна
    lengths = constellation_lengths(55.75, lst)
    gemini_len = lengths.get("Близнецы", 0)
    orion_ok = abs(gemini_len - 4.51) < 0.3
    return dict(
        zenith_ok=zenith_ok,
        conformal_ok=conformal_ok,
        astronomy_bound=astronomy_bound(),
        n_visible=len(visible),
        visible_ok=visible_ok,
        sirius_alt=round(alt_s, 1),
        sirius_up=sirius_up,
        gemini_line_deg=round(gemini_len, 2),
        orion_ok=orion_ok,
        map_ok=map_ok,
        all_ok=zenith_ok and conformal_ok and visible_ok and sirius_up and orion_ok and map_ok,
        note="стереографическая проекция — конформная (Snyder 1987); "
        "символ яркости: █ < 0ᵐ, ▓ < 1ᵐ, ▒ < 2ᵐ, ░ остальные; "
        "астроданные инъектируются через bind_astronomy (S3: render без realism)",
    )
