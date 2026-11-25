"""Регрессия №3 — коллинеарные бифуркации §10 Trivortex.lean.

Проверяется (значения γ_c = −5/4, γ_stat = −1/2 читаются из моста,
а не хардкодятся):
  [1] полином N(s, γ) = s(s−1)·M̃, M̃ = (γ+1)²(γ−1)s² + γ(4γ+5)s + (4γ+5)
      — его корни при γ = 1 равны {0, −1, 1} (s10_col_count_eq1: НЕТ
      асимметричной ветви при равных циркуляциях);
  [2] корни при γ = −1/4 равны {0, 1, 16/9, −16/5} (s10_col_count_quarter:
      обе асимметричные ветви рациональны);
  [3] вилка (pitchfork): M̃(0, γ) = 4γ + 5, нуль — ровно при γ_c = −5/4;
      проверяется тождество M̃(0,γ) − (4γ+5) ≡ 0 на сетке;
  [4] тождество дискриминанта из s10_col_disc: D = (4γ+5)(γ+2)² на сетке;
  [5] стационарная точка γ = −1/2 (s10_col_static): симметричная конфигурация
      (−d, d, 0) НЕ ДВИЖЕТСЯ под интегратором лаборатории;
  [6] асимметричное относительное равновесие Γ = (1, 1, −1/4),
      x = (1, −5/9, 16/9), ω = 27/(56π) (s10_col_asym): конфигурация
      вращается жёстко и замыкается за период 2π/ω.
"""

import math

import numpy as np
import pytest

from conftest import make_vortex_scene, pairwise_distances

pytestmark = pytest.mark.usefixtures("bridge_linked")


def col_M(s, gamma):
    """M̃(s, γ) — очищенный полином бифуркации (Trivortex.lean, s10ColM)."""
    return (gamma + 1) ** 2 * (gamma - 1) * s * s + gamma * (4 * gamma + 5) * s + (4 * gamma + 5)


def col_N(s, gamma):
    """N(s, γ) = s(s−1)·M̃(s, γ) (s10ColN)."""
    return s * (s - 1) * col_M(s, gamma)


def _real_roots(gamma, lo=-40.0, hi=40.0):
    """Все вещественные корни N(·, γ) на [lo, hi] (полином степени 4)."""
    # коэффициенты N по степеням s (пос раскрытия): соберём численно
    ss = np.linspace(lo, hi, 4001)
    vals = np.array([col_N(s, gamma) for s in ss])
    roots = []
    prev_s, prev_v = ss[0], vals[0]
    for s, v in zip(ss[1:], vals[1:]):
        if prev_v == 0.0:
            roots.append(prev_s)
        elif prev_v * v < 0:
            a, b = prev_s, s
            fa = prev_v
            for _ in range(80):  # бисекция — машинная точность
                m = 0.5 * (a + b)
                fm = col_N(m, gamma)
                if fa * fm <= 0:
                    b = m
                else:
                    a, fa = m, fm
            roots.append(0.5 * (a + b))
        prev_s, prev_v = s, v
    if vals[-1] == 0.0:
        roots.append(ss[-1])
    # дедупликация
    out = []
    for r in roots:
        if not out or abs(r - out[-1]) > 1e-8:
            out.append(r)
    return out


def test_roots_equal_circulations(testcfg):
    """[1] γ = 1: корни {0, −1, 1} — асимметричной ветви нет (s10_col_count_eq1)."""
    band = testcfg["bifurcation"]["band_root"]
    roots = _real_roots(1.0)
    expected = sorted([-1.0, 0.0, 1.0])
    assert len(roots) == 3, f"корней {len(roots)}: {roots}"
    for r, e in zip(roots, expected):
        assert abs(r - e) < band, f"корень {r} ≠ {e}"


def test_roots_quarter_circulations(testcfg):
    """[2] γ = −1/4: корни {0, 1, 16/9, −16/5} — обе асимметричные ветви
    рациональны (s10_col_count_quarter)."""
    band = testcfg["bifurcation"]["band_root"]
    roots = _real_roots(-0.25)
    expected = sorted([0.0, 1.0, 16.0 / 9.0, -16.0 / 5.0])
    assert len(roots) == 4, f"корней {len(roots)}: {roots}"
    for r, e in zip(roots, expected):
        assert abs(r - e) < band, f"корень {r} ≠ {e}"


def test_pitchfork_location(bridge, testcfg):
    """[3] вила: M̃(0, γ) = 4γ + 5 ⇒ единственная точка бифуркации
    γ_c = −5/4 (значение — из моста, s10_col_pitchfork)."""
    band = testcfg["bifurcation"]["band_identity"]
    gamma_c = bridge["gamma_pitchfork"]["value"]  # −5/4
    assert abs(col_M(0.0, gamma_c)) < band
    for g in np.linspace(-3.0, 2.0, 2001):
        assert abs(col_M(0.0, float(g)) - (4 * float(g) + 5)) < band
        if abs(float(g) - gamma_c) > 1e-6:
            assert abs(col_M(0.0, float(g))) > 0.0


def test_discriminant_identity(testcfg):
    """[4] s10_col_disc: D(γ) = γ²(4γ+5)² − 4(γ+1)²(γ−1)(4γ+5) = (4γ+5)(γ+2)²."""
    band = testcfg["bifurcation"]["band_identity"]
    for g in np.linspace(-3.0, 2.0, 2001):
        g = float(g)
        lhs = (g * (4 * g + 5)) ** 2 - 4 * ((g + 1) ** 2 * (g - 1)) * (4 * g + 5)
        rhs = (4 * g + 5) * (g + 2) ** 2
        assert abs(lhs - rhs) < band


def test_static_equilibrium(bridge, testcfg):
    """[5] γ = −1/2: коллинеарная конфигурация (−1, 1, 0) с Γ = (1, 1, −1/2)
    неподвижна (ω = 0, s10_col_static) — интегратор лаборатории подтверждает."""
    cfg = testcfg["static_gamma_half"]
    gamma = bridge["gamma_static"]["value"]  # −1/2
    d = 1.0
    positions = [(-d, 0.0), (d, 0.0), (0.0, 0.0)]
    scene = make_vortex_scene(positions, [1.0, 1.0, gamma])
    eng = scene.engine
    start = [(b.position[0], b.position[1]) for b in scene.bodies]
    n = int(round(cfg["t_total"] / cfg["dt"]))
    for _ in range(n):
        eng.step(cfg["dt"])
    drift = 0.0
    for k, b in enumerate(scene.bodies):
        drift = max(drift, math.hypot(b.position[0] - start[k][0], b.position[1] - start[k][1]))
    assert drift < cfg["band_max_drift"], f"уход стационара = {drift:.3e}"


def test_asymmetric_relative_equilibrium(testcfg):
    """[6] Γ = (1, 1, −1/4), x = (1, −5/9, 16/9), ω = 27/(56π):
    жёсткое вращение + замыкание за период (s10_col_asym)."""
    cfg = testcfg["collinear_asym"]
    xs = [1.0, -5.0 / 9.0, 16.0 / 9.0]
    gammas = [1.0, 1.0, -0.25]
    omega = 27.0 / (56.0 * math.pi)
    T = 2 * math.pi / omega

    positions = [(x, 0.0) for x in xs]
    scene = make_vortex_scene(positions, gammas)
    eng = scene.engine
    d0 = pairwise_distances(scene)
    start = [(b.position[0], b.position[1]) for b in scene.bodies]

    dt = cfg["dt"]
    n = int(round(T / dt))
    for _ in range(n):
        eng.step(dt)

    # жёсткость: парные расстояния сохранились
    d1 = pairwise_distances(scene)
    dev = max(abs(a - b) for a, b in zip(d0, d1))
    assert dev < cfg["band_dist_deviation"], f"деформация = {dev:.3e}"

    # замыкание: каждый вихрь вернулся в стартовую точку
    clos = 0.0
    for k, b in enumerate(scene.bodies):
        clos = max(clos, math.hypot(b.position[0] - start[k][0], b.position[1] - start[k][1]))
    assert clos < cfg["band_closure"], f"незамыкание = {clos:.3e}"
