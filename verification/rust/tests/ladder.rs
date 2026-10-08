// SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
// SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
//! Integration tests: the Rust numeric twin must reproduce the Python
//! ladder's reference numbers to the documented tolerances
//! (`verification/README.md` §5–§6). These are the CI-callable checks of
//! the M1 acceptance criteria for `verification/rust/`.

use trivortex_verify::verify::{has_passed, preset, run_ladder};

/// Cross-language pin: the Python ladder reports, for the quick preset,
/// omega_analytic = 0.477464829275686 (Gamma = 1, a = 1) and every check
/// inside its registered tolerance band. The Rust twin must agree to the
/// same bands — not necessarily bit-for-bit (different libm calls), but
/// inside every documented tolerance.
#[test]
fn quick_preset_reproduces_python_reference_verdict() {
    let p = preset("quick").unwrap();
    let run = run_ladder(p, "trivortex-verification-rust", std::time::Instant::now());
    assert!(run.all_passed, "the quick ladder must pass 4/4 like the Python twin");
}

#[test]
fn quick_preset_tolerances_match_registered_bands() {
    let p = preset("quick").unwrap();
    let run = run_ladder(p, "trivortex-verification-rust", std::time::Instant::now());

    let get = |idx: usize, name: &str| -> f64 {
        run.checks[idx]
            .iter()
            .find(|(k, _)| *k == name)
            .and_then(|(_, v)| match v {
                trivortex_verify::verify::Val::N(x) => Some(*x),
                _ => None,
            })
            .unwrap_or(f64::NAN)
    };

    // V1: residuals inside 1e-12
    assert!(get(0, "angular_separation_error") <= 1e-12);
    assert!(get(0, "periodicity_residual") <= 1e-12);
    // V2: shape 1e-10, omega 1e-6
    assert!(get(1, "shape_drift") <= 1e-10);
    assert!(get(1, "omega_relative_error") <= 1e-6);
    // V2 analytic pin from the Python protocol:
    assert!((get(1, "omega_analytic") - 0.477_464_829_275_686).abs() < 1e-12);
    // V3/V4: invariant drift inside 1e-10
    assert!(get(2, "worst_drift") <= 1e-10);
    assert!(get(3, "worst_drift") <= 1e-10);
}

#[test]
fn default_preset_stays_green() {
    let p = preset("default").unwrap();
    let run = run_ladder(p, "trivortex-verification-rust", std::time::Instant::now());
    for c in &run.checks {
        assert!(has_passed(c));
    }
}
