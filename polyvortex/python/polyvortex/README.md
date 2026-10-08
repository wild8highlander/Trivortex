# polyvortex — the N-vortex extension bench package

The importable heart of the bench: seven modules carrying Layer K, Layer
G, the W-ladder and the figure factory. This file is the compact API
reference; the narrative lives in the [mini-repo
README](../../README.md), the mathematical detail in the monographs
under [`docs/`](../../docs/).

## The dependency lattice

```text
classical ──► model (Layer K) ──┐
            └► ansatz (Layer G) ─┴──► ladder ──► runner / figures
```

Zero parent-framework imports at runtime; one runtime dependency
(`numpy`), plus `mpmath` in the analytic registers and `matplotlib` for
the figures only.

## `model.py` — Layer K, the Kirchhoff dynamics

| function | signature | what it returns |
|----------|-----------|-----------------|
| `vortex_rhs` | `(state, gamma)` | the Kirchhoff right-hand side of the N-vortex system |
| `rk4_step` / `integrate` | `(state, gamma, dt, n_steps)` | the RK4 stepper and the fixed-step integrator |
| `invariants` | `(state, gamma)` | the dictionary `H, P, Q, I` of the vortex integrals |
| `relative_drifts` | `(inv0, inv1)` | the relative drifts between two invariant snapshots |
| `jacobian` | `(state, gamma)` | the stability Jacobian of the configuration |
| `corotating_spectrum` | `(state, gamma, omega)` | the eigenvalues in the co-rotating frame |
| `max_growth_rate` | `(state, gamma, omega)` | $\max\operatorname{Re}\lambda$ — the Havelock classifier input |

## `ansatz.py` — Layer G, the closed form

| function | signature | what it returns |
|----------|-----------|-----------------|
| `ansatz_frequency` | `(c_ch, t_period)` | the gauge frequency law $\omega = (2\pi/T)e^{C_{Ch}/\pi}$ |
| `ansatz_amplitude` | `(c_ch)` | the modulation amplitude $\varepsilon = 1/(e^{C_{Ch}/\pi}-1)$ |
| `is_admissible` | `(c_ch)` | the Theorem-B predicate: $C_{Ch} > \pi\ln 2$ |
| `ansatz_radius` / `ansatz_angle` | `(t, c_ch, t_period, k, n)` | the H1 shape at time $t$ for vortex `k` |
| `ansatz_state` / `ansatz_velocity` | `(t, c_ch, t_period, n)` | the full H1 configuration / its velocity field |
| `min_radius` | `(c_ch, t_period, k, n, n_grid)` | the polar minimum of the H1 radius on a 4096-point grid |
| `chaplygin_diagnostic` / `diagnostic_drift` | `(…)` | the window-dependent Section-6 diagnostic, no pass/fail role |

## `classical.py` — the N-gon registers

| function | signature | what it returns |
|----------|-----------|-----------------|
| `ngon_initial` | `(n, big_r, phase)` | the frozen regular N-gon initial state |
| `ngon_omega` | `(gamma, big_r, n)` | the analytic rate $\omega_N = \Gamma(N-1)/(4\pi R^2)$ |
| `chord_table` | `(n, big_r)` | the pairwise chord lengths (the pair-cancellation register) |
| `shape_deviation` | `(state, gamma, big_r)` | the max deviation of the integrated shape from the ideal polygon |
| `unwrap_angle_delta` | `(ang_start, ang_end, expected_total)` | the branch-safe angle unwrapping for the rotation register |
| `measured_rotation_rate` | `(…)` | the measured rotation rate from an integrated trajectory |

## `ladder.py` — the registered checks

Seven `check_w*` functions, one per stage, each returning a
JSON-serializable dictionary with `passed`, the recorded residuals and
the full parameter snapshot. Tolerance bands are module constants
registered before the runs; `run_ladder(preset)` applies the preset
scalers (`quick` / `default` / `full`) and returns the payloads the
runner persists.

## `runner.py` — the JSON protocol CLI

`save_protocol(stage, check, preset, out_dir)` writes
`results/protocols/W{n}_<slug>_<preset>.json`; `main()` implements
`--stage W# --preset name` (single stage) and `--preset name` (the whole
ladder). Deterministic numbers; the wall-clock stamp carries no role in
the values.

## `figures.py` — the figure factory

`main()` regenerates the four figures plus the scheme from the committed
protocols — the pictures quote the protocol numbers in their titles.
CLI: none needed (`make figures`); importable for custom runs.

## Versioning and stability

Package version = mini-repo version (1.1.0,
[`CHANGELOG.md`](../../CHANGELOG.md)). Public API = the functions listed
above; `_`-prefixed names are internal.
