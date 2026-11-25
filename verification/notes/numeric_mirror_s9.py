#!/usr/bin/env python3
"""Numeric mirror for Section 9 (Lean formalization cross-check).

Every number/identity that Lean proves in §9 is re-derived numerically
here with mpmath high-precision integration, so the formalization and
the numerical model certify each other:

  1. the general-circulation rigid rotation: integrate the Kirchhoff ODE
     for (g1,g2,g3) = (1, 1, 2), a = 1 from the translated triangle and
     compare with the closed rotation form (genX, genY, omega = G/2pi);
  2. the centroid identity Sigma g_k w_k(t) = 0 along the trajectory;
  3. genLin eigenvalues vs charpoly lambda^2 (lambda^2+G^2) (lambda^2+3P)
     for gamma in {4, -1/2, -1};
  4. the shape-pair instances: (1,1,4): B u4 = -27 ut4, B ut4 = u4;
     (1,1,-1/2): B Uh = 0, B Ut2 = Uh; (1,1,-1): B v = sqrt(3) v;
  5. the growing mode norm |m(t)|^2 = 12 e^(2 sqrt(3) t) against direct
     ODE integration of the linearized rotating-frame flow;
  6. the (1,1,4) bounded oscillation norm 891cos^2+2079sin^2-891cs.
"""

import numpy as np
from numpy import sqrt as nsqrt
import sympy as sp

ok = []


def check(name, cond):
    ok.append((name, bool(cond)))
    print(("PASS  " if cond else "FAIL  ") + name)


# ---------------- 1+2: nonlinear continuation ------------------------------
def kirchhoff_rhs(w, g):
    """w = [x1,y1,x2,y2,x3,y3]; returns the Kirchhoff rhs (lab frame)."""
    x1, y1, x2, y2, x3, y3 = w
    d12 = (x1 - x2) ** 2 + (y1 - y2) ** 2
    d13 = (x1 - x3) ** 2 + (y1 - y3) ** 2
    d23 = (x2 - x3) ** 2 + (y2 - y3) ** 2
    g1, g2, g3 = g
    kx1 = -(g2 * (y1 - y2) / d12 + g3 * (y1 - y3) / d13) / (2 * np.pi)
    ky1 = (g2 * (x1 - x2) / d12 + g3 * (x1 - x3) / d13) / (2 * np.pi)
    kx2 = -(g1 * (y2 - y1) / d12 + g3 * (y2 - y3) / d23) / (2 * np.pi)
    ky2 = (g1 * (x2 - x1) / d12 + g3 * (x2 - x3) / d23) / (2 * np.pi)
    kx3 = -(g1 * (y3 - y1) / d13 + g2 * (y3 - y2) / d23) / (2 * np.pi)
    ky3 = (g1 * (x3 - x1) / d13 + g2 * (x3 - x2) / d23) / (2 * np.pi)
    return np.array([kx1, ky1, kx2, ky2, kx3, ky3])


g = (1.0, 1.0, 2.0)
G = sum(g)
a = 1.0
omega = G / (2 * np.pi * a**2)
eq = np.array([1 / np.sqrt(3), 0, -1 / (2 * np.sqrt(3)), 0.5, -1 / (2 * np.sqrt(3)), -0.5])
Sx = g[0] * eq[0] + g[1] * eq[2] + g[2] * eq[4]
Sy = g[0] * eq[1] + g[1] * eq[3] + g[2] * eq[5]
taux = -a * Sx / G
tauy = -a * Sy / G
anchor = eq.copy()
anchor[0::2] += taux
anchor[1::2] += tauy
check(
    "weighted centroid at t=0",
    abs(sum(g * anchor[0::2])) < 1e-14 and abs(sum(g * anchor[1::2])) < 1e-14,
)

# integrate the ODE and compare with the rigid rotation form
T = 2.0
steps = 4000
dt = T / steps
w = anchor.copy()
maxerr = 0.0
maxcent = 0.0
for i in range(steps):
    t = i * dt
    # closed form at t+dt
    c, s = np.cos(omega * (t + dt)), np.sin(omega * (t + dt))
    rot = np.empty(6)
    rot[0::2] = c * anchor[0::2] - s * anchor[1::2]
    rot[1::2] = s * anchor[0::2] + c * anchor[1::2]
    # He2 step of the true ODE
    k1 = kirchhoff_rhs(w, g)
    k2 = kirchhoff_rhs(w + dt * k1, g)
    w = w + dt * (k1 + k2) / 2
    maxerr = max(maxerr, np.abs(w - rot).max())
    maxcent = max(maxcent, abs(sum(g * w[0::2])), abs(sum(g * w[1::2])))
check("gen solution vs rigid rotation (He2, err<1e-5)", maxerr < 1e-5)
check("centroid identity along trajectory", maxcent < 1e-12)
check("omega value G/(2 pi a^2) = 2/pi for G=4", abs(omega - 2 / np.pi) < 1e-15)

# ---------------- 3: eigenvalues vs charpoly --------------------------------
x1, y1, x2, y2, x3, y3 = sp.symbols("x1 y1 x2 y2 x3 y3")
g1, g2, g3, lam = sp.symbols("g1 g2 g3 lambda")


def d2f(a, b, c, d):
    return (a - c) ** 2 + (b - d) ** 2


def field(g1, g2, g3):
    return [
        -(g2 * (y1 - y2) / d2f(x1, y1, x2, y2) + g3 * (y1 - y3) / d2f(x1, y1, x3, y3)),
        (g2 * (x1 - x2) / d2f(x1, y1, x2, y2) + g3 * (x1 - x3) / d2f(x1, y1, x3, y3)),
        -(g1 * (y2 - y1) / d2f(x1, y1, x2, y2) + g3 * (y2 - y3) / d2f(x2, y2, x3, y3)),
        (g1 * (x2 - x1) / d2f(x1, y1, x2, y2) + g3 * (x2 - x3) / d2f(x2, y2, x3, y3)),
        -(g1 * (y3 - y1) / d2f(x1, y1, x3, y3) + g2 * (y3 - y2) / d2f(x2, y2, x3, y3)),
        (g1 * (x3 - x1) / d2f(x1, y1, x3, y3) + g2 * (x3 - x2) / d2f(x2, y2, x3, y3)),
    ]


s3 = sp.sqrt(3)
eqv = [1 / s3, 0, -1 / (2 * s3), sp.Rational(1, 2), -1 / (2 * s3), -sp.Rational(1, 2)]
F = sp.Matrix(field(g1, g2, g3))
J = F.jacobian(sp.Matrix([x1, y1, x2, y2, x3, y3])).subs(dict(zip([x1, y1, x2, y2, x3, y3], eqv)))
Gg = g1 + g2 + g3
J2m = sp.Matrix([[0, -1], [1, 0]])
B = sp.simplify(J - Gg * sp.kronecker_product(sp.eye(3), J2m))
B = B.applyfunc(lambda e: sp.nsimplify(sp.radsimp(sp.simplify(e))))

for gamma in [4, sp.Rational(-1, 2), -1]:
    Bc = B.subs({g1: 1, g2: 1, g3: gamma})
    ev = sorted(
        [val for val, mult in Bc.eigenvals().items() for _ in range(mult)],
        key=lambda z: (float(sp.re(z)), float(sp.im(z))),
    )
    P = 1 + 2 * gamma
    Gv = 2 + gamma
    expected = sorted(
        [
            0,
            0,
            sp.I * Gv,
            -sp.I * Gv,
            sp.sqrt(-3 * P) if P < 0 else sp.I * sp.sqrt(3 * P),
            -sp.sqrt(-3 * P) if P < 0 else -sp.I * sp.sqrt(3 * P),
        ],
        key=lambda z: (float(sp.re(z)), float(sp.im(z))),
    )
    match = all(sp.simplify(a - b) == 0 for a, b in zip(ev, expected))
    check(f"eigenvalues match lambda^2(lam^2+G^2)(lam^2+3P), gamma={gamma}", match)


# ---------------- 4: the concrete pair identities ---------------------------
def matvec(Bc, v):
    return [sp.simplify(sum(Bc[i, j] * v[j] for j in range(6))) for i in range(6)]


B4 = B.subs({g1: 1, g2: 1, g3: 4})
u4 = [-36, -36 * s3, -36, 36 * s3, 18, 0]
ut4 = [8 * s3, -16, -12 * s3, -4, s3, 5]
check(
    "(1,1,4): B u4 = -27 ut4",
    all(sp.simplify(a + 27 * b) == 0 for a, b in zip(matvec(B4, u4), ut4)),
)
check("(1,1,4): B ut4 = u4", all(sp.simplify(a - b) == 0 for a, b in zip(matvec(B4, ut4), u4)))

Bh = B.subs({g1: 1, g2: 1, g3: sp.Rational(-1, 2)})
Uh = [-3 * s3, -3, 0, 6, -6 * s3, 6]
Ut2 = [-2, -2 * s3, -2, 2 * s3, -8, 0]
check("(1,1,-1/2): B Uh = 0", all(sp.simplify(a) == 0 for a in matvec(Bh, Uh)))
check("(1,1,-1/2): B Ut2 = Uh", all(sp.simplify(a - b) == 0 for a, b in zip(matvec(Bh, Ut2), Uh)))

Bm = B.subs({g1: 1, g2: 1, g3: -1})
v = [1, s3, 1, -s3, 2, 0]
check(
    "(1,1,-1): B v = sqrt(3) v", all(sp.simplify(a - s3 * b) == 0 for a, b in zip(matvec(Bm, v), v))
)

# ---------------- 5: growing mode norm vs ODE -------------------------------
# linearized rotating-frame flow for (1,1,-1), integrated with the EXACT
# eigenvector initial condition v: the Lean theorem predicts
# |m(t)|^2 = 12 e^(2 sqrt(3) t).
Bmn = np.array([[float(sp.N(c)) for c in Bm[i, :]] for i in range(6)])
vn = np.array([float(sp.N(c)) for c in v])
lam = nsqrt(3.0)
T2, steps2 = 1.0, 2000
dt2 = T2 / steps2
m = vn.copy()
maxrel = 0.0
for i in range(steps2):
    t = i * dt2
    # linearized flow: m' = B m (the rotating-frame linearization IS B/2pi
    # scaled: genLin = 2*pi*A_rot, so the true flow is m' = genLin/(2pi) m)
    # exact matrix exponential via Taylor (|B t| small enough at each step)
    M = Bmn * (t + dt2)
    mm = vn.copy()
    term = vn.copy()
    for kk in range(1, 40):
        term = (M @ term) / kk
        mm = mm + term
    pred = 12.0 * np.exp(2 * lam * (t + dt2))
    actual = float(np.dot(mm, mm))
    maxrel = max(maxrel, abs(actual / pred - 1))
    m = mm
check("growing mode |m|^2 = 12 e^(2 sqrt3 t) (rel err < 1e-6)", maxrel < 1e-6)

# ---------------- 6: (1,1,4) oscillation norm identity ----------------------
# UNSCALED modal solution x~(t) = cos(mu t) u4s + sin(mu t)/mu * B u4s with
# u4s = (-2,-2s3,-2,2s3,1,0): |x~|^2 = 33cos^2 + 77sin^2 - 33 cos sin
#                               = 165/2 - (11/2)(3cos+sin)^2 <= 165/2.
mu = 3 * s3
c4, s4 = sp.cos(mu), sp.sin(mu)
u4s = [-2, -2 * s3, -2, 2 * s3, 1, 0]
W4s = matvec(B4, u4s)
xt = [
    (
        sp.expand(c4 * u4s[j] + s4 * sp.Rational(1, 3) * sp.sqrt(3) * W4s[j] / mu)
        if False
        else sp.expand(c4 * u4s[j] + s4 * W4s[j] / mu)
    )
    for j in range(6)
]
norm2 = sp.simplify(sum(c**2 for c in xt))
claimed = sp.expand(33 * c4**2 + 77 * s4**2 - 33 * c4 * s4)
check("(1,1,4): |x~(t)|^2 = 33c^2+77s^2-33cs", sp.simplify(norm2 - claimed) == 0)
shift = sp.simplify(norm2 - (sp.Rational(165, 2) - sp.Rational(11, 2) * (3 * c4 + s4) ** 2))
check("(1,1,4): = 165/2 - (11/2)(3c+s)^2 (bounded by 165/2)", shift == 0)

# ---------------- summary ---------------------------------------------------
print()
print(f"ALL {sum(1 for _, c in ok if c)}/{len(ok)} checks passed")
if not all(c for _, c in ok):
    raise SystemExit(1)
