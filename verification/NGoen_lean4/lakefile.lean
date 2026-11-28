import Lake
open Lake DSL

/- TRIVORTEX-N Lean 4 verification package (the five-file program: files 1/5..5/5 landed).
   SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
   SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0 -/

package «trivortexn» where
  leanOptions := #[⟨`autoImplicit, false⟩]

@[default_target]
lean_lib «TrivortexN» where
  -- the five-file program of TRIVORTEX-N, each file a self-contained root module
  roots := #[`NGon, `NSide, `NCore, `NRoots, `NFlow]

-- Mathlib is pinned to an exact revision for reproducibility
-- (never rely on a moving target).
-- Pair: lean-toolchain v4.6.0 + mathlib4 @ tag v4.6.0 (2024-06).
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.6.0"
