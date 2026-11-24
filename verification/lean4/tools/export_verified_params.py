#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIVORTEX — мост «Lean 4 → числовая лаборатория» (verified params export).

Извлекает из Trivortex.lean СЕРТИФИЦИРОВАННЫЕ константы (утверждения теорем
и сигнатуры определений), вычисляет их числовые значения по закрытым формулам
и складывает в JSON, который читает числовая лаборатория:

    verification/trivortex_master/data/verified_params.json

Каждая запись несёт:
  * id/symbol/formula — человекочитаемая форма;
  * value — числовое значение в нормировке Γ = 1, a = 1 (детерминированно,
    без ГСЧ — воспроизводимо бит-в-бит на любом Python 3);
  * source — имя теоремы/def в Trivortex.lean;
  * statement_sha256 — sha256 ТОЧНОГО текста запечатанного утверждения:
    изменилось утверждение в Lean → изменился хеш → CI валит мост, пока
    лаборатория сознательно не примет новые значения (видимый пересмотр).

Числовая сторона (tests/test_lagrange_regression.py) НЕ хардкодит ожидания,
а читает их отсюда: симуляции гарантированно запускаются на верифицированных
данных. Обратная связь: расхождение симуляции с формально доказанными
свойствами = баг симулятора или неверная интерпретация модели (см. тесты).

Режимы:
  export_verified_params.py [--out PATH] [--check]
SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # verification/lean4/
REPO = os.path.dirname(os.path.dirname(ROOT))  # корень репозитория
DEFAULT_OUT = os.path.join(
    REPO, "verification", "trivortex_master", "data", "verified_params.json"
)

RE_THEOREM = re.compile(
    r"(?m)^(?:private\s+|protected\s+|noncomputable\s+)*(theorem|lemma)\s+([A-Za-z0-9_']+)"
)
RE_DEF = re.compile(r"(?m)^(?:private\s+|protected\s+|noncomputable\s+)*def\s+([A-Za-z0-9_']+)")


def _statement_end(src: str, start: int) -> int:
    """Позиция `:=`, открывающего доказательство/тело, от начала декларации."""
    pos, depth = start, 0
    while pos < len(src):
        ch = src[pos]
        if ch in "([{«":
            depth += 1
        elif ch in ")]}»":
            depth -= 1
        elif depth == 0 and src.startswith(":=", pos):
            return pos
        pos += 1
    return len(src)


def collect(src: str) -> tuple[dict[str, str], dict[str, str]]:
    """(теоремы, def-сигнатуры): {имя: нормализованный текст}."""
    thm, df = {}, {}
    for m in RE_THEOREM.finditer(src):
        stmt = re.sub(r"\s+", " ", src[m.start():_statement_end(src, m.start())]).strip()
        thm[m.group(2)] = stmt
    for m in RE_DEF.finditer(src):
        stmt = re.sub(r"\s+", " ", src[m.start():_statement_end(src, m.start())]).strip()
        df[m.group(1)] = stmt
    return thm, df


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ── реестр сертифицированных констант (нормировка Γ=1, a=1) ────────────────
PI = math.pi

REGISTRY = [
    dict(id="lagrange_omega", symbol="ω", formula="3Γ/(2π·a²)",
         value=3.0 / (2.0 * PI), source="lagrangeOmega", kind="def",
         note="частота вращения лагранжева треугольника (§7)"),
    dict(id="lagrange_period", symbol="T", formula="4π²·a²/(3Γ)",
         value=4.0 * PI ** 2 / 3.0, source="lag_period_closed", kind="theorem",
         note="период: 2π/ω = 4π²a²/(3Γ) (§7)"),
    dict(id="anchor_H", symbol="H₀", formula="0",
         value=0.0, source="lagrange_anchor_H", kind="theorem",
         note="якорь гамильтониана на лагранжевом решении, a=1 (§7)"),
    dict(id="anchor_P", symbol="P₀", formula="0",
         value=0.0, source="lagrange_anchor_P", kind="theorem",
         note="якорь импульса P (центроид в нуле) (§7)"),
    dict(id="anchor_Q", symbol="Q₀", formula="0",
         value=0.0, source="lagrange_anchor_Q", kind="theorem",
         note="якорь импульса Q (§7)"),
    dict(id="anchor_I", symbol="I₀", formula="Γ",
         value=1.0, source="lagrange_anchor_I", kind="theorem",
         note="якорь углового импульса I = ΣΓ|r|² = Γ при a=1 (§7)"),
    dict(id="gamma_static", symbol="γ_stat", formula="−1/2",
         value=-0.5, source="s10_col_static", kind="theorem",
         note="стационарная точка симметричной коллинеарной ветви (ω=0) (§10)"),
    dict(id="gamma_pitchfork", symbol="γ_c", formula="−5/4",
         value=-1.25, source="s10_col_pitchfork", kind="theorem",
         note="бифуркация вил коллинеарных центр-конфигураций (§10)"),
    dict(id="coercivity_coeff", symbol="c_coer", formula="Γ²/(12π·a⁴)",
         value=1.0 / (12.0 * PI), source="s10_coercive", kind="theorem",
         note="коэрцитивная константа H − H₀ ≥ (Γ²/12πa⁴)·Σ(r²ᵢⱼ−a²)² (§10, a=1)"),
    dict(id="eig_translation", symbol="λ_trans", formula="±i·(2π/Γ)·ω = ±3i",
         value=3.0, source="eig_trans1", kind="theorem",
         note="трансляционные моды: |λ| = 3 в 2π/Γ-масштабе (§8)"),
    dict(id="eig_shape", symbol="λ_shape", formula="±i·(2π/Γ)·ω = ±3i",
         value=3.0, source="eig_shapeU", kind="theorem",
         note="мода колебания формы: |λ| = 3 в 2π/Γ-масштабе (§8)"),
    dict(id="conservation_H", symbol="dH/dt", formula="0",
         value=None, source="H_kirchhoff_conserved", kind="theorem",
         note="сохранение H вдоль любого решения Кирхгофа (§4)"),
    dict(id="conservation_P", symbol="dP/dt", formula="0",
         value=None, source="P_kirchhoff_conserved", kind="theorem",
         note="сохранение P (§4)"),
    dict(id="conservation_Q", symbol="dQ/dt", formula="0",
         value=None, source="Q_kirchhoff_conserved", kind="theorem",
         note="сохранение Q (§4)"),
    dict(id="conservation_I", symbol="dI/dt", formula="0",
         value=None, source="I_kirchhoff_conserved", kind="theorem",
         note="сохранение I (§4)"),
]


def build_payload(path_lean: str) -> dict:
    src = open(path_lean, encoding="utf-8").read()
    thm, df = collect(src)
    entries = []
    for reg in REGISTRY:
        stmt = (thm.get(reg["source"]) if reg["kind"] == "theorem"
                else df.get(reg["source"]))
        if stmt is None:
            raise SystemExit(
                f"EXPORT [FAIL]: в Trivortex.lean не найден источник `{reg['source']}` "
                f"(id={reg['id']}) — реестр и формализация рассинхронизированы"
            )
        entries.append({
            "id": reg["id"],
            "symbol": reg["symbol"],
            "formula": reg["formula"],
            "value": reg["value"],
            "units": "Γ=1, a=1 (нормировка лестницы)",
            "source": reg["source"],
            "source_kind": reg["kind"],
            "statement_sha256": digest(stmt),
            "note": reg["note"],
        })
    return {
        "file": "Trivortex.lean",
        "section_span": "§1–§10",
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "entries": entries,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Экспорт верифицированных параметров")
    ap.add_argument("--lean", default=os.path.join(ROOT, "Trivortex.lean"))
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--check", action="store_true",
                    help="сравнить с существующим файлом; дрейф = FAIL")
    args = ap.parse_args()

    payload = build_payload(args.lean)
    body = {k: v for k, v in payload.items() if k != "generated_utc"}

    if args.check:
        if not os.path.isfile(args.out):
            print(f"EXPORT [FAIL]: моста нет ({args.out}); выполните экспорт без --check")
            return 1
        committed = json.load(open(args.out, encoding="utf-8"))
        committed_body = {k: v for k, v in committed.items() if k != "generated_utc"}
        if committed_body == body:
            print(f"EXPORT [PASS]: мост синхронен — {len(body['entries'])} констант, "
                  "хеши утверждений совпадают с Trivortex.lean")
            return 0
        # локализовать дрейф
        old = {e["id"]: e for e in committed.get("entries", [])}
        for e in body["entries"]:
            o = old.get(e["id"])
            if o is None:
                print(f"  ✗ новая константа: {e['id']}")
            elif o["statement_sha256"] != e["statement_sha256"]:
                print(f"  ✗ {e['id']}: утверждение {e['source']} изменилось "
                      f"({o['statement_sha256'][:10]}… → {e['statement_sha256'][:10]}…)")
            elif o.get("value") != e["value"]:
                print(f"  ✗ {e['id']}: значение {o.get('value')} → {e['value']}")
        gone = [i for i in old if i not in {e["id"] for e in body["entries"]}]
        for g in gone:
            print(f"  ✗ исчезла константа: {g}")
        print("EXPORT [FAIL]: мост рассинхронизирован с Trivortex.lean — "
              "числовая лаборатория должна СОЗНАТЕЛЬНО принять новые значения "
              "(перезапись файла + ревью)")
        return 1

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"EXPORT: {len(body['entries'])} верифицированных констант → {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
