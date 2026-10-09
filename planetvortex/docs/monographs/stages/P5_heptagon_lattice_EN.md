---
title: "P5 — the heptagon vortex lattice"
subtitle: "PLANETVORTEX — the stage monograph (P)"
---

## The claim

The rigid rotation ω₇ = 3Γ/(2πR²) measured to 10⁻¹², the invariants along the flow, the Havelock stability of N = 7 (Theorem C) — the last stable level.

**Theorems:** Theorem C (docs/theorems).  
**Code:** `python/planetvortex/model.py :: corotating_spectrum`.

## The recorded run

*Status: **PASS** · suite `planetvortex-ladder` · version 2.0.0 · date 2026-10-09*

| register | recorded |
|---|---|
| `omega_analytic` | 0.477465 |
| `omega_measured` | 0.477465 |
| `omega_relative_error` | 1.34655e-12 |
| `invariant_drifts` | {"H": 1.249565716701129e-14, "P": 5.329070518200751e-15, "Q": 2.4424906541753444e-15, "I": 8.120488408686859e-15} |
| `hamiltonian_exact` | -1.08395 |
| `hamiltonian_relative_error` | 0 |
| `max_Re_lambda` | 7.00154e-09 |
| `havelock_stable` | PASS |

**Parameters:** `{"gamma": 1.0, "big_r": 1.0, "rotations": 2.0, "steps_per_rotation": 2400}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite p --stage P --preset default
```
