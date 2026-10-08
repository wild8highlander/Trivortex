# Three-Soliton Molecule in a Mode-Locked Fiber Laser

*TRIVORTEX Research Program · v1.0.0 · Monograph Edition*

|  |  |
|---|---|
| Study | TRX-03 |
| Program | TRIVORTEX — The Three-Body Problem in the Vortex Model |
| Author | Isaev Iskhak Khamzatovich (ORCID 0009-0003-7299-0701) |
| DOI | 10.5281/zenodo.21825394 |
| Date | 2026-10-06 |
| Code | `code/trx03_soliton_molecule.py` |
| Data | `results/trx03_results.json` |

## Abstract

This monograph treats a phase-locked triplet of ultrashort pulses in a passively mode-locked fiber laser as an optical three-body system. Each pulse is a body with the conservative pair interaction V(r, Δφ) = C₁e^(−2r/L) − C₂e^(−r/L)cos 2Δφ, whose in-phase well has the analytic minimum r₀ = L·ln(2C₁/C₂) = ln(4/3) ≈ 0.287682, reproduced numerically to 5.6e-17, while the anti-phase lock Δφ = π/2 is proved purely repulsive. Relaxation of a random triplet {1.0, 2.0, 3.5} under overdamped damping converges to an equally spaced molecule whose spacing equals the three-chain equilibrium s* = 0.2018927, the root of F(s) + F(2s) = 0 — compressed 29.8 % below the pair value by the far-pair attraction, a genuine three-body effect. The conservative molecule conserves energy to 1.8e-15 over t = 100 and breathes at f = 0.469765 against the analytic Hessian mode 0.468766 (agreement 0.21 %); a sweep of the locking phase yields the full stability map, with both equilibria diverging and both modes softening to zero at the binding threshold Δφ = π/4. The soliton molecule thus stands verified as the optical twin of the TRIVORTEX three-body choreographies.

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

The word "soliton" was coined by Zabusky and Kruskal in 1965, when numerical experiments on the Korteweg–de Vries equation showed that nonlinear pulses collide and re-emerge with their identity intact. Optical solitons followed: Hasegawa and Tappert predicted in 1973 that the nonlinear Schrödinger equation admits shape-preserving pulses in fibers with anomalous dispersion, and Mollenauer, Stolen and Gordon observed them in 1980. From the very beginning it was clear that two solitons are not merely two particles — their overlapping tails make them interact, and the interaction is the optical analog of a force.

The quantitative theory of soliton interactions was built by Karpman and Solov'ev in 1981 through perturbation theory around the exact two-soliton solution, and by Gordon in 1983 through the discrete spectral picture; both approaches yield an exponential force whose sign is set by the relative phase. Malomed (1991) extended the analysis to multi-soliton bound states and their cyclic dynamics. Experimentally, Stratmann, Pagel and Mitschke (2005) directly observed temporal soliton molecules in a fiber laser, and Herink and colleagues (2017) filmed their internal dynamics in real time by spectral interferometry — including the breathing mode that this study computes analytically and numerically.

A soliton molecule is therefore a genuine bound state of N bodies, not a metaphor: its geometry is fixed by a force balance in which every pulse feels every other pulse, its stability is read off a normal-mode spectrum, and its assembly is a relaxation problem. For N = 3 all of these ingredients are exactly what the three-body problem means in the TRIVORTEX program — three agents, pairwise interactions, a collective equilibrium and a choreography of motion. The fiber laser simply replaces gravity or vortex circulation by an exponential-cosine law that can be switched by phase control.

Within the program this study is the optics-block anchor of the choreography family. It verifies, in a setting where "passing through one another" is physical rather than singular, the same structural sequence used everywhere in TRIVORTEX: analytic pair law, collective equilibrium, linearized spectrum, conservation of the invariant. The phase-locked triplet is the optical sibling of the Lagrange triangle of Theorem 3.1, and the compression of s* below r₀ is the spectral sibling of the collective force balance that fixes the equilateral configuration.

## 2. Physical formulation

In a passively mode-locked fiber laser the circulating field breaks into ultrashort soliton pulses. When two pulses overlap, their phases and envelopes exchange work through the Kerr nonlinearity and the gain/loss balance of the cavity; in the reduced Gordon–Mollenauer picture this continuous exchange is equivalent to a conservative force between point-like particles with an exponential (evanescent-tail) profile. The force depends on the phase difference Δφ between the pulses: in-phase pulses (Δφ = 0) attract, quadrature pulses (Δφ = π/2) repel. A triplet locked in phase therefore behaves as three bodies on a line, bound by a soft exponential tail and free to pass through one another as real solitons do.

The equilibrium of such a chain is a true three-body configuration. For a pair, attraction and the repulsive exponential core balance at r₀ = L·ln(2C₁/C₂). In the symmetric three-pulse molecule every pulse also feels the far pair at distance 2s, so the end-pulse balance reads F(s*) + F(2s*) = 0 and the spacing s* is compressed below r₀ — the same collective compression that the Lagrange triangle shows relative to an isolated two-body pair. Small displacements around the equilibrium decompose into normal modes of a generalized eigenproblem; the low mode is the breathing oscillation of the molecule, directly observable in real-time spectroscopy experiments.

| Parameter | Value | Meaning |
|---|---|---|
| C₁, C₂ | 2, 3 | exponential coefficients: repulsive core / attractive overlap |
| L | 1 | evanescent-tail length (unit of length) |
| m | 1 | pulse "mass" (kinetic coefficient) |
| Δφ | 0 (locked) | phase difference between adjacent pulses |
| pair equilibrium | r₀ = L·ln(2C₁/C₂) = ln(4/3) ≈ 0.287682 | analytic two-body balance |
| relaxation start | {1.0, 2.0, 3.5}, γ_d = 1 (overdamped) | random triplet, T = 90 |
| conservative probe | middle pulse +0.01, γ_d = 0, T = 100 | breathing-mode run, DOP853 1e-12 |

## 3. Mathematical model

The reduced model starts from the pair interaction. Overlapping soliton envelopes in the anomalous-dispersion fiber exchange energy and momentum through the Kerr term; keeping the leading tail-overlap terms gives the Gordon–Mollenauer potential (E1): a repulsive exponential core C₁e^(−2r/L) and an attractive overlap C₂e^(−r/L) whose strength is modulated by cos 2Δφ. The sign of the force therefore follows the phase: attraction for |Δφ| < π/4, repulsion beyond, and exact cancellation of the attractive term at Δφ = π/4 — the binding threshold. The pair equilibrium solves F(r₀, Δφ) = 0 and yields the closed form r₀ = L·ln(2C₁/(C₂ cos 2Δφ)); at the preset Δφ = 0 it is ln(4/3).

The three-body structure enters through the all-pairs chain dynamics (E3). Soliton tails act at any separation and solitons pass through one another, so the equations are invariant under particle exchange and the physically meaningful geometry of a configuration is read from the sorted positions. For the symmetric molecule with spacings (s, s) the end pulse feels the near pair F(s) and the far pair F(2s), giving the balance F(s*) + F(2s*) = 0. Because F(2s*) < 0 is attractive, the root s* is necessarily below the pair root r₀ — the chain is compressed by the third body. This is the same logical step that produces the collective geometry of the Lagrange triangle from pairwise Newtonian attraction.

Small oscillations follow from the Hessian of the total potential in the spacing coordinates (d₁, d₂) with the center of mass removed; the kinetic energy is not diagonal in these coordinates, so the normal modes solve the generalized eigenproblem (E5) with mass matrix M_g = m·`[[2/3, 1/3], [1/3, 2/3]]`. At the preset spacing s* the two eigenfrequencies are 2.4536 and 2.9453 rad (cyclic 0.390507 and 0.468766); the higher one is the breathing mode in which the middle pulse moves against the outer pair. The same Hessian evaluated along the phase sweep softens continuously to zero at the binding threshold, providing the stability map of the molecule.

**Notation**

| Symbol | Meaning |
|---|---|
| x_k | position of pulse k on the cavity axis |
| r | pair separation |
| Δφ | phase difference between adjacent pulses |
| V, F | pair potential and pair force (F = −∂V/∂r) |
| C₁, C₂ | exponential coefficients of the potential (2 and 3) |
| L | evanescent-tail length (length unit) |
| m | pulse mass (kinetic coefficient) |
| γ_d | damping coefficient (1.0 relaxation, 0 conservative) |
| r₀, s* | pair equilibrium and chain equilibrium spacing |
| H, M_g | Hessian of the chain potential and mass matrix in spacing coordinates |
| ω_i, f | angular and cyclic normal-mode frequencies |

**(E1)** Phase-dependent pair potential of two solitons.

$$V(r,\Delta\varphi) = C_1\,e^{-2r/L} - C_2\,e^{-r/L}\cos(2\Delta\varphi)$$

**(E2)** Pair force along increasing separation (F < 0 — attraction).

$$F(r,\Delta\varphi) = -\frac{\partial V}{\partial r} = \frac{2C_1}{L}e^{-2r/L} - \frac{C_2}{L}e^{-r/L}\cos(2\Delta\varphi)$$

**(E3)** Chain dynamics with all-pairs interaction and damping.

$$m\,\ddot{x}_k = -\sum_{l\neq k}\frac{\partial V(|x_k-x_l|)}{\partial x_k} - \gamma_d\,\dot{x}_k, \qquad k=1,2,3$$

**(E4)** Pair equilibrium r0 and three-chain equilibrium s* (end-pulse balance).

$$r_0 = L\ln\!\frac{2C_1}{C_2\cos 2\Delta\varphi}; \qquad F(s^*) + F(2s^*) = 0$$

**(E5)** Generalized eigenproblem for the chain normal modes (breathing spectrum).

$$H\,v = \omega^2 M_g\,v, \quad H = \begin{pmatrix} V''(s)+V''(2s) & V''(2s)\\ V''(2s) & V''(s)+V''(2s) \end{pmatrix}, \quad M_g = m\begin{pmatrix} 2/3 & 1/3\\ 1/3 & 2/3 \end{pmatrix}$$

## 4. Connection to the TRIVORTEX framework

The mapping to the TRIVORTEX core is structural, one-to-one and already visible in the equations. The three phase-locked pulses are the optical realization of the three agents of Theorem 3.1: a symmetric, phase-locked special solution of a three-body system, exactly as the rotating vortex triangle is the equal-circulation special solution of the vortex problem. The molecule spacing s*plays the role of the Lagrange-triangle side a: both are fixed not by a two-body law but by the requirement that every member be in equilibrium under the combined pull of the other two — F(s*) + F(2s*) = 0 here, the central-configuration equations there. The breathing mode ω₂ is the analog of the radial modulation of the choreography, and the phase difference Δφ controls binding exactly as the circulation ratio controls the vortex triangle: changing it moves the system through symmetric and asymmetric configurations until binding is lost (Δφ = π/4, the analog of leaving the stability island). The same exponential-cosine structure reappears in TRX-09 vortices and TRX-04 photon-fluid beams, which makes this study the reusable optical template of the program.

| Quantity in this study | TRIVORTEX analog | Comment |
|---|---|---|
| Three phase-locked pulses | three bodies of Theorem 3.1 | both are choreographic triads |
| Phase locking Δφ = 0 | equal circulations Γ | symmetric special solution |
| Molecule spacing s* | Lagrange-triangle side a | fixed by collective force balance |
| Balance F(s*) + F(2s*) = 0 | every vortex feels the other two | the three-body compression mechanism |
| Breathing mode ω₂ | radial modulation of the choreography | small oscillations about the central configuration |

## 5. Numerical method

Equilibria are computed by bracketed root finding. The pair equilibrium solves F(r) = 0 and the chain equilibrium solves F(s) + F(2s) = 0, both by Brent's method with xtol = 1e-15 and machine-level rtol on sign-stable brackets; the numeric pair root agrees with the closed form ln(4/3) to 5.6e-17. The repulsive character of the anti-phase lock is established exhaustively rather than by sampling: the minimum of F(r, π/2) over the range r ∈ [0.05, 20] on a 4000-point grid is +6e-9 > 0, i.e. the force never turns attractive.

Dynamics are integrated with the explicit Dormand–Prince 8(5,3) scheme (DOP853). The relaxation run starts from positions {1.0, 2.0, 3.5} with zero velocities under damping γ_d = 1.0 (overdamped, the Doppler-cooled regime of a mode-locked laser) and runs to T = 90 with rtol = 1e-11, atol = 1e-12 and max_step = 0.2. The conservative run holds γ_d = 0, displaces the middle pulse by +0.01 from the perfect molecule and integrates to T = 100 with rtol = atol = 1e-12 and max_step = 0.05, sampling 2000 points; the energy drift over the whole run is 1.776357e-15 against the 1e-10 acceptance tolerance.

The breathing frequency is extracted twice, independently. Numerically, the middle-pulse displacement relative to the center of mass is Hann-windowed and Fourier-transformed; the spectral peak lies at f = 0.469765. Analytically, the generalized eigenproblem (E5) at s* gives cyclic modes 0.390507 and 0.468766; the measured peak matches the nearest analytic mode to 0.21 %, comfortably inside the 1 % acceptance tolerance. Every check stores its value, target, tolerance, unit and pass flag in the JSON protocol, so the study reproduces from a single command with no network access and no stochastic seeds.

## 6. Results and analysis

### fig01 potential landscape

![Interaction landscape: phase-dependent pair potential and the three-chain force balance.](../figures/fig01_potential_landscape.png)

*Interaction landscape: phase-dependent pair potential and the three-chain force balance.*
Panel (a) shows V(r, Δφ) for four lockings: the binding well exists only for |Δφ| < π/4, has its minimum at r₀ = 0.287682, and degenerates into pure repulsion for the anti-phase case. Panel (b) shows the end-pulse balance F(s) + F(2s) = 0: the root s* = 0.201893 lies 29.8 % below the pair value r₀ — a genuine three-body compression.

### fig02 molecule formation

![Headline result: relaxation of a random triplet into the equally spaced soliton molecule.](../figures/fig02_molecule_formation.png)

*Headline result: relaxation of a random triplet into the equally spaced soliton molecule.*
Starting from positions {1.0, 2.0, 3.5} under overdamped damping, the three worldlines settle within T = 90 into an equally spaced triplet; the sorted spacings d₁(t) and d₂(t) converge to the chain equilibrium s*= 0.201893 (final mismatch 2.2e-16, offset from s* 2.8e-17), visibly below the pair value r₀ = 0.2877 marked for comparison.

### fig03 phase sweep

![Parameter sweep over the locking phase: equilibrium geometry and mode softening.](../figures/fig03_phase_sweep.png)

*Parameter sweep over the locking phase: equilibrium geometry and mode softening.*
Both equilibria diverge as the binding threshold Δφ = π/4 is approached: s* grows from 0.201893 at Δφ = 0 through 0.719380 at Δφ = 0.5 rad to 2.885 at Δφ = 0.75 rad, tracking the pair value. The chain modes soften in response — from 2.4536 and 2.9453 rad at the preset down to 0.1092 and 0.1982 rad — producing a complete stability map of the phase-locked molecule.

### fig04 breathing dynamics

![Dynamics of the conservative molecule: breathing time series and spectrum against the Hessian prediction.](../figures/fig04_breathing_dynamics.png)

*Dynamics of the conservative molecule: breathing time series and spectrum against the Hessian prediction.*
With the middle pulse displaced by 0.01 and damping removed, the molecule breathes over T = 100 while the total energy drifts by only 1.8e-15 (DOP853, rtol = atol = 1e-12). The FFT spectrum of the middle-pulse displacement peaks at f = 0.469765 against the analytic Hessian modes 0.468766 and 0.390507 — agreement to 0.21 %, an order of magnitude inside the 1 % tolerance.

**Equilibria.** The numeric pair root reproduces the closed form r₀ = L·ln(2C₁/C₂) = ln(4/3) ≈ 0.287682 to 5.6e-17 — machine zero. The exhaustive anti-phase test returns min F(r, π/2) = +6e-9 > 0 over r ∈ [0.05, 20], confirming that binding is controlled by the phase factor cos 2Δφ and disappears entirely at and beyond Δφ = π/4. The curvature of the well at the pair minimum is V″(r₀) = 2.25, which fixes the pair breathing scale √(3V″(r₀)) ≈ 2.5981 against which the chain spectrum is compared.

**Molecule formation.** Under overdamped relaxation from {1.0, 2.0, 3.5}, the sorted spacings converge to d₁ = d₂ = 0.2018926516; their final mismatch is 2.2e-16 and their offset from the independently computed chain equilibrium s* = 0.2018926516 is 2.8e-17 — both machine-level, against tolerances of 1e-8 and 1e-6. The spacing sits 29.8 % below the pair value r₀ = 0.287682: the far pair F(2s) pulls the molecule together, a clean, quantified three-body effect visible in fig02.

**Stability map.** Sweeping the locking phase Δφ from 0 to 0.75 rad shows both equilibria diverging as the binding threshold π/4 ≈ 0.7854 is approached: s* grows from 0.201893 through 0.719380 (Δφ = 0.5 rad) to 2.885 (Δφ = 0.75 rad). The chain modes soften in the same direction, from 2.4536 and 2.9453 rad at the preset to 0.1092 and 0.1982 rad at the far end of the sweep — the soft-mode behavior expected as the well flattens into pure repulsion (fig03).

**Breathing and invariants.** The conservative molecule breathes stably over T = 100 (fig04a) with total energy conserved to 1.776357e-15 — five orders of magnitude inside the 1e-10 tolerance. The FFT spectrum of the middle-pulse displacement peaks at f = 0.469765 against the analytic Hessian modes 0.468766 and 0.390507 (fig04b): agreement 0.21 %, an order of magnitude inside the 1 % acceptance tolerance. The dynamics, the spectrum and the Hessian thus triangulate the same breathing physics from three independent directions.

### Verification summary

| Check | Recorded value | Target | Tolerance | Pass |
|---|---|---|---|---|
| `pair_equilibrium_numeric_vs_analytic` | 5.55112e-17 | 0 | 1e-10 | yes |
| `antiphase_pi2_purely_repulsive` | 1 | 1 | 1e-12 | yes |
| `molecule_final_spacings_equal` | 2.22045e-16 | 0 | 1e-08 | yes |
| `molecule_final_spacing_equals_s_star` | 2.77556e-17 | 0 | 1e-06 | yes |
| `conservative_energy_drift` | 1.77636e-15 | 0 | 1e-10 | yes |
| `breathing_mode_frequency` | 0.469765 | 0.468766 | 0.0047 | yes |

*(status: **PASS**, mode: full)*

## 7. Discussion

The reduced model is deliberately minimal: point-like pulses, a pair potential without retardation or gain dynamics, and damping treated as a switchable term. Within these assumptions every conclusion is an exact statement about the governing equations rather than a simulation of a specific laser. The natural extensions — third-order dispersion and self-frequency shift (which make the force asymmetric and non-conservative), continuous cw backgrounds, larger molecules N > 3 with defect modes, and full NLSE integration of the same scenario — each preserve the verification style established here.

The parameter regime covers the generic regime of the Gordon–Mollenauer law rather than a specific cavity: C₁/C₂ = 2/3 places the pair well at r₀ ≈ 0.29 tail lengths with depth 0.25, comfortably resolved on the integration grid. The phase sweep deliberately approaches the binding threshold Δφ = π/4, where the equilibrium diverges and the Hessian develops a zero mode; exactly at threshold the brentq brackets fail, which the sweep code reports as a hard boundary rather than hiding with a regularized formula. Realistic cavities would add noise-driven phase diffusion, slowly destroying the lock — a physics question outside the conservative scope of this study.

Within the program, this study feeds TRX-04, which lifts the pair interaction into the transverse plane and recovers a rotating Lagrange triangle of beams in the Kerr photon fluid; TRX-08, which exchanges optical pulses for laser-cooled ions and reproduces the same spacing/breathing structure with a Coulomb tail; and TRX-09, the fluid-dynamical anchor where phases become circulations. Together with the celestial block (TRX-01, TRX-11) they demonstrate that the choreography sequence — pair law, collective equilibrium, normal spectrum, invariant — is portable across optics, fluids and celestial mechanics.

## 8. Conclusions

1. The pair binding law is exact: the numeric equilibrium reproduces r₀ = L·ln(2C₁/C₂) = ln(4/3) ≈ 0.287682 to 5.6e-17.
2. Binding is a phase-selection effect: the anti-phase lock Δφ = π/2 is purely repulsive over r ∈ [0.05, 20] (min force +6e-9 > 0), and the well exists only for |Δφ| < π/4.
3. A random triplet relaxes into an equally spaced molecule: d₁ = d₂ = 0.2018926516 with mismatch 2.2e-16 and offset from the analytic chain equilibrium s* only 2.8e-17.
4. The molecule is compressed 29.8 % below the pair spacing by the far-pair attraction (F(s*) + F(2s*) = 0) — a quantified genuine three-body effect.
5. The conservative molecule is a clean invariant system: energy drift 1.8e-15 over t = 100 at DOP853 rtol = atol = 1e-12.
6. The breathing spectrum is verified: FFT peak f = 0.469765 against the Hessian mode 0.468766 (agreement 0.21 %, tolerance 1 %), and the phase sweep yields the full stability map with both modes softening to zero at Δφ = π/4.

## 9. References

1. Zabusky, N. J., Kruskal, M. D. (1965). *Interaction of "solitons" in a collisionless plasma and the recurrence of initial states.* Phys. Rev. Lett. 15, 240–243.
2. Hasegawa, A., Tappert, F. (1973). *Transmission of stationary nonlinear optical pulses in dispersive dielectric fibers. I. Anomalous dispersion.* Appl. Phys. Lett. 23, 142–144.
3. Mollenauer, L. F., Stolen, R. H., Gordon, J. P. (1980). *Experimental observation of picosecond pulse narrowing and solitons in optical fibers.* Phys. Rev. Lett. 45, 1095–1098.
4. Karpman, V. I., Solov'ev, V. V. (1981). *A perturbational approach to the two-soliton systems with third-order dispersion.* Physica D 3, 487–502.
5. Gordon, J. P. (1983). *Interaction forces among solitons in optical fibers.* Optics Letters 8, 596–598.
6. Malomed, B. A. (1991). *Multistability and cyclic dynamics of solitons in dispersive media.* Phys. Rev. A 44, 6954.
7. Stratmann, M., Pagel, T., Mitschke, F. (2005). *Experimental observation of temporal soliton molecules.* Phys. Rev. Lett. 95, 143902.
8. Herink, G., Kurtz, F., Jalali, B., Solli, D. R., Ropers, C. (2017). *Real-time spectral interferometry probes the internal dynamics of femtosecond soliton molecules.* Science 356, 50–54.

### BibTeX

```bibtex
@article{gordon1983,
  author  = {Gordon, J. P.},
  title   = {Interaction forces among solitons in optical fibers},
  journal = {Optics Letters},
  year    = {1983}, volume = {8}, pages = {596--598}}

@article{karpman1981,
  author  = {Karpman, V. I. and Solov'ev, V. V.},
  title   = {A perturbational approach to the two-soliton systems with third-order dispersion},
  journal = {Physica D},
  year    = {1981}, volume = {3}, pages = {487--502}}

@article{stratmann2005,
  author  = {Stratmann, M. and Pagel, T. and Mitschke, F.},
  title   = {Experimental observation of temporal soliton molecules},
  journal = {Physical Review Letters},
  year    = {2005}, volume = {95}, pages = {143902}}

@article{herink2017,
  author  = {Herink, G. and Kurtz, F. and Jalali, B. and Solli, D. R. and Ropers, C.},
  title   = {Real-time spectral interferometry probes the internal dynamics of femtosecond soliton molecules},
  journal = {Science},
  year    = {2017}, volume = {356}, pages = {50--54}}
```

## Appendix A. Parameter table

| Symbol | Value | Role |
|---|---|---|
| C₁, C₂ | 2, 3 | potential coefficients: core repulsion / tail attraction |
| L | 1 | tail length; unit of all lengths |
| m | 1 | pulse mass; unit of mass |
| Δφ | 0 (preset); sweep 0 … 0.75 rad | locking phase; binding threshold π/4 |
| r₀ | ln(4/3) ≈ 0.287682 | pair equilibrium at Δφ = 0 |
| s* | 0.2018926516 | chain equilibrium, root of F(s) + F(2s) = 0 |
| V″(r₀) | 2.25 | curvature of the pair well at the minimum |
| relaxation | {1.0, 2.0, 3.5}, γ_d = 1, T = 90 | assembly run, DOP853 rtol = 1e-11 |
| conservative run | +0.01 on the middle pulse, γ_d = 0, T = 100 | breathing run, DOP853 rtol = atol = 1e-12 |
| chain modes | 2.4536, 2.9453 rad (0.390507, 0.468766 cyclic) | normal-mode spectrum at s* |

## Appendix B. Reproduction

```bash
python3 research/TRX-03-soliton-molecule/code/trx03_soliton_molecule.py --smoke     # < 20 s
python3 research/TRX-03-soliton-molecule/code/trx03_soliton_molecule.py              # full, 1.2 s (4.7 s with --figures)
python3 research/TRX-03-soliton-molecule/code/trx03_soliton_molecule.py --figures   # + 300-DPI figures
```

Full runtime on the reference machine: 1.2 s (4.7 s with --figures); smoke mode completes in under 20 seconds and is exercised by the repository CI.

## Appendix C. Environment

Python ≥ 3.11, numpy ≥ 2.0, scipy ≥ 1.14, matplotlib ≥ 3.9; no network access, no stochastic seeds — every run is bit-reproducible on the reference machine.
