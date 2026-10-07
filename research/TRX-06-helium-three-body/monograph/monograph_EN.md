# Helium Atom as the Coulomb Three-Body Problem (Classical Trajectory Monte Carlo)

*TRIVORTEX Research Program · v1.0.0 · Monograph Edition*

|  |  |
|---|---|
| Study | TRX-06 |
| Program | TRIVORTEX — The Three-Body Problem in the Vortex Model |
| Author | Isaev Iskhak Khamzatovich (ORCID 0009-0003-7299-0701) |
| DOI | 10.5281/zenodo.21825394 |
| Date | 2026-10-06 |
| Code | `code/trx06_helium_three_body.py` |
| Data | `results/trx06_results.json` |

## Abstract

This monograph treats the helium atom — a nucleus of charge Z = 2 and two electrons — as the classical Coulomb three-body problem, running a deterministic Monte Carlo ensemble of 3200 trajectories in the Wannier launch configuration: a radially staggered chain at hyperradius R₀ = 3 on the exact energy shell, excess energies E ∈ [0.05, 0.3] Ha, a fixed transverse kick σ = 0.01 breaking scale invariance, and a documented softening ε = 0.1 a.u. Four machine-verified results: (i) Energy is conserved over the valid ensemble to a relative drift of 4.28e-6 of the deep-well scale 2Z/ε = 40 (max |ΔE| = 1.714·10⁻⁴ a.u.; 0/3200 filtered). (ii) Outcome bookkeeping is exact (3200 = 3200); the autoionization channel is the only active outcome, single-escape fraction 1.000 in every bin. (iii) The escaping electron carries on average 7.28× the excess energy (median 5.90, band [3.24, 13.30]) while its captured partner keeps E − E_esc < 0 — binding energy released through the e⁻–e⁻ repulsion. (iv) The double-escape fraction stays at the 1e-4 counting floor; the universal Wannier slope α = 1.056 is cited, and this compact ensemble's fitted value (≈ 0, strong-coupling regime) is stored in the protocol.

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

The threshold story begins with Gregory Wannier's 1953 paper, which asked what happens when an atom is ionized with barely enough energy to release two electrons. Wannier argued that double escape must funnel through the only configuration compatible with both long-range Coulomb repulsions — the Wannier configuration in which the two electrons leave on opposite sides of the nucleus at equal distances and equal speeds — and that scale invariance of the Coulomb problem then forces a power law P_DE ∝ E^α. His phase-space argument, refined independently by Peterkop (1971), gives α = 1.056 for Z = 2, a number that became the classic benchmark of three-body breakup physics.

The classical trajectory Monte Carlo method entered atomic physics with Abrines and Percival (1966), who applied the correspondence principle to ionization and charge transfer: at large quantum numbers the quantum problem is replaced by an ensemble of classical trajectories with quantized initial conditions. For helium the method matured in the 1980s–1990s, when computers became able to integrate the full three-body Coulomb dynamics in production quantities; the autoionization channel — one electron captured, the other ejected — was recognized as the classical image of the Auger process and of the Fano (1961) resonances, with the e–e repulsion as the only energy-transfer mechanism.

The modern classical picture of the threshold region is geometric: Sacha and Eckhardt (2001) analyzed the Wannier ridge — the unstable orbit along r₁ = r₂ that organizes the escape — and showed how the triple-collision manifold channels trajectories into either double escape or autoionization. This is the three-body alternative familiar from vortex dynamics: Aref's (1979) analysis of three vortices exhibits the same competition between collapse and scattering, and the same invariant-based bookkeeping. Experiments on threshold double ionization read precisely the exponent α, which is why a CTMC study that reports its slope honestly — measured or not — stays a meaningful benchmark.

For TRIVORTEX the relevance is threefold. First, helium is the mixed-sign three-body problem: it tests the same central-force choreography bookkeeping as the gravitational and vortex trios, with the sign structure inverted. Second, the Wannier exponent is a closed-form universal benchmark — the same epistemic category as Theorem 3.1 of the monograph. Third, the laser connection is built in: the three-step model of high-harmonic generation (foundations in Agostini et al. 1979; synthesis by Corkum 1993) is a driven three-body problem of the electron, the parent ion and the field, and strong-field double ionization shows Wannier-type kinematics — this study is the atomic anchor of the program's quantum block (TRX-06, TRX-07, TRX-08).

## 2. Physical formulation

Hamiltonian dynamics in atomic units with nuclear motion neglected. The two electrons move in the field of a fixed nucleus of charge Z = 2: the Hamiltonian (E1) contains two softened attractions −Z/√(r² + ε²) and one softened repulsion +1/√(r₁₂² + ε²) with ε = 0.1 a.u. The individual electron energies εi = vi²/2 − Z/ri are the observables of the escape problem: an electron has escaped when it is beyond the radius 30 a.u. with outward radial velocity and positive individual energy, and the total H = ε₁ + ε₂ + 1/r₁₂ is conserved exactly by the dynamics — the conservation quality of the numerical integration is the first acceptance check.

The launch is the classical Wannier configuration: both electrons start on one ray at a fixed hyperradius R₀ = 3 a.u., radially staggered (inner shields outer) by Δr ∈ [0.8, 2.0], and are pushed outward with equal speeds on the exact energy shell — the launched kinetic energy makes the total exactly E ∈ [0.05, 0.3] Ha. A fixed-size, E-independent transverse kick σ = 0.01 breaks the scale invariance that would otherwise freeze the escape statistics, and the e–e repulsion acts during the outbound transit, converting symmetric pairs into autoionization events: the inner electron is captured while the outer one leaves, carrying more than the total excess energy.

| Parameter | Value | Meaning |
|---|---|---|
| Z | 2 | helium nucleus charge (atomic units) |
| ε | 0.1 a.u. | documented softening of all Coulomb denominators |
| E window | [0.05, 0.3] Ha, 8 log-spaced bins | excess energy above the double-escape threshold |
| launch | R₀ = 3 a.u., Δr ∈ [0.8, 2.0] | staggered Wannier chain, equal outward speeds |
| kick | σ = 0.01 (E-independent) | fixed transverse kick breaking scale invariance |
| ensemble | 8 × 400 = 3200, seed 7 | deterministic CTMC ensemble, t_max = 2500 |
| escape sphere | r = 30 a.u. | outward radial velocity and positive individual energy |

## 3. Mathematical model

The Hamiltonian (E1) is the classical limit of the quantum two-electron atom with the nucleus fixed at the origin: kinetic terms p₁²/2 + p₂²/2, two nuclear attractions −Z/r₁, −Z/r₂ and the electron–electron repulsion 1/r₁₂. All three denominators are softened, r → (r² + ε²)^{1/2} with ε = 0.1 a.u. — a documented regularization that removes the 1/r singularity at triple collision and at electron–nucleus passage while leaving the far-field Coulomb kinematics untouched. The softened forces (E2) are pairwise consistent (Newton's third law) and derive from a conservative potential, so the total energy H = ε₁ + ε₂ + 1/r₁₂ is an exact invariant of the flow — the quantity whose numerical drift is audited in the protocol.

The launch realizes the Wannier geometry on the exact energy shell. For a drawn stagger Δr ∈ [0.8, 2.0] the launch potential is computed from the softened Hamiltonian, the required kinetic energy is E minus that potential, and the two outward speeds are chosen equal (symmetric split, 2 · v₀²/2 = K), each deflected by a uniform transverse kick of amplitude σ; the velocity pair is then rescaled so that ½|v₁|² + ½|v₂|² equals the required kinetic energy exactly. The fixed, E-independent kick σ = 0.01 is essential: without it the launch family would be scale invariant, and the escape statistics would freeze into geometry rather than sample the excess-energy window.

Wannier's law (E4) follows from scale invariance restricted by the two Coulomb repulsions: near threshold the escape must pass along the potential saddle with r₁ ≈ r₂, and the radial scaling of the outgoing channel carries a phase-space volume E^α with α = ¼(√((100Z − 9)/(4Z − 1)) − 1), which evaluates to 1.0559 ≈ 1.056 for Z = 2. The present experiment launches at a fixed hyperradius R₀ = 3 instead of the scaling R₀ ~ 1/E, so it probes the strong-coupling regime of the fixed geometry: the double-escape channel is closed at the 1e-4 counting floor over the whole window, the window-fit slope is therefore ≈ 0, and the protocol stores that fit honestly instead of claiming the universal exponent.

**Notation**

| Symbol | Meaning |
|---|---|
| Z | nucleus charge, Z = 2 (helium) |
| ε | softening length of all Coulomb denominators, 0.1 a.u. |
| r₁, r₂, r₁₂ | electron–nucleus distances and the electron–electron separation |
| p_i, v_i | electron momenta and velocities |
| ε_i | individual electron energy, ε_i = v_i²/2 − Z/r_i |
| E | excess energy above the double-escape threshold, window [0.05, 0.3] Ha |
| E_esc | individual energy of the escaping electron |
| P_DE | double-escape fraction per excess-energy bin |
| α | Wannier threshold exponent, 1.056 (universal); fitted slope stored separately |
| R₀, Δr | launch hyperradius (3 a.u.) and radial stagger [0.8, 2.0] |
| σ | fixed transverse launch kick, 0.01 a.u. |

**(E1)** Hamiltonian in atomic units (softened denominators r → (r² + ε²)^{1/2}, ε = 0.1).

$$H = \frac{p_1^2}{2} + \frac{p_2^2}{2} - \frac{Z}{r_1} - \frac{Z}{r_2} + \frac{1}{r_{12}}, \qquad Z = 2$$

**(E2)** Softened pairwise-consistent equations of motion (Newton's third law).

$$\ddot{\mathbf{r}}_1 = -Z\,\frac{\mathbf{r}_1}{(r_1^2+\varepsilon^2)^{3/2}} + \frac{\mathbf{r}_1-\mathbf{r}_2}{(r_{12}^2+\varepsilon^2)^{3/2}}, \qquad \ddot{\mathbf{r}}_2 = -Z\,\frac{\mathbf{r}_2}{(r_2^2+\varepsilon^2)^{3/2}} - \frac{\mathbf{r}_1-\mathbf{r}_2}{(r_{12}^2+\varepsilon^2)^{3/2}}$$

**(E3)** Individual electron energies, the conserved total and the autoionization overshoot (binding energy released).

$$\varepsilon_i = \tfrac{1}{2}v_i^2 - \frac{Z}{r_i}, \qquad H = \varepsilon_1 + \varepsilon_2 + \frac{1}{r_{12}}, \qquad E_{esc}/E > 1$$

**(E4)** Wannier threshold law (Wannier 1953; independent derivation by Peterkop 1971).

$$P_{DE}(E) \propto E^{\alpha}, \qquad \alpha = \frac{1}{4}\left(\sqrt{\frac{100Z-9}{4Z-1}} - 1\right) = 1.056 \ \ (Z = 2)$$

**(E5)** Energy-quality filter: trajectories above the drift cut are discarded (0 of 3200 in the full run).

$$\delta = \max|\Delta E| \, / \, (2Z/\varepsilon) \le 4\times 10^{-4}, \qquad |\Delta E| \le 5\times 10^{-3}$$

## 4. Connection to the TRIVORTEX framework

The mapping to TRIVORTEX is structural at every level. The e⁻–e⁻–nucleus trio is the three-body problem with the sign structure inverted relative to gravity — mixed attractive and repulsive pairs — yet it obeys the same central-force bookkeeping, the same invariant-audit discipline and the same collapse-versus-scattering alternative that Aref (1979) exposed for three vortices. The autoionization overshoot, in which one body exits carrying the share of another, is the direct analog of the energy exchange that choreographies of the vortex model exhibit; the Wannier exponent α = 1.056 is a closed-form universal benchmark of the same epistemic kind as Theorem 3.1; and the documented softening ε plays exactly the role of the finite vortex cores in the TRIVORTEX regularization — both keep the singular pair interaction finite without touching the far-field dynamics.

| Quantity in this study | TRIVORTEX analog | Comment |
|---|---|---|
| e⁻–e⁻–nucleus trio | the three bodies | Coulomb three-body with mixed pair signs |
| Autoionization overshoot E_esc/E > 1 | energy exchange in choreographies | one body exits with the share of another |
| Wannier threshold law P_DE ∝ E^1.056 | closed-form benchmarks (Theorem 3.1) | a sharp universal exponent as reference point |
| Softening ε = 0.1 a.u. | finite vortex cores | documented regularization of 1/r singularities |

## 5. Numerical method

Sampling is fully deterministic: a seeded generator (seed 7) draws the stagger Δr ∈ [0.8, 2.0], the ray orientation and two transverse kick directions per trajectory; 400 trajectories are drawn per energy bin on a geometric grid of 8 excess energies from 0.05 to 0.3 Ha, giving 3200 launch states. Each state is projected onto the exact energy shell after the kicks are applied, so every launched trajectory starts with total energy E to machine precision — the subsequent drift audit measures integrator error only, not launch noise.

Integration is a per-trajectory adaptive RK4 in dt-groups: the step dt = 0.03 · r_min/v_max is clipped and quantized onto a fixed ladder of eleven levels from 10⁻⁴ to 0.3, and trajectories requiring the same level are advanced as a batch, which keeps the ensemble vectorized while preserving the adaptive rule. A trajectory ends when both electrons are beyond r = 30 a.u. with outward velocity and positive individual energy (double escape), when a terminal configuration freezes after t = 60 (one electron inside r < 1 with the other beyond r > 5, or both inside — no double escape possible on the timescale), or at t_max = 2500.

Diagnostics: the energy drift |ΔE| is tracked per trajectory as the running maximum against the launch energy; trajectories with |ΔE| > 5·10⁻³ a.u. are discarded (standard CTMC practice; 0 of 3200 in the full run). The double-escape fraction per bin carries Poisson errors √(p(1 − p)/n); the threshold slope is a least-squares fit on log₁₀–log₁₀ coordinates and is re-derived from the stored counts as an independent reproducibility check. Every quantity — value, target, tolerance, unit, pass flag — is stored in the JSON protocol, and the --figures mode adds the four panels and the scheme from the same ensemble data without touching the checks.

## 6. Results and analysis

### fig01 model landscape

![Model landscape: (a) softened Coulomb potential V(r₁, r₂) for Z = 2, ε = 0.1 — the e–e ridge wall along the diagonal and the staggered launch segment (r₁ = 3, r₂ = 3 + Δ, Δ ∈ [0.8, 2.0]); (b) chain potential V(ρ, ρ + Δ) along the launch ray for three staggers with the excess-energy window E ∈ [0.05, 0.3] Ha.](../figures/fig01_model_landscape.png)

*Model landscape: (a) softened Coulomb potential V(r₁, r₂) for Z = 2, ε = 0.1 — the e–e ridge wall along the diagonal and the staggered launch segment (r₁ = 3, r₂ = 3 + Δ, Δ ∈ [0.8, 2.0]); (b) chain potential V(ρ, ρ + Δ) along the launch ray for three staggers with the excess-energy window E ∈ [0.05, 0.3] Ha.*
Panel (a) maps the potential topography: the diagonal ridge r₁ = r₂ (the e–e repulsion wall) and the gold launch segment at r₁ = 3, r₂ = 3 + Δ with Δ ∈ [0.8, 2.0]; panel (b) shows that launched states sit above the potential asymptote and climb out unless the repulsion binds one electron.

### fig02 energy sharing

![Headline result: (a) distribution of the escaping-electron share E_esc/E over all 3200 autoionization events — mean 7.28, median 5.90, 16–84 pct band [3.24, 13.30]; (b) the measured double-escape fraction stays at the 1e-4 counting floor over E ∈ [0.05, 0.3], far below the 0.5 acceptance line; the Wannier slope 1.056 is a guide, not a resolved measurement.](../figures/fig02_energy_sharing.png)

*Headline result: (a) distribution of the escaping-electron share E_esc/E over all 3200 autoionization events — mean 7.28, median 5.90, 16–84 pct band [3.24, 13.30]; (b) the measured double-escape fraction stays at the 1e-4 counting floor over E ∈ [0.05, 0.3], far below the 0.5 acceptance line; the Wannier slope 1.056 is a guide, not a resolved measurement.*
The escaping electron carries on average 7.28× the total excess energy (median 5.90, band [3.24, 13.30]) while the captured partner keeps E − E_esc < 0 — binding energy released into the pair; not a single double escape occurs in the ensemble, so all 3200 outcomes sit in the autoionization channel.

### fig03 parameter sweeps

![Parameter sweeps: (a) per-bin mean of E_esc/E with 16–84 percentile bars across the excess-energy window — the transfer efficiency stays far above parity in every bin; (b) launch-kick sensitivity on reduced ensembles of 720 trajectories per point — the autoionization channel remains dominant for every documented kick σ, including the scale-invariant limit σ = 0.](../figures/fig03_parameter_sweeps.png)

*Parameter sweeps: (a) per-bin mean of E_esc/E with 16–84 percentile bars across the excess-energy window — the transfer efficiency stays far above parity in every bin; (b) launch-kick sensitivity on reduced ensembles of 720 trajectories per point — the autoionization channel remains dominant for every documented kick σ, including the scale-invariant limit σ = 0.*
Across the kick grid σ ∈ {0, 0.002, 0.005, 0.01, 0.02, 0.05} the single-escape fraction stays at 1.000 and the mean overshoot barely moves, 5.3421 → 5.3416 — the strong-coupling autoionization channel is insensitive to the kick that breaks scale invariance.

### fig04 autoionization dynamics

![Dynamics of one representative autoionization event (re-integrated with the same adaptive RK4 rule): (a) x–y paths — the escaper leaves through r = 30 a.u. while the captured electron winds toward the nucleus; (b) individual energies ε₁(t), ε₂(t) and the conserved total — the repulsion hands 7.28× E to the escaper.](../figures/fig04_autoionization_dynamics.png)

*Dynamics of one representative autoionization event (re-integrated with the same adaptive RK4 rule): (a) x–y paths — the escaper leaves through r = 30 a.u. while the captured electron winds toward the nucleus; (b) individual energies ε₁(t), ε₂(t) and the conserved total — the repulsion hands 7.28× E to the escaper.*
For the representative event at E = 0.107761 Ha the escaper exits at t = 19.6952 with E_esc = 0.784471 Ha (share 7.2797) and the partner is left bound at ε = −0.438084 Ha — a direct view of the three-body energy handover through the e–e repulsion.

**Conservation.** Over the whole valid ensemble of 3200 trajectories the running maximum of the energy error is 1.714·10⁻⁴ a.u.; relative to the deep-well kinetic scale 2Z/ε = 40 a.u. this is a relative drift of 4.28e-6 — two orders of magnitude inside the 4e-4 acceptance tolerance, and not a single trajectory required the 5·10⁻³ filter (0/3200 discarded). The energy shell is therefore trusted as the backbone of all downstream statistics.

**Bookkeeping and the channel.** The outcome classes sum exactly (3200 = 3200), and the composition is unanimous: the single-escape fraction is 1.000 in every one of the eight energy bins, the double-escape fraction 0.0 in every bin. The autoionization channel is thus the only active outcome of the fixed-launch geometry — a genuinely three-body result, since the e–e repulsion is the only mechanism able to hand energy from one electron to the other while the nucleus keeps the captured partner bound.

**Energy sharing.** The escaping electron carries on average 7.28× the total excess energy (7.2803 over all 3200 events; median 5.8967; 16–84 percentile band [3.2395, 13.2956]) — far above the 1.2× acceptance line. The captured partner keeps E − E_esc < 0, i.e. binding energy is released into the pair. The representative re-integrated event at E = 0.107761 Ha ends at t = 19.6952 with the escaper at E_esc = 0.784471 Ha (share 7.2797) and its partner bound at ε = −0.438084 Ha, a direct portrait of the three-body handover.

**Threshold behavior.** The measured double-escape fraction sits at the 1e-4 counting floor across the entire window E ∈ [0.05, 0.3] (below the 0.5 acceptance line everywhere), so the window-fit slope is −1.29·10⁻¹⁵ ≈ 0: the fixed-launch geometry with R₀ = 3 probes the strong-coupling regime, where P_DE is nearly E-independent. The kick sweep over σ ∈ {0, 0.002, 0.005, 0.01, 0.02, 0.05} on reduced ensembles of 720 trajectories per point leaves the channel dominant (fraction 1.000 everywhere) and the mean overshoot essentially unmoved, 5.3421 → 5.3416. The universal α = 1.056 requires near-threshold Wannier-cap conditioning and far larger ensembles; it is cited, not claimed, and the measured slope is stored in the protocol.

### Verification summary

| Check | Recorded value | Target | Tolerance | Pass |
|---|---|---|---|---|
| `max_relative_energy_drift_valid` | 4.28422e-06 | 0 | 0.0004 | yes |
| `outcome_classes_sum_to_N` | 3200 | 3200 | 1e-12 | yes |
| `autoionization_channel_active` | 1 | 1 | 1e-12 | yes |
| `escaping_electron_energy_overshoot` | 1 | 1 | 1e-12 | yes |
| `pde_below_half_everywhere` | 1 | 1 | 1e-12 | yes |
| `wannier_exponent_reported` | 1 | 1 | 1e-12 | yes |
| `fit_reproducible` | 1 | 1 | 1e-12 | yes |

*(status: **PASS**, mode: full)*

## 7. Discussion

The model is deliberately minimal: classical mechanics only, nuclear motion neglected, a fixed launch geometry and a documented softening. Within these assumptions every conclusion is an exact statement about the ensemble rather than a simulation of a specific experiment. The natural extensions — Wannier-cap conditioning (launching on the ridge with R₀ ~ 1/E so the threshold law becomes measurable), ensembles two to three orders larger, explicit quantum-classical correspondence tests, and nuclear motion for recoil — each preserve the verification style established here.

The parameter regime is chosen for structural clarity rather than for reproducing the exponential tail of the threshold law: a fixed R₀ = 3 with a fixed kick σ = 0.01 probes the strong-coupling regime of the staggered chain, and the honesty note says so openly. The measured slope (−1.29·10⁻¹⁵ ≈ 0) is stored in the protocol next to the cited universal benchmark α = 1.056 — the same epistemic discipline the program applies everywhere: a number is either measured and stored, or cited and marked as a reference, never blended.

Within the program this study anchors the quantum block: TRX-07 supplies the quantum three-body benchmark proper (Efimov physics of laser-cooled trimers), TRX-08 the trapped-ion realization, and TRX-11 keeps three bodies but exchanges the Coulomb interaction for gravity plus radiation; TRX-01 applies three-body geometry to photon pressure. The laser link runs through the three-step model of high-harmonic generation — ionization, laser-driven acceleration, recombination — whose kinematic core is the same electron-plus-ion two-body subproblem embedded here, and whose strong-field double-ionization channel shows the Wannier-type energy sharing measured in this study.

## 8. Conclusions

1. Energy is conserved over the valid ensemble to a relative drift of 4.28e-6 of the deep-well scale 2Z/ε = 40 (max |ΔE| = 1.714·10⁻⁴ a.u.; 0/3200 trajectories filtered).
2. Outcome bookkeeping is exact (3200 = 3200), and the autoionization channel is the only active outcome: the single-escape fraction is 1.000 in every energy bin.
3. The three-body energy transfer is measured: the escaping electron carries on average 7.28× the excess energy (median 5.90, 16–84 pct band [3.24, 13.30]), and the captured partner keeps E − E_esc < 0 — binding energy released.
4. No double escapes occur: P_DE stays at the 1e-4 counting floor across E ∈ [0.05, 0.3], far below the 0.5 acceptance line — the strong-coupling regime of the fixed-launch geometry.
5. The Wannier exponent is handled honestly: the fitted slope of this compact ensemble (−1.29·10⁻¹⁵ ≈ 0) is stored in the protocol, while the universal α = 1.056 is cited as a benchmark, not claimed.
6. The results are robust to the scale-breaking kick: over σ ∈ {0, 0.002, 0.005, 0.01, 0.02, 0.05} the single-escape fraction stays 1.000 and the mean overshoot moves only 5.3421 → 5.3416.

## 9. References

1. Wannier, G. H. (1953). *The threshold law for single ionization of atoms.* Physical Review 90, 817–825.
2. Peterkop, R. K. (1971). *Wannier's theory of ionization.* Journal of Physics B 4, 513–521.
3. Abrines, R., Percival, I. C. (1966). *Classical theory of charge transfer and ionization of hydrogen atoms by protons.* Proceedings of the Physical Society 88, 861–872.
4. Fano, U. (1961). *Effects of configuration interaction on intensities and phase shifts.* Physical Review 124, 1866–1878.
5. Sacha, K., Eckhardt, B. (2001). *Classical mechanics of the Wannier ridge.* Physical Review A 63, 042714.
6. Aref, H. (1979). *Motion of three vortices.* Physics of Fluids 22, 393–400 (collapse/scattering methodology shared with CTMC studies).
7. Agostini, P., Fabre, F., Mainfray, G., Petite, G., Rahman, N. K. (1979). *Free-free transitions following six-photon ionization of xenon atoms.* Physical Review Letters 42, 1127–1130 (three-step model foundations).
8. Corkum, P. B. (1993). *Plasma perspective on strong-field multiphoton ionization.* Physical Review Letters 71, 1994–1997.

### BibTeX

```bibtex
@article{wannier1953,
  author  = {Wannier, Gregory H.},
  title   = {The threshold law for single ionization of atoms},
  journal = {Physical Review},
  year    = {1953}, volume = {90}, pages = {817--825}}

@article{abrines1966,
  author  = {Abrines, R. and Percival, I. C.},
  title   = {Classical theory of charge transfer and ionization of hydrogen atoms by protons},
  journal = {Proceedings of the Physical Society},
  year    = {1966}, volume = {88}, pages = {861--872}}

@article{sacha2001,
  author  = {Sacha, K. and Eckhardt, B.},
  title   = {Classical mechanics of the Wannier ridge},
  journal = {Physical Review A},
  year    = {2001}, volume = {63}, pages = {042714}}

@article{corkum1993,
  author  = {Corkum, Paul B.},
  title   = {Plasma perspective on strong-field multiphoton ionization},
  journal = {Physical Review Letters},
  year    = {1993}, volume = {71}, pages = {1994--1997}}
```

## Appendix A. Parameter table

| Symbol | Value | Role |
|---|---|---|
| Z | 2 | helium nucleus charge |
| ε | 0.1 a.u. | softening of all Coulomb denominators |
| E window | [0.05, 0.3] Ha, 8 log-spaced bins | excess-energy grid of the ensemble |
| N | 8 × 400 = 3200, seed 7 | deterministic CTMC ensemble size |
| R₀ | 3 a.u. | launch hyperradius of the Wannier chain |
| Δr | [0.8, 2.0] | radial stagger of the chain (inner shields outer) |
| σ | 0.01 | fixed transverse kick breaking scale invariance |
| r_esc | 30 a.u. | escape radius (outward velocity, positive individual energy) |
| t_max | 2500 | integration span per trajectory |
| dt rule | 0.03 · r_min/v_max, ladder 10⁻⁴ … 0.3 | adaptive RK4 step, quantized to eleven levels |
| drift filter | energy drift ΔE ≤ 5·10⁻³ a.u. | energy-quality cut (0/3200 filtered in the full run) |
| drift scale | 2Z/ε = 40 a.u. | deep-well kinetic scale for the relative drift |

## Appendix B. Reproduction

```bash
python3 research/TRX-06-helium-three-body/code/trx06_helium_three_body.py --smoke     # < 20 s
python3 research/TRX-06-helium-three-body/code/trx06_helium_three_body.py              # full, 37.7 s
python3 research/TRX-06-helium-three-body/code/trx06_helium_three_body.py --figures   # + 300-DPI figures
```

Full runtime on the reference machine: 37.7 s; smoke mode completes in under 20 seconds and is exercised by the repository CI.

## Appendix C. Environment

Python ≥ 3.11, numpy ≥ 2.0, scipy ≥ 1.14, matplotlib ≥ 3.9; no network access, no stochastic seeds — every run is bit-reproducible on the reference machine.
