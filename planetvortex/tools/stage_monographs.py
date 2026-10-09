#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the per-stage point monographs (15 stages x 2 languages)
into docs/monographs/stages/ — each bound to the committed protocol of
the stage: the claim, the registered tolerance, the recorded results,
the theorem links, the code entry points and the reproduction command.

    PYTHONPATH=python python3 tools/stage_monographs.py
"""

from __future__ import annotations

import json
from pathlib import Path

MINI = Path(__file__).resolve().parents[1]
PROTO = MINI / "results" / "protocols"
OUT = MINI / "docs" / "monographs" / "stages"
OUT.mkdir(parents=True, exist_ok=True)

# The per-stage content: (title_en, title_ru, claim_en, claim_ru, theorem_links, code, repro)
STAGES = {
    "P1_anchor": dict(
        en=(
            "P1 — the anchor: the exact figure literals",
            "The exact dimensions of the flat heptagonal figure (Theorem A) "
            "pinned at working precision, plus the Kepler–Earth SI anchor.",
        ),
        ru=(
            "P1 — якорь: точные литералы фигуры",
            "Точные размерности плоской семиугольной фигуры (теорема A) на "
            "рабочей точности плюс якорь Кеплера–Земли в СИ.",
        ),
        theorems="Theorem A (docs/theorems)",
        code="python/planetvortex/fano.py :: exact_literals",
    ),
    "P2_kepler_register": dict(
        en=(
            "P2 — the Kepler register",
            "The mass-corrected Kepler III is the same constant for all eight "
            "planets (Lemma D): T²/a³(1 + m/M) to 10⁻¹³; the uncorrected "
            "register and the fact-sheet provenance recorded as honest "
            "diagnostics.",
        ),
        ru=(
            "P2 — регистр Кеплера",
            "Массово-исправленный третий закон Кеплера одинаков для всех восьми "
            "планет (лемма D): T²/a³(1 + m/M) до 10⁻¹³; неисправленный регистр "
            "и происхождение из факт-листов записаны честными диагностиками.",
        ),
        theorems="Lemma D (docs/theorems)",
        code="python/planetvortex/classical.py :: kepler3_*",
    ),
    "P3_planetary_nbody": dict(
        en=(
            "P3 — the planar N-body",
            "The full Newtonian Sun + 8-planets integration: energy and "
            "angular-momentum conservation, the osculating (a, e) inside the "
            "secular band, Kepler III of the integrated motion, the "
            "perturbation hierarchy.",
        ),
        ru=(
            "P3 — плоская задача N тел",
            "Полное ньютоновское интегрирование Солнце + 8 планет: сохранение "
            "энергии и момента, оскулирующие (a, e) внутри секулярной полосы, "
            "Кеплер III интегрируемого движения, иерархия возмущений.",
        ),
        theorems="Lemma D; honesty notes (README §14)",
        code="python/planetvortex/nbody.py",
    ),
    "P4_fano_algebra": dict(
        en=(
            "P4 — the PSL(2,7) algebra",
            "168 automorphisms, the two Fano models (cyclic and binary) with "
            "an explicit isomorphism, the conjugacy of the two group copies "
            "inside S₇, the congruence of the seven line-triangles.",
        ),
        ru=(
            "P4 — алгебра PSL(2,7)",
            "168 автоморфизмов, две модели Фано (циклическая и двоичная) с "
            "явным изоморфизмом, сопряжённость двух копий группы внутри S₇, "
            "конгруэнтность семи линейных треугольников.",
        ),
        theorems="Theorem A; Theorem F (the group layer)",
        code="python/planetvortex/fano.py :: automorphism_group, find_isomorphism",
    ),
    "P5_heptagon_lattice": dict(
        en=(
            "P5 — the heptagon vortex lattice",
            "The rigid rotation ω₇ = 3Γ/(2πR²) measured to 10⁻¹², the "
            "invariants along the flow, the Havelock stability of N = 7 "
            "(Theorem C) — the last stable level.",
        ),
        ru=(
            "P5 — вихревая решётка семиугольника",
            "Жёсткое вращение ω₇ = 3Γ/(2πR²) измерено до 10⁻¹², инварианты "
            "вдоль потока, хавелоковская устойчивость N = 7 (теорема C) — "
            "последний устойчивый уровень.",
        ),
        theorems="Theorem C (docs/theorems)",
        code="python/planetvortex/model.py :: corotating_spectrum",
    ),
    "P6_seven_cells": dict(
        en=(
            "P6 — the seven Fano cells",
            "The seven three-vortex cells carry exactly equal Hamiltonians "
            "(Theorem B) and congruent shape cycles with spread 0.0 — the "
            "combinatorial congruence of PSL(2,7) as a dynamical one.",
        ),
        ru=(
            "P6 — семь ячеек Фано",
            "Семь трёхвихревых ячеек несут в точности равные гамильтонианы "
            "(теорема B) и конгруэнтные циклы формы с разбросом 0,0 — "
            "комбинаторная конгруэнтность PSL(2,7) как динамическая.",
        ),
        theorems="Theorem B (docs/theorems)",
        code="python/planetvortex/ladder.py :: check_p6_cells",
    ),
    "P7_gravity_bridge": dict(
        en=(
            "P7 — the gravity bridge",
            "The Schwarzschild ladder r_s = 2GM/c², the adjacent Hill margins "
            "(the non-crossing certificate), and the mass-ladder deficit of "
            "Lemma E recorded honestly: the figure is mass-blind, the solar "
            "system is not.",
        ),
        ru=(
            "P7 — гравитационный мост",
            "Лестница Шварцшильда r_s = 2GM/c², соседние поля Хилла "
            "(сертификат непересечения) и дефицит лестницы масс леммы E, "
            "записанный честно: фигура слепа к массе, Солнечная система — нет.",
        ),
        theorems="Lemma E (docs/theorems)",
        code="python/planetvortex/classical.py :: schwarzschild_radius_m, hill_radius_au",
    ),
    "X1_sl2_enumeration": dict(
        en=(
            "X1 — PSL(2,7) from nothing",
            "All 2401 matrices over F₇ enumerated: |GL| = 2016, |SL| = 336, "
            "|PSL| = 168; the class equation 1 + 21 + 42 + 56 + 24 + 24; "
            "simplicity over all 32 unions of classes.",
        ),
        ru=(
            "X1 — PSL(2,7) из ничего",
            "Все 2401 матрицы над F₇ перечислены: |GL| = 2016, |SL| = 336, "
            "|PSL| = 168; уравнение классов 1 + 21 + 42 + 56 + 24 + 24; "
            "простота по всем 32 объединениям классов.",
        ),
        theorems="Theorem F (the group layer)",
        code="python/planetvortex/hardcore.py :: check_x1_enumeration",
    ),
    "X2_group_actions": dict(
        en=(
            "X2 — the two natural actions",
            "The action on 7 points (the S₄ subgroups) — faithful, "
            "transitive, conjugate to the research model inside S₇; the "
            "action on 8 points (the Sylow-7s) — 2-transitive; the Sylow "
            "census n₂ = 21, n₃ = 28, n₇ = 8.",
        ),
        ru=(
            "X2 — два естественных действия",
            "Действие на 7 точках (подгруппы S₄) — верное, транзитивное, "
            "сопряжённое исследовательской модели внутри S₇; действие на 8 "
            "точках (силовские 7) — 2-транзитивное; силовский контроль "
            "n₂ = 21, n₃ = 28, n₇ = 8.",
        ),
        theorems="Theorem F; Lemma F",
        code="python/planetvortex/hardcore.py :: check_x2_actions",
    ),
    "X3_triangle_hurwitz": dict(
        en=(
            "X3 — the (2,3,7) triangle generation",
            "EVERY (2,3,7) pair generates the whole group; the Klein "
            "relations; the Hurwitz arithmetic 84(g−1) = 168 = 42(2g−2); the "
            "smoothness of the Klein quartic x³y + y³z + z³x (the "
            "28(xyz)³ = 0 contradiction), genus 3.",
        ),
        ru=(
            "X3 — треугольное порождение (2,3,7)",
            "КАЖДАЯ пара (2,3,7) порождает всю группу; соотношения Клейна; "
            "арифметика Хурвица 84(g−1) = 168 = 42(2g−2); гладкость квартики "
            "Клейна x³y + y³z + z³x (противоречие 28(xyz)³ = 0), род 3.",
        ),
        theorems="Theorem F (the generation layer)",
        code="python/planetvortex/hardcore.py :: check_x3_triangle",
    ),
    "X4_hyperbolic_figure": dict(
        en=(
            "X4 — the hyperbolic {7,3} figure",
            "The exact half-edge, inradius and circumradius closed forms at "
            "50 dps; the hyperbolic Pythagoras; the area ladder π/42 → π/3 → "
            "8π; the combinatorial closure 3V = 7F = 2E = 168; the "
            "Poincaré-disk witness solved by bisection.",
        ),
        ru=(
            "X4 — гиперболическая фигура {7,3}",
            "Точные замкнутые формы полуребра, вписанного и описанного "
            "радиусов при 50 dps; гиперболический Пифагор; лестница площадей "
            "π/42 → π/3 → 8π; комбинаторное замыкание 3V = 7F = 2E = 168; "
            "свидетель в диске Пуанкаре, решённый бисекцией.",
        ),
        theorems="Theorem G (the per-register layer)",
        code="python/planetvortex/hardcore.py :: check_x4_hyperbolic",
    ),
    "X5_integrator_certification": dict(
        en=(
            "X5 — the integrator certification",
            "The measured orders 2 (leapfrog) and 4 (Yoshida); "
            "time-reversibility to roundoff; the bounded symplectic energy "
            "with no secular trend against the RK4 control; the "
            "Laplace–Runge–Lenz vector and the exact orbit equation.",
        ),
        ru=(
            "X5 — сертификация интегратора",
            "Измеренные порядки 2 (leapfrog) и 4 (Yoshida); обратимость по "
            "времени до округления; ограниченная симплектическая энергия без "
            "секулярного тренда против RK4-контроля; вектор "
            "Лапласа–Рунге–Ленца и точное уравнение орбиты.",
        ),
        theorems="The numerical discipline of the bench",
        code="python/planetvortex/hardcore.py :: check_x5_integrator",
    ),
    "X6_pn_perihelion": dict(
        en=(
            "X6 — the GR bridge",
            "The 1PN perihelion precession measured against the closed form "
            "6πGM/(a(1−e²)c²); the Newtonian control at integrator zero; "
            "Mercury 42.982″/century against the textbook 42.98″.",
        ),
        ru=(
            "X6 — мост к ОТО",
            "Перигелийное прецессирование 1PN против замкнутой формы "
            "6πGM/(a(1−e²)c²); ньютоновский контроль на интеграторном нуле; "
            "Меркурий 42,982″/столетие против учебных 42,98″.",
        ),
        theorems="The GR honesty note (README §14)",
        code="python/planetvortex/hardcore.py :: check_x6_pn_perihelion",
    ),
    "V1_inclined_registers": dict(
        en=(
            "V1 — the spatial registers",
            "The SO(3) tilt algebra of the 11-body inclination register, the "
            "exact arc registers λ = R̄·i (Lemma G), the mutual-inclination "
            "matrix with the Eris extreme, and the full 3D Newtonian run "
            "from the real J2000 sky.",
        ),
        ru=(
            "V1 — пространственные регистры",
            "SO(3)-алгебра наклонов 11-телного реестра, точные дуговые "
            "регистры λ = R̄·i (лемма G), матрица взаимных наклонений с "
            "экстремумом Эриды и полный 3D ньютоновский прогон по реальному "
            "небу J2000.",
        ),
        theorems="Lemma G (docs/theorems)",
        code="python/planetvortex/spatial.py :: check_v1_inclined",
    ),
    "V2_klein_tiling": dict(
        en=(
            "V2 — the closed gravifigure",
            "The full 24-heptagon tessellation {7,3}₈ of the Klein quartic "
            "as the coset geometry of the certified PSL(2,7) (Theorem F); "
            "the antipodal pairing (Lemma F); the 12-body gravimetric "
            "register with the EXACT budget closure Σα = 8π (Theorem G); "
            "the PGL(2,7) flag certificate and the chamber-grown disk patch.",
        ),
        ru=(
            "V2 — замкнутая гравифигура",
            "Полное 24-семиугольное разбиение {7,3}₈ квартики Клейна как "
            "косет-геометрия сертифицированного PSL(2,7) (теорема F); "
            "антиподальное паросочетание (лемма F); 12-телный гравиметрический "
            "регистр с ТОЧНЫМ замыканием бюджета Σα = 8π (теорема G); "
            "флаговый сертификат PGL(2,7) и патч chambers в диске.",
        ),
        theorems="Theorem F, Lemma F, Theorem G, Proposition H",
        code="python/planetvortex/klein.py :: check_v2_klein_tiling",
    ),
}


def _fmt_val(v, depth=0):
    """Compact rendering of a protocol value."""
    if isinstance(v, bool):
        return "PASS" if v else "FAIL"
    if isinstance(v, (int,)):
        return str(v)
    if isinstance(v, float):
        return f"{v:.6g}" if abs(v) < 1e6 else f"{v:.6e}"
    if isinstance(v, str):
        return v if len(v) < 90 else v[:87] + "..."
    if isinstance(v, dict):
        return json.dumps(v, ensure_ascii=False)[:120]
    if isinstance(v, list):
        if len(v) > 4:
            return f"[{len(v)} items]"
        return "[" + ", ".join(_fmt_val(x) for x in v) + "]"
    return str(v)


def _protocol_table(check: dict, lang: str) -> list:
    header = (
        ("| register | recorded |", "|---|---|")
        if lang == "en"
        else ("| регистр | записано |", "|---|---|")
    )
    lines = [header[0], header[1]]
    skip = {"check", "params", "passed"}
    for key, val in check.items():
        if key in skip:
            continue
        lines.append(f"| `{key}` | {_fmt_val(val)} |")
    return lines


def build_stage(slug: str, lang: str) -> str:
    info = STAGES[slug]
    stage_code = slug[0]
    rest = slug.split("_", 1)[1]
    proto_path = PROTO / f"{slug}_default.json"
    if not proto_path.exists():
        raise SystemExit(f"missing protocol {proto_path} — run `make all-ladders`")
    with proto_path.open("r", encoding="utf-8") as fh:
        proto = json.load(fh)
    check = proto["check"]
    params = check.get("params", {})
    if lang == "en":
        title, claim = info["en"]
        t_label, c_label, tol_label = "The claim", "The recorded run", "The registered tolerance"
        repro = (
            "```bash\n"
            f"cd planetvortex\n"
            f"PYTHONPATH=python python3 python/planetvortex/runner.py "
            f"--suite {'p' if stage_code == 'P' else 'x' if stage_code == 'X' else 'v'} "
            f"--stage {stage_code} --preset default\n"
            "```\n"
        )
        links = {"P": "../..", "X": "../..", "V": "../.."}[stage_code]
    else:
        title, claim = info["ru"]
        t_label, c_label, tol_label = "Утверждение", "Записанный прогон", "Зафиксированный допуск"
        repro = (
            "```bash\n"
            f"cd planetvortex\n"
            f"PYTHONPATH=python python3 python/planetvortex/runner.py "
            f"--suite {'p' if stage_code == 'P' else 'x' if stage_code == 'X' else 'v'} "
            f"--stage {stage_code} --preset default\n"
            "```\n"
        )
    status = "PASS" if check["passed"] else "FAIL"
    lines = [
        f"---",
        f'title: "{title}"',
        f'subtitle: "PLANETVORTEX — the stage monograph ({stage_code})"',
        "---",
        "",
        f"## {t_label}",
        "",
        claim,
        "",
        f"**{'Theorems' if lang == 'en' else 'Теоремы'}:** {info['theorems']}.  ",
        f"**{'Code' if lang == 'en' else 'Код'}:** `{info['code']}`.",
        "",
        f"## {c_label}",
        "",
        f"*{'Status' if lang == 'en' else 'Статус'}: **{status}** · "
        f"{'suite' if lang == 'en' else 'сьют'} `{proto['suite']}` · "
        f"{'version' if lang == 'en' else 'версия'} {proto['version']} · "
        f"{'date' if lang == 'en' else 'дата'} {proto['date_utc'][:10]}*",
        "",
    ]
    lines += _protocol_table(check, lang)
    lines += [
        "",
        f"**{'Parameters' if lang == 'en' else 'Параметры'}:** "
        f"`{json.dumps(params, ensure_ascii=False)}`",
        "",
    ]
    lines += [repro]
    return "\n".join(lines)


def main() -> None:
    count = 0
    for slug in STAGES:
        for lang in ("en", "ru"):
            stage_code = slug.split("_")[0]
            path = OUT / f"{stage_code}_{slug.split('_', 1)[1]}_{lang.upper()}.md"
            path.write_text(build_stage(slug, lang), encoding="utf-8")
            count += 1
    index = [
        "# `docs/monographs/stages/` — the per-stage point monographs",
        "",
        "One compact monograph per stage of the bench, in both languages,",
        "each bound to the committed JSON protocol of the stage: the claim,",
        "the registered tolerance, the recorded results, the theorem links,",
        "the code entry points and the reproduction command.",
        "",
        "Regenerate with `make stage-monographs`",
        "(`PYTHONPATH=python python3 tools/stage_monographs.py`).",
        "",
        "| stage | EN | RU |",
        "|-------|----|----|",
    ]
    for slug in STAGES:
        stage_code = slug.split("_")[0]
        rest = slug.split("_", 1)[1]
        index.append(
            f"| {stage_code} | [`{rest} (EN)`]({stage_code}_{rest}_EN.md) | "
            f"[`{rest} (RU)`]({stage_code}_{rest}_RU.md) |"
        )
    (OUT / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"stage monographs written: {count} + the index")


if __name__ == "__main__":
    main()
