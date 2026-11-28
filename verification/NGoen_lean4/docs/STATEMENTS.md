# The statement layer — all sealed theorems of the five-file program

> Machine-checkable source of truth: the per-file seals (`seal/manifest.json`, `seal/manifest_nside.json`, `seal/manifest_ncore.json`, `seal/manifest_nroots.json`, `seal/manifest_nflow.json` — sha256 of every normalized statement). This page is *generated* from the source — nothing here is hand-written prose about the statements. The payload-carrying statements are marked ★.

## `NGon.lean` — file 1/5 — the regular `N`-gon of identical vortices, rate forced

27 sealed theorems, 100% docstring coverage.

### Section 1

#### `ker_mul`

Multiplicativity of the kernel: `ker` of a product factors through the normalized first factor.

```lean
theorem ker_mul {a b : ℂ} (ha : (Complex.normSq a : ℂ) ≠ 0) (hb : (Complex.normSq b : ℂ) ≠ 0) : ker (a * b) = (a / (Complex.normSq a : ℂ)) * ker b
```
sealed at sha256 `53245516324c…` · [source, line 75](../NGon.lean#L75)

#### `ker_re_I`

Real part of `I*ker z`: the `(x, y)`-bridge for the transverse component.

```lean
theorem ker_re_I (z : ℂ) : (Complex.I * ker z).re = -z.im / Complex.normSq z
```
sealed at sha256 `35af54cee2ae…` · [source, line 83](../NGon.lean#L83)

#### `ker_im_I`

Imaginary part of `I*ker z`: the `(x, y)`-bridge for the radial component.

```lean
theorem ker_im_I (z : ℂ) : (Complex.I * ker z).im = z.re / Complex.normSq z
```
sealed at sha256 `aeec98667957…` · [source, line 96](../NGon.lean#L96)

### Section 2

#### `exp_two_pi_I`

The fundamental identity `exp(2*pi*I) = 1`.

```lean
theorem exp_two_pi_I : Complex.exp (Complex.ofReal' (2 * Real.pi) * Complex.I) = 1
```
sealed at sha256 `980f656a6982…` · [source, line 111](../NGon.lean#L111)

#### `normSq_unity`

Every root of unity lies on the unit circle: `|unity N m| = 1`.

```lean
theorem normSq_unity (N m : ℕ) : Complex.normSq (unity N m) = 1
```
sealed at sha256 `e5a951d77912…` · [source, line 118](../NGon.lean#L118)

#### `unity_mod`

The root of unity only depends on the residue class: `unity N (a % N) = unity N a`.

```lean
theorem unity_mod {N : ℕ} (hN : 0 < N) (a : ℕ) : unity N (a % N) = unity N a
```
sealed at sha256 `5d7f1d5fcc71…` · [source, line 124](../NGon.lean#L124)

#### `unity_congr`

Equal residues give equal roots of unity.

```lean
theorem unity_congr {N : ℕ} (hN : 0 < N) {a b : ℕ} (h : a % N = b % N) : unity N a = unity N b
```
sealed at sha256 `2160b2e03068…` · [source, line 141](../NGon.lean#L141)

#### `unity_inv`

The index-`N-m` root is the inverse of the index-`m` root: `unity N (N-m) = (unity N m)^(-1)` for `0 < m < N`.

```lean
theorem unity_inv {N : ℕ} (hN : 0 < N) {m : ℕ} (h2 : m < N) : unity N (N - m) = (unity N m)⁻¹
```
sealed at sha256 `a2edbce586b4…` · [source, line 147](../NGon.lean#L147)

#### `unity_ne_one`

Nontriviality: for `1 <= m < N` the root `unity N m` is not `1`.

```lean
theorem unity_ne_one {N : ℕ} (hN : 0 < N) {m : ℕ} (h1 : 1 ≤ m) (h2 : m < N) : unity N m ≠ 1
```
sealed at sha256 `4801000d8acf…` · [source, line 161](../NGon.lean#L161)

#### `field_re`

Bridge to the `(x, y)`-convention of the root module, real part: the transverse component of the Kirchhoff velocity at vertex `k` is `-g/(2pi)` times the sum of `(y_k - y_j)/|w_k - w_j|^2` — exactly the `I*(w_k - w_j)/|w_k - w_j|^2` kernel of the planar Kirchhoff equations.

```lean
theorem field_re (g : ℝ) (N : ℕ) (w : Fin N → ℂ) (k : Fin N) : (field g N w k).re = -(g / (2 * Real.pi)) * ∑ j in Finset.univ.erase k, ((w k).im - (w j).im) / Complex.normSq (w k - w j)
```
sealed at sha256 `f0c0044b3388…` · [source, line 199](../NGon.lean#L199)

#### `field_im`

Bridge to the `(x, y)`-convention of the root module, imaginary part: the radial component of the Kirchhoff velocity at vertex `k` is `+g/(2pi)` times the sum of `(x_k - x_j)/|w_k - w_j|^2`, matching the `(x, y)`-field of the root module.

```lean
theorem field_im (g : ℝ) (N : ℕ) (w : Fin N → ℂ) (k : Fin N) : (field g N w k).im = (g / (2 * Real.pi)) * ∑ j in Finset.univ.erase k, ((w k).re - (w j).re) / Complex.normSq (w k - w j)
```
sealed at sha256 `ca174698c453…` · [source, line 210](../NGon.lean#L210)

#### ★ `ker_pair`

The pairing identity: the two conjugate legs of the roots-of-unity sum cancel — `ker (1 - u_m) + ker (1 - u_(N-m)) = 1` for `1 <= m < N`, where `u_m = exp(2*pi*i*m/N)`. This is the discrete heartbeat of Theorem A: it halves `N-1` summands into `N-1` constants and forces the shape-factor sum `sum_(m≠0) 1/(1 - u_m) = (N-1)/2`.

```lean
theorem ker_pair {N : ℕ} (hN : 0 < N) {m : ℕ} (h1 : 1 ≤ m) (h2 : m < N) : ker (1 - unity N m) + ker (1 - unity N (N - m)) = 1
```
sealed at sha256 `522234300707…` · [source, line 222](../NGon.lean#L222)

#### ★ `sum_ker_unity`

The core finite sum — the roots-of-unity shape-factor identity of the `N`-gon: `sum_(m≠0) ker (1 - u_m) = (N-1)/2`, i.e. `sum_(m≠0) 1/(1 - exp(2*pi*i*m/N)) = (N-1)/2`. Proven by the pairing `ker(1-u_m) + ker(1-u_(N-m)) = 1` over `m = 1..N-1` plus the re-index `m ↦ N-m`; this single identity forces the polygon's rotation rate.

```lean
theorem sum_ker_unity {N : ℕ} (hN : 0 < N) : ∑ m in Finset.univ.erase (⟨0, hN⟩ : Fin N), ker (1 - unity N (m : ℕ)) = (((N - 1 : ℕ) : ℂ) / 2)
```
sealed at sha256 `68ea86673ca0…` · [source, line 264](../NGon.lean#L264)

### Section 3

#### `nGonAngle_add`

Angle bookkeeping: going `j + N - k` steps around the polygon equals `j` steps minus `k` steps plus a full turn.

```lean
theorem nGonAngle_add {N : ℕ} (hN : 0 < N) (j k : ℕ) (hk : k < N) : nGonAngle N k + nGonAngle N (j + N - k) = nGonAngle N j + 2 * Real.pi
```
sealed at sha256 `46f309b9e6ba…` · [source, line 338](../NGon.lean#L338)

#### `unity_shift`

The shifted root `unity N (j + N - k)` factors as `unity N j * (unity N k)^(-1)`.

```lean
theorem unity_shift {N : ℕ} (hN : 0 < N) (j k : ℕ) (hk : k < N) : unity N (j + N - k) = unity N j * (unity N k)⁻¹
```
sealed at sha256 `dfacd5a7808f…` · [source, line 351](../NGon.lean#L351)

#### `mod_shift_left`

Modular re-indexing, left half: `((j + N - k) % N + k) % N = j` for `j, k < N`.

```lean
theorem mod_shift_left {N k : ℕ} (hk : k < N) {j : ℕ} (hj : j < N) : ((j + N - k) % N + k) % N = j
```
sealed at sha256 `f5fd1303b397…` · [source, line 362](../NGon.lean#L362)

#### `mod_shift_right`

Modular re-indexing, right half: `((m + k) % N + N - k) % N = m` for `m, k < N`.

```lean
theorem mod_shift_right {N k : ℕ} (hN : 0 < N) (hk : k < N) {m : ℕ} (hm : m < N) : (((m + k) % N + N - k) % N) = m
```
sealed at sha256 `2a3dd603492f…` · [source, line 370](../NGon.lean#L370)

#### `mod_shift_ne_zero`

The re-index `(j + N - k) % N` never lands on `0` when `j != k < N`.

```lean
theorem mod_shift_ne_zero {N k : ℕ} (hN : 0 < N) (hk : k < N) {j : ℕ} (hj : j < N) (hne : (j : ℕ) ≠ k) : (j + N - k) % N ≠ 0
```
sealed at sha256 `e99178fd0e28…` · [source, line 386](../NGon.lean#L386)

#### `normSq_nGon`

All polygon vertices sit on the circle of radius `R`: `|nGon R N k|^2 = R^2`.

```lean
theorem normSq_nGon (R : ℝ) (N : ℕ) (k : Fin N) : Complex.normSq (nGon R N k) = R ^ 2
```
sealed at sha256 `afa1cbb0f8cf…` · [source, line 398](../NGon.lean#L398)

#### `nGon_ne_zero`

No vertex coincides with the origin (for `R != 0`).

```lean
theorem nGon_ne_zero {R : ℝ} {N : ℕ} (hR : R ≠ 0) (k : Fin N) : nGon R N k ≠ 0
```
sealed at sha256 `8e2fc25b2a9b…` · [source, line 404](../NGon.lean#L404)

#### ★ `ker_nGon_sum`

Core reduction: the pairwise kernel sum over the polygon re-indexes to the roots-of-unity finite sum, giving `nGon R N k / R^2 * (N-1)/2`.

```lean
theorem ker_nGon_sum {R : ℝ} {N : ℕ} (hR : R ≠ 0) (k : Fin N) : ∑ j in Finset.univ.erase k, ker (nGon R N k - nGon R N j) = (nGon R N k / ((R ^ 2 : ℝ) : ℂ)) * (((N - 1 : ℕ) : ℂ) / 2)
```
sealed at sha256 `ea0b4cd8f255…` · [source, line 412](../NGon.lean#L412)

#### ★ `nGon_field_eq`

MAIN THEOREM: the Kirchhoff field at vertex `k` of the regular `N`-gon equals the rigid rotation velocity `omega * I * z_k` with `omega = G*(N-1)/(4*pi*R^2)`.

```lean
theorem nGon_field_eq {R : ℝ} {N : ℕ} (g : ℝ) (hR : R ≠ 0) (k : Fin N) : field g N (nGon R N) k = ((nGonOmega g R N : ℝ) : ℂ) * Complex.I * nGon R N k
```
sealed at sha256 `126dfc90ed15…` · [source, line 487](../NGon.lean#L487)

#### ★ `nGon_omega_forced`

Uniqueness (forced value): ANY frequency `nu` for which the regular `N`-gon is a steady rotating solution must equal `nGonOmega g R N`.

```lean
theorem nGon_omega_forced {R : ℝ} {N : ℕ} (g : ℝ) (hR : R ≠ 0) (k : Fin N) (ν : ℝ) (h : field g N (nGon R N) k = (ν : ℂ) * Complex.I * nGon R N k) : ν = nGonOmega g R N
```
sealed at sha256 `6b1ff862e612…` · [source, line 501](../NGon.lean#L501)

#### `nGon_omega_ne_zero`

The forced frequency is nonzero for nonzero circulation and `N >= 2`.

```lean
theorem nGon_omega_ne_zero {g R : ℝ} {N : ℕ} (hg : g ≠ 0) (hR : R ≠ 0) (hN : 2 ≤ N) : nGonOmega g R N ≠ 0
```
sealed at sha256 `b1ac8de300a2…` · [source, line 512](../NGon.lean#L512)

#### `nGon_omega_pos_iff`

Sign: the polygon rotates counterclockwise iff the circulation `g` is positive (for `R != 0`, `N >= 2`).

```lean
theorem nGon_omega_pos_iff {g R : ℝ} {N : ℕ} (hR : R ≠ 0) (hN : 2 ≤ N) : 0 < nGonOmega g R N ↔ 0 < g
```
sealed at sha256 `fc57d3e0a5c4…` · [source, line 532](../NGon.lean#L532)

#### `nGon_side3_sq`

The side length of the equilateral triangle: `|z_1 - z_0|^2 = 3*R^2`.

```lean
theorem nGon_side3_sq (R : ℝ) : Complex.normSq (nGon R 3 1 - nGon R 3 0) = 3 * R ^ 2
```
sealed at sha256 `434490ac2057…` · [source, line 559](../NGon.lean#L559)

#### `nGon_omega_three`

`N = 3` bridge: in side-length form `a = sqrt(3)*R` the forced frequency is `3*G/(2*pi*a^2)`.

```lean
theorem nGon_omega_three (g R : ℝ) : nGonOmega g R 3 = 3 * g / (2 * Real.pi * (Real.sqrt 3 * R) ^ 2)
```
sealed at sha256 `3d4a9ac34e4c…` · [source, line 609](../NGon.lean#L609)


## `NSide.lean` — file 2/5 — the side-length law of the regular `N`-gon

22 sealed theorems, 100% docstring coverage.

### Section 2

#### `exp_I_normSq`

A point `exp(i*theta)` of the unit circle: squared norm `1`.

```lean
theorem exp_I_normSq (x : ℝ) : Complex.normSq (Complex.exp (Complex.ofReal' x * Complex.I)) = 1
```
sealed at sha256 `d1871d6f5f28…` · [source, line 68](../NSide.lean#L68)

#### `exp_I_re`

Real part of `exp(i*theta)`: the cosine.

```lean
theorem exp_I_re (x : ℝ) : (Complex.exp (Complex.ofReal' x * Complex.I)).re = Real.cos x
```
sealed at sha256 `c045203feba2…` · [source, line 74](../NSide.lean#L74)

#### `exp_I_conj_inv`

A point `exp(i*theta)` of the unit circle: the conjugate is the inverse.

```lean
theorem exp_I_conj_inv (x : ℝ) : conj (Complex.exp (Complex.ofReal' x * Complex.I)) = (Complex.exp (Complex.ofReal' x * Complex.I))⁻¹
```
sealed at sha256 `837ee61f47b3…` · [source, line 79](../NSide.lean#L79)

#### `exp_I_conj`

The conjugate of a unit-circle point `exp(i*theta)` is `exp(-i*theta)`.

```lean
theorem exp_I_conj (x : ℝ) : conj (Complex.exp (Complex.ofReal' x * Complex.I)) = Complex.exp (Complex.ofReal' (-x) * Complex.I)
```
sealed at sha256 `89c6b845a498…` · [source, line 93](../NSide.lean#L93)

#### `exp_I_add_inv`

The sum of a unit-circle point and its inverse is twice the cosine: `exp(i*x) + exp(-i*x) = 2*cos(x)` — the bridge from complex phases to real chord lengths.

```lean
theorem exp_I_add_inv (x : ℝ) : Complex.exp (Complex.ofReal' x * Complex.I) + (Complex.exp (Complex.ofReal' x * Complex.I))⁻¹ = 2 * (Real.cos x : ℂ)
```
sealed at sha256 `6be209a2c09c…` · [source, line 104](../NSide.lean#L104)

#### `normSq_unity`

Every root of unity lies on the unit circle: `|unity N m| = 1`.

```lean
theorem normSq_unity (N m : ℕ) : Complex.normSq (unity N m) = 1
```
sealed at sha256 `e5a951d77912…` · [source, line 113](../NSide.lean#L113)

#### `unity_conj_inv`

The conjugate of a root of unity is its inverse: `conj(u_m) = u_m^-1`.

```lean
theorem unity_conj_inv (N m : ℕ) : conj (unity N m) = (unity N m)⁻¹
```
sealed at sha256 `428214c14da0…` · [source, line 117](../NSide.lean#L117)

#### `unity_ne_one`

Nontriviality: for `1 <= m < N` the root `unity N m` is not `1`.

```lean
theorem unity_ne_one {N : ℕ} (hN : 0 < N) {m : ℕ} (h1 : 1 ≤ m) (h2 : m < N) : unity N m ≠ 1
```
sealed at sha256 `4801000d8acf…` · [source, line 121](../NSide.lean#L121)

#### `unity_mul_inv_exp`

The phase of vertex `a` divided by the phase of vertex `b`: `u_a * u_b^-1` is again a unit-circle point, with angle `theta_a - theta_b`.

```lean
theorem unity_mul_inv_exp (N a b : ℕ) : unity N a * (unity N b)⁻¹ = Complex.exp (Complex.ofReal' (nGonAngle N a - nGonAngle N b) * Complex.I)
```
sealed at sha256 `5ab542363354…` · [source, line 157](../NSide.lean#L157)

#### `nGon_eq_cos_sin`

A vertex in `(x, y)` form: `zeta_k = R*(cos(theta_k) + sin(theta_k)*i)` — the bridge to the planar Kirchhoff convention of the root module.

```lean
theorem nGon_eq_cos_sin (R : ℝ) (N : ℕ) (k : Fin N) : nGon R N k = (R : ℂ) * ((Real.cos (nGonAngle N (k : ℕ)) : ℂ) + (Real.sin (nGonAngle N (k : ℕ)) : ℂ) * Complex.I)
```
sealed at sha256 `f4f5a2a7592b…` · [source, line 167](../NSide.lean#L167)

#### `nGon_re`

Real part of a vertex: `x_k = R*cos(theta_k)`.

```lean
theorem nGon_re (R : ℝ) (N : ℕ) (k : Fin N) : (nGon R N k).re = R * Real.cos (nGonAngle N (k : ℕ))
```
sealed at sha256 `642f9f25c5a4…` · [source, line 173](../NSide.lean#L173)

#### `nGon_im`

Imaginary part of a vertex: `y_k = R*sin(theta_k)`.

```lean
theorem nGon_im (R : ℝ) (N : ℕ) (k : Fin N) : (nGon R N k).im = R * Real.sin (nGonAngle N (k : ℕ))
```
sealed at sha256 `0d490833d0d0…` · [source, line 181](../NSide.lean#L181)

#### `normSq_sub_unit`

The squared distance between two unit-circle points, in terms of their relative phases: `|u - v|^2 = 2 - (u*v^-1 + v*u^-1)` — the chord identity at unit radius.

```lean
theorem normSq_sub_unit (u v : ℂ) (hu : u ≠ 0) (hv : v ≠ 0) (hu1 : Complex.normSq u = 1) (hv1 : Complex.normSq v = 1) : ((Complex.normSq (u - v) : ℝ) : ℂ) = 2 - (u * v⁻¹ + v * u⁻¹)
```
sealed at sha256 `174096f01d99…` · [source, line 190](../NSide.lean#L190)

#### ★ `chord_sq`

The chord formula: the squared distance between vertices `a` and `b` of the regular `N`-gon is `2*R^2*(1 - cos(theta_a - theta_b))`. This is the discrete metric heartbeat of the polygon family: every distance in the configuration is read off one cosine.

```lean
theorem chord_sq (R : ℝ) (N : ℕ) (a b : Fin N) : Complex.normSq (nGon R N a - nGon R N b) = 2 * R ^ 2 * (1 - Real.cos (nGonAngle N (a : ℕ) - nGonAngle N (b : ℕ)))
```
sealed at sha256 `dd15594766f2…` · [source, line 208](../NSide.lean#L208)

### Section 3

#### ★ `sideSq`

The side of the regular `N`-gon: `a^2 = 2*R^2*(1 - cos(2*pi/N))`. For `N = 2` this is the diameter of the pair, `a = 2*R`; for `N = 3` it is `a^2 = 3*R^2`, the triangle of file 1/5.

```lean
theorem sideSq (R : ℝ) {N : ℕ} (hN : 2 ≤ N) : Complex.normSq (nGon R N ⟨1, by omega⟩ - nGon R N ⟨0, by omega⟩) = 2 * R ^ 2 * (1 - Real.cos (2 * Real.pi / N))
```
sealed at sha256 `713105eebe22…` · [source, line 256](../NSide.lean#L256)

#### `two_sub_cos_sq`

Twice the factor `1 - cos(2*pi/N)` is the squared distance between the unit-circle roots `u_1` and `u_0 = 1`: `2*(1 - cos(2*pi/N)) = |1 - u_1|^2`.

```lean
theorem two_sub_cos_sq (N : ℕ) (hN : 2 ≤ N) : (2 : ℝ) * (1 - Real.cos (2 * Real.pi / N)) = Complex.normSq (unity N 1 - unity N 0)
```
sealed at sha256 `858f5a6052e3…` · [source, line 268](../NSide.lean#L268)

#### `one_sub_cos_ne_zero`

The factor `1 - cos(2*pi/N)` never vanishes for `N >= 2` — the side form of the rate divides by it.

```lean
theorem one_sub_cos_ne_zero {N : ℕ} (hN : 2 ≤ N) : (1 - Real.cos (2 * Real.pi / N)) ≠ 0
```
sealed at sha256 `988e103e7f67…` · [source, line 288](../NSide.lean#L288)

#### ★ `nGon_omega_side`

SIDE FORM OF THE FORCED RATE: with `a^2 = 2*R^2*(1 - cos(2*pi/N))` the forced frequency of the `N`-gon reads `omega = (N-1)*G*(1 - cos(2*pi/N)) / (2*pi*a^2)` — the form used by the experimental literature.

```lean
theorem nGon_omega_side (g R : ℝ) (hN : 2 ≤ N) : nGonOmega g R N = ((N - 1 : ℕ) * g) * (1 - Real.cos (2 * Real.pi / N)) / (2 * Real.pi * (Real.sqrt (2 * R ^ 2 * (1 - Real.cos (2 * Real.pi / N)))) ^ 2)
```
sealed at sha256 `a8e15e650af8…` · [source, line 303](../NSide.lean#L303)

#### `nGon_omega_ne_zero`

The forced frequency is nonzero for nonzero circulation and `N >= 2` (inherited from file 1/5; the companion of the static-case analysis).

```lean
theorem nGon_omega_ne_zero {g R : ℝ} {N : ℕ} (hg : g ≠ 0) (hR : R ≠ 0) (hN : 2 ≤ N) : nGonOmega g R N ≠ 0
```
sealed at sha256 `b1ac8de300a2…` · [source, line 335](../NSide.lean#L335)

#### ★ `nGon_period`

The rotation period: `T = 2*pi/omega = 8*pi^2*R^2 / ((N-1)*G)` — one full turn of every vortex of the polygon.

```lean
theorem nGon_period (g R : ℝ) (hg : g ≠ 0) (hR : R ≠ 0) (hN : 2 ≤ N) : 2 * Real.pi / nGonOmega g R N = 8 * Real.pi ^ 2 * R ^ 2 / ((N - 1 : ℕ) * g)
```
sealed at sha256 `06ccbf7faedb…` · [source, line 355](../NSide.lean#L355)

#### `sideSq_two`

The pair `N = 2`: the "side" is the diameter, `a^2 = (2*R)^2 = 4*R^2` — the two vortices face each other across the circle.

```lean
theorem sideSq_two (R : ℝ) : Complex.normSq (nGon R 2 ⟨1, by norm_num⟩ - nGon R 2 ⟨0, by norm_num⟩) = 4 * R ^ 2
```
sealed at sha256 `00053b491e11…` · [source, line 368](../NSide.lean#L368)

#### `sideSq_three`

The triangle `N = 3`: `a^2 = 3*R^2` — the equilateral triangle of file 1/5.

```lean
theorem sideSq_three (R : ℝ) : Complex.normSq (nGon R 3 ⟨1, by norm_num⟩ - nGon R 3 ⟨0, by norm_num⟩) = 3 * R ^ 2
```
sealed at sha256 `e48082215985…` · [source, line 380](../NSide.lean#L380)


## `NCore.lean` — file 3/5 — the ring with a core: the `N`-gon plus a central vortex

36 sealed theorems, 100% docstring coverage.

### Section 1

#### `ker_mul`

Multiplicativity of the kernel: `ker` of a product factors through the normalized first factor.

```lean
theorem ker_mul {a b : ℂ} (ha : (Complex.normSq a : ℂ) ≠ 0) (hb : (Complex.normSq b : ℂ) ≠ 0) : ker (a * b) = (a / (Complex.normSq a : ℂ)) * ker b
```
sealed at sha256 `53245516324c…` · [source, line 86](../NCore.lean#L86)

### Section 2

#### `exp_two_pi_I`

The fundamental identity `exp(2*pi*I) = 1`.

```lean
theorem exp_two_pi_I : Complex.exp (Complex.ofReal' (2 * Real.pi) * Complex.I) = 1
```
sealed at sha256 `980f656a6982…` · [source, line 96](../NCore.lean#L96)

#### `normSq_unity`

Every root of unity lies on the unit circle: `|unity N m| = 1`.

```lean
theorem normSq_unity (N m : ℕ) : Complex.normSq (unity N m) = 1
```
sealed at sha256 `e5a951d77912…` · [source, line 103](../NCore.lean#L103)

#### `unity_mod`

The root of unity only depends on the residue class: `unity N (a % N) = unity N a`.

```lean
theorem unity_mod {N : ℕ} (hN : 0 < N) (a : ℕ) : unity N (a % N) = unity N a
```
sealed at sha256 `5d7f1d5fcc71…` · [source, line 109](../NCore.lean#L109)

#### `unity_congr`

Equal residues give equal roots of unity.

```lean
theorem unity_congr {N : ℕ} (hN : 0 < N) {a b : ℕ} (h : a % N = b % N) : unity N a = unity N b
```
sealed at sha256 `2160b2e03068…` · [source, line 126](../NCore.lean#L126)

#### `unity_inv`

The index-`N-m` root is the inverse of the index-`m` root: `unity N (N-m) = (unity N m)^(-1)` for `0 < m < N`.

```lean
theorem unity_inv {N : ℕ} (hN : 0 < N) {m : ℕ} (h2 : m < N) : unity N (N - m) = (unity N m)⁻¹
```
sealed at sha256 `a2edbce586b4…` · [source, line 132](../NCore.lean#L132)

#### `unity_ne_one`

Nontriviality: for `1 <= m < N` the root `unity N m` is not `1`.

```lean
theorem unity_ne_one {N : ℕ} (hN : 0 < N) {m : ℕ} (h1 : 1 ≤ m) (h2 : m < N) : unity N m ≠ 1
```
sealed at sha256 `4801000d8acf…` · [source, line 146](../NCore.lean#L146)

#### `ker_pair`

The pairing identity: the two conjugate legs of the roots-of-unity sum cancel — `ker (1 - u_m) + ker (1 - u_(N-m)) = 1` for `1 <= m < N`, where `u_m = exp(2*pi*i*m/N)`. This is the discrete heartbeat of the polygon: it halves `N-1` summands into `N-1` constants and forces the shape-factor sum `sum_(m≠0) 1/(1 - u_m) = (N-1)/2`.

```lean
theorem ker_pair {N : ℕ} (hN : 0 < N) {m : ℕ} (h1 : 1 ≤ m) (h2 : m < N) : ker (1 - unity N m) + ker (1 - unity N (N - m)) = 1
```
sealed at sha256 `522234300707…` · [source, line 184](../NCore.lean#L184)

#### `sum_ker_unity`

The core finite sum — the roots-of-unity shape-factor identity of the `N`-gon: `sum_(m≠0) ker (1 - u_m) = (N-1)/2`, i.e. `sum_(m≠0) 1/(1 - exp(2*pi*i*m/N)) = (N-1)/2`. Proven by the pairing `ker(1-u_m) + ker(1-u_(N-m)) = 1` over `m = 1..N-1` plus the re-index `m ↦ N-m`; this single identity forces the polygon's rotation rate.

```lean
theorem sum_ker_unity {N : ℕ} (hN : 0 < N) : ∑ m in Finset.univ.erase (⟨0, hN⟩ : Fin N), ker (1 - unity N (m : ℕ)) = (((N - 1 : ℕ) : ℂ) / 2)
```
sealed at sha256 `68ea86673ca0…` · [source, line 226](../NCore.lean#L226)

### Section 3

#### `unity_add`

The product of two roots of unity is the root of the summed index: `u_a * u_b = u_(a+b)`.

```lean
theorem unity_add (N a b : ℕ) : unity N a * unity N b = unity N (a + b)
```
sealed at sha256 `3c7e3fff28a0…` · [source, line 300](../NCore.lean#L300)

#### `unity_pow`

Powers of a root of unity: `(u_m)^k = u_(m*k)`.

```lean
theorem unity_pow (N m k : ℕ) : (unity N m) ^ k = unity N (m * k)
```
sealed at sha256 `eca7dab61744…` · [source, line 311](../NCore.lean#L311)

#### `mod_succ_right`

Modular bookkeeping for the successor shift on `Fin N`, right half: `((m + 1) % N + N - 1) % N = m` for `m < N`.

```lean
theorem mod_succ_right {N : ℕ} (hN : 0 < N) {m : ℕ} (hm : m < N) : ((m + 1) % N + (N - 1)) % N = m
```
sealed at sha256 `18185446b9be…` · [source, line 324](../NCore.lean#L324)

#### `mod_succ_left`

Modular bookkeeping for the successor shift on `Fin N`, left half: `((j + N - 1) % N + 1) % N = j` for `j < N`.

```lean
theorem mod_succ_left {N : ℕ} (hN : 0 < N) {j : ℕ} (hj : j < N) : ((j + N - 1) % N + 1) % N = j
```
sealed at sha256 `baa03e7fe0cb…` · [source, line 336](../NCore.lean#L336)

#### `sum_unity`

The roots of unity sum to zero: `sum_(k<N) u_k = 0` for `N >= 2` — the centroid of the regular polygon is the origin. Proven by the successor-shift trick: multiplying the sum by `u_1` re-indexes it onto itself, and `u_1 != 1` forces the sum to vanish.

```lean
theorem sum_unity {N : ℕ} (hN : 2 ≤ N) : ∑ k in (Finset.univ : Finset (Fin N)), unity N (k : ℕ) = 0
```
sealed at sha256 `a84d6f13aad6…` · [source, line 352](../NCore.lean#L352)

#### `sum_nGon`

The polygon vertices sum to zero: `sum_(k<N) z_k = 0` — the origin is the centroid.

```lean
theorem sum_nGon (R : ℝ) {N : ℕ} (hN : 2 ≤ N) : ∑ k in (Finset.univ : Finset (Fin N)), nGon R N k = 0
```
sealed at sha256 `b8a20a9d0296…` · [source, line 383](../NCore.lean#L383)

#### `ker_neg`

The kernel is odd: `ker(-w) = -ker w`.

```lean
theorem ker_neg (w : ℂ) : ker (-w) = -ker w
```
sealed at sha256 `81837325822c…` · [source, line 392](../NCore.lean#L392)

#### `nGonAngle_add`

Angle bookkeeping: going `j + N - k` steps around the polygon equals `j` steps minus `k` steps plus a full turn.

```lean
theorem nGonAngle_add {N : ℕ} (hN : 0 < N) (j k : ℕ) (hk : k < N) : nGonAngle N k + nGonAngle N (j + N - k) = nGonAngle N j + 2 * Real.pi
```
sealed at sha256 `46f309b9e6ba…` · [source, line 399](../NCore.lean#L399)

#### `unity_shift`

The shifted root `unity N (j + N - k)` factors as `unity N j * (unity N k)^(-1)`.

```lean
theorem unity_shift {N : ℕ} (hN : 0 < N) (j k : ℕ) (hk : k < N) : unity N (j + N - k) = unity N j * (unity N k)⁻¹
```
sealed at sha256 `dfacd5a7808f…` · [source, line 412](../NCore.lean#L412)

#### `mod_shift_left`

Modular re-indexing, left half: `((j + N - k) % N + k) % N = j` for `j, k < N`.

```lean
theorem mod_shift_left {N k : ℕ} (hk : k < N) {j : ℕ} (hj : j < N) : ((j + N - k) % N + k) % N = j
```
sealed at sha256 `f5fd1303b397…` · [source, line 423](../NCore.lean#L423)

#### `mod_shift_right`

Modular re-indexing, right half: `((m + k) % N + N - k) % N = m` for `m, k < N`.

```lean
theorem mod_shift_right {N k : ℕ} (hN : 0 < N) (hk : k < N) {m : ℕ} (hm : m < N) : (((m + k) % N + N - k) % N) = m
```
sealed at sha256 `2a3dd603492f…` · [source, line 431](../NCore.lean#L431)

#### `mod_shift_ne_zero`

The re-index `(j + N - k) % N` never lands on `0` when `j != k < N`.

```lean
theorem mod_shift_ne_zero {N k : ℕ} (hN : 0 < N) (hk : k < N) {j : ℕ} (hj : j < N) (hne : (j : ℕ) ≠ k) : (j + N - k) % N ≠ 0
```
sealed at sha256 `e99178fd0e28…` · [source, line 447](../NCore.lean#L447)

#### `normSq_nGon`

All polygon vertices sit on the circle of radius `R`: `|nGon R N k|^2 = R^2`.

```lean
theorem normSq_nGon (R : ℝ) (N : ℕ) (k : Fin N) : Complex.normSq (nGon R N k) = R ^ 2
```
sealed at sha256 `afa1cbb0f8cf…` · [source, line 459](../NCore.lean#L459)

#### `nGon_ne_zero`

No vertex coincides with the origin (for `R != 0`).

```lean
theorem nGon_ne_zero {R : ℝ} {N : ℕ} (hR : R ≠ 0) (k : Fin N) : nGon R N k ≠ 0
```
sealed at sha256 `8e2fc25b2a9b…` · [source, line 465](../NCore.lean#L465)

#### `ker_nGon_origin`

The kernel of a vertex seen from the origin: `ker(z_k) = z_k/R^2` — the central-vortex term. Holds for every `R`, with both sides `0` in the degenerate case `R = 0`.

```lean
theorem ker_nGon_origin (R : ℝ) (N : ℕ) (k : Fin N) : ker (nGon R N k) = nGon R N k / ((R ^ 2 : ℝ) : ℂ)
```
sealed at sha256 `ab9d119eb9e1…` · [source, line 473](../NCore.lean#L473)

#### `ker_nGon_sum`

Core reduction: the pairwise kernel sum over the polygon re-indexes to the roots-of-unity finite sum, giving `nGon R N k / R^2 * (N-1)/2`.

```lean
theorem ker_nGon_sum {R : ℝ} {N : ℕ} (hR : R ≠ 0) (k : Fin N) : ∑ j in Finset.univ.erase k, ker (nGon R N k - nGon R N j) = (nGon R N k / ((R ^ 2 : ℝ) : ℂ)) * (((N - 1 : ℕ) : ℂ) / 2)
```
sealed at sha256 `ea0b4cd8f255…` · [source, line 480](../NCore.lean#L480)

### Section 4

#### `nGon_field_eq`

The polygon main theorem (inherited from file 1/5, re-proven with the shared machinery): the ring field at vertex `k` is the rigid rotation `omega_nGon * I * z_k` with `omega_nGon = G*(N-1)/(4*pi*R^2)`.

```lean
theorem nGon_field_eq {R : ℝ} {N : ℕ} (g : ℝ) (hR : R ≠ 0) (k : Fin N) : field g N (nGon R N) k = ((nGonOmega g R N : ℝ) : ℂ) * Complex.I * nGon R N k
```
sealed at sha256 `126dfc90ed15…` · [source, line 563](../NCore.lean#L563)

#### `nCoreOmega_eq_single`

The forced frequency of the ring-with-core in single-fraction form: `omega = (G*(N-1) + 2*G0)/(4*pi*R^2)`.

```lean
theorem nCoreOmega_eq_single (g g0 R : ℝ) (N : ℕ) : nCoreOmega g g0 R N = (g * ((N - 1 : ℕ) : ℝ) + 2 * g0) / (4 * Real.pi * R ^ 2)
```
sealed at sha256 `55091b8628d0…` · [source, line 577](../NCore.lean#L577)

#### ★ `nCore_field_eq`

MAIN THEOREM: the Kirchhoff field at ring vertex `k` of the ring-with-core equals the rigid rotation velocity `omega * I * z_k` with `omega = G*(N-1)/(4*pi*R^2) + G0/(2*pi*R^2)` — the polygon rate plus the core rate.

```lean
theorem nCore_field_eq {R : ℝ} {N : ℕ} (g g0 : ℝ) (hR : R ≠ 0) (k : Fin N) : nCoreField g g0 R N k = ((nCoreOmega g g0 R N : ℝ) : ℂ) * Complex.I * nGon R N k
```
sealed at sha256 `67f6036aaf6f…` · [source, line 591](../NCore.lean#L591)

#### ★ `nCore_omega_forced`

Uniqueness (forced value): ANY frequency `nu` for which the ring-with-core is a steady rotating solution must equal `nCoreOmega g g0 R N`.

```lean
theorem nCore_omega_forced {R : ℝ} {N : ℕ} (g g0 : ℝ) (hR : R ≠ 0) (k : Fin N) (ν : ℝ) (h : nCoreField g g0 R N k = (ν : ℂ) * Complex.I * nGon R N k) : ν = nCoreOmega g g0 R N
```
sealed at sha256 `c11966112061…` · [source, line 605](../NCore.lean#L605)

#### ★ `nCore_center_field`

The central vortex feels zero force from a symmetric ring: `nCoreFieldCenter = 0` for every ring circulation — the roots of unity sum to zero.

```lean
theorem nCore_center_field (g R : ℝ) {N : ℕ} (hN : 2 ≤ N) : nCoreFieldCenter g R N = 0
```
sealed at sha256 `ece3df8ea290…` · [source, line 617](../NCore.lean#L617)

#### ★ `nCore_omega_eq_zero_iff`

STATIC RING: the forced frequency of the ring-with-core vanishes exactly when the core circulation is the critical value `G0 = -G*(N-1)/2`.

```lean
theorem nCore_omega_eq_zero_iff {g R : ℝ} {N : ℕ} (hR : R ≠ 0) (hN : 2 ≤ N) (g0 : ℝ) : nCoreOmega g g0 R N = 0 ↔ g0 = -(g * ((N - 1 : ℕ) : ℝ)) / 2
```
sealed at sha256 `311cc80d189f…` · [source, line 630](../NCore.lean#L630)

#### `nCore_static_field`

The static configuration in full: with the critical core `G0 = -G*(N-1)/2` the whole ring-with-core stands still — the field vanishes at every ring vertex.

```lean
theorem nCore_static_field {g R : ℝ} {N : ℕ} (hR : R ≠ 0) (hN : 2 ≤ N) {g0 : ℝ} (h : g0 = -(g * ((N - 1 : ℕ) : ℝ)) / 2) (k : Fin N) : nCoreField g g0 R N k = 0
```
sealed at sha256 `e895269df445…` · [source, line 651](../NCore.lean#L651)

#### ★ `nCore_omega_eq_circ`

The equal-circulation bridge: when the core carries the same circulation as the ring (`G0 = G`), the forced rate of the ring-with-core equals the rate of a regular `(N+2)`-gon of the same radius — the configuration is the `(N+1)`-vortex "ring with core" of the classical count.

```lean
theorem nCore_omega_eq_circ {g R : ℝ} {N : ℕ} (hN : 2 ≤ N) : nCoreOmega g g R N = nGonOmega g R (N + 2)
```
sealed at sha256 `956e9970fb93…` · [source, line 662](../NCore.lean#L662)

#### `nCore_omega_pos_iff`

Sign of the forced rate: the ring-with-core rotates counterclockwise exactly when `G*(N-1) + 2*G0 > 0` (for `R != 0`).

```lean
theorem nCore_omega_pos_iff {g R : ℝ} {N : ℕ} (hR : R ≠ 0) (g0 : ℝ) : 0 < nCoreOmega g g0 R N ↔ 0 < g * ((N - 1 : ℕ) : ℝ) + 2 * g0
```
sealed at sha256 `a2ef10d5802d…` · [source, line 680](../NCore.lean#L680)

#### `nCore_omega_ne_zero`

The forced rate is nonzero exactly off the critical core: `G*(N-1) + 2*G0 != 0` implies `omega != 0`.

```lean
theorem nCore_omega_ne_zero {g R : ℝ} {N : ℕ} (hR : R ≠ 0) (g0 : ℝ) (h : g * ((N - 1 : ℕ) : ℝ) + 2 * g0 ≠ 0) : nCoreOmega g g0 R N ≠ 0
```
sealed at sha256 `a8a9315a6372…` · [source, line 698](../NCore.lean#L698)

#### `nCore_omega_three`

The triangle with an equal core: for `N = 3` and `G0 = G` the forced rate is `omega = G/(pi*R^2)` — the equilateral triangle plus center of the parent module.

```lean
theorem nCore_omega_three (g R : ℝ) : nCoreOmega g g R 3 = g / (Real.pi * R ^ 2)
```
sealed at sha256 `c32c13fa7006…` · [source, line 712](../NCore.lean#L712)


## `NRoots.lean` — file 4/5 — the roots-of-unity engine: geometric sums, partial fractions, cross-ring kernels

21 sealed theorems, 100% docstring coverage.

### Section 2

#### `exp_two_pi_I`

The fundamental identity `exp(2*pi*I) = 1`.

```lean
theorem exp_two_pi_I : Complex.exp (Complex.ofReal' (2 * Real.pi) * Complex.I) = 1
```
sealed at sha256 `980f656a6982…` · [source, line 67](../NRoots.lean#L67)

#### `normSq_unity`

Every root of unity lies on the unit circle: `|unity N m| = 1`.

```lean
theorem normSq_unity (N m : ℕ) : Complex.normSq (unity N m) = 1
```
sealed at sha256 `e5a951d77912…` · [source, line 74](../NRoots.lean#L74)

#### `unity_mod`

The root of unity only depends on the residue class: `unity N (a % N) = unity N a`.

```lean
theorem unity_mod {N : ℕ} (hN : 0 < N) (a : ℕ) : unity N (a % N) = unity N a
```
sealed at sha256 `5d7f1d5fcc71…` · [source, line 80](../NRoots.lean#L80)

#### `unity_congr`

Equal residues give equal roots of unity.

```lean
theorem unity_congr {N : ℕ} (hN : 0 < N) {a b : ℕ} (h : a % N = b % N) : unity N a = unity N b
```
sealed at sha256 `2160b2e03068…` · [source, line 97](../NRoots.lean#L97)

#### `unity_inv`

The index-`N-m` root is the inverse of the index-`m` root: `unity N (N-m) = (unity N m)^(-1)` for `0 < m < N`.

```lean
theorem unity_inv {N : ℕ} (hN : 0 < N) {m : ℕ} (h2 : m < N) : unity N (N - m) = (unity N m)⁻¹
```
sealed at sha256 `a2edbce586b4…` · [source, line 103](../NRoots.lean#L103)

#### `unity_ne_one`

Nontriviality: for `1 <= m < N` the root `unity N m` is not `1`.

```lean
theorem unity_ne_one {N : ℕ} (hN : 0 < N) {m : ℕ} (h1 : 1 ≤ m) (h2 : m < N) : unity N m ≠ 1
```
sealed at sha256 `4801000d8acf…` · [source, line 117](../NRoots.lean#L117)

#### `unity_add`

The product of two roots of unity is the root of the summed index: `u_a * u_b = u_(a+b)`.

```lean
theorem unity_add (N a b : ℕ) : unity N a * unity N b = unity N (a + b)
```
sealed at sha256 `3c7e3fff28a0…` · [source, line 152](../NRoots.lean#L152)

#### `unity_pow`

Powers of a root of unity: `(u_m)^k = u_(m*k)`.

```lean
theorem unity_pow (N m k : ℕ) : (unity N m) ^ k = unity N (m * k)
```
sealed at sha256 `eca7dab61744…` · [source, line 163](../NRoots.lean#L163)

#### `mod_succ_right`

Modular bookkeeping for the successor shift on `Fin N`, right half: `((m + 1) % N + N - 1) % N = m` for `m < N`.

```lean
theorem mod_succ_right {N : ℕ} (hN : 0 < N) {m : ℕ} (hm : m < N) : ((m + 1) % N + (N - 1)) % N = m
```
sealed at sha256 `18185446b9be…` · [source, line 176](../NRoots.lean#L176)

#### `mod_succ_left`

Modular bookkeeping for the successor shift on `Fin N`, left half: `((j + N - 1) % N + 1) % N = j` for `j < N`.

```lean
theorem mod_succ_left {N : ℕ} (hN : 0 < N) {j : ℕ} (hj : j < N) : ((j + N - 1) % N + 1) % N = j
```
sealed at sha256 `baa03e7fe0cb…` · [source, line 188](../NRoots.lean#L188)

#### `unity_pow_N`

Every `N`-th root of unity is an `N`-th power of one: `u_m^N = 1`.

```lean
theorem unity_pow_N {N : ℕ} (hN : 0 < N) (m : ℕ) : (unity N m) ^ N = 1
```
sealed at sha256 `0dd713817839…` · [source, line 202](../NRoots.lean#L202)

#### `sum_unity_pow_eq_N`

GEOMETRIC-SUM DICHOTOMY, full cycle: `sum_(m<N) u_r^m = N` when `N` divides `r` — every term of the sum equals `1`.

```lean
theorem sum_unity_pow_eq_N {N : ℕ} (hN : 0 < N) {r : ℕ} (hdiv : N ∣ r) : ∑ m in (Finset.univ : Finset (Fin N)), (unity N r) ^ (m : ℕ) = ((N : ℕ) : ℂ)
```
sealed at sha256 `3ffb0ab3fffb…` · [source, line 211](../NRoots.lean#L211)

#### ★ `sum_unity_pow_eq_zero`

GEOMETRIC-SUM DICHOTOMY, vanishing half: `sum_(m<N) u_r^m = 0` when `N` does not divide `r` — the successor-shift trick: multiplying the sum by `u_r` re-indexes it onto itself, and `u_r != 1` forces the sum to vanish.

```lean
theorem sum_unity_pow_eq_zero {N : ℕ} (hN : 0 < N) {r : ℕ} (hnd : r % N ≠ 0) : ∑ m in (Finset.univ : Finset (Fin N)), (unity N r) ^ (m : ℕ) = 0
```
sealed at sha256 `452d8940668d…` · [source, line 225](../NRoots.lean#L225)

#### ★ `sum_unity`

The centroid identity re-derived from the engine: `sum_(k<N) u_k = 0` for `N >= 2` — the case `r = 1` of the geometric-sum dichotomy.

```lean
theorem sum_unity {N : ℕ} (hN : 2 ≤ N) : ∑ k in (Finset.univ : Finset (Fin N)), unity N (k : ℕ) = 0
```
sealed at sha256 `a84d6f13aad6…` · [source, line 277](../NRoots.lean#L277)

### Section 3

#### `ker_neg`

The kernel is odd: `ker(-w) = -ker w`.

```lean
theorem ker_neg (w : ℂ) : ker (-w) = -ker w
```
sealed at sha256 `81837325822c…` · [source, line 292](../NRoots.lean#L292)

#### `unity_conj_inv`

The conjugate of a root of unity is its inverse: `conj(u_m) = u_m^-1`.

```lean
theorem unity_conj_inv (N m : ℕ) : conj (unity N m) = (unity N m)⁻¹
```
sealed at sha256 `428214c14da0…` · [source, line 298](../NRoots.lean#L298)

#### `ker_eq_inv_conj`

The kernel in reciprocal-conjugate form: `ker w = 1/conj w` for `w != 0` — the form in which partial fractions act.

```lean
theorem ker_eq_inv_conj {w : ℂ} (hw : w ≠ 0) : ker w = (conj w)⁻¹
```
sealed at sha256 `34322be8bf70…` · [source, line 309](../NRoots.lean#L309)

#### `pow_sub_pow_geom`

The geometric factorization: `c^(n+1) - y^(n+1) = (c - y) * sum_(r<n+1) c^(n-r) * y^r`.

```lean
theorem pow_sub_pow_geom (c y : ℂ) (n : ℕ) : c ^ (n + 1) - y ^ (n + 1) = (c - y) * ∑ r in Finset.range (n + 1), c ^ (n - r) * y ^ r
```
sealed at sha256 `11f284e85a17…` · [source, line 322](../NRoots.lean#L322)

#### ★ `sum_inv_unity`

PARTIAL FRACTIONS over the roots of unity: for `c^N != rho^N`, `sum_(m<N) 1/(c - rho*u_m) = N*c^(N-1)/(c^N - rho^N)`. This is the engine that turns every cross-ring kernel sum into a closed rational form.

```lean
theorem sum_inv_unity {N : ℕ} (hN : 0 < N) (c rho : ℂ) (hden : (c ^ (N : ℕ) - rho ^ (N : ℕ) : ℂ) ≠ 0) : ∑ m in (Finset.univ : Finset (Fin N)), (c - rho * unity N (m : ℕ))⁻¹ = ((N : ℕ) : ℂ) * c ^ ((N : ℕ) - 1) / (c ^ (N : ℕ) - rho ^ (N : ℕ))
```
sealed at sha256 `491ea0100e51…` · [source, line 355](../NRoots.lean#L355)

#### `mod_N_sub_twice`

The half-turn involution on the residues: applying `j ↦ (N - j) % N` twice returns `j`.

```lean
theorem mod_N_sub_twice {N : ℕ} {j : ℕ} (hj : j < N) : (N - (N - j) % N) % N = j
```
sealed at sha256 `3f590a564618…` · [source, line 401](../NRoots.lean#L401)

#### ★ `sum_ker_cross`

The kernel form of the partial fractions: for `conj(z)^N != conj(rho)^N`, `sum_(j<N) ker (z - rho*u_j) = N*conj(z)^(N-1) / (conj(z)^N - conj(rho)^N)` — the field of a whole regular ring measured at an arbitrary point `z` outside its radius orbit.

```lean
theorem sum_ker_cross {N : ℕ} (hN : 0 < N) (z rho : ℂ) (hden : ((conj z) ^ (N : ℕ) - (conj rho) ^ (N : ℕ) : ℂ) ≠ 0) : ∑ j in (Finset.univ : Finset (Fin N)), ker (z - rho * unity N (j : ℕ)) = ((N : ℕ) : ℂ) * (conj z) ^ ((N : ℕ) - 1) / ((conj z) ^ (N : ℕ) - (conj rho) ^ (N : ℕ))
```
sealed at sha256 `73fa30d27ead…` · [source, line 413](../NRoots.lean#L413)


## `NFlow.lean` — file 5/5 — the rotational flow: the polygon as a Kirchhoff solution for all time

33 sealed theorems, 100% docstring coverage.

### Section 1

#### `ker_mul`

Multiplicativity of the kernel: `ker` of a product factors through the normalized first factor.

```lean
theorem ker_mul {a b : ℂ} (ha : (Complex.normSq a : ℂ) ≠ 0) (hb : (Complex.normSq b : ℂ) ≠ 0) : ker (a * b) = (a / (Complex.normSq a : ℂ)) * ker b
```
sealed at sha256 `53245516324c…` · [source, line 77](../NFlow.lean#L77)

#### `ker_re_I`

Real part of `I*ker z`: the `(x, y)`-bridge for the transverse component.

```lean
theorem ker_re_I (z : ℂ) : (Complex.I * ker z).re = -z.im / Complex.normSq z
```
sealed at sha256 `35af54cee2ae…` · [source, line 85](../NFlow.lean#L85)

#### `ker_im_I`

Imaginary part of `I*ker z`: the `(x, y)`-bridge for the radial component.

```lean
theorem ker_im_I (z : ℂ) : (Complex.I * ker z).im = z.re / Complex.normSq z
```
sealed at sha256 `aeec98667957…` · [source, line 98](../NFlow.lean#L98)

### Section 2

#### `exp_two_pi_I`

The fundamental identity `exp(2*pi*I) = 1`.

```lean
theorem exp_two_pi_I : Complex.exp (Complex.ofReal' (2 * Real.pi) * Complex.I) = 1
```
sealed at sha256 `980f656a6982…` · [source, line 113](../NFlow.lean#L113)

#### `normSq_unity`

Every root of unity lies on the unit circle: `|unity N m| = 1`.

```lean
theorem normSq_unity (N m : ℕ) : Complex.normSq (unity N m) = 1
```
sealed at sha256 `e5a951d77912…` · [source, line 120](../NFlow.lean#L120)

#### `unity_mod`

The root of unity only depends on the residue class: `unity N (a % N) = unity N a`.

```lean
theorem unity_mod {N : ℕ} (hN : 0 < N) (a : ℕ) : unity N (a % N) = unity N a
```
sealed at sha256 `5d7f1d5fcc71…` · [source, line 126](../NFlow.lean#L126)

#### `unity_congr`

Equal residues give equal roots of unity.

```lean
theorem unity_congr {N : ℕ} (hN : 0 < N) {a b : ℕ} (h : a % N = b % N) : unity N a = unity N b
```
sealed at sha256 `2160b2e03068…` · [source, line 143](../NFlow.lean#L143)

#### `unity_inv`

The index-`N-m` root is the inverse of the index-`m` root: `unity N (N-m) = (unity N m)^(-1)` for `0 < m < N`.

```lean
theorem unity_inv {N : ℕ} (hN : 0 < N) {m : ℕ} (h2 : m < N) : unity N (N - m) = (unity N m)⁻¹
```
sealed at sha256 `a2edbce586b4…` · [source, line 149](../NFlow.lean#L149)

#### `unity_ne_one`

Nontriviality: for `1 <= m < N` the root `unity N m` is not `1`.

```lean
theorem unity_ne_one {N : ℕ} (hN : 0 < N) {m : ℕ} (h1 : 1 ≤ m) (h2 : m < N) : unity N m ≠ 1
```
sealed at sha256 `4801000d8acf…` · [source, line 163](../NFlow.lean#L163)

#### `field_re`

Bridge to the `(x, y)`-convention of the root module, real part: the transverse component of the Kirchhoff velocity at vertex `k` is `-g/(2pi)` times the sum of `(y_k - y_j)/|w_k - w_j|^2` — exactly the `I*(w_k - w_j)/|w_k - w_j|^2` kernel of the planar Kirchhoff equations.

```lean
theorem field_re (g : ℝ) (N : ℕ) (w : Fin N → ℂ) (k : Fin N) : (field g N w k).re = -(g / (2 * Real.pi)) * ∑ j in Finset.univ.erase k, ((w k).im - (w j).im) / Complex.normSq (w k - w j)
```
sealed at sha256 `f0c0044b3388…` · [source, line 201](../NFlow.lean#L201)

#### `field_im`

Bridge to the `(x, y)`-convention of the root module, imaginary part: the radial component of the Kirchhoff velocity at vertex `k` is `+g/(2pi)` times the sum of `(x_k - x_j)/|w_k - w_j|^2`, matching the `(x, y)`-field of the root module.

```lean
theorem field_im (g : ℝ) (N : ℕ) (w : Fin N → ℂ) (k : Fin N) : (field g N w k).im = (g / (2 * Real.pi)) * ∑ j in Finset.univ.erase k, ((w k).re - (w j).re) / Complex.normSq (w k - w j)
```
sealed at sha256 `ca174698c453…` · [source, line 212](../NFlow.lean#L212)

#### `ker_pair`

The pairing identity: the two conjugate legs of the roots-of-unity sum cancel — `ker (1 - u_m) + ker (1 - u_(N-m)) = 1` for `1 <= m < N`, where `u_m = exp(2*pi*i*m/N)`. This is the discrete heartbeat of Theorem A: it halves `N-1` summands into `N-1` constants and forces the shape-factor sum `sum_(m≠0) 1/(1 - u_m) = (N-1)/2`.

```lean
theorem ker_pair {N : ℕ} (hN : 0 < N) {m : ℕ} (h1 : 1 ≤ m) (h2 : m < N) : ker (1 - unity N m) + ker (1 - unity N (N - m)) = 1
```
sealed at sha256 `522234300707…` · [source, line 224](../NFlow.lean#L224)

#### `sum_ker_unity`

The core finite sum — the roots-of-unity shape-factor identity of the `N`-gon: `sum_(m≠0) ker (1 - u_m) = (N-1)/2`, i.e. `sum_(m≠0) 1/(1 - exp(2*pi*i*m/N)) = (N-1)/2`. Proven by the pairing `ker(1-u_m) + ker(1-u_(N-m)) = 1` over `m = 1..N-1` plus the re-index `m ↦ N-m`; this single identity forces the polygon's rotation rate.

```lean
theorem sum_ker_unity {N : ℕ} (hN : 0 < N) : ∑ m in Finset.univ.erase (⟨0, hN⟩ : Fin N), ker (1 - unity N (m : ℕ)) = (((N - 1 : ℕ) : ℂ) / 2)
```
sealed at sha256 `68ea86673ca0…` · [source, line 266](../NFlow.lean#L266)

### Section 3

#### `nGonAngle_add`

Angle bookkeeping: going `j + N - k` steps around the polygon equals `j` steps minus `k` steps plus a full turn.

```lean
theorem nGonAngle_add {N : ℕ} (hN : 0 < N) (j k : ℕ) (hk : k < N) : nGonAngle N k + nGonAngle N (j + N - k) = nGonAngle N j + 2 * Real.pi
```
sealed at sha256 `46f309b9e6ba…` · [source, line 340](../NFlow.lean#L340)

#### `unity_shift`

The shifted root `unity N (j + N - k)` factors as `unity N j * (unity N k)^(-1)`.

```lean
theorem unity_shift {N : ℕ} (hN : 0 < N) (j k : ℕ) (hk : k < N) : unity N (j + N - k) = unity N j * (unity N k)⁻¹
```
sealed at sha256 `dfacd5a7808f…` · [source, line 353](../NFlow.lean#L353)

#### `mod_shift_left`

Modular re-indexing, left half: `((j + N - k) % N + k) % N = j` for `j, k < N`.

```lean
theorem mod_shift_left {N k : ℕ} (hk : k < N) {j : ℕ} (hj : j < N) : ((j + N - k) % N + k) % N = j
```
sealed at sha256 `f5fd1303b397…` · [source, line 364](../NFlow.lean#L364)

#### `mod_shift_right`

Modular re-indexing, right half: `((m + k) % N + N - k) % N = m` for `m, k < N`.

```lean
theorem mod_shift_right {N k : ℕ} (hN : 0 < N) (hk : k < N) {m : ℕ} (hm : m < N) : (((m + k) % N + N - k) % N) = m
```
sealed at sha256 `2a3dd603492f…` · [source, line 372](../NFlow.lean#L372)

#### `mod_shift_ne_zero`

The re-index `(j + N - k) % N` never lands on `0` when `j != k < N`.

```lean
theorem mod_shift_ne_zero {N k : ℕ} (hN : 0 < N) (hk : k < N) {j : ℕ} (hj : j < N) (hne : (j : ℕ) ≠ k) : (j + N - k) % N ≠ 0
```
sealed at sha256 `e99178fd0e28…` · [source, line 388](../NFlow.lean#L388)

#### `normSq_nGon`

All polygon vertices sit on the circle of radius `R`: `|nGon R N k|^2 = R^2`.

```lean
theorem normSq_nGon (R : ℝ) (N : ℕ) (k : Fin N) : Complex.normSq (nGon R N k) = R ^ 2
```
sealed at sha256 `afa1cbb0f8cf…` · [source, line 400](../NFlow.lean#L400)

#### `nGon_ne_zero`

No vertex coincides with the origin (for `R != 0`).

```lean
theorem nGon_ne_zero {R : ℝ} {N : ℕ} (hR : R ≠ 0) (k : Fin N) : nGon R N k ≠ 0
```
sealed at sha256 `8e2fc25b2a9b…` · [source, line 406](../NFlow.lean#L406)

#### `ker_nGon_sum`

Core reduction: the pairwise kernel sum over the polygon re-indexes to the roots-of-unity finite sum, giving `nGon R N k / R^2 * (N-1)/2`.

```lean
theorem ker_nGon_sum {R : ℝ} {N : ℕ} (hR : R ≠ 0) (k : Fin N) : ∑ j in Finset.univ.erase k, ker (nGon R N k - nGon R N j) = (nGon R N k / ((R ^ 2 : ℝ) : ℂ)) * (((N - 1 : ℕ) : ℂ) / 2)
```
sealed at sha256 `ea0b4cd8f255…` · [source, line 414](../NFlow.lean#L414)

#### `nGon_field_eq`

MAIN THEOREM: the Kirchhoff field at vertex `k` of the regular `N`-gon equals the rigid rotation velocity `omega * I * z_k` with `omega = G*(N-1)/(4*pi*R^2)`.

```lean
theorem nGon_field_eq {R : ℝ} {N : ℕ} (g : ℝ) (hR : R ≠ 0) (k : Fin N) : field g N (nGon R N) k = ((nGonOmega g R N : ℝ) : ℂ) * Complex.I * nGon R N k
```
sealed at sha256 `126dfc90ed15…` · [source, line 489](../NFlow.lean#L489)

#### `nGon_omega_ne_zero`

Uniqueness (forced value): ANY frequency `nu` for which the regular `N`-gon is a steady rotating solution must equal `nGonOmega g R N`.

```lean
theorem nGon_omega_ne_zero {g R : ℝ} {N : ℕ} (hg : g ≠ 0) (hR : R ≠ 0) (hN : 2 ≤ N) : nGonOmega g R N ≠ 0
```
sealed at sha256 `b1ac8de300a2…` · [source, line 503](../NFlow.lean#L503)

### Section 4

#### ★ `ker_smul`

Multiplication by a unit-complex scalar commutes with the kernel: `ker(c*w) = c*ker w` for `|c| = 1` — the heart of the rotational covariance.

```lean
theorem ker_smul (hc : (Complex.normSq c : ℂ) = 1) (w : ℂ) : ker (c * w) = c * ker w
```
sealed at sha256 `4ca861be5fd0…` · [source, line 525](../NFlow.lean#L525)

#### `normSq_exp_I_real`

A point `exp(i*theta)` of the unit circle: squared norm `1`.

```lean
theorem normSq_exp_I_real (x : ℝ) : ((Complex.normSq (Complex.exp (Complex.ofReal' x * Complex.I)) : ℝ) : ℂ) = 1
```
sealed at sha256 `e94884304aaf…` · [source, line 534](../NFlow.lean#L534)

#### ★ `field_smul`

COVARIANCE: the Kirchhoff field of a unit-rotation of a configuration is the rotated field — `field g N (fun k => c * w k) k = c * field g N w k` for `|c| = 1`.

```lean
theorem field_smul (hc : (Complex.normSq c : ℂ) = 1) (g : ℝ) (N : ℕ) (w : Fin N → ℂ) (k : Fin N) : field g N (fun k => c * w k) k = c * field g N w k
```
sealed at sha256 `7780f0f0109e…` · [source, line 542](../NFlow.lean#L542)

#### `unity_add`

The product of two roots of unity is the root of the summed index: `u_a * u_b = u_(a+b)`.

```lean
theorem unity_add (N a b : ℕ) : unity N a * unity N b = unity N (a + b)
```
sealed at sha256 `3c7e3fff28a0…` · [source, line 549](../NFlow.lean#L549)

#### `nGon_eq_R_unity_mod`

A vertex in root-of-unity form (raw-index version).

```lean
theorem nGon_eq_R_unity_mod (R : ℝ) (N : ℕ) (hN : 0 < N) (m : ℕ) : nGon R N ⟨m % N, Nat.mod_lt _ hN⟩ = (R : ℂ) * unity N (m % N)
```
sealed at sha256 `bc2eb8f31cf5…` · [source, line 560](../NFlow.lean#L560)

#### `nGon_eq_R_unity`

A vertex in root-of-unity form.

```lean
theorem nGon_eq_R_unity (R : ℝ) (N : ℕ) (k : Fin N) : nGon R N k = (R : ℂ) * unity N (k : ℕ)
```
sealed at sha256 `43fbe34b23cb…` · [source, line 564](../NFlow.lean#L564)

#### `nGon_succ`

The successor vertex: `nGon R N ((k+1) % N) = nGon R N k * u_1` — one step around the polygon is multiplication by the first root of unity.

```lean
theorem nGon_succ (R : ℝ) (N : ℕ) (hN : 0 < N) (k : Fin N) : nGon R N ⟨((k : ℕ) + 1) % N, Nat.mod_lt _ hN⟩ = nGon R N k * unity N 1
```
sealed at sha256 `072674957bea…` · [source, line 569](../NFlow.lean#L569)

#### ★ `nGon_flow_field`

THE FLOW: the polygon rotated by `exp(i*omega*t)` is again a rigid-rotation solution — the Kirchhoff field at the rotated configuration equals `omega * I * (rotated vertex)`, for every time `t`. This is the honest formalization of "the polygon rotates rigidly forever": the self-similar motion satisfies the Kirchhoff equations at every instant.

```lean
theorem nGon_flow_field (g : ℝ) (hR : R ≠ 0) (k : Fin N) (t : ℝ) : field g N (fun k => Complex.exp (Complex.ofReal' (nGonOmega g R N * t) * Complex.I) * nGon R N k) k = ((nGonOmega g R N : ℝ) : ℂ) * Complex.I * (Complex.exp (Complex.ofReal' (nGonOmega g R N * t) * Complex.I) * nGon R N k)
```
sealed at sha256 `f22581812c05…` · [source, line 578](../NFlow.lean#L578)

#### ★ `nGon_flow_returns`

The absolute period: at `T = 2*pi/omega` the flow returns every vortex to its own vertex — `exp(i*omega*T) = 1`, so the rotated configuration coincides with the polygon itself.

```lean
theorem nGon_flow_returns (g : ℝ) (hg : g ≠ 0) (hR : R ≠ 0) (hN : 2 ≤ N) (k : Fin N) : Complex.exp (Complex.ofReal' (nGonOmega g R N * (2 * Real.pi / nGonOmega g R N)) * Complex.I) * nGon R N k = nGon R N k
```
sealed at sha256 `a0612f0b19d2…` · [source, line 591](../NFlow.lean#L591)

#### ★ `nGon_flow_shift`

The relative period: at `T_rel = 2*pi/(N*omega)` the flow advances every vortex by one vertex — `exp(i*omega*T_rel) = u_1`, so the rotated configuration is the polygon shifted by one index.

```lean
theorem nGon_flow_shift (g : ℝ) (hg : g ≠ 0) (hR : R ≠ 0) (hN : 2 ≤ N) (k : Fin N) : Complex.exp (Complex.ofReal' (nGonOmega g R N * (2 * Real.pi / (N * nGonOmega g R N))) * Complex.I) * nGon R N k = nGon R N ⟨((k : ℕ) + 1) % N, Nat.mod_lt _ (by have
```
sealed at sha256 `980e1fe2e4ff…` · [source, line 606](../NFlow.lean#L606)


**Total: 139 sealed theorems across the five files; 0 `sorry`, 0 `axiom`; every `#print axioms` reports exactly `propext, Classical.choice, Quot.sound` (machine-checked — see the evidence log).**
