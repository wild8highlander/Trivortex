# `results/crosslang/` — the C-vs-Python register diff

| file | what it is |
|------|-----------|
| [`crosslang_report.json`](crosslang_report.json) | the committed diff: 8 registers, tolerance $10^{-9}$ — **ALL PASSED** |

The registers: the group census (|GL| = 2016, |SL| = 336, |PSL| = 168),
the map registers (V = 56, E = 84, F = 24, Euler = −4, the antipodal
freeness), the 12-body register algebra (s, α, R, ℓ, r, A), the budget
residuals below the float tolerance in both languages, the C long-double
budget shadow at exactly 0.0, the 11 arc registers, the tilt
orthogonality and the 3D two-body Kepler anchor (1.0e−13).

Re-derive: `make crosslang`.
