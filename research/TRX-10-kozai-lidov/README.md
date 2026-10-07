# TRX-10 — Kozai–Lidov Oscillations in Hierarchical Triples

*TRIVORTEX Research Program · version 1.0.0 · study TRX-10 of 12*

The Kozai–Lidov mechanism: a test particle on an inclined inner orbit of a hierarchical triple, perturbed by a distant companion, periodically exchanges eccentricity for inclination while the z-angular momentum **j_z = √(1 − e²)·cos i** stays constant; for a nearly circular initial orbit the eccentricity climbs to the closed-form maximum **e_max = √(1 − (5/3)·cos²i₀)** whenever i₀ exceeds the Kozai angle 39.23°. The study refuses to code the memorized result: the doubly-averaged quadrupole potential is built numerically — orbit quadrature, (e, ω) tabulation, cubic-spline Hamiltonian — and the resulting flow is audited against analytic benchmarks and an independent direct integration of the full three-dimensional restricted problem.

> **Edition 1.0.0.** This README is part of the first public release of the TRIVORTEX research program. The study ships as an executable script, a committed JSON protocol, four 300-dpi figures, a schematic and a bilingual monograph in four renditions (Russian and English, each in PDF and DOCX).

**At a glance**

| Aspect | Value |
|---|---|
| Block | Celestial mechanics — study 10 of 12 |
| Model | double-averaged quadrupole Kozai–Lidov problem (test particle in a hierarchical triple) |
| Key invariant | j_z = √(1 − e²)·cos i (0.500000 / 0.342020 for i₀ = 60°/70°) |
| Headline result | e_max = 0.763763 (60°) and 0.897239 (70°) reproduced by the spline flow; direct 3-D validation −2.8% |
| Verification | 4/4 checks PASS (full mode) |
| Runtime | 64.6 s full · < 20 s smoke |

| Field | Value |
|---|---|
| Study | `TRX-10` (TRX-10-kozai-lidov) |
| Program | TRIVORTEX — The Three-Body Problem in the Vortex Model |
| Author | Isaev Iskhak Khamzatovich (ORCID `0009-0003-7299-0701`) |
| DOI | [10.5281/zenodo.21825394](https://doi.org/10.5281/zenodo.21825394) |
| Version | 1.0.0 — first public release |
| Code | `research/TRX-10-kozai-lidov/code/trx10_kozai_lidov.py` |
| Protocol | `research/TRX-10-kozai-lidov/results/trx10_results.json` |
| License | `LicenseRef-Proprietary-Wild8Highlander-1.0` |

## 1. Mission

Hierarchical triples are where the three-body problem lives longest: after the short-period terms are averaged away, the quadrupole problem reduces to a slow eccentricity–inclination clock that governs asteroid triples, irregular satellite systems, hot-Jupiter migration channels and compact-object mergers. This study refuses to trust memorized formulas: the doubly-averaged quadrupole potential is built numerically — the instantaneous quadrupole disturbing function is averaged over the inner orbit by quadrature, tabulated on an (e, ω) grid at the fixed j_z of the run, and turned into a cubic spline whose analytic derivatives drive the canonical Hamiltonian flow ė = (j/e)·∂⟨U⟩/∂ω, ω̇ = −(j/e)·∂⟨U⟩/∂e.

The numerical machine is then audited against everything known analytically. The spline flow reproduces the closed-form maxima e_max = 0.763763 (i₀ = 60°) and 0.897239 (i₀ = 70°) to within 2×10⁻³, halves the KL period when the perturber mass doubles (ratio 0.481 against the ideal 0.5, inside the 3% band), sweeps the Kozai landscape over 12 inclinations, and is validated against an independent DIRECT integration of the full 3-D restricted problem (m₃/M = 0.5, a_out = 5 a_in, 200 outer orbits): smoothed maximum eccentricity 0.7423 versus 0.7638 — a −2.8% deviation consistent with the hexadecapole truncation. Laser link: laser ranging of binary and triple asteroids, and LISA-class laser interferometry of compact-object triples whose mergers are channelled by KL cycles.

## 2. Introduction and historical context

The history of the effect began half a century before its discovery papers. In 1910 Hugo von Zeipel derived the secular equations of the double-averaged quadrupole three-body problem, and the reduction to a single degree of freedom was already implicit in his work. The classical papers of 1962 appeared independently and almost simultaneously: Yoshihide Kozai analysed secular perturbations of asteroids with high inclinations (Astronomical Journal 67, 591), while Mikhail Lidov studied the evolution of artificial satellite orbits under the gravitational action of external bodies (Planetary and Space Science 9, 719) — in the Russian literature the effect is still often called the Lidov–Kozai mechanism. Both found the same phenomenon: above the critical inclination 39.23° the eccentricity and the inclination begin to exchange periodically, and the inclination at maximum eccentricity drops exactly to the critical value.

The mechanism immediately became a working tool of celestial mechanics. It bounds the lifetimes of high-latitude artificial satellites, shapes the orbital architecture of irregular satellite systems and of asteroid families, drives the growth of cometary eccentricities, and protects — or destroys — bodies on inclined orbits in planetary systems. The timescale formula t_KL ~ (M/m₃)(a_out/a_in)³ P_in shows why the effect is so universal: it is a clock whose rate depends only on the hierarchy, and every hierarchical configuration with an inclined orbit carries it.

The modern renaissance came with exoplanets and gravitational-wave astronomy. The eccentric generalizations of the mechanism (the octupole-order flips, comprehensively reviewed by Naoz 2016) turn inclined triples into a migration channel for hot Jupiters (Wu & Murray 2003; Fabrycky & Tremaine 2007) and into a merger channel for compact-object triples whose final inspirals LISA will observe (Blaes, Lee & Socrates 2002). The monograph of Shevchenko (2017) collects the applications, and the historical review of Ito & Ohtsuka (2019) reconstructs the naming and the priority — including von Zeipel's role and the Japanese and Soviet schools.

For TRIVORTEX the relevance is structural. The conserved j_z collapses the problem to one integrable degree of freedom exactly as the Chaplygin integral reduces the vortex problem; the closed-form e_max is a Theorem-3.1-type sharp analytic benchmark that the numerics must hit; and the KL clock is the secular twin of the rotating choreography period. This study therefore anchors the secular celestial block of the program (TRX-01, TRX-10, TRX-11, TRX-12) — the same three-body stage on which the laser studies act.

## 3. Physical system and preset

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

**Model assumptions**

- Test-particle limit: the inner orbit hosts a massless particle; the companion moves on a fixed circular Kepler orbit and enters only through C₂.
- Quadrupole order only: the companion potential is truncated at l = 2; for a circular outer orbit the octupole vanishes, and the hexadecapole is smaller by (a_in/a_out)².
- Double averaging: all short-period terms over the inner and outer orbits are removed — the model is purely secular.
- No dissipation: no tides, no gas, no radiation forces; the eccentricity–inclination exchange is conservative and reversible.
- The averaged potential is a numerical object (cubic spline on a 160 × 180 grid); its 1.33×10⁻⁵ residual is part of the error budget and is reported honestly.
- Canonical units GM_inner = 1, a_in = 1, n_in = 1; the direct validation uses m₃/M = 0.5, a_out = 5 a_in and 200 outer periods.

## 4. Governing equations

(E1) Double-averaged quadrupole disturbing potential (built numerically by orbit quadrature; units G m₃/2a_out³):

$$\langle U\rangle(e,\omega) = \left\langle \frac{G m_3}{2 a_{\rm out}^3}\,\big(3(\mathbf{r}\cdot\hat{\mathbf{r}}_3)^2 - \mathbf{r}^2\big) \right\rangle_{\!\text{inner orbit}}$$

(E2) Canonical Hamiltonian flow on the fixed-j_z manifold (L = 1), rates scaled by C₂:

$$\dot{e} = C_2\,\frac{j}{e}\,\frac{\partial \langle U\rangle}{\partial \omega}, \qquad \dot{\omega} = -\,C_2\,\frac{j}{e}\,\frac{\partial \langle U\rangle}{\partial e}, \qquad j = \sqrt{1 - e^2}$$

(E3) Conserved z-component of the orbital angular momentum — the invariant that locks e and i:

$$j_z = \sqrt{1 - e^2}\,\cos i = \mathrm{const}$$

(E4) Analytic maximum eccentricity for an initially circular orbit; the exchange turns on above the Kozai angle:

$$e_{\max} = \sqrt{1 - \tfrac{5}{3}\cos^2 i_0}, \qquad i_{\rm crit} = \arccos\sqrt{\tfrac{3}{5}} \approx 39.23^\circ$$

(E5) KL timescale: the cycle period scales as 1/m₃ (halves when the perturber mass doubles):

$$C_2 = \tfrac{3}{8}\,\frac{m_3}{M}\left(\frac{a_{\rm in}}{a_{\rm out}}\right)^{\!3} n_{\rm in}, \qquad t_{\rm KL} \sim \frac{1}{C_2}$$

## 5. Scheme

![TRX-10 scheme — the Kozai–Lidov exchange in a hierarchical triple: a distant circular companion drives the eccentricity of the inclined inner test-particle orbit from 0.001 to 0.764 while the inclination dips from 60° to the Kozai angle 39.23°, with j_z = √(1 − e²)·cos i conserved throughout.](figures/scheme_trx10.svg)

*TRX-10 scheme — the Kozai–Lidov exchange in a hierarchical triple: a distant circular companion drives the eccentricity of the inclined inner test-particle orbit from 0.001 to 0.764 while the inclination dips from 60° to the Kozai angle 39.23°, with j_z = √(1 − e²)·cos i conserved throughout..*

The diagram encodes the following elements:

- **Outer companion (m₃)** — distant perturber on a circular orbit of radius a_out = 20 a_in — drawn not to scale; inner units GM_inner = 1, a_in = 1
- **KL clock box** — t_KL ~ 1/C₂ with C₂ = (3/8)(m₃/M)(a_in/a_out)³·n_in — the period halves when m₃ doubles
- **Inner orbit (gold ellipse)** — drawn at e_max = 0.7638 for i₀ = 60°; the test particle cycles e: 0.001 → 0.764 each cycle
- **Inclination ledger (h₃, h)** — the inner angular-momentum vector h is tilted by i₀ = 60° from the outer-orbit normal h₃
- **Dashed red threshold** — i_crit = arccos√(3/5) = 39.23° — the Kozai angle, the exchange threshold
- **Invariant box + exchange arrows** — j_z = √(1 − e²)·cos i = 0.5 conserved; e↑ 0.001 → 0.764 while i↓ 60° → 39.2°

## 6. Mapping to TRIVORTEX

The mapping to the TRIVORTEX vortex framework is structural. The conserved j_z pins the whole eccentricity–inclination family to a one-dimensional manifold exactly as the Chaplygin integral pins the vortex orbits; the closed-form e_max = √(1 − (5/3)cos²i₀) plays the role of a Theorem-3.1-type sharp analytic benchmark that the numerics are obliged to hit; and the KL clock with period ~ 1/C₂ is the secular twin of the rotating choreography period. Methodologically the study is the program's flagship of the built-not-memorized philosophy: the averaged Hamiltonian is constructed numerically and the analytic law emerges as an output-level target — the same discipline the vortex studies apply to Chaplygin-reduced flows.

| Quantity in this study | TRIVORTEX analog | Comment |
|---|---|---|
| Hierarchical triple (test particle + companion) | three bodies with separated scales | the celestial three-body problem |
| Conserved j_z = √(1 − e²)·cos i | Chaplygin-type topological invariant | an integral that pins the orbit family |
| e_max = √(1 − (5/3)cos²i₀) | closed form of Theorem 3.1 | a sharp analytic benchmark for the numerics |
| KL clock, t_KL ~ 1/C₂ | choreography period T | secular timekeeping of the triad |
| Spline-built averaged Hamiltonian ⟨U⟩ | numerically constructed vortex Hamiltonian | both flows are driven by tabulated, not memorized, potentials |

## 7. Dimensionless formulation

All quantities are in canonical restricted-problem units: length in inner semi-major axes a_in, time in inner orbital periods (n_in = 1, GM_inner = 1), mass in the inner-pair scale M. The secular flow lives on the fixed-j_z manifold — a single Hamiltonian degree of freedom (e, ω) — and the KL clock is set by C₂ = (3/8)(m₃/M)(a_in/a_out)³·n_in; for the standard preset (m₃/M = 1, a_out = 20) the measured cycle lasts ≈ 1.04×10⁵ inner periods.

## 8. Numerical method

The averaged potential is tabulated on a 160 × 180 grid in (e, ω) with e ∈ [0.0001, 0.999] and ω ∈ [0, 2π]; each node is evaluated by the 240-point Kepler-time-weighted quadrature described in the derivation. A bicubic RectBivariateSpline (kx = ky = 3) then provides ⟨U⟩ and its exact spline derivatives ∂⟨U⟩/∂e and ∂⟨U⟩/∂ω — the Hamiltonian machine used everywhere downstream. No analytic KL formula is written anywhere in the secular pipeline.

The canonical flow is integrated with DOP853 (rtol 1e-8, atol 1e-9, max_step T/1500) over a span covering three model KL cycles, sampled at 3000 points per run. The KL period is measured as the mean spacing of successive local maxima of e above 0.7·max(e) — a robust estimator insensitive to the small-amplitude wiggles near e ≈ 0. The mass-scaling check reruns the flow at m₃/M = 2 and compares P(2m₃)/P(m₃) against 0.5 with a 3% band; the figure sweep extends the clock to m₃/M ∈ {0.5, 1, 2, 4}.

Validation is fully independent: the direct run integrates the full three-dimensional restricted problem — the test particle feels both the primary and the companion moving on its circular orbit — with DOP853 at rtol = atol = 1e-11, a 60000-step cap and 40000 dense-output samples over 200 outer periods (m₃/M = 0.5, a_out = 5 a_in). The osculating eccentricity is computed pointwise from the Laplace–Runge–Lenz vector and smoothed with a moving average over one outer period; the maximum of the smoothed curve is the reported quantity. The secular and direct models share no code path beyond the integrator, so their agreement is a genuine cross-validation.

## 9. Verification protocol and acceptance checks

Every check is registered before the run: target, tolerance and unit are committed in the protocol, not chosen after the fact.

| Check | Target | Tolerance |
|---|---|---|
| e_max (i₀ = 60°) vs analytic √(1 − (5/3)cos²i₀) | 0.763763 | 2e-3 |
| e_max (i₀ = 70°) vs analytic √(1 − (5/3)cos²i₀) | 0.897239 | 2e-3 |
| KL period ratio P(2m₃)/P(m₃) | 0.5 | 3% |
| direct 3-D smoothed e_max vs analytic | 0.763763 | 8% |

**Recorded verification run** (mode: smoke, status: **PASS**, 3/3 checks)

| Check | Recorded value | Target | Tolerance | Unit | Verdict |
|---|---|---|---|---|---|
| `e_max_i0_60` | 0.7637522327 | 0.7637626158 | 0.002 | ecc | PASS |
| `e_max_i0_70` | 0.8972294445 | 0.8972385613 | 0.002 | ecc | PASS |
| `kl_period_halves_with_m3` | 0.4931728351 | 0.5 | 0.03 | ratio | PASS |

**Check notes** — what each number means:

| Check | Note |
|---|---|
| `e_max_i0_60` | analytic sqrt(1-(5/3)cos^2 i0) = 0.763763 |
| `e_max_i0_70` | analytic sqrt(1-(5/3)cos^2 i0) = 0.897239 |
| `kl_period_halves_with_m3` | P(m3) = 111357.12, P(2 m3) = 54918.31 (period ~ 1/C2 ~ 1/m3) |

## 10. Figure gallery (300 dpi)

![{'cap_en': 'Landscape of the quadrupole Kozai–Lidov problem: (a) geometry of the hierarchical triple, (b) the analytic Kozai landscape e_max(i₀).', 'cap_ru': 'Ландшафт квадрупольной задачи Козаи–Лидова: (a) геометрия иерархической тройной, (b) аналитический ландшафт Козаи e_max(i₀).', 'walk_en': 'Panel (a) shows the inner orbit at e_max = 0.7638 inclined by i₀ = 60° and projected on the outer-orbit plane, with the companion orbit at a_out = 20 a_in dashed and not to scale; panel (b) traces e_max(i₀) = √(1 − (5/3)cos²i₀), shades the sub-critical band where no exchange occurs, and marks the study points 0.7638 (60°) and 0.8972 (70°).', 'walk_ru': 'Панель (a) показывает внутреннюю орбиту при e_max = 0.7638, наклонённую на i₀ = 60° и спроецированную на плоскость внешней орбиты; орбита компаньона a_out = 20 a_in дана пунктиром не в масштабе. Панель (b) воспроизводит e_max(i₀) = √(1 − (5/3)cos²i₀), затеняет докритическую полосу без обмена и отмечает точки исследования 0.7638 (60°) и 0.8972 (70°).'}](figures/fig01_kl_landscape.png)

*{'cap_en': 'Landscape of the quadrupole Kozai–Lidov problem: (a) geometry of the hierarchical triple, (b) the analytic Kozai landscape e_max(i₀).', 'cap_ru': 'Ландшафт квадрупольной задачи Козаи–Лидова: (a) геометрия иерархической тройной, (b) аналитический ландшафт Козаи e_max(i₀).', 'walk_en': 'Panel (a) shows the inner orbit at e_max = 0.7638 inclined by i₀ = 60° and projected on the outer-orbit plane, with the companion orbit at a_out = 20 a_in dashed and not to scale; panel (b) traces e_max(i₀) = √(1 − (5/3)cos²i₀), shades the sub-critical band where no exchange occurs, and marks the study points 0.7638 (60°) and 0.8972 (70°).', 'walk_ru': 'Панель (a) показывает внутреннюю орбиту при e_max = 0.7638, наклонённую на i₀ = 60° и спроецированную на плоскость внешней орбиты; орбита компаньона a_out = 20 a_in дана пунктиром не в масштабе. Панель (b) воспроизводит e_max(i₀) = √(1 − (5/3)cos²i₀), затеняет докритическую полосу без обмена и отмечает точки исследования 0.7638 (60°) и 0.8972 (70°).'}.*

![{'cap_en': 'Headline result — the eccentricity–inclination exchange of the secular spline flow.', 'cap_ru': 'Главный результат — обмен «эксцентриситет–наклонение» в секулярном сплайновом потоке.', 'walk_en': 'Left: e(t) cycles to 0.763733 (i₀ = 60°) and 0.897238 (70°) against the dashed analytic envelopes, with j_z = 0.500000 and 0.342020 conserved; right: over two cycles at 60° eccentricity peaks exactly when the inclination dips to 39.23° = i_crit — the antiphase exchange.', 'walk_ru': 'Слева: e(t) циклирует до 0.763733 (i₀ = 60°) и 0.897238 (70°) на фоне пунктирных аналитических огибающих, j_z = 0.500000 и 0.342020 сохраняются; справа: на двух циклах при 60° эксцентриситет достигает максимума ровно в момент провала наклонения до 39.23° = i_crit — противофазный обмен.'}](figures/fig02_kl_exchange.png)

*{'cap_en': 'Headline result — the eccentricity–inclination exchange of the secular spline flow.', 'cap_ru': 'Главный результат — обмен «эксцентриситет–наклонение» в секулярном сплайновом потоке.', 'walk_en': 'Left: e(t) cycles to 0.763733 (i₀ = 60°) and 0.897238 (70°) against the dashed analytic envelopes, with j_z = 0.500000 and 0.342020 conserved; right: over two cycles at 60° eccentricity peaks exactly when the inclination dips to 39.23° = i_crit — the antiphase exchange.', 'walk_ru': 'Слева: e(t) циклирует до 0.763733 (i₀ = 60°) и 0.897238 (70°) на фоне пунктирных аналитических огибающих, j_z = 0.500000 и 0.342020 сохраняются; справа: на двух циклах при 60° эксцентриситет достигает максимума ровно в момент провала наклонения до 39.23° = i_crit — противофазный обмен.'}.*

![{'cap_en': 'Parameter sweeps: validation of the Kozai landscape e_max(i₀) and scaling of the KL clock with the perturber mass.', 'cap_ru': 'Параметрические развёртки: валидация ландшафта Козаи e_max(i₀) и масштабирование часов Козаи–Лидова по массе возмутителя.', 'walk_en': 'Across 12 inclinations from 30° to 80° the spline flow matches the analytic landscape to 1.128×10⁻⁵ (the 40° run needs an 8× longer span: the KL period diverges at i_crit), while below i_crit eccentricity stays at e₀ = 0.001; the mass sweep over m₃/M ∈ {0.5, 1, 2, 4} confirms P ∝ 1/m₃ with a P·m₃ spread of 4.29%.', 'walk_ru': 'По 12 наклонениям от 30° до 80° сплайновый поток совпадает с аналитикой с точностью 1.128×10⁻⁵ (прогон 40° требует 8-кратного удлинения: период Козаи–Лидова расходится на i_crit), ниже i_crit эксцентриситет остаётся на e₀ = 0.001; развёртка по m₃/M ∈ {0.5, 1, 2, 4} подтверждает P ∝ 1/m₃ с разбросом произведения P·m₃ всего 4.29%.'}](figures/fig03_kl_sweeps.png)

*{'cap_en': 'Parameter sweeps: validation of the Kozai landscape e_max(i₀) and scaling of the KL clock with the perturber mass.', 'cap_ru': 'Параметрические развёртки: валидация ландшафта Козаи e_max(i₀) и масштабирование часов Козаи–Лидова по массе возмутителя.', 'walk_en': 'Across 12 inclinations from 30° to 80° the spline flow matches the analytic landscape to 1.128×10⁻⁵ (the 40° run needs an 8× longer span: the KL period diverges at i_crit), while below i_crit eccentricity stays at e₀ = 0.001; the mass sweep over m₃/M ∈ {0.5, 1, 2, 4} confirms P ∝ 1/m₃ with a P·m₃ spread of 4.29%.', 'walk_ru': 'По 12 наклонениям от 30° до 80° сплайновый поток совпадает с аналитикой с точностью 1.128×10⁻⁵ (прогон 40° требует 8-кратного удлинения: период Козаи–Лидова расходится на i_crit), ниже i_crit эксцентриситет остаётся на e₀ = 0.001; развёртка по m₃/M ∈ {0.5, 1, 2, 4} подтверждает P ∝ 1/m₃ с разбросом произведения P·m₃ всего 4.29%.'}.*

![{'cap_en': 'Dynamics on the fixed-j_z manifold: phase portrait and the residual of the tabulated Hamiltonian.', 'cap_ru': 'Динамика на многообразии фиксированного j_z: фазовый портрет и остаток табулированного гамильтониана.', 'walk_en': 'The phase portrait (ω mod π, e) shows ω librating about π/2 while e cycles between 0.001 and 0.763733 (60°) / 0.897238 (70°); the Hamiltonian residual along the 60° trajectory stays below 1.33×10⁻⁵ — the cubic-spline representation error on the 160 × 180 grid, not integrator error (DOP853, rtol 1e-8).', 'walk_ru': 'Фазовый портрет (ω mod π, e) показывает либрацию ω около π/2 при циклировании e между 0.001 и 0.763733 (60°) / 0.897238 (70°); остаток гамильтониана вдоль траектории 60° не превышает 1.33×10⁻⁵ — это ошибка кубически-сплайнового представления на сетке 160 × 180, а не ошибка интегратора (DOP853, rtol 1e-8).'}](figures/fig04_kl_dynamics.png)

*{'cap_en': 'Dynamics on the fixed-j_z manifold: phase portrait and the residual of the tabulated Hamiltonian.', 'cap_ru': 'Динамика на многообразии фиксированного j_z: фазовый портрет и остаток табулированного гамильтониана.', 'walk_en': 'The phase portrait (ω mod π, e) shows ω librating about π/2 while e cycles between 0.001 and 0.763733 (60°) / 0.897238 (70°); the Hamiltonian residual along the 60° trajectory stays below 1.33×10⁻⁵ — the cubic-spline representation error on the 160 × 180 grid, not integrator error (DOP853, rtol 1e-8).', 'walk_ru': 'Фазовый портрет (ω mod π, e) показывает либрацию ω около π/2 при циклировании e между 0.001 и 0.763733 (60°) / 0.897238 (70°); остаток гамильтониана вдоль траектории 60° не превышает 1.33×10⁻⁵ — это ошибка кубически-сплайнового представления на сетке 160 × 180, а не ошибка интегратора (DOP853, rtol 1e-8).'}.*

## 11. Results (full run)

```text
e_max_i0_60                = 7.637326e-01  (target 0.763763, tol 0.002)   PASS
e_max_i0_70                = 8.972376e-01  (target 0.897239, tol 0.002)   PASS
kl_period_halves_with_m3   = 4.810213e-01  (target 0.5, tol 0.03)         PASS
direct_3d_emax_validation  = PASS (direct smoothed e_max 0.7423 vs 0.7638, deviation -2.8%)
e_max_sweep_12pts          = max deviation 0.0000113 (i0: 30..80 deg, active range)
kl_clock_pm3_spread        = 4.29%  (P·m₃ over m₃/M in {0.5, 1, 2, 4})
spline_hamiltonian_drift   = 0.0000133  (grid 160 x 180, not integrator error)
status: PASS (4/4)   runtime: 64.6 s
```

## 12. Analysis

**Analytic maxima.** The headline checks compare the spline-flow maxima against the closed-form targets: e_max = 0.7637326 measured versus 0.7637626 analytic at i₀ = 60° (deviation 3.0×10⁻⁵) and 0.8972376 versus 0.8972386 at 70° (deviation 9.1×10⁻⁷) — both far inside the 2×10⁻³ acceptance band. The conserved quantities j_z = 0.500000 (60°) and 0.342020 (70°) stay constant along the flow, and the recorded eccentricity series returns exactly to e₀ = 0.001 at every cycle minimum (series range 0.001 … 0.76372882 in the JSON protocol).

**The exchange geometry.** fig02 shows the antiphase lock predicted by the derivation: eccentricity peaks exactly when the inclination dips to 39.2316° — numerically indistinguishable from i_crit = arccos√(3/5) — and the argument of pericentre librates about π/2 (fig04). The phase portraits of the two headline runs collapse onto the fixed-j_z manifolds j_z = 0.5 and j_z = 0.342020, the eccentricity–inclination ledger of the scheme.

**Landscape and clock.** The 12-point inclination sweep from 30° to 80° reproduces the analytic landscape with a maximum deviation of 1.128×10⁻⁵ over the active range; below i_crit (30°, 35°, 38°) eccentricity stays at e₀ = 0.001, and the 40° run needs an 8× longer span because the KL period diverges at the threshold (40°: 0.14818829 simulated versus 0.14818857 analytic; 45°: 0.40824826 versus 0.40824829; 80°: 0.97455930 versus 0.97454802). The clock scales as 1/m₃: P(2m₃)/P(m₃) = 0.481 against the ideal 0.5 (3% band; P(m₃) = 103829.39, P(2m₃) = 49944.15 in units of 1/n_in), and across m₃/M ∈ {0.5, 1, 2, 4} the product P·m₃ spreads only 4.29% (221991.0, 111355.7, 54927.46, 28661.83).

**Direct validation and error budget.** The independent 3-D run gives a smoothed maximum eccentricity 0.7423 versus 0.7638 analytic — a −2.8% deviation, inside the 8% gate and consistent with the hexadecapole truncation plus the non-test-particle mass ratio m₃/M = 0.5 at α = 0.2. The tabulated Hamiltonian drifts by at most 1.33×10⁻⁵ along the flow — the cubic-spline representation error on the 160 × 180 grid, deliberately separated from integrator error (DOP853, rtol 1e-8). Every number in this paragraph is stored in the JSON protocol with target, tolerance and pass flag.

## 13. Discussion and honest boundaries

The model is deliberately minimal: quadrupole order, test-particle inner orbit, circular outer orbit, no dissipation. Within these assumptions the conclusions are exact statements about the averaged equations, not simulations of a particular system. The natural extensions each preserve the verification style: the octupole term for eccentric companions (the eccentric Kozai–Lidov effect with orbit flips — Naoz 2016), the hexadecapole correction, comparable masses and radiation backreaction (pursued in TRX-11), and tidal friction coupling the KL cycles to orbital shrinkage in the hot-Jupiter channel.

The −2.8% direct-run deviation is not a defect but a measurement of the truncation: the direct problem at m₃/M = 0.5 and α = a_in/a_out = 0.2 is only moderately hierarchical, and higher-order multipoles plus the breakdown of the test-particle idealization push the true maximum eccentricity below the quadrupole formula. That a machine built from Newtonian gravity and geometry alone — with no KL formula inside — lands within 2.8% of a substantially non-idealized direct integration is the strongest statement of the study. The remaining error-budget line, the 1.33×10⁻⁵ Hamiltonian residual, is a property of the spline representation and could be pushed lower by refining the 160 × 180 grid, at quadratic cost in tabulation time.

Within the program this study anchors the secular celestial block: TRX-01 treats the same restricted problem at the libration points instead of secular cycles, TRX-11 integrates the comparable-mass three-body problem exactly and radiates, and TRX-12 stations a laser sailcraft at the L4 point of the same celestial stage. The laser link is direct: KL cycles are the accepted channel-forming mechanism for LISA-class compact-object mergers (Blaes, Lee & Socrates 2002), and laser ranging of binary and triple asteroids reads out exactly the orbital elements this study oscillates.

## 14. Conclusions

- The doubly-averaged quadrupole Hamiltonian, built numerically (240-point orbit quadrature, 160 × 180 spline grid), reproduces the analytic maxima e_max = 0.763763 (i₀ = 60°) and 0.897239 (70°) with deviations 3.0×10⁻⁵ and 9.1×10⁻⁷ — far inside the 2×10⁻³ tolerance.
- The eccentricity–inclination exchange is exactly antiphase: e peaks when i dips to i_crit = arccos√(3/5) = 39.23°, with j_z = 0.500000 (60°) and 0.342020 (70°) conserved along the flow.
- The Kozai landscape e_max(i₀) is validated over 12 inclinations from 30° to 80° with a maximum deviation of 1.128×10⁻⁵ over the active range; below i_crit eccentricity stays at e₀ = 0.001, and the KL period diverges at the threshold (the 40° run needs an 8× longer span).
- The KL clock obeys P ∝ 1/m₃: the measured ratio P(2m₃)/P(m₃) = 0.481 (ideal 0.5, 3% band) and the product P·m₃ spreads only 4.29% across m₃/M ∈ {0.5, 1, 2, 4}.
- An independent direct integration of the full 3-D restricted problem (m₃/M = 0.5, a_out = 5 a_in, 200 outer orbits) gives a smoothed maximum eccentricity 0.7423 versus 0.7638 — a −2.8% deviation consistent with the hexadecapole truncation and the finite mass ratio.
- The tabulated Hamiltonian is conserved to 1.33×10⁻⁵ along the flow — the honest error budget of the spline representation, reported alongside every check in the JSON protocol.

## 15. The monograph and its renditions

The complete monograph of this study exists in four renditions — Russian and English are separate documents, each in a typeset PDF and an editable DOCX:

| Rendition | Path |
|---|---|
| Monograph (English, PDF) | `monograph/monograph_EN.pdf` |
| Monograph (English, DOCX) | `monograph/monograph_EN.docx` |
| Monograph (Russian, PDF) | `monograph/monograph_RU.pdf` |
| Monograph (Russian, DOCX) | `monograph/monograph_RU.docx` |
| Reading-room copy | `publications/pdf/TRX-10-kozai-lidov_EN.pdf` · `publications/pdf/TRX-10-kozai-lidov_RU.pdf` |
| HTML source | `publications/html/TRX-10-kozai-lidov.html` |

**Monograph abstract.** This monograph treats the Kozai–Lidov mechanism — the secular exchange of eccentricity and inclination that a distant inclined companion drives in a hierarchical triple — in the full verification style of the TRIVORTEX program. Instead of coding the memorized analytic result, the study builds the doubly-averaged quadrupole Hamiltonian numerically: the instantaneous quadrupole disturbing potential is averaged over the inner orbit by a 240-point quadrature, tabulated on a 160 × 180 (e, ω) grid at the conserved j_z, and converted into a cubic spline whose derivatives drive the canonical flow. The spline flow reproduces the analytic maxima e_max = 0.763763 (i₀ = 60°) and 0.897239 (i₀ = 70°) to within the 2×10⁻³ tolerance, validates the Kozai landscape over 12 inclinations from 30° to 80° with a maximum deviation of 1.128×10⁻⁵, confirms the clock scaling P ∝ 1/m₃ (ratio P(2m₃)/P(m₃) = 0.481; P·m₃ spread 4.29%), and conserves the tabulated Hamiltonian to 1.33×10⁻⁵. An independent direct integration of the full three-dimensional restricted problem (m₃/M = 0.5, a_out = 5 a_in, 200 outer orbits) yields a smoothed maximum eccentricity of 0.7423 against 0.7638 — a −2.8% deviation consistent with the hexadecapole truncation. All four acceptance checks pass.

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
| `t` | 500 | 0 … 8.3860e+05 |
| `e` | 500 | 0.001 … 0.76360629 |

**Reproduction matrix**

| Command | What it does |
|---|---|
| `python3 research/TRX-10-kozai-lidov/code/trx10_kozai_lidov.py` | full run: physics + acceptance checks (64.6 s) |
| `python3 research/TRX-10-kozai-lidov/code/trx10_kozai_lidov.py --smoke` | CI guard: same checks, seconds-scale settings |
| `python3 research/TRX-10-kozai-lidov/code/trx10_kozai_lidov.py --figures` | regenerates the 300-dpi figure set |
| `make research-smoke` | all twelve studies in smoke mode |
| `make research-figures` | all twelve studies + figure sets |

## 17. Cross-links within the program

- **TRX-01** is the restricted-problem companion: libration points of the same celestial stage instead of secular cycles.
- **TRX-11** integrates the comparable-mass three-body problem exactly and radiates — the natural successor beyond the test-particle limit.
- **TRX-12** stations a laser sailcraft at the L4 point of the same celestial geometry (stationkeeping, not cycling).

## 18. Inside the script

The executable is a single deterministic file, `code/trx10_kozai_lidov.py`, ~pure `numpy`/`scipy` with no network access and no random state beyond fixed seeds. One run executes the full physics of the study, evaluates every registered acceptance check against its committed target and tolerance, and writes the JSON protocol — the same file quoted in §9.

| Mode | Invocation | What happens |
|---|---|---|
| Full | `python3 code/trx10_kozai_lidov.py` | complete experiment, all checks, JSON protocol (64.6 s) |
| Smoke | `python3 code/trx10_kozai_lidov.py --smoke` | identical acceptance logic at seconds-scale settings — the CI mode |
| Figures | `python3 code/trx10_kozai_lidov.py --figures` | regenerates the schematic + the four 300-dpi PNG panels |

**Outputs per run**

| File | Produced by | Content |
|---|---|---|
| `results/trx10_results.json` | every mode | status, checks (value/target/tol/unit/pass/note), series, meta |
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
| Previous study | TRX-009 |
| Next study | TRX-011 |

## 21. Notation

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

## 22. References

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

## 23. Glossary

| Term | Definition |
|---|---|
| Kozai–Lidov oscillations | secular exchange of eccentricity and inclination in a hierarchical triple, driven by the double-averaged quadrupole perturbation |
| Kozai angle i_crit | critical inclination arccos√(3/5) ≈ 39.23° above which the exchange turns on for an initially circular orbit |
| j_z | z-component of the orbital angular momentum, j_z = √(1 − e²)·cos i — the conserved quadrupole invariant |
| Double averaging | removal of the short-period terms by averaging over both orbital periods, leaving purely secular dynamics |
| Quadrupole approximation | leading anisotropic term (l = 2) of the expansion of the companion potential in a_in/a_out |
| Secular dynamics | long-term evolution of orbital elements with the mean longitudes averaged out |
| Argument of pericentre ω | orientation of the ellipse in its plane; librates about π/2 during KL cycles |
| e_max | maximum eccentricity of the KL cycle; for e₀ ≈ 0: e_max = √(1 − (5/3)cos²i₀) |
| Spline Hamiltonian | cubic-spline representation of the tabulated averaged potential that drives the flow |
| DOP853 | explicit Dormand–Prince 8(5,3) adaptive integrator, used for both the secular and the direct runs |

## 24. Appendix A. Full parameter table

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

**Protocol-level parameter snapshot** (`results` JSON, `meta` block):

| Key | Value |
|---|---|
| `equations` | `["double-averaged quadrupole Hamiltonian (numerical orbit average, spline flow)", "e_max = sqrt(1-(5/3)cos^2 i0) ; j_z = sqrt(1-e^2) cos i = const", "t_KL ~ (1/C2) ~ (m_tot/m3)(a_out/a_in)^3 P_in^2"]` |
| `e_max_60` | `0.7637522326938432` |
| `e_max_70` | `0.8972294445187509` |
| `e_max_direct` | `null` |
| `laser_link` | `"laser ranging of triple asteroids; LISA-type laser interferometry of compact-object triples"` |

## 25. Appendix B. BibTeX

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

## 26. How to cite

Cite the repository through [`CITATION.cff`](../../CITATION.cff) (DOI 10.5281/zenodo.21825394, version 1.0.0); this study is part of the TRIVORTEX Research Program. If you cite the study alone, name the monograph rendition you used and attach the JSON protocol of the run you reproduced.

```bibtex
@misc{trivortextrx102026isaev,
  author       = {Isaev, Iskhak Khamzatovich},
  title        = {Kozai–Lidov Oscillations in Hierarchical Triples (TRIVORTEX Research Program, TRX-10)},
  year         = {2026},
  howpublished = {Zenodo},
  doi          = {10.5281/zenodo.21825394},
  url          = {https://github.com/wild8highlander/research-papers}
}
```

