# MATHLIB v4.6.0 recipes — the tactic-level field guide for `Polyvortex.lean`

This document distills the working knowledge that produced the TW1.b proof-fix pass
(123 errors → 0 errors, 0 `sorry`, 2026-11-26). The recipes were validated against the
pinned environment (`leanprover/lean4:v4.6.0`, Mathlib tag `v4.6.0`) while fixing each
of the 125 enumerated proof defects — first in throwaway scratch files (the historical
`chk*.lean` series, retired in v1.0.2), then spliced into the artifact. They are kept
here because the next Lean/Mathlib bump (and TW3–TW5) will re-trigger every one of them.

Provenance: distilled from the session notes `STATE_2026-11-26*.md` (retired) and
`docs/VERIFICATION_v460.md`; each recipe below was executed in a compiling artifact.

SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0

---

## 0. Environment bootstrap (rebuildable in one script)

```bash
# elan + toolchain + Mathlib release cache (~4330 olean files)
curl https://elan.lean-lang.org/elan-init.sh -sSf | sh -s -- -y
export ELAN_HOME="$HOME/.elan" PATH="$ELAN_HOME/bin:$PATH"
cd polyvortex/polyvortex_lean4        # lean-toolchain pins v4.6.0 automatically
lake exe cache get                    # the cold Mathlib build takes hours — never do it
lake env lean Polyvortex.lean         # the ~3-minute per-iteration command
```

Iteration discipline that made TW1.b tractable: cut the section under repair into a
scratch file with the same 8 imports, iterate on the chunk (seconds, not minutes),
splice back, then run the full gate `bash tools/ci_gate.sh`. The chunk files are
session-scoped and are NOT committed — the seal and the gates certify the spliced file.

## 1. `star` vs `starRingEnd ℂ` — defeq, but `rw` sees only one form

In v4.6.0 `Complex.conj a` is locale notation for `(starRingEnd ℂ) a`; the bare
primitive is `star a`. The two are defeq (`rfl` accepts `star cE = (starRingEnd ℂ) cE`)
but **`rw` matches only the syntactic form**.

```lean
-- symptom: rw [Complex.mul_conj] does not fire on `star cE * star cE`
have : (starRingEnd ℂ) cE * (starRingEnd ℂ) cE = 1 := Complex.mul_conj _ cE
-- bridge: promote the goal with `show`, then rewrite
show ((starRingEnd ℂ) cE) * ((starRingEnd ℂ) cE) = 1
```

## 2. `HasDerivAt.comp` needs the explicit point in v4.6.0

```lean
-- WRONG: .comp hr — elaborates against the wrong implicit, "function expected"
-- RIGHT: the FIRST explicit argument of .comp is the point x
have htan : HasDerivAt (fun x => Real.tan (x / 2))
    ((1 / Real.cos (φ / 2) ^ 2) * (1 / 2)) φ :=
  (Real.hasDerivAt_tan _).comp (x := φ) (Real.hasDerivAt_div_const _ 2 _) _
```

Same for `HasDerivAt.ofReal_comp` chains in §3: keep `.comp (x := t)` everywhere.

## 3. `rw` does not fire under a λ-binder with unresolved metavariables

Higher-order unification refuses to instantiate `?F` under binders. Two escapes:

```lean
-- (a) simp only instead of rw (simp retries under binders)
simp only [div_eq_mul_inv]
-- (b) name the function explicitly at the lemma
rw [integral_comp_mul_left (f := fun x => ringOmega γ R N x) hω]
```

The explicit `(f := ...)` is mandatory for `integral_comp_mul_left`,
`integral_comp_sub_right`, and every `integral_*` transport lemma used in §4.

## 4. v4.6.0 has NO root aliases for order/interval names

| old (does not compile) | v4.6.0 spelling |
|---|---|
| `Ioo a b` | `Set.Ioo a b` |
| `uIcc a b` / `mem_uIcc` | `Set.uIcc` / `Set.mem_uIcc` |
| `EqOn f g s` | `Set.EqOn f g s` |
| `interval_congr` (root) | `integral_congr` via `open intervalIntegral` |

Note: `Set.mem_uIcc` in v4.6.0 yields the disjunction **without** `min`/`max` —
pattern-match with `rcases` (constructor + two branches), not with `min_le_iff`.

## 5. BigOperator binder syntax: `∑ x in s`, not `∑ x ∈ s`

The `∑ x ∈ s, f x` notation does not exist in v4.6.0. The binder is `in`, and the
notation lives in the `BigOperators` locale:

```lean
import Mathlib.Algebra.BigOperators.Basic
open scoped BigOperators
-- ∑ j in (Finset.range N).erase k, ...
```

All 34 call sites were converted in the API-fix pass (see `docs/VERIFICATION_v460.md`,
defect #1).

## 6. Conjugation is `star`, one import away

`Complex.conj` as a function is gone; use the `StarRing ℂ` primitive. The artifact
carries its own private wrappers (`conj_mul'`, `conj_sub'`, `conj_pow'`, `conj_conj'`,
`normSq_mul'`, `normSq_ofReal'`, `normSq_ne_zero'`) derived from
`Complex.normSq_eq_conj_mul_self` — so a future Mathlib refactor of `normSq` simp
lemmas cannot break the artifact.

## 7. Tangent/arctan toolkit that actually exists in v4.6.0

Confirmed compiling: `Real.hasDerivAt_tan`, `Real.tan_pi_div_two_sub`,
`Real.arctan_strictMono`, `Real.arctan_inv_of_pos`. NOT existing:
`arctan_add_arctan_inv` (replaced by `Real.arctan_inv_of_pos` + one `mul_one`),
`sq_eq_sq'`, `sq_eq_sq'.mp`, and a root-level `sq_neg` — the artifact proves its own
`sq_neg (a : ℝ) : (-a)^2 = a^2 := by ring` locally (§4, line ~1295).

## 8. `Real.sqrt` chains

```lean
have hksq : Real.sqrt ((1 - ε) / (1 + ε)) * (1 + ε) = Real.sqrt (1 - ε ^ 2) := by
  rw [Real.sqrt_div]           -- decompose, not field_simp
  rw [Real.sqrt_mul, Real.sqrt_mul_self]   -- then close
have hspos : 0 < Real.sqrt x := (Real.sqrt_pos).mpr hx   -- .mpr form, not sqrt_pos'
```

## 9. Cast chains when ℝ-arithmetic is elaborated inside ℂ

In §3 the pulsation positivity argument elaborates every ℝ atom as a cast
(`↑Real.pi`, `↑↑0`). The working cascade:

```lean
simp [Nat.cast_zero, Complex.ofReal_zero, mul_zero, zero_div, add_zero]
```

and instead of `congrArg` β-redexes, use a **typed** `have`:

```lean
have hstep : ((r t : ℝ) : ℂ) * ((1 + ε * Real.cos (ω * t) : ℝ) : ℂ)
    = (↑(r t) * ↑(1 + ε * Real.cos (ω * t)) : ℂ) := ring_nf rfl
```

## 10. Integrals: assemble, don't improvise

- Split halves with `intervalIntegral.integral_add_adjacent_intervals`; the measure
  is not inferred — pass `(μ := volume)` when `Continuous.intervalIntegrable` stalls.
- Kill β-redexes inside `integral_congr` branches first: `intro x _; simp only []`.
- The §4 half-and-half trick: show the second summand as `1/(1 + (-ε)·cos)` and give
  the antiderivative an ascription `poisson_cont (by rwa [sq_neg] : (-ε)^2 < 1)`.

## 11. `#print axioms` gates — keep the footprint classical

After every fix, the 26 footprints must stay inside
`{propext, Classical.choice, Quot.sound}`. Gate: `python3 tools/axioms_gate.py`.
A `sorryAx` in any footprint means an unfinished proof upstream in the dependency
chain — fix the named upstream theorem, not the gate.

## 12. When `omega` refuses modular reasoning about variable N

The modular bookkeeping of §1 (`mod_add_zero_eq`, `mod_add_eq_self`, `mul_pred_mod`)
is proven with `Nat.ModEq` cancellations only — `omega` does not solve
variable-modulus goals. `Nat.mod_add_mod`, `Nat.add_mul_mod_self_left`,
`Nat.mul_mod_right`, `Nat.le_mul_of_pos_right`, `Nat.pos_of_ne_zero` are all present
in v4.6.0 and sufficient.

---

*Keeping this file current is part of the TW2+ contract: any new tactic recipe
validated inside the artifact belongs here on the same commit.*
