# Workflows — the CI/CD Catalogue

> **Navigation:** [`.github`](../../README.md) › **`workflows`**

![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)
![CI](https://img.shields.io/github/actions/workflow/status/wild8highlander/Trivortex/ci.yml?branch=main&style=flat-square&label=CI)
![Docs](https://img.shields.io/github/actions/workflow/status/wild8highlander/Trivortex/deploy-docs.yml?branch=main&style=flat-square&label=Docs%20Deploy)

The **GitHub Actions catalogue** of the TRIVORTEX repository (version 1.0.1) —
12 YAML workflow definitions covering the verification, documentation, security
and release lifecycle. Every workflow is idempotent, uses pinned action versions
and requires no secrets beyond the built-in `GITHUB_TOKEN` (the Zenodo
publisher optionally accepts `ZENODO_TOKEN` for DOI automation).

## The catalogue

| Workflow | Triggers | Purpose |
|---|---|---|
| [`ci.yml`](ci.yml) | push / PR to `main` | ★ **TRIVORTEX CI** — syntax check of every Python file (3.10–3.12), the independent verification ladder V1–V4 (`verify.py --preset quick`) with the JSON protocol uploaded as an artifact, and the 28-test pytest guard |
| [`lint.yml`](lint.yml) | push / PR to `main` | markdownlint + yamllint + ruff/black over the sources + CITATION.cff validation |
| [`codeql.yml`](codeql.yml) | push / PR / schedule | CodeQL static security analysis of the Python code |
| [`deploy-docs.yml`](deploy-docs.yml) | push touching `docs/site/**`, releases, manual | publishes the static documentation site to GitHub Pages verbatim (no Jekyll; `.nojekyll` committed) |
| [`docker.yml`](docker.yml) | push touching `verification/docker/**`, manual | builds the seven pinned verification toolchains |
| [`zenodo.yml`](zenodo.yml) | published release | uploads the source archive to Zenodo via the Invenio API and updates the deposit metadata — mints the versioned DOI |
| [`scorecard.yml`](scorecard.yml) | schedule / push | OpenSSF Scorecard supply-chain posture assessment (refreshes `.github/badges/scorecard-badge.json`) |
| [`dependency-review.yml`](dependency-review.yml) | pull_request | blocks PRs that introduce vulnerable or prohibited dependencies |
| [`link-checker.yml`](link-checker.yml) | schedule / manual | validates links across the documentation and site pages |
| [`labeler.yml`](labeler.yml) | pull_request | auto-labels PRs by changed paths (`.github/labeler.yml`) |
| [`stale.yml`](stale.yml) | schedule | marks and closes inactive issues/PRs after a period of silence |
| [`release-drafter.yml`](release-drafter.yml) | push / PR | drafts release notes and versions from merged PRs |

## The CI job in detail

`ci.yml` is the contract that keeps the science honest. Three jobs, all on
`ubuntu-latest`:

1. **Syntax check** — `py_compile` over every Python file under `code/`,
   `verification/` and `research/` on Python 3.10, 3.11 and 3.12 (fail-fast
   disabled: the matrix reports all breakages at once).
2. **Verification ladder** — `verify.py --preset quick` (~0.5 s); the JSON
   protocol is uploaded as the `trivortex-verify-protocol` artifact
   (retention 30 days). If a single check fails, the job exits non-zero.
3. **Pytest guard** — the full `verification/tests/` suite: 13 reference-value
   pins for Theorem 3.1, 12 study smoke runs, the completeness, library and
   companion-volume tests — 28 tests total.

## Contract

- **The ladder must stay green.** `ci.yml` runs the V1–V4 checks on every
  push; a red ladder is a release blocker, not a warning.
- **JSON or it did not happen.** The ladder job uploads the JSON protocol of
  every run (retention 30 days) — the artifact is the reproducibility record.
- **Docs deploy on touch.** Any change under `docs/site/**` republishes the
  Pages site automatically; the deployment is a pure static upload with
  concurrency lock (`group: "pages"`, in-progress cancelled).
- **Release chain.** A published release triggers the Zenodo mint; the release
  notes are drafted by release-drafter from the merged PRs.

## Local equivalents

The CI steps are reproducible locally through the root Makefile:

```bash
make verify-quick   # the ladder, quick preset (what CI runs)
make test           # the 28-test pytest guard
make lint           # ruff over code/ + verification/
```
