/-
SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
-/

import Mathlib.Analysis.SpecialFunctions.Complex.Log
import Mathlib.Data.Complex.BigOperators
import Mathlib.Tactic

/-!
# TRIVORTEX-N, file 1/5: the regular `N`-gon of identical point vortices

Statement (classical, e.g. Aref 1979; forced-rotation form of the Kirchhoff
equations): `N` identical point vortices placed at the vertices of a regular
`N`-gon of circumradius `R` rotate rigidly about the centroid with angular
velocity `omega = G*(N-1)/(4*pi*R^2)`, where `G` is the common circulation
(strength) of each vortex.

Everything here is self-contained: only Mathlib is imported, nothing from the
root module `Trivortex.lean`. The file proves the statement *with the value of
the angular velocity forced*: `nGon_omega_forced` says that ANY rigid rotation
frequency `nu` under which the polygon is a steady solution must equal
`nGonOmega g R N`.

Conventions. A vertex configuration is `nGon R N k = R*exp(2*pi*i*k/N)` for
`k : Fin N`. The Kirchhoff velocity field of equal vortices `g` is `field g N w k`
(the `I*(w_k - w_j)/|w_k - w_j|^2` kernel, kernel `ker w = w/|w|^2`); it matches
the `(x, y)`-convention of the root module (bridge lemmas `field_re`, `field_im`).
The reduction to the root-of-unity shape factors uses `unity N m = exp(2*pi*i*m/N)`.

Road map. Section 1 fixes the definitions and the kernel algebra. Section 2
develops the roots of unity and proves the finite sum
`sum_(m≠0) ker(1 - exp(2*pi*i*m/N)) = (N-1)/2` via the pairing identity
`ker(1 - u_m) + ker(1 - u_(N-m)) = 1`. Section 3 assembles the main theorem and
the uniqueness of the angular velocity; the `N = 3` special case reproduces the
equilateral-triangle frequency of the root module in side-length form.
-/

open BigOperators
open scoped ComplexConjugate

namespace TrivortexN.NGon

/-! ### Section 1: Definitions and the velocity kernel -/

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

/-- The point-vortex velocity kernel: `ker w = w/|w|^2` (for `w != 0`). -/
noncomputable def ker (w : ℂ) : ℂ := w / (Complex.normSq w : ℂ)

/-- The Kirchhoff point-vortex field with equal circulations `g` at the vertices of the
    configuration `w : Fin N → ℂ`: the velocity of the `k`-th vortex is `(g/2pi) * sum_(j≠k)
    I*(w_k - w_j)/|w_k - w_j|^2`. -/
noncomputable def field (g : ℝ) (N : ℕ) (w : Fin N → ℂ) (k : Fin N) : ℂ :=
  ((g / (2 * Real.pi) : ℝ) : ℂ) * ∑ j in Finset.univ.erase k,
    Complex.I * ker (w k - w j)

/-- The forced rotation frequency of the regular `N`-gon: `omega = G*(N-1)/(4*pi*R^2)`. -/
noncomputable def nGonOmega (g R : ℝ) (N : ℕ) : ℝ :=
  g * ((N - 1 : ℕ) : ℝ) / (4 * Real.pi * R ^ 2)

/-- Multiplicativity of the kernel: `ker` of a product factors through the normalized first
    factor. -/
theorem ker_mul {a b : ℂ} (ha : (Complex.normSq a : ℂ) ≠ 0) (hb : (Complex.normSq b : ℂ) ≠ 0) :
    ker (a * b) = (a / (Complex.normSq a : ℂ)) * ker b := by
  unfold ker
  rw [Complex.normSq_mul]
  push_cast
  field_simp

/-- Real part of `I*ker z`: the `(x, y)`-bridge for the transverse component. -/
theorem ker_re_I (z : ℂ) : (Complex.I * ker z).re = -z.im / Complex.normSq z := by
  by_cases h : z = 0
  · subst h
    simp [ker]
  · have hq : Complex.normSq z ≠ 0 := fun h0 => h (Complex.normSq_eq_zero.mp h0)
    unfold ker
    rw [mul_comm Complex.I (z / (Complex.normSq z : ℂ)), Complex.mul_I_re, Complex.div_im]
    simp only [Complex.ofReal_re, Complex.ofReal_im, Complex.normSq_ofReal, mul_zero,
      zero_mul, sub_zero]
    field_simp [hq]
    ring

/-- Imaginary part of `I*ker z`: the `(x, y)`-bridge for the radial component. -/
theorem ker_im_I (z : ℂ) : (Complex.I * ker z).im = z.re / Complex.normSq z := by
  by_cases h : z = 0
  · subst h
    simp [ker]
  · have hq : Complex.normSq z ≠ 0 := fun h0 => h (Complex.normSq_eq_zero.mp h0)
    unfold ker
    rw [mul_comm Complex.I (z / (Complex.normSq z : ℂ)), Complex.mul_I_im, Complex.div_re]
    simp only [Complex.ofReal_re, Complex.ofReal_im, Complex.normSq_ofReal, mul_zero,
      zero_mul, sub_zero]
    field_simp [hq]
    ring

/-! ### Section 2: Roots of unity and the finite sum -/

/-- The fundamental identity `exp(2*pi*I) = 1`. -/
theorem exp_two_pi_I :
    Complex.exp (Complex.ofReal' (2 * Real.pi) * Complex.I) = 1 := by
  rw [Complex.exp_mul_I, ← Complex.ofReal_cos, ← Complex.ofReal_sin,
    Real.cos_two_pi, Real.sin_two_pi]
  simp

/-- Every root of unity lies on the unit circle: `|unity N m| = 1`. -/
theorem normSq_unity (N m : ℕ) : Complex.normSq (unity N m) = 1 := by
  rw [unity, Complex.normSq_apply, Complex.exp_ofReal_mul_I_re,
    Complex.exp_ofReal_mul_I_im]
  rw [← sq, ← sq, add_comm, Real.sin_sq_add_cos_sq]

/-- The root of unity only depends on the residue class: `unity N (a % N) = unity N a`. -/
theorem unity_mod {N : ℕ} (hN : 0 < N) (a : ℕ) : unity N (a % N) = unity N a := by
  have hN0 : (0 : ℝ) < N := by exact_mod_cast hN
  have hNne : (N : ℝ) ≠ 0 := hN0.ne.symm
  have hdm := Nat.div_add_mod a N
  have hθ' : nGonAngle N a = (a / N : ℕ) * (2 * Real.pi) + nGonAngle N (a % N) := by
    unfold nGonAngle
    conv_lhs => rw [← hdm]
    push_cast
    rw [mul_add, add_div, mul_div_assoc, mul_comm (↑N) ((a / N : ℕ) : ℝ),
      mul_div_cancel ((a / N : ℕ) : ℝ) hNne, mul_comm (2 * Real.pi) (↑(a / N))]
  rw [unity, unity]
  conv_rhs => rw [hθ', Complex.ofReal_add, add_mul, Complex.exp_add]
  rw [Complex.ofReal_mul, mul_assoc,
    ← show ((a / N : ℕ) : ℂ) = Complex.ofReal' ((a / N : ℕ) : ℝ) from rfl,
    Complex.exp_nat_mul, exp_two_pi_I, one_pow, one_mul]

/-- Equal residues give equal roots of unity. -/
theorem unity_congr {N : ℕ} (hN : 0 < N) {a b : ℕ} (h : a % N = b % N) :
    unity N a = unity N b := by
  rw [← unity_mod hN a, ← unity_mod hN b, h]

/-- The index-`N-m` root is the inverse of the index-`m` root: `unity N (N-m) = (unity N m)^(-1)`
    for `0 < m < N`. -/
theorem unity_inv {N : ℕ} (hN : 0 < N) {m : ℕ} (h2 : m < N) :
    unity N (N - m) = (unity N m)⁻¹ := by
  have hN0 : (0 : ℝ) < N := by exact_mod_cast hN
  have hNne : (N : ℝ) ≠ 0 := hN0.ne.symm
  have hθ : nGonAngle N (N - m) = 2 * Real.pi - nGonAngle N m := by
    unfold nGonAngle
    rw [div_eq_iff hNne, Nat.cast_sub (by omega)]
    field_simp [hNne]
    ring
  rw [unity, unity, hθ]
  conv_lhs => rw [Complex.ofReal_sub, sub_mul, Complex.exp_sub]
  rw [exp_two_pi_I, one_div]

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

/-- Bridge to the `(x, y)`-convention of the root module, real part: the transverse
    component of the Kirchhoff velocity at vertex `k` is `-g/(2pi)` times the sum of
    `(y_k - y_j)/|w_k - w_j|^2` — exactly the `I*(w_k - w_j)/|w_k - w_j|^2` kernel of
    the planar Kirchhoff equations. -/
theorem field_re (g : ℝ) (N : ℕ) (w : Fin N → ℂ) (k : Fin N) :
    (field g N w k).re
      = -(g / (2 * Real.pi)) * ∑ j in Finset.univ.erase k,
          ((w k).im - (w j).im) / Complex.normSq (w k - w j) := by
  rw [field, Complex.re_ofReal_mul, Complex.re_sum, Finset.mul_sum, Finset.mul_sum]
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [ker_re_I, Complex.sub_im, neg_mul, neg_div, mul_neg]

/-- Bridge to the `(x, y)`-convention of the root module, imaginary part: the radial
    component of the Kirchhoff velocity at vertex `k` is `+g/(2pi)` times the sum of
    `(x_k - x_j)/|w_k - w_j|^2`, matching the `(x, y)`-field of the root module. -/
theorem field_im (g : ℝ) (N : ℕ) (w : Fin N → ℂ) (k : Fin N) :
    (field g N w k).im
      = (g / (2 * Real.pi)) * ∑ j in Finset.univ.erase k,
          ((w k).re - (w j).re) / Complex.normSq (w k - w j) := by
  rw [field, Complex.im_ofReal_mul, Complex.im_sum, Finset.mul_sum, Finset.mul_sum]
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [ker_im_I, Complex.sub_re]

/-- The pairing identity: the two conjugate legs of the roots-of-unity sum cancel —
    `ker (1 - u_m) + ker (1 - u_(N-m)) = 1` for `1 <= m < N`, where `u_m = exp(2*pi*i*m/N)`.
    This is the discrete heartbeat of Theorem A: it halves `N-1` summands into `N-1`
    constants and forces the shape-factor sum `sum_(m≠0) 1/(1 - u_m) = (N-1)/2`. -/
theorem ker_pair {N : ℕ} (hN : 0 < N) {m : ℕ} (h1 : 1 ≤ m) (h2 : m < N) :
    ker (1 - unity N m) + ker (1 - unity N (N - m)) = 1 := by
  have hinv : unity N (N - m) = (unity N m)⁻¹ := unity_inv hN h2
  have hu0 : unity N m ≠ 0 := Complex.exp_ne_zero _
  have hu1 : unity N m ≠ 1 := unity_ne_one hN h1 h2
  have hcu : conj (unity N m) = (unity N m)⁻¹ := by
    have hc := Complex.mul_conj (unity N m)
    rw [normSq_unity, Complex.ofReal_one] at hc
    have hc' : conj (unity N m) * (unity N m) = 1 := by
      rw [mul_comm]
      exact hc
    field_simp [hc', hu0]
  have hsub : (1 - (unity N m)⁻¹) = -((1 - unity N m) * (unity N m)⁻¹) := by
    field_simp
  have hq : (Complex.normSq (1 - unity N (N - m)) : ℂ)
      = (Complex.normSq (1 - unity N m) : ℂ) := by
    rw [hinv, hsub, Complex.normSq_neg, Complex.normSq_mul, Complex.normSq_inv]
    rw [normSq_unity, inv_one, mul_one]
  have hu1' : 1 - unity N m ≠ 0 := by
    intro h0
    rw [sub_eq_zero] at h0
    exact hu1 h0.symm
  have h2inv : 1 - (unity N m)⁻¹ ≠ 0 := by
    intro h0
    rw [sub_eq_zero] at h0
    exact hu1 (inv_eq_one.mp h0.symm)
  have hprod : (Complex.normSq (1 - unity N m) : ℂ)
      = (1 - unity N m) * (1 - (unity N m)⁻¹) := by
    have hcc : conj (1 - unity N m) = 1 - (unity N m)⁻¹ := by
      rw [map_sub, map_one, hcu]
    rw [← hcc, Complex.mul_conj]
  have hY : (1 - unity N m) * (1 - (unity N m)⁻¹) ≠ 0 := mul_ne_zero hu1' h2inv
  unfold ker
  rw [hq, hinv, div_add_div_same, hprod, div_eq_one_iff_eq hY,
    mul_sub (1 - unity N m) (1 : ℂ) ((unity N m)⁻¹), mul_one,
    sub_mul (1 : ℂ) (unity N m) ((unity N m)⁻¹), one_mul, mul_inv_cancel hu0]
  ring

/-- The core finite sum — the roots-of-unity shape-factor identity of the `N`-gon:
    `sum_(m≠0) ker (1 - u_m) = (N-1)/2`, i.e. `sum_(m≠0) 1/(1 - exp(2*pi*i*m/N)) = (N-1)/2`.
    Proven by the pairing `ker(1-u_m) + ker(1-u_(N-m)) = 1` over `m = 1..N-1` plus the
    re-index `m ↦ N-m`; this single identity forces the polygon's rotation rate. -/
theorem sum_ker_unity {N : ℕ} (hN : 0 < N) :
    ∑ m in Finset.univ.erase (⟨0, hN⟩ : Fin N), ker (1 - unity N (m : ℕ))
      = (((N - 1 : ℕ) : ℂ) / 2) := by
  have hshift : ∑ m in Finset.univ.erase (⟨0, hN⟩ : Fin N),
      ker (1 - unity N (N - (m : ℕ)))
      = ∑ m in Finset.univ.erase (⟨0, hN⟩ : Fin N), ker (1 - unity N (m : ℕ)) := by
    refine Finset.sum_nbij (fun m : Fin N => ⟨(N - (m : ℕ)) % N, Nat.mod_lt _ hN⟩)
      (fun m hm => ?_) (fun m hm m' hm' h => ?_) (fun m' hm' => ?_)
      (fun m _ => by
        show ker (1 - unity N (N - (m : ℕ))) = ker (1 - unity N ((N - (m : ℕ)) % N))
        rw [unity_mod hN])
    · refine Finset.mem_erase.mpr ⟨?_, Finset.mem_univ _⟩
      have h1 : (m : ℕ) ≠ 0 := by
        intro h0'
        exact (Finset.mem_erase.mp hm).1 (Fin.ext (by simp [h0']))
      have h2 := m.isLt
      intro h0
      rw [Fin.mk.injEq] at h0
      rw [Nat.mod_eq_of_lt (by omega)] at h0
      omega
    · have h1 : (m : ℕ) ≠ 0 := by
        intro h0'
        exact (Finset.mem_erase.mp hm).1 (Fin.ext (by simp [h0']))
      have h3 : (m' : ℕ) ≠ 0 := by
        intro h0'
        exact (Finset.mem_erase.mp hm').1 (Fin.ext (by simp [h0']))
      have h2 := m.isLt
      have h4 := m'.isLt
      rw [Fin.mk.injEq] at h
      have e1 : (N - (m : ℕ)) % N = N - (m : ℕ) := Nat.mod_eq_of_lt (by omega)
      have e2 : (N - (m' : ℕ)) % N = N - (m' : ℕ) := Nat.mod_eq_of_lt (by omega)
      rw [e1, e2] at h
      exact Fin.ext (by omega)
    · have h1 : (m' : ℕ) ≠ 0 := by
        intro h0'
        exact (Finset.mem_erase.mp hm').1 (Fin.ext (by simp [h0']))
      have h2 := m'.isLt
      refine ⟨⟨N - (m' : ℕ), by omega⟩, ?_, ?_⟩
      · refine Finset.mem_erase.mpr ⟨?_, Finset.mem_univ _⟩
        intro h0
        rw [Fin.mk.injEq] at h0
        omega
      · have e1 : (N - (N - (m' : ℕ))) % N = (m' : ℕ) := by
          rw [Nat.mod_eq_of_lt (by omega)]
          omega
        exact Fin.ext e1
  have hpair : ∀ m ∈ Finset.univ.erase (⟨0, hN⟩ : Fin N),
      ker (1 - unity N (m : ℕ)) + ker (1 - unity N (N - (m : ℕ))) = 1 := by
    intro m hm
    have h1 : (m : ℕ) ≠ 0 := by
      intro h0
      exact (Finset.mem_erase.mp hm).1 (Fin.ext (by simp [h0]))
    have h2 := m.isLt
    exact ker_pair hN (by omega) (by omega)
  have hcard : (Finset.univ.erase (⟨0, hN⟩ : Fin N)).card = N - 1 := by
    rw [Finset.card_erase_of_mem (Finset.mem_univ (⟨0, hN⟩ : Fin N)),
      Finset.card_univ, Fintype.card_fin]
  have hadd : ∑ m in Finset.univ.erase (⟨0, hN⟩ : Fin N),
      (ker (1 - unity N (m : ℕ)) + ker (1 - unity N (N - (m : ℕ))))
      = ((N - 1 : ℕ) : ℂ) := by
    rw [Finset.sum_congr rfl (fun m hm => hpair m hm), Finset.sum_const, hcard]
    simp
  have htwo : (∑ m in Finset.univ.erase (⟨0, hN⟩ : Fin N), ker (1 - unity N (m : ℕ))) * 2
      = ((N - 1 : ℕ) : ℂ) := by
    have h := hadd
    rw [Finset.sum_add_distrib, hshift] at h
    rw [mul_two, h]
  rw [eq_div_iff two_ne_zero]
  exact htwo

/-! ### Section 3: The rigidly rotating polygon: main theorem and N = 3 -/

/-- Angle bookkeeping: going `j + N - k` steps around the polygon equals `j` steps minus `k`
    steps plus a full turn. -/
theorem nGonAngle_add {N : ℕ} (hN : 0 < N) (j k : ℕ) (hk : k < N) :
    nGonAngle N k + nGonAngle N (j + N - k) = nGonAngle N j + 2 * Real.pi := by
  have hN0 : (0 : ℝ) < N := by exact_mod_cast hN
  have hNne : (N : ℝ) ≠ 0 := hN0.ne.symm
  have hinner : (k : ℕ) + (j + N - k) = j + N := by omega
  unfold nGonAngle
  refine mul_right_cancel₀ hNne ?_
  rw [add_mul, add_mul, div_mul_cancel _ hNne, div_mul_cancel _ hNne,
    div_mul_cancel _ hNne, ← mul_add, ← mul_add, ← Nat.cast_add, hinner]
  push_cast
  ring

/-- The shifted root `unity N (j + N - k)` factors as `unity N j * (unity N k)^(-1)`. -/
theorem unity_shift {N : ℕ} (hN : 0 < N) (j k : ℕ) (hk : k < N) :
    unity N (j + N - k) = unity N j * (unity N k)⁻¹ := by
  have hθ := nGonAngle_add hN j k hk
  have hθs : nGonAngle N (j + N - k) = nGonAngle N j - nGonAngle N k + 2 * Real.pi := by
    linarith
  rw [unity, unity, unity, hθs]
  conv_lhs => rw [Complex.ofReal_add, Complex.ofReal_sub, add_mul, Complex.exp_add,
    sub_mul, Complex.exp_sub]
  rw [exp_two_pi_I, mul_one, div_eq_mul_inv]

/-- Modular re-indexing, left half: `((j + N - k) % N + k) % N = j` for `j, k < N`. -/
theorem mod_shift_left {N k : ℕ} (hk : k < N) {j : ℕ} (hj : j < N) :
    ((j + N - k) % N + k) % N = j := by
  rw [Nat.mod_add_mod]
  have h2 : j + N - k + k = j + N := by omega
  rw [h2, show (j + N) % N = (j + N * 1) % N by rw [Nat.mul_one],
    Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hj]

/-- Modular re-indexing, right half: `((m + k) % N + N - k) % N = m` for `m, k < N`. -/
theorem mod_shift_right {N k : ℕ} (hN : 0 < N) (hk : k < N) {m : ℕ} (hm : m < N) :
    (((m + k) % N + N - k) % N) = m := by
  rcases lt_or_ge (m + k) N with hlt | hge
  · have hs : (m + k) % N = m + k := Nat.mod_eq_of_lt hlt
    rw [hs, show m + k + N - k = m + N by omega,
      show (m + N) % N = (m + N * 1) % N by rw [Nat.mul_one],
      Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hm]
  · have hlt2 : m + k - N < N := by omega
    have hs : (m + k) % N = m + k - N := by
      conv_lhs => rw [show m + k = m + k - N + N * 1 by omega]
      rw [Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hlt2]
    rw [hs]
    have h4 : m + k - N + N - k = m := by omega
    rw [h4, Nat.mod_eq_of_lt hm]

/-- The re-index `(j + N - k) % N` never lands on `0` when `j != k < N`. -/
theorem mod_shift_ne_zero {N k : ℕ} (hN : 0 < N) (hk : k < N) {j : ℕ} (hj : j < N)
    (hne : (j : ℕ) ≠ k) : (j + N - k) % N ≠ 0 := by
  rcases le_total k j with hle | hlt
  · have hsplit : j + N - k = (j - k) + N := by omega
    rw [hsplit, show ((j - k) + N) % N = ((j - k) + N * 1) % N by rw [Nat.mul_one],
      Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt (by omega)]
    exact ne_of_gt (by omega)
  · have hsplit : j + N - k = N - (k - j) := by omega
    rw [hsplit, Nat.mod_eq_of_lt (by omega)]
    exact ne_of_gt (by omega)

/-- All polygon vertices sit on the circle of radius `R`: `|nGon R N k|^2 = R^2`. -/
theorem normSq_nGon (R : ℝ) (N : ℕ) (k : Fin N) :
    Complex.normSq (nGon R N k) = R ^ 2 := by
  unfold nGon
  rw [Complex.normSq_mul, ← unity, normSq_unity, mul_one, Complex.normSq_ofReal, pow_two]

/-- No vertex coincides with the origin (for `R != 0`). -/
theorem nGon_ne_zero {R : ℝ} {N : ℕ} (hR : R ≠ 0) (k : Fin N) : nGon R N k ≠ 0 := by
  intro h
  have h2 := normSq_nGon R N k
  rw [h, Complex.normSq_zero] at h2
  exact hR (pow_eq_zero_iff (by norm_num) |>.mp h2.symm)

/-- Core reduction: the pairwise kernel sum over the polygon re-indexes to the roots-of-unity
    finite sum, giving `nGon R N k / R^2 * (N-1)/2`. -/
theorem ker_nGon_sum {R : ℝ} {N : ℕ} (hR : R ≠ 0) (k : Fin N) :
    ∑ j in Finset.univ.erase k, ker (nGon R N k - nGon R N j)
      = (nGon R N k / ((R ^ 2 : ℝ) : ℂ)) * (((N - 1 : ℕ) : ℂ) / 2) := by
  have hN : 0 < N := by have := k.isLt; omega
  have hshift : ∀ j : Fin N,
      nGon R N j = nGon R N k * unity N ((j + N - (k : ℕ)) % N) := by
    intro j
    have hu : unity N ((j + N - (k : ℕ)) % N) = unity N (j : ℕ) * (unity N (k : ℕ))⁻¹ := by
      rw [unity_mod hN, unity_shift hN (j : ℕ) (k : ℕ) k.isLt]
    have hnz : unity N (k : ℕ) ≠ 0 := Complex.exp_ne_zero _
    show (R : ℂ) * unity N (j : ℕ) = (R : ℂ) * unity N (k : ℕ) * unity N ((j + N - (k : ℕ)) % N)
    rw [hu]
    have h1 : (R : ℂ) * unity N (k : ℕ) * (unity N (j : ℕ) * (unity N (k : ℕ))⁻¹)
        = (R : ℂ) * unity N (j : ℕ) * (unity N (k : ℕ) * (unity N (k : ℕ))⁻¹) := by ring
    rw [h1, mul_inv_cancel hnz, mul_one]
  have hsummand : ∀ j ∈ Finset.univ.erase k,
      ker (nGon R N k - nGon R N j)
        = (nGon R N k / ((R ^ 2 : ℝ) : ℂ)) * ker (1 - unity N ((j + N - (k : ℕ)) % N)) := by
    intro j hj
    have hne : (j : ℕ) ≠ (k : ℕ) := by
      intro h
      exact (Finset.mem_erase.mp hj).1 (Fin.ext h)
    have hroot : (j + N - (k : ℕ)) % N ≠ 0 :=
      mod_shift_ne_zero hN k.isLt j.isLt hne
    have h1 : 1 ≤ (j + N - (k : ℕ)) % N := Nat.one_le_iff_ne_zero.mpr hroot
    have h2 : (j + N - (k : ℕ)) % N < N := Nat.mod_lt _ hN
    have hfac : nGon R N k - nGon R N k * unity N ((j + N - (k : ℕ)) % N)
        = nGon R N k * (1 - unity N ((j + N - (k : ℕ)) % N)) := by
      rw [mul_sub, mul_one]
    rw [hshift j, hfac, ker_mul]
    · rw [normSq_nGon]
    · intro h0
      rw [Complex.ofReal_eq_zero, Complex.normSq_eq_zero] at h0
      exact nGon_ne_zero hR k h0
    · intro h0
      rw [Complex.ofReal_eq_zero, Complex.normSq_eq_zero, sub_eq_zero] at h0
      exact (unity_ne_one hN h1 h2) h0.symm
  have hreindex : ∑ j in Finset.univ.erase k, ker (1 - unity N ((j + N - (k : ℕ)) % N))
      = ∑ m in Finset.univ.erase (⟨0, hN⟩ : Fin N), ker (1 - unity N (m : ℕ)) := by
    refine Finset.sum_nbij (fun j : Fin N => ⟨(j + N - (k : ℕ)) % N, Nat.mod_lt _ hN⟩)
      (fun j hj => ?_) (fun j _ j' _ h => ?_) (fun m hm => ?_) (fun _ _ => rfl)
    · refine Finset.mem_erase.mpr ⟨?_, Finset.mem_univ _⟩
      have hne : (j : ℕ) ≠ (k : ℕ) := by
        intro h
        exact (Finset.mem_erase.mp hj).1 (Fin.ext h)
      have hroot := mod_shift_ne_zero hN k.isLt j.isLt hne
      intro h0
      rw [Fin.mk.injEq] at h0
      exact hroot h0
    · have h2 := j.isLt
      have h4 := j'.isLt
      have hk := k.isLt
      rw [Fin.mk.injEq] at h
      have h5 : ((j + N - (k : ℕ)) % N + (k : ℕ)) % N
          = ((j' + N - (k : ℕ)) % N + (k : ℕ)) % N := by rw [h]
      rw [mod_shift_left hk h2, mod_shift_left hk h4] at h5
      exact Fin.ext h5
    · refine ⟨⟨(m + (k : ℕ)) % N, Nat.mod_lt _ hN⟩, ?_, ?_⟩
      · refine Finset.mem_erase.mpr ⟨?_, Finset.mem_univ _⟩
        have h2 := m.isLt
        have hk := k.isLt
        have hne0 : (m : ℕ) ≠ 0 := fun h => (Finset.mem_erase.mp hm).1 (Fin.ext h)
        intro h0
        rw [Fin.mk.injEq] at h0
        have h1 := mod_shift_right hN hk h2
        rw [h0, show (k : ℕ) + N - (k : ℕ) = N by omega, Nat.mod_self] at h1
        omega
      · have h2 := m.isLt
        have hk := k.isLt
        exact Fin.ext (mod_shift_right hN hk h2)
  rw [Finset.sum_congr rfl (fun j hj => hsummand j hj), ← Finset.mul_sum, hreindex,
    sum_ker_unity hN]

/-- MAIN THEOREM: the Kirchhoff field at vertex `k` of the regular `N`-gon equals the rigid
    rotation velocity `omega * I * z_k` with `omega = G*(N-1)/(4*pi*R^2)`. -/
theorem nGon_field_eq {R : ℝ} {N : ℕ} (g : ℝ) (hR : R ≠ 0) (k : Fin N) :
    field g N (nGon R N) k
      = ((nGonOmega g R N : ℝ) : ℂ) * Complex.I * nGon R N k := by
  have hC : ((R ^ 2 : ℝ) : ℂ) ≠ 0 := by
    have h2 : R ^ 2 ≠ 0 := pow_ne_zero 2 hR
    exact_mod_cast h2
  rw [field, ← Finset.mul_sum, ker_nGon_sum hR k]
  unfold nGonOmega
  push_cast
  field_simp [hC]
  ring

/-- Uniqueness (forced value): ANY frequency `nu` for which the regular `N`-gon is a steady
    rotating solution must equal `nGonOmega g R N`. -/
theorem nGon_omega_forced {R : ℝ} {N : ℕ} (g : ℝ) (hR : R ≠ 0) (k : Fin N) (ν : ℝ)
    (h : field g N (nGon R N) k = (ν : ℂ) * Complex.I * nGon R N k) :
    ν = nGonOmega g R N := by
  have h1 := nGon_field_eq g hR k
  rw [h1] at h
  have hne : Complex.I * nGon R N k ≠ 0 :=
    mul_ne_zero Complex.I_ne_zero (nGon_ne_zero hR k)
  rw [mul_assoc, mul_assoc] at h
  exact Complex.ofReal_injective (mul_right_cancel₀ hne h).symm

/-- The forced frequency is nonzero for nonzero circulation and `N >= 2`. -/
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

/-- Sign: the polygon rotates counterclockwise iff the circulation `g` is positive (for `R != 0`,
    `N >= 2`). -/
theorem nGon_omega_pos_iff {g R : ℝ} {N : ℕ} (hR : R ≠ 0) (hN : 2 ≤ N) :
    0 < nGonOmega g R N ↔ 0 < g := by
  have h2 : (0 : ℝ) < R ^ 2 := by
    rw [pow_two]
    exact mul_self_pos.mpr hR
  have h3 : (0 : ℝ) < 4 * Real.pi * R ^ 2 := mul_pos (mul_pos (by norm_num) Real.pi_pos) h2
  have hN1 : (0 : ℝ) < ((N - 1 : ℕ) : ℝ) := by
    have : 0 < (N - 1 : ℕ) := by omega
    exact_mod_cast this
  unfold nGonOmega
  constructor
  · intro h
    rcases div_pos_iff.mp h with ⟨h1, -⟩ | ⟨h1, -⟩
    · exact mul_pos_iff_of_pos_right hN1 |>.mp h1
    · exfalso
      have h4 : (4 * Real.pi * R ^ 2 : ℝ) ≠ 0 := h3.ne'
      have h7 : (0 : ℝ) < g * ((N - 1 : ℕ) : ℝ) := by
        have h8 : g * ((N - 1 : ℕ) : ℝ)
            = g * ((N - 1 : ℕ) : ℝ) / (4 * Real.pi * R ^ 2) * (4 * Real.pi * R ^ 2) := by
          rw [div_mul_cancel _ h4]
        rw [h8]
        exact mul_pos h h3
      linarith
  · intro h
    exact div_pos (mul_pos h hN1) h3

/-- The side length of the equilateral triangle: `|z_1 - z_0|^2 = 3*R^2`. -/
theorem nGon_side3_sq (R : ℝ) :
    Complex.normSq (nGon R 3 1 - nGon R 3 0) = 3 * R ^ 2 := by
  have hA : nGonAngle 3 ((1 : Fin 3) : ℕ) = 2 * Real.pi / 3 := by
    unfold nGonAngle
    norm_num
  have hcos : Real.cos (2 * Real.pi / 3) = -1 / 2 := by
    have h1 : Real.cos (Real.pi / 3) = 1 / 2 := Real.cos_pi_div_three
    have h2 : Real.cos (2 * (Real.pi / 3)) = 2 * Real.cos (Real.pi / 3) ^ 2 - 1 :=
      Real.cos_two_mul (Real.pi / 3)
    have hπ : (2 : ℝ) * Real.pi / 3 = 2 * (Real.pi / 3) := by ring
    rw [hπ, h2, h1]
    ring
  have hsin : Real.sin (2 * Real.pi / 3) = Real.sqrt 3 / 2 := by
    have h1 : Real.sin (Real.pi / 3) = Real.sqrt 3 / 2 := Real.sin_pi_div_three
    have h2 : Real.sin (2 * (Real.pi / 3)) = 2 * Real.sin (Real.pi / 3) * Real.cos (Real.pi / 3) :=
      Real.sin_two_mul (Real.pi / 3)
    have hπ : (2 : ℝ) * Real.pi / 3 = 2 * (Real.pi / 3) := by ring
    rw [hπ, h2, h1, Real.cos_pi_div_three]
    ring
  have h0v : nGon R 3 0 = (R : ℂ) := by
    unfold nGon nGonAngle
    simp
  have h1v : nGon R 3 1 = (R : ℂ) * ((Real.cos (2 * Real.pi / 3) : ℂ)
      + (Real.sin (2 * Real.pi / 3) : ℂ) * Complex.I) := by
    rw [nGon, hA, Complex.exp_mul_I, ← Complex.ofReal_cos, ← Complex.ofReal_sin]
  have hre : (nGon R 3 1 - nGon R 3 0).re = -(3 / 2) * R := by
    rw [h1v, h0v]
    simp only [Complex.sub_re, Complex.mul_re, Complex.add_re, Complex.mul_I_re,
      Complex.I_re, Complex.I_im, Complex.ofReal_re, Complex.ofReal_im]
    rw [hcos]
    ring
  have him : (nGon R 3 1 - nGon R 3 0).im = R * Real.sqrt 3 / 2 := by
    rw [h1v, h0v]
    simp only [Complex.sub_im, Complex.mul_im, Complex.add_im, Complex.mul_I_im,
      Complex.add_re, Complex.mul_I_re, Complex.I_re, Complex.I_im,
      Complex.ofReal_re, Complex.ofReal_im]
    rw [hcos, hsin]
    ring
  rw [Complex.normSq_apply, hre, him]
  have hsq : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 3)
  have h9 : (-(3 / 2) * R) ^ 2 = 9 / 4 * R ^ 2 := by
    rw [pow_two]
    ring
  have h3' : (R * Real.sqrt 3 / 2) ^ 2 = R ^ 2 * 3 / 4 := by
    rw [div_pow, mul_pow, hsq]
    norm_num
  rw [← pow_two, ← pow_two, h9, h3']
  ring

/-- `N = 3` bridge: in side-length form `a = sqrt(3)*R` the forced frequency is `3*G/(2*pi*a^2)`. -/
theorem nGon_omega_three (g R : ℝ) :
    nGonOmega g R 3 = 3 * g / (2 * Real.pi * (Real.sqrt 3 * R) ^ 2) := by
  unfold nGonOmega
  have h1 : ((3 - 1 : ℕ) : ℝ) = 2 := by norm_num
  have h2 : (Real.sqrt 3 * R) ^ 2 = 3 * R ^ 2 := by
    rw [mul_pow, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 3)]
  rcases eq_or_ne R 0 with hR0 | hR0
  · subst hR0
    simp
  · rw [h1, h2]
    have h4 : (4 * Real.pi * R ^ 2 : ℝ) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) Real.pi_pos.ne') (pow_ne_zero 2 hR0)
    have h5 : (2 * Real.pi * (3 * R ^ 2) : ℝ) ≠ 0 :=
      mul_ne_zero (mul_ne_zero (by norm_num) Real.pi_pos.ne')
        (mul_ne_zero (by norm_num) (pow_ne_zero 2 hR0))
    rw [div_eq_div_iff h4 h5]
    ring

/-! ### Section 1 axiom footprint -/
#print axioms ker_mul
#print axioms ker_re_I
#print axioms ker_im_I

/-! ### Section 2 axiom footprint -/
#print axioms exp_two_pi_I
#print axioms normSq_unity
#print axioms unity_mod
#print axioms unity_congr
#print axioms unity_inv
#print axioms unity_ne_one
#print axioms field_re
#print axioms field_im
#print axioms ker_pair
#print axioms sum_ker_unity

/-! ### Section 3 axiom footprint -/
#print axioms nGonAngle_add
#print axioms unity_shift
#print axioms mod_shift_left
#print axioms mod_shift_right
#print axioms mod_shift_ne_zero
#print axioms normSq_nGon
#print axioms nGon_ne_zero
#print axioms ker_nGon_sum
#print axioms nGon_field_eq
#print axioms nGon_omega_forced
#print axioms nGon_omega_ne_zero
#print axioms nGon_omega_pos_iff
#print axioms nGon_side3_sq
#print axioms nGon_omega_three

end TrivortexN.NGon
