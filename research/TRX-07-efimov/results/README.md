# TRX-07 — the committed protocol

The deterministic output of the study script: the JSON protocol
[`trx07_results.json`](trx07_results.json) — the single numeric oracle the
study README, the monographs and the pytest guard quote. Nothing in
this folder is hand-written.

## The protocol schema

```jsonc
{
  "study": "trx-07",       // the study id
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
| `s0_transcendental_root` | `1.0062458` ± `1e-05` | `1.0062378251027817` | dimless | PASS |
| `efimov_length_ratio` | `22.7` ± `0.05` | `22.694382595366676` | a-ratio | PASS |
| `efimov_energy_ratio` | `515.03` ± `0.05` | `515.0350013848819` | E-ratio | PASS |
| `spectrum_all_negative` | `1.0` ± `1e-12` | `1.0` | bool | PASS |
| `ladder_ratio_E0_over_E1` | `515.0350013848819` ± `180.26225048470863` | `515.4770480625078` | E-ratio | PASS |
| `ladder_ratio_E1_over_E2` | `515.0350013848819` ± `180.26225048470863` | `514.9320638190297` | E-ratio | PASS |

Each check was registered — target and tolerance committed **before**
the recorded run. A check compares its recorded value against the band;
the overall `status` is PASS only when every check passes.


The companion [`trx07_plot.svg`](trx07_plot.svg) is the study's
vector plot snapshot — the same series the PNG gallery in
[`../figures/`](../figures/) renders at 300 dpi.

## Determinism and reproduction

```bash
python3 code/trx07_efimov.py    # rewrites the protocol with identical numbers
```

Fixed seeds, fixed grids, no wall-clock dependence inside the registers.
A `git diff` on this folder after a re-run must show only the
`runtime_s` stamp changing; any drift in a check value is a
reproducibility bug — open an issue with the protocol attached (the
[issue template](../../../.github/ISSUE_TEMPLATE/) has a field for
exactly that).
