# Lean 4 Verification — Roadmap

> Formalization / port target for the **TRIVORTEX** document
> (`verification/trivortex/python/verify.py`): Theorem 3.1 (the
> Lagrange-type rotating solution), the Chaplygin-type vortex integrals,
> their conservation laws, and the Lagrange equilateral solution.
>
> **Status: landed — v4.0 (milestones M1 + M4/M5/M6/M7 depth tracks).**
> The artifact, the CI-callable check and the bilingual documentation
> live in this directory; the acceptance criteria below are checked.
> The v4.0 release was **built and verified green** against the pinned
> toolchain (Lean 4 v4.6.0 + Mathlib4 tag v4.6.0): 106 theorems with a
> closed axiom footprint, zero `sorry`/`axiom`, `#print axioms` closed
> on every theorem (only `propext`, `Classical.choice`, `Quot.sound`).

---

## Why Lean 4

Lean 4 + Mathlib provides the trigonometric, exponential and
differential-calculus scaffolding the verification statement layer
needs (`Real.cos`, `Real.exp`, `HasDerivAt`, periodicity lemmas,
`is_const_of_deriv_eq_zero`), which makes it the fastest formal path
to the choreography, periodicity, conservation and Lagrange-solution
properties.

## Scope of the port

The port fixes exactly the objects of the Python ladder, so that
every language proves or computes the *same* statements and the
results stay comparable:

1. **Theorem 3.1 (closed form).**
   `r_k(t) = sqrt(C_Ch) * (1 + eps*cos(omega*t + 2*pi*k/3))`,
   `theta_k(t) = omega*t + 2*pi*k/3`,
   `omega = (2*pi/T)*exp(C_Ch/pi)`, `eps = 1/(exp(C_Ch/pi) - 1)`;
   properties established: exact `2*pi/3` angular separation (equilateral
   choreography), periodicity `r_k(t + 2*pi/omega) = r_k(t)`, and —
   new in v2.0 — **positivity** of `r_k(t)` in the regime
   `C_Ch > pi*ln 2` (where `eps < 1`).
2. **Chaplygin integral.** The combination
   `C_Ch = r^2*(theta_dot - q*A_theta)` with `A_theta = 1/r`, following
   the definition fixed in Section 6 of the core document, together with its
   recorded endpoint-drift diagnostic over `[0, 100*T]` (a numerical
   diagnostic by design — the honesty note of
   [`verification/README.md`](../README.md) §13 applies).
3. **Vortex integrals — statements *and* conservation laws.**
   `H`, `P = sum(Gamma*x)`, `Q = sum(Gamma*y)`, `I = sum(Gamma*|r|^2)`:
   v1.1 pinned the exact equilateral anchors `H = 0, P = 0, Q = 0,
   I = Γ`. **v2.0 additionally proves the conservation laws themselves**
   (the analytic core of checks V3/V4): the Kirchhoff point-vortex
   system is defined natively (`KirchhoffSol`: differentiable
   trajectories, no-collision hypotheses), and along *any* Kirchhoff
   solution `d/dt H = d/dt P = d/dt Q = d/dt I = 0`, hence each
   invariant is constant in time.
4. **The Lagrange equilateral solution (new in v2.0, the analytic core
   of check V2).** Three equal vortices on a rotating equilateral
   triangle of side `a` with `omega = 3*Gamma/(2*pi*a^2)` are proven to
   be an *exact* Kirchhoff solution (`lagrangeSol`), and the anchor
   values `H = 0, P = 0, Q = 0, I = Γ` are proven to hold along it
   **for all time** (side `a = 1`), not just at `t = 0`.
5. **The complete theory of the Lagrange triangle (new in v3.0,
   Section 7 of the artifact).** The `lagrange_triangle` scene of
   `verification/trivortex_master` (three equal bodies at 0°, 120°,
   240°) is formalized to full depth: the rotation-group identity
   (`lag_rotation_x/y`), the rigid velocity field d/dt r = ω·J·r
   (`lag_deriv_field_x/y`), the orbit radius a/√3 (`lag_orbit_radius`),
   the Kirchhoff field at an arbitrary trial frequency
   (`lag_kx0_field…lag_ky2_field`), **the forcing theorem**
   (`lag_omega_unique`: a rotating equilateral Kirchhoff triangle must
   rotate at exactly ω = 3Γ/(2πa²) — the analytic identity behind the
   V2 "measured omega" criterion), the period closed form
   T = 4π²a²/(3Γ) (`lag_period_closed`) with periodicity and
   half-period inversion, the choreography cycle (`lag_cycle_x0…y2`),
   the homogeneity/scaling laws of all four integrals (`*_scale`), the
   family scaling laws (`lagomega_scale`, `lag_trajectory_scale_x/y`),
   the distance certificates (`lag_dist01/02/12` — the shape part of
   check V2), and the exact anchors for a triangle of arbitrary side
   `a` (`lagrange_side_H/P/Q/I`: H = −(3Γ²/2π)·ln a, P = Q = 0,
   I = Γa²).
6. **Linear stability of the Lagrange triangle (new in v4.0, Section 8
   of the artifact).** The frame co-rotating at ω = 3Γ/(2πa²)
   (`rot_anchor`: the anchor is its exact fixed point), the
   2π/Γ-scaled linearization `linX1…linY3` with every entry proved to
   lie in ℚ(√3), all six eigenmodes (`eig_trans1/2` ±iω,
   `eig_rot` eigenvalue 0, `eig_dil` the generalized zero mapped to
   −6·phase, `eig_shapeU/W` the shape oscillation ±iω),
   certification of the linearization against the TRUE rotating-frame
   field along every modal line (`lin_cert_transX/Y`,
   `lin_cert_shapeU/W` — 24 HasDerivAt components), explicit modal
   solutions of the linearized equation for all t (`lin_sol_trans`,
   `lin_sol_shape`, `lin_sol_size` — the size drift Q(t) = q − 2ωpt),
   the orthonormal size basis (`lin_size_basis`) and the stability
   bounds (`lin_bound_trans/shape`: the norm is preserved exactly;
   `lin_bound_size`: at most linear growth) — no eigenmode grows
   exponentially: the classical Thomson criterion at N = 3, now
   machine-checked. The characteristic polynomial is λ²(λ²+9)², so
   the spectrum is {0, 0, ±iω, ±iω} in physical units.

## Acceptance criteria

- [x] The objects above are expressed in Lean 4 (Mathlib) with no hidden
      assumptions beyond Mathlib's classical foundations
      (`verification/lean4/Trivortex.lean`);
- [x] A CI-callable check: `lake build` against the pinned toolchain
      (workflow `verification-ports.yml`, job *formal-lean4*);
- [x] The artifact header carries SPDX + copyright lines (REUSE.toml)
      and a provenance note pointing at the commit of `verify.py` it
      mirrors (557bff8, the M0 release);
- [x] `verification/README.md` status table flips this row to
      *landed* with a link;
- [x] (v2.0) Mathlib is pinned to an exact tag in `lakefile.lean`
      (reproducibility: previously `@ "master"`, which cannot build
      against a pinned toolchain);
- [x] (v2.0) The conservation laws of the vortex integrals and the
      Lagrange solution theorem are proven with `#print axioms` closed
      (this absorbs the "Chaplygin identity, proven" M5 track into
      the Lean port: the conservation statement itself is now
      machine-checked);
- [x] (v3.0) The complete Lagrange-triangle theory (Section 7) is
      proven with `#print axioms` closed — 88 theorems in total, zero
      `sorry`/`axiom`.
- [x] (v4.0) Linear stability (Section 8) is proven with `#print
      axioms` closed — 106 theorems in total, zero `sorry`/`axiom`.
      The numeric mirror `verification/notes/numeric_mirror_s8.py`
      (18 checks, all PASS) and the SymPy ladder
      `verification/notes/verify_identities_s8.py` (checks A–K) pin
      the same statements in ℚ(√3) exactly.

## Build recipe

```bash
# pinned toolchain (see docker/lean4/Dockerfile)
docker build -t trivortex-lean verification/docker/lean4
docker run --rm -v "$PWD":/work -w /work trivortex-lean \
    lake build

# local (elan installed): fetch the Mathlib cache once, then build
cd verification/lean4
lake exe cache get && lake build
```

## Toolchain pin and milestones

| Pin | Value |
|---|---|
| Toolchain | Lean 4 **v4.6.0** (upgraded from v4.4.0; see note) |
| Mathlib | tag **v4.6.0** (pinned in `lakefile.lean`; was unpinned `@ master`) |
| Docker pin | [`docker/lean4/Dockerfile`](../docker/lean4/Dockerfile) |
| Artifact | `verification/lean4/Trivortex.lean` (106 axioms-closed theorems) |
| Milestone | M1 + the M4–M7 depth tracks (conservation + Lagrange + complete theory + linear stability) |
| CI status | non-blocking job in `verification-ports.yml` |

> **Toolchain note.** v1.1 pinned Lean v4.4.0 with Mathlib `@ "master"`,
> a combination that can no longer resolve (moving target + fixed
> toolchain), so the v1.1 artifact was not reproducibly buildable.
> v2.0 upgrades the toolchain to v4.6.0 and pins Mathlib to its
> matching tag `v4.6.0`, the newest pair verified to build within the
> Docker/CI disk budget of this framework. The proofs use only
> long-stable Mathlib API, so future bumps are mechanical.

## What landed

- **v1.1 (M1):** the statement layer over Mathlib — choreography
  (`theta_separation`), periodicity (`r_periodic`, `theta_periodic`),
  the Chaplygin shape and the exact equilateral anchors
  (H = 0, P = 0, Q = 0, I = Γ).
- **v2.0 (M4/M5 depth):** `eps_pos`/`eps_lt_one`/`rClosed_pos`
  (positivity of the closed form); the native Kirchhoff system
  (`kx1…ky3`, `KirchhoffSol`); the four conservation theorems
  (`P/Q/I/H_kirchhoff_deriv` + `_conserved` — V3/V4 for ANY
  circulations and ANY non-colliding solution); the Lagrange solution
  (`d2_lag01/12/02`, `lagX/lagY`, `lag_kx0…lag_ky2`,
  `lagrangeSol` — V2); the all-time anchors along the rotating
  solution (`lagrange_anchor_H/P/Q/I`); toolchain modernization
  (v4.4.0 → v4.6.0) and the pinned Mathlib tag.
- **v3.0 (M6 — the complete Lagrange-triangle theory):** Section 7 of
  the artifact — the rotation-group identity, the velocity field
  ω·J·r, the Kirchhoff field at an arbitrary trial frequency, the
  forcing theorem `lag_omega_unique`, the period closed form
  T = 4π²a²/(3Γ), the choreography cycle, the homogeneity (scaling)
  laws of the four integrals, the orbit radius, the distance
  certificates and the general-side anchors — 44 new theorems,
  88 total, all `#print axioms`-closed.
- **v4.0 (M7 — linear stability):** Section 8 of the artifact — the
  co-rotating frame and its fixed point, the 2π/Γ-scaled Jacobian
  rows in ℚ(√3), the six eigenmodes, the certification of the
  linearization against the true rotating-frame field, the modal
  solutions (translation rotation, shape oscillation, size drift),
  the orthonormal size basis and the Thomson stability bounds —
  18 new theorems, 106 total, all `#print axioms`-closed; mirrored
  numerically by `verification/notes/numeric_mirror_s8.py`.

The artifact header lists the axiom footprint (106 theorems, all
`#print axioms`-closed over Mathlib's classical foundations). The
bilingual overview lives in [README_RU.md](README_RU.md).
