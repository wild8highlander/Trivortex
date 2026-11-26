import Mathlib
#check @Complex.mul_conj
#check @Complex.ofReal_mul
#check @HasDerivAt.ofReal_comp
example : Mul ℝ ℂ := by infer_instance
example (a b : ℝ) : Complex.I * ((a * b : ℝ) : ℂ) = (a : ℂ) * Complex.I * (b : ℂ) := by
  rw [Complex.ofReal_mul]; ring
