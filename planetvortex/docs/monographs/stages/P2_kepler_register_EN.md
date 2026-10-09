---
title: "P2 — the Kepler register"
subtitle: "PLANETVORTEX — the stage monograph (P)"
---

## The claim

The mass-corrected Kepler III is the same constant for all eight planets (Lemma D): T²/a³(1 + m/M) to 10⁻¹³; the uncorrected register and the fact-sheet provenance recorded as honest diagnostics.

**Theorems:** Lemma D (docs/theorems).  
**Code:** `python/planetvortex/classical.py :: kepler3_*`.

## The recorded run

*Status: **PASS** · suite `planetvortex-ladder` · version 2.0.0 · date 2026-10-09*

| register | recorded |
|---|---|
| `per_planet` | [8 items] |
| `worst_deviation_corrected` | 6.16367e-13 |
| `worst_deviation_uncorrected` | 0.000476956 |
| `correction_improvement_factor` | 7.738173e+08 |
| `factsheet_worst_deviation` | 0.00048399 |
| `factsheet_worst_planet` | Neptune |

**Parameters:** `{"n_revolutions": 2, "steps_per_revolution": 3600, "integrator": "RK4, perihelion minima, parabolic interpolation"}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite p --stage P --preset default
```
