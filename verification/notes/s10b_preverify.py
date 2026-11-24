#!/usr/bin/env python3
"""S10b pre-verification — symbolic checks for the v7.0 deepening of Section 10
(the second asymmetric collinear relative equilibrium, the pitchfork triple
root, and the degenerate-circulation root counts).

House method (verification/notes/s10_preverify.py): every identity that the
Lean encoding relies on is machine-derived and machine-checked here BEFORE it
is encoded in Trivortex.lean.  Each check prints [PASS]/[FAIL]; the script
exits non-zero on any failure.

Run:  python3 s10b_preverify.py
"""
import sympy as sp
import sys

pi, s, g, d = sp.pi, sp.Symbol("s", real=True), sp.Symbol("gamma", real=True), sp.Symbol("d", positive=True)
x1, x2, x3, w = sp.symbols("x1 x2 x3 w", real=True, nonzero=True)

FAILS = []


def check(name, ok):
    print(("[PASS] " if ok else "[FAIL] ") + name)
    if not ok:
        FAILS.append(name)


# ---------------------------------------------------------------- chart equation
# N(s, gamma) = s(s-1) * Mtilde(s, gamma) with
#   Mtilde = (gamma+1)^2 (gamma-1) s^2 + gamma (4 gamma+5) s + (4 gamma+5)
Mtilde = (g + 1) ** 2 * (g - 1) * s ** 2 + g * (4 * g + 5) * s + (4 * g + 5)
N = s * (s - 1) * Mtilde
check("Mtilde(s,-5/4) = -(9/64) s^2", sp.simplify(Mtilde.subs(g, sp.Rational(-5, 4)) - sp.Rational(-9, 64) * s ** 2) == 0)

# ------------------------------------------------------- 1. pitchfork triple root
lhs = sp.expand(N.subs(g, sp.Rational(-5, 4)))
rhs = sp.expand(sp.Rational(-9, 64) * s ** 3 * (s - 1))
check("N(s,-5/4) = -(9/64) s^3 (s-1)", sp.simplify(lhs - rhs) == 0)
check("pitchfork triple root at s=0", sp.degree(sp.Poly(lhs, s), gen=s) == 4 and sp.Poly(lhs, s).coeff_monomial(s) == 0)

# -------------------------------------------- 2. degenerate circulation gamma=-1
lhs_m1 = sp.factor(N.subs(g, -1))
check("N(s,-1) = -s (s-1)^2", sp.simplify(lhs_m1 - (-s * (s - 1) ** 2)) == 0)
check("roots of N(s,-1) exactly {0,1}", sp.solve(N.subs(g, -1), s) == [0, 1])

# -------------------------------------------- 3. degenerate circulation gamma=-2
lhs_m2 = sp.factor(N.subs(g, -2))
check("N(s,-2) = -3 s (s-1)^3", sp.simplify(lhs_m2 - (-3 * s * (s - 1) ** 3)) == 0)
check("roots of N(s,-2) exactly {0,1}", sp.solve(N.subs(g, -2), s) == [0, 1])

# --------------------------------- 4. the SECOND asymmetric relative equilibrium
# gamma = -1/4 chart: s = x3/x1 = -16/5, centering x2 = -x1 - gamma x3.
g0 = sp.Rational(-1, 4)
s0 = sp.Rational(-16, 5)
xa = sp.Integer(1)                     # chart scale x1 = 1
xb = sp.simplify(-xa - g0 * s0)        # centering: sum g_k x_k = 0
xc = s0 * xa
check("centering x2 = -9/5", xb == sp.Rational(-9, 5))
check("momentum P = sum g_k x_k = 0", sp.simplify(1 * xa + 1 * xb + g0 * xc) == 0)

S1 = 1 / (xa - xb) + g0 / (xa - xc)
S2 = 1 / (xb - xa) + g0 / (xb - xc)
S3 = 1 / (xc - xa) + 1 / (xc - xb)
w2 = sp.simplify(S1 / (2 * pi * xa))   # 2 pi x1 w = S1
check("w = 25/(168 pi)", w2 == sp.Rational(25, 84) / (2 * pi))
check("2pi x2 w = S2", sp.simplify(2 * pi * xb * w2 - S2) == 0)
check("2pi x3 w = S3", sp.simplify(2 * pi * xc * w2 - S3) == 0)
check("S1 = 25/84", S1 == sp.Rational(25, 84))
check("S2 = -15/28", S2 == sp.Rational(-15, 28))
check("S3 = -20/21", S3 == sp.Rational(-20, 21))
# the three S-conditions, as the Lean hypotheses use them
for k, (xk, Sk) in enumerate([(xa, S1), (xb, S2), (xc, S3)], 1):
    ok = sp.simplify(
        (1 / (xk - xb) + g0 / (xk - xc) if k == 1 else
         1 / (xk - xa) + g0 / (xk - xc) if k == 2 else
         1 / (xk - xa) + 1 / (xk - xb))
        - 2 * pi * xk * w2)
    check(f"S-condition k={k} for (1,-9/5,-16/5), w=25/(168pi)", ok == 0)

# pairwise distinctness (the Lean e12/e13/e23 hypotheses)
check("distinct: 1 - (-9/5) != 0", xa - xb != 0)
check("distinct: 1 - (-16/5) != 0", xa - xc != 0)
check("distinct: -9/5 - (-16/5) != 0", xb - xc != 0)

# --------------------------- 5. cross-check of the FIRST asymmetric equilibrium
xb1, xc1 = sp.Rational(-5, 9), sp.Rational(16, 9)
S1a = 1 / (xa - xb1) + g0 / (xa - xc1)
S2a = 1 / (xb1 - xa) + g0 / (xb1 - xc1)
S3a = 1 / (xc1 - xa) + 1 / (xc1 - xb1)
wa = sp.simplify(S1a / (2 * pi * xa))
check("first asym: w = 27/(56 pi)", wa == sp.Rational(27, 56) / pi)
check("first asym: 2pi x2 w = -15/28", sp.simplify(2 * pi * xb1 * wa) == sp.Rational(-15, 28))
check("first asym: 2pi x3 w = 12/7", sp.simplify(2 * pi * xc1 * wa) == sp.Rational(12, 7))

# ------------------------------------------------- 6. bifurcation diagram sanity
check("N(s,-1/4) factor = s(s-1)(-(9s-16)(5s+16))/64",
      sp.simplify(N.subs(g, sp.Rational(-1, 4)) - s * (s - 1) * (-(9 * s - 16) * (5 * s + 16) / 64)) == 0)
check("N(s,1) = 9 s (s-1)(s+1)", sp.expand(N.subs(g, 1) - 9 * s * (s - 1) * (s + 1)) == 0)
check("disc Mtilde = (4g+5)(g+2)^2",
      sp.simplify((g * (4 * g + 5)) ** 2 - 4 * (g + 1) ** 2 * (g - 1) * (4 * g + 5)
                  - (4 * g + 5) * (g + 2) ** 2) == 0)

print()
if FAILS:
    print(f"FAILED: {len(FAILS)}")
    sys.exit(1)
print("ALL PASS")
