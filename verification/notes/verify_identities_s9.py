#!/usr/bin/env python3
"""SymPy pre-verification of every identity formalized in Section 9.

Run: python3 verify_identities_s9.py  — prints one PASS/FAIL line per
identity and exits non-zero on any failure.  This is the machine check
that stands behind the Lean chunk: the same polynomial identities are
proved in `verification/lean4/Trivortex.lean` §9 by `ring_nf` +
`simp only [s3sq, s9_s3cu]` + `ring` after the symbolic derivation.
"""
import sympy as sp

g1, g2, g3 = sp.symbols('g1 g2 g3', real=True)
s = sp.Symbol('s')                      # stand-in for sqrt(3)
s3 = sp.sqrt(3)
G = g1 + g2 + g3
P = g1 * g2 + g2 * g3 + g3 * g1
fails = []

def check(name, expr):
    """expr vanishes identically at s = sqrt(3)?"""
    e = sp.simplify(sp.expand(expr).subs(s, s3))
    okflag = e == 0
    print(("PASS  " if okflag else "FAIL  ") + name)
    if not okflag:
        fails.append(name)

# the 2*pi-scaled rotating-frame linearization at the equilateral anchor
x1, y1, x2, y2, x3, y3 = sp.symbols('x1 y1 x2 y2 x3 y3')

def d2f(a, b, c, d):
    return (a - c) ** 2 + (b - d) ** 2

def field(g1, g2, g3):
    return [
        -(g2*(y1-y2)/d2f(x1,y1,x2,y2) + g3*(y1-y3)/d2f(x1,y1,x3,y3)),
        (g2*(x1-x2)/d2f(x1,y1,x2,y2) + g3*(x1-x3)/d2f(x1,y1,x3,y3)),
        -(g1*(y2-y1)/d2f(x1,y1,x2,y2) + g3*(y2-y3)/d2f(x2,y2,x3,y3)),
        (g1*(x2-x1)/d2f(x1,y1,x2,y2) + g3*(x2-x3)/d2f(x2,y2,x3,y3)),
        -(g1*(y3-y1)/d2f(x1,y1,x3,y3) + g2*(y3-y2)/d2f(x2,y2,x3,y3)),
        (g1*(x3-x1)/d2f(x1,y1,x3,y3) + g2*(x3-x2)/d2f(x2,y2,x3,y3)),
    ]

eq = [1/s3, 0, -1/(2*s3), sp.Rational(1, 2), -1/(2*s3), -sp.Rational(1, 2)]
F = sp.Matrix(field(g1, g2, g3))
J = F.jacobian(sp.Matrix([x1, y1, x2, y2, x3, y3])).subs(
    dict(zip([x1, y1, x2, y2, x3, y3], eq)))
J2 = sp.Matrix([[0, -1], [1, 0]])
B = sp.simplify(J - G * sp.kronecker_product(sp.eye(3), J2))
B = B.applyfunc(lambda e: sp.expand(sp.nsimplify(sp.radsimp(sp.simplify(e))).subs(s3, s)))
ROWS = [[sp.expand(B[i, j]) for j in range(6)] for i in range(6)]

def mv(row, v):
    return sp.expand(sum(row[j] * v[j] for j in range(6)))

print("== characteristic polynomial ==")
lam = sp.Symbol('lambda')
gam = sp.Symbol('gamma')
Bfam = sp.Matrix([[sp.expand(ROWS[i][j].subs({g1: 1, g2: 1, g3: gam}))
                   for j in range(6)] for i in range(6)])
cp = sp.factor(Bfam.charpoly(lam).as_expr())
target = sp.expand(lam**2 * (lam**2 + (2 + gam)**2) * (lam**2 + 3 + 6*gam))
check("charpoly(1,1,gamma) = lambda^2 (lambda^2+G^2) (lambda^2+3P)",
      cp - target)

print("== general-circulation identities ==")
c1, c2 = sp.symbols('c1 c2')
vtr = [c1, c2, c1, c2, c1, c2]
for i, tgt in enumerate([G*c2, -G*c1, G*c2, -G*c1, G*c2, -G*c1]):
    check(f"s9_lin_trans row {i+1}", mv(ROWS[i], vtr) - tgt)

KV = [s*(g3-g2), -3*(g2+g3), s*(g1+2*g3), 3*g1, -s*(g1+2*g2), 3*g1]
for i in range(6):
    check(f"s9_lin_kernel row {i+1}", mv(ROWS[i], KV))

ANCH = [s*(g2+g3)/2, (g3-g2)/2, -s*g1/2, (g1+2*g3)/2, -s*g1/2, -(g1+2*g2)/2]
JANCH = [-ANCH[1], ANCH[0], -ANCH[3], ANCH[2], -ANCH[5], ANCH[4]]
for i in range(6):
    check(f"s9_lin_chain row {i+1}", mv(ROWS[i], ANCH) + 2*G*JANCH[i])

U = [-g2*g3, -s*g2*g3, -g1*g3, s*g1*g3, 2*g1*g2, 0]
W = [mv(ROWS[j], U) for j in range(6)]
for i in range(6):
    check(f"s9_shape_gen row {i+1}", mv(ROWS[i], W) + 3*P*U[i])

print("== instance (1,1,4): stable shape oscillation ==")
sub4 = {g1: 1, g2: 1, g3: 4}
B4 = [[sp.expand(ROWS[i][j].subs(sub4)) for j in range(6)] for i in range(6)]
u4 = [-36, -36*s, -36, 36*s, 18, 0]
ut4 = [8*s, -16, -12*s, -4, s, 5]
for i in range(6):
    check(f"s9_shape4_a row {i+1}", mv(B4[i], u4) + 27*ut4[i])
for i in range(6):
    check(f"s9_shape4_b row {i+1}", mv(B4[i], ut4) - u4[i])

print("== instance (1,1,-1/2): the collision ==")
subh = {g1: 1, g2: 1, g3: sp.Rational(-1, 2)}
Bh = [[sp.expand(ROWS[i][j].subs(subh)) for j in range(6)] for i in range(6)]
Uh = [-3*s, -3, 0, 6, -6*s, 6]
Ut2 = [-2, -2*s, -2, 2*s, -8, 0]
for i in range(6):
    check(f"s9_collision_a row {i+1}", mv(Bh[i], Uh))
for i in range(6):
    check(f"s9_collision_b row {i+1}", mv(Bh[i], Ut2) - Uh[i])

print("== instance (1,1,-1): linear instability ==")
subm = {g1: 1, g2: 1, g3: -1}
Bm = [[sp.expand(ROWS[i][j].subs(subm)) for j in range(6)] for i in range(6)]
v = [1, s, 1, -s, 2, 0]
for i in range(6):
    check(f"s9_eig_unst row {i+1}", mv(Bm[i], v) - s*v[i])

print("== (1,1,4) oscillation norm ==")
mu = 3*s3
c4, s4 = sp.cos(mu), sp.sin(mu)
u4s = [-2, -2*s3, -2, 2*s3, 1, 0]
B4r = [[sp.expand(ROWS[i][j].subs(sub4).subs(s, s3)) for j in range(6)]
       for i in range(6)]
W4s = [sp.expand(sum(B4r[i][j]*u4s[j] for j in range(6))) for i in range(6)]
xt = [sp.expand(c4*u4s[j] + s4*W4s[j]/mu) for j in range(6)]
norm2 = sp.simplify(sum(c**2 for c in xt))
check("|x~(t)|^2 = 33c^2+77s^2-33cs",
      norm2 - (33*c4**2 + 77*s4**2 - 33*c4*s4))
check("|x~(t)|^2 = 165/2 - (11/2)(3c+s)^2 <= 165/2",
      norm2 - (sp.Rational(165, 2)
               - sp.Rational(11, 2)*(3*c4+s4)**2))

print()
if fails:
    print(f"{len(fails)} FAILURES:")
    for f in fails:
        print("  -", f)
    raise SystemExit(1)
print("ALL IDENTITIES VERIFIED — the §9 Lean chunk is backed by SymPy.")
