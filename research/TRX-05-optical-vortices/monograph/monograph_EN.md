# Optical Vortices of Laser Beams and the Point-Vortex Analogy

*TRIVORTEX Research Program · v1.0.0 · Monograph Edition*

|  |  |
|---|---|
| Study | TRX-05 |
| Program | TRIVORTEX — The Three-Body Problem in the Vortex Model |
| Author | Isaev Iskhak Khamzatovich (ORCID 0009-0003-7299-0701) |
| DOI | 10.5281/zenodo.21825394 |
| Date | 2026-10-06 |
| Code | `code/trx05_optical_vortices.py` |
| Data | `results/trx05_results.json` |

## Abstract

This monograph treats phase singularities — optical vortices — of a paraxial laser field and makes the classical analogy with Kirchhoff point vortices quantitative in both directions. Three same-sign singularities of the field ψ(z) = exp(−r²/w²)·Π(z − z_k) are placed on an equilateral triangle of side a = 1 and integrated over three rotations (T = 39.4784) with a DOP853 scheme at rtol = atol = 1e-13. The measured rotation rate 0.477464829 reproduces the analytic Lagrange-type law ω = 3Γ/(2πa²) within the 1e-8 acceptance tolerance (agreement at the 1e-16 level). The angular impulse I = ΣΓ|r|² — the many-vortex prototype of the Chaplygin integral — stays pinned at a² = 1 with drift 1.8e-15, and the Kirchhoff Hamiltonian drifts by 4.6e-16, both far inside the 1e-12 tolerance. The rendered complex field (grid spacing 0.018) shows three dark cores tracking the vortex positions within 0.0118 against the 0.036 acceptance, and the winding number of arg ψ on r = 1.55 equals 3 exactly — the optical analogue of orbital angular momentum 3ℏ per photon. Singular optics and the classical point-vortex problem are thus numerically the same system.

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

Optical vortices — the phase singularities of light — entered physics as curiosities of wave interference and grew into a discipline of their own. Berry and Dennis (2000) gave the canonical statistical description of singularities in random waves, showing that zeros of a complex scalar field are points where phase is undefined and around which the phase winds by an integer multiple of 2π. Soskin, Gorshkov and Vasnetsov (1997) had already established that laser beams carrying such screw dislocations possess a well-defined topological charge and that this charge is the optical counterpart of orbital angular momentum — each photon of a charge-q beam carries qℏ of OAM in addition to its spin.

The classical side of the analogy is older by more than a century. Kirchhoff (1876) wrote down the equations of point vortices that still carry his name: each vortex is advected by the velocity field induced by all the others, a 1/r induction law that makes the mathematics identical to the phase gradient of an optical zero. Aref (1979) revisited the three-vortex problem and clarified its integrability and collapse structure, Newton (2001) consolidated the N-vortex problem into a standard reference, and Aref et al. (2003) surveyed vortex crystals — relative equilibria of point vortices — of which the equilateral triangle of equal circulations is the simplest and most celebrated example.

The bridge between the two disciplines is a product structure. Near a zero the field factorizes, ψ ≈ (z − z_k)·(smooth part), and the phase gradient of the factor (z − z_k) is exactly the velocity field of a point vortex; zeros of equal sign therefore move under the Kirchhoff equations to leading order. A laser beam with a designed product ψ(z) = exp(−r²/w²)·Π_k (z − z_k) thus realizes the point-vortex dynamics literally in light: the dark cores are the “bodies”, their topological charges are the circulations, and the beam's far-field winding is the total charge. The analogy is not metaphorical — it is the same system of ODEs at leading order.

For TRIVORTEX the relevance is structural. The angular impulse I = ΣΓ|r|² of the vortex system is the many-vortex prototype of the Chaplygin integral C_Ch that pins the vortex-model orbits; the rigidly rotating equilateral triangle is the optical twin of the Theorem 3.1 choreography; and the winding number of the field is the optical reading of the total vortex charge. This study therefore anchors the optics block of the program: it shows that the framework's mathematical skeleton survives verbatim when the vortices are made of light (TRX-04 provides the field-maxima counterpart, TRX-09 the classical fluid anchor).

## 2. Physical formulation

(A) Kirchhoff dynamics. Three point vortices of equal circulation Γ = 1 are placed on an equilateral triangle of side a = 1 (circumscribed radius r_c = a/√3 ≈ 0.57735) and integrated with an explicit Dormand–Prince 8(5,3) scheme over three full rotations, T = 39.4784. For equal same-sign circulations the equilateral configuration is an exact relative equilibrium: every vortex traces a circle of radius r_c about the common centroid at the analytic rate ω = 3Γ/(2πa²).

(B) Field rendering. The paraxial scalar field ψ(z) = exp(−r²/w²)·Π_k (z − z_k(t)) with a Gaussian envelope w = 3 is evaluated on a grid of 0.018 spacing over [−1.7, 1.7]² at t = 0 and t = T/4. Its intensity zeros coincide with the vortex positions, the phase winds by 2π around each core, and the winding of arg ψ on a large circle counts the total topological charge N = 3 — the optical analogue of orbital angular momentum 3ℏ per photon.

| Parameter | Value | Meaning |
|---|---|---|
| Γ | 1 | circulation of each optical vortex (= topological charge +1) |
| a | 1 | side of the equilateral vortex triangle, r_c = a/√3 ≈ 0.57735 |
| ψ(z) | exp(−r²/w²)·Π_k (z − z_k) | rendered paraxial field, Gaussian envelope w = 3 |
| grid | 0.018 over [−1.7, 1.7]² | intensity/phase rendering and zero tracking |
| integrator | DOP853, rtol = atol = 1e-13 | three rotations, T = 39.4784 |
| winding circle | r = 1.55 | topological-charge evaluation (any r > r_c) |

## 3. Mathematical model

The Kirchhoff equations (E1) follow from the induction structure of ideal flow: a point vortex of circulation Γ_j at position (x_j, y_j) induces at (x_k, y_k) the velocity Γ_j/(2π r_jk) perpendicular to the separation vector, with r_jk the distance between the two points. Summing the contributions of all other vortices gives the right-hand sides of (E1); the equations are first-order and Hamiltonian with the pair Hamiltonian (E3) in the logarithmic potential. For Γ = 1 the system is fully dimensionless once lengths are measured in units of a.

Two invariants structure the dynamics. The angular impulse (E2), I = ΣΓ_k|r_k|², is conserved by rotational symmetry — it is the exact many-vortex analogue of the Chaplygin integral of the TRIVORTEX vortex model — and for an equilateral triangle of side a it evaluates to a² identically, since every vertex sits at distance a/√3 from the centroid: I = 3·(a²/3) = a². The Kirchhoff Hamiltonian (E3) fixes the pair distances; both together lock the triangle into a relative equilibrium whose rotation rate follows from balancing the induced velocity with the orbital motion, giving the Lagrange-type law (E4), ω = 3Γ/(2πa²). For a = 1 the Hamiltonian vanishes identically (ln 1 = 0), a useful sanity marker of the preset.

The optical rendering (E5) is a product over the vortex positions times a Gaussian envelope. By construction each factor vanishes at z = z_k(t), so the intensity zeros coincide with the Kirchhoff vortices at all times; each factor contributes exactly one unit of phase winding (charge q_k = +1), and the winding number of the total field on any circle enclosing all cores equals the sum of the charges, N = Σq_k = 3. The winding integral in (E5) is the optical reading of the total charge and, through the Soskin et al. correspondence, of the orbital angular momentum 3ℏ per photon carried by the beam.

**Notation**

| Symbol | Meaning |
|---|---|
| z = x + iy | transverse complex coordinate of the beam |
| z_k(t) | trajectory of the k-th vortex / field zero |
| Γ_k | circulation of vortex k (Γ = 1 for all) |
| q_k | topological charge of singularity k (q_k = +1) |
| ψ(z) | paraxial scalar field of the beam |
| w | Gaussian envelope width (w = 3a) |
| a | side of the equilateral vortex triangle |
| r_c | circumscribed radius a/√3 ≈ 0.57735 |
| I | angular impulse I = ΣΓ\|r\|² = a² |
| H | Kirchhoff Hamiltonian (H = 0 at a = 1) |
| ω | rotation rate of the triangle, 3Γ/(2πa²) |
| T | integration span, three rotations (39.4784) |

**(E1)** Kirchhoff point-vortex equations (velocity of vortex k induced by all others).

$$u_k = -\frac{1}{2\pi}\sum_{j\neq k}\Gamma_j\,\frac{y_k - y_j}{r_{kj}^2}, \qquad v_k = +\frac{1}{2\pi}\sum_{j\neq k}\Gamma_j\,\frac{x_k - x_j}{r_{kj}^2}$$

**(E2)** Angular impulse of the vortex system — the many-vortex prototype of the Chaplygin integral; for the equilateral triangle it is pinned at a².

$$I = \sum_k \Gamma_k\,|\mathbf{r}_k|^2 = a^2$$

**(E3)** Kirchhoff Hamiltonian (logarithmic pair interaction; H = 0 identically for a = 1).

$$H = -\frac{\Gamma^2}{2\pi}\sum_{j<k} \ln r_{jk}$$

**(E4)** Analytic rotation rate of the same-sign equilateral triangle (Lagrange-type relative equilibrium).

$$\omega = \frac{3\Gamma}{2\pi a^2}$$

**(E5)** Rendered paraxial field and its winding number (total topological charge).

$$\psi(z) = e^{-r^2/w^2}\prod_k \bigl(z - z_k(t)\bigr), \qquad N = \frac{1}{2\pi}\oint \nabla(\arg\psi)\cdot d\mathbf{l} = \sum_k q_k = 3$$

## 4. Connection to the TRIVORTEX framework

The mapping is one-to-one and works in both directions. The dark cores of the rendered field are literal realizations of the TRIVORTEX vortex-model “bodies”; the topological charge q_k of each singularity plays the role of the circulation Γ_k; the angular impulse I = ΣΓ|r|² is the same invariant structure as the Chaplygin integral, here pinned exactly at a² = 1; and the rigidly rotating equilateral triangle of three same-sign singularities is the optical twin of the Theorem 3.1 choreography, obeying the identical Lagrange-type rate ω = 3Γ/(2πa²). The winding number of the far field closes the dictionary: it is the optical measurement of the total charge ΣΓ = 3, the quantity that in the vortex model fixes the orbital angular momentum of the configuration. No parameter is left unmatched — the study is the optical edition of the TRIVORTEX core.

| Quantity in this study | TRIVORTEX analog | Comment |
|---|---|---|
| Optical vortices (field zeros) | vortex model “bodies” | literal realization of the model |
| Topological charge q_k = +1 | circulation Γ_k | the charge–circulation dictionary |
| I = ΣΓ\|r\|² = a² | Chaplygin integral C_Ch | the same invariant structure |
| Equilateral triangle rotation | Theorem 3.1 choreography | identical relative equilibrium |
| Winding number 3 | total charge ΣΓ = 3 | orbital angular momentum 3ℏ per photon |

## 5. Numerical method

The vortex triangle is integrated with an explicit Dormand–Prince 8(5,3) scheme at rtol = atol = 1e-13 with max_step 0.05 over T = 39.4784 — three full rotations. The rotation rate is extracted from the polar angle of vortex 1 relative to the instantaneous centroid: the angle is unwrapped along 2000 dense samples and fitted by a straight line, whose slope 0.477464829 is the measured ω. The same fit run on the analytic trajectory returns the target value, so the check probes the integrator, not the algebra.

Both invariants are monitored pointwise along the trajectory at the same 2000 samples: the angular impulse I = ΣΓ|r|² drifts by 1.8e-15 from its initial value I = 1.000000000000 = a², and the Kirchhoff Hamiltonian drifts by 4.6e-16 from its identically-zero initial value. Both sit far below the 1e-12 acceptance tolerance — the invariant structure of the point-vortex problem survives the full three-rotation integration at round-off level.

The optical field is evaluated on a uniform grid of 0.018 spacing over [−1.7, 1.7]² at t = 0 and t = T/4. The 60 deepest intensity pixels are matched against the vortex positions: the worst distance from a vortex to its nearest minimum is 0.0118, three times inside the acceptance band of two grid cells (0.036). The winding number is computed by unwrapping arg ψ along the annulus r = 1.55 and counting the total phase turn — it returns 3.0 exactly, with no grid-level ambiguity.

## 6. Results and analysis

### fig01 field landscape

![Field landscape at t = 0: intensity |ψ|² (log scale) with the three dark cores on the triangle vertices, and the phase arg ψ with its 2π windings.](../figures/fig01_field_landscape.png)

*Field landscape at t = 0: intensity |ψ|² (log scale) with the three dark cores on the triangle vertices, and the phase arg ψ with its 2π windings.*
The intensity panel shows the three dark cores sitting exactly at the vertices of the equilateral triangle (side a = 1) inside the Gaussian envelope; the phase panel resolves the 2π winding around each core, and the dashed circle r = 1.55 is the circle on which the winding number is measured — it returns N = 3 exactly.

### fig02 rigid rotation

![Headline result — rigid rotation of the vortex triangle: core worldlines over three rotations and the linear growth of the polar angle.](../figures/fig02_rigid_rotation.png)

*Headline result — rigid rotation of the vortex triangle: core worldlines over three rotations and the linear growth of the polar angle.*
All three cores trace circles of radius r_c = a/√3 ≈ 0.57735 about the common centroid over T = 39.4784 (three rotations, period 13.1595); the measured rotation rate 0.477464829 coincides with the analytic 3Γ/(2πa²) = 0.477464829 — agreement at the 1e-16 level, seven orders inside the 1e-8 acceptance tolerance.

### fig03 parameter sweeps

![Parameter sweeps: rotation rate versus triangle side (analytic law against numeric re-runs) and zero-tracking error versus grid spacing.](../figures/fig03_parameter_sweeps.png)

*Parameter sweeps: rotation rate versus triangle side (analytic law against numeric re-runs) and zero-tracking error versus grid spacing.*
The numeric DOP853 re-runs reproduce ω(a) = 3Γ/(2πa²) to nine recorded decimals across a ∈ {0.6, 0.8, 1.0, 1.2, 1.5, 2.0} (from 1.326291192 down to 0.119366207); the tracking sweep keeps the worst core offset below the 2-cell acceptance line everywhere (0.00668 at spacing 0.012 up to 0.04922 at spacing 0.08, against acceptance 0.024–0.16), and the preset grid gives 0.01178.

### fig04 invariants rigidity

![Dynamics over three rotations: drifts of the angular impulse I and the Kirchhoff Hamiltonian H against the acceptance tolerance, and side-length deviations of the rotating triangle.](../figures/fig04_invariants_rigidity.png)

*Dynamics over three rotations: drifts of the angular impulse I and the Kirchhoff Hamiltonian H against the acceptance tolerance, and side-length deviations of the rotating triangle.*
The angular impulse drifts by 1.8e-15 and the Kirchhoff Hamiltonian by 4.6e-16 over T = 39.4784 — hundreds to thousands of times below the 1e-12 tolerance (H is 0 identically for a = 1, since ln 1 = 0); the three side-length deviations d_jk(t) − a stay at machine level, confirming the triangle rotates as a rigid equilateral configuration.

**Rotation.** The measured rotation rate is 0.477464829 against the analytic 3Γ/(2πa²) = 0.477464829 — the two numbers agree to the last recorded digit, at the 1e-16 level, seven orders of magnitude inside the 1e-8 acceptance tolerance. Over T = 39.4784 (three rotations of period 13.1595) every core traces a circle of radius r_c = 0.57735 about the common centroid, and the triangle returns to a rotated copy of itself with the side a = 1 preserved.

**Invariants.** The angular impulse stays pinned at I = 1.000000000000 = a² with maximum drift 1.8e-15, and the Kirchhoff Hamiltonian drifts by 4.6e-16 from its identically-zero initial value — roughly 560 and 2200 times below the 1e-12 tolerance respectively. Because I and H together fix the shape of a three-vortex configuration, their conservation is the dynamical reason the triangle rotates rigidly instead of deforming.

**Field rendering.** At the preset grid spacing 0.018 the deepest intensity minima track the vortices with a worst offset of 0.0118 at t = 0 and t = T/4 — three times inside the 0.036 acceptance band (two grid cells). The sweep over grid spacings 0.012–0.08 keeps the offset below the 2-cell line everywhere (0.00668 up to 0.04922 against 0.024–0.16), so the tracking of zeros by dark cores is robust, not an artifact of one resolution.

**Topology and sweeps.** The winding number of arg ψ on the evaluation circle r = 1.55 equals 3 exactly — the rendered field carries the total topological charge of the three unit singularities. The side sweep confirms the rotation law beyond the preset: numeric re-runs at a ∈ {0.6, 0.8, 1.0, 1.2, 1.5, 2.0} reproduce ω(a) = 3Γ/(2πa²) to nine recorded decimals, from 1.326291192 at a = 0.6 down to 0.119366207 at a = 2.0. The a⁻² scaling of the Lagrange-type configuration is thus verified end to end.

### Verification summary

| Check | Recorded value | Target | Tolerance | Pass |
|---|---|---|---|---|
| `rotation_rate_vs_analytic` | 0.477465 | 0.477465 | 1e-08 | yes |
| `angular_impulse_I_conserved` | 1.77636e-15 | 0 | 1e-12 | yes |
| `kirchhoff_hamiltonian_conserved` | 4.59413e-16 | 0 | 1e-12 | yes |
| `field_minima_track_vortices` | 0.0117821 | 0 | 0.036 | yes |
| `total_winding_number_is_3` | 3 | 3 | 1e-12 | yes |

*(status: **PASS**, mode: full)*

## 7. Discussion

The model is deliberately minimal: scalar paraxial field, point-like singularities, static Gaussian envelope. Within these assumptions the Kirchhoff side is exact and the optical side is its leading-order realization — real optical vortices have a finite core structure, and non-paraxial, polarization and envelope-deformation corrections enter at higher order. The product field (E5) is the cleanest possible laboratory: it separates the zero dynamics (exact Kirchhoff) from the envelope, which only weighs the intensity but does not move the zeros to leading order.

The parameter regime probes the structural core of the analogy rather than a specific beam design. Same-sign equal circulations are the integrable, relative-equilibrium case; opposite signs (translating pairs), unequal circulations, N > 3 clusters and vortex lattices in saturating media are natural extensions that the same code can host. The grid-spacing sweep shows the zero-tracking check is resolution-robust; the side sweep shows the rotation law is exactly a⁻², so the preset a = 1 is a representative point, not a tuned one.

Within the program this study is the optical edition of the vortex core. TRX-09 verifies the same equations in the pure fluid-dynamical setting with the Aref collapse manifold added; TRX-04 treats the field-maxima (bright-soliton) counterpart, where the bodies are intensity peaks rather than zeros; TRX-06 carries the zeros-of-complex-fields structure into quantum three-body ionization. Together with the classical anchor they demonstrate that the TRIVORTEX framework is a single mathematical object viewed through different physical media.

## 8. Conclusions

1. Three same-sign optical vortices on an equilateral triangle of side a = 1 rotate rigidly at the analytic rate ω = 3Γ/(2πa²) = 0.477464829, measured within the 1e-8 tolerance (agreement at the 1e-16 level).
2. The angular impulse I = ΣΓ|r|² is conserved to 1.8e-15 and stays pinned at a² = 1 — the many-vortex Chaplygin-type integral of the configuration.
3. The Kirchhoff Hamiltonian is conserved to 4.6e-16 over T = 39.4784 (H = 0 identically for a = 1); the triangle rotates as a rigid relative equilibrium.
4. The rendered complex field (grid spacing 0.018) shows three dark cores tracking the vortex positions within 0.0118 — three times inside the 0.036 two-cell acceptance.
5. The winding number of arg ψ on the circle r = 1.55 equals 3 exactly — the optical reading of the total charge and of the orbital angular momentum 3ℏ per photon.
6. The rotation law is verified across a ∈ {0.6, …, 2.0} (numeric rates matching ω(a) to nine recorded decimals), confirming the a⁻² Lagrange-type scaling end to end.

## 9. References

1. Berry, M. V., Dennis, M. R. (2000). *Phase singularities in isotropic random waves.* Proc. R. Soc. A 456, 2059–2079.
2. Soskin, M. S., Gorshkov, V. G., Vasnetsov, M. V. (1997). *Topological charge and angular momentum of light beams carrying optical vortices.* Phys. Rev. A 56, 4064–4075.
3. Kirchhoff, G. (1876). *Vorlesungen über mathematische Physik: Mechanik.* Teubner, Leipzig.
4. Aref, H. (1979). *Motion of three vortices revisited.* Phys. Fluids 22, 393–400.
5. Aref, H., Newton, P. K., Stremler, M. A., Tokieda, T., Vainchtein, D. L. (2003). *Vortex crystals.* Annu. Rev. Fluid Mech. 35, 349–395.
6. Yao, A. M., Padgett, M. J. (2011). *Orbital angular momentum: origins, behavior and applications.* Adv. Opt. Photon. 3, 161–204.
7. Dennis, M. R., O'Holleran, K., Padgett, M. J. (2009). *Singular optics: structuring optical wavefields.* Prog. Opt. 53, 293–363.
8. Newton, P. K. (2001). *The N-Vortex Problem: Analytical Techniques.* Springer, New York.

### BibTeX

```bibtex
@article{berry2000,
  author  = {Berry, M. V. and Dennis, M. R.},
  title   = {Phase singularities in isotropic random waves},
  journal = {Proceedings of the Royal Society A},
  year    = {2000}, volume = {456}, pages = {2059--2079}}

@article{soskin1997,
  author  = {Soskin, M. S. and Gorshkov, V. G. and Vasnetsov, M. V.},
  title   = {Topological charge and angular momentum of light beams carrying optical vortices},
  journal = {Physical Review A},
  year    = {1997}, volume = {56}, pages = {4064--4075}}

@book{kirchhoff1876,
  author    = {Kirchhoff, G.},
  title     = {Vorlesungen \"uber mathematische Physik: Mechanik},
  publisher = {Teubner}, address = {Leipzig}, year = {1876}}

@article{aref1979,
  author  = {Aref, Hassan},
  title   = {Motion of three vortices revisited},
  journal = {Physics of Fluids},
  year    = {1979}, volume = {22}, pages = {393--400}}
```

## Appendix A. Parameter table

| Symbol | Value | Role |
|---|---|---|
| Γ | 1 | circulation of each optical vortex |
| a | 1 | triangle side (length unit) |
| r_c | 0.57735 | core orbit radius a/√3 |
| w | 3 | Gaussian envelope width |
| grid | 0.018 over [−1.7, 1.7]² | field rendering and zero tracking |
| T | 39.4784 | integration span (three rotations, period 13.1595) |
| rtol, atol | 1e-13 | DOP853 tolerances (max_step 0.05) |
| r = 1.55 | winding circle | topological-charge evaluation |
| minima sample | 60 pixels | deepest intensity pixels matched to vortices |

## Appendix B. Reproduction

```bash
python3 research/TRX-05-optical-vortices/code/trx05_optical_vortices.py --smoke     # < 20 s
python3 research/TRX-05-optical-vortices/code/trx05_optical_vortices.py              # full, 4.83 s (4.827 s recorded with --figures)
python3 research/TRX-05-optical-vortices/code/trx05_optical_vortices.py --figures   # + 300-DPI figures
```

Full runtime on the reference machine: 4.83 s (4.827 s recorded with --figures); smoke mode completes in under 20 seconds and is exercised by the repository CI.

## Appendix C. Environment

Python ≥ 3.11, numpy ≥ 2.0, scipy ≥ 1.14, matplotlib ≥ 3.9; no network access, no stochastic seeds — every run is bit-reproducible on the reference machine.
