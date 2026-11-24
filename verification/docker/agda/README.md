# 🐳 docker · Agda — Pinned Toolchain Image

> **Navigation:** [`verification`](../../README.md) › [`docker`](../README.md) › **`agda`**

![Type](https://img.shields.io/badge/Type-Dockerfile-2496ED?style=flat-square&logo=docker&logoColor=white) ![Toolchain](https://img.shields.io/badge/Agda-2.6.4-informational?style=flat-square) ![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)

The **Dockerfile pinning the Agda (2.6.4) environment** for this framework layer. The image uses the official `agda/agda` base (the standard library ships inside the image), copies the sources, type-checks the constructive module at image build time, and defaults to running `agda Trivortex.agda` — so `docker run` reproduces exactly what CI runs, byte-for-byte at toolchain level.

## 📂 Contents — What Lives Here

| File | Size | Description |
|---|---|---|
| [`Dockerfile`](Dockerfile) | 581 B | Agda 2.6.4 environment (`agda/agda:2.6.4`) — source copy + `agda Trivortex.agda` acceptance check + verification entrypoint |

## ▶️ How to Run

```bash
# build exactly as CI does — the context is verification/ (the COPY paths):
cd verification
docker build -t rp-agda -f docker/agda/Dockerfile .
docker run --rm rp-agda
```

The build-time `RUN` executes `agda Trivortex.agda` and removes the `.agdai`/`_build` products, so the image carries the sources, not stale artifacts.

## 🔗 Cross-References

- [Docker layer](../README.md)
- [Language layer](../../agda/README.md)

## 🇷🇺 Краткое резюме (Russian Summary)

Dockerfile со средой Agda 2.6.4: база `agda/agda:2.6.4` со стандартной библиотекой, проверка `agda Trivortex.agda` при сборке образа, запуск по умолчанию.

---

<div align="center">

**[⬆ Back to top](#-docker--agda--pinned-toolchain-image)** ·
**[Repository root](../../README.md)**

*Part of [wild8highlander/Trivortex](https://github.com/wild8highlander/Trivortex) · Licensed under [IPL-RP-1.0](https://github.com/wild8highlander/Trivortex/blob/main/LICENSE.md) — All Rights Reserved*

</div>

## Toolchain pin

| Pin | Value |
|---|---|
| Toolchain | Agda 2.6.4 |
| Base image | `agda/agda:2.6.4` (stdlib preinstalled) |
| Build-time check | `agda Trivortex.agda` (interface file cleaned after the check) |
| Entrypoint | `agda Trivortex.agda && echo 'Agda check OK — constructive module verified'` |
| Pinned by | [`Dockerfile`](Dockerfile) |
| Built by | [`docker.yml`](../../../.github/workflows/docker.yml) |
| Status | **landed** — M2 (v1.1): [`Trivortex.agda`](../../agda/Trivortex.agda) type-checks, the constructive C3 rotation lattice (`rot³ ≡ id`) is proven — see the [Agda roadmap](../../agda/README.md) |

## What this image guarantees

- the same toolchain version on a laptop, in CI and on a contributor's machine —
  byte-for-byte at the toolchain level, so a proof that compiles here compiles
  everywhere;
- the verification sources are copied at build time and **type-checked during
  the build**; `docker run` executes the same `agda` check CI would, ending in
  an explicit "Agda check OK" echo;
- no floating-point drift question: the M2 artifacts for this
  toolchain are exact-arithmetic or proof objects, not simulations.

## Honest status

**The pin is real and the artifact has landed.** The image type-checks
[`Trivortex.agda`](../../agda/Trivortex.agda) — the constructive angle
arithmetic behind the M2 milestone — and a green `docker run` is the same
check the Agda job of
[`verification-ports.yml`](../../../.github/workflows/verification-ports.yml)
performs (non-blocking until the three-green-days flip). The precise scope of
what is proven constructively is stated in the
[Agda roadmap](../../agda/README.md); quote results from there, never from
this pin table alone.
