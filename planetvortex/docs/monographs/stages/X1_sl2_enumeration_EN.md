---
title: "X1 — PSL(2,7) from nothing"
subtitle: "PLANETVORTEX — the stage monograph (X)"
---

## The claim

All 2401 matrices over F₇ enumerated: |GL| = 2016, |SL| = 336, |PSL| = 168; the class equation 1 + 21 + 42 + 56 + 24 + 24; simplicity over all 32 unions of classes.

**Theorems:** Theorem F (the group layer).  
**Code:** `python/planetvortex/hardcore.py :: check_x1_enumeration`.

## The recorded run

*Status: **PASS** · suite `planetvortex-hardcore` · version 2.0.0 · date 2026-10-09*

| register | recorded |
|---|---|
| `matrices_enumerated` | 2401 |
| `group_order_gl` | 2016 |
| `group_order_sl` | 336 |
| `group_order_psl` | 168 |
| `gl_closed_form` | 2016 |
| `sl_closed_form` | 336 |
| `quotient_exactly_2_to_1` | PASS |
| `centre_sl` | [[1, 0, 0, 1], [6, 0, 0, 6]] |
| `centre_psl_trivial` | PASS |
| `element_order_census` | {"1": 1, "2": 21, "3": 56, "4": 42, "7": 48} |
| `conjugacy_class_sizes` | [6 items] |
| `class_equation_sum` | 168 |
| `normal_subgroup_union_found` | FAIL |
| `simple` | PASS |

**Parameters:** `{"field": "F_7", "model": "SL(2,7)/{+-I} canonical reps"}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite x --stage X --preset default
```
