# TRX-11 — the committed protocol

The deterministic output of the study script: the JSON protocol
[`trx11_results.json`](trx11_results.json) — the single numeric oracle the
study README, the monographs and the pytest guard quote. Nothing in
this folder is hand-written.

## The protocol schema

```jsonc
{
  "study": "trx-11",       // the study id
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
| `period_closure_error` | `0.0` ± `5e-08` | `1.2317358001612266e-08` | dimless | PASS |
| `period_in_expected_range` | `1.0` ± `1e-12` | `1.0` | bool | PASS |
| `energy_conserved` | `0.0` ± `1e-12` | `3.3306690738754696e-15` | energy | PASS |
| `angular_momentum_is_zero` | `0.0` ± `1e-09` | `1.4432899320127035e-15` | ang mom | PASS |
| `luminosity_finite_positive` | `1.0` ± `1e-12` | `1.0` | bool | PASS |
| `dominant_harmonic_on_comb` | `0.0` ± `0.05` | `0.0014996250937269195` | harmonic index | PASS |

Each check was registered — target and tolerance committed **before**
the recorded run. A check compares its recorded value against the band;
the overall `status` is PASS only when every check passes.


The companion [`trx11_plot.svg`](trx11_plot.svg) is the study's
vector plot snapshot — the same series the PNG gallery in
[`../figures/`](../figures/) renders at 300 dpi.

## Determinism and reproduction

```bash
python3 code/trx11_gw_choreography.py    # rewrites the protocol with identical numbers
```

Fixed seeds, fixed grids, no wall-clock dependence inside the registers.
A `git diff` on this folder after a re-run must show only the
`runtime_s` stamp changing; any drift in a check value is a
reproducibility bug — open an issue with the protocol attached (the
[issue template](../../../.github/ISSUE_TEMPLATE/) has a field for
exactly that).
