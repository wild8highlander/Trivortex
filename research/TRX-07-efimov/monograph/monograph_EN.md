# The Efimov Effect: Universal Quantum Three-Body Physics

*TRIVORTEX Research Program · v1.0.0 · Monograph Edition*

|  |  |
|---|---|
| Study | TRX-07 |
| Program | TRIVORTEX — The Three-Body Problem in the Vortex Model |
| Author | Isaev Iskhak Khamzatovich (ORCID 0009-0003-7299-0701) |
| DOI | 10.5281/zenodo.21825394 |
| Date | 2026-10-06 |
| Code | `code/trx07_efimov.py` |
| Data | `results/trx07_results.json` |

## Abstract

This monograph treats the Efimov effect: three identical bosons with resonant two-body interactions form an infinite Rydberg-like series of bound three-body states even though the pair potential binds no dimer. The spectrum is universal, governed by a single transcendental exponent s0 defined by s0·cosh(πs0/2) = (8/√3)·sinh(πs0/6). The study verifies the universal numbers in two independent layers. Layer one: the transcendental equation is solved with brentq, giving s0 = 1.0062378 (target 1.0062458, tolerance 1e-5), the length factor exp(π/s0) = 22.694383 and the energy factor exp(2π/s0) = 515.035001. Layer two: the hyperradial adiabatic potential −(s0² − ¼)/R² is discretized on an exponential grid (900 points over L = 20.7233), and the four computed trimers — energies −4476.18 down to −3.27·10⁻⁵, sizes 13.05 to 152604 R0 — form a geometric ladder with |E0/E1| = 515.509 (+0.09%), |E1/E2| = 514.964 (−0.01%) and |E2/E3| = 514.963 (−0.01%) against the universal 515.035. The ladder is box-independent wherever two rungs fit and monotone under grid refinement; a three-body-parameter sweep over three decades leaves the ratios invariant (spread 1.9·10⁻¹⁰) while absolute energies follow the exact R0⁻² power law (slope −2.000000). The Efimov ladder is thus established numerically as the quantum twin of the scale-invariant vortex triangle of TRIVORTEX.

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

The prediction belongs to Vitaly Efimov (1970), then working at the Budker Institute of Nuclear Physics in Novosibirsk: three identical bosons with a resonant two-body interaction must possess an infinite number of bound three-body states, even when the pair potential is too weak to bind a dimer. The claim was so counterintuitive that it met years of skepticism — until Amado and Greenwood (1977) proved the companion statement that there is no Efimov effect for four or more particles, sharpening the result from an anomaly into a genuine three-body law: the effect exists exactly at N = 3 and nowhere else.

The theory was put on firm ground through the Faddeev equations (1961), which split the three-body wave function into pair amplitudes, and through the zero-range (unitary) idealization, where the whole answer collapses to a single transcendental exponent s0. Macek (1968) had just introduced the adiabatic hyperradius for the helium atom, and the same collective coordinate governs the Efimov problem: the effective hyperradial attraction −(s0² − ¼)/R² has no length scale of its own, so the spectrum must be geometric, with the log-periodicity Δs = π/s0 in the hyperradius. Braaten and Hammer (2006) consolidated this universality into the standard reference for few-body physics.

The experimental era opened with laser-cooled atoms. Kraemer et al. (2006) observed the Efimov resonances in an ultracold gas of caesium atoms, tuning the scattering length through a Feshbach resonance and reading out the trimers by laser spectroscopy — the laser connection of this study. Zaccanti et al. (2009) then resolved the full log-periodic spectrum in potassium, and Kunitski et al. (2015) found Efimov states in atomic helium trimers, the smallest three-body system of all. The geometric factor exp(2π/s0) ≈ 515 between successive trimer energies is now measured laboratory fact.

For TRIVORTEX the relevance is structural. The hyperradial −1/R² attraction binds without any intrinsic length — precisely the scale-free binding of the vortex triangle in Theorem 3.1 — and the resulting geometric ladder, with its universal exponent s0, is the quantum twin of the radial modulation ω = (2π/T)·e^(C_Ch/π) of the vortex model. This study anchors the quantum chapter of the program: it shows that the same exponential hierarchy the vortex framework produces classically re-emerges, number for number, in the few-body spectrum of quantum mechanics.

## 2. Physical formulation

The system is three identical bosons in the unitary limit: the s-wave scattering length a is tuned to infinity (a → ∞), so the two-body subsystem binds no dimer yet scatters with the maximal cross-section. The natural collective coordinate is the hyperradius R — the size of the triangle formed by the three particles — and in the zero-range limit the adiabatic (Born–Oppenheimer-like) separation of the fast hyperangular motion leaves a single effective channel: a hyperradial attraction −(s0² − ¼)/R², whose strength s0² − ¼ ≈ 0.7625 is fixed entirely by the transcendental condition (E1) on the exponent s0 = 1.0062378.

The −1/R² attraction is marginal: it carries no intrinsic length scale, so any bound state must build its own scale out of the boundaries. Quantum mechanics supplies it multiplicatively — the outcome is the geometric Efimov ladder, with sizes R_n ∝ exp(πn/s0) and energies E_n ∝ exp(−2πn/s0). The one microscopic length that does enter is the three-body parameter R0, here modeled as a hard wall at R = R0 that anchors the comb of levels; shifting R0 slides every rung but leaves all ratios invariant — verified by the sweep of fig04 over three decades of R0.

| Parameter | Value | Meaning |
|---|---|---|
| Universal exponent s0 | 1.0062378 (target 1.0062458, tol 1e-5) | transcendental root of (E1) |
| Universal length factor | exp(π/s0) = 22.694383 | trimer size growth per rung |
| Universal energy factor | exp(2π/s0) = 515.035001 | trimer energy drop per rung |
| Three-body parameter R0 | 1e-3 | hard wall in R (short-distance phase) |
| Outer wall Rmax | 1e6 | box hosts L = ln(Rmax/R0) = 20.723266 ≈ 3.3 Efimov oscillations |
| FD grid | 900 points, Δs = 0.023051 | uniform in s = ln(R/R0) |
| Levels computed | 4 deepest trimers | energies −4476.18 … −3.27·10⁻⁵ (units of 1/R0²) |

## 3. Mathematical model

At unitarity the zero-range Faddeev equations reduce, in hyperspherical coordinates, to an eigenvalue problem for the hyperangular part of the wave function. The spectral parameter of that hyperangular problem, s0, enters the consistency condition (E1): f(s) = s·cosh(πs/2) − (8/√3)·sinh(πs/6) = 0. Its positive root s0 = 1.0062458 (the literature value; the brentq root of this study is 1.0062378) fixes the strength of the effective hyperradial channel, s0² − ¼ ≈ 0.7625, and nothing else — the entire Efimov phenomenology flows from this single number.

With the angular part frozen in the attractive channel, the hyperradial equation (E3) is scale-invariant: under R → λR the kinetic and potential terms rescale identically, so from any bound solution with energy E a new one exists at E·λ⁻². Self-similarity under the discrete step λ = exp(π/s0) closes the hierarchy: the wave-function node structure repeats after each half-turn of the log-periodic oscillation, giving the geometric ladder E_n ∝ exp(−2πn/s0) and R_n ∝ exp(πn/s0). In s = ln(R/R0) space the problem becomes translation-invariant with period π/s0 = 3.1221 — the origin of the equal rung spacing of fig01(b).

The only scale that breaks this invariance is the three-body parameter: short-range physics at distances where the zero-range idealization fails. The study models it as a hard wall at R = R0 (Dirichlet in (E3)); the outer boundary at Rmax completes the box. On the exponential grid s = ln(R/R0) with u = e^(s/2)·v the equation becomes (E4), and the symmetrization D·K·D of (E5) — D = diag(R0⁻¹e^(−s)) — produces a real symmetric matrix whose four lowest eigenvalues are exactly the four deepest trimer energies; the ladder ratios are the reported observables.

**Notation**

| Symbol | Meaning |
|---|---|
| s0 | universal Efimov exponent, root of (E1); computed 1.0062378, target 1.0062458 |
| R | hyperradius of the three-particle triangle |
| R0 | three-body parameter: hard wall at short distance (value 1e-3) |
| Rmax | outer Dirichlet wall of the box (value 1e6) |
| L | box length in log space, L = ln(Rmax/R0) = 20.723266 |
| s | logarithmic hyperradius, s = ln(R/R0) ∈ [0, L] |
| u(R), v(s) | hyperradial wave function and its log-grid image (u = e^(s/2)·v) |
| E_n | n-th trimer energy (units of 1/R0²); E0 = −4476.18 … E3 = −3.27·10⁻⁵ |
| Δs = π/s0 | ladder spacing in log space = 3.1221 |
| a_* | scattering length at which the n-th trimer appears; a_* ladder factor exp(π/s0) |
| ħ²/m | unit-setting quantum combination, set to 1 |

**(E1)** Universal quantization condition: the transcendental root solved by brentq on [0.5, 3.0].

$$s_0\,\cosh\!\left(\tfrac{\pi s_0}{2}\right) = \tfrac{8}{\sqrt{3}}\,\sinh\!\left(\tfrac{\pi s_0}{6}\right), \qquad s_0 = 1.0062458$$

**(E2)** Geometric ladders of scattering lengths (where trimers cross) and trimer energies.

$$\frac{a_*^{(n+1)}}{a_*^{(n)}} = e^{\pi/s_0} = 22.694383, \qquad \frac{E_n}{E_{n+1}} = e^{2\pi/s_0} = 515.035001$$

**(E3)** Hyperradial adiabatic equation (zero-range, unitary limit) with Dirichlet walls.

$$-\frac{d^2 u}{dR^2} - \frac{s_0^2 - 1/4}{R^2}\,u = E\,u, \qquad u(R_0) = u(R_{max}) = 0$$

**(E4)** Exponential grid transform; L = ln(Rmax/R0) = 20.723266.

$$R = R_0\,e^{s}, \quad u = e^{s/2}\,v \;\Rightarrow\; \left(-\frac{d^2}{ds^2} - s_0^2\right) v = E\,R_0^2 e^{2s} v, \quad s \in [0,\, L]$$

**(E5)** Symmetric FD eigenproblem actually diagonalized (numpy eigvalsh); its eigenvalues are the trimer energies.

$$D\,K\,D\,u = E\,u, \quad D = \mathrm{diag}\!\left(R_0^{-1} e^{-s_j}\right), \quad K_{jj} = \tfrac{2}{\Delta s^2} - s_0^2, \;\; K_{j\,j\pm 1} = -\tfrac{1}{\Delta s^2}$$

## 4. Connection to the TRIVORTEX framework

The mapping to the TRIVORTEX vortex framework is structural, not decorative. The hyperradial −1/R² attraction binds a three-body system without any intrinsic length, exactly as the scale-invariant binding of Theorem 3.1 holds the vortex triangle together; the universal exponent s0 plays the role of the circulation ratios Γ — the dimensionless constant that survives every rescaling; and the geometric Efimov ladder e^(2π/s0) = 515.035 is the quantum sibling of the radial modulation ω = (2π/T)·e^(C_Ch/π) of the vortex model — both are exponential hierarchies born from scale invariance rather than from any microscopic parameter. Even the role of the non-universal residue matches: the three-body parameter R0 shifts the absolute scale of the comb (the verified R0⁻² law) while the ratios stay pinned, just as the free circulation scale of the vortex model sets absolute frequencies but not the geometry of the choreography.

| Quantity in this study | TRIVORTEX analog | Comment |
|---|---|---|
| Three identical bosons at unitarity | three bodies with resonant effective forces | the quantum three-body problem |
| Hyperradial −1/R² attraction | scale-invariant binding of Theorem 3.1 | both bind without any intrinsic length |
| Geometric 515× energy ladder | radial modulation ω = (2π/T)·e^(C_Ch/π) | exponential structure from scale invariance |
| Universal exponent s0 | circulation ratios Γ of the vortex model | dimensionless universal constants |
| Three-body parameter R0 | the free length scale of the vortex model | shifts absolute values, ratios stay invariant |

## 5. Numerical method

The universal exponent is computed as the root of f(s) = s·cosh(πs/2) − (8/√3)·sinh(πs/6) by scipy.optimize.brentq on the bracket [0.5, 3.0] with xtol = 1e-13 and rtol = 8.9·10⁻¹⁶ — machine-limited. The same root feeds both universal factors, exp(π/s0) = 22.694383 (lengths) and exp(2π/s0) = 515.035001 (energies), which serve as the acceptance targets of the numerical layer.

The hyperradial spectrum is solved on the exponential grid s ∈ [0, L], L = ln(Rmax/R0) = 20.7233, with n = 900 uniform points (Δs = 0.023051). The tridiagonal kinetic operator K of (E5) carries the constant shift −s0²; the symmetrization A = D·K·D with D = diag(R0⁻¹e^(−s)) yields a real symmetric 900 × 900 matrix, diagonalized by numpy.linalg.eigvalsh, whose four lowest eigenvalues are the four deepest trimer energies. Negative eigenvalues are retained; the ladder ratios |En/En+1| are the reported observables.

Three sweeps interrogate the robustness of the ladder, reusing the same solver: the box-length sweep (L = 4 … 20.723 at fixed grid spacing) probes the capacity of the box; the grid sweep (n = 150 … 2200) probes discretization convergence; and the three-body-parameter sweep (R0 over three decades, seven points, fixed box shape) probes the role of the short-distance wall. Every check stores its value, target, tolerance, unit and pass flag in the JSON protocol, and the --figures mode appends the scheme, the four 300-DPI panels and all sweep data to the same machine-readable record.

## 6. Results and analysis

### fig01 efimov landscape

![Model landscape: (a) the hyperradial adiabatic potential |V(R)| = (s0² − ¼)/R² on log–log axes with the hard wall R0 (the three-body parameter) and the scaling hyperradii of the four computed trimers; (b) the same ladder in s = ln(R/R0) space.](../figures/fig01_efimov_landscape.png)

*Model landscape: (a) the hyperradial adiabatic potential |V(R)| = (s0² − ¼)/R² on log–log axes with the hard wall R0 (the three-body parameter) and the scaling hyperradii of the four computed trimers; (b) the same ladder in s = ln(R/R0) space.*
The four trimers sit at scaling hyperradii 13.0518, 296.339, 6724.76 and 152604 R0 — successive rungs spaced by the universal exp(π/s0) = 22.694 (a total size span of 1.2·10⁴); in panel (b) the rungs are equally spaced by Δs = π/s0 = 3.1221, the log-periodicity that generates the 515× energy ladder.

### fig02 universal numbers

![Headline result: (a) the transcendental quantization function f(s) = s·cosh(πs/2) − (8/√3)·sinh(πs/6) with its root s0; (b) the measured ladder ratios against the universal exp(2π/s0) = 515.035 (dashed line; acceptance band 35%).](../figures/fig02_universal_numbers.png)

*Headline result: (a) the transcendental quantization function f(s) = s·cosh(πs/2) − (8/√3)·sinh(πs/6) with its root s0; (b) the measured ladder ratios against the universal exp(2π/s0) = 515.035 (dashed line; acceptance band 35%).*
brentq returns s0 = 1.0062378 against the target 1.0062458 (tolerance 1e-5); the measured ratios |E0/E1| = 515.509 (+0.09%), |E1/E2| = 514.964 (−0.01%) and |E2/E3| = 514.963 (−0.01%) hug the dashed universal line — three orders of magnitude inside the ±35% acceptance band.

### fig03 ladder stability

![Stability of the computed ladder: (a) box-length sweep at fixed grid spacing; (b) grid refinement at the preset box.](../figures/fig03_ladder_stability.png)

*Stability of the computed ladder: (a) box-length sweep at fixed grid spacing; (b) grid refinement at the preset box.*
Wherever two rungs fit (L ≥ 8) the ratio |E0/E1| is box-independent at 515.5089–515.5091, while the number of bound trimers grows 1 → 2 → 3 → 4 with the box capacity; under grid refinement the ratios converge monotonically from 512.96/512.41 at n = 150 to 515.57/515.02 at n = 2200, and the preset n = 900 sits within 0.1% of the universal 515.035.

### fig04 scaling laws

![Scaling laws: (a) the geometric energy ladder |En|·R0² against the universal law exp(−2πn/s0); (b) the three-body parameter sweep R0 over three decades at fixed box shape.](../figures/fig04_scaling_laws.png)

*Scaling laws: (a) the geometric energy ladder |En|·R0² against the universal law exp(−2πn/s0); (b) the three-body parameter sweep R0 over three decades at fixed box shape.*
Individual rung ratios stay within 0.1% of 515.035; across R0 ∈ [1e-5, 1e-2] the deepest energy follows the exact power law |E0| ∝ R0⁻² (fitted slope −2.000000) while the ladder ratio is invariant with spread 1.9·10⁻¹⁰ — the wall shifts the absolute scale and nothing else.

**Universal numbers.** The transcendental root is s0 = 1.0062378251027817 against the literature target 1.0062458 — a deviation of 8·10⁻⁶, inside the 1e-5 acceptance tolerance. The derived factors follow: exp(π/s0) = 22.694382595366676 (target 22.7, tolerance 0.05) and exp(2π/s0) = 515.0350013848819 (target 515.03, tolerance 0.05). These three numbers are the entire nontrivial content of the Efimov effect, and they are produced here from a single bracketed root solve.

**The ladder.** The 900-point symmetrized eigenproblem yields four negative levels: −4476.182276766936, −8.683035225538072, −0.01686144228867179 and −3.27·10⁻⁵ (units of 1/R0²) — an energy span of |E0|/|E3| ≈ 1.37·10⁸. The ladder ratios are |E0/E1| = 515.508939 (+0.092%), |E1/E2| = 514.963968 (−0.014%) and |E2/E3| = 514.962911 (−0.014%) against the universal 515.035001 — deviations of order one part in a thousand, three orders of magnitude inside the ±35% acceptance band. The corresponding scaling hyperradii run from 13.0518 to 152604 R0, a size span of 1.2·10⁴ per three rungs.

**Stability.** The box-length sweep shows that wherever two rungs fit (L ≥ 8) the ratio |E0/E1| is pinned at 515.5089–515.5091 while the number of bound trimers grows 1 → 2 → 3 → 4 with the box capacity; at L = 4 and 6 a single trimer fits and the ratio is undefined. The grid sweep converges monotonically: 512.9606/512.4146 at n = 150 → 515.569/515.024 at n = 2200; the preset n = 900 sits at +0.09% of the universal value, and the refined continuum limit of this box at +0.10% — both honest readings of the residual wall effect.

**Scale invariance of the wall.** Across three decades of the three-body parameter (R0 = 1e-5 … 1e-2, seven points) the deepest energy follows the exact power law |E0| ∝ R0⁻² with fitted slope −2.000000, dropping from 4.48·10⁷ to 44.76 in units of 1/R0², while the ladder ratio |E0/E1| stays invariant with spread 1.9·10⁻¹⁰. This is the clean separation predicted by universality: the wall fixes where the comb sits, the exponent s0 fixes how far apart the teeth are.

### Verification summary

| Check | Recorded value | Target | Tolerance | Pass |
|---|---|---|---|---|
| `s0_transcendental_root` | 1.00624 | 1.00625 | 1e-05 | yes |
| `efimov_length_ratio` | 22.6944 | 22.7 | 0.05 | yes |
| `efimov_energy_ratio` | 515.035 | 515.03 | 0.05 | yes |
| `spectrum_all_negative` | 1 | 1 | 1e-12 | yes |
| `ladder_ratio_E0_over_E1` | 515.509 | 515.035 | 1.8e+02 | yes |
| `ladder_ratio_E1_over_E2` | 514.964 | 515.035 | 1.8e+02 | yes |

*(status: **PASS**, mode: full)*

## 7. Discussion

The model is deliberately minimal: a single adiabatic hyperradial channel, zero-range (unitary) two-body interactions, and the three-body parameter represented by the crudest possible device — a hard wall at R0. Within these assumptions the conclusions are exact statements about the governing equations rather than simulations of a specific atomic species. Real systems (caesium, potassium, helium trimers) carry finite-range corrections and a genuine short-distance three-body parameter E(3); these shift each rung along the logarithmic axis but — as the R0 sweep of fig04 demonstrates for the wall model — leave the universal ratios untouched.

The numerical regime is stated honestly: only the four deepest levels are computed, and their number is box-limited (the sweep shows the trimer count growing 1 → 4 as L grows to 20.7233, which hosts about 3.3 Efimov oscillations). The measured ladder ratio at the preset grid (515.509, +0.09%) is a property of the discrete box; the grid-refined value (515.569 at n = 2200, +0.10%) is the continuum limit of this box. Both sit three orders of magnitude inside the ±35% acceptance band — a deliberate asymmetry between the strictness of the physics claim and the generosity of the gate, documented rather than hidden.

Within the program, this study is the quantum sibling of TRX-06, whose classical CTMC helium lives in the same hyperradius language (Macek's adiabatic coordinate) and on the same Wannier-type three-body landscape; TRX-08 provides the opposite limit — a finite-range harmonic-plus-Coulomb trap whose spectrum is machine-precision but not universal; and TRX-02 shares the exponential signature, where tanh² amplitude laws and e^(2π/s0) ladders are both scale-invariant structures. Together with the classical vortex anchor TRX-09, the block demonstrates the thesis of the monograph: the three-body problem organizes itself around scale invariance, whether the bodies are classical vortices, atomic ions or quantum bosons.

## 8. Conclusions

1. The universal exponent is reproduced from a single bracketed root solve: s0 = 1.0062378 against the literature target 1.0062458 (deviation 8·10⁻⁶, tolerance 1e-5).
2. The universal factors follow: exp(π/s0) = 22.694383 (target 22.7) for lengths and exp(2π/s0) = 515.035001 (target 515.03) for energies — both within tolerance.
3. The numerically computed ladder of four trimers (energies −4476.18 … −3.27·10⁻⁵ in 1/R0² units, sizes 13.05 … 152604 R0) gives ratios 515.509 / 514.964 / 514.963 — within ±0.1% of the universal 515.035.
4. The ladder is box-independent wherever two rungs fit (L ≥ 8): |E0/E1| pinned at 515.5089–515.5091 while the trimer count grows 1 → 4; grid refinement converges monotonically (512.96 → 515.57 over n = 150 → 2200).
5. The three-body parameter R0 sets the scale only: across three decades the deepest energy follows the exact R0⁻² power law (fitted slope −2.000000) and the ladder ratio stays invariant (spread 1.9·10⁻¹⁰).
6. The mapping to TRIVORTEX holds structurally: s0 ↔ circulation ratios Γ, the Efimov ladder ↔ the radial modulation ω = (2π/T)·e^(C_Ch/π), and the −1/R² attraction ↔ the scale-invariant binding of Theorem 3.1 — the quantum chapter of the same scale-invariance story.

## 9. References

1. Efimov, V. (1970). *Energy levels arising from resonant two-body forces in a three-body system.* Phys. Lett. B 33, 563–564.
2. Efimov, V. (1971). *Weakly bound states of three resonantly interacting particles.* Sov. J. Nucl. Phys. 12, 589–595.
3. Faddeev, L. D. (1961). *Scattering theory for a three-particle system.* Sov. Phys. JETP 12, 1014–1019.
4. Macek, J. H. (1968). *Properties of autoionizing states of He.* J. Phys. B 1, 831–843.
5. Amado, R. D., Greenwood, F. C. (1977). *There is no Efimov effect for four or more particle systems.* Phys. Rev. D 15, 838–840.
6. Braaten, E., Hammer, H.-W. (2006). *Universality in few-body systems with large scattering length.* Phys. Rep. 428, 259–390.
7. Kraemer, T. et al. (2006). *Evidence for Efimov quantum states in an ultracold gas of caesium atoms.* Nature 440, 315–319.
8. Zaccanti, M. et al. (2009). *Observation of an Efimov spectrum in an atomic system.* Nature Phys. 5, 586–591.
9. Chin, C., Grimm, R., Julienne, P., Tiesinga, E. (2010). *Feshbach resonances in ultracold gases.* Rev. Mod. Phys. 82, 1225–1286.
10. Kunitski, M. et al. (2015). *Three-body bound states in atomic helium trimers.* Science 348, 551–555.

### BibTeX

```bibtex
@article{efimov1970,
  author  = {Efimov, Vitaly},
  title   = {Energy levels arising from resonant two-body forces in a three-body system},
  journal = {Physics Letters B},
  year    = {1970}, volume = {33}, pages = {563--564}}

@article{braaten2006,
  author  = {Braaten, Eric and Hammer, Hans-Werner},
  title   = {Universality in few-body systems with large scattering length},
  journal = {Physics Reports},
  year    = {2006}, volume = {428}, pages = {259--390}}

@article{kraemer2006,
  author  = {Kraemer, Tobias and others},
  title   = {Evidence for Efimov quantum states in an ultracold gas of caesium atoms},
  journal = {Nature},
  year    = {2006}, volume = {440}, pages = {315--319}}

@article{chin2010,
  author  = {Chin, Cheng and Grimm, Rudolf and Julienne, Paul and Tiesinga, Eite},
  title   = {Feshbach resonances in ultracold gases},
  journal = {Reviews of Modern Physics},
  year    = {2010}, volume = {82}, pages = {1225--1286}}
```

## Appendix A. Parameter table

| Symbol | Value | Role |
|---|---|---|
| s0 | 1.0062378 (target 1.0062458, tol 1e-5) | universal exponent; strength of the hyperradial channel |
| brentq bracket | [0.5, 3.0], xtol = 1e-13 | root isolation of the transcendental equation |
| R0 | 1e-3 | three-body parameter (hard wall, short-distance phase) |
| Rmax | 1e6 | outer Dirichlet wall |
| L | 20.723266 | box length in s = ln(R/R0); ≈ 3.3 Efimov oscillations |
| n_grid | 900 | uniform FD grid points in s |
| Δs | 0.023051 | grid spacing in log space |
| levels | 4 | deepest trimers computed (negative eigenvalues) |
| exp(π/s0) | 22.694383 | universal size factor per rung |
| exp(2π/s0) | 515.035001 | universal energy factor per rung; ladder acceptance band ±35% |

## Appendix B. Reproduction

```bash
python3 research/TRX-07-efimov/code/trx07_efimov.py --smoke     # < 20 s
python3 research/TRX-07-efimov/code/trx07_efimov.py              # full, 5.77 s (5.771 s recorded with --figures)
python3 research/TRX-07-efimov/code/trx07_efimov.py --figures   # + 300-DPI figures
```

Full runtime on the reference machine: 5.77 s (5.771 s recorded with --figures); smoke mode completes in under 20 seconds and is exercised by the repository CI.

## Appendix C. Environment

Python ≥ 3.11, numpy ≥ 2.0, scipy ≥ 1.14, matplotlib ≥ 3.9; no network access, no stochastic seeds — every run is bit-reproducible on the reference machine.
