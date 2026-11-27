# POLYVORTEX Lean 4 — complete declaration reference (the artifact's public API)

Every declaration of `Polyvortex.lean` (the TW1–TW5 artifact — 138 declarations) with its Lean docstring, in file order. Private helpers are marked; they are part of the seal surface and the 100% docstring ratchet. The sha256 of each theorem statement is sealed in `seal/manifest.json`.

SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0

## §0 — Private helpers  (12 declarations)

### `private `sum_range_shift_one`

```lean
private theorem sum_range_shift_one (f : ℕ → M) (n : ℕ) : ∑ m in Finset.range n, f (m + 1) = ∑ m in Finset.range n, f m + f n - f 0
```

Shifting the index of a `range`-sum by one.

### `private `sum_rot_shift`

```lean
private theorem sum_rot_shift (f : ℕ → M) (N : ℕ) : ∑ j in Finset.range N, f ((j + 1) % N) = ∑ j in Finset.range N, f j
```

The index translation `m ↦ (m + 1) % N` is summation-invariant.

### `private `sum_rot`

```lean
private theorem sum_rot (N : ℕ) : ∀ (c : ℕ) (f : ℕ → M), ∑ j in Finset.range N, f ((j + c) % N) = ∑ j in Finset.range N, f j
```

The index translation `m ↦ (m + c) % N` is summation-invariant.

### `private `sum_range_reflect_aux`

```lean
private theorem sum_range_reflect_aux (f : ℕ → M) : ∀ n : ℕ, ∑ m in Finset.range n, f ((n - 1) - m) = ∑ m in Finset.range n, f m
```

Reflecting the index of a `range`-sum, `m ↦ (n−1)−m`.

### `private `sum_erase_zero`

```lean
private theorem sum_erase_zero (f : ℕ → M) {N k : ℕ} (hk : k ∈ Finset.range N) : ∑ j in (Finset.range N).erase k, f j = ∑ j in Finset.range N, (if j = k then 0 else f j)
```

A single erased point contributes zero to the full `range`-sum.

### `private `conj_mul'`

```lean
private theorem conj_mul' (a b : ℂ) : star (a * b) = star a * star b
```

Complex conjugation is multiplicative (`star_mul'`).

### `private `conj_sub'`

```lean
private theorem conj_sub' (a b : ℂ) : star (a - b) = star a - star b
```

Complex conjugation is additive over differences.

### `private `conj_pow'`

```lean
private theorem conj_pow' (a : ℂ) : ∀ n : ℕ, star (a ^ n) = (star a) ^ n
```

Complex conjugation commutes with natural powers (`star_pow`).

### `private `conj_conj'`

```lean
private theorem conj_conj' (z : ℂ) : star (star z) = z
```

Double conjugation is the identity (`star_involutive`).

### `private `normSq_mul'`

```lean
private theorem normSq_mul' (a b : ℂ) : (Complex.normSq (a * b) : ℂ) = (Complex.normSq a : ℂ) * (Complex.normSq b : ℂ)
```

`normSq` of a product, as a `ℂ`-valued identity.

### `private `normSq_ofReal'`

```lean
private theorem normSq_ofReal' (r : ℝ) : (Complex.normSq ((r : ℂ)) : ℂ) = ((r * r : ℝ) : ℂ)
```

`normSq` of a real scalar, as a `ℂ`-valued identity.

### `private `normSq_ne_zero'`

```lean
private theorem normSq_ne_zero' {z : ℂ} (h : z ≠ 0) : Complex.normSq z ≠ 0
```

A nonzero complex number has nonzero `normSq`.

## §1 — Theorem A: the regular `N`-gon ring is an exact solution  (28 declarations)

### `noncomputable `rootExp`

```lean
noncomputable def rootExp (N : ℕ) : ℂ
```

The canonical primitive `N`-th root of unity `exp(2πi/N)`.

### `noncomputable `ringPos`

```lean
noncomputable def ringPos (R : ℝ) (ζ : ℂ) (k : ℕ) : ℂ
```

The `k`-th vertex of the regular `N`-gon ring of radius `R` with root `ζ`.

### `noncomputable `ringOmega`

```lean
noncomputable def ringOmega (γ : ℝ) (R : ℝ) (N : ℕ) : ℝ
```

The Kirchhoff angular rate of the regular `N`-gon ring of radius `R`.

### `noncomputable `kirchhoff`

```lean
noncomputable def kirchhoff (γ : ℝ) (z : ℕ → ℂ) (N : ℕ) (k : ℕ) : ℂ
```

The Kirchhoff point-vortex field: the velocity of vertex `k` induced by the other vertices of the configuration `z`.

### `private `mod_add_zero_eq`

```lean
private theorem mod_add_zero_eq {N j k : ℕ} (hj : j < N) (hk : k < N) (_hkle : k ≤ N) (h : (j + (N - k)) % N = 0) : j = k
```

If `(j + (N−k)) % N = 0` with `j, k < N` then `j = k`.

### `private `mod_self'`

```lean
private theorem mod_self' {N k : ℕ} (hkle : k ≤ N) : (k + (N - k)) % N = 0
```

`k + (N − k)` reduces to `0` modulo `N`.

### `private `mod_add_eq_self`

```lean
private theorem mod_add_eq_self {N k d : ℕ} (hk : k < N) (hd1 : 1 ≤ d) (hdN : d < N) (h : (k + d) % N = k) : False
```

If `(k + d) % N = k` then `d` is a positive multiple of `N`; with `1 ≤ d < N` this is absurd.

### `private `mul_pred_mod`

```lean
private theorem mul_pred_mod {N d : ℕ} (hd1 : 1 ≤ d) (hdN : d < N) : (d * (N - 1)) % N = (N - d) % N
```

For `1 ≤ d < N` the exponents `d·(N−1)` and `N−d` agree modulo `N`.

### `root_ne_zero`

```lean
theorem root_ne_zero {ζ : ℂ} {N : ℕ} (hN : N ≠ 0) (h1 : ζ ^ N = 1) : ζ ≠ 0
```

A nonzero exponent of a root of unity keeps the root nonzero.

### `private `normSq_pow'`

```lean
private theorem normSq_pow' (a : ℂ) : ∀ n : ℕ, (Complex.normSq (a ^ n) : ℂ) = (Complex.normSq a : ℂ) ^ n | 0 => by simp | n + 1 => by rw [pow_succ, pow_succ, normSq_mul', normSq_pow' a n] /-- For a nonnegative real `x`, `x ^ N = 1` with `N ≠ 0` forces `x = 1`. -/ private theorem real_pow_eq_one_of_nonneg {x : ℝ} (hx : 0 ≤ x) {N : ℕ} (hN : N ≠ 0) (h : x ^ N = 1) : x = 1
```

`normSq` of a natural power, as a `ℂ`-valued identity.

### `private `real_pow_eq_one_of_nonneg`

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

### `private `ring_term`

```lean
private theorem ring_term {R : ℝ} {ζ : ℂ} {N : ℕ} (hN : N ≠ 0) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (hR : R ≠ 0) {k j : ℕ} (hk : k < N) (hj : j < N) (hjk : j ≠ k) : Complex.I * (ringPos R ζ k - ringPos R ζ j) / ((Complex.normSq (ringPos R ζ k - ringPos R ζ j) : ℝ) : ℂ) = Complex.I / (R : ℂ) * ζ ^ k * (1 - ζ ^ (N - ((j + (N - k)) % N)))⁻¹
```

The pair velocity of the ring, in geometric form: the vertex pair at cyclic distance `d = (j + (N−k)) % N ∈ [1, N−1]` contributes `iζ^k/(R(1−ζ^{N−d}))`.

### `private `roots_pair_core`

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

### `noncomputable `ringOrbit`

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

### `noncomputable `eps`

```lean
noncomputable def eps (C : ℝ) : ℝ
```

The pulsation depth of the Chaplygin ansatz.

### `noncomputable `rClosed`

```lean
noncomputable def rClosed (C ω : ℝ) (N : ℕ) (t : ℝ) (k : ℕ) : ℝ
```

The pulsating radius of the ansatz at vertex `k` (the phase is common to all vertices).

### `noncomputable `thetaClosed`

```lean
noncomputable def thetaClosed (ω : ℝ) (t : ℝ) (k : ℕ) : ℝ
```

The angular phase of the ansatz.

### `eps_pos`

```lean
theorem eps_pos (C : ℝ) (hC : 0 < C) : 0 < eps C
```

On the physical branch `C > 0` the depth is strictly positive.

### `eps_lt_one_iff`

```lean
theorem eps_lt_one_iff (C : ℝ) (hC : 0 < C) : eps C < 1 ↔ Real.pi * Real.log 2 < C
```

The depth is below one exactly above the Chaplygin threshold `π·ln 2`.

### `eps_at_threshold`

```lean
theorem eps_at_threshold : eps (Real.pi * Real.log 2) = 1
```

The threshold value of the depth is exactly one.

### `rClosed_min`

```lean
theorem rClosed_min (C : ℝ) (hC : 0 < C) (t : ℝ) (k : ℕ) : (1 - eps C) * Real.sqrt C ≤ rClosed C ω N t k
```

Away from the threshold every radius of the ansatz stays above `(1 − ε)·√C > 0`.

### `rClosed_pos_iff`

```lean
theorem rClosed_pos_iff (C : ℝ) (hC : 0 < C) (hω : ω ≠ 0) : (∀ (t : ℝ) (k : ℕ), 0 < rClosed C ω N t k) ↔ Real.pi * Real.log 2 < C
```

**Theorem B.** Every radius of the pulsating ansatz stays strictly positive exactly while `π·ln 2 < C`.

### `rClosed_touches_zero_at_threshold`

```lean
theorem rClosed_touches_zero_at_threshold (hω : ω ≠ 0) : ∃ t : ℝ, rClosed (Real.pi * Real.log 2) ω N t 0 = 0 ∧ ∀ t : ℝ, 0 ≤ rClosed (Real.pi * Real.log 2) ω N t 0
```

At the threshold `C = π ln 2` the pulsation touches zero once per period and stays nonnegative.

## §3 — Lemma C: no pulsating ring can ride the Kirchhoff field  (6 declarations)

### `noncomputable `radialForm`

```lean
noncomputable def radialForm (v z : ℂ) : ℝ
```

The radial component of a velocity at a point (up to the positive factor `|z|`; its vanishing is the exact `ṙ = 0` condition).

### `noncomputable `pulsPos`

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

## §4 — Lemma D: the cycle-averaged Kirchhoff rate of the pulsation  (18 declarations)

### `noncomputable `pulsRadius`

```lean
noncomputable def pulsRadius (R ε ω t : ℝ) : ℝ
```

The pulsating radius of the symmetric H1 kinematics.

### `noncomputable `avgKinFreq`

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

### `private `abs_lt_one_of_sq_lt_one`

```lean
private theorem abs_lt_one_of_sq_lt_one {ε : ℝ} (hε : ε ^ 2 < 1) : |ε| < 1
```

A nonnegative square below one has a root below one.

### `private `sqrt_pos'`

```lean
private theorem sqrt_pos' {a : ℝ} (h : 0 < a) : 0 < Real.sqrt a
```

A positive real has a positive square root.

### `noncomputable `poissonG`

```lean
noncomputable def poissonG (ε φ : ℝ) : ℝ
```

The half-angle form of the Poisson antiderivative.

### `private `cos_half_tan`

```lean
private theorem cos_half_tan {φ : ℝ} (hφ : φ ∈ Set.Ioo (-(Real.pi)) Real.pi) : Real.cos φ = (1 - Real.tan (φ / 2) ^ 2) / (1 + Real.tan (φ / 2) ^ 2)
```

The half-angle identity for the cosine.

### `private `one_add_eps_cos_ne_zero`

```lean
private theorem one_add_eps_cos_ne_zero {ε : ℝ} (hε : ε ^ 2 < 1) (φ : ℝ) : (1 + ε * Real.cos φ) ≠ 0
```

The Poisson denominator never vanishes for `ε² < 1`.

### `private `poisson_cont`

```lean
private theorem poisson_cont {ε : ℝ} (hε : ε ^ 2 < 1) : Continuous fun φ : ℝ => 1 / (1 + ε * Real.cos φ)
```

The Poisson integrand is continuous.

### `private `arctan_add_arctan_inv`

```lean
private theorem arctan_add_arctan_inv {k : ℝ} (hk : 0 < k) : Real.arctan k + Real.arctan (k⁻¹) = Real.pi / 2
```

The half-angle antiderivative pair: `arctan k + arctan(k⁻¹) = π/2`.

### `private `hasDerivAt_poissonG`

```lean
private theorem hasDerivAt_poissonG {ε : ℝ} (hε : ε ^ 2 < 1) {φ : ℝ} (hφ : φ ∈ Set.Ioo (-(Real.pi)) Real.pi) : HasDerivAt (poissonG ε) (1 / (1 + ε * Real.cos φ)) φ
```

On `(-π, π)` the half-angle antiderivative differentiates to the Poisson integrand.

### `private `poisson_ftc`

```lean
private theorem poisson_ftc {ε : ℝ} (hε : ε ^ 2 < 1) {b : ℝ} (hb : b < Real.pi) (hb0 : 0 ≤ b) : ∫ φ in (0 : ℝ)..b, 1 / (1 + ε * Real.cos φ) = poissonG ε b - poissonG ε 0
```

The closed FTC on `[0, b]` for `0 ≤ b < π`.

### `private `sq_neg`

```lean
private theorem sq_neg (a : ℝ) : (-a) ^ 2 = a ^ 2
```

The square of a negated real equals the square.

### `private `poisson_half`

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

## §4′ — The spectral machinery of Theorem E (milestones TW2–TW5)  (60 declarations)

### `zinv`

```lean
def zinv (N : ℕ) (ζ : ℂ) (m : ℕ) : ℂ
```

The inverse exponent of `ζ ^ m` inside one period.

### `pow_congr_mod`

```lean
theorem pow_congr_mod {a b : ℕ} (hab : a % N = b % N) : ζ ^ a = ζ ^ b
```

Powers of a root of unity agree modulo the order.

### `zinv_mul`

```lean
theorem zinv_mul (m : ℕ) : zinv N ζ m * ζ ^ m = 1
```

`zinv N ζ m` is the multiplicative inverse of `ζ ^ m`.

### `private `normSq_pow_eq`

```lean
private theorem normSq_pow_eq (z : ℂ) : ∀ n : ℕ, Complex.normSq (z ^ n) = Complex.normSq z ^ n | 0 => by simp | n + 1 => by rw [pow_succ, pow_succ, Complex.normSq_mul, normSq_pow_eq z n] /-- Conjugate of a power of the root is the inverse power. -/ theorem star_zeta_pow (m : ℕ) : star (ζ ^ m) = zinv N ζ m
```

Norm-squares of powers distribute over the exponent.

### `star_zeta_pow`

```lean
theorem star_zeta_pow (m : ℕ) : star (ζ ^ m) = zinv N ζ m
```

Conjugate of a power of the root is the inverse power.

### `mul_one_sub_sum_range`

```lean
theorem mul_one_sub_sum_range (w : ℂ) : ∀ n : ℕ, (1 - w) * ∑ k in Finset.range n, w ^ k = 1 - w ^ n | 0 => by simp | n + 1 => by rw [Finset.sum_range_succ, mul_add, mul_one_sub_sum_range w n, sub_mul, one_mul, pow_succ] ring end Fourier section Fourier2 variable {N : ℕ} {ζ : ℂ} variable (hN : N ≠ 0) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (hunit : Complex.normSq ζ = 1) /-- Key modular arithmetic: `(N − m % N) % N + m ≡ 0 [MOD N]`. -/ private theorem key_mod_eq (m : ℕ) : ((N - m % N) % N + m) % N = 0
```

Telescoping identity for finite geometric sums.

### `private `key_mod_eq`

```lean
private theorem key_mod_eq (m : ℕ) : ((N - m % N) % N + m) % N = 0
```

Key modular arithmetic: `(N − m % N) % N + m ≡ 0 [MOD N]`.

### `zinv_mul_zeta_pow`

```lean
theorem zinv_mul_zeta_pow (a b c : ℕ) : zinv N ζ (a * b) * ζ ^ (c * b) = ζ ^ (((c % N + N - a % N) % N) * b)
```

The index-shift congruence behind the Fourier orthogonality.

### `sum_zeta_range`

```lean
theorem sum_zeta_range (j : ℕ) : ∑ k in Finset.range N, ζ ^ (j * k) = if j % N = 0 then (N : ℂ) else 0
```

The finite geometric sum over a full period.

### `fourier_orth`

```lean
theorem fourier_orth (n m : ℕ) : ∑ k in Finset.range N, star (ζ ^ (n * k)) * ζ ^ (m * k) = if (m % N) = (n % N) then (N : ℂ) else 0
```

Fourier orthogonality over a full period.

### `noncomputable `fmode`

```lean
noncomputable def fmode (u : ℕ → ℂ) (n : ℕ) : ℂ
```

The `n`-th Fourier mode amplitude of a configuration.

### `fmode_inversion`

```lean
theorem fmode_inversion (u : ℕ → ℂ) (hper : ∀ k, u k = u (k % N)) (k : ℕ) : u k = (1 / (N : ℂ)) * ∑ n in Finset.range N, fmode (N := N) (ζ := ζ) u n * ζ ^ (n * k)
```

Fourier inversion for `N`-periodic configurations.

### `havSig`

```lean
def havSig (N n : ℕ) : ℕ
```

The Havelock mode-coupling index `σ n = (2 − n) mod N` — the involution pairing Fourier modes of the ring linearization.

### `private `two_add_mod`

```lean
private theorem two_add_mod (N : ℕ) (hN3 : 3 ≤ N) : (2 + N) % N = 2
```

`(2 + N) % N = 2` for `3 ≤ N`.

### `private `one_add_mod`

```lean
private theorem one_add_mod (N : ℕ) (hN2 : 2 ≤ N) : (N + 1) % N = 1
```

`(N + 1) % N = 1` for `2 ≤ N`.

### `havSig_inv`

```lean
theorem havSig_inv (N : ℕ) (hN3 : 3 ≤ N) (n : ℕ) (hn : n < N) : havSig N (havSig N n) = n
```

The Havelock involution is an involution on mode indices: `σ(σ n) = n` for `n < N`.

### `noncomputable `havS`

```lean
noncomputable def havS (N : ℕ) (ζ : ℂ) (m : ℕ) : ℂ
```

The Havelock block sum `S_m = ∑_{d=1}^{N−1} (1 − ζ^{md})/(1 − ζ^d)²` — the per-mode coupling strength of the ring linearization.

### `noncomputable `havC`

```lean
noncomputable def havC (N : ℕ) (ζ : ℂ) (t : ℕ) : ℂ
```

The partial Havelock sum `C_t = ∑_{d=1}^{N−1} ζ^{td}/(1 − ζ^d)`; `S_m` telescopes through the `C_t`.

### `private `sum_Ico1`

```lean
private theorem sum_Ico1 {f : ℕ → ℂ} : ∑ d in Finset.Ico 1 N, f d = ∑ m in Finset.range (N - 1), f (m + 1)
```

`Ico 1 N`-sums reindex as `range (N−1)`-sums.

### `private `castReal_sub`

```lean
private theorem castReal_sub {a b : ℕ} (h : b ≤ a) : (((a - b : ℕ) : ℝ) : ℂ) = (((a : ℕ) : ℝ) : ℂ) - (((b : ℕ) : ℝ) : ℂ)
```

The ℕ→ℝ→ℂ cast respects bounded subtraction.

### `havC_zero`

```lean
theorem havC_zero (_hN2 : 2 ≤ N) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) : havC N ζ 0 = (((N - 1 : ℕ) : ℝ) : ℂ) / 2
```

`C_0 = (N−1)/2` — the roots-of-unity half-sum.

### `havC_one`

```lean
theorem havC_one (hN2 : 2 ≤ N) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) : havC N ζ 1 = -((N - 1 : ℕ) : ℂ) / 2
```

`C_1 = −(N−1)/2`.

### `private `sum_range_zero_Ico`

```lean
private theorem sum_range_zero_Ico {f : ℕ → ℂ} (hN1 : 1 ≤ N) : ∑ k in Finset.range N, f k = f 0 + ∑ d in Finset.Ico 1 N, f d
```

`range N` splits into the `{0}`-term and the `Ico 1 N`-sum.

### `havC_step`

```lean
theorem havC_step (hN2 : 2 ≤ N) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (t : ℕ) (ht2 : 2 ≤ t) (htN : t ≤ N - 1) : havC N ζ t = havC N ζ (t - 1) + 1
```

`C_t = C_{t−1} + 1` for `2 ≤ t ≤ N−1`.

### `havC_chain`

```lean
theorem havC_chain (hN2 : 2 ≤ N) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) : ∀ m, 1 ≤ m → m ≤ N - 1 → havC N ζ m = -((N - 1 : ℕ) : ℂ) / 2 + ((m - 1 : ℕ) : ℂ)
```

`C_m = −(N−1)/2 + (m−1)` for `1 ≤ m ≤ N−1`.

### `havS_zero`

```lean
theorem havS_zero (N : ℕ) (ζ : ℂ) : havS N ζ 0 = 0
```

`S_0 = 0`.

### `havS_step`

```lean
theorem havS_step (_hN2 : 2 ≤ N) (_h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (m : ℕ) (_hmN : m + 1 ≤ N - 1) : havS N ζ (m + 1) = havS N ζ m + havC N ζ m
```

`S_{m+1} = S_m + C_m` for `m+1 ≤ N−1`.

### `havS_closed`

```lean
theorem havS_closed (hN2 : 2 ≤ N) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) : ∀ m, 1 ≤ m → m ≤ N - 1 → havS N ζ m = (2 - ((m : ℕ) : ℂ)) * (((N : ℕ) : ℂ) - ((m : ℕ) : ℂ)) / 2
```

**The closed form:** `S_m = (2−m)(N−m)/2` for `1 ≤ m ≤ N−1` (and `S_0 = 0`).

### `havS_sym`

```lean
theorem havS_sym (hN2 : 2 ≤ N) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (n : ℕ) : havS N ζ (havSig N n) = havS N ζ (n % N)
```

`S` is invariant under the mode involution: `S_{σ n} = S_{n mod N}`.

### `private `int_prod_bound`

```lean
private theorem int_prod_bound (N k l : ℕ) (hN7 : N ≤ 7) (hsum : k + l = N - 2) : k * l ≤ N - 1
```

Integer threshold estimate: for `k + l = N − 2 ≤ 5` the product `k * l` does not exceed `N − 1` — the exact arithmetic behind the Havelock `N = 8` threshold.

### `havS_real_sq`

```lean
theorem havS_real_sq (hN2 : 2 ≤ N) (hN7 : N ≤ 7) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (m : ℕ) (hm : m < N) : ∃ r : ℝ, havS N ζ m * star (havS N ζ m) = ((r ^ 2 : ℝ) : ℂ) ∧ r ^ 2 ≤ (((N - 1 : ℕ) : ℝ) / 2) ^ 2
```

**The threshold bound.** For `N ≤ 7` every block sum of a primitive root is real with square controlled by the Kirchhoff window: `S_m · conj S_m = r²` with `r² ≤ ((N−1)/2)²` (equality `r = (N−1)/2` at `m = 1`).

### `noncomputable `corotLin`

```lean
noncomputable def corotLin (γ R : ℝ) (N : ℕ) (ζ : ℂ) (u : ℕ → ℂ) (k : ℕ) : ℂ
```

The linearization of the co-rotating Kirchhoff field at the regular ring: the first-order Havelock layer `u ↦ D(k)(u)` in co-rotating coordinates.

### `private `ringPos_eq`

```lean
private theorem ringPos_eq (R : ℝ) (ζ : ℂ) (k : ℕ) : ringPos R ζ k = (R : ℂ) * ζ ^ k
```

`ringPos` unfolds to the radius times the power of the root.

### `private `starI'`

```lean
private theorem starI' : star Complex.I = -Complex.I
```

`star` is conjugation on the ring constants.

### `private `starR'`

```lean
private theorem starR' (r : ℝ) : star (r : ℂ) = (r : ℂ)
```

`star` fixes the real scalars inside `ℂ`.

### `private `star_CR`

```lean
private theorem star_CR (R : ℝ) : star (Complex.I * (R : ℂ)) = -(Complex.I * (R : ℂ))
```

Conjugation anticommutes `i` past a real scalar.

### `corotLin_periodic`

```lean
theorem corotLin_periodic (γ R : ℝ) (N : ℕ) (ζ : ℂ) (h1 : ζ ^ N = 1) (u : ℕ → ℂ) (hper : ∀ k, u k = u (k % N)) (k : ℕ) : corotLin γ R N ζ u (k + N) = corotLin γ R N ζ u k
```

`corotLin` preserves `N`-periodicity.

### `corotLin_add`

```lean
theorem corotLin_add (γ R : ℝ) (N : ℕ) (ζ : ℂ) (u v : ℕ → ℂ) (k : ℕ) : corotLin γ R N ζ (u + v) k = corotLin γ R N ζ u k + corotLin γ R N ζ v k
```

`corotLin` is additive.

### `private `hnegI`

```lean
private theorem hnegI : (-Complex.I) * Complex.I = 1
```

The two factors of `i` cancel: `(-i) * i = 1`.

### `private `imul_neg_I`

```lean
private theorem imul_neg_I (x : ℂ) : Complex.I * (-(Complex.I * x)) = x
```

The product `i·(−i·x)` collapses back to `x`.

### `corotLin_orbit_kernel`

```lean
theorem corotLin_orbit_kernel (γ R : ℝ) (N : ℕ) (hN : 2 ≤ N) (ζ : ℂ) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (hunit : Complex.normSq ζ = 1) (k : ℕ) : corotLin γ R N ζ (fun j => Complex.I * ringPos R ζ j) k = 0
```

**TW3 (kernel certificate).** The orbit direction `i·ringPos` lies in the kernel of the ring linearization — the exact linear source of the W4 noise-floor degeneracy (the doubled zero eigenvalue).

### `private `mod_shift_add`

```lean
private theorem mod_shift_add (N d k : ℕ) (hdN : d ≤ N) (hk : k < N) : ((k + N - d) % N + d) % N = k
```

Adding `d` after the shift-reversal returns the original index.

### `private `mod_shift_sub`

```lean
private theorem mod_shift_sub (N d j : ℕ) (hdN : d ≤ N) (hj : j < N) : ((j + d) % N + N - d) % N = j
```

Adding `N - d` after the forward shift returns the original index.

### `private `sum_range_shift`

```lean
private theorem sum_range_shift (hN : N ≠ 0) (d : ℕ) (hd : d < N) {F : ℕ → ℂ} : ∑ k in Finset.range N, F ((k + N - d) % N) = ∑ j in Finset.range N, F j
```

Summation over `range N` is invariant under the shift-reversal `k ↦ (k + N - d) % N` for `d < N`.

### `zeta_havSig_apply`

```lean
theorem zeta_havSig_apply (hN3 : 3 ≤ N) (h1 : ζ ^ N = 1) (hunit : Complex.normSq ζ = 1) (n j : ℕ) : (ζ : ℂ) ^ (2 * j) * star (ζ ^ (n * j)) = ζ ^ (havSig N n * j)
```

The co-rotating weight identity: `ζ^{2j}·conj(ζ^{n·j}) = ζ^{σ(n)·j}` with `σ(n) = havSig N n`.

### `star_fmode`

```lean
theorem star_fmode (u : ℕ → ℂ) (m : ℕ) : star (@fmode N ζ u m) = ∑ k in Finset.range N, star (u k) * ζ ^ (m * k)
```

Conjugation of a Fourier coefficient swaps the weight to the other side.

### `corotLin_proj`

```lean
theorem corotLin_proj (γ R : ℝ) (hN3 : 3 ≤ N) (ζ : ℂ) (h1 : ζ ^ N = 1) (hunit : Complex.normSq ζ = 1) (u : ℕ → ℂ) (n : ℕ) : ∑ k in Finset.range N, corotLin γ R N ζ u k * star (ζ ^ (n * k)) = -Complex.I * ((ringOmega γ R N : ℝ) : ℂ) * @fmode N ζ u n - Complex.I * ((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ) * (havS N ζ (havSig N n) * star (∑ j in Finset.range N, u j * star (ζ ^ (havSig N n * j))))
```

**TW4 (master projection lemma).** For any configuration `u`, the mode-`n` Fourier coefficient of the linearized co-rotating field depends only on the mode coefficients `fmode u n` and `fmode u (havSig N n)`: `D_n = -iΩ·C_n - i·(γ/2πR²)·S_{σ(n)}·conj(C_{σ(n)})`.

### `fmode_add`

```lean
theorem fmode_add (c d : ℂ) (u v : ℕ → ℂ) (n : ℕ) : @fmode N ζ (fun k => c * u k + d * v k) n = c * @fmode N ζ u n + d * @fmode N ζ v n
```

The Fourier coefficients are ℂ-linear in the configuration (add form).

### `fmode_linearity`

```lean
theorem fmode_linearity (a b : ℂ) (u v : ℕ → ℂ) (n : ℕ) : @fmode N ζ (fun k => a * u k - b * v k) n = a * @fmode N ζ u n - b * @fmode N ζ v n
```

The Fourier coefficients are ℂ-linear in the configuration (subtract form).

### `corotLin_pair_system`

```lean
theorem corotLin_pair_system (γ R : ℝ) (hN3 : 3 ≤ N) (ζ : ℂ) (h1 : ζ ^ N = 1) (hunit : Complex.normSq ζ = 1) (u v : ℕ → ℂ) (a b : ℂ) (hu : ∀ k, corotLin γ R N ζ u k = a * u k - b * v k) (hv : ∀ k, corotLin γ R N ζ v k = b * u k + a * v k) (n : ℕ) : (a + Complex.I * ((ringOmega γ R N : ℝ) : ℂ)) * @fmode N ζ u n - b * @fmode N ζ v n = -Complex.I * (((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ) * havS N ζ (havSig N n)) * star (∑ j in Finset.range N, u j * star (ζ ^ (havSig N n * j))) ∧ (a + Complex.I * ((ringOmega γ R N : ℝ) : ℂ)) * @fmode N ζ v n + b * @fmode N ζ u n = -Complex.I * (((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ) * havS N ζ (havSig N n)) * star (∑ j in Finset.range N, v j * star (ζ ^ (havSig N n * j)))
```

**TW4 (the mode system).** For a spectral pair `(u, v)` of the co-rotating linearization with eigenvalue `ℓ = a + i·b`, the Fourier coefficients satisfy, for every mode `n`, the rotated pair system `(a+iΩ)·C_n − b·D_n = −i·β_n·conj(C_{σn})`, `b·C_n + (a+iΩ)·D_n = −i·β_n·conj(D_{σn})` with `β_n := (γ/2πR²)·havS N ζ n` and `σn := havSig N n`.

### `corotLin_dispersion`

```lean
theorem corotLin_dispersion (γ R : ℝ) (hN3 : 3 ≤ N) (ζ : ℂ) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (hunit : Complex.normSq ζ = 1) (u v : ℕ → ℂ) (a b : ℝ) (hu : ∀ k, corotLin γ R N ζ u k = ((a : ℂ)) * u k - ((b : ℂ)) * v k) (hv : ∀ k, corotLin γ R N ζ v k = ((b : ℂ)) * u k + ((a : ℂ)) * v k) (n₀ : ℕ) (hn₀ : n₀ < N) (hP : @fmode N ζ u n₀ + Complex.I * @fmode N ζ v n₀ ≠ 0 ∨ @fmode N ζ u n₀ - Complex.I * @fmode N ζ v n₀ ≠ 0) : ((a : ℂ) + Complex.I * (b : ℂ)) ^ 2 + ((ringOmega γ R N : ℝ) : ℂ) ^ 2 = ((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ) * havS N ζ n₀ * star (((γ / (2 * Real.pi * R ^ 2) : ℝ) : ℂ) * havS N ζ n₀)
```

**The Havelock dispersion relation (TW5).** For a spectral pair `(u, v)` with eigenvalue `ℓ = a + i·b` of the co-rotating linearization, any mode `n₀ < N` carrying a nonzero complex amplitude obeys `ℓ² + Ω² = β · conj β` with `β = (γ/2πR²)·S_{n₀}`.

### `corotLin_stable7`

```lean
theorem corotLin_stable7 (γ R : ℝ) (hN3 : 3 ≤ N) (hN7 : N ≤ 7) (ζ : ℂ) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (hunit : Complex.normSq ζ = 1) (u v : ℕ → ℂ) (hper_u : ∀ k, u k = u (k % N)) (hper_v : ∀ k, v k = v (k % N)) (a b : ℝ) (hu : ∀ k, corotLin γ R N ζ u k = ((a : ℂ)) * u k - ((b : ℂ)) * v k) (hv : ∀ k, corotLin γ R N ζ v k = ((b : ℂ)) * u k + ((a : ℂ)) * v k) (huv : ∃ k, u k ≠ 0 ∨ v k ≠ 0) : a = 0
```

**The Havelock small-ring stability (TW5).** For `N ≤ 7` every eigenvalue `ℓ = a + i·b` of the co-rotating linearization on nonzero spectral pairs is purely imaginary: `a = 0` — a ring of at most seven point vortices supports no growing co-rotating perturbation.

### `eigenvalueOf'`

```lean
def eigenvalueOf' (γ R : ℝ) (N : ℕ) (ζ : ℂ) (ℓ : ℂ) : Prop
```

Spectral value of the `N`-periodic pair layer: `ℓ = a + i·b` acts on a pair `(u, v)` of `N`-periodic configurations, not both identically zero, through the ℝ-linear rotation `u ↦ a·u − b·v`, `v ↦ b·u + a·v`.

### `havelockStable`

```lean
def havelockStable (γ R : ℝ) (N : ℕ) (ζ : ℂ) : Prop
```

**Havelock stability (TW5):** every spectral value of the `N`-periodic pair layer of the co-rotating linearization has nonpositive real part.

### `private `corotLin_zero`

```lean
private theorem corotLin_zero (γ R : ℝ) (N : ℕ) (ζ : ℂ) (k : ℕ) : corotLin γ R N ζ (fun _ => (0:ℂ)) k = 0
```

`corotLin` annihilates the zero configuration.

### `havelockStable_small`

```lean
theorem havelockStable_small (γ R : ℝ) (hN3 : 3 ≤ N) (hN7 : N ≤ 7) (ζ : ℂ) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (hunit : Complex.normSq ζ = 1) : havelockStable γ R N ζ
```

**TW5 (small-ring stability).** For `3 ≤ N ≤ 7` the co-rotating linearization of the regular ring is Havelock-stable.

### `private `zeta_zinv_pow`

```lean
private theorem zeta_zinv_pow (hN : N ≠ 0) (h1 : ζ ^ N = 1) (a c k : ℕ) : ζ ^ (c * k) * zinv N ζ (a * k) = ζ ^ (((c % N + N - a % N) % N) * k)
```

Swapped form of `zinv_mul_zeta_pow`: `ζ^{c·k}·zinv(a·k) = ζ^{((c % N + N − a % N) % N)·k}`.

### `private `zinv_shift`

```lean
private theorem zinv_shift (hN : N ≠ 0) (h1 : ζ ^ N = 1) (j k d : ℕ) (hdN : d < N) : zinv N ζ (j * ((k + N - d) % N)) = zinv N ζ (j * k) * ζ ^ (j * d)
```

The per-`d` index-shift identity behind the Havelock witness: `zinv(j·((k + N − d) % N)) = zinv(j·k)·ζ^{j·d}`.

### `havelock_witness`

```lean
theorem havelock_witness (γ R : ℝ) (hN8 : 8 ≤ N) (hR : R ≠ 0) (hγ : 0 < γ) (ζ : ℂ) (h1 : ζ ^ N = 1) (hprim : ∀ m ∈ Finset.Ico 1 N, ζ ^ m ≠ 1) (hunit : Complex.normSq ζ = 1) : ∃ ℓ : ℂ, eigenvalueOf' γ R N ζ ℓ ∧ 0 < ℓ.re
```

**TW5 (the Havelock instability, witness).** For `N ≥ 8` (with `γ > 0`, `R ≠ 0`) the co-rotating linearization of the regular `N`-gon ring admits a spectral value with strictly positive real part: the Havelock growing mode.

### `rootExp_unit`

```lean
theorem rootExp_unit : Complex.normSq (rootExp N) = 1
```

The canonical root lies on the unit circle.

## §5 — Theorem E: the co-rotating linearization and the Havelock classification  (5 declarations)

### `noncomputable `corotatingField`

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

### `havelockClassification`

```lean
theorem havelockClassification (γ R : ℝ) (hN3 : 3 ≤ N) (hR : R ≠ 0) (hγ : 0 < γ) : havelockStable γ R N (rootExp N) ↔ N ≤ 7
```

**Theorem E (milestone TW5, proven):** the Havelock classification — the regular `N`-gon ring (`N ≥ 3`) is Havelock-stable exactly while `N ≤ 7`. The stability half is `havelockStable_small` (via `corotLin_dispersion` and `corotLin_stable7`: the dispersion relation forces `ℓ² + Ω² = β·conj β` with `|β| ≤ Ω` for `N ≤ 7`); the instability half is `havelock_witness` (the Havelock growing mode `λ = √(β² − Ω²) > 0` at the mode pair `n₀ = N − 3`, `m = 5`).
