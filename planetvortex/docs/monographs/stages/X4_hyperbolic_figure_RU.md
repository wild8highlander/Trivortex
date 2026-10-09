---
title: "X4 — гиперболическая фигура {7,3}"
subtitle: "PLANETVORTEX — the stage monograph (X)"
---

## Утверждение

Точные замкнутые формы полуребра, вписанного и описанного радиусов при 50 dps; гиперболический Пифагор; лестница площадей π/42 → π/3 → 8π; комбинаторное замыкание 3V = 7F = 2E = 168; свидетель в диске Пуанкаре, решённый бисекцией.

**Теоремы:** Theorem G (the per-register layer).  
**Код:** `python/planetvortex/hardcore.py :: check_x4_hyperbolic`.

## Записанный прогон

*Статус: **PASS** · сьют `planetvortex-hardcore` · версия 2.0.0 · дата 2026-10-09*

| регистр | записано |
|---|---|
| `literals` | {"dps": "50", "cosh_half_edge": "1.0403492368298681173161942726052531844678191219582", "cosh_inradius": "1.1523824354812 |
| `identities_at_dps` | PASS |
| `combinatorial_closure` | PASS |
| `combinatorics` | {"V": 56, "E": 84, "F": 24, "genus": 3} |
| `disk_witness` | {"t_vertex": 0.30074261874637864, "circumradius_numeric": 0.6206717375563858, "edge_numeric": 0.5662563067353149, "angle |
| `witness_circumradius_error` | 0 |
| `witness_edge_error` | 1.11022e-16 |

**Параметры:** `{"dps": 50, "tiling": "{7,3}", "surface": "Klein quartic"}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite x --stage X --preset default
```
