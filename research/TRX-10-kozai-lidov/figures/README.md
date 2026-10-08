# TRX-10 — the figure set

The committed 300-dpi figures of the study **Kozai–Lidov Oscillations in Hierarchical Triples**, generated
by the study script (`--figures` mode; see
[`../code/`](../code/)) from the committed protocol in
[`../results/`](../results/). Every figure embeds the protocol-bound
numbers it illustrates — the pictures and the protocol cannot disagree.

## The files

| file | format | what it shows |
|------|--------|-----------------|
| [`fig01_kl_landscape.png`](fig01_kl_landscape.png) | 300 dpi | Kl Landscape |
| [`fig02_kl_exchange.png`](fig02_kl_exchange.png) | 300 dpi | Kl Exchange |
| [`fig03_kl_sweeps.png`](fig03_kl_sweeps.png) | 300 dpi | Kl Sweeps |
| [`fig04_kl_dynamics.png`](fig04_kl_dynamics.png) | 300 dpi | Kl Dynamics |

The architecture diagram [`scheme_trx10.svg`](scheme_trx10.svg) — the study's
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
python3 code/trx10_kozai_lidov.py --figures    # from the study root
# or all twelve studies at once, from the repository root:
make research-figures
```

Requirements: `numpy`, `scipy`, `matplotlib`. The figures are committed,
so reading and citing the study never requires a matplotlib
installation.
