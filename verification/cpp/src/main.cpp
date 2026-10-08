// SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
// SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
// ===========================================================================
// TRIVORTEX — VERIFICATION LABORATORY (C++17, interactive)
// ===========================================================================
// The interactive laboratory around the C++ numeric twin (milestone M3):
//   * run the V1-V4 ladder (presets or fully custom parameters);
//   * the M3 -O2 benchmark (RK4 right-hand-side evaluations per second);
//   * a convergence study (measured omega error vs integration grid);
//   * SVG plot export (vector figures — sharp at any dpi; the same data can
//     be re-rendered at 600 dpi raster by the Python laboratory);
//   * CSV data export and a JSON protocol per run (the schema of
//     verification/README.md §12);
//   * a bilingual interface (English / Русский).
//
// Usage:
//   ./trivortex-lab                              interactive menu
//   ./trivortex-lab --preset quick --no-menu     CI mode
//   ./trivortex-lab --preset quick --plots --csv --lang ru
//
// Author: Isaev Iskhak Khamzatovich (repository owner)
// Year: 2026
// ===========================================================================
#include "verify.hpp"

#include <cmath>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <string>
#include <vector>

namespace {

using namespace trivortex;

struct Config {
    Lang lang = Lang::En;
    bool no_menu = false;
    std::string preset = "default";
    std::string out_dir = "outputs/cpp";
    bool plots = false;
    bool csv = false;
};

std::string prompt(const std::string& text) {
    std::cout << text << std::flush;
    std::string line;
    if (!std::getline(std::cin, line)) return "";
    return line;
}

double ask_f64(Lang lang, const char* en, const char* ru, double def) {
    std::string raw = prompt(tr(lang, en, ru));
    if (raw.empty()) return def;
    try {
        return std::stod(raw);
    } catch (...) {
        return def;
    }
}

int ask_int(Lang lang, const char* en, const char* ru, int def) {
    std::string raw = prompt(tr(lang, en, ru));
    if (raw.empty()) return def;
    try {
        return std::stoi(raw);
    } catch (...) {
        return def;
    }
}

std::string default_out_dir() {
    // verification/outputs/cpp, relative to the executable's working tree
    return "verification/outputs/cpp";
}

void print_report(const std::vector<Check>& checks, Lang lang, double wall,
                  const std::string& preset_name, double rhs_per_s) {
    const char* pass = tr(lang, "PASS", "ПРОЙДЕНО");
    const char* fail = tr(lang, "FAIL", "ПРОВАЛ");
    std::printf("════════════════════════════════════════════════════════════════\n");
    for (const auto& c : checks) {
        std::string title = "<check>";
        for (const auto& [k, v] : c) {
            if (k == "check" && v->kind == Val::Kind::String) title = v->str;
        }
        std::printf("[%s] %s\n", has_passed(c) ? pass : fail, title.c_str());
        for (const auto& [k, v] : c) {
            if (k == "check" || k == "passed") continue;
            if (v->kind == Val::Kind::Number) {
                std::printf("    %s = %.15e\n", k.c_str(), v->num);
            } else if (v->kind == Val::Kind::String) {
                std::printf("    %s = %s\n", k.c_str(), v->str.c_str());
            } else if (v->kind == Val::Kind::Bool) {
                std::printf("    %s = %s\n", k.c_str(), v->b ? pass : fail);
            } else if (v->kind == Val::Kind::Map) {
                std::printf("    %s:\n", k.c_str());
                for (const auto& [kk, vv] : v->map) {
                    if (vv->kind == Val::Kind::Number) {
                        std::printf("      %s = %.15e\n", kk.c_str(), vv->num);
                    }
                }
            }
        }
    }
    int n_pass = 0;
    for (const auto& c : checks) {
        if (has_passed(c)) ++n_pass;
    }
    std::printf("────────────────────────────────────────────────────────────────\n");
    std::printf("  %s %d/%d %s (%s=%s, %s %.2fs, benchmark %.3e rhs/s)\n",
                tr(lang, "RESULT", "ИТОГ"), n_pass, static_cast<int>(checks.size()),
                tr(lang, "checks passed", "проверок пройдено"),
                tr(lang, "preset", "пресет"), preset_name.c_str(),
                tr(lang, "wall time", "время"), wall, rhs_per_s);
    std::printf("════════════════════════════════════════════════════════════════\n");
}

std::string field_f64_str(const Check& c, const std::string& name) {
    for (const auto& [k, v] : c) {
        if (k == name && v->kind == Val::Kind::Number) return json_float(v->num);
    }
    return "nan";
}

void save_json(const Check& report, const std::string& path) {
    write_text(path, val_to_json(vmap(report), 0));
}

void export_plots(const std::string& out_dir, Lang lang) {
    std::string plots = out_dir + "/plots";
    const double c_ch = 1.0, t_period = 2.0 * PI;
    double omega = analytical_frequency(c_ch, t_period);
    double t_r = 2.0 * PI / omega;

    // fig 1: r_k(t) for k = 0,1,2 over two modulation periods
    std::vector<Series> s1;
    for (int k = 0; k < 3; ++k) {
        Series ser;
        ser.label = "k = " + std::to_string(k);
        ser.color = palette_color(k);
        const int n = 600;
        for (int i = 0; i <= n; ++i) {
            double t = 2.0 * t_r * i / n;
            ser.points.emplace_back(t, analytical_radius(t, c_ch, t_period, k));
        }
        s1.push_back(ser);
    }
    svg_line_plot(plots + "/fig1_closed_form.svg",
                  "Theorem 3.1 closed form: r_k(t) over two modulation periods", "t",
                  "r_k(t)", s1);

    // fig 2: C_Ch(t) Section-6 diagnostic over [0, 100T]
    Series s2;
    s2.label = "C_Ch(t)";
    s2.color = palette_color(1);
    const int n2 = 1000;
    for (int i = 0; i < n2; ++i) {
        double t = 100.0 * t_period * i / (n2 - 1);
        double r = analytical_radius(t, c_ch, t_period, 0);
        s2.points.emplace_back(t, compute_chaplygin(r, omega, 1.0, 0.0));
    }
    svg_line_plot(plots + "/fig2_chaplygin_diagnostic.svg",
                  "Section-6 diagnostic: C_Ch(t) = r^2 (theta_dot - q/r), [0, 100T]", "t",
                  "C_Ch(t)", {s2});

    // fig 3: tracked Lagrange rigid rotation
    auto [v2check, traj] = check_v2_lagrange_rotation(1.0, 1.0, 2, 2000, true);
    std::vector<Series> s3;
    for (int v = 0; v < 3; ++v) {
        Series ser;
        ser.label = "vortex " + std::to_string(v);
        ser.color = palette_color(v);
        for (const auto& [t, st] : traj) ser.points.emplace_back(st[2 * v], st[2 * v + 1]);
        s3.push_back(ser);
    }
    svg_line_plot(plots + "/fig3_lagrange_trajectory.svg",
                  "V2: rigid rotation, omega = 3G/(2 pi a^2)", "x", "y", s3);

    // fig 4: convergence study
    Series s4;
    s4.label = "omega_rel_err";
    s4.color = palette_color(3);
    std::vector<std::vector<double>> conv_rows;
    for (int spp : {250, 500, 1000, 2000, 4000, 8000}) {
        auto [chk, t] = check_v2_lagrange_rotation(1.0, 1.0, 2, spp, false);
        (void)t;
        double err = 0.0;
        for (const auto& [k, v] : chk) {
            if (k == "omega_relative_error" && v->kind == Val::Kind::Number) err = v->num;
        }
        s4.points.emplace_back(static_cast<double>(spp), err);
        conv_rows.push_back({static_cast<double>(spp), err});
    }
    svg_line_plot(plots + "/fig4_convergence.svg",
                  "V2 convergence: omega relative error vs steps/period",
                  "steps per period", "omega relative error", {s4});

    // fig 5: V4 unequal-circulation trajectory
    std::vector<double> st4 = {0.0 - 0.5, 0.0 - std::sqrt(3.0) / 6.0, 1.0 - 0.5,
                               0.0 - std::sqrt(3.0) / 6.0, 0.5 - 0.5,
                               std::sqrt(3.0) / 2.0 - std::sqrt(3.0) / 6.0};
    std::vector<double> g4 = {1.0, 2.0, 3.0};
    double dt4 = (2.0 * PI / lagrange_omega(2.0, 1.0)) / 4000.0;
    std::vector<std::pair<double, std::array<double, 6>>> traj4;
    long long n_steps4 = 3LL * 4000;
    long long every4 = std::max<long long>(n_steps4 / 400, 1);
    for (long long step = 0; step < n_steps4; ++step) {
        st4 = rk4_step(st4, g4, dt4);
        if (step % every4 == 0) {
            std::array<double, 6> snap{};
            std::copy(st4.begin(), st4.end(), snap.begin());
            traj4.emplace_back(step * dt4, snap);
        }
    }
    std::vector<Series> s5;
    for (int v = 0; v < 3; ++v) {
        Series ser;
        ser.label = "Gamma_" + std::to_string(v + 1);
        ser.color = palette_color(v);
        for (const auto& [t, st] : traj4) ser.points.emplace_back(st[2 * v], st[2 * v + 1]);
        s5.push_back(ser);
    }
    svg_line_plot(plots + "/fig5_v4_unequal.svg",
                  "V4: unequal circulations Gamma = (1, 2, 3), generic triangle", "x", "y",
                  s5);

    std::printf("%s %s\n", tr(lang, "SVG plots saved to", "SVG-графики сохранены в"),
                plots.c_str());
}

void export_csv(const std::string& out_dir, Lang lang) {
    std::string data = out_dir + "/data";
    auto [v2check, traj] = check_v2_lagrange_rotation(1.0, 1.0, 2, 2000, true);
    std::vector<std::vector<double>> rows;
    for (const auto& [t, st] : traj) {
        rows.push_back({t, st[0], st[1], st[2], st[3], st[4], st[5]});
    }
    write_csv(data + "/v2_trajectory.csv", {"t", "x0", "y0", "x1", "y1", "x2", "y2"}, rows);

    const double c_ch = 1.0, t_period = 2.0 * PI;
    double omega = analytical_frequency(c_ch, t_period);
    std::vector<std::vector<double>> diag;
    for (int i = 0; i < 1000; ++i) {
        double t = 100.0 * t_period * i / 999.0;
        double r = analytical_radius(t, c_ch, t_period, 0);
        diag.push_back({t, r, compute_chaplygin(r, omega, 1.0, 0.0)});
    }
    write_csv(data + "/v1_chaplygin_diagnostic.csv", {"t", "r0", "C_Ch"}, diag);
    std::printf("%s %s\n", tr(lang, "CSV data saved to", "CSV-данные сохранены в"),
                data.c_str());
}

int run_cli(const Config& cfg) {
    const Preset* p = find_preset(cfg.preset);
    if (p == nullptr) {
        std::fprintf(stderr, "unknown preset: %s (quick | default | full)\n",
                     cfg.preset.c_str());
        return 2;
    }
    LadderRun run = run_ladder(*p, "trivortex-verification-cpp");
    print_report(run.checks, cfg.lang, run.wall_time_s, cfg.preset, run.rhs_per_s);

    std::string path = cfg.out_dir + "/trivortex_verify_" + cfg.preset + "_" +
                       utc_stamp() + ".json";
    save_json(run.report, path);
    std::printf("%s %s\n", tr(cfg.lang, "JSON protocol saved to", "JSON-протокол сохранён в"),
                path.c_str());
    if (cfg.plots) export_plots(cfg.out_dir, cfg.lang);
    if (cfg.csv) export_csv(cfg.out_dir, cfg.lang);
    return run.all_passed ? 0 : 1;
}

Config parse_args(int argc, char** argv) {
    Config cfg;
    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        if (a == "--preset" && i + 1 < argc) {
            cfg.preset = argv[++i];
            cfg.no_menu = true;
        } else if (a == "--out-dir" && i + 1 < argc) {
            cfg.out_dir = argv[++i];
        } else if (a == "--lang" && i + 1 < argc) {
            cfg.lang = lang_from_code(argv[++i]);
        } else if (a == "--plots") {
            cfg.plots = true;
        } else if (a == "--csv") {
            cfg.csv = true;
        } else if (a == "--no-menu") {
            cfg.no_menu = true;
        } else if (a == "--version") {
            std::printf("trivortex-lab 1.0.0 (C++ numeric twin, M3)\n");
            std::exit(0);
        } else if (a == "--help" || a == "-h") {
            std::printf("TRIVORTEX verification lab (C++ port)\n");
            std::printf("  --preset quick|default|full   run the ladder non-interactively\n");
            std::printf("  --out-dir DIR                 JSON protocol directory\n");
            std::printf("  --lang en|ru                  interface language\n");
            std::printf("  --plots                       export SVG figures\n");
            std::printf("  --csv                         export CSV data\n");
            std::printf("  --no-menu                     disable the interactive menu\n");
            std::exit(0);
        } else {
            std::fprintf(stderr, "unknown argument: %s (see --help)\n", a.c_str());
            std::exit(2);
        }
    }
    if (cfg.out_dir == "outputs/cpp") cfg.out_dir = default_out_dir();
    return cfg;
}

void custom_parameters(Lang lang, int& rotations, int& steps_per_period) {
    double c_ch = ask_f64(lang, "C_Ch (> 0) [1.0]: ", "C_Ch (> 0) [1.0]: ", 1.0);
    double t_period =
        ask_f64(lang, "T period [6.283185307179586]: ", "Период T [6.283185307179586]: ",
                2.0 * PI);
    double gamma =
        ask_f64(lang, "Gamma (equal circulations) [1.0]: ",
                "Гамма (одинаковые циркуляции) [1.0]: ", 1.0);
    double a = ask_f64(lang, "Triangle side a [1.0]: ", "Сторона треугольника a [1.0]: ", 1.0);
    rotations = ask_int(lang, "Rotations [5]: ", "Обороты [5]: ", 5);
    steps_per_period =
        ask_int(lang, "Steps per period [4000]: ", "Шагов на период [4000]: ", 4000);

    // A fully custom analytic-layer demo: pin the custom closed form and
    // report its reference values in the same JSON schema.
    double omega = analytical_frequency(c_ch, t_period);
    std::printf("  omega = %.15g\n  eps   = %.15g\n  omega_Lagrange(Gamma,a) = %.15g\n",
                omega, analytical_amplitude(c_ch), lagrange_omega(gamma, a));
    Check v1 = check_v1_theorem31(c_ch, t_period, 1000);
    std::printf("[%s] %s  (sep = %s, per = %s)\n", has_passed(v1) ? "PASS" : "FAIL",
                tr(lang, "custom Theorem 3.1 layer", "своя аналитическая слой Теоремы 3.1"),
                field_f64_str(v1, "angular_separation_error").c_str(),
                field_f64_str(v1, "periodicity_residual").c_str());
}

}  // namespace

int main(int argc, char** argv) {
    Config cfg = parse_args(argc, argv);
    if (cfg.no_menu) return run_cli(cfg);

    std::printf("\n╔══════════════════════════════════════════════════════════════════╗\n");
    std::printf("║        TRIVORTEX — Verification Laboratory (C++ port, M3)        ║\n");
    std::printf("║   TRIVORTEX — Лаборатория верификации (порт C++, веха M3)        ║\n");
    std::printf("╚══════════════════════════════════════════════════════════════════╝\n\n");
    std::string choice = prompt("Language / Язык: [1] English  [2] Русский  > ");
    Lang lang = (choice == "2") ? Lang::Ru : Lang::En;

    while (true) {
        std::printf("\n┌─────────────────────────────────────────────────────┐\n");
        std::printf("│ %-51s │\n", tr(lang, "MAIN MENU", "ГЛАВНОЕ МЕНЮ"));
        std::printf("├─────────────────────────────────────────────────────┤\n");
        std::printf("│ %-51s │\n", tr(lang, "1) Run the verification ladder V1-V4", "1) Запустить лестницу верификации V1-V4"));
        std::printf("│ %-51s │\n", tr(lang, "2) Custom parameters (analytic layer demo)", "2) Свои параметры (демо аналитического слоя)"));
        std::printf("│ %-51s │\n", tr(lang, "3) Analysis: convergence study", "3) Анализ: исследование сходимости"));
        std::printf("│ %-51s │\n", tr(lang, "4) Plots: export SVG figures", "4) Графики: экспорт SVG"));
        std::printf("│ %-51s │\n", tr(lang, "5) Export CSV data", "5) Экспорт CSV"));
        std::printf("│ %-51s │\n", tr(lang, "0) Exit", "0) Выход"));
        std::printf("└─────────────────────────────────────────────────────┘\n");
        std::string pick = prompt(tr(lang, "choice> ", "выбор> "));

        if (pick == "1") {
            std::string pn = prompt(tr(lang,
                "Preset [quick/default/full] (default: default): ",
                "Пресет [quick/default/full] (по умолчанию: default): "));
            Config c2 = cfg;
            c2.lang = lang;
            c2.preset = pn.empty() ? "default" : pn;
            run_cli(c2);
        } else if (pick == "2") {
            int rotations = 5, spp = 4000;
            custom_parameters(lang, rotations, spp);
        } else if (pick == "3") {
            std::printf("%s\n", tr(lang,
                "steps/period   omega_rel_err     shape_drift",
                "шагов/период   отн.ошибка omega  дрейф формы"));
            for (int spp : {250, 500, 1000, 2000, 4000, 8000}) {
                auto [chk, t] = check_v2_lagrange_rotation(1.0, 1.0, 2, spp, false);
                (void)t;
                std::printf("  %8d   %13s   %11s\n", spp,
                            field_f64_str(chk, "omega_relative_error").c_str(),
                            field_f64_str(chk, "shape_drift").c_str());
            }
        } else if (pick == "4") {
            export_plots(cfg.out_dir, lang);
        } else if (pick == "5") {
            export_csv(cfg.out_dir, lang);
        } else if (pick == "0") {
            std::printf("%s\n", tr(lang,
                "Goodbye — and keep every number bound to a run.",
                "До встречи — и держите каждое число привязанным к запуску."));
            return 0;
        } else {
            std::printf("%s\n", tr(lang, "Invalid choice, try again.",
                                   "Неверный пункт, попробуйте ещё раз."));
        }
    }
}
