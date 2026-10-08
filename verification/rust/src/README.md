# The Rust sources — the memory-safe ladder port (M1)

The Rust implementation of the V1–V4 verification ladder — the second
floating-point language of milestone **M1**, proving the core registers
are not artifacts of one runtime.

## The files

| file | role |
|------|------|
| [`lib.rs`](lib.rs) | the library root: the closed form, the Chaplygin combination, the Kirchhoff RHS, the RK4 stepper |
| [`verify.rs`](verify.rs) | the ladder implementation: V1–V4 with recorded residuals against the registered bands |
| [`report.rs`](report.rs) | the JSON protocol payload and the human-readable report rendering |
| [`i18n.rs`](i18n.rs) | the bilingual (EN/RU) report strings — the same bilingual discipline as the rest of the repository |
| [`main.rs`](main.rs) | the CLI entry point: presets, protocol output, exit codes CI keys on |

## What this port certifies

- **cross-runtime agreement**: the same V1–V4 residuals reproduced in a
  second floating-point runtime — 14/14 integration tests green (see
  [`../tests/ladder.rs`](../tests/ladder.rs));
- **memory safety without sacrificing determinism**: fixed grids, fixed
  stepper settings, byte-stable protocol output;
- **the bilingual report contract**: `--lang en|ru` mirrors the
  repository's two-language convention at the CLI level.

## Build and run

```bash
cargo test --release          # the 14-test suite (../tests/ladder.rs)
cargo run --release -- --preset quick --lang en
```

Or via the pinned Docker toolchain
([`../../docker/rust/`](../../docker/rust/)) for a compiler-pinned,
reproducible environment. The committed protocol values that
[`../../tests/test_ports.py`](../../tests/test_ports.py) pins against
were produced by this code.

## The port contract

No code shared with the Python document or ladder — only the committed
numbers bind the implementations. The acceptance criteria and the
tolerance-band rationale live in the [verification
README](../README.md); the promotion path from non-blocking to blocking
CI is documented there as well.
