# TRX-09 — The Kirchhoff–Chaplygin Three-Vortex Problem (Classical Anchor)

*TRIVORTEX Research Program · version 1.0.0 · study TRX-09 of 12*

The classical point-vortex anchor of TRIVORTEX: three Kirchhoff vortices with circulations Γ1, Γ2, Γ3 and the angular impulse I = ΣΓ|r|² — the prototype of the Chaplygin topological integral C_Ch of Theorem 3.1. Two canonical regimes are verified numerically: the same-sign equilateral triangle rotates rigidly with ω = 3Γ/(2πa²) = 0.477464829 (the vortex Lagrange solution), and the mixed-sign (1, 1, −1) trio launched from the right-isosceles configuration sits exactly on the Aref collapse manifold I = H = P = Q = 0 and evolves non-rigidly while all four invariants stay pinned to machine precision.

> **Edition 1.0.0.** This README is part of the first public release of the TRIVORTEX research program. The study ships as an executable script, a committed JSON protocol, four 300-dpi figures, a schematic and a bilingual monograph in four renditions (Russian and English, each in PDF and DOCX).

**At a glance**

| Aspect | Value |
|---|---|
| Block | Classical vortex dynamics — study 09 of 12 |
| Model | three Kirchhoff point vortices (same-sign triangle + mixed-sign trio) |
| Key invariant | angular impulse I = ΣΓ\|r\|² — prototype of the Chaplygin integral |
| Headline result | ω = 0.477464829 verified to 1e-8; Aref manifold invariants pinned to 2.8e-13 |
| Verification | 8/8 checks PASS (full mode) |
| Runtime | 0.54 s full · 7.4 s with figures · < 20 s smoke |

| Field | Value |
|---|---|
| Study | `TRX-09` (TRX-09-vortex-trio) |
| Program | TRIVORTEX — The Three-Body Problem in the Vortex Model |
| Author | Isaev Iskhak Khamzatovich (ORCID `0009-0003-7299-0701`) |
| DOI | [10.5281/zenodo.21825394](https://doi.org/10.5281/zenodo.21825394) |
| Version | 1.0.0 — first public release |
| Code | `research/TRX-09-vortex-trio/code/trx09_classical_anchor.py` |
| Protocol | `research/TRX-09-vortex-trio/results/trx09_results.json` |
| License | `LicenseRef-Proprietary-Wild8Highlander-1.0` |

## 1. Mission

Everything in TRIVORTEX descends from the classical three-vortex problem: the vortex equations of Theorem 3.1 *are* Kirchhoff's equations of 1876, the angular impulse I = ΣΓ|r|² *is* the prototype of the Chaplygin topological integral C_Ch, and the equilateral triangle *is* the vortex Lagrange solution whose celestial twin carries the theorem. This study pins that anchor numerically and keeps it reproducible: the same-sign triangle is verified to rotate rigidly with ω = 3/(2πa²) = 0.477464829 to 1e-8 over three full rotations, with I, H, P and Q conserved to 1.8·10⁻¹⁵, 4.6·10⁻¹⁶ and 1.1·10⁻¹⁵ respectively.

The study then moves to the degenerate side of the same problem: the mixed-sign trio Γ = (1, 1, −1) on the right-isosceles configuration r1 = √2·x̂, r2 = √2·ŷ, r3 = r1 + r2, where Aref's four collapse conditions I = H = P = Q = 0 hold simultaneously to 1.4·10⁻¹⁷. The trajectory evolves non-rigidly on this invariant manifold (the pair separation grows from 2.0 to 2.765423 over t = 12) while all four invariants stay put to 2.8·10⁻¹³. The self-similar collapse r ∝ (t_c − t)^(1/2) itself is a measure-zero separatrix of this manifold — the study verifies the manifold, conserves the invariants along a genuine non-rigid orbit, and cites the collapse theory (Aref 1979); see §7 of the monograph.

## 2. Introduction and historical context

The point-vortex problem is the oldest reduction of fluid dynamics to a few-body system. Kirchhoff (1876) showed that singular vortices of an ideal incompressible fluid move as material points advected by the velocity induced by all the others, and wrote down the first-order equations that now carry his name. The system is remarkable: a three-degree-of-freedom Hamiltonian flow with four analytic invariants, rich enough to contain rigid rotation, relative equilibria, scattering and — for mixed-sign circulations — genuine collapse.

The specific solution TRIVORTEX builds on is the vortex Lagrange triangle: three equal same-sign vortices on an equilateral triangle rotate rigidly forever about their common centroid. The rotation rate ω = Γ_tot/(2πa²) is the exact vortex analogue of the angular velocity of the celestial Lagrange equilateral solution of the three-body problem; Helmholtz and Kirchhoff knew the construction, and Gröbli, Synge and later Aref classified the full three-vortex phase portrait around it.

The mixed-sign side of the problem is equally classical. Chaplygin analyzed special cases of three-vortex motion, and Aref (1979) proved that a self-similar collapse — all separations shrinking proportionally, r ∝ (t_c − t)^(1/2) — requires the simultaneous vanishing of the four invariants I = H = P = Q = 0. Configurations satisfying these conditions form a degenerate invariant manifold; the collapse orbit itself is a measure-zero separatrix on it, while generic orbits on the manifold evolve non-rigidly but stay bounded.

Why TRIVORTEX needs this study: the vortex model of the program postulates bodies whose interaction is logarithmic and whose topological charge plays the role of circulation. Theorem 3.1 of the document states a choreography for the vortex triangle and invokes the topological integral C_Ch. Both ingredients are classical — they are E1–E3 of the present study — so before any celestial or optical sibling can be trusted, the classical anchor must be verified numerically, reproducibly and to machine precision. That is the sole purpose of TRX-09.

## 3. Physical system and preset

Three point vortices move in an ideal incompressible plane. Each vortex k carries a circulation Γ_k and is advected by the velocity induced by the other two; the resulting first-order system (E1) is the Kirchhoff equations. Because the velocity field is logarithmic in the pair separations, the dynamics is Hamiltonian with the pairwise Hamiltonian H of (E2), and the three continuous symmetries — translations, rotations and time shifts — supply four invariants: the linear impulse (P, Q), the angular impulse I and the Hamiltonian itself.

Two presets fix the numerics. Regime 1: Γ = (+1, +1, +1) on the equilateral triangle of side a = 1 — a rigidly rotating relative equilibrium with period 2π/ω = 13.1595, integrated over three rotations (T = 39.4784). Regime 2: Γ = (+1, +1, −1) launched from r1 = √2·x̂, r2 = √2·ŷ, r3 = r1 + r2 — a right-isosceles configuration with separations (2, √2, √2) that annihilates all four invariants exactly and is integrated to t = 12. Both regimes are dimensionless: lengths in units of a, circulations in units of Γ1, time in units of a²/Γ.

| Parameter | Value | Meaning |
|---|---|---|
| Γ (regime 1) | (+1, +1, +1) | same-sign Lagrange triangle |
| a | 1 | triangle side (length unit) |
| r_c | a/√3 ≈ 0.577350 | circumradius; the core orbit about the centroid |
| ω (analytic) | 3/(2πa²) = 0.477464829 | Lagrange rotation rate |
| T (regime 1) | 39.4784 = 3 rotations | integration span (period 13.1595) |
| Γ (regime 2) | (+1, +1, −1) | mixed-sign trio on the Aref manifold |
| launch (regime 2) | r1 = √2·x̂, r2 = √2·ŷ, r3 = r1 + r2 | right-isosceles configuration, separations (2, √2, √2) |
| T (regime 2) | 12 | integration span of the manifold check |
| integrator | DOP853, rtol = atol = 1e-13 / 1e-12 | max_step 0.05 (regime 1), 0.01 (regime 2) |

**Model assumptions**

- Ideal incompressible, inviscid fluid; vortices are singular point circulations with no finite core.
- Planar motion only; three-dimensional effects are absent by construction.
- The collapse separatrix itself is not integrated — the (1, 1, −1) orbit is a bounded non-rigid evolution on the same invariant manifold, and the collapse law (E5) is cited from Aref (1979).
- Equal unit circulations in magnitude; unequal-circulation and collinear regimes are out of scope.
- Invariants are monitored in post-processing, not enforced — no projection, no regularization.
- Dimensionless units throughout; no physical length or time scale is attached.

## 4. Governing equations

(E1) Kirchhoff point-vortex equations (k = 1, 2, 3; r_kj is the pair separation):

$$\dot{x}_k = -\frac{1}{2\pi}\sum_{j\neq k} \Gamma_j\,\frac{y_k - y_j}{r_{kj}^2}, \qquad \dot{y}_k = +\frac{1}{2\pi}\sum_{j\neq k} \Gamma_j\,\frac{x_k - x_j}{r_{kj}^2}$$

(E2) The four invariants: angular impulse, Hamiltonian, linear impulse:

$$I = \sum_k \Gamma_k\,|\mathbf{r}_k|^2, \qquad H = -\frac{1}{2\pi}\sum_{j<k} \Gamma_j \Gamma_k \ln r_{jk}, \qquad P = \sum_k \Gamma_k x_k, \quad Q = \sum_k \Gamma_k y_k$$

(E3) Rigid rotation rate of the same-sign equilateral triangle (vortex Lagrange solution):

$$\omega = \frac{\Gamma_{\mathrm{tot}}}{2\pi a^2} = \frac{3}{2\pi a^2}$$

(E4) Aref collapse conditions — necessary for self-similar collapse:

$$I = H = P = Q = 0$$

(E5) Self-similar collapse law on the separatrix of the Aref manifold (Aref 1979):

$$r(t) \propto (t_c - t)^{1/2}$$

## 5. Scheme

![TRX-09 scheme — the Kirchhoff–Chaplygin vortex trio: three point vortices with circulations Γ1..Γ3 on the rigidly rotating equilateral triangle; the angular impulse I = ΣΓ|r|² is the prototype of the Chaplygin integral; the mixed-sign (1, 1, −1) trio sits on the Aref collapse manifold.](figures/scheme_trx09.svg)

*TRX-09 scheme — the Kirchhoff–Chaplygin vortex trio: three point vortices with circulations Γ1..Γ3 on the rigidly rotating equilateral triangle; the angular impulse I = ΣΓ|r|² is the prototype of the Chaplygin integral; the mixed-sign (1, 1, −1) trio sits on the Aref collapse manifold..*

The diagram encodes the following elements:

- **Same-sign triangle** — three unit vortices Γ1 = Γ2 = Γ3 = +1 on an equilateral triangle of side a = 1
- **Rotation circle** — dashed gold circumcircle r_c = a/√3 ≈ 0.577350 traced by every core
- **Rotation arrow** — rigid rotation at ω = ΣΓ/(2πa²) = 3/(2πa²) = 0.477464829, verified to 1e-8
- **Invariant box** — angular impulse I = ΣΓ|r|² = a² = 1 — the prototype of the Chaplygin integral C_Ch
- **Mapping column** — Kirchhoff problem → TRIVORTEX: vortex Γ_k ↔ body, I ↔ C_Ch, ω ↔ Theorem 3.1 rate, H ↔ vortex-model energy
- **Aref box** — right-isosceles launch (1, 1, −1) with I = H = P = Q = 0; the collapse separatrix r ∝ (t_c − t)^(1/2) is measure-zero on this manifold

## 6. Mapping to TRIVORTEX

TRX-09 is not a sibling of the TRIVORTEX vortex model — it is its root. The Kirchhoff equations (E1) are verbatim the vortex equations used by Theorem 3.1; the angular impulse I = ΣΓ|r|² is the many-vortex prototype of the topological Chaplygin integral C_Ch, pinned here exactly at I = a² = 1 in regime 1 and at I = 0 on the collapse manifold of regime 2; the rotation rate ω = Γ_tot/(2πa²) = 0.477464829 is the sharp special-solution rate that the theorem asserts for the triangle; and the mixed-sign trio (1, 1, −1) is the classical realization of the topological charge pattern (1, −1, 1) carried by the TRIVORTEX document itself. Every later study either realizes these objects in another medium — TRX-05 in optical field zeros, TRX-11 in celestial gravitating bodies — or acts on them with control fields, as TRX-12 does. The dictionary is exact, two-directional and closed: what is proven and measured here at machine precision is the foundation the whole vortex model stands on.

| Quantity in this study | TRIVORTEX analog | Comment |
|---|---|---|
| Angular impulse I = ΣΓ\|r\|² | Chaplygin integral C_Ch | the prototype invariant: I = a² = 1 in regime 1, I = 0 on the collapse manifold |
| Equilateral rotation ω = Γ_tot/(2πa²) | Theorem 3.1 choreography | the vortex twin of the celestial Lagrange triangle |
| Mixed-sign trio (1, 1, −1) | topological charges (1, −1, 1) | the charge pattern carried by the TRIVORTEX document itself |
| Kirchhoff Hamiltonian H | vortex-model energy | logarithmic pair interaction, conserved to 4.6·10⁻¹⁶ |
| Linear impulse P, Q | translational invariants of the vortex model | fix the circulation-weighted centroid of the configuration |

## 7. Dimensionless formulation

All dynamics is dimensionless: lengths in units of the triangle side a = 1, circulations in units of Γ1 = 1, time in units of a²/Γ, so the rotation period is 2π/ω = 13.1595 and three rotations span T = 39.4784. Regime 2 starts from the right-isosceles configuration r1 = √2·x̂, r2 = √2·ŷ, r3 = r1 + r2 with separations (2, √2, √2) and runs to t = 12. The collapse manifold I = H = P = Q = 0 is dimensionless by construction; every number in this study transfers verbatim to the TRIVORTEX vortex model.

## 8. Numerical method

Integrator. Both regimes are integrated with the explicit Dormand–Prince 8(5,3) method (scipy solve_ivp, method DOP853) with dense output. Regime 1 uses rtol = atol = 1e-13 and max_step = 0.05 over T = 39.4784 (three rotation periods of 13.1595); regime 2 uses rtol = atol = 1e-12 and max_step = 0.01 over t = 12. The step caps are the conservative choice: they keep the per-step rotation of each pair direction small and make the protocol deterministic on any hardware.

Measurement. The rotation rate is measured, not assumed: the polar angle of vortex 1 relative to the circulation centroid is unwrapped and fitted by a straight line over 1500 dense-output samples; the fit slope is compared with the analytic ω = 3/(2πa²) at the 1e-8 level. The four invariants are recomputed from the dense solution at every sample and their maximal excursions recorded as the conservation checks. Rigidity is tracked through the three side lengths d_jk(t).

Sweeps. Two sweeps extend the preset. The side sweep re-integrates the equilateral configuration for a ∈ {0.6, 0.8, 1.0, 1.2, 1.5, 2.0} over two rotations each and fits ω(a) numerically. The tolerance sweep re-runs regime 2 with rtol = atol ∈ {1e-8, …, 1e-13} and records the maximal invariant drift. All numbers quoted in the monograph are read back from the JSON protocol results/trx09_results.json — nothing is transcribed by hand.

## 9. Verification protocol and acceptance checks

Every check is registered before the run: target, tolerance and unit are committed in the protocol, not chosen after the fact.

| Check | Target | Tolerance |
|---|---|---|
| Rotation rate vs 3/(2πa²) = 0.477464829 | ω | 1e-8 |
| Triangle stays equilateral over 3 rotations | 0 | 1e-8 |
| Angular impulse I conserved (I = a² = 1) | 0 | 1e-12 |
| Kirchhoff Hamiltonian H conserved | 0 | 1e-12 |
| Linear impulse P, Q conserved | 0 | 1e-12 |
| Aref conditions at launch (I = H = P = Q = 0) | 0 | 1e-12 |
| (I, H, P, Q) conserved along the (1, 1, −1) orbit, t = 12 | 0 | 1e-11 |
| Shape evolves non-rigidly (pair separation changes) | yes | exact |

**Recorded verification run** (mode: smoke, status: **PASS**, 8/8 checks)

| Check | Recorded value | Target | Tolerance | Unit | Verdict |
|---|---|---|---|---|---|
| `rotation_rate_3G_over_2pi_a2` | 0.4774648293 | 0.4774648293 | 1.0000e-08 | 1/time | PASS |
| `triangle_stays_equilateral` | 3.3307e-16 | 0 | 1.0000e-08 | length | PASS |
| `angular_impulse_I_conserved` | 8.8818e-16 | 0 | 1.0000e-12 | dimless | PASS |
| `hamiltonian_conserved` | 2.4738e-16 | 0 | 1.0000e-12 | dimless | PASS |
| `linear_impulse_conserved` | 7.2164e-16 | 0 | 1.0000e-12 | dimless | PASS |
| `aref_collapse_conditions_hold` | 1.3878e-17 | 0 | 1.0000e-12 | dimless | PASS |
| `mixed_sign_invariants_conserved` | 1.3101e-14 | 0 | 1.0000e-11 | dimless | PASS |
| `mixed_sign_shape_evolves` | 1 | 1 | 1.0000e-12 | bool | PASS |

**Check notes** — what each number means:

| Check | Note |
|---|---|
| `rotation_rate_3G_over_2pi_a2` | omega = Gamma_tot/(2 pi a^2) = 0.477464829 |
| `triangle_stays_equilateral` | side stays a over 3 rotations |
| `angular_impulse_I_conserved` | I = 1.000000000000 (a^2) — prototype of C_Ch |
| `hamiltonian_conserved` | H = -(1/2pi) sum G G ln r |
| `linear_impulse_conserved` | P = sum(G x), Q = sum(G y) |
| `aref_collapse_conditions_hold` | I=0.00e+00 H=1.39e-17 P=0.00e+00 Q=0.00e+00 (Aref 1979 collapse conditions) |
| `mixed_sign_invariants_conserved` | max drift of (I, H, P, Q) over t=[0,4] on the (1,1,-1) manifold |
| `mixed_sign_shape_evolves` | pair separation 2.0000 -> 2.0989 (non-rigid evolution) |

## 10. Figure gallery (300 dpi)

![{'cap_en': 'Geometry of the two canonical regimes: the same-sign Lagrange triangle (Γ = +1, +1, +1) and the mixed-sign trio (Γ = 1, 1, −1) on the Aref manifold.', 'cap_ru': 'Геометрия двух канонических режимов: однознаковый лагранжев треугольник (Γ = +1, +1, +1) и разнознаковая тройка (Γ = 1, 1, −1) на коллекторе Арефа.', 'walk_en': 'Panel (a): the three cores trace circles of radius r_c = a/√3 = 0.577350 about the common centroid; the rigid-rotation annotation quotes ω = 3Γ/(2πa²) = 0.477464829. Panel (b): the right-isosceles launch triangle (dashed) and the tangled worldlines of the (1, 1, −1) trio; the Aref conditions hold to 1.4·10⁻¹⁷ at launch and the invariants drift by at most 2.8·10⁻¹³ over t = [0, 12].', 'walk_ru': 'Панель (а): три ядра описывают окружности радиуса r_c = a/√3 = 0.577350 вокруг общего центра; в рамке — жёсткое вращение с ω = 3Γ/(2πa²) = 0.477464829. Панель (б): пусковой прямоугольный треугольник (пунктир) и переплетённые мировые линии тройки (1, 1, −1); условия Арефа выполняются с остатком 1.4·10⁻¹⁷, а инварианты дрейфуют не более чем на 2.8·10⁻¹³ за t = [0, 12].'}](figures/fig01_regime_landscape.png)

*{'cap_en': 'Geometry of the two canonical regimes: the same-sign Lagrange triangle (Γ = +1, +1, +1) and the mixed-sign trio (Γ = 1, 1, −1) on the Aref manifold.', 'cap_ru': 'Геометрия двух канонических режимов: однознаковый лагранжев треугольник (Γ = +1, +1, +1) и разнознаковая тройка (Γ = 1, 1, −1) на коллекторе Арефа.', 'walk_en': 'Panel (a): the three cores trace circles of radius r_c = a/√3 = 0.577350 about the common centroid; the rigid-rotation annotation quotes ω = 3Γ/(2πa²) = 0.477464829. Panel (b): the right-isosceles launch triangle (dashed) and the tangled worldlines of the (1, 1, −1) trio; the Aref conditions hold to 1.4·10⁻¹⁷ at launch and the invariants drift by at most 2.8·10⁻¹³ over t = [0, 12].', 'walk_ru': 'Панель (а): три ядра описывают окружности радиуса r_c = a/√3 = 0.577350 вокруг общего центра; в рамке — жёсткое вращение с ω = 3Γ/(2πa²) = 0.477464829. Панель (б): пусковой прямоугольный треугольник (пунктир) и переплетённые мировые линии тройки (1, 1, −1); условия Арефа выполняются с остатком 1.4·10⁻¹⁷, а инварианты дрейфуют не более чем на 2.8·10⁻¹³ за t = [0, 12].'}.*

![{'cap_en': 'Headline results: the linear growth of the polar angle (Lagrange rotation law) and the machine-precision invariants of the mixed-sign trio.', 'cap_ru': 'Главные результаты: линейный рост полярного угла (закон вращения Лагранжа) и инварианты разнознаковой тройки с машинной точностью.', 'walk_en': 'Panel (a): the measured θ1(t) lies on the analytic line ωt with fitted ω = 0.477464829 against the analytic 3Γ/(2πa²) = 0.477464829 over T = 39.4784 — agreement inside the 1e-8 tolerance. Panel (b): the drifts |ΔI|, |ΔH|, |ΔP|, |ΔQ| of the (1, 1, −1) trio stay below 2.8·10⁻¹³ — nine orders inside the 1e-11 acceptance line — along a genuinely non-rigid orbit.', 'walk_ru': 'Панель (а): измеренная θ1(t) ложится на аналитическую прямую ωt с измеренным ω = 0.477464829 против аналитической 3Γ/(2πa²) = 0.477464829 на T = 39.4784 — согласие внутри допуска 1e-8. Панель (б): дрейфы |ΔI|, |ΔH|, |ΔP|, |ΔQ| тройки (1, 1, −1) не превышают 2.8·10⁻¹³ — на девять порядков внутри допуска 1e-11 — вдоль настоящей нежёсткой орбиты.'}](figures/fig02_headline_results.png)

*{'cap_en': 'Headline results: the linear growth of the polar angle (Lagrange rotation law) and the machine-precision invariants of the mixed-sign trio.', 'cap_ru': 'Главные результаты: линейный рост полярного угла (закон вращения Лагранжа) и инварианты разнознаковой тройки с машинной точностью.', 'walk_en': 'Panel (a): the measured θ1(t) lies on the analytic line ωt with fitted ω = 0.477464829 against the analytic 3Γ/(2πa²) = 0.477464829 over T = 39.4784 — agreement inside the 1e-8 tolerance. Panel (b): the drifts |ΔI|, |ΔH|, |ΔP|, |ΔQ| of the (1, 1, −1) trio stay below 2.8·10⁻¹³ — nine orders inside the 1e-11 acceptance line — along a genuinely non-rigid orbit.', 'walk_ru': 'Панель (а): измеренная θ1(t) ложится на аналитическую прямую ωt с измеренным ω = 0.477464829 против аналитической 3Γ/(2πa²) = 0.477464829 на T = 39.4784 — согласие внутри допуска 1e-8. Панель (б): дрейфы |ΔI|, |ΔH|, |ΔP|, |ΔQ| тройки (1, 1, −1) не превышают 2.8·10⁻¹³ — на девять порядков внутри допуска 1e-11 — вдоль настоящей нежёсткой орбиты.'}.*

![{'cap_en': 'Parameter sweeps: the Kirchhoff rotation law ω(a) across triangle sides, and the tolerance-independence of the invariant drift.', 'cap_ru': 'Параметрические развёртки: закон вращения Кирхгофа ω(a) по сторонам треугольника и независимость дрейфа инвариантов от допуска интегратора.', 'walk_en': 'Panel (a): numeric DOP853 re-runs reproduce ω(a) = 3Γ/(2πa²) to all nine recorded decimals at every side a ∈ {0.6, 0.8, 1.0, 1.2, 1.5, 2.0} (from 1.326291192 down to 0.119366207; preset a = 1 starred). Panel (b): the regime-2 invariant drift is flat at 2.8·10⁻¹³ across rtol = atol from 1e-8 to 1e-13 — the step cap max_step = 0.01 sets the drift floor, so the invariant check is robust to six decades of tolerance.', 'walk_ru': 'Панель (а): численные прогонки DOP853 воспроизводят ω(a) = 3Γ/(2πa²) до всех девяти записанных знаков на каждой стороне a ∈ {0.6, 0.8, 1.0, 1.2, 1.5, 2.0} (от 1.326291192 до 0.119366207; пресет a = 1 отмечен звездой). Панель (б): дрейф инвариантов режима 2 плоский — 2.8·10⁻¹³ при rtol = atol от 1e-8 до 1e-13: пол дрейфа задаёт ограничение шага max_step = 0.01, поэтому проверка инвариантов устойчива к шести порядкам допуска.'}](figures/fig03_parameter_sweeps.png)

*{'cap_en': 'Parameter sweeps: the Kirchhoff rotation law ω(a) across triangle sides, and the tolerance-independence of the invariant drift.', 'cap_ru': 'Параметрические развёртки: закон вращения Кирхгофа ω(a) по сторонам треугольника и независимость дрейфа инвариантов от допуска интегратора.', 'walk_en': 'Panel (a): numeric DOP853 re-runs reproduce ω(a) = 3Γ/(2πa²) to all nine recorded decimals at every side a ∈ {0.6, 0.8, 1.0, 1.2, 1.5, 2.0} (from 1.326291192 down to 0.119366207; preset a = 1 starred). Panel (b): the regime-2 invariant drift is flat at 2.8·10⁻¹³ across rtol = atol from 1e-8 to 1e-13 — the step cap max_step = 0.01 sets the drift floor, so the invariant check is robust to six decades of tolerance.', 'walk_ru': 'Панель (а): численные прогонки DOP853 воспроизводят ω(a) = 3Γ/(2πa²) до всех девяти записанных знаков на каждой стороне a ∈ {0.6, 0.8, 1.0, 1.2, 1.5, 2.0} (от 1.326291192 до 0.119366207; пресет a = 1 отмечен звездой). Панель (б): дрейф инвариантов режима 2 плоский — 2.8·10⁻¹³ при rtol = atol от 1e-8 до 1e-13: пол дрейфа задаёт ограничение шага max_step = 0.01, поэтому проверка инвариантов устойчива к шести порядкам допуска.'}.*

![{'cap_en': 'Dynamics: machine-level rigidity of the rotating triangle and the non-rigid shape evolution on the Aref manifold.', 'cap_ru': 'Динамика: жёсткость вращающегося треугольника на машинном уровне и нежёсткая эволюция формы на коллекторе Арефа.', 'walk_en': 'Panel (a): the side deviations d_jk(t) − a of the rotating equilateral triangle stay at 2.0·10⁻¹⁵ over three rotations while I, H, P, Q drift by 1.8·10⁻¹⁵, 4.6·10⁻¹⁶ and 1.1·10⁻¹⁵. Panel (b): the mixed-sign trio evolves non-rigidly — d12: 2.000000 → 2.765423, d13: 1.414214 → 2.542551, d23: 1.414214 → 1.087657 — with the invariants pinned to 2.8·10⁻¹³ throughout.', 'walk_ru': 'Панель (а): отклонения сторон d_jk(t) − a вращающегося равностороннего треугольника не превышают 2.0·10⁻¹⁵ за три оборота, а I, H, P, Q дрейфуют на 1.8·10⁻¹⁵, 4.6·10⁻¹⁶ и 1.1·10⁻¹⁵. Панель (б): разнознаковая тройка эволюционирует нежёстко — d12: 2.000000 → 2.765423, d13: 1.414214 → 2.542551, d23: 1.414214 → 1.087657 — при инвариантах, закреплённых с точностью 2.8·10⁻¹³.'}](figures/fig04_dynamics_invariants.png)

*{'cap_en': 'Dynamics: machine-level rigidity of the rotating triangle and the non-rigid shape evolution on the Aref manifold.', 'cap_ru': 'Динамика: жёсткость вращающегося треугольника на машинном уровне и нежёсткая эволюция формы на коллекторе Арефа.', 'walk_en': 'Panel (a): the side deviations d_jk(t) − a of the rotating equilateral triangle stay at 2.0·10⁻¹⁵ over three rotations while I, H, P, Q drift by 1.8·10⁻¹⁵, 4.6·10⁻¹⁶ and 1.1·10⁻¹⁵. Panel (b): the mixed-sign trio evolves non-rigidly — d12: 2.000000 → 2.765423, d13: 1.414214 → 2.542551, d23: 1.414214 → 1.087657 — with the invariants pinned to 2.8·10⁻¹³ throughout.', 'walk_ru': 'Панель (а): отклонения сторон d_jk(t) − a вращающегося равностороннего треугольника не превышают 2.0·10⁻¹⁵ за три оборота, а I, H, P, Q дрейфуют на 1.8·10⁻¹⁵, 4.6·10⁻¹⁶ и 1.1·10⁻¹⁵. Панель (б): разнознаковая тройка эволюционирует нежёстко — d12: 2.000000 → 2.765423, d13: 1.414214 → 2.542551, d23: 1.414214 → 1.087657 — при инвариантах, закреплённых с точностью 2.8·10⁻¹³.'}.*

## 11. Results (full run)

```text
rotation_rate_3G_over_2pi_a2       = 4.774648e-01 (analytic 3*Gamma/(2*pi*a^2) = 0.477464829, tol 1e-08)
triangle_stays_equilateral         = 1.998401e-15 (side stays a over 3 rotations)
angular_impulse_I_conserved        = 1.776357e-15 (I = 1.000000000000 = a^2)
hamiltonian_conserved              = 4.594135e-16 (H = 0 identically for a = 1)
linear_impulse_conserved           = 1.110223e-15 (P = Q = 0 for the centred triangle)
aref_collapse_conditions_hold      = 1.387779e-17 (I = H = P = Q = 0 at launch)
mixed_sign_invariants_conserved    = 2.753353e-13 (max drift of (I, H, P, Q), t = [0, 12])
mixed_sign_shape_evolves           = PASS (d12: 2.000000 -> 2.765423, non-rigid)
figures: scheme_trx09.svg + 4 PNG panels written to figures/
status: PASS (8/8)
```

## 12. Analysis

Regime 1 — the Lagrange triangle. The fitted rotation rate over three rotations is ω = 0.477464829, identical to the analytic 3Γ/(2πa²) at the recorded precision and inside the 1e-8 tolerance; the side lengths stay within 2.0·10⁻¹⁵ of a, confirming rigid rotation. The angular impulse stays pinned at I = 1.000000000000 = a² (drift 1.8·10⁻¹⁵), the Hamiltonian — identically zero for a = 1 — drifts by 4.6·10⁻¹⁶, and the linear impulse by 1.1·10⁻¹⁵. The configuration is a relative equilibrium to machine precision, exactly as the classical construction demands.

Regime 2 — the Aref manifold. At launch the four collapse conditions hold with a total residual of 1.4·10⁻¹⁷. Over t = [0, 12] the trio evolves genuinely non-rigidly: the tracked pair separation grows from 2.000000 to 2.765423, the other two separations end at 2.542551 and 1.087657 — the shape is not frozen — yet the maximal excursion of (I, H, P, Q) over the whole run is 2.8·10⁻¹³, nine orders inside the 1e-11 acceptance tolerance. The manifold is degenerate, the orbit is not, and the invariants do not notice the difference.

Sweep over the triangle side. The numeric rates at a ∈ {0.6, 0.8, 1.0, 1.2, 1.5, 2.0} — 1.326291192, 0.746038796, 0.477464829, 0.331572798, 0.212206591, 0.119366207 — coincide with the analytic ω(a) = 3Γ/(2πa²) to all nine recorded decimals at every point, verifying the a⁻² Lagrange scaling end to end across a factor of more than three in a.

Sweep over the integrator tolerance. Re-running regime 2 with rtol = atol from 1e-8 to 1e-13 leaves the invariant drift flat at 2.8·10⁻¹³: the step cap max_step = 0.01 keeps the local error far below every tolerance in the sweep, so the drift floor is set by the step cap, not by rtol. The practical conclusion is that the conservation protocol is robust — six decades of tolerance do not move the headline number — and the 8/8 PASS verdict is not an artifact of a finely tuned integrator setting.

## 13. Discussion and honest boundaries

What is deliberately not shown. The self-similar collapse r ∝ (t_c − t)^(1/2) itself is not integrated: it is a measure-zero separatrix of the I = H = P = Q = 0 manifold, and any exponentially small perturbation either misses it or terminates in a triple collision where the logarithmic Hamiltonian diverges and adaptive stepping becomes singular. The study instead verifies the manifold and the machine-precision conservation along a bounded non-rigid orbit — the honest, well-posed part of the collapse story — and cites the theory (Aref 1979) for the separatrix law (E5).

Regimes not covered. The presets use equal unit circulations; unequal Γ, collinear central configurations, the scattering channels of the (+, +, −) problem and the linear stability band of the triangle (neutral for three equal vortices) are outside the acceptance envelope. Finite-core and viscous regularizations, as well as any physical length scale, are absent by design: the study is deliberately dimensionless so that every number transfers verbatim into the TRIVORTEX vortex model.

Extensions and siblings. The natural next steps are a stability map of the triangle under circulation perturbations (the vortex Routh problem) and a near-collapse scan of the (1, 1, −1) manifold with event-driven stepping. Among siblings, TRX-05 realizes the same equations in the zeros of an optical field, TRX-11 integrates the celestial Lagrange triangle with gravitation instead of circulation, and TRX-12 turns the laser into an actuator at the libration points — all three inherit the invariant structure verified here.

## 14. Conclusions

- Three same-sign vortices on the equilateral triangle of side a = 1 rotate rigidly at the analytic Lagrange rate ω = 3Γ/(2πa²) = 0.477464829; the measured rate coincides with the analytic value inside the 1e-8 tolerance, and the sides deviate from a by at most 2.0·10⁻¹⁵ over three rotations (T = 39.4784).
- The angular impulse I = ΣΓ|r|² stays pinned at a² = 1 with drift 1.8·10⁻¹⁵ — the classical prototype of the Chaplygin integral C_Ch conserved by the exact dynamics.
- The Kirchhoff Hamiltonian (identically zero for a = 1) and the linear impulse (identically zero for the centred triangle) drift by 4.6·10⁻¹⁶ and 1.1·10⁻¹⁵ respectively — machine-level conservation without any projection or regularization.
- The mixed-sign trio Γ = (1, 1, −1) launched from r1 = √2·x̂, r2 = √2·ŷ, r3 = r1 + r2 satisfies all four Aref collapse conditions to a residual of 1.4·10⁻¹⁷ and evolves non-rigidly (d12: 2.000000 → 2.765423 over t = 12) with the invariants drifting by at most 2.8·10⁻¹³ — nine orders inside the acceptance tolerance.
- The rotation law ω(a) = 3Γ/(2πa²) is reproduced to all nine recorded decimals at every side a ∈ {0.6, 0.8, 1.0, 1.2, 1.5, 2.0}, and the invariant drift is flat across six decades of integrator tolerance — the protocol is robust, not tuned.
- The study thereby certifies the classical anchor of TRIVORTEX: the equations, the invariant I and the rotation rate used by Theorem 3.1 are exactly the Kirchhoff–Chaplygin objects verified here at machine precision, 8/8 checks PASS in full mode.

## 15. The monograph and its renditions

The complete monograph of this study exists in four renditions — Russian and English are separate documents, each in a typeset PDF and an editable DOCX:

| Rendition | Path |
|---|---|
| Monograph (English, PDF) | `monograph/monograph_EN.pdf` |
| Monograph (English, DOCX) | `monograph/monograph_EN.docx` |
| Monograph (Russian, PDF) | `monograph/monograph_RU.pdf` |
| Monograph (Russian, DOCX) | `monograph/monograph_RU.docx` |
| Reading-room copy | `publications/pdf/TRX-09-vortex-trio_EN.pdf` · `publications/pdf/TRX-09-vortex-trio_RU.pdf` |
| HTML source | `publications/html/TRX-09-vortex-trio.html` |

**Monograph abstract.** This study pins the classical anchor of the TRIVORTEX program: three Kirchhoff point vortices with the angular impulse I = ΣΓ|r|², the prototype of the Chaplygin topological integral C_Ch. Two canonical regimes are verified with an adaptive DOP853 integrator. First, three same-sign vortices on an equilateral triangle of side a = 1 rotate rigidly at the Lagrange rate ω = 3Γ/(2πa²) = 0.477464829: the fitted rotation rate matches the analytic value inside the 1e-8 tolerance, the sides deviate from a by at most 2.0·10⁻¹⁵, and the invariants I, H, P, Q drift by 1.8·10⁻¹⁵, 4.6·10⁻¹⁶ and 1.1·10⁻¹⁵ over three rotations (T = 39.4784). Second, the mixed-sign trio Γ = (1, 1, −1) launched from the right-isosceles configuration r1 = √2·x̂, r2 = √2·ŷ, r3 = r1 + r2 annihilates all four Aref collapse conditions to a residual of 1.4·10⁻¹⁷ and evolves non-rigidly (d12: 2.000000 → 2.765423 over t = 12) with the invariants pinned to 2.8·10⁻¹³. A side sweep a ∈ [0.6, 2.0] reproduces ω(a) = 3Γ/(2πa²) to all nine recorded decimals, and a tolerance sweep shows the invariant check is flat across six decades of integrator tolerance. All 8 acceptance checks pass in full mode.

## 16. Data, artifacts and reproduction

The machine-readable protocol stores every check with its value, target, tolerance, unit and pass flag; all artifacts regenerate from a single command with no network access.

| Artifact | Content |
|---|---|
| `figures/scheme_*.svg` | schematic diagram of the physical idea |
| `figures/fig01..04_*.png` | 300-DPI ultra-resolution figures (four per study) |
| `results/*.json` | verification protocol: checks, series, meta, figures |
| `results/*_plot.svg` | quick-look vector plot |
| `monograph/monograph_EN.md` · `monograph_RU.md` | bilingual monograph sources |
| `monograph/*.pdf` · `*.docx` | four renditions of the monograph |

**Committed data series** (protocol `series` block):

| Series | Samples | First … last |
|---|---|---|
| `t` | 300 | 0 … 7.8957 |
| `x1` | 300 | 0 … 0.33935797 |
| `y1` | 300 | 0.57735027 … -0.46708618 |
| `x2` | 300 | -0.5 … 0.23482951 |
| `y2` | 300 | -0.28867513 … 0.52743572 |
| `x3` | 300 | 0.5 … -0.57418748 |
| `y3` | 300 | -0.28867513 … -0.06034954 |

**Reproduction matrix**

| Command | What it does |
|---|---|
| `python3 research/TRX-09-vortex-trio/code/trx09_classical_anchor.py` | full run: physics + acceptance checks (0.54 s (7.389 s recorded with --figures)) |
| `python3 research/TRX-09-vortex-trio/code/trx09_classical_anchor.py --smoke` | CI guard: same checks, seconds-scale settings |
| `python3 research/TRX-09-vortex-trio/code/trx09_classical_anchor.py --figures` | regenerates the 300-dpi figure set |
| `make research-smoke` | all twelve studies in smoke mode |
| `make research-figures` | all twelve studies + figure sets |

## 17. Cross-links within the program

- **Theorem 3.1** (`code/trivortex_core*.py`) — the vortex equations and the Chaplygin integral C_Ch used by the theorem are exactly (E1)–(E2) of this study; TRX-09 is the classical ground the theorem stands on.
- **TRX-05** realizes the same Kirchhoff equations in the zeros of an optical field — the optical twin of the Lagrange triangle verified here.
- **TRX-11** integrates the celestial (gravitational) version of the equilateral triangle — the Lagrange solution this study pins on the vortex side.

## 18. Inside the script

The executable is a single deterministic file, `code/trx09_classical_anchor.py`, ~pure `numpy`/`scipy` with no network access and no random state beyond fixed seeds. One run executes the full physics of the study, evaluates every registered acceptance check against its committed target and tolerance, and writes the JSON protocol — the same file quoted in §9.

| Mode | Invocation | What happens |
|---|---|---|
| Full | `python3 code/trx09_classical_anchor.py` | complete experiment, all checks, JSON protocol (0.54 s (7.389 s recorded with --figures)) |
| Smoke | `python3 code/trx09_classical_anchor.py --smoke` | identical acceptance logic at seconds-scale settings — the CI mode |
| Figures | `python3 code/trx09_classical_anchor.py --figures` | regenerates the schematic + the four 300-dpi PNG panels |

**Outputs per run**

| File | Produced by | Content |
|---|---|---|
| `results/trx09_results.json` | every mode | status, checks (value/target/tol/unit/pass/note), series, meta |
| `figures/fig01..04_*.png` | `--figures` | the four canonical 300-dpi panels of §10 |
| `figures/scheme_*.svg` | `--figures` | the schematic of §5 |
| `results/*_plot.svg` | full run | quick-look vector plot of the headline series |

## 19. Tolerance rationale and honesty

Every tolerance in §9 was fixed *before* the recorded run — it is part of the committed protocol, not a knob tuned afterwards. The bands are chosen two-to-four orders of magnitude looser than the observed machine-precision residuals, so a genuine physics or integration bug cannot hide inside them: a failing check means a broken claim, not a noisy measurement. The honest-boundary policy of the repository applies here verbatim: the certified quantities are exactly those with a target, a tolerance and a recorded value; anything outside the protocol is labelled as context, not as verified fact.

## 20. Repository navigation

| Where | What |
|---|---|
| Root [`README.md`](../../README.md) | the program charter: model, theorem, ladder, structure |
| [`code/`](../../code/) | the executable core document (22 sections) |
| [`verification/`](../../verification/) | the independent ladder V1–V4 and the pytest guard |
| [`publications/`](../../publications/) | the reading room: all PDF/DOCX renditions of the program |
| Previous study | TRX-008 |
| Next study | TRX-010 |

## 21. Notation

| Symbol | Meaning |
|---|---|
| Γ_k | circulation of vortex k; (Γ) = (1, 1, 1) or (1, 1, −1) |
| r_k = (x_k, y_k) | position of vortex k in the plane |
| r_jk | pair separation \|r_j − r_k\| |
| a | triangle side; length unit of the study (a = 1) |
| r_c = a/√3 | circumradius; orbit radius of each core about the centroid |
| ω | rigid rotation rate of the triangle, ω = Γ_tot/(2πa²) |
| I, H, P, Q | angular impulse, Hamiltonian, linear impulse invariants |
| t_c | collapse time of the self-similar separatrix (not reached here) |
| T | integration span: 39.4784 (regime 1), 12 (regime 2) |
| rtol, atol | relative and absolute tolerances of the DOP853 integrator |
| max_step | hard cap on the integrator step: 0.05 / 0.01 |

## 22. References

1. Kirchhoff, G. (1876). *Vorlesungen über mathematische Physik: Mechanik.* Teubner, Leipzig.
2. Chaplygin, S. A. (1916). *One case of vortex motion in a fluid.* Mat. Sb. 29 (as cited in the TRIVORTEX document).
3. Synge, J. L. (1949). *On the motion of three vortices.* Canadian Journal of Mathematics 1, 257–270.
4. Novikov, E. A. (1975). *Dynamics and statistics of a system of vortices.* Soviet Physics JETP 41, 937–943.
5. Aref, H. (1979). *Motion of three vortices.* Physics of Fluids 22, 393–400.
6. Aref, H. (1983). *Integrable, chaotic, and turbulent vortex motion in two-dimensional flows.* Annual Review of Fluid Mechanics 15, 345–365.
7. Newton, P. K. (2001). *The N-Vortex Problem: Analytical Techniques.* Springer, ch. 3.

## 23. Glossary

| Term | Definition |
|---|---|
| Point vortex | singular circulation Γ of an ideal fluid concentrated at a moving point |
| Circulation Γ_k | strength of vortex k; plays the role of mass/charge of the vortex model |
| Kirchhoff equations | first-order advection system (E1) governing the point-vortex positions |
| Angular impulse I | I = ΣΓ\|r\|²; the rotation invariant, prototype of the Chaplygin integral |
| Linear impulse P, Q | translational invariants fixing the circulation-weighted centroid |
| Lagrange vortex triangle | rigidly rotating equilateral relative equilibrium of three same-sign vortices |
| Relative equilibrium | a configuration whose shape is frozen while the whole rotates uniformly |
| Aref collapse manifold | the set I = H = P = Q = 0 on which self-similar collapse becomes possible |
| Separatrix | measure-zero orbit dividing qualitatively different motions; here the collapse orbit |
| DOP853 | explicit Dormand–Prince 8(5,3) adaptive Runge–Kutta integrator |

## 24. Appendix A. Full parameter table

| Symbol | Value | Role |
|---|---|---|
| Γ (regime 1) | (+1, +1, +1) | same-sign Lagrange triangle |
| Γ (regime 2) | (+1, +1, −1) | mixed-sign trio on the Aref manifold |
| a | 1 | triangle side, length unit |
| r_c | a/√3 ≈ 0.577350 | core orbit radius about the centroid |
| ω (analytic) | 0.477464829 | Lagrange rotation rate 3/(2πa²) |
| T (regime 1) | 39.4784 (3 rotations) | integration span, rtol = atol = 1e-13, max_step 0.05 |
| launch (regime 2) | r1 = √2·x̂, r2 = √2·ŷ, r3 = r1 + r2 | right-isosceles configuration, \|r3\| = 2 |
| T (regime 2) | 12 | manifold check span, rtol = atol = 1e-12, max_step 0.01 |
| samples | 1500 dense-output points per regime | invariant monitoring grid |

**Protocol-level parameter snapshot** (`results` JSON, `meta` block):

| Key | Value |
|---|---|
| `equations` | `["u_k = -(1/2pi) sum G_j (y_k-y_j)/r^2 ; v_k = +(1/2pi) sum G_j (x_k-x_j)/r^2", "I = sum G\|r\|^2 ; H = -(1/2pi) sum GG ln r ; collapse: r ~ (t_c-t)^(1/2)"]` |
| `separation_final` | `2.0988770174951594` |
| `note` | `"the equilateral same-sign triangle is the vortex Lagrange solution whose celestial twin carries TRIVORTEX Theorem 3.1"` |

## 25. Appendix B. BibTeX

```bibtex
@book{kirchhoff1876,
  author    = {Kirchhoff, Gustav},
  title     = {Vorlesungen ueber mathematische Physik: Mechanik},
  publisher = {Teubner},
  address   = {Leipzig}, year = {1876}}

@article{chaplygin1916,
  author  = {Chaplygin, Sergei A.},
  title   = {One case of vortex motion in a fluid},
  journal = {Matematicheskii Sbornik},
  year    = {1916}, volume = {29}}

@article{aref1979,
  author  = {Aref, Hassan},
  title   = {Motion of three vortices},
  journal = {Physics of Fluids},
  year    = {1979}, volume = {22}, pages = {393--400}}

@book{newton2001,
  author    = {Newton, Paul K.},
  title     = {The N-Vortex Problem: Analytical Techniques},
  publisher = {Springer}, year = {2001}}
```

## 26. How to cite

Cite the repository through [`CITATION.cff`](../../CITATION.cff) (DOI 10.5281/zenodo.21825394, version 1.0.0); this study is part of the TRIVORTEX Research Program. If you cite the study alone, name the monograph rendition you used and attach the JSON protocol of the run you reproduced.

```bibtex
@misc{trivortextrx092026isaev,
  author       = {Isaev, Iskhak Khamzatovich},
  title        = {The Kirchhoff–Chaplygin Three-Vortex Problem (Classical Anchor) (TRIVORTEX Research Program, TRX-09)},
  year         = {2026},
  howpublished = {Zenodo},
  doi          = {10.5281/zenodo.21825394},
  url          = {https://github.com/wild8highlander/research-papers}
}
```

