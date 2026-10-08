# CYCLORING mini-research — one-command discipline

PYTHON ?= python3
PVPATH := python
PROTO_DIR := results/protocols

.PHONY: help ladder quick full test lint black ruff mypy figures protocols clean

help:
	@echo "CYCLORING — the Gamma-period ring laboratory"
	@echo "  make ladder   - run W1..W7 (default preset), refresh protocols"
	@echo "  make quick    - fast smoke of the whole ladder (quick preset)"
	@echo "  make full     - long integration (full preset)"
	@echo "  make test     - the pytest guard (37 tests)"
	@echo "  make lint     - black --check + ruff + mypy (scoped to this mini-research)"
	@echo "  make figures  - regenerate figures/ (300 dpi PNG + scheme SVG)"
	@echo "  make clean    - remove caches"

ladder:
	PYTHONPATH=$(PVPATH) $(PYTHON) python/cycloring/runner.py --preset default

quick:
	PYTHONPATH=$(PVPATH) $(PYTHON) python/cycloring/runner.py --preset quick

full:
	PYTHONPATH=$(PVPATH) $(PYTHON) python/cycloring/runner.py --preset full

figures:
	PYTHONPATH=$(PVPATH) $(PYTHON) -m cycloring.figures

test:
	$(PYTHON) -m pytest tests/ -q

lint: black ruff mypy

black:
	black --check $(PVPATH)/ tests/

ruff:
	ruff check $(PVPATH)/ tests/

mypy:
	mypy $(PVPATH)/cycloring --ignore-missing-imports --no-error-summary

clean:
	rm -rf .pytest_cache tests/__pycache__ $(PVPATH)/cycloring/__pycache__
