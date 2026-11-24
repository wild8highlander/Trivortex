<!-- markdownlint-disable-file MD041 -->
<div align="center">

<img src="../docs/assets/banner_lab.svg" alt="lab/" width="100%"/>

# 🧪 lab — the Physics Core

</div>

> **Navigation:** [`verification`](../../README.md) › [`trivortex_master`](../README.md) › **`lab`**

<p align="center">
  <img src="https://img.shields.io/badge/modules-27-34D399?style=flat-square" alt="27 modules"/>
  <img src="https://img.shields.io/badge/LOC-~6.6k-34D399?style=flat-square" alt="6.6k LOC"/>
  <img src="https://img.shields.io/badge/presets-20-34D399?style=flat-square" alt="20 presets"/>
  <img src="https://img.shields.io/badge/tests-S5--S7%20%C2%B7%20S13--S20-34D399?style=flat-square" alt="tests"/>
  <img src="https://img.shields.io/badge/references-GR%20%C2%B7%20LLR%20%C2%B7%20Gillon%202017-FBBF24?style=flat-square" alt="references"/>
</p>

**lab/** is the physics core of the complex: bodies and scenes,
integrators from Newtonian RK4 to 6th-order Hamiltonian splits,
trajectory planners (including Theorem 3.1 of the Trivortex core),
20 presets, and a whole palette of "sciences": GR, chaos, tides,
radiation, CR3BP, spacecraft attitude control.

## 📂 Contents — What Lives Here

| File | Size | Description |
|---|---:|---|
| [`__init__.py`](__init__.py) | 0 B | package marker |
| [`body.py`](body.py) | 9,977 B | Scenes: bodies |
| [`scene.py`](scene.py) | 13,304 B | Scenes: the scene container |
| [`presets.py`](presets.py) | 15,451 B | Scenes: the 20 scene presets |
| [`units.py`](units.py) | 1,689 B | Scenes: units |
| [`grid_fields.py`](grid_fields.py) | 2,836 B | Scenes: grid fields |
| [`physics.py`](physics.py) | 19,446 B | Dynamics: `run_simulation`, the Newtonian engine |
| [`integrators.py`](integrators.py) | 16,138 B | Dynamics: integrators |
| [`engine_base.py`](engine_base.py) | 2,580 B | Dynamics: engine base + registration |
| [`nbody_tree.py`](nbody_tree.py) | 17,795 B | Dynamics: Barnes-Hut O(N log N) |
| [`hamiltonian_split.py`](hamiltonian_split.py) | 9,051 B | Dynamics: Hamiltonian splits of orders 2/4/6 |
| [`solar_system_sim.py`](solar_system_sim.py) | 9,523 B | Dynamics: the Solar System simulator |
| [`trajectory.py`](trajectory.py) | 25,976 B | Trajectories: planners incl. Theorem 3.1 |
| [`kepler.py`](kepler.py) | 17,410 B | Trajectories: Keplerian orbits |
| [`orbital_maneuvers.py`](orbital_maneuvers.py) | 10,342 B | Trajectories: maneuvers |
| [`choreography.py`](choreography.py) | 10,132 B | Trajectories: choreographies |
| [`relativity.py`](relativity.py) | 16,770 B | Special regimes: 1PN/2PN GR |
| [`chaos.py`](chaos.py) | 13,524 B | Special regimes: FLI and chaos diagnostics |
| [`collisions.py`](collisions.py) | 15,132 B | Special regimes: collisions |
| [`tides.py`](tides.py) | 12,908 B | Special regimes: tides |
| [`radiation.py`](radiation.py) | 12,386 B | Special regimes: radiation (Poynting-Robertson) |
| [`trojan_points.py`](trojan_points.py) | 5,534 B | Special regimes: Trojans, the Rabe criterion |
| [`halo_orbits.py`](halo_orbits.py) | 12,530 B | Special regimes: halo orbits L1–L5 |
| [`tissot.py`](tissot.py) | 7,806 B | Special regimes: Tissot indicatrix |
| [`resonances.py`](resonances.py) | 10,948 B | Special regimes: resonances |
| [`spacecraft.py`](spacecraft.py) | 20,791 B | Special regimes: quaternions/reaction wheels/PID |
| [`observables.py`](observables.py) | 1,935 B | Observables |

## Module map

```mermaid
mindmap
  root((lab/))
    Scenes
      body
      scene
      presets
      units
      grid_fields
    Dynamics
      physics
      integrators
      engine_base
      nbody_tree
      hamiltonian_split
      solar_system_sim
    Trajectories
      trajectory
      kepler
      orbital_maneuvers
      choreography
    Special regimes
      relativity
      chaos
      collisions
      tides
      radiation
      trojan_points
      halo_orbits
      tissot
      resonances
      spacecraft
    Observables
      observables
```

## Presets: real trajectories

<p align="center">
  <img src="../docs/assets/presets_gallery.png" alt="Presets: real RK4 runs" width="94%"/>
</p>

| Preset | N | Highlight |
|---|---|---|
| `inner_solar` | 5 | inner Solar System from the catalog |
| `figure_eight` | 3 | Chenciner-Montgomery choreography: E=-1.287142, closure 3.9e-08 |
| `lagrange_triangle` | 3 | rigid rotation, omega_L = 3*Gamma/(2*pi*a^2) (Lagrange 1772) |
| `vortex_ring_5` / `vortex_ring_7` | 5/7 | Kirchhoff vortex rings (7 is the last stable one) |
| `jupiter_system` / `saturn_system` | 6 | systems with moons from the catalog |
| `io_europa_ganymede` | 4 | the Laplace resonance 1:2:4 |
| `trappist_like` | 5 | Barnard's system from NASA TAP |
| `sun_all_planets` | 9 | unphysical preset: only with `allow_unphysical` |

## The Theorem 3.1 planner: admissibility (fixed in v2.0.1)

<p align="center">
  <img src="../docs/assets/theorem31_admissibility.png" alt="Theorem 3.1: admissibility" width="96%"/>
</p>

The closed form r_k(t) = sqrt(C_Ch)*(1+eps*cos(omega*t+2*pi*k/3)) is
non-degenerate for **C_Ch > pi*ln2 ~ 2.1776** (Theorem B of the
polyvortex monograph): eps < 1, radii positive, and the ring "breathes"
cleanly. At C_Ch = 1 (the core default, eps ~ 2.668) the curve is a
limacon with an inner loop: the body crosses the center and the
*geometric* 2*pi/3 separation breaks (the separation of the polar
angles theta_k holds always). Since v2.0.1 the planner records the
`admissible` flag in its metadata and test S9 checks both domains and
detects the threshold.

```python
from lab.trajectory import get_planner

planner = get_planner("analytic")
traj = planner.theorem31(C_Ch=3.14159, n_steps=500)
traj.metadata["omega"]       # 2.598... = e^(pi/pi)*(2*pi/T)
traj.metadata["admissible"]  # True: eps = 1/(e-1) ~ 0.582 < 1
```

<p align="center">
  <img src="../docs/assets/theorem31_ring.gif" alt="Breathing ring (C_Ch=pi)" width="44%"/>
  <img src="../docs/assets/figure_eight.gif" alt="figure-eight" width="44%"/>
</p>

The analytic core of this planner — the exact rotating equilateral
solution and the conservation of the vortex integrals — is proven in
Lean 4 ([`verification/lean4`](../../lean4/README.md), `lagrangeSol`
and the `P/Q/I/H_kirchhoff_*` theorems).

## Physics vs independent references

Every "science" module carries a `self_check()` against a literature
or observational reference — the quality gate (49/49) and tests
S13-S20 run them:

| Module | Reference | Result |
|---|---|---|
| [`relativity.py`](relativity.py) | Mercury 42.98"/century (GR) | 42.98"/century, Kerr ISCO, Lense-Thirring, Petersen |
| [`nbody_tree.py`](nbody_tree.py) | direct summation | error < 5%, O(N log N) speedup |
| [`chaos.py`](chaos.py) | Henon-Heiles | FLI: chaos 4.87 > regular 0.04 > oscillator -0.00 |
| [`tides.py`](tides.py) | LLR 3.82 cm/yr; Io 1e14 W; Kozai | 3.80 cm/yr; x1.56; 39.23 deg |
| [`radiation.py`](radiation.py) | Poynting-Robertson | t_PR(100 um, 1 AU) = 2.09e5 yr |
| [`collisions.py`](collisions.py) | conservation laws | momentum <= 1e-12, energy at eps=1 <= 1e-9 |
| [`halo_orbits.py`](halo_orbits.py) | NASA (Earth-Moon) | L1-L5 to the 6th digit |
| [`trojan_points.py`](trojan_points.py) | the Rabe criterion | 0.03852 |
| [`spacecraft.py`](spacecraft.py) | a 90-deg slew | 12 s, abs(H) <= 1.8e-16 |

<p align="center">
  <img src="../docs/assets/relativity_mercury.png" alt="Mercury 42.98&quot;/century" width="45%"/>
  <img src="../docs/assets/tides_moon.png" alt="Tides: Moon and Io" width="45%"/>
</p>

<p align="center">
  <img src="../docs/assets/chaos_fli.png" alt="FLI" width="46%"/>
  <img src="../docs/assets/poincare_sections.png" alt="Poincare sections" width="49%"/>
</p>

<p align="center">
  <img src="../docs/assets/barnes_hut.png" alt="Barnes-Hut" width="49%"/>
  <img src="../docs/assets/energy_conservation.png" alt="RK4 energy drift" width="45%"/>
</p>

## The Havelock limit: why N=8 is forbidden

<p align="center">
  <img src="../docs/assets/havelock_threshold.png" alt="Havelock threshold N<=7/N=8" width="92%"/>
</p>

A ring of N equal vortices is linearly stable for N <= 7 and unstable
from N >= 8 (Havelock 1893; the spectral twin is POLYVORTEX W4:
max Re lambda = +0.4502). A scan with 2% jitter: the N=8 ring
deformation is 0.285 against ~0.007 for the stable ones. That is why
`core/config.py` demands `allow_unphysical` for N=8 and refuses N>=9
(test S12).

## Quick start

```python
from core.config import from_profile
from lab.presets import build_preset
from lab.physics import run_simulation

sc = build_preset("inner_solar", from_profile("quick", n_steps=500))
summary = run_simulation(sc, n_steps=500)
print(sc.bodies[1].position, summary["t_final"])
```

Engines are injected via `register_engine` (REBOUND/Dedalus without an
import cycle lab<->realism — the S3 pattern, see
[realism/](../realism/README.md)).

## Related

- [core/](../core/README.md) — configuration and the N limit
- [analysis/](../analysis/README.md) — tests and metrics of this layer
- [render/](../render/README.md) — scene visualization

## 🇷🇺 Краткое резюме (Russian Summary)

- Физическое ядро комплекса: тела и сцены, интеграторы от ньютоновского RK4 до расщеплений гамильтониана 6-го порядка, планировщики траекторий (включая Теорему 3.1 ядра Trivortex), 20 пресетов и целый набор «наук»: ОТО, хаос, приливы, излучение, CR3BP, управление ориентацией КА;
- 27 модулей, сгруппированных в сцены, динамику, траектории, специальные режимы и наблюдаемые;
- каждый «научный» модуль несёт `self_check()` против литературной или наблюдательной ссылки: Меркурий 42.98″/век, отступание Луны 3.80 см/год, TRAPPIST-1e, FLI на потенциале Хенона—Хейлса, манёвр КА на 90° за 12 с при |H| ≤ 1.8e-16;
- планировщик Теоремы 3.1 с v2.0.1 записывает флаг `admissible`: замкнутая форма невырождена только при `C_Ch > pi*ln2 ~ 2.1776` (Теорема B), при C_Ch = 1 — Limacon с внутренней петлёй; тест S9 проверяет обе области;
- лимит Хавелока: кольцо равных вихрей устойчиво при N ≤ 7 и неустойчиво с N ≥ 8 — потому `core/config.py` требует `allow_unphysical` для N = 8 и отказывает при N ≥ 9 (тест S12).

---

<div align="center">

**[⬆ Back to top](#-lab--the-physics-core)** ·
**[trivortex_master](../README.md)** ·
**[Repository root](../../../README.md)**

*Part of [wild8highlander/Trivortex](https://github.com/wild8highlander/Trivortex) · Licensed under [IPL-RP-1.0](https://github.com/wild8highlander/Trivortex/blob/main/LICENSE.md) — All Rights Reserved*

</div>
