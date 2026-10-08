// SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
// SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
//! TRIVORTEX verification lab — report, data and plot writers.
//!
//! Everything here is hand-rolled on purpose: the numeric twin must stay
//! dependency-free so its floating-point path is exactly the platform's.
//! The writers emit:
//!   * JSON protocols (the schema of `verification/README.md` §12);
//!   * CSV data files (trajectories, diagnostics, convergence tables);
//!   * SVG vector plots (resolution-independent — the equivalent of any
//!     raster dpi; the same data can be re-rendered at 600 dpi by the
//!     Python laboratory `verification/trivortex/python/lab.py`).

use std::fs;
use std::io::Write;

use crate::verify::Val;

// ---------------------------------------------------------------------------
// JSON
// ---------------------------------------------------------------------------

/// Escape a string per the JSON spec (control chars + quote + backslash).
#[must_use]
pub fn json_escape(s: &str) -> String {
    let mut out = String::with_capacity(s.len() + 2);
    for c in s.chars() {
        match c {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            c if (c as u32) < 0x20 => out.push_str(&format!("\\u{:04x}", c as u32)),
            c => out.push(c),
        }
    }
    out
}

/// Render a float the way Python's `json` module does for doubles:
/// shortest round-trip representation; integers keep no trailing `.0`
/// ambiguity — they keep it (Python prints 2.0 as 2.0 too).
#[must_use]
pub fn json_float(v: f64) -> String {
    if v.is_nan() || v.is_infinite() {
        return "null".to_string();
    }
    if v == v.trunc() && v.abs() < 1e16 {
        format!("{v:.1}")
    } else {
        format!("{v}")
    }
}

/// Serialize a `Val` tree as indented JSON (indent = 2, like the ladder).
#[must_use]
pub fn val_to_json(v: &Val, indent: usize) -> String {
    let pad = " ".repeat(indent);
    let pad_in = " ".repeat(indent + 2);
    match v {
        Val::N(x) => json_float(*x),
        Val::B(b) => b.to_string(),
        Val::S(s) => format!("\"{}\"", json_escape(s)),
        Val::L(items) => {
            if items.is_empty() {
                return "[]".into();
            }
            let body: Vec<String> = items
                .iter()
                .map(|it| format!("{pad_in}{}", val_to_json(it, indent + 2)))
                .collect();
            format!("[\n{}]\n{pad}", body.join(",\n"))
        }
        Val::M(fields) => {
            if fields.is_empty() {
                return "{}".into();
            }
            let body: Vec<String> = fields
                .iter()
                .map(|(k, val)| {
                    format!(
                        "{pad_in}\"{}\": {}",
                        json_escape(k),
                        val_to_json(val, indent + 2)
                    )
                })
                .collect();
            format!("{{\n{}}}\n{pad}", body.join(",\n"))
        }
    }
}

/// UTC timestamp in the same shape as Python's
/// `datetime.now(timezone.utc).isoformat()`: `2026-10-08T02:39:07.123456+00:00`.
#[must_use]
pub fn utc_now_iso() -> String {
    let secs = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap_or_default()
        .as_secs();
    let (y, mo, d, h, mi, s) = civil_from_unix(secs as i64);
    format!("{y:04}-{mo:02}-{d:02}T{h:02}:{mi:02}:{s:02}+00:00")
}

/// UTC stamp for file names: `2026-10-08_02-39-07`.
#[must_use]
pub fn utc_stamp() -> String {
    let secs = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap_or_default()
        .as_secs();
    let (y, mo, d, h, mi, s) = civil_from_unix(secs as i64);
    format!("{y:04}-{mo:02}-{d:02}_{h:02}-{mi:02}-{s:02}")
}

/// Convert unix seconds to (year, month, day, hour, minute, second) — UTC.
/// Days-based civil-from-days algorithm (Howard Hinnant, public domain).
#[must_use]
#[allow(clippy::many_single_char_names)]
pub fn civil_from_unix(secs: i64) -> (i64, u32, u32, u32, u32, u32) {
    let days = secs.div_euclid(86_400);
    let rem = secs.rem_euclid(86_400);
    let h = (rem / 3600) as u32;
    let mi = ((rem % 3600) / 60) as u32;
    let s = (rem % 60) as u32;
    let z = days + 719_468;
    let era = z.div_euclid(146_097);
    let doe = z.rem_euclid(146_097);
    let yoe = (doe - doe / 1460 + doe / 36_524 - doe / 146_096) / 365;
    let y = yoe + era * 400;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let d = (doy - (153 * mp + 2) / 5 + 1) as u32;
    let m = if mp < 10 { mp + 3 } else { mp - 9 } as u32;
    let y = if m <= 2 { y + 1 } else { y };
    (y, m, d, h, mi, s)
}

/// Write text to a file, creating parent directories as needed.
pub fn write_text(path: &std::path::Path, text: &str) -> std::io::Result<()> {
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let mut f = fs::File::create(path)?;
    f.write_all(text.as_bytes())
}

// ---------------------------------------------------------------------------
// CSV
// ---------------------------------------------------------------------------

/// Write a table (header + rows of f64) as CSV.
pub fn write_csv(path: &std::path::Path, header: &[&str], rows: &[Vec<f64>]) -> std::io::Result<()> {
    let mut out = String::new();
    out.push_str(&header.join(","));
    out.push('\n');
    for row in rows {
        let cells: Vec<String> = row.iter().map(|x| json_float(*x)).collect();
        out.push_str(&cells.join(","));
        out.push('\n');
    }
    write_text(path, &out)
}

// ---------------------------------------------------------------------------
// SVG plots (dependency-free vector graphics)
// ---------------------------------------------------------------------------

pub struct Series {
    pub label: String,
    pub points: Vec<(f64, f64)>,
    pub color: String,
}

const PALETTE: [&str; 8] = [
    "#1f6feb", "#d29922", "#3fb950", "#f85149", "#ab7df8", "#39c5cf", "#e3b341", "#ff7b72",
];

fn palette(i: usize) -> &'static str {
    PALETTE[i % PALETTE.len()]
}

fn fmt_axis(v: f64) -> String {
    let a = v.abs();
    if a == 0.0 {
        "0".into()
    } else if !(1e-3..1e6).contains(&a) {
        format!("{v:.3e}")
    } else {
        format!("{v:.4}")
    }
}

/// Render a multi-series line plot into an SVG file with axes, grid and
/// legend. 900x560 viewBox, vector strokes — sharp at any dpi.
pub fn svg_line_plot(
    path: &std::path::Path,
    title: &str,
    x_label: &str,
    y_label: &str,
    series: &[Series],
) -> std::io::Result<()> {
    let (w, h) = (900.0_f64, 560.0_f64);
    let (ml, mr, mt, mb) = (72.0_f64, 24.0_f64, 56.0_f64, 64.0_f64);
    let (pw, ph) = (w - ml - mr, h - mt - mb);

    let mut xmin = f64::INFINITY;
    let mut xmax = f64::NEG_INFINITY;
    let mut ymin = f64::INFINITY;
    let mut ymax = f64::NEG_INFINITY;
    for s in series {
        for (x, y) in &s.points {
            xmin = xmin.min(*x);
            xmax = xmax.max(*x);
            ymin = ymin.min(*y);
            ymax = ymax.max(*y);
        }
    }
    if !xmin.is_finite() {
        xmin = 0.0;
        xmax = 1.0;
        ymin = 0.0;
        ymax = 1.0;
    }
    if (xmax - xmin).abs() < 1e-300 {
        xmax += 1.0;
    }
    if (ymax - ymin).abs() < 1e-300 {
        ymax += 1.0;
    }
    let pad_y = 0.05 * (ymax - ymin);
    ymin -= pad_y;
    ymax += pad_y;

    let sx = |x: f64| ml + (x - xmin) / (xmax - xmin) * pw;
    let sy = |y: f64| mt + ph - (y - ymin) / (ymax - ymin) * ph;

    let mut svg = String::with_capacity(16_384);
    svg.push_str(&format!(
        "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {w:.0} {h:.0}\" \
         font-family=\"'Segoe UI','Helvetica Neue',Arial,sans-serif\">\n"
    ));
    svg.push_str(&format!(
        "<rect width=\"{w:.0}\" height=\"{h:.0}\" fill=\"#ffffff\"/>\n"
    ));
    svg.push_str(&format!(
        "<text x=\"{}\" y=\"34\" font-size=\"20\" font-weight=\"600\" fill=\"#1f2328\" \
         text-anchor=\"middle\">{}</text>\n",
        w / 2.0,
        xml_escape(title)
    ));

    // grid + tick labels
    for i in 0..=5 {
        let t = i as f64 / 5.0;
        let x = ml + t * pw;
        let y = mt + ph - t * ph;
        svg.push_str(&format!(
            "<line x1=\"{x:.1}\" y1=\"{mt:.1}\" x2=\"{x:.1}\" y2=\"{:.1}\" \
             stroke=\"#e6e8eb\" stroke-width=\"1\"/>\n",
            mt + ph
        ));
        svg.push_str(&format!(
            "<line x1=\"{ml:.1}\" y1=\"{y:.1}\" x2=\"{:.1}\" y2=\"{y:.1}\" \
             stroke=\"#e6e8eb\" stroke-width=\"1\"/>\n",
            ml + pw
        ));
        let xv = xmin + t * (xmax - xmin);
        let yv = ymin + t * (ymax - ymin);
        svg.push_str(&format!(
            "<text x=\"{x:.1}\" y=\"{:.1}\" font-size=\"12\" fill=\"#57606a\" \
             text-anchor=\"middle\">{}</text>\n",
            mt + ph + 20.0,
            fmt_axis(xv)
        ));
        svg.push_str(&format!(
            "<text x=\"{}\" y=\"{:.1}\" font-size=\"12\" fill=\"#57606a\" \
             text-anchor=\"end\">{}</text>\n",
            ml - 8.0,
            y + 4.0,
            fmt_axis(yv)
        ));
    }

    // axes
    svg.push_str(&format!(
        "<line x1=\"{ml:.1}\" y1=\"{:.1}\" x2=\"{:.1}\" y2=\"{:.1}\" stroke=\"#1f2328\" \
         stroke-width=\"1.4\"/>\n",
        mt + ph,
        ml + pw,
        mt + ph
    ));
    svg.push_str(&format!(
        "<line x1=\"{ml:.1}\" y1=\"{mt:.1}\" x2=\"{ml:.1}\" y2=\"{:.1}\" stroke=\"#1f2328\" \
         stroke-width=\"1.4\"/>\n",
        mt + ph
    ));

    // series polylines
    for s in series {
        if s.points.is_empty() {
            continue;
        }
        let pts: Vec<String> = s
            .points
            .iter()
            .map(|(x, y)| format!("{:.2},{:.2}", sx(*x), sy(*y)))
            .collect();
        svg.push_str(&format!(
            "<polyline fill=\"none\" stroke=\"{}\" stroke-width=\"1.8\" \
             stroke-linejoin=\"round\" points=\"{}\"/>\n",
            s.color,
            pts.join(" ")
        ));
    }

    // axis captions
    svg.push_str(&format!(
        "<text x=\"{}\" y=\"{:.1}\" font-size=\"14\" fill=\"#1f2328\" \
         text-anchor=\"middle\">{}</text>\n",
        ml + pw / 2.0,
        h - 18.0,
        xml_escape(x_label)
    ));
    svg.push_str(&format!(
        "<text x=\"20\" y=\"{:.1}\" font-size=\"14\" fill=\"#1f2328\" \
         text-anchor=\"middle\" transform=\"rotate(-90 20 {:.1})\">{}</text>\n",
        mt + ph / 2.0,
        mt + ph / 2.0,
        xml_escape(y_label)
    ));

    // legend
    let lx = ml + pw - 16.0;
    for (i, s) in series.iter().enumerate() {
        let ly = mt + 16.0 + i as f64 * 22.0;
        svg.push_str(&format!(
            "<line x1=\"{}\" y1=\"{ly:.1}\" x2=\"{}\" y2=\"{ly:.1}\" stroke=\"{}\" \
             stroke-width=\"2.4\"/>\n",
            lx - 88.0,
            lx - 60.0,
            s.color
        ));
        svg.push_str(&format!(
            "<text x=\"{}\" y=\"{:.1}\" font-size=\"12.5\" fill=\"#1f2328\" \
             text-anchor=\"end\">{}</text>\n",
            lx - 96.0,
            ly + 4.0,
            xml_escape(&s.label)
        ));
    }
    svg.push_str("</svg>\n");
    write_text(path, &svg)
}

fn xml_escape(s: &str) -> String {
    s.replace('&', "&amp;")
        .replace('<', "&lt;")
        .replace('>', "&gt;")
}

/// Assign a palette color by index.
#[must_use]
pub fn color(i: usize) -> &'static str {
    palette(i)
}
