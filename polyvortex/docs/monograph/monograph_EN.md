# POLYVORTEX — A Research Monograph

## The N-vortex generalization of Theorem 3.1: the classical layer, the admissibility threshold, the kinematic obstruction and the averaged-frequency bridge

*Mini-repository `polyvortex/` of the TRIVORTEX framework — version 1.0.0.
Every number quoted below is bound to a run: see `results/protocols/` and
`make ladder`.*

---

## Abstract

This monograph extends the parent TRIVORTEX framework from the three-vortex
Lagrange setting to an arbitrary number $N$ of equal point vortices. The study
is organized as a seven-stage ladder **W1–W7** that mirrors the parent ladder
V1–V4 and adds four research registers of its own. Three rigorous statements
emerge, each with a proof or a decidable formalization path: **Theorem B**
(the closed form of Theorem 3.1 is non-degenerate exactly when
$C_{Ch} > \pi \ln 2$, where its modulation amplitude equals $\varepsilon = 1$
in closed form), **Lemma C** (the Kirchhoff radial equation obstructs every
symmetrically pulsating polygon: the induced radial velocity vanishes by pair
cancellation, so pulsation is dynamically impossible for any $N \ge 2$), and
**Lemma D** (the cycle-averaged kinematic frequency of a pulsating regular
polygon equals $\omega_N (1-\varepsilon^2)^{-3/2}$, an integral identity
certified numerically to $3 \cdot 10^{-15}$). Together they yield the
compatibility table **D1** — the periods $T_{comp}(N, C_{Ch})$ at which the
gauge frequency law of Theorem 3.1 meets the averaged Kirchhoff kinematics —
and they surface one registered fact about the parent default: the pair
$(C_{Ch}, T) = (1, 2\pi)$ lies below the admissibility threshold
$\pi \ln 2 \approx 2.177586$. All stages pass; the classical Havelock
stability threshold (stable for $N \le 7$, unstable for $N \ge 8$) is
reproduced spectrally with a three-order margin.

## 1. Scope and provenance

The parent TRIVORTEX framework anchors its verification ladder on Theorem 3.1,
a closed-form choreographic solution of the three-vortex model with the
Chaplygin topological integral, and on the numerical conservation of the
classical vortex integrals. The present mini-repository asks the natural
next question — *what survives the passage from $N = 3$ to general $N$?* —
and answers it with the same discipline that governs the parent: every claim
is either proven, or certified by a committed JSON protocol, or explicitly
labelled as a conjecture with the numbers that constrain it.

The work was prompted by a research discussion on how the three-vortex
ansatz could be lifted to $N$ vortices while keeping the hard structure —
uniform phase separation $2\pi/N$, radial modulation driven by $C_{Ch}$, and
the frequency law $\omega = (2\pi/T)\,e^{C_{Ch}/\pi}$ — intact. No external
material is quoted beyond the classical literature listed in the references;
the analysis, the code and the protocols are original to this repository.

Three design rules separate this mini-repository from the parent ladder:

1. **Self-containment.** Nothing here imports the parent ladder at runtime.
   The parent is touched only by *tests* (`tests/conftest.py` adds its path)
   for cross-validation — the same pinning discipline the parent applies to
   its multi-language ports.
2. **Two-layer honesty.** The parent model lives on two layers — the
   Kirchhoff dynamics (Layer K, numerical) and the topological closed form
   (Layer G, analytic). Conflating them is the single most common source of
   false claims around Theorem 3.1; this monograph keeps them separated
   explicitly and measures precisely where they touch (Sections 6–7).
3. **Every number is bound to a run.** Each ladder stage writes a
   deterministic JSON protocol into `results/protocols/`; the test suite
   re-derives the preset-independent registers and compares.

## 2. The two layers of the Trivortex model

**Layer K (Kirchhoff dynamics).** $N$ point vortices with circulations
$\Gamma_k$ at positions $z_k = x_k + i y_k$ obey

$$
\dot x_i = -\frac{1}{2\pi}\sum_{j \ne i} \Gamma_j
\frac{y_i - y_j}{r_{ij}^2}, \qquad
\dot y_i = +\frac{1}{2\pi}\sum_{j \ne i} \Gamma_j
\frac{x_i - x_j}{r_{ij}^2}, \qquad
r_{ij}^2 = (x_i - x_j)^2 + (y_i - y_j)^2 .
$$

The system carries the classical integrals — the Hamiltonian
$H = -\frac{1}{2\pi}\sum_{i<j}\Gamma_i\Gamma_j \ln r_{ij}$, the linear
impulses $P = \sum \Gamma_k x_k$, $Q = \sum \Gamma_k y_k$ and the angular
impulse $I = \sum \Gamma_k |z_k|^2$ — which the parent ladder verifies along
its trajectories (stages V3–V4) and this ladder re-verifies for every $N$
(stage W3). The integrals are the window-independent conserved quantities of
the model.

**Layer G (the closed form of Theorem 3.1).** The parent ladder registers
the gauge-level solution

$$
r_k(t) = \sqrt{C_{Ch}}\,\bigl(1 + \varepsilon \cos(\omega t + \tfrac{2\pi k}{3})\bigr),
\qquad
\theta_k(t) = \omega t + \tfrac{2\pi k}{3},
$$

with the frequency and amplitude laws

$$
\omega = \frac{2\pi}{T}\, e^{C_{Ch}/\pi}, \qquad
\varepsilon = \frac{1}{e^{C_{Ch}/\pi} - 1},
$$

and the Section-6 diagnostic combination
$C_{Ch}(t) = r^2(\dot\theta - q A_\theta)$ with $A_\theta = 1/r$. The parent
ladder is explicit that this diagnostic *oscillates by construction* and is
window-dependent; the pass registers of V1 are the angular separation and
the periodicity of the closed form, not the diagnostic drift. This
mini-repository keeps exactly that honesty convention (stage W1 reproduces
the parent's registers and reports the same diagnostic behaviour,
drift amplitude $\approx 15.01$ over $[0, 100\,T]$ at the registered
default, mirroring the parent's diagnostic).

The two layers are independent: Layer G prescribes kinematics, Layer K
prescribes dynamics. A closed form becomes a claim about physics only after
its compatibility with Layer K is established — and establishing precisely
that, for general $N$, is the scientific payload of this monograph.

## 3. The classical layer at general N: relative equilibria

**Theorem A (classical, Kirchhoff 1876).** *Let $N \ge 2$ equal vortices of
circulation $\Gamma$ sit at the vertices of a regular $N$-gon of circumradius
$R$. Then the configuration rotates rigidly about its centre with angular
velocity*

$$
\omega_N = \frac{\Gamma (N-1)}{4\pi R^2}.
$$

*Proof sketch.* At vertex $k$, pair the contribution of vertex $j$ with its
mirror image $j'$ under reflection through the radial axis of $k$. Writing
the chord directions explicitly, the radial components of the induced
velocity cancel in each pair while the tangential components add. Summing
the tangential parts over $j \ne k$ reduces to the roots-of-unity identity
$\sum_{m=1}^{N-1} \frac{1}{1 - e^{2\pi i m/N}} = \frac{N-1}{2}$, which turns
the velocity sum into $\Gamma (N-1)/(4\pi R)$ at radius $R$. Dividing by $R$
gives the rate. $\square$

The identity is exactly the formalization target the parent roadmap queues
as **T1** ("the roots-of-unity identity turns the velocity sum into
algebra"); Theorem A is its numerical shadow, and stage W2 certifies it:

| $N$ | $\omega_N$ (analytic) | measured (RK4, 2 rotations) | rel. error | shape dev. |
|----:|----------------------:|----------------------------:|-----------:|-----------:|
| 2 | 0.0795774715459 | 0.0795774715459 | 2.9e-12 | 2.4e-14 |
| 3 | 0.1591549430919 | 0.1591549430919 | 2.9e-12 | 2.7e-14 |
| 4 | 0.2387324146378 | 0.2387324146378 | 2.9e-12 | 2.3e-14 |
| 5 | 0.3183098861838 | 0.3183098861838 | 2.9e-12 | 2.9e-14 |
| 6 | 0.3978873577297 | 0.3978873577297 | 2.9e-12 | 3.0e-14 |
| 7 | 0.4774648292757 | 0.4774648292757 | 2.9e-12 | 3.3e-14 |
| 8 | 0.5570423008216 | 0.5570423008216 | 2.8e-12 | 1.4e-12 |

(Protocol `W2_ring_rotation_default.json`, $\Gamma = 1$, $R = 1$,
2000 steps/period.) A pleasant cross-ladder handshake: at $N = 7$, $R = 1$,
$\Gamma = 1$ the rate is $6/(4\pi) = 3/(2\pi) = 0.477464829275686$ — exactly
the parent ladder's registered Lagrange literal $\omega_{Lagrange}$. The
coincidence is trivial algebra, but it makes a memorable pin between the two
ladders and is locked by a unit test.

**Conservation along the orbits (stage W3).** The relative drifts of
$H, P, Q, I$ after two full rotations stay below $4.2 \cdot 10^{-14}$ for
every $N \in \{2,\dots,8\}$ — the parent's V3 register, reproduced for the
whole ring family (protocol `W3_invariants_default.json`).

**Spectral stability (stage W4).** Linearizing Layer K at the co-rotating
equilibrium — the Jacobian $J = A + \omega_N S$ with the analytic pair-Jacobian
$A$ and the transport generator $S$ — yields the classical classification:

| $N$ | $\max \mathrm{Re}\lambda$ | verdict | Havelock |
|----:|--------------------------------:|---------|----------|
| 2 | 6.9e-10 | stable | stable |
| 3 | 0.0 | stable | stable |
| 4 | 3.8e-9 | stable | stable |
| 5 | 0.0 | stable | stable |
| 6 | 0.0 | stable | stable |
| 7 | 7.0e-9 | stable | stable |
| 8 | **+0.4502** | unstable | unstable |

The threshold — stable for $N \le 7$, unstable from $N = 8$ — is the
Havelock (1931) result, with Khazin's later rigorous treatment; the numeric
margin is three orders of magnitude on both sides (the stable cases sit at
the defective-zero noise floor, see the Remark in Section 6.3; the unstable
$N = 8$ case grows at $\mathrm{Re}\lambda = 0.450$). This stage is the
numerical prototype of the parent roadmap item **T3**.

## 4. The generalized closed form: Hypothesis H1 and its registers

**Hypothesis H1 (working form).** *For $N$ vortices with equal circulations
and equal topological charges $q_k = q$ there exists a solution of the
combined model of the form*

$$
r_k(t) = \sqrt{C_{Ch}}\,\bigl(1 + \varepsilon \cos(\omega t + \tfrac{2\pi k}{N})\bigr),
\qquad
\theta_k(t) = \omega t + \tfrac{2\pi k}{N},
\qquad k = 0, \dots, N-1,
$$

*with $\omega = \frac{2\pi}{T} e^{C_{Ch}/\pi}$ and
$\varepsilon = \frac{1}{e^{C_{Ch}/\pi} - 1}$.*

The structural registers of the parent Theorem 3.1 generalize verbatim, and
stage W1 certifies them at $N = 3$ against the parent's pinned literals:

- **Uniform phase choreography.** The angles differ by exactly $2\pi/N$ at
  all times; the register measures the deviation of the cyclic separations
  from $2\pi/N$ (protocol value $6.9 \cdot 10^{-14}$, pure float noise of the
  modulo reduction, tolerance $10^{-12}$).
- **Periodicity.** $r_k(t + T_r) = r_k(t)$ with $T_r = 2\pi/\omega$; the
  residual is $9.4 \cdot 10^{-14}$ (float noise of the cosine evaluation).
- **Pinned literals.** At $C_{Ch} = 1$, $T = 2\pi$ the implementation
  reproduces the parent's registered frequency
  $\omega = e^{1/\pi} = 1.3748022274393588$ *bit-for-bit* (anchor error
  $0.0$), and likewise the amplitude $\varepsilon = 2.668070477\ldots$
  (anchor error $0.0$).

Two geometric observations, recorded because they matter for everything that
follows:

1. **The angular register is N-generic; the radial one is not a polygon.**
   For $\varepsilon \ne 0$ the radii of the $N$ vortices differ
   ($r_k$ carries the phase $2\pi k/N$), so the instantaneous configuration
   is *not* a regular polygon — it is a star-shaped configuration with
   uniformly spaced directions but unequal radii. The "regular $N$-gon"
   picture survives only at $\varepsilon = 0$ instants. The shape register of
   stage W6 quantifies exactly this (Section 6.2).
2. **The gauge diagnostic survives at any $N$.** The combination
   $C_{Ch}(t) = r^2(\dot\theta - q/r)$ stays a well-defined diagnostic along
   the closed form for every $N$ and keeps oscillating by construction, as
   in the parent.

## 5. Admissibility of the closed form: Theorem B

The amplitude law $\varepsilon(C_{Ch}) = 1/(e^{C_{Ch}/\pi} - 1)$ is
monotonically decreasing on $C_{Ch} > 0$, from $+\infty$ to $0$. The closed
form describes a rotating configuration with *positive* radii only while
$1 + \varepsilon \cos\varphi > 0$ for all $\varphi$, i.e. while
$\varepsilon < 1$. Solving the boundary exactly:

$$
\varepsilon = 1 \iff e^{C_{Ch}/\pi} - 1 = 1 \iff e^{C_{Ch}/\pi} = 2
\iff C_{Ch} = \pi \ln 2 .
$$

**Theorem B (admissibility).** *The closed form of Theorem 3.1 (and of
Hypothesis H1 at any $N$) has strictly positive radii for all times and all
vortices if and only if*

$$
C_{Ch} > C_{Ch}^{*} := \pi \ln 2 \approx 2.177586090303602 .
$$

*At $C_{Ch} = C_{Ch}^{*}$ the amplitude is exactly $\varepsilon = 1$ and
each radius touches zero once per period; below the threshold each radius
changes sign twice per period — in the complex plane the trajectory is
continuous ($z_k = r_k e^{i\theta_k}$ is insensitive to the phase flip
$\pi$), but the polar registers (radius positivity, the polygon picture, the
$A_\theta = 1/r$ gauge combination at the crossing instants) degenerate.*

*Proof.* The chain of equivalences above is exact real algebra:
$\varepsilon < 1 \iff e^{C_{Ch}/\pi} > 2 \iff C_{Ch}/\pi > \ln 2$. The
minimum of $1 + \varepsilon\cos\varphi$ over a period is $1 - \varepsilon$,
so positivity for all $\varphi$ is equivalent to $\varepsilon < 1$; the
touching/crossing behaviour follows from the structure of the cosine.
$\square$

Stage W5 certifies the theorem on a dense grid: over 200 values of
$C_{Ch} \in [0.5, 10]$ the equivalence
$\bigl(C_{Ch} > C_{Ch}^{*}\bigr) \Leftrightarrow (\varepsilon < 1)$ holds
with **zero violations**, the amplitude at the threshold equals 1 to
machine precision (error $0.0$), and the sampled minimum of the radius
matches the analytic $\sqrt{C_{Ch}}(1 - \varepsilon)$ within
$1.9 \cdot 10^{-7}$ — the uniform-grid sampling bound, not a model error
(protocol `W5_admissibility_default.json`).

**A registered fact about the parent default.** The parent ladder's
registered pair $(C_{Ch}, T) = (1, 2\pi)$ sits *below* the threshold:
$\varepsilon(1) \approx 2.668 > 1$. In this zone the closed form remains a
perfectly well-defined complex choreography and passes every structural
register, but the polar picture "an $N$-gon of radius
$\sqrt{C_{Ch}}(1 + \varepsilon\cos)$" is degenerate — the radii sweep
through zero. This observation feeds the parent roadmap item **T5**
("admissible region of the closed form") with a sharp, decidable boundary;
a natural reading is that the non-degenerate regime of the closed form opens
at $C_{Ch} > \pi\ln 2$, and that parameter studies of Layer G should quote
$C_{Ch}$ relative to $C_{Ch}^{*}$.

## 6. The kinematic obstruction: Lemma C

### 6.1 The symmetric pulsation case

The cleanest question about H1 is dynamical: *does the pulsating form solve
Layer K?* Strip the phase shifts from the radii first (all vortices share one
common radius $r(t)$, directions uniform) — then the configuration is a
regular $N$-gon at every instant, and the answer is exact.

**Lemma C (obstruction).** *In the Kirchhoff model with equal circulations,
let a configuration be a regular $N$-gon of common radius $r(t)$ rotating
with common angular velocity $\dot\theta = \omega(t)$. Then the induced
radial velocity vanishes identically, $v_r \equiv 0$, and the radial equation
of motion reads $\dot r = 0$. Consequently a symmetrically pulsating polygon
satisfies Layer K if and only if $\varepsilon = 0$ (and then
$\omega = \Gamma(N-1)/(4\pi R^2)$, Theorem A).*

*Proof.* Fix vertex $k$ and reflect the polygon through the radial axis of
$k$. The reflection maps the vertex set onto itself (vertex $j$ at angle
$\varphi$ swaps with the vertex at $-\varphi$), while the induced velocity
field of the pair contributes equal-and-opposite radial components: writing
the chord from $k$ to a vertex at angle $\varphi$, the induced velocity on
$k$ has radial component $+\frac{\Gamma}{2\pi d}\cos\frac{\varphi}{2}$, and
its mirror contributes
$-\frac{\Gamma}{2\pi d}\cos\frac{\varphi}{2}$. All radial contributions
cancel pairwise; the tangential ones double. Hence $v_r = 0$ for every $N$
at every instant, and the radial equation $\dot r = v_r$ forces $r$ to be
constant. $\square$

The tangential register fails independently: Layer K demands
$\omega(t) = \Gamma(N-1)/(4\pi r(t)^2)$, which is compatible with a
prescribed constant $\omega$ only when $r$ is constant. So even a
"kinematically steered" pulsation with a time-varying rate is not a free
Layer-K orbit — the ring either rotates rigidly at the Theorem-A rate or it
is not a Layer-K solution at all.

### 6.2 The phase-shifted H1 case

H1 as posed carries the phase $2\pi k/N$ in *both* the radii and the angles,
so for $\varepsilon \ne 0$ the configuration is not a polygon at all
(Section 4, observation 1). Stage W6 measures both failures on
$N = 3$, $\Gamma = 1$, $R = 1$, $\omega = 1$ over one period:

| $\varepsilon$ | shape register: max deviation from the chord table | induced radial velocity, max |
|--------------:|---------------------------------------------------:|-----------------------------:|
| 0.01 | 8.660e-3 | 3.99e-6 |
| 0.05 | 4.330e-2 | 1.01e-4 |
| 0.10 | 8.660e-2 | 4.13e-4 |
| 0.30 | 2.598e-1 | 4.00e-3 |

The shape deviation is *exactly linear* with slope $\cos(\pi/6) =
\sqrt{3}/2 \approx 0.8660$ (the slopes recovered from the table agree to
$10^{-3}$, and the test suite pins this). The induced radial velocity —
zero for the symmetric case — is here nonzero and scales approximately as
$0.04\,\varepsilon^2$ over the scanned range. Both effects vanish as
$\varepsilon \to 0$, consistently with the only $N$-gon limit being the
rigid rotation.

**Corollary (the reduction verdict).** *Within Layer K, Hypothesis H1 is a
solution exactly in its $\varepsilon = 0$ shadow — the classical Theorem A
at the kinematic rate. The frequency law $\omega = (2\pi/T)e^{C_{Ch}/\pi}$
is an independent Layer-G postulate and must not be read as the Kirchhoff
rotation rate of a polygon with mean radius $\sqrt{C_{Ch}}$; the quantitative
bridge between the two is the subject of Section 7.*

### 6.3 Numerical remark: the defective zero

The co-rotating Jacobian at the ring owns a zero eigenvalue of algebraic
multiplicity two and geometric multiplicity one (the continuum of rotated
polygons is a one-parameter family of equilibria). Rounding splits such a
defective double zero into a $\pm$-real pair of size
$\sqrt{\varepsilon_{mach}\,\|J\|} \sim 10^{-9}$ — visible in the W4 protocol
as $\max\mathrm{Re}\lambda \in \{\pm 10^{-9}\}$ for the stable cases.
The stability classifier therefore runs at tolerance $10^{-7}$, three orders
above the noise floor and three below the $N = 8$ growth rate $0.450$.

## 7. The averaged-frequency bridge: Lemma D and the D1 design rule

If pulsation is dynamically obstructed, the next best question is
*compatibility on average*: at what rate would the "instantaneous kinematics"
of a pulsating polygon rotate over a full cycle? The answer is exact.

**Lemma D (averaged frequency).** *For the symmetric pulsation
$r(t) = R(1 + \varepsilon\cos\omega t)$ with $|\varepsilon| < 1$, the
cycle-averaged Kirchhoff rate*

$$
\bigl\langle \omega_{kin} \bigr\rangle
= \frac{1}{T_r}\int_0^{T_r}
\frac{\Gamma (N-1)}{4\pi\, r(t)^2}\, dt
= \frac{\Gamma (N-1)}{4\pi R^2}\,\bigl(1 - \varepsilon^2\bigr)^{-3/2},
$$

*is independent of the modulation rate $\omega$.*

*Proof.* Substituting $\varphi = \omega t$ removes $\omega$ and reduces the
average to $\frac{\Gamma(N-1)}{4\pi R^2}\,\frac{1}{2\pi}\int_0^{2\pi}
\frac{d\varphi}{(1+\varepsilon\cos\varphi)^2}$. The standard differentiated
form of the Poisson integral,
$\frac{1}{2\pi}\int_0^{2\pi}\frac{d\varphi}{(a + b\cos\varphi)^2}
= \frac{a}{(a^2 - b^2)^{3/2}}$, at $a = 1$, $b = \varepsilon$ gives
$(1 - \varepsilon^2)^{-3/2}$. $\square$

Stage W7 certifies the integral identity by Gauss–Legendre quadrature
(160 nodes): maximum relative error $2.9 \cdot 10^{-15}$ over
$\varepsilon \in \{0.1, \dots, 0.9\}$, the bridge register for
$(N, \varepsilon) \in \{2..8\} \times \{0.2, 0.5, 0.8\}$ at
$3.5 \cdot 10^{-15}$ (protocol `W7_bridge_default.json`). The quadrature
convergence is itself a measured fact: at the quick preset's 80 nodes the
sharpest case ($\varepsilon = 0.9$) retains $2 \cdot 10^{-9}$, dropping
six orders at 160 nodes — the spectral convergence expected for analytic
integrand with the nearest pole at $\mathrm{Im}\varphi =
\mathrm{arccosh}(1/\varepsilon)$.

**Design rule D1 (compatibility curve).** *Define the compatibility period*

$$
T_{comp}(N, C_{Ch}) \;=\; 2\pi\, e^{C_{Ch}/\pi}\,
\frac{4\pi C_{Ch}\,\bigl(1 - \varepsilon^2\bigr)^{3/2}}{\Gamma (N-1)},
\qquad \varepsilon = \varepsilon(C_{Ch}),
$$

*as the unique period at which the Theorem-3.1 frequency law
$\omega = (2\pi/T)e^{C_{Ch}/\pi}$ (with the mean radius
$R^2 = C_{Ch}$) equals the averaged kinematic frequency of Lemma D. The
protocol tabulates $T_{comp}$ over the admissible window; e.g. at
$\Gamma = 1$:*

| $C_{Ch}$ | $N=3$ | $N=4$ | $N=5$ | $N=6$ | $N=7$ | $N=8$ |
|---------:|------:|------:|------:|------:|------:|------:|
| 3 | 146.13 | 97.42 | 73.06 | 58.45 | 48.71 | 41.75 |
| 5 | 875.98 | 583.99 | 437.99 | 350.39 | 291.99 | 250.28 |
| 10 | 9496.0 | 6330.7 | 4748.0 | 3798.4 | 3165.3 | 2713.2 |
| 20 | 459401.4 | 306267.6 | 229700.7 | 183760.6 | 153133.8 | 131257.6 |

The self-consistency of the table is verified to $3.5 \cdot 10^{-16}$
relative: substituting $T = T_{comp}$ back into the frequency law reproduces
the averaged kinematic rate. Two structural facts deserve attention.
First, $T_{comp}$ grows roughly like $e^{C_{Ch}/\pi}\,C_{Ch}$ — exponentially
in the gauge constant — while the classical rate decays only algebraically
in $C_{Ch}$; the gauge law and the kinematics therefore agree only along a
thin, explicitly computable curve, not on an open set. Second, the registered
parent pair $(C_{Ch}, T) = (1, 2\pi)$ lies outside the admissible window
entirely (Theorem B), so no compatibility statement can be made for it
without leaving the non-degenerate regime.

**What D1 is and is not.** D1 is a design relation for a *driven*
construction: if one insists on a pulsating choreography whose modulation
period matches its own cycle-averaged kinematic rate — e.g. for a
gauge-constrained or externally forced model variant — the constraint
selects the period $T_{comp}$ exactly. D1 is *not* a claim that Layer K
admits pulsating free orbits (Lemma C forbids that); the driven reading is
the only consistent one, and it is flagged as such in the protocol metadata.

## 8. From observations to theorems: the formalization queue

The ladder was built so that each stage maps onto a formalizable statement.
The mini-repository maintains its own queue, aligned with the parent
roadmap's theorem table (root README, Section 18.2):

| id | statement | current status in this mini-repo | formalization path | parent link |
|----|-----------|----------------------------------|--------------------|-------------|
| **TB1** | Theorem B: $\varepsilon < 1 \iff C_{Ch} > \pi\ln 2$ | proven (Section 5), certified by W5 | one-page: monotonicity of $\exp$ and $\ln$ in Mathlib or Coq's `Reals`; a decidable $\mathbb{Q}$-certificate for the boundary constant | feeds **T5** |
| **TB2** | Lemma C: $v_r \equiv 0$ for the symmetric ring; pulsation obstructed | proven (Section 6.1), certified by W6 | the chord-geometry pair-cancellation in Coq; the roots-of-unity sum in Mathlib for the tangential sum | feeds **T1** |
| **TB3** | Lemma D: $\langle\omega_{kin}\rangle = \omega_N (1-\varepsilon^2)^{-3/2}$ | proven (Section 7), certified by W7 | the differentiated Poisson integral — a standard Mathlib-style computation; or an interval-arithmetic certificate of the integral on $[-0.9, 0.9]$ | new, enables T5's region |
| **TW4** | Theorem A: rigid rotation at $\omega_N = \Gamma(N-1)/(4\pi R^2)$ | classical; measured to $2.9 \cdot 10^{-12}$ for $N = 2..8$ | the same roots-of-unity identity as TB2, then the rigid-rotation lemma | is **T1** |
| **TW5** | Havelock threshold: stable $N \le 7$, unstable $N \ge 8$ | reproduced spectrally (W4), margin $10^3$ | characteristic polynomial per mode family; Routh–Hurwitz-type criterion — decidable, hard | feeds **T3** |

The dependency order is TB1 → TB2 → TW4 → TB3 → TW5: the admissibility
theorem is the cheapest and should be formalized first; TW4 shares its
algebraic core with TB2; TB3 is an integral statement with a clean numeric
fallback (interval arithmetic); TW5 is the long-term target. Each statement
above is already phrased so that a Coq or Lean 4 port can be opened as a
stub with the numeric protocol as the reference oracle — the same
double-formalization discipline the parent roadmap prescribes for M5.

## 9. Numerical protocol summary

All protocols live in `results/protocols/` (preset `default` unless noted),
produced by `make ladder` (one command, deterministic file names). The
registered tolerances: separation and periodicity $10^{-12}$; shape and
invariant drift $10^{-10}$; measured-rate band $10^{-6}$ (parent's band);
stability classifier $10^{-7}$; algebraic identities $10^{-12}$; the W5
minimum-radius register $10^{-6}$ absolute (uniform-grid sampling bound).

| stage | register | value | verdict |
|-------|----------|-------|---------|
| W1 | separation / periodicity / anchors | 6.9e-14 / 9.4e-14 / 0.0 | PASS |
| W1 | Section-6 diagnostic drift (report-only) | 15.01 over $[0,100T]$ | — |
| W2 | $\omega_N$ relative error, $N = 2..8$ | $\le 2.9 \cdot 10^{-12}$ | PASS |
| W2 | chord-shape deviation | $\le 3.3 \cdot 10^{-14}$ ($N \le 7$) | PASS |
| W3 | worst invariant drift | $\le 4.2 \cdot 10^{-14}$ | PASS |
| W4 | stable band $\max\mathrm{Re}\lambda$ | $\le 7.0 \cdot 10^{-9}$ | PASS |
| W4 | $N = 8$ growth rate | $+0.4502$ | PASS (unstable) |
| W5 | threshold equivalences on 200 points | 0 violations | PASS |
| W5 | min-radius sampling error | $1.9 \cdot 10^{-7}$ | PASS |
| W6 | symmetric pulsation: induced $\vert v_r\vert$ | $\le 4.9 \cdot 10^{-16}$ | PASS |
| W6 | H1 phase-shifted: shape slope | $\sqrt{3}/2$ (linear in $\varepsilon$) | recorded |
| W6 | H1 phase-shifted: induced $\vert v_r\vert$ | $\approx 0.04\,\varepsilon^2$ | recorded |
| W7 | integral identity (160 GL nodes) | $2.9 \cdot 10^{-15}$ | PASS |
| W7 | bridge $(N, \varepsilon)$ grid | $3.5 \cdot 10^{-15}$ | PASS |
| W7 | $T_{comp}$ self-consistency | $3.5 \cdot 10^{-16}$ | PASS |

Runtime: `quick` 1.3 s, `default` 7.3 s, `full` $\approx$ 60 s (whole
ladder, one core of the reference laptop class).

## 10. Honesty notes

1. **Hypothesis H1 is not a Layer-K solution.** The central finding of this
   mini-repository is a *negative* result with a positive structure: the
   pulsating ansatz is dynamically obstructed (Lemma C), the phase-shifted
   variant is obstructed even geometrically (W6), and the frequency law is
   compatible with the kinematics only along the D1 curve. None of this
   diminishes the parent Theorem 3.1 — it lives on Layer G, where its
   registers are exact — but any *dynamical* reading of H1 must be dropped
   or replaced by the driven construction of Section 7.
2. **The parent default is below the admissibility threshold.** $C_{Ch} = 1$
   lies in the radius-crossing zone. This is a fact about the registered
   parameter, not about the theorem; the structural registers are blind to
   it, the polar registers are not. Parameter studies should quote
   $C_{Ch}$ relative to $\pi\ln 2$.
3. **Stability is spectral, not nonlinear.** W4 classifies the linearized
   flow; nonlinear (Arnold-type) stability is a different, harder statement
   and is not claimed.
4. **The averaged-frequency lemma is an identity about a prescribed
   kinematics**, not a statement about attractors or effective dynamics of
   free Layer-K flows.
5. **Every protocol is reproducible.** `make ladder` regenerates all seven
   JSON files byte-identically up to the UTC timestamp; the test suite
   re-derives the preset-independent registers from scratch.

## 11. Резюме (RU)

Мини-репозиторий `polyvortex/` обобщает родительскую лестницу Trivortex
с трёх вихрей на произвольное $N$. Главные результаты: (1) теорема B —
замкнутая форма Теоремы 3.1 невырождена тогда и только тогда, когда
$C_{Ch} > \pi\ln 2 \approx 2.1776$; на зарегистрированном значении
$C_{Ch} = 1$ радиусы проходят через ноль (зарегистрировано для роадмап-пункта
T5); (2) лемма C — кирхгофовская динамика запрещает симметрично пульсирующий
$N$-угольник: наведённая радиальная скорость сокращается попарно, поэтому
пульсация невозможна ни при каком $N$, и гипотеза H1 редуцируется к
классическому жёсткому вращению с $\omega_N = \Gamma(N-1)/(4\pi R^2)$,
измеренному до $2.9\cdot10^{-12}$ для $N = 2..8$; (3) лемма D — циклически
усреднённая кинематическая частота равна
$\omega_N(1-\varepsilon^2)^{-3/2}$, что даёт точную кривую совместимости
D1 между частотным законом Теоремы 3.1 и кирхгофовской кинематикой;
(4) порог Хэвелока (устойчивость при $N \le 7$, неустойчивость при
$N \ge 8$) воспроизведён спектрально с запасом в три порядка. Все
утверждения либо доказаны, либо сертифицированы JSON-протоколами; очередь
формализации TB1–TW5 согласована с теоремной очередью корневого роадмапа.

## References

1. G. R. Kirchhoff, *Vorlesungen über mathematische Physik*, Bd. I:
   Mechanik, Teubner, Leipzig, 1876. — The point-vortex equations.
2. T. H. Havelock, "The stability of motion of vortices", *Philosophical
   Magazine* **11** (1931) 617–641. — Stability of the regular vortex
   polygon; the $N \le 7$ threshold.
3. L. G. Khazin, "On the stability of regular configurations of vortices",
   *Soviet Physics Doklady* **21** (1976). — Rigorous treatment of the
   polygon stability boundary.
4. H. Aref, "Motion of three vortices revisited", *The Physics of Fluids*
   **22** (1979) 393–400. — The modern taxonomy of three-vortex relative
   motions.
5. H. Aref, P. K. Newton, M. A. Stremler, T. Tokieda, D. L. Vainchtein,
   "Vortex crystals", *Advances in Applied Mechanics* **39** (2003) 1–79. —
   The standard review of vortex relative equilibria and their stability.
6. P. K. Newton, *The N-Vortex Problem: Analytical Techniques*,
   Springer, New York, 2001. — The $N$-vortex Hamiltonian formalism used
   in Sections 2 and 3.
7. Parent framework: TRIVORTEX repository, `verification/README.md` —
   the V1–V4 ladder, the registered tolerances and the Theorem 3.1 closed
   form; root `README.md`, Section 18 — the theorem queue T1–T6 that this
   mini-repository feeds.

