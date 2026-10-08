# The build system — how the reading room is typeset

The reproducible build system behind `make pdf-library` (see the
repository root Makefile): it turns the committed Markdown sources into
the navy-gold PDF/DOCX renditions of the reading room — nothing is
recomputed, the documents typeset the committed results.

## The files

| file | role |
|------|------|
| [`md2html_lib.py`](md2html_lib.py) | the navy-gold design system: CSS, MathML rendering, cover pages, striped tables; renders through headless Chromium (Playwright) |
| [`build_pdf_library.py`](build_pdf_library.py) | builds the twelve study monographs (TRX-01…12) in RU and EN — PDF + DOCX each — into `../pdf/` and `../docx/` and mirrors them into the study folders |
| [`build_special_pdfs.py`](build_special_pdfs.py) | builds the core monograph and the research compendium — the two non-study volumes of the reading room |
| [`finalize_pdf.py`](finalize_pdf.py) | stamps PDF metadata (title, author, ORCID, DOI, keywords), QA-checks page counts and writes the final files |

## The pipeline, one document at a time

```text
../src/<doc>_<LANG>.md  ──pandoc──►  HTML (MathML, offline)
        ──Chromium print──►  styled PDF body
        ──navy-gold cover + page numbers──►  ../pdf/<doc>_<LANG>.pdf
        ──python-docx restyle──►  ../docx/<doc>_<LANG>.docx
        ──finalize_pdf.py──►  metadata + QA
```

## Requirements

Python ≥ 3.10 with `pypdf` and `python-docx`; `pandoc` ≥ 3.x on PATH;
Playwright's Chromium (the parent repository's dev container ships all
three). Rebuild everything from the repository root:

```bash
make pdf-library     # 28 PDFs + 28 DOCX, the whole reading room
```

## The invariants

- **nothing is recomputed** — the build reads committed Markdown and
  committed JSON protocols; a number in a PDF traces to a protocol, not
  to a run of the build;
- **RU and EN are separate renditions** — separate files, separate
  metadata, no half-translated volume;
- **the study folders receive mirrors** — every study monograph lands
  both in the reading room (`../pdf/`, `../docx/`) and next to its
  sources (`research/TRX-*/monograph/`), byte-identical.
