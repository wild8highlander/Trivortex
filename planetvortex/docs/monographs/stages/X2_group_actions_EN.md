---
title: "X2 — the two natural actions"
subtitle: "PLANETVORTEX — the stage monograph (X)"
---

## The claim

The action on 7 points (the S₄ subgroups) — faithful, transitive, conjugate to the research model inside S₇; the action on 8 points (the Sylow-7s) — 2-transitive; the Sylow census n₂ = 21, n₃ = 28, n₇ = 8.

**Theorems:** Theorem F; Lemma F.  
**Code:** `python/planetvortex/hardcore.py :: check_x2_actions`.

## The recorded run

*Status: **PASS** · suite `planetvortex-hardcore` · version 2.0.0 · date 2026-10-09*

| register | recorded |
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

**Parameters:** `{"model": "conjugation actions of SL(2,7)/{+-I}"}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite x --stage X --preset default
```
