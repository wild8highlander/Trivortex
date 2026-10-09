#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
PLANETVORTEX — THE CROSS-LANGUAGE DIFF (C99 vs Python)
============================================================================
Runs the C kernel (c/gravikernel) and pins every shared register
against the Python layer of the bench:

    group      |GL| = 2016, |SL| = 336, |PSL| = 168, the census
    map        V = 56, E = 84, F = 24, Euler = -4, antipodal freeness
    algebra    s_i, alpha_i, R_i, l_i, r_i, A_i for the 12 bodies and
               the budget residuals (double + long double)
    spatial    the tilt orthogonality, the arc registers

Registered tolerance: 1e-9 relative on every float register (the two
languages agree to the float64 roundoff; the C long double shadow is
reported for the budget closure).

Usage:
    PYTHONPATH=python python3 tools/crosslang_diff.py [--kernel c/gravikernel]

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MINIROOT = HERE.parent
sys.path.insert(0, str(MINIROOT / "python"))

from planetvortex import classical as cl  # noqa: E402
from planetvortex import klein as kl  # noqa: E402
from planetvortex import spatial as sp  # noqa: E402

TOLERANCE = 1e-9


def rel(a: float, b: float) -> float:
    return abs(a - b) / max(abs(b), 1e-300)


def main() -> int:
    ap = argparse.ArgumentParser(description="the C-vs-Python register diff")
    ap.add_argument("--kernel", default=str(MINIROOT / "c" / "gravikernel"))
    ap.add_argument(
        "--out", default=str(MINIROOT / "results" / "crosslang" / "crosslang_report.json")
    )
    args = ap.parse_args()

    kernel = Path(args.kernel)
    if not kernel.exists():
        print(f"kernel not found: {kernel} — run `make -C c` first", file=sys.stderr)
        return 2
    raw = subprocess.run([str(kernel)], capture_output=True, text=True, check=True).stdout
    c = json.loads(raw)

    checks: list = []

    def expect(name: str, ok: bool, detail: dict) -> None:
        checks.append({"register": name, "passed": bool(ok), "detail": detail})

    # -- the group -------------------------------------------------------
    expect(
        "group_census",
        (c["group"]["gl2_7"], c["group"]["sl2_7"], c["group"]["psl2_7"]) == (2016, 336, 168),
        {k: c["group"][k] for k in ("gl2_7", "sl2_7", "psl2_7")},
    )
    expect(
        "map_registers",
        (c["map"]["V"], c["map"]["E"], c["map"]["F"], c["map"]["euler"]) == (56, 84, 24, -4)
        and c["map"]["face_fixed_points"] == 0,
        c["map"],
    )

    # -- the register algebra --------------------------------------------
    algebra = kl.register_algebra_float()
    bodies = {row["body"]: row for row in algebra["bodies"]}
    worst = 0.0
    worst_name = ""
    for row in c["register_algebra"]["bodies"]:
        py = bodies[row["body"]]
        for key in ("s", "alpha", "circumradius", "edge", "inradius", "area"):
            r = rel(float(row[key]), py[key])
            if r > worst:
                worst, worst_name = r, f"{row['body']}.{key}"
    expect("register_algebra_12_bodies", worst <= TOLERANCE, {"worst_rel": worst, "at": worst_name})

    # the budget residuals are float64 roundoff noise (~1e-14): the
    # register is their ABSOLUTE size against the float tolerance, in
    # both languages independently
    expect(
        "budget_residuals_below_tolerance",
        float(c["register_algebra"]["alpha_sum_residual"]) <= TOLERANCE
        and float(c["register_algebra"]["total_area_residual"]) <= TOLERANCE
        and algebra["alpha_sum_residual"] <= TOLERANCE
        and algebra["total_area_residual"] <= TOLERANCE,
        {
            "c_alpha": float(c["register_algebra"]["alpha_sum_residual"]),
            "c_area": float(c["register_algebra"]["total_area_residual"]),
            "py_alpha": algebra["alpha_sum_residual"],
            "py_area": algebra["total_area_residual"],
        },
    )
    expect(
        "budget_closure_exact_c_long_double",
        float(c["register_algebra"]["ld_alpha_sum_residual"]) <= 1e-15,
        {"ld_alpha_sum_residual": float(c["register_algebra"]["ld_alpha_sum_residual"])},
    )

    # -- the spatial registers -------------------------------------------
    rows = sp.inclination_register()
    py_arcs = {row["body"]: row["arc_au"] for row in rows}
    worst_arc = 0.0
    for row in c["inclination_register"]:
        r = rel(float(row["arc"]), py_arcs[row["body"]])
        worst_arc = max(worst_arc, r)
    expect("arc_registers_11_bodies", worst_arc <= TOLERANCE, {"worst_rel": worst_arc})
    expect(
        "tilt_orthogonality",
        float(c["spatial"]["worst_orthogonality"]) <= sp.V1_TOLERANCES["tilt_orthogonality"] * 10,
        c["spatial"],
    )
    expect(
        "kepler_anchor",
        float(c["spatial"]["earth_period_anchor_rel"]) <= 1e-9,
        c["spatial"],
    )

    # -- the report -------------------------------------------------------
    all_ok = all(ch["passed"] for ch in checks)
    report = {
        "suite": "planetvortex-crosslang",
        "version": "2.0.0",
        "kernel": c["kernel"],
        "tolerance": TOLERANCE,
        "checks": checks,
        "c_report": c,
        "passed": all_ok,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)
    print("=" * 74)
    print("  PLANETVORTEX — the cross-language diff (C99 vs Python)")
    print("=" * 74)
    for ch in checks:
        print(f"  [{'PASS' if ch['passed'] else 'FAIL'}] {ch['register']}")
    print("-" * 74)
    print(
        f"  RESULT: {'ALL PASSED' if all_ok else 'FAILURES PRESENT'} "
        f"({len(checks)} registers, tolerance {TOLERANCE:g})"
    )
    print(f"  report: {out}")
    print("-" * 74)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
