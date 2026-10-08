# CYCLORING — the Python package

The package directory [`cycloring/`](cycloring/) holds the eight modules
of the mini-research program: the Gamma-period core, the defect chain,
the ring geometry, the Kirchhoff dynamics layer, the W-ladder, the JSON
runner and the bilingual figure factory. The parent directory
(`python/`) exists only to be put on `PYTHONPATH` — the package never
installs itself into site-packages, keeping the mini-research
self-contained and dependency-free.

## Why PYTHONPATH

All entry points of the mini-research assume `PYTHONPATH=python`:

```bash
# from the cycloring/ root
PYTHONPATH=python python3 python/cycloring/runner.py --stage W5 --preset default
PYTHONPATH=python python3 -m cycloring.figures --lang en
make ladder        # the Makefile sets PYTHONPATH for you
```

This is deliberate: the program ships as readable source inside the
repository, runs against plain `numpy` + `mpmath`, and leaves no build
artifacts behind. The same pattern the parent TRIVORTEX framework uses
for its verification ladder.

## The import contract

The dependency direction is strict and acyclic:

```text
periods → chain → ring → dynamics → ladder → runner / figures
```

Nothing in the package imports the parent TRIVORTEX framework at
runtime; the parent appears only in the test suite as the reference
oracle. See the module guide in
[`cycloring/README.md`](cycloring/README.md#9-the-module-guide) for the
per-module API table, and the package-level docstrings for the full
contracts.

## Quick module index

| module | role |
|--------|------|
| [`cycloring/periods.py`](cycloring/periods.py) | the Gamma-period core at 50 working digits (mpmath) |
| [`cycloring/chain.py`](cycloring/chain.py) | the defect chain and the transducer |
| [`cycloring/ring.py`](cycloring/ring.py) | the root system, characters, the breathing program |
| [`cycloring/dynamics.py`](cycloring/dynamics.py) | the Kirchhoff layer: RHS, RK4, invariants, Jacobian |
| [`cycloring/ladder.py`](cycloring/ladder.py) | the W1–W7 registered checks |
| [`cycloring/runner.py`](cycloring/runner.py) | the JSON protocol CLI |
| [`cycloring/figures.py`](cycloring/figures.py) | the bilingual figure factory (EN primary + RU mirror) |
| [`cycloring/__init__.py`](cycloring/__init__.py) | the package surface (re-exports) |

## Lint and typing

The package is covered by the mini-research lint scope
(`make lint` from the mini-research root): `black --check`, `ruff` and
`mypy --ignore-missing-imports`. CI runs the same checks — a PR that
passes locally passes remotely.
