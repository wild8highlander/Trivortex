# `js/` — the browser verifier (zero dependencies)

**One self-contained HTML file** that re-derives the bench's
load-bearing numbers in plain JavaScript — open it in any browser, no
network, no installs:

| file | what it does |
|------|--------------|
| [`verifier.html`](verifier.html) | ① the 10-check self-test battery (the 2401-matrix PSL census, the budget closure Σα = 8π, the hyperbolic Pythagoras, the tilt orthogonality, the Kepler anchor, the Poincaré-disk witness by bisection) ② **your own planet**: enter a GM (or mass in kg) — the exact register heptagon is computed and drawn on the Poincaré-disk canvas ③ the full 12-body register table with the budget line |

The JS core is a faithful port of `klein.py` + `spatial.py` (the
float64 shadow); its numbers match Python and C99 to the float64
roundoff — the Sun's register α = 1.9031343950, R = 0.9443455505 in
all three languages.
