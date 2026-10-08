# TRX-09 — the committed protocol

The deterministic output of the study script: the JSON protocol
[`trx09_results.json`](trx09_results.json) — the single numeric oracle the
study README, the monographs and the pytest guard quote. Nothing in
this folder is hand-written.

## The protocol schema

```jsonc
{
  "study": "trx-09",       // the study id
  "title": "…",                       // the study title
  "status": "PASS",               // the overall verdict
  "smoke": false,                     // whether this was a --smoke run
  "runtime_s": …,                     // the wall-time stamp (not a register)
  "checks": [ … ],                    // the registered checks, one entry each
  "series": { … },                   // the plotted series (the figure source)
  "meta": { … }                      // the full parameter snapshot
}
```

## The registered checks (8 / 8 PASS)

| check | registered band | recorded | unit | status |
|-------|-----------------|----------|------|:------:|
| `rotation_rate_3G_over_2pi_a2` | `0.477464829275686` ± `1e-08` | `0.477464829275686` | 1/time | PASS |
| `triangle_stays_equilateral` | `0.0` ± `1e-08` | `3.3306690738754696e-16` | length | PASS |
| `angular_impulse_I_conserved` | `0.0` ± `1e-12` | `8.881784197001252e-16` | dimless | PASS |
| `hamiltonian_conserved` | `0.0` ± `1e-12` | `2.4737647522494027e-16` | dimless | PASS |
| `linear_impulse_conserved` | `0.0` ± `1e-12` | `7.216449660063518e-16` | dimless | PASS |
| `aref_collapse_conditions_hold` | `0.0` ± `1e-12` | `1.3877787807814457e-17` | dimless | PASS |
| `mixed_sign_invariants_conserved` | `0.0` ± `1e-11` | `1.3100631690576847e-14` | dimless | PASS |
| `mixed_sign_shape_evolves` | `1.0` ± `1e-12` | `1.0` | bool | PASS |

Each check was registered — target and tolerance committed **before**
the recorded run. A check compares its recorded value against the band;
the overall `status` is PASS only when every check passes.


The companion [`trx09_plot.svg`](trx09_plot.svg) is the study's
vector plot snapshot — the same series the PNG gallery in
[`../figures/`](../figures/) renders at 300 dpi.

## Determinism and reproduction

```bash
python3 code/trx09_classical_anchor.py    # rewrites the protocol with identical numbers
```

Fixed seeds, fixed grids, no wall-clock dependence inside the registers.
A `git diff` on this folder after a re-run must show only the
`runtime_s` stamp changing; any drift in a check value is a
reproducibility bug — open an issue with the protocol attached (the
[issue template](../../../.github/ISSUE_TEMPLATE/) has a field for
exactly that).
