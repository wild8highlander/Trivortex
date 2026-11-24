# 🐳 docker · Rust — Pinned Toolchain Image

> **Navigation:** [`verification`](../../README.md) › [`docker`](../README.md) › **`rust`**

![Type](https://img.shields.io/badge/Type-Dockerfile-2496ED?style=flat-square&logo=docker&logoColor=white) ![Toolchain](https://img.shields.io/badge/Rust-1.77-informational?style=flat-square&logo=rust&logoColor=white) ![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)

The **Dockerfile pinning the Rust (1.77) environment** for this framework layer. The image uses the official `rust` base, copies the crate, runs the pinned-reference test guard at image build time (`cargo test --release`, `-O3`), and defaults to running the interactive laboratory at the `quick` preset — so `docker run` reproduces exactly what CI runs, byte-for-byte at toolchain level.

## 📂 Contents — What Lives Here

| File | Size | Description |
|---|---|---|
| [`Dockerfile`](Dockerfile) | 527 B | Rust 1.77 environment (`rust:1.77`) — source copy + `cargo test --release` acceptance check + laboratory entrypoint |

## ▶️ How to Run

```bash
# build exactly as CI does — the context is verification/ (the COPY paths):
cd verification
docker build -t rp-rust -f docker/rust/Dockerfile .
docker run --rm rp-rust
```

The build-time `RUN` executes `cargo test --release` — the numeric twin's pinned-reference guard plus the quick ladder; a red test fails the image build.

## 🔗 Cross-References

- [Docker layer](../README.md)
- [Language layer](../../rust/README.md)

## 🇷🇺 Краткое резюме (Russian Summary)

Dockerfile со средой Rust 1.77: база `rust:1.77`, `cargo test --release` при сборке образа, по умолчанию — лаборатория на пресете `quick` (`--no-menu --lang en`).

---

<div align="center">

**[⬆ Back to top](#-docker--rust--pinned-toolchain-image)** ·
**[Repository root](../../README.md)**

*Part of [wild8highlander/Trivortex](https://github.com/wild8highlander/Trivortex) · Licensed under [IPL-RP-1.0](https://github.com/wild8highlander/Trivortex/blob/main/LICENSE.md) — All Rights Reserved*

</div>

## Toolchain pin

| Pin | Value |
|---|---|
| Toolchain | Rust 1.77 (crate floor: `rust-version = "1.75"`, edition 2021) |
| Base image | `rust:1.77` |
| Build-time check | `cargo test --release` (pinned references + quick ladder, at `-O3`) |
| Entrypoint | `cargo run --release -- --preset quick --no-menu --lang en` |
| Pinned by | [`Dockerfile`](Dockerfile) |
| Built by | [`docker.yml`](../../../.github/workflows/docker.yml) |
| Status | **landed** — M1 (v1.1): the numeric twin crate passes 14/14 tests and commits [`protocol_quick.json`](../../rust/protocol_quick.json) — see the [Rust roadmap](../../rust/README.md) |

## What this image guarantees

- the same toolchain version on a laptop, in CI and on a contributor's machine —
  byte-for-byte at the toolchain level, so a proof that compiles here compiles
  everywhere;
- the crate is copied at build time and its **test guard runs during the
  build**; `docker run` starts the laboratory — the same entrypoint CI would;
- no floating-point drift question of the usual kind: this port *is* the
  floating-point twin — its whole job is to re-derive V1–V4 in a second
  float64 implementation and pin the result in a committed JSON protocol,
  which the [pytest guard](../../tests/README.md) cross-checks against the
  Python ladder inside the registered bands.

## Honest status

**The pin is real and the artifact has landed.** The image builds and tests
[`trivortex-verify`](../../rust/Cargo.toml) (14/14 pinned-reference tests,
quick ladder 4/4) and its committed protocol is machine-pinned against the
Python numbers. A green `docker run` mirrors the Rust job of
[`verification-ports.yml`](../../../.github/workflows/verification-ports.yml)
(non-blocking until the three-green-days flip). What the twin certifies — and
that its drifts are compared against tolerances, not bit-for-bit — is stated
in the [Rust roadmap](../../rust/README.md); quote results from there, never
from this pin table alone.
