# The Markdown sources — the committed masters of the special volumes

The Markdown sources of the two special volumes of the reading room —
the documents that are not study monographs and therefore live outside
the per-study trees:

| source | renditions | what it is |
|--------|------------|------------|
| the core monograph source | [`../pdf/TRIVORTEX-Core-Monograph_RU.pdf`](../pdf/) · `…_EN.pdf` · the DOCX pair | the executable document (`code/trivortex_core*.py`) as a book: the 22 sections, the menu, the report engine |
| the research compendium source | [`../pdf/TRIVORTEX-Research-Compendium_RU.pdf`](../pdf/) · `…_EN.pdf` · the DOCX pair | the program map: all twelve studies, every acceptance protocol quoted verbatim |

## Why sources live here

The twelve **study** monographs keep their sources next to their data in
`research/TRX-*/monograph/` — the study tree is the unit of
reproduction. The two **special** volumes span the whole program, so
their sources live here, next to the build system that renders them
([`../build/`](../build/)).

## The rendering contract

The sources are plain Markdown with `$…$`/`$$…$$` math; the build
renders the math to MathML **offline** (no CDN, no network at build
time), paints the navy-gold design through headless Chromium and stamps
metadata. Rebuild:

```bash
make pdf-library     # from the repository root
```

The committed PDF/DOCX renditions in `../pdf/` and `../docx/` are
products of these sources plus committed figures and protocols — a
change to a source without a matching renditions commit is a build
debt, and CI's link checker plus the release process keep that honest.
