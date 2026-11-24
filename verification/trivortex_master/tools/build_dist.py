#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — сборка дистрибутива v2.0.2.

  1. Прогон всех проверок (selftest + приёмка + gate) — сборка только
     из зелёного состояния;
  2. генерация примеров (make_examples) и документации (API.md,
     RELEASE_v2.0.md);
  3. ZIP + tar.gz с манифестом v2.0.2 (список файлов, sha256, размеры);
  4. копирование в /home/z/my-project/download/.

Версия: 2.0.0 (удвоенный объём).
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import zipfile
import datetime as _dt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

DOWNLOAD = "/home/z/my-project/download"
VERSION = "2.0.2"

EXCLUDE_DIRS = {"__pycache__", "runs", ".git", "data/cache"}
EXCLUDE_EXT = {".pyc", ".pyo"}


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_files() -> list[str]:
    """Все файлы пакета без исключений."""
    out = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fn in sorted(files):
            if os.path.splitext(fn)[1] in EXCLUDE_EXT:
                continue
            out.append(os.path.join(base, fn))
    return sorted(out)


def preflight() -> dict:
    """Прогон selftest + приёмки; сборка прерывается при провале."""
    from analysis.tests import run_all as run_selftest

    st = run_selftest(verbose=False)
    if not st["all_pass"]:
        raise SystemExit(f"selftest провален: {st['passed']}/{st['total']}")
    res = subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "verify_package.py")],
        capture_output=True,
        text=True,
        timeout=1200,
    )
    tail = (res.stdout or "").strip().splitlines()[-1:]
    if res.returncode != 0:
        raise SystemExit(f"приёмка провалена: {tail}")
    return dict(
        selftest=st["passed"], selftest_total=st["total"], acceptance=tail[0] if tail else "OK"
    )


def build_examples() -> dict:
    """Примеры артефактов в runs/examples."""
    from tools.make_examples import make_examples

    return make_examples()


def build_docs() -> dict:
    """API-справочник + релизные заметки."""
    from analysis.api_reference import write_api_doc
    from tools.release_notes import write_release_notes

    api = write_api_doc(version=VERSION)
    rel = write_release_notes(version=VERSION)
    return dict(api_md=api, release_md=rel)


def build_dist() -> dict:
    """ZIP + tar.gz + манифест."""
    files = collect_files()
    manifest = dict(
        version=VERSION,
        built=_dt.datetime.now().isoformat(timespec="seconds"),
        file_count=len(files),
        python_lines=0,
        files=[],
    )
    for path in files:
        rel = os.path.relpath(path, ROOT)
        size = os.path.getsize(path)
        manifest["files"].append(dict(path=rel, bytes=size, sha256=sha256(path)))
        if rel.endswith(".py"):
            manifest["python_lines"] += sum(1 for _ in open(path, encoding="utf-8"))

    os.makedirs(DOWNLOAD, exist_ok=True)
    zip_path = os.path.join(DOWNLOAD, f"trivortex_master_v{VERSION}.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, os.path.join("trivortex_master", os.path.relpath(path, ROOT)))
    tgz_path = os.path.join(DOWNLOAD, f"trivortex_master_v{VERSION}_sources.tar.gz")
    with tarfile.open(tgz_path, "w:gz") as tf:
        for path in files:
            tf.add(path, arcname=os.path.join("trivortex_master", os.path.relpath(path, ROOT)))
    # манифест (включая сами архивы)
    for artifact in (zip_path, tgz_path):
        manifest["files"].append(
            dict(
                path=os.path.basename(artifact),
                bytes=os.path.getsize(artifact),
                sha256=sha256(artifact),
            )
        )
    manifest["file_count"] = len(manifest["files"])
    manifest["total_bytes"] = sum(f["bytes"] for f in manifest["files"])
    manifest_path = os.path.join(DOWNLOAD, f"manifest_v{VERSION}.json")
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
    return dict(
        zip=zip_path,
        tgz=tgz_path,
        manifest=manifest_path,
        n_files=len(files),
        py_lines=manifest["python_lines"],
        total_bytes=manifest["total_bytes"],
    )


def copy_examples() -> list[str]:
    """Примеры в download/examples (перезапись)."""
    src = os.path.join(ROOT, "runs", "examples")
    dst = os.path.join(DOWNLOAD, "examples")
    copied = []
    if os.path.isdir(src):
        os.makedirs(dst, exist_ok=True)
        for fn in sorted(os.listdir(src)):
            s = os.path.join(src, fn)
            if os.path.isfile(s):
                shutil.copy2(s, os.path.join(dst, fn))
                copied.append(fn)
    # новые примеры v2: рейтрейсер + карта неба + corner-текст
    from render.raytracer import demo_scene, render_to_png, Camera

    png = os.path.join(dst, "raytracer_demo.png")
    render_to_png(demo_scene(), Camera(aspect=4 / 3), png, width=160, height=120)
    copied.append(os.path.basename(png))
    from render.ascii_sky import bind_astronomy, sky_map_ascii
    from realism.bright_stars import BRIGHT_STARS
    from realism.sky_coordinates import (
        angular_separation,
        equatorial_to_horizontal,
    )

    # S3: render не импортирует realism — каталог инъектируется здесь
    bind_astronomy(lambda: BRIGHT_STARS, equatorial_to_horizontal, angular_separation)
    sky = sky_map_ascii(55.75, 1.5708)
    with open(os.path.join(dst, "sky_map_55N.txt"), "w", encoding="utf-8") as fh:
        fh.write(sky)
    copied.append("sky_map_55N.txt")
    return copied


def main() -> int:
    print("── СБОРКА v2.0.2 ─────────────────────────────")
    pf = preflight()
    print(
        f"preflight: selftest {pf['selftest']}/{pf['selftest_total']}, "
        f"приёмка: {pf['acceptance']}"
    )
    ex = build_examples()
    print(f"примеры: {len(ex)} артефактов")
    docs = build_docs()
    print(f"документация: API.md + RELEASE_v2.0.md")
    dist = build_dist()
    print(
        f"дистрибутив: {dist['n_files']} файлов, "
        f"{dist['py_lines']} строк Python, "
        f"{dist['total_bytes'] / 1e6:.1f} МБ"
    )
    copied = copy_examples()
    print(f"копии примеров в download/examples: {len(copied)}")
    print(f"ZIP: {dist['zip']}")
    print(f"TGZ: {dist['tgz']}")
    print(f"манифест: {dist['manifest']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
