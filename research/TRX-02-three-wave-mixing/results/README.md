# TRX-02 — the committed protocol

The deterministic output of the study script: the JSON protocol
[`trx02_results.json`](trx02_results.json) — the single numeric oracle the
study README, the monographs and the pytest guard quote. Nothing in
this folder is hand-written.

## The protocol schema

```jsonc
{
  "study": "trx-02",       // the study id
  "title": "…",                       // the study title
  "status": "PASS",               // the overall verdict
  "smoke": false,                     // whether this was a --smoke run
  "runtime_s": …,                     // the wall-time stamp (not a register)
  "checks": [ … ],                    // the registered checks, one entry each
  "series": { … },                   // the plotted series (the figure source)
  "meta": { … }                      // the full parameter snapshot
}
```

## The registered checks (7 / 7 PASS)

| check | registered band | recorded | unit | status |
|-------|-----------------|----------|------|:------:|
| `ManleyRowe_I13_drift` | `0.0` ± `1e-10` | `5.10702591327572e-15` | dimless | PASS |
| `ManleyRowe_I23_drift` | `0.0` ± `1e-10` | `1.7763568394002505e-15` | dimless | PASS |
| `ManleyRowe_I12diff_drift` | `0.0` ± `1e-10` | `3.774758283725532e-15` | dimless | PASS |
| `Pump_period_repeatability` | `0.0` ± `1e-06` | `4.469729741884976e-08` | dimless | PASS |
| `Pump_revival_error` | `0.0` ± `1e-08` | `2.4424906541753444e-15` | dimless | PASS |
| `Pump_full_depletion_occurs` | `1.0` ± `1e-12` | `1.0` | bool | PASS |
| `SHG_tanh2_conversion_error` | `0.0` ± `1e-08` | `2.220446049250313e-16` | dimless | PASS |

Each check was registered — target and tolerance committed **before**
the recorded run. A check compares its recorded value against the band;
the overall `status` is PASS only when every check passes.


The companion [`trx02_plot.svg`](trx02_plot.svg) is the study's
vector plot snapshot — the same series the PNG gallery in
[`../figures/`](../figures/) renders at 300 dpi.

## Determinism and reproduction

```bash
python3 code/trx02_three_wave_mixing.py    # rewrites the protocol with identical numbers
```

Fixed seeds, fixed grids, no wall-clock dependence inside the registers.
A `git diff` on this folder after a re-run must show only the
`runtime_s` stamp changing; any drift in a check value is a
reproducibility bug — open an issue with the protocol attached (the
[issue template](../../../.github/ISSUE_TEMPLATE/) has a field for
exactly that).
