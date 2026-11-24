"""Регрессия №2 — линейный спектр возмущённого треугольника против §8 Lean.

V0-лестница: 6×6-матрица линеаризации (в 2π/Γ-масштабе) — ровно те шесть
строк linX1…linY3, что формализованы в Trivortex.lean (§8). Проверяется:

  [1] собственные значения: max|Re λ| ≈ 0 (спектральная устойчивость,
      классическая устойчивость Томсона N = 3) и пара чисто мнимых
      ±3i (в 2π/Γ-масштабе) — значение 3 читается из моста;
  [2] модальные тождества из теорем eig_trans1/2, eig_rot, eig_dil,
      eig_shapeU/W — векторы и образы В ТОЧНОСТИ как в запечатанных
      утверждениях;
  [3] согласованный с мостом digest: векторы хардкодятся здесь, но
      fixture bridge_linked сверяет statement_sha256 этих теорем с
      Trivortex.lean — если утверждение изменится, тест упадёт на
      рассинхронизации раньше, чем даст неверный ответ.
"""
import math

import pytest

pytestmark = pytest.mark.usefixtures("bridge_linked")

# ── шесть строк линеаризации (Trivortex.lean §8, 2π/Γ-масштаб) ──────────────
_SQ3 = math.sqrt(3.0)


def linX1(v):
    d1, e1, d2, e2, d3, e3 = v
    return 2 * e1 + _SQ3 / 2 * d2 + e2 / 2 - _SQ3 / 2 * d3 + e3 / 2


def linY1(v):
    d1, e1, d2, e2, d3, e3 = v
    return -4 * d1 + d2 / 2 - _SQ3 / 2 * e2 + d3 / 2 + _SQ3 / 2 * e3


def linX2(v):
    d1, e1, d2, e2, d3, e3 = v
    return _SQ3 / 2 * d1 + e1 / 2 - _SQ3 / 2 * d2 + 7 * e2 / 2 - e3


def linY2(v):
    d1, e1, d2, e2, d3, e3 = v
    return d1 / 2 - _SQ3 / 2 * e1 - 5 * d2 / 2 + _SQ3 / 2 * e2 - d3


def linX3(v):
    d1, e1, d2, e2, d3, e3 = v
    return -_SQ3 / 2 * d1 + e1 / 2 - e2 + _SQ3 / 2 * d3 + 7 * e3 / 2


def linY3(v):
    d1, e1, d2, e2, d3, e3 = v
    return d1 / 2 + _SQ3 / 2 * e1 - d2 - 5 * d3 / 2 - _SQ3 / 2 * e3


ROWS = [linX1, linY1, linX2, linY2, linX3, linY3]


def apply_M(v):
    return tuple(row(v) for row in ROWS)


# ── модальные векторы из запечатанных утверждений eig_* ─────────────────────
V_T1 = (1, 0, 1, 0, 1, 0)            # eig_trans1
V_T2 = (0, 1, 0, 1, 0, 1)            # eig_trans2
V_R = (0, 1 / _SQ3, -1 / 2, -1 / (2 * _SQ3), 1 / 2, -1 / (2 * _SQ3))  # eig_rot
V_D = (1 / _SQ3, 0, -1 / (2 * _SQ3), 1 / 2, -1 / (2 * _SQ3), -1 / 2)  # eig_dil
V_U = (1, 0, 1 / 2, -_SQ3 / 2, 0, 0)  # eig_shapeU
V_W = (0, 1, _SQ3 / 2, 1 / 2, 0, 0)   # eig_shapeW


def _sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def _scale(a, k):
    return tuple(x * k for x in a)


def _maxabs(a):
    return max(abs(x) for x in a)


def test_translation_pair(testcfg):
    """eig_trans1/2: M vT1 = −3·vT2, M vT2 = +3·vT1 (собственные значения ±3i)."""
    band = testcfg["linear_spectrum"]["band_modal"]
    assert _maxabs(_sub(apply_M(V_T1), _scale(V_T2, -3))) < band
    assert _maxabs(_sub(apply_M(V_T2), _scale(V_T1, +3))) < band


def test_phase_mode(testcfg):
    """eig_rot: M vR = 0 — фазовая мода, нулевое собственное значение."""
    assert _maxabs(apply_M(V_R)) < testcfg["linear_spectrum"]["band_modal"]


def test_size_drift_jordan(testcfg):
    """eig_dil: M vD = −6·vR — жорданова цепочка: дрейф размера растёт
    ЛИНЕЙНО (не экспоненциально) — классическая устойчивость Томсона."""
    band = testcfg["linear_spectrum"]["band_modal"]
    assert _maxabs(_sub(apply_M(V_D), _scale(V_R, -6))) < band


def test_shape_oscillation(testcfg):
    """eig_shapeU/W: M u = −3·w, M w = +3·u — колебание формы на ±3i."""
    band = testcfg["linear_spectrum"]["band_modal"]
    assert _maxabs(_sub(apply_M(V_U), _scale(V_W, -3))) < band
    assert _maxabs(_sub(apply_M(V_W), _scale(V_U, +3))) < band


def test_spectrum_is_purely_imaginary(bridge, testcfg):
    """[1] max|Re λ| ≈ 0; ненулевые собственные значения = ±3i·k, k ∈ {1} —
    значение 3 приходит из моста (2π/Γ-масштаб §8)."""
    import numpy as np

    M = np.zeros((6, 6))
    for j in range(6):
        e = np.zeros(6)
        e[j] = 1.0
        M[:, j] = [row(e) for row in ROWS]
    lam = np.linalg.eigvals(M)
    bands = testcfg["linear_spectrum"]
    max_re = float(np.max(np.abs(lam.real)))
    assert max_re < bands["band_re"], f"max|Re λ| = {max_re:.3e} — рост!"

    eig3 = bridge["eig_translation"]["value"]  # = 3
    imags = sorted(abs(float(l.imag)) for l in lam)
    # порог отделяет настоящие моды (3) от числового шума жордановых нулей (~1e-8)
    nonzero = [v for v in imags if v > eig3 * 1e-3]
    assert nonzero == pytest.approx([eig3] * 4, abs=1e-6), (
        f"модули мнимых частей {nonzero} ≠ 4×{eig3}"
    )
    # ровно две (почти) нулевые моды — фазовая и размерная (жорданова цепочка)
    assert sum(1 for v in imags if v <= eig3 * 1e-3) == 2
