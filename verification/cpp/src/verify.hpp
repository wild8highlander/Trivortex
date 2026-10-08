// SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
// SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
// ===========================================================================
// TRIVORTEX — C++ NUMERIC TWIN OF THE VERIFICATION LADDER V1–V4
// ===========================================================================
// A line-for-line floating-point port of verification/trivortex/python/
// verify.py (M0 release) into dependency-free C++17. It re-implements the
// three fixed objects from the published formulas and nothing else:
//
//   1. Theorem 3.1 closed form
//        r_k(t)     = sqrt(C_Ch) * (1 + eps * cos(omega*t + 2*pi*k/3))
//        omega      = (2*pi/T) * exp(C_Ch/pi)
//        eps        = 1 / (exp(C_Ch/pi) - 1)
//   2. The Chaplygin topological integral  C_Ch = r^2 (theta_dot - q*A_theta)
//   3. The vortex integrals H, P, Q, I integrated with classical RK4.
//
// INDEPENDENCE CONTRACT: shares no code with code/trivortex_core*.py — only
// the mathematics and the numbers. This is the M3 benchmark ladder: the same
// four checks the Python and Rust ladders run, timed at -O2.
//
// Author: Isaev Iskhak Khamzatovich (repository owner)
// Year: 2026
// ===========================================================================
#pragma once

#include <array>
#include <algorithm>
#include <cstdint>
#include <cstddef>
#include <memory>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace trivortex {

inline constexpr double PI = 3.14159265358979323846;

// --- presets (mirror of verify.py) -----------------------------------------
struct Preset {
    const char* name;
    int rotations;
    int steps_per_period;
    int n_points_cch;
};

inline const Preset PRESETS[3] = {
    {"quick", 2, 2000, 200},
    {"default", 5, 4000, 1000},
    {"full", 20, 8000, 2000},
};

inline const Preset* find_preset(const std::string& name) {
    for (const auto& p : PRESETS) {
        if (name == p.name) return &p;
    }
    return nullptr;
}

// --- tolerance bands (registered in verification/README.md §6) --------------
inline constexpr double TOL_CHAPLYGIN_DRIFT = 1e-12;
inline constexpr double TOL_ANGULAR_SEP = 1e-12;
inline constexpr double TOL_SHAPE_DRIFT = 1e-10;
inline constexpr double TOL_OMEGA_REL_ERR = 1e-6;
inline constexpr double TOL_INVARIANT_DRIFT = 1e-10;

// --- Section A: analytic layer (Theorem 3.1) --------------------------------

/// omega = (2*pi/T) * exp(C_Ch/pi) — Theorem 3.1.
double analytical_frequency(double c_ch, double t_period);

/// eps = 1/(exp(C_Ch/pi) - 1); the document's guard returns 1 for C_Ch<=0.01.
double analytical_amplitude(double c_ch);

/// r_k(t) = sqrt(C_Ch) * (1 + eps*cos(omega*t + 2*pi*k/3)), k = 0,1,2.
double analytical_radius(double t, double c_ch, double t_period, int k);

/// C_Ch = r^2 * (theta_dot - q*A_theta) with the gauge A_theta = 1/r.
double compute_chaplygin(double r, double theta_dot, double q, double a_theta);

/// Python-style modulo: result in [0, m) for m > 0.
double python_mod(double x, double m);

/// Python-style round(): half-to-even (CPython's banker's rounding).
double py_round_half_even(double x);

// --- Section B: numerical layer (Kirchhoff dynamics, RK4) -------------------

/// Kirchhoff right-hand side; state = flat [x0,y0,x1,y1,...].
std::vector<double> vortex_rhs(const std::vector<double>& state,
                               const std::vector<double>& gamma);

/// One classical RK4 step.
std::vector<double> rk4_step(const std::vector<double>& state,
                             const std::vector<double>& gamma, double dt);

/// H, P, Q, I — the classical (Chaplygin-type) vortex integrals.
std::array<double, 4> invariants(const std::vector<double>& state,
                                 const std::vector<double>& gamma);

/// Three equal vortices on an equilateral triangle of side a.
std::vector<double> equilateral_initial(double a);

/// omega = 3*Gamma/(2*pi*a^2) — the point-vortex Lagrange solution.
double lagrange_omega(double gamma, double a);

/// Side lengths (01, 12, 20) of the triangle in `xy`.
std::array<double, 3> side_lengths(const std::vector<double>& xy);

// --- JSON protocol value tree ------------------------------------------------

struct Val;
using ValPtr = std::shared_ptr<Val>;

struct Val {
    enum class Kind { Number, String, Bool, List, Map } kind;
    double num = 0.0;
    bool b = false;
    std::string str;
    std::vector<ValPtr> list;
    std::vector<std::pair<std::string, ValPtr>> map;
};

ValPtr vnum(double x);
ValPtr vstr(const std::string& s);
ValPtr vbool(bool b);
ValPtr vlist(std::vector<ValPtr> items);
ValPtr vmap(std::vector<std::pair<std::string, ValPtr>> fields);

std::string val_to_json(const ValPtr& v, int indent);

// --- the four checks ---------------------------------------------------------

using Check = std::vector<std::pair<std::string, ValPtr>>;

Check check_v1_theorem31(double c_ch, double t_period, int n_points);

/// V2; when `track` is true, samples ~400 trajectory snapshots.
std::tuple<Check, std::vector<std::pair<double, std::array<double, 6>>>>
check_v2_lagrange_rotation(double gamma, double a, int rotations,
                           int steps_per_period, bool track);

Check check_v3_invariants(double gamma, double a, int rotations,
                          int steps_per_period);

Check check_v4_robustness(const std::array<double, 3>& gammas, double a,
                          int rotations, int steps_per_period);

bool has_passed(const Check& c);

// --- the ladder run ----------------------------------------------------------

struct LadderRun {
    Check report;
    std::vector<Check> checks;
    bool all_passed;
    double wall_time_s;
    /// RK4 right-hand-side evaluations per second (the M3 benchmark metric).
    double rhs_per_s;
};

LadderRun run_ladder(const Preset& p, const std::string& suite);

/// Raw benchmark: RK4 steps per second for the Lagrange problem at -O2.
std::tuple<double, long long> benchmark_rk4(int rotations, int steps_per_period);

// --- i18n strings (EN / RU) ---------------------------------------------------

enum class Lang { En, Ru };
Lang lang_from_code(const std::string& code);
const char* tr(Lang l, const char* en, const char* ru);

// --- report / data / plot writers ---------------------------------------------

std::string json_escape(const std::string& s);
std::string json_float(double v);
std::string utc_now_iso();
std::string utc_stamp();
bool write_text(const std::string& path, const std::string& text);
bool write_csv(const std::string& path, const std::vector<std::string>& header,
               const std::vector<std::vector<double>>& rows);

struct Series {
    std::string label;
    std::vector<std::pair<double, double>> points;
    std::string color;
};

bool svg_line_plot(const std::string& path, const std::string& title,
                   const std::string& x_label, const std::string& y_label,
                   const std::vector<Series>& series);

const char* palette_color(int i);

}  // namespace trivortex
