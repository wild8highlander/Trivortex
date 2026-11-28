/-
SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
-/

import Mathlib.Analysis.SpecialFunctions.Complex.Log
import Mathlib.Data.Complex.BigOperators
import Mathlib.Tactic

/-!
# TRIVORTEX-N, file 2/5: the side-length law of the regular `N`-gon

Statement (classical metric identity of the regular polygon, e.g. Aref 1979):
in the regular `N`-gon of circumradius `R` the squared chord between vertices
`a` and `b` is `2*R^2*(1 - cos(theta_a - theta_b))` with `theta_k = 2*pi*k/N`;
in particular the side length obeys `a^2 = 2*R^2*(1 - cos(2*pi/N))` (`a = 2*R`
for the pair `N = 2`, `a^2 = 3*R^2` for the triangle `N = 3`), and the forced
rotation rate `omega = G*(N-1)/(4*pi*R^2)` of file 1/5 takes the side-length
form `omega = (N-1)*G*(1 - cos(2*pi/N)) / (2*pi*a^2)`, with rotation period
`T = 8*pi^2*R^2 / ((N-1)*G)`.

Everything here is self-contained: only Mathlib is imported, nothing from the
root module or from the sibling files of the TRIVORTEX-N package. The rate
value is the one *forced* by file 1/5 (`nGonOmega`); this file is its metric
companion: it converts the circumradius form into the side-length form used by
the experimental literature on vortex polygons.

Conventions. A vertex is `nGon R N k = R*exp(2*pi*i*k/N)` for `k : Fin N`
(the root-of-unity shape factor `unity N m = exp(2*pi*i*m/N)` carries the
geometry); the forced rate is `nGonOmega g R N = G*(N-1)/(4*pi*R^2)`.

Road map. Section 1 fixes the definitions. Section 2 develops the minimal
`exp(i*theta)` calculus on the unit circle (norm, conjugate = inverse, real
part, sum with the conjugate) and proves the chord formula. Section 3 derives
the side-length law: the side squared, the non-vanishing of
`1 - cos(2*pi/N)`, the side form of the forced rate, the rotation period, and
the `N = 2` / `N = 3` specializations.
-/

open BigOperators
open scoped ComplexConjugate

namespace TrivortexN.NSide

/-! ### Section 1: Definitions -/

/-- The angular position of vertex `k`: `theta_k = 2*pi*k/N`. -/
noncomputable def nGonAngle (N k : ℕ) : ℝ := 2 * Real.pi * k / N

/-- Vertex `k` of the regular `N`-gon of circumradius `R`: `zeta_k = R*exp(i*theta_k)` with
    `theta_k = 2*pi*k/N`. -/
noncomputable def nGon (R : ℝ) (N : ℕ) (k : Fin N) : ℂ :=
  R * Complex.exp (nGonAngle N (k : ℕ) * Complex.I)

/-- The `N`-th root of unity `exp(2*pi*i*m/N)` — the shape factor of vertex `m` relative to
    vertex `0`. -/
noncomputable def unity (N m : ℕ) : ℂ :=
  Complex.exp (nGonAngle N m * Complex.I)

/-- The forced rotation frequency of the regular `N`-gon: `omega = G*(N-1)/(4*pi*R^2)`
    (the value forced by file 1/5; this file re-expresses it in side-length form). -/
noncomputable def nGonOmega (g R : ℝ) (N : ℕ) : ℝ :=
  g * ((N - 1 : ℕ) : ℝ) / (4 * Real.pi * R ^ 2)

/-! ### Section 2: The `exp(i*theta)` calculus and the chord formula -/

/-- A point `exp(i*theta)` of the unit circle: squared norm `1`. -/
theorem exp_I_normSq (x : ℝ) :
    Complex.normSq (Complex.exp (Complex.ofReal' x * Complex.I)) = 1 := by
  rw [Complex.normSq_apply, Complex.exp_ofReal_mul_I_re, Complex.exp_ofReal_mul_I_im]
  rw [← sq, ← sq, add_comm, Real.sin_sq_add_cos_sq]

/-- Real part of `exp(i*theta)`: the cosine. -/
theorem exp_I_re (x : ℝ) :
    (Complex.exp (Complex.ofReal' x * Complex.I)).re = Real.cos x :=
  Complex.exp_ofReal_mul_I_re x

/-- A point `exp(i*theta)` of the unit circle: the conjugate is the inverse. -/
theorem exp_I_conj_inv (x : ℝ) :
    conj (Complex.exp (Complex.ofReal' x * Complex.I))
      = (Complex.exp (Complex.ofReal' x * Complex.I))⁻¹ := by
  have hu0 : Complex.exp (Complex.ofReal' x * Complex.I) ≠ 0 := Complex.exp_ne_zero _
  have hc : Complex.exp (Complex.ofReal' x * Complex.I)
      * conj (Complex.exp (Complex.ofReal' x * Complex.I)) = 1 := by
    have h := Complex.mul_conj (Complex.exp (Complex.ofReal' x * Complex.I))
    rw [exp_I_normSq, Complex.ofReal_one] at h
    exact h
  have hinv : Complex.exp (Complex.ofReal' x * Complex.I)
      * (Complex.exp (Complex.ofReal' x * Complex.I))⁻¹ = 1 := mul_inv_cancel hu0
  exact mul_left_cancel₀ hu0 (hc.trans hinv.symm)

/-- The conjugate of a unit-circle point `exp(i*theta)` is `exp(-i*theta)`. -/
theorem exp_I_conj (x : ℝ) :
    conj (Complex.exp (Complex.ofReal' x * Complex.I))
      = Complex.exp (Complex.ofReal' (-x) * Complex.I) := by
  rw [exp_I_conj_inv, ← Complex.exp_neg]
  congr 1
  push_cast
  ring

/-- The sum of a unit-circle point and its inverse is twice the cosine:
    `exp(i*x) + exp(-i*x) = 2*cos(x)` — the bridge from complex phases to real
    chord lengths. -/
theorem exp_I_add_inv (x : ℝ) :
    Complex.exp (Complex.ofReal' x * Complex.I)
      + (Complex.exp (Complex.ofReal' x * Complex.I))⁻¹
      = 2 * (Real.cos x : ℂ) := by
  rw [← exp_I_conj_inv, Complex.add_conj, Complex.exp_ofReal_mul_I_re]
  push_cast
  rfl

/-- Every root of unity lies on the unit circle: `|unity N m| = 1`. -/
theorem normSq_unity (N m : ℕ) : Complex.normSq (unity N m) = 1 :=
  exp_I_normSq (nGonAngle N m)

/-- The conjugate of a root of unity is its inverse: `conj(u_m) = u_m^-1`. -/
theorem unity_conj_inv (N m : ℕ) : conj (unity N m) = (unity N m)⁻¹ :=
  exp_I_conj_inv (nGonAngle N m)

/-- Nontriviality: for `1 <= m < N` the root `unity N m` is not `1`. -/
theorem unity_ne_one {N : ℕ} (hN : 0 < N) {m : ℕ} (h1 : 1 ≤ m) (h2 : m < N) :
    unity N m ≠ 1 := by
  intro h
  have hN0 : (0 : ℝ) < N := by exact_mod_cast hN
  have hNne : (N : ℝ) ≠ 0 := hN0.ne.symm
  rw [unity] at h
  rw [Complex.exp_eq_one_iff] at h
  obtain ⟨t, ht⟩ := h
  have hstep : (nGonAngle N m : ℂ) = (((t : ℝ) * (2 * Real.pi) : ℝ) : ℂ) := by
    refine mul_right_cancel₀ Complex.I_ne_zero ?_
    rw [ht]
    push_cast
    ring
  have hθ : nGonAngle N m = (t : ℝ) * (2 * Real.pi) :=
    Complex.ofReal_injective hstep
  unfold nGonAngle at hθ
  have hmn : (m : ℝ) = (t : ℝ) * N := by
    rw [div_eq_iff hNne] at hθ
    have hpi : (2 * Real.pi : ℝ) ≠ 0 := by positivity
    have h2' : (2 * Real.pi) * ((t : ℝ) * N) = ((t : ℝ) * (2 * Real.pi)) * N := by ring
    exact mul_left_cancel₀ hpi (by rw [h2']; exact hθ)
  have htval : (t : ℝ) = (m : ℝ) / N := by
    rw [eq_div_iff hNne]
    linarith
  have htpos : (0 : ℝ) < (t : ℝ) := by
    rw [htval]
    exact div_pos (by exact_mod_cast h1) hN0
  have htpos1 : (t : ℝ) < 1 := by
    rw [htval]
    exact (div_lt_one hN0).mpr (by exact_mod_cast h2)
  have ht1 : 0 < (t : ℤ) := by exact_mod_cast htpos
  have ht2 : (t : ℤ) < 1 := by exact_mod_cast htpos1
  omega

/-- The phase of vertex `a` divided by the phase of vertex `b`: `u_a * u_b^-1` is again a
    unit-circle point, with angle `theta_a - theta_b`. -/
theorem unity_mul_inv_exp (N a b : ℕ) :
    unity N a * (unity N b)⁻¹
      = Complex.exp (Complex.ofReal' (nGonAngle N a - nGonAngle N b) * Complex.I) := by
  rw [← unity_conj_inv N b, unity, unity, exp_I_conj, ← Complex.exp_add]
  congr 1
  push_cast
  ring

/-- A vertex in `(x, y)` form: `zeta_k = R*(cos(theta_k) + sin(theta_k)*i)` — the bridge to
    the planar Kirchhoff convention of the root module. -/
theorem nGon_eq_cos_sin (R : ℝ) (N : ℕ) (k : Fin N) :
    nGon R N k = (R : ℂ) * ((Real.cos (nGonAngle N (k : ℕ)) : ℂ)
      + (Real.sin (nGonAngle N (k : ℕ)) : ℂ) * Complex.I) := by
  rw [nGon, Complex.exp_mul_I, ← Complex.ofReal_cos, ← Complex.ofReal_sin]

/-- Real part of a vertex: `x_k = R*cos(theta_k)`. -/
theorem nGon_re (R : ℝ) (N : ℕ) (k : Fin N) :
    (nGon R N k).re = R * Real.cos (nGonAngle N (k : ℕ)) := by
  rw [nGon_eq_cos_sin]
  simp only [Complex.mul_re, Complex.add_re, Complex.mul_I_re, Complex.I_re,
    Complex.I_im, Complex.ofReal_re, Complex.ofReal_im, mul_zero, add_zero]
  ring

/-- Imaginary part of a vertex: `y_k = R*sin(theta_k)`. -/
theorem nGon_im (R : ℝ) (N : ℕ) (k : Fin N) :
    (nGon R N k).im = R * Real.sin (nGonAngle N (k : ℕ)) := by
  rw [nGon_eq_cos_sin]
  simp only [Complex.mul_im, Complex.add_im, Complex.mul_I_im, Complex.I_re,
    Complex.I_im, Complex.ofReal_re, Complex.ofReal_im, add_zero, mul_zero]
  ring

/-- The squared distance between two unit-circle points, in terms of their relative phases:
    `|u - v|^2 = 2 - (u*v^-1 + v*u^-1)` — the chord identity at unit radius. -/
theorem normSq_sub_unit (u v : ℂ) (hu : u ≠ 0) (hv : v ≠ 0)
    (hu1 : Complex.normSq u = 1) (hv1 : Complex.normSq v = 1) :
    ((Complex.normSq (u - v) : ℝ) : ℂ) = 2 - (u * v⁻¹ + v * u⁻¹) := by
  have hcu : conj u = u⁻¹ := by
    have hc := Complex.mul_conj u
    rw [hu1, Complex.ofReal_one] at hc
    exact mul_left_cancel₀ hu (hc.trans (mul_inv_cancel hu).symm)
  have hcv : conj v = v⁻¹ := by
    have hc := Complex.mul_conj v
    rw [hv1, Complex.ofReal_one] at hc
    exact mul_left_cancel₀ hv (hc.trans (mul_inv_cancel hv).symm)
  rw [← Complex.mul_conj, map_sub, hcu, hcv]
  field_simp [hu, hv]
  ring

/-- The chord formula: the squared distance between vertices `a` and `b` of the regular
    `N`-gon is `2*R^2*(1 - cos(theta_a - theta_b))`. This is the discrete metric heartbeat
    of the polygon family: every distance in the configuration is read off one cosine. -/
theorem chord_sq (R : ℝ) (N : ℕ) (a b : Fin N) :
    Complex.normSq (nGon R N a - nGon R N b)
      = 2 * R ^ 2
        * (1 - Real.cos (nGonAngle N (a : ℕ) - nGonAngle N (b : ℕ))) := by
  have hshift : nGon R N a - nGon R N b
      = (R : ℂ) * (unity N (a : ℕ) - unity N (b : ℕ)) := by
    rw [nGon, nGon, ← unity, ← unity]
    ring
  have hpair : unity N (a : ℕ) * (unity N (b : ℕ))⁻¹
      + unity N (b : ℕ) * (unity N (a : ℕ))⁻¹
      = 2 * (Real.cos (nGonAngle N (a : ℕ) - nGonAngle N (b : ℕ)) : ℂ) := by
    have hcomm : unity N (b : ℕ) * (unity N (a : ℕ))⁻¹
        = conj (unity N (a : ℕ) * (unity N (b : ℕ))⁻¹) := by
      rw [unity_mul_inv_exp N b a, unity_mul_inv_exp N a b, exp_I_conj_inv,
        ← Complex.exp_neg]
      congr 1
      push_cast
      ring
    rw [hcomm, unity_mul_inv_exp N a b, exp_I_conj_inv, exp_I_add_inv]
  have hza : unity N (a : ℕ) ≠ 0 := Complex.exp_ne_zero _
  have hzb : unity N (b : ℕ) ≠ 0 := Complex.exp_ne_zero _
  have hsub := normSq_sub_unit (unity N (a : ℕ)) (unity N (b : ℕ)) hza hzb
    (normSq_unity N a) (normSq_unity N b)
  have hprod : (unity N (a : ℕ) - unity N (b : ℕ))
      * ((unity N (a : ℕ))⁻¹ - (unity N (b : ℕ))⁻¹)
      = 2 - (unity N (a : ℕ) * (unity N (b : ℕ))⁻¹
        + unity N (b : ℕ) * (unity N (a : ℕ))⁻¹) := by
    rw [← hsub, ← Complex.mul_conj, map_sub, unity_conj_inv, unity_conj_inv]
  have hRc : (R : ℂ) * (R : ℂ)
      * ((unity N (a : ℕ) - unity N (b : ℕ))
        * ((unity N (a : ℕ))⁻¹ - (unity N (b : ℕ))⁻¹))
      = ((R : ℂ) * (unity N (a : ℕ) - unity N (b : ℕ)))
        * ((R : ℂ) * ((unity N (a : ℕ))⁻¹ - (unity N (b : ℕ))⁻¹)) := by
    ring
  have hkey : ((Complex.normSq (nGon R N a - nGon R N b) : ℝ) : ℂ)
      = ((2 * R ^ 2
        * (1 - Real.cos (nGonAngle N (a : ℕ) - nGonAngle N (b : ℕ))) : ℝ) : ℂ) := by
    rw [hshift, ← Complex.mul_conj, map_mul, Complex.conj_ofReal, map_sub,
      unity_conj_inv, unity_conj_inv, ← hRc, hprod, hpair]
    push_cast
    ring
  exact Complex.ofReal_injective hkey

/-! ### Section 3: The side-length law -/

/-- The side of the regular `N`-gon: `a^2 = 2*R^2*(1 - cos(2*pi/N))`. For `N = 2` this is
    the diameter of the pair, `a = 2*R`; for `N = 3` it is `a^2 = 3*R^2`, the triangle of
    file 1/5. -/
theorem sideSq (R : ℝ) {N : ℕ} (hN : 2 ≤ N) :
    Complex.normSq (nGon R N ⟨1, by omega⟩ - nGon R N ⟨0, by omega⟩)
      = 2 * R ^ 2 * (1 - Real.cos (2 * Real.pi / N)) := by
  have h := chord_sq R N ⟨1, by omega⟩ ⟨0, by omega⟩
  rw [show Real.cos (nGonAngle N ((⟨1, by omega⟩ : Fin N) : ℕ)
        - nGonAngle N ((⟨0, by omega⟩ : Fin N) : ℕ)) = Real.cos (2 * Real.pi / N) from by
      show Real.cos (nGonAngle N 1 - nGonAngle N 0) = _
      simp [nGonAngle]] at h
  exact h

/-- Twice the factor `1 - cos(2*pi/N)` is the squared distance between the unit-circle
    roots `u_1` and `u_0 = 1`: `2*(1 - cos(2*pi/N)) = |1 - u_1|^2`. -/
theorem two_sub_cos_sq (N : ℕ) (hN : 2 ≤ N) :
    (2 : ℝ) * (1 - Real.cos (2 * Real.pi / N))
      = Complex.normSq (unity N 1 - unity N 0) := by
  have h := chord_sq 1 N ⟨1, by omega⟩ ⟨0, by omega⟩
  rw [show Real.cos (nGonAngle N ((⟨1, by omega⟩ : Fin N) : ℕ)
        - nGonAngle N ((⟨0, by omega⟩ : Fin N) : ℕ)) = Real.cos (2 * Real.pi / N) from by
      show Real.cos (nGonAngle N 1 - nGonAngle N 0) = _
      simp [nGonAngle]] at h
  have h1 : nGon 1 N ⟨1, by omega⟩ = unity N 1 := by
    show (1 : ℂ) * Complex.exp (nGonAngle N 1 * Complex.I) = _
    rw [one_mul, ← unity]
  have h0 : nGon 1 N ⟨0, by omega⟩ = unity N 0 := by
    show (1 : ℂ) * Complex.exp (nGonAngle N 0 * Complex.I) = _
    rw [one_mul, ← unity]
  rw [h1, h0] at h
  norm_num at h
  linarith

/-- The factor `1 - cos(2*pi/N)` never vanishes for `N >= 2` — the side form of the rate
    divides by it. -/
theorem one_sub_cos_ne_zero {N : ℕ} (hN : 2 ≤ N) :
    (1 - Real.cos (2 * Real.pi / N)) ≠ 0 := by
  intro h
  have hsq := two_sub_cos_sq N hN
  rw [h, mul_zero] at hsq
  have hz : Complex.normSq (unity N 1 - unity N 0) = 0 := hsq.symm
  rw [Complex.normSq_eq_zero] at hz
  have hu0 : unity N 0 = 1 := by
    simp [unity, nGonAngle]
  have h1 : unity N 1 ≠ 1 := unity_ne_one (by omega) (by omega) (by omega)
  exact h1 (by rw [sub_eq_zero.mp hz]; exact hu0)

/-- SIDE FORM OF THE FORCED RATE: with `a^2 = 2*R^2*(1 - cos(2*pi/N))` the forced frequency
    of the `N`-gon reads `omega = (N-1)*G*(1 - cos(2*pi/N)) / (2*pi*a^2)` — the form used by
    the experimental literature. -/
theorem nGon_omega_side (g R : ℝ) (hN : 2 ≤ N) :
    nGonOmega g R N
      = ((N - 1 : ℕ) * g) * (1 - Real.cos (2 * Real.pi / N))
        / (2 * Real.pi * (Real.sqrt (2 * R ^ 2 * (1 - Real.cos (2 * Real.pi / N)))) ^ 2) := by
  have hpos : (0 : ℝ) ≤ 2 * R ^ 2 * (1 - Real.cos (2 * Real.pi / N)) :=
    mul_nonneg (mul_nonneg (by norm_num) (sq_nonneg R)) (by
      have hsq := Complex.normSq_nonneg (unity N 1 - unity N 0)
      have hfac := two_sub_cos_sq N hN
      linarith)
  have hsq : (Real.sqrt (2 * R ^ 2 * (1 - Real.cos (2 * Real.pi / N)))) ^ 2
      = 2 * R ^ 2 * (1 - Real.cos (2 * Real.pi / N)) :=
    Real.sq_sqrt hpos
  rcases eq_or_ne R 0 with hR0 | hR0
  · subst hR0
    simp [nGonOmega]
  · have h4 : (4 * Real.pi * R ^ 2 : ℝ) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) Real.pi_pos.ne') (pow_ne_zero 2 hR0)
    have hX : (2 * R ^ 2 * (1 - Real.cos (2 * Real.pi / N)) : ℝ) ≠ 0 := by
      intro hX0
      rcases mul_eq_zero.mp hX0 with h | h
      · rcases mul_eq_zero.mp h with h' | h'
        · norm_num at h'
        · exact hR0 (pow_eq_zero_iff (by norm_num) |>.mp h')
      · exact one_sub_cos_ne_zero hN h
    have hden : (2 * Real.pi * (2 * R ^ 2 * (1 - Real.cos (2 * Real.pi / N))) : ℝ) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) Real.pi_pos.ne') hX
    unfold nGonOmega
    rw [hsq, div_eq_div_iff h4 hden]
    ring

/-- The forced frequency is nonzero for nonzero circulation and `N >= 2` (inherited from
    file 1/5; the companion of the static-case analysis). -/
theorem nGon_omega_ne_zero {g R : ℝ} {N : ℕ} (hg : g ≠ 0) (hR : R ≠ 0) (hN : 2 ≤ N) :
    nGonOmega g R N ≠ 0 := by
  have hN1 : ((N - 1 : ℕ) : ℝ) ≠ 0 := by
    have : (N - 1 : ℕ) ≠ 0 := by omega
    exact Nat.cast_ne_zero.mpr this
  unfold nGonOmega
  intro h
  rw [div_eq_zero_iff] at h
  rcases h with h' | h'
  · rcases mul_eq_zero.mp h' with h'' | h''
    · exact hg h''
    · exact hN1 h''
  · have h2 : (0 : ℝ) < R ^ 2 := by
      rw [pow_two]
      exact mul_self_pos.mpr hR
    have hp : (0 : ℝ) < 4 * Real.pi * R ^ 2 := mul_pos (mul_pos (by norm_num) Real.pi_pos) h2
    linarith

/-- The rotation period: `T = 2*pi/omega = 8*pi^2*R^2 / ((N-1)*G)` — one full turn of every
    vortex of the polygon. -/
theorem nGon_period (g R : ℝ) (hg : g ≠ 0) (hR : R ≠ 0) (hN : 2 ≤ N) :
    2 * Real.pi / nGonOmega g R N
      = 8 * Real.pi ^ 2 * R ^ 2 / ((N - 1 : ℕ) * g) := by
  have hd : (4 * Real.pi * R ^ 2 : ℝ) ≠ 0 := by
    have h2 : R ^ 2 ≠ 0 := pow_ne_zero 2 hR
    exact mul_ne_zero (mul_ne_zero (by norm_num) Real.pi_pos.ne') h2
  have hdg : g * ((N - 1 : ℕ) : ℝ) ≠ 0 := mul_ne_zero hg (Nat.cast_ne_zero.mpr (by omega))
  unfold nGonOmega
  field_simp [hd, hdg]
  ring

/-- The pair `N = 2`: the "side" is the diameter, `a^2 = (2*R)^2 = 4*R^2` — the two vortices
    face each other across the circle. -/
theorem sideSq_two (R : ℝ) :
    Complex.normSq (nGon R 2 ⟨1, by norm_num⟩ - nGon R 2 ⟨0, by norm_num⟩) = 4 * R ^ 2 := by
  have h := chord_sq R 2 ⟨1, by norm_num⟩ ⟨0, by norm_num⟩
  rw [show Real.cos (nGonAngle 2 ((⟨1, by norm_num⟩ : Fin 2) : ℕ)
        - nGonAngle 2 ((⟨0, by norm_num⟩ : Fin 2) : ℕ)) = -1 from by
      have hθ : nGonAngle 2 1 - nGonAngle 2 0 = Real.pi := by
        unfold nGonAngle
        ring
      rw [hθ, Real.cos_pi]] at h
  linarith

/-- The triangle `N = 3`: `a^2 = 3*R^2` — the equilateral triangle of file 1/5. -/
theorem sideSq_three (R : ℝ) :
    Complex.normSq (nGon R 3 ⟨1, by norm_num⟩ - nGon R 3 ⟨0, by norm_num⟩) = 3 * R ^ 2 := by
  have h := chord_sq R 3 ⟨1, by norm_num⟩ ⟨0, by norm_num⟩
  rw [show Real.cos (nGonAngle 3 ((⟨1, by norm_num⟩ : Fin 3) : ℕ)
        - nGonAngle 3 ((⟨0, by norm_num⟩ : Fin 3) : ℕ)) = Real.cos (2 * Real.pi / 3) from by
      have hθ : nGonAngle 3 1 - nGonAngle 3 0 = 2 * Real.pi / 3 := by
        unfold nGonAngle
        ring
      rw [hθ]] at h
  have hcos : Real.cos (2 * Real.pi / 3) = -1 / 2 := by
    have h1 : Real.cos (Real.pi / 3) = 1 / 2 := Real.cos_pi_div_three
    have h2 : Real.cos (2 * (Real.pi / 3)) = 2 * Real.cos (Real.pi / 3) ^ 2 - 1 :=
      Real.cos_two_mul (Real.pi / 3)
    have hπ : (2 : ℝ) * Real.pi / 3 = 2 * (Real.pi / 3) := by ring
    rw [hπ, h2, h1]
    ring
  rw [hcos] at h
  linarith

/-! ### Section 3 axiom footprint -/
#print axioms exp_I_normSq
#print axioms exp_I_re
#print axioms exp_I_conj_inv
#print axioms exp_I_conj
#print axioms exp_I_add_inv
#print axioms normSq_unity
#print axioms unity_conj_inv
#print axioms unity_ne_one
#print axioms unity_mul_inv_exp
#print axioms nGon_eq_cos_sin
#print axioms nGon_re
#print axioms nGon_im
#print axioms normSq_sub_unit
#print axioms chord_sq
#print axioms sideSq
#print axioms two_sub_cos_sq
#print axioms one_sub_cos_ne_zero
#print axioms nGon_omega_side
#print axioms nGon_omega_ne_zero
#print axioms nGon_period
#print axioms sideSq_two
#print axioms sideSq_three

end TrivortexN.NSide
