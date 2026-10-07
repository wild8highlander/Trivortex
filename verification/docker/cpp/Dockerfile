FROM gcc:13
RUN apt-get update && apt-get install -y cmake make && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY cpp/ /app/cpp/
WORKDIR /app/cpp
RUN mkdir -p build && cd build && cmake .. && make -j$(nproc)
ENTRYPOINT ["sh", "-c", "cd build && for s in section1_correction_b section2_preprint section3_ab_cloud section4_kdv section5_klein_attractor section6_riemann_zeros; do ./verify_$s; done"]
