import Mathlib.Tactic
example (φ : ℝ) (hφ : φ ∈ Set.Ioo (-Real.pi) Real.pi) :
    Real.cos φ = (1 - Real.tan (φ / 2) ^ 2) / (1 + Real.tan (φ / 2) ^ 2) := by
  have hφlo : -(Real.pi / 2) < φ / 2 := by linarith [hφ.1]
  have hφhi : φ / 2 < Real.pi / 2 := by linarith [hφ.2]
  have hcos0 : Real.cos (φ / 2) ≠ 0 := (Real.cos_pos_of_mem_Ioo ⟨hφlo, hφhi⟩).ne'
  have hnum : (1 : ℝ) - Real.tan (φ / 2) ^ 2
      = (Real.cos (φ / 2) ^ 2 - Real.sin (φ / 2) ^ 2) / Real.cos (φ / 2) ^ 2 := by
    have ht2 : Real.tan (φ / 2) ^ 2 = Real.sin (φ / 2) ^ 2 / Real.cos (φ / 2) ^ 2 := by
      rw [Real.tan_eq_sin_div_cos, div_pow]
    rw [ht2]
    field_simp [hcos0]
  have hsq : (1 : ℝ) + Real.tan (φ / 2) ^ 2 = 1 / Real.cos (φ / 2) ^ 2 := by
    rw [Real.tan_eq_sin_div_cos, div_pow]
    field_simp [hcos0, Real.sin_sq_add_cos_sq (φ / 2)]
  have hφ2 : Real.cos φ = Real.cos (2 * (φ / 2)) := by
    rw [show ((2 : ℝ) * (φ / 2)) = φ from by ring]
  rw [hφ2, Real.cos_two_mul', hnum, hsq]
  field_simp [hcos0]
