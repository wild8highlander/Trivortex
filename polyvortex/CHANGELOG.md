# Changelog

All notable changes to the polyvortex mini-repository are documented here.
The format follows Keep a Changelog; this file is excluded from the
markdownlint contract of the parent repository.

## [1.0.0] — 2026-10-08

### Added

- The self-contained mini-repository `polyvortex/` inside the TRIVORTEX
  framework: the N-vortex extension bench with its own codes, monograph,
  ladder and protocols.
- `python/polyvortex/model.py` — Layer K: vectorized Kirchhoff RHS for N
  vortices, RK4, the integrals H, P, Q, I, the analytic pair-Jacobian and
  the co-rotating stability spectrum.
- `python/polyvortex/ansatz.py` — Layer G: the generalized Theorem 3.1
  closed form (Hypothesis H1), the admissibility threshold
  `C_CH_STAR = pi*ln(2)`, the minimum-radius register and the Section-6
  gauge diagnostic.
- `python/polyvortex/classical.py` — the regular N-gon relative
  equilibria: `omega_N = Gamma*(N-1)/(4*pi*R^2)`, the chord table, the
  unwrap discipline for measured rotation rates.
- `python/polyvortex/ladder.py` — the seven-stage W-ladder:
  W1 anchor (pinned Theorem 3.1 literals at N=3), W2 ring rotation
  (N=2..8), W3 invariant conservation, W4 Havelock stability threshold,
  W5 admissibility, W6 kinematic obstruction, W7 averaged-frequency
  bridge with the T_comp compatibility table.
- `python/polyvortex/runner.py` — the JSON protocol CLI
  (`--preset quick|default|full`, `--stage W1..W7`).
- `tests/` — 26 tests: cross-validation against the parent ladder (RHS,
  invariants, the diagnostic), the Jacobian vs finite differences, the
  pinned literals, the threshold identities, the committed-protocol
  re-derivation ("bound to a run").
- `results/protocols/` — seven committed JSON protocols (default preset),
  deterministic file names.
- `docs/monograph.md` — the research monograph: Theorem B
  (admissibility, pi*ln 2), Lemma C (the radial pair-cancellation
  obstruction), Lemma D (the (1-eps^2)^(-3/2) averaged-frequency
  identity), the D1 compatibility table, the TB1..TW5 formalization
  queue aligned with the parent roadmap T1/T3/T5.
- `Makefile` — ladder / quick / test / lint / clean.

### Findings

- The parent default pair (C_Ch, T) = (1, 2*pi) lies below the
  admissibility threshold pi*ln(2): the closed form crosses r = 0 there
  (structural registers unaffected, polar registers degenerate).
- Hypothesis H1 is dynamically obstructed: the induced radial velocity of
  the symmetric pulsation vanishes identically (Lemma C), and the
  phase-shifted variant fails the shape register linearly with slope
  sqrt(3)/2 while its induced radial velocity scales as ~0.04*eps^2.
- The Havelock threshold is reproduced spectrally: stable N<=7 with
  max Re(lambda) <= 7e-9, unstable N=8 with max Re(lambda) = +0.450.
- Cross-ladder handshake: omega_N at (N=7, R=1, Gamma=1) equals
  6/(4*pi) = 3/(2*pi) = 0.477464829275686 — the parent's registered
  Lagrange literal (locked by a unit test).

## [1.1.0] — 2026-10-08

### Added

- `python/polyvortex/figures.py` — the publication figure factory: four
  300 dpi PNG figures + the architecture scheme SVG, every plotted register
  read from the committed W1..W7 protocols; the `make figures` target.
- `figures/` — fig01 two layers, fig02 ring rotation, fig03 stability scan,
  fig04 admissibility + D1, scheme_polyvortex.svg.
- `docs/monograph/` — the big research monograph in two renditions
  (monograph_RU.md new full translation; monograph_EN.md moved from
  docs/monograph.md) and its DOCX + PDF renditions (LibreOffice pipeline,
  field TOCs, embedded figures).
- `docs/monographs/` — the theorem monograph edition: five separate
  bilingual monographs (Theorems A, B, E; Lemmas C, D), each with the
  statement, the full proof, the protocol certification, the discussion,
  the roadmap link and the references — 20 files (RU + EN, DOCX + PDF).

### Changed

- Version bumped to 1.1.0 across the package; the committed protocols
  regenerated with the new suite version.
- README/README_RU: the publication-stack section and the updated layout.
