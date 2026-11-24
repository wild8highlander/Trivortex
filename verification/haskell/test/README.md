<!-- markdownlint-disable-file MD041 -->
<div align="center">

# 🧪 The Haskell Integration Suite

![Haskell](https://img.shields.io/badge/Haskell-GHC%209.4-5E5061?style=flat-square&logo=haskell&logoColor=white)
![Type](https://img.shields.io/badge/Type-test%20suite-2EA043?style=flat-square)
[![Ports CI](https://img.shields.io/github/actions/workflow/status/wild8highlander/Trivortex/verification-ports.yml?branch=main&style=flat-square&label=Ports%20CI)](https://github.com/wild8highlander/Trivortex/actions/workflows/verification-ports.yml)
![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)

</div>

> **Navigation:** [`verification`](../../README.md) › [`haskell`](../README.md) › **`test`**

[`Ladder.hs`](Ladder.hs) — the Cabal test suite `trivortex-guard` of the
Haskell port: it pins both the `Double`-precision and the exact ℚ(√3)
registers of the V1–V4 ladder against the committed reference numbers,
and checks the protocol payload stability.

## 📂 The File

| File | Size | Lines | Role |
|---|---|---|---|
| [`Ladder.hs`](Ladder.hs) | 4 725 B | 106 | 21 checks (`r1`–`r21`): analytic pins mirroring `test_trivortex.py`, the quick-ladder verdicts and bands, the exact-anchor check, the JSON smoke |

## ✅ What the Suite Covers

- the **Double track**: choreography separations, periodicity, rigid
  rotation, integral conservation — each against its registered band
  (V1 residuals `1e-12`, V2 shape `1e-10` / omega `1e-6`, V3/V4 drifts
  `1e-10`) plus the cross-language pin ω = `0.477464829275686`;
- the **exact track**: the algebraic identities certified by evaluation
  on ℚ(√3) rationals — check `r19` requires all five `exactAnchors`
  identities (side squares exactly 1; `P = 0`; `Q = 0`; `I = Γ`;
  `H = 0`) — equality without tolerance;
- the **protocol contract**: JSON shape, deterministic fields, the
  bilingual report rendering.

## 🚀 Running

```bash
cabal test    # from verification/haskell/
```

CI runs this suite in the non-blocking port job *haskell-dual-ladder*
([`verification-ports.yml`](https://github.com/wild8highlander/Trivortex/actions/workflows/verification-ports.yml);
definition in
[`../../../.github/workflows/verification-ports.yml`](../../../.github/workflows/verification-ports.yml)).

## 🔗 Adding a Test

A new register means a new rung in
[`../src/Trivortex/Verify.hs`](../src/Trivortex/Verify.hs) with its
tolerance registered first, then a test here — the suite never asserts a
number that no protocol carries. The tolerance bands themselves are
registered in the [verification README](../README.md); the statement
layer they measure against is formalized in the
[Lean 4 hub](../../lean4/README.md).

## 🇷🇺 Краткое резюме (Russian Summary)

- `test/Ladder.hs` — cabal-набор `trivortex-guard`: 21 проверка
  (`r1`–`r21`), пиннящая регистры `Double` и точного ℚ(√3) к
  закоммиченным опорным числам;
- трек `Double`: разделения хореографии, периодичность, жёсткое вращение,
  сохранение интегралов — каждый против своей зарегистрированной полосы,
  плюс кросс-языковой пин ω = 0.477464829275686;
- точный трек: пять якорных тождеств ℚ(√3) (квадраты сторон 1; P = 0;
  Q = 0; I = Γ; H = 0) — равенство без допусков, проверка `r19`;
- контракт протокола: форма JSON, детерминированные поля, двуязычный
  рендеринг отчёта; CI гоняет набор в задании *haskell-dual-ladder*.

---

<div align="center">

**[⬆ Back to top](#-the-haskell-integration-suite)** ·
**[Repository root](../../../README.md)**

*Part of [wild8highlander/Trivortex](https://github.com/wild8highlander/Trivortex) · Licensed under [IPL-RP-1.0](https://github.com/wild8highlander/Trivortex/blob/main/LICENSE.md) — All Rights Reserved*

</div>
