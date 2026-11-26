import Mathlib.Tactic
#check @Real.sqrt_pos
example (φ x : ℝ) (h : Real.cos x ≠ 0) :
    (1 : ℝ) - Real.tan x ^ 2 = (Real.cos x ^ 2 - Real.sin x ^ 2) / Real.cos x ^ 2 := by
  have ht2 : Real.tan x ^ 2 = Real.sin x ^ 2 / Real.cos x ^ 2 := by
    rw [Real.tan_eq_sin_div_cos, div_pow]
  rw [ht2]
  field_simp [h]
  ring
