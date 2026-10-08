# TRX-05 — the committed protocol

The deterministic output of the study script: the JSON protocol
[`trx05_results.json`](trx05_results.json) — the single numeric oracle the
study README, the monographs and the pytest guard quote. Nothing in
this folder is hand-written.

## The protocol schema

```jsonc
{
  "study": "trx-05",       // the study id
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
| `rotation_rate_vs_analytic` | `0.477464829275686` ± `1e-08` | `0.47746482927568645` | 1/time | PASS |
| `angular_impulse_I_conserved` | `0.0` ± `1e-12` | `1.3322676295501878e-15` | dimless | PASS |
| `kirchhoff_hamiltonian_conserved` | `0.0` ± `1e-12` | `3.5339496460705754e-16` | dimless | PASS |
| `field_minima_track_vortices` | `0.0` ± `0.06000000000000005` | `0.01612500200232333` | length | PASS |
| `total_winding_number_is_3` | `3.0` ± `1e-12` | `3.0` | integer | PASS |

Each check was registered — target and tolerance committed **before**
the recorded run. A check compares its recorded value against the band;
the overall `status` is PASS only when every check passes.


The companion [`trx05_plot.svg`](trx05_plot.svg) is the study's
vector plot snapshot — the same series the PNG gallery in
[`../figures/`](../figures/) renders at 300 dpi.

## Determinism and reproduction

```bash
python3 code/trx05_optical_vortices.py    # rewrites the protocol with identical numbers
```

Fixed seeds, fixed grids, no wall-clock dependence inside the registers.
A `git diff` on this folder after a re-run must show only the
`runtime_s` stamp changing; any drift in a check value is a
reproducibility bug — open an issue with the protocol attached (the
[issue template](../../../.github/ISSUE_TEMPLATE/) has a field for
exactly that).
