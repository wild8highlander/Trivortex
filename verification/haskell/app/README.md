# The CLI entry point of the Haskell port

[`Main.hs`](Main.hs) — the executable entry point of the dual
(Double + exact ℚ(√3)) verification ladder: preset selection, the
V1–V4 registers, the bilingual report and the JSON protocol output.

## The module it serves

All logic lives in the library module
[`../src/Trivortex/Verify.hs`](../src/Trivortex/Verify.hs); the entry
point only parses arguments, runs the ladder and renders the results.
The design contract — thin CLI, testable library — mirrors the other
language ports.

## Build and run

```bash
cabal run -- --preset quick     # from verification/haskell/
```

or inside the pinned Docker toolchain
([`../../docker/haskell/`](../../docker/haskell/)). The suite that pins
this executable lives in [`../test/Ladder.hs`](../test/Ladder.hs); the
port contract and the tolerance policy are documented in the
[Haskell sources README](../src/README.md) and the
[verification README](../../README.md).
