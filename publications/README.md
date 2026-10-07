# TRIVORTEX Publications — the Reading Room

*TRIVORTEX Research Program · version 1.0.0 · PDF + DOCX library*

This folder is the reading room of the repository: every research artifact of
the program exists here as a typeset, vector, language-separated document with
a navy-gold cover, MathML-rendered equations, embedded 300-dpi figures, numbered
pages and document metadata. **Russian and English are separate files** — each
language can be read, printed and cited independently — and every document
exists in two renditions: a vector **PDF** and an editable **DOCX**. The library
is generated from the same markdown sources that live next to the code, so it
can be rebuilt from scratch at any time with one command.

## Contents

```text
publications/
├── pdf/                                        # 28 vector A4 PDFs
│   ├── TRX-01-laser-radiation-pressure_RU.pdf  # study monographs, Russian (12)
│   ├── TRX-01-laser-radiation-pressure_EN.pdf  # study monographs, English (12)
│   ├── …                                       # TRX-02 … TRX-12
│   ├── TRIVORTEX-Core-Monograph_RU.pdf         # the executable core as a book
│   ├── TRIVORTEX-Core-Monograph_EN.pdf
│   ├── TRIVORTEX-Research-Compendium_RU.pdf    # the program map
│   └── TRIVORTEX-Research-Compendium_EN.pdf
├── docx/                                       # the same 28 documents, editable
│   └── …                                       # identical naming, .docx suffix
├── html/                                       # 14 editable HTML sources (1:1)
├── src/                                        # markdown sources: core + compendium
├── build/                                      # the reproducible build system
│   ├── md2html_lib.py                          # navy-gold design system + renderer
│   ├── build_pdf_library.py                    # the twelve study monographs
│   ├── build_special_pdfs.py                   # core monograph + compendium
│   └── finalize_pdf.py                         # metadata stamping + QA
└── README.md                                   # this guide
```

Per-study renditions also live next to their sources:
`research/TRX-*/monograph/monograph_<LANG>.{pdf,docx}` — byte-identical to the
reading-room copies.

## The naming scheme

| Pattern | Example | Meaning |
|---|---|---|
| `TRX-<nn>-<slug>_<LANG>.pdf` | `TRX-09-vortex-trio_RU.pdf` | study monograph, Russian, typeset |
| `TRX-<nn>-<slug>_<LANG>.docx` | `TRX-09-vortex-trio_EN.docx` | study monograph, English, editable |
| `TRIVORTEX-Core-Monograph_<LANG>.pdf` | `TRIVORTEX-Core-Monograph_EN.pdf` | the executable core as a book |
| `TRIVORTEX-Research-Compendium_<LANG>.pdf` | `TRIVORTEX-Research-Compendium_RU.pdf` | the program map with every protocol |
| `monograph_<LANG>.{pdf,docx}` (study folders) | `monograph_RU.pdf` | the rendition next to its sources |

## What each study PDF contains

Every `TRX-<nn>_<LANG>.pdf` (10–14 pages) holds the complete monograph of one
study in one language: a navy-gold cover with metadata (author, ORCID, DOI,
sources, license), the ten-section monograph — abstract, introduction, physical
formulation, mathematical model, connection to the TRIVORTEX framework, numerical
method, results and analysis, discussion, conclusions — the parameter appendices,
and the four committed 300-dpi figures as a captioned gallery. Equations render
as MathML, tables keep their headers across page breaks, and page numbers follow
the standard scheme (cover unnumbered, body from 1).

## The core monograph

`TRIVORTEX-Core-Monograph_<LANG>.pdf` (~6 pages per language) is the executable
core `code/trivortex_core*.py` presented as a book: the model, the 22-section
architecture, Theorem 3.1 with its reference values, the Chaplygin integral with
its honesty note, the verification ladder V1–V4 with the certified results, the
menu and report engine, the astronomical presets and the reproduction protocol.
The result is a volume that can be read like a monograph and executed like a
program.

## The compendium

`TRIVORTEX-Research-Compendium_<LANG>.pdf` (~11 pages per language) is the
program-level map: a glance table of all twelve studies and one dossier per
study — the committed abstract plus the machine-readable acceptance protocol
(check, measured value, target, tolerance, verdict) quoted directly from the
results JSON. Nothing in the compendium is retyped by hand; it is assembled by
the build script from the committed protocols.

## Rebuilding

```bash
python3 publications/build/build_pdf_library.py     # the 12 study monographs ×4 renditions
python3 publications/build/build_special_pdfs.py    # core monograph + compendium ×4
# or everything at once:
make pdf-library
```

Dependencies: Python ≥ 3.10 with `pypdf` and `python-docx`; `pandoc` ≥ 3.x
(markdown → HTML with MathML, markdown → DOCX with native equations); Playwright's
Chromium (print-grade PDF rendering with stamped page numbers). The build is
fully offline: fonts are system Liberation families, equations never touch a CDN.
No study data is recomputed — the documents typeset the committed results. Each
PDF build stamps document metadata (title, author, subject, keywords) and
validates the page count before declaring success.

## What the DOCX renditions contain

The DOCX files are not afterthoughts — they are full editions for word
processors: native Word equations (pandoc converts LaTeX to OMML), embedded
300-dpi figures, restyled headings and tables in the navy-gold system, document
properties (title, author, subject, keywords) and Word page-number fields in the
footer. They are the versions you can annotate, translate further or excerpt
when preparing lectures and manuscripts.

## Design system

| Element | Value |
|---|---|
| Cover | full-bleed navy `#0A1A3A` → `#12264F` gradient, gold `#C9A227` rules |
| Wordmark | TRIVORTEX, letter-spaced small caps, gold |
| Headings | Liberation Sans, navy, gold underline on H1 |
| Body | Liberation Serif 10.2 pt, justified, hanging hyphens |
| Tables | navy header band, gold rule, zebra stripes |
| Figures | bordered, captioned, centered, max 92% width |
| Code blocks | navy panel, gold left border |
| Page footer | "TRIVORTEX Research Program · Version 1.0.0" + page N of M |

## How to cite a document from the library

Cite the repository through [`CITATION.cff`](../CITATION.cff)
(DOI 10.5281/zenodo.21825394) and name the exact rendition, e.g.:
"TRX-09 monograph, Russian edition, PDF" — the file's own metadata carries the
same information. Program author: Isaev Iskhak Khamzatovich
([ORCID 0009-0003-7299-0701](https://orcid.org/0009-0003-7299-0701)).
