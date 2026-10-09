# Changelog

All notable changes to the PLANETVORTEX mini-repository are documented
in this file. The format follows Keep a Changelog; this file is
excluded from the markdownlint contract of the parent repository.

## [2.0.0] — 2026-10-09

### Added

- The spatial V-register (`python/planetvortex/vregister.py` with the
  two engines `spatial.py` and `klein.py`) — the roadmap items V1 and
  V2 as two committed stages:
  - **V1** the spatial inclined registers: the SO(3) tilt algebra of
    the 11-body inclination register (Sun + 8 planets + Ceres + Eris,
    JPL J2000 inclinations and nodes), the exact arc registers
    lambda = R_bar * i, the 55-pair mutual-inclination matrix, and the
    full 3D Newtonian integration of the real J2000 sky — E and the
    vector L conserved, the osculating (a, e, i) inside the secular
    bands, Kepler III from the perihelion passages, the z-ladder.
  - **V2** the closed gravifigure: the Klein map {7,3}_8 as the coset
    geometry of the certified PSL(2,7) — V = 56, E = 84, F = 24, Euler
    −4, 3-regular, 7-gonal, connected, orientable; the PGL(2,7) flag
    certificate (336 flags, simply transitive); the chamber patch in
    the Poincare disk grows to exactly 336 chambers = 24 heptagons
    with 168 sides pairing onto 84 map edges; the witness involution
    pairs the 24 faces into 12 antipodal registers; the 12-body
    gravimetric angle register alpha_i = 2pi/3 − sigma*s_i with
    sum(s_i) = 0 closes the curvature budget exactly:
    sum(alpha_i) = 8pi = 2pi(2g−2) — the Euler characteristic absorbs
    the mass ladder.
- The multi-language kernel: `c/gravikernel.c` (the F_7 group
  arithmetic and the coset geometry in C, compiled by `c/Makefile`)
  and `js/verifier.html` (the self-contained browser verifier of the
  same registers); `tools/crosslang_diff.py` writes
  `results/crosslang/crosslang_report.json` — three languages, one
  truth.
- The self-check CLI `python/planetvortex/cli.py`: arbitrary body
  registers (name, GM, a, i, Omega, period) in, the full ladder out,
  a focused monograph generated in MD + DOCX + PDF — see
  `results/generated/` for the worked examples (the Kepler-452b
  demonstration).
- The formal theorems corpus `docs/theorems/` (Theorems F, G and
  Lemmas F, G with proofs, EN + RU) and the focused per-stage
  monographs `docs/monographs/stages/` (all 15 stages, EN + RU).
- The publication factory `python/planetvortex/pubfigures.py` —
  the 600 dpi ultra-resolution figures per stage folder
  (`figures/600dpi/`) plus the three animations
  (`figures/600dpi/animations/`): the V1 inclined system, the V2
  tiling assembly and the register sweep.
- `python/planetvortex/monograph_gen.py` — the DOCX/PDF monograph
  engine behind the CLI and the editions.
- `tests/test_pv_vregister.py` — 21 tests of the V-register
  (80 total).
- `docs/CI.md` — the continuous-integration contract of the
  mini-repository.

### Changed

- `runner.py` gains `--suite v` (suite planetvortex-vregister);
  version 2.0.0 across all 15 protocols (7 P + 6 X + 2 V).
- The mini READMEs (EN/RU) restructured around the spatial turn:
  new section 5 (the V-register), the 600 dpi gallery, the
  multi-language and self-check chapters; the Makefile gains `v`
  and `all-ladders` targets; the quick preset smokes all three
  suites.

## [1.1.0] — 2026-10-09

### Added

- The hardcore X-register (`python/planetvortex/hardcore.py`) — six
  adversarial stages X1..X6 that re-derive every load-bearing claim of
  the bench by an independent method:
  - **X1** PSL(2,7) from first principles: 2401 matrices over F_7
    enumerated; |GL| = 2016, |SL| = 336, |PSL| = 168; the quotient
    {±I} exactly 2-to-1; the class equation 1 + 21 + 42 + 56 + 24 + 24;
    simplicity certified over all 32 unions of conjugacy classes.
  - **X2** the two natural actions: the faithful transitive action on
    the seven S_4 subgroups (one of the two conjugacy classes) whose
    image is CONJUGATE in S_7 to the research model; the 2-transitive
    (3-homogeneous) action on the eight Sylow-7 subgroups; the Sylow
    census n2 = 21, n3 = 28, n7 = 8 with the Frobenius-21 normalizer.
  - **X3** the (2,3,7) triangle generation: all 336 pairs generate the
    whole group; the Klein relations; the Hurwitz arithmetic
    84(g−1) = 168 = 42(2g−2); the smoothness certificate of the Klein
    quartic (28(xyz)^3 = 0 contradiction + coordinate cases), genus 3.
  - **X4** the hyperbolic {7,3} figure at 50 dps: the exact half-edge,
    inradius and circumradius closed forms, the hyperbolic Pythagoras,
    the area ladder pi/42 → pi/3 → 8pi = 2pi(2g−2), the combinatorial
    closure 3V = 7F = 2E = 168 and 14F = 4E = 6V = 336, plus the
    Poincare-disk construction solved numerically as the independent
    witness (circumradius matched to 0.0, edge to 1.1e-16).
  - **X5** integrator certification: measured convergence order
    2 (leapfrog) and 4 (Yoshida), time-reversibility to roundoff,
    bounded symplectic energy with no secular trend (ratio ≤ 0.01
    against the RK4 control at 0.99), the Laplace-Runge-Lenz vector,
    the vis-viva law and the exact orbit equation.
  - **X6** the GR bridge: 1PN perihelion precession measured against
    the closed form 6πGM/(a(1−e²)c²) — Mercury 42.982″/century against
    the textbook 42.98″ (5.3e-5), the Newtonian control at integrator
    zero, the full 8-planet formula ladder.
- `runner.py --suite p|x|all` — the X-register runs and records its own
  JSON protocols (X1..X6, suite planetvortex-hardcore).
- `tests/test_pv_hardcore.py` — 21 tests of the X-register (59 total).
- `figures/fig05_hardcore_certificates.png` — the four certificates:
  the class equation, the measured convergence orders, the Mercury
  precession against the closed form, the Poincare-disk {7,3} witness.
- `docs/monograph/` — Appendix X in both languages (the hardcore layer).

### Changed

- `runner.py` version 1.1.0; the mini Makefile gains `hardcore` and
  `all-ladders`; the quick preset now smokes both suites.

## [1.0.0] — 2026-10-09

### Added

- `python/planetvortex/classical.py` — Layer P: the committed NASA
  register (GM, radii, semi-major axes, eccentricities, periods,
  surface gravities), the unit system (AU–year–solar mass), the
  two-body Kepler registers with the mass correction, the Schwarzschild
  ladder, the Hill spheres and the gravity ladder.
- `python/planetvortex/fano.py` — Layer F: the Fano plane on Z_7
  (lines {i, i+1, i+3}), the 168 line-preserving permutations
  (PSL(2,7)), the binary model GL(3,2) over F_2, the explicit
  isomorphism, the exact figure closed forms (Theorem A) and the exact
  vortex Hamiltonians (Theorem B).
- `python/planetvortex/model.py` — Layer V: the vectorized Kirchhoff
  N-vortex dynamics, RK4, the invariants H/P/Q/I, the analytic
  Jacobian and the co-rotating stability spectrum.
- `python/planetvortex/nbody.py` — Layer N: the full Newtonian
  Sun + 8-planets planar integrator, barycentric momentum balance,
  total energy/angular momentum, osculating (a, e), the perturbation
  hierarchy.
- `python/planetvortex/ladder.py` — the P1–P7 registered checks with
  the tolerance table and the quick/default/full presets.
- `python/planetvortex/runner.py` — the JSON protocol CLI (suite
  `planetvortex-ladder`, version 1.0.0).
- `python/planetvortex/figures.py` — the protocol-bound figure factory:
  fig01 the gravity figure, fig02 the Kepler register, fig03 the
  planetary simulation, fig04 the vortex lattice + the architecture
  scheme SVG.
- `tests/` — the 38-test guard, including the cross-pin against the
  sibling polyvortex ladder (N = 7 row, bit-for-bit).
- `results/protocols/` — the seven committed default-preset protocols.
- `figures/` — the four 300 dpi figures + the scheme.
- `docs/monograph/` — the big research monograph, RU + EN (md, docx,
  pdf).
- `docs/monographs/` — the theorem editions: Theorems A, B, C and
  Lemmas D, E, RU + EN, docx + pdf (20 files).
- `Makefile` — ladder / quick / full / figures / test / lint / clean.

### Findings

- The exact figure: every Fano line of the heptagonal gravity figure
  is the congruent triangle with angles (pi/7, 2pi/7, 4pi/7), sides
  2R sin(k pi/7) and area sqrt(7)/4 R^2 — the sin-product identity
  sqrt(7)/8 does the work; the chord product is exactly R^3 sqrt(7)
  (Theorem A, protocol P1/P4).
- The seven equal cells: all seven three-vortex Trivortex cells carry
  the same Hamiltonian -(1/2pi) ln(sqrt(7) R^3) and the same shape
  period 9.3814..., measured with spread 0.0 — the dynamical shadow of
  PSL(2,7) (Theorem B, protocol P6).
- The heptagon lattice is Havelock-stable at N = 7 — the last stable
  level, cross-pinned bit-for-bit against the polyvortex W4 scan
  (Theorem C, protocol P5).
- Kepler III certified dynamically: corrected to 6.2e-13 across the
  eight planets, uncorrected misses by m/2M_sun = 4.77e-4 (Jupiter) —
  a 7.7e8x separation; the fact-sheet tables are epoch-mixed at 4.8e-4
  and recorded as provenance diagnostics (Lemma D, protocol P2).
- The mass-ladder deficit is real and quantified: the Fano line sums
  of log10(GM/GM_Earth) span 6.71 dex, and a mild 10% gravity-weighted
  circulation ladder deforms the vortex figure by 0.30 within one
  rotation while the equal ring stays at machine zero (Lemma E,
  protocol P7).
