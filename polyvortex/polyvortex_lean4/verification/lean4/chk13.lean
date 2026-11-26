import Mathlib.Tactic
example (z : ℂ) : z * star z = z * (starRingEnd ℂ) z := by rfl
example (z : ℂ) : z * star z = ↑(Complex.normSq z) := by
  show z * (starRingEnd ℂ) z = _
  rw [Complex.mul_conj]
example (z : ℂ) : z * star z = ↑(Complex.normSq z) := by
  rw [Complex.mul_conj]
