# The dev container — one-click reproducible environment

The Codespaces / Dev Containers specification for TRIVORTEX: open the
repository in GitHub Codespaces (or any Dev Containers-capable editor)
and land in a Python 3.12 environment with the full dependency set
already installed — clone-to-first-run in one step, no local setup.

## What the container provides

- **Python 3.12** — the newest line of the repository's support matrix
  (3.10 / 3.11 / 3.12);
- **the dependency floor preinstalled** — `numpy`, `scipy`,
  `matplotlib`, `mpmath`, `pytest`, plus the lint toolchain (`ruff`,
  `black`, `mypy`) and pre-commit;
- **docker-in-docker** — so the seven pinned verification toolchains
  ([`verification/docker/`](../verification/docker/)) build and run
  inside the same environment;
- **VS Code extensions** — the Python and Jupyter baselines.

## First commands inside the container

```bash
make verify-quick      # the V1–V4 ladder, quick preset (~0.5 s)
make test              # the pytest guard
cd cycloring && make ladder && make test     # the Gamma-period ring lab
cd polyvortex && make ladder && make test    # the N-vortex bench
python3 code/trivortex_core_en.py            # the interactive document
```

## The contract

The container pins the *environment*, not the results: every number it
produces comes from the registered checks and committed protocols, and
CI remains the arbiter of green. Changes to
[`devcontainer.json`](devcontainer.json) must keep the image
dependency-free of any result-affecting state — the container is a
workbench, never a source of numbers.
