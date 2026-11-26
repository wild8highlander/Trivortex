/-
SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
-/
/-
==========================================================================
POLYVORTEX — LEAN 4 FORMALIZATION: THE N-VORTEX EXTENSION BENCH (v1.0)
==========================================================================
Milestone TW1 artifact: `verification/lean4/Polyvortex.lean`.

Provenance: this file generalizes the analytic layer of the Trivortex
monograph (repository wild8highlander/Trivortex, branch main, commit
58b7c7f) from `N = 3` to an arbitrary number `N ≥ 2` of point vortices,
expressed over `ℝ` and `ℂ` with Mathlib v4.6.0.  It proves, with zero
`sorry` and a sealed axiom footprint, the layer that the parent release
still certifies numerically only:

  1. THEOREM A (§1): the regular `N`-gon ring
       z_k(t) = R·ζ^k·exp(i·ω_N·t),   ω_N = Γ(N−1)/(4πR²)
     is an exact solution of the Kirchhoff point-vortex equations for
     every primitive `N`-th root of unity `ζ` (`ring_velocity`,
     `ringOrbit_sol`).  The analytic core is the roots-of-unity identity
       Σ_{m=1}^{N−1} 1/(1−ζ^m) = (N−1)/2
     (`sum_roots_of_unity`), proven by the involution m ↦ N−m.  The
     frequency is FORCED: a uniformly rotating ring solves the Kirchhoff
     field iff ω = ω_N — the polygonal analogue of the parent's Lagrange
     forcing theorem (`lag_omega_unique`).  At N = 3 the rate reproduces
     the parent value 3Γ/(2πa²) (`ringOmega_three_eq_lagrange`).

  2. THEOREM B (§2): the admissibility threshold of the pulsating ansatz
     r(t) = √C·(1 + ε·cos ωt), ε = 1/(exp(C/π) − 1):
       (∀ t k, 0 < r(t)) ↔ π·ln 2 < C
     (`rClosed_pos_iff`), with the exact-touch certificate at the
     threshold C = π ln 2 (`rClosed_touches_zero_at_threshold`) — the
     H1-gate of the parent protocol, lifted to the N-ring.

  3. LEMMA C (§3): NO pulsating ring can ride the Kirchhoff field: if
     the uniformly rotating pulsating configuration satisfies the
     point-vortex ODE, its radius is constant (`lemmaC_pulsation`,
     `lemmaC_radius_constant`); hence the C_Ch-pulsation scenario is
     obstructed in the N-vortex layer (`lemmaC_H1_reduction`).  The
     vanishing of the radial velocity is read off the exact ring
     solution (`ring_radial_zero`).

  4. LEMMA D (§4): the cycle-averaged Kirchhoff rate of the symmetric
     pulsation is independent of the pulsation frequency
     (`lemmaD_omega_independent`, `lemmaD_bridge`):
       avgKinFreq = ω_N / ((1−ε²)·√(1−ε²)),
     certified by the exact Poisson integral
       ∫₀^{2π} dφ/(1 + ε·cos φ) = 2π/√(1−ε²)
     (`poisson_integral`) and its squared companion (`poisson_sq`),
     both proven in closed form — no numerical quadrature anywhere.

  5. THEOREM E (§5, statement layer): the co-rotating field and its
     linearization at the ring (`corotatingField`, `corotLin`), the
     degeneracy certificates `ring_fixed_point`,
     `ring_corotating_constant`, `corotLin_orbit_kernel` (the orbit
     direction sits in the kernel of the co-rotating linearization —
     the exact source of the W4 noise floor), and the exact W4
     acceptance criterion (`havelockClassification`).  The spectral
     proof of the criterion is the queued milestone TW5 and is NOT
     claimed here; the parent monograph certifies it numerically.

Zero `sorry`, zero `axiom`, zero `native_decide`, zero `unsafe`.
The axiom footprint of every public theorem is sealed at the end of this
file and gated by `tools/axioms_gate.py` to
{propext, Classical.choice, Quot.sound}.
-/

import Mathlib.Tactic
import Mathlib.Algebra.BigOperators.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Arctan
import Mathlib.Analysis.SpecialFunctions.Trigonometric.ArctanDeriv
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.MeasureTheory.Integral.IntervalIntegral
import Mathlib.MeasureTheory.Integral.FundThmCalculus

/-!
# Polyvortex: the N-vortex extension bench

See the module docstring above for the five certified layers and
`README.md` for the protocol.  The numbering of the sections below
matches `docs/STATEMENTS.md`.
-/

namespace Polyvortex

open MeasureTheory intervalIntegral
open scoped BigOperators


/-!
### § 0. Private helpers

Reindexing lemmas for sums over `Finset.range` (each proven from
`Finset.sum_range_succ` alone), conjugation and `normSq` helpers for `ℂ`.
Nothing here is specific to vortices; everything is `private`.
-/

section Helpers

variable {M : Type*} [CommRing M]

/-- Shifting the index of a `range`-sum by one. -/
private theorem sum_range_shift_one (f : ℕ → M) (n : ℕ) :
    ∑ m in Finset.range n, f (m + 1) = ∑ m in Finset.range n, f m + f n - f 0 := by
  have h := Finset.sum_range_succ' f n
  rw [Finset.sum_range_succ f n] at h
  linear_combination h.symm

/-- The index translation `m ↦ (m + 1) % N` is summation-invariant. -/
private theorem sum_rot_shift (f : ℕ → M) (N : ℕ) :
    ∑ j in Finset.range N, f ((j + 1) % N) = ∑ j in Finset.range N, f j := by
  cases N with
  | zero => simp
  | succ n =>
      have h1 : ∀ j ∈ Finset.range n, (j + 1) % (n + 1) = j + 1 := fun j hj =>
        Nat.mod_eq_of_lt (by have := Finset.mem_range.mp hj; omega)
      have h2 : (n + 1) % (n + 1) = 0 := Nat.mod_self (n + 1)
      rw [Finset.sum_range_succ f n,
        Finset.sum_range_succ (fun j => f ((j + 1) % (n + 1))) n, h2,
        Finset.sum_congr rfl (fun j hj => by rw [h1 j hj]), sum_range_shift_one]
      ring

/-- The index translation `m ↦ (m + c) % N` is summation-invariant. -/
private theorem sum_rot (N : ℕ) : ∀ (c : ℕ) (f : ℕ → M),
    ∑ j in Finset.range N, f ((j + c) % N) = ∑ j in Finset.range N, f j := by
  intro c
  induction c with
  | zero =>
      intro f
      refine Finset.sum_congr rfl fun j hj => ?_
      rw [Nat.add_zero]
      exact congrArg f (Nat.mod_eq_of_lt (Finset.mem_range.mp hj))
  | succ c ih =>
      intro f
      have key : ∀ j : ℕ, (j + (c + 1)) % N = ((j + c) % N + 1) % N := by
        intro j
        rw [← Nat.add_assoc, Nat.mod_add_mod]
      have ih' : ∑ j in Finset.range N, f (((j + c) % N + 1) % N)
          = ∑ j in Finset.range N, f ((j + 1) % N) :=
        ih (fun m => f ((m + 1) % N))
      rw [Finset.sum_congr rfl (fun j _ => by rw [key j]), ih', sum_rot_shift f N]

/-- Reflecting the index of a `range`-sum, `m ↦ (n−1)−m`. -/
private theorem sum_range_reflect_aux (f : ℕ → M) : ∀ n : ℕ,
    ∑ m in Finset.range n, f ((n - 1) - m) = ∑ m in Finset.range n, f m :=
  fun n => Finset.sum_range_reflect f n

/-- A single erased point contributes zero to the full `range`-sum. -/
private theorem sum_erase_zero (f : ℕ → M) {N k : ℕ} (hk : k ∈ Finset.range N) :
    ∑ j in (Finset.range N).erase k, f j
      = ∑ j in Finset.range N, (if j = k then 0 else f j) := by
  have hnot : k ∉ (Finset.range N).erase k := by simp [hk]
  have hzero : ((if k = k then (0 : M) else f k) : M) = 0 := by simp
  have key : ∑ j in insert k ((Finset.range N).erase k), (if j = k then 0 else f j)
      = ∑ j in Finset.range N, (if j = k then 0 else f j) := by
    rw [Finset.insert_erase hk]
  rw [← key, Finset.sum_insert hnot, hzero, Finset.sum_congr rfl (fun j hj => ?_),
    zero_add]
  exact (if_neg (Finset.mem_erase.mp hj).1).symm

/-- Complex conjugation is multiplicative (`star_mul'`). -/
private theorem conj_mul' (a b : ℂ) :
    star (a * b) = star a * star b :=
  star_mul' a b

/-- Complex conjugation is additive over differences. -/
private theorem conj_sub' (a b : ℂ) :
    star (a - b) = star a - star b := by
  exact star_sub a b

/-- Complex conjugation commutes with natural powers (`star_pow`). -/
private theorem conj_pow' (a : ℂ) : ∀ n : ℕ,
    star (a ^ n) = (star a) ^ n :=
  star_pow a

/-- Double conjugation is the identity (`star_involutive`). -/
private theorem conj_conj' (z : ℂ) : star (star z) = z :=
  star_involutive z

/-- `normSq` of a product, as a `ℂ`-valued identity. -/
private theorem normSq_mul' (a b : ℂ) :
    (Complex.normSq (a * b) : ℂ) = (Complex.normSq a : ℂ) * (Complex.normSq b : ℂ) := by
  rw [Complex.normSq_mul, Complex.ofReal_mul]

/-- `normSq` of a real scalar, as a `ℂ`-valued identity. -/
private theorem normSq_ofReal' (r : ℝ) :
    (Complex.normSq ((r : ℂ)) : ℂ) = ((r * r : ℝ) : ℂ) := by
  rw [Complex.normSq_ofReal]

/-- A nonzero complex number has nonzero `normSq`. -/
private theorem normSq_ne_zero' {z : ℂ} (h : z ≠ 0) : Complex.normSq z ≠ 0 := by
  intro h0
  exact h (Complex.normSq_eq_zero.mp h0)

end Helpers

/-!
### § 1. Theorem A: the regular `N`-gon ring is an exact solution

The ring `z_k = R·ζ^k` (with `ζ` a primitive `N`-th root of unity) is carried
by the Kirchhoff field exactly as a solid rotation with angular rate
`ω_N = Γ(N−1)/(4πR²)` (`ring_velocity`), and the rate is forced:
a uniformly rotating ring solves the Kirchhoff field iff `ω = ω_N`
(`ringOrbit_sol`).
-/

section TheoremA

/-! #### The objects. -/

/-- The canonical primitive `N`-th root of unity `exp(2πi/N)`. -/
noncomputable def rootExp (N : ℕ) : ℂ := Complex.exp (2 * Real.pi * Complex.I / (N : ℂ))

/-- The `k`-th vertex of the regular `N`-gon ring of radius `R` with root `ζ`. -/
noncomputable def ringPos (R : ℝ) (ζ : ℂ) (k : ℕ) : ℂ := (R : ℂ) * ζ ^ k

/-- The Kirchhoff angular rate of the regular `N`-gon ring of radius `R`. -/
noncomputable def ringOmega (γ : ℝ) (R : ℝ) (N : ℕ) : ℝ :=
  γ * ((N - 1 : ℕ) : ℝ) / (4 * Real.pi * R ^ 2)

/-- The Kirchhoff point-vortex field: the velocity of vertex `k` induced by
the other vertices of the configuration `z`. -/
noncomputable def kirchhoff (γ : ℝ) (z : ℕ → ℂ) (N : ℕ) (k : ℕ) : ℂ :=
  ((γ / (2 * Real.pi) : ℝ) : ℂ) *
    ∑ j in (Finset.range N).erase k,
      Complex.I * (z k - z j) / ((Complex.normSq (z k - z j) : ℝ) : ℂ)

/-! #### Modular bookkeeping. -/

/-- If `(j + (N−k)) % N = 0` with `j, k < N` then `j = k`. -/
private theorem mod_add_zero_eq {N j k : ℕ} (hj : j < N) (hk : k < N) (_hkle : k ≤ N)
    (h : (j + (N - k)) % N = 0) : j = k := by
  have e1 : (j + (N - k) + k) % N = (0 + k) % N := by
    rw [← Nat.mod_add_mod, h]
  rw [show (j + (N - k) + k) = j + N * 1 from by omega,
    Nat.add_mul_mod_self_left, Nat.zero_add] at e1
  exact (Nat.mod_eq_of_lt hj).symm.trans (e1.trans (Nat.mod_eq_of_lt hk))

/-- `k + (N − k)` reduces to `0` modulo `N`. -/
private theorem mod_self' {N k : ℕ} (hkle : k ≤ N) : (k + (N - k)) % N = 0 := by
  rw [show (k + (N - k)) = N from by omega, Nat.mod_self]

/-- If `(k + d) % N = k` then `d` is a positive multiple of `N`; with `1 ≤ d < N`
this is absurd. -/
private theorem mod_add_eq_self {N k d : ℕ} (hk : k < N) (hd1 : 1 ≤ d) (hdN : d < N)
    (h : (k + d) % N = k) : False := by
  have hmeq : (k + d) ≡ (k + 0) [MOD N] := by
    show (k + d) % N = (k + 0) % N
    rw [h, Nat.add_zero]
    exact (Nat.mod_eq_of_lt hk).symm
  have hd0 : d % N = 0 := Nat.ModEq.add_left_cancel' k hmeq
  have hdiv : d / N * N = d := by
    have hdm := Nat.div_add_mod d N
    rw [Nat.mul_comm N (d / N), hd0, Nat.add_zero] at hdm
    exact hdm
  rcases Nat.eq_zero_or_pos (d / N) with hq | hq
  · rw [hq, Nat.zero_mul] at hdiv
    exact absurd hdiv.symm (by omega)
  · have hle : N ≤ d := by
      rw [← hdiv, Nat.mul_comm]
      exact Nat.le_mul_of_pos_right N hq
    omega

/-- For `1 ≤ d < N` the exponents `d·(N−1)` and `N−d` agree modulo `N`. -/
private theorem mul_pred_mod {N d : ℕ} (hd1 : 1 ≤ d) (hdN : d < N) :
    (d * (N - 1)) % N = (N - d) % N := by
  have e1 : (d * (N - 1)) + d ≡ 0 [MOD N] := by
    show ((d * (N - 1)) + d) % N = 0 % N
    rw [show (d * (N - 1)) + d = N * d
        from by rw [Nat.mul_sub_left_distrib, Nat.mul_one,
          Nat.sub_add_cancel (Nat.le_mul_of_pos_right d
            (show (0:ℕ) < N from by omega)), Nat.mul_comm],
      Nat.mul_mod_right, Nat.zero_mod]
  have e2 : ((N - d) + d) ≡ 0 [MOD N] := by
    show (((N - d) + d) % N) = 0 % N
    rw [show (N - d) + d = N from by omega, Nat.mod_self, Nat.zero_mod]
  have e12 : (d * (N - 1)) + d ≡ ((N - d) + d) [MOD N] := e1.trans e2.symm
  exact Nat.ModEq.add_right_cancel' d e12

/-! #### Roots of unity. -/

/-- A nonzero exponent of a root of unity keeps the root nonzero. -/
theorem root_ne_zero {ζ : ℂ} {N : ℕ} (hN : N ≠ 0) (h1 : ζ ^ N = 1) : ζ ≠ 0 := by
  intro hz
  rw [hz, zero_pow hN] at h1
  norm_num at h1

/-- `normSq` of a natural power, as a `ℂ`-valued identity. -/
private theorem normSq_pow' (a : ℂ) : ∀ n : ℕ,
    (Complex.normSq (a ^ n) : ℂ) = (Complex.normSq a : ℂ) ^ n
  | 0 => by simp
  | n + 1 => by rw [pow_succ, pow_succ, normSq_mul', normSq_pow' a n]

/-- For a nonnegative real `x`, `x ^ N = 1` with `N ≠ 0` forces `x = 1`. -/
private theorem real_pow_eq_one_of_nonneg {x : ℝ} (hx : 0 ≤ x) {N : ℕ} (hN : N ≠ 0)
    (h : x ^ N = 1) : x = 1 := by
  rcases lt_or_le x 1 with hxlt | hge
  · exact absurd h (ne_of_lt (pow_lt_one hx hxlt hN))
  · rcases lt_or_eq_of_le hge with h1lt | hxe
    · exact absurd h (ne_of_gt (one_lt_pow h1lt hN))
    · exact hxe.symm

/-- The conjugate of a root of unity is its `(N−1)`-st power. -/
theorem conj_root_unity {ζ : ℂ} {N : ℕ} (hN : N ≠ 0) (h1 : ζ ^ N = 1) :
    star ζ = ζ ^ (N - 1) := by
  have hc : (Complex.normSq ζ : ℂ) ^ N = 1 := by
    rw [Complex.normSq_eq_conj_mul_self]
    simp only [starRingEnd_apply]
    rw [mul_pow, ← conj_pow', h1, star_one, mul_one]
  have hr : Complex.normSq ζ = 1 := by
    refine real_pow_eq_one_of_nonneg (Complex.normSq_nonneg ζ) hN ?_
    have h2 := hc
    rw [← Complex.ofReal_pow, ← Complex.ofReal_one, Complex.ofReal_inj] at h2
    exact h2
  refine mul_left_cancel₀ (root_ne_zero hN h1) ?_
  calc ζ * star ζ = star ζ * ζ := mul_comm _ _
    _ = (Complex.normSq ζ : ℂ) := (Complex.normSq_eq_conj_mul_self).symm
    _ = 1 := by rw [hr, Complex.ofReal_one]
    _ = ζ ^ N := h1.symm
    _ = ζ * ζ ^ (N - 1) := by
        conv_lhs => rw [show N = N - 1 + 1 from by omega]

/-- Any exponent of a root of unity reduces modulo `N`. -/
theorem pow_mod_eq {ζ : ℂ} {N : ℕ} (h1 : ζ ^ N = 1) (m : ℕ) :
    ζ ^ (m % N) = ζ ^ m := by
  conv_rhs => rw [(Nat.mod_add_div m N).symm]
  rw [pow_add, pow_mul, h1, one_pow, mul_one]

/-- On the ring, the difference of two vertices factors through `1 − ζ^d`. -/
theorem ringPos_sub_ringPos {R : ℝ} {ζ : ℂ} {N : ℕ} (h1 : ζ ^ N = 1)
    {k j : ℕ} (hk : k < N) (_hj : j < N) :
    ringPos R ζ k - ringPos R ζ j
      = (R : ℂ) * ζ ^ k * (1 - ζ ^ ((j + (N - k)) % N)) := by
  have hmod : ζ ^ ((j + (N - k)) % N) = ζ ^ (j + (N - k)) := pow_mod_eq h1 _
  have hexp : ζ ^ k * ζ ^ (j + (N - k)) = ζ ^ j := by
    rw [← pow_add, show k + (j + (N - k)) = j + N from by omega, pow_add, h1,
      mul_one]
  unfold ringPos
  rw [hmod]
  linear_combination (R : ℂ) * hexp

/-- The pair velocity of the ring, in geometric form: the vertex pair at cyclic
distance `d = (j + (N−k)) % N ∈ [1, N−1]` contributes `iζ^k/(R(1−ζ^{N−d}))`. -/
private theorem ring_term {R : ℝ} {ζ : ℂ} {N : ℕ} (hN : N ≠ 0) (h1 : ζ ^ N = 1)
    (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (hR : R ≠ 0) {k j : ℕ} (hk : k < N)
    (hj : j < N) (hjk : j ≠ k) :
    Complex.I * (ringPos R ζ k - ringPos R ζ j)
        / ((Complex.normSq (ringPos R ζ k - ringPos R ζ j) : ℝ) : ℂ)
      = Complex.I / (R : ℂ) * ζ ^ k
        * (1 - ζ ^ (N - ((j + (N - k)) % N)))⁻¹ := by
  have hN0 : N ≠ 0 := by omega
  set d := (j + (N - k)) % N with _hddef
  have hdN : d < N := Nat.mod_lt _ (Nat.pos_of_ne_zero hN0)
  have hd1 : 1 ≤ d := by
    refine Nat.pos_of_ne_zero fun h0 => hjk ?_
    exact mod_add_zero_eq hj hk hk.le h0
  have hx1 : ζ ^ d ≠ 1 := hprim d (Finset.mem_Ico.mpr ⟨hd1, hdN⟩)
  have hzone : (1 - ζ ^ d) ≠ 0 := sub_ne_zero.mpr (Ne.symm hx1)
  have hzone' : (1 - ζ ^ (N - d)) ≠ 0 :=
    sub_ne_zero.mpr (Ne.symm
      (hprim (N - d) (Finset.mem_Ico.mpr ⟨by omega, by omega⟩)))
  have hdiff : ringPos R ζ k - ringPos R ζ j
      = (R : ℂ) * ζ ^ k * (1 - ζ ^ d) := ringPos_sub_ringPos h1 hk hj
  have hck : (Complex.normSq (ζ ^ k) : ℂ) = 1 := by
    rw [Complex.normSq_eq_conj_mul_self]
    simp only [starRingEnd_apply]
    rw [conj_pow', conj_root_unity hN h1, ← pow_mul, ← pow_add,
      Nat.mul_sub_right_distrib,
      show N * k - 1 * k + k = N * k from by
        have hkle : k ≤ N * k := by
          rw [Nat.mul_comm]
          exact Nat.le_mul_of_pos_right k (show (0:ℕ) < N from by omega)
        rw [Nat.one_mul, Nat.sub_add_cancel hkle],
      pow_mul, h1, one_pow]
  have hexp2 : ζ ^ ((N - 1) * d) = ζ ^ (N - d) := by
    rw [← pow_mod_eq h1 ((N - 1) * d), Nat.mul_comm (N - 1) d,
      mul_pred_mod hd1 hdN, Nat.mod_eq_of_lt (by omega)]
  have hcd : (Complex.normSq (1 - ζ ^ d) : ℂ) = (1 - ζ ^ (N - d)) * (1 - ζ ^ d) := by
    rw [Complex.normSq_eq_conj_mul_self]
    simp only [starRingEnd_apply]
    rw [conj_sub', conj_pow', conj_root_unity hN h1, ← pow_mul, star_one, hexp2]
  have hRc : (R : ℂ) ≠ 0 := by exact_mod_cast hR
  have hR2 : ((R * R : ℝ) : ℂ) ≠ 0 := by exact_mod_cast mul_ne_zero hR hR
  rw [hdiff, normSq_mul', normSq_mul', normSq_ofReal', hck, mul_one, hcd]
  field_simp [hRc, hR2, hzone, hzone']
  ring

/-- The field core of the pairing: for `x·y = 1`, `x ≠ 0`, `x ≠ 1` the two
reflected fractions sum to one (this covers the fixed point `x = y = −1`). -/
private theorem roots_pair_core {x y : ℂ} (hxy : x * y = 1) (_hx0 : x ≠ 0) (hx1 : x ≠ 1) :
    1 / (1 - x) + 1 / (1 - y) = 1 := by
  have _hy0 : y ≠ 0 := by
    intro hy
    rw [hy, mul_zero] at hxy
    exact zero_ne_one hxy
  have hy1 : y ≠ 1 := by
    intro hy
    apply hx1
    rw [← hxy, hy, mul_one]
  have hz1 : (1 - x) ≠ 0 := sub_ne_zero.mpr (Ne.symm hx1)
  have hz2 : (1 - y) ≠ 0 := sub_ne_zero.mpr (Ne.symm hy1)
  have hnum : (1 - y) + (1 - x) = (1 - x) * (1 - y) := by
    linear_combination hxy.symm
  rw [div_add_div 1 1 hz1 hz2, one_mul, mul_one, hnum,
    div_self (mul_ne_zero hz1 hz2)]

/-- **The roots-of-unity identity** — the analytic core of Theorem A:
`∑_{m=1}^{N−1} 1/(1−ζ^m) = (N−1)/2`, proven by the involution `m ↦ N−m`
(the fixed point `m = N/2` contributes `1/2` through the same field identity). -/
theorem sum_roots_of_unity {ζ : ℂ} {N : ℕ} (h1 : ζ ^ N = 1)
    (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) :
    ∑ m in Finset.range (N - 1), 1 / (1 - ζ ^ (m + 1)) = (((N - 1 : ℕ) : ℝ) : ℂ) / 2 := by
  rcases N with _ | _ | n
  · simp
  · simp
  · -- N = n + 2 ≥ 2
    have hN0 : (n + 2) ≠ 0 := by omega
    have hζ : ζ ≠ 0 := root_ne_zero hN0 h1
    have hpair : ∀ m ∈ Finset.range (n + 1),
        1 / (1 - ζ ^ (m + 1)) + 1 / (1 - ζ ^ (n - m + 1)) = 1 := by
      intro m hm
      have hx0 : ζ ^ (m + 1) ≠ 0 := pow_ne_zero _ hζ
      have hx1 : ζ ^ (m + 1) ≠ 1 :=
        hprim (m + 1) (Finset.mem_Ico.mpr ⟨by omega,
          by have := Finset.mem_range.mp hm; omega⟩)
      have hexp : ζ ^ (m + 1) * ζ ^ (n - m + 1) = ζ ^ (n + 2) := by
        rw [← pow_add, show m + 1 + (n - m + 1) = n + 2 from by
          have := Finset.mem_range.mp hm; omega]
      exact roots_pair_core (hexp.trans h1) hx0 hx1
    have href : (∑ m in Finset.range (n + 1), 1 / (1 - ζ ^ (n - m + 1)) : ℂ)
        = ∑ m in Finset.range (n + 1), 1 / (1 - ζ ^ (m + 1)) :=
      sum_range_reflect_aux (fun m => 1 / (1 - ζ ^ (m + 1))) (n + 1)
    have hsum : (∑ m in Finset.range (n + 1), 1 / (1 - ζ ^ (m + 1)) : ℂ)
        + ∑ m in Finset.range (n + 1), 1 / (1 - ζ ^ (n - m + 1))
          = (((n + 1 : ℕ) : ℝ) : ℂ) := by
      rw [← Finset.sum_add_distrib, Finset.sum_congr rfl (fun m hm => hpair m hm),
        Finset.sum_const, Finset.card_range, nsmul_eq_mul, mul_one,
        Complex.ofReal_nat_cast]
    rw [href] at hsum
    have hS : (∑ m in Finset.range (n + 1), 1 / (1 - ζ ^ (m + 1)) : ℂ)
        = (((n + 1 : ℕ) : ℝ) : ℂ) / 2 := by
      rw [eq_div_iff two_ne_zero, ← mul_comm (2:ℂ)
        (∑ m in Finset.range (n + 1), 1 / (1 - ζ ^ (m + 1))), two_mul]
      exact hsum
    rw [show ((n + 2 : ℕ) - 1) = n + 1 from by omega, hS]

/-- **Theorem A.** The Kirchhoff field on the ring is exactly the solid-rotation
field `i·ω_N·z_k` at every vertex. -/
theorem ring_velocity (γ : ℝ) (N : ℕ) (hN : 2 ≤ N) (R : ℝ) (hR : R ≠ 0) (ζ : ℂ)
    (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) {k : ℕ} (hk : k < N) :
    kirchhoff γ (ringPos R ζ) N k
      = Complex.I * ((ringOmega γ R N : ℝ) : ℂ) * ringPos R ζ k := by
  have hN0 : N ≠ 0 := by omega
  have inner : (∑ j in (Finset.range N).erase k,
      (1 - ζ ^ (N - ((j + (N - k)) % N)))⁻¹ : ℂ) = (((N - 1 : ℕ) : ℝ) : ℂ) / 2 := by
    have hF0 : (1 - ζ ^ N)⁻¹ = (0 : ℂ) := by
      rw [h1, sub_self, inv_zero]
    have e0 : (∑ j in (Finset.range N).erase k,
        (1 - ζ ^ (N - ((j + (N - k)) % N)))⁻¹ : ℂ)
        = ∑ j in Finset.range N, (1 - ζ ^ (N - ((j + (N - k)) % N)))⁻¹ := by
      rw [sum_erase_zero (fun j => (1 - ζ ^ (N - ((j + (N - k)) % N)))⁻¹)
        (Finset.mem_range.mpr hk)]
      refine Finset.sum_congr rfl fun j _hj => ?_
      by_cases hjk : j = k
      · subst hjk
        rw [if_pos rfl, mod_self' hk.le, Nat.sub_zero, hF0]
      · rw [if_neg hjk]
    have rot : (∑ j in Finset.range N, (1 - ζ ^ (N - ((j + (N - k)) % N)))⁻¹ : ℂ)
        = ∑ j in Finset.range N, (fun m => (1 - ζ ^ (N - m))⁻¹) ((j + (N - k)) % N) :=
      rfl
    have rot' : (∑ j in Finset.range N, (fun m => (1 - ζ ^ (N - m))⁻¹) ((j + (N - k)) % N) : ℂ)
        = ∑ j in Finset.range N, (fun m => (1 - ζ ^ (N - m))⁻¹) j :=
      sum_rot N (N - k) (fun m => (1 - ζ ^ (N - m))⁻¹)
    have hsplit : (∑ j in Finset.range N, (fun m => (1 - ζ ^ (N - m))⁻¹) j : ℂ)
        = (1 - ζ ^ (N - 0))⁻¹
          + ∑ j in Finset.range (N - 1), (1 - ζ ^ (N - (j + 1)))⁻¹ := by
        obtain ⟨k, rfl⟩ : ∃ k, N = k + 1 := ⟨N - 1, by omega⟩
        rw [Finset.sum_range_succ' (fun m => (1 - ζ ^ (k + 1 - m))⁻¹) k,
          add_comm]
        rfl
    rw [e0, rot, rot', hsplit, Nat.sub_zero, hF0, zero_add]
    have reflH := sum_range_reflect_aux (fun m => (1 - ζ ^ (N - (m + 1)))⁻¹) (N - 1)
    rw [← reflH]
    rw [Finset.sum_congr rfl (fun m hm => by
      have hmN : m < N - 1 := Finset.mem_range.mp hm
      show ((1 - ζ ^ (N - ((N - 1 - 1) - m + 1)))⁻¹ : ℂ) = (1 - ζ ^ (m + 1))⁻¹
      rw [show N - ((N - 1 - 1) - m + 1) = m + 1 from by omega])]
    rw [← sum_roots_of_unity h1 hprim]
    exact Finset.sum_congr rfl fun m _ => (one_div _).symm
  simp only [kirchhoff]
  rw [Finset.sum_congr rfl (fun j hj =>
    ring_term hN0 h1 hprim hR hk
      (Finset.mem_range.mp (Finset.mem_erase.mp hj).2)
      (Finset.mem_erase.mp hj).1)]
  rw [← Finset.mul_sum, inner]
  have _hw : (ringOmega γ R N : ℝ) = γ * ((N - 1 : ℕ) : ℝ) / (4 * Real.pi * R ^ 2) := rfl
  show ((γ / (2 * Real.pi) : ℝ) : ℂ) * (Complex.I / (R : ℂ) * ζ ^ k
      * ((((N - 1 : ℕ) : ℝ) : ℂ) / 2))
    = Complex.I * ((γ * ((N - 1 : ℕ) : ℝ) / (4 * Real.pi * R ^ 2) : ℝ) : ℂ)
      * ((R : ℂ) * ζ ^ k)
  have hRc : (R : ℂ) ≠ 0 := by exact_mod_cast hR
  have hR2 : ((R * R : ℝ) : ℂ) ≠ 0 := by exact_mod_cast mul_ne_zero hR hR
  field_simp [hRc, hR2, Real.pi_ne_zero]
  ring

/-- Rotational equivariance of the Kirchhoff field: multiplication by a unit
complex number carries solutions to solutions. -/
theorem kirchhoff_smul (γ : ℝ) {N : ℕ} {z : ℕ → ℂ} {u : ℂ} (hu : Complex.normSq u = 1)
    (k : ℕ) :
    kirchhoff γ (fun j => u * z j) N k = u * kirchhoff γ z N k := by
  have hs : (∑ j in (Finset.range N).erase k,
      Complex.I * (u * z k - u * z j) / ((Complex.normSq (u * z k - u * z j) : ℝ) : ℂ) : ℂ)
      = u * ∑ j in (Finset.range N).erase k,
        Complex.I * (z k - z j) / ((Complex.normSq (z k - z j) : ℝ) : ℂ) := by
    have hterm : ∀ j ∈ (Finset.range N).erase k,
        Complex.I * (u * z k - u * z j)
            / ((Complex.normSq (u * z k - u * z j) : ℝ) : ℂ)
          = u * (Complex.I * (z k - z j)
            / ((Complex.normSq (z k - z j) : ℝ) : ℂ)) := by
      intro j _
      rw [← mul_sub u, Complex.normSq_mul, hu, one_mul]
      ring
    rw [Finset.sum_congr rfl hterm, ← Finset.mul_sum]
  simp only [kirchhoff]
  rw [hs]
  ring

/-- The complex exponential of a purely imaginary number lies on the unit
circle. -/
theorem normSq_exp_I_mul (θ : ℝ) :
    Complex.normSq (Complex.exp (Complex.I * θ)) = 1 := by
  have hre : (Complex.I * (θ : ℂ)).re = 0 := by
    rw [Complex.mul_re, Complex.I_re, Complex.I_im, Complex.ofReal_re,
      Complex.ofReal_im, zero_mul, mul_zero, sub_self]
  have him : (Complex.I * (θ : ℂ)).im = θ := by
    rw [Complex.mul_im, Complex.I_re, Complex.I_im, Complex.ofReal_im,
      Complex.ofReal_re]
    ring
  rw [Complex.normSq_apply, Complex.exp_re, Complex.exp_im, hre, him,
    Real.exp_zero, one_mul, one_mul, ← sq, ← sq, add_comm]
  exact Real.sin_sq_add_cos_sq θ

/-- The uniformly rotating ring orbit. -/
noncomputable def ringOrbit (R : ℝ) (ζ : ℂ) (ω : ℝ) (t : ℝ) (k : ℕ) : ℂ :=
  ringPos R ζ k * Complex.exp (Complex.I * (ω * t))

/-- The orbit is carried at angular rate `ω`: its derivative is `iω·z_k(t)`. -/
theorem ringOrbit_deriv (R : ℝ) (ζ : ℂ) (ω : ℝ) (k : ℕ) (t : ℝ) :
    HasDerivAt (fun s => ringOrbit R ζ ω s k)
      (Complex.I * ω * ringOrbit R ζ ω t k) t := by
  have hinner : HasDerivAt (fun s : ℝ => Complex.I * ((ω * s : ℝ) : ℂ))
      (Complex.I * ((ω : ℝ) : ℂ)) t := by
    have h1 := HasDerivAt.const_smul (Complex.I * ((ω : ℝ) : ℂ))
      (ContinuousLinearMap.hasDerivAt (x := t) Complex.ofRealCLM)
    simp only [smul_eq_mul, ContinuousLinearMap.coe_coe, Complex.ofRealCLM_apply,
      Complex.ofReal_one, mul_one] at h1
    rw [show (fun s : ℝ => Complex.I * ((ω * s : ℝ) : ℂ))
        = fun s : ℝ => Complex.I * ((ω : ℝ) : ℂ) * ((s : ℝ) : ℂ) from by
      funext s; rw [mul_assoc, ← Complex.ofReal_mul]]
    exact h1
  have hexp : HasDerivAt (Complex.exp ∘ fun s : ℝ => Complex.I * ((ω * s : ℝ) : ℂ))
      (Complex.exp (Complex.I * ((ω * t : ℝ) : ℂ)) * (Complex.I * ((ω : ℝ) : ℂ))) t :=
    HasDerivAt.comp (x := t) (h := fun s : ℝ => Complex.I * ((ω * s : ℝ) : ℂ))
      (Complex.hasDerivAt_exp (Complex.I * ((ω * t : ℝ) : ℂ))) hinner
  simpa [ringOrbit, mul_assoc, mul_comm, mul_left_comm, Function.comp_apply] using
    HasDerivAt.const_mul (ringPos R ζ k) hexp

/-- The Kirchhoff field evaluated on the rotating orbit at time `t`. -/
theorem kirchhoff_ringOrbit (γ : ℝ) (N : ℕ) (hN : 2 ≤ N) (R : ℝ) (hR : R ≠ 0) (ζ : ℂ)
    (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (ω : ℝ) (t : ℝ)
    {k : ℕ} (hk : k < N) :
    kirchhoff γ (fun j => ringOrbit R ζ ω t j) N k
      = Complex.I * ((ringOmega γ R N : ℝ) : ℂ) * ringOrbit R ζ ω t k := by
  have hu : Complex.normSq (Complex.exp (Complex.I * (↑ω * ↑t))) = 1 := by
    rw [← Complex.ofReal_mul]
    exact normSq_exp_I_mul (ω * t)
  have hfun : (fun j => ringOrbit R ζ ω t j)
      = fun j => Complex.exp (Complex.I * (ω * t)) * ringPos R ζ j := by
    funext j
    unfold ringOrbit
    ring
  rw [hfun, kirchhoff_smul γ hu k, ring_velocity γ N hN R hR ζ h1 hprim hk]
  unfold ringOrbit
  ring

/-- **The forcing theorem for the ring.** A uniformly rotating ring solves the
Kirchhoff equations exactly when the angular rate is `ω_N` — the polygonal
analogue of the parent monograph's Lagrange forcing theorem. -/
theorem ringOrbit_sol (γ : ℝ) (N : ℕ) (hN : 2 ≤ N) (R : ℝ) (hR : R ≠ 0) (ζ : ℂ)
    (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (ω : ℝ) :
    (∀ (t : ℝ) (k : ℕ), HasDerivAt (fun s => ringOrbit R ζ ω s k)
        (kirchhoff γ (fun j => ringOrbit R ζ ω t j) N k) t) ↔ ω = ringOmega γ R N := by
  constructor
  · intro hode
    have heq := HasDerivAt.unique (hode 0 0) (ringOrbit_deriv R ζ ω 0 0)
    rw [kirchhoff_ringOrbit γ N hN R hR ζ h1 hprim ω 0 (by omega)] at heq
    have hpos : ringOrbit R ζ ω 0 0 ≠ 0 := by
      unfold ringOrbit ringPos
      exact mul_ne_zero
        (mul_ne_zero (by exact_mod_cast hR)
          (pow_ne_zero 0 (root_ne_zero (by omega : N ≠ 0) h1)))
        (Complex.exp_ne_zero _)
    have hcanc : Complex.I * ω = Complex.I * ((ringOmega γ R N : ℝ) : ℂ) :=
      (mul_right_cancel₀ hpos heq).symm
    exact Complex.ofReal_inj.mp (mul_left_cancel₀ Complex.I_ne_zero hcanc)
  · intro hw
    subst hw
    intro t k
    have hN0 : N ≠ 0 := by omega
    have hmod : k % N < N := Nat.mod_lt _ (Nat.pos_of_ne_zero hN0)
    have hkp : kirchhoff γ (fun j => ringOrbit R ζ (ringOmega γ R N) t j) N k
        = kirchhoff γ (fun j => ringOrbit R ζ (ringOmega γ R N) t j) N (k % N) := by
      unfold kirchhoff
      simp only []
      have hz2 : ringOrbit R ζ (ringOmega γ R N) t k
          = ringOrbit R ζ (ringOmega γ R N) t (k % N) := by
        unfold ringOrbit ringPos
        rw [← pow_mod_eq h1 k]
      rcases Nat.lt_or_ge k N with hkl | hkg
      · rw [Nat.mod_eq_of_lt hkl]
      · rw [Finset.erase_eq_of_not_mem (by simp [Finset.mem_range, hkg])]
        have hR : ∑ x in Finset.range N,
            Complex.I * (ringOrbit R ζ (ringOmega γ R N) t (k % N)
                - ringOrbit R ζ (ringOmega γ R N) t x)
              / ((Complex.normSq (ringOrbit R ζ (ringOmega γ R N) t (k % N)
                  - ringOrbit R ζ (ringOmega γ R N) t x) : ℝ) : ℂ)
            = ∑ j in (Finset.range N).erase (k % N),
            Complex.I * (ringOrbit R ζ (ringOmega γ R N) t (k % N)
                - ringOrbit R ζ (ringOmega γ R N) t j)
              / ((Complex.normSq (ringOrbit R ζ (ringOmega γ R N) t (k % N)
                  - ringOrbit R ζ (ringOmega γ R N) t j) : ℝ) : ℂ) := by
          rw [← Finset.sum_erase_add (Finset.range N)
            (fun x => Complex.I * (ringOrbit R ζ (ringOmega γ R N) t (k % N)
                - ringOrbit R ζ (ringOmega γ R N) t x)
              / ((Complex.normSq (ringOrbit R ζ (ringOmega γ R N) t (k % N)
                  - ringOrbit R ζ (ringOmega γ R N) t x) : ℝ) : ℂ))
            (Finset.mem_range.mpr hmod)]
          rw [sub_self, mul_zero, Complex.normSq_zero, Complex.ofReal_zero,
            div_zero, add_zero]
        rw [← hR]
        congr 1
        refine Finset.sum_congr rfl fun j _ => ?_
        rw [hz2]
    rw [hkp, kirchhoff_ringOrbit γ N hN R hR ζ h1 hprim (ringOmega γ R N) t
      hmod]
    have hzfun : (fun s => ringOrbit R ζ (ringOmega γ R N) s k)
        = fun s => ringOrbit R ζ (ringOmega γ R N) s (k % N) := by
      funext s
      unfold ringOrbit ringPos
      rw [← pow_mod_eq h1 k]
    rw [hzfun]
    exact ringOrbit_deriv R ζ (ringOmega γ R N) (k % N) t

/-! #### The canonical root. -/

/-- The canonical root is a genuine root of unity. -/
theorem rootExp_pow {N : ℕ} (hN : N ≠ 0) : rootExp N ^ N = 1 := by
  rcases Nat.eq_zero_or_pos N with h | _h
  · exact absurd h hN
  unfold rootExp
  rw [← Complex.exp_nat_mul]
  have hc : ((N : ℂ) * (2 * Real.pi * Complex.I / (N : ℂ)) : ℂ)
      = 2 * Real.pi * Complex.I := by
    field_simp [show ((N : ℂ)) ≠ 0 from by exact_mod_cast hN]
    ring
  rw [hc]
  refine Complex.ext ?_ ?_
  · rw [Complex.exp_re,
      show (2 * Real.pi * Complex.I).re = 0 from by
        simp [Complex.mul_re, Complex.I_re, Complex.I_im],
      show (2 * Real.pi * Complex.I).im = 2 * Real.pi from by
        simp [Complex.mul_im, Complex.I_re, Complex.I_im],
      Real.exp_zero, Real.cos_two_pi, mul_one, Complex.one_re]
  · rw [Complex.exp_im,
      show (2 * Real.pi * Complex.I).im = 2 * Real.pi from by
        simp [Complex.mul_im, Complex.I_re, Complex.I_im],
      show (2 * Real.pi * Complex.I).re = 0 from by
        simp [Complex.mul_re, Complex.I_re, Complex.I_im],
      Real.exp_zero, Real.sin_two_pi, mul_zero, Complex.one_im]

/-- The canonical root is primitive. -/
theorem rootExp_prim {N : ℕ} (hN : 2 ≤ N) :
    ∀ m ∈ Finset.Ico 1 N, rootExp N ^ m ≠ 1 := by
  intro m hm hc
  have hN0 : N ≠ 0 := by omega
  have hm1 : 1 ≤ m := (Finset.mem_Ico.mp hm).1
  have hmN : m < N := (Finset.mem_Ico.mp hm).2
  unfold rootExp at hc
  rw [← Complex.exp_nat_mul] at hc
  have hrew : ((m : ℂ) * (2 * Real.pi * Complex.I / (N : ℂ)) : ℂ)
      = Complex.I * ((2 * Real.pi * m / N : ℝ) : ℂ) := by
    field_simp [show ((N : ℂ)) ≠ 0 from by exact_mod_cast hN0]
    ring
  rw [hrew] at hc
  have hre : Real.cos (2 * Real.pi * m / N) = 1 := by
    have h1 := congrArg Complex.re hc
    rw [Complex.exp_re,
      show (Complex.I * ((2 * Real.pi * m / N : ℝ) : ℂ)).re = 0 from by
        rw [Complex.mul_re, Complex.I_re, Complex.I_im, Complex.ofReal_re,
          Complex.ofReal_im, zero_mul, mul_zero, sub_self],
      show (Complex.I * ((2 * Real.pi * m / N : ℝ) : ℂ)).im = 2 * Real.pi * m / N from by
        rw [Complex.mul_im, Complex.I_re, Complex.I_im, Complex.ofReal_im,
          Complex.ofReal_re, zero_mul, one_mul, zero_add],
      Real.exp_zero, one_mul, Complex.one_re] at h1
    exact h1
  rcases (Real.cos_eq_one_iff _).mp hre with ⟨n, hn⟩
  have hn_orig := hn
  have h2pi : (2 * Real.pi) ≠ 0 := by positivity
  have hNr : ((N : ℝ)) ≠ 0 := by exact_mod_cast hN0
  field_simp at hn
  have hn0 : (0 : ℤ) < n := by
    by_contra hneg
    have hle : (n : ℤ) ≤ 0 := by omega
    have hler : ((n : ℤ) : ℝ) ≤ 0 := by exact_mod_cast hle
    have hx0 : (0 : ℝ) < 2 * Real.pi * m / N :=
      div_pos (mul_pos (by positivity) (by exact_mod_cast hm1))
        (Nat.cast_pos.mpr (by omega))
    have h3 : ((n : ℤ) : ℝ) * (2 * Real.pi) ≤ 0 := by nlinarith [Real.pi_pos]
    rw [hn_orig] at h3
    linarith
  have htnr : ((n.toNat : ℕ) : ℝ) = ((n : ℤ) : ℝ) := by
    exact_mod_cast (Int.toNat_of_nonneg (by omega : (0 : ℤ) ≤ n))
  have hdiv : m = n.toNat * N := by
    have h2 := hn_orig.symm
    rw [div_eq_iff hNr, mul_assoc ((n : ℝ)) (2 * Real.pi) ((N : ℝ)),
      mul_comm (2 * Real.pi) ((N : ℝ)),
      ← mul_assoc ((n : ℝ)) ((N : ℝ)) (2 * Real.pi),
      mul_comm (2 * Real.pi) ((m : ℝ))] at h2
    have hmNr : ((m : ℕ) : ℝ) = ((n : ℤ) : ℝ) * ((N : ℕ) : ℝ) :=
      mul_right_cancel₀ h2pi h2
    have hcast : ((n.toNat * N : ℕ) : ℝ) = ((m : ℕ) : ℝ) := by
      rw [Nat.cast_mul, htnr]
      exact hmNr.symm
    exact (Nat.cast_inj.mp hcast).symm
  have hp : (0 : ℕ) < n.toNat := by
    have h1 : (1 : ℤ) ≤ n := by omega
    rw [← Int.toNat_of_nonneg (by omega : (0 : ℤ) ≤ n)] at h1
    omega
  have hle : N ≤ m := by
    calc N = N * 1 := (Nat.mul_one N).symm
      _ ≤ N * n.toNat := Nat.mul_le_mul (le_refl N) (Nat.succ_le_of_lt hp)
      _ = m := by rw [Nat.mul_comm, hdiv]
  omega

/-- At `N = 3` and `R = a/√3` the ring rate is exactly the Lagrange rate of the
parent monograph, `3Γ/(2πa²)` — the cross-link to the equilateral triangle. -/
theorem ringOmega_three_eq_lagrange (γ a : ℝ) (ha : a ≠ 0) :
    ringOmega γ (a / Real.sqrt 3) 3 = 3 * γ / (2 * Real.pi * a ^ 2) := by
  have h3 : Real.sqrt 3 ≠ 0 := by
    intro h
    have hs := Real.mul_self_sqrt (show (0 : ℝ) ≤ 3 from by norm_num)
    rw [h, mul_zero] at hs
    norm_num at hs
  rw [ringOmega]
  field_simp [h3, Real.pi_ne_zero, ha]
  ring

/-- The ring rotates forward for forward circulation. -/
theorem ring_rotation_rate_pos {γ R : ℝ} (hγ : 0 < γ) {N : ℕ} (hN : 2 ≤ N)
    (hR : 0 < R) : 0 < ringOmega γ R N := by
  rw [ringOmega]
  refine div_pos (mul_pos hγ ?_)
    (mul_pos (show (0:ℝ) < 4 * Real.pi from by positivity) (pow_pos hR 2))
  exact Nat.cast_pos.mpr (by omega)

end TheoremA

/-!
### § 2. Theorem B: the admissibility threshold of the pulsating ansatz

The symmetric H1 kinematics `r(t) = √C·(1 + ε·cos ωt)`, `ε = 1/(exp(C/π) − 1)`,
keeps every radius strictly positive exactly while `π·ln 2 < C`
(`rClosed_pos_iff`); at the threshold `C = π ln 2` the pulsation touches zero
once per period (`rClosed_touches_zero_at_threshold`).
-/

section TheoremB

variable {N : ℕ} {ω : ℝ}

/-- The pulsation depth of the Chaplygin ansatz. -/
noncomputable def eps (C : ℝ) : ℝ := 1 / (Real.exp (C / Real.pi) - 1)

/-- The pulsating radius of the ansatz at vertex `k` (the phase is common to
all vertices). -/
noncomputable def rClosed (C ω : ℝ) (N : ℕ) (t : ℝ) (k : ℕ) : ℝ :=
  Real.sqrt C * (1 + eps C * Real.cos (ω * t + 2 * Real.pi * (k : ℝ) / N))

/-- The angular phase of the ansatz. -/
noncomputable def thetaClosed (ω : ℝ) (t : ℝ) (k : ℕ) : ℝ :=
  ω * t + 2 * Real.pi * (k : ℝ) / N

/-- On the physical branch `C > 0` the depth is strictly positive. -/
theorem eps_pos (hC : 0 < C) : 0 < eps C := by
  have hgt : (1 : ℝ) < Real.exp (C / Real.pi) := by
    have h := Real.exp_lt_exp.mpr (div_pos hC Real.pi_pos)
    rw [Real.exp_zero] at h
    exact h
  exact div_pos one_pos (sub_pos.mpr hgt)

/-- The depth is below one exactly above the Chaplygin threshold `π·ln 2`. -/
theorem eps_lt_one_iff (hC : 0 < C) : eps C < 1 ↔ Real.pi * Real.log 2 < C := by
  have hgt : (1 : ℝ) < Real.exp (C / Real.pi) := by
    have h := Real.exp_lt_exp.mpr (div_pos hC Real.pi_pos)
    rw [Real.exp_zero] at h
    exact h
  have hden : (0 : ℝ) < Real.exp (C / Real.pi) - 1 := sub_pos.mpr hgt
  rw [eps, one_div]
  constructor
  · intro h
    have h1 : (1:ℝ) < Real.exp (C / Real.pi) - 1 := by
      rcases (inv_lt_one_iff).mp h with h0 | h1'
      · exact absurd h0 (by linarith)
      · exact h1'
    have h2 : (2 : ℝ) < Real.exp (C / Real.pi) := by linarith
    rw [show (2 : ℝ) = Real.exp (Real.log 2) from
        (Real.exp_log (by norm_num)).symm] at h2
    have h4 := (lt_div_iff Real.pi_pos).mp (Real.exp_lt_exp.mp h2)
    rwa [mul_comm] at h4
  · intro h
    have h4 := (lt_div_iff Real.pi_pos).mpr (by rw [mul_comm]; exact h)
    have h2 : (2 : ℝ) < Real.exp (C / Real.pi) := by
      rw [show (2 : ℝ) = Real.exp (Real.log 2) from
          (Real.exp_log (by norm_num)).symm]
      exact Real.exp_lt_exp.mpr h4
    exact (inv_lt_one_iff).mpr (Or.inr (by linarith))

/-- The threshold value of the depth is exactly one. -/
theorem eps_at_threshold : eps (Real.pi * Real.log 2) = 1 := by
  rw [eps, show (Real.pi * Real.log 2) / Real.pi = Real.log 2 from
    mul_div_cancel_left _ Real.pi_ne_zero, Real.exp_log (by norm_num)]
  norm_num

/-- Away from the threshold every radius of the ansatz stays above
`(1 − ε)·√C > 0`. -/
theorem rClosed_min (hC : 0 < C) (t : ℝ) (k : ℕ) :
    (1 - eps C) * Real.sqrt C ≤ rClosed C ω N t k := by
  rw [rClosed]
  have he : (0 : ℝ) < eps C := eps_pos hC
  have _hc : Real.cos (ω * t + 2 * Real.pi * (k : ℝ) / N) ≤ 1 := Real.cos_le_one _
  have hc2 : (-1 : ℝ) ≤ Real.cos (ω * t + 2 * Real.pi * (k : ℝ) / N) :=
    Real.neg_one_le_cos _
  have hkey : (1 - eps C) ≤ (1 : ℝ) + eps C * Real.cos (ω * t + 2 * Real.pi * (k : ℝ) / N) := by
    have hp : eps C * (-1 : ℝ) ≤ eps C * Real.cos (ω * t + 2 * Real.pi * (k : ℝ) / N) :=
      mul_le_mul_of_nonneg_left hc2 he.le
    have _hneg : eps C * (-1 : ℝ) = -eps C := by ring
    linarith
  calc (1 - eps C) * Real.sqrt C
      ≤ (1 + eps C * Real.cos (ω * t + 2 * Real.pi * (k : ℝ) / N)) * Real.sqrt C :=
        mul_le_mul_of_nonneg_right hkey (Real.sqrt_nonneg C)
    _ = Real.sqrt C * (1 + eps C * Real.cos (ω * t + 2 * Real.pi * (k : ℝ) / N)) :=
        mul_comm _ _

/-- **Theorem B.** Every radius of the pulsating ansatz stays strictly positive
exactly while `π·ln 2 < C`. -/
theorem rClosed_pos_iff (hC : 0 < C) (hω : ω ≠ 0) :
    (∀ (t : ℝ) (k : ℕ), 0 < rClosed C ω N t k) ↔ Real.pi * Real.log 2 < C := by
  constructor
  · intro h
    by_contra hle
    push_neg at hle
    have hge : (1 : ℝ) ≤ eps C := by
      by_contra hlt
      push_neg at hlt
      exact ((eps_lt_one_iff hC).mp hlt).not_le hle
    have hzero := h (Real.pi / ω) 0
    rw [rClosed,
      show ω * (Real.pi / ω) + 2 * Real.pi * ((0 : ℕ) : ℝ) / N = Real.pi from by
        rw [mul_div_cancel' Real.pi hω, Nat.cast_zero, mul_zero, zero_div, add_zero],
      Real.cos_pi] at hzero
    have hs : (0 : ℝ) < Real.sqrt C := Real.sqrt_pos.mpr hC
    have hpos : (0 : ℝ) < 1 + eps C * (-1 : ℝ) := by
      have hd := div_pos hzero hs
      rwa [mul_div_cancel_left (1 + eps C * (-1 : ℝ)) (ne_of_gt hs)] at hd
    rw [show eps C * (-1 : ℝ) = -eps C from by ring] at hpos
    linarith
  · intro h t k
    rw [rClosed]
    have he : (0 : ℝ) < eps C := eps_pos hC
    have hel : eps C < 1 := (eps_lt_one_iff hC).mpr h
    have _hc1 : Real.cos (ω * t + 2 * Real.pi * (k : ℝ) / N) ≤ 1 := Real.cos_le_one _
    have hc2 : (-1 : ℝ) ≤ Real.cos (ω * t + 2 * Real.pi * (k : ℝ) / N) :=
      Real.neg_one_le_cos _
    have hprod : eps C * (-1 : ℝ) ≤ eps C * Real.cos (ω * t + 2 * Real.pi * (k : ℝ) / N) :=
      mul_le_mul_of_nonneg_left hc2 he.le
    have hinner : (0 : ℝ) < 1 + eps C * Real.cos (ω * t + 2 * Real.pi * (k : ℝ) / N) := by
      linarith
    exact mul_pos (Real.sqrt_pos.mpr hC) hinner

/-- At the threshold `C = π ln 2` the pulsation touches zero once per period
and stays nonnegative. -/
theorem rClosed_touches_zero_at_threshold (hω : ω ≠ 0) :
    ∃ t : ℝ, rClosed (Real.pi * Real.log 2) ω N t 0 = 0
      ∧ ∀ t : ℝ, 0 ≤ rClosed (Real.pi * Real.log 2) ω N t 0 := by
  refine ⟨Real.pi / ω, ?_, ?_⟩
  · rw [rClosed,
      show ω * (Real.pi / ω) + 2 * Real.pi * ((0 : ℕ) : ℝ) / N = Real.pi from by
        rw [mul_div_cancel' Real.pi hω, Nat.cast_zero, mul_zero, zero_div, add_zero],
      Real.cos_pi, eps_at_threshold]
    ring
  · intro t
    rw [rClosed]
    have he : eps (Real.pi * Real.log 2) = 1 := eps_at_threshold
    have hc2 : (-1 : ℝ) ≤ Real.cos (ω * t + 2 * Real.pi * ((0 : ℕ) : ℝ) / N) :=
      Real.neg_one_le_cos _
    have hkey : eps (Real.pi * Real.log 2) * (-1 : ℝ)
        ≤ eps (Real.pi * Real.log 2) * Real.cos (ω * t + 2 * Real.pi * ((0 : ℕ) : ℝ) / N) := by
      refine mul_le_mul_of_nonneg_left hc2 ?_
      rw [he]
      norm_num
    exact mul_nonneg (Real.sqrt_nonneg _) (by linarith)

end TheoremB

/-!
### § 3. Lemma C: no pulsating ring can ride the Kirchhoff field

If the uniformly rotating pulsating configuration of the H1 kinematics
satisfies the point-vortex ODE, its pulsation is stationary
(`lemmaC_pulsation`, `lemmaC_radius_constant`); hence a nontrivial
Chaplygin pulsation is obstructed in the N-vortex layer
(`lemmaC_H1_reduction`).  On the exact ring the radial velocity vanishes
(`ring_radial_zero`).
-/

section LemmaC

variable {γ : ℝ} {N : ℕ}

/-- The radial component of a velocity at a point (up to the positive factor
`|z|`; its vanishing is the exact `ṙ = 0` condition). -/
noncomputable def radialForm (v z : ℂ) : ℝ := (v * star z).re

/-- The pulsating-ring kinematics at vertex `k`: common pulsation `r`, common
rotation `θ`, canonical root phases. -/
noncomputable def pulsPos (r θ : ℝ → ℝ) (N : ℕ) (t : ℝ) (k : ℕ) : ℂ :=
  (r t) * Complex.exp (Complex.I * (θ t + 2 * Real.pi * (k : ℝ) / N))

/-- On the exact ring the radial velocity vanishes identically. -/
theorem ring_radial_zero (γ : ℝ) (N : ℕ) (hN : 2 ≤ N) (R : ℝ) (hR : R ≠ 0) (ζ : ℂ)
    (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) {k : ℕ} (hk : k < N) :
    radialForm (kirchhoff γ (ringPos R ζ) N k) (ringPos R ζ k) = 0 := by
  rw [ring_velocity γ N hN R hR ζ h1 hprim hk, radialForm]
  simp only [Complex.star_def, Complex.conj_re, Complex.conj_im, Complex.mul_re,
    Complex.mul_im, Complex.I_re, Complex.I_im, Complex.ofReal_im,
    Complex.ofReal_re]
  ring

/-- **Lemma C (pulsation obstruction).** If the uniformly rotating pulsating
configuration satisfies the point-vortex ODE at vertex `0`, its pulsation is
stationary: `r' = 0`. -/
theorem lemmaC_pulsation {γ : ℝ} {N : ℕ} (hN : 2 ≤ N) {r θ : ℝ → ℝ}
    (hr : Differentiable ℝ r) (hθ : Differentiable ℝ θ)
    (hODE : ∀ t : ℝ, HasDerivAt (fun s => pulsPos r θ N s 0)
      (kirchhoff γ (fun k => pulsPos r θ N t k) N 0) t)
    (t : ℝ) : deriv r t = 0 := by
  have hN0 : N ≠ 0 := by omega
  have hu : ∀ u : ℝ, Complex.normSq (Complex.exp (Complex.I * θ u)) = 1 :=
    fun u => normSq_exp_I_mul (θ u)
  have hconf : ∀ u : ℝ, (fun k => pulsPos r θ N u k)
      = fun k => Complex.exp (Complex.I * θ u) * ringPos (r u) (rootExp N) k := by
    intro u
    funext k
    unfold pulsPos ringPos rootExp
    rw [mul_add, Complex.exp_add, ← Complex.exp_nat_mul,
      show ((k : ℂ) * (2 * Real.pi * Complex.I / (N : ℂ)) : ℂ)
        = Complex.I * (2 * Real.pi * (k : ℝ) / N) from by
        have _hNc : ((N : ℝ) : ℂ) ≠ 0 := by exact_mod_cast hN0
        field_simp
        ring]
    ring
  have hfield : ∀ u : ℝ, kirchhoff γ (fun k => pulsPos r θ N u k) N 0
      = Complex.I * ((ringOmega γ (r u) N : ℝ) : ℂ) * pulsPos r θ N u 0 := by
    intro u
    rcases eq_or_ne (r u) 0 with hz | hz
    · simp only [pulsPos, hz, Complex.ofReal_zero]
      simp [kirchhoff, ringOmega, mul_zero, zero_mul, zero_div,
        Complex.normSq_zero]
    · rw [hconf u, kirchhoff_smul γ (hu u) 0,
        ring_velocity γ N hN (r u) hz (rootExp N) (rootExp_pow hN0) (rootExp_prim hN)
          (k := 0) (by omega)]
      simp only [pulsPos, ringPos, pow_zero, mul_one, Nat.cast_zero,
        Complex.ofReal_zero, mul_zero, zero_div, add_zero]
      ring
  -- the derivative of the 0-th pulsating coordinate
  set cE : ℂ := Complex.exp (Complex.I * θ t) with hcE
  have hE : HasDerivAt (fun s => Complex.exp (Complex.I * θ s))
      (cE * (Complex.I * deriv θ t)) t := by
    have hinner : HasDerivAt (fun s => Complex.I * ((θ s : ℝ) : ℂ))
        (Complex.I * ((deriv θ t : ℝ) : ℂ)) t :=
      HasDerivAt.const_mul Complex.I
        ((DifferentiableAt.hasDerivAt (hθ t)).ofReal_comp)
    exact HasDerivAt.comp (x := t)
      (h := fun s => Complex.I * ((θ s : ℝ) : ℂ))
      (Complex.hasDerivAt_exp (Complex.I * ((θ t : ℝ) : ℂ))) hinner
  have hpuls : HasDerivAt (fun s => pulsPos r θ N s 0)
      ((((deriv r t : ℝ) : ℂ) + Complex.I * ((r t * deriv θ t : ℝ) : ℂ)) * cE) t := by
    have hfun : (fun s => pulsPos r θ N s 0)
        = fun s => (r s) * Complex.exp (Complex.I * θ s) := by
      funext s
      unfold pulsPos
      simp only [Nat.cast_zero, Complex.ofReal_zero, mul_zero, zero_div, add_zero]
    rw [hfun]
    simpa [hcE, add_mul, mul_add, mul_comm, mul_left_comm, mul_assoc,
      Complex.ofReal_mul] using
      HasDerivAt.mul ((hr t).hasDerivAt.ofReal_comp) hE
  have heq := HasDerivAt.unique (hODE t) hpuls
  have hp0 : pulsPos r θ N t 0 = (r t) * cE := by
    unfold pulsPos
    simp only [Nat.cast_zero, Complex.ofReal_zero, mul_zero, zero_div, add_zero]
  rw [hfield t, hp0] at heq
  have hEc : cE * star cE = 1 := by
    show cE * (starRingEnd ℂ) cE = 1
    rw [hcE, Complex.mul_conj, normSq_exp_I_mul, Complex.ofReal_one]
  have hstep : Complex.I * ((ringOmega γ (r t) N : ℝ) : ℂ) * ((r t) * cE) * star cE
      = (((deriv r t : ℝ) : ℂ) + Complex.I * ((r t * deriv θ t : ℝ) : ℂ)) * cE
        * star cE :=
    congrArg (fun x : ℂ => x * star cE) heq
  rw [mul_assoc (((deriv r t : ℝ) : ℂ) + Complex.I * ((r t * deriv θ t : ℝ) : ℂ)) cE
      (star cE), hEc, mul_one,
    mul_assoc (Complex.I * ((ringOmega γ (r t) N : ℝ) : ℂ)) (((r t : ℝ) : ℂ) * cE)
      (star cE), mul_assoc ((r t : ℝ) : ℂ) cE (star cE), hEc, mul_one] at hstep
  have hre := congrArg Complex.re hstep
  simp only [Complex.add_re, Complex.mul_re, Complex.I_re, Complex.I_im,
    Complex.ofReal_im, Complex.ofReal_re] at hre
  linarith

/-- A stationary pulsation is a constant radius. -/
theorem lemmaC_radius_constant {r : ℝ → ℝ} (hr : Differentiable ℝ r)
    (h0 : ∀ t : ℝ, deriv r t = 0) (s t : ℝ) : r s = r t :=
  is_const_of_deriv_eq_zero hr h0 s t

/-- **Lemma C, corollary (H1 reduction).** A nontrivial Chaplygin pulsation of
the pulsating-ring kinematics is not a Kirchhoff solution. -/
theorem lemmaC_H1_reduction {C ω : ℝ} (hC : 0 < C) (hω : ω ≠ 0) (hε : eps C ≠ 0)
    (hN : 2 ≤ N) :
    ¬ ∀ t : ℝ, HasDerivAt
        (fun s => pulsPos (fun u => rClosed C ω N u 0) (fun u => ω * u) N s 0)
        (kirchhoff γ (fun k => pulsPos (fun u => rClosed C ω N u 0) (fun u => ω * u) N t k)
          N 0) t := by
  intro hODE
  have hrC : Differentiable ℝ (fun u => rClosed C ω N u 0) := by
    unfold rClosed
    exact (differentiable_const _).mul
      ((differentiable_const _).add ((differentiable_const _).mul
        (Real.differentiable_cos.comp
          (((differentiable_const ω).mul differentiable_id).add (differentiable_const _)))))
  have hθC : Differentiable ℝ (fun u => ω * u) :=
    (differentiable_const ω).mul differentiable_id
  have hstat := lemmaC_pulsation hN hrC hθC hODE
  have hconst := lemmaC_radius_constant hrC hstat 0 (Real.pi / ω)
  simp only [rClosed, Real.cos_zero, Real.cos_pi,
    show (ω * 0 + 2 * Real.pi * ((0 : ℕ) : ℝ) / N : ℝ) = 0 from by norm_num,
    show (ω * (Real.pi / ω) + 2 * Real.pi * ((0 : ℕ) : ℝ) / N : ℝ) = Real.pi from
      by field_simp [hω, mul_comm]] at hconst
  have hs : Real.sqrt C ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr hC)
  refine hε ?_
  have hxy := mul_left_cancel₀ hs hconst
  linarith

end LemmaC

/-!
### § 4. Lemma D: the cycle-averaged Kirchhoff rate of the pulsation

The cycle average of the ring rate along the symmetric pulsation is
independent of the pulsation frequency (`lemmaD_omega_independent`) and
equals `ω_N/((1−ε²)·√(1−ε²))` (`lemmaD_bridge`), certified by the exact
Poisson integral `∫₀^{2π} dφ/(1+ε·cos φ) = 2π/√(1−ε²)` (`poisson_integral`)
and its squared companion (`poisson_sq`) — both in closed form.
-/

section LemmaD

/-- The pulsating radius of the symmetric H1 kinematics. -/
noncomputable def pulsRadius (R ε ω t : ℝ) : ℝ := R * (1 + ε * Real.cos (ω * t))

/-- The cycle-averaged Kirchhoff rate over one pulsation period (Lemma D). -/
noncomputable def avgKinFreq (γ R ε ω : ℝ) (N : ℕ) : ℝ :=
  (ω / (2 * Real.pi)) * ∫ t in (0 : ℝ)..(2 * Real.pi / ω),
    ringOmega γ (pulsRadius R ε ω t) N

/-- The ring rate scales as the inverse square of the radius. -/
theorem ringOmega_smul_radius {γ R : ℝ} (_hR : R ≠ 0) {u : ℝ} (_hu : u ≠ 0) (N : ℕ) :
    ringOmega γ (R * u) N = ringOmega γ R N / u ^ 2 := by
  rw [ringOmega, ringOmega, mul_pow]
  ring

/-- **Lemma D, frequency independence.** The cycle average factors into the
ring rate times an ε-only shape factor. -/
theorem lemmaD_omega_independent {γ R ε ω : ℝ} (hω : ω ≠ 0) (hR : R ≠ 0)
    (hε : ε ^ 2 < 1) (N : ℕ) :
    avgKinFreq γ R ε ω N
      = ringOmega γ R N * ((1 / (2 * Real.pi)) * ∫ φ in (0 : ℝ)..(2 * Real.pi),
        ((1 + ε * Real.cos φ) ^ 2)⁻¹) := by
  have habs : |ε| < 1 := by
    by_contra hge
    push_neg at hge
    have h1 : |ε| * |ε| ≥ 1 := by nlinarith [hge, abs_nonneg ε]
    rw [← pow_two] at h1
    rw [sq_abs] at h1
    exact absurd hε (not_lt.mpr h1)
  have huni : ∀ φ : ℝ, (1 + ε * Real.cos φ) ≠ 0 := by
    intro φ h0
    have hcabs : |Real.cos φ| ≤ 1 := abs_le.mpr ⟨Real.neg_one_le_cos _, Real.cos_le_one _⟩
    have hprod : |ε * Real.cos φ| < 1 := by
      rw [abs_mul]
      calc |ε| * |Real.cos φ| ≤ |ε| * 1 :=
            mul_le_mul_of_nonneg_left hcabs (abs_nonneg ε)
        _ = |ε| := mul_one _
        _ < 1 := habs
    have hneg : ε * Real.cos φ = -1 := by linarith
    rw [hneg, abs_neg, abs_one] at hprod
    norm_num at hprod
  rw [avgKinFreq]
  have hsub : (∫ t in (0 : ℝ)..(2 * Real.pi / ω), ringOmega γ (pulsRadius R ε ω t) N : ℝ)
      = ∫ t in (0 : ℝ)..(2 * Real.pi / ω),
        (fun φ => ringOmega γ (R * (1 + ε * Real.cos φ)) N) (ω * t) := rfl
  rw [hsub,
    integral_comp_mul_left (fun x => ringOmega γ (R * (1 + ε * Real.cos x)) N) hω,
    mul_zero, smul_eq_mul,
    show ((ω : ℝ) * (2 * Real.pi / ω)) = 2 * Real.pi from (by field_simp; ring)]
  rw [integral_congr (show Set.EqOn (fun φ => ringOmega γ (R * (1 + ε * Real.cos φ)) N)
      (fun φ => ringOmega γ R N / (1 + ε * Real.cos φ) ^ 2)
      (Set.uIcc 0 (2 * Real.pi)) from by
    intro φ _
    exact ringOmega_smul_radius hR (huni φ) N)]
  simp only [div_eq_mul_inv]
  rw [integral_const_mul]
  field_simp
  ring

/-- A nonnegative square below one has a root below one. -/
private theorem abs_lt_one_of_sq_lt_one {ε : ℝ} (hε : ε ^ 2 < 1) : |ε| < 1 := by
  by_contra hge
  push_neg at hge
  have h1 : |ε| * |ε| ≥ 1 := by nlinarith [hge, abs_nonneg ε]
  rw [← pow_two] at h1
  rw [sq_abs] at h1
  exact absurd hε (not_lt.mpr h1)

/-- A positive real has a positive square root. -/
private theorem sqrt_pos' {a : ℝ} (h : 0 < a) : 0 < Real.sqrt a :=
  (Real.sqrt_pos).mpr h

/-! #### The Poisson integral. -/

/-- The half-angle form of the Poisson antiderivative. -/
noncomputable def poissonG (ε φ : ℝ) : ℝ :=
  (2 / Real.sqrt (1 - ε ^ 2)) * Real.arctan
    (Real.sqrt ((1 - ε) / (1 + ε)) * Real.tan (φ / 2))

/-- The half-angle identity for the cosine. -/
private theorem cos_half_tan {φ : ℝ} (hφ : φ ∈ Set.Ioo (-(Real.pi)) Real.pi) :
    Real.cos φ = (1 - Real.tan (φ / 2) ^ 2) / (1 + Real.tan (φ / 2) ^ 2) := by
  have hφlo : -(Real.pi / 2) < φ / 2 := by linarith [hφ.1]
  have hφhi : φ / 2 < Real.pi / 2 := by linarith [hφ.2]
  have hcos0 : Real.cos (φ / 2) ≠ 0 :=
    (Real.cos_pos_of_mem_Ioo ⟨hφlo, hφhi⟩).ne'
  have hsq : (1 : ℝ) + Real.tan (φ / 2) ^ 2 = 1 / Real.cos (φ / 2) ^ 2 := by
    rw [Real.tan_eq_sin_div_cos, div_pow]
    field_simp [hcos0, Real.sin_sq_add_cos_sq (φ / 2)]
  have hnum : (1 : ℝ) - Real.tan (φ / 2) ^ 2
      = (Real.cos (φ / 2) ^ 2 - Real.sin (φ / 2) ^ 2) / Real.cos (φ / 2) ^ 2 := by
    have ht2 : Real.tan (φ / 2) ^ 2 = Real.sin (φ / 2) ^ 2 / Real.cos (φ / 2) ^ 2 := by
      rw [Real.tan_eq_sin_div_cos, div_pow]
    rw [ht2]
    field_simp [hcos0]
  have hφ2 : Real.cos φ = Real.cos (2 * (φ / 2)) := by
    rw [show ((2 : ℝ) * (φ / 2)) = φ from by ring]
  rw [hφ2, Real.cos_two_mul', hnum, hsq]
  field_simp [hcos0]

/-- The Poisson denominator never vanishes for `ε² < 1`. -/
private theorem one_add_eps_cos_ne_zero {ε : ℝ} (hε : ε ^ 2 < 1) (φ : ℝ) :
    (1 + ε * Real.cos φ) ≠ 0 := by
  have habs := abs_lt_one_of_sq_lt_one hε
  intro h0
  have hcabs : |Real.cos φ| ≤ 1 := abs_le.mpr ⟨Real.neg_one_le_cos _, Real.cos_le_one _⟩
  have hprod : |ε * Real.cos φ| < 1 := by
    rw [abs_mul]
    calc |ε| * |Real.cos φ| ≤ |ε| * 1 := mul_le_mul_of_nonneg_left hcabs (abs_nonneg ε)
      _ = |ε| := mul_one _
      _ < 1 := habs
  have hneg : ε * Real.cos φ = -1 := by linarith
  rw [hneg, abs_neg, abs_one] at hprod
  norm_num at hprod

/-- The Poisson integrand is continuous. -/
private theorem poisson_cont {ε : ℝ} (hε : ε ^ 2 < 1) :
    Continuous fun φ : ℝ => 1 / (1 + ε * Real.cos φ) :=
  continuous_const.div
    (Continuous.add continuous_const
      (Continuous.mul continuous_const Real.continuous_cos))
    (one_add_eps_cos_ne_zero hε)

/-- The half-angle antiderivative pair: `arctan k + arctan(k⁻¹) = π/2`. -/
private theorem arctan_add_arctan_inv {k : ℝ} (hk : 0 < k) :
    Real.arctan k + Real.arctan (k⁻¹) = Real.pi / 2 := by
  have ha := Real.arctan_mem_Ioo k
  have _hb := Real.arctan_mem_Ioo (k⁻¹)
  have hapos : (0 : ℝ) < Real.arctan k := by
    have h0 := Real.arctan_strictMono (show (0:ℝ) < k from hk)
    rwa [Real.arctan_zero] at h0
  have _hki : (0 : ℝ) < k⁻¹ := inv_pos.mpr hk
  have hbin : Real.pi / 2 - Real.arctan k ∈ Set.Ioo (-(Real.pi / 2)) (Real.pi / 2) :=
    ⟨by linarith [ha.2], by linarith [hapos]⟩
  have hαtan : Real.tan (Real.arctan k) = k := by
    have h1 := Real.arctan_tan ha.1 ha.2
    have h2 : Real.arctan (Real.tan (Real.arctan k)) = Real.arctan k := by rw [h1]
    exact Real.arctan_injective h2
  have _hs0 : Real.sin (Real.arctan k) ≠ 0 :=
    ne_of_gt (Real.sin_pos_of_mem_Ioo ⟨hapos, lt_trans ha.2 (by linarith [Real.pi_pos])⟩)
  have htan : Real.tan (Real.pi / 2 - Real.arctan k) = k⁻¹ := by
    rw [Real.tan_pi_div_two_sub, hαtan]
  have hbeq : Real.arctan (k⁻¹) = Real.pi / 2 - Real.arctan k := by
    have h1 := Real.arctan_tan hbin.1 hbin.2
    rw [htan] at h1
    exact h1
  rw [hbeq]
  ring

/-- On `(-π, π)` the half-angle antiderivative differentiates to the Poisson
integrand. -/
private theorem hasDerivAt_poissonG {ε : ℝ} (hε : ε ^ 2 < 1) {φ : ℝ}
    (hφ : φ ∈ Set.Ioo (-(Real.pi)) Real.pi) :
    HasDerivAt (poissonG ε) (1 / (1 + ε * Real.cos φ)) φ := by
  have habs := abs_lt_one_of_sq_lt_one hε
  have hpe : (0 : ℝ) < 1 + ε := by linarith [(abs_lt.mp habs).1]
  have hme : (0 : ℝ) < 1 - ε := by linarith [(abs_lt.mp habs).2]
  have _hc : (0 : ℝ) < 1 - ε ^ 2 := by linarith
  have hk0 : 0 < Real.sqrt ((1 - ε) / (1 + ε)) := sqrt_pos' (div_pos hme hpe)
  have hcos0 : Real.cos (φ / 2) ≠ 0 :=
    (Real.cos_pos_of_mem_Ioo ⟨by linarith [hφ.1], by linarith [hφ.2]⟩).ne'
  have hksq : Real.sqrt ((1 - ε) / (1 + ε)) * (1 + ε) = Real.sqrt (1 - ε ^ 2) := by
    have h1 : Real.sqrt ((1 - ε) / (1 + ε)) * Real.sqrt ((1 + ε) * (1 + ε))
        = Real.sqrt (1 - ε ^ 2) := by
      rw [← Real.sqrt_mul (div_nonneg hme.le hpe.le)]
      congr 1
      field_simp [hpe.ne']
      ring
    rw [← h1, Real.sqrt_mul_self (by positivity)]
  have hsq : (1 : ℝ) + Real.tan (φ / 2) ^ 2 = 1 / Real.cos (φ / 2) ^ 2 := by
    rw [Real.tan_eq_sin_div_cos]
    field_simp
  have hhalf : HasDerivAt (fun x : ℝ => Real.tan (x / 2))
      ((1 / Real.cos (φ / 2) ^ 2) * (1 / 2)) φ :=
    (Real.hasDerivAt_tan hcos0).comp (x := φ)
      (HasDerivAt.div_const (hasDerivAt_id φ) 2)
  have hcomp : HasDerivAt (fun x : ℝ =>
      Real.arctan (Real.sqrt ((1 - ε) / (1 + ε)) * Real.tan (x / 2)))
      (2⁻¹ * (Real.sqrt ((1 - ε) / (1 + ε))
        * ((1 + Real.tan (φ / 2) ^ 2)
          * (1 + Real.sqrt ((1 - ε) / (1 + ε)) ^ 2 * Real.tan (φ / 2) ^ 2)⁻¹))) φ := by
    have hsq' : (Real.cos (φ / 2) ^ 2)⁻¹ = 1 + Real.tan (φ / 2) ^ 2 := by
      rw [inv_eq_one_div]; exact hsq.symm
    simpa [mul_comm, mul_left_comm, mul_assoc, mul_pow, hsq', Function.comp_def] using
      (Real.hasDerivAt_arctan
        (Real.sqrt ((1 - ε) / (1 + ε)) * Real.tan (φ / 2))).comp (x := φ)
        (HasDerivAt.const_mul (Real.sqrt ((1 - ε) / (1 + ε))) hhalf)
  have h1 := HasDerivAt.const_mul (2 / Real.sqrt (1 - ε ^ 2)) hcomp
  rw [show ((2 / Real.sqrt (1 - ε ^ 2)) * (2⁻¹ * (Real.sqrt ((1 - ε) / (1 + ε))
        * ((1 + Real.tan (φ / 2) ^ 2)
          * (1 + Real.sqrt ((1 - ε) / (1 + ε)) ^ 2 * Real.tan (φ / 2) ^ 2)⁻¹))))
      = 1 / (1 + ε * Real.cos φ) from by
    rw [← hksq, eq_div_iff (one_add_eps_cos_ne_zero hε φ), cos_half_tan hφ,
      show Real.sqrt ((1 - ε) / (1 + ε)) ^ 2 = (1 - ε) / (1 + ε) from
        Real.sq_sqrt (div_nonneg hme.le hpe.le)]
    field_simp [hk0.ne', hpe.ne', hme.ne']
    ring] at h1
  exact h1

/-- The closed FTC on `[0, b]` for `0 ≤ b < π`. -/
private theorem poisson_ftc {ε : ℝ} (hε : ε ^ 2 < 1) {b : ℝ} (hb : b < Real.pi)
    (hb0 : 0 ≤ b) :
    ∫ φ in (0 : ℝ)..b, 1 / (1 + ε * Real.cos φ)
      = poissonG ε b - poissonG ε 0 := by
  refine integral_eq_sub_of_hasDerivAt (fun x hx => ?_)
    (Continuous.intervalIntegrable (poisson_cont hε) _ _)
  rw [Set.mem_uIcc] at hx
  have hxIoo : x ∈ Set.Ioo (-(Real.pi)) Real.pi := by
    constructor
    · rcases hx with hx | hx
      · linarith [hx.1, Real.pi_pos]
      · linarith [hx.2, Real.pi_pos]
    · rcases hx with hx | hx
      · linarith [hx.2, hb]
      · linarith [hx.2, hb]
  exact hasDerivAt_poissonG hε hxIoo

/-- The square of a negated real equals the square. -/
private theorem sq_neg (a : ℝ) : (-a) ^ 2 = a ^ 2 := by ring

/-- The half-period Poisson integral over `[0, π]`. -/
private theorem poisson_half {ε : ℝ} (hε : ε ^ 2 < 1) :
    ∫ φ in (0 : ℝ)..Real.pi, 1 / (1 + ε * Real.cos φ)
      = Real.pi / Real.sqrt (1 - ε ^ 2) := by
  have habs := abs_lt_one_of_sq_lt_one hε
  have hpe : (0 : ℝ) < 1 + ε := by linarith [(abs_lt.mp habs).1]
  have hme : (0 : ℝ) < 1 - ε := by linarith [(abs_lt.mp habs).2]
  have hc : (0 : ℝ) < 1 - ε ^ 2 := by linarith
  have hkpos : 0 < Real.sqrt ((1 - ε) / (1 + ε)) := sqrt_pos' (div_pos hme hpe)
  have hsplit := (integral_add_adjacent_intervals
      (Continuous.intervalIntegrable (μ := volume) (poisson_cont hε) 0 (Real.pi / 2))
      (Continuous.intervalIntegrable (μ := volume) (poisson_cont hε) (Real.pi / 2) Real.pi)).symm
  -- transport the second half onto `[0, π/2]` with `ε ↦ −ε`
  have htrans : (∫ φ in (Real.pi / 2)..Real.pi, 1 / (1 + ε * Real.cos φ) : ℝ)
      = ∫ φ in (0 : ℝ)..(Real.pi / 2), 1 / (1 - ε * Real.cos φ) := by
    rw [integral_congr (show Set.EqOn (fun x => 1 / (1 + ε * Real.cos x))
        (fun x => 1 / (1 - ε * Real.cos (x - Real.pi)))
        (Set.uIcc (Real.pi / 2) Real.pi) from by
      intro x _
      show 1 / (1 + ε * Real.cos x) = 1 / (1 - ε * Real.cos (x - Real.pi))
      rw [show Real.cos (x - Real.pi) = -Real.cos x from by
        rw [Real.cos_sub, Real.cos_pi, Real.sin_pi]
        ring]
      ring),
      integral_comp_sub_right (fun y => 1 / (1 - ε * Real.cos y)) Real.pi,
      show (Real.pi / 2 - Real.pi) = (-1 : ℝ) * (Real.pi / 2) from by ring,
      show (Real.pi - Real.pi) = (-1 : ℝ) * 0 from by ring]
    rw [integral_congr (show Set.EqOn (fun x => 1 / (1 - ε * Real.cos x))
      (fun x => (fun w => 1 / (1 - ε * Real.cos w)) ((-1) * x))
      (Set.uIcc ((-1 : ℝ) * (Real.pi / 2)) ((-1 : ℝ) * 0)) from by
      intro x _
      show 1 / (1 - ε * Real.cos x) = 1 / (1 - ε * Real.cos ((-1 : ℝ) * x))
      rw [show ((-1 : ℝ) * x) = -x from by ring, Real.cos_neg])]
    rw [integral_comp_mul_left (c := (-1 : ℝ))
      (fun y => 1 / (1 - ε * Real.cos y)) (by norm_num)]
    rw [integral_symm]
    simp only [smul_eq_mul, inv_neg_one, neg_one_mul, neg_neg]
  -- add the two halves
  rw [hsplit, htrans,
    show (∫ φ in (0 : ℝ)..(Real.pi / 2), 1 / (1 - ε * Real.cos φ))
      = ∫ φ in (0 : ℝ)..(Real.pi / 2), 1 / (1 + (-ε) * Real.cos φ) from by
      simp only [show ∀ φ : ℝ, (1 : ℝ) - ε * Real.cos φ
        = 1 + (-ε) * Real.cos φ from fun φ => by ring],
    (integral_add (Continuous.intervalIntegrable (poisson_cont hε) _ _)
      (Continuous.intervalIntegrable (poisson_cont
        (by rwa [sq_neg] : (-ε : ℝ) ^ 2 < 1)) _ _)).symm]
  -- the combined antiderivative over `[0, π/2]`
  have hcombo : ∫ φ in (0 : ℝ)..(Real.pi / 2),
      1 / (1 + ε * Real.cos φ) + 1 / (1 + (-ε) * Real.cos φ)
      = poissonG ε (Real.pi / 2) + poissonG (-ε) (Real.pi / 2)
        - (poissonG ε 0 + poissonG (-ε) 0) := by
    refine integral_eq_sub_of_hasDerivAt
      (f := fun x => poissonG ε x + poissonG (-ε) x) (fun x hx => ?_)
      (Continuous.intervalIntegrable
        ((poisson_cont hε).add
          (poisson_cont (by rwa [sq_neg] : (-ε : ℝ) ^ 2 < 1))) _ _)
    rw [Set.mem_uIcc] at hx
    have hxIoo : x ∈ Set.Ioo (-(Real.pi)) Real.pi := by
      constructor
      · rcases hx with hx | hx
        · linarith [hx.1, Real.pi_pos]
        · linarith [hx.1, hx.2, Real.pi_pos]
      · rcases hx with hx | hx
        · linarith [hx.2, Real.pi_pos]
        · linarith [hx.2, Real.pi_pos]
    exact HasDerivAt.add (hasDerivAt_poissonG hε hxIoo)
      (hasDerivAt_poissonG (by rwa [sq_neg] : (-ε : ℝ) ^ 2 < 1) hxIoo)
  have hz : poissonG ε 0 = 0 ∧ poissonG (-ε) 0 = 0 := by
    unfold poissonG
    constructor <;> rw [show (0 : ℝ) / 2 = 0 from by ring, Real.tan_zero, mul_zero,
      Real.arctan_zero, mul_zero]
  have hk2 : Real.sqrt ((1 - -ε) / (1 + -ε)) = (Real.sqrt ((1 - ε) / (1 + ε)))⁻¹ := by
    have h1 : ((1 - ε) / (1 + ε)) * ((1 + ε) / (1 - ε)) = 1 := by
      rw [div_mul_div_comm, mul_comm (1 - ε) (1 + ε),
        div_self (mul_ne_zero hpe.ne' hme.ne')]
    have h2 : Real.sqrt ((1 - ε) / (1 + ε)) * Real.sqrt ((1 - -ε) / (1 + -ε)) = 1 := by
      rw [show ((1 - -ε : ℝ)) = 1 + ε from by ring, show ((1 + -ε : ℝ)) = 1 - ε from by ring,
        ← Real.sqrt_mul (div_nonneg hme.le hpe.le), h1, Real.sqrt_one]
    exact eq_inv_of_mul_eq_one_left
      (show Real.sqrt ((1 - -ε) / (1 + -ε)) * Real.sqrt ((1 - ε) / (1 + ε)) = 1 from by
        rw [mul_comm]; exact h2)
  have hpair : poissonG ε (Real.pi / 2) + poissonG (-ε) (Real.pi / 2)
      = (2 / Real.sqrt (1 - ε ^ 2)) * (Real.pi / 2) := by
    unfold poissonG
    have hta : Real.tan (Real.pi / 2 / 2) = 1 := by
      rw [show (Real.pi / 2 / 2 : ℝ) = Real.pi / 4 from by ring, Real.tan_pi_div_four]
    rw [hta, mul_one, sq_neg ε, hk2, mul_one, ← mul_add,
      Real.arctan_inv_of_pos hkpos]
    congr 1
    ring
  rw [hcombo, hz.1, hz.2, add_zero, sub_zero, hpair]
  have hsq0 : Real.sqrt (1 - ε ^ 2) ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr hc)
  field_simp [hc.ne', hsq0]
  try ring

/-- **The Poisson integral.** `∫₀^{2π} dφ/(1+ε·cos φ) = 2π/√(1−ε²)`, proven in
closed form by the half-angle antiderivative — no numerical quadrature. -/
theorem poisson_integral {ε : ℝ} (hε : ε ^ 2 < 1) :
    ∫ φ in (0 : ℝ)..(2 * Real.pi), 1 / (1 + ε * Real.cos φ)
      = 2 * Real.pi / Real.sqrt (1 - ε ^ 2) := by
  have hshift : (∫ φ in Real.pi..(2 * Real.pi), 1 / (1 + ε * Real.cos φ) : ℝ)
      = ∫ φ in (0 : ℝ)..Real.pi, 1 / (1 - ε * Real.cos φ) := by
    rw [integral_congr (show Set.EqOn (fun x => 1 / (1 + ε * Real.cos x))
        (fun x => (fun y => 1 / (1 - ε * Real.cos y)) (x - Real.pi))
        (Set.uIcc Real.pi (2 * Real.pi)) from by
      intro x _
      show 1 / (1 + ε * Real.cos x) = 1 / (1 - ε * Real.cos (x - Real.pi))
      rw [Real.cos_sub, Real.cos_pi, Real.sin_pi]
      ring),
      integral_comp_sub_right (fun y => 1 / (1 - ε * Real.cos y)) Real.pi,
      show (Real.pi - Real.pi : ℝ) = 0 from by ring,
      show (2 * Real.pi - Real.pi) = Real.pi from by ring]
  have hsplit := (integral_add_adjacent_intervals
      (Continuous.intervalIntegrable (μ := volume) (poisson_cont hε) 0 Real.pi)
      (Continuous.intervalIntegrable (μ := volume) (poisson_cont hε) Real.pi (2 * Real.pi))).symm
  rw [hsplit, hshift, poisson_half hε,
    show (∫ φ in (0 : ℝ)..Real.pi, 1 / (1 - ε * Real.cos φ))
      = ∫ φ in (0 : ℝ)..Real.pi, 1 / (1 + (-ε) * Real.cos φ) from by
      simp only [show ∀ φ : ℝ, (1 : ℝ) - ε * Real.cos φ
        = 1 + (-ε) * Real.cos φ from fun φ => by ring],
    poisson_half (by rwa [sq_neg] : (-ε : ℝ) ^ 2 < 1)]
  field_simp
  ring

/-- The squared companion of the Poisson integral, via the antiderivative
`g = sin φ/(1+ε·cos φ)`: `∫ g' = 0` on the closed cycle. -/
theorem poisson_sq {ε : ℝ} (hε : ε ^ 2 < 1) :
    ∫ φ in (0 : ℝ)..(2 * Real.pi), ((1 + ε * Real.cos φ) ^ 2)⁻¹
      = 2 * Real.pi / ((1 - ε ^ 2) * Real.sqrt (1 - ε ^ 2)) := by
  have hc : (0 : ℝ) < 1 - ε ^ 2 := by linarith
  have hd0 : ∀ φ : ℝ, ((1 + ε * Real.cos φ) ^ 2)⁻¹
      = (1 / (1 - ε ^ 2)) * (1 / (1 + ε * Real.cos φ)
        - ε * ((Real.cos φ + ε) / (1 + ε * Real.cos φ) ^ 2)) := by
    intro φ
    field_simp [one_add_eps_cos_ne_zero hε φ, hc.ne']
    ring
  have hden : ∀ x : ℝ, (1 + ε * Real.cos x) ^ 2 ≠ 0 :=
    fun x => pow_ne_zero 2 (one_add_eps_cos_ne_zero hε x)
  have hnum : Continuous fun x : ℝ => (Real.cos x + ε) / (1 + ε * Real.cos x) ^ 2 :=
    Continuous.div (Continuous.add Real.continuous_cos continuous_const)
      (Continuous.pow (Continuous.add continuous_const
        (Continuous.mul continuous_const Real.continuous_cos)) 2) hden
  set g : ℝ → ℝ := fun φ => Real.sin φ / (1 + ε * Real.cos φ) with hgdef
  have hg : ∀ φ : ℝ, HasDerivAt g ((Real.cos φ + ε) / (1 + ε * Real.cos φ) ^ 2) φ := by
    intro φ
    rw [hgdef]
    have hd := HasDerivAt.div (Real.hasDerivAt_sin φ)
      ((hasDerivAt_const φ (1 : ℝ)).add
        (HasDerivAt.const_mul ε (Real.hasDerivAt_cos φ))) (one_add_eps_cos_ne_zero hε φ)
    have h1 : Real.sin φ ^ 2 = 1 - Real.cos φ ^ 2 := by
      linarith [Real.sin_sq_add_cos_sq φ]
    have h2 : Real.cos φ * (1 + ε * Real.cos φ) + Real.sin φ * (ε * Real.sin φ)
        = Real.cos φ + ε := by
      rw [mul_comm (Real.sin φ) (ε * Real.sin φ),
        mul_assoc ε (Real.sin φ) (Real.sin φ),
        ← pow_two (Real.sin φ), h1]
      ring
    simpa [mul_neg, neg_neg, h2] using hd
  rw [integral_congr (show Set.EqOn (fun φ => ((1 + ε * Real.cos φ) ^ 2)⁻¹)
      (fun φ => (1 / (1 - ε ^ 2)) * (1 / (1 + ε * Real.cos φ)
        - ε * ((Real.cos φ + ε) / (1 + ε * Real.cos φ) ^ 2)))
      (Set.uIcc 0 (2 * Real.pi)) from fun φ _ => hd0 φ),
    integral_const_mul,
    intervalIntegral.integral_sub (Continuous.intervalIntegrable (poisson_cont hε) _ _)
      (Continuous.intervalIntegrable (continuous_const.mul hnum) _ _), integral_const_mul,
    poisson_integral hε]
  have hgint : ∫ φ in (0 : ℝ)..(2 * Real.pi),
      (Real.cos φ + ε) / (1 + ε * Real.cos φ) ^ 2 = g (2 * Real.pi) - g 0 :=
    integral_eq_sub_of_hasDerivAt (fun x _ => hg x)
      (Continuous.intervalIntegrable hnum _ _)
  have hg2pi : g (2 * Real.pi) = (0 : ℝ) := by
    simp only [hgdef]
    rw [Real.sin_two_pi, zero_div]
  have hg0 : g 0 = (0 : ℝ) := by
    simp only [hgdef]
    rw [Real.sin_zero, zero_div]
  rw [hgint, hg2pi, hg0, sub_self, mul_zero]
  have hsq0 : Real.sqrt (1 - ε ^ 2) ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr hc)
  field_simp [hc.ne', hsq0]

/-- **Lemma D.** The cycle-averaged Kirchhoff rate of the symmetric pulsation
equals `ω_N/((1−ε²)·√(1−ε²))` — independent of the pulsation frequency. -/
theorem lemmaD_bridge {γ R ε ω : ℝ} (hω : ω ≠ 0) (hR : R ≠ 0) (hε : ε ^ 2 < 1) (N : ℕ) :
    avgKinFreq γ R ε ω N = ringOmega γ R N / ((1 - ε ^ 2) * Real.sqrt (1 - ε ^ 2)) := by
  rw [lemmaD_omega_independent hω hR hε N, poisson_sq hε]
  field_simp

end LemmaD

/-!
### § 5. Theorem E (statement layer): the co-rotating linearization

The exact W4 objects: the co-rotating field, its linearization at the ring,
the orbit-direction kernel certificate, and the Havelock classification as
an exact acceptance criterion.  The spectral proof of the criterion is the
queued milestone TW5 and is recorded — not claimed.
-/

section TheoremE

variable {γ ω R : ℝ} {N : ℕ}

/-- The co-rotating Kirchhoff field at angular rate `ω`. -/
noncomputable def corotatingField (γ ω : ℝ) (z : ℕ → ℂ) (N : ℕ) (k : ℕ) : ℂ :=
  kirchhoff γ z N k - Complex.I * ((ω : ℝ) : ℂ) * z k

/-- The ring is a fixed point of the co-rotating field at the Theorem-A rate. -/
theorem ring_fixed_point (γ R : ℝ) (ζ : ℂ) (hN : 2 ≤ N) (hR : R ≠ 0)
    (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) {k : ℕ} (hk : k < N) :
    corotatingField γ (ringOmega γ R N) (ringPos R ζ) N k = 0 := by
  rw [corotatingField, ring_velocity γ N hN R hR ζ h1 hprim hk]
  ring

/-- The co-rotating field vanishes identically along the rotating orbit —
the exact source of the W4 noise-floor degeneracy. -/
theorem ring_corotating_constant (γ R : ℝ) (ζ : ℂ) (hN : 2 ≤ N) (hR : R ≠ 0)
    (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) {k : ℕ} (hk : k < N) :
    ∀ t : ℝ, corotatingField γ (ringOmega γ R N) (ringOrbit R ζ (ringOmega γ R N) t) N k = 0 := by
  intro t
  have hconfF : ringOrbit R ζ (ringOmega γ R N) t
      = fun j => Complex.exp (Complex.I * (ringOmega γ R N * t)) * ringPos R ζ j := by
    funext j
    exact mul_comm (ringPos R ζ j)
      (Complex.exp (Complex.I * (ringOmega γ R N * t)))
  have hu : Complex.normSq (Complex.exp (Complex.I * (ringOmega γ R N * t))) = 1 := by
    rw [← Complex.ofReal_mul]
    exact normSq_exp_I_mul (ringOmega γ R N * t)
  rw [corotatingField, hconfF]
  simp only [kirchhoff_smul γ hu k,
    ring_velocity γ N hN R hR ζ h1 hprim hk]
  ring

/-- `λ` is a spectral value of an ℝ-linear perturbation layer. -/
def eigenvalueOf (L : (ℕ → ℂ) → ℕ → ℂ) (ℓ : ℂ) : Prop :=
  ∃ u : ℕ → ℂ, u ≠ 0 ∧ ∀ k : ℕ, L u k = ℓ * u k

/-- The W4 spectral-stability criterion: every spectral value of the
co-rotating linearization at the ring has nonpositive real part. -/
def spectrallyStable (γ ω R : ℝ) (N : ℕ) (ζ : ℂ) : Prop :=
  ∀ ℓ : ℂ, eigenvalueOf (fun u k => kirchhoff γ (fun j => (ringPos R ζ) j) N k
    - Complex.I * ((ω : ℝ) : ℂ) * u k) ℓ → ℓ.re ≤ 0

/-- **Theorem E (recorded, not claimed):** the W4 Havelock classification —
the regular `N`-gon ring is spectrally stable exactly while `N ≤ 7`.  This is
the exact acceptance criterion of milestone TW4; its spectral proof (stability
for `N ≤ 7`, the Havelock instability for `N ≥ 8`) is the queued milestone
TW5 and is NOT proven in this file.  The parent monograph certifies it
numerically; the present file contributes the exact statement layer together
with the degeneracy certificates `ring_fixed_point`,
`ring_corotating_constant` and the Theorem-A forcing theorem. -/
def havelockClassification : Prop :=
  ∀ (N : ℕ) (γ R : ℝ), 2 ≤ N → R ≠ 0 →
    spectrallyStable γ (ringOmega γ R N) R N (rootExp N) ↔ N ≤ 7

end TheoremE

/-!
### Axiom footprint

Sealed at build time by `tools/axioms_gate.py`: every public theorem must
depend only on {propext, Classical.choice, Quot.sound}.
-/

section AxiomFootprint

#print axioms ring_velocity
#print axioms ringOrbit_sol
#print axioms ringOmega_three_eq_lagrange
#print axioms ring_rotation_rate_pos
#print axioms rootExp_pow
#print axioms rootExp_prim
#print axioms kirchhoff_smul
#print axioms normSq_exp_I_mul
#print axioms ringOrbit_deriv
#print axioms eps_pos
#print axioms eps_lt_one_iff
#print axioms eps_at_threshold
#print axioms rClosed_min
#print axioms rClosed_pos_iff
#print axioms rClosed_touches_zero_at_threshold
#print axioms ring_radial_zero
#print axioms lemmaC_pulsation
#print axioms lemmaC_radius_constant
#print axioms lemmaC_H1_reduction
#print axioms lemmaD_omega_independent
#print axioms lemmaD_bridge
#print axioms poisson_integral
#print axioms poisson_sq
#print axioms ringOmega_smul_radius
#print axioms ring_fixed_point
#print axioms ring_corotating_constant

end AxiomFootprint

end Polyvortex


















