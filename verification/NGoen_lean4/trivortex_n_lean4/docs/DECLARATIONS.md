# Declaration reference — every declaration of `NGon.lean`
33 declarations: **6 definitions** and **27 theorems**, 100% docstring coverage (ratchet: `seal/docstring_baseline.json`), 27 `#print axioms` directives.

| # | line | kind | name | section | doc | seal |
|---:|---:|---|---|---|:-:|:-:|
| 1 | 47 | `def` | [`nGonAngle`](../NGon.lean#L47) | §1 | ✓ | — |
| 2 | 51 | `def` | [`nGon`](../NGon.lean#L51) | §1 | ✓ | — |
| 3 | 56 | `def` | [`unity`](../NGon.lean#L56) | §1 | ✓ | — |
| 4 | 60 | `def` | [`ker`](../NGon.lean#L60) | §1 | ✓ | — |
| 5 | 65 | `def` | [`field`](../NGon.lean#L65) | §1 | ✓ | — |
| 6 | 70 | `def` | [`nGonOmega`](../NGon.lean#L70) | §1 | ✓ | — |
| 7 | 75 | `theorem` | [`ker_mul`](../NGon.lean#L75) | §1 | ✓ | [`53245516…`](../seal/manifest.json) |
| 8 | 83 | `theorem` | [`ker_re_I`](../NGon.lean#L83) | §1 | ✓ | [`35af54ce…`](../seal/manifest.json) |
| 9 | 96 | `theorem` | [`ker_im_I`](../NGon.lean#L96) | §1 | ✓ | [`aeec9866…`](../seal/manifest.json) |
| 10 | 111 | `theorem` | [`exp_two_pi_I`](../NGon.lean#L111) | §2 | ✓ | [`980f656a…`](../seal/manifest.json) |
| 11 | 118 | `theorem` | [`normSq_unity`](../NGon.lean#L118) | §2 | ✓ | [`e5a951d7…`](../seal/manifest.json) |
| 12 | 124 | `theorem` | [`unity_mod`](../NGon.lean#L124) | §2 | ✓ | [`5d7f1d5f…`](../seal/manifest.json) |
| 13 | 141 | `theorem` | [`unity_congr`](../NGon.lean#L141) | §2 | ✓ | [`2160b2e0…`](../seal/manifest.json) |
| 14 | 147 | `theorem` | [`unity_inv`](../NGon.lean#L147) | §2 | ✓ | [`a2edbce5…`](../seal/manifest.json) |
| 15 | 161 | `theorem` | [`unity_ne_one`](../NGon.lean#L161) | §2 | ✓ | [`4801000d…`](../seal/manifest.json) |
| 16 | 199 | `theorem` | [`field_re`](../NGon.lean#L199) | §2 | ✓ | [`f0c0044b…`](../seal/manifest.json) |
| 17 | 210 | `theorem` | [`field_im`](../NGon.lean#L210) | §2 | ✓ | [`ca174698…`](../seal/manifest.json) |
| 18 | 222 | `theorem` | [`ker_pair`](../NGon.lean#L222) | §2 | ✓ | [`52223430…`](../seal/manifest.json) |
| 19 | 264 | `theorem` | [`sum_ker_unity`](../NGon.lean#L264) | §2 | ✓ | [`68ea8667…`](../seal/manifest.json) |
| 20 | 338 | `theorem` | [`nGonAngle_add`](../NGon.lean#L338) | §3 | ✓ | [`46f309b9…`](../seal/manifest.json) |
| 21 | 351 | `theorem` | [`unity_shift`](../NGon.lean#L351) | §3 | ✓ | [`dfacd5a7…`](../seal/manifest.json) |
| 22 | 362 | `theorem` | [`mod_shift_left`](../NGon.lean#L362) | §3 | ✓ | [`f5fd1303…`](../seal/manifest.json) |
| 23 | 370 | `theorem` | [`mod_shift_right`](../NGon.lean#L370) | §3 | ✓ | [`2a3dd603…`](../seal/manifest.json) |
| 24 | 386 | `theorem` | [`mod_shift_ne_zero`](../NGon.lean#L386) | §3 | ✓ | [`e99178fd…`](../seal/manifest.json) |
| 25 | 398 | `theorem` | [`normSq_nGon`](../NGon.lean#L398) | §3 | ✓ | [`afa1cbb0…`](../seal/manifest.json) |
| 26 | 404 | `theorem` | [`nGon_ne_zero`](../NGon.lean#L404) | §3 | ✓ | [`8e2fc25b…`](../seal/manifest.json) |
| 27 | 412 | `theorem` | [`ker_nGon_sum`](../NGon.lean#L412) | §3 | ✓ | [`ea0b4cd8…`](../seal/manifest.json) |
| 28 | 487 | `theorem` | [`nGon_field_eq`](../NGon.lean#L487) | §3 | ✓ | [`126dfc90…`](../seal/manifest.json) |
| 29 | 501 | `theorem` | [`nGon_omega_forced`](../NGon.lean#L501) | §3 | ✓ | [`6b1ff862…`](../seal/manifest.json) |
| 30 | 512 | `theorem` | [`nGon_omega_ne_zero`](../NGon.lean#L512) | §3 | ✓ | [`b1ac8de3…`](../seal/manifest.json) |
| 31 | 532 | `theorem` | [`nGon_omega_pos_iff`](../NGon.lean#L532) | §3 | ✓ | [`fc57d3e0…`](../seal/manifest.json) |
| 32 | 559 | `theorem` | [`nGon_side3_sq`](../NGon.lean#L559) | §3 | ✓ | [`434490ac…`](../seal/manifest.json) |
| 33 | 609 | `theorem` | [`nGon_omega_three`](../NGon.lean#L609) | §3 | ✓ | [`3d4a9ac3…`](../seal/manifest.json) |

## The six definitions (the object layer)
| name | type | meaning |
|---|---|---|
| [`nGonAngle`](../NGon.lean#L47) | `ℝ` | `θ_k = 2πk/N` — the angular position of vertex `k` |
| [`nGon`](../NGon.lean#L51) | `ℂ` | `z_k = R·exp(i·θ_k)` — vertex `k` of the regular `N`-gon of circumradius `R` |
| [`unity`](../NGon.lean#L56) | `ℂ` | `u_m = exp(2πi·m/N)` — the `m`-th root of unity (shape factor) |
| [`ker`](../NGon.lean#L60) | `ℂ` | `ker w = w/|w|²` — the point-vortex velocity kernel |
| [`field`](../NGon.lean#L65) | `ℂ` | the Kirchhoff velocity of equal vortices `g` at vertex `k` of a configuration `w` |
| [`nGonOmega`](../NGon.lean#L70) | `ℝ` | `ω = Γ(N−1)/(4πR²)` — the forced rotation rate of the polygon |

## Section narrative
* **§1 (9 declarations, lines 44–107).** The object layer: vertices, the kernel, the field, the forced rate. The kernel algebra (`ker_mul`) and the two `(x, y)`-bridges (`ker_re_I`, `ker_im_I`) tie the complex kernel to the planar Kirchhoff convention of the root module.
* **§2 (10 theorems, lines 108–322).** The root-of-unity calculus: `unity_mod/inv/ne_one`, the `(x, y)` bridges for the field, the **pairing identity** `ker_pair` and the **core finite sum** `sum_ker_unity = (N−1)/2` — the single identity that forces the rotation rate.
* **§3 (14 theorems, lines 323–615).** Angle bookkeeping and modular re-indexing (`nGonAngle_add`, `unity_shift`, `mod_shift_*`), the geometry lemmas (`normSq_nGon`, `nGon_ne_zero`), the **core reduction** `ker_nGon_sum`, the **MAIN THEOREM** `nGon_field_eq`, the **uniqueness** `nGon_omega_forced`, the corollaries (`nGon_omega_ne_zero`, `nGon_omega_pos_iff`) and the **N = 3 bridge** (`nGon_side3_sq`, `nGon_omega_three`).

*Generated from the source; do not edit by hand.*
