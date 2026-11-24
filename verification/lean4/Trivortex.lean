/-
SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
-/
/-
==========================================================================
TRIVORTEX — LEAN 4 FORMALIZATION: THE FULL STATEMENT LAYER (v6.0)
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
  3'. Section 7 (v3.0): the complete theory of the Lagrange triangle —
     rotation-group identity, velocity field ω·J·r, Kirchhoff field at
     an arbitrary trial frequency, the FORCING theorem for ω, period
     closed form T = 4π²a²/(3Γ), choreography cycle, scaling laws,
     orbit radius, distance certificates, general-side anchors.
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

  4'. Section 8 (v4.0): LINEAR STABILITY of the Lagrange triangle — the
     frame co-rotating with the triangle (ẇ = V(w) − ω·Jw), the anchor
     as its fixed point, the 2π/Γ-scaled linearization linX1…linY3,
     all six eigenmodes (translations ±iω, phase 0, size drift, shape
     oscillation ±iω), certification of the linearization against the
     TRUE rotating-frame field along every modal direction, explicit
     modal solutions of the linearized rotating-frame equation for all
     t, and the stability bounds: translation and shape modes preserve
     their norm exactly, the size drift grows at most linearly — no
     eigenmode grows exponentially (the classical Thomson stability at
     N = 3).

  5'. Section 9 (v5.0): NONLINEAR CONTINUATION OF THE MODES and
     BIFURCATION ANALYSIS AT UNEQUAL CIRCULATIONS.
       • 9.1 the Lagrange branch continues for ARBITRARY circulations
         (g1, g2, g3) with G = g1+g2+g3 =/= 0: the equilateral triangle
         translated so that its circulation-weighted centroid sits at
         the origin and rotating rigidly at omega = G/(2*pi*a^2) is an
         EXACT Kirchhoff solution (s9_rel_eq) — the rotation rate is
         regular in the side parameter (s9_omega_scale);
       • 9.2 the mode families persist EXACTLY in the full nonlinear
         system: the translation orbit (the Kirchhoff field is
         translation-invariant, s9_sol_shift), the phase orbit
         (re-timed solutions, s9_sol_time) and the constant norm of the
         rotating-frame translation deviation (s9_trans_dev);
       • 9.3 the 2*pi-scaled rotating-frame linearization genLinX1…
         genLinY3 for arbitrary circulations, tied to the §8 certified
         matrix on the diagonal (s9_lin_diag); its characteristic
         polynomial is lambda^2*(lambda^2 + G^2)*(lambda^2 + 3*P) with
         P = G1G2+G2G3+G3G1 (s9_lin_trans, s9_lin_kernel, s9_lin_chain,
         s9_shape_gen — all SymPy-verified). THE BIFURCATION: P > 0 the
         shape pair oscillates (+-i*sqrt(3P); instance (1,1,4) with the
         bounded modal solution s9_lin_sol_shape4); P = 0 the pair
         collides at zero (instance (1,1,-1/2): kernel + Jordan chain,
         s9_collision_a/b); P < 0 a REAL eigenvalue pair ±sqrt(-3P)
         appears (instance (1,1,-1): s9_eig_unst) with the exponentially
         growing modal solution m(t) = e^(sqrt(3)*t)*v and
         |m(t)|^2 = 12*e^(2*sqrt(3)*t) (s9_lin_sol_unst, s9_growth_norm)
         — linear instability across the hypersurface
         G1G2+G2G3+G3G1 = 0.

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

/-! ## Section 7 — the Lagrange triangle: the complete theory -/

/-! The `lagrange_triangle` scene of `verification/trivortex_master`
    (`data/presets_scenes.json`: three equal bodies at 0°, 120°, 240°, the
    classical 1772 solution) is the configuration formalized in Section 6.
    This section completes its theory to the same depth the numerical
    ladders exercise it with (`verification/trivortex/python/verify.py`,
    check V2): the rotation-group identity, the kinematic velocity field
    d/dt r = ω·Jr, the Kirchhoff field at an arbitrary trial frequency, the
    forcing theorem for the frequency, the period closed form and
    periodicity, the choreography cycle (one third of the period permutes
    the vortices cyclically), the homogeneity (scaling) laws of the vortex
    integrals, the orbit radius, the distance certificates, the scaling
    law of the family, and the exact anchor values of all four integrals
    for a triangle of arbitrary side a. -/

/-! ### trigonometric half-period identities -/

private theorem cos_add_pi_unit (u : ℝ) : Real.cos (u + Real.pi) = -Real.cos u := by
  rw [Real.cos_add, Real.cos_pi, Real.sin_pi]
  ring

private theorem sin_add_pi_unit (u : ℝ) : Real.sin (u + Real.pi) = -Real.sin u := by
  rw [Real.sin_add, Real.cos_pi, Real.sin_pi]
  ring

/-! ### the homogeneity of the vortex integrals (scaling laws) -/

/-- The distance between two scaled points scales linearly: the pairwise
    term of the Kirchhoff integrals is homogeneous of degree 1. -/
theorem vortexDist_scale (c x1 y1 x2 y2 : ℝ) (hc : 0 ≤ c) :
    vortexDist (c * x1) (c * y1) (c * x2) (c * y2)
      = c * vortexDist x1 y1 x2 y2 := by
  unfold vortexDist
  have hexp : (c * x1 - c * x2) ^ 2 + (c * y1 - c * y2) ^ 2
      = c ^ 2 * ((x1 - x2) ^ 2 + (y1 - y2) ^ 2) := by ring
  have hD : 0 ≤ (x1 - x2) ^ 2 + (y1 - y2) ^ 2 := by positivity
  have hD2 : 0 ≤ c ^ 2 := sq_nonneg c
  rw [hexp, Real.sqrt_mul hD2, Real.sqrt_sq hc]

/-- The linear impulse P = ΣΓx is homogeneous of degree 1. -/
theorem Pvortex_scale (c g1 g2 g3 x1 x2 x3 : ℝ) :
    Pvortex g1 g2 g3 (c * x1) (c * x2) (c * x3) = c * Pvortex g1 g2 g3 x1 x2 x3 := by
  unfold Pvortex
  ring

/-- The linear impulse Q = ΣΓy is homogeneous of degree 1. -/
theorem Qvortex_scale (c g1 g2 g3 y1 y2 y3 : ℝ) :
    Qvortex g1 g2 g3 (c * y1) (c * y2) (c * y3) = c * Qvortex g1 g2 g3 y1 y2 y3 := by
  unfold Qvortex
  ring

/-- The angular impulse I = ΣΓ|r|² is homogeneous of degree 2. -/
theorem Ivortex_scale (c g1 g2 g3 x1 y1 x2 y2 x3 y3 : ℝ) :
    Ivortex g1 g2 g3 (c * x1) (c * y1) (c * x2) (c * y2) (c * x3) (c * y3)
      = c ^ 2 * Ivortex g1 g2 g3 x1 y1 x2 y2 x3 y3 := by
  unfold Ivortex
  ring

/-- **The Hamiltonian is quasi-homogeneous**: scaling the configuration by
    c > 0 shifts H by −(1/2π)·(Γ₁Γ₂+Γ₁Γ₃+Γ₂Γ₃)·ln c — the logarithmic
    scaling law behind "smaller vortex triangles rotate faster". -/
theorem Hvortex_scale (c g1 g2 g3 x1 y1 x2 y2 x3 y3 : ℝ) (hc : 0 < c)
    (h12 : vortexDist x1 y1 x2 y2 ≠ 0) (h13 : vortexDist x1 y1 x3 y3 ≠ 0)
    (h23 : vortexDist x2 y2 x3 y3 ≠ 0) :
    Hvortex g1 g2 g3 (c * x1) (c * y1) (c * x2) (c * y2) (c * x3) (c * y3)
      = Hvortex g1 g2 g3 x1 y1 x2 y2 x3 y3
        - (1 / (2 * Real.pi)) * (g1 * g2 + g1 * g3 + g2 * g3) * Real.log c := by
  unfold Hvortex at *
  rw [vortexDist_scale c x1 y1 x2 y2 hc.le, vortexDist_scale c x1 y1 x3 y3 hc.le,
    vortexDist_scale c x2 y2 x3 y3 hc.le,
    Real.log_mul (ne_of_gt hc) h12, Real.log_mul (ne_of_gt hc) h13,
    Real.log_mul (ne_of_gt hc) h23]
  ring

/-! ### the rotation-group identity and the velocity field -/

/-- **The Lagrange choreography is a one-parameter rotation group**: the
    state at time t + s is the state at time t rotated by the angle ω·s —
    the exact statement of "rigid rotation". -/
theorem lag_rotation_x (a ω s t : ℝ) (k : ℕ) :
    lagX a ω (t + s) k
      = Real.cos (ω * s) * lagX a ω t k - Real.sin (ω * s) * lagY a ω t k := by
  unfold lagX lagY
  rw [show ω * (t + s) + 2 * Real.pi * (k:ℝ) / 3
        = (ω * t + 2 * Real.pi * (k:ℝ) / 3) + ω * s from by ring, Real.cos_add]
  ring

/-- The y-coordinate twin of `lag_rotation_x`. -/
theorem lag_rotation_y (a ω s t : ℝ) (k : ℕ) :
    lagY a ω (t + s) k
      = Real.sin (ω * s) * lagX a ω t k + Real.cos (ω * s) * lagY a ω t k := by
  unfold lagX lagY
  rw [show ω * (t + s) + 2 * Real.pi * (k:ℝ) / 3
        = (ω * t + 2 * Real.pi * (k:ℝ) / 3) + ω * s from by ring, Real.sin_add]
  ring

/-- **The rigid-rotation velocity field**: whatever the frequency, the
    trajectory derivative is exactly d/dt r_k = −ω·y_k — the point-vortex
    velocity equals ω·J·r (J = the quarter-turn). -/
theorem lag_deriv_field_x (a ω t : ℝ) (k : ℕ) :
    HasDerivAt (fun s => lagX a ω s k) (-ω * lagY a ω t k) t := by
  refine (lagX_deriv a ω t k).congr_deriv ?_
  unfold lagY
  ring

/-- The y-component of the rigid-rotation velocity field: d/dt y_k = ω·x_k. -/
theorem lag_deriv_field_y (a ω t : ℝ) (k : ℕ) :
    HasDerivAt (fun s => lagY a ω s k) (ω * lagX a ω t k) t := by
  refine (lagY_deriv a ω t k).congr_deriv ?_
  unfold lagX
  ring

/-- **The orbit radius**: every vortex of the rotating triangle stays on
    the circle of radius a/√3 centered at the origin — |r_k(t)|² = a²/3. -/
theorem lag_orbit_radius (a ω t : ℝ) (k : ℕ) :
    lagX a ω t k ^ 2 + lagY a ω t k ^ 2 = a ^ 2 / 3 := by
  have h3 : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hs2 : Real.sqrt 3 * Real.sqrt 3 = 3 := by linear_combination h3
  have hcc : (a / Real.sqrt 3) * (a / Real.sqrt 3) = a ^ 2 / 3 := by
    rw [show (a / Real.sqrt 3) * (a / Real.sqrt 3)
        = a * a / (Real.sqrt 3 * Real.sqrt 3) from by ring, hs2]
    ring
  have h := Real.sin_sq_add_cos_sq (ω * t + 2 * Real.pi * (k:ℝ) / 3)
  unfold lagX lagY
  have hexp : ((a / Real.sqrt 3) * Real.cos (ω * t + 2 * Real.pi * (k:ℝ) / 3)) ^ 2
      + ((a / Real.sqrt 3) * Real.sin (ω * t + 2 * Real.pi * (k:ℝ) / 3)) ^ 2
      = (a / Real.sqrt 3) * (a / Real.sqrt 3)
        * (Real.cos (ω * t + 2 * Real.pi * (k:ℝ) / 3) ^ 2
          + Real.sin (ω * t + 2 * Real.pi * (k:ℝ) / 3) ^ 2) := by
    ring
  rw [hexp, hcc]
  linear_combination (a ^ 2 / 3) * h

/-! ### the period of the choreography -/

/-- **The period closed form**: one full turn of the triangle takes
    T = 2π/ω = 4π²a²/(3Γ) — the number the V2 ladder measures. -/
theorem lag_period_closed (g a : ℝ) (hg : g ≠ 0) (ha : a ≠ 0) :
    2 * Real.pi / lagrangeOmega g a = 4 * Real.pi ^ 2 * a ^ 2 / (3 * g) := by
  have h2 : (0:ℝ) < a ^ 2 := by rw [pow_two]; exact mul_self_pos.mpr ha
  have hnum : (3 * g : ℝ) ≠ 0 := mul_ne_zero (show (3:ℝ) ≠ 0 from by norm_num) hg
  have hden : (2 * Real.pi * a ^ 2 : ℝ) ≠ 0 :=
    mul_ne_zero (show (2 * Real.pi : ℝ) ≠ 0 from by positivity) (ne_of_gt h2)
  unfold lagrangeOmega
  field_simp [hnum, hden]
  ring

/-- **Periodicity of the choreography**: after T = 2π/ω every vortex is
    exactly back at its starting point — the point-vortex twin of the
    `r_periodic`/`theta_periodic` certificates of the V1 closed form. -/
theorem lagX_periodic (a ω t : ℝ) (k : ℕ) (hω : ω ≠ 0) :
    lagX a ω (t + 2 * Real.pi / ω) k = lagX a ω t k := by
  unfold lagX
  rw [show ω * (t + 2 * Real.pi / ω) + 2 * Real.pi * (k:ℝ) / 3
        = (ω * t + 2 * Real.pi * (k:ℝ) / 3) + 2 * Real.pi from by field_simp; ring,
    Real.cos_add_two_pi]

/-- The y-coordinate twin of `lagX_periodic`. -/
theorem lagY_periodic (a ω t : ℝ) (k : ℕ) (hω : ω ≠ 0) :
    lagY a ω (t + 2 * Real.pi / ω) k = lagY a ω t k := by
  unfold lagY
  rw [show ω * (t + 2 * Real.pi / ω) + 2 * Real.pi * (k:ℝ) / 3
        = (ω * t + 2 * Real.pi * (k:ℝ) / 3) + 2 * Real.pi from by field_simp; ring,
    Real.sin_add_two_pi]

/-- After half the period the triangle is exactly inverted through the
    origin (rotated by π). -/
theorem lagX_half_period (a ω t : ℝ) (k : ℕ) (hω : ω ≠ 0) :
    lagX a ω (t + Real.pi / ω) k = -lagX a ω t k := by
  unfold lagX
  rw [show ω * (t + Real.pi / ω) + 2 * Real.pi * (k:ℝ) / 3
        = (ω * t + 2 * Real.pi * (k:ℝ) / 3) + Real.pi from by field_simp; ring,
    cos_add_pi_unit]
  ring

/-- The y-coordinate twin of `lagX_half_period`. -/
theorem lagY_half_period (a ω t : ℝ) (k : ℕ) (hω : ω ≠ 0) :
    lagY a ω (t + Real.pi / ω) k = -lagY a ω t k := by
  unfold lagY
  rw [show ω * (t + Real.pi / ω) + 2 * Real.pi * (k:ℝ) / 3
        = (ω * t + 2 * Real.pi * (k:ℝ) / 3) + Real.pi from by field_simp; ring,
    sin_add_pi_unit]
  ring

/-! ### the choreography cycle -/

/-- **The choreography cycle**: one third of the period maps vortex 0
    exactly onto vortex 1 — the triangle advances by exactly one vertex
    (x-part). -/
theorem lag_cycle_x0 (a ω t : ℝ) (hω : ω ≠ 0) :
    lagX a ω (t + 2 * Real.pi / (3 * ω)) 0 = lagX a ω t 1 := by
  unfold lagX
  rw [show ω * (t + 2 * Real.pi / (3 * ω)) + 2 * Real.pi * (0:ℕ) / 3
        = ω * t + 2 * Real.pi * (1:ℕ) / 3 from by push_cast; field_simp; ring]

/-- The cycle continues: one third of the period maps vortex 1 onto
    vortex 2 (x-part). -/
theorem lag_cycle_x1 (a ω t : ℝ) (hω : ω ≠ 0) :
    lagX a ω (t + 2 * Real.pi / (3 * ω)) 1 = lagX a ω t 2 := by
  unfold lagX
  rw [show ω * (t + 2 * Real.pi / (3 * ω)) + 2 * Real.pi * (1:ℕ) / 3
        = ω * t + 2 * Real.pi * (2:ℕ) / 3 from by push_cast; field_simp; ring]

/-- The cycle closes: one third of the period maps vortex 2 onto vortex 0
    (x-part) — the permutation (0 1 2) of the choreography. -/
theorem lag_cycle_x2 (a ω t : ℝ) (hω : ω ≠ 0) :
    lagX a ω (t + 2 * Real.pi / (3 * ω)) 2 = lagX a ω t 0 := by
  unfold lagX
  rw [show ω * (t + 2 * Real.pi / (3 * ω)) + 2 * Real.pi * (2:ℕ) / 3
        = (ω * t + 2 * Real.pi * (0:ℕ) / 3) + 2 * Real.pi from by push_cast; field_simp; ring,
    Real.cos_add_two_pi]

/-- The choreography cycle, y-part (vortex 0 → 1). -/
theorem lag_cycle_y0 (a ω t : ℝ) (hω : ω ≠ 0) :
    lagY a ω (t + 2 * Real.pi / (3 * ω)) 0 = lagY a ω t 1 := by
  unfold lagY
  rw [show ω * (t + 2 * Real.pi / (3 * ω)) + 2 * Real.pi * (0:ℕ) / 3
        = ω * t + 2 * Real.pi * (1:ℕ) / 3 from by push_cast; field_simp; ring]

/-- The choreography cycle, y-part (vortex 1 → 2). -/
theorem lag_cycle_y1 (a ω t : ℝ) (hω : ω ≠ 0) :
    lagY a ω (t + 2 * Real.pi / (3 * ω)) 1 = lagY a ω t 2 := by
  unfold lagY
  rw [show ω * (t + 2 * Real.pi / (3 * ω)) + 2 * Real.pi * (1:ℕ) / 3
        = ω * t + 2 * Real.pi * (2:ℕ) / 3 from by push_cast; field_simp; ring]

/-- The choreography cycle, y-part (vortex 2 → 0). -/
theorem lag_cycle_y2 (a ω t : ℝ) (hω : ω ≠ 0) :
    lagY a ω (t + 2 * Real.pi / (3 * ω)) 2 = lagY a ω t 0 := by
  unfold lagY
  rw [show ω * (t + 2 * Real.pi / (3 * ω)) + 2 * Real.pi * (2:ℕ) / 3
        = (ω * t + 2 * Real.pi * (0:ℕ) / 3) + 2 * Real.pi from by push_cast; field_simp; ring,
    Real.sin_add_two_pi]

/-! ### the Kirchhoff field at an arbitrary trial frequency -/

/-- **The Kirchhoff field, form 1 (x-velocity of vortex 0)**: at the
    vertices of the rotating equilateral triangle — for ANY trial
    frequency ω — the Kirchhoff x-velocity is −ω_G·y₀ where
    ω_G = 3Γ/(2πa²) is the Lagrange frequency: the field depends only on
    the configuration, not on the trial frequency. -/
theorem lag_kx0_field (g a ω t : ℝ) :
    kx1 g g g (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1)
      (lagX a ω t 2) (lagY a ω t 2)
      = -(3 * g / (2 * Real.pi * a ^ 2)) * lagY a ω t 0 := by
  have hd1 : d2 (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1) = a ^ 2 :=
    d2_lag01 a ω t
  have hd2 : d2 (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 2) (lagY a ω t 2) = a ^ 2 :=
    d2_lag02 a ω t
  have hs := lagY_sum a ω t
  have hsum : g * (lagY a ω t 0 - lagY a ω t 1) + g * (lagY a ω t 0 - lagY a ω t 2)
      = 3 * g * lagY a ω t 0 := by
    linear_combination (-g) * hs
  unfold kx1
  rw [hd1, hd2, show g * (lagY a ω t 0 - lagY a ω t 1) / a ^ 2
        + g * (lagY a ω t 0 - lagY a ω t 2) / a ^ 2
      = (g * (lagY a ω t 0 - lagY a ω t 1) + g * (lagY a ω t 0 - lagY a ω t 2)) / a ^ 2 from by
      ring, hsum]
  ring

/-- The Kirchhoff field, form 2 (x-velocity of vortex 1). -/
theorem lag_kx1_field (g a ω t : ℝ) :
    kx2 g g g (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1)
      (lagX a ω t 2) (lagY a ω t 2)
      = -(3 * g / (2 * Real.pi * a ^ 2)) * lagY a ω t 1 := by
  have hd1 : d2 (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1) = a ^ 2 :=
    d2_lag01 a ω t
  have hd2 : d2 (lagX a ω t 1) (lagY a ω t 1) (lagX a ω t 2) (lagY a ω t 2) = a ^ 2 :=
    d2_lag12 a ω t
  have hs := lagY_sum a ω t
  have hsum : g * (lagY a ω t 1 - lagY a ω t 0) + g * (lagY a ω t 1 - lagY a ω t 2)
      = 3 * g * lagY a ω t 1 := by
    linear_combination (-g) * hs
  unfold kx2
  rw [hd1, hd2, show g * (lagY a ω t 1 - lagY a ω t 0) / a ^ 2
        + g * (lagY a ω t 1 - lagY a ω t 2) / a ^ 2
      = (g * (lagY a ω t 1 - lagY a ω t 0) + g * (lagY a ω t 1 - lagY a ω t 2)) / a ^ 2 from by
      ring, hsum]
  ring

/-- The Kirchhoff field, form 3 (x-velocity of vortex 2). -/
theorem lag_kx2_field (g a ω t : ℝ) :
    kx3 g g g (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1)
      (lagX a ω t 2) (lagY a ω t 2)
      = -(3 * g / (2 * Real.pi * a ^ 2)) * lagY a ω t 2 := by
  have hd1 : d2 (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 2) (lagY a ω t 2) = a ^ 2 :=
    d2_lag02 a ω t
  have hd2 : d2 (lagX a ω t 1) (lagY a ω t 1) (lagX a ω t 2) (lagY a ω t 2) = a ^ 2 :=
    d2_lag12 a ω t
  have hs := lagY_sum a ω t
  have hsum : g * (lagY a ω t 2 - lagY a ω t 0) + g * (lagY a ω t 2 - lagY a ω t 1)
      = 3 * g * lagY a ω t 2 := by
    linear_combination (-g) * hs
  unfold kx3
  rw [hd1, hd2, show g * (lagY a ω t 2 - lagY a ω t 0) / a ^ 2
        + g * (lagY a ω t 2 - lagY a ω t 1) / a ^ 2
      = (g * (lagY a ω t 2 - lagY a ω t 0) + g * (lagY a ω t 2 - lagY a ω t 1)) / a ^ 2 from by
      ring, hsum]
  ring

/-- The Kirchhoff field, form 4 (y-velocity of vortex 0). -/
theorem lag_ky0_field (g a ω t : ℝ) :
    ky1 g g g (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1)
      (lagX a ω t 2) (lagY a ω t 2)
      = (3 * g / (2 * Real.pi * a ^ 2)) * lagX a ω t 0 := by
  have hd1 : d2 (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1) = a ^ 2 :=
    d2_lag01 a ω t
  have hd2 : d2 (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 2) (lagY a ω t 2) = a ^ 2 :=
    d2_lag02 a ω t
  have hc := lagX_sum a ω t
  have hsum : g * (lagX a ω t 0 - lagX a ω t 1) + g * (lagX a ω t 0 - lagX a ω t 2)
      = 3 * g * lagX a ω t 0 := by
    linear_combination (-g) * hc
  unfold ky1
  rw [hd1, hd2, show g * (lagX a ω t 0 - lagX a ω t 1) / a ^ 2
        + g * (lagX a ω t 0 - lagX a ω t 2) / a ^ 2
      = (g * (lagX a ω t 0 - lagX a ω t 1) + g * (lagX a ω t 0 - lagX a ω t 2)) / a ^ 2 from by
      ring, hsum]
  ring

/-- The Kirchhoff field, form 5 (y-velocity of vortex 1). -/
theorem lag_ky1_field (g a ω t : ℝ) :
    ky2 g g g (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1)
      (lagX a ω t 2) (lagY a ω t 2)
      = (3 * g / (2 * Real.pi * a ^ 2)) * lagX a ω t 1 := by
  have hd1 : d2 (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1) = a ^ 2 :=
    d2_lag01 a ω t
  have hd2 : d2 (lagX a ω t 1) (lagY a ω t 1) (lagX a ω t 2) (lagY a ω t 2) = a ^ 2 :=
    d2_lag12 a ω t
  have hc := lagX_sum a ω t
  have hsum : g * (lagX a ω t 1 - lagX a ω t 0) + g * (lagX a ω t 1 - lagX a ω t 2)
      = 3 * g * lagX a ω t 1 := by
    linear_combination (-g) * hc
  unfold ky2
  rw [hd1, hd2, show g * (lagX a ω t 1 - lagX a ω t 0) / a ^ 2
        + g * (lagX a ω t 1 - lagX a ω t 2) / a ^ 2
      = (g * (lagX a ω t 1 - lagX a ω t 0) + g * (lagX a ω t 1 - lagX a ω t 2)) / a ^ 2 from by
      ring, hsum]
  ring

/-- The Kirchhoff field, form 6 (y-velocity of vortex 2). -/
theorem lag_ky2_field (g a ω t : ℝ) :
    ky3 g g g (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1)
      (lagX a ω t 2) (lagY a ω t 2)
      = (3 * g / (2 * Real.pi * a ^ 2)) * lagX a ω t 2 := by
  have hd1 : d2 (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 2) (lagY a ω t 2) = a ^ 2 :=
    d2_lag02 a ω t
  have hd2 : d2 (lagX a ω t 1) (lagY a ω t 1) (lagX a ω t 2) (lagY a ω t 2) = a ^ 2 :=
    d2_lag12 a ω t
  have hc := lagX_sum a ω t
  have hsum : g * (lagX a ω t 2 - lagX a ω t 0) + g * (lagX a ω t 2 - lagX a ω t 1)
      = 3 * g * lagX a ω t 2 := by
    linear_combination (-g) * hc
  unfold ky3
  rw [hd1, hd2, show g * (lagX a ω t 2 - lagX a ω t 0) / a ^ 2
        + g * (lagX a ω t 2 - lagX a ω t 1) / a ^ 2
      = (g * (lagX a ω t 2 - lagX a ω t 0) + g * (lagX a ω t 2 - lagX a ω t 1)) / a ^ 2 from by
      ring, hsum]
  ring

/-! ### the frequency is forced -/

/-- **THE FORCING THEOREM — the frequency is not an ansatz choice.**
    If the equilateral triangle rotating at an arbitrary trial frequency ν
    is to satisfy the Kirchhoff y-equation at t = 0, then necessarily
    ν = 3Γ/(2πa²): the Lagrange angular velocity is uniquely determined by
    the configuration and the circulation. This is the analytic identity
    behind the V2 criterion "measured omega = 3Γ/(2πa²) within 1e-6". -/
theorem lag_omega_unique (g a ν : ℝ) (ha : a ≠ 0)
    (h : ky1 g g g (lagX a ν 0 0) (lagY a ν 0 0) (lagX a ν 0 1) (lagY a ν 0 1)
      (lagX a ν 0 2) (lagY a ν 0 2) = ν * lagX a ν 0 0) :
    ν = lagrangeOmega g a := by
  have hfield := lag_ky0_field g a ν 0
  rw [hfield] at h
  have hx0 : lagX a ν 0 0 = a / Real.sqrt 3 := by
    unfold lagX
    rw [phase0_eq, mul_zero, Real.cos_zero]
    ring
  have hx0ne : lagX a ν 0 0 ≠ 0 := by
    rw [hx0]
    intro h0
    field_simp at h0
    exact ha h0
  have h3g : (3 * g / (2 * Real.pi * a ^ 2) : ℝ) = lagrangeOmega g a := by
    unfold lagrangeOmega
    ring
  rw [h3g] at h
  exact (mul_right_cancel₀ hx0ne h).symm

/-- The Lagrange frequency is nonzero whenever the circulation and the
    side are nonzero. -/
theorem lagomega_ne_zero (g a : ℝ) (hg : g ≠ 0) (ha : a ≠ 0) :
    lagrangeOmega g a ≠ 0 := by
  have h2 : (0:ℝ) < a ^ 2 := by rw [pow_two]; exact mul_self_pos.mpr ha
  have hnum : (3 * g : ℝ) ≠ 0 := mul_ne_zero (show (3:ℝ) ≠ 0 from by norm_num) hg
  have hden : (2 * Real.pi * a ^ 2 : ℝ) ≠ 0 :=
    mul_ne_zero (show (2 * Real.pi : ℝ) ≠ 0 from by positivity) (ne_of_gt h2)
  unfold lagrangeOmega
  intro h
  exact div_ne_zero hnum hden h

/-- **The direction of the rotation**: the Lagrange frequency is positive
    exactly when the circulation is positive (the side length enters
    through a², so it never flips the sign) — counterclockwise for Γ > 0. -/
theorem lagomega_pos_iff (g a : ℝ) (ha : a ≠ 0) : 0 < lagrangeOmega g a ↔ 0 < g := by
  have h2 : (0:ℝ) < a ^ 2 := by rw [pow_two]; exact mul_self_pos.mpr ha
  have hden : 0 < 2 * Real.pi * a ^ 2 :=
    mul_pos (show (0:ℝ) < 2 * Real.pi from by positivity) h2
  unfold lagrangeOmega
  constructor
  · intro h
    rcases div_pos_iff.mp h with ⟨h1, -⟩ | ⟨h1, h2'⟩
    · linarith
    · exfalso
      linarith
  · intro hg
    exact div_pos (mul_pos (show (0:ℝ) < 3 from by norm_num) hg) hden

/-! ### the scaling law of the family -/

/-- The Lagrange frequency scales as ω(λa) = ω(a)/λ² — halving the
    triangle quadruples the spin rate. -/
theorem lagomega_scale (g a c : ℝ) (hg : g ≠ 0) (hc : c ≠ 0) (ha : a ≠ 0) :
    lagrangeOmega g (c * a) = lagrangeOmega g a / c ^ 2 := by
  have h2 : (0:ℝ) < c ^ 2 := by rw [pow_two]; exact mul_self_pos.mpr hc
  have ha2 : (0:ℝ) < a ^ 2 := by rw [pow_two]; exact mul_self_pos.mpr ha
  have hca : (0:ℝ) < (c * a) ^ 2 := by
    rw [pow_two]
    exact mul_self_pos.mpr (mul_ne_zero hc ha)
  have hden1 : (2 * Real.pi * (c * a) ^ 2 : ℝ) ≠ 0 :=
    mul_ne_zero (show (2 * Real.pi : ℝ) ≠ 0 from by positivity) (ne_of_gt hca)
  have hden2 : (2 * Real.pi * a ^ 2 : ℝ) ≠ 0 :=
    mul_ne_zero (show (2 * Real.pi : ℝ) ≠ 0 from by positivity) (ne_of_gt ha2)
  have hnum : (3 * g : ℝ) ≠ 0 := mul_ne_zero (show (3:ℝ) ≠ 0 from by norm_num) hg
  unfold lagrangeOmega
  field_simp [hden1, hden2, hnum, ne_of_gt h2]
  ring

/-- The trajectories of the family are scaled copies: the solution at side
    c·a is c times the solution at side a, run at the scaled time t/c². -/
theorem lagX_scale (c a ω t : ℝ) (k : ℕ) : lagX (c * a) ω t k = c * lagX a ω t k := by
  unfold lagX
  ring

/-- The y-coordinate twin of `lagX_scale`. -/
theorem lagY_scale (c a ω t : ℝ) (k : ℕ) : lagY (c * a) ω t k = c * lagY a ω t k := by
  unfold lagY
  ring

/-- The initial vertex k = a·(the reference vertex k): the t = 0 slice of
    the rotating triangle is the reference state, scaled. -/
theorem lagX_zero (a ω : ℝ) (k : ℕ) : lagX a ω 0 k = a * lagX 1 ω 0 k := by
  have h := lagX_scale a 1 ω 0 k
  rwa [mul_one] at h

/-- The y-coordinate twin of `lagX_zero`. -/
theorem lagY_zero (a ω : ℝ) (k : ℕ) : lagY a ω 0 k = a * lagY 1 ω 0 k := by
  have h := lagY_scale a 1 ω 0 k
  rwa [mul_one] at h

/-- **The trajectory scaling law**: lagX(c·a, ω(c·a), t) = c·lagX(a, ω(a),
    t/c²) — the same choreography, time-rescaled. Together with
    `lagomega_scale` this is the complete similarity solution of the
    Lagrange family. -/
theorem lag_trajectory_scale_x (g a c t : ℝ) (k : ℕ) (hc : c ≠ 0) (ha : a ≠ 0) :
    lagX (c * a) (lagrangeOmega g (c * a)) t k
      = c * lagX a (lagrangeOmega g a) (t / c ^ 2) k := by
  unfold lagX lagrangeOmega
  have harg : (3 * g / (2 * Real.pi * (c * a) ^ 2)) * t + 2 * Real.pi * (k:ℝ) / 3
        = (3 * g / (2 * Real.pi * a ^ 2)) * (t / c ^ 2) + 2 * Real.pi * (k:ℝ) / 3 := by
    field_simp
    ring
  rw [harg]
  ring

/-- The y-coordinate twin of `lag_trajectory_scale_x`. -/
theorem lag_trajectory_scale_y (g a c t : ℝ) (k : ℕ) (hc : c ≠ 0) (ha : a ≠ 0) :
    lagY (c * a) (lagrangeOmega g (c * a)) t k
      = c * lagY a (lagrangeOmega g a) (t / c ^ 2) k := by
  unfold lagY lagrangeOmega
  have harg : (3 * g / (2 * Real.pi * (c * a) ^ 2)) * t + 2 * Real.pi * (k:ℝ) / 3
        = (3 * g / (2 * Real.pi * a ^ 2)) * (t / c ^ 2) + 2 * Real.pi * (k:ℝ) / 3 := by
    field_simp
    ring
  rw [harg]
  ring

/-! ### the distance certificates (the shape part of check V2) -/

/-- **The side lengths never change, in distance form**: the 0–1 side of
    the rotating triangle is exactly a for every t (0 < a) — the exact
    counterpart of the `shape_drift ≤ 1e-10` band of check V2. -/
theorem lag_dist01 (a ω t : ℝ) (ha : 0 < a) :
    vortexDist (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 1) (lagY a ω t 1) = a := by
  rw [vortexDist_eq, d2_lag01 a ω t, Real.sqrt_sq (le_of_lt ha)]

/-- The 0–2 side is exactly a for every t. -/
theorem lag_dist02 (a ω t : ℝ) (ha : 0 < a) :
    vortexDist (lagX a ω t 0) (lagY a ω t 0) (lagX a ω t 2) (lagY a ω t 2) = a := by
  rw [vortexDist_eq, d2_lag02 a ω t, Real.sqrt_sq (le_of_lt ha)]

/-- The 1–2 side is exactly a for every t. -/
theorem lag_dist12 (a ω t : ℝ) (ha : 0 < a) :
    vortexDist (lagX a ω t 1) (lagY a ω t 1) (lagX a ω t 2) (lagY a ω t 2) = a := by
  rw [vortexDist_eq, d2_lag12 a ω t, Real.sqrt_sq (le_of_lt ha)]

/-! ### the anchors for a triangle of arbitrary side a -/

/-- **H along the rotating triangle of side a** (0 < a, all t): the
    Hamiltonian takes the exact value −(3Γ²/2π)·ln a — the a = 1 anchor
    `lagrange_anchor_H` is the specialization ln 1 = 0. -/
theorem lagrange_side_H (g a : ℝ) (ha : 0 < a) (t : ℝ) :
    Hvortex g g g (lagX a (lagrangeOmega g a) t 0) (lagY a (lagrangeOmega g a) t 0)
      (lagX a (lagrangeOmega g a) t 1) (lagY a (lagrangeOmega g a) t 1)
      (lagX a (lagrangeOmega g a) t 2) (lagY a (lagrangeOmega g a) t 2)
      = -(3 * g ^ 2 / (2 * Real.pi)) * Real.log a := by
  have hcons := H_kirchhoff_conserved g g g (lagrangeSol g a ha) t 0
  simp only [lagrangeSol] at hcons
  rw [hcons, lagX_zero a (lagrangeOmega g a) 0, lagY_zero a (lagrangeOmega g a) 0,
    lagX_zero a (lagrangeOmega g a) 1, lagY_zero a (lagrangeOmega g a) 1,
    lagX_zero a (lagrangeOmega g a) 2, lagY_zero a (lagrangeOmega g a) 2,
    lagX0_eq1 (lagrangeOmega g a), lagY0_eq1 (lagrangeOmega g a),
    lagX0_eq2 (lagrangeOmega g a), lagY0_eq2 (lagrangeOmega g a),
    lagX0_eq3 (lagrangeOmega g a), lagY0_eq3 (lagrangeOmega g a),
    Hvortex_scale a g g g eqX1 eqY1 eqX2 eqY2 eqX3 eqY3 ha
      (by rw [side1]; norm_num) (by rw [side3']; norm_num) (by rw [side2]; norm_num),
    H_equilateral g]
  ring

/-- **P along the rotating triangle of side a** (all t): the linear
    impulse stays exactly 0. -/
theorem lagrange_side_P (g a : ℝ) (ha : 0 < a) (t : ℝ) :
    Pvortex g g g (lagX a (lagrangeOmega g a) t 0) (lagX a (lagrangeOmega g a) t 1)
      (lagX a (lagrangeOmega g a) t 2) = 0 := by
  have hcons := P_kirchhoff_conserved g g g (lagrangeSol g a ha) t 0
  simp only [lagrangeSol] at hcons
  rw [hcons, lagX_zero a (lagrangeOmega g a) 0, lagX_zero a (lagrangeOmega g a) 1,
    lagX_zero a (lagrangeOmega g a) 2,
    lagX0_eq1 (lagrangeOmega g a), lagX0_eq2 (lagrangeOmega g a),
    lagX0_eq3 (lagrangeOmega g a), Pvortex_scale, P_equilateral]
  ring

/-- **Q along the rotating triangle of side a** (all t): the linear
    impulse stays exactly 0. -/
theorem lagrange_side_Q (g a : ℝ) (ha : 0 < a) (t : ℝ) :
    Qvortex g g g (lagY a (lagrangeOmega g a) t 0) (lagY a (lagrangeOmega g a) t 1)
      (lagY a (lagrangeOmega g a) t 2) = 0 := by
  have hcons := Q_kirchhoff_conserved g g g (lagrangeSol g a ha) t 0
  simp only [lagrangeSol] at hcons
  rw [hcons, lagY_zero a (lagrangeOmega g a) 0, lagY_zero a (lagrangeOmega g a) 1,
    lagY_zero a (lagrangeOmega g a) 2,
    lagY0_eq1 (lagrangeOmega g a), lagY0_eq2 (lagrangeOmega g a),
    lagY0_eq3 (lagrangeOmega g a), Qvortex_scale, Q_equilateral]
  ring

/-- **I along the rotating triangle of side a** (all t): the angular
    impulse takes the exact value Γa² — the a = 1 anchor
    `lagrange_anchor_I` is the specialization a² = 1. -/
theorem lagrange_side_I (g a : ℝ) (ha : 0 < a) (t : ℝ) :
    Ivortex g g g (lagX a (lagrangeOmega g a) t 0) (lagY a (lagrangeOmega g a) t 0)
      (lagX a (lagrangeOmega g a) t 1) (lagY a (lagrangeOmega g a) t 1)
      (lagX a (lagrangeOmega g a) t 2) (lagY a (lagrangeOmega g a) t 2) = g * a ^ 2 := by
  have hcons := I_kirchhoff_conserved g g g (lagrangeSol g a ha) t 0
  simp only [lagrangeSol] at hcons
  rw [hcons, lagX_zero a (lagrangeOmega g a) 0, lagY_zero a (lagrangeOmega g a) 0,
    lagX_zero a (lagrangeOmega g a) 1, lagY_zero a (lagrangeOmega g a) 1,
    lagX_zero a (lagrangeOmega g a) 2, lagY_zero a (lagrangeOmega g a) 2,
    lagX0_eq1 (lagrangeOmega g a), lagY0_eq1 (lagrangeOmega g a),
    lagX0_eq2 (lagrangeOmega g a), lagY0_eq2 (lagrangeOmega g a),
    lagX0_eq3 (lagrangeOmega g a), lagY0_eq3 (lagrangeOmega g a),
    Ivortex_scale, I_equilateral]
  ring

/-! ## Section 8 — linear stability: the eigenmodes of the perturbed triangle -/

/-! The classical linear stability analysis of the Lagrange equilateral
    solution, performed in the frame co-rotating with the triangle.  In
    that frame the Kirchhoff dynamics read ẇ = V(w) − ω·Jw (per vortex:
    rotX = kx + ω·y, rotY = ky − ω·x), and the anchor state of Section 3
    is a fixed point (§8.1) — the restatement of Section 6 at t = 0.
    Linearizing at the anchor gives the 6×6 operator whose (2π/Γ)-scaled
    rows `linX1`…`linY3` are registered in §8.2.  Its spectrum is
    λ²·(λ²+9)² (SymPy-verified in `notes/verify_identities_s8.py` and
    numerically in `tools/numeric_mirror_s8.py`): eigenvalues 0 — the
    phase and size drifts of the Lagrange family — and the purely
    imaginary pair ±3i with multiplicity TWO, one copy carried by
    translations and one by the shape oscillations.  §8.3 exhibits all
    six eigenmodes explicitly, §8.4 their modal solutions of the
    linearized rotating-frame equation (the shape pair oscillates at
    exactly the Lagrange angular velocity ω), and §8.5 the stability
    bounds: every mode preserves its norm except the size drift, which
    grows at most linearly in time — no eigenmode grows exponentially.
    The equilateral triangle of equal vortices is linearly stable.

    Certification: the rows `linX1`…`linY3` are the partial derivatives
    of the true rotating-frame field at the anchor; `lin_cert_transX`,
    `lin_cert_transY`, `lin_cert_shapeU`, `lin_cert_shapeW` prove the
    directional derivatives of the TRUE field along those modal
    directions equal the linearization applied to the direction.  The
    phase and size modes are certified exactly (and beyond first order)
    by the nonlinear family theorems of Section 7: a phase-shifted
    triangle is the same solution (`lag_rotation_x`) and a rescaled
    triangle is a solution at ω/λ² (`lag_trajectory_scale_x`). -/

/-! ### the frame rotating with the triangle -/

/-- The x-velocity of vortex 1 in the frame rotating at angular velocity
    ω: the Kirchhoff field plus the frame term ω·y₁ (from ẇ = V − ω·Jw). -/
noncomputable def rotX1 (g ω x1 y1 x2 y2 x3 y3 : ℝ) : ℝ :=
  kx1 g g g x1 y1 x2 y2 x3 y3 + ω * y1

/-- The y-velocity of vortex 1 in the rotating frame. -/
noncomputable def rotY1 (g ω x1 y1 x2 y2 x3 y3 : ℝ) : ℝ :=
  ky1 g g g x1 y1 x2 y2 x3 y3 - ω * x1

/-- The x-velocity of vortex 2 in the rotating frame. -/
noncomputable def rotX2 (g ω x1 y1 x2 y2 x3 y3 : ℝ) : ℝ :=
  kx2 g g g x1 y1 x2 y2 x3 y3 + ω * y2

/-- The y-velocity of vortex 2 in the rotating frame. -/
noncomputable def rotY2 (g ω x1 y1 x2 y2 x3 y3 : ℝ) : ℝ :=
  ky2 g g g x1 y1 x2 y2 x3 y3 - ω * x2

/-- The x-velocity of vortex 3 in the rotating frame. -/
noncomputable def rotX3 (g ω x1 y1 x2 y2 x3 y3 : ℝ) : ℝ :=
  kx3 g g g x1 y1 x2 y2 x3 y3 + ω * y3

/-- The y-velocity of vortex 3 in the rotating frame. -/
noncomputable def rotY3 (g ω x1 y1 x2 y2 x3 y3 : ℝ) : ℝ :=
  ky3 g g g x1 y1 x2 y2 x3 y3 - ω * x3

private theorem s3sq : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)

/-- Division by √3 rewritten into ℚ·√3 form.  `ring` treats `(Real.sqrt 3)⁻¹`
    as an inert atom and cannot cancel it, so every √3-division is normalized
    away before the final `ring` / `linear_combination` closer. -/
private theorem div_sqrt3 (p : ℝ) : p / Real.sqrt 3 = Real.sqrt 3 / 3 * p := by
  have hne : Real.sqrt 3 ≠ 0 := by positivity
  rw [div_eq_iff hne]
  linear_combination (-(p / 3)) * s3sq

private theorem div_2sqrt3 (p : ℝ) : p / (2 * Real.sqrt 3) = Real.sqrt 3 / 6 * p := by
  have hne : (2 * Real.sqrt 3) ≠ 0 := by positivity
  rw [div_eq_iff hne]
  linear_combination (-(p / 3)) * s3sq

/-- The squared anchor distances: all three sides have d2 = 1. -/
private theorem d2_anchor12 : d2 eqX1 eqY1 eqX2 eqY2 = 1 := by
  have h := side1
  rw [vortexDist_eq] at h
  have hpos : 0 ≤ d2 eqX1 eqY1 eqX2 eqY2 := by unfold d2; positivity
  calc d2 eqX1 eqY1 eqX2 eqY2
      = (Real.sqrt (d2 eqX1 eqY1 eqX2 eqY2)) ^ 2 := (Real.sq_sqrt hpos).symm
    _ = 1 ^ 2 := by rw [h]
    _ = 1 := by norm_num

private theorem d2_anchor13 : d2 eqX1 eqY1 eqX3 eqY3 = 1 := by
  have h := side3'
  rw [vortexDist_eq] at h
  have hpos : 0 ≤ d2 eqX1 eqY1 eqX3 eqY3 := by unfold d2; positivity
  calc d2 eqX1 eqY1 eqX3 eqY3
      = (Real.sqrt (d2 eqX1 eqY1 eqX3 eqY3)) ^ 2 := (Real.sq_sqrt hpos).symm
    _ = 1 ^ 2 := by rw [h]
    _ = 1 := by norm_num

private theorem d2_anchor23 : d2 eqX2 eqY2 eqX3 eqY3 = 1 := by
  have h := side2
  rw [vortexDist_eq] at h
  have hpos : 0 ≤ d2 eqX2 eqY2 eqX3 eqY3 := by unfold d2; positivity
  calc d2 eqX2 eqY2 eqX3 eqY3
      = (Real.sqrt (d2 eqX2 eqY2 eqX3 eqY3)) ^ 2 := (Real.sq_sqrt hpos).symm
    _ = 1 ^ 2 := by rw [h]
    _ = 1 := by norm_num

/-! The anchor coordinate differences (both directions), as they appear
    in the Kirchhoff numerators. -/

private theorem eqdx12 : eqX1 - eqX2 = Real.sqrt 3 / 2 := by
  unfold eqX1 eqX2
  rw [div_sqrt3, div_2sqrt3]
  ring

private theorem eqdy12 : eqY1 - eqY2 = -(1 / 2) := by unfold eqY1 eqY2; ring

private theorem eqdx13 : eqX1 - eqX3 = Real.sqrt 3 / 2 := by
  unfold eqX1 eqX3
  rw [div_sqrt3, div_2sqrt3]
  ring

private theorem eqdy13 : eqY1 - eqY3 = 1 / 2 := by unfold eqY1 eqY3; ring

private theorem eqdx23 : eqX2 - eqX3 = 0 := by unfold eqX2 eqX3; ring

private theorem eqdy23 : eqY2 - eqY3 = 1 := by unfold eqY2 eqY3; ring

private theorem eqdx21 : eqX2 - eqX1 = -(Real.sqrt 3 / 2) := by
  unfold eqX1 eqX2
  rw [div_sqrt3, div_2sqrt3]
  ring

private theorem eqdy21 : eqY2 - eqY1 = 1 / 2 := by unfold eqY1 eqY2; ring

private theorem eqdx31 : eqX3 - eqX1 = -(Real.sqrt 3 / 2) := by
  unfold eqX1 eqX3
  rw [div_sqrt3, div_2sqrt3]
  ring

private theorem eqdy31 : eqY3 - eqY1 = -(1 / 2) := by unfold eqY1 eqY3; ring

private theorem eqdx32 : eqX3 - eqX2 = 0 := by unfold eqX2 eqX3; ring

private theorem eqdy32 : eqY3 - eqY2 = -1 := by unfold eqY2 eqY3; ring

/-- **The rotating-frame equilibrium (§8.1).**  The equilateral anchor of
    Section 3, viewed in the frame rotating at the Lagrange angular
    velocity ω = 3Γ/(2πa²), is a fixed point of the rotating-frame field:
    all six velocity components vanish.  This is the t = 0 restatement of
    the Lagrange solution of Section 6. -/
theorem rot_anchor (g : ℝ) :
    rotX1 g (lagrangeOmega g 1) eqX1 eqY1 eqX2 eqY2 eqX3 eqY3 = 0
      ∧ rotY1 g (lagrangeOmega g 1) eqX1 eqY1 eqX2 eqY2 eqX3 eqY3 = 0
      ∧ rotX2 g (lagrangeOmega g 1) eqX1 eqY1 eqX2 eqY2 eqX3 eqY3 = 0
      ∧ rotY2 g (lagrangeOmega g 1) eqX1 eqY1 eqX2 eqY2 eqX3 eqY3 = 0
      ∧ rotX3 g (lagrangeOmega g 1) eqX1 eqY1 eqX2 eqY2 eqX3 eqY3 = 0
      ∧ rotY3 g (lagrangeOmega g 1) eqX1 eqY1 eqX2 eqY2 eqX3 eqY3 = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · unfold rotX1 kx1
    rw [d2_anchor12, d2_anchor13, eqdy12, eqdy13]
    unfold eqY1 lagrangeOmega
    ring
  · unfold rotY1 ky1
    rw [d2_anchor12, d2_anchor13, eqdx12, eqdx13]
    unfold eqX1 lagrangeOmega
    rw [div_sqrt3]
    ring
  · unfold rotX2 kx2
    rw [d2_anchor12, d2_anchor23, eqdy21, eqdy23]
    unfold eqY2 lagrangeOmega
    ring
  · unfold rotY2 ky2
    rw [d2_anchor12, d2_anchor23, eqdx21, eqdx23]
    unfold eqX2 lagrangeOmega
    rw [div_2sqrt3]
    ring
  · unfold rotX3 kx3
    rw [d2_anchor13, d2_anchor23, eqdy31, eqdy32]
    unfold eqY3 lagrangeOmega
    ring
  · unfold rotY3 ky3
    rw [d2_anchor13, d2_anchor23, eqdx31, eqdx32]
    unfold eqX3 lagrangeOmega
    rw [div_2sqrt3]
    ring

/-! ### the linearization at the anchor (the 2π/Γ-scaled Jacobian rows) -/

/-! The six rows below are the Jacobian of the rotating-frame field
    at the anchor, scaled by 2π/Γ so that every entry lies in ℚ(√3):
    linRow_j(d) = (2π/Γ) · ∂(rot component j)/∂(direction d)|anchor.
    Entry provenance: computed symbolically by the SymPy ladder
    (`notes/verify_identities_s8.py`, check B) and certified along the
    modal directions by `lin_cert_*` below; the frame contribution
    −3·J per vortex is folded in. -/

/-- Row 1 (rotX₁): the derivative of the x-velocity of vortex 1 in the
    direction (dx1, dy1, dx2, dy2, dx3, dy3), in 2π/Γ units. -/
noncomputable def linX1 (dx1 dy1 dx2 dy2 dx3 dy3 : ℝ) : ℝ :=
  2 * dy1 + Real.sqrt 3 / 2 * dx2 + 1 / 2 * dy2
    - Real.sqrt 3 / 2 * dx3 + 1 / 2 * dy3

/-- Row 2 (rotY₁). -/
noncomputable def linY1 (dx1 dy1 dx2 dy2 dx3 dy3 : ℝ) : ℝ :=
  -4 * dx1 + 1 / 2 * dx2 - Real.sqrt 3 / 2 * dy2 + 1 / 2 * dx3
    + Real.sqrt 3 / 2 * dy3

/-- Row 3 (rotX₂). -/
noncomputable def linX2 (dx1 dy1 dx2 dy2 dx3 dy3 : ℝ) : ℝ :=
  Real.sqrt 3 / 2 * dx1 + 1 / 2 * dy1 - Real.sqrt 3 / 2 * dx2 + 7 / 2 * dy2
    - dy3

/-- Row 4 (rotY₂). -/
noncomputable def linY2 (dx1 dy1 dx2 dy2 dx3 dy3 : ℝ) : ℝ :=
  1 / 2 * dx1 - Real.sqrt 3 / 2 * dy1 - 5 / 2 * dx2 + Real.sqrt 3 / 2 * dy2
    - dx3

/-- Row 5 (rotX₃). -/
noncomputable def linX3 (dx1 dy1 dx2 dy2 dx3 dy3 : ℝ) : ℝ :=
  -Real.sqrt 3 / 2 * dx1 + 1 / 2 * dy1 - dy2 + Real.sqrt 3 / 2 * dx3
    + 7 / 2 * dy3

/-- Row 6 (rotY₃). -/
noncomputable def linY3 (dx1 dy1 dx2 dy2 dx3 dy3 : ℝ) : ℝ :=
  1 / 2 * dx1 + Real.sqrt 3 / 2 * dy1 - dx2 - 5 / 2 * dx3
    - Real.sqrt 3 / 2 * dy3

/-! ### the six eigenmodes -/

/-- **Eigenmode 1 — translation (x):** the uniform x-shift direction
    (1,0,1,0,1,0) is mapped by the linearization to −3·(0,1,0,1,0,1):
    in the rotating frame a translated triangle orbits at the angular
    velocity ω.  Eigenvalues ±3i (in 2π/Γ units) = ±iω. -/
theorem eig_trans1 :
    linX1 1 0 1 0 1 0 = 0
      ∧ linY1 1 0 1 0 1 0 = -3
      ∧ linX2 1 0 1 0 1 0 = 0
      ∧ linY2 1 0 1 0 1 0 = -3
      ∧ linX3 1 0 1 0 1 0 = 0
      ∧ linY3 1 0 1 0 1 0 = -3 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · unfold linX1; ring
  · unfold linY1; ring
  · unfold linX2; ring
  · unfold linY2; ring
  · unfold linX3; ring
  · unfold linY3; ring

/-- **Eigenmode 2 — translation (y):** the uniform y-shift direction
    (0,1,0,1,0,1) is mapped to +3·(1,0,1,0,1,0). -/
theorem eig_trans2 :
    linX1 0 1 0 1 0 1 = 3
      ∧ linY1 0 1 0 1 0 1 = 0
      ∧ linX2 0 1 0 1 0 1 = 3
      ∧ linY2 0 1 0 1 0 1 = 0
      ∧ linX3 0 1 0 1 0 1 = 3
      ∧ linY3 0 1 0 1 0 1 = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · unfold linX1; ring
  · unfold linY1; ring
  · unfold linX2; ring
  · unfold linY2; ring
  · unfold linX3; ring
  · unfold linY3; ring

/-- **Eigenmode 3 — phase (rotation):** the phase direction J·anchor
    (rotate the whole triangle infinitesimally) is annihilated by the
    linearization: eigenvalue 0.  Certified beyond first order by
    Section 7: a phase-shifted triangle is the same solution
    (`lag_rotation_x`). -/
theorem eig_rot :
    linX1 0 (1 / Real.sqrt 3) (-1 / 2) (-1 / (2 * Real.sqrt 3)) (1 / 2)
        (-1 / (2 * Real.sqrt 3)) = 0
      ∧ linY1 0 (1 / Real.sqrt 3) (-1 / 2) (-1 / (2 * Real.sqrt 3)) (1 / 2)
        (-1 / (2 * Real.sqrt 3)) = 0
      ∧ linX2 0 (1 / Real.sqrt 3) (-1 / 2) (-1 / (2 * Real.sqrt 3)) (1 / 2)
        (-1 / (2 * Real.sqrt 3)) = 0
      ∧ linY2 0 (1 / Real.sqrt 3) (-1 / 2) (-1 / (2 * Real.sqrt 3)) (1 / 2)
        (-1 / (2 * Real.sqrt 3)) = 0
      ∧ linX3 0 (1 / Real.sqrt 3) (-1 / 2) (-1 / (2 * Real.sqrt 3)) (1 / 2)
        (-1 / (2 * Real.sqrt 3)) = 0
      ∧ linY3 0 (1 / Real.sqrt 3) (-1 / 2) (-1 / (2 * Real.sqrt 3)) (1 / 2)
        (-1 / (2 * Real.sqrt 3)) = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · unfold linX1
    simp only [div_sqrt3, div_2sqrt3]
    ring
  · unfold linY1; ring
  · unfold linX2
    simp only [div_sqrt3, div_2sqrt3]
    ring
  · unfold linY2
    simp only [div_sqrt3, div_2sqrt3]
    linear_combination (-(1 / 4)) * s3sq
  · unfold linX3
    simp only [div_sqrt3, div_2sqrt3]
    ring
  · unfold linY3
    simp only [div_sqrt3, div_2sqrt3]
    linear_combination (1 / 4) * s3sq

/-- **Eigenmode 4 — size (dilation):** the radial direction (the anchor
    itself, per vortex) is mapped to −6·(the phase direction): the
    generalized zero eigenvalue.  A triangle of a different size rotates
    at a different rate, so in the fixed frame it drifts linearly —
    certified beyond first order by Section 7 (`lag_trajectory_scale_x`:
    the solution at side c·a runs at ω/c²). -/
theorem eig_dil :
    linX1 (1 / Real.sqrt 3) 0 (-1 / (2 * Real.sqrt 3)) (1 / 2)
        (-1 / (2 * Real.sqrt 3)) (-1 / 2) = 0
      ∧ linY1 (1 / Real.sqrt 3) 0 (-1 / (2 * Real.sqrt 3)) (1 / 2)
        (-1 / (2 * Real.sqrt 3)) (-1 / 2) = -6 / Real.sqrt 3
      ∧ linX2 (1 / Real.sqrt 3) 0 (-1 / (2 * Real.sqrt 3)) (1 / 2)
        (-1 / (2 * Real.sqrt 3)) (-1 / 2) = 3
      ∧ linY2 (1 / Real.sqrt 3) 0 (-1 / (2 * Real.sqrt 3)) (1 / 2)
        (-1 / (2 * Real.sqrt 3)) (-1 / 2) = 3 / Real.sqrt 3
      ∧ linX3 (1 / Real.sqrt 3) 0 (-1 / (2 * Real.sqrt 3)) (1 / 2)
        (-1 / (2 * Real.sqrt 3)) (-1 / 2) = -3
      ∧ linY3 (1 / Real.sqrt 3) 0 (-1 / (2 * Real.sqrt 3)) (1 / 2)
        (-1 / (2 * Real.sqrt 3)) (-1 / 2) = 3 / Real.sqrt 3 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · unfold linX1; ring
  · unfold linY1
    simp only [div_sqrt3, div_2sqrt3]
    ring
  · unfold linX2
    simp only [div_sqrt3, div_2sqrt3]
    linear_combination (1 / 4) * s3sq
  · unfold linY2
    simp only [div_sqrt3, div_2sqrt3]
    ring
  · unfold linX3
    simp only [div_sqrt3, div_2sqrt3]
    linear_combination (-(1 / 4)) * s3sq
  · unfold linY3
    simp only [div_sqrt3, div_2sqrt3]
    ring

/-- **Eigenmode 5 — shape (u):** the shape direction
    u = (1, 0, 1/2, −√3/2, 0, 0) — vortices 1 and 2 move, vortex 3
    rests — is mapped to −3·w with w = (0, 1, √3/2, 1/2, 0, 0). -/
theorem eig_shapeU :
    linX1 1 0 (1 / 2) (-Real.sqrt 3 / 2) 0 0 = 0
      ∧ linY1 1 0 (1 / 2) (-Real.sqrt 3 / 2) 0 0 = -3
      ∧ linX2 1 0 (1 / 2) (-Real.sqrt 3 / 2) 0 0 = -3 * Real.sqrt 3 / 2
      ∧ linY2 1 0 (1 / 2) (-Real.sqrt 3 / 2) 0 0 = -3 / 2
      ∧ linX3 1 0 (1 / 2) (-Real.sqrt 3 / 2) 0 0 = 0
      ∧ linY3 1 0 (1 / 2) (-Real.sqrt 3 / 2) 0 0 = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · unfold linX1; ring
  · unfold linY1; linear_combination (1 / 4) * s3sq
  · unfold linX2; ring
  · unfold linY2; linear_combination (-(1 / 4)) * s3sq
  · unfold linX3; ring
  · unfold linY3; ring

/-- **Eigenmode 6 — shape (w):** the conjugate shape direction
    w = (0, 1, √3/2, 1/2, 0, 0) is mapped to +3·u: together with
    `eig_shapeU` the shape plane carries the eigenvalue pair ±3i
    (in 2π/Γ units) — the shape oscillation at the Lagrange frequency. -/
theorem eig_shapeW :
    linX1 0 1 (Real.sqrt 3 / 2) (1 / 2) 0 0 = 3
      ∧ linY1 0 1 (Real.sqrt 3 / 2) (1 / 2) 0 0 = 0
      ∧ linX2 0 1 (Real.sqrt 3 / 2) (1 / 2) 0 0 = 3 / 2
      ∧ linY2 0 1 (Real.sqrt 3 / 2) (1 / 2) 0 0 = -3 * Real.sqrt 3 / 2
      ∧ linX3 0 1 (Real.sqrt 3 / 2) (1 / 2) 0 0 = 0
      ∧ linY3 0 1 (Real.sqrt 3 / 2) (1 / 2) 0 0 = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · unfold linX1; linear_combination (1 / 4) * s3sq
  · unfold linY1; ring
  · unfold linX2; linear_combination (-(1 / 4)) * s3sq
  · unfold linY2; ring
  · unfold linX3; ring
  · unfold linY3; ring

/-! ### certification: the true rotating-frame field along the modes -/

private theorem hasDerivAt_const_mul_id (c t : ℝ) :
    HasDerivAt (fun s => c * s) c t :=
  ((hasDerivAt_const (c := c) (x := t)).mul
    (hasDerivAt_id (𝕜 := ℝ) (x := t))).congr_deriv (by ring)

private theorem hasDerivAt_affine (c0 c1 t : ℝ) :
    HasDerivAt (fun s => c0 + c1 * s) c1 t :=
  ((hasDerivAt_const (c := c0) (x := t)).add
    (hasDerivAt_const_mul_id c1 t)).congr_deriv (by ring)

/-- The squared distance between two uniformly moving points is a
    quadratic polynomial of time (used at t = 0 only). -/
private theorem hasDerivAt_quad0 (d0 d1 d2 : ℝ) :
    HasDerivAt (fun s => d0 + d1 * s + d2 * s ^ 2) d1 0 := by
  have hmul : HasDerivAt (fun s : ℝ => s * s) (0:ℝ) 0 := by
    refine deriv_congr
      (((hasDerivAt_id (𝕜 := ℝ) (x := 0)).mul
        (hasDerivAt_id (𝕜 := ℝ) (x := 0))).congr_deriv (by simp)) (fun y => ?_)
    simp only [id_eq]
  have hs : HasDerivAt (fun s : ℝ => s ^ 2) (0:ℝ) 0 := by
    refine deriv_congr hmul (fun y => ?_)
    exact (pow_two y).symm
  have hq : HasDerivAt (fun s => d2 * s ^ 2) (d2 * 0) 0 :=
    deriv_mul_const_left hs
  exact (((hasDerivAt_const (c := d0) (x := 0)).add
    (hasDerivAt_const_mul_id d1 0)).add hq).congr_deriv (by ring)

/-- **The quotient rule at t = 0**: an affine numerator over a quadratic
    denominator, evaluated where the denominator is d0 ≠ 0. -/
private theorem hasDerivAt_quot0 (c0 c1 d0 d1 d2 : ℝ) (hd : d0 ≠ 0) :
    HasDerivAt (fun s => (c0 + c1 * s) / (d0 + d1 * s + d2 * s ^ 2))
      ((c1 * d0 - c0 * d1) / d0 ^ 2) 0 :=
  ((hasDerivAt_affine c0 c1 0).div (hasDerivAt_quad0 d0 d1 d2)
    (by simpa using hd)).congr_deriv (by ring)

/-- The squared distance only sees coordinate differences. -/
private theorem d2_shiftX (b x1 y1 x2 y2 : ℝ) :
    d2 (x1 + b) y1 (x2 + b) y2 = d2 x1 y1 x2 y2 := by
  unfold d2; ring

private theorem d2_shiftY (b x1 y1 x2 y2 : ℝ) :
    d2 x1 (y1 + b) x2 (y2 + b) = d2 x1 y1 x2 y2 := by
  unfold d2; ring

private theorem add_sub_add_eq (a b s : ℝ) : a + s - (b + s) = a - b := by
  ring

/-- **Certification of the translation modes (x):** the derivative at
    t = 0 of the TRUE rotating-frame field, evaluated along the line
    anchor + t·(1,0,1,0,1,0), is exactly the linearization applied to
    that direction — all six components.  (The vortex part is constant
    along the line by translation invariance; only the frame term
    −ω·x is affine.) -/
theorem lin_cert_transX (g : ℝ) :
    HasDerivAt (fun s => rotX1 g (lagrangeOmega g 1) (eqX1 + s) eqY1
        (eqX2 + s) eqY2 (eqX3 + s) eqY3)
      (g / (2 * Real.pi) * linX1 1 0 1 0 1 0) 0
      ∧ HasDerivAt (fun s => rotY1 g (lagrangeOmega g 1) (eqX1 + s) eqY1
        (eqX2 + s) eqY2 (eqX3 + s) eqY3)
      (g / (2 * Real.pi) * linY1 1 0 1 0 1 0) 0
      ∧ HasDerivAt (fun s => rotX2 g (lagrangeOmega g 1) (eqX1 + s) eqY1
        (eqX2 + s) eqY2 (eqX3 + s) eqY3)
      (g / (2 * Real.pi) * linX2 1 0 1 0 1 0) 0
      ∧ HasDerivAt (fun s => rotY2 g (lagrangeOmega g 1) (eqX1 + s) eqY1
        (eqX2 + s) eqY2 (eqX3 + s) eqY3)
      (g / (2 * Real.pi) * linY2 1 0 1 0 1 0) 0
      ∧ HasDerivAt (fun s => rotX3 g (lagrangeOmega g 1) (eqX1 + s) eqY1
        (eqX2 + s) eqY2 (eqX3 + s) eqY3)
      (g / (2 * Real.pi) * linX3 1 0 1 0 1 0) 0
      ∧ HasDerivAt (fun s => rotY3 g (lagrangeOmega g 1) (eqX1 + s) eqY1
        (eqX2 + s) eqY2 (eqX3 + s) eqY3)
      (g / (2 * Real.pi) * linY3 1 0 1 0 1 0) 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · have hE : ∀ s : ℝ, rotX1 g (lagrangeOmega g 1) (eqX1 + s) eqY1
        (eqX2 + s) eqY2 (eqX3 + s) eqY3 = 0 := by
      intro s
      unfold rotX1 kx1
      rw [d2_shiftX s eqX1 eqY1 eqX2 eqY2, d2_shiftX s eqX1 eqY1 eqX3 eqY3,
        d2_anchor12, d2_anchor13, eqdy12, eqdy13]
      unfold eqY1 lagrangeOmega
      ring
    have h := deriv_congr (hasDerivAt_const (c := 0) (x := 0))
      (fun s => (hE s).symm)
    exact h.congr_deriv (by unfold linX1; ring)
  · have hE : ∀ s : ℝ, rotY1 g (lagrangeOmega g 1) (eqX1 + s) eqY1
        (eqX2 + s) eqY2 (eqX3 + s) eqY3
        = -(lagrangeOmega g 1) * s := by
      intro s
      unfold rotY1 ky1
      rw [add_sub_add_eq eqX1 eqX2 s, add_sub_add_eq eqX1 eqX3 s,
        d2_shiftX s eqX1 eqY1 eqX2 eqY2, d2_shiftX s eqX1 eqY1 eqX3 eqY3,
        d2_anchor12, d2_anchor13, eqdx12, eqdx13]
      unfold eqX1 lagrangeOmega
      rw [div_sqrt3]
      ring
    have h := deriv_congr (hasDerivAt_const_mul_id (-(lagrangeOmega g 1)) 0)
      (fun s => (hE s).symm)
    exact h.congr_deriv (by unfold linY1 lagrangeOmega; ring)
  · have hE : ∀ s : ℝ, rotX2 g (lagrangeOmega g 1) (eqX1 + s) eqY1
        (eqX2 + s) eqY2 (eqX3 + s) eqY3 = 0 := by
      intro s
      unfold rotX2 kx2
      rw [d2_shiftX s eqX1 eqY1 eqX2 eqY2, d2_shiftX s eqX2 eqY2 eqX3 eqY3,
        d2_anchor12, d2_anchor23, eqdy21, eqdy23]
      unfold eqY2 lagrangeOmega
      ring
    have h := deriv_congr (hasDerivAt_const (c := 0) (x := 0))
      (fun s => (hE s).symm)
    exact h.congr_deriv (by unfold linX2; ring)
  · have hE : ∀ s : ℝ, rotY2 g (lagrangeOmega g 1) (eqX1 + s) eqY1
        (eqX2 + s) eqY2 (eqX3 + s) eqY3
        = -(lagrangeOmega g 1) * s := by
      intro s
      unfold rotY2 ky2
      rw [add_sub_add_eq eqX2 eqX1 s, add_sub_add_eq eqX2 eqX3 s,
        d2_shiftX s eqX1 eqY1 eqX2 eqY2, d2_shiftX s eqX2 eqY2 eqX3 eqY3,
        d2_anchor12, d2_anchor23, eqdx21, eqdx23]
      unfold eqX2 lagrangeOmega
      rw [div_2sqrt3]
      ring
    have h := deriv_congr (hasDerivAt_const_mul_id (-(lagrangeOmega g 1)) 0)
      (fun s => (hE s).symm)
    exact h.congr_deriv (by unfold linY2 lagrangeOmega; ring)
  · have hE : ∀ s : ℝ, rotX3 g (lagrangeOmega g 1) (eqX1 + s) eqY1
        (eqX2 + s) eqY2 (eqX3 + s) eqY3 = 0 := by
      intro s
      unfold rotX3 kx3
      rw [d2_shiftX s eqX1 eqY1 eqX3 eqY3, d2_shiftX s eqX2 eqY2 eqX3 eqY3,
        d2_anchor13, d2_anchor23, eqdy31, eqdy32]
      unfold eqY3 lagrangeOmega
      ring
    have h := deriv_congr (hasDerivAt_const (c := 0) (x := 0))
      (fun s => (hE s).symm)
    exact h.congr_deriv (by unfold linX3; ring)
  · have hE : ∀ s : ℝ, rotY3 g (lagrangeOmega g 1) (eqX1 + s) eqY1
        (eqX2 + s) eqY2 (eqX3 + s) eqY3
        = -(lagrangeOmega g 1) * s := by
      intro s
      unfold rotY3 ky3
      rw [add_sub_add_eq eqX3 eqX1 s, add_sub_add_eq eqX3 eqX2 s,
        d2_shiftX s eqX1 eqY1 eqX3 eqY3, d2_shiftX s eqX2 eqY2 eqX3 eqY3,
        d2_anchor13, d2_anchor23, eqdx31, eqdx32]
      unfold eqX3 lagrangeOmega
      rw [div_2sqrt3]
      ring
    have h := deriv_congr (hasDerivAt_const_mul_id (-(lagrangeOmega g 1)) 0)
      (fun s => (hE s).symm)
    exact h.congr_deriv (by unfold linY3 lagrangeOmega; ring)

/-- **Certification of the translation modes (y):** the same along the
    line anchor + t·(0,1,0,1,0,1). -/
theorem lin_cert_transY (g : ℝ) :
    HasDerivAt (fun s => rotX1 g (lagrangeOmega g 1) eqX1 (eqY1 + s)
        eqX2 (eqY2 + s) eqX3 (eqY3 + s))
      (g / (2 * Real.pi) * linX1 0 1 0 1 0 1) 0
      ∧ HasDerivAt (fun s => rotY1 g (lagrangeOmega g 1) eqX1 (eqY1 + s)
        eqX2 (eqY2 + s) eqX3 (eqY3 + s))
      (g / (2 * Real.pi) * linY1 0 1 0 1 0 1) 0
      ∧ HasDerivAt (fun s => rotX2 g (lagrangeOmega g 1) eqX1 (eqY1 + s)
        eqX2 (eqY2 + s) eqX3 (eqY3 + s))
      (g / (2 * Real.pi) * linX2 0 1 0 1 0 1) 0
      ∧ HasDerivAt (fun s => rotY2 g (lagrangeOmega g 1) eqX1 (eqY1 + s)
        eqX2 (eqY2 + s) eqX3 (eqY3 + s))
      (g / (2 * Real.pi) * linY2 0 1 0 1 0 1) 0
      ∧ HasDerivAt (fun s => rotX3 g (lagrangeOmega g 1) eqX1 (eqY1 + s)
        eqX2 (eqY2 + s) eqX3 (eqY3 + s))
      (g / (2 * Real.pi) * linX3 0 1 0 1 0 1) 0
      ∧ HasDerivAt (fun s => rotY3 g (lagrangeOmega g 1) eqX1 (eqY1 + s)
        eqX2 (eqY2 + s) eqX3 (eqY3 + s))
      (g / (2 * Real.pi) * linY3 0 1 0 1 0 1) 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · have hE : ∀ s : ℝ, rotX1 g (lagrangeOmega g 1) eqX1 (eqY1 + s)
        eqX2 (eqY2 + s) eqX3 (eqY3 + s)
        = lagrangeOmega g 1 * s := by
      intro s
      unfold rotX1 kx1
      rw [add_sub_add_eq eqY1 eqY2 s, add_sub_add_eq eqY1 eqY3 s,
        d2_shiftY s eqX1 eqY1 eqX2 eqY2, d2_shiftY s eqX1 eqY1 eqX3 eqY3,
        d2_anchor12, d2_anchor13, eqdy12, eqdy13]
      unfold eqY1 lagrangeOmega
      ring
    have h := deriv_congr (hasDerivAt_const_mul_id (lagrangeOmega g 1) 0)
      (fun s => (hE s).symm)
    exact h.congr_deriv (by unfold linX1 lagrangeOmega; ring)
  · have hE : ∀ s : ℝ, rotY1 g (lagrangeOmega g 1) eqX1 (eqY1 + s)
        eqX2 (eqY2 + s) eqX3 (eqY3 + s) = 0 := by
      intro s
      unfold rotY1 ky1
      rw [d2_shiftY s eqX1 eqY1 eqX2 eqY2, d2_shiftY s eqX1 eqY1 eqX3 eqY3,
        d2_anchor12, d2_anchor13, eqdx12, eqdx13]
      unfold eqX1 lagrangeOmega
      rw [div_sqrt3]
      ring
    have h := deriv_congr (hasDerivAt_const (c := 0) (x := 0))
      (fun s => (hE s).symm)
    exact h.congr_deriv (by unfold linY1; ring)
  · have hE : ∀ s : ℝ, rotX2 g (lagrangeOmega g 1) eqX1 (eqY1 + s)
        eqX2 (eqY2 + s) eqX3 (eqY3 + s)
        = lagrangeOmega g 1 * s := by
      intro s
      unfold rotX2 kx2
      rw [add_sub_add_eq eqY2 eqY1 s, add_sub_add_eq eqY2 eqY3 s,
        d2_shiftY s eqX1 eqY1 eqX2 eqY2, d2_shiftY s eqX2 eqY2 eqX3 eqY3,
        d2_anchor12, d2_anchor23, eqdy21, eqdy23]
      unfold eqY2 lagrangeOmega
      ring
    have h := deriv_congr (hasDerivAt_const_mul_id (lagrangeOmega g 1) 0)
      (fun s => (hE s).symm)
    exact h.congr_deriv (by unfold linX2 lagrangeOmega; ring)
  · have hE : ∀ s : ℝ, rotY2 g (lagrangeOmega g 1) eqX1 (eqY1 + s)
        eqX2 (eqY2 + s) eqX3 (eqY3 + s) = 0 := by
      intro s
      unfold rotY2 ky2
      rw [d2_shiftY s eqX1 eqY1 eqX2 eqY2, d2_shiftY s eqX2 eqY2 eqX3 eqY3,
        d2_anchor12, d2_anchor23, eqdx21, eqdx23]
      unfold eqX2 lagrangeOmega
      rw [div_2sqrt3]
      ring
    have h := deriv_congr (hasDerivAt_const (c := 0) (x := 0))
      (fun s => (hE s).symm)
    exact h.congr_deriv (by unfold linY2; ring)
  · have hE : ∀ s : ℝ, rotX3 g (lagrangeOmega g 1) eqX1 (eqY1 + s)
        eqX2 (eqY2 + s) eqX3 (eqY3 + s)
        = lagrangeOmega g 1 * s := by
      intro s
      unfold rotX3 kx3
      rw [add_sub_add_eq eqY3 eqY1 s, add_sub_add_eq eqY3 eqY2 s,
        d2_shiftY s eqX1 eqY1 eqX3 eqY3, d2_shiftY s eqX2 eqY2 eqX3 eqY3,
        d2_anchor13, d2_anchor23, eqdy31, eqdy32]
      unfold eqY3 lagrangeOmega
      ring
    have h := deriv_congr (hasDerivAt_const_mul_id (lagrangeOmega g 1) 0)
      (fun s => (hE s).symm)
    exact h.congr_deriv (by unfold linX3 lagrangeOmega; ring)
  · have hE : ∀ s : ℝ, rotY3 g (lagrangeOmega g 1) eqX1 (eqY1 + s)
        eqX2 (eqY2 + s) eqX3 (eqY3 + s) = 0 := by
      intro s
      unfold rotY3 ky3
      rw [d2_shiftY s eqX1 eqY1 eqX3 eqY3, d2_shiftY s eqX2 eqY2 eqX3 eqY3,
        d2_anchor13, d2_anchor23, eqdx31, eqdx32]
      unfold eqX3 lagrangeOmega
      rw [div_2sqrt3]
      ring
    have h := deriv_congr (hasDerivAt_const (c := 0) (x := 0))
      (fun s => (hE s).symm)
    exact h.congr_deriv (by unfold linY3; ring)

/-! ### certification: the true rotating-frame field along the shape modes -/

/-! The shape directions u = (1, 0, 1/2, −√3/2, 0, 0) and
    w = (0, 1, √3/2, 1/2, 0, 0) are not symmetry directions, so along
    their lines the Kirchhoff part of the rotating-frame field genuinely
    varies: the pairwise squared distances become quadratic polynomials
    of the line parameter.  The next eighteen private lemmas are the
    polynomial core (coordinate differences and squared distances along
    the two lines); all of them are exact identities in ℚ(√3). -/

private theorem lin_dxU12 (s : ℝ) :
    eqX1 + s - (eqX2 + s / 2) = Real.sqrt 3 / 2 + s / 2 := by
  linear_combination eqdx12

private theorem lin_dxU13 (s : ℝ) :
    eqX1 + s - eqX3 = Real.sqrt 3 / 2 + s := by
  linear_combination eqdx13

private theorem lin_dxU23 (s : ℝ) : eqX2 + s / 2 - eqX3 = s / 2 := by
  unfold eqX2 eqX3; ring

private theorem lin_dxU21 (s : ℝ) :
    eqX2 + s / 2 - (eqX1 + s) = -(Real.sqrt 3 / 2) - s / 2 := by
  linear_combination eqdx21

private theorem lin_dxU31 (s : ℝ) :
    eqX3 - (eqX1 + s) = -(Real.sqrt 3 / 2) - s := by
  linear_combination eqdx31

private theorem lin_dxU32 (s : ℝ) : eqX3 - (eqX2 + s / 2) = -s / 2 := by
  unfold eqX2 eqX3; ring

private theorem lin_dyU12 (s : ℝ) :
    eqY1 - (eqY2 - Real.sqrt 3 / 2 * s) = -(1 / 2) + Real.sqrt 3 / 2 * s := by
  linear_combination eqdy12

private theorem lin_dyU13 : eqY1 - eqY3 = 1 / 2 := eqdy13

private theorem lin_dyU23 (s : ℝ) :
    eqY2 - Real.sqrt 3 / 2 * s - eqY3 = 1 - Real.sqrt 3 / 2 * s := by
  linear_combination eqdy23

private theorem lin_dyU21 (s : ℝ) :
    eqY2 - Real.sqrt 3 / 2 * s - eqY1 = 1 / 2 - Real.sqrt 3 / 2 * s := by
  linear_combination eqdy21

private theorem lin_dyU31 : eqY3 - eqY1 = -(1 / 2) := eqdy31

private theorem lin_dyU32 (s : ℝ) :
    eqY3 - (eqY2 - Real.sqrt 3 / 2 * s) = -1 + Real.sqrt 3 / 2 * s := by
  linear_combination eqdy32

private theorem lin_d2U12 (s : ℝ) :
    d2 (eqX1 + s) eqY1 (eqX2 + s / 2) (eqY2 - Real.sqrt 3 / 2 * s) = 1 + s ^ 2 := by
  unfold d2
  rw [lin_dxU12, lin_dyU12]
  linear_combination ((1 + s ^ 2) / 4) * s3sq

private theorem lin_d2U13 (s : ℝ) :
    d2 (eqX1 + s) eqY1 eqX3 eqY3 = 1 + Real.sqrt 3 * s + s ^ 2 := by
  unfold d2
  rw [lin_dxU13, lin_dyU13]
  linear_combination (1 / 4) * s3sq

private theorem lin_d2U23 (s : ℝ) :
    d2 (eqX2 + s / 2) (eqY2 - Real.sqrt 3 / 2 * s) eqX3 eqY3
      = 1 - Real.sqrt 3 * s + s ^ 2 := by
  unfold d2
  rw [lin_dxU23, lin_dyU23]
  linear_combination (s ^ 2 / 4) * s3sq

private theorem lin_dxW12 (s : ℝ) :
    eqX1 - (eqX2 + Real.sqrt 3 / 2 * s) = Real.sqrt 3 / 2 - Real.sqrt 3 / 2 * s := by
  linear_combination eqdx12

private theorem lin_dyW12 (s : ℝ) :
    eqY1 + s - (eqY2 + s / 2) = -(1 / 2) + s / 2 := by
  linear_combination eqdy12

private theorem lin_dxW13 : eqX1 - eqX3 = Real.sqrt 3 / 2 := eqdx13

private theorem lin_dyW13 (s : ℝ) : eqY1 + s - eqY3 = 1 / 2 + s := by
  linear_combination eqdy13

private theorem lin_dxW21 (s : ℝ) :
    eqX2 + Real.sqrt 3 / 2 * s - eqX1 = -(Real.sqrt 3 / 2) + Real.sqrt 3 / 2 * s := by
  linear_combination eqdx21

private theorem lin_dyW21 (s : ℝ) :
    eqY2 + s / 2 - (eqY1 + s) = 1 / 2 - s / 2 := by
  linear_combination eqdy21

private theorem lin_dyW23 (s : ℝ) : eqY2 + s / 2 - eqY3 = 1 + s / 2 := by
  linear_combination eqdy23

private theorem lin_dxW23 (s : ℝ) :
    eqX2 + Real.sqrt 3 / 2 * s - eqX3 = Real.sqrt 3 / 2 * s := by
  unfold eqX2 eqX3; ring

private theorem lin_dyW31 (s : ℝ) :
    eqY3 - (eqY1 + s) = -(1 / 2) - s := by
  linear_combination eqdy31

private theorem lin_dxW31 : eqX3 - eqX1 = -(Real.sqrt 3 / 2) := eqdx31

private theorem lin_dyW32 (s : ℝ) :
    eqY3 - (eqY2 + s / 2) = -1 - s / 2 := by
  linear_combination eqdy32

private theorem lin_dxW32 (s : ℝ) :
    eqX3 - (eqX2 + Real.sqrt 3 / 2 * s) = -(Real.sqrt 3 / 2) * s := by
  unfold eqX2 eqX3; ring

private theorem lin_d2W12 (s : ℝ) :
    d2 eqX1 (eqY1 + s) (eqX2 + Real.sqrt 3 / 2 * s) (eqY2 + s / 2)
      = 1 - 2 * s + s ^ 2 := by
  unfold d2
  rw [lin_dxW12, lin_dyW12]
  linear_combination ((1 - s) ^ 2 / 4) * s3sq

private theorem lin_d2W13 (s : ℝ) :
    d2 eqX1 (eqY1 + s) eqX3 eqY3 = 1 + s + s ^ 2 := by
  unfold d2
  rw [lin_dxW13, lin_dyW13]
  linear_combination (1 / 4) * s3sq

private theorem lin_d2W23 (s : ℝ) :
    d2 (eqX2 + Real.sqrt 3 / 2 * s) (eqY2 + s / 2) eqX3 eqY3
      = 1 + s + s ^ 2 := by
  unfold d2
  rw [lin_dxW23, lin_dyW23]
  linear_combination (s ^ 2 / 4) * s3sq

private theorem lin_hasDerivAt_add_id (c t : ℝ) :
    HasDerivAt (fun s => c + s) 1 t :=
  ((hasDerivAt_const (c := c) (x := t)).add
    (hasDerivAt_id (𝕜 := ℝ) (x := t))).congr_deriv (by ring)

/-- **Certification of the shape mode u:** the derivative at t = 0 of the
    TRUE rotating-frame field, evaluated along the line
    anchor + t·(1, 0, 1/2, −√3/2, 0, 0), is exactly the linearization
    applied to that direction — all six components.  Unlike the
    translation lines, here the Kirchhoff quotients genuinely vary (two
    of the three squared distances become quadratic in the line
    parameter), so this certifies the interior rows of the Jacobian. -/
theorem lin_cert_shapeU (g : ℝ) :
    HasDerivAt (fun s => rotX1 g (lagrangeOmega g 1) (eqX1 + s) eqY1
        (eqX2 + s / 2) (eqY2 - Real.sqrt 3 / 2 * s) eqX3 eqY3)
      (g / (2 * Real.pi) * linX1 1 0 (1 / 2) (-Real.sqrt 3 / 2) 0 0) 0
    ∧ HasDerivAt (fun s => rotY1 g (lagrangeOmega g 1) (eqX1 + s) eqY1
        (eqX2 + s / 2) (eqY2 - Real.sqrt 3 / 2 * s) eqX3 eqY3)
      (g / (2 * Real.pi) * linY1 1 0 (1 / 2) (-Real.sqrt 3 / 2) 0 0) 0
    ∧ HasDerivAt (fun s => rotX2 g (lagrangeOmega g 1) (eqX1 + s) eqY1
        (eqX2 + s / 2) (eqY2 - Real.sqrt 3 / 2 * s) eqX3 eqY3)
      (g / (2 * Real.pi) * linX2 1 0 (1 / 2) (-Real.sqrt 3 / 2) 0 0) 0
    ∧ HasDerivAt (fun s => rotY2 g (lagrangeOmega g 1) (eqX1 + s) eqY1
        (eqX2 + s / 2) (eqY2 - Real.sqrt 3 / 2 * s) eqX3 eqY3)
      (g / (2 * Real.pi) * linY2 1 0 (1 / 2) (-Real.sqrt 3 / 2) 0 0) 0
    ∧ HasDerivAt (fun s => rotX3 g (lagrangeOmega g 1) (eqX1 + s) eqY1
        (eqX2 + s / 2) (eqY2 - Real.sqrt 3 / 2 * s) eqX3 eqY3)
      (g / (2 * Real.pi) * linX3 1 0 (1 / 2) (-Real.sqrt 3 / 2) 0 0) 0
    ∧ HasDerivAt (fun s => rotY3 g (lagrangeOmega g 1) (eqX1 + s) eqY1
        (eqX2 + s / 2) (eqY2 - Real.sqrt 3 / 2 * s) eqX3 eqY3)
      (g / (2 * Real.pi) * linY3 1 0 (1 / 2) (-Real.sqrt 3 / 2) 0 0) 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · -- rotX1: quotient 12 varies ((−1/2 + √3·s/2)/(1 + s²)), quotient 13
    -- varies ((1/2)/(1 + √3·s + s²)); the frame term is constant (y₁ rests).
    have hq12 : HasDerivAt (fun s => (-(1 / 2) + Real.sqrt 3 / 2 * s) / (1 + s ^ 2))
        ((Real.sqrt 3 / 2 * 1 - -(1 / 2) * 0) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 (-(1 / 2)) (Real.sqrt 3 / 2) 1 0 1
        (by norm_num)) (fun s => by ring)
    have hq13 : HasDerivAt (fun s => (1 / 2) / (1 + Real.sqrt 3 * s + s ^ 2))
        ((0 * 1 - 1 / 2 * Real.sqrt 3) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 (1 / 2) 0 1 (Real.sqrt 3) 1
        (by norm_num)) (fun s => by ring)
    have hfr : HasDerivAt (fun s => lagrangeOmega g 1 * eqY1) (0:ℝ) 0 :=
      hasDerivAt_const (c := lagrangeOmega g 1 * eqY1) (x := (0:ℝ))
    have hfull := (deriv_mul_const_left (hq12.add hq13)
      (c := -(g / (2 * Real.pi)))).add hfr
    exact deriv_congr hfull (fun s => by
      unfold rotX1 kx1
      rw [lin_dyU12, lin_d2U12, lin_dyU13, lin_d2U13]
      ring) |>.congr_deriv (by
        unfold linX1
        ring)
  · -- rotY1: quotients (√3/2 + s/2)/(1 + s²) and (√3/2 + s)/(1 + √3·s + s²);
    -- the frame term −ω·(eqX1 + s) is affine with slope −ω.
    have hq12 : HasDerivAt (fun s => (Real.sqrt 3 / 2 + s / 2) / (1 + s ^ 2))
        ((1 / 2 * 1 - Real.sqrt 3 / 2 * 0) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 (Real.sqrt 3 / 2) (1 / 2) 1 0 1
        (by norm_num)) (fun s => by ring)
    have hq13 : HasDerivAt (fun s => (Real.sqrt 3 / 2 + s) / (1 + Real.sqrt 3 * s + s ^ 2))
        ((1 * 1 - Real.sqrt 3 / 2 * Real.sqrt 3) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 (Real.sqrt 3 / 2) 1 1 (Real.sqrt 3) 1
        (by norm_num)) (fun s => by ring)
    have hfr := deriv_mul_const_left (lin_hasDerivAt_add_id eqX1 0)
      (c := -(lagrangeOmega g 1))
    have hfull := (deriv_mul_const_left (hq12.add hq13)
      (c := g / (2 * Real.pi))).add hfr
    exact deriv_congr hfull (fun s => by
      unfold rotY1 ky1
      rw [lin_dxU12, lin_d2U12, lin_dxU13, lin_d2U13]
      ring) |>.congr_deriv (by
        unfold linY1 lagrangeOmega
        linear_combination (-(3 * g / (8 * Real.pi))) * s3sq)
  · -- rotX2: quotients (1/2 − √3·s/2)/(1 + s²) and (1 − √3·s/2)/(1 − √3·s + s²);
    -- the frame term ω·(eqY2 − √3·s/2) has slope −ω·√3/2.
    have hq21 : HasDerivAt (fun s => (1 / 2 - Real.sqrt 3 / 2 * s) / (1 + s ^ 2))
        ((-(Real.sqrt 3 / 2) * 1 - 1 / 2 * 0) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 (1 / 2) (-(Real.sqrt 3 / 2)) 1 0 1
        (by norm_num)) (fun s => by ring)
    have hq23 : HasDerivAt (fun s => (1 - Real.sqrt 3 / 2 * s) / (1 - Real.sqrt 3 * s + s ^ 2))
        ((-(Real.sqrt 3 / 2) * 1 - 1 * -(Real.sqrt 3)) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 1 (-(Real.sqrt 3 / 2)) 1 (-(Real.sqrt 3)) 1
        (by norm_num)) (fun s => by ring)
    have hy2' : HasDerivAt (fun s => eqY2 - Real.sqrt 3 / 2 * s)
        (-(Real.sqrt 3 / 2)) 0 :=
      deriv_congr ((hasDerivAt_const (c := eqY2) (x := 0)).add
        (deriv_mul_const_left (hasDerivAt_id (𝕜 := ℝ) (x := 0))
          (c := -(Real.sqrt 3 / 2)))) (fun s => by simp only [id_eq]; ring)
        |>.congr_deriv (by ring)
    have hfull := (deriv_mul_const_left (hq21.add hq23)
      (c := -(g / (2 * Real.pi)))).add
      (deriv_mul_const_left hy2' (c := lagrangeOmega g 1))
    exact deriv_congr hfull (fun s => by
      unfold rotX2 kx2
      rw [lin_dyU21, lin_d2U12, lin_dyU23, lin_d2U23]
      ring) |>.congr_deriv (by
        unfold linX2 lagrangeOmega
        ring)
  · -- rotY2: quotients (−√3/2 − s/2)/(1 + s²) and (s/2)/(1 − √3·s + s²);
    -- the frame term −ω·(eqX2 + s/2) has slope −ω/2.
    have hq21 : HasDerivAt (fun s => (-(Real.sqrt 3 / 2) - s / 2) / (1 + s ^ 2))
        ((-(1 / 2) * 1 - -(Real.sqrt 3 / 2) * 0) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 (-(Real.sqrt 3 / 2)) (-(1 / 2)) 1 0 1
        (by norm_num)) (fun s => by ring)
    have hq23 : HasDerivAt (fun s => (s / 2) / (1 - Real.sqrt 3 * s + s ^ 2))
        ((1 / 2 * 1 - 0 * -(Real.sqrt 3)) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 0 (1 / 2) 1 (-(Real.sqrt 3)) 1
        (by norm_num)) (fun s => by ring)
    have hx2' : HasDerivAt (fun s => eqX2 + s / 2) (1 / 2) 0 :=
      deriv_congr ((hasDerivAt_const (c := eqX2) (x := 0)).add
        (deriv_mul_const_left (hasDerivAt_id (𝕜 := ℝ) (x := 0)) (c := 1 / 2)))
        (fun s => by simp only [id_eq]; ring) |>.congr_deriv (by ring)
    have hfull := (deriv_mul_const_left (hq21.add hq23)
      (c := g / (2 * Real.pi))).add
      (deriv_mul_const_left hx2' (c := -(lagrangeOmega g 1)))
    exact deriv_congr hfull (fun s => by
      unfold rotY2 ky2
      rw [lin_dxU21, lin_d2U12, lin_dxU23, lin_d2U23]
      ring) |>.congr_deriv (by
        unfold linY2 lagrangeOmega
        linear_combination (g / (8 * Real.pi)) * s3sq)
  · -- rotX3: quotients (−1/2)/(1 + √3·s + s²) and (−1 + √3·s/2)/(1 − √3·s + s²);
    -- the frame term ω·eqY3 is constant.
    have hq31 : HasDerivAt (fun s => (-(1 / 2)) / (1 + Real.sqrt 3 * s + s ^ 2))
        ((0 * 1 - -(1 / 2) * Real.sqrt 3) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 (-(1 / 2)) 0 1 (Real.sqrt 3) 1
        (by norm_num)) (fun s => by ring)
    have hq32 : HasDerivAt (fun s => (-1 + Real.sqrt 3 / 2 * s) / (1 - Real.sqrt 3 * s + s ^ 2))
        ((Real.sqrt 3 / 2 * 1 - -1 * -(Real.sqrt 3)) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 (-(1)) (Real.sqrt 3 / 2) 1 (-(Real.sqrt 3)) 1
        (by norm_num)) (fun s => by ring)
    have hfr : HasDerivAt (fun s => lagrangeOmega g 1 * eqY3) (0:ℝ) 0 :=
      hasDerivAt_const (c := lagrangeOmega g 1 * eqY3) (x := (0:ℝ))
    have hfull := (deriv_mul_const_left (hq31.add hq32)
      (c := -(g / (2 * Real.pi)))).add hfr
    exact deriv_congr hfull (fun s => by
      unfold rotX3 kx3
      rw [lin_dyU31, lin_d2U13, lin_dyU32, lin_d2U23]
      ring) |>.congr_deriv (by
        unfold linX3
        ring)
  · -- rotY3: quotients (−√3/2 − s)/(1 + √3·s + s²) and (−s/2)/(1 − √3·s + s²);
    -- the frame term −ω·eqX3 is constant.
    have hq31 : HasDerivAt (fun s => (-(Real.sqrt 3 / 2) - s) / (1 + Real.sqrt 3 * s + s ^ 2))
        ((-(1) * 1 - -(Real.sqrt 3 / 2) * Real.sqrt 3) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 (-(Real.sqrt 3 / 2)) (-(1)) 1 (Real.sqrt 3) 1
        (by norm_num)) (fun s => by ring)
    have hq32 : HasDerivAt (fun s => (-(s / 2)) / (1 - Real.sqrt 3 * s + s ^ 2))
        ((-(1 / 2) * 1 - 0 * -(Real.sqrt 3)) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 0 (-(1 / 2)) 1 (-(Real.sqrt 3)) 1
        (by norm_num)) (fun s => by ring)
    have hfr : HasDerivAt (fun s => -(lagrangeOmega g 1) * eqX3) (0:ℝ) 0 :=
      hasDerivAt_const (c := -(lagrangeOmega g 1) * eqX3) (x := (0:ℝ))
    have hfull := (deriv_mul_const_left (hq31.add hq32)
      (c := g / (2 * Real.pi))).add hfr
    exact deriv_congr hfull (fun s => by
      unfold rotY3 ky3
      rw [lin_dxU31, lin_d2U13, lin_dxU32, lin_d2U23]
      ring) |>.congr_deriv (by
        unfold linY3
        linear_combination (g / (4 * Real.pi)) * s3sq)

/-- **Certification of the shape mode w:** the same along the line
    anchor + t·(0, 1, √3/2, 1/2, 0, 0).  Together with `lin_cert_shapeU`
    every interior entry of the 2π/Γ-scaled Jacobian is now certified
    against the true rotating-frame field. -/
theorem lin_cert_shapeW (g : ℝ) :
    HasDerivAt (fun s => rotX1 g (lagrangeOmega g 1) eqX1 (eqY1 + s)
        (eqX2 + Real.sqrt 3 / 2 * s) (eqY2 + s / 2) eqX3 eqY3)
      (g / (2 * Real.pi) * linX1 0 1 (Real.sqrt 3 / 2) (1 / 2) 0 0) 0
    ∧ HasDerivAt (fun s => rotY1 g (lagrangeOmega g 1) eqX1 (eqY1 + s)
        (eqX2 + Real.sqrt 3 / 2 * s) (eqY2 + s / 2) eqX3 eqY3)
      (g / (2 * Real.pi) * linY1 0 1 (Real.sqrt 3 / 2) (1 / 2) 0 0) 0
    ∧ HasDerivAt (fun s => rotX2 g (lagrangeOmega g 1) eqX1 (eqY1 + s)
        (eqX2 + Real.sqrt 3 / 2 * s) (eqY2 + s / 2) eqX3 eqY3)
      (g / (2 * Real.pi) * linX2 0 1 (Real.sqrt 3 / 2) (1 / 2) 0 0) 0
    ∧ HasDerivAt (fun s => rotY2 g (lagrangeOmega g 1) eqX1 (eqY1 + s)
        (eqX2 + Real.sqrt 3 / 2 * s) (eqY2 + s / 2) eqX3 eqY3)
      (g / (2 * Real.pi) * linY2 0 1 (Real.sqrt 3 / 2) (1 / 2) 0 0) 0
    ∧ HasDerivAt (fun s => rotX3 g (lagrangeOmega g 1) eqX1 (eqY1 + s)
        (eqX2 + Real.sqrt 3 / 2 * s) (eqY2 + s / 2) eqX3 eqY3)
      (g / (2 * Real.pi) * linX3 0 1 (Real.sqrt 3 / 2) (1 / 2) 0 0) 0
    ∧ HasDerivAt (fun s => rotY3 g (lagrangeOmega g 1) eqX1 (eqY1 + s)
        (eqX2 + Real.sqrt 3 / 2 * s) (eqY2 + s / 2) eqX3 eqY3)
      (g / (2 * Real.pi) * linY3 0 1 (Real.sqrt 3 / 2) (1 / 2) 0 0) 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · -- rotX1: quotients (−1/2 + s/2)/(1 − 2·s + s²) and (1/2 + s)/(1 + s + s²);
    -- the frame term ω·(eqY1 + s) has slope ω.
    have hq12 : HasDerivAt (fun s => (-(1 / 2) + s / 2) / (1 - 2 * s + s ^ 2))
        ((1 / 2 * 1 - -(1 / 2) * -(2)) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 (-(1 / 2)) (1 / 2) 1 (-(2)) 1
        (by norm_num)) (fun s => by ring)
    have hq13 : HasDerivAt (fun s => (1 / 2 + s) / (1 + s + s ^ 2))
        ((1 * 1 - 1 / 2 * 1) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 (1 / 2) 1 1 1 1
        (by norm_num)) (fun s => by ring)
    have hy1 := lin_hasDerivAt_add_id eqY1 0
    have hfull := (deriv_mul_const_left (hq12.add hq13)
      (c := -(g / (2 * Real.pi)))).add
      (deriv_mul_const_left hy1 (c := lagrangeOmega g 1))
    exact deriv_congr hfull (fun s => by
      unfold rotX1 kx1
      rw [lin_dyW12, lin_d2W12, lin_dyW13, lin_d2W13]
      ring) |>.congr_deriv (by
        unfold linX1 lagrangeOmega
        linear_combination (-(g / (8 * Real.pi))) * s3sq)
  · -- rotY1: quotients (√3/2 − √3·s/2)/(1 − 2·s + s²) and (√3/2)/(1 + s + s²);
    -- the frame term −ω·eqX1 is constant.
    have hq12 : HasDerivAt (fun s => (Real.sqrt 3 / 2 - Real.sqrt 3 / 2 * s) / (1 - 2 * s + s ^ 2))
        ((-(Real.sqrt 3 / 2) * 1 - Real.sqrt 3 / 2 * -(2)) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 (Real.sqrt 3 / 2) (-(Real.sqrt 3 / 2)) 1 (-(2)) 1
        (by norm_num)) (fun s => by ring)
    have hq13 : HasDerivAt (fun s => (Real.sqrt 3 / 2) / (1 + s + s ^ 2))
        ((0 * 1 - Real.sqrt 3 / 2 * 1) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 (Real.sqrt 3 / 2) 0 1 1 1
        (by norm_num)) (fun s => by ring)
    have hfr : HasDerivAt (fun s => -(lagrangeOmega g 1) * eqX1) (0:ℝ) 0 :=
      hasDerivAt_const (c := -(lagrangeOmega g 1) * eqX1) (x := (0:ℝ))
    have hfull := (deriv_mul_const_left (hq12.add hq13)
      (c := g / (2 * Real.pi))).add hfr
    exact deriv_congr hfull (fun s => by
      unfold rotY1 ky1
      rw [lin_dxW12, lin_d2W12, lin_dxW13, lin_d2W13]
      ring) |>.congr_deriv (by
        unfold linY1
        ring)
  · -- rotX2: quotients (1/2 − s/2)/(1 − 2·s + s²) and (1 + s/2)/(1 + s + s²);
    -- the frame term ω·(eqY2 + s/2) has slope ω/2.
    have hq21 : HasDerivAt (fun s => (1 / 2 - s / 2) / (1 - 2 * s + s ^ 2))
        ((-(1 / 2) * 1 - 1 / 2 * -(2)) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 (1 / 2) (-(1 / 2)) 1 (-(2)) 1
        (by norm_num)) (fun s => by ring)
    have hq23 : HasDerivAt (fun s => (1 + s / 2) / (1 + s + s ^ 2))
        ((1 / 2 * 1 - 1 * 1) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 1 (1 / 2) 1 1 1
        (by norm_num)) (fun s => by ring)
    have hy2' := (hasDerivAt_const (c := eqY2) (x := 0)).add
      (deriv_mul_const_left (hasDerivAt_id (𝕜 := ℝ) (x := 0)) (c := 1 / 2))
    have hfull := (deriv_mul_const_left (hq21.add hq23)
      (c := -(g / (2 * Real.pi)))).add
      (deriv_mul_const_left hy2' (c := lagrangeOmega g 1))
    exact deriv_congr hfull (fun s => by
      unfold rotX2 kx2
      rw [lin_dyW21, lin_d2W12, lin_dyW23, lin_d2W23]
      simp only [id_eq]
      ring) |>.congr_deriv (by
        unfold linX2 lagrangeOmega
        linear_combination (g / (8 * Real.pi)) * s3sq)
  · -- rotY2: quotients (−√3/2 + √3·s/2)/(1 − 2·s + s²) and (√3·s/2)/(1 + s + s²);
    -- the frame term −ω·(eqX2 + √3·s/2) has slope −ω·√3/2.
    have hq21 : HasDerivAt (fun s => (-(Real.sqrt 3 / 2) + Real.sqrt 3 / 2 * s) / (1 - 2 * s + s ^ 2))
        ((Real.sqrt 3 / 2 * 1 - -(Real.sqrt 3 / 2) * -(2)) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 (-(Real.sqrt 3 / 2)) (Real.sqrt 3 / 2) 1 (-(2)) 1
        (by norm_num)) (fun s => by ring)
    have hq23 : HasDerivAt (fun s => (Real.sqrt 3 / 2 * s) / (1 + s + s ^ 2))
        ((Real.sqrt 3 / 2 * 1 - 0 * 1) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 0 (Real.sqrt 3 / 2) 1 1 1
        (by norm_num)) (fun s => by ring)
    have hx2' : HasDerivAt (fun s => eqX2 + Real.sqrt 3 / 2 * s)
        (Real.sqrt 3 / 2) 0 :=
      deriv_congr ((hasDerivAt_const (c := eqX2) (x := 0)).add
        (deriv_mul_const_left (hasDerivAt_id (𝕜 := ℝ) (x := 0))
          (c := Real.sqrt 3 / 2))) (fun s => by simp only [id_eq])
        |>.congr_deriv (by ring)
    have hfull := (deriv_mul_const_left (hq21.add hq23)
      (c := g / (2 * Real.pi))).add
      (deriv_mul_const_left hx2' (c := -(lagrangeOmega g 1)))
    exact deriv_congr hfull (fun s => by
      unfold rotY2 ky2
      rw [lin_dxW21, lin_d2W12, lin_dxW23, lin_d2W23]
      ring) |>.congr_deriv (by
        unfold linY2 lagrangeOmega
        ring)
  · -- rotX3: quotients (−1/2 − s)/(1 + s + s²) and (−1 − s/2)/(1 + s + s²);
    -- the frame term ω·eqY3 is constant.
    have hq31 : HasDerivAt (fun s => (-(1 / 2) - s) / (1 + s + s ^ 2))
        ((-(1) * 1 - -(1 / 2) * 1) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 (-(1 / 2)) (-(1)) 1 1 1
        (by norm_num)) (fun s => by ring)
    have hq32 : HasDerivAt (fun s => (-1 - s / 2) / (1 + s + s ^ 2))
        ((-(1 / 2) * 1 - -(1) * 1) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 (-(1)) (-(1 / 2)) 1 1 1
        (by norm_num)) (fun s => by ring)
    have hfr : HasDerivAt (fun s => lagrangeOmega g 1 * eqY3) (0:ℝ) 0 :=
      hasDerivAt_const (c := lagrangeOmega g 1 * eqY3) (x := (0:ℝ))
    have hfull := (deriv_mul_const_left (hq31.add hq32)
      (c := -(g / (2 * Real.pi)))).add hfr
    exact deriv_congr hfull (fun s => by
      unfold rotX3 kx3
      rw [lin_dyW31, lin_d2W13, lin_dyW32, lin_d2W23]
      ring) |>.congr_deriv (by
        unfold linX3
        ring)
  · -- rotY3: quotients (−√3/2)/(1 + s + s²) and (−√3·s/2)/(1 + s + s²);
    -- the frame term −ω·eqX3 is constant.
    have hq31 : HasDerivAt (fun s => (-(Real.sqrt 3 / 2)) / (1 + s + s ^ 2))
        ((0 * 1 - -(Real.sqrt 3 / 2) * 1) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 (-(Real.sqrt 3 / 2)) 0 1 1 1
        (by norm_num)) (fun s => by ring)
    have hq32 : HasDerivAt (fun s => (-(Real.sqrt 3 / 2 * s)) / (1 + s + s ^ 2))
        ((-(Real.sqrt 3 / 2) * 1 - 0 * 1) / 1 ^ 2) 0 :=
      deriv_congr (hasDerivAt_quot0 0 (-(Real.sqrt 3 / 2)) 1 1 1
        (by norm_num)) (fun s => by ring)
    have hfr : HasDerivAt (fun s => -(lagrangeOmega g 1) * eqX3) (0:ℝ) 0 :=
      hasDerivAt_const (c := -(lagrangeOmega g 1) * eqX3) (x := (0:ℝ))
    have hfull := (deriv_mul_const_left (hq31.add hq32)
      (c := g / (2 * Real.pi))).add hfr
    exact deriv_congr hfull (fun s => by
      unfold rotY3 ky3
      rw [lin_dxW31, lin_d2W13, lin_dxW32, lin_d2W23]
      ring) |>.congr_deriv (by
        unfold linY3
        ring)

/-! ### the modal solutions of the linearized rotating-frame equation -/

/-- Derivative of cos(c·s) at an arbitrary point (the composition of
    `Real.hasDerivAt_cos` with the linear map s ↦ c·s). -/
private theorem cos_comp (c t : ℝ) :
    HasDerivAt (fun s => Real.cos (c * s)) (-(Real.sin (c * t)) * c) t :=
  HasDerivAt.comp (𝕜 := ℝ) t (Real.hasDerivAt_cos (c * t))
    (hasDerivAt_const_mul_id c t)

/-- Derivative of sin(c·s) at an arbitrary point. -/
private theorem sin_comp (c t : ℝ) :
    HasDerivAt (fun s => Real.sin (c * s)) (Real.cos (c * t) * c) t :=
  HasDerivAt.comp (𝕜 := ℝ) t (Real.hasDerivAt_sin (c * t))
    (hasDerivAt_const_mul_id c t)

/-- The x-amplitude of the translation modal solution:
    b₁·cos(ωt) + b₂·sin(ωt). -/
noncomputable def transXamp (b1 b2 c t : ℝ) : ℝ :=
  b1 * Real.cos (c * t) + b2 * Real.sin (c * t)

/-- The y-amplitude of the translation modal solution:
    b₂·cos(ωt) − b₁·sin(ωt). -/
noncomputable def transYamp (b1 b2 c t : ℝ) : ℝ :=
  b2 * Real.cos (c * t) - b1 * Real.sin (c * t)

/-- The u-amplitude of the shape modal solution:
    p·cos(ωt) + q·sin(ωt). -/
noncomputable def shapeUamp (p q c t : ℝ) : ℝ :=
  p * Real.cos (c * t) + q * Real.sin (c * t)

/-- The w-amplitude of the shape modal solution:
    q·cos(ωt) − p·sin(ωt). -/
noncomputable def shapeWamp (p q c t : ℝ) : ℝ :=
  q * Real.cos (c * t) - p * Real.sin (c * t)

/-- The phase amplitude of the size modal solution: Q(t) = q − 2ω·p·t
    (the size amplitude stays p; the phase drifts linearly — the
    generalized zero eigenvalue of §8.3). -/
noncomputable def sizeDriftQ (p q c t : ℝ) : ℝ := q - 2 * c * p * t

/-! The linearization rows on the three invariant modal planes.  On the
    translation plane every perturbation is uniform, so the √3 terms of
    the rows cancel; on the shape plane they conspire to the rotation
    M0·u = −3·w, M0·w = +3·u; on the size plane M0·vD = −6·vR, M0·vR = 0
    (the generalized zero).  All values agree with the SymPy ladder
    (`notes/verify_identities_s8.py`, checks C–G). -/

private theorem linX1_trans (c1 c2 : ℝ) : linX1 c1 c2 c1 c2 c1 c2 = 3 * c2 := by
  unfold linX1; ring

private theorem linY1_trans (c1 c2 : ℝ) : linY1 c1 c2 c1 c2 c1 c2 = -3 * c1 := by
  unfold linY1; ring

private theorem linX2_trans (c1 c2 : ℝ) : linX2 c1 c2 c1 c2 c1 c2 = 3 * c2 := by
  unfold linX2; ring

private theorem linY2_trans (c1 c2 : ℝ) : linY2 c1 c2 c1 c2 c1 c2 = -3 * c1 := by
  unfold linY2; ring

private theorem linX3_trans (c1 c2 : ℝ) : linX3 c1 c2 c1 c2 c1 c2 = 3 * c2 := by
  unfold linX3; ring

private theorem linY3_trans (c1 c2 : ℝ) : linY3 c1 c2 c1 c2 c1 c2 = -3 * c1 := by
  unfold linY3; ring

private theorem linX1_shape (u w : ℝ) :
    linX1 u w (u / 2 + Real.sqrt 3 / 2 * w) (-(Real.sqrt 3 / 2) * u + w / 2) 0 0
      = 3 * w := by
  unfold linX1
  linear_combination (w / 4) * s3sq

private theorem linY1_shape (u w : ℝ) :
    linY1 u w (u / 2 + Real.sqrt 3 / 2 * w) (-(Real.sqrt 3 / 2) * u + w / 2) 0 0
      = -3 * u := by
  unfold linY1
  linear_combination (u / 4) * s3sq

private theorem linX2_shape (u w : ℝ) :
    linX2 u w (u / 2 + Real.sqrt 3 / 2 * w) (-(Real.sqrt 3 / 2) * u + w / 2) 0 0
      = -(3 * Real.sqrt 3 / 2) * u + 3 / 2 * w := by
  unfold linX2
  linear_combination (-(w / 4)) * s3sq

private theorem linY2_shape (u w : ℝ) :
    linY2 u w (u / 2 + Real.sqrt 3 / 2 * w) (-(Real.sqrt 3 / 2) * u + w / 2) 0 0
      = -(3 / 2) * u - 3 * Real.sqrt 3 / 2 * w := by
  unfold linY2
  linear_combination (-(u / 4)) * s3sq

private theorem linX3_shape (u w : ℝ) :
    linX3 u w (u / 2 + Real.sqrt 3 / 2 * w) (-(Real.sqrt 3 / 2) * u + w / 2) 0 0
      = 0 := by
  unfold linX3; ring

private theorem linY3_shape (u w : ℝ) :
    linY3 u w (u / 2 + Real.sqrt 3 / 2 * w) (-(Real.sqrt 3 / 2) * u + w / 2) 0 0
      = 0 := by
  unfold linY3; ring

private theorem linX1_size (p q : ℝ) :
    linX1 (p / Real.sqrt 3) (q / Real.sqrt 3)
        (-(p / (2 * Real.sqrt 3)) - q / 2) (p / 2 - q / (2 * Real.sqrt 3))
        (-(p / (2 * Real.sqrt 3)) + q / 2) (-p / 2 - q / (2 * Real.sqrt 3))
      = 0 := by
  unfold linX1
  simp only [div_sqrt3, div_2sqrt3]
  ring

private theorem linY1_size (p q : ℝ) :
    linY1 (p / Real.sqrt 3) (q / Real.sqrt 3)
        (-(p / (2 * Real.sqrt 3)) - q / 2) (p / 2 - q / (2 * Real.sqrt 3))
        (-(p / (2 * Real.sqrt 3)) + q / 2) (-p / 2 - q / (2 * Real.sqrt 3))
      = -6 * p / Real.sqrt 3 := by
  unfold linY1
  simp only [div_sqrt3, div_2sqrt3]
  ring

private theorem linX2_size (p q : ℝ) :
    linX2 (p / Real.sqrt 3) (q / Real.sqrt 3)
        (-(p / (2 * Real.sqrt 3)) - q / 2) (p / 2 - q / (2 * Real.sqrt 3))
        (-(p / (2 * Real.sqrt 3)) + q / 2) (-p / 2 - q / (2 * Real.sqrt 3))
      = 3 * p := by
  unfold linX2
  simp only [div_sqrt3, div_2sqrt3]
  linear_combination (p / 4) * s3sq

private theorem linY2_size (p q : ℝ) :
    linY2 (p / Real.sqrt 3) (q / Real.sqrt 3)
        (-(p / (2 * Real.sqrt 3)) - q / 2) (p / 2 - q / (2 * Real.sqrt 3))
        (-(p / (2 * Real.sqrt 3)) + q / 2) (-p / 2 - q / (2 * Real.sqrt 3))
      = 3 * p / Real.sqrt 3 := by
  unfold linY2
  simp only [div_sqrt3, div_2sqrt3]
  linear_combination (-(q / 4)) * s3sq

private theorem linX3_size (p q : ℝ) :
    linX3 (p / Real.sqrt 3) (q / Real.sqrt 3)
        (-(p / (2 * Real.sqrt 3)) - q / 2) (p / 2 - q / (2 * Real.sqrt 3))
        (-(p / (2 * Real.sqrt 3)) + q / 2) (-p / 2 - q / (2 * Real.sqrt 3))
      = -3 * p := by
  unfold linX3
  simp only [div_sqrt3, div_2sqrt3]
  linear_combination (-(p / 4)) * s3sq

private theorem linY3_size (p q : ℝ) :
    linY3 (p / Real.sqrt 3) (q / Real.sqrt 3)
        (-(p / (2 * Real.sqrt 3)) - q / 2) (p / 2 - q / (2 * Real.sqrt 3))
        (-(p / (2 * Real.sqrt 3)) + q / 2) (-p / 2 - q / (2 * Real.sqrt 3))
      = 3 * p / Real.sqrt 3 := by
  unfold linY3
  simp only [div_sqrt3, div_2sqrt3]
  linear_combination (q / 4) * s3sq

/-- **Modal solution — the translation pair (§8.4).**  For the initial
    uniform shift (b₁, b₂) the linearized rotating-frame equation is
    solved FOR ALL t by the uniformly shifted triangle whose offset
    rotates at exactly the Lagrange angular velocity
    ω = lagrangeOmega g 1: the derivative of every component equals the
    linearization (rows linX/linY) applied to the current perturbation.
    In the lab frame this is the exact Galilean shift of the Lagrange
    solution. -/
theorem lin_sol_trans (g b1 b2 t : ℝ) :
    HasDerivAt (fun s => eqX1 + transXamp b1 b2 (lagrangeOmega g 1) s)
      (g / (2 * Real.pi) * linX1 (transXamp b1 b2 (lagrangeOmega g 1) t)
        (transYamp b1 b2 (lagrangeOmega g 1) t)
        (transXamp b1 b2 (lagrangeOmega g 1) t)
        (transYamp b1 b2 (lagrangeOmega g 1) t)
        (transXamp b1 b2 (lagrangeOmega g 1) t)
        (transYamp b1 b2 (lagrangeOmega g 1) t)) t
    ∧ HasDerivAt (fun s => eqY1 + transYamp b1 b2 (lagrangeOmega g 1) s)
      (g / (2 * Real.pi) * linY1 (transXamp b1 b2 (lagrangeOmega g 1) t)
        (transYamp b1 b2 (lagrangeOmega g 1) t)
        (transXamp b1 b2 (lagrangeOmega g 1) t)
        (transYamp b1 b2 (lagrangeOmega g 1) t)
        (transXamp b1 b2 (lagrangeOmega g 1) t)
        (transYamp b1 b2 (lagrangeOmega g 1) t)) t
    ∧ HasDerivAt (fun s => eqX2 + transXamp b1 b2 (lagrangeOmega g 1) s)
      (g / (2 * Real.pi) * linX2 (transXamp b1 b2 (lagrangeOmega g 1) t)
        (transYamp b1 b2 (lagrangeOmega g 1) t)
        (transXamp b1 b2 (lagrangeOmega g 1) t)
        (transYamp b1 b2 (lagrangeOmega g 1) t)
        (transXamp b1 b2 (lagrangeOmega g 1) t)
        (transYamp b1 b2 (lagrangeOmega g 1) t)) t
    ∧ HasDerivAt (fun s => eqY2 + transYamp b1 b2 (lagrangeOmega g 1) s)
      (g / (2 * Real.pi) * linY2 (transXamp b1 b2 (lagrangeOmega g 1) t)
        (transYamp b1 b2 (lagrangeOmega g 1) t)
        (transXamp b1 b2 (lagrangeOmega g 1) t)
        (transYamp b1 b2 (lagrangeOmega g 1) t)
        (transXamp b1 b2 (lagrangeOmega g 1) t)
        (transYamp b1 b2 (lagrangeOmega g 1) t)) t
    ∧ HasDerivAt (fun s => eqX3 + transXamp b1 b2 (lagrangeOmega g 1) s)
      (g / (2 * Real.pi) * linX3 (transXamp b1 b2 (lagrangeOmega g 1) t)
        (transYamp b1 b2 (lagrangeOmega g 1) t)
        (transXamp b1 b2 (lagrangeOmega g 1) t)
        (transYamp b1 b2 (lagrangeOmega g 1) t)
        (transXamp b1 b2 (lagrangeOmega g 1) t)
        (transYamp b1 b2 (lagrangeOmega g 1) t)) t
    ∧ HasDerivAt (fun s => eqY3 + transYamp b1 b2 (lagrangeOmega g 1) s)
      (g / (2 * Real.pi) * linY3 (transXamp b1 b2 (lagrangeOmega g 1) t)
        (transYamp b1 b2 (lagrangeOmega g 1) t)
        (transXamp b1 b2 (lagrangeOmega g 1) t)
        (transYamp b1 b2 (lagrangeOmega g 1) t)
        (transXamp b1 b2 (lagrangeOmega g 1) t)
        (transYamp b1 b2 (lagrangeOmega g 1) t)) t := by
  have hX := (deriv_mul_const_left (cos_comp (lagrangeOmega g 1) t) (c := b1)).add
    (deriv_mul_const_left (sin_comp (lagrangeOmega g 1) t) (c := b2))
  have hY : HasDerivAt (fun s => transYamp b1 b2 (lagrangeOmega g 1) s)
      (b2 * (-(Real.sin (lagrangeOmega g 1 * t)) * lagrangeOmega g 1)
        - b1 * (Real.cos (lagrangeOmega g 1 * t) * lagrangeOmega g 1)) t :=
    deriv_congr ((deriv_mul_const_left (cos_comp (lagrangeOmega g 1) t) (c := b2)).add
      (deriv_mul_const_left (sin_comp (lagrangeOmega g 1) t) (c := -b1)))
      (fun s => by simp only [transYamp]; ring) |>.congr_deriv (by ring)
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · exact ((hasDerivAt_const (c := eqX1) (x := t)).add hX).congr_deriv (by
      rw [linX1_trans]
      simp only [transXamp, transYamp, lagrangeOmega]
      ring)
  · exact ((hasDerivAt_const (c := eqY1) (x := t)).add hY).congr_deriv (by
      rw [linY1_trans]
      simp only [transXamp, transYamp, lagrangeOmega]
      ring)
  · exact ((hasDerivAt_const (c := eqX2) (x := t)).add hX).congr_deriv (by
      rw [linX2_trans]
      simp only [transXamp, transYamp, lagrangeOmega]
      ring)
  · exact ((hasDerivAt_const (c := eqY2) (x := t)).add hY).congr_deriv (by
      rw [linY2_trans]
      simp only [transXamp, transYamp, lagrangeOmega]
      ring)
  · exact ((hasDerivAt_const (c := eqX3) (x := t)).add hX).congr_deriv (by
      rw [linX3_trans]
      simp only [transXamp, transYamp, lagrangeOmega]
      ring)
  · exact ((hasDerivAt_const (c := eqY3) (x := t)).add hY).congr_deriv (by
      rw [linY3_trans]
      simp only [transXamp, transYamp, lagrangeOmega]
      ring)

/-- **Modal solution — the shape pair (§8.4).**  For initial amplitudes
    (p, q) on the shape plane u, w the linearized rotating-frame equation
    is solved FOR ALL t by the shape oscillation at exactly the Lagrange
    angular velocity: u-amplitude p·cos ωt + q·sin ωt, w-amplitude
    q·cos ωt − p·sin ωt, vortex 3 resting.  This is the genuine interior
    oscillation of the perturbed triangle. -/
theorem lin_sol_shape (g p q t : ℝ) :
    HasDerivAt (fun s => eqX1 + shapeUamp p q (lagrangeOmega g 1) s)
      (g / (2 * Real.pi) * linX1 (shapeUamp p q (lagrangeOmega g 1) t)
        (shapeWamp p q (lagrangeOmega g 1) t)
        (shapeUamp p q (lagrangeOmega g 1) t / 2
          + Real.sqrt 3 / 2 * shapeWamp p q (lagrangeOmega g 1) t)
        (-(Real.sqrt 3 / 2) * shapeUamp p q (lagrangeOmega g 1) t
          + shapeWamp p q (lagrangeOmega g 1) t / 2) 0 0) t
    ∧ HasDerivAt (fun s => eqY1 + shapeWamp p q (lagrangeOmega g 1) s)
      (g / (2 * Real.pi) * linY1 (shapeUamp p q (lagrangeOmega g 1) t)
        (shapeWamp p q (lagrangeOmega g 1) t)
        (shapeUamp p q (lagrangeOmega g 1) t / 2
          + Real.sqrt 3 / 2 * shapeWamp p q (lagrangeOmega g 1) t)
        (-(Real.sqrt 3 / 2) * shapeUamp p q (lagrangeOmega g 1) t
          + shapeWamp p q (lagrangeOmega g 1) t / 2) 0 0) t
    ∧ HasDerivAt (fun s => eqX2 + shapeUamp p q (lagrangeOmega g 1) s / 2
        + Real.sqrt 3 / 2 * shapeWamp p q (lagrangeOmega g 1) s)
      (g / (2 * Real.pi) * linX2 (shapeUamp p q (lagrangeOmega g 1) t)
        (shapeWamp p q (lagrangeOmega g 1) t)
        (shapeUamp p q (lagrangeOmega g 1) t / 2
          + Real.sqrt 3 / 2 * shapeWamp p q (lagrangeOmega g 1) t)
        (-(Real.sqrt 3 / 2) * shapeUamp p q (lagrangeOmega g 1) t
          + shapeWamp p q (lagrangeOmega g 1) t / 2) 0 0) t
    ∧ HasDerivAt (fun s => eqY2 + -(Real.sqrt 3 / 2) * shapeUamp p q (lagrangeOmega g 1) s
        + shapeWamp p q (lagrangeOmega g 1) s / 2)
      (g / (2 * Real.pi) * linY2 (shapeUamp p q (lagrangeOmega g 1) t)
        (shapeWamp p q (lagrangeOmega g 1) t)
        (shapeUamp p q (lagrangeOmega g 1) t / 2
          + Real.sqrt 3 / 2 * shapeWamp p q (lagrangeOmega g 1) t)
        (-(Real.sqrt 3 / 2) * shapeUamp p q (lagrangeOmega g 1) t
          + shapeWamp p q (lagrangeOmega g 1) t / 2) 0 0) t
    ∧ HasDerivAt (fun s => eqX3)
      (g / (2 * Real.pi) * linX3 (shapeUamp p q (lagrangeOmega g 1) t)
        (shapeWamp p q (lagrangeOmega g 1) t)
        (shapeUamp p q (lagrangeOmega g 1) t / 2
          + Real.sqrt 3 / 2 * shapeWamp p q (lagrangeOmega g 1) t)
        (-(Real.sqrt 3 / 2) * shapeUamp p q (lagrangeOmega g 1) t
          + shapeWamp p q (lagrangeOmega g 1) t / 2) 0 0) t
    ∧ HasDerivAt (fun s => eqY3)
      (g / (2 * Real.pi) * linY3 (shapeUamp p q (lagrangeOmega g 1) t)
        (shapeWamp p q (lagrangeOmega g 1) t)
        (shapeUamp p q (lagrangeOmega g 1) t / 2
          + Real.sqrt 3 / 2 * shapeWamp p q (lagrangeOmega g 1) t)
        (-(Real.sqrt 3 / 2) * shapeUamp p q (lagrangeOmega g 1) t
          + shapeWamp p q (lagrangeOmega g 1) t / 2) 0 0) t := by
  have hU := (deriv_mul_const_left (cos_comp (lagrangeOmega g 1) t) (c := p)).add
    (deriv_mul_const_left (sin_comp (lagrangeOmega g 1) t) (c := q))
  have hW : HasDerivAt (fun s => shapeWamp p q (lagrangeOmega g 1) s)
      (q * (-(Real.sin (lagrangeOmega g 1 * t)) * lagrangeOmega g 1)
        - p * (Real.cos (lagrangeOmega g 1 * t) * lagrangeOmega g 1)) t :=
    deriv_congr ((deriv_mul_const_left (cos_comp (lagrangeOmega g 1) t) (c := q)).add
      (deriv_mul_const_left (sin_comp (lagrangeOmega g 1) t) (c := -p)))
      (fun s => by simp only [shapeWamp]; ring) |>.congr_deriv (by ring)
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · exact ((hasDerivAt_const (c := eqX1) (x := t)).add hU).congr_deriv (by
      rw [linX1_shape]
      simp only [shapeUamp, shapeWamp, lagrangeOmega]
      ring)
  · exact ((hasDerivAt_const (c := eqY1) (x := t)).add hW).congr_deriv (by
      rw [linY1_shape]
      simp only [shapeUamp, shapeWamp, lagrangeOmega]
      ring)
  · exact deriv_congr ((hasDerivAt_const (c := eqX2) (x := t)).add
      ((deriv_mul_const_left hU (c := 1 / 2)).add
        (deriv_mul_const_left hW (c := Real.sqrt 3 / 2))))
      (fun s => by simp only [shapeUamp, shapeWamp]; ring) |>.congr_deriv (by
        rw [linX2_shape]
        simp only [shapeUamp, shapeWamp, lagrangeOmega]
        ring)
  · exact deriv_congr ((hasDerivAt_const (c := eqY2) (x := t)).add
      ((deriv_mul_const_left hU (c := -(Real.sqrt 3 / 2))).add
        (deriv_mul_const_left hW (c := 1 / 2))))
      (fun s => by simp only [shapeUamp, shapeWamp]; ring) |>.congr_deriv (by
        rw [linY2_shape]
        simp only [shapeUamp, shapeWamp, lagrangeOmega]
        ring)
  · exact (hasDerivAt_const (c := eqX3) (x := t)).congr_deriv (by
      rw [linX3_shape]
      ring)
  · exact (hasDerivAt_const (c := eqY3) (x := t)).congr_deriv (by
      rw [linY3_shape]
      ring)

/-- **Modal solution — the size drift (§8.4).**  For initial data (p, q)
    on the size plane vD, vR (vD = the anchor, vR = J·vD the phase
    direction) the linearized rotating-frame equation is solved FOR ALL
    t by: the size amplitude stays p, the phase amplitude drifts
    linearly, Q(t) = q − 2ω·p·t — the generalized zero eigenvalue: no
    growth, but no restoration either. -/
theorem lin_sol_size (g p q t : ℝ) :
    HasDerivAt (fun s => eqX1 + p / Real.sqrt 3)
      (g / (2 * Real.pi) * linX1 (p / Real.sqrt 3)
        (sizeDriftQ p q (lagrangeOmega g 1) t / Real.sqrt 3)
        (-(p / (2 * Real.sqrt 3)) - sizeDriftQ p q (lagrangeOmega g 1) t / 2)
        (p / 2 - sizeDriftQ p q (lagrangeOmega g 1) t / (2 * Real.sqrt 3))
        (-(p / (2 * Real.sqrt 3)) + sizeDriftQ p q (lagrangeOmega g 1) t / 2)
        (-p / 2 - sizeDriftQ p q (lagrangeOmega g 1) t / (2 * Real.sqrt 3))) t
    ∧ HasDerivAt (fun s => eqY1 + sizeDriftQ p q (lagrangeOmega g 1) s / Real.sqrt 3)
      (g / (2 * Real.pi) * linY1 (p / Real.sqrt 3)
        (sizeDriftQ p q (lagrangeOmega g 1) t / Real.sqrt 3)
        (-(p / (2 * Real.sqrt 3)) - sizeDriftQ p q (lagrangeOmega g 1) t / 2)
        (p / 2 - sizeDriftQ p q (lagrangeOmega g 1) t / (2 * Real.sqrt 3))
        (-(p / (2 * Real.sqrt 3)) + sizeDriftQ p q (lagrangeOmega g 1) t / 2)
        (-p / 2 - sizeDriftQ p q (lagrangeOmega g 1) t / (2 * Real.sqrt 3))) t
    ∧ HasDerivAt (fun s => eqX2 + (-(p / (2 * Real.sqrt 3))
        - sizeDriftQ p q (lagrangeOmega g 1) s / 2))
      (g / (2 * Real.pi) * linX2 (p / Real.sqrt 3)
        (sizeDriftQ p q (lagrangeOmega g 1) t / Real.sqrt 3)
        (-(p / (2 * Real.sqrt 3)) - sizeDriftQ p q (lagrangeOmega g 1) t / 2)
        (p / 2 - sizeDriftQ p q (lagrangeOmega g 1) t / (2 * Real.sqrt 3))
        (-(p / (2 * Real.sqrt 3)) + sizeDriftQ p q (lagrangeOmega g 1) t / 2)
        (-p / 2 - sizeDriftQ p q (lagrangeOmega g 1) t / (2 * Real.sqrt 3))) t
    ∧ HasDerivAt (fun s => eqY2 + (p / 2
        - sizeDriftQ p q (lagrangeOmega g 1) s / (2 * Real.sqrt 3)))
      (g / (2 * Real.pi) * linY2 (p / Real.sqrt 3)
        (sizeDriftQ p q (lagrangeOmega g 1) t / Real.sqrt 3)
        (-(p / (2 * Real.sqrt 3)) - sizeDriftQ p q (lagrangeOmega g 1) t / 2)
        (p / 2 - sizeDriftQ p q (lagrangeOmega g 1) t / (2 * Real.sqrt 3))
        (-(p / (2 * Real.sqrt 3)) + sizeDriftQ p q (lagrangeOmega g 1) t / 2)
        (-p / 2 - sizeDriftQ p q (lagrangeOmega g 1) t / (2 * Real.sqrt 3))) t
    ∧ HasDerivAt (fun s => eqX3 + (-(p / (2 * Real.sqrt 3))
        + sizeDriftQ p q (lagrangeOmega g 1) s / 2))
      (g / (2 * Real.pi) * linX3 (p / Real.sqrt 3)
        (sizeDriftQ p q (lagrangeOmega g 1) t / Real.sqrt 3)
        (-(p / (2 * Real.sqrt 3)) - sizeDriftQ p q (lagrangeOmega g 1) t / 2)
        (p / 2 - sizeDriftQ p q (lagrangeOmega g 1) t / (2 * Real.sqrt 3))
        (-(p / (2 * Real.sqrt 3)) + sizeDriftQ p q (lagrangeOmega g 1) t / 2)
        (-p / 2 - sizeDriftQ p q (lagrangeOmega g 1) t / (2 * Real.sqrt 3))) t
    ∧ HasDerivAt (fun s => eqY3 + (-p / 2
        - sizeDriftQ p q (lagrangeOmega g 1) s / (2 * Real.sqrt 3)))
      (g / (2 * Real.pi) * linY3 (p / Real.sqrt 3)
        (sizeDriftQ p q (lagrangeOmega g 1) t / Real.sqrt 3)
        (-(p / (2 * Real.sqrt 3)) - sizeDriftQ p q (lagrangeOmega g 1) t / 2)
        (p / 2 - sizeDriftQ p q (lagrangeOmega g 1) t / (2 * Real.sqrt 3))
        (-(p / (2 * Real.sqrt 3)) + sizeDriftQ p q (lagrangeOmega g 1) t / 2)
        (-p / 2 - sizeDriftQ p q (lagrangeOmega g 1) t / (2 * Real.sqrt 3))) t := by
  have hQ : HasDerivAt (fun s => sizeDriftQ p q (lagrangeOmega g 1) s)
      (-(2 * lagrangeOmega g 1 * p)) t :=
    deriv_congr (hasDerivAt_affine q (-(2 * lagrangeOmega g 1 * p)) t)
      (fun s => by simp only [sizeDriftQ]; ring)
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · exact (hasDerivAt_const (c := eqX1 + p / Real.sqrt 3) (x := t)).congr_deriv (by
      rw [linX1_size]
      ring)
  · exact deriv_congr ((hasDerivAt_const (c := eqY1) (x := t)).add
      (deriv_mul_const_left hQ (c := 1 / Real.sqrt 3)))
      (fun s => by simp only [sizeDriftQ]; ring) |>.congr_deriv (by
        rw [linY1_size]
        simp only [sizeDriftQ, lagrangeOmega]
        ring)
  · exact deriv_congr ((hasDerivAt_const
      (c := eqX2 + -(p / (2 * Real.sqrt 3))) (x := t)).add
      (deriv_mul_const_left hQ (c := -(1 / 2))))
      (fun s => by ring) |>.congr_deriv (by
        rw [linX2_size]
        simp only [sizeDriftQ, lagrangeOmega]
        ring)
  · exact deriv_congr ((hasDerivAt_const
      (c := eqY2 + p / 2) (x := t)).add
      (deriv_mul_const_left hQ (c := -(1 / (2 * Real.sqrt 3)))))
      (fun s => by ring) |>.congr_deriv (by
        rw [linY2_size]
        simp only [sizeDriftQ, lagrangeOmega]
        ring)
  · exact deriv_congr ((hasDerivAt_const
      (c := eqX3 + -(p / (2 * Real.sqrt 3))) (x := t)).add
      (deriv_mul_const_left hQ (c := 1 / 2)))
      (fun s => by ring) |>.congr_deriv (by
        rw [linX3_size]
        simp only [sizeDriftQ, lagrangeOmega]
        ring)
  · exact deriv_congr ((hasDerivAt_const
      (c := eqY3 + -(p / 2)) (x := t)).add
      (deriv_mul_const_left hQ (c := -(1 / (2 * Real.sqrt 3)))))
      (fun s => by ring) |>.congr_deriv (by
        rw [linY3_size]
        simp only [sizeDriftQ, lagrangeOmega]
        ring)

/-! ### the stability bounds (§8.5) -/

/-- The size plane (vD = anchor, vR = J·anchor) is an orthonormal frame:
    |vD|² = |vR|² = 1 and vD·vR = 0.  Consequently the modal norm
    sqrt(p² + Q²) IS the Euclidean norm of the size modal perturbation
    p·vD + Q·vR, and `lin_bound_size` is a genuine norm bound. -/
theorem lin_size_basis :
    (1 / Real.sqrt 3) ^ 2 + 0 ^ 2 + (-(1 / (2 * Real.sqrt 3))) ^ 2 + (1 / 2) ^ 2
        + (-(1 / (2 * Real.sqrt 3))) ^ 2 + (-(1 / 2)) ^ 2 = 1
    ∧ (1 / Real.sqrt 3) * 0 + 0 * (1 / Real.sqrt 3)
        + (-(1 / (2 * Real.sqrt 3))) * (-1 / 2)
        + (1 / 2) * (-(1 / (2 * Real.sqrt 3)))
        + (-(1 / (2 * Real.sqrt 3))) * (1 / 2)
        + (-(1 / 2)) * (-(1 / (2 * Real.sqrt 3))) = 0
    ∧ 0 ^ 2 + (1 / Real.sqrt 3) ^ 2 + (-1 / 2) ^ 2
        + (-(1 / (2 * Real.sqrt 3))) ^ 2 + (1 / 2) ^ 2
        + (-(1 / (2 * Real.sqrt 3))) ^ 2 = 1 := by
  refine ⟨?_, ?_, ?_⟩
  · simp only [div_sqrt3, div_2sqrt3]
    linear_combination (1 / 6) * s3sq
  · ring
  · simp only [div_sqrt3, div_2sqrt3]
    linear_combination (1 / 6) * s3sq

/-- **Stability of the translation pair (§8.5).**  The Euclidean norm of
    the translation modal perturbation is EXACTLY preserved: the offset
    (b₁·cos ωt + b₂·sin ωt, b₂·cos ωt − b₁·sin ωt) has squared norm
    b₁² + b₂² for every t — pure rotation of the offset vector. -/
theorem lin_bound_trans (g b1 b2 t : ℝ) :
    transXamp b1 b2 (lagrangeOmega g 1) t ^ 2
      + transYamp b1 b2 (lagrangeOmega g 1) t ^ 2 = b1 ^ 2 + b2 ^ 2 := by
  unfold transXamp transYamp
  linear_combination (b1 ^ 2 + b2 ^ 2) *
    (Real.sin_sq_add_cos_sq (lagrangeOmega g 1 * t))

/-- **Stability of the shape pair (§8.5).**  The Euclidean norm of the
    shape modal perturbation is EXACTLY preserved: (p·cos ωt + q·sin ωt)²
    + (q·cos ωt − p·sin ωt)² = p² + q² for every t — the shape plane
    oscillates without growth. -/
theorem lin_bound_shape (g p q t : ℝ) :
    shapeUamp p q (lagrangeOmega g 1) t ^ 2
      + shapeWamp p q (lagrangeOmega g 1) t ^ 2 = p ^ 2 + q ^ 2 := by
  unfold shapeUamp shapeWamp
  linear_combination (p ^ 2 + q ^ 2) *
    (Real.sin_sq_add_cos_sq (lagrangeOmega g 1 * t))

/-- **Stability of the size drift (§8.5).**  The modal norm of the size
    perturbation grows AT MOST LINEARLY in time,
      sqrt(p² + Q(t)²) ≤ sqrt(p² + q²) + 2·|ω·p·t|,
    and by `lin_size_basis` the same bound holds for the Euclidean norm
    of the full 6-component perturbation.  In particular NO eigenmode of
    the linearized rotating-frame flow grows exponentially — the
    equilateral triangle of equal vortices is linearly (spectrally)
    stable, the classical Thomson criterion at N = 3. -/
theorem lin_bound_size (g p q t : ℝ) :
    Real.sqrt (p ^ 2 + sizeDriftQ p q (lagrangeOmega g 1) t ^ 2)
      ≤ Real.sqrt (p ^ 2 + q ^ 2) + 2 * abs (lagrangeOmega g 1 * p * t) := by
  simp only [sizeDriftQ]
  have hRabs : abs (2 * lagrangeOmega g 1 * p * t)
      = 2 * abs (lagrangeOmega g 1 * p * t) := by
    rw [abs_mul, abs_mul, abs_mul, abs_mul, abs_mul,
      abs_of_pos (by norm_num : (0 : ℝ) < 2)]
    ring
  have hqle : abs q ≤ Real.sqrt (p ^ 2 + q ^ 2) := by
    have h1 : q ^ 2 ≤ p ^ 2 + q ^ 2 := le_add_of_nonneg_left (sq_nonneg p)
    have h2 : Real.sqrt (q ^ 2) ≤ Real.sqrt (p ^ 2 + q ^ 2) :=
      Real.sqrt_le_sqrt h1
    rwa [Real.sqrt_sq_eq_abs] at h2
  have hR : 2 * lagrangeOmega g 1 * p * t = 2 * lagrangeOmega g 1 * p * t := rfl
  have hkey : -(q * (2 * lagrangeOmega g 1 * p * t))
      ≤ abs q * abs (2 * lagrangeOmega g 1 * p * t) := by
    have h4 : -(q * (2 * lagrangeOmega g 1 * p * t))
        ≤ abs (-(q * (2 * lagrangeOmega g 1 * p * t))) := le_abs_self _
    rwa [abs_neg, abs_mul] at h4
  have hRpos : 0 ≤ abs (2 * lagrangeOmega g 1 * p * t) := abs_nonneg _
  have hkey2 : -(q * (2 * lagrangeOmega g 1 * p * t))
      ≤ Real.sqrt (p ^ 2 + q ^ 2) * abs (2 * lagrangeOmega g 1 * p * t) :=
    le_trans hkey (mul_le_mul_of_nonneg_right hqle hRpos)
  have hsqr : p ^ 2 + (q - 2 * lagrangeOmega g 1 * p * t) ^ 2
      ≤ (Real.sqrt (p ^ 2 + q ^ 2) + abs (2 * lagrangeOmega g 1 * p * t)) ^ 2 := by
    have e : (Real.sqrt (p ^ 2 + q ^ 2) + abs (2 * lagrangeOmega g 1 * p * t)) ^ 2
        = Real.sqrt (p ^ 2 + q ^ 2) ^ 2
          + 2 * Real.sqrt (p ^ 2 + q ^ 2) * abs (2 * lagrangeOmega g 1 * p * t)
          + abs (2 * lagrangeOmega g 1 * p * t) ^ 2 := by ring
    have hN : Real.sqrt (p ^ 2 + q ^ 2) ^ 2 = p ^ 2 + q ^ 2 :=
      Real.sq_sqrt (by positivity)
    have hsq2 : abs (2 * lagrangeOmega g 1 * p * t) ^ 2
        = (2 * lagrangeOmega g 1 * p * t) ^ 2 := sq_abs _
    rw [e, hN, hsq2]
    have hexpand : (q - 2 * lagrangeOmega g 1 * p * t) ^ 2
        = q ^ 2 - 2 * q * (2 * lagrangeOmega g 1 * p * t)
          + (2 * lagrangeOmega g 1 * p * t) ^ 2 := by ring
    rw [hexpand]
    linarith [hkey2]
  have h1 : 0 ≤ Real.sqrt (p ^ 2 + q ^ 2)
      + abs (2 * lagrangeOmega g 1 * p * t) := by positivity
  have hfinal : Real.sqrt (p ^ 2 + (q - 2 * lagrangeOmega g 1 * p * t) ^ 2)
      ≤ Real.sqrt (p ^ 2 + q ^ 2) + abs (2 * lagrangeOmega g 1 * p * t) := by
    calc Real.sqrt (p ^ 2 + (q - 2 * lagrangeOmega g 1 * p * t) ^ 2)
        ≤ Real.sqrt ((Real.sqrt (p ^ 2 + q ^ 2)
            + abs (2 * lagrangeOmega g 1 * p * t)) ^ 2) :=
          Real.sqrt_le_sqrt hsqr
      _ = Real.sqrt (p ^ 2 + q ^ 2) + abs (2 * lagrangeOmega g 1 * p * t) := by
          rw [Real.sqrt_sq h1]
  rw [← hRabs]
  exact hfinal

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

#print axioms vortexDist_scale
#print axioms Pvortex_scale
#print axioms Qvortex_scale
#print axioms Ivortex_scale
#print axioms Hvortex_scale
#print axioms lag_rotation_x
#print axioms lag_rotation_y
#print axioms lag_deriv_field_x
#print axioms lag_deriv_field_y
#print axioms lag_orbit_radius
#print axioms lag_period_closed
#print axioms lagX_periodic
#print axioms lagY_periodic
#print axioms lagX_half_period
#print axioms lagY_half_period
#print axioms lag_cycle_x0
#print axioms lag_cycle_x1
#print axioms lag_cycle_x2
#print axioms lag_cycle_y0
#print axioms lag_cycle_y1
#print axioms lag_cycle_y2
#print axioms lag_kx0_field
#print axioms lag_kx1_field
#print axioms lag_kx2_field
#print axioms lag_ky0_field
#print axioms lag_ky1_field
#print axioms lag_ky2_field
#print axioms lag_omega_unique
#print axioms lagomega_ne_zero
#print axioms lagomega_pos_iff
#print axioms lagomega_scale
#print axioms lagX_scale
#print axioms lagY_scale
#print axioms lagX_zero
#print axioms lagY_zero
#print axioms lag_trajectory_scale_x
#print axioms lag_trajectory_scale_y
#print axioms lag_dist01
#print axioms lag_dist02
#print axioms lag_dist12
#print axioms lagrange_side_H
#print axioms lagrange_side_P
#print axioms lagrange_side_Q
#print axioms lagrange_side_I

#print axioms rot_anchor
#print axioms eig_trans1
#print axioms eig_trans2
#print axioms eig_rot
#print axioms eig_dil
#print axioms eig_shapeU
#print axioms eig_shapeW
#print axioms lin_cert_transX
#print axioms lin_cert_transY
#print axioms lin_cert_shapeU
#print axioms lin_cert_shapeW
#print axioms lin_sol_trans
#print axioms lin_sol_shape
#print axioms lin_sol_size
#print axioms lin_size_basis
#print axioms lin_bound_trans
#print axioms lin_bound_shape
#print axioms lin_bound_size











/-! ## Section 9 — Nonlinear continuation of the modes; bifurcation
     analysis at unequal circulations -/

/-! ### 9.1 The general-circulation Lagrange family

For ARBITRARY circulations (g1, g2, g3) with nonzero total G = g1+g2+g3
the equilateral triangle persists as an exact relative equilibrium: the
configuration w_k(t) = R(ωt)·(a·q_k + τ) with the circulation-weighted
centroid at the origin (τ = −a·ΣΓ_j q_j / G) rotates rigidly at

    ω = G / (2πa²),

the direct generalization of the §7 frequency ω = 3Γ/(2πa²) at Γ1=Γ2=Γ3.
This is the nonlinear continuation of the Lagrange branch through the
whole circulation simplex — including mixed-sign circulations, where the
bifurcation analysis of §9.3 shows the spectral transition. -/

/-- The general-circulation angular frequency: ω = G/(2πa²) with
    G = Γ1+Γ2+Γ3 (the Kirchhoff generalization of `lagrangeOmega`). -/
noncomputable def genOmega (g1 g2 g3 a : ℝ) : ℝ :=
  (g1 + g2 + g3) / (2 * Real.pi * a ^ 2)

/-- The x-translation placing the circulation-weighted centroid of the
    side-a equilateral triangle at the origin. -/
noncomputable def tauX (g1 g2 g3 a : ℝ) : ℝ :=
  -a * (g1 * eqX1 + g2 * eqX2 + g3 * eqX3) / (g1 + g2 + g3)

/-- The y-translation placing the circulation-weighted centroid of the
    side-a equilateral triangle at the origin. -/
noncomputable def tauY (g1 g2 g3 a : ℝ) : ℝ :=
  -a * (g1 * eqY1 + g2 * eqY2 + g3 * eqY3) / (g1 + g2 + g3)

/-- The x-coordinate of vortex k of the general-circulation relative
    equilibrium: the §7 rotated triangle translated by the rotating
    centroid-offset (τx(t), τy(t)) = R(ωt)·(τx, τy). -/
noncomputable def genX (g1 g2 g3 a t : ℝ) (k : ℕ) : ℝ :=
  lagX a (genOmega g1 g2 g3 a) t k
    + Real.cos (genOmega g1 g2 g3 a * t) * tauX g1 g2 g3 a
    - Real.sin (genOmega g1 g2 g3 a * t) * tauY g1 g2 g3 a

/-- The y-coordinate twin of `genX`. -/
noncomputable def genY (g1 g2 g3 a t : ℝ) (k : ℕ) : ℝ :=
  lagY a (genOmega g1 g2 g3 a) t k
    + Real.sin (genOmega g1 g2 g3 a * t) * tauX g1 g2 g3 a
    + Real.cos (genOmega g1 g2 g3 a * t) * tauY g1 g2 g3 a

/-- **Rigid rotation of the general-circulation triangle (x).**  Whatever
    the circulations, the continued family rotates rigidly:
    d/dt x_k = −ω·y_k with ω = G/(2πa²). -/
theorem s9_gen_deriv_x (g1 g2 g3 a t : ℝ) (k : ℕ) :
    HasDerivAt (fun s => genX g1 g2 g3 a s k)
      (-(genOmega g1 g2 g3 a) * genY g1 g2 g3 a t k) t := by
  have h1 : HasDerivAt (fun s => lagX a (genOmega g1 g2 g3 a) s k)
      (-(genOmega g1 g2 g3 a) * lagY a (genOmega g1 g2 g3 a) t k) t :=
    lag_deriv_field_x a (genOmega g1 g2 g3 a) t k
  have hc := cos_comp (genOmega g1 g2 g3 a) t
  have hs := sin_comp (genOmega g1 g2 g3 a) t
  have h2 := (hc.const_mul (tauX g1 g2 g3 a)).sub (hs.const_mul (tauY g1 g2 g3 a))
  have h := h1.add h2
  refine (deriv_congr h (by intro s; unfold genX; ring)).congr_deriv ?_
  unfold genY
  ring

/-- **Rigid rotation of the general-circulation triangle (y).** -/
theorem s9_gen_deriv_y (g1 g2 g3 a t : ℝ) (k : ℕ) :
    HasDerivAt (fun s => genY g1 g2 g3 a s k)
      (genOmega g1 g2 g3 a * genX g1 g2 g3 a t k) t := by
  have h1 : HasDerivAt (fun s => lagY a (genOmega g1 g2 g3 a) s k)
      (genOmega g1 g2 g3 a * lagX a (genOmega g1 g2 g3 a) t k) t :=
    lag_deriv_field_y a (genOmega g1 g2 g3 a) t k
  have hc := cos_comp (genOmega g1 g2 g3 a) t
  have hs := sin_comp (genOmega g1 g2 g3 a) t
  have h2 := (hs.const_mul (tauX g1 g2 g3 a)).add (hc.const_mul (tauY g1 g2 g3 a))
  have h := h1.add h2
  refine (deriv_congr h (by intro s; unfold genY; ring)).congr_deriv ?_
  unfold genX
  ring

/-- The continued triangle has the same pairwise distances as the §7
    triangle: the translation cancels in every difference (pair 1,2). -/
theorem s9_gen_dist01 (g1 g2 g3 a t : ℝ) :
    d2 (genX g1 g2 g3 a t 0) (genY g1 g2 g3 a t 0)
      (genX g1 g2 g3 a t 1) (genY g1 g2 g3 a t 1) = a ^ 2 := by
  have hxx : genX g1 g2 g3 a t 0 - genX g1 g2 g3 a t 1
      = lagX a (genOmega g1 g2 g3 a) t 0 - lagX a (genOmega g1 g2 g3 a) t 1 := by
    unfold genX; ring
  have hyy : genY g1 g2 g3 a t 0 - genY g1 g2 g3 a t 1
      = lagY a (genOmega g1 g2 g3 a) t 0 - lagY a (genOmega g1 g2 g3 a) t 1 := by
    unfold genY; ring
  have hc : d2 (genX g1 g2 g3 a t 0) (genY g1 g2 g3 a t 0)
      (genX g1 g2 g3 a t 1) (genY g1 g2 g3 a t 1)
      = d2 (lagX a (genOmega g1 g2 g3 a) t 0) (lagY a (genOmega g1 g2 g3 a) t 0)
        (lagX a (genOmega g1 g2 g3 a) t 1) (lagY a (genOmega g1 g2 g3 a) t 1) := by
    unfold d2; rw [hxx, hyy]
  rw [hc]
  exact d2_lag01 a (genOmega g1 g2 g3 a) t

/-- Pair 1,3. -/
theorem s9_gen_dist02 (g1 g2 g3 a t : ℝ) :
    d2 (genX g1 g2 g3 a t 0) (genY g1 g2 g3 a t 0)
      (genX g1 g2 g3 a t 2) (genY g1 g2 g3 a t 2) = a ^ 2 := by
  have hxx : genX g1 g2 g3 a t 0 - genX g1 g2 g3 a t 2
      = lagX a (genOmega g1 g2 g3 a) t 0 - lagX a (genOmega g1 g2 g3 a) t 2 := by
    unfold genX; ring
  have hyy : genY g1 g2 g3 a t 0 - genY g1 g2 g3 a t 2
      = lagY a (genOmega g1 g2 g3 a) t 0 - lagY a (genOmega g1 g2 g3 a) t 2 := by
    unfold genY; ring
  have hc : d2 (genX g1 g2 g3 a t 0) (genY g1 g2 g3 a t 0)
      (genX g1 g2 g3 a t 2) (genY g1 g2 g3 a t 2)
      = d2 (lagX a (genOmega g1 g2 g3 a) t 0) (lagY a (genOmega g1 g2 g3 a) t 0)
        (lagX a (genOmega g1 g2 g3 a) t 2) (lagY a (genOmega g1 g2 g3 a) t 2) := by
    unfold d2; rw [hxx, hyy]
  rw [hc]
  exact d2_lag02 a (genOmega g1 g2 g3 a) t

/-- Pair 2,3. -/
theorem s9_gen_dist12 (g1 g2 g3 a t : ℝ) :
    d2 (genX g1 g2 g3 a t 1) (genY g1 g2 g3 a t 1)
      (genX g1 g2 g3 a t 2) (genY g1 g2 g3 a t 2) = a ^ 2 := by
  have hxx : genX g1 g2 g3 a t 1 - genX g1 g2 g3 a t 2
      = lagX a (genOmega g1 g2 g3 a) t 1 - lagX a (genOmega g1 g2 g3 a) t 2 := by
    unfold genX; ring
  have hyy : genY g1 g2 g3 a t 1 - genY g1 g2 g3 a t 2
      = lagY a (genOmega g1 g2 g3 a) t 1 - lagY a (genOmega g1 g2 g3 a) t 2 := by
    unfold genY; ring
  have hc : d2 (genX g1 g2 g3 a t 1) (genY g1 g2 g3 a t 1)
      (genX g1 g2 g3 a t 2) (genY g1 g2 g3 a t 2)
      = d2 (lagX a (genOmega g1 g2 g3 a) t 1) (lagY a (genOmega g1 g2 g3 a) t 1)
        (lagX a (genOmega g1 g2 g3 a) t 2) (lagY a (genOmega g1 g2 g3 a) t 2) := by
    unfold d2; rw [hxx, hyy]
  rw [hc]
  exact d2_lag12 a (genOmega g1 g2 g3 a) t

/-- **The circulation-weighted centroid stays at the origin (x).**
    Σ Γ_k x_k(t) = 0 along the whole continued trajectory — the identity
    that makes the rigid rotation an exact solution. -/
theorem s9_gen_centroid_x (g1 g2 g3 a t : ℝ) (hG : g1 + g2 + g3 ≠ 0) :
    g1 * genX g1 g2 g3 a t 0 + g2 * genX g1 g2 g3 a t 1
      + g3 * genX g1 g2 g3 a t 2 = 0 := by
  have hr0 : lagX a (genOmega g1 g2 g3 a) t 0
      = Real.cos (genOmega g1 g2 g3 a * t) * lagX a (genOmega g1 g2 g3 a) 0 0
        - Real.sin (genOmega g1 g2 g3 a * t) * lagY a (genOmega g1 g2 g3 a) 0 0 := by
    have h := lag_rotation_x a (genOmega g1 g2 g3 a) t 0 0
    rw [zero_add] at h; exact h
  have hr1 : lagX a (genOmega g1 g2 g3 a) t 1
      = Real.cos (genOmega g1 g2 g3 a * t) * lagX a (genOmega g1 g2 g3 a) 0 1
        - Real.sin (genOmega g1 g2 g3 a * t) * lagY a (genOmega g1 g2 g3 a) 0 1 := by
    have h := lag_rotation_x a (genOmega g1 g2 g3 a) t 0 1
    rw [zero_add] at h; exact h
  have hr2 : lagX a (genOmega g1 g2 g3 a) t 2
      = Real.cos (genOmega g1 g2 g3 a * t) * lagX a (genOmega g1 g2 g3 a) 0 2
        - Real.sin (genOmega g1 g2 g3 a * t) * lagY a (genOmega g1 g2 g3 a) 0 2 := by
    have h := lag_rotation_x a (genOmega g1 g2 g3 a) t 0 2
    rw [zero_add] at h; exact h
  have hA : g1 * lagX a (genOmega g1 g2 g3 a) t 0
      + g2 * lagX a (genOmega g1 g2 g3 a) t 1
      + g3 * lagX a (genOmega g1 g2 g3 a) t 2
      = Real.cos (genOmega g1 g2 g3 a * t)
        * (g1 * lagX a (genOmega g1 g2 g3 a) 0 0
          + g2 * lagX a (genOmega g1 g2 g3 a) 0 1
          + g3 * lagX a (genOmega g1 g2 g3 a) 0 2)
        - Real.sin (genOmega g1 g2 g3 a * t)
        * (g1 * lagY a (genOmega g1 g2 g3 a) 0 0
          + g2 * lagY a (genOmega g1 g2 g3 a) 0 1
          + g3 * lagY a (genOmega g1 g2 g3 a) 0 2) := by
    linear_combination g1 * hr0 + g2 * hr1 + g3 * hr2
  have hX0 : g1 * lagX a (genOmega g1 g2 g3 a) 0 0
      + g2 * lagX a (genOmega g1 g2 g3 a) 0 1
      + g3 * lagX a (genOmega g1 g2 g3 a) 0 2
      = a * (g1 * eqX1 + g2 * eqX2 + g3 * eqX3) := by
    rw [lagX_zero a (genOmega g1 g2 g3 a) 0, lagX_zero a (genOmega g1 g2 g3 a) 1,
      lagX_zero a (genOmega g1 g2 g3 a) 2, lagX0_eq1, lagX0_eq2, lagX0_eq3]
    ring
  have hY0 : g1 * lagY a (genOmega g1 g2 g3 a) 0 0
      + g2 * lagY a (genOmega g1 g2 g3 a) 0 1
      + g3 * lagY a (genOmega g1 g2 g3 a) 0 2
      = a * (g1 * eqY1 + g2 * eqY2 + g3 * eqY3) := by
    rw [lagY_zero a (genOmega g1 g2 g3 a) 0, lagY_zero a (genOmega g1 g2 g3 a) 1,
      lagY_zero a (genOmega g1 g2 g3 a) 2, lagY0_eq1, lagY0_eq2, lagY0_eq3]
    ring
  have htx : a * (g1 * eqX1 + g2 * eqX2 + g3 * eqX3)
      + (g1 + g2 + g3) * tauX g1 g2 g3 a = 0 := by
    unfold tauX
    rw [show (g1 + g2 + g3) * (-a * (g1 * eqX1 + g2 * eqX2 + g3 * eqX3)
        / (g1 + g2 + g3))
      = -(a * (g1 * eqX1 + g2 * eqX2 + g3 * eqX3))
        * ((g1 + g2 + g3) / (g1 + g2 + g3)) from by ring,
      div_self hG, mul_one]
    ring
  have hty : a * (g1 * eqY1 + g2 * eqY2 + g3 * eqY3)
      + (g1 + g2 + g3) * tauY g1 g2 g3 a = 0 := by
    unfold tauY
    rw [show (g1 + g2 + g3) * (-a * (g1 * eqY1 + g2 * eqY2 + g3 * eqY3)
        / (g1 + g2 + g3))
      = -(a * (g1 * eqY1 + g2 * eqY2 + g3 * eqY3))
        * ((g1 + g2 + g3) / (g1 + g2 + g3)) from by ring,
      div_self hG, mul_one]
    ring
  unfold genX
  linear_combination hA + Real.cos (genOmega g1 g2 g3 a * t) * hX0
    - Real.sin (genOmega g1 g2 g3 a * t) * hY0
    + Real.cos (genOmega g1 g2 g3 a * t) * htx
    - Real.sin (genOmega g1 g2 g3 a * t) * hty

/-- The circulation-weighted centroid stays at the origin (y). -/
theorem s9_gen_centroid_y (g1 g2 g3 a t : ℝ) (hG : g1 + g2 + g3 ≠ 0) :
    g1 * genY g1 g2 g3 a t 0 + g2 * genY g1 g2 g3 a t 1
      + g3 * genY g1 g2 g3 a t 2 = 0 := by
  have hs0 : lagY a (genOmega g1 g2 g3 a) t 0
      = Real.sin (genOmega g1 g2 g3 a * t) * lagX a (genOmega g1 g2 g3 a) 0 0
        + Real.cos (genOmega g1 g2 g3 a * t) * lagY a (genOmega g1 g2 g3 a) 0 0 := by
    have h := lag_rotation_y a (genOmega g1 g2 g3 a) t 0 0
    rw [zero_add] at h; exact h
  have hs1 : lagY a (genOmega g1 g2 g3 a) t 1
      = Real.sin (genOmega g1 g2 g3 a * t) * lagX a (genOmega g1 g2 g3 a) 0 1
        + Real.cos (genOmega g1 g2 g3 a * t) * lagY a (genOmega g1 g2 g3 a) 0 1 := by
    have h := lag_rotation_y a (genOmega g1 g2 g3 a) t 0 1
    rw [zero_add] at h; exact h
  have hs2 : lagY a (genOmega g1 g2 g3 a) t 2
      = Real.sin (genOmega g1 g2 g3 a * t) * lagX a (genOmega g1 g2 g3 a) 0 2
        + Real.cos (genOmega g1 g2 g3 a * t) * lagY a (genOmega g1 g2 g3 a) 0 2 := by
    have h := lag_rotation_y a (genOmega g1 g2 g3 a) t 0 2
    rw [zero_add] at h; exact h
  have hB : g1 * lagY a (genOmega g1 g2 g3 a) t 0
      + g2 * lagY a (genOmega g1 g2 g3 a) t 1
      + g3 * lagY a (genOmega g1 g2 g3 a) t 2
      = Real.sin (genOmega g1 g2 g3 a * t)
        * (g1 * lagX a (genOmega g1 g2 g3 a) 0 0
          + g2 * lagX a (genOmega g1 g2 g3 a) 0 1
          + g3 * lagX a (genOmega g1 g2 g3 a) 0 2)
        + Real.cos (genOmega g1 g2 g3 a * t)
        * (g1 * lagY a (genOmega g1 g2 g3 a) 0 0
          + g2 * lagY a (genOmega g1 g2 g3 a) 0 1
          + g3 * lagY a (genOmega g1 g2 g3 a) 0 2) := by
    linear_combination g1 * hs0 + g2 * hs1 + g3 * hs2
  have hX0 : g1 * lagX a (genOmega g1 g2 g3 a) 0 0
      + g2 * lagX a (genOmega g1 g2 g3 a) 0 1
      + g3 * lagX a (genOmega g1 g2 g3 a) 0 2
      = a * (g1 * eqX1 + g2 * eqX2 + g3 * eqX3) := by
    rw [lagX_zero a (genOmega g1 g2 g3 a) 0, lagX_zero a (genOmega g1 g2 g3 a) 1,
      lagX_zero a (genOmega g1 g2 g3 a) 2, lagX0_eq1, lagX0_eq2, lagX0_eq3]
    ring
  have hY0 : g1 * lagY a (genOmega g1 g2 g3 a) 0 0
      + g2 * lagY a (genOmega g1 g2 g3 a) 0 1
      + g3 * lagY a (genOmega g1 g2 g3 a) 0 2
      = a * (g1 * eqY1 + g2 * eqY2 + g3 * eqY3) := by
    rw [lagY_zero a (genOmega g1 g2 g3 a) 0, lagY_zero a (genOmega g1 g2 g3 a) 1,
      lagY_zero a (genOmega g1 g2 g3 a) 2, lagY0_eq1, lagY0_eq2, lagY0_eq3]
    ring
  have htx : a * (g1 * eqX1 + g2 * eqX2 + g3 * eqX3)
      + (g1 + g2 + g3) * tauX g1 g2 g3 a = 0 := by
    unfold tauX
    rw [show (g1 + g2 + g3) * (-a * (g1 * eqX1 + g2 * eqX2 + g3 * eqX3)
        / (g1 + g2 + g3))
      = -(a * (g1 * eqX1 + g2 * eqX2 + g3 * eqX3))
        * ((g1 + g2 + g3) / (g1 + g2 + g3)) from by ring,
      div_self hG, mul_one]
    ring
  have hty : a * (g1 * eqY1 + g2 * eqY2 + g3 * eqY3)
      + (g1 + g2 + g3) * tauY g1 g2 g3 a = 0 := by
    unfold tauY
    rw [show (g1 + g2 + g3) * (-a * (g1 * eqY1 + g2 * eqY2 + g3 * eqY3)
        / (g1 + g2 + g3))
      = -(a * (g1 * eqY1 + g2 * eqY2 + g3 * eqY3))
        * ((g1 + g2 + g3) / (g1 + g2 + g3)) from by ring,
      div_self hG, mul_one]
    ring
  unfold genY
  linear_combination hB + Real.sin (genOmega g1 g2 g3 a * t) * hX0
    + Real.cos (genOmega g1 g2 g3 a * t) * hY0
    + Real.sin (genOmega g1 g2 g3 a * t) * htx
    + Real.cos (genOmega g1 g2 g3 a * t) * hty

/-- **The Kirchhoff field along the continued triangle (vortex 1, x).**
    The weighted-centroid identity collapses the partner sums:
    V_x(w_1) = −ω·y_1 exactly, for arbitrary circulations. -/
theorem s9_gen_field_x1 (g1 g2 g3 a t : ℝ) (hG : g1 + g2 + g3 ≠ 0) :
    kx1 g1 g2 g3 (genX g1 g2 g3 a t 0) (genY g1 g2 g3 a t 0)
      (genX g1 g2 g3 a t 1) (genY g1 g2 g3 a t 1)
      (genX g1 g2 g3 a t 2) (genY g1 g2 g3 a t 2)
      = -(genOmega g1 g2 g3 a) * genY g1 g2 g3 a t 0 := by
  have hd1 := s9_gen_dist01 g1 g2 g3 a t
  have hd2 := s9_gen_dist02 g1 g2 g3 a t
  have hc := s9_gen_centroid_y g1 g2 g3 a t hG
  have hsum : g2 * (genY g1 g2 g3 a t 0 - genY g1 g2 g3 a t 1)
      + g3 * (genY g1 g2 g3 a t 0 - genY g1 g2 g3 a t 2)
      = (g1 + g2 + g3) * genY g1 g2 g3 a t 0 := by
    have hr : g2 * (genY g1 g2 g3 a t 0 - genY g1 g2 g3 a t 1)
        + g3 * (genY g1 g2 g3 a t 0 - genY g1 g2 g3 a t 2)
        = (g1 + g2 + g3) * genY g1 g2 g3 a t 0
          - (g1 * genY g1 g2 g3 a t 0 + g2 * genY g1 g2 g3 a t 1
            + g3 * genY g1 g2 g3 a t 2) := by
      ring
    rw [hr, hc]; ring
  have hω : genOmega g1 g2 g3 a = (g1 + g2 + g3) / (2 * Real.pi * a ^ 2) := rfl
  unfold kx1
  rw [hd1, hd2]
  linear_combination (-(1 / (2 * Real.pi * a ^ 2))) * hsum
    + genY g1 g2 g3 a t 0 * hω

/-- Vortex 1, y-component. -/
theorem s9_gen_field_y1 (g1 g2 g3 a t : ℝ) (hG : g1 + g2 + g3 ≠ 0) :
    ky1 g1 g2 g3 (genX g1 g2 g3 a t 0) (genY g1 g2 g3 a t 0)
      (genX g1 g2 g3 a t 1) (genY g1 g2 g3 a t 1)
      (genX g1 g2 g3 a t 2) (genY g1 g2 g3 a t 2)
      = genOmega g1 g2 g3 a * genX g1 g2 g3 a t 0 := by
  have hd1 := s9_gen_dist01 g1 g2 g3 a t
  have hd2 := s9_gen_dist02 g1 g2 g3 a t
  have hc := s9_gen_centroid_x g1 g2 g3 a t hG
  have hsum : g2 * (genX g1 g2 g3 a t 0 - genX g1 g2 g3 a t 1)
      + g3 * (genX g1 g2 g3 a t 0 - genX g1 g2 g3 a t 2)
      = (g1 + g2 + g3) * genX g1 g2 g3 a t 0 := by
    have hr : g2 * (genX g1 g2 g3 a t 0 - genX g1 g2 g3 a t 1)
        + g3 * (genX g1 g2 g3 a t 0 - genX g1 g2 g3 a t 2)
        = (g1 + g2 + g3) * genX g1 g2 g3 a t 0
          - (g1 * genX g1 g2 g3 a t 0 + g2 * genX g1 g2 g3 a t 1
            + g3 * genX g1 g2 g3 a t 2) := by
      ring
    rw [hr, hc]; ring
  have hω : genOmega g1 g2 g3 a = (g1 + g2 + g3) / (2 * Real.pi * a ^ 2) := rfl
  unfold ky1
  rw [hd1, hd2]
  linear_combination (1 / (2 * Real.pi * a ^ 2)) * hsum
    - genX g1 g2 g3 a t 0 * hω

/-- Vortex 2, x-component. -/
theorem s9_gen_field_x2 (g1 g2 g3 a t : ℝ) (hG : g1 + g2 + g3 ≠ 0) :
    kx2 g1 g2 g3 (genX g1 g2 g3 a t 0) (genY g1 g2 g3 a t 0)
      (genX g1 g2 g3 a t 1) (genY g1 g2 g3 a t 1)
      (genX g1 g2 g3 a t 2) (genY g1 g2 g3 a t 2)
      = -(genOmega g1 g2 g3 a) * genY g1 g2 g3 a t 1 := by
  have hd1 := s9_gen_dist01 g1 g2 g3 a t
  have hd2 := s9_gen_dist12 g1 g2 g3 a t
  have hc := s9_gen_centroid_y g1 g2 g3 a t hG
  have hsum : g1 * (genY g1 g2 g3 a t 1 - genY g1 g2 g3 a t 0)
      + g3 * (genY g1 g2 g3 a t 1 - genY g1 g2 g3 a t 2)
      = (g1 + g2 + g3) * genY g1 g2 g3 a t 1 := by
    have hr : g1 * (genY g1 g2 g3 a t 1 - genY g1 g2 g3 a t 0)
        + g3 * (genY g1 g2 g3 a t 1 - genY g1 g2 g3 a t 2)
        = (g1 + g2 + g3) * genY g1 g2 g3 a t 1
          - (g1 * genY g1 g2 g3 a t 0 + g2 * genY g1 g2 g3 a t 1
            + g3 * genY g1 g2 g3 a t 2) := by
      ring
    rw [hr, hc]; ring
  have hω : genOmega g1 g2 g3 a = (g1 + g2 + g3) / (2 * Real.pi * a ^ 2) := rfl
  unfold kx2
  rw [hd1, hd2]
  linear_combination (-(1 / (2 * Real.pi * a ^ 2))) * hsum
    + genY g1 g2 g3 a t 1 * hω

/-- Vortex 2, y-component. -/
theorem s9_gen_field_y2 (g1 g2 g3 a t : ℝ) (hG : g1 + g2 + g3 ≠ 0) :
    ky2 g1 g2 g3 (genX g1 g2 g3 a t 0) (genY g1 g2 g3 a t 0)
      (genX g1 g2 g3 a t 1) (genY g1 g2 g3 a t 1)
      (genX g1 g2 g3 a t 2) (genY g1 g2 g3 a t 2)
      = genOmega g1 g2 g3 a * genX g1 g2 g3 a t 1 := by
  have hd1 := s9_gen_dist01 g1 g2 g3 a t
  have hd2 := s9_gen_dist12 g1 g2 g3 a t
  have hc := s9_gen_centroid_x g1 g2 g3 a t hG
  have hsum : g1 * (genX g1 g2 g3 a t 1 - genX g1 g2 g3 a t 0)
      + g3 * (genX g1 g2 g3 a t 1 - genX g1 g2 g3 a t 2)
      = (g1 + g2 + g3) * genX g1 g2 g3 a t 1 := by
    have hr : g1 * (genX g1 g2 g3 a t 1 - genX g1 g2 g3 a t 0)
        + g3 * (genX g1 g2 g3 a t 1 - genX g1 g2 g3 a t 2)
        = (g1 + g2 + g3) * genX g1 g2 g3 a t 1
          - (g1 * genX g1 g2 g3 a t 0 + g2 * genX g1 g2 g3 a t 1
            + g3 * genX g1 g2 g3 a t 2) := by
      ring
    rw [hr, hc]; ring
  have hω : genOmega g1 g2 g3 a = (g1 + g2 + g3) / (2 * Real.pi * a ^ 2) := rfl
  unfold ky2
  rw [hd1, hd2]
  linear_combination (1 / (2 * Real.pi * a ^ 2)) * hsum
    - genX g1 g2 g3 a t 1 * hω

/-- Vortex 3, x-component. -/
theorem s9_gen_field_x3 (g1 g2 g3 a t : ℝ) (hG : g1 + g2 + g3 ≠ 0) :
    kx3 g1 g2 g3 (genX g1 g2 g3 a t 0) (genY g1 g2 g3 a t 0)
      (genX g1 g2 g3 a t 1) (genY g1 g2 g3 a t 1)
      (genX g1 g2 g3 a t 2) (genY g1 g2 g3 a t 2)
      = -(genOmega g1 g2 g3 a) * genY g1 g2 g3 a t 2 := by
  have hd1 := s9_gen_dist02 g1 g2 g3 a t
  have hd2 := s9_gen_dist12 g1 g2 g3 a t
  have hc := s9_gen_centroid_y g1 g2 g3 a t hG
  have hsum : g1 * (genY g1 g2 g3 a t 2 - genY g1 g2 g3 a t 0)
      + g2 * (genY g1 g2 g3 a t 2 - genY g1 g2 g3 a t 1)
      = (g1 + g2 + g3) * genY g1 g2 g3 a t 2 := by
    have hr : g1 * (genY g1 g2 g3 a t 2 - genY g1 g2 g3 a t 0)
        + g2 * (genY g1 g2 g3 a t 2 - genY g1 g2 g3 a t 1)
        = (g1 + g2 + g3) * genY g1 g2 g3 a t 2
          - (g1 * genY g1 g2 g3 a t 0 + g2 * genY g1 g2 g3 a t 1
            + g3 * genY g1 g2 g3 a t 2) := by
      ring
    rw [hr, hc]; ring
  have hω : genOmega g1 g2 g3 a = (g1 + g2 + g3) / (2 * Real.pi * a ^ 2) := rfl
  unfold kx3
  rw [hd1, hd2]
  linear_combination (-(1 / (2 * Real.pi * a ^ 2))) * hsum
    + genY g1 g2 g3 a t 2 * hω

/-- Vortex 3, y-component. -/
theorem s9_gen_field_y3 (g1 g2 g3 a t : ℝ) (hG : g1 + g2 + g3 ≠ 0) :
    ky3 g1 g2 g3 (genX g1 g2 g3 a t 0) (genY g1 g2 g3 a t 0)
      (genX g1 g2 g3 a t 1) (genY g1 g2 g3 a t 1)
      (genX g1 g2 g3 a t 2) (genY g1 g2 g3 a t 2)
      = genOmega g1 g2 g3 a * genX g1 g2 g3 a t 2 := by
  have hd1 := s9_gen_dist02 g1 g2 g3 a t
  have hd2 := s9_gen_dist12 g1 g2 g3 a t
  have hc := s9_gen_centroid_x g1 g2 g3 a t hG
  have hsum : g1 * (genX g1 g2 g3 a t 2 - genX g1 g2 g3 a t 0)
      + g2 * (genX g1 g2 g3 a t 2 - genX g1 g2 g3 a t 1)
      = (g1 + g2 + g3) * genX g1 g2 g3 a t 2 := by
    have hr : g1 * (genX g1 g2 g3 a t 2 - genX g1 g2 g3 a t 0)
        + g2 * (genX g1 g2 g3 a t 2 - genX g1 g2 g3 a t 1)
        = (g1 + g2 + g3) * genX g1 g2 g3 a t 2
          - (g1 * genX g1 g2 g3 a t 0 + g2 * genX g1 g2 g3 a t 1
            + g3 * genX g1 g2 g3 a t 2) := by
      ring
    rw [hr, hc]; ring
  have hω : genOmega g1 g2 g3 a = (g1 + g2 + g3) / (2 * Real.pi * a ^ 2) := rfl
  unfold ky3
  rw [hd1, hd2]
  linear_combination (1 / (2 * Real.pi * a ^ 2)) * hsum
    - genX g1 g2 g3 a t 2 * hω

/-- **THE NONLINEAR CONTINUATION THEOREM (§9.1).**  For ARBITRARY
    circulations g1, g2, g3 with nonzero total G = g1+g2+g3 and any side
    a ≠ 0, the equilateral triangle translated so that its
    circulation-weighted centroid sits at the origin and rotating rigidly
    at ω = G/(2πa²) is an EXACT Kirchhoff solution.  The §7 Lagrange
    family (g1 = g2 = g3 = Γ) therefore extends to a full
    three-parameter branch through circulation space — the nonlinear
    continuation of the relative equilibrium. -/
theorem s9_rel_eq (g1 g2 g3 a : ℝ) (ha : a ≠ 0) (hG : g1 + g2 + g3 ≠ 0) :
    KirchhoffSol g1 g2 g3 where
  x1 := fun t => genX g1 g2 g3 a t 0
  y1 := fun t => genY g1 g2 g3 a t 0
  x2 := fun t => genX g1 g2 g3 a t 1
  y2 := fun t => genY g1 g2 g3 a t 1
  x3 := fun t => genX g1 g2 g3 a t 2
  y3 := fun t => genY g1 g2 g3 a t 2
  hx1 := fun t => by
    show HasDerivAt (fun t => genX g1 g2 g3 a t 0)
      (kx1 g1 g2 g3 (genX g1 g2 g3 a t 0) (genY g1 g2 g3 a t 0)
        (genX g1 g2 g3 a t 1) (genY g1 g2 g3 a t 1)
        (genX g1 g2 g3 a t 2) (genY g1 g2 g3 a t 2)) t
    exact (deriv_congr (s9_gen_deriv_x g1 g2 g3 a t 0)
      (fun s => rfl)).congr_deriv (s9_gen_field_x1 g1 g2 g3 a t hG).symm
  hy1 := fun t => by
    show HasDerivAt (fun t => genY g1 g2 g3 a t 0)
      (ky1 g1 g2 g3 (genX g1 g2 g3 a t 0) (genY g1 g2 g3 a t 0)
        (genX g1 g2 g3 a t 1) (genY g1 g2 g3 a t 1)
        (genX g1 g2 g3 a t 2) (genY g1 g2 g3 a t 2)) t
    exact (deriv_congr (s9_gen_deriv_y g1 g2 g3 a t 0)
      (fun s => rfl)).congr_deriv (s9_gen_field_y1 g1 g2 g3 a t hG).symm
  hx2 := fun t => by
    show HasDerivAt (fun t => genX g1 g2 g3 a t 1)
      (kx2 g1 g2 g3 (genX g1 g2 g3 a t 0) (genY g1 g2 g3 a t 0)
        (genX g1 g2 g3 a t 1) (genY g1 g2 g3 a t 1)
        (genX g1 g2 g3 a t 2) (genY g1 g2 g3 a t 2)) t
    exact (deriv_congr (s9_gen_deriv_x g1 g2 g3 a t 1)
      (fun s => rfl)).congr_deriv (s9_gen_field_x2 g1 g2 g3 a t hG).symm
  hy2 := fun t => by
    show HasDerivAt (fun t => genY g1 g2 g3 a t 1)
      (ky2 g1 g2 g3 (genX g1 g2 g3 a t 0) (genY g1 g2 g3 a t 0)
        (genX g1 g2 g3 a t 1) (genY g1 g2 g3 a t 1)
        (genX g1 g2 g3 a t 2) (genY g1 g2 g3 a t 2)) t
    exact (deriv_congr (s9_gen_deriv_y g1 g2 g3 a t 1)
      (fun s => rfl)).congr_deriv (s9_gen_field_y2 g1 g2 g3 a t hG).symm
  hx3 := fun t => by
    show HasDerivAt (fun t => genX g1 g2 g3 a t 2)
      (kx3 g1 g2 g3 (genX g1 g2 g3 a t 0) (genY g1 g2 g3 a t 0)
        (genX g1 g2 g3 a t 1) (genY g1 g2 g3 a t 1)
        (genX g1 g2 g3 a t 2) (genY g1 g2 g3 a t 2)) t
    exact (deriv_congr (s9_gen_deriv_x g1 g2 g3 a t 2)
      (fun s => rfl)).congr_deriv (s9_gen_field_x3 g1 g2 g3 a t hG).symm
  hy3 := fun t => by
    show HasDerivAt (fun t => genY g1 g2 g3 a t 2)
      (ky3 g1 g2 g3 (genX g1 g2 g3 a t 0) (genY g1 g2 g3 a t 0)
        (genX g1 g2 g3 a t 1) (genY g1 g2 g3 a t 1)
        (genX g1 g2 g3 a t 2) (genY g1 g2 g3 a t 2)) t
    exact (deriv_congr (s9_gen_deriv_y g1 g2 g3 a t 2)
      (fun s => rfl)).congr_deriv (s9_gen_field_y3 g1 g2 g3 a t hG).symm
  hd12 := fun t => by
    show d2 (genX g1 g2 g3 a t 0) (genY g1 g2 g3 a t 0)
      (genX g1 g2 g3 a t 1) (genY g1 g2 g3 a t 1) ≠ 0
    rw [s9_gen_dist01 g1 g2 g3 a t]
    exact pow_ne_zero 2 ha
  hd13 := fun t => by
    show d2 (genX g1 g2 g3 a t 0) (genY g1 g2 g3 a t 0)
      (genX g1 g2 g3 a t 2) (genY g1 g2 g3 a t 2) ≠ 0
    rw [s9_gen_dist02 g1 g2 g3 a t]
    exact pow_ne_zero 2 ha
  hd23 := fun t => by
    show d2 (genX g1 g2 g3 a t 1) (genY g1 g2 g3 a t 1)
      (genX g1 g2 g3 a t 2) (genY g1 g2 g3 a t 2) ≠ 0
    rw [s9_gen_dist12 g1 g2 g3 a t]
    exact pow_ne_zero 2 ha

/-- **The rotation rate of the continued branch is regular in the side
    parameter**: ω(c·a) = ω(a)/c² — the §7 scaling law persists for
    arbitrary circulations; dω/da ≠ 0, so the branch continues through
    every scale with no bifurcation of the rotation rate. -/
theorem s9_omega_scale (g1 g2 g3 a c : ℝ) (hc : c ≠ 0) :
    genOmega g1 g2 g3 (c * a) = genOmega g1 g2 g3 a / c ^ 2 := by
  unfold genOmega
  rw [show (c * a) ^ 2 = c ^ 2 * a ^ 2 from by ring]
  ring

/-! ### 9.2 Exact nonlinear continuation of the modes

§8 proved that the ±iω translation pair, the phase mode and the size
drift are eigenmodes of the LINEARIZED rotating-frame flow.  §9.2 shows
that the corresponding mode families persist EXACTLY in the full
nonlinear system, for arbitrary circulations:

  • translations: the Kirchhoff field is translation-invariant, so
    shifting a solution by any constant vector δ = (b1, b2) yields
    another exact solution — the 2-parameter translation orbit.  In the
    co-rotating frame the deviation R(−ωt)·δ has the CONSTANT norm
    |δ|: the nonlinear realization of the ±iω eigenpair.
  • phase: re-timing a solution (t ↦ t + s) yields another exact
    solution — the rotation orbit, the nonlinear realization of the
    zero eigenvalue (phase mode). -/

/-- Translation invariance of the Kirchhoff field (vortex 1, x). -/
theorem s9_kx_shift (g1 g2 g3 b1 b2 x1 y1 x2 y2 x3 y3 : ℝ) :
    kx1 g1 g2 g3 (x1 + b1) (y1 + b2) (x2 + b1) (y2 + b2) (x3 + b1) (y3 + b2)
      = kx1 g1 g2 g3 x1 y1 x2 y2 x3 y3 := by
  unfold kx1
  rw [show d2 (x1 + b1) (y1 + b2) (x2 + b1) (y2 + b2)
      = d2 x1 y1 x2 y2 from by unfold d2; ring,
    show d2 (x1 + b1) (y1 + b2) (x3 + b1) (y3 + b2)
      = d2 x1 y1 x3 y3 from by unfold d2; ring]
  ring

/-- Translation invariance (vortex 1, y). -/
theorem s9_ky_shift (g1 g2 g3 b1 b2 x1 y1 x2 y2 x3 y3 : ℝ) :
    ky1 g1 g2 g3 (x1 + b1) (y1 + b2) (x2 + b1) (y2 + b2) (x3 + b1) (y3 + b2)
      = ky1 g1 g2 g3 x1 y1 x2 y2 x3 y3 := by
  unfold ky1
  rw [show d2 (x1 + b1) (y1 + b2) (x2 + b1) (y2 + b2)
      = d2 x1 y1 x2 y2 from by unfold d2; ring,
    show d2 (x1 + b1) (y1 + b2) (x3 + b1) (y3 + b2)
      = d2 x1 y1 x3 y3 from by unfold d2; ring]
  ring

/-- Translation invariance (vortex 2, x). -/
theorem s9_kx2_shift (g1 g2 g3 b1 b2 x1 y1 x2 y2 x3 y3 : ℝ) :
    kx2 g1 g2 g3 (x1 + b1) (y1 + b2) (x2 + b1) (y2 + b2) (x3 + b1) (y3 + b2)
      = kx2 g1 g2 g3 x1 y1 x2 y2 x3 y3 := by
  unfold kx2
  rw [show d2 (x1 + b1) (y1 + b2) (x2 + b1) (y2 + b2)
      = d2 x1 y1 x2 y2 from by unfold d2; ring,
    show d2 (x2 + b1) (y2 + b2) (x3 + b1) (y3 + b2)
      = d2 x2 y2 x3 y3 from by unfold d2; ring]
  ring

/-- Translation invariance (vortex 2, y). -/
theorem s9_ky2_shift (g1 g2 g3 b1 b2 x1 y1 x2 y2 x3 y3 : ℝ) :
    ky2 g1 g2 g3 (x1 + b1) (y1 + b2) (x2 + b1) (y2 + b2) (x3 + b1) (y3 + b2)
      = ky2 g1 g2 g3 x1 y1 x2 y2 x3 y3 := by
  unfold ky2
  rw [show d2 (x1 + b1) (y1 + b2) (x2 + b1) (y2 + b2)
      = d2 x1 y1 x2 y2 from by unfold d2; ring,
    show d2 (x2 + b1) (y2 + b2) (x3 + b1) (y3 + b2)
      = d2 x2 y2 x3 y3 from by unfold d2; ring]
  ring

/-- Translation invariance (vortex 3, x). -/
theorem s9_kx3_shift (g1 g2 g3 b1 b2 x1 y1 x2 y2 x3 y3 : ℝ) :
    kx3 g1 g2 g3 (x1 + b1) (y1 + b2) (x2 + b1) (y2 + b2) (x3 + b1) (y3 + b2)
      = kx3 g1 g2 g3 x1 y1 x2 y2 x3 y3 := by
  unfold kx3
  rw [show d2 (x1 + b1) (y1 + b2) (x3 + b1) (y3 + b2)
      = d2 x1 y1 x3 y3 from by unfold d2; ring,
    show d2 (x2 + b1) (y2 + b2) (x3 + b1) (y3 + b2)
      = d2 x2 y2 x3 y3 from by unfold d2; ring]
  ring

/-- Translation invariance (vortex 3, y). -/
theorem s9_ky3_shift (g1 g2 g3 b1 b2 x1 y1 x2 y2 x3 y3 : ℝ) :
    ky3 g1 g2 g3 (x1 + b1) (y1 + b2) (x2 + b1) (y2 + b2) (x3 + b1) (y3 + b2)
      = ky3 g1 g2 g3 x1 y1 x2 y2 x3 y3 := by
  unfold ky3
  rw [show d2 (x1 + b1) (y1 + b2) (x3 + b1) (y3 + b2)
      = d2 x1 y1 x3 y3 from by unfold d2; ring,
    show d2 (x2 + b1) (y2 + b2) (x3 + b1) (y3 + b2)
      = d2 x2 y2 x3 y3 from by unfold d2; ring]
  ring

/-- **The 2-parameter translation orbit (§9.2).**  Shifting ANY Kirchhoff
    solution by a constant vector δ = (b1, b2) produces another exact
    Kirchhoff solution — for arbitrary circulations the translation
    symmetry survives intact, and the deviation of the shifted solution
    from the base one is the constant vector δ itself. -/
theorem s9_sol_shift (g1 g2 g3 a b1 b2 : ℝ) (ha : a ≠ 0) (hG : g1 + g2 + g3 ≠ 0) :
    KirchhoffSol g1 g2 g3 := by
  have sol : KirchhoffSol g1 g2 g3 := s9_rel_eq g1 g2 g3 a ha hG
  exact {
    x1 := fun t => sol.x1 t + b1
    y1 := fun t => sol.y1 t + b2
    x2 := fun t => sol.x2 t + b1
    y2 := fun t => sol.y2 t + b2
    x3 := fun t => sol.x3 t + b1
    y3 := fun t => sol.y3 t + b2
    hx1 := fun t => by
      have h := (sol.hx1 t).add (hasDerivAt_const (c := b1) (x := t))
        |>.congr_deriv (by ring)
      show HasDerivAt (fun t => sol.x1 t + b1)
        (kx1 g1 g2 g3 (sol.x1 t + b1) (sol.y1 t + b2)
          (sol.x2 t + b1) (sol.y2 t + b2)
          (sol.x3 t + b1) (sol.y3 t + b2)) t
      exact h.congr_deriv (by rw [s9_kx_shift])
    hy1 := fun t => by
      have h := (sol.hy1 t).add (hasDerivAt_const (c := b2) (x := t))
        |>.congr_deriv (by ring)
      show HasDerivAt (fun t => sol.y1 t + b2)
        (ky1 g1 g2 g3 (sol.x1 t + b1) (sol.y1 t + b2)
          (sol.x2 t + b1) (sol.y2 t + b2)
          (sol.x3 t + b1) (sol.y3 t + b2)) t
      exact h.congr_deriv (by rw [s9_ky_shift])
    hx2 := fun t => by
      have h := (sol.hx2 t).add (hasDerivAt_const (c := b1) (x := t))
        |>.congr_deriv (by ring)
      show HasDerivAt (fun t => sol.x2 t + b1)
        (kx2 g1 g2 g3 (sol.x1 t + b1) (sol.y1 t + b2)
          (sol.x2 t + b1) (sol.y2 t + b2)
          (sol.x3 t + b1) (sol.y3 t + b2)) t
      exact h.congr_deriv (by rw [s9_kx2_shift])
    hy2 := fun t => by
      have h := (sol.hy2 t).add (hasDerivAt_const (c := b2) (x := t))
        |>.congr_deriv (by ring)
      show HasDerivAt (fun t => sol.y2 t + b2)
        (ky2 g1 g2 g3 (sol.x1 t + b1) (sol.y1 t + b2)
          (sol.x2 t + b1) (sol.y2 t + b2)
          (sol.x3 t + b1) (sol.y3 t + b2)) t
      exact h.congr_deriv (by rw [s9_ky2_shift])
    hx3 := fun t => by
      have h := (sol.hx3 t).add (hasDerivAt_const (c := b1) (x := t))
        |>.congr_deriv (by ring)
      show HasDerivAt (fun t => sol.x3 t + b1)
        (kx3 g1 g2 g3 (sol.x1 t + b1) (sol.y1 t + b2)
          (sol.x2 t + b1) (sol.y2 t + b2)
          (sol.x3 t + b1) (sol.y3 t + b2)) t
      exact h.congr_deriv (by rw [s9_kx3_shift])
    hy3 := fun t => by
      have h := (sol.hy3 t).add (hasDerivAt_const (c := b2) (x := t))
        |>.congr_deriv (by ring)
      show HasDerivAt (fun t => sol.y3 t + b2)
        (ky3 g1 g2 g3 (sol.x1 t + b1) (sol.y1 t + b2)
          (sol.x2 t + b1) (sol.y2 t + b2)
          (sol.x3 t + b1) (sol.y3 t + b2)) t
      exact h.congr_deriv (by rw [s9_ky3_shift])
    hd12 := fun t => by
      show d2 (sol.x1 t + b1) (sol.y1 t + b2) (sol.x2 t + b1) (sol.y2 t + b2) ≠ 0
      rw [show d2 (sol.x1 t + b1) (sol.y1 t + b2) (sol.x2 t + b1) (sol.y2 t + b2)
        = d2 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) from by unfold d2; ring]
      exact sol.hd12 t
    hd13 := fun t => by
      show d2 (sol.x1 t + b1) (sol.y1 t + b2) (sol.x3 t + b1) (sol.y3 t + b2) ≠ 0
      rw [show d2 (sol.x1 t + b1) (sol.y1 t + b2) (sol.x3 t + b1) (sol.y3 t + b2)
        = d2 (sol.x1 t) (sol.y1 t) (sol.x3 t) (sol.y3 t) from by unfold d2; ring]
      exact sol.hd13 t
    hd23 := fun t => by
      show d2 (sol.x2 t + b1) (sol.y2 t + b2) (sol.x3 t + b1) (sol.y3 t + b2) ≠ 0
      rw [show d2 (sol.x2 t + b1) (sol.y2 t + b2) (sol.x3 t + b1) (sol.y3 t + b2)
        = d2 (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t) from by unfold d2; ring]
      exact sol.hd23 t
  }

/-- **The phase orbit (§9.2).**  Re-timing ANY Kirchhoff solution by a
    constant shift (t ↦ t + s) produces another exact solution — the
    one-parameter rotation orbit of the relative equilibrium, the
    nonlinear realization of the zero eigenvalue (the phase mode). -/
theorem s9_sol_time (g1 g2 g3 a s : ℝ) (ha : a ≠ 0) (hG : g1 + g2 + g3 ≠ 0) :
    KirchhoffSol g1 g2 g3 := by
  have sol : KirchhoffSol g1 g2 g3 := s9_rel_eq g1 g2 g3 a ha hG
  exact {
    x1 := fun t => sol.x1 (t + s)
    y1 := fun t => sol.y1 (t + s)
    x2 := fun t => sol.x2 (t + s)
    y2 := fun t => sol.y2 (t + s)
    x3 := fun t => sol.x3 (t + s)
    y3 := fun t => sol.y3 (t + s)
    hx1 := fun t => by
      have hf : HasDerivAt (fun u : ℝ => u + s) 1 t :=
        ((hasDerivAt_id (𝕜 := ℝ) (x := t)).add
          (hasDerivAt_const (c := s) (x := t))).congr_deriv (by ring)
      have h := (sol.hx1 (t + s)).comp t hf
      show HasDerivAt (fun t => sol.x1 (t + s))
        (kx1 g1 g2 g3 (sol.x1 (t + s)) (sol.y1 (t + s))
          (sol.x2 (t + s)) (sol.y2 (t + s))
          (sol.x3 (t + s)) (sol.y3 (t + s))) t
      exact h.congr_deriv (by ring)
    hy1 := fun t => by
      have hf : HasDerivAt (fun u : ℝ => u + s) 1 t :=
        ((hasDerivAt_id (𝕜 := ℝ) (x := t)).add
          (hasDerivAt_const (c := s) (x := t))).congr_deriv (by ring)
      have h := (sol.hy1 (t + s)).comp t hf
      show HasDerivAt (fun t => sol.y1 (t + s))
        (ky1 g1 g2 g3 (sol.x1 (t + s)) (sol.y1 (t + s))
          (sol.x2 (t + s)) (sol.y2 (t + s))
          (sol.x3 (t + s)) (sol.y3 (t + s))) t
      exact h.congr_deriv (by ring)
    hx2 := fun t => by
      have hf : HasDerivAt (fun u : ℝ => u + s) 1 t :=
        ((hasDerivAt_id (𝕜 := ℝ) (x := t)).add
          (hasDerivAt_const (c := s) (x := t))).congr_deriv (by ring)
      have h := (sol.hx2 (t + s)).comp t hf
      show HasDerivAt (fun t => sol.x2 (t + s))
        (kx2 g1 g2 g3 (sol.x1 (t + s)) (sol.y1 (t + s))
          (sol.x2 (t + s)) (sol.y2 (t + s))
          (sol.x3 (t + s)) (sol.y3 (t + s))) t
      exact h.congr_deriv (by ring)
    hy2 := fun t => by
      have hf : HasDerivAt (fun u : ℝ => u + s) 1 t :=
        ((hasDerivAt_id (𝕜 := ℝ) (x := t)).add
          (hasDerivAt_const (c := s) (x := t))).congr_deriv (by ring)
      have h := (sol.hy2 (t + s)).comp t hf
      show HasDerivAt (fun t => sol.y2 (t + s))
        (ky2 g1 g2 g3 (sol.x1 (t + s)) (sol.y1 (t + s))
          (sol.x2 (t + s)) (sol.y2 (t + s))
          (sol.x3 (t + s)) (sol.y3 (t + s))) t
      exact h.congr_deriv (by ring)
    hx3 := fun t => by
      have hf : HasDerivAt (fun u : ℝ => u + s) 1 t :=
        ((hasDerivAt_id (𝕜 := ℝ) (x := t)).add
          (hasDerivAt_const (c := s) (x := t))).congr_deriv (by ring)
      have h := (sol.hx3 (t + s)).comp t hf
      show HasDerivAt (fun t => sol.x3 (t + s))
        (kx3 g1 g2 g3 (sol.x1 (t + s)) (sol.y1 (t + s))
          (sol.x2 (t + s)) (sol.y2 (t + s))
          (sol.x3 (t + s)) (sol.y3 (t + s))) t
      exact h.congr_deriv (by ring)
    hy3 := fun t => by
      have hf : HasDerivAt (fun u : ℝ => u + s) 1 t :=
        ((hasDerivAt_id (𝕜 := ℝ) (x := t)).add
          (hasDerivAt_const (c := s) (x := t))).congr_deriv (by ring)
      have h := (sol.hy3 (t + s)).comp t hf
      show HasDerivAt (fun t => sol.y3 (t + s))
        (ky3 g1 g2 g3 (sol.x1 (t + s)) (sol.y1 (t + s))
          (sol.x2 (t + s)) (sol.y2 (t + s))
          (sol.x3 (t + s)) (sol.y3 (t + s))) t
      exact h.congr_deriv (by ring)
    hd12 := fun t => by
      show d2 (sol.x1 (t + s)) (sol.y1 (t + s))
        (sol.x2 (t + s)) (sol.y2 (t + s)) ≠ 0
      exact sol.hd12 (t + s)
    hd13 := fun t => by
      show d2 (sol.x1 (t + s)) (sol.y1 (t + s))
        (sol.x3 (t + s)) (sol.y3 (t + s)) ≠ 0
      exact sol.hd13 (t + s)
    hd23 := fun t => by
      show d2 (sol.x2 (t + s)) (sol.y2 (t + s))
        (sol.x3 (t + s)) (sol.y3 (t + s)) ≠ 0
      exact sol.hd23 (t + s)
  }

/-- **The nonlinear ±iω translation mode (§9.2).**  In the frame
    co-rotating with ω = G/(2πa²), the deviation of the δ-shifted
    solution from the base trajectory is R(−ωt)·δ — a vector rotating at
    rate −ω — and its norm is EXACTLY |δ| for every t:
      (cos ωt·b1 + sin ωt·b2)² + (−sin ωt·b1 + cos ωt·b2)² = b1² + b2².
    The linear §8 prediction (translation modes preserve their norm
    exactly) is realized identically in the full nonlinear system, for
    arbitrary circulations. -/
theorem s9_trans_dev (g1 g2 g3 a b1 b2 t : ℝ) :
    (Real.cos (genOmega g1 g2 g3 a * t) * b1
        + Real.sin (genOmega g1 g2 g3 a * t) * b2) ^ 2
      + (-Real.sin (genOmega g1 g2 g3 a * t) * b1
        + Real.cos (genOmega g1 g2 g3 a * t) * b2) ^ 2
      = b1 ^ 2 + b2 ^ 2 := by
  linear_combination (b1 ^ 2 + b2 ^ 2)
    * Real.sin_sq_add_cos_sq (genOmega g1 g2 g3 a * t)

/-- Row 1 (rotX₁) of the 2π-scaled rotating-frame linearization at
    the equilateral anchor, for ARBITRARY circulations.  At
    g1 = g2 = g3 = g it equals g·linX1 (the §8 certified matrix). -/
noncomputable def genLinX1 (g1 g2 g3 dx1 dy1 dx2 dy2 dx3 dy3 : ℝ) : ℝ :=
g1 * dy1 - (1 / 2) * (Real.sqrt 3 * g2 * dx1) + (1 / 2) * (Real.sqrt 3 * g2 * dx2) + (1
    / 2) * (g2 * dy1) + (1 / 2) * (g2 * dy2) + (1 / 2) * (Real.sqrt 3 * g3 * dx1) - (1 /
    2) * (Real.sqrt 3 * g3 * dx3) + (1 / 2) * (g3 * dy1) + (1 / 2) * (g3 * dy3)

/-- Row 2 (rotY₁). -/
noncomputable def genLinY1 (g1 g2 g3 dx1 dy1 dx2 dy2 dx3 dy3 : ℝ) : ℝ :=
-g1 * dx1 + (1 / 2) * (Real.sqrt 3 * g2 * dy1) - (1 / 2) * (Real.sqrt 3 * g2 * dy2) - (3
    / 2) * (g2 * dx1) + (1 / 2) * (g2 * dx2) - (1 / 2) * (Real.sqrt 3 * g3 * dy1) + (1 /
    2) * (Real.sqrt 3 * g3 * dy3) - (3 / 2) * (g3 * dx1) + (1 / 2) * (g3 * dx3)

/-- Row 3 (rotX₂). -/
noncomputable def genLinX2 (g1 g2 g3 dx1 dy1 dx2 dy2 dx3 dy3 : ℝ) : ℝ :=
(1 / 2) * (Real.sqrt 3 * g1 * dx1) - (1 / 2) * (Real.sqrt 3 * g1 * dx2) + (1 / 2) * (g1
    * dy1) + (1 / 2) * (g1 * dy2) + g2 * dy2 + 2 * (g3 * dy2) - g3 * dy3

/-- Row 4 (rotY₂). -/
noncomputable def genLinY2 (g1 g2 g3 dx1 dy1 dx2 dy2 dx3 dy3 : ℝ) : ℝ :=
-(1 / 2) * (Real.sqrt 3 * g1 * dy1) + (1 / 2) * (Real.sqrt 3 * g1 * dy2) + (1 / 2) * (g1
    * dx1) - (3 / 2) * (g1 * dx2) - g2 * dx2 - g3 * dx3

/-- Row 5 (rotX₃). -/
noncomputable def genLinX3 (g1 g2 g3 dx1 dy1 dx2 dy2 dx3 dy3 : ℝ) : ℝ :=
-(1 / 2) * (Real.sqrt 3 * g1 * dx1) + (1 / 2) * (Real.sqrt 3 * g1 * dx3) + (1 / 2) * (g1
    * dy1) + (1 / 2) * (g1 * dy3) - g2 * dy2 + 2 * (g2 * dy3) + g3 * dy3

/-- Row 6 (rotY₃). -/
noncomputable def genLinY3 (g1 g2 g3 dx1 dy1 dx2 dy2 dx3 dy3 : ℝ) : ℝ :=
(1 / 2) * (Real.sqrt 3 * g1 * dy1) - (1 / 2) * (Real.sqrt 3 * g1 * dy3) + (1 / 2) * (g1
    * dx1) - (3 / 2) * (g1 * dx3) - g2 * dx2 - g3 * dx3

private theorem s9_s3cu : (Real.sqrt 3) ^ 3 = 3 * Real.sqrt 3 := by
  linear_combination (Real.sqrt 3) * s3sq

/-- **The translation eigenpair persists for ARBITRARY circulations**: the
    2π-scaled rotating-frame linearization maps the uniform translation
    (c₁,c₂,c₁,c₂,c₁,c₂) to (Gc₂,−Gc₁,…) with G = ΣΓ; eigenvalues ±iG.
    The translation pair never bifurcates on the branch. -/
theorem s9_lin_trans (g1 g2 g3 c1 c2 : ℝ) :
    genLinX1 g1 g2 g3 (c1) (c2) (c1) (c2) (c1) (c2) = g1 * c2 + g2 * c2 + g3 * c2
      ∧ genLinY1 g1 g2 g3 (c1) (c2) (c1) (c2) (c1) (c2) = -g1 * c1 - g2 * c1 - g3 * c1
      ∧ genLinX2 g1 g2 g3 (c1) (c2) (c1) (c2) (c1) (c2) = g1 * c2 + g2 * c2 + g3 * c2
      ∧ genLinY2 g1 g2 g3 (c1) (c2) (c1) (c2) (c1) (c2) = -g1 * c1 - g2 * c1 - g3 * c1
      ∧ genLinX3 g1 g2 g3 (c1) (c2) (c1) (c2) (c1) (c2) = g1 * c2 + g2 * c2 + g3 * c2
      ∧ genLinY3 g1 g2 g3 (c1) (c2) (c1) (c2) (c1) (c2) = -g1 * c1 - g2 * c1 - g3 * c1 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · unfold genLinX1
    ring
  · unfold genLinY1
    ring
  · unfold genLinX2
    ring
  · unfold genLinY2
    ring
  · unfold genLinX3
    ring
  · unfold genLinY3
    ring

/-- **Congruence with the §8 linearization**: at equal circulations
    g1 = g2 = g3 = g the general matrix is exactly g·(linX1…linY3),
    the matrix certified against the true rotating-frame field in §8.4
    (lin_cert_transX/Y, lin_cert_shapeU/W).  The certification therefore
    transfers to genLin on the diagonal family. -/
theorem s9_lin_diag (g dx1 dy1 dx2 dy2 dx3 dy3 : ℝ) :
    genLinX1 g g g (dx1) (dy1) (dx2) (dy2) (dx3) (dy3) = g * linX1 (dx1) (dy1) (dx2) (dy2) (dx3) (dy3)
      ∧ genLinY1 g g g (dx1) (dy1) (dx2) (dy2) (dx3) (dy3) = g * linY1 (dx1) (dy1) (dx2) (dy2) (dx3) (dy3)
      ∧ genLinX2 g g g (dx1) (dy1) (dx2) (dy2) (dx3) (dy3) = g * linX2 (dx1) (dy1) (dx2) (dy2) (dx3) (dy3)
      ∧ genLinY2 g g g (dx1) (dy1) (dx2) (dy2) (dx3) (dy3) = g * linY2 (dx1) (dy1) (dx2) (dy2) (dx3) (dy3)
      ∧ genLinX3 g g g (dx1) (dy1) (dx2) (dy2) (dx3) (dy3) = g * linX3 (dx1) (dy1) (dx2) (dy2) (dx3) (dy3)
      ∧ genLinY3 g g g (dx1) (dy1) (dx2) (dy2) (dx3) (dy3) = g * linY3 (dx1) (dy1) (dx2) (dy2) (dx3) (dy3) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · unfold genLinX1 linX1
    ring
  · unfold genLinY1 linY1
    ring
  · unfold genLinX2 linX2
    ring
  · unfold genLinY2 linY2
    ring
  · unfold genLinX3 linX3
    ring
  · unfold genLinY3 linY3
    ring

/-- **The phase mode lies in the kernel for ARBITRARY circulations.**
    KV = (2√3G/(3g1))·J(anchor) spans ker(genLin): the phase family of
    §9.2 (re-timed solutions) makes the rotating-frame deviation
    R(φ)(anchor) − anchor constant, so the linearized flow kills its
    direction J(anchor) — the zero eigenvalue of §8 persists globally. -/
theorem s9_lin_kernel (g1 g2 g3 : ℝ) :
    genLinX1 g1 g2 g3 (-Real.sqrt 3 * g2 + Real.sqrt 3 * g3) (-3 * g2 - 3 * g3) (Real.sqrt 3 * g1 + 2 * (Real.sqrt 3 * g3)) (3 * g1) (-Real.sqrt 3 * g1 - 2 * (Real.sqrt 3 * g2)) (3 * g1) = 0
      ∧ genLinY1 g1 g2 g3 (-Real.sqrt 3 * g2 + Real.sqrt 3 * g3) (-3 * g2 - 3 * g3) (Real.sqrt 3 * g1 + 2 * (Real.sqrt 3 * g3)) (3 * g1) (-Real.sqrt 3 * g1 - 2 * (Real.sqrt 3 * g2)) (3 * g1) = 0
      ∧ genLinX2 g1 g2 g3 (-Real.sqrt 3 * g2 + Real.sqrt 3 * g3) (-3 * g2 - 3 * g3) (Real.sqrt 3 * g1 + 2 * (Real.sqrt 3 * g3)) (3 * g1) (-Real.sqrt 3 * g1 - 2 * (Real.sqrt 3 * g2)) (3 * g1) = 0
      ∧ genLinY2 g1 g2 g3 (-Real.sqrt 3 * g2 + Real.sqrt 3 * g3) (-3 * g2 - 3 * g3) (Real.sqrt 3 * g1 + 2 * (Real.sqrt 3 * g3)) (3 * g1) (-Real.sqrt 3 * g1 - 2 * (Real.sqrt 3 * g2)) (3 * g1) = 0
      ∧ genLinX3 g1 g2 g3 (-Real.sqrt 3 * g2 + Real.sqrt 3 * g3) (-3 * g2 - 3 * g3) (Real.sqrt 3 * g1 + 2 * (Real.sqrt 3 * g3)) (3 * g1) (-Real.sqrt 3 * g1 - 2 * (Real.sqrt 3 * g2)) (3 * g1) = 0
      ∧ genLinY3 g1 g2 g3 (-Real.sqrt 3 * g2 + Real.sqrt 3 * g3) (-3 * g2 - 3 * g3) (Real.sqrt 3 * g1 + 2 * (Real.sqrt 3 * g3)) (3 * g1) (-Real.sqrt 3 * g1 - 2 * (Real.sqrt 3 * g2)) (3 * g1) = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · simp only [genLinX1]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinY1]
    ring
  · simp only [genLinX2]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinY2]
    ring
  · simp only [genLinX3]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinY3]
    ring

/-- **The size-drift Jordan chain for ARBITRARY circulations.**  ANCH =
    G·(anchor) is the rotating-frame fixed point; the dilation family
    (scaled triangles are again relative equilibria, §9.1) gives
    genLin(ANCH) = −2G·J(ANCH): the generalized zero mode of §8.5
    persists on the whole branch.  Combined with s9_lin_kernel:
    genLin²(ANCH) = 4G²·ANCH − … — the Jordan block at 0. -/
theorem s9_lin_chain (g1 g2 g3 : ℝ) :
    genLinX1 g1 g2 g3 ((1 / 2) * (Real.sqrt 3 * g2) + (1 / 2) * (Real.sqrt 3 * g3)) (-(1 / 2) * g2 + (1 / 2) * g3) (-(1 / 2) * (Real.sqrt 3 * g1)) ((1 / 2) * g1 + g3) (-(1 / 2) * (Real.sqrt 3 * g1)) (-(1 / 2) * g1 - g2) = -g1 * g2 + g1 * g3 - g2 ^ 2 + g3 ^ 2
      ∧ genLinY1 g1 g2 g3 ((1 / 2) * (Real.sqrt 3 * g2) + (1 / 2) * (Real.sqrt 3 * g3)) (-(1 / 2) * g2 + (1 / 2) * g3) (-(1 / 2) * (Real.sqrt 3 * g1)) ((1 / 2) * g1 + g3) (-(1 / 2) * (Real.sqrt 3 * g1)) (-(1 / 2) * g1 - g2) = -Real.sqrt 3 * g1 * g2 - Real.sqrt 3 * g1 * g3 - Real.sqrt 3 * g2 ^ 2 - 2 * (Real.sqrt 3 * g2 * g3) - Real.sqrt 3 * g3 ^ 2
      ∧ genLinX2 g1 g2 g3 ((1 / 2) * (Real.sqrt 3 * g2) + (1 / 2) * (Real.sqrt 3 * g3)) (-(1 / 2) * g2 + (1 / 2) * g3) (-(1 / 2) * (Real.sqrt 3 * g1)) ((1 / 2) * g1 + g3) (-(1 / 2) * (Real.sqrt 3 * g1)) (-(1 / 2) * g1 - g2) = g1 ^ 2 + g1 * g2 + 3 * (g1 * g3) + 2 * (g2 * g3) + 2 * g3 ^ 2
      ∧ genLinY2 g1 g2 g3 ((1 / 2) * (Real.sqrt 3 * g2) + (1 / 2) * (Real.sqrt 3 * g3)) (-(1 / 2) * g2 + (1 / 2) * g3) (-(1 / 2) * (Real.sqrt 3 * g1)) ((1 / 2) * g1 + g3) (-(1 / 2) * (Real.sqrt 3 * g1)) (-(1 / 2) * g1 - g2) = Real.sqrt 3 * g1 ^ 2 + Real.sqrt 3 * g1 * g2 + Real.sqrt 3 * g1 * g3
      ∧ genLinX3 g1 g2 g3 ((1 / 2) * (Real.sqrt 3 * g2) + (1 / 2) * (Real.sqrt 3 * g3)) (-(1 / 2) * g2 + (1 / 2) * g3) (-(1 / 2) * (Real.sqrt 3 * g1)) ((1 / 2) * g1 + g3) (-(1 / 2) * (Real.sqrt 3 * g1)) (-(1 / 2) * g1 - g2) = -g1 ^ 2 - 3 * (g1 * g2) - g1 * g3 - 2 * g2 ^ 2 - 2 * (g2 * g3)
      ∧ genLinY3 g1 g2 g3 ((1 / 2) * (Real.sqrt 3 * g2) + (1 / 2) * (Real.sqrt 3 * g3)) (-(1 / 2) * g2 + (1 / 2) * g3) (-(1 / 2) * (Real.sqrt 3 * g1)) ((1 / 2) * g1 + g3) (-(1 / 2) * (Real.sqrt 3 * g1)) (-(1 / 2) * g1 - g2) = Real.sqrt 3 * g1 ^ 2 + Real.sqrt 3 * g1 * g2 + Real.sqrt 3 * g1 * g3 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · simp only [genLinX1]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinY1]
    ring
  · simp only [genLinX2]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinY2]
    ring
  · simp only [genLinX3]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinY3]
    ring

/-- **The shape-mode characteristic pair for ARBITRARY circulations
    (second-order form).**  genLin²(U) = −3P·U with P = Γ1Γ2+Γ2Γ3+Γ3Γ1
    and U = (−Γ2Ι3, −√3Γ2Ι3, −Γ1Ι3, √3Γ1Ι3, 2Γ1Γ2, 0).  The characteristic
    polynomial of genLin (SymPy-verified) is therefore
        λ·(λ² + G²)·(λ² + 3P)
    with the translation factor ±iG (s9_lin_trans), the kernel/chain at 0
    (s9_lin_kernel, s9_lin_chain) and THE SHAPE FACTOR λ² + 3P:
    P > 0 ⇒ shape oscillates (±i√(3P));  P < 0 ⇒ λ² = −3P > 0 — a REAL
    eigenvalue pair ±√(−3P), linear instability;  P = 0 ⇒ the pair
    collides at the origin — the bifurcation hypersurface Γ1Γ2+Γ2Ι3+Γ3Γ1 = 0. -/
theorem s9_shape_gen (g1 g2 g3 : ℝ) :
    genLinX1 g1 g2 g3 (genLinX1 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinY1 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinX2 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinY2 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinX3 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinY3 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) = 3 * (g1 * g2 ^ 2 * g3) + 3 * (g1 * g2 * g3 ^ 2) + 3 * (g2 ^ 2 * g3 ^ 2)
      ∧ genLinY1 g1 g2 g3 (genLinX1 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinY1 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinX2 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinY2 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinX3 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinY3 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) = 3 * (Real.sqrt 3 * g1 * g2 ^ 2 * g3) + 3 * (Real.sqrt 3 * g1 * g2 * g3 ^ 2) + 3 * (Real.sqrt 3 * g2 ^ 2 * g3 ^ 2)
      ∧ genLinX2 g1 g2 g3 (genLinX1 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinY1 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinX2 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinY2 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinX3 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinY3 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) = 3 * (g1 ^ 2 * g2 * g3) + 3 * (g1 ^ 2 * g3 ^ 2) + 3 * (g1 * g2 * g3 ^ 2)
      ∧ genLinY2 g1 g2 g3 (genLinX1 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinY1 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinX2 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinY2 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinX3 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinY3 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) = -3 * (Real.sqrt 3 * g1 ^ 2 * g2 * g3) - 3 * (Real.sqrt 3 * g1 ^ 2 * g3 ^ 2) - 3 * (Real.sqrt 3 * g1 * g2 * g3 ^ 2)
      ∧ genLinX3 g1 g2 g3 (genLinX1 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinY1 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinX2 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinY2 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinX3 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinY3 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) = -6 * (g1 ^ 2 * g2 ^ 2) - 6 * (g1 ^ 2 * g2 * g3) - 6 * (g1 * g2 ^ 2 * g3)
      ∧ genLinY3 g1 g2 g3 (genLinX1 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinY1 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinX2 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinY2 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinX3 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) (genLinY3 g1 g2 g3 (-g2 * g3) (-Real.sqrt 3 * g2 * g3) (-g1 * g3) (Real.sqrt 3 * g1 * g3) (2 * (g1 * g2)) (0)) = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · simp only [genLinX1, genLinY1, genLinX2, genLinY2, genLinX3, genLinY3]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinX1, genLinY1, genLinX2, genLinY2, genLinX3, genLinY3]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinX1, genLinY1, genLinX2, genLinY2, genLinX3, genLinY3]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinX1, genLinY1, genLinX2, genLinY2, genLinX3, genLinY3]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinX1, genLinY1, genLinX2, genLinY2, genLinX3, genLinY3]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinX1, genLinY1, genLinX2, genLinY2, genLinX3, genLinY3]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring

/-- **Unequal same-sign circulations (Γ = (1,1,4), P = 9 > 0): the shape
    pair oscillates.**  First-order form: genLin(1,1,4)·u4 = −27·utilde4.
    Together with s9_shape4_b this is the complex-structure pair
    J̃² = −27·id on the shape plane: eigenvalues ±i√27 = ±3i√3 — purely
    imaginary (compare ±3i at Γ = (1,1,1) in §8).  The oscillation
    frequency 3√3 replaces 3 as the circulation ratio moves — no growth. -/
theorem s9_shape4_a :
    genLinX1 1 1 4 (-36) (-36 * Real.sqrt 3) (-36) (36 * Real.sqrt 3) (18) (0) = -27 * (8 * Real.sqrt 3)
      ∧ genLinY1 1 1 4 (-36) (-36 * Real.sqrt 3) (-36) (36 * Real.sqrt 3) (18) (0) = -27 * (-16)
      ∧ genLinX2 1 1 4 (-36) (-36 * Real.sqrt 3) (-36) (36 * Real.sqrt 3) (18) (0) = -27 * (-12 * Real.sqrt 3)
      ∧ genLinY2 1 1 4 (-36) (-36 * Real.sqrt 3) (-36) (36 * Real.sqrt 3) (18) (0) = -27 * (-4)
      ∧ genLinX3 1 1 4 (-36) (-36 * Real.sqrt 3) (-36) (36 * Real.sqrt 3) (18) (0) = -27 * (Real.sqrt 3)
      ∧ genLinY3 1 1 4 (-36) (-36 * Real.sqrt 3) (-36) (36 * Real.sqrt 3) (18) (0) = -27 * (5) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · simp only [genLinX1]
    ring
  · simp only [genLinY1]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinX2]
    ring
  · simp only [genLinY2]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinX3]
    ring
  · simp only [genLinY3]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring

/-- **The twin relation**: genLin(1,1,4)·utilde4 = u4 — closes the
    ±3i√3 shape pair at Γ = (1,1,4). -/
theorem s9_shape4_b :
    genLinX1 1 1 4 (8 * Real.sqrt 3) (-16) (-12 * Real.sqrt 3) (-4) (Real.sqrt 3) (5) = -36
      ∧ genLinY1 1 1 4 (8 * Real.sqrt 3) (-16) (-12 * Real.sqrt 3) (-4) (Real.sqrt 3) (5) = -36 * Real.sqrt 3
      ∧ genLinX2 1 1 4 (8 * Real.sqrt 3) (-16) (-12 * Real.sqrt 3) (-4) (Real.sqrt 3) (5) = -36
      ∧ genLinY2 1 1 4 (8 * Real.sqrt 3) (-16) (-12 * Real.sqrt 3) (-4) (Real.sqrt 3) (5) = 36 * Real.sqrt 3
      ∧ genLinX3 1 1 4 (8 * Real.sqrt 3) (-16) (-12 * Real.sqrt 3) (-4) (Real.sqrt 3) (5) = 18
      ∧ genLinY3 1 1 4 (8 * Real.sqrt 3) (-16) (-12 * Real.sqrt 3) (-4) (Real.sqrt 3) (5) = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · simp only [genLinX1]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinY1]
    ring
  · simp only [genLinX2]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinY2]
    ring
  · simp only [genLinX3]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinY3]
    ring

/-- **The shape oscillation is a modal solution at Γ = (1,1,4).**  The
    curve x(t) = 3√3·cos(3√3·t)·u4 + sin(3√3·t)·(−27·utilde4) solves the
    LINEARIZED rotating-frame equation ẋ = genLin(1,1,4)·x exactly for
    every t (all six components).  Rescaling by 1/18 (the theorem's
    vectors are the 18-fold of the primitive u4, utilde4), the primitive
    modal solution has the bounded-oscillation norm
      |x̃(t)|² = 33cos²(3√3t) + 77sin²(3√3t) − 33cos(3√3t)sin(3√3t)
               = 165/2 − (11/2)(3cos + sin)² ≤ 165/2
    (SymPy-checked) — no growth, confirming neutral stability at
    unequal same-sign circulations. -/
theorem s9_lin_sol_shape4 (t : ℝ) :
    HasDerivAt (fun t => ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (-216 * Real.sqrt 3)))
      (genLinX1 1 1 4 ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (-216 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (432)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (324 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (108)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (18) + Real.sin ((3 * Real.sqrt 3) * t) * (-27 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (0) + Real.sin ((3 * Real.sqrt 3) * t) * (-135))) t
      ∧ HasDerivAt (fun t => ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (432)))
      (genLinY1 1 1 4 ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (-216 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (432)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (324 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (108)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (18) + Real.sin ((3 * Real.sqrt 3) * t) * (-27 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (0) + Real.sin ((3 * Real.sqrt 3) * t) * (-135))) t
      ∧ HasDerivAt (fun t => ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (324 * Real.sqrt 3)))
      (genLinX2 1 1 4 ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (-216 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (432)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (324 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (108)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (18) + Real.sin ((3 * Real.sqrt 3) * t) * (-27 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (0) + Real.sin ((3 * Real.sqrt 3) * t) * (-135))) t
      ∧ HasDerivAt (fun t => ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (108)))
      (genLinY2 1 1 4 ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (-216 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (432)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (324 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (108)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (18) + Real.sin ((3 * Real.sqrt 3) * t) * (-27 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (0) + Real.sin ((3 * Real.sqrt 3) * t) * (-135))) t
      ∧ HasDerivAt (fun t => ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (18) + Real.sin ((3 * Real.sqrt 3) * t) * (-27 * Real.sqrt 3)))
      (genLinX3 1 1 4 ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (-216 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (432)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (324 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (108)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (18) + Real.sin ((3 * Real.sqrt 3) * t) * (-27 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (0) + Real.sin ((3 * Real.sqrt 3) * t) * (-135))) t
      ∧ HasDerivAt (fun t => ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (0) + Real.sin ((3 * Real.sqrt 3) * t) * (-135)))
      (genLinY3 1 1 4 ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (-216 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (432)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (324 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (108)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (18) + Real.sin ((3 * Real.sqrt 3) * t) * (-27 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (0) + Real.sin ((3 * Real.sqrt 3) * t) * (-135))) t := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · have h1 : HasDerivAt (fun t => (3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36))
      (-(27) * Real.sin ((3 * Real.sqrt 3) * t) * (-36)) t :=
      HasDerivAt.congr_deriv
      (deriv_congr ((cos_comp (3 * Real.sqrt 3) t).const_mul ((3 * Real.sqrt 3) * (-36)))
      (fun s => by ring))
      (by ring_nf; simp only [s3sq, s9_s3cu]; ring)
    have h2 : HasDerivAt (fun t => Real.sin ((3 * Real.sqrt 3) * t) * (-216 * Real.sqrt 3))
      (Real.cos ((3 * Real.sqrt 3) * t) * ((3 * Real.sqrt 3) * (-216 * Real.sqrt 3))) t :=
      HasDerivAt.congr_deriv
      (deriv_congr ((sin_comp (3 * Real.sqrt 3) t).const_mul (-216 * Real.sqrt 3))
      (fun s => by ring))
      (by ring)
    show HasDerivAt (fun t => ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (-216 * Real.sqrt 3)))
      (genLinX1 1 1 4 ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (-216 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (432)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (324 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (108)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (18) + Real.sin ((3 * Real.sqrt 3) * t) * (-27 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (0) + Real.sin ((3 * Real.sqrt 3) * t) * (-135))) t
    refine (deriv_congr (h1.add h2) (fun s => rfl)).congr_deriv ?_
    simp only [genLinX1]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · have h1 : HasDerivAt (fun t => (3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36 * Real.sqrt 3))
      (-(27) * Real.sin ((3 * Real.sqrt 3) * t) * (-36 * Real.sqrt 3)) t :=
      HasDerivAt.congr_deriv
      (deriv_congr ((cos_comp (3 * Real.sqrt 3) t).const_mul ((3 * Real.sqrt 3) * (-36 * Real.sqrt 3)))
      (fun s => by ring))
      (by ring_nf; simp only [s3sq, s9_s3cu]; ring)
    have h2 : HasDerivAt (fun t => Real.sin ((3 * Real.sqrt 3) * t) * (432))
      (Real.cos ((3 * Real.sqrt 3) * t) * ((3 * Real.sqrt 3) * (432))) t :=
      HasDerivAt.congr_deriv
      (deriv_congr ((sin_comp (3 * Real.sqrt 3) t).const_mul (432))
      (fun s => by ring))
      (by ring)
    show HasDerivAt (fun t => ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (432)))
      (genLinY1 1 1 4 ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (-216 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (432)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (324 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (108)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (18) + Real.sin ((3 * Real.sqrt 3) * t) * (-27 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (0) + Real.sin ((3 * Real.sqrt 3) * t) * (-135))) t
    refine (deriv_congr (h1.add h2) (fun s => rfl)).congr_deriv ?_
    simp only [genLinY1]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · have h1 : HasDerivAt (fun t => (3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36))
      (-(27) * Real.sin ((3 * Real.sqrt 3) * t) * (-36)) t :=
      HasDerivAt.congr_deriv
      (deriv_congr ((cos_comp (3 * Real.sqrt 3) t).const_mul ((3 * Real.sqrt 3) * (-36)))
      (fun s => by ring))
      (by ring_nf; simp only [s3sq, s9_s3cu]; ring)
    have h2 : HasDerivAt (fun t => Real.sin ((3 * Real.sqrt 3) * t) * (324 * Real.sqrt 3))
      (Real.cos ((3 * Real.sqrt 3) * t) * ((3 * Real.sqrt 3) * (324 * Real.sqrt 3))) t :=
      HasDerivAt.congr_deriv
      (deriv_congr ((sin_comp (3 * Real.sqrt 3) t).const_mul (324 * Real.sqrt 3))
      (fun s => by ring))
      (by ring)
    show HasDerivAt (fun t => ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (324 * Real.sqrt 3)))
      (genLinX2 1 1 4 ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (-216 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (432)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (324 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (108)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (18) + Real.sin ((3 * Real.sqrt 3) * t) * (-27 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (0) + Real.sin ((3 * Real.sqrt 3) * t) * (-135))) t
    refine (deriv_congr (h1.add h2) (fun s => rfl)).congr_deriv ?_
    simp only [genLinX2]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · have h1 : HasDerivAt (fun t => (3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (36 * Real.sqrt 3))
      (-(27) * Real.sin ((3 * Real.sqrt 3) * t) * (36 * Real.sqrt 3)) t :=
      HasDerivAt.congr_deriv
      (deriv_congr ((cos_comp (3 * Real.sqrt 3) t).const_mul ((3 * Real.sqrt 3) * (36 * Real.sqrt 3)))
      (fun s => by ring))
      (by ring_nf; simp only [s3sq, s9_s3cu]; ring)
    have h2 : HasDerivAt (fun t => Real.sin ((3 * Real.sqrt 3) * t) * (108))
      (Real.cos ((3 * Real.sqrt 3) * t) * ((3 * Real.sqrt 3) * (108))) t :=
      HasDerivAt.congr_deriv
      (deriv_congr ((sin_comp (3 * Real.sqrt 3) t).const_mul (108))
      (fun s => by ring))
      (by ring)
    show HasDerivAt (fun t => ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (108)))
      (genLinY2 1 1 4 ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (-216 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (432)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (324 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (108)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (18) + Real.sin ((3 * Real.sqrt 3) * t) * (-27 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (0) + Real.sin ((3 * Real.sqrt 3) * t) * (-135))) t
    refine (deriv_congr (h1.add h2) (fun s => rfl)).congr_deriv ?_
    simp only [genLinY2]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · have h1 : HasDerivAt (fun t => (3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (18))
      (-(27) * Real.sin ((3 * Real.sqrt 3) * t) * (18)) t :=
      HasDerivAt.congr_deriv
      (deriv_congr ((cos_comp (3 * Real.sqrt 3) t).const_mul ((3 * Real.sqrt 3) * (18)))
      (fun s => by ring))
      (by ring_nf; simp only [s3sq, s9_s3cu]; ring)
    have h2 : HasDerivAt (fun t => Real.sin ((3 * Real.sqrt 3) * t) * (-27 * Real.sqrt 3))
      (Real.cos ((3 * Real.sqrt 3) * t) * ((3 * Real.sqrt 3) * (-27 * Real.sqrt 3))) t :=
      HasDerivAt.congr_deriv
      (deriv_congr ((sin_comp (3 * Real.sqrt 3) t).const_mul (-27 * Real.sqrt 3))
      (fun s => by ring))
      (by ring)
    show HasDerivAt (fun t => ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (18) + Real.sin ((3 * Real.sqrt 3) * t) * (-27 * Real.sqrt 3)))
      (genLinX3 1 1 4 ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (-216 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (432)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (324 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (108)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (18) + Real.sin ((3 * Real.sqrt 3) * t) * (-27 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (0) + Real.sin ((3 * Real.sqrt 3) * t) * (-135))) t
    refine (deriv_congr (h1.add h2) (fun s => rfl)).congr_deriv ?_
    simp only [genLinX3]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · have h1 : HasDerivAt (fun t => (3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (0))
      (-(27) * Real.sin ((3 * Real.sqrt 3) * t) * (0)) t :=
      HasDerivAt.congr_deriv
      (deriv_congr ((cos_comp (3 * Real.sqrt 3) t).const_mul ((3 * Real.sqrt 3) * (0)))
      (fun s => by ring))
      (by ring)
    have h2 : HasDerivAt (fun t => Real.sin ((3 * Real.sqrt 3) * t) * (-135))
      (Real.cos ((3 * Real.sqrt 3) * t) * ((3 * Real.sqrt 3) * (-135))) t :=
      HasDerivAt.congr_deriv
      (deriv_congr ((sin_comp (3 * Real.sqrt 3) t).const_mul (-135))
      (fun s => by ring))
      (by ring)
    show HasDerivAt (fun t => ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (0) + Real.sin ((3 * Real.sqrt 3) * t) * (-135)))
      (genLinY3 1 1 4 ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (-216 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (432)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (-36) + Real.sin ((3 * Real.sqrt 3) * t) * (324 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (36 * Real.sqrt 3) + Real.sin ((3 * Real.sqrt 3) * t) * (108)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (18) + Real.sin ((3 * Real.sqrt 3) * t) * (-27 * Real.sqrt 3)) ((3 * Real.sqrt 3) * Real.cos ((3 * Real.sqrt 3) * t) * (0) + Real.sin ((3 * Real.sqrt 3) * t) * (-135))) t
    refine (deriv_congr (h1.add h2) (fun s => rfl)).congr_deriv ?_
    simp only [genLinY3]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring

/-- **The bifurcation point Γ = (1,1,−1/2): the shape pair collides at 0.**
    Here P = 1+2Γ = 0, and the kernel of genLin(1,1,−1/2) gains the shape
    direction Uh (kernel rank jumps 1 → 2): the eigenvalue 0 of the
    characteristic factor λ²+3P reaches algebraic multiplicity 4. -/
theorem s9_collision_a :
    genLinX1 1 1 (-1/2) (-3 * Real.sqrt 3) (-3) (0) (6) (-6 * Real.sqrt 3) (6) = 0
      ∧ genLinY1 1 1 (-1/2) (-3 * Real.sqrt 3) (-3) (0) (6) (-6 * Real.sqrt 3) (6) = 0
      ∧ genLinX2 1 1 (-1/2) (-3 * Real.sqrt 3) (-3) (0) (6) (-6 * Real.sqrt 3) (6) = 0
      ∧ genLinY2 1 1 (-1/2) (-3 * Real.sqrt 3) (-3) (0) (6) (-6 * Real.sqrt 3) (6) = 0
      ∧ genLinX3 1 1 (-1/2) (-3 * Real.sqrt 3) (-3) (0) (6) (-6 * Real.sqrt 3) (6) = 0
      ∧ genLinY3 1 1 (-1/2) (-3 * Real.sqrt 3) (-3) (0) (6) (-6 * Real.sqrt 3) (6) = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · simp only [genLinX1]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinY1]
    ring
  · simp only [genLinX2]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinY2]
    ring
  · simp only [genLinX3]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinY3]
    ring

/-- **The Jordan chain at the collision**: genLin(1,1,−1/2)·Utilde2 = Uh.
    The shape plane carries a nontrivial Jordan block at the eigenvalue 0
    — the steady-state (Krein) collision: crossing Γ = −1/2 the purely
    imaginary pair ±i√(3P)→±√(−3P) passes through zero and re-emerges
    on the real axis (linear instability for Γ < −1/2). -/
theorem s9_collision_b :
    genLinX1 1 1 (-1/2) (-2) (-2 * Real.sqrt 3) (-2) (2 * Real.sqrt 3) (-8) (0) = -3 * Real.sqrt 3
      ∧ genLinY1 1 1 (-1/2) (-2) (-2 * Real.sqrt 3) (-2) (2 * Real.sqrt 3) (-8) (0) = -3
      ∧ genLinX2 1 1 (-1/2) (-2) (-2 * Real.sqrt 3) (-2) (2 * Real.sqrt 3) (-8) (0) = 0
      ∧ genLinY2 1 1 (-1/2) (-2) (-2 * Real.sqrt 3) (-2) (2 * Real.sqrt 3) (-8) (0) = 6
      ∧ genLinX3 1 1 (-1/2) (-2) (-2 * Real.sqrt 3) (-2) (2 * Real.sqrt 3) (-8) (0) = -6 * Real.sqrt 3
      ∧ genLinY3 1 1 (-1/2) (-2) (-2 * Real.sqrt 3) (-2) (2 * Real.sqrt 3) (-8) (0) = 6 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · simp only [genLinX1]
    ring
  · simp only [genLinY1]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinX2]
    ring
  · simp only [genLinY2]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinX3]
    ring
  · simp only [genLinY3]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring

/-- **Mixed-sign circulations Γ = (1,1,−1): LINEAR INSTABILITY.**  Here
    P = 1−1−1 = −1 < 0 and the shape factor λ²+3P = λ²−3 contributes the
    REAL eigenvalue pair ±√3: genLin(1,1,−1)·v = √3·v with the exact
    eigenvector v = (1, √3, 1, −√3, 2, 0).  A real positive eigenvalue of
    the rotating-frame linearization means exponential growth of shape
    perturbations — the equilateral Lagrange configuration is linearly
    UNSTABLE on this side of the bifurcation hypersurface. -/
theorem s9_eig_unst :
    genLinX1 1 1 (-1) (1) (Real.sqrt 3) (1) (-Real.sqrt 3) (2) (0) = Real.sqrt 3 * (1)
      ∧ genLinY1 1 1 (-1) (1) (Real.sqrt 3) (1) (-Real.sqrt 3) (2) (0) = Real.sqrt 3 * (Real.sqrt 3)
      ∧ genLinX2 1 1 (-1) (1) (Real.sqrt 3) (1) (-Real.sqrt 3) (2) (0) = Real.sqrt 3 * (1)
      ∧ genLinY2 1 1 (-1) (1) (Real.sqrt 3) (1) (-Real.sqrt 3) (2) (0) = Real.sqrt 3 * (-Real.sqrt 3)
      ∧ genLinX3 1 1 (-1) (1) (Real.sqrt 3) (1) (-Real.sqrt 3) (2) (0) = Real.sqrt 3 * (2)
      ∧ genLinY3 1 1 (-1) (1) (Real.sqrt 3) (1) (-Real.sqrt 3) (2) (0) = Real.sqrt 3 * (0) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · simp only [genLinX1]
    ring
  · simp only [genLinY1]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · simp only [genLinX2]
    ring
  · simp only [genLinY2]
    ring
  · simp only [genLinX3]
    ring
  · simp only [genLinY3]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring

private theorem s9_exp_comp (t : ℝ) :
    HasDerivAt (fun s => Real.exp (Real.sqrt 3 * s))
      (Real.exp (Real.sqrt 3 * t) * Real.sqrt 3) t :=
  (Real.hasDerivAt_exp (Real.sqrt 3 * t)).comp t
    (hasDerivAt_const_mul_id (Real.sqrt 3) t)

/-- **The growing modal solution at Γ = (1,1,−1).**  m(t) = e^(√3·t)·v
    solves the linearized rotating-frame equation ẋ = genLin(1,1,−1)·m
    exactly (all six components).  Its norm grows like e^(√3·t):
    |m(t)|² = 12·e^(2√3·t) (s9_growth_norm) — the modal perturbation
    amplifies by a factor e^√3 every unit time: exponential instability. -/
theorem s9_lin_sol_unst (t : ℝ) :
    HasDerivAt (fun t => Real.exp (Real.sqrt 3 * t) * (1))
      (genLinX1 1 1 (-1) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (-Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (2)) (Real.exp (Real.sqrt 3 * t) * (0))) t
      ∧ HasDerivAt (fun t => Real.exp (Real.sqrt 3 * t) * (Real.sqrt 3))
      (genLinY1 1 1 (-1) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (-Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (2)) (Real.exp (Real.sqrt 3 * t) * (0))) t
      ∧ HasDerivAt (fun t => Real.exp (Real.sqrt 3 * t) * (1))
      (genLinX2 1 1 (-1) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (-Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (2)) (Real.exp (Real.sqrt 3 * t) * (0))) t
      ∧ HasDerivAt (fun t => Real.exp (Real.sqrt 3 * t) * (-Real.sqrt 3))
      (genLinY2 1 1 (-1) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (-Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (2)) (Real.exp (Real.sqrt 3 * t) * (0))) t
      ∧ HasDerivAt (fun t => Real.exp (Real.sqrt 3 * t) * (2))
      (genLinX3 1 1 (-1) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (-Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (2)) (Real.exp (Real.sqrt 3 * t) * (0))) t
      ∧ HasDerivAt (fun t => Real.exp (Real.sqrt 3 * t) * (0))
      (genLinY3 1 1 (-1) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (-Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (2)) (Real.exp (Real.sqrt 3 * t) * (0))) t := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · have h1 : HasDerivAt (fun t => Real.exp (Real.sqrt 3 * t) * (1))
      (Real.sqrt 3 * Real.exp (Real.sqrt 3 * t) * (1)) t :=
      HasDerivAt.congr_deriv
      (deriv_congr ((s9_exp_comp t).const_mul (1))
      (fun s => by ring))
      (by ring)
    show HasDerivAt (fun t => Real.exp (Real.sqrt 3 * t) * (1))
      (genLinX1 1 1 (-1) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (-Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (2)) (Real.exp (Real.sqrt 3 * t) * (0))) t
    refine (deriv_congr h1 (fun s => rfl)).congr_deriv ?_
    simp only [genLinX1]
    ring
  · have h1 : HasDerivAt (fun t => Real.exp (Real.sqrt 3 * t) * (Real.sqrt 3))
      (Real.sqrt 3 * Real.exp (Real.sqrt 3 * t) * (Real.sqrt 3)) t :=
      HasDerivAt.congr_deriv
      (deriv_congr ((s9_exp_comp t).const_mul (Real.sqrt 3))
      (fun s => by ring))
      (by ring)
    show HasDerivAt (fun t => Real.exp (Real.sqrt 3 * t) * (Real.sqrt 3))
      (genLinY1 1 1 (-1) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (-Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (2)) (Real.exp (Real.sqrt 3 * t) * (0))) t
    refine (deriv_congr h1 (fun s => rfl)).congr_deriv ?_
    simp only [genLinY1]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring
  · have h1 : HasDerivAt (fun t => Real.exp (Real.sqrt 3 * t) * (1))
      (Real.sqrt 3 * Real.exp (Real.sqrt 3 * t) * (1)) t :=
      HasDerivAt.congr_deriv
      (deriv_congr ((s9_exp_comp t).const_mul (1))
      (fun s => by ring))
      (by ring)
    show HasDerivAt (fun t => Real.exp (Real.sqrt 3 * t) * (1))
      (genLinX2 1 1 (-1) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (-Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (2)) (Real.exp (Real.sqrt 3 * t) * (0))) t
    refine (deriv_congr h1 (fun s => rfl)).congr_deriv ?_
    simp only [genLinX2]
    ring
  · have h1 : HasDerivAt (fun t => Real.exp (Real.sqrt 3 * t) * (-Real.sqrt 3))
      (Real.sqrt 3 * Real.exp (Real.sqrt 3 * t) * (-Real.sqrt 3)) t :=
      HasDerivAt.congr_deriv
      (deriv_congr ((s9_exp_comp t).const_mul (-Real.sqrt 3))
      (fun s => by ring))
      (by ring)
    show HasDerivAt (fun t => Real.exp (Real.sqrt 3 * t) * (-Real.sqrt 3))
      (genLinY2 1 1 (-1) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (-Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (2)) (Real.exp (Real.sqrt 3 * t) * (0))) t
    refine (deriv_congr h1 (fun s => rfl)).congr_deriv ?_
    simp only [genLinY2]
    ring
  · have h1 : HasDerivAt (fun t => Real.exp (Real.sqrt 3 * t) * (2))
      (Real.sqrt 3 * Real.exp (Real.sqrt 3 * t) * (2)) t :=
      HasDerivAt.congr_deriv
      (deriv_congr ((s9_exp_comp t).const_mul (2))
      (fun s => by ring))
      (by ring)
    show HasDerivAt (fun t => Real.exp (Real.sqrt 3 * t) * (2))
      (genLinX3 1 1 (-1) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (-Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (2)) (Real.exp (Real.sqrt 3 * t) * (0))) t
    refine (deriv_congr h1 (fun s => rfl)).congr_deriv ?_
    simp only [genLinX3]
    ring
  · have h1 : HasDerivAt (fun t => Real.exp (Real.sqrt 3 * t) * (0))
      (Real.sqrt 3 * Real.exp (Real.sqrt 3 * t) * (0)) t :=
      HasDerivAt.congr_deriv
      (deriv_congr ((s9_exp_comp t).const_mul (0))
      (fun s => by ring))
      (by ring)
    show HasDerivAt (fun t => Real.exp (Real.sqrt 3 * t) * (0))
      (genLinY3 1 1 (-1) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (1)) (Real.exp (Real.sqrt 3 * t) * (-Real.sqrt 3)) (Real.exp (Real.sqrt 3 * t) * (2)) (Real.exp (Real.sqrt 3 * t) * (0))) t
    refine (deriv_congr h1 (fun s => rfl)).congr_deriv ?_
    simp only [genLinY3]
    ring_nf
    simp only [s3sq, s9_s3cu]
    ring

/-- **Exponential growth of the unstable mode (norm identity).**
    |m(t)|² = 12·e^(2√3·t): the shape perturbation of the mixed-sign
    triangle Γ = (1,1,−1) is unbounded — the nonlinear counterpart of the
    §8 stability bounds, on the far side of the bifurcation. -/
theorem s9_growth_norm (t : ℝ) :
    (Real.exp (Real.sqrt 3 * t) * (1)) ^ 2
      + (Real.exp (Real.sqrt 3 * t) * (Real.sqrt 3)) ^ 2
      + (Real.exp (Real.sqrt 3 * t) * (1)) ^ 2
      + (Real.exp (Real.sqrt 3 * t) * (-(Real.sqrt 3))) ^ 2
      + (Real.exp (Real.sqrt 3 * t) * (2)) ^ 2
      + (Real.exp (Real.sqrt 3 * t) * (0)) ^ 2
      = 12 * Real.exp (Real.sqrt 3 * t) ^ 2 := by
  ring_nf
  linear_combination (2 * Real.exp (Real.sqrt 3 * t) ^ 2) * s3sq

/-!
## Section 10 — nonlinear Lyapunov stability via H/I and collinear bifurcations (v6.0)

### 10.1  The energy–Casimir (Lyapunov H/I) stability of the Lagrange triangle

The conserved quantities of §3/§5 — the Hamiltonian H, the angular impulse
I and the linear impulses P, Q — are now used as a Lyapunov (energy–Casimir)
certificate.  At the unit anchor (side a = 1) the level set

    {P = 0, Q = 0, I = Γ}

carries a rigid identity: the sum of the three squared sides is EXACTLY 3.
On that set, whenever every squared side stays in the annulus [1/2, 3/2],
the Hamiltonian dominates the squared shape deviation:

    H ≥ (Γ²/(12π)) · Σ_{pairs} (d2_ij − 1)²,

with the anchor value H₀ = 0 as the minimum.  This is the coercive
Lyapunov inequality; the closing theorems `s10_lyapunov_stab` /
`s10_lyapunov_dist` propagate it in time and yield nonlinear (Lyapunov)
stability of the triangle orbit: the shape deviation is bounded by the
conserved energy excess FOR ALL TIME.
-/

private theorem s10_gsq_pos (g : ℝ) (hg : g ≠ 0) : (0:ℝ) < g * g := by
  rcases lt_or_gt_of_ne hg with h | h <;> nlinarith

/-- Continuity of the square of a continuous real function. -/
private theorem s10_sq_cont {f : ℝ → ℝ} (hf : Continuous f) :
    Continuous (fun s => f s ^ 2) := by
  have h2 : (fun s => f s ^ 2) = (fun s => f s * f s) := by
    funext s
    rw [pow_two]
  rw [h2]
  exact hf.mul hf

/-- Derivative of t ↦ t². -/
private theorem s10_id_sq_deriv (t : ℝ) :
    HasDerivAt (fun s : ℝ => s ^ 2) (2 * t) t := by
  have h : HasDerivAt (fun s : ℝ => s * s) (t + t) t := by
    refine HasDerivAt.congr_deriv ((hasDerivAt_id t).mul (hasDerivAt_id t)) ?_
    simp only [id_eq]
    ring
  have h2 : (fun s : ℝ => s ^ 2) = (fun s : ℝ => s * s) := by
    funext s
    rw [pow_two]
  rw [h2]
  exact h.congr_deriv (by ring)

/-- Derivative of w ↦ w − w²/3 at any point. -/
private theorem s10_Bderiv_lemma (v : ℝ) :
    HasDerivAt (fun w : ℝ => w - w ^ 2 / 3) (1 - 2 * v / 3) v := by
  have hfun : (fun w : ℝ => w - w ^ 2 / 3)
      = (fun w : ℝ => id w - (fun s : ℝ => s ^ 2) w / 3) := by
    funext w
    simp only [id_eq]
  rw [hfun]
  exact (hasDerivAt_id v).sub ((s10_id_sq_deriv v).div_const 3)

/-- Derivative of w ↦ −w − w²/3 at any point. -/
private theorem s10_Bderiv2_lemma (v : ℝ) :
    HasDerivAt (fun w : ℝ => -w - w ^ 2 / 3) (-1 - 2 * v / 3) v := by
  have hfun : (fun w : ℝ => -w - w ^ 2 / 3)
      = (fun w : ℝ => -id w - (fun s : ℝ => s ^ 2) w / 3) := by
    funext w
    simp only [id_eq]
  rw [hfun]
  exact (hasDerivAt_id v).neg.sub ((s10_id_sq_deriv v).div_const 3)

/-! ### the one-dimensional logarithmic Lyapunov inequality -/

/-- **The logarithmic Lyapunov inequality.**  For every `u` in the
    annulus [−1/2, 1/2],  ln(1+u) ≤ u − u²/3.  Both sides are compared
    by the fencing theorem on the two half-intervals, anchored at the
    exact contact point u = 0 where both sides equal 0. -/
theorem s10_log_bound (u : ℝ) (h1 : -(1/2 : ℝ) ≤ u) (h2 : u ≤ 1/2) :
    Real.log (1 + u) ≤ u - u ^ 2 / 3 := by
  have hfpos : ContinuousOn (fun v : ℝ => Real.log (1 + v)) (Set.Icc 0 (1/2)) := by
    intro v hv
    have hne : (1 + v : ℝ) ≠ 0 := by
      have h := (Set.mem_Icc.mp hv).1
      linarith
    exact ((Real.continuousAt_log hne).comp_continuousWithinAt
      ((continuous_const.add continuous_id).continuousWithinAt))
  have hfneg : ContinuousOn (fun v : ℝ => Real.log (1 - v)) (Set.Icc 0 (1/2)) := by
    intro v hv
    have hne : (1 - v : ℝ) ≠ 0 := by
      have h := (Set.mem_Icc.mp hv).2
      linarith
    exact ((Real.continuousAt_log hne).comp_continuousWithinAt
      ((continuous_const.sub continuous_id).continuousWithinAt))
  have hBcont : ContinuousOn (fun v : ℝ => v - v ^ 2 / 3) (Set.Icc 0 (1/2)) :=
    (continuous_id.sub ((s10_sq_cont continuous_id).div_const 3)).continuousOn
  have hBcont2 : ContinuousOn (fun v : ℝ => -v - v ^ 2 / 3) (Set.Icc 0 (1/2)) :=
    ((continuous_id.neg).sub ((s10_sq_cont continuous_id).div_const 3)).continuousOn
  have hBderiv : ∀ v ∈ Set.Ico (0:ℝ) (1/2),
      HasDerivWithinAt (fun w : ℝ => w - w ^ 2 / 3) (1 - 2 * v / 3) (Set.Ici v) v :=
    fun v _ => (s10_Bderiv_lemma v).hasDerivWithinAt
  have hBderiv2 : ∀ v ∈ Set.Ico (0:ℝ) (1/2),
      HasDerivWithinAt (fun w : ℝ => -w - w ^ 2 / 3) (-1 - 2 * v / 3) (Set.Ici v) v :=
    fun v _ => (s10_Bderiv2_lemma v).hasDerivWithinAt
  -- positive half: log(1+v) ≤ v − v²/3 on [0, 1/2]
  have hpos : ∀ v ∈ Set.Icc (0:ℝ) (1/2), Real.log (1 + v) ≤ v - v ^ 2 / 3 := by
    refine image_le_of_deriv_right_le_deriv_boundary (f' := fun v => 1 / (1 + v)) hfpos ?_
      (by simp) hBcont hBderiv ?_
    · intro v hv
      have hne : (1 + v : ℝ) ≠ 0 := by
        have h := (Set.mem_Ico.mp hv).1
        linarith
      exact (((hasDerivAt_const v (1:ℝ)).add (hasDerivAt_id v)).log hne).hasDerivWithinAt.congr_deriv
        (by simp only [zero_add, id_eq])
    · intro v hv
      have hx1 : (0:ℝ) < 1 + v := by
        have hq := (Set.mem_Ico.mp hv).1
        linarith
      have hx2 : v ≤ 1/2 := by
        have hq := (Set.mem_Ico.mp hv).2
        linarith
      have hx0 : 0 ≤ v := by
        have hq := (Set.mem_Ico.mp hv).1
        linarith
      have h2v : 0 ≤ 1 - 2 * v := by linarith
      rw [div_le_iff hx1]
      nlinarith [hx0, h2v]
  -- negative half: log(1−v) ≤ −v − v²/3 on [0, 1/2]
  have hneg : ∀ v ∈ Set.Icc (0:ℝ) (1/2), Real.log (1 - v) ≤ -v - v ^ 2 / 3 := by
    refine image_le_of_deriv_right_le_deriv_boundary (f' := fun v => -1 / (1 - v)) hfneg ?_
      (by simp) hBcont2 hBderiv2 ?_
    · intro v hv
      have hne : (1 - v : ℝ) ≠ 0 := by
        have h := (Set.mem_Ico.mp hv).2
        linarith
      exact (((hasDerivAt_const v (1:ℝ)).sub (hasDerivAt_id v)).log hne).hasDerivWithinAt.congr_deriv
        (by simp only [zero_sub, id_eq])
    · intro v hv
      have hx1 : (0:ℝ) < 1 - v := by
        have hq := (Set.mem_Ico.mp hv).2
        linarith
      have hx0 : 0 ≤ v := by
        have hq := (Set.mem_Ico.mp hv).1
        linarith
      have h3 : (1:ℝ) / (1 - v) ≥ 1 + 2 * v / 3 := by
        rw [ge_iff_le, le_div_iff hx1]
        nlinarith [hx0]
      show -1 / (1 - v) ≤ -1 - 2 * v / 3
      rw [show -1 / (1 - v) = -((1:ℝ) / (1 - v)) from by ring]
      linarith
  rcases le_or_lt u 0 with hle | hlt
  · -- u ≤ 0: apply the negative half with v = −u
    have hv : -u ∈ Set.Icc (0:ℝ) (1/2) := by
      constructor
      · linarith
      · linarith
    have h := hneg (-u) hv
    have e1 : Real.log (1 + u) = Real.log (1 - -u) := by
      rw [show 1 - -u = 1 + u from by ring]
    rw [e1]
    have e2 : u - u ^ 2 / 3 = -(-u) - (-u) ^ 2 / 3 := by ring
    rw [e2]
    exact h
  · -- u ≥ 0: apply the positive half
    have hv : u ∈ Set.Icc (0:ℝ) (1/2) := by
      constructor
      · linarith
      · linarith
    exact hpos u hv

/-! ### the sum-of-squares identity on the momentum level set -/

/-- The sum of the three squared sides is 3·Σ|w|² − |Σw|²: pure algebra. -/
theorem s10_sumsq (x1 y1 x2 y2 x3 y3 : ℝ) :
    d2 x1 y1 x2 y2 + d2 x1 y1 x3 y3 + d2 x2 y2 x3 y3
      = 3 * (x1 ^ 2 + y1 ^ 2 + x2 ^ 2 + y2 ^ 2 + x3 ^ 2 + y3 ^ 2)
        - ((x1 + x2 + x3) ^ 2 + (y1 + y2 + y3) ^ 2) := by
  unfold d2
  ring

/-- **The rigid identity on the anchor level set.**  For equal circulations
    with P = Q = 0 and I = Γ (the unit-anchor values), the sum of the three
    squared sides is EXACTLY 3 — the shape space is compact without any
    further normalization. -/
theorem s10_sumsq_anchor (g x1 y1 x2 y2 x3 y3 : ℝ) (hg : g ≠ 0)
    (hP : Pvortex g g g x1 x2 x3 = 0) (hQ : Qvortex g g g y1 y2 y3 = 0)
    (hI : Ivortex g g g x1 y1 x2 y2 x3 y3 = g) :
    d2 x1 y1 x2 y2 + d2 x1 y1 x3 y3 + d2 x2 y2 x3 y3 = 3 := by
  have hx : x1 + x2 + x3 = 0 := by
    have h2 : g * (x1 + x2 + x3) = 0 := by
      unfold Pvortex at hP
      rw [show g * (x1 + x2 + x3) = g * x1 + g * x2 + g * x3 from by ring]
      exact hP
    rcases mul_eq_zero.mp h2 with h | h
    · exact absurd h hg
    · linarith
  have hy : y1 + y2 + y3 = 0 := by
    have h2 : g * (y1 + y2 + y3) = 0 := by
      unfold Qvortex at hQ
      rw [show g * (y1 + y2 + y3) = g * y1 + g * y2 + g * y3 from by ring]
      exact hQ
    rcases mul_eq_zero.mp h2 with h | h
    · exact absurd h hg
    · linarith
  have hsq : x1 ^ 2 + y1 ^ 2 + x2 ^ 2 + y2 ^ 2 + x3 ^ 2 + y3 ^ 2 = 1 := by
    have h2 : Ivortex g g g x1 y1 x2 y2 x3 y3
        = g * (x1 ^ 2 + y1 ^ 2 + x2 ^ 2 + y2 ^ 2 + x3 ^ 2 + y3 ^ 2) := by
      unfold Ivortex
      ring
    rw [h2] at hI
    have hI4 : g * (x1 ^ 2 + y1 ^ 2 + x2 ^ 2 + y2 ^ 2 + x3 ^ 2 + y3 ^ 2) = g * 1 := by
      rw [mul_one]
      exact hI
    exact mul_left_cancel₀ hg hI4
  rw [s10_sumsq x1 y1 x2 y2 x3 y3, hx, hy]
  rw [show (0:ℝ) ^ 2 + (0:ℝ) ^ 2 = 0 from by ring]
  linarith

/-- **AM–GM for three positive reals with sum 3**: xyz ≤ 1, proved by pure
    algebra (4xy ≤ (x+y)² and s²(3−s) ≤ 4 via (2−s)²(s+1) ≥ 0). -/
private theorem s10_amgm3 (x y z : ℝ) (hx : 0 < x) (hy : 0 < y) (hz : 0 < z)
    (hsum : x + y + z = 3) : x * y * z ≤ 1 := by
  have h1 : 4 * x * y ≤ (x + y) ^ 2 := by nlinarith [sq_nonneg (x - y)]
  have hzs : z = 3 - x - y := by linarith
  subst hzs
  have hs : 0 < x + y := by linarith
  have hz2 : 0 ≤ 3 - x - y := le_of_lt hz
  have hprod : 0 ≤ (2 - (x + y)) ^ 2 * ((x + y) + 1) := by
    have hp2 : 0 ≤ (2 - (x + y)) ^ 2 := sq_nonneg _
    have hp3 : 0 ≤ (x + y) + 1 := le_of_lt (by linarith)
    nlinarith [hp2, hp3]
  have hid : 4 - (x + y) ^ 2 * (3 - (x + y)) = (2 - (x + y)) ^ 2 * ((x + y) + 1) := by
    ring
  have k1 : 4 * (x * y * (3 - x - y)) ≤ (x + y) ^ 2 * (3 - x - y) := by
    nlinarith [h1, hz2]
  have k2 : (x + y) ^ 2 * (3 - (x + y)) ≤ 4 := by
    linarith [hid, hprod]
  linarith

/-- **H is globally nonnegative on the anchor level set.**  With P = Q = 0,
    I = Γ and pairwise distinct vortices, the Hamiltonian satisfies
    H ≥ 0 = H(anchor): the equilateral triangle is the global energy
    minimum of the level set (AM–GM on the three squared sides). -/
theorem s10_H_nonneg (g x1 y1 x2 y2 x3 y3 : ℝ) (hg : g ≠ 0)
    (hP : Pvortex g g g x1 x2 x3 = 0) (hQ : Qvortex g g g y1 y2 y3 = 0)
    (hI : Ivortex g g g x1 y1 x2 y2 x3 y3 = g)
    (e12 : d2 x1 y1 x2 y2 ≠ 0) (e13 : d2 x1 y1 x3 y3 ≠ 0) (e23 : d2 x2 y2 x3 y3 ≠ 0) :
    0 ≤ Hvortex g g g x1 y1 x2 y2 x3 y3 := by
  have hp12 : 0 < d2 x1 y1 x2 y2 := by
    have hle : (0:ℝ) ≤ d2 x1 y1 x2 y2 := by unfold d2; positivity
    exact lt_of_le_of_ne hle (Ne.symm e12)
  have hp13 : 0 < d2 x1 y1 x3 y3 := by
    have hle : (0:ℝ) ≤ d2 x1 y1 x3 y3 := by unfold d2; positivity
    exact lt_of_le_of_ne hle (Ne.symm e13)
  have hp23 : 0 < d2 x2 y2 x3 y3 := by
    have hle : (0:ℝ) ≤ d2 x2 y2 x3 y3 := by unfold d2; positivity
    exact lt_of_le_of_ne hle (Ne.symm e23)
  have hprod : d2 x1 y1 x2 y2 * d2 x1 y1 x3 y3 * d2 x2 y2 x3 y3 ≤ 1 :=
    s10_amgm3 (d2 x1 y1 x2 y2) (d2 x1 y1 x3 y3) (d2 x2 y2 x3 y3) hp12 hp13 hp23
      (by linarith [s10_sumsq_anchor g x1 y1 x2 y2 x3 y3 hg hP hQ hI])
  have hlog : Real.log (d2 x1 y1 x2 y2) + Real.log (d2 x1 y1 x3 y3)
      + Real.log (d2 x2 y2 x3 y3) ≤ 0 := by
    have e1 : Real.log (d2 x1 y1 x2 y2) + Real.log (d2 x1 y1 x3 y3)
        + Real.log (d2 x2 y2 x3 y3)
        = Real.log (d2 x1 y1 x2 y2 * d2 x1 y1 x3 y3 * d2 x2 y2 x3 y3) := by
      rw [Real.log_mul (ne_of_gt (mul_pos hp12 hp13)) (ne_of_gt hp23),
        Real.log_mul (ne_of_gt hp12) (ne_of_gt hp13)]
    rw [e1]
    have h2 : Real.log (d2 x1 y1 x2 y2 * d2 x1 y1 x3 y3 * d2 x2 y2 x3 y3)
        ≤ Real.log 1 := Real.log_le_log (mul_pos (mul_pos hp12 hp13) hp23) hprod
    rwa [Real.log_one] at h2
  have hpos2 : (0:ℝ) < g * g / (4 * Real.pi) :=
    div_pos (s10_gsq_pos g hg) (by linarith [Real.pi_pos])
  have hHv : Hvortex g g g x1 y1 x2 y2 x3 y3
      = (g * g / (4 * Real.pi)) * -(Real.log (d2 x1 y1 x2 y2)
        + Real.log (d2 x1 y1 x3 y3) + Real.log (d2 x2 y2 x3 y3)) := by
    unfold Hvortex
    rw [vortexDist_eq x1 y1 x2 y2, Real.log_sqrt (by unfold d2; positivity),
      vortexDist_eq x1 y1 x3 y3, Real.log_sqrt (by unfold d2; positivity),
      vortexDist_eq x2 y2 x3 y3, Real.log_sqrt (by unfold d2; positivity)]
    ring
  rw [hHv]
  exact mul_nonneg hpos2.le (by linarith)

/-! ### the coercive Lyapunov inequality -/

/-- **The coercive Lyapunov inequality (energy–Casimir certificate).**  On
    the anchor level set {P = 0, Q = 0, I = Γ} with every squared side in
    the annulus [1/2, 3/2], the Hamiltonian dominates the squared shape
    deviation:
      H ≥ (Γ²/(12π)) · ((d2_12 − 1)² + (d2_13 − 1)² + (d2_23 − 1)²).
    The proof chains the logarithmic Lyapunov inequality over the three
    sides with the rigid identity Σd2 = 3. -/
theorem s10_coercive (g x1 y1 x2 y2 x3 y3 : ℝ) (hg : g ≠ 0)
    (hP : Pvortex g g g x1 x2 x3 = 0) (hQ : Qvortex g g g y1 y2 y3 = 0)
    (hI : Ivortex g g g x1 y1 x2 y2 x3 y3 = g)
    (hA : (1/2 : ℝ) ≤ d2 x1 y1 x2 y2) (hA2 : d2 x1 y1 x2 y2 ≤ 3/2)
    (hB : (1/2 : ℝ) ≤ d2 x1 y1 x3 y3) (hB2 : d2 x1 y1 x3 y3 ≤ 3/2)
    (hC : (1/2 : ℝ) ≤ d2 x2 y2 x3 y3) (hC2 : d2 x2 y2 x3 y3 ≤ 3/2) :
    (g * g / (12 * Real.pi)) * ((d2 x1 y1 x2 y2 - 1) ^ 2 + (d2 x1 y1 x3 y3 - 1) ^ 2
        + (d2 x2 y2 x3 y3 - 1) ^ 2)
      ≤ Hvortex g g g x1 y1 x2 y2 x3 y3 := by
  have u12 : -(1/2 : ℝ) ≤ d2 x1 y1 x2 y2 - 1 ∧ d2 x1 y1 x2 y2 - 1 ≤ 1/2 := by
    constructor <;> linarith
  have u13 : -(1/2 : ℝ) ≤ d2 x1 y1 x3 y3 - 1 ∧ d2 x1 y1 x3 y3 - 1 ≤ 1/2 := by
    constructor <;> linarith
  have u23 : -(1/2 : ℝ) ≤ d2 x2 y2 x3 y3 - 1 ∧ d2 x2 y2 x3 y3 - 1 ≤ 1/2 := by
    constructor <;> linarith
  have l12 : Real.log (d2 x1 y1 x2 y2) ≤ (d2 x1 y1 x2 y2 - 1)
      - (d2 x1 y1 x2 y2 - 1) ^ 2 / 3 := by
    have e1 : Real.log (d2 x1 y1 x2 y2) = Real.log (1 + (d2 x1 y1 x2 y2 - 1)) := by
      rw [show 1 + (d2 x1 y1 x2 y2 - 1) = d2 x1 y1 x2 y2 from by ring]
    rw [e1]
    exact s10_log_bound _ u12.1 u12.2
  have l13 : Real.log (d2 x1 y1 x3 y3) ≤ (d2 x1 y1 x3 y3 - 1)
      - (d2 x1 y1 x3 y3 - 1) ^ 2 / 3 := by
    have e1 : Real.log (d2 x1 y1 x3 y3) = Real.log (1 + (d2 x1 y1 x3 y3 - 1)) := by
      rw [show 1 + (d2 x1 y1 x3 y3 - 1) = d2 x1 y1 x3 y3 from by ring]
    rw [e1]
    exact s10_log_bound _ u13.1 u13.2
  have l23 : Real.log (d2 x2 y2 x3 y3) ≤ (d2 x2 y2 x3 y3 - 1)
      - (d2 x2 y2 x3 y3 - 1) ^ 2 / 3 := by
    have e1 : Real.log (d2 x2 y2 x3 y3) = Real.log (1 + (d2 x2 y2 x3 y3 - 1)) := by
      rw [show 1 + (d2 x2 y2 x3 y3 - 1) = d2 x2 y2 x3 y3 from by ring]
    rw [e1]
    exact s10_log_bound _ u23.1 u23.2
  have hsum3 := s10_sumsq_anchor g x1 y1 x2 y2 x3 y3 hg hP hQ hI
  have hzero : (d2 x1 y1 x2 y2 - 1) + (d2 x1 y1 x3 y3 - 1) + (d2 x2 y2 x3 y3 - 1) = 0 := by
    linarith
  have hL : Real.log (d2 x1 y1 x2 y2) + Real.log (d2 x1 y1 x3 y3)
      + Real.log (d2 x2 y2 x3 y3)
      ≤ -((d2 x1 y1 x2 y2 - 1) ^ 2 + (d2 x1 y1 x3 y3 - 1) ^ 2
        + (d2 x2 y2 x3 y3 - 1) ^ 2) / 3 := by
    linarith
  set U := (d2 x1 y1 x2 y2 - 1) ^ 2 + (d2 x1 y1 x3 y3 - 1) ^ 2
    + (d2 x2 y2 x3 y3 - 1) ^ 2 with hUdef
  have hs12 : 0 ≤ d2 x1 y1 x2 y2 := by unfold d2; positivity
  have hs13 : 0 ≤ d2 x1 y1 x3 y3 := by unfold d2; positivity
  have hs23 : 0 ≤ d2 x2 y2 x3 y3 := by unfold d2; positivity
  have hpos : (0:ℝ) < g * g / (4 * Real.pi) :=
    div_pos (s10_gsq_pos g hg) (by linarith [Real.pi_pos])
  have hHv : Hvortex g g g x1 y1 x2 y2 x3 y3
      = -(g * g / (4 * Real.pi)) * (Real.log (d2 x1 y1 x2 y2)
        + Real.log (d2 x1 y1 x3 y3) + Real.log (d2 x2 y2 x3 y3)) := by
    unfold Hvortex
    rw [vortexDist_eq x1 y1 x2 y2, Real.log_sqrt hs12,
      vortexDist_eq x1 y1 x3 y3, Real.log_sqrt hs13,
      vortexDist_eq x2 y2 x3 y3, Real.log_sqrt hs23]
    ring
  have h1 : (g * g / (4 * Real.pi)) * (Real.log (d2 x1 y1 x2 y2)
      + Real.log (d2 x1 y1 x3 y3) + Real.log (d2 x2 y2 x3 y3))
      ≤ (g * g / (4 * Real.pi)) * (-U / 3) := by
    exact mul_le_mul_of_nonneg_left hL (le_of_lt hpos)
  rw [hHv, show (g * g / (12 * Real.pi)) * U
      = -((g * g / (4 * Real.pi)) * (-U / 3)) from by ring, neg_mul]
  exact neg_le_neg h1

/-- **The distance form of the certificate.**  (r_ij − 1)² ≤ (d2_ij − 1)²
    pointwise, since (r²−1)² − (r−1)² = (r−1)²·r·(r+2) ≥ 0. -/
private theorem s10_dist_sq (x1 y1 x2 y2 : ℝ) :
    (vortexDist x1 y1 x2 y2 - 1) ^ 2 ≤ (d2 x1 y1 x2 y2 - 1) ^ 2 := by
  have hr : 0 ≤ vortexDist x1 y1 x2 y2 := by unfold vortexDist; positivity
  have he : d2 x1 y1 x2 y2 = vortexDist x1 y1 x2 y2 ^ 2 := by
    rw [vortexDist_eq, Real.sq_sqrt (by unfold d2; positivity)]
  rw [he]
  have p1 : 0 ≤ (vortexDist x1 y1 x2 y2 - 1) ^ 2 := sq_nonneg _
  have p2 : 0 ≤ vortexDist x1 y1 x2 y2 * (vortexDist x1 y1 x2 y2 + 2) := by
    have h2 : 0 ≤ vortexDist x1 y1 x2 y2 ^ 2 := sq_nonneg _
    nlinarith [hr]
  have p3 : 0 ≤ (vortexDist x1 y1 x2 y2 - 1) ^ 2
      * (vortexDist x1 y1 x2 y2 * (vortexDist x1 y1 x2 y2 + 2)) := by
    nlinarith [p1, p2]
  have e2 : (vortexDist x1 y1 x2 y2 ^ 2 - 1) ^ 2
      - (vortexDist x1 y1 x2 y2 - 1) ^ 2
      = (vortexDist x1 y1 x2 y2 - 1) ^ 2
        * (vortexDist x1 y1 x2 y2 * (vortexDist x1 y1 x2 y2 + 2)) := by
    ring
  linarith [e2 ▸ p3]

/-- **Corollary — the Lyapunov certificate in distance form.**  Under the
    hypotheses of `s10_coercive`,
      Σ (r_ij − 1)² ≤ (12π/Γ²) · H. -/
theorem s10_dist_bound (g x1 y1 x2 y2 x3 y3 : ℝ) (hg : g ≠ 0)
    (hP : Pvortex g g g x1 x2 x3 = 0) (hQ : Qvortex g g g y1 y2 y3 = 0)
    (hI : Ivortex g g g x1 y1 x2 y2 x3 y3 = g)
    (hA : (1/2 : ℝ) ≤ d2 x1 y1 x2 y2) (hA2 : d2 x1 y1 x2 y2 ≤ 3/2)
    (hB : (1/2 : ℝ) ≤ d2 x1 y1 x3 y3) (hB2 : d2 x1 y1 x3 y3 ≤ 3/2)
    (hC : (1/2 : ℝ) ≤ d2 x2 y2 x3 y3) (hC2 : d2 x2 y2 x3 y3 ≤ 3/2) :
    (vortexDist x1 y1 x2 y2 - 1) ^ 2 + (vortexDist x1 y1 x3 y3 - 1) ^ 2
      + (vortexDist x2 y2 x3 y3 - 1) ^ 2
      ≤ (12 * Real.pi / (g * g)) * Hvortex g g g x1 y1 x2 y2 x3 y3 := by
  have hpos : (0:ℝ) < g * g / (12 * Real.pi) :=
    div_pos (s10_gsq_pos g hg) (by linarith [Real.pi_pos])
  have h := s10_coercive g x1 y1 x2 y2 x3 y3 hg hP hQ hI hA hA2 hB hB2 hC hC2
  have hcomm : (g * g / (12 * Real.pi)) * ((d2 x1 y1 x2 y2 - 1) ^ 2
      + (d2 x1 y1 x3 y3 - 1) ^ 2 + (d2 x2 y2 x3 y3 - 1) ^ 2)
      = ((d2 x1 y1 x2 y2 - 1) ^ 2 + (d2 x1 y1 x3 y3 - 1) ^ 2
        + (d2 x2 y2 x3 y3 - 1) ^ 2) * (g * g / (12 * Real.pi)) := by
    rw [mul_comm]
  rw [hcomm] at h
  have hdiv : (d2 x1 y1 x2 y2 - 1) ^ 2 + (d2 x1 y1 x3 y3 - 1) ^ 2
      + (d2 x2 y2 x3 y3 - 1) ^ 2
      ≤ (12 * Real.pi / (g * g)) * Hvortex g g g x1 y1 x2 y2 x3 y3 := by
    rw [show (12 * Real.pi / (g * g)) * Hvortex g g g x1 y1 x2 y2 x3 y3
        = Hvortex g g g x1 y1 x2 y2 x3 y3 / (g * g / (12 * Real.pi)) from by
          field_simp [hg, Real.pi_pos]; ring]
    exact (le_div_iff hpos).mpr h
  have e1 := s10_dist_sq x1 y1 x2 y2
  have e2 := s10_dist_sq x1 y1 x3 y3
  have e3 := s10_dist_sq x2 y2 x3 y3
  linarith [hdiv, e1, e2, e3]

/-! ### the variational principle: partial gradients at the anchor

The four slot-derivatives of a pair logarithm (which coordinate slot
varies), then the six partial gradients of H and of I at the equilateral
anchor, and the Lagrange multiplier identity: the energy–Casimir
functional  H + (3Γ/(4π))·I  has ZERO gradient at the anchor — the
variational statement that the triangle is a critical point of H on every
I-level (with multiplier ω_L = 3Γ/(4π); the factor 2 relative to the §8
rotation rate ω = 3Γ/(2π) reflects the convention I = ΣΓ|w|²). -/

private theorem s10_inv_s3 : (1:ℝ) / Real.sqrt 3 = Real.sqrt 3 / 3 := by
  have hs3ne : Real.sqrt 3 ≠ 0 := by positivity
  rw [div_eq_iff hs3ne, show (Real.sqrt 3 / 3) * Real.sqrt 3
      = (Real.sqrt 3) ^ 2 / 3 from by ring, s3sq]
  norm_num

private theorem s10_inv_2s3 : (1:ℝ) / (2 * Real.sqrt 3) = Real.sqrt 3 / 6 := by
  rw [div_eq_iff (by exact mul_ne_zero two_ne_zero (ne_of_gt (Real.sqrt_pos.mpr (by norm_num : (0:ℝ) < 3)))),
    show (Real.sqrt 3 / 6) * (2 * Real.sqrt 3) = (Real.sqrt 3) ^ 2 / 3 from by ring, s3sq]
  norm_num

/-- Slot 1 (x of the first point) of the pair log. -/
private theorem s10_dlog1 (t Y P Q : ℝ) (hne : d2 t Y P Q ≠ 0) :
    HasDerivAt (fun w : ℝ => Real.log (vortexDist w Y P Q))
      ((t - P) / d2 t Y P Q) t := by
  have h := deriv_log_dist (hasDerivAt_id t) (hasDerivAt_const t Y)
    (hasDerivAt_const t P) (hasDerivAt_const t Q) hne
  exact (deriv_congr h (by intro s; rfl)).congr_deriv (by
    simp only [id_eq]
    ring)

/-- Slot 2 (y of the first point) of the pair log. -/
private theorem s10_dlog2 (t X P Q : ℝ) (hne : d2 X t P Q ≠ 0) :
    HasDerivAt (fun w : ℝ => Real.log (vortexDist X w P Q))
      ((t - Q) / d2 X t P Q) t := by
  have h := deriv_log_dist (hasDerivAt_const t X) (hasDerivAt_id t)
    (hasDerivAt_const t P) (hasDerivAt_const t Q) hne
  exact (deriv_congr h (by intro s; rfl)).congr_deriv (by
    simp only [id_eq]
    ring)

/-- Slot 3 (x of the second point) of the pair log. -/
private theorem s10_dlog3 (t X Y Q : ℝ) (hne : d2 X Y t Q ≠ 0) :
    HasDerivAt (fun w : ℝ => Real.log (vortexDist X Y w Q))
      ((t - X) / d2 X Y t Q) t := by
  have h := deriv_log_dist (hasDerivAt_const t X) (hasDerivAt_const t Y)
    (hasDerivAt_id t) (hasDerivAt_const t Q) hne
  exact (deriv_congr h (by intro s; rfl)).congr_deriv (by
    simp only [id_eq]
    ring)

/-- Slot 4 (y of the second point) of the pair log. -/
private theorem s10_dlog4 (t X Y P : ℝ) (hne : d2 X Y P t ≠ 0) :
    HasDerivAt (fun w : ℝ => Real.log (vortexDist X Y P w))
      ((t - Y) / d2 X Y P t) t := by
  have h := deriv_log_dist (hasDerivAt_const t X) (hasDerivAt_const t Y)
    (hasDerivAt_const t P) (hasDerivAt_id t) hne
  exact (deriv_congr h (by intro s; rfl)).congr_deriv (by
    simp only [id_eq]
    ring)

private theorem s10_dH_x1 (g : ℝ) :
    HasDerivAt (fun w => Hvortex g g g w eqY1 eqX2 eqY2 eqX3 eqY3)
      (-(3 * g * g / (2 * Real.pi)) * eqX1) eqX1 := by
  have hs3ne : Real.sqrt 3 ≠ 0 := by positivity
  have hA : HasDerivAt (fun w : ℝ => Real.log (vortexDist w eqY1 eqX2 eqY2))
      (Real.sqrt 3 / 2) eqX1 :=
    (s10_dlog1 eqX1 eqY1 eqX2 eqY2 (by rw [d2_anchor12]; norm_num)).congr_deriv
      (by rw [eqdx12, d2_anchor12]; ring)
  have hB : HasDerivAt (fun w : ℝ => Real.log (vortexDist w eqY1 eqX3 eqY3))
      (Real.sqrt 3 / 2) eqX1 :=
    (s10_dlog1 eqX1 eqY1 eqX3 eqY3 (by rw [d2_anchor13]; norm_num)).congr_deriv
      (by rw [eqdx13, d2_anchor13]; ring)
  have hC : HasDerivAt (fun w : ℝ => Real.log (vortexDist eqX2 eqY2 eqX3 eqY3)) 0 eqX1 :=
    hasDerivAt_const _ _
  have hsum := ((hA.const_mul (g * g)).add (hB.const_mul (g * g))).add (hC.const_mul (g * g))
  have hsum2 := deriv_mul_const_left hsum (c := -(1 / (2 * Real.pi)))
  exact (deriv_congr hsum2 (by intro w; unfold Hvortex; ring)).congr_deriv
    (by unfold eqX1; rw [s10_inv_s3]; ring)

private theorem s10_dH_y1 (g : ℝ) :
    HasDerivAt (fun w => Hvortex g g g eqX1 w eqX2 eqY2 eqX3 eqY3)
      (-(3 * g * g / (2 * Real.pi)) * eqY1) eqY1 := by
  have hA : HasDerivAt (fun w : ℝ => Real.log (vortexDist eqX1 w eqX2 eqY2))
      (-(1 / 2)) eqY1 :=
    (s10_dlog2 eqY1 eqX1 eqX2 eqY2 (by rw [d2_anchor12]; norm_num)).congr_deriv
      (by rw [eqdy12, d2_anchor12]; ring)
  have hB : HasDerivAt (fun w : ℝ => Real.log (vortexDist eqX1 w eqX3 eqY3))
      (1 / 2) eqY1 :=
    (s10_dlog2 eqY1 eqX1 eqX3 eqY3 (by rw [d2_anchor13]; norm_num)).congr_deriv
      (by rw [eqdy13, d2_anchor13]; ring)
  have hC : HasDerivAt (fun w : ℝ => Real.log (vortexDist eqX2 eqY2 eqX3 eqY3)) 0 eqY1 :=
    hasDerivAt_const _ _
  have hsum := ((hA.const_mul (g * g)).add (hB.const_mul (g * g))).add (hC.const_mul (g * g))
  have hsum2 := deriv_mul_const_left hsum (c := -(1 / (2 * Real.pi)))
  exact (deriv_congr hsum2 (by intro w; unfold Hvortex; ring)).congr_deriv
    (by unfold eqY1; ring)

private theorem s10_dH_x2 (g : ℝ) :
    HasDerivAt (fun w => Hvortex g g g eqX1 eqY1 w eqY2 eqX3 eqY3)
      (-(3 * g * g / (2 * Real.pi)) * eqX2) eqX2 := by
  have hs3ne : Real.sqrt 3 ≠ 0 := by positivity
  have hA : HasDerivAt (fun w : ℝ => Real.log (vortexDist eqX1 eqY1 w eqY2))
      (-(Real.sqrt 3 / 2)) eqX2 :=
    (s10_dlog3 eqX2 eqX1 eqY1 eqY2 (by rw [d2_anchor12]; norm_num)).congr_deriv
      (by rw [eqdx21, d2_anchor12]; ring)
  have hB : HasDerivAt (fun w : ℝ => Real.log (vortexDist w eqY2 eqX3 eqY3))
      0 eqX2 :=
    (s10_dlog1 eqX2 eqY2 eqX3 eqY3 (by rw [d2_anchor23]; norm_num)).congr_deriv
      (by rw [eqdx23, d2_anchor23]; ring)
  have hC : HasDerivAt (fun w : ℝ => Real.log (vortexDist eqX1 eqY1 eqX3 eqY3)) 0 eqX2 :=
    hasDerivAt_const _ _
  have hsum := ((hA.const_mul (g * g)).add (hB.const_mul (g * g))).add (hC.const_mul (g * g))
  have hsum2 := deriv_mul_const_left hsum (c := -(1 / (2 * Real.pi)))
  exact (deriv_congr hsum2 (by intro w; unfold Hvortex; ring)).congr_deriv
    (by unfold eqX2; rw [s10_inv_2s3]; ring)

private theorem s10_dH_y2 (g : ℝ) :
    HasDerivAt (fun w => Hvortex g g g eqX1 eqY1 eqX2 w eqX3 eqY3)
      (-(3 * g * g / (2 * Real.pi)) * eqY2) eqY2 := by
  have hA : HasDerivAt (fun w : ℝ => Real.log (vortexDist eqX1 eqY1 eqX2 w))
      (1 / 2) eqY2 :=
    (s10_dlog4 eqY2 eqX1 eqY1 eqX2 (by rw [d2_anchor12]; norm_num)).congr_deriv
      (by rw [eqdy21, d2_anchor12]; ring)
  have hB : HasDerivAt (fun w : ℝ => Real.log (vortexDist eqX2 w eqX3 eqY3))
      1 eqY2 :=
    (s10_dlog2 eqY2 eqX2 eqX3 eqY3 (by rw [d2_anchor23]; norm_num)).congr_deriv
      (by rw [eqdy23, d2_anchor23]; ring)
  have hC : HasDerivAt (fun w : ℝ => Real.log (vortexDist eqX1 eqY1 eqX3 eqY3)) 0 eqY2 :=
    hasDerivAt_const _ _
  have hsum := ((hA.const_mul (g * g)).add (hB.const_mul (g * g))).add (hC.const_mul (g * g))
  have hsum2 := deriv_mul_const_left hsum (c := -(1 / (2 * Real.pi)))
  exact (deriv_congr hsum2 (by intro w; unfold Hvortex; ring)).congr_deriv
    (by unfold eqY2; ring)

private theorem s10_dH_x3 (g : ℝ) :
    HasDerivAt (fun w => Hvortex g g g eqX1 eqY1 eqX2 eqY2 w eqY3)
      (-(3 * g * g / (2 * Real.pi)) * eqX3) eqX3 := by
  have hs3ne : Real.sqrt 3 ≠ 0 := by positivity
  have hA : HasDerivAt (fun w : ℝ => Real.log (vortexDist eqX1 eqY1 w eqY3))
      (-(Real.sqrt 3 / 2)) eqX3 :=
    (s10_dlog3 eqX3 eqX1 eqY1 eqY3 (by rw [d2_anchor13]; norm_num)).congr_deriv
      (by rw [eqdx31, d2_anchor13]; ring)
  have hB : HasDerivAt (fun w : ℝ => Real.log (vortexDist eqX2 eqY2 w eqY3))
      0 eqX3 :=
    (s10_dlog3 eqX3 eqX2 eqY2 eqY3 (by rw [d2_anchor23]; norm_num)).congr_deriv
      (by
        have e : eqX3 - eqX2 = 0 := by unfold eqX2 eqX3; ring
        rw [e, d2_anchor23]; ring)
  have hC : HasDerivAt (fun w : ℝ => Real.log (vortexDist eqX1 eqY1 eqX2 eqY2)) 0 eqX3 :=
    hasDerivAt_const _ _
  have hsum := ((hA.const_mul (g * g)).add (hB.const_mul (g * g))).add (hC.const_mul (g * g))
  have hsum2 := deriv_mul_const_left hsum (c := -(1 / (2 * Real.pi)))
  exact (deriv_congr hsum2 (by intro w; unfold Hvortex; ring)).congr_deriv
    (by unfold eqX3; rw [s10_inv_2s3]; ring)

private theorem s10_dH_y3 (g : ℝ) :
    HasDerivAt (fun w => Hvortex g g g eqX1 eqY1 eqX2 eqY2 eqX3 w)
      (-(3 * g * g / (2 * Real.pi)) * eqY3) eqY3 := by
  have hA : HasDerivAt (fun w : ℝ => Real.log (vortexDist eqX1 eqY1 eqX3 w))
      (-(1 / 2)) eqY3 :=
    (s10_dlog4 eqY3 eqX1 eqY1 eqX3 (by rw [d2_anchor13]; norm_num)).congr_deriv
      (by rw [eqdy31, d2_anchor13]; ring)
  have hB : HasDerivAt (fun w : ℝ => Real.log (vortexDist eqX2 eqY2 eqX3 w))
      (-1) eqY3 :=
    (s10_dlog4 eqY3 eqX2 eqY2 eqX3 (by rw [d2_anchor23]; norm_num)).congr_deriv
      (by
        have e : eqY3 - eqY2 = -1 := by unfold eqY2 eqY3; ring
        rw [e, d2_anchor23]; ring)
  have hC : HasDerivAt (fun w : ℝ => Real.log (vortexDist eqX1 eqY1 eqX2 eqY2)) 0 eqY3 :=
    hasDerivAt_const _ _
  have hsum := ((hA.const_mul (g * g)).add (hB.const_mul (g * g))).add (hC.const_mul (g * g))
  have hsum2 := deriv_mul_const_left hsum (c := -(1 / (2 * Real.pi)))
  exact (deriv_congr hsum2 (by intro w; unfold Hvortex; ring)).congr_deriv
    (by unfold eqY3; ring)

/-! the six partial gradients of the angular impulse (pure polynomials) -/

private theorem s10_dI_x1 (g : ℝ) :
    HasDerivAt (fun w => Ivortex g g g w eqY1 eqX2 eqY2 eqX3 eqY3) (2 * g * eqX1) eqX1 := by
  have h1 : HasDerivAt (fun w : ℝ => w * w) (eqX1 + eqX1) eqX1 := by
    refine HasDerivAt.congr_deriv ((hasDerivAt_id eqX1).mul (hasDerivAt_id eqX1)) ?_
    simp only [id_eq]
    ring
  have h2 : HasDerivAt (fun w : ℝ => eqY1 * eqY1) 0 eqX1 := hasDerivAt_const _ _
  have h3 : HasDerivAt (fun w : ℝ => eqX2 * eqX2 + eqY2 * eqY2) 0 eqX1 :=
    hasDerivAt_const _ _
  have h4 : HasDerivAt (fun w : ℝ => eqX3 * eqX3 + eqY3 * eqY3) 0 eqX1 :=
    hasDerivAt_const _ _
  have h := ((h1.add h2).const_mul g).add ((h3.const_mul g).add (h4.const_mul g))
  exact (deriv_congr h (by intro w; unfold Ivortex; ring)).congr_deriv (by ring)

private theorem s10_dI_y1 (g : ℝ) :
    HasDerivAt (fun w => Ivortex g g g eqX1 w eqX2 eqY2 eqX3 eqY3) (2 * g * eqY1) eqY1 := by
  have h1 : HasDerivAt (fun w : ℝ => eqX1 * eqX1) 0 eqY1 := hasDerivAt_const _ _
  have h2 : HasDerivAt (fun w : ℝ => w * w) (eqY1 + eqY1) eqY1 := by
    refine HasDerivAt.congr_deriv ((hasDerivAt_id eqY1).mul (hasDerivAt_id eqY1)) ?_
    simp only [id_eq]
    ring
  have h3 : HasDerivAt (fun w : ℝ => eqX2 * eqX2 + eqY2 * eqY2) 0 eqY1 :=
    hasDerivAt_const _ _
  have h4 : HasDerivAt (fun w : ℝ => eqX3 * eqX3 + eqY3 * eqY3) 0 eqY1 :=
    hasDerivAt_const _ _
  have h := ((h1.add h2).const_mul g).add ((h3.const_mul g).add (h4.const_mul g))
  exact (deriv_congr h (by intro w; unfold Ivortex; ring)).congr_deriv (by ring)

private theorem s10_dI_x2 (g : ℝ) :
    HasDerivAt (fun w => Ivortex g g g eqX1 eqY1 w eqY2 eqX3 eqY3) (2 * g * eqX2) eqX2 := by
  have h1 : HasDerivAt (fun w : ℝ => eqX1 * eqX1 + eqY1 * eqY1) 0 eqX2 :=
    hasDerivAt_const _ _
  have h2 : HasDerivAt (fun w : ℝ => w * w) (eqX2 + eqX2) eqX2 := by
    refine HasDerivAt.congr_deriv ((hasDerivAt_id eqX2).mul (hasDerivAt_id eqX2)) ?_
    simp only [id_eq]
    ring
  have h3 : HasDerivAt (fun w : ℝ => eqY2 * eqY2) 0 eqX2 := hasDerivAt_const _ _
  have h4 : HasDerivAt (fun w : ℝ => eqX3 * eqX3 + eqY3 * eqY3) 0 eqX2 :=
    hasDerivAt_const _ _
  have h := ((h1.add h2).const_mul g).add ((h3.const_mul g).add (h4.const_mul g))
  exact (deriv_congr h (by intro w; unfold Ivortex; ring)).congr_deriv (by ring)

private theorem s10_dI_y2 (g : ℝ) :
    HasDerivAt (fun w => Ivortex g g g eqX1 eqY1 eqX2 w eqX3 eqY3) (2 * g * eqY2) eqY2 := by
  have h1 : HasDerivAt (fun w : ℝ => eqX1 * eqX1 + eqY1 * eqY1) 0 eqY2 :=
    hasDerivAt_const _ _
  have h2 : HasDerivAt (fun w : ℝ => eqX2 * eqX2) 0 eqY2 := hasDerivAt_const _ _
  have h3 : HasDerivAt (fun w : ℝ => w * w) (eqY2 + eqY2) eqY2 := by
    refine HasDerivAt.congr_deriv ((hasDerivAt_id eqY2).mul (hasDerivAt_id eqY2)) ?_
    simp only [id_eq]
    ring
  have h4 : HasDerivAt (fun w : ℝ => eqX3 * eqX3 + eqY3 * eqY3) 0 eqY2 :=
    hasDerivAt_const _ _
  have h := ((h1.add h2).const_mul g).add ((h3.const_mul g).add (h4.const_mul g))
  exact (deriv_congr h (by intro w; unfold Ivortex; ring)).congr_deriv (by ring)

private theorem s10_dI_x3 (g : ℝ) :
    HasDerivAt (fun w => Ivortex g g g eqX1 eqY1 eqX2 eqY2 w eqY3) (2 * g * eqX3) eqX3 := by
  have h1 : HasDerivAt (fun w : ℝ => eqX1 * eqX1 + eqY1 * eqY1) 0 eqX3 :=
    hasDerivAt_const _ _
  have h2 : HasDerivAt (fun w : ℝ => eqX2 * eqX2 + eqY2 * eqY2) 0 eqX3 :=
    hasDerivAt_const _ _
  have h3 : HasDerivAt (fun w : ℝ => w * w) (eqX3 + eqX3) eqX3 := by
    refine HasDerivAt.congr_deriv ((hasDerivAt_id eqX3).mul (hasDerivAt_id eqX3)) ?_
    simp only [id_eq]
    ring
  have h4 : HasDerivAt (fun w : ℝ => eqY3 * eqY3) 0 eqX3 := hasDerivAt_const _ _
  have h := ((h1.add h2).const_mul g).add ((h3.const_mul g).add (h4.const_mul g))
  exact (deriv_congr h (by intro w; unfold Ivortex; ring)).congr_deriv (by ring)

private theorem s10_dI_y3 (g : ℝ) :
    HasDerivAt (fun w => Ivortex g g g eqX1 eqY1 eqX2 eqY2 eqX3 w) (2 * g * eqY3) eqY3 := by
  have h1 : HasDerivAt (fun w : ℝ => eqX1 * eqX1 + eqY1 * eqY1) 0 eqY3 :=
    hasDerivAt_const _ _
  have h2 : HasDerivAt (fun w : ℝ => eqX2 * eqX2 + eqY2 * eqY2) 0 eqY3 :=
    hasDerivAt_const _ _
  have h3 : HasDerivAt (fun w : ℝ => eqX3 * eqX3) 0 eqY3 := hasDerivAt_const _ _
  have h4 : HasDerivAt (fun w : ℝ => w * w) (eqY3 + eqY3) eqY3 := by
    refine HasDerivAt.congr_deriv ((hasDerivAt_id eqY3).mul (hasDerivAt_id eqY3)) ?_
    simp only [id_eq]
    ring
  have h := ((h1.add h2).const_mul g).add ((h3.const_mul g).add (h4.const_mul g))
  exact (deriv_congr h (by intro w; unfold Ivortex; ring)).congr_deriv (by ring)

/-! ### the Lagrange multiplier identity (energy–Casimir criticality) -/

/-- **Variational principle, x₁-slot.**  The energy–Casimir functional
    H + (3Γ/(4π))·I has zero x₁-gradient at the anchor:
    ∇H = −(3Γ/(4π))·∇I there (Lagrange multiplier ω_L = 3Γ/(4π)). -/
theorem s10_casimir_x1 (g : ℝ) :
    HasDerivAt (fun w => Hvortex g g g w eqY1 eqX2 eqY2 eqX3 eqY3
      + (3 * g / (4 * Real.pi)) * Ivortex g g g w eqY1 eqX2 eqY2 eqX3 eqY3) 0 eqX1 := by
  have hH := s10_dH_x1 g
  have hI := s10_dI_x1 g
  exact (hH.add (deriv_mul_const_left hI (c := 3 * g / (4 * Real.pi)))).congr_deriv (by ring)

/-- **Variational principle, y₁-slot.** -/
theorem s10_casimir_y1 (g : ℝ) :
    HasDerivAt (fun w => Hvortex g g g eqX1 w eqX2 eqY2 eqX3 eqY3
      + (3 * g / (4 * Real.pi)) * Ivortex g g g eqX1 w eqX2 eqY2 eqX3 eqY3) 0 eqY1 := by
  have hH := s10_dH_y1 g
  have hI := s10_dI_y1 g
  exact (hH.add (deriv_mul_const_left hI (c := 3 * g / (4 * Real.pi)))).congr_deriv (by ring)

/-- **Variational principle, x₂-slot.** -/
theorem s10_casimir_x2 (g : ℝ) :
    HasDerivAt (fun w => Hvortex g g g eqX1 eqY1 w eqY2 eqX3 eqY3
      + (3 * g / (4 * Real.pi)) * Ivortex g g g eqX1 eqY1 w eqY2 eqX3 eqY3) 0 eqX2 := by
  have hH := s10_dH_x2 g
  have hI := s10_dI_x2 g
  exact (hH.add (deriv_mul_const_left hI (c := 3 * g / (4 * Real.pi)))).congr_deriv (by ring)

/-- **Variational principle, y₂-slot.** -/
theorem s10_casimir_y2 (g : ℝ) :
    HasDerivAt (fun w => Hvortex g g g eqX1 eqY1 eqX2 w eqX3 eqY3
      + (3 * g / (4 * Real.pi)) * Ivortex g g g eqX1 eqY1 eqX2 w eqX3 eqY3) 0 eqY2 := by
  have hH := s10_dH_y2 g
  have hI := s10_dI_y2 g
  exact (hH.add (deriv_mul_const_left hI (c := 3 * g / (4 * Real.pi)))).congr_deriv (by ring)

/-- **Variational principle, x₃-slot.** -/
theorem s10_casimir_x3 (g : ℝ) :
    HasDerivAt (fun w => Hvortex g g g eqX1 eqY1 eqX2 eqY2 w eqY3
      + (3 * g / (4 * Real.pi)) * Ivortex g g g eqX1 eqY1 eqX2 eqY2 w eqY3) 0 eqX3 := by
  have hH := s10_dH_x3 g
  have hI := s10_dI_x3 g
  exact (hH.add (deriv_mul_const_left hI (c := 3 * g / (4 * Real.pi)))).congr_deriv (by ring)

/-- **Variational principle, y₃-slot.** -/
theorem s10_casimir_y3 (g : ℝ) :
    HasDerivAt (fun w => Hvortex g g g eqX1 eqY1 eqX2 eqY2 eqX3 w
      + (3 * g / (4 * Real.pi)) * Ivortex g g g eqX1 eqY1 eqX2 eqY2 eqX3 w) 0 eqY3 := by
  have hH := s10_dH_y3 g
  have hI := s10_dI_y3 g
  exact (hH.add (deriv_mul_const_left hI (c := 3 * g / (4 * Real.pi)))).congr_deriv (by ring)

/-! ### the in-time Lyapunov stability theorem

The annulus in which the coercive inequality holds is propagated along the
whole trajectory by a continuous-induction argument: the deep-interior
target [15/16, 17/16] has a margin of 7/16 on both sides of the annulus
[1/2, 3/2], so no trajectory that starts in the target with a small energy
excess can ever leave the annulus. -/

/-- A squared-deviation bound of (1/16)² pins each squared side inside the
    deep-interior target [15/16, 17/16]. -/
private theorem s10_mem16 {d : ℝ} (h : (d - 1) ^ 2 ≤ (1/16 : ℝ) ^ 2) :
    d ∈ Set.Icc (15/16 : ℝ) (17/16) := by
  rw [Set.mem_Icc]
  constructor
  · rcases lt_or_le d (15/16) with hlt | hle
    · exfalso
      have hid : (d - 1) ^ 2 - (1/16 : ℝ) ^ 2
          = (-(d - 1) - 1/16) * (-(d - 1) + 1/16) := by ring
      have hp : (0:ℝ) < -(d - 1) - 1/16 := by linarith
      have hq : (0:ℝ) < -(d - 1) + 1/16 := by linarith
      have hpr : (0:ℝ) < (-(d - 1) - 1/16) * (-(d - 1) + 1/16) := by nlinarith [hp, hq]
      linarith [hid ▸ hpr, h]
    · linarith
  · rcases lt_or_le (17/16) d with hgt | hle
    · exfalso
      have hid : (d - 1) ^ 2 - (1/16 : ℝ) ^ 2
          = ((d - 1) - 1/16) * ((d - 1) + 1/16) := by ring
      have hp : (0:ℝ) < (d - 1) - 1/16 := by linarith
      have hq : (0:ℝ) < (d - 1) + 1/16 := by linarith
      have hpr : (0:ℝ) < ((d - 1) - 1/16) * ((d - 1) + 1/16) := by nlinarith [hp, hq]
      linarith [hid ▸ hpr, h]
    · linarith

/-- **The annulus propagation (continuous induction).**  If the three
    squared-side functions are continuous, start in the deep-interior
    target at 0, and satisfy the coercive bound whenever they are in the
    annulus, then they stay in the annulus forever (for t ≥ 0). -/
private theorem s10_propagate {dA dB dC : ℝ → ℝ}
    (hcA : Continuous dA) (hcB : Continuous dB) (hcC : Continuous dC)
    (h0 : dA 0 ∈ Set.Icc (15/16 : ℝ) (17/16) ∧ dB 0 ∈ Set.Icc (15/16 : ℝ) (17/16)
      ∧ dC 0 ∈ Set.Icc (15/16 : ℝ) (17/16))
    (hbound : ∀ s : ℝ, dA s ∈ Set.Icc (1/2 : ℝ) (3/2) → dB s ∈ Set.Icc (1/2 : ℝ) (3/2) →
      dC s ∈ Set.Icc (1/2 : ℝ) (3/2) →
      (dA s - 1) ^ 2 + (dB s - 1) ^ 2 + (dC s - 1) ^ 2 ≤ (1/16 : ℝ) ^ 2)
    (t0 : ℝ) (ht0 : 0 ≤ t0) :
    dA t0 ∈ Set.Icc (1/2 : ℝ) (3/2) ∧ dB t0 ∈ Set.Icc (1/2 : ℝ) (3/2)
      ∧ dC t0 ∈ Set.Icc (1/2 : ℝ) (3/2) := by
  set P : Set ℝ := dA ⁻¹' (Set.Icc (1/2 : ℝ) (3/2))
    ∩ (dB ⁻¹' (Set.Icc (1/2 : ℝ) (3/2)) ∩ dC ⁻¹' (Set.Icc (1/2 : ℝ) (3/2))) with hPdef
  have hPcl : IsClosed P := by
    have e1 : IsClosed ((Set.univ : Set ℝ) ∩ dA ⁻¹' (Set.Icc (1/2 : ℝ) (3/2))) :=
      hcA.continuousOn.preimage_isClosed_of_isClosed isClosed_univ isClosed_Icc
    have e2 : IsClosed ((Set.univ : Set ℝ) ∩ dB ⁻¹' (Set.Icc (1/2 : ℝ) (3/2))) :=
      hcB.continuousOn.preimage_isClosed_of_isClosed isClosed_univ isClosed_Icc
    have e3 : IsClosed ((Set.univ : Set ℝ) ∩ dC ⁻¹' (Set.Icc (1/2 : ℝ) (3/2))) :=
      hcC.continuousOn.preimage_isClosed_of_isClosed isClosed_univ isClosed_Icc
    rw [Set.univ_inter] at e1 e2 e3
    exact e1.inter (e2.inter e3)
  have h0P : (0 : ℝ) ∈ P := by
    rcases h0 with ⟨h1, h2, h3⟩
    refine ⟨?_, ?_, ?_⟩
    · exact Set.mem_preimage.mpr (by
        rcases Set.mem_Icc.mp h1 with ⟨m1, m2⟩
        exact Set.mem_Icc.mpr ⟨by linarith, by linarith⟩)
    · exact Set.mem_preimage.mpr (by
        rcases Set.mem_Icc.mp h2 with ⟨m1, m2⟩
        exact Set.mem_Icc.mpr ⟨by linarith, by linarith⟩)
    · exact Set.mem_preimage.mpr (by
        rcases Set.mem_Icc.mp h3 with ⟨m1, m2⟩
        exact Set.mem_Icc.mpr ⟨by linarith, by linarith⟩)
  set E : Set ℝ := {s | 0 ≤ s ∧ s ≤ t0 ∧ ∀ r ∈ Set.Icc (0 : ℝ) s, r ∈ P} with hEdef
  have hE0 : (0 : ℝ) ∈ E := by
    refine ⟨le_refl _, ht0, ?_⟩
    intro r hr
    rcases Set.mem_Icc.mp hr with ⟨m1, m2⟩
    have hr0 : r = 0 := by linarith
    rw [hr0]
    exact h0P
  have hEne : E.Nonempty := ⟨0, hE0⟩
  set T := sSup E with hTdef
  have hTle : T ≤ t0 := Real.sSup_le (fun s hs => hs.2.1) ht0
  have hEbdd : BddAbove E := ⟨t0, fun x hx => hx.2.1⟩
  have hTge : (0 : ℝ) ≤ T := le_csSup hEbdd hE0
  -- approximation: every point of [0, T) lies in P
  have happ : ∀ r : ℝ, 0 ≤ r → r < T → r ∈ P := by
    intro r hr1 hr2
    by_contra hcon
    have hall : ∀ s ∈ E, s ≤ r := by
      intro s hs
      by_contra hgt
      exact hcon (hs.2.2 r ⟨hr1, by linarith⟩)
    have hsup : T ≤ r := Real.sSup_le hall hr1
    linarith
  -- T belongs to P (closedness of P plus the approximation property)
  have hTP : T ∈ P := by
    rw [← hPcl.closure_eq]
    rw [Metric.mem_closure_iff]
    intro ε hε
    rcases le_or_lt ε T with hle | hlt
    · exact ⟨T - ε / 2, happ (T - ε / 2) (by linarith) (by linarith),
        by rw [Real.dist_eq, abs_lt]; constructor <;> linarith⟩
    · exact ⟨0, h0P, by rw [Real.dist_eq, sub_zero, abs_lt]; constructor <;> linarith⟩
  -- the deep-interior margin at T
  have hTPA : dA T ∈ Set.Icc (1/2 : ℝ) (3/2) := Set.mem_preimage.mp hTP.1
  have hTPB : dB T ∈ Set.Icc (1/2 : ℝ) (3/2) := Set.mem_preimage.mp hTP.2.1
  have hTPC : dC T ∈ Set.Icc (1/2 : ℝ) (3/2) := Set.mem_preimage.mp hTP.2.2
  have hsum := hbound T hTPA hTPB hTPC
  have kA : (dA T - 1) ^ 2 ≤ (1/16 : ℝ) ^ 2 := by
    have z2 : 0 ≤ (dB T - 1) ^ 2 := sq_nonneg _
    have z3 : 0 ≤ (dC T - 1) ^ 2 := sq_nonneg _
    linarith
  have kB : (dB T - 1) ^ 2 ≤ (1/16 : ℝ) ^ 2 := by
    have z1 : 0 ≤ (dA T - 1) ^ 2 := sq_nonneg _
    have z3 : 0 ≤ (dC T - 1) ^ 2 := sq_nonneg _
    linarith
  have kC : (dC T - 1) ^ 2 ≤ (1/16 : ℝ) ^ 2 := by
    have z1 : 0 ≤ (dA T - 1) ^ 2 := sq_nonneg _
    have z2 : 0 ≤ (dB T - 1) ^ 2 := sq_nonneg _
    linarith
  rcases Set.mem_Icc.mp (s10_mem16 kA) with ⟨a1, a2⟩
  rcases Set.mem_Icc.mp (s10_mem16 kB) with ⟨b1, b2⟩
  rcases Set.mem_Icc.mp (s10_mem16 kC) with ⟨c1, c2⟩
  rcases lt_or_eq_of_le hTle with hTlt | hTeq
  · -- T < t0: extend beyond T and contradict the supremum
    have oA : IsOpen {s | dA s ∈ Set.Ioo (1/2 : ℝ) (3/2)} :=
      hcA.isOpen_preimage _ isOpen_Ioo
    have oB : IsOpen {s | dB s ∈ Set.Ioo (1/2 : ℝ) (3/2)} :=
      hcB.isOpen_preimage _ isOpen_Ioo
    have oC : IsOpen {s | dC s ∈ Set.Ioo (1/2 : ℝ) (3/2)} :=
      hcC.isOpen_preimage _ isOpen_Ioo
    have mA : T ∈ {s | dA s ∈ Set.Ioo (1/2 : ℝ) (3/2)} :=
      Set.mem_Ioo.mpr ⟨by linarith, by linarith⟩
    have mB : T ∈ {s | dB s ∈ Set.Ioo (1/2 : ℝ) (3/2)} :=
      Set.mem_Ioo.mpr ⟨by linarith, by linarith⟩
    have mC : T ∈ {s | dC s ∈ Set.Ioo (1/2 : ℝ) (3/2)} :=
      Set.mem_Ioo.mpr ⟨by linarith, by linarith⟩
    obtain ⟨εA, hεA⟩ := Metric.isOpen_iff.mp oA T mA
    obtain ⟨εB, hεB⟩ := Metric.isOpen_iff.mp oB T mB
    obtain ⟨εC, hεC⟩ := Metric.isOpen_iff.mp oC T mC
    set δ := min (min εA εB) (min εC (t0 - T)) with hδdef
    have hδA : δ ≤ εA := le_trans (min_le_left _ _) (min_le_left _ _)
    have hδB : δ ≤ εB := le_trans (min_le_left _ _) (min_le_right _ _)
    have hδC : δ ≤ εC := le_trans (min_le_right (min εA εB) _) (min_le_left _ _)
    have hδt : δ ≤ t0 - T := le_trans (min_le_right (min εA εB) _) (min_le_right _ _)
    have hδpos : 0 < δ := by
      have p1 : 0 < εA := hεA.1
      have p2 : 0 < εB := hεB.1
      have p3 : 0 < εC := hεC.1
      have p4 : 0 < t0 - T := by linarith
      rw [hδdef]
      exact lt_min (lt_min p1 p2) (lt_min p3 p4)
    have hTE : T + δ / 2 ∈ E := by
      refine ⟨by linarith, by linarith, ?_⟩
      intro r hr
      rcases Set.mem_Icc.mp hr with ⟨m1, m2⟩
      rcases lt_or_le r T with h1 | h2
      · exact happ r m1 h1
      · rcases lt_or_eq_of_le h2 with h3 | h4
        · -- T < r ≤ T + δ/2: inside all three open preimages
          refine ⟨?_, ?_, ?_⟩
          · have hbA : r ∈ Metric.ball T εA := by
              rw [Metric.mem_ball, Real.dist_eq, abs_lt]
              constructor <;> linarith only [hδA, hδpos, h3, m2, hεA.1]
            have hmem := hεA.right hbA
            exact Set.mem_preimage.mpr (Set.mem_Icc.mpr
              ⟨le_of_lt (Set.mem_Ioo.mp hmem).1, le_of_lt (Set.mem_Ioo.mp hmem).2⟩)
          · have hbB : r ∈ Metric.ball T εB := by
              rw [Metric.mem_ball, Real.dist_eq, abs_lt]
              constructor <;> linarith only [hδB, hδpos, h3, m2, hεB.1]
            have hmem := hεB.right hbB
            exact Set.mem_preimage.mpr (Set.mem_Icc.mpr
              ⟨le_of_lt (Set.mem_Ioo.mp hmem).1, le_of_lt (Set.mem_Ioo.mp hmem).2⟩)
          · have hbC : r ∈ Metric.ball T εC := by
              rw [Metric.mem_ball, Real.dist_eq, abs_lt]
              constructor <;> linarith only [hδC, hδpos, h3, m2, hεC.1]
            have hmem := hεC.right hbC
            exact Set.mem_preimage.mpr (Set.mem_Icc.mpr
              ⟨le_of_lt (Set.mem_Ioo.mp hmem).1, le_of_lt (Set.mem_Ioo.mp hmem).2⟩)
        · rw [← h4]
          exact hTP
    -- contradiction: T + δ/2 > T = sSup E
    have hsup := le_csSup hEbdd hTE
    linarith
  · -- T = t0: t0 itself is in the annulus
    rw [← hTeq]
    exact ⟨Set.mem_preimage.mp hTP.1, Set.mem_preimage.mp hTP.2.1,
      Set.mem_preimage.mp hTP.2.2⟩

/-- **Nonlinear Lyapunov stability of the Lagrange triangle (H/I form).**
    Let a Kirchhoff solution with equal circulations Γ > 0 stay on the
    anchor level set (P = Q = 0, I = Γ at every time) and start with energy
    excess at most (Γ²/(12π))·(1/16)² and all squared sides in the
    deep-interior target [15/16, 17/16].  Then at EVERY time t ∈ ℝ the
    squared shape deviation is controlled by the conserved energy excess:
      Σ_pairs (d2_ij(t) − 1)² ≤ (12π/Γ²) · H(0).
    This is the energy–Casimir Lyapunov theorem: the equilateral triangle
    is nonlinearly stable modulo the symmetries, with the explicit
    Lyapunov inequality as the certificate. -/
theorem s10_lyapunov_stab (g : ℝ) (hg : 0 < g) (sol : KirchhoffSol g g g)
    (hP : ∀ t, Pvortex g g g (sol.x1 t) (sol.x2 t) (sol.x3 t) = 0)
    (hQ : ∀ t, Qvortex g g g (sol.y1 t) (sol.y2 t) (sol.y3 t) = 0)
    (hI : ∀ t, Ivortex g g g (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
      (sol.x3 t) (sol.y3 t) = g)
    (hH : Hvortex g g g (sol.x1 0) (sol.y1 0) (sol.x2 0) (sol.y2 0)
      (sol.x3 0) (sol.y3 0) ≤ (g * g / (12 * Real.pi)) * ((1/16 : ℝ) ^ 2))
    (h0 : d2 (sol.x1 0) (sol.y1 0) (sol.x2 0) (sol.y2 0) ∈ Set.Icc (15/16 : ℝ) (17/16)
      ∧ d2 (sol.x1 0) (sol.y1 0) (sol.x3 0) (sol.y3 0) ∈ Set.Icc (15/16 : ℝ) (17/16)
      ∧ d2 (sol.x2 0) (sol.y2 0) (sol.x3 0) (sol.y3 0) ∈ Set.Icc (15/16 : ℝ) (17/16))
    (t : ℝ) :
    (d2 (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) - 1) ^ 2
      + (d2 (sol.x1 t) (sol.y1 t) (sol.x3 t) (sol.y3 t) - 1) ^ 2
      + (d2 (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t) - 1) ^ 2
      ≤ (12 * Real.pi / (g * g)) * Hvortex g g g (sol.x1 0) (sol.y1 0) (sol.x2 0)
        (sol.y2 0) (sol.x3 0) (sol.y3 0) := by
  set dA : ℝ → ℝ := fun s => d2 (sol.x1 s) (sol.y1 s) (sol.x2 s) (sol.y2 s) with hdAdef
  set dB : ℝ → ℝ := fun s => d2 (sol.x1 s) (sol.y1 s) (sol.x3 s) (sol.y3 s) with hdBdef
  set dC : ℝ → ℝ := fun s => d2 (sol.x2 s) (sol.y2 s) (sol.x3 s) (sol.y3 s) with hdCdef
  -- continuity of the three squared-side functions
  have hc1 : Continuous (fun s => sol.x1 s) :=
    continuous_iff_continuousAt.mpr (fun u => (sol.hx1 u).continuousAt)
  have hc2 : Continuous (fun s => sol.y1 s) :=
    continuous_iff_continuousAt.mpr (fun u => (sol.hy1 u).continuousAt)
  have hc3 : Continuous (fun s => sol.x2 s) :=
    continuous_iff_continuousAt.mpr (fun u => (sol.hx2 u).continuousAt)
  have hc4 : Continuous (fun s => sol.y2 s) :=
    continuous_iff_continuousAt.mpr (fun u => (sol.hy2 u).continuousAt)
  have hc5 : Continuous (fun s => sol.x3 s) :=
    continuous_iff_continuousAt.mpr (fun u => (sol.hx3 u).continuousAt)
  have hc6 : Continuous (fun s => sol.y3 s) :=
    continuous_iff_continuousAt.mpr (fun u => (sol.hy3 u).continuousAt)
  have hcA : Continuous dA := by
    rw [hdAdef]
    show Continuous (fun s => (sol.x1 s - sol.x2 s) ^ 2 + (sol.y1 s - sol.y2 s) ^ 2)
    exact (s10_sq_cont (hc1.sub hc3)).add (s10_sq_cont (hc2.sub hc4))
  have hcB : Continuous dB := by
    rw [hdBdef]
    show Continuous (fun s => (sol.x1 s - sol.x3 s) ^ 2 + (sol.y1 s - sol.y3 s) ^ 2)
    exact (s10_sq_cont (hc1.sub hc5)).add (s10_sq_cont (hc2.sub hc6))
  have hcC : Continuous dC := by
    rw [hdCdef]
    show Continuous (fun s => (sol.x2 s - sol.x3 s) ^ 2 + (sol.y2 s - sol.y3 s) ^ 2)
    exact (s10_sq_cont (hc3.sub hc5)).add (s10_sq_cont (hc4.sub hc6))
  -- the coercive bound on the annulus, with the conserved energy
  have hcons0 : ∀ s : ℝ, Hvortex g g g (sol.x1 s) (sol.y1 s) (sol.x2 s) (sol.y2 s)
      (sol.x3 s) (sol.y3 s) = Hvortex g g g (sol.x1 0) (sol.y1 0) (sol.x2 0) (sol.y2 0)
      (sol.x3 0) (sol.y3 0) := fun s => H_kirchhoff_conserved g g g sol s 0
  have hbound : ∀ s : ℝ, dA s ∈ Set.Icc (1/2 : ℝ) (3/2) → dB s ∈ Set.Icc (1/2 : ℝ) (3/2) →
      dC s ∈ Set.Icc (1/2 : ℝ) (3/2) →
      (dA s - 1) ^ 2 + (dB s - 1) ^ 2 + (dC s - 1) ^ 2 ≤ (1/16 : ℝ) ^ 2 := by
    intro s mA mB mC
    have hcoer := s10_coercive g (sol.x1 s) (sol.y1 s) (sol.x2 s) (sol.y2 s)
      (sol.x3 s) (sol.y3 s) (ne_of_gt hg) (hP s) (hQ s) (hI s)
      mA.1 mA.2 mB.1 mB.2 mC.1 mC.2
    rw [hcons0 s] at hcoer
    have hpos : (0:ℝ) < g * g / (12 * Real.pi) := by positivity
    have h2 : (g * g / (12 * Real.pi)) * ((dA s - 1) ^ 2 + (dB s - 1) ^ 2 + (dC s - 1) ^ 2)
        ≤ (g * g / (12 * Real.pi)) * ((1/16 : ℝ) ^ 2) := le_trans hcoer hH
    exact le_of_mul_le_mul_left h2 hpos
  -- propagate the annulus to all times and conclude
  have hpos : (0:ℝ) < g * g / (12 * Real.pi) := by positivity
  have hgoal : ∀ u : ℝ, dA u ∈ Set.Icc (1/2 : ℝ) (3/2) → dB u ∈ Set.Icc (1/2 : ℝ) (3/2) →
      dC u ∈ Set.Icc (1/2 : ℝ) (3/2) →
      (dA u - 1) ^ 2 + (dB u - 1) ^ 2 + (dC u - 1) ^ 2
        ≤ (12 * Real.pi / (g * g)) * Hvortex g g g (sol.x1 0) (sol.y1 0) (sol.x2 0)
          (sol.y2 0) (sol.x3 0) (sol.y3 0) := by
    intro u mA mB mC
    have hcoer := s10_coercive g (sol.x1 u) (sol.y1 u) (sol.x2 u) (sol.y2 u)
      (sol.x3 u) (sol.y3 u) (ne_of_gt hg) (hP u) (hQ u) (hI u)
      mA.1 mA.2 mB.1 mB.2 mC.1 mC.2
    rw [hcons0 u] at hcoer
    rw [show (12 * Real.pi / (g * g)) * Hvortex g g g (sol.x1 0) (sol.y1 0) (sol.x2 0)
        (sol.y2 0) (sol.x3 0) (sol.y3 0)
        = Hvortex g g g (sol.x1 0) (sol.y1 0) (sol.x2 0) (sol.y2 0) (sol.x3 0) (sol.y3 0)
          / (g * g / (12 * Real.pi)) from by field_simp; ring]
    rw [mul_comm (g * g / (12 * Real.pi))] at hcoer
    exact (le_div_iff hpos).mpr hcoer
  rcases le_or_lt 0 t with htp | htn
  · have h3 := s10_propagate hcA hcB hcC h0 hbound t htp
    exact hgoal t h3.1 h3.2.1 h3.2.2
  · -- t < 0: mirror the trajectory in time
    have hcA' : Continuous (fun s => dA (-s)) := hcA.comp continuous_neg
    have hcB' : Continuous (fun s => dB (-s)) := hcB.comp continuous_neg
    have hcC' : Continuous (fun s => dC (-s)) := hcC.comp continuous_neg
    have h0' : (fun s => dA (-s)) 0 ∈ Set.Icc (15/16 : ℝ) (17/16)
        ∧ (fun s => dB (-s)) 0 ∈ Set.Icc (15/16 : ℝ) (17/16)
        ∧ (fun s => dC (-s)) 0 ∈ Set.Icc (15/16 : ℝ) (17/16) := by
      constructor
      · show dA (-(0:ℝ)) ∈ Set.Icc (15/16 : ℝ) (17/16)
        rw [neg_zero]; exact h0.1
      · constructor
        · show dB (-(0:ℝ)) ∈ Set.Icc (15/16 : ℝ) (17/16)
          rw [neg_zero]; exact h0.2.1
        · show dC (-(0:ℝ)) ∈ Set.Icc (15/16 : ℝ) (17/16)
          rw [neg_zero]; exact h0.2.2
    have hbound' : ∀ s : ℝ, (fun s => dA (-s)) s ∈ Set.Icc (1/2 : ℝ) (3/2) →
        (fun s => dB (-s)) s ∈ Set.Icc (1/2 : ℝ) (3/2) →
        (fun s => dC (-s)) s ∈ Set.Icc (1/2 : ℝ) (3/2) →
        ((fun s => dA (-s)) s - 1) ^ 2 + ((fun s => dB (-s)) s - 1) ^ 2
          + ((fun s => dC (-s)) s - 1) ^ 2 ≤ (1/16 : ℝ) ^ 2 := by
      intro s mA mB mC
      exact hbound (-s) mA mB mC
    have h3 := s10_propagate hcA' hcB' hcC' h0' hbound' (-t) (by linarith)
    have h4 : dA t ∈ Set.Icc (1/2 : ℝ) (3/2) ∧ dB t ∈ Set.Icc (1/2 : ℝ) (3/2)
        ∧ dC t ∈ Set.Icc (1/2 : ℝ) (3/2) := by
      simp only [neg_neg] at h3
      exact h3
    exact hgoal t h4.1 h4.2.1 h4.2.2

/-- **Nonlinear Lyapunov stability, distance form.**  Under the hypotheses
    of `s10_lyapunov_stab`, at every time the three squared distances
    (from the side-1 values) are bounded by the conserved energy excess:
      Σ_pairs (r_ij(t) − 1)² ≤ (12π/Γ²) · H(0). -/
theorem s10_lyapunov_dist (g : ℝ) (hg : 0 < g) (sol : KirchhoffSol g g g)
    (hP : ∀ t, Pvortex g g g (sol.x1 t) (sol.x2 t) (sol.x3 t) = 0)
    (hQ : ∀ t, Qvortex g g g (sol.y1 t) (sol.y2 t) (sol.y3 t) = 0)
    (hI : ∀ t, Ivortex g g g (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
      (sol.x3 t) (sol.y3 t) = g)
    (hH : Hvortex g g g (sol.x1 0) (sol.y1 0) (sol.x2 0) (sol.y2 0)
      (sol.x3 0) (sol.y3 0) ≤ (g * g / (12 * Real.pi)) * ((1/16 : ℝ) ^ 2))
    (h0 : d2 (sol.x1 0) (sol.y1 0) (sol.x2 0) (sol.y2 0) ∈ Set.Icc (15/16 : ℝ) (17/16)
      ∧ d2 (sol.x1 0) (sol.y1 0) (sol.x3 0) (sol.y3 0) ∈ Set.Icc (15/16 : ℝ) (17/16)
      ∧ d2 (sol.x2 0) (sol.y2 0) (sol.x3 0) (sol.y3 0) ∈ Set.Icc (15/16 : ℝ) (17/16))
    (t : ℝ) :
    (vortexDist (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t) - 1) ^ 2
      + (vortexDist (sol.x1 t) (sol.y1 t) (sol.x3 t) (sol.y3 t) - 1) ^ 2
      + (vortexDist (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t) - 1) ^ 2
      ≤ (12 * Real.pi / (g * g)) * Hvortex g g g (sol.x1 0) (sol.y1 0) (sol.x2 0)
        (sol.y2 0) (sol.x3 0) (sol.y3 0) := by
  have h := s10_lyapunov_stab g hg sol hP hQ hI hH h0 t
  have e1 := s10_dist_sq (sol.x1 t) (sol.y1 t) (sol.x2 t) (sol.y2 t)
  have e2 := s10_dist_sq (sol.x1 t) (sol.y1 t) (sol.x3 t) (sol.y3 t)
  have e3 := s10_dist_sq (sol.x2 t) (sol.y2 t) (sol.x3 t) (sol.y3 t)
  linarith

/-!
### 10.2  Collinear central configurations and their bifurcations

For the circulation family Γ = (1, 1, γ) the collinear relative equilibria
centered at the origin are classified exactly.  A triple (x₁, x₂, x₃) on
the x-axis, pairwise distinct, rotates rigidly about the origin with rate
w exactly when the S-conditions hold: S₁ = 2πx₁w, S₂ = 2πx₂w,
S₃ = 2πx₃w with S₁ = 1/(x₁−x₂) + γ/(x₁−x₃), S₂ = 1/(x₂−x₁) +
γ/(x₂−x₃), S₃ = 1/(x₃−x₁) + 1/(x₃−x₂).  With the ratio s = x₃/x₁
(the centering x₂ = −x₁ − γx₃ built in) the condition reduces to the
polynomial N(s, γ) = s(s−1)·M̃(s, γ) = 0 with
M̃(s,γ) = (γ+1)²(γ−1)s² + γ(4γ+5)s + (4γ+5) of discriminant
(4γ+5)(γ+2)².  The symmetric branch s = 0 exists for every γ (rate
ω = (γ+½)/(2πd²), vanishing at γ = −½); the asymmetric branch
bifurcates exactly at the pitchfork γ = −5/4; at γ₀ = −1/4 both
asymmetric solutions are exactly rational (s = 16/9 and s = −16/5),
so the solution count jumps from one to three.
-/

/-- The rotation rate of the symmetric collinear family (d, −d, 0). -/
noncomputable def colOmega (gamma d : ℝ) : ℝ :=
  (1 / 2 + gamma) / (2 * Real.pi * d ^ 2)

/-- The cleared bifurcation polynomial M̃(s, γ). -/
noncomputable def s10ColM (s gamma : ℝ) : ℝ :=
  (gamma + 1) ^ 2 * (gamma - 1) * s ^ 2 + gamma * (4 * gamma + 5) * s + (4 * gamma + 5)

/-- The cleared bifurcation polynomial N(s, γ) = s(s−1)·M̃(s, γ). -/
noncomputable def s10ColN (s gamma : ℝ) : ℝ :=
  s * (s - 1) * s10ColM s gamma

/-- Distance of two rigidly rotated collinear points is the squared
    difference of their abscissas. -/
private theorem s10_rot_d2 (a b w t : ℝ) :
    d2 (a * Real.cos (w * t)) (a * Real.sin (w * t))
      (b * Real.cos (w * t)) (b * Real.sin (w * t)) = (a - b) ^ 2 := by
  unfold d2
  rw [show a * Real.cos (w * t) - b * Real.cos (w * t)
        = (a - b) * Real.cos (w * t) from by ring,
    show a * Real.sin (w * t) - b * Real.sin (w * t)
        = (a - b) * Real.sin (w * t) from by ring,
    show ((a - b) * Real.cos (w * t)) ^ 2
        + ((a - b) * Real.sin (w * t)) ^ 2
        = (a - b) ^ 2 * (Real.sin (w * t) ^ 2 + Real.cos (w * t) ^ 2) from by ring,
    Real.sin_sq_add_cos_sq]
  ring

/-- Rational cancellation on a rotated-collinear pair: the field term
    reduces to the S-sum form. -/
private theorem s10_pair_cancel (p q r v gamma : ℝ) (hq : p - q ≠ 0) (hr : p - r ≠ 0) :
    1 * ((p - q) * v) / ((p - q) ^ 2) + gamma * ((p - r) * v) / ((p - r) ^ 2)
      = v * (1 / (p - q) + gamma / (p - r)) := by
  rw [one_mul, show (p - q) ^ 2 = (p - q) * (p - q) from by ring,
    mul_div_mul_left v (p - q) hq,
    show (p - r) ^ 2 = (p - r) * (p - r) from by ring,
    show gamma * ((p - r) * v) = (p - r) * (gamma * v) from by ring,
    mul_div_mul_left (gamma * v) (p - r) hr]
  ring

/-- Cancellation of the 2π factor in the rigid-rotation identification. -/
private theorem s10_2pi_mul (z : ℝ) : 1 / (2 * Real.pi) * (2 * Real.pi * z) = z := by
  have hpi : (2:ℝ) * Real.pi ≠ 0 := mul_ne_zero two_ne_zero Real.pi_pos.ne'
  field_simp
  ring

/-- Multiplicative self-cancellation. -/
private theorem s10_dinv (d : ℝ) (hd : d ≠ 0) : d * d⁻¹ = 1 := by
  field_simp [hd]

/-- Squared-times-inverse cancellation. -/
private theorem s10_d2inv (d : ℝ) (hd : d ≠ 0) : d ^ 2 * d⁻¹ = d := by
  rw [pow_two]
  rw [mul_assoc d d d⁻¹, s10_dinv d hd]
  ring

/-- The rotation-rate cancellation: 2πd·(q/(2πd²)) = q/d. -/
private theorem s10_rate_cancel (d q : ℝ) (hd : d ≠ 0) :
    2 * Real.pi * d * (q / (2 * Real.pi * d ^ 2)) = q / d := by
  have hpi : (2:ℝ) * Real.pi ≠ 0 := mul_ne_zero two_ne_zero Real.pi_pos.ne'
  field_simp [hpi]
  ring
private theorem s10_neg_ne {a b : ℝ} (h : a - b ≠ 0) : b - a ≠ 0 := by
  intro h0
  apply h
  linarith

/-- The x-velocity component of vortex 1 at the rotated
    collinear configuration. -/
private theorem s10_cfx1 (gamma x1 x2 x3 w t : ℝ)
    (e12 : x1 - x2 ≠ 0) (e13 : x1 - x3 ≠ 0)
    (h1 : 1 / (x1 - x2) + gamma / (x1 - x3) = 2 * Real.pi * x1 * w) :
    kx1 1 1 gamma (x1 * Real.cos (w * t)) (x1 * Real.sin (w * t))
      (x2 * Real.cos (w * t)) (x2 * Real.sin (w * t))
      (x3 * Real.cos (w * t)) (x3 * Real.sin (w * t))
      = -w * (x1 * Real.sin (w * t)) := by
  simp only [kx1]
  rw [s10_rot_d2 x1 x2 w t, s10_rot_d2 x1 x3 w t,
    show x1 * Real.sin (w * t) - x2 * Real.sin (w * t) = (x1 - x2) * Real.sin (w * t) from by ring,
    show x1 * Real.sin (w * t) - x3 * Real.sin (w * t) = (x1 - x3) * Real.sin (w * t) from by ring,
show 1 * ((x1 - x2) * Real.sin (w * t)) / ((x1 - x2) ^ 2)
        + gamma * ((x1 - x3) * Real.sin (w * t)) / ((x1 - x3) ^ 2)
        = Real.sin (w * t) * (1 / (x1 - x2) + gamma / (x1 - x3)) from
      s10_pair_cancel x1 x2 x3 (Real.sin (w * t)) gamma e12 e13,
    h1]
  rw [show Real.sin (w * t) * (2 * Real.pi * x1 * w) = 2 * Real.pi * (Real.sin (w * t) * x1 * w) from by ring]
  linarith [s10_2pi_mul (Real.sin (w * t) * x1 * w)]

/-- The y-velocity component of vortex 1 at the rotated
    collinear configuration. -/
private theorem s10_cfy1 (gamma x1 x2 x3 w t : ℝ)
    (e12 : x1 - x2 ≠ 0) (e13 : x1 - x3 ≠ 0)
    (h1 : 1 / (x1 - x2) + gamma / (x1 - x3) = 2 * Real.pi * x1 * w) :
    ky1 1 1 gamma (x1 * Real.cos (w * t)) (x1 * Real.sin (w * t))
      (x2 * Real.cos (w * t)) (x2 * Real.sin (w * t))
      (x3 * Real.cos (w * t)) (x3 * Real.sin (w * t))
      = w * (x1 * Real.cos (w * t)) := by
  simp only [ky1]
  rw [s10_rot_d2 x1 x2 w t, s10_rot_d2 x1 x3 w t,
    show x1 * Real.cos (w * t) - x2 * Real.cos (w * t) = (x1 - x2) * Real.cos (w * t) from by ring,
    show x1 * Real.cos (w * t) - x3 * Real.cos (w * t) = (x1 - x3) * Real.cos (w * t) from by ring,
show 1 * ((x1 - x2) * Real.cos (w * t)) / ((x1 - x2) ^ 2)
        + gamma * ((x1 - x3) * Real.cos (w * t)) / ((x1 - x3) ^ 2)
        = Real.cos (w * t) * (1 / (x1 - x2) + gamma / (x1 - x3)) from
      s10_pair_cancel x1 x2 x3 (Real.cos (w * t)) gamma e12 e13,
    h1]
  rw [show Real.cos (w * t) * (2 * Real.pi * x1 * w) = 2 * Real.pi * (Real.cos (w * t) * x1 * w) from by ring]
  linarith [s10_2pi_mul (Real.cos (w * t) * x1 * w)]

/-- The x-velocity component of vortex 2 at the rotated
    collinear configuration. -/
private theorem s10_cfx2 (gamma x1 x2 x3 w t : ℝ)
    (e12 : x2 - x1 ≠ 0) (e23 : x2 - x3 ≠ 0)
    (h2 : 1 / (x2 - x1) + gamma / (x2 - x3) = 2 * Real.pi * x2 * w) :
    kx2 1 1 gamma (x1 * Real.cos (w * t)) (x1 * Real.sin (w * t))
      (x2 * Real.cos (w * t)) (x2 * Real.sin (w * t))
      (x3 * Real.cos (w * t)) (x3 * Real.sin (w * t))
      = -w * (x2 * Real.sin (w * t)) := by
  simp only [kx2]
  rw [s10_rot_d2 x1 x2 w t, s10_rot_d2 x2 x3 w t,
    show x2 * Real.sin (w * t) - x1 * Real.sin (w * t) = (x2 - x1) * Real.sin (w * t) from by ring,
    show x2 * Real.sin (w * t) - x3 * Real.sin (w * t) = (x2 - x3) * Real.sin (w * t) from by ring,
show 1 * ((x2 - x1) * Real.sin (w * t)) / ((x1 - x2) ^ 2)
        + gamma * ((x2 - x3) * Real.sin (w * t)) / ((x2 - x3) ^ 2)
        = Real.sin (w * t) * (1 / (x2 - x1) + gamma / (x2 - x3)) from by
      rw [show (x1 - x2) ^ 2 = (x2 - x1) ^ 2 from by ring,
    ]
      exact s10_pair_cancel x2 x1 x3 (Real.sin (w * t)) gamma e12 e23,
    h2]
  rw [show Real.sin (w * t) * (2 * Real.pi * x2 * w) = 2 * Real.pi * (Real.sin (w * t) * x2 * w) from by ring]
  linarith [s10_2pi_mul (Real.sin (w * t) * x2 * w)]

/-- The y-velocity component of vortex 2 at the rotated
    collinear configuration. -/
private theorem s10_cfy2 (gamma x1 x2 x3 w t : ℝ)
    (e12 : x2 - x1 ≠ 0) (e23 : x2 - x3 ≠ 0)
    (h2 : 1 / (x2 - x1) + gamma / (x2 - x3) = 2 * Real.pi * x2 * w) :
    ky2 1 1 gamma (x1 * Real.cos (w * t)) (x1 * Real.sin (w * t))
      (x2 * Real.cos (w * t)) (x2 * Real.sin (w * t))
      (x3 * Real.cos (w * t)) (x3 * Real.sin (w * t))
      = w * (x2 * Real.cos (w * t)) := by
  simp only [ky2]
  rw [s10_rot_d2 x1 x2 w t, s10_rot_d2 x2 x3 w t,
    show x2 * Real.cos (w * t) - x1 * Real.cos (w * t) = (x2 - x1) * Real.cos (w * t) from by ring,
    show x2 * Real.cos (w * t) - x3 * Real.cos (w * t) = (x2 - x3) * Real.cos (w * t) from by ring,
show 1 * ((x2 - x1) * Real.cos (w * t)) / ((x1 - x2) ^ 2)
        + gamma * ((x2 - x3) * Real.cos (w * t)) / ((x2 - x3) ^ 2)
        = Real.cos (w * t) * (1 / (x2 - x1) + gamma / (x2 - x3)) from by
      rw [show (x1 - x2) ^ 2 = (x2 - x1) ^ 2 from by ring,
    ]
      exact s10_pair_cancel x2 x1 x3 (Real.cos (w * t)) gamma e12 e23,
    h2]
  rw [show Real.cos (w * t) * (2 * Real.pi * x2 * w) = 2 * Real.pi * (Real.cos (w * t) * x2 * w) from by ring]
  linarith [s10_2pi_mul (Real.cos (w * t) * x2 * w)]

/-- The x-velocity component of vortex 3 at the rotated
    collinear configuration. -/
private theorem s10_cfx3 (gamma x1 x2 x3 w t : ℝ)
    (e13 : x3 - x1 ≠ 0) (e23 : x3 - x2 ≠ 0)
    (h3 : 1 / (x3 - x1) + 1 / (x3 - x2) = 2 * Real.pi * x3 * w) :
    kx3 1 1 gamma (x1 * Real.cos (w * t)) (x1 * Real.sin (w * t))
      (x2 * Real.cos (w * t)) (x2 * Real.sin (w * t))
      (x3 * Real.cos (w * t)) (x3 * Real.sin (w * t))
      = -w * (x3 * Real.sin (w * t)) := by
  simp only [kx3]
  rw [s10_rot_d2 x1 x3 w t, s10_rot_d2 x2 x3 w t,
    show x3 * Real.sin (w * t) - x1 * Real.sin (w * t) = (x3 - x1) * Real.sin (w * t) from by ring,
    show x3 * Real.sin (w * t) - x2 * Real.sin (w * t) = (x3 - x2) * Real.sin (w * t) from by ring,
show 1 * ((x3 - x1) * Real.sin (w * t)) / ((x1 - x3) ^ 2)
        + 1 * ((x3 - x2) * Real.sin (w * t)) / ((x2 - x3) ^ 2)
        = Real.sin (w * t) * (1 / (x3 - x1) + 1 / (x3 - x2)) from by
      rw [show (x1 - x3) ^ 2 = (x3 - x1) ^ 2 from by ring,
    show (x2 - x3) ^ 2 = (x3 - x2) ^ 2 from by ring,
    ]
      exact s10_pair_cancel x3 x1 x2 (Real.sin (w * t)) (1:ℝ) e13 e23,
    h3]
  rw [show Real.sin (w * t) * (2 * Real.pi * x3 * w) = 2 * Real.pi * (Real.sin (w * t) * x3 * w) from by ring]
  linarith [s10_2pi_mul (Real.sin (w * t) * x3 * w)]

/-- The y-velocity component of vortex 3 at the rotated
    collinear configuration. -/
private theorem s10_cfy3 (gamma x1 x2 x3 w t : ℝ)
    (e13 : x3 - x1 ≠ 0) (e23 : x3 - x2 ≠ 0)
    (h3 : 1 / (x3 - x1) + 1 / (x3 - x2) = 2 * Real.pi * x3 * w) :
    ky3 1 1 gamma (x1 * Real.cos (w * t)) (x1 * Real.sin (w * t))
      (x2 * Real.cos (w * t)) (x2 * Real.sin (w * t))
      (x3 * Real.cos (w * t)) (x3 * Real.sin (w * t))
      = w * (x3 * Real.cos (w * t)) := by
  simp only [ky3]
  rw [s10_rot_d2 x1 x3 w t, s10_rot_d2 x2 x3 w t,
    show x3 * Real.cos (w * t) - x1 * Real.cos (w * t) = (x3 - x1) * Real.cos (w * t) from by ring,
    show x3 * Real.cos (w * t) - x2 * Real.cos (w * t) = (x3 - x2) * Real.cos (w * t) from by ring,
show 1 * ((x3 - x1) * Real.cos (w * t)) / ((x1 - x3) ^ 2)
        + 1 * ((x3 - x2) * Real.cos (w * t)) / ((x2 - x3) ^ 2)
        = Real.cos (w * t) * (1 / (x3 - x1) + 1 / (x3 - x2)) from by
      rw [show (x1 - x3) ^ 2 = (x3 - x1) ^ 2 from by ring,
    show (x2 - x3) ^ 2 = (x3 - x2) ^ 2 from by ring,
    ]
      exact s10_pair_cancel x3 x1 x2 (Real.cos (w * t)) (1:ℝ) e13 e23,
    h3]
  rw [show Real.cos (w * t) * (2 * Real.pi * x3 * w) = 2 * Real.pi * (Real.cos (w * t) * x3 * w) from by ring]
  linarith [s10_2pi_mul (Real.cos (w * t) * x3 * w)]


/-- **The general collinear rotating relative equilibrium.**  Three
    vortices with circulations (1, 1, γ) at the collinear positions
    (x₁, x₂, x₃), pairwise distinct, rotate rigidly about the origin with
    rate w exactly when the three S-conditions hold. -/
theorem s10_col_sol_gen (gamma x1 x2 x3 w : ℝ)
    (e12 : x1 - x2 ≠ 0) (e13 : x1 - x3 ≠ 0) (e23 : x2 - x3 ≠ 0)
    (h1 : 1 / (x1 - x2) + gamma / (x1 - x3) = 2 * Real.pi * x1 * w)
    (h2 : 1 / (x2 - x1) + gamma / (x2 - x3) = 2 * Real.pi * x2 * w)
    (h3 : 1 / (x3 - x1) + 1 / (x3 - x2) = 2 * Real.pi * x3 * w) :
    KirchhoffSol 1 1 gamma where
  x1 := fun t => x1 * Real.cos (w * t)
  y1 := fun t => x1 * Real.sin (w * t)
  x2 := fun t => x2 * Real.cos (w * t)
  y2 := fun t => x2 * Real.sin (w * t)
  x3 := fun t => x3 * Real.cos (w * t)
  y3 := fun t => x3 * Real.sin (w * t)
  hd12 := fun t => by
    rw [s10_rot_d2 x1 x2 w t]
    exact pow_ne_zero 2 e12
  hd13 := fun t => by
    rw [s10_rot_d2 x1 x3 w t]
    exact pow_ne_zero 2 e13
  hd23 := fun t => by
    rw [s10_rot_d2 x2 x3 w t]
    exact pow_ne_zero 2 e23
  hx1 := fun t => by
    rw [s10_cfx1 gamma x1 x2 x3 w t e12 e13 h1]
    exact (deriv_mul_const_left (cos_comp w t) (c := x1)).congr_deriv (by ring)
  hy1 := fun t => by
    rw [s10_cfy1 gamma x1 x2 x3 w t e12 e13 h1]
    exact (deriv_mul_const_left (sin_comp w t) (c := x1)).congr_deriv (by ring)
  hx2 := fun t => by
    rw [s10_cfx2 gamma x1 x2 x3 w t (s10_neg_ne e12) e23 h2]
    exact (deriv_mul_const_left (cos_comp w t) (c := x2)).congr_deriv (by ring)
  hy2 := fun t => by
    rw [s10_cfy2 gamma x1 x2 x3 w t (s10_neg_ne e12) e23 h2]
    exact (deriv_mul_const_left (sin_comp w t) (c := x2)).congr_deriv (by ring)
  hx3 := fun t => by
    rw [s10_cfx3 gamma x1 x2 x3 w t (s10_neg_ne e13) (s10_neg_ne e23) h3]
    exact (deriv_mul_const_left (cos_comp w t) (c := x3)).congr_deriv (by ring)
  hy3 := fun t => by
    rw [s10_cfy3 gamma x1 x2 x3 w t (s10_neg_ne e13) (s10_neg_ne e23) h3]
    exact (deriv_mul_const_left (sin_comp w t) (c := x3)).congr_deriv (by ring)

/-- **The symmetric collinear family** (d, −d, 0) with circulations
    (1, 1, γ) is a rotating relative equilibrium for EVERY γ and every
    d ≠ 0, with rotation rate ω = (γ+½)/(2πd²) — the centering and the
    S-conditions hold by the exact cancellation at the midpoint. -/
theorem s10_col_sym (gamma d : ℝ) (hd : d ≠ 0) :
    KirchhoffSol 1 1 gamma := by
  have he12 : d - (-d) ≠ 0 := by
    rcases lt_or_gt_of_ne hd with h | h <;> linarith
  have he13 : d - 0 ≠ 0 := by
    rcases lt_or_gt_of_ne hd with h | h <;> linarith
  have he23 : (-d) - 0 ≠ 0 := by
    rcases lt_or_gt_of_ne hd with h | h <;> linarith
  have h2pi : (2:ℝ) * Real.pi ≠ 0 := mul_ne_zero two_ne_zero Real.pi_pos.ne'
  have hw : 2 * Real.pi * d * (colOmega gamma d) = (1 / 2 + gamma) / d := by
    unfold colOmega
    exact s10_rate_cancel d (1 / 2 + gamma) hd
  have h1 : 1 / (d - (-d)) + gamma / (d - 0)
      = 2 * Real.pi * d * (colOmega gamma d) := by
    rw [show d - (-d) = 2 * d from by ring, show d - 0 = d from by ring, hw,
      show (1:ℝ) / (2 * d) = 1 / 2 / d from by field_simp [hd, h2pi], add_div]
  have h2 : 1 / ((-d) - d) + gamma / ((-d) - 0)
      = 2 * Real.pi * (-d) * (colOmega gamma d) := by
    rw [show 2 * Real.pi * (-d) * (colOmega gamma d)
        = -(2 * Real.pi * d * (colOmega gamma d)) from by ring, hw,
      show (1:ℝ) / ((-d) - d) = -((1: ℝ) / (2 * d)) from by
        rw [show (-d) - d = -(2 * d) from by ring, div_neg],
      show gamma / ((-d) - 0) = -(gamma / d) from by
        rw [show (-d) - 0 = -d from by ring, div_neg]]
    rw [show -((1: ℝ) / (2 * d)) + -(gamma / d)
        = -((1 / 2 + gamma) / d) from by
      rw [show (1:ℝ) / (2 * d) = 1 / 2 / d from by field_simp [hd, h2pi],
        ← neg_add, ← add_div]]
  have h3 : 1 / (0 - d) + 1 / (0 - (-d)) = 2 * Real.pi * 0 * (colOmega gamma d) := by
    rw [show 2 * Real.pi * 0 * (colOmega gamma d) = 0 from by ring,
      show (1:ℝ) / (0 - d) = -((1: ℝ) / d) from by
        rw [show 0 - d = -d from by ring, div_neg],
      show 1 / (0 - (-d)) = 1 / d from by
        rw [show 0 - (-d) = d from by ring]]
    linarith
  exact s10_col_sol_gen gamma d (-d) 0 (colOmega gamma d) he12 he13 he23 h1 h2 h3

/-- **The stationary collinear equilibrium.**  At γ = −½ the symmetric
    collinear configuration (d, −d, 0) has rotation rate ω = 0: it is a
    genuine stationary point of the Kirchhoff field (a constant solution
    with xₖ(t) = xₖ cos(0) , yₖ(t) = xₖ sin(0)) — the steady-state
    bifurcation point of the collinear family. -/
theorem s10_col_static (d : ℝ) (hd : d ≠ 0) :
    KirchhoffSol 1 1 (-1 / 2) := by
  have he12 : d - (-d) ≠ 0 := by
    rcases lt_or_gt_of_ne hd with h | h <;> linarith
  have he13 : d - 0 ≠ 0 := by
    rcases lt_or_gt_of_ne hd with h | h <;> linarith
  have he23 : (-d) - 0 ≠ 0 := by
    rcases lt_or_gt_of_ne hd with h | h <;> linarith
  have h1 : 1 / (d - (-d)) + (-1 / 2) / (d - 0) = 2 * Real.pi * d * 0 := by
    rw [show d - (-d) = 2 * d from by ring, show d - 0 = d from by ring,
      show 2 * Real.pi * d * 0 = 0 from by ring]
    field_simp [hd]
  have h2 : 1 / ((-d) - d) + (-1 / 2) / ((-d) - 0) = 2 * Real.pi * (-d) * 0 := by
    rw [show (-d) - d = -(2 * d) from by ring, show (-d) - 0 = -d from by ring,
      show 2 * Real.pi * (-d) * 0 = 0 from by ring]
    field_simp [hd]
  have h3 : 1 / (0 - d) + 1 / (0 - (-d)) = 2 * Real.pi * 0 * 0 := by
    rw [show 0 - d = -d from by ring, show 0 - (-d) = d from by ring,
      show 2 * Real.pi * 0 * 0 = 0 from by ring]
    field_simp [hd]
  exact s10_col_sol_gen (-1 / 2) d (-d) 0 0 he12 he13 he23 h1 h2 h3

/-- **The pitchfork.**  The constant coefficient of the bifurcation
    polynomial vanishes EXACTLY at γ = −5/4: this is where the asymmetric
    collinear branch is born (M̃(0, γ) = 4γ + 5). -/
theorem s10_col_pitchfork (gamma : ℝ) :
    s10ColM 0 gamma = 0 ↔ gamma = -5 / 4 := by
  constructor
  · intro h
    unfold s10ColM at h
    linarith
  · intro h
    unfold s10ColM
    rw [h]
    ring

/-- **The discriminant identity.**  The discriminant of the quadratic
    M̃(s, γ) in s is (4γ+5)(γ+2)² — the complete bifurcation diagram of
    the collinear family: two asymmetric roots exactly when γ > −5/4
    (γ ≠ −2), the double root at the pitchfork γ = −5/4, and the
    degenerate collision root at γ = −2. -/
theorem s10_col_disc (gamma : ℝ) :
    (gamma * (4 * gamma + 5)) ^ 2
      - 4 * ((gamma + 1) ^ 2 * (gamma - 1)) * (4 * gamma + 5)
      = (4 * gamma + 5) * (gamma + 2) ^ 2 := by
  ring

/-- **The asymmetric-branch count at γ₀ = −1/4.**  The chart equation
    N(s, −1/4) = 0 has exactly the roots s = 0, s = 16/9, s = −16/5 and
    s = 1 (the last excluded by distinctness): the symmetric
    configuration plus TWO asymmetric collinear relative equilibria. -/
theorem s10_col_count_quarter (s : ℝ) :
    s10ColN s (-1 / 4) = 0 ↔ s = 0 ∨ s = 16 / 9 ∨ s = -16 / 5 ∨ s = 1 := by
  have hform : ∀ s : ℝ, s10ColN s (-1 / 4)
      = s * (s - 1) * (-(9 * s - 16) * (5 * s + 16) / 64) := by
    intro s
    unfold s10ColN s10ColM
    ring
  constructor
  · intro h
    rw [hform s] at h
    rcases mul_eq_zero.mp h with h1 | h1
    · rcases mul_eq_zero.mp h1 with h2 | h2
      · exact Or.inl (by linarith)
      · exact Or.inr (Or.inr (Or.inr (by linarith)))
    · rw [div_eq_zero_iff] at h1
      rcases h1 with h1 | h1
      · rcases mul_eq_zero.mp h1 with h2 | h2
        · rw [neg_eq_zero] at h2
          exact Or.inr (Or.inl (by linarith))
        · exact Or.inr (Or.inr (Or.inl (by linarith)))
      · exact absurd h1 (by norm_num : ((64:ℝ) ≠ 0))
  · intro h
    rcases h with h | h | h | h
    · rw [hform s, h]
      ring
    · rw [hform s, h]
      ring
    · rw [hform s, h]
      ring
    · rw [hform s, h]
      ring

/-- **No asymmetric branch at equal circulations.**  For Γ = (1, 1, 1) the
    chart equation N(s, 1) = 0 has only the roots s = 0, s = −1 and
    s = 1 — every collinear relative equilibrium has a vortex at the
    midpoint (all roots correspond to symmetric configurations). -/
theorem s10_col_count_eq1 (s : ℝ) :
    s10ColN s 1 = 0 ↔ s = 0 ∨ s = -1 ∨ s = 1 := by
  have hform : ∀ s : ℝ, s10ColN s 1 = 9 * s * (s - 1) * (s + 1) := by
    intro s
    unfold s10ColN s10ColM
    ring
  constructor
  · intro h
    rw [hform s] at h
    rcases mul_eq_zero.mp h with h1 | h1
    · rcases mul_eq_zero.mp h1 with h2 | h2
      · exact Or.inl (by linarith)
      · exact Or.inr (Or.inr (by linarith))
    · exact Or.inr (Or.inl (by linarith))
  · intro h
    rcases h with h | h | h
    · rw [hform s, h]
      ring
    · rw [hform s, h]
      ring
    · rw [hform s, h]
      ring

/-- **The exact asymmetric collinear relative equilibrium** at
    Γ = (1, 1, −1/4): the configuration (1, −5/9, 16/9) — the middle
    vortex is vortex 1 — rotates at ω = 27/(56π).  Together with the
    symmetric branch this realizes the post-bifurcation count of three
    collinear relative equilibria (up to scaling). -/
theorem s10_col_asym :
    KirchhoffSol 1 1 (-1 / 4) := by
  have he12 : (1: ℝ) - (-5: ℝ) / 9 ≠ 0 := by norm_num
  have e13 : (1: ℝ) - (16: ℝ) / 9 ≠ 0 := by norm_num
  have e23 : ((-5: ℝ) / 9) - (16: ℝ) / 9 ≠ 0 := by norm_num
  have h1r : (2:ℝ) * Real.pi * 1 * (27 / 56 / Real.pi) = 27 / 28 := by
    field_simp [Real.pi_pos.ne']
    ring
  have h2r : (2:ℝ) * Real.pi * ((-5:ℝ) / 9) * (27 / 56 / Real.pi) = -15 / 28 := by
    field_simp [Real.pi_pos.ne']
    ring
  have h3r : (2:ℝ) * Real.pi * ((16:ℝ) / 9) * (27 / 56 / Real.pi) = 12 / 7 := by
    field_simp [Real.pi_pos.ne']
    ring
  have h1 : 1 / ((1: ℝ) - (-5: ℝ) / 9) + (-1 / 4) / ((1: ℝ) - (16: ℝ) / 9)
      = 2 * Real.pi * 1 * (27 / 56 / Real.pi) := by
    rw [h1r]
    norm_num
  have h2 : 1 / ((-5: ℝ) / 9 - 1) + (-1 / 4) / ((-5: ℝ) / 9 - (16: ℝ) / 9)
      = 2 * Real.pi * ((-5:ℝ) / 9) * (27 / 56 / Real.pi) := by
    rw [h2r]
    norm_num
  have h3 : 1 / ((16: ℝ) / 9 - 1) + 1 / ((16: ℝ) / 9 - (-5: ℝ) / 9)
      = 2 * Real.pi * ((16:ℝ) / 9) * (27 / 56 / Real.pi) := by
    rw [h3r]
    norm_num
  exact s10_col_sol_gen (-1 / 4) 1 ((-5: ℝ) / 9) ((16: ℝ) / 9) (27 / 56 / Real.pi)
    he12 e13 e23 h1 h2 h3

/-! ### Section 9 axiom footprint -/

#print axioms s9_gen_deriv_x
#print axioms s9_gen_deriv_y
#print axioms s9_gen_dist01
#print axioms s9_gen_dist02
#print axioms s9_gen_dist12
#print axioms s9_gen_centroid_x
#print axioms s9_gen_centroid_y
#print axioms s9_gen_field_x1
#print axioms s9_gen_field_y1
#print axioms s9_gen_field_x2
#print axioms s9_gen_field_y2
#print axioms s9_gen_field_x3
#print axioms s9_gen_field_y3
#print axioms s9_rel_eq
#print axioms s9_omega_scale
#print axioms s9_kx_shift
#print axioms s9_ky_shift
#print axioms s9_kx2_shift
#print axioms s9_ky2_shift
#print axioms s9_kx3_shift
#print axioms s9_ky3_shift
#print axioms s9_sol_shift
#print axioms s9_sol_time
#print axioms s9_trans_dev
#print axioms s9_lin_trans
#print axioms s9_lin_diag
#print axioms s9_lin_kernel
#print axioms s9_lin_chain
#print axioms s9_shape_gen
#print axioms s9_shape4_a
#print axioms s9_shape4_b
#print axioms s9_lin_sol_shape4
#print axioms s9_collision_a
#print axioms s9_collision_b
#print axioms s9_eig_unst
#print axioms s9_exp_comp
#print axioms s9_lin_sol_unst
#print axioms s9_growth_norm

/-! ### Section 10 axiom footprint -/

#print axioms s10_log_bound
#print axioms s10_sumsq
#print axioms s10_sumsq_anchor
#print axioms s10_H_nonneg
#print axioms s10_coercive
#print axioms s10_dist_bound
#print axioms s10_casimir_x1
#print axioms s10_casimir_y1
#print axioms s10_casimir_x2
#print axioms s10_casimir_y2
#print axioms s10_casimir_x3
#print axioms s10_casimir_y3
#print axioms s10_lyapunov_stab
#print axioms s10_lyapunov_dist
#print axioms s10_col_sol_gen
#print axioms s10_col_sym
#print axioms s10_col_static
#print axioms s10_col_asym
#print axioms s10_col_pitchfork
#print axioms s10_col_disc
#print axioms s10_col_count_quarter
#print axioms s10_col_count_eq1

end Trivortex
