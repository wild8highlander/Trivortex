/-
SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
-/
/-
==========================================================================
TRIVORTEX — LEAN 4 FORMALIZATION OF THE VERIFICATION STATEMENT LAYER
==========================================================================
Milestone M1 artifact: `verification/lean4/Trivortex.lean`.

Provenance: this file mirrors the analytic layer of
`verification/trivortex/python/verify.py` (M0 release, repository main
branch, commit 557bff8) — the same three fixed objects, expressed over
`ℝ` with Mathlib:

  1. Theorem 3.1 closed form
       r_k(t)     = √C_Ch · (1 + eps · cos(ω·t + 2πk/3))
       theta_k(t) = ω·t + 2πk/3
       ω = (2π/T)·exp(C_Ch/π),  eps = 1/(exp(C_Ch/π) − 1)
     with the two certified properties PROVEN here:
       • equilateral choreography: theta_(k+1) − theta_k = 2π/3 exactly;
       • periodicity: r_k(t + 2π/ω) = r_k(t) and
         theta_k(t + 2π/ω) = theta_k(t) + 2π.
  2. The Chaplygin topological integral C_Ch = r²(θ̇ − q·A_θ) with the
     gauge A_θ = 1/r: the algebraic shape C_Ch = r²θ̇ − q·r is PROVEN.
  3. The vortex integrals H, P, Q, I of the Kirchhoff equations — defined
     natively; for the equilateral reference state (side a = 1) the exact
     anchor values H = 0, P = 0, Q = 0, I = Γ are PROVEN. The conservation
     claim itself (V3/V4) is the specification the numerical ladders
     certify to the registered tolerance bands, recorded below as a
     machine-checked structure.

AXIOM FOOTPRINT: no `axiom`/`sorry` anywhere — `#print axioms` at the
bottom demonstrates that every theorem depends only on Mathlib's standard
classical foundations (propext, Classical.choice, Quot.sound).

Build (pinned toolchain, docker/lean4/Dockerfile — Lean 4 4.4.0 + Mathlib):
    docker build -t trivortex-lean verification/docker/lean4
    docker run --rm -v "$PWD":/work -w /work verification/lean4 \
        lake build

Author: Isaev Iskhak Khamzatovich (repository owner)
Year: 2026
==========================================================================
-/
import Mathlib.Tactic

namespace Trivortex

/-! ## Section 1 — Theorem 3.1: the closed form and its properties -/

/-- Angular frequency of the closed form: ω = (2π/T)·exp(C_Ch/π). -/
noncomputable def omega (C T : ℝ) : ℝ := (2 * π / T) * Real.exp (C / π)

/-- Radial modulation amplitude: eps = 1/(exp(C_Ch/π) − 1). -/
noncomputable def eps (C : ℝ) : ℝ := 1 / (Real.exp (C / π) - 1)

/-- The radial closed form of Theorem 3.1 for the k-th vortex (k = 0,1,2). -/
noncomputable def rClosed (C T t : ℝ) (k : ℕ) : ℝ :=
  Real.sqrt C * (1 + eps C * Real.cos (omega C T * t + 2 * π * k / 3))

/-- The angular closed form: the rigidly rotating phase of the k-th vortex. -/
noncomputable def thetaClosed (C T t : ℝ) (k : ℕ) : ℝ :=
  omega C T * t + 2 * π * k / 3

/-- The frequency is nonzero in the physical regime C_Ch > 0, T > 0. -/
theorem omega_ne_zero {C T : ℝ} (hC : 0 < C) (hT : 0 < T) : omega C T ≠ 0 := by
  unfold omega
  intro h
  rcases mul_eq_zero.mp h with h1 | h2
  · exact div_ne_zero (by positivity) (ne_of_gt hT) h1
  · exact Real.exp_ne_zero _ h2

/-- **Certified property (a): the equilateral choreography.**
    The angular closed form keeps the exact 2π/3 separation between
    consecutive vortices — the algebraic core of the V1 criterion. -/
theorem theta_separation (C T t : ℝ) (k : ℕ) :
    thetaClosed C T t (k + 1) - thetaClosed C T t k = 2 * π / 3 := by
  unfold thetaClosed
  ring

/-- Stepping three vortices forward returns to vortex 0 with one full turn. -/
theorem theta_three_step (C T t : ℝ) :
    thetaClosed C T t 0 + 2 * π = thetaClosed C T t 3 := by
  unfold thetaClosed
  ring

/-- **Certified property (b): periodicity of the radial closed form.**
    T_r = 2π/ω is a period for every vortex index — the second pass/fail
    criterion of check V1 of the verification ladder. -/
theorem r_periodic (C T t : ℝ) (k : ℕ) (hC : 0 < C) (hT : 0 < T) :
    rClosed C T (t + 2 * π / omega C T) k = rClosed C T t k := by
  have hw : omega C T ≠ 0 := omega_ne_zero hC hT
  have hTne : T ≠ 0 := ne_of_gt hT
  have harg : omega C T * (t + 2 * π / omega C T) + 2 * π * (k : ℝ) / 3
      = (omega C T * t + 2 * π * (k : ℝ) / 3) + 2 * π := by
    unfold omega
    field_simp
  unfold rClosed
  rw [harg, Real.cos_period]

/-- The angular closed form advances by exactly one full turn per T_r —
    the choreography is periodic in the rotating frame. -/
theorem theta_periodic (C T t : ℝ) (k : ℕ) (hC : 0 < C) (hT : 0 < T) :
    thetaClosed C T (t + 2 * π / omega C T) k = thetaClosed C T t k + 2 * π := by
  have hw : omega C T ≠ 0 := omega_ne_zero hC hT
  have hTne : T ≠ 0 := ne_of_gt hT
  unfold thetaClosed omega at *
  field_simp

/-- In the physical regime the frequency is positive. -/
theorem omega_pos {C T : ℝ} (hC : 0 < C) (hT : 0 < T) : 0 < omega C T := by
  unfold omega
  refine mul_pos ?_ (Real.exp_pos _)
  exact div_pos (by positivity) (ne_of_gt hT)

/-! ## Section 2 — the Chaplygin topological integral -/

/-- **The algebraic shape of the Chaplygin integral.** With the gauge
    A_θ = 1/r of Section 6 of the core document, the combination recorded
    by the ladders is C_Ch = r²θ̇ − q·r — proven once and for all here. -/
theorem chaplygin_shape {r thetaDot q : ℝ} (hr : r ≠ 0) :
    r * r * (thetaDot - q * (1 / r)) = r * r * thetaDot - q * r := by
  field_simp

/-- The gauge normalization 1/r·r = 1 for a nonzero radius. -/
theorem gauge_inverse {r : ℝ} (hr : r ≠ 0) : 1 / r * r = 1 := by
  field_simp

/-! ## Section 3 — the vortex integrals of the Kirchhoff equations -/

/-- Distance of two points in the plane. -/
noncomputable def vortexDist (x1 y1 x2 y2 : ℝ) : ℝ :=
  Real.sqrt ((x1 - x2) ^ 2 + (y1 - y2) ^ 2)

/-- Hamiltonian H = −(1/2π)·Σ_{i<j} ΓᵢΓⱼ·ln r_ij. -/
noncomputable def Hvortex (g1 g2 g3 x1 y1 x2 y2 x3 y3 : ℝ) : ℝ :=
  -(1 / (2 * π)) * (g1 * g2 * Real.log (vortexDist x1 y1 x2 y2)
    + g1 * g3 * Real.log (vortexDist x1 y1 x3 y3)
    + g2 * g3 * Real.log (vortexDist x2 y2 x3 y3))

/-- Linear impulses P = Σ Γx and Q = Σ Γy. -/
noncomputable def Pvortex (g1 g2 g3 x1 x2 x3 : ℝ) : ℝ := g1 * x1 + g2 * x2 + g3 * x3
noncomputable def Qvortex (g1 g2 g3 y1 y2 y3 : ℝ) : ℝ := g1 * y1 + g2 * y2 + g3 * y3

/-- Angular impulse I = Σ Γ|r|². -/
noncomputable def Ivortex (g1 g2 g3 x1 y1 x2 y2 x3 y3 : ℝ) : ℝ :=
  g1 * (x1 ^ 2 + y1 ^ 2) + g2 * (x2 ^ 2 + y2 ^ 2) + g3 * (x3 ^ 2 + y3 ^ 2)

/-! ### the equilateral reference state (side a = 1, circumradius 1/√3) -/

/-- The equilateral initial condition of the numerical ladders
    (`equilateral_initial(1.0)`): angles 0, 2π/3, 4π/3 on the circle of
    radius 1/√3 — the same coordinates, exact over `ℝ`. -/
noncomputable def eqX1 : ℝ := 1 / Real.sqrt 3
noncomputable def eqY1 : ℝ := 0
noncomputable def eqX2 : ℝ := -(1 / (2 * Real.sqrt 3))
noncomputable def eqY2 : ℝ := 1 / 2
noncomputable def eqX3 : ℝ := -(1 / (2 * Real.sqrt 3))
noncomputable def eqY3 : ℝ := -(1 / 2)

/-- The three side lengths of the reference state are exactly 1. -/
theorem side1 : vortexDist eqX1 eqY1 eqX2 eqY2 = 1 := by
  have hsq : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have h3 : (3:ℝ) ≠ 0 := by norm_num
  have hdx : eqX1 - eqX2 = 3 / (2 * Real.sqrt 3) := by
    unfold eqX1 eqX2; field_simp [hsq]
  have hdy : eqY1 - eqY2 = -(1 / 2) := by unfold eqY1 eqY2; ring
  unfold vortexDist
  rw [hdx, hdy]
  rw [show (3 / (2 * Real.sqrt 3)) ^ 2 = 3 / 4 from by field_simp [hsq]]
  rw [show (-(1 / 2)) ^ 2 = 1 / 4 from by ring]
  rw [show (3:ℝ) / 4 + 1 / 4 = 1 from by ring]
  exact Real.sqrt_one

theorem side2 : vortexDist eqX2 eqY2 eqX3 eqY3 = 1 := by
  unfold vortexDist eqX2 eqY2 eqX3 eqY3
  rw [show (-(1 / (2 * Real.sqrt 3)) - -(1 / (2 * Real.sqrt 3))) ^ 2 = 0 from by ring]
  rw [show (1 / 2 - -(1 / 2)) ^ 2 = 1 from by ring]
  rw [add_zero, Real.sqrt_one]

theorem side3 : vortexDist eqX3 eqY3 eqX1 eqY1 = 1 := by
  have hsq : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have h3 : (3:ℝ) ≠ 0 := by norm_num
  have hdx : eqX3 - eqX1 = -(3 / (2 * Real.sqrt 3)) := by
    unfold eqX3 eqX1; field_simp [hsq]
  have hdy : eqY3 - eqY1 = -(1 / 2) := by unfold eqY3 eqY1; ring
  unfold vortexDist
  rw [hdx, hdy]
  rw [show (-(3 / (2 * Real.sqrt 3))) ^ 2 = 3 / 4 from by field_simp [hsq]]
  rw [show (-(1 / 2)) ^ 2 = 1 / 4 from by ring]
  rw [show (3:ℝ) / 4 + 1 / 4 = 1 from by ring]
  exact Real.sqrt_one

/-! ### the exact anchor values of the vortex integrals -/

/-- **Exact anchor: H = 0** for the equilateral reference state with equal
    circulations (all three pairwise distances are exactly 1, ln 1 = 0). -/
theorem H_equilateral (g : ℝ) :
    Hvortex g g g eqX1 eqY1 eqX2 eqY2 eqX3 eqY3 = 0 := by
  unfold Hvortex
  rw [side1, side3, side2, Real.log_one]
  ring

/-- **Exact anchor: P = 0** (the centroid of the reference state is the
    origin). -/
theorem P_equilateral (g : ℝ) : Pvortex g g g eqX1 eqX2 eqX3 = 0 := by
  unfold Pvortex eqX1 eqX2 eqX3
  have hsq : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hs3ne : Real.sqrt 3 ≠ 0 := by positivity
  field_simp [hsq, hs3ne]

/-- **Exact anchor: Q = 0**. -/
theorem Q_equilateral (g : ℝ) : Qvortex g g g eqY1 eqY2 eqY3 = 0 := by
  unfold Qvortex eqY1 eqY2 eqY3
  ring

/-- **Exact anchor: I = Γ** (each vortex sits at radius 1/√3, so
    Σ Γ|r|² = 3Γ·(1/3) = Γ). -/
theorem I_equilateral (g : ℝ) :
    Ivortex g g g eqX1 eqY1 eqX2 eqY2 eqX3 eqY3 = g := by
  unfold Ivortex eqX1 eqY1 eqX2 eqY2 eqX3 eqY3
  have hsq : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hs3ne : Real.sqrt 3 ≠ 0 := by positivity
  field_simp [hsq, hs3ne]
  ring

/-! ## Section 4 — the Lagrange specification and the registered bands -/

/-- The Lagrange angular velocity of the rigidly rotating equilateral
    triangle: ω = 3Γ/(2πa²) — the point-vortex twin of the classical
    Lagrange solution. The numerical ladders (Python M0, Rust/C++ M1/M3)
    verify checks V2–V4 against this specification to the registered
    tolerance bands. -/
noncomputable def lagrangeOmega (gamma a : ℝ) : ℝ := 3 * gamma / (2 * π * a ^ 2)

/-- The tolerance bands of the framework (verification/README.md §6) as a
    machine-checked structure: every language port quotes these numbers. -/
structure ToleranceBands where
  bandClosedForm : ℝ  -- 1e-12 : V1 residuals
  bandRk4 : ℝ         -- 1e-10 : V2–V4 drifts
  bandOmega : ℝ       -- 1e-6  : measured omega

/-- The bands registered in `verification/README.md` §6. -/
noncomputable def registeredBands : ToleranceBands :=
  ⟨1e-12, 1e-10, 1e-6⟩

/-! ## The axiom footprint -/

-- Every theorem above must depend only on Mathlib's classical foundations.
#print axioms theta_separation
#print axioms theta_three_step
#print axioms r_periodic
#print axioms theta_periodic
#print axioms omega_pos
#print axioms chaplygin_shape
#print axioms gauge_inverse
#print axioms side1
#print axioms side2
#print axioms side3
#print axioms H_equilateral
#print axioms P_equilateral
#print axioms Q_equilateral
#print axioms I_equilateral

end Trivortex
