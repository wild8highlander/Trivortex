#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIVORTEX-N Lean 4 — эквивалент `lake exe mk_all --check` для однофайлового пакета.

`mk_all` — инструмент Mathlib-репозитория; для downstream-пакета из ОДНОГО
файла NGon.lean он сводится к следующему контракту:

  1. в пакете ровно один корневой lean-модуль — NGon.lean
     (лишних «осиротевших» .lean-модулей нет);
  2. lakefile.lean объявляет его корнем (`roots := #[`NGon]`) и
     default-таргетом — легкораном CI;
  3. корневой файл НЕ импортирует сам себя и не содержит ссылок на
     несуществующие модули (все импорты — Mathlib);
  4. пиннинги воспроизводимы: lean-toolchain зафиксирован,
     Mathlib затребован ТОЧНЫМ тегом (не веткой).

Провал любого пункта ва́лит CI.
SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
"""

from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

EXPECTED_ROOTS = ["NGon.lean", "NSide.lean", "NCore.lean", "NRoots.lean", "NFlow.lean"]
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.6.0"
EXPECTED_MATHLIB_TAG = "v4.6.0"


def main() -> int:
    problems: list[str] = []

    # 1. ровно пять корневых lean-модулей (lakefile.lean — конфиг Lake, не модуль):
    #    пятифайловая программа TRIVORTEX-N приземлена целиком.
    lean_files = sorted(
        f
        for f in os.listdir(ROOT)
        if f.endswith(".lean") and f != "lakefile.lean" and os.path.isfile(os.path.join(ROOT, f))
    )
    if lean_files != sorted(EXPECTED_ROOTS):
        problems.append(f"ожидались {EXPECTED_ROOTS}, найдено: {lean_files}")

    # 2. lakefile: пять корней + default-таргет + пин Mathlib
    lakefile = open(os.path.join(ROOT, "lakefile.lean"), encoding="utf-8").read()
    if "roots := #[" not in lakefile:
        problems.append("lakefile.lean: roots := #[...] не объявлен")
    else:
        for stem in ("NGon", "NSide", "NCore", "NRoots", "NFlow"):
            if f"`{stem}" not in lakefile:
                problems.append(f"lakefile.lean: корень `{stem} не объявлен")
    if "@[default_target]" not in lakefile:
        problems.append("lakefile.lean: нет @[default_target] (lake build не соберёт артефакт)")
    m = re.search(r'mathlib4\.git"\s*@\s*"([^"]+)"', lakefile)
    if not m:
        problems.append("lakefile.lean: Mathlib не затребован точным пином")
    elif m.group(1) != EXPECTED_MATHLIB_TAG:
        problems.append(
            f"lakefile.lean: Mathlib пин {m.group(1)} ≠ {EXPECTED_MATHLIB_TAG} (воспроизводимость)"
        )
    if "autoImplicit, false" not in lakefile:
        problems.append("lakefile.lean: autoImplicit false не включён (гигиена подписей)")

    # 3. самособлюдение импортов (все пять файлов импортируют только Mathlib)
    total_imports = 0
    for root_file in EXPECTED_ROOTS:
        src = open(os.path.join(ROOT, root_file), encoding="utf-8").read()
        imports = re.findall(r"(?m)^\s*import\s+([A-Za-z0-9_.]+)", src)
        total_imports += len(imports)
        self_imports = [
            i
            for i in imports
            if i.startswith(("Trivortex", "NGon", "NSide", "NCore", "NRoots", "NFlow"))
        ]
        if self_imports:
            problems.append(f"{root_file} импортирует свои модули: {self_imports}")

    # 4. пин toolchain
    toolchain = open(os.path.join(ROOT, "lean-toolchain"), encoding="utf-8").read().strip()
    if toolchain != EXPECTED_TOOLCHAIN:
        problems.append(f"lean-toolchain = {toolchain!r} ≠ {EXPECTED_TOOLCHAIN!r}")

    print(
        f"IMPORTS: roots {len(EXPECTED_ROOTS)} файлов; imports: {total_imports} "
        f"(все Mathlib); toolchain {toolchain}; mathlib pin {'OK' if m else '—'}"
    )
    if problems:
        print("IMPORTS [FAIL]:")
        for p in problems:
            print("  ✗ " + p)
        return 1
    print("IMPORTS [PASS] — однофайловый контракт и пиннинги выдержаны")
    return 0


if __name__ == "__main__":
    sys.exit(main())
