---
title: "P2 — регистр Кеплера"
subtitle: "PLANETVORTEX — the stage monograph (P)"
---

## Утверждение

Массово-исправленный третий закон Кеплера одинаков для всех восьми планет (лемма D): T²/a³(1 + m/M) до 10⁻¹³; неисправленный регистр и происхождение из факт-листов записаны честными диагностиками.

**Теоремы:** Lemma D (docs/theorems).  
**Код:** `python/planetvortex/classical.py :: kepler3_*`.

## Записанный прогон

*Статус: **PASS** · сьют `planetvortex-ladder` · версия 2.0.0 · дата 2026-10-09*

| регистр | записано |
|---|---|
| `per_planet` | [8 items] |
| `worst_deviation_corrected` | 6.16367e-13 |
| `worst_deviation_uncorrected` | 0.000476956 |
| `correction_improvement_factor` | 7.738173e+08 |
| `factsheet_worst_deviation` | 0.00048399 |
| `factsheet_worst_planet` | Neptune |

**Параметры:** `{"n_revolutions": 2, "steps_per_revolution": 3600, "integrator": "RK4, perihelion minima, parabolic interpolation"}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite p --stage P --preset default
```
