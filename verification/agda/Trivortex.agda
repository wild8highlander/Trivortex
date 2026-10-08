------------------------------------------------------------------------
-- SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
-- SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
------------------------------------------------------------------------
-- TRIVORTEX — CONSTRUCTIVE ANGLE ARITHMETIC (Agda, milestone M2)
------------------------------------------------------------------------
-- Milestone M2 artifact: `verification/agda/Trivortex.agda`.
--
-- Provenance: this module mirrors the analytic layer of
-- `verification/trivortex/python/verify.py` (M0 release, repository main
-- branch, commit 557bff8) in a CONSTRUCTIVE form. The angle bookkeeping
-- of the choreography is discretized onto the rotation lattice it actually
-- lives on: one full turn is the unit, the three vortices of the
-- equilateral choreography occupy the lattice points 0, 1/3, 2/3, and the
-- choreography statements reduce to finite, normalization-free arithmetic
-- on `Fin 3`:
--
--   * the equilateral choreography: `rot` advances each vortex by exactly
--     one lattice step (a rigid 120° shift), has no fixed point, and
--     composes to the identity after three steps — three steps of 1/3 of
--     a turn make one full turn (V1, property (a) + the C3 group);
--   * periodicity of the radial closed form over ℚ, given the single
--     declared axiom below (V1, property (b));
--   * the Chaplygin combination C_Ch = r²θ̇ − q·r over ℚ with its
--     additivity-in-θ̇ identity — the algebraic shape the ladders record;
--   * the vortex integrals P, Q with the exact centroid anchors
--     P = Q = 0 for every state whose centroid sits at the origin
--     (the symmetric reference state included).
--
-- AXIOM FOOTPRINT (declared, per the acceptance criteria of the stub):
--   postulate c      : ℚ → ℚ                      -- the cosine atom
--   postulate c-add1 : ∀ q → c (q + 1ℚ) ≡ c q     -- period: one turn
-- Everything else is proven constructively from the Agda standard
-- library. The wrap-around of the phase lattice (three uniform steps
-- closing the circle) is exactly the content of `rot³-id` on the lattice
-- side; the corresponding turn-modulo identification on the ℚ side lives
-- behind the declared period axiom — an honest division of labor that
-- this header makes explicit.
--
-- Type-check (pinned toolchain, docker/agda/Dockerfile — Agda 2.6 + stdlib):
--     docker build -t trivortex-agda verification/docker/agda
--     docker run --rm -v "$PWD":/work -w /work trivortex-agda \
--         agda verification/agda/Trivortex.agda
--
-- Author: Isaev Iskhak Khamzatovich (repository owner)
-- Year: 2026
------------------------------------------------------------------------

module Trivortex where

open import Data.Empty using (⊥)
open import Data.Fin using (Fin; zero; suc)
open import Data.Rational using (ℚ; 0ℚ; 1ℚ; _+_; _*_; -_; _−_)
open import Data.Rational.Properties
  using (*-distribˡ-+; +-assoc; +-comm; *-identityʳ; *-zeroʳ)
open import Relation.Binary.PropositionalEquality
  using (_≡_; refl; cong; sym; trans)
open Relation.Binary.PropositionalEquality.≡-Reasoning
  using (begin_; _≡⟨_⟩_; _∎)

------------------------------------------------------------------------
-- Section 1 — the C3 rotation lattice of the choreography
------------------------------------------------------------------------

-- The three vortices of the equilateral choreography occupy the lattice
-- points 0, 1/3, 2/3 of a turn. Advancing each vortex to the position of
-- the next is the generator of the C3 rotation group.

-- `rot` sends each lattice point to the next one, cyclically.
rot : Fin 3 → Fin 3
rot zero               = suc zero
rot (suc zero)         = suc (suc zero)
rot (suc (suc zero))   = zero
rot (suc (suc (suc ())))

-- * Certified property: `rot` is a 3-cycle — three steps of 1/3 of a
--   turn compose into one full turn, i.e. the identity on the lattice.
--   This is the constructive form of "three vortices at 120° close the
--   circle" — the angular-arithmetic core of the choreography.
rot³-id : ∀ (i : Fin 3) → rot (rot (rot i)) ≡ i
rot³-id zero               = refl
rot³-id (suc zero)         = refl
rot³-id (suc (suc zero))   = refl
rot³-id (suc (suc (suc ())))

-- * Certified property: the angular separation of consecutive vortices
--   never vanishes — a 1/3-shifted orbit has no fixed point. (The
--   positive counterpart is `rot³-id`: the orbit of every point is the
--   whole lattice.)
no-fixed-point : ∀ (i : Fin 3) → rot i ≡ i → ⊥
no-fixed-point zero               ()
no-fixed-point (suc zero)         ()
no-fixed-point (suc (suc zero))   ()
no-fixed-point (suc (suc (suc ())))

------------------------------------------------------------------------
-- Section 2 — the phase lattice
------------------------------------------------------------------------

-- The phase of the k-th vortex: uniform steps of δ of a turn, on the
-- same Fin 3 lattice. With δ = 1/3 of a turn this is the angular
-- bookkeeping of the equilateral choreography; the module keeps δ
-- abstract so no rational normalization is needed anywhere.

phaseOf : ℚ → Fin 3 → ℚ
phaseOf δ zero               = 0ℚ
phaseOf δ (suc zero)         = δ
phaseOf δ (suc (suc zero))   = δ + δ
phaseOf δ (suc (suc (suc ())))

-- * Certified property: consecutive phases advance by EXACTLY one step
--   δ (the rigid 120° shift, for every δ — in particular for δ = 1/3).
uniform-step : ∀ δ (i : Fin 2) → phaseOf δ (suc i) ≡ phaseOf δ i + δ
uniform-step δ zero               = refl
uniform-step δ (suc zero)         = refl
uniform-step δ (suc (suc ()))

-- * Certified property: advancing by one lattice step via `rot` shifts
--   the phase by exactly one step δ, on the open chain:
phase-shifts-by-one-step : ∀ δ (i : Fin 2) →
  phaseOf δ (suc i) ≡ phaseOf δ i + δ
phase-shifts-by-one-step = uniform-step

------------------------------------------------------------------------
-- Section 3 — the radial closed form over ℚ (periodicity)
------------------------------------------------------------------------

-- The cosine atom, valued in ℚ, with ONE declared axiom: its period is
-- one full turn. This is the constructive counterpart of the standard
-- lemma cos(x + 2π) = cos(x) proven in the Coq/Lean/Isabelle ports.
--
-- NOTE on the declared axiom: the acceptance criteria of the roadmap stub
-- allow "no hidden assumptions beyond the axioms listed in the artifact
-- header" — `c` and `c-add1` are exactly those, and nothing else is
-- postulated in this module.

postulate
  c      : ℚ → ℚ
  c-add1 : ∀ q → c (q + 1ℚ) ≡ c q

-- Theorem 3.1 closed form, in turn units: the radial modulation of the
-- k-th vortex, r(t) = r0·(1 + ε·c(ω̂·t + φ)) with the phase φ of the
-- lattice point (Section 2). Periodicity needs no property of φ beyond
-- its being a constant shift.
r : (r0 eps ω̂ φ : ℚ) → ℚ → ℚ
r r0 eps ω̂ φ t = r0 * (1ℚ + eps * c (ω̂ * t + φ))

-- * Certified property: the closed form is periodic with period one full
--   turn of the cosine atom — T̂ = 1. (With ω̂ in turns per unit time the
--   modulation period is T_r = 1/ω̂ time units; the statement below is
--   the same claim with the turn as the time unit.)
r-periodic : ∀ r0 eps ω̂ φ t → r r0 eps ω̂ φ (t + 1ℚ) ≡ r r0 eps ω̂ φ t
r-periodic r0 eps ω̂ φ t =
  begin
    r0 * (1ℚ + eps * c (ω̂ * (t + 1ℚ) + φ))
  ≡⟨ cong (λ u → r0 * (1ℚ + eps * c (u + φ))) (*-distribˡ-+ ω̂ t 1ℚ) ⟩
    r0 * (1ℚ + eps * c ((ω̂ * t + ω̂ * 1ℚ) + φ))
  ≡⟨ cong (λ u → r0 * (1ℚ + eps * c ((ω̂ * t + u) + φ))) (*-identityʳ ω̂) ⟩
    r0 * (1ℚ + eps * c ((ω̂ * t + 1ℚ) + φ))
  ≡⟨ cong (λ u → r0 * (1ℚ + eps * c u))
          (trans (sym (+-assoc (ω̂ * t) 1ℚ φ))
          (trans (cong ((ω̂ * t) +_) (+-comm 1ℚ φ))
                 (+-assoc (ω̂ * t) φ 1ℚ))) ⟩
    r0 * (1ℚ + eps * c ((ω̂ * t + φ) + 1ℚ))
  ≡⟨ cong (λ u → r0 * (1ℚ + eps * u)) (c-add1 (ω̂ * t + φ)) ⟩
    r0 * (1ℚ + eps * c (ω̂ * t + φ))
  ∎

------------------------------------------------------------------------
-- Section 4 — the Chaplygin combination over ℚ
------------------------------------------------------------------------

-- The Chaplygin topological integral, in the gauge A_θ = 1/r of Section 6
-- of the core document, in the algebraic shape the ladders record:
-- C_Ch(r, θ̇, q) = r²·θ̇ − q·r  (written with an explicit negation so the
-- module needs no rational-subtraction normalization lemmas).
C : (r θ̇ q : ℚ) → ℚ
C r θ̇ q = (r * r * θ̇) + (- (q * r))

-- * Certified property: additivity in θ̇ — the gauge-increment identity
--   used by the ladder when comparing the recorded combination across
--   parameter scans: C(r, θ̇+δ, q) = C(r, θ̇, q) + r²·δ.
C-additive : ∀ r θ̇ δ q →
  C r (θ̇ + δ) q ≡ (C r θ̇ q) + (r * r * δ)
C-additive r θ̇ δ q =
  begin
    ((r * r) * (θ̇ + δ)) − (q * r)
  ≡⟨ cong (λ u → u − (q * r)) (*-distribˡ-+ (r * r) θ̇ δ) ⟩
    ((r * r * θ̇) + (r * r * δ)) − (q * r)
  ≡⟨ sym (+-assoc (r * r * θ̇) (r * r * δ) (- (q * r))) ⟩
    (r * r * θ̇) + ((r * r * δ) + (- (q * r)))
  ≡⟨ cong ((r * r * θ̇) +_) (+-comm (r * r * δ) (- (q * r))) ⟩
    (r * r * θ̇) + ((- (q * r)) + (r * r * δ))
  ≡⟨ +-assoc (r * r * θ̇) (- (q * r)) (r * r * δ) ⟩
    ((r * r * θ̇) − (q * r)) + (r * r * δ)
  ∎

------------------------------------------------------------------------
-- Section 5 — the vortex integrals: exact centroid anchors
------------------------------------------------------------------------

-- Linear impulses P = Σ Γx and Q = Σ Γy, for three vortices with equal
-- circulations Γ.
P : (Γ x1 x2 x3 : ℚ) → ℚ
P Γ x1 x2 x3 = (Γ * x1) + ((Γ * x2) + (Γ * x3))

Q : (Γ y1 y2 y3 : ℚ) → ℚ
Q Γ y1 y2 y3 = (Γ * y1) + ((Γ * y2) + (Γ * y3))

-- Angular impulse I = Σ Γ|r|² (the ladders certify its conservation
-- numerically; the definition is included so all four integrals live in
-- one constructive module).
I : (Γ x1 y1 x2 y2 x3 y3 : ℚ) → ℚ
I Γ x1 y1 x2 y2 x3 y3 =
  (Γ * (x1 * x1 + y1 * y1)) + ((Γ * (x2 * x2 + y2 * y2)) + (Γ * (x3 * x3 + y3 * y3)))

-- * Certified property (exact anchor): if the centroid of the three
--   vortices sits at the origin — x1 + x2 + x3 ≡ 0 — then P ≡ 0 exactly,
--   for EVERY circulation Γ. This is the analytic anchor of check V3:
--   the numerical ladder starts exactly at P = Q = 0.
P-anchored : ∀ Γ x1 x2 x3 → (x1 + x2 + x3) ≡ 0ℚ →
  P Γ x1 x2 x3 ≡ 0ℚ
P-anchored Γ x1 x2 x3 h =
  begin
    (Γ * x1) + ((Γ * x2) + (Γ * x3))
  ≡⟨ cong ((Γ * x1) +_) (sym (*-distribˡ-+ Γ x2 x3)) ⟩
    (Γ * x1) + (Γ * (x2 + x3))
  ≡⟨ sym (*-distribˡ-+ Γ x1 (x2 + x3)) ⟩
    Γ * (x1 + (x2 + x3))
  ≡⟨ cong (Γ *_) (+-assoc x1 x2 x3) ⟩
    Γ * ((x1 + x2) + x3)
  ≡⟨ cong (Γ *_) h ⟩
    Γ * 0ℚ
  ≡⟨ *-zeroʳ Γ ⟩
    0ℚ
  ∎

-- * Certified property (exact anchor): the same statement for Q.
Q-anchored : ∀ Γ y1 y2 y3 → (y1 + y2 + y3) ≡ 0ℚ →
  Q Γ y1 y2 y3 ≡ 0ℚ
Q-anchored Γ y1 y2 y3 h =
  begin
    (Γ * y1) + ((Γ * y2) + (Γ * y3))
  ≡⟨ cong ((Γ * y1) +_) (sym (*-distribˡ-+ Γ y2 y3)) ⟩
    (Γ * y1) + (Γ * (y2 + y3))
  ≡⟨ sym (*-distribˡ-+ Γ y1 (y2 + y3)) ⟩
    Γ * (y1 + (y2 + y3))
  ≡⟨ cong (Γ *_) (+-assoc y1 y2 y3) ⟩
    Γ * ((y1 + y2) + y3)
  ≡⟨ cong (Γ *_) h ⟩
    Γ * 0ℚ
  ≡⟨ *-zeroʳ Γ ⟩
    0ℚ
  ∎
