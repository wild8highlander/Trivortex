#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIVORTEX Lean 4 — линтер конвенций Mathlib и докстрингов.

Проверки (замечание научного руководителя №3):
  1. ИМЕНОВАНИЕ:
     * theorem/lemma/def    → snake_case  (^[a-z][A-Za-z0-9_']*$);
     * structure/class/abbrev → UpperCamelCase (^[A-Z][A-Za-z0-9']*$);
     * namespace/пакет — из lakefile, отдельно не проверяется.
  2. ДОКСТРИНГИ на ключевых декларациях: покрытие `/-- ... -/` по секциям
     контролируется «ракетой» (ratchet) — покрытие может только расти:
     seal/docstring_baseline.json фиксирует текущий максимум; откат вниз
     ва́лит CI. Явный подъём планки: --update-baseline (видно в ревью).
  3. ФУНДАМЕНТ АКСИОМ: каждая директива `#print axioms NAME` должна
     ссылаться на существующую теорему — переименование/удаление теоремы
     не может тихо оголить аксиомный след.
  4. Гигиена: табы, хвостовые пробелы, сверхдлинные строки — сводка.

`lake lint` из замечания — инструмент Mathlib-репозитория (линтеры
объявлены в lakefile самого Mathlib) и для однофайлового downstream-пакета
не запускается; его роль здесь выполняет этот скрипт с теми же целями.

Режимы:
  lint_conventions.py [--file F] [--update-baseline]
SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

RE_THEOREM = re.compile(r"(?m)^(?:private\s+|protected\s+|noncomputable\s+)*(theorem|lemma)\s+([A-Za-z0-9_']+)")
RE_DEF = re.compile(r"(?m)^(?:private\s+|protected\s+|noncomputable\s+)*(?:abbrev\s+|@\[[^\]]*\]\s*)*def\s+([A-Za-z0-9_']+)")
RE_STRUCT = re.compile(r"(?m)^(?:private\s+|protected\s+)*(structure|class|abbrev)\s+([A-Za-z0-9_']+)")
RE_PRINT_AX = re.compile(r"(?m)^#print\s+axioms\s+([A-Za-z0-9_'.]+)")
RE_SECTION = re.compile(r"(?m)^\s*(?:/-!\s*)?#+\s*Section\s*(\d+)")


def _has_docstring(lines: list[str], decl_line: int, max_up: int = 6) -> bool:
    """Докстринг над декларацией: многострочный `/-- ... -/` заканчивается на `-/`."""
    j = decl_line - 2  # 0-based индекс строки над decl
    for _ in range(max_up):
        if j < 0:
            return False
        s = lines[j].strip()
        if s == "":
            j -= 1
            continue
        return s.endswith("-/") and not s.startswith("--")
    return False


def decls_and_sections(src: str):
    """Список (line, kind, name, has_docstring, section)."""
    lines = src.split("\n")
    sections: list[tuple[int, str]] = [(1, "0-preamble")]
    for i, ln in enumerate(lines, 1):
        m = RE_SECTION.match(ln)
        if m:
            sections.append((i, m.group(1)))

    def which_section(line_no: int) -> str:
        cur = sections[0][1]
        for start, tag in sections:
            if start <= line_no:
                cur = tag
        return cur

    out = []
    for m in RE_THEOREM.finditer(src):
        line = src.count("\n", 0, m.start()) + 1
        name = m.group(2)
        has_doc = _has_docstring(lines, line)
        out.append((line, m.group(1), name, has_doc, which_section(line)))
    for m in RE_DEF.finditer(src):
        line = src.count("\n", 0, m.start()) + 1
        has_doc = _has_docstring(lines, line, max_up=8)
        out.append((line, "def", m.group(1), has_doc, which_section(line)))
    for m in RE_STRUCT.finditer(src):
        line = src.count("\n", 0, m.start()) + 1
        out.append((line, m.group(1), m.group(2), False, which_section(line)))
    return out, sections


def main() -> int:
    ap = argparse.ArgumentParser(description="Линтер конвенций Trivortex.lean")
    ap.add_argument("--file", default=os.path.join(ROOT, "Trivortex.lean"))
    ap.add_argument("--baseline", default=os.path.join(ROOT, "seal", "docstring_baseline.json"))
    ap.add_argument("--update-baseline", action="store_true")
    args = ap.parse_args()

    src = open(args.file, encoding="utf-8").read()
    decls, sections = decls_and_sections(src)
    theorem_names = {d[2] for d in decls if d[1] in ("theorem", "lemma")}

    violations: list[str] = []

    # 1. именование (новые — строго; исторические — через grandfather-список)
    exceptions = set()
    exc_path = os.path.join(ROOT, "seal", "naming_exceptions.json")
    if os.path.isfile(exc_path):
        exc_raw = json.load(open(exc_path, encoding="utf-8"))
        exceptions = set(exc_raw.get("names", []) if isinstance(exc_raw, dict) else exc_raw)
    for line, kind, name, _, _ in decls:
        if kind in ("theorem", "lemma", "def"):
            ok = re.fullmatch(r"[a-z][A-Za-z0-9_']*", name)
        else:
            ok = re.fullmatch(r"[A-Z][A-Za-z0-9']*", name)
        if not ok and name in exceptions:
            continue
        if not ok:
            violations.append(
                f"{line}: имя `{name}` ({kind}) не в "
                + ("snake_case" if kind in ("theorem", "lemma", "def") else "UpperCamelCase")
                + " ( grandfather-список: seal/naming_exceptions.json )"
            )

    # 3. фундамент аксиом — ссылки на существующие декларации
    known_names = {d[2] for d in decls}
    for m in RE_PRINT_AX.finditer(src):
        name = m.group(1).split(".")[-1]
        if name not in known_names:
            violations.append(f"#print axioms ссылается на несуществующую теорему `{name}`")

    # 4. гигиена (сводка)
    tabs = len(re.findall(r"\t", src))
    trail = len(re.findall(r"(?m)[ \t]+$", src))
    long_lines = [i + 1 for i, ln in enumerate(src.split("\n")) if len(ln) > 120]

    # 2. покрытие докстрингами (по секциям)
    per: dict[str, dict[str, int]] = {}
    for _, kind, _, has_doc, sec in decls:
        if kind in ("structure", "class", "abbrev"):
            continue
        d = per.setdefault(sec, {"total": 0, "covered": 0})
        d["total"] += 1
        if has_doc:
            d["covered"] += 1
    tot = sum(d["total"] for d in per.values())
    cov = sum(d["covered"] for d in per.values())
    overall = (cov / tot) if tot else 1.0

    if args.update_baseline:
        os.makedirs(os.path.dirname(args.baseline), exist_ok=True)
        payload = {
            "note": "ракет докстрингов: обновление — явное действие (видно в ревью)",
            "overall": {"covered": cov, "total": tot},
            "by_section": {
                sec: {"covered": d["covered"], "total": d["total"]}
                for sec, d in sorted(per.items())
            },
        }
        json.dump(payload, open(args.baseline, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(f"LINT: база докстрингов обновлена — покрытие {overall:.1%} ({cov}/{tot})")
        return 0

    # сравнение с ракетой (точное, перекрёстным умножением — без округлений)
    if os.path.isfile(args.baseline):
        base = json.load(open(args.baseline, encoding="utf-8"))
        b = base.get("overall", {})
        b_cov, b_tot = b.get("covered", 0), b.get("total", 0)
        if tot and cov * b_tot < b_cov * tot:
            violations.append(
                f"покрытие докстрингов упало: {cov}/{tot} < базы {b_cov}/{b_tot} "
                "(ракет: только рост; --update-baseline — явно)"
            )
        for sec, d in sorted(per.items()):
            b2 = base.get("by_section", {}).get(sec)
            if b2 and d["total"]:
                if d["covered"] * b2["total"] < b2["covered"] * d["total"]:
                    violations.append(
                        f"секция {sec}: покрытие докстрингов {d['covered']}/{d['total']} "
                        f"< базы {b2['covered']}/{b2['total']}"
                    )

    # сводка
    print(f"LINT: деклараций {len(decls)}; секций: {len(sections) - 1}")
    print(f"LINT: докстринги: {cov}/{tot} = {overall:.1%}")
    for sec, d in sorted(per.items()):
        c = (d["covered"] / d["total"]) if d["total"] else 1.0
        print(f"  Section {sec:>2}: {d['covered']:>3}/{d['total']:<3} = {c:5.1%}")
    if tabs or trail or long_lines:
        print(f"LINT (сводка гигиены): табов {tabs}, хвостовых пробелов {trail}, строк >120: {len(long_lines)}")

    if violations:
        print(f"LINT [FAIL]: {len(violations)} нарушений:")
        for v in violations[:30]:
            print("  ✗ " + v)
        return 1
    print("LINT [PASS] — конвенции и ракет докстрингов выдержаны")
    return 0


if __name__ == "__main__":
    sys.exit(main())
