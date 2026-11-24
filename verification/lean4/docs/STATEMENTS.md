# STATEMENT INDEX — `Trivortex.lean`

*Auto-generated from `Trivortex.lean` on 2026-11-24 by `verification/notes/make_statement_index.py` — do not hand-edit; regenerate after every change to the Lean file.*

| Metric | Value |
|---|---|
| Theorems indexed | **170** |
| `#print axioms` statements | **170** |
| `sorry` occurrences | **0** (must stay 0) |
| `axiom` declarations | **0** (must stay 0) |
| Top-level sections | 11 |

**Axiom footprint:** every theorem resolves to `[propext, Classical.choice, Quot.sound]` — Mathlib's classical foundations only.

## Contents

- **Section 1 — Theorem 3.1: the closed form and its properties** — 9 theorems
  - the radial regime: positivity of the closed form — 3
- **Section 2 — the Chaplygin topological integral** — 2 theorems
- **Section 3 — the vortex integrals of the Kirchhoff equations** — 9 theorems
  - the equilateral reference state (side a = 1, circumradius 1/√3) — 4
  - the exact anchor values of the vortex integrals — 4
- **Section 4 — the Lagrange specification and the registered bands** — 0 theorems
- **Section 5 — the Kirchhoff point-vortex system and its conservation laws** — 8 theorems
  - private differentiation helpers — 0
  - the linear impulses P and Q are conserved — 4
  - the angular impulse I is conserved — 2
  - the Hamiltonian H is conserved — 2
- **Section 6 — the Lagrange equilateral solution** — 17 theorems
  - the anchors hold along the Lagrange solution for all time — 4
- **Section 7 — the Lagrange triangle: the complete theory** — 44 theorems
  - trigonometric half-period identities — 0
  - the homogeneity of the vortex integrals (scaling laws) — 5
  - the rotation-group identity and the velocity field — 5
  - the period of the choreography — 5
  - the choreography cycle — 6
  - the Kirchhoff field at an arbitrary trial frequency — 6
  - the frequency is forced — 3
  - the scaling law of the family — 7
  - the distance certificates (the shape part of check V2) — 3
  - the anchors for a triangle of arbitrary side a — 4
- **Section 8 — linear stability: the eigenmodes of the perturbed triangle** — 18 theorems
  - the frame rotating with the triangle — 1
  - the linearization at the anchor (the 2π/Γ-scaled Jacobian rows) — 0
  - the six eigenmodes — 6
  - certification: the true rotating-frame field along the modes — 2
  - certification: the true rotating-frame field along the shape modes — 2
  - the modal solutions of the linearized rotating-frame equation — 3
  - the stability bounds (§8.5) — 4
- **The axiom footprint** — 0 theorems
- **Section 9 — Nonlinear continuation of the modes; bifurcation analysis at unequal circulations** — 37 theorems
  - 9.1 The general-circulation Lagrange family — 15
  - 9.2 Exact nonlinear continuation of the modes — 22
- **Section 10 — nonlinear Lyapunov stability via H/I and collinear bifurcations (v6.0)** — 26 theorems
  - 10.1 The energy–Casimir (Lyapunov H/I) stability of the Lagrange triangle — 0
  - the one-dimensional logarithmic Lyapunov inequality — 1
  - the sum-of-squares identity on the momentum level set — 3
  - the coercive Lyapunov inequality — 2
  - the variational principle: partial gradients at the anchor — 0
  - the Lagrange multiplier identity (energy–Casimir criticality) — 6
  - the in-time Lyapunov stability theorem — 2
  - 10.2 Collinear central configurations and their bifurcations — 8
  - 10.3 — the deepening: pitchfork triple root, degenerate circulations, and the second asymmetric equilibrium — 4
  - Section 9 axiom footprint — 0
  - Section 10 axiom footprint — 0

## Section 1 — Theorem 3.1: the closed form and its properties

| Theorem | Statement (docstring, first line) |
|---|---|
| [`omega_ne_zero`](../Trivortex.lean) | The frequency is nonzero in the physical regime C_Ch > 0, T > 0. |
| [`theta_separation`](../Trivortex.lean) | **Certified property (a): the equilateral choreography.** The angular closed form keeps the exact 2π/3 separation between consecutive vortices — the algebrai… |
| [`theta_three_step`](../Trivortex.lean) | Stepping three vortices forward returns to vortex 0 with one full turn. |
| [`r_periodic`](../Trivortex.lean) | **Certified property (b): periodicity of the radial closed form.** T_r = 2π/ω is a period for every vortex index — the second pass/fail criterion of check V1… |
| [`theta_periodic`](../Trivortex.lean) | The angular closed form advances by exactly one full turn per T_r — the choreography is periodic in the rotating frame. -/ the choreography is periodic in th… |
| [`omega_pos`](../Trivortex.lean) | In the physical regime the frequency is positive. |

### the radial regime: positivity of the closed form

| Theorem | Statement (docstring, first line) |
|---|---|
| [`eps_pos`](../Trivortex.lean) | The modulation amplitude is positive whenever C_Ch > 0. |
| [`eps_lt_one`](../Trivortex.lean) | **Regime certificate.** eps < 1 exactly when exp(C_Ch/π) > 2, i.e. when C_Ch > π·ln 2; in that regime the radial factor of Theorem 3.1 is bounded away from z… |
| [`rClosed_pos`](../Trivortex.lean) | **Certified property (c): positivity of the radial closed form.** In the regime C_Ch > π·ln 2 the radius of every vortex stays strictly positive for all time… |

## Section 2 — the Chaplygin topological integral

| Theorem | Statement (docstring, first line) |
|---|---|
| [`chaplygin_shape`](../Trivortex.lean) | **The algebraic shape of the Chaplygin integral.** With the gauge A_θ = 1/r of Section 6 of the core document, the combination recorded by the ladders is C_C… |
| [`gauge_inverse`](../Trivortex.lean) | The gauge normalization 1/r·r = 1 for a nonzero radius. |

## Section 3 — the vortex integrals of the Kirchhoff equations

| Theorem | Statement (docstring, first line) |
|---|---|
| [`vortexDist_eq`](../Trivortex.lean) | *(no docstring)* |

### the equilateral reference state (side a = 1, circumradius 1/√3)

| Theorem | Statement (docstring, first line) |
|---|---|
| [`side1`](../Trivortex.lean) | The three side lengths of the reference state are exactly 1. |
| [`side2`](../Trivortex.lean) | *(no docstring)* |
| [`side3`](../Trivortex.lean) | *(no docstring)* |
| [`side3`](../Trivortex.lean) | The mirrored form of `side3` used by the Hamiltonian anchor. |

### the exact anchor values of the vortex integrals

| Theorem | Statement (docstring, first line) |
|---|---|
| [`H_equilateral`](../Trivortex.lean) | **Exact anchor: H = 0** for the equilateral reference state with equal circulations (all three pairwise distances are exactly 1, ln 1 = 0). -/ circulations (… |
| [`P_equilateral`](../Trivortex.lean) | **Exact anchor: P = 0** (the centroid of the reference state is the origin). -/ origin). |
| [`Q_equilateral`](../Trivortex.lean) | **Exact anchor: Q = 0**. |
| [`I_equilateral`](../Trivortex.lean) | **Exact anchor: I = Γ** (each vortex sits at radius 1/√3, so Σ Γ\|r\|² = 3Γ·(1/3) = Γ). -/ Σ Γ\|r\|² = 3Γ·(1/3) = Γ). |

## Section 4 — the Lagrange specification and the registered bands

## Section 5 — the Kirchhoff point-vortex system and its conservation laws

### private differentiation helpers

### the linear impulses P and Q are conserved

| Theorem | Statement (docstring, first line) |
|---|---|
| [`P_kirchhoff_deriv`](../Trivortex.lean) | **V3/V4 formal core, impulse P.** Along any Kirchhoff solution the linear impulse P = ΣΓx has identically zero derivative. -/ linear impulse P = ΣΓx has iden… |
| [`P_kirchhoff_conserved`](../Trivortex.lean) | **P is constant along any Kirchhoff solution.** |
| [`Q_kirchhoff_deriv`](../Trivortex.lean) | **V3/V4 formal core, impulse Q.** Along any Kirchhoff solution the linear impulse Q = ΣΓy has identically zero derivative. -/ linear impulse Q = ΣΓy has iden… |
| [`Q_kirchhoff_conserved`](../Trivortex.lean) | **Q is constant along any Kirchhoff solution.** |

### the angular impulse I is conserved

| Theorem | Statement (docstring, first line) |
|---|---|
| [`I_kirchhoff_deriv`](../Trivortex.lean) | **V3/V4 formal core, angular impulse.** Along any Kirchhoff solution the angular impulse I = ΣΓ\|r\|² has identically zero derivative. -/ the angular impulse… |
| [`I_kirchhoff_conserved`](../Trivortex.lean) | **I is constant along any Kirchhoff solution.** |

### the Hamiltonian H is conserved

| Theorem | Statement (docstring, first line) |
|---|---|
| [`H_kirchhoff_deriv`](../Trivortex.lean) | **V3/V4 formal core, the Hamiltonian.** Along any Kirchhoff solution the vortex Hamiltonian H = −(1/2π)ΣΓᵢΓⱼ ln r_ij has identically zero derivative — the Ki… |
| [`H_kirchhoff_conserved`](../Trivortex.lean) | **H is constant along any Kirchhoff solution.** |

## Section 6 — the Lagrange equilateral solution

| Theorem | Statement (docstring, first line) |
|---|---|
| [`d2_lag01`](../Trivortex.lean) | **The rotating triangle is equilateral for all t.** Every pairwise squared distance is exactly a² (pair 0,1). -/ squared distance is exactly a² (pair 0,1). |
| [`d2_lag12`](../Trivortex.lean) | Pairwise squared distance of the rotating triangle (pair 1,2). |
| [`d2_lag02`](../Trivortex.lean) | Pairwise squared distance of the rotating triangle (pair 0,2). |
| [`lagX_sum`](../Trivortex.lean) | The centroid of the rotating triangle stays at the origin (x-parts). |
| [`lagY_sum`](../Trivortex.lean) | The centroid of the rotating triangle stays at the origin (y-parts). |
| [`lagX_deriv`](../Trivortex.lean) | Kinematics of the rotating triangle: ẋ_k = −ω·(a/√3)·sin(phase_k). |
| [`lagY_deriv`](../Trivortex.lean) | Kinematics of the rotating triangle: ẏ_k = ω·(a/√3)·cos(phase_k). |
| [`lag_kx0`](../Trivortex.lean) | **Kirchhoff velocity of vortex 0 matches the rigid rotation.** |
| [`lag_kx1`](../Trivortex.lean) | **Kirchhoff velocity of vortex 1 matches the rigid rotation.** |
| [`lag_kx2`](../Trivortex.lean) | **Kirchhoff velocity of vortex 2 matches the rigid rotation.** |
| [`lag_ky0`](../Trivortex.lean) | **Kirchhoff y-velocity of vortex 0 matches the rigid rotation.** |
| [`lag_ky1`](../Trivortex.lean) | **Kirchhoff y-velocity of vortex 1 matches the rigid rotation.** |
| [`lag_ky2`](../Trivortex.lean) | **Kirchhoff y-velocity of vortex 2 matches the rigid rotation.** |

### the anchors hold along the Lagrange solution for all time

| Theorem | Statement (docstring, first line) |
|---|---|
| [`lagrange_anchor_H`](../Trivortex.lean) | **The Hamiltonian stays exactly 0 along the rotating solution** (side a = 1, equal circulations): the Section 3 anchor is a statement about ALL times, not ju… |
| [`lagrange_anchor_P`](../Trivortex.lean) | **The impulse P stays exactly 0 along the rotating solution.** |
| [`lagrange_anchor_Q`](../Trivortex.lean) | **The impulse Q stays exactly 0 along the rotating solution.** |
| [`lagrange_anchor_I`](../Trivortex.lean) | **The angular impulse stays exactly Γ along the rotating solution.** |

## Section 7 — the Lagrange triangle: the complete theory

### trigonometric half-period identities

### the homogeneity of the vortex integrals (scaling laws)

| Theorem | Statement (docstring, first line) |
|---|---|
| [`vortexDist_scale`](../Trivortex.lean) | The distance between two scaled points scales linearly: the pairwise term of the Kirchhoff integrals is homogeneous of degree 1. -/ term of the Kirchhoff int… |
| [`Pvortex_scale`](../Trivortex.lean) | The linear impulse P = ΣΓx is homogeneous of degree 1. |
| [`Qvortex_scale`](../Trivortex.lean) | The linear impulse Q = ΣΓy is homogeneous of degree 1. |
| [`Ivortex_scale`](../Trivortex.lean) | The angular impulse I = ΣΓ\|r\|² is homogeneous of degree 2. |
| [`Hvortex_scale`](../Trivortex.lean) | **The Hamiltonian is quasi-homogeneous**: scaling the configuration by c > 0 shifts H by −(1/2π)·(Γ₁Γ₂+Γ₁Γ₃+Γ₂Γ₃)·ln c — the logarithmic scaling law behind "… |

### the rotation-group identity and the velocity field

| Theorem | Statement (docstring, first line) |
|---|---|
| [`lag_rotation_x`](../Trivortex.lean) | **The Lagrange choreography is a one-parameter rotation group**: the state at time t + s is the state at time t rotated by the angle ω·s — the exact statemen… |
| [`lag_rotation_y`](../Trivortex.lean) | The y-coordinate twin of `lag_rotation_x`. |
| [`lag_deriv_field_x`](../Trivortex.lean) | **The rigid-rotation velocity field**: whatever the frequency, the trajectory derivative is exactly d/dt r_k = −ω·y_k — the point-vortex velocity equals ω·J·… |
| [`lag_deriv_field_y`](../Trivortex.lean) | The y-component of the rigid-rotation velocity field: d/dt y_k = ω·x_k. |
| [`lag_orbit_radius`](../Trivortex.lean) | **The orbit radius**: every vortex of the rotating triangle stays on the circle of radius a/√3 centered at the origin — \|r_k(t)\|² = a²/3. -/ the circle of … |

### the period of the choreography

| Theorem | Statement (docstring, first line) |
|---|---|
| [`lag_period_closed`](../Trivortex.lean) | **The period closed form**: one full turn of the triangle takes T = 2π/ω = 4π²a²/(3Γ) — the number the V2 ladder measures. -/ T = 2π/ω = 4π²a²/(3Γ) — the num… |
| [`lagX_periodic`](../Trivortex.lean) | **Periodicity of the choreography**: after T = 2π/ω every vortex is exactly back at its starting point — the point-vortex twin of the `r_periodic`/`theta_per… |
| [`lagY_periodic`](../Trivortex.lean) | The y-coordinate twin of `lagX_periodic`. |
| [`lagX_half_period`](../Trivortex.lean) | After half the period the triangle is exactly inverted through the origin (rotated by π). -/ origin (rotated by π). |
| [`lagY_half_period`](../Trivortex.lean) | The y-coordinate twin of `lagX_half_period`. |

### the choreography cycle

| Theorem | Statement (docstring, first line) |
|---|---|
| [`lag_cycle_x0`](../Trivortex.lean) | **The choreography cycle**: one third of the period maps vortex 0 exactly onto vortex 1 — the triangle advances by exactly one vertex (x-part). -/ (x-part). |
| [`lag_cycle_x1`](../Trivortex.lean) | The cycle continues: one third of the period maps vortex 1 onto vortex 2 (x-part). -/ vortex 2 (x-part). |
| [`lag_cycle_x2`](../Trivortex.lean) | The cycle closes: one third of the period maps vortex 2 onto vortex 0 (x-part) — the permutation (0 1 2) of the choreography. -/ (x-part) — the permutation (… |
| [`lag_cycle_y0`](../Trivortex.lean) | The choreography cycle, y-part (vortex 0 → 1). |
| [`lag_cycle_y1`](../Trivortex.lean) | The choreography cycle, y-part (vortex 1 → 2). |
| [`lag_cycle_y2`](../Trivortex.lean) | The choreography cycle, y-part (vortex 2 → 0). |

### the Kirchhoff field at an arbitrary trial frequency

| Theorem | Statement (docstring, first line) |
|---|---|
| [`lag_kx0_field`](../Trivortex.lean) | **The Kirchhoff field, form 1 (x-velocity of vortex 0)**: at the vertices of the rotating equilateral triangle — for ANY trial frequency ω — the Kirchhoff x-… |
| [`lag_kx1_field`](../Trivortex.lean) | The Kirchhoff field, form 2 (x-velocity of vortex 1). |
| [`lag_kx2_field`](../Trivortex.lean) | The Kirchhoff field, form 3 (x-velocity of vortex 2). |
| [`lag_ky0_field`](../Trivortex.lean) | The Kirchhoff field, form 4 (y-velocity of vortex 0). |
| [`lag_ky1_field`](../Trivortex.lean) | The Kirchhoff field, form 5 (y-velocity of vortex 1). |
| [`lag_ky2_field`](../Trivortex.lean) | The Kirchhoff field, form 6 (y-velocity of vortex 2). |

### the frequency is forced

| Theorem | Statement (docstring, first line) |
|---|---|
| [`lag_omega_unique`](../Trivortex.lean) | **THE FORCING THEOREM — the frequency is not an ansatz choice.** If the equilateral triangle rotating at an arbitrary trial frequency ν is to satisfy the Kir… |
| [`lagomega_ne_zero`](../Trivortex.lean) | The Lagrange frequency is nonzero whenever the circulation and the side are nonzero. -/ side are nonzero. |
| [`lagomega_pos_iff`](../Trivortex.lean) | **The direction of the rotation**: the Lagrange frequency is positive exactly when the circulation is positive (the side length enters through a², so it neve… |

### the scaling law of the family

| Theorem | Statement (docstring, first line) |
|---|---|
| [`lagomega_scale`](../Trivortex.lean) | The Lagrange frequency scales as ω(λa) = ω(a)/λ² — halving the triangle quadruples the spin rate. -/ triangle quadruples the spin rate. |
| [`lagX_scale`](../Trivortex.lean) | The trajectories of the family are scaled copies: the solution at side c·a is c times the solution at side a, run at the scaled time t/c². -/ c·a is c times … |
| [`lagY_scale`](../Trivortex.lean) | The y-coordinate twin of `lagX_scale`. |
| [`lagX_zero`](../Trivortex.lean) | The initial vertex k = a·(the reference vertex k): the t = 0 slice of the rotating triangle is the reference state, scaled. -/ the rotating triangle is the r… |
| [`lagY_zero`](../Trivortex.lean) | The y-coordinate twin of `lagX_zero`. |
| [`lag_trajectory_scale_x`](../Trivortex.lean) | **The trajectory scaling law**: lagX(c·a, ω(c·a), t) = c·lagX(a, ω(a), t/c²) — the same choreography, time-rescaled. Together with `lagomega_scale` this is t… |
| [`lag_trajectory_scale_y`](../Trivortex.lean) | The y-coordinate twin of `lag_trajectory_scale_x`. |

### the distance certificates (the shape part of check V2)

| Theorem | Statement (docstring, first line) |
|---|---|
| [`lag_dist01`](../Trivortex.lean) | **The side lengths never change, in distance form**: the 0–1 side of the rotating triangle is exactly a for every t (0 < a) — the exact counterpart of the `s… |
| [`lag_dist02`](../Trivortex.lean) | The 0–2 side is exactly a for every t. |
| [`lag_dist12`](../Trivortex.lean) | The 1–2 side is exactly a for every t. |

### the anchors for a triangle of arbitrary side a

| Theorem | Statement (docstring, first line) |
|---|---|
| [`lagrange_side_H`](../Trivortex.lean) | **H along the rotating triangle of side a** (0 < a, all t): the Hamiltonian takes the exact value −(3Γ²/2π)·ln a — the a = 1 anchor `lagrange_anchor_H` is th… |
| [`lagrange_side_P`](../Trivortex.lean) | **P along the rotating triangle of side a** (all t): the linear impulse stays exactly 0. -/ impulse stays exactly 0. |
| [`lagrange_side_Q`](../Trivortex.lean) | **Q along the rotating triangle of side a** (all t): the linear impulse stays exactly 0. -/ impulse stays exactly 0. |
| [`lagrange_side_I`](../Trivortex.lean) | **I along the rotating triangle of side a** (all t): the angular impulse takes the exact value Γa² — the a = 1 anchor `lagrange_anchor_I` is the specializati… |

## Section 8 — linear stability: the eigenmodes of the perturbed triangle

### the frame rotating with the triangle

| Theorem | Statement (docstring, first line) |
|---|---|
| [`rot_anchor`](../Trivortex.lean) | **The rotating-frame equilibrium (§8.1).** The equilateral anchor of Section 3, viewed in the frame rotating at the Lagrange angular velocity ω = 3Γ/(2πa²), … |

### the linearization at the anchor (the 2π/Γ-scaled Jacobian rows)

### the six eigenmodes

| Theorem | Statement (docstring, first line) |
|---|---|
| [`eig_trans1`](../Trivortex.lean) | **Eigenmode 1 — translation (x):** the uniform x-shift direction (1,0,1,0,1,0) is mapped by the linearization to −3·(0,1,0,1,0,1): in the rotating frame a tr… |
| [`eig_trans2`](../Trivortex.lean) | **Eigenmode 2 — translation (y):** the uniform y-shift direction (0,1,0,1,0,1) is mapped to +3·(1,0,1,0,1,0). -/ (0,1,0,1,0,1) is mapped to +3·(1,0,1,0,1,0). |
| [`eig_rot`](../Trivortex.lean) | **Eigenmode 3 — phase (rotation):** the phase direction J·anchor (rotate the whole triangle infinitesimally) is annihilated by the linearization: eigenvalue … |
| [`eig_dil`](../Trivortex.lean) | **Eigenmode 4 — size (dilation):** the radial direction (the anchor itself, per vortex) is mapped to −6·(the phase direction): the generalized zero eigenvalu… |
| [`eig_shapeU`](../Trivortex.lean) | **Eigenmode 5 — shape (u):** the shape direction u = (1, 0, 1/2, −√3/2, 0, 0) — vortices 1 and 2 move, vortex 3 rests — is mapped to −3·w with w = (0, 1, √3/… |
| [`eig_shapeW`](../Trivortex.lean) | **Eigenmode 6 — shape (w):** the conjugate shape direction w = (0, 1, √3/2, 1/2, 0, 0) is mapped to +3·u: together with `eig_shapeU` the shape plane carries … |

### certification: the true rotating-frame field along the modes

| Theorem | Statement (docstring, first line) |
|---|---|
| [`lin_cert_transX`](../Trivortex.lean) | **Certification of the translation modes (x):** the derivative at t = 0 of the TRUE rotating-frame field, evaluated along the line anchor + t·(1,0,1,0,1,0), … |
| [`lin_cert_transY`](../Trivortex.lean) | **Certification of the translation modes (y):** the same along the line anchor + t·(0,1,0,1,0,1). -/ line anchor + t·(0,1,0,1,0,1). |

### certification: the true rotating-frame field along the shape modes

| Theorem | Statement (docstring, first line) |
|---|---|
| [`lin_cert_shapeU`](../Trivortex.lean) | **Certification of the shape mode u:** the derivative at t = 0 of the TRUE rotating-frame field, evaluated along the line anchor + t·(1, 0, 1/2, −√3/2, 0, 0)… |
| [`lin_cert_shapeW`](../Trivortex.lean) | **Certification of the shape mode w:** the same along the line anchor + t·(0, 1, √3/2, 1/2, 0, 0). Together with `lin_cert_shapeU` every interior entry of th… |

### the modal solutions of the linearized rotating-frame equation

| Theorem | Statement (docstring, first line) |
|---|---|
| [`lin_sol_trans`](../Trivortex.lean) | **Modal solution — the translation pair (§8.4).** For the initial uniform shift (b₁, b₂) the linearized rotating-frame equation is solved FOR ALL t by the un… |
| [`lin_sol_shape`](../Trivortex.lean) | **Modal solution — the shape pair (§8.4).** For initial amplitudes (p, q) on the shape plane u, w the linearized rotating-frame equation is solved FOR ALL t … |
| [`lin_sol_size`](../Trivortex.lean) | **Modal solution — the size drift (§8.4).** For initial data (p, q) on the size plane vD, vR (vD = the anchor, vR = J·vD the phase direction) the linearized … |

### the stability bounds (§8.5)

| Theorem | Statement (docstring, first line) |
|---|---|
| [`lin_size_basis`](../Trivortex.lean) | The size plane (vD = anchor, vR = J·anchor) is an orthonormal frame: \|vD\|² = \|vR\|² = 1 and vD·vR = 0. Consequently the modal norm sqrt(p² + Q²) IS the Eu… |
| [`lin_bound_trans`](../Trivortex.lean) | **Stability of the translation pair (§8.5).** The Euclidean norm of the translation modal perturbation is EXACTLY preserved: the offset (b₁·cos ωt + b₂·sin ω… |
| [`lin_bound_shape`](../Trivortex.lean) | **Stability of the shape pair (§8.5).** The Euclidean norm of the shape modal perturbation is EXACTLY preserved: (p·cos ωt + q·sin ωt)² + (q·cos ωt − p·sin ω… |
| [`lin_bound_size`](../Trivortex.lean) | **Stability of the size drift (§8.5).** The modal norm of the size perturbation grows AT MOST LINEARLY in time, sqrt(p² + Q(t)²) ≤ sqrt(p² + q²) + 2·\|ω·p·t\… |

## The axiom footprint

## Section 9 — Nonlinear continuation of the modes; bifurcation analysis at unequal circulations

### 9.1 The general-circulation Lagrange family

| Theorem | Statement (docstring, first line) |
|---|---|
| [`s9_gen_deriv_x`](../Trivortex.lean) | **Rigid rotation of the general-circulation triangle (x).** Whatever the circulations, the continued family rotates rigidly: d/dt x_k = −ω·y_k with ω = G/(2π… |
| [`s9_gen_deriv_y`](../Trivortex.lean) | **Rigid rotation of the general-circulation triangle (y).** |
| [`s9_gen_dist01`](../Trivortex.lean) | The continued triangle has the same pairwise distances as the §7 triangle: the translation cancels in every difference (pair 1,2). -/ triangle: the translati… |
| [`s9_gen_dist02`](../Trivortex.lean) | Pair 1,3. |
| [`s9_gen_dist12`](../Trivortex.lean) | Pair 2,3. |
| [`s9_gen_centroid_x`](../Trivortex.lean) | **The circulation-weighted centroid stays at the origin (x).** Σ Γ_k x_k(t) = 0 along the whole continued trajectory — the identity that makes the rigid rota… |
| [`s9_gen_centroid_y`](../Trivortex.lean) | The circulation-weighted centroid stays at the origin (y). |
| [`s9_gen_field_x1`](../Trivortex.lean) | **The Kirchhoff field along the continued triangle (vortex 1, x).** The weighted-centroid identity collapses the partner sums: V_x(w_1) = −ω·y_1 exactly, for… |
| [`s9_gen_field_y1`](../Trivortex.lean) | Vortex 1, y-component. |
| [`s9_gen_field_x2`](../Trivortex.lean) | Vortex 2, x-component. |
| [`s9_gen_field_y2`](../Trivortex.lean) | Vortex 2, y-component. |
| [`s9_gen_field_x3`](../Trivortex.lean) | Vortex 3, x-component. |
| [`s9_gen_field_y3`](../Trivortex.lean) | Vortex 3, y-component. |
| [`s9_rel_eq`](../Trivortex.lean) | **THE NONLINEAR CONTINUATION THEOREM (§9.1).** For ARBITRARY circulations g1, g2, g3 with nonzero total G = g1+g2+g3 and any side a ≠ 0, the equilateral tria… |
| [`s9_omega_scale`](../Trivortex.lean) | **The rotation rate of the continued branch is regular in the side parameter**: ω(c·a) = ω(a)/c² — the §7 scaling law persists for arbitrary circulations; dω… |

### 9.2 Exact nonlinear continuation of the modes

| Theorem | Statement (docstring, first line) |
|---|---|
| [`s9_kx_shift`](../Trivortex.lean) | Translation invariance of the Kirchhoff field (vortex 1, x). |
| [`s9_ky_shift`](../Trivortex.lean) | Translation invariance (vortex 1, y). |
| [`s9_kx2_shift`](../Trivortex.lean) | Translation invariance (vortex 2, x). |
| [`s9_ky2_shift`](../Trivortex.lean) | Translation invariance (vortex 2, y). |
| [`s9_kx3_shift`](../Trivortex.lean) | Translation invariance (vortex 3, x). |
| [`s9_ky3_shift`](../Trivortex.lean) | Translation invariance (vortex 3, y). |
| [`s9_sol_shift`](../Trivortex.lean) | **The 2-parameter translation orbit (§9.2).** Shifting ANY Kirchhoff solution by a constant vector δ = (b1, b2) produces another exact Kirchhoff solution — f… |
| [`s9_sol_time`](../Trivortex.lean) | **The phase orbit (§9.2).** Re-timing ANY Kirchhoff solution by a constant shift (t ↦ t + s) produces another exact solution — the one-parameter rotation orb… |
| [`s9_trans_dev`](../Trivortex.lean) | **The nonlinear ±iω translation mode (§9.2).** In the frame co-rotating with ω = G/(2πa²), the deviation of the δ-shifted solution from the base trajectory i… |
| [`s9_lin_trans`](../Trivortex.lean) | **The translation eigenpair persists for ARBITRARY circulations**: the 2π-scaled rotating-frame linearization maps the uniform translation (c₁,c₂,c₁,c₂,c₁,c₂… |
| [`s9_lin_diag`](../Trivortex.lean) | **Congruence with the §8 linearization**: at equal circulations g1 = g2 = g3 = g the general matrix is exactly g·(linX1…linY3), the matrix certified against … |
| [`s9_lin_kernel`](../Trivortex.lean) | **The phase mode lies in the kernel for ARBITRARY circulations.** KV = (2√3G/(3g1))·J(anchor) spans ker(genLin): the phase family of §9.2 (re-timed solutions… |
| [`s9_lin_chain`](../Trivortex.lean) | **The size-drift Jordan chain for ARBITRARY circulations.** ANCH = G·(anchor) is the rotating-frame fixed point; the dilation family (scaled triangles are ag… |
| [`s9_shape_gen`](../Trivortex.lean) | **The shape-mode characteristic pair for ARBITRARY circulations (second-order form).** genLin²(U) = −3P·U with P = Γ1Γ2+Γ2Γ3+Γ3Γ1 and U = (−Γ2Ι3, −√3Γ2Ι3, −Γ… |
| [`s9_shape4_a`](../Trivortex.lean) | **Unequal same-sign circulations (Γ = (1,1,4), P = 9 > 0): the shape pair oscillates.** First-order form: genLin(1,1,4)·u4 = −27·utilde4. Together with s9_sh… |
| [`s9_shape4_b`](../Trivortex.lean) | **The twin relation**: genLin(1,1,4)·utilde4 = u4 — closes the ±3i√3 shape pair at Γ = (1,1,4). -/ ±3i√3 shape pair at Γ = (1,1,4). |
| [`s9_lin_sol_shape4`](../Trivortex.lean) | **The shape oscillation is a modal solution at Γ = (1,1,4).** The curve x(t) = 3√3·cos(3√3·t)·u4 + sin(3√3·t)·(−27·utilde4) solves the LINEARIZED rotating-fr… |
| [`s9_collision_a`](../Trivortex.lean) | **The bifurcation point Γ = (1,1,−1/2): the shape pair collides at 0.** Here P = 1+2Γ = 0, and the kernel of genLin(1,1,−1/2) gains the shape direction Uh (k… |
| [`s9_collision_b`](../Trivortex.lean) | **The Jordan chain at the collision**: genLin(1,1,−1/2)·Utilde2 = Uh. The shape plane carries a nontrivial Jordan block at the eigenvalue 0 — the steady-stat… |
| [`s9_eig_unst`](../Trivortex.lean) | **Mixed-sign circulations Γ = (1,1,−1): LINEAR INSTABILITY.** Here P = 1−1−1 = −1 < 0 and the shape factor λ²+3P = λ²−3 contributes the REAL eigenvalue pair … |
| [`s9_lin_sol_unst`](../Trivortex.lean) | **The growing modal solution at Γ = (1,1,−1).** m(t) = e^(√3·t)·v solves the linearized rotating-frame equation ẋ = genLin(1,1,−1)·m exactly (all six compone… |
| [`s9_growth_norm`](../Trivortex.lean) | **Exponential growth of the unstable mode (norm identity).** \|m(t)\|² = 12·e^(2√3·t): the shape perturbation of the mixed-sign triangle Γ = (1,1,−1) is unbo… |

## Section 10 — nonlinear Lyapunov stability via H/I and collinear bifurcations (v6.0)

### 10.1 The energy–Casimir (Lyapunov H/I) stability of the Lagrange triangle

### the one-dimensional logarithmic Lyapunov inequality

| Theorem | Statement (docstring, first line) |
|---|---|
| [`s10_log_bound`](../Trivortex.lean) | **The logarithmic Lyapunov inequality.** For every `u` in the annulus [−1/2, 1/2], ln(1+u) ≤ u − u²/3. Both sides are compared by the fencing theorem on the … |

### the sum-of-squares identity on the momentum level set

| Theorem | Statement (docstring, first line) |
|---|---|
| [`s10_sumsq`](../Trivortex.lean) | The sum of the three squared sides is 3·Σ\|w\|² − \|Σw\|²: pure algebra. |
| [`s10_sumsq_anchor`](../Trivortex.lean) | **The rigid identity on the anchor level set.** For equal circulations with P = Q = 0 and I = Γ (the unit-anchor values), the sum of the three squared sides … |
| [`s10_H_nonneg`](../Trivortex.lean) | **H is globally nonnegative on the anchor level set.** With P = Q = 0, I = Γ and pairwise distinct vortices, the Hamiltonian satisfies H ≥ 0 = H(anchor): the… |

### the coercive Lyapunov inequality

| Theorem | Statement (docstring, first line) |
|---|---|
| [`s10_coercive`](../Trivortex.lean) | **The coercive Lyapunov inequality (energy–Casimir certificate).** On the anchor level set {P = 0, Q = 0, I = Γ} with every squared side in the annulus [1/2,… |
| [`s10_dist_bound`](../Trivortex.lean) | **Corollary — the Lyapunov certificate in distance form.** Under the hypotheses of `s10_coercive`, Σ (r_ij − 1)² ≤ (12π/Γ²) · H. -/ Σ (r_ij − 1)² ≤ (12π/Γ²) … |

### the variational principle: partial gradients at the anchor

### the Lagrange multiplier identity (energy–Casimir criticality)

| Theorem | Statement (docstring, first line) |
|---|---|
| [`s10_casimir_x1`](../Trivortex.lean) | **Variational principle, x₁-slot.** The energy–Casimir functional H + (3Γ/(4π))·I has zero x₁-gradient at the anchor: ∇H = −(3Γ/(4π))·∇I there (Lagrange mult… |
| [`s10_casimir_y1`](../Trivortex.lean) | **Variational principle, y₁-slot.** |
| [`s10_casimir_x2`](../Trivortex.lean) | **Variational principle, x₂-slot.** |
| [`s10_casimir_y2`](../Trivortex.lean) | **Variational principle, y₂-slot.** |
| [`s10_casimir_x3`](../Trivortex.lean) | **Variational principle, x₃-slot.** |
| [`s10_casimir_y3`](../Trivortex.lean) | **Variational principle, y₃-slot.** |

### the in-time Lyapunov stability theorem

| Theorem | Statement (docstring, first line) |
|---|---|
| [`s10_lyapunov_stab`](../Trivortex.lean) | **Nonlinear Lyapunov stability of the Lagrange triangle (H/I form).** Let a Kirchhoff solution with equal circulations Γ > 0 stay on the anchor level set (P … |
| [`s10_lyapunov_dist`](../Trivortex.lean) | **Nonlinear Lyapunov stability, distance form.** Under the hypotheses of `s10_lyapunov_stab`, at every time the three squared distances (from the side-1 valu… |

### 10.2 Collinear central configurations and their bifurcations

| Theorem | Statement (docstring, first line) |
|---|---|
| [`s10_col_sol_gen`](../Trivortex.lean) | **The general collinear rotating relative equilibrium.** Three vortices with circulations (1, 1, γ) at the collinear positions (x₁, x₂, x₃), pairwise distinc… |
| [`s10_col_sym`](../Trivortex.lean) | **The symmetric collinear family** (d, −d, 0) with circulations (1, 1, γ) is a rotating relative equilibrium for EVERY γ and every d ≠ 0, with rotation rate … |
| [`s10_col_static`](../Trivortex.lean) | **The stationary collinear equilibrium.** At γ = −½ the symmetric collinear configuration (d, −d, 0) has rotation rate ω = 0: it is a genuine stationary poin… |
| [`s10_col_pitchfork`](../Trivortex.lean) | **The pitchfork.** The constant coefficient of the bifurcation polynomial vanishes EXACTLY at γ = −5/4: this is where the asymmetric collinear branch is born… |
| [`s10_col_disc`](../Trivortex.lean) | **The discriminant identity.** The discriminant of the quadratic M̃(s, γ) in s is (4γ+5)(γ+2)² — the complete bifurcation diagram of the collinear family: tw… |
| [`s10_col_count_quarter`](../Trivortex.lean) | **The asymmetric-branch count at γ₀ = −1/4.** The chart equation N(s, −1/4) = 0 has exactly the roots s = 0, s = 16/9, s = −16/5 and s = 1 (the last excluded… |
| [`s10_col_count_eq1`](../Trivortex.lean) | **No asymmetric branch at equal circulations.** For Γ = (1, 1, 1) the chart equation N(s, 1) = 0 has only the roots s = 0, s = −1 and s = 1 — every collinear… |
| [`s10_col_asym`](../Trivortex.lean) | **The exact asymmetric collinear relative equilibrium** at Γ = (1, 1, −1/4): the configuration (1, −5/9, 16/9) — the middle vortex is vortex 1 — rotates at ω… |

### 10.3 — the deepening: pitchfork triple root, degenerate circulations, and the second asymmetric equilibrium

| Theorem | Statement (docstring, first line) |
|---|---|
| [`s10_pitchfork_double`](../Trivortex.lean) | **The pitchfork is a triple root.** At the pitchfork γ = −5/4 the chart polynomial collapses to N(s, −5/4) = −(9/64)·s³·(s−1): the quadratic factor degenerat… |
| [`s10_col_count_neg1`](../Trivortex.lean) | **The degenerate circulation γ = −1.** Because (γ+1)² vanishes, the quadratic factor of the chart equation collapses to a linear one: N(s, −1) = −s·(s−1)², s… |
| [`s10_col_count_neg2`](../Trivortex.lean) | **The discriminant-zero circulation γ = −2.** The discriminant (4γ+5)(γ+2)² vanishes because of (γ+2)²: the quadratic factor is the perfect square −3·(s−1)² … |
| [`s10_col_asym2`](../Trivortex.lean) | **The second asymmetric collinear relative equilibrium** at Γ = (1, 1, −1/4): the configuration (1, −9/5, −16/5) — vortex 3 is the outer one on the negative … |

### Section 9 axiom footprint

### Section 10 axiom footprint
