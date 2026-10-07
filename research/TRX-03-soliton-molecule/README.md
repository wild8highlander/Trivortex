# TRX-03 — Three-Soliton Molecule in a Mode-Locked Fiber Laser

*TRIVORTEX Research Program · version 1.0.0 · study TRX-03 of 12*

Three ultrashort pulses circulating in a passively mode-locked fiber laser form a phase-locked "soliton molecule": in the reduced particle picture each pulse is a body with the conservative, phase-dependent pair interaction **V(r, Δφ) = C₁e^(−2r/L) − C₂e^(−r/L)cos 2Δφ**. The phase-locked triplet is a genuine optical three-body choreography: its equilibrium spacing s*is fixed by the three-body balance F(s*) + F(2s*) = 0, is compressed ≈ 30 % below the pair value r₀ = ln(4/3), and supports a breathing normal mode verified by FFT against the Hessian prediction to 0.21 %.

> **Edition 1.0.0.** This README is part of the first public release of the TRIVORTEX research program. The study ships as an executable script, a committed JSON protocol, four 300-dpi figures, a schematic and a bilingual monograph in four renditions (Russian and English, each in PDF and DOCX).

**At a glance**

| Aspect | Value |
|---|---|
| Block | Laser optics — study 03 of 12 |
| Model | three-pulse chain with phase-dependent exponential pair potential (C₁ = 2, C₂ = 3, L = 1) |
| Key invariant | total energy of the conservative molecule (drift 1.8e-15) |
| Headline result | molecule at s* = 0.2018927 — 29.8 % below the pair r₀ = ln(4/3) ≈ 0.287682 |
| Verification | 6/6 checks PASS (full mode) |
| Runtime | 1.2 s full · 4.7 s with figures · < 20 s smoke |

| Field | Value |
|---|---|
| Study | `TRX-03` (TRX-03-soliton-molecule) |
| Program | TRIVORTEX — The Three-Body Problem in the Vortex Model |
| Author | Isaev Iskhak Khamzatovich (ORCID `0009-0003-7299-0701`) |
| DOI | [10.5281/zenodo.21825394](https://doi.org/10.5281/zenodo.21825394) |
| Version | 1.0.0 — first public release |
| Code | `research/TRX-03-soliton-molecule/code/trx03_soliton_molecule.py` |
| Protocol | `research/TRX-03-soliton-molecule/results/trx03_results.json` |
| License | `LicenseRef-Proprietary-Wild8Highlander-1.0` |

## 1. Mission

Soliton molecules are the closest optical cousins of the three-body choreographies at the heart of TRIVORTEX. The monograph's Theorem 3.1 binds three vortices into a rigid rotating triangle; a mode-locked fiber laser binds three light pulses into an equally spaced temporal molecule by exactly the same mechanism — a pair-wise attractive balance in which every member feels all the others. This study makes that analogy quantitative and verifiable: the pulses become "bodies", their evanescent tails become the interaction law, and the cavity provides the environment in which the molecule assembles, relaxes and breathes.

The study verifies four things to machine precision: that the pair binding law reproduces its analytic equilibrium r₀ = L·ln(2C₁/C₂) = ln(4/3) to 5.6e-17; that the anti-phase lock (Δφ = π/2) is purely repulsive over the whole tested range, so binding is a phase-selection effect; that a random triplet under overdamped damping relaxes into an equally spaced molecule whose spacing equals the three-chain equilibrium s* — the root of F(s) + F(2s) = 0, a genuinely three-body quantity compressed below the pair value; and that the conservative molecule conserves energy to 1.8e-15 while its breathing mode frequency matches the analytic Hessian spectrum to 0.21 %. Together these checks turn a qualitative optics story into a controlled three-body experiment in software.

## 2. Introduction and historical context

The word "soliton" was coined by Zabusky and Kruskal in 1965, when numerical experiments on the Korteweg–de Vries equation showed that nonlinear pulses collide and re-emerge with their identity intact. Optical solitons followed: Hasegawa and Tappert predicted in 1973 that the nonlinear Schrödinger equation admits shape-preserving pulses in fibers with anomalous dispersion, and Mollenauer, Stolen and Gordon observed them in 1980. From the very beginning it was clear that two solitons are not merely two particles — their overlapping tails make them interact, and the interaction is the optical analog of a force.

The quantitative theory of soliton interactions was built by Karpman and Solov'ev in 1981 through perturbation theory around the exact two-soliton solution, and by Gordon in 1983 through the discrete spectral picture; both approaches yield an exponential force whose sign is set by the relative phase. Malomed (1991) extended the analysis to multi-soliton bound states and their cyclic dynamics. Experimentally, Stratmann, Pagel and Mitschke (2005) directly observed temporal soliton molecules in a fiber laser, and Herink and colleagues (2017) filmed their internal dynamics in real time by spectral interferometry — including the breathing mode that this study computes analytically and numerically.

A soliton molecule is therefore a genuine bound state of N bodies, not a metaphor: its geometry is fixed by a force balance in which every pulse feels every other pulse, its stability is read off a normal-mode spectrum, and its assembly is a relaxation problem. For N = 3 all of these ingredients are exactly what the three-body problem means in the TRIVORTEX program — three agents, pairwise interactions, a collective equilibrium and a choreography of motion. The fiber laser simply replaces gravity or vortex circulation by an exponential-cosine law that can be switched by phase control.

Within the program this study is the optics-block anchor of the choreography family. It verifies, in a setting where "passing through one another" is physical rather than singular, the same structural sequence used everywhere in TRIVORTEX: analytic pair law, collective equilibrium, linearized spectrum, conservation of the invariant. The phase-locked triplet is the optical sibling of the Lagrange triangle of Theorem 3.1, and the compression of s* below r₀ is the spectral sibling of the collective force balance that fixes the equilateral configuration.

## 3. Physical system and preset

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

**Model assumptions**

- Point-particle reduction: pulses are described by positions and phases only; their shape is assumed rigid (fundamental solitons).
- The pair interaction is conservative and instantaneous; retardation, third-order dispersion and self-frequency shift are neglected.
- Phase locking Δφ = 0 is imposed as the operating point; the sweep treats Δφ as a static parameter, not a dynamical variable.
- Equal pulses: identical amplitude, mass m = 1 and tail length L for all three members.
- Damping is a switchable linear term (γ_d = 1 relaxation, γ_d = 0 conservative); no noise-driven phase diffusion is modeled.
- Solitons pass through one another; molecular geometry is therefore judged by sorted positions.

## 4. Governing equations

(E1) Phase-dependent pair potential of two solitons:

$$V(r,\Delta\varphi) = C_1\,e^{-2r/L} - C_2\,e^{-r/L}\cos(2\Delta\varphi)$$

(E2) Pair force along increasing separation (F < 0 — attraction):

$$F(r,\Delta\varphi) = -\frac{\partial V}{\partial r} = \frac{2C_1}{L}e^{-2r/L} - \frac{C_2}{L}e^{-r/L}\cos(2\Delta\varphi)$$

(E3) Chain dynamics with all-pairs interaction and damping:

$$m\,\ddot{x}_k = -\sum_{l\neq k}\frac{\partial V(|x_k-x_l|)}{\partial x_k} - \gamma_d\,\dot{x}_k, \qquad k=1,2,3$$

(E4) Pair equilibrium r0 and three-chain equilibrium s* (end-pulse balance):

$$r_0 = L\ln\!\frac{2C_1}{C_2\cos 2\Delta\varphi}; \qquad F(s^*) + F(2s^*) = 0$$

(E5) Generalized eigenproblem for the chain normal modes (breathing spectrum):

$$H\,v = \omega^2 M_g\,v, \quad H = \begin{pmatrix} V''(s)+V''(2s) & V''(2s)\\ V''(2s) & V''(s)+V''(2s) \end{pmatrix}, \quad M_g = m\begin{pmatrix} 2/3 & 1/3\\ 1/3 & 2/3 \end{pmatrix}$$

## 5. Scheme

![TRX-03 scheme — soliton molecule: a phase-locked triplet circulating in a mode-locked fiber ring, bound by the phase-dependent exponential pair interaction; the potential well with minimum r₀ = ln(4/3) holds an equally spaced molecule at s*, fixed by the three-body balance F(s*) + F(2s*) = 0.](figures/scheme_trx03.svg)

*TRX-03 scheme — soliton molecule: a phase-locked triplet circulating in a mode-locked fiber ring, bound by the phase-dependent exponential pair interaction; the potential well with minimum r₀ = ln(4/3) holds an equally spaced molecule at s*, fixed by the three-body balance F(s*) + F(2s*) = 0..*

The diagram encodes the following elements:

- **Fiber ring** — mode-locked fiber laser cavity; circulating pulses pass through one another
- **Three gold pulses** — phase-locked at Δφ = 0 — an optical three-body choreography
- **Potential well** — V(r, 0) with minimum at the pair equilibrium r₀ = ln(4/3) ≈ 0.2877
- **Repulsive branch** — anti-phase Δφ = π/2 curve: binding is a phase-selection effect
- **Equally spaced molecule** — spacing s*= 0.2019 from the balance F(s*) + F(2s*) = 0
- **Compression note** — far-pair attraction holds the spacing ≈ 30 % below the pair value

## 6. Mapping to TRIVORTEX

The mapping to the TRIVORTEX core is structural, one-to-one and already visible in the equations. The three phase-locked pulses are the optical realization of the three agents of Theorem 3.1: a symmetric, phase-locked special solution of a three-body system, exactly as the rotating vortex triangle is the equal-circulation special solution of the vortex problem. The molecule spacing s*plays the role of the Lagrange-triangle side a: both are fixed not by a two-body law but by the requirement that every member be in equilibrium under the combined pull of the other two — F(s*) + F(2s*) = 0 here, the central-configuration equations there. The breathing mode ω₂ is the analog of the radial modulation of the choreography, and the phase difference Δφ controls binding exactly as the circulation ratio controls the vortex triangle: changing it moves the system through symmetric and asymmetric configurations until binding is lost (Δφ = π/4, the analog of leaving the stability island). The same exponential-cosine structure reappears in TRX-09 vortices and TRX-04 photon-fluid beams, which makes this study the reusable optical template of the program.

| Quantity in this study | TRIVORTEX analog | Comment |
|---|---|---|
| Three phase-locked pulses | three bodies of Theorem 3.1 | both are choreographic triads |
| Phase locking Δφ = 0 | equal circulations Γ | symmetric special solution |
| Molecule spacing s* | Lagrange-triangle side a | fixed by collective force balance |
| Balance F(s*) + F(2s*) = 0 | every vortex feels the other two | the three-body compression mechanism |
| Breathing mode ω₂ | radial modulation of the choreography | small oscillations about the central configuration |

## 7. Dimensionless formulation

All quantities are dimensionless in cavity units: lengths in units of the evanescent-tail length L, energies in units of C₁, time in units of (m L²/C₁)^(1/2); the pulse mass m = 1. Damping γ_d = 1.0 in the relaxation runs (overdamped regime of a mode-locked laser) and γ_d = 0 in the conservative runs.

## 8. Numerical method

Equilibria are computed by bracketed root finding. The pair equilibrium solves F(r) = 0 and the chain equilibrium solves F(s) + F(2s) = 0, both by Brent's method with xtol = 1e-15 and machine-level rtol on sign-stable brackets; the numeric pair root agrees with the closed form ln(4/3) to 5.6e-17. The repulsive character of the anti-phase lock is established exhaustively rather than by sampling: the minimum of F(r, π/2) over the range r ∈ [0.05, 20] on a 4000-point grid is +6e-9 > 0, i.e. the force never turns attractive.

Dynamics are integrated with the explicit Dormand–Prince 8(5,3) scheme (DOP853). The relaxation run starts from positions {1.0, 2.0, 3.5} with zero velocities under damping γ_d = 1.0 (overdamped, the Doppler-cooled regime of a mode-locked laser) and runs to T = 90 with rtol = 1e-11, atol = 1e-12 and max_step = 0.2. The conservative run holds γ_d = 0, displaces the middle pulse by +0.01 from the perfect molecule and integrates to T = 100 with rtol = atol = 1e-12 and max_step = 0.05, sampling 2000 points; the energy drift over the whole run is 1.776357e-15 against the 1e-10 acceptance tolerance.

The breathing frequency is extracted twice, independently. Numerically, the middle-pulse displacement relative to the center of mass is Hann-windowed and Fourier-transformed; the spectral peak lies at f = 0.469765. Analytically, the generalized eigenproblem (E5) at s* gives cyclic modes 0.390507 and 0.468766; the measured peak matches the nearest analytic mode to 0.21 %, comfortably inside the 1 % acceptance tolerance. Every check stores its value, target, tolerance, unit and pass flag in the JSON protocol, so the study reproduces from a single command with no network access and no stochastic seeds.

## 9. Verification protocol and acceptance checks

Every check is registered before the run: target, tolerance and unit are committed in the protocol, not chosen after the fact.

| Check | Target | Tolerance |
|---|---|---|
| Pair equilibrium: brentq root vs r₀ = ln(4/3) | 0 | 1e-10 |
| Δφ = π/2 purely repulsive (min force over r ∈ [0.05, 20]) | > 0 | exact |
| Final spacings equal (sorted positions after relaxation) | 0 | 1e-8 |
| Final spacing equals s* (root of F(s) + F(2s) = 0) | 0 | 1e-6 |
| Conservative energy drift over t = 100 | 0 | 1e-10 |
| Breathing frequency: FFT peak vs Hessian eigenfrequency | equal | 1% |

**Recorded verification run** (mode: smoke, status: **PASS**, 6/6 checks)

| Check | Recorded value | Target | Tolerance | Unit | Verdict |
|---|---|---|---|---|---|
| `pair_equilibrium_numeric_vs_analytic` | 5.5511e-17 | 0 | 1.0000e-10 | length | PASS |
| `antiphase_pi2_purely_repulsive` | 1 | 1 | 1.0000e-12 | bool | PASS |
| `molecule_final_spacings_equal` | 2.2204e-16 | 0 | 1.0000e-08 | length | PASS |
| `molecule_final_spacing_equals_s_star` | 2.7756e-17 | 0 | 1.0000e-06 | length | PASS |
| `conservative_energy_drift` | 1.3323e-15 | 0 | 1.0000e-10 | energy | PASS |
| `breathing_mode_frequency` | 0.468825 | 0.4687663104 | 0.004687663104 | 1/time | PASS |

**Check notes** — what each number means:

| Check | Note |
|---|---|
| `pair_equilibrium_numeric_vs_analytic` | r0 = L*ln(2C1/C2) = 0.287682072452 |
| `antiphase_pi2_purely_repulsive` | min pair force over r in [0.05,20] = 6.183461e-09 (must be > 0) |
| `molecule_final_spacings_equal` | d1=0.2018926516, d2=0.2018926516 |
| `molecule_final_spacing_equals_s_star` | 3-chain equilibrium s* (F(s)+F(2s)=0) = 0.2018926516; pair r0 = 0.287682 |
| `conservative_energy_drift` | damping-free molecule, t=100 |
| `breathing_mode_frequency` | FFT peak vs nearest chain mode from Hessian: [0.390507 0.468766] |

## 10. Figure gallery (300 dpi)

![{'cap_en': 'Interaction landscape: phase-dependent pair potential and the three-chain force balance.', 'cap_ru': 'Ландшафт взаимодействия: фазозависимый парный потенциал и силовой баланс трёхзвенной цепочки.', 'walk_en': 'Panel (a) shows V(r, Δφ) for four lockings: the binding well exists only for |Δφ| < π/4, has its minimum at r₀ = 0.287682, and degenerates into pure repulsion for the anti-phase case. Panel (b) shows the end-pulse balance F(s) + F(2s) = 0: the root s* = 0.201893 lies 29.8 % below the pair value r₀ — a genuine three-body compression.', 'walk_ru': 'Панель (а) показывает V(r, Δφ) для четырёх синхронизаций: связывающая яма существует лишь при |Δφ| < π/4, имеет минимум в r₀ = 0.287682 и вырождается в чистое отталкивание в противофазном случае. Панель (б) показывает баланс концевого импульса F(s) + F(2s) = 0: корень s* = 0.201893 лежит на 29.8 % ниже парного значения r₀ — подлинное трёхтельное сжатие.'}](figures/fig01_potential_landscape.png)

*{'cap_en': 'Interaction landscape: phase-dependent pair potential and the three-chain force balance.', 'cap_ru': 'Ландшафт взаимодействия: фазозависимый парный потенциал и силовой баланс трёхзвенной цепочки.', 'walk_en': 'Panel (a) shows V(r, Δφ) for four lockings: the binding well exists only for |Δφ| < π/4, has its minimum at r₀ = 0.287682, and degenerates into pure repulsion for the anti-phase case. Panel (b) shows the end-pulse balance F(s) + F(2s) = 0: the root s* = 0.201893 lies 29.8 % below the pair value r₀ — a genuine three-body compression.', 'walk_ru': 'Панель (а) показывает V(r, Δφ) для четырёх синхронизаций: связывающая яма существует лишь при |Δφ| < π/4, имеет минимум в r₀ = 0.287682 и вырождается в чистое отталкивание в противофазном случае. Панель (б) показывает баланс концевого импульса F(s) + F(2s) = 0: корень s*= 0.201893 лежит на 29.8 % ниже парного значения r₀ — подлинное трёхтельное сжатие.'}.*

![{'cap_en': 'Headline result: relaxation of a random triplet into the equally spaced soliton molecule.', 'cap_ru': 'Главный результат: релаксация случайного триплета в равноотстоящую солитонную молекулу.', 'walk_en': 'Starting from positions {1.0, 2.0, 3.5} under overdamped damping, the three worldlines settle within T = 90 into an equally spaced triplet; the sorted spacings d₁(t) and d₂(t) converge to the chain equilibrium s* = 0.201893 (final mismatch 2.2e-16, offset from s* 2.8e-17), visibly below the pair value r₀ = 0.2877 marked for comparison.', 'walk_ru': 'Стартуя с позиций {1.0, 2.0, 3.5} при сверхвязком демпфировании, три мировые линии за T = 90 приходят к равноотстоящему триплету; сортированные расстояния d₁(t) и d₂(t) сходятся к равновесию цепочки s* = 0.201893 (конечное расхождение 2.2e-16, отклонение от s* 2.8e-17), заметно ниже парного значения r₀ = 0.2877, нанесённого для сравнения.'}](figures/fig02_molecule_formation.png)

*{'cap_en': 'Headline result: relaxation of a random triplet into the equally spaced soliton molecule.', 'cap_ru': 'Главный результат: релаксация случайного триплета в равноотстоящую солитонную молекулу.', 'walk_en': 'Starting from positions {1.0, 2.0, 3.5} under overdamped damping, the three worldlines settle within T = 90 into an equally spaced triplet; the sorted spacings d₁(t) and d₂(t) converge to the chain equilibrium s* = 0.201893 (final mismatch 2.2e-16, offset from s*2.8e-17), visibly below the pair value r₀ = 0.2877 marked for comparison.', 'walk_ru': 'Стартуя с позиций {1.0, 2.0, 3.5} при сверхвязком демпфировании, три мировые линии за T = 90 приходят к равноотстоящему триплету; сортированные расстояния d₁(t) и d₂(t) сходятся к равновесию цепочки s* = 0.201893 (конечное расхождение 2.2e-16, отклонение от s*2.8e-17), заметно ниже парного значения r₀ = 0.2877, нанесённого для сравнения.'}.*

![{'cap_en': 'Parameter sweep over the locking phase: equilibrium geometry and mode softening.', 'cap_ru': 'Развёртка по фазе синхронизации: равновесная геометрия и размягчение мод.', 'walk_en': 'Both equilibria diverge as the binding threshold Δφ = π/4 is approached: s* grows from 0.201893 at Δφ = 0 through 0.719380 at Δφ = 0.5 rad to 2.885 at Δφ = 0.75 rad, tracking the pair value. The chain modes soften in response — from 2.4536 and 2.9453 rad at the preset down to 0.1092 and 0.1982 rad — producing a complete stability map of the phase-locked molecule.', 'walk_ru': 'Оба равновесия расходятся при приближении к порогу связывания Δφ = π/4: s* растёт от 0.201893 при Δφ = 0 через 0.719380 при Δφ = 0.5 рад до 2.885 при Δφ = 0.75 рад, следя за парным значением. Цепочечные моды в ответ размягчаются — от 2.4536 и 2.9453 рад в пресете до 0.1092 и 0.1982 рад — давая полную карту устойчивости синхронизованной молекулы.'}](figures/fig03_phase_sweep.png)

*{'cap_en': 'Parameter sweep over the locking phase: equilibrium geometry and mode softening.', 'cap_ru': 'Развёртка по фазе синхронизации: равновесная геометрия и размягчение мод.', 'walk_en': 'Both equilibria diverge as the binding threshold Δφ = π/4 is approached: s* grows from 0.201893 at Δφ = 0 through 0.719380 at Δφ = 0.5 rad to 2.885 at Δφ = 0.75 rad, tracking the pair value. The chain modes soften in response — from 2.4536 and 2.9453 rad at the preset down to 0.1092 and 0.1982 rad — producing a complete stability map of the phase-locked molecule.', 'walk_ru': 'Оба равновесия расходятся при приближении к порогу связывания Δφ = π/4: s*растёт от 0.201893 при Δφ = 0 через 0.719380 при Δφ = 0.5 рад до 2.885 при Δφ = 0.75 рад, следя за парным значением. Цепочечные моды в ответ размягчаются — от 2.4536 и 2.9453 рад в пресете до 0.1092 и 0.1982 рад — давая полную карту устойчивости синхронизованной молекулы.'}.*

![{'cap_en': 'Dynamics of the conservative molecule: breathing time series and spectrum against the Hessian prediction.', 'cap_ru': 'Динамика консервативной молекулы: временной ряд дыхания и спектр против гессиановского предсказания.', 'walk_en': 'With the middle pulse displaced by 0.01 and damping removed, the molecule breathes over T = 100 while the total energy drifts by only 1.8e-15 (DOP853, rtol = atol = 1e-12). The FFT spectrum of the middle-pulse displacement peaks at f = 0.469765 against the analytic Hessian modes 0.468766 and 0.390507 — agreement to 0.21 %, an order of magnitude inside the 1 % tolerance.', 'walk_ru': 'При смещении среднего импульса на 0.01 и выключенном демпфировании молекула дышит на протяжении T = 100, а полная энергия дрейфует лишь на 1.8e-15 (DOP853, rtol = atol = 1e-12). Спектр Фурье смещения среднего импульса имеет пик на f = 0.469765 против аналитических гессиановских мод 0.468766 и 0.390507 — согласие 0.21 %, на порядок внутри допуска 1 %.'}](figures/fig04_breathing_dynamics.png)

*{'cap_en': 'Dynamics of the conservative molecule: breathing time series and spectrum against the Hessian prediction.', 'cap_ru': 'Динамика консервативной молекулы: временной ряд дыхания и спектр против гессиановского предсказания.', 'walk_en': 'With the middle pulse displaced by 0.01 and damping removed, the molecule breathes over T = 100 while the total energy drifts by only 1.8e-15 (DOP853, rtol = atol = 1e-12). The FFT spectrum of the middle-pulse displacement peaks at f = 0.469765 against the analytic Hessian modes 0.468766 and 0.390507 — agreement to 0.21 %, an order of magnitude inside the 1 % tolerance.', 'walk_ru': 'При смещении среднего импульса на 0.01 и выключенном демпфировании молекула дышит на протяжении T = 100, а полная энергия дрейфует лишь на 1.8e-15 (DOP853, rtol = atol = 1e-12). Спектр Фурье смещения среднего импульса имеет пик на f = 0.469765 против аналитических гессиановских мод 0.468766 и 0.390507 — согласие 0.21 %, на порядок внутри допуска 1 %.'}.*

## 11. Results (full run)

```text
pair_equilibrium_numeric_vs_analytic   = 5.551115e-17  (r0 = L*ln(2C1/C2) = ln(4/3))
antiphase_pi2_purely_repulsive         = PASS (min pair force +6e-9 > 0 over r in [0.05, 20])
molecule_final_spacings_equal          = 2.220446e-16  (d1 = d2 = 0.2018926516)
molecule_final_spacing_equals_s_star   = 2.775558e-17  (s* = 0.2018926516; pair r0 = 0.287682)
conservative_energy_drift              = 1.776357e-15  (damping-free molecule, t = 100)
breathing_mode_frequency               = 0.469765 vs 0.468766 (Hessian), error 0.21%
status: PASS (6/6)
```

## 12. Analysis

**Equilibria.** The numeric pair root reproduces the closed form r₀ = L·ln(2C₁/C₂) = ln(4/3) ≈ 0.287682 to 5.6e-17 — machine zero. The exhaustive anti-phase test returns min F(r, π/2) = +6e-9 > 0 over r ∈ [0.05, 20], confirming that binding is controlled by the phase factor cos 2Δφ and disappears entirely at and beyond Δφ = π/4. The curvature of the well at the pair minimum is V″(r₀) = 2.25, which fixes the pair breathing scale √(3V″(r₀)) ≈ 2.5981 against which the chain spectrum is compared.

**Molecule formation.** Under overdamped relaxation from {1.0, 2.0, 3.5}, the sorted spacings converge to d₁ = d₂ = 0.2018926516; their final mismatch is 2.2e-16 and their offset from the independently computed chain equilibrium s* = 0.2018926516 is 2.8e-17 — both machine-level, against tolerances of 1e-8 and 1e-6. The spacing sits 29.8 % below the pair value r₀ = 0.287682: the far pair F(2s) pulls the molecule together, a clean, quantified three-body effect visible in fig02.

**Stability map.** Sweeping the locking phase Δφ from 0 to 0.75 rad shows both equilibria diverging as the binding threshold π/4 ≈ 0.7854 is approached: s* grows from 0.201893 through 0.719380 (Δφ = 0.5 rad) to 2.885 (Δφ = 0.75 rad). The chain modes soften in the same direction, from 2.4536 and 2.9453 rad at the preset to 0.1092 and 0.1982 rad at the far end of the sweep — the soft-mode behavior expected as the well flattens into pure repulsion (fig03).

**Breathing and invariants.** The conservative molecule breathes stably over T = 100 (fig04a) with total energy conserved to 1.776357e-15 — five orders of magnitude inside the 1e-10 tolerance. The FFT spectrum of the middle-pulse displacement peaks at f = 0.469765 against the analytic Hessian modes 0.468766 and 0.390507 (fig04b): agreement 0.21 %, an order of magnitude inside the 1 % acceptance tolerance. The dynamics, the spectrum and the Hessian thus triangulate the same breathing physics from three independent directions.

## 13. Discussion and honest boundaries

The reduced model is deliberately minimal: point-like pulses, a pair potential without retardation or gain dynamics, and damping treated as a switchable term. Within these assumptions every conclusion is an exact statement about the governing equations rather than a simulation of a specific laser. The natural extensions — third-order dispersion and self-frequency shift (which make the force asymmetric and non-conservative), continuous cw backgrounds, larger molecules N > 3 with defect modes, and full NLSE integration of the same scenario — each preserve the verification style established here.

The parameter regime covers the generic regime of the Gordon–Mollenauer law rather than a specific cavity: C₁/C₂ = 2/3 places the pair well at r₀ ≈ 0.29 tail lengths with depth 0.25, comfortably resolved on the integration grid. The phase sweep deliberately approaches the binding threshold Δφ = π/4, where the equilibrium diverges and the Hessian develops a zero mode; exactly at threshold the brentq brackets fail, which the sweep code reports as a hard boundary rather than hiding with a regularized formula. Realistic cavities would add noise-driven phase diffusion, slowly destroying the lock — a physics question outside the conservative scope of this study.

Within the program, this study feeds TRX-04, which lifts the pair interaction into the transverse plane and recovers a rotating Lagrange triangle of beams in the Kerr photon fluid; TRX-08, which exchanges optical pulses for laser-cooled ions and reproduces the same spacing/breathing structure with a Coulomb tail; and TRX-09, the fluid-dynamical anchor where phases become circulations. Together with the celestial block (TRX-01, TRX-11) they demonstrate that the choreography sequence — pair law, collective equilibrium, normal spectrum, invariant — is portable across optics, fluids and celestial mechanics.

## 14. Conclusions

- The pair binding law is exact: the numeric equilibrium reproduces r₀ = L·ln(2C₁/C₂) = ln(4/3) ≈ 0.287682 to 5.6e-17.
- Binding is a phase-selection effect: the anti-phase lock Δφ = π/2 is purely repulsive over r ∈ [0.05, 20] (min force +6e-9 > 0), and the well exists only for |Δφ| < π/4.
- A random triplet relaxes into an equally spaced molecule: d₁ = d₂ = 0.2018926516 with mismatch 2.2e-16 and offset from the analytic chain equilibrium s* only 2.8e-17.
- The molecule is compressed 29.8 % below the pair spacing by the far-pair attraction (F(s*) + F(2s*) = 0) — a quantified genuine three-body effect.
- The conservative molecule is a clean invariant system: energy drift 1.8e-15 over t = 100 at DOP853 rtol = atol = 1e-12.
- The breathing spectrum is verified: FFT peak f = 0.469765 against the Hessian mode 0.468766 (agreement 0.21 %, tolerance 1 %), and the phase sweep yields the full stability map with both modes softening to zero at Δφ = π/4.

## 15. The monograph and its renditions

The complete monograph of this study exists in four renditions — Russian and English are separate documents, each in a typeset PDF and an editable DOCX:

| Rendition | Path |
|---|---|
| Monograph (English, PDF) | `monograph/monograph_EN.pdf` |
| Monograph (English, DOCX) | `monograph/monograph_EN.docx` |
| Monograph (Russian, PDF) | `monograph/monograph_RU.pdf` |
| Monograph (Russian, DOCX) | `monograph/monograph_RU.docx` |
| Reading-room copy | `publications/pdf/TRX-03-soliton-molecule_EN.pdf` · `publications/pdf/TRX-03-soliton-molecule_RU.pdf` |
| HTML source | `publications/html/TRX-03-soliton-molecule.html` |

**Monograph abstract.** This monograph treats a phase-locked triplet of ultrashort pulses in a passively mode-locked fiber laser as an optical three-body system. Each pulse is a body with the conservative pair interaction V(r, Δφ) = C₁e^(−2r/L) − C₂e^(−r/L)cos 2Δφ, whose in-phase well has the analytic minimum r₀ = L·ln(2C₁/C₂) = ln(4/3) ≈ 0.287682, reproduced numerically to 5.6e-17, while the anti-phase lock Δφ = π/2 is proved purely repulsive. Relaxation of a random triplet {1.0, 2.0, 3.5} under overdamped damping converges to an equally spaced molecule whose spacing equals the three-chain equilibrium s* = 0.2018927, the root of F(s) + F(2s) = 0 — compressed 29.8 % below the pair value by the far-pair attraction, a genuine three-body effect. The conservative molecule conserves energy to 1.8e-15 over t = 100 and breathes at f = 0.469765 against the analytic Hessian mode 0.468766 (agreement 0.21 %); a sweep of the locking phase yields the full stability map, with both equilibria diverging and both modes softening to zero at the binding threshold Δφ = π/4. The soliton molecule thus stands verified as the optical twin of the TRIVORTEX three-body choreographies.

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
| `t` | 20 | 0 … 95.2381 |
| `x1` | 20 | -0.20189265 … -0.19641232 |
| `x2` | 20 | 0.01 … -0.00100968 |
| `x3` | 20 | 0.20189265 … 0.207422 |

**Reproduction matrix**

| Command | What it does |
|---|---|
| `python3 research/TRX-03-soliton-molecule/code/trx03_soliton_molecule.py` | full run: physics + acceptance checks (1.2 s (4.7 s with --figures)) |
| `python3 research/TRX-03-soliton-molecule/code/trx03_soliton_molecule.py --smoke` | CI guard: same checks, seconds-scale settings |
| `python3 research/TRX-03-soliton-molecule/code/trx03_soliton_molecule.py --figures` | regenerates the 300-dpi figure set |
| `make research-smoke` | all twelve studies in smoke mode |
| `make research-figures` | all twelve studies + figure sets |

## 17. Cross-links within the program

- **TRX-04** lifts the pair interaction into the transverse plane (Kerr photon fluid) and recovers a rotating Lagrange beam triangle.
- **TRX-08** exchanges optical pulses for laser-cooled ions — the same spacing/breathing structure with a Coulomb tail.
- **TRX-09** is the fluid-dynamical anchor with circulations instead of phases (Kirchhoff–Chaplygin vortex pair/triplet).

## 18. Inside the script

The executable is a single deterministic file, `code/trx03_soliton_molecule.py`, ~pure `numpy`/`scipy` with no network access and no random state beyond fixed seeds. One run executes the full physics of the study, evaluates every registered acceptance check against its committed target and tolerance, and writes the JSON protocol — the same file quoted in §9.

| Mode | Invocation | What happens |
|---|---|---|
| Full | `python3 code/trx03_soliton_molecule.py` | complete experiment, all checks, JSON protocol (1.2 s (4.7 s with --figures)) |
| Smoke | `python3 code/trx03_soliton_molecule.py --smoke` | identical acceptance logic at seconds-scale settings — the CI mode |
| Figures | `python3 code/trx03_soliton_molecule.py --figures` | regenerates the schematic + the four 300-dpi PNG panels |

**Outputs per run**

| File | Produced by | Content |
|---|---|---|
| `results/trx03_results.json` | every mode | status, checks (value/target/tol/unit/pass/note), series, meta |
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
| Previous study | TRX-002 |
| Next study | TRX-004 |

## 21. Notation

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

## 22. References

1. Zabusky, N. J., Kruskal, M. D. (1965). *Interaction of "solitons" in a collisionless plasma and the recurrence of initial states.* Phys. Rev. Lett. 15, 240–243.
2. Hasegawa, A., Tappert, F. (1973). *Transmission of stationary nonlinear optical pulses in dispersive dielectric fibers. I. Anomalous dispersion.* Appl. Phys. Lett. 23, 142–144.
3. Mollenauer, L. F., Stolen, R. H., Gordon, J. P. (1980). *Experimental observation of picosecond pulse narrowing and solitons in optical fibers.* Phys. Rev. Lett. 45, 1095–1098.
4. Karpman, V. I., Solov'ev, V. V. (1981). *A perturbational approach to the two-soliton systems with third-order dispersion.* Physica D 3, 487–502.
5. Gordon, J. P. (1983). *Interaction forces among solitons in optical fibers.* Optics Letters 8, 596–598.
6. Malomed, B. A. (1991). *Multistability and cyclic dynamics of solitons in dispersive media.* Phys. Rev. A 44, 6954.
7. Stratmann, M., Pagel, T., Mitschke, F. (2005). *Experimental observation of temporal soliton molecules.* Phys. Rev. Lett. 95, 143902.
8. Herink, G., Kurtz, F., Jalali, B., Solli, D. R., Ropers, C. (2017). *Real-time spectral interferometry probes the internal dynamics of femtosecond soliton molecules.* Science 356, 50–54.

## 23. Glossary

| Term | Definition |
|---|---|
| Soliton molecule | a bound state of several solitons held by tail-overlap forces, with fixed internal spacing |
| Phase locking Δφ | constant phase difference between pulses; Δφ = 0 binds, π/2 repels |
| Evanescent tail L | exponential decay length of the soliton overlap; the length unit of the study |
| Pair potential V(r, Δφ) | Gordon–Mollenauer law: repulsive core C₁e^(−2r/L) plus phase-gated attraction |
| Pair equilibrium r₀ | root of F(r) = 0; r₀ = L·ln(2C₁/C₂) = ln(4/3) at Δφ = 0 |
| Chain equilibrium s* | symmetric three-pulse spacing: root of F(s) + F(2s) = 0 |
| Three-body compression | s* < r₀ because the far pair attracts; here 29.8 % |
| Breathing mode | normal oscillation in which the middle pulse moves against the outer pair |
| Generalized eigenproblem | H v = ω² M_g v with the non-diagonal spacing-coordinate mass matrix |
| Overdamped relaxation | assembly under strong damping γ_d = 1, the Doppler-cooled analog for lasers |

## 24. Appendix A. Full parameter table

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

**Protocol-level parameter snapshot** (`results` JSON, `meta` block):

| Key | Value |
|---|---|
| `equations` | `["V(r, dphi) = C1 exp(-2r/L) - C2 exp(-r/L) cos(2 dphi)", "m x_k'' = -sum_l dV/dx_k - gamma_d x_k'", "r0 = L ln(2C1/(C2 cos 2dphi)) ; omega_b = sqrt(3 V''(r0))"]` |
| `parameters` | `{"C1": 2.0, "C2": 3.0, "L": 1.0, "m": 1.0, "dphi_locked": 0.0, "gamma_relax": 0.5}` |
| `Vpp_r0` | `2.250000000000001` |
| `chain_equilibrium_s_star` | `0.20189265157156813` |
| `chain_mode_frequencies` | `[2.4536290211302063, 2.9453455942921276]` |
| `note` | `"phase-locked triplet = optical three-body choreography; the same exponential-cosine structure appears in TRX-09 vortices and TRX-04 beams"` |

## 25. Appendix B. BibTeX

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

## 26. How to cite

Cite the repository through [`CITATION.cff`](../../CITATION.cff) (DOI 10.5281/zenodo.21825394, version 1.0.0); this study is part of the TRIVORTEX Research Program. If you cite the study alone, name the monograph rendition you used and attach the JSON protocol of the run you reproduced.

```bibtex
@misc{trivortextrx032026isaev,
  author       = {Isaev, Iskhak Khamzatovich},
  title        = {Three-Soliton Molecule in a Mode-Locked Fiber Laser (TRIVORTEX Research Program, TRX-03)},
  year         = {2026},
  howpublished = {Zenodo},
  doi          = {10.5281/zenodo.21825394},
  url          = {https://github.com/wild8highlander/Trivortex}
}
```

