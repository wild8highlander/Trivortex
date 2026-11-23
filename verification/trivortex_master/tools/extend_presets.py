#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Добавить 10 новых пресетов в data/presets_scenes.json (id проверены)."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data", "presets_scenes.json")

NEW = [
    dict(id="saturn_system", name="Система Сатурна (6 тел)",
         description="N=6: Сатурн, Мимас, Титан, Япет, Феба и тестовая "
                     "частица в кольцевой щели Кассини.",
         bodies=[dict(catalog="saturn", role="central"),
                 dict(catalog="mimas"),
                 dict(catalog="titan"),
                 dict(catalog="iapetus"),
                 dict(catalog="phoebe"),
                 dict(catalog="test_particle_1", orbit_km=125000.0,
                      role="satellite")],
         engine="native_newton", scale_mode="macro",
         time_span_days=90.0, suggested_backend="mpl"),
    dict(id="uranus_system", name="Система Урана (5 тел)",
         description="N=5: Уран с наклонной осью и Miranda, Titania, "
                     "Oberon; контроль наклонной орбитальной плоскости.",
         bodies=[dict(catalog="uranus", role="central"),
                 dict(catalog="miranda"),
                 dict(catalog="titania"),
                 dict(catalog="oberon")],
         engine="native_newton", scale_mode="macro",
         time_span_days=120.0, suggested_backend="mpl"),
    dict(id="neptune_system", name="Система Нептуна (4 тела)",
         description="N=4: Нептун, Тритон (ретроградная орбита!), "
                     "Протей и Нереида — проверка обратных орбит.",
         bodies=[dict(catalog="neptune", role="central"),
                 dict(catalog="triton"),
                 dict(catalog="proteus"),
                 dict(catalog="nereid")],
         engine="native_newton", scale_mode="macro",
         time_span_days=150.0, suggested_backend="mpl"),
    dict(id="mars_moons", name="Марс с Фобосом и Деймосом",
         description="N=3: Марс и два спутника на пределе Роша и за "
                     "синхронной орбитой — миграция приливов.",
         bodies=[dict(catalog="mars", role="central"),
                 dict(catalog="phobos"),
                 dict(catalog="deimos")],
         engine="native_newton", scale_mode="macro",
         time_span_days=20.0, suggested_backend="mpl"),
    dict(id="earth_moon_l4", name="Тройка Земля–Луна–L4",
         description="N=3: Земля, Луна и тестовая частица в точке Лагранжа "
                     "L4 (устойчивая либрация вокруг 60°).",
         bodies=[dict(catalog="earth", role="central"),
                 dict(catalog="moon"),
                 dict(catalog="test_particle_1", orbit_km=384400.0,
                      role="satellite", angle_deg=60.0)],
         engine="native_newton", scale_mode="macro",
         time_span_days=90.0, suggested_backend="mpl"),
    dict(id="pluto_charon", name="Плутон–Харон–Никта–Гидра",
         description="N=4: двойная планета с близкими спутниками — "
                     "динамика барицентрической системы.",
         bodies=[dict(catalog="pluto", role="central"),
                 dict(catalog="charon"),
                 dict(catalog="nix"),
                 dict(catalog="hydra")],
         engine="native_newton", scale_mode="macro",
         time_span_days=45.0, suggested_backend="mpl"),
    dict(id="proxima_system", name="Система Проксимы (4 тела)",
         description="N=4: Проксима Центавра, планеты b и d и "
                     "лёгкое межзвёздное тело на гиперболическом заходе.",
         bodies=[dict(catalog="proxima_centauri", role="central"),
                 dict(catalog="exo_proxima_cen_b"),
                 dict(catalog="exo_proxima_cen_d"),
                 dict(catalog="test_particle_1", orbit_km=0.4 * 1.496e8,
                      role="satellite")],
         engine="native_newton", scale_mode="macro",
         time_span_days=30.0, suggested_backend="mpl"),
    dict(id="vesta_trio", name="Хаотическое трио главного пояса",
         description="N=3: Веста, Паллада и Юнона — взаимные возмущения "
                     "трёх астероидов с периодами ≈ 2:2:1.4.",
         bodies=[dict(catalog="vesta"),
                 dict(catalog="pallas"),
                 dict(catalog="juno")],
         engine="native_newton", scale_mode="macro",
         time_span_days=365.0, suggested_backend="mpl"),
    dict(id="halley_earth", name="Галлея–Земля–Солнце",
         description="N=3: Солнце, Земля и комета Галлея (e=0.967) — "
                     "пролёт у Земли и выброс на ретроградный заход.",
         bodies=[dict(catalog="sun", role="central"),
                 dict(catalog="earth"),
                 dict(catalog="halley")],
         engine="native_newton", scale_mode="macro",
         time_span_days=365.0, suggested_backend="mpl"),
    dict(id="io_europa_ganymede", name="Лапласов резонанс",
         description="N=4: Юпитер, Ио, Европа, Ганимед — цепочка "
                     "2:1-2:1 и либрация лапласовой фазы.",
         bodies=[dict(catalog="jupiter", role="central"),
                 dict(catalog="io"),
                 dict(catalog="europa"),
                 dict(catalog="ganymede")],
         engine="native_newton", scale_mode="macro",
         time_span_days=60.0, suggested_backend="mpl"),
]


def main() -> int:
    data = json.load(open(PATH, encoding="utf-8"))
    existing = {p["id"] for p in data["presets"]}
    added = 0
    for preset in NEW:
        if preset["id"] in existing:
            print(f"  пропуск (уже есть): {preset['id']}")
            continue
        data["presets"].append(preset)
        added += 1
    with open(PATH, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    print(f"добавлено: {added}, всего пресетов: {len(data['presets'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
