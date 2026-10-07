# Rust Verification — Roadmap

> Formalization / port target for the **TRIVORTEX** document
> (`code/trivortex_core*.py`): Theorem 3.1 (the Lagrange-type rotating
> solution) and the conservation of the Chaplygin-type vortex integrals.
>
> **Status: planned — skeleton.** This directory currently holds the plan
> and the build recipe; the artifacts appear with milestone M1 (see
> [`verification/README.md`](../README.md) for the ladder).

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

- [ ] The three objects above are expressed in Rust with no hidden
      assumptions beyond the axioms listed in the artifact header;
- [ ] A CI-callable check reproduces the reference numbers of the Python
      ladder (V1-V4) to the documented tolerances;
- [ ] The artifact header carries SPDX + copyright lines (see REUSE.toml)
      and a provenance note pointing at the commit of `verify.py` it
      mirrors;
- [ ] `verification/README.md` status table flips this row from
      *planned* to *in review / done* with a link.

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
| CI status | not required to pass until the milestone lands |

## What lands with milestone M1

1. the numeric twin of the ladder (f64, no_std-friendly core) — the three fixed objects (closed form, Chaplygin integral,
   vortex integrals) expressed natively;
2. a CI-callable check that reproduces the Python ladder's reference numbers
   to the documented tolerances (or, for the provers, checks the statements
   with the axioms listed in the artifact header);
3. the acceptance-criteria checklist at the top of this file flipped to done,
   with the artifact header carrying SPDX + copyright lines and a provenance
   note pointing at the commit of `verify.py` it mirrors.

Until then, this directory states the plan and holds nothing else — the
repository's honesty rule forbids quoting a plan as a verification.
