# POLYVORTEX Lean 4 — complete declaration reference (the artifact's public API)

Every declaration of `Polyvortex.lean` (v1.0.2, TW1.b artifact — 1,609 lines, 79 declarations) with its Lean docstring, in file order. Private helpers are marked; they are part of the seal surface and the 100% docstring ratchet. The sha256 of each theorem statement is sealed in `seal/manifest.json`.

SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0


## §0 — Private helpers: cyclic sums and ℂ conjugate/normSq toolkit  (12 declarations)

### `private` `sum_range_shift_one`

```lean
private theorem sum_range_shift_one (f : ℕ → M) (n : ℕ) : ∑ m in Finset.range n, f (m + 1) = ∑ m in Finset.range n, f m + f n - f 0
```

Shifting the index of a `range`-sum by one.

### `private` `sum_rot_shift`

```lean
private theorem sum_rot_shift (f : ℕ → M) (N : ℕ) : ∑ j in Finset.range N, f ((j + 1) % N) = ∑ j in Finset.range N, f j
```

The index translation `m ↦ (m + 1) % N` is summation-invariant.

### `private` `sum_rot`

```lean
private theorem sum_rot (N : ℕ) : ∀ (c : ℕ) (f : ℕ → M), ∑ j in Finset.range N, f ((j + c) % N) = ∑ j in Finset.range N, f j
```

The index translation `m ↦ (m + c) % N` is summation-invariant.

### `private` `sum_range_reflect_aux`

```lean
private theorem sum_range_reflect_aux (f : ℕ → M) : ∀ n : ℕ, ∑ m in Finset.range n, f ((n - 1) - m) = ∑ m in Finset.range n, f m
```

Reflecting the index of a `range`-sum, `m ↦ (n−1)−m`.

### `private` `sum_erase_zero`

```lean
private theorem sum_erase_zero (f : ℕ → M) {N k : ℕ} (hk : k ∈ Finset.range N) : ∑ j in (Finset.range N).erase k, f j = ∑ j in Finset.range N, (if j = k then 0 else f j)
```

A single erased point contributes zero to the full `range`-sum.

### `private` `conj_mul'`

```lean
private theorem conj_mul' (a b : ℂ) : star (a * b) = star a * star b
```

Complex conjugation is multiplicative (`star_mul'`).

### `private` `conj_sub'`

```lean
private theorem conj_sub' (a b : ℂ) : star (a - b) = star a - star b
```

Complex conjugation is additive over differences.

### `private` `conj_pow'`

```lean
private theorem conj_pow' (a : ℂ) : ∀ n : ℕ, star (a ^ n) = (star a) ^ n
```

Complex conjugation commutes with natural powers (`star_pow`).

### `private` `conj_conj'`

```lean
private theorem conj_conj' (z : ℂ) : star (star z) = z
```

Double conjugation is the identity (`star_involutive`).

### `private` `normSq_mul'`

```lean
private theorem normSq_mul' (a b : ℂ) : (Complex.normSq (a * b) : ℂ) = (Complex.normSq a : ℂ) * (Complex.normSq b : ℂ)
```

`normSq` of a product, as a `ℂ`-valued identity.

### `private` `normSq_ofReal'`

```lean
private theorem normSq_ofReal' (r : ℝ) : (Complex.normSq ((r : ℂ)) : ℂ) = ((r * r : ℝ) : ℂ)
```

`normSq` of a real scalar, as a `ℂ`-valued identity.

### `private` `normSq_ne_zero'`

```lean
private theorem normSq_ne_zero' {z : ℂ} (h : z ≠ 0) : Complex.normSq z ≠ 0
```

A nonzero complex number has nonzero `normSq`.


## §1 — Theorem A: the regular `N`-gon ring is an exact Kirchhoff solution (forced)  (28 declarations)

### `rootExp`

```lean
noncomputable def rootExp (N : ℕ) : ℂ
```

The canonical primitive `N`-th root of unity `exp(2πi/N)`.

### `ringPos`

```lean
noncomputable def ringPos (R : ℝ) (ζ : ℂ) (k : ℕ) : ℂ
```

The `k`-th vertex of the regular `N`-gon ring of radius `R` with root `ζ`.

### `ringOmega`

```lean
noncomputable def ringOmega (γ : ℝ) (R : ℝ) (N : ℕ) : ℝ
```

The Kirchhoff angular rate of the regular `N`-gon ring of radius `R`.

### `kirchhoff`

```lean
noncomputable def kirchhoff (γ : ℝ) (z : ℕ → ℂ) (N : ℕ) (k : ℕ) : ℂ
```

The Kirchhoff point-vortex field: the velocity of vertex `k` induced by the other vertices of the configuration `z`.

### `private` `mod_add_zero_eq`

```lean
private theorem mod_add_zero_eq {N j k : ℕ} (hj : j < N) (hk : k < N) (_hkle : k ≤ N) (h : (j + (N - k)) % N = 0) : j = k
```

If `(j + (N−k)) % N = 0` with `j, k < N` then `j = k`.

### `private` `mod_self'`

```lean
private theorem mod_self' {N k : ℕ} (hkle : k ≤ N) : (k + (N - k)) % N = 0
```

`k + (N − k)` reduces to `0` modulo `N`.

### `private` `mod_add_eq_self`

```lean
private theorem mod_add_eq_self {N k d : ℕ} (hk : k < N) (hd1 : 1 ≤ d) (hdN : d < N) (h : (k + d) % N = k) : False
```

If `(k + d) % N = k` then `d` is a positive multiple of `N`; with `1 ≤ d < N` this is absurd.

### `private` `mul_pred_mod`

```lean
private theorem mul_pred_mod {N d : ℕ} (hd1 : 1 ≤ d) (hdN : d < N) : (d * (N - 1)) % N = (N - d) % N
```

For `1 ≤ d < N` the exponents `d·(N−1)` and `N−d` agree modulo `N`.

### `root_ne_zero`

```lean
theorem root_ne_zero {ζ : ℂ} {N : ℕ} (hN : N ≠ 0) (h1 : ζ ^ N = 1) : ζ ≠ 0
```

A nonzero exponent of a root of unity keeps the root nonzero.

### `private` `normSq_pow'`

```lean
private theorem normSq_pow' (a : ℂ) : ∀ n : ℕ, (Complex.normSq (a ^ n) : ℂ) = (Complex.normSq a : ℂ) ^ n | 0 => by simp | n + 1 => by rw [pow_succ, pow_succ, normSq_mul', normSq_pow' a n]  /-- For a nonnegative real `x`, `x ^ N = 1` with `N ≠ 0` forces `x = 1`. -/ private theorem real_pow_eq_one_of_nonneg {x : ℝ} (hx : 0 ≤ x) {N : ℕ} (hN : N ≠ 0) (h : x ^ N = 1) : x = 1
```

`normSq` of a natural power, as a `ℂ`-valued identity.

### `private` `real_pow_eq_one_of_nonneg`

```lean
private theorem real_pow_eq_one_of_nonneg {x : ℝ} (hx : 0 ≤ x) {N : ℕ} (hN : N ≠ 0) (h : x ^ N = 1) : x = 1
```

For a nonnegative real `x`, `x ^ N = 1` with `N ≠ 0` forces `x = 1`.

### `conj_root_unity`

```lean
theorem conj_root_unity {ζ : ℂ} {N : ℕ} (hN : N ≠ 0) (h1 : ζ ^ N = 1) : star ζ = ζ ^ (N - 1)
```

The conjugate of a root of unity is its `(N−1)`-st power.

### `pow_mod_eq`

```lean
theorem pow_mod_eq {ζ : ℂ} {N : ℕ} (h1 : ζ ^ N = 1) (m : ℕ) : ζ ^ (m % N) = ζ ^ m
```

Any exponent of a root of unity reduces modulo `N`.

### `ringPos_sub_ringPos`

```lean
theorem ringPos_sub_ringPos {R : ℝ} {ζ : ℂ} {N : ℕ} (h1 : ζ ^ N = 1) {k j : ℕ} (hk : k < N) (_hj : j < N) : ringPos R ζ k - ringPos R ζ j = (R : ℂ) * ζ ^ k * (1 - ζ ^ ((j + (N - k)) % N))
```

On the ring, the difference of two vertices factors through `1 − ζ^d`.

### `private` `ring_term`

```lean
private theorem ring_term {R : ℝ} {ζ : ℂ} {N : ℕ} (hN : N ≠ 0) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (hR : R ≠ 0) {k j : ℕ} (hk : k < N) (hj : j < N) (hjk : j ≠ k) : Complex.I * (ringPos R ζ k - ringPos R ζ j) / ((Complex.normSq (ringPos R ζ k - ringPos R ζ j) : ℝ) : ℂ) = Complex.I / (R : ℂ) * ζ ^ k * (1 - ζ ^ (N - ((j + (N - k)) % N)))⁻¹
```

The pair velocity of the ring, in geometric form: the vertex pair at cyclic distance `d = (j + (N−k)) % N ∈ [1, N−1]` contributes `iζ^k/(R(1−ζ^{N−d}))`.

### `private` `roots_pair_core`

```lean
private theorem roots_pair_core {x y : ℂ} (hxy : x * y = 1) (_hx0 : x ≠ 0) (hx1 : x ≠ 1) : 1 / (1 - x) + 1 / (1 - y) = 1
```

The field core of the pairing: for `x·y = 1`, `x ≠ 0`, `x ≠ 1` the two reflected fractions sum to one (this covers the fixed point `x = y = −1`).

### `sum_roots_of_unity`

```lean
theorem sum_roots_of_unity {ζ : ℂ} {N : ℕ} (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) : ∑ m in Finset.range (N - 1), 1 / (1 - ζ ^ (m + 1)) = (((N - 1 : ℕ) : ℝ) : ℂ) / 2
```

**The roots-of-unity identity** — the analytic core of Theorem A: `∑_{m=1}^{N−1} 1/(1−ζ^m) = (N−1)/2`, proven by the involution `m ↦ N−m` (the fixed point `m = N/2` contributes `1/2` through the same field identity).

### `ring_velocity`

```lean
theorem ring_velocity (γ : ℝ) (N : ℕ) (hN : 2 ≤ N) (R : ℝ) (hR : R ≠ 0) (ζ : ℂ) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) {k : ℕ} (hk : k < N) : kirchhoff γ (ringPos R ζ) N k = Complex.I * ((ringOmega γ R N : ℝ) : ℂ) * ringPos R ζ k
```

**Theorem A.** The Kirchhoff field on the ring is exactly the solid-rotation field `i·ω_N·z_k` at every vertex.

### `kirchhoff_smul`

```lean
theorem kirchhoff_smul (γ : ℝ) {N : ℕ} {z : ℕ → ℂ} {u : ℂ} (hu : Complex.normSq u = 1) (k : ℕ) : kirchhoff γ (fun j => u * z j) N k = u * kirchhoff γ z N k
```

Rotational equivariance of the Kirchhoff field: multiplication by a unit complex number carries solutions to solutions.

### `normSq_exp_I_mul`

```lean
theorem normSq_exp_I_mul (θ : ℝ) : Complex.normSq (Complex.exp (Complex.I * θ)) = 1
```

The complex exponential of a purely imaginary number lies on the unit circle.

### `ringOrbit`

```lean
noncomputable def ringOrbit (R : ℝ) (ζ : ℂ) (ω : ℝ) (t : ℝ) (k : ℕ) : ℂ
```

The uniformly rotating ring orbit.

### `ringOrbit_deriv`

```lean
theorem ringOrbit_deriv (R : ℝ) (ζ : ℂ) (ω : ℝ) (k : ℕ) (t : ℝ) : HasDerivAt (fun s => ringOrbit R ζ ω s k) (Complex.I * ω * ringOrbit R ζ ω t k) t
```

The orbit is carried at angular rate `ω`: its derivative is `iω·z_k(t)`.

### `kirchhoff_ringOrbit`

```lean
theorem kirchhoff_ringOrbit (γ : ℝ) (N : ℕ) (hN : 2 ≤ N) (R : ℝ) (hR : R ≠ 0) (ζ : ℂ) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (ω : ℝ) (t : ℝ) {k : ℕ} (hk : k < N) : kirchhoff γ (fun j => ringOrbit R ζ ω t j) N k = Complex.I * ((ringOmega γ R N : ℝ) : ℂ) * ringOrbit R ζ ω t k
```

The Kirchhoff field evaluated on the rotating orbit at time `t`.

### `ringOrbit_sol`

```lean
theorem ringOrbit_sol (γ : ℝ) (N : ℕ) (hN : 2 ≤ N) (R : ℝ) (hR : R ≠ 0) (ζ : ℂ) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (ω : ℝ) : (∀ (t : ℝ) (k : ℕ), HasDerivAt (fun s => ringOrbit R ζ ω s k) (kirchhoff γ (fun j => ringOrbit R ζ ω t j) N k) t) ↔ ω = ringOmega γ R N
```

**The forcing theorem for the ring.** A uniformly rotating ring solves the Kirchhoff equations exactly when the angular rate is `ω_N` — the polygonal analogue of the parent monograph's Lagrange forcing theorem.

### `rootExp_pow`

```lean
theorem rootExp_pow {N : ℕ} (hN : N ≠ 0) : rootExp N ^ N = 1
```

The canonical root is a genuine root of unity.

### `rootExp_prim`

```lean
theorem rootExp_prim {N : ℕ} (hN : 2 ≤ N) : ∀ m ∈ Finset.Ico 1 N, rootExp N ^ m ≠ 1
```

The canonical root is primitive.

### `ringOmega_three_eq_lagrange`

```lean
theorem ringOmega_three_eq_lagrange (γ a : ℝ) (ha : a ≠ 0) : ringOmega γ (a / Real.sqrt 3) 3 = 3 * γ / (2 * Real.pi * a ^ 2)
```

At `N = 3` and `R = a/√3` the ring rate is exactly the Lagrange rate of the parent monograph, `3Γ/(2πa²)` — the cross-link to the equilateral triangle.

### `ring_rotation_rate_pos`

```lean
theorem ring_rotation_rate_pos {γ R : ℝ} (hγ : 0 < γ) {N : ℕ} (hN : 2 ≤ N) (hR : 0 < R) : 0 < ringOmega γ R N
```

The ring rotates forward for forward circulation.


## §2 — Theorem B: the admissibility threshold of the pulsating ansatz  (9 declarations)

### `eps`

```lean
noncomputable def eps (C : ℝ) : ℝ
```

The pulsation depth of the Chaplygin ansatz.

### `rClosed`

```lean
noncomputable def rClosed (C ω : ℝ) (N : ℕ) (t : ℝ) (k : ℕ) : ℝ
```

The pulsating radius of the ansatz at vertex `k` (the phase is common to all vertices).

### `thetaClosed`

```lean
noncomputable def thetaClosed (ω : ℝ) (t : ℝ) (k : ℕ) : ℝ
```

The angular phase of the ansatz.

### `eps_pos`

```lean
theorem eps_pos (hC : 0 < C) : 0 < eps C
```

On the physical branch `C > 0` the depth is strictly positive.

### `eps_lt_one_iff`

```lean
theorem eps_lt_one_iff (hC : 0 < C) : eps C < 1 ↔ Real.pi * Real.log 2 < C
```

The depth is below one exactly above the Chaplygin threshold `π·ln 2`.

### `eps_at_threshold`

```lean
theorem eps_at_threshold : eps (Real.pi * Real.log 2) = 1
```

The threshold value of the depth is exactly one.

### `rClosed_min`

```lean
theorem rClosed_min (hC : 0 < C) (t : ℝ) (k : ℕ) : (1 - eps C) * Real.sqrt C ≤ rClosed C ω N t k
```

Away from the threshold every radius of the ansatz stays above `(1 − ε)·√C > 0`.

### `rClosed_pos_iff`

```lean
theorem rClosed_pos_iff (hC : 0 < C) (hω : ω ≠ 0) : (∀ (t : ℝ) (k : ℕ), 0 < rClosed C ω N t k) ↔ Real.pi * Real.log 2 < C
```

**Theorem B.** Every radius of the pulsating ansatz stays strictly positive exactly while `π·ln 2 < C`.

### `rClosed_touches_zero_at_threshold`

```lean
theorem rClosed_touches_zero_at_threshold (hω : ω ≠ 0) : ∃ t : ℝ, rClosed (Real.pi * Real.log 2) ω N t 0 = 0 ∧ ∀ t : ℝ, 0 ≤ rClosed (Real.pi * Real.log 2) ω N t 0
```

At the threshold `C = π ln 2` the pulsation touches zero once per period and stays nonnegative.


## §3 — Lemma C: no pulsating ring can ride the Kirchhoff field  (6 declarations)

### `radialForm`

```lean
noncomputable def radialForm (v z : ℂ) : ℝ
```

The radial component of a velocity at a point (up to the positive factor `|z|`; its vanishing is the exact `ṙ = 0` condition).

### `pulsPos`

```lean
noncomputable def pulsPos (r θ : ℝ → ℝ) (N : ℕ) (t : ℝ) (k : ℕ) : ℂ
```

The pulsating-ring kinematics at vertex `k`: common pulsation `r`, common rotation `θ`, canonical root phases.

### `ring_radial_zero`

```lean
theorem ring_radial_zero (γ : ℝ) (N : ℕ) (hN : 2 ≤ N) (R : ℝ) (hR : R ≠ 0) (ζ : ℂ) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) {k : ℕ} (hk : k < N) : radialForm (kirchhoff γ (ringPos R ζ) N k) (ringPos R ζ k) = 0
```

On the exact ring the radial velocity vanishes identically.

### `lemmaC_pulsation`

```lean
theorem lemmaC_pulsation {γ : ℝ} {N : ℕ} (hN : 2 ≤ N) {r θ : ℝ → ℝ} (hr : Differentiable ℝ r) (hθ : Differentiable ℝ θ) (hODE : ∀ t : ℝ, HasDerivAt (fun s => pulsPos r θ N s 0) (kirchhoff γ (fun k => pulsPos r θ N t k) N 0) t) (t : ℝ) : deriv r t = 0
```

**Lemma C (pulsation obstruction).** If the uniformly rotating pulsating configuration satisfies the point-vortex ODE at vertex `0`, its pulsation is stationary: `r' = 0`.

### `lemmaC_radius_constant`

```lean
theorem lemmaC_radius_constant {r : ℝ → ℝ} (hr : Differentiable ℝ r) (h0 : ∀ t : ℝ, deriv r t = 0) (s t : ℝ) : r s = r t
```

A stationary pulsation is a constant radius.

### `lemmaC_H1_reduction`

```lean
theorem lemmaC_H1_reduction {C ω : ℝ} (hC : 0 < C) (hω : ω ≠ 0) (hε : eps C ≠ 0) (hN : 2 ≤ N) : ¬ ∀ t : ℝ, HasDerivAt (fun s => pulsPos (fun u => rClosed C ω N u 0) (fun u => ω * u) N s 0) (kirchhoff γ (fun k => pulsPos (fun u => rClosed C ω N u 0) (fun u => ω * u) N t k) N 0) t
```

**Lemma C, corollary (H1 reduction).** A nontrivial Chaplygin pulsation of the pulsating-ring kinematics is not a Kirchhoff solution.


## §4 — Lemma D: the cycle-averaged Kirchhoff rate and the Poisson integral  (18 declarations)

### `pulsRadius`

```lean
noncomputable def pulsRadius (R ε ω t : ℝ) : ℝ
```

The pulsating radius of the symmetric H1 kinematics.

### `avgKinFreq`

```lean
noncomputable def avgKinFreq (γ R ε ω : ℝ) (N : ℕ) : ℝ
```

The cycle-averaged Kirchhoff rate over one pulsation period (Lemma D).

### `ringOmega_smul_radius`

```lean
theorem ringOmega_smul_radius {γ R : ℝ} (_hR : R ≠ 0) {u : ℝ} (_hu : u ≠ 0) (N : ℕ) : ringOmega γ (R * u) N = ringOmega γ R N / u ^ 2
```

The ring rate scales as the inverse square of the radius.

### `lemmaD_omega_independent`

```lean
theorem lemmaD_omega_independent {γ R ε ω : ℝ} (hω : ω ≠ 0) (hR : R ≠ 0) (hε : ε ^ 2 < 1) (N : ℕ) : avgKinFreq γ R ε ω N = ringOmega γ R N * ((1 / (2 * Real.pi)) * ∫ φ in (0 : ℝ)..(2 * Real.pi), ((1 + ε * Real.cos φ) ^ 2)⁻¹)
```

**Lemma D, frequency independence.** The cycle average factors into the ring rate times an ε-only shape factor.

### `private` `abs_lt_one_of_sq_lt_one`

```lean
private theorem abs_lt_one_of_sq_lt_one {ε : ℝ} (hε : ε ^ 2 < 1) : |ε| < 1
```

A nonnegative square below one has a root below one.

### `private` `sqrt_pos'`

```lean
private theorem sqrt_pos' {a : ℝ} (h : 0 < a) : 0 < Real.sqrt a
```

A positive real has a positive square root.

### `poissonG`

```lean
noncomputable def poissonG (ε φ : ℝ) : ℝ
```

The half-angle form of the Poisson antiderivative.

### `private` `cos_half_tan`

```lean
private theorem cos_half_tan {φ : ℝ} (hφ : φ ∈ Set.Ioo (-(Real.pi)) Real.pi) : Real.cos φ = (1 - Real.tan (φ / 2) ^ 2) / (1 + Real.tan (φ / 2) ^ 2)
```

The half-angle identity for the cosine.

### `private` `one_add_eps_cos_ne_zero`

```lean
private theorem one_add_eps_cos_ne_zero {ε : ℝ} (hε : ε ^ 2 < 1) (φ : ℝ) : (1 + ε * Real.cos φ) ≠ 0
```

The Poisson denominator never vanishes for `ε² < 1`.

### `private` `poisson_cont`

```lean
private theorem poisson_cont {ε : ℝ} (hε : ε ^ 2 < 1) : Continuous fun φ : ℝ => 1 / (1 + ε * Real.cos φ)
```

The Poisson integrand is continuous.

### `private` `arctan_add_arctan_inv`

```lean
private theorem arctan_add_arctan_inv {k : ℝ} (hk : 0 < k) : Real.arctan k + Real.arctan (k⁻¹) = Real.pi / 2
```

The half-angle antiderivative pair: `arctan k + arctan(k⁻¹) = π/2`.

### `private` `hasDerivAt_poissonG`

```lean
private theorem hasDerivAt_poissonG {ε : ℝ} (hε : ε ^ 2 < 1) {φ : ℝ} (hφ : φ ∈ Set.Ioo (-(Real.pi)) Real.pi) : HasDerivAt (poissonG ε) (1 / (1 + ε * Real.cos φ)) φ
```

On `(-π, π)` the half-angle antiderivative differentiates to the Poisson integrand.

### `private` `poisson_ftc`

```lean
private theorem poisson_ftc {ε : ℝ} (hε : ε ^ 2 < 1) {b : ℝ} (hb : b < Real.pi) (hb0 : 0 ≤ b) : ∫ φ in (0 : ℝ)..b, 1 / (1 + ε * Real.cos φ) = poissonG ε b - poissonG ε 0
```

The closed FTC on `[0, b]` for `0 ≤ b < π`.

### `private` `sq_neg`

```lean
private theorem sq_neg (a : ℝ) : (-a) ^ 2 = a ^ 2
```

The square of a negated real equals the square.

### `private` `poisson_half`

```lean
private theorem poisson_half {ε : ℝ} (hε : ε ^ 2 < 1) : ∫ φ in (0 : ℝ)..Real.pi, 1 / (1 + ε * Real.cos φ) = Real.pi / Real.sqrt (1 - ε ^ 2)
```

The half-period Poisson integral over `[0, π]`.

### `poisson_integral`

```lean
theorem poisson_integral {ε : ℝ} (hε : ε ^ 2 < 1) : ∫ φ in (0 : ℝ)..(2 * Real.pi), 1 / (1 + ε * Real.cos φ) = 2 * Real.pi / Real.sqrt (1 - ε ^ 2)
```

**The Poisson integral.** `∫₀^{2π} dφ/(1+ε·cos φ) = 2π/√(1−ε²)`, proven in closed form by the half-angle antiderivative — no numerical quadrature.

### `poisson_sq`

```lean
theorem poisson_sq {ε : ℝ} (hε : ε ^ 2 < 1) : ∫ φ in (0 : ℝ)..(2 * Real.pi), ((1 + ε * Real.cos φ) ^ 2)⁻¹ = 2 * Real.pi / ((1 - ε ^ 2) * Real.sqrt (1 - ε ^ 2))
```

The squared companion of the Poisson integral, via the antiderivative `g = sin φ/(1+ε·cos φ)`: `∫ g' = 0` on the closed cycle.

### `lemmaD_bridge`

```lean
theorem lemmaD_bridge {γ R ε ω : ℝ} (hω : ω ≠ 0) (hR : R ≠ 0) (hε : ε ^ 2 < 1) (N : ℕ) : avgKinFreq γ R ε ω N = ringOmega γ R N / ((1 - ε ^ 2) * Real.sqrt (1 - ε ^ 2))
```

**Lemma D.** The cycle-averaged Kirchhoff rate of the symmetric pulsation equals `ω_N/((1−ε²)·√(1−ε²))` — independent of the pulsation frequency.


## §5 — Theorem E (statement layer): the co-rotating linearization and W4  (6 declarations)

### `corotatingField`

```lean
noncomputable def corotatingField (γ ω : ℝ) (z : ℕ → ℂ) (N : ℕ) (k : ℕ) : ℂ
```

The co-rotating Kirchhoff field at angular rate `ω`.

### `ring_fixed_point`

```lean
theorem ring_fixed_point (γ R : ℝ) (ζ : ℂ) (hN : 2 ≤ N) (hR : R ≠ 0) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) {k : ℕ} (hk : k < N) : corotatingField γ (ringOmega γ R N) (ringPos R ζ) N k = 0
```

The ring is a fixed point of the co-rotating field at the Theorem-A rate.

### `ring_corotating_constant`

```lean
theorem ring_corotating_constant (γ R : ℝ) (ζ : ℂ) (hN : 2 ≤ N) (hR : R ≠ 0) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) {k : ℕ} (hk : k < N) : ∀ t : ℝ, corotatingField γ (ringOmega γ R N) (ringOrbit R ζ (ringOmega γ R N) t) N k = 0
```

The co-rotating field vanishes identically along the rotating orbit — the exact source of the W4 noise-floor degeneracy.

### `eigenvalueOf`

```lean
def eigenvalueOf (L : (ℕ → ℂ) → ℕ → ℂ) (ℓ : ℂ) : Prop
```

`λ` is a spectral value of an ℝ-linear perturbation layer.

### `spectrallyStable`

```lean
def spectrallyStable (γ ω R : ℝ) (N : ℕ) (ζ : ℂ) : Prop
```

The W4 spectral-stability criterion: every spectral value of the co-rotating linearization at the ring has nonpositive real part.

### `havelockClassification`

```lean
def havelockClassification : Prop
```

**Theorem E (milestone TW5, proven):** the Havelock classification — the regular `N`-gon ring (`N ≥ 3`) is Havelock-stable exactly while `N ≤ 7` (`havelockClassification`: every spectral value of the co-rotating linearization on the `N`-periodic pair layer is purely imaginary for `N ≤ 7` via `corotLin_dispersion`/`corotLin_stable7`, and the Havelock growing mode `λ = √(β² − Ω²) > 0` of `havelock_witness` appears for `N ≥ 8`). The parent monograph certifies it numerically; the present file contributes the exact statement layer together with the degeneracy certificates `ring_fixed_point`, `ring_corotating_constant` and the Theorem-A forcing theorem.


