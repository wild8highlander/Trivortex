<!-- markdownlint-disable-file MD041 -->
<div align="center">

<!-- ══════════════════════════════════════════════════════════════ -->
<!-- POLYVORTEX — monumental navy-and-gold header                   -->
<!-- ══════════════════════════════════════════════════════════════ -->
<img src="../docs/assets/banner-polyvortex.svg" width="100%" alt="POLYVORTEX — The N-Vortex Extension Bench"/>

### The N-Vortex Extension Bench

**A self-contained mini-repository inside the TRIVORTEX framework:**
the passage from the three-vortex Theorem 3.1 to an arbitrary number $N$
of equal point vortices — with its own codes, its own monograph, its own
verification ladder and its own committed protocols. The bench measures
exactly where the two layers of the model touch: the Kirchhoff numeric
dynamics (Layer K) and the topological closed form with its gauge law
(Layer G).

<img src="../docs/assets/divider-gold.svg" width="50%" alt="gold ornament divider"/>

**[Isaev Iskhak Khamzatovich](https://orcid.org/0009-0003-7299-0701)** · ORCID `0009-0003-7299-0701` · Independent Researcher

[🧭 Parent framework](../README.md) · [🔬 The research program](../research/README.md) · [🏛 Reading room](../publications/README.md) · [🌀 The ring laboratory](../cycloring/README.md)

<!-- ROW 1 — STATUS -->
[![TRIVORTEX CI](https://img.shields.io/github/actions/workflow/status/wild8highlander/Trivortex/ci.yml?branch=main&style=for-the-badge&logo=github&label=CI)](https://github.com/wild8highlander/Trivortex/actions/workflows/ci.yml)
[![Lint](https://img.shields.io/github/actions/workflow/status/wild8highlander/Trivortex/lint.yml?branch=main&style=for-the-badge&logo=github&label=Lint)](https://github.com/wild8highlander/Trivortex/actions/workflows/lint.yml)
[![pytest](https://img.shields.io/badge/pytest-26%20passed-2EA043?style=for-the-badge&logo=pytest&label=Guard)](tests/)
[![Ladder](https://img.shields.io/badge/ladder-W1%E2%80%93W7%20%E2%9C%93%207%2F7-2EA043?style=for-the-badge&label=W-ladder)](results/protocols/)

<!-- ROW 2 — IDENTITY -->
[![Version](https://img.shields.io/badge/version-1.1.0-1284BA?style=for-the-badge&label=Polyvortex)](CHANGELOG.md)
[![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=for-the-badge&logo=github)](../LICENSE.md)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](../pyproject.toml)
[![numpy](https://img.shields.io/badge/numpy-%E2%89%A51.24-013243?style=for-the-badge&logo=numpy)](../pyproject.toml)
[![mpmath](https://img.shields.io/badge/mpmath-registers-8A2BE2?style=for-the-badge&label=Precision)](python/polyvortex/ansatz.py)

<!-- ROW 3 — SCHOLARLY PAYLOAD -->
[![Monograph](https://img.shields.io/badge/monograph-6%20renditions%20RU%2BEN-9558B2?style=for-the-badge&label=Big%20book)](docs/monograph/)
[![Theorems](https://img.shields.io/badge/theorem%20edition-5%20%C3%97%202%20languages%20%C3%97%202%20formats-8A2BE2?style=for-the-badge&label=Theorems)](docs/monographs/)
[![Figures](https://img.shields.io/badge/figures-4%20%C3%97%20300%20dpi%20%2B%20scheme-1284BA?style=for-the-badge&label=Figures)](figures/)
[![Protocols](https://img.shields.io/badge/protocols-7%20committed%20JSON-2EA043?style=for-the-badge&label=Protocols)](results/protocols/)

</div>

---

## Table of contents

1. [What this is](#1-what-this-is)
2. [The mathematics — the three statements and the two lemmas](#2-the-mathematics--the-three-statements-and-the-two-lemmas)
3. [The W-ladder — seven registered stages](#3-the-w-ladder--seven-registered-stages)
4. [The stability scan and the admissibility boundary](#4-the-stability-scan-and-the-admissibility-boundary)
5. [The figure gallery](#5-the-figure-gallery)
6. [The publication stack](#6-the-publication-stack)
7. [Quickstart](#7-quickstart)
8. [Repository layout](#8-repository-layout)
9. [The module guide](#9-the-module-guide)
10. [The test guard — 26 tests](#10-the-test-guard--26-tests)
11. [Relation to the parent framework](#11-relation-to-the-parent-framework)
12. [The reproduction protocol](#12-the-reproduction-protocol)
13. [Honesty notes](#13-honesty-notes)
14. [FAQ](#14-faq)
15. [Roadmap of the mini-repository](#15-roadmap-of-the-mini-repository)

---

## 1. What this is

The parent framework anchors on **Theorem 3.1** — the closed-form
choreography of three vortices with the Chaplygin topological integral,
$\omega = (2\pi/T)\,e^{C_{Ch}/\pi}$ — and verifies the classical layer of
the model with the V1–V4 ladder. This mini-repository lifts the whole
picture to general $N$ and measures exactly where the two layers of the
model touch:

- **Layer K** — the Kirchhoff point-vortex dynamics (numerical): the
  right-hand side, an RK4 integrator, the invariants $H, P, Q, I$ and the
  stability Jacobian of the regular $N$-gon;
- **Layer G** — the topological closed form and its gauge law (analytic):
  the H1 ansatz $r_k(t) = \sqrt{C_{Ch}}\,(1+\varepsilon\cos\omega t)$ with
  the frequency fixed by the Chaplygin constant.

The scientific payload is a seven-stage ladder **W1–W7** and a publication
stack modelled one-to-one on the parent repository: the research monograph
([`docs/monograph/`](docs/monograph/) — Russian and English, each in
Markdown, DOCX and PDF) and the **theorem monograph edition**
([`docs/monographs/`](docs/monographs/) — five separate monographs, one
per theorem/lemma, each in Russian and English, DOCX and PDF). The bench
delivers three rigorous statements — Theorem B, Lemma C and Lemma D — plus
the classical registers generalized and reproduced numerically, all bound
to committed JSON protocols that CI re-derives on every push.

The bench never imports the parent at runtime; the parent is imported only
by tests, as the reference oracle — the same pinning discipline the parent
applies to its language ports.

---

## 2. The mathematics — the three statements and the two lemmas

### 2.1 Theorem A — the rigid rotation of the N-gon (the classical register)

$N$ equal vortices at the vertices of a regular $N$-gon of circumradius
$R$ rotate rigidly at

$\omega_N = \frac{\Gamma\,(N-1)}{4\pi R^2},$

a consequence of the roots-of-unity identity
$\sum_k 1/(1-\zeta_N^k) = (N-1)/2$. The ladder's stage W2 measures the
rotation of the freely integrated $N$-gon against this formula for
$N = 2..8$: the worst relative error across the scan is
$2.9\times10^{-12}$ and the worst shape deviation is $3.4\times10^{-12}$
— the formula holds at integration precision. For $N = 3$ this is exactly
the Lagrange triangle of the parent's Theorem 3.1, with
$\omega = 0.159154943091895$ at unit side radius.

### 2.2 Theorem B — the admissibility threshold $\pi\ln 2$

The closed form is non-degenerate (strictly positive radii at all times)
if and only if

$\boxed{\ C_{Ch} > \pi\ln 2 = 2.177586090303602\ldots\ }$

at the threshold the modulation amplitude equals $\varepsilon = 1$ exactly,
and below it the H1 ansatz demands a negative radius — the configuration
self-intersects through the origin. Stage W5 certifies the equivalence on
a 200-point grid of $C_{Ch}$ values (**zero equivalence violations**) and
pins the amplitude at the threshold to machine zero. The registered parent
default $C_{Ch} = 1$ lies **below** the threshold — a sharp, decidable
boundary delivered to the parent roadmap item **T5**: the structural
registers of Theorem 3.1 are blind to the degeneration, the polar
registers are not.

### 2.3 Lemma C — the kinematic obstruction

The induced radial velocity of a regular $N$-gon **vanishes identically**
(pair cancellation: every vortex feels equal inward and outward pulls
from its neighbours). Therefore a symmetrically pulsating polygon is not
a Layer-K orbit for any $\varepsilon \ne 0$: Hypothesis H1 reduces to the
classical rigid rotation $\omega_N$. Stage W6 pins the induced radial
velocity to $\sim 1.3\times10^{-16}$ — machine zero — and shows that the
phase-shifted variant of H1 fails even the shape register, linearly with
slope $\sqrt{3}/2$. The obstruction is what keeps the two layers
honestly separated: no unphysical "breathing polygon" claims.

### 2.4 Lemma D — the averaged-frequency bridge

Although a pulsating polygon is not a Layer-K orbit, its **cycle-averaged
kinematic rate** is exact: over one pulsation period the mean angular rate
of a ring riding the H1 shape is

$\langle\omega_{kin}\rangle = \omega_N\,(1-\varepsilon^2)^{-3/2},$

an integral identity certified to $2.9\times10^{-15}$. The gauge frequency
law and the kinematics therefore meet on the **D1 compatibility curve**:
the exact periods $T_{comp}(N, C_{Ch})$ at which the gauge law agrees with
the averaged kinematics. Stage W7 certifies the bridge to
$3.5\times10^{-15}$ and tabulates $T_{comp}$ — the design rule any future
pulsating-ring experiment must satisfy.

### 2.5 Theorem E — the Havelock stability threshold

The linearized Kirchhoff dynamics at the regular $N$-gon reproduces the
classical Havelock classification: **stable for $N \le 7$, unstable for
$N \ge 8$**. Stage W4 computes the full co-rotating spectrum for
$N = 2..8$: the stable cases sit on the numerically-zero noise floor
($\max\operatorname{Re}\lambda \le 7\times10^{-9}$), while $N = 8$ shows
$\max\operatorname{Re}\lambda = +0.4502$ — a three-order-of-magnitude
margin, visible in [`fig03`](figures/fig03_stability_scan.png). This is
the prototype of the parent roadmap item **T3** (spectral stability of
the choreography).

---

## 3. The W-ladder — seven registered stages

Every stage carries a registered tolerance committed **before** the
recorded run, and every run writes a deterministic JSON protocol into
[`results/protocols/`](results/protocols/) with a full parameter
snapshot. The committed protocols of the default preset:

| stage | register | registered tolerance | recorded result | status |
|-------|----------|----------------------|-----------------|:------:|
| **W1** | the Theorem 3.1 anchor at $N=3$: separation, periodicity, pinned literals | $\le 10^{-12}$ | $6.9\times10^{-14}$ / $9.4\times10^{-14}$ | PASS |
| **W2** | the rigid rotation $\omega_N = \Gamma(N-1)/(4\pi R^2)$, $N = 2..8$ | $\le 10^{-9}$ rel. | $2.9\times10^{-12}$ (worst) | PASS |
| **W3** | the invariants $H, P, Q, I$ along the $N$-gon orbits | $\le 10^{-10}$ drift | $4.3\times10^{-14}$ (worst) | PASS |
| **W4** | the spectral stability: Havelock $N \le 7$ / $N \ge 8$ | classifier $10^{-7}$ | $+7\times10^{-9}$ … $+0.4502$ | PASS |
| **W5** | the admissibility: $\varepsilon < 1 \iff C_{Ch} > \pi\ln 2$ | 0 violations / 200 pts | 0 violations | PASS |
| **W6** | the kinematic obstruction (Lemma C + the H1 shape register) | $\le 10^{-12}$ | $1.3\times10^{-16}$ | PASS |
| **W7** | the averaged-frequency bridge + the $T_{comp}$ table (D1) | $\le 10^{-12}$ rel. | $3.5\times10^{-15}$ | PASS |

Stages W1–W3 generalize the parent registers V1–V3; stages W4–W7 are the
new research content. Every protocol is a deterministic JSON file bound to
a run; the test suite re-derives the preset-independent numbers and pins
the rest to the committed protocols.

---

## 4. The stability scan and the admissibility boundary

Two scans organize the bench's numeric payload. The **stability scan**
(stage W4) walks $N = 2..8$, linearizes the Kirchhoff flow at the frozen
polygon, and classifies each level by the sign of
$\max\operatorname{Re}\lambda$:

| $N$ | $\max\operatorname{Re}\lambda$ | classification |
|----:|-------------------------------|-----------------|
| 2 | $6.9\times10^{-10}$ | stable (Havelock) |
| 3 | $1.7\times10^{-17}$ | stable (Havelock) |
| 4 | $3.8\times10^{-9}$ | stable (Havelock) |
| 5–6 | $\le 0$ (noise floor) | stable (Havelock) |
| 7 | $7.0\times10^{-9}$ | stable — the last stable level |
| 8 | $\mathbf{+0.4502}$ | **unstable** — the Havelock threshold |

The **admissibility scan** (stage W5) walks a 200-point grid of $C_{Ch}$
against the exact threshold: the equivalence
$\varepsilon < 1 \iff C_{Ch} > \pi\ln 2$ holds at every grid point, the
minimum-radius register matches its closed form to $1.9\times10^{-7}$
over a 4096-point polar grid, and the amplitude at the threshold is
machine-zero. Together the two scans draw the bench's central picture:
where the ring is dynamically stable, and where the closed form is
geometrically admissible — two independent boundaries, both certified.

<div align="center">
<img src="figures/fig03_stability_scan.png" width="86%" alt="The Havelock stability scan N=2..8 and the threshold spectra"/>
</div>

---

## 5. The figure gallery

All figures are generated at **300 dpi** by the protocol-bound factory
[`python/polyvortex/figures.py`](python/polyvortex/figures.py) and are
regenerable with `make figures`. Every figure embeds its protocol
residuals in the title — the pictures quote the same numbers the
protocols certify.

| figure | stages | what it shows |
|--------|:------:|----------------|
| [`fig01_two_layers.png`](figures/fig01_two_layers.png) | — | Layer G against Layer K: the limaçon riders of the H1 ansatz ($N=3$) and the rigid $N$-gon ring ($N=7$) |
| [`fig02_ring_rotation.png`](figures/fig02_ring_rotation.png) | W2 | $\omega_N$ analytic against measured (RK4, two rotations) with the relative error band |
| [`fig03_stability_scan.png`](figures/fig03_stability_scan.png) | W4 | the Havelock scan $\max\operatorname{Re}\lambda(N)$ and the threshold spectra pair |
| [`fig04_admissibility_bridge.png`](figures/fig04_admissibility_bridge.png) | W5, W7 | the $\pi\ln 2$ admissibility boundary and the D1 compatibility periods $T_{comp}$ |
| [`scheme_polyvortex.svg`](figures/scheme_polyvortex.svg) | — | the architecture: Layer K + Layer G → the W-ladder → committed protocols |

<div align="center">

**The two layers side by side**

<img src="figures/fig01_two_layers.png" width="86%" alt="Layer G limacon riders and Layer K rigid ring"/>

**The rigid rotation, formula against measurement (W2)**

<img src="figures/fig02_ring_rotation.png" width="86%" alt="Rigid rotation of the N-gon: analytic vs measured"/>

**The admissibility boundary and the D1 bridge (W5, W7)**

<img src="figures/fig04_admissibility_bridge.png" width="86%" alt="The pi ln 2 boundary and the compatibility periods"/>

</div>

---

## 6. The publication stack

| item | languages | formats | where |
|------|-----------|---------|-------|
| the big research monograph (W-ladder science) | RU, EN | `.md`, `.docx`, `.pdf` | [`docs/monograph/`](docs/monograph/) |
| Theorem A — the rigid rotation of the N-gon | RU, EN | `.docx`, `.pdf` | [`docs/monographs/`](docs/monographs/) |
| Theorem B — the admissibility threshold $\pi\ln 2$ | RU, EN | `.docx`, `.pdf` | [`docs/monographs/`](docs/monographs/) |
| Theorem E — the Havelock stability threshold | RU, EN | `.docx`, `.pdf` | [`docs/monographs/`](docs/monographs/) |
| Lemma C — the kinematic obstruction | RU, EN | `.docx`, `.pdf` | [`docs/monographs/`](docs/monographs/) |
| Lemma D — the averaged-frequency bridge + D1 | RU, EN | `.docx`, `.pdf` | [`docs/monographs/`](docs/monographs/) |
| figures (fig01–fig04 + the scheme) | EN | `.png` 300 dpi, `.svg` | [`figures/`](figures/) |

Every document embeds the figures and quotes only protocol-bound numbers;
the DOCX files carry proper field TOCs, the PDFs are the LibreOffice
render of the very same DOCX (the parent repository's pipeline).

---

## 7. Quickstart

Requirements: Python ≥ 3.10 with `numpy` (+ `mpmath`, `matplotlib`,
`pytest` for the optional registers). From the repository root:

```bash
cd polyvortex

make ladder   # run W1..W7 (default preset), refresh the JSON protocols
make quick    # 1.3 s smoke of the whole ladder
make full     # long integration (full preset)
make figures  # regenerate figures/ (300 dpi PNG + the scheme SVG)
make test     # the pytest guard (26 tests, ~2 s)
make lint     # black --check + ruff + mypy (scoped to this mini-repo)
```

The runner can also address a single stage:

```bash
PYTHONPATH=python python3 python/polyvortex/runner.py --stage W4 --preset default
```

The presets trade integration effort for wall time:

| preset | what it does | typical wall | used by |
|--------|--------------|--------------|---------|
| `quick` | coarse smoke of all seven stages | ≈ 1.3 s | CI, iteration |
| `default` | the committed protocol preset | ≈ 7 s | protocols, tests |
| `full` | long integration, tight tolerances | ≈ 30 s | release validation |

The Python API is one import away:

```python
import sys; sys.path.insert(0, "python")

from polyvortex import ansatz, classical, model

# the admissibility threshold, exact
from mpmath import pi, log, mp
mp.dps = 30
print(pi * log(2))  # 2.17758609030360213050...

# the rigid rotation rate of the N-gon, analytic
print(classical.ring_rotation(7))  # Gamma*(N-1)/(4 pi R^2) at unit Gamma, R

# the Layer-K invariants along an integrated orbit
print(model.invariants.__doc__)
```

---

## 8. Repository layout

```text
polyvortex/
├── README.md            ← this file
├── README_RU.md         ← the Russian mirror
├── CHANGELOG.md         ← the mini-repo changelog
├── Makefile             ← ladder / quick / full / figures / test / lint
├── docs/
│   ├── monograph/       ← THE BIG MONOGRAPH: monograph_RU|EN.{md,docx,pdf}
│   └── monographs/      ← THEOREM EDITION: Theorems A, B, E; Lemmas C, D
│                          (POLYVORTEX-<item>_{RU,EN}.docx / .pdf, 20 files)
├── figures/             ← fig01–fig04 (300 dpi PNG) + scheme_polyvortex.svg
│                          generated by `make figures`, bound to protocols
├── python/polyvortex/
│   ├── model.py         ← Layer K: Kirchhoff RHS, RK4, invariants, Jacobian
│   ├── ansatz.py        ← Layer G: the H1 closed form, threshold, diagnostic
│   ├── classical.py     ← the N-gon relative equilibria, chords, unwrap
│   ├── ladder.py        ← the W1..W7 checks
│   ├── runner.py        ← the JSON protocol CLI
│   └── figures.py       ← the figure factory (300 dpi, protocol-bound)
├── tests/               ← 26 tests incl. cross-validation vs the parent ladder
└── results/protocols/   ← the committed JSON protocols (default preset)
```

Each subfolder carries its own README with the local API, file index and
regeneration instructions — start with
[`python/polyvortex/`](python/polyvortex/) for the module guide.

---

## 9. The module guide

Seven modules, ≈ 1.8 kLOC, zero dependencies beyond `numpy` (+ `mpmath`
in the analytic registers):

| module | lines | role | key entry points |
|--------|------:|------|------------------|
| [`model.py`](python/polyvortex/model.py) | 176 | Layer K: the Kirchhoff dynamics | `rhs`, `rk4_step`, `invariants`, `jacobian` |
| [`ansatz.py`](python/polyvortex/ansatz.py) | 151 | Layer G: the H1 closed form | `h1_radius`, `gauge_frequency`, `amplitude`, `admissibility_threshold` |
| [`classical.py`](python/polyvortex/classical.py) | 90 | the N-gon relative equilibria | `ring_rotation`, `polygon_positions`, `chord_pairs`, `unwrap` |
| [`ladder.py`](python/polyvortex/ladder.py) | 540 | the W1–W7 registered checks | `run_stage`, `run_ladder` |
| [`runner.py`](python/polyvortex/runner.py) | 125 | the JSON protocol CLI | `--stage`, `--preset` |
| [`figures.py`](python/polyvortex/figures.py) | 533 | the figure factory | `main` |
| [`__init__.py`](python/polyvortex/__init__.py) | 19 | the package surface | re-exports the public API |

The dependency direction is strict: `classical → model/ansatz → ladder →
runner/figures`. Nothing in the package imports the parent framework at
runtime — the parent appears only in tests, as the reference oracle (see
[§11](#11-relation-to-the-parent-framework)).

---

## 10. The test guard — 26 tests

The pytest guard re-derives every preset-independent number of the ladder
and cross-pins the anchor values against the parent framework's own
ladder:

| suite | tests | what they guard |
|-------|------:|-----------------|
| `test_classical.py` | 5 | $\omega_N$ for $N = 2..8$, the chord pair-cancellation, the unwrap register |
| `test_ansatz.py` | 9 | the H1 radius, the $\pi\ln 2$ threshold, the amplitude-at-threshold identity |
| `test_model.py` | 6 | the Kirchhoff RHS, the invariants, the Jacobian spectrum at $N = 3$ |
| `test_ladder.py` | 6 | the ladder rungs themselves + the parent-ladder cross-pins + protocol shape |

Run them with `make test` or `python3 -m pytest tests/ -v`. The guard
needs only `numpy` and `pytest` — the same dependency floor the CI uses,
so a green guard on your laptop is the same green guard CI sees.

---

## 11. Relation to the parent framework

| parent register | this mini-repo | note |
|-----------------|----------------|------|
| V1 (Theorem 3.1 registers) | W1 | bit-for-bit pinned literals at $N = 3$ |
| V2 (Lagrange rigid rotation) | W2 | generalized to $\omega_N$, $N = 2..8$ |
| V3/V4 (integral conservation) | W3 | $N$-generic |
| roadmap **T1** (N-gon ring) | Theorem A + W2 | numerical shadow of the roots-of-unity identity |
| roadmap **T3** (spectral stability) | W4 | the prototype of the spectrum computation |
| roadmap **T5** (admissible region) | Theorem B + W5 | the exact boundary $\pi\ln 2$ |
| roadmap §18 theorem queue | monograph §8 | the TB1→TW5 formalization queue |

The mini-repository never imports the parent at runtime; the parent is
imported only by tests, as the reference oracle — the same pinning
discipline the parent applies to its language ports.

---

## 12. The reproduction protocol

To reproduce every number in this README from scratch:

1. **clone and enter** — `git clone https://github.com/wild8highlander/Trivortex.git && cd Trivortex/polyvortex`;
2. **run the ladder** — `make ladder`; the seven JSON protocols in
   `results/protocols/` are regenerated with identical numbers
   (deterministic integration, fixed grids);
3. **regenerate the figures** — `make figures`; the factory reads the
   committed protocols and rebuilds the figure set;
4. **run the guard** — `make test`; 26 tests re-derive the
   preset-independent registers and cross-pin the anchor against the
   parent ladder;
5. **compare** — every number quoted in [§3](#3-the-w-ladder--seven-registered-stages)
   and [§4](#4-the-stability-scan-and-the-admissibility-boundary) must
   match your run to the printed precision; a mismatch is a bug — open an
   issue with your protocol JSON attached.

The whole loop takes under ten seconds on a laptop; the ladder is pure
float64 RK4 with the spectral registers in numpy.

---

## 13. Honesty notes

- Hypothesis H1 is **not** a Kirchhoff solution for $\varepsilon \ne 0$
  (Lemma C); the gauge frequency law and the kinematics agree only along
  the D1 curve. The monograph keeps the two layers separated by design.
- The parent's registered default $(C_{Ch}, T) = (1, 2\pi)$ lies below the
  admissibility threshold; the structural registers are blind to it, the
  polar registers are not. See monograph Sections 5 and 10.
- Stability is spectral (linear), not nonlinear; nothing beyond the
  linearized classification is claimed.
- The W1 anchor's Section-6 drift value (≈ 15.0) is recorded as a
  **window-dependent diagnostic** exactly as in the parent — it has no
  pass/fail role and is not counted among the certified registers.

---

## 14. FAQ

**Q: What exactly is "the H1 ansatz"?**
The hypothesis that the breathing ring of the parent's closed form —
$r_k(t) = \sqrt{C_{Ch}}\,(1+\varepsilon\cos\omega t)$, phases $2\pi k/N$ —
might generalize from $N = 3$ to arbitrary $N$. Theorem B says when the
shape is geometrically admissible ($C_{Ch} > \pi\ln 2$), Lemma C says the
symmetric pulsation is dynamically obstructed, and Lemma D says the
averaged kinematics still meets the gauge law on the D1 curve. The three
statements together are the honest fate of H1: admissible, obstructed,
bridgeable.

**Q: Why is $C_{Ch} = 1$ below the threshold, and does it matter?**
$\pi\ln 2 \approx 2.1776 > 1$, so the parent's registered default makes H1
demand a negative radius — the closed form "breathes through the origin".
The parent's structural registers (choreography, periodicity) never touch
the polar shape, so they are blind to this; the polar registers record it.
Theorem B turns that observation into a decidable boundary.

**Q: Which N should I scan first?**
$N = 7$ and $N = 8$: the last stable and first unstable levels of the
Havelock classification. [`fig03`](figures/fig03_stability_scan.png) is
the single most information-dense picture of the bench — three orders of
magnitude between the noise floor and the unstable eigenvalue.

**Q: How does the cross-validation against the parent work?**
The test suite imports the parent's ladder protocol
(`verification/outputs/` or the committed reference values) and asserts
that the bench's W1 anchor reproduces the same $\omega$, $\varepsilon$ and
residual literals bit-for-bit. The two ladders share no code — only the
committed numbers bind them, exactly like a language port.

**Q: Can I add unequal circulations?**
That is roadmap item **P4**: a deformed ring with $\{\Gamma_k\}$ unequal
is a relative equilibrium only under specific conditions. The `model.py`
layer already accepts a circulation vector; the ladder does not yet
register a claim about it. Nothing in the current protocols covers
unequal $\Gamma$ — see [§13](#13-honesty-notes) and the monograph §8.

---

## 15. Roadmap of the mini-repository

1. **P1 — formalize TB1** (Theorem B) in Coq and Lean 4: the cheapest
   decidable statement; the numeric protocol is the oracle.
2. **P2 — TB2/TW4** (Lemma C + Theorem A): the roots-of-unity identity in
   Mathlib; the chord pair-cancellation in Coq.
3. **P3 — TB3** (Lemma D): the differentiated Poisson integral, or an
   interval-arithmetic certificate on $[-0.9, 0.9]$.
4. **P4 — widening**: unequal circulations $\{\Gamma_k\}$ (when does a
   regular ring remain a relative equilibrium?), rings of rings, and the
   stability map over the $\Gamma$-ratio grid (feeds parent R4).

---

<div align="center">

<img src="../docs/assets/divider-gold.svg" width="35%" alt="divider"/>

**POLYVORTEX** · The N-Vortex Extension Bench · **Version 1.1.0** ·
part of the [TRIVORTEX](../README.md) research program ·
[DOI 10.5281/zenodo.21825394](https://doi.org/10.5281/zenodo.21825394) ·
[ORCID 0009-0003-7299-0701](https://orcid.org/0009-0003-7299-0701) ·
[The Russian mirror](README_RU.md) · MMXXVI

</div>
