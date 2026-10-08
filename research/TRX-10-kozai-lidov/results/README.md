# TRX-10 — the committed protocol

The deterministic output of the study script: the JSON protocol
[`trx10_results.json`](trx10_results.json) — the single numeric oracle the
study README, the monographs and the pytest guard quote. Nothing in
this folder is hand-written.

## The protocol schema

```jsonc
{
  "study": "trx-10",       // the study id
  "title": "…",                       // the study title
  "status": "PASS",               // the overall verdict
  "smoke": false,                     // whether this was a --smoke run
  "runtime_s": …,                     // the wall-time stamp (not a register)
  "checks": [ … ],                    // the registered checks, one entry each
  "series": { … },                   // the plotted series (the figure source)
  "meta": { … }                      // the full parameter snapshot
}
```

## The registered checks (3 / 3 PASS)

| check | registered band | recorded | unit | status |
|-------|-----------------|----------|------|:------:|
| `e_max_i0_60` | `0.7637626158259733` ± `0.002` | `0.7637522326938432` | ecc | PASS |
| `e_max_i0_70` | `0.8972385613271877` ± `0.002` | `0.8972294445187509` | ecc | PASS |
| `kl_period_halves_with_m3` | `0.5` ± `0.03` | `0.4931728350700682` | ratio | PASS |

Each check was registered — target and tolerance committed **before**
the recorded run. A check compares its recorded value against the band;
the overall `status` is PASS only when every check passes.


The companion [`trx10_plot.svg`](trx10_plot.svg) is the study's
vector plot snapshot — the same series the PNG gallery in
[`../figures/`](../figures/) renders at 300 dpi.

## Determinism and reproduction

```bash
python3 code/trx10_kozai_lidov.py    # rewrites the protocol with identical numbers
```

Fixed seeds, fixed grids, no wall-clock dependence inside the registers.
A `git diff` on this folder after a re-run must show only the
`runtime_s` stamp changing; any drift in a check value is a
reproducibility bug — open an issue with the protocol attached (the
[issue template](../../../.github/ISSUE_TEMPLATE/) has a field for
exactly that).
