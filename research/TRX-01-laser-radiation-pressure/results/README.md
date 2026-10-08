# TRX-01 — the committed protocol

The deterministic output of the study script: the JSON protocol
[`trx01_results.json`](trx01_results.json) — the single numeric oracle the
study README, the monographs and the pytest guard quote. Nothing in
this folder is hand-written.

## The protocol schema

```jsonc
{
  "study": "trx-01",       // the study id
  "title": "…",                       // the study title
  "status": "PASS",               // the overall verdict
  "smoke": false,                     // whether this was a --smoke run
  "runtime_s": …,                     // the wall-time stamp (not a register)
  "checks": [ … ],                    // the registered checks, one entry each
  "series": { … },                   // the plotted series (the figure source)
  "meta": { … }                      // the full parameter snapshot
}
```

## The registered checks (6 / 6 PASS)

| check | registered band | recorded | unit | status |
|-------|-----------------|----------|------|:------:|
| `L1_abscissa_beta0` | `0.8369151` ± `5e-06` | `0.8369151258197127` | dimless | PASS |
| `L4_shift_monotone_in_beta` | `1.0` ± `1e-12` | `1.0` | bool | PASS |
| `L4_shift_toward_radiating_primary` | `1.0` ± `1e-12` | `1.0` | bool | PASS |
| `L4_max_Re_eigenvalue_beta0` | `0.0` ± `1e-08` | `1.8566962203814263e-16` | 1/time | PASS |
| `L1_shifts_toward_radiating_primary` | `1.0` ± `1e-12` | `1.0` | bool | PASS |
| `Jacobi_drift_L4_orbit_beta0.05` | `0.0` ± `1e-10` | `8.881784197001252e-16` | dimless | PASS |

Each check was registered — target and tolerance committed **before**
the recorded run. A check compares its recorded value against the band;
the overall `status` is PASS only when every check passes.


The companion [`trx01_plot.svg`](trx01_plot.svg) is the study's
vector plot snapshot — the same series the PNG gallery in
[`../figures/`](../figures/) renders at 300 dpi.

## Determinism and reproduction

```bash
python3 code/trx01_laser_radiation_pressure.py    # rewrites the protocol with identical numbers
```

Fixed seeds, fixed grids, no wall-clock dependence inside the registers.
A `git diff` on this folder after a re-run must show only the
`runtime_s` stamp changing; any drift in a check value is a
reproducibility bug — open an issue with the protocol attached (the
[issue template](../../../.github/ISSUE_TEMPLATE/) has a field for
exactly that).
