#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
PLANETVORTEX — RUNNER: BIND EVERY NUMBER TO A RUN (JSON PROTOCOLS)
============================================================================
CLI front end of the P-ladder. Runs the whole ladder or a single stage
and writes one deterministic JSON protocol per stage into
planetvortex/results/protocols/ — the same "every number is bound to a
run" discipline as the parent repository and the polyvortex bench.

Usage
-----
    python3 runner.py --preset default                 # the whole ladder
    python3 runner.py --stage P4 --preset default      # one stage
    python3 runner.py --preset quick --out-dir /tmp/x  # custom protocol dir

Exit code 0 = all requested stages passed, 1 = at least one failed.

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..")))

import planetvortex.hardcore as hardcore  # noqa: E402
import planetvortex.ladder as ladder  # noqa: E402
import planetvortex.vregister as vregister  # noqa: E402

STAGE_SLUGS = {
    "P1": "P1_anchor",
    "P2": "P2_kepler_register",
    "P3": "P3_planetary_nbody",
    "P4": "P4_fano_algebra",
    "P5": "P5_heptagon_lattice",
    "P6": "P6_seven_cells",
    "P7": "P7_gravity_bridge",
    "X1": "X1_sl2_enumeration",
    "X2": "X2_group_actions",
    "X3": "X3_triangle_hurwitz",
    "X4": "X4_hyperbolic_figure",
    "X5": "X5_integrator_certification",
    "X6": "X6_pn_perihelion",
    "V1": "V1_inclined_registers",
    "V2": "V2_klein_tiling",
}

SUITES = {
    "p": ("planetvortex-ladder", ladder.CHECK_FUNCS, ladder.PRESETS),
    "x": ("planetvortex-hardcore", hardcore.X_CHECK_FUNCS, hardcore.X_PRESETS),
    "v": ("planetvortex-vregister", vregister.CHECK_FUNCS, vregister.PRESETS),
}


def default_out_dir() -> str:
    return os.path.normpath(os.path.join(HERE, "..", "..", "results", "protocols"))


def save_protocol(
    stage: str, check: dict, preset: str, out_dir: str, suite_tag: str = "planetvortex-ladder"
) -> str:
    os.makedirs(out_dir, exist_ok=True)
    report = {
        "suite": suite_tag,
        "version": "2.0.0",
        "stage": stage,
        "preset": preset,
        "date_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "check": check,
    }
    path = os.path.join(out_dir, f"{STAGE_SLUGS[stage]}_{preset}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description="PLANETVORTEX ladder runner")
    ap.add_argument(
        "--suite",
        default="p",
        choices=["p", "x", "v", "all"],
        help="p = the P-ladder (P1..P7), x = the hardcore X-register "
        "(X1..X6), v = the V-register (V1..V2), all = everything",
    )
    ap.add_argument("--preset", default="default")
    ap.add_argument(
        "--stage",
        default="all",
        help="run one stage or the whole suite",
    )
    ap.add_argument("--out-dir", default=None, help="protocol output directory")
    args = ap.parse_args()

    suite_names = ["p", "x", "v"] if args.suite == "all" else [args.suite]
    selected: list = []
    for name in suite_names:
        suite_tag, funcs, presets = SUITES[name]
        if args.preset not in presets:
            ap.error(f"preset {args.preset!r} is not defined for suite {name!r}")
        stages = sorted(funcs) if args.stage == "all" else [args.stage]
        for stage in stages:
            if stage not in funcs:
                ap.error(f"stage {stage!r} is not in suite {name!r}")
            selected.append((name, suite_tag, funcs, presets, stage))

    out_dir = args.out_dir or default_out_dir()
    t0 = time.perf_counter()
    print("=" * 74)
    print("  PLANETVORTEX — the planetary gravity-geometry bench")
    print("  suites: " + ", ".join(suite_names) + f"  preset={args.preset}")
    print("=" * 74)
    all_ok = True
    for name, suite_tag, funcs, presets, stage in selected:
        t_s = time.perf_counter()
        check = funcs[stage](presets[args.preset])
        status = "PASS" if check["passed"] else "FAIL"
        all_ok = all_ok and check["passed"]
        path = save_protocol(stage, check, args.preset, out_dir, suite_tag)
        print(f"\n[{status}] {check['check']}")
        print(f"    stage {stage}  wall {time.perf_counter() - t_s:.2f}s")
        print(f"    protocol: {path}")
    wall = time.perf_counter() - t0
    print("\n" + "-" * 74)
    print(
        f"  RESULT: {'ALL PASSED' if all_ok else 'FAILURES PRESENT'} "
        f"({len(selected)} stages, suites={','.join(suite_names)}, "
        f"preset={args.preset}, wall {wall:.2f}s)"
    )
    print("-" * 74)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
