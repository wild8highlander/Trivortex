# POLYVORTEX — the committed W-protocols

Seven deterministic JSON files, one per ladder stage, keyed to the
`default` preset. These files are the numeric oracle of the bench: the
tests pin to them (including the cross-validation against the parent
framework's ladder), the figure factory reads them, the READMEs and the
monographs quote them.

## The file index

| file | stage | check | headline recorded values |
|------|:-----:|-------|--------------------------|
| [`W1_anchor_default.json`](W1_anchor_default.json) | W1 | the Theorem-3.1 anchor at $N=3$: separation, periodicity, pinned literals | separation error `6.88e-14`; periodicity residual `9.39e-14`; $\omega$, $\varepsilon$ anchor errors `0.0` |
| [`W2_ring_rotation_default.json`](W2_ring_rotation_default.json) | W2 | the rigid rotation $\omega_N$, $N = 2..8$ | worst $\omega$ rel. error `2.86e-12`; worst shape deviation `3.35e-12` |
| [`W3_invariants_default.json`](W3_invariants_default.json) | W3 | the invariants $H, P, Q, I$ along the N-gon orbits | worst relative drift `4.32e-14` across $N = 2..8$ |
| [`W4_stability_default.json`](W4_stability_default.json) | W4 | the Havelock threshold: stable $N\le7$ / unstable $N\ge8$ | stable floor `≤ 7.0e-9`; $N=8$: `max Re λ = +0.4502` |
| [`W5_admissibility_default.json`](W5_admissibility_default.json) | W5 | the admissibility equivalence vs $\pi\ln 2$ | threshold `2.177586090303602`; 0 violations / 200 points; min-radius error `1.9e-7` |
| [`W6_obstruction_default.json`](W6_obstruction_default.json) | W6 | the kinematic obstruction (Lemma C) + the H1 shape register | induced radial velocity `≈ 1.3e-16`; phase-shifted shape fails linearly (slope $\sqrt{3}/2$) |
| [`W7_bridge_default.json`](W7_bridge_default.json) | W7 | the averaged-frequency bridge + the $T_{comp}$ table (D1) | integral identity `2.9e-15`; bridge `3.5e-15`; compatibility self-check `3.5e-16` |

## The schema (stable across stages)

```jsonc
{
  "suite": "polyvortex-ladder",
  "version": "1.1.0",
  "stage": "W4",
  "preset": "default",
  "date_utc": "…",                   // the run stamp (carries no role in the numbers)
  "check": { … },                    // the registered statement + recorded registers
  "params": { … },                   // the full parameter snapshot
  "passed": true
}
```

The **W1 anchor is the parent-binding stage**: its pinned literals
($\omega = 1.3748022274393588$, the separation and periodicity
residuals) are the same numbers the parent ladder V1 certifies — the two
ladders share no code, only these committed values.

## Regeneration and determinism

```bash
make ladder   # rewrites all seven files with identical numbers
```

Fixed grids, fixed integrator settings, deterministic linear algebra — a
`git diff` on this folder after a re-run must be empty; otherwise it is
a reproducibility bug: open an issue with the diff attached.
