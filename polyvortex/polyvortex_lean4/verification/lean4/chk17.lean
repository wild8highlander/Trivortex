import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.ArctanDeriv
example (φ : ℝ) (hcos0 : Real.cos (φ / 2) ≠ 0) : True := by
  have h1 : HasDerivAt (fun x : ℝ => Real.tan (x / 2))
      ((1 / Real.cos (φ / 2) ^ 2) * (1 / 2)) φ :=
    (Real.hasDerivAt_tan hcos0).comp (x := φ)
      (HasDerivAt.div_const (hasDerivAt_id φ) 2)
  trivial
