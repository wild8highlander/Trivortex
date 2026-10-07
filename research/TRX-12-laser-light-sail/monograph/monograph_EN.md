# Laser Highway: Light-Sail Stationkeeping at L4/L5

*TRIVORTEX Research Program · v1.0.0 · Monograph Edition*

|  |  |
|---|---|
| Study | TRX-12 |
| Program | TRIVORTEX — The Three-Body Problem in the Vortex Model |
| Author | Isaev Iskhak Khamzatovich (ORCID 0009-0003-7299-0701) |
| DOI | 10.5281/zenodo.21825394 |
| Date | 2026-10-06 |
| Code | `code/trx12_laser_light_sail.py` |
| Data | `results/trx12_results.json` |

## Abstract

This monograph treats a photon light sail in the Earth–Moon circular restricted three-body problem as an actuated libration-point system: a 1 MW laser pushes a 10 kg sail with photon thrust a_L = 2P/(cm), capped at the dimensionless ceiling a_max = 0.2443, and a proportional-derivative beam-steering law points the thrust. Two operations of the laser highway are verified. Stationkeeping: starting 1.1·10⁻³ away from the linearly stable L4 point, the controlled sail converges to |r − L4| ≤ 7.5e-07 for all t > T/4 (T = 100, ≈ 434 days) while using the photon ceiling 0% of the time (peak demand 0.0051, headroom 48×); the same initial state without control never comes closer than 0.0041 — a contrast of ≈ 5500×. Orbit raising: open-loop thrust along velocity pumps the Jacobi constant strictly monotonically, net ΔC_J = 1063.51 over T = 30 with the largest single-step increase at −0.06. A 17 × 17 PD gain-plane sweep brackets the operating point (4, 4), and an SI power table (57.8 kW … 2.89 MW per 100 kg and 30 days) closes the model to engineering numbers.

## Contents

1. Abstract
2. 1. Introduction and historical context
3. 1. Physical formulation
4. 1. Mathematical model
5. 1. Connection to the TRIVORTEX framework
6. 1. Numerical method
7. 1. Results and analysis
8. 1. Discussion
9. 1. Conclusions
10. 1. References
Appendix A. Parameter table
Appendix B. Reproduction

## 1. Introduction and historical context

The equilateral solutions of the three-body problem were found by Joseph-Louis Lagrange in his 1772 *Essai sur le problème des trois corps*, and for more than a century they were regarded as mathematical curiosities. The discovery of the Trojan asteroids at the Sun–Jupiter L4 and L5 turned the Lagrange triangle into a real object of celestial mechanics, and Szebehely's 1967 monograph consolidated the restricted problem into the standard reference frame every modern libration-point mission still uses. For the Earth–Moon system the triangular points are especially tempting stations: linearly stable for μ < μ_Routh ≈ 0.03852, they ask only for a stationkeeping technique that removes the offsets their neutral stability lets persist forever.

The physics of the required actuator is surprisingly old. Lebedev (1901) measured the pressure of light on solids, and Nichols and Hull (1903) confirmed it independently; the idea of propelling a vehicle by photons was put on a quantitative footing by Marx (1966), who computed the parameters of an interstellar vehicle pushed by a terrestrial laser beam, and by Redding (1967), who analysed staged photon rockets. These two Nature papers founded laser propulsion: a beam of power P delivers thrust 2P/(cm) to a mirrored sail — per kilogram of payload, the cheapest reaction mass imaginable, since the propellant is light itself.

Forward (1984) turned the arithmetic into a roundtrip interstellar mission design and fixed the canonical figure of merit — the photon ceiling 2P/(cm) — that every later beamed-energy concept inherited, from kilometer-scale lightsails to laser arrays for sailcraft. Close to home, McInnes (1999) systematized the dynamics of sailing craft in gravity fields, Baoyin and McInnes (2006) computed displaced equilibrium families for sails, and Simo and McInnes (2009) placed solar sails on displaced Earth–Moon Lagrange-point trajectories. The present study keeps the same physical ceiling but replaces the passive sail orientation with an actively steered beam — a laser highway in miniature.

For TRIVORTEX the relevance is structural rather than technological. The L4 point is the celestial twin of the same-sign vortex triangle of Theorem 3.1, the Jacobi integral plays the role of the Chaplygin integral C_Ch, and the beam-steering law is the analog of circulation control: an actuator applied to a special solution of the same central-configuration family. The laser block of the program now closes symmetrically — TRX-01 points the laser at the primaries and dresses gravity, TRX-12 points it at the spacecraft and dresses the equations of motion with a bounded thrust term; together they demonstrate that the invariant structuring the phase space is also the quantity an actuator can move.

## 2. Physical formulation

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

## 3. Mathematical model

In the rotating frame the primaries are fixed at (−μ, 0) and (1 − μ, 0), and the sail obeys (E1): Newtonian attraction, centrifugal and Coriolis terms, plus the laser acceleration a_L. The Coriolis force does no work, so for any thrust history the Jacobi identity (E4) holds pointwise: Ċ_J = −2a_L·v. With the thrust off, C_J is the single integral of the planar restricted problem and its level sets bound the accessible region; with the thrust on, its rate of change is a pure control quantity — the laser can only remove C_J when pushing along the velocity, never add it.

The actuator model (E2)–(E3) is deliberately honest. Photon momentum flux P/c doubled by a mirrored sail gives the ceiling a_max = 2P/(cm); for P = 1 MW and m = 10 kg this is 6.67·10⁻⁴ m/s² in SI, or a_max = 0.2443 in canonical units after multiplying by TU²/LU. The PD law u = −K_p(r − r_L4) − K_d·v with K_p = K_d = 4 points the thrust vector; whenever the demanded vector exceeds the ceiling it is rescaled to the ceiling and the saturation counter increments — the control authority is bounded by physics, not by the controller's optimism. With μ = 0.0121505856 well inside the Routh limit μ_Routh ≈ 0.03852, the uncontrolled equilibrium at L4 is an elliptic center: offsets neither grow nor decay, which is exactly why stationkeeping is meaningful and exactly why free drift never converges.

The orbit-raising operation follows from the same identity. Thrust locked along the velocity, a_L = a_max·v/|v|, turns Ċ_J = −2a_L·v into a strictly negative quantity of size 2a_max|v|: the sail climbs the invariant-manifold ladder of the restricted problem, lowering C_J until the zero-velocity topology opens a new corridor between the primaries. For slow, long burns the SI mapping (E5) closes the model: a desired Δv delivered over T_burn needs a = Δv/T_burn and beam power P = m·a·c/2 — the table quoted in the results (100 kg, 30 days) spans 57.8 kW … 2.89 MW for Δv ∈ {10, 50, 100, 500} m/s.

**Notation**

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

**(E1)** CR3BP equations of motion in the rotating frame with laser thrust appended.

$$\ddot{x} - 2\dot{y} = \frac{\partial\Omega}{\partial x} + a_{Lx}, \qquad \ddot{y} + 2\dot{x} = \frac{\partial\Omega}{\partial y} + a_{Ly}, \qquad \Omega = \tfrac{1}{2}(x^2+y^2) + \frac{1-\mu}{r_1} + \frac{\mu}{r_2}$$

**(E2)** Photon thrust along the beam direction û (P = 1 MW, m = 10 kg).

$$a_L = \frac{2P}{c\,m}\,\hat{u}$$

**(E3)** PD beam-steering law bounded by the photon ceiling (K_p = K_d = 4).

$$\mathbf{u} = -K_p\,(\mathbf{r} - \mathbf{r}_{L4}) - K_d\,\mathbf{v}, \qquad |\mathbf{a}_L| \le a_{\max} = \frac{2P}{cm} = 0.2443$$

**(E4)** Jacobi constant; monotone pumping under along-velocity thrust.

$$C_J = 2\Omega - (\dot{x}^2 + \dot{y}^2), \qquad \dot{C}_J = -2\,\mathbf{a}_L\cdot\mathbf{v} \le 0$$

**(E5)** SI power table (100 kg sail, 30 days, Δv ∈ {10, 50, 100, 500} m/s).

$$P = \frac{m\,a\,c}{2}, \qquad a = \frac{\Delta v}{T_{burn}}$$

## 4. Connection to the TRIVORTEX framework

The mapping is one-to-one at the structural level. The libration point L4 is the celestial realization of the Lagrange triangle vertex — the same central configuration that underlies the same-sign vortex triangle of Theorem 3.1; the Jacobi constant plays the role of the Chaplygin integral C_Ch as the invariant that pins the orbit to a reduced phase space; and the PD beam-steering law acts on the libration solution exactly as circulation control acts on a vortex configuration — an actuator applied to a special solution of the same equations. The photon ceiling a_max = 2P/(cm) is the celestial twin of the finite-force regularization used in the vortex model: both keep the actuator honest, capping how fast the invariant can be moved. The laser highway thus closes the TRIVORTEX loop — the quantity that structures the phase space (C_J ↔ C_Ch) is precisely the quantity the actuator moves.

| Quantity in this study | TRIVORTEX analog | Comment |
|---|---|---|
| L4 libration point | Lagrange triangle vertex (Theorem 3.1) | the same central configuration |
| Jacobi constant C_J | Chaplygin integral C_Ch | the invariant the laser moves |
| PD beam-steering law u | circulation control in the vortex model | actuating a special solution |
| Photon ceiling 2P/(cm) | finite-force regularization | honest actuator limits |

## 5. Numerical method

All trajectories are integrated in the rotating frame with an explicit Dormand–Prince 8(5,3) scheme (scipy solve_ivp, DOP853) at rtol = atol = 1e-11 with dense output; the stationkeeping runs use T = 100 with max_step = 0.1 and 800 recorded samples, the pumping run T = 30 with max_step = 0.02 and 800 samples. The control law is evaluated inside the right-hand side: u = −K_p(r − r_L4) − K_d·v with K_p = K_d = 4, rescaled to the ceiling a_max = 0.2443 whenever its norm exceeds it, and the fraction of saturated control evaluations is accumulated as the run proceeds.

The contrast run repeats the integration from the identical initial state L4 + (1e-3, 5e-4), v = (2e-4, −1e-4) with the control switched off, so the only difference between the two trajectories is the laser. Acceptance checks are computed on strict windows — max |r − L4| for t > T/4 (controlled) and min |r − L4| for t > T/2 (free) — so that neither the transient nor the start point can flatter the result. A PD gain-plane sweep repeats the controlled run for a 17 × 17 grid of gains (K_p from 0.5 to 512, K_d from 0.5 to 32, logarithmic, the operating point (4, 4) pinned to both grids) over T = 60 per cell, recording the late-time bound and the saturation fraction of every cell.

The open-loop pumping run starts on an eccentric orbit about the Earth primary (r₀ = 0.10, speed 1.05× the local circular value) with the full ceiling thrust locked along the velocity; C_J is sampled at 800 points over T = 30 and the largest single-step increase is checked against zero. The SI power table (E5) is recomputed analytically for Δv ∈ {10, 50, 100, 500} m/s delivered over 30 days by a 100 kg sail, and its internal consistency (P = m·a·c/2) is itself a check in the protocol.

## 6. Results and analysis

### fig01 landscape

![Landscape of the Earth–Moon laser highway, μ = 0.0121505856: (a) rotating-frame potential with the lunar orbit, the equilateral points L4/L5 and the photon beam cone from Earth toward L4; (b) zoom at L4 over T = 100 — the free sail wanders on a tadpole of extent 0.026 while the controlled sail converges (inset: the controlled spiral).](../figures/fig01_landscape.png)

*Landscape of the Earth–Moon laser highway, μ = 0.0121505856: (a) rotating-frame potential with the lunar orbit, the equilateral points L4/L5 and the photon beam cone from Earth toward L4; (b) zoom at L4 over T = 100 — the free sail wanders on a tadpole of extent 0.026 while the controlled sail converges (inset: the controlled spiral).*
Panel (a) shows the 2Ω topography with Earth (gold), the Moon (navy) and the dashed lunar orbit, with the beam corridor drawn from Earth to L4; panel (b) contrasts the free tadpole (extent up to 0.026 from L4) with the controlled spiral collapsing onto the nominal point, the inset window spanning 2.5·10⁻³.

### fig02 stationkeep

![Headline result — laser stationkeeping versus free drift: (a) distance to L4 on a logarithmic scale over T = 100 (≈ 434 days); the controlled sail settles at 7.5e-07 while the free sail never comes closer than 0.0041 after T/2 — a contrast of ≈ 5500×; (b) the stationkeeping budget: controlled bound, acceptance tolerance 2e-4, initial offset 1.1·10⁻³ and the free-drift floor.](../figures/fig02_stationkeep.png)

*Headline result — laser stationkeeping versus free drift: (a) distance to L4 on a logarithmic scale over T = 100 (≈ 434 days); the controlled sail settles at 7.5e-07 while the free sail never comes closer than 0.0041 after T/2 — a contrast of ≈ 5500×; (b) the stationkeeping budget: controlled bound, acceptance tolerance 2e-4, initial offset 1.1·10⁻³ and the free-drift floor.*
The gold curve drops by more than three decades during the transient and then hugs the 7.5e-07 level, far below the dashed acceptance bound 2e-4; the bar panel lines up the four budget distances on a logarithmic axis from the controlled bound to the free-drift floor 0.0041.

### fig03 control map

![PD gain-plane control map on the same integrator (T = 60 per cell, 17 × 17 gains, K_p from 0.5 to 512 and K_d from 0.5 to 32): (a) logarithm of the late-time stationkeeping error with the acceptance contour 2e-4 and the operating point (4, 4) marked — the map spans 0 (tightest cells) to 123.3 (weak gains lose the station); (b) saturation fraction of the photon-thrust ceiling, near zero across the working region.](../figures/fig03_control_map.png)

*PD gain-plane control map on the same integrator (T = 60 per cell, 17 × 17 gains, K_p from 0.5 to 512 and K_d from 0.5 to 32): (a) logarithm of the late-time stationkeeping error with the acceptance contour 2e-4 and the operating point (4, 4) marked — the map spans 0 (tightest cells) to 123.3 (weak gains lose the station); (b) saturation fraction of the photon-thrust ceiling, near zero across the working region.*
The gold star marks the operating point (4, 4), whose late bound is 1.75·10⁻⁵ with zero saturation; the darkest corners of panel (b) show where aggressive gains press against the photon ceiling (up to 0.87 of steps saturated), 77 of the 289 cells exceeding the 5% level.

### fig04 dynamics

![Dynamics of the two laser operations: (a) open-loop Jacobi pumping — C_J decreases monotonically under along-velocity thrust, net ΔC_J = 1063.51 over T = 30 (largest single-step increase −0.06); (b) control effort of the stationkeeping run — peak demand 0.0051 (= 1.4·10⁻⁵ m/s², equivalent to 20.7 kW on 10 kg) against the photon ceiling 0.2443, headroom 48×.](../figures/fig04_dynamics.png)

*Dynamics of the two laser operations: (a) open-loop Jacobi pumping — C_J decreases monotonically under along-velocity thrust, net ΔC_J = 1063.51 over T = 30 (largest single-step increase −0.06); (b) control effort of the stationkeeping run — peak demand 0.0051 (= 1.4·10⁻⁵ m/s², equivalent to 20.7 kW on 10 kg) against the photon ceiling 0.2443, headroom 48×.*
Panel (a) records the invariant sliding from −7.66 down to −1068 with strictly negative increments; panel (b) shows the demand |a_L| peaking at the transient start (the initial state alone demands ≈ 5.1·10⁻³) and collapsing toward the plot floor 1e-7, never approaching the dashed ceiling 0.2443.

**Stationkeeping.** From the initial offset 1.118·10⁻³ the controlled sail collapses onto L4 during the transient and then stays bounded by 7.5e-07 for all t > T/4 — a final error ≈ 270× tighter than the 2e-4 acceptance tolerance. The uncontrolled twin never comes closer than 0.0041 over its second half and wanders on a tadpole of extent up to 0.026: the contrast factor between the free floor and the controlled bound is ≈ 5500×. This is the entire mission case for a laser highway in one number.

**Actuator budget.** The peak control demand is 0.0051 (the initial state alone demands ≈ 5.1·10⁻³ of ceiling), or 1.4·10⁻⁵ m/s² in SI — equivalent to 20.7 kW of beam power on the 10 kg sail — against the ceiling 0.2443: a headroom of 48×. The saturation fraction of the headline run is exactly 0.0: the photon ceiling is never touched. The 17 × 17 gain sweep brackets the operating point from both sides — the late-time bound spans 0 (tightest cells) to 123.3 (weak gains lose the station), while the operating point (4, 4) holds 1.75·10⁻⁵ with zero saturation; aggressive high-gain corners do press against the ceiling (up to 0.87 of steps saturated), and 77 of the 289 cells exceed the 5% saturation level.

**Jacobi pumping.** With the full ceiling thrust locked along the velocity, C_J slides monotonically from −7.66 down to −1068 over T = 30: net ΔC_J = 1063.51, and the largest single-step increase across the whole record is −0.0604 — every increment strictly negative, exactly as Ċ_J = −2a_L·v ≤ 0 demands. The laser demonstrably moves the invariant that structures the restricted problem's phase space.

**Engineering closure.** The SI table prices the operations: delivering Δv ∈ {10, 50, 100, 500} m/s to a 100 kg sail over 30 days costs 57.8 kW, 289 kW, 578 kW and 2.89 MW of beam power respectively — while the stationkeeping task itself runs at a peak equivalent of 20.7 kW on 10 kg. A 1 MW transmitter therefore holds a station with a 48× margin and simultaneously has photon budget for meaningful orbit raising: the laser highway is a single power plant serving both operations.

### Verification summary

| Check | Recorded value | Target | Tolerance | Pass |
|---|---|---|---|---|
| `controlled_l4_bound` | 7.47949e-07 | 0 | 0.0002 | yes |
| `control_saturation_fraction` | 0 | 0 | 0.05 | yes |
| `free_drift_never_converges` | 1 | 1 | 1e-12 | yes |
| `jacobi_pumped_monotonically` | 1 | 1 | 1e-12 | yes |
| `power_table_consistent` | 1 | 1 | 1e-12 | yes |

*(status: **PASS**, mode: full)*

## 7. Discussion

The model is deliberately minimal: planar motion, circular primary orbits, instantaneous beam pointing and an ideal mirrored sail. Within these assumptions every conclusion is an exact statement about the governing equations rather than a simulation of a specific mission. The natural extensions — eccentric binaries, out-of-plane halo families around the collinear points, beam-transit delay and diffraction losses in the pointing loop, adaptive or frequency-shaped gains — each preserve the verification style established here, and none of them can remove the central fact that a bounded, correctly pointed force turns neutral libration into a controlled equilibrium.

The parameter regime is chosen for honesty rather than spectacle. The photon ceiling 0.2443 follows from SI constants (1 MW, 10 kg, c) and is never assumed away; the gain sweep shows where the controller would need more authority than the beam can deliver (77 of 289 cells above 5% saturation, up to 0.87) and where weak gains simply lose the station (bounds up to 123.3). The operating point (4, 4) sits in a broad low-error, zero-saturation region, which is the practically relevant statement: the laser highway does not live on the edge of its actuator.

Within the program this study is the actuator half of the laser block. TRX-01 dresses the primaries with radiation and maps how the libration landscape deforms; TRX-12 dresses the spacecraft itself and holds it at the undressed landscape's best address. TRX-10 supplies the secular transport machinery (Kozai–Lidov cycles) that a laser highway would exploit for large, naturally slow rearrangements between manifolds, and TRX-11 covers the extreme-mass regime of the same three-body stage. Together they bound the same message from both sides: invariants structure the phase space, and actuators — massless but bounded — move those invariants.

## 8. Conclusions

1. PD-controlled laser stationkeeping holds |r − L4| ≤ 7.5e-07 for all t > T/4 from an initial offset of 1.1·10⁻³ — the 2e-4 acceptance tolerance is beaten by ≈ 270×.
2. Free drift never converges: the identical initial state keeps a floor of 0.0041 and a tadpole extent up to 0.026 — a contrast of ≈ 5500× with the controlled bound.
3. The photon ceiling is never touched: control saturation fraction 0.0; peak demand 0.0051 (= 1.4·10⁻⁵ m/s², 20.7 kW equivalent) is 48× below the ceiling 0.2443 set by 1 MW on 10 kg.
4. The PD gain plane (17 × 17, K_p 0.5–512, K_d 0.5–32) brackets the operating point (4, 4): late bounds span 0 to 123.3, and the operating point holds 1.75·10⁻⁵ with zero saturation.
5. Jacobi pumping is strictly monotone: net ΔC_J = 1063.51 over T = 30 with the largest single-step increase −0.0604 — the laser demonstrably moves the invariant C_J = 2Ω − v².
6. The SI power table prices the highway: Δv ∈ {10, 50, 100, 500} m/s over 30 days on 100 kg costs 57.8 kW … 2.89 MW of beam power — one 1 MW transmitter covers stationkeeping with headroom for orbit raising.

## 9. References

1. Marx, G. (1966). *Interstellar vehicle propelled by terrestrial laser beam.* Nature 211, 22–23.
2. Redding, J. L. (1967). *Interstellar travel via multi-stage photon rockets.* Nature 213, 588–590.
3. Forward, R. L. (1984). *Roundtrip interstellar travel using laser-pushed lightsails.* Journal of Spacecraft and Rockets 21, 187–195.
4. Simmons, J. F. L., McDonald, A. J. C., Ward, J. C. (1985). *The restricted three-body problem with radiation pressure.* Celestial Mechanics 35, 145–187.
5. McInnes, C. R. (1999). *Solar Sailing: Technology, Dynamics and Mission Applications.* Springer-Praxis, Chichester.
6. Vulpetti, G., Johnson, L., Matloff, G. L. (2008). *Solar Sails: A Novel Approach to Interplanetary Flight.* Springer, New York.
7. Baoyin, H., McInnes, C. R. (2006). *Solar sail halo orbits at the Sun–Earth artificial L1 point.* Celestial Mechanics and Dynamical Astronomy 94, 301–316.
8. Simo, J., McInnes, C. R. (2009). *Solar sail trajectories at the Earth-Moon Lagrange points.* 59th International Astronautical Congress, IAC-09.C1.6.13.
9. Szebehely, V. (1967). *Theory of Orbits: The Restricted Problem of Three Bodies.* Academic Press, New York.

### BibTeX

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

## Appendix A. Parameter table

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

## Appendix B. Reproduction

```bash
python3 research/TRX-12-laser-light-sail/code/trx12_laser_light_sail.py --smoke     # < 20 s
python3 research/TRX-12-laser-light-sail/code/trx12_laser_light_sail.py              # full, 41.4 s
python3 research/TRX-12-laser-light-sail/code/trx12_laser_light_sail.py --figures   # + 300-DPI figures
```

Full runtime on the reference machine: 41.4 s; smoke mode completes in under 20 seconds and is exercised by the repository CI.

## Appendix C. Environment

Python ≥ 3.11, numpy ≥ 2.0, scipy ≥ 1.14, matplotlib ≥ 3.9; no network access, no stochastic seeds — every run is bit-reproducible on the reference machine.
