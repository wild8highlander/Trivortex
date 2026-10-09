#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the PLANETVORTEX V-editions (TheoremF, LemmaF, TheoremG,
LemmaG) as Markdown, then render DOCX (pandoc, house navy-gold
reference styles) and PDF (LibreOffice headless) — the same pipeline
as the P/X editions of docs/monographs/.

    PYTHONPATH=python python3 tools/editions_v.py
"""

from __future__ import annotations

import subprocess
from pathlib import Path

MINI = Path(__file__).resolve().parents[1]
ROOT = MINI / "docs" / "monographs"
ROOT.mkdir(parents=True, exist_ok=True)
REFERENCE = MINIROOT = MINI.parent / "polyvortex" / "docs" / "monograph" / "monograph_RU.docx"

STATEMENTS = {
    "TheoremF": {
        "en_title": "Theorem F — the coset construction of the Klein map",
        "ru_title": "Теорема F — косет-конструкция карты Клейна",
        "en_stmt": (
            "Let $G = \\mathrm{PSL}(2,7)$ (168 classes over $\\mathbb{F}_7$) and "
            "let $(a, b)$ be any pair with $a^2 = b^3 = (ab)^7 = 1$. With "
            "$X = \\langle a\\rangle$, $Y = \\langle b\\rangle$, "
            "$Z = \\langle ab\\rangle$, define the vertices as the right "
            "cosets $gY$, the edges as $gX$, the faces as $gZ$, with the "
            "incidence by nonempty coset intersection. Then there are 56 "
            "vertices, 84 edges, 24 faces and $V - E + F = -4$; every vertex "
            "has degree 3, every face is a 7-cycle; the map is connected and "
            "orientable; the left action of $G$ is faithful — the Klein map "
            "$\\{7,3\\}_8$ with $\\mathrm{Aut}^+ \\cong \\mathrm{PSL}(2,7)$ "
            "and $|\\mathrm{Aut}| = 336$ including reflections."
        ),
        "ru_stmt": (
            "Пусть $G = \\mathrm{PSL}(2,7)$ (168 классов над $\\mathbb{F}_7$) и "
            "пусть $(a, b)$ — произвольная пара с $a^2 = b^3 = (ab)^7 = 1$. При "
            "$X = \\langle a\\rangle$, $Y = \\langle b\\rangle$, "
            "$Z = \\langle ab\\rangle$ определим вершины как правые косеты $gY$, "
            "рёбра как $gX$, грани как $gZ$, инцидентность — по непустому "
            "пересечению косетов. Тогда вершин 56, рёбер 84, граней 24 и "
            "$V - E + F = -4$; каждая вершина имеет степень 3, каждая грань — "
            "7-цикл; карта связна и ориентируема; левое действие $G$ верно — "
            "карта Клейна $\\{7,3\\}_8$ с $\\mathrm{Aut}^+ \\cong "
            "\\mathrm{PSL}(2,7)$ и $|\\mathrm{Aut}| = 336$ с отражениями."
        ),
        "en_proof": (
            "The number of right cosets of $H$ is $|G|/|H|$: $168/3 = 56$, "
            "$168/2 = 84$, $168/7 = 24$. The stabilizer chain of the triangle "
            "group gives exactly 3 edges per vertex, 2 vertices and 2 faces "
            "per edge, and a 7-cycle of edges per face. The (2,3,7) triple "
            "generates $G$, so the flag graph is connected; the full flag set "
            "of 336 pairwise-incident triples has a bipartite adjacency graph "
            "(two flags adjacent iff they differ in one member) — orientability. "
            "Hence $\\chi = V - E + F = -4$, genus $g = 1 - \\chi/2 = 3$. "
            "Faithfulness: the core of $\\langle b\\rangle$ is trivial in the "
            "simple group $G$. The Hurwitz bound $84(g-1) = 168$ caps the "
            "orientation-preserving automorphisms at the certified 168; the "
            "reflections double the count. $\\square$"
        ),
        "ru_proof": (
            "Число правых косетов $H$ равно $|G|/|H|$: $168/3 = 56$, "
            "$168/2 = 84$, $168/7 = 24$. Стабилизаторная цепь треугольной "
            "группы даёт ровно 3 ребра на вершину, 2 вершины и 2 грани на "
            "ребро, 7-цикл рёбер на грань. Тройка (2,3,7) порождает $G$, "
            "поэтому флаговый граф связен; полный набор из 336 попарно "
            "инцидентных троек имеет двудольный граф смежности (два флага "
            "смежны iff различаются одним членом) — ориентируемость. Значит "
            "$\\chi = V - E + F = -4$, род $g = 1 - \\chi/2 = 3$. Верность: "
            "ядро $\\langle b\\rangle$ тривиально в простой группе $G$. "
            "Граница Хурвица $84(g-1) = 168$ ограничивает автоморфизмы, "
            "сохраняющие ориентацию, сертифицированными 168; отражения "
            "удваивают счёт. $\\square$"
        ),
        "en_cert": "Stage V2 (V2_klein_tiling_default.json): the exact combinatorial registers, the connected and bipartite flag graph, and the PGL(2,7) flag certificate on all 336 × 3 flag moves.",
        "ru_cert": "Стадия V2 (V2_klein_tiling_default.json): точные комбинаторные регистры, связный и двудольный флаговый граф и флаговый сертификат PGL(2,7) на всех 336 × 3 стеночных движениях.",
    },
    "LemmaF": {
        "en_title": "Lemma F — the antipodal freeness",
        "ru_title": "Лемма F — свобода антиподов",
        "en_stmt": (
            "The witness involution $a$ (order 2) acts on the 24 faces $gZ$ "
            "without fixed points; hence it pairs them into 12 antipodal "
            "pairs — one pair per gravimetric register of stage V2."
        ),
        "ru_stmt": (
            "Свидетель-инволюция $a$ (порядка 2) действует на 24 грани $gZ$ "
            "без неподвижных точек; значит, она разбивает их на 12 "
            "антиподальных пар — по паре на гравиметрический регистр стадии V2."
        ),
        "en_proof": (
            "Suppose $a$ fixes the face $gZ$: $agZ = gZ$, hence "
            "$g^{-1}ag \\in Z = \\langle ab\\rangle$. The left side has order "
            "2 (conjugation preserves order), the right side is a group of "
            "order 7 — an element of order 2 cannot lie in a group of order "
            "7. Contradiction. A fixed-point-free involution on a 24-element "
            "set is a product of 12 transpositions. $\\square$"
        ),
        "ru_proof": (
            "Пусть $a$ фиксирует грань $gZ$: $agZ = gZ$, значит "
            "$g^{-1}ag \\in Z = \\langle ab\\rangle$. Слева элемент порядка 2 "
            "(сопряжение сохраняет порядок), справа — группа порядка 7: "
            "элемент порядка 2 не лежит в группе порядка 7. Противоречие. "
            "Инволюция без неподвижных точек на 24-элементном множестве — "
            "произведение 12 транспозиций. $\\square$"
        ),
        "en_cert": "Stage V2: the 12 antipodal pairs; face_fixed_points = 0 in the C99 kernel report as well.",
        "ru_cert": "Стадия V2: 12 антиподальных пар; face_fixed_points = 0 и в отчёте C99-ядра.",
    },
    "TheoremG": {
        "en_title": "Theorem G — the budget closure (the capstone)",
        "ru_title": "Теорема G — замыкание бюджета (венец)",
        "en_stmt": (
            "Let $\\mathrm{GM}_1, \\ldots, \\mathrm{GM}_{12}$ be the "
            "gravitational parameters of the registered 12-body set and "
            "$s_i = \\ln \\mathrm{GM}_i - \\frac{1}{12}\\sum_j \\ln "
            "\\mathrm{GM}_j$ the geometric-mean normalization. Then: "
            "$\\sum_i s_i = 0$ exactly; the vertex-angle register "
            "$\\alpha_i = \\frac{2\\pi}{3} - \\sigma s_i$ (any $\\sigma > 0$) "
            "satisfies $\\sum_i \\alpha_i = 8\\pi$ exactly; the decorated "
            "tessellation of the 12 antipodal heptagon pairs therefore closes "
            "on the Gauss–Bonnet budget of the Klein quartic, "
            "$\\sum_i 2A_i = \\sum_i 2(5\\pi - 7\\alpha_i) = 8\\pi = 2\\pi(2g-2)$; "
            "and the heavier the body, the wider its heptagon. The Euler "
            "characteristic absorbs the mass ladder."
        ),
        "ru_stmt": (
            "Пусть $\\mathrm{GM}_1, \\ldots, \\mathrm{GM}_{12}$ — гравитационные "
            "параметры зафиксированного 12-телного набора и $s_i = \\ln "
            "\\mathrm{GM}_i - \\frac{1}{12}\\sum_j \\ln \\mathrm{GM}_j$ — "
            "нормировка на геометрическое среднее. Тогда: $\\sum_i s_i = 0$ "
            "точно; регистр углов $\\alpha_i = \\frac{2\\pi}{3} - \\sigma s_i$ "
            "(при любом $\\sigma > 0$) удовлетворяет $\\sum_i \\alpha_i = 8\\pi$ "
            "точно; украшенная замощение 12 антиподальных пар потому замыкается "
            "на бюджет Гаусса–Бонне квартики Клейна, $\\sum_i 2A_i = 8\\pi = "
            "2\\pi(2g-2)$; и чем тяжелее тело, тем шире его семиугольник. "
            "Характеристика Эйлера вбирает лестницу масс."
        ),
        "en_proof": (
            "(1) $\\sum_i s_i = \\sum_i \\ln \\mathrm{GM}_i - 12 \\cdot "
            "\\frac{1}{12} \\sum_j \\ln \\mathrm{GM}_j = 0$. (2) $\\sum_i "
            "\\alpha_i = 12 \\cdot \\frac{2\\pi}{3} - \\sigma \\sum_i s_i = "
            "8\\pi$. (3) The area of a hyperbolic $n$-gon with interior angles "
            "$\\alpha_1, \\ldots, \\alpha_n$ is $(n-2)\\pi - \\sum \\alpha_k$ "
            "(Gauss–Bonnet per cell), so for $n = 7$: $\\sum_i 2A_i = "
            "2(60\\pi - 7 \\cdot 8\\pi) = 8\\pi$. (4) A regular hyperbolic "
            "heptagon of vertex angle $\\alpha \\in (0, 5\\pi/7)$ exists and is "
            "unique; its right-triangle trigonometry gives the closed forms "
            "$\\cosh R = \\cot(\\alpha/2)\\cot(\\pi/7)$, $\\cosh(\\ell/2) = "
            "\\cos(\\pi/7)/\\sin(\\alpha/2)$, $\\cosh r = \\cos(\\alpha/2)/"
            "\\sin(\\pi/7)$; the monotonicity chain $\\ln \\mathrm{GM} \\uparrow "
            "\\Rightarrow s \\uparrow \\Rightarrow \\alpha \\downarrow "
            "\\Rightarrow A \\uparrow$ finishes the claim. $\\square$"
        ),
        "ru_proof": (
            "(1) $\\sum_i s_i = \\sum_i \\ln \\mathrm{GM}_i - 12 \\cdot "
            "\\frac{1}{12} \\sum_j \\ln \\mathrm{GM}_j = 0$. (2) $\\sum_i "
            "\\alpha_i = 12 \\cdot \\frac{2\\pi}{3} - \\sigma \\sum_i s_i = "
            "8\\pi$. (3) Площадь гиперболического $n$-угольника с углами "
            "$\\alpha_1, \\ldots, \\alpha_n$ равна $(n-2)\\pi - \\sum "
            "\\alpha_k$ (Гаусс–Бонне для ячейки), поэтому для $n = 7$: "
            "$\\sum_i 2A_i = 2(60\\pi - 56\\pi) = 8\\pi$. (4) Правильный "
            "гиперболический семиугольник с углом $\\alpha \\in (0, 5\\pi/7)$ "
            "существует и единствен; тригонометрия прямоугольного треугольника "
            "даёт замкнутые формы $\\cosh R = \\cot(\\alpha/2)\\cot(\\pi/7)$, "
            "$\\cosh(\\ell/2) = \\cos(\\pi/7)/\\sin(\\alpha/2)$, $\\cosh r = "
            "\\cos(\\alpha/2)/\\sin(\\pi/7)$; цепочка монотонности "
            "$\\ln \\mathrm{GM} \\uparrow \\Rightarrow s \\uparrow "
            "\\Rightarrow \\alpha \\downarrow \\Rightarrow A \\uparrow$ "
            "завершает утверждение. $\\square$"
        ),
        "en_cert": "Stage V2 at 50 dps: the budget closure Σα − 8π = 4.3e−50, the area closure, the Pythagoras on all 12 registers, the Poincaré-disk witnesses; the C99 kernel re-derives the algebra independently (long-double residual 0.0).",
        "ru_cert": "Стадия V2 при 50 dps: замыкание бюджета Σα − 8π = 4,3·10⁻⁵⁰, замыкание площади, Пифагор на всех 12 регистрах, свидетели в диске Пуанкаре; C99-ядро независимо воспроизводит алгебру (остаток long double 0,0).",
    },
    "LemmaG": {
        "en_title": "Lemma G — the arc register of the spatial tilt",
        "ru_title": "Лемма G — дуговой регистр пространственного наклона",
        "en_stmt": (
            "Let $i_i$ be the J2000 inclination of the body $i$ (the committed "
            "JPL register) and $\\bar{R} = 1$ AU the register radius. Then "
            "$\\lambda_i = \\bar{R}\\, i_i\\ \\mathrm{[rad]}$ is an exact, "
            "monotone, dimension-free measure of the spatial tilt, and the "
            "tilt operator $T_i = R_z(\\Omega_i) R_x(i_i) \\in SO(3)$ sends "
            "the ecliptic normal to the orbit normal $n_i = (\\sin i_i \\sin "
            "\\Omega_i,\\ -\\sin i_i \\cos \\Omega_i,\\ \\cos i_i)$ exactly."
        ),
        "ru_stmt": (
            "Пусть $i_i$ — наклонение J2000 тела $i$ (зафиксированный реестр "
            "JPL) и $\\bar{R} = 1$ а.е. — радиус регистра. Тогда $\\lambda_i = "
            "\\bar{R}\\, i_i$ [рад] — точная, монотонная, безразмерная мера "
            "пространственного наклона, а оператор наклона $T_i = R_z(\\Omega_i) "
            "R_x(i_i) \\in SO(3)$ переводит нормаль эклиптики в нормаль орбиты "
            "$n_i = (\\sin i_i \\sin \\Omega_i,\\ -\\sin i_i \\cos \\Omega_i,\\ "
            "\\cos i_i)$ точно."
        ),
        "en_proof": (
            "$T_i$ is a product of rotations, hence lies in $SO(3)$ — "
            "orthogonality and $\\det = 1$ are closed under multiplication. "
            "The image of $(0,0,1)$ under $R_z(\\Omega)R_x(i)$: $R_x(i)(0,0,1) "
            "= (0, -\\sin i, \\cos i)$; $R_z(\\Omega)$ rotates the "
            "$xy$-components: $(\\sin i \\sin \\Omega, -\\sin i \\cos \\Omega, "
            "\\cos i)$. $\\lambda = \\bar{R} i$ is linear in the angle with a "
            "fixed positive constant — monotone by inspection: it is the arc "
            "length cut by the tilt angle on the register circle. $\\square$"
        ),
        "ru_proof": (
            "$T_i$ — произведение вращений, значит лежит в $SO(3)$: "
            "ортогональность и $\\det = 1$ замкнуты относительно умножения. "
            "Образ $(0,0,1)$ при $R_z(\\Omega)R_x(i)$: $R_x(i)(0,0,1) = "
            "(0, -\\sin i, \\cos i)$; $R_z(\\Omega)$ вращает $xy$-компоненты: "
            "$(\\sin i \\sin \\Omega, -\\sin i \\cos \\Omega, \\cos i)$. "
            "$\\lambda = \\bar{R} i$ линейно по углу с фиксированной "
            "положительной константой — монотонность очевидна: это длина дуги, "
            "вырезаемой углом наклона на окружности регистра. $\\square$"
        ),
        "en_cert": "Stage V1: the orthogonality at 2.2e−16, the normal recovery at 0.0, the monotone arc ladder, and the 3D J2000 run (energy 2.1e−13, the vector L at 4.7e−15, Kepler III at 1.0e−4 against the secular mean elements).",
        "ru_cert": "Стадия V1: ортогональность 2,2·10⁻¹⁶, восстановление нормали 0,0, монотонная дуговая лестница и 3D-прогон J2000 (энергия 2,1·10⁻¹³, вектор L 4,7·10⁻¹⁵, Кеплер III 1,0·10⁻⁴ против секулярных средних элементов).",
    },
}


def md_for(key: str, lang: str) -> str:
    item = STATEMENTS[key]
    if lang == "en":
        title, stmt, proof, cert = (
            item["en_title"],
            item["en_stmt"],
            item["en_proof"],
            item["en_cert"],
        )
        label = "Statement", "Proof", "Computational certificate"
    else:
        title, stmt, proof, cert = (
            item["ru_title"],
            item["ru_stmt"],
            item["ru_proof"],
            item["ru_cert"],
        )
        label = "Формулировка", "Доказательство", "Вычислительный сертификат"
    return (
        f'---\ntitle: "{title}"\nsubtitle: "PLANETVORTEX — the point monograph"\n'
        "---\n\n"
        f"## {label[0]}\n\n{stmt}\n\n"
        f"## {label[1]}\n\n{proof}\n\n"
        f"## {label[2]}\n\n{cert}\n"
    )


def main() -> None:
    for key in STATEMENTS:
        for lang in ("en", "ru"):
            md = ROOT / f"PLANETVORTEX-{key}_{lang.upper()}.md"
            md.write_text(md_for(key, lang), encoding="utf-8")
            print("md:", md)
            docx = md.with_suffix(".docx")
            cmd = ["pandoc", str(md), "-o", str(docx), "--toc", "--toc-depth=2"]
            if REFERENCE.exists():
                cmd += ["--reference-doc", str(REFERENCE)]
            subprocess.run(cmd, check=True)
            print("docx:", docx)
    pdfs = [str(p.with_suffix(".docx")) for p in ROOT.glob("PLANETVORTEX-*_*.md")]
    subprocess.run(
        ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", str(ROOT)] + pdfs,
        check=True,
        timeout=900,
    )
    print("pdfs rendered")


if __name__ == "__main__":
    main()
