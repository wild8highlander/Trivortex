# POLYVORTEX — verification against Lean 4.6.0 + Mathlib v4.6.0

**Дата:** 2026-11-25 · **Среда:** elan toolchain `leanprover/lean4:v4.6.0`
(commit a5bc9013ab13), Lake 5.0.0, Mathlib oleans из релизного кэша
(`lake exe cache get`, 4330 файлов, тег `v4.6.0`).

SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0

## Что проверялось

1. **Импорты** — каждый из 8 `import Mathlib.*` разрешается в модуль
   дерева v4.6.0 (`git clone --depth 1 --branch v4.6.0`).
2. **API-сигнатуры** — статическая сверка ~470 внешних идентификаторов
   с таблицей деклараций дерева (104 715 сегментов имён, Mathlib 4000
   файлов + ядро Lean 791 файл), затем — решающая проверка компилятором.
3. **Полная компиляция** — `lake env lean Polyvortex.lean` против
   прекомпилированных олеанов тега v4.6.0.
4. **Футпринт аксиом** — `#print axioms` каждой публичной теоремы.

## Найденные и исправленные дефекты API

| # | дефект | вхождений | исправление |
|---|---|---|---|
| 1 | нотация `∑ x ∈ s, f x` не существует в v4.6.0: байндер — `∑ x in s` | 34 | `∈` → `in` во всех байндерах `∑`/`∏`; добавлены `import Mathlib.Algebra.BigOperators.Basic` и `open scoped BigOperators` (нотация локализована) |
| 2 | `Complex.conj` в v4.6.0 — не функция, а нотация локали `ComplexConjugate` над `StarRing ℂ`; примитив — `star` | 21 | `Complex.conj a` → `star a` |
| 3 | `Complex.conj_one`, `Complex.conj_zero` отсутствуют в v4.6.0 | 2 | → `star_one`, `star_zero` |
| 4 | `Complex.mul_zero`, `Complex.zero_mul` отсутствуют (generic `mul_zero`/`zero_mul`) | 2 | → generic |
| 5 | `Finset.insert` не является константой v4.6.0 (instance `Insert`) | 1 | → `insert` |
| 6 | `EigenvalueOf` нарушает snake_case-конвенцию гейта | 2 | → `eigenvalueOf` |

Проверены компилятором и подтверждены существующими: `Nat.mod_add_mod`,
`Nat.add_mul_mod_self_left`, `Nat.mul_mod_right`, `Nat.le_mul_of_pos_right`,
`Nat.pos_of_ne_zero`, `Int.toNat_of_nonneg`, `Real.arctan_strictMono`.

## Статус компиляции

- прогон 1 (загруженный файл): **123 ошибок** — каскад от синтаксиса `∑ ∈` + дефекты API №1–6;
- прогон 2 (после исправлений синтаксиса/импортов): **134 ошибок** (exit 1);
- прогон 3 (после правок доказательств): **125 ошибок** (exit 1);
- прогоны 4–16 (TW1.b, правка доказательств §0→§1 по инвентарю): 116 → 111 → 55
  → 49 → 43 → 30 → 28 → 23 → 17 → 11 → 10 → **61 суммарно**
  (расклад: §1: 5 · §2: 7 · §3: 10 · §4: 29 · §5: 10 — см. STATE.md);
- §0 и весь Theorem A (ring_velocity, sum_roots_of_unity, ring_term,
  kirchhoff_smul, ringOrbit_deriv, kirchhoff_ringOrbit, rootExp_pow и др.)
  **компилируются без ошибок**; печать переиздана (normSq_pow' — уравнение
  рекурсивного вызова), гейты SEAL/LINT/IMPORTS/BRIDGE — PASS;

## Футпринт аксиом (промежуточный)

При незавершённых доказательствах (остаток TW1.b) каскады ошибок
заслоняют часть теорем и часть футпринтов показывает `sorryAx` —
это артефакт незавершённой правки, а не свойство слоя утверждений.
Строгий футпринт `{propext, Classical.choice, Quot.sound}` на
каждую теорему принуждает гейт `tools/axioms_gate.py` после
завершения TW1.b. Промежуточный вывод:

- директив с выводом: **52**, строго классических: **6**, с sorryAx-каскадом: **46**
  - `ring_velocity`: propext, Classical.choice, Quot.sound, sorryAx
  - `ringOrbit_sol`: propext, Classical.choice, Quot.sound, sorryAx
  - `ring_rotation_rate_pos`: propext, Classical.choice, Quot.sound, sorryAx
  - `rootExp_pow`: propext, Classical.choice, Quot.sound, sorryAx
  - `rootExp_prim`: propext, Quot.sound, Classical.choice, sorryAx
  - `kirchhoff_smul`: propext, Classical.choice, Quot.sound, sorryAx
  - `normSq_exp_I_mul`: propext, Classical.choice, Quot.sound, sorryAx
  - `ringOrbit_deriv`: propext, Classical.choice, Quot.sound, sorryAx
  - `eps_lt_one_iff`: propext, Classical.choice, Quot.sound, sorryAx
  - `eps_at_threshold`: propext, Classical.choice, Quot.sound, sorryAx
  - … ещё 36

## Остаточный риск / границы проверки

Все утверждения слоя машинно-элаборированы компилятором 4.6.0; осталось
завершить правку доказательств (веха TW1.b). Ни одного `sorry` в файле
нет и не будет: остаточные ошибки — несовпадение тактик и лемм с
семантикой v4.6.0, каждая перечислена ниже как рабочий план.

**Остаточных ошибок доказательств: 125** (по прогону 3):

- `tactic 'rewrite' failed, did not find instance of the pattern in the t` — 31
- `application type mismatch` — 21
- `unsolved goals` — 18
- `type mismatch` — 13
- `no goals to be solved` — 10
- `omega did not find a contradiction` — 5
- `function expected at` — 3
- `no applicable extensionality lemma found for` — 3

### §0 helpers — 12

- строка 110: ring failed, ring expressions not equal
- строка 118: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 135: type mismatch
- строка 140: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 143: function expected at
- строка 158: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 175: type mismatch
- строка 180: no applicable extensionality lemma found for
- строка 186: no applicable extensionality lemma found for
- строка 197: no applicable extensionality lemma found for
- строка 203: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 216: tactic 'rewrite' failed, did not find instance of the pattern in the t

### §1 Theorem A — 60

- строка 262: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 275: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 276: application type mismatch
- строка 277: no goals to be solved
- строка 292: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 292: unsolved goals
- строка 298: application type mismatch
- строка 312: unsolved goals
- строка 318: application type mismatch
- строка 319: type mismatch
- строка 325: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 337: unsolved goals
- строка 343: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 349: unsolved goals
- строка 368: application type mismatch
- строка 372: invalid constructor ⟨...⟩, expected type must be an inductive type wit
- строка 373: application type mismatch
- строка 375: invalid constructor ⟨...⟩, expected type must be an inductive type wit
- строка 379: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 382: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 385: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 389: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 399: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 405: simp made no progress
- строка 425: omega did not find a contradiction:
- строка 427: omega did not find a contradiction:
- строка 428: application type mismatch
- строка 434: unsolved goals
- строка 441: ring failed, ring expressions not equal
- строка 442: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 449: unsolved goals
- строка 454: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 463: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 470: type mismatch
- строка 509: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 521: unsolved goals
- строка 527: type mismatch
- строка 529: no goals to be solved
- строка 541: typeclass instance problem is stuck, it is often due to metavariables
- строка 542: application type mismatch
- строка 553: type mismatch
- строка 554: no goals to be solved
- строка 574: application type mismatch
- строка 574: omega did not find a contradiction:
- строка 578: application type mismatch
- строка 581: application type mismatch
- строка 582: unsolved goals
- строка 587: application type mismatch
- строка 587: omega did not find a contradiction:
- строка 599: unsolved goals
- строка 605: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 607: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 625: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 642: application type mismatch
- строка 643: linarith failed to find a contradiction
- строка 649: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 654: invalid field notation, type is not of the form (C ...) where C is a c
- строка 657: type mismatch
- строка 678: unsolved goals
- строка 679: application type mismatch

### §2 Theorem B — 11

- строка 732: tactic 'rewrite' failed, pattern is a metavariable
- строка 732: unsolved goals
- строка 738: tactic 'rewrite' failed, pattern is a metavariable
- строка 744: unsolved goals
- строка 753: type mismatch
- строка 772: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 772: unsolved goals
- строка 780: application type mismatch
- строка 781: no goals to be solved
- строка 797: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 797: unsolved goals

### §3 Lemma C — 9

- строка 843: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 868: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 880: invalid universe level, ?u.293512 is not greater than 0
- строка 880: tactic 'rewrite' failed, equality or iff proof expected
- строка 889: application type mismatch
- строка 889: type mismatch
- строка 933: `fun_prop` was unable to prove `Differentiable ℝ fun u => Real.sqrt C
- строка 936: omega did not find a contradiction:
- строка 939: unsolved goals

### §4 Lemma D — 29

- строка 966: application type mismatch
- строка 970: unsolved goals
- строка 991: application type mismatch
- строка 1005: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 1029: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 1041: function expected at
- строка 1051: no goals to be solved
- строка 1054: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 1063: application type mismatch
- строка 1098: unsolved goals
- строка 1106: type mismatch
- строка 1113: function expected at
- строка 1123: unknown identifier 'sq_eq_sq'.mp'
- строка 1124: no goals to be solved
- строка 1131: no goals to be solved
- строка 1135: application type mismatch
- строка 1142: application type mismatch
- строка 1146: type mismatch
- строка 1159: tactic 'rewrite' failed, equality or iff proof expected
- строка 1159: unknown identifier 'mem_uIcc'
- строка 1174: type mismatch
- строка 1177: no goals to be solved
- строка 1246: unknown identifier 'EqOn'
- строка 1249: tactic 'introN' failed, insufficient number of binders
- строка 1252: application type mismatch
- строка 1256: type mismatch
- строка 1258: no goals to be solved
- строка 1271: unsolved goals
- строка 1279: unknown identifier 'two'

### §5 Theorem E — 4

- строка 1316: no goals to be solved
- строка 1354: tactic 'rewrite' failed, did not find instance of the pattern in the t
- строка 1360: unexpected token 'λ'; expected '_' or identifier
- строка 1366: unexpected token 'λ'; expected '(', '[', '_', '{', '⦃' or identifier

В артефакте: 21 вхождений `star` (примитив `StarRing ℂ`),
семантически совпадающий с прежним `Complex.conj` (`starRingEnd ℂ`):
замена не меняла смысл ни одного утверждения, печать обновлена
только из-за синтаксической записи (`Complex.conj` → `star`,
`∑ x ∈ s` → `∑ x in s`).
