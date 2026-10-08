// SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
// SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
//! TRIVORTEX verification crate (Rust port, milestone M1).
//!
//! * [`verify`] — the numeric twin of the Python ladder V1–V4
//!   (the planned artifact `verification/rust/verify.rs`);
//! * [`report`] — dependency-free JSON protocol / CSV / SVG writers;
//! * [`i18n`] — bilingual (EN/RU) interface strings for the interactive lab.

pub mod i18n;
pub mod report;
pub mod verify;
