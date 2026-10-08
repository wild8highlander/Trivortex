# The Haskell integration suite

[`Ladder.hs`](Ladder.hs) — the Cabal test suite of the Haskell port: it
pins both the Double-precision and the exact ℚ(√3) registers of the
V1–V4 ladder against the committed reference numbers, and checks the
protocol payload stability.

## What the suite covers

- the **Double track**: choreography separations, periodicity, rigid
  rotation, integral conservation — each against its registered band;
- the **exact track**: the algebraic identities certified by evaluation
  on ℚ(√3) rationals — equality without tolerance;
- the **protocol contract**: JSON shape, deterministic fields, the
  bilingual report rendering.

## Running

```bash
cabal test    # from verification/haskell/
```

CI runs this suite in the non-blocking port job
([`verification-ports.yml`](../../../.github/workflows/verification-ports.yml)).
A new register means a new rung in
[`../src/Trivortex/Verify.hs`](../src/Trivortex/Verify.hs) with its
tolerance registered first, then a test here — the suite never asserts a
number that no protocol carries.
