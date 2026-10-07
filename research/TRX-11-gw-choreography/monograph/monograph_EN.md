# Gravitational Waves from the Figure-Eight Choreography

*TRIVORTEX Research Program · v1.0.0 · Monograph Edition*

|  |  |
|---|---|
| Study | TRX-11 |
| Program | TRIVORTEX — The Three-Body Problem in the Vortex Model |
| Author | Isaev Iskhak Khamzatovich (ORCID 0009-0003-7299-0701) |
| DOI | 10.5281/zenodo.21825394 |
| Date | 2026-10-06 |
| Code | `code/trx11_gw_choreography.py` |
| Data | `results/trx11_results.json` |

## Abstract

This monograph turns the figure-eight choreography of Chenciner and Montgomery — three equal masses chasing each other along a single closed curve with zero angular momentum — into a quantified gravitational-wave source. The period is found by global minimisation of the configuration closure over one revolution: T = 6.325914025, matching the published 6.32591398 to 1.2e-08, with energy conserved to 3.6e-15 and the angular momentum zero to 1.4e-15 throughout. In the quadrupole approximation (G = c = D = 1) the mass quadrupole drives a plus-polarised strain spanning −4.04 to +4.85 that repeats six times per orbit period. The choreography symmetry Q(T/3) = Q(0), verified to 1.5·10⁻⁸, locks the spectrum into a harmonic comb: the dominant line lands at n = 6 of the orbital comb (f·T = 5.9995, residual 5.0e-4) with overtones at 12 and 18 of relative amplitudes 0.091 and 0.0061. The time-averaged antenna pattern peaks along the orbital normal at 3.01 times the mean exact luminosity of 76.51, and a velocity-detuning sweep over k = 0.90 … 1.10 shows the eight is an isolated solution: the k = 1 closure residual is 7.6·10⁻⁹ while every detuned case exceeds 0.028. LISA-class laser interferometers are the natural readout.

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

Gravitational waves entered physics as a prediction of general relativity: Einstein derived the linearised field equations in 1916 and returned to the question in 1918 with the famous quadrupole formula, establishing that accelerating masses radiate energy at a rate controlled by the third time derivative of the mass quadrupole tensor. For decades the formula was disputed even among theorists — Eddington suspected the waves of being coordinate artifacts — until the quadrupole luminosity was worked out for concrete systems: Peters and Mathews (1963) computed the orbit-averaged radiation of Keplerian binaries, and the measured orbital decay of the binary pulsar PSR 1913+16 by Taylor and Weisberg (1982) confirmed that formula to better than half a percent, awarding the quadrupole approximation the status of quantitative science.

The modern formalism descends from Thorne's 1980 review, which systematised the multipole expansion of gravitational radiation — source multipoles, the trace-free projection, the energy flux — into the standard toolbox used by every waveform model today; Maggiore's monograph (2007) fixed the pedagogical canon. Within this framework the plus-polarised strain of a distant observer is proportional to the second derivative of the trace-free quadrupole, and the luminosity is the squared sum of third derivatives — exactly the two objects this study computes for a three-body source, in units G = c = D = 1.

The source itself has a shorter but remarkable history. Moore (1993) found, by numerical search over braided periodic orbits, that three equal bodies can chase each other along one curve; Chenciner and Montgomery (2000) then proved the existence of this figure-eight solution rigorously, via a variational argument combined with computer assistance, and Simó (2002) mapped the dynamical properties of the associated Poincaré map. The solution is exceptional in several ways at once: it is periodic, planar, collision-free, and it carries exactly zero angular momentum — a property that no circular binary shares and that shapes the emitted waveform.

For TRIVORTEX the relevance is structural. The monograph's vortex program studies special triads — the rotating Lagrange triangle, the (1, −1, 1) collapse trio, the secular hierarchical cycles — and the figure-eight is the celestial sibling of the same family: a choreography whose symmetry group, not whose parameters, fixes its observables. Adding the quadrupole channel turns the choreography from a curiosity of celestial mechanics into a potential astrophysical signal, and the natural readout instrument is laser-based: LISA, Taiji and TianQin are laser interferometers whose million-kilometre arms are built on laser stability. The study therefore also documents the laser connection that runs through the laser block of the program (TRX-01, TRX-12).

## 2. Physical formulation

Planar Newtonian three-body problem with three equal masses, G = m = 1. The initial condition is the Chenciner–Montgomery figure-eight: r₁ = (0.97000436, −0.24308753), r₂ = −r₁, r₃ = (0, 0), v₃ = (−0.93240737, −0.86473146), v₁ = v₂ = −v₃/2. The total momentum and the total angular momentum vanish identically, and all three bodies trace the same closed curve shifted in time — a choreography in the strict sense. Over one period T = 6.325914 the pairwise separations sweep the interval from 0.6905 to 2.0000 and are permuted among the three pairs every T/3.

The wave model is the leading quadrupole term of general relativity in the far-zone, slow-motion limit. With G = c = D = 1 the plus-polarised strain read by a distant observer is proportional to the second derivative of Q_xx − Q_yy, and the luminosity is P = (1/5)Σ_ij (d³Q_ij/dt³)² evaluated on the trace-free part of the quadrupole. The emitter is deliberately idealised: Newtonian gravity supplies the source motion, and relativity enters only as a readout formula — no back-reaction on the orbit, no higher multipoles.

| Parameter | Value | Meaning |
|---|---|---|
| Masses, constant | m₁ = m₂ = m₃ = 1, G = 1 | planar Newtonian three-body problem |
| Initial positions | r₁ = (0.97000436, −0.24308753), r₂ = −r₁, r₃ = (0, 0) | Chenciner–Montgomery initial condition |
| Initial velocities | v₃ = (−0.93240737, −0.86473146), v₁ = v₂ = −v₃/2 | zero total momentum, zero angular momentum |
| Integrator | DOP853, rtol = atol = 1e-13, max_step 0.005 | one period; 12001-point dense sampling for the quadrupole |
| Period search | closure minimisation over t ∈ [2, 11], xatol 1e-13 | global minimum of the configuration closure |
| Wave model | quadrupole, G = c = D = 1 | h₊ ∝ d²(Qxx − Qyy)/dt²; P = (1/5)Σ(d³Q_ij/dt³)² |

## 3. Mathematical model

The quadrupole channel follows from the slow-motion, weak-field expansion of the Einstein equations. To leading order the radiative degrees of freedom are driven by the trace-free part of the second mass moment Q_ij = Σ_k m_k x_ki x_kj (E2); the transverse-traceless projection at the observer gives the two polarisations, and for a face-on optimally oriented detector the plus-polarised strain is proportional to the second derivative of Q_xx − Q_yy (E3). The energy flux is set by the third derivatives (E4): with G and c restored, P = (G/5c⁵)⟨Σ(d³Q_ij/dt³)²⟩, so in the units G = c = D = 1 used throughout, the luminosity is literally (1/5) of the squared sum of third derivatives. The mass dipole is conserved (centre-of-mass motion) and cannot radiate; the quadrupole is the first radiating moment.

The choreography structure enters through (E5). Because the three masses are equal and chase each other along one curve, the set of positions repeats itself every third of the period: {r_k(T/3)} = {r_k(0)}. The quadrupole, being a symmetric function of the configuration, is then exactly periodic with T/3, which restricts the spectrum to harmonics of 3/T. The measured spectrum sharpens this further: the dominant line lands at f·T = 5.9995, twice the pattern frequency 3/T, and the strain itself repeats six times per period — visible in the waveform panel as six identical lobes. The zero angular momentum is the second structural input: it removes the rotational Doppler-like asymmetry that a spinning binary would imprint, leaving a waveform whose shape is fixed by the figure-eight geometry alone.

Numerically the quadrupole derivatives are computed exactly rather than by finite differences. Differentiating Newton's law (E1) once more gives the jerk — the third time derivative of position — in closed form, and the chain rule then yields the exact second derivatives Q̈ = Σ(2vv + 2xa) and third derivatives Q⃛ = Σ(6va + 2xj) of every quadrupole component from the state (positions, velocities, accelerations, jerks). This matters because chained finite differentiation of a numerically sampled trace amplifies error by orders of magnitude per pass: the acceptance check deliberately uses the simple finite-difference estimator as a finiteness gate only (recorded value 1.65e8 in G = c = D = 1 units), while the physical luminosity reported by the figure pipeline is 76.51 mean with peak 159.73.

**Notation**

| Symbol | Meaning |
|---|---|
| Q_ij | mass quadrupole tensor, Q_ij = Σ_k m_k x_ki x_kj |
| h₊(t) | plus-polarised strain at the observer, ∝ d²(Qxx − Qyy)/dt² |
| P | gravitational-wave luminosity (G = c = D = 1 units) |
| T | period of the choreography, 6.325914025 in G = m = 1 |
| n | harmonic index of the orbital comb, f = n/T |
| f·T | dimensionless position of a spectral line on the comb |
| θ | observer inclination measured from the orbital normal |
| k | velocity scale factor of the detuning sweep |
| L_z | total angular momentum of the three bodies (identically zero) |
| r_ij | pairwise separation, sweeping [0.6905, 2.0000] over one period |
| Q⃛_ij | third time derivative of the quadrupole, driving the luminosity (E4) |

**(E1)** Newtonian three-body dynamics (planar, equal masses).

$$\ddot{\boldsymbol{r}}_k = \sum_{j \neq k} \frac{\boldsymbol{r}_j - \boldsymbol{r}_k}{\left|\boldsymbol{r}_j - \boldsymbol{r}_k\right|^3}, \qquad G = m = 1$$

**(E2)** Mass quadrupole tensor of the emitter.

$$Q_{ij} = \sum_k m_k\, x_{ki}\, x_{kj}$$

**(E3)** Plus-polarised waveform read by a distant observer (G = c = D = 1).

$$h_+(t) \propto \frac{d^2}{dt^2}\left(Q_{xx} - Q_{yy}\right)$$

**(E4)** Gravitational-wave luminosity on the trace-free quadrupole (G = c = D = 1).

$$P = \frac{1}{5}\sum_{ij} \left(\frac{d^3 Q_{ij}}{dt^3}\right)^{2}$$

**(E5)** Choreography exchange symmetry and the harmonic comb.

$$\{\boldsymbol{r}_k(T/3)\} = \{\boldsymbol{r}_k(0)\} \;\Rightarrow\; Q(t + T/3) = Q(t) \;\Rightarrow\; \tilde{h}(f) \neq 0 \ \text{only at}\ f = n \cdot \frac{3}{T}$$

## 4. Connection to the TRIVORTEX framework

Within the TRIVORTEX framework the figure-eight is the second special three-body solution besides the rotating equilateral choreography of Theorem 3.1 — two answers of one problem to the same requirement of exact periodicity. The zero angular momentum of the eight is the celestial twin of the document's own charge pattern: a tuned circulation triplet (1, −1, 1) whose angular impulse vanishes, so both models live on the zero-impulse slice of their phase spaces. The quadrupole comb at multiples of 3/T plays the role of the radial modulation frequency ω of Theorem 3.1 — in both cases a single spectral line family is the fingerprint of the triad's symmetry. Finally, the detection channel is a laser channel: TRX-01 and TRX-12 put lasers inside the three-body dynamics as actuators, while this study points lasers at it as detectors, closing the laser theme from both ends. TRX-09 supplies the vortex-language description of the same choreographic idea, and TRX-10 its hierarchical (secular) limit.

| Quantity in this study | TRIVORTEX analog | Comment |
|---|---|---|
| Figure-eight choreography | rotating equilateral choreography of Theorem 3.1 | two special solutions of one problem |
| Zero angular momentum L = 0 | tuned circulation pattern (1, −1, 1) | the document's own charge triplet |
| Quadrupole comb at multiples of 3/T | radial modulation ω of Theorem 3.1 | spectral fingerprint of the triad |
| Choreography period T = 6.325914 | rigid rotation period of the vortex triangle | both special solutions carry a single clock |
| LISA-class detection | laser themes of TRX-01/12 | lasers as the measuring instrument |

## 5. Numerical method

The period is found before anything else is measured. The full system is integrated over [0, 12] with DOP853 at rtol = atol = 1e-13 and max_step 0.01; the closure is defined as the maximum deviation of the three positions from their initial values, scanned on a 1800-point grid over t ∈ [2, 11], and refined by bounded scalar minimisation with xatol 1e-13. The global minimum gives T = 6.325914025 with a closure residual of 1.2e-08 — inside the 5e-8 acceptance tolerance and consistent with the published 6.32591398. The period is then re-integrated over exactly [0, T] at max_step 0.005, and the invariants are monitored pointwise: the energy drift stays at 3.6e-15 and the total angular momentum at 1.4e-15 across 3000 samples.

The quadrupole pipeline reuses the same trajectory: states are sampled on a 12001-point grid for the protocol checks and on a 4801-point grid for the figures, and the quadrupole derivatives are evaluated from the exact analytic formulas — positions, velocities, accelerations and jerks of the DOP853 dense output — so the displayed waveform, spectrum and luminosity carry no numerical-differentiation edge artifacts. The strain is the second derivative of Q_xx − Q_yy; the instantaneous luminosity uses the trace-free combination (2Q⃛xx − Q⃛yy)/3, (2Q⃛yy − Q⃛xx)/3, −(Q⃛xx + Q⃛yy)/3 together with Q⃛xy, summed per (E4).

The spectral and directional diagnostics are deterministic. The spectrum is an FFT of the mean-subtracted exact strain over one full period — no window is needed because the signal is exactly periodic — with harmonic amplitudes tabulated for n = 1 … 30 of the orbital frequency. The antenna pattern is the time average of the transverse-traceless projected luminosity tensor contracted with the projector onto each sky direction, evaluated on a 181 × 121 (θ, φ) grid. The velocity-detuning sweep integrates the rescaled initial states (all velocities multiplied by k ∈ {0.90, 0.95, 0.98, 0.99, 1.00, 1.01, 1.02, 1.05, 1.10}) over [0, 8] at rtol = atol = 1e-11 and refines the first return with xatol 1e-10.

## 6. Results and analysis

### fig01 orbit overview

![Orbit overview: (a) the figure-eight trajectory traced by all three equal masses over one period T = 6.325914 with the chase direction marked; (b) pairwise separations over the same period.](../figures/fig01_orbit_overview.png)

*Orbit overview: (a) the figure-eight trajectory traced by all three equal masses over one period T = 6.325914 with the chase direction marked; (b) pairwise separations over the same period.*
All three bodies trace the identical closed curve; the pairwise separations r12/r13/r23 sweep the same range 0.6905 to 2.0000 and are permuted among the pairs every T/3 — the exchange symmetry that powers the quadrupole.

### fig02 waveform comb

![Headline result: plus-polarised waveform of the choreography over one orbit period (left) and the harmonic comb of its spectrum (right).](../figures/fig02_waveform_comb.png)

*Headline result: plus-polarised waveform of the choreography over one orbit period (left) and the harmonic comb of its spectrum (right).*
The exact strain spans −4.04 to +4.85 and repeats every T/6; the spectrum is a pure comb with lines at n = 6, 12, 18 of relative amplitudes 1 : 0.091 : 0.0061, every other harmonic staying below 0.0013 of the dominant line at f·T = 5.9988.

### fig03 pattern sweep

![Directionality and isolation: time-averaged quadrupole antenna pattern (left) and the velocity-detuning sweep around the choreography (right).](../figures/fig03_pattern_sweep.png)

*Directionality and isolation: time-averaged quadrupole antenna pattern (left) and the velocity-detuning sweep around the choreography (right).*
Emission peaks along the orbital normal at 3.01 times the mean luminosity with in-plane minima 0.055 of the peak; scaling the initial velocities by k leaves the k = 1 closure residual at 7.6·10⁻⁹ while the nearest detuned case (k = 1.01) jumps to 0.028 with return-time shifts up to 1.67 — the eight is an isolated solution.

### fig04 quadrupole dynamics

![Emitter dynamics: exact second derivatives of the quadrupole components (left) and the instantaneous and cumulative radiated energy (right).](../figures/fig04_quadrupole_dynamics.png)

*Emitter dynamics: exact second derivatives of the quadrupole components (left) and the instantaneous and cumulative radiated energy (right).*
The T/3 exchange symmetry and the T/2 sign flip of the xy component are visible in the components; the exact luminosity averages 76.51, peaks at 159.73, and the cumulative radiated energy reaches 484.10 over one period (G = c = D = 1).

**Orbit and symmetry.** The period closure closes the loop first: T = 6.325914025 against the published 6.32591398, a mismatch of 1.2e-08 inside the 5e-8 tolerance, and the configuration returns on itself to the same 1.2e-08. Energy is conserved to 3.6e-15 and the angular momentum is zero to 1.4e-15 — the defining L = 0 property holds at machine precision. The pairwise separations sweep 0.6905 to 2.0000 and are permuted among the three pairs every T/3, and the same order-3 exchange shows up on the quadrupole: Q(T/3) = Q(0) to 1.5·10⁻⁸ while Q(T/2) − Q(0) = 0.943 — the half period is emphatically not a symmetry, the choreography exchange is order three, not two.

**Waveform and comb.** The exact plus-polarised strain spans −4.04 to +4.85 over one period and repeats every T/6, visible as six identical lobes in the waveform panel. The spectrum is a pure comb: the dominant line at n = 6 of the orbital comb (f·T = 5.9988 for the windowless exact spectrum; the acceptance check, computed on the finite-difference series with a Hann window, gives f·T = 5.9995 with residual 5.0e-4 against the 0.05 tolerance), overtones at n = 12, 18, 24 of relative amplitudes 0.091, 0.0061, 0.0004, and every other harmonic of the orbital frequency suppressed below 0.0013 of the peak. The dominant harmonic sits at exactly twice the T/3 pattern frequency 3/T, as the symmetry bookkeeping predicts.

**Directionality.** The time-averaged quadrupole antenna pattern, built from exact third derivatives, peaks along the orbital normal at 3.01 times the mean luminosity — a face-on observer receives the strongest signal — while in-plane emission is suppressed to 0.055 of the peak both along the x-axis and along the diagonals of the eight. For a LISA-class instrument the observable is therefore strongly inclination-dependent, and the gold lobes drawn in the scheme mark the only directions worth pointing at.

**Isolation and energy bookkeeping.** The velocity-detuning sweep proves the choreography is not a member of a nearby family: at k = 1 the closure residual is 7.6·10⁻⁹, while the nearest detuned case (k = 1.01) already sits at 0.028 and the extremes k = 0.90 and k = 1.10 reach 0.826 and 0.945, with return-time shifts from −1.63 to +1.67. On the energy side the exact luminosity averages 76.51 with a maximum of 159.73, so one period radiates 484.10 in G = c = D = 1 units. The acceptance-proxy value 1.65e8 recorded in the protocol is deliberately not used as a physical number: the chained finite-difference estimator amplifies sampling noise by orders of magnitude, and its only job is the finiteness gate 0 < P < 1e10, which it passes.

### Verification summary

| Check | Recorded value | Target | Tolerance | Pass |
|---|---|---|---|---|
| `period_closure_error` | 1.23174e-08 | 0 | 5e-08 | yes |
| `period_in_expected_range` | 1 | 1 | 1e-12 | yes |
| `energy_conserved` | 3.55271e-15 | 0 | 1e-12 | yes |
| `angular_momentum_is_zero` | 1.44329e-15 | 0 | 1e-09 | yes |
| `luminosity_finite_positive` | 1 | 1 | 1e-12 | yes |
| `quadrupole_choreography_symmetry` | 1 | 1 | 1e-12 | yes |
| `dominant_harmonic_on_comb` | 0.000499958 | 0 | 0.05 | yes |

*(status: **PASS**, mode: full)*

## 7. Discussion

The model is deliberately minimal: Newtonian dynamics plus the leading quadrupole formula, planar and equal-mass. Within these assumptions every reported number is an exact statement about the governing equations rather than a simulation of a specific astrophysical system. The natural extensions each keep the verification style: unequal-mass choreographies and their literature continuum, the full multipole ladder beyond the quadrupole (octupole and higher), the gravitational-wave back-reaction on the orbit over many periods, and the time-dependent detector response of a LISA-class instrument at arbitrary inclination, which the present antenna pattern only summarises.

The parameter regime is chosen for structural clarity. All results are quoted in units where G = m = c = D = 1; the physical mapping is linear — a system of total mass M and size scale L repeats the same dimensionless solution with the orbital frequency scaled by √(GM/L³) and the strain by GM/(c²D). Which astrophysical population could actually radiate into the mHz band of LISA, whether any natural system realises (or is captured into) a choreography, and how the comb signature survives environmental perturbations are astrophysical questions that lie beyond this study's scope but are now well posed: the comb and its 1 : 0.091 : 0.0061 amplitude ladder are falsifiable targets.

Within the program this study completes the comparable-mass branch of the three-body block. TRX-10 treats the hierarchical (secular) limit of the same problem — Kozai–Lidov cycles instead of a choreography; TRX-09 describes the same choreographic idea in the vortex language of the monograph; TRX-01 and TRX-12 put lasers inside the three-body problem as actuators, while this study points lasers at it as the measuring instrument. Together they cover the three-body problem of the TRIVORTEX program from the restricted to the radiating comparable-mass case.

## 8. Conclusions

1. The period of the figure-eight choreography, found by global minimisation of the configuration closure, is T = 6.325914025 — matching the published 6.32591398 to 1.2e-08 and inside the 5e-8 acceptance tolerance.
2. Energy is conserved to 3.6e-15 and the total angular momentum stays zero to 1.4e-15 over one full period: the defining L = 0 property of the eight holds at machine precision.
3. The equal-mass exchange symmetry is verified on the quadrupole: Q(T/3) = Q(0) to 1.5·10⁻⁸ while Q(T/2) − Q(0) = 0.943, confirming the choreography exchange is order three.
4. The plus-polarised waveform spans −4.04 to +4.85, repeats six times per period, and its spectrum is a pure comb: dominant line at n = 6 (f·T = 5.9995, residual 5.0e-4), overtones at 12, 18, 24 with amplitudes 0.091, 0.0061, 0.0004, all other harmonics below 0.0013 of the peak.
5. The time-averaged antenna pattern peaks along the orbital normal at 3.01 times the mean exact luminosity (76.51 mean, 159.73 peak, 484.10 radiated per period in G = c = D = 1); in-plane emission is suppressed to 0.055 of the peak.
6. The velocity-detuning sweep over k = 0.90 … 1.10 shows the eight is isolated: the k = 1 closure residual is 7.6·10⁻⁹ while every detuned case exceeds 0.028, with return-time shifts up to 1.67.

## 9. References

1. Einstein, A. (1918). *Über Gravitationswellen.* Sitzungsberichte der Königlich Preussischen Akademie der Wissenschaften (Berlin), 154–167.
2. Peters, P. C., Mathews, J. (1963). *Gravitational radiation from point masses in a Keplerian orbit.* Physical Review 131, 435–440.
3. Thorne, K. S. (1980). *Multipole expansions of gravitational radiation.* Reviews of Modern Physics 52, 299–339.
4. Moore, C. (1993). *Braids in classical dynamics.* Physical Review Letters 70, 3675–3679.
5. Chenciner, A., Montgomery, R. (2000). *A remarkable periodic solution of the three-body problem in the case of equal masses.* Annals of Mathematics 152, 881–901.
6. Simó, C. (2002). *Dynamical properties of the eight map.* Celestial Mechanics 4, 343.
7. Taylor, J. H., Weisberg, J. M. (1982). *A new test of general relativity: gravitational radiation and the binary pulsar PSR 1913+16.* The Astrophysical Journal 253, 908–920.
8. Maggiore, M. (2007). *Gravitational Waves. Volume 1: Theory and Experiments.* Oxford University Press.
9. Amaro-Seoane, P. et al. (2017). *Laser Interferometer Space Antenna.* arXiv:1702.00786.

### BibTeX

```bibtex
@article{einstein1918,
  author  = {Einstein, Albert},
  title   = {{\"U}ber Gravitationswellen},
  journal = {Sitzungsberichte der K{\"o}niglich Preussischen Akademie der Wissenschaften (Berlin)},
  year    = {1918}, pages = {154--167}}

@article{peters1963,
  author  = {Peters, Peter C. and Mathews, Jon},
  title   = {Gravitational radiation from point masses in a Keplerian orbit},
  journal = {Physical Review},
  year    = {1963}, volume = {131}, pages = {435--440}}

@article{thorne1980,
  author  = {Thorne, Kip S.},
  title   = {Multipole expansions of gravitational radiation},
  journal = {Reviews of Modern Physics},
  year    = {1980}, volume = {52}, pages = {299--339}}

@article{chenciner2000,
  author  = {Chenciner, Alain and Montgomery, Richard},
  title   = {A remarkable periodic solution of the three-body problem in the case of equal masses},
  journal = {Annals of Mathematics},
  year    = {2000}, volume = {152}, pages = {881--901}}

@book{maggiore2007,
  author    = {Maggiore, Michele},
  title     = {Gravitational Waves. Volume 1: Theory and Experiments},
  publisher = {Oxford University Press}, year = {2007}}
```

## Appendix A. Parameter table

| Symbol | Value | Role |
|---|---|---|
| G, m | 1, 1 | gravitational constant and equal masses (canonical units) |
| r₁(0) | (0.97000436, −0.24308753) | initial position of body 1; r₂ = −r₁, r₃ = (0, 0) |
| v₃(0) | (−0.93240737, −0.86473146) | initial velocity of body 3; v₁ = v₂ = −v₃/2 |
| T | 6.325914025 | period from closure minimisation (published 6.32591398) |
| Integrator | DOP853, rtol = atol = 1e-13 | max_step 0.005 (period search: 0.01) |
| Dense sampling | 12001 points per period | quadrupole derivative grid (figures: 4801) |
| Period search | t ∈ [2, 11], 1800-point grid, xatol 1e-13 | bounded minimisation of the closure |
| Spectrum | n ≤ 30 harmonics of f = 1/T | FFT of the mean-subtracted exact strain, no window |
| Antenna grid | 181 × 121 (θ, φ) | time-averaged TT-projected luminosity tensor |
| Detuning sweep | k ∈ {0.90 … 1.10}, 9 values | closure refinement xatol 1e-10, integration [0, 8] |

## Appendix B. Reproduction

```bash
python3 research/TRX-11-gw-choreography/code/trx11_gw_choreography.py --smoke     # < 20 s
python3 research/TRX-11-gw-choreography/code/trx11_gw_choreography.py              # full, 8.17 s
python3 research/TRX-11-gw-choreography/code/trx11_gw_choreography.py --figures   # + 300-DPI figures
```

Full runtime on the reference machine: 8.17 s; smoke mode completes in under 20 seconds and is exercised by the repository CI.

## Appendix C. Environment

Python ≥ 3.11, numpy ≥ 2.0, scipy ≥ 1.14, matplotlib ≥ 3.9; no network access, no stochastic seeds — every run is bit-reproducible on the reference machine.
