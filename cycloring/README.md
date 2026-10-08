# CYCLORING — the Gamma-period ring laboratory

*A self-contained mini-research program: the regular N-vortex ring treated
as an algebraic object — the root system of one binomial — with its angular
phases on the cyclotomic lattice and its radial modulation produced from
Gamma-periods through a finite defect chain. The program ships its own
codes, its own verification ladder, its own protocols, its own figures and
its own monographs.*

Version 1.0.0 · License: LicenseRef-Proprietary-Wild8Highlander-1.0
(see LICENSE.md at the repository root) · Python 3.10+ · numpy, mpmath

---

## What this is

The program starts from the frozen regular N-gon of equal point vortices
(the rigid relative equilibrium rotating at
$\omega_L = \Gamma(N-1)/(4\pi R^2)$) and asks one question: **can the whole
breathing dynamics of the ring be read off from a finite set of periods of
the level?** The answer assembled here is yes, through four registers:

1. **The ring is a root system (Theorem 1).** The configuration
   $z_k(t) = r(t)\,\zeta_N^k e^{i\nu t}$ is exactly the full set of roots of
   $z^N = \sigma(t)$ with $\sigma(t) = r(t)^N e^{iN\nu t}$; the power sums
   satisfy $S_m = \sum_k z_k^m = 0$ for $m < N$ and $S_N = N\sigma$, the
   linear impulse vanishes identically, and the Galois group
   $\mathrm{Gal}(\mathbb{Q}(\zeta_N)/\mathbb{Q})$ acts on the ring by
   relabeling the vortices — the character lattice $\widehat\mu_N$ IS the
   mode decomposition of the ring.
2. **The boundary of the period domain is algebraic (Theorem 2).** With
   $\Omega_{a,b} = \Gamma(a/N)\Gamma(b/N)/\Gamma((a+b)/N)$ the reflection
   identity gives $\Omega_{a,N-a} = \pi/\sin(\pi a/N)$ — every boundary
   period is an algebraic multiple of $\pi$, while the interior periods are
   genuine Gamma-transcendentals. The sine product
   $\prod_m 2\sin(\pi m/N) = N$ is the algebraic backbone.
3. **The defect chain is a period transducer (Theorem 3).** From the triple
   $(N, B, \lambda_0)$ — level, angular impulse, frozen frequency — the
   chain $\delta = \pi/N$, $k = \lceil B\lambda_0/\Gamma^2\rceil$,
   $\gamma = \delta^4/k$, $\delta_{eff} = \delta^5/k$,
   $\Delta_{Ch} = \gamma W_N/(N-1)$ produces the modulation program
   $\varepsilon = \Delta/(1+\Delta)$,
   $\nu = \omega_L (1+\Delta)^3/(1+2\Delta)^{3/2} = \omega_L(1-\varepsilon^2)^{-3/2}$,
   $C_N = \ln(1+1/\Delta) = -\ln\varepsilon$. The classical limit
   $\Delta \to 0$ recovers the rigid ring.
4. **The synchronous breathing closes exactly (Theorem 4).** The cycle mean
   of the frozen transport law is
   $\langle(1+\varepsilon\cos u)^{-2}\rangle = (1-\varepsilon^2)^{-3/2}$ —
   choosing $\nu$ to be exactly this mean makes every vortex ride a closed
   rosette and returns the whole configuration after
   $T_c = 2\pi/\nu$. The dichotomy register (Theorem 5): the pair-distance
   product and the discriminant $N^N\sigma^{N-1}$ are algebraic, while the
   Hamiltonian carries the transcendental shell
   $H(R) = -\frac{\Gamma^2}{2\pi}\left[\frac{N(N-1)}{2}\ln R + \frac{N}{2}\ln N\right]$.

## The W-ladder

| stage | register | status | protocol |
|-------|----------|:------:|----------|
| W1 | The period core: reflection identity, P(1,1)=1, symmetry | PASS | `W1_period_core_default.json` |
| W2 | The algebraic boundary: Ω(a,N−a) = π/sin(πa/N) + sine product | PASS | `W2_algebraic_boundary_default.json` |
| W3 | The root system: z^N − σ identity, moments, impulse | PASS | `W3_root_system_default.json` |
| W4 | The polygon flow: rigid rotation, shape, invariants, H form | PASS | `W4_polygon_flow_default.json` |
| W5 | The transport identity + the exact 2π phase advance | PASS | `W5_transport_identity_default.json` |
| W6 | The synchronous closure of the rosettes | PASS | `W6_synchronous_closure_default.json` |
| W7 | The transducer table of the levels N = 7, 9, 15, 30 | PASS | `W7_transducer_default.json` |

Every protocol is a deterministic JSON file bound to a run; the test suite
re-derives the preset-independent numbers. The mpmath registers run at 50
working digits (identity tolerances 1e−30); the dynamics registers use RK4
(rate tolerance 1e−9, invariant drifts 1e−12).

## The registered level table (default preset)

| N | k | W_N | Δ_Ch | ε_N | ν/ω_L | C_N |
|---|---|-----|------|-----|-------|-----|
| 7 | 4 | 2.175444 | 3.677e−03 | 3.664e−03 | 1.0000201 | 5.609 |
| 9 | 6 | 2.416543 | 7.474e−04 | 7.469e−04 | 1.0000042 | 7.200 |
| 15 | 17 | 2.915447 | 2.357e−05 | 2.357e−05 | 1.0000000 | 10.656 |
| 30 | 70 | 3.603649 | 2.135e−07 | 2.135e−07 | 1.0000000 | 15.360 |

The stiffness grows with the level: the breathing amplitude falls like a
power law Δ_Ch(N) ≈ 1.7·10³·N^{−6.7} on the scanned range N = 3..30, so
high cyclotomic levels are stiff rings and the low levels breathe.

## The publication stack

| item | languages | formats |
|------|-----------|---------|
| the big research monograph | RU, EN | `.md`, `.docx`, `.pdf` |
| Theorem 1 — the root system of the ring | RU, EN | `.docx`, `.pdf` |
| Theorem 2 — the algebraic boundary of the period domain | RU, EN | `.docx`, `.pdf` |
| Theorem 3 — the period transducer | RU, EN | `.docx`, `.pdf` |
| Theorem 4 — the synchronous breathing | RU, EN | `.docx`, `.pdf` |
| Theorem 5 — the dichotomy of the invariants | RU, EN | `.docx`, `.pdf` |
| figures (fig01–fig05 + the scheme) | — | `.png` 300 dpi, `.svg` |

Every document embeds the figures and quotes only protocol-bound numbers;
the DOCX files carry proper field TOCs, the PDFs are the LibreOffice render
of the very same DOCX.

## Quickstart

```bash
# from the mini-research root
cd cycloring

make ladder   # run W1..W7 (default preset), refresh the JSON protocols
make quick    # fast smoke of the whole ladder
make figures  # regenerate figures/ (300 dpi PNG + the scheme SVG)
make test     # the pytest guard (37 tests)
make lint     # black --check + ruff + mypy (scoped)
```

The runner can also address a single stage:

```bash
PYTHONPATH=python python3 python/cycloring/runner.py --stage W5 --preset default
```

## Layout

```text
cycloring/
├── README.md            ← this file
├── README_RU.md         ← the Russian mirror
├── CHANGELOG.md         ← the mini-research changelog
├── Makefile             ← ladder / quick / full / figures / test / lint
├── docs/
│   ├── monograph/       ← THE BIG MONOGRAPH: monograph_RU|EN.{md,docx,pdf}
│   └── monographs/      ← THEOREM EDITION: Theorems 1–5
│                          (CYCLORING-Theorem{k}_{RU,EN}.docx / .pdf, 20 files)
├── figures/             ← fig01–fig05 (300 dpi PNG) + scheme_cycloring.svg
│                          generated by `make figures`, bound to protocols
├── python/cycloring/
│   ├── periods.py       ← the Gamma-period core (mpmath)
│   ├── chain.py         ← the defect chain + the transducer
│   ├── ring.py          ← the root system, characters, the breathing program
│   ├── dynamics.py      ← the Kirchhoff layer: RHS, RK4, H/P/Q/I, Jacobian
│   ├── ladder.py        ← the W1..W7 checks
│   ├── runner.py        ← the JSON protocol CLI
│   └── figures.py       ← the figure factory (300 dpi, protocol-bound)
├── tests/               ← the pytest guard (37 tests)
└── results/protocols/   ← the committed JSON protocols (default preset)
```

## Honesty notes

- The breathing program is a **kinematic program**: the frozen polygon has
  no radial velocity in the Kirchhoff field (pair cancellation), so the
  pump must supply the radial drive; the angular transport, however, is
  not prescribed but follows the frozen law Λ₀/r(t)² — and that is why the
  transport identity and the synchronous closure are exact statements,
  not approximations.
- The interior periods Ω(a,b) with a+b ≠ N are treated as transcendental
  constants of Gamma type; no algebraic reduction is claimed for them, and
  none is used anywhere in the chain — the only periods the chain consumes
  are the normalized diagonal sums W_N and the algebraic boundary values.
- The power law Δ_Ch(N) ≈ 1.7·10³·N^{−6.7} is a numerical fit on
  N = 3..30, not an asymptotic theorem; only the monotonicity of γ is
  proved.
- All dynamics registers are RK4 with the tolerances listed above; the
  spectral registers of the Jacobian are used only as diagnostics, the
  ladder does not claim nonlinear stability results.

## Roadmap of the mini-research

1. **C1 — formalize Theorem 1** (the root system + the roots-of-unity
   filter) in Coq and Lean 4: pure algebra, the cheapest decidable target.
2. **C2 — the reflection register** (Theorem 2) as an interval-arithmetic
   certificate on a dense grid of levels.
3. **C3 — the transport identity** (Theorem 4) via the differentiated
   Poisson integral, or a verified quadrature certificate.
4. **C4 — widening**: unequal circulations (when does a deformed ring keep
   a period lattice?), the two-frequency breathing programs with
   Ω/ν = P(a,b), and the character-mode shear experiment.
