# 🐳 docker · Isabelle-HOL — Pinned Toolchain Image

> **Navigation:** [`verification`](../../README.md) › [`docker`](../README.md) › **`isabelle`**

![Type](https://img.shields.io/badge/Type-Dockerfile-2496ED?style=flat-square&logo=docker&logoColor=white) ![Toolchain](https://img.shields.io/badge/Isabelle--HOL-2024-informational?style=flat-square) ![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)

The **Dockerfile pinning the Isabelle-HOL (2024) environment** for this framework layer. The image uses the official `makarius/isabelle` base, copies the session sources, builds the HOL session at image build time, and defaults to `isabelle build -D .` — so `docker run` reproduces exactly what CI runs, byte-for-byte at toolchain level.

## 📂 Contents — What Lives Here

| File | Size | Description |
|---|---|---|
| [`Dockerfile`](Dockerfile) | 514 B | Isabelle-HOL 2024 environment (`makarius/isabelle:Isabelle2024`) — source copy + session build + verification entrypoint |

## ▶️ How to Run

```bash
# build exactly as CI does — the context is verification/ (the COPY paths):
cd verification
docker build -t rp-isabelle -f docker/isabelle/Dockerfile .
docker run --rm rp-isabelle
```

The build-time `RUN` executes `isabelle build -D .` — a broken session fails the image build. The optional SMT session (`Trivortex_SMT.thy`) stays disabled until Z3 ships in the pinned image (the M4 track).

## 🔗 Cross-References

- [Docker layer](../README.md)
- [Language layer](../../isabelle/README.md)

## 🇷🇺 Краткое резюме (Russian Summary)

Dockerfile со средой Isabelle-HOL 2024: база `makarius/isabelle:Isabelle2024`, сборка сессии при сборке образа, `isabelle build -D .` по умолчанию; SMT-сессия опциональна до появления Z3 в образе.

---

<div align="center">

**[⬆ Back to top](#-docker--isabelle-hol--pinned-toolchain-image)** ·
**[Repository root](../../README.md)**

*Part of [wild8highlander/Trivortex](https://github.com/wild8highlander/Trivortex) · Licensed under [IPL-RP-1.0](https://github.com/wild8highlander/Trivortex/blob/main/LICENSE.md) — All Rights Reserved*

</div>

## Toolchain pin

| Pin | Value |
|---|---|
| Toolchain | Isabelle/HOL 2024 |
| Base image | `makarius/isabelle:Isabelle2024` |
| Build-time check | `isabelle build -D .` (the default `ROOT` session) |
| Entrypoint | `isabelle build -D .` |
| Pinned by | [`Dockerfile`](Dockerfile) |
| Built by | [`docker.yml`](../../../.github/workflows/docker.yml) |
| Status | **landed** — M2 (v1.1): [`Trivortex.thy`](../../isabelle/Trivortex.thy) HOL-proven; [`Trivortex_SMT.thy`](../../isabelle/Trivortex_SMT.thy) stays an optional session until Z3 is in the image — see the [Isabelle hub](../../isabelle/README.md) |

## What this image guarantees

- the same toolchain version on a laptop, in CI and on a contributor's machine —
  byte-for-byte at the toolchain level, so a proof that compiles here compiles
  everywhere;
- the verification sources are copied at build time and the **HOL session builds
  during the build**; `docker run` re-executes the same acceptance check CI
  would;
- no floating-point drift question: the M2 artifacts for this
  toolchain are exact-arithmetic or proof objects, not simulations.

## Honest status

**The pin is real and the artifact has landed — with one declared gap.** The
HOL session of [`Trivortex.thy`](../../isabelle/Trivortex.thy) is proven and
builds green; the SMT-discharged bounds of
[`Trivortex_SMT.thy`](../../isabelle/Trivortex_SMT.thy) remain an *optional*
session because Z3 is not in the pinned image — that move is pre-registered
as M4 ("Isabelle SMT online"). See the [milestone table](../README.md) and the
[Isabelle/HOL roadmap](../../isabelle/README.md); quote results from there,
never from this pin table alone.
