# TRIVORTEX — repository assets

The shared visual assets of the repository: the banners, dividers,
schemes and showcase figures the READMEs and the documentation site
embed. Everything here is a committed, diffable source file (SVG) or a
build product (PNG) — no screenshots, no binaries of unknown origin.

## The inventory

| asset | role | used by |
|-------|------|---------|
| [`banner-hero.svg`](banner-hero.svg) | the monumental navy-and-gold header of the root README | root README |
| [`banner-cycloring.svg`](banner-cycloring.svg) | the header banner of the Gamma-period ring laboratory | `cycloring/README.md` (+ RU mirror) |
| [`banner-polyvortex.svg`](banner-polyvortex.svg) | the header banner of the N-vortex extension bench | `polyvortex/README.md` (+ RU mirror) |
| [`logo-trivortex.svg`](logo-trivortex.svg) | the program mark: three intertwined vortex rings over the Lagrange triangle | root README, sub-program READMEs |
| [`divider-gold.svg`](divider-gold.svg) | the gold ornament divider | READMEs across the repository |
| [`title-page.svg`](title-page.svg) | the title page artwork | publications design |
| [`orbits-showcase.svg`](orbits-showcase.svg) | three choreographies in one panel (figure-eight, Lagrange triangle, unequal circulations) | root README §1 |
| [`social-preview.png`](social-preview.png) / [`.svg`](social-preview.svg) | the GitHub social preview card | repository settings |
| [`ladder-accuracy.png`](ladder-accuracy.png) | recorded residuals against registered tolerance bands (log scale) | root README §5 |
| [`program-checks-dashboard.png`](program-checks-dashboard.png) | all 80 registered acceptance checks across the twelve studies, all PASS | root README §11 |

## The design system

One visual family across the repository: the navy gradient
(`#0E2145 → #0A1730`), the gold accents (`#D4AF37`), the steel/sky
blues (`#2E5FA3`, `#7FA6D9`), the crimson `#B03A2E` for warnings, the
soft grid `#D5DCE8`. The matplotlib figures of the mini-programs and
the research studies use the same palette (`figures.py` modules), so
README galleries, monographs and banners render as one brand.

## Editing

SVGs are hand-editable and hand-edited — keep them dependency-free
(no external fonts beyond the DejaVu family, no rasters, no scripts).
PNGs are build products: regenerate them from their scripts, never
overwrite by hand. The social preview is wired in the repository
settings (Settings → Social preview) and renders at 1280×640.
