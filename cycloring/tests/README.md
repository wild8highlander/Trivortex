# CYCLORING — the pytest guard (37 tests)

The test suite of the mini-research. It re-derives every
preset-independent number of the W-ladder from first principles and pins
the preset-dependent ones to the committed protocols in
[`results/protocols/`](../results/protocols/) — so a green guard means
both the mathematics and the committed artifacts agree.

## Running the suite

```bash
make test                       # from the mini-research root: pytest tests/ -q
python3 -m pytest tests/ -v     # equivalent, verbose
```

Dependencies: `numpy`, `mpmath`, `pytest`. CI runs the same suite on
every push (Python 3.10 / 3.11 / 3.12 matrix) — see
[`ci.yml`](../../.github/workflows/ci.yml) at the repository root.

## The suites

| file | tests | what they guard |
|------|------:|-----------------|
| [`test_cr_periods.py`](test_cr_periods.py) | 7 | the reflection identity at 50 digits, `P(1,1) = 1`, the symmetry register, the boundary values of the registered levels |
| [`test_cr_chain.py`](test_cr_chain.py) | 10 | the defect chain step by step, the transducer and its inverse, the rows of the registered level table, the monotonic ordering of the stiffness |
| [`test_cr_dynamics.py`](test_cr_dynamics.py) | 10 | the Kirchhoff RHS against a hand-computed reference, the RK4 conserving register, the invariants `H, P, Q, I`, the closed-form Hamiltonian against pairwise summation, the rosette program of Theorem 4 |
| [`test_cr_ladder.py`](test_cr_ladder.py) | 10 | the ladder rungs themselves (quick in-process runs), the protocol shape and `passed` flags, the round-trip of the transducer, the sine-product register |

Plus [`conftest.py`](conftest.py): the shared fixtures — the
package-path bootstrap, the committed-protocol loader and the tolerance
constants.

## The testing philosophy

The suite follows the parent repository's registration discipline:

- **a test is a claim with a band.** Every numeric assertion compares
  against a tolerance that was chosen before the reference run, not
  tuned afterwards;
- **protocols are artifacts, not printouts.** The ladder's committed
  JSONs are load-bearing: the guard reads them and fails loudly if a
  re-derived number disagrees with the committed one;
- **self-contained by design.** The suite needs no network, no parent
  framework, no figures — it is the same 37 tests locally and in CI.

## Adding a test

New tests belong to the suite whose register they guard; a new register
means a new ladder stage first (with its tolerance registered in
[`ladder.py`](../python/cycloring/ladder.py) and a protocol committed),
then a test. Never assert a number that no protocol carries.
