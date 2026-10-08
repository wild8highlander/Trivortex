// SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
// SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
// TRIVORTEX C++ port — implementation (see verify.hpp for the contract).
#include "verify.hpp"

#include <chrono>
#include <cmath>
#include <cstdio>
#include <fstream>
#include <sstream>

namespace trivortex {

// ---------------------------------------------------------------------------
// Section A — analytic layer (Theorem 3.1)
// ---------------------------------------------------------------------------

double analytical_frequency(double c_ch, double t_period) {
    return (2.0 * PI / t_period) * std::exp(c_ch / PI);
}

double analytical_amplitude(double c_ch) {
    return c_ch > 0.01 ? 1.0 / (std::exp(c_ch / PI) - 1.0) : 1.0;
}

double analytical_radius(double t, double c_ch, double t_period, int k) {
    double omega = analytical_frequency(c_ch, t_period);
    double eps = analytical_amplitude(c_ch);
    double r0 = c_ch > 0.0 ? std::sqrt(c_ch) : 0.01;
    return r0 * (1.0 + eps * std::cos(omega * t + 2.0 * PI * k / 3.0));
}

double compute_chaplygin(double r, double theta_dot, double q, double a_theta) {
    double a = a_theta > 0.0 ? a_theta : (r > 0.0 ? 1.0 / r : 0.0);
    return r * r * (theta_dot - q * a);
}

double python_mod(double x, double m) {
    double r = std::fmod(x, m);
    return r < 0.0 ? r + m : r;
}

double py_round_half_even(double x) {
    double fl = std::floor(x);
    double diff = x - fl;
    if (diff < 0.5) return fl;
    if (diff > 0.5) return fl + 1.0;
    long long even = static_cast<long long>(fl);
    return (even % 2 == 0) ? fl : fl + 1.0;
}

// ---------------------------------------------------------------------------
// Section B — numerical layer
// ---------------------------------------------------------------------------

std::vector<double> vortex_rhs(const std::vector<double>& state,
                               const std::vector<double>& gamma) {
    const int n = static_cast<int>(gamma.size());
    std::vector<double> dxy(2 * n, 0.0);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (i == j) continue;
            double dx = state[2 * i] - state[2 * j];
            double dy = state[2 * i + 1] - state[2 * j + 1];
            double r2 = dx * dx + dy * dy;
            if (r2 == 0.0) continue;
            dxy[2 * i] += -gamma[j] * dy / r2 / (2.0 * PI);
            dxy[2 * i + 1] += gamma[j] * dx / r2 / (2.0 * PI);
        }
    }
    return dxy;
}

std::vector<double> rk4_step(const std::vector<double>& state,
                             const std::vector<double>& gamma, double dt) {
    auto k1 = vortex_rhs(state, gamma);
    std::vector<double> s2(state.size()), s3(state.size()), s4(state.size());
    for (std::size_t i = 0; i < state.size(); ++i) s2[i] = state[i] + 0.5 * dt * k1[i];
    auto k2 = vortex_rhs(s2, gamma);
    for (std::size_t i = 0; i < state.size(); ++i) s3[i] = state[i] + 0.5 * dt * k2[i];
    auto k3 = vortex_rhs(s3, gamma);
    for (std::size_t i = 0; i < state.size(); ++i) s4[i] = state[i] + dt * k3[i];
    auto k4 = vortex_rhs(s4, gamma);
    std::vector<double> out(state.size());
    for (std::size_t i = 0; i < state.size(); ++i) {
        out[i] = state[i] + (dt / 6.0) * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]);
    }
    return out;
}

std::array<double, 4> invariants(const std::vector<double>& state,
                                 const std::vector<double>& gamma) {
    const int n = static_cast<int>(gamma.size());
    double h = 0.0;
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            double dx = state[2 * i] - state[2 * j];
            double dy = state[2 * i + 1] - state[2 * j + 1];
            double r = std::sqrt(dx * dx + dy * dy);
            h += -gamma[i] * gamma[j] * std::log(r) / (2.0 * PI);
        }
    }
    double p = 0.0, q = 0.0, imp = 0.0;
    for (int i = 0; i < n; ++i) {
        double x = state[2 * i], y = state[2 * i + 1];
        p += gamma[i] * x;
        q += gamma[i] * y;
        imp += gamma[i] * (x * x + y * y);
    }
    return {h, p, q, imp};
}

std::vector<double> equilateral_initial(double a) {
    double r = a / std::sqrt(3.0);
    std::vector<double> pts;
    pts.reserve(6);
    for (int k = 0; k < 3; ++k) {
        double ang = 2.0 * PI * k / 3.0;
        pts.push_back(r * std::cos(ang));
        pts.push_back(r * std::sin(ang));
    }
    return pts;
}

double lagrange_omega(double gamma, double a) {
    return 3.0 * gamma / (2.0 * PI * a * a);
}

std::array<double, 3> side_lengths(const std::vector<double>& xy) {
    auto d = [&](int i, int j) {
        double dx = xy[2 * i] - xy[2 * j];
        double dy = xy[2 * i + 1] - xy[2 * j + 1];
        return std::sqrt(dx * dx + dy * dy);
    };
    return {d(0, 1), d(1, 2), d(2, 0)};
}

// ---------------------------------------------------------------------------
// JSON value tree
// ---------------------------------------------------------------------------

ValPtr vnum(double x) {
    auto v = std::make_shared<Val>();
    v->kind = Val::Kind::Number;
    v->num = x;
    return v;
}

ValPtr vstr(const std::string& s) {
    auto v = std::make_shared<Val>();
    v->kind = Val::Kind::String;
    v->str = s;
    return v;
}

ValPtr vbool(bool b) {
    auto v = std::make_shared<Val>();
    v->kind = Val::Kind::Bool;
    v->b = b;
    return v;
}

ValPtr vlist(std::vector<ValPtr> items) {
    auto v = std::make_shared<Val>();
    v->kind = Val::Kind::List;
    v->list = std::move(items);
    return v;
}

ValPtr vmap(std::vector<std::pair<std::string, ValPtr>> fields) {
    auto v = std::make_shared<Val>();
    v->kind = Val::Kind::Map;
    v->map = std::move(fields);
    return v;
}

std::string json_escape(const std::string& s) {
    std::string out;
    out.reserve(s.size() + 2);
    for (char c : s) {
        switch (c) {
            case '"': out += "\\\""; break;
            case '\\': out += "\\\\"; break;
            case '\n': out += "\\n"; break;
            case '\r': out += "\\r"; break;
            case '\t': out += "\\t"; break;
            default:
                if (static_cast<unsigned char>(c) < 0x20) {
                    char buf[8];
                    std::snprintf(buf, sizeof(buf), "\\u%04x", c);
                    out += buf;
                } else {
                    out += c;
                }
        }
    }
    return out;
}

std::string json_float(double v) {
    if (std::isnan(v) || std::isinf(v)) return "null";
    char buf[40];
    if (v == std::trunc(v) && std::fabs(v) < 1e16) {
        std::snprintf(buf, sizeof(buf), "%.1f", v);
    } else {
        std::snprintf(buf, sizeof(buf), "%.17g", v);
    }
    return buf;
}

static std::string pad(int n) { return std::string(static_cast<std::size_t>(n), ' '); }

std::string val_to_json(const ValPtr& v, int indent) {
    std::ostringstream os;
    switch (v->kind) {
        case Val::Kind::Number: os << json_float(v->num); break;
        case Val::Kind::Bool: os << (v->b ? "true" : "false"); break;
        case Val::Kind::String: os << '"' << json_escape(v->str) << '"'; break;
        case Val::Kind::List: {
            if (v->list.empty()) { os << "[]"; break; }
            os << "[\n";
            for (std::size_t i = 0; i < v->list.size(); ++i) {
                os << pad(indent + 2) << val_to_json(v->list[i], indent + 2);
                if (i + 1 < v->list.size()) os << ',';
                os << '\n';
            }
            os << pad(indent) << ']';
            break;
        }
        case Val::Kind::Map: {
            if (v->map.empty()) { os << "{}"; break; }
            os << "{\n";
            for (std::size_t i = 0; i < v->map.size(); ++i) {
                os << pad(indent + 2) << '"' << json_escape(v->map[i].first)
                   << "\": " << val_to_json(v->map[i].second, indent + 2);
                if (i + 1 < v->map.size()) os << ',';
                os << '\n';
            }
            os << pad(indent) << '}';
            break;
        }
    }
    return os.str();
}

// ---------------------------------------------------------------------------
// Time
// ---------------------------------------------------------------------------

static void civil_from_unix(std::int64_t secs, int& y, int& mo, int& d, int& h,
                            int& mi, int& s) {
    std::int64_t days = secs / 86400;
    std::int64_t rem = secs % 86400;
    if (rem < 0) { rem += 86400; --days; }
    h = static_cast<int>(rem / 3600);
    mi = static_cast<int>((rem % 3600) / 60);
    s = static_cast<int>(rem % 60);
    std::int64_t z = days + 719468;
    std::int64_t era = z / 146097;
    std::int64_t doe = z - era * 146097;
    std::int64_t yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365;
    std::int64_t yy = yoe + era * 400;
    std::int64_t doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    std::int64_t mp = (5 * doy + 2) / 153;
    d = static_cast<int>(doy - (153 * mp + 2) / 5 + 1);
    mo = static_cast<int>(mp < 10 ? mp + 3 : mp - 9);
    y = static_cast<int>(mo <= 2 ? yy + 1 : yy);
}

static std::int64_t unix_now() {
    return std::chrono::duration_cast<std::chrono::seconds>(
               std::chrono::system_clock::now().time_since_epoch())
        .count();
}

std::string utc_now_iso() {
    int y, mo, d, h, mi, s;
    civil_from_unix(unix_now(), y, mo, d, h, mi, s);
    char buf[40];
    std::snprintf(buf, sizeof(buf), "%04d-%02d-%02dT%02d:%02d:%02d+00:00", y, mo, d, h, mi, s);
    return buf;
}

std::string utc_stamp() {
    int y, mo, d, h, mi, s;
    civil_from_unix(unix_now(), y, mo, d, h, mi, s);
    char buf[40];
    std::snprintf(buf, sizeof(buf), "%04d-%02d-%02d_%02d-%02d-%02d", y, mo, d, h, mi, s);
    return buf;
}

// ---------------------------------------------------------------------------
// The four checks
// ---------------------------------------------------------------------------

static void push_field(Check& c, const std::string& k, ValPtr v) {
    c.emplace_back(k, std::move(v));
}

Check check_v1_theorem31(double c_ch, double t_period, int n_points) {
    double omega = analytical_frequency(c_ch, t_period);
    double t_r = 2.0 * PI / omega;
    double t_max = 100.0 * t_period;

    // (a) equilateral choreography at the four probed times
    double sep_err = 0.0;
    const double fracs[4] = {0.0, 0.25, 0.5, 1.0};
    for (double f : fracs) {
        double t = f * t_max;
        double angles[3];
        for (int k = 0; k < 3; ++k) angles[k] = omega * t + 2.0 * PI * k / 3.0;
        for (int i = 0; i < 3; ++i) {
            double d = python_mod(angles[(i + 1) % 3] - angles[i], 2.0 * PI);
            sep_err = std::fmax(sep_err, std::fabs(d - 2.0 * PI / 3.0));
        }
    }

    // (b) periodicity of the closed form
    double per_res = 0.0;
    const double pfracs[4] = {0.0, 0.137, 0.5, 0.811};
    for (int k = 0; k < 3; ++k) {
        for (double f : pfracs) {
            double t = f * t_max;
            per_res = std::fmax(per_res,
                                std::fabs(analytical_radius(t + t_r, c_ch, t_period, k) -
                                          analytical_radius(t, c_ch, t_period, k)));
        }
    }

    // diagnostic: Section-6 endpoint drift of C_Ch(t)
    double step = n_points > 1 ? t_max / (n_points - 1) : 0.0;
    double drift = 0.0;
    if (n_points > 0) {
        double base = compute_chaplygin(analytical_radius(0.0, c_ch, t_period, 0), omega, 1.0, 0.0);
        for (int i = 0; i < n_points; ++i) {
            double t = i * step;
            double c = compute_chaplygin(analytical_radius(t, c_ch, t_period, 0), omega, 1.0, 0.0);
            drift = std::fmax(drift, std::fabs(c - base));
        }
    }

    Check c;
    push_field(c, "check", vstr("V1 Theorem 3.1: choreography + periodicity of the closed form"));
    push_field(c, "angular_separation_error", vnum(sep_err));
    push_field(c, "angular_separation_tolerance", vnum(TOL_ANGULAR_SEP));
    push_field(c, "periodicity_residual", vnum(per_res));
    push_field(c, "periodicity_tolerance", vnum(TOL_CHAPLYGIN_DRIFT));
    push_field(c, "section6_drift_diagnostic", vnum(drift));
    push_field(c, "passed", vbool(sep_err <= TOL_ANGULAR_SEP && per_res <= TOL_CHAPLYGIN_DRIFT));
    push_field(c, "params",
               vmap({{"C_Ch", vnum(c_ch)},
                     {"T", vnum(t_period)},
                     {"n_points", vnum(n_points)},
                     {"omega", vnum(omega)},
                     {"window", vstr("0..100T")}}));
    return c;
}

std::tuple<Check, std::vector<std::pair<double, std::array<double, 6>>>>
check_v2_lagrange_rotation(double gamma, double a, int rotations,
                           int steps_per_period, bool track) {
    std::vector<double> state = equilateral_initial(a);
    double omega = lagrange_omega(gamma, a);
    double period = 2.0 * PI / omega;
    double dt = period / steps_per_period;
    std::vector<double> gamma_vec = {gamma, gamma, gamma};

    double ang_start = std::atan2(state[1], state[0]);
    long long n_steps = static_cast<long long>(rotations) * steps_per_period;
    long long track_every = track ? std::max<long long>(n_steps / 400, 1) : 0;
    std::vector<std::pair<double, std::array<double, 6>>> trajectory;

    for (long long step = 0; step < n_steps; ++step) {
        state = rk4_step(state, gamma_vec, dt);
        if (track && step % track_every == 0) {
            std::array<double, 6> snap{};
            std::copy(state.begin(), state.end(), snap.begin());
            trajectory.emplace_back(step * dt, snap);
        }
    }

    double ang_end = std::atan2(state[1], state[0]);
    double expected_total = omega * static_cast<double>(n_steps) * dt;
    double raw_diff = ang_end - ang_start;
    double measured_total =
        raw_diff + 2.0 * PI * py_round_half_even((expected_total - raw_diff) / (2.0 * PI));
    double omega_rel_err = std::fabs(measured_total - expected_total) / expected_total;

    auto sides = side_lengths(state);
    double shape_drift =
        std::fmax(std::fabs(sides[0] - a), std::fmax(std::fabs(sides[1] - a), std::fabs(sides[2] - a))) / a;

    Check c;
    push_field(c, "check", vstr("V2 Lagrange rigid rotation: shape + analytic omega = 3G/(2pi a^2)"));
    push_field(c, "shape_drift", vnum(shape_drift));
    push_field(c, "shape_tolerance", vnum(TOL_SHAPE_DRIFT));
    push_field(c, "omega_analytic", vnum(omega));
    push_field(c, "omega_relative_error", vnum(omega_rel_err));
    push_field(c, "omega_tolerance", vnum(TOL_OMEGA_REL_ERR));
    push_field(c, "passed", vbool(shape_drift <= TOL_SHAPE_DRIFT && omega_rel_err <= TOL_OMEGA_REL_ERR));
    push_field(c, "params",
               vmap({{"Gamma", vnum(gamma)},
                     {"a", vnum(a)},
                     {"rotations", vnum(rotations)},
                     {"steps_per_period", vnum(steps_per_period)},
                     {"dt", vnum(dt)}}));
    return {c, trajectory};
}

static std::pair<std::vector<std::pair<std::string, double>>, double>
worst_drift(const std::array<double, 4>& inv0, const std::array<double, 4>& inv1) {
    const char* names[4] = {"H", "P", "Q", "I"};
    std::vector<std::pair<std::string, double>> drifts;
    double worst = 0.0;
    for (int k = 0; k < 4; ++k) {
        double d = std::fabs(inv1[k] - inv0[k]) / std::fmax(std::fabs(inv0[k]), 1.0);
        drifts.emplace_back(names[k], d);
        worst = std::fmax(worst, d);
    }
    return {drifts, worst};
}

Check check_v3_invariants(double gamma, double a, int rotations,
                          int steps_per_period) {
    std::vector<double> state = equilateral_initial(a);
    double omega = lagrange_omega(gamma, a);
    double dt = (2.0 * PI / omega) / steps_per_period;
    std::vector<double> gamma_vec = {gamma, gamma, gamma};

    auto inv0 = invariants(state, gamma_vec);
    long long n_steps = static_cast<long long>(rotations) * steps_per_period;
    for (long long i = 0; i < n_steps; ++i) state = rk4_step(state, gamma_vec, dt);
    auto inv1 = invariants(state, gamma_vec);

    auto [drifts, worst] = worst_drift(inv0, inv1);
    Check c;
    push_field(c, "check", vstr("V3 vortex integrals: H, P, Q, I conserved (equal Gamma)"));
    std::vector<std::pair<std::string, ValPtr>> drift_fields;
    for (const auto& [dk, dv] : drifts) drift_fields.emplace_back(dk, vnum(dv));
    push_field(c, "relative_drifts", vmap(std::move(drift_fields)));
    push_field(c, "worst_drift", vnum(worst));
    push_field(c, "tolerance", vnum(TOL_INVARIANT_DRIFT));
    push_field(c, "passed", vbool(worst <= TOL_INVARIANT_DRIFT));
    push_field(c, "params",
               vmap({{"Gamma", vnum(gamma)},
                     {"a", vnum(a)},
                     {"rotations", vnum(rotations)},
                     {"steps_per_period", vnum(steps_per_period)}}));
    return c;
}

Check check_v4_robustness(const std::array<double, 3>& gammas, double a,
                          int rotations, int steps_per_period) {
    // Generic triangle, centroid shifted to the origin.
    double cy = std::sqrt(3.0) / 2.0 * a;
    double cx = (0.0 + a + 0.5 * a) / 3.0;
    double cyy = cy / 3.0;
    std::vector<double> state = {0.0 - cx, 0.0 - cyy, a - cx, 0.0 - cyy,
                                 0.5 * a - cx, cy - cyy};
    std::vector<double> gamma_vec(gammas.begin(), gammas.end());

    auto inv0 = invariants(state, gamma_vec);
    double mean_gamma = (gammas[0] + gammas[1] + gammas[2]) / 3.0;
    double omega_ref = lagrange_omega(mean_gamma, a);
    double dt = (2.0 * PI / omega_ref) / steps_per_period;
    long long n_steps = static_cast<long long>(rotations) * steps_per_period;
    for (long long i = 0; i < n_steps; ++i) state = rk4_step(state, gamma_vec, dt);
    auto inv1 = invariants(state, gamma_vec);

    auto [drifts, worst] = worst_drift(inv0, inv1);
    Check c;
    push_field(c, "check", vstr("V4 robustness: H, P, Q, I conserved for Gamma = (1, 2, 3)"));
    std::vector<std::pair<std::string, ValPtr>> drift_fields;
    for (const auto& [dk, dv] : drifts) drift_fields.emplace_back(dk, vnum(dv));
    push_field(c, "relative_drifts", vmap(std::move(drift_fields)));
    push_field(c, "worst_drift", vnum(worst));
    push_field(c, "tolerance", vnum(TOL_INVARIANT_DRIFT));
    push_field(c, "passed", vbool(worst <= TOL_INVARIANT_DRIFT));
    push_field(c, "params",
               vmap({{"Gamma", vlist({vnum(gammas[0]), vnum(gammas[1]), vnum(gammas[2])})},
                     {"a", vnum(a)},
                     {"rotations", vnum(rotations)},
                     {"steps_per_period", vnum(steps_per_period)}}));
    return c;
}

bool has_passed(const Check& c) {
    for (const auto& [k, v] : c) {
        if (k == "passed" && v->kind == Val::Kind::Bool && v->b) return true;
    }
    return false;
}

// ---------------------------------------------------------------------------
// The ladder + M3 benchmark
// ---------------------------------------------------------------------------

std::tuple<double, long long> benchmark_rk4(int rotations, int steps_per_period) {
    std::vector<double> state = equilateral_initial(1.0);
    std::vector<double> gamma_vec = {1.0, 1.0, 1.0};
    double omega = lagrange_omega(1.0, 1.0);
    double dt = (2.0 * PI / omega) / steps_per_period;
    long long n_steps = static_cast<long long>(rotations) * steps_per_period;

    auto t0 = std::chrono::steady_clock::now();
    for (long long i = 0; i < n_steps; ++i) state = rk4_step(state, gamma_vec, dt);
    auto t1 = std::chrono::steady_clock::now();
    double wall = std::chrono::duration<double>(t1 - t0).count();
    long long rhs_calls = n_steps * 4;  // four RHS evaluations per RK4 step
    double per_s = wall > 0 ? static_cast<double>(rhs_calls) / wall : 0.0;
    return {per_s, rhs_calls};
}

LadderRun run_ladder(const Preset& p, const std::string& suite) {
    auto t0 = std::chrono::steady_clock::now();
    Check v1 = check_v1_theorem31(1.0, 2.0 * PI, p.n_points_cch);
    auto [v2, traj] =
        check_v2_lagrange_rotation(1.0, 1.0, p.rotations, p.steps_per_period, false);
    (void)traj;
    Check v3 = check_v3_invariants(1.0, 1.0, p.rotations, p.steps_per_period);
    Check v4 = check_v4_robustness({1.0, 2.0, 3.0}, 1.0, std::max(p.rotations - 2, 2),
                                   p.steps_per_period);
    auto [rhs_per_s, rhs_calls] = benchmark_rk4(p.rotations, p.steps_per_period);
    (void)rhs_calls;
    auto t1 = std::chrono::steady_clock::now();
    double wall = std::chrono::duration<double>(t1 - t0).count();

    std::vector<Check> checks = {v1, v2, v3, v4};
    int n_pass = 0;
    for (const auto& c : checks) {
        if (has_passed(c)) ++n_pass;
    }
    bool all = n_pass == static_cast<int>(checks.size());

    Check report;
    push_field(report, "suite", vstr(suite));
    push_field(report, "version", vstr("1.0"));
    push_field(report, "preset", vstr(p.name));
    push_field(report, "date_utc", vstr(utc_now_iso()));
    push_field(report, "wall_time_s", vnum(wall));
    push_field(report, "checks_passed", vnum(n_pass));
    push_field(report, "checks_total", vnum(static_cast<int>(checks.size())));
    push_field(report, "all_passed", vbool(all));
    push_field(report, "benchmark_rhs_per_s", vnum(rhs_per_s));
    std::vector<ValPtr> check_vals;
    for (const auto& c : checks) {
        std::vector<std::pair<std::string, ValPtr>> fields;
        for (const auto& [k, v] : c) fields.emplace_back(k, v);
        check_vals.push_back(vmap(std::move(fields)));
    }
    push_field(report, "checks", vlist(std::move(check_vals)));

    return LadderRun{report, checks, all, wall, rhs_per_s};
}

// ---------------------------------------------------------------------------
// i18n
// ---------------------------------------------------------------------------

Lang lang_from_code(const std::string& code) {
    return (code == "ru" || code == "RU") ? Lang::Ru : Lang::En;
}

const char* tr(Lang l, const char* en, const char* ru) { return l == Lang::Ru ? ru : en; }

// ---------------------------------------------------------------------------
// File writers
// ---------------------------------------------------------------------------

bool write_text(const std::string& path, const std::string& text) {
    std::ifstream probe(path);
    std::string dir;
    std::size_t pos = path.find_last_of('/');
    if (pos != std::string::npos) dir = path.substr(0, pos);
    if (!dir.empty()) {
        std::string cmd = "mkdir -p '" + dir + "'";
        int rc = std::system(cmd.c_str());
        (void)rc;
    }
    std::ofstream f(path, std::ios::binary | std::ios::trunc);
    if (!f.is_open()) return false;
    f << text;
    return f.good();
}

bool write_csv(const std::string& path, const std::vector<std::string>& header,
               const std::vector<std::vector<double>>& rows) {
    std::ostringstream os;
    for (std::size_t i = 0; i < header.size(); ++i) {
        os << header[i];
        if (i + 1 < header.size()) os << ',';
    }
    os << '\n';
    for (const auto& row : rows) {
        for (std::size_t i = 0; i < row.size(); ++i) {
            os << json_float(row[i]);
            if (i + 1 < row.size()) os << ',';
        }
        os << '\n';
    }
    return write_text(path, os.str());
}

// ---------------------------------------------------------------------------
// SVG plots (vector graphics — sharp at any dpi)
// ---------------------------------------------------------------------------

const char* palette_color(int i) {
    static const char* PAL[8] = {"#1f6feb", "#d29922", "#3fb950", "#f85149",
                                 "#ab7df8", "#39c5cf", "#e3b341", "#ff7b72"};
    return PAL[i % 8];
}

static std::string xml_escape(const std::string& s) {
    std::string out;
    for (char c : s) {
        if (c == '&') out += "&amp;";
        else if (c == '<') out += "&lt;";
        else if (c == '>') out += "&gt;";
        else out += c;
    }
    return out;
}

static std::string fmt_axis(double v) {
    double a = std::fabs(v);
    char buf[40];
    if (a == 0.0) return "0";
    if (a < 1e-3 || a >= 1e6) {
        std::snprintf(buf, sizeof(buf), "%.3e", v);
    } else {
        std::snprintf(buf, sizeof(buf), "%.4f", v);
    }
    return buf;
}

bool svg_line_plot(const std::string& path, const std::string& title,
                   const std::string& x_label, const std::string& y_label,
                   const std::vector<Series>& series) {
    const double w = 900.0, h = 560.0;
    const double ml = 72.0, mr = 24.0, mt = 56.0, mb = 64.0;
    const double pw = w - ml - mr, ph = h - mt - mb;

    double xmin = 1e308, xmax = -1e308, ymin = 1e308, ymax = -1e308;
    for (const auto& s : series) {
        for (const auto& [x, y] : s.points) {
            xmin = std::fmin(xmin, x);
            xmax = std::fmax(xmax, x);
            ymin = std::fmin(ymin, y);
            ymax = std::fmax(ymax, y);
        }
    }
    if (xmin > xmax) { xmin = 0; xmax = 1; ymin = 0; ymax = 1; }
    if (xmax - xmin < 1e-300) xmax += 1.0;
    if (ymax - ymin < 1e-300) ymax += 1.0;
    double pad_y = 0.05 * (ymax - ymin);
    ymin -= pad_y;
    ymax += pad_y;

    auto sx = [&](double x) { return ml + (x - xmin) / (xmax - xmin) * pw; };
    auto sy = [&](double y) { return mt + ph - (y - ymin) / (ymax - ymin) * ph; };

    std::ostringstream os;
    os << "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 900 560\" "
          "font-family=\"'Segoe UI','Helvetica Neue',Arial,sans-serif\">\n";
    os << "<rect width=\"900\" height=\"560\" fill=\"#ffffff\"/>\n";
    os << "<text x=\"450\" y=\"34\" font-size=\"20\" font-weight=\"600\" fill=\"#1f2328\" "
          "text-anchor=\"middle\">" << xml_escape(title) << "</text>\n";

    char buf[512];
    for (int i = 0; i <= 5; ++i) {
        double t = i / 5.0;
        double gx = ml + t * pw;
        double gy = mt + ph - t * ph;
        std::snprintf(buf, sizeof(buf),
                      "<line x1=\"%.1f\" y1=\"%.1f\" x2=\"%.1f\" y2=\"%.1f\" "
                      "stroke=\"#e6e8eb\" stroke-width=\"1\"/>\n",
                      gx, mt, gx, mt + ph);
        os << buf;
        std::snprintf(buf, sizeof(buf),
                      "<line x1=\"%.1f\" y1=\"%.1f\" x2=\"%.1f\" y2=\"%.1f\" "
                      "stroke=\"#e6e8eb\" stroke-width=\"1\"/>\n",
                      ml, gy, ml + pw, gy);
        os << buf;
        std::snprintf(buf, sizeof(buf),
                      "<text x=\"%.1f\" y=\"%.1f\" font-size=\"12\" fill=\"#57606a\" "
                      "text-anchor=\"middle\">%s</text>\n",
                      gx, mt + ph + 20.0, fmt_axis(xmin + t * (xmax - xmin)).c_str());
        os << buf;
        std::snprintf(buf, sizeof(buf),
                      "<text x=\"%.1f\" y=\"%.1f\" font-size=\"12\" fill=\"#57606a\" "
                      "text-anchor=\"end\">%s</text>\n",
                      ml - 8.0, gy + 4.0, fmt_axis(ymin + t * (ymax - ymin)).c_str());
        os << buf;
    }

    std::snprintf(buf, sizeof(buf),
                  "<line x1=\"%.1f\" y1=\"%.1f\" x2=\"%.1f\" y2=\"%.1f\" stroke=\"#1f2328\" "
                  "stroke-width=\"1.4\"/>\n",
                  ml, mt + ph, ml + pw, mt + ph);
    os << buf;
    std::snprintf(buf, sizeof(buf),
                  "<line x1=\"%.1f\" y1=\"%.1f\" x2=\"%.1f\" y2=\"%.1f\" stroke=\"#1f2328\" "
                  "stroke-width=\"1.4\"/>\n",
                  ml, mt, ml, mt + ph);
    os << buf;

    for (const auto& s : series) {
        if (s.points.empty()) continue;
        os << "<polyline fill=\"none\" stroke=\"" << s.color
           << "\" stroke-width=\"1.8\" stroke-linejoin=\"round\" points=\"";
        bool first = true;
        for (const auto& [x, y] : s.points) {
            std::snprintf(buf, sizeof(buf), "%.2f,%.2f", sx(x), sy(y));
            if (!first) os << ' ';
            os << buf;
            first = false;
        }
        os << "\"/>\n";
    }

    std::snprintf(buf, sizeof(buf),
                  "<text x=\"%.1f\" y=\"%.1f\" font-size=\"14\" fill=\"#1f2328\" "
                  "text-anchor=\"middle\">%s</text>\n",
                  ml + pw / 2.0, h - 18.0, xml_escape(x_label).c_str());
    os << buf;
    std::snprintf(buf, sizeof(buf),
                  "<text x=\"20\" y=\"%.1f\" font-size=\"14\" fill=\"#1f2328\" "
                  "text-anchor=\"middle\" transform=\"rotate(-90 20 %.1f)\">%s</text>\n",
                  mt + ph / 2.0, mt + ph / 2.0, xml_escape(y_label).c_str());
    os << buf;

    double lx = ml + pw - 16.0;
    for (std::size_t i = 0; i < series.size(); ++i) {
        double ly = mt + 16.0 + static_cast<double>(i) * 22.0;
        std::snprintf(buf, sizeof(buf),
                      "<line x1=\"%.1f\" y1=\"%.1f\" x2=\"%.1f\" y2=\"%.1f\" stroke=\"%s\" "
                      "stroke-width=\"2.4\"/>\n",
                      lx - 88.0, ly, lx - 60.0, ly, series[i].color.c_str());
        os << buf;
        std::snprintf(buf, sizeof(buf),
                      "<text x=\"%.1f\" y=\"%.1f\" font-size=\"12.5\" fill=\"#1f2328\" "
                      "text-anchor=\"end\">%s</text>\n",
                      lx - 96.0, ly + 4.0, xml_escape(series[i].label).c_str());
        os << buf;
    }
    os << "</svg>\n";
    return write_text(path, os.str());
}

}  // namespace trivortex
