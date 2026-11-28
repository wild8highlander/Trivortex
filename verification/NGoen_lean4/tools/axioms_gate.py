#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIVORTEX-N NGON Lean 4 — аксиомный гейт (axioms gate).

Запускает полную компиляцию корневого файла (`lake env lean NGon.lean`),
парсит вывод всех директив `#print axioms` и ва́лит проверку, если:

  1. какая-либо теорема зависит от аксиомы ВНЕ разрешённого набора
     {propext, Classical.choice, Quot.sound};
  2. количество отпечатков в выводе ≠ количеству `#print axioms` в исходнике
     (защита от урезанной/упавшей сборки);
  3. в исходнике есть `sorry` / объявление `axiom` / `native_decide` / `unsafe`;
  4. в журнале компиляции есть `warning:` или `error:`.
     (пиннингованный Lake v4.6 не знает флагов `--wfail/--iofail`; гейт
     воспроизводит их семантику, валя сборку при любом предупреждении).

Использование:
  tools/axioms_gate.py [--file NGon.lean] [--workdir DIR] [--lake lake]
                       [--log PATH] [--verbose]

Код возврата: 0 — чисто, 1 — гейт сработал (печатается таблица нарушений).
SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

ALLOWED_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})

# 'Polyvortex.s10_lyapunov_stab' depends on axioms: [propext, Classical.choice, Quot.sound]
# имя может содержать апостроф ('side3'') — жадный захват до ПОСЛЕДНЕЙ кавычки
RE_DEPENDS = re.compile(r"^'(.*)' depends on axioms: \[([^\]]*)\]")
# '_private.Polyvortex.0.Polyvortex.s9_exp_comp' does not depend on any axioms
RE_NO_AXIOMS = re.compile(r"^'(.*)' does not depend on any axioms")
# исходные директивы
RE_PRINT_DIRECTIVE = re.compile(r"(?m)^#print\s+axioms\s+([A-Za-z0-9_'.]+)")

# Запрещённые маркеры в исходнике (защита от «тихой» деградации доказательств).
# axiom-ОБЪЯВЛЕНИЯ — именно объявления, а не слово в комментарии/строке.
FORBIDDEN_SOURCE_PATTERNS = [
    (re.compile(r"(?m)^\s*axiom\s+[A-Za-z0-9_']+\s*:"), "объявление `axiom`"),
    (re.compile(r"(?m)\bsorry\b(?![A-Za-z0-9_'])"), "незакрытый `sorry`"),
    (re.compile(r"(?m)^#print\s+axioms\s+[^\n]*sorryAx"), "печать sorryAx"),
    (re.compile(r"(?m)\bnative_decide\b"), "`native_decide` (неофициальная арифметика)"),
    (re.compile(r"(?m)^\s*unsafe\b"), "`unsafe`-блок"),
    (re.compile(r"(?m)^\s*@\[implemented_by\b"), "аднотация `implemented_by`"),
]


def strip_lean_syntax(src: str) -> str:
    """Убирает комментарии и строки: маркеры `sorry`/`axiom` в ДОКЕ не нарушения."""
    # 1) строковые литералы (с экранированием)
    src = re.sub(r'"(?:[^"\\]|\\.)*"', '""', src)
    # 2) вложенные блочные комментарии /- ... -/ (Lean-вложенность)
    out, depth, i = [], 0, 0
    while i < len(src):
        if src.startswith("/-", i):
            depth += 1
            i += 2
            out.append(" " if depth == 1 else "")
        elif src.startswith("-/", i) and depth > 0:
            depth -= 1
            i += 2
        elif depth == 0:
            out.append(src[i])
            i += 1
        else:
            i += 1  # внутри комментария — пропускаем, но НЕ добавляем в out
    src = "".join(out)
    # 3) строчные комментарии -- ...
    src = re.sub(r"(?m)--[^\n]*", "", src)
    return src


def parse_args() -> argparse.Namespace:
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)  # verification/lean4/
    ap = argparse.ArgumentParser(description="Аксиомный гейт NGon.lean")
    ap.add_argument("--file", default="NGon.lean", help="имя корневого lean-файла")
    ap.add_argument("--workdir", default=root, help="каталог пакета (запуск lake env)")
    ap.add_argument("--lake", default="lake", help="исполняемый lake (PATH)")
    ap.add_argument("--log", default=None, help="куда сохранить журнал компиляции")
    ap.add_argument(
        "--from-log",
        default=None,
        dest="from_log",
        help="не компилировать заново: разобрать готовый журнал",
    )
    ap.add_argument("--timeout", type=int, default=900, help="таймаут компиляции, сек")
    ap.add_argument("--verbose", action="store_true")
    return ap.parse_args()


def compile_lean(args: argparse.Namespace) -> tuple[int, str]:
    """`lake env lean FILE` в каталоге пакета; возвращает (код, журнал)."""
    cmd = [args.lake, "env", "lean", args.file]
    env = dict(os.environ)
    env.setdefault("LEAN_ABORT_ON_OOM", "1")
    proc = subprocess.run(
        cmd,
        cwd=args.workdir,
        env=env,
        capture_output=True,
        text=True,
        timeout=args.timeout,
    )
    log = proc.stdout + ("\n" + proc.stderr if proc.stderr else "")
    if args.log:
        with open(args.log, "w", encoding="utf-8") as fh:
            fh.write(log)
    return proc.returncode, log


def parse_axiom_lines(log: str) -> dict[str, list[str]]:
    """{полное имя: список аксиом} из строк `#print axioms` вывода lean."""
    out: dict[str, list[str]] = {}
    for line in log.splitlines():
        line = line.strip()
        m = RE_NO_AXIOMS.match(line)
        if m:
            out[m.group(1)] = []
            continue
        m = RE_DEPENDS.match(line)
        if m:
            name, raw = m.group(1), m.group(2)
            axioms = [a.strip() for a in raw.split(",") if a.strip()]
            out[name] = axioms
    return out


def main() -> int:
    args = parse_args()
    src_path = os.path.join(args.workdir, args.file)
    if not os.path.isfile(src_path):
        print(f"AXIOMS GATE [FAIL]: нет файла {src_path}")
        return 1
    src = open(src_path, encoding="utf-8").read()
    directives = RE_PRINT_DIRECTIVE.findall(src)
    code_only = strip_lean_syntax(src)

    violations: list[str] = []

    # (3) запрещённые маркеры в исходнике (только КОД, без комментариев)
    for pat, label in FORBIDDEN_SOURCE_PATTERNS:
        hits = pat.findall(code_only)
        if hits:
            violations.append(f"исходник содержит {label}: {len(hits)} шт.")

    # компиляция (или разбор готового журнала)
    if args.from_log:
        rc = 0
        log = open(args.from_log, encoding="utf-8").read()
    else:
        try:
            rc, log = compile_lean(args)
        except subprocess.TimeoutExpired:
            print(f"AXIOMS GATE [FAIL]: компиляция не уложилась в {args.timeout} с")
            return 1
    if rc != 0:
        print(f"AXIOMS GATE [FAIL]: lake env lean завершился с кодом {rc}")
        for line in log.splitlines():
            if "error" in line.lower():
                print("  | " + line)
        if args.log is None:
            print("(запустите с --log PATH, чтобы сохранить полный журнал)")
        return 1

    # (4) предупреждения = провал (семантика --wfail для Lake v4.6)
    warn_lines = [ln for ln in log.splitlines() if re.search(r"\bwarning:", ln)]
    for ln in warn_lines[:20]:
        violations.append(f"предупреждение компилятора (wfail): {ln.strip()}")

    # (1) посторонние аксиомы
    printed = parse_axiom_lines(log)
    extra = {}
    for name, axioms in sorted(printed.items()):
        bad = [a for a in axioms if a not in ALLOWED_AXIOMS]
        dup = len(axioms) != len(set(axioms))
        if bad or dup:
            extra[name] = axioms
    for name, axioms in sorted(extra.items()):
        violations.append(f"теорема '{name}' зависит от аксиом вне whitelist: {axioms}")

    # (2) полнота отпечатков
    n_src, n_out = len(directives), len(printed)
    if n_src != n_out:
        violations.append(
            f"число отпечатков в выводе ({n_out}) ≠ числу директив в исходнике ({n_src}) "
            "— сборка урезана или #print axioms не исполнены"
        )
    missing = set(directives) - {n.split(".")[-1] for n in printed}
    if missing and args.verbose:
        print("не испечатались:", sorted(missing)[:10])

    # сводка
    n_clean = sum(1 for ax in printed.values() if not ax)
    n_std = sum(1 for ax in printed.values() if ax and set(ax) <= ALLOWED_AXIOMS)
    print(
        f"AXIOMS GATE: {len(printed)} отпечатков "
        f"({n_clean} без аксиом, {n_std} на стандартном наборе "
        f"[propext, Classical.choice, Quot.sound]); "
        f"исходных директив: {n_src}"
    )

    if violations:
        print("AXIOMS GATE [FAIL]:")
        for v in violations:
            print("  ✗ " + v)
        return 1
    print("AXIOMS GATE [PASS] — все теоремы на заявленном наборе аксиом")
    return 0


if __name__ == "__main__":
    sys.exit(main())
