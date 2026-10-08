import Lake
open Lake DSL

/- TRIVORTEX Lean 4 verification package (milestone M1).
   SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
   SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0 -/

package «trivortex» where
  leanOptions := #[⟨`autoImplicit, false⟩]

@[default_target]
lean_lib «Trivortex» where
  -- the artifact is the single file Trivortex.lean at the package root
  roots := #[`Trivortex]

-- Mathlib supplies Real.cos_period, Real.exp_pos, Real.sq_sqrt and the
-- tactic suite (field_simp, positivity, norm_num) used by Trivortex.lean.
-- The Docker image (docker/lean4/Dockerfile) resolves and caches Mathlib;
-- see verification/lean4/README.md for the pinned-revision note.
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "master"
