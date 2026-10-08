# CYCLORING: Gamma-periods, the defect chain, and the synchronous breathing of a vortex ring

## A self-contained numerical-analytical study

---

## 1. Setting: from the rigid ring to the periodic modulation

The regular N-gon of equal point vortices is the most economical laboratory of collective vortex motion. The configuration is specified by one radius and one angle: the vortices occupy the vertices of a polygon and rotate as a whole at a constant angular rate. The entire kinematics here is algebraic in nature: the angular positions are the roots of unity $\zeta_N^k = e^{2\pi i k/N}$, and any relation between the vortices reduces to the arithmetic of the cyclotomic lattice. The present study takes this observation to its conclusion: we show that not only the angular but also the radial dynamics of the ring can be read off a finite set of transcendental constants — the Gamma-periods of the level.

The program splits into four registers. The first register is the algebraization: the ring is the root system of a single binomial $z^N = \sigma(t)$, and every instantaneous relation between the vortices is expressed by the roots-of-unity filter. The second register is the periodic one: for the level N we introduce the functional $\Omega_{a,b} = \Gamma(a/N)\Gamma(b/N)/\Gamma((a+b)/N)$, its boundary turns out to be algebraic, and its diagonal sums produce the period witness $W_N$. The third register is the defect chain: from the triple $(N, B, \lambda_0)$ a finite chain $\delta \to \gamma \to \delta_{eff} \to \Delta_{Ch}$ is built, which converts the periods of the level into the amplitude and the frequency of the modulation. The fourth register is dynamical: the synchronous breathing at the transducer-prescribed frequency closes exactly, and every rosette returns to its start after $T_c = 2\pi/\nu$.

All statements of the program split into two sorts. Theorems 1–5, proved here, are clean statements: the binomial identity, the roots-of-unity filter, the algebraicity of the boundary, the mean-transport identity, the closed form of the Hamiltonian. Each carries a full proof and a numerical certificate from the ladder W1–W7. The numerical laws — for instance the stiffness power law $\Delta_{Ch}(N)$ — are reported honestly as numerical approximations with their scan range. This standard — "a theorem with a proof plus a protocol with a tolerance" — is maintained throughout.

## 2. The model and the basic objects

Point vortices with circulations $\Gamma_k$ in the complex plane obey

$$
\frac{d\bar z_k}{dt} = \frac{1}{2\pi i}\sum_{j \neq k} \frac{\Gamma_j}{z_k - z_j}, \qquad k = 0, \ldots, N-1,
$$

with the classical integrals — the Hamiltonian, the impulse and the moment:

$$
H = -\frac{1}{2\pi}\sum_{i<j} \Gamma_i \Gamma_j \ln |z_i - z_j|, \qquad L = \sum_k \Gamma_k z_k, \qquad I = \sum_k \Gamma_k |z_k|^2.
$$

We work in the natural units $\Gamma = R_0 = 1$, where $R_0$ is the base radius of the ring. The rigid ring is the configuration $z_k = R\zeta_N^k$; the key elementary fact about it is the pair cancellation. For a pair of vertices $z_k - z_j = Re^{i\theta_k}(1 - e^{i(\theta_j - \theta_k)})$, and the sum over all neighbors splits into a real half and an antisymmetric cotangent tail:

$$
\sum_{j \neq k} \frac{1}{1 - e^{i(\theta_j - \theta_k)}} = \frac{N-1}{2}, \qquad \sum_{j \neq k} \cot\frac{\pi(j-k)}{N} = 0.
$$

Hence the rigid-rotation theorem: the frozen polygon rotates as a whole at

$$
\omega_L = \frac{\Gamma(N-1)}{4\pi R^2},
$$

and the radial velocity component of every vortex vanishes identically. This is an exact statement, not an approximation: it follows from the antisymmetry of the cotangent sum and is re-checked numerically at stage W4 with the relative error $1.1 \cdot 10^{-10}$ (RK4, two turns, N = 7). The consequence for the whole program: any breathing of the ring is a radial program the kinematical flow does not sustain by itself; the angular transport of the ring under an arbitrary radius program $r(t)$, however, follows the frozen law with the adiabatic invariant

$$
\Lambda_0 = \omega_L R^2 = \frac{\Gamma(N-1)}{4\pi},
$$

which is free of the radius. The invariance of the polygon in the flow and the supporting role of the radial drive are discussed in Section 6 and pinned in the honesty notes.

The level triple that launches the whole chain is now natural: $N$ is the order of the cyclotomic lattice, $B = N\Gamma R_0^2$ is the angular impulse of the frozen ring, $\lambda_0 = \Gamma(N-1)/(4\pi R_0^2)$ is its frozen frequency. Both are exact integral registers of the ring, and their product $B\lambda_0/\Gamma^2 = N(N-1)/(4\pi)$ is dimensionless.

## 3. Theorem 1 — the root system of the ring

The first register of the program is the complete algebraization of the configuration. Let

$$
z_k(t) = r(t)\,\zeta_N^k e^{i\nu t}, \qquad \zeta_N = e^{2\pi i/N}, \qquad k = 0, \ldots, N-1,
$$

be the kinematic program of the ring with the common radius $r(t)$ and the common angular rate $\nu$. The following theorem holds.

**Theorem 1 (root system).** For every time t the polynomial $F_t(z) = \prod_k (z - z_k(t))$ is the binomial

$$
F_t(z) = z^N - \sigma(t), \qquad \sigma(t) = r(t)^N e^{iN\nu t},
$$

that is, the ring is exactly the full set of roots of $z^N = \sigma(t)$. Moreover, the power sums satisfy the roots-of-unity filter $S_m(t) = \sum_k z_k^m = 0$ for $1 \leq m \leq N-1$ and $S_N(t) = N\sigma(t)$, the linear impulse $L = \Gamma\sum_k z_k$ vanishes identically, and the Galois group $\mathrm{Gal}(\mathbb{Q}(\zeta_N)/\mathbb{Q}) \cong (\mathbb{Z}/N)^\times$ acts on the ring by relabeling the vortices: $\sigma_a: \zeta_N^k \mapsto \zeta_N^{ak}$.

Proof. The set $\{r e^{i\nu t}\zeta_N^k\}$ is the full root set of the binomial $z^N = r^N e^{iN\nu t}$: the N-th power erases the factor $\zeta_N^k$ since $\zeta_N^{Nk} = 1$, and all N vortices land on the same value $\sigma(t) = r^N e^{iN\nu t}$. Since the binomial $z^N - \sigma$ has exactly N roots and all are listed, the identity $F_t(z) = z^N - \sigma(t)$ is proved. For the power sums expand $z_k^m = r^m e^{im\nu t}\zeta_N^{mk}$: the sum becomes the geometric sum $\sum_k \zeta_N^{mk}$, equal to N when $N \vert m$ and to zero otherwise; for $1 \leq m \leq N-1$ there is no divisibility, hence $S_m = 0$, and for $m = N$ every summand equals $r^N e^{iN\nu t}$, so $S_N = N\sigma$. The vanishing impulse is the case $m = 1$. Finally, the automorphism $\sigma_a$ of $\mathbb{Q}(\zeta_N)$ sends $\zeta_N^k \mapsto \zeta_N^{ak}$ for $\gcd(a, N) = 1$ and therefore permutes the roots of the binomial: the Galois action on the ring is exactly the vortex permutation $k \mapsto ak \ \mathrm{mod}\  N$. The theorem is proved. ∎

The practical corollary is the character decomposition of the deformations. Perturb the ring, $z_k = z_k^{(0)} + \eta_k$; the coefficients

$$
c_m = \frac{1}{N}\sum_k z_k \zeta_N^{-mk}
$$

are exactly the projections of the perturbation onto the characters of the lattice $\mu_N$: the ideal ring populates only the master mode $m = 1$ ($c_1 = re^{i\nu t}$, the rest are zeros to $10^{-10}$ — a test register), and any deformation appears as the population of the senior modes. The roots-of-unity filter is the discrete Fourier transform on the cyclotomic lattice, and the entire "algebraization" of the first register is precisely it. The numerical certificate is stage W3: the binomial identity holds with the normalized residual $6.4 \cdot 10^{-11}$, the power sums with $2.9 \cdot 10^{-14}$, the impulse with $1.9 \cdot 10^{-15}$.

## 4. Theorem 2 — the periods of the level and the algebraic boundary

The second register introduces the periodic functional of the level. For integers $a, b \ge 1$ set

$$
\Omega_{a,b} = \frac{\Gamma(a/N)\,\Gamma(b/N)}{\Gamma((a+b)/N)}, \qquad P(a,b) = \frac{\Omega_{a,b}}{\Omega_{1,1}},
$$

call the normalized periods $P(a,b)$ the periodic coordinates of the pair $(a,b)$, and the period witness of the level —

$$
W_N = \sum_{a=1}^{N-1} P(a, a)
$$

— its diagonal sum. The functional is symmetric: $\Omega_{a,b} = \Omega_{b,a}$.

**Theorem 2 (the algebraic boundary).** For $1 \leq a \leq N-1$ the boundary period equals

$$
\Omega_{a, N-a} = \Gamma(a/N)\,\Gamma(1 - a/N) = \frac{\pi}{\sin(\pi a/N)},
$$

that is, it lies in $\pi \cdot \mathbb{Q}(\zeta_N)^\times$ — an algebraic multiple of π. Moreover, the sine product

$$
\prod_{m=1}^{N-1} 2\sin\frac{\pi m}{N} = N
$$

is exact, and therefore the product of all boundary periods equals $\pi^{N-1} 2^{N-1}/N$.

Proof. The reflection identity $\Gamma(z)\Gamma(1-z) = \pi/\sin(\pi z)$ at $z = a/N$ gives the first part immediately: the denominator $\Gamma(1)$ is one, and $\sin(\pi a/N)$ is an algebraic number generated by $\zeta_N$. For the sine product consider $\frac{z^N - 1}{z - 1} = \prod_{m=1}^{N-1}(z - \zeta_N^m)$ and substitute $z = 1$: the left side is N, the right side is $\prod_m (1 - \zeta_N^m)$. Passing to the moduli gives $\prod_m |1 - \zeta_N^m| = N$, and $|1 - e^{i\varphi}| = 2\sin(\varphi/2)$ completes the proof. The product of the boundary periods follows directly: $\prod_a \pi/\sin(\pi a/N) = \pi^{N-1} \cdot 2^{N-1}/N$. ∎

The dichotomy "the boundary is algebraic, the interior is Gamma-transcendental" is the main periodic fact of the program. At small levels the boundary values are elementary: $\Omega_{1,2} = 2\pi/\sqrt{3}$ at N = 3, $\Omega_{1,3} = \pi\sqrt{2}$ and $\Omega_{2,2} = \pi$ at N = 4, $\Omega_{3,3} = \pi$ at N = 6. The interior periods — for instance $P(2,2) \approx 0.411$ at N = 7 — admit no known algebraic reductions, and the program never consumes them as algebraic: the chain takes only the diagonal sums $W_N$ (as the numerical constants of the level) and the boundary values. The certificates are stages W1 and W2: the reflection identity holds with the residual $5.1 \cdot 10^{-49}$, the sine product with $5.1 \cdot 10^{-49}$ (mpmath, 50 working digits); the float versions of the registers hold $10^{-12}$.

## 5. Theorem 3 — the period transducer

The third register connects the two previous ones: the defect chain converts the arithmetic of the level into the modulation program of the ring. The input is the triple $(N, B, \lambda_0)$ of Section 2; the output is the triple $(\varepsilon, \nu, C_N)$: the amplitude, the frequency and the log-stiffness of the breathing.

**Theorem 3 (the transducer).** Set successively

$$
\delta = \frac{\pi}{N}, \qquad k = \left\lceil \frac{B\lambda_0}{\Gamma^2} \right\rceil, \qquad \gamma = \frac{\delta^4}{k}, \qquad \delta_{eff} = \frac{\delta^5}{k}, \qquad \Delta_{Ch} = \frac{\gamma\, W_N}{N-1}.
$$

Then the map

$$
\varepsilon = \frac{\Delta_{Ch}}{1 + \Delta_{Ch}}, \qquad \nu = \omega_L\,\frac{(1+\Delta_{Ch})^3}{(1+2\Delta_{Ch})^{3/2}}, \qquad C_N = \ln\!\left(1 + \frac{1}{\Delta_{Ch}}\right) = -\ln \varepsilon
$$

is well defined for $\Delta_{Ch} > 0$, bijective, and its frequency branch is identical to the synchronous law $\nu = \omega_L(1-\varepsilon^2)^{-3/2}$. Moreover: (i) $\gamma(N)$ strictly decreases in N from N = 4 on; (ii) the classical limit $\Delta_{Ch} \to 0$ gives $\varepsilon \to 0$, $\nu \to \omega_L$, $C_N \to \infty$ — the rigid ring.

Proof. Well-definedness: $\Delta_{Ch} > 0$ as a product of the positive $\gamma$ and $W_N$; the map $\varepsilon = \Delta/(1+\Delta)$ is a fractional-linear isomorphism $(0,\infty) \to (0,1)$ with the inverse $\Delta = \varepsilon/(1-\varepsilon)$. The branch identity: from $\varepsilon = \Delta/(1+\Delta)$ we get $1 - \varepsilon^2 = \frac{(1+\Delta)^2 - \Delta^2}{(1+\Delta)^2} = \frac{1+2\Delta}{(1+\Delta)^2}$, whence $(1-\varepsilon^2)^{-3/2} = \frac{(1+\Delta)^3}{(1+2\Delta)^{3/2}}$ — the frequency branches coincide. Monotonicity: $\delta^4 = \pi^4/N^4$ strictly decreases, while $k = \lceil N(N-1)/(4\pi)\rceil$ is non-decreasing and strictly increases for $N \ge 4$ (the step $2N/(4\pi) > 1$), hence $\gamma = \delta^4/k$ strictly decreases. The limit: as $\Delta \to 0$ the fractional-linear isomorphism gives $\varepsilon \to 0$, the expansion $(1-\varepsilon^2)^{-3/2} = 1 + \frac{3}{2}\varepsilon^2 + O(\varepsilon^4)$ gives $\nu \to \omega_L$, and $C_N = -\ln\varepsilon \to \infty$. ∎

The numerical shape of the transducer is pinned by stage W7; the registered table of the four levels is given in Section 8. On the scan range N = 3..30 the discriminant follows the power law $\Delta_{Ch}(N) \approx 1.7 \cdot 10^{3} \cdot N^{-6.7}$ — a numerical approximation, not an asymptotic theorem; only the monotonicity is proved. The economical meaning of the chain: only one number of the level grows with N — the period witness $W_N \approx \ln N + O(1)$, slowly, while the defects $\gamma \sim \delta^4/k$ fall fast; their product creates the observed stiffness of the high levels.

## 6. Theorem 4 — the synchronous breathing and the closure

The fourth register is the dynamical content of the program. Let the ring be driven by the radial breathing program

$$
r(t) = R_0\,(1 + \varepsilon\cos \nu t), \qquad \theta_k(t) = \nu t + \frac{2\pi k}{N},
$$

with the amplitude $\varepsilon = \varepsilon_N$ from the transducer. The pair cancellations of Section 2 guarantee: in the Kirchhoff field such a configuration has no radial velocity of its own, so the radial drive must be supplied by a pump; the angular transport of the ring, however, is not prescribed — it follows the frozen law with the instantaneous rate $\Lambda_0/r(t)^2$.

**Theorem 4 (synchronous breathing).** The mean-transport identity holds:

$$
M_T\!\left[(1 + \varepsilon \cos u)^{-2}\right] = \frac{1}{2\pi}\int_0^{2\pi} \frac{du}{(1+\varepsilon\cos u)^2} = \frac{1}{(1-\varepsilon^2)^{3/2}},
$$

and therefore the phase accumulated by the ring over one breathing cycle at the frequency

$$
\nu = \omega_L(R_0)\,(1-\varepsilon^2)^{-3/2},
$$

equals exactly $2\pi$: every rosette $z_k(t) = r(t)e^{i(\nu t + 2\pi k/N)}$ is closed, and the whole configuration returns to its start at $T_c = 2\pi/\nu$.

Proof. The integral reduces by $t = \tan(u/2)$ to a rational one; the standard computation gives $\int_0^{2\pi}\frac{du}{a + b\cos u} = \frac{2\pi}{\sqrt{a^2 - b^2}}$ for $a > |b|$, and the differentiation in the parameter a gives $\int_0^{2\pi}\frac{du}{(a + b\cos u)^2} = \frac{2\pi a}{(a^2 - b^2)^{3/2}}$; at $a = 1$, $b = \varepsilon$ we obtain the identity. The phase over a cycle: $\int_0^{T_c}\frac{\Lambda_0\,dt}{r(t)^2} = \frac{\Lambda_0}{\nu R_0^2}\int_0^{2\pi}\frac{du}{(1+\varepsilon\cos u)^2} = \frac{\Lambda_0}{\nu R_0^2} \cdot \frac{2\pi}{(1-\varepsilon^2)^{3/2}}$; at the synchronous choice $\nu = \frac{\Lambda_0}{R_0^2}(1-\varepsilon^2)^{-3/2}$ this product equals $2\pi$ exactly. The closure of the configuration: at $t = T_c$ the phase of every vortex is shifted by exactly $2\pi$, the radius program is periodic, and $z_k(T_c) = z_k(0)$. ∎

It is essential that both parts of the theorem are exact statements, not approximations: the transport identity is an integral identity, and the closure is a consequence of periodicity. The numerical certificates: stage W5 holds the mpmath residual of the identity at $10^{-30}$ over the grid $\varepsilon \in [0.05, 0.6]$ and confirms the exact $2\pi$ phase advance with the error $3.6 \cdot 10^{-13}$; stage W6 pins the closure of the level rosettes (N = 7, $\varepsilon = \varepsilon_7$) with the residual $10^{-15}$ and the shape rigidity along the program — all $|z_k|$ coincide to $10^{-16}$. The geometry of the program is illustrated by fig03: at the raised amplitude $\varepsilon = 0.25$ every vortex rides the limacon $r(\theta) = R_0(1 + \varepsilon\cos(\theta - 2\pi k/N))$, and the family of seven rosettes closes over three periods.

## 7. Theorem 5 — the dichotomy of the invariants

The fifth register answers which of the classical invariants of the ring are algebraic and which carry a transcendental shell.

**Theorem 5 (the dichotomy).** For the frozen regular N-gon of radius R:

(i) the pair-distance product is algebraic in R:

$$
\prod_{i<j} |z_i - z_j| = R^{\frac{N(N-1)}{2}}\, N^{\frac{N}{2}}, \qquad \left|\mathrm{disc}(z^N - \sigma)\right| = N^N |\sigma|^{N-1};
$$

(ii) the Hamiltonian has the closed form

$$
H(R) = -\frac{\Gamma^2}{2\pi}\left[\frac{N(N-1)}{2}\ln R + \frac{N}{2}\ln N\right],
$$

that is, it splits into an R-algebraic part and a transcendental ln-shell;

(iii) the impulses $L = 0$, the moment $I = N\Gamma R^2$ are algebraic, and the power sums $S_m$ are cyclotomic.

Proof. (i) The distance between the vertices is $R|1 - \zeta_N^{j-i}|$, and the product over the pairs splits into $R^{N(N-1)/2}$ and the chord product $\prod_m |1-\zeta_N^m|^{N/2} = N^{N/2}$ — by Theorem 2. The discriminant of the binomial $z^N - \sigma$ equals $(-1)^{N(N-1)/2} N^N \sigma^{N-1}$ — the standard formula for $x^n - a$; its modulus gives the second register, and the root system of Theorem 1 links the discriminant to the squared product of the root differences. (ii) The logarithm of the product from (i) is exactly the sum $\sum_{i<j}\ln|z_i - z_j|$, and the substitution into the definition of H gives the closed form; the term $\frac{N}{2}\ln N$ is the constant of the level, the term with $\ln R$ is the only transcendental shell. (iii) The impulse is Theorem 1; the moment is the direct computation $\sum_k |z_k|^2 = NR^2$. ∎

The dichotomy agrees with the periodic register: the boundary periods (the algebraic multiples of π) serve the algebraic registers of the ring — the chords, the discriminant, the moment; the interior Gamma-periods serve the modulation — the amplitude and the frequency of the breathing through $W_N$. The numerical certificate is stage W4: the closed form of H matches the direct pairwise summation with the error $10^{-16}$, the distance product with $1.3 \cdot 10^{-16}$; the picture is fig05.

## 8. The verification ladder W1–W7

The ladder consists of seven stages; each is a deterministic JSON protocol in `results/protocols/` bound to a run. The presets: quick (smoke), default (registration), full (long integration).

| stage | register | tolerance | result |
|-------|----------|-----------|--------|
| W1 | reflection identity + P(1,1) = 1 + symmetry | 1e−30 | 5.1e−49 |
| W2 | the algebraic boundary + the sine product | 1e−30 | 5.1e−49 |
| W3 | the binomial z^N − σ + moments + impulse | 1e−10 / 1e−12 | 6.4e−11 / 2.9e−14 |
| W4 | rigid rotation, shape, invariants, the H form | 1e−9 / 1e−12 | 1.1e−10 / 2.0e−12 |
| W5 | the mean-transport identity + the 2π advance | 1e−30 / 1e−12 | 1.0e−30 / 3.6e−13 |
| W6 | the rosette closure + the shape rigidity | 1e−9 | 1.5e−15 |
| W7 | the transducer table + the stiffness order + the round trip | 1e−15 | 1.2e−16 |

The registered table of the levels (the default preset):

| N | k | W_N | Δ_Ch | ε_N | ν/ω_L | C_N |
|---|---|-----|------|-----|-------|-----|
| 7 | 4 | 2.175444 | 3.677e−03 | 3.664e−03 | 1.0000201 | 5.609 |
| 9 | 6 | 2.416543 | 7.474e−04 | 7.469e−04 | 1.0000042 | 7.200 |
| 15 | 17 | 2.915447 | 2.357e−05 | 2.357e−05 | 1.0000000 | 10.656 |
| 30 | 70 | 3.603649 | 2.135e−07 | 2.135e−07 | 1.0000000 | 15.360 |

The test guard of the mini-research is 37 tests; together with the parent package the full guard is 126 tests and keeps every number of the tables bound to the protocols.

## 9. The numerical experiments and the figures

The figure factory reads the registers from the committed protocols and never invents numbers; the trajectory panels are pictures of the program recomputed from the modules. fig01 shows the period field of the level N = 15 and the algebraic boundary: the residual of the reflection identity is $5.1 \cdot 10^{-49}$ on all fourteen boundary pairs. fig02 — the defect chain: the discriminant $\Delta_{Ch}(N)$ on the grid N = 3..30 with the power approximation $1.7 \cdot 10^3 \cdot N^{-6.7}$ and the mark of the four registered levels; the right panel contrasts the amplitude $\varepsilon_N$ and the stiffness $C_N$.

The synchronous breathing is shown on fig03: the rosettes of the seven vortices over three closure periods at the illustrative amplitude $\varepsilon = 0.25$ (the level value $\varepsilon_7 = 3.664 \cdot 10^{-3}$ is far smaller — a stiff ring). fig04 — the mean-transport identity: the quadrature mean and the closed form $(1-\varepsilon^2)^{-3/2}$ merge over the whole grid, the residual of the inset is at the machine level. fig05 — the dichotomy: on the left, the boundary (algebraic) and the diagonal (Gamma-period) values of the level N = 7; on the right, the closed form of the Hamiltonian against the direct pairwise summation.

## 10. The honest limitations

The breathing program is kinematic: the Kirchhoff flow does not sustain the radial velocity of the polygon, so the radial drive is an external pump. The angular transport, however, is not prescribed — it follows the frozen law $\Lambda_0/r(t)^2$, and that is why the transport identity and the closure are exact; but the direct integration of the free ring from the modulated initial condition yields the rigid rotation at the radius $R_0(1+\varepsilon)$ — the ring will not breathe by itself. The stiffness power law is a numerical approximation on a finite range; only the defect monotonicity is proved. The interior periods are treated as transcendental constants of Gamma type with no algebraic claims; no reduction is used anywhere. The spectral registers of the Jacobian serve as diagnostics; the ladder claims no stability results. Finally, all tolerances of the ladder are machine tolerances, not mathematically strict bounds; the formalization queue C1–C3 of the roadmap addresses this.

## 11. Summary

A self-contained study has been assembled that translates the vortex ring into the language of algebra and periods. The ring is the root system of a binomial; its deformations live on the character lattice; the boundary of the period domain of the level is algebraic; a finite defect chain converts the Gamma-periods into the modulation program; the synchronous breathing at the transducer frequency closes exactly; the invariants of the ring split into an algebraic part and a transcendental ln-shell. Every register is held by a theorem with a proof and a protocol with a tolerance; the ladder W1–W7, the table of the levels 7/9/15/30, five figures and thirty-seven tests form a reproducible circuit. The roadmap C1–C4 leads from the numerical certificates to formalization and extensions — unequal circulations, two-frequency programs, and the senior-mode experiments.
