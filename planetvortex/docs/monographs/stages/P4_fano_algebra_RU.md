---
title: "P4 — алгебра PSL(2,7)"
subtitle: "PLANETVORTEX — the stage monograph (P)"
---

## Утверждение

168 автоморфизмов, две модели Фано (циклическая и двоичная) с явным изоморфизмом, сопряжённость двух копий группы внутри S₇, конгруэнтность семи линейных треугольников.

**Теоремы:** Theorem A; Theorem F (the group layer).  
**Код:** `python/planetvortex/fano.py :: automorphism_group, find_isomorphism`.

## Записанный прогон

*Статус: **PASS** · сьют `planetvortex-ladder` · версия 2.0.0 · дата 2026-10-09*

| регистр | записано |
|---|---|
| `group_order_cyclic` | 168 |
| `group_order_binary` | 168 |
| `n_lines` | 7 |
| `n_flags` | 21 |
| `has_identity` | PASS |
| `closed_under_product` | PASS |
| `inverses_present` | PASS |
| `point_transitive` | PASS |
| `stabilizer_point` | 24 |
| `stabilizer_line` | 24 |
| `pair_axiom` | PASS |
| `isomorphism_found` | PASS |
| `isomorphism_maps_lines_to_lines` | PASS |
| `groups_conjugate_in_s7` | PASS |
| `congruence_max_abs_error` | 6.66134e-16 |
| `area_max_abs_error` | 1.11022e-16 |
| `angle_ladder_max_abs_error` | 5.55112e-16 |

**Параметры:** `{"tolerances": "integers exact; chords/angles/area <= 1e-12"}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite p --stage P --preset default
```
