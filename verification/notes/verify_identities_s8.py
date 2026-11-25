#!/usr/bin/env python3
"""Symbolic pre-verification of every identity planned for Trivortex.lean §8
(linear stability: the eigenmodes of perturbations of the equilateral triangle).

Conventions (mirror verify.py / Trivortex.lean):
  Kirchhoff RHS:  dx_i = -1/(2pi) * sum_{j!=i} G_j (y_i - y_j)/D_ij
                 dy_i = +1/(2pi) * sum_{j!=i} G_j (x_i - y_j)/D_ij
  D_ij = (x_i-x_j)^2 + (y_i-y_j)^2
  Anchor (side a=1):  (1/sqrt3, 0), (-1/(2 sqrt3), 1/2), (-1/(2 sqrt3), -1/2)
  lagrangeOmega g 1 = 3 g / (2 pi)

Rotating frame:  w = e^{-i omega t} zeta  =>  wdot = V(w) - omega*J w,
  i.e. per vortex:  rotX_k = kx_k + omega*y_k,   rotY_k = ky_k - omega*x_k.

M0 := (2 pi / g) * Jacobian of the rotating-frame field at the anchor
(entries then lie in Q(sqrt3); the g/(2 pi) factor is the physical scale).

Checks (all must print True / exact):
  A. anchor is an equilibrium of the rotating frame at omega = lagrangeOmega g 1;
  B. M0 matrix entries: exact closed forms;
  C. translation modes:  M0 vT1 = -3 * vT2', M0 vT2 = +3 * vT1'
     (vT1 = (1,0,1,0,1,0), vT2 = (0,1,0,1,0,1)); eigenvalues +-3i;
  D. rotation mode:      M0 vR = 0   (vR = J*anchor per vortex);
  E. dilation mode:     M0 vD = -6 vR (vD = anchor per vortex);  nilpotency M0^2 vD = 0;
  F. shape modes:        eigenvalues +-i*nu0 with nu0 exact; M0 u = -nu0 u', M0 u' = nu0 u;
  G. characteristic polynomial factors  x^2 (x^2+9) (x^2+nu0^2);
  H. directional derivatives of the TRUE rotating-frame field along
     vT1, vT2, vR, vD equal (g/2pi)*M0*v (certification arithmetic);
  I. norm-preservation data for the shape block (u . u' = 0, |u| = |u'|).
"""

import sympy as sp

x1, y1, x2, y2, x3, y3 = sp.symbols("x1 y1 x2 y2 x3 y3", real=True)
g = sp.Symbol("g", positive=True)
pi = sp.pi
r3 = sp.sqrt(3)

D12 = (x1 - x2) ** 2 + (y1 - y2) ** 2
D13 = (x1 - x3) ** 2 + (y1 - y3) ** 2
D23 = (x2 - x3) ** 2 + (y2 - y3) ** 2

# --- Kirchhoff field V (lab frame), equal circulations g ---
kx1 = -(g / (2 * pi)) * ((y1 - y2) / D12 + (y1 - y3) / D13)
ky1 = +(g / (2 * pi)) * ((x1 - x2) / D12 + (x1 - x3) / D13)
kx2 = -(g / (2 * pi)) * ((y2 - y1) / D12 + (y2 - y3) / D23)
ky2 = +(g / (2 * pi)) * ((x2 - x1) / D12 + (x2 - x3) / D23)
kx3 = -(g / (2 * pi)) * ((y3 - y1) / D13 + (y3 - y2) / D23)
ky3 = +(g / (2 * pi)) * ((x3 - x1) / D13 + (x3 - x2) / D23)

omega = 3 * g / (2 * pi)  # lagrangeOmega g 1

# rotating-frame field F = V - omega*J:  rotX_k = kx_k + omega*y_k ; rotY_k = ky_k - omega*x_k
F = sp.Matrix(
    [
        kx1 + omega * y1,
        ky1 - omega * x1,
        kx2 + omega * y2,
        ky2 - omega * x2,
        kx3 + omega * y3,
        ky3 - omega * x3,
    ]
)
vars6 = [x1, y1, x2, y2, x3, y3]

anchor = sp.Matrix([1 / r3, 0, -1 / (2 * r3), sp.Rational(1, 2), -1 / (2 * r3), -sp.Rational(1, 2)])

print("=== A. equilibrium of the rotating frame ===")
Feq = F.subs(dict(zip(vars6, anchor)))
print("F(anchor) =", sp.simplify(Feq.T))
print("A. all zero:", Feq == sp.zeros(6, 1))

print("=== B. the linearization M0 = (2pi/g) * Jacobian(F) at anchor ===")
Jac = F.jacobian(vars6)
Jsub = Jac.subs(dict(zip(vars6, anchor)))
M0 = sp.simplify(sp.nsimplify(2 * pi / g * Jsub, [r3]))
print("M0 =")
sp.pprint(M0)

print("=== C. translation modes ===")
vT1 = sp.Matrix([1, 0, 1, 0, 1, 0])
vT2 = sp.Matrix([0, 1, 0, 1, 0, 1])
print("M0 vT1 =", (M0 * vT1).T, "  == -3 vT2:", sp.simplify(M0 * vT1 + 3 * vT2) == sp.zeros(6, 1))
print("M0 vT2 =", (M0 * vT2).T, "  == +3 vT1:", sp.simplify(M0 * vT2 - 3 * vT1) == sp.zeros(6, 1))

print("=== D. rotation mode vR = J*anchor per vortex ===")
vR = sp.Matrix([-anchor[1], anchor[0], -anchor[3], anchor[2], -anchor[5], anchor[4]])
print("vR =", vR.T)
print("M0 vR == 0:", sp.simplify(M0 * vR) == sp.zeros(6, 1))

print("=== E. dilation mode vD = anchor per vortex ===")
vD = anchor
print("M0 vD + 6 vR == 0:", sp.simplify(M0 * vD + 6 * vR) == sp.zeros(6, 1))
print("nilpotent: M0^2 vD == 0:", sp.simplify(M0 * (M0 * vD)) == sp.zeros(6, 1))

print("=== F/G. spectrum: characteristic polynomial ===")
lam = sp.Symbol("lambda")
charpoly = sp.Poly(sp.factor(M0.charpoly(lam).as_expr()), lam)
print("charpoly(M0) =", charpoly.as_expr())
eigs = M0.eigenvals()
print("eigenvalues:", {sp.simplify(k): v for k, v in eigs.items()})

print("=== F. eigenvector structure (geometric multiplicities) ===")
vec0 = M0.eigenvects()
for val, mult, vs in vec0:
    s = sp.simplify(val)
    print(f"eigenvalue {s}  (alg mult {mult})  geom mult {len(vs)}")
    for v in vs:
        vv = sp.simplify(sp.nsimplify(v, [r3]))
        print("    eigvec:", vv.T)

# the shape pair: eigenvector for +3i NOT in the translation span
# translation eigvec for +3i is vT1 + i vT2; find a second, independent one.
target = None
for val, mult, vs in vec0:
    if sp.simplify(val) == 3 * sp.I and len(vs) == 2:
        cands = [sp.simplify(sp.nsimplify(v, [r3])) for v in vs]
        # pick the one that is not (proportional to) vT1 + I*vT2
        for v in cands:
            comp = sp.Matrix([sp.re(c) for c in v] + [0])  # dummy
            # independence test against vT1, vT2 (real span of the trans eigvec)
            Mtest = sp.Matrix.hstack(
                vT1, vT2, sp.Matrix([sp.re(c) for c in v]), sp.Matrix([sp.im(c) for c in v])
            )
            if sp.simplify(Mtest.rank()) == 4:
                target = v
                break
        if target is not None:
            break

print("=== F. shape eigenvector (second +3i direction, normalised) ===")
assert target is not None, "no second +3i eigenvector: NOT diagonalizable!"
vc = sp.simplify(sp.nsimplify(target, [r3]))
# normalise: divide by the first nonzero entry to keep entries in Q(sqrt3)
first = [c for c in vc if c != 0][0]
vc = sp.simplify(vc / first)
u = sp.Matrix([sp.re(c) for c in vc])
w = sp.Matrix([sp.im(c) for c in vc])
print("u  =", u.T)
print("w  =", w.T)
print("M0 u == -3 w:", sp.simplify(M0 * u + 3 * w) == sp.zeros(6, 1))
print("M0 w == +3 u:", sp.simplify(M0 * w - 3 * u) == sp.zeros(6, 1))
print("u . w =", sp.simplify(u.dot(w)), "  (want 0)")
print("|u|^2 =", sp.simplify(u.dot(u)), "   |w|^2 =", sp.simplify(w.dot(w)))

print("=== G. charpoly ===")
print("det(lam I - M0) =", sp.factor(sp.Poly((sp.Matrix.eye(6) * lam - M0).det(), lam).as_expr()))
print(
    "same as lam^2 (lam^2+9)^2 :",
    sp.simplify((sp.Matrix.eye(6) * lam - M0).det() - lam**2 * (lam**2 + 9) ** 2) == 0,
)

print("=== H. certification: directional derivatives of the TRUE field ===")
t = sp.Symbol("t", real=True)


def cert(direction, name):
    subs = {v: anchor[i] + t * direction[i] for i, v in enumerate(vars6)}
    path = F.subs(subs)
    deriv = sp.diff(path, t).subs(t, 0)
    target = M0 * direction  # * g/(2pi) restored below
    ok = sp.simplify(deriv - (g / (2 * pi)) * target) == sp.zeros(6, 1)
    print(f"H[{name}]: d/dt F(anchor + t*{name})(0) == (g/2pi) M0 {name} : {ok}")
    if not ok:
        print("  deriv  =", sp.simplify(deriv).T)
        print("  target=", sp.simplify((g / (2 * pi)) * target).T)
    return ok


cert(vT1, "vT1")
cert(vT2, "vT2")
cert(vR, "vR")
cert(vD, "vD")

# the shape eigenvectors found above
u_shape = sp.Matrix([1, 0, sp.Rational(1, 2), -r3 / 2, 0, 0])
w_shape = sp.Matrix([0, 1, r3 / 2, sp.Rational(1, 2), 0, 0])
cert(u_shape, "u_shape")
cert(w_shape, "w_shape")

print("=== J. modal basis: independence + dual covectors ===")
V = sp.Matrix.hstack(vT1, vT2, vR, vD, u_shape, w_shape)
print("det [vT1 vT2 vR vD u w] =", sp.simplify(sp.nsimplify(V.det(), [r3])))
D = sp.simplify(V.inv())
print("dual covector rows d_i (V.inv()):")
sp.pprint(sp.nsimplify(D, [r3]))
print("V * D == I:", sp.simplify(V * D) == sp.Matrix.eye(6))
print("orthogonality data:")
for nm, vec in [("vT1", vT1), ("vT2", vT2), ("vR", vR), ("vD", vD), ("u", u_shape), ("w", w_shape)]:
    print(f"  |{nm}|^2 =", sp.simplify(vec.dot(vec)))
print("  vD . vR =", sp.simplify(vD.dot(vR)))
print("  vD . vT1 =", sp.simplify(vD.dot(vT1)), "   vR . vT1 =", sp.simplify(vR.dot(vT1)))
print("  u . vT1 =", sp.simplify(u_shape.dot(vT1)), "   u . vT2 =", sp.simplify(u_shape.dot(vT2)))
print("  u . vR =", sp.simplify(u_shape.dot(vR)), "   u . vD =", sp.simplify(u_shape.dot(vD)))

print("=== K. numeric sanity of the raw Jacobian eigenvalues ===")
Jnum = sp.N(Jsub.subs(g, 1.0))
print(
    "numeric eigenvalues:",
    sorted([complex(ev) for ev in Jnum.eigenvals().keys()], key=lambda z: (z.real, z.imag)),
)

print("=== DONE ===")
