# TRIVORTEX — Verification Framework

> The multi-language skeleton that keeps every number in the TRIVORTEX
> document honest: one working Python verification ladder today, seven
> pinned toolchains and a formalization roadmap around it.

![Status](https://img.shields.io/badge/ladder-V1%E2%80%93V4%20%E2%9C%93%204%2F4-2EA043?style=flat-square)
![Tests](https://img.shields.io/badge/pytest-28%20passed-2EA043?style=flat-square&logo=pytest)
![Languages](https://img.shields.io/badge/toolchains-7%20pinned-2496ED?style=flat-square&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)

---

## Table of contents

1. [What this framework is for](#1-what-this-framework-is-for)
2. [What survives from the previous edition](#2-what-survives-from-the-previous-edition)
3. [Directory layout](#3-directory-layout)
4. [The working Python ladder (today)](#4-the-working-python-ladder-today)
5. [The V1–V4 checks in detail](#5-the-v1v4-checks-in-detail)
6. [Tolerance bands](#6-tolerance-bands)
7. [Multi-language roadmap and milestones](#7-multi-language-roadmap-and-milestones)
8. [Docker toolchains](#8-docker-toolchains)
9. [How to reproduce everything](#9-how-to-reproduce-everything)
10. [How to contribute a new language](#10-how-to-contribute-a-new-language)
11. [The 27-test pytest guard in detail](#11-the-27-test-pytest-guard-in-detail)
12. [The JSON protocol schema](#12-the-json-protocol-schema)
13. [Honesty notes](#13-honesty-notes)
14. [Frequently asked questions](#14-frequently-asked-questions)

---

## 1. What this framework is for

The TRIVORTEX document — [`code/trivortex_core*.py`](../code/README.md) —
makes a small set of sharp, checkable claims about the three-body (and
N-body) problem in the vortex model: a closed-form rotating solution
(Theorem 3.1), a topological integral attributed to Chaplygin, and the
classical conservation laws of point-vortex dynamics. Numbers that are
only ever printed by the code that defines them are not verification;
they are repetition. This framework exists to break that circularity: the
checks live in **independent code** (`trivortex/python/verify.py` shares
no imports with the core document), run in a CI job on every push, emit
JSON protocols with full parameter snapshots, and are mapped onto a
multi-language port plan so that a future refactor cannot silently move
the goalposts.

Three principles govern the framework, inherited from the previous
edition of this repository and kept deliberately:

- **Every number is bound to a run.** Each check reports its residual,
  its tolerance, its parameter snapshot and its wall time; the JSON
  report is the single source of truth for the README tables.
- **Both outcomes are results.** A check that returns *effect* and a
  check that returns *strict bound* are equally valid science; what is
  not acceptable is an unclear criterion. Every criterion here is
  registered in advance in this README.
- **Skeletons are labelled as skeletons.** Directories whose artifacts
  have not landed yet say so in their first line. Nothing in this
  repository pretends to be verified when it is merely planned.

---

## 2. What survives from the previous edition

The repository is a single-direction research program (TRIVORTEX
v1.0.0) around the three-body vortex document. In `verification/`, the
**infrastructure** is organized for one purpose — keeping the program's
claims honest:

| Component | Status | Role under TRIVORTEX |
|---|---|---|
| `docker/` — 7 pinned toolchain images | **kept as-is** | same images, now aimed at Theorem 3.1 ports |
| `common/python/` — verifier base + config | **kept, config re-targeted** | shared verifier protocol for future sections |
| `tests/` — pytest suite | **rebuilt** | 27 tests guarding V1–V4, the analytic layer and the research program |
| section directories (`section1…section6`) | **removed** | belonged to the retired research lines (KdV, AB-Cloud, Klein, Riemann) |
| `python_levels/`, `julia_levels/` (L1–L5) | **removed** | legacy per-language verification chains |
| `api/`, `demo/`, `web-dashboard/`, `notebooks/` | **removed** | superseded by the static documentation site |
| per-language ports (Coq, Lean4, …) | **roadmap stubs** | see [section 7](#7-multi-language-roadmap-and-milestones) |

If you are looking for the retired multi-topic verification chains
(KdV, AB-Cloud, Klein, Riemann): they remain reachable in
git history and in the Zenodo record 10.5281/zenodo.21825394.

---

## 3. Directory layout

```text
verification/
├── README.md                  ← this document
├── Makefile                   ← thin wrapper: run, test, docker targets
├── CODEOWNERS                 ← review routing per language directory
├── trivortex/                 ← ★ the working ladder (milestone M0)
│   ├── README.md              ← what it checks and why it is independent
│   └── python/
│       └── verify.py          ← V1–V4, JSON protocol, presets
├── tests/                     ← pytest suite (27 tests, ~20 s)
│   ├── README.md
│   └── test_trivortex.py
├── common/                    ← shared verifier protocol (kept)
│   └── python/
│       ├── verifier_base.py   ← BaseVerifier: banner, ledger, JSON verdict
│       ├── config.py          ← presets + section registry (re-targeted)
│       └── main.py            ← aggregate CLI
├── docker/                    ← 7 pinned toolchains (kept)
│   ├── agda/  coq/  cpp/  haskell/
│   ├── isabelle/  lean4/  rust/
│   └── README.md
├── coq/    README.md          ← roadmap stub (M1)
├── lean4/  README.md          ← roadmap stub (M1)
├── isabelle/ README.md        ← roadmap stub (M2)
├── agda/   README.md          ← roadmap stub (M2)
├── rust/   README.md          ← roadmap stub (M1)
├── cpp/    README.md          ← roadmap stub (M3)
└── haskell/ README.md         ← roadmap stub (M3)
```

---

## 4. The working Python ladder (today)

`trivortex/python/verify.py` is a self-contained script (~450 lines with
documentation) whose only dependency is `numpy`. It re-implements, from
scratch, the objects it checks — the closed form of Theorem 3.1, the
Chaplygin combination, the Kirchhoff right-hand side and a classical RK4
stepper — so a bug in `code/trivortex_core*.py` cannot hide inside a
shared helper. The ladder has three presets:

| Preset | Rotations | Steps/period | C_Ch probes | Typical wall time |
|---|---|---|---|---|
| `quick` | 2 | 2 000 | 200 | ~0.5 s |
| `default` | 5 | 4 000 | 1 000 | ~2 s |
| `full` | 20 | 8 000 | 2 000 | ~35 s |

```bash
python3 verification/trivortex/python/verify.py                 # default
python3 verification/trivortex/python/verify.py --preset quick  # CI mode
python3 verification/trivortex/python/verify.py --preset full --out-dir /tmp/rep
```

Every invocation writes a JSON protocol (`suite`, `preset`, UTC date,
per-check residuals and parameter snapshots, wall time) — the same
"numbers are bound to runs" discipline the repository has used since its
first release.

---

## 5. The V1–V4 checks in detail

### V1 — Theorem 3.1: choreography and periodicity of the closed form

The document's analytic solution places the three vortices at angles
`θ_k(t) = ωt + 2πk/3` — an equilateral triangle rotating rigidly — with a
radial modulation `r_k(t) = √C_Ch·(1 + ε·cos(ωt + 2πk/3))`. Two properties
are checked as pass/fail criteria: the **angular separation stays exactly
`2π/3`** (residual `≤ 1e-12`) at all probed times, and the closed form is
**periodic** with `T_r = 2π/ω` (residual `≤ 1e-12`). The endpoint drift of
the gauge-dependent combination `C_Ch(t) = r²(θ̇ − q·A_θ)` — the quantity
recorded by Section 6 of the core document — is reported as a *diagnostic*
with no pass/fail role, because by construction it oscillates with the
radial modulation; see [section 13](#13-honesty-notes).

### V2 — Rigid rotation at the Lagrange angular velocity

Three equal point vortices on an equilateral triangle of side `a` are
integrated with RK4 over several full rotations. The classical result —
the point-vortex twin of the Lagrange equilateral solution of the
three-body problem — is that the triangle rotates rigidly with
`ω = 3Γ/(2πa²)`. The check pins both the **shape** (relative side drift
`≤ 1e-10`) and the **frequency** (measured vs analytic, relative error
`≤ 1e-6`). The angle unwrapping lifts the raw `atan2` difference to the
branch closest to the expected unwrapped angle, so whole turns are
handled exactly.

### V3 — Conservation of the vortex integrals (equal circulations)

Along the V2 trajectory, the four classical invariants of point-vortex
dynamics are monitored: the Hamiltonian `H = −(1/2π)Σ_{i<j} ΓᵢΓⱼ ln rᵢⱼ`,
the linear impulses `P = ΣΓx`, `Q = ΣΓy`, and the angular impulse
`I = ΣΓ|r|²`. These are the many-body conservation laws of the model —
the Chaplygin-type integrals for vortex systems. Relative drift `≤ 1e-10`
per quantity.

### V4 — Robustness with unequal circulations

The same conservation statement for `Γ = (1, 2, 3)` started from a
generic (non-symmetric) triangle: the integrals do not require the
symmetric initial condition. Relative drift `≤ 1e-10`. Together V3+V4
demonstrate that the conservation laws are properties of the *equations*,
not artifacts of the equilateral choreography.

---

## 6. Tolerance bands

| Band | Applies to | Rationale |
|---|---|---|
| `1e-12` | closed-form residuals (V1) | argument reduction of `cos`, transcendental round-off in float64 |
| `1e-10` | RK4 invariants and shape (V2–V4) | fourth-order truncation at `dt = T/2000` dominates |
| `1e-6` | measured angular velocity (V2) | finite-step integration of the angle over multiple turns |

Tolerances are registered here and in `verify.py` **before** a check is
written; a test whose residual sits far below its band gets a tighter
band, because a check that cannot fail protects nothing.

---

## 7. Multi-language roadmap and milestones

The framework keeps seven pinned toolchains (Docker) and grows ports of
the same three objects — closed form, Chaplygin combination, vortex
integrals — language by language. Every port states its acceptance
criteria in its directory README *before* the artifacts land.

| Language directory | Artifact target | Milestone | Status |
|---|---|---|---|
| `trivortex/python/` | working ladder V1–V4 + JSON | **M0** | ✅ **done** (this release) |
| `tests/` | pytest guard of the ladder + program | **M0** | ✅ **done** (27 tests) |
| `coq/` | `Trivortex.v` — statement layer + choreography | **M1** | planned — skeleton |
| `lean4/` | `Trivortex.lean` — choreography + periodicity via Mathlib | **M1** | planned — skeleton |
| `rust/` | crate — second floating-point implementation of V1–V4 | **M1** | planned — skeleton |
| `isabelle/` | `Trivortex.thy` — SMT-discharged invariant bounds | **M2** | planned — skeleton |
| `agda/` | `Trivortex.agda` — constructive angle arithmetic | **M2** | planned — skeleton |
| `cpp/` | CMake/CTest port + `-O2` benchmark of the ladder | **M3** | planned — skeleton |
| `haskell/` | `Double` vs exact-rational dual run of the ladder | **M3** | planned — skeleton |

Milestone definitions:

- **M0 — independent ladder** *(this release)*: one language runs all
  four checks in CI with JSON protocols.
- **M1 — independent re-derivation**: a second proof assistant and a
  second floating-point language reproduce the closed-form properties
  and the ladder numbers.
- **M2 — cross-checked statements**: two proof assistants prove the same
  statement layer with disjoint axiom sets; Isabelle SMT closes the
  drift bounds.
- **M3 — performance & exactness**: compiled benchmark ladder and an
  exact-arithmetic split of the residual budget.

---

## 8. Docker toolchains

One image per toolchain, each a thin layer over the official base image:

| Image | Base | Pins |
|---|---|---|
| `docker/coq/` | `rocq/rocq` | Coq/Rocq 8.18, standard Reals stack |
| `docker/lean4/` | Lean community image | elan + lake, toolchain file |
| `docker/isabelle/` | `makarius/isabelle` | Isabelle-HOL 2024 session env |
| `docker/agda/` | `agda/agda` | Agda 2.6 + standard library |
| `docker/rust/` | `rust` | stable ≥ 1.75, Cargo cache mounted |
| `docker/cpp/` | `gcc` | GCC + CMake, C++17 |
| `docker/haskell/` | `haskell` | GHC 9.4 + cabal |

Build and run any of them with the recipe in the corresponding language
README (see [section 3](#3-directory-layout) for the paths). The CI builds
images opportunistically via `docker.yml`; until milestone M1, a failing
formal toolchain never blocks `main`.

---

## 9. How to reproduce everything

```bash
# 1. the working ladder (three presets)
python3 verification/trivortex/python/verify.py --preset quick
python3 verification/trivortex/python/verify.py --preset default
python3 verification/trivortex/python/verify.py --preset full

# 2. the pytest guard
python -m pytest verification/tests/ -v

# 3. the shared protocol CLI (sanity of the kept common package)
python3 verification/common/python/main.py --section 1 --preset default

# 4. any pinned toolchain
docker build -t trivortex-coq verification/docker/coq
```

Environment: Python ≥ 3.10, `numpy ≥ 1.24` (see `pyproject.toml`);
everything else is optional. On a laptop, the whole section 1–2 takes
under five seconds.

---

## 10. How to contribute a new language

1. Open an issue titled `port: <language>` describing which of the three
   objects (closed form / Chaplygin / integrals) you target and which
   milestone it belongs to.
2. Copy the structure of an existing roadmap README: *why this language*,
   *scope*, *acceptance criteria*, *build recipe* — criteria first, code
   second.
3. Pin the toolchain as a new `docker/<language>/Dockerfile`; never rely
   on unpinned system packages.
4. Land the port with a JSON protocol produced by a real run (the same
   schema as the Python ladder) and flip the status table here in the
   same commit.
5. Keep the CI contract: a port may be added as *non-blocking*; turning a
   port blocking requires a green run on three consecutive days.

The review rules live in [`CONTRIBUTING.md`](../CONTRIBUTING.md); code
ownership per directory in [`verification/CODEOWNERS`](CODEOWNERS).

---

## 11. The 27-test pytest guard in detail

`verification/tests/` is the CI-friendly wrapper around the whole program.
It needs only `numpy` and `pytest`, runs in ≈ 20 s, and contains 27 tests:

| Suite | Tests | Guards |
|---|---|---|
| `test_trivortex.py` — analytic pins | 13 | Theorem 3.1 reference values: ω = 1.3748022274393588, ε = 0.7276379117656014 (exact to float64), periodicity of the closed form, C_Ch formula shape, the quick-preset ladder in-process, JSON protocol shape |
| `test_research_smoke.py` — study smoke | 12 | every TRX-01…12 script executes in `--smoke` mode, exits 0, and its committed protocol reports `status: PASS` |
| `test_research_smoke.py` — completeness | 1 | every study ships README, code, pack, scheme SVG, four 300-dpi figures, monograph sources and the four monograph renditions (PDF+DOCX × RU/EN) |
| `test_research_smoke.py` — library | 1 | the reading room: 28 PDFs + 28 DOCX + HTML sources + the four build-system scripts |

The reference constants are *pinned, not assumed*: each expected value is
computed from the closed form inside the test itself, so the suite fails if the
formula — not just the implementation — drifts.

---

## 12. The JSON protocol schema

Every ladder run writes a self-describing protocol; the same schema is shared
by the research studies:

```json
{
  "suite": "trivortex-verification",
  "version": "1.0",
  "preset": "quick",
  "date_utc": "2026-10-07T05:57:30+00:00",
  "wall_time_s": 0.53,
  "checks_passed": 4,
  "checks_total": 4,
  "all_passed": true,
  "checks": [
    {
      "check": "V1 Theorem 3.1: choreography + periodicity ...",
      "passed": true,
      "angular_separation_error": 6.9e-14,
      "angular_separation_tolerance": 1e-12,
      "params": {"C_Ch": 1.0, "T": 6.283185307179586, "...": "..."}
    }
  ]
}
```

| Field | Meaning |
|---|---|
| `preset` | which registered parameter set ran (`quick` / `default` / `full`) |
| `checks_passed` / `checks_total` | the verdict at a glance |
| `checks[].passed` | per-check verdict against the registered tolerance |
| `checks[].params` | the full parameter snapshot — the protocol is reproducible from the file alone |
| `date_utc`, `wall_time_s` | provenance of the run |

---

## 13. Honesty notes

- The Section-6 drift diagnostic of the core document is **recorded, not
  hidden**: the combination `C_Ch(t) = r²(θ̇ − q·A_θ)` with `A_θ = 1/r`
  oscillates together with the radial modulation, so its endpoint drift
  depends on the integration window. The window-independent conserved
  quantities of the model are the vortex integrals `H, P, Q, I` — and
  those are what V3/V4 certify. This separation between *recorded
  diagnostics* and *certified invariants* is deliberate and applies to
  every language port.
- The roadmap stubs contain **plans, not results**; each of them says so
  in its first line. Status tables elsewhere in the repository must not
  quote a stub as a verification.
- The reference constants used by the pytest suite (e.g.
  `ω = 1.3748022274393588` for `C_Ch = 1`) are computed from the closed
  form in the test itself — they are *pinned*, not *assumed*.

---

## 14. Frequently asked questions

**Q: Why does the ladder not import the document?**
Because a checker that shares code with the checked cannot certify it. The
ladder re-implements the closed form, the Kirchhoff right-hand side and its own
RK4 stepper from the published formulas — the only things shared are the
mathematics and the numbers.

**Q: Which preset should I run?**
`quick` (~0.5 s) is what CI runs on every push; `default` (~2 s) is the local
workhorse; `full` (~35 s) is for release validation and tighter integration
grids. The registered tolerances hold for all three.

**Q: A check failed — what now?**
Attach the JSON protocol to an issue. The protocol carries the full parameter
snapshot, so the failure is reproducible without a single follow-up question.
If the failure involves a research study, attach that study's
`results/trxNN_results.json` too.

**Q: Can I add a V5 check?**
Yes — the contract is in section 10: register the criterion (statement,
tolerance, preset) in this README *before* the code lands, keep it independent
of the core document, emit the same JSON schema, and pin reference values in
the pytest suite.

**Q: What do the roadmap stubs contain?**
Plans, not results — and each says so in its first line. A stub quotes
acceptance criteria and the toolchain pin it will use; it never quotes a
verification result. Status tables elsewhere in the repository must not treat
a stub as a verification.
