import Mathlib.Tactic
import Mathlib.MeasureTheory.Integral.IntervalIntegral
#check @div_eq_mul_inv
example (K f : ℝ → ℝ) :
    ∫ φ in (0:ℝ)..(2*Real.pi), K φ / (1 + φ) ^ 2
      = K φ * ∫ φ' in (0:ℝ)..(2*Real.pi), ((1 + φ') ^ 2)⁻¹ := by
  rw [div_eq_mul_inv, integral_const_mul]
