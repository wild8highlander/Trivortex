---
title: "X6 — the GR bridge"
subtitle: "PLANETVORTEX — the stage monograph (X)"
---

## The claim

The 1PN perihelion precession measured against the closed form 6πGM/(a(1−e²)c²); the Newtonian control at integrator zero; Mercury 42.982″/century against the textbook 42.98″.

**Theorems:** The GR honesty note (README §14).  
**Code:** `python/planetvortex/hardcore.py :: check_x6_pn_perihelion`.

## The recorded run

*Status: **PASS** · suite `planetvortex-hardcore` · version 2.0.0 · date 2026-10-09*

| register | recorded |
|---|---|
| `per_planet` | [{"planet": "Mercury", "a_au": 0.38709927, "e": 0.20563593, "formula_rad_per_orbit": 5.018850845434587e-07, "measured_rad, {"planet": "Venus", "a_au": 0.72333566, "e": 0.00677672, "formula_rad_per_orbit": 2.572429467502201e-07, "measured_rad_p, {"planet": "Earth", "a_au": 1.00000261, "e": 0.01671123, "formula_rad_per_orbit": 1.861160449588561e-07, "measured_rad_p] |
| `worst_measured_over_formula_deviation` | 9.3466e-05 |
| `worst_newtonian_advance_rad_per_orbit` | 2.88382e-11 |
| `mercury_arcsec_per_century` | 42.9823 |
| `textbook_mercury_arcsec_per_century` | 42.98 |
| `century_anchor_relative_error` | 5.31611e-05 |
| `formula_ladder_all_planets` | [8 items] |

**Parameters:** `{"n_orbits": 30, "steps_per_orbit": 2400, "planets_numeric": ["Mercury", "Venus", "Earth"], "pn_gauge": "harmonic, test particle", "c_au_per_year": 63241.07708426628}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite x --stage X --preset default
```
