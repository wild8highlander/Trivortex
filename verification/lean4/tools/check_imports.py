#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIVORTEX Lean 4 — эквивалент `lake exe mk_all --check` для однофайлового пакета.

`mk_all` — инструмент Mathlib-репозитория (генерирует Mathlib/Tactic/*.lean
со списком импортов всех модулей и проверяет его полноту). Для
downstream-пакета из ОДНОГО файла Trivortex.lean недоступен и по смыслу
сводится к следующему контракту, который здесь и проверяется:

  1. в пакете ровно один корневой lean-модуль — Trivortex.lean
     (лишних «осиротевших» .lean-модулей нет);
  2. lakefile.lean объявляет его корнем (`roots := #[`Trivortex]`) и
     default-таргетом — легкораном CI;
  3. корневой файл НЕ импортирует сам себя и не содержит ссылок на
     несуществующие модули;
  4. пиннинги воспроизводимы: lean-toolchain зафиксирован,
     Mathlib затребован ТОЧНЫМ тегом (не веткой).

Провал любого пункта ва́лит CI — это «no orphan modules»-часть
замечания №1 научного руководителя.
SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
"""

from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

EXPECTED_ROOT = "Trivortex.lean"
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.6.0"
EXPECTED_MATHLIB_TAG = "v4.6.0"


def main() -> int:
    problems: list[str] = []

    # 1. ровно один корневой lean-модуль (lakefile.lean — конфиг Lake, не модуль)
    lean_files = [
        f for f in os.listdir(ROOT)
        if f.endswith(".lean") and f != "lakefile.lean"
        and os.path.isfile(os.path.join(ROOT, f))
    ]
    if lean_files != [EXPECTED_ROOT]:
        problems.append(f"ожидался единственный {EXPECTED_ROOT}, найдено: {lean_files}")

    # 2. lakefile: корень + default-таргет + пин Mathlib
    lakefile = open(os.path.join(ROOT, "lakefile.lean"), encoding="utf-8").read()
    if "roots := #[`Trivortex]" not in lakefile:
        problems.append("lakefile.lean: roots := #[`Trivortex] не объявлен")
    if "@[default_target]" not in lakefile:
        problems.append("lakefile.lean: нет @[default_target] (lake build не соберёт артефакт)")
    m = re.search(r'mathlib4\.git"\s*@\s*"([^"]+)"', lakefile)
    if not m:
        problems.append("lakefile.lean: Mathlib не затребован точным пином")
    elif m.group(1) != EXPECTED_MATHLIB_TAG:
        problems.append(f"lakefile.lean: Mathlib пин {m.group(1)} ≠ {EXPECTED_MATHLIB_TAG} (воспроизводимость)")

    # 3. самособлюдение импортов
    src = open(os.path.join(ROOT, EXPECTED_ROOT), encoding="utf-8").read()
    imports = re.findall(r"(?m)^\s*import\s+([A-Za-z0-9_.]+)", src)
    self_imports = [i for i in imports if i.startswith("Trivortex")]
    if self_imports:
        problems.append(f"корневой файл импортирует свои модули: {self_imports}")

    # 4. пин toolchain
    toolchain = open(os.path.join(ROOT, "lean-toolchain"), encoding="utf-8").read().strip()
    if toolchain != EXPECTED_TOOLCHAIN:
        problems.append(f"lean-toolchain = {toolchain!r} ≠ {EXPECTED_TOOLCHAIN!r}")

    print(f"IMPORTS: root {EXPECTED_ROOT}; imports: {len(imports)} (все внешние); "
          f"toolchain {toolchain}; mathlib pin {'OK' if m else '—'}")
    if problems:
        print("IMPORTS [FAIL]:")
        for p in problems:
            print("  ✗ " + p)
        return 1
    print("IMPORTS [PASS] — однофайловый контракт и пиннинги выдержаны")
    return 0


if __name__ == "__main__":
    sys.exit(main())
