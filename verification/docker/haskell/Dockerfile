FROM haskell:9.4-slim
# TRIVORTEX verification — pinned GHC + cabal toolchain (milestone M3)
# SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
# SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
WORKDIR /app
COPY haskell/ /app/haskell/
WORKDIR /app/haskell
# the CI-callable check of the M3 acceptance criteria: the Double ladder's
# pinned-reference guard plus the exact ℚ(√3) anchor identities
RUN cabal update && cabal build all && cabal test trivortex-guard
ENTRYPOINT ["sh", "-c", "echo 0 | cabal run trivortex-lab"]
