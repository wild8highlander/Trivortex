#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build the study-monograph PDF library (24 PDFs).

For every one of the twelve TRX studies and both languages, the canonical
DOCX in publications/docx/ is typeset to a vector A4 PDF in
publications/pdf/, then mirrored byte-identically into the study folder as
research/<study>/monograph/monograph_<lang>.pdf.

Usage:
    python publications/build/build_pdf_library.py [--workers N]

Author: Isaev Iskhak Khamzatovich (repository owner)
License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
"""

from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor

from md2html_lib import DOCX_DIR, LANGS, STUDIES, ensure_dirs, mirror_to_study_folder, soffice_convert


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--workers", type=int, default=4,
                    help="parallel LibreOffice profiles (default 4)")
    args = ap.parse_args()
    ensure_dirs()

    jobs = [(DOCX_DIR / f"{slug}_{lang}.docx", i % args.workers)
            for i, (slug, lang) in
            enumerate((s, l) for s in STUDIES for l in LANGS)]
    missing = [str(j[0]) for j in jobs if not j[0].exists()]
    if missing:
        print("Missing canonical DOCX:", *missing, sep="\n  ")
        return 1

    ok = 0
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for (src, _idx), done in zip(jobs, ex.map(
                lambda j: soffice_convert(j[0],
                                          src.parent.parent / "pdf",
                                          j[1]), jobs)):
            ok += done
            print(f"  {'ok' if done else 'FAILED'}: {src.stem}.pdf", flush=True)

    mirrored = sum(mirror_to_study_folder(s, l)
                   for s in STUDIES for l in LANGS)
    print(f"library PDFs: {ok}/{len(jobs)}, mirrors: {mirrored}/{len(jobs)}")
    return 0 if ok == len(jobs) and mirrored == len(jobs) else 1


if __name__ == "__main__":
    sys.exit(main())
