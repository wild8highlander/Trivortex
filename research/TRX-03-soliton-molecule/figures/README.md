# TRX-03 — the figure set

The committed 300-dpi figures of the study **Three-Soliton Molecule in a Mode-Locked Fiber Laser**, generated
by the study script (`--figures` mode; see
[`../code/`](../code/)) from the committed protocol in
[`../results/`](../results/). Every figure embeds the protocol-bound
numbers it illustrates — the pictures and the protocol cannot disagree.

## The files

| file | format | what it shows |
|------|--------|-----------------|
| [`fig01_potential_landscape.png`](fig01_potential_landscape.png) | 300 dpi | Potential Landscape |
| [`fig02_molecule_formation.png`](fig02_molecule_formation.png) | 300 dpi | Molecule Formation |
| [`fig03_phase_sweep.png`](fig03_phase_sweep.png) | 300 dpi | Phase Sweep |
| [`fig04_breathing_dynamics.png`](fig04_breathing_dynamics.png) | 300 dpi | Breathing Dynamics |

The architecture diagram [`scheme_trx03.svg`](scheme_trx03.svg) — the study's
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
python3 code/trx03_soliton_molecule.py --figures    # from the study root
# or all twelve studies at once, from the repository root:
make research-figures
```

Requirements: `numpy`, `scipy`, `matplotlib`. The figures are committed,
so reading and citing the study never requires a matplotlib
installation.
