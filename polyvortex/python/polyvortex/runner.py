#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
POLYVORTEX — RUNNER: BIND EVERY NUMBER TO A RUN (JSON PROTOCOLS)
============================================================================
CLI front end of the W-ladder. Runs the whole ladder or a single stage
and writes one deterministic JSON protocol per stage into
polyvortex/results/protocols/ — the same "every number is bound to a
run" discipline as the parent repository.

Usage
-----
    python3 runner.py --preset default                 # the whole ladder
    python3 runner.py --stage W4 --preset default      # one stage
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

import polyvortex.ladder as ladder  # noqa: E402

STAGE_SLUGS = {
    "W1": "W1_anchor",
    "W2": "W2_ring_rotation",
    "W3": "W3_invariants",
    "W4": "W4_stability",
    "W5": "W5_admissibility",
    "W6": "W6_obstruction",
    "W7": "W7_bridge",
}

STAGE_FUNCS = {
    "W1": lambda cfg: ladder.check_w1_anchor(n_points=cfg["n_points"]),
    "W2": lambda cfg: ladder.check_w2_ring_rotation(
        rotations=cfg["rotations"], steps_per_period=cfg["steps_per_period"]
    ),
    "W3": lambda cfg: ladder.check_w3_invariants(
        rotations=cfg["rotations"], steps_per_period=cfg["steps_per_period"]
    ),
    "W4": lambda cfg: ladder.check_w4_stability(),
    "W5": lambda cfg: ladder.check_w5_admissibility(cch_grid=cfg["cch_grid"]),
    "W6": lambda cfg: ladder.check_w6_obstruction(),
    "W7": lambda cfg: ladder.check_w7_bridge(quad_nodes=cfg["quad_nodes"]),
}


def default_out_dir() -> str:
    return os.path.normpath(os.path.join(HERE, "..", "..", "results", "protocols"))


def save_protocol(stage: str, check: dict, preset: str, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    report = {
        "suite": "polyvortex-ladder",
        "version": "1.1.0",
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
    ap = argparse.ArgumentParser(description="POLYVORTEX W-ladder runner")
    ap.add_argument("--preset", default="default", choices=sorted(ladder.PRESETS))
    ap.add_argument(
        "--stage",
        default="all",
        choices=["all"] + sorted(STAGE_FUNCS),
        help="run one stage or the whole ladder",
    )
    ap.add_argument("--out-dir", default=None, help="protocol output directory")
    args = ap.parse_args()
    out_dir = args.out_dir or default_out_dir()

    cfg = ladder.PRESETS[args.preset]
    stages = sorted(STAGE_FUNCS) if args.stage == "all" else [args.stage]

    t0 = time.perf_counter()
    print("=" * 74)
    print("  POLYVORTEX — THE W-LADDER (N-vortex extension of Theorem 3.1)")
    print("=" * 74)
    all_ok = True
    for stage in stages:
        t_s = time.perf_counter()
        check = STAGE_FUNCS[stage](cfg)
        status = "PASS" if check["passed"] else "FAIL"
        all_ok = all_ok and check["passed"]
        path = save_protocol(stage, check, args.preset, out_dir)
        print(f"\n[{status}] {check['check']}")
        print(f"    stage {stage}  wall {time.perf_counter() - t_s:.2f}s")
        print(f"    protocol: {path}")
    wall = time.perf_counter() - t0
    print("\n" + "-" * 74)
    print(
        f"  RESULT: {'ALL PASSED' if all_ok else 'FAILURES PRESENT'} "
        f"({len(stages)} stages, preset={args.preset}, wall {wall:.2f}s)"
    )
    print("-" * 74)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
