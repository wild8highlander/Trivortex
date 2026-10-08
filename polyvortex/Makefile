# POLYVORTEX mini-repository — one-command discipline
# (mirrors the parent repository's Makefile style)

PYTHON ?= python3
PVPATH := python
PROTO_DIR := results/protocols

.PHONY: help ladder quick full test lint black ruff mypy figures protocols clean

help:
	@echo "POLYVORTEX — the N-vortex extension bench"
	@echo "  make ladder   - run W1..W7 (default preset), refresh protocols"
	@echo "  make quick    - 1.3 s smoke of the whole ladder (quick preset)"
	@echo "  make full     - long integration (full preset)"
	@echo "  make test     - the pytest guard (26 tests)"
	@echo "  make lint     - black --check + ruff + mypy (scoped)"
	@echo "  make figures  - regenerate figures/ (300 dpi PNG + scheme SVG)"
	@echo "  make clean    - remove caches"

ladder:
	PYTHONPATH=$(PVPATH) $(PYTHON) python/polyvortex/runner.py --preset default

quick:
	PYTHONPATH=$(PVPATH) $(PYTHON) python/polyvortex/runner.py --preset quick

full:
	PYTHONPATH=$(PVPATH) $(PYTHON) python/polyvortex/runner.py --preset full

figures:
	PYTHONPATH=$(PVPATH) $(PYTHON) -m polyvortex.figures

test:
	$(PYTHON) -m pytest tests/ -q

lint: black ruff mypy

black:
	black --check $(PVPATH)/ tests/

ruff:
	ruff check $(PVPATH)/ tests/

mypy:
	mypy $(PVPATH)/polyvortex --ignore-missing-imports --no-error-summary

clean:
	rm -rf .pytest_cache tests/__pycache__ $(PVPATH)/polyvortex/__pycache__
