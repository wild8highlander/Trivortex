# `docs/monographs/` — the theorem editions

**One point monograph per theorem/lemma, in Russian and English, in
DOCX and PDF** (the V-editions also carry their Markdown sources) —
rendered by the house pipeline: pandoc with the polyvortex
navy-gold reference styles, then LibreOffice headless.

## The planar editions (stages P1–P7)

| edition | EN | RU |
|---------|----|----|
| Theorem A — the exact dimensions of the figure | [docx](PLANETVORTEX-TheoremA_EN.docx) / [pdf](PLANETVORTEX-TheoremA_EN.pdf) | [docx](PLANETVORTEX-TheoremA_RU.docx) / [pdf](PLANETVORTEX-TheoremA_RU.pdf) |
| Theorem B — the seven equal cells | [docx](PLANETVORTEX-TheoremB_EN.docx) / [pdf](PLANETVORTEX-TheoremB_EN.pdf) | [docx](PLANETVORTEX-TheoremB_RU.docx) / [pdf](PLANETVORTEX-TheoremB_RU.pdf) |
| Theorem C — the rigid heptagon lattice | [docx](PLANETVORTEX-TheoremC_EN.docx) / [pdf](PLANETVORTEX-TheoremC_EN.pdf) | [docx](PLANETVORTEX-TheoremC_RU.docx) / [pdf](PLANETVORTEX-TheoremC_RU.pdf) |
| Lemma D — the Kepler register and the mass correction | [docx](PLANETVORTEX-LemmaD_EN.docx) / [pdf](PLANETVORTEX-LemmaD_EN.pdf) | [docx](PLANETVORTEX-LemmaD_RU.docx) / [pdf](PLANETVORTEX-LemmaD_RU.pdf) |
| Lemma E — the mass-ladder deficit | [docx](PLANETVORTEX-LemmaE_EN.docx) / [pdf](PLANETVORTEX-LemmaE_EN.pdf) | [docx](PLANETVORTEX-LemmaE_RU.docx) / [pdf](PLANETVORTEX-LemmaE_RU.pdf) |

## The V-editions (stages V1–V2, new in 2.0 — with `.md` sources)

| edition | EN | RU |
|---------|----|----|
| Theorem F — the coset construction of the Klein map | [md](PLANETVORTEX-TheoremF_EN.md) · [docx](PLANETVORTEX-TheoremF_EN.docx) / [pdf](PLANETVORTEX-TheoremF_EN.pdf) | [md](PLANETVORTEX-TheoremF_RU.md) · [docx](PLANETVORTEX-TheoremF_RU.docx) / [pdf](PLANETVORTEX-TheoremF_RU.pdf) |
| Lemma F — the antipodal freeness | [md](PLANETVORTEX-LemmaF_EN.md) · [docx](PLANETVORTEX-LemmaF_EN.docx) / [pdf](PLANETVORTEX-LemmaF_EN.pdf) | [md](PLANETVORTEX-LemmaF_RU.md) · [docx](PLANETVORTEX-LemmaF_RU.docx) / [pdf](PLANETVORTEX-LemmaF_RU.pdf) |
| Theorem G — the budget closure (the capstone) | [md](PLANETVORTEX-TheoremG_EN.md) · [docx](PLANETVORTEX-TheoremG_EN.docx) / [pdf](PLANETVORTEX-TheoremG_EN.pdf) | [md](PLANETVORTEX-TheoremG_RU.md) · [docx](PLANETVORTEX-TheoremG_RU.docx) / [pdf](PLANETVORTEX-TheoremG_RU.pdf) |
| Lemma G — the arc register of the spatial tilt | [md](PLANETVORTEX-LemmaG_EN.md) · [docx](PLANETVORTEX-LemmaG_EN.docx) / [pdf](PLANETVORTEX-LemmaG_EN.pdf) | [md](PLANETVORTEX-LemmaG_RU.md) · [docx](PLANETVORTEX-LemmaG_RU.docx) / [pdf](PLANETVORTEX-LemmaG_RU.pdf) |

## The per-stage point monographs

The 15 stages of the three suites have their own compact monographs
(both languages), each bound to the committed protocol:
[`stages/`](stages/) — regenerate with `make stage-monographs`.

Regenerate the V-editions with
`PYTHONPATH=python python3 tools/editions_v.py`.
The formal corpus with the full proofs:
[`docs/theorems/`](../theorems/).
