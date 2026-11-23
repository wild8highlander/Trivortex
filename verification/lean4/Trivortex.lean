/-
SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
-/
/-
==========================================================================
TRIVORTEX — LEAN 4 FORMALIZATION: THE FULL STATEMENT LAYER (v2.0)
==========================================================================
Milestone M4/M5 artifact: `verification/lean4/Trivortex.lean`.

Provenance: this file mirrors the analytic layer of
`verification/trivortex/python/verify.py` (M0 release, repository main
branch, commit 557bff8) — the same three fixed objects, expressed over
`ℝ` with Mathlib — and adds the two dynamical statements that the v1.1
release still left to the numerical ladders only:

  1. Theorem 3.1 closed form
       r_k(t)     = √C_Ch · (1 + eps · cos(ω·t + 2πk/3))
       theta_k(t) = ω·t + 2πk/3
       ω = (2π/T)·exp(C_Ch/π),  eps = 1/(exp(C_Ch/π) − 1)
     PROVEN here:
       • equilateral choreography: theta_(k+1) − theta_k = 2π/3 exactly;
       • periodicity: r_k(t + 2π/ω) = r_k(t) and
         theta_k(t + 2π/ω) = theta_k(t) + 2π;
       • positivity: in the regime C_Ch > π·ln 2 (i.e. eps < 1) every
         r_k(t) is strictly positive for all t.
  2. The Chaplygin topological integral C_Ch = r²(θ̇ − q·A_θ) with the
     gauge A_θ = 1/r: the algebraic shape C_Ch = r²θ̇ − q·r is PROVEN.
  3. The vortex integrals H, P, Q, I of the Kirchhoff equations.
     v1.1 proved the exact equilateral anchor values H = 0, P = 0,
     Q = 0, I = Γ. v2.0 additionally PROVES the conservation laws
     themselves — the analytic core of checks V3/V4:
       • the Kirchhoff point-vortex system is defined natively
         (right-hand side, solution structure with differentiable
         trajectories and no-collision hypotheses);
       • along ANY Kirchhoff solution the four integrals are CONSTANT:
         d/dt H = d/dt P = d/dt Q = d/dt I = 0, hence
         H(t) = H(0), P(t) = P(0), Q(t) = Q(0), I(t) = I(0);
       • the Lagrange equilateral rotation (three equal vortices on a
         rotating triangle of side a with ω = 3Γ/(2πa²)) is PROVEN to be
         an exact Kirchhoff solution — the analytic core of check V2 —
         and the anchor values H = 0, P = 0, Q = 0, I = Γ therefore
         hold along it FOR ALL TIME (a = 1).

AXIOM FOOTPRINT: no `axiom`/`sorry` anywhere — `#print axioms` at the
bottom demonstrates that every theorem depends only on Mathlib's standard
classical foundations (propext, Classical.choice, Quot.sound).

Toolchain pin (reproducibility, verification/README.md §8): Lean 4
v4.6.0 + Mathlib4 tag v4.6.0, resolved through the pinned `lakefile.lean`.

Build (pinned toolchain, docker/lean4/Dockerfile):
    docker build -t trivortex-lean verification/docker/lean4
    docker run --rm -v "$PWD":/work -w /work verification/lean4 \
        lake build
Local (elan installed): cd verification/lean4 && lake exe cache get && lake build

Author: Isaev Iskhak Khamzatovich (repository owner)
Year: 2026
==========================================================================
-/
import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv

namespace Trivortex

/-! ## Section 1 — Theorem 3.1: the closed form and its properties -/

/-- Angular frequency of the closed form: ω = (2π/T)·exp(C_Ch/π). -/
noncomputable def omega (C T : ℝ) : ℝ := (2 * Real.pi / T) * Real.exp (C / Real.pi)

/-- Radial modulation amplitude: eps = 1/(exp(C_Ch/π) − 1). -/
noncomputable def eps (C : ℝ) : ℝ := 1 / (Real.exp (C / Real.pi) - 1)

/-- The radial closed form of Theorem 3.1 for the k-th vortex (k = 0,1,2). -/
noncomputable def rClosed (C T t : ℝ) (k : ℕ) : ℝ :=
  Real.sqrt C * (1 + eps C * Real.cos (omega C T * t + 2 * Real.pi * k / 3))

/-- The angular closed form: the rigidly rotating phase of the k-th vortex. -/
noncomputable def thetaClosed (C T t : ℝ) (k : ℕ) : ℝ :=
  omega C T * t + 2 * Real.pi * k / 3

/-- The frequency is nonzero in the physical regime C_Ch > 0, T > 0. -/
theorem omega_ne_zero {C T : ℝ} (hC : 0 < C) (hT : 0 < T) : omega C T ≠ 0 := by
  unfold omega
  intro h
  rcases mul_eq_zero.mp h with h1 | h2
  · exact div_ne_zero (by positivity) (ne_of_gt hT) h1
  · exact absurd h2 (ne_of_gt (Real.exp_pos _))

/-- **Certified property (a): the equilateral choreography.**
    The angular closed form keeps the exact 2π/3 separation between
    consecutive vortices — the algebraic core of the V1 criterion. -/
theorem theta_separation (C T t : ℝ) (k : ℕ) :
    thetaClosed C T t (k + 1) - thetaClosed C T t k = 2 * Real.pi / 3 := by
  unfold thetaClosed
  push_cast
  ring

/-- Stepping three vortices forward returns to vortex 0 with one full turn. -/
theorem theta_three_step (C T t : ℝ) :
    thetaClosed C T t 0 + 2 * Real.pi = thetaClosed C T t 3 := by
  unfold thetaClosed
  push_cast
  ring

/-- **Certified property (b): periodicity of the radial closed form.**
    T_r = 2π/ω is a period for every vortex index — the second pass/fail
    criterion of check V1 of the verification ladder. -/
theorem r_periodic (C T t : ℝ) (k : ℕ) (hC : 0 < C) (hT : 0 < T) :
    rClosed C T (t + 2 * Real.pi / omega C T) k = rClosed C T t k := by
  have hw : omega C T ≠ 0 := omega_ne_zero hC hT
  have hTne : T ≠ 0 := ne_of_gt hT
  have harg : omega C T * (t + 2 * Real.pi / omega C T) + 2 * Real.pi * (k : ℝ) / 3
      = (omega C T * t + 2 * Real.pi * (k : ℝ) / 3) + 2 * Real.pi := by
    unfold omega
    field_simp
    ring
  unfold rClosed
  rw [harg, Real.cos_add_two_pi]

/-- The angular closed form advances by exactly one full turn per T_r —
    the choreography is periodic in the rotating frame. -/
theorem theta_periodic (C T t : ℝ) (k : ℕ) (hC : 0 < C) (hT : 0 < T) :
    thetaClosed C T (t + 2 * Real.pi / omega C T) k = thetaClosed C T t k + 2 * Real.pi := by
  have hw : omega C T ≠ 0 := omega_ne_zero hC hT
  have hTne : T ≠ 0 := ne_of_gt hT
  unfold thetaClosed omega at *
  field_simp
  ring

/-- In the physical regime the frequency is positive. -/
theorem omega_pos {C T : ℝ} (hC : 0 < C) (hT : 0 < T) : 0 < omega C T := by
  unfold omega
  refine mul_pos ?_ (Real.exp_pos _)
  exact div_pos (by positivity) hT

/-! ### the radial regime: positivity of the closed form -/

/-- The modulation amplitude is positive whenever C_Ch > 0. -/
theorem eps_pos {C : ℝ} (hC : 0 < C) : 0 < eps C := by
  have h1 : (1:ℝ) < Real.exp (C / Real.pi) :=
    Real.one_lt_exp_iff.mpr (by positivity)
  have h2 : (0:ℝ) < Real.exp (C / Real.pi) - 1 := by linarith
  unfold eps
  exact div_pos zero_lt_one h2

/-- **Regime certificate.** eps < 1 exactly when exp(C_Ch/π) > 2, i.e.
    when C_Ch > π·ln 2; in that regime the radial factor of Theorem 3.1
    is bounded away from zero for every phase. -/
theorem eps_lt_one {C : ℝ} (hC : Real.pi * Real.log 2 < C) : eps C < 1 := by
  have hp : (0:ℝ) < Real.pi := Real.pi_pos
  have hl : Real.log 2 < C / Real.pi := by
    rw [lt_div_iff hp]
    linarith
  have h2 : (2:ℝ) < Real.exp (C / Real.pi) := by
    have := Real.exp_lt_exp.mpr hl
    rwa [Real.exp_log (by norm_num)] at this
  have h1 : (1:ℝ) < Real.exp (C / Real.pi) - 1 := by linarith
  have hd : (0:ℝ) < Real.exp (C / Real.pi) - 1 := by linarith
  unfold eps
  rw [div_lt_iff hd]
  linarith

/-- **Certified property (c): positivity of the radial closed form.**
    In the regime C_Ch > π·ln 2 the radius of every vortex stays strictly
    positive for all times — the closed form never crosses the origin. -/
theorem rClosed_pos {C T : ℝ} (hC : 0 < C) (hln : Real.pi * Real.log 2 < C)
    (t : ℝ) (k : ℕ) : 0 < rClosed C T t k := by
  have heps : 0 < eps C := eps_pos hC
  have hlt : eps C < 1 := eps_lt_one hln
  have hc : -1 ≤ Real.cos (omega C T * t + 2 * Real.pi * (k : ℝ) / 3) :=
    Real.neg_one_le_cos _
  have hinner : (0:ℝ) < 1 + eps C * Real.cos (omega C T * t + 2 * Real.pi * (k : ℝ) / 3) := by
    nlinarith [heps, hlt, hc]
  unfold rClosed
  exact mul_pos (by positivity) hinner

/-! ## Section 2 — the Chaplygin topological integral -/

/-- **The algebraic shape of the Chaplygin integral.** With the gauge
    A_θ = 1/r of Section 6 of the core document, the combination recorded
    by the ladders is C_Ch = r²θ̇ − q·r — proven once and for all here. -/
theorem chaplygin_shape {r thetaDot q : ℝ} (hr : r ≠ 0) :
    r * r * (thetaDot - q * (1 / r)) = r * r * thetaDot - q * r := by
  field_simp
  ring

/-- The gauge normalization 1/r·r = 1 for a nonzero radius. -/
theorem gauge_inverse {r : ℝ} (hr : r ≠ 0) : 1 / r * r = 1 := by
  field_simp

/-! ## Section 3 — the vortex integrals of the Kirchhoff equations -/

/-- Distance of two points in the plane. -/
noncomputable def vortexDist (x1 y1 x2 y2 : ℝ) : ℝ :=
  Real.sqrt ((x1 - x2) ^ 2 + (y1 - y2) ^ 2)

/-- The squared distance — the polynomial core of `vortexDist`. -/
def d2 (x1 y1 x2 y2 : ℝ) : ℝ := (x1 - x2) ^ 2 + (y1 - y2) ^ 2

theorem vortexDist_eq (x1 y1 x2 y2 : ℝ) :
    vortexDist x1 y1 x2 y2 = Real.sqrt (d2 x1 y1 x2 y2) := rfl

/-- Hamiltonian H = −(1/2π)·Σ_{i<j} ΓᵢΓⱼ·ln r_ij. -/
noncomputable def Hvortex (g1 g2 g3 x1 y1 x2 y2 x3 y3 : ℝ) : ℝ :=
  -(1 / (2 * Real.pi)) * (g1 * g2 * Real.log (vortexDist x1 y1 x2 y2)
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
  have hs3ne : Real.sqrt 3 ≠ 0 := by positivity
  have hdx : eqX1 - eqX2 = 3 / (2 * Real.sqrt 3) := by
    unfold eqX1 eqX2; field_simp [hsq, hs3ne]; nlinarith [hsq]
  have hdy : eqY1 - eqY2 = -(1 / 2) := by unfold eqY1 eqY2; ring
  have hq : (3 / (2 * Real.sqrt 3)) ^ 2 + (-(1 / 2)) ^ 2 = 1 := by
    field_simp [hsq, hs3ne]
    nlinarith [hsq]
  unfold vortexDist
  rw [hdx, hdy, hq]
  exact Real.sqrt_one

theorem side2 : vortexDist eqX2 eqY2 eqX3 eqY3 = 1 := by
  unfold vortexDist eqX2 eqY2 eqX3 eqY3
  have hq : (-(1 / (2 * Real.sqrt 3)) - -(1 / (2 * Real.sqrt 3))) ^ 2
      + (1 / 2 - -(1 / 2)) ^ 2 = 1 := by
    ring
  rw [hq]
  exact Real.sqrt_one

theorem side3 : vortexDist eqX3 eqY3 eqX1 eqY1 = 1 := by
  have hsq : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hs3ne : Real.sqrt 3 ≠ 0 := by positivity
  have hdx : eqX3 - eqX1 = -(3 / (2 * Real.sqrt 3)) := by
    unfold eqX3 eqX1; field_simp [hsq, hs3ne]; nlinarith [hsq]
  have hdy : eqY3 - eqY1 = -(1 / 2) := by unfold eqY3 eqY1; ring
  have hq : (-(3 / (2 * Real.sqrt 3))) ^ 2 + (-(1 / 2)) ^ 2 = 1 := by
    field_simp [hsq, hs3ne]
    nlinarith [hsq]
  unfold vortexDist
  rw [hdx, hdy, hq]
  exact Real.sqrt_one

/-- The mirrored form of `side3` used by the Hamiltonian anchor. -/
theorem side3' : vortexDist eqX1 eqY1 eqX3 eqY3 = 1 := by
  have hsq : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hs3ne : Real.sqrt 3 ≠ 0 := by positivity
  have hdx : eqX1 - eqX3 = 3 / (2 * Real.sqrt 3) := by
    unfold eqX1 eqX3; field_simp [hsq, hs3ne]; nlinarith [hsq]
  have hdy : eqY1 - eqY3 = 1 / 2 := by unfold eqY1 eqY3; ring
  have hq : (3 / (2 * Real.sqrt 3)) ^ 2 + (1 / 2) ^ 2 = 1 := by
    field_simp [hsq, hs3ne]
    nlinarith [hsq]
  unfold vortexDist
  rw [hdx, hdy, hq]
  exact Real.sqrt_one

/-! ### the exact anchor values of the vortex integrals -/

/-- **Exact anchor: H = 0** for the equilateral reference state with equal
    circulations (all three pairwise distances are exactly 1, ln 1 = 0). -/
theorem H_equilateral (g : ℝ) :
    Hvortex g g g eqX1 eqY1 eqX2 eqY2 eqX3 eqY3 = 0 := by
  unfold Hvortex
  rw [side1, side3', side2, Real.log_one]
  ring

/-- **Exact anchor: P = 0** (the centroid of the reference state is the
    origin). -/
theorem P_equilateral (g : ℝ) : Pvortex g g g eqX1 eqX2 eqX3 = 0 := by
  unfold Pvortex eqX1 eqX2 eqX3
  have hsq : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hs3ne : Real.sqrt 3 ≠ 0 := by positivity
  field_simp [hsq, hs3ne]
  nlinarith [hsq]

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
  linear_combination (-128 * g * Real.sqrt 3 ^ 2) * hsq

/-! ## Section 4 — the Lagrange specification and the registered bands -/

/-- The Lagrange angular velocity of the rigidly rotating equilateral
    triangle: ω = 3Γ/(2πa²) — the point-vortex twin of the classical
    Lagrange solution. Section 6 proves that the rotation at exactly this
    frequency is a Kirchhoff solution. -/
noncomputable def lagrangeOmega (gamma a : ℝ) : ℝ := 3 * gamma / (2 * Real.pi * a ^ 2)

/-- The tolerance bands of the framework (verification/README.md §6) as a
    machine-checked structure: every language port quotes these numbers. -/
structure ToleranceBands where
  bandClosedForm : ℝ  -- 1e-12 : V1 residuals
  bandRk4 : ℝ         -- 1e-10 : V2–V4 drifts
  bandOmega : ℝ       -- 1e-6  : measured omega

/-- The bands registered in `verification/README.md` §6. -/
noncomputable def registeredBands : ToleranceBands :=
  ⟨1e-12, 1e-10, 1e-6⟩

/-! ## Section 5 — the Kirchhoff point-vortex system and its conservation laws -/

/-! The right-hand side below mirrors `vortex_rhs` of
    `verification/trivortex/python/verify.py` exactly (three vortices,
    circulations Γ₁, Γ₂, Γ₃):
      dx_i/dt = −1/(2π) Σ_{j≠i} Γ_j (y_i − y_j)/r_ij²,
      dy_i/dt = +1/(2π) Σ_{j≠i} Γ_j (x_i − x_j)/r_ij². -/

/-- x-velocity of vortex 1 (partners 2 and 3). -/
noncomputable def kx1 (g1 g2 g3 x1 y1 x2 y2 x3 y3 : ℝ) : ℝ :=
  -(1 / (2 * Real.pi)) * (g2 * (y1 - y2) / d2 x1 y1 x2 y2
    + g3 * (y1 - y3) / d2 x1 y1 x3 y3)

/-- y-velocity of vortex 1. -/
noncomputable def ky1 (g1 g2 g3 x1 y1 x2 y2 x3 y3 : ℝ) : ℝ :=
  (1 / (2 * Real.pi)) * (g2 * (x1 - x2) / d2 x1 y1 x2 y2
    + g3 * (x1 - x3) / d2 x1 y1 x3 y3)

/-- x-velocity of vortex 2 (partners 1 and 3). -/
noncomputable def kx2 (g1 g2 g3 x1 y1 x2 y2 x3 y3 : ℝ) : ℝ :=
  -(1 / (2 * Real.pi)) * (g1 * (y2 - y1) / d2 x1 y1 x2 y2
    + g3 * (y2 - y3) / d2 x2 y2 x3 y3)

/-- y-velocity of vortex 2. -/
noncomputable def ky2 (g1 g2 g3 x1 y1 x2 y2 x3 y3 : ℝ) : ℝ :=
  (1 / (2 * Real.pi)) * (g1 * (x2 - x1) / d2 x1 y1 x2 y2
    + g3 * (x2 - x3) / d2 x2 y2 x3 y3)

/-- x-velocity of vortex 3 (partners 1 and 2). -/
noncomputable def kx3 (g1 g2 g3 x1 y1 x2 y2 x3 y3 : ℝ) : ℝ :=
  -(1 / (2 * Real.pi)) * (g1 * (y3 - y1) / d2 x1 y1 x3 y3
    + g2 * (y3 - y2) / d2 x2 y2 x3 y3)

/-- y-velocity of vortex 3. -/
noncomputable def ky3 (g1 g2 g3 x1 y1 x2 y2 x3 y3 : ℝ) : ℝ :=
  (1 / (2 * Real.pi)) * (g1 * (x3 - x1) / d2 x1 y1 x3 y3
    + g2 * (x3 - x2) / d2 x2 y2 x3 y3)

/-- **A Kirchhoff solution**: three differentiable plane trajectories
    obeying the point-vortex equations, with no two vortices ever
    colliding (so the right-hand side is defined for all t). -/
structure KirchhoffSol (g1 g2 g3 : ℝ) where
  x1 : ℝ → ℝ
  y1 : ℝ → ℝ
  x2 : ℝ → ℝ
  y2 : ℝ → ℝ
  x3 : ℝ → ℝ
  y3 : ℝ → ℝ
  hx1 : ∀ t, HasDerivAt (x1) (kx1 g1 g2 g3 (x1 t) (y1 t) (x2 t) (y2 t) (x3 t) (y3 t)) t
  hy1 : ∀ t, HasDerivAt (y1) (ky1 g1 g2 g3 (x1 t) (y1 t) (x2 t) (y2 t) (x3 t) (y3 t)) t
  hx2 : ∀ t, HasDerivAt (x2) (kx2 g1 g2 g3 (x1 t) (y1 t) (x2 t) (y2 t) (x3 t) (y3 t)) t
  hy2 : ∀ t, HasDerivAt (y2) (ky2 g1 g2 g3 (x1 t) (y1 t) (x2 t) (y2 t) (x3 t) (y3 t)) t
  hx3 : ∀ t, HasDerivAt (x3) (kx3 g1 g2 g3 (x1 t) (y1 t) (x2 t) (y2 t) (x3 t) (y3 t)) t
  hy3 : ∀ t, HasDerivAt (y3) (ky3 g1 g2 g3 (x1 t) (y1 t) (x2 t) (y2 t) (x3 t) (y3 t)) t
  hd12 : ∀ t, d2 (x1 t) (y1 t) (x2 t) (y2 t) ≠ 0
  hd13 : ∀ t, d2 (x1 t) (y1 t) (x3 t) (y3 t) ≠ 0
  hd23 : ∀ t, d2 (x2 t) (y2 t) (x3 t) (y3 t) ≠ 0

/-! ### private differentiation helpers -/

private theorem deriv_mul_const_left {f : ℝ → ℝ} {f' c : ℝ} {t : ℝ}
    (h : HasDerivAt f f' t) : HasDerivAt (fun s => c * f s) (c * f') t :=
  ((hasDerivAt_const (c := c) (x := t)).mul h).congr_deriv (by simp)

private theorem deriv_congr {f g : ℝ → ℝ} {f' t : ℝ}
    (h : HasDerivAt f f' t) (heq : ∀ s, f s = g s) : HasDerivAt g f' t :=
  h.congr_of_eventuallyEq (Filter.eventually_of_forall fun s => (heq s).symm)

/-! ### the linear impulses P and Q are conserved -/

/-- **V3/V4 formal core, impulse P.** Along any Kirchhoff solution the
    linear impulse P = ΣΓx has identically zero derivative. -/
theorem P_kirchhoff_deriv (g1 g2 g3 : ℝ) (sol : KirchhoffSol g1 g2 g3) (t : ℝ) :
    HasDerivAt (fun s => Pvortex g1 g2 g3 (sol.x1 s) (sol.x2 s) (sol.x3 s)) 0 t := by
  have h1 := deriv_mul_const_left (sol.hx1 t) (c := g1)
  have h2 := deriv_mul_const_left (sol.hx2 t) (c := g2)
  have h3 := deriv_mul_const_left (sol.hx3 t) (c := g3)
  have hsum := (h1.add h2).add h3
  have hzero : g1 * kx1 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
        (sol.x3 t) (sol.y3 t)
      + g2 * kx2 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
        (sol.x3 t) (sol.y3 t)
      + g3 * kx3 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
        (sol.x3 t) (sol.y3 t) = 0 := by
    have e12 := sol.hd12 t
    have e13 := sol.hd13 t
    have e23 := sol.hd23 t
    simp only [kx1, kx2, kx3]
    field_simp
    ring
  rw [hzero] at hsum
  exact hsum

/-- **P is constant along any Kirchhoff solution.** -/
theorem P_kirchhoff_conserved (g1 g2 g3 : ℝ) (sol : KirchhoffSol g1 g2 g3) (s t : ℝ) :
    Pvortex g1 g2 g3 (sol.x1 s) (sol.x2 s) (sol.x3 s)
      = Pvortex g1 g2 g3 (sol.x1 t) (sol.x2 t) (sol.x3 t) := by
  have h : ∀ u, HasDerivAt (fun r => Pvortex g1 g2 g3 (sol.x1 r) (sol.x2 r) (sol.x3 r)) 0 u :=
    fun u => P_kirchhoff_deriv g1 g2 g3 sol u
  exact is_const_of_deriv_eq_zero (fun u => (h u).differentiableAt)
    (fun u => (h u).deriv) s t

/-- **V3/V4 formal core, impulse Q.** Along any Kirchhoff solution the
    linear impulse Q = ΣΓy has identically zero derivative. -/
theorem Q_kirchhoff_deriv (g1 g2 g3 : ℝ) (sol : KirchhoffSol g1 g2 g3) (t : ℝ) :
    HasDerivAt (fun s => Qvortex g1 g2 g3 (sol.y1 s) (sol.y2 s) (sol.y3 s)) 0 t := by
  have h1 := deriv_mul_const_left (sol.hy1 t) (c := g1)
  have h2 := deriv_mul_const_left (sol.hy2 t) (c := g2)
  have h3 := deriv_mul_const_left (sol.hy3 t) (c := g3)
  have hsum := (h1.add h2).add h3
  have hzero : g1 * ky1 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
        (sol.x3 t) (sol.y3 t)
      + g2 * ky2 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
        (sol.x3 t) (sol.y3 t)
      + g3 * ky3 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
        (sol.x3 t) (sol.y3 t) = 0 := by
    have e12 := sol.hd12 t
    have e13 := sol.hd13 t
    have e23 := sol.hd23 t
    simp only [kx1, kx2, kx3, ky1, ky2, ky3]
    field_simp
    ring
  rw [hzero] at hsum
  exact hsum

/-- **Q is constant along any Kirchhoff solution.** -/
theorem Q_kirchhoff_conserved (g1 g2 g3 : ℝ) (sol : KirchhoffSol g1 g2 g3) (s t : ℝ) :
    Qvortex g1 g2 g3 (sol.y1 s) (sol.y2 s) (sol.y3 s)
      = Qvortex g1 g2 g3 (sol.y1 t) (sol.y2 t) (sol.y3 t) := by
  have h : ∀ u, HasDerivAt (fun r => Qvortex g1 g2 g3 (sol.y1 r) (sol.y2 r) (sol.y3 r)) 0 u :=
    fun u => Q_kirchhoff_deriv g1 g2 g3 sol u
  exact is_const_of_deriv_eq_zero (fun u => (h u).differentiableAt)
    (fun u => (h u).deriv) s t

/-! ### the angular impulse I is conserved -/

/-- **V3/V4 formal core, angular impulse.** Along any Kirchhoff solution
    the angular impulse I = ΣΓ|r|² has identically zero derivative. -/
theorem I_kirchhoff_deriv (g1 g2 g3 : ℝ) (sol : KirchhoffSol g1 g2 g3) (t : ℝ) :
    HasDerivAt (fun s => Ivortex g1 g2 g3 (sol.x1 s) (sol.y1 s)
      (sol.x2 s) (sol.y2 s) (sol.x3 s) (sol.y3 s)) 0 t := by
  have sq1 : HasDerivAt (fun s => sol.x1 s * sol.x1 s + sol.y1 s * sol.y1 s)
      (kx1 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t) * sol.x1 t
        + sol.x1 t * kx1 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t)
      + (ky1 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t) * sol.y1 t
        + sol.y1 t * ky1 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t)
          (sol.y3 t))) t :=
    ((sol.hx1 t).mul (sol.hx1 t)).add ((sol.hy1 t).mul (sol.hy1 t))
  have sq2 : HasDerivAt (fun s => sol.x2 s * sol.x2 s + sol.y2 s * sol.y2 s)
      (kx2 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t) * sol.x2 t
        + sol.x2 t * kx2 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t)
      + (ky2 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t) * sol.y2 t
        + sol.y2 t * ky2 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t)
          (sol.y3 t))) t :=
    ((sol.hx2 t).mul (sol.hx2 t)).add ((sol.hy2 t).mul (sol.hy2 t))
  have sq3 : HasDerivAt (fun s => sol.x3 s * sol.x3 s + sol.y3 s * sol.y3 s)
      (kx3 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t) * sol.x3 t
        + sol.x3 t * kx3 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t)
      + (ky3 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t) * sol.y3 t
        + sol.y3 t * ky3 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t)
          (sol.y3 t))) t :=
    ((sol.hx3 t).mul (sol.hx3 t)).add ((sol.hy3 t).mul (sol.hy3 t))
  have v1 := deriv_mul_const_left sq1 (c := g1)
  have v2 := deriv_mul_const_left sq2 (c := g2)
  have v3 := deriv_mul_const_left sq3 (c := g3)
  have hsum := (v1.add v2).add v3
  have hzero : g1 * (kx1 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
        (sol.x3 t) (sol.y3 t) * sol.x1 t + sol.x1 t * kx1 g1 g2 g3 (sol.x1 t) (sol.y1 t)
          (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t)
        + (ky1 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t)
          * sol.y1 t + sol.y1 t * ky1 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
            (sol.x3 t) (sol.y3 t)))
      + g2 * (kx2 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t)
        * sol.x2 t + sol.x2 t * kx2 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
          (sol.x3 t) (sol.y3 t)
        + (ky2 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t)
          * sol.y2 t + sol.y2 t * ky2 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
            (sol.x3 t) (sol.y3 t)))
      + g3 * (kx3 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t)
        * sol.x3 t + sol.x3 t * kx3 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
          (sol.x3 t) (sol.y3 t)
        + (ky3 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t)
          * sol.y3 t + sol.y3 t * ky3 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
            (sol.x3 t) (sol.y3 t))) = 0 := by
    have e12 := sol.hd12 t
    have e13 := sol.hd13 t
    have e23 := sol.hd23 t
    simp only [kx1, kx2, kx3, ky1, ky2, ky3]
    field_simp
    ring
  rw [hzero] at hsum
  exact deriv_congr hsum fun s => by unfold Ivortex; ring

/-- **I is constant along any Kirchhoff solution.** -/
theorem I_kirchhoff_conserved (g1 g2 g3 : ℝ) (sol : KirchhoffSol g1 g2 g3) (s t : ℝ) :
    Ivortex g1 g2 g3 (sol.x1 s) (sol.y1 s) (sol.x2 s) (sol.y2 s) (sol.x3 s) (sol.y3 s)
      = Ivortex g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
        (sol.x3 t) (sol.y3 t) := by
  have h : ∀ u, HasDerivAt (fun r => Ivortex g1 g2 g3 (sol.x1 r) (sol.y1 r)
      (sol.x2 r) (sol.y2 r) (sol.x3 r) (sol.y3 r)) 0 u :=
    fun u => I_kirchhoff_deriv g1 g2 g3 sol u
  exact is_const_of_deriv_eq_zero (fun u => (h u).differentiableAt)
    (fun u => (h u).deriv) s t

/-! ### the Hamiltonian H is conserved -/

/-- Differentiation of the logarithmic pair distance: if four coordinate
    functions are differentiable at t and the two points do not coincide,
    then d/dt ln r(t) = ((Δx)(Δẋ) + (Δy)(Δẏ))/r². -/
private theorem deriv_log_dist {a b c d : ℝ → ℝ} {a' b' c' d' t : ℝ}
    (ha : HasDerivAt a a' t) (hb : HasDerivAt b b' t)
    (hc : HasDerivAt c c' t) (hd : HasDerivAt d d' t)
    (hne : d2 (a t) (b t) (c t) (d t) ≠ 0) :
    HasDerivAt (fun s => Real.log (vortexDist (a s) (b s) (c s) (d s)))
      (((a t - c t) * (a' - c') + (b t - d t) * (b' - d'))
        / d2 (a t) (b t) (c t) (d t)) t := by
  have hpos : (0:ℝ) < d2 (a t) (b t) (c t) (d t) := by
    have hle : (0:ℝ) ≤ d2 (a t) (b t) (c t) (d t) := by
      unfold d2
      positivity
    rcases lt_or_eq_of_le hle with h | h
    · exact h
    · exact absurd h.symm hne
  have hsq : Real.sqrt (d2 (a t) (b t) (c t) (d t)) ≠ 0 := by
    intro h0
    exact hne (by rw [← Real.sq_sqrt hpos.le, h0]; ring)
  have hsubx := ha.sub hc
  have hsuby := hb.sub hd
  have hsqx := hsubx.mul hsubx
  have hsqy := hsuby.mul hsuby
  have hq := hsqx.add hsqy
  have hq2 : HasDerivAt (fun s => d2 (a s) (b s) (c s) (d s))
      ((a' - c') * (a t - c t) + (a t - c t) * (a' - c')
        + ((b' - d') * (b t - d t) + (b t - d t) * (b' - d'))) t :=
    deriv_congr hq fun s => by unfold d2; ring
  have hcomp : HasDerivAt (Real.log ∘ Real.sqrt)
      ((Real.sqrt (d2 (a t) (b t) (c t) (d t)))⁻¹
        * (1 / (2 * Real.sqrt (d2 (a t) (b t) (c t) (d t)))))
      (d2 (a t) (b t) (c t) (d t)) := by
    exact HasDerivAt.comp (𝕜 := ℝ) (d2 (a t) (b t) (c t) (d t))
      (Real.hasDerivAt_log hsq) (Real.hasDerivAt_sqrt hne)
  have hfinal : HasDerivAt ((Real.log ∘ Real.sqrt) ∘ fun s => d2 (a s) (b s) (c s) (d s))
      (((Real.sqrt (d2 (a t) (b t) (c t) (d t)))⁻¹
        * (1 / (2 * Real.sqrt (d2 (a t) (b t) (c t) (d t))))) *
        ((a' - c') * (a t - c t) + (a t - c t) * (a' - c')
          + ((b' - d') * (b t - d t) + (b t - d t) * (b' - d')))) t := by
    exact HasDerivAt.comp (𝕜 := ℝ) t hcomp hq2
  refine deriv_congr (hfinal.congr_deriv ?_) fun s => rfl
  have hsqD : (Real.sqrt (d2 (a t) (b t) (c t) (d t))) ^ 2
      = d2 (a t) (b t) (c t) (d t) := Real.sq_sqrt hpos.le
  field_simp [hsqD]
  linear_combination (-2) * (a' * a t - a' * c t - c' * a t + c' * c t
    + b' * b t - b' * d t - d' * b t + d' * d t) * hsqD

/-- **V3/V4 formal core, the Hamiltonian.** Along any Kirchhoff solution
    the vortex Hamiltonian H = −(1/2π)ΣΓᵢΓⱼ ln r_ij has identically zero
    derivative — the Kirchhoff system is its own Hamiltonian flow. -/
theorem H_kirchhoff_deriv (g1 g2 g3 : ℝ) (sol : KirchhoffSol g1 g2 g3) (t : ℝ) :
    HasDerivAt (fun s => Hvortex g1 g2 g3 (sol.x1 s) (sol.y1 s) (sol.x2 s) (sol.y2 s)
      (sol.x3 s) (sol.y3 s)) 0 t := by
  have hA := deriv_log_dist (sol.hx1 t) (sol.hy1 t) (sol.hx2 t) (sol.hy2 t) (sol.hd12 t)
  have hB := deriv_log_dist (sol.hx1 t) (sol.hy1 t) (sol.hx3 t) (sol.hy3 t) (sol.hd13 t)
  have hC := deriv_log_dist (sol.hx2 t) (sol.hy2 t) (sol.hx3 t) (sol.hy3 t) (sol.hd23 t)
  have vA := deriv_mul_const_left hA (c := g1 * g2)
  have vB := deriv_mul_const_left hB (c := g1 * g3)
  have vC := deriv_mul_const_left hC (c := g2 * g3)
  have hInner := (vA.add vB).add vC
  have hOuter := deriv_mul_const_left hInner (c := -(1 / (2 * Real.pi)))
  have hzero : -(1 / (2 * Real.pi)) * (g1 * g2 * (((sol.x1 t - sol.x2 t)
        * (kx1 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t)
          - kx2 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t))
        + (sol.y1 t - sol.y2 t) * (ky1 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
          (sol.x3 t) (sol.y3 t) - ky2 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
            (sol.x3 t) (sol.y3 t)))
        / d2 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t))
      + g1 * g3 * (((sol.x1 t - sol.x3 t)
        * (kx1 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t)
          - kx3 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t))
        + (sol.y1 t - sol.y3 t) * (ky1 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
          (sol.x3 t) (sol.y3 t) - ky3 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
            (sol.x3 t) (sol.y3 t)))
        / d2 (sol.x1 t) (sol.y1 t) (sol.x3 t) (sol.y3 t))
      + g2 * g3 * (((sol.x2 t - sol.x3 t)
        * (kx2 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t)
          - kx3 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t))
        + (sol.y2 t - sol.y3 t) * (ky2 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
          (sol.x3 t) (sol.y3 t) - ky3 g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
            (sol.x3 t) (sol.y3 t)))
        / d2 (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t))) = 0 := by
    have e12 := sol.hd12 t
    have e13 := sol.hd13 t
    have e23 := sol.hd23 t
    simp only [kx1, kx2, kx3, ky1, ky2, ky3]
    field_simp
    ring
  rw [hzero] at hOuter
  exact hOuter

/-- **H is constant along any Kirchhoff solution.** -/
theorem H_kirchhoff_conserved (g1 g2 g3 : ℝ) (sol : KirchhoffSol g1 g2 g3) (s t : ℝ) :
    Hvortex g1 g2 g3 (sol.x1 s) (sol.y1 s) (sol.x2 s) (sol.y2 s) (sol.x3 s) (sol.y3 s)
      = Hvortex g1 g2 g3 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
        (sol.x3 t) (sol.y3 t) := by
  have h : ∀ u, HasDerivAt (fun r => Hvortex g1 g2 g3 (sol.x1 r) (sol.y1 r)
      (sol.x2 r) (sol.y2 r) (sol.x3 r) (sol.y3 r)) 0 u :=
    fun u => H_kirchhoff_deriv g1 g2 g3 sol u
  exact is_const_of_deriv_eq_zero (fun u => (h u).differentiableAt)
    (fun u => (h u).deriv) s t

/-! ## Section 6 — the Lagrange equilateral solution -/

/-! The point-vortex twin of the classical Lagrange solution: three equal
    vortices on the vertices of an equilateral triangle of side a,
    rotating rigidly at ω = 3Γ/(2πa²). This section proves that the
    rotation at exactly this frequency is a Kirchhoff solution — the
    analytic core of check V2 — and that the equilateral anchor values
    of Section 3 therefore hold along it for all time. -/

private theorem cos_two_pi_div_three : Real.cos (2 * Real.pi / 3) = -(1 / 2) := by
  have h3 : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  rw [show (2 * Real.pi / 3 : ℝ) = Real.pi / 3 + Real.pi / 3 from by ring, Real.cos_add,
      Real.cos_pi_div_three, Real.sin_pi_div_three]
  linear_combination (-1 / 4) * h3

private theorem sin_two_pi_div_three : Real.sin (2 * Real.pi / 3) = Real.sqrt 3 / 2 := by
  rw [show (2 * Real.pi / 3 : ℝ) = Real.pi / 3 + Real.pi / 3 from by ring, Real.sin_add,
      Real.sin_pi_div_three, Real.cos_pi_div_three]
  ring

private theorem cos_four_pi_div_three : Real.cos (4 * Real.pi / 3) = -(1 / 2) := by
  have h3 : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  rw [show (4 * Real.pi / 3 : ℝ) = 2 * Real.pi / 3 + 2 * Real.pi / 3 from by ring,
      Real.cos_add, cos_two_pi_div_three, sin_two_pi_div_three]
  linear_combination (-1 / 4) * h3

private theorem sin_four_pi_div_three : Real.sin (4 * Real.pi / 3) = -(Real.sqrt 3 / 2) := by
  rw [show (4 * Real.pi / 3 : ℝ) = 2 * Real.pi / 3 + 2 * Real.pi / 3 from by ring,
      Real.sin_add, cos_two_pi_div_three, sin_two_pi_div_three]
  ring

private theorem phase0_eq (ω t : ℝ) : ω * t + 2 * Real.pi * (0:ℕ) / 3 = ω * t := by
  push_cast
  ring

private theorem phase1_eq (ω t : ℝ) :
    ω * t + 2 * Real.pi * (1:ℕ) / 3 = ω * t + 2 * Real.pi / 3 := by
  push_cast
  ring

private theorem phase2_eq (ω t : ℝ) :
    ω * t + 2 * Real.pi * (2:ℕ) / 3 = ω * t + 4 * Real.pi / 3 := by
  push_cast
  ring

/-- The x-coordinate of the k-th vortex of the rotating triangle:
    (a/√3)·cos(ω·t + 2πk/3). -/
noncomputable def lagX (a ω t : ℝ) (k : ℕ) : ℝ :=
  (a / Real.sqrt 3) * Real.cos (ω * t + 2 * Real.pi * k / 3)

/-- The y-coordinate of the k-th vortex of the rotating triangle. -/
noncomputable def lagY (a ω t : ℝ) (k : ℕ) : ℝ :=
  (a / Real.sqrt 3) * Real.sin (ω * t + 2 * Real.pi * k / 3)

private theorem sin_sum (u : ℝ) :
    Real.sin u + Real.sin (u + 2 * Real.pi / 3) + Real.sin (u + 4 * Real.pi / 3) = 0 := by
  have h3 : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  rw [show u + 4 * Real.pi / 3 = (u + 2 * Real.pi / 3) + 2 * Real.pi / 3 from by ring,
      Real.sin_add (u + 2 * Real.pi / 3) (2 * Real.pi / 3), Real.sin_add u (2 * Real.pi / 3),
      Real.cos_add u (2 * Real.pi / 3), sin_two_pi_div_three, cos_two_pi_div_three]
  linear_combination (-Real.sin u / 4) * h3

private theorem cos_sum (u : ℝ) :
    Real.cos u + Real.cos (u + 2 * Real.pi / 3) + Real.cos (u + 4 * Real.pi / 3) = 0 := by
  have h3 : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  rw [show u + 4 * Real.pi / 3 = (u + 2 * Real.pi / 3) + 2 * Real.pi / 3 from by ring,
      Real.cos_add (u + 2 * Real.pi / 3) (2 * Real.pi / 3), Real.cos_add u (2 * Real.pi / 3),
      Real.sin_add u (2 * Real.pi / 3), sin_two_pi_div_three, cos_two_pi_div_three]
  linear_combination (-Real.cos u / 4) * h3

private theorem trig_pair_dist (u v : ℝ) :
    (Real.cos u - Real.cos v) ^ 2 + (Real.sin u - Real.sin v) ^ 2
      = 2 - 2 * Real.cos (u - v) := by
  have h1 : Real.sin u ^ 2 + Real.cos u ^ 2 = 1 := Real.sin_sq_add_cos_sq u
  have h2 : Real.sin v ^ 2 + Real.cos v ^ 2 = 1 := Real.sin_sq_add_cos_sq v
  have h3 : Real.cos u * Real.cos v + Real.sin u * Real.sin v = Real.cos (u - v) := by
    rw [← Real.cos_sub]
  have hexp : (Real.cos u - Real.cos v) ^ 2 + (Real.sin u - Real.sin v) ^ 2
      = (Real.sin u ^ 2 + Real.cos u ^ 2) + (Real.sin v ^ 2 + Real.cos v ^ 2)
        - 2 * (Real.cos u * Real.cos v + Real.sin u * Real.sin v) := by ring
  rw [hexp, h1, h2, h3]
  ring

/-- **The rotating triangle is equilateral for all t.** Every pairwise
    squared distance is exactly a² (pair 0,1). -/
theorem d2_lag01 (a ω t : ℝ) :
    d2 (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1) = a ^ 2 := by
  have h3 : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hcos : Real.cos (ω * t - (ω * t + 2 * Real.pi / 3)) = -(1 / 2) := by
    rw [show ω * t - (ω * t + 2 * Real.pi / 3) = -(2 * Real.pi / 3) from by ring,
      Real.cos_neg, cos_two_pi_div_three]
  have hs2 : Real.sqrt 3 * Real.sqrt 3 = 3 := by linear_combination h3
  have hcc : (a / Real.sqrt 3) * (a / Real.sqrt 3) = a ^ 2 / 3 := by
    rw [show (a / Real.sqrt 3) * (a / Real.sqrt 3)
        = a * a / (Real.sqrt 3 * Real.sqrt 3) from by ring, hs2]
    ring
  unfold d2 lagX lagY
  rw [phase0_eq, phase1_eq]
  have hexp : ((a / Real.sqrt 3) * Real.cos (ω * t) - (a / Real.sqrt 3)
        * Real.cos (ω * t + 2 * Real.pi / 3)) ^ 2
      + ((a / Real.sqrt 3) * Real.sin (ω * t) - (a / Real.sqrt 3)
        * Real.sin (ω * t + 2 * Real.pi / 3)) ^ 2
      = (a / Real.sqrt 3) * (a / Real.sqrt 3)
        * ((Real.cos (ω * t) - Real.cos (ω * t + 2 * Real.pi / 3)) ^ 2
          + (Real.sin (ω * t) - Real.sin (ω * t + 2 * Real.pi / 3)) ^ 2) := by ring
  rw [hexp, trig_pair_dist, hcos, hcc]
  ring

/-- Pairwise squared distance of the rotating triangle (pair 1,2). -/
theorem d2_lag12 (a ω t : ℝ) :
    d2 (lagX a ω t 1) (lagY a ω t 1) (lagX a ω t 2) (lagY a ω t 2) = a ^ 2 := by
  have h3 : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hcos : Real.cos ((ω * t + 2 * Real.pi / 3) - (ω * t + 4 * Real.pi / 3)) = -(1 / 2) := by
    rw [show (ω * t + 2 * Real.pi / 3) - (ω * t + 4 * Real.pi / 3)
        = -(2 * Real.pi / 3) from by ring, Real.cos_neg, cos_two_pi_div_three]
  have hs2 : Real.sqrt 3 * Real.sqrt 3 = 3 := by linear_combination h3
  have hcc : (a / Real.sqrt 3) * (a / Real.sqrt 3) = a ^ 2 / 3 := by
    rw [show (a / Real.sqrt 3) * (a / Real.sqrt 3)
        = a * a / (Real.sqrt 3 * Real.sqrt 3) from by ring, hs2]
    ring
  unfold d2 lagX lagY
  rw [phase1_eq, phase2_eq]
  have hexp : ((a / Real.sqrt 3) * Real.cos (ω * t + 2 * Real.pi / 3) - (a / Real.sqrt 3)
        * Real.cos (ω * t + 4 * Real.pi / 3)) ^ 2
      + ((a / Real.sqrt 3) * Real.sin (ω * t + 2 * Real.pi / 3) - (a / Real.sqrt 3)
        * Real.sin (ω * t + 4 * Real.pi / 3)) ^ 2
      = (a / Real.sqrt 3) * (a / Real.sqrt 3)
        * ((Real.cos (ω * t + 2 * Real.pi / 3) - Real.cos (ω * t + 4 * Real.pi / 3)) ^ 2
          + (Real.sin (ω * t + 2 * Real.pi / 3) - Real.sin (ω * t + 4 * Real.pi / 3)) ^ 2) := by
    ring
  rw [hexp, trig_pair_dist, hcos, hcc]
  ring

/-- Pairwise squared distance of the rotating triangle (pair 0,2). -/
theorem d2_lag02 (a ω t : ℝ) :
    d2 (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 2) (lagY a ω t 2) = a ^ 2 := by
  have h3 : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hcos : Real.cos (ω * t - (ω * t + 4 * Real.pi / 3)) = -(1 / 2) := by
    rw [show ω * t - (ω * t + 4 * Real.pi / 3) = -(4 * Real.pi / 3) from by ring,
      Real.cos_neg, cos_four_pi_div_three]
  have hs2 : Real.sqrt 3 * Real.sqrt 3 = 3 := by linear_combination h3
  have hcc : (a / Real.sqrt 3) * (a / Real.sqrt 3) = a ^ 2 / 3 := by
    rw [show (a / Real.sqrt 3) * (a / Real.sqrt 3)
        = a * a / (Real.sqrt 3 * Real.sqrt 3) from by ring, hs2]
    ring
  unfold d2 lagX lagY
  rw [phase0_eq, phase2_eq]
  have hexp : ((a / Real.sqrt 3) * Real.cos (ω * t) - (a / Real.sqrt 3)
        * Real.cos (ω * t + 4 * Real.pi / 3)) ^ 2
      + ((a / Real.sqrt 3) * Real.sin (ω * t) - (a / Real.sqrt 3)
        * Real.sin (ω * t + 4 * Real.pi / 3)) ^ 2
      = (a / Real.sqrt 3) * (a / Real.sqrt 3)
        * ((Real.cos (ω * t) - Real.cos (ω * t + 4 * Real.pi / 3)) ^ 2
          + (Real.sin (ω * t) - Real.sin (ω * t + 4 * Real.pi / 3)) ^ 2) := by
    ring
  rw [hexp, trig_pair_dist, hcos, hcc]
  ring

/-- The centroid of the rotating triangle stays at the origin (x-parts). -/
theorem lagX_sum (a ω t : ℝ) :
    lagX a ω t 0 + lagX a ω t 1 + lagX a ω t 2 = 0 := by
  have hc := cos_sum (ω * t)
  unfold lagX
  rw [phase0_eq, phase1_eq, phase2_eq]
  linear_combination (a / Real.sqrt 3) * hc

/-- The centroid of the rotating triangle stays at the origin (y-parts). -/
theorem lagY_sum (a ω t : ℝ) :
    lagY a ω t 0 + lagY a ω t 1 + lagY a ω t 2 = 0 := by
  have hs := sin_sum (ω * t)
  unfold lagY
  rw [phase0_eq, phase1_eq, phase2_eq]
  linear_combination (a / Real.sqrt 3) * hs

/-- Kinematics of the rotating triangle: ẋ_k = −ω·(a/√3)·sin(phase_k). -/
theorem lagX_deriv (a ω t : ℝ) (k : ℕ) :
    HasDerivAt (fun s => lagX a ω s k)
      (-(a / Real.sqrt 3) * (ω * Real.sin (ω * t + 2 * Real.pi * k / 3))) t := by
  have hlin : HasDerivAt (fun s => ω * s + 2 * Real.pi * k / 3) ω t := by
    have hmul : HasDerivAt (fun s => ω * s) ω t :=
      ((hasDerivAt_const (c := ω) (x := t)).mul
        (hasDerivAt_id (𝕜 := ℝ) (x := t))).congr_deriv (by ring)
    exact (hmul.add (hasDerivAt_const (c := 2 * Real.pi * k / 3) (x := t))).congr_deriv (by ring)
  have hcos' : HasDerivAt (fun s => Real.cos (ω * s + 2 * Real.pi * k / 3))
      (-(Real.sin (ω * t + 2 * Real.pi * k / 3)) * ω) t :=
    HasDerivAt.comp (𝕜 := ℝ) t (Real.hasDerivAt_cos (ω * t + 2 * Real.pi * k / 3)) hlin
  exact (deriv_mul_const_left hcos' (c := a / Real.sqrt 3)).congr_deriv (by ring)

/-- Kinematics of the rotating triangle: ẏ_k = ω·(a/√3)·cos(phase_k). -/
theorem lagY_deriv (a ω t : ℝ) (k : ℕ) :
    HasDerivAt (fun s => lagY a ω s k)
      ((a / Real.sqrt 3) * (ω * Real.cos (ω * t + 2 * Real.pi * k / 3))) t := by
  have hlin : HasDerivAt (fun s => ω * s + 2 * Real.pi * k / 3) ω t := by
    have hmul : HasDerivAt (fun s => ω * s) ω t :=
      ((hasDerivAt_const (c := ω) (x := t)).mul
        (hasDerivAt_id (𝕜 := ℝ) (x := t))).congr_deriv (by ring)
    exact (hmul.add (hasDerivAt_const (c := 2 * Real.pi * k / 3) (x := t))).congr_deriv (by ring)
  have hsin' : HasDerivAt (fun s => Real.sin (ω * s + 2 * Real.pi * k / 3))
      (Real.cos (ω * t + 2 * Real.pi * k / 3) * ω) t :=
    HasDerivAt.comp (𝕜 := ℝ) t (Real.hasDerivAt_sin (ω * t + 2 * Real.pi * k / 3)) hlin
  exact (deriv_mul_const_left hsin' (c := a / Real.sqrt 3)).congr_deriv (by ring)

/-- **Kirchhoff velocity of vortex 0 matches the rigid rotation.** -/
theorem lag_kx0 (g a : ℝ) (ha : 0 < a) (ω t : ℝ) (hw : ω = lagrangeOmega g a) :
    kx1 g g g (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1)
      (lagX a ω t 2) (lagY a ω t 2)
      = -(a / Real.sqrt 3) * (ω * Real.sin (ω * t)) := by
  have hd1 : d2 (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1) = a ^ 2 :=
    d2_lag01 a ω t
  have hd2 : d2 (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 2) (lagY a ω t 2) = a ^ 2 :=
    d2_lag02 a ω t
  have hs := lagY_sum a ω t
  have hsum : g * (lagY a ω t 0 - lagY a ω t 1) + g * (lagY a ω t 0 - lagY a ω t 2)
      = 3 * g * lagY a ω t 0 := by
    linear_combination (-g) * hs
  have hstep : g * (lagY a ω t 0 - lagY a ω t 1) / a ^ 2
      + g * (lagY a ω t 0 - lagY a ω t 2) / a ^ 2
      = 3 * g * lagY a ω t 0 / a ^ 2 := by
    rw [show g * (lagY a ω t 0 - lagY a ω t 1) / a ^ 2
        + g * (lagY a ω t 0 - lagY a ω t 2) / a ^ 2
        = (g * (lagY a ω t 0 - lagY a ω t 1) + g * (lagY a ω t 0 - lagY a ω t 2)) / a ^ 2 from by
        ring, hsum]
  unfold kx1
  rw [hd1, hd2, hstep]
  unfold lagY
  rw [phase0_eq, hw]
  unfold lagrangeOmega
  ring

/-- **Kirchhoff velocity of vortex 1 matches the rigid rotation.** -/
theorem lag_kx1 (g a : ℝ) (ha : 0 < a) (ω t : ℝ) (hw : ω = lagrangeOmega g a) :
    kx2 g g g (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1)
      (lagX a ω t 2) (lagY a ω t 2)
      = -(a / Real.sqrt 3) * (ω * Real.sin (ω * t + 2 * Real.pi / 3)) := by
  have hd1 : d2 (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1) = a ^ 2 :=
    d2_lag01 a ω t
  have hd2 : d2 (lagX a ω t 1) (lagY a ω t 1) (lagX a ω t 2) (lagY a ω t 2) = a ^ 2 :=
    d2_lag12 a ω t
  have hs := lagY_sum a ω t
  have hsum : g * (lagY a ω t 1 - lagY a ω t 0) + g * (lagY a ω t 1 - lagY a ω t 2)
      = 3 * g * lagY a ω t 1 := by
    linear_combination (-g) * hs
  have hstep : g * (lagY a ω t 1 - lagY a ω t 0) / a ^ 2
      + g * (lagY a ω t 1 - lagY a ω t 2) / a ^ 2
      = 3 * g * lagY a ω t 1 / a ^ 2 := by
    rw [show g * (lagY a ω t 1 - lagY a ω t 0) / a ^ 2
        + g * (lagY a ω t 1 - lagY a ω t 2) / a ^ 2
        = (g * (lagY a ω t 1 - lagY a ω t 0) + g * (lagY a ω t 1 - lagY a ω t 2)) / a ^ 2 from by
        ring, hsum]
  unfold kx2
  rw [hd1, hd2, hstep]
  unfold lagY
  rw [phase1_eq, hw]
  unfold lagrangeOmega
  ring

/-- **Kirchhoff velocity of vortex 2 matches the rigid rotation.** -/
theorem lag_kx2 (g a : ℝ) (ha : 0 < a) (ω t : ℝ) (hw : ω = lagrangeOmega g a) :
    kx3 g g g (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1)
      (lagX a ω t 2) (lagY a ω t 2)
      = -(a / Real.sqrt 3) * (ω * Real.sin (ω * t + 4 * Real.pi / 3)) := by
  have hd1 : d2 (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 2) (lagY a ω t 2) = a ^ 2 :=
    d2_lag02 a ω t
  have hd2 : d2 (lagX a ω t 1) (lagY a ω t 1) (lagX a ω t 2) (lagY a ω t 2) = a ^ 2 :=
    d2_lag12 a ω t
  have hs := lagY_sum a ω t
  have hsum : g * (lagY a ω t 2 - lagY a ω t 0) + g * (lagY a ω t 2 - lagY a ω t 1)
      = 3 * g * lagY a ω t 2 := by
    linear_combination (-g) * hs
  have hstep : g * (lagY a ω t 2 - lagY a ω t 0) / a ^ 2
      + g * (lagY a ω t 2 - lagY a ω t 1) / a ^ 2
      = 3 * g * lagY a ω t 2 / a ^ 2 := by
    rw [show g * (lagY a ω t 2 - lagY a ω t 0) / a ^ 2
        + g * (lagY a ω t 2 - lagY a ω t 1) / a ^ 2
        = (g * (lagY a ω t 2 - lagY a ω t 0) + g * (lagY a ω t 2 - lagY a ω t 1)) / a ^ 2 from by
        ring, hsum]
  unfold kx3
  rw [hd1, hd2, hstep]
  unfold lagY
  rw [phase2_eq, hw]
  unfold lagrangeOmega
  ring

/-- **Kirchhoff y-velocity of vortex 0 matches the rigid rotation.** -/
theorem lag_ky0 (g a : ℝ) (ha : 0 < a) (ω t : ℝ) (hw : ω = lagrangeOmega g a) :
    ky1 g g g (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1)
      (lagX a ω t 2) (lagY a ω t 2)
      = (a / Real.sqrt 3) * (ω * Real.cos (ω * t)) := by
  have hd1 : d2 (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1) = a ^ 2 :=
    d2_lag01 a ω t
  have hd2 : d2 (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 2) (lagY a ω t 2) = a ^ 2 :=
    d2_lag02 a ω t
  have hc := lagX_sum a ω t
  have hsum : g * (lagX a ω t 0 - lagX a ω t 1) + g * (lagX a ω t 0 - lagX a ω t 2)
      = 3 * g * lagX a ω t 0 := by
    linear_combination (-g) * hc
  have hstep : g * (lagX a ω t 0 - lagX a ω t 1) / a ^ 2
      + g * (lagX a ω t 0 - lagX a ω t 2) / a ^ 2
      = 3 * g * lagX a ω t 0 / a ^ 2 := by
    rw [show g * (lagX a ω t 0 - lagX a ω t 1) / a ^ 2
        + g * (lagX a ω t 0 - lagX a ω t 2) / a ^ 2
        = (g * (lagX a ω t 0 - lagX a ω t 1) + g * (lagX a ω t 0 - lagX a ω t 2)) / a ^ 2 from by
        ring, hsum]
  unfold ky1
  rw [hd1, hd2, hstep]
  unfold lagX
  rw [phase0_eq, hw]
  unfold lagrangeOmega
  ring

/-- **Kirchhoff y-velocity of vortex 1 matches the rigid rotation.** -/
theorem lag_ky1 (g a : ℝ) (ha : 0 < a) (ω t : ℝ) (hw : ω = lagrangeOmega g a) :
    ky2 g g g (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1)
      (lagX a ω t 2) (lagY a ω t 2)
      = (a / Real.sqrt 3) * (ω * Real.cos (ω * t + 2 * Real.pi / 3)) := by
  have hd1 : d2 (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1) = a ^ 2 :=
    d2_lag01 a ω t
  have hd2 : d2 (lagX a ω t 1) (lagY a ω t 1) (lagX a ω t 2) (lagY a ω t 2) = a ^ 2 :=
    d2_lag12 a ω t
  have hc := lagX_sum a ω t
  have hsum : g * (lagX a ω t 1 - lagX a ω t 0) + g * (lagX a ω t 1 - lagX a ω t 2)
      = 3 * g * lagX a ω t 1 := by
    linear_combination (-g) * hc
  have hstep : g * (lagX a ω t 1 - lagX a ω t 0) / a ^ 2
      + g * (lagX a ω t 1 - lagX a ω t 2) / a ^ 2
      = 3 * g * lagX a ω t 1 / a ^ 2 := by
    rw [show g * (lagX a ω t 1 - lagX a ω t 0) / a ^ 2
        + g * (lagX a ω t 1 - lagX a ω t 2) / a ^ 2
        = (g * (lagX a ω t 1 - lagX a ω t 0) + g * (lagX a ω t 1 - lagX a ω t 2)) / a ^ 2 from by
        ring, hsum]
  unfold ky2
  rw [hd1, hd2, hstep]
  unfold lagX
  rw [phase1_eq, hw]
  unfold lagrangeOmega
  ring

/-- **Kirchhoff y-velocity of vortex 2 matches the rigid rotation.** -/
theorem lag_ky2 (g a : ℝ) (ha : 0 < a) (ω t : ℝ) (hw : ω = lagrangeOmega g a) :
    ky3 g g g (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1)
      (lagX a ω t 2) (lagY a ω t 2)
      = (a / Real.sqrt 3) * (ω * Real.cos (ω * t + 4 * Real.pi / 3)) := by
  have hd1 : d2 (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 2) (lagY a ω t 2) = a ^ 2 :=
    d2_lag02 a ω t
  have hd2 : d2 (lagX a ω t 1) (lagY a ω t 1) (lagX a ω t 2) (lagY a ω t 2) = a ^ 2 :=
    d2_lag12 a ω t
  have hc := lagX_sum a ω t
  have hsum : g * (lagX a ω t 2 - lagX a ω t 0) + g * (lagX a ω t 2 - lagX a ω t 1)
      = 3 * g * lagX a ω t 2 := by
    linear_combination (-g) * hc
  have hstep : g * (lagX a ω t 2 - lagX a ω t 0) / a ^ 2
      + g * (lagX a ω t 2 - lagX a ω t 1) / a ^ 2
      = 3 * g * lagX a ω t 2 / a ^ 2 := by
    rw [show g * (lagX a ω t 2 - lagX a ω t 0) / a ^ 2
        + g * (lagX a ω t 2 - lagX a ω t 1) / a ^ 2
        = (g * (lagX a ω t 2 - lagX a ω t 0) + g * (lagX a ω t 2 - lagX a ω t 1)) / a ^ 2 from by
        ring, hsum]
  unfold ky3
  rw [hd1, hd2, hstep]
  unfold lagX
  rw [phase2_eq, hw]
  unfold lagrangeOmega
  ring

/-- **THE LAGRANGE EQUILATERAL SOLUTION (V2 formal core).**
    Three equal vortices placed on a rotating equilateral triangle of
    side a with angular velocity ω = 3Γ/(2πa²) form an exact Kirchhoff
    solution — the point-vortex twin of the classical Lagrange solution
    of the three-body problem. -/
noncomputable def lagrangeSol (g a : ℝ) (ha : 0 < a) : KirchhoffSol g g g where
  x1 := fun s => lagX a (lagrangeOmega g a) s 0
  y1 := fun s => lagY a (lagrangeOmega g a) s 0
  x2 := fun s => lagX a (lagrangeOmega g a) s 1
  y2 := fun s => lagY a (lagrangeOmega g a) s 1
  x3 := fun s => lagX a (lagrangeOmega g a) s 2
  y3 := fun s => lagY a (lagrangeOmega g a) s 2
  hx1 := fun t => by
    have hd := lagX_deriv a (lagrangeOmega g a) t 0
    exact hd.congr_deriv (by rw [phase0_eq, lag_kx0 g a ha (lagrangeOmega g a) t rfl])
  hy1 := fun t => by
    have hd := lagY_deriv a (lagrangeOmega g a) t 0
    refine hd.congr_deriv ?_
    rw [phase0_eq, lag_ky0 g a ha (lagrangeOmega g a) t rfl]
  hx2 := fun t => by
    have hd := lagX_deriv a (lagrangeOmega g a) t 1
    exact hd.congr_deriv (by rw [phase1_eq, lag_kx1 g a ha (lagrangeOmega g a) t rfl])
  hy2 := fun t => by
    have hd := lagY_deriv a (lagrangeOmega g a) t 1
    refine hd.congr_deriv ?_
    rw [phase1_eq, lag_ky1 g a ha (lagrangeOmega g a) t rfl]
  hx3 := fun t => by
    have hd := lagX_deriv a (lagrangeOmega g a) t 2
    exact hd.congr_deriv (by rw [phase2_eq, lag_kx2 g a ha (lagrangeOmega g a) t rfl])
  hy3 := fun t => by
    have hd := lagY_deriv a (lagrangeOmega g a) t 2
    refine hd.congr_deriv ?_
    rw [phase2_eq, lag_ky2 g a ha (lagrangeOmega g a) t rfl]
  hd12 := fun t => by
    show d2 (lagX a (lagrangeOmega g a) t 0) (lagY a (lagrangeOmega g a) t 0)
      (lagX a (lagrangeOmega g a) t 1) (lagY a (lagrangeOmega g a) t 1) ≠ 0
    rw [d2_lag01 a (lagrangeOmega g a) t]
    positivity
  hd13 := fun t => by
    show d2 (lagX a (lagrangeOmega g a) t 0) (lagY a (lagrangeOmega g a) t 0)
      (lagX a (lagrangeOmega g a) t 2) (lagY a (lagrangeOmega g a) t 2) ≠ 0
    rw [d2_lag02 a (lagrangeOmega g a) t]
    positivity
  hd23 := fun t => by
    show d2 (lagX a (lagrangeOmega g a) t 1) (lagY a (lagrangeOmega g a) t 1)
      (lagX a (lagrangeOmega g a) t 2) (lagY a (lagrangeOmega g a) t 2) ≠ 0
    rw [d2_lag12 a (lagrangeOmega g a) t]
    positivity

/-! ### the anchors hold along the Lagrange solution for all time -/

private theorem lagX0_eq1 (ω : ℝ) : lagX 1 ω 0 0 = eqX1 := by
  unfold lagX eqX1
  rw [phase0_eq, mul_zero, Real.cos_zero]
  ring

private theorem lagY0_eq1 (ω : ℝ) : lagY 1 ω 0 0 = eqY1 := by
  unfold lagY eqY1
  rw [phase0_eq, mul_zero, Real.sin_zero]
  ring

private theorem lagX0_eq2 (ω : ℝ) : lagX 1 ω 0 1 = eqX2 := by
  unfold lagX eqX2
  rw [phase1_eq, mul_zero, zero_add, cos_two_pi_div_three]
  ring

private theorem lagY0_eq2 (ω : ℝ) : lagY 1 ω 0 1 = eqY2 := by
  unfold lagY eqY2
  rw [phase1_eq, mul_zero, zero_add, sin_two_pi_div_three]
  field_simp

private theorem lagX0_eq3 (ω : ℝ) : lagX 1 ω 0 2 = eqX3 := by
  unfold lagX eqX3
  rw [phase2_eq, mul_zero, zero_add, cos_four_pi_div_three]
  ring

private theorem lagY0_eq3 (ω : ℝ) : lagY 1 ω 0 2 = eqY3 := by
  unfold lagY eqY3
  rw [phase2_eq, mul_zero, zero_add, sin_four_pi_div_three]
  field_simp

/-- **The Hamiltonian stays exactly 0 along the rotating solution**
    (side a = 1, equal circulations): the Section 3 anchor is a
    statement about ALL times, not just t = 0. -/
theorem lagrange_anchor_H (g t : ℝ) :
    Hvortex g g g (lagX 1 (lagrangeOmega g 1) t 0) (lagY 1 (lagrangeOmega g 1) t 0)
      (lagX 1 (lagrangeOmega g 1) t 1) (lagY 1 (lagrangeOmega g 1) t 1)
      (lagX 1 (lagrangeOmega g 1) t 2) (lagY 1 (lagrangeOmega g 1) t 2) = 0 := by
  have hc : Hvortex g g g (lagX 1 (lagrangeOmega g 1) t 0) (lagY 1 (lagrangeOmega g 1) t 0)
      (lagX 1 (lagrangeOmega g 1) t 1) (lagY 1 (lagrangeOmega g 1) t 1)
      (lagX 1 (lagrangeOmega g 1) t 2) (lagY 1 (lagrangeOmega g 1) t 2)
      = Hvortex g g g (lagX 1 (lagrangeOmega g 1) 0 0) (lagY 1 (lagrangeOmega g 1) 0 0)
      (lagX 1 (lagrangeOmega g 1) 0 1) (lagY 1 (lagrangeOmega g 1) 0 1)
      (lagX 1 (lagrangeOmega g 1) 0 2) (lagY 1 (lagrangeOmega g 1) 0 2) :=
    H_kirchhoff_conserved g g g (lagrangeSol g 1 (by norm_num)) t 0
  have h0 : Hvortex g g g (lagX 1 (lagrangeOmega g 1) 0 0) (lagY 1 (lagrangeOmega g 1) 0 0)
      (lagX 1 (lagrangeOmega g 1) 0 1) (lagY 1 (lagrangeOmega g 1) 0 1)
      (lagX 1 (lagrangeOmega g 1) 0 2) (lagY 1 (lagrangeOmega g 1) 0 2) = 0 := by
    rw [lagX0_eq1, lagY0_eq1, lagX0_eq2, lagY0_eq2, lagX0_eq3, lagY0_eq3]
    exact H_equilateral g
  exact hc.trans h0

/-- **The impulse P stays exactly 0 along the rotating solution.** -/
theorem lagrange_anchor_P (g t : ℝ) :
    Pvortex g g g (lagX 1 (lagrangeOmega g 1) t 0) (lagX 1 (lagrangeOmega g 1) t 1)
      (lagX 1 (lagrangeOmega g 1) t 2) = 0 := by
  have hc : Pvortex g g g (lagX 1 (lagrangeOmega g 1) t 0) (lagX 1 (lagrangeOmega g 1) t 1)
      (lagX 1 (lagrangeOmega g 1) t 2)
      = Pvortex g g g (lagX 1 (lagrangeOmega g 1) 0 0) (lagX 1 (lagrangeOmega g 1) 0 1)
      (lagX 1 (lagrangeOmega g 1) 0 2) :=
    P_kirchhoff_conserved g g g (lagrangeSol g 1 (by norm_num)) t 0
  have h0 : Pvortex g g g (lagX 1 (lagrangeOmega g 1) 0 0) (lagX 1 (lagrangeOmega g 1) 0 1)
      (lagX 1 (lagrangeOmega g 1) 0 2) = 0 := by
    rw [lagX0_eq1, lagX0_eq2, lagX0_eq3]
    exact P_equilateral g
  exact hc.trans h0

/-- **The impulse Q stays exactly 0 along the rotating solution.** -/
theorem lagrange_anchor_Q (g t : ℝ) :
    Qvortex g g g (lagY 1 (lagrangeOmega g 1) t 0) (lagY 1 (lagrangeOmega g 1) t 1)
      (lagY 1 (lagrangeOmega g 1) t 2) = 0 := by
  have hc : Qvortex g g g (lagY 1 (lagrangeOmega g 1) t 0) (lagY 1 (lagrangeOmega g 1) t 1)
      (lagY 1 (lagrangeOmega g 1) t 2)
      = Qvortex g g g (lagY 1 (lagrangeOmega g 1) 0 0) (lagY 1 (lagrangeOmega g 1) 0 1)
      (lagY 1 (lagrangeOmega g 1) 0 2) :=
    Q_kirchhoff_conserved g g g (lagrangeSol g 1 (by norm_num)) t 0
  have h0 : Qvortex g g g (lagY 1 (lagrangeOmega g 1) 0 0) (lagY 1 (lagrangeOmega g 1) 0 1)
      (lagY 1 (lagrangeOmega g 1) 0 2) = 0 := by
    rw [lagY0_eq1, lagY0_eq2, lagY0_eq3]
    exact Q_equilateral g
  exact hc.trans h0

/-- **The angular impulse stays exactly Γ along the rotating solution.** -/
theorem lagrange_anchor_I (g t : ℝ) :
    Ivortex g g g (lagX 1 (lagrangeOmega g 1) t 0) (lagY 1 (lagrangeOmega g 1) t 0)
      (lagX 1 (lagrangeOmega g 1) t 1) (lagY 1 (lagrangeOmega g 1) t 1)
      (lagX 1 (lagrangeOmega g 1) t 2) (lagY 1 (lagrangeOmega g 1) t 2) = g := by
  have hc : Ivortex g g g (lagX 1 (lagrangeOmega g 1) t 0) (lagY 1 (lagrangeOmega g 1) t 0)
      (lagX 1 (lagrangeOmega g 1) t 1) (lagY 1 (lagrangeOmega g 1) t 1)
      (lagX 1 (lagrangeOmega g 1) t 2) (lagY 1 (lagrangeOmega g 1) t 2)
      = Ivortex g g g (lagX 1 (lagrangeOmega g 1) 0 0) (lagY 1 (lagrangeOmega g 1) 0 0)
      (lagX 1 (lagrangeOmega g 1) 0 1) (lagY 1 (lagrangeOmega g 1) 0 1)
      (lagX 1 (lagrangeOmega g 1) 0 2) (lagY 1 (lagrangeOmega g 1) 0 2) :=
    I_kirchhoff_conserved g g g (lagrangeSol g 1 (by norm_num)) t 0
  have h0 : Ivortex g g g (lagX 1 (lagrangeOmega g 1) 0 0) (lagY 1 (lagrangeOmega g 1) 0 0)
      (lagX 1 (lagrangeOmega g 1) 0 1) (lagY 1 (lagrangeOmega g 1) 0 1)
      (lagX 1 (lagrangeOmega g 1) 0 2) (lagY 1 (lagrangeOmega g 1) 0 2) = g := by
    rw [lagX0_eq1, lagY0_eq1, lagX0_eq2, lagY0_eq2, lagX0_eq3, lagY0_eq3]
    exact I_equilateral g
  exact hc.trans h0

/-! ## The axiom footprint -/

-- Every theorem above must depend only on Mathlib's classical foundations.
#print axioms theta_separation
#print axioms theta_three_step
#print axioms r_periodic
#print axioms theta_periodic
#print axioms omega_pos
#print axioms eps_pos
#print axioms eps_lt_one
#print axioms rClosed_pos
#print axioms chaplygin_shape
#print axioms gauge_inverse
#print axioms side1
#print axioms side2
#print axioms side3
#print axioms side3'
#print axioms H_equilateral
#print axioms P_equilateral
#print axioms Q_equilateral
#print axioms I_equilateral
#print axioms P_kirchhoff_deriv
#print axioms P_kirchhoff_conserved
#print axioms Q_kirchhoff_deriv
#print axioms Q_kirchhoff_conserved
#print axioms I_kirchhoff_deriv
#print axioms I_kirchhoff_conserved
#print axioms H_kirchhoff_deriv
#print axioms H_kirchhoff_conserved
#print axioms d2_lag01
#print axioms d2_lag12
#print axioms d2_lag02
#print axioms lagX_sum
#print axioms lagY_sum
#print axioms lagX_deriv
#print axioms lagY_deriv
#print axioms lag_kx0
#print axioms lag_kx1
#print axioms lag_kx2
#print axioms lag_ky0
#print axioms lag_ky1
#print axioms lag_ky2
#print axioms lagrangeSol
#print axioms lagrange_anchor_H
#print axioms lagrange_anchor_P
#print axioms lagrange_anchor_Q
#print axioms lagrange_anchor_I

end Trivortex
