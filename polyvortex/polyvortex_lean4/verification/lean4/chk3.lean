import Mathlib.Tactic
example (ε : ℝ) (hpe : 0 < 1 + ε) (hc : 0 < 1 - ε ^ 2) :
    Real.sqrt ((1 - ε) / (1 + ε)) * (1 + ε) = Real.sqrt (1 - ε ^ 2) := by
  have hp : (0 : ℝ) < (1 + ε) ^ 2 := by positivity
  rw [← Real.mul_self_sqrt hp.le, ← Real.sqrt_mul (Real.sqrt_nonneg _),
    ← Real.sqrt_mul (Real.sqrt_nonneg _)]
  congr 1
  field_simp [hpe.ne']
  ring
