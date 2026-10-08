# TRIVORTEX verification — C++ port (milestone M3)
# SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
# SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
#
# CMake/CTest port of the verification ladder plus the -O2 benchmark.
#   cmake -S verification/cpp -B verification/cpp/build
#   cmake --build verification/cpp/build -j
#   ctest --test-dir verification/cpp/build --output-on-failure
cmake_minimum_required(VERSION 3.16)
project(trivortex_verify_cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

# The M3 benchmark ladder is compiled at -O2 (registered in the roadmap).
set(CMAKE_CXX_FLAGS_RELEASE "-O2")

add_library(trivortex_core src/verify.cpp)
target_include_directories(trivortex_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src)

# The interactive laboratory binary
add_executable(trivortex-lab src/main.cpp)
target_link_libraries(trivortex-lab PRIVATE trivortex_core)

# The CTest guard: pinned reference values + the quick ladder verdicts
enable_testing()
add_executable(trivortex-tests src/tests.cpp)
target_link_libraries(trivortex-tests PRIVATE trivortex_core)
add_test(NAME trivortex_reference_guard COMMAND trivortex-tests)
