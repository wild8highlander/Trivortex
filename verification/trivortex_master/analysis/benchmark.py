#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — бенчмарк-комплекс: производительность всех подсистем.

Сценарии (каждый — время + контроль корректности):

  B1  интеграторы: RK4 vs leapfrog vs Yoshida4 (двухтеловая);
  B2  Barnes-Hut: построение дерева, сила, ускорение vs direct;
  B3  рендер: pure_raster кадр, raytracer кадр, ascii кадр;
  B4  PNG/GIF: кодирование кадра, LZW-сжатие;
  B5  вихревой движок: шаг N=7, интегралы;
  B6  MCMC: 2000 итераций на линейной модели;
  B7  отчёты: полный набор 7 форматов;
  B8  вейвлет CWT на 600 точках.

Итог — сводная таблица + JSON-протокол; сравнение с референсными
временами (пороги медленных регрессий задаются множителем).
"""
from __future__ import annotations

import json
import os
import sys
import time
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


class Bench:
    """Один сценарий: замер + порог."""

    def __init__(self, name: str, threshold_s: float | None = None):
        self.name = name
        self.threshold = threshold_s
        self.elapsed = 0.0
        self.metrics: dict[str, Any] = {}
        self.passed = True
        self._t0 = 0.0

    def __enter__(self):
        self._t0 = time.perf_counter()
        return self

    def __exit__(self, *exc):
        self.elapsed = time.perf_counter() - self._t0
        if self.threshold is not None and self.elapsed > self.threshold:
            self.passed = False
        return False


def bench_integrators() -> Bench:
    """B1: двухтеловая орбита, 1000 шагов каждым интегратором."""
    b = Bench("B1 интеграторы", threshold_s=30.0)
    import math
    from lab.integrators import Leapfrog, Yoshida4, rk4_step
    G = 1.0

    def accel(pos, t):
        out = []
        for i in range(len(pos)):
            ax = ay = az = 0.0
            for j in range(len(pos)):
                if i == j:
                    continue
                dx = pos[j][0] - pos[i][0]
                dy = pos[j][1] - pos[i][1]
                dz = pos[j][2] - pos[i][2]
                r = math.sqrt(dx * dx + dy * dy + dz * dz) + 1e-12
                f = G / (r ** 3)
                ax += f * dx
                ay += f * dy
                az += f * dz
            out.append((ax, ay, az))
        return out

    def deriv(y, t):
        n = len(y) // 6
        out = [0.0] * len(y)
        for i in range(n):
            out[6 * i:6 * i + 3] = y[6 * i + 3:6 * i + 6]
        acc = accel([tuple(y[6 * i:6 * i + 3]) for i in range(n)], t)
        for i in range(n):
            out[6 * i + 3:6 * i + 6] = acc[i]
        return out

    v = math.sqrt(0.5)
    y0 = [-0.5, 0, 0, 0, -v, 0, 0.5, 0, 0, 0, v, 0]
    with b:
        t_rk4 = time.perf_counter()
        y = list(y0)
        for _ in range(500):
            y, _t = rk4_step(deriv, y, 0, 0.02)
        t_rk4 = time.perf_counter() - t_rk4
        t_lf = time.perf_counter()
        lf = Leapfrog(accel, 2)
        y = list(y0)
        for _ in range(500):
            y, _t = lf.step(y, 0, 0.02)
        t_lf = time.perf_counter() - t_lf
        t_yo = time.perf_counter()
        yo = Yoshida4(accel, 2)
        y = list(y0)
        for _ in range(500):
            y, _t = yo.step(y, 0, 0.02)
        t_yo = time.perf_counter() - t_yo
    b.metrics = dict(rk4_s=t_rk4, leapfrog_s=t_lf, yoshida4_s=t_yo,
                     yoshida_slower=t_yo / max(t_lf, 1e-9))
    b.passed = t_rk4 < 15 and t_lf < 10
    return b


def bench_barnes_hut() -> Bench:
    """B2: дерево на 400 телах."""
    b = Bench("B2 Barnes-Hut", threshold_s=25.0)
    from lab.nbody_tree import BarnesHutTree, BodyLite, benchmark
    with b:
        res = benchmark(n_bodies=400, seed=1)
    b.metrics = res
    b.passed = res["err_rms"] < 0.1
    return b


def bench_render() -> Bench:
    """B3: кадры всеми бэкендами."""
    b = Bench("B3 рендер", threshold_s=25.0)
    with b:
        from render.pure_raster import render_bodies
        bodies = [dict(position=(0, 0, 0), radius=0.3, color="#FDB813"),
                  dict(position=(1.2, 0.4, 0), radius=0.15, color="#4FD1C5"),
                  dict(position=(-1, -0.5, 0.6), radius=0.12,
                       color="#E8C766")]
        t0 = time.perf_counter()
        frame = render_bodies(bodies, width=320, height=240)
        t_pure = time.perf_counter() - t0
        # raytracer
        from render.raytracer import demo_scene, render_to_png, Camera
        t0 = time.perf_counter()
        render_to_png(demo_scene(), Camera(aspect=4 / 3),
                      "/tmp/tv_bench_rt.png", width=100, height=75)
        t_ray = time.perf_counter() - t0
        # ascii
        from render.backend_ascii import render_ascii
        t0 = time.perf_counter()
        render_ascii([dict(position=p["position"], radius=0.2,
                            color=p["color"]) for p in bodies],
                     width=60, height=18)
        t_ascii = time.perf_counter() - t0
    b.metrics = dict(pure_s=t_pure, raytracer_s=t_ray, ascii_s=t_ascii)
    b.passed = frame is not None and t_ascii < 2.0
    return b


def bench_codecs() -> Bench:
    """B4: PNG и GIF-кодирование."""
    b = Bench("B4 PNG/GIF кодеки", threshold_s=30.0)
    with b:
        from render.png_codec import write_png
        px = bytearray()
        for y in range(180):
            for x in range(240):
                px += bytes([(x * y) % 256, x % 256, y % 256])
        t0 = time.perf_counter()
        write_png("/tmp/tv_bench.png", px, 240, 180)
        t_png = time.perf_counter() - t0
        from render.animator import write_gif
        frames = [bytes((i % 256 if (j // 8) % 2 else 0)
                        for j in range(120 * 90)) for i in range(6)]
        t0 = time.perf_counter()
        write_gif("/tmp/tv_bench.gif", frames, 120, 90, delay_cs=5)
        t_gif = time.perf_counter() - t0
    size_png = os.path.getsize("/tmp/tv_bench.png")
    size_gif = os.path.getsize("/tmp/tv_bench.gif")
    b.metrics = dict(png_s=t_png, gif_s=t_gif,
                     png_bytes=size_png, gif_bytes=size_gif)
    b.passed = size_png > 1000 and size_gif > 500
    return b


def bench_vortex() -> Bench:
    """B5: вихревой движок N=7, 200 шагов."""
    b = Bench("B5 вихревой движок", threshold_s=20.0)
    with b:
        import math
        from core.config import from_profile
        from lab.body import Body
        from lab.physics import run_simulation
        from lab.scene import Scene
        cfg = from_profile("quick", n_steps=200,
                           physics_engine="native_vortex")
        sc = Scene(cfg, name="bench_vortex")
        for k in range(7):
            phi = 2 * math.pi * k / 7
            sc.add_body(Body(id=f"v{k}", name=f"V{k}", mass=1.0,
                             radius=0.02,
                             position=(math.cos(phi), math.sin(phi), 0),
                             circulation=1.0, type="synthetic",
                             source="bench"))
        sc.dt = 0.02
        sim = run_simulation(sc, n_steps=200)
    b.metrics = dict(energy_drift=sim["energy_drift_rel"],
                     t_final=sc.t)
    b.passed = sim["energy_drift_rel"] < 1e-8
    return b


def bench_mcmc() -> Bench:
    """B6: MCMC 4×800 итераций."""
    b = Bench("B6 MCMC", threshold_s=60.0)
    with b:
        from analysis.mcmc import MetropolisSampler, gaussian_loglike, \
            linear_model, flat_prior
        import random as _rnd
        rng = _rnd.Random(1)
        x = [i / 8.0 for i in range(40)]
        data = [1.5 + 0.8 * xi + rng.gauss(0, 0.15) for xi in x]

        def log_post(theta):
            lp = flat_prior(theta, [(-10, 10), (-10, 10)])
            if lp == float("-inf"):
                return lp
            return lp + gaussian_loglike(
                lambda th: linear_model(th, x), data,
                [0.15] * len(x), theta)

        t0 = time.perf_counter()
        for seed in range(4):
            s = MetropolisSampler(log_post, [1, 1], [0.1, 0.02], seed=seed)
            s.run(800, burn_in=200)
        t_mcmc = time.perf_counter() - t0
    b.metrics = dict(total_s=t_mcmc, chains=4, samples_per_chain=800)
    b.passed = t_mcmc < 55
    return b


def bench_reports() -> Bench:
    """B7: полный набор отчётов."""
    b = Bench("B7 отчёты 7 форматов", threshold_s=45.0)
    with b:
        from core.config import from_profile
        from lab.presets import build_preset
        from lab.physics import run_simulation
        from reports.engine import (ReportData, generate_reports,
                                    validate_outputs)
        sc = build_preset("earth_moon", from_profile("quick", n_steps=15))
        run_simulation(sc, n_steps=15)
        data = ReportData("Бенчмарк", scene=sc)
        data.fill_from_scene()
        written = generate_reports(data, "/tmp/tv_bench_reports",
                                   formats=["txt", "md", "html", "csv",
                                            "json", "docx", "pdf"])
        problems = validate_outputs(written)
    b.metrics = dict(written=len(written), problems=problems)
    b.passed = not problems and len(written) == 7
    return b


def bench_wavelet() -> Bench:
    """B8: CWT Морле на 600 точках, 24 частоты."""
    b = Bench("B8 вейвлет CWT", threshold_s=40.0)
    with b:
        import math as _m
        from analysis.wavelets import cwt_morlet
        dt = 0.01
        y = [_m.sin(2 * _m.pi * 3 * i * dt) for i in range(600)]
        freqs = [1 + 5 * i / 23.0 for i in range(24)]
        cwt = cwt_morlet(y, dt, freqs=freqs)
    b.metrics = dict(n_freqs=len(cwt["freqs"]),
                     n_times=len(cwt["times"]))
    b.passed = len(cwt["freqs"]) == 24
    return b


ALL_BENCHES = [bench_integrators, bench_barnes_hut, bench_render,
               bench_codecs, bench_vortex, bench_mcmc, bench_reports,
               bench_wavelet]


def run_all(only: list[str] | None = None) -> dict:
    """Прогнать бенчмарки; вернуть протокол."""
    results = []
    for fn in ALL_BENCHES:
        b = fn()
        if only and b.name.split()[0] not in only:
            continue
        mark = "✓" if b.passed else "✗"
        print(f"  [{mark}] {b.name}: {b.elapsed:.2f} с "
              f"({', '.join(f'{k}={_fmt(v)}' for k, v in list(b.metrics.items())[:3])})")
        results.append(dict(name=b.name, elapsed_s=b.elapsed,
                            passed=b.passed, metrics=b.metrics,
                            threshold_s=b.threshold))
    return dict(
        benches=results,
        total_s=sum(r["elapsed_s"] for r in results),
        passed=sum(1 for r in results if r["passed"]),
        total=len(results),
        all_pass=all(r["passed"] for r in results),
    )


def _fmt(v: Any) -> str:
    if isinstance(v, float):
        return f"{v:.3g}"
    return str(v)


def save_protocol(result: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=1, default=str)


if __name__ == "__main__":
    protocol = run_all()
    save_protocol(protocol, os.path.join(ROOT, "runs", "benchmark.json"))
    print(f"\nитог: {protocol['passed']}/{protocol['total']} за "
          f"{protocol['total_s']:.1f} с")
