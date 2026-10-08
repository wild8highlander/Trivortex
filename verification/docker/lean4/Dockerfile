FROM ubuntu:24.04
# TRIVORTEX verification — pinned Lean 4 toolchain (milestone M1)
# SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
# SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl git ca-certificates \
 && rm -rf /var/lib/apt/lists/*
# elan + the pinned toolchain of verification/lean4/lean-toolchain
RUN curl https://elan.lean-lang.org/elan-init.sh -sSf | sh -s -- -y \
 && /root/.elan/bin/elan toolchain install v4.4.0 \
 && /root/.elan/bin/elan default v4.4.0
ENV PATH="/root/.elan/bin:${PATH}"
WORKDIR /app
COPY lean4/ /app/lean4/
WORKDIR /app/lean4
# the CI-callable check of the M1 acceptance criteria: the Mathlib
# formalization builds (Mathlib is resolved and cached at image build time)
RUN lake update && lake exe cache get! && lake build
ENTRYPOINT ["lake", "build"]
