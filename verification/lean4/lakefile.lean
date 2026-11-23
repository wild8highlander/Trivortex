import Lake
open Lake DSL

/- TRIVORTEX Lean 4 verification package (milestone M4, v2.0).
   SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
   SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0 -/

package «trivortex» where
  leanOptions := #[⟨`autoImplicit, false⟩]

@[default_target]
lean_lib «Trivortex» where
  -- the artifact is the single file Trivortex.lean at the package root
  roots := #[`Trivortex]

-- Mathlib is pinned to an exact revision for reproducibility
-- (verification/README.md §8: never rely on a moving target).
-- Pair: lean-toolchain v4.6.0 + mathlib4 @ tag v4.6.0 (2024-06).
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.6.0"
