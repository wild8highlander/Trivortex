# cycloring — the Gamma-period ring package

The importable heart of the mini-research: eight modules that carry the
five theorems, the W-ladder and the figure factory. This file is the
compact API reference; the narrative lives in the
[mini-research README](../../README.md), the mathematical detail in the
monographs under [`docs/`](../../docs/).

## The dependency lattice

```text
periods ──► chain ──► ring ──► dynamics ──► ladder ──► runner
                                        └──► figures
```

Strictly acyclic, zero parent-framework imports at runtime, two runtime
dependencies (`numpy`, `mpmath`) and one optional (`matplotlib`, figures
only). Import cost is negligible; every module is importable standalone.

## `periods.py` — the Gamma-period core

Everything the chain consumes, computed at 50 working digits.

| function | signature | what it returns |
|----------|-----------|-----------------|
| `omega_mp` / `omega` | `(a, b, n)` | the level period $\Omega_{a,b} = \Gamma(a/N)\Gamma(b/N)/\Gamma((a+b)/N)$, mpmath / float64 |
| `normalized_p_mp` / `normalized_p` | `(a, b, n)` | the normalized diagonal sum $P(a,b)$ |
| `reflection_residual_mp` | `(a, n)` | the residual of $\Omega_{a,N-a} - \pi/\sin(\pi a/N)$ |
| `boundary_periods_mp` | `(n)` | the full boundary table: rows `(a, period, closed_form, residual)` |
| `sine_product_residual_mp` | `(n)` | the residual of $\prod_m 2\sin(\pi m/N) = N$ |
| `period_witness_mp` / `period_witness` | `(n)` | the combined transcendental witness of the level |
| `boundary_period`, `omega_11` | `(a, n)`, `(n)` | float64 convenience wrappers |
| `level_periods` | `(n, a_max=None)` | the dictionary of all periods up to `a_max` |
| `reflection_residual_float` | `(a, n)` | the float64 reflection residual |

## `chain.py` — the defect chain and the transducer

| function | signature | what it returns |
|----------|-----------|-----------------|
| `base_frequency` | `(n, gamma, big_r)` | $\omega_L = \Gamma(N-1)/(4\pi R^2)$ |
| `angular_impulse` | `(n, gamma, big_r)` | $B = N\Gamma R_0^2$ |
| `stiffness_index` | `(n, gamma, big_r)` | the defect count $k = \lceil B\lambda_0/\Gamma^2 \rceil$ |
| `defect_chain` | `(n, gamma, big_r)` | the full chain dictionary: $\delta$, $k$, $\gamma$, $\delta_{eff}$, $W_N$, $\Delta_{Ch}$ |
| `transducer` | `(delta_ch)` | the triple $(\varepsilon, \nu/\omega_L, C_N)$ |
| `inverse_transducer` | `(eps)` | the round trip $\Delta_{Ch}(\varepsilon)$ |
| `level_table` | `(levels, gamma)` | the registered table of §4 of the README |

## `ring.py` — the root system and the breathing program

| function | signature | what it returns |
|----------|-----------|-----------------|
| `polygon_positions` / `polygon_positions_xy` | `(n, big_r, theta0)` | the frozen regular N-gon (complex / xy) |
| `master_sigma` | `(big_r, nu, t, n)` | the binomial right side $\sigma(t)$ |
| `frozen_rate` | `(n, gamma, big_r)` | the frozen rotation rate $\lambda_0$ |
| `adiabatic_invariant` | `(n, gamma)` | the frozen angular invariant |
| `root_system_residual` | `(zs, n_probes)` | the max residual of $z_k^N = \sigma$ over probes |
| `moment_sums` | `(zs, m_max)` | the power sums $S_m$ |
| `impulse` | `(zs, gamma)` | the complex linear impulse $P + iQ$ |
| `character_amplitudes` | `(zs)` | the character-lattice decomposition of the shape |
| `pumped_radius` / `pumped_positions` / `pumped_positions_xy` | `(t, ...)` | the breathing program at time $t$ |
| `synchronous_frequency` | `(big_r, eps, gamma, n)` | the synchronous $\nu = \omega_L(1-\varepsilon^2)^{-3/2}$ |
| `closure_time`, `transport_phase`, `closure_residual` | `(…)` | the rosette-closure registers of Theorem 4 |
| `mean_transport_ratio` | `(eps)` | the quadrature mean $\langle(1+\varepsilon\cos u)^{-2}\rangle$ |
| `rosette_curve` | `(k, n, big_r, eps, nu, t_max)` | the sampled rosette of vortex `k` |

## `dynamics.py` — the Kirchhoff layer

| function | signature | what it returns |
|----------|-----------|-----------------|
| `vortex_rhs` | `(state, gamma_vec)` | the Kirchhoff right-hand side |
| `rk4_step` / `integrate` | `(state, gamma_vec, dt, …)` | the RK4 stepper and the fixed-step integrator |
| `invariants` | `(state, gamma_vec)` | the dictionary `H, P, Q, I` of the vortex integrals |
| `relative_drifts` | `(inv0, inv1)` | the relative drifts between two invariant snapshots |
| `jacobian` | `(state, gamma_vec)` | the stability Jacobian of the configuration |
| `hamiltonian_closed_form` | `(n, big_r, gamma)` | the Theorem-5 shell $H(R)$ |
| `distance_product` / `discriminant_binomial` | `(…)` | the algebraic registers of Theorem 5 |
| `hamiltonian_measured` | `(state, gamma_vec)` | the direct pairwise Hamiltonian |

## `ladder.py` — the registered checks

Seven `check_w*` functions, one per stage, each returning a JSON-serializable
dictionary with `passed`, the recorded residuals and the full parameter
snapshot. The tolerance bands are module constants registered before the
runs; `run_stage(stage, preset_name)` and `run_all(preset_name)` apply the
preset scalers (`quick` / `default` / `full`) and return the protocol
payloads the runner persists.

## `runner.py` — the JSON protocol CLI

`write_protocol(stage, preset, result)` writes
`results/protocols/W{n}_<slug>_<preset>.json`; `main()` implements
`--stage W# --preset name` (single stage) and `--preset name` (whole
ladder). Deterministic output: no wall-clock fields inside the numbers.

## `figures.py` — the bilingual figure factory

`main(proto_dir, out_dir, langs)` generates the language editions:
`en` → `figures/`, `ru` → `figures/ru/`. CLI:
`--lang both|en|ru` (default `both`), `--proto-dir`, `--out-dir`. Every
panel reads its registers from the committed protocols — the figures are
pictures *of* the runs, never independent computations.

## Versioning and stability

The package version is the mini-research version (1.0.0,
[`CHANGELOG.md`](../../CHANGELOG.md)). Public API = the functions listed
above; everything starting with `_` is internal and may change without
notice between minor versions.
