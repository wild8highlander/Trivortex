# PLANETVORTEX — the committed protocols

Thirteen deterministic JSON files — seven of the P-ladder (P1..P7) and
six of the hardcore X-register (X1..X6) — keyed to the `default`
preset. These files are the numeric oracle of the bench: the tests pin
to them (including the cross-validation against the sibling polyvortex
ladder), the figure factory reads them, the READMEs and the monographs
quote them.

## The file index

| file | stage | check | headline recorded values |
|------|:-----:|-------|--------------------------|
| [`P1_anchor_default.json`](P1_anchor_default.json) | P1 | the exact figure literals + the Kepler–Earth anchor | chords $s_1$ `0.8677674782351162`, $s_2$ `1.5636629649360596`, $s_3$ `1.9498558243636472` AU; area $\sqrt{7}/4$; $\omega_7$ `0.4774648292756860`; Kepler anchor `9.75e-6` |
| [`P2_kepler_register_default.json`](P2_kepler_register_default.json) | P2 | Kepler III of the two-body dynamics, 8 planets | worst corrected `6.16e-13`; uncorrected `4.77e-4` (Jupiter); improvement `7.7e8`$\times$; fact-sheet worst `4.8e-4` (Neptune) |
| [`P3_planetary_nbody_default.json`](P3_planetary_nbody_default.json) | P3 | the Sun + 8-planets N-body, 12 yr | energy drift `2.07e-13`; AM drift `0.0`; worst $\Delta a/a$ `4.9e-3`; Kepler-dyn `2.5e-5`; perturbation hierarchy `2.2e-3` |
| [`P4_fano_algebra_default.json`](P4_fano_algebra_default.json) | P4 | the PSL(2,7) algebra, exact | 168 + 168; stabilizers `24/24`; 21 flags; isomorphism + conjugacy `True`; congruence `6.7e-16` |
| [`P5_heptagon_lattice_default.json`](P5_heptagon_lattice_default.json) | P5 | the heptagon lattice | $\omega$ error `1.35e-12`; invariants `≤ 1.25e-14`; $\max\mathrm{Re}\,\lambda$ `7.0e-9`; $H_{ring}$ `−1.08395426662194` exact |
| [`P6_seven_cells_default.json`](P6_seven_cells_default.json) | P6 | the seven cells | $T_{shape}$ `9.3814`, spread `0.0`; residual `3.9e-7`; drift `9.1e-14`; shape departure `0.288` |
| [`P7_gravity_bridge_default.json`](P7_gravity_bridge_default.json) | P7 | the gravity bridge | Schwarzschild error `1.0e-16`; Hill min margin `5.08`; line-spread `6.71 dex`; weighted-ring drift `0.298` vs `9.8e-15` |
| [`X1_sl2_enumeration_default.json`](X1_sl2_enumeration_default.json) | X1 | PSL(2,7) from first principles | `2016 / 336 / 168`; quotient 2-to-1 `True`; class equation `1+21+24+24+42+56`; order census `{1:1, 2:21, 3:56, 4:42, 7:48}`; simple `True` |
| [`X2_group_actions_default.json`](X2_group_actions_default.json) | X2 | the two natural actions | Sylow census `n2=21, n3=28, n7=8`; normalizers `8 / 21` (Frobenius census `{1:1, 3:14, 7:6}`); seven `S_4`s, stabilizer `{1:1, 2:9, 3:8, 4:6}`; action7 `168` faithful transitive; **bridge to the research model `True`**; action8 2-transitive `56/56` |
| [`X3_triangle_hurwitz_default.json`](X3_triangle_hurwitz_default.json) | X3 | the (2,3,7) generation + Hurwitz + Klein | product orders `{2:168, 3:336, 4:336, 7:336}`; `336` pairs, `0` non-generating; Klein relations `True×4`; Hurwitz `168 = 84·2 = 42·4`; quartic smooth, genus `3` |
| [`X4_hyperbolic_figure_default.json`](X4_hyperbolic_figure_default.json) | X4 | the hyperbolic {7,3} figure at 50 dps | Pythagoras residual `3.2e-29`; area ladder `π/42 → π/3 → 8π` exact to `3.2e-29`; `3V=7F=2E=168`, `14F=4E=6V=336`; disk witness: R error `0.0`, edge error `1.1e-16` |
| [`X5_integrator_certification_default.json`](X5_integrator_certification_default.json) | X5 | the integrator certification | slopes `2.000/3.995`; reversal `≤ 7.5e-12`; trend ratios `0.006 / 0.0002` vs RK4 `0.99`; LRL `≤ 5.5e-11`; vis-viva `≤ 2.3e-12`; orbit equation `≤ 7.3e-11` |
| [`X6_pn_perihelion_default.json`](X6_pn_perihelion_default.json) | X6 | the 1PN GR bridge | measured/formula `≤ 4.6e-4` (Mercury, Venus, Earth); Newtonian control `1.9e-10` rad/orbit; **Mercury `42.982″`/century** vs textbook `42.98` (`5.3e-5`); full 8-planet ladder `42.98 → 0.0008` |

## The schema (stable across stages)

```jsonc
{
  "suite": "planetvortex-ladder",     // the X protocols: "planetvortex-hardcore"
  "version": "1.1.0",
  "stage": "P4",
  "preset": "default",
  "date_utc": "…",                   // the run stamp (carries no role in the numbers)
  "check": { … },                    // the registered statement + recorded registers
  "params": { … },                   // the full parameter snapshot
  "passed": true
}
```

The **P1 anchor is the figure-binding stage**: its pinned literals
($s_1$, $s_2$, $s_3$, the angle ladder $\pi/7 : 2\pi/7 : 4\pi/7$, the
area $\sqrt{7}/4$ and $\omega_7 = 3/2\pi$) are the exact closed forms
of Theorem A — the same numbers the sibling polyvortex ladder carries
at $N = 7$ for the rate, bound here to the figure.

## Regeneration and determinism

```bash
make all-ladders   # rewrites all thirteen files with identical numbers
```

Fixed grids, fixed integrator settings, deterministic linear algebra —
a `git diff` on this folder after a re-run must be empty (the run
stamp `date_utc` excepted); otherwise it is a reproducibility bug:
open an issue with the diff attached.
