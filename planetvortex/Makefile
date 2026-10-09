# PLANETVORTEX mini-repository — one-command discipline
# (mirrors the parent repository's Makefile style)

PYTHON ?= python3
PVPATH := python
PROTO_DIR := results/protocols

.PHONY: help ladder hardcore vregister all-ladders quick full test lint black ruff mypy figures figures600 animations crosslang monograph verify-all stage-monographs clean

help:
	@echo "PLANETVORTEX — the planetary gravity-geometry bench"
	@echo "  make ladder   - run P1..P7 (default preset), refresh protocols"
	@echo "  make hardcore - run X1..X6, the hardcore X-register (default)"
	@echo "  make vregister - run V1..V2, the spatial + Klein V-register (default)"
	@echo "  make all-ladders - P-ladder + X-register + V-register back to back"
	@echo "  make full     - long integration (full preset)"
	@echo "  make test     - the pytest guard (52 tests)"
	@echo "  make lint     - black --check + ruff + mypy (scoped)"
	@echo "  make figures  - regenerate figures/ (300 dpi PNG + scheme SVG)"
	@echo "  make figures600 - regenerate figures/600dpi/ (600 dpi, per task)"
	@echo "  make animations - regenerate the GIF animations"
	@echo "  make crosslang  - build the C kernel and cross-check against Python"
	@echo "  make monograph  - generate the sample monographs (md/docx/pdf)"
	@echo "  make stage-monographs - regenerate the per-stage point monographs"
	@echo "  make verify-all - all suites + pytest + the C cross-check"
	@echo "  make clean    - remove caches"

ladder:
	PYTHONPATH=$(PVPATH) $(PYTHON) python/planetvortex/runner.py --suite p --preset default

hardcore:
	PYTHONPATH=$(PVPATH) $(PYTHON) python/planetvortex/runner.py --suite x --preset default

vregister:
	PYTHONPATH=$(PVPATH) $(PYTHON) python/planetvortex/runner.py --suite v --preset default

all-ladders:
	PYTHONPATH=$(PVPATH) $(PYTHON) python/planetvortex/runner.py --suite all --preset default

figures600:
	PYTHONPATH=$(PVPATH) $(PYTHON) -m planetvortex.pubfigures --dpi 600

animations:
	PYTHONPATH=$(PVPATH) $(PYTHON) -m planetvortex.pubfigures --animations

crosslang:
	$(MAKE) -C c
	PYTHONPATH=$(PVPATH) $(PYTHON) tools/crosslang_diff.py

monograph:
	PYTHONPATH=$(PVPATH) $(PYTHON) -m planetvortex.cli monograph --bodies "Sun,Jupiter,Saturn,Earth" --lang en --format all
	PYTHONPATH=$(PVPATH) $(PYTHON) -m planetvortex.cli monograph --bodies "Sun,Jupiter,Saturn,Earth" --lang ru --format all

stage-monographs:
	PYTHONPATH=$(PVPATH) $(PYTHON) tools/stage_monographs.py

verify-all: all-ladders
	$(PYTHON) -m pytest tests/ -q
	$(MAKE) crosslang

quick:
	PYTHONPATH=$(PVPATH) $(PYTHON) python/planetvortex/runner.py --suite all --preset quick

full:
	PYTHONPATH=$(PVPATH) $(PYTHON) python/planetvortex/runner.py --preset full

figures:
	PYTHONPATH=$(PVPATH) $(PYTHON) -m planetvortex.figures

test:
	$(PYTHON) -m pytest tests/ -q

lint: black ruff mypy

black:
	black --check $(PVPATH)/ tests/

ruff:
	ruff check $(PVPATH)/ tests/

mypy:
	mypy $(PVPATH)/planetvortex --ignore-missing-imports --no-error-summary

clean:
	rm -rf .pytest_cache tests/__pycache__ $(PVPATH)/planetvortex/__pycache__
