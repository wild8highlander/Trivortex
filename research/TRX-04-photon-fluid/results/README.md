# TRX-04 — the committed protocol

The deterministic output of the study script: the JSON protocol
[`trx04_results.json`](trx04_results.json) — the single numeric oracle the
study README, the monographs and the pytest guard quote. Nothing in
this folder is hand-written.

## The protocol schema

```jsonc
{
  "study": "trx-04",       // the study id
  "title": "…",                       // the study title
  "status": "PASS",               // the overall verdict
  "smoke": false,                     // whether this was a --smoke run
  "runtime_s": …,                     // the wall-time stamp (not a register)
  "checks": [ … ],                    // the registered checks, one entry each
  "series": { … },                   // the plotted series (the figure source)
  "meta": { … }                      // the full parameter snapshot
}
```

## The registered checks (9 / 9 PASS)

| check | registered band | recorded | unit | status |
|-------|-----------------|----------|------|:------:|
| `triangle_equilateral_deviation` | `0.0` ± `1e-06` | `4.440892098500626e-15` | rel | PASS |
| `measured_rotation_rate` | `0.22313016014842985` ± `1e-08` | `0.2231301601484294` | 1/time | PASS |
| `energy_conservation_rotation` | `0.0` ± `1e-10` | `2.220446049250313e-16` | energy | PASS |
| `angular_momentum_conservation` | `0.0` ± `1e-10` | `8.881784197001252e-16` | ang mom | PASS |
| `antiphase_no_collapse` | `1.0` ± `1e-12` | `1.0` | bool | PASS |
| `antiphase_expands` | `1.0` ± `1e-12` | `1.0` | bool | PASS |
| `energy_conservation_repulsion` | `0.0` ± `1e-10` | `3.0531133177191805e-16` | energy | PASS |
| `binary_stays_bound` | `1.0` ± `1e-12` | `1.0` | bool | PASS |
| `binary_energy_conservation` | `0.0` ± `1e-10` | `1.7706530686112387e-12` | energy | PASS |

Each check was registered — target and tolerance committed **before**
the recorded run. A check compares its recorded value against the band;
the overall `status` is PASS only when every check passes.


The companion [`trx04_plot.svg`](trx04_plot.svg) is the study's
vector plot snapshot — the same series the PNG gallery in
[`../figures/`](../figures/) renders at 300 dpi.

## Determinism and reproduction

```bash
python3 code/trx04_photon_fluid.py    # rewrites the protocol with identical numbers
```

Fixed seeds, fixed grids, no wall-clock dependence inside the registers.
A `git diff` on this folder after a re-run must show only the
`runtime_s` stamp changing; any drift in a check value is a
reproducibility bug — open an issue with the protocol attached (the
[issue template](../../../.github/ISSUE_TEMPLATE/) has a field for
exactly that).
