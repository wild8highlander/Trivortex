#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Статический анализатор собственного кода TRIVORTEX MASTER.

Обходит все .py пакета: считает функции/классы/docstring-покрытие,
импорты, самые длинные функции, маркеры задач. Питает пункт меню
«Справка → О комплексе» и отчёты о качестве кода.
"""

from __future__ import annotations

import ast
import os
from dataclasses import dataclass, field

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@dataclass
class ModuleInfo:
    path: str
    lines: int = 0
    functions: int = 0
    classes: int = 0
    documented: int = 0
    total_defs: int = 0
    longest_function: str = ""
    longest_len: int = 0
    todos: int = 0


def analyze_module(path: str) -> ModuleInfo:
    info = ModuleInfo(path=os.path.relpath(path, ROOT))
    try:
        src = open(path, encoding="utf-8").read()
    except OSError:
        return info
    info.lines = src.count("\n") + 1
    info.todos = sum(1 for ln in src.splitlines() if "TODO" in ln or "FIXME" in ln)
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return info
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            info.functions += 1
            info.total_defs += 1
            if ast.get_docstring(node):
                info.documented += 1
            length = (node.end_lineno or node.lineno) - node.lineno
            if length > info.longest_len:
                info.longest_len = length
                info.longest_function = node.name
        elif isinstance(node, ast.ClassDef):
            info.classes += 1
            if ast.get_docstring(node):
                info.documented += 1
            info.total_defs += 1
    return info


def analyze_all() -> dict:
    infos = []
    for pkg in ("core", "lab", "realism", "render", "reports", "analysis", "tools"):
        pdir = os.path.join(ROOT, pkg)
        if not os.path.isdir(pdir):
            continue
        for base, dirs, files in os.walk(pdir):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for fn in sorted(files):
                if fn.endswith(".py") and fn != "__init__.py":
                    infos.append(analyze_module(os.path.join(base, fn)))
    entry = os.path.join(ROOT, "trivortex_master.py")
    if os.path.isfile(entry):
        infos.append(analyze_module(entry))
    total_lines = sum(i.lines for i in infos)
    total_funcs = sum(i.functions for i in infos)
    total_classes = sum(i.classes for i in infos)
    documented = sum(i.documented for i in infos)
    defs = sum(i.total_defs for i in infos)
    return dict(
        modules=len(infos),
        total_lines=total_lines,
        functions=total_funcs,
        classes=total_classes,
        docstring_coverage=documented / max(defs, 1),
        todos=sum(i.todos for i in infos),
        by_module=[
            dict(
                path=i.path, lines=i.lines, functions=i.functions, classes=i.classes, todos=i.todos
            )
            for i in infos
        ],
    )
