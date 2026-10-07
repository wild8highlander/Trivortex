FROM rust:1.75
WORKDIR /app
COPY rust/ /app/rust/
WORKDIR /app/rust
RUN cargo build --release
ENTRYPOINT ["sh", "-c", "for s in section1_correction_b section2_preprint section3_ab_cloud section4_kdv section5_klein_attractor section6_riemann_zeros; do ./target/release/verify_$s; done"]
