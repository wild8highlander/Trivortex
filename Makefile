# TRIVORTEX — Top-level Makefile

.PHONY: help install run run-ru run-en verify verify-quick verify-full test mini-test mini-ladders mini-figures cycloring-ladder cycloring-test polyvortex-ladder polyvortex-test planetvortex-ladder planetvortex-hardcore planetvortex-vregister planetvortex-crosslang planetvortex-test docs docs-serve lint clean

.DEFAULT_GOAL := help

PYTHON ?= python3

help: ## Show help
        @echo "TRIVORTEX — Makefile commands"
        @echo ""
        @grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
        awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies
        $(PYTHON) -m pip install numpy scipy matplotlib mpmath pytest ruff
        @echo "Optional: pip install -e '.[dev]' for pre-commit and linting"

run: ## Run the interactive document (EN console, default mirror)
        cd code && $(PYTHON) trivortex_core.py

run-ru: ## Run the interactive document (RU mirror)
        cd code && $(PYTHON) trivortex_core_ru.py

run-en: ## Run the interactive document (EN mirror)
        cd code && $(PYTHON) trivortex_core_en.py

verify: ## Run the independent verification ladder (default preset)
        $(PYTHON) verification/trivortex/python/verify.py --preset default

verify-quick: ## Fast ladder smoke run (~0.5 s, what CI runs)
        $(PYTHON) verification/trivortex/python/verify.py --preset quick

verify-full: ## Long ladder run with tight integration (~35 s)
        $(PYTHON) verification/trivortex/python/verify.py --preset full

test: ## Run the pytest guard (27 tests)
        $(PYTHON) -m pytest verification/tests/ -v --tb=short

mini-test: ## Run all three mini-program guards (37 cycloring + 26 polyvortex + 80 planetvortex tests)
        $(PYTHON) -m pytest cycloring/tests/ polyvortex/tests/ planetvortex/tests/ -v --tb=short

mini-ladders: ## Run all mini-program ladders W+P+X+V (default preset, refresh protocols)
        cd cycloring && PYTHONPATH=python $(PYTHON) python/cycloring/runner.py --preset default
        cd polyvortex && PYTHONPATH=python $(PYTHON) python/polyvortex/runner.py --preset default
        cd planetvortex && PYTHONPATH=python $(PYTHON) python/planetvortex/runner.py --suite all --preset default

mini-figures: ## Regenerate all three mini-program figure sets (EN primary + RU mirror)
        cd cycloring && PYTHONPATH=python $(PYTHON) -m cycloring.figures
        cd polyvortex && PYTHONPATH=python $(PYTHON) -m polyvortex.figures
        cd planetvortex && PYTHONPATH=python $(PYTHON) -m planetvortex.figures

cycloring-ladder: ## CYCLORING: run W1..W7 (default preset)
        cd cycloring && PYTHONPATH=python $(PYTHON) python/cycloring/runner.py --preset default

cycloring-test: ## CYCLORING: the pytest guard (37 tests)
        cd cycloring && $(PYTHON) -m pytest tests/ -q

polyvortex-ladder: ## POLYVORTEX: run W1..W7 (default preset)
        cd polyvortex && PYTHONPATH=python $(PYTHON) python/polyvortex/runner.py --preset default

polyvortex-test: ## POLYVORTEX: the pytest guard (26 tests)
        cd polyvortex && $(PYTHON) -m pytest tests/ -q

planetvortex-ladder: ## PLANETVORTEX: run P1..P7 (default preset)
        cd planetvortex && PYTHONPATH=python $(PYTHON) python/planetvortex/runner.py --suite p --preset default

planetvortex-hardcore: ## PLANETVORTEX: run X1..X6, the hardcore X-register (default preset)
        cd planetvortex && PYTHONPATH=python $(PYTHON) python/planetvortex/runner.py --suite x --preset default

planetvortex-vregister: ## PLANETVORTEX: run V1..V2, the spatial V-register (default preset)
        cd planetvortex && PYTHONPATH=python $(PYTHON) python/planetvortex/runner.py --suite v --preset default

planetvortex-crosslang: ## PLANETVORTEX: the three-language oracle (C99 build + run vs Python)
        cd planetvortex && make -C c clean run > /dev/null
        cd planetvortex && PYTHONPATH=python $(PYTHON) tools/crosslang_diff.py

planetvortex-test: ## PLANETVORTEX: the pytest guard (80 tests)
        cd planetvortex && $(PYTHON) -m pytest tests/ -q

docs: ## Preview hint for the documentation site
        @echo "Serving docs/site at http://localhost:8080 ..."
        $(PYTHON) -m http.server 8080 -d docs/site

docs-serve: docs

lint: ## Ruff over the Python sources
        $(PYTHON) -m ruff check code/ verification/ --ignore=E501,E402,F401,F841

clean: ## Remove generated outputs and caches
        rm -rf verification/outputs
        find . -name "__pycache__" -type d -prune -exec rm -rf {} \; 2>/dev/null || true

research-smoke: ## Run all twelve studies in CI smoke mode
        @for d in research/TRX-*/code/*.py; do \
        echo "== $$d"; $(PYTHON) "$$d" --smoke || exit 1; done

research-full: ## Run all twelve studies in full mode
        @for d in research/TRX-*/code/*.py; do \
        echo "== $$d"; $(PYTHON) "$$d" || exit 1; done

research-figures: ## Run all twelve studies in full mode + ultra-res figures
        @for d in research/TRX-*/code/*.py; do \
        echo "== $$d"; $(PYTHON) "$$d" --figures || exit 1; done

animations: ## Regenerate the four orbital animations (GIF + MP4)
        $(PYTHON) docs/animations/make_animations.py

pdf-library: ## Rebuild the 14 bilingual publication PDFs (12 studies + core + compendium)
        $(PYTHON) publications/build/build_pdf_library.py
        $(PYTHON) publications/build/build_special_pdfs.py
