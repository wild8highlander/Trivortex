// SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
// SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
// ===========================================================================
// TRIVORTEX C++ port — the CTest guard.
// The pinned reference values are recomputed from the closed form here
// (pinned, not assumed), mirroring verification/tests/test_trivortex.py and
// the Rust tests. These are the CI-callable checks of the M3 acceptance
// criteria for verification/cpp/.
// ===========================================================================
#include "verify.hpp"

#include <cmath>
#include <cstdio>
#include <cstdlib>

namespace {

using namespace trivortex;

int failures = 0;

void expect_close(const char* what, double got, double expected, double rel) {
    double err = std::fabs(got - expected) / std::fmax(std::fabs(expected), 1.0);
    if (!(err <= rel)) {
        std::printf("FAIL %s: got %.17g, expected %.17g (rel err %.3e > %.0e)\n", what,
                    got, expected, err, rel);
        ++failures;
    } else {
        std::printf("  ok %s = %.17g\n", what, got);
    }
}

void expect_true(const char* what, bool cond) {
    if (!cond) {
        std::printf("FAIL %s\n", what);
        ++failures;
    } else {
        std::printf("  ok %s\n", what);
    }
}

double field(const Check& c, const char* name) {
    for (const auto& [k, v] : c) {
        if (k == name && v->kind == Val::Kind::Number) return v->num;
    }
    return std::nan("");
}

}  // namespace

int main() {
    std::printf("TRIVORTEX C++ guard — pinned reference values\n");

    // -- Theorem 3.1 analytic pins (mirroring test_trivortex.py) ------------
    expect_close("omega(C=1, T=2pi)",
                 analytical_frequency(1.0, 2.0 * PI),
                 1.3748022274393588, 1e-12);
    expect_close("eps(C=1)", analytical_amplitude(1.0),
                 1.0 / (std::exp(1.0 / PI) - 1.0), 1e-15);
    expect_true("eps guard (C<=0.01) returns 1", analytical_amplitude(0.005) == 1.0);

    double omega_ref = analytical_frequency(1.0, 2.0 * PI);
    double t_r = 2.0 * PI / omega_ref;
    for (int k = 0; k < 3; ++k) {
        double res = std::fabs(analytical_radius(1.234 + t_r, 1.0, 2.0 * PI, k) -
                               analytical_radius(1.234, 1.0, 2.0 * PI, k));
        expect_true("closed-form periodicity (k)",
                    res <= 1e-12);
    }

    // C_Ch formula shape: r^2*theta_dot - q*r with A_theta = 1/r
    expect_close("chaplygin shape", compute_chaplygin(0.5, 2.0, 1.0, 0.0),
                 0.5 * 0.5 * 2.0 - 1.0 * 0.5, 1e-15);

    // -- Lagrange analytic pins ---------------------------------------------
    expect_close("omega_Lagrange(1,1)", lagrange_omega(1.0, 1.0), 3.0 / (2.0 * PI), 1e-15);
    expect_close("omega_Lagrange(2,3)", lagrange_omega(2.0, 3.0), 6.0 / (2.0 * PI * 9.0),
                 1e-15);

    auto init = equilateral_initial(1.0);
    auto sides = side_lengths(init);
    expect_true("equilateral sides", std::fabs(sides[0] - 1.0) <= 1e-14 &&
                                         std::fabs(sides[1] - 1.0) <= 1e-14 &&
                                         std::fabs(sides[2] - 1.0) <= 1e-14);

    // pair rigid rotation of the RHS
    std::vector<double> st = {1.0, 0.0, -1.0, 0.0};
    std::vector<double> g = {1.0, 1.0};
    auto d = vortex_rhs(st, g);
    expect_true("pair antisymmetry dx", std::fabs(d[0]) <= 1e-15 && std::fabs(d[2]) <= 1e-15);
    expect_close("pair dy0", d[1], 0.5 / (2.0 * PI), 1e-14);
    expect_close("pair dy1", d[3], -0.5 / (2.0 * PI), 1e-14);

    // -- the quick ladder: verdicts inside the registered bands -------------
    const Preset* p = find_preset("quick");
    LadderRun run = run_ladder(*p, "trivortex-verification-cpp");
    std::printf("quick ladder: %d/%d checks passed (%.2fs)\n", run.all_passed ? 4 : 0, 4,
                run.wall_time_s);
    expect_true("V1 quick passed", has_passed(run.checks[0]));
    expect_true("V2 quick passed", has_passed(run.checks[1]));
    expect_true("V3 quick passed", has_passed(run.checks[2]));
    expect_true("V4 quick passed", has_passed(run.checks[3]));
    expect_close("V2 omega_analytic pin", field(run.checks[1], "omega_analytic"),
                 0.477464829275686, 1e-12);
    expect_true("V1 separation band", field(run.checks[0], "angular_separation_error") <= 1e-12);
    expect_true("V2 shape band", field(run.checks[1], "shape_drift") <= 1e-10);
    expect_true("V2 omega band", field(run.checks[1], "omega_relative_error") <= 1e-6);
    expect_true("V3 drift band", field(run.checks[2], "worst_drift") <= 1e-10);
    expect_true("V4 drift band", field(run.checks[3], "worst_drift") <= 1e-10);
    expect_true("benchmark measured", run.rhs_per_s > 0.0);

    // -- JSON serialization smoke -------------------------------------------
    std::string json = val_to_json(vmap(run.report), 0);
    expect_true("json contains suite", json.find("\"suite\"") != std::string::npos);
    expect_true("json contains all_passed", json.find("\"all_passed\"") != std::string::npos);
    expect_true("json contains benchmark", json.find("\"benchmark_rhs_per_s\"") != std::string::npos);

    if (failures == 0) {
        std::printf("ALL C++ GUARD TESTS PASSED\n");
        return 0;
    }
    std::printf("%d GUARD TEST(S) FAILED\n", failures);
    return 1;
}
