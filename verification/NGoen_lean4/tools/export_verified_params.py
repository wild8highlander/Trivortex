#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIVORTEX-N Lean 4 — мост в числовую лабораторию (гейт 5/5, пятифайловый контракт).

Для КАЖДОГО из пяти файлов программы (NGon, NSide, NCore, NRoots, NFlow):
  1. data/verified_params_<stem>.json — сертифицированные константы; каждая запись
     связана statement_sha256 с печатью seal/manifest[_<stem>].json — гейт ва́лит
     проверку, если константа ссылается на несуществующее утверждение или если
     запечатанное утверждение изменилось после приёмки лабораторией;
  2. data/<stem>_numeric_check.json — отчёт лаборатории: all_pass обязан быть true,
     худшая невязка — в допуске.

Режимы: --check (CI) / --list. Код возврата: 0 — мост синхронен, 1 — гейт сработал.
SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FILES = ["NGon", "NSide", "NCore", "NRoots", "NFlow"]
TOLERANCE = 1e-9


def seal_manifest(stem: str) -> dict:
    name = "manifest.json" if stem == "NGon" else f"manifest_{stem.lower()}.json"
    return json.load(open(os.path.join(ROOT, "seal", name), encoding="utf-8"))


def check_file(stem: str) -> tuple[bool, list[str]]:
    problems: list[str] = []
    params_path = os.path.join(ROOT, "data", f"verified_params_{stem.lower()}.json")
    lab_path = os.path.join(ROOT, "data", f"{stem.lower()}_numeric_check.json")

    if stem == "NGon" and not os.path.isfile(params_path):
        # файл 1/5 хранит параметры в исходном формате data/verified_params.json
        params_path = os.path.join(ROOT, "data", "verified_params.json")

    params = json.load(open(params_path, encoding="utf-8"))
    lab = json.load(open(lab_path, encoding="utf-8"))
    seal = seal_manifest(stem)
    statements = seal["statements"]

    if not lab.get("all_pass", False):
        problems.append(f"{stem}: лаборатория reported all_pass=false")
    worst = lab.get("worst_residual", 0.0)
    if worst >= TOLERANCE:
        problems.append(f"{stem}: худшая невязка {worst:.3e} ≥ допуска {TOLERANCE:.0e}")

    for p in params.get("params", []):
        sha = p.get("statement_sha256", "")
        if sha == "UNSEALED" or sha not in statements.values():
            problems.append(
                f"{stem}: константа {p.get('id')} не связана с печатью "
                "(statement_sha256 отсутствует в seal-манифесте)")
    return (not problems), problems


def main() -> int:
    ap = argparse.ArgumentParser(description="Мост в числовую лабораторию (пять файлов)")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.list:
        for stem in FILES:
            lab_path = os.path.join(ROOT, "data", f"{stem.lower()}_numeric_check.json")
            lab = json.load(open(lab_path, encoding="utf-8"))
            print(f"{stem:8s} checks={len(lab.get('checks', [])):2d} "
                  f"worst={lab.get('worst_residual', 0.0):.3e} "
                  f"pass={lab.get('all_pass')}")
        return 0

    ok_all = True
    for stem in FILES:
        ok, problems = check_file(stem)
        status = "PASS" if ok else "FAIL"
        print(f"BRIDGE [{status}] — {stem}")
        for problem in problems:
            print(f"  ✗ {problem}")
        ok_all = ok_all and ok

    print("BRIDGE [PASS] — мост синхронен с печатью, лаборатория зелёная"
          if ok_all else "BRIDGE [FAIL]")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
