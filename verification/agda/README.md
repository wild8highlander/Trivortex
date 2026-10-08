# Agda Verification — Roadmap

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

- [x] The three objects above are expressed in Agda (standard library) with no hidden
      assumptions beyond the axioms listed in the artifact header
      (`verification/agda/Trivortex.agda`);
- [x] A CI-callable check: `agda verification/agda/Trivortex.agda` — type-checks the constructive module in the pinned image (workflow `verification-ports.yml`, job *formal-agda*);
- [x] The artifact header carries SPDX + copyright lines (REUSE.toml)
      and a provenance note pointing at the commit of `verify.py` it
      mirrors (557bff8, the M0 release);
- [x] `verification/README.md` status table flips this row to
      *landed (v1.1)* with a link.

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
| CI status | non-blocking job in `verification-ports.yml` |

## What landed (v1.1)

1. the constructive angle arithmetic: the C3 rotation lattice of the choreography (`rot³ ≡ id` proven on `Fin 3`), the uniform-step phase lattice, the periodicity of the closed form over ℚ given the single declared turn-period axiom, the Chaplygin additivity identity and the exact centroid anchors P = Q = 0;
2. the axiom footprint is declared in the artifact header (the cosine atom and its period — nothing else is postulated).

The artifact header lists the axiom footprint; the JSON protocol of a
real run is committed next to the artifact (`protocol_quick.json`) where
the port is numerical. The bilingual overview lives in
[README_RU.md](README_RU.md).
