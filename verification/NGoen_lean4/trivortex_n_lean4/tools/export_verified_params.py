#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIVORTEX-N — мост «Lean 4 → числовая лаборатория» (verified params export).

Извлекает из NGon.lean СЕРТИФИЦИРОВАННЫЕ константы (замкнутые формулы
запечатанных утверждений), вычисляет их числовые значения в нормировке
Γ = 1, R = 1 и складывает в JSON:

    verification/trivortex_n/data/verified_params.json

Каждая запись несёт:
  * id/symbol/formula — человекочитаемая форма;
  * value — числовое значение (детерминированно, без ГСЧ — воспроизводимо
    бит-в-бит на любом Python 3);
  * source — имя теоремы/def в NGon.lean;
  * statement_sha256 — sha256 ТОЧНОГО текста запечатанного утверждения
    (из seal/manifest.json): изменилось утверждение в Lean → изменился хеш
    → CI валит мост, пока лаборатория сознательно не примет новые значения.

Нормировка: Γ = g = 1, R = 1 ⇒ ω_N = (N−1)/(4π) = (N−1)/(4πR²)·Γ.
SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # trivortex_n_lean4/
REPO = os.path.dirname(os.path.dirname(ROOT))  # корень репо (сосед polyvortex_lean4 → verification/)
DEFAULT_OUT = os.path.join(REPO, "verification", "trivortex_n", "data", "verified_params.json")
SEAL = os.path.join(ROOT, "seal", "manifest.json")


def build_params(seal: dict) -> list[dict]:
    """Числовые значения по замкнутым формулам запечатанных утверждений."""
    pi = math.pi

    def sha(name: str) -> str:
        return seal["statements"].get(name, "UNSEALED")

    def omega(n: int) -> float:
        # nGonOmega g R N при Γ=1, R=1: (N-1)/(4π)
        return (n - 1.0) / (4.0 * pi)

    return [
        {
            "id": "ngon_rate_N3",
            "symbol": "ω_3(R=1)",
            "value": omega(3),
            "formula": "Γ(N−1)/(4πR²), N=3, Γ=1, R=1 = 1/(2π)",
            "source": "nGonOmega",
            "statement_sha256": sha("nGon_omega_three"),
        },
        {
            "id": "ngon_rate_N5",
            "symbol": "ω_5(R=1)",
            "value": omega(5),
            "formula": "Γ(N−1)/(4πR²), N=5, Γ=1, R=1 = 1/π",
            "source": "nGonOmega",
            "statement_sha256": sha("nGon_field_eq"),
        },
        {
            "id": "ngon_rate_N7",
            "symbol": "ω_7(R=1)",
            "value": omega(7),
            "formula": "Γ(N−1)/(4πR²), N=7, Γ=1, R=1 = 3/(2π)",
            "source": "nGonOmega",
            "statement_sha256": sha("nGon_field_eq"),
        },
        {
            "id": "ngon_rate_N8_havelock_edge",
            "symbol": "ω_8(R=1)",
            "value": omega(8),
            "formula": "Γ(N−1)/(4πR²), N=8, Γ=1, R=1 = 7/(4π) — порог Хэвелока",
            "source": "nGonOmega",
            "statement_sha256": sha("nGon_field_eq"),
        },
        {
            "id": "shape_factor_sum_N8",
            "symbol": "Σ_{m≠0} 1/(1−u_m), N=8",
            "value": 3.5,
            "formula": "(N−1)/2 = 7/2 (sum_ker_unity)",
            "source": "sum_ker_unity",
            "statement_sha256": sha("sum_ker_unity"),
        },
        {
            "id": "side3_sq_unit",
            "symbol": "|z_1−z_0|², N=3, R=1",
            "value": 3.0,
            "formula": "3·R² (nGon_side3_sq), R=1",
            "source": "nGon_side3_sq",
            "statement_sha256": sha("nGon_side3_sq"),
        },
        {
            "id": "omega_three_side_form_a1",
            "symbol": "ω_3(a=1)",
            "value": 3.0 / (2.0 * pi),
            "formula": "3Γ/(2πa²) (nGon_omega_three), Γ=1, a=√3·R=1",
            "source": "nGon_omega_three",
            "statement_sha256": sha("nGon_omega_three"),
        },
        {
            "id": "omega_nonzero_N2",
            "symbol": "ω_2(R=1)",
            "value": omega(2),
            "formula": "Γ(N−1)/(4πR²), N=2, Γ=1, R=1 = 1/(4π) ≠ 0 (nGon_omega_ne_zero)",
            "source": "nGon_omega_ne_zero",
            "statement_sha256": sha("nGon_omega_ne_zero"),
        },
    ]


def main() -> int:
    ap = argparse.ArgumentParser(description="TRIVORTEX-N verified-params bridge")
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if not os.path.exists(SEAL):
        print(f"BRIDGE [FAIL]: нет печати {SEAL} — сначала seal_check.py --update")
        return 1
    with open(SEAL, encoding="utf-8") as f:
        seal = json.load(f)
    params = build_params(seal)
    unsealed = [p["id"] for p in params if p["statement_sha256"] == "UNSEALED"]
    if unsealed:
        print(f"BRIDGE [FAIL]: нет печати для {unsealed}")
        return 1

    doc = {
        "note": (
            "сертифицированные константы NGon.lean (TRIVORTEX-N, file 1/5); "
            "нормировка Γ=1, R=1; значения детерминированы формулами запечатанных "
            "утверждений; statement_sha256 связывает запись с печатью; "
            "файл бит-в-бит детерминирован — метки времени запрещены"
        ),
        "params": params,
    }
    payload = json.dumps(doc, ensure_ascii=False, indent=1, sort_keys=False) + "\n"

    if args.check:
        if not os.path.exists(args.out):
            print(
                f"BRIDGE [SKIP]: лаборатория ещё не приняла параметры ({args.out}); "
                "запустите без --check для первой выгрузки"
            )
            return 0
        with open(args.out, encoding="utf-8") as f:
            old = f.read()
        if old == payload:
            print("BRIDGE [PASS] — мост синхронен с печатью")
            return 0
        print(
            "BRIDGE [FAIL]: verified_params.json расходится с печатью "
            "(осознанный пересмотр: запустите без --check)"
        )
        return 1

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(payload)
    print(f"BRIDGE [UPDATED]: {len(params)} сертифицированных констант → {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
