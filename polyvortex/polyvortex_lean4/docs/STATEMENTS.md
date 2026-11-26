# POLYVORTEX Lean 4 — the statement layer, declaration by declaration

Generated from `Polyvortex.lean` (TW1.b artifact, 1,609 lines) by `tools/lint_conventions.py`-compatible parsing; the sha256 seals of every theorem statement live in `seal/manifest.json` and are enforced by `tools/seal_check.py --check`. Regenerate after any release with the companion script (counts must equal the lint gate: 79 declarations).

SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0

## Census

| section | content | declarations |
|---|---|---|
| §0 | Private helpers: cyclic sums and ℂ conjugate/normSq toolkit | 12 |
| §1 | Theorem A: the regular `N`-gon ring is an exact Kirchhoff solution (forced) | 28 |
| §2 | Theorem B: the admissibility threshold of the pulsating ansatz | 9 |
| §3 | Lemma C: no pulsating ring can ride the Kirchhoff field | 6 |
| §4 | Lemma D: the cycle-averaged Kirchhoff rate and the Poisson integral | 18 |
| §5 | Theorem E (statement layer): the co-rotating linearization and W4 | 6 |

**Total:** 79 declarations — 62 theorems/lemmas, 17 definitions.


## § 0. Private helpers: cyclic sums and ℂ conjugate/normSq toolkit

- `private theorem sum_range_shift_one`
- `private theorem sum_rot_shift`
- `private theorem sum_rot`
- `private theorem sum_range_reflect_aux`
- `private theorem sum_erase_zero`
- `private theorem conj_mul'`
- `private theorem conj_sub'`
- `private theorem conj_pow'`
- `private theorem conj_conj'`
- `private theorem normSq_mul'`
- `private theorem normSq_ofReal'`
- `private theorem normSq_ne_zero'`

## § 1. Theorem A: the regular `N`-gon ring is an exact Kirchhoff solution (forced)

- `noncomputable def rootExp`
- `noncomputable def ringPos`
- `noncomputable def ringOmega`
- `noncomputable def kirchhoff`
- `private theorem mod_add_zero_eq`
- `private theorem mod_self'`
- `private theorem mod_add_eq_self`
- `private theorem mul_pred_mod`
- `theorem root_ne_zero`
- `private theorem normSq_pow'`
- `private theorem real_pow_eq_one_of_nonneg`
- `theorem conj_root_unity`
- `theorem pow_mod_eq`
- `theorem ringPos_sub_ringPos`
- `private theorem ring_term`
- `private theorem roots_pair_core`
- `theorem sum_roots_of_unity`
- `theorem ring_velocity`
- `theorem kirchhoff_smul`
- `theorem normSq_exp_I_mul`
- `noncomputable def ringOrbit`
- `theorem ringOrbit_deriv`
- `theorem kirchhoff_ringOrbit`
- `theorem ringOrbit_sol`
- `theorem rootExp_pow`
- `theorem rootExp_prim`
- `theorem ringOmega_three_eq_lagrange`
- `theorem ring_rotation_rate_pos`

## § 2. Theorem B: the admissibility threshold of the pulsating ansatz

- `noncomputable def eps`
- `noncomputable def rClosed`
- `noncomputable def thetaClosed`
- `theorem eps_pos`
- `theorem eps_lt_one_iff`
- `theorem eps_at_threshold`
- `theorem rClosed_min`
- `theorem rClosed_pos_iff`
- `theorem rClosed_touches_zero_at_threshold`

## § 3. Lemma C: no pulsating ring can ride the Kirchhoff field

- `noncomputable def radialForm`
- `noncomputable def pulsPos`
- `theorem ring_radial_zero`
- `theorem lemmaC_pulsation`
- `theorem lemmaC_radius_constant`
- `theorem lemmaC_H1_reduction`

## § 4. Lemma D: the cycle-averaged Kirchhoff rate and the Poisson integral

- `noncomputable def pulsRadius`
- `noncomputable def avgKinFreq`
- `theorem ringOmega_smul_radius`
- `theorem lemmaD_omega_independent`
- `private theorem abs_lt_one_of_sq_lt_one`
- `private theorem sqrt_pos'`
- `noncomputable def poissonG`
- `private theorem cos_half_tan`
- `private theorem one_add_eps_cos_ne_zero`
- `private theorem poisson_cont`
- `private theorem arctan_add_arctan_inv`
- `private theorem hasDerivAt_poissonG`
- `private theorem poisson_ftc`
- `private theorem sq_neg`
- `private theorem poisson_half`
- `theorem poisson_integral`
- `theorem poisson_sq`
- `theorem lemmaD_bridge`

## § 5. Theorem E (statement layer): the co-rotating linearization and W4

- `noncomputable def corotatingField`
- `theorem ring_fixed_point`
- `theorem ring_corotating_constant`
- `def eigenvalueOf`
- `def spectrallyStable`
- `def havelockClassification`

