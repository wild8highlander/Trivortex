#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build the two special publications (4 PDFs): the executable core as a book
and the research program compendium, in both Russian and English.

Usage:
    python publications/build/build_special_pdfs.py [--workers N]

Author: Isaev Iskhak Khamzatovich (repository owner)
License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
"""

from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor

from md2html_lib import DOCX_DIR, LANGS, SPECIALS, ensure_dirs, soffice_convert


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--workers", type=int, default=2,
                    help="parallel LibreOffice profiles (default 2)")
    args = ap.parse_args()
    ensure_dirs()

    pdf_dir = DOCX_DIR.parent / "pdf"
    jobs = [(DOCX_DIR / f"{name}_{lang}.docx", i % args.workers)
            for i, (name, lang) in
            enumerate((n, l) for n in SPECIALS for l in LANGS)]
    missing = [str(j[0]) for j in jobs if not j[0].exists()]
    if missing:
        print("Missing canonical DOCX:", *missing, sep="\n  ")
        return 1

    ok = 0
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for (src, _idx), done in zip(jobs, ex.map(
                lambda j: soffice_convert(j[0], pdf_dir, j[1]), jobs)):
            ok += done
            print(f"  {'ok' if done else 'FAILED'}: {src.stem}.pdf", flush=True)
    print(f"special PDFs: {ok}/{len(jobs)}")
    return 0 if ok == len(jobs) else 1


if __name__ == "__main__":
    sys.exit(main())
