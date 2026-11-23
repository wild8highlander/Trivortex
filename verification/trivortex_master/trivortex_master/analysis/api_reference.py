#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — автоматический генератор справочника API.

Обходит все публичные модули пакета через inspect/ast и строит:

  * справочник функций/классов: сигнатуры, docstring-первая строка,
    модуль-источник;
  * статистику покрытия документацией;
  * Markdown-справочник (docs/API.md) и данные для пункта меню;
  * оглавление по пакетам (core/lab/render/realism/reports/analysis).

Гарантированно честный: то, что в справочнике, существует в коде
(генерация из ast, а не рукописный список).
"""
from __future__ import annotations

import ast
import os
import re
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKAGES = ("core", "lab", "render", "realism", "reports", "analysis")
ENTRY_FILES = ("trivortex_master.py",)


def _first_line(doc: str | None) -> str:
    if not doc:
        return ""
    for line in doc.strip().splitlines():
        s = line.strip()
        if s:
            return s
    return ""


def _format_signature(node: ast.FunctionDef | ast.AsyncFunctionDef
                      ) -> str:
    """Строка сигнатуры без аннотаций (компактно)."""
    args = []
    defaults_offset = len(node.args.args) - len(node.args.defaults)
    for i, a in enumerate(node.args.args):
        s = a.arg
        di = i - defaults_offset
        if di >= 0 and node.args.defaults:
            try:
                s += "=" + ast.unparse(node.args.defaults[di])
            except Exception:
                s += "=…"
        args.append(s)
    if node.args.vararg:
        args.append("*" + node.args.vararg.arg)
    for a, d in zip(node.args.kwonlyargs, node.args.kw_defaults):
        s = a.arg
        if d is not None:
            try:
                s += "=" + ast.unparse(d)
            except Exception:
                s += "=…"
        args.append(s)
    if node.args.kwarg:
        args.append("**" + node.args.kwarg.arg)
    return f"{node.name}({', '.join(args)})"


def scan_module(path: str, package: str) -> dict[str, Any]:
    """Сканировать один файл: функции/классы/методы."""
    rel = os.path.relpath(path, ROOT)
    info: dict[str, Any] = dict(
        module=rel, package=package,
        functions=[], classes=[], documented=0, total=0, lines=0)
    try:
        src = open(path, encoding="utf-8").read()
    except OSError:
        return info
    info["lines"] = src.count("\n") + 1
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return info

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("_"):
                continue
            doc = _first_line(ast.get_docstring(node))
            info["functions"].append(dict(
                name=node.name,
                signature=_format_signature(node),
                doc=doc, documented=bool(doc)))
            info["total"] += 1
            info["documented"] += 1 if doc else 0
        elif isinstance(node, ast.ClassDef):
            doc = _first_line(ast.get_docstring(node))
            methods = []
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                        and not sub.name.startswith("_"):
                    mdoc = _first_line(ast.get_docstring(sub))
                    methods.append(dict(name=sub.name,
                                        signature=_format_signature(sub),
                                        doc=mdoc, documented=bool(mdoc)))
                    info["total"] += 1
                    info["documented"] += 1 if mdoc else 0
            info["classes"].append(dict(name=node.name, doc=doc,
                                        documented=bool(doc), methods=methods))
            info["total"] += 1
            info["documented"] += 1 if doc else 0
    return info


def scan_all() -> list[dict[str, Any]]:
    """Просканировать весь пакет."""
    out = []
    for pkg in PACKAGES:
        pdir = os.path.join(ROOT, pkg)
        if not os.path.isdir(pdir):
            continue
        for base, dirs, files in os.walk(pdir):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for fn in sorted(files):
                if fn.endswith(".py") and fn != "__init__.py":
                    out.append(scan_module(os.path.join(base, fn), pkg))
    for entry in ENTRY_FILES:
        path = os.path.join(ROOT, entry)
        if os.path.isfile(path):
            out.append(scan_module(path, "entry"))
    return out


# ═══════════════════════════════════════════════════════════════════════════
# Экспорт в Markdown
# ═══════════════════════════════════════════════════════════════════════════
def to_markdown(infos: list[dict[str, Any]], version: str = "2.0.0"
                ) -> str:
    """Markdown-справочник API."""
    lines = [f"# TRIVORTEX MASTER v{version} — справочник API", ""]
    lines.append("_Автогенерация из AST: всё, что здесь описано, "
                 "существует в коде._")
    lines.append("")
    total_f = sum(len(i["functions"]) for i in infos)
    total_c = sum(len(i["classes"]) for i in infos)
    total_doc = sum(i["documented"] for i in infos)
    total_def = sum(i["total"] for i in infos)
    lines.append(f"**{len(infos)} модулей · {total_c} классов · "
                 f"{total_f} функций · документировано "
                 f"{total_doc}/{total_def} "
                 f"({100 * total_doc / max(total_def, 1):.0f}%)**")
    lines.append("")
    # оглавление по пакетам
    lines.append("## Оглавление")
    lines.append("")
    by_pkg: dict[str, list] = {}
    for i in infos:
        by_pkg.setdefault(i["package"], []).append(i)
    for pkg in sorted(by_pkg):
        lines.append(f"- **{pkg}**: "
                     + ", ".join(f"`{os.path.basename(m['module'])}`"
                                 for m in by_pkg[pkg]))
    lines.append("")
    # тело
    for pkg in sorted(by_pkg):
        lines.append(f"## Пакет `{pkg}`")
        lines.append("")
        for mod in by_pkg[pkg]:
            lines.append(f"### `{mod['module']}`")
            lines.append("")
            if mod["classes"]:
                lines.append("**Классы:**")
                lines.append("")
                for cls in mod["classes"]:
                    doc = f" — {cls['doc']}" if cls["doc"] else ""
                    lines.append(f"- `{cls['name']}`{doc}")
                    for m in cls["methods"]:
                        mdoc = f" — {m['doc']}" if m["doc"] else ""
                        lines.append(f"  - `{m['signature']}`{mdoc}")
                lines.append("")
            if mod["functions"]:
                lines.append("**Функции:**")
                lines.append("")
                for f in mod["functions"]:
                    doc = f" — {f['doc']}" if f["doc"] else ""
                    lines.append(f"- `{f['signature']}`{doc}")
                lines.append("")
    return "\n".join(lines)


def write_api_doc(output: str | None = None, version: str = "2.0.0"
                  ) -> str:
    """Сгенерировать docs/API.md."""
    infos = scan_all()
    md = to_markdown(infos, version)
    output = output or os.path.join(ROOT, "docs", "API.md")
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w", encoding="utf-8") as fh:
        fh.write(md)
    return output


def stats() -> dict[str, Any]:
    """Сводка для меню «О комплексе»."""
    infos = scan_all()
    total_f = sum(len(i["functions"]) for i in infos)
    total_c = sum(len(i["classes"]) for i in infos)
    total_doc = sum(i["documented"] for i in infos)
    total_def = sum(i["total"] for i in infos)
    return dict(
        modules=len(infos), classes=total_c, functions=total_f,
        documented=total_doc, total_definitions=total_def,
        docstring_coverage=total_doc / max(total_def, 1),
        lines=sum(i["lines"] for i in infos),
    )


def self_check() -> dict:
    """Справочник сгенерирован и содержит реальные функции."""
    path = write_api_doc()
    text = open(path, encoding="utf-8").read()
    st = stats()
    # выборочная проверка: ключевые функции реально в справочнике
    must_have = ["theorem31", "run_simulation", "write_png", "lzw_compress",
                 "kepler_E", "lyapunov_exponent", "generate_reports"]
    missing = [m for m in must_have if m not in text]
    return dict(
        path=path, size_bytes=os.path.getsize(path),
        **st,
        missing_samples=missing,
        ok=(not missing and st["modules"] >= 30
            and st["functions"] >= 250),
    )


if __name__ == "__main__":
    import json
    print(json.dumps(self_check(), ensure_ascii=False, indent=1,
                     default=str))
