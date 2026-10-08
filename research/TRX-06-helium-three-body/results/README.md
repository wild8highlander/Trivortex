# TRX-06 — the committed protocol

The deterministic output of the study script: the JSON protocol
[`trx06_results.json`](trx06_results.json) — the single numeric oracle the
study README, the monographs and the pytest guard quote. Nothing in
this folder is hand-written.

## The protocol schema

```jsonc
{
  "study": "trx-06",       // the study id
  "title": "…",                       // the study title
  "status": "PASS",               // the overall verdict
  "smoke": false,                     // whether this was a --smoke run
  "runtime_s": …,                     // the wall-time stamp (not a register)
  "checks": [ … ],                    // the registered checks, one entry each
  "series": { … },                   // the plotted series (the figure source)
  "meta": { … }                      // the full parameter snapshot
}
```

## The registered checks (5 / 5 PASS)

| check | registered band | recorded | unit | status |
|-------|-----------------|----------|------|:------:|
| `max_relative_energy_drift_valid` | `0.0` ± `0.0004` | `2.883893521896108e-06` | rel | PASS |
| `outcome_classes_sum_to_N` | `120` ± `1e-12` | `120` | count | PASS |
| `autoionization_channel_active` | `1.0` ± `1e-12` | `1.0` | bool | PASS |
| `escaping_electron_energy_overshoot` | `1.0` ± `1e-12` | `1.0` | bool | PASS |
| `fit_reproducible` | `1.0` ± `1e-12` | `1.0` | bool | PASS |

Each check was registered — target and tolerance committed **before**
the recorded run. A check compares its recorded value against the band;
the overall `status` is PASS only when every check passes.


The companion [`trx06_plot.svg`](trx06_plot.svg) is the study's
vector plot snapshot — the same series the PNG gallery in
[`../figures/`](../figures/) renders at 300 dpi.

## Determinism and reproduction

```bash
python3 code/trx06_helium_three_body.py    # rewrites the protocol with identical numbers
```

Fixed seeds, fixed grids, no wall-clock dependence inside the registers.
A `git diff` on this folder after a re-run must show only the
`runtime_s` stamp changing; any drift in a check value is a
reproducibility bug — open an issue with the protocol attached (the
[issue template](../../../.github/ISSUE_TEMPLATE/) has a field for
exactly that).
