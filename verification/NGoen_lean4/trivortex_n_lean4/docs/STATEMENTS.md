# The statement layer — all 27 sealed theorems of `NGon.lean`

> Machine-checkable source of truth: [`seal/manifest.json`](../seal/manifest.json) (sha256 of every normalized statement). This page is *generated* from the source — nothing here is hand-written prose about the statements.
>
> The five statements that carry the mathematical payload are marked ★.


## Section 1

Section 1 — definitions and the velocity kernel (3 theorems).


### `ker_mul`

Multiplicativity of the kernel: `ker` of a product factors through the normalized first factor.
```lean
theorem ker_mul {a b : ℂ} (ha : (Complex.normSq a : ℂ) ≠ 0) (hb : (Complex.normSq b : ℂ) ≠ 0) : ker (a * b) = (a / (Complex.normSq a : ℂ)) * ker b
```
sealed at sha256 `53245516324ce196…` · [source, line 75](../NGon.lean#L75)

### `ker_re_I`

Real part of `I*ker z`: the `(x, y)`-bridge for the transverse component.
```lean
theorem ker_re_I (z : ℂ) : (Complex.I * ker z).re = -z.im / Complex.normSq z
```
sealed at sha256 `35af54cee2ae1257…` · [source, line 83](../NGon.lean#L83)

### `ker_im_I`

Imaginary part of `I*ker z`: the `(x, y)`-bridge for the radial component.
```lean
theorem ker_im_I (z : ℂ) : (Complex.I * ker z).im = z.re / Complex.normSq z
```
sealed at sha256 `aeec98667957a34e…` · [source, line 96](../NGon.lean#L96)

## Section 2

Section 2 — roots of unity and the core finite sum (10 theorems).


### `exp_two_pi_I`

The fundamental identity `exp(2*pi*I) = 1`.
```lean
theorem exp_two_pi_I : Complex.exp (Complex.ofReal' (2 * Real.pi) * Complex.I) = 1
```
sealed at sha256 `980f656a6982f452…` · [source, line 111](../NGon.lean#L111)

### `normSq_unity`

Every root of unity lies on the unit circle: `|unity N m| = 1`.
```lean
theorem normSq_unity (N m : ℕ) : Complex.normSq (unity N m) = 1
```
sealed at sha256 `e5a951d77912b86e…` · [source, line 118](../NGon.lean#L118)

### `unity_mod`

The root of unity only depends on the residue class: `unity N (a % N) = unity N a`.
```lean
theorem unity_mod {N : ℕ} (hN : 0 < N) (a : ℕ) : unity N (a % N) = unity N a
```
sealed at sha256 `5d7f1d5fcc718b21…` · [source, line 124](../NGon.lean#L124)

### `unity_congr`

Equal residues give equal roots of unity.
```lean
theorem unity_congr {N : ℕ} (hN : 0 < N) {a b : ℕ} (h : a % N = b % N) : unity N a = unity N b
```
sealed at sha256 `2160b2e030685cf8…` · [source, line 141](../NGon.lean#L141)

### `unity_inv`

The index-`N-m` root is the inverse of the index-`m` root: `unity N (N-m) = (unity N m)^(-1)` for `0 < m < N`.
```lean
theorem unity_inv {N : ℕ} (hN : 0 < N) {m : ℕ} (h2 : m < N) : unity N (N - m) = (unity N m)⁻¹
```
sealed at sha256 `a2edbce586b47cae…` · [source, line 147](../NGon.lean#L147)

### `unity_ne_one`

Nontriviality: for `1 <= m < N` the root `unity N m` is not `1`.
```lean
theorem unity_ne_one {N : ℕ} (hN : 0 < N) {m : ℕ} (h1 : 1 ≤ m) (h2 : m < N) : unity N m ≠ 1
```
sealed at sha256 `4801000d8acf57c8…` · [source, line 161](../NGon.lean#L161)

### `field_re`

Bridge to the `(x, y)`-convention of the root module, real part: the transverse component of the Kirchhoff velocity at vertex `k` is `-g/(2pi)` times the sum of `(y_k - y_j)/|w_k - w_j|^2` — exactly the `I*(w_k - w_j)/|w_k - w_j|^2` kernel of the planar Kirchhoff equations.
```lean
theorem field_re (g : ℝ) (N : ℕ) (w : Fin N → ℂ) (k : Fin N) : (field g N w k).re = -(g / (2 * Real.pi)) * ∑ j in Finset.univ.erase k, ((w k).im - (w j).im) / Complex.normSq (w k - w j)
```
sealed at sha256 `f0c0044b3388b9a9…` · [source, line 199](../NGon.lean#L199)

### `field_im`

Bridge to the `(x, y)`-convention of the root module, imaginary part: the radial component of the Kirchhoff velocity at vertex `k` is `+g/(2pi)` times the sum of `(x_k - x_j)/|w_k - w_j|^2`, matching the `(x, y)`-field of the root module.
```lean
theorem field_im (g : ℝ) (N : ℕ) (w : Fin N → ℂ) (k : Fin N) : (field g N w k).im = (g / (2 * Real.pi)) * ∑ j in Finset.univ.erase k, ((w k).re - (w j).re) / Complex.normSq (w k - w j)
```
sealed at sha256 `ca174698c45326ac…` · [source, line 210](../NGon.lean#L210)

### `ker_pair` ★

The pairing identity: the two conjugate legs of the roots-of-unity sum cancel — `ker (1 - u_m) + ker (1 - u_(N-m)) = 1` for `1 <= m < N`, where `u_m = exp(2*pi*i*m/N)`. This is the discrete heartbeat of Theorem A: it halves `N-1` summands into `N-1` constants and forces the shape-factor sum `sum_(m≠0) 1/(1 - u_m) = (N-1)/2`.
```lean
theorem ker_pair {N : ℕ} (hN : 0 < N) {m : ℕ} (h1 : 1 ≤ m) (h2 : m < N) : ker (1 - unity N m) + ker (1 - unity N (N - m)) = 1
```
sealed at sha256 `52223430070753a5…` · [source, line 222](../NGon.lean#L222)

### `sum_ker_unity` ★

The core finite sum — the roots-of-unity shape-factor identity of the `N`-gon: `sum_(m≠0) ker (1 - u_m) = (N-1)/2`, i.e. `sum_(m≠0) 1/(1 - exp(2*pi*i*m/N)) = (N-1)/2`. Proven by the pairing `ker(1-u_m) + ker(1-u_(N-m)) = 1` over `m = 1..N-1` plus the re-index `m ↦ N-m`; this single identity forces the polygon's rotation rate.
```lean
theorem sum_ker_unity {N : ℕ} (hN : 0 < N) : ∑ m in Finset.univ.erase (⟨0, hN⟩ : Fin N), ker (1 - unity N (m : ℕ)) = (((N - 1 : ℕ) : ℂ) / 2)
```
sealed at sha256 `68ea86673ca0a7e9…` · [source, line 264](../NGon.lean#L264)

## Section 3

Section 3 — the rigidly rotating polygon, uniqueness of the frequency, the N = 3 bridge (14 theorems).


### `nGonAngle_add`

Angle bookkeeping: going `j + N - k` steps around the polygon equals `j` steps minus `k` steps plus a full turn.
```lean
theorem nGonAngle_add {N : ℕ} (hN : 0 < N) (j k : ℕ) (hk : k < N) : nGonAngle N k + nGonAngle N (j + N - k) = nGonAngle N j + 2 * Real.pi
```
sealed at sha256 `46f309b9e6bacefb…` · [source, line 338](../NGon.lean#L338)

### `unity_shift`

The shifted root `unity N (j + N - k)` factors as `unity N j * (unity N k)^(-1)`.
```lean
theorem unity_shift {N : ℕ} (hN : 0 < N) (j k : ℕ) (hk : k < N) : unity N (j + N - k) = unity N j * (unity N k)⁻¹
```
sealed at sha256 `dfacd5a7808f0b03…` · [source, line 351](../NGon.lean#L351)

### `mod_shift_left`

Modular re-indexing, left half: `((j + N - k) % N + k) % N = j` for `j, k < N`.
```lean
theorem mod_shift_left {N k : ℕ} (hk : k < N) {j : ℕ} (hj : j < N) : ((j + N - k) % N + k) % N = j
```
sealed at sha256 `f5fd1303b3976b0d…` · [source, line 362](../NGon.lean#L362)

### `mod_shift_right`

Modular re-indexing, right half: `((m + k) % N + N - k) % N = m` for `m, k < N`.
```lean
theorem mod_shift_right {N k : ℕ} (hN : 0 < N) (hk : k < N) {m : ℕ} (hm : m < N) : (((m + k) % N + N - k) % N) = m
```
sealed at sha256 `2a3dd603492fef16…` · [source, line 370](../NGon.lean#L370)

### `mod_shift_ne_zero`

The re-index `(j + N - k) % N` never lands on `0` when `j != k < N`.
```lean
theorem mod_shift_ne_zero {N k : ℕ} (hN : 0 < N) (hk : k < N) {j : ℕ} (hj : j < N) (hne : (j : ℕ) ≠ k) : (j + N - k) % N ≠ 0
```
sealed at sha256 `e99178fd0e28b954…` · [source, line 386](../NGon.lean#L386)

### `normSq_nGon`

All polygon vertices sit on the circle of radius `R`: `|nGon R N k|^2 = R^2`.
```lean
theorem normSq_nGon (R : ℝ) (N : ℕ) (k : Fin N) : Complex.normSq (nGon R N k) = R ^ 2
```
sealed at sha256 `afa1cbb0f8cf7792…` · [source, line 398](../NGon.lean#L398)

### `nGon_ne_zero`

No vertex coincides with the origin (for `R != 0`).
```lean
theorem nGon_ne_zero {R : ℝ} {N : ℕ} (hR : R ≠ 0) (k : Fin N) : nGon R N k ≠ 0
```
sealed at sha256 `8e2fc25b2a9ba845…` · [source, line 404](../NGon.lean#L404)

### `ker_nGon_sum` ★

Core reduction: the pairwise kernel sum over the polygon re-indexes to the roots-of-unity finite sum, giving `nGon R N k / R^2 * (N-1)/2`.
```lean
theorem ker_nGon_sum {R : ℝ} {N : ℕ} (hR : R ≠ 0) (k : Fin N) : ∑ j in Finset.univ.erase k, ker (nGon R N k - nGon R N j) = (nGon R N k / ((R ^ 2 : ℝ) : ℂ)) * (((N - 1 : ℕ) : ℂ) / 2)
```
sealed at sha256 `ea0b4cd8f255f9ad…` · [source, line 412](../NGon.lean#L412)

### `nGon_field_eq` ★

MAIN THEOREM: the Kirchhoff field at vertex `k` of the regular `N`-gon equals the rigid rotation velocity `omega * I * z_k` with `omega = G*(N-1)/(4*pi*R^2)`.
```lean
theorem nGon_field_eq {R : ℝ} {N : ℕ} (g : ℝ) (hR : R ≠ 0) (k : Fin N) : field g N (nGon R N) k = ((nGonOmega g R N : ℝ) : ℂ) * Complex.I * nGon R N k
```
sealed at sha256 `126dfc90ed150fe3…` · [source, line 487](../NGon.lean#L487)

### `nGon_omega_forced` ★

Uniqueness (forced value): ANY frequency `nu` for which the regular `N`-gon is a steady rotating solution must equal `nGonOmega g R N`.
```lean
theorem nGon_omega_forced {R : ℝ} {N : ℕ} (g : ℝ) (hR : R ≠ 0) (k : Fin N) (ν : ℝ) (h : field g N (nGon R N) k = (ν : ℂ) * Complex.I * nGon R N k) : ν = nGonOmega g R N
```
sealed at sha256 `6b1ff862e61212da…` · [source, line 501](../NGon.lean#L501)

### `nGon_omega_ne_zero`

The forced frequency is nonzero for nonzero circulation and `N >= 2`.
```lean
theorem nGon_omega_ne_zero {g R : ℝ} {N : ℕ} (hg : g ≠ 0) (hR : R ≠ 0) (hN : 2 ≤ N) : nGonOmega g R N ≠ 0
```
sealed at sha256 `b1ac8de300a2b9f2…` · [source, line 512](../NGon.lean#L512)

### `nGon_omega_pos_iff`

Sign: the polygon rotates counterclockwise iff the circulation `g` is positive (for `R != 0`, `N >= 2`).
```lean
theorem nGon_omega_pos_iff {g R : ℝ} {N : ℕ} (hR : R ≠ 0) (hN : 2 ≤ N) : 0 < nGonOmega g R N ↔ 0 < g
```
sealed at sha256 `fc57d3e0a5c4af22…` · [source, line 532](../NGon.lean#L532)

### `nGon_side3_sq`

The side length of the equilateral triangle: `|z_1 - z_0|^2 = 3*R^2`.
```lean
theorem nGon_side3_sq (R : ℝ) : Complex.normSq (nGon R 3 1 - nGon R 3 0) = 3 * R ^ 2
```
sealed at sha256 `434490ac2057f43d…` · [source, line 559](../NGon.lean#L559)

### `nGon_omega_three`

`N = 3` bridge: in side-length form `a = sqrt(3)*R` the forced frequency is `3*G/(2*pi*a^2)`.
```lean
theorem nGon_omega_three (g R : ℝ) : nGonOmega g R 3 = 3 * g / (2 * Real.pi * (Real.sqrt 3 * R) ^ 2)
```
sealed at sha256 `3d4a9ac34e4c1613…` · [source, line 609](../NGon.lean#L609)

---

*Generated from `NGon.lean` + `seal/manifest.json`; do not edit by hand — rerun `scripts`/`tools` instead.*
