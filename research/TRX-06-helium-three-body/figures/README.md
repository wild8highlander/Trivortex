# TRX-06 — the figure set

The committed 300-dpi figures of the study **Helium Atom as the Coulomb Three-Body Problem (Classical Trajectory Monte Carlo)**, generated
by the study script (`--figures` mode; see
[`../code/`](../code/)) from the committed protocol in
[`../results/`](../results/). Every figure embeds the protocol-bound
numbers it illustrates — the pictures and the protocol cannot disagree.

## The files

| file | format | what it shows |
|------|--------|-----------------|
| [`fig01_model_landscape.png`](fig01_model_landscape.png) | 300 dpi | Model Landscape |
| [`fig02_energy_sharing.png`](fig02_energy_sharing.png) | 300 dpi | Energy Sharing |
| [`fig03_parameter_sweeps.png`](fig03_parameter_sweeps.png) | 300 dpi | Parameter Sweeps |
| [`fig04_autoionization_dynamics.png`](fig04_autoionization_dynamics.png) | 300 dpi | Autoionization Dynamics |

The architecture diagram [`scheme_trx06.svg`](scheme_trx06.svg) — the study's
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
python3 code/trx06_helium_three_body.py --figures    # from the study root
# or all twelve studies at once, from the repository root:
make research-figures
```

Requirements: `numpy`, `scipy`, `matplotlib`. The figures are committed,
so reading and citing the study never requires a matplotlib
installation.
