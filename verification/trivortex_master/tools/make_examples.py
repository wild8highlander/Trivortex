#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерация демонстрационных артефактов: GIF, графики, отчёты всех форматов.

Запускается build_zip.py перед сборкой, чтобы в поставке были живые
примеры работы комплекса. Всё на stdlib + matplotlib при наличии.
"""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from core.config import from_profile
from lab.presets import build_preset
from lab.physics import run_simulation
from render.animator import animate_scene
from render.engine import get_backend
from reports.engine import ReportData, generate_reports, validate_outputs


def make_examples(out_dir: str | None = None) -> dict:
    out = out_dir or os.path.join(ROOT, "runs", "examples")
    os.makedirs(out, exist_ok=True)
    made = {}

    # 1) figure-eight: GIF
    scene = build_preset("figure_eight", from_profile("quick", n_steps=240))
    run_simulation(scene, n_steps=240)
    res = animate_scene(
        scene,
        os.path.join(out, "figure_eight.gif"),
        n_frames=24,
        fps=10,
        backend="pure",
        width=320,
        height=240,
    )
    made["gif"] = res["bytes"]

    # 2) Лагранж: полный набор графиков + отчёты 7 форматов
    scene2 = build_preset("lagrange_triangle", from_profile("quick", n_steps=300))
    sim = run_simulation(scene2, n_steps=300)
    eng = get_backend("mpl", scene2.config)
    eng.setup(scene2)
    charts = eng.render_trajectory(out, prefix="lagrange")
    data = ReportData(
        "Демонстрация: треугольник Лагранжа",
        scene=scene2,
        sim_summary={k: str(v)[:28] for k, v in sim.items()},
    )
    data.fill_from_scene()
    for p in charts:
        data.add_chart(p, os.path.basename(p))
    written = generate_reports(
        data, out, formats=["txt", "md", "html", "csv", "json", "docx", "pdf"]
    )
    problems = validate_outputs(written)
    made["reports"] = {k: os.path.getsize(v) for k, v in written.items()}
    made["problems"] = problems

    # 3) вихревое кольцо N=7: GIF
    scene3 = build_preset("vortex_ring_7", from_profile("quick", n_steps=240))
    run_simulation(scene3, n_steps=240)
    res3 = animate_scene(
        scene3,
        os.path.join(out, "vortex_ring7.gif"),
        n_frames=24,
        fps=10,
        backend="pure",
        width=320,
        height=240,
    )
    made["gif_ring7"] = res3["bytes"]
    return made


if __name__ == "__main__":
    print(make_examples())
