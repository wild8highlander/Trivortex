---
title: "X3 — треугольное порождение (2,3,7)"
subtitle: "PLANETVORTEX — the stage monograph (X)"
---

## Утверждение

КАЖДАЯ пара (2,3,7) порождает всю группу; соотношения Клейна; арифметика Хурвица 84(g−1) = 168 = 42(2g−2); гладкость квартики Клейна x³y + y³z + z³x (противоречие 28(xyz)³ = 0), род 3.

**Теоремы:** Theorem F (the generation layer).  
**Код:** `python/planetvortex/hardcore.py :: check_x3_triangle`.

## Записанный прогон

*Статус: **PASS** · сьют `planetvortex-hardcore` · версия 2.0.0 · дата 2026-10-09*

| регистр | записано |
|---|---|
| `n_involutions` | 21 |
| `n_order3` | 56 |
| `product_order_distribution` | {"2": 168, "3": 336, "4": 336, "7": 336} |
| `n_pairs_237` | 336 |
| `n_non_generating` | 0 |
| `witness_pair_orders` | [2, 3, 7] |
| `klein_relations` | {"a_squared_identity": true, "b_cubed_identity": true, "ab_seventh_identity": true, "commutator_fourth_identity": true} |
| `hurwitz_bound_84_g_minus_1` | 168 |
| `riemann_hurwitz_42_2g_minus_2` | 168 |
| `class_equation_cross_check` | 168 |
| `orbifold_chi_numerator` | -1 |
| `orbifold_chi_denominator` | 42 |
| `klein_quartic_smoothness` | {"lhs_product": {"(3, 3, 3)": 27}, "rhs_product": {"(3, 3, 3)": 1}, "identity_27_xyz3": true, "contradiction_28": true,  |

**Параметры:** `{"group": "PSL(2,7) matrix model", "genus": 3}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite x --stage X --preset default
```
