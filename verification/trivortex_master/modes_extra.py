#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — дополнительные режимы меню (наука, анализ, рендер).

Каждый режим запускает self_check соответствующего модуля (все
проверки — против независимых эталонов: наблюдения, аналитика,
литература), печатает цветную сводку и сохраняет протокол JSON в
каталог прогона. Импортируется из trivortex_master.py при старте —
регистрация идёт через @register_mode.

Категории: Наука (14), Анализ (10), Рендер (4), Отчёты (3),
Инструменты (3) — 34 режима сверх базовых 21.
"""

from __future__ import annotations

import json
import os

from core.registry import register_mode
from render.hud import kv, colorize, cyn,   verdict_icon


def bind_ascii_sky() -> bool:
    """S3-чистая инъекция астроданных для render.ascii_sky.

    render не импортирует realism (правило направлений S3: render →
    {core, lab}); каталог ярких звёзд и преобразования координат
    передаются сюда, на верхний слой меню. Аналог register_engine()
    для адаптеров движков. Возвращает True при успехе."""
    try:
        from realism.bright_stars import BRIGHT_STARS
        from realism.sky_coordinates import (
            angular_separation,
            equatorial_to_horizontal,
        )
        from render.ascii_sky import bind_astronomy

        bind_astronomy(lambda: BRIGHT_STARS, equatorial_to_horizontal, angular_separation)
        return True
    except Exception:  # noqa: BLE001 — карта неба опциональна в меню
        return False


# привязка при импорте модуля: режим «Карта неба (ASCII)» и quality gate
# получают работающий каталог без скрытой зависимости render → realism
_ASCII_SKY_BOUND = bind_ascii_sky()


class _AppShim:
    """Минимальная обвязка App: только new_run_dir (пути к протоколам).

    Режимы этого модуля автономны — сцена не требуется.
    """

    def __init__(self, base_dir: str | None = None):
        self.base_dir = base_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs")

    def new_run_dir(self, tag: str) -> str:
        import datetime as _dt

        d = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = os.path.join(self.base_dir, f"{d}_{tag}")
        os.makedirs(run_dir, exist_ok=True)
        return run_dir


# режимы принимают тот же app-объект, что и базовые (утиная типизация)
App = _AppShim


def _run_selfcheck(
    app: App, label: str, module: str, subtitle: str, func: str = "self_check"
) -> dict:
    """Общая обвязка: заголовок → self_check → печать → протокол JSON."""
    print(colorize(f"\n  {label}", cyn, True))
    print(f"  {subtitle}")
    res: dict = {}
    ok = False
    try:
        mod = __import__(module, fromlist=[func])
        res = getattr(mod, func)()
        ok = bool(res.get("all_ok", res.get("ok", False)))
    except Exception as exc:
        res = dict(error=f"{type(exc).__name__}: {exc}")
        ok = False
    mark = verdict_icon(ok)
    if ok:
        print(f"  {mark} проверка пройдена")
    else:
        print(f"  {mark} ПРОВАЛ: {res.get('error', 'несоответствие эталону')}")
    # печать ключевых величин (первые 6 скалярных)
    shown = 0
    for k, v in res.items():
        if shown >= 6:
            break
        if isinstance(v, (int, float, bool, str)) and k not in ("error",):
            if isinstance(v, float) and abs(v) < 1e-3 or abs(v) > 1e6:
                print(kv(k, f"{v:.3e}"))
            else:
                print(kv(k, str(v)))
            shown += 1
    run_dir = app.new_run_dir(label)
    with open(os.path.join(run_dir, f"{label}.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1, default=str)
    print(f"  протокол: {run_dir}/{label}.json")
    return res


# ═══════════════════════════════════════════════════════════════════════════
# НАУКА (14 режимов)
# ═══════════════════════════════════════════════════════════════════════════
@register_mode(
    name="science_relativity",
    title="Постньютон (1PN/2PN, ОТО)",
    category="Наука",
    icon="🌌",
    order=10,
    description="Меркурий 42.98″/век, Халс-Тейлор, ISCO, ЛТ",
)
def mode_science_relativity(app: App):
    _run_selfcheck(
        app,
        "science_relativity",
        "lab.relativity",
        "1PN Меркурий 42.98″/век; слияние PSR B1913+16; ISCO Керра",
    )


@register_mode(
    name="science_barnes_hut",
    title="Barnes-Hut O(N log N)",
    category="Наука",
    icon="🌳",
    order=20,
    description="Октодерево vs прямое суммирование: точность/скорость",
)
def mode_science_barnes_hut(app: App):
    _run_selfcheck(
        app,
        "science_barnes_hut",
        "lab.nbody_tree",
        "θ-критерий, leapfrog-дрейф энергии, ускорение ×N",
    )


@register_mode(
    name="science_chaos",
    title="Хаос: FLI/Пуанкаре/Ласкар",
    category="Наука",
    icon="🌀",
    order=30,
    description="Хеньон-Хейлес E=1/8 против E=1/12",
)
def mode_science_chaos(app: App):
    _run_selfcheck(
        app, "science_chaos", "lab.chaos", "FLI разделяет хаос и регулярность; дрейф частот"
    )


@register_mode(
    name="science_collisions",
    title="Столкновения и осколки",
    category="Наука",
    icon="💥",
    order=40,
    description="Импульс/энергия: слияние, отскок, фрагментация",
)
def mode_science_collisions(app: App):
    _run_selfcheck(
        app,
        "science_collisions",
        "lab.collisions",
        "законы сохранения при слиянии/отскоке/разрушении",
    )


@register_mode(
    name="science_tides",
    title="Приливы",
    category="Наука",
    icon="🌊",
    order=50,
    description="Луна 3.8 см/год (LLR), Ио 1e14 Вт, Козаи 39.23°",
)
def mode_science_tides(app: App):
    _run_selfcheck(
        app, "science_tides", "lab.tides", "миграция Луны, нагрев Ио, критический наклон Козаи"
    )


@register_mode(
    name="science_radiation",
    title="Радиация: П-Р/Ярковский",
    category="Наука",
    icon="☀️",
    order=60,
    description="t_PR пылинки, β-граница, Starshot 0.2c",
)
def mode_science_radiation(app: App):
    _run_selfcheck(
        app,
        "science_radiation",
        "lab.radiation",
        "Wyatt-Whipple, β = 3L/(16πcGMρs), световой парус",
    )


@register_mode(
    name="science_resonances",
    title="Резонансы",
    category="Наука",
    icon="🔗",
    order=70,
    description="Кирквуд, Лаплас 4:2:1, Wisdom, TTV LXW12",
)
def mode_science_resonances(app: App):
    _run_selfcheck(
        app,
        "science_resonances",
        "lab.resonances",
        "положения p:q, хаотическая зона, сверхпериоды TTV",
    )


@register_mode(
    name="science_tissot",
    title="Тиссеран",
    category="Наука",
    icon="🧭",
    order=80,
    description="T_J и динамическая классификация малых тел",
)
def mode_science_tissot(app: App):
    _run_selfcheck(
        app, "science_tissot", "lab.tissot", "Церера 4.57, со-орбита T=3, классы Levison 1996"
    )


@register_mode(
    name="science_halo",
    title="CR3BP и точки Лагранжа",
    category="Наука",
    icon="🛰️",
    order=90,
    description="L1–L5 Земля-Луна, интеграл Якоби, Лиссажу",
)
def mode_science_halo(app: App):
    _run_selfcheck(
        app, "science_halo", "lab.halo_orbits", "NASA-точность L1/L2, дрейф C ~ dt⁴ (RK4)"
    )


@register_mode(
    name="science_planetary",
    title="Архитектуры систем",
    category="Наука",
    icon="🪐",
    order=100,
    description="Hill-устойчивость, упаковка ЗЖЗ, TRAPPIST-1",
)
def mode_science_planetary(app: App):
    _run_selfcheck(
        app,
        "science_planetary",
        "realism.planetary_systems",
        "Гладман, T_eq TRAPPIST-1e, цепочка 8:5:3:2:4:3:2",
    )


@register_mode(
    name="science_stellar",
    title="Звёздная физика",
    category="Наука",
    icon="⭐",
    order=110,
    description="M-L-R, времена жизни, Рош-Эггльтон",
)
def mode_science_stellar(app: App):
    _run_selfcheck(
        app,
        "science_stellar",
        "realism.stellar",
        "Солнце точное, O-звезда ~1.4 млн лет, красный карлик",
    )


@register_mode(
    name="science_mission",
    title="Миссии: Hohmann/Циолковский",
    category="Наука",
    icon="🚀",
    order=120,
    description="Земля→Марс 5.6 км/с, porkchop, бюджет топлива",
)
def mode_science_mission(app: App):
    _run_selfcheck(
        app, "science_mission", "realism.mission_design", "гоманн, C3 окна, многоступенчатая ракета"
    )


@register_mode(
    name="science_encounter",
    title="Гравиманёвры",
    category="Наука",
    icon="🎯",
    order=130,
    description="поворот v∞, Oberth, случай Voyager 2",
)
def mode_science_encounter(app: App):
    _run_selfcheck(
        app, "science_encounter", "realism.encounter", "δ = 2arcsin(1/(1+rp·v∞²/μ)), эффект Оберта"
    )


@register_mode(
    name="science_horizons",
    title="Эфемериды Horizons",
    category="Наука",
    icon="📡",
    order=140,
    description="JPL API + честный offline-режим",
)
def mode_science_horizons(app: App):
    _run_selfcheck(
        app,
        "science_horizons",
        "realism.jpl_horizons",
        "векторы планет на сегодня; offline = средние элементы",
    )


# ═══════════════════════════════════════════════════════════════════════════
# АНАЛИЗ (10 режимов)
# ═══════════════════════════════════════════════════════════════════════════
@register_mode(
    name="analysis_lombscargle",
    title="Ломб-Скаргл",
    category="Анализ",
    icon="📈",
    order=15,
    description="периоды в неравномерных рядах, FAP",
)
def mode_analysis_lombscargle(app: App):
    _run_selfcheck(
        app,
        "analysis_lombscargle",
        "analysis.lomb_scargle",
        "сигнал 7.4 сут с пропусками; шум не детектируется",
    )


@register_mode(
    name="analysis_ttvs",
    title="TTV-анализ",
    category="Анализ",
    icon="⏱️",
    order=16,
    description="O−C, амплитуда/период, super-period",
)
def mode_analysis_ttvs(app: App):
    _run_selfcheck(app, "analysis_ttvs", "analysis.ttvs", "восстановление синтетической TTV; LXW12")


@register_mode(
    name="analysis_bls",
    title="BLS транзиты",
    category="Анализ",
    icon="📉",
    order=17,
    description="Box Least Squares, SDE, SNR глубины",
)
def mode_analysis_bls(app: App):
    _run_selfcheck(
        app,
        "analysis_bls",
        "analysis.periodogram",
        "P=3.5 сут, глубина 1%, 200 ppm — восстановление",
    )


@register_mode(
    name="analysis_mcmc",
    title="MCMC Метрополиса",
    category="Анализ",
    icon="🎲",
    order=18,
    description="апостериорные распределения, R̂ Гельмана",
)
def mode_analysis_mcmc(app: App):
    _run_selfcheck(
        app, "analysis_mcmc", "analysis.mcmc", "4 цепи, согласие с МНК-интервалом, R̂ < 1.1"
    )


@register_mode(
    name="analysis_wavelets",
    title="Вейвлеты Морле",
    category="Анализ",
    icon="〰️",
    order=19,
    description="CWT, скалограммы, гребень chirp",
)
def mode_analysis_wavelets(app: App):
    _run_selfcheck(
        app, "analysis_wavelets", "analysis.wavelets", "chirp 2→5 Гц: гребень с ошибкой < 15%"
    )


@register_mode(
    name="analysis_fitting",
    title="Левенберг-Марквардт",
    category="Анализ",
    icon="🎯",
    order=20,
    description="нелинейный МНК, ковариации, RV-кривая",
)
def mode_analysis_fitting(app: App):
    _run_selfcheck(
        app,
        "analysis_fitting",
        "analysis.fitting",
        "гаусс в 3σ; K = 10.04 ± 0.18 м/с при истине 10",
    )


@register_mode(
    name="analysis_iod",
    title="Определение орбиты (IOD)",
    category="Анализ",
    icon="🔭",
    order=21,
    description="элементы из RA/Dec наблюдений (LM)",
)
def mode_analysis_iod(app: App):
    _run_selfcheck(
        app, "analysis_iod", "analysis.orbital_elements_fit", "5 эпох, dof=4, восстановление a и e"
    )


@register_mode(
    name="analysis_proper",
    title="Собственные элементы",
    category="Анализ",
    icon="👨‍👩‍👧‍👦",
    order=22,
    description="семьи астероидов, HCM-кластеризация",
)
def mode_analysis_proper(app: App):
    _run_selfcheck(
        app,
        "analysis_proper",
        "analysis.proper_elements",
        "две синтетические семьи, Δv-критерий, Zappalà 1990",
    )


@register_mode(
    name="analysis_sky",
    title="Небесные координаты",
    category="Анализ",
    icon="🌐",
    order=23,
    description="RA/Dec ↔ Az/Alt/эклиптика, GMST, прецессия",
)
def mode_analysis_sky(app: App):
    _run_selfcheck(
        app, "analysis_sky", "realism.sky_coordinates", "Полюс→Alt=φ, Сириус β=−39.6°, GMST J2000"
    )


@register_mode(
    name="analysis_tle",
    title="TLE-эфемериды",
    category="Анализ",
    icon="🛰️",
    order=24,
    description="разбор NORAD TLE, контрольные суммы",
)
def mode_analysis_tle(app: App):
    _run_selfcheck(app, "analysis_tle", "realism.tles", "формат NORAD, период МКС ~92.9 мин")


# ═══════════════════════════════════════════════════════════════════════════
# РЕНДЕР (4 режима)
# ═══════════════════════════════════════════════════════════════════════════
@register_mode(
    name="render_raytracer",
    title="Рейтрейсер",
    category="Рендер",
    icon="🔆",
    order=10,
    description="Фонг+тени+отражения, PNG-кодер",
)
def mode_render_raytracer(app: App):
    _run_selfcheck(
        app,
        "render_raytracer",
        "render.raytracer",
        "3 сферы + пол: видимость, тонемаппинг Рейнхарда",
    )


@register_mode(
    name="render_particles",
    title="Частицы",
    category="Рендер",
    icon="✨",
    order=20,
    description="взрывы, аккреционные диски, джеты",
)
def mode_render_particles(app: App):
    _run_selfcheck(
        app, "render_particles", "render.particles", "жизненный цикл, гравитация+drag, палитры"
    )


@register_mode(
    name="render_camera",
    title="Кинематографические камеры",
    category="Рендер",
    icon="🎬",
    order=30,
    description="орбита, следование, Катмулл-Ром, тряска",
)
def mode_render_camera(app: App):
    _run_selfcheck(
        app, "render_camera", "render.camera", "орбита держит дистанцию, пути через ключи"
    )


@register_mode(
    name="render_spectrum",
    title="Цвета звёзд",
    category="Рендер",
    icon="🎨",
    order=40,
    description="чёрное тело → CIE → sRGB",
)
def mode_render_spectrum(app: App):
    _run_selfcheck(
        app, "render_spectrum", "render.spectrum", "Солнце белое, M-карлик красный, O — голубая"
    )


@register_mode(
    name="render_ascii_sky",
    title="Карта неба (ASCII)",
    category="Рендер",
    icon="🌐",
    order=60,
    description="стереографическая проекция, 25 звёзд",
)
def mode_render_ascii_sky(app: App):
    _run_selfcheck(
        app, "render_ascii_sky", "render.ascii_sky", "конформность, зенит в центре, линии Ориона"
    )


# ═══════════════════════════════════════════════════════════════════════════
# ОТЧЁТЫ (3 режима)
# ═══════════════════════════════════════════════════════════════════════════
@register_mode(
    name="reports_xlsx",
    title="Отчёт XLSX",
    category="Отчёты",
    icon="📊",
    order=10,
    description="OOXML-книга без openpyxl (stdlib)",
)
def mode_reports_xlsx(app: App):
    _run_selfcheck(
        app, "reports_xlsx", "reports.writers.xlsx_writer", "валидация zip/XML + чтение openpyxl"
    )


@register_mode(
    name="reports_pptx",
    title="Отчёт PPTX",
    category="Отчёты",
    icon="📽️",
    order=20,
    description="OOXML-презентация со слайдами и PNG",
)
def mode_reports_pptx(app: App):
    _run_selfcheck(
        app, "reports_pptx", "reports.writers.pptx_writer", "валидация zip + чтение python-pptx"
    )


@register_mode(
    name="reports_odt",
    title="Отчёт ODT",
    category="Отчёты",
    icon="📄",
    order=30,
    description="OpenDocument Text (soffice валидирует)",
)
def mode_reports_odt(app: App):
    _run_selfcheck(
        app,
        "reports_odt",
        "reports.writers.odt_writer",
        "mimetype STORED, XML-части, конверсия в PDF",
    )


@register_mode(
    name="science_cosmology",
    title="Космология ΛCDM",
    category="Наука",
    icon="🔭",
    order=150,
    description="возраст 13.80 Gyr, d_L(z=1), закон Хаббла",
)
def mode_science_cosmology(app: App):
    _run_selfcheck(
        app,
        "science_cosmology",
        "realism.cosmology",
        "Planck 2018: возраст, световые расстояния, E(z)",
    )


@register_mode(
    name="science_maneuvers",
    title="Орбитальные манёвры",
    category="Наука",
    icon="🧮",
    order=160,
    description="биэллиптика (порог 11.94), фазирование, драг",
)
def mode_science_maneuvers(app: App):
    _run_selfcheck(
        app,
        "science_maneuvers",
        "lab.orbital_maneuvers",
        "порог биэллиптики, Δv наклонения, vis-viva",
    )


@register_mode(
    name="science_almanac",
    title="Альманах",
    category="Наука",
    icon="📅",
    order=170,
    description="фазы Луны, восходы, полярные дни, сезоны",
)
def mode_science_almanac(app: App):
    _run_selfcheck(
        app, "science_almanac", "realism.almanac", "синодический месяц, рефракция, арктический круг"
    )


@register_mode(
    name="analysis_lightcurves",
    title="Кривые блеска транзитов",
    category="Анализ",
    icon="📉",
    order=25,
    description="лимбовое затемнение, Мандель-Аголь, fit r/R",
)
def mode_analysis_lightcurves(app: App):
    _run_selfcheck(
        app,
        "analysis_lightcurves",
        "analysis.lightcurves",
        "δ = (r/R)² без затемнения; fit на сетке диска",
    )


@register_mode(
    name="analysis_corner",
    title="Corner-диаграммы",
    category="Анализ",
    icon="🔺",
    order=26,
    description="маргиналы, HPD 68/95%, ASCII-рендер",
)
def mode_analysis_corner(app: App):
    _run_selfcheck(
        app,
        "analysis_corner",
        "analysis.corner_plots",
        "гауссовы цепи: пик, ширина HPD, 2D-плотность",
    )


@register_mode(
    name="render_compositor",
    title="Композитор кадров",
    category="Рендер",
    icon="🖼️",
    order=50,
    description="слои: звёзды/тела/сетка/виньетка, blend",
)
def mode_render_compositor(app: App):
    _run_selfcheck(
        app, "render_compositor", "render.frame_compositor", "аддитив/альфа/z-порядок, экспорт PNG"
    )


@register_mode(
    name="science_solar_system",
    title="Симуляция Солнечной системы",
    category="Наука",
    icon="🌞",
    order=180,
    description="8 планет из каталога, периоды, синодика",
)
def mode_science_solar_system(app: App):
    _run_selfcheck(
        app,
        "science_solar_system",
        "lab.solar_system_sim",
        "Кеплер-III против NASA, синодика, бюджет момента",
    )


@register_mode(
    name="science_eclipses",
    title="Затмения и Сарос",
    category="Наука",
    icon="🌑",
    order=190,
    description="конус тени, Сарос 6585.32 сут, затменный год",
)
def mode_science_eclipses(app: App):
    _run_selfcheck(
        app,
        "science_eclipses",
        "realism.eclipse_predictor",
        "Сарос 223 синодических, сезон 173.31 сут",
    )


@register_mode(
    name="science_trojans",
    title="Троянцы Лагранжа",
    category="Наука",
    icon="⚔️",
    order=200,
    description="критерий Рабе 0.03852, либрация Троянцев",
)
def mode_science_trojans(app: App):
    _run_selfcheck(app, "science_trojans", "lab.trojan_points", "L4/L5 устойчивы при μ < 0.03852")


@register_mode(
    name="science_bright_stars",
    title="Каталог ярких звёзд",
    category="Наука",
    icon="✴️",
    order=210,
    description="топ-25 Hipparcos: RA/Dec/mag, видимость",
)
def mode_science_bright_stars(app: App):
    _run_selfcheck(
        app,
        "science_bright_stars",
        "realism.bright_stars",
        "Сириус −1.46ᵐ, Вега циркумполярна на 60° с.ш.",
    )


@register_mode(
    name="science_hamiltonian",
    title="Гамильтоновы интеграторы",
    category="Наука",
    icon="⚙️",
    order=220,
    description="KDK/Yoshida-4/Suzuki-6, дрейф энергии",
)
def mode_science_hamiltonian(app: App):
    _run_selfcheck(
        app,
        "science_hamiltonian",
        "lab.hamiltonian_split",
        "Yoshida-4 на 3 порядка точнее leapfrog",
    )


@register_mode(
    name="analysis_entropy",
    title="Энтропии рядов",
    category="Анализ",
    icon="🎰",
    order=27,
    description="Шеннон, Bandt-Pompe, SampleEn, суррогаты",
)
def mode_analysis_entropy(app: App):
    _run_selfcheck(
        app, "analysis_entropy", "analysis.entropy", "шум > сигнал; суррогатный тест Theiler"
    )


@register_mode(
    name="tools_data_export",
    title="Экспорт данных",
    category="Инструменты",
    icon="📤",
    order=40,
    description="CSV/TSV/JSONL/Markdown/LaTeX/ASCII",
)
def mode_tools_data_export(app: App):
    _run_selfcheck(
        app, "tools_data_export", "tools.data_exporter", "RFC 4180 roundtrip, booktabs, GFM"
    )


@register_mode(
    name="science_spacecraft",
    title="КА: ориентация и маховики",
    category="Наука",
    icon="🛸",
    order=230,
    description="кватернионы, уравнения Эйлера, ПИД-разворот",
)
def mode_science_spacecraft(app: App):
    _run_selfcheck(
        app, "science_spacecraft", "lab.spacecraft", "90° разворот за 12 с; |H| сохраняется"
    )


@register_mode(
    name="science_observatory",
    title="Обсерватория: сессии",
    category="Наука",
    icon="🔭",
    order=240,
    description="планировщик наблюдений, airmass, SNR",
)
def mode_science_observatory(app: App):
    _run_selfcheck(
        app,
        "science_observatory",
        "realism.observatory",
        "окна видимости, Кастен-Янг, фотометрия CCD",
    )


@register_mode(
    name="science_spaceweather",
    title="Космическая погода",
    category="Наука",
    icon="🌪️",
    order=250,
    description="Паркер 47°, Kp/Ap, магнитопауза, ГКЛ",
)
def mode_science_spaceweather(app: App):
    _run_selfcheck(
        app,
        "science_spaceweather",
        "realism.space_weather",
        "спираль Паркера, шкалы NOAA G1-G5, вспышки GOES",
    )


@register_mode(
    name="tools_pipeline",
    title="Конвейер данных",
    category="Инструменты",
    icon="⚙️",
    order=50,
    description="DAG шагов, кэш, изоляция сбоев, provenance",
)
def mode_tools_pipeline(app: App):
    _run_selfcheck(
        app, "tools_pipeline", "analysis.pipeline", "топология Кана, мемоизация, контракты"
    )


# ═══════════════════════════════════════════════════════════════════════════
# ИНСТРУМЕНТЫ (3 режима)
# ═══════════════════════════════════════════════════════════════════════════
@register_mode(
    name="tools_benchmark",
    title="Бенчмарк B1–B8",
    category="Инструменты",
    icon="⏲️",
    order=10,
    description="интеграторы, дерево, рендер, кодеки, отчёты",
)
def mode_tools_benchmark(app: App):
    from analysis.benchmark import run_all, save_protocol

    print(colorize("\n  БЕНЧМАРК-КОМПЛЕКС B1–B8", cyn, True))
    result = run_all()
    run_dir = app.new_run_dir("tools_benchmark")
    path = os.path.join(run_dir, "benchmark.json")
    save_protocol(result, path)
    print(
        f"  {verdict_icon(result['all_pass'])} "
        f"{result['passed']}/{result['total']} сценариев за "
        f"{result['total_s']:.1f} с"
    )
    print(f"  протокол: {path}")


@register_mode(
    name="tools_apiref",
    title="API-справочник",
    category="Инструменты",
    icon="📚",
    order=20,
    description="автогенерация docs/API.md из AST",
)
def mode_tools_apiref(app: App):

    _run_selfcheck(
        app,
        "tools_apiref",
        "analysis.api_reference",
        "65+ модулей, покрытие docstrings, реальные сигнатуры",
    )


@register_mode(
    name="tools_gate",
    title="Quality gate (полный CI)",
    category="Инструменты",
    icon="🛡️",
    order=30,
    description="selftest + приёмка + 30 self-check + гигиена",
)
def mode_tools_gate(app: App):
    from tools.quality_gate import run_full_gate, print_gate

    print(colorize("\n  QUALITY GATE", cyn, True))
    gate = run_full_gate(json_path=os.path.join(app.new_run_dir("tools_gate"), "quality_gate.json"))
    print_gate(gate)
