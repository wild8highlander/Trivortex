# TW1.b — completion report: the artifact compiles clean

**Дата:** 2026-11-26 · **Статус:** TW1.b ЗАВЕРШЁН. Отчёт `VERIFICATION_v460.md`
фиксировал промежуточное состояние (125 ошибок по прогону 3); настоящий документ —
финал того же прохода.

SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0

## Результат

`lake env lean Polyvortex.lean` → **EXIT 0: 0 ошибок, 0 `sorry`**, против реальных
оленанов Mathlib v4.6.0. Все 26 директив `#print axioms` дают строго классический
набор `{propext, Classical.choice, Quot.sound}` — `sorryAx` отсутствует для всех
перечисленных теорем.

Полный проход всех пяти гейтов (`bash tools/ci_gate.sh`) зафиксирован машинным
логом: [`docs/evidence/ci_gate_2026-11-26.log`](evidence/ci_gate_2026-11-26.log):

| # | гейт | вердикт |
|---|---|---|
| 1 | `check_imports.py` — однофайловый контракт + пиннинг | **PASS** |
| 2 | `axioms_gate.py` — полная компиляция + 26 футпринтов | **PASS** |
| 3 | `seal_check.py --check` — 62 утверждения совпадают с печатью | **PASS** |
| 4 | `lint_conventions.py` — конвенции + 100% докстрингов (79/79) | **PASS** |
| 5 | `export_verified_params.py --check` — мост синхронен с печатью | **PASS** |

Машинный вывод футпринтов аксиом: [`docs/evidence/axioms_gate_2026-11-26.log`](evidence/axioms_gate_2026-11-26.log)
— 26 строк вида `'Polyvortex.<theorem>' depends on axioms: [propext, Classical.choice, Quot.sound]`.

## Что изменилось относительно v1.0.1 (аудиторский слепок)

| параметр | v1.0.1 (audit) | v1.0.2 (artifact) |
|---|---|---|
| строк в файле | 1,439 | 1,609 |
| теорем | 61 | 62 (+ локальная `sq_neg`) |
| определений | 17 | 17 |
| деклараций (ракет lint) | 78 | 79 |
| директив `#print axioms` | 26 | 26 |
| компиляция | ожидалась | **EXIT 0** |
| печать | sha256 × 61 | переиздана: sha256 × 62 (2026-11-26T08:20:16Z) |

Смысловой слой утверждений не менялся: правка была доказательственной (тактики,
касты, явные аргументы транспорт-лемм), плюс добавлена локальная вспомогательная
теорема `sq_neg` (в Mathlib v4.6.0 корневой `sq_neg` отсутствует — рецепт в
[`MATHLIB_RECIPES.md`](MATHLIB_RECIPES.md) §7).

## Хронология прохода (по committed-логам)

- прогоны 1–3: 123 → 134 → 125 ошибок (API-дефекты v4.6.0 — см. `VERIFICATION_v460.md`);
- прогоны 4–16 (`logs/compile4..16`): 116 → 62, секции закрывались по порядку §0→§5;
- прогон 44 (`compile44.log` в истории репозитория): 14 ошибок — хвост §4 и §5;
- финальный прогон (compile55): **0 ошибок**; полный CI 5/5 PASS (лог в evidence).

Сводный график спуска: `assets/charts/proof-fix-descent.png`.

## Классы правок последней мили (compile44 → compile55)

1. `hasDerivAt_poissonG` (финал h1): связка `rw [← hksq, cos_half_tan hφ]` +
   `field_simp` с positivity-гипотезами; остаток чисто алгебраический — добит `ring`.
2. `poisson_half`: `Continuous.intervalIntegrable` — явный `(μ := volume)` и сборка
   через `integral_add_adjacent_intervals`.
3. `htrans`: β-редексы в ветке `integral_congr` — `intro x _; simp only []` перед `rw`.
4. Футпринты §5 и Theorem E: `Real.cos (?x - ?y)` под β-редексами, литералы `2 * Real.pi`
   вместо несуществующего идентификатора `two`.
5. Синтаксические следы старых правок в Theorem E — прочистка зоны строк 1470–1500.

Детали и полный каталог приёмов: [`MATHLIB_RECIPES.md`](MATHLIB_RECIPES.md).

## Что осталось (вне TW1.b)

- `lake build` полного пакета (файл чист; остаётся упаковка и сборка audit-копии в CI);
- TW2: числовые лестницы для N-кольца, регрессия на `verified_params.json`, галерея;
- TW3: `corotLin` как явный ℝ-линейный оператор + теорема о ядре;
- TW4: спектральное доказательство устойчивости при N ≤ 7 (дискретное Фурье);
- TW5: неустойчивость при N ≥ 8 → `havelockClassification` становится теоремой.
