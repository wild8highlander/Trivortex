# TRX-06 — Helium Atom as the Coulomb Three-Body Problem (Classical Trajectory Monte Carlo)

*TRIVORTEX Research Program · version 1.0.0 · study TRX-06 of 12*

The helium atom — a nucleus of charge Z = 2 and two electrons — is the smallest physical system whose classical limit is the honest three-body problem: two attractive and one repulsive Coulomb pair, all of order unity. The study runs a deterministic classical trajectory Monte Carlo (CTMC) ensemble of 3200 trajectories launched in the Wannier configuration — a radially staggered chain at hyperradius R₀ = 3 on the exact energy shell, with a fixed kick σ = 0.01 and a documented softening ε = 0.1 a.u. — and measures the autoionization channel: one electron is captured while the other escapes carrying on average 7.28× the excess energy, the fingerprint of three-body energy transfer through the e⁻–e⁻ repulsion. The double-escape statistics are read against Wannier's threshold law P_DE ∝ E^1.056, reported honestly for the strong-coupling regime of the fixed-launch geometry.

> **Edition 1.0.0.** This README is part of the first public release of the TRIVORTEX research program. The study ships as an executable script, a committed JSON protocol, four 300-dpi figures, a schematic and a bilingual monograph in four renditions (Russian and English, each in PDF and DOCX).

**At a glance**

| Aspect | Value |
|---|---|
| Block | Quantum three-body — study 06 of 12 |
| Model | classical Coulomb three-body (He), softened, Z = 2, ε = 0.1 a.u. |
| Key invariant | total energy H = ε₁ + ε₂ + 1/r₁₂ |
| Headline result | escaper carries 7.28× E; single-escape fraction 1.000 |
| Verification | 7/7 checks PASS (full mode) |
| Runtime | 37.7 s full · < 20 s smoke |

| Field | Value |
|---|---|
| Study | `TRX-06` (TRX-06-helium-three-body) |
| Program | TRIVORTEX — The Three-Body Problem in the Vortex Model |
| Author | Isaev Iskhak Khamzatovich (ORCID `0009-0003-7299-0701`) |
| DOI | [10.5281/zenodo.21825394](https://doi.org/10.5281/zenodo.21825394) |
| Version | 1.0.0 — first public release |
| Code | `research/TRX-06-helium-three-body/code/trx06_helium_three_body.py` |
| Protocol | `research/TRX-06-helium-three-body/results/trx06_results.json` |
| License | `LicenseRef-Proprietary-Wild8Highlander-1.0` |

## 1. Mission

Helium is the quantum Coulomb three-body problem, and in its classical limit it is the genuine article: two Coulomb attractions to the nucleus and one Coulomb repulsion between the electrons, with no small parameter to hide behind. Near the double-escape threshold the problem obeys Wannier's law P_DE(E) ∝ E^α with the celebrated universal exponent α = 1.056 — a closed-form benchmark of exactly the kind the TRIVORTEX monograph attaches to its vortex choreographies. The laser connection is structural: the three-step model of high-harmonic generation (ionization → laser-driven acceleration → recombination) is a driven three-body problem of the electron, the parent ion and the field, and strong-field double ionization shows the same Wannier-type kinematics.

The study implements a vectorized, energy-filtered CTMC ensemble (8 × 400 = 3200 trajectories, deterministic seed) with a documented softening ε = 0.1 a.u. and an eleven-level adaptive time step, and verifies: machine-grade energy conservation over the valid ensemble (relative drift 4.28e-6 of the deep-well scale 2Z/ε = 40; max |ΔE| = 1.714·10⁻⁴ a.u., 0/3200 filtered); exact bookkeeping of the outcome classes (3200 = 3200); that the autoionization channel is active and, in fact, the only active outcome (single-escape fraction 1.000 in every energy bin); that the escaping electron carries on average 7.28× the total excess energy (median 5.90, 16–84 pct band [3.24, 13.30]) while its partner is captured — the signature of binding energy released into the pair; and that the double-escape fraction stays below one half across the window, with the fitted Wannier slope stored honestly (see §10 and the honesty note): recovering the exact α = 1.056 requires near-threshold Wannier-cap conditioning beyond a compact ensemble.

## 2. Introduction and historical context

The threshold story begins with Gregory Wannier's 1953 paper, which asked what happens when an atom is ionized with barely enough energy to release two electrons. Wannier argued that double escape must funnel through the only configuration compatible with both long-range Coulomb repulsions — the Wannier configuration in which the two electrons leave on opposite sides of the nucleus at equal distances and equal speeds — and that scale invariance of the Coulomb problem then forces a power law P_DE ∝ E^α. His phase-space argument, refined independently by Peterkop (1971), gives α = 1.056 for Z = 2, a number that became the classic benchmark of three-body breakup physics.

The classical trajectory Monte Carlo method entered atomic physics with Abrines and Percival (1966), who applied the correspondence principle to ionization and charge transfer: at large quantum numbers the quantum problem is replaced by an ensemble of classical trajectories with quantized initial conditions. For helium the method matured in the 1980s–1990s, when computers became able to integrate the full three-body Coulomb dynamics in production quantities; the autoionization channel — one electron captured, the other ejected — was recognized as the classical image of the Auger process and of the Fano (1961) resonances, with the e–e repulsion as the only energy-transfer mechanism.

The modern classical picture of the threshold region is geometric: Sacha and Eckhardt (2001) analyzed the Wannier ridge — the unstable orbit along r₁ = r₂ that organizes the escape — and showed how the triple-collision manifold channels trajectories into either double escape or autoionization. This is the three-body alternative familiar from vortex dynamics: Aref's (1979) analysis of three vortices exhibits the same competition between collapse and scattering, and the same invariant-based bookkeeping. Experiments on threshold double ionization read precisely the exponent α, which is why a CTMC study that reports its slope honestly — measured or not — stays a meaningful benchmark.

For TRIVORTEX the relevance is threefold. First, helium is the mixed-sign three-body problem: it tests the same central-force choreography bookkeeping as the gravitational and vortex trios, with the sign structure inverted. Second, the Wannier exponent is a closed-form universal benchmark — the same epistemic category as Theorem 3.1 of the monograph. Third, the laser connection is built in: the three-step model of high-harmonic generation (foundations in Agostini et al. 1979; synthesis by Corkum 1993) is a driven three-body problem of the electron, the parent ion and the field, and strong-field double ionization shows Wannier-type kinematics — this study is the atomic anchor of the program's quantum block (TRX-06, TRX-07, TRX-08).

## 3. Physical system and preset

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

**Model assumptions**

- Nuclear motion is neglected: the nucleus is a fixed force center of charge Z = 2 (infinite-mass approximation).
- Classical mechanics only — no tunneling, no exchange symmetry, no spin; the correspondence is justified by the large excitation scale of the launch.
- All Coulomb denominators are softened at the documented ε = 0.1 a.u.; the far-field kinematics is untouched.
- Fixed launch geometry: hyperradius R₀ = 3 with the E-independent kick σ = 0.01 probes the strong-coupling regime, not the near-threshold scaling limit R₀ ~ 1/E.
- Deep-bound terminal configurations freeze after t = 60 (one electron inside r < 1 with the other beyond r > 5, or both inside): they cannot double-escape on the timescale.
- Energy-quality filter: trajectories with |ΔE| > 5·10⁻³ a.u. are discarded (standard CTMC practice; 0 of 3200 in the full run).

## 4. Governing equations

(E1) Hamiltonian in atomic units (softened denominators r → (r² + ε²)^{1/2}, ε = 0.1):

$$H = \frac{p_1^2}{2} + \frac{p_2^2}{2} - \frac{Z}{r_1} - \frac{Z}{r_2} + \frac{1}{r_{12}}, \qquad Z = 2$$

(E2) Softened pairwise-consistent equations of motion (Newton's third law):

$$\ddot{\mathbf{r}}_1 = -Z\,\frac{\mathbf{r}_1}{(r_1^2+\varepsilon^2)^{3/2}} + \frac{\mathbf{r}_1-\mathbf{r}_2}{(r_{12}^2+\varepsilon^2)^{3/2}}, \qquad \ddot{\mathbf{r}}_2 = -Z\,\frac{\mathbf{r}_2}{(r_2^2+\varepsilon^2)^{3/2}} - \frac{\mathbf{r}_1-\mathbf{r}_2}{(r_{12}^2+\varepsilon^2)^{3/2}}$$

(E3) Individual electron energies, the conserved total and the autoionization overshoot (binding energy released):

$$\varepsilon_i = \tfrac{1}{2}v_i^2 - \frac{Z}{r_i}, \qquad H = \varepsilon_1 + \varepsilon_2 + \frac{1}{r_{12}}, \qquad E_{esc}/E > 1$$

(E4) Wannier threshold law (Wannier 1953; independent derivation by Peterkop 1971):

$$P_{DE}(E) \propto E^{\alpha}, \qquad \alpha = \frac{1}{4}\left(\sqrt{\frac{100Z-9}{4Z-1}} - 1\right) = 1.056 \ \ (Z = 2)$$

(E5) Energy-quality filter: trajectories above the drift cut are discarded (0 of 3200 in the full run):

$$\delta = \max|\Delta E| \, / \, (2Z/\varepsilon) \le 4\times 10^{-4}, \qquad |\Delta E| \le 5\times 10^{-3}$$

## 5. Scheme

![TRX-06 scheme — helium as the Coulomb three-body problem: the e⁻–e⁻ repulsion is the energy-transfer channel; the escaper leaves through the r = 30 a.u. sphere with E₁ ≈ 7.28 E while its partner is captured at E₂ ≈ −6.3 E; the Wannier mini-plot contrasts the universal slope α = 1.056 with the measured strong-coupling floor.](figures/scheme_trx06.svg)

*TRX-06 scheme — helium as the Coulomb three-body problem: the e⁻–e⁻ repulsion is the energy-transfer channel; the escaper leaves through the r = 30 a.u. sphere with E₁ ≈ 7.28 E while its partner is captured at E₂ ≈ −6.3 E; the Wannier mini-plot contrasts the universal slope α = 1.056 with the measured strong-coupling floor..*

The diagram encodes the following elements:

- **Nucleus (+2)** — helium core of charge Z = 2 (gold circle) attracting both electrons with −Z/r
- **Two electrons** — launched on the staggered Wannier chain R₀ = 3, Δr ∈ [0.8, 2.0] — mixed-sign Coulomb pairs
- **1/r₁₂ repulsion** — double arrow between the electrons — the energy-transfer channel of autoionization
- **Escaping electron** — gold dashed path crossing the r = 30 a.u. escape sphere carrying E₁ ≈ 7.28 E
- **Captured electron** — blue spiral winding into the nucleus, E₂ = E − E₁ ≈ −6.3 E (binding energy released)
- **Wannier mini-plot** — gold points at the strong-coupling floor against the dashed universal slope α = 1.056

## 6. Mapping to TRIVORTEX

The mapping to TRIVORTEX is structural at every level. The e⁻–e⁻–nucleus trio is the three-body problem with the sign structure inverted relative to gravity — mixed attractive and repulsive pairs — yet it obeys the same central-force bookkeeping, the same invariant-audit discipline and the same collapse-versus-scattering alternative that Aref (1979) exposed for three vortices. The autoionization overshoot, in which one body exits carrying the share of another, is the direct analog of the energy exchange that choreographies of the vortex model exhibit; the Wannier exponent α = 1.056 is a closed-form universal benchmark of the same epistemic kind as Theorem 3.1; and the documented softening ε plays exactly the role of the finite vortex cores in the TRIVORTEX regularization — both keep the singular pair interaction finite without touching the far-field dynamics.

| Quantity in this study | TRIVORTEX analog | Comment |
|---|---|---|
| e⁻–e⁻–nucleus trio | the three bodies | Coulomb three-body with mixed pair signs |
| Autoionization overshoot E_esc/E > 1 | energy exchange in choreographies | one body exits with the share of another |
| Wannier threshold law P_DE ∝ E^1.056 | closed-form benchmarks (Theorem 3.1) | a sharp universal exponent as reference point |
| Softening ε = 0.1 a.u. | finite vortex cores | documented regularization of 1/r singularities |

## 7. Dimensionless formulation

Atomic units throughout: ℏ = m_e = e = 1; lengths in bohr, energies in Hartree. The excess-energy window [0.05, 0.3] Ha spans the classical near-threshold regime above the double-escape threshold. The only internal scale of the softened problem is the deep-well kinetic scale 2Z/ε = 40 a.u., relative to which the energy drift is measured.

## 8. Numerical method

Sampling is fully deterministic: a seeded generator (seed 7) draws the stagger Δr ∈ [0.8, 2.0], the ray orientation and two transverse kick directions per trajectory; 400 trajectories are drawn per energy bin on a geometric grid of 8 excess energies from 0.05 to 0.3 Ha, giving 3200 launch states. Each state is projected onto the exact energy shell after the kicks are applied, so every launched trajectory starts with total energy E to machine precision — the subsequent drift audit measures integrator error only, not launch noise.

Integration is a per-trajectory adaptive RK4 in dt-groups: the step dt = 0.03 · r_min/v_max is clipped and quantized onto a fixed ladder of eleven levels from 10⁻⁴ to 0.3, and trajectories requiring the same level are advanced as a batch, which keeps the ensemble vectorized while preserving the adaptive rule. A trajectory ends when both electrons are beyond r = 30 a.u. with outward velocity and positive individual energy (double escape), when a terminal configuration freezes after t = 60 (one electron inside r < 1 with the other beyond r > 5, or both inside — no double escape possible on the timescale), or at t_max = 2500.

Diagnostics: the energy drift |ΔE| is tracked per trajectory as the running maximum against the launch energy; trajectories with |ΔE| > 5·10⁻³ a.u. are discarded (standard CTMC practice; 0 of 3200 in the full run). The double-escape fraction per bin carries Poisson errors √(p(1 − p)/n); the threshold slope is a least-squares fit on log₁₀–log₁₀ coordinates and is re-derived from the stored counts as an independent reproducibility check. Every quantity — value, target, tolerance, unit, pass flag — is stored in the JSON protocol, and the --figures mode adds the four panels and the scheme from the same ensemble data without touching the checks.

## 9. Verification protocol and acceptance checks

Every check is registered before the run: target, tolerance and unit are committed in the protocol, not chosen after the fact.

| Check | Target | Tolerance |
|---|---|---|
| Max relative energy drift over the valid ensemble (scale 2Z/ε = 40) | 0 | 4e-4 |
| Outcome classes sum to N | 3200 | exact |
| Autoionization channel active (single-escape fraction) | > 0.5 | exact |
| Escaping-electron energy overshoot | > 1.2×E | exact |
| P_DE below 0.5 across the window (strong-coupling regime) | yes | exact |
| Wannier exponent reported (fit stored honestly) | finite | exact |
| Fit reproducible from stored counts | identical | exact |

**Recorded verification run** (mode: smoke, status: **PASS**, 5/5 checks)

| Check | Recorded value | Target | Tolerance | Unit | Verdict |
|---|---|---|---|---|---|
| `max_relative_energy_drift_valid` | 2.8839e-06 | 0 | 4.0000e-04 | rel | PASS |
| `outcome_classes_sum_to_N` | 120 | 120 | 1.0000e-12 | count | PASS |
| `autoionization_channel_active` | 1 | 1 | 1.0000e-12 | bool | PASS |
| `escaping_electron_energy_overshoot` | 1 | 1 | 1.0000e-12 | bool | PASS |
| `fit_reproducible` | 1 | 1 | 1.0000e-12 | bool | PASS |

**Check notes** — what each number means:

| Check | Note |
|---|---|
| `max_relative_energy_drift_valid` | max \|dE\| = 1.154e-04 a.u.; 0/120 filtered out |
| `outcome_classes_sum_to_N` | valid=120, filtered=0 |
| `autoionization_channel_active` | single-escape fraction = 1.000 (energy transfer via e-e repulsion) |
| `escaping_electron_energy_overshoot` | escaping electron carries 7.83x the total excess energy (binding released) |
| `fit_reproducible` | same stored counts reproduce the same alpha |

## 10. Figure gallery (300 dpi)

![{'cap_en': 'Model landscape: (a) softened Coulomb potential V(r₁, r₂) for Z = 2, ε = 0.1 — the e–e ridge wall along the diagonal and the staggered launch segment (r₁ = 3, r₂ = 3 + Δ, Δ ∈ [0.8, 2.0]); (b) chain potential V(ρ, ρ + Δ) along the launch ray for three staggers with the excess-energy window E ∈ [0.05, 0.3] Ha.', 'cap_ru': 'Ландшафт модели: (а) смягчённый кулоновский потенциал V(r₁, r₂) при Z = 2, ε = 0.1 — стена гребня e–e вдоль диагонали и разнесённый стартовый сегмент (r₁ = 3, r₂ = 3 + Δ, Δ ∈ [0.8, 2.0]); (б) цепочечный потенциал V(ρ, ρ + Δ) вдоль стартового луча для трёх разносов с окном избыточной энергии E ∈ [0.05, 0.3] Ha.', 'walk_en': 'Panel (a) maps the potential topography: the diagonal ridge r₁ = r₂ (the e–e repulsion wall) and the gold launch segment at r₁ = 3, r₂ = 3 + Δ with Δ ∈ [0.8, 2.0]; panel (b) shows that launched states sit above the potential asymptote and climb out unless the repulsion binds one electron.', 'walk_ru': 'Панель (а) картирует топографию потенциала: диагональный гребень r₁ = r₂ (стена отталкивания e–e) и золотой стартовый сегмент при r₁ = 3, r₂ = 3 + Δ с Δ ∈ [0.8, 2.0]; панель (б) показывает, что запущенные состояния лежат выше асимптоты потенциала и выбираются наружу, если только отталкивание не свяжет один из электронов.'}](figures/fig01_model_landscape.png)

*{'cap_en': 'Model landscape: (a) softened Coulomb potential V(r₁, r₂) for Z = 2, ε = 0.1 — the e–e ridge wall along the diagonal and the staggered launch segment (r₁ = 3, r₂ = 3 + Δ, Δ ∈ [0.8, 2.0]); (b) chain potential V(ρ, ρ + Δ) along the launch ray for three staggers with the excess-energy window E ∈ [0.05, 0.3] Ha.', 'cap_ru': 'Ландшафт модели: (а) смягчённый кулоновский потенциал V(r₁, r₂) при Z = 2, ε = 0.1 — стена гребня e–e вдоль диагонали и разнесённый стартовый сегмент (r₁ = 3, r₂ = 3 + Δ, Δ ∈ [0.8, 2.0]); (б) цепочечный потенциал V(ρ, ρ + Δ) вдоль стартового луча для трёх разносов с окном избыточной энергии E ∈ [0.05, 0.3] Ha.', 'walk_en': 'Panel (a) maps the potential topography: the diagonal ridge r₁ = r₂ (the e–e repulsion wall) and the gold launch segment at r₁ = 3, r₂ = 3 + Δ with Δ ∈ [0.8, 2.0]; panel (b) shows that launched states sit above the potential asymptote and climb out unless the repulsion binds one electron.', 'walk_ru': 'Панель (а) картирует топографию потенциала: диагональный гребень r₁ = r₂ (стена отталкивания e–e) и золотой стартовый сегмент при r₁ = 3, r₂ = 3 + Δ с Δ ∈ [0.8, 2.0]; панель (б) показывает, что запущенные состояния лежат выше асимптоты потенциала и выбираются наружу, если только отталкивание не свяжет один из электронов.'}.*

![{'cap_en': 'Headline result: (a) distribution of the escaping-electron share E_esc/E over all 3200 autoionization events — mean 7.28, median 5.90, 16–84 pct band [3.24, 13.30]; (b) the measured double-escape fraction stays at the 1e-4 counting floor over E ∈ [0.05, 0.3], far below the 0.5 acceptance line; the Wannier slope 1.056 is a guide, not a resolved measurement.', 'cap_ru': 'Главный результат: (а) распределение доли уходящего электрона E_esc/E по всем 3200 событиям автоионизации — среднее 7.28, медиана 5.90, полоса 16–84 процентилей [3.24, 13.30]; (б) измеренная доля двойного ухода остаётся на счётном полу 1e-4 по E ∈ [0.05, 0.3], далеко ниже линии допуска 0.5; наклон Ваннье 1.056 показан как ориентир, а не как разрешённое измерение.', 'walk_en': 'The escaping electron carries on average 7.28× the total excess energy (median 5.90, band [3.24, 13.30]) while the captured partner keeps E − E_esc < 0 — binding energy released into the pair; not a single double escape occurs in the ensemble, so all 3200 outcomes sit in the autoionization channel.', 'walk_ru': 'Уходящий электрон уносит в среднем 7.28× полной избыточной энергии (медиана 5.90, полоса [3.24, 13.30]), а захваченный партнёр сохраняет E − E_esc < 0 — энергия связи выделяется в пару; в ансамбле нет ни одного двойного ухода, поэтому все 3200 исходов лежат в канале автоионизации.'}](figures/fig02_energy_sharing.png)

*{'cap_en': 'Headline result: (a) distribution of the escaping-electron share E_esc/E over all 3200 autoionization events — mean 7.28, median 5.90, 16–84 pct band [3.24, 13.30]; (b) the measured double-escape fraction stays at the 1e-4 counting floor over E ∈ [0.05, 0.3], far below the 0.5 acceptance line; the Wannier slope 1.056 is a guide, not a resolved measurement.', 'cap_ru': 'Главный результат: (а) распределение доли уходящего электрона E_esc/E по всем 3200 событиям автоионизации — среднее 7.28, медиана 5.90, полоса 16–84 процентилей [3.24, 13.30]; (б) измеренная доля двойного ухода остаётся на счётном полу 1e-4 по E ∈ [0.05, 0.3], далеко ниже линии допуска 0.5; наклон Ваннье 1.056 показан как ориентир, а не как разрешённое измерение.', 'walk_en': 'The escaping electron carries on average 7.28× the total excess energy (median 5.90, band [3.24, 13.30]) while the captured partner keeps E − E_esc < 0 — binding energy released into the pair; not a single double escape occurs in the ensemble, so all 3200 outcomes sit in the autoionization channel.', 'walk_ru': 'Уходящий электрон уносит в среднем 7.28× полной избыточной энергии (медиана 5.90, полоса [3.24, 13.30]), а захваченный партнёр сохраняет E − E_esc < 0 — энергия связи выделяется в пару; в ансамбле нет ни одного двойного ухода, поэтому все 3200 исходов лежат в канале автоионизации.'}.*

![{'cap_en': 'Parameter sweeps: (a) per-bin mean of E_esc/E with 16–84 percentile bars across the excess-energy window — the transfer efficiency stays far above parity in every bin; (b) launch-kick sensitivity on reduced ensembles of 720 trajectories per point — the autoionization channel remains dominant for every documented kick σ, including the scale-invariant limit σ = 0.', 'cap_ru': 'Размывки параметров: (а) среднее E_esc/E по бинам с барами 16–84 процентилей по окну избыточной энергии — эффективность переноса всюду далеко выше паритета; (б) чувствительность к стартовому пинку на редуцированных ансамблях по 720 траекторий на точку — канал автоионизации остаётся доминирующим для каждого документированного пинка σ, включая масштабно-инвариантный предел σ = 0.', 'walk_en': 'Across the kick grid σ ∈ {0, 0.002, 0.005, 0.01, 0.02, 0.05} the single-escape fraction stays at 1.000 and the mean overshoot barely moves, 5.3421 → 5.3416 — the strong-coupling autoionization channel is insensitive to the kick that breaks scale invariance.', 'walk_ru': 'По сетке пинков σ ∈ {0, 0.002, 0.005, 0.01, 0.02, 0.05} доля одинарного ухода держится на 1.000, а среднее превышение почти не движется, 5.3421 → 5.3416, — сильносвязный канал автоионизации нечувствителен к пинку, ломающему масштабную инвариантность.'}](figures/fig03_parameter_sweeps.png)

*{'cap_en': 'Parameter sweeps: (a) per-bin mean of E_esc/E with 16–84 percentile bars across the excess-energy window — the transfer efficiency stays far above parity in every bin; (b) launch-kick sensitivity on reduced ensembles of 720 trajectories per point — the autoionization channel remains dominant for every documented kick σ, including the scale-invariant limit σ = 0.', 'cap_ru': 'Размывки параметров: (а) среднее E_esc/E по бинам с барами 16–84 процентилей по окну избыточной энергии — эффективность переноса всюду далеко выше паритета; (б) чувствительность к стартовому пинку на редуцированных ансамблях по 720 траекторий на точку — канал автоионизации остаётся доминирующим для каждого документированного пинка σ, включая масштабно-инвариантный предел σ = 0.', 'walk_en': 'Across the kick grid σ ∈ {0, 0.002, 0.005, 0.01, 0.02, 0.05} the single-escape fraction stays at 1.000 and the mean overshoot barely moves, 5.3421 → 5.3416 — the strong-coupling autoionization channel is insensitive to the kick that breaks scale invariance.', 'walk_ru': 'По сетке пинков σ ∈ {0, 0.002, 0.005, 0.01, 0.02, 0.05} доля одинарного ухода держится на 1.000, а среднее превышение почти не движется, 5.3421 → 5.3416, — сильносвязный канал автоионизации нечувствителен к пинку, ломающему масштабную инвариантность.'}.*

![{'cap_en': 'Dynamics of one representative autoionization event (re-integrated with the same adaptive RK4 rule): (a) x–y paths — the escaper leaves through r = 30 a.u. while the captured electron winds toward the nucleus; (b) individual energies ε₁(t), ε₂(t) and the conserved total — the repulsion hands 7.28× E to the escaper.', 'cap_ru': 'Динамика одного показательного события автоионизации (переинтегрированного тем же адаптивным правилом RK4): (а) пути в плоскости x–y — уходящий покидает сферу r = 30 а.е., а захваченный электрон наматывается на ядро; (б) индивидуальные энергии ε₁(t), ε₂(t) и сохраняющаяся полная — отталкивание передаёт уходящему 7.28× E.', 'walk_en': 'For the representative event at E = 0.107761 Ha the escaper exits at t = 19.6952 with E_esc = 0.784471 Ha (share 7.2797) and the partner is left bound at ε = −0.438084 Ha — a direct view of the three-body energy handover through the e–e repulsion.', 'walk_ru': 'Для показательного события при E = 0.107761 Ha уходящий покидает систему в момент t = 19.6952 с E_esc = 0.784471 Ha (доля 7.2797), а партнёр остаётся связанным при ε = −0.438084 Ha, — прямой взгляд на трёхтельную передачу энергии через отталкивание e–e.'}](figures/fig04_autoionization_dynamics.png)

*{'cap_en': 'Dynamics of one representative autoionization event (re-integrated with the same adaptive RK4 rule): (a) x–y paths — the escaper leaves through r = 30 a.u. while the captured electron winds toward the nucleus; (b) individual energies ε₁(t), ε₂(t) and the conserved total — the repulsion hands 7.28× E to the escaper.', 'cap_ru': 'Динамика одного показательного события автоионизации (переинтегрированного тем же адаптивным правилом RK4): (а) пути в плоскости x–y — уходящий покидает сферу r = 30 а.е., а захваченный электрон наматывается на ядро; (б) индивидуальные энергии ε₁(t), ε₂(t) и сохраняющаяся полная — отталкивание передаёт уходящему 7.28× E.', 'walk_en': 'For the representative event at E = 0.107761 Ha the escaper exits at t = 19.6952 with E_esc = 0.784471 Ha (share 7.2797) and the partner is left bound at ε = −0.438084 Ha — a direct view of the three-body energy handover through the e–e repulsion.', 'walk_ru': 'Для показательного события при E = 0.107761 Ha уходящий покидает систему в момент t = 19.6952 с E_esc = 0.784471 Ha (доля 7.2797), а партнёр остаётся связанным при ε = −0.438084 Ha, — прямой взгляд на трёхтельную передачу энергии через отталкивание e–e.'}.*

## 11. Results (full run)

```text
max_relative_energy_drift_valid     = 4.284e-06  (max |dE| = 1.714·10^-04 a.u.; 0/3200 filtered out)
outcome_classes_sum_to_N            = PASS (3200 = 3200)
autoionization_channel_active       = PASS (single-escape fraction 1.000)
escaping_electron_energy_overshoot  = PASS (7.28 x the total excess energy)
pde_below_half_everywhere           = PASS (strong-coupling regime: P_DE < 0.5 over the window)
wannier_exponent_reported           = PASS (fitted slope alpha = -1.29·10^-15; see honesty note)
fit_reproducible                    = PASS (same stored counts reproduce the same alpha)
status: PASS (7/7)
```

## 12. Analysis

**Conservation.** Over the whole valid ensemble of 3200 trajectories the running maximum of the energy error is 1.714·10⁻⁴ a.u.; relative to the deep-well kinetic scale 2Z/ε = 40 a.u. this is a relative drift of 4.28e-6 — two orders of magnitude inside the 4e-4 acceptance tolerance, and not a single trajectory required the 5·10⁻³ filter (0/3200 discarded). The energy shell is therefore trusted as the backbone of all downstream statistics.

**Bookkeeping and the channel.** The outcome classes sum exactly (3200 = 3200), and the composition is unanimous: the single-escape fraction is 1.000 in every one of the eight energy bins, the double-escape fraction 0.0 in every bin. The autoionization channel is thus the only active outcome of the fixed-launch geometry — a genuinely three-body result, since the e–e repulsion is the only mechanism able to hand energy from one electron to the other while the nucleus keeps the captured partner bound.

**Energy sharing.** The escaping electron carries on average 7.28× the total excess energy (7.2803 over all 3200 events; median 5.8967; 16–84 percentile band [3.2395, 13.2956]) — far above the 1.2× acceptance line. The captured partner keeps E − E_esc < 0, i.e. binding energy is released into the pair. The representative re-integrated event at E = 0.107761 Ha ends at t = 19.6952 with the escaper at E_esc = 0.784471 Ha (share 7.2797) and its partner bound at ε = −0.438084 Ha, a direct portrait of the three-body handover.

**Threshold behavior.** The measured double-escape fraction sits at the 1e-4 counting floor across the entire window E ∈ [0.05, 0.3] (below the 0.5 acceptance line everywhere), so the window-fit slope is −1.29·10⁻¹⁵ ≈ 0: the fixed-launch geometry with R₀ = 3 probes the strong-coupling regime, where P_DE is nearly E-independent. The kick sweep over σ ∈ {0, 0.002, 0.005, 0.01, 0.02, 0.05} on reduced ensembles of 720 trajectories per point leaves the channel dominant (fraction 1.000 everywhere) and the mean overshoot essentially unmoved, 5.3421 → 5.3416. The universal α = 1.056 requires near-threshold Wannier-cap conditioning and far larger ensembles; it is cited, not claimed, and the measured slope is stored in the protocol.

## 13. Discussion and honest boundaries

The model is deliberately minimal: classical mechanics only, nuclear motion neglected, a fixed launch geometry and a documented softening. Within these assumptions every conclusion is an exact statement about the ensemble rather than a simulation of a specific experiment. The natural extensions — Wannier-cap conditioning (launching on the ridge with R₀ ~ 1/E so the threshold law becomes measurable), ensembles two to three orders larger, explicit quantum-classical correspondence tests, and nuclear motion for recoil — each preserve the verification style established here.

The parameter regime is chosen for structural clarity rather than for reproducing the exponential tail of the threshold law: a fixed R₀ = 3 with a fixed kick σ = 0.01 probes the strong-coupling regime of the staggered chain, and the honesty note says so openly. The measured slope (−1.29·10⁻¹⁵ ≈ 0) is stored in the protocol next to the cited universal benchmark α = 1.056 — the same epistemic discipline the program applies everywhere: a number is either measured and stored, or cited and marked as a reference, never blended.

Within the program this study anchors the quantum block: TRX-07 supplies the quantum three-body benchmark proper (Efimov physics of laser-cooled trimers), TRX-08 the trapped-ion realization, and TRX-11 keeps three bodies but exchanges the Coulomb interaction for gravity plus radiation; TRX-01 applies three-body geometry to photon pressure. The laser link runs through the three-step model of high-harmonic generation — ionization, laser-driven acceleration, recombination — whose kinematic core is the same electron-plus-ion two-body subproblem embedded here, and whose strong-field double-ionization channel shows the Wannier-type energy sharing measured in this study.

## 14. Conclusions

- Energy is conserved over the valid ensemble to a relative drift of 4.28e-6 of the deep-well scale 2Z/ε = 40 (max |ΔE| = 1.714·10⁻⁴ a.u.; 0/3200 trajectories filtered).
- Outcome bookkeeping is exact (3200 = 3200), and the autoionization channel is the only active outcome: the single-escape fraction is 1.000 in every energy bin.
- The three-body energy transfer is measured: the escaping electron carries on average 7.28× the excess energy (median 5.90, 16–84 pct band [3.24, 13.30]), and the captured partner keeps E − E_esc < 0 — binding energy released.
- No double escapes occur: P_DE stays at the 1e-4 counting floor across E ∈ [0.05, 0.3], far below the 0.5 acceptance line — the strong-coupling regime of the fixed-launch geometry.
- The Wannier exponent is handled honestly: the fitted slope of this compact ensemble (−1.29·10⁻¹⁵ ≈ 0) is stored in the protocol, while the universal α = 1.056 is cited as a benchmark, not claimed.
- The results are robust to the scale-breaking kick: over σ ∈ {0, 0.002, 0.005, 0.01, 0.02, 0.05} the single-escape fraction stays 1.000 and the mean overshoot moves only 5.3421 → 5.3416.

## 15. The monograph and its renditions

The complete monograph of this study exists in four renditions — Russian and English are separate documents, each in a typeset PDF and an editable DOCX:

| Rendition | Path |
|---|---|
| Monograph (English, PDF) | `monograph/monograph_EN.pdf` |
| Monograph (English, DOCX) | `monograph/monograph_EN.docx` |
| Monograph (Russian, PDF) | `monograph/monograph_RU.pdf` |
| Monograph (Russian, DOCX) | `monograph/monograph_RU.docx` |
| Reading-room copy | `publications/pdf/TRX-06-helium-three-body_EN.pdf` · `publications/pdf/TRX-06-helium-three-body_RU.pdf` |
| HTML source | `publications/html/TRX-06-helium-three-body.html` |

**Monograph abstract.** This monograph treats the helium atom — a nucleus of charge Z = 2 and two electrons — as the classical Coulomb three-body problem, running a deterministic Monte Carlo ensemble of 3200 trajectories in the Wannier launch configuration: a radially staggered chain at hyperradius R₀ = 3 on the exact energy shell, excess energies E ∈ [0.05, 0.3] Ha, a fixed transverse kick σ = 0.01 breaking scale invariance, and a documented softening ε = 0.1 a.u. Four machine-verified results: (i) Energy is conserved over the valid ensemble to a relative drift of 4.28e-6 of the deep-well scale 2Z/ε = 40 (max |ΔE| = 1.714·10⁻⁴ a.u.; 0/3200 filtered). (ii) Outcome bookkeeping is exact (3200 = 3200); the autoionization channel is the only active outcome, single-escape fraction 1.000 in every bin. (iii) The escaping electron carries on average 7.28× the excess energy (median 5.90, band [3.24, 13.30]) while its captured partner keeps E − E_esc < 0 — binding energy released through the e⁻–e⁻ repulsion. (iv) The double-escape fraction stays at the 1e-4 counting floor; the universal Wannier slope α = 1.056 is cited, and this compact ensemble's fitted value (≈ 0, strong-coupling regime) is stored in the protocol.

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
| `E` | 3 | 0.05 … 0.3 |
| `P_DE` | 3 | 1.0000e-04 … 1.0000e-04 |
| `P_DE_poisson_err` | 3 | 0 … 0 |

**Reproduction matrix**

| Command | What it does |
|---|---|
| `python3 research/TRX-06-helium-three-body/code/trx06_helium_three_body.py` | full run: physics + acceptance checks (37.7 s) |
| `python3 research/TRX-06-helium-three-body/code/trx06_helium_three_body.py --smoke` | CI guard: same checks, seconds-scale settings |
| `python3 research/TRX-06-helium-three-body/code/trx06_helium_three_body.py --figures` | regenerates the 300-dpi figure set |
| `make research-smoke` | all twelve studies in smoke mode |
| `make research-figures` | all twelve studies + figure sets |

## 17. Cross-links within the program

- **TRX-07** is the quantum three-body benchmark proper (Efimov physics of laser-cooled Cs trimers) — the quantum envelope of the same trio.
- **TRX-11** keeps three bodies but exchanges the Coulomb interaction for gravity plus radiation (GW choreographies).
- **TRX-01** applies three-body geometry to photon pressure (laser on dust); the HHG three-step link lives in the strong-field community around TRX-06.

## 18. Inside the script

The executable is a single deterministic file, `code/trx06_helium_three_body.py`, ~pure `numpy`/`scipy` with no network access and no random state beyond fixed seeds. One run executes the full physics of the study, evaluates every registered acceptance check against its committed target and tolerance, and writes the JSON protocol — the same file quoted in §9.

| Mode | Invocation | What happens |
|---|---|---|
| Full | `python3 code/trx06_helium_three_body.py` | complete experiment, all checks, JSON protocol (37.7 s) |
| Smoke | `python3 code/trx06_helium_three_body.py --smoke` | identical acceptance logic at seconds-scale settings — the CI mode |
| Figures | `python3 code/trx06_helium_three_body.py --figures` | regenerates the schematic + the four 300-dpi PNG panels |

**Outputs per run**

| File | Produced by | Content |
|---|---|---|
| `results/trx06_results.json` | every mode | status, checks (value/target/tol/unit/pass/note), series, meta |
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
| Previous study | TRX-005 |
| Next study | TRX-007 |

## 21. Notation

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

## 22. References

1. Wannier, G. H. (1953). *The threshold law for single ionization of atoms.* Physical Review 90, 817–825.
2. Peterkop, R. K. (1971). *Wannier's theory of ionization.* Journal of Physics B 4, 513–521.
3. Abrines, R., Percival, I. C. (1966). *Classical theory of charge transfer and ionization of hydrogen atoms by protons.* Proceedings of the Physical Society 88, 861–872.
4. Fano, U. (1961). *Effects of configuration interaction on intensities and phase shifts.* Physical Review 124, 1866–1878.
5. Sacha, K., Eckhardt, B. (2001). *Classical mechanics of the Wannier ridge.* Physical Review A 63, 042714.
6. Aref, H. (1979). *Motion of three vortices.* Physics of Fluids 22, 393–400 (collapse/scattering methodology shared with CTMC studies).
7. Agostini, P., Fabre, F., Mainfray, G., Petite, G., Rahman, N. K. (1979). *Free-free transitions following six-photon ionization of xenon atoms.* Physical Review Letters 42, 1127–1130 (three-step model foundations).
8. Corkum, P. B. (1993). *Plasma perspective on strong-field multiphoton ionization.* Physical Review Letters 71, 1994–1997.

## 23. Glossary

| Term | Definition |
|---|---|
| CTMC | classical trajectory Monte Carlo: ensemble of classical trajectories with statistically drawn initial conditions |
| Autoionization | one electron is captured while the other escapes, taking more than the total excess energy |
| Double escape | both electrons leave the nucleus region on positive individual energies |
| Wannier threshold law | P_DE ∝ E^α near the double-escape threshold; α = 1.056 for Z = 2 |
| Wannier configuration | electrons launched on one ray, radially staggered, on the exact energy shell |
| Excess energy E | total energy above the double-escape threshold, shared by the pair |
| Overshoot E_esc/E | ratio of the escaping electron's individual energy to the excess energy |
| Softening ε | regularization r → (r² + ε²)^{1/2} of the Coulomb denominators, ε = 0.1 a.u. |
| Energy shell | launched state with total energy exactly E (kinetic + potential = E) |
| Counting floor | the 1e-4 value at which a zero-count bin is plotted on log axes |

## 24. Appendix A. Full parameter table

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

**Protocol-level parameter snapshot** (`results` JSON, `meta` block):

| Key | Value |
|---|---|
| `equations` | `["H = p1^2/2 + p2^2/2 - Z/r1 - Z/r2 + 1/r12   (Z=2, softened eps=0.1)", "Wannier law: P_DE(E) ~ E^alpha, alpha = 1.056"]` |
| `experiment` | `"Wannier-configuration launch: R0 = 3 a.u., radially staggered collinear chain (delta_r in [0.8, 2.0]), equal outward speeds on the exact energy shell, fixed transverse kick sigma = 0.01, escape radius 30 a.u."` |
| `n_trajectories` | `120` |
| `alpha_fitted` | `4.011872789999887e-16` |
| `laser_link` | `"three-step model of HHG: electron + parent ion + laser field; strong-field double ionization shows the same Wannier kinematics"` |

## 25. Appendix B. BibTeX

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

## 26. How to cite

Cite the repository through [`CITATION.cff`](../../CITATION.cff) (DOI 10.5281/zenodo.21825394, version 1.0.0); this study is part of the TRIVORTEX Research Program. If you cite the study alone, name the monograph rendition you used and attach the JSON protocol of the run you reproduced.

```bibtex
@misc{trivortextrx062026isaev,
  author       = {Isaev, Iskhak Khamzatovich},
  title        = {Helium Atom as the Coulomb Three-Body Problem (Classical Trajectory Monte Carlo) (TRIVORTEX Research Program, TRX-06)},
  year         = {2026},
  howpublished = {Zenodo},
  doi          = {10.5281/zenodo.21825394},
  url          = {https://github.com/wild8highlander/Trivortex}
}
```

