# TRIVORTEX Verification — Makefile

.PHONY: help run run-quick run-full lab lab-smoke test ports \
        rust rust-test cpp cpp-test haskell haskell-test \
        coq lean4 isabelle agda docker-build clean

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

lab: ## Open the interactive scientific laboratory (bilingual, 600 dpi)
	$(PYTHON) trivortex/python/lab.py

lab-smoke: ## Laboratory CI smoke: quick ladder + one dashboard figure
	$(PYTHON) trivortex/python/lab.py --smoke

test: ## Run the full pytest guard suite (core + research + ports)
	cd .. && $(PYTHON) -m pytest verification/tests/ -v --tb=short

common: ## Sanity check of the shared verifier package
	$(PYTHON) common/python/main.py --section 1 --preset default

# ── the multi-language ports (M1–M3) ─────────────────────────────────────

rust: ## Rust numeric twin: pinned-reference guard + quick ladder
	cargo test --release --manifest-path rust/Cargo.toml

rust-lab: ## Rust interactive laboratory (bilingual)
	cargo run --release --manifest-path rust/Cargo.toml

cpp: ## C++ port: CMake configure + build + CTest guard
	cmake -S cpp -B cpp/build -DCMAKE_BUILD_TYPE=Release
	cmake --build cpp/build -j
	ctest --test-dir cpp/build --output-on-failure

cpp-lab: ## C++ interactive laboratory (bilingual, benchmark at -O2)
	./cpp/build/trivortex-lab

haskell: ## Haskell dual ladder: cabal build + exact-anchor guard
	cd haskell && cabal build all && cabal test trivortex-guard

haskell-lab: ## Haskell interactive laboratory (Double vs ℚ(√3) dual)
	cd haskell && echo 0 | cabal run trivortex-lab

coq: ## Coq statement layer: coqc + Print Assumptions
	coqc coq/Trivortex.v

lean4: ## Lean 4 Mathlib formalization: lake build
	cd lean4 && lake build

isabelle: ## Isabelle HOL session build
	isabelle build -D isabelle

agda: ## Agda constructive module type-check
	agda agda/Trivortex.agda

docker-build: ## Build every pinned toolchain image (opportunistic)
	@for d in docker/*/; do \
		img="trivortex-$$(basename $$d)"; \
		echo "building $$img ..."; \
		docker build -t "$$img" "$$d" || echo "  (skipped: $$img)"; \
	done

clean: ## Remove generated outputs
	rm -rf outputs

.PHONY: run-check
run-check: ## Verify the Makefile parses
	@$(MAKE) -n run-quick >/dev/null && echo "Makefile OK"
