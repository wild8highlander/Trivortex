# C++ Verification — Roadmap

> Formalization / port target for the **TRIVORTEX** document
> (`code/trivortex_core*.py`): Theorem 3.1 (the Lagrange-type rotating
> solution) and the conservation of the Chaplygin-type vortex integrals.
>
> **Status: landed — v1.1 (milestone M3).** The artifact, the
> CI-callable check and the bilingual documentation live in this
> directory; the acceptance criteria below are checked. Local runs
> need the pinned toolchain (Docker); the repository CI runs the
> port non-blocking (see [`verification/README.md`](../README.md) §7).

---

## Why C++

C++ keeps the legacy toolchain of computational physics
honest: the port is a single translation unit implementing the same
four checks with `std::sin`/`std::cos` and a fixed-order RK4, driven by
CMake/CTest. Its role is benchmarking (the same ladder compiled with
`-O2 -march=native` runs orders of magnitude faster than Python) and
serving as the reference for any future GPU port of the vortex
dynamics.

## Scope of the port

The port fixes exactly three objects, so that every language proves or
computes the *same* statements and the results stay comparable:

1. **Theorem 3.1 (closed form).**
   `r_k(t) = sqrt(C_Ch) * (1 + eps*cos(omega*t + 2*pi*k/3))`,
   `theta_k(t) = omega*t + 2*pi*k/3`,
   `omega = (2*pi/T)*exp(C_Ch/pi)`, `eps = 1/(exp(C_Ch/pi) - 1)`;
   properties to establish: exact `2*pi/3` angular separation (equilateral
   choreography) and periodicity `r_k(t + 2*pi/omega) = r_k(t)`.
2. **Chaplygin integral.** The combination
   `C_Ch = r^2*(theta_dot - q*A_theta)` with `A_theta = 1/r`, following the
   definition fixed in Section 6 of the core document, together with its
   recorded endpoint-drift diagnostic over `[0, 100*T]`.
3. **Vortex integrals.** `H`, `P = sum(Gamma*x)`, `Q = sum(Gamma*y)`,
   `I = sum(Gamma*|r|^2)` along numerically integrated Kirchhoff
   trajectories — conserved to the tolerance bands of
   [`verification/tests/`](../tests/README.md).

## Acceptance criteria

- [x] The three objects above are expressed in C++ (CMake) with no hidden
      assumptions beyond the axioms listed in the artifact header
      (`verification/cpp/` (CMake/CTest port + the `-O2` benchmark ladder));
- [x] A CI-callable check: `cmake -S verification/cpp -B build && ctest --test-dir build` — runs the pinned-reference guard (21 assertions) and the benchmark ladder (workflow `verification-ports.yml`, job *cpp-ctest*);
- [x] The artifact header carries SPDX + copyright lines (REUSE.toml)
      and a provenance note pointing at the commit of `verify.py` it
      mirrors (557bff8, the M0 release);
- [x] `verification/README.md` status table flips this row to
      *landed (v1.1)* with a link.

## Build recipe

```bash
# pinned toolchain (see docker/cpp/Dockerfile)
docker build -t trivortex-cpp docker/cpp
docker run --rm -v "$PWD":/work -w /work trivortex-cpp bash -c \
    "cmake -S verification/cpp -B build && cmake --build build && ctest --test-dir build"   # lands with M1
```

The Dockerfile in [`docker/cpp/Dockerfile`](../docker/cpp/Dockerfile)
pins the toolchain; the repository CI never requires this build to pass
until milestone M1 lands.

## Toolchain pin and milestones

| Pin | Value |
|---|---|
| Toolchain | C++ 23 (GCC 13) |
| Docker pin | [`docker/cpp/Dockerfile`](../docker/cpp/Dockerfile) |
| Planned artifact | `verification/cpp/verify.cpp` |
| Milestone | **M3** of the staged plan |
| CI status | non-blocking job in `verification-ports.yml` |

## What landed (v1.1)

1. the numeric twin compiled at `-O2` with the CTest guard of pinned reference values, reproducing the Python ladder's verdicts;
2. the `-O2` benchmark (RK4 right-hand-side evaluations per second) recorded in every JSON protocol (`benchmark_rhs_per_s`);
3. the interactive bilingual laboratory (`trivortex-lab`): presets, custom parameters, convergence analysis, JSON/CSV/SVG export.

The artifact header lists the axiom footprint; the JSON protocol of a
real run is committed next to the artifact (`protocol_quick.json`) where
the port is numerical. The bilingual overview lives in
[README_RU.md](README_RU.md).
