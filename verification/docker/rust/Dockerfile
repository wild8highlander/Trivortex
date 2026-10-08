FROM rust:1.77
# TRIVORTEX verification — pinned Rust toolchain (milestone M1 numeric twin)
# SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
# SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
WORKDIR /app
COPY rust/ /app/rust/
WORKDIR /app/rust
# the CI-callable check of the M1 acceptance criteria: the numeric twin's
# pinned-reference guard plus the quick ladder, built and run at -O3
RUN cargo test --release
ENTRYPOINT ["sh", "-c", "cargo run --release -- --preset quick --no-menu --lang en"]
