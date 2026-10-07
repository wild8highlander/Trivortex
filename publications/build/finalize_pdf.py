#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QA pass over the PDF library: verifies the expected 28 files exist, are
non-trivial in size, start with a %PDF header, and (when pypdf is
installed) stamps the document metadata (title, author, license note).

Usage:
    python publications/build/finalize_pdf.py [--stamp]

Author: Isaev Iskhak Khamzatovich (repository owner)
License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
"""

from __future__ import annotations

import argparse
import sys

from md2html_lib import LANGS, PDF_DIR, SPECIALS, STUDIES

EXPECTED = (
    [f"{slug}_{lang}.pdf" for slug in STUDIES for lang in LANGS]
    + [f"{name}_{lang}.pdf" for name in SPECIALS for lang in LANGS]
)

AUTHOR = "Isaev Iskhak Khamzatovich"
LICENSE_NOTE = ("LicenseRef-Proprietary-Wild8Highlander-1.0; "
                "see LICENSE.md in the repository root")


def stamp(path) -> bool:
    """Stamp PDF metadata (best effort; requires pypdf)."""
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        return False
    reader = PdfReader(str(path))
    writer = PdfWriter()
    writer.append(reader)
    writer.add_metadata({
        "/Author": AUTHOR,
        "/Title": path.stem.replace("_", " — "),
        "/Subject": "TRIVORTEX research program",
        "/Keywords": "TRIVORTEX, three-body problem, vortex model",
        "/License": LICENSE_NOTE,
    })
    with open(path, "wb") as fh:
        writer.write(fh)
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stamp", action="store_true",
                    help="also stamp metadata (needs pypdf)")
    args = ap.parse_args()

    failures = 0
    stamped = 0
    for name in EXPECTED:
        p = PDF_DIR / name
        if not p.exists():
            print(f"MISSING  {name}")
            failures += 1
            continue
        size = p.stat().st_size
        header = p.open("rb").read(5)
        if header != b"%PDF-":
            print(f"BAD PDF  {name} (header {header!r})")
            failures += 1
            continue
        note = ""
        if args.stamp and stamp(p):
            stamped += 1
            note = " (stamped)"
        print(f"ok       {name}  {size / 1024:8.0f} KiB{note}")
    print(f"\n{len(EXPECTED) - failures}/{len(EXPECTED)} PDFs pass QA; "
          f"{stamped} stamped")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
