---
title: "P6 — семь ячеек Фано"
subtitle: "PLANETVORTEX — the stage monograph (P)"
---

## Утверждение

Семь трёхвихревых ячеек несут в точности равные гамильтонианы (теорема B) и конгруэнтные циклы формы с разбросом 0,0 — комбинаторная конгруэнтность PSL(2,7) как динамическая.

**Теоремы:** Theorem B (docs/theorems).  
**Код:** `python/planetvortex/ladder.py :: check_p6_cells`.

## Записанный прогон

*Статус: **PASS** · сьют `planetvortex-ladder` · версия 2.0.0 · дата 2026-10-09*

| регистр | записано |
|---|---|
| `per_cell` | [7 items] |
| `hamiltonian_spread` | 5.55112e-17 |
| `hamiltonian_exact_relative_error` | 1.79241e-16 |
| `T_shape_mean` | 9.3814 |
| `T_shape_relative_spread` | 0 |
| `worst_return_residual` | 3.8638e-07 |
| `worst_invariant_drift` | 9.14824e-14 |
| `max_shape_deviation` | 0.287618 |

**Параметры:** `{"t_max": 240.0, "dt": 0.004, "sample_every": 4, "gamma": 1.0, "big_r": 1.0, "integrator": "batched RK4 over the (7,3,2) cell array"}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite p --stage P --preset default
```
