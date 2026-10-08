// SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
// SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
//! ===========================================================================
//! TRIVORTEX — VERIFICATION LABORATORY (Rust, interactive)
//! ===========================================================================
//! A full-fledged command-line laboratory around the Rust numeric twin:
//!   * run the V1–V4 ladder (presets quick / default / full or custom
//!     parameters C_Ch, T, Gamma, a, rotations, steps/period);
//!   * a convergence study (measured omega error vs integration grid);
//!   * SVG plot export (vector figures, sharp at any resolution — the same
//!     data can be re-rendered at 600 dpi raster by the Python lab);
//!   * CSV data export and a JSON protocol per run (schema of
//!     `verification/README.md` §12 — every number bound to a run);
//!   * a bilingual interface (English / Русский, chosen at start or via
//!     `--lang en|ru`).
//!
//! Usage (non-interactive, CI-friendly):
//!     cargo run --release -- --preset quick --out-dir verification/outputs/rust
//!     cargo run --release -- --lang ru --no-menu --preset default --plots --csv
//!     cargo test   # the pinned-reference guard (tests/ladder.rs + unit tests)
//!
//! Author: Isaev Iskhak Khamzatovich (repository owner)
//! Year: 2026
//! ===========================================================================

use std::io::{self, BufRead, Write};
use std::path::{Path, PathBuf};
use std::process::ExitCode;
use std::time::Instant;

use trivortex_verify::i18n::{from_code, Lang, Strings};
use trivortex_verify::report::{color, svg_line_plot, val_to_json, write_csv, write_text, Series};
use trivortex_verify::verify::{
    analytical_frequency, analytical_radius, check_v2_lagrange_rotation, compute_chaplygin,
    equilateral_initial, has_passed, lagrange_omega, preset, rk4_step, run_ladder, Preset, Val,
};

const SUITE: &str = "trivortex-verification-rust";

struct Config {
    lang: Lang,
    no_menu: bool,
    preset: Option<String>,
    out_dir: PathBuf,
    plots: bool,
    csv: bool,
}

fn main() -> ExitCode {
    let cfg = parse_args();
    let s = Strings;
    let lang = cfg.lang;

    if cfg.no_menu {
        let preset_name = cfg.preset.clone().unwrap_or_else(|| "default".into());
        return run_cli(&cfg, &preset_name);
    }

    // ---- interactive session -------------------------------------------
    println!();
    println!("{}", banner(&s.welcome(lang)));
    println!();

    let lang = if cfg.lang == Lang::En && !cfg.no_menu {
        // offer the language choice only in a truly interactive session
        let choice = prompt(&s.choose_lang(lang));
        match choice.trim() {
            "2" => Lang::Ru,
            _ => Lang::En,
        }
    } else {
        lang
    };
    println!("{}", if lang == Lang::Ru { s.lang_set_ru(lang) } else { s.lang_set_en(lang) });

    let out_dir = cfg.out_dir.clone();
    let mut last_json: Option<String> = None;

    loop {
        println!();
        println!("┌─────────────────────────────────────────────────────┐");
        println!("│ {} │", center(&s.menu_title(lang), 51));
        println!("├─────────────────────────────────────────────────────┤");
        for line in [s.m1(lang), s.m2(lang), s.m3(lang), s.m4(lang), s.m5(lang), s.m6(lang), s.m0(lang)] {
            println!("│ {:<51} │", line);
        }
        println!("└─────────────────────────────────────────────────────┘");
        print!("{}", s.prompt_choice(lang));
        io::stdout().flush().ok();
        let mut line = String::new();
        io::stdin().lock().read_line(&mut line).ok();
        match line.trim() {
            "1" => {
                let preset_name = prompt(s.preset_prompt(lang));
                let preset_name = if preset_name.trim().is_empty() {
                    "default".to_string()
                } else {
                    preset_name.trim().to_string()
                };
                match run_cli(
                    &Config {
                        lang,
                        no_menu: true,
                        preset: Some(preset_name.clone()),
                        out_dir: out_dir.clone(),
                        plots: false,
                        csv: false,
                    },
                    &preset_name,
                ) {
                    ExitCode::SUCCESS => last_json = find_latest_json(&out_dir),
                    _ => {}
                }
            }
            "2" => {
                println!("{}", s.custom_note(lang));
                let p = custom_parameters(lang);
                let t0 = Instant::now();
                let run = trivortex_verify::verify::run_ladder(p, SUITE, t0);
                print_report(&run.checks, lang, run.wall_time_s, "custom");
                let path = out_dir.join(format!(
                    "trivortex_verify_custom_{}.json",
                    trivortex_verify::report::utc_stamp()
                ));
                save_json(&run.report, &path);
                println!("{} {}", s.json_saved(lang), path.display());
                last_json = find_latest_json(&out_dir);
            }
            "3" => {
                convergence_study(&out_dir, lang);
            }
            "4" => {
                export_plots(&out_dir, lang);
                println!("{} {}", s.plots_saved(lang), out_dir.join("plots").display());
            }
            "5" => {
                export_csv(&out_dir, lang);
                println!("{} {}", s.csv_saved(lang), out_dir.join("data").display());
            }
            "6" => {
                let latest = last_json.clone().or_else(|| find_latest_json(&out_dir));
                match latest.as_deref() {
                    Some(p) => {
                        println!("--- JSON ---");
                        println!("{}", std::fs::read_to_string(p).unwrap_or_default());
                    }
                    None => println!("{}", s.invalid(lang)),
                }
            }
            "0" => {
                println!("{}", s.byefr(lang));
                return ExitCode::SUCCESS;
            }
            _ => println!("{}", s.invalid(lang)),
        }
    }
}

// ---------------------------------------------------------------------------
// CLI helpers
// ---------------------------------------------------------------------------

fn parse_args() -> Config {
    let mut cfg = Config {
        lang: Lang::En,
        no_menu: false,
        preset: None,
        out_dir: default_out_dir(),
        plots: false,
        csv: false,
    };
    let args: Vec<String> = std::env::args().collect();
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--lang" => {
                i += 1;
                if i < args.len() {
                    cfg.lang = from_code(&args[i]);
                }
            }
            "--no-menu" => cfg.no_menu = true,
            "--preset" => {
                i += 1;
                if i < args.len() {
                    cfg.preset = Some(args[i].clone());
                    cfg.no_menu = true;
                }
            }
            "--out-dir" => {
                i += 1;
                if i < args.len() {
                    cfg.out_dir = PathBuf::from(&args[i]);
                }
            }
            "--plots" => cfg.plots = true,
            "--csv" => cfg.csv = true,
            "--version" => {
                println!("trivortex-lab {} (Rust numeric twin, M1)", env!("CARGO_PKG_VERSION"));
                std::process::exit(0);
            }
            "--help" | "-h" => {
                println!("TRIVORTEX verification lab (Rust port)");
                println!("  --preset quick|default|full   run the ladder non-interactively");
                println!("  --out-dir DIR                 JSON protocol directory");
                println!("  --lang en|ru                  interface language");
                println!("  --plots                       export SVG figures");
                println!("  --csv                         export CSV data");
                println!("  --no-menu                     disable the interactive menu");
                std::process::exit(0);
            }
            other => {
                eprintln!("unknown argument: {other} (see --help)");
                std::process::exit(2);
            }
        }
        i += 1;
    }
    cfg
}

fn default_out_dir() -> PathBuf {
    // verification/outputs/rust, mirroring the Python ladder's default
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .map(|p| p.join("outputs").join("rust"))
        .unwrap_or_else(|| PathBuf::from("outputs/rust"))
}

fn run_cli(cfg: &Config, preset_name: &str) -> ExitCode {
    let s = Strings;
    let lang = cfg.lang;
    let Some(p) = preset(preset_name) else {
        eprintln!("unknown preset: {preset_name} (quick | default | full)");
        return ExitCode::FAILURE;
    };
    println!("{}", s.running(lang));
    let t0 = Instant::now();
    let run = run_ladder(p, SUITE, t0);
    print_report(&run.checks, lang, run.wall_time_s, preset_name);

    let stamp = trivortex_verify::report::utc_stamp();
    let path = cfg
        .out_dir
        .join(format!("trivortex_verify_{preset_name}_{stamp}.json"));
    save_json(&run.report, &path);
    println!("{} {}", s.json_saved(lang), path.display());

    if cfg.plots {
        export_plots(&cfg.out_dir, lang);
        println!("{} {}", s.plots_saved(lang), cfg.out_dir.join("plots").display());
    }
    if cfg.csv {
        export_csv(&cfg.out_dir, lang);
        println!("{} {}", s.csv_saved(lang), cfg.out_dir.join("data").display());
    }

    if run.all_passed {
        ExitCode::SUCCESS
    } else {
        ExitCode::FAILURE
    }
}

fn save_json(report: &[(String, Val)], path: &Path) {
    let json = val_to_json(&Val::M(report.to_vec()), 0);
    if let Err(e) = write_text(path, &json) {
        eprintln!("failed to write {}: {e}", path.display());
    }
}

fn find_latest_json(dir: &Path) -> Option<String> {
    let mut best: Option<(std::time::SystemTime, String)> = None;
    if let Ok(rd) = std::fs::read_dir(dir) {
        for entry in rd.flatten() {
            let name = entry.file_name().to_string_lossy().into_owned();
            if name.starts_with("trivortex_verify") && name.ends_with(".json") {
                if let Ok(md) = entry.metadata() {
                    let t = md.modified().unwrap_or(std::time::UNIX_EPOCH);
                    if best.as_ref().map_or(true, |(bt, _)| t > *bt) {
                        best = Some((t, entry.path().display().to_string()));
                    }
                }
            }
        }
    }
    best.map(|(_, p)| p)
}

// ---------------------------------------------------------------------------
// Pretty printing
// ---------------------------------------------------------------------------

fn banner(text: &str) -> String {
    format!(
        "╔══════════════════════════════════════════════════════════════════╗\n║{:^66}║\n╚══════════════════════════════════════════════════════════════════╝",
        format!(" {text} ")
    )
}

fn center(text: &str, width: usize) -> String {
    let len = text.chars().count();
    if len >= width {
        return text.to_string();
    }
    let left = (width - len) / 2;
    format!("{}{}", " ".repeat(left), text)
}

fn fmt_res(name: &str, v: &Val, lang: Lang, s: &Strings) -> String {
    match v {
        Val::N(x) => format!("    {name} = {x:e}"),
        Val::S(x) => format!("    {name} = {x}"),
        Val::B(true) => format!("    {name} = {}", s.pass_mark(lang)),
        Val::B(false) => format!("    {name} = {}", s.fail_mark(lang)),
        Val::M(fields) => {
            let mut out = format!("    {name}:\n");
            for (k, val) in fields {
                match val {
                    Val::N(x) => out.push_str(&format!("      {k} = {x:e}\n")),
                    Val::S(x) => out.push_str(&format!("      {k} = {x}\n")),
                    _ => {}
                }
            }
            out
        }
        Val::L(_) => format!("    {name} = [...]"),
    }
}

fn print_report(
    checks: &[Vec<(&'static str, Val)>],
    lang: Lang,
    wall: f64,
    preset_name: &str,
) {
    let s = Strings;
    println!("════════════════════════════════════════════════════════════════");
    for c in checks {
        let passed = has_passed(c);
        let mark = if passed { s.pass_mark(lang) } else { s.fail_mark(lang) };
        let title = c
            .iter()
            .find(|(k, _)| *k == "check")
            .and_then(|(_, v)| match v {
                Val::S(x) => Some(x.clone()),
                _ => None,
            })
            .unwrap_or_default();
        println!("[{mark}] {title}");
        for (k, v) in c {
            if *k == "check" || *k == "passed" {
                continue;
            }
            println!("{}", fmt_res(k, v, lang, &s));
        }
    }
    let n_pass = checks.iter().filter(|c| has_passed(c)).count();
    println!("────────────────────────────────────────────────────────────────");
    println!(
        "  {} {}/{} {} ({}={}, {} {:.2}s)",
        s.result_line(lang),
        n_pass,
        checks.len(),
        s.checks_passed(lang),
        s.preset(lang),
        preset_name,
        s.wall(lang),
        wall
    );
    println!("════════════════════════════════════════════════════════════════");
}

// ---------------------------------------------------------------------------
// Menu actions
// ---------------------------------------------------------------------------

fn prompt(text: &str) -> String {
    print!("{text}");
    io::stdout().flush().ok();
    let mut line = String::new();
    io::stdin().lock().read_line(&mut line).ok();
    line
}

fn ask_f64(text: &str, default: f64) -> f64 {
    let raw = prompt(text);
    let raw = raw.trim();
    if raw.is_empty() {
        return default;
    }
    raw.parse().unwrap_or(default)
}

fn ask_usize(text: &str, default: usize) -> usize {
    let raw = prompt(text);
    let raw = raw.trim();
    if raw.is_empty() {
        return default;
    }
    raw.parse().unwrap_or(default)
}

#[allow(clippy::too_many_lines)]
fn custom_parameters(lang: Lang) -> Preset {
    let s = Strings;
    let c_ch = ask_f64(s.cch_prompt(lang), 1.0);
    let t_period = ask_f64(s.t_prompt(lang), 2.0 * std::f64::consts::PI);
    let gamma = ask_f64(s.gamma_prompt(lang), 1.0);
    let a = ask_f64(s.a_prompt(lang), 1.0);
    let rotations = ask_usize(s.rot_prompt(lang), 5);
    let steps_per_period = ask_usize(s.spp_prompt(lang), 4000);
    let _ = (analytical_frequency(c_ch, t_period), gamma, a); // echoed below
    Preset { rotations, steps_per_period, n_points_cch: 1000 }
}

fn convergence_study(out_dir: &Path, lang: Lang) {
    let s = Strings;
    println!("{}", s.conv_title(lang));
    println!("{}", s.conv_header(lang));
    let grids = [250_usize, 500, 1000, 2000, 4000, 8000];
    let mut rows: Vec<Vec<f64>> = Vec::new();
    let mut series: Vec<(f64, f64)> = Vec::new();
    for spp in grids {
        // mirror of V2 with the analytic reference omega
        let (res, _) = check_v2_lagrange_rotation(1.0, 1.0, 2, spp, false);
        let omega_err = field_f64(&res, "omega_relative_error");
        let shape = field_f64(&res, "shape_drift");
        println!("  {spp:>13}   {omega_err:>13.3e}   {shape:>11.3e}");
        rows.push(vec![spp as f64, omega_err, shape]);
        series.push((spp as f64, omega_err));
    }
    let data_dir = out_dir.join("data");
    let _ = write_csv(
        &data_dir.join("convergence_study.csv"),
        &["steps_per_period", "omega_relative_error", "shape_drift"],
        &rows,
    );
    let _ = svg_line_plot(
        &out_dir.join("plots").join("fig4_convergence.svg"),
        "V2 convergence: omega relative error vs steps/period",
        "steps per period",
        "omega relative error",
        &[Series { label: "omega_rel_err".into(), points: series, color: color(0).into() }],
    );
}

fn field_f64(check: &[(&'static str, Val)], name: &str) -> f64 {
    check
        .iter()
        .find(|(k, _)| *k == name)
        .and_then(|(_, v)| match v {
            Val::N(x) => Some(*x),
            _ => None,
        })
        .unwrap_or(f64::NAN)
}

/// Export five SVG figures (vector graphics — sharp at any dpi):
///   1. closed form r_k(t) for k = 0,1,2 over two modulation periods;
///   2. the Section-6 Chaplygin diagnostic C_Ch(t) over [0, 100T];
///   3. the Lagrange rigid-rotation trajectory (V2, tracked);
///   4. the convergence study (omega error vs grid);
///   5. the V4 unequal-circulation trajectory with invariants annotated.
fn export_plots(out_dir: &Path, lang: Lang) {
    let s = Strings;
    let plots = out_dir.join("plots");
    let _ = std::fs::create_dir_all(&plots);

    // --- fig 1: r_k(t), Theorem 3.1 --------------------------------------
    let (c_ch, t_period) = (1.0_f64, 2.0_f64 * std::f64::consts::PI);
    let omega = analytical_frequency(c_ch, t_period);
    let t_r = 2.0 * std::f64::consts::PI / omega;
    let n = 600;
    let mut series_k = Vec::new();
    for k in 0..3 {
        let pts: Vec<(f64, f64)> = (0..=n)
            .map(|i| {
                let t = i as f64 / n as f64 * 2.0 * t_r;
                (t, analytical_radius(t, c_ch, t_period, k))
            })
            .collect();
        series_k.push(Series {
            label: format!("k = {k}"),
            points: pts,
            color: color(k).into(),
        });
    }
    let _ = svg_line_plot(
        &plots.join("fig1_closed_form.svg"),
        "Theorem 3.1 closed form: r_k(t) over two modulation periods",
        "t",
        "r_k(t)",
        &series_k,
    );

    // --- fig 2: C_Ch(t) Section-6 diagnostic ------------------------------
    let t_max = 100.0 * t_period;
    let n = 1000;
    let pts: Vec<(f64, f64)> = (0..n)
        .map(|i| {
            let t = i as f64 / (n - 1) as f64 * t_max;
            let r = analytical_radius(t, c_ch, t_period, 0);
            (t, compute_chaplygin(r, omega, 1.0, 0.0))
        })
        .collect();
    let _ = svg_line_plot(
        &plots.join("fig2_chaplygin_diagnostic.svg"),
        "Section-6 diagnostic: C_Ch(t) = r^2 (theta_dot - q/r), window [0, 100T]",
        "t",
        "C_Ch(t)",
        &[Series { label: "C_Ch(t)".into(), points: pts, color: color(1).into() }],
    );

    // --- fig 3: Lagrange rigid rotation (tracked trajectory) --------------
    let (_res, traj) = check_v2_lagrange_rotation(1.0, 1.0, 2, 2000, true);
    let mut series_v = Vec::new();
    for v in 0..3 {
        let pts: Vec<(f64, f64)> =
            traj.iter().map(|(_, s)| (s[2 * v], s[2 * v + 1])).collect();
        series_v.push(Series {
            label: format!("vortex {v}"),
            points: pts,
            color: color(v).into(),
        });
    }
    let _ = svg_line_plot(
        &plots.join("fig3_lagrange_trajectory.svg"),
        "V2: rigid rotation, omega = 3G/(2 pi a^2)",
        "x",
        "y",
        &series_v,
    );

    // --- fig 4: convergence ------------------------------------------------
    convergence_study_quiet(&plots);

    // --- fig 5: V4 unequal-circulation trajectory -------------------------
    let traj4 = v4_trajectory();
    let mut series_v = Vec::new();
    for v in 0..3 {
        let pts: Vec<(f64, f64)> =
            traj4.iter().map(|(_, s)| (s[2 * v], s[2 * v + 1])).collect();
        series_v.push(Series {
            label: format!("Gamma_{} = {}", v + 1, [1.0, 2.0, 3.0][v]),
            points: pts,
            color: color(v).into(),
        });
    }
    let _ = svg_line_plot(
        &plots.join("fig5_v4_unequal.svg"),
        "V4: unequal circulations Gamma = (1, 2, 3), generic triangle",
        "x",
        "y",
        &series_v,
    );

    println!("{}", s.figure1(lang));
    println!("{}", s.figure2(lang));
    println!("{}", s.figure3(lang));
    println!("{}", s.figure4(lang));
    println!("{}", s.figure5(lang));
}

fn convergence_study_quiet(plots: &Path) {
    let grids = [250_usize, 500, 1000, 2000, 4000, 8000];
    let series: Vec<(f64, f64)> = grids
        .iter()
        .map(|&spp| {
            let (res, _) = check_v2_lagrange_rotation(1.0, 1.0, 2, spp, false);
            (spp as f64, field_f64(&res, "omega_relative_error"))
        })
        .collect();
    let _ = svg_line_plot(
        &plots.join("fig4_convergence.svg"),
        "V2 convergence: omega relative error vs steps/period",
        "steps per period",
        "omega relative error",
        &[Series { label: "omega_rel_err".into(), points: series, color: color(3).into() }],
    );
}

/// A tracked V4 integration (same parameters as the check, with tracking).
fn v4_trajectory() -> Vec<(f64, [f64; 6])> {
    let a = 1.0_f64;
    let gammas = [1.0_f64, 2.0, 3.0];
    let cy = 3.0_f64.sqrt() / 2.0 * a;
    let cx = (a + 0.5 * a) / 3.0;
    let cyy = cy / 3.0;
    let mut state: Vec<f64> = vec![
        -cx,
        -cyy,
        a - cx,
        -cyy,
        0.5 * a - cx,
        cy - cyy,
    ];
    let mean_gamma = 2.0;
    let omega_ref = lagrange_omega(mean_gamma, a);
    let dt = (2.0 * std::f64::consts::PI / omega_ref) / 4000.0;
    let n_steps = 3 * 4000;
    let track_every = (n_steps / 400).max(1);
    let mut traj = Vec::new();
    for step in 0..n_steps {
        state = rk4_step(&state, &gammas, dt);
        if step % track_every == 0 {
            let mut snap = [0.0_f64; 6];
            snap.copy_from_slice(&state);
            traj.push((step as f64 * dt, snap));
        }
    }
    traj
}

/// Export CSV data: the V2 tracked trajectory and the V1 diagnostic grid.
fn export_csv(out_dir: &Path, _lang: Lang) {
    let data = out_dir.join("data");
    let _ = std::fs::create_dir_all(&data);

    let (_res, traj) = check_v2_lagrange_rotation(1.0, 1.0, 2, 2000, true);
    let rows: Vec<Vec<f64>> = traj
        .iter()
        .map(|(t, s)| vec![*t, s[0], s[1], s[2], s[3], s[4], s[5]])
        .collect();
    let _ = write_csv(
        &data.join("v2_trajectory.csv"),
        &["t", "x0", "y0", "x1", "y1", "x2", "y2"],
        &rows,
    );

    let (c_ch, t_period) = (1.0_f64, 2.0_f64 * std::f64::consts::PI);
    let omega = analytical_frequency(c_ch, t_period);
    let t_max = 100.0 * t_period;
    let rows: Vec<Vec<f64>> = (0..1000)
        .map(|i| {
            let t = i as f64 / 999.0 * t_max;
            let r = analytical_radius(t, c_ch, t_period, 0);
            vec![t, r, compute_chaplygin(r, omega, 1.0, 0.0)]
        })
        .collect();
    let _ = write_csv(
        &data.join("v1_chaplygin_diagnostic.csv"),
        &["t", "r0", "C_Ch"],
        &rows,
    );

    let init = equilateral_initial(1.0);
    let rows = vec![init.iter().copied().collect::<Vec<f64>>()];
    let _ = write_csv(
        &data.join("v2_initial_state.csv"),
        &["x0", "y0", "x1", "y1", "x2", "y2"],
        &rows,
    );
}
