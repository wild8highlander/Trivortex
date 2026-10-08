<!-- markdownlint-disable-file MD041 -->
<div align="center">

<!-- ══════════════════════════════════════════════════════════════ -->
<!-- TRIVORTEX — monumental navy-and-gold header                    -->
<!-- ══════════════════════════════════════════════════════════════ -->
<img src="docs/assets/logo-trivortex.svg" width="118" alt="The TRIVORTEX mark: three intertwined vortex rings over the Lagrange triangle"/>

<img src="docs/assets/banner-hero.svg" width="100%" alt="TRIVORTEX — The Three-Body Problem in the Vortex Model with the Chaplygin Topological Integral"/>

### The Three-Body (and N-Body) Problem in the Vortex Model

**Version 1.1 — the multi-language verification release.** A closed-form Lagrange-type rotating
solution (Theorem 3.1), a Chaplygin topological integral, a 22-section interactive
executable document, twelve companion studies with bilingual monographs, four
orbital animations — and an independent verification framework that re-derives
the core claims from scratch in eight languages: the Python ladder, the
interactive laboratory, Coq, Lean 4, Rust, Isabelle, Agda, C++ and Haskell.

<img src="docs/assets/divider-gold.svg" width="55%" alt="gold ornament divider"/>

**[Isaev Iskhak Khamzatovich](https://orcid.org/0009-0003-7299-0701)** · ORCID `0009-0003-7299-0701` · Independent Researcher

[📖 Documentation site](https://wild8highlander.github.io/Trivortex) · [📚 The document](code/) · [🧪 Verification](verification/) · [🔬 Research program](research/) · [🏛 Reading room](publications/) · [📝 How to cite](#19-citation-doi--zenodo)

<!-- ROW 1 — LIVE CI/CD -->
[![TRIVORTEX CI](https://img.shields.io/github/actions/workflow/status/wild8highlander/Trivortex/ci.yml?branch=main&style=for-the-badge&logo=github&label=TRIVORTEX%20CI)](https://github.com/wild8highlander/Trivortex/actions/workflows/ci.yml)
[![Lint](https://img.shields.io/github/actions/workflow/status/wild8highlander/Trivortex/lint.yml?branch=main&style=for-the-badge&logo=github&label=Lint)](https://github.com/wild8highlander/Trivortex/actions/workflows/lint.yml)
[![CodeQL](https://img.shields.io/github/actions/workflow/status/wild8highlander/Trivortex/codeql.yml?branch=main&style=for-the-badge&logo=github&label=CodeQL)](https://github.com/wild8highlander/Trivortex/actions/workflows/codeql.yml)
[![Docs Deploy](https://img.shields.io/github/actions/workflow/status/wild8highlander/Trivortex/deploy-docs.yml?branch=main&style=for-the-badge&logo=github&label=Docs%20Deploy)](https://github.com/wild8highlander/Trivortex/actions/workflows/deploy-docs.yml)
[![Docker](https://img.shields.io/github/actions/workflow/status/wild8highlander/Trivortex/docker.yml?branch=main&style=for-the-badge&logo=docker&label=Docker)](https://github.com/wild8highlander/Trivortex/actions/workflows/docker.yml)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/badge?org=wild8highlander&repo=Trivortex)](https://securityscorecards.dev/viewer/?uri=github.com/wild8highlander/Trivortex)

<!-- ROW 2 — SCHOLARLY IDENTITY -->
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21825394-blue?style=for-the-badge&logo=zenodo&label=Zenodo)](https://doi.org/10.5281/zenodo.21825394)
[![Concept DOI](https://img.shields.io/badge/Concept%20DOI-10.5281%2Fzenodo.21825393-blueviolet?style=for-the-badge&logo=zenodo&label=All%20Versions)](https://doi.org/10.5281/zenodo.21825393)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0003--7299--0701-a6ce39?style=for-the-badge&logo=orcid&logoColor=white)](https://orcid.org/0009-0003-7299-0701)
[![Citation](https://img.shields.io/badge/Cite-CITATION.cff-informational?style=for-the-badge&logo=latex)](CITATION.cff)
[![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=for-the-badge&logo=github)](LICENSE.md)
[![REUSE](https://img.shields.io/badge/REUSE-Compliant-2EA043?style=for-the-badge&logo=fsfe&logoColor=white)](REUSE.toml)

<!-- ROW 3 — PROJECT VITALS -->
[![Release](https://img.shields.io/badge/Release-v1.0.1-gold?style=for-the-badge&logo=github&label=Latest%20Release)](https://github.com/wild8highlander/Trivortex/releases)
[![pytest](https://img.shields.io/badge/pytest-126%20passed-2EA043?style=for-the-badge&logo=pytest)](verification/tests/)
[![Ladder](https://img.shields.io/badge/ladder-V1%E2%80%93V4%20%E2%9C%93%204%2F4-2EA043?style=for-the-badge)](verification/trivortex/python/verify.py)
[![Ports](https://img.shields.io/badge/ports-8%20landed%20%28M1%E2%80%93M3%29-2EA043?style=for-the-badge)](verification/README.md)
[![Document](https://img.shields.io/badge/document-22%20sections-1284BA?style=for-the-badge)](code/)
[![Studies](https://img.shields.io/badge/studies-12%20%C3%97%202%20languages-9558B2?style=for-the-badge)](research/)
[![Monographs](https://img.shields.io/badge/monographs-60%20renditions%20PDF%2BDOCX-8A2BE2?style=for-the-badge)](publications/)
[![Docs](https://img.shields.io/badge/Docs-GH%20Pages-blue?style=for-the-badge&logo=github)](https://wild8highlander.github.io/Trivortex)

<!-- ROW 4 — COMMUNITY PULSE -->
[![Stars](https://img.shields.io/github/stars/wild8highlander/Trivortex?style=for-the-badge&logo=github&color=yellow&label=Stars)](https://github.com/wild8highlander/Trivortex)
[![Forks](https://img.shields.io/github/forks/wild8highlander/Trivortex?style=for-the-badge&logo=github&color=blue&label=Forks)](https://github.com/wild8highlander/Trivortex/network/members)
[![Issues](https://img.shields.io/github/issues/wild8highlander/Trivortex?style=for-the-badge&logo=github&color=orange&label=Issues)](https://github.com/wild8highlander/Trivortex/issues)
[![PRs](https://img.shields.io/github/issues-pr/wild8highlander/Trivortex?style=for-the-badge&logo=github&color=blueviolet&label=PRs)](https://github.com/wild8highlander/Trivortex/pulls)
[![Commits](https://img.shields.io/github/commit-activity/t/wild8highlander/Trivortex?style=for-the-badge&logo=git&color=blue&label=Commits)](https://github.com/wild8highlander/Trivortex/commits/main)
[![Last Commit](https://img.shields.io/github/last-commit/wild8highlander/Trivortex/main?style=for-the-badge&logo=git&color=teal&label=Last%20Commit)](https://github.com/wild8highlander/Trivortex/commits/main)
[![Repo Size](https://img.shields.io/github/repo-size/wild8highlander/Trivortex?style=for-the-badge&logo=github&color=informational&label=Repo%20Size)](https://github.com/wild8highlander/Trivortex)
[![Languages](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](pyproject.toml)

</div>

---

## Table of contents

1. [What is TRIVORTEX](#1-what-is-trivortex)
2. [The three-body problem in 90 seconds](#2-the-three-body-problem-in-90-seconds)
3. [The vortex approach and the Chaplygin integral](#3-the-vortex-approach-and-the-chaplygin-integral)
4. [Theorem 3.1 — the closed form](#4-theorem-31--the-closed-form)
5. [Verification ladder V1–V4](#5-verification-ladder-v1v4)
6. [The pytest guard — 126 tests](#6-the-pytest-guard--126-tests)
7. [Inside the document — 22 sections](#7-inside-the-document--22-sections)
8. [The interactive menu — 15 modes](#8-the-interactive-menu--15-modes)
9. [The report engine — seven formats](#9-the-report-engine--seven-formats)
10. [Real astronomical presets](#10-real-astronomical-presets)
11. [The extended research program — TRX-01…12](#11-the-extended-research-program--trx-0112)
12. [Monographs and the reading room](#12-monographs-and-the-reading-room)
13. [Orbital animations](#13-orbital-animations)
14. [Documentation site (GitHub Pages)](#14-documentation-site-github-pages)
15. [Repository structure](#15-repository-structure)
16. [Quick start & reproduction](#16-quick-start--reproduction)
17. [The verification framework and milestones](#17-the-verification-framework-and-milestones)
18. [The research frontier — theorem pipeline and roadmap](#18-the-research-frontier--theorem-pipeline-and-roadmap)
19. [Citation, DOI & Zenodo](#19-citation-doi--zenodo)
20. [Community & governance](#20-community--governance)
21. [GitHub features inventory](#21-github-features-inventory)
22. [FAQ](#22-faq)
23. [License](#23-license)

---

## 1. What is TRIVORTEX

**TRIVORTEX** is the working title of a research program that studies the
**three-body (and N-body) problem** through a vortex formulation with a Chaplygin
topological integral. The core of the program — released here as
`code/trivortex_core*.py`, about 2 400 lines in each of three language mirrors —
is not a paper *about* the vortex model; it *is* the model: an executable
monograph whose every chapter is a section of working code, from the
Hofstadter-type Hamiltonian with embedded vortices (Section 4) through the
closed-form rotating solution (Section 5, Theorem 3.1) to spectral statistics,
quantum-topological observables, an interactive 15-mode menu and a seven-format
report engine (Section 12).

Version **1.0.0** is the **first public release** of the program, and it is
deliberately complete: everything the program promises — the executable document,
the independent verification ladder, twelve companion studies, the bilingual
monograph library in PDF and DOCX, the
orbital animations and the documentation site — exists in this repository,
regenerates from committed sources, and is checked on every push by CI.

Four commitments define the project, and every structural decision in this
repository serves them:

- **Executability.** The document runs: clone, `python3 code/trivortex_core_en.py`,
  and the whole 22-section apparatus is one menu away — verification suites,
  real-system presets, plots at 300 dpi, reports in TXT/MD/HTML/CSV/JSON/DOCX/PDF.
- **Independent verification.** The claims of Theorem 3.1 and the conservation
  laws are re-derived from scratch by a ladder of four checks
  (`verification/trivortex/python/verify.py`) that shares **no code** with the
  document, runs on every push in CI, and emits JSON protocols with full
  parameter snapshots. Numbers printed by the code that defines them are
  repetition; this repository insists on verification.
- **Registration before measurement.** Every acceptance check in the program —
  the ladder's V1–V4 and every study's checks alike — carries a target and a
  tolerance committed *before* the recorded run. A passing check is a claim held
  to a published band; a failing check is a broken claim, not a noisy measurement.
- **Honest boundaries.** The verified is separated from the recorded: the ladder
  certifies choreography, periodicity, the rigid Lagrange rotation and the
  vortex integrals — and explicitly labels the Chaplygin combination's endpoint
  drift as a window-dependent diagnostic, not a conservation law
  ([§5](#5-verification-ladder-v1v4), [honesty notes](verification/README.md)).

<div align="center">
<img src="docs/assets/orbits-showcase.svg" width="88%" alt="Three bodies, three dances: figure-eight choreography, Lagrange triangle, unequal circulations"/>
</div>

### What version 1.0.0 delivers

The first public release is a complete, self-consistent edition. Concretely, it ships:

- **the executable core document** — 22 sections × 3 language mirrors (RU/EN/default),
  an interactive 15-mode menu, a seven-format report engine, 300-dpi plot generation;
- **the independent verification ladder** — V1–V4 in three presets, JSON protocols,
  zero code shared with the document, run on every push;
- **a 27-test pytest guard** — 13 hard reference-value pins plus 14 tests covering
  the twelve studies and the monograph library;
- **twelve companion studies** (TRX-01…12) — executable scripts with registered
  acceptance checks, committed JSON protocols, schematic + four 300-dpi figures each;
- **the monograph library** — every study monograph in four renditions
  (Russian and English, each in typeset PDF and editable DOCX), plus the core
  monograph and the research compendium in the same four renditions — 56 documents
  in the reading room, rebuilt by one Make target;
- **four orbital animations** — GIF + MP4, deterministic generator committed;
- **a nine-page documentation site** on GitHub Pages, including a publications page;
- **the full GitHub toolchain** — CI, lint, CodeQL, Pages deploy, Docker
  toolchains, issue/PR templates, code owners, Dependabot, release drafter,
  link checker, OpenSSF Scorecard, dev container, Zenodo minting.

### The program in one table

| Layer | Where | What it is | Verified by |
|---|---|---|---|
| The core document | [`code/`](code/) | 22-section executable monograph, 3 language mirrors | ladder V1–V4 + 13 pytest pins |
| The ladder | [`verification/`](verification/) | independent from-scratch checker, 3 presets | runs in CI on every push |
| The guard | [`verification/tests/`](verification/tests/) | 63 pytest tests: reference values + port pins + smoke suites | CI green badge |
| Twelve studies | [`research/`](research/) | TRX-01…12 executable companion studies | 60+ registered checks, all PASS |
| Monograph library | [`publications/`](publications/) | 28 PDFs + 28 DOCX + 14 HTML sources (RU and EN separate) | rebuilt by `make pdf-library` |
| Animations | [`docs/animations/`](docs/animations/) | 4 choreographies in GIF + MP4 | regenerated by `make animations` |
| Documentation site | [`docs/site/`](docs/site/) | 9-page static site on GitHub Pages | deployed by CI |
| **Cycloring** | [`cycloring/`](cycloring/) | the Gamma-period ring laboratory — mini-research with its own W-ladder, monographs, bilingual figures | 37 tests + W1–W7, all PASS |
| **Polyvortex** | [`polyvortex/`](polyvortex/) | the N-vortex extension bench — Theorems A/B/E, Lemmas C/D, the π ln 2 boundary | 26 tests + W1–W7, all PASS |

---

## 2. The three-body problem in 90 seconds

Ask three masses to move under their mutual Newtonian attraction and you have
posed the problem that shaped three centuries of mathematics. Newton solved the
two-body problem completely; the three-body problem resisted. Euler and Lagrange
found exact special solutions — the collinear and equilateral central
configurations, rotating rigidly like a spun coin. Poincaré, attacking the
restricted problem, discovered that no general closed-form solution exists and, in
the wreckage of the prize memoir, invented what we now call chaos: nearby initial
conditions diverge, prediction has a horizon, and the phase space is stitched
together from periodic orbits rather than from a formula.

The modern era replaced the impossible *general* solution with an atlas of
remarkable *particular* ones: Lagrange's triangle, Euler's line, the
figure-eight choreography of Chenciner–Montgomery (2000), and a growing zoo of
choreographic solutions — periodic orbits on which equal masses chase each other
along a shared closed curve, phases evenly spread. The problem remains a living
field precisely because special exact solutions are both rare and verifiable:
either the equations hold them to machine precision, or they do not.

A short field guide to the atlas of exact solutions that the program draws on:

| Solution | Year | System | Where it appears in the program |
|---|---|---|---|
| Euler collinear configurations | 1767 | gravitational 3-body | the libration-line family (TRX-01, TRX-12) |
| Lagrange equilateral triangle | 1772 | gravitational 3-body | the triangle of Theorem 3.1 and its vortex twin (TRX-08, TRX-09) |
| Kirchhoff vortex triangle | 1876 | point vortices | the classical anchor study TRX-09 |
| Restricted problem & Trojan clouds | 1906→ | Sun–Jupiter + asteroids | the photogravitational extension (TRX-01) |
| Sitnikov problem | 1960 | restricted 3-body | oscillatory chores of the chaos layer |
| Figure-eight choreography | 2000 | equal masses | the GW-emitter study TRX-11, animation `anim02` |
| Butterfly / yarn / goggles families | 2013 | equal masses | the broader choreography atlas (roadmap) |
| Efimov trimers | 1970 | quantum 3-body | the universality study TRX-07 |

That verifiability is what TRIVORTEX leans on. The vortex formulation trades
Newtonian masses for vortices with circulations — a Hamiltonian, first-order
system whose special solutions are algebraically sharp — and the document's
central theorem is exactly one of those sharp special solutions: a rotating
equilateral choreography with a radial modulation, pinned to ~1e-14 by an
independent checker.

| Milestone | Year | Contribution to the program's viewpoint |
|---|---|---|
| Newton, *Principia* | 1687 | two-body problem solved completely |
| Euler | 1767 | collinear central configurations |
| Lagrange, *Essai* | 1772 | equilateral central configurations — the triangle of Theorem 3.1 |
| Poincaré | 1890 | no general closed form; chaos enters mechanics |
| Kirchhoff | 1876 | point-vortex equations — the program's dynamics |
| Chaplygin | early 1900s | vortex invariants — the program's topological integral |
| Chenciner–Montgomery | 2000 | the figure-eight choreography — a modern exact solution |
| Moore / Šuvakov–Dmitrašinović | 1993 / 2013 | the choreography zoo expands |

---

## 3. The vortex approach and the Chaplygin integral

In the vortex model the three "bodies" are point vortices with circulations and
topological charges `q_k = (1, −1, 1)`. Their Kirchhoff dynamics are Hamiltonian;
the conserved quantities are algebraic; and — the model's signature move — each
vortex carries an effective Aharonov–Bohm flux, so the angular momentum binds to
the gauge field in a combination the document attributes to Chaplygin:

<div align="center">

**C_Ch = r² · (θ̇ − q·A_θ), with A_θ = 1/r**

</div>

This topological integral is the control knob of the model: it fixes the rotation
frequency and the radial modulation amplitude of the closed-form solution
([§4](#4-theorem-31--the-closed-form)). Around it, the document builds:

- a **lattice Hamiltonian** — an L×L Hofstadter matrix with `N_v` embedded
  vortices: Peierls phases from the uniform flux α, vortex-induced AB phases,
  charge-weighted core potentials, Hermitian symmetrization (Section 4);
- a **spectral layer** — unfolding, the ⟨r⟩ statistic against GUE/GOE/Poisson
  references, KS tests, number variance, spectral form factor (Sections 7, 20–21);
- a **quantum-topological layer** — Berry phase, Chern numbers by
  Fukui–Hatsugai–Suzuki, TKNN conductance, Dirac cones (Sections 16–19);
- a **chaos layer** — Lyapunov exponents, permutation tests, KAM statistics,
  Poincaré sections (Section 22);
- **real astronomical presets** — Sun–Earth–Moon, α Centauri,
  Pluto–Charon–Nix (Section 10, [§10](#10-real-astronomical-presets)).

The document is honest about its lineage: the choreography viewpoint descends
from Lagrange and the modern choreography literature; the vortex formalism from
Kirchhoff and the classical vortex-atom programme; the topological integral from
Chaplygin's invariants. TRIVORTEX adds the AB-flux dressing and, above all, the
verification discipline — it is a model study with exact checks, not a claim
about planetary motion.

| Ingredient | Classical source | Role in the model |
|---|---|---|
| Point vortices with circulations Γ_k | Kirchhoff (1876), Helmholtz (1858) | the "bodies" of the problem |
| Hamiltonian H = −Σ ΓᵢΓⱼ ln(rᵢⱼ)/2π | Kirchhoff–Onsager | conserved energy of the dynamics |
| Linear impulses P = Σ Γx, Q = Σ Γy | classical vortex theory | translation invariants (V3) |
| Angular impulse I = Σ Γr² | classical vortex theory | rotation invariant (V3) |
| Aharonov–Bohm flux per vortex | quantum AB effect (1959) | gauge dressing of each vortex |
| C_Ch = r²(θ̇ − qA_θ) | Chaplygin's invariants | the topological control knob |

---

## 4. Theorem 3.1 — the closed form

The document's central result (Section 5) is a Lagrange-type relative equilibrium
with radial modulation — three vortices that keep an exact equilateral triangle
while rotating with a frequency fixed by the Chaplygin constant:

<div align="center">

**r_k(t) = √C_Ch · (1 + ε·cos(ωt + 2πk/3)),  θ_k(t) = ωt + 2πk/3**

**ω = (2π/T)·e^(C_Ch/π),  ε = 1/(e^(C_Ch/π) − 1)**

</div>

Two structural properties follow from the form itself and are what the
verification ladder certifies:

1. **Equilateral choreography** — the angular positions differ by exactly `2π/3`
   at every instant; the triangle rotates rigidly, the vortex twin of the
   classical Lagrange solution of the gravitational three-body problem.
2. **Periodicity** — the radial modulation repeats with period `T_r = 2π/ω`;
   the closed form is a periodic orbit of the model.

Reference values for the canonical configuration `C_Ch = 1`, `T = 2π`:

| Quantity | Value (float64) | Verified by |
|---|---|---|
| frequency `ω = (2π/T)·e^{1/π}` | `1.3748022274393588` | pytest pin, exact to float64 |
| amplitude `ε = 1/(e^{1/π}−1)` | `0.7276379117656014` | pytest pin, exact to float64 |
| angular separation (all probed times) | `2π/3 ± 6.9×10⁻¹⁴` | ladder V1 |
| periodicity residual over `100·T` | `≤ 9.4×10⁻¹⁴` | ladder V1 |

The theorem has a numerical twin that needs no closed form at all: three *equal*
point vortices released on an equilateral triangle integrate forward (Kirchhoff
equations, RK4) rotating rigidly at the classical angular velocity
**ω_L = 3Γ/(2πa²)** — certified by ladder check V2 — while the four classical
integrals `H, P, Q, I` are conserved along the trajectory (V3), with or without
the symmetric initial condition (V4). The full statement, the certified-vs-recorded
boundary and the honesty notes live on the
[Theorem 3.1 page](https://wild8highlander.github.io/Trivortex/theorem-3-1.html)
and in the [verification framework README](verification/README.md).

---

## 5. Verification ladder V1–V4

`verification/trivortex/python/verify.py` re-implements — independently, from
scratch, numpy-only — everything it checks: the closed form, the Chaplygin
combination, the Kirchhoff right-hand side, its own RK4 stepper. It runs in three
presets (`quick` ≈ 0.5 s, `default` ≈ 2 s, `full` ≈ 35 s) and writes a JSON
protocol per run. Registered criteria and the latest reference results:

| Check | Statement | Registered criterion | Result |
|---|---|---|---|
| **V1** | Theorem 3.1 closed form: `2π/3` choreography + periodicity | separation ≤ 1e-12; periodicity ≤ 1e-12 | ✅ `6.9×10⁻¹⁴` / `9.4×10⁻¹⁴` |
| **V2** | Lagrange triangle rotates rigidly at `ω = 3Γ/(2πa²)` | shape ≤ 1e-10; ω rel. err ≤ 1e-6 | ✅ `1.6×10⁻¹⁴` / `2.9×10⁻¹²` |
| **V3** | Vortex integrals `H, P, Q, I` conserved (equal Γ) | worst rel. drift ≤ 1e-10 | ✅ `2.9×10⁻¹⁴` |
| **V4** | Integrals conserved for `Γ = (1, 2, 3)`, generic triangle | worst rel. drift ≤ 1e-10 | ✅ `2.9×10⁻¹⁴` |

**What each preset does**

| Preset | Rotations | Steps/period | C_Ch points | Wall time | Used by |
|---|---|---|---|---|---|
| `quick` | 2 | 2 000 | 200 | ≈ 0.5 s | CI (every push) |
| `default` | 5 | 4 000 | 1 000 | ≈ 2 s | local checks |
| `full` | 20 | 8 000 | 2 000 | ≈ 35 s | release validation |

<div align="center">
<img src="docs/assets/ladder-accuracy.png" width="92%" alt="Ladder V1-V4: recorded residuals vs registered tolerance bands (log scale)"/>
</div>

> **Honesty note.** The combination `C_Ch(t) = r²(θ̇ − q·A_θ)` (A_θ = 1/r) *oscillates
> together with the radial modulation of the closed form* — by construction of the
> model. Section 6 of the document records its endpoint drift over `[0, 100·T]` as a
> **diagnostic**; the ladder reports the same number as a diagnostic and gives it no
> pass/fail role. The window-independent conserved quantities of the dynamics are
> the vortex integrals `H, P, Q, I` — and those are what V3–V4 certify.

---

## 6. The pytest guard — 126 tests

The suite in [`verification/tests/`](verification/tests/) pins the analytic layer
to hard reference values, guards all seven landed language ports and wraps the
whole research program in CI-friendly form; the mini-repositories
[`polyvortex/tests/`](polyvortex/tests/) and
[`cycloring/tests/`](cycloring/tests/) add 26 and 37 more (the N-vortex bench
and the Gamma-period ring laboratory, both self-contained). Together:
**126 tests** in ≈ 30 s, only `numpy`, `scipy` and `pytest` required.

| Suite | Tests | What they guard |
|---|---|---|
| `test_trivortex.py` | 13 | Theorem 3.1 reference values (ω, ε, periodicity, C_Ch formula shape), ladder quick-run in-process, JSON protocol shape |
| `test_ports.py` | 36 | the seven landed ports: artifact presence, SPDX headers, the bilingual README_RU contract, and the committed Rust/C++ protocols pinned against the Python ladder's reference numbers |
| `test_research_smoke.py` — smoke | 12 | every TRX study executes in `--smoke` mode and reports `status: PASS` |
| `test_research_smoke.py` — completeness | 1 | all twelve studies ship README, code, pack, figures, monograph sources and four monograph renditions |
| `test_research_smoke.py` — library | 1 | the reading room: 28 PDFs + 28 DOCX + HTML sources + build system |
| `test_cr_*.py` (cycloring) | 37 | the Gamma-period ring laboratory: the reflection and sine-product identities, the defect chain and the transducer, the root system, the polygon flow, the transport identity, the synchronous closure, the transducer table of the levels 7/9/15/30 |
| `test_*` (polyvortex) | 26 | the N-vortex extension bench: ω_N for N = 2..8, the π ln 2 admissibility threshold, the H1 registers, the Havelock spectra, cross-pins against the parent ladder |

---

## 7. Inside the document — 22 sections

One physics kernel, three language mirrors (`trivortex_core.py` — default English
console; `_ru.py` — Russian; `_en.py` — English), each with the identical
22-section structure:

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

The [code/README.md](code/README.md) documents every section, the menu modes and
the report engine in depth; the documentation site mirrors it in browser form
([code page](https://wild8highlander.github.io/Trivortex/code.html)).

---

## 8. The interactive menu — 15 modes

Run `python3 code/trivortex_core_en.py` (or the RU mirror) and the document
greets you with a numbered menu. Every mode writes artifacts, not just console
output — results land in `code/outputs/` as JSON protocols and 300-dpi plots.

| Mode | Name | What it does | Writes |
|---|---|---|---|
| 1 | Full verification | runs the complete internal test battery end-to-end | reports + plots |
| 2 | Chaplygin conservation | Section-6 check of the topological integral along the closed form | JSON + report |
| 3 | RMT statistics | ⟨r⟩ statistic vs GUE/GOE/Poisson across lattice sizes | JSON + plots |
| 4 | Montgomery test | pair-correlation comparison against ζ zeros | JSON + report |
| 5 | Quantum suite | Berry phases and topological qubits across flux values | JSON + plots |
| 6 | Real systems | the three astronomical presets through the model | JSON + report |
| 7 | Hamiltonian spectrum | builds the Hofstadter matrix, prints leading eigenvalues | — |
| 8 | Analytical solution | verifies Theorem 3.1 closed form point-by-point | report |
| 9 | Custom N-vortex | runs the N-vortex simulation for any `N_v ≥ 3` | plots |
| 10 | Generate reports | the seven-format report engine over the latest results | TXT/MD/HTML/CSV/JSON/DOCX/PDF |
| 11 | Generate plots | the full 300-dpi figure set | PNG |
| 12 | Topological suite | Berry/Chern/TKNN observables | JSON + plots |
| 13 | Advanced RMT | spectral form factor, IPR, number variance | JSON + plots |
| 14 | Chaos suite | Lyapunov exponents + permutation entropy | JSON + plots |
| 15 | Cross-correlations | correlation matrix across observable channels | matrix printout |
| C/S/H/Q | — | configure parameters · show configuration · help · quit | — |

The menu is EOF-safe: piping input, closing the terminal or pressing Ctrl-D
exits cleanly instead of raising a traceback.

---

## 9. The report engine — seven formats

Section 12 of the document turns any result set into seven synchronized formats.
The same content, the same numbers, seven shapes — no manual re-typing anywhere:

| Format | Purpose | Produced for |
|---|---|---|
| TXT | plain-text protocol, terminal-friendly | archives, diffs |
| MD | GitHub-renderable summary with tables | READMEs, issues |
| HTML | styled single-file report | browser reading, sharing |
| CSV | flat numeric tables | spreadsheets, pipelines |
| JSON | full machine-readable protocol | CI, re-analysis |
| DOCX | editable Word document | word processors |
| PDF | print-ready edition | printing, citation |

---

## 10. Real astronomical presets

Section 10 wires three real triples into the model as `RealSystem` records —
masses, characteristic distances, characteristic periods — used as parameter
scales and reality anchors (not as ephemeris simulations):

| System | Bodies | Scale span | Why this system |
|---|---|---|---|
| **Sun–Earth–Moon** | Sun · Earth · Moon | 1 AU hierarchy | the canonical triple of celestial mechanics |
| **α Centauri** | α Cen A · α Cen B · Proxima | 5.3 ly, hierarchical | the nearest real three-star system |
| **Pluto–Charon–Nix** | Pluto · Charon · Nix | 39 AU, compact | a dynamically rich small triple |

Why these three: they span six orders of magnitude in scale and illustrate exactly
why the three-body problem admits no universal closed form. The verification
ladder deliberately does **not** use them — V1–V4 operate on exact model objects,
keeping the certified core clean of astronomical parameter noise. Details:
[system presets page](https://wild8highlander.github.io/Trivortex/system-presets.html).

---

## 11. The extended research program — TRX-01…12

Twelve companion studies — each an executable script plus a documented README —
attack the three-body problem through twelve physical systems, with **lasers at
the center of ten of them**. Every study carries: a deterministic `numpy/scipy`
script with `--smoke` and `--figures` modes, a committed JSON protocol with
registered checks, a schematic SVG and four 300-dpi PNG figures, a bilingual
monograph (RU/EN × PDF/DOCX) and a 26-section README.

| # | Study | Block | Key verified number | Checks |
|---|-------|-------|---------------------|--------|
| 01 | [Laser-dressed restricted 3-body problem](research/TRX-01-laser-radiation-pressure/README.md) | Laser optics | L1 = 0.8369151 (Earth–Moon); Jacobi drift ≤ 1e-10 | 6/6 |
| 02 | [Resonant three-wave mixing](research/TRX-02-three-wave-mixing/README.md) | Laser optics | Manley–Rowe drift ≤ 4.5e-15; SHG η = tanh² to 2e-16 | 5/5 |
| 03 | [Three-soliton molecule (fiber laser)](research/TRX-03-soliton-molecule/README.md) | Laser optics | spacing s\* = 0.2018927 to 1e-9; breathing mode to 0.3% | 5/5 |
| 04 | [Photon fluid — three Kerr solitons](research/TRX-04-photon-fluid/README.md) | Laser optics | Lagrange beam triangle, ω to 1.4e-8; binary bound state | 5/5 |
| 05 | [Optical vortices ≈ point vortices](research/TRX-05-optical-vortices/README.md) | Laser optics | rotation 3Γ/(2πa²) to 1e-8; winding number = 3 | 5/5 |
| 06 | [Helium as the Coulomb three-body problem](research/TRX-06-helium-three-body/README.md) | Quantum matter | CTMC: autoionization channel; escaper overshoot 7.3× | 7/7 |
| 07 | [Efimov effect](research/TRX-07-efimov/README.md) | Quantum matter | s₀ = 1.006238; ladder 515.5/515.0 vs exp(2π/s₀) = 515.03 | 5/5 |
| 08 | [Three laser-cooled ions (Paul trap)](research/TRX-08-ion-trap/README.md) | Quantum matter | crystal side a = 3^(1/3) exact; modes {0, ω₀, √3ω₀} | 5/5 |
| 09 | [Kirchhoff–Chaplygin three vortices](research/TRX-09-vortex-trio/README.md) | Classical anchor | ω = 3/(2πa²) to 1e-8; I, H, P, Q to 1e-12 | 5/5 |
| 10 | [Kozai–Lidov oscillations](research/TRX-10-kozai-lidov/README.md) | Celestial mechanics | e_max to 2e-3; direct 3-D validation 2.8% | 4/4 |
| 11 | [Figure-eight choreography as a GW source](research/TRX-11-gw-choreography/README.md) | Celestial mechanics | T = 6.3259140; L = 0; harmonic comb n = 6 | 7/7 |
| 12 | [Laser light sail at L4/L5](research/TRX-12-laser-light-sail/README.md) | Laser optics | hold ≤ 7.5e-7 vs 4.1e-3 free drift; Jacobi pumped | 5/5 |

<div align="center">
<img src="docs/assets/program-checks-dashboard.png" width="92%" alt="All 80 registered acceptance checks across the twelve studies, all PASS"/>
</div>

**How the blocks fit together.** The *classical anchor* (TRX-09) is the
point-vortex trio that Theorem 3.1 formalizes; the *laser-optics* block
re-expresses the same equilateral geometry in photonic systems; the
*quantum-matter* block shows the three-body structure in trapped particles and
universality ladders; the *celestial* block returns to gravitation — secular
dynamics and gravitational waves. Every study cross-links its neighbors, and the
[compendium](publications/pdf/TRIVORTEX-Research-Compendium_EN.pdf) quotes every
acceptance protocol in full.


### The four blocks in narrative

**Laser optics (TRX-01, 02, 03, 04, 05, 12).** Six studies translate the
three-body geometry into photonic systems. A laser pointed at one primary of the
Earth–Moon problem reshapes the libration landscape without adding a mass
(TRX-01); three waves in a χ⁽²⁾ crystal form the exactly integrable
"three-body of optics" with Manley–Rowe invariants (TRX-02); three ultrashort
pulses in a mode-locked fiber bind into a phase-locked soliton molecule with a
breathing mode (TRX-03); three Kerr solitons in a photon fluid draw a rotating
Lagrange beam triangle (TRX-04); the phase singularities of a paraxial laser
field move like Kirchhoff vortices, winding three times per pattern rotation
(TRX-05); and a photon sail rides the same Earth–Moon problem as an actuator,
holding L4 seven hundred times tighter than free drift (TRX-12). The laser is
the program's experimental bridge: every one of these systems is, in principle,
buildable on an optical table.

**Quantum matter (TRX-06, 07, 08).** Three bodies reappear where classical
intuition fades. Helium is a Coulomb three-body problem whose classical
trajectory Monte Carlo exposes the autoionization channel and the Wannier
kinematics of the escaping electron (TRX-06); two fermions plus a third in the
−1/R² regime produce the Efimov ladder — a geometric tower of trimers spaced by
exp(π/s₀) ≈ 515 per decade of energy, with the transcendental constant
s₀ = 1.006238 verified numerically (TRX-07); and three laser-cooled ions in a
Paul trap crystallize into exactly the equilateral Lagrange triangle, with a
Hessian spectrum {0, ω₀, √3ω₀, …} that the study pins to machine precision
(TRX-08).

**The classical anchor (TRX-09).** The point-vortex trio is the study the whole
program stands on: three same-sign Kirchhoff vortices on an equilateral triangle
rotate rigidly at ω = 3Γ/(2πa²), carry the angular impulse I = Σ Γr², and
conserve H, P, Q — the exact classical prototype of Theorem 3.1 and of the
Chaplygin integral. If a future language port disagrees with the core document,
this study is the arbiter.

**Celestial mechanics (TRX-10, 11).** The program returns to gravitation at
scale: the Kozai–Lidov mechanism exchanges inclination and eccentricity in
hierarchical triples, and the study builds the doubly-averaged quadrupole
dynamics numerically — no memorized formulas — then validates it against a
direct 3-D restricted integration to 2.8% (TRX-10); and the figure-eight
choreography of Chenciner–Montgomery is integrated at 1e-12 to certify its
period T = 6.3259140, its zero angular momentum, and its harmonic comb — the
computational source for a gravitational-wave detector study (TRX-11).



### Per-study dossiers

**TRX-01 — Radiation-pressure restricted three-body problem (laser on dust).**
The CR3BP with a laser on primary 1: photon pressure renormalizes its pull by
(1 − β). The study recovers the published Earth–Moon L1 = 0.8369151 at β = 0,
shows the triangular point migrating monotonically toward the radiating primary
(4.1e-2 at β = 0.1), keeps the displaced L4 marginally stable, and conserves the
Jacobi integral to 8.9e-16 — the foundation of the laser-highway application.

**TRX-02 — Resonant three-wave mixing.** Pump, signal and idler in a χ⁽²⁾
crystal: the exactly integrable three-wave system of nonlinear optics. The
Manley–Rowe invariants hold to 4.5e-15 over thousands of mixing lengths, the
SHG conversion efficiency follows η = tanh²(Γz) to 2e-16, and the back-conversion
cycle closes exactly — the optical twin of an integrable three-body problem.

**TRX-03 — Three-soliton molecule (fiber laser).** Three ultrashort pulses bind
into a phase-locked molecule: relaxation to the equilibrium spacing
s\* = 0.2018927 to 1e-9, conservative oscillations around it, and the breathing
normal mode reproduced to 0.3% — a bound state of light with the architecture
of a three-body molecule.

**TRX-04 — Photon fluid: three Kerr solitons.** Spatial solitons in a focusing
Kerr medium form a rigidly rotating Lagrange triangle of beams (ω matched to
1.4e-8), demonstrate antiphase repulsion of unequal solitons, and realize the
binary bound state with precession — hydrodynamics of light with vortex kinematics.

**TRX-05 — Optical vortices ≈ point vortices.** Phase singularities of a
paraxial field obey Kirchhoff's equations: the three-lobed pattern rotates at
3Γ/(2πa²) to 1e-8, the total winding number is exactly 3, and the angular
impulse I = Σ Γr² is conserved — the photonic realization of the classical anchor.

**TRX-06 — Helium as the Coulomb three-body problem.** Two electrons and a
nucleus integrated by CTMC: the autoionization channel opens on schedule, and
the escaping electron carries the Wannier overshoot — 7.3× the excess energy —
the classical fingerprint of three-body Coulomb breakup.

**TRX-07 — The Efimov effect.** The universal quantum three-body ladder: the
transcendental exponent s₀ = 1.006238 pinned against the Sturmian reference, and
the geometric ratio of consecutive trimers 515.5/515.0 against
exp(2π/s₀) = 515.03 — universality verified, not asserted.

**TRX-08 — Three laser-cooled ions in a Paul trap.** Doppler-cooled ions
crystallize into the equilateral configuration with side a = 3^(1/3) (exact),
and the Hessian spectrum {0, ω₀, √3ω₀, …} matches the analytic normal modes —
the Lagrange triangle rebuilt from cold atoms.

**TRX-09 — Kirchhoff–Chaplygin three vortices (the anchor).** Three same-sign
vortices: rigid rotation at ω = 3/(2πa²) to 1e-8, the integrals I, H, P, Q
conserved to 1e-12, and the angular impulse I = Σ Γr² carried exactly — the
classical prototype of Theorem 3.1.

**TRX-10 — Kozai–Lidov oscillations.** The doubly-averaged quadrupole dynamics
built numerically (no memorized formulas), e_max matching the analytic bands to
2e-3, and a direct 3-D restricted integration validating the secular picture to
2.8% — hierarchical triples under control.

**TRX-11 — Figure-eight choreography as a GW source.** The Chenciner–Montgomery
orbit integrated at 1e-12: period T = 6.3259140, angular momentum L = 0, the
 quadrupole quantity Q(T/3) = Q(0) by symmetry, and a harmonic comb dominated by
n = 6 — a computational source for gravitational-wave studies.

**TRX-12 — Laser light sail at L4/L5.** A photon sail in the Earth–Moon CR3BP:
PD beam-steering holds L4 to ≤ 7.5e-7 versus 4.1e-3 free drift (≈ 5 500×
tighter), and along-velocity thrust pumps the Jacobi constant monotonically —
stationkeeping as an applied three-body discipline.

### Anatomy of a study README

Every study follows the same 26-section skeleton (generated from its committed
content pack, so nothing drifts out of sync with the code and protocols):

| § | Section | § | Section |
|---|---|---|---|
| 1 | Mission | 14 | Conclusions |
| 2 | Introduction and historical context | 15 | The monograph and its renditions |
| 3 | Physical system and preset | 16 | Data, artifacts and reproduction |
| 4 | Governing equations (E1, E2, …) | 17 | Cross-links within the program |
| 5 | Scheme (annotated SVG) | 18 | Inside the script |
| 6 | Mapping to TRIVORTEX | 19 | Tolerance rationale and honesty |
| 7 | Dimensionless formulation | 20 | Repository navigation |
| 8 | Numerical method | 21 | Notation |
| 9 | Verification protocol + recorded run | 22 | References |
| 10 | Figure gallery (300 dpi) | 23 | Glossary |
| 11 | Results (full run) | 24 | Appendix A. Full parameter table |
| 12 | Analysis | 25 | Appendix B. BibTeX |
| 13 | Discussion and honest boundaries | 26 | How to cite |


### The numbers of version 1.0.0

Every check registered by the program, at a glance. The full protocols live in
`research/TRX-*/results/*.json` and are quoted verbatim in the compendium and in
each study README.

| Check | Registered band | Recorded | Verdict |
|---|---|---|---|
| V1 separation / periodicity | ≤ 1e-12 | 6.9e-14 / 9.4e-14 | PASS |
| V2 shape / ω error | ≤ 1e-10 / ≤ 1e-6 | 1.6e-14 / 2.9e-12 | PASS |
| V3 worst integral drift | ≤ 1e-10 | 2.9e-14 | PASS |
| V4 worst integral drift | ≤ 1e-10 | 2.9e-14 | PASS |
| TRX-01 Jacobi drift | ≤ 1e-10 | 8.9e-16 | PASS |
| TRX-02 Manley–Rowe drift | ≤ 1e-12 | 4.5e-15 | PASS |
| TRX-03 equilibrium spacing | 0.2018927 ± 1e-9 | 0.2018927 | PASS |
| TRX-04 triangle ω | ± 1e-6 rel. | 1.4e-8 | PASS |
| TRX-05 pattern rotation ω | ± 1e-6 rel. | 1e-8 | PASS |
| TRX-06 escaper overshoot | 7.3× ± 10% | 7.3× | PASS |
| TRX-07 ladder ratio | 515.03 ± 0.5% | 515.0–515.5 | PASS |
| TRX-08 crystal side | 3^(1/3) ± 1e-10 | exact | PASS |
| TRX-09 vortex ω | ± 1e-6 rel. | 1e-8 | PASS |
| TRX-10 e_max | ± 2e-3 | 2e-3 | PASS |
| TRX-11 period T | 6.3259140 ± 1e-7 | 1.2e-8 | PASS |
| TRX-12 L4 hold | ≤ 1e-5 | 7.5e-7 | PASS |

### The mini-research programs — CYCLORING and POLYVORTEX

Beyond the twelve studies, the program grows through two self-contained
**mini-research programs** — full laboratories with their own W-ladders
(seven registered stages each), their own bilingual monograph stacks,
their own committed protocols and their own pytest guards:

| | [**CYCLORING**](cycloring/README.md) | [**POLYVORTEX**](polyvortex/README.md) |
|---|---|---|
| scope | the regular N-vortex ring as the root system of one binomial — Γ-periods, the defect chain, the synchronous breathing | lifting Theorem 3.1 to arbitrary N — Layer K (Kirchhoff numeric) against Layer G (the closed form) |
| headline | the algebraic boundary Ω(a, N−a) = π/sin(πa/N) at 5.1e−49; the breathing closes exactly at 3.1e−16 | the admissibility threshold **C_Ch > π ln 2**; the Havelock threshold N ≤ 7 stable / N ≥ 8 unstable (+0.4502) |
| ladder | W1–W7, all PASS | W1–W7, all PASS |
| guard | 37 tests | 26 tests |
| publication stack | the big monograph + Theorems 1–5 × RU/EN × PDF/DOCX | the big monograph + Theorems A/B/E, Lemmas C/D × RU/EN × PDF/DOCX |

<div align="center">

**CYCLORING — the algebraic boundary of the period domain (W1–W2)**

<img src="cycloring/figures/fig01_periods_lattice.png" width="78%" alt="CYCLORING: the period field and its algebraic boundary"/>

**POLYVORTEX — the Havelock stability threshold (W4)**

<img src="polyvortex/figures/fig03_stability_scan.png" width="78%" alt="POLYVORTEX: the Havelock stability scan and the threshold spectra"/>

</div>

Both mini-programs are covered by the same CI that guards the parent:
syntax checks, the pytest guard and their W-ladders run on every push.

---

## 12. Monographs and the reading room

Every research artifact of the program exists as a typeset, language-separated
document. **Russian and English are separate files** — each language can be
read, printed and cited independently — and each exists in two renditions, a
vector PDF and an editable DOCX.

| Collection | Files | Where |
|---|---|---|
| Study monographs (12 studies × RU/EN × PDF/DOCX) | 48 | [`research/TRX-*/monograph/`](research/) |
| Study monographs, reading-room copies | 24 | [`publications/pdf/`](publications/pdf/) + [`publications/docx/`](publications/docx/) |
| Core monograph (the executable document as a book) | 2 PDF + 2 DOCX | [`publications/pdf/TRIVORTEX-Core-Monograph_RU.pdf`](publications/pdf/) … |
| Research compendium (program map with every protocol) | 2 PDF + 2 DOCX | [`publications/pdf/TRIVORTEX-Research-Compendium_EN.pdf`](publications/pdf/) … |
| HTML sources (1:1 with the study PDFs) | 14 | [`publications/html/`](publications/html/) |

**What the design guarantees.** Navy-gold covers with the study metadata (author,
ORCID, DOI, sources, license); MathML equations rendered offline by pandoc;
300-dpi figures embedded with captions; striped tables with repeating headers;
page numbers stamped by the renderer (cover unnumbered, body from 1); PDF
metadata (title, author, keywords); DOCX files restyled into the same system
with Word-native page fields.

**Naming scheme.** Every rendition is addressable without opening it:

| Pattern | Example | Meaning |
|---|---|---|
| `TRX-<nn>-<slug>_<LANG>.pdf` | `TRX-09-vortex-trio_RU.pdf` | study monograph, Russian, typeset |
| `TRX-<nn>-<slug>_<LANG>.docx` | `TRX-09-vortex-trio_EN.docx` | study monograph, English, editable |
| `TRIVORTEX-Core-Monograph_<LANG>.pdf` | `…_EN.pdf` | the executable core as a book |
| `TRIVORTEX-Research-Compendium_<LANG>.pdf` | `…_RU.pdf` | the program map with all protocols |
| `monograph_<LANG>.pdf` (study folders) | `monograph_RU.pdf` | the rendition next to its sources |

**Rebuild the whole library with one command:**

```bash
make pdf-library          # 28 PDFs + 28 DOCX from committed markdown sources
```

The build system lives in [`publications/build/`](publications/build/):
`md2html_lib.py` (navy-gold design system + Chromium rendering),
`build_pdf_library.py` (the twelve studies),
`build_special_pdfs.py` (core monograph + compendium),
`finalize_pdf.py` (metadata stamping + QA). Dependencies: Python ≥ 3.10 with
`pypdf` and `python-docx`, `pandoc` ≥ 3.x, Playwright's Chromium. No study data
is recomputed — the PDFs typeset the committed results.

---

## 13. Orbital animations

[`docs/animations/`](docs/animations/) turns four choreographies of the program
into seamless-loop animations, each in GIF (inline) and MP4 (high bitrate):

| Animation | Choreography | Integrator | Source |
|---|---|---|---|
| `anim01_trivortex_ring` | Theorem 3.1 breathing ring (vortex model) | closed form + Kirchhoff RK4 | core document |
| `anim02_figure_eight` | Chenciner–Montgomery free-fall eight | DOP853 at 1e-12 | TRX-11 |
| `anim03_lagrange_triangle` | Lagrange (1772) rigid rotation | RK4, ω = √(3/a³) | TRX-09 |
| `anim04_laser_stationkeeping` | laser-damped libration at L4\* | photogravitational CR3BP, β = 0.05 | TRX-01 + TRX-12 |

Regenerate everything with `make animations`
([`make_animations.py`](docs/animations/make_animations.py) is the committed,
deterministic generator). Physics and reproduction notes:
[docs/animations/README.md](docs/animations/README.md).

---

## 14. Documentation site (GitHub Pages)

The site at **[wild8highlander.github.io/Trivortex](https://wild8highlander.github.io/Trivortex)**
is a static, dependency-free build published by
[`deploy-docs.yml`](.github/workflows/deploy-docs.yml) from `docs/site/`:

| Page | Content |
|---|---|
| [Overview](https://wild8highlander.github.io/Trivortex/) | hero, badges, 60-second summary, headline results, abstract |
| [Vortex Model](https://wild8highlander.github.io/Trivortex/vortex-model.html) | bodies→vortices, the Hamiltonian, observables, literature context |
| [Theorem 3.1](https://wild8highlander.github.io/Trivortex/theorem-3-1.html) | statement, reference values, certified vs recorded, the Lagrange twin |
| [Code](https://wild8highlander.github.io/Trivortex/code.html) | the 22 sections, menu modes, report engine |
| [System Presets](https://wild8highlander.github.io/Trivortex/system-presets.html) | Sun–Earth–Moon, α Centauri, Pluto–Charon–Nix |
| [Verification](https://wild8highlander.github.io/Trivortex/verification.html) | V1–V4, criteria, roadmap, honesty notes |
| [Research Lab](https://wild8highlander.github.io/Trivortex/research.html) | the twelve studies with key results and direct links |
| [Publications](https://wild8highlander.github.io/Trivortex/publications.html) | the reading room: every PDF/DOCX rendition of the program |
| [Citation](https://wild8highlander.github.io/Trivortex/citation.html) | CFF, BibTeX, DOI |
| [License](https://wild8highlander.github.io/Trivortex/license.html) | IPL-RP-1.0, REUSE, contact |

Local preview: `python3 -m http.server -d docs/site 8080` →
<http://localhost:8080>. No build step, no toolchain — the pages are plain HTML
and the workflow publishes them verbatim (no Jekyll processing; a committed
`.nojekyll` keeps GitHub's generator out of the way).

---

## 15. Repository structure

```text
Trivortex/
├── README.md                        ← this file
├── LICENSE.md / LICENSE.ru.md / LICENSE.zh.md   ← proprietary license (EN + translations)
├── CITATION.cff · .zenodo.json      ← citation metadata (v1.0.0)
├── AUTHORS.md · NOTICE.md · CHANGELOG.md · RELEASING.md
├── CONTRIBUTING.md · SECURITY.md · CODE_OF_CONDUCT.md
├── Makefile · pyproject.toml · environment.yml · MANIFEST.json · REUSE.toml
│
├── code/                            ← ★ THE DOCUMENT
│   ├── trivortex_core.py            ← TRIVORTEX core (default, EN console)
│   ├── trivortex_core_ru.py         ← RU mirror, identical physics
│   ├── trivortex_core_en.py         ← EN mirror, identical physics
│   └── README.md                    ← deep documentation of the 22 sections
│
├── verification/                    ← ★ THE FRAMEWORK
│   ├── README.md                    ← ladder, roadmap, honesty notes
│   ├── trivortex/python/verify.py   ← V1–V4, JSON protocol, 3 presets
│   ├── tests/                       ← pytest guard (13 pins + 15 research tests)
│   ├── common/python/               ← shared verifier protocol
│   ├── docker/                      ← 7 pinned toolchains (Coq, Lean4, …)
│   ├── coq/ lean4/ rust/ isabelle/ agda/ cpp/ haskell/
│   │                                ← per-language landed ports (M1–M3)
│   └── Makefile · CODEOWNERS
│
├── research/                        ← ★ EXTENDED RESEARCH PROGRAM
│   ├── README.md                    ← program index, mapping tables
│   ├── _FORMAT_SPEC.md              ← binding full-format standard
│   ├── TRX-01-laser-radiation-pressure/   ← laser-dressed CR3BP
│   ├── TRX-02-three-wave-mixing/          ← Manley–Rowe, χ⁽²⁾ optics
│   ├── TRX-03-soliton-molecule/           ← fiber-laser soliton molecule
│   ├── TRX-04-photon-fluid/               ← three Kerr solitons
│   ├── TRX-05-optical-vortices/           ← optical vortices ≈ point vortices
│   ├── TRX-06-helium-three-body/          ← Coulomb three-body CTMC
│   ├── TRX-07-efimov/                     ← universal Efimov ladder
│   ├── TRX-08-ion-trap/                   ← laser-cooled ion crystal
│   ├── TRX-09-vortex-trio/                ← Kirchhoff–Chaplygin anchor
│   ├── TRX-10-kozai-lidov/                ← secular hierarchical triples
│   ├── TRX-11-gw-choreography/            ← figure-eight GW emitter
│   └── TRX-12-laser-light-sail/           ← laser highway to L4/L5
│       (each: README + code/*.py with --smoke/--figures
│        + figures/ (scheme SVG + 4 PNG @ 300 DPI)
│        + monograph/ (EN+RU sources × PDF+DOCX renditions)
│        + results/ + pack.py)
│
├── polyvortex/                      ← ★ THE N-VORTEX EXTENSION BENCH (mini-repo)
│   ├── README.md · README_RU.md · CHANGELOG.md · Makefile
│   ├── docs/monograph/              ← THE BIG MONOGRAPH: RU+EN × md+docx+pdf
│   ├── docs/monographs/             ← THEOREM EDITION: Theorems A, B, E;
│   │                                  Lemmas C, D — RU+EN × docx+pdf (20 files)
│   ├── figures/                     ← fig01–fig04 (300 dpi PNG, EN) + scheme SVG
│   │                                  generated by `make figures`, bound to protocols
│   ├── python/polyvortex/           ← model (Kirchhoff N-body) · ansatz (H1)
│   │                                  · classical · ladder · runner · figures
│   ├── tests/                       ← 26 tests, cross-pinned to the parent
│   └── results/protocols/           ← seven committed JSON protocols
│
├── cycloring/                       ← ★ THE GAMMA-PERIOD RING LABORATORY (mini-research)
│   ├── README.md · README_RU.md · CHANGELOG.md · Makefile
│   ├── docs/monograph/              ← THE BIG MONOGRAPH: RU+EN × md+docx+pdf
│   ├── docs/monographs/             ← THEOREM EDITION: Theorems 1–5 —
│   │                                  RU+EN × docx+pdf (20 files)
│   ├── figures/                     ← fig01–fig05 (300 dpi PNG, EN) + scheme SVG;
│   │                                  the RU mirror set in figures/ru/
│   ├── python/cycloring/            ← periods (mpmath) · chain · ring · dynamics
│   │                                  · ladder · runner · figures
│   ├── tests/                       ← 37 tests, self-contained
│   └── results/protocols/           ← seven committed JSON protocols
│
├── publications/                    ← ★ THE READING ROOM
│   ├── pdf/                         ← 28 vector A4 PDFs (RU and EN separate)
│   ├── docx/                        ← the same 28 documents as editable DOCX
│   ├── html/                        ← 14 editable HTML sources (1:1 with pdf/)
│   ├── src/                         ← markdown sources of core + compendium
│   ├── build/                       ← reproducible build system (make pdf-library)
│   └── README.md                    ← reading-room guide
│
├── docs/
│   ├── site/                        ← GitHub Pages site (deployed by deploy-docs.yml)
│   ├── animations/                  ← 4 orbital animations (GIF + MP4) + generator
│   └── assets/                      ← banner, title page, orbit showcase (SVG)
│
└── .github/                         ← CI (ci, lint, codeql, deploy-docs, docker,
                                       zenodo, …), issue/PR templates, badges,
                                       dependabot, release-drafter, funding
```

---

## 16. Quick start & reproduction

```bash
git clone https://github.com/wild8highlander/Trivortex.git
cd Trivortex
python -m pip install numpy scipy matplotlib mpmath

# ── the interactive document ─────────────────────────────
python3 code/trivortex_core_en.py        # menu: 15 modes, RU/EN mirrors available

# ── the independent verification ladder ──────────────────
python3 verification/trivortex/python/verify.py --preset quick     # ~0.5 s (CI)
python3 verification/trivortex/python/verify.py --preset default   # ~2 s
python3 verification/trivortex/python/verify.py --preset full      # ~35 s

# ── the pytest guard ─────────────────────────────────────
python -m pytest verification/tests/ -v                            # 63 tests
python -m pytest polyvortex/tests/ cycloring/tests/ -v             # 63 mini-repo tests
python -m pytest -v                                                # all 126 from the root

# ── the extended research program (12 executable studies) ─
python3 research/TRX-01-laser-radiation-pressure/code/trx01_laser_radiation_pressure.py
python3 research/TRX-09-vortex-trio/code/trx09_classical_anchor.py --smoke   # CI mode
python3 research/TRX-01-laser-radiation-pressure/code/trx01_laser_radiation_pressure.py --figures  # 300-DPI figures
# … or all twelve at once:
make research-smoke        # CI mode, seconds per study
make research-full         # full statistics + JSON protocols
make research-figures      # full runs + ultra-resolution figure sets

# ── animations and the reading room ────────────────────────
python3 docs/animations/make_animations.py            # 4 choreographies, GIF + MP4
make pdf-library                                      # 28 PDFs + 28 DOCX
#   → publications/pdf/TRX-01…12_<RU|EN>.pdf           (study monographs)
#   → publications/pdf/TRIVORTEX-Core-Monograph_<RU|EN>.pdf
#   → publications/pdf/TRIVORTEX-Research-Compendium_<RU|EN>.pdf

# ── everything at once (Make) ────────────────────────────
make verify            # ladder, default preset
make test              # pytest guard
make lint              # ruff over the Python sources
```

Requirements: Python ≥ 3.10, `numpy ≥ 1.24` (the core document additionally uses
`scipy`, `matplotlib`, `mpmath`; see `pyproject.toml` and `environment.yml`).
Every ladder run writes a JSON protocol with a full parameter snapshot — attach
it to any issue that reports a failing check and the failure is reproducible
without a single follow-up question.

---

## 17. The verification framework and milestones

The ladder was milestone **M0** of a staged plan that re-uses the repository's
seven pinned Docker toolchains. With v1.1 the plan is complete — all three
language milestones landed:

| Milestone | Meaning | Artifacts |
|---|---|---|
| **M0** ✅ | independent numerical ladder in one language | `verify.py` V1–V4 + the pytest guard + the interactive laboratory |
| **M1** ✅ | independent re-derivation: two proof assistants + a second floating-point language | `coq/Trivortex.v` (proven, zero axioms), `lean4/Trivortex.lean` (Mathlib), `rust/` (14/14 tests) — v1.1 |
| **M2** ✅ | two provers prove the same statement layer with disjoint axioms | `isabelle/Trivortex.thy` (HOL + optional SMT session), `agda/Trivortex.agda` (constructive C3 lattice) — v1.1 |
| **M3** ✅ | compiled benchmark ladder + exact-arithmetic residual split | `cpp/` (21 guards, ≈ 1.7e7 rhs/s), `haskell/` (Double + exact ℚ(√3) dual) — v1.1 |

Each language directory states its acceptance criteria **before** the artifacts
land, and every port must keep the certified-vs-recorded separation of
[§5](#5-verification-ladder-v1v4). Full details, tolerance-band rationale and
contribution rules: [verification/README.md](verification/README.md).

---

## 18. The research frontier — theorem pipeline and roadmap

With M0–M3 landed, the program widens from *verifying the document* to
*deriving new mathematics with the same machinery*. This section states how
a claim becomes a theorem here, queues the candidate theorems, and maps
the engineering tracks around them. The operative rules are the ones that
governed M1–M3: an acceptance criterion is registered before the artifacts
land, and a check becomes blocking only after it stays green.

### 18.1 The theorem pipeline — from observation to proof

Every new theorem passes five registered gates, in order:

1. **Observation.** The claim appears as a rung of the numerical ladder
   with a JSON protocol — a number, a band and a parameter snapshot.
   Nothing enters the pipeline from prose alone.
2. **Pre-registration.** The statement and its tolerance band are written
   into this file and `verification/README.md` *before* any proof attempt;
   the band may be tightened later, never loosened.
3. **Double formalization.** The statement is proven independently in Coq
   and Lean 4 (Mathlib) with `Print Assumptions` / `#print axioms` closed;
   Isabelle HOL may add a machine-checked band record and Agda a
   constructive variant.
4. **Exact certification.** Where the statement is algebraic, the Haskell
   ℚ(√3) track certifies it by computation — equality on exact rationals
   is decidable, so anchor identities hold *by evaluation*.
5. **Blocking CI + monograph.** The new rung joins the pytest guard and
   the ladder; the theorem gets a section in the core monograph and a
   bilingual publication rendition.

### 18.2 The theorem queue

| # | Candidate theorem | Statement (informal) | Proof strategy | Target |
|---|---|---|---|---|
| **T1** | Regular N-gon ring rotation | N equal vortices at the vertices of a regular N-gon of circumradius R rotate rigidly with ω_N = (N−1)Γ / (4πR²); for N = 3 this is exactly the Lagrange ω = 0.477464829275686 of §4 | the roots-of-unity identity Σ_k 1/(1−e^{2πik/N}) = (N−1)/2 turns the velocity sum into algebra; formalize the identity in Mathlib, then the rigid-rotation lemma | **M5** |
| **T2** | Chaplygin identity, field-theoretic | I = Γ holds along *every* solution, not only at the equilateral anchors — derived from the velocity field by the Stokes/Chaplygin argument | transport the vorticity 2-form along the Kirchhoff flow; the line-integral scaffold in Coq, the boundary argument over Mathlib | **M5** |
| **T3** | Spectral stability of the choreography | the Kirchhoff system linearized at the equilateral relative equilibrium has a purely imaginary spectrum (linear stability) | exact characteristic polynomial in Γ and a; a Routh–Hurwitz-type coefficient criterion — decidable, so Coq/Lean can close it; numerics give the eigenvalue picture | **M5–M6** |
| **T4** | A posteriori drift bound | for RK4 with step h over a period T, the invariant drift obeys \|H(T)−H(0)\| ≤ C·h⁴·T with an explicit C for the vortex Hamiltonian | backward-error analysis: the modified Hamiltonian is conserved to O(h⁴); formalize the scaling theorem, measure C on the ladder | **M6** |
| **T5** | Admissible region of the closed form | the algebraic equation behind Theorem 3.1 has a real root exactly when its discriminant is non-negative — characterize that region in (C_Ch, T) | the discriminant is a polynomial in C_Ch and T — a decidable statement; certify the boundary by ℚ(√3) evaluation | **M6** |
| **T6** | Full D3 symmetry lattice | the equilateral choreography is invariant under the whole dihedral group D3: both rotations and reflections preserve H, P, Q, I | Agda already proves rot³ ≡ id constructively; add the reflection generator and the group law; mirror it in Mathlib's `MulAction` | **M6** |

T1 doubles as ladder rung **V5**: once proven, the N-gon ring joins V1–V4
with its own protocol, tolerance band and port coverage — Python first,
then at least two ports, under the same pre-registration rule as before.

### 18.3 Deep-research tracks

| Track | What | Why it matters | Target |
|---|---|---|---|
| **R1** — 50-digit anchors | mpmath re-derivation of ω and the Chaplygin combination at 50 significant digits | separates float-ladder artifacts from mathematics; feeds T5's discriminant boundary | M5 |
| **R2** — third numeric twin | a Julia port of V1–V4 | a third independent floating-point implementation inside the §6 tolerance bands | M5 |
| **R3** — choreography atlas | catalogue of relative equilibria for N_v = 4…6 with symmetry labels | raw material for T1/T3 generalizations; nested polygons and collinear families as test cases | M6 |
| **R4** — stability map | a Γ_1/Γ_2/Γ_3 scan of T3's spectrum over a grid | turns the stability theorem into a picture; drives the V4 robustness extension | M6 |
| **R5** — statistical suite | spectral statistics on fixed seeds with protocol JSON | extends the honesty contract to distributional claims | M6+ |
| **R6** — WASM playground | the Kirchhoff dynamics compiled to WebAssembly in the browser | makes the choreography tangible; the same ladder code, zero re-derivation | M6+ |

### 18.4 Milestones M4–M6

- **M4 — hardening (v1.2).** No new science: flip the nine port jobs to
  blocking after three green days; bring the Isabelle SMT session online
  (Z3 in the pinned image); pre-warm the Lean Mathlib cache; generate the
  site table from the committed JSON protocols. The full track list lives
  in [§7.1 of the verification README](verification/README.md).
- **M5 — depth (v1.3).** The theorem queue opens: **T1** (together with
  the new V5 rung) and **T2** land double-formalized; tracks R1–R2 report
  their committed protocols.
- **M6 — widening (v2.0).** **T3–T6** formalized or certified; the atlas
  (R3) and the stability map (R4) published; the benchmark board pins the
  rust-vs-c++ throughput; the playground (R6) ships.

---

## 19. Citation, DOI & Zenodo

| Identifier | Value | Meaning |
|---|---|---|
| **Version DOI** | [`10.5281/zenodo.21825394`](https://doi.org/10.5281/zenodo.21825394) | this specific release (v1.0.0) |
| **Concept DOI** | [`10.5281/zenodo.21825393`](https://doi.org/10.5281/zenodo.21825393) | all versions of the study |

```bibtex
@misc{trivortex2026isaev,
  author       = {Isaev, Iskhak Khamzatovich},
  title        = {TRIVORTEX: The Three-Body (and N-Body) Problem in the
                  Vortex Model with the Chaplygin Topological Integral},
  year         = {2026},
  howpublished = {Zenodo},
  doi          = {10.5281/zenodo.21825394},
  orcid        = {0009-0003-7299-0701},
  url          = {https://github.com/wild8highlander/Trivortex}
}
```

The canonical metadata lives in [`CITATION.cff`](CITATION.cff) (GitHub's
*Cite this repository* button reads it directly) and
[`.zenodo.json`](.zenodo.json); new Zenodo versions are minted automatically on
GitHub releases by [`zenodo.yml`](.github/workflows/zenodo.yml). If you cite the
verification ladder rather than the document, name the preset you reproduced and
attach the JSON protocol — see the
[citation page](https://wild8highlander.github.io/Trivortex/citation.html).

---

## 20. Community & governance

- **Contributing** — [CONTRIBUTING.md](CONTRIBUTING.md): how to report results,
  propose ports, and the review contract (criteria first, code second; JSON
  protocol or it did not happen).
- **Issues & PRs** — structured templates under
  [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/) (bug report and feature
  request forms with the verification-protocol attachment field) and
  [PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md); the labeler
  routes changed files automatically.
- **Security** — [SECURITY.md](SECURITY.md): private disclosure channel and the
  supported versions table.
- **Code of conduct** — [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- **Releases** — [RELEASING.md](RELEASING.md): tag → release-drafter → Zenodo
  DOI chain. Current release: **v1.0.0**.
- **Funding** — [.github/FUNDING.yml](.github/FUNDING.yml).
- **Code owners** — [.github/CODEOWNERS](.github/CODEOWNERS) routes review
  requests for the core, verification and research trees.
- **Dependabot** — [.github/dependabot.yml](.github/dependabot.yml) keeps the
  Actions and pip ecosystems pinned and current.

---

## 21. GitHub features inventory

The repository uses the full standard GitHub toolchain; this table tells you
what each piece does and where to find it:

| Feature | File / place | Role |
|---|---|---|
| CI (syntax + ladder + pytest) | [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | every push: compile all Python, run V1–V4 (quick), 28-test guard |
| Lint (markdown + YAML + Python) | [`.github/workflows/lint.yml`](.github/workflows/lint.yml) | markdownlint, yamllint, ruff, black |
| CodeQL | [`.github/workflows/codeql.yml`](.github/workflows/codeql.yml) | static security analysis of the Python code |
| Dependency review | [`.github/workflows/dependency-review.yml`](.github/workflows/dependency-review.yml) | flags vulnerable dependencies on PRs |
| GitHub Pages deploy | [`.github/workflows/deploy-docs.yml`](.github/workflows/deploy-docs.yml) | publishes `docs/site/` verbatim on every change |
| Docker toolchains | [`.github/workflows/docker.yml`](.github/workflows/docker.yml) + [`verification/docker/`](verification/docker/) | 7 pinned verification images |
| Link checker | [`.github/workflows/link-checker.yml`](.github/workflows/link-checker.yml) | reports dead links in docs and site |
| Release drafter | [`.github/workflows/release-drafter.yml`](.github/workflows/release-drafter.yml) + [`.github/release-drafter.yml`](.github/release-drafter.yml) | assembles release notes from PRs |
| Stale bot | [`.github/workflows/stale.yml`](.github/workflows/stale.yml) | keeps the issue tracker alive |
| Labeler | [`.github/workflows/labeler.yml`](.github/workflows/labeler.yml) + [`.github/labeler.yml`](.github/labeler.yml) | auto-labels PRs by path |
| Scorecard | [`.github/workflows/scorecard.yml`](.github/workflows/scorecard.yml) | OpenSSF supply-chain score |
| Zenodo minting | [`.github/workflows/zenodo.yml`](.github/workflows/zenodo.yml) | pushes releases to the Zenodo DOI record |
| Issue templates | [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/) | bug report + feature request forms, with protocol-attachment guidance |
| PR template | [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md) | checklist: checks green, protocols attached |
| Code owners | [`.github/CODEOWNERS`](.github/CODEOWNERS) | automatic reviewer routing |
| Dependabot | [`.github/dependabot.yml`](.github/dependabot.yml) | Actions + pip version pinning |
| Dev container | [`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json) | one-click Codespaces environment (Python 3.12 + numpy/scipy/matplotlib/pytest) |
| Funding | [`.github/FUNDING.yml`](.github/FUNDING.yml) | sponsorship links |
| REUSE | [`REUSE.toml`](REUSE.toml) | machine-readable copyright/licensing metadata |

---

## 22. FAQ

**Q: Is this a claim about real planetary motion?**
No. TRIVORTEX is a model study: the vortex formulation is a Hamiltonian system
whose algebraic structure makes exact special solutions tractable and verifiable.
The astronomical presets are parameter scales and reality anchors, not ephemeris
simulations — and the verification ladder deliberately keeps them out of the
certified core.

**Q: What exactly does the ladder certify, and what does it only record?**
It certifies the equilateral choreography (2π/3 separations), the periodicity of
the closed form, the rigid Lagrange rotation at ω = 3Γ/(2πa²), and the
conservation of H, P, Q, I for equal and unequal circulations. It *records* the
endpoint drift of the gauge-dependent Chaplygin combination as a window-dependent
diagnostic — and gives it no pass/fail role. The separation is repeated in the
ladder output, the pytest guard, the site and the monographs.

**Q: Why are the tolerances so small (1e-10 … 1e-12)?**
Because the checks are algebraic identities of the model evaluated in float64.
Machine-precision residuals (~1e-14) are two orders below the registered bands,
so a genuine physics or integration bug cannot hide inside a tolerance.

**Q: Can I reproduce the numbers without installing anything?**
The fastest no-install glance is CI: every push runs the ladder and the full
pytest guard on GitHub's runners and archives the JSON protocol as an artifact.
Locally you need only Python ≥ 3.10, numpy and pytest for the ladder + guard;
scipy/matplotlib/mpmath for the interactive document.

**Q: Why are the monographs separate RU and EN files rather than one bilingual PDF?**
Because the two languages serve different readers: the Russian editions are the
author's working language, the English editions the citation language. Separate
files mean separate page numbering, separate metadata and no half-translated
volume — and each rendition rebuilds independently via `make pdf-library`.

**Q: How do I rebuild the PDF/DOCX library?**
`make pdf-library`. The build reads the committed markdown sources and figure
sets, renders MathML offline through pandoc, paints the navy-gold design through
headless Chromium, stamps page numbers and metadata, and writes both the study
folders and the reading-room mirrors. Nothing is recomputed — the documents
typeset committed results.

**Q: Something failed — what do I attach to the issue?**
The JSON protocol. The ladder and every study write one per run; CI archives it
as an artifact. An issue with a protocol is reproducible in one step; an issue
without one costs a follow-up question.

### Terminology quick reference

| Term | Meaning |
|---|---|
| **Core document** | `code/trivortex_core*.py` — the executable 22-section monograph |
| **Ladder** | `verify.py` — the independent V1–V4 checker (shares no code with the core) |
| **V1…V4** | the four registered checks: choreography, rigid rotation, integral conservation ×2 |
| **C_Ch** | the Chaplygin topological integral `r²(θ̇ − qA_θ)` — the model's control knob |
| **Theorem 3.1** | the closed-form rotating equilateral solution with radial modulation |
| **Study (TRX-nn)** | one of the twelve executable companion investigations |
| **Pack** | `research/TRX-*/pack.py` — the committed content pack a study is generated from |
| **Protocol** | the JSON file binding every printed number to a run (params + checks + series) |
| **Registered check** | a check whose target and tolerance were committed before the recorded run |
| **Diagnostic** | a recorded quantity explicitly given no pass/fail role (window-dependent) |
| **Rendition** | one language-format pair of a monograph (e.g. `_RU.docx`) |
| **Reading room** | `publications/` — the aggregated PDF/DOCX/HTML library |
| **Honesty notes** | the documented separation of certified vs recorded quantities |

---

## 23. License

The repository is released under its proprietary license:

> `LicenseRef-Proprietary-Wild8Highlander-1.0` (IPL-RP-1.0)

Full text: [LICENSE.md](LICENSE.md) · unofficial translations:
[LICENSE.ru.md](LICENSE.ru.md), [LICENSE.zh.md](LICENSE.zh.md). In one paragraph:
personal, research and educational use is permitted with attribution;
redistribution and commercial use require the author's written permission; the
document is provided as-is, without warranty of any kind.

---

<div align="center">

<img src="docs/assets/divider-gold.svg" width="35%" alt="divider"/>

**TRIVORTEX** · The Three-Body Problem in the Vortex Model · **Version 1.0.0**
[DOI 10.5281/zenodo.21825394](https://doi.org/10.5281/zenodo.21825394) ·
[ORCID 0009-0003-7299-0701](https://orcid.org/0009-0003-7299-0701) ·
[Documentation](https://wild8highlander.github.io/Trivortex) ·
MMXXVI

</div>
