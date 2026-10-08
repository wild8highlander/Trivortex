# CYCLORING — the committed W-protocols

Seven deterministic JSON files, one per ladder stage, keyed to the
`default` preset. These files are the numeric oracle of the whole
mini-research: the tests pin to them, the figure factory reads them, the
READMEs and the monographs quote them.

## The file index

| file | stage | check | headline recorded values |
|------|:-----:|-------|--------------------------|
| [`W1_period_core_default.json`](W1_period_core_default.json) | W1 | the reflection identity + `P(1,1)=1` + symmetry | max reflection residual `5.13e-49`; normalization and symmetry errors `0.0` |
| [`W2_algebraic_boundary_default.json`](W2_algebraic_boundary_default.json) | W2 | $\Omega_{a,N-a} = \pi/\sin(\pi a/N)$ + the sine product | max boundary residual `5.13e-49`; sine product residual `5.13e-49` |
| [`W3_root_system_default.json`](W3_root_system_default.json) | W3 | the $z^N - \sigma$ identity + moments + impulse | worst root-system residual `6.4e-11` (level 15); impulse residual `≤ 1.1e-15` |
| [`W4_polygon_flow_default.json`](W4_polygon_flow_default.json) | W4 | rigid rotation + shape + invariants + the $H$ form | $\omega$ rel. error `1.37e-12`; worst invariant drift `1.25e-14`; $H$ closed-form error `0.0` |
| [`W5_transport_identity_default.json`](W5_transport_identity_default.json) | W5 | the mean-transport law + the exact $2\pi$ phase advance | mpmath residual `2.67e-51`; float residual `4.44e-16`; phase advance error `1.78e-15` |
| [`W6_synchronous_closure_default.json`](W6_synchronous_closure_default.json) | W6 | the synchronous closure of the rosettes | closure residual `3.14e-16`; shape rigidity `4.44e-16`; radial excursion `7.33e-3` |
| [`W7_transducer_default.json`](W7_transducer_default.json) | W7 | the transducer table of the levels 7/9/15/30 | the four rows of the registered level table; ordering + round-trip checks |

## The schema (stable across stages)

```jsonc
{
  "stage": "W4",                     // the stage id
  "preset": "default",               // the preset key
  "check": "W4 polygon flow: …",     // the registered statement
  "…": "…",                          // stage-specific recorded registers
  "params": { … },                   // the full parameter snapshot of the run
  "passed": true                     // the verdict against the registered band
}
```

Two families of keys appear across the files:

- **identity registers** — residuals of algebraic identities, computed at
  50 mpmath digits, tolerance band $10^{-30}$;
- **dynamics registers** — RK4 rate errors and invariant drifts,
  tolerance bands $10^{-9}$ (rate) and $10^{-12}$ (drifts).

## Regeneration and determinism

```bash
make ladder   # rewrites all seven files with identical numbers
```

The runs are deterministic: fixed grids, fixed integrator settings, no
wall-clock fields inside the numbers (the runner stamps only the
protocol, not the values). A `git diff` on this folder after a re-run
must be empty; if it is not, that is a reproducibility bug — open an
issue with the diff attached.
