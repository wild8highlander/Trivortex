# PLANETVORTEX — the package API

The compact API reference of the nine modules. Signatures are quoted
from the source; `$`-math follows the parent repository's rendering
conventions. Package version = mini-repo version (**1.1.0**);
`_`-prefixed names are internal.

## classical.py — Layer P, the planetary registers

| function | signature | what it returns |
|----------|-----------|-----------------|
| `PLANETS` | `Tuple[Planet, ...]` | the committed NASA register: `name, gm, radius_km, a_au, e, period_days, gravity_ms2` |
| `solar_mass_ratio` | `(planet) -> float` | $m_i/M_\odot$ from GM |
| `mu_planet` | `(planet) -> float` | $\mu_i = 4\pi^2 (1 + m_i/M_\odot)$, AU³/yr² |
| `kepler_period_years` | `(planet) -> float` | $T = 2\pi\sqrt{a^3/\mu_i}$ — the two-body period |
| `kepler3_corrected` / `kepler3_uncorrected` | `(planet) -> float` | the $T^2/a^3$ registers with/without $(1 + m/M)$ |
| `kepler3_spread` | `(corrected=True) -> dict` | the worst pairwise spread + the offending pair |
| `schwarzschild_radius_m` | `(gm_si) -> float` | $r_s = 2\mathrm{GM}/c^2$, metres |
| `hill_radius_au` | `(planet) -> float` | $r_H = a (m/3M_\odot)^{1/3}$, AU |
| `gravity_ladder` | `() -> dict` | $\log_{10}(\mathrm{GM}_i/\mathrm{GM}_\oplus)$, all eight |
| `station_planets` | `() -> Tuple[Planet, ...]` | the seven wanderers in orbital order |
| `gravity_weights` | `() -> np.ndarray` | the mean-one circulation ladder for P7 |
| `osculating_a_e` | `(rx, ry, vx, vy, mu) -> (a, e)` | the planar vis-viva reduction |

## fano.py — Layer F, the structure and the exact figure

| function | signature | what it returns |
|----------|-----------|-----------------|
| `cyclic_line_triples` / `fano_lines` | `() -> list` | the seven lines $\{i, i+1, i+3\} \pmod 7$ |
| `line_of_pair` | `(i, j) -> tuple` | the unique line through two points |
| `incidence_matrix` | `() -> np.ndarray` | the 7×7 point-line incidence |
| `automorphism_group` | `() -> list` | PSL(2,7): the 168 line-preserving permutations of $\mathbb{Z}_7$ |
| `gl3_2` | `() -> list` | GL(3,2): the 168 invertible matrices over $\mathbb{F}_2$ |
| `find_isomorphism` | `() -> dict \| None` | the explicit line-preserving bijection $\mathbb{Z}_7 \to \mathbb{F}_2^3$ |
| `heptagon_coordinates` | `(big_r=1.0) -> np.ndarray` | the figure's vertices, station order |
| `chord_classes` | `(big_r=1.0) -> tuple` | $s_1, s_2, s_3 = 2R\sin(k\pi/7)$ |
| `line_triangle_geometry` | `(verts, big_r) -> dict` | sides / angles / area of one line-triangle |
| `exact_literals` | `(dps=40) -> dict` | the mpmath-pinned closed forms of Theorem A |
| `cell_hamiltonian` | `(gamma, big_r) -> float` | $-(\Gamma^2/2\pi)\ln(\sqrt{7} R^3)$ — every cell |
| `ring_hamiltonian` | `(gamma, big_r) -> float` | $7\,H_{cell}$ — the whole ring |
| `ring_omega` | `(gamma, big_r) -> float` | $\Gamma(N-1)/(4\pi R^2)$ at $N = 7$ |

## model.py — Layer V, the Kirchhoff lattice

| function | signature | what it returns |
|----------|-----------|-----------------|
| `vortex_rhs` | `(state, gamma) -> np.ndarray` | the vectorized Kirchhoff RHS, N vortices |
| `rk4_step` / `integrate` | `(state, gamma, dt, n)` | the classical RK4 flow |
| `invariants` | `(state, gamma) -> dict` | $H, P, Q, I$ |
| `relative_drifts` | `(inv0, inv1) -> dict` | the registered drift discipline |
| `jacobian` | `(state, gamma) -> np.ndarray` | the analytic $2N \times 2N$ Jacobian |
| `corotating_spectrum` | `(state, gamma, omega) -> np.ndarray` | the Havelock eigenvalues |
| `max_growth_rate` | `(state, gamma, omega) -> float` | $\max \mathrm{Re}\,\lambda$ |
| `ring_state` | `(big_r) -> np.ndarray` | the flat heptagon state |
| `unwrap_rotation` | `(state, R, T, dt, gamma) -> float` | the measured rotation rate |

## nbody.py — Layer N, the planetary simulation

| function | signature | what it returns |
|----------|-----------|-----------------|
| `planet_masses` | `() -> np.ndarray` | $[1, m_1, \ldots, m_8]$ in solar units |
| `initial_state` | `() -> np.ndarray` | the committed IC: perihelia aligned, momentum zero |
| `rhs` / `rk4_step` / `integrate` | `(state, masses, dt, …)` | the full Newtonian flow, all pairwise terms |
| `total_energy` / `total_angular_momentum` | `(state, masses) -> float` | the conservation registers |
| `osculating_elements` | `(state, k) -> (a, e)` | heliocentric osculating $(a, e)$ of planet $k$ |
| `perturbation_hierarchy` | `(state) -> dict` | $\max \sum_{j \ne i, \odot} a_j / a_\odot$ |

## ladder.py — the P1–P7 checks

| function | signature | what it returns |
|----------|-----------|-----------------|
| `TOLERANCES` | `dict` | the tolerance table, committed before the runs |
| `PRESETS` | `dict` | `quick` / `default` / `full` parameter snapshots |
| `check_p1_anchor` … `check_p7_bridge` | `(…) -> dict` | one registered statement per stage, JSON-serializable |
| `run_ladder` | `(preset="default") -> list` | the whole ladder |

## hardcore.py — the X1–X6 hardcore attacks

| function | signature | what it certifies |
|----------|-----------|-------------------|
| `gl2_7` / `sl2_7` / `psl_elements` | `() -> list` | the brute-force matrix models: 2016 / 336 / 168 |
| `check_x1_enumeration` | `() -> dict` | the orders, the 2-to-1 quotient, the centres, the class equation $1+21+42+56+24+24$, the simplicity certificate over all 32 unions |
| `check_x2_actions` | `() -> dict` | the 7-point action on one $S_4$ class (conjugate in $S_7$ to the research model), the 2-transitive 8-point action, the Sylow census $n_2=21$, $n_3=28$, $n_7=8$ |
| `check_x3_triangle` | `(dps=50) -> dict` | all 336 $(2,3,7)$ pairs generate; the Klein relations; the Hurwitz arithmetic; the Klein quartic smoothness certificate |
| `_hyperbolic_literals` | `(dps) -> dict` | the exact $\{7,3\}$ closed forms at dps digits |
| `check_x4_hyperbolic` | `(dps=50) -> dict` | the hyperbolic Pythagoras, the area ladder $\pi/42 \to \pi/3 \to 8\pi$, the combinatorial closure, the Poincaré-disk witness |
| `check_x5_integrator` | `(leap_grid, yosh_grid, …) -> dict` | the measured orders 2/4, the reversibility, the bounded energy without secular trend, the LRL/vis-viva/orbit registers |
| `check_x6_pn_perihelion` | `(n_orbits, steps_per_orbit, planets) -> dict` | the 1PN precession vs $6\pi\mathrm{GM}/(a(1-e^2)c^2)$; Mercury $42.982''$/century |
| `X_TOLERANCES` / `X_PRESETS` | `dict` | the committed tolerance table and the effort dials of the X-register |
| `run_hardcore` | `(preset="default") -> list` | the whole X-register |

## runner.py and figures.py

| entry | CLI | output |
|-------|-----|--------|
| `runner.main` | `--suite {p,x,all} --preset {quick,default,full} --stage {all,P1..P7,X1..X6} --out-dir` | `results/protocols/{stage}_{preset}.json` |
| `figures.main` | `--out --protocols` | `figures/fig01..fig05.png` + `scheme_planetvortex.svg` |

## Versioning and stability

Package version = mini-repo version (**1.1.0**). The protocol envelope
(`suite`, `version`, `stage`, `preset`, `date_utc`) is stable across
stages — the X protocols carry `suite = planetvortex-hardcore`; the
register names inside `check` are bound by the committed JSON files
and the test guard. `_`-prefixed helpers
(`_cell_rhs_batch`, `_shape_descriptor_batch`, `_two_body_period`,
`_mat_inv`, `_disk_witness`, …) are internal to the bench and may
move.
