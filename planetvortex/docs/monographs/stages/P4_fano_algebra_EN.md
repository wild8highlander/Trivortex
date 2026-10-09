---
title: "P4 — the PSL(2,7) algebra"
subtitle: "PLANETVORTEX — the stage monograph (P)"
---

## The claim

168 automorphisms, the two Fano models (cyclic and binary) with an explicit isomorphism, the conjugacy of the two group copies inside S₇, the congruence of the seven line-triangles.

**Theorems:** Theorem A; Theorem F (the group layer).  
**Code:** `python/planetvortex/fano.py :: automorphism_group, find_isomorphism`.

## The recorded run

*Status: **PASS** · suite `planetvortex-ladder` · version 2.0.0 · date 2026-10-09*

| register | recorded |
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

**Parameters:** `{"tolerances": "integers exact; chords/angles/area <= 1e-12"}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite p --stage P --preset default
```
