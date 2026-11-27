/-
TW5 scratch chunk 1: Fourier machinery over a primitive root of unity.
SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
-/
import Polyvortex

namespace Polyvortex

open scoped BigOperators

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

private theorem normSq_pow_eq (z : ℂ) : ∀ n : ℕ,
    Complex.normSq (z ^ n) = Complex.normSq z ^ n
  | 0 => by simp
  | n + 1 => by
    rw [pow_succ, pow_succ, Complex.normSq_mul, normSq_pow_eq z n]

/-- Conjugate of a power of the root is the inverse power. -/
theorem star_ζ_pow (m : ℕ) : star (ζ ^ m) = zinv N ζ m := by
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
    rw [star_ζ_pow hN h1 hunit]
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

private theorem ringPos_eq (R : ℝ) (ζ : ℂ) (k : ℕ) : ringPos R ζ k = (R : ℂ) * ζ ^ k := rfl

/-- `star` is conjugation on the ring constants. -/
private theorem starI' : star Complex.I = -Complex.I :=
  Complex.conj_I

private theorem starR' (r : ℝ) : star (r : ℂ) = (r : ℂ) :=
  Complex.conj_ofReal r

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

private theorem ImulnegI (x : ℂ) : Complex.I * (-(Complex.I * x)) = x := by
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
      star_ζ_pow hN0 h1 hunit k]
    ring
  have husd : ∀ d ∈ Finset.Ico 1 N,
      star (u ((k + N - d) % N)) = -(Complex.I * (R : ℂ)) * star (ζ ^ k) * ζ ^ d := by
    intro d hd
    have hd1 : 1 ≤ d := (Finset.mem_Ico.mp hd).1
    have hdN : d < N := (Finset.mem_Ico.mp hd).2
    have hze : ζ ^ ((k + N - d) % N) = ζ ^ (k + N - d) :=
      pow_congr_mod h1 (Nat.mod_modEq _ _)
    have hNd : ζ ^ (N - d) = star (ζ ^ d) := by
      rw [star_ζ_pow hN0 h1 hunit d]
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
    rw [star_ζ_pow hN0 h1 hunit k, mul_comm, zinv_mul hN0 h1 k]
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
      ← mul_assoc, ← mul_assoc, ImulnegI]
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
  rw [star_ζ_pow hN0 h1 hunit (n * j), mul_comm (ζ ^ (2 * j)) (zinv N ζ (n * j)),
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
  set c0 : ℂ := ((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ) with hc0def
  set β : ℂ := c0 * havS N ζ n₀ with hβdef
  set C : ℂ := @fmode N ζ u n₀ with hCdef
  set D : ℂ := @fmode N ζ v n₀ with hDdef
  set Cm : ℂ := @fmode N ζ u (havSig N n₀) with hCmdef
  set Dm : ℂ := @fmode N ζ v (havSig N n₀) with hDmdef
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
  have hN3 : 3 ≤ N := by omega
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
  have hA : (0:ℝ) < -sval := by
    rw [hsvalform]; push_cast; linarith
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
  set lam : ℝ := Real.sqrt (β * β - ringOmega γ R N * ringOmega γ R N) with hlamdef
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
  set u : ℕ → ℂ := fun k => (((p : ℝ) : ℂ) + Complex.I) * (ζ ^ (nn0 * k) + ζ ^ (5 * k)) with hudef
  set v : ℕ → ℂ := fun _ => (0:ℂ) with hvdef
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
      star_add, star_ζ_pow hN0 h1 hunit, star_ζ_pow hN0 h1 hunit]
    ring
  have hstar' : ∀ (k d : ℕ), d < N →
      star (u ((k + N - d) % N))
      = (((p : ℝ) : ℂ) - Complex.I)
        * (zinv N ζ (nn0 * k) * ζ ^ (nn0 * d) + zinv N ζ (5 * k) * ζ ^ (5 * d)) := by
    intro k d hdN
    rw [huApp ((k + N - d) % N), star_mul, star_add ((p : ℝ) : ℂ) Complex.I, starR', starI',
      star_add, star_ζ_pow hN0 h1 hunit, star_ζ_pow hN0 h1 hunit,
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
theorem rootExp_unit (hN : N ≠ 0) : Complex.normSq (rootExp N) = 1 := by
  have harg : ((2 * Real.pi * Complex.I / (N : ℂ) : ℂ))
      = Complex.I * ((2 * Real.pi / (N : ℝ) : ℝ) : ℂ) := by
    rw [← Complex.ofReal_nat_cast, Complex.ofReal_div, Complex.ofReal_mul]
    push_cast
    ring
  unfold rootExp
  rw [harg]
  exact normSq_exp_I_mul (2 * Real.pi / (N : ℝ))

/-- **Theorem E (TW5, proven):** the Havelock classification — the regular
`N`-gon ring of vortices (`N ≥ 3`) is Havelock-stable exactly while `N ≤ 7`:
for `N ≤ 7` every spectral value of the co-rotating linearization on the
`N`-periodic pair layer is purely imaginary, while for `N ≥ 8` the Havelock
growing mode provides a spectral value with strictly positive real part. -/
theorem havelock_classification (γ R : ℝ) (hN3 : 3 ≤ N) (hR : R ≠ 0) (hγ : 0 < γ) :
    havelockStable γ R N (rootExp N) ↔ N ≤ 7 := by
  constructor
  · intro hstable
    by_contra hge
    have hN8 : 8 ≤ N := by omega
    obtain ⟨ℓ, hval, hpos⟩ := havelock_witness γ R hN8 hR hγ (rootExp N)
      (rootExp_pow (by omega)) (rootExp_prim (by omega)) (rootExp_unit (by omega))
    have h1 := hstable ℓ hval
    linarith
  · intro hle7
    exact havelockStable_small γ R hN3 hle7 (rootExp N) (rootExp_pow (by omega))
      (rootExp_prim (by omega)) (rootExp_unit (by omega))

end HavelockSetup

end Polyvortex
