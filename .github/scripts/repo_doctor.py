#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TrivortexBot repo doctor — the self-healing guardian of the repository.

The doctor is the third organ of TrivortexBot (after Dependabot and the
dependabot auto-merge workflow): it periodically diagnoses the repository
for the classes of decay that GitHub Actions silently tolerates — broken
workflow trigger syntax, an invalid dependabot.yml, stale analytic pins,
nested self-duplicate packaging, hygiene drift, markdown rot (v1.2: the
LF/YML classes mirror the lint gate) — and repairs everything that is
safe to repair in place, then reports the rest.

Finding classes (the letters are the repair domain):
  * WF — GitHub Actions workflows: trigger syntax, missing `on:`,
    missing `permissions:`, malformed cron schedules, floating action pins;
  * DB — .github/dependabot.yml schema;
  * CT — the analytic constant pins of Theorem 3.1 and of the §8 mirror
    (ω = e^(1/π) with C_Ch = 1, T = 2π; ω = 3G/2π with G = 1;
    ε = 1/(e^(1/π) − 1)) — the doctor recomputes them from the formula,
    exactly like verification/trivortex/python/verify.py and its pytest
    guard do, so a drift in either the formula or the pinned tables is
    caught here first;
  * MF — Makefile recipe indentation (the "missing separator" class);
  * FS — filesystem and whitespace hygiene (trailing whitespace, missing
    final newlines, nested self-duplicate packaging);
  * LF — lint-gate mirror (v1.2): the mechanical subset of the markdown
    gate (MD009/010/012/028/032/040/045/051/056) plus repo-wide file
    hygiene, so PRs cannot re-introduce a class the Lint workflow fixed
    before;
  * YML — the yamllint gate mirror (document start, line length);
  * PK — packaging drift: a ruff per-file-ignore pattern that no longer
    matches any file;
  * JS — invalid JSON under .github/.

Design contract (kept deliberately small so CI can trust it):
  * stdlib-only at run time (PyYAML/tomllib are used opportunistically
    when present and skipped with an advisory otherwise);
  * every auto-fix is a targeted, byte-exact substitution — the doctor
    never invents structure it cannot verify (renumbering an ordered
    list, guessing a fence language or rewriting a broken table changes
    intent, so LF-007/009/010/011 report instead of fix);
  * exit codes: 0 = clean, 1 = findings, 2 = usage error.

Run from the repository root:
    python3 .github/scripts/repo_doctor.py --check     # diagnose only
    python3 .github/scripts/repo_doctor.py --fix      # diagnose + repair
    python3 .github/scripts/repo_doctor.py --fix --json
    python3 .github/scripts/repo_doctor.py --check --report /tmp/report.md
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import math
import os
import re
import sys
import urllib.parse
from dataclasses import dataclass

try:
    import yaml
except ImportError:  # PyYAML is absent in minimal sandboxes, never on runners
    yaml = None

try:
    import tomllib  # Python 3.11+
except ImportError:  # pragma: no cover — runners are on 3.12
    tomllib = None

# ── The closed-form reference values of Theorem 3.1 (C_Ch = 1, T = 2π) ─────
# ω = (2π/T)·e^(C_Ch/π) and ε = 1/(e^(C_Ch/π) − 1) — the doctor recomputes
# them from the formula, exactly like verification/trivortex/python/verify.py
# and its pytest guard do, so a drift in either the formula or the pinned
# table of verification/README.md §11 is caught here first.
# The §8 numeric mirror additionally pins ω = 3G/2π in the G = 1
# normalization (verification/notes/numeric_mirror_s8.log) — a different,
# equally exact constant: it is accepted, not flagged.
OMEGA_31 = math.exp(1.0 / math.pi)
OMEGA_MIRROR_G1 = 3.0 / (2.0 * math.pi)
EPSILON_31 = 1.0 / (math.exp(1.0 / math.pi) - 1.0)
STALE_EPSILON = "0.7276379117656014"  # the historical README pin (see §11)
OMEGA_OK = (OMEGA_31, OMEGA_MIRROR_G1)
EPSILON_OK = (EPSILON_31,)

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
CRON_LINE = re.compile(r"^\s*(?:-\s*)?cron:\s*['\"]?(?P<expr>[^'\"\n]+?)['\"]?\s*$")
PERMISSIONS_LINE = re.compile(r"^permissions:")
# five fields: minute, hour, day-of-month, month, day-of-week
CRON_FIELD = re.compile(r"^(?:\*|\*\/\d+|\d+(?:-\d+)?)(?:,(?:\*|\*\/\d+|\d+(?:-\d+)?))*$")
CRON_RANGE = ((0, 59), (0, 23), (1, 31), (1, 12), (0, 7))


def cron_field_in_range(field: str, low: int, high: int) -> bool:
    """True when one cron field only names values inside its allowed range
    ('*', '*/N', 'A', 'A-B', and comma lists of those)."""
    parts = field.split(",")
    for part in parts:
        step: str | None = None
        if part.startswith("*/"):
            step = part[2:]
            part = "*"
        if part == "*":
            if step is not None and not step.isdigit():
                return False
            continue
        numbers = [int(x) for x in part.split("-")]
        if any(not low <= number <= high for number in numbers):
            return False
    return True


# ── the LF/YML gate mirror: which text files the doctor inspects ────────────
# `results`/`runs` hold committed run artifacts (protocols, reports) — data,
# regenerated without a trailing newline by their writers; the doctor treats
# them like the outputs/ skip of CT-002, not as lint surface.
SKIP_DIRS = {
    ".git",
    "outputs",
    "__pycache__",
    "node_modules",
    ".venv",
    ".ruff_cache",
    ".pytest_cache",
    "results",
    "runs",
}
TEXT_EXTENSIONS = (".py", ".md", ".yml", ".yaml", ".cff", ".toml", ".cfg")

# markdown structural anchors
FENCE_LINE = re.compile(r"^ {0,3}(?P<marker>`{3,}|~{3,})(?P<info>.*)$")
QUOTE_LINE = re.compile(r"^ {0,3}>")
HEADING_LINE = re.compile(r"^(?: {0,3}> ?)* {0,3}#{1,6}\s+(?P<text>.*?)\s*#*\s*$")
LIST_ITEM = re.compile(r"^(?P<indent>\s*)(?P<bullet>[-*+]\s|\d{1,9}[.)]\s)")
IMG_TAG = re.compile(r"<img\b(?P<attrs>[^>]*?)/?>")
MD_LINK_FRAGMENT = re.compile(r"\]\(#(?P<frag>[^)\s]+)\)")
MD_HREF_FRAGMENT = re.compile(r"href=\"#(?P<frag>[^\"]+)\"")
MD012_KEEP = 3  # .markdownlint.json: "MD012": {"maximum": 3}
MD009_BREAK = 2  # .markdownlint.json: "MD009": {"br_spaces": 2}
# parser-consumed DATA markdown: its citation numbering is semantic, not a
# list convention — the lint gate excludes it, and so does the mirror.
MARKDOWN_DATA_EXEMPT = {"verification/trivortex_master/data/literature.md"}


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


class FenceScanner:
    """Tracks fenced code regions across the lines of one markdown file.

    feed() returns True while the line belongs to a fenced block (the
    fence lines themselves included), mirroring how markdownlint scopes
    MD010/MD012/MD028/MD032/MD040 to prose only.
    """

    def __init__(self) -> None:
        self.active = False
        self.char = ""
        self.length = 0
        self.info = ""
        self.opened_here = False

    def feed(self, raw: str) -> bool:
        line = raw.rstrip("\n")
        match = FENCE_LINE.match(line)
        self.opened_here = False
        if self.active:
            closed = (
                match is not None
                and match.group("marker")[0] == self.char
                and len(match.group("marker")) >= self.length
                and not match.group("info").strip()
            )
            if closed:
                self.active = False
            return True
        if match is not None:
            self.active = True
            self.char = match.group("marker")[0]
            self.length = len(match.group("marker"))
            self.info = match.group("info")
            self.opened_here = True
            return True
        return False


def github_slug(text: str) -> str:
    """The GitHub anchor of a heading: lowercase, punctuation stripped,
    spaces (each of them) turned into hyphens. Underscores inside words
    survive — they are word characters."""
    plain = re.sub(r"[*`~]", "", text)
    plain = re.sub(r"(?<!\w)_+(?!\w)", "", plain)
    plain = plain.strip().lower()
    plain = re.sub(r"[^\w\- ]", "", plain, flags=re.UNICODE)
    return plain.strip("-").replace(" ", "-")


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

    def repo_files(self, extensions: tuple[str, ...]) -> list[str]:
        """Every repository file with one of the extensions, stable order,
        skipping VCS/build/runtime artifact directories."""
        found: list[str] = []
        for dirpath, dirnames, filenames in os.walk(self.root):
            dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
            for name in sorted(filenames):
                if name.endswith(extensions):
                    found.append(os.path.join(dirpath, name))
        return found

    def markdown_files(self) -> list[str]:
        """Repository markdown minus the parser-consumed data file."""
        return [
            path
            for path in self.repo_files((".md",))
            if os.path.relpath(path, self.root).replace(os.sep, "/") not in MARKDOWN_DATA_EXEMPT
        ]

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
        return not any(char in text for char in "[]{},")  # noqa: SIM108 — stdlib style

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

    def check_workflow_permissions(self) -> None:
        """WF-005: a workflow without an explicit permissions block runs on
        the repo-default token scope; the OpenSSF scorecard dings it."""
        for path in self.workflows():
            found = False
            with open(path, encoding="utf-8") as handle:
                for raw in handle:
                    if PERMISSIONS_LINE.match(raw):
                        found = True
                        break
            if not found:
                self.report(
                    "WF-005",
                    path,
                    0,
                    "workflow defines no top-level permissions block "
                    "(runs with the repository-default token scope)",
                    advisory=True,
                )

    def check_workflow_crons(self) -> None:
        """WF-006: a malformed schedule expression silently never fires."""
        for path in self.workflows():
            with open(path, encoding="utf-8") as handle:
                for index, raw in enumerate(handle, start=1):
                    match = CRON_LINE.match(raw)
                    if match is None:
                        continue
                    fields = match.group("expr").split()
                    shape_ok = len(fields) == 5 and all(CRON_FIELD.match(field) for field in fields)
                    range_ok = shape_ok and all(
                        cron_field_in_range(field, *CRON_RANGE[position])
                        for position, field in enumerate(fields)
                    )
                    if not range_ok:
                        self.report(
                            "WF-006",
                            path,
                            index,
                            f"malformed cron expression: {match.group('expr')!r} "
                            "(expect five fields: min hour day month weekday, in range)",
                        )

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
                    if symbol == "ω" and float(number) in OMEGA_OK:
                        continue
                    if symbol == "ε" and float(number) in EPSILON_OK:
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
                        expected = "e^(1/π) or 3G/2π (G = 1)" if symbol == "ω" else "1/(e^(1/π)−1)"
                        self.report(
                            "CT-001",
                            path,
                            index,
                            f"{symbol} pin {number} disagrees with the "
                            f"closed-form reference ({expected})",
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
        for dirpath, dirnames, filenames in os.walk(self.root):
            dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
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
        """FS-002/FS-003 own the .github/ tree (the LF class below owns the
        rest of the repository)."""
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

    # ── LF-001/LF-002: repo-wide whitespace hygiene ────────────────────────
    # Mirrors the pre-commit trailing-whitespace / end-of-file-fixer hooks
    # outside .github/ (which FS-002/FS-003 own). Markdown keeps its two
    # hard-break spaces (MD009 br_spaces: 2): exactly two are allowed,
    # one or three-plus are violations.
    def check_file_hygiene(self) -> None:
        github_prefix = os.path.join(self.root, ".github") + os.sep
        for path in self.repo_files(TEXT_EXTENSIONS):
            if path.startswith(github_prefix):
                continue
            is_markdown = path.endswith(".md")
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
            lines = text.splitlines(keepends=True)
            changed = False
            for index, raw in enumerate(lines, start=1):
                body = raw.rstrip("\n")
                stripped = body.rstrip(" \t")
                if stripped == body:
                    continue
                if is_markdown:
                    trailing = len(body) - len(body.rstrip(" \t"))
                    if trailing == MD009_BREAK:
                        continue  # exactly two spaces = the allowed hard break
                    tail = " " * MD009_BREAK if trailing > MD009_BREAK else ""
                    stripped = stripped + tail
                self.report("LF-001", path, index, "trailing whitespace", fixable=True)
                if self.fix:
                    newline = "\n" if raw.endswith("\n") else ""
                    lines[index - 1] = stripped + newline
                    changed = True
                    self.findings[-1].fixed = True
            if text and not text.endswith("\n"):
                self.report("LF-002", path, len(lines), "missing final newline", fixable=True)
                if self.fix:
                    lines.append("\n")
                    changed = True
                    self.findings[-1].fixed = True
            if changed:
                self.write_back(path, "".join(lines))

    # ── LF: the mechanical markdown gate ───────────────────────────────────
    def check_markdown(self) -> None:
        for path in self.markdown_files():
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
            lines = text.splitlines(keepends=True)
            # the banner pass may insert a line, the blank-run pass may
            # delete several — the fence map is recomputed after every
            # line-count-changing pass so later passes stay aligned
            changed = self._md_banner_disable(path, lines)
            scanner = FenceScanner()
            fenced = [scanner.feed(raw) for raw in lines]
            changed = self._md_tabs(path, lines, fenced) or changed
            changed = self._md_blank_runs(path, lines, fenced) or changed
            scanner = FenceScanner()
            fenced = [scanner.feed(raw) for raw in lines]
            changed = self._md_quote_gaps(path, lines, fenced) or changed
            changed = self._md_list_blanks(path, lines, fenced) or changed
            scanner = FenceScanner()
            fenced = [scanner.feed(raw) for raw in lines]
            changed = self._md_img_alt(path, lines, fenced) or changed
            self._md_fence_languages(path, lines)
            if changed:
                self.write_back(path, "".join(lines))

    def _md_banner_disable(self, path: str, lines: list[str]) -> bool:
        """LF-012 = MD041 for the banner-first READMEs. A file that opens
        with an HTML banner block fails MD041 unless it carries the
        file-scoped disable comment — the repository's own convention (the
        root README and the MASTER README both use it). The single-file
        editions materialize their README from an embedded template and
        the template drops the comment, so every regeneration reintroduces
        the violation: the doctor re-applies the comment."""
        if not lines or not lines[0].lstrip().startswith("<"):
            return False
        if lines[0].lstrip().startswith("<!--"):
            # an invisible HTML comment (e.g. a different disable directive)
            # is tolerated by the gate the same way an H1 is
            return False
        if "markdownlint-disable-file MD041" in "".join(lines[:3]):
            return False
        self.report(
            "LF-012",
            path,
            1,
            "banner-first markdown without the MD041 disable comment "
            "(the file-scoped disable is the repository convention)",
            fixable=True,
        )
        if self.fix:
            lines.insert(0, "<!-- markdownlint-disable-file MD041 -->\n")
            self.findings[-1].fixed = True
            return True
        return False

    def _md_tabs(self, path: str, lines: list[str], fenced: list[bool]) -> bool:
        """LF-003 = MD010. Tabs in prose become four spaces; tabs inside
        fenced code may be meaningful (Makefile recipes) — report only."""
        changed = False
        for index, raw in enumerate(lines, start=1):
            if "\t" not in raw:
                continue
            if fenced[index - 1]:
                self.report(
                    "LF-003", path, index, "tab inside a fenced code block (MD010) — verify intent"
                )
                continue
            self.report("LF-003", path, index, "tab in markdown prose (MD010)", fixable=True)
            if self.fix:
                lines[index - 1] = raw.replace("\t", " " * 4)
                changed = True
                self.findings[-1].fixed = True
        return changed

    def _md_blank_runs(self, path: str, lines: list[str], fenced: list[bool]) -> bool:
        """LF-004 = MD012: more than three consecutive blank lines in prose."""
        changed = False
        run_start = 0
        for index in range(len(lines) + 1):
            blank = index < len(lines) and lines[index].strip() == "" and not fenced[index]
            if not blank and run_start:
                length = index - run_start
                if length > MD012_KEEP:
                    self.report(
                        "LF-004",
                        path,
                        run_start + 1,
                        f"{length} consecutive blank lines (MD012 maximum is {MD012_KEEP})",
                        fixable=True,
                    )
                    if self.fix:
                        del lines[run_start + MD012_KEEP : index]
                        changed = True
                        self.findings[-1].fixed = True
                run_start = 0
            elif blank and not run_start:
                run_start = index
        return changed

    def _md_quote_gaps(self, path: str, lines: list[str], fenced: list[bool]) -> bool:
        """LF-005 = MD028: a blank line between two blockquote lines splits
        what markdown renders as one quote; join with a `>` spacer."""
        changed = False
        index = 1
        while index < len(lines) - 1:
            if (
                not fenced[index]
                and not fenced[index - 1]
                and not fenced[index + 1]
                and lines[index].strip() == ""
                and QUOTE_LINE.match(lines[index - 1])
                and QUOTE_LINE.match(lines[index + 1])
            ):
                self.report(
                    "LF-005",
                    path,
                    index + 1,
                    "blank line between two blockquotes (MD028)",
                    fixable=True,
                )
                if self.fix:
                    lines[index] = ">\n"
                    changed = True
                    self.findings[-1].fixed = True
                index += 3
                continue
            index += 1
        return changed

    def _md_list_blanks(self, path: str, lines: list[str], fenced: list[bool]) -> bool:
        """LF-008 = MD032, scoped to the adjacency class: two list blocks of
        different marker types (ol → ul) back to back at the same indent.
        Paragraph-interruption (a list starting after prose) is deliberately
        NOT mirrored: prose lines routinely begin with "4. " or "+ " as
        sentence/LaTeX continuations, and only a real markdown parser can
        tell them from list starts — that residual class stays with the
        markdownlint gate, which escalates instead of guessing."""
        changed = False
        insertions: list[int] = []

        def is_ordered(raw: str) -> bool:
            return bool(re.match(r"^\s*\d", raw))

        for index, raw in enumerate(lines, start=1):
            if fenced[index - 1] or index < 2:
                continue
            item = LIST_ITEM.match(raw)
            prev_item = None if index < 2 else LIST_ITEM.match(lines[index - 2])
            if item is None or prev_item is None:
                continue
            if is_ordered(lines[index - 2]) != is_ordered(raw) and len(
                prev_item.group("indent")
            ) == len(item.group("indent")):
                insertions.append(index)
        shift = 0
        for position in sorted(set(insertions)):
            self.report(
                "LF-008",
                path,
                position,
                "adjacent ordered and bullet lists need a separating blank line (MD032)",
                fixable=True,
            )
            if self.fix:
                lines.insert(position - 1 + shift, "\n")
                shift += 1
                changed = True
                self.findings[-1].fixed = True
        return changed

    def _md_img_alt(self, path: str, lines: list[str], fenced: list[bool]) -> bool:
        """LF-006 = MD045: <img> tags must carry alt text."""
        changed = False
        for index, raw in enumerate(lines, start=1):
            if fenced[index - 1] or "<img" not in raw:
                continue
            if ">" not in raw:
                self.report("LF-006", path, index, "<img> tag spans lines — add alt text by hand")
                continue
            missing = [m for m in IMG_TAG.finditer(raw) if "alt=" not in m.group("attrs")]
            if not missing:
                continue
            self.report(
                "LF-006",
                path,
                index,
                f"<img> without alt text (MD045) — {len(missing)} tag(s)",
                fixable=True,
            )
            if self.fix:

                def add_alt(match: re.Match[str]) -> str:
                    close = "/>" if match.group(0).endswith("/>") else ">"
                    return "<img" + match.group("attrs") + ' alt="image"' + close

                lines[index - 1] = IMG_TAG.sub(add_alt, raw)
                changed = True
                self.findings[-1].fixed = True
        return changed

    def _md_fence_languages(self, path: str, lines: list[str]) -> None:
        """LF-011 = MD040: an opening fence with no language is reported —
        the doctor cannot guess the language without changing intent."""
        scanner = FenceScanner()
        for index, raw in enumerate(lines, start=1):
            scanner.feed(raw)
            if scanner.opened_here and not scanner.info.strip():
                self.report(
                    "LF-011",
                    path,
                    index,
                    "fenced code block opens without a language (MD040)",
                )

    # ── LF-009: markdown table column counts ───────────────────────────────
    def check_markdown_tables(self) -> None:
        cell_split = re.compile(r"(?<!\\)\|")
        separator = re.compile(r"[|\s:\-]+")

        def cells(raw: str) -> int:
            stripped = raw.strip()
            if not (stripped.startswith("|") and stripped.endswith("|")):
                return -1
            return len(cell_split.split(stripped)) - 2

        for path in self.markdown_files():
            with open(path, encoding="utf-8") as handle:
                lines = handle.read().splitlines(keepends=True)
            scanner = FenceScanner()
            fenced = [scanner.feed(raw) for raw in lines]
            index = 0
            while index < len(lines):
                if fenced[index] or cells(lines[index]) < 1:
                    index += 1
                    continue
                if index + 1 >= len(lines) or not separator.fullmatch(lines[index + 1].strip()):
                    index += 1
                    continue
                header = cells(lines[index])
                row = index + 2
                while row < len(lines) and not fenced[row] and cells(lines[row]) >= 0:
                    if cells(lines[row]) != header and not separator.fullmatch(lines[row].strip()):
                        self.report(
                            "LF-009",
                            path,
                            row + 1,
                            f"table row has {cells(lines[row])} cells, header has "
                            f"{header} (MD056 — an unescaped | inside a cell?)",
                        )
                    row += 1
                index = row

    # ── LF-010: link fragments resolve to a heading of the same file ──────
    def check_markdown_fragments(self) -> None:
        for path in self.markdown_files():
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
            lines = text.splitlines(keepends=True)
            scanner = FenceScanner()
            fenced = [scanner.feed(raw) for raw in lines]
            slugs: dict[str, int] = {}
            for index, raw in enumerate(lines, start=1):
                if fenced[index - 1]:
                    continue
                match = HEADING_LINE.match(raw)
                if match is None:
                    continue
                slug = github_slug(match.group("text"))
                if not slug:
                    continue
                occurrence = slugs.get(slug, 0)
                slugs[slug] = occurrence + 1
                if occurrence:
                    slugs[f"{slug}-{occurrence}"] = 1
            for index, raw in enumerate(lines, start=1):
                if fenced[index - 1]:
                    continue
                for pattern in (MD_LINK_FRAGMENT, MD_HREF_FRAGMENT):
                    for match in pattern.finditer(raw):
                        fragment = urllib.parse.unquote(match.group("frag"))
                        if not fragment or fragment in slugs:
                            continue
                        self.report(
                            "LF-010",
                            path,
                            index,
                            f"link fragment #{fragment} has no matching heading (MD051)",
                        )

    # ── YML: the yamllint gate mirror ──────────────────────────────────────
    def check_yaml_gate(self) -> None:
        targets = self.workflows() + [
            p
            for p in (
                os.path.join(self.root, ".pre-commit-config.yaml"),
                os.path.join(self.root, "environment.yml"),
                os.path.join(self.root, "CITATION.cff"),
            )
            if os.path.isfile(p)
        ]
        zenodo = os.path.join(self.root, ".github", "workflows", "zenodo.yml")
        for path in targets:
            if os.path.abspath(path) == os.path.abspath(zenodo):
                continue  # .yamllint.yml ignores it (embedded JSON heredoc)
            with open(path, encoding="utf-8") as handle:
                lines = handle.read().splitlines(keepends=True)
            changed = False
            if lines and not lines[0].startswith("---"):
                self.report(
                    "YML-001",
                    path,
                    1,
                    "missing document start '---' (yamllint document-start)",
                    fixable=True,
                )
                if self.fix:
                    lines.insert(0, "---\n")
                    changed = True
                    self.findings[-1].fixed = True
            for index, raw in enumerate(lines, start=1):
                if len(raw.rstrip("\n")) > 120:
                    self.report(
                        "YML-002",
                        path,
                        index,
                        f"line longer than 120 characters ({len(raw.rstrip())} > 120)",
                    )
            if changed:
                self.write_back(path, "".join(lines))

    # ── PK: packaging drift ────────────────────────────────────────────────
    def check_ruff_per_file_ignores(self) -> None:
        """PK-001: a per-file-ignore pattern that matches no file means the
        exempted file was moved, renamed or deleted — retire the pattern."""
        if tomllib is None:
            self.report(
                "PK-001",
                os.path.join(self.root, "pyproject.toml"),
                0,
                "tomllib unavailable — per-file-ignores drift check skipped",
                advisory=True,
            )
            return
        pyproject = os.path.join(self.root, "pyproject.toml")
        if not os.path.isfile(pyproject):
            return
        with open(pyproject, "rb") as handle:
            document = tomllib.load(handle)
        patterns = (
            document.get("tool", {}).get("ruff", {}).get("lint", {}).get("per-file-ignores", {})
        )
        if not patterns:
            return
        relatives = [
            os.path.relpath(path, self.root).replace(os.sep, "/")
            for path in self.repo_files((".py",))
        ]
        for pattern in patterns:
            matches = [rel for rel in relatives if fnmatch.fnmatch(rel, pattern)]
            if not matches:
                self.report(
                    "PK-001",
                    pyproject,
                    0,
                    f"ruff per-file-ignore pattern {pattern!r} matches no file",
                )

    # ── JS: JSON validity under .github/ ───────────────────────────────────
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
        self.check_workflow_permissions()
        self.check_workflow_crons()
        self.check_action_pins()
        self.check_dependabot()
        self.check_theorem31_pins()
        self.check_stale_epsilon_occurrences()
        self.check_makefile_indentation()
        self.check_nested_duplicates()
        self.check_hygiene()
        self.check_file_hygiene()
        self.check_markdown()
        self.check_markdown_tables()
        self.check_markdown_fragments()
        self.check_yaml_gate()
        self.check_ruff_per_file_ignores()
        self.check_json()
        return 1 if any(not f.advisory and not f.fixed for f in self.findings) else 0


def render_report(doctor: RepoDoctor) -> str:
    """A compact markdown report — the artifact the workflows post into
    TrivortexBot issues when a finding survives the heal pass."""
    lines = [
        "## TrivortexBot repo doctor — findings",
        "",
        f"Repository root: `{doctor.root}`",
        "",
        "| Code | Location | Status | Finding |",
        "| --- | --- | --- | --- |",
    ]
    for finding in doctor.findings:
        status = "ADVISORY" if finding.advisory else ("FIXED" if finding.fixed else "OPEN")
        where = f"`{finding.path}:{finding.line}`" if finding.line else f"`{finding.path}`"
        message = finding.message.replace("|", "\\|")
        lines.append(f"| {finding.code} | {where} | {status} | {message} |")
    open_count = sum(1 for f in doctor.findings if not f.advisory and not f.fixed)
    lines.append("")
    lines.append(f"**{len(doctor.findings)} findings, {open_count} open after this pass.**")
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="diagnose only (no modifications)")
    parser.add_argument(
        "--fix", action="store_true", help="diagnose and apply safe repairs in place"
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--report", metavar="PATH", help="write a markdown findings report to PATH")
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
        print(f"TrivortexBot repo doctor v1.2 — mode: {mode}")
        print(f"repository: {doctor.root}")
        for finding in doctor.findings:
            flag = "[fix ]" if finding.fixed else "[adv ]" if finding.advisory else "[open]"
            print(f"{flag} {finding.code} {finding.path}:{finding.line} " f"— {finding.message}")
        open_count = sum(1 for f in doctor.findings if not f.advisory and not f.fixed)
        if doctor.rewritten:
            print(f"repaired files: {sorted(doctor.rewritten)}")
        print(f"findings: {len(doctor.findings)} " f"({open_count} open after this pass)")
    if options.report:
        with open(options.report, "w", encoding="utf-8", newline="") as handle:
            handle.write(render_report(doctor))
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
