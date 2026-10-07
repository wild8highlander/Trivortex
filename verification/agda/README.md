# Agda Verification — Roadmap

> Formalization / port target for the **TRIVORTEX** document
> (`code/trivortex_core*.py`): Theorem 3.1 (the Lagrange-type rotating
> solution) and the conservation of the Chaplygin-type vortex integrals.
>
> **Status: planned — skeleton.** This directory currently holds the plan
> and the build recipe; the artifacts appear with milestone M1 (see
> [`verification/README.md`](../README.md) for the ladder).

---

## Why Agda

Agda serves as the *independent* proof assistant in the
matrix: its constructive background makes it a good stress test for
whether the statement layer of Theorem 3.1 is phrased without
accidental classical shortcuts. The port targets the choreography
property (constructive angle arithmetic mod 2*pi/3) and the periodicity
lemma; the analytic-frequency identity follows from the standard
library's real-number machinery.

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

- [ ] The three objects above are expressed in Agda (standard library) with no hidden
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
# pinned toolchain (see docker/agda/Dockerfile)
docker build -t trivortex-agda docker/agda
docker run --rm -v "$PWD":/work -w /work trivortex-agda \
    agda verification/agda/Trivortex.agda   # lands with milestone M1
```

The Dockerfile in [`docker/agda/Dockerfile`](../docker/agda/Dockerfile)
pins the toolchain; the repository CI never requires this build to pass
until milestone M1 lands.

## Toolchain pin and milestones

| Pin | Value |
|---|---|
| Toolchain | Agda 2.6.4 |
| Docker pin | [`docker/agda/Dockerfile`](../docker/agda/Dockerfile) |
| Planned artifact | `verification/agda/Trivortex.agda` |
| Milestone | **M2** of the staged plan |
| CI status | not required to pass until the milestone lands |

## What lands with milestone M2

1. the second prover, cubical-friendly statements (milestone M2) — the three fixed objects (closed form, Chaplygin integral,
   vortex integrals) expressed natively;
2. a CI-callable check that reproduces the Python ladder's reference numbers
   to the documented tolerances (or, for the provers, checks the statements
   with the axioms listed in the artifact header);
3. the acceptance-criteria checklist at the top of this file flipped to done,
   with the artifact header carrying SPDX + copyright lines and a provenance
   note pointing at the commit of `verify.py` it mirrors.

Until then, this directory states the plan and holds nothing else — the
repository's honesty rule forbids quoting a plan as a verification.
