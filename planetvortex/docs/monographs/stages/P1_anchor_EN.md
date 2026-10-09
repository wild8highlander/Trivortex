---
title: "P1 — the anchor: the exact figure literals"
subtitle: "PLANETVORTEX — the stage monograph (P)"
---

## The claim

The exact dimensions of the flat heptagonal figure (Theorem A) pinned at working precision, plus the Kepler–Earth SI anchor.

**Theorems:** Theorem A (docs/theorems).  
**Code:** `python/planetvortex/fano.py :: exact_literals`.

## The recorded run

*Status: **PASS** · suite `planetvortex-ladder` · version 2.0.0 · date 2026-10-09*

| register | recorded |
|---|---|
| `exact_literals` | {"s1": "0.867767478235116240951536665697", "s2": "1.56366296493605961741688905335", "s3": "1.949855824363647214036263365 |
| `chord_relative_errors` | {"s1": 0.0, "s2": 0.0, "s3": 0.0} |
| `angle_relative_errors` | [4.94753e-16, 0, 1.23688e-16] |
| `area_relative_error` | 1.6785e-16 |
| `omega_relative_error` | 0 |
| `kepler_earth_si_value` | 2.9747e-19 |
| `kepler_earth_si_constant` | 2.97473e-19 |
| `kepler_earth_relative_error` | 9.74552e-06 |

**Parameters:** `{"dps": 30, "big_r": 1.0, "au_m": 149597870700.0, "gm_sun": 1.32712440018e+20}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite p --stage P --preset default
```
