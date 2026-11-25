#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерация data-файлов: literature.md, presets_scenes.json, trajectories.json, баннеры."""

from __future__ import annotations
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)
os.makedirs(os.path.join(DATA, "banners"), exist_ok=True)

# ═════════════════════════ literature.md ═════════════════════════
LITERATURE = """# TRIVORTEX MASTER — список литературы и источников данных

Каждый объект `data/catalog.json` ссылается на источник полем `source`.
Ниже — аннотированный перечень всех источников плана и каталога.

## Ядро Trivortex (наследуемый репозиторий)

1. **Isaev I. Kh. TRIVORTEX — The Three-Body (and N-Body) Problem in the
   Vortex Model, v1.0–1.1 (2026).** Ядро: `code/trivortex_core_en.py`,
   22 секции; Теорема 3.1 (замкнутая форма), топологический интеграл
   Чаплыгина, RMT-анализ, квантовый блок.
   <https://github.com/wild8highlander/Trivortex>
2. **Isaev I. Kh. Verification ladder V1–V4.**
   `verification/trivortex/python/verify.py` — независимая проверка Теоремы 3.1:
   хореография 2π/3 (остаток 6.9e-14), периодичность (9.4e-14), сохранение
   интегралов H, P, Q, I (2.9e-14). JSON-протоколы каждого прогона.
   <https://github.com/wild8highlander/Trivortex/tree/main/verification>
3. **Isaev I. Kh. POLYVORTEX — N-vortex bench, W-ladder W1–W7.**
   Порог Хевелока N ≤ 7 устойчиво / N ≥ 8 неустойчиво (стадия W4,
   max Re λ = +0.4502 при N=8); граница допустимости C_Ch > π·ln 2 (W5);
   ω_N = Γ(N−1)/(4πR²) (W2). Обоснование лимита тел 3–7 в TRIVORTEX MASTER.
   <https://github.com/wild8highlander/Trivortex/tree/main/polyvortex>
4. **Isaev I. Kh. CYCLORING.** Γ-периоды правильного кольца, W1–W7, 37 тестов.
   <https://github.com/wild8highlander/Trivortex/tree/main/cycloring>
5. **Isaev I. Kh. PLANETVORTEX.** PSL(2,7)-гравифигура Солнечной системы,
   Кеплер III с точностью 6.2e-13, прецессия Меркурия 42.982″/век (X6).
   <https://github.com/wild8highlander/Trivortex/tree/main/planetvortex>
6. **Isaev I. Kh. Research program TRX-01…TRX-12.** Двенадцать спутных
   исследований: лазерное давление, трёхволновое смешение, солитонные
   молекулы, фотонная жидкость, оптические вихри, гелий, эффект Эфимова,
   ионная ловушка, вихревое трио, Козаи–Лидов, ГВ-хореография, лазерный парус.
   <https://github.com/wild8highlander/Trivortex/tree/main/research>

## Физические движки (опциональные)

7. **Rein H., Liu S.-F. REBOUND: an open-source multi-purpose N-body code
   for collisional dynamics.** Astronomy & Astrophysics 537, A128 (2012).
   DOI: 10.1051/0004-6361/201118085. Интеграторы IAS15
   (Rein & Spiegel 2015, MNRAS 446, 1424), WHFast (Rein & Tamayo 2015),
   MERCURIUS. Лицензия GPL-3.0. <https://github.com/hannorein/rebound>
8. **Burns K. J., Vasil G. M., Oishi J. S., Lecoanet D., Brown B. P.
   Dedalus: A Flexible Framework for Numerically Solving Partial Differential
   Equations.** Physical Review Research 2, 023068 (2020).
   DOI: 10.1103/PhysRevResearch.2.023068.
   <https://github.com/DedalusProject/dedalus>

## Данные

9. **NASA Exoplanet Archive. Planetary Systems (ps) table.** TAP-сервис
   (sync/async), форматы VOTable/CSV/JSON. Источник экзопланетной части
   каталога; снимок кэшируется в `data/cache/exoplanets_<дата>.json`.
   <https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html>
10. **NASA NSSDC Planetary Fact Sheets.** Массы, радиусы, орбитальные
    параметры планет и их спутников.
    <https://nssdc.gsfc.nasa.gov/planetary/factsheet/>
11. **NASA NSSDC Asteroid / Comet Fact Sheets.**
    <https://nssdc.gsfc.nasa.gov/planetary/factsheet/asteroidfact.html>,
    <https://nssdc.gsfc.nasa.gov/planetary/factsheet/cometfact.html>
12. **SIMBAD astronomical database (CDS).** Параметры ближайших звёзд.
    <https://simbad.cds.unistra.fr/simbad/>
13. **JPL Small-Body Database Lookup.** Параметры астероидов.
    <https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html>

## Классика небесной механики и вихревой динамики

14. **Lagrange J. L. Essai sur le problème des trois corps.** Œuvres t. 6
    (1772). Равностороннее решение — основа Теоремы 3.1.
15. **Havelock T. H. The stability of motion of rectilinear vortices
    (ring of vortices).** Philosophical Magazine 11, 617–633 (1931).
    Классификация устойчивости N-вихревого кольца: порог N = 7/8.
16. **Chenciner A., Montgomery R. A remarkable periodic solution of the
    three-body problem in the case of equal masses.** Annals of Mathematics
    152, 881–901 (2000). DOI: 10.2307/2661357. Figure-eight хореография —
    пресет планировщика AnalyticPlanner.
17. **Aref H. Point vortex dynamics: a classical mathematics playground.**
    Journal of Mathematical Physics 48, 065401 (2007).
    DOI: 10.1063/1.2425100. Интегралы Кирхгофа H, P, Q, I.
18. **Šuvakov M., Dmitrašinović V. Three Classes of Newtonian Three-Body
    Planar Periodic Orbits.** PRL 110, 114301 (2013).
    DOI: 10.1103/PhysRevLett.110.114301. Атлас хореографий:
    бабочка, пряжа, очки и др.
19. **Murray C. D., Dermott S. F. Solar System Dynamics.** Cambridge
    University Press (1999). Возмущения, резонансы, механизм Козаи–Лидова.
20. **Chaplygin S. A. Об одном случае вихревого движения в жидкости.**
    Труды Отделения Физических Наук ОЛЕ (1903). Топологический интеграл.

## Прототип интерфейса

21. **AB-CLOUD Verification Suite · AURORA Edition (приложение к плану).**
    Прототип визуального языка: модули ABUI (truecolor ANSI, градиенты),
    ABMon (системный монитор из /proc), однострочный динамический
    прогресс-бар с EMA-ETA и очередью кадров, байтовые писатели
    PNG/GIF89a/PDF/DOCX на stdlib (собственные DEFLATE и LZW).
"""

# ═════════════════════════ presets_scenes.json ═════════════════════════
PRESETS = {
    "version": "1.0.0",
    "presets": [
        {
            "id": "inner_solar",
            "name": "Внутренняя Солнечная система",
            "description": "Солнце + Меркурий, Венера, Земля, Марс (N=5): "
            "ньютоновская гравитация, годовой масштаб.",
            "bodies": [
                {"catalog": "sun", "role": "central"},
                {"catalog": "mercury"},
                {"catalog": "venus"},
                {"catalog": "earth"},
                {"catalog": "mars"},
            ],
            "engine": "native_newton",
            "scale_mode": "macro",
            "time_span_years": 2.0,
            "suggested_backend": "mpl",
        },
        {
            "id": "earth_moon",
            "name": "Земля–Луна–станция",
            "description": "N=3: Земля, Луна и тестовая частица на переходной "
            "орбите; проверка пределов устойчивости.",
            "bodies": [
                {"catalog": "earth", "role": "central"},
                {"catalog": "moon"},
                {"catalog": "test_particle_1", "orbit_km": 200000.0, "role": "satellite"},
            ],
            "engine": "native_newton",
            "scale_mode": "macro",
            "time_span_days": 30.0,
            "suggested_backend": "mpl",
        },
        {
            "id": "jupiter_system",
            "name": "Система Юпитера",
            "description": "N=6: Юпитер и галилеевы луны + Амальтея — " "резонанс Лапласа 1:2:4.",
            "bodies": [
                {"catalog": "jupiter", "role": "central"},
                {"catalog": "io"},
                {"catalog": "europa"},
                {"catalog": "ganymede"},
                {"catalog": "callisto"},
                {"catalog": "amalthea"},
            ],
            "engine": "native_newton",
            "scale_mode": "macro",
            "time_span_days": 20.0,
            "suggested_backend": "mpl",
        },
        {
            "id": "lagrange_triangle",
            "name": "Треугольник Лагранжа",
            "description": "N=3: три равных тела в вершинах равностороннего "
            "треугольника — классическое решение 1772 года.",
            "bodies": [
                {"synthetic": "equal_mass_1", "pos_deg": 0},
                {"synthetic": "equal_mass_2", "pos_deg": 120},
                {"synthetic": "equal_mass_3", "pos_deg": 240},
            ],
            "engine": "native_newton",
            "scale_mode": "macro",
            "time_span_periods": 4.0,
            "suggested_backend": "mpl",
        },
        {
            "id": "figure_eight",
            "name": "Figure-eight (Шенкер–Монтгомери)",
            "description": "N=3: знаменитая хореография 2000 года — три равные "
            "массы гоняются по одной кривой в форме восьмёрки.",
            "bodies": [
                {"synthetic": "equal_mass_1"},
                {"synthetic": "equal_mass_2"},
                {"synthetic": "equal_mass_3"},
            ],
            "planner": "figure_eight",
            "engine": "native_newton",
            "scale_mode": "macro",
            "time_span_periods": 2.0,
            "suggested_backend": "mpl",
        },
        {
            "id": "vortex_ring_5",
            "name": "Вихревое кольцо N=5",
            "description": "N=5: пять точечных вихрей с Γ=1 на правильном "
            "пятиугольнике — жёсткое вращение ω_N = Γ(N−1)/(4πR²).",
            "bodies": [
                {"synthetic": "vortex_trio_a"},
                {"synthetic": "vortex_trio_b"},
                {"synthetic": "vortex_trio_c"},
                {"synthetic": "equal_mass_4"},
                {"synthetic": "equal_mass_5"},
            ],
            "engine": "native_vortex",
            "scale_mode": "micro",
            "time_span_periods": 3.0,
            "suggested_backend": "mpl",
        },
        {
            "id": "vortex_ring_7",
            "name": "Вихревое кольцо N=7 (последний устойчивый)",
            "description": "N=7: последний устойчивый уровень Хавелока — "
            "семь вихрей на правильном семиугольнике.",
            "bodies": [
                {"synthetic": "vortex_trio_a"},
                {"synthetic": "vortex_trio_b"},
                {"synthetic": "vortex_trio_c"},
                {"synthetic": "equal_mass_1"},
                {"synthetic": "equal_mass_2"},
                {"synthetic": "equal_mass_3"},
                {"synthetic": "equal_mass_4"},
            ],
            "engine": "native_vortex",
            "scale_mode": "micro",
            "time_span_periods": 3.0,
            "suggested_backend": "mpl",
        },
        {
            "id": "sun_all_planets",
            "name": "Солнце + все 8 планет (N=9)*",
            "description": "Демонстрация неустойчивой конфигурации: N=9 — "
            "выше жёсткого лимита; запускается только с флагом "
            "allow_unphysical (см. порог Хавелока).",
            "bodies": [
                {"catalog": "sun", "role": "central"},
                {"catalog": "mercury"},
                {"catalog": "venus"},
                {"catalog": "earth"},
                {"catalog": "mars"},
                {"catalog": "jupiter"},
                {"catalog": "saturn"},
                {"catalog": "uranus"},
                {"catalog": "neptune"},
            ],
            "engine": "native_newton",
            "scale_mode": "macro",
            "time_span_years": 50.0,
            "unphysical": True,
            "note": "N=9: превышение hard_max_bodies=8 — конфигурация вне "
            "физической вселенной модели; включается только с флагом "
            "allow_unphysical.",
            "suggested_backend": "mpl",
        },
        {
            "id": "trappist_like",
            "name": "Система Барнарда (N=5)",
            "description": "N=5: звезда Барнарда и её четыре суперземли с "
            "орбитами 0,019–0,038 а.е. — реальные данные "
            "NASA Exoplanet Archive (TAP).",
            "bodies": [
                {"catalog": "barnard's_star", "role": "central"},
                {"catalog": "exo_barnard_d"},
                {"catalog": "exo_barnard_b"},
                {"catalog": "exo_barnard_c"},
                {"catalog": "exo_barnard_e"},
            ],
            "engine": "native_newton",
            "scale_mode": "macro",
            "time_span_days": 30.0,
            "suggested_backend": "mpl",
        },
        {
            "id": "binary_plus_planet",
            "name": "Двойная звезда с планетой (N=3)",
            "description": "α Cen A, α Cen B и гипотетическая планета на "
            "нестабильной орбите — классическая задача "
            "ограниченных трёх тел.",
            "bodies": [
                {"catalog": "alpha_centauri_a", "role": "binary"},
                {"catalog": "alpha_centauri_b", "role": "binary"},
                {"catalog": "earth", "orbit_au": 11.0},
            ],
            "engine": "native_newton",
            "scale_mode": "macro",
            "time_span_years": 200.0,
            "suggested_backend": "mpl",
        },
        {
            "id": "saturn_system",
            "name": "Система Сатурна (6 тел)",
            "description": "N=6: Сатурн, Мимас, Титан, Япет, Феба и тестовая частица в кольцевой "
            "щели Кассини.",
            "bodies": [
                {"catalog": "saturn", "role": "central"},
                {"catalog": "mimas"},
                {"catalog": "titan"},
                {"catalog": "iapetus"},
                {"catalog": "phoebe"},
                {"catalog": "test_particle_1", "orbit_km": 125000.0, "role": "satellite"},
            ],
            "engine": "native_newton",
            "scale_mode": "macro",
            "time_span_days": 90.0,
            "suggested_backend": "mpl",
        },
        {
            "id": "uranus_system",
            "name": "Система Урана (5 тел)",
            "description": "N=5: Уран с наклонной осью и Miranda, Titania, Oberon; контроль "
            "наклонной орбитальной плоскости.",
            "bodies": [
                {"catalog": "uranus", "role": "central"},
                {"catalog": "miranda"},
                {"catalog": "titania"},
                {"catalog": "oberon"},
            ],
            "engine": "native_newton",
            "scale_mode": "macro",
            "time_span_days": 120.0,
            "suggested_backend": "mpl",
        },
        {
            "id": "neptune_system",
            "name": "Система Нептуна (4 тела)",
            "description": "N=4: Нептун, Тритон (ретроградная орбита!), Протей и Нереида — проверка "
            "обратных орбит.",
            "bodies": [
                {"catalog": "neptune", "role": "central"},
                {"catalog": "triton"},
                {"catalog": "proteus"},
                {"catalog": "nereid"},
            ],
            "engine": "native_newton",
            "scale_mode": "macro",
            "time_span_days": 150.0,
            "suggested_backend": "mpl",
        },
        {
            "id": "mars_moons",
            "name": "Марс с Фобосом и Деймосом",
            "description": "N=3: Марс и два спутника на пределе Роша и за синхронной орбитой — "
            "миграция приливов.",
            "bodies": [
                {"catalog": "mars", "role": "central"},
                {"catalog": "phobos"},
                {"catalog": "deimos"},
            ],
            "engine": "native_newton",
            "scale_mode": "macro",
            "time_span_days": 20.0,
            "suggested_backend": "mpl",
        },
        {
            "id": "earth_moon_l4",
            "name": "Тройка Земля–Луна–L4",
            "description": "N=3: Земля, Луна и тестовая частица в точке Лагранжа L4 (устойчивая "
            "либрация вокруг 60°).",
            "bodies": [
                {"catalog": "earth", "role": "central"},
                {"catalog": "moon"},
                {
                    "catalog": "test_particle_1",
                    "orbit_km": 384400.0,
                    "role": "satellite",
                    "angle_deg": 60.0,
                },
            ],
            "engine": "native_newton",
            "scale_mode": "macro",
            "time_span_days": 90.0,
            "suggested_backend": "mpl",
        },
        {
            "id": "pluto_charon",
            "name": "Плутон–Харон–Никта–Гидра",
            "description": "N=4: двойная планета с близкими спутниками — динамика барицентрической "
            "системы.",
            "bodies": [
                {"catalog": "pluto", "role": "central"},
                {"catalog": "charon"},
                {"catalog": "nix"},
                {"catalog": "hydra"},
            ],
            "engine": "native_newton",
            "scale_mode": "macro",
            "time_span_days": 45.0,
            "suggested_backend": "mpl",
        },
        {
            "id": "proxima_system",
            "name": "Система Проксимы (4 тела)",
            "description": "N=4: Проксима Центавра, планеты b и d и лёгкое межзвёздное тело на "
            "гиперболическом заходе.",
            "bodies": [
                {"catalog": "proxima_centauri", "role": "central"},
                {"catalog": "exo_proxima_cen_b"},
                {"catalog": "exo_proxima_cen_d"},
                {"catalog": "test_particle_1", "orbit_km": 59840000.0, "role": "satellite"},
            ],
            "engine": "native_newton",
            "scale_mode": "macro",
            "time_span_days": 30.0,
            "suggested_backend": "mpl",
        },
        {
            "id": "vesta_trio",
            "name": "Хаотическое трио главного пояса",
            "description": "N=3: Веста, Паллада и Юнона — взаимные возмущения трёх астероидов с "
            "периодами ≈ 2:2:1.4.",
            "bodies": [
                {"catalog": "vesta"},
                {"catalog": "pallas"},
                {"catalog": "juno"},
            ],
            "engine": "native_newton",
            "scale_mode": "macro",
            "time_span_days": 365.0,
            "suggested_backend": "mpl",
        },
        {
            "id": "halley_earth",
            "name": "Галлея–Земля–Солнце",
            "description": "N=3: Солнце, Земля и комета Галлея (e=0.967) — пролёт у Земли и выброс "
            "на ретроградный заход.",
            "bodies": [
                {"catalog": "sun", "role": "central"},
                {"catalog": "earth"},
                {"catalog": "halley"},
            ],
            "engine": "native_newton",
            "scale_mode": "macro",
            "time_span_days": 365.0,
            "suggested_backend": "mpl",
        },
        {
            "id": "io_europa_ganymede",
            "name": "Лапласов резонанс",
            "description": "N=4: Юпитер, Ио, Европа, Ганимед — цепочка 2:1-2:1 и либрация лапласовой "
            "фазы.",
            "bodies": [
                {"catalog": "jupiter", "role": "central"},
                {"catalog": "io"},
                {"catalog": "europa"},
                {"catalog": "ganymede"},
            ],
            "engine": "native_newton",
            "scale_mode": "macro",
            "time_span_days": 60.0,
            "suggested_backend": "mpl",
        },
    ],
}

# ═════════════════════════ trajectories.json ═════════════════════════
TRAJECTORIES = {
    "version": "1.0.0",
    "library": [
        {
            "id": "theorem31_ring",
            "name": "Теорема 3.1 — дышащее кольцо",
            "planner": "theorem31",
            "params": {"C_Ch": 1.0, "T": 6.283185307179586, "N": 3},
            "reference": "замкнутая форма: r_k(t)=√C_Ch·(1+ε·cos(ωt+2πk/3)), "
            "ω=(2π/T)·e^(C_Ch/π)=1.3748022274393588, "
            "ε=1/(e^(1/π)−1)=2.6680737914285615",
            "source": "Trivortex README §4; ladder V1 (6.9e-14)",
        },
        {
            "id": "lagrange_equilateral",
            "name": "Лагранж 1772 — равносторонний треугольник",
            "planner": "lagrange",
            "params": {"side": 1.0, "mass": 1.0, "N": 3},
            "reference": "жёсткое вращение треугольника; вихревой близнец — "
            "ω_L = 3Γ/(2πa²) (ladder V2)",
            "source": "Lagrange, Essai (1772); Trivortex verification V2",
        },
        {
            "id": "figure_eight",
            "name": "Figure-eight (Ченшинер–Монтгомери)",
            "planner": "figure_eight",
            "params": {"mass": 1.0, "G": 1.0},
            "reference": "периодическая хореография равных масс, "
            "x0=±0.97000436, v0=(0.4662036850, 0.4323657300)",
            "source": "Chenciner & Montgomery, Ann. Math. 152 (2000)",
        },
        {
            "id": "butterfly_I",
            "name": "Бабочка I (Шуваков–Дмитрашинович)",
            "planner": "scripted",
            "params": {"family": "butterfly", "variant": "I"},
            "reference": "хореография семейства бабочек PRL 110, 114301",
            "source": "Šuvakov & Dmitrašinović (2013)",
        },
        {
            "id": "circular_orbit",
            "name": "Круговая кеплерова орбита",
            "planner": "kepler",
            "params": {"eccentricity": 0.0},
            "reference": "v = √(GM/r); замкнутый круг",
            "source": "классика",
        },
        {
            "id": "elliptic_e06",
            "name": "Эллипс e=0.6",
            "planner": "kepler",
            "params": {"eccentricity": 0.6},
            "reference": "кеплеров эллипс с эксцентриситетом 0.6",
            "source": "классика",
        },
        {
            "id": "transfer_hohmann",
            "name": "Гоманов переход Земля→Марс",
            "planner": "scripted",
            "params": {"r1_au": 1.0, "r2_au": 1.524},
            "reference": "двухимпульсный переход между круговыми орбитами",
            "source": "Hohmann, Die Erreichbarkeit der Himmelskörper (1925)",
        },
    ],
}

# ═════════════════════════ banners/acll.txt ═════════════════════════
BANNER = """ █████╗ ██╗      █████╗ ██╗     ██╗      ██████╗
██╔══██╗██║     ██╔══██╗██║     ██║     ██╔════╝
███████║██║     ███████║██║     ██║     ██║
██╔══██║██║     ██╔══██║██║     ██║     ██║
██║  ██║███████╗██║  ██║███████╗███████╗╚██████╗
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝"""

BANNER_PLAIN = """+=====================================================+
|  A C L L   ·   T R I V O R T E X   M A S T E R      |
|          лаборатория N тел · v2.0.3                  |
+====================================================="""

# ═════════════════════════ запись ═════════════════════════
with open(os.path.join(DATA, "literature.md"), "w", encoding="utf-8") as fh:
    fh.write(LITERATURE)

with open(os.path.join(DATA, "presets_scenes.json"), "w", encoding="utf-8") as fh:
    json.dump(PRESETS, fh, ensure_ascii=False, indent=1)

with open(os.path.join(DATA, "trajectories.json"), "w", encoding="utf-8") as fh:
    json.dump(TRAJECTORIES, fh, ensure_ascii=False, indent=1)

with open(os.path.join(DATA, "banners", "acll.txt"), "w", encoding="utf-8") as fh:
    fh.write(BANNER)
with open(os.path.join(DATA, "banners", "acll_plain.txt"), "w", encoding="utf-8") as fh:
    fh.write(BANNER_PLAIN)

print("data-файлы записаны:")
for f in sorted(os.listdir(DATA)):
    p = os.path.join(DATA, f)
    if os.path.isfile(p):
        print(f"  {f}: {os.path.getsize(p)} байт")
