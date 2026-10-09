---
title: "V1 — the spatial registers"
subtitle: "PLANETVORTEX — the stage monograph (V)"
---

## The claim

The SO(3) tilt algebra of the 11-body inclination register, the exact arc registers λ = R̄·i (Lemma G), the mutual-inclination matrix with the Eris extreme, and the full 3D Newtonian run from the real J2000 sky.

**Theorems:** Lemma G (docs/theorems).  
**Code:** `python/planetvortex/spatial.py :: check_v1_inclined`.

## The recorded run

*Status: **PASS** · suite `planetvortex-vregister` · version 2.0.0 · date 2026-10-09*

| register | recorded |
|---|---|
| `tilt_registers` | {"worst_orthogonality": 2.220446049250313e-16, "worst_determinant_gap": 3.3306690738754696e-16, "worst_normal_recovery": |
| `mutual_inclinations` | {"n_pairs": 55, "max_mutual_deg": 44.247748281520686, "max_pair": ["Neptune", "Eris"]} |
| `energy_drift_relative` | 2.14063e-13 |
| `angular_momentum_drift_relative` | 4.72475e-15 |
| `angular_momentum_vector_drift` | 4.54303e-15 |
| `worst_a_deviation_relative` | 0.00446895 |
| `worst_e_deviation` | 0.00466933 |
| `worst_inclination_drift_rad` | 2.41372e-05 |
| `worst_kepler3_dynamic_deviation` | 0.000102844 |
| `z_ladder_au` | {"Mercury": 0.05116648789990574, "Venus": 0.043066166214913805, "Earth": 3.07875660834799e-05, "Mars": 0.053578382725087 |
| `per_planet` | [8 items] |

**Parameters:** `{"years": 12.0, "dt": 0.0002, "n_steps": 60000, "sample_every": 8, "bodies": 9, "dimension": 3}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite v --stage V --preset default
```
