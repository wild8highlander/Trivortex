#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — сборка dist/trivortex_master_v<version>.zip.

Включает ровно поставку: 9 пакетов + data/ + docs + сам скрипт.
Исключает __pycache__, *.pyc/.pyo, .git, runs/ (кроме .gitkeep),
logs/, dist/, временные файлы. Рядом с архивом пишет manifest
с числом файлов, суммарным размером и контрольными суммами.

Запуск:  python3 build_zip.py [--version 2.0.0] [--skip-tests]
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
VERSION = "2.0.2"

INCLUDE_DIRS = ["core", "lab", "realism", "render", "reports", "analysis", "data", "tools"]
INCLUDE_FILES = [
    "trivortex_master.py",
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "requirements-optional.txt",
    "build_zip.py",
]

EXCLUDE_DIRS = {"__pycache__", ".git", ".pytest_cache", ".mypy_cache", "dist", "logs", "runs"}
EXCLUDE_EXT = {".pyc", ".pyo", ".tmp", ".log", ".bak"}
EXCLUDE_NAMES = {".DS_Store", ".tv_ctl"}


def collect() -> list[str]:
    """Собрать относительные пути файлов поставки."""
    files: list[str] = []
    for item in INCLUDE_DIRS:
        p = os.path.join(ROOT, item)
        if not os.path.isdir(p):
            continue
        for base, dirs, names in os.walk(p):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for name in names:
                if name in EXCLUDE_NAMES:
                    continue
                if os.path.splitext(name)[1] in EXCLUDE_EXT:
                    continue
                rel = os.path.relpath(os.path.join(base, name), ROOT)
                files.append(rel)
    for name in INCLUDE_FILES:
        p = os.path.join(ROOT, name)
        if os.path.isfile(p):
            files.append(name)
    return sorted(files)


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build(version: str) -> tuple[str, dict]:
    files = collect()
    dist = os.path.join(ROOT, "dist")
    os.makedirs(dist, exist_ok=True)
    target = os.path.join(dist, f"trivortex_master_v{version}.zip")

    manifest = dict(
        version=version,
        built=_dt.datetime.now().isoformat(timespec="seconds"),
        file_count=len(files),
        total_bytes=0,
        python_lines=0,
        files=[],
    )

    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for rel in files:
            full = os.path.join(ROOT, rel)
            size = os.path.getsize(full)
            manifest["total_bytes"] += size
            if rel.endswith(".py"):
                with open(full, encoding="utf-8") as fh:
                    manifest["python_lines"] += sum(1 for _ in fh)
            manifest["files"].append(dict(path=rel, bytes=size, sha256=sha256(full)))
            arcname = os.path.join("trivortex_master", rel)
            zf.write(full, arcname)

    manifest_path = os.path.join(dist, f"manifest_v{version}.json")
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
    return target, manifest


def verify(zip_path: str) -> list[str]:
    """Целостность архива + smoke-проверка состава."""
    problems = []
    with zipfile.ZipFile(zip_path) as zf:
        if zf.testzip() is not None:
            problems.append("битые CRC в zip")
        names = zf.namelist()
        for must in (
            "trivortex_master/trivortex_master.py",
            "trivortex_master/README.md",
            "trivortex_master/LICENSE",
            "trivortex_master/data/catalog.json",
        ):
            if must not in names:
                problems.append(f"в архиве нет {must}")
        # banned
        for name in names:
            if "__pycache__" in name or name.endswith(".pyc"):
                problems.append(f"мусор в архиве: {name}")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description="Сборка ZIP поставки MASTER")
    ap.add_argument("--version", default=VERSION)
    ap.add_argument("--skip-tests", action="store_true", help="не запускать selftest перед сборкой")
    ns = ap.parse_args()

    if not ns.skip_tests:
        print("[build] прогон selftest S1–S12 …")
        ret = os.system(
            f"{sys.executable} {ROOT}/trivortex_master.py " f"--selftest > /dev/null 2>&1"
        )
        if ret != 0:
            print("[build] ✗ selftest не прошёл — сборка отменена")
            return 1
        print("[build] ✓ selftest пройден")

    target, manifest = build(ns.version)
    problems = verify(target)
    if problems:
        print("[build] ✗ проблемы архива:")
        for p in problems:
            print("   -", p)
        return 1

    print(f"[build] ✓ {os.path.relpath(target, ROOT)}")
    print(
        f"        файлов: {manifest['file_count']}, "
        f"{manifest['total_bytes'] / 1024:.0f} КБ, "
        f"строк Python: {manifest['python_lines']:,}"
    )
    print(f"        manifest: dist/manifest_v{ns.version}.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
