# 🐳 docker · Coq/Rocq — Pinned Toolchain Image

> **Navigation:** [`verification`](../../README.md) › [`docker`](../README.md) › **`coq`**

![Type](https://img.shields.io/badge/Type-Dockerfile-2496ED?style=flat-square&logo=docker&logoColor=white) ![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)

The **Dockerfile pinning the Coq/Rocq (8.18) environment** for this framework layer. The image installs the toolchain (coq_makefile or per-file coqc as the in-container flow), copies the verification sources, and defaults to running the Coq/Rocq verification — so `docker run` reproduces exactly what CI runs, byte-for-byte at toolchain level.

## 📂 Contents — What Lives Here

| File | Size | Description |
|---|---|---|
| [`Dockerfile`](Dockerfile) | 179 B | Coq/Rocq 8.18 environment — install + source copy + verification entrypoint |

## ▶️ How to Run

```bash
docker build -t rp-coq verification/docker/coq
docker run --rm rp-coq
```

## 🔗 Cross-References

- [Docker layer](../README.md)
- [Language layer](../../coq/README.md)

## 🇷🇺 Краткое резюме (Russian Summary)

Dockerfile со средой Coq/Rocq 8.18: установка тулчейна + запуск верификации по умолчанию.

---

<div align="center">

**[⬆ Back to top](#-docker--coqrocq--pinned-toolchain-image)** ·
**[Repository root](../../README.md)**

*Part of [wild8highlander/research-papers](https://github.com/wild8highlander/research-papers) · Licensed under [IPL-RP-1.0](https://github.com/wild8highlander/research-papers/blob/main/LICENSE.md) — All Rights Reserved*

</div>

## Toolchain pin

| Pin | Value |
|---|---|
| Toolchain | Coq / Rocq 8.18 |
| Base image | `coqorg/coq:8.18.0` |
| Entrypoint | per-file build (the in-container flow) |
| Pinned by | [`Dockerfile`](Dockerfile) |
| Built by | [`docker.yml`](../../../.github/workflows/docker.yml) |
| Status | roadmap pin — the artifact lands with milestone **M1** |

## What this image guarantees

- the same toolchain version on a laptop, in CI and on a contributor's machine —
  byte-for-byte at the toolchain level, so a proof that compiles here compiles
  everywhere;
- the verification sources are copied at build time; `docker run` executes the
  same entrypoint CI would;
- no floating-point drift question: the M1 artifacts for this
  toolchain are exact-arithmetic or proof objects, not simulations.

## Honest status

**This is a pinned plan, not a result.** The image builds and the toolchain
runs, but the Coq / Rocq artifact for Theorem 3.1 has not landed yet — see the
[milestone table](../README.md) and the
[Coq / Rocq roadmap](../../coq/README.md). Nothing in this directory should be quoted as a
verification.
