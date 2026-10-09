---
title: "P6 — the seven Fano cells"
subtitle: "PLANETVORTEX — the stage monograph (P)"
---

## The claim

The seven three-vortex cells carry exactly equal Hamiltonians (Theorem B) and congruent shape cycles with spread 0.0 — the combinatorial congruence of PSL(2,7) as a dynamical one.

**Theorems:** Theorem B (docs/theorems).  
**Code:** `python/planetvortex/ladder.py :: check_p6_cells`.

## The recorded run

*Status: **PASS** · suite `planetvortex-ladder` · version 2.0.0 · date 2026-10-09*

| register | recorded |
|---|---|
| `per_cell` | [7 items] |
| `hamiltonian_spread` | 5.55112e-17 |
| `hamiltonian_exact_relative_error` | 1.79241e-16 |
| `T_shape_mean` | 9.3814 |
| `T_shape_relative_spread` | 0 |
| `worst_return_residual` | 3.8638e-07 |
| `worst_invariant_drift` | 9.14824e-14 |
| `max_shape_deviation` | 0.287618 |

**Parameters:** `{"t_max": 240.0, "dt": 0.004, "sample_every": 4, "gamma": 1.0, "big_r": 1.0, "integrator": "batched RK4 over the (7,3,2) cell array"}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite p --stage P --preset default
```
