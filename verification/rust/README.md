# Rust Verification — Roadmap

> Formalization / port target for the **TRIVORTEX** document
> (`code/trivortex_core*.py`): Theorem 3.1 (the Lagrange-type rotating
> solution) and the conservation of the Chaplygin-type vortex integrals.
>
> **Status: landed — v1.1 (milestone M1).** The artifact, the
> CI-callable check and the bilingual documentation live in this
> directory; the acceptance criteria below are checked. Local runs
> need the pinned toolchain (Docker); the repository CI runs the
> port non-blocking until it stays green for three consecutive days
> (see [`verification/README.md`](../README.md) §7).

---

## Why Rust

Rust is the numerical port target: the Kirchhoff
right-hand side and the RK4 stepper of `verify.py` translate line for
line into a small crate, and `cargo test` gives the CI a second,
independent floating-point implementation. Divergences between the
Python and Rust ladders are the cheapest early-warning system for
platform-specific floating-point surprises (x87 vs SSE, fused
multiply-add contraction, libm differences).

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

- [x] The three objects above are expressed in Rust with no hidden
      assumptions beyond the axioms listed in the artifact header
      (`verification/rust/` crate (the twin core lives in `src/verify.rs`));
- [x] A CI-callable check: `cargo test --release --manifest-path verification/rust/Cargo.toml` — runs the pinned-reference guard (14 tests) and the quick ladder (workflow `verification-ports.yml`, job *rust-numeric-twin*);
- [x] The artifact header carries SPDX + copyright lines (REUSE.toml)
      and a provenance note pointing at the commit of `verify.py` it
      mirrors (557bff8, the M0 release);
- [x] `verification/README.md` status table flips this row to
      *landed (v1.1)* with a link.

## Build recipe

```bash
# pinned toolchain (see docker/rust/Dockerfile)
docker build -t trivortex-rust docker/rust
docker run --rm -v "$PWD":/work -w /work trivortex-rust \
    cargo test --manifest-path verification/rust/Cargo.toml   # lands with M1
```

The Dockerfile in [`docker/rust/Dockerfile`](../docker/rust/Dockerfile)
pins the toolchain; the repository CI never requires this build to pass
until milestone M1 lands.

## Toolchain pin and milestones

| Pin | Value |
|---|---|
| Toolchain | Rust 1.77 |
| Docker pin | [`docker/rust/Dockerfile`](../docker/rust/Dockerfile) |
| Planned artifact | `verification/rust/verify.rs` |
| Milestone | **M1** of the staged plan |
| CI status | non-blocking job in `verification-ports.yml` |

## What landed (v1.1)

1. the numeric twin of the ladder (f64, dependency-free core) — the three fixed objects expressed natively, with the quick preset reproducing the Python reference numbers inside the registered bands;
2. the interactive bilingual laboratory (`trivortex-lab`): presets, custom parameters, convergence analysis, JSON protocol, CSV data and native SVG figures;
3. the committed reference protocol `protocol_quick.json` of a real run.

The artifact header lists the axiom footprint; the JSON protocol of a
real run is committed next to the artifact (`protocol_quick.json`) where
the port is numerical. The bilingual overview lives in
[README_RU.md](README_RU.md).
