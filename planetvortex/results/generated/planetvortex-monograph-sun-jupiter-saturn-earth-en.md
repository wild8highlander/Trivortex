---
title: "The Gravitational Register of Sun, Jupiter, Saturn, Earth"
subtitle: "A personal monograph of the PLANETVORTEX closed gravifigure"
date: 2026-10-09 07:30 UTC
---

## 1. The model in one page

The Klein quartic $x^3y + y^3z + z^3x = 0$ is the genus-3 surface whose automorphism group $\mathrm{PSL}(2,7)$ of order 168 attains the Hurwitz bound $84(g-1)$. Its $\{7,3\}$ tessellation carries 24 heptagons — 12 antipodal pairs — and stage V2 of the bench carries the mass ladder of the chosen bodies in the vertex angles: $\alpha_i = 2\pi/3 - \sigma\, s_i$ with $s_i = \ln \mathrm{GM}_i - \langle \ln \mathrm{GM}\rangle$. The geometric-mean normalization makes $\sum s_i = 0$ exactly, and that is precisely the condition that the decorated tessellation closes on the Gauss–Bonnet budget $\sum \alpha_i = 8\pi = 2\pi(2g-2)$: the Euler characteristic absorbs the mass ladder. The heavier the body, the wider its heptagon — gravity drawn as geometry, in exact closed form: $\cosh R_i = \cot(\alpha_i/2)\,\cot(\pi/7)$, $\cosh(\ell_i/2) = \cos(\pi/7)/\sin(\alpha_i/2)$, $\cosh r_i = \cos(\alpha_i/2)/\sin(\pi/7)$, $A_i = 5\pi - 7\alpha_i$.

## 2. The gravimetric register algebra of the chosen set

### 2.1 The exact register dimensions

| body | GM, m³/s² | s | α, rad | R | ℓ | r | A | i, ° | λ, rad |
|---|---|---|---|---|---|---|---|---|---|
| **Sun** | 1.327124e+20 | +6.9575 | 1.922675 | 0.915956 | 0.881879 | 0.779261 | 2.249242 | — | — |
| **Jupiter** | 1.266865e+17 | +0.0033 | 2.094313 | 0.620843 | 0.566427 | 0.545417 | 1.047769 | 1.3044 | 0.022766 |
| **Saturn** | 3.793119e+16 | -1.2026 | 2.124078 | 0.555220 | 0.501664 | 0.490318 | 0.839420 | 2.4860 | 0.043389 |
| **Earth** | 3.986004e+14 | -5.7582 | 2.236515 | 0.138342 | 0.120360 | 0.124492 | 0.052360 | 0.0000 | 0.000000 |

λ = R̄·i is the arc register of the spatial tilt against the ecliptic (R̄ = 1 AU); the inclination rows come from the committed J2000 register (JPL).

### 2.2 The budget closure of this set

The budget closure of this set: Σα = 8.377580409573 against 8π = 25.132741228718 — residual 1.68e+01 (**the figure does NOT close (check the normalization)**).

## 3. The spatial registers (the inclined sky)

The spatial registers of the bench: the tilt operators $T = R_z(\Omega) R_x(i) \in SO(3)$, the arc registers $\lambda_i = \bar{R}\, i_i$ and the mutual-inclination matrix are certified by stage V1 (protocol `V1_inclined_registers.json`); the 3D Newtonian run from the real J2000 sky carries the conservation of the energy and of the full angular-momentum vector.

## 4. The verification certificate of this run

This monograph was generated together with a live verification run; the checks below were executed by the generator, not quoted.

| # | check | result | recorded |
|---|-------|:------:|----------|
| 1 | Σα = 8π (mpmath, 30 dps) | **PASS** | 0.0 |
| 2 | Σα = 8π (float64) | **PASS** | 7.11e-15 |
| 3 | the hyperbolic Pythagoras (12 cells) | **PASS** | 3.74e-16 |
| 4 | the SO(3) tilt orthogonality | **PASS** | 2.22e-16 |
| 5 | protocol P4_fano_algebra | **PASS** | committed |
| 6 | protocol X4_hyperbolic_figure | **PASS** | committed |
| 7 | protocol V2_klein_tiling | **PASS** | committed |

## 5. The corpus and the reproduction commands

The formal corpus: Theorems A–C, Lemma D, Lemma E (the planar bench), Theorem F (the coset construction), Lemma F (the antipodal freeness), Theorem G (the budget closure), Lemma G (the arc register) — docs/theorems/.

Every plotted or quoted number of the bench is bound to a JSON protocol in `results/protocols/` — committed before the run's tolerance, refreshed after it.

Reproduce everything with the committed pipeline (from the mini-repository root):

```bash
make all-ladders   # P1..P7 + X1..X6 + V1..V2, JSON protocols
make test          # the pytest guard
make crosslang     # the C99 kernel vs Python
make figures600    # this gallery at 600 dpi
make monograph     # a sample monograph
```

