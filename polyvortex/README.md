# POLYVORTEX — the N-vortex extension bench

*A self-contained mini-repository inside the TRIVORTEX framework:
the passage from the three-vortex Theorem 3.1 to an arbitrary number
$N$ of equal point vortices — with its own codes, its own monograph,
its own verification ladder and its own protocols.*

Version 1.1.0 · License: LicenseRef-Proprietary-Wild8Highlander-1.0
(see LICENSE.md at the repository root) · Python 3.10+ · numpy

---

## What this is

The parent framework anchors on **Theorem 3.1** — the closed-form
choreography of three vortices with the Chaplygin topological integral
$\omega = (2\pi/T)e^{C_{Ch}/\pi}$ — and verifies the classical layer of the
model with the V1–V4 ladder. This mini-repository lifts the whole picture to
general $N$ and measures exactly where the two layers of the model touch:

- **Layer K** — the Kirchhoff point-vortex dynamics (numerical);
- **Layer G** — the topological closed form and its gauge law (analytic).

The scientific payload is a seven-stage ladder **W1–W7** and a publication
stack modelled one-to-one on the parent repository: the research monograph
([docs/monograph/](docs/monograph/) — Russian and English, each in Markdown,
DOCX and PDF) and the **theorem monograph edition**
([docs/monographs/](docs/monographs/) — five separate monographs, one per
theorem/lemma, each in Russian and English, DOCX and PDF). Three rigorous
statements:

1. **Theorem B (admissibility).** The closed form is non-degenerate
   (strictly positive radii at all times) iff
   $C_{Ch} > \pi\ln 2 = 2.177586090303602\ldots$; at the threshold the
   modulation amplitude equals $\varepsilon = 1$ exactly. The registered
   parent default $C_{Ch} = 1$ lies below it — a sharp, decidable boundary
   delivered to the parent roadmap item **T5**.
2. **Lemma C (kinematic obstruction).** The induced radial velocity of a
   regular $N$-gon vanishes identically (pair cancellation), so a
   symmetrically pulsating polygon is not a Layer-K orbit for any
   $\varepsilon \ne 0$: Hypothesis H1 reduces to the classical rigid
   rotation $\omega_N = \Gamma(N-1)/(4\pi R^2)$. The phase-shifted variant
   of H1 fails even the shape register, linearly with slope $\sqrt{3}/2$.
3. **Lemma D (averaged-frequency bridge).** The cycle-averaged kinematic
   rate of a pulsating ring is $\omega_N (1 - \varepsilon^2)^{-3/2}$ — an
   integral identity certified to $3 \cdot 10^{-15}$ — which yields the
   compatibility curve **D1**: the exact periods $T_{comp}(N, C_{Ch})$ at
   which the gauge frequency law meets the averaged kinematics.

Plus the classical registers, generalized and reproduced numerically:
the rigid rotation measured to $2.9 \cdot 10^{-12}$ for $N = 2..8$,
the invariants $H, P, Q, I$ conserved to $4.2 \cdot 10^{-14}$, and the
**Havelock stability threshold** (stable $N \le 7$, unstable $N \ge 8$)
reproduced spectrally with a three-order margin ($N = 8$:
$\max\operatorname{Re}\lambda = +0.450$).

## The W-ladder

| stage | register | status | protocol |
|-------|----------|:------:|----------|
| W1 | Theorem 3.1 anchor at $N = 3$: separation, periodicity, pinned literals | PASS | `W1_anchor_default.json` |
| W2 | Rigid rotation of the $N$-gon, $N = 2..8$: $\omega_N$ formula + shape | PASS | `W2_ring_rotation_default.json` |
| W3 | Invariants $H, P, Q, I$ along the $N$-gon orbits | PASS | `W3_invariants_default.json` |
| W4 | Spectral stability: the Havelock threshold $N \le 7$ / $N \ge 8$ | PASS | `W4_stability_default.json` |
| W5 | Admissibility: $\varepsilon < 1 \iff C_{Ch} > \pi \ln 2$ | PASS | `W5_admissibility_default.json` |
| W6 | The kinematic obstruction (Lemma C + the H1 shape register) | PASS | `W6_obstruction_default.json` |
| W7 | The averaged-frequency bridge + the $T_{comp}$ table (D1) | PASS | `W7_bridge_default.json` |

Stages W1–W3 generalize the parent registers V1–V3; stages W4–W7 are the
new research content. Every protocol is a deterministic JSON file bound to
a run; the test suite re-derives the preset-independent numbers.

## The publication stack

| item | languages | formats |
|------|-----------|---------|
| the big research monograph (W-ladder science) | RU, EN | `.md`, `.docx`, `.pdf` |
| Theorem A — rigid rotation of the N-gon | RU, EN | `.docx`, `.pdf` |
| Theorem B — the admissibility threshold `pi*ln 2` | RU, EN | `.docx`, `.pdf` |
| Theorem E — the Havelock stability threshold | RU, EN | `.docx`, `.pdf` |
| Lemma C — the kinematic obstruction | RU, EN | `.docx`, `.pdf` |
| Lemma D — the averaged-frequency bridge + D1 | RU, EN | `.docx`, `.pdf` |
| figures (fig01–fig04 + the scheme) | — | `.png` 300 dpi, `.svg` |

Every document embeds the figures and quotes only protocol-bound numbers;
the DOCX files carry proper field TOCs, the PDFs are the LibreOffice render
of the very same DOCX (the parent repository's pipeline).

## Quickstart

```bash
# from the repository root
cd polyvortex

make ladder   # run W1..W7 (default preset), refresh the JSON protocols
make quick    # 1.3 s smoke of the whole ladder
make figures  # regenerate figures/ (300 dpi PNG + the scheme SVG)
make test     # the pytest guard (26 tests, ~2 s)
make lint     # black --check + ruff + mypy (scoped to this mini-repo)
```

The runner can also address a single stage:

```bash
python3 python/polyvortex/runner.py --stage W4 --preset default
```

## Layout

```text
polyvortex/
├── README.md            ← this file
├── README_RU.md         ← the Russian mirror
├── CHANGELOG.md         ← the mini-repo changelog
├── Makefile             ← ladder / quick / full / figures / test / lint
├── docs/
│   ├── monograph/       ← THE BIG MONOGRAPH: monograph_RU|EN.{md,docx,pdf}
│   ├── monographs/      ← THEOREM EDITION: Theorems A, B, E; Lemmas C, D
│   │                      (POLYVORTEX-<item>_{RU,EN}.docx / .pdf, 20 files)
│   └── ...
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

## Relation to the parent framework

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

## Honesty notes

- Hypothesis H1 is **not** a Kirchhoff solution for $\varepsilon \ne 0$
  (Lemma C); the gauge frequency law and the kinematics agree only along
  the D1 curve. The monograph keeps the two layers separated by design.
- The parent's registered default $(C_{Ch}, T) = (1, 2\pi)$ lies below the
  admissibility threshold; the structural registers are blind to it, the
  polar registers are not. See monograph Sections 5 and 10.
- Stability is spectral (linear), not nonlinear; nothing beyond the
  linearized classification is claimed.

## Roadmap of the mini-repository

1. **P1 — formalize TB1** (Theorem B) in Coq and Lean 4: the cheapest
   decidable statement; the numeric protocol is the oracle.
2. **P2 — TB2/TW4** (Lemma C + Theorem A): the roots-of-unity identity in
   Mathlib; the chord pair-cancellation in Coq.
3. **P3 — TB3** (Lemma D): the differentiated Poisson integral, or an
   interval-arithmetic certificate on $[-0.9, 0.9]$.
4. **P4 — widening**: unequal circulations $\{\Gamma_k\}$ (when does a
   regular ring remain a relative equilibrium?), rings of rings, and the
   stability map over the $\Gamma$-ratio grid (feeds parent R4).
