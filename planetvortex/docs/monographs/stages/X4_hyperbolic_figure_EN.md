---
title: "X4 — the hyperbolic {7,3} figure"
subtitle: "PLANETVORTEX — the stage monograph (X)"
---

## The claim

The exact half-edge, inradius and circumradius closed forms at 50 dps; the hyperbolic Pythagoras; the area ladder π/42 → π/3 → 8π; the combinatorial closure 3V = 7F = 2E = 168; the Poincaré-disk witness solved by bisection.

**Theorems:** Theorem G (the per-register layer).  
**Code:** `python/planetvortex/hardcore.py :: check_x4_hyperbolic`.

## The recorded run

*Status: **PASS** · suite `planetvortex-hardcore` · version 2.0.0 · date 2026-10-09*

| register | recorded |
|---|---|
| `literals` | {"dps": "50", "cosh_half_edge": "1.0403492368298681173161942726052531844678191219582", "cosh_inradius": "1.1523824354812 |
| `identities_at_dps` | PASS |
| `combinatorial_closure` | PASS |
| `combinatorics` | {"V": 56, "E": 84, "F": 24, "genus": 3} |
| `disk_witness` | {"t_vertex": 0.30074261874637864, "circumradius_numeric": 0.6206717375563858, "edge_numeric": 0.5662563067353149, "angle |
| `witness_circumradius_error` | 0 |
| `witness_edge_error` | 1.11022e-16 |

**Parameters:** `{"dps": 50, "tiling": "{7,3}", "surface": "Klein quartic"}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite x --stage X --preset default
```
