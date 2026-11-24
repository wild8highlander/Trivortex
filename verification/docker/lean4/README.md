# 🐳 docker · Lean 4 — Pinned Toolchain Image

> **Navigation:** [`verification`](../../README.md) › [`docker`](../README.md) › **`lean4`**

![Type](https://img.shields.io/badge/Type-Dockerfile-2496ED?style=flat-square&logo=docker&logoColor=white) ![Toolchain](https://img.shields.io/badge/Lean%204-v4.6.0-informational?style=flat-square&logo=lean) ![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)

The **Dockerfile pinning the Lean 4 (v4.6.0) environment** for this framework layer. The image installs elan and the pinned toolchain, fetches the Mathlib cache, compiles the formalization at image build time, and defaults to running `lake build` — so `docker run` reproduces exactly what CI runs, byte-for-byte at toolchain level.

## 📂 Contents — What Lives Here

| File | Size | Description |
|---|---|---|
| [`Dockerfile`](Dockerfile) | 1 018 B | Lean 4 v4.6.0 environment — ubuntu:24.04 + elan, toolchain pin, Mathlib cache, source copy, `lake build` entrypoint |

## ▶️ How to Run

```bash
# build exactly as CI does — the context is verification/ (the COPY paths):
cd verification
docker build -t rp-lean4 -f docker/lean4/Dockerfile .
docker run --rm rp-lean4
```

The build-time `RUN` executes `lake update && lake exe cache get! && lake build` — a broken formalization fails the image build, not just the run.

## 🔗 Cross-References

- [Docker layer](../README.md)
- [Language layer](../../lean4/README.md)

## 🇷🇺 Краткое резюме (Russian Summary)

Dockerfile со средой Lean 4 v4.6.0: база `ubuntu:24.04` + elan, тулчейн из `lean-toolchain`, кэш Mathlib при сборке, запуск `lake build` по умолчанию.

---

<div align="center">

**[⬆ Back to top](#-docker--lean-4--pinned-toolchain-image)** ·
**[Repository root](../../README.md)**

*Part of [wild8highlander/Trivortex](https://github.com/wild8highlander/Trivortex) · Licensed under [IPL-RP-1.0](https://github.com/wild8highlander/Trivortex/blob/main/LICENSE.md) — All Rights Reserved*

</div>

## Toolchain pin

| Pin | Value |
|---|---|
| Toolchain | Lean 4 **v4.6.0** |
| Toolchain file | `leanprover/lean4:v4.6.0` — [`verification/lean4/lean-toolchain`](../../lean4/lean-toolchain) |
| Base image | `ubuntu:24.04` + elan (`elan toolchain install v4.6.0`, `elan default v4.6.0`) |
| Mathlib | tag v4.6.0, resolved by [`lakefile.lean`](../../lean4/lakefile.lean); olean cache fetched at image build |
| Entrypoint | `lake build` |
| Pinned by | [`Dockerfile`](Dockerfile) |
| Built by | [`docker.yml`](../../../.github/workflows/docker.yml) |
| Status | **landed** — M1 (v1.1) plus the M4/M5 depth tracks: the artifact is [`Trivortex.lean`](../../lean4/Trivortex.lean) v5.0, §1–§9, 145 `#print axioms` statements, every footprint closed to exactly `propext`, `Classical.choice`, `Quot.sound` |

## What this image guarantees

- the same toolchain version on a laptop, in CI and on a contributor's machine —
  byte-for-byte at the toolchain level, so a proof that compiles here compiles
  everywhere;
- the verification sources are copied at build time and **compiled during the
  build** (`lake update && lake exe cache get! && lake build`); `docker run`
  re-executes `lake build` — the same entrypoint CI would;
- no floating-point drift question: the Lean artifact is a proof object, not a
  simulation — `#print axioms` reports the closed classical footprint on every
  theorem.

## Honest status

**The pin is real and the artifact has landed.** The image compiles
[`Trivortex.lean`](../../lean4/Trivortex.lean) (v5.0 statement layer, §1–§9)
against Lean v4.6.0 + Mathlib tag v4.6.0; a green `docker run` is the same
acceptance check the lean4 job of
[`verification-ports.yml`](../../../.github/workflows/verification-ports.yml)
performs (non-blocking until the three-green-days flip). What the landed
artifact proves — and what it deliberately does not yet prove — is stated in
the [Lean 4 hub](../../lean4/README.md); quote results from there, never from
this pin table alone.
