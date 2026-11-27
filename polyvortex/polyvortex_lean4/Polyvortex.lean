/-
SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
-/
/-
==========================================================================
POLYVORTEX — LEAN 4 FORMALIZATION: THE N-VORTEX EXTENSION BENCH
==========================================================================
Milestones TW1–TW5 artifact: `polyvortex/polyvortex_lean4/Polyvortex.lean`.
The full program is landed: Theorems A–E, Lemmas C/D and the complete
spectral proof of the Havelock classification.

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

  5. THEOREM E (§5): the co-rotating field and its linearization at the
     ring (`corotatingField`, `corotLin`), the degeneracy certificates
     `ring_fixed_point`, `ring_corotating_constant`,
     `corotLin_orbit_kernel` (the orbit direction sits in the kernel of
     the co-rotating linearization — the exact source of the W4 noise
     floor), and the FULL Havelock classification, now a THEOREM
     (`havelockClassification`): the regular `N`-gon ring (`N ≥ 3`)
     is Havelock-stable exactly while `N ≤ 7`.

  6. THE SPECTRAL MACHINERY (§4′, milestones TW2–TW5): the Fourier layer
     over a primitive root of unity (`zinv`, `fmode`, `fourier_orth`,
     `fmode_inversion`), the Havelock block sums with the closed form
       S_m = (2−m)(N−m)/2
     (`havS_closed`) and the `N ≤ 7` threshold `havS_real_sq`
     (`|S_m| ≤ (N−1)/2`); the ring linearization `corotLin` with the
     orbit-direction kernel (TW3); the master projection lemma
     `corotLin_proj` and the Havelock dispersion relation
       ℓ² + Ω² = β·conj β,   β = (γ/2πR²)·S_{n₀}
     (`corotLin_dispersion`, TW4); and the two halves of the spectral
     proof (TW5): `corotLin_stable7`/`havelockStable_small` — every
     spectral value of the `N ≤ 7` ring is purely imaginary — and
     `havelock_witness` — the Havelock growing mode
       λ = √(β² − Ω²) > 0
     for `N ≥ 8` at the mode pair `n₀ = N − 3`, `m = 5`.  The two halves
     assemble into the theorem `havelockClassification`.

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

See the module docstring above for the six certified layers and
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
theorem eps_pos (C : ℝ) (hC : 0 < C) : 0 < eps C := by
  have hgt : (1 : ℝ) < Real.exp (C / Real.pi) := by
    have h := Real.exp_lt_exp.mpr (div_pos hC Real.pi_pos)
    rw [Real.exp_zero] at h
    exact h
  exact div_pos one_pos (sub_pos.mpr hgt)

/-- The depth is below one exactly above the Chaplygin threshold `π·ln 2`. -/
theorem eps_lt_one_iff (C : ℝ) (hC : 0 < C) : eps C < 1 ↔ Real.pi * Real.log 2 < C := by
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
theorem rClosed_min (C : ℝ) (hC : 0 < C) (t : ℝ) (k : ℕ) :
    (1 - eps C) * Real.sqrt C ≤ rClosed C ω N t k := by
  rw [rClosed]
  have he : (0 : ℝ) < eps C := eps_pos C hC
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
theorem rClosed_pos_iff (C : ℝ) (hC : 0 < C) (hω : ω ≠ 0) :
    (∀ (t : ℝ) (k : ℕ), 0 < rClosed C ω N t k) ↔ Real.pi * Real.log 2 < C := by
  constructor
  · intro h
    by_contra hle
    push_neg at hle
    have hge : (1 : ℝ) ≤ eps C := by
      by_contra hlt
      push_neg at hlt
      exact ((eps_lt_one_iff C hC).mp hlt).not_le hle
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
    have he : (0 : ℝ) < eps C := eps_pos C hC
    have hel : eps C < 1 := (eps_lt_one_iff C hC).mpr h
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
### § 4′. The spectral machinery of Theorem E (milestones TW2–TW5)

Fourier analysis over a primitive `N`-th root of unity: the inverse powers
`zinv`, power congruences modulo the order, the Fourier modes `fmode` with
their inversion formula.  The Havelock block-sum machine: the mode involution
`havSig`, the block sums `havS`/`havC` with the closed form
`S_m = (2−m)(N−m)/2` and the `N ≤ 7` threshold `havS_real_sq`.  The ring
linearization `corotLin` with the orbit-direction kernel (TW3), the master
projection lemma `corotLin_proj` and the dispersion relation
`corotLin_dispersion` (TW4), and the two halves of the spectral proof (TW5):
`corotLin_stable7` — every spectral value of the `N ≤ 7` ring is purely
imaginary — and `havelock_witness` — the Havelock growing mode
`λ = √(β² − Ω²) > 0` for `N ≥ 8` at the mode pair `n₀ = N − 3`, `m = 5`.
-/

section Fourier

variable {N : ℕ} {ζ : ℂ}
variable (hN : N ≠ 0) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1)
  (hunit : Complex.normSq ζ = 1)

/-- The inverse exponent of `ζ ^ m` inside one period. -/
def zinv (N : ℕ) (ζ : ℂ) (m : ℕ) : ℂ := ζ ^ ((N - m % N) % N)

/-- Powers of a root of unity agree modulo the order. -/
theorem pow_congr_mod {a b : ℕ} (hab : a % N = b % N) :
    ζ ^ a = ζ ^ b := by
  conv_lhs => rw [← pow_mod_eq h1 a]
  conv_rhs => rw [← pow_mod_eq h1 b]
  rw [hab]

/-- `zinv N ζ m` is the multiplicative inverse of `ζ ^ m`. -/
theorem zinv_mul (m : ℕ) : zinv N ζ m * ζ ^ m = 1 := by
  have hmlt : m % N < N := Nat.mod_lt m (Nat.pos_of_ne_zero hN)
  have e1 : ((N - m % N) % N + m) % N = ((N - m % N) + m) % N :=
    Nat.ModEq.add_right m (Nat.mod_modEq _ _)
  have h2 : N - m % N + m % N = N := Nat.sub_add_cancel (Nat.le_of_lt hmlt)
  have e3 : (N - m % N) + m = N * (m / N + 1) := by
    have h3a : N * (m / N + 1) = N * (m / N) + N := by rw [Nat.mul_add, Nat.mul_one]
    nth_rewrite 2 [(Nat.div_add_mod m N).symm]
    rw [Nat.add_comm (N - m % N) (N * (m / N) + m % N),
      Nat.add_assoc (N * (m / N)) (m % N) (N - m % N),
      Nat.add_comm (m % N) (N - m % N), h2, ← h3a]
  have e4 : ((N - m % N) + m) % N = 0 := by rw [e3, Nat.mul_mod_right]
  have hkey := e1.trans e4
  show ζ ^ ((N - m % N) % N) * ζ ^ m = 1
  rw [← pow_add, pow_congr_mod h1 (hkey.trans (Nat.zero_mod N).symm), pow_zero]

/-- Norm-squares of powers distribute over the exponent. -/
private theorem normSq_pow_eq (z : ℂ) : ∀ n : ℕ,
    Complex.normSq (z ^ n) = Complex.normSq z ^ n
  | 0 => by simp
  | n + 1 => by
    rw [pow_succ, pow_succ, Complex.normSq_mul, normSq_pow_eq z n]

/-- Conjugate of a power of the root is the inverse power. -/
theorem star_zeta_pow (m : ℕ) : star (ζ ^ m) = zinv N ζ m := by
  have hzm : ζ ^ m ≠ 0 := by
    rcases Nat.eq_zero_or_pos m with rfl | hm
    · exact one_ne_zero
    · intro hcon
      exact root_ne_zero hN h1 ((pow_eq_zero_iff (ne_of_gt hm)).mp hcon)
  refine mul_left_cancel₀ hzm ?_
  show ζ ^ m * (starRingEnd ℂ) (ζ ^ m) = ζ ^ m * zinv N ζ m
  rw [mul_comm (ζ ^ m) ((starRingEnd ℂ) (ζ ^ m)), ← Complex.normSq_eq_conj_mul_self,
    normSq_pow_eq, Complex.ofReal_pow, hunit, Complex.ofReal_one, one_pow,
    mul_comm (ζ ^ m) (zinv N ζ m), zinv_mul hN h1 m]

/-- Telescoping identity for finite geometric sums. -/
theorem mul_one_sub_sum_range (w : ℂ) : ∀ n : ℕ,
    (1 - w) * ∑ k in Finset.range n, w ^ k = 1 - w ^ n
  | 0 => by simp
  | n + 1 => by
    rw [Finset.sum_range_succ, mul_add, mul_one_sub_sum_range w n, sub_mul, one_mul,
      pow_succ]
    ring


end Fourier

section Fourier2

variable {N : ℕ} {ζ : ℂ}
variable (hN : N ≠ 0) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1)
  (hunit : Complex.normSq ζ = 1)

/-- Key modular arithmetic: `(N − m % N) % N + m ≡ 0 [MOD N]`. -/
private theorem key_mod_eq (m : ℕ) : ((N - m % N) % N + m) % N = 0 := by
  have hmlt : m % N < N := Nat.mod_lt m (Nat.pos_of_ne_zero hN)
  have e1 : ((N - m % N) % N + m) % N = ((N - m % N) + m) % N :=
    Nat.ModEq.add_right m (Nat.mod_modEq _ _)
  have h2 : N - m % N + m % N = N := Nat.sub_add_cancel (Nat.le_of_lt hmlt)
  have e3 : (N - m % N) + m = N * (m / N + 1) := by
    have h3a : N * (m / N + 1) = N * (m / N) + N := by rw [Nat.mul_add, Nat.mul_one]
    nth_rewrite 2 [(Nat.div_add_mod m N).symm]
    rw [Nat.add_comm (N - m % N) (N * (m / N) + m % N),
      Nat.add_assoc (N * (m / N)) (m % N) (N - m % N),
      Nat.add_comm (m % N) (N - m % N), h2, ← h3a]
  rw [e1, e3, Nat.mul_mod_right]

/-- The index-shift congruence behind the Fourier orthogonality. -/
theorem zinv_mul_zeta_pow (a b c : ℕ) :
    zinv N ζ (a * b) * ζ ^ (c * b) = ζ ^ (((c % N + N - a % N) % N) * b) := by
  have hXab : ((N - (a * b) % N) % N + a * b) ≡ 0 [MOD N] := key_mod_eq hN (a * b)
  have hA : ((N - (a * b) % N) % N + c * b) + a * b ≡ c * b [MOD N] := by
    rw [Nat.add_assoc, Nat.add_comm (c * b) (a * b), ← Nat.add_assoc]
    exact (Nat.ModEq.add_right (c * b) hXab).trans (by rw [Nat.zero_add])
  have hB : ((c % N + N - a % N) % N) * b + a * b ≡ c * b [MOD N] := by
    have h1c : (c % N + N - a % N) % N + a ≡ c [MOD N] := by
      have hle2 : a % N ≤ c % N + N :=
        Nat.le_trans (Nat.le_of_lt (Nat.mod_lt a (Nat.pos_of_ne_zero hN)))
          (Nat.le_add_left N (c % N))
      have t1 : (c % N + N - a % N) % N + a
          ≡ (c % N + N - a % N) + a [MOD N] :=
        Nat.ModEq.add_right a (Nat.mod_modEq _ _)
      have t2 : (c % N + N - a % N) + a
          ≡ (c % N + N - a % N) + a % N [MOD N] :=
        Nat.ModEq.add_left _ (Nat.mod_modEq a N).symm
      have t3 : (c % N + N - a % N) + a % N ≡ c % N + N [MOD N] := by
        rw [Nat.sub_add_cancel hle2]
      have t4 : (c % N + N) ≡ c % N [MOD N] := by
        show (c % N + N) % N = c % N % N
        rw [Nat.add_mod, Nat.mod_self]
        simp
      have t5 : c % N ≡ c [MOD N] := Nat.mod_modEq c N
      exact t1.trans (t2.trans (t3.trans (t4.trans t5)))
    rw [← Nat.add_mul]
    exact Nat.ModEq.mul_right b h1c
  show ζ ^ ((N - (a * b) % N) % N) * ζ ^ (c * b)
      = ζ ^ (((c % N + N - a % N) % N) * b)
  rw [← pow_add]
  exact pow_congr_mod h1 (Nat.ModEq.add_right_cancel' (a * b)
    (hA.trans hB.symm))

/-- The finite geometric sum over a full period. -/
theorem sum_zeta_range (j : ℕ) :
    ∑ k in Finset.range N, ζ ^ (j * k) = if j % N = 0 then (N : ℂ) else 0 := by
  by_cases hj : j % N = 0
  · rw [if_pos hj]
    have hterm : ∀ k ∈ Finset.range N, ζ ^ (j * k) = (1 : ℂ) := by
      intro k _
      rw [pow_congr_mod h1 (show (j * k) % N = (0 % N : ℕ) from by
        rw [Nat.mul_mod, hj, Nat.zero_mul, Nat.zero_mod]), pow_zero]
    rw [Finset.sum_congr rfl hterm, Finset.sum_const]
    simp
  · rw [if_neg hj]
    have hwN : (ζ ^ j) ^ N = 1 := by
      rw [← pow_mul ζ j N, Nat.mul_comm j N, pow_mul ζ N j, h1, one_pow]
    have hw1 : ζ ^ j ≠ 1 := by
      intro h1w
      have hlt : j % N < N := Nat.mod_lt j (Nat.pos_of_ne_zero hN)
      have hmem : j % N ∈ Finset.Ico 1 N :=
        Finset.mem_Ico.mpr ⟨Nat.pos_of_ne_zero hj, hlt⟩
      exact hprim (j % N) hmem ((pow_mod_eq h1 j).trans h1w)
    have hzero : (1 - ζ ^ j) * ∑ k in Finset.range N, ζ ^ (j * k) = 0 := by
      have hterm : ∑ k in Finset.range N, ζ ^ (j * k)
          = ∑ k in Finset.range N, (ζ ^ j) ^ k :=
        Finset.sum_congr rfl fun k _ => pow_mul ζ j k
      rw [hterm, mul_one_sub_sum_range, hwN, sub_self]
    exact (mul_eq_zero.mp hzero).resolve_left
      (fun h => by rw [sub_eq_zero] at h; exact hw1 h.symm)

/-- Fourier orthogonality over a full period. -/
theorem fourier_orth (n m : ℕ) :
    ∑ k in Finset.range N, star (ζ ^ (n * k)) * ζ ^ (m * k)
      = if (m % N) = (n % N) then (N : ℂ) else 0 := by
  have hterm : ∀ k ∈ Finset.range N, star (ζ ^ (n * k)) * ζ ^ (m * k)
      = ζ ^ (((m % N + N - n % N) % N) * k) := fun k _ => by
    rw [star_zeta_pow hN h1 hunit]
    exact zinv_mul_zeta_pow hN h1 n k m
  rw [Finset.sum_congr rfl hterm]
  by_cases hmn : m % N = n % N
  · rw [if_pos hmn]
    have hδ : ((m % N + N - n % N) % N) = 0 := by
      rw [hmn, Nat.add_sub_cancel_left, Nat.mod_self]
    have hterm2 : ∀ k ∈ Finset.range N,
        ζ ^ (((m % N + N - n % N) % N) * k) = (1 : ℂ) := by
      intro k _
      have hk0 : (((m % N + N - n % N) % N) * k) % N = (0 % N : ℕ) := by
        rw [hδ, Nat.zero_mul, Nat.zero_mod]
      exact pow_congr_mod h1 hk0
    rw [Finset.sum_congr rfl hterm2, Finset.sum_const]
    simp
  · rw [if_neg hmn]
    have hδlt : ((m % N + N - n % N) % N) < N :=
      Nat.mod_lt _ (Nat.pos_of_ne_zero hN)
    have hδne : ((m % N + N - n % N) % N) ≠ 0 := by
      intro h0
      refine hmn ?_
      have hle : n % N ≤ m % N + N :=
        Nat.le_trans (Nat.le_of_lt (Nat.mod_lt n (Nat.pos_of_ne_zero hN)))
          (Nat.le_add_left N (m % N))
      have q1 : m % N ≡ (m % N + N - n % N) + n % N [MOD N] := by
        have r1 : m % N ≡ m % N + N [MOD N] := by
          show (m % N) % N = (m % N + N) % N
          rw [Nat.add_mod, Nat.mod_self, Nat.add_zero]
          show (m : ℕ) % N ≡ m % N % N [MOD N]
          exact (Nat.mod_modEq (m % N) N).symm
        have r2 : (m % N + N - n % N) + n % N ≡ m % N + N [MOD N] := by
          rw [Nat.sub_add_cancel hle]
        exact r1.trans r2.symm
      have q2 : (m % N + N - n % N) + n % N ≡ n % N [MOD N] := by
        have r3 : (m % N + N - n % N) + n % N
            ≡ (m % N + N - n % N) % N + n % N [MOD N] :=
          Nat.ModEq.add_right _ (Nat.mod_modEq _ _).symm
        have r4 : (m % N + N - n % N) % N + n % N ≡ n % N [MOD N] := by
          rw [h0, Nat.zero_add]
        exact r3.trans r4
      have e1 : (m : ℕ) % N = (m : ℕ) % N % N := by
        show (m : ℕ) ≡ m % N [MOD N]
        exact (Nat.mod_modEq m N).symm
      have e2 : (m : ℕ) % N % N
          = ((m % N + N - n % N) + n % N) % N := by
        show (m : ℕ) % N ≡ (m % N + N - n % N) + n % N [MOD N]
        exact q1
      have e3 : ((m % N + N - n % N) + n % N) % N = (n : ℕ) % N % N := by
        show ((m % N + N - n % N) + n % N) ≡ (n : ℕ) % N [MOD N]
        exact q2
      have e4 : (n : ℕ) % N % N = (n : ℕ) % N := by
        show (n : ℕ) % N ≡ n [MOD N]
        exact Nat.mod_modEq n N
      exact e1.trans (e2.trans (e3.trans e4))
    rw [sum_zeta_range hN h1 hprim,
      if_neg (show ((m % N + N - n % N) % N) % N ≠ 0 from by
        rw [Nat.mod_eq_of_lt hδlt]; exact hδne)]

/-- The `n`-th Fourier mode amplitude of a configuration. -/
noncomputable def fmode (u : ℕ → ℂ) (n : ℕ) : ℂ := ∑ k in Finset.range N, u k * star (ζ ^ (n * k))

/-- Fourier inversion for `N`-periodic configurations. -/
theorem fmode_inversion (u : ℕ → ℂ) (hper : ∀ k, u k = u (k % N)) (k : ℕ) :
    u k = (1 / (N : ℂ)) * ∑ n in Finset.range N,
        fmode (N := N) (ζ := ζ) u n * ζ ^ (n * k) := by
  have hNz : (N : ℂ) ≠ 0 := by exact_mod_cast hN
  have hswap : ∑ n in Finset.range N, fmode (N := N) (ζ := ζ) u n * ζ ^ (n * k)
      = ∑ j in Finset.range N, u j
        * (∑ n in Finset.range N, star (ζ ^ (n * j)) * ζ ^ (n * k)) := by
    have step1 : ∀ n ∈ Finset.range N, fmode (N := N) (ζ := ζ) u n * ζ ^ (n * k)
        = ∑ j in Finset.range N, (u j * star (ζ ^ (n * j))) * ζ ^ (n * k) := by
      intro n _
      rw [fmode, Finset.sum_mul]
    rw [Finset.sum_congr rfl step1, Finset.sum_comm]
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [Finset.mul_sum]
    exact Finset.sum_congr rfl fun i _ => mul_assoc _ _ _
  rw [hswap]
  have hinner : ∀ j ∈ Finset.range N,
      u j * (∑ n in Finset.range N, star (ζ ^ (n * j)) * ζ ^ (n * k))
        = if (k % N) = j then u j * (N : ℂ) else 0 := by
    intro j hj
    have hjN : j % N = j := Nat.mod_eq_of_lt (Finset.mem_range.mp hj)
    have hsum : ∑ n in Finset.range N, star (ζ ^ (n * j)) * ζ ^ (n * k)
        = if (k % N) = j then (N : ℂ) else 0 := by
      rw [Finset.sum_congr rfl (fun n _ => by
        rw [Nat.mul_comm n j, Nat.mul_comm n k]),
        fourier_orth hN h1 hprim hunit, hjN]
    by_cases hkc : k % N = j
    · rw [hsum, if_pos hkc, if_pos hkc]
    · rw [hsum, if_neg hkc, if_neg hkc, mul_zero]
  rw [Finset.sum_congr rfl hinner]
  rw [Finset.sum_ite_eq (Finset.range N) (k % N) (fun j => u j * (N : ℂ)),
    if_pos (Finset.mem_range.mpr (Nat.mod_lt k (Nat.pos_of_ne_zero hN)))]
  rw [hper k, div_mul_eq_mul_div, one_mul]
  field_simp

end Fourier2

section HavelockSetup

variable {γ R : ℝ} {N : ℕ} {ζ : ℂ}

/-- The Havelock mode-coupling index `σ n = (2 − n) mod N` — the involution
pairing Fourier modes of the ring linearization. -/
def havSig (N n : ℕ) : ℕ := (2 + N - n % N) % N

/-- `(2 + N) % N = 2` for `3 ≤ N`. -/
private theorem two_add_mod (N : ℕ) (hN3 : 3 ≤ N) : (2 + N) % N = 2 := by
  rw [Nat.add_mod, Nat.mod_self, Nat.add_zero, Nat.mod_eq_of_lt (Nat.mod_lt _ (by omega))]
  exact Nat.mod_eq_of_lt (by omega : 2 < N)

/-- `(N + 1) % N = 1` for `2 ≤ N`. -/
private theorem one_add_mod (N : ℕ) (hN2 : 2 ≤ N) : (N + 1) % N = 1 := by
  rw [Nat.add_mod, Nat.mod_self, Nat.zero_add, Nat.mod_eq_of_lt (Nat.mod_lt _ (by omega))]
  exact Nat.mod_eq_of_lt (by omega : 1 < N)

/-- The Havelock involution is an involution on mode indices: `σ(σ n) = n`
for `n < N`. -/
theorem havSig_inv (N : ℕ) (hN3 : 3 ≤ N) (n : ℕ) (hn : n < N) :
    havSig N (havSig N n) = n := by
  rcases Nat.lt_or_ge n 3 with hlt | hge
  · -- n ≤ 2: σ n = 2 − n, then σ(2−n) = n
    have hs : havSig N n = 2 - n := by
      rw [havSig, Nat.mod_eq_of_lt hn]
      have he : 2 + N - n = (2 - n) + N := by omega
      rw [he, Nat.add_mod_right, Nat.mod_eq_of_lt (by omega)]
    rw [hs, havSig, Nat.mod_eq_of_lt (show (2 - n) < N from by omega)]
    have he2 : 2 + N - (2 - n) = n + N := by omega
    rw [he2, Nat.add_mod_right, Nat.mod_eq_of_lt hn]
  · -- n ≥ 3: σ n = 2 + N − n (already < N), then σ(2+N−n) = n
    have hs : havSig N n = 2 + N - n := by
      rw [havSig, Nat.mod_eq_of_lt hn,
        Nat.mod_eq_of_lt (show 2 + N - n < N from by omega)]
    have h1 : havSig N (2 + N - n) = n := by
      rw [havSig, Nat.mod_eq_of_lt (show (2 + N - n) < N from by omega)]
      have he2 : 2 + N - (2 + N - n) = n := by omega
      rw [he2, Nat.mod_eq_of_lt hn]
    rw [hs, h1]

/-- The Havelock block sum `S_m = ∑_{d=1}^{N−1} (1 − ζ^{md})/(1 − ζ^d)²` —
the per-mode coupling strength of the ring linearization. -/
noncomputable def havS (N : ℕ) (ζ : ℂ) (m : ℕ) : ℂ :=
  ∑ d in Finset.Ico 1 N, (1 - ζ ^ (m * d)) / (1 - ζ ^ d) ^ 2

/-- The partial Havelock sum `C_t = ∑_{d=1}^{N−1} ζ^{td}/(1 − ζ^d)`;
`S_m` telescopes through the `C_t`. -/
noncomputable def havC (N : ℕ) (ζ : ℂ) (t : ℕ) : ℂ :=
  ∑ d in Finset.Ico 1 N, ζ ^ (t * d) / (1 - ζ ^ d)

/-! #### The closed form of `S_m`. -/

/-- `Ico 1 N`-sums reindex as `range (N−1)`-sums. -/
private theorem sum_Ico1 {f : ℕ → ℂ} :
    ∑ d in Finset.Ico 1 N, f d = ∑ m in Finset.range (N - 1), f (m + 1) := by
  rw [Finset.sum_Ico_eq_sum_range]
  exact Finset.sum_congr rfl fun m _ => by rw [Nat.add_comm 1 m]

/-- The ℕ→ℝ→ℂ cast respects bounded subtraction. -/
private theorem castReal_sub {a b : ℕ} (h : b ≤ a) :
    (((a - b : ℕ) : ℝ) : ℂ) = (((a : ℕ) : ℝ) : ℂ) - (((b : ℕ) : ℝ) : ℂ) := by
  rw [Nat.cast_sub h, Complex.ofReal_sub]

/-- `C_0 = (N−1)/2` — the roots-of-unity half-sum. -/
theorem havC_zero (_hN2 : 2 ≤ N) (h1 : ζ ^ N = 1)
    (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) :
    havC N ζ 0 = (((N - 1 : ℕ) : ℝ) : ℂ) / 2 := by
  rw [havC, sum_Ico1]
  rw [Finset.sum_congr rfl fun m _ => by rw [Nat.zero_mul, pow_zero]]
  exact sum_roots_of_unity h1 hprim

/-- `C_1 = −(N−1)/2`. -/
theorem havC_one (hN2 : 2 ≤ N) (h1 : ζ ^ N = 1)
    (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) :
    havC N ζ 1 = -((N - 1 : ℕ) : ℂ) / 2 := by
  have hz := havC_zero hN2 h1 hprim
  have hterm : ∀ d ∈ Finset.Ico 1 N,
      ζ ^ (1 * d) / (1 - ζ ^ d) = ζ ^ (0 * d) / (1 - ζ ^ d) - 1 := by
    intro d hd
    have hne : ζ ^ d ≠ 1 := hprim d hd
    have hne0 : (1 - ζ ^ d) ≠ 0 := fun h => hne (sub_eq_zero.mp h).symm
    rw [Nat.one_mul, Nat.zero_mul, pow_zero, eq_sub_iff_add_eq]
    field_simp
  have hsplit : havC N ζ 1 = havC N ζ 0 - ((N - 1 : ℕ) : ℂ) := by
    rw [havC, Finset.sum_congr rfl hterm, Finset.sum_sub_distrib, Finset.sum_const,
      Nat.card_Ico, nsmul_eq_mul, ← havC, mul_one]
  rw [hsplit, hz, Complex.ofReal_nat_cast]
  ring

/-- `range N` splits into the `{0}`-term and the `Ico 1 N`-sum. -/
private theorem sum_range_zero_Ico {f : ℕ → ℂ} (hN1 : 1 ≤ N) :
    ∑ k in Finset.range N, f k = f 0 + ∑ d in Finset.Ico 1 N, f d := by
  have hr := Finset.sum_range_add (fun k => f k) 1 (N - 1)
  rw [show (1 + (N - 1) : ℕ) = N from by omega, Finset.sum_range_one] at hr
  rw [Finset.sum_congr rfl (fun i (_ : i ∈ Finset.range (N - 1)) =>
      show f (1 + i) = f (i + 1) from by rw [Nat.add_comm 1 i])] at hr
  rw [hr, ← sum_Ico1]

/-- `C_t = C_{t−1} + 1` for `2 ≤ t ≤ N−1`. -/
theorem havC_step (hN2 : 2 ≤ N) (h1 : ζ ^ N = 1)
    (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1)
    (t : ℕ) (ht2 : 2 ≤ t) (htN : t ≤ N - 1) :
    havC N ζ t = havC N ζ (t - 1) + 1 := by
  have hN0 : N ≠ 0 := by omega
  have hpN : ∀ d ∈ Finset.Ico 1 N, 1 - ζ ^ d ≠ 0 := fun d hd h =>
    hprim d hd (sub_eq_zero.mp h).symm
  have hterm : ∀ d ∈ Finset.Ico 1 N,
      ζ ^ (t * d) / (1 - ζ ^ d) - ζ ^ ((t - 1) * d) / (1 - ζ ^ d)
        = -(ζ ^ ((t - 1) * d)) := by
    intro d hd
    have hne0 : (1 - ζ ^ d) ≠ 0 := hpN d hd
    have htd : t * d = (t - 1) * d + d := by
      conv_lhs => rw [show t = (t - 1) + 1 from by omega]
      rw [Nat.add_mul, Nat.one_mul]
    rw [htd, pow_add, ← sub_div,
      show ζ ^ ((t - 1) * d) * ζ ^ d - ζ ^ ((t - 1) * d)
        = -(ζ ^ ((t - 1) * d) * (1 - ζ ^ d)) from by ring,
      neg_div, mul_div_assoc, div_self hne0, mul_one]
  have htn : (t - 1) % N ≠ 0 := by
    rw [Nat.mod_eq_of_lt (by omega : t - 1 < N)]
    omega
  have hz := sum_zeta_range hN0 h1 hprim (t - 1)
  rw [if_neg htn, sum_range_zero_Ico (by omega : 1 ≤ N), Nat.mul_zero, pow_zero] at hz
  have hsumIco : ∑ d in Finset.Ico 1 N, ζ ^ ((t - 1) * d) = -1 := by
    rw [eq_neg_iff_add_eq_zero, add_comm]
    exact hz
  have hsum : havC N ζ t - havC N ζ (t - 1) = 1 := by
    rw [havC, havC, ← Finset.sum_sub_distrib, Finset.sum_congr rfl hterm,
      Finset.sum_neg_distrib, hsumIco]
    ring
  rw [sub_eq_iff_eq_add, add_comm] at hsum
  exact hsum

/-- `C_m = −(N−1)/2 + (m−1)` for `1 ≤ m ≤ N−1`. -/
theorem havC_chain (hN2 : 2 ≤ N) (h1 : ζ ^ N = 1)
    (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) :
    ∀ m, 1 ≤ m → m ≤ N - 1 →
      havC N ζ m = -((N - 1 : ℕ) : ℂ) / 2 + ((m - 1 : ℕ) : ℂ) := by
  intro m
  induction m with
  | zero => intro h _; exact absurd h (Nat.not_succ_le_zero 0)
  | succ t ih =>
    rw [show (Nat.succ t : ℕ) = t + 1 from rfl]
    rcases t with _ | t'
    · intro _ _
      rw [show ((Nat.zero + 1 : ℕ) = 1) from rfl,
        show ((1 - 1 : ℕ) = 0) from by norm_num, Nat.cast_zero, add_zero]
      exact havC_one hN2 h1 hprim
    · intro _ _
      rw [show (Nat.succ t' + 1 : ℕ) = t' + 2 from rfl]
      have hprev := ih (by omega) (by omega)
      rw [show (Nat.succ t' : ℕ) = t' + 1 from rfl,
        show (((t' + 1 - 1 : ℕ) : ℂ) = ((t' : ℕ) : ℂ)) from by
          rw [show (t' + 1 - 1 : ℕ) = t' from by omega]] at hprev
      have hstep := havC_step hN2 h1 hprim (t' + 2) (by omega) (by omega)
      rw [show ((t' + 2 - 1 : ℕ) = t' + 1) from by omega] at hstep
      rw [show (((t' + 2 - 1 : ℕ) : ℂ) = ((t' : ℕ) : ℂ) + 1) from by
        rw [show (t' + 2 - 1 : ℕ) = t' + 1 from by omega, Nat.cast_add, Nat.cast_one]]
      rw [hstep, hprev]
      ring

/-- `S_0 = 0`. -/
theorem havS_zero (N : ℕ) (ζ : ℂ) : havS N ζ 0 = 0 := by
  simp [havS]

/-- `S_{m+1} = S_m + C_m` for `m+1 ≤ N−1`. -/
theorem havS_step (_hN2 : 2 ≤ N) (_h1 : ζ ^ N = 1)
    (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1)
    (m : ℕ) (_hmN : m + 1 ≤ N - 1) :
    havS N ζ (m + 1) = havS N ζ m + havC N ζ m := by
  rw [havS, havS, havC, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun d hd => ?_
  have hne0 : (1 - ζ ^ d) ≠ 0 := fun h => hprim d hd (sub_eq_zero.mp h).symm
  have hmd : (m + 1) * d = m * d + d := by rw [Nat.succ_mul]
  rw [hmd, pow_add]
  field_simp
  ring

/-- **The closed form:** `S_m = (2−m)(N−m)/2` for `1 ≤ m ≤ N−1` (and `S_0 = 0`). -/
theorem havS_closed (hN2 : 2 ≤ N) (h1 : ζ ^ N = 1)
    (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) :
    ∀ m, 1 ≤ m → m ≤ N - 1 →
      havS N ζ m = (2 - ((m : ℕ) : ℂ)) * (((N : ℕ) : ℂ) - ((m : ℕ) : ℂ)) / 2 := by
  intro m
  induction m with
  | zero => intro h1m _; exact absurd h1m (Nat.not_succ_le_zero 0)
  | succ t ih =>
    rw [show (Nat.succ t : ℕ) = t + 1 from rfl]
    rcases t with _ | t'
    · -- m = 1: S_1 = C_0 = (N−1)/2
      intro _ _
      have h1c := havC_zero hN2 h1 hprim
      have hS1 : havS N ζ 1 = havC N ζ 0 := by
        rw [havS, havC]
        refine Finset.sum_congr rfl fun d hd => ?_
        have hne0 : (1 - ζ ^ d) ≠ 0 := fun h => hprim d hd (sub_eq_zero.mp h).symm
        rw [Nat.one_mul, Nat.zero_mul, pow_zero]
        field_simp
        ring
      rw [show ((Nat.zero + 1 : ℕ) = 1) from rfl, hS1, h1c,
        castReal_sub (by omega : (1 : ℕ) ≤ N), Nat.cast_one, Complex.ofReal_one,
        Complex.ofReal_nat_cast]
      ring
    · -- m = t'+2 ≥ 2: S_m = S_{m−1} + C_{m−1}
      intro _ _
      rw [show (Nat.succ t' + 1 : ℕ) = t' + 2 from rfl]
      have hprev := ih (by omega) (by omega)
      rw [show (Nat.succ t' : ℕ) = t' + 1 from rfl, Nat.cast_add, Nat.cast_one] at hprev
      have hstep := havS_step hN2 h1 hprim (t' + 1) (by omega)
      rw [show ((t' + 1 + 1 : ℕ) = t' + 2) from by omega] at hstep
      have hC := havC_chain hN2 h1 hprim (t' + 1) (by omega) (by omega)
      rw [show ((t' + 1 - 1 : ℕ) : ℂ) = ((t' : ℕ) : ℂ) from by
        rw [show (t' + 1 - 1 : ℕ) = t' from by omega],
        Nat.cast_sub (by omega : (1 : ℕ) ≤ N), Nat.cast_one] at hC
      rw [hstep, hprev, hC, Nat.cast_add, Nat.cast_two]
      ring

/-- `S` is invariant under the mode involution: `S_{σ n} = S_{n mod N}`. -/
theorem havS_sym (hN2 : 2 ≤ N) (h1 : ζ ^ N = 1)
    (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (n : ℕ) :
    havS N ζ (havSig N n) = havS N ζ (n % N) := by
  have hmodlt : n % N < N := Nat.mod_lt n (by omega)
  have hzero : havS N ζ 0 = 0 := havS_zero N ζ
  rcases Nat.lt_or_ge (n % N) 3 with hlt | hge
  · rcases Nat.eq_zero_or_pos (n % N) with h0 | hpos
    · -- t = 0: σ n = 2 (N ≥ 3) or n mod N (N = 2); both give the same S-value
      have hN3 : 3 ≤ N ∨ N = 2 := by omega
      rcases hN3 with hN3 | hN3
      · have h2m : ((2 + N - n % N) % N) = 2 := by
          rw [h0, Nat.sub_zero]; exact two_add_mod N hN3
        rw [havSig, h2m, h0, hzero,
          havS_closed hN2 h1 hprim 2 (by omega) (by omega)]
        ring
      · rw [hN3]
        rcases Nat.mod_two_eq_zero_or_one n with hk | hk
        · rw [havSig, hk, show ((2 + 2 - 0 : ℕ) % 2) = 0 from by decide]
        · rw [havSig, hk, show ((2 + 2 - 1 : ℕ) % 2) = 1 from by decide]
    · -- t = 1 or t = 2
      rcases Nat.lt_or_ge (n % N) 2 with h1t | h2t
      · -- t = 1: σ n = 1
        have h1v : n % N = 1 := by omega
        have h1m : ((2 + N - n % N) % N) = 1 := by
          rw [h1v, show ((2 + N - 1 : ℕ) = N + 1) from by omega, one_add_mod N hN2]
        rw [havSig, h1m, h1v]
      · -- t = 2: σ n = 0
        have h2v : n % N = 2 := by omega
        have h2m : ((2 + N - n % N) % N) = 0 := by
          rw [h2v, show ((2 + N - 2 : ℕ) = N) from by omega, Nat.mod_self]
        rw [havSig, h2m, hzero, h2v,
          havS_closed hN2 h1 hprim 2 (by omega) (by omega)]
        ring
  · -- t ≥ 3: σ n = 2 + N − t, and the closed forms agree
    rw [havSig]
    generalize hn : n % N = t
    have _hmodlt : n % N < N := Nat.mod_lt n (by omega)
    have _ht3 : 3 ≤ t := by rw [← hn]; exact hge
    have hltN : 2 + N - t < N := by omega
    have hsig : ((2 + N - t) % N) = 2 + N - t := Nat.mod_eq_of_lt hltN
    have hcast : (((2 + N - t : ℕ) : ℂ)) = ((N : ℕ) : ℂ) + 2 - ((t : ℕ) : ℂ) := by
      rw [show ((2 + N - t : ℕ) = N + 2 - t) from by omega,
        Nat.cast_sub (by omega : t ≤ N + 2), Nat.cast_add, Nat.cast_two]
    rw [hsig, havS_closed hN2 h1 hprim (2 + N - t) (by omega) (by omega),
      hcast, havS_closed hN2 h1 hprim t (by omega) (by omega)]
    ring

/-! #### The small-ring threshold: `|S_m| ≤ (N−1)/2` for `N ≤ 7`. -/

/-- Integer threshold estimate: for `k + l = N − 2 ≤ 5` the product `k * l`
does not exceed `N − 1` — the exact arithmetic behind the Havelock `N = 8`
threshold. -/
private theorem int_prod_bound (N k l : ℕ) (hN7 : N ≤ 7)
    (hsum : k + l = N - 2) : k * l ≤ N - 1 := by
  rcases Nat.eq_zero_or_pos k with hk | hk
  · rw [hk, Nat.zero_mul]; omega
  · rcases Nat.lt_or_ge k 6 with hk5 | hk6
    · interval_cases k
      all_goals omega
    · omega

/-- **The threshold bound.** For `N ≤ 7` every block sum of a primitive root
is real with square controlled by the Kirchhoff window: `S_m · conj S_m = r²`
with `r² ≤ ((N−1)/2)²` (equality `r = (N−1)/2` at `m = 1`). -/
theorem havS_real_sq (hN2 : 2 ≤ N) (hN7 : N ≤ 7) (h1 : ζ ^ N = 1)
    (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (m : ℕ) (hm : m < N) :
    ∃ r : ℝ, havS N ζ m * star (havS N ζ m) = ((r ^ 2 : ℝ) : ℂ)
      ∧ r ^ 2 ≤ (((N - 1 : ℕ) : ℝ) / 2) ^ 2 := by
  rcases Nat.eq_zero_or_pos m with h0 | h0
  · refine ⟨0, ?_, ?_⟩
    · rw [h0, havS_zero, zero_mul]
      norm_num
    · rw [show ((0:ℝ) ^ 2 : ℝ) = 0 from by norm_num]
      positivity
  · have h1m : 1 ≤ m := h0
    have hmr : m ≤ N - 1 := by omega
    set TRE : ℝ := ((2:ℝ) - ((m:ℕ):ℝ)) * (((N:ℕ):ℝ) - ((m:ℕ):ℝ)) / 2 with hTREdef
    have hcast : havS N ζ m = ((TRE : ℝ) : ℂ) := by
      rw [havS_closed hN2 h1 hprim m h1m hmr, hTREdef]
      push_cast
      ring
    refine ⟨TRE, ?_, ?_⟩
    · rw [hcast, Complex.star_def, Complex.conj_ofReal, ← Complex.ofReal_mul, pow_two]
    · rcases Nat.lt_or_ge m 3 with h23 | h3
      · rcases Nat.lt_or_ge m 2 with h1t | h2t
        · -- m = 1: TRE = (N−1)/2, equality
          have hm1 : m = 1 := by omega
          have hN1 : ((N:ℕ):ℝ) - ((1:ℕ):ℝ) = ((N - 1 : ℕ) : ℝ) := by
            rw [Nat.cast_sub (by omega)]
          rw [hTREdef, hm1, hN1]
          norm_num
        · -- m = 2: TRE = 0
          have hm2 : m = 2 := by omega
          have hz : ((2:ℝ) - ((2:ℕ):ℝ)) = 0 := by norm_num
          rw [hTREdef, hm2, hz, zero_mul, zero_div]
          rw [show ((0:ℝ) ^ 2 : ℝ) = 0 from by norm_num]
          positivity
      · -- m ≥ 3: |TRE| = (m−2)(N−m)/2 ≤ (N−1)/2
        have hk : 2 ≤ m := by omega
        have hmlN : m ≤ N := by omega
        have hkl : (m - 2) * (N - m) ≤ N - 1 :=
          int_prod_bound N (m - 2) (N - m) hN7 (by omega)
        have h2m : ((2:ℝ) - ((m:ℕ):ℝ)) = -(((m - 2 : ℕ) : ℝ)) := by
          rw [Nat.cast_sub hk, neg_sub, Nat.cast_two]
        have hNm : ((N:ℕ):ℝ) - ((m:ℕ):ℝ) = ((N - m : ℕ) : ℝ) := by
          rw [Nat.cast_sub hmlN]
        have hXle : ((m - 2 : ℕ) : ℝ) * ((N - m : ℕ) : ℝ) ≤ ((N - 1 : ℕ) : ℝ) := by
          exact_mod_cast hkl
        have hTREsq : ((2:ℝ) - ((m:ℕ):ℝ)) * (((N:ℕ):ℝ) - ((m:ℕ):ℝ)) / 2
            = -(((m - 2 : ℕ) : ℝ) * ((N - m : ℕ) : ℝ) / 2) := by
          rw [h2m, hNm]
          ring
        rw [hTREdef, hTREsq, neg_sq]
        exact pow_le_pow_left (by positivity) (by linarith) 2

/-! #### The ring linearization `corotLin` (TW3). -/

/-- The linearization of the co-rotating Kirchhoff field at the regular ring:
the first-order Havelock layer `u ↦ D(k)(u)` in co-rotating coordinates. -/
noncomputable def corotLin (γ R : ℝ) (N : ℕ) (ζ : ℂ) (u : ℕ → ℂ) (k : ℕ) : ℂ :=
  -Complex.I * ((ringOmega γ R N : ℝ) : ℂ) * u k
    - Complex.I * (((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ)) * ζ ^ (2 * k)
      * ∑ d in Finset.Ico 1 N,
        (star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2

/-- `ringPos` unfolds to the radius times the power of the root. -/
private theorem ringPos_eq (R : ℝ) (ζ : ℂ) (k : ℕ) : ringPos R ζ k = (R : ℂ) * ζ ^ k := rfl

/-- `star` is conjugation on the ring constants. -/
private theorem starI' : star Complex.I = -Complex.I :=
  Complex.conj_I

/-- `star` fixes the real scalars inside `ℂ`. -/
private theorem starR' (r : ℝ) : star (r : ℂ) = (r : ℂ) :=
  Complex.conj_ofReal r

/-- Conjugation anticommutes `i` past a real scalar. -/
private theorem star_CR (R : ℝ) : star (Complex.I * (R : ℂ)) = -(Complex.I * (R : ℂ)) := by
  rw [star_mul, starI', starR']
  ring

/-- `corotLin` preserves `N`-periodicity. -/
theorem corotLin_periodic (γ R : ℝ) (N : ℕ) (ζ : ℂ) (h1 : ζ ^ N = 1)
    (u : ℕ → ℂ) (hper : ∀ k, u k = u (k % N)) (k : ℕ) :
    corotLin γ R N ζ u (k + N) = corotLin γ R N ζ u k := by
  have hmod1 : (k + N) % N = k % N := Nat.add_mod_right k N
  have h2N : ζ ^ (2 * N) = 1 := by
    rw [show ((2 * N : ℕ) = N + N) from by ring, pow_add, h1, mul_one]
  have hsum : ∀ d ∈ Finset.Ico 1 N,
      (star (u k) - star (u ((k + N + N - d) % N))) / (1 - ζ ^ d) ^ 2
        = (star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2 := by
    intro d hd
    have hd2 : d < N := (Finset.mem_Ico.mp hd).2
    have hdN : d ≤ N := by omega
    rw [Nat.add_sub_assoc hdN (k + N), Nat.add_sub_assoc hdN k,
      Nat.add_right_comm k N (N - d), Nat.add_mod_right]
  rw [corotLin, corotLin,
    show (2 * (k + N) : ℕ) = 2 * k + 2 * N from by ring, pow_add, h2N, mul_one,
    hper (k + N), hmod1, ← hper k, Finset.sum_congr rfl hsum]

/-- `corotLin` is additive. -/
theorem corotLin_add (γ R : ℝ) (N : ℕ) (ζ : ℂ) (u v : ℕ → ℂ) (k : ℕ) :
    corotLin γ R N ζ (u + v) k = corotLin γ R N ζ u k + corotLin γ R N ζ v k := by
  rw [corotLin, corotLin, corotLin, Pi.add_apply, star_add, mul_add]
  rw [Finset.sum_congr rfl (fun d (_ : d ∈ Finset.Ico 1 N) => by
    rw [Pi.add_apply, star_add,
      show ((star (u k) + star (v k)) - (star (u ((k + N - d) % N)) + star (v ((k + N - d) % N))))
        = (star (u k) - star (u ((k + N - d) % N)))
          + (star (v k) - star (v ((k + N - d) % N))) from by ring, add_div])]
  rw [Finset.sum_add_distrib]
  ring

/-- The two factors of `i` cancel: `(-i) * i = 1`. -/
private theorem hnegI : (-Complex.I) * Complex.I = 1 := by
  rw [neg_mul, Complex.I_mul_I, neg_neg]

/-- The product `i·(−i·x)` collapses back to `x`. -/
private theorem imul_neg_I (x : ℂ) : Complex.I * (-(Complex.I * x)) = x := by
  rw [mul_neg, ← mul_assoc, Complex.I_mul_I, neg_one_mul, neg_neg]

/-- **TW3 (kernel certificate).** The orbit direction `i·ringPos` lies in the
kernel of the ring linearization — the exact linear source of the W4
noise-floor degeneracy (the doubled zero eigenvalue). -/
theorem corotLin_orbit_kernel (γ R : ℝ) (N : ℕ) (hN : 2 ≤ N) (ζ : ℂ)
    (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1)
    (hunit : Complex.normSq ζ = 1) (k : ℕ) :
    corotLin γ R N ζ (fun j => Complex.I * ringPos R ζ j) k = 0 := by
  have hN0 : N ≠ 0 := by omega
  set u : ℕ → ℂ := fun j => Complex.I * ringPos R ζ j with hu
  have husk : star (u k) = -(Complex.I * (R : ℂ)) * star (ζ ^ k) := by
    simp only [hu]
    rw [ringPos_eq, star_mul, star_mul, starI', starR',
      star_zeta_pow hN0 h1 hunit k]
    ring
  have husd : ∀ d ∈ Finset.Ico 1 N,
      star (u ((k + N - d) % N)) = -(Complex.I * (R : ℂ)) * star (ζ ^ k) * ζ ^ d := by
    intro d hd
    have hd1 : 1 ≤ d := (Finset.mem_Ico.mp hd).1
    have hdN : d < N := (Finset.mem_Ico.mp hd).2
    have hze : ζ ^ ((k + N - d) % N) = ζ ^ (k + N - d) :=
      pow_congr_mod h1 (Nat.mod_modEq _ _)
    have hNd : ζ ^ (N - d) = star (ζ ^ d) := by
      rw [star_zeta_pow hN0 h1 hunit d]
      show ζ ^ (N - d) = ζ ^ ((N - d % N) % N)
      rw [show ((d % N : ℕ) = d) from Nat.mod_eq_of_lt hdN,
        show (((N - d) % N : ℕ) = N - d) from
          Nat.mod_eq_of_lt (Nat.sub_lt (by omega) hd1)]
    simp only [hu]
    rw [ringPos_eq, star_mul, star_mul, starI', starR',
      hze, Nat.add_sub_assoc (show d ≤ N from by omega) k, pow_add, star_mul, hNd,
      star_star]
    ring
  have hzsq : ζ ^ k * star (ζ ^ k) = 1 := by
    rw [star_zeta_pow hN0 h1 hunit k, mul_comm, zinv_mul hN0 h1 k]
  have hz2k : ζ ^ (2 * k) * star (ζ ^ k) = ζ ^ k := by
    rw [show ((2 * k : ℕ) = k + k) from by ring, pow_add, mul_assoc, hzsq, mul_one]
  have hOm : ((ringOmega γ R N : ℝ) : ℂ)
      = (((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ)) * (((N - 1 : ℕ) : ℝ) : ℂ) / 2 := by
    rw [ringOmega]
    push_cast
    ring
  have hsum : ∑ d in Finset.Ico 1 N,
      (star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2
      = -(Complex.I * (R : ℂ)) * star (ζ ^ k) * (((N - 1 : ℕ) : ℝ) : ℂ) / 2 := by
    have hne0 : ∀ d ∈ Finset.Ico 1 N, (1 - ζ ^ d) ≠ 0 := fun d hd h =>
      hprim d hd (sub_eq_zero.mp h).symm
    have hperd : ∀ d ∈ Finset.Ico 1 N,
        (star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2
          = -(Complex.I * (R : ℂ)) * star (ζ ^ k) / (1 - ζ ^ d) := by
      intro d hd
      have h1d : (1 - ζ ^ d) ≠ 0 := hne0 d hd
      rw [husk, husd d hd]
      field_simp
      ring
    rw [Finset.sum_congr rfl hperd,
      Finset.sum_congr rfl (fun x _ => by rw [← mul_one_div]),
      ← Finset.mul_sum, sum_Ico1,
      sum_roots_of_unity h1 hprim]
    ring
  have h2nd : Complex.I * ((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ) * ζ ^ (2 * k)
      * ∑ d in Finset.Ico 1 N,
          (star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2
    = ((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ) * (R : ℂ) * ζ ^ k
        * (((N - 1 : ℕ) : ℝ) : ℂ) / 2 := by
    rw [hsum, ← mul_div_assoc,
      mul_assoc (-(Complex.I * (R : ℂ))) (star (ζ ^ k)) (((N - 1 : ℕ) : ℝ) : ℂ),
      mul_comm (Complex.I * ((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ)) (ζ ^ (2 * k)),
      mul_assoc,
      mul_left_comm (ζ ^ (2 * k))
        (Complex.I * ((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ))
        (-(Complex.I * (R : ℂ)) * (star (ζ ^ k) * (((N - 1 : ℕ) : ℝ) : ℂ))),
      mul_left_comm (ζ ^ (2 * k)) (-(Complex.I * (R : ℂ)))
        (star (ζ ^ k) * (((N - 1 : ℕ) : ℝ) : ℂ)),
      ← mul_assoc (ζ ^ (2 * k)) (star (ζ ^ k)) (((N - 1 : ℕ) : ℝ) : ℂ), hz2k]
    rw [mul_assoc, mul_comm ((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ)
        (-(Complex.I * (R : ℂ)) * (ζ ^ k * (((N - 1 : ℕ) : ℝ) : ℂ))),
      ← mul_assoc, ← mul_assoc, imul_neg_I]
    ring
  rw [corotLin, h2nd, hOm]
  simp only [hu]
  rw [ringPos_eq]
  linear_combination (((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ) * (((N - 1 : ℕ) : ℝ) : ℂ)
    * (R : ℂ) * ζ ^ k / 2) * hnegI


/-! #### The master projection lemma (TW4). -/

/-- Adding `d` after the shift-reversal returns the original index. -/
private theorem mod_shift_add (N d k : ℕ) (hdN : d ≤ N) (hk : k < N) :
    ((k + N - d) % N + d) % N = k := by
  have hA : ((k + N - d) % N + d) % N = (k + N - d + d) % N :=
    Nat.ModEq.add_right d (Nat.mod_modEq (k + N - d) N)
  have hB : (k + N - d + d) = k + N := by omega
  rw [hA, hB, Nat.add_mod_right k N, Nat.mod_eq_of_lt hk]

/-- Adding `N - d` after the forward shift returns the original index. -/
private theorem mod_shift_sub (N d j : ℕ) (hdN : d ≤ N) (hj : j < N) :
    ((j + d) % N + N - d) % N = j := by
  have h2 : ((j + d) % N + (N - d)) % N = (j + d + (N - d)) % N :=
    Nat.ModEq.add_right (N - d) (Nat.mod_modEq (j + d) N)
  have hEq : ((j + d) % N + N - d) = (j + d) % N + (N - d) :=
    Nat.add_sub_assoc hdN ((j + d) % N)
  have hEq2 : j + d + (N - d) = j + N := by
    rw [Nat.add_assoc, Nat.add_comm d (N - d), Nat.sub_add_cancel hdN]
  rw [hEq, h2, hEq2, Nat.add_mod_right j N, Nat.mod_eq_of_lt hj]

/-- Summation over `range N` is invariant under the shift-reversal
`k ↦ (k + N - d) % N` for `d < N`. -/
private theorem sum_range_shift (hN : N ≠ 0) (d : ℕ) (hd : d < N) {F : ℕ → ℂ} :
    ∑ k in Finset.range N, F ((k + N - d) % N) = ∑ j in Finset.range N, F j := by
  refine Finset.sum_nbij' (fun k => (k + N - d) % N) (fun j => (j + d) % N) ?_ ?_ ?_ ?_
    (fun _ _ => rfl)
  · intro k _
    simp only [Finset.mem_range]
    exact Nat.mod_lt _ (Nat.pos_of_ne_zero hN)
  · intro j _
    simp only [Finset.mem_range]
    exact Nat.mod_lt _ (Nat.pos_of_ne_zero hN)
  · intro k hk
    simp only [Finset.mem_range] at hk
    exact mod_shift_add N d k (by omega) hk
  · intro j hj
    simp only [Finset.mem_range] at hj
    exact mod_shift_sub N d j (by omega) hj

/-- The co-rotating weight identity: `ζ^{2j}·conj(ζ^{n·j}) = ζ^{σ(n)·j}` with
`σ(n) = havSig N n`. -/
theorem zeta_havSig_apply (hN3 : 3 ≤ N) (h1 : ζ ^ N = 1)
    (hunit : Complex.normSq ζ = 1) (n j : ℕ) :
    (ζ : ℂ) ^ (2 * j) * star (ζ ^ (n * j)) = ζ ^ (havSig N n * j) := by
  have hN0 : N ≠ 0 := by omega
  rw [star_zeta_pow hN0 h1 hunit (n * j), mul_comm (ζ ^ (2 * j)) (zinv N ζ (n * j)),
    zinv_mul_zeta_pow hN0 h1 n j 2,
    show ((2 % N + N - n % N) % N : ℕ) = havSig N n from by
      rw [havSig, Nat.mod_eq_of_lt (show (2:ℕ) < N from by omega)]]

/-- Conjugation of a Fourier coefficient swaps the weight to the other side. -/
theorem star_fmode (u : ℕ → ℂ) (m : ℕ) :
    star (@fmode N ζ u m) = ∑ k in Finset.range N, star (u k) * ζ ^ (m * k) := by
  show star (∑ k in Finset.range N, u k * star (ζ ^ (m * k)))
    = ∑ k in Finset.range N, star (u k) * ζ ^ (m * k)
  rw [← starRingEnd_apply, map_sum (starRingEnd ℂ)]
  refine Finset.sum_congr rfl fun k _ => ?_
  rw [starRingEnd_apply, star_mul, star_star, mul_comm]

/-- **TW4 (master projection lemma).** For any configuration `u`, the mode-`n`
Fourier coefficient of the linearized co-rotating field depends only on the
mode coefficients `fmode u n` and `fmode u (havSig N n)`:
`D_n = -iΩ·C_n - i·(γ/2πR²)·S_{σ(n)}·conj(C_{σ(n)})`. -/
theorem corotLin_proj (γ R : ℝ) (hN3 : 3 ≤ N) (ζ : ℂ) (h1 : ζ ^ N = 1)
    (hunit : Complex.normSq ζ = 1) (u : ℕ → ℂ) (n : ℕ) :
    ∑ k in Finset.range N, corotLin γ R N ζ u k * star (ζ ^ (n * k))
      = -Complex.I * ((ringOmega γ R N : ℝ) : ℂ) * @fmode N ζ u n
        - Complex.I * ((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ)
          * (havS N ζ (havSig N n)
            * star (∑ j in Finset.range N, u j * star (ζ ^ (havSig N n * j)))) := by
  have hN0 : N ≠ 0 := by omega
  have hw : ∀ j, ζ ^ (havSig N n * j) = ζ ^ (2 * j) * star (ζ ^ (n * j)) :=
    fun j => (zeta_havSig_apply hN3 h1 hunit n j).symm
  have hsf : star (@fmode N ζ u (havSig N n))
      = ∑ k in Finset.range N, star (u k) * ζ ^ (havSig N n * k) :=
    star_fmode u (havSig N n)
  show (∑ k in Finset.range N, corotLin γ R N ζ u k * star (ζ ^ (n * k))
    = -Complex.I * ((ringOmega γ R N : ℝ) : ℂ)
      * (∑ j in Finset.range N, u j * star (ζ ^ (n * j)))
      - Complex.I * ((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ)
        * (havS N ζ (havSig N n)
          * star (∑ j in Finset.range N, u j * star (ζ ^ (havSig N n * j)))))
  have hW0 : ∑ k in Finset.range N, ζ ^ (havSig N n * k) * star (u k)
      = star (@fmode N ζ u (havSig N n)) := by
    rw [hsf]
    exact Finset.sum_congr rfl fun k _ => mul_comm (ζ ^ (havSig N n * k)) (star (u k))
  have hWd : ∀ d ∈ Finset.Ico 1 N,
      ∑ k in Finset.range N, ζ ^ (havSig N n * k) * star (u ((k + N - d) % N))
        = ζ ^ (havSig N n * d) * star (@fmode N ζ u (havSig N n)) := by
    intro d hd
    have hdN : d < N := (Finset.mem_Ico.mp hd).2
    have hF : ∑ k in Finset.range N,
        ζ ^ (havSig N n * (((k + N - d) % N + d) % N)) * star (u ((k + N - d) % N))
        = ∑ j in Finset.range N, ζ ^ (havSig N n * ((j + d) % N)) * star (u j) :=
      sum_range_shift (F := fun j => ζ ^ (havSig N n * ((j + d) % N)) * star (u j))
        hN0 d hdN
    have hF' : ∑ k in Finset.range N, ζ ^ (havSig N n * k) * star (u ((k + N - d) % N))
        = ∑ j in Finset.range N, ζ ^ (havSig N n * ((j + d) % N)) * star (u j) := by
      rw [Finset.sum_congr rfl (fun k hk => by
        simp only [Finset.mem_range] at hk
        rw [mod_shift_add N d k (by omega) hk])] at hF
      exact hF
    have hShift : ∀ j ∈ Finset.range N,
        ζ ^ (havSig N n * ((j + d) % N)) * star (u j)
          = ζ ^ (havSig N n * d) * (ζ ^ (havSig N n * j) * star (u j)) := by
      intro j _
      have hExp : (havSig N n * ((j + d) % N)) % N = (havSig N n * (j + d)) % N :=
        (Nat.mod_modEq (j + d) N).mul_left (havSig N n)
      rw [pow_congr_mod h1 hExp, Nat.mul_add, pow_add]
      ring
    rw [hF', Finset.sum_congr rfl hShift, ← Finset.mul_sum,
      Finset.sum_congr rfl (fun k _ => mul_comm (ζ ^ (havSig N n * k)) (star (u k))),
      ← hsf]
  have hsplit : ∀ k : ℕ, corotLin γ R N ζ u k * star (ζ ^ (n * k))
      = (-Complex.I * ((ringOmega γ R N : ℝ) : ℂ) * u k) * star (ζ ^ (n * k))
        - (Complex.I * ((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ) * ζ ^ (2 * k)
          * (∑ d in Finset.Ico 1 N,
              (star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2))
          * star (ζ ^ (n * k)) := by
    intro k; rw [corotLin]; ring
  have hp1 : ∀ k : ℕ, (-Complex.I * ((ringOmega γ R N : ℝ) : ℂ) * u k)
        * star (ζ ^ (n * k))
      = -Complex.I * ((ringOmega γ R N : ℝ) : ℂ) * (u k * star (ζ ^ (n * k))) := by
    intro k; rw [← mul_assoc]
  have hp1b : ∑ k in Finset.range N, -Complex.I * ((ringOmega γ R N : ℝ) : ℂ)
        * (u k * star (ζ ^ (n * k)))
      = -Complex.I * ((ringOmega γ R N : ℝ) : ℂ)
        * ∑ k in Finset.range N, u k * star (ζ ^ (n * k)) :=
    (Finset.mul_sum _ _ _).symm
  have hp2 : ∀ k : ℕ, (Complex.I * ((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ) * ζ ^ (2 * k)
          * (∑ d in Finset.Ico 1 N,
              (star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2))
        * star (ζ ^ (n * k))
      = Complex.I * ((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ)
        * (ζ ^ (2 * k) * star (ζ ^ (n * k))
          * (∑ d in Finset.Ico 1 N,
              (star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2)) := by
    intro k; ring
  have hp3b : ∑ k in Finset.range N, Complex.I * ((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ)
          * (ζ ^ (2 * k) * star (ζ ^ (n * k))
            * (∑ d in Finset.Ico 1 N,
                (star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2))
      = Complex.I * ((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ)
        * ∑ k in Finset.range N, (ζ ^ (2 * k) * star (ζ ^ (n * k))
            * (∑ d in Finset.Ico 1 N,
                (star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2)) :=
    (Finset.mul_sum _ _ _).symm
  have hp6k : ∀ k : ℕ, ζ ^ (2 * k) * star (ζ ^ (n * k))
          * (∑ d in Finset.Ico 1 N,
              (star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2)
      = ∑ d in Finset.Ico 1 N, ζ ^ (havSig N n * k)
          * ((star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2) := by
    intro k; rw [← hw k, Finset.mul_sum]
  have hp6 : ∑ k in Finset.range N, (ζ ^ (2 * k) * star (ζ ^ (n * k))
          * (∑ d in Finset.Ico 1 N,
              (star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2))
      = ∑ k in Finset.range N, ∑ d in Finset.Ico 1 N, ζ ^ (havSig N n * k)
          * ((star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2) := by
    rw [Finset.sum_congr rfl (fun k _ => hp6k k)]
  have hp7a : ∀ (d k : ℕ), ζ ^ (havSig N n * k)
          * ((star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2)
      = (ζ ^ (havSig N n * k) * (star (u k) - star (u ((k + N - d) % N))))
        / (1 - ζ ^ d) ^ 2 := by
    intro d k; rw [mul_div_assoc']
  have hp7b : ∀ (d k : ℕ), ζ ^ (havSig N n * k)
          * (star (u k) - star (u ((k + N - d) % N)))
      = ζ ^ (havSig N n * k) * star (u k)
        - ζ ^ (havSig N n * k) * star (u ((k + N - d) % N)) := by
    intro d k; rw [mul_sub]
  have hp7 : ∀ d ∈ Finset.Ico 1 N,
      ∑ k in Finset.range N, ζ ^ (havSig N n * k)
          * ((star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2)
      = (∑ k in Finset.range N, ζ ^ (havSig N n * k) * star (u k)
          - ∑ k in Finset.range N, ζ ^ (havSig N n * k)
            * star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2 := by
    intro d _hd
    rw [Finset.sum_congr rfl (fun k _ => hp7a d k), ← Finset.sum_div,
      Finset.sum_congr rfl (fun k _ => hp7b d k), Finset.sum_sub_distrib]
  have hp8 : ∑ d in Finset.Ico 1 N, ∑ k in Finset.range N, ζ ^ (havSig N n * k)
          * ((star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2)
      = star (@fmode N ζ u (havSig N n)) * havS N ζ (havSig N n) := by
    have hd1 : ∀ d ∈ Finset.Ico 1 N,
        ∑ k in Finset.range N, ζ ^ (havSig N n * k)
            * ((star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2)
        = (star (@fmode N ζ u (havSig N n))
            - ζ ^ (havSig N n * d) * star (@fmode N ζ u (havSig N n)))
          / (1 - ζ ^ d) ^ 2 := by
      intro d hd
      rw [hp7 d hd, hW0, hWd d hd]
    have hd2 : ∀ d ∈ Finset.Ico 1 N,
        (star (@fmode N ζ u (havSig N n))
            - ζ ^ (havSig N n * d) * star (@fmode N ζ u (havSig N n)))
          / (1 - ζ ^ d) ^ 2
        = star (@fmode N ζ u (havSig N n))
          * ((1 - ζ ^ (havSig N n * d)) / (1 - ζ ^ d) ^ 2) := by
      intro d _
      ring
    have hd3 : ∑ d in Finset.Ico 1 N, star (@fmode N ζ u (havSig N n))
          * ((1 - ζ ^ (havSig N n * d)) / (1 - ζ ^ d) ^ 2)
        = star (@fmode N ζ u (havSig N n)) * havS N ζ (havSig N n) := by
      rw [havS]
      exact (Finset.mul_sum _ _ _).symm
    rw [Finset.sum_congr rfl hd1, Finset.sum_congr rfl hd2, hd3]
  rw [Finset.sum_congr rfl (fun k _ => hsplit k), Finset.sum_sub_distrib,
    Finset.sum_congr rfl (fun k _ => hp1 k), hp1b,
    Finset.sum_congr rfl (fun k _ => hp2 k), hp3b, hp6, Finset.sum_comm, hp8,
    mul_comm (star (@fmode N ζ u (havSig N n))) (havS N ζ (havSig N n))]
  rfl


/-- The Fourier coefficients are ℂ-linear in the configuration (add form). -/
theorem fmode_add (c d : ℂ) (u v : ℕ → ℂ) (n : ℕ) :
    @fmode N ζ (fun k => c * u k + d * v k) n
      = c * @fmode N ζ u n + d * @fmode N ζ v n := by
  have hk : ∀ k : ℕ, (c * u k + d * v k) * star (ζ ^ (n * k))
      = c * (u k * star (ζ ^ (n * k))) + d * (v k * star (ζ ^ (n * k))) := by
    intro k; ring
  show (∑ k in Finset.range N, (c * u k + d * v k) * star (ζ ^ (n * k))
    = c * ∑ k in Finset.range N, u k * star (ζ ^ (n * k))
      + d * ∑ k in Finset.range N, v k * star (ζ ^ (n * k)))
  rw [Finset.sum_congr rfl (fun k _ => hk k), Finset.sum_add_distrib,
    ← Finset.mul_sum (Finset.range N) (fun k => u k * star (ζ ^ (n * k))) c,
    ← Finset.mul_sum (Finset.range N) (fun k => v k * star (ζ ^ (n * k))) d]

/-- The Fourier coefficients are ℂ-linear in the configuration (subtract form). -/
theorem fmode_linearity (a b : ℂ) (u v : ℕ → ℂ) (n : ℕ) :
    @fmode N ζ (fun k => a * u k - b * v k) n
      = a * @fmode N ζ u n - b * @fmode N ζ v n := by
  have hk : ∀ k : ℕ, (a * u k - b * v k) * star (ζ ^ (n * k))
      = a * (u k * star (ζ ^ (n * k))) - b * (v k * star (ζ ^ (n * k))) := by
    intro k; ring
  show (∑ k in Finset.range N, (a * u k - b * v k) * star (ζ ^ (n * k))
    = a * ∑ k in Finset.range N, u k * star (ζ ^ (n * k))
      - b * ∑ k in Finset.range N, v k * star (ζ ^ (n * k)))
  rw [Finset.sum_congr rfl (fun k _ => hk k), Finset.sum_sub_distrib,
    ← Finset.mul_sum (Finset.range N) (fun k => u k * star (ζ ^ (n * k))) a,
    ← Finset.mul_sum (Finset.range N) (fun k => v k * star (ζ ^ (n * k))) b]

/-- **TW4 (the mode system).** For a spectral pair `(u, v)` of the co-rotating
linearization with eigenvalue `ℓ = a + i·b`, the Fourier coefficients satisfy,
for every mode `n`, the rotated pair system
`(a+iΩ)·C_n − b·D_n = −i·β_n·conj(C_{σn})`, `b·C_n + (a+iΩ)·D_n = −i·β_n·conj(D_{σn})`
with `β_n := (γ/2πR²)·havS N ζ n` and `σn := havSig N n`. -/
theorem corotLin_pair_system (γ R : ℝ) (hN3 : 3 ≤ N) (ζ : ℂ) (h1 : ζ ^ N = 1)
    (hunit : Complex.normSq ζ = 1) (u v : ℕ → ℂ) (a b : ℂ)
    (hu : ∀ k, corotLin γ R N ζ u k = a * u k - b * v k)
    (hv : ∀ k, corotLin γ R N ζ v k = b * u k + a * v k) (n : ℕ) :
    (a + Complex.I * ((ringOmega γ R N : ℝ) : ℂ)) * @fmode N ζ u n
        - b * @fmode N ζ v n
      = -Complex.I * (((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ)
          * havS N ζ (havSig N n))
        * star (∑ j in Finset.range N, u j * star (ζ ^ (havSig N n * j)))
    ∧ (a + Complex.I * ((ringOmega γ R N : ℝ) : ℂ)) * @fmode N ζ v n
        + b * @fmode N ζ u n
      = -Complex.I * (((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ)
          * havS N ζ (havSig N n))
        * star (∑ j in Finset.range N, v j * star (ζ ^ (havSig N n * j))) := by
  have hu' : ∑ k in Finset.range N, corotLin γ R N ζ u k * star (ζ ^ (n * k))
      = a * @fmode N ζ u n - b * @fmode N ζ v n := by
    have h1' : ∀ k : ℕ, corotLin γ R N ζ u k * star (ζ ^ (n * k))
        = (a * u k - b * v k) * star (ζ ^ (n * k)) := fun k => by rw [hu k]
    show (∑ k in Finset.range N, corotLin γ R N ζ u k * star (ζ ^ (n * k))
      = a * @fmode N ζ u n - b * @fmode N ζ v n)
    rw [Finset.sum_congr rfl (fun k _ => h1' k)]
    show (@fmode N ζ (fun k => a * u k - b * v k) n
      = a * @fmode N ζ u n - b * @fmode N ζ v n)
    exact fmode_linearity a b u v n
  have hv' : ∑ k in Finset.range N, corotLin γ R N ζ v k * star (ζ ^ (n * k))
      = b * @fmode N ζ u n + a * @fmode N ζ v n := by
    have h1' : ∀ k : ℕ, corotLin γ R N ζ v k * star (ζ ^ (n * k))
        = (b * u k + a * v k) * star (ζ ^ (n * k)) := fun k => by rw [hv k]
    show (∑ k in Finset.range N, corotLin γ R N ζ v k * star (ζ ^ (n * k))
      = b * @fmode N ζ u n + a * @fmode N ζ v n)
    rw [Finset.sum_congr rfl (fun k _ => h1' k)]
    show (@fmode N ζ (fun k => b * u k + a * v k) n
      = b * @fmode N ζ u n + a * @fmode N ζ v n)
    exact fmode_add b a u v n
  have hC := corotLin_proj γ R hN3 ζ h1 hunit u n
  have hD := corotLin_proj γ R hN3 ζ h1 hunit v n
  rw [hu'] at hC
  rw [hv'] at hD
  constructor
  · rw [show ((a + Complex.I * ((ringOmega γ R N : ℝ) : ℂ)) * @fmode N ζ u n
        - b * @fmode N ζ v n
      = a * @fmode N ζ u n - b * @fmode N ζ v n
        + Complex.I * ((ringOmega γ R N : ℝ) : ℂ) * @fmode N ζ u n) from by ring, hC]
    ring
  · rw [show ((a + Complex.I * ((ringOmega γ R N : ℝ) : ℂ)) * @fmode N ζ v n
        + b * @fmode N ζ u n
      = b * @fmode N ζ u n + a * @fmode N ζ v n
        + Complex.I * ((ringOmega γ R N : ℝ) : ℂ) * @fmode N ζ v n) from by ring, hD]
    ring

/-- **The Havelock dispersion relation (TW5).** For a spectral pair `(u, v)`
with eigenvalue `ℓ = a + i·b` of the co-rotating linearization, any mode
`n₀ < N` carrying a nonzero complex amplitude obeys
`ℓ² + Ω² = β · conj β` with `β = (γ/2πR²)·S_{n₀}`. -/
theorem corotLin_dispersion (γ R : ℝ) (hN3 : 3 ≤ N) (ζ : ℂ) (h1 : ζ ^ N = 1)
    (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (hunit : Complex.normSq ζ = 1)
    (u v : ℕ → ℂ) (a b : ℝ)
    (hu : ∀ k, corotLin γ R N ζ u k = ((a : ℂ)) * u k - ((b : ℂ)) * v k)
    (hv : ∀ k, corotLin γ R N ζ v k = ((b : ℂ)) * u k + ((a : ℂ)) * v k)
    (n₀ : ℕ) (hn₀ : n₀ < N)
    (hP : @fmode N ζ u n₀ + Complex.I * @fmode N ζ v n₀ ≠ 0
      ∨ @fmode N ζ u n₀ - Complex.I * @fmode N ζ v n₀ ≠ 0) :
    ((a : ℂ) + Complex.I * (b : ℂ)) ^ 2 + ((ringOmega γ R N : ℝ) : ℂ) ^ 2
      = ((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ) * havS N ζ n₀
        * star (((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ) * havS N ζ n₀) := by
  obtain ⟨E1, E2⟩ := corotLin_pair_system γ R hN3 ζ h1 hunit u v ((a : ℂ)) ((b : ℂ)) hu hv n₀
  obtain ⟨E1', E2'⟩ := corotLin_pair_system γ R hN3 ζ h1 hunit u v ((a : ℂ)) ((b : ℂ)) hu hv
    (havSig N n₀)
  rw [havSig_inv N hN3 n₀ hn₀] at E1' E2'
  have hfold : ∀ (w : ℕ → ℂ) (p : ℕ),
      star (∑ j in Finset.range N, w j * star (ζ ^ (p * j))) = star (@fmode N ζ w p) :=
    fun _ _ => rfl
  rw [hfold u (havSig N n₀)] at E1
  rw [hfold v (havSig N n₀)] at E2
  rw [hfold u n₀] at E1'
  rw [hfold v n₀] at E2'
  rw [havS_sym (by omega) h1 hprim, Nat.mod_eq_of_lt hn₀] at E1 E2
  set Om : ℂ := ((ringOmega γ R N : ℝ) : ℂ) with hOmdef
  set c0 : ℂ := ((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ)
  set β : ℂ := c0 * havS N ζ n₀
  set C : ℂ := @fmode N ζ u n₀
  set D : ℂ := @fmode N ζ v n₀
  set Cm : ℂ := @fmode N ζ u (havSig N n₀)
  set Dm : ℂ := @fmode N ζ v (havSig N n₀)
  have hI2 : Complex.I * Complex.I + 1 = 0 := by rw [Complex.I_mul_I]; ring
  have hI : ((a : ℂ) + Complex.I * (Om + (b : ℂ))) * (C + Complex.I * D)
      = -Complex.I * β * (star Cm + Complex.I * star Dm) := by
    linear_combination E1 + Complex.I * E2 + ((b : ℂ) * D) * hI2
  have hII : ((a : ℂ) + Complex.I * (Om + (b : ℂ))) * (Cm + Complex.I * Dm)
      = -Complex.I * β * (star C + Complex.I * star D) := by
    linear_combination E1' + Complex.I * E2' + ((b : ℂ) * Dm) * hI2
  have hIII : ((a : ℂ) + Complex.I * (Om - (b : ℂ))) * (C - Complex.I * D)
      = -Complex.I * β * (star Cm - Complex.I * star Dm) := by
    linear_combination E1 - Complex.I * E2 + ((b : ℂ) * D) * hI2
  have hIV : ((a : ℂ) + Complex.I * (Om - (b : ℂ))) * (Cm - Complex.I * Dm)
      = -Complex.I * β * (star C - Complex.I * star D) := by
    linear_combination E1' - Complex.I * E2' + ((b : ℂ) * Dm) * hI2
  have hstarQ' : star (Cm - Complex.I * Dm) = star Cm + Complex.I * star Dm := by
    rw [star_sub, star_mul, starI']; ring
  have hstarQ : star (Cm + Complex.I * Dm) = star Cm - Complex.I * star Dm := by
    rw [star_add, star_mul, starI']; ring
  have hstarIV : star ((a : ℂ) + Complex.I * (Om - (b : ℂ)))
      * (star Cm + Complex.I * star Dm)
      = Complex.I * star β * (C + Complex.I * D) := by
    rw [← hstarQ', ← star_mul,
      mul_comm (Cm - Complex.I * Dm) ((a : ℂ) + Complex.I * (Om - (b : ℂ))), hIV]
    simp only [star_mul, star_sub, star_star, starI', star_neg, neg_neg]
    ring
  have hstarII : star ((a : ℂ) + Complex.I * (Om + (b : ℂ)))
      * (star Cm - Complex.I * star Dm)
      = Complex.I * star β * (C - Complex.I * D) := by
    rw [← hstarQ, ← star_mul,
      mul_comm (Cm + Complex.I * Dm) ((a : ℂ) + Complex.I * (Om + (b : ℂ))), hII]
    simp only [star_mul, star_add, star_star, starI', star_neg, neg_neg]
    ring
  have hstary : star ((a : ℂ) + Complex.I * (Om - (b : ℂ)))
      = ((a : ℂ)) - Complex.I * (Om - (b : ℂ)) := by
    rw [star_add, starR', hOmdef, ← Complex.ofReal_sub, star_CR]
    ring
  have hstarx : star ((a : ℂ) + Complex.I * (Om + (b : ℂ)))
      = ((a : ℂ)) - Complex.I * (Om + (b : ℂ)) := by
    rw [star_add, starR', hOmdef, ← Complex.ofReal_add, star_CR]
    ring
  have hxsy : ((a : ℂ) + Complex.I * (Om + (b : ℂ)))
      * (((a : ℂ)) - Complex.I * (Om - (b : ℂ)))
      = ((a : ℂ) + Complex.I * (b : ℂ)) ^ 2 + Om ^ 2 := by
    linear_combination (-(Om * Om)) * hI2
  have hysx : ((a : ℂ) + Complex.I * (Om - (b : ℂ)))
      * (((a : ℂ)) - Complex.I * (Om + (b : ℂ)))
      = ((a : ℂ) - Complex.I * (b : ℂ)) ^ 2 + Om ^ 2 := by
    linear_combination (-(Om * Om)) * hI2
  have hkey : ((a : ℂ) + Complex.I * (Om + (b : ℂ)))
      * star ((a : ℂ) + Complex.I * (Om - (b : ℂ))) * (C + Complex.I * D)
      = β * star β * (C + Complex.I * D) := by
    linear_combination (star ((a : ℂ) + Complex.I * (Om - (b : ℂ)))) * hI
      + (-(Complex.I * β)) * hstarIV
      + (-(β * star β * (C + Complex.I * D))) * hI2
  have hkey' : ((a : ℂ) + Complex.I * (Om - (b : ℂ)))
      * star ((a : ℂ) + Complex.I * (Om + (b : ℂ))) * (C - Complex.I * D)
      = β * star β * (C - Complex.I * D) := by
    linear_combination (star ((a : ℂ) + Complex.I * (Om + (b : ℂ)))) * hIII
      + (-(Complex.I * β)) * hstarII
      + (-(β * star β * (C - Complex.I * D))) * hI2
  rw [hstary] at hkey
  rw [hstarx] at hkey'
  rcases hP with hPne | hPne'
  · have hcon : ((a : ℂ) + Complex.I * (b : ℂ)) ^ 2 + Om ^ 2 = β * star β := by
      refine mul_right_cancel₀ hPne ?_
      rw [← hxsy]
      exact hkey
    exact hcon
  · have hcon' : ((a : ℂ) - Complex.I * (b : ℂ)) ^ 2 + Om ^ 2 = β * star β := by
      refine mul_right_cancel₀ hPne' ?_
      rw [← hysx]
      exact hkey'
    have hstarOm : star (Om ^ 2) = Om ^ 2 := by
      rw [star_pow, hOmdef, starR']
    have hfin := congrArg star hcon'
    rw [star_add, star_pow, hstarOm, star_sub, starR', star_CR b, sub_neg_eq_add,
      star_mul, star_star] at hfin
    exact hfin

/-- **The Havelock small-ring stability (TW5).** For `N ≤ 7` every eigenvalue
`ℓ = a + i·b` of the co-rotating linearization on nonzero spectral pairs is
purely imaginary: `a = 0` — a ring of at most seven point vortices supports no
growing co-rotating perturbation. -/
theorem corotLin_stable7 (γ R : ℝ) (hN3 : 3 ≤ N) (hN7 : N ≤ 7) (ζ : ℂ)
    (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1)
    (hunit : Complex.normSq ζ = 1) (u v : ℕ → ℂ)
    (hper_u : ∀ k, u k = u (k % N)) (hper_v : ∀ k, v k = v (k % N))
    (a b : ℝ)
    (hu : ∀ k, corotLin γ R N ζ u k = ((a : ℂ)) * u k - ((b : ℂ)) * v k)
    (hv : ∀ k, corotLin γ R N ζ v k = ((b : ℂ)) * u k + ((a : ℂ)) * v k)
    (huv : ∃ k, u k ≠ 0 ∨ v k ≠ 0) :
    a = 0 := by
  -- some mode n₀ < N carries a nonzero amplitude (Fourier inversion)
  have hfind : ∃ n₀ : ℕ, n₀ < N ∧ (@fmode N ζ u n₀ ≠ 0 ∨ @fmode N ζ v n₀ ≠ 0) := by
    by_contra hall
    push_neg at hall
    obtain ⟨k, hk⟩ := huv
    have hu0 : ∀ n ∈ Finset.range N, @fmode N ζ u n * ζ ^ (n * k) = 0 := fun n hn => by
      rw [(hall n (Finset.mem_range.mp hn)).1, zero_mul]
    have hv0 : ∀ n ∈ Finset.range N, @fmode N ζ v n * ζ ^ (n * k) = 0 := fun n hn => by
      rw [(hall n (Finset.mem_range.mp hn)).2, zero_mul]
    rcases hk with hku | hkv
    · refine hku ?_
      rw [fmode_inversion (by omega) h1 hprim hunit u hper_u k,
        Finset.sum_eq_zero hu0]
      simp
    · refine hkv ?_
      rw [fmode_inversion (by omega) h1 hprim hunit v hper_v k,
        Finset.sum_eq_zero hv0]
      simp
  obtain ⟨n₀, hn₀, hCD⟩ := hfind
  -- the pair P = C + iD or P' = C - iD is nonzero
  have hPdisj : @fmode N ζ u n₀ + Complex.I * @fmode N ζ v n₀ ≠ 0
      ∨ @fmode N ζ u n₀ - Complex.I * @fmode N ζ v n₀ ≠ 0 := by
    rcases hCD with hC | hD
    · by_contra hcon
      push_neg at hcon
      have h2C : (2 : ℂ) * @fmode N ζ u n₀
          = (@fmode N ζ u n₀ + Complex.I * @fmode N ζ v n₀)
            + (@fmode N ζ u n₀ - Complex.I * @fmode N ζ v n₀) := by ring
      rw [hcon.1, hcon.2, add_zero] at h2C
      exact hC (mul_right_cancel₀ (by norm_num : (2 : ℂ) ≠ 0)
        (by rw [mul_comm (@fmode N ζ u n₀) 2, zero_mul]; exact h2C))
    · by_contra hcon
      push_neg at hcon
      have h2D : (2 : ℂ) * Complex.I * @fmode N ζ v n₀
          = (@fmode N ζ u n₀ + Complex.I * @fmode N ζ v n₀)
            - (@fmode N ζ u n₀ - Complex.I * @fmode N ζ v n₀) := by ring
      rw [hcon.1, hcon.2, sub_zero] at h2D
      have h2I : (2 : ℂ) * Complex.I ≠ 0 := by
        intro hz
        rcases mul_eq_zero.mp hz with h2 | hI0
        · norm_num at h2
        · exact Complex.I_ne_zero hI0
      exact hD (mul_right_cancel₀ h2I (by
        rw [mul_comm (@fmode N ζ v n₀) ((2 : ℂ) * Complex.I), h2D, zero_mul]))
  -- the dispersion relation at n₀
  have hdisp := corotLin_dispersion γ R hN3 ζ h1 hprim hunit u v a b hu hv n₀ hn₀ hPdisj
  -- real currency: β·conj β = c0r² · r² with r² ≤ ((N−1)/2)², and c0r·(N−1)/2 = Ω
  set c0r : ℝ := γ / (2 * Real.pi * R ^ 2) with hc0r
  obtain ⟨r, hrSq, hrBound⟩ := havS_real_sq (by omega) hN7 h1 hprim n₀ hn₀
  have hstarβ : star (c0r * havS N ζ n₀) = c0r * star (havS N ζ n₀) := by
    rw [star_mul, starR', mul_comm]
  have hβsq : (c0r * havS N ζ n₀) * star (c0r * havS N ζ n₀)
      = ((((c0r * c0r) * r ^ 2 : ℝ)) : ℂ) := by
    rw [hstarβ, mul_mul_mul_comm, ← Complex.ofReal_mul, hrSq, ← Complex.ofReal_mul]
  have hOm : c0r * (((N - 1 : ℕ) : ℝ) / 2) = ringOmega γ R N := by
    rw [hc0r, ringOmega]
    field_simp
    ring
  have hbound : (c0r * c0r) * r ^ 2 ≤ ringOmega γ R N ^ 2 := by
    rw [← hOm]
    calc (c0r * c0r) * r ^ 2
        ≤ (c0r * c0r) * (((N - 1 : ℕ) : ℝ) / 2) ^ 2 :=
          mul_le_mul_of_nonneg_left hrBound (mul_self_nonneg c0r)
      _ = (c0r * (((N - 1 : ℕ) : ℝ) / 2)) ^ 2 := by ring
  rw [hβsq] at hdisp
  have hΩre : Complex.re (((ringOmega γ R N : ℝ) : ℂ) ^ 2) = ringOmega γ R N ^ 2 := by
    rw [pow_two, Complex.mul_re]
    simp only [Complex.ofReal_re, Complex.ofReal_im]
    ring
  have hΩim : Complex.im (((ringOmega γ R N : ℝ) : ℂ) ^ 2) = 0 := by
    rw [pow_two, Complex.mul_im]
    simp only [Complex.ofReal_re, Complex.ofReal_im]
    ring
  have himsq : Complex.im (((a : ℂ) + Complex.I * (b : ℂ)) ^ 2) = 2 * a * b := by
    rw [pow_two, Complex.mul_im]
    simp only [Complex.add_re, Complex.add_im, Complex.mul_re, Complex.mul_im,
      Complex.ofReal_re, Complex.ofReal_im, Complex.I_re, Complex.I_im]
    ring
  have hresq : Complex.re (((a : ℂ) + Complex.I * (b : ℂ)) ^ 2) = a ^ 2 - b ^ 2 := by
    rw [pow_two, Complex.mul_re]
    simp only [Complex.add_re, Complex.add_im, Complex.mul_re, Complex.mul_im,
      Complex.ofReal_re, Complex.ofReal_im, Complex.I_re, Complex.I_im]
    ring
  have hab : a * b = 0 := by
    have hI := congrArg Complex.im hdisp
    rw [Complex.add_im, himsq, hΩim, Complex.ofReal_im, add_zero] at hI
    rcases mul_eq_zero.mp hI with h2a | hb
    · have ha0 : a = 0 :=
        mul_left_cancel₀ (by norm_num : (2 : ℝ) ≠ 0) (by rw [mul_zero]; exact h2a)
      rw [ha0, zero_mul]
    · rw [hb, mul_zero]
  have hre : a ^ 2 - b ^ 2 + ringOmega γ R N ^ 2 = (c0r * c0r) * r ^ 2 := by
    have hR := congrArg Complex.re hdisp
    rw [Complex.add_re, hresq, hΩre, Complex.ofReal_re] at hR
    exact hR
  rcases mul_eq_zero.mp hab with ha | hb
  · exact ha
  · rw [hb, zero_pow (by norm_num : (2 : ℕ) ≠ 0), sub_zero] at hre
    have ha2 : a ^ 2 ≤ 0 := by
      have h2 : a ^ 2 + ringOmega γ R N ^ 2 ≤ ringOmega γ R N ^ 2 :=
        le_trans (le_of_eq hre) hbound
      linarith
    exact sq_eq_zero_iff.mp (le_antisymm ha2 (by positivity))

/-! #### The spectral layer (TW5): eigenpairs, stability, witness. -/

/-- Spectral value of the `N`-periodic pair layer: `ℓ = a + i·b` acts on a pair
`(u, v)` of `N`-periodic configurations, not both identically zero, through the
ℝ-linear rotation `u ↦ a·u − b·v`, `v ↦ b·u + a·v`. -/
def eigenvalueOf' (γ R : ℝ) (N : ℕ) (ζ : ℂ) (ℓ : ℂ) : Prop :=
  ∃ u v : ℕ → ℂ,
    (∀ k, u k = u (k % N)) ∧ (∀ k, v k = v (k % N)) ∧
    (u ≠ 0 ∨ v ≠ 0) ∧
    ∀ k, corotLin γ R N ζ u k = ((ℓ.re : ℝ) : ℂ) * u k - ((ℓ.im : ℝ) : ℂ) * v k
      ∧ corotLin γ R N ζ v k = ((ℓ.im : ℝ) : ℂ) * u k + ((ℓ.re : ℝ) : ℂ) * v k

/-- **Havelock stability (TW5):** every spectral value of the `N`-periodic pair
layer of the co-rotating linearization has nonpositive real part. -/
def havelockStable (γ R : ℝ) (N : ℕ) (ζ : ℂ) : Prop :=
  ∀ ℓ : ℂ, eigenvalueOf' γ R N ζ ℓ → ℓ.re ≤ 0

/-- `corotLin` annihilates the zero configuration. -/
private theorem corotLin_zero (γ R : ℝ) (N : ℕ) (ζ : ℂ) (k : ℕ) :
    corotLin γ R N ζ (fun _ => (0:ℂ)) k = 0 := by
  simp [corotLin]

/-- **TW5 (small-ring stability).** For `3 ≤ N ≤ 7` the co-rotating
linearization of the regular ring is Havelock-stable. -/
theorem havelockStable_small (γ R : ℝ) (hN3 : 3 ≤ N) (hN7 : N ≤ 7) (ζ : ℂ)
    (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1)
    (hunit : Complex.normSq ζ = 1) : havelockStable γ R N ζ := by
  intro ℓ hval
  obtain ⟨u, v, hpu, hpv, hne, hsys⟩ := hval
  have hu : ∀ k, corotLin γ R N ζ u k = ((ℓ.re : ℝ) : ℂ) * u k - ((ℓ.im : ℝ) : ℂ) * v k :=
    fun k => (hsys k).1
  have hv : ∀ k, corotLin γ R N ζ v k = ((ℓ.im : ℝ) : ℂ) * u k + ((ℓ.re : ℝ) : ℂ) * v k :=
    fun k => (hsys k).2
  have hne' : ∃ k, u k ≠ 0 ∨ v k ≠ 0 := by
    rcases hne with h0 | h0
    · obtain ⟨k, hk⟩ := Function.ne_iff.mp h0
      exact ⟨k, Or.inl hk⟩
    · obtain ⟨k, hk⟩ := Function.ne_iff.mp h0
      exact ⟨k, Or.inr hk⟩
  rw [corotLin_stable7 γ R hN3 hN7 ζ h1 hprim hunit u v hpu hpv ℓ.re ℓ.im hu hv hne']

/-- Swapped form of `zinv_mul_zeta_pow`: `ζ^{c·k}·zinv(a·k) = ζ^{((c % N + N − a % N) % N)·k}`. -/
private theorem zeta_zinv_pow (hN : N ≠ 0) (h1 : ζ ^ N = 1) (a c k : ℕ) :
    ζ ^ (c * k) * zinv N ζ (a * k) = ζ ^ (((c % N + N - a % N) % N) * k) := by
  rw [mul_comm (ζ ^ (c * k)) (zinv N ζ (a * k)), zinv_mul_zeta_pow hN h1 a k c]

/-- The per-`d` index-shift identity behind the Havelock witness:
`zinv(j·((k + N − d) % N)) = zinv(j·k)·ζ^{j·d}`. -/
private theorem zinv_shift (hN : N ≠ 0) (h1 : ζ ^ N = 1) (j k d : ℕ) (hdN : d < N) :
    zinv N ζ (j * ((k + N - d) % N)) = zinv N ζ (j * k) * ζ ^ (j * d) := by
  unfold zinv
  rw [← pow_add]
  refine pow_congr_mod h1 ?_
  have hA : ((k + N - d) % N + d) % N = k % N := by
    have h1a : ((k + N - d) % N + d) % N = ((k + N - d) + d) % N :=
      Nat.ModEq.add_right d (Nat.mod_modEq (k + N - d) N)
    rw [h1a, show (((k + N - d) + d : ℕ) = k + N) from by omega, Nat.add_mod_right k N]
  have hshift : (j * ((k + N - d) % N) + j * d) % N = (j * k) % N := by
    have hAm : ((k + N - d) % N + d) ≡ k [MOD N] := hA
    have h2 := hAm.mul_left j
    rw [Nat.mul_add] at h2
    exact h2
  have hE2 : ((N - (j * k) % N) % N + j * d + j * ((k + N - d) % N)) % N = 0 := by
    rw [Nat.add_assoc, Nat.add_comm (j * d) (j * ((k + N - d) % N))]
    have hAm2 : (j * ((k + N - d) % N) + j * d) ≡ j * k [MOD N] := hshift
    have h3 : ((N - (j * k) % N) % N + (j * ((k + N - d) % N) + j * d)) % N
        = ((N - (j * k) % N) % N + j * k) % N := hAm2.add_left ((N - (j * k) % N) % N)
    rw [h3, key_mod_eq hN (j * k)]
  have hE1 : ((N - (j * ((k + N - d) % N)) % N) % N + j * ((k + N - d) % N)) % N = 0 :=
    key_mod_eq hN _
  have hE1m : ((N - (j * ((k + N - d) % N)) % N) % N + j * ((k + N - d) % N)) ≡ 0 [MOD N] := hE1
  have hE2m : ((N - (j * k) % N) % N + j * d + j * ((k + N - d) % N)) ≡ 0 [MOD N] := hE2
  exact Nat.ModEq.add_right_cancel' (j * ((k + N - d) % N)) (hE1m.trans hE2m.symm)

/-- **TW5 (the Havelock instability, witness).** For `N ≥ 8` (with `γ > 0`,
`R ≠ 0`) the co-rotating linearization of the regular `N`-gon ring admits a
spectral value with strictly positive real part: the Havelock growing mode. -/
theorem havelock_witness (γ R : ℝ) (hN8 : 8 ≤ N) (hR : R ≠ 0) (hγ : 0 < γ)
    (ζ : ℂ) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1)
    (hunit : Complex.normSq ζ = 1) :
    ∃ ℓ : ℂ, eigenvalueOf' γ R N ζ ℓ ∧ 0 < ℓ.re := by
  have hN0 : N ≠ 0 := by omega
  have hn0lt : (N - 3 : ℕ) < N := by omega
  have h5lt : (5 : ℕ) < N := by omega
  -- the real currency
  set c0r : ℝ := γ / (2 * Real.pi * R ^ 2) with hc0rdef
  have hc0rpos : (0:ℝ) < c0r := by
    rw [hc0rdef]
    exact div_pos hγ (by positivity)
  set nn0 : ℕ := N - 3 with hn0def
  set sval : ℝ := ((2:ℝ) - ((nn0:ℕ):ℝ)) * (((N:ℕ):ℝ) - ((nn0:ℕ):ℝ)) / 2 with hsvaldef
  set β : ℝ := c0r * sval with hβdef
  set Ω0 : ℝ := (((N - 1 : ℕ) : ℝ) / 2) with hΩ0def
  -- closed form of the block sum at the witness mode
  have hSre : havS N ζ nn0 = ((sval : ℝ) : ℂ) := by
    rw [havS_closed (by omega) h1 hprim nn0 (by omega) (by omega), hsvaldef]
    push_cast
    ring
  have hsig : havSig N nn0 = 5 := by
    rw [havSig, Nat.mod_eq_of_lt hn0lt, hn0def,
      show ((2 + N - (N - 3) : ℕ) = 5) from by omega,
      Nat.mod_eq_of_lt h5lt]
  have hSm : havS N ζ 5 = havS N ζ nn0 := by
    have hsy := havS_sym (by omega) h1 hprim nn0
    rw [hsig, Nat.mod_eq_of_lt hn0lt] at hsy
    exact hsy
  -- the threshold identity Ω = c0r·(N−1)/2 and the gap β² > Ω²
  have hOm : ringOmega γ R N = c0r * Ω0 := by
    rw [hc0rdef, ringOmega, hΩ0def]
    ring
  have hsN8 : (8:ℝ) ≤ ((N:ℕ):ℝ) := by exact_mod_cast hN8
  have hnn0cast : ((nn0:ℕ):ℝ) = ((N:ℕ):ℝ) - 3 := by
    rw [hn0def, Nat.cast_sub (by omega)]
    norm_num
  have hsvalform : sval = ((5 - ((N:ℕ):ℝ)) * 3) / 2 := by
    rw [hsvaldef, hnn0cast]
    ring
  have hB : Ω0 < -sval := by
    rw [hsvalform, hΩ0def, Nat.cast_sub (by omega)]; push_cast; linarith
  have hC : (0:ℝ) ≤ Ω0 := by
    rw [hΩ0def]; positivity
  have hgap : Ω0 ^ 2 < sval ^ 2 := by
    have hP : (-sval - Ω0) * (-sval + Ω0) = sval ^ 2 - Ω0 ^ 2 := by ring
    have hpos : (0:ℝ) < (-sval - Ω0) * (-sval + Ω0) :=
      mul_pos (show (0:ℝ) < -sval - Ω0 from by linarith)
        (show (0:ℝ) < -sval + Ω0 from by linarith)
    have hpos2 : (0:ℝ) < sval ^ 2 - Ω0 ^ 2 := by rw [← hP]; exact hpos
    linarith
  have hlamSqpos : (0:ℝ) < β * β - ringOmega γ R N * ringOmega γ R N := by
    have h1 : β * β - ringOmega γ R N * ringOmega γ R N
        = c0r * c0r * (sval ^ 2 - Ω0 ^ 2) := by
      rw [hβdef, hOm]
      ring
    rw [h1]
    exact mul_pos (mul_pos hc0rpos hc0rpos) (sub_pos.mpr hgap)
  set lam : ℝ := Real.sqrt (β * β - ringOmega γ R N * ringOmega γ R N)
  have hlampos : (0:ℝ) < lam := Real.sqrt_pos.mpr hlamSqpos
  have hlam0 : lam ≠ 0 := ne_of_gt hlampos
  have hlamMul : lam * lam = β * β - ringOmega γ R N * ringOmega γ R N :=
    Real.mul_self_sqrt (le_of_lt hlamSqpos)
  set p : ℝ := (ringOmega γ R N - β) / lam with hpdef
  -- the scalar identity behind the growing mode
  have hcf : (((c0r : ℝ) : ℂ)) * (((sval : ℝ) : ℂ)) = ((β : ℝ) : ℂ) := by
    rw [← Complex.ofReal_mul, ← hβdef]
  have hP : ringOmega γ R N - β = lam * p := by
    rw [hpdef, div_eq_inv_mul, mul_inv_cancel_left₀ hlam0]
  have hQ : p * (ringOmega γ R N + β) = -lam := by
    refine mul_left_cancel₀ hlam0 ?_
    rw [hpdef, ← mul_assoc, div_eq_inv_mul, mul_inv_cancel_left₀ hlam0, mul_neg, hlamMul]
    ring
  have hI2 : Complex.I * Complex.I = -(1:ℂ) := Complex.I_mul_I
  have hPc : ((ringOmega γ R N : ℝ) : ℂ) - ((β : ℝ) : ℂ)
      = ((lam : ℝ) : ℂ) * ((p : ℝ) : ℂ) := by
    rw [← Complex.ofReal_mul, ← Complex.ofReal_sub]
    exact congrArg Complex.ofReal hP
  have hQc : ((p : ℝ) : ℂ) * (((ringOmega γ R N : ℝ) : ℂ) + ((β : ℝ) : ℂ))
      + ((lam : ℝ) : ℂ) = 0 := by
    have h1 : ((p * (ringOmega γ R N + β) : ℝ) : ℂ) = ((-lam : ℝ) : ℂ) :=
      congrArg Complex.ofReal hQ
    rw [Complex.ofReal_mul, Complex.ofReal_add, Complex.ofReal_neg] at h1
    linear_combination h1
  have hscal : (-(Complex.I)) * ((ringOmega γ R N : ℝ) : ℂ) * (((p : ℝ) : ℂ) + Complex.I)
      - (Complex.I) * ((β : ℝ) : ℂ) * (((p : ℝ) : ℂ) - Complex.I)
      = ((lam : ℝ) : ℂ) * (((p : ℝ) : ℂ) + Complex.I) := by
    linear_combination (((β : ℝ) : ℂ) - ((ringOmega γ R N : ℝ) : ℂ)) * hI2 + hPc
      + (-(Complex.I)) * hQc
  -- the eigenmode and its bookkeeping
  set u : ℕ → ℂ := fun k => (((p : ℝ) : ℂ) + Complex.I) * (ζ ^ (nn0 * k) + ζ ^ (5 * k))
  set v : ℕ → ℂ := fun _ => (0:ℂ)
  have hpowmod : ∀ (j k : ℕ), ζ ^ (j * (k % N)) = ζ ^ (j * k) := by
    intro j k
    refine pow_congr_mod h1 ?_
    exact (Nat.mod_modEq k N).mul_left j
  have huApp : ∀ k : ℕ, u k = (((p : ℝ) : ℂ) + Complex.I) * (ζ ^ (nn0 * k) + ζ ^ (5 * k)) :=
    fun _ => rfl
  have huper : ∀ k, u k = u (k % N) := by
    intro k
    rw [huApp k, huApp (k % N), hpowmod nn0 k, hpowmod 5 k]
  have hvper : ∀ k, v k = v (k % N) := fun _ => rfl
  have hcne : (((p : ℝ) : ℂ) + Complex.I) ≠ 0 := by
    intro hz
    have him : Complex.im (((p : ℝ) : ℂ) + Complex.I) = 1 := by
      rw [Complex.add_im, Complex.ofReal_im, Complex.I_im]
      ring
    rw [hz, Complex.zero_im] at him
    exact absurd him (by norm_num)
  have hu0 : u 0 = (((p : ℝ) : ℂ) + Complex.I) * 2 := by
    rw [huApp 0, Nat.mul_zero, Nat.mul_zero, pow_zero]
    norm_num
  have hune : u ≠ 0 := by
    intro hz
    have h1 : u 0 = 0 := congrFun hz 0
    rw [hu0] at h1
    exact mul_ne_zero hcne (by norm_num) h1
  -- the two per-`k` power collapses
  have hzA : ∀ k : ℕ, ζ ^ (2 * k) * zinv N ζ (nn0 * k) = ζ ^ (5 * k) := by
    intro k
    rw [zeta_zinv_pow hN0 h1 nn0 2 k,
      show ((2 % N + N - nn0 % N) % N : ℕ) = 5 from by
        rw [Nat.mod_eq_of_lt (show (2:ℕ) < N by omega), Nat.mod_eq_of_lt hn0lt, hn0def,
          show ((2 + N - (N - 3) : ℕ) = 5) from by omega,
          Nat.mod_eq_of_lt h5lt]]
  have hzB : ∀ k : ℕ, ζ ^ (2 * k) * zinv N ζ (5 * k) = ζ ^ (nn0 * k) := by
    intro k
    rw [zeta_zinv_pow hN0 h1 5 2 k,
      show ((2 % N + N - 5 % N) % N : ℕ) = nn0 from by
        rw [Nat.mod_eq_of_lt (show (2:ℕ) < N by omega), Nat.mod_eq_of_lt h5lt,
          show ((2 + N - 5 : ℕ) = N - 3) from by omega,
          ← hn0def, Nat.mod_eq_of_lt hn0lt]]
  -- conjugation of the mode, pointwise
  have hstar : ∀ k : ℕ, star (u k)
      = (((p : ℝ) : ℂ) - Complex.I) * (zinv N ζ (nn0 * k) + zinv N ζ (5 * k)) := by
    intro k
    rw [huApp k, star_mul, star_add ((p : ℝ) : ℂ) Complex.I, starR', starI',
      star_add, star_zeta_pow hN0 h1 hunit, star_zeta_pow hN0 h1 hunit]
    ring
  have hstar' : ∀ (k d : ℕ), d < N →
      star (u ((k + N - d) % N))
      = (((p : ℝ) : ℂ) - Complex.I)
        * (zinv N ζ (nn0 * k) * ζ ^ (nn0 * d) + zinv N ζ (5 * k) * ζ ^ (5 * d)) := by
    intro k d hdN
    rw [huApp ((k + N - d) % N), star_mul, star_add ((p : ℝ) : ℂ) Complex.I, starR', starI',
      star_add, star_zeta_pow hN0 h1 hunit, star_zeta_pow hN0 h1 hunit,
      zinv_shift hN0 h1 nn0 k d hdN, zinv_shift hN0 h1 5 k d hdN]
    ring
  have hfold : ∀ (a : ℂ) (j : ℕ),
      ∑ d in Finset.Ico 1 N, a * ((1 - ζ ^ (j * d)) / (1 - ζ ^ d) ^ 2)
      = a * havS N ζ j := fun a j =>
    (Finset.mul_sum (Finset.Ico 1 N) (fun d => (1 - ζ ^ (j * d)) / (1 - ζ ^ d) ^ 2) a).symm
  -- the displacement sum collapses to the block sum
  have hcore : ∀ k : ℕ, ζ ^ (2 * k) * ∑ d in Finset.Ico 1 N,
      (star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2
      = ((sval : ℝ) : ℂ) * (((p : ℝ) : ℂ) - Complex.I) * (ζ ^ (nn0 * k) + ζ ^ (5 * k)) := by
    intro k
    have hper2 : ∀ d ∈ Finset.Ico 1 N,
        ζ ^ (2 * k) * ((star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2)
        = (((p : ℝ) : ℂ) - Complex.I) * (ζ ^ (2 * k) * zinv N ζ (nn0 * k))
            * ((1 - ζ ^ (nn0 * d)) / (1 - ζ ^ d) ^ 2)
          + (((p : ℝ) : ℂ) - Complex.I) * (ζ ^ (2 * k) * zinv N ζ (5 * k))
            * ((1 - ζ ^ (5 * d)) / (1 - ζ ^ d) ^ 2) := by
      intro d hdN
      have hdNlt : d < N := (Finset.mem_Ico.mp hdN).2
      rw [hstar k, hstar' k d hdNlt]
      ring
    rw [Finset.mul_sum, Finset.sum_congr rfl hper2, Finset.sum_add_distrib]
    rw [hfold ((((p : ℝ) : ℂ) - Complex.I) * (ζ ^ (2 * k) * zinv N ζ (nn0 * k))) nn0]
    rw [hfold ((((p : ℝ) : ℂ) - Complex.I) * (ζ ^ (2 * k) * zinv N ζ (5 * k))) 5]
    rw [hzA, hzB, hSm, hSre]
    ring
  have hsum : ∀ k : ℕ, Complex.I * ((c0r : ℝ) : ℂ) * ζ ^ (2 * k)
      * ∑ d in Finset.Ico 1 N,
        (star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2
      = Complex.I * ((β : ℝ) : ℂ) * (((p : ℝ) : ℂ) - Complex.I)
        * (ζ ^ (nn0 * k) + ζ ^ (5 * k)) := by
    intro k
    rw [mul_assoc (Complex.I * ((c0r : ℝ) : ℂ)) (ζ ^ (2 * k))
        (∑ d in Finset.Ico 1 N,
          (star (u k) - star (u ((k + N - d) % N))) / (1 - ζ ^ d) ^ 2)]
    rw [hcore k]
    linear_combination (Complex.I * (((p : ℝ) : ℂ) - Complex.I)
        * (ζ ^ (nn0 * k) + ζ ^ (5 * k))) * hcf
  have hmain : ∀ k : ℕ, corotLin γ R N ζ u k = ((lam : ℝ) : ℂ) * u k := by
    intro k
    rw [corotLin, ← hc0rdef, hsum k, huApp k]
    linear_combination (ζ ^ (nn0 * k) + ζ ^ (5 * k)) * hscal
  refine ⟨((lam : ℝ) : ℂ), ⟨u, v, huper, hvper, Or.inl hune, ?_⟩, ?_⟩
  · intro k
    refine ⟨?_, ?_⟩
    · rw [Complex.ofReal_re, Complex.ofReal_im, Complex.ofReal_zero, zero_mul, sub_zero]
      exact hmain k
    · have hvk : v k = (0:ℂ) := rfl
      have hvc : corotLin γ R N ζ v k = 0 := corotLin_zero γ R N ζ k
      rw [hvc, hvk, Complex.ofReal_im, Complex.ofReal_zero, zero_mul,
        Complex.ofReal_re, mul_zero, add_zero]
  · rw [Complex.ofReal_re]
    exact hlampos

/-- The canonical root lies on the unit circle. -/
theorem rootExp_unit : Complex.normSq (rootExp N) = 1 := by
  have harg : ((2 * Real.pi * Complex.I / (N : ℂ) : ℂ))
      = Complex.I * ((2 * Real.pi / (N : ℝ) : ℝ) : ℂ) := by
    rw [← Complex.ofReal_nat_cast, Complex.ofReal_div, Complex.ofReal_mul]
    push_cast
    ring
  unfold rootExp
  rw [harg]
  exact normSq_exp_I_mul (2 * Real.pi / (N : ℝ))

end HavelockSetup

/-!
### § 5. Theorem E: the co-rotating linearization and the Havelock classification

The exact W4 objects: the co-rotating field, its linearization at the ring,
the orbit-direction kernel certificate, and the Havelock classification.
The spectral proof (milestone TW5) is carried out in the spectral machinery
section § 4′ above; the classification below is a theorem, and the generic
spectral predicates `eigenvalueOf`/`eigenvalueOf'` are retained as the
recorded statement layer of the parent monograph.
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

/-- **Theorem E (milestone TW5, proven):** the Havelock classification — the
regular `N`-gon ring (`N ≥ 3`) is Havelock-stable exactly while `N ≤ 7`.
The stability half is `havelockStable_small` (via `corotLin_dispersion` and
`corotLin_stable7`: the dispersion relation forces `ℓ² + Ω² = β·conj β`
with `|β| ≤ Ω` for `N ≤ 7`); the instability half is `havelock_witness`
(the Havelock growing mode `λ = √(β² − Ω²) > 0` at the mode pair
`n₀ = N − 3`, `m = 5`). -/
theorem havelockClassification (γ R : ℝ) (hN3 : 3 ≤ N) (hR : R ≠ 0) (hγ : 0 < γ) :
    havelockStable γ R N (rootExp N) ↔ N ≤ 7 := by
  constructor
  · intro hstable
    by_contra hge
    have hN8 : 8 ≤ N := by omega
    obtain ⟨ℓ, hval, hpos⟩ := havelock_witness γ R hN8 hR hγ (rootExp N)
      (rootExp_pow (by omega)) (rootExp_prim (by omega)) (rootExp_unit)
    have h1 := hstable ℓ hval
    linarith
  · intro hle7
    exact havelockStable_small γ R hN3 hle7 (rootExp N) (rootExp_pow (by omega))
      (rootExp_prim (by omega)) (rootExp_unit)

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

#print axioms fmode_inversion
#print axioms havSig_inv
#print axioms havS_closed
#print axioms havS_sym
#print axioms havS_real_sq
#print axioms corotLin_orbit_kernel
#print axioms corotLin_proj
#print axioms corotLin_pair_system
#print axioms corotLin_dispersion
#print axioms corotLin_stable7
#print axioms havelockStable_small
#print axioms havelock_witness
#print axioms rootExp_unit
#print axioms havelockClassification

end AxiomFootprint

end Polyvortex


















