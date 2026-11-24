<!-- markdownlint-disable-file MD041 -->
<div align="center">

# 🧪 The Rust Integration Suite — 14 Tests

![Rust](https://img.shields.io/badge/Rust-1.77%20%28MSRV%201.75%29-DEA584?style=flat-square&logo=rust&logoColor=white)
![Type](https://img.shields.io/badge/Type-test%20suite-2EA043?style=flat-square)
[![Ports CI](https://img.shields.io/github/actions/workflow/status/wild8highlander/Trivortex/verification-ports.yml?branch=main&style=flat-square&label=Ports%20CI)](https://github.com/wild8highlander/Trivortex/actions/workflows/verification-ports.yml)
![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)

</div>

> **Navigation:** [`verification`](../../README.md) › [`rust`](../README.md) › **`tests`**

The Cargo integration suite ([`ladder.rs`](ladder.rs)) that pins the
Rust ladder against the committed reference numbers — the artifact
behind the "14/14 tests" claim of the M1 milestone. The 14 `cargo test`
checks split into 3 integration tests here plus the 11 unit tests inside
[`../src/verify.rs`](../src/verify.rs).

## 📂 The File

| File | Size | Lines | Tests |
|---|---|---|---|
| [`ladder.rs`](ladder.rs) | 2 359 B | 58 | 3 integration tests: `quick_preset_reproduces_python_reference_verdict`, `quick_preset_tolerances_match_registered_bands`, `default_preset_stays_green` |

## ✅ What the Suite Checks

- **the Python cross-language pin** — for the quick preset the Python
  ladder reports ω = `0.477464829275686` (Γ = 1, a = 1) with every check
  inside its registered band; the Rust twin must agree to the same bands,
  not necessarily bit-for-bit (different libm calls) but inside every
  documented tolerance;
- **the V1 registers** — the closed-form choreography separations
  (`angular_separation_error`) and the periodicity residual, against the
  committed `1e-12` band;
- **the V2 register** — the rigid Lagrange rotation: `shape_drift`
  against `1e-10` and the measured ω (`omega_relative_error`) against
  `1e-6`, plus the analytic ω pin `0.477464829275686` to `1e-12`;
- **the V3/V4 registers** — the conservation of `H, P, Q, I` for equal
  (`worst_drift` of V3) and unequal circulations Γ = (1, 2, 3) (V4),
  drifts against the registered `1e-10` band;
- **the default preset stays green** — every check of the full `default` ladder run passes;
- **protocol stability** — the JSON payload shape (`report_schema_shape` among the unit tests) and the byte-stability of the deterministic fields.

## 🚀 Running

```bash
cargo test --release     # from verification/rust/
```

The suite is also what CI's non-blocking port job *rust-numeric-twin*
runs ([`verification-ports.yml`](https://github.com/wild8highlander/Trivortex/actions/workflows/verification-ports.yml);
definition in
[`../../../.github/workflows/verification-ports.yml`](../../../.github/workflows/verification-ports.yml));
its promotion to blocking is governed by the policy in the
[verification README](../README.md) — three green days, then blocking.

## 🔗 Adding a Test

A new register means a new ladder rung first (tolerance registered in
[`../src/verify.rs`](../src/verify.rs) and a protocol committed), then a
test here. The suite never asserts a number that no protocol carries —
the same discipline as the pytest guard on the Python side. The
statement layer the numbers are measured against is formalized in the
[Lean 4 hub](../../lean4/README.md).

## 🇷🇺 Краткое резюме (Russian Summary)

- `tests/ladder.rs` — интеграционный набор из 3 тестов, пиннящий
  Rust-лестницу к закоммиченным опорным числам; вместе с 11 юнит-тестами
  в `src/verify.rs` это те самые 14/14 из вехи M1;
- кросс-языковой пин Python: ω = 0.477464829275686 при Γ = 1, a = 1,
  каждая проверка внутри своей полосы;
- регистры V1 (остатки ≤ 1e-12), V2 (форма ≤ 1e-10, ω ≤ 1e-6) и
  V3/V4 (дрейфы инвариантов ≤ 1e-10 при равных и неравных циркуляциях);
- пресет default остаётся зелёным целиком; CI гоняет набор в задании
  *rust-numeric-twin*, перевод в blocking — по политике «три зелёных дня».

---

<div align="center">

**[⬆ Back to top](#-the-rust-integration-suite--14-tests)** ·
**[Repository root](../../../README.md)**

*Part of [wild8highlander/Trivortex](https://github.com/wild8highlander/Trivortex) · Licensed under [IPL-RP-1.0](https://github.com/wild8highlander/Trivortex/blob/main/LICENSE.md) — All Rights Reserved*

</div>
