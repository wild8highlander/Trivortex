# LEAN_V7_REPORT — Section 10.3: the collinear bifurcation picture completed, plus the package features

**Artifact:** `verification/lean4/Trivortex.lean` v7.0 (6 589 lines)
**Toolchain:** Lean 4 v4.6.0 + Mathlib4 tag v4.6.0 (pinned in `lakefile.lean`,
unchanged from v6.0)
**Method:** the house discipline — every identity machine-derived and
machine-checked in SymPy (`verification/notes/s10b_preverify.py`, **27/27
PASS**) *before* the Lean encoding, then encoded strictly in the established
proof idioms of §10 (`unfold` + `ring` polynomial forms, `mul_eq_zero` root
ladders, the `s10_col_sol_gen` assembly with `field_simp [Real.pi_pos.ne']` +
`norm_num` rational certificates).
**Honest scope note:** the Lean toolchain is not available in the authoring
sandbox, so `lake build` was not run here; the four new proofs are pure
`ring`/`norm_num`-style algebra over previously-proven shapes
(`s10_col_sol_gen` closed 22 statements in v6.0), and every numeric claim is
backed by the committed SymPy log.

---

## 1. What v7.0 adds

### 1.1 Four new theorems (§10.3, inside Section 10)

| Statement | Content |
|---|---|
| `s10_pitchfork_double` | at the pitchfork γ = −5/4 the chart polynomial collapses to **N(s, −5/4) = −(9/64)·s³·(s−1)** — the quadratic factor degenerates to −(9/64)s², so the symmetric root s = 0 is TRIPLE: the two asymmetric roots collide with it exactly at the pitchfork |
| `s10_col_count_neg1` | at γ = −1 ((γ+1)² = 0 kills the quadratic term) N(s, −1) = −s(s−1)², so the only roots are the symmetric s = 0 and the excluded collision s = 1 — the asymmetric branch has merged back, ONE distinct relative equilibrium |
| `s10_col_count_neg2` | at γ = −2 ((γ+2)² = 0 kills the discriminant) the quadratic factor is the perfect square −3(s−1)² and N(s, −2) = −3·s·(s−1)³ — again only s = 0 plus the TRIPLE excluded collision root |
| `s10_col_asym2` | **the second exact rational asymmetric relative equilibrium** at Γ = (1, 1, −1/4): the configuration (1, −9/5, −16/5) with ω = 25/(168π) is a `KirchhoffSol` — together with `s10_col_asym` BOTH asymmetric roots s = 16/9 and s = −16/5 of the chart are realized by exact rational configurations |

The bifurcation theorem of §10 now reads in full: the symmetric collinear
branch persists for every γ and loses its rotation rate at γ = −½; the
asymmetric branch is born at the pitchfork γ = −5/4 — where the symmetric root
is TRIPLE — exists for γ > −5/4 (discriminant (4γ+5)(γ+2)²), merges back for
the degenerate circulations γ = −1 and γ = −2, and at γ₀ = −1/4 all three
relative equilibria are exact rationals, BOTH asymmetric ones realized as
`KirchhoffSol` values.

### 1.2 The data that motivated it

The v6.0 pre-verification log (`s10_preverify.log`, "extras" block) already
carried the second asymmetric solution and the pitchfork factorization —
formalized here. The new script re-derives everything independently and adds
the degenerate-circulation counts:

```
[PASS] N(s,-5/4) = -(9/64) s^3 (s-1)          [PASS] centering x2 = -9/5
[PASS] N(s,-1) = -s (s-1)^2                   [PASS] momentum P = sum g_k x_k = 0
[PASS] N(s,-2) = -3 s (s-1)^3                 [PASS] w = 25/(168 pi)
[PASS] roots of N(s,-1) exactly {0,1}         [PASS] 2pi x2 w = S2 / 2pi x3 w = S3
[PASS] roots of N(s,-2) exactly {0,1}         [PASS] S-conditions k=1,2,3
...
ALL PASS
```

## 2. Package features added in v7.0

| Feature | File(s) | What it does |
|---|---|---|
| **Statement index** | `lean4/docs/STATEMENTS.md` + `notes/make_statement_index.py` | auto-generated index of all **170** theorems grouped by section (11 groups), each with its docstring's first line; header carries the metric table (170 prints, 0 sorry, 0 axiom); regenerate after every change |
| **Dedicated CI lane** | `.github/workflows/lean-verify.yml` | standalone pinned build (lean-action, cache-first) + the **axiom-footprint guard**: every printed footprint must equal `[propext, Classical.choice, Quot.sound]`, any `sorryAx` fails the run; a stale-`STATEMENTS.md` warning |
| **Two new GIF assets** | `lean4/assets/lyapunov_stability.gif`, `lean4/assets/collinear_bifurcation.gif` | §10.1: the perturbed triangle under the TRUE Kirchhoff flow (RK4, the same initial data as the V1 ladder rung) with the certified bound `Σ(d²−1)² ≤ (12π/Γ²)H(0)` held for all t (Hamiltonian drift 1.7e−15 on screen); §10.2/10.3: the chart equation N(s,γ)=0 with the live root sweep across the pitchfork, the degenerate circulations, the rational anchors, and the rigidly rotating relative equilibria — both in the repository traffic-light palette, generator committed (`notes/make_s10_gifs.py`) |
| **READMEs synced to v7.0** | `lean4/README.md`, `lean4/README_RU.md` | the v6.0 commit had left both at v5.0; now: status blocks, badges (170 axioms, 309 theorems, 6 589 lines), TOC §1–§10, the §6.10 deep dive with both GIFs, the three-footprint-block contract (170/170), file inventory with `docs/STATEMENTS.md`, CI section with `lean-verify.yml`, timeline v6.0+v7.0 rows, constellation/matrix rows, gallery, FAQ numbers, roadmap (§10 landed; open: Crandall–Rabinowitz, general-γ Lyapunov), Appendix A census with the §10 block |
| **notes/README.md completed** | `notes/README.md` | the v6.0 scripts were never listed there; now all §10 tracks, the v7.0 scripts, their run lines and the committed-log verdicts are in the tables |

## 3. Acceptance criteria (as far as the sandbox allows)

| Criterion | Status |
|---|---|
| §10.3 symbolic pre-verification (`s10b_preverify.py`) | **27/27 PASS** (committed log) |
| zero `sorry` / `sorryAx` / `axiom` declarations | **confirmed** by scan (proof-terminator scan + header/footer audit) |
| `#print axioms` statements | **170** — one per public theorem, all new theorems printed |
| declaration census | 309 theorems/lemmas (170 public + 139 private) · 58 defs · 2 structures — matches every number quoted in both READMEs |
| `lake env lean Trivortex.lean` compiles | **not run in the sandbox** (no Lean toolchain); the four new proofs reuse the exact idioms that closed 22 §10 statements in v6.0 — run `lake build` (or the new `lean-verify.yml` lane) to confirm |
| README/README_RU anchor sync | script-driven, every replacement asserted unique (`notes/update_readme_v7.py`) |

## 4. Files touched

| File | Change |
|---|---|
| `verification/lean4/Trivortex.lean` | v6.0 → v7.0: header block 6'', §10.3 (~130 new lines: 4 theorems), 4 new `#print axioms` |
| `verification/lean4/docs/STATEMENTS.md` | **new** — auto-generated statement index (170 theorems / 11 sections) |
| `verification/lean4/README.md` | v5.0 → v7.0 sync (40 anchored replacements + 3 inserts) |
| `verification/lean4/README_RU.md` | то же по-русски (39 replacements + 3 inserts) |
| `verification/lean4/assets/lyapunov_stability.gif` | **new** — 88 frames, 0.43 MB |
| `verification/lean4/assets/collinear_bifurcation.gif` | **new** — 96 frames, 1.00 MB |
| `verification/notes/s10b_preverify.py` / `.log` | **new** — 27/27 PASS |
| `verification/notes/make_s10_gifs.py` | **new** — the GIF generator |
| `verification/notes/make_statement_index.py` | **new** — the statement-index generator |
| `verification/notes/update_readme_v7.py` | **new** — the README sync script (kept for provenance) |
| `verification/notes/README.md` | the v6/v7 scripts, run lines and log verdicts added to the tables |
| `verification/notes/LEAN_V7_REPORT.md` | **new** — this report |
| `.github/workflows/lean-verify.yml` | **new** — the dedicated CI lane |

## 5. Scope notes (what is and is not claimed)

- The four new theorems are exact algebraic statements about the chart
  polynomial and the Kirchhoff solution structure — they complete the
  *bifurcation diagram*, not the perturbation theory.
- The Crandall–Rabinowitz theorem for the asymmetric branch beyond its
  existence at rational γ₀ and general-γ Lyapunov stability for unequal
  circulations remain open (now recorded in the roadmap of both READMEs).
- The CI workflow is delivered as a file; it runs on GitHub infrastructure
  and was not executed in the authoring sandbox.
