# The PDF shelf — 28 typeset volumes (RU and EN separate)

The typeset heart of the reading room: 28 vector A4 PDFs covering the
whole program, each citable, printable and addressable without opening
it — the naming scheme is the catalog.

## The shelf map

| pattern | count | meaning |
|---------|------:|---------|
| `TRX-<nn>-<slug>_<LANG>.pdf` | 24 | the twelve study monographs × RU/EN, e.g. [`TRX-09-vortex-trio_EN.pdf`](TRX-09-vortex-trio_EN.pdf) |
| `TRIVORTEX-Core-Monograph_<LANG>.pdf` | 2 | the executable document as a book |
| `TRIVORTEX-Research-Compendium_<LANG>.pdf` | 2 | the program map with every acceptance protocol quoted |

The DOCX twins of every file live in [`../docx/`](../docx/) — same
content, editable.

## The design contract

Navy-gold covers carrying the study metadata (author, ORCID, DOI,
sources, license); MathML equations rendered offline; 300-dpi figures
embedded with captions; striped tables with repeating headers; page
numbers stamped by the renderer (cover unnumbered, body from 1); PDF
metadata (title, author, keywords) consistent with
[`CITATION.cff`](../../CITATION.cff) and `.zenodo.json`.

## Rebuild

```bash
make pdf-library     # 28 PDFs + 28 DOCX from committed sources
```

The build ([`../build/`](../build/)) reads the committed Markdown,
figures and protocols — nothing is recomputed. The PDFs typeset
committed results; a number in a PDF traces to a protocol JSON, and the
compendium quotes every protocol in full.
