// SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
// SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
//! ===========================================================================
//! TRIVORTEX — RUST NUMERIC TWIN OF THE VERIFICATION LADDER V1–V4
//! ===========================================================================
//! A line-for-line floating-point port of
//! `verification/trivortex/python/verify.py` (provenance: repository main
//! branch, `verify.py` v1.0, the M0 release). The twin re-implements the same
//! three fixed objects from the published formulas and nothing else:
//!
//!   1. Theorem 3.1 closed form
//!        r_k(t)     = sqrt(C_Ch) · (1 + eps · cos(omega·t + 2πk/3))
//!        theta_k(t) = omega·t + 2πk/3
//!        omega      = (2π/T) · exp(C_Ch/π)
//!        eps        = 1 / (exp(C_Ch/π) − 1)
//!   2. The Chaplygin topological integral
//!        C_Ch = r² · (theta_dot − q · A_theta),  A_theta = 1/r
//!   3. The vortex integrals of the Kirchhoff equations
//!        H = −(1/2π) Σ_{i<j} Γ_i Γ_j ln r_ij
//!        P = Σ Γ_i x_i ,  Q = Σ Γ_i y_i ,  I = Σ Γ_i |r_i|²
//!      integrated with a classical RK4 stepper.
//!
//! INDEPENDENCE CONTRACT (same as the Python ladder): this module shares no
//! code with the core document `code/trivortex_core*.py` — the only things
//! shared are the mathematics and the numbers. The core module confines
//! itself to primitive f64 arithmetic (no collections, no I/O, no libc calls
//! beyond libm), so a no_std port is a header change plus a libm crate.
//!
//! Divergences between this ladder and the Python ladder are the early-
//! warning system for platform-specific floating-point surprises (x87 vs
//! SSE, FMA contraction, libm differences) — see `verification/rust/README.md`.
//!
//! Author: Isaev Iskhak Khamzatovich (repository owner)
//! Year: 2026
//! ===========================================================================

#![allow(clippy::needless_range_loop)]

pub const PI: f64 = std::f64::consts::PI;

// ---------------------------------------------------------------------------
// Presets (mirror of verify.py PRESETS / common/python/config.py)
// ---------------------------------------------------------------------------

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Preset {
    pub rotations: usize,
    pub steps_per_period: usize,
    pub n_points_cch: usize,
}

pub const PRESETS: [(&str, Preset); 3] = [
    ("quick", Preset { rotations: 2, steps_per_period: 2000, n_points_cch: 200 }),
    ("default", Preset { rotations: 5, steps_per_period: 4000, n_points_cch: 1000 }),
    ("full", Preset { rotations: 20, steps_per_period: 8000, n_points_cch: 2000 }),
];

#[must_use]
pub fn preset(name: &str) -> Option<Preset> {
    PRESETS.iter().find(|(n, _)| *n == name).map(|(_, p)| *p)
}

// ---------------------------------------------------------------------------
// Tolerance bands (registered in verification/README.md §6 BEFORE the code)
// ---------------------------------------------------------------------------

pub const TOL_CHAPLYGIN_DRIFT: f64 = 1e-12; // V1 periodicity residual band
pub const TOL_ANGULAR_SEP: f64 = 1e-12; // V1 equilateral separation band
pub const TOL_SHAPE_DRIFT: f64 = 1e-10; // V2 relative side drift band
pub const TOL_OMEGA_REL_ERR: f64 = 1e-6; // V2 measured-vs-analytic omega band
pub const TOL_INVARIANT_DRIFT: f64 = 1e-10; // V3/V4 relative drift band

// ---------------------------------------------------------------------------
// Section A — analytic layer (Theorem 3.1)
// ---------------------------------------------------------------------------

/// omega = (2*PI/T) * exp(C_Ch/PI) — Theorem 3.1.
#[must_use]
pub fn analytical_frequency(c_ch: f64, t_period: f64) -> f64 {
    (2.0 * PI / t_period) * (c_ch / PI).exp()
}

/// eps = 1/(exp(C_Ch/PI) - 1) — Theorem 3.1. The document's small-`C_Ch`
/// guard returns eps = 1 for C_Ch <= 0.01.
#[must_use]
pub fn analytical_amplitude(c_ch: f64) -> f64 {
    if c_ch > 0.01 {
        1.0 / ((c_ch / PI).exp() - 1.0)
    } else {
        1.0
    }
}

/// r_k(t) = sqrt(C_Ch) * (1 + eps*cos(omega*t + 2*PI*k/3)).
#[must_use]
pub fn analytical_radius(t: f64, c_ch: f64, t_period: f64, k: usize) -> f64 {
    let omega = analytical_frequency(c_ch, t_period);
    let eps = analytical_amplitude(c_ch);
    let r0 = if c_ch > 0.0 { c_ch.sqrt() } else { 0.01 };
    r0 * (1.0 + eps * (omega * t + 2.0 * PI * k as f64 / 3.0).cos())
}

/// C_Ch = r^2 * (theta_dot - q*A_theta) — the topological integral.
/// With the gauge A_theta = 1/r (the default when `a_theta` is not given).
#[must_use]
pub fn compute_chaplygin(r: f64, theta_dot: f64, q: f64, a_theta: f64) -> f64 {
    let a = if a_theta > 0.0 {
        a_theta
    } else if r > 0.0 {
        1.0 / r
    } else {
        0.0
    };
    r * r * (theta_dot - q * a)
}

/// Python-style modulo: result in [0, m) for m > 0 (Rust's `%` keeps the
/// sign of the dividend; the separation check relies on the lifted branch).
#[must_use]
pub fn python_mod(x: f64, m: f64) -> f64 {
    let r = x % m;
    if r < 0.0 {
        r + m
    } else {
        r
    }
}

/// Python-style round(): half-to-even, matching CPython's banker's rounding
/// used by the unwrap correction in V2. In practice the fractional part is
/// ~1e-9 away from an integer, so the tie branch never fires — it is here
/// for faithfulness, not for need.
#[must_use]
pub fn py_round_half_even(x: f64) -> f64 {
    let floor = x.floor();
    let diff = x - floor;
    if diff < 0.5 {
        floor
    } else if diff > 0.5 {
        floor + 1.0
    } else {
        // exactly .5 — choose the even neighbour
        if (floor as i64) % 2 == 0 {
            floor
        } else {
            floor + 1.0
        }
    }
}

/// V1 — Theorem 3.1 closed form: choreography, periodicity, and the recorded
/// Section-6 drift diagnostic.
///
/// Pass/fail criteria (registered in `verification/README.md` §5):
///   (a) the three vortices keep the exact 2π/3 angular separation at all
///       probed times (equilateral choreography), residual ≤ 1e-12;
///   (b) the closed form is periodic: r_k(t + T_r) = r_k(t) with
///       T_r = 2π/omega, residual ≤ 1e-12.
/// The gauge-dependent combination C_Ch(t) = r²(theta_dot − q·A_theta) is
/// REPORTED as a diagnostic with no pass/fail role — it oscillates by
/// construction; see the honesty notes in `verification/README.md` §13.
#[must_use]
pub fn check_v1_theorem31(c_ch: f64, t_period: f64, n_points: usize) -> Vec<(&'static str, Val)> {
    let omega = analytical_frequency(c_ch, t_period);
    let t_r = 2.0 * PI / omega;
    let t_max = 100.0 * t_period;

    // (a) equilateral choreography at the four probed times
    let mut sep_err = 0.0_f64;
    for frac in [0.0, 0.25, 0.5, 1.0] {
        let t = frac * t_max;
        let angles: Vec<f64> =
            (0..3).map(|k| omega * t + 2.0 * PI * k as f64 / 3.0).collect();
        for i in 0..3 {
            let d = python_mod(angles[(i + 1) % 3] - angles[i], 2.0 * PI);
            sep_err = sep_err.max((d - 2.0 * PI / 3.0).abs());
        }
    }

    // (b) periodicity of the closed form
    let mut per_res = 0.0_f64;
    for k in 0..3 {
        for frac in [0.0, 0.137, 0.5, 0.811] {
            let t = frac * t_max;
            let res = (analytical_radius(t + t_r, c_ch, t_period, k)
                - analytical_radius(t, c_ch, t_period, k))
                .abs();
            per_res = per_res.max(res);
        }
    }

    // diagnostic: Section-6 endpoint drift of C_Ch(t) along the closed form
    // (numpy.linspace(0, t_max, n_points) equivalent)
    let step = if n_points > 1 { t_max / (n_points - 1) as f64 } else { 0.0 };
    let mut drift = 0.0_f64;
    if n_points > 0 {
        let base = compute_chaplygin(analytical_radius(0.0, c_ch, t_period, 0), omega, 1.0, 0.0);
        for i in 0..n_points {
            let t = i as f64 * step;
            let c = compute_chaplygin(analytical_radius(t, c_ch, t_period, 0), omega, 1.0, 0.0);
            drift = drift.max((c - base).abs());
        }
    }

    let passed = sep_err <= TOL_ANGULAR_SEP && per_res <= TOL_CHAPLYGIN_DRIFT;
    let mut out: Vec<(&'static str, Val)> = vec![
        (
            "check",
            Val::S("V1 Theorem 3.1: choreography + periodicity of the closed form".into()),
        ),
        ("angular_separation_error", Val::N(sep_err)),
        ("angular_separation_tolerance", Val::N(TOL_ANGULAR_SEP)),
        ("periodicity_residual", Val::N(per_res)),
        ("periodicity_tolerance", Val::N(TOL_CHAPLYGIN_DRIFT)),
        ("section6_drift_diagnostic", Val::N(drift)),
        ("passed", Val::B(passed)),
    ];
    out.push((
        "params",
        Val::M(vec![
            ("C_Ch".into(), Val::N(c_ch)),
            ("T".into(), Val::N(t_period)),
            ("n_points".into(), Val::N(n_points as f64)),
            ("omega".into(), Val::N(omega)),
            ("window".into(), Val::S("0..100T".into())),
        ]),
    ));
    out
}

// ---------------------------------------------------------------------------
// Section B — numerical layer (point-vortex dynamics, RK4)
// ---------------------------------------------------------------------------

/// Kirchhoff equations for point vortices.
///
/// `state` = flat [x0, y0, x1, y1, ...]; `gamma[i]` circulations.
///   dx_i/dt = -1/(2π) Σ_{j≠i} Γ_j (y_i − y_j) / r_ij²
///   dy_i/dt = +1/(2π) Σ_{j≠i} Γ_j (x_i − x_j) / r_ij²
#[must_use]
pub fn vortex_rhs(state: &[f64], gamma: &[f64]) -> Vec<f64> {
    let n = gamma.len();
    let mut dxy = vec![0.0_f64; 2 * n];
    for i in 0..n {
        for j in 0..n {
            if i == j {
                continue;
            }
            let dx = state[2 * i] - state[2 * j];
            let dy = state[2 * i + 1] - state[2 * j + 1];
            let r2 = dx * dx + dy * dy;
            if r2 == 0.0 {
                continue;
            }
            dxy[2 * i] += -gamma[j] * dy / r2 / (2.0 * PI);
            dxy[2 * i + 1] += gamma[j] * dx / r2 / (2.0 * PI);
        }
    }
    dxy
}

/// One classical RK4 step of the vortex dynamics.
#[must_use]
pub fn rk4_step(state: &[f64], gamma: &[f64], dt: f64) -> Vec<f64> {
    let k1 = vortex_rhs(state, gamma);
    let s2: Vec<f64> = state.iter().zip(&k1).map(|(s, k)| s + 0.5 * dt * k).collect();
    let k2 = vortex_rhs(&s2, gamma);
    let s3: Vec<f64> = state.iter().zip(&k2).map(|(s, k)| s + 0.5 * dt * k).collect();
    let k3 = vortex_rhs(&s3, gamma);
    let s4: Vec<f64> = state.iter().zip(&k3).map(|(s, k)| s + dt * k).collect();
    let k4 = vortex_rhs(&s4, gamma);
    state
        .iter()
        .zip(&k1)
        .zip(&k2)
        .zip(&k3)
        .zip(&k4)
        .map(|((((s, a), b), c), d)| s + (dt / 6.0) * (a + 2.0 * b + 2.0 * c + d))
        .collect()
}

/// H, P, Q, I — the classical (Chaplygin-type) vortex integrals.
#[must_use]
pub fn invariants(state: &[f64], gamma: &[f64]) -> [f64; 4] {
    let n = gamma.len();
    let mut h = 0.0_f64;
    for i in 0..n {
        for j in (i + 1)..n {
            let dx = state[2 * i] - state[2 * j];
            let dy = state[2 * i + 1] - state[2 * j + 1];
            let r = (dx * dx + dy * dy).sqrt();
            h += -gamma[i] * gamma[j] * r.ln() / (2.0 * PI);
        }
    }
    let mut p = 0.0_f64;
    let mut q = 0.0_f64;
    let mut imp = 0.0_f64;
    for i in 0..n {
        let x = state[2 * i];
        let y = state[2 * i + 1];
        p += gamma[i] * x;
        q += gamma[i] * y;
        imp += gamma[i] * (x * x + y * y);
    }
    [h, p, q, imp]
}

/// Three equal vortices on an equilateral triangle of side `a`,
/// circumradius r = a/sqrt(3), flat [x0, y0, x1, y1, x2, y2].
#[must_use]
pub fn equilateral_initial(a: f64) -> Vec<f64> {
    let r = a / 3.0_f64.sqrt();
    let mut pts = Vec::with_capacity(6);
    for k in 0..3 {
        let ang = 2.0 * PI * k as f64 / 3.0;
        pts.push(r * ang.cos());
        pts.push(r * ang.sin());
    }
    pts
}

/// Analytic angular velocity of the rigidly rotating equilateral triangle:
/// omega = 3*Gamma/(2*PI*a^2) — the point-vortex Lagrange solution.
#[must_use]
pub fn lagrange_omega(gamma: f64, a: f64) -> f64 {
    3.0 * gamma / (2.0 * PI * a * a)
}

#[must_use]
pub fn side_lengths(xy: &[f64]) -> [f64; 3] {
    let d = |i: usize, j: usize| {
        let dx = xy[2 * i] - xy[2 * j];
        let dy = xy[2 * i + 1] - xy[2 * j + 1];
        (dx * dx + dy * dy).sqrt()
    };
    [d(0, 1), d(1, 2), d(2, 0)]
}

fn worst_drift(inv0: &[f64; 4], inv1: &[f64; 4]) -> ([(&'static str, f64); 4], f64) {
    let mut worst = 0.0_f64;
    let mut drifts = [("H", 0.0_f64), ("P", 0.0), ("Q", 0.0), ("I", 0.0)];
    for k in 0..4 {
        let d = (inv1[k] - inv0[k]).abs() / inv0[k].abs().max(1.0);
        drifts[k].1 = d;
        worst = worst.max(d);
    }
    (drifts, worst)
}

/// V2 — rigid rotation + measured vs analytic omega.
/// When `track` is true the trajectory is sampled every `track_every` steps
/// for later SVG plotting; the returned vector holds (t, [x0,y0,…,x2,y2]).
#[must_use]
#[allow(clippy::too_many_arguments)]
pub fn check_v2_lagrange_rotation(
    gamma: f64,
    a: f64,
    rotations: usize,
    steps_per_period: usize,
    track: bool,
) -> (Vec<(&'static str, Val)>, Vec<(f64, [f64; 6])>) {
    let mut state = equilateral_initial(a);
    let omega = lagrange_omega(gamma, a);
    let period = 2.0 * PI / omega;
    let dt = period / steps_per_period as f64;
    let gamma_vec = [gamma, gamma, gamma];

    let ang_start = state[1].atan2(state[0]);
    let n_steps = rotations * steps_per_period;
    let track_every = if track { (n_steps / 400).max(1) } else { usize::MAX };
    let mut trajectory: Vec<(f64, [f64; 6])> = Vec::new();

    for (step, ()) in std::iter::repeat(()).take(n_steps).enumerate() {
        state = rk4_step(&state, &gamma_vec, dt);
        if track && step % track_every == 0 {
            let mut snap = [0.0_f64; 6];
            snap.copy_from_slice(&state);
            trajectory.push((step as f64 * dt, snap));
        }
    }

    let ang_end = state[1].atan2(state[0]);

    // Unwrap: lift the raw angle difference to the branch closest to the
    // expected unwrapped angle, so whole turns and atan2 branch flips
    // (angle returning as -1e-9 instead of +2π − 1e-9) are handled.
    let expected_total = omega * n_steps as f64 * dt;
    let raw_diff = ang_end - ang_start;
    let measured_total =
        raw_diff + 2.0 * PI * py_round_half_even((expected_total - raw_diff) / (2.0 * PI));
    let omega_rel_err = (measured_total - expected_total).abs() / expected_total;

    let sides = side_lengths(&state);
    let shape_drift = sides.iter().fold(0.0_f64, |m, s| m.max((s - a).abs())) / a;

    let passed = shape_drift <= TOL_SHAPE_DRIFT && omega_rel_err <= TOL_OMEGA_REL_ERR;
    let mut out: Vec<(&'static str, Val)> = vec![
        (
            "check",
            Val::S("V2 Lagrange rigid rotation: shape + analytic omega = 3G/(2pi a^2)".into()),
        ),
        ("shape_drift", Val::N(shape_drift)),
        ("shape_tolerance", Val::N(TOL_SHAPE_DRIFT)),
        ("omega_analytic", Val::N(omega)),
        ("omega_relative_error", Val::N(omega_rel_err)),
        ("omega_tolerance", Val::N(TOL_OMEGA_REL_ERR)),
        ("passed", Val::B(passed)),
    ];
    out.push((
        "params",
        Val::M(vec![
            ("Gamma".into(), Val::N(gamma)),
            ("a".into(), Val::N(a)),
            ("rotations".into(), Val::N(rotations as f64)),
            ("steps_per_period".into(), Val::N(steps_per_period as f64)),
            ("dt".into(), Val::N(dt)),
        ]),
    ));
    (out, trajectory)
}

/// V3 — H, P, Q, I conserved along the Lagrange trajectory.
#[must_use]
pub fn check_v3_invariants(
    gamma: f64,
    a: f64,
    rotations: usize,
    steps_per_period: usize,
) -> Vec<(&'static str, Val)> {
    let state = equilateral_initial(a);
    let omega = lagrange_omega(gamma, a);
    let dt = (2.0 * PI / omega) / steps_per_period as f64;
    let gamma_vec = [gamma, gamma, gamma];

    let inv0 = invariants(&state, &gamma_vec);
    let mut cur = state;
    let n_steps = rotations * steps_per_period;
    for _ in 0..n_steps {
        cur = rk4_step(&cur, &gamma_vec, dt);
    }
    let inv1 = invariants(&cur, &gamma_vec);

    let (drifts, worst) = worst_drift(&inv0, &inv1);
    let passed = worst <= TOL_INVARIANT_DRIFT;
    let mut out: Vec<(&'static str, Val)> = vec![
        (
            "check",
            Val::S("V3 vortex integrals: H, P, Q, I conserved (equal Gamma)".into()),
        ),
        (
            "relative_drifts",
            Val::M(drifts.iter().map(|(k, v)| ((*k).into(), Val::N(*v))).collect()),
        ),
        ("worst_drift", Val::N(worst)),
        ("tolerance", Val::N(TOL_INVARIANT_DRIFT)),
        ("passed", Val::B(passed)),
    ];
    out.push((
        "params",
        Val::M(vec![
            ("Gamma".into(), Val::N(gamma)),
            ("a".into(), Val::N(a)),
            ("rotations".into(), Val::N(rotations as f64)),
            ("steps_per_period".into(), Val::N(steps_per_period as f64)),
        ]),
    ));
    out
}

/// V4 — integrals conserved for unequal circulations (no symmetry needed).
#[must_use]
pub fn check_v4_robustness(
    gammas: [f64; 3],
    a: f64,
    rotations: usize,
    steps_per_period: usize,
) -> Vec<(&'static str, Val)> {
    // Generic triangle, centroid shifted to the origin.
    let cy = 3.0_f64.sqrt() / 2.0 * a;
    let cx = (0.0 + a + 0.5 * a) / 3.0;
    let cyy = cy / 3.0;
    let state: Vec<f64> = vec![
        0.0 - cx,
        0.0 - cyy,
        a - cx,
        0.0 - cyy,
        0.5 * a - cx,
        cy - cyy,
    ];
    let gamma_vec = gammas;

    let inv0 = invariants(&state, &gamma_vec);
    // Reference period from the mean circulation scale (integration window).
    let mean_gamma = (gammas[0] + gammas[1] + gammas[2]) / 3.0;
    let omega_ref = lagrange_omega(mean_gamma, a);
    let dt = (2.0 * PI / omega_ref) / steps_per_period as f64;
    let mut cur = state;
    let n_steps = rotations * steps_per_period;
    for _ in 0..n_steps {
        cur = rk4_step(&cur, &gamma_vec, dt);
    }
    let inv1 = invariants(&cur, &gamma_vec);

    let (drifts, worst) = worst_drift(&inv0, &inv1);
    let passed = worst <= TOL_INVARIANT_DRIFT;
    let mut out: Vec<(&'static str, Val)> = vec![
        (
            "check",
            Val::S("V4 robustness: H, P, Q, I conserved for Gamma = (1, 2, 3)".into()),
        ),
        (
            "relative_drifts",
            Val::M(drifts.iter().map(|(k, v)| ((*k).into(), Val::N(*v))).collect()),
        ),
        ("worst_drift", Val::N(worst)),
        ("tolerance", Val::N(TOL_INVARIANT_DRIFT)),
        ("passed", Val::B(passed)),
    ];
    out.push((
        "params",
        Val::M(vec![
            (
                "Gamma".into(),
                Val::L(gammas.iter().map(|g| Val::N(*g)).collect()),
            ),
            ("a".into(), Val::N(a)),
            ("rotations".into(), Val::N(rotations as f64)),
            ("steps_per_period".into(), Val::N(steps_per_period as f64)),
        ]),
    ));
    out
}

// ---------------------------------------------------------------------------
// Runner — the JSON-protocol ladder
// ---------------------------------------------------------------------------

/// A dynamically-typed value for the JSON protocol (schema-compatible with
/// the Python ladder's report — see verification/README.md §12).
#[derive(Clone, Debug)]
pub enum Val {
    N(f64),
    S(String),
    B(bool),
    L(Vec<Val>),
    M(Vec<(String, Val)>),
}

/// Run the four checks with the given preset parameters. `suite` names the
/// emitting implementation (e.g. "trivortex-verification-rust").
#[must_use]
pub fn run_ladder(p: Preset, suite: &str, t0: std::time::Instant) -> LadderRun {
    let v1 = check_v1_theorem31(1.0, 2.0 * PI, p.n_points_cch);
    let (v2, _traj) = check_v2_lagrange_rotation(1.0, 1.0, p.rotations, p.steps_per_period, false);
    let v3 = check_v3_invariants(1.0, 1.0, p.rotations, p.steps_per_period);
    let v4 = check_v4_robustness(
        [1.0, 2.0, 3.0],
        1.0,
        p.rotations.saturating_sub(2).max(2),
        p.steps_per_period,
    );
    let checks = vec![v1, v2, v3, v4];
    let n_pass = checks.iter().filter(|c| has_passed(c)).count();
    let all = n_pass == checks.len();
    let wall = t0.elapsed().as_secs_f64();

    let preset_name = PRESETS
        .iter()
        .find(|(_, q)| *q == p)
        .map_or("default", |(n, _)| *n);

    let report = vec![
        ("suite".to_string(), Val::S(suite.to_string())),
        ("version".to_string(), Val::S("1.0".into())),
        ("preset".to_string(), Val::S(preset_name.to_string())),
        ("date_utc".to_string(), Val::S(crate::report::utc_now_iso())),
        ("wall_time_s".to_string(), Val::N(wall)),
        ("checks_passed".to_string(), Val::N(n_pass as f64)),
        ("checks_total".to_string(), Val::N(checks.len() as f64)),
        ("all_passed".to_string(), Val::B(all)),
        (
            "checks".to_string(),
            Val::L(checks.iter().map(|c| Val::M(named(c))).collect()),
        ),
    ];
    LadderRun { report, checks, all_passed: all, wall_time_s: wall }
}

fn named(c: &[(&'static str, Val)]) -> Vec<(String, Val)> {
    c.iter().map(|(k, v)| ((*k).to_string(), v.clone())).collect()
}

/// True when the check's `passed` field is present and true.
#[must_use]
pub fn has_passed(c: &[(&'static str, Val)]) -> bool {
    c.iter().any(|(k, v)| *k == "passed" && matches!(v, Val::B(true)))
}

/// The ladder result bundle.
pub struct LadderRun {
    /// The JSON-compatible report tree (schema of verification/README.md §12).
    pub report: Vec<(String, Val)>,
    /// Raw per-check field lists, in V1..V4 order.
    pub checks: Vec<Vec<(&'static str, Val)>>,
    /// Verdict: every check passed against its registered tolerance.
    pub all_passed: bool,
    /// Wall time of the whole run, seconds.
    pub wall_time_s: f64,
}

// ---------------------------------------------------------------------------
// Tests — the pinned reference values (pinned, not assumed: each expected
// value is recomputed from the closed form here, mirroring test_trivortex.py)
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    fn close(a: f64, b: f64, rel: f64) -> bool {
        (a - b).abs() <= rel * b.abs().max(1.0)
    }

    #[test]
    fn frequency_reference_value() {
        // omega = (2*pi/T) * exp(C_Ch/pi), C_Ch = 1, T = 2*pi
        let expected = (2.0 * PI / (2.0 * PI)) * (1.0 / PI).exp();
        assert!(close(analytical_frequency(1.0, 2.0 * PI), expected, 1e-15));
        assert!(close(expected, 1.374_802_227_439_358_8, 1e-12));
    }

    #[test]
    fn amplitude_reference_value() {
        let expected = 1.0 / ((1.0 / PI).exp() - 1.0);
        assert!(close(analytical_amplitude(1.0), expected, 1e-15));
    }

    #[test]
    fn amplitude_small_cch_guard() {
        // for C_Ch <= 0.01 the document's guard returns eps = 1
        assert_eq!(analytical_amplitude(0.005), 1.0);
    }

    #[test]
    fn closed_form_periodicity() {
        let omega = analytical_frequency(1.0, 2.0 * PI);
        let t_r = 2.0 * PI / omega;
        for k in 0..3 {
            let r1 = analytical_radius(1.234, 1.0, 2.0 * PI, k);
            let r2 = analytical_radius(1.234 + t_r, 1.0, 2.0 * PI, k);
            assert!((r1 - r2).abs() <= 1e-12);
        }
    }

    #[test]
    fn chaplygin_formula_shape() {
        // C_Ch = r^2 * (theta_dot - q * A_theta); with A_theta = 1/r:
        // C_Ch = r^2 * theta_dot - q * r
        let (r, theta_dot, q) = (0.5, 2.0, 1.0);
        assert!(close(
            compute_chaplygin(r, theta_dot, q, 0.0),
            r * r * theta_dot - q * r,
            1e-15
        ));
    }

    #[test]
    fn analytic_omega_reference() {
        assert!(close(lagrange_omega(1.0, 1.0), 3.0 / (2.0 * PI), 1e-15));
        assert!(close(lagrange_omega(2.0, 3.0), 6.0 / (2.0 * PI * 9.0), 1e-15));
    }

    #[test]
    fn equilateral_initial_shape() {
        let state = equilateral_initial(1.0);
        let sides = side_lengths(&state);
        for s in sides {
            assert!((s - 1.0).abs() <= 1e-14);
        }
    }

    #[test]
    fn vortex_rhs_rigid_rotation_of_pair() {
        // two equal vortices at (+1,0) and (-1,0): no radial motion, and the
        // pair rotates counter-clockwise (right vortex up, left vortex down)
        let state = [1.0, 0.0, -1.0, 0.0];
        let gamma = [1.0, 1.0];
        let d = vortex_rhs(&state, &gamma);
        assert!(d[0].abs() <= 1e-15);
        assert!(d[2].abs() <= 1e-15);
        assert!(close(d[1], 0.5 / (2.0 * PI), 1e-14));
        assert!(close(d[3], -0.5 / (2.0 * PI), 1e-14));
    }

    #[test]
    fn python_mod_branches() {
        let two_pi = 2.0 * PI;
        assert!((python_mod(-4.0 * PI / 3.0, two_pi) - 2.0 * PI / 3.0).abs() <= 1e-15);
        assert!((python_mod(2.0 * PI / 3.0, two_pi) - 2.0 * PI / 3.0).abs() <= 1e-15);
    }

    #[test]
    fn quick_ladder_v1_to_v4_pass() {
        let p = preset("quick").unwrap();
        let run = run_ladder(p, "trivortex-verification-rust", std::time::Instant::now());
        assert_eq!(run.checks.len(), 4);
        for (i, c) in run.checks.iter().enumerate() {
            assert!(has_passed(c), "check V{} failed: {:#?}", i + 1, c);
        }
        assert!(run.all_passed);
    }

    #[test]
    fn report_schema_shape() {
        let p = preset("quick").unwrap();
        let run = run_ladder(p, "trivortex-verification-rust", std::time::Instant::now());
        let keys: Vec<&str> = run.report.iter().map(|(k, _)| k.as_str()).collect();
        for expected in [
            "suite",
            "version",
            "preset",
            "date_utc",
            "wall_time_s",
            "checks_passed",
            "checks_total",
            "all_passed",
            "checks",
        ] {
            assert!(keys.contains(&expected), "missing field {expected}");
        }
    }
}
