#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TrivortexBot repo doctor — the self-healing guardian of the repository.

The doctor is the third organ of TrivortexBot (after Dependabot and the
dependabot auto-merge workflow): it periodically diagnoses the repository
for the classes of decay that GitHub Actions silently tolerates — broken
workflow trigger syntax, an invalid dependabot.yml, stale analytic pins,
nested self-duplicate packaging, hygiene drift — and repairs everything
that is safe to repair in place, then reports the rest.

Design contract (kept deliberately small so CI can trust it):
  * stdlib-only at run time (PyYAML is used opportunistically when present
    and skipped with an advisory otherwise);
  * every auto-fix is a targeted, byte-exact substitution — the doctor
    never invents structure it cannot verify;
  * exit codes: 0 = clean, 1 = findings, 2 = usage error.

Run from the repository root:
    python3 .github/scripts/repo_doctor.py --check     # diagnose only
    python3 .github/scripts/repo_doctor.py --fix      # diagnose + repair
    python3 .github/scripts/repo_doctor.py --fix --json
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from dataclasses import dataclass

try:
    import yaml
except ImportError:  # PyYAML is absent in minimal sandboxes, never on runners
    yaml = None

# ── The closed-form reference values of Theorem 3.1 (C_Ch = 1, T = 2π) ─────
# ω = (2π/T)·e^(C_Ch/π) and ε = 1/(e^(C_Ch/π) − 1) — the doctor recomputes
# them from the formula, exactly like verification/trivortex/python/verify.py
# and its pytest guard do, so a drift in either the formula or the pinned
# table of verification/README.md §11 is caught here first.
OMEGA_31 = math.exp(1.0 / math.pi)
EPSILON_31 = 1.0 / (math.exp(1.0 / math.pi) - 1.0)
STALE_EPSILON = "0.7276379117656014"  # the historical README pin (see §11)

DEPENDABOT_ECOSYSTEMS = {
    "bundler",
    "cargo",
    "composer",
    "devcontainers",
    "docker",
    "elm",
    "gitsubmodule",
    "github-actions",
    "go",
    "gradle",
    "maven",
    "npm",
    "nuget",
    "pip",
    "poetry",
    "pub",
    "swift",
    "terraform",
}
DEPENDABOT_INTERVALS = {"daily", "weekly", "monthly"}

BRANCH_LINE = re.compile(r"^(?P<indent>\s*)branches:\s*(?P<value>\S.*?)\s*$")
USES_LINE = re.compile(r"^\s*uses:\s*(?P<ref>\S+)\s*$")
PIN_LINE = re.compile(r"(?P<sym>[εω])\s*=\s*(?P<num>\d+\.\d+)")
FLOAT_OK = {"ε": EPSILON_31, "ω": OMEGA_31}


@dataclass
class Finding:
    """One diagnosed issue: auto-fixable ones carry the applied status."""

    code: str
    path: str
    line: int
    message: str
    fixable: bool = False
    advisory: bool = False
    fixed: bool = False

    def as_dict(self) -> dict:
        status = "ADVISORY" if self.advisory else ("FIXED" if self.fixed else "OPEN")
        return {
            "code": self.code,
            "path": self.path,
            "line": self.line,
            "message": self.message,
            "status": status,
        }


class RepoDoctor:
    """Collects findings over one repository pass, optionally repairing."""

    def __init__(self, root: str, fix: bool) -> None:
        self.root = os.path.abspath(root)
        self.fix = fix
        self.findings: list[Finding] = []
        self.rewritten: set[str] = set()

    # ── plumbing ──────────────────────────────────────────────────────────
    def report(
        self,
        code: str,
        path: str,
        line: int,
        message: str,
        *,
        fixable: bool = False,
        advisory: bool = False,
    ) -> None:
        self.findings.append(
            Finding(
                code,
                os.path.relpath(path, self.root),
                line,
                message,
                fixable=fixable,
                advisory=advisory,
            )
        )

    def workflows(self) -> list[str]:
        folder = os.path.join(self.root, ".github", "workflows")
        if not os.path.isdir(folder):
            return []
        return sorted(
            os.path.join(folder, name)
            for name in os.listdir(folder)
            if name.endswith((".yml", ".yaml"))
        )

    def readme_targets(self) -> list[str]:
        """verification/README.md + the READMEs of its depth-1 packages."""
        targets = [os.path.join(self.root, "verification", "README.md")]
        base = os.path.join(self.root, "verification")
        if os.path.isdir(base):
            for name in sorted(os.listdir(base)):
                candidate = os.path.join(base, name, "README.md")
                if os.path.isfile(candidate):
                    targets.append(candidate)
        return [t for t in targets if os.path.isfile(t)]

    def write_back(self, path: str, text: str) -> None:
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
        self.rewritten.add(path)

    # ── WF: GitHub Actions workflow hygiene ───────────────────────────────
    def check_workflow_triggers(self) -> None:
        for path in self.workflows():
            with open(path, encoding="utf-8") as handle:
                lines = handle.read().splitlines(keepends=True)
            changed = False
            for index, raw in enumerate(lines, start=1):
                match = BRANCH_LINE.match(raw.rstrip("\n"))
                if match is None:
                    continue
                value = match.group("value")
                if self._branch_value_ok(value):
                    continue
                self.report(
                    "WF-001", path, index, f"branch filter is not a list: {value!r}", fixable=True
                )
                if self.fix and value == "ain]":
                    lines[index - 1] = raw.replace(f"branches: {value}", "branches: [main]")
                    changed = True
                    self.findings[-1].fixed = True
            if changed:
                self.write_back(path, "".join(lines))

    @staticmethod
    def _branch_value_ok(value: str) -> bool:
        text = value.strip()
        if text.startswith("["):
            return text.endswith("]") and text.count("[") == text.count("]")
        if text[:1] in {"'", '"'}:
            return len(text) >= 2 and text[-1] == text[0]
        return not any(char in text for char in "[]{},")

    def check_workflow_yaml(self) -> None:
        if yaml is None:
            self.report(
                "WF-002",
                os.path.join(self.root, "README.md"),
                0,
                "PyYAML not importable — deep YAML parsing skipped",
                advisory=True,
            )
            return
        for path in self.workflows():
            try:
                with open(path, encoding="utf-8") as handle:
                    document = yaml.safe_load(handle)
            except yaml.YAMLError as error:
                self.report("WF-002", path, 0, f"YAML parse error: {error}")
                continue
            if not isinstance(document, dict):
                self.report("WF-003", path, 0, "workflow is not a mapping")
                continue
            if "on" not in document and True not in document:
                self.report("WF-003", path, 0, "workflow defines no `on:`")

    def check_action_pins(self) -> None:
        for path in self.workflows():
            with open(path, encoding="utf-8") as handle:
                for index, raw in enumerate(handle, start=1):
                    match = USES_LINE.match(raw)
                    if match is None:
                        continue
                    ref = match.group("ref")
                    tag = ref.rsplit("@", 1)[-1]
                    if not re.fullmatch(r"v\d+(\.\d+)*", tag):
                        continue
                    self.report(
                        "WF-004",
                        path,
                        index,
                        f"action pinned by floating tag @{tag} " "(SHA pinning is recommended)",
                        advisory=True,
                    )

    # ── DB: dependabot.yml schema ─────────────────────────────────────────
    def check_dependabot(self) -> None:
        path = os.path.join(self.root, ".github", "dependabot.yml")
        if not os.path.isfile(path):
            self.report("DB-001", path, 0, "dependabot.yml is missing")
            return
        if yaml is None:
            return  # structural checks below need a parser
        try:
            with open(path, encoding="utf-8") as handle:
                document = yaml.safe_load(handle)
        except yaml.YAMLError as error:
            self.report("DB-002", path, 0, f"YAML parse error: {error}")
            return
        if not isinstance(document, dict) or document.get("version") != 2:
            self.report("DB-002", path, 0, "version must be 2")
            return
        for key in document:
            if key not in {"version", "updates", "registries"}:
                self.report(
                    "DB-005",
                    path,
                    0,
                    f"top-level key {key!r} is not valid dependabot "
                    "schema (groups must live under an update entry)",
                )
        updates = document.get("updates")
        if not isinstance(updates, list):
            self.report("DB-003", path, 0, "updates must be a list")
            return
        seen: set[tuple[str, str]] = set()
        for entry in updates:
            if not isinstance(entry, dict):
                self.report("DB-003", path, 0, "update entry is not a map")
                continue
            ecosystem = entry.get("package-ecosystem")
            directory = str(entry.get("directory", "/"))
            if ecosystem not in DEPENDABOT_ECOSYSTEMS:
                self.report(
                    "DB-003",
                    path,
                    0,
                    f"unsupported package-ecosystem: {ecosystem!r} "
                    "(conda has no Dependabot support)",
                )
                continue
            pair = (ecosystem, directory)
            if pair in seen:
                self.report("DB-004", path, 0, f"duplicate (ecosystem, directory) pair: {pair}")
            seen.add(pair)
            schedule = entry.get("schedule", {})
            interval = schedule.get("interval") if isinstance(schedule, dict) else None
            if interval not in DEPENDABOT_INTERVALS:
                self.report("DB-006", path, 0, f"invalid schedule interval: {interval!r}")

    # ── CT: analytic constant drift ────────────────────────────────────────
    def check_theorem31_pins(self) -> None:
        for path in self.readme_targets():
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
            lines = text.splitlines(keepends=True)
            changed = False
            for index, raw in enumerate(lines, start=1):
                for match in PIN_LINE.finditer(raw):
                    symbol = match.group("sym")
                    number = match.group("num")
                    if len(number.split(".")[-1]) < 10:
                        # truncated prose (e.g. an erratum note that quotes
                        # "ε=0.7276…"), not a float64 pin — not our business
                        continue
                    if float(number) == FLOAT_OK[symbol]:
                        continue
                    if symbol == "ε" and number == STALE_EPSILON:
                        message = (
                            "stale ε pin (the historical table "
                            "value); true closed form: 1/(e^(1/π)−1)"
                        )
                        self.report("CT-001", path, index, message, fixable=True)
                        if self.fix:
                            lines[index - 1] = raw.replace(
                                f"ε = {STALE_EPSILON}", f"ε = {EPSILON_31!r}"
                            )
                            changed = True
                            self.findings[-1].fixed = True
                    else:
                        self.report(
                            "CT-001",
                            path,
                            index,
                            f"{symbol} pin {number} disagrees with the "
                            "closed-form reference value",
                        )
            if changed:
                self.write_back(path, "".join(lines))

    # ── CT-002: the stale ε pin wherever prose carries it ──────────────────
    # CT-001 only sees pins written as "ε = <number>" inside verification/;
    # the table layout (formula in one cell, the number in the next — root
    # README, the RU/EN monograph sources, the published site) hides from
    # that regex. The wrong float64 literal itself is unambiguous, so hunt
    # the documentation surfaces (markdown + site HTML) repo-wide by value.
    def check_stale_epsilon_occurrences(self) -> None:
        skip_dirs = {".git", "outputs", "__pycache__", "node_modules", ".venv"}
        for dirpath, dirnames, filenames in os.walk(self.root):
            dirnames[:] = sorted(d for d in dirnames if d not in skip_dirs)
            for name in filenames:
                if not name.endswith((".md", ".html")):
                    continue
                path = os.path.join(dirpath, name)
                with open(path, encoding="utf-8") as handle:
                    text = handle.read()
                if STALE_EPSILON not in text:
                    continue
                lines = text.splitlines(keepends=True)
                changed = False
                for index, raw in enumerate(lines, start=1):
                    if STALE_EPSILON not in raw:
                        continue
                    message = (
                        "stale ε pin outside the ε-adjacent scan — the true "
                        f"closed form 1/(e^(1/π)−1) = {EPSILON_31!r}"
                    )
                    self.report("CT-002", path, index, message, fixable=True)
                    if self.fix:
                        lines[index - 1] = raw.replace(STALE_EPSILON, repr(EPSILON_31))
                        changed = True
                        self.findings[-1].fixed = True
                if changed:
                    self.write_back(path, "".join(lines))

    # ── MF: Makefile recipe indentation ──────────────────────────────────
    # A recipe line indented with eight spaces instead of a tab is the one
    # decay class that turns `make verify-quick` into
    # "*** missing separator (did you mean TAB instead of 8 spaces?)".
    def makefiles(self) -> list[str]:
        found: list[str] = []
        for dirpath, _dirnames, filenames in os.walk(self.root):
            if ".git" in dirpath.split(os.sep):
                continue
            for name in filenames:
                if name == "Makefile" or name.endswith(".mk"):
                    found.append(os.path.join(dirpath, name))
        return found

    def check_makefile_indentation(self) -> None:
        for path in self.makefiles():
            with open(path, encoding="utf-8") as handle:
                lines = handle.read().splitlines(keepends=True)
            changed = False
            for index, raw in enumerate(lines, start=1):
                body = raw.rstrip("\n")
                if not body.startswith(" " * 8):
                    continue
                self.report(
                    "MF-001",
                    path,
                    index,
                    "recipe line indented with 8 spaces instead of a tab "
                    "(make refuses to parse it)",
                    fixable=True,
                )
                if self.fix:
                    stripped = body
                    while stripped.startswith(" " * 8):
                        stripped = stripped[8:]
                    newline = "\n" if raw.endswith("\n") else ""
                    lines[index - 1] = "\t" + stripped + newline
                    changed = True
                    self.findings[-1].fixed = True
            if changed:
                self.write_back(path, "".join(lines))

    # ── FS: filesystem hygiene ─────────────────────────────────────────────
    def check_nested_duplicates(self) -> None:
        for dirpath, _dirnames, _filenames in os.walk(self.root):
            parts = os.path.relpath(dirpath, self.root).split(os.sep)
            if len(parts) >= 2 and parts[-1] == parts[-2]:
                count = sum(len(files) for _d, _s, files in os.walk(dirpath))
                self.report(
                    "FS-001",
                    dirpath,
                    0,
                    f"nested self-duplicate directory ({count} files "
                    "below it) — deduplicate the packaging",
                )

    def check_hygiene(self) -> None:
        base = os.path.join(self.root, ".github")
        if not os.path.isdir(base):
            return
        for dirpath, _dirnames, filenames in os.walk(base):
            for name in filenames:
                if not name.endswith((".yml", ".yaml", ".py", ".json")):
                    continue
                path = os.path.join(dirpath, name)
                with open(path, encoding="utf-8") as handle:
                    text = handle.read()
                lines = text.splitlines(keepends=True)
                changed = False
                for index, raw in enumerate(lines, start=1):
                    body = raw.rstrip("\n")
                    stripped = body.rstrip(" \t")
                    if body != stripped:
                        self.report("FS-002", path, index, "trailing whitespace", fixable=True)
                        if self.fix:
                            lines[index - 1] = stripped + "\n" if raw.endswith("\n") else stripped
                            changed = True
                            self.findings[-1].fixed = True
                if text and not text.endswith("\n"):
                    self.report("FS-003", path, len(lines), "missing final newline", fixable=True)
                    if self.fix:
                        lines.append("\n")
                        changed = True
                        self.findings[-1].fixed = True
                if changed:
                    self.write_back(path, "".join(lines))

    def check_json(self) -> None:
        base = os.path.join(self.root, ".github")
        for dirpath, _dirnames, filenames in os.walk(base):
            for name in filenames:
                if not name.endswith(".json"):
                    continue
                path = os.path.join(dirpath, name)
                try:
                    with open(path, encoding="utf-8") as handle:
                        json.load(handle)
                except (OSError, ValueError) as error:
                    self.report("JS-001", path, 0, f"invalid JSON: {error}")

    # ── the pass ───────────────────────────────────────────────────────────
    def run(self) -> int:
        self.check_workflow_triggers()
        self.check_workflow_yaml()
        self.check_action_pins()
        self.check_dependabot()
        self.check_theorem31_pins()
        self.check_stale_epsilon_occurrences()
        self.check_makefile_indentation()
        self.check_nested_duplicates()
        self.check_hygiene()
        self.check_json()
        return 1 if any(not f.advisory and not f.fixed for f in self.findings) else 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="diagnose only (no modifications)")
    parser.add_argument(
        "--fix", action="store_true", help="diagnose and apply safe repairs in place"
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--repo", default=".", help="repository root (default: cwd)")
    options = parser.parse_args(argv)
    if not options.check and not options.fix:
        options.check = True
    if options.check and options.fix:
        print("error: --check and --fix are mutually exclusive", file=sys.stderr)
        return 2

    doctor = RepoDoctor(options.repo, fix=options.fix)
    status = doctor.run()

    if options.json:
        print(json.dumps([f.as_dict() for f in doctor.findings], ensure_ascii=False, indent=2))
    else:
        mode = "check" if options.check else "fix"
        print(f"TrivortexBot repo doctor — mode: {mode}")
        print(f"repository: {doctor.root}")
        for finding in doctor.findings:
            flag = "[fix ]" if finding.fixed else "[adv ]" if finding.advisory else "[open]"
            print(f"{flag} {finding.code} {finding.path}:{finding.line} " f"— {finding.message}")
        open_count = sum(1 for f in doctor.findings if not f.advisory and not f.fixed)
        if doctor.rewritten:
            print(f"repaired files: {sorted(doctor.rewritten)}")
        print(f"findings: {len(doctor.findings)} " f"({open_count} open after this pass)")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
