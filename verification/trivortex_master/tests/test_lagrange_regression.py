"""Регрессия №1 — лагранжев треугольник Кирхгофа против §7/§4/§10 Lean.

Проверяется (все ожидания читаются из моста data/verified_params.json,
построенного по Trivortex.lean, — а не из хардкода):
  [A] якорные значения H = 0, P = 0, Q = 0, I = Γ (§7, a = 1, Γ = 1);
  [B] сохранение H, P, Q, I вдоль интегрирования RK4 (§4: d/dt = 0);
  [C] жёсткое вращение: форма сохраняется (все парные расстояния = a);
  [D] частота вращения ω: восстановленная из симуляции против формулы
      3Γ/(2πa²) (мост);
  [E] период T = 4π²a²/(3Γ) (мост): хореография замыкается за T.
"""
import math

import pytest

from conftest import lagrange_positions, make_vortex_scene, pairwise_distances

pytestmark = pytest.mark.usefixtures("bridge_linked")


def test_anchor_values(bridge, testcfg):
    """[A] якоря §7 в t = 0 — точные значения из моста."""
    a = 1.0
    scene = make_vortex_scene(lagrange_positions(a), [1.0, 1.0, 1.0])
    eng = scene.engine
    ints = eng.integrals()
    band = testcfg["lagrange"]["band_anchor"]
    assert abs(ints["H"] - bridge["anchor_H"]["value"]) < band
    assert abs(ints["P"] - bridge["anchor_P"]["value"]) < band
    assert abs(ints["Q"] - bridge["anchor_Q"]["value"]) < band
    assert abs(ints["I"] - bridge["anchor_I"]["value"]) < band


def test_conservation_and_rotation(bridge, testcfg):
    """[B]+[C]+[D]+[E]: интегрирование 2 периодов, RK4 лаборатории."""
    cfg = testcfg["lagrange"]
    a = 1.0
    positions = lagrange_positions(a)
    scene = make_vortex_scene(positions, [1.0, 1.0, 1.0])
    eng = scene.engine

    T = bridge["lagrange_period"]["value"]     # 4π²/3
    omega = bridge["lagrange_omega"]["value"]  # 3/(2π)
    assert T * omega == pytest.approx(2 * math.pi, rel=1e-12)

    ints0 = eng.integrals()
    d0 = pairwise_distances(scene)

    dt = cfg["dt"]
    n_steps = int(round(2 * T / dt))
    t = 0.0
    worst_H = worst_I = 0.0
    max_shape = 0.0
    for k in range(n_steps):
        eng.step(dt)
        t += dt
        if k % 25 == 0 or k == n_steps - 1:
            ints = eng.integrals()
            worst_H = max(worst_H, abs(ints["H"] - ints0["H"]))
            worst_I = max(worst_I, abs(ints["I"] - ints0["I"]))
            max_shape = max(
                max_shape,
                max(abs(dj - d0[j]) for j, dj in enumerate(pairwise_distances(scene))),
            )

    band = cfg["band_integral_drift"]
    assert worst_H < band, f"дрейф H = {worst_H:.3e} > {band}"
    assert worst_I < band, f"дрейф I = {worst_I:.3e} > {band}"
    ints_end = eng.integrals()
    assert abs(ints_end["P"] - ints0["P"]) < band
    assert abs(ints_end["Q"] - ints0["Q"]) < band

    # [C] жёсткость формы
    assert max_shape < cfg["band_shape_deviation"], (
        f"отклонение формы = {max_shape:.3e}"
    )

    # [D] частота: угловая фаза вихря 0 продвинулась на 2π·(2 периода)·ω/ω
    x0, y0 = positions[0]
    bx = scene.bodies[0].position
    theta_total = math.atan2(bx[1], bx[0]) - math.atan2(y0, x0)
    theta_total = (theta_total + 4 * math.pi) % (4 * math.pi)  # 2 оборота
    expected_phase = 4 * math.pi  # за 2T фаза = 2T·ω = 4π
    assert abs(theta_total - expected_phase) < 0.05, (
        f"фаза {theta_total:.6f} rad вместо {expected_phase}"
    )

    # [E] замыкание хореографии за один период T
    scene2 = make_vortex_scene(positions, [1.0, 1.0, 1.0])
    eng2 = scene2.engine
    n_one = int(round(T / dt))
    for _ in range(n_one):
        eng2.step(dt)
    worst_closure = 0.0
    for k, body in enumerate(scene2.bodies):
        xk, yk = positions[k]
        worst_closure = max(
            worst_closure,
            math.hypot(body.position[0] - xk, body.position[1] - yk),
        )
    assert worst_closure < cfg["band_period_closure"], (
        f"незамыкание за период = {worst_closure:.3e}"
    )


def test_omega_recovery_precision(bridge, testcfg):
    """[D+] точное восстановление ω из фазы за полпериода (узкий допуск)."""
    cfg = testcfg["lagrange"]
    positions = lagrange_positions(1.0)
    scene = make_vortex_scene(positions, [1.0, 1.0, 1.0])
    eng = scene.engine
    omega = bridge["lagrange_omega"]["value"]

    dt = cfg["dt"]
    half_T = math.pi / omega  # половина периода
    n = int(round(half_T / dt))
    for _ in range(n):
        eng.step(dt)
    bx = scene.bodies[0].position
    theta = math.atan2(bx[1], bx[0])
    # за t = π/ω фаза продвигается ровно на π
    dtheta = (theta - math.atan2(positions[0][1], positions[0][0]))
    dtheta = (dtheta + math.pi) % (2 * math.pi) - math.pi
    omega_meas = dtheta / half_T
    rel = abs(omega_meas - omega) / omega
    assert rel < 0.01, f"восстановленная ω = {omega_meas:.6f}, ω моста = {omega:.6f}"
