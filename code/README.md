# TRIVORTEX — The Core Document (`code/`)

> **Navigation:** [repository root](../README.md) › **`code/`**
>
> The heart of the repository: the TRIVORTEX document itself — three language
> mirrors of one 22-section executable monograph on the three-body (and N-body)
> problem in the vortex model with the Chaplygin topological integral.

![Python](https://img.shields.io/badge/Python-3.10–3.12-informational?style=flat-square&logo=python&logoColor=white)
![Lines](https://img.shields.io/badge/size-~2400%20lines%20%C3%97%203-blue?style=flat-square)
![Sections](https://img.shields.io/badge/structure-22%20sections-1284BA?style=flat-square)
![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)

---

## Table of contents

1. [What lives here](#1-what-lives-here)
2. [Provenance and naming](#2-provenance-and-naming)
3. [The three mirrors](#3-the-three-mirrors)
4. [The 22 sections — full map](#4-the-22-sections--full-map)
5. [Running the document](#5-running-the-document)
6. [The interactive menu — all 15 modes](#6-the-interactive-menu--all-15-modes)
7. [The report engine — seven formats](#7-the-report-engine--seven-formats)
8. [Configuration surface](#8-configuration-surface)
9. [Numerical quality and reproducibility](#9-numerical-quality-and-reproducibility)
10. [Relationship to the verification ladder](#10-relationship-to-the-verification-ladder)
11. [Output artifacts map](#11-output-artifacts-map)
12. [Performance profile](#12-performance-profile)
13. [Error handling and robustness](#13-error-handling-and-robustness)
14. [Known quirks and honest caveats](#14-known-quirks-and-honest-caveats)
15. [Extending the document](#15-extending-the-document)
16. [Frequently asked questions](#16-frequently-asked-questions)

---

## 1. What lives here

| File | Console language | Role |
|---|---|---|
| [`trivortex_core.py`](trivortex_core.py) | English (default) | the canonical TRIVORTEX document |
| [`trivortex_core_ru.py`](trivortex_core_ru.py) | Russian | RU mirror — identical physics, identical structure |
| [`trivortex_core_en.py`](trivortex_core_en.py) | English | EN mirror — identical physics, identical structure |

Each mirror is a single self-contained script of roughly 2 400 lines whose only
hard dependencies are `numpy` and `scipy`; `matplotlib` (plots) and `mpmath`
(extra precision) are optional and degrade gracefully when absent. There is no
package to install: the document *is* the file, and every result it prints is
produced by code you can read in the same file.

---

## 2. Provenance and naming

The files carry the TRIVORTEX name; the physics and the 22-section
repository restructure, together with the working-title change of the document
itself:

- **title:** «TRIVORTEX — Vortex Model of the Three-Body (and N-Body) Problem — v1.0»
- **author:** Isaev Iskhak Khamzatovich (ORCID 0009-0003-7299-0701)

The rename touched the module docstring headers, the console banner and the
report title strings — **no logic was modified**. The former name is preserved
in each header as a provenance note, and the reference to the historical Julia
twin (`AB_Cloud_Vortex_System_v2.jl`) is kept as-is: that companion file lived
outside this repository, and a TRIVORTEX-branded Julia port is on the roadmap
([§15](#15-extending-the-document)).

---

## 3. The three mirrors

Why three files with the same physics? The document grew as an interactive
console monograph, and its author maintains native-language variants so the
on-screen narrative (banners, menu prompts, section summaries) reads naturally
in each language. The discipline that keeps the mirrors honest:

- identical 22-section layout, identical section numbering, identical formulas;
- identical `Config` defaults, so the same command produces the same numbers on
  all three;
- identical report schemas — a JSON emitted by the RU mirror parses with the
  same reader as one from the EN mirror.

The default mirror for citation and CI purposes is `trivortex_core.py`. The CI
pipeline syntax-checks all three on Python 3.10–3.12.

---

## 4. The 22 sections — full map

| № | Section | What it does | Key symbols |
|---|---|---|---|
| 1 | Imports and dependencies | numpy/scipy/matplotlib stack; optional mpmath; font and DPI setup | — |
| 2 | Constants and global configuration | SI constants; RMT reference values for ⟨r⟩; the `Config` class | `G_NEWTON`, `R_GUE`, `Config` |
| 3 | Data structures | result containers for every suite | `ChaplyginResults`, `RMTResults`, `TopologicalResults`, `AdvancedRMTResults`, `ChaosResults` |
| 4 | Hamiltonian construction | L×L Hofstadter matrix with `N_v` embedded vortices: Peierls phases `2πα(ix−1)dy`, vortex AB phases, charge-weighted core potential, Hermitian symmetrization | `build_hofstadter_hamiltonian` |
| 5 | **Analytical solution (Theorem 3.1)** | the closed form `r_k(t)`, `θ_k(t)`; frequency `ω = (2π/T)·e^{C_Ch/π}`; amplitude `ε = 1/(e^{C_Ch/π}−1)`; the Chaplygin combination | `analytical_solution_r/theta`, `analytical_frequency`, `analytical_amplitude`, `compute_chaplygin_constant` |
| 6 | Chaplygin conservation verification | Section-6 procedure: `C_Ch(t)` recorded along the closed form over `[0, 100·T]`; endpoint-drift diagnostic; Berry-phase side value | `verify_chaplygin_conservation` |
| 7 | Spectral statistics (GUE/GOE/Poisson) | polynomial unfolding, ⟨r⟩ statistic, manual KS tests against the three classical ensembles, ensemble verdict | `unfold_spacings`, `compute_r_statistic`, `analyze_rmt_statistics` |
| 8 | Zeta zeros and Montgomery test | first 50 Riemann ζ-zeros as reference spectrum; Montgomery pair-correlation comparison | `KNOWN_ZETA_ZEROS` |
| 9 | Quantum version with topological qubits | quantized vortex model, topological qubit states | — |
| 10 | Real system presets | `RealSystem` records: Sun–Earth–Moon, α Centauri, Pluto–Charon–Nix | `real_systems_presets` |
| 11 | High-resolution plot generation | 300-dpi figures: analytic solution, spectra, phase diagrams | `generate_plot_analytical_solution` |
| 12 | Report generation | one data model → TXT, MD, HTML, CSV, JSON, DOCX (RTF), PDF writers, zero external dependencies | `generate_all_reports` |
| 13 | Comprehensive test functions | in-document self-tests of the analytic and spectral layers | — |
| 14 | Interactive menu | the 15-mode console driver | `display_menu` |
| 15 | Main entry point | banner + menu loop | `main` |
| 16 | Berry phase calculation | Berry phase along parameter loops in the vortex background | `compute_berry_phase` |
| 17 | Chern number computation | Fukui–Hatsugai–Suzuki lattice method | — |
| 18 | TKNN Hall conductance | topological transport from Chern markers | — |
| 19 | Dirac cone analysis | locating and fitting Dirac points | — |
| 20 | Spectral form factor | `K(t)` with GUE ramp/plateau comparison | — |
| 21 | Number variance and IPR | `Σ²(L)` spectral rigidity; inverse participation ratio | `compute_number_variance` |
| 22 | Lyapunov exponent + permutation test | largest Lyapunov exponent; permutation Z-score; KAM statistics | — |

The numbering is stable and citable: "Section 6 of the document" means the same
thing in every mirror, in the verification ladder, and in the documentation
site.

---

## 5. Running the document

```bash
# canonical mirror, interactive menu
python3 trivortex_core.py

# language variants
python3 trivortex_core_ru.py
python3 trivortex_core_en.py
```

Requirements: Python ≥ 3.10; `numpy`, `scipy` (hard); `matplotlib` (plots),
`mpmath` (extra precision) — both optional. A full interactive session with all
15 modes takes a few minutes on a laptop; individual suites are seconds each.

---

## 6. The interactive menu — all 15 modes

| Mode | Suite | What it runs |
|---|---|---|
| `1` | Full verification | the whole analytic + spectral chain in one pass |
| `2` | Chaplygin verification suite | `C_Ch` diagnostics across parameter ranges (the Section-6 procedure) |
| `3` | RMT statistics | ⟨r⟩ and KS verdicts for `N_v ∈ {3, 5, 10, 15, 25, 50}` |
| `4` | Montgomery test | model spectrum vs the first 100 ζ-zeros |
| `5` | Quantum suite | Berry phase, Chern numbers, Hall conductance on an α-grid |
| `6` | Real systems | the three astronomical presets, printed and analysed |
| `7` | Hamiltonian spectrum | first 20 eigenvalues of the built matrix |
| `8` | Theorem 3.1 check | closed form vs its own reference table |
| `9` | Custom `N_v` | generalized simulation for `N_v = 3, 4, 5, …` |
| `10` | Reports | the seven-format bundle of Section 12 |
| `11` | Plots | 300-dpi figures (after a suite has produced data) |
| `12` | Topological suite | Sections 16–19 in action |
| `13` | Advanced RMT | number variance, form factor, IPR (Sections 20–21) |
| `14` | Chaos suite | Lyapunov exponents, permutation test (Section 22) |
| `15` | Cross-correlations | correlation matrix across the observable keys |
| `c` / `s` / `h` / `q` | configure / show config / help / quit | session management |

---

## 7. The report engine — seven formats

Section 12 renders one result object into seven formats: **TXT, MD, HTML, CSV,
JSON, DOCX (via RTF), PDF** — with no external dependencies beyond the standard
library, which keeps the document truly self-contained. Every report header
carries the document title, the version and the parameter snapshot used, so a
report file is reproducible from its own metadata. The JSON variant is the
machine-readable contract: flat schema, stable keys, parseable by the same
reader across all three mirrors.

---

## 8. Configuration surface

The `Config` class (Section 2) exposes every tunable:

| Group | Parameters | Defaults |
|---|---|---|
| lattice | `lattice_size` (L), `n_vortices` (N_v), `alpha` (flux), `disorder_strength` (W), `n_seeds` | 20, 3, 0.5, 2.0, 5 |
| Chaplygin | `C_Ch`, `q_charges`, `T_period` | 1.0, (1, −1, 1), 2π |
| output | `generate_plots`, `plot_dpi`, report directory | on request, 300 dpi |

The interactive `c` menu mode mutates the session configuration; for scripted
use, import the mirror as a module and drive the section functions directly —
they are plain functions with no hidden global state beyond `matplotlib`'s
Agg backend.

---

## 9. Numerical quality and reproducibility

- The Hamiltonian build is **seeded** (`seed=42` by default): the same command
  yields the same matrix, spectrum and statistics on any machine.
- The analytic layer (Section 5) is exact float64 arithmetic — no integrators
  involved — so its reference values (e.g. `ω = 1.3748022274393588` for
  `C_Ch = 1`) are pinned by the pytest suite in
  [`verification/tests/`](../verification/tests/README.md).
- Numerical suites report their own residuals next to every verdict, and the
  report engine copies the parameter snapshot into every output format.
- The **independent** confirmation of the core claims lives outside this
  folder: [`verification/trivortex/python/verify.py`](../verification/trivortex/python/verify.py)
  re-derives the choreography, the Lagrange rotation and the vortex integrals
  from scratch (next section).

---

## 10. Relationship to the verification ladder

This document and the ladder are deliberately **independent codebases** checking
the same objects:

| Object | In the document | In the ladder |
|---|---|---|
| closed form of Theorem 3.1 | Section 5 | `check_v1_theorem31` |
| Chaplygin combination `C_Ch(t)` | Section 6 (recorded drift) | V1 diagnostic (recorded, no pass/fail role) |
| Lagrange rigid rotation | Section 4/5 physics | `check_v2_lagrange_rotation` (RK4, ω = 3Γ/(2πa²)) |
| vortex integrals `H, P, Q, I` | implicit in the dynamics | `check_v3_invariants`, `check_v4_robustness` |

If a refactor ever makes the two disagree, the pytest guard catches it at the
pinned reference values before either side drifts. The ladder's honesty notes
explain why the C_Ch drift is a *recorded diagnostic* rather than a conservation
law — read [`verification/README.md §11`](../verification/README.md#11-honesty-notes)
before quoting it anywhere.

---

## 11. Output artifacts map

Every mode of the menu writes artifacts, never bare console output alone. The
`outputs/` directory is the document's own archive; it is regenerated on demand
and never required for the ladder (which shares no code with the document).

| Artifact | Producer | Content |
|---|---|---|
| `outputs/report_*.txt` | modes 1, 10 | plain-text verification protocol |
| `outputs/report_*.md` | modes 1, 10 | GitHub-renderable summary with tables |
| `outputs/report_*.html` | modes 1, 10 | styled single-file HTML report |
| `outputs/report_*.csv` | modes 1, 10 | flat numeric tables for pipelines |
| `outputs/report_*.json` | modes 1, 10 | full machine-readable protocol |
| `outputs/report_*.docx` | modes 1, 10 | editable Word edition |
| `outputs/report_*.pdf` | modes 1, 10 | print-ready edition |
| `outputs/plot_*.png` | modes 1, 9, 11 | 300-dpi figures |
| `outputs/chaplygin_*.json` | mode 2 | Section-6 conservation diagnostics |
| `outputs/rmt_*.json` | mode 3 | spectral-statistics protocols |
| `outputs/quantum_*.json` | mode 5 | Berry-phase and qubit protocols |
| `outputs/chaos_*.json` | mode 14 | Lyapunov + permutation protocols |

All writers share one data model (Section 3 containers), so a value that appears
in the TXT report appears identically in the JSON protocol and the DOCX edition
— there is no second code path that could drift.

---

## 12. Performance profile

Timings on a single modern core, Python 3.12, float64:

| Operation | Typical time | Dominated by |
|---|---|---|
| Menu startup (banner + config) | < 0.1 s | imports |
| Hofstadter matrix build (L = 25, N_v = 3) | ~0.3 s | Kronecker products |
| Full spectrum + unfolding (L = 25) | ~1.2 s | eigensolver |
| ⟨r⟩ statistic over 5 lattice sizes | ~4 s | repeated eigensolves |
| Montgomery test (50 ζ-zeros) | ~0.8 s | pair-correlation scan |
| Berry phase sweep (8 flux values) | ~2.5 s | parameter loops |
| Report engine, all seven formats | ~0.4 s | string assembly |
| Full verification suite (mode 1) | ~15–25 s | everything above |
| 300-dpi plot set (mode 11) | ~3 s | matplotlib rendering |

The document is deliberately single-threaded and deterministic: no random state
beyond fixed seeds, no parallelism that could reorder floating-point sums.

---

## 13. Error handling and robustness

The interactive layer is designed to survive real terminal conditions:

- **EOF-safe input** — every `input()` in the menu loop, the configuration
  dialogs and the pause prompt goes through `safe_input()`: piping input,
  closing the terminal or pressing Ctrl-D exits cleanly (`SystemExit(0)`)
  instead of raising `EOFError` tracebacks.
- **Ctrl-C** — interrupts land as a clean `SystemExit(130)`, not a stack trace.
- **Per-action containment** — each menu action runs inside its own try/except;
  a failure prints `[ERROR] type: message` plus the traceback, and the menu
  continues with the configuration intact.
- **Optional dependencies degrade** — `matplotlib` and `mpmath` are probed at
  import; the analytic, spectral and report layers run headless without them,
  and the menu flags the unavailable modes instead of crashing.
- **Invalid choices** are reported and re-prompted, never fatal.

---

## 14. Known quirks and honest caveats

- **The C_Ch drift is window-dependent.** Section 6 records the endpoint drift
  of an oscillating combination; its value depends on `[0, T_max]`. This is a
  property of the model's definition, documented rather than hidden.
- **The Julia twin is referenced, not shipped.** The docstring headers mention
  `AB_Cloud_Vortex_System_v2.jl` — the historical companion file lived outside
  this repository. The Python mirrors are the canonical executable text.
- **Preset masses are configuration, not results.** Section 10's astronomical
  records carry source-scale uncertainties (Nix's mass is order-of-magnitude);
  the verified core of the ladder never depends on them.
- **`matplotlib` must be importable for plots only.** The analytic, spectral and
  report layers run headless without it.

---

## 15. Extending the document

1. **Pick the section number first.** A new experiment becomes Section 23+ in
   *all three mirrors simultaneously* — the mirrors only diverge in console
   language, never in structure.
2. **Results go into a container** (Section 3 pattern), so the report engine
   picks it up in all seven formats without per-format code.
3. **Claims go through the ladder.** If a new section makes a checkable claim,
   add the corresponding independent check to
   [`verification/trivortex/python/verify.py`](../verification/trivortex/python/verify.py)
   with a registered criterion in
   [`verification/README.md`](../verification/README.md) *before* the code
   lands, and pin reference values in
   [`verification/tests/`](../verification/tests/README.md).
4. **Update the maps.** The section table in this README, the section map on
   the [code page](https://wild8highlander.github.io/Trivortex/code.html)
   and the `SECTION_NAMES` registry in
   [`verification/common/python/config.py`](../verification/common/python/config.py)
   must move together with the code.

---

## 16. Frequently asked questions

**Q: Which mirror should I run?**
`trivortex_core.py` (default console: English) is canonical. `_en.py` and
`_ru.py` are the explicit language mirrors; all three share the identical
22-section structure and physics, and differ only in console language.

**Q: Why does the document exist as one big file?**
The file *is* the document: 22 numbered sections that read in order, like a
monograph, and execute in order, like a program. Splitting it into a package
would make the "executable monograph" claim false — and the file is still small
enough to read in one sitting (~2 400 lines).

**Q: The ladder disagrees with the document — who wins?**
The ladder. It shares no code with the document by design; if the two disagree,
the document has a bug. Attach both JSON protocols to an issue and the
discrepancy is reproducible in one step.

**Q: Can I cite a section of the document?**
Yes — the numbering is stable and identical across mirrors. "Section 5,
Theorem 3.1" means the same thing in the code, in the ladder, in the monographs
and on the documentation site.

**Q: How do I regenerate every plot and protocol from scratch?**
Mode 1 of the menu (full verification) or, headlessly:
`python3 -c "import runpy; runpy.run_path('code/trivortex_core.py')"` with stdin
closed is not the intended path — use the menu or the Make targets; the ladder
regenerates its own protocols independently.
