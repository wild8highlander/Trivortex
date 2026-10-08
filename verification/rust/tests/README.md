# The Rust integration suite — 14 tests, one per ladder register

The Cargo integration suite ([`ladder.rs`](ladder.rs)) that pins the
Rust ladder against the committed reference numbers — the artifact
behind the "14/14 tests" claim of the M1 milestone.

## What the suite checks

- **the V1 registers** — the closed-form choreography separations and
  the periodicity residual, against the committed band;
- **the V2 register** — the rigid Lagrange rotation: shape deviation
  and the measured ω against `3Γ/(2πa²)`;
- **the V3/V4 registers** — the conservation of `H, P, Q, I` for equal
  and unequal circulations, drifts against the registered band;
- **protocol stability** — the JSON payload shape, the bilingual report
  rendering, and the byte-stability of the deterministic fields.

## Running

```bash
cargo test --release     # from verification/rust/
```

The suite is also what CI's non-blocking port job runs (see
[`verification-ports.yml`](../../../.github/workflows/verification-ports.yml));
its promotion to blocking is governed by the policy in the
[verification README](../README.md) — three green days, then blocking.

## Adding a test

A new register means a new ladder rung first (tolerance registered in
[`../src/verify.rs`](../src/verify.rs) and a protocol committed), then a
test here. The suite never asserts a number that no protocol carries —
the same discipline as the pytest guard on the Python side.
