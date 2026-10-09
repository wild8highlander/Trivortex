#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
PLANETVORTEX — THE COMMAND LINE
============================================================================
The user-facing CLI of the bench: register the body, verify the run,
generate the monograph — "хотел проверить — раз и проверил".

    PYTHONPATH=python python3 -m planetvortex.cli register --body Mars
    PYTHONPATH=python python3 -m planetvortex.cli register \
        --custom "Kepler-452b#3.29e24*1.63" --json
    PYTHONPATH=python python3 -m planetvortex.cli verify --preset quick
    PYTHONPATH=python python3 -m planetvortex.cli monograph \
        --bodies "Sun,Earth,Mars" --lang ru --format pdf

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from . import classical as cl
from . import klein as kl
from . import monograph_gen as mg
from . import spatial as sp


def _registered_or_custom(name: str, gm_arg: float | None, mass_arg: float | None) -> dict:
    registered = {b.name: b for b in kl.BODIES}
    if name in registered:
        b = registered[name]
        try:
            incl = cl.spatial_register_by_name(name).inclination_deg
        except KeyError:
            incl = None
        return {"body": name, "gm": b.gm, "kind": b.kind, "incl_deg": incl}
    if gm_arg is not None:
        return {"body": name, "gm": gm_arg, "kind": "custom", "incl_deg": None}
    if mass_arg is not None:
        return {"body": name, "gm": mass_arg * cl.G_NEWTON, "kind": "custom", "incl_deg": None}
    raise SystemExit(f"unknown body {name!r}: pass --gm or --mass-kg for a custom body")


def cmd_register(args: argparse.Namespace) -> int:
    if args.custom:
        name, _, spec = args.custom.partition("#")
        gm = None
        mass = None
        if "@" in spec:
            gm = float(spec.split("@")[1])
        elif spec:
            parts = spec.split("*")
            mass = float(parts[0])
        body = _registered_or_custom(name, gm, mass)
        if body["kind"] != "custom":
            print(f"'{name}' is a registered body — printing its register anyway")
    else:
        body = _registered_or_custom(args.body, args.gm, args.mass_kg)

    # the register algebra over the registered 12 plus this body
    spec_rows = [
        {
            "body": b.name,
            "gm": b.gm,
            "kind": b.kind,
            "incl_deg": (
                cl.spatial_register_by_name(b.name).inclination_deg
                if _has_spatial(b.name)
                else None
            ),
        }
        for b in kl.BODIES
    ]
    bodies = spec_rows + ([body] if body["kind"] == "custom" else [])
    rows, stats = mg.register_rows(bodies)
    row = next(r for r in rows if r["body"] == body["body"])
    payload = {
        "body": row["body"],
        "kind": body["kind"],
        "gm_m3_s2": row["gm"],
        "s_log_normalization": row["s"],
        "vertex_angle_rad": row["alpha"],
        "vertex_angle_deg": math.degrees(row["alpha"]),
        "circumradius_R": row["R"],
        "edge_l": row["edge"],
        "inradius_r": row["inradius"],
        "area_A": row["area"],
        "formulas": [
            "alpha = 2pi/3 - sigma * (ln GM - mean(ln GM))",
            "cosh R = cot(alpha/2) cot(pi/7)",
            "cosh(l/2) = cos(pi/7) / sin(alpha/2)",
            "cosh r = cos(alpha/2) / sin(pi/7)",
            "A = 5pi - 7 alpha",
        ],
        "budget": {
            "alpha_sum": stats["alpha_sum"],
            "eight_pi": 8.0 * math.pi,
            "residual": abs(stats["alpha_sum"] - 8.0 * math.pi),
            "note": "exact by the geometric-mean normalization (sum s = 0)",
        },
    }
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print("=" * 74)
        print(f"  PLANETVORTEX register: {row['body']}  ({body['kind']})")
        print("=" * 74)
        print(f"  GM                      = {row['gm']:.6e} m^3/s^2")
        print(f"  s (log normalization)   = {row['s']:+.6f}")
        print(
            f"  vertex angle alpha      = {row['alpha']:.6f} rad "
            f"({math.degrees(row['alpha']):.3f} deg)"
        )
        print(f"  circumradius R          = {row['R']:.9f}")
        print(f"  edge l                  = {row['edge']:.9f}")
        print(f"  inradius r              = {row['inradius']:.9f}")
        print(f"  area A = 5pi - 7 alpha  = {row['area']:.9f}")
        print(f"  (hyperbolic units, R_bar = 1; the pair area 2A enters the 8pi budget)")
        if body["incl_deg"] is not None:
            print(
                f"  spatial tilt i          = {body['incl_deg']:.5f} deg "
                f"(arc lambda = {math.radians(body['incl_deg']):.6f} rad at R_bar = 1 AU)"
            )
        print(
            f"  budget of this set      = {stats['alpha_sum']:.12f} vs 8pi "
            f"(residual {abs(stats['alpha_sum'] - 8.0 * math.pi):.2e})"
        )
        print("-" * 74)
    return 0


def _has_spatial(name: str) -> bool:
    try:
        cl.spatial_register_by_name(name)
        return True
    except KeyError:
        return False


def cmd_verify(args: argparse.Namespace) -> int:
    from . import vregister as vr

    report = vr.run_v_register(args.preset)
    for stage in ("V1", "V2"):
        check = report[stage]
        status = "PASS" if check["passed"] else "FAIL"
        print(f"[{status}] {stage}: {check['check'][:110]}...")
    print(
        f"RESULT: {'ALL PASSED' if report['all_passed'] else 'FAILURES PRESENT'} "
        f"(preset {args.preset})"
    )
    return 0 if report["all_passed"] else 1


def cmd_monograph(args: argparse.Namespace) -> int:
    artifacts = mg.generate(
        args.bodies, lang=args.lang, fmt=args.format, out_dir=Path(args.out) if args.out else None
    )
    for kind, path in artifacts.items():
        print(f"  {kind}: {path}")
    return 0


def main(argv: list | None = None) -> int:
    ap = argparse.ArgumentParser(prog="planetvortex", description="the bench CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_reg = sub.add_parser("register", help="the exact register of one body")
    p_reg.add_argument("--body", default="Earth", help="a registered body name")
    p_reg.add_argument("--custom", help="Name#mass_kg*radius_km or Name@GM")
    p_reg.add_argument("--gm", type=float, help="GM of a custom body, m^3/s^2")
    p_reg.add_argument("--mass-kg", type=float, help="mass of a custom body, kg")
    p_reg.add_argument("--json", action="store_true")
    p_reg.set_defaults(func=cmd_register)

    p_ver = sub.add_parser("verify", help="run the V-register (V1 + V2)")
    p_ver.add_argument("--preset", default="quick", choices=["quick", "default", "full"])
    p_ver.set_defaults(func=cmd_verify)

    p_mon = sub.add_parser("monograph", help="generate a personal monograph")
    p_mon.add_argument(
        "--bodies", required=True, help='e.g. "Sun,Earth,Mars" or "Sun,Kepler-452b#3.29e24*1.63"'
    )
    p_mon.add_argument("--lang", default="en", choices=["en", "ru"])
    p_mon.add_argument("--format", default="all", choices=["md", "docx", "pdf", "all"])
    p_mon.add_argument("--out", default=None, help="output directory")
    p_mon.set_defaults(func=cmd_monograph)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
