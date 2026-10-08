# TRX-09 — the figure set

The committed 300-dpi figures of the study **The Kirchhoff–Chaplygin Three-Vortex Problem (Classical Anchor)**, generated
by the study script (`--figures` mode; see
[`../code/`](../code/)) from the committed protocol in
[`../results/`](../results/). Every figure embeds the protocol-bound
numbers it illustrates — the pictures and the protocol cannot disagree.

## The files

| file | format | what it shows |
|------|--------|-----------------|
| [`fig01_regime_landscape.png`](fig01_regime_landscape.png) | 300 dpi | Regime Landscape |
| [`fig02_headline_results.png`](fig02_headline_results.png) | 300 dpi | Headline Results |
| [`fig03_parameter_sweeps.png`](fig03_parameter_sweeps.png) | 300 dpi | Parameter Sweeps |
| [`fig04_dynamics_invariants.png`](fig04_dynamics_invariants.png) | 300 dpi | Dynamics Invariants |

The architecture diagram [`scheme_trx09.svg`](scheme_trx09.svg) — the study's
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
python3 code/trx09_classical_anchor.py --figures    # from the study root
# or all twelve studies at once, from the repository root:
make research-figures
```

Requirements: `numpy`, `scipy`, `matplotlib`. The figures are committed,
so reading and citing the study never requires a matplotlib
installation.
