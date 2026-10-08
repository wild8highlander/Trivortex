# TRX-08 — the committed protocol

The deterministic output of the study script: the JSON protocol
[`trx08_results.json`](trx08_results.json) — the single numeric oracle the
study README, the monographs and the pytest guard quote. Nothing in
this folder is hand-written.

## The protocol schema

```jsonc
{
  "study": "trx-08",       // the study id
  "title": "…",                       // the study title
  "status": "PASS",               // the overall verdict
  "smoke": false,                     // whether this was a --smoke run
  "runtime_s": …,                     // the wall-time stamp (not a register)
  "checks": [ … ],                    // the registered checks, one entry each
  "series": { … },                   // the plotted series (the figure source)
  "meta": { … }                      // the full parameter snapshot
}
```

## The registered checks (10 / 10 PASS)

| check | registered band | recorded | unit | status |
|-------|-----------------|----------|------|:------:|
| `global_minimum_reached` | `0.0` ± `1e-09` | `0.0` | energy | PASS |
| `crystallization_energy_released` | `1.0` ± `1e-12` | `1.0` | bool | PASS |
| `crystal_side_equals_analytic` | `1.4422495703074083` ± `1e-08` | `1.442249570307408` | length | PASS |
| `crystal_equilateral` | `0.0` ± `1e-08` | `0.0` | length | PASS |
| `crystal_angles_120deg` | `0.0` ± `1e-06` | `4.440892098500626e-16` | rad | PASS |
| `zero_rotation_mode` | `1.0` ± `1e-12` | `1.0` | bool | PASS |
| `two_com_modes_at_omega0` | `1.0` ± `1e-12` | `1.0` | bool | PASS |
| `breathing_mode_sqrt3` | `1.0` ± `1e-12` | `1.0` | bool | PASS |
| `static_equilibrium_holds` | `0.0` ± `1e-09` | `1.3877787807814457e-15` | length | PASS |
| `conservative_energy_conserved` | `0.0` ± `1e-10` | `8.881784197001252e-16` | energy | PASS |

Each check was registered — target and tolerance committed **before**
the recorded run. A check compares its recorded value against the band;
the overall `status` is PASS only when every check passes.


The companion [`trx08_plot.svg`](trx08_plot.svg) is the study's
vector plot snapshot — the same series the PNG gallery in
[`../figures/`](../figures/) renders at 300 dpi.

## Determinism and reproduction

```bash
python3 code/trx08_ion_trap.py    # rewrites the protocol with identical numbers
```

Fixed seeds, fixed grids, no wall-clock dependence inside the registers.
A `git diff` on this folder after a re-run must show only the
`runtime_s` stamp changing; any drift in a check value is a
reproducibility bug — open an issue with the protocol attached (the
[issue template](../../../.github/ISSUE_TEMPLATE/) has a field for
exactly that).
