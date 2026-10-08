# TRX-02 — the figure set

The committed 300-dpi figures of the study **Resonant Three-Wave Interaction (Manley–Rowe, χ⁽²⁾ Optics)**, generated
by the study script (`--figures` mode; see
[`../code/`](../code/)) from the committed protocol in
[`../results/`](../results/). Every figure embeds the protocol-bound
numbers it illustrates — the pictures and the protocol cannot disagree.

## The files

| file | format | what it shows |
|------|--------|-----------------|
| [`fig01_resonance_geometry.png`](fig01_resonance_geometry.png) | 300 dpi | Resonance Geometry |
| [`fig02_pump_depletion.png`](fig02_pump_depletion.png) | 300 dpi | Pump Depletion |
| [`fig03_parameter_sweep.png`](fig03_parameter_sweep.png) | 300 dpi | Parameter Sweep |
| [`fig04_invariants_shg.png`](fig04_invariants_shg.png) | 300 dpi | Invariants Shg |

The architecture diagram [`scheme_trx02.svg`](scheme_trx02.svg) — the study's
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
python3 code/trx02_three_wave_mixing.py --figures    # from the study root
# or all twelve studies at once, from the repository root:
make research-figures
```

Requirements: `numpy`, `scipy`, `matplotlib`. The figures are committed,
so reading and citing the study never requires a matplotlib
installation.
