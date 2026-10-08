# POLYVORTEX — the Python package

The package directory [`polyvortex/`](polyvortex/) holds the seven
modules of the N-vortex extension bench: the Kirchhoff dynamics layer
(Layer K), the closed-form ansatz layer (Layer G), the classical N-gon
registers, the W-ladder, the JSON runner and the figure factory. The
parent directory (`python/`) exists only to be put on `PYTHONPATH` —
the bench ships as readable source and never installs into
site-packages.

## Why PYTHONPATH

All entry points assume `PYTHONPATH=python`:

```bash
# from the polyvortex/ root
PYTHONPATH=python python3 python/polyvortex/runner.py --stage W4 --preset default
PYTHONPATH=python python3 -m polyvortex.figures
make ladder        # the Makefile sets PYTHONPATH for you
```

The same pattern the parent TRIVORTEX framework and the sibling
mini-research [`cycloring`](../../cycloring/python/README.md) use.

## The import contract

Strict and acyclic:

```text
classical ──► model (Layer K) ──┐
            └► ansatz (Layer G) ─┴──► ladder ──► runner / figures
```

Nothing imports the parent framework at runtime; the parent is imported
only by the test suite as the reference oracle.

## Quick module index

| module | role |
|--------|------|
| [`polyvortex/model.py`](polyvortex/model.py) | Layer K: Kirchhoff RHS, RK4, invariants, Jacobian, co-rotating spectrum |
| [`polyvortex/ansatz.py`](polyvortex/ansatz.py) | Layer G: the H1 closed form, the π ln 2 threshold, the Chaplygin diagnostic |
| [`polyvortex/classical.py`](polyvortex/classical.py) | the N-gon relative equilibria: ω_N, chords, unwrap |
| [`polyvortex/ladder.py`](polyvortex/ladder.py) | the W1–W7 registered checks |
| [`polyvortex/runner.py`](polyvortex/runner.py) | the JSON protocol CLI |
| [`polyvortex/figures.py`](polyvortex/figures.py) | the figure factory (300 dpi, protocol-bound) |
| [`polyvortex/__init__.py`](polyvortex/__init__.py) | the package surface (re-exports) |

## Lint and typing

Covered by the mini-repo lint scope (`make lint`): `black --check`,
`ruff`, `mypy --ignore-missing-imports`. CI runs the same checks — a PR
that passes locally passes remotely.
