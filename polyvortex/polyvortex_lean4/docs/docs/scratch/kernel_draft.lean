/-
Kernel-draft: TW3 kernel certificate (карантин — 2 оставшиеся ошибки в hNd:
omega на `0 < d` с hd : d ∈ Ico 1 N в контексте и хвост ring; текст ниже
предназначен для вставки в chkE.lean внутрь section HavelockSetup).
Контекст-факты, которые уже собраны и работают: starI'/starR' (через
Complex.conj_I/conj_ofReal + exact-дефэка), ringPos_eq (rfl), hzsq, hz2k, hOm,
hsum (hperd + ← mul_sum + mul_one_div + sum_Ico1 + sum_roots_of_unity),
husk (ЗЕЛЁН — simp only [hu] + ringPos_eq + star_ζ_pow hN0 h1 hunit k),
husd (почти зелён — остался hNd).
Урок: omega НЕ доказывает `0 < d` из `d ∈ Ico 1 N` — нужен явный
`have hd1 : 1 ≤ d := (Finset.mem_Ico.mp hd).1` ДО by-omega (сделано), и
`Nat.sub_lt (hN0') (hd1)` вместо omega для `N − d < N` (сделано — след. ошибка
в цепочке Nat.mod_eq_of_lt (Nat.sub_lt ...) — см. лог).
-/
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
    have hdN : d < N := (Finset.mem_Ico.mp hd).2
    have hze : ζ ^ ((k + N - d) % N) = ζ ^ (k + N - d) :=
      pow_congr_mod h1 (Nat.mod_modEq _ _)
    have hNd : ζ ^ (N - d) = star (ζ ^ d) := by
      rw [star_ζ_pow hN0 h1 hunit d]
      show ζ ^ (N - d) = ζ ^ ((N - d % N) % N)
      rw [show ((d % N : ℕ) = d) from Nat.mod_eq_of_lt hdN,
        show (((N - d) % N : ℕ) = N - d) from
          Nat.mod_eq_of_lt (Nat.sub_lt (by omega) (by omega))]
    simp only [hu]
    rw [ringPos_eq, star_mul, star_mul, starI', starR',
      hze, show ((k + N - d : ℕ) = k + (N - d)) from by ring, pow_add, star_mul, hNd,
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
      rw [husk, husd d hd, show ((1 - ζ ^ d) ^ 2 : ℂ) = (1 - ζ ^ d) * (1 - ζ ^ d) from
        pow_two _, mul_div_assoc, mul_div_mul_left _ (hne0 d hd)]
    rw [Finset.sum_congr rfl hperd, ← Finset.mul_sum, ← mul_one_div,
      sum_Ico1 (fun d => 1 / (1 - ζ ^ d)),
      Finset.sum_congr rfl (fun m _ => by rw [Nat.add_comm 1 m]),
      sum_roots_of_unity h1 hprim]
  rw [corotLin, husk, hsum, hz2k, hOm]
  push_cast [Complex.ofReal_nat_cast]
  ring

