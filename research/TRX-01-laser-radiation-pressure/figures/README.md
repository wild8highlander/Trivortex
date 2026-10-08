# TRX-01 — the figure set

The committed 300-dpi figures of the study **Radiation-Pressure Restricted Three-Body Problem (Laser on Dust)**, generated
by the study script (`--figures` mode; see
[`../code/`](../code/)) from the committed protocol in
[`../results/`](../results/). Every figure embeds the protocol-bound
numbers it illustrates — the pictures and the protocol cannot disagree.

## The files

| file | format | what it shows |
|------|--------|-----------------|
| [`fig01_landscape.png`](fig01_landscape.png) | 300 dpi | Landscape |
| [`fig02_l4_shift.png`](fig02_l4_shift.png) | 300 dpi | L4 Shift |
| [`fig03_stability_scan.png`](fig03_stability_scan.png) | 300 dpi | Stability Scan |
| [`fig04_jacobi_drift.png`](fig04_jacobi_drift.png) | 300 dpi | Jacobi Drift |

The architecture diagram [`scheme_trx01.svg`](scheme_trx01.svg) — the study's
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
python3 code/trx01_laser_radiation_pressure.py --figures    # from the study root
# or all twelve studies at once, from the repository root:
make research-figures
```

Requirements: `numpy`, `scipy`, `matplotlib`. The figures are committed,
so reading and citing the study never requires a matplotlib
installation.
