// SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
// SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
//! TRIVORTEX verification lab — bilingual interface strings (EN / RU).
//!
//! The lab speaks the repository's two languages: English by default (the
//! language of the code, the monographs EN and the CI), Russian on request
//! (the language of the core document RU and the owner's notes).

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Lang {
    En,
    Ru,
}

#[must_use]
pub fn from_code(code: &str) -> Lang {
    if code.eq_ignore_ascii_case("ru") {
        Lang::Ru
    } else {
        Lang::En
    }
}

/// All user-facing strings of the interactive laboratory.
pub struct Strings;

macro_rules! bi {
    ($field:ident, $en:expr, $ru:expr) => {
        impl Strings {
            #[must_use]
            pub fn $field(&self, l: Lang) -> &'static str {
                match l {
                    Lang::En => $en,
                    Lang::Ru => $ru,
                }
            }
        }
    };
}

bi!(welcome, "TRIVORTEX — Verification Laboratory (Rust port, milestone M1)", "TRIVORTEX — Лаборатория верификации (порт Rust, веха M1)");
bi!(choose_lang, "Language / Язык: [1] English  [2] Русский", "Language / Язык: [1] English  [2] Русский");
bi!(menu_title, "MAIN MENU", "ГЛАВНОЕ МЕНЮ");
bi!(m1, "1) Run the verification ladder V1-V4 (preset)", "1) Запустить лестницу верификации V1-V4 (пресет)");
bi!(m2, "2) Custom parameters (C_Ch, T, Gamma, a, rotations, steps)", "2) Свои параметры (C_Ch, T, Gamma, a, обороты, шаги)");
bi!(m3, "3) Analysis: convergence study (omega error vs steps)", "3) Анализ: сходимость (ошибка omega от числа шагов)");
bi!(m4, "4) Plots: export SVG figures (vector, any dpi)", "4) Графики: экспорт SVG (вектор, любое dpi)");
bi!(m5, "5) Export CSV data (trajectory, diagnostics)", "5) Экспорт CSV (траектория, диагностика)");
bi!(m6, "6) Show latest JSON protocol", "6) Показать последний JSON-протокол");
bi!(m0, "0) Exit", "0) Выход");
bi!(prompt_choice, "choice> ", "выбор> ");
bi!(preset_prompt, "Preset [quick/default/full] (default: default): ", "Пресет [quick/default/full] (по умолчанию: default): ");
bi!(cch_prompt, "C_Ch (> 0) [1.0]: ", "C_Ch (> 0) [1.0]: ");
bi!(t_prompt, "T period [6.283185307179586]: ", "Период T [6.283185307179586]: ");
bi!(gamma_prompt, "Gamma (equal circulations) [1.0]: ", "Гамма (одинаковые циркуляции) [1.0]: ");
bi!(a_prompt, "Triangle side a [1.0]: ", "Сторона треугольника a [1.0]: ");
bi!(rot_prompt, "Rotations [5]: ", "Обороты [5]: ");
bi!(spp_prompt, "Steps per period [4000]: ", "Шагов на период [4000]: ");
bi!(running, "Running the ladder ...", "Лестница запущена ...");
bi!(result_line, "RESULT", "ИТОГ");
bi!(checks_passed, "checks passed", "проверок пройдено");
bi!(preset, "preset", "пресет");
bi!(wall, "wall time", "время");
bi!(json_saved, "JSON protocol saved to", "JSON-протокол сохранён в");
bi!(plots_saved, "SVG plots saved to", "SVG-графики сохранены в");
bi!(csv_saved, "CSV data saved to", "CSV-данные сохранены в");
bi!(out_dir_prompt, "Output directory [verification/outputs/rust]: ", "Каталог вывода [verification/outputs/rust]: ");
bi!(conv_title, "Convergence study: measured omega error vs integration grid", "Исследование сходимости: ошибка omega от сетки интегрирования");
bi!(conv_header, "steps/period   omega_rel_err     shape_drift", "шагов/период   отн.ошибка omega  дрейф формы");
bi!(conv_running, "Integrating ...", "Интегрирование ...");
bi!(byefr, "Goodbye — and keep every number bound to a run.", "До встречи — и держите каждое число привязанным к запуску.");
bi!(invalid, "Invalid choice, try again.", "Неверный пункт, попробуйте ещё раз.");
bi!(pass_mark, "PASS", "ПРОЙДЕНО");
bi!(fail_mark, "FAIL", "ПРОВАЛ");
bi!(custom_note, "Custom run: tolerances are the registered ones (README §6).", "Свой запуск: допуски — зарегистрированные (README §6).");
bi!(lang_set_en, "Language: English", "Язык: английский");
bi!(lang_set_ru, "Язык: русский", "Язык: русский");
bi!(figure1, "fig1_closed_form.svg — r_k(t), Theorem 3.1, k = 0,1,2", "fig1_closed_form.svg — r_k(t), Теорема 3.1, k = 0,1,2");
bi!(figure2, "fig2_chaplygin_diagnostic.svg — C_Ch(t) over [0, 100T]", "fig2_chaplygin_diagnostic.svg — C_Ch(t) на [0, 100T]");
bi!(figure3, "fig3_lagrange_trajectory.svg — rigid rotation of the triangle", "fig3_lagrange_trajectory.svg — жёсткое вращение треугольника");
bi!(figure4, "fig4_convergence.svg — omega error vs grid", "fig4_convergence.svg — ошибка omega от сетки");
bi!(figure5, "fig5_v4_unequal.svg — unequal-circulation robustness (drifts)", "fig5_v4_unequal.svg — устойчивость при неравных циркуляциях");
