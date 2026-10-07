# TRIVORTEX Research Program — Full-Format Study Specification (v2.2.0)

This document is the binding standard for the **full monograph format** of every
TRX study in `research/`. Version 2.1.0 introduced executable studies
(README + code + JSON protocol + quick SVG). Version 2.2.0 ("Monograph
Edition") upgrades every study to the layout below. The standard exists so
that all twelve studies look, read and reproduce identically — "everything in
its place".

---

## 1. Target directory layout (per study)

```text
research/TRX-XX-slug/
├── README.md               # EN — expanded full-format README (sections 1–14)
├── README_RU.md            # RU — full mirror of README.md (not a summary)
├── code/
│   └── trxXX_*.py          # existing script, extended with --figures mode
├── figures/
│   ├── scheme_trxXX.svg    # schematic diagram (authored SVG, navy–gold)
│   ├── fig01_<slug>.png    # 300 DPI (ultra-resolution)
│   ├── fig02_<slug>.png
│   ├── fig03_<slug>.png
│   └── fig04_<slug>.png    # exactly 4 PNG figures per study
├── monograph/
│   ├── monograph_EN.md     # ≥ 240 lines, 10 sections (see §4)
│   └── monograph_RU.md     # ≥ 240 lines, full translation (see §5)
└── results/
    ├── trxXX_results.json  # existing protocol (unchanged semantics)
    └── trxXX_plot.svg      # existing quick-look plot (kept)
```

## 2. Figure requirements (`--figures` mode)

The study script must accept `--figures` (composable with `--smoke`):
`python3 code/trxXX_*.py --figures` writes the 5 vector/raster artifacts into
`figures/` and adds a `"figures"` block (file names + captions) to the JSON
protocol. Requirements:

- **Resolution**: `dpi=300`, figure sizes ~11×7.5 in → ≥ 3000 px wide.
- **Layout**: `constrained_layout=True`; never call `tight_layout()`,
  `subplots_adjust()` or `savefig(..., bbox_inches="tight")`.
- **Palette**: NAVY `#0A1730`, GOLD `#D4AF37`, LIGHT GOLD `#F0D98C`;
  series colors: `["#D4AF37", "#4C72B0", "#55A868", "#C44E52", "#8172B2"]`.
  White figure background; navy titles; grid `alpha=0.3`.
- **Text**: figure language is **English** (repository convention; the
  bilingual prose lives in the README/monographs). Every axis labelled with
  units; every figure has a suptitle `TRX-XX · <short title>`; legends pushed
  outside the axes with `bbox_to_anchor` when they would overlap data.
- **Panel plan** (adapt to the study's actual computed data):
  `fig01` — geometry / landscape overview of the model;
  `fig02` — headline quantitative result (the money plot);
  `fig03` — parameter sweep / stability-sensitivity map;
  `fig04` — dynamics: time series, phase portrait or residual/invariant plot.
- **Scheme** (`scheme_trxXX.svg`): hand-authored static SVG, white background,
  navy strokes (1.5–2 px), gold accents, English labels, title line
  `TRX-XX — Scheme: <concept>`, width 960, viewBox kept, no external
  references. It must explain the physical idea of the study (bodies, fields,
  laser paths, invariant flow), not the software architecture.
- Smoke mode must remain fast (< 20 s); `--figures` in smoke mode is allowed
  but not required by CI; full-mode figures are the canonical deliverable.

## 3. README.md (EN) — expanded structure

Rewrite/expand the existing README to **≥ 200 lines**, keeping the current
section numbering style and all existing verified facts (they are already
correct — extend, do not contradict):

1. Title + one-paragraph essence (bold key quantities).
2. Mission — why this study exists in TRIVORTEX (expand to 2 paragraphs).
3. Physical system and preset (tables preserved).
4. Governing equations (numbered E1, E2, … as already used).
5. Scheme — embed `figures/scheme_trxXX.svg` + a bullet walkthrough of the
   diagram elements.
6. Mapping to TRIVORTEX (table preserved; add ≥ 1 row if natural).
7. Dimensionless formulation.
8. Numerical experiment and acceptance checks (table preserved).
9. Figure gallery — embed all four PNGs with captions and one sentence each.
10. How to run (run, smoke, figures) — code block with the three commands.
11. Results (full run) — console block with the real numbers from the JSON.
12. Data & reproduction — file map of the study directory.
13. Cross-links (preserved; keep TRX cross-references accurate).
14. References (preserved, numbered).

## 4. monograph/monograph_EN.md — structure

**≥ 240 lines**, academic register, 10 sections, LaTeX in `$…$` / `$$…$$`
(GitHub rendering), figures embedded by relative path `../figures/…`:

1. **Title block** — study id, title, program line
   (`TRIVORTEX Research Program · v2.2.0 · Monograph Edition`), date,
   author line `Isaev Iskhak Khamzatovich`, DOI line
   `10.5281/zenodo.21825394`.
2. **Abstract** — 150–200 words, self-contained, with headline numbers.
3. **1. Introduction and historical context** — the classical lineage of the
   problem (≥ 4 paragraphs: origin, key results, modern relevance, why
   TRIVORTEX needs it).
4. **2. Physical formulation** — system, scenario, assumptions, preset table.
5. **3. Mathematical model** — full equations with definitions of every
   symbol, numbered (M1), (M2), …; include the derivation logic, not just
   the result.
6. **4. Connection to the TRIVORTEX framework** — mapping table + a paragraph
   on the Chaplygin-integral / theorem-3.1 viewpoint.
7. **5. Numerical method** — integrator, tolerances, bracketing/Newton
   details, parameter table, reproducibility statement.
8. **6. Results and analysis** — subsections per figure; every real number
   quoted from `results/trxXX_results.json`; embed all four figures.
9. **7. Discussion** — limitations, parameter regimes not covered, natural
   extensions, relation to sibling studies.
10. **8. Conclusions** — numbered findings (5–8 items, each with the number).
11. **9. References** — ≥ 6 numbered entries, real literature.
12. **Appendix A** — full parameter table; **Appendix B** — reproduction
    commands and expected runtimes.

## 5. Bilingual rules (RU mirror)

- `monograph_RU.md` and `README_RU.md` are **full translations**, not
  summaries: every section, table, equation, caption and reference title
  policy must be present.
- Keep equations, symbols, units and code identifiers as-is; translate prose.
- Reference titles stay in the original language; add Russian rubric
  («Список литературы»).
- Russian scientific orthography: «задача трёх тел», «интеграл Чаплыгина»,
  «точки Лагранжа», «циркуляция», кавычки-«ёлочки».
- Section headers mirror the EN numbering one-to-one so cross-references
  survive translation.

## 6. Code rules

- The study script keeps its existing behavior, checks and JSON semantics.
  `--figures` is additive: compute (or reuse) the same data, then render.
- No new third-party dependencies (numpy / scipy / matplotlib only).
- The full run incl. `--figures` must finish < 120 s on CI-grade hardware.
- Keep the module docstring, banner style and the `add(...)` protocol helper
  conventions already used by the scripts.

## 7. Quality gates (self-check before reporting done)

- [ ] `figures/scheme_trxXX.svg` + exactly 4 PNGs exist, each PNG ≥ 2400 px wide.
- [ ] `monograph/monograph_EN.md` and `monograph_RU.md` ≥ 240 lines each.
- [ ] `README.md` ≥ 200 lines; `README_RU.md` ≥ 190 lines; headers mirror.
- [ ] Every number quoted in prose appears in `results/trxXX_results.json`.
- [ ] Script runs: `--smoke` (PASS, < 20 s), full (PASS), `--figures` (5 files).
- [ ] No emojis anywhere; no artificial “End of document” markers.
- [ ] Figures language English; prose languages correct and consistent.

## 8. Out of scope for study agents (maintainer-only files)

Do **not** modify: `research/README.md` (index), root `README.md`, site
generator / `docs/site/`, `MANIFEST.json`, `CHANGELOG*`, `CITATION.cff`,
`.zenodo.json`, `Makefile`, CI workflows, anything under `verification/`.
Those are updated in the integration pass.
