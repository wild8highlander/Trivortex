# TRIVORTEX Research Compendium

*TRIVORTEX Research Program v1.0.0 · EN edition*

|  |  |
|---|---|
| Program | TRIVORTEX — Trivortex |
| Author | Isaev Iskhak Khamzatovich (ORCID 0009-0003-7299-0701) |
| DOI | 10.5281/zenodo.21825394 |
| Version | 1.0.0 — first public release |
| License | LicenseRef-Proprietary-Wild8Highlander-1.0 |

## Abstract

TRIVORTEX is a research program around the three-body problem. Twelve companion studies — each an executable script, a committed JSON protocol and a bilingual monograph — attack the problem through twelve physical systems, with lasers at the center of ten of them. The table lists the headline verified number of every study; the dossiers that follow quote the full machine-readable protocol of each.

## 1. The program at a glance

TRIVORTEX is a research program around the three-body problem. Twelve companion studies — each an executable script, a committed JSON protocol and a bilingual monograph — attack the problem through twelve physical systems, with lasers at the center of ten of them. The table lists the headline verified number of every study; the dossiers that follow quote the full machine-readable protocol of each.

| # | Study | Directory | Status |
|---|---|---|---|
| TRX-01 | Radiation-Pressure Restricted Three-Body Problem (Laser on Dust) | `TRX-01-laser-radiation-pressure` | PASS |
| TRX-02 | Resonant Three-Wave Interaction (ManleyâRowe, Ïâ½Â²â¾ Optics) | `TRX-02-three-wave-mixing` | PASS |
| TRX-03 | Three-Soliton Molecule in a Mode-Locked Fiber Laser | `TRX-03-soliton-molecule` | PASS |
| TRX-04 | Photon Fluid: Three Kerr Solitons (Spatial, 2-D) | `TRX-04-photon-fluid` | PASS |
| TRX-05 | Optical Vortices of Laser Beams and the Point-Vortex Analogy | `TRX-05-optical-vortices` | PASS |
| TRX-06 | Helium Atom as the Coulomb Three-Body Problem (Classical Trajectory Monte Carlo) | `TRX-06-helium-three-body` | PASS |
| TRX-07 | The Efimov Effect: Universal Quantum Three-Body Physics | `TRX-07-efimov` | PASS |
| TRX-08 | Three Laser-Cooled Ions in a Linear Paul Trap: the Table-Top Lagrange Triangle | `TRX-08-ion-trap` | PASS |
| TRX-09 | The KirchhoffâChaplygin Three-Vortex Problem (Classical Anchor) | `TRX-09-vortex-trio` | PASS |
| TRX-10 | KozaiâLidov Oscillations in Hierarchical Triples | `TRX-10-kozai-lidov` | PASS |
| TRX-11 | Gravitational Waves from the Figure-Eight Choreography | `TRX-11-gw-choreography` | PASS |
| TRX-12 | Laser Highway: Light-Sail Stationkeeping at L4/L5 | `TRX-12-laser-light-sail` | PASS |

## 2. Study dossiers

Each dossier quotes the acceptance checks exactly as committed in `research/TRX-*/results/trx*_results.json` — check, measured value, target, tolerance and verdict. Nothing here is retyped by hand: this chapter is assembled by `publications/build/build_special_pdfs.py` directly from the committed protocols.

### TRX-01 — Radiation-Pressure Restricted Three-Body Problem (Laser on Dust)

The circular restricted three-body problem (CR3BP) in which primary 1 is illuminated by an intense laser beam. Photon radiation pressure reduces the effective pull of that primary on a massless particle by the factor (1 â Î²), with Î² = F_rad / F_grav â the "laser-dressed" CR3BP. The laser acts as a third physical agent that reshapes the libration-point landscape without adding a mass.

|  |  |
|---|---|
| Study | `TRX-01-laser-radiation-pressure` |
| Status | **PASS** |
| Full-run time | 0.10 s |
| Code | `research/TRX-01-laser-radiation-pressure/code/` |
| Monograph | `publications/pdf/TRX-01-laser-radiation-pressure_EN.pdf` |

**Acceptance checks**

| check | measured | target | tolerance | Status |
|---|---|---|---|---|
| `L1_abscissa_beta0` | 0.836915 | 0.836915 | 5.000e-06 | PASS |
| `L4_shift_monotone_in_beta` | 1 | 1 | 1.000e-12 | PASS |
| `L4_shift_toward_radiating_primary` | 1 | 1 | 1.000e-12 | PASS |
| `L4_max_Re_eigenvalue_beta0` | 1.857e-16 | 0 | 1.000e-08 | PASS |
| `L1_shifts_toward_radiating_primary` | 1 | 1 | 1.000e-12 | PASS |
| `Jacobi_drift_L4_orbit_beta0.05` | 8.882e-16 | 0 | 1.000e-10 | PASS |

### TRX-02 — Resonant Three-Wave Interaction (ManleyâRowe, Ïâ½Â²â¾ Optics)

Resonant three-wave mixing in a lossless, phase-matched Ïâ½Â²â¾ crystal â the canonical "three-body problem of nonlinear optics". A pump wave at Ïâ = Ïâ + Ïâ exchanges photons with a signalâidler pair; the ManleyâRowe relations keep the photon bookkeeping exact, and the equal-coupling amplitude equations are canonically equivalent to the Euler top â the same integrable family as the Kirchhoff three-vortex problem that underlies Theorem 3.1 of TRIVORTEX.

|  |  |
|---|---|
| Study | `TRX-02-three-wave-mixing` |
| Status | **PASS** |
| Full-run time | 0.6 s |
| Code | `research/TRX-02-three-wave-mixing/code/` |
| Monograph | `publications/pdf/TRX-02-three-wave-mixing_EN.pdf` |

**Acceptance checks**

| check | measured | target | tolerance | Status |
|---|---|---|---|---|
| `ManleyRowe_I13_drift` | 5.107e-15 | 0 | 1.000e-10 | PASS |
| `ManleyRowe_I23_drift` | 1.776e-15 | 0 | 1.000e-10 | PASS |
| `ManleyRowe_I12diff_drift` | 3.775e-15 | 0 | 1.000e-10 | PASS |
| `Pump_period_repeatability` | 4.470e-08 | 0 | 1.000e-06 | PASS |
| `Pump_revival_error` | 2.442e-15 | 0 | 1.000e-08 | PASS |
| `Pump_full_depletion_occurs` | 1 | 1 | 1.000e-12 | PASS |
| `SHG_tanh2_conversion_error` | 2.220e-16 | 0 | 1.000e-08 | PASS |

### TRX-03 — Three-Soliton Molecule in a Mode-Locked Fiber Laser

Three ultrashort pulses circulating in a passively mode-locked fiber laser form a phase-locked "soliton molecule": in the reduced particle picture each pulse is a body with the conservative, phase-dependent pair interaction V(r, ÎÏ) = Câe^(â2r/L) â Câe^(âr/L)cos 2ÎÏ. The phase-locked triplet is a genuine optical three-body choreography: its equilibrium spacing s*is fixed by the three-body balance F(s*) + F(2s*) = 0, is compressed â 30 % below the pair value râ = ln(4/3), and supports a breathing normal mode verified by FFT against the Hessian prediction to 0.21 %.

|  |  |
|---|---|
| Study | `TRX-03-soliton-molecule` |
| Status | **PASS** |
| Full-run time | 1.2 s (4.7 s with --figures) |
| Code | `research/TRX-03-soliton-molecule/code/` |
| Monograph | `publications/pdf/TRX-03-soliton-molecule_EN.pdf` |

**Acceptance checks**

| check | measured | target | tolerance | Status |
|---|---|---|---|---|
| `pair_equilibrium_numeric_vs_analytic` | 5.551e-17 | 0 | 1.000e-10 | PASS |
| `antiphase_pi2_purely_repulsive` | 1 | 1 | 1.000e-12 | PASS |
| `molecule_final_spacings_equal` | 2.220e-16 | 0 | 1.000e-08 | PASS |
| `molecule_final_spacing_equals_s_star` | 2.776e-17 | 0 | 1.000e-06 | PASS |
| `conservative_energy_drift` | 1.332e-15 | 0 | 1.000e-10 | PASS |
| `breathing_mode_frequency` | 0.468825 | 0.468766 | 0.00468766 | PASS |

### TRX-04 — Photon Fluid: Three Kerr Solitons (Spatial, 2-D)

Three laser beams co-propagating in a focusing Kerr medium behave as a photon fluid: each beam is a spatial soliton of the nonlinear SchrÃ¶dinger equation, and pairs of beams exchange conservative two-body forces whose sign is set by the relative phase â in-phase beams attract, anti-phase beams repel â with the exponential profile V(r) = âUÂ·e^(âr/w). The in-phase triplet realizes an optical Lagrange central configuration: an equilateral beam triangle of side a = 3 rotates rigidly at Ï = e^(â3/2) = 0.223130160, the exponential-force counterpart of the Newtonian ÏÂ² = 3Gm/aÂ³ of Theorem 3.1. The study verifies the choreography to machine precision: the triangle stays equilateral to 1.8e-08 over three full rotations, the measured rotation rate matches the analytic law to 1.1Ã10â»Â¹Â¹, energy and angular momentum are conserved to 4.7e-16 and 2.2e-15, the anti-phase trio expands cleanly to 23.476, and an in-phase binary stays bound with a precessing orbit â an optical three-body scattering table closed by 9/9 checks PASS.

|  |  |
|---|---|
| Study | `TRX-04-photon-fluid` |
| Status | **PASS** |
| Full-run time | 9.4 s (9.415 s recorded with --figures) |
| Code | `research/TRX-04-photon-fluid/code/` |
| Monograph | `publications/pdf/TRX-04-photon-fluid_EN.pdf` |

**Acceptance checks**

| check | measured | target | tolerance | Status |
|---|---|---|---|---|
| `triangle_equilateral_deviation` | 4.441e-15 | 0 | 1.000e-06 | PASS |
| `measured_rotation_rate` | 0.22313 | 0.22313 | 1.000e-08 | PASS |
| `energy_conservation_rotation` | 2.220e-16 | 0 | 1.000e-10 | PASS |
| `angular_momentum_conservation` | 8.882e-16 | 0 | 1.000e-10 | PASS |
| `antiphase_no_collapse` | 1 | 1 | 1.000e-12 | PASS |
| `antiphase_expands` | 1 | 1 | 1.000e-12 | PASS |
| `energy_conservation_repulsion` | 3.053e-16 | 0 | 1.000e-10 | PASS |
| `binary_stays_bound` | 1 | 1 | 1.000e-12 | PASS |
| `binary_energy_conservation` | 1.771e-12 | 0 | 1.000e-10 | PASS |

### TRX-05 — Optical Vortices of Laser Beams and the Point-Vortex Analogy

Three phase singularities â optical vortices â of a paraxial laser field behave, to leading order, exactly like Kirchhoff point vortices of ideal fluid dynamics. The study realizes the vortex representation of TRIVORTEX *literally in light*: three same-sign singularities of the field Ï(z) = exp(ârÂ²/wÂ²)Â·Î (z â z_k) sit on an equilateral triangle of side a = 1 and rotate rigidly with the analytic angular velocity Ï = 3Î/(2ÏaÂ²) = 0.477464829, measured to 1e-8, while the angular impulse I = Î£Î|r|Â² (the many-vortex prototype of the Chaplygin integral) stays pinned at aÂ² = 1 and the winding number of the rendered field equals 3 exactly â the analogue of orbital angular momentum 3â per photon.

|  |  |
|---|---|
| Study | `TRX-05-optical-vortices` |
| Status | **PASS** |
| Full-run time | 4.83 s (4.827 s recorded with --figures) |
| Code | `research/TRX-05-optical-vortices/code/` |
| Monograph | `publications/pdf/TRX-05-optical-vortices_EN.pdf` |

**Acceptance checks**

| check | measured | target | tolerance | Status |
|---|---|---|---|---|
| `rotation_rate_vs_analytic` | 0.477465 | 0.477465 | 1.000e-08 | PASS |
| `angular_impulse_I_conserved` | 1.332e-15 | 0 | 1.000e-12 | PASS |
| `kirchhoff_hamiltonian_conserved` | 3.534e-16 | 0 | 1.000e-12 | PASS |
| `field_minima_track_vortices` | 0.016125 | 0 | 0.06 | PASS |
| `total_winding_number_is_3` | 3 | 3 | 1.000e-12 | PASS |

### TRX-06 — Helium Atom as the Coulomb Three-Body Problem (Classical Trajectory Monte Carlo)

The helium atom â a nucleus of charge Z = 2 and two electrons â is the smallest physical system whose classical limit is the honest three-body problem: two attractive and one repulsive Coulomb pair, all of order unity. The study runs a deterministic classical trajectory Monte Carlo (CTMC) ensemble of 3200 trajectories launched in the Wannier configuration â a radially staggered chain at hyperradius Râ = 3 on the exact energy shell, with a fixed kick Ï = 0.01 and a documented softening Îµ = 0.1 a.u. â and measures the autoionization channel: one electron is captured while the other escapes carrying on average 7.28Ã the excess energy, the fingerprint of three-body energy transfer through the eâ»âeâ» repulsion. The double-escape statistics are read against Wannier's threshold law P_DE â E^1.056, reported honestly for the strong-coupling regime of the fixed-launch geometry.

|  |  |
|---|---|
| Study | `TRX-06-helium-three-body` |
| Status | **PASS** |
| Full-run time | 37.7 s |
| Code | `research/TRX-06-helium-three-body/code/` |
| Monograph | `publications/pdf/TRX-06-helium-three-body_EN.pdf` |

**Acceptance checks**

| check | measured | target | tolerance | Status |
|---|---|---|---|---|
| `max_relative_energy_drift_valid` | 2.884e-06 | 0 | 4.000e-04 | PASS |
| `outcome_classes_sum_to_N` | 120 | 120 | 1.000e-12 | PASS |
| `autoionization_channel_active` | 1 | 1 | 1.000e-12 | PASS |
| `escaping_electron_energy_overshoot` | 1 | 1 | 1.000e-12 | PASS |
| `fit_reproducible` | 1 | 1 | 1.000e-12 | PASS |

### TRX-07 — The Efimov Effect: Universal Quantum Three-Body Physics

Three identical bosons with resonant (unitary) two-body interactions form an infinite Rydberg-like series of bound three-body states â Efimov trimers â even though the pair potential binds no dimer. The spectrum is universal: it is governed by a single transcendental exponent s0 defined by s0Â·cosh(Ïs0/2) = (8/â3)Â·sinh(Ïs0/6), s0 = 1.0062378 (target 1.0062458), and it is organized in a geometric ladder â trimer sizes grow by exp(Ï/s0) = 22.694383 and energies drop by exp(2Ï/s0) = 515.035001 per rung. The study realizes the ladder numerically on the hyperradial adiabatic potential â(s0Â² â Â¼)/RÂ²: the four computed trimers reproduce the universal energy ratio within Â±0.1% (515.509 / 514.964 / 514.963), and a three-body-parameter sweep shows the ratios invariant (spread 1.9Â·10â»Â¹â°) while absolute energies follow the exact R0â»Â² power law â the quantum twin of the scale-invariant vortex triangle of TRIVORTEX.

|  |  |
|---|---|
| Study | `TRX-07-efimov` |
| Status | **PASS** |
| Full-run time | 5.77 s (5.771 s recorded with --figures) |
| Code | `research/TRX-07-efimov/code/` |
| Monograph | `publications/pdf/TRX-07-efimov_EN.pdf` |

**Acceptance checks**

| check | measured | target | tolerance | Status |
|---|---|---|---|---|
| `s0_transcendental_root` | 1.00624 | 1.00625 | 1.000e-05 | PASS |
| `efimov_length_ratio` | 22.6944 | 22.7 | 0.05 | PASS |
| `efimov_energy_ratio` | 515.035 | 515.03 | 0.05 | PASS |
| `spectrum_all_negative` | 1 | 1 | 1.000e-12 | PASS |
| `ladder_ratio_E0_over_E1` | 515.477 | 515.035 | 180.262 | PASS |
| `ladder_ratio_E1_over_E2` | 514.932 | 515.035 | 180.262 | PASS |

### TRX-08 — Three Laser-Cooled Ions in a Linear Paul Trap: the Table-Top Lagrange Triangle

Three laser-cooled ions in the transverse plane of a linear Paul trap form a table-top three-body problem: a two-dimensional harmonic rf pseudopotential confines them, their mutual Coulomb repulsion pushes them apart, and Doppler cooling â modelled as a linear drag âÎ³_dÂ·v â dissipates energy until the ions crystallize into the equilateral Lagrange triangle of side a = (3Îº/ÏâÂ²)^(1/3) = 3^(1/3) = 1.4422495703. The study verifies the whole chain to machine precision: sides equal to 4.4e-16, central angles 2Ï/3 to 4.4e-16, the normal-mode ladder {0, Ïâ (Ã2), â(3/2)Ïâ (Ã2), â3Ïâ} confirmed to 1.4Â·10â»â¸, and a conservative hold at the exact equilibrium that keeps the crystal static to 3.9e-15 over fifty time units with energy drift 8.9e-16 â the trapped-ion twin of the Lagrange relative equilibrium behind TRIVORTEX Theorem 3.1 and the smallest ion-crystal quantum simulator.

|  |  |
|---|---|
| Study | `TRX-08-ion-trap` |
| Status | **PASS** |
| Full-run time | 6.79 s (6.794 s recorded with --figures) |
| Code | `research/TRX-08-ion-trap/code/` |
| Monograph | `publications/pdf/TRX-08-ion-trap_EN.pdf` |

**Acceptance checks**

| check | measured | target | tolerance | Status |
|---|---|---|---|---|
| `global_minimum_reached` | 0 | 0 | 1.000e-09 | PASS |
| `crystallization_energy_released` | 1 | 1 | 1.000e-12 | PASS |
| `crystal_side_equals_analytic` | 1.44225 | 1.44225 | 1.000e-08 | PASS |
| `crystal_equilateral` | 0 | 0 | 1.000e-08 | PASS |
| `crystal_angles_120deg` | 4.441e-16 | 0 | 1.000e-06 | PASS |
| `zero_rotation_mode` | 1 | 1 | 1.000e-12 | PASS |
| `two_com_modes_at_omega0` | 1 | 1 | 1.000e-12 | PASS |
| `breathing_mode_sqrt3` | 1 | 1 | 1.000e-12 | PASS |
| `static_equilibrium_holds` | 1.388e-15 | 0 | 1.000e-09 | PASS |
| `conservative_energy_conserved` | 8.882e-16 | 0 | 1.000e-10 | PASS |

### TRX-09 — The KirchhoffâChaplygin Three-Vortex Problem (Classical Anchor)

The classical point-vortex anchor of TRIVORTEX: three Kirchhoff vortices with circulations Î1, Î2, Î3 and the angular impulse I = Î£Î|r|Â² â the prototype of the Chaplygin topological integral C_Ch of Theorem 3.1. Two canonical regimes are verified numerically: the same-sign equilateral triangle rotates rigidly with Ï = 3Î/(2ÏaÂ²) = 0.477464829 (the vortex Lagrange solution), and the mixed-sign (1, 1, â1) trio launched from the right-isosceles configuration sits exactly on the Aref collapse manifold I = H = P = Q = 0 and evolves non-rigidly while all four invariants stay pinned to machine precision.

|  |  |
|---|---|
| Study | `TRX-09-vortex-trio` |
| Status | **PASS** |
| Full-run time | 0.54 s (7.389 s recorded with --figures) |
| Code | `research/TRX-09-vortex-trio/code/` |
| Monograph | `publications/pdf/TRX-09-vortex-trio_EN.pdf` |

**Acceptance checks**

| check | measured | target | tolerance | Status |
|---|---|---|---|---|
| `rotation_rate_3G_over_2pi_a2` | 0.477465 | 0.477465 | 1.000e-08 | PASS |
| `triangle_stays_equilateral` | 3.331e-16 | 0 | 1.000e-08 | PASS |
| `angular_impulse_I_conserved` | 8.882e-16 | 0 | 1.000e-12 | PASS |
| `hamiltonian_conserved` | 2.474e-16 | 0 | 1.000e-12 | PASS |
| `linear_impulse_conserved` | 7.216e-16 | 0 | 1.000e-12 | PASS |
| `aref_collapse_conditions_hold` | 1.388e-17 | 0 | 1.000e-12 | PASS |
| `mixed_sign_invariants_conserved` | 1.310e-14 | 0 | 1.000e-11 | PASS |
| `mixed_sign_shape_evolves` | 1 | 1 | 1.000e-12 | PASS |

### TRX-10 — KozaiâLidov Oscillations in Hierarchical Triples

The KozaiâLidov mechanism: a test particle on an inclined inner orbit of a hierarchical triple, perturbed by a distant companion, periodically exchanges eccentricity for inclination while the z-angular momentum j_z = â(1 â eÂ²)Â·cos i stays constant; for a nearly circular initial orbit the eccentricity climbs to the closed-form maximum e_max = â(1 â (5/3)Â·cosÂ²iâ) whenever iâ exceeds the Kozai angle 39.23Â°. The study refuses to code the memorized result: the doubly-averaged quadrupole potential is built numerically â orbit quadrature, (e, Ï) tabulation, cubic-spline Hamiltonian â and the resulting flow is audited against analytic benchmarks and an independent direct integration of the full three-dimensional restricted problem.

|  |  |
|---|---|
| Study | `TRX-10-kozai-lidov` |
| Status | **PASS** |
| Full-run time | 64.6 s |
| Code | `research/TRX-10-kozai-lidov/code/` |
| Monograph | `publications/pdf/TRX-10-kozai-lidov_EN.pdf` |

**Acceptance checks**

| check | measured | target | tolerance | Status |
|---|---|---|---|---|
| `e_max_i0_60` | 0.763752 | 0.763763 | 0.002 | PASS |
| `e_max_i0_70` | 0.897229 | 0.897239 | 0.002 | PASS |
| `kl_period_halves_with_m3` | 0.493173 | 0.5 | 0.03 | PASS |

### TRX-11 — Gravitational Waves from the Figure-Eight Choreography

The figure-eight choreography (Chenciner & Montgomery 2000) â three equal masses chasing each other along a single closed curve with zero angular momentum â is treated as a laboratory gravitational-wave source. In the quadrupole approximation (G = c = D = 1) the mass quadrupole Q_ij = Î£ m_k x_ki x_kj drives a plus-polarised strain that repeats six times per orbit period T = 6.325914, and the choreography symmetry locks the spectrum into a pure harmonic comb with the dominant line at n = 6 of the orbital comb.

|  |  |
|---|---|
| Study | `TRX-11-gw-choreography` |
| Status | **PASS** |
| Full-run time | 8.17 s |
| Code | `research/TRX-11-gw-choreography/code/` |
| Monograph | `publications/pdf/TRX-11-gw-choreography_EN.pdf` |

**Acceptance checks**

| check | measured | target | tolerance | Status |
|---|---|---|---|---|
| `period_closure_error` | 1.232e-08 | 0 | 5.000e-08 | PASS |
| `period_in_expected_range` | 1 | 1 | 1.000e-12 | PASS |
| `energy_conserved` | 3.331e-15 | 0 | 1.000e-12 | PASS |
| `angular_momentum_is_zero` | 1.443e-15 | 0 | 1.000e-09 | PASS |
| `luminosity_finite_positive` | 1 | 1 | 1.000e-12 | PASS |
| `dominant_harmonic_on_comb` | 0.00149963 | 0 | 0.05 | PASS |

### TRX-12 — Laser Highway: Light-Sail Stationkeeping at L4/L5

A photon light sail in the EarthâMoon circular restricted three-body problem, pushed by a 1 MW laser beam: the thrust a_L = 2P/(cm) is pointed by a proportional-derivative beam-steering law and capped by the photon ceiling a_max = 0.2443 (dimensionless). The study demonstrates the two core operations of a "laser highway" â holding a spacecraft at the linearly stable but neutrally drifting L4 point to 7.5e-07 of the nominal position, and pumping the Jacobi constant down with along-velocity thrust to move between invariant manifolds.

|  |  |
|---|---|
| Study | `TRX-12-laser-light-sail` |
| Status | **PASS** |
| Full-run time | 41.4 s |
| Code | `research/TRX-12-laser-light-sail/code/` |
| Monograph | `publications/pdf/TRX-12-laser-light-sail_EN.pdf` |

**Acceptance checks**

| check | measured | target | tolerance | Status |
|---|---|---|---|---|
| `controlled_l4_bound` | 8.763e-05 | 0 | 2.000e-04 | PASS |
| `control_saturation_fraction` | 0 | 0 | 0.05 | PASS |
| `free_drift_never_converges` | 1 | 1 | 1.000e-12 | PASS |
| `jacobi_pumped_monotonically` | 1 | 1 | 1.000e-12 | PASS |
| `power_table_consistent` | 1 | 1 | 1.000e-12 | PASS |

## 4. Reproduction

```bash
# smoke: all twelve acceptance suites in seconds (what CI runs)
for d in research/TRX-*/code/*.py; do python3 "$d" --smoke; done

# full: every study, full statistics, JSON protocols
for d in research/TRX-*/code/*.py; do python3 "$d"; done

# ultra-resolution figure sets (300 dpi)
for d in research/TRX-*/code/*.py; do python3 "$d" --figures; done
```

**3. The verification discipline** — Every study is a deterministic script (numpy/scipy only) that executes its physics, compares the measured numbers against published or registered targets, and writes a JSON protocol with a full parameter snapshot. The `--smoke` mode runs the same acceptance logic in seconds and is wired into CI; the full mode and the `--figures` mode regenerate the 300-dpi figure set. A study passes only when every check is green — the same discipline the core verification ladder V1–V4 applies to Theorem 3.1 of the vortex document.
