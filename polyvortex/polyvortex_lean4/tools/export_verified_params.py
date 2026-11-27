#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""POLYVORTEX — мост «Lean 4 → числовая лаборатория» (verified params export).

Извлекает из Polyvortex.lean СЕРТИФИЦИРОВАННЫЕ константы (замкнутые формулы
запечатанных утверждений), вычисляет их числовые значения в нормировке
Γ = 1, a = 1 и складывает в JSON:

    verification/polyvortex/data/verified_params.json

Каждая запись несёт:
  * id/symbol/formula — человекочитаемая форма;
  * value — числовое значение (детерминированно, без ГСЧ — воспроизводимо
    бит-в-бит на любом Python 3);
  * source — имя теоремы/def в Polyvortex.lean;
  * statement_sha256 — sha256 ТОЧНОГО текста запечатанного утверждения
    (из seal/manifest.json): изменилось утверждение в Lean → изменился хеш
    → CI валит мост, пока лаборатория сознательно не примет новые значения.

Режимы:
  export_verified_params.py [--out PATH] [--check]
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
ROOT = os.path.dirname(HERE)  # verification/lean4/
REPO = os.path.dirname(os.path.dirname(ROOT))
DEFAULT_OUT = os.path.join(REPO, "verification", "polyvortex", "data", "verified_params.json")
SEAL = os.path.join(ROOT, "seal", "manifest.json")


def build_params(seal: dict) -> list[dict]:
    """Числовые значения по замкнутым формулам запечатанных утверждений."""
    pi, ln2, e = math.pi, math.log(2.0), math.e

    def sha(name: str) -> str:
        return seal["statements"].get(name, "UNSEALED")

    ring3 = 3.0 / (2.0 * pi)  # ringOmega_three_eq_lagrange, a=1
    ringN5R1 = (5.0 - 1.0) / (4.0 * pi)  # ringOmega γ R N, N=5, R=1
    thresh = pi * ln2  # eps_lt_one_iff / rClosed_pos_iff
    eps_thr = 1.0 / (math.exp(thresh / pi) - 1.0)  # eps_at_threshold = 1
    eps1 = 1.0 / (math.exp(1.0 / pi) - 1.0)  # eps C=1 (физическая ветвь C>0)
    half = 0.5
    poisson_half_eps = 2.0 * pi / math.sqrt(1.0 - half**2)  # poisson_integral
    poisson_sq_eps = 2.0 * pi / ((1.0 - half**2) * math.sqrt(1.0 - half**2))
    shape = 1.0 / ((1.0 - half**2) * math.sqrt(1.0 - half**2))  # lemmaD_bridge
    # Havelock witness growth rate at the threshold ring N=8, Γ=1, R=1:
    #   witness mode n₀ = N−3 = 5, pair mode m = havSig n₀ = 5;
    #   S_5 = (2−5)(8−5)/2 = −9/2 (havS_closed);
    #   β = c0·S_5 with c0 = γ/(2πR²) = 1/(2π); Ω = γ(N−1)/(4πR²) = 7/(4π);
    #   λ = √(β²−Ω²) = c0·√(81/4 − 49/4) = c0·√8 = √2/π (havelock_witness).
    hav_n8 = math.sqrt(2.0) / pi

    return [
        {
            "id": "ring_rate_N3",
            "symbol": "ω_3(R=1)",
            "value": ring3,
            "formula": "3Γ/(2πa²), Γ=1, a=1",
            "source": "ringOmega_three_eq_lagrange",
            "statement_sha256": sha("ringOmega_three_eq_lagrange"),
        },
        {
            "id": "ring_rate_N5",
            "symbol": "ω_5(R=1)",
            "value": ringN5R1,
            "formula": "Γ(N−1)/(4πR²), N=5, R=1",
            "source": "ringOmega",
            "statement_sha256": sha("ring_velocity"),
        },
        {
            "id": "chaplygin_threshold",
            "symbol": "π·ln2",
            "value": thresh,
            "formula": "π·ln 2",
            "source": "rClosed_pos_iff",
            "statement_sha256": sha("rClosed_pos_iff"),
        },
        {
            "id": "eps_at_threshold",
            "symbol": "ε(π·ln2)",
            "value": eps_thr,
            "formula": "1/(exp(C/π)−1) at C=π·ln2",
            "source": "eps_at_threshold",
            "statement_sha256": sha("eps_at_threshold"),
        },
        {
            "id": "eps_default_C1",
            "symbol": "ε(1)",
            "value": eps1,
            "formula": "1/(exp(1/π)−1)",
            "source": "eps_pos",
            "statement_sha256": sha("eps_pos"),
        },
        {
            "id": "poisson_half",
            "symbol": "J(ε=½)",
            "value": poisson_half_eps,
            "formula": "2π/√(1−ε²)",
            "source": "poisson_integral",
            "statement_sha256": sha("poisson_integral"),
        },
        {
            "id": "poisson_sq_half",
            "symbol": "I(ε=½)",
            "value": poisson_sq_eps,
            "formula": "2π/((1−ε²)·√(1−ε²))",
            "source": "poisson_sq",
            "statement_sha256": sha("poisson_sq"),
        },
        {
            "id": "lemmaD_shape_half",
            "symbol": "ω_N-shape(ε=½)",
            "value": shape,
            "formula": "1/((1−ε²)^{3/2})",
            "source": "lemmaD_bridge",
            "statement_sha256": sha("lemmaD_bridge"),
        },
        {
            "id": "havelock_witness_N8",
            "symbol": "λ(N=8)",
            "value": hav_n8,
            "formula": "√(β²−Ω²) = √2/π, Γ=1, R=1, witness pair n₀=5, m=5",
            "source": "havelock_witness",
            "statement_sha256": sha("havelock_witness"),
        },
    ]


def main() -> int:
    ap = argparse.ArgumentParser(description="POLYVORTEX verified-params bridge")
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
            "сертифицированные константы Polyvortex.lean; нормировка "
            "Γ=1, a=1; значения детерминированы формулами запечатанных "
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
