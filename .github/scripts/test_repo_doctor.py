#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integration test for the TrivortexBot repo doctor.

Builds a scratch repository with one planted violation per finding class,
runs the doctor in --fix mode, asserts every fixable class is healed,
every report-only class is escalated, and a second --check pass is stable.

Run: python3 .github/scripts/test_repo_doctor.py
     (or `make doctor-test`)
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DOCTOR = os.path.join(HERE, "repo_doctor.py")
PYPROJECT = os.path.join(ROOT, "pyproject.toml")

WORKFLOW_BAD = """name: broken
on:
  push:
    branches: ain]
  schedule:
    - cron: '0 99 * * *'
jobs:
  a:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
"""

MD_BAD = (
    "> **Navigation:** [up](../README.md) › **`x`**\n"
    "\n"
    "> The description quote continues here.\n"
    "\n"
    "Paragraph before list.\n"
    "1. first ordered item\n"
    "- first bullet item\n"
    "\n"
    "\n"
    "\n"
    "\n"
    "\n"
    "\tTABPROSE\n"
    '<img src="https://img.shields.io/badge/x-1-22D3EE"/>\n'
    "\n"
    "```python\n"
    'print("fenced tab\tkept")\n'
    "```\n"
    "\n"
    "| Head | Tail |\n"
    "|---|---|\n"
    "| a | b | c |\n"
    "| two | cells |\n"
    "\n"
    "[bad anchor](#no-such-heading)\n"
    "\n"
    "```\n"
    "bare fence with no language\n"
    "```\n"
    "\n"
    "```text\n"
    "ok fence\n"
    "```   \n"
)  # trailing three spaces on the last fence close line; final newline present

PY_BAD = "import os \nx = 1\n\n\n\ndef f():\n    pass"

DATA_BAD = "ε = 0.7276379117656014 stale pin\nω = 1.9999999999 wrong pin"

HEALED_OPEN = {"CT-001", "DB-006", "LF-003", "LF-009", "LF-010", "LF-011", "PK-001", "WF-006"}


def build(root: str) -> None:
    os.makedirs(f"{root}/.github/workflows", exist_ok=True)
    os.makedirs(f"{root}/.github/scripts", exist_ok=True)
    os.makedirs(f"{root}/verification/notes", exist_ok=True)

    def write(path: str, text: str) -> None:
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)

    write(f"{root}/.github/workflows/broken.yml", WORKFLOW_BAD)
    write(f"{root}/.github/scripts/tool.py", PY_BAD)
    write(f"{root}/docs.md", MD_BAD)
    write(f"{root}/banner.md", '<p align="center">\n  <img src="b.svg"/>\n</p>\n')
    write(f"{root}/verification/notes/README.md", DATA_BAD)
    write(f"{root}/verification/README.md", "root readme")  # no final newline
    write(f"{root}/Makefile", "target:\n        echo hi\n")
    write(
        f"{root}/.github/dependabot.yml",
        "version: 2\nupdates:\n  - package-ecosystem: pip\n    directory: /\n"
        "    schedule:\n      interval: hourly\n",
    )
    # per-file-ignores pointing at a file that does not exist (PK-001)
    write(
        f"{root}/pyproject.toml",
        open(PYPROJECT, encoding="utf-8")
        .read()
        .replace(
            '"verification/trivortex_master/trivortex_master_single.py" = ["F811", "N801"]',
            '"verification/trivortex_master/trivortex_single_MISSING.py" = ["F811", "N801"]',
        ),
    )


def run(args: list[str], cwd: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, DOCTOR, *args, "--repo", cwd],
        capture_output=True,
        text=True,
        check=False,
    )


STATUS_CODE = re.compile(r"^\[(fix |adv |open)\] (\S+)")


def codes_of(output: str, status: str) -> set[str]:
    found = set()
    for line in output.splitlines():
        match = STATUS_CODE.match(line)
        if match and match.group(1).strip() == status:
            found.add(match.group(2))
    return found


def main() -> int:
    root = tempfile.mkdtemp(prefix="doctor-test-")
    try:
        build(root)
        fixed = run(["--fix"], root)
        if fixed.stderr:
            print("FAIL — the doctor crashed during --fix:")
            print(fixed.stderr)
            return 1
        fixed_codes = codes_of(fixed.stdout, "fix")
        open_codes = codes_of(fixed.stdout, "open")

        must_fix = {
            "WF-001",
            "CT-001",
            "MF-001",
            "FS-002",
            "FS-003",
            "LF-001",
            "LF-002",
            "LF-003",
            "LF-004",
            "LF-005",
            "LF-006",
            "LF-008",
            "LF-012",
            "YML-001",
        }
        missing = {code for code in must_fix if code not in fixed_codes}
        if missing:
            print("FAIL — expected fixable classes not healed:", sorted(missing))
            print(fixed.stdout)
            return 1
        # WF-005 (advisory) and PK-001 (report-only) must be present at all
        advisory = codes_of(fixed.stdout, "adv")
        if "WF-005" not in advisory or "PK-001" not in open_codes:
            print("FAIL — WF-005 advisory or PK-001 report missing")
            print(fixed.stdout)
            return 1
        if open_codes != HEALED_OPEN:
            print("FAIL — open set mismatch.\nexpected:", sorted(HEALED_OPEN))
            print("got:", sorted(open_codes))
            for line in fixed.stdout.splitlines():
                if line.startswith("[open]"):
                    print("   ", line)
            return 1
        if fixed.returncode != 1:
            print("FAIL — fix run must exit 1 while report-only findings remain")
            return 1

        # spot-check the healed content
        wf = open(f"{root}/.github/workflows/broken.yml", encoding="utf-8").read()
        assert "branches: [main]" in wf, wf
        assert wf.startswith("---\n"), "YML-001 did not prepend document start"
        md = open(f"{root}/docs.md", encoding="utf-8").read()
        banner = open(f"{root}/banner.md", encoding="utf-8").read()
        assert banner.startswith("<!-- markdownlint-disable-file MD041 -->\n<p"), "LF-012"
        assert "\n>\n" in md, "LF-005 quote gap not merged"
        assert 'alt="image"' in md, "LF-006 alt not added"
        assert "    TABPROSE" in md, "LF-003 tab not spaced"
        assert "\t" not in md.replace("fenced tab\tkept", ""), "LF-003 scope"
        assert "b | c |" in md, "LF-009 table row must stay intact (report-only)"
        assert md.endswith("```   \n") is False, "LF-001 trailing spaces on md"
        # MD009 keeps two of the three trailing spaces as a hard break
        assert md.splitlines()[-1] == "```" + " " * 2, "LF-001 trims to the allowed break"
        readme = open(f"{root}/verification/README.md", encoding="utf-8").read()
        assert readme.endswith("\n"), "LF-002 final newline"
        mk = open(f"{root}/Makefile", encoding="utf-8").read()
        assert "\techo hi" in mk, "MF-001 not tabbed"
        py = open(f"{root}/.github/scripts/tool.py", encoding="utf-8").read()
        assert py.endswith("\n") and "import os\n" in py, "FS hygiene"
        notes = open(f"{root}/verification/notes/README.md", encoding="utf-8").read()
        assert "0.7276379117656014" not in notes, "CT-001 stale epsilon not fixed"

        # second pass: only the report-only classes remain open
        check = run(["--check"], root)
        still_open = codes_of(check.stdout, "open")
        if still_open != HEALED_OPEN:
            print("FAIL — second check open set:", sorted(still_open))
            return 1
        print("PASS — fixable classes healed, report-only classes escalated, re-check stable")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
