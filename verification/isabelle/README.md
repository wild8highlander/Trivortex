# Isabelle/HOL Verification — Roadmap

> Formalization / port target for the **TRIVORTEX** document
> (`code/trivortex_core*.py`): Theorem 3.1 (the Lagrange-type rotating
> solution) and the conservation of the Chaplygin-type vortex integrals.
>
> **Status: landed — v1.1 (milestone M2).** The artifact, the
> CI-callable check and the bilingual documentation live in this
> directory; the acceptance criteria below are checked. Local runs
> need the pinned toolchain (Docker); the repository CI runs the
> port non-blocking (see [`verification/README.md`](../README.md) §7).

---

## Why Isabelle/HOL

Isabelle/HOL offers the strongest automation (`smt`,
`auto`, `presburger`) of the LCF family, which suits the invariant
conservation checks: the drift statements are polynomial/rational
bounds once the closed form is substituted, and SMT can discharge most
of them. The plan is a single `Trivortex.thy` session mirroring the
Coq artifact statement-for-statement, so the two provers cross-check
each other.

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

- [x] The three objects above are expressed in Isabelle/HOL with no hidden
      assumptions beyond the axioms listed in the artifact header
      (`verification/isabelle/Trivortex.thy` (+ optional `Trivortex_SMT.thy`));
- [x] A CI-callable check: `isabelle build -D verification/isabelle` — builds the HOL session in the pinned Isabelle2024 image (workflow `verification-ports.yml`, job *formal-isabelle*);
- [x] The artifact header carries SPDX + copyright lines (REUSE.toml)
      and a provenance note pointing at the commit of `verify.py` it
      mirrors (557bff8, the M0 release);
- [x] `verification/README.md` status table flips this row to
      *landed (v1.1)* with a link.

## Build recipe

```bash
# pinned toolchain (see docker/isabelle/Dockerfile)
docker build -t trivortex-isabelle docker/isabelle
docker run --rm -v "$PWD":/work -w /work trivortex-isabelle \
    isabelle build -D verification/isabelle   # lands with milestone M1
```

The Dockerfile in [`docker/isabelle/Dockerfile`](../docker/isabelle/Dockerfile)
pins the toolchain; the repository CI never requires this build to pass
until milestone M1 lands.

## Toolchain pin and milestones

| Pin | Value |
|---|---|
| Toolchain | Isabelle/HOL 2024 |
| Docker pin | [`docker/isabelle/Dockerfile`](../docker/isabelle/Dockerfile) |
| Planned artifact | `verification/isabelle/Trivortex.thy` |
| Milestone | **M2** of the staged plan |
| CI status | non-blocking job in `verification-ports.yml` |

## What landed (v1.1)

1. the statement layer with proven choreography and periodicity lemmas, the Chaplygin shape and the exact equilateral anchors;
2. the registered tolerance bands as a machine-checked record with decidable ordering;
3. the optional SMT-discharged numeric bounds (`Trivortex_SMT.thy`) — kept out of the default build until Z3 ships in the toolchain image (documented in `ROOT`).

The artifact header lists the axiom footprint; the JSON protocol of a
real run is committed next to the artifact (`protocol_quick.json`) where
the port is numerical. The bilingual overview lives in
[README_RU.md](README_RU.md).
