---
title: "P5 — вихревая решётка семиугольника"
subtitle: "PLANETVORTEX — the stage monograph (P)"
---

## Утверждение

Жёсткое вращение ω₇ = 3Γ/(2πR²) измерено до 10⁻¹², инварианты вдоль потока, хавелоковская устойчивость N = 7 (теорема C) — последний устойчивый уровень.

**Теоремы:** Theorem C (docs/theorems).  
**Код:** `python/planetvortex/model.py :: corotating_spectrum`.

## Записанный прогон

*Статус: **PASS** · сьют `planetvortex-ladder` · версия 2.0.0 · дата 2026-10-09*

| регистр | записано |
|---|---|
| `omega_analytic` | 0.477465 |
| `omega_measured` | 0.477465 |
| `omega_relative_error` | 1.34655e-12 |
| `invariant_drifts` | {"H": 1.249565716701129e-14, "P": 5.329070518200751e-15, "Q": 2.4424906541753444e-15, "I": 8.120488408686859e-15} |
| `hamiltonian_exact` | -1.08395 |
| `hamiltonian_relative_error` | 0 |
| `max_Re_lambda` | 7.00154e-09 |
| `havelock_stable` | PASS |

**Параметры:** `{"gamma": 1.0, "big_r": 1.0, "rotations": 2.0, "steps_per_rotation": 2400}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite p --stage P --preset default
```
