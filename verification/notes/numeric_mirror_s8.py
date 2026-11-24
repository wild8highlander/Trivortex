#!/usr/bin/env python3
"""Numeric mirror of the Section 8 theorems (Trivortex.lean v4.0).

Section 8 = linear stability of the Lagrange triangle in the frame
co-rotating at omega = 3*G/(2*pi*a^2).  This script evaluates every
Section-8 statement in double precision:

  [1] rot_anchor        : the anchor is a fixed point of the rotating-frame
                          field (all six components vanish);
  [2] linX1..linY3      : the 2*pi/Gamma-scaled Jacobian rows (Lean defs)
                          agree with a central-difference Jacobian of the
                          TRUE rotating-frame field at the anchor;
  [3] eig_trans1/2      : M0 vT1 = -3 vT2, M0 vT2 = +3 vT1  (eigenvalues +-3i);
  [4] eig_rot           : M0 vR = 0 (the phase mode, eigenvalue 0);
  [5] eig_dil           : M0 vD = -6 vR (the generalized zero);
  [6] eig_shapeU/W      : M0 u = -3 w, M0 w = +3 u (the shape oscillation);
  [7] char. polynomial  : det(lambda I - M0) = lambda^2 (lambda^2 + 9)^2
                          (Thomson, N = 3);
  [8] lin_cert_transX/Y : d/dt of the TRUE field along the translation lines
                          = (g/2pi) * M0 v (central differences, all 6 comps);
  [9] lin_cert_shapeU/W : the same along the shape lines (quotients vary);
  [10] lin_sol_trans    : x(t) = (b1 cos wt + b2 sin wt, b2 cos wt - b1 sin wt)
                          solves the linearized equation on a t-grid;
  [11] lin_sol_shape    : u(t) = (p cos wt + q sin wt, q cos wt - p sin wt)
                          solves it too;
  [12] lin_sol_size     : the size drift Q(t) = q - 2 w p t solves it;
  [13] lin_bound_trans  : |(x1(t), x2(t))|^2 = b1^2 + b2^2 (exact on a grid);
  [14] lin_bound_shape  : |(u(t), w(t))|^2 = p^2 + q^2 (exact on a grid);
  [15] lin_bound_size   : sqrt(p^2 + Q(t)^2) <= sqrt(p^2 + q^2) + 2|w p t|;
  [16] lin_size_basis   : the size-plane frame (vD, vR) is orthonormal.
"""
import math
import numpy as np

G = 1.0
r3 = math.sqrt(3.0)
omega = 3.0 * G / (2.0 * math.pi)          # lagrangeOmega g 1  (a = 1)
k = G / (2.0 * math.pi)                    # the 1/(2*pi) physical scale

# the equilateral anchor (eqX1..eqY3)
eq = np.array([1.0 / r3, 0.0, -1.0 / (2.0 * r3), 0.5, -1.0 / (2.0 * r3), -0.5])

def field(w):
    """The TRUE rotating-frame field F(w) = V(w) - omega*Jw (six comps)."""
    x1, y1, x2, y2, x3, y3 = w
    D12 = (x1 - x2) ** 2 + (y1 - y2) ** 2
    D13 = (x1 - x3) ** 2 + (y1 - y3) ** 2
    D23 = (x2 - x3) ** 2 + (y2 - y3) ** 2
    kx1 = -k * G * ((y1 - y2) / D12 + (y1 - y3) / D13)
    ky1 = +k * G * ((x1 - x2) / D12 + (x1 - x3) / D13)
    kx2 = -k * G * ((y2 - y1) / D12 + (y2 - y3) / D23)
    ky2 = +k * G * ((x2 - x1) / D12 + (x2 - x3) / D23)
    kx3 = -k * G * ((y3 - y1) / D13 + (y3 - y2) / D23)
    ky3 = +k * G * ((x3 - x1) / D13 + (x3 - x2) / D23)
    return np.array([kx1 + omega * y1, ky1 - omega * x1,
                     kx2 + omega * y2, ky2 - omega * x2,
                     kx3 + omega * y3, ky3 - omega * x3])

# the six linearization rows, exactly as in Trivortex.lean (2*pi/Gamma units)
def linX1(a): d1, e1, d2, e2, d3, e3 = a; return 2*e1 + r3/2*d2 + e2/2 - r3/2*d3 + e3/2
def linY1(a): d1, e1, d2, e2, d3, e3 = a; return -4*d1 + d2/2 - r3/2*e2 + d3/2 + r3/2*e3
def linX2(a): d1, e1, d2, e2, d3, e3 = a; return r3/2*d1 + e1/2 - r3/2*d2 + 7*e2/2 - e3
def linY2(a): d1, e1, d2, e2, d3, e3 = a; return d1/2 - r3/2*e1 - 5*d2/2 + r3/2*e2 - d3
def linX3(a): d1, e1, d2, e2, d3, e3 = a; return -r3/2*d1 + e1/2 - e2 + r3/2*d3 + 7*e3/2
def linY3(a): d1, e1, d2, e2, d3, e3 = a; return d1/2 + r3/2*e1 - d2 - 5*d3/2 - r3/2*e3
ROWS = [linX1, linY1, linX2, linY2, linX3, linY3]

def M0(v):
    return np.array([row(v) for row in ROWS])

def fd_jacobian(w, h=1e-6):
    J = np.zeros((6, 6))
    for j in range(6):
        wp, wm = w.copy(), w.copy()
        wp[j] += h; wm[j] -= h
        J[:, j] = (field(wp) - field(wm)) / (2 * h)
    return J

ok = lambda e, band: "PASS" if e < band else "FAIL"

print(f"G = {G}, omega = {omega:.15f} (3G/2pi = {3*G/(2*math.pi):.15f})")

# [1] rot_anchor -------------------------------------------------------------
F0 = field(eq)
e1 = float(np.max(np.abs(F0)))
print(f"\n[1] rot_anchor: max|F(anchor)| = {e1:.3e}            {ok(e1, 1e-12)}")

# [2] the Lean rows vs the true Jacobian (2*pi/Gamma = 1/(k*G) scaling) ------
J = fd_jacobian(eq)
M0_true = (1.0 / (k * G)) * J          # (2*pi/Gamma) * dF/dw, Gamma = G
e2 = float(np.max(np.abs(M0_true - M0(np.zeros(6) + np.eye(6)[:, 0] * 0))))
# compare row-by-row on the six unit directions
e2 = max(float(np.max(np.abs(M0_true[:, j] - M0(np.eye(6)[j])))) for j in range(6))
print(f"[2] rows vs true Jacobian: max abs diff = {e2:.3e}  {ok(e2, 1e-5)}")

# [3] eig_trans1/2 -----------------------------------------------------------
vT1 = np.array([1, 0, 1, 0, 1, 0], dtype=float)
vT2 = np.array([0, 1, 0, 1, 0, 1], dtype=float)
e3 = max(float(np.max(np.abs(M0(vT1) - (-3) * vT2))),
         float(np.max(np.abs(M0(vT2) - (+3) * vT1))))
print(f"[3] eig_trans: max|M0 vT - image| = {e3:.3e}         {ok(e3, 1e-12)}")

# [4] eig_rot ----------------------------------------------------------------
vR = np.array([0.0, 1 / r3, -0.5, -1 / (2 * r3), 0.5, -1 / (2 * r3)])
e4 = float(np.max(np.abs(M0(vR))))
print(f"[4] eig_rot:   max|M0 vR| = {e4:.3e}                 {ok(e4, 1e-12)}")

# [5] eig_dil ----------------------------------------------------------------
vD = np.array([1 / r3, 0.0, -1 / (2 * r3), 0.5, -1 / (2 * r3), -0.5])
e5 = float(np.max(np.abs(M0(vD) - (-6) * vR)))
print(f"[5] eig_dil:   max|M0 vD + 6 vR| = {e5:.3e}          {ok(e5, 1e-12)}")

# [6] eig_shapeU/W -----------------------------------------------------------
def shapeU(u, w): return np.array([u, w, u/2 + r3/2*w, -r3/2*u + w/2, 0.0, 0.0])
u_, w_ = M0(shapeU(1.0, 0.0)), M0(shapeU(0.0, 1.0))
e6 = max(float(np.max(np.abs(u_ - (-3) * shapeU(0.0, 1.0)))),
         float(np.max(np.abs(w_ - (+3) * shapeU(1.0, 0.0)))))
print(f"[6] eig_shape: max|M0 u + 3 w, M0 w - 3 u| = {e6:.3e}  {ok(e6, 1e-12)}")

# [7] characteristic polynomial ----------------------------------------------
Mmat = np.array([[row(np.eye(6)[j]) for j in range(6)] for row in ROWS])
lam = np.linalg.eigvals(Mmat)
lam_s = sorted(lam, key=lambda z: (round(z.real, 6), round(z.imag, 6)))
expect = np.array([0, 0, 3j, -3j, 3j, -3j], dtype=complex)
exp_s = sorted(expect, key=lambda z: (round(z.real, 6), round(z.imag, 6)))
e7 = max(abs(a - b) for a, b in zip(lam_s, exp_s))
poly = np.poly(Mmat)                    # monic coefficients, high -> low
target = np.array([1, 0, 18, 0, 81, 0, 0], dtype=float)   # x^2 (x^2+9)^2
e7b = float(np.max(np.abs(poly - target)))
print(f"[7] spectrum = {{0,0,+-3i,+-3i}}: max err = {e7:.3e}  {ok(e7, 1e-6)}")
print(f"    det(xI - M0) coeffs vs x^2(x^2+9)^2: max err = {e7b:.3e} {ok(e7b, 1e-8)}")

# [8][9] lin_cert_* : time-derivatives of the TRUE field along mode lines ----
def cert(line, tag):
    errs = []
    for j in range(6):
        h = 1e-6
        wp, wm = eq.copy(), eq.copy()
        wp += h * line; wm -= h * line
        d = (field(wp) - field(wm)) / (2 * h)
        errs.append(abs(d[j] - (k * G) * M0(line)[j]))
    e = max(errs)
    print(f"[{tag}] d/dt true field vs (g/2pi) M0 v: max err = {e:.3e}  {ok(e, 1e-5)}")
    return e

cert(vT1, "8a lin_cert_transX")
cert(vT2, "8b lin_cert_transY")
cert(shapeU(1.0, 0.0), "9a lin_cert_shapeU")
cert(shapeU(0.0, 1.0), "9b lin_cert_shapeW")

# [10][11][12] the modal solutions satisfy x'(t) = (g/2pi) M0 x(t) -----------
def amp_trans(b1, b2, t):
    c, s = math.cos(omega * t), math.sin(omega * t)
    return b1 * c + b2 * s, b2 * c - b1 * s
def amp_shape(p, q, t):
    c, s = math.cos(omega * t), math.sin(omega * t)
    return p * c + q * s, q * c - p * s

def resid_trans(b1, b2, ts):
    m = 0.0
    for t in ts:
        u, w = amp_trans(b1, b2, t)
        du = omega * (-b1 * math.sin(omega * t) + b2 * math.cos(omega * t))
        dw = omega * (-b2 * math.sin(omega * t) - b1 * math.cos(omega * t))
        lin = M0(np.array([u, w, u, w, u, w], dtype=float))
        m = max(m, abs(du - k * G * lin[0]), abs(dw - k * G * lin[1]))
    return m
def resid_shape(p, q, ts):
    m = 0.0
    for t in ts:
        u, w = amp_shape(p, q, t)
        du = omega * (-p * math.sin(omega * t) + q * math.cos(omega * t))
        dw = omega * (-q * math.sin(omega * t) - p * math.cos(omega * t))
        lin = M0(shapeU(u, w))
        m = max(m, abs(du - k * G * lin[0]), abs(dw - k * G * lin[1]))
    return m
def resid_size(p, q, ts):
    m = 0.0
    for t in ts:
        Q = q - 2 * omega * p * t
        dQ = -2 * omega * p
        v = np.array([p / r3, Q / r3, -p / (2 * r3) - Q / 2,
                      p / 2 - Q / (2 * r3), -p / (2 * r3) + Q / 2,
                      -p / 2 - Q / (2 * r3)])
        lin = M0(v)
        # d/dt of all six comps vs (g/2pi) M0 v
        dv = np.array([0.0, dQ / r3, -dQ / 2, -dQ / (2 * r3), dQ / 2, -dQ / (2 * r3)])
        for j in range(6):
            m = max(m, abs(dv[j] - k * G * lin[j]))
    return m

ts = np.linspace(0.0, 2.0, 41)
e10 = resid_trans(0.7, -1.3, ts)
e11 = resid_shape(1.1, 0.6, ts)
e12 = resid_size(0.8, -0.9, ts)
print(f"[10] lin_sol_trans ODE residual  = {e10:.3e}            {ok(e10, 1e-10)}")
print(f"[11] lin_sol_shape ODE residual  = {e11:.3e}            {ok(e11, 1e-10)}")
print(f"[12] lin_sol_size  ODE residual  = {e12:.3e}            {ok(e12, 1e-10)}")

# [13][14] norm preservation -------------------------------------------------
def norm_trans(b1, b2, ts):
    return max(abs((amp_trans(b1, b2, t)[0]**2 + amp_trans(b1, b2, t)[1]**2)
                   - (b1**2 + b2**2)) for t in ts)
def norm_shape(p, q, ts):
    return max(abs((amp_shape(p, q, t)[0]**2 + amp_shape(p, q, t)[1]**2)
                   - (p**2 + q**2)) for t in ts)
e13 = norm_trans(0.7, -1.3, np.linspace(0, 10, 201))
e14 = norm_shape(1.1, 0.6, np.linspace(0, 10, 201))
print(f"[13] lin_bound_trans  |norm^2 - b^2| = {e13:.3e}        {ok(e13, 1e-10)}")
print(f"[14] lin_bound_shape  |norm^2 - p^2| = {e14:.3e}        {ok(e14, 1e-10)}")

# [15] the size-drift bound --------------------------------------------------
def bound_size(p, q, ts):
    """margin = RHS - LHS of the Lean bound; the bound holds iff >= 0."""
    return min(math.sqrt(p*p + q*q) + 2*abs(omega*p*t)
               - math.sqrt(p*p + (q - 2*omega*p*t)**2) for t in ts)
e15 = bound_size(0.8, -0.9, np.linspace(-5, 5, 201))
print(f"[15] lin_bound_size margin (>=0)     = {e15:.3e}         "
      f"{'PASS' if e15 > -1e-12 else 'FAIL'}")

# [16] orthonormal size basis -------------------------------------------------
vD6 = vD
vR6 = vR
nd, nr = float(np.dot(vD6, vD6)), float(np.dot(vR6, vR6))
dr = float(np.dot(vD6, vR6))
e16 = max(abs(nd - 1), abs(nr - 1), abs(dr))
print(f"[16] lin_size_basis |vD|^2,|vR|^2, vD.vR deviations = {e16:.3e} {ok(e16, 1e-12)}")

print("\nall Section-8 numeric mirrors done.")
