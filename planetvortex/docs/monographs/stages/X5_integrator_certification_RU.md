---
title: "X5 — сертификация интегратора"
subtitle: "PLANETVORTEX — the stage monograph (X)"
---

## Утверждение

Измеренные порядки 2 (leapfrog) и 4 (Yoshida); обратимость по времени до округления; ограниченная симплектическая энергия без секулярного тренда против RK4-контроля; вектор Лапласа–Рунге–Ленца и точное уравнение орбиты.

**Теоремы:** The numerical discipline of the bench.  
**Код:** `python/planetvortex/hardcore.py :: check_x5_integrator`.

## Записанный прогон

*Статус: **PASS** · сьют `planetvortex-hardcore` · версия 2.0.0 · дата 2026-10-09*

| регистр | записано |
|---|---|
| `convergence` | {"leapfrog_grid": [300, 600, 1200, 2400], "leapfrog_errors": [0.02565691601491552, 0.006410769413173237, 0.0016024732687 |
| `reversibility` | {"leapfrog": 8.742120762792925e-13, "yoshida4": 7.478944519826449e-12} |
| `energy_envelopes` | {"leapfrog": {"max_relative": 0.002038154639526777, "secular_trend_ratio": 0.002584034778770475}, "yoshida4": {"max_rela |
| `two_body_invariants` | {"e": 0.4, "revolutions": 12, "steps_per_period": 8000, "lrl_drift": 1.0983609059866522e-10, "vis_viva_relative": 2.2285 |

**Параметры:** `{"order_orbit": {"a": 1.0, "e": 0.4, "t_final_periods": 5.37}, "bounded_window_periods": 80, "bounded_steps_per_period": 150}`

```bash
cd planetvortex
PYTHONPATH=python python3 python/planetvortex/runner.py --suite x --stage X --preset default
```
