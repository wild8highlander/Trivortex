FROM gcc:13
# TRIVORTEX verification — pinned GCC + CMake toolchain (milestone M3)
# SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
# SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
RUN apt-get update && apt-get install -y cmake make && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY cpp/ /app/cpp/
WORKDIR /app/cpp
# the CI-callable check of the M3 acceptance criteria: the pinned-reference
# CTest guard plus the -O2 benchmark ladder
RUN cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j"$(nproc)"
ENTRYPOINT ["sh", "-c", "ctest --test-dir build --output-on-failure && ./build/trivortex-lab --preset quick --no-menu --out-dir outputs/cpp"]
