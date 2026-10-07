# TRIVORTEX Verification — Makefile

.PHONY: help run run-quick run-full test common docker-build clean

PYTHON ?= python3
COMPOSE ?= docker compose

help: ## Show help
	@echo "TRIVORTEX verification commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

run: ## Run the working ladder (default preset)
	$(PYTHON) trivortex/python/verify.py --preset default

run-quick: ## Fast smoke run (what CI executes)
	$(PYTHON) trivortex/python/verify.py --preset quick

run-full: ## Long integration, tighter grid (~35 s)
	$(PYTHON) trivortex/python/verify.py --preset full

test: ## Run the pytest guard suite (28 tests)
	cd .. && $(PYTHON) -m pytest verification/tests/ -v --tb=short

common: ## Sanity check of the shared verifier package
	$(PYTHON) common/python/main.py --section 1 --preset default

docker-build: ## Build every pinned toolchain image (opportunistic)
	@for d in docker/*/; do \
		img="trivortex-$$(basename $$d)"; \
		echo "building $$img ..."; \
		docker build -t "$$img" "$$d" || echo "  (skipped: $$img)"; \
	done

clean: ## Remove generated outputs
	rm -rf outputs
