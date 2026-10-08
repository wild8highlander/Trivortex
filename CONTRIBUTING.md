# Contributing to TRIVORTEX

First, thank you for considering a contribution to the **TRIVORTEX** project —
the study of the three-body (and N-body) problem in the vortex model with the
Chaplygin topological integral. This document explains what kinds of
contributions fit the repository, what the review contract is, and how to make
sure your number becomes part of the record rather than a bug report.

> **The one-line contract:** *criteria first, code second; JSON protocol or it
> did not happen.*

---

## Table of contents

1. [What this repository accepts](#1-what-this-repository-accepts)
2. [Ground rules](#2-ground-rules)
3. [Reporting a verification result](#3-reporting-a-verification-result)
4. [Proposing a language port (M1–M3)](#4-proposing-a-language-port-m1m3)
5. [Improving the document](#5-improving-the-document)
6. [Documentation and site changes](#6-documentation-and-site-changes)
7. [Development setup](#7-development-setup)
8. [Commit and PR conventions](#8-commit-and-pr-conventions)
9. [Review process](#9-review-process)
10. [Licensing of contributions](#10-licensing-of-contributions)

---

## 1. What this repository accepts

| Kind of contribution | Where it lands | Typical size |
|---|---|---|
| Independent verification results (reproduced numbers) | issue + JSON protocol attachment | small |
| New checks for the ladder (`V5`, `V6`, …) | `verification/trivortex/python/verify.py` + criteria | medium |
| Language ports of the ladder (Coq, Lean4, Rust, …) | `verification/<language>/` | large |
| New sections of the document (Section 23+) | `code/trivortex_core*.py`, all three mirrors | large |
| Bug fixes with a failing-check demonstration | anywhere | small |
| Documentation, site pages, SVG artwork | `docs/`, `*.md` | small–medium |

Out of scope: gravitational three-body ephemeris simulations (the presets are
configuration, not simulation targets), rewrites that change the physics without
a registered criterion, and any content for the retired research directions
(git history and Zenodo keep them; the main branch does not).

## 2. Ground rules

1. **Registered criteria.** Every checkable claim gets its pass/fail criterion
   written in `verification/README.md` *before* the check is implemented.
   Retrospective criteria are how confirmation bias gets into a repository.
2. **Independence.** Ladder code shares no imports with
   `code/trivortex_core*.py`. If you find yourself importing the document to
   verify the document, stop and re-derive.
3. **Certified vs recorded.** Keep the boundary the ladder enforces:
   window-dependent diagnostics (like the C_Ch endpoint drift) are *recorded*;
   only window-independent statements are *certified*. See
   [`verification/README.md §13`](verification/README.md#13-honesty-notes).
4. **All three mirrors move together.** Structural changes to the document
   (new sections, changed numbering) land in
   `trivortex_core.py`, `trivortex_core_ru.py` and `trivortex_core_en.py` in
   one commit.
5. **Respect the license.** The repository is proprietary
   (`LicenseRef-Proprietary-Wild8Highlander-1.0`); by opening a PR you agree
   that your contribution is offered under the same license
   ([§10](#10-licensing-of-contributions)).

## 3. Reporting a verification result

Reproduced the ladder? Excellent — open an issue titled
`verification result: <preset> on <platform>` and attach:

1. the JSON protocol from your run
   (`python3 verification/trivortex/python/verify.py --preset default` writes it
   automatically);
2. your platform line (`python3 -c "import sys, numpy; print(sys.version,
   numpy.__version__)"`);
3. any residual that differed from the reference table, even if it still
   passed.

Residuals that sit *below* the reference values are as interesting as
failures: they tell us where the tolerance bands are loose and should be
tightened.

## 4. Proposing a language port (M1–M3)

The roadmap lives in [`verification/README.md §7`](verification/README.md#7-multi-language-roadmap-and-milestones).
Each language directory already contains a roadmap README with the scope (the
same three objects for every port) and acceptance criteria. To claim one:

1. open an issue `port: <language>` naming the milestone you target;
2. the plan in the directory README is the contract — amend it in the same PR
   that lands the artifacts, never after;
3. pin the toolchain as `verification/docker/<language>/Dockerfile`;
4. land with a JSON protocol from a real run (the same schema as the Python
   ladder) and flip the status table in `verification/README.md` in the same
   commit;
5. a port starts **non-blocking** in CI; it becomes blocking after three
   consecutive green days.

## 5. Improving the document

The document is `code/trivortex_core*.py` — an executable monograph, and its
style rules are strict for good reasons:

- new experiments become **Section 23+** in all three mirrors simultaneously;
- results go into a Section-3-style result container so the report engine
  picks them up in all seven formats without per-format code;
- the section numbering is citable and must not be reshuffled;
- keep the module docstring's provenance note (the former name and the Julia
  twin reference) — they are history, not decoration.

Performance work is welcome when it does not change numbers: if an optimization
moves a residual by more than the tolerance band, that is a *new result* and
needs a registered criterion.

## 6. Documentation and site changes

The documentation site is plain HTML/CSS in `docs/site/` (published by
`deploy-docs.yml`, no build step) and the SVG assets are generated by scripts
under version control in the repository history (`docs/assets/`). When editing
pages, keep the shared stylesheet (`assets/css/style.css`) as the single source
of visual identity — navy and gold are not optional. Validate HTML structure
before submitting (any tag-balance checker will do).

## 7. Development setup

```bash
git clone https://github.com/wild8highlander/Trivortex.git
cd Trivortex
python -m pip install numpy scipy matplotlib mpmath pytest ruff
make test              # the pytest guard (28 tests)
make verify-quick      # the ladder, CI preset
make run               # the interactive document
```

The CI pipeline (`.github/workflows/ci.yml`) runs exactly this ladder + pytest
on Python 3.10–3.12; run it locally first and your PR is halfway green.

## 8. Commit and PR conventions

- Commit messages follow the Conventional Commits style enforced by
  `.commitlintrc.json` — `feat:`, `fix:`, `docs:`, `verification:`, `code:`.
- One logical change per PR; a PR that lands a port must include the artifacts,
  the status-table flip and the JSON protocol.
- PRs use the template under `.github/PULL_REQUEST_TEMPLATE.md`; fill the
  checklist honestly — "criteria registered before implementation" is a checkbox
  a reviewer will actually verify.

## 9. Review process

1. A maintainer (see `CODEOWNERS`) triages within a few days;
2. for verification contributions, the reviewer re-runs your protocol locally —
   the parameter snapshot must make this possible without questions;
3. for ports, the reviewer checks the acceptance criteria line by line against
   the directory README;
4. squash-merge with a conventional commit message; the release notes are
   drafted automatically (`release-drafter.yml`) and every release is deposited
   to Zenodo (`zenodo.yml`) with a versioned DOI.

## 10. Licensing of contributions

By submitting a pull request you grant the copyright holder the right to
include your contribution in the repository and in any derived edition under
`LicenseRef-Proprietary-Wild8Highlander-1.0`. Attribution is given in the
release notes and, for substantial contributions, in `AUTHORS.md`.
