# Coq / Rocq Verification — Roadmap

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

## Why Coq / Rocq

Coq is the natural home for the *statement layer* of
Theorem 3.1: the closed form, the choreography property and the
periodicity lemma are plain real-analysis statements over `R`, well
within reach of the standard library plus `Coquelicot` for elementary
calculus. The goal is not a full mechanization of hydrodynamics — it is
a machine-checked kernel that pins the exact formulas and their
immediate consequences, so that any future refactor of the numerical
code can be diffed against a proven specification.

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

- [x] The three objects above are expressed in Gallina with no hidden
      assumptions beyond the axioms listed in the artifact header
      (`verification/coq/Trivortex.v`);
- [x] A CI-callable check: `coqc verification/coq/Trivortex.v` — compiles the statement layer and prints the closed axiom footprint (workflow `verification-ports.yml`, job *formal-coq*);
- [x] The artifact header carries SPDX + copyright lines (REUSE.toml)
      and a provenance note pointing at the commit of `verify.py` it
      mirrors (557bff8, the M0 release);
- [x] `verification/README.md` status table flips this row to
      *landed (v1.1)* with a link.

## Build recipe

```bash
# pinned toolchain (see docker/coq/Dockerfile)
docker build -t trivortex-coq docker/coq
docker run --rm -v "$PWD":/work -w /work trivortex-coq \
    coqc verification/coq/Trivortex.v   # lands with milestone M1
```

The Dockerfile in [`docker/coq/Dockerfile`](../docker/coq/Dockerfile)
pins the toolchain; the repository CI never requires this build to pass
until milestone M1 lands.

## Toolchain pin and milestones

| Pin | Value |
|---|---|
| Toolchain | Coq / Rocq 8.18 |
| Docker pin | [`docker/coq/Dockerfile`](../docker/coq/Dockerfile) |
| Planned artifact | `verification/coq/Trivortex.v` |
| Milestone | **M1** of the staged plan |
| CI status | non-blocking job in `verification-ports.yml` |

## What landed (v1.1)

1. the statement layer of Theorem 3.1 in Gallina — the closed form, the Chaplygin integral and the vortex integrals expressed natively, with the choreography and periodicity lemmas **proven** (zero `Axiom`s; `Print Assumptions` reports only the standard-library classical base);
2. the exact anchor values of the equilateral reference state proven: H = 0, P = 0, Q = 0, I = Γ;
3. the registered tolerance bands as a machine-checked record.

The artifact header lists the axiom footprint; the JSON protocol of a
real run is committed next to the artifact (`protocol_quick.json`) where
the port is numerical. The bilingual overview lives in
[README_RU.md](README_RU.md).
