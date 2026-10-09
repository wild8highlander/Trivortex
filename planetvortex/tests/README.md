# PLANETVORTEX — the test guard

The pytest guard of the planetary bench: 59 tests re-deriving every
preset-independent number of the P-ladder and the hardcore X-register
and cross-pinning the heptagon register against the sibling polyvortex
bench.

## Running the suite

```bash
make test                       # from the mini-repo root
python3 -m pytest tests/ -v     # equivalent
```

The bootstrap (`conftest.py`) puts `python/` on `sys.path` for the
bench's own package and `../polyvortex/python` for the sibling oracle
— imported only by the cross-pin test, never at runtime.

## The suites

| file | tests | what they guard |
|------|------:|-----------------|
| `test_pv_fano.py` | 8 | the Fano axioms on $\mathbb{Z}_7$ (7 lines × 3 points, 21 pairs, 3 lines per point), the 168-element group in the cyclic and binary models, the explicit isomorphism and the congruent line-triangles, the mpmath closed forms, the $\sqrt{7}$ Hamiltonian identities |
| `test_pv_classical.py` | 8 | the sanity of the committed register, Kepler III measured in the two-body dynamics (corrected $10^{-9}$, the $\sqrt{1+m}$ signature exact), the Schwarzschild ladder, the Hill margins, the gravity ladder, the fact-sheet provenance bound |
| `test_pv_model.py` | 6 | the vectorized Kirchhoff RHS against the explicit pairwise sum, the invariant conservation, the analytic Jacobian against central differences, the rigid rotation of the heptagon at $1e-11$, the Havelock floor of $N = 7$, the exact ring geometry |
| `test_pv_nbody.py` | 6 | the two-body orbit closure at $10^{-12}$ (relative state), the exact barycentric momentum balance, the full-system conservation over the quick window, the secular band of the osculating elements, the perturbation hierarchy, the vis-viva anchor |
| `test_pv_ladder.py` | 7 | the quick ladder end-to-end, the committed protocol envelope, the pinned P1 literals, the P4 exactness, the P6 congruence (short window), the cross-pin against `polyvortex` (bit-for-bit $\omega_7$ and the ring Hamiltonian), the P7 bridge registers |
| `test_pv_hardcore.py` | 21 | the quick X-register end-to-end, the brute-force enumeration and the class equation, the 32-union simplicity certificate, the Sylow census, both actions and the $S_7$ bridge, the $(2,3,7)$ generation and the product-order distribution, the Hurwitz/Klein arithmetic, the hyperbolic identities and the disk witness, the measured orders 2/4, the bounded energy and the two-body invariants, the Mercury textbook anchor and the ordered precession ladder, the committed X-protocol envelope and headline pins |

## The cross-validation discipline

The cross-pin test imports the sibling package
(`pytest.importorskip("polyvortex")`) and asserts:

- `ngon_omega(1.0, 1.0, 7) == ring_omega(1.0, 1.0)` — bit-for-bit;
- the two independent Kirchhoff layers assign the same Hamiltonian and
  angular impulse to the same ring (within $10^{-12}$).

The two ladders share **no code**; only the committed numbers bind
them — the same discipline the parent applies to its language ports.

## The testing philosophy

A test is a claim with a band. The tolerances are chosen from the
physics of the band (integration order, window length, element
dynamics), committed before the recorded runs, and never tuned after.
Where a register cannot be exact (secular element drift, fact-sheet
provenance), the recorded value is quoted as a diagnostic with the
honest band in the docstring.

## Adding a test

A new test must either re-derive a number a protocol carries or pin a
closed form. Never assert a number that no protocol carries — run
`make all-ladders` first and bind the claim to the committed JSON.
