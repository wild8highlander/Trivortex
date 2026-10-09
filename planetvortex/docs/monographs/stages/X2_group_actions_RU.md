---
title: "X2 — два естественных действия"
subtitle: "PLANETVORTEX — the stage monograph (X)"
---

## Утверждение

Действие на 7 точках (подгруппы S₄) — верное, транзитивное, сопряжённое исследовательской модели внутри S₇; действие на 8 точках (силовские 7) — 2-транзитивное; силовский контроль n₂ = 21, n₃ = 28, n₇ = 8.

**Теоремы:** Theorem F; Lemma F.  
**Код:** `python/planetvortex/hardcore.py :: check_x2_actions`.

## Записанный прогон

*Статус: **PASS** · сьют `planetvortex-hardcore` · версия 2.0.0 · дата 2026-10-09*

| регистр | записано |
|---|---|
| `involutions` | 21 |
| `elements_order3` | 56 |
| `elements_order7` | 48 |
| `sylow_7_count` | 8 |
| `sylow_3_count` | 28 |
| `sylow_2_count` | 21 |
| `normalizer_sylow2_order` | 8 |
| `normalizer_sylow7_order` | 21 |
| `normalizer_sylow7_order_census` | {"1": 1, "3": 14, "7": 6} |
| `s4_subgroup_count` | 7 |
| `s4_subgroup_count_all_classes` | 14 |
| `s4_stabilizer_order_census` | {"1": 1, "2": 9, "3": 8, "4": 6} |
| `action7_image_order` | 168 |
| `action7_kernel` | 1 |
| `action7_transitive` | PASS |
| `bridge_to_research_model` | PASS |
| `bridge_sigma` | [7 items] |
| `action8_image_order` | 168 |
| `action8_2_transitive` | PASS |
| `action8_ordered_pair_orbit_size` | 56 |
| `action8_triple_orbit_size` | 56 |

**Параметры:** `{"model": "conjugation actions of SL(2,7)/{+-I}"}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite x --stage X --preset default
```
