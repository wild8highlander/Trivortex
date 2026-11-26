import Mathlib.Tactic
#check @intervalIntegral.integral_congr_ae
#check @intervalIntegral.integral_congr
example {f g : ℝ → ℝ} {a b : ℝ} (h : Set.EqOn f g (Set.uIcc a b)) :
    ∫ x in a..b, f x = ∫ x in a..b, g x := by
  exact? says skip
