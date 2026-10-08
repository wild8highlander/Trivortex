# TRX-07 — the monograph renditions

The typeset publication layer of the study **The Efimov Effect: Universal Quantum Three-Body Physics**: one
bilingual monograph, four renditions — Russian and English as separate
files, each in editable DOCX and typeset PDF.

## The files

| rendition | language | format |
|-----------|:--------:|--------|
| [`monograph_EN.md`](monograph_EN.md) | EN | Markdown — the committed source |
| [`monograph_EN.docx`](monograph_EN.docx) | EN | DOCX — the editable master (field TOC) |
| [`monograph_EN.pdf`](monograph_EN.pdf) | EN | PDF — the typeset, print-ready edition |
| [`monograph_RU.md`](monograph_RU.md) | RU | Markdown — the committed source |
| [`monograph_RU.docx`](monograph_RU.docx) | RU | DOCX — the editable master (field TOC) |
| [`monograph_RU.pdf`](monograph_RU.pdf) | RU | PDF — the typeset, print-ready edition |

The reading-room mirrors of the same documents live in
[`publications/pdf/`](../../../publications/pdf/) and
[`publications/docx/`](../../../publications/docx/) — byte-identical
copies committed by the build.

## What is inside

The full narrative of the study: the physical system and the preset
(§3), the governing equations (§4), the scheme (§5), the mapping to
TRIVORTEX (§6), the dimensionless formulation (§7), the numerical
method (§8), the verification protocol with every registered check
quoted (§9), the embedded figure gallery (§10), the results and their
analysis (§11–§12), the honest boundaries (§13) and the bibliography.

## The rendition discipline

- **RU and EN are separate volumes** — separate page numbering and
  metadata, no half-translated book;
- **the PDF is the LibreOffice render of the DOCX master**, both built
  from the committed Markdown by the navy-gold pipeline
  ([`publications/build/`](../../../publications/build/),
  `make pdf-library`);
- **protocol-bound numbers only** — every quantity quoted in the text
  comes from [`../results/`](../results/); the monograph never
  recomputes or approximates.
