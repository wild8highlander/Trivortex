---
title: "P3 — the planar N-body"
subtitle: "PLANETVORTEX — the stage monograph (P)"
---

## The claim

The full Newtonian Sun + 8-planets integration: energy and angular-momentum conservation, the osculating (a, e) inside the secular band, Kepler III of the integrated motion, the perturbation hierarchy.

**Theorems:** Lemma D; honesty notes (README §14).  
**Code:** `python/planetvortex/nbody.py`.

## The recorded run

*Status: **PASS** · suite `planetvortex-ladder` · version 2.0.0 · date 2026-10-09*

| register | recorded |
|---|---|
| `energy_drift_relative` | 2.0737e-13 |
| `angular_momentum_drift_relative` | 0 |
| `worst_a_deviation_relative` | 0.00637231 |
| `worst_e_deviation` | 0.00365329 |
| `worst_kepler3_dynamic_deviation` | 2.51381e-05 |
| `max_perturbation_ratio` | 0.00218223 |
| `per_planet` | [8 items] |

**Parameters:** `{"years": 12.0, "dt": 0.0002, "n_steps": 60000, "sample_every": 8, "bodies": 9}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite p --stage P --preset default
```
