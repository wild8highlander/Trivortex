import Mathlib.Tactic
example (ε : ℝ) (hpe : 0 < 1 + ε) (hme : 0 < 1 - ε) (hc : 0 < 1 - ε ^ 2) :
    Real.sqrt ((1 - ε) / (1 + ε)) * (1 + ε) = Real.sqrt (1 - ε ^ 2) := by
  have h1 : Real.sqrt ((1 - ε) / (1 + ε)) * Real.sqrt ((1 + ε) * (1 + ε))
      = Real.sqrt (1 - ε ^ 2) := by
    rw [← Real.sqrt_mul (div_nonneg hme.le hpe.le)]
    congr 1
    field_simp [hpe.ne']
    ring
  rw [← h1, Real.sqrt_mul_self (by positivity)]
