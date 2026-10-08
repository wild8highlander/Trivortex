# The C++ sources — the compiled benchmark ladder (M3)

The C++17 implementation of the V1–V4 verification ladder — the
compiled, throughput-oriented port of milestone **M3**, with an
exact-arithmetic residual split that separates float artifacts from
mathematics.

## The files

| file | role |
|------|------|
| [`verify.hpp`](verify.hpp) | the core header: the closed form, the Chaplygin combination, the Kirchhoff RHS, the RK4 stepper, the registered tolerance bands |
| [`verify.cpp`](verify.cpp) | the ladder implementation: V1–V4 with the recorded residuals and the JSON protocol payload |
| [`tests.cpp`](tests.cpp) | the 21-guard test battery that re-derives the reference numbers independently of the ladder code paths |
| [`main.cpp`](main.cpp) | the CLI entry point: preset selection, protocol output, the benchmark mode |

## What this port certifies

- **throughput**: ≈ 1.7e7 RHS evaluations per second — the benchmark
  board number the roadmap pins against the Rust port;
- **the exact-residual split**: where the statement is algebraic, the
  ladder separates the float residual from the exact value (the
  ℚ(√3)-style evaluation happens on the Haskell side; C++ quantifies
  the floating-point envelope around it);
- **the same V1–V4 registers** with the same recorded residuals and
  tolerance bands as the Python ladder — no port-specific tolerances.

## Build and run

The port builds inside its pinned Docker toolchain
([`../../docker/cpp/`](../../docker/cpp/)) to keep the compiler and
stdlib identical across machines:

```bash
# via the pinned toolchain (recommended)
docker build -t trivortex-cpp ../../docker/cpp
docker run --rm -v "$PWD/../../..":/repo trivortex-cpp /verification/cpp

# or locally with any C++17 compiler
g++ -O2 -std=c++17 -I src src/*.cpp -o trivortex_cpp && ./trivortex_cpp
```

The run prints the ladder report and writes the JSON protocol. The
committed protocol values the pytest guard pins against
([`../../tests/test_ports.py`](../../tests/test_ports.py)) were produced
by this code — a re-run must reproduce them to the printed precision.

## The port contract

This directory shares **no code** with the Python document or ladder;
only the committed numbers bind the implementations. Acceptance
criteria, tolerance-band rationale and the promotion-to-blocking policy
live in the [verification README](../README.md).
