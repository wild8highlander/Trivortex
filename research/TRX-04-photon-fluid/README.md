# TRX-04 — Photon Fluid: Three Kerr Solitons (Spatial, 2-D)

*TRIVORTEX Research Program · version 1.0.0 · study TRX-04 of 12*

Three laser beams co-propagating in a focusing Kerr medium behave as a **photon fluid**: each beam is a spatial soliton of the nonlinear Schrödinger equation, and pairs of beams exchange conservative two-body forces whose sign is set by the relative phase — in-phase beams attract, anti-phase beams repel — with the exponential profile **V(r) = ∓U·e^(−r/w)**. The in-phase triplet realizes an optical Lagrange central configuration: an equilateral beam triangle of side a = 3 rotates rigidly at **ω = e^(−3/2) = 0.223130160**, the exponential-force counterpart of the Newtonian ω² = 3Gm/a³ of Theorem 3.1. The study verifies the choreography to machine precision: the triangle stays equilateral to 1.8e-08 over three full rotations, the measured rotation rate matches the analytic law to 1.1×10⁻¹¹, energy and angular momentum are conserved to 4.7e-16 and 2.2e-15, the anti-phase trio expands cleanly to 23.476, and an in-phase binary stays bound with a precessing orbit — an optical three-body scattering table closed by 9/9 checks PASS.

> **Edition 1.0.0.** This README is part of the first public release of the TRIVORTEX research program. The study ships as an executable script, a committed JSON protocol, four 300-dpi figures, a schematic and a bilingual monograph in four renditions (Russian and English, each in PDF and DOCX).

**At a glance**

| Aspect | Value |
|---|---|
| Block | Laser optics — study 04 of 12 |
| Model | three spatial Kerr solitons with phase-signed exponential pair force (U = w = m = 1) |
| Key invariant | total energy of all three runs (drift ≤ 3.0e-12; rotation 4.7e-16) |
| Headline result | rigid rotation of the beam triangle at ω = 0.223130160 vs analytic to 1.1×10⁻¹¹; rigidity 1.8e-08 |
| Verification | 9/9 checks PASS (full mode) |
| Runtime | 9.4 s recorded full run (with --figures) · smoke < 20 s |

| Field | Value |
|---|---|
| Study | `TRX-04` (TRX-04-photon-fluid) |
| Program | TRIVORTEX — The Three-Body Problem in the Vortex Model |
| Author | Isaev Iskhak Khamzatovich (ORCID `0009-0003-7299-0701`) |
| DOI | [10.5281/zenodo.21825394](https://doi.org/10.5281/zenodo.21825394) |
| Version | 1.0.0 — first public release |
| Code | `research/TRX-04-photon-fluid/code/trx04_photon_fluid.py` |
| Protocol | `research/TRX-04-photon-fluid/results/trx04_results.json` |
| License | `LicenseRef-Proprietary-Wild8Highlander-1.0` |

## 1. Mission

Spatial solitons turn a nonlinear optical medium into a collisionless photon gas with genuine two-body forces. This makes optics a unique laboratory for the three-body problem: the "bodies" are beams of light, the force law is written by the medium, and the sign of every pairwise force is set by a phase dial. This study asks whether the crown jewel of the classical three-body problem — the rigidly rotating equilateral triangle of Lagrange — survives in this optical setting, and answers it quantitatively: the equilateral configuration is a central configuration for the exponential Kerr force exactly as it is for Newtonian gravity, with the rotation law ω² = 3Ue^(−a/w)/(maw) = 0.049787 at the preset side a = 3.

The verification program is deliberately strict. The rotating triangle must stay equilateral to 1e-6 over three full turns (achieved 1.8e-08) and its measured rotation rate must reproduce the analytic ω = 0.223130160 within 1e-8 (achieved agreement to 1.1×10⁻¹¹). Energy must be conserved in all three runs — rotation, repulsion, binary — to 1e-10, and angular momentum to the same level (achieved 4.7e-16, 3.6e-16, 3.0e-12 and 2.2e-15). The anti-phase trio must not collapse and must expand (final separation 23.476 from initial 3.000), and the in-phase binary must remain inside the bound window separation ∈ [0.5, 6] over t = 80 (observed range [0.635, 3.000]). All nine checks PASS in the recorded full run, so the optical three-body table can be quoted as verified fact rather than simulation folklore.

## 2. Introduction and historical context

Self-trapping of light is as old as nonlinear optics. Askar'yan proposed in 1962 that an intense beam could raise the refractive index enough to guide itself, and Chiao, Garmire and Townes demonstrated self-trapping of optical beams in 1964 — the experiment that made "a beam of light behaving as a particle of light" concrete. The pure Kerr nonlinearity, however, makes the two-dimensional self-trapping problem critical (the Townes collapse), so stable spatial solitons in real media rely on saturation — photorefractive crystals, nematic liquid crystals, atomic vapors. The concept that survives in every such medium is the same: a beam that carries itself like a particle.

The next step was the realization that two such light particles exert forces on each other. Reynaud and Barthelemy (1990) demonstrated optically controlled interaction between two fundamental soliton beams, and Aitchison and colleagues (1991) observed spatial soliton interactions directly in a nonlinear glass waveguide. The decisive control knob is the relative phase: coherent in-phase beams attract, anti-phase beams repel, and quadrature beams pass through — the phase acts as a switchable gravitational charge. Stegeman and Segev (1999) consolidated this physics in their review of optical spatial solitons and their interactions, the founding literature of beam-by-beam collision experiments.

The collective picture — many beams as a gas or fluid of mutually attracting particles — was pushed by Snyder, Mitchell and Kivshar (1995), who unified the self-trapping of light and matter waves, and by Bialynicki-Birula's photon-wave description of light as a many-body wave system. Today the umbrella term is quantum fluids of light, reviewed by Carusotto and Ciuti (2013); nematicons in nematic liquid crystals (Assanto and Peccianti, 2012) remain the cleanest classical realization of long-range, phase-tunable beam forces. Within this literature the three-beam triangle is the simplest genuinely collective object: every member feels both others, and no pairwise subproblem predicts the outcome.

That is precisely the situation Lagrange analyzed in 1772, when he found that three bodies placed at the vertices of an equilateral triangle and given the right velocities rotate rigidly forever — the only non-collinear central configuration of the Newtonian three-body problem and the content of Theorem 3.1 in the TRIVORTEX monograph. This study transplants that construction into the photon fluid: the exponential Kerr force replaces the Newtonian 1/r force, the phase replaces the mass sign, and the equilateral beam triangle replaces the celestial one. The siblings are already in place — TRX-03 in the temporal (fiber-laser) domain, TRX-05 with field zeros instead of maxima, TRX-08 with ions in a trap — making TRX-04 the spatial-optics anchor of the choreography family.

## 3. Physical system and preset

In a medium with a focusing Kerr nonlinearity the refractive index grows with intensity, so a bright beam digs its own waveguide and propagates without diffracting — a spatial soliton of the equation iA_z + ½∇²A + |A|²A = 0. Two such beams whose tails overlap exert forces on one another through the shared nonlinear index: coherent, in-phase beams interfere constructively in the overlap region and attract, while anti-phase beams interfere destructively and repel. In the particle approximation — the working horse of this study — each beam is replaced by a point body of mass m moving in the transverse plane, and the pair interaction is the exponential law V_pm(r) = −Ue^(−r/w) (in phase) and V_ap(r) = +Ue^(−r/w) (anti-phase), with force magnitude (U/w)·e^(−r/w). The length w is the interaction scale (beam-waist unit) and U the potential depth.

The equilateral triangle is special for any central force between equal members. At the vertices of an equilateral triangle of side a each beam feels two edge forces of magnitude F = (U/w)e^(−a/w) directed along the sides; their resultant is √3·F and points exactly at the centroid, at distance r_c = a/√3. The balance √3·F = mω²r_c then fixes the rigid rotation rate ω² = 3Ue^(−a/w)/(maw) — the same central-configuration balance that produces the Lagrange equilateral solution in the Newtonian problem, where ω² = 3Gm/a³. Sign flips matter as much as magnitudes: switching one phase to anti-phase converts one edge force from attraction to repulsion, the resultant no longer points at the centroid, and the rigid rotation is destroyed — the anti-phase trio simply expands. A pair of in-phase beams with negative relative energy forms a bound binary whose orbit precesses, because the exponential force is not inverse-square.

| Parameter | Value | Meaning |
|---|---|---|
| U, w, m | 1, 1, 1 | potential depth, interaction scale, soliton mass (natural units) |
| a | 3 | triangle side of the rotation run; operating point |
| r_c | a/√3 = 1.732051 | orbit radius of each beam about the centroid |
| ω | e^(−3/2) = 0.223130160 | analytic rotation rate (ω² = e^(−3) = 0.049787) |
| T_rotation | 84.4778 = 3·2π/ω | rotation run: three full turns |
| anti-phase run | same geometry, zero velocities, T = 40 | repulsive expansion test |
| binary | r₀ = 3, v_b = ±0.15, E_rel = −0.027, T = 80 | in-phase bound-pair run |
| integrator | DOP853, rtol = atol = 1e-12, max_step = 0.1 | all runs, dense output |

**Model assumptions**

- Particle approximation: each beam is a point body in the transverse plane; its transverse profile is assumed rigid (fundamental solitons, no deformation or radiation shedding).
- The pair force is the isotropic exponential law ∓(U/w)e^(−r/w) — conservative and instantaneous; retardation, absorption and medium dynamics are neglected.
- Planar 2-D model: all motion is in the transverse plane; propagation along z is uniform and does not couple back into the dynamics.
- Equal members: identical potential depth U, interaction scale w and mass m for all beams; the optical phase enters only as the pair sign s = ±1 (fixed in phase or anti-phase, not a dynamical variable).
- The focusing NLS (E1) is documented context; the dynamics are integrated at the particle level, and the particle approximation is assumed valid for well-separated beams (r ≳ 2w).
- Integrator precision: DOP853 with rtol = atol = 1e-12 and max_step = 0.1; conservation errors reported are those of the recorded runs on the reference machine.

## 4. Governing equations

(E1) Focusing nonlinear Schrödinger equation — the underlying field equation (documented context):

$$i\,\frac{\partial A}{\partial z} + \tfrac{1}{2}\nabla_\perp^2 A + |A|^2 A = 0$$

(E2) Pair potentials of two spatial solitons: in phase (attraction) and anti-phase (repulsion):

$$V_{\rm pm}(r) = -U\,e^{-r/w}, \qquad V_{\rm ap}(r) = +U\,e^{-r/w}$$

(E3) Planar equations of motion of the N photon-fluid bodies with all-pairs forces:

$$m\,\ddot{\mathbf{r}}_k = \sum_{l\neq k} s\,\frac{U}{w}\,e^{-r_{kl}/w}\,\frac{\mathbf{r}_k-\mathbf{r}_l}{r_{kl}}, \quad s=-1\ \text{(in phase)},\ s=+1\ \text{(anti-phase)}$$

(E4) Rotation rate of the rigidly rotating equilateral beam triangle (Lagrange central configuration):

$$\omega^2 = \frac{3U\,e^{-a/w}}{m\,a\,w} \;\left(= e^{-3} = 0.049787\ \text{at the preset}\right)$$

(E5) Conserved invariants of the planar model: total energy and angular momentum:

$$E = \sum_k \tfrac{1}{2}m\,|\dot{\mathbf{r}}_k|^2 + \sum_{k<l} s\,U\,e^{-r_{kl}/w}, \qquad L_z = \sum_k m\,(x_k\dot{y}_k - y_k\dot{x}_k)$$

(E6) Bound-state condition of the in-phase binary at launch separation r₀ (preset: 0.0225 − 0.049787 = −0.027):

$$E_{\rm rel} = m\,v_b^2 - U\,e^{-r_0/w} < 0 \;\Leftrightarrow\; v_b < \sqrt{U\,e^{-r_0/w}} = e^{-3/2} \approx 0.223130$$

## 5. Scheme

![TRX-04 scheme — photon fluid: three in-phase Kerr solitons in a focusing medium (left): the attractive pair forces along the triangle edges supply the centripetal balance mω²r_c of the rigidly rotating Lagrange beam triangle; the pair interaction (right): in-phase attraction V = −U·exp(−r/w), anti-phase repulsion V = +U·exp(−r/w), the operating point a = 3 and the binary bound-state condition.](figures/scheme_trx04.svg)

*TRX-04 scheme — photon fluid: three in-phase Kerr solitons in a focusing medium (left): the attractive pair forces along the triangle edges supply the centripetal balance mω²r_c of the rigidly rotating Lagrange beam triangle; the pair interaction (right): in-phase attraction V = −U·exp(−r/w), anti-phase repulsion V = +U·exp(−r/w), the operating point a = 3 and the binary bound-state condition..*

The diagram encodes the following elements:

- **Focusing Kerr medium (left panel)** — top view of the nonlinear medium; the beams propagate along z, out of the page
- **Three beam spots** — in-phase spatial solitons at the vertices of an equilateral triangle of side a = 3
- **Gold arrows along the edges** — attractive pair forces that supply the centripetal balance mω²r_c about the centroid
- **Rotation arrow, ω = 0.2231** — rigid rotation of the Lagrange beam triangle; the dashed radius marks r_c = a/√3
- **Pair-energy curves (right panel)** — in-phase attraction V = −U·exp(−r/w) against anti-phase repulsion V = +U·exp(−r/w) above the zero line V = 0 (free beams)
- **Operating point a = 3 and info boxes** — force (U/w)·exp(−3) = 0.0498, rotation law ω² = 3U·exp(−a/w)/(maw), and the binary note with escape threshold 0.2231 for the preset v_b = 0.15

## 6. Mapping to TRIVORTEX

Within the TRIVORTEX program this study is the spatial-optics realization of Theorem 3.1. The three Kerr solitons play the three gravitating bodies; the rotating beam triangle is the Lagrange equilateral solution; and the measured rotation rate checks the central-configuration balance exactly as the Newtonian ω² = 3Gm/a³ does, with the exponential force ω² = 3Ue^(−a/w)/(maw) = 0.049787 at the preset. The relative optical phase plays the role of the circulation sign in the vortex model: in-phase is the equal-circulation, mutually attracting case that supports the choreography, anti-phase is the repulsive sign that destroys it — the same sign hierarchy that separates bound from unbound vortex pairs. The precessing binary adds the two-body layer of the same mapping: eccentric orbits, fixed turning points, conserved E and L_z, but a non-Kepler force law. TRX-03 repeats this structure on a line with temporal solitons, TRX-05 replaces field maxima by field zeros and recovers Kirchhoff's vortex equations, and TRX-08 trades photons for ions; together they demonstrate that the choreography sequence — pair law, central configuration, invariants — is portable across optics, fluids and celestial mechanics.

| Quantity in this study | TRIVORTEX analog | Comment |
|---|---|---|
| Three Kerr solitons | three gravitating bodies | same central-configuration problem |
| Exponential attraction e^(−r/w) | Newtonian 1/r attraction | force law changes, geometry does not |
| Rotating beam triangle | Lagrange equilateral solution | identical balance structure, Theorem 3.1 |
| Relative phase (in/anti) | circulation sign in the vortex model | attraction ↔ repulsion switch |
| Rotation law ω² = 3Ue^(−a/w)/(maw) | ω² = 3Gm/a³ for point masses | third-law-type verification target |
| In-phase binary with precession | eccentric two-body orbit | non-Kepler force, same invariant bookkeeping |

## 7. Dimensionless formulation

All quantities are dimensionless in beam units: lengths in units of the interaction scale w (the beam-waist unit), energies in units of the potential depth U, masses in units of the soliton mass m, and times in units of w·√(m/U). At the preset U = w = m = 1 every quantity is a plain number: the rotation rate ω = 0.223130160 is dimensionless, the triangle side is a = 3, and the binary launch velocity is v_b = 0.15.

## 8. Numerical method

The model is a planar N-body system with the interleaved state layout [x₁, y₁, vx₁, vy₁, …]. At the preset U = w = m = 1 the triangle side is a = 3, the initial positions sit on the circle r_c = a/√3 = 1.732051, and the initial velocities are the rigid-rotation field ω·r_c with the analytic rate ω = √(3Ue^(−a/w)/(maw)) = 0.22313016014842985. All runs integrate the equations of motion (E3) with the explicit Dormand–Prince 8(5,3) scheme (scipy DOP853, rtol = atol = 1e-12, max_step = 0.1, dense output for uniform sampling). The rotation run lasts T = 3·2π/ω = 84.4778 — three full turns — sampled at 2400 points.

Diagnostics are exact and independent of the integrator's internal steps. The equilateral rigidity is the maximum over time of |d(t) − a|/a for all three pairwise distances. The rotation rate is measured by unwrapping the polar angle of beam 1 about the instantaneous centroid and fitting a straight line in time — the slope is the recorded rotation rate. The total energy (E5) and the angular momentum L_z are evaluated on ~300 uniformly spaced samples per run. The anti-phase run starts from the same triangle at rest and integrates to T = 40; the binary run launches two beams at (±1.5, 0) with transverse velocities ∓0.15 and integrates to T = 80, both at the same tolerances.

Every acceptance check is registered in the JSON protocol with its value, target, tolerance, unit and pass flag; the recorded full run passes 9/9. The --figures mode adds the scheme SVG and four 300-DPI PNG panels together with two parameter sweeps stored in the protocol: the side sweep (seven sides a = 2.0…8.0, each with a full re-integration over one rotation period and a fresh slope measurement) and the binary velocity sweep (sixteen launch velocities v_b = 0.06…0.34 over T = 40). No network access and no stochastic seeds are used; the run is bit-reproducible on the reference machine.

## 9. Verification protocol and acceptance checks

Every check is registered before the run: target, tolerance and unit are committed in the protocol, not chosen after the fact.

| Check | Target | Tolerance |
|---|---|---|
| Equilateral deviation over 3 rotations (max rel. side change) | 0 | 1e-6 |
| Measured rotation rate vs analytic ω = 0.223130160 | equal | 1e-8 |
| Energy drift, rotation run (t = 84.4778) | 0 | 1e-10 |
| Angular-momentum drift, rotation run | 0 | 1e-10 |
| Anti-phase trio: min pairwise distance ≥ 0.95a | yes | exact |
| Anti-phase trio expands (final > initial separation) | yes | exact |
| Energy drift, anti-phase run (t = 40) | 0 | 1e-10 |
| Binary: separation within [0.5, 6] over t = 80 | yes | exact |
| Energy drift, binary run (t = 80) | 0 | 1e-10 |

**Recorded verification run** (mode: smoke, status: **PASS**, 9/9 checks)

| Check | Recorded value | Target | Tolerance | Unit | Verdict |
|---|---|---|---|---|---|
| `triangle_equilateral_deviation` | 4.4409e-15 | 0 | 1.0000e-06 | rel | PASS |
| `measured_rotation_rate` | 0.2231301601 | 0.2231301601 | 1.0000e-08 | 1/time | PASS |
| `energy_conservation_rotation` | 2.2204e-16 | 0 | 1.0000e-10 | energy | PASS |
| `angular_momentum_conservation` | 8.8818e-16 | 0 | 1.0000e-10 | ang mom | PASS |
| `antiphase_no_collapse` | 1 | 1 | 1.0000e-12 | bool | PASS |
| `antiphase_expands` | 1 | 1 | 1.0000e-12 | bool | PASS |
| `energy_conservation_repulsion` | 3.0531e-16 | 0 | 1.0000e-10 | energy | PASS |
| `binary_stays_bound` | 1 | 1 | 1.0000e-12 | bool | PASS |
| `binary_energy_conservation` | 1.7707e-12 | 0 | 1.0000e-10 | energy | PASS |

**Check notes** — what each number means:

| Check | Note |
|---|---|
| `triangle_equilateral_deviation` | max side deviation over 3 rotations |
| `measured_rotation_rate` | analytic omega^2 = 3U e^(-a/w)/(m a w) -> omega = 0.223130160 |
| `antiphase_no_collapse` | min pairwise distance 3.0000 >= 0.95 a |
| `antiphase_expands` | final separation 12.545 > initial 3.000 |
| `binary_stays_bound` | separation range [0.635, 3.000] |

## 10. Figure gallery (300 dpi)

![{'cap_en': 'Model landscape: photon-fluid pair interaction and the initial beam triangle of the rotation run.', 'cap_ru': 'Ландшафт модели: парное взаимодействие фотонной жидкости и стартовый треугольник пучков вращательного прогона.', 'walk_en': 'Panel (a) shows the pair interaction landscape: in-phase attraction V = −U·e^(−r/w) (gold) against anti-phase repulsion V = +U·e^(−r/w) (red dashed) — the phase acts as an attractive/repulsive charge; the operating point a = 3 sits at force (U/w)·e^(−a/w) = 0.0498. Panel (b) shows the initial condition of the rotation run: the equilateral beam triangle with side a = 3, orbit radius r_c = a/√3 = 1.732051, and pair forces supplying the centripetal balance mω²r_c at the preset rate ω = 0.223130.', 'walk_ru': 'Панель (а) показывает ландшафт парного взаимодействия: синфазное притяжение V = −U·e^(−r/w) (золотое) против противофазного отталкивания V = +U·e^(−r/w) (красный пунктир) — фаза действует как притягивающий/отталкивающий заряд; рабочая точка a = 3 лежит при силе (U/w)·e^(−a/w) = 0.0498. Панель (б) показывает начальное условие вращательного прогона: равносторонний треугольник пучков со стороной a = 3, радиус орбиты r_c = a/√3 = 1.732051 и парные силы, создающие центростремительный баланс mω²r_c при пресетной скорости ω = 0.223130.'}](figures/fig01_photon_fluid_landscape.png)

*{'cap_en': 'Model landscape: photon-fluid pair interaction and the initial beam triangle of the rotation run.', 'cap_ru': 'Ландшафт модели: парное взаимодействие фотонной жидкости и стартовый треугольник пучков вращательного прогона.', 'walk_en': 'Panel (a) shows the pair interaction landscape: in-phase attraction V = −U·e^(−r/w) (gold) against anti-phase repulsion V = +U·e^(−r/w) (red dashed) — the phase acts as an attractive/repulsive charge; the operating point a = 3 sits at force (U/w)·e^(−a/w) = 0.0498. Panel (b) shows the initial condition of the rotation run: the equilateral beam triangle with side a = 3, orbit radius r_c = a/√3 = 1.732051, and pair forces supplying the centripetal balance mω²r_c at the preset rate ω = 0.223130.', 'walk_ru': 'Панель (а) показывает ландшафт парного взаимодействия: синфазное притяжение V = −U·e^(−r/w) (золотое) против противофазного отталкивания V = +U·e^(−r/w) (красный пунктир) — фаза действует как притягивающий/отталкивающий заряд; рабочая точка a = 3 лежит при силе (U/w)·e^(−a/w) = 0.0498. Панель (б) показывает начальное условие вращательного прогона: равносторонний треугольник пучков со стороной a = 3, радиус орбиты r_c = a/√3 = 1.732051 и парные силы, создающие центростремительный баланс mω²r_c при пресетной скорости ω = 0.223130.'}.*

![{'cap_en': 'Headline result: rigid rotation of the photon-fluid triangle over three full turns and its equilateral rigidity.', 'cap_ru': 'Главный результат: жёсткое вращение треугольника фотонной жидкости за три полных оборота и его равносторонняя жёсткость.', 'walk_en': 'Panel (a) shows the worldlines of the three beams over three full turns (T = 84.4778): circular orbits about the common centroid, the triangle carried rigidly like a solid body. Panel (b) plots the relative side deviations |d(t) − a|/a on a log scale: they never exceed 1.8e-08, a factor of about 56 inside the 1e-6 acceptance tolerance, while the measured rotation rate 0.223130160 matches the analytic ω = 0.223130160 — the optical Lagrange configuration confirmed dynamically.', 'walk_ru': 'Панель (а) показывает мировые линии трёх пучков за три полных оборота (T = 84.4778): круговые орбиты вокруг общего центроида, треугольник переносится жёстко, как твёрдое тело. Панель (б) откладывает относительные отклонения сторон |d(t) − a|/a в логарифмическом масштабе: они не превышают 1.8e-08 — примерно в 56 раз внутри допуска 1e-6, — а измеренная скорость вращения 0.223130160 совпадает с аналитической ω = 0.223130160: оптическая лагранжева конфигурация подтверждена динамически.'}](figures/fig02_triangle_rotation.png)

*{'cap_en': 'Headline result: rigid rotation of the photon-fluid triangle over three full turns and its equilateral rigidity.', 'cap_ru': 'Главный результат: жёсткое вращение треугольника фотонной жидкости за три полных оборота и его равносторонняя жёсткость.', 'walk_en': 'Panel (a) shows the worldlines of the three beams over three full turns (T = 84.4778): circular orbits about the common centroid, the triangle carried rigidly like a solid body. Panel (b) plots the relative side deviations |d(t) − a|/a on a log scale: they never exceed 1.8e-08, a factor of about 56 inside the 1e-6 acceptance tolerance, while the measured rotation rate 0.223130160 matches the analytic ω = 0.223130160 — the optical Lagrange configuration confirmed dynamically.', 'walk_ru': 'Панель (а) показывает мировые линии трёх пучков за три полных оборота (T = 84.4778): круговые орбиты вокруг общего центроида, треугольник переносится жёстко, как твёрдое тело. Панель (б) откладывает относительные отклонения сторон |d(t) − a|/a в логарифмическом масштабе: они не превышают 1.8e-08 — примерно в 56 раз внутри допуска 1e-6, — а измеренная скорость вращения 0.223130160 совпадает с аналитической ω = 0.223130160: оптическая лагранжева конфигурация подтверждена динамически.'}.*

![{'cap_en': 'Parameter sweeps: rotation rate versus triangle side and the binary bound/unbound map versus launch velocity.', 'cap_ru': 'Развёртки параметров: скорость вращения в зависимости от стороны треугольника и карта связанности бинарной пары в зависимости от стартовой скорости.', 'walk_en': 'Panel (a) sweeps the triangle side: the analytic Kerr law ω(a) = √(3Ue^(−a/w)/(maw)) runs from 0.450558 at a = 2 through the preset 0.223130 at a = 3 down to 0.011216 at a = 8, numeric DOP853 re-runs sit on the curve at all seven grid sides, and the Newtonian 1/r reference (0.333333 at the preset) decays markedly slower — 0.076547 at a = 8 against the Kerr 0.011216. Panel (b) maps the binary outcome versus launch velocity: max separation stays at 3.0 for v_b ≤ 0.26 and grows to 7.7515, 13.2491, 16.4935 and 19.1521 for v_b = 0.28–0.34 over T = 40, bracketing the analytic escape threshold v_b* = e^(−3/2) = 0.223130.', 'walk_ru': 'Панель (а) развёртывает сторону треугольника: аналитический керровский закон ω(a) = √(3Ue^(−a/w)/(maw)) идёт от 0.450558 при a = 2 через пресет 0.223130 при a = 3 до 0.011216 при a = 8, численные повторные прогоны DOP853 ложатся на кривую во всех семи точках сетки, а ньютоновская эталонная кривая 1/r (0.333333 в пресете) спадает заметно медленнее — 0.076547 при a = 8 против керровских 0.011216. Панель (б) картирует исход для бинарной пары в зависимости от стартовой скорости: максимальное расстояние остаётся 3.0 при v_b ≤ 0.26 и растёт до 7.7515, 13.2491, 16.4935 и 19.1521 при v_b = 0.28–0.34 за T = 40, обрамляя аналитический порог убегания v_b* = e^(−3/2) = 0.223130.'}](figures/fig03_parameter_sweeps.png)

*{'cap_en': 'Parameter sweeps: rotation rate versus triangle side and the binary bound/unbound map versus launch velocity.', 'cap_ru': 'Развёртки параметров: скорость вращения в зависимости от стороны треугольника и карта связанности бинарной пары в зависимости от стартовой скорости.', 'walk_en': 'Panel (a) sweeps the triangle side: the analytic Kerr law ω(a) = √(3Ue^(−a/w)/(maw)) runs from 0.450558 at a = 2 through the preset 0.223130 at a = 3 down to 0.011216 at a = 8, numeric DOP853 re-runs sit on the curve at all seven grid sides, and the Newtonian 1/r reference (0.333333 at the preset) decays markedly slower — 0.076547 at a = 8 against the Kerr 0.011216. Panel (b) maps the binary outcome versus launch velocity: max separation stays at 3.0 for v_b ≤ 0.26 and grows to 7.7515, 13.2491, 16.4935 and 19.1521 for v_b = 0.28–0.34 over T = 40, bracketing the analytic escape threshold v_b* = e^(−3/2) = 0.223130.', 'walk_ru': 'Панель (а) развёртывает сторону треугольника: аналитический керровский закон ω(a) = √(3Ue^(−a/w)/(maw)) идёт от 0.450558 при a = 2 через пресет 0.223130 при a = 3 до 0.011216 при a = 8, численные повторные прогоны DOP853 ложатся на кривую во всех семи точках сетки, а ньютоновская эталонная кривая 1/r (0.333333 в пресете) спадает заметно медленнее — 0.076547 при a = 8 против керровских 0.011216. Панель (б) картирует исход для бинарной пары в зависимости от стартовой скорости: максимальное расстояние остаётся 3.0 при v_b ≤ 0.26 и растёт до 7.7515, 13.2491, 16.4935 и 19.1521 при v_b = 0.28–0.34 за T = 40, обрамляя аналитический порог убегания v_b*= e^(−3/2) = 0.223130.'}.*

![{'cap_en': 'Dynamics and invariants: precessing bound orbit of the in-phase binary and the energy-drift bookkeeping of all three runs.', 'cap_ru': 'Динамика и инварианты: прецессирующая связанная орбита синфазной бинарной пары и учёт дрейфа энергии во всех трёх прогонах.', 'walk_en': 'Panel (a) shows the precessing bound orbit of the in-phase binary (launch separation 3, transverse velocity 0.15, E_rel = −0.027 < 0, T = 80): the separation breathes inside [0.635, 3.000] while the orbit axis slowly rotates — the signature of a non-inverse-square force. Panel (b) tracks the energy drift |E(t) − E(0)| of the three runs on a log scale: 4.7e-16 (rotation), 3.6e-16 (anti-phase trio) and 3.0e-12 (binary), all far below the 1e-10 acceptance tolerance.', 'walk_ru': 'Панель (а) показывает прецессирующую связанную орбиту синфазной бинарной пары (стартовое расстояние 3, поперечная скорость 0.15, E_rel = −0.027 < 0, T = 80): расстояние дышит внутри [0.635, 3.000], а ось орбиты медленно поворачивается — подпись не обратно-квадратичной силы. Панель (б) отслеживает дрейф энергии |E(t) − E(0)| трёх прогонов в логарифмическом масштабе: 4.7e-16 (вращение), 3.6e-16 (противофазное трио) и 3.0e-12 (бинарная пара) — всё далеко ниже допуска 1e-10.'}](figures/fig04_binary_dynamics_invariants.png)

*{'cap_en': 'Dynamics and invariants: precessing bound orbit of the in-phase binary and the energy-drift bookkeeping of all three runs.', 'cap_ru': 'Динамика и инварианты: прецессирующая связанная орбита синфазной бинарной пары и учёт дрейфа энергии во всех трёх прогонах.', 'walk_en': 'Panel (a) shows the precessing bound orbit of the in-phase binary (launch separation 3, transverse velocity 0.15, E_rel = −0.027 < 0, T = 80): the separation breathes inside [0.635, 3.000] while the orbit axis slowly rotates — the signature of a non-inverse-square force. Panel (b) tracks the energy drift |E(t) − E(0)| of the three runs on a log scale: 4.7e-16 (rotation), 3.6e-16 (anti-phase trio) and 3.0e-12 (binary), all far below the 1e-10 acceptance tolerance.', 'walk_ru': 'Панель (а) показывает прецессирующую связанную орбиту синфазной бинарной пары (стартовое расстояние 3, поперечная скорость 0.15, E_rel = −0.027 < 0, T = 80): расстояние дышит внутри [0.635, 3.000], а ось орбиты медленно поворачивается — подпись не обратно-квадратичной силы. Панель (б) отслеживает дрейф энергии |E(t) − E(0)| трёх прогонов в логарифмическом масштабе: 4.7e-16 (вращение), 3.6e-16 (противофазное трио) и 3.0e-12 (бинарная пара) — всё далеко ниже допуска 1e-10.'}.*

## 11. Results (full run)

```text
triangle_equilateral_deviation   = 1.8e-08
measured_rotation_rate           = 2.231302e-01 (target 0.22313016014842985)
energy_conservation_rotation     = 4.7e-16
angular_momentum_conservation    = 2.2e-15
antiphase_no_collapse            = PASS (min distance 3.0000 >= 0.95 a)
antiphase_expands                = PASS (final separation 23.476 > initial 3.000)
energy_conservation_repulsion    = 3.6e-16
binary_stays_bound               = PASS (separation range [0.635, 3.000])
binary_energy_conservation       = 3.0e-12
status: PASS (9/9)
```

## 12. Analysis

**Rigid rotation.** Over three full turns (T = 84.4778) the triangle stays equilateral to 1.8e-08 in relative side deviation — a factor of about 56 inside the 1e-6 acceptance tolerance (fig02b). The measured rotation rate 0.223130160 reproduces the analytic ω = 0.223130160 to 1.1×10⁻¹¹ in absolute terms, versus a tolerance of 1e-8 — the central-configuration balance (E4) is not merely satisfied but satisfied at round-off level. The invariants confirm the cleanliness of the run: energy drift 4.7e-16 and angular-momentum drift 2.2e-15, both orders of magnitude below the 1e-10 gate.

**Side sweep.** The rotation law is verified as a law, not a point: re-integrating one full period at each of the seven grid sides a = 2.0, 2.5, 3.0, 4.0, 5.0, 6.5, 8.0 reproduces the analytic curve everywhere — ω from 0.450558 at a = 2 through 0.313850 (a = 2.5), 0.223130 (a = 3), 0.117204 (a = 4), 0.063583 (a = 5), 0.026342 (a = 6.5) down to 0.011216 at a = 8. The Newtonian 1/r reference rotates systematically faster at large separations: 0.333333 against the Kerr 0.223130 at the preset, and 0.076547 against 0.011216 at a = 8 — the exponential tail dies out, and the choreography slows down correspondingly (fig03a).

**Anti-phase expansion.** With all phases flipped, the same triangle at rest expands monotonically: the minimum pairwise distance never drops below 3.0000 (the initial value; the 0.95a = 2.85 floor is never approached), and the final separation reaches 23.476 at T = 40 — a clean repulsive scattering event with energy conserved to 3.6e-16. This is the sign-flip control experiment: identical geometry, identical integrator, opposite outcome — the phase, not the geometry, decides the fate of the triplet.

**Binary and bound/unbound map.** The in-phase binary with v_b = 0.15 breathes inside [0.635, 3.000] over the whole t = 80 window (fig04a) with energy drift 3.0e-12 — the largest of the three runs yet still a factor of about 33 below the 1e-10 tolerance. The velocity sweep turns the single trajectory into a map (fig03b): max separation stays at the initial 3.0 for all v_b ≤ 0.26 and jumps to 7.7515, 13.2491, 16.4935 and 19.1521 for v_b = 0.28–0.34 over T = 40. The analytic threshold v_b*= e^(−3/2) = 0.223130 sits inside the trapped band: the angular-momentum barrier keeps near-threshold launches bound for the whole observation window, so the numerically observed escape edge lies between 0.26 and 0.28 rather than exactly at v_b*.

## 13. Discussion and honest boundaries

The model is deliberately minimal: point-like beams, an isotropic exponential pair force, no retardation, no absorption, and the optical phase entering only as the sign s = ±1 of each pair. Within these assumptions every statement in this study is an exact property of the governing equations rather than a simulation of a particular experiment. The particle approximation is the standard reduction for well-separated solitons; its breakdown at near-field overlap (where beams deform, fuse or shed radiation) is outside the conservative scope here, and the natural extensions — full NLS integration of the same triangle, saturating media, unequal beams, three-dimensional geometries — would each preserve the verification style established above.

The parameter regime is chosen where the physics is clean. At the preset a = 3 the edge force is (U/w)e^(−3) = 0.049787 — weak, so the beams are well separated in units of the interaction scale and the particle picture is self-consistent — and the rotation is correspondingly slow, ω = 0.223130. The binary preset v_b = 0.15 sits at 67 % of the escape threshold 0.223130, comfortably inside the bound region but far enough from zero to give a visibly precessing orbit. The velocity sweep shows the interesting boundary structure: the escape edge observed numerically (between 0.26 and 0.28) lies above the two-body threshold 0.223130 because the centrifugal barrier temporarily traps marginally supercritical launches — a genuinely three-dimensional-in-time effect that a static energy argument alone would miss.

Within the program, TRX-04 plays the role of the spatial optics bridge. Upstream, TRX-03 verifies the same molecular physics in the temporal domain of a fiber laser, where the force law carries an additional phase-cosine modulation; downstream, TRX-05 moves from field maxima to field zeros — optical vortices — and recovers Kirchhoff's vortex equations, while TRX-08 replaces photons by laser-cooled ions with a harmonic trap and Coulomb tail. Together with the celestial block (TRX-01, TRX-11) these studies show that the equilateral central configuration is a form, not an accident: it re-emerges in every medium whose two-body law is central, conservative and pair-additive, with only the rotation law changing.

## 14. Conclusions

- The equilateral beam triangle is a genuine optical central configuration: it rotates rigidly over three full turns (T = 84.4778) with the side staying equilateral to 1.8e-08, versus the 1e-6 acceptance gate.
- The measured rotation rate 0.223130160 reproduces the analytic Lagrange law ω² = 3Ue^(−a/w)/(maw) (ω = e^(−3/2) = 0.223130160 at the preset) to 1.1×10⁻¹¹ — the balance is confirmed at round-off level.
- The rotation law is verified as a law across the side sweep a = 2.0…8.0: numeric re-runs sit on the analytic curve at all seven sides (ω from 0.450558 down to 0.011216), while the Newtonian 1/r reference decays markedly slower (0.076547 at a = 8).
- Invariants are conserved at machine level in all runs: energy drift 4.7e-16 (rotation), 3.6e-16 (anti-phase trio), 3.0e-12 (binary), angular-momentum drift 2.2e-15 — all below the 1e-10 tolerance.
- The phase sign controls the outcome: the anti-phase trio never collapses (min pairwise distance 3.0000 ≥ 0.95a) and expands to 23.476, while the in-phase binary with E_rel = −0.027 stays bound with its separation inside [0.635, 3.000] over t = 80.
- The bound/unbound map is established: max separation stays 3.0 for v_b ≤ 0.26 and escape follows for v_b = 0.28–0.34 (7.7515 → 19.1521 over T = 40); the observed escape edge lies above the two-body threshold v_b* = e^(−3/2) = 0.223130 because the centrifugal barrier temporarily traps near-threshold launches.

## 15. The monograph and its renditions

The complete monograph of this study exists in four renditions — Russian and English are separate documents, each in a typeset PDF and an editable DOCX:

| Rendition | Path |
|---|---|
| Monograph (English, PDF) | `monograph/monograph_EN.pdf` |
| Monograph (English, DOCX) | `monograph/monograph_EN.docx` |
| Monograph (Russian, PDF) | `monograph/monograph_RU.pdf` |
| Monograph (Russian, DOCX) | `monograph/monograph_RU.docx` |
| Reading-room copy | `publications/pdf/TRX-04-photon-fluid_EN.pdf` · `publications/pdf/TRX-04-photon-fluid_RU.pdf` |
| HTML source | `publications/html/TRX-04-photon-fluid.html` |

**Monograph abstract.** This monograph treats three laser beams propagating through a focusing Kerr medium as a photon fluid whose members — spatial solitons of the nonlinear Schrödinger equation — interact through phase-dependent two-body forces: in-phase beams attract with V = −Ue^(−r/w), anti-phase beams repel with V = +Ue^(−r/w). In the particle approximation the in-phase triplet forms a Lagrange central configuration: an equilateral beam triangle of side a = 3 rotating rigidly at ω = 0.223130160, fixed by the force balance ω² = 3Ue^(−a/w)/(maw) — the optical sibling of Newton's Lagrange solution. The numerical experiment verifies the choreography to machine precision: the triangle stays equilateral to 1.8e-08 over three full rotations (T = 84.4778), the measured rotation rate matches the analytic value to 1.1×10⁻¹¹, energy and angular momentum are conserved to 4.7e-16 and 2.2e-15, the anti-phase trio expands to 23.476 without collapse, and an in-phase binary with E_rel = −0.027 stays bound (separation within [0.635, 3.000], energy drift 3.0e-12) over t = 80. All nine acceptance checks PASS.

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
| `t` | 600 | 0 … 21.1195 |
| `x1` | 600 | 0 … 1.73205081 |
| `y1` | 600 | 1.73205081 … -0 |
| `x2` | 600 | -1.5 … -0.8660254 |
| `y2` | 600 | -0.8660254 … 1.5 |
| `x3` | 600 | 1.5 … -0.8660254 |
| `y3` | 600 | -0.8660254 … -1.5 |

**Reproduction matrix**

| Command | What it does |
|---|---|
| `python3 research/TRX-04-photon-fluid/code/trx04_photon_fluid.py` | full run: physics + acceptance checks (9.4 s (9.415 s recorded with --figures)) |
| `python3 research/TRX-04-photon-fluid/code/trx04_photon_fluid.py --smoke` | CI guard: same checks, seconds-scale settings |
| `python3 research/TRX-04-photon-fluid/code/trx04_photon_fluid.py --figures` | regenerates the 300-dpi figure set |
| `make research-smoke` | all twelve studies in smoke mode |
| `make research-figures` | all twelve studies + figure sets |

## 17. Cross-links within the program

- **TRX-03** is the 1-D fiber-laser version of the same molecular physics: temporal solitons with a phase-cosine force law and a breathing bound state.
- **TRX-05** replaces the field maxima by field *zeros* (optical vortices) and recovers Kirchhoff's vortex equations — the same triangle with circulations instead of phases.
- **TRX-08** trades photons for ions — the trap harmonic force plus the Coulomb tail, with the same central-configuration and invariant bookkeeping.

## 18. Inside the script

The executable is a single deterministic file, `code/trx04_photon_fluid.py`, ~pure `numpy`/`scipy` with no network access and no random state beyond fixed seeds. One run executes the full physics of the study, evaluates every registered acceptance check against its committed target and tolerance, and writes the JSON protocol — the same file quoted in §9.

| Mode | Invocation | What happens |
|---|---|---|
| Full | `python3 code/trx04_photon_fluid.py` | complete experiment, all checks, JSON protocol (9.4 s (9.415 s recorded with --figures)) |
| Smoke | `python3 code/trx04_photon_fluid.py --smoke` | identical acceptance logic at seconds-scale settings — the CI mode |
| Figures | `python3 code/trx04_photon_fluid.py --figures` | regenerates the schematic + the four 300-dpi PNG panels |

**Outputs per run**

| File | Produced by | Content |
|---|---|---|
| `results/trx04_results.json` | every mode | status, checks (value/target/tol/unit/pass/note), series, meta |
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
| Previous study | TRX-003 |
| Next study | TRX-005 |

## 21. Notation

| Symbol | Meaning |
|---|---|
| A | slowly varying beam envelope; A_z, ∇²⊥ are the z-derivative and transverse Laplacian |
| U, w, m | potential depth, interaction scale (beam-waist unit) and soliton mass; all 1 at the preset |
| s | pair sign: −1 in phase (attraction), +1 anti-phase (repulsion) |
| r, r_kl | pair separation between beams k and l |
| a, r_c | triangle side and centroid orbit radius a/√3 |
| ω | rotation rate of the rigid triangle; ω² = 3Ue^(−a/w)/(maw) |
| v_b | binary transverse launch velocity (preset 0.15) |
| E_rel | relative energy of the binary pair, m·v_b² − Ue^(−r₀/w) |
| E, L_z | total energy and angular momentum, the conserved invariants (E5) |
| T | duration of a run (rotation 84.4778; anti-phase 40; binary 80) |
| V_pm, V_ap | in-phase and anti-phase pair potentials (E2) |

## 22. References

1. Chiao, R. Y., Garmire, E., Townes, C. H. (1964). *Self-trapping of optical beams.* Phys. Rev. Lett. 13, 479–482.
2. Snyder, A. W., Mitchell, D. J., Kivshar, Y. S. (1995). *Unification of self-trapping of light and matter waves.* Phys. Rev. E 51, 3061–3066.
3. Stegeman, G. I., Segev, M. (1999). *Optical spatial solitons and their interactions.* Science 286, 1518–1523.
4. Reynaud, F., Barthelemy, A. (1990). *Optically controlled interaction between two fundamental soliton beams.* Europhys. Lett. 12, 401–405.
5. Aitchison, J. S., Weiner, A. M., Silberberg, Y., Oliver, M. K., Jackel, J. L., Leaird, D. E., Vogel, E. M., Smith, P. W. E. (1991). *Experimental observation of spatial soliton interactions.* Opt. Lett. 16, 15–17.
6. Assanto, G., Peccianti, M. (2012). *Nematicons: spatial optical solitons in nematic liquid crystals.* Phys. Rep. 516, 147–208.
7. Carusotto, I., Ciuti, C. (2013). *Quantum fluids of light.* Rev. Mod. Phys. 85, 291–315.
8. Bialynicki-Birula, I. (2006). *Photon waves.* Acta Phys. Pol. A 109, 20–32.
9. Lagrange, J.-L. (1772). *Essai sur le problème des trois corps.* In: Œuvres de Lagrange, Vol. 6. Gauthier-Villars, Paris (1873).

## 23. Glossary

| Term | Definition |
|---|---|
| Photon fluid | an ensemble of light beams behaving as a gas of mutually interacting particles with tunable two-body forces |
| Spatial soliton | a beam that propagates in a focusing nonlinear medium without diffracting, carrying its own waveguide |
| Kerr nonlinearity | refractive-index change proportional to intensity; the field equation is the focusing NLS (E1) |
| Relative phase | the optical phase difference between beams: in phase attracts, anti-phase repels |
| Particle approximation | reduction of well-separated beams to point bodies with pair forces |
| Central configuration | positions where the net force on each body points at the centroid proportional to its radius; the equilateral triangle is one |
| Lagrange triangle | the rigidly rotating equilateral three-body solution found in 1772; here its optical realization |
| Binary | a bound in-phase pair whose separation oscillates between turning points while the orbit precesses |
| Escape threshold v_b* | launch velocity separating bound from unbound pair orbits; here √(Ue^(−r₀/w)) = e^(−3/2) = 0.223130 |
| Beam-waist unit w | the exponential interaction scale; the length unit of the study |

## 24. Appendix A. Full parameter table

| Symbol | Value | Role |
|---|---|---|
| U, w, m | 1, 1, 1 | natural units: energy, length, mass |
| a | 3 | triangle side; operating point of the rotation run |
| r_c | a/√3 = 1.732051 | beam orbit radius about the centroid |
| (U/w)e^(−a/w) | 0.049787 | edge force at the operating point (= ω²) |
| ω | e^(−3/2) = 0.22313016014842985 | analytic rotation rate at the preset |
| T_rotation | 84.4778 | rotation run: three full turns, 2400 samples |
| anti-phase run | same triangle at rest, T = 40 | repulsive expansion control |
| binary preset | r₀ = 3, v_b = ±0.15, E_rel = −0.027, T = 80 | in-phase bound-pair run |
| v_b* | e^(−3/2) = 0.223130 | analytic escape threshold of the binary |
| velocity sweep | 16 launches, v_b = 0.06…0.34, T = 40 | bound/unbound map of fig03b |
| integrator | DOP853, rtol = atol = 1e-12, max_step = 0.1 | all runs, dense output |

**Protocol-level parameter snapshot** (`results` JSON, `meta` block):

| Key | Value |
|---|---|
| `equations` | `["i A_z + (1/2) laplacian(A) + \|A\|^2 A = 0   (focusing NLS)", "V_pm(r) = -U exp(-r/w) ; V_ap(r) = +U exp(-r/w)", "Lagrange triangle: omega^2 = 3 U exp(-a/w) / (m a w)"]` |
| `omega_triangle_exp` | `0.22313016014842985` |
| `omega_triangle_newtonian_reference` | `0.3333333333333333` |
| `mapping_note` | `"Newtonian V=-1/r gives omega^2=3Gm/a^3; the exponential Kerr force gives omega^2=3U e^{-a/w}/(m a w) — same choreography class as TRIVORTEX Theorem 3.1"` |

## 25. Appendix B. BibTeX

```bibtex
@article{chiao1964,
  author  = {Chiao, R. Y. and Garmire, E. and Townes, C. H.},
  title   = {Self-trapping of optical beams},
  journal = {Physical Review Letters},
  year    = {1964}, volume = {13}, pages = {479--482}}

@article{snyder1995,
  author  = {Snyder, A. W. and Mitchell, D. J. and Kivshar, Y. S.},
  title   = {Unification of self-trapping of light and matter waves},
  journal = {Physical Review E},
  year    = {1995}, volume = {51}, pages = {3061--3066}}

@article{aitchison1991,
  author  = {Aitchison, J. S. and Weiner, A. M. and Silberberg, Y. and Oliver, M. K. and Jackel, J. L. and Leaird, D. E. and Vogel, E. M. and Smith, P. W. E.},
  title   = {Experimental observation of spatial soliton interactions},
  journal = {Optics Letters},
  year    = {1991}, volume = {16}, pages = {15--17}}

@article{carusotto2013,
  author  = {Carusotto, Iacopo and Ciuti, Cristiano},
  title   = {Quantum fluids of light},
  journal = {Reviews of Modern Physics},
  year    = {2013}, volume = {85}, pages = {291--315}}

@misc{lagrange1772,
  author  = {Lagrange, Joseph-Louis},
  title   = {Essai sur le probl{\`e}me des trois corps},
  year    = {1772},
  note    = {In: Œuvres de Lagrange, Vol. 6, Gauthier-Villars, Paris, 1873}}
```

## 26. How to cite

Cite the repository through [`CITATION.cff`](../../CITATION.cff) (DOI 10.5281/zenodo.21825394, version 1.0.0); this study is part of the TRIVORTEX Research Program. If you cite the study alone, name the monograph rendition you used and attach the JSON protocol of the run you reproduced.

```bibtex
@misc{trivortextrx042026isaev,
  author       = {Isaev, Iskhak Khamzatovich},
  title        = {Photon Fluid: Three Kerr Solitons (Spatial, 2-D) (TRIVORTEX Research Program, TRX-04)},
  year         = {2026},
  howpublished = {Zenodo},
  doi          = {10.5281/zenodo.21825394},
  url          = {https://github.com/wild8highlander/research-papers}
}
```

