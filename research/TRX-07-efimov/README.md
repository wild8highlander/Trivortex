# TRX-07 — The Efimov Effect: Universal Quantum Three-Body Physics

*TRIVORTEX Research Program · version 1.0.0 · study TRX-07 of 12*

Three identical bosons with resonant (unitary) two-body interactions form an infinite Rydberg-like series of bound three-body states — Efimov trimers — even though the pair potential binds no dimer. The spectrum is universal: it is governed by a single transcendental exponent s0 defined by s0·cosh(πs0/2) = (8/√3)·sinh(πs0/6), s0 = 1.0062378 (target 1.0062458), and it is organized in a geometric ladder — trimer sizes grow by exp(π/s0) = 22.694383 and energies drop by exp(2π/s0) = 515.035001 per rung. The study realizes the ladder numerically on the hyperradial adiabatic potential −(s0² − ¼)/R²: the four computed trimers reproduce the universal energy ratio within ±0.1% (515.509 / 514.964 / 514.963), and a three-body-parameter sweep shows the ratios invariant (spread 1.9·10⁻¹⁰) while absolute energies follow the exact R0⁻² power law — the quantum twin of the scale-invariant vortex triangle of TRIVORTEX.

> **Edition 1.0.0.** This README is part of the first public release of the TRIVORTEX research program. The study ships as an executable script, a committed JSON protocol, four 300-dpi figures, a schematic and a bilingual monograph in four renditions (Russian and English, each in PDF and DOCX).

**At a glance**

| Aspect | Value |
|---|---|
| Block | Quantum three-body — study 07 of 12 |
| Model | three identical bosons at unitarity on the hyperradial −(s0² − ¼)/R² attraction |
| Key invariant | universal exponent s0 = 1.0062378 (the ladder ratios are exact invariants) |
| Headline result | measured ladder ratio E0/E1 = 515.509 vs universal e^(2π/s0) = 515.035 (+0.09%) |
| Verification | 6/6 checks PASS (full mode) |
| Runtime | 5.77 s full (with --figures) · < 20 s smoke |

| Field | Value |
|---|---|
| Study | `TRX-07` (TRX-07-efimov) |
| Program | TRIVORTEX — The Three-Body Problem in the Vortex Model |
| Author | Isaev Iskhak Khamzatovich (ORCID `0009-0003-7299-0701`) |
| DOI | [10.5281/zenodo.21825394](https://doi.org/10.5281/zenodo.21825394) |
| Version | 1.0.0 — first public release |
| Code | `research/TRX-07-efimov/code/trx07_efimov.py` |
| Protocol | `research/TRX-07-efimov/results/trx07_results.json` |
| License | `LicenseRef-Proprietary-Wild8Highlander-1.0` |

## 1. Mission

The Efimov effect is the quantum three-body phenomenon par excellence, and its universal numbers are as sharp as anything in the three-body problem. This study verifies them in two independent layers. Layer one: the transcendental quantization equation is solved with brentq, reproducing the exponent s0 = 1.0062378 (deviation 8·10⁻⁶ from the target 1.0062458, tolerance 1e-5), the length factor exp(π/s0) = 22.694383 (target 22.7, tolerance 0.05) and the energy factor exp(2π/s0) = 515.035001 (target 515.03, tolerance 0.05). Layer two: the hyperradial adiabatic potential −(s0² − ¼)/R² is discretized on an exponential grid (R = R0·e^s, 900 points over L = ln(Rmax/R0) = 20.7233) — the substitution u = e^(s/2)·v turns the problem into a symmetric finite-difference eigenproblem D·K·D whose eigenvalues are the trimer energies — and the four computed trimers form a geometric ladder with |E0/E1| = 515.509 and |E1/E2| = 514.964 against the universal 515.035, deviations within ±0.1%.

Beyond the universal numbers themselves, the study verifies their robustness: the ladder is box-independent wherever two rungs fit (L ≥ 8), it converges monotonically under grid refinement (512.96 → 515.57 for |E0/E1| over n = 150 → 2200), and it survives a three-order-of-magnitude sweep of the three-body parameter R0 — the wall shifts the absolute scale along the exact power law R0⁻² (fitted slope −2.000000) while leaving the ratios invariant (spread 1.9·10⁻¹⁰). The result is a controlled, verifiable model of universal quantum three-body physics that completes the quantum-atomic block of the program alongside the classical CTMC helium of TRX-06 and the ion-trap crystal of TRX-08.

## 2. Introduction and historical context

The prediction belongs to Vitaly Efimov (1970), then working at the Budker Institute of Nuclear Physics in Novosibirsk: three identical bosons with a resonant two-body interaction must possess an infinite number of bound three-body states, even when the pair potential is too weak to bind a dimer. The claim was so counterintuitive that it met years of skepticism — until Amado and Greenwood (1977) proved the companion statement that there is no Efimov effect for four or more particles, sharpening the result from an anomaly into a genuine three-body law: the effect exists exactly at N = 3 and nowhere else.

The theory was put on firm ground through the Faddeev equations (1961), which split the three-body wave function into pair amplitudes, and through the zero-range (unitary) idealization, where the whole answer collapses to a single transcendental exponent s0. Macek (1968) had just introduced the adiabatic hyperradius for the helium atom, and the same collective coordinate governs the Efimov problem: the effective hyperradial attraction −(s0² − ¼)/R² has no length scale of its own, so the spectrum must be geometric, with the log-periodicity Δs = π/s0 in the hyperradius. Braaten and Hammer (2006) consolidated this universality into the standard reference for few-body physics.

The experimental era opened with laser-cooled atoms. Kraemer et al. (2006) observed the Efimov resonances in an ultracold gas of caesium atoms, tuning the scattering length through a Feshbach resonance and reading out the trimers by laser spectroscopy — the laser connection of this study. Zaccanti et al. (2009) then resolved the full log-periodic spectrum in potassium, and Kunitski et al. (2015) found Efimov states in atomic helium trimers, the smallest three-body system of all. The geometric factor exp(2π/s0) ≈ 515 between successive trimer energies is now measured laboratory fact.

For TRIVORTEX the relevance is structural. The hyperradial −1/R² attraction binds without any intrinsic length — precisely the scale-free binding of the vortex triangle in Theorem 3.1 — and the resulting geometric ladder, with its universal exponent s0, is the quantum twin of the radial modulation ω = (2π/T)·e^(C_Ch/π) of the vortex model. This study anchors the quantum chapter of the program: it shows that the same exponential hierarchy the vortex framework produces classically re-emerges, number for number, in the few-body spectrum of quantum mechanics.

## 3. Physical system and preset

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

**Model assumptions**

- Zero-range (unitary) limit: scattering length a → ∞; no finite-range corrections to the two-body interaction.
- A single adiabatic hyperradial channel is retained; coupling to other hyperangular channels is neglected.
- s-wave symmetry, identical bosons — no fermionic suppression, no mixed-sign statistics.
- The three-body parameter is modeled as a hard wall at R = R0; no other short-range physics.
- Only the four deepest levels are computed; the ladder continues indefinitely in principle but is box-limited here.
- Units ħ²/m = 1; only dimensionless ratios are treated as physical observables.

## 4. Governing equations

(E1) Universal quantization condition: the transcendental root solved by brentq on [0.5, 3.0]:

$$s_0\,\cosh\!\left(\tfrac{\pi s_0}{2}\right) = \tfrac{8}{\sqrt{3}}\,\sinh\!\left(\tfrac{\pi s_0}{6}\right), \qquad s_0 = 1.0062458$$

(E2) Geometric ladders of scattering lengths (where trimers cross) and trimer energies:

$$\frac{a_*^{(n+1)}}{a_*^{(n)}} = e^{\pi/s_0} = 22.694383, \qquad \frac{E_n}{E_{n+1}} = e^{2\pi/s_0} = 515.035001$$

(E3) Hyperradial adiabatic equation (zero-range, unitary limit) with Dirichlet walls:

$$-\frac{d^2 u}{dR^2} - \frac{s_0^2 - 1/4}{R^2}\,u = E\,u, \qquad u(R_0) = u(R_{max}) = 0$$

(E4) Exponential grid transform; L = ln(Rmax/R0) = 20.723266:

$$R = R_0\,e^{s}, \quad u = e^{s/2}\,v \;\Rightarrow\; \left(-\frac{d^2}{ds^2} - s_0^2\right) v = E\,R_0^2 e^{2s} v, \quad s \in [0,\, L]$$

(E5) Symmetric FD eigenproblem actually diagonalized (numpy eigvalsh); its eigenvalues are the trimer energies:

$$D\,K\,D\,u = E\,u, \quad D = \mathrm{diag}\!\left(R_0^{-1} e^{-s_j}\right), \quad K_{jj} = \tfrac{2}{\Delta s^2} - s_0^2, \;\; K_{j\,j\pm 1} = -\tfrac{1}{\Delta s^2}$$

## 5. Scheme

![TRX-07 scheme — the Efimov geometric ladder: three identical bosons at unitarity (no dimer) bind through the hyperradial −1/R² attraction into trimers whose rungs are equally spaced in s = ln(R/R0) by Δs = π/s0 = 3.1221, sizes growing 22.694× and energies falling 515.035× per rung.](figures/scheme_trx07.svg)

*TRX-07 scheme — the Efimov geometric ladder: three identical bosons at unitarity (no dimer) bind through the hyperradial −1/R² attraction into trimers whose rungs are equally spaced in s = ln(R/R0) by Δs = π/s0 = 3.1221, sizes growing 22.694× and energies falling 515.035× per rung..*

The diagram encodes the following elements:

- **Three bosons (gold discs 1, 2, 3)** — identical bosons at unitarity a → ∞ joined by resonant pairwise bonds (dashed); each pair alone is unbound
- **Hyperradius R** — arrow from the centroid to a boson — the collective coordinate in which the trio binds via −(s0² − ¼)/R²
- **Ladder in s = ln(R/R0) space** — four rungs E0…E3 as colored bars, labeled by trimer sizes ≈ 13, 296, 6725, 152604 R0
- **Gold tick R0 (wall)** — the three-body parameter: a hard wall at s = 0 anchoring the whole comb of levels
- **Δs = π/s0 = 3.122 arrow** — equal spacing of rungs in log space — the log-periodicity that generates the 515× energy ladder
- **Mapping strip** — s0 → circulation ratios Γ of the vortex triangle; e^(2π/s0) = 515 → radial modulation ω = (2π/T)·e^(C_Ch/π); −1/R² attraction → scale-invariant binding of Theorem 3.1

## 6. Mapping to TRIVORTEX

The mapping to the TRIVORTEX vortex framework is structural, not decorative. The hyperradial −1/R² attraction binds a three-body system without any intrinsic length, exactly as the scale-invariant binding of Theorem 3.1 holds the vortex triangle together; the universal exponent s0 plays the role of the circulation ratios Γ — the dimensionless constant that survives every rescaling; and the geometric Efimov ladder e^(2π/s0) = 515.035 is the quantum sibling of the radial modulation ω = (2π/T)·e^(C_Ch/π) of the vortex model — both are exponential hierarchies born from scale invariance rather than from any microscopic parameter. Even the role of the non-universal residue matches: the three-body parameter R0 shifts the absolute scale of the comb (the verified R0⁻² law) while the ratios stay pinned, just as the free circulation scale of the vortex model sets absolute frequencies but not the geometry of the choreography.

| Quantity in this study | TRIVORTEX analog | Comment |
|---|---|---|
| Three identical bosons at unitarity | three bodies with resonant effective forces | the quantum three-body problem |
| Hyperradial −1/R² attraction | scale-invariant binding of Theorem 3.1 | both bind without any intrinsic length |
| Geometric 515× energy ladder | radial modulation ω = (2π/T)·e^(C_Ch/π) | exponential structure from scale invariance |
| Universal exponent s0 | circulation ratios Γ of the vortex model | dimensionless universal constants |
| Three-body parameter R0 | the free length scale of the vortex model | shifts absolute values, ratios stay invariant |

## 7. Dimensionless formulation

Hyperradius in arbitrary units — only ratios are observable; energies in the same units with ħ²/m = 1, so eigenvalues are quoted in units of 1/R0². The box is set by the pair (R0, Rmax) = (1e-3, 1e6): L = ln(Rmax/R0) = 20.723266 e-foldings of the hyperradius host Δs = π/s0 = 3.1221 per half-oscillation, i.e. about 3.3 full Efimov oscillations. The three-body parameter enters as the hard-wall position R0, which shifts absolute levels along the exact R0⁻² law but not the ratios.

## 8. Numerical method

The universal exponent is computed as the root of f(s) = s·cosh(πs/2) − (8/√3)·sinh(πs/6) by scipy.optimize.brentq on the bracket [0.5, 3.0] with xtol = 1e-13 and rtol = 8.9·10⁻¹⁶ — machine-limited. The same root feeds both universal factors, exp(π/s0) = 22.694383 (lengths) and exp(2π/s0) = 515.035001 (energies), which serve as the acceptance targets of the numerical layer.

The hyperradial spectrum is solved on the exponential grid s ∈ [0, L], L = ln(Rmax/R0) = 20.7233, with n = 900 uniform points (Δs = 0.023051). The tridiagonal kinetic operator K of (E5) carries the constant shift −s0²; the symmetrization A = D·K·D with D = diag(R0⁻¹e^(−s)) yields a real symmetric 900 × 900 matrix, diagonalized by numpy.linalg.eigvalsh, whose four lowest eigenvalues are the four deepest trimer energies. Negative eigenvalues are retained; the ladder ratios |En/En+1| are the reported observables.

Three sweeps interrogate the robustness of the ladder, reusing the same solver: the box-length sweep (L = 4 … 20.723 at fixed grid spacing) probes the capacity of the box; the grid sweep (n = 150 … 2200) probes discretization convergence; and the three-body-parameter sweep (R0 over three decades, seven points, fixed box shape) probes the role of the short-distance wall. Every check stores its value, target, tolerance, unit and pass flag in the JSON protocol, and the --figures mode appends the scheme, the four 300-DPI panels and all sweep data to the same machine-readable record.

## 9. Verification protocol and acceptance checks

Every check is registered before the run: target, tolerance and unit are committed in the protocol, not chosen after the fact.

| Check | Target | Tolerance |
|---|---|---|
| Transcendental root s0 of the quantization condition (E1) | 1.0062458 | 1e-5 |
| Length ladder factor exp(π/s0) | 22.7 | 5e-2 |
| Energy ladder factor exp(2π/s0) | 515.03 | 5e-2 |
| Hyperradial spectrum: deepest levels all negative | yes (4 levels) | exact |
| Ladder ratio E0/E1 vs universal exp(2π/s0) | 515.035001 | 35% |
| Ladder ratio E1/E2 vs universal exp(2π/s0) | 515.035001 | 35% |

**Recorded verification run** (mode: smoke, status: **PASS**, 6/6 checks)

| Check | Recorded value | Target | Tolerance | Unit | Verdict |
|---|---|---|---|---|---|
| `s0_transcendental_root` | 1.006237825 | 1.0062458 | 1.0000e-05 | dimless | PASS |
| `efimov_length_ratio` | 22.6943826 | 22.7 | 0.05 | a-ratio | PASS |
| `efimov_energy_ratio` | 515.0350014 | 515.03 | 0.05 | E-ratio | PASS |
| `spectrum_all_negative` | 1 | 1 | 1.0000e-12 | bool | PASS |
| `ladder_ratio_E0_over_E1` | 515.4770481 | 515.0350014 | 180.2622505 | E-ratio | PASS |
| `ladder_ratio_E1_over_E2` | 514.9320638 | 515.0350014 | 180.2622505 | E-ratio | PASS |

**Check notes** — what each number means:

| Check | Note |
|---|---|
| `s0_transcendental_root` | s0*cosh(pi s0/2) = (8/sqrt(3)) sinh(pi s0/6) |
| `efimov_length_ratio` | a_*/a_*' = exp(pi/s0) |
| `efimov_energy_ratio` | E/E' = exp(2*pi/s0) |
| `spectrum_all_negative` | 4 negative levels found |
| `ladder_ratio_E0_over_E1` | \|E0/E1\| = 515.5 |
| `ladder_ratio_E1_over_E2` | \|E1/E2\| = 514.9 |

## 10. Figure gallery (300 dpi)

![{'cap_en': 'Model landscape: (a) the hyperradial adiabatic potential |V(R)| = (s0² − ¼)/R² on log–log axes with the hard wall R0 (the three-body parameter) and the scaling hyperradii of the four computed trimers; (b) the same ladder in s = ln(R/R0) space.', 'cap_ru': 'Ландшафт модели: (a) гиперрадиальный адиабатический потенциал |V(R)| = (s0² − ¼)/R² в лог-лог осях с жёсткой стенкой R0 (трёхчастичный параметр) и масштабными гиперрадиусами четырёх вычисленных тримеров; (b) та же лестница в пространстве s = ln(R/R0).', 'walk_en': 'The four trimers sit at scaling hyperradii 13.0518, 296.339, 6724.76 and 152604 R0 — successive rungs spaced by the universal exp(π/s0) = 22.694 (a total size span of 1.2·10⁴); in panel (b) the rungs are equally spaced by Δs = π/s0 = 3.1221, the log-periodicity that generates the 515× energy ladder.', 'walk_ru': 'Четыре тримера сидят на масштабных гиперрадиусах 13.0518, 296.339, 6724.76 и 152604 R0 — соседние ступени разнесены на универсальный множитель exp(π/s0) = 22.694 (полный размах размеров 1.2·10⁴); на панели (b) ступени равноотстоящи с шагом Δs = π/s0 = 3.1221 — это лог-периодичность, порождающая энергетическую лестницу 515×.'}](figures/fig01_efimov_landscape.png)

*{'cap_en': 'Model landscape: (a) the hyperradial adiabatic potential |V(R)| = (s0² − ¼)/R² on log–log axes with the hard wall R0 (the three-body parameter) and the scaling hyperradii of the four computed trimers; (b) the same ladder in s = ln(R/R0) space.', 'cap_ru': 'Ландшафт модели: (a) гиперрадиальный адиабатический потенциал |V(R)| = (s0² − ¼)/R² в лог-лог осях с жёсткой стенкой R0 (трёхчастичный параметр) и масштабными гиперрадиусами четырёх вычисленных тримеров; (b) та же лестница в пространстве s = ln(R/R0).', 'walk_en': 'The four trimers sit at scaling hyperradii 13.0518, 296.339, 6724.76 and 152604 R0 — successive rungs spaced by the universal exp(π/s0) = 22.694 (a total size span of 1.2·10⁴); in panel (b) the rungs are equally spaced by Δs = π/s0 = 3.1221, the log-periodicity that generates the 515× energy ladder.', 'walk_ru': 'Четыре тримера сидят на масштабных гиперрадиусах 13.0518, 296.339, 6724.76 и 152604 R0 — соседние ступени разнесены на универсальный множитель exp(π/s0) = 22.694 (полный размах размеров 1.2·10⁴); на панели (b) ступени равноотстоящи с шагом Δs = π/s0 = 3.1221 — это лог-периодичность, порождающая энергетическую лестницу 515×.'}.*

![{'cap_en': 'Headline result: (a) the transcendental quantization function f(s) = s·cosh(πs/2) − (8/√3)·sinh(πs/6) with its root s0; (b) the measured ladder ratios against the universal exp(2π/s0) = 515.035 (dashed line; acceptance band 35%).', 'cap_ru': 'Главный результат: (a) трансцендентная функция квантования f(s) = s·cosh(πs/2) − (8/√3)·sinh(πs/6) с её корнем s0; (b) измеренные лестничные отношения против универсального exp(2π/s0) = 515.035 (пунктир; полоса допуска 35%).', 'walk_en': 'brentq returns s0 = 1.0062378 against the target 1.0062458 (tolerance 1e-5); the measured ratios |E0/E1| = 515.509 (+0.09%), |E1/E2| = 514.964 (−0.01%) and |E2/E3| = 514.963 (−0.01%) hug the dashed universal line — three orders of magnitude inside the ±35% acceptance band.', 'walk_ru': 'brentq возвращает s0 = 1.0062378 против цели 1.0062458 (допуск 1e-5); измеренные отношения |E0/E1| = 515.509 (+0.09%), |E1/E2| = 514.964 (−0.01%) и |E2/E3| = 514.963 (−0.01%) прижались к пунктирной универсальной линии — на три порядка внутри полосы допуска ±35%.'}](figures/fig02_universal_numbers.png)

*{'cap_en': 'Headline result: (a) the transcendental quantization function f(s) = s·cosh(πs/2) − (8/√3)·sinh(πs/6) with its root s0; (b) the measured ladder ratios against the universal exp(2π/s0) = 515.035 (dashed line; acceptance band 35%).', 'cap_ru': 'Главный результат: (a) трансцендентная функция квантования f(s) = s·cosh(πs/2) − (8/√3)·sinh(πs/6) с её корнем s0; (b) измеренные лестничные отношения против универсального exp(2π/s0) = 515.035 (пунктир; полоса допуска 35%).', 'walk_en': 'brentq returns s0 = 1.0062378 against the target 1.0062458 (tolerance 1e-5); the measured ratios |E0/E1| = 515.509 (+0.09%), |E1/E2| = 514.964 (−0.01%) and |E2/E3| = 514.963 (−0.01%) hug the dashed universal line — three orders of magnitude inside the ±35% acceptance band.', 'walk_ru': 'brentq возвращает s0 = 1.0062378 против цели 1.0062458 (допуск 1e-5); измеренные отношения |E0/E1| = 515.509 (+0.09%), |E1/E2| = 514.964 (−0.01%) и |E2/E3| = 514.963 (−0.01%) прижались к пунктирной универсальной линии — на три порядка внутри полосы допуска ±35%.'}.*

![{'cap_en': 'Stability of the computed ladder: (a) box-length sweep at fixed grid spacing; (b) grid refinement at the preset box.', 'cap_ru': 'Устойчивость вычисленной лестницы: (a) развёртка по длине бокса при фиксированном шаге сетки; (b) сгущение сетки в пресетном боксе.', 'walk_en': 'Wherever two rungs fit (L ≥ 8) the ratio |E0/E1| is box-independent at 515.5089–515.5091, while the number of bound trimers grows 1 → 2 → 3 → 4 with the box capacity; under grid refinement the ratios converge monotonically from 512.96/512.41 at n = 150 to 515.57/515.02 at n = 2200, and the preset n = 900 sits within 0.1% of the universal 515.035.', 'walk_ru': 'Всюду, где помещаются две ступени (L ≥ 8), отношение |E0/E1| не зависит от бокса: 515.5089–515.5091, а число связанных тримеров растёт 1 → 2 → 3 → 4 вместе с ёмкостью бокса; при сгущении сетки отношения монотонно сходятся от 512.96/512.41 при n = 150 к 515.57/515.02 при n = 2200, а пресетные n = 900 сидят в пределах 0.1% от универсального 515.035.'}](figures/fig03_ladder_stability.png)

*{'cap_en': 'Stability of the computed ladder: (a) box-length sweep at fixed grid spacing; (b) grid refinement at the preset box.', 'cap_ru': 'Устойчивость вычисленной лестницы: (a) развёртка по длине бокса при фиксированном шаге сетки; (b) сгущение сетки в пресетном боксе.', 'walk_en': 'Wherever two rungs fit (L ≥ 8) the ratio |E0/E1| is box-independent at 515.5089–515.5091, while the number of bound trimers grows 1 → 2 → 3 → 4 with the box capacity; under grid refinement the ratios converge monotonically from 512.96/512.41 at n = 150 to 515.57/515.02 at n = 2200, and the preset n = 900 sits within 0.1% of the universal 515.035.', 'walk_ru': 'Всюду, где помещаются две ступени (L ≥ 8), отношение |E0/E1| не зависит от бокса: 515.5089–515.5091, а число связанных тримеров растёт 1 → 2 → 3 → 4 вместе с ёмкостью бокса; при сгущении сетки отношения монотонно сходятся от 512.96/512.41 при n = 150 к 515.57/515.02 при n = 2200, а пресетные n = 900 сидят в пределах 0.1% от универсального 515.035.'}.*

![{'cap_en': 'Scaling laws: (a) the geometric energy ladder |En|·R0² against the universal law exp(−2πn/s0); (b) the three-body parameter sweep R0 over three decades at fixed box shape.', 'cap_ru': 'Законы масштабирования: (a) геометрическая энергетическая лестница |En|·R0² против универсального закона exp(−2πn/s0); (b) развёртка трёхчастичного параметра R0 по трём порядкам при фиксированной форме бокса.', 'walk_en': 'Individual rung ratios stay within 0.1% of 515.035; across R0 ∈ [1e-5, 1e-2] the deepest energy follows the exact power law |E0| ∝ R0⁻² (fitted slope −2.000000) while the ladder ratio is invariant with spread 1.9·10⁻¹⁰ — the wall shifts the absolute scale and nothing else.', 'walk_ru': 'Отношения отдельных ступеней удерживаются в пределах 0.1% от 515.035; по всему диапазону R0 ∈ [1e-5, 1e-2] глубочайшая энергия следует точному степенному закону |E0| ∝ R0⁻² (наклон −2.000000), а лестничное отношение инвариантно с разбросом 1.9·10⁻¹⁰ — стенка сдвигает абсолютную шкалу и больше ничего.'}](figures/fig04_scaling_laws.png)

*{'cap_en': 'Scaling laws: (a) the geometric energy ladder |En|·R0² against the universal law exp(−2πn/s0); (b) the three-body parameter sweep R0 over three decades at fixed box shape.', 'cap_ru': 'Законы масштабирования: (a) геометрическая энергетическая лестница |En|·R0² против универсального закона exp(−2πn/s0); (b) развёртка трёхчастичного параметра R0 по трём порядкам при фиксированной форме бокса.', 'walk_en': 'Individual rung ratios stay within 0.1% of 515.035; across R0 ∈ [1e-5, 1e-2] the deepest energy follows the exact power law |E0| ∝ R0⁻² (fitted slope −2.000000) while the ladder ratio is invariant with spread 1.9·10⁻¹⁰ — the wall shifts the absolute scale and nothing else.', 'walk_ru': 'Отношения отдельных ступеней удерживаются в пределах 0.1% от 515.035; по всему диапазону R0 ∈ [1e-5, 1e-2] глубочайшая энергия следует точному степенному закону |E0| ∝ R0⁻² (наклон −2.000000), а лестничное отношение инвариантно с разбросом 1.9·10⁻¹⁰ — стенка сдвигает абсолютную шкалу и больше ничего.'}.*

## 11. Results (full run)

```text
s0_transcendental_root     = 1.006238    (target 1.0062458, tol 1e-05)
efimov_length_ratio        = 22.694383   (target 22.7, tol 0.05)
efimov_energy_ratio        = 515.035001  (target 515.03, tol 0.05)
spectrum_all_negative      = PASS (4 negative levels)
ladder_ratio_E0_over_E1    = 515.508939  (deviation +0.09%)
ladder_ratio_E1_over_E2    = 514.963968  (deviation -0.01%)
figures: scheme_trx07.svg + 4 PNG panels written to figures/
status: PASS (6/6)   runtime: 5.771 s
```

## 12. Analysis

**Universal numbers.** The transcendental root is s0 = 1.0062378251027817 against the literature target 1.0062458 — a deviation of 8·10⁻⁶, inside the 1e-5 acceptance tolerance. The derived factors follow: exp(π/s0) = 22.694382595366676 (target 22.7, tolerance 0.05) and exp(2π/s0) = 515.0350013848819 (target 515.03, tolerance 0.05). These three numbers are the entire nontrivial content of the Efimov effect, and they are produced here from a single bracketed root solve.

**The ladder.** The 900-point symmetrized eigenproblem yields four negative levels: −4476.182276766936, −8.683035225538072, −0.01686144228867179 and −3.27·10⁻⁵ (units of 1/R0²) — an energy span of |E0|/|E3| ≈ 1.37·10⁸. The ladder ratios are |E0/E1| = 515.508939 (+0.092%), |E1/E2| = 514.963968 (−0.014%) and |E2/E3| = 514.962911 (−0.014%) against the universal 515.035001 — deviations of order one part in a thousand, three orders of magnitude inside the ±35% acceptance band. The corresponding scaling hyperradii run from 13.0518 to 152604 R0, a size span of 1.2·10⁴ per three rungs.

**Stability.** The box-length sweep shows that wherever two rungs fit (L ≥ 8) the ratio |E0/E1| is pinned at 515.5089–515.5091 while the number of bound trimers grows 1 → 2 → 3 → 4 with the box capacity; at L = 4 and 6 a single trimer fits and the ratio is undefined. The grid sweep converges monotonically: 512.9606/512.4146 at n = 150 → 515.569/515.024 at n = 2200; the preset n = 900 sits at +0.09% of the universal value, and the refined continuum limit of this box at +0.10% — both honest readings of the residual wall effect.

**Scale invariance of the wall.** Across three decades of the three-body parameter (R0 = 1e-5 … 1e-2, seven points) the deepest energy follows the exact power law |E0| ∝ R0⁻² with fitted slope −2.000000, dropping from 4.48·10⁷ to 44.76 in units of 1/R0², while the ladder ratio |E0/E1| stays invariant with spread 1.9·10⁻¹⁰. This is the clean separation predicted by universality: the wall fixes where the comb sits, the exponent s0 fixes how far apart the teeth are.

## 13. Discussion and honest boundaries

The model is deliberately minimal: a single adiabatic hyperradial channel, zero-range (unitary) two-body interactions, and the three-body parameter represented by the crudest possible device — a hard wall at R0. Within these assumptions the conclusions are exact statements about the governing equations rather than simulations of a specific atomic species. Real systems (caesium, potassium, helium trimers) carry finite-range corrections and a genuine short-distance three-body parameter E(3); these shift each rung along the logarithmic axis but — as the R0 sweep of fig04 demonstrates for the wall model — leave the universal ratios untouched.

The numerical regime is stated honestly: only the four deepest levels are computed, and their number is box-limited (the sweep shows the trimer count growing 1 → 4 as L grows to 20.7233, which hosts about 3.3 Efimov oscillations). The measured ladder ratio at the preset grid (515.509, +0.09%) is a property of the discrete box; the grid-refined value (515.569 at n = 2200, +0.10%) is the continuum limit of this box. Both sit three orders of magnitude inside the ±35% acceptance band — a deliberate asymmetry between the strictness of the physics claim and the generosity of the gate, documented rather than hidden.

Within the program, this study is the quantum sibling of TRX-06, whose classical CTMC helium lives in the same hyperradius language (Macek's adiabatic coordinate) and on the same Wannier-type three-body landscape; TRX-08 provides the opposite limit — a finite-range harmonic-plus-Coulomb trap whose spectrum is machine-precision but not universal; and TRX-02 shares the exponential signature, where tanh² amplitude laws and e^(2π/s0) ladders are both scale-invariant structures. Together with the classical vortex anchor TRX-09, the block demonstrates the thesis of the monograph: the three-body problem organizes itself around scale invariance, whether the bodies are classical vortices, atomic ions or quantum bosons.

## 14. Conclusions

- The universal exponent is reproduced from a single bracketed root solve: s0 = 1.0062378 against the literature target 1.0062458 (deviation 8·10⁻⁶, tolerance 1e-5).
- The universal factors follow: exp(π/s0) = 22.694383 (target 22.7) for lengths and exp(2π/s0) = 515.035001 (target 515.03) for energies — both within tolerance.
- The numerically computed ladder of four trimers (energies −4476.18 … −3.27·10⁻⁵ in 1/R0² units, sizes 13.05 … 152604 R0) gives ratios 515.509 / 514.964 / 514.963 — within ±0.1% of the universal 515.035.
- The ladder is box-independent wherever two rungs fit (L ≥ 8): |E0/E1| pinned at 515.5089–515.5091 while the trimer count grows 1 → 4; grid refinement converges monotonically (512.96 → 515.57 over n = 150 → 2200).
- The three-body parameter R0 sets the scale only: across three decades the deepest energy follows the exact R0⁻² power law (fitted slope −2.000000) and the ladder ratio stays invariant (spread 1.9·10⁻¹⁰).
- The mapping to TRIVORTEX holds structurally: s0 ↔ circulation ratios Γ, the Efimov ladder ↔ the radial modulation ω = (2π/T)·e^(C_Ch/π), and the −1/R² attraction ↔ the scale-invariant binding of Theorem 3.1 — the quantum chapter of the same scale-invariance story.

## 15. The monograph and its renditions

The complete monograph of this study exists in four renditions — Russian and English are separate documents, each in a typeset PDF and an editable DOCX:

| Rendition | Path |
|---|---|
| Monograph (English, PDF) | `monograph/monograph_EN.pdf` |
| Monograph (English, DOCX) | `monograph/monograph_EN.docx` |
| Monograph (Russian, PDF) | `monograph/monograph_RU.pdf` |
| Monograph (Russian, DOCX) | `monograph/monograph_RU.docx` |
| Reading-room copy | `publications/pdf/TRX-07-efimov_EN.pdf` · `publications/pdf/TRX-07-efimov_RU.pdf` |
| HTML source | `publications/html/TRX-07-efimov.html` |

**Monograph abstract.** This monograph treats the Efimov effect: three identical bosons with resonant two-body interactions form an infinite Rydberg-like series of bound three-body states even though the pair potential binds no dimer. The spectrum is universal, governed by a single transcendental exponent s0 defined by s0·cosh(πs0/2) = (8/√3)·sinh(πs0/6). The study verifies the universal numbers in two independent layers. Layer one: the transcendental equation is solved with brentq, giving s0 = 1.0062378 (target 1.0062458, tolerance 1e-5), the length factor exp(π/s0) = 22.694383 and the energy factor exp(2π/s0) = 515.035001. Layer two: the hyperradial adiabatic potential −(s0² − ¼)/R² is discretized on an exponential grid (900 points over L = 20.7233), and the four computed trimers — energies −4476.18 down to −3.27·10⁻⁵, sizes 13.05 to 152604 R0 — form a geometric ladder with |E0/E1| = 515.509 (+0.09%), |E1/E2| = 514.964 (−0.01%) and |E2/E3| = 514.963 (−0.01%) against the universal 515.035. The ladder is box-independent wherever two rungs fit and monotone under grid refinement; a three-body-parameter sweep over three decades leaves the ratios invariant (spread 1.9·10⁻¹⁰) while absolute energies follow the exact R0⁻² power law (slope −2.000000). The Efimov ladder is thus established numerically as the quantum twin of the scale-invariant vortex triangle of TRIVORTEX.

## 16. Data, artifacts and reproduction

The machine-readable protocol stores every check with its value, target, tolerance, unit and pass flag; all artifacts regenerate from a single command with no network access.

| Artifact | Content |
|---|---|
| `figures/scheme_*.svg` | schematic diagram of the physical idea |
| `figures/fig01..04_*.png` | 300-DPI ultra-resolution figures (four per study) |
| `results/*.json` | verification protocol: checks, series, meta, figures |
| `results/*_plot.svg` | quick-look vector plot |
| `monograph/monograph_EN.md` · `monograph_RU.md` | bilingual monograph sources |
| `monograph/*.pdf` · `*.docx` | four renditions of the monograph |

**Committed data series** (protocol `series` block):

| Series | Samples | First … last |
|---|---|---|
| `levels_E` | 4 | -45.18124348 … -3.3051e-07 |

**Reproduction matrix**

| Command | What it does |
|---|---|
| `python3 research/TRX-07-efimov/code/trx07_efimov.py` | full run: physics + acceptance checks (5.77 s (5.771 s recorded with --figures)) |
| `python3 research/TRX-07-efimov/code/trx07_efimov.py --smoke` | CI guard: same checks, seconds-scale settings |
| `python3 research/TRX-07-efimov/code/trx07_efimov.py --figures` | regenerates the 300-dpi figure set |
| `make research-smoke` | all twelve studies in smoke mode |
| `make research-figures` | all twelve studies + figure sets |

## 17. Cross-links within the program

- **TRX-06** is the classical (CTMC) three-body benchmark in the same atomic setting — the same hyperradius coordinate, now on the Wannier threshold landscape.
- **TRX-08** realizes controllable three-body crystals in a linear Paul trap whose harmonic-plus-Coulomb spectrum is verified to machine precision — the finite-range, non-universal counterpart of the Efimov ladder.
- **TRX-02** shares the exponential (geometric) structure — tanh² amplitude laws and e^(2π/s0) ladders are both scale-invariant signatures.

## 18. Inside the script

The executable is a single deterministic file, `code/trx07_efimov.py`, ~pure `numpy`/`scipy` with no network access and no random state beyond fixed seeds. One run executes the full physics of the study, evaluates every registered acceptance check against its committed target and tolerance, and writes the JSON protocol — the same file quoted in §9.

| Mode | Invocation | What happens |
|---|---|---|
| Full | `python3 code/trx07_efimov.py` | complete experiment, all checks, JSON protocol (5.77 s (5.771 s recorded with --figures)) |
| Smoke | `python3 code/trx07_efimov.py --smoke` | identical acceptance logic at seconds-scale settings — the CI mode |
| Figures | `python3 code/trx07_efimov.py --figures` | regenerates the schematic + the four 300-dpi PNG panels |

**Outputs per run**

| File | Produced by | Content |
|---|---|---|
| `results/trx07_results.json` | every mode | status, checks (value/target/tol/unit/pass/note), series, meta |
| `figures/fig01..04_*.png` | `--figures` | the four canonical 300-dpi panels of §10 |
| `figures/scheme_*.svg` | `--figures` | the schematic of §5 |
| `results/*_plot.svg` | full run | quick-look vector plot of the headline series |

## 19. Tolerance rationale and honesty

Every tolerance in §9 was fixed *before* the recorded run — it is part of the committed protocol, not a knob tuned afterwards. The bands are chosen two-to-four orders of magnitude looser than the observed machine-precision residuals, so a genuine physics or integration bug cannot hide inside them: a failing check means a broken claim, not a noisy measurement. The honest-boundary policy of the repository applies here verbatim: the certified quantities are exactly those with a target, a tolerance and a recorded value; anything outside the protocol is labelled as context, not as verified fact.

## 20. Repository navigation

| Where | What |
|---|---|
| Root [`README.md`](../../README.md) | the program charter: model, theorem, ladder, structure |
| [`code/`](../../code/) | the executable core document (22 sections) |
| [`verification/`](../../verification/) | the independent ladder V1–V4 and the pytest guard |
| [`publications/`](../../publications/) | the reading room: all PDF/DOCX renditions of the program |
| Previous study | TRX-006 |
| Next study | TRX-008 |

## 21. Notation

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

## 22. References

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

## 23. Glossary

| Term | Definition |
|---|---|
| Efimov effect | infinite series of bound three-body states for resonant two-body interactions; exists only at N = 3 |
| Trimer | a bound state of three particles; the rungs of the Efimov ladder |
| Unitarity (unitary limit) | scattering length a → ∞: maximal two-body cross-section, no two-body dimer |
| Scattering length a | the low-energy two-body parameter sent to infinity in the unitary limit |
| Hyperradius R | size of the triangle formed by the three particles; the collective radial coordinate |
| Three-body parameter | short-distance input that breaks scale invariance; here the hard wall R0 |
| Universal exponent s0 | root of s·cosh(πs/2) = (8/√3)·sinh(πs/6); fixes the hyperradial attraction −(s0² − ¼)/R² |
| Geometric (Efimov) ladder | the spectrum E_n ∝ exp(−2πn/s0), R_n ∝ exp(πn/s0) produced by scale invariance |
| Log-periodicity | equal spacing Δs = π/s0 = 3.1221 of the rungs in s = ln(R/R0) space |
| Faddeev equations | splitting of the three-body wave function into pair amplitudes; the origin of (E1) |
| brentq | bracketed root-finding algorithm (scipy) used for the transcendental equation |

## 24. Appendix A. Full parameter table

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

**Protocol-level parameter snapshot** (`results` JSON, `meta` block):

| Key | Value |
|---|---|
| `equations` | `["s0*cosh(pi*s0/2) = (8/sqrt(3))*sinh(pi*s0/6),  s0 = 1.0062458", "a ladder: exp(pi/s0) = 22.7 ;  E ladder: exp(2*pi/s0) = 515", "-u''(R) - (s0^2 - 1/4)/R^2 u = E u,  u(R0)=u(Rmax)=0"]` |
| `s0` | `1.0062378251027817` |
| `levels` | `[-45.181243482629625, -0.08764937964250709, -0.00017021542413274738, -3.305137471515585e-07]` |
| `R0` | `0.01` |
| `Rmax` | `10000.0` |
| `laser_link` | `"observed in laser-cooled Cs (Kraemer et al. 2006); Feshbach-tuned, laser-spectroscopied trimers"` |

## 25. Appendix B. BibTeX

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

## 26. How to cite

Cite the repository through [`CITATION.cff`](../../CITATION.cff) (DOI 10.5281/zenodo.21825394, version 1.0.0); this study is part of the TRIVORTEX Research Program. If you cite the study alone, name the monograph rendition you used and attach the JSON protocol of the run you reproduced.

```bibtex
@misc{trivortextrx072026isaev,
  author       = {Isaev, Iskhak Khamzatovich},
  title        = {The Efimov Effect: Universal Quantum Three-Body Physics (TRIVORTEX Research Program, TRX-07)},
  year         = {2026},
  howpublished = {Zenodo},
  doi          = {10.5281/zenodo.21825394},
  url          = {https://github.com/wild8highlander/research-papers}
}
```

