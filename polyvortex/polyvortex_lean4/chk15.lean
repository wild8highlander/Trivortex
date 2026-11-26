import Mathlib.Tactic
example (φ : ℝ) (hcos0 : Real.cos (φ / 2) ≠ 0)
    (hsq : (1 : ℝ) + Real.tan (φ / 2) ^ 2 = 1 / Real.cos (φ / 2) ^ 2) :
    HasDerivAt (fun x : ℝ => Real.tan (x / 2)) ((1 + Real.tan (φ / 2) ^ 2) / 2) φ := by
  simpa [← hsq, mul_comm, mul_left_comm, mul_assoc] using
    (Real.hasDerivAt_tan hcos0).comp (x := φ)
      (HasDerivAt.div_const (hasDerivAt_id φ) 2)
