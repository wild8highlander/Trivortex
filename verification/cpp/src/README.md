<!-- markdownlint-disable-file MD041 -->
<div align="center">

# 🧱 The C++ Sources — the Compiled Benchmark Ladder (M3)

![C++17](https://img.shields.io/badge/C%2B%2B-17-00599C?style=flat-square&logo=cplusplus&logoColor=white)
![Type](https://img.shields.io/badge/Type-source%20map-2496ED?style=flat-square)
![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)

</div>

> **Navigation:** [`verification`](../../README.md) › [`cpp`](../README.md) › **`src`**

The C++17 implementation of the V1–V4 verification ladder — the
compiled, throughput-oriented port of milestone **M3**, with an
exact-arithmetic residual split that separates float artifacts from
mathematics.

## 📂 The Files

| File | Size | Lines | Role |
|---|---|---|---|
| [`verify.hpp`](verify.hpp) | 7 098 B | 196 | the core header: the closed form, the Chaplygin combination, the Kirchhoff RHS, the RK4 stepper, the registered tolerance bands, the JSON value tree |
| [`verify.cpp`](verify.cpp) | 29 363 B | 751 | the ladder implementation: V1–V4 with the recorded residuals and the JSON protocol payload |
| [`tests.cpp`](tests.cpp) | 5 366 B | 124 | the CTest guard battery that re-derives the reference numbers independently of the ladder code paths |
| [`main.cpp`](main.cpp) | 18 964 B | 400 | the CLI entry point: preset selection, protocol output, the benchmark mode, the bilingual (EN/RU) menu |

## ✅ What This Port Certifies

- **throughput**: ≈ 1.7e7 RHS evaluations per second (`benchmark_rhs_per_s`
  = 16734651.19 in the committed [`protocol_quick.json`](../protocol_quick.json)) —
  the benchmark board number the roadmap pins against the Rust port;
- **the exact-residual split**: where the statement is algebraic, the
  ladder separates the float residual from the exact value (the
  ℚ(√3)-style evaluation happens on the Haskell side; C++ quantifies
  the floating-point envelope around it);
- **the same V1–V4 registers** with the same recorded residuals and
  tolerance bands as the Python ladder — no port-specific tolerances.

## 🚀 Build and Run

The port builds inside its pinned Docker toolchain
([`../../docker/cpp/`](../../docker/cpp/), image `gcc:13`) to keep the
compiler and stdlib identical across machines:

```bash
# via the pinned toolchain (recommended)
docker build -t trivortex-cpp verification/docker/cpp
docker run --rm trivortex-cpp          # CTest guard + quick ladder in CI mode

# or locally with any C++17 compiler
g++ -O2 -std=c++17 -I src src/*.cpp -o trivortex_cpp && ./trivortex_cpp
```

The run prints the ladder report and writes the JSON protocol. The
committed protocol values the pytest guard pins against
([`../../tests/test_ports.py`](../../tests/test_ports.py)) were produced
by this code — a re-run must reproduce them to the printed precision.

## 🔗 The Port Contract

This directory shares **no code** with the Python document or ladder;
only the committed numbers bind the implementations. Acceptance
criteria, tolerance-band rationale and the promotion-to-blocking policy
live in the [verification README](../README.md); the statement layer the
numbers must match is formalized in the
[Lean 4 hub](../../lean4/README.md).

## 🇷🇺 Краткое резюме (Russian Summary)

- `verify.hpp`/`verify.cpp` — ядро-двойник лестницы V1–V4: те же формулы
  и допуски, что в `verify.py`, плюс JSON-дерево значений;
- `tests.cpp` — CTest-защита: 25 утверждений `expect_*`, опорные значения
  пересчитываются независимо от кодовых путей лестницы («pinned, not assumed»);
- `main.cpp` — интерактивная двуязычная лаборатория `trivortex-lab`:
  пресеты, свои параметры, сходимость, экспорт JSON/CSV/SVG;
- сертифицируется пропускная способность ≈ 1.7·10⁷ вычислений правой части
  RK4 в секунду (`benchmark_rhs_per_s`) — цифра-эталон против порта Rust;
- никаких порто-специфичных допусков: те же регистры V1–V4 и те же полосы, что у Python-лестницы; код с Python-документом не разделяется.

---

<div align="center">

**[⬆ Back to top](#-the-c-sources--the-compiled-benchmark-ladder-m3)** ·
**[Repository root](../../../README.md)**

*Part of [wild8highlander/Trivortex](https://github.com/wild8highlander/Trivortex) · Licensed under [IPL-RP-1.0](https://github.com/wild8highlander/Trivortex/blob/main/LICENSE.md) — All Rights Reserved*

</div>
