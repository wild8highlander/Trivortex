---
title: "V2 — the closed gravifigure"
subtitle: "PLANETVORTEX — the stage monograph (V)"
---

## The claim

The full 24-heptagon tessellation {7,3}₈ of the Klein quartic as the coset geometry of the certified PSL(2,7) (Theorem F); the antipodal pairing (Lemma F); the 12-body gravimetric register with the EXACT budget closure Σα = 8π (Theorem G); the PGL(2,7) flag certificate and the chamber-grown disk patch.

**Theorems:** Theorem F, Lemma F, Theorem G, Proposition H.  
**Code:** `python/planetvortex/klein.py :: check_v2_klein_tiling`.

## The recorded run

*Status: **PASS** · suite `planetvortex-vregister` · version 2.0.0 · date 2026-10-09*

| register | recorded |
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

**Parameters:** `{"dps": 50, "ceiling_margin": 0.05, "tiling": "{7,3}_8"}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite v --stage V --preset default
```
