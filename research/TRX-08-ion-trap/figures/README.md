# TRX-08 — the figure set

The committed 300-dpi figures of the study **Three Laser-Cooled Ions in a Linear Paul Trap: the Table-Top Lagrange Triangle**, generated
by the study script (`--figures` mode; see
[`../code/`](../code/)) from the committed protocol in
[`../results/`](../results/). Every figure embeds the protocol-bound
numbers it illustrates — the pictures and the protocol cannot disagree.

## The files

| file | format | what it shows |
|------|--------|-----------------|
| [`fig01_crystal_landscape.png`](fig01_crystal_landscape.png) | 300 dpi | Crystal Landscape |
| [`fig02_crystal_and_modes.png`](fig02_crystal_and_modes.png) | 300 dpi | Crystal And Modes |
| [`fig03_scaling_sweeps.png`](fig03_scaling_sweeps.png) | 300 dpi | Scaling Sweeps |
| [`fig04_crystallization_dynamics.png`](fig04_crystallization_dynamics.png) | 300 dpi | Crystallization Dynamics |

The architecture diagram [`scheme_trx08.svg`](scheme_trx08.svg) — the study's
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
python3 code/trx08_ion_trap.py --figures    # from the study root
# or all twelve studies at once, from the repository root:
make research-figures
```

Requirements: `numpy`, `scipy`, `matplotlib`. The figures are committed,
so reading and citing the study never requires a matplotlib
installation.
