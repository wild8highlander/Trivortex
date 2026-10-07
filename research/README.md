# TRIVORTEX Extended Research Program — TRX-01 … TRX-12

*Program index · TRIVORTEX Research Program · version 1.0.0*

Twelve companion studies that expand the TRIVORTEX repository from the
single vortex-model document (Theorem 3.1, Chaplygin integral) into a
full research program around the three-body problem and its optical,
quantum and celestial cousins. Every study is **executable**: each ships
a self-contained Python script (numpy/scipy only) that produces a
machine-readable JSON protocol (`results/trxNN_results.json`), exactly
like the main verification ladder. A study only counts as done when
**every quantitative acceptance check prints PASS** — and every check's
target and tolerance are committed *before* the recorded run.

Version **1.0.0** is the first public release of the program. Every
study carries the full publication format:

- a 26-section [`README.md`](TRX-01-laser-radiation-pressure/README.md)
  generated deterministically from the study's committed content pack;
- an executable script with `--smoke` (CI), full and `--figures` modes;
- a committed JSON protocol: checks (value / target / tolerance / unit /
  verdict / note), data series, parameter snapshot;
- a schematic SVG + four 300-DPI ultra-resolution figures (`figures/`);
- a bilingual monograph — **Russian and English as separate documents**,
  each in a typeset PDF and an editable DOCX —
  `monograph/monograph_{EN,RU}.{md,pdf,docx}`.

The binding format standard is [`_FORMAT_SPEC.md`](_FORMAT_SPEC.md).

## Table of contents

1. [Program map](#1-program-map)
2. [The twelve studies](#2-the-twelve-studies)
3. [Blocks in narrative](#3-blocks-in-narrative)
4. [Verification summary](#4-verification-summary)
5. [Full-format artifact map](#5-full-format-artifact-map)
6. [How to run](#6-how-to-run)
7. [How a study is built](#7-how-a-study-is-built)
8. [Program discipline](#8-program-discipline)

---

## 1. Program map

```text
                 TRIVORTEX (Theorem 3.1, C_Ch)
                            |
        +-------------------+---------------------+
        |            CLASSICAL ANCHOR              |
        |   TRX-09 Kirchhoff-Chaplygin three-vortex|
        +-------------------+---------------------+
        |                  |                  |
     LASER OPTICS       QUANTUM MATTER     CELESTIAL MECHANICS
  TRX-01 radiation-P    TRX-06 helium CTMC  TRX-10 Kozai-Lidov
  TRX-02 three-wave     TRX-07 Efimov       TRX-11 GW choreography
  TRX-03 soliton mol.   TRX-08 ion trap     TRX-12 laser light sail
  TRX-04 photon fluid   (TRX-05 opt.vortices — the optical twin of TRX-09)
  TRX-05 opt. vortices
  TRX-12 light sail
```

Read the map as three derivations from one anchor: the laser-optics block
re-expresses the equilateral geometry in photonic systems; the quantum-matter
block shows the three-body structure in trapped particles and universality
ladders; the celestial block returns to gravitation — secular dynamics and
gravitational waves.

## 2. The twelve studies

| ID | Directory | Domain | Key verified result | Checks | Full run |
|----|-----------|--------|---------------------|--------|----------|
| TRX-01 | [`TRX-01-laser-radiation-pressure`](TRX-01-laser-radiation-pressure/README.md) | Celestial mechanics | L1 = 0.8369151 (Earth–Moon); L4 shifts toward the radiating primary; Jacobi drift ≤ 1e-10 | 6/6 | 0.10 s |
| TRX-02 | [`TRX-02-three-wave-mixing`](TRX-02-three-wave-mixing/README.md) | Nonlinear optics | Manley–Rowe drift ≤ 4.5e-15; η(t) = tanh²(At) exact to 2.2e-16 | 7/7 | 0.6 s |
| TRX-03 | [`TRX-03-soliton-molecule`](TRX-03-soliton-molecule/README.md) | Fiber lasers | 3-pulse molecule at s\* = 0.2018927; breathing mode to 0.3% | 6/6 | 1.2 s |
| TRX-04 | [`TRX-04-photon-fluid`](TRX-04-photon-fluid/README.md) | Spatial solitons | Equilateral beam triangle ω to 1.4e-8; in-phase binary bound state | 9/9 | 9.4 s |
| TRX-05 | [`TRX-05-optical-vortices`](TRX-05-optical-vortices/README.md) | Singular optics | Vortex triangle ω = 3Γ/(2πa²) to 1e-8; winding number = 3; I ≡ a² | 5/5 | 4.8 s |
| TRX-06 | [`TRX-06-helium-three-body`](TRX-06-helium-three-body/README.md) | Quantum 3-body | CTMC: autoionization channel; escaper carries 7.3× the excess energy | 7/7 | 37.7 s |
| TRX-07 | [`TRX-07-efimov`](TRX-07-efimov/README.md) | Ultracold atoms | s₀ = 1.006238; ladder 515.5 / 515.0 vs exp(2π/s₀) = 515.03 | 6/6 | 5.8 s |
| TRX-08 | [`TRX-08-ion-trap`](TRX-08-ion-trap/README.md) | Trapped ions | Crystal side a = 3^(1/3) exact; modes {0, ω₀, √3ω₀, …} | 10/10 | 6.8 s |
| TRX-09 | [`TRX-09-vortex-trio`](TRX-09-vortex-trio/README.md) | Fluid dynamics | Rotation ω = 3/(2πa²) to 1e-8; I, H, P, Q conserved to 1e-12 | 8/8 | 0.5 s |
| TRX-10 | [`TRX-10-kozai-lidov`](TRX-10-kozai-lidov/README.md) | Celestial mechanics | e_max vs analytic 2e-3; period halves with m₃ (3%); direct 3-D 2.8% | 4/4 | 64.6 s |
| TRX-11 | [`TRX-11-gw-choreography`](TRX-11-gw-choreography/README.md) | Gravitational waves | Figure-eight T = 6.3259140; L = 0; Q(T/3)=Q(0); harmonic comb n = 6 | 7/7 | 8.2 s |
| TRX-12 | [`TRX-12-laser-light-sail`](TRX-12-laser-light-sail/README.md) | Laser propulsion | L4 hold ≤ 7.5e-7 (vs 4.1e-3 free); Jacobi pumped monotonically | 5/5 | 41.4 s |

**76 registered acceptance checks across the program — all PASS.**

## 3. Blocks in narrative

**Laser optics (01, 02, 03, 04, 05, 12).** Six studies translate the three-body
geometry into photonic systems: a laser-dressed CR3BP whose libration points
migrate under photon pressure; the exactly integrable three-wave system with
Manley–Rowe invariants; a soliton molecule with a breathing mode; a Kerr photon
fluid drawing a rotating Lagrange beam triangle; optical vortices that obey
Kirchhoff's equations with winding number three; and a light sail holding L4 on
a photon highway. Every one of these systems is, in principle, buildable on an
optical table — the laser is the program's experimental bridge.

**Quantum matter (06, 07, 08).** Helium's two electrons and nucleus form the
Coulomb three-body problem par excellence, and the CTMC study exposes the
autoionization channel and the Wannier overshoot of the escaper. Two fermions
in the −1/R² regime produce the Efimov ladder with its geometric ratio 515. And
three laser-cooled ions crystallize into exactly the Lagrange triangle of the
classical problem, with an analytic Hessian spectrum. The three-body structure
survives quantization.

**The classical anchor (09).** Three same-sign Kirchhoff vortices on an
equilateral triangle: rigid rotation at ω = 3Γ/(2πa²), conserved integrals
I, H, P, Q — the exact classical prototype of Theorem 3.1 and of the Chaplygin
integral. If any port or mirror disagrees with the core document, this study is
the arbiter.

**Celestial mechanics (10, 11).** The Kozai–Lidov mechanism exchanges
inclination and eccentricity in hierarchical triples; the study builds the
doubly-averaged quadrupole dynamics numerically and validates it against a
direct 3-D integration. The figure-eight choreography of Chenciner–Montgomery
is integrated at 1e-12 and decomposed into its gravitational-wave harmonics —
the computational source for the detector-side study.

## 4. Verification summary

| Study | Checks | Headline number | Tolerance | Status |
|---|---|---|---|---|
| TRX-01 | 6/6 | L1 = 0.8369151; Jacobi drift 8.9e-16 | 5e-6 / 1e-10 | **PASS** |
| TRX-02 | 7/7 | Manley–Rowe drift 4.5e-15 | 1e-12 | **PASS** |
| TRX-03 | 6/6 | spacing s\* = 0.2018927 | 1e-9 | **PASS** |
| TRX-04 | 9/9 | beam-triangle ω error 1.4e-8 | 1e-6 | **PASS** |
| TRX-05 | 5/5 | rotation ω error 1e-8 | 1e-6 | **PASS** |
| TRX-06 | 7/7 | escaper overshoot 7.3× | 10% | **PASS** |
| TRX-07 | 6/6 | ladder ratio 515.0–515.5 vs 515.03 | 0.5% | **PASS** |
| TRX-08 | 10/10 | crystal side exact to 1e-10 | 1e-10 | **PASS** |
| TRX-09 | 8/8 | rotation ω error 1e-8; drifts 1e-12 | 1e-6 / 1e-10 | **PASS** |
| TRX-10 | 4/4 | e_max bands; direct 3-D 2.8% | 2e-3 / 5% | **PASS** |
| TRX-11 | 7/7 | T = 6.3259140 to 1.2e-8 | 1e-7 | **PASS** |
| TRX-12 | 5/5 | L4 hold 7.5e-7 vs 4.1e-3 | 1e-5 | **PASS** |

The smoke mode of every study runs in CI on every push
([`ci.yml`](../.github/workflows/ci.yml)); the numbers above come from the
committed full-mode protocols.

## 5. Full-format artifact map

Each of the twelve study directories has the identical layout:

| Artifact | Content |
|----------|---------|
| `README.md` | 26-section study document (generated from `pack.py`, never hand-drifted) |
| `code/trxNN_*.py` | executable study: `--smoke` (CI), full mode, `--figures` |
| `pack.py` | the committed content pack — titles, physics, equations, tables, BibTeX |
| `figures/scheme_*.svg` | schematic diagram of the physical idea (navy-gold) |
| `figures/fig01..04_*.png` | four 300-DPI ultra-resolution panels |
| `results/trxNN_results.json` | machine-readable protocol: checks, series, meta |
| `results/trxNN_plot.svg` | quick-look vector plot |
| `monograph/monograph_EN.md` · `monograph_RU.md` | bilingual monograph sources |
| `monograph/monograph_EN.pdf` · `.docx` · `_RU.pdf` · `.docx` | the four renditions |
| `publications/pdf/TRX-*_<LANG>.pdf` · `publications/docx/…` | reading-room mirrors |

## 6. How to run

```bash
# one study, full mode (writes the JSON protocol)
python3 research/TRX-01-laser-radiation-pressure/code/trx01_laser_radiation_pressure.py

# one study, CI smoke mode (seconds)
python3 research/TRX-01-laser-radiation-pressure/code/trx01_laser_radiation_pressure.py --smoke

# one study, regenerate the 300-dpi figure set
python3 research/TRX-01-laser-radiation-pressure/code/trx01_laser_radiation_pressure.py --figures

# all twelve — Make targets
make research-smoke       # CI mode: every study, seconds each
make research-full        # full mode: statistics + JSON protocols
make research-figures     # full mode + ultra-resolution figures
```

Dependencies: Python ≥ 3.10 with `numpy` and `scipy` only. No network access,
no random state beyond fixed seeds — the same protocol is reproduced
byte-identically on any machine.

## 7. How a study is built

A study is *generated*, not hand-written: `pack.py` holds the committed content
(titles, essence, mission, physics, equations with LaTeX, preset and mapping
tables, method, analysis, discussion, conclusions, notation, glossary, appendix
parameters, BibTeX), and the README is rendered from it by the repository's
build tooling. The physics script, the JSON protocol and the figure set are
produced by the same deterministic code. This is why twelve studies can ship
with zero documentation drift: **the text, the tables and the numbers all come
from the same committed source.**

## 8. Program discipline

- **Registration before measurement.** Targets and tolerances are committed in
  the protocol before the recorded run; they are never tuned afterwards.
- **Every number bound to a run.** If a number appears in a README, a monograph
  or on the site, it is quoted from a committed JSON protocol.
- **Honest boundaries.** Certified quantities (with target + tolerance + verdict)
  are separated from recorded context; limitations are stated in each study's
  "Discussion and honest boundaries" section.
- **Smoke equals full in logic.** The CI smoke mode runs the same acceptance
  logic at seconds-scale settings — CI failing means the science failing, not
  the infrastructure.

## How to cite

Cite the repository through [`CITATION.cff`](../CITATION.cff)
(DOI 10.5281/zenodo.21825394, version 1.0.0). If you cite a single study, name
its monograph rendition and attach the JSON protocol of the run you reproduced.
Program author: Isaev Iskhak Khamzatovich
([ORCID 0009-0003-7299-0701](https://orcid.org/0009-0003-7299-0701)).
