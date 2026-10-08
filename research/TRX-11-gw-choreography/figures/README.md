# TRX-11 — the figure set

The committed 300-dpi figures of the study **Gravitational Waves from the Figure-Eight Choreography**, generated
by the study script (`--figures` mode; see
[`../code/`](../code/)) from the committed protocol in
[`../results/`](../results/). Every figure embeds the protocol-bound
numbers it illustrates — the pictures and the protocol cannot disagree.

## The files

| file | format | what it shows |
|------|--------|-----------------|
| [`fig01_orbit_overview.png`](fig01_orbit_overview.png) | 300 dpi | Orbit Overview |
| [`fig02_waveform_comb.png`](fig02_waveform_comb.png) | 300 dpi | Waveform Comb |
| [`fig03_pattern_sweep.png`](fig03_pattern_sweep.png) | 300 dpi | Pattern Sweep |
| [`fig04_quadrupole_dynamics.png`](fig04_quadrupole_dynamics.png) | 300 dpi | Quadrupole Dynamics |

The architecture diagram [`scheme_trx11.svg`](scheme_trx11.svg) — the study's
schematic: the physical system, the layer structure and the path from
the governing equations to the registered checks. It is the picture the
study README [§5](../README.md) annotates.

## The style

The TRIVORTEX figure family: the navy/steel/crimson palette, navy
spines, ticks in, grid behind — the same system as the parent
repository's galleries and the two mini-programs
([`cycloring`](../../../cycloring/figures/),
[`polyvortex`](../../../polyvortex/figures/)).

## Regeneration

```bash
python3 code/trx11_gw_choreography.py --figures    # from the study root
# or all twelve studies at once, from the repository root:
make research-figures
```

Requirements: `numpy`, `scipy`, `matplotlib`. The figures are committed,
so reading and citing the study never requires a matplotlib
installation.
