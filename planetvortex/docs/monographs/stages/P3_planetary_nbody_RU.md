---
title: "P3 — плоская задача N тел"
subtitle: "PLANETVORTEX — the stage monograph (P)"
---

## Утверждение

Полное ньютоновское интегрирование Солнце + 8 планет: сохранение энергии и момента, оскулирующие (a, e) внутри секулярной полосы, Кеплер III интегрируемого движения, иерархия возмущений.

**Теоремы:** Lemma D; honesty notes (README §14).  
**Код:** `python/planetvortex/nbody.py`.

## Записанный прогон

*Статус: **PASS** · сьют `planetvortex-ladder` · версия 2.0.0 · дата 2026-10-09*

| регистр | записано |
|---|---|
| `energy_drift_relative` | 2.0737e-13 |
| `angular_momentum_drift_relative` | 0 |
| `worst_a_deviation_relative` | 0.00637231 |
| `worst_e_deviation` | 0.00365329 |
| `worst_kepler3_dynamic_deviation` | 2.51381e-05 |
| `max_perturbation_ratio` | 0.00218223 |
| `per_planet` | [8 items] |

**Параметры:** `{"years": 12.0, "dt": 0.0002, "n_steps": 60000, "sample_every": 8, "bodies": 9}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite p --stage P --preset default
```
