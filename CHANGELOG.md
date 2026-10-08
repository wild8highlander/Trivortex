# Changelog

All notable changes to the TRIVORTEX research program are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [SemVer](https://semver.org/).

---

## [Unreleased]

### Added — the multi-language verification ports (milestones M1–M3, v1.1)

The verification roadmap stopped being a roadmap: every planned port
landed, with its acceptance criteria checked in the same commit that
brought the artifact.

- **M0+ — the interactive scientific laboratory**
  (`verification/trivortex/python/lab.py`): a bilingual (EN/RU)
  researcher's bench around the unchanged `verify.py` — presets and
  fully custom parameters (C_Ch, T, Γ, a, rotations, steps/period),
  convergence and invariant-drift analyses, and a full figure set at
  600 dpi in three formats (PNG + PDF + SVG): the closed form, the
  Section-6 Chaplygin diagnostic, the choreography, the convergence,
  the unequal-circulation robustness, the drift scan and a one-glance
  dashboard. Every run writes the registered JSON protocol and CSV data.
- **M1 — independent re-derivation**
  - `verification/coq/Trivortex.v` — the statement layer in Gallina with
    the choreography and periodicity lemmas **proven**; zero axioms
    beyond the standard-library classical base (`Print Assumptions`
    closed), plus the exact equilateral anchors H = 0, P = 0, Q = 0,
    I = Γ and the tolerance bands as a machine-checked record.
  - `verification/lean4/Trivortex.lean` — the same statement layer over
    Mathlib (`theta_separation`, `r_periodic`, `theta_periodic`, the
    Chaplygin shape, the exact anchors), all `#print axioms`-closed,
    with `lakefile.lean` + `lean-toolchain` (v4.4.0).
  - `verification/rust/` — the dependency-free f64 numeric twin of the
    ladder: 14 pinned-reference tests, the quick preset reproducing the
    Python reference numbers inside the registered bands (the V4 drifts
    match bit-for-bit in printed form), an interactive bilingual
    laboratory with JSON/CSV/SVG export, and the committed protocol of a
    real run (`rust/protocol_quick.json`).
- **M2 — cross-checked statements**
  - `verification/isabelle/Trivortex.thy` — the Isabelle2024 HOL session
    with proven choreography/periodicity, the exact anchors and the
    machine-checked band record; the SMT-discharged numeric bounds land
    as an optional session (`Trivortex_SMT.thy`) kept out of the default
    build until Z3 ships in the pinned image.
  - `verification/agda/Trivortex.agda` — the constructive angle
    arithmetic: the C3 rotation lattice of the choreography (`rot³ ≡ id`
    on `Fin 3`), the uniform-phase lattice, the closed-form periodicity
    over ℚ given the single declared turn-period axiom, the Chaplygin
    additivity identity and the exact centroid anchors.
- **M3 — performance & exactness**
  - `verification/cpp/` — the CMake/CTest port compiled at `-O2`: 21
    pinned-reference guard assertions, the benchmark metric
    (`benchmark_rhs_per_s`, ≈ 1.7e7 rhs/s measured) in every protocol,
    and the interactive bilingual laboratory with SVG/CSV export;
    the committed protocol of a real run (`cpp/protocol_quick.json`).
  - `verification/haskell/` — the dual ladder: the `Double` numeric twin
    (base-only, no dependencies) paired with the exact-rational run over
    ℚ(√3), where the equilateral anchor identities hold *by computation*
    (equality on ℚ(√3) is decidable); 21 guard assertions; bilingual lab.
- **Infrastructure**
  - `.github/workflows/verification-ports.yml` — the non-blocking CI
    contract of §10: cargo test, CMake/CTest, cabal test, the lab smoke,
    and the four formal toolchains compiled inside their pinned images.
  - All seven toolchain Dockerfiles re-targeted from the retired section
    binaries to the landed artifacts (the Rust image now builds the M1
    crate; Isabelle bumped to the documented Isabelle2024 pin).
  - `verification/tests/test_ports.py` — the toolchain-agnostic port
    guard (36 tests): artifact presence, SPDX headers, the bilingual
    README_RU contract, and the committed Rust/C++ protocols pinned
    against the Python ladder's reference numbers.
  - `verification/README.md`, `docs/site/verification.html` and every
    port README flipped from *planned — skeleton* to *landed*, with each
    directory gaining a bilingual `README_RU.md`.

## [1.0.1] — 2026-10-07 — the toolchain-consistency release

A maintenance release: no physics content changed — every theorem,
verification check, study, figure and monograph is bit-for-bit the 1.0.0
program. What changed is the repository toolchain around it, made fully
self-consistent after the rename to Trivortex.

### Fixed
- **Repository identity.** All 310 references to the pre-rename repository
  slug `research-papers` (README badges and links, CITATION.cff, pyproject
  URLs, .zenodo.json, the documentation site, every research and verification
  README, the license texts, the Zenodo release workflow) now point to
  `wild8highlander/Trivortex` and its GitHub Pages site
  `wild8highlander.github.io/Trivortex`.
- `Makefile`: the pytest-guard help line said «28 tests»; the guard runs 27.
- `docs/site/index.html`: the pytest badge said «28 passed»; it is 27.
- `.github/workflows/lint.yml`: the mypy step targeted the nonexistent
  `verification/python/` directory; it now checks
  `verification/common/python` and `verification/trivortex/python`.
- `.github/workflows/docker.yml`: the build matrix referenced `python`,
  `julia` and `java` Dockerfiles that do not exist and silently skipped the
  real `agda` and `isabelle` images; the matrix now matches the committed
  Dockerfiles exactly.
- `.github/workflows/scorecard.yml`: the Scorecard action was given a
  nonexistent `SCORECARD_TOKEN` secret; it now uses the built-in
  `GITHUB_TOKEN`.
- `.github/workflows/zenodo.yml`: release archives and deposit metadata are
  now named `trivortex-<tag>` and carry the correct repository URL.
- `.commitlintrc.json`: the file carried shell-style `#` comment lines above
  the JSON body; strict JSON loaders (commitlint's own included) reject
  comments, so the config could be silently ignored. It is now valid JSON.
- `.github/workflows/zenodo.yml`: the release deposit declared
  `CC-BY-NC-SA-4.0` while `LICENSE.md`, `.zenodo.json` and `MANIFEST.json`
  all declare IPL-RP-1.0; every Zenodo pathway now states the same license
  (`LicenseRef-Proprietary-Wild8Highlander-1.0`).
- `.gitignore`: Python bytecode (`__pycache__/`, `*.py[cod]`), tooling caches
  (`.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, coverage), virtualenvs
  and OS noise are now ignored, so running the document or the tests can no
  longer stage artifacts into a commit.
- Release metadata alignment: `pyproject.toml`, `CITATION.cff`,
  `.zenodo.json` and the README/ documentation-site release badges all state
  1.0.1, matching the tag.

### Added
- `SUPPORT.md`: the support channel guide (which channel for what,
  reproduction checklists, response expectations).
- A ready-to-upload `social-preview.png` (1280×640) for the repository
  settings — Settings → General → Social preview.

---

## [1.0.0] — 2026-10-07 — the first public release

The first complete, self-consistent public edition of the TRIVORTEX research
program: the executable three-body vortex document, its independent
verification ladder, twelve companion studies, the bilingual monograph library,
the orbital animations, the documentation
site and the full GitHub toolchain — everything regenerated from committed
sources and checked on every push.

### Added — the core program
- `code/trivortex_core*.py`: the 22-section executable document in three
  language mirrors (default EN console + explicit RU and EN mirrors), an
  interactive 15-mode menu, a seven-format report engine
  (TXT/MD/HTML/CSV/JSON/DOCX/PDF), 300-dpi plot generation and EOF-safe
  interactive I/O.
- Theorem 3.1 — the Lagrange-type closed-form rotating solution with the
  radial modulation `r_k(t) = √C_Ch·(1 + ε·cos(ωt + 2πk/3))`,
  `ω = (2π/T)·e^(C_Ch/π)` — pinned to hard float64 reference values.
- The Chaplygin topological integral `C_Ch = r²(θ̇ − q·A_θ)` with the honest
  certified-vs-recorded separation of the endpoint-drift diagnostic.

### Added — verification
- `verification/trivortex/python/verify.py`: the independent from-scratch
  ladder V1–V4 (zero code shared with the document), three presets
  (quick ≈ 0.5 s, default ≈ 2 s, full ≈ 35 s), JSON protocols with full
  parameter snapshots.
- `verification/tests/`: the 28-test pytest guard — 13 hard reference-value
  pins, 12 study smoke suites, the completeness test, the library test and
  the companion-volume test.
- `verification/docker/`: seven pinned toolchains (Coq, Lean 4, Rust,
  Isabelle-HOL, Agda, C++, Haskell) carrying the staged M1–M3 roadmap.

### Added — the extended research program (TRX-01…12)
- Twelve executable studies around the three-body problem — laser optics
  (TRX-01…05, 12), quantum matter (TRX-06…08), the classical Kirchhoff–Chaplygin
  anchor (TRX-09) and celestial mechanics (TRX-10, 11) — 80 registered
  acceptance checks, all PASS, every number bound to a committed JSON protocol.
- Deterministic `--smoke` / `--figures` modes wired into CI and Make.
- Schematic SVG + four ultra-resolution (450-dpi) figures per study, all
  committed.

### Added — publications and monographs
- The reading room `publications/`: 28 typeset vector PDFs + 28 editable
  DOCX — Russian and English as separate documents — covering the twelve
  study monographs, the core monograph and the research compendium; 14
  editable HTML sources; navy-gold design system; MathML equations rendered
  offline via pandoc; page numbers stamped by headless Chromium; document
  metadata on every file.
- `publications/build/`: the reproducible build system
  (`md2html_lib.py`, `build_pdf_library.py`, `build_special_pdfs.py`,
  `finalize_pdf.py`) — one command (`make pdf-library`) rebuilds the library.

### Added — docs, site and tooling
- `docs/animations/`: four seamless-loop orbital animations (GIF + MP4) with a
  committed deterministic generator.
- `docs/site/`: the nine-page GitHub Pages documentation site, including the
  publications page and a branded 404; deployed verbatim (static upload,
  `.nojekyll`) by `deploy-docs.yml`.
- Program-level dashboards: `docs/assets/program-checks-dashboard.png` and
  `docs/assets/ladder-accuracy.png` (600 dpi), generated from the committed
  protocols.
- The full GitHub toolchain: CI (syntax + ladder + pytest), lint (markdown/
  YAML/Python), CodeQL, dependency review, Docker builds, link checker,
  OpenSSF Scorecard, release drafter, stale bot, labeler, Zenodo minting,
  issue/PR templates, code owners, Dependabot, funding, REUSE metadata and a
  dev container.
- `Makefile`: `verify`, `verify-quick`, `verify-full`, `test`, `lint`,
  `research-smoke`, `research-full`, `research-figures`, `animations`,
  `pdf-library`, `docs`.

### Fixed
- The interactive menu no longer crashes with `EOFError` on piped input,
  closed terminals or Ctrl-D; Ctrl-C exits cleanly (`SystemExit`).
- `lint.yml` branch filters (`branches: [main]`) restored to valid syntax.
- All broken relative links across the documentation removed (the retired
  multi-topic trees are no longer referenced anywhere).
- The publications test now matches the actual v1.0.0 library layout
  (28 + 28 renditions) and passes.

### Changed
- Version branding unified to **1.0.0** across README, CHANGELOG,
  CITATION.cff, `.zenodo.json`, `pyproject.toml`, the code banners, the
  documentation site and the badge wall.
- Authorship corrected everywhere: Isaev Iskhak Khamzatovich
  (ORCID 0009-0003-7299-0701).
- Documentation expanded: the root README, every study README (26 sections),
  the framework, code, publications, research and docs indexes — all rebuilt
  for the 1.0.0 edition, English-only.
- Study figures regenerated at 450 dpi (ultra-resolution edition).

### Removed
- All `README_RU.md` mirrors — the documentation is English-only by design;
  the Russian language lives where it belongs, in the separate Russian
  monograph renditions and the RU console mirror of the document.
- Stale provenance references to retired multi-topic trees.

---

[Unreleased]: https://github.com/wild8highlander/Trivortex/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/wild8highlander/Trivortex/releases/tag/v1.0.1
[1.0.0]: https://github.com/wild8highlander/Trivortex/releases/tag/v1.0.0
