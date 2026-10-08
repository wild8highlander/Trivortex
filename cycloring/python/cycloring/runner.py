#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
CYCLORING — THE PROTOCOL RUNNER
============================================================================
Binds every ladder stage to a deterministic JSON protocol file in
results/protocols/{stage}_{preset}.json — the same "bound to a run"
discipline as the parent repository's research directories.

    PYTHONPATH=python python3 python/cycloring/runner.py --preset default
    PYTHONPATH=python python3 python/cycloring/runner.py --stage W5

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..")))

import cycloring.ladder as ladder  # noqa: E402

PACKAGE_DIR = Path(__file__).resolve().parent
MINIROOT = PACKAGE_DIR.parents[1]
PROTOCOL_DIR = MINIROOT / "results" / "protocols"

STAGE_SLUGS = {
    "W1": "W1_period_core",
    "W2": "W2_algebraic_boundary",
    "W3": "W3_root_system",
    "W4": "W4_polygon_flow",
    "W5": "W5_transport_identity",
    "W6": "W6_synchronous_closure",
    "W7": "W7_transducer",
}


def write_protocol(stage: str, preset: str, result: dict) -> Path:
    """Write one deterministic protocol file."""
    PROTOCOL_DIR.mkdir(parents=True, exist_ok=True)
    slug = STAGE_SLUGS.get(stage, stage)
    out = PROTOCOL_DIR / f"{slug}_{preset}.json"
    payload = {"stage": stage, "preset": preset}
    payload.update(result)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="CYCLORING W-ladder runner")
    parser.add_argument("--preset", default="default", choices=sorted(ladder.PRESETS))
    parser.add_argument("--stage", default=None, help="run a single stage W1..W7")
    args = parser.parse_args()

    stages = [args.stage.upper()] if args.stage else list(ladder.STAGES)
    all_pass = True
    for stage in stages:
        result = ladder.run_stage(stage, args.preset)
        path = write_protocol(stage, args.preset, result)
        status = "PASS" if result["passed"] else "FAIL"
        all_pass = all_pass and bool(result["passed"])
        print(f"{stage} [{args.preset}] {status} -> {path.relative_to(MINIROOT)}")
    print("LADDER", "PASS" if all_pass else "FAIL")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
