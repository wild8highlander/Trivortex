# POLYVORTEX Lean 4 — the statement layer, declaration by declaration

Generated from `Polyvortex.lean` v1.0; the sha256 seals of every
theorem statement live in `seal/manifest.json` and are enforced by
`tools/seal_check.py --check`.

SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0

## Census

| section | content | declarations |
|---|---|---|
| §0 | Private helpers | 12 |
| §1 | Theorem A: the regular `N`-gon ring is an exact solution | 28 |
| §2 | Theorem B: the admissibility threshold of the pulsating ansatz | 9 |
| §3 | Lemma C: no pulsating ring can ride the Kirchhoff field | 6 |
| §4 | Lemma D: the cycle-averaged Kirchhoff rate of the pulsation | 17 |
| §5 | Theorem E (statement layer): the co-rotating linearization | 6 |
| H | header & module docstring | 0 |

**Total:** 78 declarations — 61 theorems/lemmas, 17 definitions.

## § 0. Private helpers

- `theorem sum_range_shift_one`
- `theorem sum_rot_shift`
- `theorem sum_rot`
- `theorem sum_range_reflect_aux`
- `theorem sum_erase_zero`
- `theorem conj_mul'`
- `theorem conj_sub'`
- `theorem conj_pow'`
- `theorem conj_conj'`
- `theorem normSq_mul'`
- `theorem normSq_ofReal'`
- `theorem normSq_ne_zero'`

## § 1. Theorem A: the regular `N`-gon ring is an exact solution

- `def rootExp`
- `def ringPos`
- `def ringOmega`
- `def kirchhoff`
- `theorem mod_add_zero_eq`
- `theorem mod_self'`
- `theorem mod_add_eq_self`
- `theorem mul_pred_mod`
- `theorem root_ne_zero`
- `theorem normSq_pow'`
- `theorem real_pow_eq_one_of_nonneg`
- `theorem conj_root_unity`
- `theorem pow_mod_eq`
- `theorem ringPos_sub_ringPos`
- `theorem ring_term`
- `theorem roots_pair_core`
- `theorem sum_roots_of_unity`
- `theorem ring_velocity`
- `theorem kirchhoff_smul`
- `theorem normSq_exp_I_mul`
- `def ringOrbit`
- `theorem ringOrbit_deriv`
- `theorem kirchhoff_ringOrbit`
- `theorem ringOrbit_sol`
- `theorem rootExp_pow`
- `theorem rootExp_prim`
- `theorem ringOmega_three_eq_lagrange`
- `theorem ring_rotation_rate_pos`

## § 2. Theorem B: the admissibility threshold of the pulsating ansatz

- `def eps`
- `def rClosed`
- `def thetaClosed`
- `theorem eps_pos`
- `theorem eps_lt_one_iff`
- `theorem eps_at_threshold`
- `theorem rClosed_min`
- `theorem rClosed_pos_iff`
- `theorem rClosed_touches_zero_at_threshold`

## § 3. Lemma C: no pulsating ring can ride the Kirchhoff field

- `def radialForm`
- `def pulsPos`
- `theorem ring_radial_zero`
- `theorem lemmaC_pulsation`
- `theorem lemmaC_radius_constant`
- `theorem lemmaC_H1_reduction`

## § 4. Lemma D: the cycle-averaged Kirchhoff rate of the pulsation

- `def pulsRadius`
- `def avgKinFreq`
- `theorem ringOmega_smul_radius`
- `theorem lemmaD_omega_independent`
- `theorem abs_lt_one_of_sq_lt_one`
- `theorem sqrt_pos'`
- `def poissonG`
- `theorem cos_half_tan`
- `theorem one_add_eps_cos_ne_zero`
- `theorem poisson_cont`
- `theorem arctan_add_arctan_inv`
- `theorem hasDerivAt_poissonG`
- `theorem poisson_ftc`
- `theorem poisson_half`
- `theorem poisson_integral`
- `theorem poisson_sq`
- `theorem lemmaD_bridge`

## § 5. Theorem E (statement layer): the co-rotating linearization

- `def corotatingField`
- `theorem ring_fixed_point`
- `theorem ring_corotating_constant`
- `def eigenvalueOf`
- `def spectrallyStable`
- `def havelockClassification`

