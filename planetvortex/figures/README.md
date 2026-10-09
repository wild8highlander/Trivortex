# `figures/` — the figure gallery

Two tiers:

| tier | where | how |
|------|-------|-----|
| the 300 dpi set + the scheme | this folder: `fig01–fig05`, `scheme_planetvortex.svg` | `make figures` (`python/planetvortex/figures.py`) |
| **the 600 dpi gallery, per task, + the GIF animations** | [`600dpi/`](600dpi/) — every task has its own folder with its own README | `make figures600` and `make animations` (`python/planetvortex/pubfigures.py`) |

| file | stages | what it shows |
|------|:------:|----------------|
| [`fig01_fano_gravity_figure.png`](fig01_fano_gravity_figure.png) | — | THE FIGURE: the heptagon of the seven wandering planets, the Sun at the centre, the seven Fano lines one-chord-per-class; the exact line-triangle with angles $(\pi/7, 2\pi/7, 4\pi/7)$ and area $\sqrt{7}/4$ |
| [`fig02_kepler_register.png`](fig02_kepler_register.png) | P2 | the Kepler comb $T = a^{3/2}$ and the three registers |
| [`fig03_planetary_simulation.png`](fig03_planetary_simulation.png) | P3 | the integrated inner and outer system (12 yr, RK4) with the conservation registers |
| [`fig04_vortex_lattice.png`](fig04_vortex_lattice.png) | P5, P6 | the $N = 7$ lattice over two rigid rotations; the seven congruent shape cycles |
| [`fig05_hardcore_certificates.png`](fig05_hardcore_certificates.png) | X1, X4, X5, X6 | the class equation, the measured orders, the precession ladder, the disk witness |
| [`scheme_planetvortex.svg`](scheme_planetvortex.svg) | — | the architecture |
| [`600dpi/`](600dpi/) | all | the ultra-high-resolution gallery: `V2_klein_tiling/` (the closed gravifigure!), `V1_inclined_registers/`, the P/X folders, `animations/` |

Every figure embeds its protocol residuals in the title — the
pictures quote the same numbers the protocols certify. The 600 dpi
factory is protocol-bound: it reads `results/protocols/*.json` and
refuses to run against a stale tree.
