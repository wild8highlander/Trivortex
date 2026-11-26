import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.ArctanDeriv
example (φ ε : ℝ) (hcos0 : Real.cos (φ / 2) ≠ 0)
    (hsq : (1 : ℝ) + Real.tan (φ / 2) ^ 2 = 1 / Real.cos (φ / 2) ^ 2) :
    HasDerivAt (fun x => Real.arctan (Real.sqrt ((1 - ε) / (1 + ε)) * Real.tan (x / 2)))
      (1 / (1 + Real.sqrt ((1 - ε) / (1 + ε)) ^ 2 * Real.tan (φ / 2) ^ 2)
        * (Real.sqrt ((1 - ε) / (1 + ε)) * ((1 + Real.tan (φ / 2) ^ 2) / 2))) φ := by
  have hhalf : HasDerivAt (fun x : ℝ => Real.tan (x / 2))
      ((1 / Real.cos (φ / 2) ^ 2) * (1 / 2)) φ :=
    (Real.hasDerivAt_tan hcos0).comp (x := φ)
      (HasDerivAt.div_const (hasDerivAt_id φ) 2)
  have hsq' : (Real.cos (φ / 2) ^ 2)⁻¹ = 1 + Real.tan (φ / 2) ^ 2 := by
    rw [inv_eq_one_div]; exact hsq.symm
  simpa [mul_comm, mul_left_comm, mul_assoc, mul_pow, hsq', Function.comp_def, div_eq_mul_inv] using
    (Real.hasDerivAt_arctan
      (Real.sqrt ((1 - ε) / (1 + ε)) * Real.tan (φ / 2))).comp (x := φ)
      (HasDerivAt.const_mul (Real.sqrt ((1 - ε) / (1 + ε))) hhalf)
