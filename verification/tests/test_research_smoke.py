#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smoke tests for the extended research program (research/TRX-*).

Runs every study script in --smoke mode (fast CI settings) and asserts:
  * exit code 0 (all acceptance checks passed);
  * the JSON protocol reports status PASS.

Author: Isaev Iskhak Khamzatovich (repository owner)
License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
RESEARCH = REPO_ROOT / "research"

STUDIES = sorted(p for p in RESEARCH.glob("TRX-*") if p.is_dir() and list(p.glob("code/trx*.py")))


@pytest.mark.parametrize("study_dir", STUDIES, ids=lambda p: p.name)
def test_research_study_smoke(study_dir: Path):
    scripts = sorted(study_dir.glob("code/trx*.py"))
    assert scripts, f"no study script found in {study_dir}"
    script = scripts[0]
    result = subprocess.run(
        [sys.executable, str(script), "--smoke"],
        capture_output=True,
        text=True,
        timeout=300,
        cwd=str(script.parent),
    )
    assert result.returncode == 0, (
        f"{script.name} --smoke failed (exit {result.returncode}):\n"
        f"{result.stdout[-4000:]}\n{result.stderr[-2000:]}"
    )
    protocol_file = study_dir / "results" / f"trx{script.stem.split('_')[0][3:]}_results.json"
    if protocol_file.exists():
        protocol = json.loads(protocol_file.read_text(encoding="utf-8"))
        assert (
            protocol.get("status") == "PASS"
        ), f"{study_dir.name}: protocol status = {protocol.get('status')}"


def test_research_program_completeness():
    """All twelve studies must exist with README, code and results."""
    expected = [
        "TRX-01-laser-radiation-pressure",
        "TRX-02-three-wave-mixing",
        "TRX-03-soliton-molecule",
        "TRX-04-photon-fluid",
        "TRX-05-optical-vortices",
        "TRX-06-helium-three-body",
        "TRX-07-efimov",
        "TRX-08-ion-trap",
        "TRX-09-vortex-trio",
        "TRX-10-kozai-lidov",
        "TRX-11-gw-choreography",
        "TRX-12-laser-light-sail",
    ]
    for name in expected:
        d = RESEARCH / name
        assert (d / "README.md").exists(), f"missing {name}/README.md"
        assert list(d.glob("code/trx*.py")), f"missing {name}/code script"
        assert (d / "README.md").read_text(encoding="utf-8"), f"empty {name}/README.md"
        # v1.0.0 monograph layout: bilingual sources + per-language renditions
        assert (d / "pack.py").exists(), f"missing {name}/pack.py"
        assert list(d.glob("figures/scheme_*.svg")), f"missing {name}/figures scheme SVG"
        assert len(list(d.glob("figures/fig*.png"))) == 4, f"{name}: expected 4 PNG figures"
        assert (
            d / "monograph" / "monograph_EN.md"
        ).exists(), f"missing {name}/monograph/monograph_EN.md"
        assert (
            d / "monograph" / "monograph_RU.md"
        ).exists(), f"missing {name}/monograph/monograph_RU.md"
        # monograph renditions: PDF + DOCX, Russian and English separately
        for lang in ("EN", "RU"):
            for ext in ("pdf", "docx"):
                f = d / "monograph" / f"monograph_{lang}.{ext}"
                assert f.exists(), f"missing {name}/monograph/monograph_{lang}.{ext}"
    assert len(STUDIES) == 12


def test_publications_library():
    """v1.0.0 reading room: per-language PDF + DOCX library, build system."""
    repo = Path(__file__).resolve().parents[2]

    # orbital animations (GIF + MP4 per choreography)
    anim = repo / "docs" / "animations"
    for name in (
        "anim01_trivortex_ring",
        "anim02_figure_eight",
        "anim03_lagrange_triangle",
        "anim04_laser_stationkeeping",
    ):
        assert (anim / f"{name}.gif").exists(), f"missing {name}.gif"
        assert (anim / f"{name}.mp4").exists(), f"missing {name}.mp4"
    assert (anim / "make_animations.py").exists()
    assert (anim / "README.md").exists()

    studies = [
        "TRX-01-laser-radiation-pressure",
        "TRX-02-three-wave-mixing",
        "TRX-03-soliton-molecule",
        "TRX-04-photon-fluid",
        "TRX-05-optical-vortices",
        "TRX-06-helium-three-body",
        "TRX-07-efimov",
        "TRX-08-ion-trap",
        "TRX-09-vortex-trio",
        "TRX-10-kozai-lidov",
        "TRX-11-gw-choreography",
        "TRX-12-laser-light-sail",
    ]

    # publication PDFs: 12 studies x {RU, EN} + core x {RU, EN} + compendium x {RU, EN}
    pdf_dir = repo / "publications" / "pdf"
    pdfs = sorted(p.name for p in pdf_dir.glob("*.pdf"))
    assert len(pdfs) == 28, f"expected 28 publication PDFs, found {len(pdfs)}"
    for core in (
        "TRIVORTEX-Core-Monograph_RU.pdf",
        "TRIVORTEX-Core-Monograph_EN.pdf",
        "TRIVORTEX-Research-Compendium_RU.pdf",
        "TRIVORTEX-Research-Compendium_EN.pdf",
    ):
        assert core in pdfs, f"missing {core}"
    for name in studies:
        for lang in ("RU", "EN"):
            assert f"{name}_{lang}.pdf" in pdfs, f"missing publication PDF for {name} ({lang})"
        # editable HTML source ships next to every study PDF
        assert (
            repo / "publications" / "html" / f"{name}.html"
        ).exists(), f"missing HTML source for {name}"

    # DOCX mirror: same 28 documents in editable Word form
    docx_dir = repo / "publications" / "docx"
    docx = sorted(p.name for p in docx_dir.glob("*.docx"))
    assert len(docx) == 28, f"expected 28 publication DOCX, found {len(docx)}"
    assert "TRIVORTEX-Core-Monograph_RU.docx" in docx
    for name in studies:
        for lang in ("RU", "EN"):
            assert f"{name}_{lang}.docx" in docx, f"missing publication DOCX for {name} ({lang})"

    # build system + reading-room guide
    for b in ("md2html_lib.py", "build_pdf_library.py", "build_special_pdfs.py", "finalize_pdf.py"):
        assert (repo / "publications" / "build" / b).exists(), f"missing {b}"
    assert (repo / "publications" / "README.md").exists()
