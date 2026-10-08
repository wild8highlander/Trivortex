# TRX-03 — the committed protocol

The deterministic output of the study script: the JSON protocol
[`trx03_results.json`](trx03_results.json) — the single numeric oracle the
study README, the monographs and the pytest guard quote. Nothing in
this folder is hand-written.

## The protocol schema

```jsonc
{
  "study": "trx-03",       // the study id
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
| `pair_equilibrium_numeric_vs_analytic` | `0.0` ± `1e-10` | `5.551115123125783e-17` | length | PASS |
| `antiphase_pi2_purely_repulsive` | `1.0` ± `1e-12` | `1.0` | bool | PASS |
| `molecule_final_spacings_equal` | `0.0` ± `1e-08` | `2.220446049250313e-16` | length | PASS |
| `molecule_final_spacing_equals_s_star` | `0.0` ± `1e-06` | `2.7755575615628914e-17` | length | PASS |
| `conservative_energy_drift` | `0.0` ± `1e-10` | `1.3322676295501878e-15` | energy | PASS |
| `breathing_mode_frequency` | `0.46876631044552824` ± `0.004687663104455283` | `0.46882500000000005` | 1/time | PASS |

Each check was registered — target and tolerance committed **before**
the recorded run. A check compares its recorded value against the band;
the overall `status` is PASS only when every check passes.


The companion [`trx03_plot.svg`](trx03_plot.svg) is the study's
vector plot snapshot — the same series the PNG gallery in
[`../figures/`](../figures/) renders at 300 dpi.

## Determinism and reproduction

```bash
python3 code/trx03_soliton_molecule.py    # rewrites the protocol with identical numbers
```

Fixed seeds, fixed grids, no wall-clock dependence inside the registers.
A `git diff` on this folder after a re-run must show only the
`runtime_s` stamp changing; any drift in a check value is a
reproducibility bug — open an issue with the protocol attached (the
[issue template](../../../.github/ISSUE_TEMPLATE/) has a field for
exactly that).
