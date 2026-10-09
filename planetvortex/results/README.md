# `results/` — the committed evidence

| folder | contents |
|--------|----------|
| [`protocols/`](protocols/) | the 15 committed JSON protocols (P1–P7, X1–X6, V1–V2, default preset) — one deterministic file per stage, regenerated identically by `make all-ladders` |
| [`crosslang/`](crosslang/) | the C99-vs-Python register diff (8/8 PASS at $10^{-9}$) — `make crosslang` |
| [`generated/`](generated/) | the monograph generator's committed samples (EN + RU + the Kepler-452b custom-body edition) — `make monograph` |
| [`runs/`](runs/) | the durable run records (the disk-patch geometry, the register tables, the closure registers) |

Every file here is regenerable from the committed pipeline; the
tolerances were committed before the recorded runs.
