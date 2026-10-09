# PLANETVORTEX — the Python package

The package directory [`planetvortex/`](planetvortex/) holds the eight
modules of the planetary gravity-geometry bench: the planetary
registers layer (Layer P), the PSL(2,7) figure layer (Layer F), the
Kirchhoff vortex lattice (Layer V), the Newtonian N-body layer
(Layer N), the P-ladder, the JSON runner and the figure factory. The
parent directory (`python/`) exists only to be put on `PYTHONPATH` —
the bench ships as readable source and never installs into
site-packages.

## Why PYTHONPATH

All entry points assume `PYTHONPATH=python`:

```bash
# from the planetvortex/ root
PYTHONPATH=python python3 python/planetvortex/runner.py --stage P4 --preset default
PYTHONPATH=python python3 -m planetvortex.figures
make ladder        # the Makefile sets PYTHONPATH for you
```

The same pattern the parent TRIVORTEX framework and the sibling
mini-repositories ([`cycloring`](../../cycloring/python/README.md),
[`polyvortex`](../../polyvortex/python/README.md)) use.

## The import contract

Strict and acyclic:

```text
fano (Layer F) ──► classical (Layer P) ──► model (V) / nbody (N) ──┐
                                                                    ├──► ladder ──► runner / figures
```

Nothing imports the parent framework or the sibling benches at
runtime; they are imported only by the test suite as the reference
oracles.

## Quick module index

| module | role |
|--------|------|
| [`planetvortex/classical.py`](planetvortex/classical.py) | Layer P: the NASA register, Kepler III, Schwarzschild, Hill, the gravity ladder |
| [`planetvortex/fano.py`](planetvortex/fano.py) | Layer F: PSL(2,7) in two models, the exact figure, the closed forms |
| [`planetvortex/model.py`](planetvortex/model.py) | Layer V: Kirchhoff RHS, RK4, invariants, Jacobian, the co-rotating spectrum |
| [`planetvortex/nbody.py`](planetvortex/nbody.py) | Layer N: the Sun + 8-planets integrator, osculating elements, conservation |
| [`planetvortex/ladder.py`](planetvortex/ladder.py) | the P1–P7 registered checks |
| [`planetvortex/runner.py`](planetvortex/runner.py) | the JSON protocol CLI |
| [`planetvortex/figures.py`](planetvortex/figures.py) | the figure factory (300 dpi, protocol-bound) |
| [`planetvortex/__init__.py`](planetvortex/__init__.py) | the package surface (re-exports) |

## Lint and typing

Covered by the mini-repo lint scope (`make lint`): `black --check`,
`ruff`, `mypy --ignore-missing-imports`. CI runs the same checks — a
PR that passes locally passes remotely.
