# Kozai–Lidov Oscillations in Hierarchical Triples

*TRIVORTEX Research Program · v1.0.0 · Monograph Edition*

|  |  |
|---|---|
| Study | TRX-10 |
| Program | TRIVORTEX — The Three-Body Problem in the Vortex Model |
| Author | Isaev Iskhak Khamzatovich (ORCID 0009-0003-7299-0701) |
| DOI | 10.5281/zenodo.21825394 |
| Date | 2026-10-06 |
| Code | `code/trx10_kozai_lidov.py` |
| Data | `results/trx10_results.json` |

## Abstract

This monograph treats the Kozai–Lidov mechanism — the secular exchange of eccentricity and inclination that a distant inclined companion drives in a hierarchical triple — in the full verification style of the TRIVORTEX program. Instead of coding the memorized analytic result, the study builds the doubly-averaged quadrupole Hamiltonian numerically: the instantaneous quadrupole disturbing potential is averaged over the inner orbit by a 240-point quadrature, tabulated on a 160 × 180 (e, ω) grid at the conserved j_z, and converted into a cubic spline whose derivatives drive the canonical flow. The spline flow reproduces the analytic maxima e_max = 0.763763 (i₀ = 60°) and 0.897239 (i₀ = 70°) to within the 2×10⁻³ tolerance, validates the Kozai landscape over 12 inclinations from 30° to 80° with a maximum deviation of 1.128×10⁻⁵, confirms the clock scaling P ∝ 1/m₃ (ratio P(2m₃)/P(m₃) = 0.481; P·m₃ spread 4.29%), and conserves the tabulated Hamiltonian to 1.33×10⁻⁵. An independent direct integration of the full three-dimensional restricted problem (m₃/M = 0.5, a_out = 5 a_in, 200 outer orbits) yields a smoothed maximum eccentricity of 0.7423 against 0.7638 — a −2.8% deviation consistent with the hexadecapole truncation. All four acceptance checks pass.

## Contents

1. Abstract
2. 1. Introduction and historical context
3. 1. Physical formulation
4. 1. Mathematical model
5. 1. Connection to the TRIVORTEX framework
6. 1. Numerical method
7. 1. Results and analysis
8. 1. Discussion
9. 1. Conclusions
10. 1. References
Appendix A. Parameter table
Appendix B. Reproduction

## 1. Introduction and historical context

The history of the effect began half a century before its discovery papers. In 1910 Hugo von Zeipel derived the secular equations of the double-averaged quadrupole three-body problem, and the reduction to a single degree of freedom was already implicit in his work. The classical papers of 1962 appeared independently and almost simultaneously: Yoshihide Kozai analysed secular perturbations of asteroids with high inclinations (Astronomical Journal 67, 591), while Mikhail Lidov studied the evolution of artificial satellite orbits under the gravitational action of external bodies (Planetary and Space Science 9, 719) — in the Russian literature the effect is still often called the Lidov–Kozai mechanism. Both found the same phenomenon: above the critical inclination 39.23° the eccentricity and the inclination begin to exchange periodically, and the inclination at maximum eccentricity drops exactly to the critical value.

The mechanism immediately became a working tool of celestial mechanics. It bounds the lifetimes of high-latitude artificial satellites, shapes the orbital architecture of irregular satellite systems and of asteroid families, drives the growth of cometary eccentricities, and protects — or destroys — bodies on inclined orbits in planetary systems. The timescale formula t_KL ~ (M/m₃)(a_out/a_in)³ P_in shows why the effect is so universal: it is a clock whose rate depends only on the hierarchy, and every hierarchical configuration with an inclined orbit carries it.

The modern renaissance came with exoplanets and gravitational-wave astronomy. The eccentric generalizations of the mechanism (the octupole-order flips, comprehensively reviewed by Naoz 2016) turn inclined triples into a migration channel for hot Jupiters (Wu & Murray 2003; Fabrycky & Tremaine 2007) and into a merger channel for compact-object triples whose final inspirals LISA will observe (Blaes, Lee & Socrates 2002). The monograph of Shevchenko (2017) collects the applications, and the historical review of Ito & Ohtsuka (2019) reconstructs the naming and the priority — including von Zeipel's role and the Japanese and Soviet schools.

For TRIVORTEX the relevance is structural. The conserved j_z collapses the problem to one integrable degree of freedom exactly as the Chaplygin integral reduces the vortex problem; the closed-form e_max is a Theorem-3.1-type sharp analytic benchmark that the numerics must hit; and the KL clock is the secular twin of the rotating choreography period. This study therefore anchors the secular celestial block of the program (TRX-01, TRX-10, TRX-11, TRX-12) — the same three-body stage on which the laser studies act.

## 2. Physical formulation

The system is a restricted hierarchical triple: the inner binary consists of a primary with GM_inner = 1 on a_in = 1 and a massless test particle; the outer companion m₃ moves on a circular orbit of radius a_out ≫ a_in (20 a_in in the secular model, 5 a_in in the direct validation). The instantaneous quadrupole disturbing potential is U = (G m₃/2a_out³)·(3(r·r̂₃)² − r²) — the l = 2 term of the expansion of the companion's potential in the small hierarchy parameter α = a_in/a_out; for a circular outer orbit the octupole (l = 3) term vanishes identically.

Averaging U over both orbital periods leaves an axisymmetric function ⟨U⟩(e, ω) that depends on the orientation of the ellipse only through the argument of pericentre. The z-component of the angular momentum, j_z = √(1 − e²)·cos i, is conserved exactly, so the secular problem collapses to one Hamiltonian degree of freedom on the fixed-j_z manifold: eccentricity grows exactly when the inclination falls, the two being locked together by j_z. The rate of the clock is set by C₂ = (3/8)(m₃/M)(a_in/a_out)³·n_in, the inverse of the KL timescale.

| Parameter | Value | Meaning |
|---|---|---|
| Units | GM_inner = 1, a_in = 1, n_in = 1 | the inner binary defines length and time |
| e₀, ω₀ | 0.001, π/2 (90°) | initially circular orbit; ω₀ at the libration centre |
| i₀ | {60°, 70°} | headline inclinations, both above i_crit = 39.23° |
| m₃/M | 1.0 (secular scan), 0.5 (direct) | outer-to-inner mass ratio |
| a_out | 20 a_in (secular), 5 a_in (direct) | hierarchy separator α = a_in/a_out |
| Spline grid | 160 × 180 (e × ω), 240-point orbit quadrature | tabulation of the averaged potential ⟨U⟩ |
| Secular integrator | DOP853, rtol 1e-8, atol 1e-9 | canonical spline flow, 3 KL cycles per run |
| Direct integrator | DOP853, rtol = atol = 1e-11 | full 3-D restricted problem, 200 outer periods |

## 3. Mathematical model

Start from the companion's potential expanded in a Legendre series in the small hierarchy parameter α = a_in/a_out. The monopole (l = 0) term only shifts the inner orbit's energy; the quadrupole (l = 2) term, U ∝ (3(r·r̂₃)² − r²)/2a_out³, is the first anisotropic contribution and the one that survives averaging; for a circular outer orbit the octupole (l = 3) term vanishes identically, and the next surviving term, the hexadecapole (l = 4), is smaller by α². The inner-orbit average is performed in the script by a 240-point quadrature in true anomaly with weights proportional to r² — the exact Kepler time-weight dt ∝ r² df — rather than by quoting the memorized analytic average.

Averaging the quadrupole term over the outer circular orbit leaves an axisymmetric potential ⟨U⟩(e, ω). Because ⟨U⟩ does not depend on the longitude of the node, the z-component of angular momentum j_z = √(1 − e²)·cos i is conserved exactly, and the dynamics collapse to one Hamiltonian degree of freedom (e, ω) on the fixed-j_z manifold. The canonical equations (E2) with the rate scale C₂ (E5) are then integrated numerically; since ⟨U⟩ has period π in ω, the phase is folded into [0, π), which keeps the integrator fast and the phase bounded.

The maximum eccentricity follows from the geometry of the fixed points. For an initially circular inner orbit (j_z = cos i₀) eccentricity growth is possible only above the critical inclination i_crit = arccos√(3/5) ≈ 39.23°, where the libration island about ω = π/2 opens. At the eccentricity maximum the condition ė = 0 forces ∂⟨U⟩/∂ω = 0, i.e. ω = π/2, and the inclination simultaneously reaches its minimum (j_z links e and i monotonically); the closed form (E4), e_max = √(1 − (5/3)cos²i₀), follows. The flow thus predicts not only the amplitude but also the antiphase geometry of the exchange — the property verified in fig02.

**Notation**

| Symbol | Meaning |
|---|---|
| e | eccentricity of the inner (test-particle) orbit |
| i | inclination of the inner orbit to the outer orbital plane |
| ω | argument of pericentre of the inner orbit |
| e₀, ω₀, i₀ | initial values: 0.001, π/2, {60°, 70°} |
| j = √(1 − e²) | dimensionless angular momentum of the inner orbit (L = 1) |
| j_z | conserved z-component, j_z = √(1 − e²)·cos i |
| m₃/M | perturber-to-inner mass ratio |
| a_in, a_out | inner and outer semi-major axes (a_in = 1) |
| n_in | inner mean motion (n_in = 1) |
| C₂ | KL rate, C₂ = (3/8)(m₃/M)(a_in/a_out)³·n_in |
| ⟨U⟩ | double-averaged quadrupole potential (spline-tabulated) |

**(E1)** Double-averaged quadrupole disturbing potential (built numerically by orbit quadrature; units G m₃/2a_out³).

$$\langle U\rangle(e,\omega) = \left\langle \frac{G m_3}{2 a_{\rm out}^3}\,\big(3(\mathbf{r}\cdot\hat{\mathbf{r}}_3)^2 - \mathbf{r}^2\big) \right\rangle_{\!\text{inner orbit}}$$

**(E2)** Canonical Hamiltonian flow on the fixed-j_z manifold (L = 1), rates scaled by C₂.

$$\dot{e} = C_2\,\frac{j}{e}\,\frac{\partial \langle U\rangle}{\partial \omega}, \qquad \dot{\omega} = -\,C_2\,\frac{j}{e}\,\frac{\partial \langle U\rangle}{\partial e}, \qquad j = \sqrt{1 - e^2}$$

**(E3)** Conserved z-component of the orbital angular momentum — the invariant that locks e and i.

$$j_z = \sqrt{1 - e^2}\,\cos i = \mathrm{const}$$

**(E4)** Analytic maximum eccentricity for an initially circular orbit; the exchange turns on above the Kozai angle.

$$e_{\max} = \sqrt{1 - \tfrac{5}{3}\cos^2 i_0}, \qquad i_{\rm crit} = \arccos\sqrt{\tfrac{3}{5}} \approx 39.23^\circ$$

**(E5)** KL timescale: the cycle period scales as 1/m₃ (halves when the perturber mass doubles).

$$C_2 = \tfrac{3}{8}\,\frac{m_3}{M}\left(\frac{a_{\rm in}}{a_{\rm out}}\right)^{\!3} n_{\rm in}, \qquad t_{\rm KL} \sim \frac{1}{C_2}$$

## 4. Connection to the TRIVORTEX framework

The mapping to the TRIVORTEX vortex framework is structural. The conserved j_z pins the whole eccentricity–inclination family to a one-dimensional manifold exactly as the Chaplygin integral pins the vortex orbits; the closed-form e_max = √(1 − (5/3)cos²i₀) plays the role of a Theorem-3.1-type sharp analytic benchmark that the numerics are obliged to hit; and the KL clock with period ~ 1/C₂ is the secular twin of the rotating choreography period. Methodologically the study is the program's flagship of the built-not-memorized philosophy: the averaged Hamiltonian is constructed numerically and the analytic law emerges as an output-level target — the same discipline the vortex studies apply to Chaplygin-reduced flows.

| Quantity in this study | TRIVORTEX analog | Comment |
|---|---|---|
| Hierarchical triple (test particle + companion) | three bodies with separated scales | the celestial three-body problem |
| Conserved j_z = √(1 − e²)·cos i | Chaplygin-type topological invariant | an integral that pins the orbit family |
| e_max = √(1 − (5/3)cos²i₀) | closed form of Theorem 3.1 | a sharp analytic benchmark for the numerics |
| KL clock, t_KL ~ 1/C₂ | choreography period T | secular timekeeping of the triad |
| Spline-built averaged Hamiltonian ⟨U⟩ | numerically constructed vortex Hamiltonian | both flows are driven by tabulated, not memorized, potentials |

## 5. Numerical method

The averaged potential is tabulated on a 160 × 180 grid in (e, ω) with e ∈ [0.0001, 0.999] and ω ∈ [0, 2π]; each node is evaluated by the 240-point Kepler-time-weighted quadrature described in the derivation. A bicubic RectBivariateSpline (kx = ky = 3) then provides ⟨U⟩ and its exact spline derivatives ∂⟨U⟩/∂e and ∂⟨U⟩/∂ω — the Hamiltonian machine used everywhere downstream. No analytic KL formula is written anywhere in the secular pipeline.

The canonical flow is integrated with DOP853 (rtol 1e-8, atol 1e-9, max_step T/1500) over a span covering three model KL cycles, sampled at 3000 points per run. The KL period is measured as the mean spacing of successive local maxima of e above 0.7·max(e) — a robust estimator insensitive to the small-amplitude wiggles near e ≈ 0. The mass-scaling check reruns the flow at m₃/M = 2 and compares P(2m₃)/P(m₃) against 0.5 with a 3% band; the figure sweep extends the clock to m₃/M ∈ {0.5, 1, 2, 4}.

Validation is fully independent: the direct run integrates the full three-dimensional restricted problem — the test particle feels both the primary and the companion moving on its circular orbit — with DOP853 at rtol = atol = 1e-11, a 60000-step cap and 40000 dense-output samples over 200 outer periods (m₃/M = 0.5, a_out = 5 a_in). The osculating eccentricity is computed pointwise from the Laplace–Runge–Lenz vector and smoothed with a moving average over one outer period; the maximum of the smoothed curve is the reported quantity. The secular and direct models share no code path beyond the integrator, so their agreement is a genuine cross-validation.

## 6. Results and analysis

### fig01 kl landscape

![Landscape of the quadrupole Kozai–Lidov problem: (a) geometry of the hierarchical triple, (b) the analytic Kozai landscape e_max(i₀).](../figures/fig01_kl_landscape.png)

*Landscape of the quadrupole Kozai–Lidov problem: (a) geometry of the hierarchical triple, (b) the analytic Kozai landscape e_max(i₀).*
Panel (a) shows the inner orbit at e_max = 0.7638 inclined by i₀ = 60° and projected on the outer-orbit plane, with the companion orbit at a_out = 20 a_in dashed and not to scale; panel (b) traces e_max(i₀) = √(1 − (5/3)cos²i₀), shades the sub-critical band where no exchange occurs, and marks the study points 0.7638 (60°) and 0.8972 (70°).

### fig02 kl exchange

![Headline result — the eccentricity–inclination exchange of the secular spline flow.](../figures/fig02_kl_exchange.png)

*Headline result — the eccentricity–inclination exchange of the secular spline flow.*
Left: e(t) cycles to 0.763733 (i₀ = 60°) and 0.897238 (70°) against the dashed analytic envelopes, with j_z = 0.500000 and 0.342020 conserved; right: over two cycles at 60° eccentricity peaks exactly when the inclination dips to 39.23° = i_crit — the antiphase exchange.

### fig03 kl sweeps

![Parameter sweeps: validation of the Kozai landscape e_max(i₀) and scaling of the KL clock with the perturber mass.](../figures/fig03_kl_sweeps.png)

*Parameter sweeps: validation of the Kozai landscape e_max(i₀) and scaling of the KL clock with the perturber mass.*
Across 12 inclinations from 30° to 80° the spline flow matches the analytic landscape to 1.128×10⁻⁵ (the 40° run needs an 8× longer span: the KL period diverges at i_crit), while below i_crit eccentricity stays at e₀ = 0.001; the mass sweep over m₃/M ∈ {0.5, 1, 2, 4} confirms P ∝ 1/m₃ with a P·m₃ spread of 4.29%.

### fig04 kl dynamics

![Dynamics on the fixed-j_z manifold: phase portrait and the residual of the tabulated Hamiltonian.](../figures/fig04_kl_dynamics.png)

*Dynamics on the fixed-j_z manifold: phase portrait and the residual of the tabulated Hamiltonian.*
The phase portrait (ω mod π, e) shows ω librating about π/2 while e cycles between 0.001 and 0.763733 (60°) / 0.897238 (70°); the Hamiltonian residual along the 60° trajectory stays below 1.33×10⁻⁵ — the cubic-spline representation error on the 160 × 180 grid, not integrator error (DOP853, rtol 1e-8).

**Analytic maxima.** The headline checks compare the spline-flow maxima against the closed-form targets: e_max = 0.7637326 measured versus 0.7637626 analytic at i₀ = 60° (deviation 3.0×10⁻⁵) and 0.8972376 versus 0.8972386 at 70° (deviation 9.1×10⁻⁷) — both far inside the 2×10⁻³ acceptance band. The conserved quantities j_z = 0.500000 (60°) and 0.342020 (70°) stay constant along the flow, and the recorded eccentricity series returns exactly to e₀ = 0.001 at every cycle minimum (series range 0.001 … 0.76372882 in the JSON protocol).

**The exchange geometry.** fig02 shows the antiphase lock predicted by the derivation: eccentricity peaks exactly when the inclination dips to 39.2316° — numerically indistinguishable from i_crit = arccos√(3/5) — and the argument of pericentre librates about π/2 (fig04). The phase portraits of the two headline runs collapse onto the fixed-j_z manifolds j_z = 0.5 and j_z = 0.342020, the eccentricity–inclination ledger of the scheme.

**Landscape and clock.** The 12-point inclination sweep from 30° to 80° reproduces the analytic landscape with a maximum deviation of 1.128×10⁻⁵ over the active range; below i_crit (30°, 35°, 38°) eccentricity stays at e₀ = 0.001, and the 40° run needs an 8× longer span because the KL period diverges at the threshold (40°: 0.14818829 simulated versus 0.14818857 analytic; 45°: 0.40824826 versus 0.40824829; 80°: 0.97455930 versus 0.97454802). The clock scales as 1/m₃: P(2m₃)/P(m₃) = 0.481 against the ideal 0.5 (3% band; P(m₃) = 103829.39, P(2m₃) = 49944.15 in units of 1/n_in), and across m₃/M ∈ {0.5, 1, 2, 4} the product P·m₃ spreads only 4.29% (221991.0, 111355.7, 54927.46, 28661.83).

**Direct validation and error budget.** The independent 3-D run gives a smoothed maximum eccentricity 0.7423 versus 0.7638 analytic — a −2.8% deviation, inside the 8% gate and consistent with the hexadecapole truncation plus the non-test-particle mass ratio m₃/M = 0.5 at α = 0.2. The tabulated Hamiltonian drifts by at most 1.33×10⁻⁵ along the flow — the cubic-spline representation error on the 160 × 180 grid, deliberately separated from integrator error (DOP853, rtol 1e-8). Every number in this paragraph is stored in the JSON protocol with target, tolerance and pass flag.

### Verification summary

| Check | Recorded value | Target | Tolerance | Pass |
|---|---|---|---|---|
| `e_max_i0_60` | 0.763733 | 0.763763 | 0.002 | yes |
| `e_max_i0_70` | 0.897238 | 0.897239 | 0.002 | yes |
| `kl_period_halves_with_m3` | 0.481021 | 0.5 | 0.03 | yes |
| `direct_3d_emax_validation` | 1 | 1 | 1e-12 | yes |

*(status: **PASS**, mode: full)*

## 7. Discussion

The model is deliberately minimal: quadrupole order, test-particle inner orbit, circular outer orbit, no dissipation. Within these assumptions the conclusions are exact statements about the averaged equations, not simulations of a particular system. The natural extensions each preserve the verification style: the octupole term for eccentric companions (the eccentric Kozai–Lidov effect with orbit flips — Naoz 2016), the hexadecapole correction, comparable masses and radiation backreaction (pursued in TRX-11), and tidal friction coupling the KL cycles to orbital shrinkage in the hot-Jupiter channel.

The −2.8% direct-run deviation is not a defect but a measurement of the truncation: the direct problem at m₃/M = 0.5 and α = a_in/a_out = 0.2 is only moderately hierarchical, and higher-order multipoles plus the breakdown of the test-particle idealization push the true maximum eccentricity below the quadrupole formula. That a machine built from Newtonian gravity and geometry alone — with no KL formula inside — lands within 2.8% of a substantially non-idealized direct integration is the strongest statement of the study. The remaining error-budget line, the 1.33×10⁻⁵ Hamiltonian residual, is a property of the spline representation and could be pushed lower by refining the 160 × 180 grid, at quadratic cost in tabulation time.

Within the program this study anchors the secular celestial block: TRX-01 treats the same restricted problem at the libration points instead of secular cycles, TRX-11 integrates the comparable-mass three-body problem exactly and radiates, and TRX-12 stations a laser sailcraft at the L4 point of the same celestial stage. The laser link is direct: KL cycles are the accepted channel-forming mechanism for LISA-class compact-object mergers (Blaes, Lee & Socrates 2002), and laser ranging of binary and triple asteroids reads out exactly the orbital elements this study oscillates.

## 8. Conclusions

1. The doubly-averaged quadrupole Hamiltonian, built numerically (240-point orbit quadrature, 160 × 180 spline grid), reproduces the analytic maxima e_max = 0.763763 (i₀ = 60°) and 0.897239 (70°) with deviations 3.0×10⁻⁵ and 9.1×10⁻⁷ — far inside the 2×10⁻³ tolerance.
2. The eccentricity–inclination exchange is exactly antiphase: e peaks when i dips to i_crit = arccos√(3/5) = 39.23°, with j_z = 0.500000 (60°) and 0.342020 (70°) conserved along the flow.
3. The Kozai landscape e_max(i₀) is validated over 12 inclinations from 30° to 80° with a maximum deviation of 1.128×10⁻⁵ over the active range; below i_crit eccentricity stays at e₀ = 0.001, and the KL period diverges at the threshold (the 40° run needs an 8× longer span).
4. The KL clock obeys P ∝ 1/m₃: the measured ratio P(2m₃)/P(m₃) = 0.481 (ideal 0.5, 3% band) and the product P·m₃ spreads only 4.29% across m₃/M ∈ {0.5, 1, 2, 4}.
5. An independent direct integration of the full 3-D restricted problem (m₃/M = 0.5, a_out = 5 a_in, 200 outer orbits) gives a smoothed maximum eccentricity 0.7423 versus 0.7638 — a −2.8% deviation consistent with the hexadecapole truncation and the finite mass ratio.
6. The tabulated Hamiltonian is conserved to 1.33×10⁻⁵ along the flow — the honest error budget of the spline representation, reported alongside every check in the JSON protocol.

## 9. References

1. Kozai, Y. (1962). *Secular perturbations of asteroids with high inclination and eccentricity.* Astronomical Journal 67, 591–598.
2. Lidov, M. L. (1962). *The evolution of orbits of artificial satellites of planets under the action of gravitational perturbations of external bodies.* Planetary and Space Science 9, 719–759.
3. von Zeipel, H. (1910). *Sur les perturbations séculaires des orbites astronomiques.* Astronomische Nachrichten 183, 345–362.
4. Naoz, S. (2016). *The eccentric Kozai–Lidov effect and beyond.* Annual Review of Astronomy and Astrophysics 54, 341–396.
5. Shevchenko, I. I. (2017). *The Lidov–Kozai Effect — Applications in Celestial Mechanics.* Springer, Astrophysics and Space Science Library 441.
6. Ito, T., Ohtsuka, K. (2019). *The Lidov–Kozai oscillation and Hirayama families.* Monographic Notices of the National Astronomical Observatory of Japan 1, 1–168.
7. Murray, C. D., Dermott, S. F. (1999). *Solar System Dynamics.* Cambridge University Press.
8. Wu, Y., Murray, N. W. (2003). *Planet migration and binary companions: the case of HD 80606.* The Astrophysical Journal 589, 605–614.
9. Fabrycky, D., Tremaine, S. (2007). *Shrinking binary and planetary orbits by the Kozai cycle with tidal friction.* The Astrophysical Journal 669, 1298–1315.
10. Blaes, O., Lee, M. H., Socrates, A. (2002). *The Kozai mechanism and the evolution of binary supermassive black holes.* The Astrophysical Journal 578, 775–786.

### BibTeX

```bibtex
@article{kozai1962,
  author  = {Kozai, Yoshihide},
  title   = {Secular perturbations of asteroids with high inclination and eccentricity},
  journal = {Astronomical Journal},
  year    = {1962}, volume = {67}, pages = {591--598}}

@article{lidov1962,
  author  = {Lidov, Mikhail L.},
  title   = {The evolution of orbits of artificial satellites of planets under the action of gravitational perturbations of external bodies},
  journal = {Planetary and Space Science},
  year    = {1962}, volume = {9}, pages = {719--759}}

@article{naoz2016,
  author  = {Naoz, Smadar},
  title   = {The eccentric Kozai--Lidov effect and beyond},
  journal = {Annual Review of Astronomy and Astrophysics},
  year    = {2016}, volume = {54}, pages = {341--396}}

@book{shevchenko2017,
  author    = {Shevchenko, Ivan I.},
  title     = {The Lidov--Kozai Effect: Applications in Celestial Mechanics},
  publisher = {Springer}, series = {Astrophysics and Space Science Library 441}, year = {2017}}

@article{ito2019,
  author  = {Ito, Takashi and Ohtsuka, Katsuhito},
  title   = {The Lidov--Kozai oscillation and Hirayama families},
  journal = {Monographic Notices of the National Astronomical Observatory of Japan},
  year    = {2019}, volume = {1}, pages = {1--168}}
```

## Appendix A. Parameter table

| Symbol | Value | Role |
|---|---|---|
| e₀ | 0.001 | initial eccentricity (near-circular) |
| ω₀ | π/2 | initial argument of pericentre |
| i₀ | {60°, 70°} | initial inclinations of the headline runs |
| m₃/M (secular) | 1.0 headline; {0.5, 1, 2, 4} clock sweep | perturber mass ratio |
| a_out (secular) | 20 a_in | outer orbit radius, hierarchy α = 0.05 |
| secular grid | 160 × 180 (e × ω) | spline tabulation of ⟨U⟩ |
| orbit quadrature | 240 points in true anomaly, weights ∝ r² | inner-orbit Kepler-time average |
| secular integrator | DOP853, rtol 1e-8, atol 1e-9, max_step T/1500 | canonical spline flow, 3 KL cycles |
| direct run | m₃/M = 0.5, a_out = 5 a_in, 200 outer periods | full 3-D restricted problem |
| direct integrator | DOP853, rtol = atol = 1e-11, 60000-step cap, 40000 samples | osculating e smoothed over one outer period |
| runtime | 64.6 s full, < 20 s smoke | reference machine |

## Appendix B. Reproduction

```bash
python3 research/TRX-10-kozai-lidov/code/trx10_kozai_lidov.py --smoke     # < 20 s
python3 research/TRX-10-kozai-lidov/code/trx10_kozai_lidov.py              # full, 64.6 s
python3 research/TRX-10-kozai-lidov/code/trx10_kozai_lidov.py --figures   # + 300-DPI figures
```

Full runtime on the reference machine: 64.6 s; smoke mode completes in under 20 seconds and is exercised by the repository CI.

## Appendix C. Environment

Python ≥ 3.11, numpy ≥ 2.0, scipy ≥ 1.14, matplotlib ≥ 3.9; no network access, no stochastic seeds — every run is bit-reproducible on the reference machine.
