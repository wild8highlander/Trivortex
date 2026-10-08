# TRX-05 — the figure set

The committed 300-dpi figures of the study **Optical Vortices of Laser Beams and the Point-Vortex Analogy**, generated
by the study script (`--figures` mode; see
[`../code/`](../code/)) from the committed protocol in
[`../results/`](../results/). Every figure embeds the protocol-bound
numbers it illustrates — the pictures and the protocol cannot disagree.

## The files

| file | format | what it shows |
|------|--------|-----------------|
| [`fig01_field_landscape.png`](fig01_field_landscape.png) | 300 dpi | Field Landscape |
| [`fig02_rigid_rotation.png`](fig02_rigid_rotation.png) | 300 dpi | Rigid Rotation |
| [`fig03_parameter_sweeps.png`](fig03_parameter_sweeps.png) | 300 dpi | Parameter Sweeps |
| [`fig04_invariants_rigidity.png`](fig04_invariants_rigidity.png) | 300 dpi | Invariants Rigidity |

The architecture diagram [`scheme_trx05.svg`](scheme_trx05.svg) — the study's
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
python3 code/trx05_optical_vortices.py --figures    # from the study root
# or all twelve studies at once, from the repository root:
make research-figures
```

Requirements: `numpy`, `scipy`, `matplotlib`. The figures are committed,
so reading and citing the study never requires a matplotlib
installation.
