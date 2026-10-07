# TRX-08 — Three Laser-Cooled Ions in a Linear Paul Trap: the Table-Top Lagrange Triangle

*TRIVORTEX Research Program · version 1.0.0 · study TRX-08 of 12*

Three laser-cooled ions in the transverse plane of a linear Paul trap form a table-top three-body problem: a two-dimensional harmonic rf pseudopotential confines them, their mutual Coulomb repulsion pushes them apart, and Doppler cooling — modelled as a linear drag −γ_d·v — dissipates energy until the ions crystallize into the equilateral **Lagrange triangle** of side a = (3κ/ω₀²)^(1/3) = 3^(1/3) = 1.4422495703. The study verifies the whole chain to machine precision: sides equal to 4.4e-16, central angles 2π/3 to 4.4e-16, the normal-mode ladder {0, ω₀ (×2), √(3/2)ω₀ (×2), √3ω₀} confirmed to 1.4·10⁻⁸, and a conservative hold at the exact equilibrium that keeps the crystal static to 3.9e-15 over fifty time units with energy drift 8.9e-16 — the trapped-ion twin of the Lagrange relative equilibrium behind TRIVORTEX Theorem 3.1 and the smallest ion-crystal quantum simulator.

> **Edition 1.0.0.** This README is part of the first public release of the TRIVORTEX research program. The study ships as an executable script, a committed JSON protocol, four 300-dpi figures, a schematic and a bilingual monograph in four renditions (Russian and English, each in PDF and DOCX).

**At a glance**

| Aspect | Value |
|---|---|
| Block | Quantum three-body — study 08 of 12 |
| Model | three ions in a 2-D harmonic rf pseudopotential + Coulomb repulsion (ω₀ = κ = m = 1) |
| Key structure | equilateral Lagrange triangle, a = 3^(1/3) = 1.4422495703, U* = 3.120125734578 |
| Headline result | mode ladder {0, ω₀×2, √(3/2)ω₀×2, √3ω₀} confirmed to 1.4·10⁻⁸; static hold 3.9e-15 over t = 50 |
| Verification | 10/10 checks PASS (full mode) |
| Runtime | 6.79 s full · < 20 s smoke |

| Field | Value |
|---|---|
| Study | `TRX-08` (TRX-08-ion-trap) |
| Program | TRIVORTEX — The Three-Body Problem in the Vortex Model |
| Author | Isaev Iskhak Khamzatovich (ORCID `0009-0003-7299-0701`) |
| DOI | [10.5281/zenodo.21825394](https://doi.org/10.5281/zenodo.21825394) |
| Version | 1.0.0 — first public release |
| Code | `research/TRX-08-ion-trap/code/trx08_ion_trap.py` |
| Protocol | `research/TRX-08-ion-trap/results/trx08_results.json` |
| License | `LicenseRef-Proprietary-Wild8Highlander-1.0` |

## 1. Mission

Ion traps turn the three-body problem into an afternoon experiment. Three laser-cooled ions spontaneously arrange into an equilateral triangle whose size is fixed by one algebraic force balance, a³ = 3κ/ω₀², and whose vibrational spectrum is pure group theory: one zero mode, two centre-of-mass translations, two quadrupole deformations and one breathing mode. For TRIVORTEX this is a new realization of the central-configuration logic: two competing scales — harmonic confinement versus Coulomb repulsion here, vortex attraction versus Abel–Hertz flux there — fix the size of the same equilateral triad, and the trapped crystal is the table-top twin of the Lagrange relative equilibrium of Theorem 3.1.

The study verifies that chain end to end. A damped inertial relaxation from a seeded random start (with a documented finite-wavepacket softening ε_relax = 0.05) is Newton-polished on the strict unsoftened force balance and lands on the exact triangle a = 3^(1/3) = 1.44224957 — sides equal to 4.4e-16, central angles 2π/3 to 4.4e-16, and the potential equal to the analytic triangle energy U* = 3.120125734578 exactly. The finite-difference Hessian confirms the full mode ladder to 1.4·10⁻⁸, and a conservative run started exactly at equilibrium holds it statically to 3.9e-15 over fifty time units with energy drift 8.9e-16: the ion crystal is a frozen choreography. Independent re-runs additionally reproduce the scaling law a(κ) = (3κ/ω₀²)^(1/3) and map the crystallization time across the Doppler-drag range.

## 2. Introduction and historical context

The quadrupole ion trap was invented by Wolfgang Paul and Helmut Steinwedel in 1953 as a mass spectrometer without a magnetic field; the radiofrequency pseudopotential they introduced lets charged particles float in a nearly harmonic well far from any material surface. Half a century of refinement — recognized by the 1989 Nobel Prize shared by Paul and Hans Dehmelt — turned the trap into the workhorse of atomic spectroscopy, frequency standards and, later, quantum information. Paul's 1990 Nobel lecture in the Reviews of Modern Physics remains the canonical introduction to the pseudopotential picture used throughout this study.

Laser cooling supplied the second ingredient. The 1975 proposals of Hänsch and Schawlow (free atoms) and of Wineland and Dehmelt (trapped ions) showed that red-detuned light slows an absorber toward the Doppler limit; Itano and Wineland (1982) worked out the full theory for ions in harmonic and Penning traps. Cooling removes kinetic energy order by order, and in a harmonic confinement the coldest state of a cloud is no cloud at all: the competition between the confining force and the mutual Coulomb repulsion has a crystalline ground state.

That phase transition was observed in 1987: Diedrich and colleagues in Garching saw laser-cooled stored ions jump from a disordered cloud to an ordered crystal, and Dubin and O'Neil's 1999 review consolidated the whole field — trapped nonneutral plasmas, liquids and crystals — into a single statistical-mechanics framework with the Coulomb coupling parameter as the control variable. For a handful of ions the crystal geometry is dictated by elementary force balance: two ions line up, three form an equilateral triangle, larger ensembles arrange in rings and shells — the finite-N precursors of Wigner crystals.

The small crystals then became quantum technology. Cirac and Zoller's 1995 proposal used the collective vibrational modes of a trapped-ion string as a data bus for quantum gates, and James (1998) computed the exact normal-mode spectrum of small ion crystals — precisely the object this study verifies classically. Three ions form the smallest ion-crystal quantum simulator (Blatt and Roos 2012), and their mode ladder — zero, centre-of-mass, breathing — is the table-top counterpart of the TRIVORTEX triad: the equilateral configuration of Theorem 3.1, realized in an afternoon experiment with a linear Paul trap and a pair of cooling lasers.

## 3. Physical system and preset

Three equal ions move in the transverse (x, y) plane of a linear Paul trap. The time-averaged rf pseudopotential is harmonic in the plane, U_trap = mω₀²r²/2; the mutual Coulomb repulsion κ/rij pushes the ions apart; the Doppler-cooling lasers are modelled by a linear drag −γ_d·v. The dynamics is two-dimensional and dimensionless with ω₀ = κ = m = 1, the state interleaved as [x₁, y₁, v₁ˣ, v₁ʸ, …] for the three ions, and the Coulomb force is softened as κ·r/(r² + ε²)^(3/2) with a documented ε during the relaxation stage.

Two competing length scales leave a single dimensionless combination κ/ω₀² that fixes the crystal size: at the equilateral configuration each ion feels a radially outward Coulomb push √3κ/a² and an inward trap pull ω₀²a/√3, so the balance gives a = (3κ/ω₀²)^(1/3) — 3^(1/3) = 1.4422495703 for the preset. Because the trap is isotropic, the orientation of the triangle is free — this is exactly the zero Hessian mode. During cooling the energy is dissipated, but the trap is static in the lab frame, so the crystal is a static equilibrium: with γ_d = 0 and zero initial velocity the conservative dynamics K + U keeps it frozen.

| Parameter | Value | Meaning |
|---|---|---|
| ω₀, κ, m | 1, 1, 1 | dimensionless trap frequency, Coulomb strength, ion mass |
| state | interleaved [x₁, y₁, v₁ˣ, v₁ʸ, …] | three ions in the transverse trap plane |
| initial condition | seeded random in [−1, 1]², zero velocities | rng seed 3 |
| cooling | γ_d = 0.8, linear drag −γ_d·v | Doppler-cooling model, relaxation stage only |
| softening | ε_relax = 0.05, polish at ε = 1e-12 | finite cooled wavepacket → strict force balance |
| time spans | T_relax = 60, T_hold = 50 | crystallization window and conservative hold |
| Ca⁺ mapping | m = 40 amu, trap 1 MHz | physical scale; κ sets the trap length scale |

**Model assumptions**

- Two-dimensional dynamics in the transverse plane; axial motion and rf micromotion are not modeled (pseudopotential approximation, valid when the drive frequency greatly exceeds ω₀).
- Doppler cooling is reduced to a linear drag −γ_d·v; photon recoil heating and saturation physics are omitted.
- The relaxation uses a documented softening ε_relax = 0.05 (finite cooled wavepacket); all acceptance numbers are Newton-polished on the strict ε = 1e-12 force balance.
- Three identical ions; no species mix, stray charges or trap anisotropy in the plane (orientation is a free zero mode).
- The crystal is a static equilibrium of the lab-frame dynamics, so the conservative hold with γ_d = 0 is an exact invariant test.
- A single seeded run (rng seed 3) per stage; the protocol is deterministic, offline and bit-reproducible.

## 4. Governing equations

(E1) Dynamics of the three-ion crystal (harmonic trap + softened Coulomb repulsion + Doppler drag):

$$m\ddot{\mathbf{r}}_k = -m\omega_0^2\,\mathbf{r}_k - \gamma_d\dot{\mathbf{r}}_k + \kappa\sum_{l\ne k}\frac{\mathbf{r}_k-\mathbf{r}_l}{\bigl(|\mathbf{r}_k-\mathbf{r}_l|^2+\epsilon^2\bigr)^{3/2}}$$

(E2) Equilateral force balance: the crystal side:

$$\omega_0^2\,\frac{a}{\sqrt{3}} = \sqrt{3}\,\frac{\kappa}{a^2}\quad\Longrightarrow\quad a = \left(\frac{3\kappa}{\omega_0^2}\right)^{1/3} = 3^{1/3} = 1.4422495703$$

(E3) Energy along the equilateral family; its minimum is the force-balance side:

$$U(a) = \tfrac{1}{2}\omega_0^2 a^2 + \frac{3\kappa}{a},\qquad U_* = \tfrac{3}{2}\cdot 3^{2/3} = 3.120125734578$$

(E4) Normal-mode ladder: eigenvalues of the 6×6 position Hessian at the crystal:

$$\omega^2 = \mathrm{eig}\,\frac{\partial^2 U}{\partial x_i\,\partial x_j},\qquad \omega \in \{0,\ \omega_0\ (\times 2),\ \sqrt{\tfrac{3}{2}}\,\omega_0\ (\times 2),\ \sqrt{3}\,\omega_0\}$$

(E5) Static hold: the equilibrium is an exact solution of the conservative dynamics:

$$\mathbf{r}_k(0) = \mathbf{r}_k^{*},\ \dot{\mathbf{r}}_k(0) = 0,\ \gamma_d = 0\ \Longrightarrow\ \mathbf{r}_k(t) = \mathbf{r}_k^{*}$$

## 5. Scheme

![TRX-08 scheme — three laser-cooled ions in the transverse plane of a linear Paul trap crystallize into the equilateral Lagrange triangle under Coulomb repulsion, harmonic confinement and Doppler drag; the normal-mode ladder and the mapping to the TRIVORTEX vortex model are shown on the right.](figures/scheme_trx08.svg)

*TRX-08 scheme — three laser-cooled ions in the transverse plane of a linear Paul trap crystallize into the equilateral Lagrange triangle under Coulomb repulsion, harmonic confinement and Doppler drag; the normal-mode ladder and the mapping to the TRIVORTEX vortex model are shown on the right..*

The diagram encodes the following elements:

- **Four rf rods** — quadrupole electrode cross-section generating the harmonic pseudopotential U = mω₀²r²/2 (dashed equipotentials)
- **Three gold ions** — the equilateral crystal of side a = 3^(1/3) = 1.442249570 (trap length units)
- **Coulomb push vs trap pull** — force balance on an ion: two Coulomb pushes plus the harmonic pull sum to zero
- **Doppler-cooling beams (−γv)** — the laser drag that dissipates the binding energy ΔU = 1.7609 during crystallization
- **Normal-mode ladder** — 0 (rigid rotation), ω₀ (×2, centre of mass), √(3/2)ω₀ (×2, quadrupole), √3ω₀ = 1.732051 (breathing)
- **Mapping strip** — crystal → Lagrange relative equilibrium; breathing → radial modulation of Theorem 3.1; zero mode → continuous choreography family

## 6. Mapping to TRIVORTEX

The three-ion crystal is the table-top member of the same central-configuration family that anchors TRIVORTEX. The equilateral triangle is literally the Lagrange solution: one algebraic force balance fixes its size, just as the balance of vortex attractions and Abel–Hertz flux fixes the size of the same-sign vortex triangle of Theorem 3.1 — in both problems two competing scales leave a single dimensionless combination that sets the geometry. The mode correspondence is equally direct: the breathing mode √3ω₀ is the radial modulation of the Theorem 3.1 triangle, the two centre-of-mass modes reflect the shared translational symmetry, and the zero rigid-rotation mode — the free orientation of the crystal in the isotropic trap — is the continuous family of relative equilibria, the same degeneracy that makes the vortex triangle a rotating choreography rather than a static figure. What the ion trap adds is dissipation as a selection mechanism: cooling drives the configuration downhill to the central configuration and freezes it there, which is exactly how the monograph's rotating triads are realized in laboratory matter.

| Quantity in this study | TRIVORTEX analog | Comment |
|---|---|---|
| Ion crystal triangle | Lagrange equilateral solution | same central configuration |
| Coulomb repulsion + harmonic trap | vortex attractions + AH flux | competing scales fix the size |
| Breathing mode √3ω₀ | radial modulation of Theorem 3.1 | collective breathing of the triad |
| Zero rotation mode | continuous choreography family | free orientation of the relative equilibrium |

## 7. Dimensionless formulation

Time in units of 1/ω₀, lengths in units of ℓ = (κ/mω₀²)^(1/3), energies in units of mω₀²ℓ² = κ/ℓ. The preset sets ω₀ = κ = m = 1, so the crystal side is a = 3^(1/3) = 1.4422495703 and its energy U* = 1.5·3^(2/3) = 3.120125734578. The trap is isotropic, so the crystal orientation is free (the zero mode); for a Ca⁺ ion (m = 40 amu) in a 1 MHz trap the Coulomb parameter κ = q²/(4πε₀)/(mω₀²ℓ³) sets the physical length scale.

## 8. Numerical method

Crystallization stage: the three ions start from a seeded random configuration in [−1, 1]² with zero velocities (rng seed 3) and relax under the damped inertial dynamics (E1) with γ_d = 0.8 and the documented softening ε_relax = 0.05, integrated with the explicit Dormand–Prince 8(5,3) scheme at rtol = atol = 1e-11, max_step 0.05, over T_relax = 60. The end state is the softened equilibrium — the stand-in for the finite cooled wavepacket.

Polish and spectrum stage: the relaxed configuration seeds a Newton root-find (scipy hybr, tol 1e-14) of the strict force balance at ε = 1e-12, with the analytic triangle as a documented fallback; the polished crystal is compared against a = 3^(1/3) (sides, equality, 2π/3 angles) and against the analytic energy U* = 3.120125734578. Normal modes come from a finite-difference Hessian (central fourth-order stencil, h = 1e-4) diagonalized with eigvalsh; the zero, COM and breathing mode counts are accepted in 5e-6 frequency windows.

Invariant and sweeps stage: the static hold integrates the conservative dynamics (γ_d = 0) from the analytic equilibrium with rtol = atol = 1e-12 over t = 50, recording the position drift and the total-energy drift. Two sweeps close the protocol: five Coulomb strengths κ ∈ {0.25, 0.5, 1, 2, 4} are re-relaxed and re-polished against the cubic law a(κ) = (3κ/ω₀²)^(1/3), and six Doppler drags γ_d ∈ {0.4, 0.6, 0.8, 1.2, 1.6, 2.4} are scored by the settle time — the first moment the side spread stays below 0.01 within the 600-sample window. Every check stores value, target, tolerance, unit and pass flag in the JSON protocol; the run is deterministic, offline and bit-reproducible.

## 9. Verification protocol and acceptance checks

Every check is registered before the run: target, tolerance and unit are committed in the protocol, not chosen after the fact.

| Check | Target | Tolerance |
|---|---|---|
| Global minimum reached: U_final − U_triangle | 0 | 1e-9 |
| Binding energy released during cooling | > 0 | exact |
| Crystal side vs a = 3^(1/3) | a | 1e-8 |
| Sides equal (equilateral) | 0 | 1e-8 |
| Central angles 2π/3 | 0 | 1e-6 |
| Exactly one zero Hessian eigenvalue (rotation) | 1 | 1e-6 |
| Exactly two COM modes at ω₀ | 2 | 5e-6 |
| Breathing mode at √3ω₀ | 1 | 5e-6 |
| Static equilibrium hold over t = 50 | 0 | 1e-9 |
| Conservative energy drift | 0 | 1e-10 |

**Recorded verification run** (mode: smoke, status: **PASS**, 10/10 checks)

| Check | Recorded value | Target | Tolerance | Unit | Verdict |
|---|---|---|---|---|---|
| `global_minimum_reached` | 0 | 0 | 1.0000e-09 | energy | PASS |
| `crystallization_energy_released` | 1 | 1 | 1.0000e-12 | bool | PASS |
| `crystal_side_equals_analytic` | 1.44224957 | 1.44224957 | 1.0000e-08 | length | PASS |
| `crystal_equilateral` | 0 | 0 | 1.0000e-08 | length | PASS |
| `crystal_angles_120deg` | 4.4409e-16 | 0 | 1.0000e-06 | rad | PASS |
| `zero_rotation_mode` | 1 | 1 | 1.0000e-12 | bool | PASS |
| `two_com_modes_at_omega0` | 1 | 1 | 1.0000e-12 | bool | PASS |
| `breathing_mode_sqrt3` | 1 | 1 | 1.0000e-12 | bool | PASS |
| `static_equilibrium_holds` | 1.3878e-15 | 0 | 1.0000e-09 | length | PASS |
| `conservative_energy_conserved` | 8.8818e-16 | 0 | 1.0000e-10 | energy | PASS |

**Check notes** — what each number means:

| Check | Note |
|---|---|
| `global_minimum_reached` | U_final = 3.120125734578 vs analytic triangle U = 3.120125734578 |
| `crystallization_energy_released` | binding energy released during cooling: 1.7609 |
| `crystal_side_equals_analytic` | sides = [1.44224957 1.44224957 1.44224957], a = (3k/w0^2)^(1/3) = 1.442249570 |
| `crystal_equilateral` | max side - min side |
| `crystal_angles_120deg` | central angles = [2.0943951 2.0943951 2.0943951] (2*pi/3 each) |
| `zero_rotation_mode` | eigenvalues = [-2.00000000e-08  9.99999990e-01  1.00000003e+00  1.49999999e+00 1.50000003e+00  3.00000001e+00] |
| `two_com_modes_at_omega0` | COM translational modes at exactly omega0 |
| `breathing_mode_sqrt3` | breathing = sqrt(3)*omega0 = 1.732051 |
| `static_equilibrium_holds` | positions unchanged after t=50 with zero initial velocity |
| `conservative_energy_conserved` | damping-free crystal, t=50 |

## 10. Figure gallery (300 dpi)

![{'cap_en': 'Model landscape of the three-ion crystal: (a) potential slice with ions 2 and 3 held at the equilibrium vertices and ion 1 scanned over the trap plane; (b) potential energy along the equilateral family U(a) = ω₀²a²/2 + 3κ/a.', 'cap_ru': 'Ландшафт модели трёхионного кристалла: (а) срез потенциала при зафиксированных во 2-й и 3-й вершинах равновесия ионах и сканируемом по плоскости ловушки ионе 1; (б) потенциальная энергия вдоль равностороннего семейства U(a) = ω₀²a²/2 + 3κ/a.', 'walk_en': 'The scanned-ion minimum lands exactly on the third vertex of the triangle, and the one-dimensional energy profile has its minimum at a* = 3^(1/3) = 1.442249570 with U* = 3.120125735 (trap energy units) — the force balance (E2) is the minimizer of the energy (E3).', 'walk_ru': 'Минимум при сканировании иона 1 попадает точно в третью вершину треугольника, а одномерный профиль энергии имеет минимум при a* = 3^(1/3) = 1.442249570 с U* = 3.120125735 (энергетические единицы ловушки) — баланс сил (E2) является минимизатором энергии (E3).'}](figures/fig01_crystal_landscape.png)

*{'cap_en': 'Model landscape of the three-ion crystal: (a) potential slice with ions 2 and 3 held at the equilibrium vertices and ion 1 scanned over the trap plane; (b) potential energy along the equilateral family U(a) = ω₀²a²/2 + 3κ/a.', 'cap_ru': 'Ландшафт модели трёхионного кристалла: (а) срез потенциала при зафиксированных во 2-й и 3-й вершинах равновесия ионах и сканируемом по плоскости ловушки ионе 1; (б) потенциальная энергия вдоль равностороннего семейства U(a) = ω₀²a²/2 + 3κ/a.', 'walk_en': 'The scanned-ion minimum lands exactly on the third vertex of the triangle, and the one-dimensional energy profile has its minimum at a* = 3^(1/3) = 1.442249570 with U*= 3.120125735 (trap energy units) — the force balance (E2) is the minimizer of the energy (E3).', 'walk_ru': 'Минимум при сканировании иона 1 попадает точно в третью вершину треугольника, а одномерный профиль энергии имеет минимум при a* = 3^(1/3) = 1.442249570 с U*= 3.120125735 (энергетические единицы ловушки) — баланс сил (E2) является минимизатором энергии (E3).'}.*

![{'cap_en': 'Headline result: (a) the Newton-polished crystal with the exact force balance on each ion; (b) the six Hessian normal-mode frequencies against the analytic ladder.', 'cap_ru': 'Главный результат: (а) отполированный методом Ньютона кристалл с точным балансом сил на каждом ионе; (б) шесть собственных частот гессиана против аналитической лестницы.', 'walk_en': 'The polished triangle has side a = 1.442249570 with all three sides equal to 4.4e-16, and the measured finite-difference spectrum {0, 1.0, 1.0, 1.2247449, 1.2247449, 1.7320508} deviates from the analytic ladder {0, ω₀ (×2), √(3/2)ω₀ (×2), √3ω₀} by at most 1.4·10⁻⁸ against the 5e-6 tolerance.', 'walk_ru': 'Отполированный треугольник имеет сторону a = 1.442249570, все три стороны равны с точностью 4.4e-16, а измеренный конечно-разностный спектр {0, 1.0, 1.0, 1.2247449, 1.2247449, 1.7320508} отклоняется от аналитической лестницы {0, ω₀ (×2), √(3/2)ω₀ (×2), √3ω₀} не более чем на 1.4·10⁻⁸ при допуске 5e-6.'}](figures/fig02_crystal_and_modes.png)

*{'cap_en': 'Headline result: (a) the Newton-polished crystal with the exact force balance on each ion; (b) the six Hessian normal-mode frequencies against the analytic ladder.', 'cap_ru': 'Главный результат: (а) отполированный методом Ньютона кристалл с точным балансом сил на каждом ионе; (б) шесть собственных частот гессиана против аналитической лестницы.', 'walk_en': 'The polished triangle has side a = 1.442249570 with all three sides equal to 4.4e-16, and the measured finite-difference spectrum {0, 1.0, 1.0, 1.2247449, 1.2247449, 1.7320508} deviates from the analytic ladder {0, ω₀ (×2), √(3/2)ω₀ (×2), √3ω₀} by at most 1.4·10⁻⁸ against the 5e-6 tolerance.', 'walk_ru': 'Отполированный треугольник имеет сторону a = 1.442249570, все три стороны равны с точностью 4.4e-16, а измеренный конечно-разностный спектр {0, 1.0, 1.0, 1.2247449, 1.2247449, 1.7320508} отклоняется от аналитической лестницы {0, ω₀ (×2), √(3/2)ω₀ (×2), √3ω₀} не более чем на 1.4·10⁻⁸ при допуске 5e-6.'}.*

![{'cap_en': 'Parameter sweeps: (a) crystal side versus Coulomb strength κ — relaxation + Newton re-runs against the analytic cubic law; (b) crystallization settle time versus Doppler drag γ_d.', 'cap_ru': 'Развертки параметров: (а) сторона кристалла против кулоновской силы κ — прогоны релаксации с полировкой Ньютона против аналитического кубического закона; (б) время кристаллизации против доплеровского трения γ_d.', 'walk_en': 'Independent re-runs reproduce a(κ) = (3κ/ω₀²)^(1/3) exactly at all five κ ∈ {0.25, 0.5, 1, 2, 4} — a from 0.908560296 to 2.289428485 — while the settle time decreases monotonically from 24.341 to 5.609 (1/ω₀ units) over γ_d ∈ [0.4, 2.4], with no overdamped upturn inside the scanned window.', 'walk_ru': 'Независимые прогоны воспроизводят a(κ) = (3κ/ω₀²)^(1/3) точно во всех пяти точках κ ∈ {0.25, 0.5, 1, 2, 4} — a от 0.908560296 до 2.289428485, — а время кристаллизации монотонно убывает от 24.341 до 5.609 (единицы 1/ω₀) по γ_d ∈ [0.4, 2.4] без передемпфированного подъёма внутри сканируемого окна.'}](figures/fig03_scaling_sweeps.png)

*{'cap_en': 'Parameter sweeps: (a) crystal side versus Coulomb strength κ — relaxation + Newton re-runs against the analytic cubic law; (b) crystallization settle time versus Doppler drag γ_d.', 'cap_ru': 'Развертки параметров: (а) сторона кристалла против кулоновской силы κ — прогоны релаксации с полировкой Ньютона против аналитического кубического закона; (б) время кристаллизации против доплеровского трения γ_d.', 'walk_en': 'Independent re-runs reproduce a(κ) = (3κ/ω₀²)^(1/3) exactly at all five κ ∈ {0.25, 0.5, 1, 2, 4} — a from 0.908560296 to 2.289428485 — while the settle time decreases monotonically from 24.341 to 5.609 (1/ω₀ units) over γ_d ∈ [0.4, 2.4], with no overdamped upturn inside the scanned window.', 'walk_ru': 'Независимые прогоны воспроизводят a(κ) = (3κ/ω₀²)^(1/3) точно во всех пяти точках κ ∈ {0.25, 0.5, 1, 2, 4} — a от 0.908560296 до 2.289428485, — а время кристаллизации монотонно убывает от 24.341 до 5.609 (единицы 1/ω₀) по γ_d ∈ [0.4, 2.4] без передемпфированного подъёма внутри сканируемого окна.'}.*

![{'cap_en': 'Crystallization dynamics: (a) worldlines of the three ions from the seeded random start into the crystal (γ_d = 0.8, T = 60); (b) cooling decay |U(t) − U_min| versus the conservative hold |E(t) − E(0)|.', 'cap_ru': 'Динамика кристаллизации: (а) мировые линии трёх ионов от засеянного случайного старта до кристалла (γ_d = 0.8, T = 60); (б) спад при охлаждении |U(t) − U_min| против консервативного удержания |E(t) − E(0)|.', 'walk_en': 'Cooling at γ_d = 0.8 releases the binding energy ΔU = 1.7609 and settles the triangle within the T = 60 window, while the conservative run started at the exact equilibrium keeps the energy drift at 8.9e-16 over t = 50 — the crystal is a frozen choreography.', 'walk_ru': 'Охлаждение при γ_d = 0.8 высвобождает энергию связи ΔU = 1.7609 и успокаивает треугольник внутри окна T = 60, а консервативный прогон из точного равновесия держит дрейф энергии на уровне 8.9e-16 на протяжении t = 50 — кристалл является замороженной хореографией.'}](figures/fig04_crystallization_dynamics.png)

*{'cap_en': 'Crystallization dynamics: (a) worldlines of the three ions from the seeded random start into the crystal (γ_d = 0.8, T = 60); (b) cooling decay |U(t) − U_min| versus the conservative hold |E(t) − E(0)|.', 'cap_ru': 'Динамика кристаллизации: (а) мировые линии трёх ионов от засеянного случайного старта до кристалла (γ_d = 0.8, T = 60); (б) спад при охлаждении |U(t) − U_min| против консервативного удержания |E(t) − E(0)|.', 'walk_en': 'Cooling at γ_d = 0.8 releases the binding energy ΔU = 1.7609 and settles the triangle within the T = 60 window, while the conservative run started at the exact equilibrium keeps the energy drift at 8.9e-16 over t = 50 — the crystal is a frozen choreography.', 'walk_ru': 'Охлаждение при γ_d = 0.8 высвобождает энергию связи ΔU = 1.7609 и успокаивает треугольник внутри окна T = 60, а консервативный прогон из точного равновесия держит дрейф энергии на уровне 8.9e-16 на протяжении t = 50 — кристалл является замороженной хореографией.'}.*

## 11. Results (full run)

```text
global_minimum_reached           = 0.0        (U_final = U_triangle = 3.120125734578)
crystallization_energy_released  = PASS       (binding energy 1.7609 released)
crystal_side_equals_analytic     = 1.442249570 (a = 3^(1/3) = 1.4422495703)
crystal_equilateral              = 4.4e-16    (max side - min side)
crystal_angles_120deg            = 4.4e-16    (2*pi/3 = 2.0943951 rad each)
zero_rotation_mode               = PASS
two_com_modes_at_omega0          = PASS
breathing_mode_sqrt3             = PASS (omega_b = 1.7320508 = sqrt(3))
static_equilibrium_holds         = 3.9e-15    (positions after t = 50)
conservative_energy_conserved    = 8.9e-16    (damping-free crystal, t = 50)
status: PASS (10/10)
```

## 12. Analysis

**Crystallization and global minimum.** From the seeded random start the damped relaxation releases the binding energy ΔU = 1.7609 and descends into the crystal well; after the Newton polish on the strict balance the potential equals the analytic triangle energy exactly — the recorded U_final − U_triangle is 0.0 against the 1e-9 tolerance, with U* = 3.120125734578. The two-stage design is what makes the check honest: the softened relaxation provides a robust landscape, and the strict polish ties the reported numbers to the ideal force balance (E2) rather than to the softening.

**Geometry of the crystal.** The polished triangle has mean side 1.4422495703074085 against the analytic 3^(1/3) = 1.4422495703074083 (agreement far inside the 1e-8 tolerance); the three sides are equal to 4.4e-16 and the three central angles equal 2π/3 = 2.0943951 rad each to 4.4e-16. The crystal recorded in the protocol sits on the canonical orientation with circumradius 0.8326832 = a/√3, but the orientation itself is a free zero mode of the isotropic trap.

**Mode ladder and invariants.** The finite-difference Hessian (h = 1e-4) returns frequencies {0.0, 0.999999997, 1.000000014, 1.224744867, 1.224744882, 1.732050810}: exactly one zero mode, two COM modes at ω₀ and one breathing mode at √3ω₀ = 1.7320508, with the maximum deviation from the analytic ladder of 1.4·10⁻⁸ against the 5e-6 tolerance. The conservative hold started exactly at the equilibrium keeps the positions fixed to 3.9e-15 over t = 50 and the total energy to 8.9e-16 — both round-off level, confirming that the crystal is a static exact solution of the damping-free dynamics.

**Scaling and drag response.** Five independent re-runs reproduce the cubic law a(κ) = (3κ/ω₀²)^(1/3) with no free fitting: the numeric sides 0.908560296, 1.144714243, 1.442249570, 1.817120593, 2.289428485 coincide with the analytic values at all five κ ∈ {0.25, 0.5, 1, 2, 4}. The drag sweep shows the settle time falling monotonically from 24.341 to 5.609 (1/ω₀ units) as γ_d grows over [0.4, 2.4] — the underdamped transient penalty dominates the scanned window and the overdamped upturn lies beyond γ_d = 2.4, so the preset γ_d = 0.8 sits in the transient-dominated regime with settle time 11.720.

## 13. Discussion and honest boundaries

The model is deliberately minimal: two-dimensional, harmonic pseudopotential, identical ions, and cooling reduced to a linear drag. Within these assumptions every reported number is an exact statement about the governing equations rather than a simulation of a specific apparatus. The natural extensions each preserve the verification style: photon-recoil heating added to the drag (a Fokker–Planck rather than deterministic cooling model), axial degrees of freedom and the full 3-D crystal, anharmonic and segmented trap geometries, and the micromotion corrections beyond the pseudopotential approximation — valid whenever the rf drive frequency greatly exceeds ω₀.

The parameter regime couples to real hardware through one scale. The dimensionless preset (ω₀ = κ = m = 1) maps to a Ca⁺ ion (m = 40 amu) in a 1 MHz trap through κ = q²/(4πε₀)/(mω₀²ℓ³), which sets the trap length scale ℓ and with it the crystal size a·ℓ; the drag γ_d = 0.8 encodes the Doppler cooling rate in units of ω₀. The softening ε_relax = 0.05 is the one effective parameter of the relaxation stage, and its role is documented and then removed: all acceptance checks are evaluated on the strict unsoftened balance, so the reported machine-precision agreement is not an artifact of the regularization.

Within the program this study is the matter-wave anchor of the Lagrange block. It shares the harmonic-balance logic with TRX-01, where the same equilateral configuration appears as the celestial libration points under a laser-renormalized gravity; it is the optical twin of TRX-03, where three solitons play the same central configuration with the same breathing-mode logic; and it hands the exact three-ion geometry and mode ladder to TRX-07, where quantum correlations are layered onto the same three-body skeleton. Together the three studies show the Lagrange triad operating across optics, celestial mechanics and laboratory quantum matter.

## 14. Conclusions

- Damped Doppler cooling crystallizes three ions into the equilateral Lagrange triangle; the two-stage protocol (softened relaxation, Newton polish on the strict balance) reaches the analytic crystal energy U* = 3.120125734578 with the recorded difference exactly 0.0 (tolerance 1e-9).
- The crystal geometry is machine-exact: side a = 3^(1/3) = 1.4422495703, sides equal to 4.4e-16, central angles 2π/3 = 2.0943951 rad each to 4.4e-16.
- The normal-mode ladder is confirmed by the finite-difference Hessian: exactly one zero mode (rigid rotation), two COM modes at ω₀, one breathing mode at √3ω₀ = 1.7320508; maximum deviation from the analytic ladder 1.4·10⁻⁸ against the 5e-6 tolerance.
- Started exactly at equilibrium, the conservative dynamics holds the crystal statically to 3.9e-15 over t = 50 with total-energy drift 8.9e-16 — the ion crystal is a frozen choreography.
- The scaling law a(κ) = (3κ/ω₀²)^(1/3) is reproduced without free parameters by independent relaxation + Newton re-runs at all five κ ∈ {0.25, 0.5, 1, 2, 4} (a from 0.908560296 to 2.289428485).
- The crystallization (settle) time decreases monotonically from 24.341 to 5.609 (1/ω₀ units) over the Doppler-drag window γ_d ∈ [0.4, 2.4]; the underdamped transient penalty dominates and the preset γ_d = 0.8 settles in 11.720.

## 15. The monograph and its renditions

The complete monograph of this study exists in four renditions — Russian and English are separate documents, each in a typeset PDF and an editable DOCX:

| Rendition | Path |
|---|---|
| Monograph (English, PDF) | `monograph/monograph_EN.pdf` |
| Monograph (English, DOCX) | `monograph/monograph_EN.docx` |
| Monograph (Russian, PDF) | `monograph/monograph_RU.pdf` |
| Monograph (Russian, DOCX) | `monograph/monograph_RU.docx` |
| Reading-room copy | `publications/pdf/TRX-08-ion-trap_EN.pdf` · `publications/pdf/TRX-08-ion-trap_RU.pdf` |
| HTML source | `publications/html/TRX-08-ion-trap.html` |

**Monograph abstract.** This monograph treats three laser-cooled ions in the transverse plane of a linear Paul trap as a table-top three-body problem: a two-dimensional harmonic rf pseudopotential confines the ions, their mutual Coulomb repulsion pushes them apart, and Doppler cooling — modelled as a linear drag −γ_d·v — dissipates energy until the ions crystallize. The study establishes, end to end and to machine precision, that the attractor of the cooled dynamics is the equilateral Lagrange triangle of side a = (3κ/ω₀²)^(1/3) = 3^(1/3) = 1.4422495703: a seeded relaxation with a documented wavepacket softening ε = 0.05, Newton-polished on the strict force balance, reproduces the analytic crystal energy U* = 3.120125734578 exactly, with all three sides equal to 4.4e-16 and central angles 2π/3 to 4.4e-16. The finite-difference Hessian confirms the full normal-mode ladder {0, ω₀ (×2), √(3/2)ω₀ (×2), √3ω₀} — one rigid-rotation zero mode, two centre-of-mass modes, one breathing mode — to 1.4·10⁻⁸ against the 5e-6 tolerance. Started exactly at equilibrium, the conservative dynamics holds the crystal statically to 3.9e-15 over fifty time units with energy drift 8.9e-16: the ion crystal is a frozen choreography, the trapped-ion twin of the Lagrange relative equilibrium.

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
| `t` | 2 | 0 … 1 |
| `x1` | 2 | -0.82870167 … -0.37791169 |
| `y1` | 2 | -0.52637899 … -0.74198654 |
| `x2` | 2 | 0.60254893 … 0.83153504 |
| `y2` | 2 | 0.16432407 … 0.04371215 |
| `x3` | 2 | -0.81174272 … -0.45362335 |
| `y3` | 2 | -0.13374612 … 0.6982744 |

**Reproduction matrix**

| Command | What it does |
|---|---|
| `python3 research/TRX-08-ion-trap/code/trx08_ion_trap.py` | full run: physics + acceptance checks (6.79 s (6.794 s recorded with --figures)) |
| `python3 research/TRX-08-ion-trap/code/trx08_ion_trap.py --smoke` | CI guard: same checks, seconds-scale settings |
| `python3 research/TRX-08-ion-trap/code/trx08_ion_trap.py --figures` | regenerates the 300-dpi figure set |
| `make research-smoke` | all twelve studies in smoke mode |
| `make research-figures` | all twelve studies + figure sets |

## 17. Cross-links within the program

- **TRX-03** is the optical twin: three solitons in a mode-locked fibre play the same central configuration with the same breathing-mode logic.
- **TRX-07** adds quantum correlations (Efimov physics) to the same three-body geometry this study fixes classically.
- **TRX-01** uses the same harmonic-trap-like balance in the celestial setting of the libration points.

## 18. Inside the script

The executable is a single deterministic file, `code/trx08_ion_trap.py`, ~pure `numpy`/`scipy` with no network access and no random state beyond fixed seeds. One run executes the full physics of the study, evaluates every registered acceptance check against its committed target and tolerance, and writes the JSON protocol — the same file quoted in §9.

| Mode | Invocation | What happens |
|---|---|---|
| Full | `python3 code/trx08_ion_trap.py` | complete experiment, all checks, JSON protocol (6.79 s (6.794 s recorded with --figures)) |
| Smoke | `python3 code/trx08_ion_trap.py --smoke` | identical acceptance logic at seconds-scale settings — the CI mode |
| Figures | `python3 code/trx08_ion_trap.py --figures` | regenerates the schematic + the four 300-dpi PNG panels |

**Outputs per run**

| File | Produced by | Content |
|---|---|---|
| `results/trx08_results.json` | every mode | status, checks (value/target/tol/unit/pass/note), series, meta |
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
| Previous study | TRX-007 |
| Next study | TRX-009 |

## 21. Notation

| Symbol | Meaning |
|---|---|
| r_k = (x_k, y_k) | position of ion k in the transverse plane |
| ω₀ | trap pseudopotential frequency (preset 1) |
| κ | Coulomb strength (preset 1) |
| γ_d | Doppler-drag coefficient (preset 0.8) |
| ε, ε_relax | Coulomb softening; 1e-12 in the polish, 0.05 in the relaxation |
| a | equilateral crystal side, a = (3κ/ω₀²)^(1/3) = 3^(1/3) |
| U | total potential energy (trap + Coulomb) |
| H | 6×6 position Hessian of U at the crystal |
| ΔU | binding energy released during cooling (= 1.7609) |
| T_relax, T_hold | relaxation (60) and static-hold (50) time spans |
| t_s | settle time from the drag sweep |

## 22. References

1. Paul, W., Steinwedel, H. (1953). *Ein neues Massenspektrometer ohne Magnetfeld.* Zeitschrift für Naturforschung A 8, 448–450.
2. Paul, W. (1990). *Electromagnetic traps for charged and neutral particles.* Reviews of Modern Physics 62, 531–540.
3. Itano, W. M., Wineland, D. J. (1982). *Laser cooling of ions stored in harmonic and Penning traps.* Physical Review A 25, 35–54.
4. Diedrich, F., Peik, E., Chen, J. M., Quint, W., Walther, H. (1987). *Observation of a phase transition of stored laser-cooled ions.* Physical Review Letters 59, 2931–2934.
5. Cirac, J. I., Zoller, P. (1995). *Quantum computations with cold trapped ions.* Physical Review Letters 74, 4091–4094.
6. James, D. F. V. (1998). *Quantum dynamics of cold trapped ions with application to quantum computation.* Applied Physics B 66, 181–190.
7. Dubin, D. H. E., O'Neil, T. M. (1999). *Trapped nonneutral plasmas, liquids, and crystals.* Reviews of Modern Physics 71, 87–172.
8. Blatt, R., Roos, C. F. (2012). *Quantum simulations with trapped ions.* Nature Physics 8, 277–284.

## 23. Glossary

| Term | Definition |
|---|---|
| Paul trap | radiofrequency quadrupole trap confining charged particles in an oscillating inhomogeneous field |
| rf pseudopotential | time-averaged effective potential of the rf drive; harmonic (mω₀²r²/2) in the trap plane |
| Doppler cooling | laser cooling by red-detuned light; modelled here as a linear drag −γ_d·v |
| Ion crystal | ordered configuration of trapped ions fixed by the balance of confinement and Coulomb repulsion |
| Lagrange triangle | the equilateral central configuration of the three-body problem; here the three-ion crystal |
| Normal modes | small-oscillation eigenmodes of the Hessian; here 0, ω₀ (×2), √(3/2)ω₀ (×2), √3ω₀ |
| Breathing mode | the √3ω₀ mode in which the triangle expands and contracts radially |
| Zero mode | the Hessian nullspace direction — free rigid rotation (orientation) of the crystal in the isotropic trap |
| Softening ε | regularization κ·r/(r² + ε²)^(3/2) of the Coulomb singularity; 0.05 in relaxation, 1e-12 in the polish |
| Settle time | first moment the side spread of the relaxing triangle stays below 0.01 |

## 24. Appendix A. Full parameter table

| Symbol | Value | Role |
|---|---|---|
| ω₀, κ, m | 1, 1, 1 | dimensionless trap frequency, Coulomb strength, ion mass |
| γ_d | 0.8 | Doppler drag during relaxation |
| ε_relax → ε | 0.05 → 1e-12 | softening in relaxation, strict balance in the polish |
| T_relax, T_hold | 60, 50 | relaxation and static-hold spans |
| initial condition | seeded random in [−1, 1]², v = 0 (seed 3) | crystallization start |
| settle criterion | side spread below 0.01 | gamma-sweep settle time |
| sweeps | κ ∈ {0.25, 0.5, 1, 2, 4}; γ_d ∈ {0.4, 0.6, 0.8, 1.2, 1.6, 2.4} | scaling and drag-response re-runs |
| Ca⁺ scale | m = 40 amu, trap 1 MHz | physical mapping; κ sets the length scale |

**Protocol-level parameter snapshot** (`results` JSON, `meta` block):

| Key | Value |
|---|---|
| `equations` | `["m x_k'' = -m omega0^2 x_k - gamma_d x_k' + kappa sum (x_k-x_l)/r^3", "a = (3 kappa/omega0^2)^(1/3) ;  modes: 0, omega0 (x2), sqrt(3) omega0, ..."]` |
| `a_analytic` | `1.4422495703074083` |
| `mode_frequencies` | `[0.0, 0.9999999969612642, 1.0000000136146097, 1.2247448672197627, 1.2247448824186384, 1.732050809523816]` |
| `Ca_params` | `{"m_amu": 40, "trap_MHz": 1.0, "note": "kappa = q^2/(4 pi eps0) / (m omega0^2 a0^3) sets the length scale"}` |
| `laser_link` | `"Doppler cooling modelled by gamma_d; three-ion crystals are the smallest ion-crystal quantum simulator"` |

## 25. Appendix B. BibTeX

```bibtex
@article{paul1990,
  author  = {Paul, W.},
  title   = {Electromagnetic traps for charged and neutral particles},
  journal = {Reviews of Modern Physics},
  year    = {1990}, volume = {62}, pages = {531--540}}

@article{itano1982,
  author  = {Itano, W. M. and Wineland, D. J.},
  title   = {Laser cooling of ions stored in harmonic and Penning traps},
  journal = {Physical Review A},
  year    = {1982}, volume = {25}, pages = {35--54}}

@article{diedrich1987,
  author  = {Diedrich, F. and Peik, E. and Chen, J. M. and Quint, W. and Walther, H.},
  title   = {Observation of a phase transition of stored laser-cooled ions},
  journal = {Physical Review Letters},
  year    = {1987}, volume = {59}, pages = {2931--2934}}

@article{dubin1999,
  author  = {Dubin, D. H. E. and O'Neil, T. M.},
  title   = {Trapped nonneutral plasmas, liquids, and crystals},
  journal = {Reviews of Modern Physics},
  year    = {1999}, volume = {71}, pages = {87--172}}
```

## 26. How to cite

Cite the repository through [`CITATION.cff`](../../CITATION.cff) (DOI 10.5281/zenodo.21825394, version 1.0.0); this study is part of the TRIVORTEX Research Program. If you cite the study alone, name the monograph rendition you used and attach the JSON protocol of the run you reproduced.

```bibtex
@misc{trivortextrx082026isaev,
  author       = {Isaev, Iskhak Khamzatovich},
  title        = {Three Laser-Cooled Ions in a Linear Paul Trap: the Table-Top Lagrange Triangle (TRIVORTEX Research Program, TRX-08)},
  year         = {2026},
  howpublished = {Zenodo},
  doi          = {10.5281/zenodo.21825394},
  url          = {https://github.com/wild8highlander/Trivortex}
}
```

