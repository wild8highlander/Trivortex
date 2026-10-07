# 🐳 verification · docker — Pinned Toolchain Images (×7)

> **Navigation:** [`verification`](../README.md) › **`docker`**

![Type](https://img.shields.io/badge/Type-Docker-2496ED?style=flat-square&logo=docker&logoColor=white) ![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)

One **Docker image per extended toolchain** — seven subfolders, each with its own `Dockerfile` pinning the exact environment a formal or compiled port needs. This is how a reviewer reproduces a result without installing Lean, Coq, Isabelle, Agda or the compiled toolchains locally: pull the base image, build the folder, run the verification inside the container.

The images are wired into `docker.yml` (build) and referenced by the verification workflows; each `Dockerfile` is minimal — official base image, toolchain install, the verification source copied in, and the TRIVORTEX port run as the default command once its milestone lands (M1–M3; see the roadmap in the framework root). Image sizes are dominated by the proof assistants (Isabelle and Lean being the largest); the compiled-language images are small.

## 📂 Contents — What Lives Here

| File | Size | Description |
|---|---|---|
| [`agda/`](agda/) | — | Agda 2.6 with the standard library preinstalled |
| [`coq/`](coq/) | — | Coq/Rocq 8.18 with the standard Reals stack |
| [`cpp/`](cpp/) | — | GCC/Clang + CMake for the C++17 ports |
| [`haskell/`](haskell/) | — | GHC 9.4 + Cabal for the Haskell project |
| [`isabelle/`](isabelle/) | — | Isabelle-HOL 2024 session environment |
| [`lean4/`](lean4/) | — | Lean 4 + elan/lake, toolchain pinned by lean-toolchain |
| [`rust/`](rust/) | — | Rust stable (1.75+) for the Cargo crate |

## 🗂 Directory Layout

```text
docker/
├── agda/   # 2 files
│   ├── Dockerfile
│   └── README.md  (this file)
├── coq/   # 2 files
│   ├── Dockerfile
│   └── README.md  (this file)
├── cpp/   # 2 files
│   ├── Dockerfile
│   └── README.md  (this file)
├── haskell/   # 2 files
│   ├── Dockerfile
│   └── README.md  (this file)
├── isabelle/   # 2 files
│   ├── Dockerfile
│   └── README.md  (this file)
├── lean4/   # 2 files
│   ├── Dockerfile
│   └── README.md  (this file)
├── rust/   # 2 files
│   ├── Dockerfile
│   └── README.md  (this file)
└── README.md  (this file)
```

## ▶️ How to Run

```bash
# Example — build and run the Lean image:
docker build -t rp-lean verification/docker/lean4
docker run --rm rp-lean
# Or run the whole matrix from the root:
make docker-up
```

## 🔗 Cross-References

- [Root README — Quick Start](../../README.md)
- [CI workflow docker.yml](../../.github/workflows/README.md)

## 🇷🇺 Краткое резюме (Russian Summary)

**verification/docker/** — семь Docker-образов, по одному на расширенный тулчейн (Lean 4, Coq, Isabelle, Agda, C++, Rust, Haskell); в каждом Dockerfile зафиксирована среда, команда по умолчанию — запуск верификации. Сборка — docker.yml / make docker-up.

---

<div align="center">

**[⬆ Back to top](#-verification--docker--pinned-toolchain-images-7)** ·
**[Repository root](../README.md)**

*Part of [wild8highlander/research-papers](https://github.com/wild8highlander/research-papers) · Licensed under [IPL-RP-1.0](https://github.com/wild8highlander/research-papers/blob/main/LICENSE.md) — All Rights Reserved*

</div>
