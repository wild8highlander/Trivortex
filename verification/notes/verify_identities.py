#!/usr/bin/env python3
"""Symbolic pre-verification of every identity planned for Trivortex.lean v2.0.

Mirrors verify.py conventions:
  Kirchhoff RHS:  dx_i = -1/(2pi) * sum_{j!=i} G_j (y_i - y_j)/D_ij
                 dy_i = +1/(2pi) * sum_{j!=i} G_j (x_i - x_j)/D_ij
  D_ij = (x_i-x_j)^2 + (y_i-y_j)^2
  H = -(1/2pi) * sum_{i<j} G_i G_j ln r_ij,  r = sqrt(D)
  P = sum G x,  Q = sum G y,  I = sum G |z|^2
  Lagrange omega = 3 G / (2 pi a^2)

Checks (all must print True):
  1. dP/dt = 0 (substituted velocities, cleared denominators)
  2. dQ/dt = 0
  3. dI/dt = 0
  4. dH/dt = 0  (via per-pair log-dist derivatives d ln r_ij / dt)
  5. Lagrange: rotating equilateral satisfies Kirchhoff velocities with w = 3G/(2 pi a^2)
  6. eps regime: eps = 1/(exp(C/pi)-1) < 1 iff C > pi ln 2 (numeric spot check only)
"""
import sympy as sp

x1, y1, x2, y2, x3, y3 = sp.symbols("x1 y1 x2 y2 x3 y3", real=True)
g1, g2, g3 = sp.symbols("g1 g2 g3", real=True)
pi = sp.pi

D12 = (x1 - x2) ** 2 + (y1 - y2) ** 2
D13 = (x1 - x3) ** 2 + (y1 - y3) ** 2
D23 = (x2 - x3) ** 2 + (y2 - y3) ** 2

# Kirchhoff velocities (verify.py vortex_rhs)
kx1 = -(g2 * (y1 - y2) / D12 + g3 * (y1 - y3) / D13) / (2 * pi)
ky1 = +(g2 * (x1 - x2) / D12 + g3 * (x1 - x3) / D13) / (2 * pi)
kx2 = -(g1 * (y2 - y1) / D12 + g3 * (y2 - y3) / D23) / (2 * pi)
ky2 = +(g1 * (x2 - x1) / D12 + g3 * (x2 - x3) / D23) / (2 * pi)
kx3 = -(g1 * (y3 - y1) / D13 + g2 * (y3 - y2) / D23) / (2 * pi)
ky3 = +(g1 * (x3 - x1) / D13 + g2 * (x3 - x2) / D23) / (2 * pi)

ok = True

# --- P, Q, I ---
dP = g1 * kx1 + g2 * kx2 + g3 * kx3
dQ = g1 * ky1 + g2 * ky2 + g3 * ky3
dI = 2 * (g1 * (x1 * kx1 + y1 * ky1) + g2 * (x2 * kx2 + y2 * ky2)
          + g3 * (x3 * kx3 + y3 * ky3))
for name, expr in (("dP/dt", dP), ("dQ/dt", dQ), ("dI/dt", dI)):
    cleared = sp.simplify(sp.together(expr * (2 * pi) * D12 * D13 * D23))
    good = sp.simplify(cleared) == 0
    ok &= good
    print(f"{name} == 0 (after clearing denominators): {good}")

# --- H: dH/dt = -(1/2pi) sum_{i<j} G_i G_j * d(ln r_ij)/dt,
#     d ln r_ij / dt = ((xi-xj)(dxi-dxj) + (yi-yj)(dyi-dyj)) / D_ij
dln12 = ((x1 - x2) * (kx1 - kx2) + (y1 - y2) * (ky1 - ky2)) / D12
dln13 = ((x1 - x3) * (kx1 - kx3) + (y1 - y3) * (ky1 - ky3)) / D13
dln23 = ((x2 - x3) * (kx2 - kx3) + (y2 - y3) * (ky2 - ky3)) / D23
dH = -(g1 * g2 * dln12 + g1 * g3 * dln13 + g2 * g3 * dln23) / (2 * pi)
cleared = sp.simplify(sp.together(dH * (2 * pi) ** 2 * D12 * D13 * D23))
good = sp.simplify(cleared) == 0
ok &= good
print(f"dH/dt == 0 (after clearing denominators):     {good}")

# --- Lagrange solution: rotating equilateral, R = a/sqrt(3), w = 3G/(2 pi a^2)
a, w, t = sp.symbols("a w t", positive=True)
R = a / sp.sqrt(3)
G = sp.symbols("G", positive=True)
X = [R * sp.cos(w * t + 2 * pi * k / 3) for k in range(3)]
Y = [R * sp.sin(w * t + 2 * pi * k / 3) for k in range(3)]
w_lag = 3 * G / (2 * pi * a ** 2)

# pairwise distances stay a^2 (equilateral) and centroid is zero
for (i, j) in ((0, 1), (1, 2), (2, 0)):
    Dij = sp.simplify((X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2)
    good = sp.simplify(Dij - a ** 2) == 0
    ok &= good
    print(f"D_{i}{j}(t) == a^2 for all t:                    {good}")
good = sp.simplify(X[0] + X[1] + X[2]) == 0 and sp.simplify(Y[0] + Y[1] + Y[2]) == 0
ok &= good
print(f"centroid == 0 for all t:                        {good}")

# Kirchhoff velocity of vortex 0 at the rotating state equals -w*y0 / +w*x0
D01 = a ** 2
D02 = a ** 2
kx0_lag = -(G * (Y[0] - Y[1]) / D01 + G * (Y[0] - Y[2]) / D02) / (2 * pi)
ky0_lag = +(G * (X[0] - X[1]) / D01 + G * (X[0] - X[2]) / D02) / (2 * pi)
good = sp.simplify(sp.trigsimp(kx0_lag + w_lag * Y[0])) == 0 and \
       sp.simplify(sp.trigsimp(ky0_lag - w_lag * X[0])) == 0
ok &= good
print(f"Kirchhoff(x,y) == (-w*y0, +w*x0) with w=3G/(2 pi a^2): {good}")

# and the rigid-rotation kinematic velocities match (dx0 = -w y0, dy0 = +w x0)
dx0 = sp.diff(X[0], t)
dy0 = sp.diff(Y[0], t)
good = sp.simplify(sp.trigsimp(dx0 + w * Y[0])) == 0 and \
       sp.simplify(sp.trigsimp(dy0 - w * X[0])) == 0
ok &= good
print(f"kinematic velocities == (-w*y0, +w*x0):           {good}")

# --- eps regime spot check (float) ---
import math
C = 1.0
eps_val = 1.0 / (math.exp(C / math.pi) - 1.0)
print(f"eps(C=1) = {eps_val:.10f}  (repo README table says 0.7276..., "
      f"e^-1/pi = {math.exp(-1/math.pi):.10f} -> mismatch documented)")
print(f"eps < 1 iff C > pi*ln2 = {math.pi*math.log(2):.6f}: "
      f"C=2.2 -> eps={1.0/(math.exp(2.2/math.pi)-1):.4f}")

print("\nALL IDENTITIES:", "TRUE" if ok else "FALSE — FIX BEFORE LEAN")
