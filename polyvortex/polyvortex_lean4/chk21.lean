import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.ArctanDeriv
example (φ ε : ℝ) (hpe : 0 < 1 + ε) (hme : 0 < 1 - ε) (hksq : Real.sqrt ((1 - ε) / (1 + ε)) * (1 + ε)
    = Real.sqrt (1 - ε ^ 2)) (hct : Real.cos φ = (1 - Real.tan (φ / 2) ^ 2)
    / (1 + Real.tan (φ / 2) ^ 2)) :
    (2 / Real.sqrt (1 - ε ^ 2)) * (2⁻¹ * (Real.sqrt ((1 - ε) / (1 + ε))
          * ((1 + Real.tan (φ / 2) ^ 2)
            * (1 + Real.sqrt ((1 - ε) / (1 + ε)) ^ 2 * Real.tan (φ / 2) ^ 2)⁻¹)))
      = 1 / (1 + ε * Real.cos φ) := by
  have hX : (0:ℝ) < 1 + Real.tan (φ / 2) ^ 2 := by positivity
  have hD : (0:ℝ) < 1 + Real.tan (φ / 2) ^ 2 + ε * (1 - Real.tan (φ / 2) ^ 2) :=
    by nlinarith [hpe, hme, mul_nonneg hme.le (sq_nonneg (Real.tan (φ / 2)))]
  field_simp [hksq, hct, hpe.ne', hme.ne', hX.ne', hD.ne']
  field_simp [hX.ne', hD.ne']
  ring
