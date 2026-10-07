# TRIVORTEX — Working Verification Ladder

> The independent, dependency-light checker of the TRIVORTEX document.
> **Status: active (milestone M0).** This is the only directory in the
> framework whose artifacts are executed by CI today.

---

## What lives here

| Path | Contents |
|---|---|
| `python/verify.py` | the V1–V4 ladder: closed-form checks, Kirchhoff RK4 dynamics, JSON protocol, three presets |

## Why this is "independent" verification

`verify.py` shares **no code** with `code/trivortex_core*.py`. It
re-implements from scratch the objects it checks — the closed form of
Theorem 3.1, the Chaplygin combination `C_Ch = r²(θ̇ − q·A_θ)`, the
Kirchhoff right-hand side of point-vortex dynamics, and its own RK4
stepper. A regression in the core document's numerics therefore cannot
hide behind a shared helper: the ladder either reproduces the claims with
its own arithmetic or it fails loudly.

The full statement of the checks, the tolerance bands, the milestone
plan and the honesty notes live in the framework root:
[`verification/README.md`](../README.md).

## Quick start

```bash
# fast smoke run — what CI executes
python3 python/verify.py --preset quick

# default ladder (~2 s) and the long integration (~35 s)
python3 python/verify.py
python3 python/verify.py --preset full

# explicit JSON output directory
python3 python/verify.py --preset default --out-dir /tmp/trivortex
```

A healthy run ends with:

```text
  RESULT: 4/4 checks passed  (preset=default, wall time 2.18s)
  JSON report: .../trivortex_verify_default_2026-10-06_06-20-11.json
```

## The JSON protocol

Each run writes one file with the UTC date, the preset, the wall time and
per-check records (`check`, residuals, tolerances, `passed`, full
parameter snapshot). The schema is intentionally flat and stable so the
same reader works for the Python ladder and for every future language
port. Attach the JSON to any issue that reports a failing check — the
parameter snapshot makes the failure reproducible without asking a
single follow-up question.
