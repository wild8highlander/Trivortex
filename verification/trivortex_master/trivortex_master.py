#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║  TRIVORTEX MASTER — лабораторный комплекс N тел · v1.0.0 · AURORA       ║
║  лаборатория N тел · планирование траекторий · 2D/3D/4D · отчёты 7 fmt  ║
╚══════════════════════════════════════════════════════════════════════════╝

Единая точка входа. Работает на чистом Python 3.10+ (stdlib-first);
numpy/matplotlib/imageio/REBOUND/Dedalus/fpdf2 — опциональные усилители.

Запуск:
    python3 trivortex_master.py                # интерактивное меню
    python3 trivortex_master.py --selftest     # структурные тесты S1–S12
    python3 trivortex_master.py --preset inner_solar --simulate --render --report
    python3 trivortex_master.py --profile quick --banner-only
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
import traceback

# путь к пакету — сам файл лежит в корне trivortex_master/
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# инъекция адаптеров REBOUND/Dedalus/Custom в диспетчер движков
import realism  # noqa: F401  (регистрирует движки при импорте)
import modes_extra  # noqa: F401  (34 доп. режима меню)

import core.registry as R
from core.registry import REGISTRY, register_mode
from core.config import MasterConfig, UnphysicalConfiguration, from_profile, \
    resolve_paths, PROFILES
from render.hud import (banner, print_banner, orn, kv, colorize, gry, wht,
                        cyn, ylw, grn, red, mag, org, verdict_icon,
                        warn_plate, ProgressBar, Monitor, detect_color_mode,
                        color_off, RESET)

VERSION = "2.0.0"


# ═══════════════════════════════════════════════════════════════════════════
# Глобальное состояние приложения
# ═══════════════════════════════════════════════════════════════════════════
class App:
    """Сессия лаборатории: конфиг, сцена, последние результаты."""

    def __init__(self):
        self.config = resolve_paths(from_profile("standard"), ROOT)
        self.scene = None
        self.last_sim = None
        self.last_charts: list[str] = []
        self.last_reports: dict[str, str] = {}
        self.runs_dir = os.path.join(ROOT, "runs")
        os.makedirs(self.runs_dir, exist_ok=True)
        self.session_log = os.path.join(
            self.runs_dir,
            f"session_{_dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        self._log("сессия начата")

    def _log(self, msg: str) -> None:
        try:
            with open(self.session_log, "a", encoding="utf-8") as fh:
                fh.write(f"{_dt.datetime.now().isoformat(timespec='seconds')}"
                         f"  {msg}\n")
        except OSError:
            pass

    def new_run_dir(self, tag: str) -> str:
        d = os.path.join(self.runs_dir,
                         f"run_{tag}_{_dt.datetime.now().strftime('%Y%m%d_%H%M%S')}")
        os.makedirs(d, exist_ok=True)
        return d

    def require_scene(self):
        if self.scene is None:
            print(colorize("\n  сцена не создана — сначала пункт 1 (Лаборатория)",
                           org))
            return None
        return self.scene


APP = App()


# ═══════════════════════════════════════════════════════════════════════════
# Меню: категории
# ═══════════════════════════════════════════════════════════════════════════

# ── 1. ЛАБОРАТОРИЯ ──────────────────────────────────────────────────────────
@register_mode(name="scene_create", title="Создать сцену из пресета",
               category="Лаборатория", icon="◈", order=10,
               description="Пресеты: Солнечная система, Лагранж, вихревые кольца…")
def mode_scene_create(app: App):
    from lab.presets import load_presets, build_preset
    presets = load_presets()
    print(colorize("\n  ПРЕСЕТЫ СЦЕН", cyn, True))
    for i, p in enumerate(presets, 1):
        n = len(p.get("bodies", []))
        flag = colorize(" ⚠ вне физической вселенной", red) if p.get("unphysical") else ""
        print(f"  {i:2d}. {p['name']} (N={n}){flag}")
        print(f"      {p.get('description', '')[:90]}")
    choice = input("\n  номер пресета (0 — отмена): ").strip()
    if not choice.isdigit() or int(choice) == 0:
        return
    idx = int(choice) - 1
    if idx < 0 or idx >= len(presets):
        print(colorize("  нет такого пресета", red))
        return
    preset = presets[idx]
    try:
        if preset.get("unphysical"):
            ok = input(colorize(
                "  пресет вне физической вселенной (N>8); включить "
                "allow_unphysical? y/n: ", ylw)).strip().lower()
            if ok != "y":
                print("  отмена")
                return
            app.config.allow_unphysical = True
        app.scene = build_preset(preset["id"], app.config)
        app._log(f"сцена создана: {preset['id']} N={app.scene.n}")
        print(colorize(f"\n  ✓ сцена «{app.scene.name}»: N={app.scene.n}, "
                       f"dt={app.scene.dt:.3g}", grn, True))
        if app.scene.unphysical_flag:
            print(colorize(
                "  ⚠ N вне физической вселенной модели (порог Хавелока: "
                "кольцо устойчиво при N≤7; N=8 → max Re λ = +0.4502)", red, True))
        rep = app.scene.validate()
        for w in rep.warnings[:5]:
            print(colorize(f"  ⚠ {w}", ylw))
    except (UnphysicalConfiguration, KeyError, ValueError) as exc:
        print(colorize(f"\n  ✗ {exc}", red))


@register_mode(name="scene_custom", title="Своя сцена (N тел вручную)",
               category="Лаборатория", icon="◇", order=20,
               description="Задать тела по одному: масса, радиус, позиция, скорость")
def mode_scene_custom(app: App):
    from lab.body import Body
    from lab.scene import Scene
    sc = Scene(app.config, name="custom")
    print(colorize("\n  СБОРКА СЦЕНЫ ВРУЧНУЮ (пустой ввод — закончить)", cyn, True))
    print(f"  допустимо N = 3…{app.config.max_bodies}"
          + (colorize(" (8 — только с allow_unphysical)", gry) if not app.config.allow_unphysical else ""))
    n = 0
    while True:
        if n >= 3:
            cont = input(f"\n  тел: {n}. Добавить ещё? (y/n): ").strip().lower()
            if cont != "y":
                break
        try:
            name = input(f"  тело {n + 1}: имя = ").strip()
            if not name:
                if n >= 3:
                    break
                print(colorize("  имя обязательно (пока тел < 3)", ylw))
                continue
            mass = float(input("    масса (кг) [1e22]: ") or 1e22)
            radius = float(input("    радиус (м) [1e5]: ") or 1e5)
            pos = input("    позиция x,y,z (м) [0,0,0]: ").strip() or "0,0,0"
            vel = input("    скорость vx,vy,vz (м/с) [0,0,0]: ").strip() or "0,0,0"
            pos_t = tuple(float(x) for x in pos.split(","))
            vel_t = tuple(float(x) for x in vel.split(","))
            b = Body(id=name.lower().replace(" ", "_"), name=name,
                     mass=mass, radius=radius,
                     position=pos_t, velocity=vel_t,
                     color=["#4FD1C5", "#E8C766", "#A78BFA", "#7DD3FC",
                            "#FB7185", "#34D399", "#FF9A76", "#C8D8D8"][n % 8],
                     type="synthetic", source="custom")
            sc.add_body(b)
            n += 1
        except UnphysicalConfiguration as exc:
            print(colorize(f"\n  ✗ {exc}", red, True))
            break
        except ValueError as exc:
            print(colorize(f"  ✗ неверное число: {exc}", red))
    if n >= 3:
        sc.dt = max(1e-3, 1e-7 * max(abs(c) for b in sc.bodies
                                      for c in b.position) or 1e-3)
        app.scene = sc
        app._log(f"своя сцена: N={n}")
        print(colorize(f"\n  ✓ сцена собрана: N={n}, dt={sc.dt:.3g}", grn, True))
    else:
        print(colorize("  нужно минимум 3 тела — сцена отброшена", ylw))


@register_mode(name="scene_info", title="Показать текущую сцену",
               category="Лаборатория", icon="☰", order=30,
               description="Тела, массы, энергии, предупреждения валидатора")
def mode_scene_info(app: App):
    sc = app.require_scene()
    if not sc:
        return
    from realism.validator import realism_report
    print(colorize(f"\n  СЦЕНА «{sc.name}» (N={sc.n}, t={sc.t:.3g})", cyn, True))
    for b in sc.bodies:
        print(kv(b.name, f"m={b.mass:.3g} кг  r={b.radius:.3g} м  "
                         f"v={b.speed():.3g}"))
    print(kv("полная масса", f"{sc.total_mass():.4g} кг"))
    print(kv("энергия", f"{sc.total_energy():.4g} Дж"))
    rep = realism_report(sc)
    print(kv("физичность", "да" if rep["physical"] else "НЕТ",
             ) + ("" if rep["physical"] else colorize("  ⚠", red)))
    for w in rep["warnings"][:6]:
        print(colorize(f"  ⚠ {w['message']}", ylw))


@register_mode(name="scene_catalog", title="Каталог объектов (поиск)",
               category="Лаборатория", icon="★", order=40,
               description="258 объектов с источниками: планеты, луны, экзопланеты…")
def mode_scene_catalog(app: App):
    from lab.presets import search_catalog, catalog_summary, load_catalog
    cat = load_catalog()
    print(colorize("\n  КАТАЛОГ: " + ", ".join(
        f"{k}: {v}" for k, v in catalog_summary(cat).items()), gry))
    q = input("  поиск (часть имени/тип/host; пусто — первые 15): ").strip()
    from lab.presets import catalog_objects
    recs = search_catalog(q) if q else catalog_objects(cat)[:15]
    for rec in recs[:20]:
        print(f"  {rec['id']:<28} {rec['name']:<26} {rec['type']:<12} "
              f"{rec['mass_kg']:.2g} кг")


# ── 2. ВИЗУАЛИЗАЦИЯ ────────────────────────────────────────────────────────
@register_mode(name="viz_render", title="Визуализировать (2D/3D/4D)",
               category="Визуализация", icon="◐", order=10,
               description="Графики траекторий выбранным бэкендом")
def mode_viz_render(app: App):
    sc = app.require_scene()
    if not sc:
        return
    if not sc.trajectory_history:
        print(colorize("  у сцены нет истории — сначала прогоните симуляцию",
                       ylw))
        return
    from render.engine import available_backends, get_backend
    backends = available_backends()
    print(colorize("\n  бэкенды: ", cyn) + ", ".join(backends))
    b = input(f"  бэкенд [{app.config.render_backend}]: ").strip() \
        or app.config.render_backend
    run_dir = app.new_run_dir("viz")
    try:
        eng = get_backend(b, app.config)
        eng.setup(sc)
        if hasattr(eng, "render_trajectory"):
            outs = eng.render_trajectory(run_dir, prefix="scene")
        else:
            eng.draw_frame(sc.t / 2)
            ext = "txt" if b == "ascii" else "png"
            p = os.path.join(run_dir, f"scene_frame.{ext}")
            eng.save_frame(p)
            outs = [p]
        app.last_charts = outs
        app._log(f"визуализация {b}: {len(outs)} файлов")
        print(colorize(f"\n  ✓ создано {len(outs)} файлов в {run_dir}", grn, True))
        for p in outs:
            print(f"    {os.path.basename(p)}  "
                  f"({os.path.getsize(p)} байт)")
    except Exception as exc:
        print(colorize(f"  ✗ {type(exc).__name__}: {exc}", red))


@register_mode(name="viz_ascii", title="ASCII-кадр в терминал",
               category="Визуализация", icon="▚", order=20,
               description="Мгновенный терминальный рендер текущего состояния")
def mode_viz_ascii(app: App):
    sc = app.require_scene()
    if not sc:
        return
    from render.backend_ascii import render_ascii, print_ascii
    bodies = [dict(position=b.position, radius=max(b.radius / 1e9, 0.05),
                   color=b.color, label=b.name) for b in sc.bodies]
    trails = None
    if sc.trajectory_history:
        trails = [[(s[i][0], s[i][1], s[i][2])
                   for s in sc.trajectory_history[::max(1, len(sc.trajectory_history)//12)]]
                  for i in range(len(sc.bodies))]
    lines = render_ascii(bodies, width=78, height=24, trails=trails)
    print_ascii(lines)


# ── 3. СИМУЛЯЦИИ ───────────────────────────────────────────────────────────
@register_mode(name="sim_run", title="Прогнать симуляцию",
               category="Симуляции", icon="▶", order=10,
               description="Движок, шаги, прогресс-бар, детекторы событий")
def mode_sim_run(app: App):
    sc = app.require_scene()
    if not sc:
        return
    from lab.physics import run_simulation, engine_registry
    engines = sorted(engine_registry().keys())
    print(colorize("\n  движки: ", cyn) + ", ".join(engines))
    eng = input(f"  движок [{app.config.physics_engine}]: ").strip() \
        or app.config.physics_engine
    steps_s = input(f"  шагов [{app.config.n_steps}]: ").strip()
    steps = int(steps_s) if steps_s.isdigit() else app.config.n_steps
    try:
        sc.apply_engine(eng)
    except (ValueError, Exception) as exc:
        print(colorize(f"  движок недоступен: {exc} — используется native",
                       ylw))
    bar = ProgressBar(f"симуляция «{sc.name}»", steps,
                      monitor=Monitor() if app.config.monitor_inline else None)
    sim = run_simulation(sc, n_steps=steps, progress=bar)
    app.last_sim = sim
    app._log(f"симуляция {sim['engine']}: {steps} шагов, "
             f"дрейф {sim['energy_drift_rel']:.1e}")
    bar.finish(f"t={sim['t_final']:.3g}")
    print(colorize(f"\n  ✓ движок {sim['engine']}, t={sim['t_final']:.4g}, "
                   f"дрейф энергии {sim['energy_drift_rel']:.1e}", grn, True))
    if sim["new_events"]:
        print(colorize(f"  события ({len(sim['new_events'])}):", ylw))
        for e in sim["new_events"][:6]:
            print(f"    {e['kind']}: {e['detail'][:70]}")
    if sc.unphysical_flag:
        print(colorize("  ⚠ конфигурация вне физической вселенной модели "
                       "(порог Хавелока, N=8: max Re λ = +0.4502)", red, True))


@register_mode(name="sim_trajectory", title="Запланировать траекторию",
               category="Симуляции", icon="✳", order=20,
               description="Теорема 3.1, Лагранж, figure-eight, Кеплер, waypoints")
def mode_sim_trajectory(app: App):
    from lab.trajectory import get_planner
    planners = ["theorem31 (Теорема 3.1: дышащее кольцо)",
                "lagrange (равносторонний треугольник)",
                "figure_eight (Ченшинер–Монтгомери)",
                "ring (вихревое кольцо N=2..8, Кирхгоф)",
                "orbit (кеплерова орбита)"]
    print(colorize("\n  ПЛАНИРОВЩИКИ", cyn, True))
    for p in planners:
        print(f"  • {p}")
    choice = input("  какой (имя в скобках): ").strip().split(" ")[0]
    run_dir = app.new_run_dir("traj")
    try:
        ap = get_planner("analytic")
        if choice == "theorem31":
            traj = ap.theorem31(n_steps=300)
        elif choice == "lagrange":
            traj = ap.lagrange(n_steps=300)
        elif choice == "figure_eight":
            traj = ap.figure_eight(n_steps=400)
        elif choice == "ring":
            n = input("  N вихрей (2–8) [5]: ").strip()
            n = int(n) if n.isdigit() else 5
            kp = get_planner("kirchhoff")
            traj = kp.ring(N=max(2, min(8, n)), n_steps=300)
        elif choice == "orbit":
            kp = get_planner("kepler")
            traj = kp.orbit(n_steps=300)
        else:
            print(colorize("  неизвестный планировщик", red))
            return
        traj.to_json(os.path.join(run_dir, "trajectory.json"))
        traj.to_csv(os.path.join(run_dir, "trajectory.csv"))
        app._log(f"траектория {choice}: {len(traj.times)} кадров")
        print(colorize(f"\n  ✓ {choice}: {len(traj.times)} кадров → {run_dir}",
                       grn, True))
        # сразу покажем график, если mpl есть
        try:
            from render.backend_mpl import plot_2d, HAVE_MPL
            if HAVE_MPL:
                plot_2d(traj, os.path.join(run_dir, "traj_2d.png"),
                        style="neon_dark", title=choice)
                app.last_charts = [os.path.join(run_dir, "traj_2d.png")]
                print(colorize("  график: traj_2d.png", grn))
        except ImportError:
            pass
    except Exception as exc:
        print(colorize(f"  ✗ {type(exc).__name__}: {exc}", red))


# ── 4. АНИМАЦИИ ────────────────────────────────────────────────────────────
@register_mode(name="anim_gif", title="Собрать GIF-анимацию",
               category="Анимации", icon="🎞", order=10,
               description="Собственный LZW-кодер GIF89a, без зависимостей")
def mode_anim_gif(app: App):
    sc = app.require_scene()
    if not sc:
        return
    if not sc.trajectory_history:
        print(colorize("  нет истории — прогоните симуляцию", ylw))
        return
    from render.animator import animate_scene
    frames_s = input("  кадров [36]: ").strip()
    frames = int(frames_s) if frames_s.isdigit() else 36
    w_s = input("  ширина [480]: ").strip()
    w = int(w_s) if w_s.isdigit() else 480
    h = int(w * 0.75)
    run_dir = app.new_run_dir("anim")
    out = os.path.join(run_dir, "animation.gif")
    try:
        res = animate_scene(sc, out, n_frames=frames, fps=12,
                            backend="pure", width=w, height=h)
        app._log(f"gif: {res['bytes']} байт, {res['frames']} кадров")
        print(colorize(f"\n  ✓ GIF: {res['frames']} кадров, {res['bytes']} "
                       f"байт → {out}", grn, True))
    except Exception as exc:
        print(colorize(f"  ✗ {type(exc).__name__}: {exc}", red))


@register_mode(name="anim_mp4", title="Собрать MP4-видео",
               category="Анимации", icon="🎬", order=20,
               description="ffmpeg или imageio (при наличии)")
def mode_anim_mp4(app: App):
    sc = app.require_scene()
    if not sc:
        return
    if not sc.trajectory_history:
        print(colorize("  нет истории — прогоните симуляцию", ylw))
        return
    from render.animator import animate_scene
    run_dir = app.new_run_dir("anim")
    out = os.path.join(run_dir, "animation.mp4")
    try:
        res = animate_scene(sc, out, n_frames=24, fps=10, backend="pure",
                            width=480, height=360, format="mp4")
        app._log(f"mp4: {res['bytes']} байт")
        print(colorize(f"\n  ✓ MP4: {res['bytes']} байт → {out}", grn, True))
    except Exception as exc:
        print(colorize(f"  ✗ {exc}: попробуйте GIF (работает всегда)", red))


# ── 5. АНАЛИЗ ──────────────────────────────────────────────────────────────
@register_mode(name="analysis_selftest", title="Структурные тесты S1–S12",
               category="Анализ", icon="🧪", order=10,
               description="Структуры, направления, зависимости, интегралы V3/V4")
def mode_analysis_selftest(app: App):
    from analysis.tests import run_all
    print(colorize("\n  СТРУКТУРНЫЕ ТЕСТЫ S1–S12", cyn, True))
    summary = run_all()
    mark = verdict_icon(summary["all_pass"])
    print(f"\n  {mark} {summary['passed']}/{summary['total']} пройдено")
    run_dir = app.new_run_dir("selftest")
    with open(os.path.join(run_dir, "selftest.json"), "w",
              encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1)
    print(f"  протокол: {run_dir}/selftest.json")


@register_mode(name="analysis_metrics", title="Метрики текущей сцены",
               category="Анализ", icon="📐", order=20,
               description="Ляпунов, интегралы, расстояния, периоды")
def mode_analysis_metrics(app: App):
    sc = app.require_scene()
    if not sc:
        return
    from analysis.metrics import lyapunov_exponent, integral_drifts, \
        scene_summary_metrics
    print(colorize("\n  МЕТРИКИ", cyn, True))
    lam = lyapunov_exponent(sc, n_steps=min(150, app.config.n_steps))
    verdict = colorize("ХАОС", red, True) if lam["chaotic"] else \
        colorize("регулярно", grn, True)
    print(kv("ляпуновский показатель",
             f"{lam['lyapunov']:.3e} 1/t — {verdict}"))
    drifts = integral_drifts(sc)
    for k, v in drifts.items():
        if isinstance(v, float):
            print(kv(k, f"{v:.2e}"))
        else:
            print(kv(k, str(v)))
    summ = scene_summary_metrics(sc)
    if "distances" in summ:
        d = summ["distances"]
        print(kv("межтелные расстояния",
                 f"min {d['min']:.3g} / max {d['max']:.3g} / mean {d['mean']:.3g}"))


@register_mode(name="analysis_field", title="Полевые исследования",
               category="Анализ", icon="🔬", order=30,
               description="Сканы масса×скорость, кольца Хавелока, бифуркации")
def mode_analysis_field(app: App):
    from analysis import field
    print(colorize("\n  ПОЛЕВЫЕ ИССЛЕДОВАНИЯ", cyn, True))
    print("  1. скан масса × скорость (ньютоновский)")
    print("  2. кольца Хавелока N=2..8 (вихревая устойчивость)")
    choice = input("  что (1/2/оба) [2]: ").strip() or "2"
    run_dir = app.new_run_dir("field")
    results = []
    bar = ProgressBar("полевые исследования", 100)
    try:
        if choice in ("1", "оба"):
            results.append(field.scan_mass_velocity(
                progress=bar,
                output_json=os.path.join(run_dir, "scan_mass_velocity.json")))
            print(colorize(f"  ✓ скан 1: {len(results[-1]['grid'])} узлов, "
                           f"бифуркаций: {len(results[-1]['bifurcations'])}",
                           grn))
        if choice in ("2", "оба"):
            res = field.scan_havelock(
                progress=bar,
                output_json=os.path.join(run_dir, "scan_havelock.json"))
            results.append(res)
            print(colorize(
                f"  ✓ Хавелок: согласие динамики с прогнозом W4 — "
                f"{res['havelock_matches']}/{res['havelock_total']}", grn))
        bar.finish()
    except Exception as exc:
        bar.finish()
        print(colorize(f"  ✗ {type(exc).__name__}: {exc}", red))
        traceback.print_exc()
    app._log(f"полевые исследования: {len(results)} сканов")
    # таблицы в терминал
    from analysis.field import field_tables
    for name, headers, rows in field_tables(results):
        print(colorize(f"\n  {name}", cyn, True))
        from reports.charts import ascii_table
        for line in ascii_table(headers, rows).splitlines():
            print("  " + line)


@register_mode(name="analysis_rmt", title="RMT-статистика спектров",
               category="Анализ", icon="∑", order=40,
               description="⟨r⟩ Джиролами: GUE/GOE/GSE/Poisson (наследие ядра)")
def mode_analysis_rmt(app: App):
    from analysis.rmt import synthetic_ensemble, analyze_spectrum
    import json
    print(colorize("\n  RMT-АНАЛИЗ (наследие trivortex_core, секция 7)", cyn, True))
    kind = input("  ансамбль (goe/gue) [goe]: ").strip() or "goe"
    evs = synthetic_ensemble(kind, n=50, seed=7)
    res = analyze_spectrum(evs, degree=5)
    print(kv("уровней", str(res.get("n_levels"))))
    print(kv("⟨r⟩", f"{res.get('r_mean', float('nan')):.4f}"))
    print(kv("классификация", str(res.get("ensemble"))))
    print(kv("эталоны", "GUE 0.5996 · GOE 0.5307 · GSE 0.6762 · Poisson 0.3863"))
    run_dir = app.new_run_dir("rmt")
    with open(os.path.join(run_dir, "rmt.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, default=str, indent=1)
    print(colorize(f"  протокол: {run_dir}/rmt.json", gry))


# ── 6. ОТЧЁТЫ ──────────────────────────────────────────────────────────────
@register_mode(name="reports_generate", title="Сгенерировать отчёты",
               category="Отчёты", icon="📄", order=10,
               description="TXT · MD · HTML · CSV · JSON · DOCX · PDF")
def mode_reports_generate(app: App):
    sc = app.require_scene()
    if not sc:
        return
    from reports.engine import ReportData, generate_reports, validate_outputs
    print(colorize("\n  форматы: txt md html csv json docx pdf", cyn))
    fmts_s = input("  форматы через пробел [все]: ").strip()
    fmts = fmts_s.split() if fmts_s else ["txt", "md", "html", "csv",
                                          "json", "docx", "pdf"]
    theme = app.config.report_theme
    run_dir = app.new_run_dir("report")
    data = ReportData(f"Отчёт по сцене «{sc.name}»", scene=sc,
                      sim_summary=app.last_sim or {}, config=app.config)
    data.fill_from_scene()
    # графики, если есть
    if sc.trajectory_history:
        try:
            from render.engine import get_backend
            eng = get_backend("mpl", app.config)
            eng.setup(sc)
            charts = eng.render_trajectory(run_dir, prefix="chart")
            for p in charts:
                data.add_chart(p, os.path.basename(p))
            app.last_charts = charts
        except ImportError:
            pass
    # метрики
    from analysis.metrics import scene_summary_metrics
    m = scene_summary_metrics(sc)
    data.extra_sections.append(("Метрики", json.dumps(
        m, ensure_ascii=False, default=str)[:800]))
    written = generate_reports(data, run_dir, formats=fmts, theme=theme)
    problems = validate_outputs(written)
    app.last_reports = written
    app._log(f"отчёты: {', '.join(fmts)} → {run_dir}")
    print(colorize(f"\n  ✓ отчёты в {run_dir}", grn, True))
    for fmt, path in written.items():
        sz = os.path.getsize(path) if os.path.isfile(path) else 0
        print(f"    {fmt:5s} {sz:>8d} байт  {os.path.basename(path)}")
    if problems:
        print(colorize("  ⚠ проблемы: " + "; ".join(problems), ylw))


# ── 7. НАСТРОЙКИ ───────────────────────────────────────────────────────────
@register_mode(name="settings_profile", title="Профиль конфигурации",
               category="Настройки", icon="⚙", order=10,
               description="quick / standard / realistic / research / cinematic / pure_stdlib")
def mode_settings_profile(app: App):
    print(colorize("\n  ПРОФИЛИ", cyn, True))
    for name, params in PROFILES.items():
        print(f"  • {name:<12} " + ", ".join(f"{k}={v}" for k, v in
                                             list(params.items())[:3]))
    choice = input("  профиль [standard]: ").strip() or "standard"
    try:
        allow = app.config.allow_unphysical
        app.config = resolve_paths(from_profile(choice), ROOT)
        app.config.allow_unphysical = allow
        app._log(f"профиль: {choice}")
        print(colorize(f"  ✓ профиль {choice} применён", grn, True))
    except ValueError as exc:
        print(colorize(f"  ✗ {exc}", red))


@register_mode(name="settings_physics", title="Физика реальности",
               category="Настройки", icon="🜨", order=20,
               description="G, dt, шаги, релятивизм 1PN, диссипация, лимиты N")
def mode_settings_physics(app: App):
    c = app.config
    print(colorize("\n  ФИЗИКА РЕАЛЬНОСТИ", cyn, True))
    print(kv("G", f"{c.G:.6e} м³кг⁻¹с⁻²"))
    print(kv("dt", f"{c.dt:.3g}"))
    print(kv("шагов", str(c.n_steps)))
    print(kv("релятивизм 1PN", "вкл" if c.enable_relativity else "выкл"))
    print(kv("диссипация", "вкл" if c.enable_dissipation else "выкл"))
    print(kv("диапазон N", f"{c.min_bodies}…{c.max_bodies}"
                           f" (жёсткий лимит {c.hard_max_bodies})"))
    print(kv("allow_unphysical", "вкл" if c.allow_unphysical else "выкл"))
    what = input("\n  изменить (G/dt/steps/rel/diss/allow/пусто-выход): ").strip()
    try:
        if what == "G":
            c.G = float(input(f"  G [{c.G:g}]: ") or c.G)
        elif what == "dt":
            c.dt = float(input(f"  dt [{c.dt:g}]: ") or c.dt)
        elif what == "steps":
            c.n_steps = int(input(f"  шагов [{c.n_steps}]: ") or c.n_steps)
        elif what == "rel":
            c.enable_relativity = not c.enable_relativity
        elif what == "diss":
            c.enable_dissipation = not c.enable_dissipation
        elif what == "allow":
            c.allow_unphysical = not c.allow_unphysical
            if c.allow_unphysical:
                print(colorize("  ⚠ N=8 теперь разрешён — конфигурации будут "
                               "помечаться «вне физической вселенной»", ylw, True))
        else:
            return
        app._log(f"физика: {what} изменён")
        print(colorize("  ✓ применено", grn))
    except ValueError as exc:
        print(colorize(f"  ✗ {exc}", red))


@register_mode(name="settings_save", title="Сохранить/загрузить конфиг",
               category="Настройки", icon="💾", order=30,
               description="JSON-снимок конфигурации сессии")
def mode_settings_save(app: App):
    what = input("  save/load [save]: ").strip() or "save"
    path = os.path.join(ROOT, "runs", "config.json")
    if what == "save":
        app.config.save(path)
        print(colorize(f"  ✓ конфигурация → {path}", grn))
    else:
        if os.path.isfile(path):
            app.config = resolve_paths(MasterConfig.load(path), ROOT)
            print(colorize("  ✓ конфигурация загружена", grn))
        else:
            print(colorize("  снимка нет", ylw))


# ── 8. СПРАВКА ─────────────────────────────────────────────────────────────
@register_mode(name="help_engines", title="Статус движков и зависимостей",
               category="Справка", icon="♥", order=10,
               description="Что доступно, что опционально, что сделать")
def mode_help_engines(app: App):
    from core.registry import engine_status_lines
    from render.engine import available_backends
    from core import bridge
    print(colorize("\n  СТАТУС ДВИЖКОВ", cyn, True))
    for mark, label, why in engine_status_lines():
        color = grn if mark == "✓" else gry
        line = f"  [{mark}] {label}"
        if why:
            line += colorize(f" — {why}", gry)
        print(colorize(line, color))
    print(colorize(f"\n  графические бэкенды: {', '.join(available_backends())}",
                   wht))
    st = bridge.health_check()
    print(colorize(f"  ядро Trivortex: "
                   + ("найдено — лестница V1–V4 доступна" if st.available
                      else "не найдено (автономный режим)"),
                   grn if st.available else ylw))


@register_mode(name="help_literature", title="Литература и источники",
               category="Справка", icon="📚", order=20,
               description="Аннотированный список: ядро, движки, данные, классика")
def mode_help_literature(app: App):
    path = os.path.join(ROOT, "data", "literature.md")
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        # первые ~40 строк
        lines = text.splitlines()
        print(colorize("\n  " + "ЛИТЕРАТУРА (первые позиции)", cyn, True))
        shown = 0
        for ln in lines:
            if ln.startswith(("1.", "2.", "3.", "7.", "8.", "9.", "15.", "16.")):
                print("  " + ln[:100])
                shown += 1
            if shown >= 8:
                break
        print(colorize(f"\n  полный список: {path}", gry))
    else:
        print(colorize("  literature.md не найден", ylw))


@register_mode(name="help_about", title="О комплексе",
               category="Справка", icon="ℹ", order=30,
               description="Версия, объём, философия stdlib-first")
def mode_help_about(app: App):
    total_lines = 0
    for base, _dirs, files in os.walk(ROOT):
        if "__pycache__" in base or ".git" in base:
            continue
        for f in files:
            if f.endswith(".py"):
                try:
                    with open(os.path.join(base, f), encoding="utf-8") as fh:
                        total_lines += sum(1 for _ in fh)
                except OSError:
                    pass
    print(colorize("\n  TRIVORTEX MASTER v" + VERSION + " · AURORA", cyn, True))
    print(kv("строк Python", f"{total_lines:,}"))
    print(kv("философия", "stdlib-first: всё работает без внешних пакетов"))
    print(kv("диапазон N", "3–7; 8 — с флагом (порог Хавелока +0.4502)"))
    print(kv("форматы отчётов", "TXT MD HTML CSV JSON DOCX PDF"))
    print(kv("GIF", "собственный LZW-кодер GIF89a — без imageio"))
    print(kv("PNG", "собственный DEFLATE+фильтры — без Pillow"))
    print(kv("литература", "data/literature.md — 21 источник с URL/DOI"))


# ═══════════════════════════════════════════════════════════════════════════
# Отрисовка меню
# ═══════════════════════════════════════════════════════════════════════════
def print_menu() -> None:
    print()
    print(colorize("┌── ГЛАВНОЕ МЕНЮ " + "─" * 45 + "┐", mag, True))
    counter = 1
    global _MENU_INDEX
    _MENU_INDEX = {}
    for cat in REGISTRY.menu_spec():
        print(colorize(f"│ ▸ {cat['category']}", mag, True))
        for item in cat["items"]:
            key = str(counter)
            _MENU_INDEX[key] = item["name"]
            icon = item["icon"]
            title = item["title"]
            if not item["available"]:
                title += colorize("  (недоступно: "
                                  + "; ".join(item["blocked_reasons"])[:40]
                                  + ")", gry)
            print(f"│  {colorize(key, ylw, True)}  {icon} {title}")
            counter += 1
    print(colorize("│  " + colorize("0", ylw, True) + "  ✖ Выход", wht))
    print(colorize("└" + "─" * 60 + "┘", mag, True))


_MENU_INDEX: dict[str, str] = {}


def interactive() -> int:
    """Главный интерактивный цикл; EOF-safe, Ctrl-C-safe."""
    detect_color_mode()
    print_banner(VERSION, "лаборатория N тел · траектории · 2D/3D/4D · "
                          "отчёты 7 форматов · stdlib-first")
    from core.registry import engine_status_lines
    marks = "  ".join(f"[{m}]{lbl[:12]}" for m, lbl, _w
                      in engine_status_lines()[:6])
    print(colorize("  движки: " + marks, gry))
    if APP.config.allow_unphysical:
        print(colorize("  ⚠ allow_unphysical: ВКЛ — конфигурации N=8 помечаются",
                       ylw, True))
    empty_reads = 0
    while True:
        print_menu()
        try:
            choice = input("  номер пункта > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  выход")
            break
        if not choice:
            empty_reads += 1
            if empty_reads > 50:
                print("  слишком много пустых вводов — выходим")
                break
            continue
        empty_reads = 0
        if choice in ("0", "q", "q!", "exit", "quit", "выход"):
            break
        mode_name = _MENU_INDEX.get(choice)
        if mode_name is None:
            print(colorize(f"  нет пункта {choice}", red))
            continue
        entry = REGISTRY.get(mode_name)
        if entry is None:
            continue
        try:
            entry.callable(APP)
        except KeyboardInterrupt:
            print(colorize("\n  прервано — возврат в меню", ylw))
        except Exception as exc:
            print(colorize(f"\n  ✗ ошибка режима: {type(exc).__name__}: {exc}",
                           red))
            traceback.print_exc(file=sys.stderr)
            APP._log(f"ошибка в {mode_name}: {exc}")
        # пауза, чтобы прочитать вывод
        try:
            input(colorize("\n  Enter — в меню…", gry))
        except (EOFError, KeyboardInterrupt):
            print()
            break
    APP._log("сессия завершена")
    print(colorize("\n  лог сессии: " + APP.session_log, gry))
    return 0


# ═══════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════
def cli(args: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="trivortex_master",
        description="TRIVORTEX MASTER — лабораторный комплекс N тел")
    parser.add_argument("--selftest", action="store_true",
                        help="структурные тесты S1–S12")
    parser.add_argument("--profile", default="standard",
                        choices=list(PROFILES), help="профиль конфигурации")
    parser.add_argument("--preset", help="пресет сцены (id)")
    parser.add_argument("--simulate", action="store_true",
                        help="прогнать симуляцию")
    parser.add_argument("--steps", type=int, default=None)
    parser.add_argument("--render", action="store_true",
                        help="визуализировать (mpl при наличии)")
    parser.add_argument("--gif", action="store_true",
                        help="собрать GIF")
    parser.add_argument("--report", action="store_true",
                        help="отчёты во всех форматах")
    parser.add_argument("--banner-only", action="store_true")
    parser.add_argument("--allow-unphysical", action="store_true",
                        help="разрешить N=8 (вне физической вселенной)")
    parser.add_argument("--no-color", action="store_true")
    ns = parser.parse_args(args)

    if ns.no_color:
        color_off()

    if ns.selftest:
        from analysis.tests import run_all
        summary = run_all()
        return 0 if summary["all_pass"] else 1

    if ns.banner_only:
        print_banner(VERSION)
        return 0

    if not (ns.preset or ns.simulate or ns.render or ns.report or ns.gif):
        return interactive()

    # батч-режим
    APP.config = resolve_paths(from_profile(ns.profile), ROOT)
    if ns.allow_unphysical:
        APP.config.allow_unphysical = True
    if ns.steps:
        APP.config.n_steps = ns.steps
    if ns.preset:
        from lab.presets import build_preset
        try:
            APP.scene = build_preset(ns.preset, APP.config)
            print(f"сцена: {APP.scene.name} (N={APP.scene.n})")
        except (UnphysicalConfiguration, KeyError) as exc:
            print(f"✗ {exc}")
            return 1
    if ns.simulate:
        from lab.physics import run_simulation
        bar = ProgressBar("симуляция", APP.config.n_steps)
        APP.last_sim = run_simulation(APP.scene, progress=bar)
        bar.finish(f"t={APP.last_sim['t_final']:.3g}")
        print(f"дрейф энергии: {APP.last_sim['energy_drift_rel']:.1e}")
    if ns.render:
        mode_viz_render(APP)
    if ns.gif:
        mode_anim_gif(APP)
    if ns.report:
        mode_reports_generate(APP)
    return 0


def main() -> int:
    try:
        return cli(sys.argv[1:])
    except KeyboardInterrupt:
        print("\nпрервано")
        return 130


if __name__ == "__main__":
    sys.exit(main())
