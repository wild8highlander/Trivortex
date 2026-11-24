#!/usr/bin/env python3
"""Sync README.md and README_RU.md from the v5.0 state to v7.0:
v6.0 (Section 10) + v7.0 (Section 10.3 deepening, new GIFs, statement index,
CI workflow, census).  Every replacement is an exact-anchor pair asserted to
hit the expected number of times — a missed anchor aborts the run."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.join(HERE, "..", "lean4")

# ----------------------------------------------------------------- shared new content
S610_EN = '''
### 6.10 Section 10 — nonlinear Lyapunov stability and the completed collinear bifurcation (§10.1–§10.3)

The v6.0–v7.0 depth tracks, in three moves:

1. **10.1 — energy–Casimir (Lyapunov H/I) stability.** On the momentum level set
   `{P = 0, Q = 0, I = Γ}` the rigid identity `Σᵢ<ⱼ d²ᵢⱼ = 3` holds exactly
   (`s10_sumsq_anchor`); the logarithmic inequality `ln(1+u) ≤ u − u²/3`
   (`s10_log_bound`) drives the **coercive certificate**
   `H ≥ (Γ²/(12π))·Σ(d²ᵢⱼ−1)²` over the annulus `d²ᵢⱼ ∈ [1/2, 3/2]`
   (`s10_coercive`) — and AM–GM makes the triangle the global energy minimum
   (`s10_H_nonneg`). The energy–Casimir functional `H + (3Γ/(4π))·I` has zero
   gradient at the anchor in all six slots (`s10_casimir_x1…y3`, multiplier
   `ω_L = 3Γ/(4π)`), and the in-time theorem `s10_lyapunov_stab` closes the
   loop: any level-set solution starting in the deep-interior target
   `[15/16, 17/16]` satisfies `Σ(d²ᵢⱼ(t)−1)² ≤ (12π/Γ²)·H(0)` at **every**
   `t ∈ ℝ` — continuous-induction annulus propagation plus the exact
   conservation of `H, I, P, Q` (`s10_lyapunov_dist` is the distance form).

![Lyapunov stability: the perturbed triangle under the true Kirchhoff flow, the certified bound held for all t](assets/lyapunov_stability.gif)

2. **10.2 — collinear central configurations and their bifurcations.** The
   general collinear rotating relative equilibrium (`s10_col_sol_gen`), the
   symmetric branch `(d, −d, 0)` for every γ (`s10_col_sym`), the static point
   at `γ = −½` (`s10_col_static`); the chart equation `N(s, γ) = s(s−1)·M̃(s, γ)`
   with the pitchfork `M̃(0, γ) = 4γ+5` vanishing exactly at `γ = −5/4`
   (`s10_col_pitchfork`), the discriminant `(4γ+5)(γ+2)²` (`s10_col_disc`), the
   root-count ladder at `γ₀ = −1/4` (`s10_col_count_quarter`) and `γ = 1`
   (`s10_col_count_eq1`), and the exact asymmetric relative equilibrium
   `(1, −5/9, 16/9)` at `ω = 27/(56π)` (`s10_col_asym`).
3. **10.3 — the bifurcation picture completed (v7.0).** The pitchfork is a
   **triple root**: `N(s, −5/4) = −(9/64)·s³·(s−1)` (`s10_pitchfork_double`).
   At the degenerate circulations the asymmetric branch merges back into the
   symmetric one: `γ = −1` ((γ+1)² = 0 → `N = −s(s−1)²`,
   `s10_col_count_neg1`) and `γ = −2` ((γ+2)² = 0 → `N = −3·s·(s−1)³`,
   `s10_col_count_neg2`). And the **second** exact rational asymmetric
   relative equilibrium at `γ₀ = −1/4` lands: `(1, −9/5, −16/5)` with
   `ω = 25/(168π)` (`s10_col_asym2`) — both asymmetric roots `s = 16/9` and
   `s = −16/5` of the chart are now realized as exact `KirchhoffSol` values.
   Every identity was SymPy-certified before the Lean encoding
   ([`../notes/s10b_preverify.py`](../notes/s10b_preverify.py), 27/27 PASS).

![The collinear bifurcation across the pitchfork γ = −5/4: the chart equation, the live root sweep, and the rotating relative equilibria](assets/collinear_bifurcation.gif)

'''

S610_RU = '''
### 6.10 Секция 10 — нелинейная устойчивость по Ляпунову и завершённая коллинеарная бифуркация (§10.1–§10.3)

Треки углубления v6.0–v7.0, тремя ходами:

1. **10.1 — устойчивость по Ляпунову через H/I (энергия–Казимир).** На уровне
   моментов `{P = 0, Q = 0, I = Γ}` жёсткое тождество `Σᵢ<ⱼ d²ᵢⱼ = 3` выполняется
   точно (`s10_sumsq_anchor`); логарифмическое неравенство
   `ln(1+u) ≤ u − u²/3` (`s10_log_bound`) даёт **коэрцитивный сертификат**
   `H ≥ (Γ²/(12π))·Σ(d²ᵢⱼ−1)²` на аннулусе `d²ᵢⱼ ∈ [1/2, 3/2]` (`s10_coercive`),
   а AM–GM делает треугольник глобальным минимумом энергии (`s10_H_nonneg`).
   Функционал энергия–Казимир `H + (3Γ/(4π))·I` имеет нулевой градиент в якоре
   по всем шести слотам (`s10_casimir_x1…y3`, множитель `ω_L = 3Γ/(4π)`), и
   теорема во времени `s10_lyapunov_stab` замыкает картину: любое решение на
   уровне, стартующее в глубинной мишени `[15/16, 17/16]`, удовлетворяет
   `Σ(d²ᵢⱼ(t)−1)² ≤ (12π/Γ²)·H(0)` в **каждый** момент `t ∈ ℝ` —
   непрерывная индукция по аннулусу плюс точное сохранение `H, I, P, Q`
   (`s10_lyapunov_dist` — форма расстояний).

![Устойчивость по Ляпунову: возмущённый треугольник в истинном потоке Кирхгоффа, сертифицированная граница держится всё время](assets/lyapunov_stability.gif)

2. **10.2 — коллинеарные центральные конфигурации и их бифуркации.** Общее
   коллинеарное вращающееся относительное равновесие (`s10_col_sol_gen`),
   симметричная ветвь `(d, −d, 0)` при любом γ (`s10_col_sym`), стационарная
   точка при `γ = −½` (`s10_col_static`); уравнение карты
   `N(s, γ) = s(s−1)·M̃(s, γ)` с вилкой `M̃(0, γ) = 4γ+5`, исчезающей ровно при
   `γ = −5/4` (`s10_col_pitchfork`), дискриминант `(4γ+5)(γ+2)²`
   (`s10_col_disc`), лестница подсчёта корней при `γ₀ = −1/4`
   (`s10_col_count_quarter`) и `γ = 1` (`s10_col_count_eq1`), и точное
   асимметричное относительное равновесие `(1, −5/9, 16/9)` с `ω = 27/(56π)`
   (`s10_col_asym`).
3. **10.3 — картина бифуркации завершена (v7.0).** Вилка — **тройной корень**:
   `N(s, −5/4) = −(9/64)·s³·(s−1)` (`s10_pitchfork_double`). При вырожденных
   циркуляциях асимметричная ветвь сливается обратно с симметричной:
   `γ = −1` ((γ+1)² = 0 → `N = −s(s−1)²`, `s10_col_count_neg1`) и `γ = −2`
   ((γ+2)² = 0 → `N = −3·s·(s−1)³`, `s10_col_count_neg2`). И **вторая** точная
   рациональная асимметричная конфигурация при `γ₀ = −1/4`: `(1, −9/5, −16/5)`
   с `ω = 25/(168π)` (`s10_col_asym2`) — оба асимметричных корня карты
   `s = 16/9` и `s = −16/5` реализованы как точные `KirchhoffSol`. Каждое
   тождество сертифицировано SymPy до Lean-кодирования
   ([`../notes/s10b_preverify.py`](../notes/s10b_preverify.py), 27/27 PASS).

![Коллинеарная бифуркация поперёк вилки γ = −5/4: уравнение карты, живой обзор корней и вращающиеся относительные равновесия](assets/collinear_bifurcation.gif)

'''

S10_CENSUS_EN = '''<details>
<summary><b>Section 10 — nonlinear Lyapunov stability and the collinear bifurcation</b> — lines 4891–6518: 26 theorems/lemmas, 3 defs · <i>click to expand</i></summary>

**Definitions & structures:** `colOmega` · `s10ColM` · `s10ColN`

**Theorems & lemmas:**
`s10_log_bound` · `s10_sumsq` · `s10_sumsq_anchor` · `s10_H_nonneg` · `s10_coercive` · `s10_dist_bound`
`s10_casimir_x1` · `s10_casimir_y1` · `s10_casimir_x2` · `s10_casimir_y2` · `s10_casimir_x3` · `s10_casimir_y3`
`s10_lyapunov_stab` · `s10_lyapunov_dist` · `s10_col_sol_gen` · `s10_col_sym` · `s10_col_static` · `s10_col_pitchfork`
`s10_col_disc` · `s10_col_count_quarter` · `s10_col_count_eq1` · `s10_col_asym` · `s10_pitchfork_double` · `s10_col_count_neg1`
`s10_col_count_neg2` · `s10_col_asym2`

</details>

'''

# ------------------------------------------------------------------- EN pairs
EN_PAIRS = [
    # banner alt text
    ("144 axioms closed, 0 sorry, 0 axiom",
     "170 axioms closed, 0 sorry, 0 axiom", 1),
    # intro block
    ("""**The formalization layer, landed at v5.0.** One file — `Trivortex.lean`, 4,915 lines —
re-derives the analytic core of the vortex three-body program inside
[Lean 4](https://lean-lang.org) + [Mathlib](https://github.com/leanprover-community/mathlib4):
Theorem 3.1 (the closed-form Lagrange-type choreography), the Chaplygin topological
integral, the Kirchhoff conservation laws, the Lagrange equilateral solution, the
complete triangle theory, linear stability, and the bifurcation at unequal circulations —
**144 `#print axioms` statements, zero `sorry`, zero `axiom`**, every footprint closed on
exactly `propext · Classical.choice · Quot.sound`.""",
     """**The formalization layer, landed at v7.0.** One file — `Trivortex.lean`, 6,589 lines —
re-derives the analytic core of the vortex three-body program inside
[Lean 4](https://lean-lang.org) + [Mathlib](https://github.com/leanprover-community/mathlib4):
Theorem 3.1 (the closed-form Lagrange-type choreography), the Chaplygin topological
integral, the Kirchhoff conservation laws, the Lagrange equilateral solution, the
complete triangle theory, linear stability, the bifurcation at unequal circulations,
nonlinear Lyapunov stability via H/I, and the completed collinear bifurcation picture —
**170 `#print axioms` statements, zero `sorry`, zero `axiom`**, every footprint closed on
exactly `propext · Classical.choice · Quot.sound`.""", 1),
    ("%23print%20axioms-144%20closed", "%23print%20axioms-170%20closed", 1),
    ("landed%20v5.0%20(%C2%A71%E2%80%93%C2%A79)-gold",
     "landed%20v7.0%20(%C2%A71%E2%80%93%C2%A710.3)-gold", 1),
    ("README.md#11-version-timeline--v11--v50", "README.md#11-version-timeline--v11--v70", 1),
    ("artifact-4%2C915%20lines", "artifact-6%2C589%20lines", 1),
    ("theorems-243-", "theorems-309-", 1),
    ("defs%20%2B%20structures-55%20%2B%202-", "defs%20%2B%20structures-58%20%2B%202-", 1),
    ("milestone-M1%20%2B%20M4%2FM5%20depth-", "milestone-M1%20%2B%20M4%2FM5%20%2B%20%C2%A710%20depth-", 1),
    # TOC
    ("6. [Deep dive — section by section (§1–§9)](#6-deep-dive--section-by-section-19)",
     "6. [Deep dive — section by section (§1–§10)](#6-deep-dive--section-by-section-110)", 1),
    ("11. [Version timeline — v1.1 → v5.0](#11-version-timeline--v11--v50)",
     "11. [Version timeline — v1.1 → v7.0](#11-version-timeline--v11--v70)", 1),
    # TL;DR table
    ("| **Artifact** | [`Trivortex.lean`](Trivortex.lean) — 4,915 lines, one namespace, one file |",
     "| **Artifact** | [`Trivortex.lean`](Trivortex.lean) — 6,589 lines, one namespace, one file |", 1),
    ("| **Sections** | §1–§9 (+ two axiom-footprint blocks) — see the [deep dive](#6-deep-dive--section-by-section-19) |",
     "| **Sections** | §1–§10.3 (+ three axiom-footprint blocks) — see the [deep dive](#6-deep-dive--section-by-section-110) |", 1),
    ("| **Declarations** | 243 theorems/lemmas (144 public + 99 `private` helpers) · 55 defs · 2 structures |",
     "| **Declarations** | 309 theorems/lemmas (170 public + 139 `private` helpers) · 58 defs · 2 structures |", 1),
    ("| **Machine-checked closure** | **144 `#print axioms` statements — all closed**",
     "| **Machine-checked closure** | **170 `#print axioms` statements — all closed**", 1),
    ("| **Status** | ✅ **landed — v5.0** (statement layer §1–§9; M1 + the M4/M5 depth tracks) |",
     "| **Status** | ✅ **landed — v7.0** (§1–§10.3; M1 + the M4/M5 depth tracks + the §10 stability/bifurcation track) |", 1),
    # deep-dive intro + header
    ("and §7–§9 (over half the file) are the v3.0–v5.0 depth tracks.",
     "and §7–§10 (over half the file) are the v3.0–v7.0 depth tracks.", 1),
    ("## 6. Deep dive — section by section (§1–§9)",
     "## 6. Deep dive — section by section (§1–§10)", 1),
    # axiom-footprint section
    ("""Every load-bearing statement ends in the two footprint blocks of the artifact
(lines 3373–3494 for §1–§8, lines 4874–4913 for §9). The contract they enforce:""",
     """Every load-bearing statement ends in one of the three footprint blocks of the
artifact (lines 3389–3510 for §1–§8, lines 6519–6559 for §9, lines 6560–6589 for
§10). The contract they enforce:""", 1),
    ("144 / 144  #print axioms statements closed   ·   0 sorry   ·   0 axiom",
     "170 / 170  #print axioms statements closed   ·   0 sorry   ·   0 axiom", 1),
    # file inventory
    ("| [`Trivortex.lean`](Trivortex.lean) | 4,915 | 243 KB | the artifact: §1–§9 + axiom footprint (see [§6](#6-deep-dive--section-by-section-19)) |",
     "| [`Trivortex.lean`](Trivortex.lean) | 6,589 | 331 KB | the artifact: §1–§10.3 + axiom footprint (see [§6](#6-deep-dive--section-by-section-110)) |", 1),
    ("| [`README_RU.md`](README_RU.md) | — | — | the same overview, in Russian |",
     """| [`README_RU.md`](README_RU.md) | — | — | the same overview, in Russian |
| [`docs/STATEMENTS.md`](docs/STATEMENTS.md) | auto | 24 KB | the auto-generated index of all 170 theorems, grouped by section (regenerate: `python3 ../notes/make_statement_index.py`) |""", 1),
    # CI mermaid + dedicated workflow
    ('D{"footprint check<br/>#print axioms × 144"}', 'D{"footprint check<br/>#print axioms × 170"}', 1),
    ("""(lines 3373–3494 for §1–§8, lines 4874–4913 for §9).""", """(see [§7](#7-the-axiom-footprint--nothing-but-classical-foundations)).""", 0),  # placeholder no-op guard
    # reproducibility pins
    ("| Artifact | [`Trivortex.lean`](Trivortex.lean) — §1–§9, 144 `#print axioms` statements |",
     "| Artifact | [`Trivortex.lean`](Trivortex.lean) — §1–§10.3, 170 `#print axioms` statements |", 1),
    ("| Milestone | M1 + the M4/M5 depth tracks (conservation + Lagrange + stability + bifurcation) |",
     "| Milestone | M1 + the depth tracks §7–§10 (triangle theory + stability + bifurcation + Lyapunov) |", 1),
    # timeline
    ("## 11. Version timeline — v1.1 → v5.0", "## 11. Version timeline — v1.1 → v7.0", 1),
    ("    v5.0 : Section 9 — nonlinear continuation : general-circulation family s9_rel_eq : exact mode persistence : bifurcation at Π = 0 with explicit instances\n",
     """    v5.0 : Section 9 — nonlinear continuation : general-circulation family s9_rel_eq : exact mode persistence : bifurcation at Π = 0 with explicit instances
    v6.0 : Section 10 — Lyapunov stability via H/I : coercive certificate Γ²/(12π) : energy–Casimir criticality : collinear pitchfork at γ = −5/4
    v7.0 : §10.3 — bifurcation completed : pitchfork triple root : degenerate γ = −1, −2 : second rational asymmetric RE (1, −9/5, −16/5) · ω = 25/(168π)
""", 1),
    ("| v5.0 | §9 | nonlinear continuation + bifurcation | instability across `Π = 0`, proven |",
     """| v5.0 | §9 | nonlinear continuation + bifurcation | instability across `Π = 0`, proven |
| v6.0 | §10.1–§10.2 | nonlinear Lyapunov stability + the collinear bifurcation | coercive certificate, energy–Casimir criticality, pitchfork, asymmetric RE |
| v7.0 | §10.3 | the bifurcation picture completed | pitchfork triple root, degenerate circulations, both rational asymmetric REs |""", 1),
    # constellation + matrix
    ("**`Trivortex.lean` — §1–§9, 144 axioms closed**", "**`Trivortex.lean` — §1–§10.3, 170 axioms closed**", 1),
    ("§8/§9 numeric mirrors & identity checks (the SymPy pre-verification of the Lean algebra)",
     "§8/§9/§10 numeric mirrors & identity checks (the SymPy pre-verification of the Lean algebra)", 1),
    ("✔ **144 closed footprints**", "✔ **170 closed footprints**", 1),
    ("✔ **proven (§8–§9)**", "✔ **proven (§8–§10)**", 1),
    # gallery pack list
    ("[`assets/bifurcation_window.gif`](assets/bifurcation_window.gif) (§9),",
     """[`assets/bifurcation_window.gif`](assets/bifurcation_window.gif) (§9),
[`assets/lyapunov_stability.gif`](assets/lyapunov_stability.gif) (§10.1),
[`assets/collinear_bifurcation.gif`](assets/collinear_bifurcation.gif) (§10.2–10.3),""", 1),
    # FAQ
    ("Here every one of the 144 printed\nstatements shows only `propext`, `Classical.choice`, `Quot.sound`.",
     "Here every one of the 170 printed\nstatements shows only `propext`, `Classical.choice`, `Quot.sound`.", 1),
    ("which is why the census counts 144\nfootprints over 243 theorems plus defs.",
     "which is why the census counts 170\nfootprints over 309 theorems plus defs.", 1),
    ("(57 SymPy PASS lines for §9,\n19 for §8 — see the logs there).",
     "(57 SymPy PASS lines for §9,\n19 for §8, 30 for §10 and 27 more for the §10.3 deepening — see the logs there).", 1),
    # roadmap
    ("  then in at least two ports; if the Lean port takes it, expect a §10.",
     """  then in at least two ports. The §10 slot is taken: v6.0–v7.0 landed Lyapunov
  stability via H/I and the completed collinear bifurcation; the next widening
  candidate is the V5 `N = 7` ring — expect a §11. Two open-theory targets from
  the §10 scope notes: the Crandall–Rabinowitz perturbation theorem for the
  asymmetric branch beyond γ₀ = −1/4, and general-γ Lyapunov stability for
  unequal circulations.""", 1),
    # census
    ("**Full declaration census** — 243 theorems/lemmas (144 public + 99 `private` helpers) + 57 definitions/structures. Names are verbatim Lean identifiers.",
     "**Full declaration census** — 309 theorems/lemmas (170 public + 139 `private` helpers) + 60 definitions/structures. Names are verbatim Lean identifiers.", 1),
    ("<summary><b>Axiom footprint (§1–§8 prints)</b> — lines 3373–4915: 39 theorems/lemmas, 11 defs · <i>click to expand</i></summary>",
     "<summary><b>Section 9 — nonlinear continuation and bifurcation (§9)</b> — lines 3511–4890: 39 theorems/lemmas, 11 defs · <i>click to expand</i></summary>", 1),
]

EN_INSERTS = [
    # §6.10 before section 7 (EN)
    ("\n---\n\n## 7. The axiom footprint — nothing but classical foundations",
     S610_EN, "before"),
    # dedicated CI workflow paragraph after the §9.3 mermaid fence
    ('    D -->|"any leak"| F["red · port blocked"]\n```\n',
     '''
**v7.0 addition — a dedicated `lean-verify.yml` workflow** (`.github/workflows/`):
the same pinned build, standalone — elan from `lean-toolchain`, `lake exe cache
get`, `lake build`, then the axiom-footprint guard: every printed footprint must
equal `[propext, Classical.choice, Quot.sound]`, and any `sorryAx` fails the run
on the spot.
''', "after"),
    # census §10 block before CENSUS-END
    ("<!--CENSUS-END-->", S10_CENSUS_EN, "before"),
]


def apply(path, pairs, inserts):
    src = open(path, encoding="utf-8").read()
    for old, new, cnt in pairs:
        if cnt == 0:
            continue
        n = src.count(old)
        assert n == cnt, f"{os.path.basename(path)}: {n} hits (want {cnt}) for {old[:70]!r}"
        src = src.replace(old, new)
    for anchor, text, mode in inserts:
        n = src.count(anchor)
        assert n == 1, f"{os.path.basename(path)}: anchor {n} hits (want 1): {anchor[:60]!r}"
        src = src.replace(anchor, text + anchor if mode == "before" else anchor + text)
    open(path, "w", encoding="utf-8").write(src)
    print(f"updated {os.path.basename(path)}: "
          f"{sum(p[2] for p in pairs if p[2])} replacements, {len(inserts)} inserts")


# ------------------------------------------------------------------- RU pairs
RU_PAIRS = [
    ("144 аксиомы замкнуты, 0 sorry, 0 axiom", "170 аксиом замкнуты, 0 sorry, 0 axiom", 1),
    ("""**Слой формализации, доведённый до v5.0.** Один файл — `Trivortex.lean`, 4 915 строк —
выводит заново аналитическое ядро вихревой программы трёх тел внутри
[Lean 4](https://lean-lang.org) + [Mathlib](https://github.com/leanprover-community/mathlib):
теорема 3.1 (замкнутая лагранжева хореография), топологический интеграл Чаплыгина,
законы сохранения системы Кирхгоффа, равностороннее решение Лагранжа, полная теория
треугольника, линейная устойчивость и бифуркация при неравных циркуляциях —
**144 инструкции `#print axioms`, ноль `sorry`, ноль `axiom`**, каждый футпринт замкнут
ровно на `propext · Classical.choice · Quot.sound`.""",
     """**Слой формализации, доведённый до v7.0.** Один файл — `Trivortex.lean`, 6 589 строк —
выводит заново аналитическое ядро вихревой программы трёх тел внутри
[Lean 4](https://lean-lang.org) + [Mathlib](https://github.com/leanprover-community/mathlib):
теорема 3.1 (замкнутая лагранжева хореография), топологический интеграл Чаплыгина,
законы сохранения системы Кирхгоффа, равностороннее решение Лагранжа, полная теория
треугольника, линейная устойчивость, бифуркация при неравных циркуляциях, нелинейная
устойчивость по Ляпунову через H/I и завершённая коллинеарная бифуркация —
**170 инструкций `#print axioms`, ноль `sorry`, ноль `axiom`**, каждый футпринт замкнут
ровно на `propext · Classical.choice · Quot.sound`.""", 1),
    ("%23print%20axioms-144%20замкнуто", "%23print%20axioms-170%20замкнуто", 1),
    ("[![Status](https://img.shields.io/badge/статус-завершено%20v5.0%20(%C2%A71%E2%80%93%C2%A79)-gold?style=for-the-badge&label=Релиз)](#11-шкала-времени--v11--v50)",
     "[![Status](https://img.shields.io/badge/статус-завершено%20v7.0%20(%C2%A71%E2%80%93%C2%A710.3)-gold?style=for-the-badge&label=Релиз)](#11-шкала-времени--v11--v70)", 1),
    ("артефакт-4%2C915%20строк", "артефакт-6%2C589%20строк", 1),
    ("теоремы-243-", "теоремы-309-", 1),
    ("определения%20%2B%20структуры-55%20%2B%202-", "определения%20%2B%20структуры-58%20%2B%202-", 1),
    ("веха-M1%20%2B%20треки%20M4%2FM5-", "веха-M1%20%2B%20треки%20M4%2FM5%20%2B%20%C2%A710-", 1),
    ("6. [Глубокое погружение — секция за секцией (§1–§9)](#6-глубокое-погружение--секция-за-секцией-19)",
     "6. [Глубокое погружение — секция за секцией (§1–§10)](#6-глубокое-погружение--секция-за-секцией-110)", 1),
    ("11. [Шкала времени — v1.1 → v5.0](#11-шкала-времени--v11--v50)",
     "11. [Шкала времени — v1.1 → v7.0](#11-шкала-времени--v11--v70)", 1),
    ("| **Артефакт** | [`Trivortex.lean`](Trivortex.lean) — 4 915 строк, один namespace, один файл |",
     "| **Артефакт** | [`Trivortex.lean`](Trivortex.lean) — 6 589 строк, один namespace, один файл |", 1),
    ("| **Секции** | §1–§9 (+ два блока футпринта аксиом) — см. [погружение](#6-глубокое-погружение--секция-за-секцией-19) |",
     "| **Секции** | §1–§10.3 (+ три блока футпринта аксиом) — см. [погружение](#6-глубокое-погружение--секция-за-секцией-110) |", 1),
    ("| **Декларации** | 243 теоремы/леммы (144 публичных + 99 `private`-помощников) · 55 определений · 2 структуры |",
     "| **Декларации** | 309 теорем/лемм (170 публичных + 139 `private`-помощников) · 58 определений · 2 структуры |", 1),
    ("| **Машинная замкнутость** | **144 инструкции `#print axioms` — все замкнуты**",
     "| **Машинная замкнутость** | **170 инструкций `#print axioms` — все замкнуты**", 1),
    ("| **Статус** | ✅ **завершено — v5.0** (слой утверждений §1–§9; M1 + треки углубления M4/M5) |",
     "| **Статус** | ✅ **завершено — v7.0** (§1–§10.3; M1 + треки углубления M4/M5 + трек §10 устойчивость/бифуркация) |", 1),
    ("### 5.3 Из чего сделаны 4 915 строк", "### 5.3 Из чего сделаны 6 589 строк", 1),
    ('    "§9 продолжение/бифуркация" : 1379\n',
     '    "§9 продолжение/бифуркация" : 1380\n    "§10 Ляпунов/бифуркация" : 1698\n', 1),
    ("а §7–§9 (больше половины файла) — треки углубления v3.0–v5.0.",
     "а §7–§10 (больше половины файла) — треки углубления v3.0–v7.0.", 1),
    ("## 6. Глубокое погружение — секция за секцией (§1–§9)",
     "## 6. Глубокое погружение — секция за секцией (§1–§10)", 1),
    ("""Каждое несущее утверждение заканчивается в двух футпринт-блоках артефакта
(строки 3373–3494 для §1–§8, строки 4874–4913 для §9). Контракт, который они
навязывают:""",
     """Каждое несущее утверждение заканчивается в одном из трёх футпринт-блоков
артефакта (строки 3389–3510 для §1–§8, строки 6519–6559 для §9, строки 6560–6589
для §10). Контракт, который они навязывают:""", 1),
    ("144 / 144  #print axioms statements closed   ·   0 sorry   ·   0 axiom",
     "170 / 170  #print axioms statements closed   ·   0 sorry   ·   0 axiom", 1),
    ("| [`Trivortex.lean`](Trivortex.lean) | 4 915 | 243 КБ | артефакт: §1–§9 + футпринт аксиом (см. [§6](#6-глубокое-погружение--секция-за-секцией-19)) |",
     "| [`Trivortex.lean`](Trivortex.lean) | 6 589 | 331 КБ | артефакт: §1–§10.3 + футпринт аксиом (см. [§6](#6-глубокое-погружение--секция-за-секцией-110)) |", 1),
    ("| [`README_RU.md`](README_RU.md) | — | — | тот же обзор на русском |",
     """| [`README_RU.md`](README_RU.md) | — | — | тот же обзор на русском |
| [`docs/STATEMENTS.md`](docs/STATEMENTS.md) | авто | 24 КБ | авто-индекс всех 170 теорем по секциям (регенерация: `python3 ../notes/make_statement_index.py`) |""", 1),
    ('D{"проверка футпринта<br/>#print axioms × 144"}', 'D{"проверка футпринта<br/>#print axioms × 170"}', 1),
    ("| Артефакт | [`Trivortex.lean`](Trivortex.lean) — §1–§9, 144 инструкции `#print axioms` |",
     "| Артефакт | [`Trivortex.lean`](Trivortex.lean) — §1–§10.3, 170 инструкций `#print axioms` |", 1),
    ("| Веха | M1 + треки углубления M4/M5 (сохранение + Лагранж + устойчивость + бифуркация) |",
     "| Веха | M1 + треки углубления §7–§10 (теория треугольника + устойчивость + бифуркация + Ляпунов) |", 1),
    ("## 11. Шкала времени — v1.1 → v5.0", "## 11. Шкала времени — v1.1 → v7.0", 1),
    ("    v5.0 : Раздел 9 — нелинейное продолжение : семейство с произвольными циркуляциями s9_rel_eq : точное сохранение мод : бифуркация при Π = 0 с явными экземплярами\n",
     """    v5.0 : Раздел 9 — нелинейное продолжение : семейство с произвольными циркуляциями s9_rel_eq : точное сохранение мод : бифуркация при Π = 0 с явными экземплярами
    v6.0 : Раздел 10 — устойчивость по Ляпунову через H/I : коэрцитивный сертификат Γ²/(12π) : критичность энергия–Казимир : коллинеарная вилка при γ = −5/4
    v7.0 : §10.3 — бифуркация завершена : тройной корень вилки : вырожденные γ = −1, −2 : второе рациональное асимметричное РЭ (1, −9/5, −16/5) · ω = 25/(168π)
""", 1),
    ("| v5.0 | §9 | нелинейное продолжение + бифуркация | неустойчивость поперёк `Π = 0`, доказана |",
     """| v5.0 | §9 | нелинейное продолжение + бифуркация | неустойчивость поперёк `Π = 0`, доказана |
| v6.0 | §10.1–§10.2 | нелинейная устойчивость по Ляпунову + коллинеарная бифуркация | коэрцитивный сертификат, критичность энергия–Казимир, вилка, асимметричное РЭ |
| v7.0 | §10.3 | картина бифуркации завершена | тройной корень, вырожденные циркуляции, оба рациональных асимметричных РЭ |""", 1),
    ("**`Trivortex.lean` — §1–§9, 144 аксиом закрыто**", "**`Trivortex.lean` — §1–§10.3, 170 аксиом закрыто**", 1),
    ("числовые зеркала §8/§9 и проверка тождеств", "числовые зеркала §8/§9/§10 и проверка тождеств", 1),
    ("✔ **144 закрытых футпринта**", "✔ **170 закрытых футпринтов**", 1),
    ("✔ **доказано (§8–§9)**", "✔ **доказано (§8–§10)**", 1),
    ("[`assets/bifurcation_window.gif`](assets/bifurcation_window.gif) (§9),",
     """[`assets/bifurcation_window.gif`](assets/bifurcation_window.gif) (§9),
[`assets/lyapunov_stability.gif`](assets/lyapunov_stability.gif) (§10.1),
[`assets/collinear_bifurcation.gif`](assets/collinear_bifurcation.gif) (§10.2–10.3),""", 1),
    ("Здесь каждая из 144\nнапечатанных инструкций показывает только",
     "Здесь каждая из 170\nнапечатанных инструкций показывает только", 1),
    ("поэтому ценз насчитывает 144 футпринта на 243 теоремы плюс определения.",
     "поэтому ценз насчитывает 170 футпринтов на 309 теорем плюс определения.", 1),
    ("""- **M6 — расширение.** V5 — регулярное вихревое кольцо `N = 7` приземляется
  сначала в Python, затем минимум в двух портах; если возьмёт Lean-порт —
  ждите §10.""",
     """- **M6 — расширение.** V5 — регулярное вихревое кольцо `N = 7` приземляется
  сначала в Python, затем минимум в двух портах. Слот §10 занят: v6.0–v7.0
  принесли устойчивость по Ляпунову через H/I и завершённую коллинеарную
  бифуркацию; следующий кандидат на расширение — кольцо V5 `N = 7` — ждите §11.
  Две открытые теоретические цели из scope-заметок §10: теорема возмущений
  Крандалла–Рабиновица для асимметричной ветви за пределами γ₀ = −1/4 и
  ляпуновская устойчивость общего γ при неравных циркуляциях.""", 1),
    ("**Full declaration census** — 243 theorems/lemmas (144 public + 99 `private` helpers) + 57 definitions/structures. Names are verbatim Lean identifiers.",
     "**Full declaration census** — 309 theorems/lemmas (170 public + 139 `private` helpers) + 60 definitions/structures. Names are verbatim Lean identifiers.", 1),
    ("<summary><b>Axiom footprint (§1–§8 prints)</b> — lines 3373–4915: 39 theorems/lemmas, 11 defs · <i>click to expand</i></summary>",
     "<summary><b>Section 9 — nonlinear continuation and bifurcation (§9)</b> — lines 3511–4890: 39 theorems/lemmas, 11 defs · <i>click to expand</i></summary>", 1),
]

RU_INSERTS = [
    ("\n---\n\n## 7. Футпринт аксиом — ничего, кроме классических оснований",
     S610_RU, "before"),
    ('    D -->|"любая утечка"| F["красная · порт заблокирован"]\n```\n',
     '''
**Добавление v7.0 — отдельный workflow `lean-verify.yml`** (`.github/workflows/`):
тот же закреплённый билд автономно — elan из `lean-toolchain`, `lake exe cache
get`, `lake build`, затем охрана футпринта: каждый напечатанный футпринт обязан
равняться `[propext, Classical.choice, Quot.sound]`, и любой `sorryAx` валит прогон.
''', "after"),
    ("<!--CENSUS-END-->", S10_CENSUS_EN, "before"),
]

# EN pie: add the §10 slice (the mermaid pie lives in §5 "Architecture in pictures")
EN_PAIRS.append(('    "§9 continuation/bifurcation" : 1379\n',
                 '    "§9 continuation/bifurcation" : 1380\n    "§10 Lyapunov/bifurcation" : 1698\n', 1))

if __name__ == "__main__":
    apply(os.path.join(LEAN, "README.md"), EN_PAIRS, EN_INSERTS)
    apply(os.path.join(LEAN, "README_RU.md"), RU_PAIRS, RU_INSERTS)
    print("README sync to v7.0 complete")


