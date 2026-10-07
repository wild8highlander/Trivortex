# TRIVORTEX Orbital Animations

*TRIVORTEX Research Program · version 1.0.0*

This folder holds the four reference animations of the repository. Each one is
a seamless closed loop built from the exact analytic period of the underlying
solution (or from a full period of the integrated orbit), rendered in the
repository navy-gold style (`#0A1730` background, gold `#D4AF37`, cyan
`#59C2FF`, rose `#FF7A9E`). Every animation exists in two formats: **GIF**
(universal playback, in-repo preview, site embedding) and **MP4** (H.264,
compact, for slides and documents). On-frame text follows the repository
figure convention (English); the prose documentation lives in this README.

| File | What it shows | Physics |
|---|---|---|
| `anim01_trivortex_ring.gif/.mp4` | The breathing-ring choreography of Theorem 3.1: three bodies at fixed angles `2πk/3` pulse radially in a 120°-phase-locked wave | `r_k(t) = √C_Ch·(1 + ε·cos(ωt + 2πk/3))`, `ω = (2π/T)·e^(C_Ch/π)`; here `C_Ch = 1`, `ε = 0.14`, loop = one breathing period `2π/ω` |
| `anim02_figure_eight.gif/.mp4` | The Chenciner–Montgomery free-fall figure eight (2000): three equal masses chase each other along one closed curve | classic initial conditions, Newtonian gravity `G = m = 1`, integrated with DOP853 at `rtol = atol = 1e-12`; loop = one orbit period `T ≈ 6.324090548` |
| `anim03_lagrange_triangle.gif/.mp4` | Lagrange's 1772 equilateral solution: three equal masses rotate rigidly, preserving the triangle | `ω = √(3Gm/a³)` with `G = m = a = 1`; loop = one revolution `2π/ω`; the celestial twin of the TRIVORTEX vortex triangle |
| `anim04_laser_stationkeeping.gif/.mp4` | Laser station-keeping at the photogravitational L4 (crossing of TRX-01 and TRX-12): a free sail librates widely, a laser-guided sail locks onto the radiation-displaced point `L4*` | Earth–Moon `μ = 0.0121505856`, radiation `β = 0.05` renormalizes primary 1; PD beam-steering `kp = kd = 4` with photon-thrust cap `a_max = 2P/(cm)` (dimensionless `0.244`), the TRX-12 operating point |

## Reading the laser animation

Two sails start from the same displaced position near `L4*`. The rose sail is
unguided: its tadpole libration wanders far from the displaced point over the
40 time units of the run. The cyan sail is pushed by a laser whose thrust is
steered by the PD law `u = sat_{a_max}(−kp·Δr − kd·v)`; the golden beam line
from the radiating primary is drawn whenever the laser is firing, and the
readout in the lower left corner reports the instantaneous thrust. By
`t ≈ 15` the guided sail is already hovering on `L4*`, and by the end of the
run the thrust has decayed to zero — the sail is captured. This is the visual
summary of TRX-01 (the laser moves the libration point) and TRX-12 (the laser
holds a sail there) in one picture.

## Reproduction

```bash
python3 docs/animations/make_animations.py            # GIF + MP4 (ffmpeg for MP4)
python3 docs/animations/make_animations.py --preview  # + poster PNGs for inspection
```

Dependencies: Python ≥ 3.11, numpy, scipy, matplotlib ≥ 3.9; ffmpeg optional
(MP4 branch). No network access, no stochastic seeds: every loop is a closed
form or a fixed-accuracy integration, so the output is bit-reproducible on
the reference machine. Runtime is ≈ 2.5 min for all four animations on the
reference machine.

## Design notes

- All four loops are seamless: animations 01 and 03 close on the analytic
  period of the solution, animation 02 closes on the numerically refined
  figure-eight period, and animation 04 is a fading-cycle rendering of a
  finite integration run.
- The `L4*` marker (gold cross) is the displaced triangular point obtained by
  a two-dimensional Newton iteration on `∇Ω = 0` for the photogravitational
  potential — the same solver as in TRX-01.
- Colors, fonts and layout mirror `docs/assets/*.svg` and the 300-DPI figure
  standard of `research/_FORMAT_SPEC.md`, so animations, schemes and figures
  read as one visual family.

---

## Regenerating

The generator is committed and deterministic:

```bash
python3 docs/animations/make_animations.py   # or: make animations
```

It rebuilds all four choreographies in both formats from the committed
integrators — no manual frame editing anywhere. Requirements: `numpy`,
`scipy`, `matplotlib` (frames), `imageio` (GIF assembly) and `imageio-ffmpeg`
(MP4 assembly). Every loop closes exactly: the frame count and the time grid
are derived from the analytic period of the underlying solution, so the last
frame continues seamlessly into the first.

## Format guide

| Format | Role | Properties |
|---|---|---|
| GIF | in-repo preview, GitHub embedding, README figures | 640 px, universal playback, looped |
| MP4 | slides, documents, site hero material | H.264, compact, 300-dpi-crisp rendering |

## Palette and figure convention

The animations use the repository's identity palette — navy `#0A1730`
background, gold `#D4AF37` accents, cyan `#59C2FF` and rose `#FF7A9E` series —
the same system as the SVG figures, the study figures and the monograph
covers. On-frame text follows the repository figure convention (English);
the physics and the reproduction notes live in this README.

## Physics notes

- **anim01 (Theorem 3.1 ring):** the radial pulsation is the closed-form
  modulation `r_k(t) = √C_Ch·(1 + ε·cos(ωt + 2πk/3))` with the exact
  frequency lock `ω = (2π/T)·e^{C_Ch/π}` — the triangle never deforms, it
  breathes.
- **anim02 (figure eight):** the Chenciner–Montgomery initial conditions,
  integrated with DOP853 at `rtol = atol = 1e-12`; the loop is one full orbit
  period `T ≈ 6.324090548`, and the closing error is below the integrator
  tolerance.
- **anim03 (Lagrange triangle):** rigid rotation at `ω = √(3Gm/a³)` — the
  celestial twin of the same-sign vortex triangle of TRX-09 and Theorem 3.1.
- **anim04 (laser stationkeeping):** the photogravitational Earth–Moon problem
  with `β = 0.05`; the unguided sail librates away from the displaced point,
  the PD-steered sail locks onto `L4*` — the TRX-01 + TRX-12 operating point.
