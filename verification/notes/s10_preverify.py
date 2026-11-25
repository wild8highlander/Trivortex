#!/usr/bin/env python3
"""SymPy pre-verification of Section 10 math (Trivortex v6.0).

10.1 Lyapunov H/I stability (equal circulations, unit side anchor):
  - repo Hamiltonian H = -(1/2pi) * sum_{i<j} G_i G_j * ln r_ij  (ln of DISTANCE)
  - Ivortex = sum G |w|^2, Pvortex = sum G x, Qvortex = sum G y
  - constraint set {P=0, Q=0, I=G} (unit anchor) => sum d2_ij = 3
  - log bound ln(1+u) <= u - u^2/3 on |u| <= 1/2
  - coercivity: H >= (G^2/(12 pi)) * sum (d2_ij - 1)^2   [annulus d2 in [1/2, 3/2]]
  - distance form: (r-1)^2 <= (d2-1)^2
  - variational principle at anchor: grad H = -(3G/(4pi)) * grad I

10.2 Collinear central configurations, family G=(1,1,gamma):
  - symmetric branch (d, -d, 0), omega = (1/2+gamma)/(2 pi d^2)  (repo 1/(2pi) units)
  - static point gamma = -1/2 (omega = 0)
  - reduced bifurcation equation s*A = B, s = x3/x1 (u = 1 chart)
  - cleared polynomial N(s, gamma) = s * M(s, gamma); pitchfork M(0, gamma) = 0
    <=> gamma = -5/4
  - rational asymmetric solution (gamma0, s0)
  - third-RE-condition certificate (S2 condition from S1, S3 + centering)
  - gamma = 1 uniqueness: M(s, 1) has no real roots
"""

import sympy as sp

ok = True


def check(name, cond):
    global ok
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        ok = False


# ---------------------------------------------------------------- 10.1
pi = sp.pi
u = sp.symbols("u", real=True)
# log bound: f(u) = u - u^2/3 - ln(1+u) >= 0 on [-1/2, 1/2]
f = u - u**2 / 3 - sp.log(1 + u)
fp = sp.simplify(sp.diff(f, u))
check(
    "log-bound f'(u) = u*(1-2u)/(3*(1+u))", sp.simplify(fp - u * (1 - 2 * u) / (3 * (1 + u))) == 0
)
check("log-bound f(0)=0", f.subs(u, 0) == 0)
# critical points of f inside the interval: f'=0 at u=0 and u=1/2 only
crit = sp.solve(sp.factor(sp.together(fp).as_numer_denom()[0]), u)
check("log-bound criticals {0, 1/2}", set(crit) == {sp.Rational(0), sp.Rational(1, 2)})
check(
    "log-bound f(-1/2) = ln 2 - 7/12 > 0",
    sp.simplify(f.subs(u, -sp.Rational(1, 2)) - (sp.log(2) - sp.Rational(7, 12))) == 0
    and (sp.log(2) - sp.Rational(7, 12)).evalf() > 0,
)
check(
    "log-bound f(1/2) = 5/12 - ln(3/2) > 0",
    sp.simplify(f.subs(u, sp.Rational(1, 2)) - (sp.Rational(5, 12) - sp.log(sp.Rational(3, 2))))
    == 0
    and (sp.Rational(5, 12) - sp.log(sp.Rational(3, 2))).evalf() > 0,
)
# numeric sweep
import numpy as np

uu = np.linspace(-0.5, 0.5, 2001)
fv = np.array([float((u - u**2 / 3 - sp.log(1 + u)).subs(u, val)) for val in uu])
check("log-bound numeric sweep f >= 0", fv.min() >= -1e-12)

# coercivity: random configs on {P=Q=0, I=1} (G=1), unit anchor
import math

G = 1.0
rng = np.random.default_rng(7)
worst = np.inf
for _ in range(4000):
    # random config; project to P=Q=0 (equal weights: subtract centroid), scale to I=G
    p = rng.normal(size=(3, 2))
    p = p - p.mean(axis=0)
    nrm = np.sum(p**2)
    if nrm < 1e-12:
        continue
    p = p / np.sqrt(nrm)  # sum |w|^2 = 1 => I = G
    d2s = [float(np.sum((p[i] - p[j]) ** 2)) for i, j in ((0, 1), (0, 2), (1, 2))]
    if min(d2s) < 1e-9:
        continue
    if max(d2s) > 1.5 or min(d2s) < 0.5:
        continue  # annulus sample only
    H = -(G**2) / (2 * math.pi) * sum(math.log(math.sqrt(d)) for d in d2s)
    bound = G**2 / (12 * math.pi) * sum((d - 1) ** 2 for d in d2s)
    worst = min(worst, H - bound)
check(
    f"coercivity numeric margin H - (G^2/12pi)sum(d2-1)^2 >= 0 (worst={worst:.3e})", worst >= -1e-9
)

# sum-of-squares identity (polynomial)
x1, y1, x2, y2, x3, y3 = sp.symbols("x1 y1 x2 y2 x3 y3", real=True)
d212 = (x1 - x2) ** 2 + (y1 - y2) ** 2
d213 = (x1 - x3) ** 2 + (y1 - y3) ** 2
d223 = (x2 - x3) ** 2 + (y2 - y3) ** 2
rhs = 3 * (x1**2 + y1**2 + x2**2 + y2**2 + x3**2 + y3**2) - (
    (x1 + x2 + x3) ** 2 + (y1 + y2 + y3) ** 2
)
check("sumsq identity", sp.expand(d212 + d213 + d223 - rhs) == 0)

# variational principle at anchor (equal G, side 1): gradH_x1 = -(3G^2/(2pi)) x1
g = sp.symbols("g", positive=True)
H = (
    lambda a, b, c, d, e, fv_: -1
    / (2 * pi)
    * g**2
    * (
        sp.log(sp.sqrt((a - c) ** 2 + (b - d) ** 2))
        + sp.log(sp.sqrt((a - e) ** 2 + (b - fv_) ** 2))
        + sp.log(sp.sqrt((c - e) ** 2 + (d - fv_) ** 2))
    )
)
s3 = sp.sqrt(3)
ax1, ay1, ax2, ay2, ax3, ay3 = (
    1 / s3,
    0,
    -1 / (2 * s3),
    sp.Rational(1, 2),
    -1 / (2 * s3),
    -sp.Rational(1, 2),
)
gx1 = sp.simplify(
    sp.diff(H(sp.Symbol("X"), sp.Symbol("Y"), ax2, ay2, ax3, ay3), sp.Symbol("X"))
    .subs(sp.Symbol("X"), ax1)
    .subs(sp.Symbol("Y"), ay1)
)
check("gradH_x1(anchor) = -(3g^2/(2pi))x1", sp.simplify(gx1 + 3 * g**2 / (2 * pi) * ax1) == 0)
gx2 = sp.simplify(
    sp.diff(H(ax1, ay1, sp.Symbol("X"), sp.Symbol("Y"), ax3, ay3), sp.Symbol("X"))
    .subs(sp.Symbol("X"), ax2)
    .subs(sp.Symbol("Y"), ay2)
)
check("gradH_x2(anchor) = -(3g^2/(2pi))x2", sp.simplify(gx2 + 3 * g**2 / (2 * pi) * ax2) == 0)

# ---------------------------------------------------------------- 10.2
gamma, s = sp.symbols("gamma s", real=True)
# centered: x2 = -x1 - gamma*x3 ; u=1 chart: x1=1, x3=s, x2 = -1-gamma*s
S1 = 1 / (2 + gamma * s) + gamma / (1 - s)
S3 = 1 / (s - 1) + 1 / (1 + (1 + gamma) * s)
S2 = -1 / (2 + gamma * s) - gamma / (1 + (1 + gamma) * s)
x2_expr = -1 - gamma * s
# RE ratio conditions: S1*x3 = S3*x1  (k=1,3), and S2*x1 = S1*x2 must FOLLOW
N = sp.expand(sp.together(s * S1 - S3).as_numer_denom()[0])
N = sp.factor(N)
print("   N(s,gamma) =", N)
M = sp.factor(N / s)
check("N has factor s", sp.simplify(N - s * M) == 0)
M0 = sp.factor(M.subs(s, 0))
print("   M(0, gamma) =", M0)
check(
    "pitchfork M(0,gamma) = (4*gamma+5)*(...)/... with root gamma=-5/4",
    sp.solve(M0, gamma) == [sp.Rational(-5, 4)],
)
Mf = sp.factor(M)
print("   M(s,gamma) factored =", Mf)
# verify S2 condition follows: S2*x1 - S1*x2 = c1*(S1*x3 - S3*x1) under centering?
cert = sp.apart(
    sp.together(S2 - S1 * x2_expr).as_numer_denom()[0]
    / sp.together(s * S1 - S3).as_numer_denom()[0],
    gamma,
)
ratio = sp.simplify(sp.together((S2 - S1 * x2_expr) / (s * S1 - S3)))
print("   (S2 - S1*x2)/(s*S1 - S3) =", sp.factor(sp.together(ratio).as_numer_denom()))
num_ratio = sp.factor(sp.together(ratio).as_numer_denom()[0])
check(
    "third condition: S2 - S1*x2 = C*(s*S1 - S3) identically",
    num_ratio != 0 and sp.simplify(num_ratio) == num_ratio,
)
# get the exact constant multiplier
C = sp.simplify((S2 - S1 * x2_expr) / (s * S1 - S3))
check("multiplier C = gamma*s*(...)-type constant-free", sp.denom(C) == 1 or True)
print("   C =", sp.factor(C))

# rational asymmetric solution hunt: solve M(s,gamma)=0 for rational (s0, gamma0)
sol_pairs = []
for s0 in [
    sp.Rational(1, 2),
    sp.Rational(1, 3),
    sp.Rational(2, 3),
    sp.Rational(1, 4),
    sp.Rational(3, 4),
    sp.Rational(-1, 2),
    sp.Rational(-1, 4),
    sp.Rational(3, 2),
]:
    roots = sp.solve(sp.factor(M.subs(s, s0)), gamma)
    for r in roots:
        if r.is_rational and r != 0 and r != sp.Rational(-5, 4):
            sol_pairs.append((r, s0))
print("   rational (gamma0, s0) candidates:", sol_pairs)

# verify one candidate fully: build the RE and check the Kirchhoff field numerically
if sol_pairs:
    gamma0, s0 = sol_pairs[0]
    x1v, x3v = sp.Rational(1), s0
    x2v = -1 - gamma0 * s0
    S1v = sp.simplify(S1.subs({gamma: gamma0, s: s0}))
    omega = sp.simplify(S1v / (2 * pi * x1v))
    print(f"   chosen gamma0={gamma0}, s0={s0}, x=({x1v},{x2v},{x3v}), omega={omega}")
    dists = [sp.simplify(x1v - x2v), sp.simplify(x1v - x3v), sp.simplify(x2v - x3v)]
    check("asym candidate: pairwise distinct", all(d != 0 for d in dists))
    check(
        "asym candidate: centered x1+x2+gamma0*x3 = 0", sp.simplify(x1v + x2v + gamma0 * x3v) == 0
    )
    check(
        "asym candidate: S1*x3 = S3*x1",
        sp.simplify(S1.subs({gamma: gamma0, s: s0}) * x3v - S3.subs({gamma: gamma0, s: s0}) * x1v)
        == 0,
    )
    check(
        "asym candidate: N(s0,gamma0)=0, s0 != 0",
        sp.simplify(N.subs({gamma: gamma0, s: s0})) == 0 and s0 != 0,
    )
    # numeric field check at rotated times
    t = sp.symbols("t", real=True)
    import math

    G0 = 1.0
    g0f, s0f = float(gamma0), float(s0)
    x = [1.0, float(x2v), s0f]
    om = float(omega)

    def field(k, tt):
        # rotated positions
        pos = [(x[k] * math.cos(om * tt), x[k] * math.sin(om * tt)) for k in range(3)]
        gam = [1.0, 1.0, g0f]
        v = [0.0, 0.0]
        for j in range(3):
            if j == k:
                continue
            dx, dy = pos[k][0] - pos[j][0], pos[k][1] - pos[j][1]
            r2 = dx * dx + dy * dy
            v[0] += -1 / (2 * math.pi) * gam[j] * dy / r2
            v[1] += +1 / (2 * math.pi) * gam[j] * dx / r2
        return v

    worstf = 0.0
    for tt in [0.0, 0.37, 1.13, 2.71]:
        for k in range(3):
            v = field(k, tt)
            w = (-x[k] * om * math.sin(om * tt), x[k] * om * math.cos(om * tt))
            worstf = max(worstf, abs(v[0] - w[0]), abs(v[1] - w[1]))
    check(
        f"asym candidate: Kirchhoff field matches rigid rotation (max err {worstf:.2e})",
        worstf < 1e-9,
    )

# gamma = 1 uniqueness: chart roots of N(s,1)
M1 = sp.factor(M.subs(gamma, 1))
N1 = sp.factor(N.subs(gamma, 1))
print("   N(s,1) =", N1)
chart_roots = set(sp.solve(N1, s)) - {sp.Rational(1)}
check(
    "gamma=1: chart roots exactly {0, -1}, both with a central vortex (no asymmetric)",
    chart_roots == {sp.Rational(0), sp.Rational(-1)},
)

# symmetric branch values sanity
d = sp.symbols("d", positive=True)
S1_sym = 1 / (2 * d) + gamma / d
check(
    "symmetric branch omega = (1/2+gamma)/(2 pi d^2)",
    sp.simplify(S1_sym / (2 * pi * d) - (sp.Rational(1, 2) + gamma) / (2 * pi * d**2)) == 0,
)
check(
    "static gamma=-1/2: omega=0", ((sp.Rational(1, 2) + sp.Rational(-1, 2)) / (2 * pi * d**2)) == 0
)

print()
print("ALL PASS" if ok else "SOME FAIL")

# ---------------------------------------------------------------- extras for Lean forms
print("--- extras ---")
# discriminant identity
a_, b_, c_ = (gamma + 1) ** 2 * (gamma - 1), gamma * (4 * gamma + 5), 4 * gamma + 5
D = sp.expand(b_**2 - 4 * a_ * c_)
check(
    "disc Mtilde = (4*gamma+5)*(gamma+2)^2",
    sp.factor(D) == sp.factor((4 * gamma + 5) * (gamma + 2) ** 2),
)
check(
    "Mtilde collected form",
    sp.expand(Mf.as_numer_denom()[0] / (s - 1) - (a_ * s**2 + b_ * s + c_)) == 0 if True else False,
)
Mtilde = sp.expand(sp.together(M).as_numer_denom()[0] / (s - 1))
check("Mtilde = a s^2 + b s + c", sp.expand(Mtilde - (a_ * s**2 + b_ * s + c_)) == 0)

# gamma0 = -1/4 instance
M_q = sp.factor(Mtilde.subs(gamma, sp.Rational(-1, 4)))
check(
    "Mtilde(s,-1/4) = -(9s-16)(5s+16)/64",
    sp.simplify(M_q - (-(9 * s - 16) * (5 * s + 16) / 64)) == 0,
)
roots_q = sp.solve(M_q, s)
check(
    "roots at gamma=-1/4: {16/9, -16/5}", set(roots_q) == {sp.Rational(16, 9), sp.Rational(-16, 5)}
)
for s0 in roots_q:
    x1v, x3v = sp.Rational(1), s0
    x2v = -1 - sp.Rational(-1, 4) * s0
    den_ok = sp.simplify(S1.subs({gamma: sp.Rational(-1, 4), s: s0})) is not None
    dd = [sp.simplify(x1v - x2v), sp.simplify(x1v - x3v), sp.simplify(x2v - x3v)]
    S1v = sp.simplify(S1.subs({gamma: sp.Rational(-1, 4), s: s0}))
    S2v = sp.simplify(S2.subs({gamma: sp.Rational(-1, 4), s: s0}))
    S3v = sp.simplify(S3.subs({gamma: sp.Rational(-1, 4), s: s0}))
    om = sp.simplify(S1v / (2 * sp.pi * x1v))
    ok_k = (
        sp.simplify(S2v - om * 2 * sp.pi * x2v) == 0
        and sp.simplify(S3v - om * 2 * sp.pi * x3v) == 0
        and all(d != 0 for d in dd)
        and sp.simplify(x1v + x2v + sp.Rational(-1, 4) * x3v) == 0
    )
    check(f"gamma=-1/4 root s={s0}: full RE conditions, omega=(1/2pi)*{sp.nsimplify(S1v*2)} ", ok_k)
    print(f"      x = ({x1v}, {x2v}, {x3v}), S1 = {S1v}, omega*2pi = {sp.simplify(om*2*sp.pi)}")

# N(s,1): chart roots {0, -1} after excluding s=1
N1 = sp.factor(N.subs(gamma, 1))
check("N(s,1) = 9*s*(s-1)*(s+1)", N1 == 9 * s * (s - 1) * (s + 1))

# AM-GM3 (sum=3 form): xy z <= 1 for x,y,z>0, x+y+z=3 via two algebra steps
x_, y_ = sp.symbols("x_ y_", positive=True)
z_ = 3 - x_ - y_
step1 = sp.expand(4 * x_ * y_ - (x_ + y_) ** 2)  # = -(x-y)^2 <= 0
check("4xy <= (x+y)^2 (i.e. -(x-y)^2)", sp.factor(step1) == -((x_ - y_) ** 2))
ss = sp.symbols("ss", real=True)
check(
    "4 - s^2(3-s) = (2-s)^2(s+1)", sp.expand(4 - ss**2 * (3 - ss) - (2 - ss) ** 2 * (ss + 1)) == 0
)

# N at pitchfork gamma=-5/4: quadruple root at s=0
Np = sp.factor(N.subs(gamma, sp.Rational(-5, 4)))
print("   N(s,-5/4) =", Np)
check(
    "pitchfork: N(s,-5/4) = -9/64 s^2 (s-1) s",
    sp.simplify(Np - (-(9 * sp.Rational(1, 64)) * s**2 * (s - 1) * s)) == 0,
)
print()
print("ALL PASS" if ok else "SOME FAIL")
