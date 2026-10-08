# The Haskell sources — the exact-arithmetic dual ladder (M3)

The Haskell implementation of milestone **M3**: the same V1–V4
registers computed twice — once in `Double` for the float envelope, once
in exact rational arithmetic over ℚ(√3) — so that algebraic identities
are certified *by evaluation*, not merely measured.

## The files

| file | role |
|------|------|
| [`src/Trivortex/Verify.hs`](Trivortex/Verify.hs) | the core module: the closed form, the Kirchhoff RHS, the RK4 stepper, the exact ℚ(√3) arithmetic, the V1–V4 registers |
| [`app/Main.hs`](../app/Main.hs) | the CLI entry point: presets, the dual-mode ladder, protocol output |
| [`test/Ladder.hs`](../test/Ladder.hs) | the integration suite pinning both the Double and the exact registers |

## The exact-arithmetic split

The equilateral choreography lives in ℚ(√3): the coordinates are exact
rational combinations of 1 and √3, so the algebraic identities of the
ladder (separations, the chord structure, the invariant values at the
anchor) are **decidable by computation** — equality on exact rationals
either holds or does not, with no tolerance involved. The Double track
runs the same registers in floating point and quantifies the envelope;
the exact track proves the identities hold by evaluation. The residual
split the C++ port measures, this port *closes*.

## Build and run

Inside the pinned Docker toolchain
([`../../docker/haskell/`](../../docker/haskell/)) for a
reproducible GHC environment:

```bash
cabal test       # the integration suite (test/Ladder.hs)
cabal run        # the dual ladder, default preset
```

The committed protocol values that
[`../../tests/test_ports.py`](../../tests/test_ports.py) pins against
were produced by this code.

## The port contract

No code shared with the Python document or ladder — only the committed
numbers bind the implementations. Acceptance criteria and tolerance
policy: the [verification README](../README.md).
