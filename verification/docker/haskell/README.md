# 🐳 docker · Haskell — Pinned Toolchain Image

> **Navigation:** [`verification`](../../README.md) › [`docker`](../README.md) › **`haskell`**

![Type](https://img.shields.io/badge/Type-Dockerfile-2496ED?style=flat-square&logo=docker&logoColor=white) ![Toolchain](https://img.shields.io/badge/GHC-9.4-informational?style=flat-square&logo=haskell&logoColor=white) ![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)

The **Dockerfile pinning the Haskell (GHC 9.4) environment** for this framework layer. The image uses the official `haskell` slim base, copies the cabal project, updates the package index, builds and tests at image build time (`cabal test trivortex-guard` — the pinned-reference guard plus the exact ℚ(√3) anchor identities), and defaults to running the dual laboratory — so `docker run` reproduces exactly what CI runs, byte-for-byte at toolchain level.

## 📂 Contents — What Lives Here

| File | Size | Description |
|---|---|---|
| [`Dockerfile`](Dockerfile) | 553 B | GHC 9.4 environment (`haskell:9.4-slim`) — source copy + `cabal build`/`cabal test` acceptance check + laboratory entrypoint |

## ▶️ How to Run

```bash
# build exactly as CI does — the context is verification/ (the COPY paths):
cd verification
docker build -t rp-haskell -f docker/haskell/Dockerfile .
docker run --rm rp-haskell
```

The build-time `RUN` executes `cabal update && cabal build all && cabal test trivortex-guard` — a red guard fails the image build. The entrypoint pipes `0` into the lab's menu, the scripted non-interactive entry.

## 🔗 Cross-References

- [Docker layer](../README.md)
- [Language layer](../../haskell/README.md)

## 🇷🇺 Краткое резюме (Russian Summary)

Dockerfile со средой GHC 9.4: база `haskell:9.4-slim`, `cabal update && cabal build all && cabal test trivortex-guard` при сборке образа, по умолчанию — двойная лаборатория (`echo 0 | cabal run trivortex-lab`).

---

<div align="center">

**[⬆ Back to top](#-docker--haskell--pinned-toolchain-image)** ·
**[Repository root](../../README.md)**

*Part of [wild8highlander/Trivortex](https://github.com/wild8highlander/Trivortex) · Licensed under [IPL-RP-1.0](https://github.com/wild8highlander/Trivortex/blob/main/LICENSE.md) — All Rights Reserved*

</div>

## Toolchain pin

| Pin | Value |
|---|---|
| Toolchain | Haskell (GHC) 9.4 |
| Base image | `haskell:9.4-slim` |
| Build-time check | `cabal update && cabal build all && cabal test trivortex-guard` |
| Entrypoint | `echo 0 | cabal run trivortex-lab` |
| Pinned by | [`Dockerfile`](Dockerfile) |
| Built by | [`docker.yml`](../../../.github/workflows/docker.yml) |
| Status | **landed** — M3 (v1.1): the dual ladder runs — `Double` plus the exact ℚ(√3) run, where the equilateral anchor identities hold by computation — see the [Haskell roadmap](../../haskell/README.md) |

## What this image guarantees

- the same toolchain version on a laptop, in CI and on a contributor's machine —
  byte-for-byte at the toolchain level, so a proof that compiles here compiles
  everywhere;
- the project is copied at build time and its **guard test runs during the
  build**; `docker run` starts the dual laboratory — the same entrypoint CI
  would;
- the exactness story is the point of this port: the `Double` ladder rides the
  usual float64 bands, while the ℚ(√3) dual certifies the equilateral anchors
  in exact arithmetic; extending the exact run to the full V1–V4 loop is the
  pre-registered M5 track ("Exact Haskell everywhere").

## Honest status

**The pin is real and the artifact has landed.** The image builds and guards
[`trivortex-verify`](../../haskell/trivortex-verify.cabal) — the M3 dual
ladder — and a green `docker run` mirrors the Haskell job of
[`verification-ports.yml`](../../../.github/workflows/verification-ports.yml)
(non-blocking until the three-green-days flip). Exactly which anchors are
exact and which checks stay float64 is stated in the
[Haskell (GHC) roadmap](../../haskell/README.md); quote results from there,
never from this pin table alone.
