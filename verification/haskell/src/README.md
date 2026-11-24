<!-- markdownlint-disable-file MD041 -->
<div align="center">

# 📐 The Haskell Sources — the Exact-Arithmetic Dual Ladder (M3)

![Haskell](https://img.shields.io/badge/Haskell-GHC%209.4-5E5061?style=flat-square&logo=haskell&logoColor=white)
![Type](https://img.shields.io/badge/Type-library-2496ED?style=flat-square)
![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)

</div>

> **Navigation:** [`verification`](../../README.md) › [`haskell`](../README.md) › **`src`**

The Haskell implementation of milestone **M3**: the same V1–V4
registers computed twice — once in `Double` for the float envelope, once
in exact rational arithmetic over ℚ(√3) — so that algebraic identities
are certified *by evaluation*, not merely measured.

## 📂 The Files

| File | Size | Lines | Role |
|---|---|---|---|
| [`Trivortex/Verify.hs`](Trivortex/Verify.hs) | 28 676 B | 729 | the core module: the closed form, the Kirchhoff RHS, the RK4 stepper, the exact ℚ(√3) arithmetic, the V1–V4 registers (`checkV1`–`checkV4`), `runLadder`, `exactAnchors` |
| [`../app/Main.hs`](../app/Main.hs) | 12 277 B | 250 | the CLI entry point: presets, the dual-mode ladder, protocol output |
| [`../test/Ladder.hs`](../test/Ladder.hs) | 4 725 B | 106 | the integration suite pinning both the `Double` and the exact registers |

## ✅ The Exact-Arithmetic Split

The equilateral choreography lives in ℚ(√3): the coordinates are exact
rational combinations of 1 and √3, so the algebraic identities of the
ladder (separations, the chord structure, the invariant values at the
anchor) are **decidable by computation** — equality on exact rationals
either holds or does not, with no tolerance involved. Concretely, the
exact dual represents numbers as `p + q·√3` with `Rational` coefficients
and decides equality via `p = p' ∧ q = q'` (correct because √3 is
irrational); the five certified anchor identities are the side squares
exactly 1, `P = 0`, `Q = 0`, `I = Γ`, `H = 0`. The `Double` track runs
the same registers in floating point and quantifies the envelope; the
residual split the C++ port measures, this port *closes*.

## 🚀 Build and Run

Inside the pinned Docker toolchain
([`../../docker/haskell/`](../../docker/haskell/), image
`haskell:9.4-slim`) for a reproducible GHC environment:

```bash
cabal test       # the integration suite (test/Ladder.hs)
cabal run        # the dual ladder, default preset
```

The library depends on nothing but `base` (`-O2 -Wall`) — the
floating-point path is exactly the platform's, with no library in
between. The committed protocol values that
[`../../tests/test_ports.py`](../../tests/test_ports.py) pins against
were produced by this code.

## 🔗 The Port Contract

No code shared with the Python document or ladder — only the committed
numbers bind the implementations. Acceptance criteria and tolerance
policy: the [verification README](../README.md); the statement layer the
anchors mirror: the [Lean 4 hub](../../lean4/README.md).

## 🇷🇺 Краткое резюме (Russian Summary)

- `src/Trivortex/Verify.hs` — ядро порта: f64-двойник лестницы V1–V4
  (те же формулы и допуски) плюс точный dual на ℚ(√3);
- числа точного трека — `p + q·√3` с коэффициентами из `Rational`;
  равенство разрешимо (√3 иррационален), поэтому якоря
  `P = 0, Q = 0, I = Γ, H = 0` и квадраты сторон = 1 выполняются
  **вычислением**, без допусков;
- библиотека зависит только от `base` (`-O2 -Wall`): плавающий путь —
  ровно платформенный;
- расщепление остатка, которое измеряет порт C++, здесь замыкается;
  закоммиченные числа, к которым пиннится pytest-защита, произведены
  этим кодом.

---

<div align="center">

**[⬆ Back to top](#-the-haskell-sources--the-exact-arithmetic-dual-ladder-m3)** ·
**[Repository root](../../../README.md)**

*Part of [wild8highlander/Trivortex](https://github.com/wild8highlander/Trivortex) · Licensed under [IPL-RP-1.0](https://github.com/wild8highlander/Trivortex/blob/main/LICENSE.md) — All Rights Reserved*

</div>
