# 🐳 docker · Coq/Rocq — Pinned Toolchain Image

> **Navigation:** [`verification`](../../README.md) › [`docker`](../README.md) › **`coq`**

![Type](https://img.shields.io/badge/Type-Dockerfile-2496ED?style=flat-square&logo=docker&logoColor=white) ![Toolchain](https://img.shields.io/badge/Coq%2FRocq-8.18-informational?style=flat-square) ![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)

The **Dockerfile pinning the Coq/Rocq (8.18) environment** for this framework layer. The image uses the official `coqorg/coq` base, copies the verification sources, compiles the statement layer at image build time (and cleans the build products), and defaults to running `coqc Trivortex.v` — so `docker run` reproduces exactly what CI runs, byte-for-byte at toolchain level.

## 📂 Contents — What Lives Here

| File | Size | Description |
|---|---|---|
| [`Dockerfile`](Dockerfile) | 629 B | Coq/Rocq 8.18 environment (`coqorg/coq:8.18-ocaml-4.14`) — source copy + `coqc` acceptance check + verification entrypoint |

## ▶️ How to Run

```bash
# build exactly as CI does — the context is verification/ (the COPY paths):
cd verification
docker build -t rp-coq -f docker/coq/Dockerfile .
docker run --rm rp-coq
```

The build-time `RUN` executes `coqc Trivortex.v` and removes the `.vo/.vos/.vok/.glob/.aux` products, so the image carries the sources, not stale artifacts.

## 🔗 Cross-References

- [Docker layer](../README.md)
- [Language layer](../../coq/README.md)

## 🇷🇺 Краткое резюме (Russian Summary)

Dockerfile со средой Coq/Rocq 8.18: база `coqorg/coq:8.18-ocaml-4.14`, компиляция `Trivortex.v` при сборке образа, запуск `coqc` по умолчанию.

---

<div align="center">

**[⬆ Back to top](#-docker--coqrocq--pinned-toolchain-image)** ·
**[Repository root](../../README.md)**

*Part of [wild8highlander/Trivortex](https://github.com/wild8highlander/Trivortex) · Licensed under [IPL-RP-1.0](https://github.com/wild8highlander/Trivortex/blob/main/LICENSE.md) — All Rights Reserved*

</div>

## Toolchain pin

| Pin | Value |
|---|---|
| Toolchain | Coq / Rocq 8.18 |
| Base image | `coqorg/coq:8.18-ocaml-4.14` |
| Build-time check | `coqc Trivortex.v` (products cleaned after the check) |
| Entrypoint | `coqc Trivortex.v && echo 'Coq build OK — statement layer verified'` |
| Pinned by | [`Dockerfile`](Dockerfile) |
| Built by | [`docker.yml`](../../../.github/workflows/docker.yml) |
| Status | **landed** — M1 (v1.1): [`Trivortex.v`](../../coq/Trivortex.v) compiles, statement layer proven, zero axioms — see the [Coq hub](../../coq/README.md) |

## What this image guarantees

- the same toolchain version on a laptop, in CI and on a contributor's machine —
  byte-for-byte at the toolchain level, so a proof that compiles here compiles
  everywhere;
- the verification sources are copied at build time and **compiled during the
  build**; `docker run` executes the same `coqc` acceptance check CI would,
  ending in an explicit "Coq build OK" echo;
- no floating-point drift question: the M1 artifacts for this
  toolchain are exact-arithmetic or proof objects, not simulations.

## Honest status

**The pin is real and the artifact has landed.** The image compiles
[`Trivortex.v`](../../coq/Trivortex.v) — the M1 statement layer, proven with a
closed axiom footprint — and a green `docker run` is the same check the Coq
job of [`verification-ports.yml`](../../../.github/workflows/verification-ports.yml)
performs (non-blocking until the three-green-days flip). What the artifact
proves — and what it deliberately does not yet prove (the `I = Γ` derivation
is M5) — is stated in the [Coq / Rocq roadmap](../../coq/README.md); quote
results from there, never from this pin table alone.
