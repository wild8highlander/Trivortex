---
title: "V2 — замкнутая гравифигура"
subtitle: "PLANETVORTEX — the stage monograph (V)"
---

## Утверждение

Полное 24-семиугольное разбиение {7,3}₈ квартики Клейна как косет-геометрия сертифицированного PSL(2,7) (теорема F); антиподальное паросочетание (лемма F); 12-телный гравиметрический регистр с ТОЧНЫМ замыканием бюджета Σα = 8π (теорема G); флаговый сертификат PGL(2,7) и патч chambers в диске.

**Теоремы:** Theorem F, Lemma F, Theorem G, Proposition H.  
**Код:** `python/planetvortex/klein.py :: check_v2_klein_tiling`.

## Записанный прогон

*Статус: **PASS** · сьют `planetvortex-vregister` · версия 2.0.0 · дата 2026-10-09*

| регистр | записано |
|---|---|
| `combinatorics` | {"V": 56, "E": 84, "F": 24, "euler": -4, "vertex_degrees": [3], "face_lengths": [7], "edge_valences": [2], "n_antipodal_ |
| `connected` | PASS |
| `orientable` | PASS |
| `witness_triple` | {"a_index": 0, "b_index": 1, "c_index": 63} |
| `register_algebra` | {"sigma": 0.015524718017380526, "s_sum": -3.907985046680551e-14, "alpha_sum": 25.132741228718352, "alpha_sum_residual":  |
| `exact_registers` | {"dps": 50, "bodies": [{"body": "Sun", "s": "12.319754029629188495651218822458094094700630427519", "alpha": "1.903134395 |
| `disk_witnesses` | {"heaviest": {"body": "Sun", "alpha": 1.9031343950397146, "circumradius_closed": 0.9443455504836687, "circumradius_witne |
| `chamber_patch` | {"chambers": 336, "n_heptagons": 24, "interior_sides": 9, "n_boundary_pairs": 75, "n_map_edges": 84, "heptagon_sides": 1 |
| `body_assignment` | [12 items] |

**Параметры:** `{"dps": 50, "ceiling_margin": 0.05, "tiling": "{7,3}_8"}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite v --stage V --preset default
```
