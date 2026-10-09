---
title: "P7 — гравитационный мост"
subtitle: "PLANETVORTEX — the stage monograph (P)"
---

## Утверждение

Лестница Шварцшильда r_s = 2GM/c², соседние поля Хилла (сертификат непересечения) и дефицит лестницы масс леммы E, записанный честно: фигура слепа к массе, Солнечная система — нет.

**Теоремы:** Lemma E (docs/theorems).  
**Код:** `python/planetvortex/classical.py :: schwarzschild_radius_m, hill_radius_au`.

## Записанный прогон

*Статус: **PASS** · сьют `planetvortex-ladder` · версия 2.0.0 · дата 2026-10-09*

| регистр | записано |
|---|---|
| `schwarzschild_ladder` | [9 items] |
| `schwarzschild_worst_relative_error` | 1.0065e-16 |
| `hill_margins` | [7 items] |
| `hill_min_margin` | 5.08485 |
| `figure_dimensions_au` | {"side_s1": 0.8677674782351162, "short_diagonal_s2": 1.5636629649360596, "long_diagonal_s3": 1.9498558243636472, "cell_a |
| `diagnostics` | {"mass_ladder_line_sums": {"Mercury+Venus+Jupiter": 1.155866, "Venus+Mars+Saturn": 0.92081, "Mars+Jupiter+Uranus": 2.695 |

**Параметры:** `{"dps": 30, "tolerances": {"hill_margin_min": 3.0}}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite p --stage P --preset default
```
