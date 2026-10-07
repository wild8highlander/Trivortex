# TRIVORTEX — The Three-Body (and N-Body) Problem in the Vortex Model with the Chaplygin Topological Integral

*Core Monograph · English edition · TRIVORTEX Research Program v1.0.0*

|  |  |
|---|---|
| Document | `code/trivortex_core*.py` — the executable core, 22 sections |
| Author | Isaev Iskhak Khamzatovich (ORCID 0009-0003-7299-0701) |
| Program | TRIVORTEX — research-papers repository, version 1.0.0 |
| DOI | 10.5281/zenodo.21825394 (concept DOI 10.5281/zenodo.21825393) |
| Verification | Independent ladder V1–V4 + 27-test pytest guard, run on every push |
| License | LicenseRef-Proprietary-Wild8Highlander-1.0 |

## Abstract

TRIVORTEX is an executable research document that studies the three-body (and N-body) problem through a vortex formulation with a Chaplygin topological integral. The document is not a paper *about* the vortex model — it *is* the model: an interactive Python volume of about 2,400 lines in three language mirrors, whose every chapter is a section of working code, from the Hofstadter-type Hamiltonian with embedded vortices through the closed-form rotating solution (Theorem 3.1) to spectral statistics, quantum-topological observables, an interactive 15-mode menu and a seven-format report engine. An independent verification ladder — code that shares nothing with the document — re-derives the central claims from scratch on every push and certifies them to residuals of order 1e-14. This monograph is the reader's companion to the executable core: it states the model, the theorem, the certified boundaries and the reproduction protocol in words, so the volume can be read like a book and executed like a program.

## 1. The problem and the vortex reformulation

Ask three masses to move under their mutual Newtonian attraction and you have posed the problem that shaped three centuries of mathematics. Newton solved the two-body problem completely; the three-body problem resisted. Euler and Lagrange found exact special solutions — the collinear and equilateral central configurations rotating rigidly like a spun coin — and Poincaré, attacking the restricted problem, discovered that no general closed-form solution exists, inventing chaos in the wreckage of the prize memoir. The modern era replaced the impossible *general* solution with an atlas of remarkable *particular* ones: Lagrange's triangle, Euler's line, the figure-eight choreography of Chenciner–Montgomery, and a growing zoo of choreographic solutions. The field lives because special exact solutions are both rare and verifiable: either the equations hold them to machine precision, or they do not.

TRIVORTEX leans on exactly that verifiability. The vortex formulation trades Newtonian masses for point vortices with circulations — a Hamiltonian, first-order system whose special solutions are algebraically sharp. The three "bodies" are vortices with topological charges $q_k = (1, -1, 1)$; their Kirchhoff dynamics conserve algebraic invariants; and each vortex carries an effective Aharonov–Bohm flux, so that the angular momentum binds to the gauge field in a combination the document attributes to Chaplygin.

## 2. The Chaplygin topological integral

The model's signature quantity is the topological integral

$$C_{Ch} = r^2\,(\dot{\theta} - q\,A_\theta), \qquad A_\theta = \frac{1}{r},$$

which pins the gauge flux to the rotation and acts as the control knob of the closed-form solution: given $C_{Ch}$ and the period $T$, the rotation frequency and the radial modulation amplitude are both fixed. The document is deliberately honest about the status of this combination: along the closed form the gauge-dependent $C_{Ch}(t)$ oscillates together with the radial modulation — by construction of the model — and its endpoint drift over a finite window is recorded as a *diagnostic*, not a conservation law. The window-independent conserved quantities of the dynamics are the classical vortex integrals $H$, $P$, $Q$, $I$, and those are what the numerical ladder certifies in checks V3–V4.

> **Honesty note.** The certified layer (choreography, periodicity, rigid rotation, integral conservation) is separated from the recorded layer (window-dependent Chaplygin drift) everywhere in the repository — in the ladder output, in the pytest guard, on the documentation site and in this monograph.

## 3. Theorem 3.1 — the closed form

The central result is a Lagrange-type relative equilibrium with radial modulation: three vortices that keep an exact equilateral triangle while rotating with a frequency fixed by the Chaplygin constant,

$$r_k(t) = \sqrt{C_{Ch}}\,\bigl(1 + \varepsilon\cos(\omega t + 2\pi k/3)\bigr), \qquad \theta_k(t) = \omega t + 2\pi k/3,$$

$$\omega = \frac{2\pi}{T}\,e^{C_{Ch}/\pi}, \qquad \varepsilon = \frac{1}{e^{C_{Ch}/\pi} - 1}.$$

Two structural properties follow from the form itself and are what the ladder certifies: the **equilateral choreography** (angular positions differ by exactly $2\pi/3$ at every instant — the vortex twin of the classical Lagrange triangle) and the **periodicity** of the radial modulation with period $T_r = 2\pi/\omega$. Reference values for the canonical configuration $C_{Ch} = 1$, $T = 2\pi$:

| Quantity | Value (float64) | Verified by |
|---|---|---|
| frequency $\omega = (2\pi/T)\,e^{1/\pi}$ | `1.3748022274393588` | pytest pin, exact to float64 |
| amplitude $\varepsilon = 1/(e^{1/\pi}-1)$ | `0.7276379117656014` | pytest pin, exact to float64 |
| angular separation (all probed times) | $2\pi/3 \pm 6.9\times10^{-14}$ | ladder V1 |
| periodicity residual over $100\,T$ | $\le 9.4\times10^{-14}$ | ladder V1 |

The theorem also has a numerical twin that needs no closed form: three *equal* point vortices released on an equilateral triangle integrate forward (Kirchhoff equations, RK4) rotating rigidly at the classical angular velocity $\omega_L = 3\Gamma/(2\pi a^2)$ — ladder check V2 — while the four classical integrals $H, P, Q, I$ are conserved along the trajectory (V3), with or without the symmetric initial condition (V4).

## 4. The independent verification ladder

`verification/trivortex/python/verify.py` re-implements — independently, from scratch, numpy-only — everything it checks: the closed form, the Chaplygin combination, the Kirchhoff right-hand side, its own RK4 stepper. It shares **no code** with the document, runs in three presets (`quick` ≈ 0.5 s, `default` ≈ 2 s, `full` ≈ 35 s) and writes a JSON protocol with a full parameter snapshot per run. Registered criteria and reference results:

| Check | Statement | Registered criterion | Result |
|---|---|---|---|
| **V1** | Theorem 3.1 closed form: $2\pi/3$ choreography + periodicity | separation ≤ 1e-12; periodicity ≤ 1e-12 | 6.9e-14 / 9.4e-14 |
| **V2** | Lagrange triangle rotates rigidly at $\omega = 3\Gamma/(2\pi a^2)$ | shape ≤ 1e-10; ω rel. err ≤ 1e-6 | 1.6e-14 / 2.9e-12 |
| **V3** | Vortex integrals $H, P, Q, I$ conserved (equal Γ) | worst rel. drift ≤ 1e-10 | 2.9e-14 |
| **V4** | Integrals conserved for $\Gamma = (1, 2, 3)$, generic triangle | worst rel. drift ≤ 1e-10 | 2.9e-14 |

A 27-test pytest guard pins the analytic layer to hard reference values and wraps the ladder in CI-friendly form; the CI workflow runs both on every push and uploads the JSON protocol as an artifact. Numbers printed by the code that defines them are repetition; this repository insists on verification.

## 5. Inside the executable document

One physics kernel, three language mirrors (`trivortex_core.py` — default English console; `_ru.py` — Russian; `_en.py` — English), each with the identical 22-section structure:

| № | Section | № | Section |
|---|---|---|---|
| 1 | Imports and dependencies | 12 | Report engine — TXT/MD/HTML/CSV/JSON/DOCX/PDF |
| 2 | Constants and global configuration | 13 | Comprehensive test functions |
| 3 | Data structures (result containers) | 14 | Interactive menu (15 modes) |
| 4 | Hamiltonian construction (Hofstadter + N vortices) | 15 | Main entry point |
| 5 | **Analytical solution (Theorem 3.1)** | 16 | Berry phase calculation |
| 6 | Chaplygin conservation verification | 17 | Chern numbers (Fukui–Hatsugai–Suzuki) |
| 7 | Spectral statistics (GUE/GOE/Poisson) | 18 | TKNN Hall conductance |
| 8 | Zeta zeros and Montgomery test | 19 | Dirac cone analysis |
| 9 | Quantum version with topological qubits | 20 | Spectral form factor |
| 10 | Real system presets | 21 | Number variance and IPR |
| 11 | High-resolution plot generation | 22 | Lyapunov exponent + permutation test |

Around the analytic core the document builds four observables layers: a **spectral layer** (unfolding, the ⟨r⟩ statistic against GUE/GOE/Poisson references, KS tests, number variance, spectral form factor), a **quantum-topological layer** (Berry phase, Chern numbers by the Fukui–Hatsugai–Suzuki method, TKNN conductance, Dirac cones), a **chaos layer** (Lyapunov exponents, permutation tests, KAM statistics) and a **report engine** that emits every result as TXT, MD, HTML, CSV, JSON, DOCX and PDF with plots at 300 dpi.

## 6. Real astronomical presets

Section 10 wires three real triples into the model as `RealSystem` records — masses, characteristic distances, characteristic periods — used as parameter scales and reality anchors (not as ephemeris simulations):

| System | Bodies | Scale span |
|---|---|---|
| Sun–Earth–Moon | Sun · Earth · Moon | 1 AU hierarchy, the canonical triple |
| α Centauri | α Cen A · α Cen B · Proxima | the nearest real three-star system |
| Pluto–Charon–Nix | Pluto · Charon · Nix | a dynamically rich small triple |

The verification ladder deliberately does **not** use them: V1–V4 operate on exact model objects, keeping the certified core clean of astronomical parameter noise.

## 7. Reproduction

```bash
git clone https://github.com/wild8highlander/research-papers.git
cd research-papers
python -m pip install numpy scipy matplotlib mpmath

# the interactive document (menu: 15 modes, RU/EN mirrors available)
python3 code/trivortex_core_en.py

# the independent verification ladder
python3 verification/trivortex/python/verify.py --preset quick   # ~0.5 s (CI)
python3 verification/trivortex/python/verify.py --preset default # ~2 s
python3 verification/trivortex/python/verify.py --preset full    # ~35 s

# the pytest guard (27 tests)
python -m pytest verification/tests/ -v
```

Every ladder run writes a JSON protocol with a full parameter snapshot — attach it to any issue that reports a failing check and the failure is reproducible without a single follow-up question.

## 8. Provenance and citation

Author: Isaev Iskhak Khamzatovich ([ORCID 0009-0003-7299-0701](https://orcid.org/0009-0003-7299-0701)), independent researcher. Version 1.0.0 is the first public release of the TRIVORTEX research program. Cite via [`CITATION.cff`](https://github.com/wild8highlander/research-papers/blob/main/CITATION.cff):

```bibtex
@misc{trivortex2026isaev,
  author       = {Isaev, Iskhak Khamzatovich},
  title        = {TRIVORTEX: The Three-Body (and N-Body) Problem in the
                  Vortex Model with the Chaplygin Topological Integral},
  year         = {2026},
  howpublished = {Zenodo},
  doi          = {10.5281/zenodo.21825394},
  url          = {https://github.com/wild8highlander/research-papers}
}
```

License: `LicenseRef-Proprietary-Wild8Highlander-1.0` — personal, research and educational use with attribution; redistribution and commercial use require the author's written permission. Documentation site: [wild8highlander.github.io/research-papers](https://wild8highlander.github.io/research-papers).
