# THE CYCLORING MONOGRAPH — the big book (RU + EN, md + docx + pdf)

The complete research narrative of the Gamma-period ring laboratory as
one volume, in two languages and three formats each:

| rendition | language | format | role |
|-----------|:--------:|--------|------|
| [`monograph_EN.md`](monograph_EN.md) | EN | Markdown | the committed source |
| [`monograph_EN.docx`](monograph_EN.docx) | EN | DOCX | the editable master (field TOC) |
| [`monograph_EN.pdf`](monograph_EN.pdf) | EN | PDF | the typeset, print-ready edition |
| [`monograph_RU.md`](monograph_RU.md) | RU | Markdown | the committed source |
| [`monograph_RU.docx`](monograph_RU.docx) | RU | DOCX | the editable master (field TOC) |
| [`monograph_RU.pdf`](monograph_RU.pdf) | RU | PDF | the typeset, print-ready edition |

## What is inside

The big monograph carries the whole program in one volume: the frozen
regular N-gon and the leading question; the five theorems (the root
system, the algebraic boundary, the defect chain, the synchronous
breathing, the dichotomy of the invariants) with statements, proofs and
protocol bindings; the W1–W7 ladder with its registered tolerance bands;
the registered level table of the levels 7/9/15/30; all five figures
embedded at 300 dpi; and the honesty chapter that separates the
certified from the recorded.

## The quoting rule

Every number printed in the monograph originates from the committed
protocols in [`../../results/protocols/`](../../results/protocols/).
The monograph is generated *after* the ladder runs and quotes the
protocols verbatim — it never recomputes, approximates or rounds beyond
the printed precision of its sources.

## The rendition pipeline

`monograph_<LANG>.md` → (pandoc + the navy-gold design system) →
`monograph_<LANG>.docx` → (LibreOffice headless) →
`monograph_<LANG>.pdf`. The DOCX carries proper field TOCs; the PDF is
its render — the identical pipeline as the parent repository's reading
room ([`publications/`](../../../publications/)).

The language rule: **RU and EN are separate volumes**, each with its own
page numbering and metadata — no half-translated book.
