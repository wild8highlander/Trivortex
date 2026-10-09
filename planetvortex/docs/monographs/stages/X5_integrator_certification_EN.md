---
title: "X5 — the integrator certification"
subtitle: "PLANETVORTEX — the stage monograph (X)"
---

## The claim

The measured orders 2 (leapfrog) and 4 (Yoshida); time-reversibility to roundoff; the bounded symplectic energy with no secular trend against the RK4 control; the Laplace–Runge–Lenz vector and the exact orbit equation.

**Theorems:** The numerical discipline of the bench.  
**Code:** `python/planetvortex/hardcore.py :: check_x5_integrator`.

## The recorded run

*Status: **PASS** · suite `planetvortex-hardcore` · version 2.0.0 · date 2026-10-09*

| register | recorded |
|---|---|
| `convergence` | {"leapfrog_grid": [300, 600, 1200, 2400], "leapfrog_errors": [0.02565691601491552, 0.006410769413173237, 0.0016024732687 |
| `reversibility` | {"leapfrog": 8.742120762792925e-13, "yoshida4": 7.478944519826449e-12} |
| `energy_envelopes` | {"leapfrog": {"max_relative": 0.002038154639526777, "secular_trend_ratio": 0.002584034778770475}, "yoshida4": {"max_rela |
| `two_body_invariants` | {"e": 0.4, "revolutions": 12, "steps_per_period": 8000, "lrl_drift": 1.0983609059866522e-10, "vis_viva_relative": 2.2285 |

**Parameters:** `{"order_orbit": {"a": 1.0, "e": 0.4, "t_final_periods": 5.37}, "bounded_window_periods": 80, "bounded_steps_per_period": 150}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite x --stage X --preset default
```
