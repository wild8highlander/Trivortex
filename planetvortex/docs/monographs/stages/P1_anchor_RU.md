---
title: "P1 — якорь: точные литералы фигуры"
subtitle: "PLANETVORTEX — the stage monograph (P)"
---

## Утверждение

Точные размерности плоской семиугольной фигуры (теорема A) на рабочей точности плюс якорь Кеплера–Земли в СИ.

**Теоремы:** Theorem A (docs/theorems).  
**Код:** `python/planetvortex/fano.py :: exact_literals`.

## Записанный прогон

*Статус: **PASS** · сьют `planetvortex-ladder` · версия 2.0.0 · дата 2026-10-09*

| регистр | записано |
|---|---|
| `exact_literals` | {"s1": "0.867767478235116240951536665697", "s2": "1.56366296493605961741688905335", "s3": "1.949855824363647214036263365 |
| `chord_relative_errors` | {"s1": 0.0, "s2": 0.0, "s3": 0.0} |
| `angle_relative_errors` | [4.94753e-16, 0, 1.23688e-16] |
| `area_relative_error` | 1.6785e-16 |
| `omega_relative_error` | 0 |
| `kepler_earth_si_value` | 2.9747e-19 |
| `kepler_earth_si_constant` | 2.97473e-19 |
| `kepler_earth_relative_error` | 9.74552e-06 |

**Параметры:** `{"dps": 30, "big_r": 1.0, "au_m": 149597870700.0, "gm_sun": 1.32712440018e+20}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite p --stage P --preset default
```
