# POLYVORTEX Lean 4 — the statement layer, declaration by declaration

Generated from `Polyvortex.lean` (the TW1–TW5 artifact — the full program: Theorems A–E, Lemmas C/D and the spectral machinery of §4′) by the docs generator; the sha256 seals of every theorem statement live in `seal/manifest.json` and are enforced by `tools/seal_check.py --check`. Counts must equal the lint gate: 138 declarations.

SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0

## Census

| section | content | theorems | definitions | total |
|---|---|---|---|---|
| §0 | Private helpers | 12 | 0 | **12** |
| §1 | Theorem A: the regular `N`-gon ring is an exact solution | 23 | 5 | **28** |
| §2 | Theorem B: the admissibility threshold of the pulsating ansatz | 6 | 3 | **9** |
| §3 | Lemma C: no pulsating ring can ride the Kirchhoff field | 4 | 2 | **6** |
| §4 | Lemma D: the cycle-averaged Kirchhoff rate of the pulsation | 15 | 3 | **18** |
| §4′ | The spectral machinery of Theorem E (milestones TW2–TW5) | 52 | 8 | **60** |
| §5 | Theorem E: the co-rotating linearization and the Havelock classification | 3 | 2 | **5** |
| | **total** | **115** | **23** | **138** |

## § 0. Private helpers

- `private` `sum_range_shift_one`
- `private` `sum_rot_shift`
- `private` `sum_rot`
- `private` `sum_range_reflect_aux`
- `private` `sum_erase_zero`
- `private` `conj_mul'`
- `private` `conj_sub'`
- `private` `conj_pow'`
- `private` `conj_conj'`
- `private` `normSq_mul'`
- `private` `normSq_ofReal'`
- `private` `normSq_ne_zero'`

## § 1. Theorem A: the regular `N`-gon ring is an exact solution

- `noncomputable` `rootExp`
- `noncomputable` `ringPos`
- `noncomputable` `ringOmega`
- `noncomputable` `kirchhoff`
- `private` `mod_add_zero_eq`
- `private` `mod_self'`
- `private` `mod_add_eq_self`
- `private` `mul_pred_mod`
- `root_ne_zero`
- `private` `normSq_pow'`
- `private` `real_pow_eq_one_of_nonneg`
- `conj_root_unity`
- `pow_mod_eq`
- `ringPos_sub_ringPos`
- `private` `ring_term`
- `private` `roots_pair_core`
- `sum_roots_of_unity`
- `ring_velocity`
- `kirchhoff_smul`
- `normSq_exp_I_mul`
- `noncomputable` `ringOrbit`
- `ringOrbit_deriv`
- `kirchhoff_ringOrbit`
- `ringOrbit_sol`
- `rootExp_pow`
- `rootExp_prim`
- `ringOmega_three_eq_lagrange`
- `ring_rotation_rate_pos`

## § 2. Theorem B: the admissibility threshold of the pulsating ansatz

- `noncomputable` `eps`
- `noncomputable` `rClosed`
- `noncomputable` `thetaClosed`
- `eps_pos`
- `eps_lt_one_iff`
- `eps_at_threshold`
- `rClosed_min`
- `rClosed_pos_iff`
- `rClosed_touches_zero_at_threshold`

## § 3. Lemma C: no pulsating ring can ride the Kirchhoff field

- `noncomputable` `radialForm`
- `noncomputable` `pulsPos`
- `ring_radial_zero`
- `lemmaC_pulsation`
- `lemmaC_radius_constant`
- `lemmaC_H1_reduction`

## § 4. Lemma D: the cycle-averaged Kirchhoff rate of the pulsation

- `noncomputable` `pulsRadius`
- `noncomputable` `avgKinFreq`
- `ringOmega_smul_radius`
- `lemmaD_omega_independent`
- `private` `abs_lt_one_of_sq_lt_one`
- `private` `sqrt_pos'`
- `noncomputable` `poissonG`
- `private` `cos_half_tan`
- `private` `one_add_eps_cos_ne_zero`
- `private` `poisson_cont`
- `private` `arctan_add_arctan_inv`
- `private` `hasDerivAt_poissonG`
- `private` `poisson_ftc`
- `private` `sq_neg`
- `private` `poisson_half`
- `poisson_integral`
- `poisson_sq`
- `lemmaD_bridge`

## § 4′. The spectral machinery of Theorem E (milestones TW2–TW5)

- `zinv`
- `pow_congr_mod`
- `zinv_mul`
- `private` `normSq_pow_eq`
- `star_zeta_pow`
- `mul_one_sub_sum_range`
- `private` `key_mod_eq`
- `zinv_mul_zeta_pow`
- `sum_zeta_range`
- `fourier_orth`
- `noncomputable` `fmode`
- `fmode_inversion`
- `havSig`
- `private` `two_add_mod`
- `private` `one_add_mod`
- `havSig_inv`
- `noncomputable` `havS`
- `noncomputable` `havC`
- `private` `sum_Ico1`
- `private` `castReal_sub`
- `havC_zero`
- `havC_one`
- `private` `sum_range_zero_Ico`
- `havC_step`
- `havC_chain`
- `havS_zero`
- `havS_step`
- `havS_closed`
- `havS_sym`
- `private` `int_prod_bound`
- `havS_real_sq`
- `noncomputable` `corotLin`
- `private` `ringPos_eq`
- `private` `starI'`
- `private` `starR'`
- `private` `star_CR`
- `corotLin_periodic`
- `corotLin_add`
- `private` `hnegI`
- `private` `imul_neg_I`
- `corotLin_orbit_kernel`
- `private` `mod_shift_add`
- `private` `mod_shift_sub`
- `private` `sum_range_shift`
- `zeta_havSig_apply`
- `star_fmode`
- `corotLin_proj`
- `fmode_add`
- `fmode_linearity`
- `corotLin_pair_system`
- `corotLin_dispersion`
- `corotLin_stable7`
- `eigenvalueOf'`
- `havelockStable`
- `private` `corotLin_zero`
- `havelockStable_small`
- `private` `zeta_zinv_pow`
- `private` `zinv_shift`
- `havelock_witness`
- `rootExp_unit`

## § 5. Theorem E: the co-rotating linearization and the Havelock classification

- `noncomputable` `corotatingField`
- `ring_fixed_point`
- `ring_corotating_constant`
- `eigenvalueOf`
- `havelockClassification`

