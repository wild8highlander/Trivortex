# PLANETVORTEX — the documentation

The publication stack of the planetary gravity-geometry bench: the big
research monograph and the theorem editions, in Russian and English.

```text
docs/
├── monograph/     ← THE BIG MONOGRAPH: monograph_RU|EN.{md,docx,pdf}
└── monographs/    ← THEOREM EDITION: Theorems A, B, C; Lemmas D, E
                     (PLANETVORTEX-<item>_{RU,EN}.docx / .pdf, 20 files)
```

## Which document to read first

- **the monograph** ([`monograph/`](monograph/)) — the full science:
  the two layers of the bench, the three theorems and two lemmas with
  proofs, the seven-stage P-ladder, the planetary simulation and the
  honesty boundaries;
- **the theorem editions** ([`monographs/`](monographs/)) — one short
  dossier per statement (statement, proof, protocol binding), for
  citation and for the formalization queue.

## The rendition discipline

The Russian and English monographs are **separate files**, each
complete, not machine mirrors of one another: the prose is authored in
its language, while the numbers, tables and figures are identical and
protocol-bound. The DOCX files are the editable masters (proper field
TOCs, the navy-gold design), the PDF files are the LibreOffice render
of the very same DOCX — the parent repository's pipeline:

```text
monograph_<LANG>.md  →  (pandoc + navy-gold design)  →  .docx
                                             .docx  →  (LibreOffice headless)  →  .pdf
```

Every document quotes only protocol-bound numbers from
[`../results/protocols/`](../results/protocols/) — the same numbers
the READMEs and the figures quote. A number that no protocol carries
does not appear in any document.
