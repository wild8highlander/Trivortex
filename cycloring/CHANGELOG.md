# Changelog — cycloring

All notable changes of the Gamma-period ring laboratory are documented here.
The format follows Keep a Changelog; versions are semver.

## [1.0.0] — 2026-10-08

### Added

- The Gamma-period core `periods.py`: the functional
  Ω(a,b) = Γ(a/N)Γ(b/N)/Γ((a+b)/N), the reflection register
  Γ(z)Γ(1−z) = π/sin(πz), the sine product Π 2 sin(πm/N) = N,
  the normalized periods P(a,b) and the witness W_N (mpmath, 50 digits).
- The defect chain `chain.py`: the triple (N, B, λ₀) → δ = π/N,
  k = ⌈Bλ₀/Γ²⌉, γ = δ⁴/k, δ_eff = δ⁵/k, Δ_Ch = γ·W_N/(N−1), and the
  transducer ε = Δ/(1+Δ), ν = ω_L(1+Δ)³/(1+2Δ)^{3/2} = ω_L(1−ε²)^{−3/2},
  C_N = ln(1+1/Δ) = −ln ε.
- The algebraization layer `ring.py`: the root system z^N = σ(t), the
  roots-of-unity filter (moments S_m), the character decomposition, the
  pumped synchronous-breathing program and its closed rosettes.
- The Kirchhoff layer `dynamics.py`: vectorized RHS, RK4, H/P/Q/I, the
  analytic Jacobian, the closed-form Hamiltonian of the regular polygon
  and the distance-product/discriminant registers.
- The verification-and-research ladder W1–W7 with deterministic JSON
  protocols (`results/protocols/*.json`, default preset):
  period core, algebraic boundary, root system, polygon flow, transport
  identity, synchronous closure, transducer table of the levels 7/9/15/30.
- The figure factory `figures.py`: five 300 dpi publication figures bound
  to the committed protocols plus the architecture scheme SVG.
- The pytest guard (37 tests) and the publication stack: the research
  monograph (RU/EN, MD/DOCX/PDF) and the five-theorem monograph edition
  (RU/EN, DOCX/PDF).
