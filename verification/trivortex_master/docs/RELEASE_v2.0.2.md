# v2.0.2 — English documentation release (2026-11-24)

A documentation patch release (details in CHANGELOG.md): the entire
README surface is now **English** — the root README (rewritten and
enriched: collapsible accelerator table, FAQ, roadmap timeline,
contributing rules) plus all ten subfolder READMEs. The acceptance
check A10 is language-neutral (accepts `profile` or `профил`). The
asset gallery gains three new real-run charts: Poincare sections of
the Henon-Heiles potential, the Lambda-CDM distance ladder, and a
color-magnitude view of the 25 brightest stars; all banner and chart
titles are translated, and the SVG chip text is XML-escaped. Full
quality gate of both editions — **PASSED**.

- **96 modules**, 115 classes, 632 functions; ~56990 lines; docstring coverage 66%
- catalog: **538 objects** (asteroid: 20, comet: 10, dwarf_planet: 5, exoplanet: 440, moon: 29, planet: 8, star: 16, synthetic: 10)
- scene presets: **20**; menu modes: **73** in 11 categories
- selftest S1–S24: ✓ 24/24 · acceptance A1–A20: 20/20 · quality gate: 49/49 + hygiene clean

## Удвоение против v1.0.0

| Метрика | v1.0.0 | v2.0.0 | × |
|---|---|---|---|
| модули | 44 | 96 | ×2.18 ✓ |
| классы | 60 | 115 | ×1.92 |
| функции | 250 | 632 | ×2.53 ✓ |
| строки | 11776 | 56990 | ×4.84 ✓ |
| каталог | 258 | 538 | ×2.09 ✓ |
| пресеты | 10 | 20 | ×2.00 ✓ |
| режимы меню | 21 | 73 | ×3.48 ✓ |

*Не все метрики удвоены — см. таблицу.*
