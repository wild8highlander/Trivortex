# Authors

## Principal Investigator

**Isaev Iskhak Khamzatovich** (Исаев Исхак Хамзатович)

- **Role**: Principal Investigator & Sole Author
- **Affiliation**: Independent Researcher, Russian Federation
- **Email**: [aslan08_05@mail.ru](mailto:aslan08_05@mail.ru)
- **ORCID**: [0009-0003-7299-0701](https://orcid.org/0009-0003-7299-0701)
- **GitHub**: [@wild8highlander](https://github.com/wild8highlander)

### Research Interests

- The three-body (and N-body) problem: special solutions and choreographies
- Vortex dynamics: point vortices, Kirchhoff equations, relative equilibria
- Topological integrals of motion (Chaplygin-type invariants, AB-flux dressing)
- Celestial mechanics and Hamiltonian systems
- Spectral statistics and quantum-topological observables of vortex lattices
- Independent verification of numerical claims; multi-language porting

### Key Contributions

- **TRIVORTEX** (v1.0.0) — the working title and the single direction of
  this repository: an executable 22-section monograph on the three-body problem
  in the vortex model with the Chaplygin topological integral
  (formerly released as «AB-Cloud Vortex System for N-Body Problem»);
- **Theorem 3.1** — a Lagrange-type closed-form rotating solution
  `r_k(t) = √C_Ch·(1 + ε·cos(ωt + 2πk/3))`, `θ_k(t) = ωt + 2πk/3`,
  `ω = (2π/T)·e^(C_Ch/π)`, with the exact 2π/3 equilateral choreography;
- the **independent verification ladder V1–V4** with registered criteria and
  JSON protocols: choreography and periodicity (≤ 1e-12), the rigid Lagrange
  rotation at `ω = 3Γ/(2πa²)` (≤ 1e-6), and conservation of the vortex
  integrals `H, P, Q, I` (≤ 1e-10) for equal and unequal circulations;
- the **multi-language verification skeleton**: seven pinned Docker toolchains
  (Coq, Lean 4, Isabelle-HOL, Agda, Rust, C++, Haskell) and the staged
  M1–M3 formalization roadmap.

### Earlier editions

The repository's pre-restructure editions (v1.x — AB-Cloud spectral studies,
KdV, Klein attractor, Choptuik–Riemann) remain in
git history and in the versioned Zenodo record
[`10.5281/zenodo.21825394`](https://doi.org/10.5281/zenodo.21825394); since
version 1.0.0 the repository is a single-direction program dedicated to TRIVORTEX.

## Contributions

The verification framework, documentation site, CI pipeline and community
infrastructure are maintained by the principal investigator, with contributions
welcome under the rules of [`CONTRIBUTING.md`](CONTRIBUTING.md).
