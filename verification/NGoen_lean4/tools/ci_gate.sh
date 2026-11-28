#!/usr/bin/env bash
# TRIVORTEX-N NGON Lean 4 — единый CI-гейт verification/lean4.
#
# Порядок (заметка научного руководителя №1, «строгий конвейер»):
#   1. check_imports.py     — эквивалент `lake exe mk_all --check` для
#                             однофайлового пакета (нет осиротевших модулей,
#                             пиннинги toolchain/Mathlib на месте);
#   2. axioms_gate.py       — lake env lean NGon.lean (полная компиляция
#                             с эквивалентом --wfail/--iofail: warning = FAIL),
#                             затем #print axioms по КАЖДОЙ теореме: набор аксиом
#                             обязан быть точно [propext, Classical.choice,
#                             Quot.sound]; sorry/axiom/native_decide/unsafe —
#                             запрещены; число отпечатков = числу директив;
#   3. seal_check.py        — печать утверждений не тронута (замечание №2);
#   4. lint_conventions.py  — конвенции Mathlib + ракет докстрингов (№3);
#   5. export_verified_params.py --check — мост в числовую лабораторию
#                             синхронен с запечатанными утверждениями (№6).
#
# Локально:   bash tools/ci_gate.sh
# Переменные: LAKE (по умолчанию lake из PATH), ELAN_HOME — при необходимости.
# SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
# SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$HERE")"
FAILED=()
# GATE_SKIP="bridge" — исключить именованные шаги (напр., в Docker-образе,
# где нет соседнего polyvortex для шага-моста)
SKIP="${GATE_SKIP:-}"
run_step() {  # run_step NAME cmd...
  local name="$1"; shift
  case ",$SKIP," in *",$name,"*) echo "[skip] $name (GATE_SKIP)"; return 0;; esac
  "$@"
}

step() { printf '\n──── %s ────\n' "$1"; }

FILES=(NGon NSide NCore NRoots NFlow)

step "1/5 imports (пятифайловый контракт)"
run_step imports python3 "$HERE/check_imports.py" || FAILED+=("imports")

step "2/5 axioms gate (полная компиляция всех пяти файлов)"
for f in "${FILES[@]}"; do
  run_step axioms_gate python3 "$HERE/axioms_gate.py" --file "$ROOT/$f.lean" \
    --workdir "$ROOT" --log "$ROOT/axioms_gate.log" || FAILED+=("axioms_gate:$f")
done

step "3/5 seal (печать утверждений всех пяти файлов)"
for f in "${FILES[@]}"; do
  run_step seal python3 "$HERE/seal_check.py" --check --file "$ROOT/$f.lean" \
    || FAILED+=("seal:$f")
done

step "4/5 conventions + docstring ratchet (все пять файлов)"
for f in "${FILES[@]}"; do
  run_step lint python3 "$HERE/lint_conventions.py" --file "$ROOT/$f.lean" \
    || FAILED+=("lint:$f")
done

step "5/5 bridge (verified params + числовая лаборатория, все пять файлов)"
run_step bridge python3 "$HERE/export_verified_params.py" --check || FAILED+=("bridge")

printf '\n════ CI GATE: %s ════\n' \
  "$([[ ${#FAILED[@]} -eq 0 ]] && echo 'PASS — Lean-уровень чист' || echo "FAIL: ${FAILED[*]}")"
[[ ${#FAILED[@]} -eq 0 ]]
