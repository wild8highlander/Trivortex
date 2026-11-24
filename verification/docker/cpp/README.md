# 🐳 docker · C++ — Pinned Toolchain Image

> **Navigation:** [`verification`](../../README.md) › [`docker`](../README.md) › **`cpp`**

![Type](https://img.shields.io/badge/Type-Dockerfile-2496ED?style=flat-square&logo=docker&logoColor=white) ![Toolchain](https://img.shields.io/badge/GCC-13-informational?style=flat-square&logo=c&logoColor=white) ![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)

The **Dockerfile pinning the C++ (GCC 13, C++17) environment** for this framework layer. The image uses the official `gcc` base, adds CMake and make, configures and builds the Release ladder at image build time, and defaults to running the CTest guard plus the benchmark laboratory — so `docker run` reproduces exactly what CI runs, byte-for-byte at toolchain level.

## 📂 Contents — What Lives Here

| File | Size | Description |
|---|---|---|
| [`Dockerfile`](Dockerfile) | 694 B | GCC 13 environment (`gcc:13`) + CMake — source copy + Release build acceptance check + `ctest`/lab entrypoint |

## ▶️ How to Run

```bash
# build exactly as CI does — the context is verification/ (the COPY paths):
cd verification
docker build -t rp-cpp -f docker/cpp/Dockerfile .
docker run --rm rp-cpp
```

The build-time `RUN` executes `cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j"$(nproc)"` — the M3 benchmark ladder compiles at `-O2` (registered in [`CMakeLists.txt`](../../cpp/CMakeLists.txt), `CMAKE_CXX_STANDARD 17`).

## 🔗 Cross-References

- [Docker layer](../README.md)
- [Language layer](../../cpp/README.md)

## 🇷🇺 Краткое резюме (Russian Summary)

Dockerfile со средой C++ (GCC 13, стандарт C++17): база `gcc:13` + CMake, Release-сборка при сборке образа, по умолчанию — `ctest` плюс лаборатория на пресете `quick`.

---

<div align="center">

**[⬆ Back to top](#-docker--c--pinned-toolchain-image)** ·
**[Repository root](../../README.md)**

*Part of [wild8highlander/Trivortex](https://github.com/wild8highlander/Trivortex) · Licensed under [IPL-RP-1.0](https://github.com/wild8highlander/Trivortex/blob/main/LICENSE.md) — All Rights Reserved*

</div>

## Toolchain pin

| Pin | Value |
|---|---|
| Toolchain | GCC 13, C++17 (`CMAKE_CXX_STANDARD 17`, extensions off) |
| Base image | `gcc:13` (+ `cmake`, `make` from apt) |
| Build-time check | CMake configure + build, `-DCMAKE_BUILD_TYPE=Release`, all cores |
| Entrypoint | `ctest --test-dir build --output-on-failure && ./build/trivortex-lab --preset quick --no-menu --out-dir outputs/cpp` |
| Pinned by | [`Dockerfile`](Dockerfile) |
| Built by | [`docker.yml`](../../../.github/workflows/docker.yml) |
| Status | **landed** — M3 (v1.1): the CMake/CTest port passes its guard and commits [`protocol_quick.json`](../../cpp/protocol_quick.json) with the `-O2` benchmark (`benchmark_rhs_per_s`) — see the [C++ roadmap](../../cpp/README.md) |

## What this image guarantees

- the same toolchain version on a laptop, in CI and on a contributor's machine —
  byte-for-byte at the toolchain level, so a proof that compiles here compiles
  everywhere;
- the port is copied at build time and **built during the build**; `docker run`
  executes the CTest pinned-reference guard and then the interactive laboratory —
  the same entrypoint CI would;
- the benchmark number (`benchmark_rhs_per_s`, ~1.7e7 rhs/s in the committed
  protocol) is machine-dependent — the M6 "benchmark board" track pins rust vs
  c++ side by side on the same machine before it may be quoted as a comparison.

## Honest status

**The pin is real and the artifact has landed.** The image compiles the M3
port (21 CTest guards) and commits the protocol of a real run, machine-pinned
against the Python ladder by the
[pytest guard](../../tests/README.md). A green `docker run` mirrors the C++
job of [`verification-ports.yml`](../../../.github/workflows/verification-ports.yml)
(non-blocking until the three-green-days flip). Scope and benchmark caveats
are stated in the [C++ roadmap](../../cpp/README.md); quote results from
there, never from this pin table alone.
