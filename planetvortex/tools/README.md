# `tools/` — the auxiliary pipeline

| script | what it does |
|--------|--------------|
| [`crosslang_diff.py`](crosslang_diff.py) | runs the C99 kernel and pins every shared register against Python (8/8 at $10^{-9}$); writes `results/crosslang/crosslang_report.json` |
| [`editions_v.py`](editions_v.py) | generates the V-editions (Theorem F, Lemma F, Theorem G, Lemma G) as Markdown, then renders DOCX (pandoc, the house navy-gold styles) and PDF (LibreOffice headless) |
| [`stage_monographs.py`](stage_monographs.py) | generates the 15 × 2 per-stage point monographs into `docs/monographs/stages/`, each bound to the committed protocol |

```bash
make crosslang        # = make -C c && PYTHONPATH=python python3 tools/crosslang_diff.py
PYTHONPATH=python python3 tools/editions_v.py
make stage-monographs # = PYTHONPATH=python python3 tools/stage_monographs.py
```
