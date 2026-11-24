<!-- markdownlint-disable-file MD041 -->
<div align="center">

# 🦀 The Rust Sources — the Memory-Safe Ladder Port (M1)

![Rust](https://img.shields.io/badge/Rust-1.77%20%28MSRV%201.75%29-DEA584?style=flat-square&logo=rust&logoColor=white)
![Type](https://img.shields.io/badge/Type-source%20map-2496ED?style=flat-square)
![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)

</div>

> **Navigation:** [`verification`](../../README.md) › [`rust`](../README.md) › **`src`**

The Rust implementation of the V1–V4 verification ladder — the second
floating-point language of milestone **M1**, proving the core registers
are not artifacts of one runtime.

## 📂 The Files

| File | Size | Lines | Role |
|---|---|---|---|
| [`lib.rs`](lib.rs) | 519 B | 12 | the library root: the closed form, the Chaplygin combination, the Kirchhoff RHS, the RK4 stepper (via its three modules) |
| [`verify.rs`](verify.rs) | 26 272 B | 732 | the ladder implementation: V1–V4 with recorded residuals against the registered bands; primitive f64 only — no collections, no I/O, no libc beyond libm — plus the 11 unit tests |
| [`report.rs`](report.rs) | 11 789 B | 367 | the dependency-free JSON protocol payload, CSV data and native SVG figure writers |
| [`i18n.rs`](i18n.rs) | 5 491 B | 82 | the bilingual (EN/RU) report strings — the same bilingual discipline as the rest of the repository |
| [`main.rs`](main.rs) | 24 138 B | 654 | the CLI entry point (`trivortex-lab`): presets, protocol output, exit codes CI keys on |

## ✅ What This Port Certifies

- **cross-runtime agreement**: the same V1–V4 residuals reproduced in a
  second floating-point runtime — 14/14 tests green (11 unit tests in
  [`verify.rs`](verify.rs) + 3 integration tests in
  [`../tests/ladder.rs`](../tests/ladder.rs));
- **memory safety without sacrificing determinism**: fixed grids, fixed
  stepper settings, byte-stable protocol output;
- **the bilingual report contract**: `--lang en|ru` mirrors the
  repository's two-language convention at the CLI level;
- **`no_std` readiness**: the core module confines itself to primitive
  f64 arithmetic, so a `no_std` port is a header change plus a libm crate.

## 🚀 Build and Run

```bash
cargo test --release          # the 14-test suite
cargo run --release -- --preset quick --lang en
```

Or via the pinned Docker toolchain
([`../../docker/rust/`](../../docker/rust/), image `rust:1.77`) for a
compiler-pinned, reproducible environment. The committed protocol values
that [`../../tests/test_ports.py`](../../tests/test_ports.py) pins
against were produced by this code.

## 🔗 The Port Contract

No code shared with the Python document or ladder — only the committed
numbers bind the implementations. The acceptance criteria and the
tolerance-band rationale live in the
[verification README](../README.md); the promotion path from
non-blocking to blocking CI is documented there as well. The statement
layer the residuals are measured against is formalized in the
[Lean 4 hub](../../lean4/README.md).

## 🇷🇺 Краткое резюме (Russian Summary)

- `src/verify.rs` — ядро-двойник лестницы V1–V4: аналитический слой,
  уравнения Кирхгофа, RK4, зарегистрированные полосы, 11 юнит-тестов;
  только примитивный f64 — без коллекций, I/O и libc кроме libm;
- `src/report.rs` / `src/i18n.rs` — JSON-протокол, CSV, векторные SVG и
  двуязычные строки EN/RU без единой зависимости;
- `src/main.rs` — CLI `trivortex-lab`: пресеты, меню, вывод протокола,
  коды выхода, на которые ключится CI;
- сертифицируется кросс-рантайм-согласие: те же остатки V1–V4 во второй
  плавающей реализации, 14/14 тестов зелёные;
- код с Python-документом и лестницей не разделяется — связывают только
  закоммиченные числа.

---

<div align="center">

**[⬆ Back to top](#-the-rust-sources--the-memory-safe-ladder-port-m1)** ·
**[Repository root](../../../README.md)**

*Part of [wild8highlander/Trivortex](https://github.com/wild8highlander/Trivortex) · Licensed under [IPL-RP-1.0](https://github.com/wild8highlander/Trivortex/blob/main/LICENSE.md) — All Rights Reserved*

</div>
