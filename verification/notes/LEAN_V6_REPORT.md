# LEAN_V6_REPORT — Section 10: nonlinear Lyapunov stability via H/I and the collinear bifurcation analysis

**Artifact:** `verification/lean4/Trivortex.lean` v6.0 (6 454 lines)
**Toolchain:** Lean 4 v4.6.0 + Mathlib4 tag v4.6.0 (pinned in `lakefile.lean`)
**Build:** `lake env lean Trivortex.lean` — **green, 0 errors** (benign
`unusedVariables` linter notes, the same class as in §1–§9)
**Axiom footprint:** all **166** `#print axioms` statements resolve to
exactly `[propext, Classical.choice, Quot.sound]` — Mathlib's classical
foundations only, nothing added. **No `sorry`, no `sorryAx`, no `axiom`
anywhere.**

**Numeric mirror:** `verification/notes/v2_ladder_track_s10.py` — the
**V2-ladder, all rungs PASS** (V0 spectral re-check, V1 Lyapunov H/I
ladder with RK4 integration of the true Kirchhoff ODE, V2 collinear
bifurcation ladder). `verification/notes/s10_preverify.py` — **all 30
symbolic identities PASS** (SymPy), including the log-Lyapunov
inequality constants, the coercive certificate constant Γ²/(12π), and
the collinear bifurcation polynomial
N(s,γ) = s(s−1)·[(γ+1)²(γ−1)s² + γ(4γ+5)s + (4γ+5)] with discriminant
(4γ+5)(γ+2)².

---

## 1. What Section 10 adds (24 new statements, 142 → 166 + defs)

Section 10 answers the two questions the v5 report left open: *is the
Lagrange triangle nonlinearly (Lyapunov) stable, not merely linearly?*
and *what happens to the collinear relative equilibria as the
circulations become unequal?*

### 10.1 Nonlinear Lyapunov stability via H/I (energy–Casimir)

| Statement | Content |
|---|---|
| `s10_sumsq`, `s10_sumsq_anchor` | the rigid identity Σᵢ<ⱼ r²ᵢⱼ = 3·Σ|w|² − |Σw|²; on the anchor level set {P = 0, Q = 0, I = Γ} the sum of the squared sides is EXACTLY 3 |
| `s10_log_bound` | the one-dimensional Lyapunov logarithmic inequality ln(1+u) ≤ u − u²/3 on |u| ≤ 1/2 (both half-intervals fenced against u − u²/3 from the exact contact point u = 0) |
| `s10_H_nonneg` | H ≥ 0 on the whole level set (AM–GM on the three squared sides, pure algebra: 4xy ≤ (x+y)², s²(3−s) ≤ 4 via (2−s)²(s+1) ≥ 0) — the triangle is the GLOBAL energy minimum |
| `s10_coercive` | **the coercive Lyapunov inequality**: on the level set with every squared side in the annulus [1/2, 3/2], H ≥ (Γ²/(12π))·Σᵢ<ⱼ (r²ᵢⱼ − 1)² — the certified constant Γ²/(12π) |
| `s10_dist_bound` | the distance form Σ(rᵢⱼ − 1)² ≤ (12π/Γ²)·H |
| `s10_casimir_x1..y3` | **the variational principle**: the energy–Casimir functional H + (3Γ/(4π))·I has ZERO gradient at the anchor (six slots) — the Lagrange multiplier ω_L = 3Γ/(4π), consistent with the §8 rotation rate up to the I-convention factor 2 |
| `s10_lyapunov_stab` | **the in-time Lyapunov stability theorem**: any Kirchhoff solution staying on the level set, starting with the energy excess ≤ (Γ²/(12π))·(1/16)² and all squared sides in the deep-interior target [15/16, 17/16], satisfies Σ(d²ᵢⱼ(t) − 1)² ≤ (12π/Γ²)·H(0) at EVERY time t ∈ ℝ — proved by the continuous-induction annulus propagation (the sSup/supremum-extension argument) and the exact conservation of H, I, P, Q |
| `s10_lyapunov_dist` | the distance form: Σ(rᵢⱼ(t) − 1)² ≤ (12π/Γ²)·H(0) for all t |

**The stability theorem in one line:** the equilateral triangle of three
equal point vortices is nonlinearly (Lyapunov) stable modulo the
symmetries, with the certified Lyapunov inequality as the quantitative
certificate — the shape deviation is controlled by the conserved energy
excess for all time, in both directions of time.

### 10.2 Collinear central configurations and their bifurcations

| Statement | Content |
|---|---|
| `s10_col_sol_gen` | **the general collinear rotating relative equilibrium**: centered distinct collinear triples (x₁, x₂, x₃) with circulations (1, 1, γ) rotate rigidly about the origin with rate w EXACTLY when the S-conditions Sₖ = 2πxₖw hold (S₁ = 1/(x₁−x₂) + γ/(x₁−x₃), etc.) |
| `s10_col_sym` | the symmetric branch (d, −d, 0) is a rotating relative equilibrium for EVERY γ (rate ω = (γ+½)/(2πd²)) — the midpoint cancellation makes all three S-conditions exact |
| `s10_col_static` | at γ = −½ the rotation rate vanishes: the collinear configuration is a genuine STATIONARY point of the Kirchhoff field — the steady-state bifurcation point |
| `s10_col_bif_eq` | the chart equation: the relative-equilibrium ratio condition is EXACTLY N(s, γ) = 0 with s = x₃/x₁ |
| `s10_col_pitchfork` | M̃(0, γ) = 4γ + 5 vanishes EXACTLY at γ = −5/4 — the pitchfork point where the asymmetric branch is born |
| `s10_col_disc` | the discriminant of M̃(s, γ) in s is (4γ+5)(γ+2)² — the complete bifurcation diagram |
| `s10_col_count_quarter` | at γ₀ = −1/4 the chart equation has exactly the roots s = 0, 16/9, −16/5 (plus the excluded collision s = 1): THREE collinear relative equilibria, two of them exactly rational |
| `s10_col_count_eq1` | at γ = 1 only the symmetric roots s = 0, −1 (every collinear relative equilibrium has a vortex at the midpoint) |
| `s10_col_asym` | **the exact asymmetric relative equilibrium** at Γ = (1, 1, −1/4): the configuration (1, −5/9, 16/9) with ω = 27/(56π) is a KirchhoffSol |

**The bifurcation theorem in one line:** the symmetric collinear branch
persists for every γ and loses its rotation rate at γ = −½; the
asymmetric branch exists exactly for γ > −5/4 (pitchfork at −5/4,
discriminant (4γ+5)(γ+2)²), so the number of collinear relative
equilibria jumps from one to three across the pitchfork — and at
γ₀ = −1/4 all three are exact rationals.

## 2. Method

1. **Derivation:** every identity was machine-derived and machine-checked
   in SymPy (`scripts/s10_preverify.py`, 30 checks) BEFORE the Lean
   encoding: the log-inequality constants, the coercive constant, the
   variational multiplier, the bifurcation polynomial and its
   discriminant, the rational asymmetric roots.
2. **Lean encoding:** the Lyapunov inequality is fenced
   (`image_le_of_deriv_right_le_deriv_boundary`) on both half-intervals
   from the contact point u = 0; the coercivity chains it over the three
   sides with the rigid identity Σd² = 3; the in-time stability is the
   continuous-induction annulus propagation (supremum extension with the
   deep-interior margin 7/16); the collinear field collapse is the
   pairwise-cancellation certificate x₁S₂ − x₂S₁ = γ(x₃S₁ − x₁S₃).
3. **Numeric mirror:** the V2-ladder (`scripts/v2_ladder_track_s10.py`)
   re-checks every formal statement numerically: the spectral ladder of
   §9, the rigid identity and the coercive certificate (Monte-Carlo,
   6 000 samples), the in-time Lyapunov bound along an RK4 integration of
   the true Kirchhoff ODE (6 000 steps, Hamiltonian drift 2e−15), the
   symmetric-branch rigid rotation over the γ-sweep, the static point,
   the root-count ladder across the pitchfork, and the exact asymmetric
   relative equilibria.

## 3. Acceptance criteria (all green)

| Criterion | Status |
|---|---|
| `lake env lean Trivortex.lean` compiles | **0 errors** |
| zero `sorry` / `sorryAx` / `axiom` declarations | **confirmed** |
| every `#print axioms` closed to `[propext, Classical.choice, Quot.sound]` | **166/166** |
| §10 numeric mirror (V2-ladder) | **all rungs PASS** |
| §10 symbolic pre-verification | **30/30 PASS** |
| bilingual status blocks updated | **done (EN + RU)** |

## 4. Files touched

| File | Change |
|---|---|
| `verification/lean4/Trivortex.lean` | v5.0 → v6.0: header, §10 (~1 540 new lines), 22 new `#print axioms` |
| `verification/lean4/README.md` | status block: v6.0, ten sections, 187 statements |
| `verification/lean4/README_RU.md` | то же по-русски |
| `verification/notes/s10_preverify.py` | **new** — symbolic pre-verification (30 checks) |
| `verification/notes/s10_preverify.log` | **new** — run log |
| `verification/notes/v2_ladder_track_s10.py` | **new** — the V2-ladder numerical track |
| `verification/notes/v2_ladder_track_s10.log` | **new** — run log (all rungs PASS) |

## 5. Scope notes (what is and is not claimed)

- The Lyapunov theorem is stated on the level set {P = Q = 0, I = Γ}
  with the initial data in the deep-interior target [15/16, 17/16] — the
  modulo-symmetries reduction (quotienting translations and rotations)
  is implicit in the distance-form conclusion; the certified constants
  are exact.
- The coercive inequality covers the annulus r²ᵢⱼ ∈ [1/2, 3/2]; the
  global (non-annulus) lower bound is the separate AM–GM theorem
  H ≥ 0.
- The collinear classification is stated in the x₁ ≠ 0 chart with the
  centering x₂ = −x₁ − γx₃; the count statements are up to scaling.
- The perturbation-theory (Crandall–Rabinowitz) theorem for the
  asymmetric branch beyond its existence at rational γ₀ remains open,
  as does the general-γ Lyapunov stability for unequal circulations.
