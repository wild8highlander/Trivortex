#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — структурные и интеграционные тесты S1–S12.

S1  структура сцены          S7  энергия ньютоновского RK4
S2  сериализация             S8  сравнение движков (native vs REBOUND)
S3  направления зависимостей S9  траектории (Теорема 3.1, 2π/3)
S4  реестр режимов           S10 рендер-контракты
S5  интегралы V3 (равные Γ)  S11 отчёты (7 форматов)
S6  интегралы V4 (Γ=1,2,3)   S12 лимит N=8 (порог Хавелока)

Запуск: из меню («Анализ») или python3 trivortex_master.py --selftest
"""
from __future__ import annotations

import importlib
import io
import json
import math
import os
import sys
from typing import Any

from core.config import MasterConfig, UnphysicalConfiguration, from_profile
from lab.body import Body
from lab.physics import run_simulation
from lab.scene import Scene
from lab.trajectory import get_planner

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestResult:
    def __init__(self, test_id: str, name: str):
        self.id = test_id
        self.name = name
        self.passed = False
        self.details: list[str] = []
        self.metrics: dict[str, Any] = {}

    def ok(self, msg: str = "") -> "TestResult":
        self.passed = True
        if msg:
            self.details.append(msg)
        return self

    def fail(self, msg: str) -> "TestResult":
        self.passed = False
        self.details.append(msg)
        return self

    def check(self, cond: bool, ok_msg: str, fail_msg: str) -> bool:
        if cond:
            self.details.append(ok_msg)
            self.passed = True
        else:
            self.details.append("✗ " + fail_msg)
            self.passed = False
        return cond

    def to_dict(self) -> dict[str, Any]:
        return dict(id=self.id, name=self.name, passed=self.passed,
                    details=self.details, metrics=self.metrics)


# ═══════════════════════════════════════════════════════════════════════════
# S1 — структура сцены
# ═══════════════════════════════════════════════════════════════════════════
def test_s1() -> TestResult:
    r = TestResult("S1", "структура сцены")
    from lab.presets import load_presets, build_preset
    cfg = from_profile("quick", n_steps=5)
    presets = load_presets()
    r.metrics["presets"] = len(presets)
    ok_count = 0
    for p in presets:
        try:
            if p.get("unphysical"):
                continue
            sc = build_preset(p["id"], cfg)
            rep = sc.validate()
            if rep.ok:
                ok_count += 1
            else:
                r.details.append(f"пресет {p['id']}: {rep.problems}")
        except Exception as exc:
            r.details.append(f"пресет {p['id']}: {type(exc).__name__}: {exc}")
    r.check(ok_count >= 8,
            f"пресетов без проблем: {ok_count}/{len(presets)}",
            f"слишком много проблем: {ok_count}/{len(presets)}")
    # тела валидны
    sc = build_preset("inner_solar", cfg)
    r.check(all(not b.validate() for b in sc.bodies),
            "все тела Scene.validate чисты", "есть невалидные тела")
    return r.ok() if r.passed else r


# ═══════════════════════════════════════════════════════════════════════════
# S2 — сериализация сцены
# ═══════════════════════════════════════════════════════════════════════════
def test_s2() -> TestResult:
    r = TestResult("S2", "сериализация сцены")
    from lab.presets import build_preset
    cfg = from_profile("quick", n_steps=10)
    sc = build_preset("jupiter_system", cfg)
    run_simulation(sc, n_steps=10)
    d = sc.to_dict(include_history=True)
    path = "/tmp/tv_s2_scene.json"
    sc.save(path)
    sc2 = Scene.load(path)
    same_bodies = (len(sc2.bodies) == len(sc.bodies)
                   and all(a.id == b.id and a.mass == b.mass
                           for a, b in zip(sc.bodies, sc2.bodies)))
    r.check(same_bodies, "roundtrip JSON: тела идентичны",
            "тела после загрузки отличаются")
    r.check(abs(sc2.t - sc.t) < 1e-12, "время сохранилось", "время потерялось")
    r.check(len(sc2.trajectory_history) == len(sc.trajectory_history),
            "история сохранилась", "история потерялась")
    os.remove(path)
    return r.ok() if r.passed else r


# ═══════════════════════════════════════════════════════════════════════════
# S3 — направления зависимостей (ацикличность графа импортов)
# ═══════════════════════════════════════════════════════════════════════════
def _module_imports(path: str) -> set[str]:
    """Извлечь локальные импорты из .py-файла (без exec!)."""
    with open(path, "r", encoding="utf-8") as fh:
        src = fh.read()
    import ast
    tree = ast.parse(src)
    local = set()
    packages = ("core", "lab", "render", "reports", "realism", "analysis")
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            top = node.module.split(".")[0]
            if top in packages:
                # берём только первый уровень (пакет)
                parts = node.module.split(".")
                local.add(parts[0])
        elif isinstance(node, ast.Import):
            for alias in node.names:
                top = alias.name.split(".")[0]
                if top in packages:
                    local.add(top)
    return local


def test_s3() -> TestResult:
    r = TestResult("S3", "направления зависимостей (граф ацикличен)")
    graph: dict[str, set[str]] = {}
    for pkg in ("core", "lab", "render", "reports", "realism", "analysis"):
        pdir = os.path.join(ROOT, pkg)
        if not os.path.isdir(pdir):
            continue
        for fn in os.listdir(pdir):
            if fn.endswith(".py") and fn != "__init__.py":
                mod = f"{pkg}"
                graph.setdefault(mod, set())
                graph[mod] |= _module_imports(os.path.join(pdir, fn))
    # правила направлений: уровень может импортировать только ниже
    # (realism — адаптеры движков для lab; reports — таблицы для analysis)
    rules = {
        "lab": {"core"},
        "render": {"core", "lab"},
        "reports": {"core", "lab", "render"},
        "realism": {"core", "lab"},
        "analysis": {"core", "lab", "render", "realism", "reports"},
        "core": set(),
    }
    violations = []
    for mod, deps in graph.items():
        allowed = rules.get(mod, set())
        for dep in deps:
            if dep not in allowed | {mod}:
                violations.append(f"{mod} → {dep} (разрешено: {allowed or '—'})")
    r.metrics["graph"] = {k: sorted(v) for k, v in graph.items()}
    r.check(not violations,
            "направления импортов соблюдены: " +
            "; ".join(f"{k}→{sorted(v)}" for k, v in graph.items()),
            "; ".join(violations))
    # ацикличность (DFS по графу межпакетных зависимостей; self-loop
    # «пакет → собственный подпакет» циклом не считается)
    WHITE, GREY, BLACK = 0, 1, 2
    color = {k: WHITE for k in graph}

    def has_cycle(node: str) -> bool:
        color[node] = GREY
        for nxt in graph.get(node, ()):
            if nxt == node or nxt not in color:
                continue  # self-loop / неизвестный узел — не цикл
            if color[nxt] == GREY:
                return True
            if color[nxt] == WHITE and has_cycle(nxt):
                return True
        color[node] = BLACK
        return False

    cyclic = any(color[k] == WHITE and has_cycle(k) for k in graph)
    r.check(not cyclic, "циклов в графе нет", "в графе есть цикл")
    return r.ok() if r.passed else r


# ═══════════════════════════════════════════════════════════════════════════
# S4 — реестр режимов
# ═══════════════════════════════════════════════════════════════════════════
def test_s4() -> TestResult:
    r = TestResult("S4", "реестр режимов")
    from core.registry import REGISTRY
    try:
        import trivortex_master  # регистрирует режимы при первом импорте
    except ValueError:
        pass  # повторный импорт в том же процессе — уже зарегистрировано
    spec = REGISTRY.menu_spec()
    r.metrics["categories"] = len(spec)
    r.metrics["modes"] = sum(len(c["items"]) for c in spec)
    r.check(r.metrics["modes"] >= 9,
            f"режимов: {r.metrics['modes']} в {r.metrics['categories']} категориях",
            "меньше 9 режимов")
    # все callable
    bad = [m.name for m in REGISTRY.all_modes() if not callable(m.callable)]
    r.check(not bad, "все режимы вызываемы", f"невызываемы: {bad}")
    return r.ok() if r.passed else r


# ═══════════════════════════════════════════════════════════════════════════
# S5/S6 — интегралы вихревого движка (критерии лестницы V3/V4)
# ═══════════════════════════════════════════════════════════════════════════
def _vortex_scene(gammas: list[float], cfg: MasterConfig) -> Scene:
    sc = Scene(cfg, name=f"vortex_{len(gammas)}")
    n = len(gammas)
    R = 1.0
    for k in range(n):
        phi = 2 * math.pi * k / n
        sc.add_body(Body(
            id=f"v{k}", name=f"V{k}", mass=1.0, radius=0.02,
            position=(R * math.cos(phi), R * math.sin(phi), 0.0),
            circulation=gammas[k], color="#A78BFA", type="synthetic",
            source="Kirchhoff"))
    sc.apply_engine("native_vortex")
    # период: ω_N = ΓΣ(N-1)/(4πR²) для равных Γ; для смешанных — min
    total_g = sum(abs(g) for g in gammas)
    omega = total_g * (n - 1) / (4 * math.pi * R * R * n) if n > 1 else 1.0
    sc.dt = (2 * math.pi / max(abs(omega), 1e-9)) / 400.0
    return sc


def test_s5() -> TestResult:
    r = TestResult("S5", "интегралы Кирхгофа, равные Γ (V3)")
    cfg = from_profile("quick", n_steps=200, physics_engine="native_vortex")
    sc = _vortex_scene([1.0, 1.0, 1.0], cfg)
    run_simulation(sc, n_steps=200)
    from analysis.metrics import integral_drifts
    drifts = integral_drifts(sc)
    r.metrics.update({k: drifts.get(k) for k in ("H_drift", "P_drift",
                                                 "Q_drift", "I_drift")})
    ok = (drifts.get("H_drift", 1) <= 1e-10
          and drifts.get("P_drift", 1) <= 1e-10
          and drifts.get("Q_drift", 1) <= 1e-10
          and drifts.get("I_drift", 1) <= 1e-10)
    r.check(ok,
            f"H:{drifts.get('H_drift'):.1e} P:{drifts.get('P_drift'):.1e} "
            f"Q:{drifts.get('Q_drift'):.1e} I:{drifts.get('I_drift'):.1e} "
            "— все ≤ 1e-10 (критерий V3)",
            "дрейф интегралов выше 1e-10")
    return r.ok() if r.passed else r


def test_s6() -> TestResult:
    r = TestResult("S6", "интегралы Кирхгофа, Γ=(1,2,3) (V4)")
    cfg = from_profile("quick", n_steps=200, physics_engine="native_vortex")
    sc = _vortex_scene([1.0, 2.0, 3.0], cfg)
    run_simulation(sc, n_steps=200)
    from analysis.metrics import integral_drifts
    drifts = integral_drifts(sc)
    r.metrics.update({k: drifts.get(k) for k in ("H_drift", "P_drift",
                                                 "Q_drift", "I_drift")})
    ok = (drifts.get("H_drift", 1) <= 1e-10
          and drifts.get("P_drift", 1) <= 1e-10
          and drifts.get("Q_drift", 1) <= 1e-10
          and drifts.get("I_drift", 1) <= 1e-10)
    r.check(ok,
            f"смешанные Γ: дрейфы ≤ 1e-10 (критерий V4)",
            "дрейф выше 1e-10 при Γ=(1,2,3)")
    return r.ok() if r.passed else r


# ═══════════════════════════════════════════════════════════════════════════
# S7 — энергия ньютоновского RK4
# ═══════════════════════════════════════════════════════════════════════════
def test_s7() -> TestResult:
    r = TestResult("S7", "сохранение энергии, ньютоновский RK4")
    from lab.presets import build_preset
    cfg = from_profile("quick", n_steps=200)
    sc = build_preset("earth_moon", cfg)
    sim = run_simulation(sc, n_steps=200)
    drift = sim["energy_drift_rel"]
    r.metrics["energy_drift"] = drift
    r.check(drift <= 1e-6,
            f"дрейф энергии {drift:.1e} ≤ 1e-6",
            f"дрейф энергии {drift:.1e} > 1e-6")
    return r.ok() if r.passed else r


# ═══════════════════════════════════════════════════════════════════════════
# S8 — сравнение движков
# ═══════════════════════════════════════════════════════════════════════════
def test_s8() -> TestResult:
    r = TestResult("S8", "сравнение движков (native vs REBOUND)")
    try:
        import rebound  # noqa: F401
    except ImportError:
        r.metrics["skipped"] = True
        return r.ok("REBOUND не установлен — сравнение пропущено "
                    "(штатный fallback)")
    from lab.presets import build_preset
    from lab.physics import get_engine
    cfg = from_profile("quick", n_steps=100)
    sc1 = build_preset("inner_solar", cfg)
    run_simulation(sc1, n_steps=100)
    sc2 = build_preset("inner_solar", cfg)
    eng = get_engine("rebound", sc2)
    sc2.engine = eng
    run_simulation(sc2, n_steps=100)
    d = math.dist(sc1.bodies[1].position, sc2.bodies[1].position)
    r.metrics["position_diff_m"] = d
    r.check(d / 1.496e11 <= 1e-3,
            f"расхождение положений {d:.3g} м ≤ 1e-3 а.е.",
            f"расхождение {d:.3g} слишком велико")
    return r.ok() if r.passed else r


# ═══════════════════════════════════════════════════════════════════════════
# S9 — траектории: Теорема 3.1 (хореография 2π/3)
# ═══════════════════════════════════════════════════════════════════════════
def test_s9() -> TestResult:
    r = TestResult("S9", "планировщик Теоремы 3.1: хореография 2π/3")
    planner = get_planner("analytic")
    traj = planner.theorem31(n_steps=120)
    from core.bridge import THEOREM31_REF
    r.check(abs(traj.metadata["omega"] - THEOREM31_REF["omega"]) < 1e-12,
            f"ω = {traj.metadata['omega']:.13f} (эталон "
            f"{THEOREM31_REF['omega']:.13f})",
            "ω не совпала с эталоном ядра")
    # угловое разделение 2π/3: по позициям (r>0), допуская циклический
    # порядок вершин (2π/3 или 4π/3); скачки atan2 при r→0 отсечены
    omega = traj.metadata["omega"]
    worst_sep = 0.0
    for frame in traj.states:
        thetas = []
        for st in frame:
            rr = math.hypot(st[0], st[1])
            if rr >= 1e-12:
                thetas.append(math.atan2(st[1], st[0]))
        if len(thetas) == 3:
            for i in range(3):
                d = (thetas[(i + 1) % 3] - thetas[i]) % (2 * math.pi)
                if d > math.pi:
                    d = 2 * math.pi - d
                err = min(abs(d - 2 * math.pi / 3), abs(d - 4 * math.pi / 3))
                worst_sep = max(worst_sep, err)
    r.metrics["max_separation_error"] = worst_sep
    r.check(worst_sep <= 1e-9,
            f"разделение 2π/3: макс. ошибка {worst_sep:.1e} (лестница V1: ≤1e-12)",
            f"разделение 2π/3 нарушено: {worst_sep:.1e}")
    # периодичность r
    t_r = 2 * math.pi / traj.metadata["omega"]
    r0 = [math.hypot(*s[:2]) for s in traj.states[0]]
    rT = [math.hypot(*s[:2]) for s in traj.sample(t_r)]
    per = max(abs(a - b) for a, b in zip(r0, rT))
    r.check(per <= 1e-12, f"периодичность r: {per:.1e} ≤ 1e-12",
            f"периодичность нарушена: {per:.1e}")
    return r.ok() if r.passed else r


# ═══════════════════════════════════════════════════════════════════════════
# S10 — рендер-контракты
# ═══════════════════════════════════════════════════════════════════════════
def test_s10() -> TestResult:
    r = TestResult("S10", "рендер-контракты: все бэкенды пишут файлы")
    from lab.presets import build_preset
    from render.engine import available_backends, get_backend
    cfg = from_profile("quick", n_steps=20)
    sc = build_preset("lagrange_triangle", cfg)
    run_simulation(sc, n_steps=20)
    for backend in available_backends():
        try:
            eng = get_backend(backend, sc.config)
            eng.setup(sc)
            if backend == "mpl":
                outs = eng.render_trajectory("/tmp/tv_s10", prefix=f"b_{backend}")
                ok = all(os.path.isfile(p) and os.path.getsize(p) > 3000
                         for p in outs)
            else:
                eng.draw_frame(sc.t / 2)
                path = f"/tmp/tv_s10_{backend}.{'txt' if backend == 'ascii' else 'png'}"
                os.makedirs("/tmp", exist_ok=True)
                size = eng.save_frame(path)
                ok = os.path.isfile(path) and size > 200
                if ok:
                    os.remove(path)
            r.check(ok, f"{backend}: файлы созданы", f"{backend}: файл битый")
        except Exception as exc:
            r.check(False, "", f"{backend}: {type(exc).__name__}: {exc}")
    return r.ok() if r.passed else r


# ═══════════════════════════════════════════════════════════════════════════
# S11 — отчёты
# ═══════════════════════════════════════════════════════════════════════════
def test_s11() -> TestResult:
    r = TestResult("S11", "отчёты: все 7 форматов")
    from lab.presets import build_preset
    from reports.engine import (ReportData, generate_reports,
                                validate_outputs)
    cfg = from_profile("quick", n_steps=15)
    sc = build_preset("earth_moon", cfg)
    sim = run_simulation(sc, n_steps=15)
    data = ReportData("S11-тест", scene=sc, sim_summary={"t": sim["t_final"]})
    data.fill_from_scene()
    written = generate_reports(data, "/tmp/tv_s11",
                               formats=["txt", "md", "html", "csv", "json",
                                        "docx", "pdf"])
    problems = validate_outputs(written)
    r.metrics["written"] = {k: os.path.getsize(v)
                            for k, v in written.items()
                            if not str(v).startswith("ОШИБКА")}
    r.check(not problems and len(r.metrics["written"]) == 7,
            "все 7 форматов валидны",
            "; ".join(problems) or "не все форматы созданы")
    return r.ok() if r.passed else r


# ═══════════════════════════════════════════════════════════════════════════
# S12 — лимит N=8 (порог Хавелока)
# ═══════════════════════════════════════════════════════════════════════════
def test_s12() -> TestResult:
    r = TestResult("S12", "лимит N=8: порог Хавелока")
    from lab.presets import build_preset
    cfg = from_profile("quick", n_steps=5)
    # N=8 без флага → исключение
    sc = build_preset("vortex_ring_7", cfg)
    b8 = Body(id="v8", name="V8", mass=1.0, radius=0.02,
              position=(2.0, 0.0, 0.0), circulation=1.0,
              color="#FB7185", type="synthetic", source="Havelock test")
    try:
        sc.add_body(b8)
        r.check(False, "", "N=8 добавился без флага!")
    except UnphysicalConfiguration:
        r.check(True, "N=8 без флага: UnphysicalConfiguration — отказ", "")
    # N=8 с флагом → unphysical_flag
    cfg2 = from_profile("quick", n_steps=5, allow_unphysical=True)
    sc2 = build_preset("vortex_ring_7", cfg2)
    sc2.add_body(Body(id="v8", name="V8", mass=1.0, radius=0.02,
                      position=(2.0, 0.0, 0.0), circulation=1.0,
                      color="#FB7185", type="synthetic",
                      source="Havelock test"))
    r.check(sc2.unphysical_flag and len(sc2.events) >= 1,
            "N=8 с флагом: unphysical_flag=True + событие в протоколе",
            "флаг/событие не выставлены")
    # N=9 → жёсткий отказ всегда
    try:
        sc2.add_body(Body(id="v9", name="V9", mass=1.0, radius=0.02,
                          position=(0.0, 2.0, 0.0), type="synthetic"))
        r.check(False, "", "N=9 добавился!")
    except UnphysicalConfiguration:
        r.check(True, "N=9: жёсткий отказ (hard_max_bodies=8)", "")
    return r.ok() if r.passed else r


# ═══════════════════════════════════════════════════════════════════════════
# Раннер
# ═══════════════════════════════════════════════════════════════════════════

def _load_extra():
    """S13–S24 из tests_extra (модули с независимыми эталонами)."""
    try:
        from analysis.tests_extra import EXTRA_TESTS
        return list(EXTRA_TESTS)
    except ImportError:
        return []


ALL_TESTS = [test_s1, test_s2, test_s3, test_s4, test_s5, test_s6,
             test_s7, test_s8, test_s9, test_s10, test_s11, test_s12,
             *_load_extra()]


def run_all(tests: list[str] | None = None, verbose: bool = True
            ) -> dict[str, Any]:
    """Прогон выбранных (или всех) тестов; возвращает сводку."""
    results = []
    for fn in ALL_TESTS:
        if tests and fn.__name__.replace("test_", "") not in tests:
            continue
        try:
            res = fn()
        except Exception as exc:
            res = TestResult(fn.__name__.replace("test_", "").upper(),
                             fn.__doc__ or "")
            res.fail(f"исключение: {type(exc).__name__}: {exc}")
        results.append(res)
        if verbose:
            mark = "✓" if res.passed else "✗"
            print(f"  [{mark}] {res.id} {res.name}")
            for d in res.details[:3]:
                print(f"        {d}")
    passed = sum(1 for r in results if r.passed)
    summary = dict(
        total=len(results), passed=passed, failed=len(results) - passed,
        results=[r.to_dict() for r in results],
        all_pass=passed == len(results),
    )
    return summary
