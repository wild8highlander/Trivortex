---
title: "V1 — пространственные регистры"
subtitle: "PLANETVORTEX — the stage monograph (V)"
---

## Утверждение

SO(3)-алгебра наклонов 11-телного реестра, точные дуговые регистры λ = R̄·i (лемма G), матрица взаимных наклонений с экстремумом Эриды и полный 3D ньютоновский прогон по реальному небу J2000.

**Теоремы:** Lemma G (docs/theorems).  
**Код:** `python/planetvortex/spatial.py :: check_v1_inclined`.

## Записанный прогон

*Статус: **PASS** · сьют `planetvortex-vregister` · версия 2.0.0 · дата 2026-10-09*

| регистр | записано |
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

**Параметры:** `{"years": 12.0, "dt": 0.0002, "n_steps": 60000, "sample_every": 8, "bodies": 9, "dimension": 3}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite v --stage V --preset default
```
