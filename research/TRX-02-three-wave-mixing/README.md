# TRX-02 — Resonant Three-Wave Interaction (Manley–Rowe, χ⁽²⁾ Optics)

*TRIVORTEX Research Program · version 1.0.0 · study TRX-02 of 12*

Resonant three-wave mixing in a lossless, phase-matched χ⁽²⁾ crystal — the canonical "three-body problem of nonlinear optics". A pump wave at ω₃ = ω₁ + ω₂ exchanges photons with a signal–idler pair; the Manley–Rowe relations keep the photon bookkeeping exact, and the equal-coupling amplitude equations are canonically equivalent to the Euler top — the same integrable family as the Kirchhoff three-vortex problem that underlies Theorem 3.1 of TRIVORTEX.

> **Edition 1.0.0.** This README is part of the first public release of the TRIVORTEX research program. The study ships as an executable script, a committed JSON protocol, four 300-dpi figures, a schematic and a bilingual monograph in four renditions (Russian and English, each in PDF and DOCX).

**At a glance**

| Aspect | Value |
|---|---|
| Block | Nonlinear optics — study 02 of 12 |
| Model | resonant three-wave mixing in a χ⁽²⁾ crystal (equal couplings, Δk = 0) |
| Key invariant | Manley–Rowe invariants I₁, I₂, I₃ |
| Headline result | invariant drift ≤ 5.4e-15 over T = 50; SHG closed-form error 2.2e-16 |
| Verification | 7/7 checks PASS (full mode) |
| Runtime | 0.6 s full · < 20 s smoke |

| Field | Value |
|---|---|
| Study | `TRX-02` (TRX-02-three-wave-mixing) |
| Program | TRIVORTEX — The Three-Body Problem in the Vortex Model |
| Author | Isaev Iskhak Khamzatovich (ORCID `0009-0003-7299-0701`) |
| DOI | [10.5281/zenodo.21825394](https://doi.org/10.5281/zenodo.21825394) |
| Version | 1.0.0 — first public release |
| Code | `research/TRX-02-three-wave-mixing/code/trx02_three_wave_mixing.py` |
| Protocol | `research/TRX-02-three-wave-mixing/results/trx02_results.json` |
| License | `LicenseRef-Proprietary-Wild8Highlander-1.0` |

## 1. Mission

Optical parametric processes are, photon-for-photon, a three-body problem: one pump photon is converted into a signal photon and an idler photon, and the three complex amplitudes obey first-order equations whose exact invariants are the optical Manley–Rowe relations. TRIVORTEX is built on an integrable triad — three vortices with quadratic conservation laws — so the resonant three-wave system is its optical twin: the same structure of quadratic invariants, the same periodic choreography, the same Euler-top backbone. This study establishes that correspondence quantitatively, on the shared ground of machine-precision verification rather than analogy alone.

The study verifies four things to machine precision: that the Manley–Rowe invariants hold to ≤ 5.3e-15 over fifty time units of full pump depletion and revival; that the exchange is exactly periodic with a repeatable period T_ex = 5.650961242 (consecutive periods agreeing to 8.7e-8); that the pump collapses to 6.3e-5 of its flux — genuine full depletion, 99.994% of the peak removed — and revives with error 2.4e-15; and that the degenerate channel reproduces the textbook closed form η(t) = tanh²(At) to 2.2e-16 — a closed-form anchor in the same spirit as the closed form of Theorem 3.1.

## 2. Introduction and historical context

The story begins with the laser itself: in 1961 Franken, Hill, Peters and Weinreich observed second-harmonic generation — light emerging from a quartz crystal at exactly twice the ruby laser frequency — and founded nonlinear optics. Within a year, Armstrong, Bloembergen, Ducuing and Pershan (1962) wrote down the coupled-wave equations that remain the working language of the field, and Kroll (1962) proposed parametric amplification in extended media. The first optical parametric oscillator of Giordmaine and Miller (1965) in LiNbO₃ turned the three-wave interaction into a practical, tunable light source, a role parametric devices still play today.

The conservation laws of the field are older than the optical realization. Manley and Rowe (1956) derived their general energy relations for nonlinear elements in the microwave era, and they transfer verbatim to optics: combinations of the photon fluxes in the interacting waves stay constant. In the resonant three-wave system these Manley–Rowe relations are not merely bookkeeping — they are the exact invariants that make the dynamics integrable, the direct analogue of the circulation integrals of ideal-fluid vortex motion.

The integrability itself became a classical subject. Kaup, Reiman and Bers (1979) systematized the space-time evolution of nonlinear three-wave interactions in their Reviews of Modern Physics survey, exhibiting the soliton solutions and the reduction of the system to integrable canonical forms; the equal-coupling case is canonically equivalent to the Euler top, the torque-free rigid body. Modern relevance is easy to list: optical parametric oscillators and amplifiers, squeezed-light sources for gravitational-wave detectors, terahertz generation and frequency-comb technology all run on precisely this three-wave engine.

For TRIVORTEX the relevance is structural. The program's core is an integrable triad — three Kirchhoff vortices with quadratic conservation laws and a periodic choreography (Theorem 3.1, with its closed form). The resonant three-wave system is that triad's optical twin: quadratic invariants (Manley–Rowe), a periodic choreography (pump depletion and revival with period T_ex), and a closed-form anchor (the tanh² law of second-harmonic generation). Verifying this twin to machine precision is the natural second step of the program, immediately after the celestial twin of TRX-01.

## 3. Physical system and preset

The physical system is a χ⁽²⁾ nonlinear crystal (e.g. MgO:LiNbO₃) supporting three collinear plane waves: the pump at ω₃, the signal at ω₁ and the idler at ω₂, with the resonance conditions ω₃ = ω₁ + ω₂ (energy matching) and k₃ = k₁ + k₂, i.e. Δk = 0 (momentum matching). In the photon picture the nonlinear polarization converts one pump photon into a signal–idler pair and back; in the classical picture the three complex amplitudes are coupled by the second-order susceptibility and exchange flux while the medium itself stays passive and lossless.

With equal normalized couplings the flux exchange becomes the exact optical image of torque-free rigid-body rotation (the Euler top): the photon fluxes |a_k|² play the role of squared angular-momentum components, the Manley–Rowe invariants fix the invariant planes, and the trajectory is a closed periodic cycle on their intersection. The pump empties into the signal–idler pair and refills again — the exchange period T_ex is the period of that choreography — and the degenerate channel a₁ = a₂ (second-harmonic generation) reduces to a one-line closed form used as the verification anchor.

| Parameter | Value | Meaning |
|---|---|---|
| a₁(0), a₂(0) | 0.2, 0.3 (real) | signal and idler seed amplitudes |
| a₃(0) | 1.0·i (phase π/2) | pump seed; phase chosen so Im(Z) ≠ 0 |
| couplings γ₁, γ₂, γ₃ | 1, 1, 1 (normalized) | equal lossless χ⁽²⁾ coupling |
| phase matching | Δk = 0 | perfect collinear matching, no detuning |
| integration | T = 50, DOP853, rtol = atol = 1e-13 | max_step 0.02, dense output |
| SHG channel | s(0) = A = 1, p(0) = 0 | degenerate limit for the tanh² anchor |

**Model assumptions**

- Lossless medium: no linear or nonlinear absorption, so the Manley–Rowe relations hold exactly.
- Perfect phase matching Δk = 0; detuning and group-velocity mismatch are not modeled.
- Plane-wave, collinear interaction; diffraction and transverse effects are neglected.
- Equal normalized couplings γ₁ = γ₂ = γ₃ — the isotropic (Euler-top) case.
- Classical mean-field amplitudes; quantum noise and spontaneous parametric seeding are not modeled beyond the deterministic idler seed.
- Pump depletion is fully retained — no fixed-pump approximation is made.
- The exchange period is measured between refined pump-flux maxima; no analytic period formula is assumed anywhere.
- The fig03 sweep is a diagnostics artifact stored in the JSON figures block, not an acceptance check.

## 4. Governing equations

(E1) Resonant three-wave amplitude equations (equal couplings, Δk = 0):

$$\frac{da_1}{dt} = i\,a_2^{*}a_3, \qquad \frac{da_2}{dt} = i\,a_1^{*}a_3, \qquad \frac{da_3}{dt} = i\,a_1 a_2$$

(E2) Manley–Rowe invariants (photon-pair bookkeeping):

$$I_1 = |a_1|^2 + |a_3|^2, \qquad I_2 = |a_2|^2 + |a_3|^2, \qquad I_3 = |a_1|^2 - |a_2|^2$$

(E3) Degenerate (SHG) channel: closed-form plane-wave conversion:

$$\eta(t) = \tanh^2(At), \qquad s = A\,\mathrm{sech}(At), \qquad p = iA\,\tanh(At)$$

## 5. Scheme

![TRX-02 scheme — resonant three-wave mixing: a pump wave (ω₃, k₃) enters a lossless phase-matched χ⁽²⁾ crystal and exchanges photons with the signal (ω₁, k₁) and idler (ω₂, k₂) waves; energy and momentum matching close the resonance, and the Manley–Rowe relations keep the photon bookkeeping exact.](figures/scheme_trx02.svg)

*TRX-02 scheme — resonant three-wave mixing: a pump wave (ω₃, k₃) enters a lossless phase-matched χ⁽²⁾ crystal and exchanges photons with the signal (ω₁, k₁) and idler (ω₂, k₂) waves; energy and momentum matching close the resonance, and the Manley–Rowe relations keep the photon bookkeeping exact..*

The diagram encodes the following elements:

- **Pump wave** — gold sinusoid (ω₃, k₃, amplitude a₃) entering the crystal; its flux |a₃|² depletes into the pair and revives periodically
- **χ⁽²⁾ crystal** — lossless, perfectly phase-matched (Δk = 0) medium; inside it one pump photon splits into a signal–idler pair
- **Signal / idler waves** — blue and green sinusoids (ω₁, k₁) and (ω₂, k₂) leaving the crystal, seeded by a₁(0) = 0.2 and a₂(0) = 0.3
- **Energy matching** — ω₃ = ω₁ + ω₂: one pump photon ↔ one signal + one idler (down-conversion and its reverse, SFG)
- **Momentum matching** — k₃ = k₁ + k₂ in the co-propagating geometry, so Δk = 0 and the coupling accumulates over the medium
- **Manley–Rowe bookkeeping** — I₁ = |a₁|² + |a₃|², I₂ = |a₂|² + |a₃|², I₃ = |a₁|² − |a₂|² stay constant — the optical twin of vortex circulation bookkeeping

## 6. Mapping to TRIVORTEX

The mapping to TRIVORTEX is one-to-one at the structural level. The three complex amplitudes form an integrable triad exactly as three Kirchhoff vortices do: the Manley–Rowe relations I₁, I₂, I₃ play the role of the vortex integrals H, P, Q, I, the periodic pump depletion–revival cycle is the optical choreography that mirrors the vortex triangle's rotation, and the Euler-top equivalence of the equal-coupling case is the same integrable family that gives the Kirchhoff problem its elliptic solutions. Even the verification style is shared: the tanh² law anchors the numerics with a closed form, in the same spirit as the closed form of Theorem 3.1, and the photon-pair bookkeeping of the Manley–Rowe relations is the precise optical analogue of circulation bookkeeping in the vortex model. TRX-02 therefore serves as the optics-side twin of the program core and feeds the Kerr extension (TRX-04), the vortex verification (TRX-09) and the radiating three-body dynamics (TRX-11).

| Quantity in this study | TRIVORTEX analog | Comment |
|---|---|---|
| Three complex amplitudes a₁, a₂, a₃ | three vortices Γ₁, Γ₂, Γ₃ | both are integrable triads with quadratic invariants |
| Manley–Rowe invariants I₁, I₂, I₃ | vortex integrals H, P, Q, I | quadratic conservation laws that fix the orbit |
| Pump depletion / revival cycle T_ex | choreographic exchange of the vortex triangle | periodic circulation of the "energy" around the triad |
| Euler-top equivalence | Kirchhoff three-vortex equivalence | the same integrable family; shared elliptic solutions |
| SHG closed form tanh²(At) | closed form of Theorem 3.1 | an exact solution anchoring the numerics |

## 7. Dimensionless formulation

Time is measured in units of 1/(γA₀) with equal coupling γ and pump scale A₀; amplitudes are normalized so that |a_k|² is the photon-flux bookkeeping variable. Physical units map back through the standard χ⁽²⁾ coupled-wave normalization (Boyd, *Nonlinear Optics*, ch. 2); all results below are stated in these dimensionless units.

## 8. Numerical method

The three complex amplitudes are split into six real ODEs (real and imaginary parts) and integrated with an explicit Dormand–Prince 8(5,3) scheme at rtol = atol = 1e-13, max_step = 0.02, over t ∈ [0, 50] with dense output. The Manley–Rowe invariants are evaluated pointwise on 2500 samples along the trajectory, and their maximal excursion from the initial values (I₁ = 1.04, I₂ = 1.09, I₃ = −0.05) is recorded as the drift check; the same dense solution supplies the photon-flux series used by the figures.

The exchange period is extracted from the pump flux |a₃|²: local maxima are detected on a dense grid of 20001 samples, then refined by bounded scalar minimization with xatol = 1e-13. Two consecutive refined maxima give T_ex1 = 5.650961242 and T_ex2 = 5.650961155 — repeatability 8.7e-8 against the 1e-6 tolerance — and the flux at those maxima differs by 2.4e-15 (the revival check). Full depletion is tested against the 5% threshold: the pump minimum on the dense grid reaches 6.3e-5 of the peak flux 1.04.

The degenerate channel is integrated at the same tolerance from s(0) = 1, p(0) = 0 and compared with η(t) = tanh²(At) on 60 points over t ∈ [0.05, 3]; the maximal deviation is the SHG check. The fig03 parameter sweep (17 initial pump amplitudes in [0.4, 2.0], T = 50, rtol = 1e-10) is computed only in --figures mode and stored in the figures block of the JSON protocol. Every check stores value, target, tolerance, unit and pass flag; runs are deterministic, need no network access and no random seeds.

## 9. Verification protocol and acceptance checks

Every check is registered before the run: target, tolerance and unit are committed in the protocol, not chosen after the fact.

| Check | Target | Tolerance |
|---|---|---|
| Drift of I₁ = \|a₁\|² + \|a₃\|² over t ∈ [0, 50] | 0 | 1e-10 |
| Drift of I₂ = \|a₂\|² + \|a₃\|² over t ∈ [0, 50] | 0 | 1e-10 |
| Drift of I₃ = \|a₁\|² − \|a₂\|² over t ∈ [0, 50] | 0 | 1e-10 |
| Repeatability \|T_ex,2 − T_ex,1\| of the exchange period | 0 | 1e-6 |
| Pump revival error \|a₃(T_ex)\|² − \|a₃(0)\|² | 0 | 1e-8 |
| Full depletion: min \|a₃\|² < 5% of its peak | yes | exact |
| SHG conversion vs η(t) = tanh²(At) | 0 | 1e-8 |

**Recorded verification run** (mode: smoke, status: **PASS**, 7/7 checks)

| Check | Recorded value | Target | Tolerance | Unit | Verdict |
|---|---|---|---|---|---|
| `ManleyRowe_I13_drift` | 5.1070e-15 | 0 | 1.0000e-10 | dimless | PASS |
| `ManleyRowe_I23_drift` | 1.7764e-15 | 0 | 1.0000e-10 | dimless | PASS |
| `ManleyRowe_I12diff_drift` | 3.7748e-15 | 0 | 1.0000e-10 | dimless | PASS |
| `Pump_period_repeatability` | 4.4697e-08 | 0 | 1.0000e-06 | dimless | PASS |
| `Pump_revival_error` | 2.4425e-15 | 0 | 1.0000e-08 | dimless | PASS |
| `Pump_full_depletion_occurs` | 1 | 1 | 1.0000e-12 | bool | PASS |
| `SHG_tanh2_conversion_error` | 2.2204e-16 | 0 | 1.0000e-08 | dimless | PASS |

**Check notes** — what each number means:

| Check | Note |
|---|---|
| `ManleyRowe_I13_drift` | \|a1\|^2+\|a3\|^2 |
| `ManleyRowe_I23_drift` | \|a2\|^2+\|a3\|^2 |
| `ManleyRowe_I12diff_drift` | \|a1\|^2-\|a2\|^2 |
| `Pump_period_repeatability` | T_ex1=5.650961203, T_ex2=5.650961158 |
| `Pump_revival_error` | \|a3\|^2 after one full exchange period |
| `Pump_full_depletion_occurs` | pump drops below 5% of its peak |
| `SHG_tanh2_conversion_error` | eta(t) = tanh^2(A t), plane-wave second-harmonic generation |

## 10. Figure gallery (300 dpi)

![{'cap_en': 'Overview of the model: resonance geometry of the wave triad and the initial photon-flux bookkeeping.', 'cap_ru': 'Обзор модели: резонансная геометрия триады волн и начальная фотонная бухгалтерия потоков.', 'walk_en': 'Panel (a) shows the photon-energy diagram of the resonant triad: the pump photon at ω₃ = ω₁ + ω₂ splits into a signal–idler pair (down-conversion) with the reverse sum-frequency channel; panel (b) stacks the initial fluxes |a₁|² = 0.04, |a₂|² = 0.09, |a₃|² = 1.00 into the Manley–Rowe pairs I₁ = 1.04 and I₂ = 1.09.', 'walk_ru': 'Панель (a) показывает фотонно-энергетическую диаграмму резонансной триады: фотон накачки при ω₃ = ω₁ + ω₂ распадается на пару «сигнал — холостая волна» (параметрическая расщепка) с обратным каналом суммарной частоты; панель (b) складывает начальные потоки |a₁|² = 0.04, |a₂|² = 0.09, |a₃|² = 1.00 в пары Мэнли–Роу I₁ = 1.04 и I₂ = 1.09.'}](figures/fig01_resonance_geometry.png)

*{'cap_en': 'Overview of the model: resonance geometry of the wave triad and the initial photon-flux bookkeeping.', 'cap_ru': 'Обзор модели: резонансная геометрия триады волн и начальная фотонная бухгалтерия потоков.', 'walk_en': 'Panel (a) shows the photon-energy diagram of the resonant triad: the pump photon at ω₃ = ω₁ + ω₂ splits into a signal–idler pair (down-conversion) with the reverse sum-frequency channel; panel (b) stacks the initial fluxes |a₁|² = 0.04, |a₂|² = 0.09, |a₃|² = 1.00 into the Manley–Rowe pairs I₁ = 1.04 and I₂ = 1.09.', 'walk_ru': 'Панель (a) показывает фотонно-энергетическую диаграмму резонансной триады: фотон накачки при ω₃ = ω₁ + ω₂ распадается на пару «сигнал — холостая волна» (параметрическая расщепка) с обратным каналом суммарной частоты; панель (b) складывает начальные потоки |a₁|² = 0.04, |a₂|² = 0.09, |a₃|² = 1.00 в пары Мэнли–Роу I₁ = 1.04 и I₂ = 1.09.'}.*

![{'cap_en': 'Headline result: periodic pump depletion and revival over T = 50, with one exchange cycle enlarged.', 'cap_ru': 'Главный результат: периодическое истощение и возрождение накачки на T = 50 с увеличенным циклом обмена.', 'walk_en': 'Over T = 50 the pump makes about 8.8 full cycles (T_ex = 5.650961242): it collapses to |a₃|² = 6.3e-5 — 99.994% of its peak 1.04 removed — and revives with error 2.4e-15; the zoom shows the refined maxima and the exchange period arrow.', 'walk_ru': 'За T = 50 накачка совершает около 8.8 полных циклов (T_ex = 5.650961242): она проседает до |a₃|² = 6.3e-5 — снято 99.994% пика 1.04 — и возрождается с ошибкой 2.4e-15; на увеличении видны уточнённые максимумы и стрелка периода обмена.'}](figures/fig02_pump_depletion.png)

*{'cap_en': 'Headline result: periodic pump depletion and revival over T = 50, with one exchange cycle enlarged.', 'cap_ru': 'Главный результат: периодическое истощение и возрождение накачки на T = 50 с увеличенным циклом обмена.', 'walk_en': 'Over T = 50 the pump makes about 8.8 full cycles (T_ex = 5.650961242): it collapses to |a₃|² = 6.3e-5 — 99.994% of its peak 1.04 removed — and revives with error 2.4e-15; the zoom shows the refined maxima and the exchange period arrow.', 'walk_ru': 'За T = 50 накачка совершает около 8.8 полных циклов (T_ex = 5.650961242): она проседает до |a₃|² = 6.3e-5 — снято 99.994% пика 1.04 — и возрождается с ошибкой 2.4e-15; на увеличении видны уточнённые максимумы и стрелка периода обмена.'}.*

![{'cap_en': 'Parameter sweep over the initial pump amplitude |a₃(0)| ∈ [0.4, 2.0]: exchange period and depletion depth.', 'cap_ru': 'Развёртка по начальной амплитуде накачки |a₃(0)| ∈ [0.4, 2.0]: период обмена и глубина истощения.', 'walk_en': 'Across 17 runs (T = 50, rtol = 1e-10) the exchange period decreases monotonically from 9.028821 to 3.556606, while the depletion depth min/max of |a₃|² stays below 5.2e-6 — every regime of the sweep is pumped to essentially complete conversion.', 'walk_ru': 'По 17 прогонам (T = 50, rtol = 1e-10) период обмена монотонно убывает от 9.028821 до 3.556606, а глубина истощения min/max величины |a₃|² не превышает 5.2e-6 — весь диапазон развёртки прокачан до практически полной конверсии.'}](figures/fig03_parameter_sweep.png)

*{'cap_en': 'Parameter sweep over the initial pump amplitude |a₃(0)| ∈ [0.4, 2.0]: exchange period and depletion depth.', 'cap_ru': 'Развёртка по начальной амплитуде накачки |a₃(0)| ∈ [0.4, 2.0]: период обмена и глубина истощения.', 'walk_en': 'Across 17 runs (T = 50, rtol = 1e-10) the exchange period decreases monotonically from 9.028821 to 3.556606, while the depletion depth min/max of |a₃|² stays below 5.2e-6 — every regime of the sweep is pumped to essentially complete conversion.', 'walk_ru': 'По 17 прогонам (T = 50, rtol = 1e-10) период обмена монотонно убывает от 9.028821 до 3.556606, а глубина истощения min/max величины |a₃|² не превышает 5.2e-6 — весь диапазон развёртки прокачан до практически полной конверсии.'}.*

![{'cap_en': 'Dynamics diagnostics: Manley–Rowe residuals along the orbit and the SHG closed-form comparison.', 'cap_ru': 'Диагностика динамики: остатки Мэнли–Роу вдоль орбиты и сравнение с замкнутой формулой SHG.', 'walk_en': 'The invariant residuals stay at the 1e-15 level (max 5.3e-15 against the 1e-10 tolerance), and the degenerate channel tracks η(t) = tanh²(At) to 2.220446e-16 — one unit in the last place of double precision.', 'walk_ru': 'Остатки инвариантов держатся на уровне 1e-15 (максимум 5.3e-15 против допуска 1e-10), а вырожденный канал следует за η(t) = tanh²(At) с точностью 2.220446e-16 — одна единица последнего разряда двойной точности.'}](figures/fig04_invariants_shg.png)

*{'cap_en': 'Dynamics diagnostics: Manley–Rowe residuals along the orbit and the SHG closed-form comparison.', 'cap_ru': 'Диагностика динамики: остатки Мэнли–Роу вдоль орбиты и сравнение с замкнутой формулой SHG.', 'walk_en': 'The invariant residuals stay at the 1e-15 level (max 5.3e-15 against the 1e-10 tolerance), and the degenerate channel tracks η(t) = tanh²(At) to 2.220446e-16 — one unit in the last place of double precision.', 'walk_ru': 'Остатки инвариантов держатся на уровне 1e-15 (максимум 5.3e-15 против допуска 1e-10), а вырожденный канал следует за η(t) = tanh²(At) с точностью 2.220446e-16 — одна единица последнего разряда двойной точности.'}.*

## 11. Results (full run)

```text
ManleyRowe_I13_drift                = 5.329071e-15   (tol 1e-10)
ManleyRowe_I23_drift                = 4.218847e-15   (tol 1e-10)
ManleyRowe_I12diff_drift            = 4.496403e-15   (tol 1e-10)
Pump_period_repeatability           = 8.743724e-08   (T_ex1=5.650961242, T_ex2=5.650961155)
Pump_revival_error                  = 2.442491e-15   (tol 1e-8)
Pump_full_depletion_occurs          = PASS (pump drops below 5% of its peak)
SHG_tanh2_conversion_error          = 2.220446e-16   (tol 1e-8)
status: PASS (7/7)
```

## 12. Analysis

**Invariants.** Over the full run T = 50 (about 8.8 exchange cycles) the Manley–Rowe drifts are 5.329071e-15 for I₁, 4.218847e-15 for I₂ and 4.496403e-15 for I₃ — more than four orders of magnitude below the 1e-10 acceptance tolerance and at the round-off level of double precision. The orbit is therefore exactly confined to the intersection of the invariant surfaces, which is the geometric content of integrability for the three-wave triad.

**Periodic exchange.** The pump flux oscillates with the refined exchange period T_ex = 5.650961242; consecutive periods agree to 8.743724e-08, and the flux at successive maxima reproduces itself to 2.442491e-15. Between maxima the pump collapses to |a₃|² = 6.32941e-05 — 99.994% of its peak value 1.04 removed — so the cycle is a genuine full-depletion–revival choreography, not a shallow modulation.

**Parameter sweep.** Sweeping the initial pump amplitude over [0.4, 2.0] in 17 runs, the exchange period decreases monotonically from 9.028821 to 3.556606: stronger pumps exchange photons faster. The depletion depth (min/max of |a₃|² over each run) stays between 4.2e-10 and 5.2e-6 across the whole grid — every regime of the sweep reaches essentially complete conversion, and the sweep invariant drift (≤ 1.5e-9 at the looser sweep tolerance 1e-10) confirms that the map itself is clean.

**Closed-form anchor.** In the degenerate channel the numerical conversion efficiency follows η(t) = tanh²(At) with maximal deviation 2.220446e-16 over the 60 sample points — one unit in the last place of double precision. The exact solution validates the normalization, the phase convention and the integrator in one shot; it is the optical counterpart of anchoring the vortex choreography on the closed form of Theorem 3.1.

## 13. Discussion and honest boundaries

The model is deliberately minimal: equal couplings, plane waves, perfect phase matching and no losses. Within these assumptions every conclusion is an exact statement about the governing equations rather than a simulation of a specific crystal. The natural extensions each preserve the verification style established here: detuning (Δk ≠ 0 adds a linear phase term and breaks the strict periodicity), group-velocity mismatch for pulses, unequal couplings (the asymmetric Euler top), cavity boundary conditions (the driven OPO), and quantum seeding by spontaneous parametric down-conversion.

The numerical regime is stated honestly. The verification numbers come exclusively from rtol = atol = 1e-13 runs; the fig03 sweep uses the looser 1e-10 because the deep pump minima are sharp features that dominate integration cost, and its outputs are stored as figure data rather than acceptance checks. Physical units map back through the standard χ⁽²⁾ normalization (for MgO:LiNbO₃, |χ⁽²⁾| ≈ 4 pm/V at 1 µm), so T_ex can be translated into a crystal length once the input intensities are fixed.

Within the program, this study anchors the integrable-triad block of the optics line: TRX-04 extends the pair interaction to spatial Kerr solitons (the soliton molecule), TRX-09 verifies the vortex twin of the same integrable family, and TRX-11 keeps the Hamiltonian three-body core but adds radiation. Together with TRX-01 and TRX-12 they close the loop between the celestial, the optical and the vortex formulations of TRIVORTEX.

## 14. Conclusions

- The equal-coupling three-wave system conserves the Manley–Rowe invariants to ≤ 5.329071e-15 over T = 50 (tolerance 1e-10) — machine-level photon bookkeeping.
- Pump depletion and revival is exactly periodic: T_ex = 5.650961242, consecutive periods agreeing to 8.743724e-08 and the revival flux reproduced to 2.442491e-15.
- The pump undergoes genuine full depletion, collapsing to |a₃|² = 6.32941e-05 — 99.994% of its peak flux 1.04 removed — before reviving.
- The exchange period is tunable by the pump amplitude: T_ex decreases monotonically from 9.028821 to 3.556606 over |a₃(0)| ∈ [0.4, 2.0], with depletion depth ≤ 5.2e-6 across the sweep.
- The degenerate (SHG) channel reproduces the closed form η(t) = tanh²(At) to 2.220446e-16 — one unit in the last place of double precision.
- The system is canonically equivalent to the Euler top and hence to the Kirchhoff three-vortex problem, making TRX-02 the optical twin of the TRIVORTEX core.

## 15. The monograph and its renditions

The complete monograph of this study exists in four renditions — Russian and English are separate documents, each in a typeset PDF and an editable DOCX:

| Rendition | Path |
|---|---|
| Monograph (English, PDF) | `monograph/monograph_EN.pdf` |
| Monograph (English, DOCX) | `monograph/monograph_EN.docx` |
| Monograph (Russian, PDF) | `monograph/monograph_RU.pdf` |
| Monograph (Russian, DOCX) | `monograph/monograph_RU.docx` |
| Reading-room copy | `publications/pdf/TRX-02-three-wave-mixing_EN.pdf` · `publications/pdf/TRX-02-three-wave-mixing_RU.pdf` |
| HTML source | `publications/html/TRX-02-three-wave-mixing.html` |

**Monograph abstract.** This monograph treats the resonant three-wave interaction in a lossless, perfectly phase-matched χ⁽²⁾ crystal — the canonical three-body problem of nonlinear optics. Three complex amplitudes (pump, signal, idler) obey the equal-coupling amplitude equations, a Hamiltonian system canonically equivalent to the Euler top and hence to the Kirchhoff three-vortex problem at the core of TRIVORTEX. The study verifies the integrable structure to machine precision: over T = 50 — roughly 8.8 full exchange cycles — the Manley–Rowe invariants drift by at most 5.329071e-15, more than four orders below the 1e-10 acceptance tolerance; the exchange is exactly periodic with T_ex = 5.650961242, consecutive periods agreeing to 8.7e-8; the pump undergoes genuine full depletion, collapsing to |a₃|² = 6.3e-5 (99.994% of its peak 1.04 removed) and reviving with error 2.4e-15; and the degenerate channel reproduces the closed-form conversion law η(t) = tanh²(At) to 2.220446e-16 — one unit in the last place of double precision. A sweep over the initial pump amplitude shows the exchange period monotonically tunable from 9.03 to 3.56. All seven acceptance checks pass.

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
| `t` | 600 | 0 … 20 |
| `n1` | 600 | 0.04 … 0.7407238519 |
| `n2` | 600 | 0.09 … 0.7907238519 |
| `n3` | 600 | 1 … 0.2992761481 |

**Reproduction matrix**

| Command | What it does |
|---|---|
| `python3 research/TRX-02-three-wave-mixing/code/trx02_three_wave_mixing.py` | full run: physics + acceptance checks (0.6 s) |
| `python3 research/TRX-02-three-wave-mixing/code/trx02_three_wave_mixing.py --smoke` | CI guard: same checks, seconds-scale settings |
| `python3 research/TRX-02-three-wave-mixing/code/trx02_three_wave_mixing.py --figures` | regenerates the 300-dpi figure set |
| `make research-smoke` | all twelve studies in smoke mode |
| `make research-figures` | all twelve studies + figure sets |

## 17. Cross-links within the program

- **TRX-09** verifies the vortex twin of the same integrable family.
- **TRX-04** extends the pair interaction to spatial Kerr solitons.
- **TRX-11** keeps the Hamiltonian three-body core but adds radiation.
- **TRX-01** shares the verification culture: closed-form and invariant-based acceptance checks at machine precision.

## 18. Inside the script

The executable is a single deterministic file, `code/trx02_three_wave_mixing.py`, ~pure `numpy`/`scipy` with no network access and no random state beyond fixed seeds. One run executes the full physics of the study, evaluates every registered acceptance check against its committed target and tolerance, and writes the JSON protocol — the same file quoted in §9.

| Mode | Invocation | What happens |
|---|---|---|
| Full | `python3 code/trx02_three_wave_mixing.py` | complete experiment, all checks, JSON protocol (0.6 s) |
| Smoke | `python3 code/trx02_three_wave_mixing.py --smoke` | identical acceptance logic at seconds-scale settings — the CI mode |
| Figures | `python3 code/trx02_three_wave_mixing.py --figures` | regenerates the schematic + the four 300-dpi PNG panels |

**Outputs per run**

| File | Produced by | Content |
|---|---|---|
| `results/trx02_results.json` | every mode | status, checks (value/target/tol/unit/pass/note), series, meta |
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
| Previous study | TRX-001 |
| Next study | TRX-003 |

## 21. Notation

| Symbol | Meaning |
|---|---|
| a₁, a₂, a₃ | complex amplitudes of signal, idler and pump |
| a* | complex conjugate |
| \|a_k\|² | photon flux in wave k (dimensionless) |
| I₁, I₂, I₃ | Manley–Rowe invariants |
| γ_k | coupling coefficients (all 1 after normalization) |
| Δk | phase mismatch k₃ − k₁ − k₂ |
| T_ex | exchange period between successive pump maxima |
| η | SHG conversion efficiency |
| A | initial amplitude of the SHG channel |
| t, T | time and integration span (dimensionless) |

## 22. References

1. Manley, J. M., Rowe, H. E. (1956). *Some general properties of nonlinear elements — Part I. General energy relations.* Proc. IRE 44, 904–913.
2. Franken, P. A., Hill, A. E., Peters, C. W., Weinreich, G. (1961). *Generation of optical harmonics.* Phys. Rev. Lett. 7, 118–119.
3. Armstrong, J. A., Bloembergen, N., Ducuing, J., Pershan, P. S. (1962). *Interactions between light waves in a nonlinear dielectric.* Phys. Rev. 127, 1918–1939.
4. Kroll, N. M. (1962). *Parametric amplification in spatially extended media and application to the design of tunable oscillators.* Phys. Rev. 127, 1207–1213.
5. Giordmaine, J. A., Miller, R. C. (1965). *Tunable coherent parametric oscillation in LiNbO₃ at optical frequencies.* Phys. Rev. Lett. 14, 973–976.
6. Kaup, D. J., Reiman, A., Bers, A. (1979). *Space-time evolution of nonlinear three-wave interactions. I. Interactions in a homogeneous medium.* Rev. Mod. Phys. 51, 275–309.
7. Boyd, R. W. (2008). *Nonlinear Optics*, 3rd ed., Academic Press.

## 23. Glossary

| Term | Definition |
|---|---|
| Three-wave mixing | resonant nonlinear-optical process in which waves at ω₁, ω₂ and ω₃ = ω₁ + ω₂ exchange photons through a χ⁽²⁾ nonlinearity |
| Pump / signal / idler | the high-frequency wave a₃ and the generated pair a₁, a₂ of a down-conversion triad |
| Manley–Rowe relations | quadratic conservation laws for photon fluxes, originally derived for nonlinear microwave elements (1956) |
| Photon flux \|a_k\|² | normalized intensity proportional to the photon flow carried by wave k |
| Pump depletion | transfer of pump flux into the signal–idler pair until the pump is (almost) emptied |
| Exchange period T_ex | time between successive pump maxima — one full choreographic cycle of the triad |
| SHG | second-harmonic generation: the degenerate channel ω₁ = ω₂ = ω₃/2 |
| Conversion efficiency η | share of the total flux carried by the second harmonic, η = \|p\|²/(\|p\|² + \|s\|²) |
| Phase matching | condition k₃ = k₁ + k₂ (Δk = 0) letting the coupling accumulate over the medium |
| Euler top | torque-free rigid-body rotation; the canonical integrable equivalent of the equal-coupling three-wave system |

## 24. Appendix A. Full parameter table

| Symbol | Value | Role |
|---|---|---|
| a₁(0), a₂(0) | 0.2, 0.3 | signal/idler seeds (real) |
| a₃(0) | 1.0·i | pump seed, phase π/2 |
| γ₁, γ₂, γ₃ | 1, 1, 1 | normalized couplings |
| Δk | 0 | phase mismatch |
| T | 50 | integration span of the main run |
| rtol, atol | 1e-13 | DOP853 tolerances (main run) |
| max_step | 0.02 | integrator step cap (main run) |
| dense samples | 20001 | pump-maximum detection grid |
| A | 1 | SHG seed amplitude |
| sweep | \|a₃(0)\| ∈ [0.4, 2.0], 17 pts, rtol 1e-10 | fig03 parameter sweep (--figures mode) |

**Protocol-level parameter snapshot** (`results` JSON, `meta` block):

| Key | Value |
|---|---|
| `equations` | `["da1/dt = i a2*a3 ; da2/dt = i a1* a3 ; da3/dt = i a1 a2", "I1 = \|a1\|^2+\|a3\|^2 ; I2 = \|a2\|^2+\|a3\|^2 ; I3 = \|a1\|^2-\|a2\|^2", "SHG degenerate limit: eta(t) = tanh^2(A t)"]` |
| `initial_state` | `{"a1": "0.2", "a2": "0.3", "a3": "1.0j"}` |
| `exchange_period_Tex` | `5.650961203091371` |
| `invariants_initial` | `[1.04, 1.09, -0.04999999999999999]` |
| `note` | `"equal-coupling lossless system; canonically equivalent to the Euler top (hence to the Kirchhoff three-vortex problem used by TRIVORTEX)"` |

## 25. Appendix B. BibTeX

```bibtex
@article{manley1956,
  author  = {Manley, J. M. and Rowe, H. E.},
  title   = {Some general properties of nonlinear elements. Part {I}: General energy relations},
  journal = {Proceedings of the IRE},
  year    = {1956}, volume = {44}, number = {7}, pages = {904--913}}

@article{armstrong1962,
  author  = {Armstrong, J. A. and Bloembergen, N. and Ducuing, J. and Pershan, P. S.},
  title   = {Interactions between light waves in a nonlinear dielectric},
  journal = {Physical Review},
  year    = {1962}, volume = {127}, pages = {1918--1939}}

@article{kaup1979,
  author  = {Kaup, D. J. and Reiman, A. and Bers, A.},
  title   = {Space-time evolution of nonlinear three-wave interactions. {I}: Interactions in a homogeneous medium},
  journal = {Reviews of Modern Physics},
  year    = {1979}, volume = {51}, pages = {275--309}}

@book{boyd2008,
  author    = {Boyd, R. W.},
  title     = {Nonlinear Optics},
  edition   = {3rd},
  publisher = {Academic Press}, year = {2008}}
```

## 26. How to cite

Cite the repository through [`CITATION.cff`](../../CITATION.cff) (DOI 10.5281/zenodo.21825394, version 1.0.0); this study is part of the TRIVORTEX Research Program. If you cite the study alone, name the monograph rendition you used and attach the JSON protocol of the run you reproduced.

```bibtex
@misc{trivortextrx022026isaev,
  author       = {Isaev, Iskhak Khamzatovich},
  title        = {Resonant Three-Wave Interaction (Manley–Rowe, χ⁽²⁾ Optics) (TRIVORTEX Research Program, TRX-02)},
  year         = {2026},
  howpublished = {Zenodo},
  doi          = {10.5281/zenodo.21825394},
  url          = {https://github.com/wild8highlander/research-papers}
}
```

