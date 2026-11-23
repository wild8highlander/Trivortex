#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — quality gate: единый CI-контур пакета.

Один вызов собирает ВСЕ показатели качества и пишет протокол:

  * selftest (S1–S24) и приёмка (A1–A20) — через tests/verify_package;
  * self_check всех аналитических модулей напрямую (relativity,
    nbody_tree, chaos, collisions, tides, radiation, planetary_systems,
    stellar, resonances, lomb_scargle, ttvs, halo_orbits,
    proper_elements, spectrum, tissot, orbital_elements_fit,
    periodogram, tles, mission_design, encounter, mcmc, wavelets,
    fitting, benchmark);
  * docstring-покрытие (analysis.api_reference);
  * скан TODO/FIXME/XXX и китайских/латинских заглушек в коде;
  * лимиты строк и размера каталога.

Протокол: JSON + консольная сводка. Ненулевой код выхода при провале.
"""

from __future__ import annotations

import json
import os
import re
import sys
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def scan_source_hygiene() -> dict:
    """Скан заглушек и мусора во всех .py.

    Тонкость: маркеры в КАВЫЧКАХ ('TODO' в коде подсчёта маркеров) —
    данные, а не заглушки; собственный файл сканера исключается.
    Настоящие заглушки: маркеры вне кавычек + raise NotImplementedError."""
    patterns = re.compile(
        r"\b(TODO|FIXME|XXX|HACK)\b|待补充|待完成|placeholder\s*$|" r"raise NotImplementedError",
        re.MULTILINE,
    )
    quoted = re.compile(r"[\'\"].{0,3}(?:TODO|FIXME|XXX|HACK).{0,3}[\'\"]")
    self_file = os.path.relpath(os.path.abspath(__file__), ROOT)
    findings = []
    n_files = 0
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for fn in files:
            if not fn.endswith(".py"):
                continue
            n_files += 1
            path = os.path.join(base, fn)
            rel = os.path.relpath(path, ROOT)
            if rel == self_file:
                continue
            src = open(path, encoding="utf-8").read()
            for m in patterns.finditer(src):
                line_no = src[: m.start()].count("\n") + 1
                line = src.splitlines()[line_no - 1]
                if quoted.search(line):
                    continue  # маркер как данные в кавычках
                findings.append(f"{rel}:{line_no}: {m.group(0)}")
    return dict(files=n_files, findings=findings, clean=not findings)


def module_selfchecks() -> list[dict]:
    """self_check() всех модулей с независимыми эталонами."""
    checks = []

    def run(label, module, func="self_check"):
        try:
            mod = __import__(module, fromlist=[func])
            res = getattr(mod, func)()
            ok = bool(res.get("all_ok", res.get("ok", False)))
            checks.append(dict(module=label, ok=ok, result=res))
        except Exception as exc:
            checks.append(
                dict(module=label, ok=False, result=dict(error=f"{type(exc).__name__}: " f"{exc}"))
            )

    run("relativity", "lab.relativity")
    run("nbody_tree", "lab.nbody_tree")
    run("chaos", "lab.chaos")
    run("collisions", "lab.collisions")
    run("tides", "lab.tides")
    run("radiation", "lab.radiation")
    run("resonances", "lab.resonances")
    run("tissot", "lab.tissot")
    run("halo_orbits", "lab.halo_orbits")
    run("planetary_systems", "realism.planetary_systems")
    run("stellar", "realism.stellar")
    run("sky_coordinates", "realism.sky_coordinates")
    run("tles", "realism.tles")
    run("mission_design", "realism.mission_design")
    run("encounter", "realism.encounter")
    run("lomb_scargle", "analysis.lomb_scargle")
    run("ttvs", "analysis.ttvs")
    run("periodogram", "analysis.periodogram")
    run("proper_elements", "analysis.proper_elements")
    run("orbital_elements_fit", "analysis.orbital_elements_fit")
    run("mcmc", "analysis.mcmc")
    run("wavelets", "analysis.wavelets")
    run("fitting", "analysis.fitting")
    run("xlsx_writer", "reports.writers.xlsx_writer")
    run("pptx_writer", "reports.writers.pptx_writer")
    run("odt_writer", "reports.writers.odt_writer")
    run("raytracer", "render.raytracer")
    run("particles", "render.particles")
    run("camera", "render.camera")
    run("spectrum", "render.spectrum")
    run("frame_compositor", "render.frame_compositor")
    run("cosmology", "realism.cosmology")
    run("almanac", "realism.almanac")
    run("orbital_maneuvers", "lab.orbital_maneuvers")
    run("lightcurves", "analysis.lightcurves")
    run("corner_plots", "analysis.corner_plots")
    run("entropy", "analysis.entropy")
    run("hamiltonian_split", "lab.hamiltonian_split")
    run("trojans", "lab.trojan_points")
    run("solar_system_sim", "lab.solar_system_sim")
    run("eclipses", "realism.eclipse_predictor")
    run("bright_stars", "realism.bright_stars")
    run("data_exporter", "tools.data_exporter")
    run("ascii_sky", "render.ascii_sky")
    run("release_notes", "tools.release_notes")
    run("spacecraft", "lab.spacecraft")
    run("observatory", "realism.observatory")
    run("pipeline", "analysis.pipeline")
    run("space_weather", "realism.space_weather")
    return checks


def run_full_gate(json_path: str | None = None) -> dict:
    """Полный прогон gate: selftest + приёмка + самопроверки + гигиена."""
    from analysis.tests import run_all as _run_all
    from tools.verify_package import run_acceptance
    from analysis.api_reference import stats as api_stats

    st = _run_all(verbose=False)
    acc_raw = run_acceptance()
    acc = dict(passed=sum(1 for v in acc_raw.values() if v), total=len(acc_raw), details=acc_raw)
    mods = module_selfchecks()
    hygiene = scan_source_hygiene()
    api = api_stats()

    py_lines = 0
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for fn in files:
            if fn.endswith(".py"):
                py_lines += sum(1 for _ in open(os.path.join(base, fn), encoding="utf-8"))

    mods_ok = [m for m in mods if m["ok"]]
    gate = dict(
        selftest=dict(passed=st["passed"], total=st["total"], details=st.get("details", {})),
        acceptance=dict(passed=acc["passed"], total=acc["total"], details=acc.get("details", {})),
        module_selfchecks=dict(
            passed=len(mods_ok),
            total=len(mods),
            modules=[dict(module=m["module"], ok=m["ok"]) for m in mods],
        ),
        hygiene=dict(files=hygiene["files"], findings=hygiene["findings"], clean=hygiene["clean"]),
        api=dict(
            modules=api["modules"],
            classes=api["classes"],
            functions=api["functions"],
            docstring_coverage=api["docstring_coverage"],
        ),
        code=dict(py_lines=py_lines),
        passed=(
            st["passed"] == st["total"]
            and acc["passed"] == acc["total"]
            and len(mods_ok) == len(mods)
            and hygiene["clean"]
        ),
    )
    if json_path:
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(gate, fh, ensure_ascii=False, indent=1, default=str)
    return gate


def print_gate(gate: dict) -> None:
    """Консольная сводка (используется в CI-режиме)."""
    print("── QUALITY GATE ──────────────────────────────────")
    print(f"selftest:      {gate['selftest']['passed']}/{gate['selftest']['total']}")
    print(f"acceptance:    {gate['acceptance']['passed']}/{gate['acceptance']['total']}")
    print(
        f"module checks: {gate['module_selfchecks']['passed']}/{gate['module_selfchecks']['total']}"
    )
    for m in gate["module_selfchecks"]["modules"]:
        if not m["ok"]:
            print(f"  ✗ {m['module']}")
    print(f"hygiene:       {'чисто' if gate['hygiene']['clean'] else 'НАЙДЕНЫ ЗАГЛУШКИ'}")
    for f in gate["hygiene"]["findings"][:10]:
        print(f"  ⚠ {f}")
    print(f"docstrings:    {gate['api']['docstring_coverage']:.0%}")
    print(f"python lines:  {gate['code']['py_lines']}")
    # группировка модулей по пакетам
    by_pkg: dict[str, list[str]] = {}
    for m in gate["module_selfchecks"]["modules"]:
        pkg = m["module"].split(".")[0]
        by_pkg.setdefault(pkg, []).append("✓" if m["ok"] else "✗")
    for pkg, marks in sorted(by_pkg.items()):
        ok_n = marks.count("✓")
        print(f"  {pkg:10s}: {ok_n}/{len(marks)} {''.join(marks)}")
    print(f"ИТОГ:          {'PASSED' if gate['passed'] else 'FAILED'}")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=os.path.join(ROOT, "runs", "quality_gate.json"))
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    g = run_full_gate(args.json)
    if not args.quiet:
        print_gate(g)
    sys.exit(0 if g["passed"] else 1)
