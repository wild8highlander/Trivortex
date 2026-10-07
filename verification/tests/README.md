# TRIVORTEX — Test Suite

> Pytest coverage for the verification ladder of the three-body vortex
> model. **28 tests, all passing.** Every test is bound to either a hard
> analytic reference value (Theorem 3.1, Lagrange angular velocity) or a
> numerical residual produced by a real RK4 run — no mocked numbers, no
> skipped physics.

---

## Table of contents

1. [Quick start](#1-quick-start)
2. [What is covered](#2-what-is-covered)
3. [Test map](#3-test-map)
4. [Tolerance philosophy](#4-tolerance-philosophy)
5. [Writing new tests](#5-writing-new-tests)
6. [CI integration](#6-ci-integration)

---

## 1. Quick start

From the repository root:

```bash
python -m pip install numpy pytest
python -m pytest verification/tests/ -v
```

Expected tail of a healthy run:

```text
verification/tests/test_trivortex.py::TestReportGeneration::test_json_report_serializes PASSED
============================== 13 passed in ~2s ==============================
```

The suite needs only `numpy` and `pytest` — no LaTeX, no provers, no
Docker. The heavy cross-language matrix is intentionally kept out of this
suite; see [`verification/README.md`](../README.md) for the language
roadmap.

---

## 2. What is covered

The suite guards three layers of the TRIVORTEX document against regressions:

| Layer | Guarded property | Typical residual |
|---|---|---|
| **Analytic** | Closed form of Theorem 3.1: frequency `ω = (2π/T)·e^{C_Ch/π}`, amplitude `ε = 1/(e^{C_Ch/π}−1)`, periodicity of `r_k(t)`, shape of the Chaplygin combination | `≤ 1e-12` (float64 exactness) |
| **Numerical core** | Kirchhoff right-hand side: antisymmetry, rotation sense, zero radial drift for the rigid pair | `≤ 1e-15` |
| **Ladder V1–V4** | Choreography 2π/3, periodicity, rigid Lagrange rotation with `ω = 3Γ/(2πa²)`, conservation of `H, P, Q, I` (equal and unequal circulations) | `≤ 1e-10` |

The ladder tests run the same code paths as
[`verification/trivortex/python/verify.py`](../trivortex/python/verify.py)
but with the fast `quick` preset, so the full suite finishes in about two
seconds — cheap enough to run on every push, which is exactly what the
[`trivortex-ci.yml`](../../.github/workflows/ci.yml) workflow does.

---

## 3. Test map

```text
test_trivortex.py
├── TestTheorem31                      ← analytic layer, hard references
│   ├── test_frequency_reference_value       ω = 1.3748022274393588 (C_Ch=1)
│   ├── test_amplitude_reference_value       ε = 1/(e^{1/π}−1)
│   ├── test_amplitude_small_cch_guard       the C_Ch ≤ 0.01 guard
│   ├── test_closed_form_periodicity         r_k(t+T_r) = r_k(t)
│   └── test_chaplygin_formula_shape         C_Ch = r²θ̇ − q·r (A_θ = 1/r)
├── TestLagrangeSolution               ← classical results, pinned
│   ├── test_analytic_omega_reference        ω = 3Γ/(2πa²)
│   ├── test_equilateral_initial_shape       sides = (a, a, a)
│   └── test_vortex_rhs_rigid_rotation_of_pair   Kirchhoff pair, exact
├── TestVerificationLadder             ← V1–V4 in the quick preset
│   ├── test_v1_choreography
│   ├── test_v2_lagrange_rotation
│   ├── test_v3_invariants
│   └── test_v4_robustness
└── TestReportGeneration
    └── test_json_report_serializes          JSON protocol round-trip
```

---

## 4. Tolerance philosophy

Tolerances in this suite are **not** tuned to make tests pass; they encode
what float64 arithmetic can honestly deliver for each quantity class:

- **1e-15 / 1e-14** — algebraic identities evaluated in float64
  (antisymmetry of the right-hand side, reference constants);
- **1e-12** — closed-form residuals of Theorem 3.1 (argument reduction in
  `cos`, transcendental round-off);
- **1e-10** — RK4-integrated invariants over several rotation periods
  (fourth-order truncation at `dt = T/2000` dominates).

If a residual sits far *below* its tolerance band, the test is loosened —
a passing test that cannot fail is dead weight. If a residual ever creeps
*above* its band, that is treated as a regression of the model code, not
of the test.

---

## 5. Writing new tests

1. Import the ladder module through the existing
   `importlib` shim at the top of `test_trivortex.py` (it loads
   `verify.py` by path, so no package installation is needed).
2. Bound every new numerical assertion to a **named reference**: an exact
   analytic value, a docstring with the formula, or a JSON protocol from a
   recorded run.
3. Keep individual tests under ~5 s wall time; long integrations belong to
   the `full` preset of `verify.py`, not to the pytest suite.
4. Name tests after the property they protect
   (`test_<property>_<context>`), so a red test reads as a diagnosis.

Example — adding a conservation check for a new configuration:

```python
def test_invariants_survive_random_vortex_config(self):
    rng = np.random.default_rng(42)
    state = rng.normal(scale=0.5, size=8)          # 4 vortices
    gamma = rng.choice([1.0, -1.0], size=4)
    inv0 = tv.invariants(state, gamma)
    for _ in range(2000):
        state = tv.rk4_step(state, gamma, 1e-3)
    inv1 = tv.invariants(state, gamma)
    for key in inv0:
        assert abs(inv1[key] - inv0[key]) <= 1e-9, key
```

---

## 6. CI integration

The suite is the second job of the repository pipeline:

- **Workflow**: [`.github/workflows/trivortex-ci.yml`](../../.github/workflows/ci.yml)
- **Trigger**: every push to `main` and every pull request;
- **Matrix**: Python 3.10 / 3.11 / 3.12 on `ubuntu-latest`;
- **Steps**: `pip install numpy pytest` → `pytest verification/tests/ -v`
  → `verify.py --preset quick` → upload of the JSON report artifact.

A green run produces the badge in the root README; a red run uploads the
failing JSON protocol so the regression can be diagnosed from the
artifact alone, without re-running anything locally.
