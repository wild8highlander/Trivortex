# TRX-12 — Laser Highway: Light-Sail Stationkeeping at L4/L5

*TRIVORTEX Research Program · version 1.0.0 · study TRX-12 of 12*

A photon light sail in the Earth–Moon circular restricted three-body problem, pushed by a 1 MW laser beam: the thrust **a_L = 2P/(cm)** is pointed by a proportional-derivative beam-steering law and capped by the photon ceiling **a_max = 0.2443** (dimensionless). The study demonstrates the two core operations of a "laser highway" — holding a spacecraft at the linearly stable but neutrally drifting L4 point to **7.5e-07** of the nominal position, and pumping the Jacobi constant down with along-velocity thrust to move between invariant manifolds.

> **Edition 1.0.0.** This README is part of the first public release of the TRIVORTEX research program. The study ships as an executable script, a committed JSON protocol, four 300-dpi figures, a schematic and a bilingual monograph in four renditions (Russian and English, each in PDF and DOCX).

**At a glance**

| Aspect | Value |
|---|---|
| Block | Laser highway — study 12 of 12 |
| Model | Earth–Moon CR3BP + photon-thrust actuator (μ = 0.0121505856) |
| Key invariant | Jacobi constant C_J — pumped down by along-velocity thrust |
| Headline result | controlled bound 7.5e-07 at L4 — ≈ 5500× tighter than free drift |
| Verification | 5/5 checks PASS (full mode) |
| Runtime | 41.4 s full run recorded with figures · < 20 s smoke |

| Field | Value |
|---|---|
| Study | `TRX-12` (TRX-12-laser-light-sail) |
| Program | TRIVORTEX — The Three-Body Problem in the Vortex Model |
| Author | Isaev Iskhak Khamzatovich (ORCID `0009-0003-7299-0701`) |
| DOI | [10.5281/zenodo.21825394](https://doi.org/10.5281/zenodo.21825394) |
| Version | 1.0.0 — first public release |
| Code | `research/TRX-12-laser-light-sail/code/trx12_laser_light_sail.py` |
| Protocol | `research/TRX-12-laser-light-sail/results/trx12_results.json` |
| License | `LicenseRef-Proprietary-Wild8Highlander-1.0` |

## 1. Mission

The Earth–Moon L4 point is linearly stable for μ = 0.0121505856 < μ_Routh ≈ 0.03852, but the stability is neutral: a spacecraft placed near it librates forever around it with whatever offset it started — never converging, never leaving. The free run of this study keeps a distance floor of 0.0041 over its second half and wanders on a tadpole of extent up to 0.026. A laser-powered sail changes that: photon thrust 2P/(cm), pointed by a PD beam-steering law, drives the libration amplitude down and holds the station to microns of the nominal point. The operation is verified honestly: with a 1 MW beam on a 10 kg sail (a_max = 0.2443 computed from SI units, not assumed), a PD-controlled sail starting 1.1·10⁻³ away from L4 converges to |r − L4| ≤ 7.5e-07 and stays there, using the photon ceiling 0% of the time after the transient.

The second operation is orbit raising. With the beam pointed along the velocity, the Jacobi constant C_J = 2Ω − v² obeys Ċ_J = −2a_L·v ≤ 0 and decreases monotonically: the laser pumps the sail across the invariant-manifold ladder that organizes the restricted problem, instead of fighting gravity point-by-point. The open-loop demo lowers C_J by 1063.51 over T = 30 with the largest single-step increase at −0.06 (strictly monotone), and the SI power table for a 100 kg sail over 30 days (Δv ∈ {10, 50, 100, 500} m/s costs 57.8 kW … 2.89 MW of beam power) closes the loop to engineering numbers. Together the two operations define the laser highway: hold where you want to stay, move C_J when you want to go.

## 2. Introduction and historical context

The equilateral solutions of the three-body problem were found by Joseph-Louis Lagrange in his 1772 *Essai sur le problème des trois corps*, and for more than a century they were regarded as mathematical curiosities. The discovery of the Trojan asteroids at the Sun–Jupiter L4 and L5 turned the Lagrange triangle into a real object of celestial mechanics, and Szebehely's 1967 monograph consolidated the restricted problem into the standard reference frame every modern libration-point mission still uses. For the Earth–Moon system the triangular points are especially tempting stations: linearly stable for μ < μ_Routh ≈ 0.03852, they ask only for a stationkeeping technique that removes the offsets their neutral stability lets persist forever.

The physics of the required actuator is surprisingly old. Lebedev (1901) measured the pressure of light on solids, and Nichols and Hull (1903) confirmed it independently; the idea of propelling a vehicle by photons was put on a quantitative footing by Marx (1966), who computed the parameters of an interstellar vehicle pushed by a terrestrial laser beam, and by Redding (1967), who analysed staged photon rockets. These two Nature papers founded laser propulsion: a beam of power P delivers thrust 2P/(cm) to a mirrored sail — per kilogram of payload, the cheapest reaction mass imaginable, since the propellant is light itself.

Forward (1984) turned the arithmetic into a roundtrip interstellar mission design and fixed the canonical figure of merit — the photon ceiling 2P/(cm) — that every later beamed-energy concept inherited, from kilometer-scale lightsails to laser arrays for sailcraft. Close to home, McInnes (1999) systematized the dynamics of sailing craft in gravity fields, Baoyin and McInnes (2006) computed displaced equilibrium families for sails, and Simo and McInnes (2009) placed solar sails on displaced Earth–Moon Lagrange-point trajectories. The present study keeps the same physical ceiling but replaces the passive sail orientation with an actively steered beam — a laser highway in miniature.

For TRIVORTEX the relevance is structural rather than technological. The L4 point is the celestial twin of the same-sign vortex triangle of Theorem 3.1, the Jacobi integral plays the role of the Chaplygin integral C_Ch, and the beam-steering law is the analog of circulation control: an actuator applied to a special solution of the same central-configuration family. The laser block of the program now closes symmetrically — TRX-01 points the laser at the primaries and dresses gravity, TRX-12 points it at the spacecraft and dresses the equations of motion with a bounded thrust term; together they demonstrate that the invariant structuring the phase space is also the quantity an actuator can move.

## 3. Physical system and preset

Planar CR3BP in the rotating frame. The Earth and the Moon move on circular orbits about their barycenter and are fixed at (−μ, 0) and (1 − μ, 0) in the co-rotating axes; the sail is a massless particle responding to their gravity, to the centrifugal and Coriolis terms, and to the photon thrust. The whole stationkeeping problem lives in the topography of one scalar function — the effective potential Ω — whose sole maximum of interest sits at the equilateral point L4 = (½ − μ, √3/2).

The actuator is photon momentum. A beam of power P carries momentum flux P/c, and a mirrored sail returns it, doubling the transfer: the thrust is a_L = 2P/(cm) along the beam direction, exactly 6.67·10⁻⁴ m/s² for 1 MW on 10 kg, or 0.2443 in canonical units — a real force ceiling computed from SI constants, not a fitted parameter. The control law points this bounded force: u = −K_p(r − r_L4) − K_d·v with gains K_p = K_d = 4, saturated at the ceiling. The same physics read backwards gives the orbit-raising rule: thrust along velocity does negative work on C_J at the rate −2a_L·v, so a laser highway moves between manifolds by spending photons, not fuel.

| Parameter | Value | Meaning |
|---|---|---|
| μ | 0.0121505856 | Earth–Moon mass parameter |
| LU, TU | 3.844·10⁸ m, 3.752·10⁵ s | canonical length and time (GM = 1; month = 2π) |
| laser | P = 1 MW, m = 10 kg | transmitter and sail → a_max = 0.2443 (= 6.67·10⁻⁴ m/s²) |
| start state | L4 + (1e-3, 5e-4), v = (2e-4, −1e-4) | initial offset 1.118·10⁻³ from L4 |
| PD gains | K_p = K_d = 4 | beam-steering law, saturated at a_max |
| spans | T = 100 keep · 30 pump · 60 per gain cell | ≈ 434 · 130 · 261 days in TU units |
| integrator | DOP853, rtol = atol = 1e-11 | dense output; max_step 0.1 (0.02 pumping) |

**Model assumptions**

- Planar motion; the out-of-plane dimension and halo families are not modeled.
- Circular primary orbits with the constant Earth–Moon mass parameter μ = 0.0121505856.
- Photon thrust is the only non-gravitational force: no ablation, no sail aging, no beam-transit delay — the beam direction is an idealized instantaneous control input.
- The sail is a perfect photon reflector: the thrust magnitude is capped by a_max = 2P/(cm) = 0.2443 (1 MW on 10 kg), computed from SI constants rather than fitted.
- The sail mass is constant; the PD law is continuous-time and saturates instantaneously at the ceiling.
- The open-loop pumping run ignores stationkeeping: the full ceiling thrust is locked along the velocity — a deliberately idealized demonstration of the C_J ladder.

## 4. Governing equations

(E1) CR3BP equations of motion in the rotating frame with laser thrust appended:

$$\ddot{x} - 2\dot{y} = \frac{\partial\Omega}{\partial x} + a_{Lx}, \qquad \ddot{y} + 2\dot{x} = \frac{\partial\Omega}{\partial y} + a_{Ly}, \qquad \Omega = \tfrac{1}{2}(x^2+y^2) + \frac{1-\mu}{r_1} + \frac{\mu}{r_2}$$

(E2) Photon thrust along the beam direction û (P = 1 MW, m = 10 kg):

$$a_L = \frac{2P}{c\,m}\,\hat{u}$$

(E3) PD beam-steering law bounded by the photon ceiling (K_p = K_d = 4):

$$\mathbf{u} = -K_p\,(\mathbf{r} - \mathbf{r}_{L4}) - K_d\,\mathbf{v}, \qquad |\mathbf{a}_L| \le a_{\max} = \frac{2P}{cm} = 0.2443$$

(E4) Jacobi constant; monotone pumping under along-velocity thrust:

$$C_J = 2\Omega - (\dot{x}^2 + \dot{y}^2), \qquad \dot{C}_J = -2\,\mathbf{a}_L\cdot\mathbf{v} \le 0$$

(E5) SI power table (100 kg sail, 30 days, Δv ∈ {10, 50, 100, 500} m/s):

$$P = \frac{m\,a\,c}{2}, \qquad a = \frac{\Delta v}{T_{burn}}$$

## 5. Scheme

![TRX-12 scheme — the laser highway: a 1 MW photon beam from Earth pushes a 10 kg light sail near L4; the PD feedback loop points the photon thrust and collapses the free-drift halo onto the nominal point, while along-velocity thrust pumps C_J down for orbit raising.](figures/scheme_trx12.svg)

*TRX-12 scheme — the laser highway: a 1 MW photon beam from Earth pushes a 10 kg light sail near L4; the PD feedback loop points the photon thrust and collapses the free-drift halo onto the nominal point, while along-velocity thrust pumps C_J down for orbit raising..*

The diagram encodes the following elements:

- **Earth · laser site** — gold disc with the 1 MW transmitter; the barycentre cross marks the rotating-frame origin
- **Photon beam cone** — gold corridor from the laser site to the sail — thrust 2P/(cm) along the beam axis
- **Moon · m₂ = μ** — second primary with μ = 0.0121505856, unperturbed Newtonian gravity
- **Equilateral guide lines** — dashed Earth–L4–Moon triangle of side LU = 3.844·10⁸ m
- **L4 halo and light sail** — dashed free-drift halo collapsed by the sail onto |r − L4| ≈ 7.5·10⁻⁷
- **Feedback control loop** — box with the PD law u = −K_p(r − r_L4) − K_d·v and the ceiling |a_L| ≤ 2P/(cm) = 0.2443; the bottom note states the orbit-raising rule Ċ_J = −2a_L·v ≤ 0

## 6. Mapping to TRIVORTEX

The mapping is one-to-one at the structural level. The libration point L4 is the celestial realization of the Lagrange triangle vertex — the same central configuration that underlies the same-sign vortex triangle of Theorem 3.1; the Jacobi constant plays the role of the Chaplygin integral C_Ch as the invariant that pins the orbit to a reduced phase space; and the PD beam-steering law acts on the libration solution exactly as circulation control acts on a vortex configuration — an actuator applied to a special solution of the same equations. The photon ceiling a_max = 2P/(cm) is the celestial twin of the finite-force regularization used in the vortex model: both keep the actuator honest, capping how fast the invariant can be moved. The laser highway thus closes the TRIVORTEX loop — the quantity that structures the phase space (C_J ↔ C_Ch) is precisely the quantity the actuator moves.

| Quantity in this study | TRIVORTEX analog | Comment |
|---|---|---|
| L4 libration point | Lagrange triangle vertex (Theorem 3.1) | the same central configuration |
| Jacobi constant C_J | Chaplygin integral C_Ch | the invariant the laser moves |
| PD beam-steering law u | circulation control in the vortex model | actuating a special solution |
| Photon ceiling 2P/(cm) | finite-force regularization | honest actuator limits |

## 7. Dimensionless formulation

All dynamics in canonical CR3BP units: length = Earth–Moon distance LU = 3.844·10⁸ m, time = TU = 3.752·10⁵ s (GM = 1; one full primary revolution is 2π ≈ 27.3 days), mass = m₁ + m₂. Accelerations are measured in LU/TU² (1 unit ≈ 2.73 mm/s²) and velocities in LU/TU (1 unit ≈ 1.02 km/s); the photon ceiling 0.2443 corresponds to 1 MW on a 10 kg sail.

## 8. Numerical method

All trajectories are integrated in the rotating frame with an explicit Dormand–Prince 8(5,3) scheme (scipy solve_ivp, DOP853) at rtol = atol = 1e-11 with dense output; the stationkeeping runs use T = 100 with max_step = 0.1 and 800 recorded samples, the pumping run T = 30 with max_step = 0.02 and 800 samples. The control law is evaluated inside the right-hand side: u = −K_p(r − r_L4) − K_d·v with K_p = K_d = 4, rescaled to the ceiling a_max = 0.2443 whenever its norm exceeds it, and the fraction of saturated control evaluations is accumulated as the run proceeds.

The contrast run repeats the integration from the identical initial state L4 + (1e-3, 5e-4), v = (2e-4, −1e-4) with the control switched off, so the only difference between the two trajectories is the laser. Acceptance checks are computed on strict windows — max |r − L4| for t > T/4 (controlled) and min |r − L4| for t > T/2 (free) — so that neither the transient nor the start point can flatter the result. A PD gain-plane sweep repeats the controlled run for a 17 × 17 grid of gains (K_p from 0.5 to 512, K_d from 0.5 to 32, logarithmic, the operating point (4, 4) pinned to both grids) over T = 60 per cell, recording the late-time bound and the saturation fraction of every cell.

The open-loop pumping run starts on an eccentric orbit about the Earth primary (r₀ = 0.10, speed 1.05× the local circular value) with the full ceiling thrust locked along the velocity; C_J is sampled at 800 points over T = 30 and the largest single-step increase is checked against zero. The SI power table (E5) is recomputed analytically for Δv ∈ {10, 50, 100, 500} m/s delivered over 30 days by a 100 kg sail, and its internal consistency (P = m·a·c/2) is itself a check in the protocol.

## 9. Verification protocol and acceptance checks

Every check is registered before the run: target, tolerance and unit are committed in the protocol, not chosen after the fact.

| Check | Target | Tolerance |
|---|---|---|
| Controlled: max \|r − L4\| for t > T/4 | 0 | 2e-4 |
| Control saturation fraction (t > transient) | 0 | 5% |
| Free drift: min \|r − L4\| after T/2 | > 5e-4 | exact |
| Jacobi pumping: max single-step C_J increase | ≤ 1e-9 | exact |
| SI power table internally consistent (P = m·a·c/2) | yes | exact |

**Recorded verification run** (mode: smoke, status: **PASS**, 5/5 checks)

| Check | Recorded value | Target | Tolerance | Unit | Verdict |
|---|---|---|---|---|---|
| `controlled_l4_bound` | 8.7632e-05 | 0 | 2.0000e-04 | dimless | PASS |
| `control_saturation_fraction` | 0 | 0 | 0.05 | fraction | PASS |
| `free_drift_never_converges` | 1 | 1 | 1.0000e-12 | bool | PASS |
| `jacobi_pumped_monotonically` | 1 | 1 | 1.0000e-12 | bool | PASS |
| `power_table_consistent` | 1 | 1 | 1.0000e-12 | bool | PASS |

**Check notes** — what each number means:

| Check | Note |
|---|---|
| `controlled_l4_bound` | max \|r-L4\| for t > T/4 (start offset 1.1e-3); a_max = 0.2443 |
| `control_saturation_fraction` | fraction of control steps at the photon-thrust ceiling |
| `free_drift_never_converges` | min \|r-L4\| without control = 0.0048 (stays 5x wider than controlled) |
| `jacobi_pumped_monotonically` | max single-step C_J increase = -2.42e-02; net dC_J = 159.9524 |
| `power_table_consistent` | P = m a c / 2 for dv in {10,50,100,500} m/s over 30 days |

## 10. Figure gallery (300 dpi)

![{'cap_en': 'Landscape of the Earth–Moon laser highway, μ = 0.0121505856: (a) rotating-frame potential with the lunar orbit, the equilateral points L4/L5 and the photon beam cone from Earth toward L4; (b) zoom at L4 over T = 100 — the free sail wanders on a tadpole of extent 0.026 while the controlled sail converges (inset: the controlled spiral).', 'cap_ru': 'Ландшафт лазерной трассы Земля–Луна при μ = 0.0121505856: (а) потенциал во вращающейся системе с лунной орбитой, равносторонними точками L4/L5 и конусом фотонного пучка от Земли к L4; (б) увеличение у L4 на T = 100 — свободный парус бродит по «головастику» размером 0.026, управляемый сходится (врезка: управляемая спираль).', 'walk_en': 'Panel (a) shows the 2Ω topography with Earth (gold), the Moon (navy) and the dashed lunar orbit, with the beam corridor drawn from Earth to L4; panel (b) contrasts the free tadpole (extent up to 0.026 from L4) with the controlled spiral collapsing onto the nominal point, the inset window spanning 2.5·10⁻³.', 'walk_ru': 'Панель (а) показывает топографию 2Ω с Землёй (золотая), Луной (тёмная) и пунктирной лунной орбитой, вдоль которой к L4 прорисован коридор пучка; панель (б) противопоставляет свободного «головастика» (размер до 0.026 от L4) управляемой спирали, схлопывающейся в номинальную точку, — окно врезки охватывает 2.5·10⁻³.'}](figures/fig01_landscape.png)

*{'cap_en': 'Landscape of the Earth–Moon laser highway, μ = 0.0121505856: (a) rotating-frame potential with the lunar orbit, the equilateral points L4/L5 and the photon beam cone from Earth toward L4; (b) zoom at L4 over T = 100 — the free sail wanders on a tadpole of extent 0.026 while the controlled sail converges (inset: the controlled spiral).', 'cap_ru': 'Ландшафт лазерной трассы Земля–Луна при μ = 0.0121505856: (а) потенциал во вращающейся системе с лунной орбитой, равносторонними точками L4/L5 и конусом фотонного пучка от Земли к L4; (б) увеличение у L4 на T = 100 — свободный парус бродит по «головастику» размером 0.026, управляемый сходится (врезка: управляемая спираль).', 'walk_en': 'Panel (a) shows the 2Ω topography with Earth (gold), the Moon (navy) and the dashed lunar orbit, with the beam corridor drawn from Earth to L4; panel (b) contrasts the free tadpole (extent up to 0.026 from L4) with the controlled spiral collapsing onto the nominal point, the inset window spanning 2.5·10⁻³.', 'walk_ru': 'Панель (а) показывает топографию 2Ω с Землёй (золотая), Луной (тёмная) и пунктирной лунной орбитой, вдоль которой к L4 прорисован коридор пучка; панель (б) противопоставляет свободного «головастика» (размер до 0.026 от L4) управляемой спирали, схлопывающейся в номинальную точку, — окно врезки охватывает 2.5·10⁻³.'}.*

![{'cap_en': 'Headline result — laser stationkeeping versus free drift: (a) distance to L4 on a logarithmic scale over T = 100 (≈ 434 days); the controlled sail settles at 7.5e-07 while the free sail never comes closer than 0.0041 after T/2 — a contrast of ≈ 5500×; (b) the stationkeeping budget: controlled bound, acceptance tolerance 2e-4, initial offset 1.1·10⁻³ and the free-drift floor.', 'cap_ru': 'Главный результат — лазерное удержание против свободного дрейфа: (а) расстояние до L4 в логарифмическом масштабе на T = 100 (≈ 434 суток); управляемый парус оседает на 7.5e-07, тогда как свободный ни разу не подходит ближе 0.0041 после T/2 — контраст ≈ 5500×; (б) бюджет удержания: управляемая граница, приёмочный допуск 2e-4, начальное смещение 1.1·10⁻³ и пол свободного дрейфа.', 'walk_en': 'The gold curve drops by more than three decades during the transient and then hugs the 7.5e-07 level, far below the dashed acceptance bound 2e-4; the bar panel lines up the four budget distances on a logarithmic axis from the controlled bound to the free-drift floor 0.0041.', 'walk_ru': 'Золотая кривая падает более чем на три порядка во время переходного процесса и затем прижимается к уровню 7.5e-07, далеко ниже пунктирной приёмочной границы 2e-4; столбиковая панель выстраивает четыре бюджетных расстояния на логарифмической оси — от управляемой границы до пола свободного дрейфа 0.0041.'}](figures/fig02_stationkeep.png)

*{'cap_en': 'Headline result — laser stationkeeping versus free drift: (a) distance to L4 on a logarithmic scale over T = 100 (≈ 434 days); the controlled sail settles at 7.5e-07 while the free sail never comes closer than 0.0041 after T/2 — a contrast of ≈ 5500×; (b) the stationkeeping budget: controlled bound, acceptance tolerance 2e-4, initial offset 1.1·10⁻³ and the free-drift floor.', 'cap_ru': 'Главный результат — лазерное удержание против свободного дрейфа: (а) расстояние до L4 в логарифмическом масштабе на T = 100 (≈ 434 суток); управляемый парус оседает на 7.5e-07, тогда как свободный ни разу не подходит ближе 0.0041 после T/2 — контраст ≈ 5500×; (б) бюджет удержания: управляемая граница, приёмочный допуск 2e-4, начальное смещение 1.1·10⁻³ и пол свободного дрейфа.', 'walk_en': 'The gold curve drops by more than three decades during the transient and then hugs the 7.5e-07 level, far below the dashed acceptance bound 2e-4; the bar panel lines up the four budget distances on a logarithmic axis from the controlled bound to the free-drift floor 0.0041.', 'walk_ru': 'Золотая кривая падает более чем на три порядка во время переходного процесса и затем прижимается к уровню 7.5e-07, далеко ниже пунктирной приёмочной границы 2e-4; столбиковая панель выстраивает четыре бюджетных расстояния на логарифмической оси — от управляемой границы до пола свободного дрейфа 0.0041.'}.*

![{'cap_en': 'PD gain-plane control map on the same integrator (T = 60 per cell, 17 × 17 gains, K_p from 0.5 to 512 and K_d from 0.5 to 32): (a) logarithm of the late-time stationkeeping error with the acceptance contour 2e-4 and the operating point (4, 4) marked — the map spans 0 (tightest cells) to 123.3 (weak gains lose the station); (b) saturation fraction of the photon-thrust ceiling, near zero across the working region.', 'cap_ru': 'Карта управления на плоскости ПД-коэффициентов на том же интеграторе (T = 60 на ячейку, 17 × 17 пар, K_p от 0.5 до 512 и K_d от 0.5 до 32): (а) логарифм позднего времени ошибки удержания с контуром допуска 2e-4 и рабочей точкой (4, 4) — карта простирается от 0 (самые тесные ячейки) до 123.3 (слабые коэффициенты теряют станцию); (б) доля насыщения фотонного потолка, близкая к нулю во всей рабочей области.', 'walk_en': 'The gold star marks the operating point (4, 4), whose late bound is 1.75·10⁻⁵ with zero saturation; the darkest corners of panel (b) show where aggressive gains press against the photon ceiling (up to 0.87 of steps saturated), 77 of the 289 cells exceeding the 5% level.', 'walk_ru': 'Золотая звезда отмечает рабочую точку (4, 4) с поздней границей 1.75·10⁻⁵ и нулевым насыщением; самые тёмные углы панели (б) показывают, где агрессивные коэффициенты прижимаются к фотонному потолку (до 0.87 насыщенных шагов) — 77 из 289 ячеек превышают уровень 5%.'}](figures/fig03_control_map.png)

*{'cap_en': 'PD gain-plane control map on the same integrator (T = 60 per cell, 17 × 17 gains, K_p from 0.5 to 512 and K_d from 0.5 to 32): (a) logarithm of the late-time stationkeeping error with the acceptance contour 2e-4 and the operating point (4, 4) marked — the map spans 0 (tightest cells) to 123.3 (weak gains lose the station); (b) saturation fraction of the photon-thrust ceiling, near zero across the working region.', 'cap_ru': 'Карта управления на плоскости ПД-коэффициентов на том же интеграторе (T = 60 на ячейку, 17 × 17 пар, K_p от 0.5 до 512 и K_d от 0.5 до 32): (а) логарифм позднего времени ошибки удержания с контуром допуска 2e-4 и рабочей точкой (4, 4) — карта простирается от 0 (самые тесные ячейки) до 123.3 (слабые коэффициенты теряют станцию); (б) доля насыщения фотонного потолка, близкая к нулю во всей рабочей области.', 'walk_en': 'The gold star marks the operating point (4, 4), whose late bound is 1.75·10⁻⁵ with zero saturation; the darkest corners of panel (b) show where aggressive gains press against the photon ceiling (up to 0.87 of steps saturated), 77 of the 289 cells exceeding the 5% level.', 'walk_ru': 'Золотая звезда отмечает рабочую точку (4, 4) с поздней границей 1.75·10⁻⁵ и нулевым насыщением; самые тёмные углы панели (б) показывают, где агрессивные коэффициенты прижимаются к фотонному потолку (до 0.87 насыщенных шагов) — 77 из 289 ячеек превышают уровень 5%.'}.*

![{'cap_en': 'Dynamics of the two laser operations: (a) open-loop Jacobi pumping — C_J decreases monotonically under along-velocity thrust, net ΔC_J = 1063.51 over T = 30 (largest single-step increase −0.06); (b) control effort of the stationkeeping run — peak demand 0.0051 (= 1.4·10⁻⁵ m/s², equivalent to 20.7 kW on 10 kg) against the photon ceiling 0.2443, headroom 48×.', 'cap_ru': 'Динамика двух лазерных операций: (а) открытая прокачка Якоби — C_J монотонно убывает при тяге вдоль скорости, суммарное ΔC_J = 1063.51 за T = 30 (наибольший одношаговый прирост −0.06); (б) управление в режиме удержания — пиковая потребность 0.0051 (= 1.4·10⁻⁵ м/с², эквивалент 20.7 кВт на 10 кг) против фотонного потолка 0.2443, запас 48×.', 'walk_en': 'Panel (a) records the invariant sliding from −7.66 down to −1068 with strictly negative increments; panel (b) shows the demand |a_L| peaking at the transient start (the initial state alone demands ≈ 5.1·10⁻³) and collapsing toward the plot floor 1e-7, never approaching the dashed ceiling 0.2443.', 'walk_ru': 'Панель (а) фиксирует скольжение инварианта от −7.66 вниз до −1068 со строго отрицательными приращениями; панель (б) показывает пик потребности |a_L| в начале переходного процесса (одно начальное состояние требует ≈ 5.1·10⁻³) и спад к нижней границе графика 1e-7 — пунктирный потолок 0.2443 не достигается никогда.'}](figures/fig04_dynamics.png)

*{'cap_en': 'Dynamics of the two laser operations: (a) open-loop Jacobi pumping — C_J decreases monotonically under along-velocity thrust, net ΔC_J = 1063.51 over T = 30 (largest single-step increase −0.06); (b) control effort of the stationkeeping run — peak demand 0.0051 (= 1.4·10⁻⁵ m/s², equivalent to 20.7 kW on 10 kg) against the photon ceiling 0.2443, headroom 48×.', 'cap_ru': 'Динамика двух лазерных операций: (а) открытая прокачка Якоби — C_J монотонно убывает при тяге вдоль скорости, суммарное ΔC_J = 1063.51 за T = 30 (наибольший одношаговый прирост −0.06); (б) управление в режиме удержания — пиковая потребность 0.0051 (= 1.4·10⁻⁵ м/с², эквивалент 20.7 кВт на 10 кг) против фотонного потолка 0.2443, запас 48×.', 'walk_en': 'Panel (a) records the invariant sliding from −7.66 down to −1068 with strictly negative increments; panel (b) shows the demand |a_L| peaking at the transient start (the initial state alone demands ≈ 5.1·10⁻³) and collapsing toward the plot floor 1e-7, never approaching the dashed ceiling 0.2443.', 'walk_ru': 'Панель (а) фиксирует скольжение инварианта от −7.66 вниз до −1068 со строго отрицательными приращениями; панель (б) показывает пик потребности |a_L| в начале переходного процесса (одно начальное состояние требует ≈ 5.1·10⁻³) и спад к нижней границе графика 1e-7 — пунктирный потолок 0.2443 не достигается никогда.'}.*

## 11. Results (full run)

```text
controlled_l4_bound               = 7.5e-07  (vs 1.1·10⁻³ initial offset; tol 2e-4)
control_saturation_fraction       = 0.0      (never at the photon ceiling 0.2443)
free_drift_never_converges        = PASS (min 0.0041 over the second half)
jacobi_pumped_monotonically       = PASS (max step increase −0.0604; net dC_J = 1063.51)
power_table_consistent            = PASS (P = m·a·c/2 for Δv ∈ {10, 50, 100, 500} m/s)
status: PASS (5/5)   runtime: 41.4 s (full run recorded with --figures)
```

## 12. Analysis

**Stationkeeping.** From the initial offset 1.118·10⁻³ the controlled sail collapses onto L4 during the transient and then stays bounded by 7.5e-07 for all t > T/4 — a final error ≈ 270× tighter than the 2e-4 acceptance tolerance. The uncontrolled twin never comes closer than 0.0041 over its second half and wanders on a tadpole of extent up to 0.026: the contrast factor between the free floor and the controlled bound is ≈ 5500×. This is the entire mission case for a laser highway in one number.

**Actuator budget.** The peak control demand is 0.0051 (the initial state alone demands ≈ 5.1·10⁻³ of ceiling), or 1.4·10⁻⁵ m/s² in SI — equivalent to 20.7 kW of beam power on the 10 kg sail — against the ceiling 0.2443: a headroom of 48×. The saturation fraction of the headline run is exactly 0.0: the photon ceiling is never touched. The 17 × 17 gain sweep brackets the operating point from both sides — the late-time bound spans 0 (tightest cells) to 123.3 (weak gains lose the station), while the operating point (4, 4) holds 1.75·10⁻⁵ with zero saturation; aggressive high-gain corners do press against the ceiling (up to 0.87 of steps saturated), and 77 of the 289 cells exceed the 5% saturation level.

**Jacobi pumping.** With the full ceiling thrust locked along the velocity, C_J slides monotonically from −7.66 down to −1068 over T = 30: net ΔC_J = 1063.51, and the largest single-step increase across the whole record is −0.0604 — every increment strictly negative, exactly as Ċ_J = −2a_L·v ≤ 0 demands. The laser demonstrably moves the invariant that structures the restricted problem's phase space.

**Engineering closure.** The SI table prices the operations: delivering Δv ∈ {10, 50, 100, 500} m/s to a 100 kg sail over 30 days costs 57.8 kW, 289 kW, 578 kW and 2.89 MW of beam power respectively — while the stationkeeping task itself runs at a peak equivalent of 20.7 kW on 10 kg. A 1 MW transmitter therefore holds a station with a 48× margin and simultaneously has photon budget for meaningful orbit raising: the laser highway is a single power plant serving both operations.

## 13. Discussion and honest boundaries

The model is deliberately minimal: planar motion, circular primary orbits, instantaneous beam pointing and an ideal mirrored sail. Within these assumptions every conclusion is an exact statement about the governing equations rather than a simulation of a specific mission. The natural extensions — eccentric binaries, out-of-plane halo families around the collinear points, beam-transit delay and diffraction losses in the pointing loop, adaptive or frequency-shaped gains — each preserve the verification style established here, and none of them can remove the central fact that a bounded, correctly pointed force turns neutral libration into a controlled equilibrium.

The parameter regime is chosen for honesty rather than spectacle. The photon ceiling 0.2443 follows from SI constants (1 MW, 10 kg, c) and is never assumed away; the gain sweep shows where the controller would need more authority than the beam can deliver (77 of 289 cells above 5% saturation, up to 0.87) and where weak gains simply lose the station (bounds up to 123.3). The operating point (4, 4) sits in a broad low-error, zero-saturation region, which is the practically relevant statement: the laser highway does not live on the edge of its actuator.

Within the program this study is the actuator half of the laser block. TRX-01 dresses the primaries with radiation and maps how the libration landscape deforms; TRX-12 dresses the spacecraft itself and holds it at the undressed landscape's best address. TRX-10 supplies the secular transport machinery (Kozai–Lidov cycles) that a laser highway would exploit for large, naturally slow rearrangements between manifolds, and TRX-11 covers the extreme-mass regime of the same three-body stage. Together they bound the same message from both sides: invariants structure the phase space, and actuators — massless but bounded — move those invariants.

## 14. Conclusions

- PD-controlled laser stationkeeping holds |r − L4| ≤ 7.5e-07 for all t > T/4 from an initial offset of 1.1·10⁻³ — the 2e-4 acceptance tolerance is beaten by ≈ 270×.
- Free drift never converges: the identical initial state keeps a floor of 0.0041 and a tadpole extent up to 0.026 — a contrast of ≈ 5500× with the controlled bound.
- The photon ceiling is never touched: control saturation fraction 0.0; peak demand 0.0051 (= 1.4·10⁻⁵ m/s², 20.7 kW equivalent) is 48× below the ceiling 0.2443 set by 1 MW on 10 kg.
- The PD gain plane (17 × 17, K_p 0.5–512, K_d 0.5–32) brackets the operating point (4, 4): late bounds span 0 to 123.3, and the operating point holds 1.75·10⁻⁵ with zero saturation.
- Jacobi pumping is strictly monotone: net ΔC_J = 1063.51 over T = 30 with the largest single-step increase −0.0604 — the laser demonstrably moves the invariant C_J = 2Ω − v².
- The SI power table prices the highway: Δv ∈ {10, 50, 100, 500} m/s over 30 days on 100 kg costs 57.8 kW … 2.89 MW of beam power — one 1 MW transmitter covers stationkeeping with headroom for orbit raising.

## 15. The monograph and its renditions

The complete monograph of this study exists in four renditions — Russian and English are separate documents, each in a typeset PDF and an editable DOCX:

| Rendition | Path |
|---|---|
| Monograph (English, PDF) | `monograph/monograph_EN.pdf` |
| Monograph (English, DOCX) | `monograph/monograph_EN.docx` |
| Monograph (Russian, PDF) | `monograph/monograph_RU.pdf` |
| Monograph (Russian, DOCX) | `monograph/monograph_RU.docx` |
| Reading-room copy | `publications/pdf/TRX-12-laser-light-sail_EN.pdf` · `publications/pdf/TRX-12-laser-light-sail_RU.pdf` |
| HTML source | `publications/html/TRX-12-laser-light-sail.html` |

**Monograph abstract.** This monograph treats a photon light sail in the Earth–Moon circular restricted three-body problem as an actuated libration-point system: a 1 MW laser pushes a 10 kg sail with photon thrust a_L = 2P/(cm), capped at the dimensionless ceiling a_max = 0.2443, and a proportional-derivative beam-steering law points the thrust. Two operations of the laser highway are verified. Stationkeeping: starting 1.1·10⁻³ away from the linearly stable L4 point, the controlled sail converges to |r − L4| ≤ 7.5e-07 for all t > T/4 (T = 100, ≈ 434 days) while using the photon ceiling 0% of the time (peak demand 0.0051, headroom 48×); the same initial state without control never comes closer than 0.0041 — a contrast of ≈ 5500×. Orbit raising: open-loop thrust along velocity pumps the Jacobi constant strictly monotonically, net ΔC_J = 1063.51 over T = 30 with the largest single-step increase at −0.06. A 17 × 17 PD gain-plane sweep brackets the operating point (4, 4), and an SI power table (57.8 kW … 2.89 MW per 100 kg and 30 days) closes the model to engineering numbers.

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
| `t` | 300 | 0 … 40 |
| `x` | 300 | 0.488849414 … 0.487849416 |
| `y` | 300 | 0.866525404 … 0.86602541 |
| `dist_ctrl` | 300 | 0.001118034 … 6.4000e-09 |
| `dist_free` | 300 | 0.001118034 … 0.0140711938 |
| `CJ_pump` | 400 | -7.664530578 … -167.2118233 |

**Reproduction matrix**

| Command | What it does |
|---|---|
| `python3 research/TRX-12-laser-light-sail/code/trx12_laser_light_sail.py` | full run: physics + acceptance checks (41.4 s) |
| `python3 research/TRX-12-laser-light-sail/code/trx12_laser_light_sail.py --smoke` | CI guard: same checks, seconds-scale settings |
| `python3 research/TRX-12-laser-light-sail/code/trx12_laser_light_sail.py --figures` | regenerates the 300-dpi figure set |
| `make research-smoke` | all twelve studies in smoke mode |
| `make research-figures` | all twelve studies + figure sets |

## 17. Cross-links within the program

- **TRX-01** is the perturbative twin: the same laser acts on the *primaries* there and on the *spacecraft* here.
- **TRX-10** supplies the secular transport machinery (Kozai–Lidov) that a laser highway would exploit for larger transfers.
- **TRX-11** covers the extreme mass regime of the same three-body stage.

## 18. Inside the script

The executable is a single deterministic file, `code/trx12_laser_light_sail.py`, ~pure `numpy`/`scipy` with no network access and no random state beyond fixed seeds. One run executes the full physics of the study, evaluates every registered acceptance check against its committed target and tolerance, and writes the JSON protocol — the same file quoted in §9.

| Mode | Invocation | What happens |
|---|---|---|
| Full | `python3 code/trx12_laser_light_sail.py` | complete experiment, all checks, JSON protocol (41.4 s) |
| Smoke | `python3 code/trx12_laser_light_sail.py --smoke` | identical acceptance logic at seconds-scale settings — the CI mode |
| Figures | `python3 code/trx12_laser_light_sail.py --figures` | regenerates the schematic + the four 300-dpi PNG panels |

**Outputs per run**

| File | Produced by | Content |
|---|---|---|
| `results/trx12_results.json` | every mode | status, checks (value/target/tol/unit/pass/note), series, meta |
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
| Previous study | TRX-011 |
| Next study | TRX-012 |

## 21. Notation

| Symbol | Meaning |
|---|---|
| x, y | sail coordinates in the rotating frame |
| ẋ, ẏ | sail velocities in the rotating frame |
| Ω | effective potential, Ω = ½(x²+y²) + (1−μ)/r₁ + μ/r₂ |
| r₁, r₂ | distances to Earth and Moon |
| μ | mass parameter, Earth–Moon: 0.0121505856 |
| P, m | beam power and sail mass (1 MW, 10 kg) |
| a_L | photon thrust acceleration, a_L = 2P/(cm)·û |
| a_max | photon-thrust ceiling, 0.2443 dimensionless |
| K_p, K_d | proportional and derivative gains (4, 4) |
| C_J | Jacobi constant |
| T | integration span (100 keep · 30 pump · 60 per gain cell) |

## 22. References

1. Marx, G. (1966). *Interstellar vehicle propelled by terrestrial laser beam.* Nature 211, 22–23.
2. Redding, J. L. (1967). *Interstellar travel via multi-stage photon rockets.* Nature 213, 588–590.
3. Forward, R. L. (1984). *Roundtrip interstellar travel using laser-pushed lightsails.* Journal of Spacecraft and Rockets 21, 187–195.
4. Simmons, J. F. L., McDonald, A. J. C., Ward, J. C. (1985). *The restricted three-body problem with radiation pressure.* Celestial Mechanics 35, 145–187.
5. McInnes, C. R. (1999). *Solar Sailing: Technology, Dynamics and Mission Applications.* Springer-Praxis, Chichester.
6. Vulpetti, G., Johnson, L., Matloff, G. L. (2008). *Solar Sails: A Novel Approach to Interplanetary Flight.* Springer, New York.
7. Baoyin, H., McInnes, C. R. (2006). *Solar sail halo orbits at the Sun–Earth artificial L1 point.* Celestial Mechanics and Dynamical Astronomy 94, 301–316.
8. Simo, J., McInnes, C. R. (2009). *Solar sail trajectories at the Earth-Moon Lagrange points.* 59th International Astronautical Congress, IAC-09.C1.6.13.
9. Szebehely, V. (1967). *Theory of Orbits: The Restricted Problem of Three Bodies.* Academic Press, New York.

## 23. Glossary

| Term | Definition |
|---|---|
| CR3BP | circular restricted three-body problem: two primaries on circular orbits plus a massless particle |
| Libration point | equilibrium of the effective potential in the rotating frame (L1…L5) |
| L4/L5 | triangular (equilateral) libration points, linearly stable for μ < μ_Routh ≈ 0.03852 |
| Tadpole orbit | libration orbit encircling L4 or L5 without leaving its lobe |
| Light sail | mirrored spacecraft propelled by photon momentum flux P/c |
| Photon ceiling a_max | thrust limit a_max = 2P/(cm); 0.2443 dimensionless for 1 MW on 10 kg |
| PD beam-steering law | control u = −K_p(r − r_L4) − K_d·v that points the photon thrust |
| Stationkeeping | holding a spacecraft within a tolerance of a nominal libration point |
| Jacobi constant C_J | the single integral of the planar restricted problem, C_J = 2Ω − v² |
| Invariant manifold | set of orbits sharing a C_J level; the ladder the laser climbs |

## 24. Appendix A. Full parameter table

| Symbol | Value | Role |
|---|---|---|
| μ | 0.0121505856 | mass parameter (Earth–Moon) |
| LU, TU | 3.844·10⁸ m, 3.752·10⁵ s | canonical units (GM = 1; month = 2π ≈ 27.3 days) |
| P, m | 1 MW, 10 kg | transmitter power and sail mass |
| a_max | 0.2443 (= 6.67·10⁻⁴ m/s²) | photon ceiling 2P/(cm) in LU/TU² |
| K_p, K_d | 4, 4 | PD beam-steering gains |
| start state | L4 + (1e-3, 5e-4), v = (2e-4, −1e-4) | initial offset 1.118·10⁻³ |
| T | 100 · 30 · 60 | spans: stationkeeping · pumping · per gain cell |
| rtol, atol | 1e-11 | DOP853 tolerances (max_step 0.1, 0.02 pumping) |
| pumping start | r₀ = 0.10, v = 1.05 v_circ | eccentric orbit about Earth, full thrust along v |
| power table | Δv ∈ {10, 50, 100, 500} m/s, 100 kg, 30 days | P = m·a·c/2 → 57.8 kW … 2.89 MW |

**Protocol-level parameter snapshot** (`results` JSON, `meta` block):

| Key | Value |
|---|---|
| `equations` | `["x'' - 2y' = dOmega/dx + a_Lx ;  y'' + 2x' = dOmega/dy + a_Ly", "a_L = 2P/(c m) ;  C_J = 2*Omega - v^2 (decreases under along-velocity thrust)"]` |
| `a_max_dimensionless` | `0.2443050878901552` |
| `power_table_100kg_30days` | `[{"dv_m_s": 10.0, "power_W": 57830.33526234568}, {"dv_m_s": 50.0, "power_W": 289151.67631172837}, {"dv_m_s": 100.0, "power_W": 578303.3526234567}, {"dv_m_s": 500.0, "power_W": 2891516.7631172836}]` |
| `note` | `"Earth-Moon L4 is linearly stable, so free drift oscillates forever; laser stationkeeping holds a much tighter tolerance"` |

## 25. Appendix B. BibTeX

```bibtex
@article{marx1966,
  author  = {Marx, Ga},
  title   = {Interstellar vehicle propelled by terrestrial laser beam},
  journal = {Nature},
  year    = {1966}, volume = {211}, pages = {22--23}}

@article{redding1967,
  author  = {Redding, J. L.},
  title   = {Interstellar travel via multi-stage photon rockets},
  journal = {Nature},
  year    = {1967}, volume = {213}, pages = {588--590}}

@article{forward1984,
  author  = {Forward, Robert L.},
  title   = {Roundtrip interstellar travel using laser-pushed lightsails},
  journal = {Journal of Spacecraft and Rockets},
  year    = {1984}, volume = {21}, pages = {187--195}}

@book{mcinnes1999,
  author    = {McInnes, Colin R.},
  title     = {Solar Sailing: Technology, Dynamics and Mission Applications},
  publisher = {Springer-Praxis}, year = {1999}}
```

## 26. How to cite

Cite the repository through [`CITATION.cff`](../../CITATION.cff) (DOI 10.5281/zenodo.21825394, version 1.0.0); this study is part of the TRIVORTEX Research Program. If you cite the study alone, name the monograph rendition you used and attach the JSON protocol of the run you reproduced.

```bibtex
@misc{trivortextrx122026isaev,
  author       = {Isaev, Iskhak Khamzatovich},
  title        = {Laser Highway: Light-Sail Stationkeeping at L4/L5 (TRIVORTEX Research Program, TRX-12)},
  year         = {2026},
  howpublished = {Zenodo},
  doi          = {10.5281/zenodo.21825394},
  url          = {https://github.com/wild8highlander/research-papers}
}
```

