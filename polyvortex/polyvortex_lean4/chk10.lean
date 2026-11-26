import Mathlib.Tactic
import Mathlib.MeasureTheory.Integral.IntervalIntegral
#check @intervalIntegral.integral_comp_mul_left
example (ω : ℝ) (hω : ω ≠ 0) (F : ℝ → ℝ) :
    ∫ t in (0:ℝ)..(2*Real.pi/ω), (fun φ => F φ) (ω * t)
      = (1/ω) * ∫ x in (ω*0)..(ω*(2*Real.pi/ω)), F x := by
  rw [integral_comp_mul_left hω]
