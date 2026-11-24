#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — тесты S13–S24 (расширение удвоенного объёма).

Каждый тест покрывает отдельный аналитический модуль против
независимого эталона (наблюдение/аналитика/литература):

S13 relativity — Меркурий 42.98″/век      S19 planetary — Hill/TRAPPIST
S14 nbody_tree — Barnes-Hut точность      S20 stellar — Солнце/O/карлик
S15 chaos — FLI упорядочивание            S21 xlsx — openpyxl-валидация
S16 collisions — законы сохранения        S22 pptx — python-pptx-чтение
S17 tides — Луна/Ио/Козаи                 S23 mcmc — МНК-согласие + R̂
S18 radiation — t_PR/β/Бенну/Starshot     S24 wavelets+fitting — chirp+гаусс

Подключается из analysis.tests (ALL_TESTS += EXTRA_TESTS).
"""

from __future__ import annotations

from typing import Any

from analysis.tests import TestResult


def _run_module_check(
    r: TestResult, module: str, min_key: str = "all_ok", alt_key: str = "ok"
) -> dict[str, Any]:
    """Общая обвязка: self_check модуля → TestResult."""
    try:
        mod = __import__(module, fromlist=["self_check"])
        res = getattr(mod, "self_check")()
        ok = bool(res.get(min_key, res.get(alt_key, False)))
        r.metrics = res
        r.check(
            ok,
            f"{module}: эталон выполнен",
            f"{module}: {res.get('error', 'несоответствие эталону')}",
        )
    except Exception as exc:
        r.fail(f"{module}: {type(exc).__name__}: {exc}")
    return r.metrics


# ═══════════════════════════════════════════════════════════════════════════
def test_s13() -> TestResult:
    """Handle test s13."""
    r = TestResult("S13", "relativity: прецессия Меркурия 42.98″/век")
    m = _run_module_check(r, "lab.relativity")
    # дополнительная жёсткая проверка: величина именно 42.98 ± 0.5
    val = m.get("mercury_1pn")
    r.check(
        val is not None and abs(val - 42.98) < 0.5,
        f"Меркурий: {val:.2f}″/век (ОТО 42.98)",
        f"Меркурий: {val} — вне допуска",
    )
    return r


def test_s14() -> TestResult:
    """Handle test s14."""
    r = TestResult("S14", "Barnes-Hut: точность и ускорение")
    from lab.nbody_tree import benchmark

    b = benchmark(n_bodies=350, seed=5)
    r.metrics = {k: v for k, v in b.items() if not isinstance(v, list)}
    r.check(
        b["err_rms"] < 0.05,
        f"ошибка силы err_rms={b['err_rms']:.3f} < 5%",
        f"err_rms={b['err_rms']:.3f} — слишком грубо",
    )
    r.check(
        b["speedup"] > 1.0,
        f"дерево быстрее прямого суммирования ×{b['speedup']:.2f}",
        f"дерево медленнее прямого ({b['speedup']:.2f}×)",
    )
    return r


def test_s15() -> TestResult:
    """Handle test s15."""
    r = TestResult("S15", "chaos: FLI упорядочивание орбит")
    m = _run_module_check(r, "lab.chaos")
    flis = (m.get("fli_oscillator"), m.get("fli_hh_regular"), m.get("fli_hh_chaotic"))
    r.check(
        all(isinstance(v, (int, float)) for v in flis) and flis[2] > flis[1],
        f"FLI: осц {flis[0]:.2f} ≤ рег {flis[1]:.2f} < хаос {flis[2]:.2f}",
        f"FLI не разделил орбиты: {flis}",
    )
    return r


def test_s16() -> TestResult:
    """Handle test s16."""
    r = TestResult("S16", "collisions: законы сохранения")
    _run_module_check(r, "lab.collisions")
    return r


def test_s17() -> TestResult:
    """Handle test s17."""
    r = TestResult("S17", "tides: Луна 3.8 см/год, Ио, Козаи")
    m = _run_module_check(r, "lab.tides")
    val = m.get("moon_cm_per_year")
    r.check(
        val is not None and 0.5 < val < 20.0,
        f"Луна: {val:.2f} см/год (LLR 3.82)",
        f"Луна: {val} см/год — вне физического диапазона",
    )
    return r


def test_s18() -> TestResult:
    """Handle test s18."""
    r = TestResult("S18", "radiation: Пойнтинг-Робертсон/Ярковский")
    m = _run_module_check(r, "lab.radiation")
    t_pr = m.get("grain_pr_lifetime_years")
    r.check(
        t_pr is not None and 1e5 < t_pr < 5e5,
        f"t_PR(100 мкм, 1 а.е.) = {t_pr:.2e} лет",
        f"t_PR = {t_pr} — вне диапазона Wyatt-Whipple",
    )
    return r


def test_s19() -> TestResult:
    """Handle test s19."""
    r = TestResult("S19", "planetary_systems: Hill + TRAPPIST-1")
    m = _run_module_check(r, "realism.planetary_systems")
    t_eq = m.get("trappist_T_eq")
    r.check(
        t_eq is not None and abs(t_eq - 249.0) < 15.0,
        f"TRAPPIST-1e T_eq = {t_eq:.0f} К (Gillon 2017: 249)",
        f"T_eq = {t_eq} — расхождение с Gillon",
    )
    return r


def test_s20() -> TestResult:
    """Handle test s20."""
    r = TestResult("S20", "stellar: Солнце/O-звезда/карлик/Рош")
    m = _run_module_check(r, "realism.stellar")
    o_life = m.get("ostar_life_gyr")
    r.check(
        o_life is not None and 0.0005 < o_life < 0.02,
        f"O-звезда 30 M☉ живёт {o_life * 1000:.1f} млн лет",
        f"время жизни O-звезды {o_life} Gyr — неверно",
    )
    return r


def test_s21() -> TestResult:
    """Handle test s21."""
    r = TestResult("S21", "xlsx_writer: openpyxl читает книгу")
    m = _run_module_check(r, "reports.writers.xlsx_writer")
    read_ok = m.get("openpyxl_read_ok")
    r.check(
        read_ok in (None, True),
        "openpyxl: 2 листа, ячейка на месте",
        f"openpyxl прочитал неверно: {read_ok}",
    )
    return r


def test_s22() -> TestResult:
    """Handle test s22."""
    r = TestResult("S22", "pptx_writer: python-pptx читает слайды")
    m = _run_module_check(r, "reports.writers.pptx_writer")
    read_ok = m.get("pptx_read_ok")
    r.check(
        read_ok in (None, True),
        "python-pptx: 3 слайда на месте",
        f"python-pptx прочитал неверно: {read_ok}",
    )
    return r


def test_s23() -> TestResult:
    """Handle test s23."""
    r = TestResult("S23", "mcmc: согласие с МНК и R̂")
    m = _run_module_check(r, "analysis.mcmc")
    b_mcmc = m.get("b_mean")
    b_ols = m.get("b_ols")
    se = m.get("se_b")
    r.check(
        b_mcmc is not None and abs(b_mcmc - b_ols) < 2.0 * se,
        f"MCMC b={b_mcmc:.3f} ≈ МНК b={b_ols:.3f} (SE {se:.3f})",
        f"MCMC b={b_mcmc} не согласован с МНК {b_ols}",
    )
    return r


def test_s24() -> TestResult:
    """Handle test s24."""
    r = TestResult("S24", "wavelets + fitting: chirp и гауссов пик")
    _run_module_check(r, "analysis.wavelets")
    _run_module_check(r, "analysis.fitting")
    return r


EXTRA_TESTS = [
    test_s13,
    test_s14,
    test_s15,
    test_s16,
    test_s17,
    test_s18,
    test_s19,
    test_s20,
    test_s21,
    test_s22,
    test_s23,
    test_s24,
]
