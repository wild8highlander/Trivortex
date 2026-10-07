#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shared helpers for the TRIVORTEX publications build system.

The reading room ships every monograph in two renditions: a vector PDF
(typeset from the canonical DOCX) and the editable DOCX itself.  The build
scripts in this directory share the discovery logic below:

    md2html_lib.py       pandoc-based Markdown -> HTML with repo styling
    build_pdf_library.py the twelve study monographs (24 PDFs)
    build_special_pdfs.py core monograph + compendium (4 PDFs)
    finalize_pdf.py      metadata stamping + QA report

Author: Isaev Iskhak Khamzatovich (repository owner)
License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
"""

from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCX_DIR = REPO_ROOT / "publications" / "docx"
PDF_DIR = REPO_ROOT / "publications" / "pdf"
HTML_DIR = REPO_ROOT / "publications" / "html"
SRC_DIR = REPO_ROOT / "publications" / "src"
RESEARCH = REPO_ROOT / "research"

STUDIES = [
    "TRX-01-laser-radiation-pressure", "TRX-02-three-wave-mixing",
    "TRX-03-soliton-molecule", "TRX-04-photon-fluid",
    "TRX-05-optical-vortices", "TRX-06-helium-three-body",
    "TRX-07-efimov", "TRX-08-ion-trap", "TRX-09-vortex-trio",
    "TRX-10-kozai-lidov", "TRX-11-gw-choreography",
    "TRX-12-laser-light-sail",
]
SPECIALS = [
    "TRIVORTEX-Core-Monograph", "TRIVORTEX-Research-Compendium",
]
LANGS = ("RU", "EN")


def ensure_dirs() -> None:
    """Create the output directories if they are missing."""
    for d in (PDF_DIR, HTML_DIR):
        d.mkdir(parents=True, exist_ok=True)


def soffice_convert(src: Path, outdir: Path, profile_index: int = 0) -> bool:
    """Convert *src* (DOCX) to PDF with a headless LibreOffice instance.

    A dedicated user profile per worker index allows running several
    conversions in parallel without profile-lock clashes.
    """
    expected = outdir / (src.stem + ".pdf")
    if expected.exists():
        return True
    profile = f"/tmp/lo_profile_{profile_index}"
    r = subprocess.run(
        ["soffice", "--headless", "--norestore",
         f"-env:UserInstallation=file://{profile}",
         "--convert-to", "pdf:writer_pdf_Export",
         "--outdir", str(outdir), str(src)],
        capture_output=True, text=True, timeout=300,
    )
    return expected.exists()


def mirror_to_study_folder(slug: str, lang: str) -> bool:
    """Copy publications/pdf/<slug>_<lang>.pdf next to the monograph sources."""
    src = PDF_DIR / f"{slug}_{lang}.pdf"
    dst = RESEARCH / slug / "monograph" / f"monograph_{lang}.pdf"
    if not src.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.read_bytes() == src.read_bytes():
        return True
    dst.write_bytes(src.read_bytes())
    return True


STYLE = """
body{font-family:Georgia,serif;max-width:860px;margin:2rem auto;
     padding:0 1.2rem;line-height:1.55;color:#1a1a2e}
h1,h2,h3{font-family:'Iowan Old Style',Georgia,serif;color:#0f2557}
table{border-collapse:collapse;margin:1rem auto}
td,th{border:1px solid #c9c9d6;padding:.35rem .6rem}
code,pre{font-family:'JetBrains Mono',Consolas,monospace;font-size:.92em}
pre{background:#f4f4f8;padding:.8rem;border-radius:6px;overflow-x:auto}
img{max-width:100%}
"""


def md2html(src: Path, dst: Path | None = None, title: str = "") -> Path:
    """Convert a Markdown source to styled HTML via pandoc."""
    dst = dst or HTML_DIR / (src.stem + ".html")
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["pandoc", str(src), "-f", "gfm", "-t", "html5", "-s",
           "--metadata", f"title={title or src.stem}",
           "-o", str(dst)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"pandoc failed: {r.stderr[:400]}")
    html = dst.read_text(encoding="utf-8")
    if "</head>" in html and "body{" not in html:
        html = html.replace("</head>",
                            f"<style>{STYLE}</style></head>")
        dst.write_text(html, encoding="utf-8")
    return dst


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(
        description="Convert monograph Markdown sources to styled HTML.")
    ap.add_argument("sources", nargs="+", help="*.md files to convert")
    ap.add_argument("--outdir", default=str(HTML_DIR))
    args = ap.parse_args()
    for s in args.sources:
        out = md2html(Path(s), Path(args.outdir) / (Path(s).stem + ".html"))
        print(f"ok: {out}")
