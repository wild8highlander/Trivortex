#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""POLYVORTEX Lean 4 — seal-check: дисциплина «сначала утверждение, потом доказательство».

Механика:
  * из Polyvortex.lean извлекается КАЖДОЕ объявление теоремы/леммы вместе с
    полным текстом утверждения (от имени до `:=` — байндеры, гипотезы,
    заключение);
  * нормализованный текст хешируется sha256 и фиксируется в
    seal/manifest.json («печать», seal);
  * `--check` сравнивает текущий исходник с печатью и ва́лит CI, если
    какое-либо утверждение ИЗМЕНИЛОСЬ, появилось или исчезло.

Зачем это нужно: самая коварная ошибка формализации — незаметное
ослабление условий теоремы под имеющееся доказательство (ослабить
гипотезу, поменять знак, «подкрутить» константу). Печать фиксирует
утверждения ДО начала работы над доказательством; пересмотр допускается
только ЯВНО — обновлением печати (`--update`), что видно в ревью diff'ом.

Режимы:
  seal_check.py --check [--file F]          проверка против seal/manifest.json
  seal_check.py --update                    ЯВНОе обновление печати
  seal_check.py --show NAME                 показать запечатанное утверждение
  seal_check.py --list                      список запечатанных имён

Замечание о докстрингах: комментарии `/-- ... -/` ПРЕДШЕСТВУЮТ теореме и в
хеш утверждения не входят — правка документации печать не трогает.
Изменения в доказательстве (`:= ...`) также не влияют на хеш.
SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # verification/lean4/

# (private|protected|noncomputable)? theorem|lemma NAME ... :=  (на верхнем уровне)
RE_DECL = re.compile(
    r"(?m)^(?:private\s+|protected\s+|noncomputable\s+)*(theorem|lemma)\s+([A-Za-z0-9_']+)"
)

PAIRS = {"(": ")", "[": "]", "{": "}", "«": "»"}


def extract_statements(src: str) -> dict[str, str]:
    """{имя: нормализованный текст утверждения} для всех theorem/lemma."""
    out: dict[str, str] = {}
    for m in RE_DECL.finditer(src):
        kind, name = m.group(1), m.group(2)
        start = m.start()
        pos = m.end()
        depth = 0
        stmt_end = -1
        while pos < len(src):
            ch = src[pos]
            if ch in PAIRS:
                depth += 1
            elif ch in PAIRS.values():
                depth -= 1
            elif depth == 0 and src.startswith(":=", pos):
                stmt_end = pos
                break
            elif depth == 0 and ch == "\n":
                # многострочные утверждения — ок; прерываем только по ':='
                pass
            pos += 1
        if stmt_end < 0:  # не нашли ':=' — берём до конца файла (аномалия)
            stmt_end = len(src)
        stmt = src[start:stmt_end]
        # нормализация: пробельные последовательности → один пробел
        stmt = re.sub(r"\s+", " ", stmt).strip()
        out[name] = stmt
    return out


def digest(stmt: str) -> str:
    return hashlib.sha256(stmt.encode("utf-8")).hexdigest()


def manifest_path(seal_dir: str) -> str:
    return os.path.join(seal_dir, "manifest.json")


def build_manifest(src: str) -> dict:
    stmts = extract_statements(src)
    return {
        "file": "Polyvortex.lean",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "theorem_count": len(stmts),
        "statements": {name: digest(s) for name, s in sorted(stmts.items())},
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Seal-check утверждений Polyvortex.lean")
    ap.add_argument("--file", default=os.path.join(ROOT, "Polyvortex.lean"))
    ap.add_argument("--seal-dir", default=os.path.join(ROOT, "seal"))
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--update", action="store_true")
    ap.add_argument("--show", default=None, metavar="NAME")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    src = open(args.file, encoding="utf-8").read()
    stmts = extract_statements(src)
    path = manifest_path(args.seal_dir)

    if args.show:
        name = args.show
        if name not in stmts:
            print(f"нет такой теоремы: {name}")
            return 1
        print(stmts[name])
        return 0

    if args.list:
        for name in sorted(stmts):
            print(name)
        return 0

    if args.update:
        os.makedirs(args.seal_dir, exist_ok=True)
        man = build_manifest(src)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(man, fh, indent=1, ensure_ascii=False, sort_keys=False)
            fh.write("\n")
        print(
            f"SEAL [UPDATED]: печать обновлена ЯВНО — {man['theorem_count']} утверждений в {path}"
        )
        print(
            "SEAL: это видимое действие в ревью; «подкрутить» утверждение незаметно больше нельзя"
        )
        return 0

    # режим --check (основной для CI)
    if not os.path.isfile(path):
        print(f"SEAL [FAIL]: нет печати {path}; выполните seal_check.py --update")
        return 1
    man = json.load(open(path, encoding="utf-8"))
    sealed = man.get("statements", {})

    added = [n for n in stmts if n not in sealed]
    removed = [n for n in sealed if n not in stmts]
    changed = [n for n in stmts if n in sealed and digest(stmts[n]) != sealed[n]]

    print(f"SEAL: запечатано {len(sealed)}; в исходнике {len(stmts)} утверждений")
    if added or removed or changed:
        print(
            "SEAL [FAIL] — утверждениЯ изменились; пересмотр ДОЛЖЕН быть явным (seal_check.py --update):"
        )
        for n in added[:15]:
            print(f"  + новое утверждение: {n}")
        for n in removed[:15]:
            print(f"  − исчезло утверждение: {n}")
        for n in changed[:15]:
            print(
                f"  ~ изменено утверждение: {n} (было {sealed[n][:12]}…, стало {digest(stmts[n])[:12]}…)"
            )
        if len(added) + len(removed) + len(changed) > 15:
            print(f"  … всего {len(added) + len(removed) + len(changed)} расхождений")
        return 1
    print("SEAL [PASS] — все утверждения совпадают с печатью")
    return 0


if __name__ == "__main__":
    sys.exit(main())
