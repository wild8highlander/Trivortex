# .github — the repository automation

The GitHub-facing configuration: CI/CD workflows, issue/PR templates,
code owners, funding and the repository's automation metadata. The
pipeline design principle: **a green run is a claim held to a published
band** — every workflow enforces a registered criterion, never a vibe.

## The workflows (13)

| workflow | role |
|----------|------|
| [`workflows/ci.yml`](workflows/ci.yml) | every push: compile all Python (code/, verification/, research/, cycloring/, polyvortex/), the V1–V4 ladder (quick), the pytest guard, the W-ladders of the two mini-programs |
| [`workflows/lint.yml`](workflows/lint.yml) | markdownlint, yamllint, ruff, black, mypy |
| [`workflows/codeql.yml`](workflows/codeql.yml) | static security analysis of the Python code |
| [`workflows/deploy-docs.yml`](workflows/deploy-docs.yml) | publishes `docs/site/` verbatim to GitHub Pages |
| [`workflows/docker.yml`](workflows/docker.yml) | builds the seven pinned verification toolchains |
| [`workflows/verification-ports.yml`](workflows/verification-ports.yml) | runs all language ports (non-blocking; promotion policy in the verification README) |
| [`workflows/link-checker.yml`](workflows/link-checker.yml) | lychee over md/rst/html — dead links fail loudly |
| [`workflows/zenodo.yml`](workflows/zenodo.yml) | mints a new Zenodo DOI version on each GitHub release |
| [`workflows/release-drafter.yml`](workflows/release-drafter.yml) | assembles release notes from PRs |
| [`workflows/scorecard.yml`](workflows/scorecard.yml) | the OpenSSF supply-chain score |
| [`workflows/stale.yml`](workflows/stale.yml) | keeps the issue tracker alive |
| [`workflows/labeler.yml`](workflows/labeler.yml) | auto-labels PRs by changed paths |
| [`workflows/dependency-review.yml`](workflows/dependency-review.yml) | flags vulnerable dependencies on PRs |

## The rest of the folder

| path | role |
|------|------|
| [`ISSUE_TEMPLATE/`](ISSUE_TEMPLATE/) | the bug report and feature request forms, with the verification-protocol attachment field |
| [`PULL_REQUEST_TEMPLATE.md`](PULL_REQUEST_TEMPLATE.md) | the checklist: checks green, protocols attached |
| [`CODEOWNERS`](CODEOWNERS) | automatic reviewer routing for the core, verification and research trees |
| [`dependabot.yml`](dependabot.yml) | version pinning for the Actions and pip ecosystems |
| [`FUNDING.yml`](FUNDING.yml) | sponsorship links |
| [`labeler.yml`](labeler.yml) | the labeler's path→label mapping |
| [`badges/`](badges/) | committed badge payloads (the OpenSSF scorecard badge source) |

## Changing the automation

Workflow changes must keep the `permissions: contents: read` minimalism,
the concurrency groups and the explicit `workflow_dispatch` triggers.
YAML is linted by yamllint (`.yamllint.yml` at the root) — run it before
pushing; CI's own green badge is the repository's face.
