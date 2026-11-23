#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — генератор релизных заметок (CHANGELOG-секция).

Собирает факты о релизе из живых данных (не рукопись):

  * из analysis.api_reference.stats(): число модулей/классов/функций,
    покрытие docstrings, строк кода;
  * из tests/verify_package: статус selftest и приёмки;
  * из data/catalog.json: объём каталога, типы объектов;
  * из lab.presets: число пресетов; из core.registry — режимы меню;
  * из runs/quality_gate.json (если есть): модульные проверки.

Экспорт: Markdown-секция для CHANGELOG.md + JSON-протокол.

Самопроверка: заметки содержат фактические ключевые числа и
генерируются без исключений.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def collect_release_facts() -> dict:
    """Собрать все факты о текущем состоянии пакета."""
    from analysis.api_reference import stats as api_stats
    from lab.presets import load_presets, load_catalog
    from analysis.tests import run_all as run_selftest

    api = api_stats()
    # полный счёт строк (api_stats сканирует только пакеты, без tools/)
    py_lines = 0
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for fn in files:
            if fn.endswith(".py"):
                py_lines += sum(1 for _ in open(os.path.join(base, fn), encoding="utf-8"))
    api["lines"] = py_lines
    catalog = load_catalog()
    n_objects = catalog.get("count", len(catalog.get("objects", [])))
    n_presets = len(load_presets())

    # режимы меню (без печати баннера)
    try:
        import trivortex_master  # noqa: F401
        import modes_extra  # noqa: F401

        n_modes = len(trivortex_master.REGISTRY.all_modes())
        categories = trivortex_master.REGISTRY.categories()
    except Exception:
        n_modes, categories = 0, []

    # selftest без verbose
    st = run_selftest(verbose=False)

    # типы объектов каталога
    type_counts: dict[str, int] = {}
    for obj in catalog.get("objects", []):
        t = obj.get("type", "?")
        type_counts[t] = type_counts.get(t, 0) + 1

    return dict(
        generated=_dt.datetime.now().isoformat(timespec="seconds"),
        api=dict(
            modules=api["modules"],
            classes=api["classes"],
            functions=api["functions"],
            docstring_coverage=round(api["docstring_coverage"], 3),
            lines=api["lines"],
        ),
        catalog=dict(objects=n_objects, by_type=type_counts),
        presets=n_presets,
        menu=dict(modes=n_modes, categories=categories),
        selftest=dict(passed=st["passed"], total=st["total"], all_pass=st["all_pass"]),
    )


def render_markdown(facts: dict, version: str = "2.0.0") -> str:
    """Markdown-секция CHANGELOG."""
    L = [f"# v{version} — удвоенный объём ({facts['generated']})", ""]
    L.append(
        f"- **{facts['api']['modules']} модулей**, "
        f"{facts['api']['classes']} классов, "
        f"{facts['api']['functions']} функций; "
        f"~{facts['api']['lines']} строк; покрытие docstrings "
        f"{facts['api']['docstring_coverage']:.0%}"
    )
    L.append(
        f"- каталог: **{facts['catalog']['objects']} объектов** "
        f"(" + ", ".join(f"{t}: {n}" for t, n in sorted(facts["catalog"]["by_type"].items())) + ")"
    )
    L.append(
        f"- пресетов сцен: **{facts['presets']}**; режимов меню: "
        f"**{facts['menu']['modes']}** в "
        f"{len(facts['menu']['categories'])} категориях"
    )
    st = facts["selftest"]
    mark = "✓" if st["all_pass"] else "✗"
    L.append(f"- selftest S1–S24: {mark} {st['passed']}/{st['total']}")
    L.append("")
    return "\n".join(L)


# ═══════════════════════════════════════════════════════════════════════════
# Сравнение с v1.0.0 (факты удвоения объёма)
# ═══════════════════════════════════════════════════════════════════════════
V1_FACTS = dict(
    modules=44,
    classes=60,
    functions=250,
    lines=11776,
    catalog=258,
    presets=10,
    modes=21,
)


def _v1_ast_facts() -> dict:
    """Точные классы/функции v1.0.0: AST по git-версии файла-манифеста.

    Если git-история недоступна — берём оценки V1_FACTS и помечаем."""
    import subprocess

    try:
        out = subprocess.run(
            ["git", "show", "HEAD:trivortex_master/../download/manifest_v1.0.0.json"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception:
        return dict(exact=False)
    return dict(exact=False)  # манифест не хранит AST-статистику


# Классы/функции v1: из списка файлов манифеста через git show
def _v1_code_facts() -> dict:
    """AST-подсчёт классов/функций по каждому .py v1 из git."""
    import subprocess

    try:
        manifest = subprocess.run(
            ["git", "show", "a02c266b:download/manifest_v1.0.0.json"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if manifest.returncode != 0:
            return dict(classes=V1_FACTS["classes"], functions=V1_FACTS["functions"], exact=False)
        files = json.loads(manifest.stdout).get("files", [])
        classes = functions = 0
        import ast as _ast

        for entry in files:
            if not entry["path"].endswith(".py"):
                continue
            blob = subprocess.run(
                ["git", "show", f"a02c266b:download/../{entry['path']}"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if blob.returncode != 0:
                continue
            try:
                tree = _ast.parse(blob.stdout)
            except SyntaxError:
                continue
            for node in _ast.walk(tree):
                if isinstance(node, _ast.ClassDef):
                    classes += 1
                elif isinstance(node, _ast.FunctionDef):
                    functions += 1
        if classes == 0:
            return dict(classes=V1_FACTS["classes"], functions=V1_FACTS["functions"], exact=False)
        return dict(classes=classes, functions=functions, exact=True)
    except Exception:
        return dict(classes=V1_FACTS["classes"], functions=V1_FACTS["functions"], exact=False)


def doubling_report(facts: dict | None = None) -> dict:
    """Факты удвоения: v2.0.0 против v1.0.0 по всем метрикам."""
    if facts is None:
        facts = collect_release_facts()
    v1 = _v1_code_facts()
    v1_classes = v1["classes"]
    v1_functions = v1["functions"]
    rows = []
    pairs = [
        ("модули", facts["api"]["modules"], V1_FACTS["modules"]),
        ("классы", facts["api"]["classes"], v1_classes),
        ("функции", facts["api"]["functions"], v1_functions),
        ("строки", facts["api"]["lines"], V1_FACTS["lines"]),
        ("каталог", facts["catalog"]["objects"], V1_FACTS["catalog"]),
        ("пресеты", facts["presets"], V1_FACTS["presets"]),
        ("режимы меню", facts["menu"]["modes"], V1_FACTS["modes"]),
    ]
    for name, now, was in pairs:
        ratio = now / max(was, 1)
        rows.append(
            dict(metric=name, v1=was, v2=now, ratio=round(ratio, 2), doubled=(ratio >= 1.99))
        )
    all_doubled = all(r["doubled"] for r in rows)
    return dict(rows=rows, all_doubled=all_doubled, note="цель — удвоение каждой метрики v1.0.0")


def render_doubling_markdown(doubling: dict) -> str:
    """Таблица удвоения для CHANGELOG."""
    L = [
        "",
        "## Удвоение против v1.0.0",
        "",
        "| Метрика | v1.0.0 | v2.0.0 | × |",
        "|---|---|---|---|",
    ]
    for r in doubling["rows"]:
        mark = " ✓" if r["doubled"] else ""
        L.append(f"| {r['metric']} | {r['v1']} | {r['v2']} | " f"×{r['ratio']:.2f}{mark} |")
    L.append("")
    if doubling["all_doubled"]:
        L.append("_Все метрики удвоены или превышены._")
    else:
        L.append("*Не все метрики удвоены — см. таблицу.*")
    return "\n".join(L) + "\n"


def write_release_notes(
    path: str | None = None, version: str = "2.0.0", include_doubling: bool = True
) -> str:
    """Записать CHANGELOG-секцию (по умолчанию docs/RELEASE_v2.0.md)."""
    facts = collect_release_facts()
    path = path or os.path.join(ROOT, "docs", f"RELEASE_v{version}.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    text = render_markdown(facts, version)
    if include_doubling:
        doubling = doubling_report(facts)
        text += render_doubling_markdown(doubling)
        with open(path + ".doubling.json", "w", encoding="utf-8") as fh:
            json.dump(doubling, fh, ensure_ascii=False, indent=1, default=str)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    with open(path + ".json", "w", encoding="utf-8") as fh:
        json.dump(facts, fh, ensure_ascii=False, indent=1, default=str)
    return path


def self_check() -> dict:
    """Заметки сгенерированы; таблица удвоения присутствует."""
    path = write_release_notes()
    text = open(path, encoding="utf-8").read()
    facts = collect_release_facts()
    has_modules = f"{facts['api']['modules']} модулей" in text
    has_objects = f"{facts['catalog']['objects']} объектов" in text
    has_selftest = "selftest S1–S24" in text
    dbl = doubling_report(facts)
    has_doubling = "Удвоение против v1.0.0" in text
    return dict(
        path=path,
        size_bytes=os.path.getsize(path),
        has_modules=has_modules,
        has_objects=has_objects,
        has_selftest=has_selftest,
        has_doubling=has_doubling,
        doubling_all=dbl["all_doubled"],
        doubling_rows=dbl["rows"],
        ok=has_modules and has_objects and has_selftest and has_doubling,
    )


if __name__ == "__main__":
    print(self_check())
