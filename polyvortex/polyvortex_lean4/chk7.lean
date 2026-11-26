import Mathlib.Tactic
open Real
example {f g : ℝ → ℝ} {a b : ℝ} (h : ∀ x, f x = g x) :
    ∫ x in a..b, f x = ∫ x in a..b, g x := by
  exact? says skip
