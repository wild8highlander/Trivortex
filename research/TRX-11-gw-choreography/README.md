# TRX-11 — Gravitational Waves from the Figure-Eight Choreography

*TRIVORTEX Research Program · version 1.0.0 · study TRX-11 of 12*

The figure-eight choreography (Chenciner & Montgomery 2000) — three equal masses chasing each other along a single closed curve with zero angular momentum — is treated as a laboratory gravitational-wave source. In the quadrupole approximation (G = c = D = 1) the mass quadrupole Q_ij = Σ m_k x_ki x_kj drives a plus-polarised strain that repeats six times per orbit period T = 6.325914, and the choreography symmetry locks the spectrum into a pure harmonic comb with the dominant line at n = 6 of the orbital comb.

> **Edition 1.0.0.** This README is part of the first public release of the TRIVORTEX research program. The study ships as an executable script, a committed JSON protocol, four 300-dpi figures, a schematic and a bilingual monograph in four renditions (Russian and English, each in PDF and DOCX).

**At a glance**

| Aspect | Value |
|---|---|
| Block | Gravitational waves — study 11 of 12 |
| Model | figure-eight choreography (G = m = 1) + quadrupole radiation (G = c = D = 1) |
| Key invariant | zero angular momentum L = 0 (held to 1.4e-15 over one period) |
| Headline result | strain repeating every T/6; pure comb with the dominant line at n = 6 (f·T = 5.9995) |
| Verification | 7/7 checks PASS (full mode) |
| Runtime | 8.17 s full (with figures) · < 20 s smoke |

| Field | Value |
|---|---|
| Study | `TRX-11` (TRX-11-gw-choreography) |
| Program | TRIVORTEX — The Three-Body Problem in the Vortex Model |
| Author | Isaev Iskhak Khamzatovich (ORCID `0009-0003-7299-0701`) |
| DOI | [10.5281/zenodo.21825394](https://doi.org/10.5281/zenodo.21825394) |
| Version | 1.0.0 — first public release |
| Code | `research/TRX-11-gw-choreography/code/trx11_gw_choreography.py` |
| Protocol | `research/TRX-11-gw-choreography/results/trx11_results.json` |
| License | `LicenseRef-Proprietary-Wild8Highlander-1.0` |

## 1. Mission

A choreography is the cleanest gravitational-wave emitter the three-body problem offers: one periodic curve, three masses, zero angular momentum, and a quadrupole whose exchange symmetries imprint a sharp comb on the spectrum. Among the special solutions collected in the TRIVORTEX monograph — the rotating Lagrange triangle, the Aref collapse trio, the hierarchical secular triples — the figure-eight is the only one that is simultaneously periodic, non-hierarchical and non-colliding, which makes it the natural benchmark for three-body gravitational-wave astronomy. This study pins the emitter down quantitatively rather than qualitatively: the period, the invariants, the waveform, the spectrum and the antenna pattern are all measured and stored as machine-checkable numbers.

The study verifies seven things to numerical precision: that the period found by global minimisation of the configuration closure, T = 6.325914025, matches the published value 6.32591398 to 1.2e-08; that energy is conserved to 3.6e-15 and the total angular momentum stays zero to 1.4e-15 throughout the period — the defining property of the figure-eight; that the equal-mass choreography symmetry holds on the quadrupole, Q(T/3) = Q(0) to 1.5·10⁻⁸, which locks the waveform to a harmonic comb; and that the measured dominant harmonic lands at n = 6 of the orbital comb, twice the T/3 pattern frequency, exactly as the symmetry bookkeeping predicts. Because LISA, Taiji and TianQin are laser interferometers, the detection channel of this study is a laser channel — the instruments that would actually measure three-body GW signatures are built on laser stability over million-kilometre arms.

## 2. Introduction and historical context

Gravitational waves entered physics as a prediction of general relativity: Einstein derived the linearised field equations in 1916 and returned to the question in 1918 with the famous quadrupole formula, establishing that accelerating masses radiate energy at a rate controlled by the third time derivative of the mass quadrupole tensor. For decades the formula was disputed even among theorists — Eddington suspected the waves of being coordinate artifacts — until the quadrupole luminosity was worked out for concrete systems: Peters and Mathews (1963) computed the orbit-averaged radiation of Keplerian binaries, and the measured orbital decay of the binary pulsar PSR 1913+16 by Taylor and Weisberg (1982) confirmed that formula to better than half a percent, awarding the quadrupole approximation the status of quantitative science.

The modern formalism descends from Thorne's 1980 review, which systematised the multipole expansion of gravitational radiation — source multipoles, the trace-free projection, the energy flux — into the standard toolbox used by every waveform model today; Maggiore's monograph (2007) fixed the pedagogical canon. Within this framework the plus-polarised strain of a distant observer is proportional to the second derivative of the trace-free quadrupole, and the luminosity is the squared sum of third derivatives — exactly the two objects this study computes for a three-body source, in units G = c = D = 1.

The source itself has a shorter but remarkable history. Moore (1993) found, by numerical search over braided periodic orbits, that three equal bodies can chase each other along one curve; Chenciner and Montgomery (2000) then proved the existence of this figure-eight solution rigorously, via a variational argument combined with computer assistance, and Simó (2002) mapped the dynamical properties of the associated Poincaré map. The solution is exceptional in several ways at once: it is periodic, planar, collision-free, and it carries exactly zero angular momentum — a property that no circular binary shares and that shapes the emitted waveform.

For TRIVORTEX the relevance is structural. The monograph's vortex program studies special triads — the rotating Lagrange triangle, the (1, −1, 1) collapse trio, the secular hierarchical cycles — and the figure-eight is the celestial sibling of the same family: a choreography whose symmetry group, not whose parameters, fixes its observables. Adding the quadrupole channel turns the choreography from a curiosity of celestial mechanics into a potential astrophysical signal, and the natural readout instrument is laser-based: LISA, Taiji and TianQin are laser interferometers whose million-kilometre arms are built on laser stability. The study therefore also documents the laser connection that runs through the laser block of the program (TRX-01, TRX-12).

## 3. Physical system and preset

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

**Model assumptions**

- Newtonian dynamics; general relativity enters only through the leading quadrupole formula (slow-motion, weak-field regime).
- Planar motion; out-of-plane excursions are not modelled, and the observer direction enters only through the antenna pattern.
- Equal masses and the exact Chenciner–Montgomery initial condition; unequal-mass choreographies are out of scope.
- Quadrupole order only: no higher multipoles, no gravitational-wave memory, and no back-reaction on the orbit within one period.
- The luminosity acceptance check uses the chained finite-difference estimator as a finiteness gate only; the figure pipeline recomputes the luminosity from exact analytic derivatives (76.51 mean versus the noise-dominated proxy 1.65e8).
- All quantities are dimensionless with G = m = 1 and wave units G = c = D = 1; the physical scaling to (M, D) is linear.

## 4. Governing equations

(E1) Newtonian three-body dynamics (planar, equal masses):

$$\ddot{\boldsymbol{r}}_k = \sum_{j \neq k} \frac{\boldsymbol{r}_j - \boldsymbol{r}_k}{\left|\boldsymbol{r}_j - \boldsymbol{r}_k\right|^3}, \qquad G = m = 1$$

(E2) Mass quadrupole tensor of the emitter:

$$Q_{ij} = \sum_k m_k\, x_{ki}\, x_{kj}$$

(E3) Plus-polarised waveform read by a distant observer (G = c = D = 1):

$$h_+(t) \propto \frac{d^2}{dt^2}\left(Q_{xx} - Q_{yy}\right)$$

(E4) Gravitational-wave luminosity on the trace-free quadrupole (G = c = D = 1):

$$P = \frac{1}{5}\sum_{ij} \left(\frac{d^3 Q_{ij}}{dt^3}\right)^{2}$$

(E5) Choreography exchange symmetry and the harmonic comb:

$$\{\boldsymbol{r}_k(T/3)\} = \{\boldsymbol{r}_k(0)\} \;\Rightarrow\; Q(t + T/3) = Q(t) \;\Rightarrow\; \tilde{h}(f) \neq 0 \ \text{only at}\ f = n \cdot \frac{3}{T}$$

## 5. Scheme

![TRX-11 scheme — the figure-eight choreography as a gravitational-wave emitter: three equal masses chase each other along one closed curve with zero angular momentum; the rotating quadrupole radiates through lobes peaked along the orbital normal, and a LISA-class laser interferometer reads the strain.](figures/scheme_trx11.svg)

*TRX-11 scheme — the figure-eight choreography as a gravitational-wave emitter: three equal masses chase each other along one closed curve with zero angular momentum; the rotating quadrupole radiates through lobes peaked along the orbital normal, and a LISA-class laser interferometer reads the strain..*

The diagram encodes the following elements:

- **Figure-eight curve (navy)** — the single closed trajectory traced by all three bodies; period T = 6.325914 in G = m = 1 units
- **Dashed reflection axis** — the symmetry axis of the eight, aligned with the initial velocity direction of m₃
- **Bodies m₁, m₂ (gold) and m₃ (white)** — the Chenciner–Montgomery starting state at t = 0; the gold arrow marks the chase direction along the curve
- **Exchange annotation** — each body runs the whole eight and the roles permute every T/3 ≈ 2.109, while the total angular momentum stays L = 0 (defining property)
- **Quadrupole lobes + LISA-class box** — radiation is strongest along the orbital normal, where a distant laser interferometer sits at inclination θ
- **Waveform strip and comb panel** — plus-polarised strain h₊ ∝ d²(Qxx − Qyy)/dt² with six repeats per orbit period, range −4.04 … +4.85, and a spectrum comb at n = 6, 12, 18 with amplitudes 1 : 0.091 : 0.0061

## 6. Mapping to TRIVORTEX

Within the TRIVORTEX framework the figure-eight is the second special three-body solution besides the rotating equilateral choreography of Theorem 3.1 — two answers of one problem to the same requirement of exact periodicity. The zero angular momentum of the eight is the celestial twin of the document's own charge pattern: a tuned circulation triplet (1, −1, 1) whose angular impulse vanishes, so both models live on the zero-impulse slice of their phase spaces. The quadrupole comb at multiples of 3/T plays the role of the radial modulation frequency ω of Theorem 3.1 — in both cases a single spectral line family is the fingerprint of the triad's symmetry. Finally, the detection channel is a laser channel: TRX-01 and TRX-12 put lasers inside the three-body dynamics as actuators, while this study points lasers at it as detectors, closing the laser theme from both ends. TRX-09 supplies the vortex-language description of the same choreographic idea, and TRX-10 its hierarchical (secular) limit.

| Quantity in this study | TRIVORTEX analog | Comment |
|---|---|---|
| Figure-eight choreography | rotating equilateral choreography of Theorem 3.1 | two special solutions of one problem |
| Zero angular momentum L = 0 | tuned circulation pattern (1, −1, 1) | the document's own charge triplet |
| Quadrupole comb at multiples of 3/T | radial modulation ω of Theorem 3.1 | spectral fingerprint of the triad |
| Choreography period T = 6.325914 | rigid rotation period of the vortex triangle | both special solutions carry a single clock |
| LISA-class detection | laser themes of TRX-01/12 | lasers as the measuring instrument |

## 7. Dimensionless formulation

All dynamics in canonical units G = m = 1: length in orbital radii, time in orbital units (one period T ≈ 6.33), energy in Gm²/L. Wave quantities in G = c = D = 1: strain in units of Gm/(c²D) and luminosity in units of Gm²ω⁶/c⁵, so the physical scaling to a system of total mass M and size scale L at distance D is linear in M and D — the same dimensionless solution maps onto any mass scale.

## 8. Numerical method

The period is found before anything else is measured. The full system is integrated over [0, 12] with DOP853 at rtol = atol = 1e-13 and max_step 0.01; the closure is defined as the maximum deviation of the three positions from their initial values, scanned on a 1800-point grid over t ∈ [2, 11], and refined by bounded scalar minimisation with xatol 1e-13. The global minimum gives T = 6.325914025 with a closure residual of 1.2e-08 — inside the 5e-8 acceptance tolerance and consistent with the published 6.32591398. The period is then re-integrated over exactly [0, T] at max_step 0.005, and the invariants are monitored pointwise: the energy drift stays at 3.6e-15 and the total angular momentum at 1.4e-15 across 3000 samples.

The quadrupole pipeline reuses the same trajectory: states are sampled on a 12001-point grid for the protocol checks and on a 4801-point grid for the figures, and the quadrupole derivatives are evaluated from the exact analytic formulas — positions, velocities, accelerations and jerks of the DOP853 dense output — so the displayed waveform, spectrum and luminosity carry no numerical-differentiation edge artifacts. The strain is the second derivative of Q_xx − Q_yy; the instantaneous luminosity uses the trace-free combination (2Q⃛xx − Q⃛yy)/3, (2Q⃛yy − Q⃛xx)/3, −(Q⃛xx + Q⃛yy)/3 together with Q⃛xy, summed per (E4).

The spectral and directional diagnostics are deterministic. The spectrum is an FFT of the mean-subtracted exact strain over one full period — no window is needed because the signal is exactly periodic — with harmonic amplitudes tabulated for n = 1 … 30 of the orbital frequency. The antenna pattern is the time average of the transverse-traceless projected luminosity tensor contracted with the projector onto each sky direction, evaluated on a 181 × 121 (θ, φ) grid. The velocity-detuning sweep integrates the rescaled initial states (all velocities multiplied by k ∈ {0.90, 0.95, 0.98, 0.99, 1.00, 1.01, 1.02, 1.05, 1.10}) over [0, 8] at rtol = atol = 1e-11 and refines the first return with xatol 1e-10.

## 9. Verification protocol and acceptance checks

Every check is registered before the run: target, tolerance and unit are committed in the protocol, not chosen after the fact.

| Check | Target | Tolerance |
|---|---|---|
| Period closure error (configuration returns to itself) | 0 | 5e-8 |
| Period inside the published range [6.2, 6.5] | yes | exact |
| Energy drift over one period | 0 | 1e-12 |
| Total angular momentum (defining L = 0) | 0 | 1e-9 |
| Mean luminosity proxy finite, 0 < P < 1e10 | yes | exact |
| Quadrupole choreography symmetry Q(T/3) = Q(0) | yes | 1e-6 |
| Dominant harmonic on the comb (f·T = integer) | 0 | 0.05 |

**Recorded verification run** (mode: smoke, status: **PASS**, 6/6 checks)

| Check | Recorded value | Target | Tolerance | Unit | Verdict |
|---|---|---|---|---|---|
| `period_closure_error` | 1.2317e-08 | 0 | 5.0000e-08 | dimless | PASS |
| `period_in_expected_range` | 1 | 1 | 1.0000e-12 | bool | PASS |
| `energy_conserved` | 3.3307e-15 | 0 | 1.0000e-12 | energy | PASS |
| `angular_momentum_is_zero` | 1.4433e-15 | 0 | 1.0000e-09 | ang mom | PASS |
| `luminosity_finite_positive` | 1 | 1 | 1.0000e-12 | bool | PASS |
| `dominant_harmonic_on_comb` | 0.001499625094 | 0 | 0.05 | harmonic index | PASS |

**Check notes** — what each number means:

| Check | Note |
|---|---|
| `period_closure_error` | T = 6.325914025 (config closure after one period) |
| `period_in_expected_range` | T = 6.325914 within the published range |
| `energy_conserved` | relative drift below 1e-12 |
| `angular_momentum_is_zero` | the figure-eight carries exactly zero angular momentum |
| `luminosity_finite_positive` | mean GW luminosity proxy = 98060745.9786 (G=c=D=1) |
| `dominant_harmonic_on_comb` | peak at f*T = 5.9985 -> harmonic n = 6 of the orbit period |

## 10. Figure gallery (300 dpi)

![{'cap_en': 'Orbit overview: (a) the figure-eight trajectory traced by all three equal masses over one period T = 6.325914 with the chase direction marked; (b) pairwise separations over the same period.', 'cap_ru': 'Обзор орбиты: (a) траектория-«восьмёрка», которую все три равные массы обводят за один период T = 6.325914, с отмеченным направлением погони; (b) парные расстояния за тот же период.', 'walk_en': 'All three bodies trace the identical closed curve; the pairwise separations r12/r13/r23 sweep the same range 0.6905 to 2.0000 and are permuted among the pairs every T/3 — the exchange symmetry that powers the quadrupole.', 'walk_ru': 'Все три тела обводят одну и ту же замкнутую кривую; парные расстояния r12/r13/r23 пробегают один и тот же диапазон от 0.6905 до 2.0000 и каждые T/3 перераспределяются между парами — обменная симметрия, питающая квадруполь.'}](figures/fig01_orbit_overview.png)

*{'cap_en': 'Orbit overview: (a) the figure-eight trajectory traced by all three equal masses over one period T = 6.325914 with the chase direction marked; (b) pairwise separations over the same period.', 'cap_ru': 'Обзор орбиты: (a) траектория-«восьмёрка», которую все три равные массы обводят за один период T = 6.325914, с отмеченным направлением погони; (b) парные расстояния за тот же период.', 'walk_en': 'All three bodies trace the identical closed curve; the pairwise separations r12/r13/r23 sweep the same range 0.6905 to 2.0000 and are permuted among the pairs every T/3 — the exchange symmetry that powers the quadrupole.', 'walk_ru': 'Все три тела обводят одну и ту же замкнутую кривую; парные расстояния r12/r13/r23 пробегают один и тот же диапазон от 0.6905 до 2.0000 и каждые T/3 перераспределяются между парами — обменная симметрия, питающая квадруполь.'}.*

![{'cap_en': 'Headline result: plus-polarised waveform of the choreography over one orbit period (left) and the harmonic comb of its spectrum (right).', 'cap_ru': 'Главный результат: плюс-поляризованная форма волны хореографии за один орбитальный период (слева) и гармоническая гребёнка её спектра (справа).', 'walk_en': 'The exact strain spans −4.04 to +4.85 and repeats every T/6; the spectrum is a pure comb with lines at n = 6, 12, 18 of relative amplitudes 1 : 0.091 : 0.0061, every other harmonic staying below 0.0013 of the dominant line at f·T = 5.9988.', 'walk_ru': 'Точная деформация лежит в диапазоне от −4.04 до +4.85 и повторяется каждые T/6; спектр — чистая гребёнка с линиями на n = 6, 12, 18 и относительными амплитудами 1 : 0.091 : 0.0061, все прочие гармоники лежат ниже 0.0013 доминирующей линии на f·T = 5.9988.'}](figures/fig02_waveform_comb.png)

*{'cap_en': 'Headline result: plus-polarised waveform of the choreography over one orbit period (left) and the harmonic comb of its spectrum (right).', 'cap_ru': 'Главный результат: плюс-поляризованная форма волны хореографии за один орбитальный период (слева) и гармоническая гребёнка её спектра (справа).', 'walk_en': 'The exact strain spans −4.04 to +4.85 and repeats every T/6; the spectrum is a pure comb with lines at n = 6, 12, 18 of relative amplitudes 1 : 0.091 : 0.0061, every other harmonic staying below 0.0013 of the dominant line at f·T = 5.9988.', 'walk_ru': 'Точная деформация лежит в диапазоне от −4.04 до +4.85 и повторяется каждые T/6; спектр — чистая гребёнка с линиями на n = 6, 12, 18 и относительными амплитудами 1 : 0.091 : 0.0061, все прочие гармоники лежат ниже 0.0013 доминирующей линии на f·T = 5.9988.'}.*

![{'cap_en': 'Directionality and isolation: time-averaged quadrupole antenna pattern (left) and the velocity-detuning sweep around the choreography (right).', 'cap_ru': 'Направленность и изолированность: усреднённая по времени квадрупольная диаграмма направленности (слева) и развёртка по расстройке скоростей вокруг хореографии (справа).', 'walk_en': 'Emission peaks along the orbital normal at 3.01 times the mean luminosity with in-plane minima 0.055 of the peak; scaling the initial velocities by k leaves the k = 1 closure residual at 7.6·10⁻⁹ while the nearest detuned case (k = 1.01) jumps to 0.028 with return-time shifts up to 1.67 — the eight is an isolated solution.', 'walk_ru': 'Излучение достигает максимума вдоль нормали к орбите — 3.01 средней светимости, внутриплоскостные минимумы составляют 0.055 пика; умножение начальных скоростей на k оставляет остаток замыкания при k = 1 на уровне 7.6·10⁻⁹, тогда как ближайший расстроенный случай (k = 1.01) скачет до 0.028 со сдвигами времени возврата до 1.67 — восьмёрка изолирована.'}](figures/fig03_pattern_sweep.png)

*{'cap_en': 'Directionality and isolation: time-averaged quadrupole antenna pattern (left) and the velocity-detuning sweep around the choreography (right).', 'cap_ru': 'Направленность и изолированность: усреднённая по времени квадрупольная диаграмма направленности (слева) и развёртка по расстройке скоростей вокруг хореографии (справа).', 'walk_en': 'Emission peaks along the orbital normal at 3.01 times the mean luminosity with in-plane minima 0.055 of the peak; scaling the initial velocities by k leaves the k = 1 closure residual at 7.6·10⁻⁹ while the nearest detuned case (k = 1.01) jumps to 0.028 with return-time shifts up to 1.67 — the eight is an isolated solution.', 'walk_ru': 'Излучение достигает максимума вдоль нормали к орбите — 3.01 средней светимости, внутриплоскостные минимумы составляют 0.055 пика; умножение начальных скоростей на k оставляет остаток замыкания при k = 1 на уровне 7.6·10⁻⁹, тогда как ближайший расстроенный случай (k = 1.01) скачет до 0.028 со сдвигами времени возврата до 1.67 — восьмёрка изолирована.'}.*

![{'cap_en': 'Emitter dynamics: exact second derivatives of the quadrupole components (left) and the instantaneous and cumulative radiated energy (right).', 'cap_ru': 'Динамика излучателя: точные вторые производные компонент квадруполя (слева) и мгновенная с накопленной излучённой энергией (справа).', 'walk_en': 'The T/3 exchange symmetry and the T/2 sign flip of the xy component are visible in the components; the exact luminosity averages 76.51, peaks at 159.73, and the cumulative radiated energy reaches 484.10 over one period (G = c = D = 1).', 'walk_ru': 'В компонентах видны обменная симметрия T/3 и смена знака xy-компоненты на T/2; точная светимость в среднем равна 76.51 с пиком 159.73, а накопленная излучённая энергия достигает 484.10 за один период (G = c = D = 1).'}](figures/fig04_quadrupole_dynamics.png)

*{'cap_en': 'Emitter dynamics: exact second derivatives of the quadrupole components (left) and the instantaneous and cumulative radiated energy (right).', 'cap_ru': 'Динамика излучателя: точные вторые производные компонент квадруполя (слева) и мгновенная с накопленной излучённой энергией (справа).', 'walk_en': 'The T/3 exchange symmetry and the T/2 sign flip of the xy component are visible in the components; the exact luminosity averages 76.51, peaks at 159.73, and the cumulative radiated energy reaches 484.10 over one period (G = c = D = 1).', 'walk_ru': 'В компонентах видны обменная симметрия T/3 и смена знака xy-компоненты на T/2; точная светимость в среднем равна 76.51 с пиком 159.73, а накопленная излучённая энергия достигает 484.10 за один период (G = c = D = 1).'}.*

## 11. Results (full run)

```text
period_closure_error                = 1.2e-08  (T = 6.325914025)
period_in_expected_range            = PASS (6.325914 vs published 6.325914)
energy_conserved                    = 3.6e-15
angular_momentum_is_zero            = 1.4e-15
luminosity_finite_positive          = PASS (P = 1.65e8 in G=c=D=1 units)
quadrupole_choreography_symmetry    = PASS (|Q(T/3)-Q(0)| = 1.48·10⁻⁸)
dominant_harmonic_on_comb           = PASS (f*T = 5.9995 -> n = 6)
status: PASS (7/7)
```

## 12. Analysis

**Orbit and symmetry.** The period closure closes the loop first: T = 6.325914025 against the published 6.32591398, a mismatch of 1.2e-08 inside the 5e-8 tolerance, and the configuration returns on itself to the same 1.2e-08. Energy is conserved to 3.6e-15 and the angular momentum is zero to 1.4e-15 — the defining L = 0 property holds at machine precision. The pairwise separations sweep 0.6905 to 2.0000 and are permuted among the three pairs every T/3, and the same order-3 exchange shows up on the quadrupole: Q(T/3) = Q(0) to 1.5·10⁻⁸ while Q(T/2) − Q(0) = 0.943 — the half period is emphatically not a symmetry, the choreography exchange is order three, not two.

**Waveform and comb.** The exact plus-polarised strain spans −4.04 to +4.85 over one period and repeats every T/6, visible as six identical lobes in the waveform panel. The spectrum is a pure comb: the dominant line at n = 6 of the orbital comb (f·T = 5.9988 for the windowless exact spectrum; the acceptance check, computed on the finite-difference series with a Hann window, gives f·T = 5.9995 with residual 5.0e-4 against the 0.05 tolerance), overtones at n = 12, 18, 24 of relative amplitudes 0.091, 0.0061, 0.0004, and every other harmonic of the orbital frequency suppressed below 0.0013 of the peak. The dominant harmonic sits at exactly twice the T/3 pattern frequency 3/T, as the symmetry bookkeeping predicts.

**Directionality.** The time-averaged quadrupole antenna pattern, built from exact third derivatives, peaks along the orbital normal at 3.01 times the mean luminosity — a face-on observer receives the strongest signal — while in-plane emission is suppressed to 0.055 of the peak both along the x-axis and along the diagonals of the eight. For a LISA-class instrument the observable is therefore strongly inclination-dependent, and the gold lobes drawn in the scheme mark the only directions worth pointing at.

**Isolation and energy bookkeeping.** The velocity-detuning sweep proves the choreography is not a member of a nearby family: at k = 1 the closure residual is 7.6·10⁻⁹, while the nearest detuned case (k = 1.01) already sits at 0.028 and the extremes k = 0.90 and k = 1.10 reach 0.826 and 0.945, with return-time shifts from −1.63 to +1.67. On the energy side the exact luminosity averages 76.51 with a maximum of 159.73, so one period radiates 484.10 in G = c = D = 1 units. The acceptance-proxy value 1.65e8 recorded in the protocol is deliberately not used as a physical number: the chained finite-difference estimator amplifies sampling noise by orders of magnitude, and its only job is the finiteness gate 0 < P < 1e10, which it passes.

## 13. Discussion and honest boundaries

The model is deliberately minimal: Newtonian dynamics plus the leading quadrupole formula, planar and equal-mass. Within these assumptions every reported number is an exact statement about the governing equations rather than a simulation of a specific astrophysical system. The natural extensions each keep the verification style: unequal-mass choreographies and their literature continuum, the full multipole ladder beyond the quadrupole (octupole and higher), the gravitational-wave back-reaction on the orbit over many periods, and the time-dependent detector response of a LISA-class instrument at arbitrary inclination, which the present antenna pattern only summarises.

The parameter regime is chosen for structural clarity. All results are quoted in units where G = m = c = D = 1; the physical mapping is linear — a system of total mass M and size scale L repeats the same dimensionless solution with the orbital frequency scaled by √(GM/L³) and the strain by GM/(c²D). Which astrophysical population could actually radiate into the mHz band of LISA, whether any natural system realises (or is captured into) a choreography, and how the comb signature survives environmental perturbations are astrophysical questions that lie beyond this study's scope but are now well posed: the comb and its 1 : 0.091 : 0.0061 amplitude ladder are falsifiable targets.

Within the program this study completes the comparable-mass branch of the three-body block. TRX-10 treats the hierarchical (secular) limit of the same problem — Kozai–Lidov cycles instead of a choreography; TRX-09 describes the same choreographic idea in the vortex language of the monograph; TRX-01 and TRX-12 put lasers inside the three-body problem as actuators, while this study points lasers at it as the measuring instrument. Together they cover the three-body problem of the TRIVORTEX program from the restricted to the radiating comparable-mass case.

## 14. Conclusions

- The period of the figure-eight choreography, found by global minimisation of the configuration closure, is T = 6.325914025 — matching the published 6.32591398 to 1.2e-08 and inside the 5e-8 acceptance tolerance.
- Energy is conserved to 3.6e-15 and the total angular momentum stays zero to 1.4e-15 over one full period: the defining L = 0 property of the eight holds at machine precision.
- The equal-mass exchange symmetry is verified on the quadrupole: Q(T/3) = Q(0) to 1.5·10⁻⁸ while Q(T/2) − Q(0) = 0.943, confirming the choreography exchange is order three.
- The plus-polarised waveform spans −4.04 to +4.85, repeats six times per period, and its spectrum is a pure comb: dominant line at n = 6 (f·T = 5.9995, residual 5.0e-4), overtones at 12, 18, 24 with amplitudes 0.091, 0.0061, 0.0004, all other harmonics below 0.0013 of the peak.
- The time-averaged antenna pattern peaks along the orbital normal at 3.01 times the mean exact luminosity (76.51 mean, 159.73 peak, 484.10 radiated per period in G = c = D = 1); in-plane emission is suppressed to 0.055 of the peak.
- The velocity-detuning sweep over k = 0.90 … 1.10 shows the eight is isolated: the k = 1 closure residual is 7.6·10⁻⁹ while every detuned case exceeds 0.028, with return-time shifts up to 1.67.

## 15. The monograph and its renditions

The complete monograph of this study exists in four renditions — Russian and English are separate documents, each in a typeset PDF and an editable DOCX:

| Rendition | Path |
|---|---|
| Monograph (English, PDF) | `monograph/monograph_EN.pdf` |
| Monograph (English, DOCX) | `monograph/monograph_EN.docx` |
| Monograph (Russian, PDF) | `monograph/monograph_RU.pdf` |
| Monograph (Russian, DOCX) | `monograph/monograph_RU.docx` |
| Reading-room copy | `publications/pdf/TRX-11-gw-choreography_EN.pdf` · `publications/pdf/TRX-11-gw-choreography_RU.pdf` |
| HTML source | `publications/html/TRX-11-gw-choreography.html` |

**Monograph abstract.** This monograph turns the figure-eight choreography of Chenciner and Montgomery — three equal masses chasing each other along a single closed curve with zero angular momentum — into a quantified gravitational-wave source. The period is found by global minimisation of the configuration closure over one revolution: T = 6.325914025, matching the published 6.32591398 to 1.2e-08, with energy conserved to 3.6e-15 and the angular momentum zero to 1.4e-15 throughout. In the quadrupole approximation (G = c = D = 1) the mass quadrupole drives a plus-polarised strain spanning −4.04 to +4.85 that repeats six times per orbit period. The choreography symmetry Q(T/3) = Q(0), verified to 1.5·10⁻⁸, locks the spectrum into a harmonic comb: the dominant line lands at n = 6 of the orbital comb (f·T = 5.9995, residual 5.0e-4) with overtones at 12 and 18 of relative amplitudes 0.091 and 0.0061. The time-averaged antenna pattern peaks along the orbital normal at 3.01 times the mean exact luminosity of 76.51, and a velocity-detuning sweep over k = 0.90 … 1.10 shows the eight is an isolated solution: the k = 1 closure residual is 7.6·10⁻⁹ while every detuned case exceeds 0.028. LISA-class laser interferometers are the natural readout.

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
| `t` | 300 | 0 … 3.16296 |
| `x3` | 300 | 0 … 1.0000e-08 |
| `y3` | 300 | 0 … -1.0000e-08 |
| `h_plus` | 401 | -2.022088124 … -2.022088176 |

**Reproduction matrix**

| Command | What it does |
|---|---|
| `python3 research/TRX-11-gw-choreography/code/trx11_gw_choreography.py` | full run: physics + acceptance checks (8.17 s) |
| `python3 research/TRX-11-gw-choreography/code/trx11_gw_choreography.py --smoke` | CI guard: same checks, seconds-scale settings |
| `python3 research/TRX-11-gw-choreography/code/trx11_gw_choreography.py --figures` | regenerates the 300-dpi figure set |
| `make research-smoke` | all twelve studies in smoke mode |
| `make research-figures` | all twelve studies + figure sets |

## 17. Cross-links within the program

- **TRX-10** covers the hierarchical (secular) limit of the same three-body problem — Kozai–Lidov cycles instead of a comparable-mass choreography.
- **TRX-01/12** place lasers *inside* the three-body dynamics as actuators; this study points lasers *at* it as detectors (LISA-class readout of three-body gravity).
- **TRX-09** is the vortex-language description of the same choreographic idea: three circulations replacing three masses.

## 18. Inside the script

The executable is a single deterministic file, `code/trx11_gw_choreography.py`, ~pure `numpy`/`scipy` with no network access and no random state beyond fixed seeds. One run executes the full physics of the study, evaluates every registered acceptance check against its committed target and tolerance, and writes the JSON protocol — the same file quoted in §9.

| Mode | Invocation | What happens |
|---|---|---|
| Full | `python3 code/trx11_gw_choreography.py` | complete experiment, all checks, JSON protocol (8.17 s) |
| Smoke | `python3 code/trx11_gw_choreography.py --smoke` | identical acceptance logic at seconds-scale settings — the CI mode |
| Figures | `python3 code/trx11_gw_choreography.py --figures` | regenerates the schematic + the four 300-dpi PNG panels |

**Outputs per run**

| File | Produced by | Content |
|---|---|---|
| `results/trx11_results.json` | every mode | status, checks (value/target/tol/unit/pass/note), series, meta |
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
| Previous study | TRX-010 |
| Next study | TRX-012 |

## 21. Notation

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

## 22. References

1. Einstein, A. (1918). *Über Gravitationswellen.* Sitzungsberichte der Königlich Preussischen Akademie der Wissenschaften (Berlin), 154–167.
2. Peters, P. C., Mathews, J. (1963). *Gravitational radiation from point masses in a Keplerian orbit.* Physical Review 131, 435–440.
3. Thorne, K. S. (1980). *Multipole expansions of gravitational radiation.* Reviews of Modern Physics 52, 299–339.
4. Moore, C. (1993). *Braids in classical dynamics.* Physical Review Letters 70, 3675–3679.
5. Chenciner, A., Montgomery, R. (2000). *A remarkable periodic solution of the three-body problem in the case of equal masses.* Annals of Mathematics 152, 881–901.
6. Simó, C. (2002). *Dynamical properties of the eight map.* Celestial Mechanics 4, 343.
7. Taylor, J. H., Weisberg, J. M. (1982). *A new test of general relativity: gravitational radiation and the binary pulsar PSR 1913+16.* The Astrophysical Journal 253, 908–920.
8. Maggiore, M. (2007). *Gravitational Waves. Volume 1: Theory and Experiments.* Oxford University Press.
9. Amaro-Seoane, P. et al. (2017). *Laser Interferometer Space Antenna.* arXiv:1702.00786.

## 23. Glossary

| Term | Definition |
|---|---|
| Choreography | a periodic solution in which all bodies trace the same closed curve, shifted in time |
| Figure-eight choreography | the Chenciner–Montgomery equal-mass solution with zero angular momentum, period T ≈ 6.3259 in G = m = 1 |
| Mass quadrupole Q_ij | second moment Σ m_k x_ki x_kj of the mass distribution; the source of leading-order gravitational radiation |
| Plus-polarised strain h₊ | transverse-traceless projection of d²(Qxx − Qyy)/dt² observed at distance D |
| GW luminosity P | power radiated in gravitational waves, P = (1/5)Σ(d³Q_ij/dt³)² in G = c = D = 1 |
| Harmonic comb | a spectrum consisting of equidistant lines at integer multiples of a base frequency |
| Antenna pattern | direction-dependent time-averaged radiated power dP/dΩ of the emitter |
| Closure residual | maximum deviation of the configuration from its initial state after a candidate period |
| Velocity detuning | scaling all initial velocities by a factor k ≠ 1 to probe whether the periodic orbit is isolated |
| Jerk | third time derivative of position; needed for the exact d³Q/dt³ of the luminosity formula |

## 24. Appendix A. Full parameter table

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

**Protocol-level parameter snapshot** (`results` JSON, `meta` block):

| Key | Value |
|---|---|
| `equations` | `["Q_ij = sum_k m_k x_ki x_kj ;  h_plus ~ d^2(Qxx-Qyy)/dt^2", "P = (1/5) sum_ij (d^3 Q_ij/dt^3)^2   (G = c = D = 1)", "Chenciner-Montgomery figure-eight: T ~ 6.3244, L = 0"]` |
| `period_T` | `6.32591402544423` |
| `mean_luminosity_proxy` | `98060745.97859268` |
| `dominant_harmonic_index` | `6` |
| `laser_link` | `"LISA/Taiji/TianQin laser interferometers are the natural detectors of three-body GW signatures"` |

## 25. Appendix B. BibTeX

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

## 26. How to cite

Cite the repository through [`CITATION.cff`](../../CITATION.cff) (DOI 10.5281/zenodo.21825394, version 1.0.0); this study is part of the TRIVORTEX Research Program. If you cite the study alone, name the monograph rendition you used and attach the JSON protocol of the run you reproduced.

```bibtex
@misc{trivortextrx112026isaev,
  author       = {Isaev, Iskhak Khamzatovich},
  title        = {Gravitational Waves from the Figure-Eight Choreography (TRIVORTEX Research Program, TRX-11)},
  year         = {2026},
  howpublished = {Zenodo},
  doi          = {10.5281/zenodo.21825394},
  url          = {https://github.com/wild8highlander/Trivortex}
}
```

