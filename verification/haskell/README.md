# Haskell Verification — Roadmap

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

## Why Haskell

Haskell closes the matrix with a lazy, purely functional
implementation of the ladder. The exact-arithmetic story is the
interesting part: the same four checks run once in `Double` and once in
exact rationals (bounded by rational approximation of the
transcendental pieces), which lets the team quantify how much of the
residual budget is consumed by transcendental round-off versus
integrator truncation — a number no other language in the matrix
produces this directly.

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

- [x] The three objects above are expressed in Haskell (GHC + cabal) with no hidden
      assumptions beyond the axioms listed in the artifact header
      (`verification/haskell/` (the `Double` ladder + the exact ℚ(√3) dual));
- [x] A CI-callable check: `cd verification/haskell && cabal test trivortex-guard` — runs the pinned-reference guard and the exact-anchor check (workflow `verification-ports.yml`, job *haskell-dual-ladder*);
- [x] The artifact header carries SPDX + copyright lines (REUSE.toml)
      and a provenance note pointing at the commit of `verify.py` it
      mirrors (557bff8, the M0 release);
- [x] `verification/README.md` status table flips this row to
      *landed (v1.1)* with a link.

## Build recipe

```bash
# pinned toolchain (see docker/haskell/Dockerfile)
docker build -t trivortex-haskell docker/haskell
docker run --rm -v "$PWD":/work -w /work trivortex-haskell \
    cabal build all   # lands with milestone M1
```

The Dockerfile in [`docker/haskell/Dockerfile`](../docker/haskell/Dockerfile)
pins the toolchain; the repository CI never requires this build to pass
until milestone M1 lands.

## Toolchain pin and milestones

| Pin | Value |
|---|---|
| Toolchain | Haskell (GHC) 9.6 |
| Docker pin | [`docker/haskell/Dockerfile`](../docker/haskell/Dockerfile) |
| Planned artifact | `verification/haskell/Verify.hs` |
| Milestone | **M3** of the staged plan |
| CI status | non-blocking job in `verification-ports.yml` |

## What landed (v1.1)

1. the `Double` numeric twin of the ladder (dependency-free, base-only), with the quick preset reproducing the Python reference numbers;
2. the exact-rational dual run: the four anchor values of the equilateral reference state computed in ℚ(√3) where P = 0, Q = 0, I = Γ and H = 0 hold *by computation* (equality on ℚ(√3) is decidable);
3. the interactive bilingual laboratory with SVG/CSV/JSON export.

The artifact header lists the axiom footprint; the JSON protocol of a
real run is committed next to the artifact (`protocol_quick.json`) where
the port is numerical. The bilingual overview lives in
[README_RU.md](README_RU.md).
