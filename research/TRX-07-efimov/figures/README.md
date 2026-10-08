# TRX-07 — the figure set

The committed 300-dpi figures of the study **The Efimov Effect: Universal Quantum Three-Body Physics**, generated
by the study script (`--figures` mode; see
[`../code/`](../code/)) from the committed protocol in
[`../results/`](../results/). Every figure embeds the protocol-bound
numbers it illustrates — the pictures and the protocol cannot disagree.

## The files

| file | format | what it shows |
|------|--------|-----------------|
| [`fig01_efimov_landscape.png`](fig01_efimov_landscape.png) | 300 dpi | Efimov Landscape |
| [`fig02_universal_numbers.png`](fig02_universal_numbers.png) | 300 dpi | Universal Numbers |
| [`fig03_ladder_stability.png`](fig03_ladder_stability.png) | 300 dpi | Ladder Stability |
| [`fig04_scaling_laws.png`](fig04_scaling_laws.png) | 300 dpi | Scaling Laws |

The architecture diagram [`scheme_trx07.svg`](scheme_trx07.svg) — the study's
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
python3 code/trx07_efimov.py --figures    # from the study root
# or all twelve studies at once, from the repository root:
make research-figures
```

Requirements: `numpy`, `scipy`, `matplotlib`. The figures are committed,
so reading and citing the study never requires a matplotlib
installation.
