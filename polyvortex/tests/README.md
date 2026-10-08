# POLYVORTEX — the pytest guard (26 tests)

The test suite of the bench. It re-derives every preset-independent
number of the W-ladder and cross-pins the Theorem-3.1 anchor against the
parent framework's own reference values — a green guard means the bench,
its committed protocols and the parent ladder all agree.

## Running the suite

```bash
make test                       # from the mini-repo root: pytest tests/ -q
python3 -m pytest tests/ -v     # equivalent, verbose
```

Dependencies: `numpy`, `pytest` (the parent cross-pins additionally
locate the parent tree via the committed reference values). CI runs the
same suite on every push — see
[`ci.yml`](../../.github/workflows/ci.yml) at the repository root.

## The suites

| file | tests | what they guard |
|------|------:|-----------------|
| [`test_classical.py`](test_classical.py) | 5 | $\omega_N$ for $N = 2..8$, the chord pair-cancellation behind Lemma C, the unwrap register of the rotation measurement |
| [`test_ansatz.py`](test_ansatz.py) | 9 | the H1 radius and velocity fields, the $\pi\ln 2$ admissibility threshold, the amplitude-at-threshold identity, the min-radius polar register |
| [`test_model.py`](test_model.py) | 6 | the Kirchhoff RHS against finite differences, the invariants `H, P, Q, I` (including the parent-ladder cross-pin), conservation at $N = 4$, the neutral mode of the co-rotating spectrum |
| [`test_ladder.py`](test_ladder.py) | 6 | the ladder rungs themselves (quick in-process runs), the committed protocol shape and `passed` flags |

Plus [`conftest.py`](conftest.py): the package-path bootstrap, the
committed-protocol loader and the shared tolerance constants.

## The cross-validation discipline

The bench shares **no code** with the parent framework; the only thing
binding them is committed numbers. `test_model.py` asserts that the
bench's invariants match the parent ladder's reference values
bit-for-bit at the $N = 3$ anchor, exactly the way the parent treats its
language ports. If a future change breaks that pin, the failure is a
real physics or integration discrepancy — not a formatting artifact.

## The testing philosophy

The same registration discipline as everywhere in the program:

- **a test is a claim with a band** — tolerances chosen before the
  reference run, never tuned after;
- **protocols are artifacts, not printouts** — the guard reads
  [`results/protocols/`](../results/protocols/) and fails loudly on any
  disagreement;
- **self-contained by design** — no network, no figures, no document
  toolchain; the same 26 tests locally and in CI.

## Adding a test

A new register means a new ladder stage first (tolerance registered in
[`ladder.py`](../python/polyvortex/ladder.py), protocol committed), then
a test in the suite that owns the register. Never assert a number that
no protocol carries.
