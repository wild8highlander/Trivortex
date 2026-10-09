---
title: "X3 — the (2,3,7) triangle generation"
subtitle: "PLANETVORTEX — the stage monograph (X)"
---

## The claim

EVERY (2,3,7) pair generates the whole group; the Klein relations; the Hurwitz arithmetic 84(g−1) = 168 = 42(2g−2); the smoothness of the Klein quartic x³y + y³z + z³x (the 28(xyz)³ = 0 contradiction), genus 3.

**Theorems:** Theorem F (the generation layer).  
**Code:** `python/planetvortex/hardcore.py :: check_x3_triangle`.

## The recorded run

*Status: **PASS** · suite `planetvortex-hardcore` · version 2.0.0 · date 2026-10-09*

| register | recorded |
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

**Parameters:** `{"group": "PSL(2,7) matrix model", "genus": 3}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite x --stage X --preset default
```
