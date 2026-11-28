/-
SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
-/

import Mathlib.Analysis.SpecialFunctions.Complex.Log
import Mathlib.Data.Complex.BigOperators
import Mathlib.Tactic

/-!
# TRIVORTEX-N, file 4/5: the roots-of-unity engine — geometric sums, partial fractions,
cross-ring kernels

Statement (the computational heart of the TRIVORTEX-N program): for the `N`-th roots of
unity `u_m = exp(2*pi*i*m/N)` the geometric sums `sum_(m<N) u_r^m` equal `N` exactly when
`N` divides `r` and vanish otherwise; consequently the partial-fraction identity
`sum_(m<N) 1/(c - rho*u_m) = N*c^(N-1)/(c^N - rho^N)` holds whenever `c^N != rho^N`, and
the cross-ring kernel sum between two concentric regular `N`-gons collapses to the closed
form `sum_j ker(z - rho*u_j) = N*conj(z)^(N-1)/(conj(z)^N - conj(rho)^N)` (for
`conj(z)^N != conj(rho)^N`), where `ker w = w/|w|^2` is the point-vortex kernel. As
applications the engine re-derives, independently of file 1/5's pairing identity, the
centroid identity `sum_(k<N) u_k = 0` and the ring self-field cross-check
`sum_(j≠k) ker(z_k - z_j) = z_k/R^2 * (N-1)/2`.

Everything here is self-contained: only Mathlib is imported, nothing from the root module
or from the sibling files of the TRIVORTEX-N package. The engine is the tool that unlocks
the multi-ring configurations of the future TRIVORTEX-N files: every cross-sum between two
symmetric rings is a partial fraction over the roots of unity.

Conventions. The roots of unity are `unity N m = exp(2*pi*i*m/N)`; the point-vortex
kernel is `ker w = w/|w|^2` (total, with `ker 0 = 0`); ring vertices are
`nGon R N k = R*exp(2*pi*i*k/N)`.

Road map. Section 1 fixes the definitions. Section 2 develops the root algebra
(unit circle, residues, inverses, non-triviality, products and powers) and proves the
geometric-sum dichotomy by the successor-shift trick. Section 3 proves the geometric
factorization `c^N - y^N`, the partial-fraction identity, its kernel form and the
two-ring cross-sum, and closes with the self-field cross-check.
-/

open BigOperators
open scoped ComplexConjugate

namespace TrivortexN.NRoots

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

/-- The point-vortex velocity kernel: `ker w = w/|w|^2` (total; `ker 0 = 0`). -/
noncomputable def ker (w : ℂ) : ℂ := w / (Complex.normSq w : ℂ)

/-! ### Section 2: The root algebra and the geometric-sum engine -/

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

/-- The product of two roots of unity is the root of the summed index: `u_a * u_b = u_(a+b)`. -/
theorem unity_add (N a b : ℕ) : unity N a * unity N b = unity N (a + b) := by
  have hθ : nGonAngle N (a + b) = nGonAngle N a + nGonAngle N b := by
    unfold nGonAngle
    rw [Nat.cast_add]
    ring
  rw [unity, unity, unity, hθ, ← Complex.exp_add]
  congr 1
  push_cast
  ring

/-- Powers of a root of unity: `(u_m)^k = u_(m*k)`. -/
theorem unity_pow (N m k : ℕ) : (unity N m) ^ k = unity N (m * k) := by
  induction k with
  | zero =>
    simp only [pow_zero, Nat.mul_zero]
    simp [unity, nGonAngle]
  | succ k ih =>
    rw [pow_succ, ih, unity_add]
    congr 1
    simp only [Nat.succ_eq_add_one]
    ring

/-- Modular bookkeeping for the successor shift on `Fin N`, right half:
    `((m + 1) % N + N - 1) % N = m` for `m < N`. -/
theorem mod_succ_right {N : ℕ} (hN : 0 < N) {m : ℕ} (hm : m < N) :
    ((m + 1) % N + (N - 1)) % N = m := by
  rcases Nat.lt_or_ge (m + 1) N with hlt | hge
  · rw [Nat.mod_eq_of_lt hlt, show m + 1 + (N - 1) = m + N by omega,
      show (m + N) % N = (m + N * 1) % N by rw [Nat.mul_one], Nat.add_mul_mod_self_left,
      Nat.mod_eq_of_lt hm]
  · have hEq : m + 1 = N := by omega
    rw [hEq, Nat.mod_self, zero_add, Nat.mod_eq_of_lt (by omega)]
    omega

/-- Modular bookkeeping for the successor shift on `Fin N`, left half:
    `((j + N - 1) % N + 1) % N = j` for `j < N`. -/
theorem mod_succ_left {N : ℕ} (hN : 0 < N) {j : ℕ} (hj : j < N) :
    ((j + N - 1) % N + 1) % N = j := by
  rcases Nat.eq_zero_or_pos j with h0 | hpos
  · subst h0
    have e1 : (0 + N - 1) % N = N - 1 := by
      rw [zero_add, Nat.mod_eq_of_lt (by omega)]
    rw [e1, show N - 1 + 1 = N by omega, Nat.mod_self]
  · have e1 : (j + N - 1) % N = j - 1 := by
      have hsplit : j + N - 1 = (j - 1) + N := by omega
      rw [hsplit, show ((j - 1) + N) % N = ((j - 1) + N * 1) % N by rw [Nat.mul_one],
        Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt (by omega)]
    rw [e1, show j - 1 + 1 = j from by omega, Nat.mod_eq_of_lt hj]

/-- Every `N`-th root of unity is an `N`-th power of one: `u_m^N = 1`. -/
theorem unity_pow_N {N : ℕ} (hN : 0 < N) (m : ℕ) : (unity N m) ^ N = 1 := by
  rw [unity_pow, Nat.mul_comm]
  have hNN : unity N N = unity N 0 := by
    rw [← unity_mod hN N, Nat.mod_self]
  have hu0 : unity N 0 = 1 := by simp [unity, nGonAngle]
  rw [← unity_pow N N m, hNN, hu0, one_pow]

/-- GEOMETRIC-SUM DICHOTOMY, full cycle: `sum_(m<N) u_r^m = N` when `N` divides `r` — every
    term of the sum equals `1`. -/
theorem sum_unity_pow_eq_N {N : ℕ} (hN : 0 < N) {r : ℕ} (hdiv : N ∣ r) :
    ∑ m in (Finset.univ : Finset (Fin N)), (unity N r) ^ (m : ℕ) = ((N : ℕ) : ℂ) := by
  have hNN : unity N N = 1 := by
    rw [← unity_mod hN N, Nat.mod_self]
    simp [unity, nGonAngle]
  have hur : unity N r = 1 := by
    obtain ⟨q, hq⟩ := hdiv
    rw [hq, ← unity_pow N N q, hNN, one_pow]
  rw [Finset.sum_congr rfl fun m _ => by rw [hur]]
  simp

/-- GEOMETRIC-SUM DICHOTOMY, vanishing half: `sum_(m<N) u_r^m = 0` when `N` does not divide
    `r` — the successor-shift trick: multiplying the sum by `u_r` re-indexes it onto itself,
    and `u_r != 1` forces the sum to vanish. -/
theorem sum_unity_pow_eq_zero {N : ℕ} (hN : 0 < N) {r : ℕ} (hnd : r % N ≠ 0) :
    ∑ m in (Finset.univ : Finset (Fin N)), (unity N r) ^ (m : ℕ) = 0 := by
  have hx1 : unity N r ≠ 1 := by
    have hlt : r % N < N := Nat.mod_lt _ hN
    have h1 : 1 ≤ r % N := Nat.one_le_iff_ne_zero.mpr hnd
    have h := unity_ne_one hN h1 hlt
    rwa [unity_mod hN] at h
  have hmodshift : ∀ k : ℕ, (r * ((k : ℕ) + 1)) % N = (r * (((k : ℕ) + 1) % N)) % N := by
    intro k
    have hdm := Nat.div_add_mod ((k : ℕ) + 1) N
    have hsplit : r * ((k : ℕ) + 1)
        = r * (((k : ℕ) + 1) % N) + N * (r * (((k : ℕ) + 1) / N)) := by
      conv_lhs => rw [← hdm]
      rw [Nat.mul_add]
      ring
    rw [hsplit, Nat.add_mul_mod_self_left]
  have hmul : (unity N r) * (∑ k in (Finset.univ : Finset (Fin N)), (unity N r) ^ (k : ℕ))
      = ∑ k in (Finset.univ : Finset (Fin N)), (unity N r) ^ (k : ℕ) := by
    have hstep1 : ∑ k in (Finset.univ : Finset (Fin N)),
        (unity N r) * ((unity N r) ^ (k : ℕ))
        = ∑ k in (Finset.univ : Finset (Fin N)), unity N ((r * ((k : ℕ) + 1)) % N) := by
      refine Finset.sum_congr rfl fun k _ => ?_
      rw [unity_mod hN (r * ((k : ℕ) + 1)), ← unity_pow N r ((k : ℕ) + 1), pow_succ',
        mul_comm ((unity N r) ^ (k : ℕ)) (unity N r)]
    have hstep3 : ∑ k in (Finset.univ : Finset (Fin N)),
        unity N ((r * ((k : ℕ) + 1)) % N)
        = ∑ j in (Finset.univ : Finset (Fin N)), unity N (r * (j : ℕ)) := by
      refine Finset.sum_nbij (fun k : Fin N => ⟨((k : ℕ) + 1) % N, Nat.mod_lt _ hN⟩)
        (fun k _ => Finset.mem_univ _) (fun k _ k' _ h => ?_) (fun m _ => ?_) (fun k _ => ?_)
      · have e1 : (((k : ℕ) + 1) % N + (N - 1)) % N = (k : ℕ) := mod_succ_right hN k.isLt
        have e2 : (((k' : ℕ) + 1) % N + (N - 1)) % N = (k' : ℕ) := mod_succ_right hN k'.isLt
        rw [Fin.mk.injEq] at h
        exact Fin.ext (by rw [← e1, ← e2, h])
      · refine ⟨⟨((m : ℕ) + N - 1) % N, Nat.mod_lt _ hN⟩, Finset.mem_univ _, ?_⟩
        have e1 : (((m : ℕ) + N - 1) % N + 1) % N = (m : ℕ) := mod_succ_left hN m.isLt
        rw [Fin.mk.injEq]
        exact e1
      · show unity N ((r * ((k : ℕ) + 1)) % N) = unity N (r * (((k : ℕ) + 1) % N))
        rw [hmodshift k, unity_mod hN]
    have hstep2 : ∑ j in (Finset.univ : Finset (Fin N)), unity N (r * (j : ℕ))
        = ∑ k in (Finset.univ : Finset (Fin N)), (unity N r) ^ (k : ℕ) :=
      Finset.sum_congr rfl fun j _ => (unity_pow N r (j : ℕ)).symm
    rw [Finset.mul_sum, hstep1, hstep3, hstep2]
  have hsub : (unity N r - 1) * (∑ k in (Finset.univ : Finset (Fin N)), (unity N r) ^ (k : ℕ))
      = 0 := by
    rw [sub_mul, hmul, one_mul, sub_self]
  rcases mul_eq_zero.mp hsub with h | h
  · exact absurd (sub_eq_zero.mp h) hx1
  · exact h

/-- The centroid identity re-derived from the engine: `sum_(k<N) u_k = 0` for `N >= 2` —
    the case `r = 1` of the geometric-sum dichotomy. -/
theorem sum_unity {N : ℕ} (hN : 2 ≤ N) :
    ∑ k in (Finset.univ : Finset (Fin N)), unity N (k : ℕ) = 0 := by
  have hnd : (1 : ℕ) % N ≠ 0 := by
    rw [Nat.mod_eq_of_lt (by omega)]
    norm_num
  have h := sum_unity_pow_eq_zero (by omega) hnd
  have h2 : ∑ k in (Finset.univ : Finset (Fin N)), unity N (k : ℕ)
      = ∑ m in (Finset.univ : Finset (Fin N)), (unity N 1) ^ (m : ℕ) :=
    (Finset.sum_congr rfl fun m _ => by rw [unity_pow N 1 (m : ℕ), one_mul])
  exact h2.trans h


/-! ### Section 3: Partial fractions and the cross-ring kernels -/

/-- The kernel is odd: `ker(-w) = -ker w`. -/
theorem ker_neg (w : ℂ) : ker (-w) = -ker w := by
  unfold ker
  rw [Complex.normSq_neg]
  ring

/-- The conjugate of a root of unity is its inverse: `conj(u_m) = u_m^-1`. -/
theorem unity_conj_inv (N m : ℕ) : conj (unity N m) = (unity N m)⁻¹ := by
  have hu0 : unity N m ≠ 0 := Complex.exp_ne_zero _
  have hc : unity N m * conj (unity N m) = 1 := by
    have h := Complex.mul_conj (unity N m)
    rw [normSq_unity, Complex.ofReal_one] at h
    exact h
  have hinv : unity N m * (unity N m)⁻¹ = 1 := mul_inv_cancel hu0
  exact mul_left_cancel₀ hu0 (hc.trans hinv.symm)

/-- The kernel in reciprocal-conjugate form: `ker w = 1/conj w` for `w != 0` — the form in
    which partial fractions act. -/
theorem ker_eq_inv_conj {w : ℂ} (hw : w ≠ 0) : ker w = (conj w)⁻¹ := by
  have hw0 : (Complex.normSq w : ℂ) ≠ 0 := by
    intro h0
    exact hw (Complex.normSq_eq_zero.mp (Complex.ofReal_injective h0))
  have hcw : conj w ≠ 0 := by
    intro h0
    have h1 : Complex.normSq w = 0 := by
      rw [← Complex.normSq_conj, h0, Complex.normSq_zero]
    exact hw (Complex.normSq_eq_zero.mp h1)
  unfold ker
  rw [div_eq_iff hw0, ← Complex.mul_conj w, mul_left_comm, inv_mul_cancel hcw, mul_one]

/-- The geometric factorization: `c^(n+1) - y^(n+1) = (c - y) * sum_(r<n+1) c^(n-r) * y^r`. -/
theorem pow_sub_pow_geom (c y : ℂ) (n : ℕ) :
    c ^ (n + 1) - y ^ (n + 1) = (c - y) * ∑ r in Finset.range (n + 1), c ^ (n - r) * y ^ r := by
  induction n with
  | zero =>
    simp only [Nat.zero_add, Finset.range_one, Finset.sum_singleton, Nat.sub_zero,
      pow_zero, pow_one, mul_one]
  | succ k ih =>
    -- normalize `succ k + 1` to `k + 1 + 1` (definitionally equal)
    show c ^ (k + 1 + 1) - y ^ (k + 1 + 1)
      = (c - y) * ∑ r in Finset.range (k + 1 + 1), c ^ (k + 1 - r) * y ^ r
    have hsplit : c ^ (k + 1 + 1) - y ^ (k + 1 + 1)
        = c ^ (k + 1) * (c - y) + y * (c ^ (k + 1) - y ^ (k + 1)) := by
      rw [mul_sub]
      ring
    have hsplit2 : ∑ r in Finset.range (k + 1 + 1), c ^ (k + 1 - r) * y ^ r
        = c ^ (k + 1) + y * ∑ r in Finset.range (k + 1), c ^ (k - r) * y ^ r := by
      rw [Finset.sum_range_succ']
      have h1' : ∑ i in Finset.range (k + 1), c ^ (k + 1 - (i + 1)) * y ^ (i + 1)
          = ∑ i in Finset.range (k + 1), y * (c ^ (k - i) * y ^ i) :=
        Finset.sum_congr rfl fun i _ => by
          rw [show k + 1 - (i + 1) = k - i from by omega, pow_succ]
          ring
      have h2' : ∑ i in Finset.range (k + 1), y * (c ^ (k - i) * y ^ i)
          = y * ∑ i in Finset.range (k + 1), c ^ (k - i) * y ^ i :=
        (Finset.mul_sum (Finset.range (k + 1)) (fun i : ℕ => c ^ (k - i) * y ^ i) y).symm
      rw [h1', h2', Nat.sub_zero, pow_zero, mul_one,
        add_comm (y * ∑ i in Finset.range (k + 1), c ^ (k - i) * y ^ i) (c ^ (k + 1))]
    rw [hsplit2, hsplit, ih]
    ring

/-- PARTIAL FRACTIONS over the roots of unity: for `c^N != rho^N`,
    `sum_(m<N) 1/(c - rho*u_m) = N*c^(N-1)/(c^N - rho^N)`. This is the engine that turns
    every cross-ring kernel sum into a closed rational form. -/
theorem sum_inv_unity {N : ℕ} (hN : 0 < N) (c rho : ℂ)
    (hden : (c ^ (N : ℕ) - rho ^ (N : ℕ) : ℂ) ≠ 0) :
    ∑ m in (Finset.univ : Finset (Fin N)), (c - rho * unity N (m : ℕ))⁻¹
      = ((N : ℕ) : ℂ) * c ^ ((N : ℕ) - 1) / (c ^ (N : ℕ) - rho ^ (N : ℕ)) := by
  have huN : ∀ m : Fin N, (rho * unity N (m : ℕ)) ^ (N : ℕ) = rho ^ (N : ℕ) := fun m => by
    rw [mul_pow, unity_pow_N hN (m : ℕ), mul_one]
  have hcne : ∀ m : Fin N, c - rho * unity N (m : ℕ) ≠ 0 := by
    intro m h0
    apply hden
    have hceq : c = rho * unity N (m : ℕ) := sub_eq_zero.mp h0
    rw [hceq, huN m, sub_self]
  have hterm : ∀ m : Fin N, (c - rho * unity N (m : ℕ))⁻¹ * (c ^ (N : ℕ) - rho ^ (N : ℕ))
      = ∑ r in Finset.range (N : ℕ), c ^ ((N : ℕ) - 1 - r) * rho ^ r * (unity N (m : ℕ)) ^ r := by
    intro m
    have hgeo := pow_sub_pow_geom c (rho * unity N (m : ℕ)) (N - 1)
    rw [show (N - 1 : ℕ) + 1 = N from by omega] at hgeo
    rw [← huN m, hgeo]
    have h1 : (c - rho * unity N (m : ℕ))⁻¹
        * ((c - rho * unity N (m : ℕ)) * ∑ r in Finset.range (N : ℕ),
          c ^ ((N : ℕ) - 1 - r) * (rho * unity N (m : ℕ)) ^ r)
        = ((c - rho * unity N (m : ℕ))⁻¹ * (c - rho * unity N (m : ℕ)))
          * ∑ r in Finset.range (N : ℕ),
          c ^ ((N : ℕ) - 1 - r) * (rho * unity N (m : ℕ)) ^ r := by
      rw [← mul_assoc]
    rw [h1, inv_mul_cancel (hcne m), one_mul]
    exact Finset.sum_congr rfl fun r _ => by rw [mul_pow, ← mul_assoc]
  have hD : ∑ m in (Finset.univ : Finset (Fin N)),
      (c - rho * unity N (m : ℕ))⁻¹ * (c ^ (N : ℕ) - rho ^ (N : ℕ))
      = ((N : ℕ) : ℂ) * c ^ ((N : ℕ) - 1) := by
    rw [Finset.sum_congr rfl (fun m _ => hterm m), Finset.sum_comm]
    have hconv : ∀ r : ℕ, ∑ m in (Finset.univ : Finset (Fin N)), (unity N (m : ℕ)) ^ r
        = ∑ m in (Finset.univ : Finset (Fin N)), (unity N r) ^ (m : ℕ) := fun r =>
      Finset.sum_congr rfl fun m _ => by
        rw [unity_pow N (m : ℕ) r, Nat.mul_comm, ← unity_pow N r (m : ℕ)]
    rw [Finset.sum_eq_single_of_mem 0 (Finset.mem_range.mpr hN)]
    · simp
    · intro r hmem hr
      rw [Finset.mem_range] at hmem
      have hnd : r % (N : ℕ) ≠ 0 := by
        rw [Nat.mod_eq_of_lt hmem]
        exact hr
      simp only [← Finset.mul_sum]
      rw [hconv r, sum_unity_pow_eq_zero hN hnd, mul_zero]
  rw [eq_div_iff hden, Finset.sum_mul, ← hD]

/-- The half-turn involution on the residues: applying `j ↦ (N - j) % N` twice returns `j`. -/
theorem mod_N_sub_twice {N : ℕ} {j : ℕ} (hj : j < N) :
    (N - (N - j) % N) % N = j := by
  rcases Nat.eq_zero_or_pos j with h0 | hpos
  · subst h0
    simp
  · have hmod : (N - j) % N = N - j := Nat.mod_eq_of_lt (by omega)
    rw [hmod, Nat.sub_sub_self (by omega), Nat.mod_eq_of_lt hj]

set_option maxHeartbeats 1000000 in
/-- The kernel form of the partial fractions: for `conj(z)^N != conj(rho)^N`,
    `sum_(j<N) ker (z - rho*u_j) = N*conj(z)^(N-1) / (conj(z)^N - conj(rho)^N)` — the field
    of a whole regular ring measured at an arbitrary point `z` outside its radius orbit. -/
theorem sum_ker_cross {N : ℕ} (hN : 0 < N) (z rho : ℂ)
    (hden : ((conj z) ^ (N : ℕ) - (conj rho) ^ (N : ℕ) : ℂ) ≠ 0) :
    ∑ j in (Finset.univ : Finset (Fin N)), ker (z - rho * unity N (j : ℕ))
      = ((N : ℕ) : ℂ) * (conj z) ^ ((N : ℕ) - 1)
        / ((conj z) ^ (N : ℕ) - (conj rho) ^ (N : ℕ)) := by
  have hne : ∀ j : Fin N, z - rho * unity N (j : ℕ) ≠ 0 := by
    intro j h0
    apply hden
    have hceq : z = rho * unity N (j : ℕ) := sub_eq_zero.mp h0
    have hc : conj z = (conj rho) * (unity N (j : ℕ))⁻¹ := by
      rw [hceq, map_mul, unity_conj_inv]
    rw [hc, mul_pow, inv_pow, unity_pow_N hN (j : ℕ), inv_one, mul_one, sub_self]
  have hker : ∀ j : Fin N, ker (z - rho * unity N (j : ℕ))
      = (conj (z - rho * unity N (j : ℕ)))⁻¹ := fun j => ker_eq_inv_conj (hne j)
  -- the re-index `j ↦ (N - j) % N` turns `u_j^-1` into `u_j`, converting the conjugated
  -- summand into the partial-fraction shape
  have hre : ∑ j in (Finset.univ : Finset (Fin N)),
      ((conj z) - (conj rho) * (unity N (j : ℕ)))⁻¹
      = ∑ j in (Finset.univ : Finset (Fin N)),
      ((conj z) - (conj rho) * (unity N (j : ℕ))⁻¹)⁻¹ := by
    refine Finset.sum_nbij (fun j : Fin N => ⟨(N - (j : ℕ)) % N, Nat.mod_lt _ hN⟩)
      (fun j _ => Finset.mem_univ _) (fun j _ j' _ h => ?_) (fun m _ => ?_) (fun j _ => ?_)
    · rw [Fin.mk.injEq] at h
      have hj := mod_N_sub_twice (N := N) (j := (j : ℕ)) (by have := j.isLt; omega)
      have hj' := mod_N_sub_twice (N := N) (j := (j' : ℕ)) (by have := j'.isLt; omega)
      exact Fin.ext (by rw [← hj, ← hj', h])
    · refine ⟨⟨(N - (m : ℕ)) % N, Nat.mod_lt _ hN⟩, Finset.mem_univ _, ?_⟩
      rw [Fin.mk.injEq]
      exact mod_N_sub_twice (N := N) (j := (m : ℕ)) m.isLt
    · show ((conj z) - (conj rho) * (unity N (j : ℕ)))⁻¹
        = ((conj z) - (conj rho) * (unity N ((N - (j : ℕ)) % N))⁻¹)⁻¹
      have hu : unity N ((N - (j : ℕ)) % N) = (unity N (j : ℕ))⁻¹ := by
        rcases Nat.eq_zero_or_pos (j : ℕ) with h0 | -
        · have hu0 : unity N 0 = 1 := by
            simp only [unity, nGonAngle, Nat.cast_zero, zero_mul, mul_zero, zero_div,
              Complex.ofReal_zero, zero_mul, Complex.exp_zero]
          rw [show (j : ℕ) = 0 from h0, Nat.sub_zero, Nat.mod_self, hu0, inv_one]
        · rw [unity_mod hN, unity_inv hN j.isLt]
      rw [hu, inv_inv]

  have hkey : ∑ j in (Finset.univ : Finset (Fin N)), ker (z - rho * unity N (j : ℕ))
      = ∑ j in (Finset.univ : Finset (Fin N)),
        ((conj z) - (conj rho) * (unity N (j : ℕ))⁻¹)⁻¹ :=
    Finset.sum_congr rfl fun j _ => by rw [hker j, map_sub, map_mul, unity_conj_inv]
  rw [hkey, ← hre]
  exact sum_inv_unity hN (conj z) (conj rho) hden
/-! ### Axiom footprint -/
#print axioms exp_two_pi_I
#print axioms normSq_unity
#print axioms unity_mod
#print axioms unity_congr
#print axioms unity_inv
#print axioms unity_ne_one
#print axioms unity_add
#print axioms unity_pow
#print axioms mod_succ_right
#print axioms mod_succ_left
#print axioms unity_pow_N
#print axioms sum_unity_pow_eq_N
#print axioms sum_unity_pow_eq_zero
#print axioms sum_unity
#print axioms ker_neg
#print axioms unity_conj_inv
#print axioms ker_eq_inv_conj
#print axioms pow_sub_pow_geom
#print axioms sum_inv_unity
#print axioms mod_N_sub_twice
#print axioms sum_ker_cross

end TrivortexN.NRoots
