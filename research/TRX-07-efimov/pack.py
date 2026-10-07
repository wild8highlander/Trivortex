# -*- coding: utf-8 -*-
"""Content pack for TRX-07 (v1.0.0 Monograph Edition). Rendered by scripts/build_study_docs.py."""

PACK = {
    "meta": {
        "study_id": "TRX-07",
        "dir_name": "TRX-07-efimov",
        "title_en": "The Efimov Effect: Universal Quantum Three-Body Physics",
        "title_ru": "Эффект Ефимова: универсальная квантовая физика трёх тел",
        "script": "trx07_efimov.py",
        "results_json": "trx07_results.json",
        "scheme_file": "scheme_trx07.svg",
        "runtime_full": "5.77 s (5.771 s recorded with --figures)",
    },
    "essence_en": (
        "Three identical bosons with resonant (unitary) two-body interactions form an "
        "infinite Rydberg-like series of bound three-body states — Efimov trimers — even though the "
        "pair potential binds no dimer. The spectrum is universal: it is governed by a single "
        "transcendental exponent s0 defined by s0·cosh(πs0/2) = (8/√3)·sinh(πs0/6), s0 = 1.0062378 "
        "(target 1.0062458), and it is organized in a geometric ladder — trimer sizes grow by "
        "exp(π/s0) = 22.694383 and energies drop by exp(2π/s0) = 515.035001 per rung. The study "
        "realizes the ladder numerically on the hyperradial adiabatic potential −(s0² − ¼)/R²: the "
        "four computed trimers reproduce the universal energy ratio within ±0.1% (515.509 / 514.964 "
        "/ 514.963), and a three-body-parameter sweep shows the ratios invariant (spread 1.9·10⁻¹⁰) "
        "while absolute energies follow the exact R0⁻² power law — the quantum twin of the "
        "scale-invariant vortex triangle of TRIVORTEX."
    ),
    "essence_ru": (
        "Три одинаковых бозона с резонансным (унитарным) парным взаимодействием образуют "
        "бесконечную ридберговскую серию связанных трёхчастичных состояний — тримеров Ефимова, — "
        "хотя парный потенциал не связывает даже димер. Спектр универсален: им управляет единственный "
        "трансцендентный показатель s0, определяемый уравнением "
        "s0·cosh(πs0/2) = (8/√3)·sinh(πs0/6), s0 = 1.0062378 (цель 1.0062458), и он организован в "
        "геометрическую лестницу — размеры тримеров растут в exp(π/s0) = 22.694383 раза, энергии "
        "падают в exp(2π/s0) = 515.035001 раза на каждую ступень. Исследование воспроизводит "
        "лестницу численно на гиперрадиальном адиабатическом потенциале −(s0² − ¼)/R²: четыре "
        "вычисленных тримера дают универсальное энергетическое отношение с точностью ±0.1% "
        "(515.509 / 514.964 / 514.963), а развёртка по трёхчастичному параметру показывает "
        "инвариантность отношений (разброс 1.9·10⁻¹⁰) при точном степенном законе R0⁻² для "
        "абсолютных энергий — квантовый близнец масштабно-инвариантного вихревого треугольника "
        "TRIVORTEX."
    ),
    "mission_en": [
        (
            "The Efimov effect is the quantum three-body phenomenon par excellence, and its universal "
            "numbers are as sharp as anything in the three-body problem. This study verifies them in "
            "two independent layers. Layer one: the transcendental quantization equation is solved "
            "with brentq, reproducing the exponent s0 = 1.0062378 (deviation 8·10⁻⁶ from the target "
            "1.0062458, tolerance 1e-5), the length factor exp(π/s0) = 22.694383 (target 22.7, "
            "tolerance 0.05) and the energy factor exp(2π/s0) = 515.035001 (target 515.03, tolerance "
            "0.05). Layer two: the hyperradial adiabatic potential −(s0² − ¼)/R² is discretized on an "
            "exponential grid (R = R0·e^s, 900 points over L = ln(Rmax/R0) = 20.7233) — the "
            "substitution u = e^(s/2)·v turns the problem into a symmetric finite-difference "
            "eigenproblem D·K·D whose eigenvalues are the trimer energies — and the four computed "
            "trimers form a geometric ladder with |E0/E1| = 515.509 and |E1/E2| = 514.964 against the "
            "universal 515.035, deviations within ±0.1%."
        ),
        (
            "Beyond the universal numbers themselves, the study verifies their robustness: the ladder "
            "is box-independent wherever two rungs fit (L ≥ 8), it converges monotonically under grid "
            "refinement (512.96 → 515.57 for |E0/E1| over n = 150 → 2200), and it survives a "
            "three-order-of-magnitude sweep of the three-body parameter R0 — the wall shifts the "
            "absolute scale along the exact power law R0⁻² (fitted slope −2.000000) while leaving the "
            "ratios invariant (spread 1.9·10⁻¹⁰). The result is a controlled, verifiable model of "
            "universal quantum three-body physics that completes the quantum-atomic block of the "
            "program alongside the classical CTMC helium of TRX-06 and the ion-trap crystal of "
            "TRX-08."
        ),
    ],
    "mission_ru": [
        (
            "Эффект Ефимова — квантовое трёхчастичное явление в чистом виде, а его универсальные "
            "числа настолько же точны, как всё в задаче трёх тел. Данное исследование проверяет их в "
            "двух независимых слоях. Слой первый: трансцендентное уравнение квантования решается "
            "методом Брента (brentq), воспроизводя показатель s0 = 1.0062378 (отклонение 8·10⁻⁶ от "
            "цели 1.0062458, допуск 1e-5), множитель длины exp(π/s0) = 22.694383 (цель 22.7, допуск "
            "0.05) и множитель энергии exp(2π/s0) = 515.035001 (цель 515.03, допуск 0.05). Слой "
            "второй: гиперрадиальный адиабатический потенциал −(s0² − ¼)/R² дискретизируется на "
            "экспоненциальной сетке (R = R0·e^s, 900 точек на длине L = ln(Rmax/R0) = 20.7233) — "
            "подстановка u = e^(s/2)·v превращает задачу в симметричную конечно-разностную проблему "
            "D·K·D, чьи собственные значения суть энергии тримеров, — и четыре вычисленных тримера "
            "образуют геометрическую лестницу с |E0/E1| = 515.509 и |E1/E2| = 514.964 против "
            "универсального 515.035, отклонения в пределах ±0.1%."
        ),
        (
            "Помимо самих универсальных чисел, исследование проверяет их устойчивость: лестница не "
            "зависит от длины бокса там, где помещаются две ступени (L ≥ 8), монотонно сходится по "
            "сгущению сетки (512.96 → 515.57 для |E0/E1| по n = 150 → 2200) и переживает "
            "трёхпорядковую развёртку трёхчастичного параметра R0 — стенка сдвигает абсолютную шкалу "
            "вдоль точного степенного закона R0⁻² (наклон −2.000000), оставляя отношения "
            "инвариантными (разброс 1.9·10⁻¹⁰). Результат — контролируемая, проверяемая модель "
            "универсальной квантовой физики трёх тел, замыкающая квантово-атомный блок программы "
            "вместе с классическим CTMC-гелием TRX-06 и ионным кристаллом TRX-08."
        ),
    ],
    "physics_en": [
        (
            "The system is three identical bosons in the unitary limit: the s-wave scattering length "
            "a is tuned to infinity (a → ∞), so the two-body subsystem binds no dimer yet scatters "
            "with the maximal cross-section. The natural collective coordinate is the hyperradius R — "
            "the size of the triangle formed by the three particles — and in the zero-range limit the "
            "adiabatic (Born–Oppenheimer-like) separation of the fast hyperangular motion leaves a "
            "single effective channel: a hyperradial attraction −(s0² − ¼)/R², whose strength "
            "s0² − ¼ ≈ 0.7625 is fixed entirely by the transcendental condition (E1) on the exponent "
            "s0 = 1.0062378."
        ),
        (
            "The −1/R² attraction is marginal: it carries no intrinsic length scale, so any bound "
            "state must build its own scale out of the boundaries. Quantum mechanics supplies it "
            "multiplicatively — the outcome is the geometric Efimov ladder, with sizes "
            "R_n ∝ exp(πn/s0) and energies E_n ∝ exp(−2πn/s0). The one microscopic length that does "
            "enter is the three-body parameter R0, here modeled as a hard wall at R = R0 that anchors "
            "the comb of levels; shifting R0 slides every rung but leaves all ratios invariant — "
            "verified by the sweep of fig04 over three decades of R0."
        ),
    ],
    "physics_ru": [
        (
            "Система — три одинаковых бозона в унитарном пределе: s-волновая длина рассеяния a "
            "доведена до бесконечности (a → ∞), поэтому двухчастичная подсистема не связывает димер, "
            "но рассеивает с максимальным сечением. Естественная коллективная координата — "
            "гиперрадиус R, размер треугольника, образуемого тремя частицами; в нуль-радиальном "
            "пределе адиабатическое (борн-оппенгеймеровское) разделение быстрого гиперуглового "
            "движения оставляет один эффективный канал: гиперрадиальное притяжение −(s0² − ¼)/R², "
            "сила которого s0² − ¼ ≈ 0.7625 полностью задаётся трансцендентным условием (E1) на "
            "показатель s0 = 1.0062378."
        ),
        (
            "Притяжение −1/R² маргинально: оно не несёт собственного масштаба длины, поэтому любое "
            "связанное состояние строит масштаб из граничных условий. Квантовая механика поставляет "
            "его мультипликативно — так возникает геометрическая лестница Ефимова с размерами "
            "R_n ∝ exp(πn/s0) и энергиями E_n ∝ exp(−2πn/s0). Единственная микроскопическая длина, "
            "которая входит в задачу, — трёхчастичный параметр R0; здесь он моделируется жёсткой "
            "стенкой при R = R0, закрепляющей гребёнку уровней: сдвиг R0 передвигает каждую ступень, "
            "но оставляет все отношения инвариантными — это проверено развёрткой по трём порядкам R0 "
            "на рис. 04."
        ),
    ],
    "preset_table": {
        "header_en": ["Parameter", "Value", "Meaning"],
        "header_ru": ["Параметр", "Значение", "Смысл"],
        "rows_en": [
            [
                "Universal exponent s0",
                "1.0062378 (target 1.0062458, tol 1e-5)",
                "transcendental root of (E1)",
            ],
            ["Universal length factor", "exp(π/s0) = 22.694383", "trimer size growth per rung"],
            ["Universal energy factor", "exp(2π/s0) = 515.035001", "trimer energy drop per rung"],
            ["Three-body parameter R0", "1e-3", "hard wall in R (short-distance phase)"],
            [
                "Outer wall Rmax",
                "1e6",
                "box hosts L = ln(Rmax/R0) = 20.723266 ≈ 3.3 Efimov oscillations",
            ],
            ["FD grid", "900 points, Δs = 0.023051", "uniform in s = ln(R/R0)"],
            [
                "Levels computed",
                "4 deepest trimers",
                "energies −4476.18 … −3.27·10⁻⁵ (units of 1/R0²)",
            ],
        ],
        "rows_ru": [
            [
                "Универсальный показатель s0",
                "1.0062378 (цель 1.0062458, допуск 1e-5)",
                "трансцендентный корень (E1)",
            ],
            [
                "Универсальный множитель длины",
                "exp(π/s0) = 22.694383",
                "рост размера тримера за ступень",
            ],
            [
                "Универсальный множитель энергии",
                "exp(2π/s0) = 515.035001",
                "падение энергии тримера за ступень",
            ],
            ["Трёхчастичный параметр R0", "1e-3", "жёсткая стенка в R (фаза коротких расстояний)"],
            [
                "Внешняя стенка Rmax",
                "1e6",
                "бокс вмещает L = ln(Rmax/R0) = 20.723266 ≈ 3.3 осцилляции Ефимова",
            ],
            ["Конечно-разностная сетка", "900 точек, Δs = 0.023051", "равномерная по s = ln(R/R0)"],
            [
                "Вычисляемые уровни",
                "4 глубочайших тримера",
                "энергии −4476.18 … −3.27·10⁻⁵ (единицы 1/R0²)",
            ],
        ],
    },
    "equations": [
        {
            "id": "E1",
            "latex": "s_0\\,\\cosh\\!\\left(\\tfrac{\\pi s_0}{2}\\right) = \\tfrac{8}{\\sqrt{3}}\\,\\sinh\\!\\left(\\tfrac{\\pi s_0}{6}\\right), \\qquad s_0 = 1.0062458",
            "desc_en": "Universal quantization condition: the transcendental root solved by brentq on [0.5, 3.0]",
            "desc_ru": "Универсальное условие квантования: трансцендентный корень, найденный brentq на [0.5, 3.0]",
        },
        {
            "id": "E2",
            "latex": "\\frac{a_*^{(n+1)}}{a_*^{(n)}} = e^{\\pi/s_0} = 22.694383, \\qquad \\frac{E_n}{E_{n+1}} = e^{2\\pi/s_0} = 515.035001",
            "desc_en": "Geometric ladders of scattering lengths (where trimers cross) and trimer energies",
            "desc_ru": "Геометрические лестницы длин рассеяния (точек появления тримеров) и энергий тримеров",
        },
        {
            "id": "E3",
            "latex": "-\\frac{d^2 u}{dR^2} - \\frac{s_0^2 - 1/4}{R^2}\\,u = E\\,u, \\qquad u(R_0) = u(R_{max}) = 0",
            "desc_en": "Hyperradial adiabatic equation (zero-range, unitary limit) with Dirichlet walls",
            "desc_ru": "Гиперрадиальное адиабатическое уравнение (нуль-радиальный предел, унитарность) со стенками Дирихле",
        },
        {
            "id": "E4",
            "latex": "R = R_0\\,e^{s}, \\quad u = e^{s/2}\\,v \\;\\Rightarrow\\; \\left(-\\frac{d^2}{ds^2} - s_0^2\\right) v = E\\,R_0^2 e^{2s} v, \\quad s \\in [0,\\, L]",
            "desc_en": "Exponential grid transform; L = ln(Rmax/R0) = 20.723266",
            "desc_ru": "Переход к экспоненциальной сетке; L = ln(Rmax/R0) = 20.723266",
        },
        {
            "id": "E5",
            "latex": "D\\,K\\,D\\,u = E\\,u, \\quad D = \\mathrm{diag}\\!\\left(R_0^{-1} e^{-s_j}\\right), \\quad K_{jj} = \\tfrac{2}{\\Delta s^2} - s_0^2, \\;\\; K_{j\\,j\\pm 1} = -\\tfrac{1}{\\Delta s^2}",
            "desc_en": "Symmetric FD eigenproblem actually diagonalized (numpy eigvalsh); its eigenvalues are the trimer energies",
            "desc_ru": "Симметричная конечно-разностная задача, фактически диагонализуемая (numpy eigvalsh); её собственные значения — энергии тримеров",
        },
    ],
    "scheme_cap_en": (
        "TRX-07 scheme — the Efimov geometric ladder: three identical bosons at "
        "unitarity (no dimer) bind through the hyperradial −1/R² attraction into trimers whose "
        "rungs are equally spaced in s = ln(R/R0) by Δs = π/s0 = 3.1221, sizes growing 22.694× and "
        "energies falling 515.035× per rung."
    ),
    "scheme_cap_ru": (
        "Схема TRX-07 — геометрическая лестница Ефимова: три одинаковых бозона в "
        "предел унитарности (без димера) связываются гиперрадиальным притяжением −1/R² в тримеры, "
        "ступени которых равноотстоящи в s = ln(R/R0) с шагом Δs = π/s0 = 3.1221; размеры растут в "
        "22.694 раза, энергии падают в 515.035 раза за ступень."
    ),
    "scheme_walk_en": [
        [
            "Three bosons (gold discs 1, 2, 3)",
            "identical bosons at unitarity a → ∞ joined by resonant pairwise bonds (dashed); each pair alone is unbound",
        ],
        [
            "Hyperradius R",
            "arrow from the centroid to a boson — the collective coordinate in which the trio binds via −(s0² − ¼)/R²",
        ],
        [
            "Ladder in s = ln(R/R0) space",
            "four rungs E0…E3 as colored bars, labeled by trimer sizes ≈ 13, 296, 6725, 152604 R0",
        ],
        [
            "Gold tick R0 (wall)",
            "the three-body parameter: a hard wall at s = 0 anchoring the whole comb of levels",
        ],
        [
            "Δs = π/s0 = 3.122 arrow",
            "equal spacing of rungs in log space — the log-periodicity that generates the 515× energy ladder",
        ],
        [
            "Mapping strip",
            "s0 → circulation ratios Γ of the vortex triangle; e^(2π/s0) = 515 → radial modulation ω = (2π/T)·e^(C_Ch/π); −1/R² attraction → scale-invariant binding of Theorem 3.1",
        ],
    ],
    "scheme_walk_ru": [
        [
            "Три бозона (золотые диски 1, 2, 3)",
            "одинаковые бозоны в пределе унитарности a → ∞, соединённые резонансными парными связями (пунктир); каждая пара сама по себе не связана",
        ],
        [
            "Гиперрадиус R",
            "стрелка от центра масс к бозону — коллективная координата, в которой трио связывается потенциалом −(s0² − ¼)/R²",
        ],
        [
            "Лестница в пространстве s = ln(R/R0)",
            "четыре ступени E0…E3 цветными полосами с подписями размеров тримеров ≈ 13, 296, 6725, 152604 R0",
        ],
        [
            "Золотая насечка R0 (стенка)",
            "трёхчастичный параметр: жёсткая стенка при s = 0, закрепляющая всю гребёнку уровней",
        ],
        [
            "Стрелка Δs = π/s0 = 3.122",
            "равные промежутки между ступенями в логарифмическом пространстве — лог-периодичность, порождающая энергетическую лестницу 515×",
        ],
        [
            "Полоса соответствий",
            "s0 → отношения циркуляций Γ вихревого треугольника; e^(2π/s0) = 515 → радиальная модуляция ω = (2π/T)·e^(C_Ch/π); притяжение −1/R² → масштабно-инвариантное связывание теоремы 3.1",
        ],
    ],
    "mapping": {
        "header_en": ["Quantity in this study", "TRIVORTEX analog", "Comment"],
        "header_ru": ["Величина исследования", "Аналог в TRIVORTEX", "Комментарий"],
        "rows_en": [
            [
                "Three identical bosons at unitarity",
                "three bodies with resonant effective forces",
                "the quantum three-body problem",
            ],
            [
                "Hyperradial −1/R² attraction",
                "scale-invariant binding of Theorem 3.1",
                "both bind without any intrinsic length",
            ],
            [
                "Geometric 515× energy ladder",
                "radial modulation ω = (2π/T)·e^(C_Ch/π)",
                "exponential structure from scale invariance",
            ],
            [
                "Universal exponent s0",
                "circulation ratios Γ of the vortex model",
                "dimensionless universal constants",
            ],
            [
                "Three-body parameter R0",
                "the free length scale of the vortex model",
                "shifts absolute values, ratios stay invariant",
            ],
        ],
        "rows_ru": [
            [
                "Три одинаковых бозона в пределе унитарности",
                "три тела с резонансными эффективными силами",
                "квантовая задача трёх тел",
            ],
            [
                "Гиперрадиальное притяжение −1/R²",
                "масштабно-инвариантное связывание теоремы 3.1",
                "оба связывают без собственной длины",
            ],
            [
                "Геометрическая энергетическая лестница 515×",
                "радиальная модуляция ω = (2π/T)·e^(C_Ch/π)",
                "экспоненциальная структура из масштабной инвариантности",
            ],
            [
                "Универсальный показатель s0",
                "отношения циркуляций Γ вихревой модели",
                "безразмерные универсальные константы",
            ],
            [
                "Трёхчастичный параметр R0",
                "свободный масштаб длины вихревой модели",
                "сдвигает абсолютные значения, отношения инвариантны",
            ],
        ],
    },
    "nondim_en": (
        "Hyperradius in arbitrary units — only ratios are observable; energies in the same "
        "units with ħ²/m = 1, so eigenvalues are quoted in units of 1/R0². The box is set by the "
        "pair (R0, Rmax) = (1e-3, 1e6): L = ln(Rmax/R0) = 20.723266 e-foldings of the hyperradius "
        "host Δs = π/s0 = 3.1221 per half-oscillation, i.e. about 3.3 full Efimov oscillations. "
        "The three-body parameter enters as the hard-wall position R0, which shifts absolute "
        "levels along the exact R0⁻² law but not the ratios."
    ),
    "nondim_ru": (
        "Гиперрадиус в произвольных единицах — наблюдаемы только отношения; энергии в тех "
        "же единицах с ħ²/m = 1, поэтому собственные значения приводятся в единицах 1/R0². Бокс "
        "задаётся парой (R0, Rmax) = (1e-3, 1e6): длина L = ln(Rmax/R0) = 20.723266 "
        "экспоненциальных единиц гиперрадиуса вмещает Δs = π/s0 = 3.1221 на пол-осцилляции, то есть около 3.3 полных "
        "осцилляций Ефимова. Трёхчастичный параметр входит как положение жёсткой стенки R0, "
        "сдвигающее абсолютные уровни вдоль точного закона R0⁻², но не отношения."
    ),
    "checks": {
        "header_en": ["Check", "Target", "Tolerance"],
        "header_ru": ["Проверка", "Цель", "Допуск"],
        "rows_en": [
            ["Transcendental root s0 of the quantization condition (E1)", "1.0062458", "1e-5"],
            ["Length ladder factor exp(π/s0)", "22.7", "5e-2"],
            ["Energy ladder factor exp(2π/s0)", "515.03", "5e-2"],
            ["Hyperradial spectrum: deepest levels all negative", "yes (4 levels)", "exact"],
            ["Ladder ratio E0/E1 vs universal exp(2π/s0)", "515.035001", "35%"],
            ["Ladder ratio E1/E2 vs universal exp(2π/s0)", "515.035001", "35%"],
        ],
        "rows_ru": [
            ["Трансцендентный корень s0 условия квантования (E1)", "1.0062458", "1e-5"],
            ["Множитель длины exp(π/s0)", "22.7", "5e-2"],
            ["Множитель энергии exp(2π/s0)", "515.03", "5e-2"],
            ["Гиперрадиальный спектр: глубочайшие уровни отрицательны", "да (4 уровня)", "точно"],
            ["Лестничное отношение E0/E1 против универсального exp(2π/s0)", "515.035001", "35%"],
            ["Лестничное отношение E1/E2 против универсального exp(2π/s0)", "515.035001", "35%"],
        ],
    },
    "figure_caps": {
        "fig01_efimov_landscape.png": {
            "cap_en": "Model landscape: (a) the hyperradial adiabatic potential |V(R)| = (s0² − ¼)/R² on log–log axes with the hard wall R0 (the three-body parameter) and the scaling hyperradii of the four computed trimers; (b) the same ladder in s = ln(R/R0) space.",
            "cap_ru": "Ландшафт модели: (a) гиперрадиальный адиабатический потенциал |V(R)| = (s0² − ¼)/R² в лог-лог осях с жёсткой стенкой R0 (трёхчастичный параметр) и масштабными гиперрадиусами четырёх вычисленных тримеров; (b) та же лестница в пространстве s = ln(R/R0).",
            "walk_en": "The four trimers sit at scaling hyperradii 13.0518, 296.339, 6724.76 and 152604 R0 — successive rungs spaced by the universal exp(π/s0) = 22.694 (a total size span of 1.2·10⁴); in panel (b) the rungs are equally spaced by Δs = π/s0 = 3.1221, the log-periodicity that generates the 515× energy ladder.",
            "walk_ru": "Четыре тримера сидят на масштабных гиперрадиусах 13.0518, 296.339, 6724.76 и 152604 R0 — соседние ступени разнесены на универсальный множитель exp(π/s0) = 22.694 (полный размах размеров 1.2·10⁴); на панели (b) ступени равноотстоящи с шагом Δs = π/s0 = 3.1221 — это лог-периодичность, порождающая энергетическую лестницу 515×.",
        },
        "fig02_universal_numbers.png": {
            "cap_en": "Headline result: (a) the transcendental quantization function f(s) = s·cosh(πs/2) − (8/√3)·sinh(πs/6) with its root s0; (b) the measured ladder ratios against the universal exp(2π/s0) = 515.035 (dashed line; acceptance band 35%).",
            "cap_ru": "Главный результат: (a) трансцендентная функция квантования f(s) = s·cosh(πs/2) − (8/√3)·sinh(πs/6) с её корнем s0; (b) измеренные лестничные отношения против универсального exp(2π/s0) = 515.035 (пунктир; полоса допуска 35%).",
            "walk_en": "brentq returns s0 = 1.0062378 against the target 1.0062458 (tolerance 1e-5); the measured ratios |E0/E1| = 515.509 (+0.09%), |E1/E2| = 514.964 (−0.01%) and |E2/E3| = 514.963 (−0.01%) hug the dashed universal line — three orders of magnitude inside the ±35% acceptance band.",
            "walk_ru": "brentq возвращает s0 = 1.0062378 против цели 1.0062458 (допуск 1e-5); измеренные отношения |E0/E1| = 515.509 (+0.09%), |E1/E2| = 514.964 (−0.01%) и |E2/E3| = 514.963 (−0.01%) прижались к пунктирной универсальной линии — на три порядка внутри полосы допуска ±35%.",
        },
        "fig03_ladder_stability.png": {
            "cap_en": "Stability of the computed ladder: (a) box-length sweep at fixed grid spacing; (b) grid refinement at the preset box.",
            "cap_ru": "Устойчивость вычисленной лестницы: (a) развёртка по длине бокса при фиксированном шаге сетки; (b) сгущение сетки в пресетном боксе.",
            "walk_en": "Wherever two rungs fit (L ≥ 8) the ratio |E0/E1| is box-independent at 515.5089–515.5091, while the number of bound trimers grows 1 → 2 → 3 → 4 with the box capacity; under grid refinement the ratios converge monotonically from 512.96/512.41 at n = 150 to 515.57/515.02 at n = 2200, and the preset n = 900 sits within 0.1% of the universal 515.035.",
            "walk_ru": "Всюду, где помещаются две ступени (L ≥ 8), отношение |E0/E1| не зависит от бокса: 515.5089–515.5091, а число связанных тримеров растёт 1 → 2 → 3 → 4 вместе с ёмкостью бокса; при сгущении сетки отношения монотонно сходятся от 512.96/512.41 при n = 150 к 515.57/515.02 при n = 2200, а пресетные n = 900 сидят в пределах 0.1% от универсального 515.035.",
        },
        "fig04_scaling_laws.png": {
            "cap_en": "Scaling laws: (a) the geometric energy ladder |En|·R0² against the universal law exp(−2πn/s0); (b) the three-body parameter sweep R0 over three decades at fixed box shape.",
            "cap_ru": "Законы масштабирования: (a) геометрическая энергетическая лестница |En|·R0² против универсального закона exp(−2πn/s0); (b) развёртка трёхчастичного параметра R0 по трём порядкам при фиксированной форме бокса.",
            "walk_en": "Individual rung ratios stay within 0.1% of 515.035; across R0 ∈ [1e-5, 1e-2] the deepest energy follows the exact power law |E0| ∝ R0⁻² (fitted slope −2.000000) while the ladder ratio is invariant with spread 1.9·10⁻¹⁰ — the wall shifts the absolute scale and nothing else.",
            "walk_ru": "Отношения отдельных ступеней удерживаются в пределах 0.1% от 515.035; по всему диапазону R0 ∈ [1e-5, 1e-2] глубочайшая энергия следует точному степенному закону |E0| ∝ R0⁻² (наклон −2.000000), а лестничное отношение инвариантно с разбросом 1.9·10⁻¹⁰ — стенка сдвигает абсолютную шкалу и больше ничего.",
        },
    },
    "results_block": [
        "s0_transcendental_root     = 1.006238    (target 1.0062458, tol 1e-05)",
        "efimov_length_ratio        = 22.694383   (target 22.7, tol 0.05)",
        "efimov_energy_ratio        = 515.035001  (target 515.03, tol 0.05)",
        "spectrum_all_negative      = PASS (4 negative levels)",
        "ladder_ratio_E0_over_E1    = 515.508939  (deviation +0.09%)",
        "ladder_ratio_E1_over_E2    = 514.963968  (deviation -0.01%)",
        "figures: scheme_trx07.svg + 4 PNG panels written to figures/",
        "status: PASS (6/6)   runtime: 5.771 s",
    ],
    "abstract_en": (
        "This monograph treats the Efimov effect: three identical bosons with resonant "
        "two-body interactions form an infinite Rydberg-like series of bound three-body states even "
        "though the pair potential binds no dimer. The spectrum is universal, governed by a single "
        "transcendental exponent s0 defined by s0·cosh(πs0/2) = (8/√3)·sinh(πs0/6). The study "
        "verifies the universal numbers in two independent layers. Layer one: the transcendental "
        "equation is solved with brentq, giving s0 = 1.0062378 (target 1.0062458, tolerance 1e-5), "
        "the length factor exp(π/s0) = 22.694383 and the energy factor exp(2π/s0) = 515.035001. "
        "Layer two: the hyperradial adiabatic potential −(s0² − ¼)/R² is discretized on an "
        "exponential grid (900 points over L = 20.7233), and the four computed trimers — energies "
        "−4476.18 down to −3.27·10⁻⁵, sizes 13.05 to 152604 R0 — form a geometric ladder with "
        "|E0/E1| = 515.509 (+0.09%), |E1/E2| = 514.964 (−0.01%) and |E2/E3| = 514.963 (−0.01%) "
        "against the universal 515.035. The ladder is box-independent wherever two rungs fit and "
        "monotone under grid refinement; a three-body-parameter sweep over three decades leaves the "
        "ratios invariant (spread 1.9·10⁻¹⁰) while absolute energies follow the exact R0⁻² power "
        "law (slope −2.000000). The Efimov ladder is thus established numerically as the quantum "
        "twin of the scale-invariant vortex triangle of TRIVORTEX."
    ),
    "abstract_ru": (
        "Монография посвящена эффекту Ефимова: три одинаковых бозона с резонансным "
        "парным взаимодействием образуют бесконечную ридберговскую серию связанных "
        "трёхчастичных состояний, хотя парный потенциал не связывает даже димер. Спектр "
        "универсален и управляется единственным трансцендентным показателем s0, определяемым "
        "уравнением s0·cosh(πs0/2) = (8/√3)·sinh(πs0/6). Исследование проверяет универсальные "
        "числа в двух независимых слоях. Слой первый: трансцендентное уравнение решается методом "
        "Брента, давая s0 = 1.0062378 (цель 1.0062458, допуск 1e-5), множитель длины "
        "exp(π/s0) = 22.694383 и множитель энергии exp(2π/s0) = 515.035001. Слой второй: "
        "гиперрадиальный адиабатический потенциал −(s0² − ¼)/R² дискретизируется на "
        "экспоненциальной сетке (900 точек на длине L = 20.7233), и четыре вычисленных тримера — "
        "энергии от −4476.18 до −3.27·10⁻⁵, размеры от 13.05 до 152604 R0 — образуют "
        "геометрическую лестницу с |E0/E1| = 515.509 (+0.09%), |E1/E2| = 514.964 (−0.01%) и "
        "|E2/E3| = 514.963 (−0.01%) против универсального 515.035. Лестница не зависит от бокса "
        "всюду, где помещаются две ступени, и монотонно сходится по сетке; развёртка "
        "трёхчастичного параметра по трём порядкам оставляет отношения инвариантными (разброс "
        "1.9·10⁻¹⁰), а абсолютные энергии следуют точному закону R0⁻² (наклон −2.000000). Лестница "
        "Ефимова установлена численно как квантовый близнец масштабно-инвариантного вихревого "
        "треугольника TRIVORTEX."
    ),
    "intro_en": [
        (
            "The prediction belongs to Vitaly Efimov (1970), then working at the Budker Institute of "
            "Nuclear Physics in Novosibirsk: three identical bosons with a resonant two-body "
            "interaction must possess an infinite number of bound three-body states, even when the "
            "pair potential is too weak to bind a dimer. The claim was so counterintuitive that it "
            "met years of skepticism — until Amado and Greenwood (1977) proved the companion "
            "statement that there is no Efimov effect for four or more particles, sharpening the "
            "result from an anomaly into a genuine three-body law: the effect exists exactly at N = 3 "
            "and nowhere else."
        ),
        (
            "The theory was put on firm ground through the Faddeev equations (1961), which split the "
            "three-body wave function into pair amplitudes, and through the zero-range (unitary) "
            "idealization, where the whole answer collapses to a single transcendental exponent s0. "
            "Macek (1968) had just introduced the adiabatic hyperradius for the helium atom, and the "
            "same collective coordinate governs the Efimov problem: the effective hyperradial "
            "attraction −(s0² − ¼)/R² has no length scale of its own, so the spectrum must be "
            "geometric, with the log-periodicity Δs = π/s0 in the hyperradius. Braaten and Hammer "
            "(2006) consolidated this universality into the standard reference for few-body physics."
        ),
        (
            "The experimental era opened with laser-cooled atoms. Kraemer et al. (2006) observed the "
            "Efimov resonances in an ultracold gas of caesium atoms, tuning the scattering length "
            "through a Feshbach resonance and reading out the trimers by laser spectroscopy — the "
            "laser connection of this study. Zaccanti et al. (2009) then resolved the full log-periodic "
            "spectrum in potassium, and Kunitski et al. (2015) found Efimov states in atomic helium "
            "trimers, the smallest three-body system of all. The geometric factor exp(2π/s0) ≈ 515 "
            "between successive trimer energies is now measured laboratory fact."
        ),
        (
            "For TRIVORTEX the relevance is structural. The hyperradial −1/R² attraction binds without "
            "any intrinsic length — precisely the scale-free binding of the vortex triangle in "
            "Theorem 3.1 — and the resulting geometric ladder, with its universal exponent s0, is the "
            "quantum twin of the radial modulation ω = (2π/T)·e^(C_Ch/π) of the vortex model. This "
            "study anchors the quantum chapter of the program: it shows that the same exponential "
            "hierarchy the vortex framework produces classically re-emerges, number for number, in "
            "the few-body spectrum of quantum mechanics."
        ),
    ],
    "intro_ru": [
        (
            "Предсказание принадлежит Виталию Ефимову (1970), работавшему тогда в Институте ядерной "
            "физики им. Будкера в Новосибирске: три одинаковых бозона с резонансным парным "
            "взаимодействием должны обладать бесконечным числом связанных трёхчастичных состояний, "
            "даже если парный потенциал слишком слаб, чтобы связать димер. Утверждение было настолько "
            "контринтуитивным, что многие годы встречало скепсис — пока Амадо и Гринвуд (1977) не "
            "доказали парное утверждение об отсутствии эффекта Ефимова для четырёх и более частиц, "
            "превратив аномалию в настоящий трёхчастичный закон: эффект существует ровно при N = 3 и "
            "нигде больше."
        ),
        (
            "Теория встала на твёрдую почву благодаря уравнениям Фаддеева (1961), разбивающим "
            "волновую функцию трёх тел на парные амплитуды, и нуль-радиальной (унитарной) "
            "идеализации, в которой весь ответ сворачивается к единственному трансцендентному "
            "показателю s0. Мачек (1968) как раз ввёл адиабатический гиперрадиус для атома гелия, и "
            "та же коллективная координата управляет задачей Ефимова: эффективное гиперрадиальное "
            "притяжение −(s0² − ¼)/R² не имеет собственного масштаба длины, поэтому спектр обязан "
            "быть геометрическим, с лог-периодичностью Δs = π/s0 по гиперрадиусу. Братен и Хаммер "
            "(2006) закрепили эту универсальность в стандартном справочнике физики малых частиц."
        ),
        (
            "Экспериментальная эра открылась лазерно-охлаждёнными атомами. Крамер и др. (2006) "
            "наблюдали резонансы Ефимова в ультрахолодном газе атомов цезия, проводя длину рассеяния "
            "через фешбаховский резонанс и считывая тримеры лазерной спектроскопией, — лазерная "
            "связь данного исследования. Закканти и др. (2009) затем разрешили полную лог-периодическую "
            "спектральную серию в калии, а Кунитски и др. (2015) нашли состояния Ефимова в атомных "
            "тримерах гелия — самой маленькой трёхчастичной системе вообще. Геометрический множитель "
            "exp(2π/s0) ≈ 515 между энергиями соседних тримеров — ныне измеренный лабораторный факт."
        ),
        (
            "Для TRIVORTEX значимость структурна. Гиперрадиальное притяжение −1/R² связывает без "
            "какой-либо собственной длины — в точности масштабно-свободное связывание вихревого "
            "треугольника в теореме 3.1, — а возникающая геометрическая лестница с её универсальным "
            "показателем s0 есть квантовый близнец радиальной модуляции ω = (2π/T)·e^(C_Ch/π) "
            "вихревой модели. Данное исследование — якорь квантовой главы программы: оно показывает, "
            "что та же экспоненциальная иерархия, которую вихревой каркас порождает классически, "
            "возникает число в число и в спектре квантовой механики малых тел."
        ),
    ],
    "derivation_en": [
        (
            "At unitarity the zero-range Faddeev equations reduce, in hyperspherical coordinates, to "
            "an eigenvalue problem for the hyperangular part of the wave function. The spectral "
            "parameter of that hyperangular problem, s0, enters the consistency condition (E1): "
            "f(s) = s·cosh(πs/2) − (8/√3)·sinh(πs/6) = 0. Its positive root s0 = 1.0062458 (the "
            "literature value; the brentq root of this study is 1.0062378) fixes the strength of the "
            "effective hyperradial channel, s0² − ¼ ≈ 0.7625, and nothing else — the entire Efimov "
            "phenomenology flows from this single number."
        ),
        (
            "With the angular part frozen in the attractive channel, the hyperradial equation (E3) is "
            "scale-invariant: under R → λR the kinetic and potential terms rescale identically, so "
            "from any bound solution with energy E a new one exists at E·λ⁻². Self-similarity under "
            "the discrete step λ = exp(π/s0) closes the hierarchy: the wave-function node structure "
            "repeats after each half-turn of the log-periodic oscillation, giving the geometric "
            "ladder E_n ∝ exp(−2πn/s0) and R_n ∝ exp(πn/s0). In s = ln(R/R0) space the problem becomes "
            "translation-invariant with period π/s0 = 3.1221 — the origin of the equal rung spacing "
            "of fig01(b)."
        ),
        (
            "The only scale that breaks this invariance is the three-body parameter: short-range "
            "physics at distances where the zero-range idealization fails. The study models it as a "
            "hard wall at R = R0 (Dirichlet in (E3)); the outer boundary at Rmax completes the box. "
            "On the exponential grid s = ln(R/R0) with u = e^(s/2)·v the equation becomes "
            "(E4), and the symmetrization D·K·D of (E5) — D = diag(R0⁻¹e^(−s)) — produces a real "
            "symmetric matrix whose four lowest eigenvalues are exactly the four deepest trimer "
            "energies; the ladder ratios are the reported observables."
        ),
    ],
    "derivation_ru": [
        (
            "В унитарном пределе нуль-радиальные уравнения Фаддеева в гиперсферических координатах "
            "сводятся к задаче на собственные значения гиперугловой части волновой функции. "
            "Спектральный параметр этой гиперугловой задачи s0 входит в условие согласованности (E1): "
            "f(s) = s·cosh(πs/2) − (8/√3)·sinh(πs/6) = 0. Его положительный корень s0 = 1.0062458 "
            "(литературное значение; корень brentq данного исследования — 1.0062378) фиксирует силу "
            "эффективного гиперрадиального канала s0² − ¼ ≈ 0.7625 — и больше ничего: вся "
            "феноменология Ефимова вытекает из этого единственного числа."
        ),
        (
            "При замороженной угловой части в притягивающем канале гиперрадиальное уравнение (E3) "
            "масштабно-инвариантно: при R → λR кинетический и потенциальный члены перемасштабируются "
            "одинаково, поэтому из любого связанного решения с энергией E возникает новое с "
            "E·λ⁻². Самоподобие при дискретном шаге λ = exp(π/s0) замыкает иерархию: узловая "
            "структура волновой функции повторяется после каждой полуволны лог-периодической "
            "осцилляции, порождая геометрическую лестницу E_n ∝ exp(−2πn/s0) и R_n ∝ exp(πn/s0). В "
            "пространстве s = ln(R/R0) задача становится трансляционно-инвариантной с периодом "
            "π/s0 = 3.1221 — отсюда равный шаг ступеней на рис. 01(b)."
        ),
        (
            "Единственный масштаб, нарушающий эту инвариантность, — трёхчастичный параметр: "
            "короткодействующая физика на расстояниях, где нуль-радиальная идеализация отказывает. "
            "Исследование моделирует его жёсткой стенкой при R = R0 (Дирихле в (E3)); внешняя граница "
            "при Rmax замыкает бокс. На экспоненциальной сетке s = ln(R/R0) с подстановкой "
            "u = e^(s/2)·v уравнение переходит в (E4), а симметризация D·K·D из (E5) — "
            "D = diag(R0⁻¹e^(−s)) — даёт вещественную симметричную матрицу, чьи четыре нижних "
            "собственных значения суть ровно четыре глубочайшие энергии тримеров; отчётные "
            "наблюдаемые — лестничные отношения."
        ),
    ],
    "connection_en": (
        "The mapping to the TRIVORTEX vortex framework is structural, not decorative. "
        "The hyperradial −1/R² attraction binds a three-body system without any intrinsic length, "
        "exactly as the scale-invariant binding of Theorem 3.1 holds the vortex triangle together; "
        "the universal exponent s0 plays the role of the circulation ratios Γ — the dimensionless "
        "constant that survives every rescaling; and the geometric Efimov ladder e^(2π/s0) = 515.035 "
        "is the quantum sibling of the radial modulation ω = (2π/T)·e^(C_Ch/π) of the vortex model "
        "— both are exponential hierarchies born from scale invariance rather than from any "
        "microscopic parameter. Even the role of the non-universal residue matches: the three-body "
        "parameter R0 shifts the absolute scale of the comb (the verified R0⁻² law) while the "
        "ratios stay pinned, just as the free circulation scale of the vortex model sets absolute "
        "frequencies but not the geometry of the choreography."
    ),
    "connection_ru": (
        "Соответствие вихревому каркасу TRIVORTEX структурно, а не декоративно. "
        "Гиперрадиальное притяжение −1/R² связывает трёхчастичную систему без какой-либо "
        "собственной длины — в точности как масштабно-инвариантное связывание теоремы 3.1 "
        "удерживает вихревой треугольник; универсальный показатель s0 играет роль отношений "
        "циркуляций Γ — безразмерной константы, переживающей любое перемасштабирование; а "
        "геометрическая лестница Ефимова e^(2π/s0) = 515.035 — квантовый собрат радиальной "
        "модуляции ω = (2π/T)·e^(C_Ch/π) вихревой модели: обе — экспоненциальные иерархии, "
        "рождённые масштабной инвариантностью, а не каким-либо микроскопическим параметром. Даже "
        "роль неуниверсального остатка совпадает: трёхчастичный параметр R0 сдвигает абсолютную "
        "шкалу гребёнки (проверенный закон R0⁻²), оставляя отношения закреплёнными, — как и "
        "свободный масштаб циркуляции вихревой модели задаёт абсолютные частоты, но не геометрию "
        "хореографии."
    ),
    "method_en": [
        (
            "The universal exponent is computed as the root of f(s) = s·cosh(πs/2) − "
            "(8/√3)·sinh(πs/6) by scipy.optimize.brentq on the bracket [0.5, 3.0] with xtol = 1e-13 "
            "and rtol = 8.9·10⁻¹⁶ — machine-limited. The same root feeds both universal factors, "
            "exp(π/s0) = 22.694383 (lengths) and exp(2π/s0) = 515.035001 (energies), which serve as "
            "the acceptance targets of the numerical layer."
        ),
        (
            "The hyperradial spectrum is solved on the exponential grid s ∈ [0, L], L = ln(Rmax/R0) = "
            "20.7233, with n = 900 uniform points (Δs = 0.023051). The tridiagonal kinetic operator K "
            "of (E5) carries the constant shift −s0²; the symmetrization A = D·K·D with "
            "D = diag(R0⁻¹e^(−s)) yields a real symmetric 900 × 900 matrix, diagonalized by "
            "numpy.linalg.eigvalsh, whose four lowest eigenvalues are the four deepest trimer "
            "energies. Negative eigenvalues are retained; the ladder ratios |En/En+1| are the "
            "reported observables."
        ),
        (
            "Three sweeps interrogate the robustness of the ladder, reusing the same solver: the "
            "box-length sweep (L = 4 … 20.723 at fixed grid spacing) probes the capacity of the box; "
            "the grid sweep (n = 150 … 2200) probes discretization convergence; and the "
            "three-body-parameter sweep (R0 over three decades, seven points, fixed box shape) probes "
            "the role of the short-distance wall. Every check stores its value, target, tolerance, "
            "unit and pass flag in the JSON protocol, and the --figures mode appends the scheme, the "
            "four 300-DPI panels and all sweep data to the same machine-readable record."
        ),
    ],
    "method_ru": [
        (
            "Универсальный показатель вычисляется как корень f(s) = s·cosh(πs/2) − (8/√3)·sinh(πs/6) "
            "методом scipy.optimize.brentq на скобке [0.5, 3.0] с xtol = 1e-13 и rtol = 8.9·10⁻¹⁶ — "
            "предел машинной точности. Тот же корень питает оба универсальных множителя, "
            "exp(π/s0) = 22.694383 (длины) и exp(2π/s0) = 515.035001 (энергии), служащие целями "
            "допуска численного слоя."
        ),
        (
            "Гиперрадиальный спектр решается на экспоненциальной сетке s ∈ [0, L], L = ln(Rmax/R0) = "
            "20.7233, с n = 900 равномерных точек (Δs = 0.023051). Трёхдиагональный кинетический "
            "оператор K из (E5) несёт постоянный сдвиг −s0²; симметризация A = D·K·D с "
            "D = diag(R0⁻¹e^(−s)) даёт вещественную симметричную матрицу 900 × 900, "
            "диагонализуемую numpy.linalg.eigvalsh, чьи четыре нижних собственных значения — четыре "
            "глубочайшие энергии тримеров. Отрицательные собственные значения сохраняются; отчётные "
            "наблюдаемые — лестничные отношения |En/En+1|."
        ),
        (
            "Три развёртки допрашивают устойчивость лестницы на том же решателе: развёртка по длине "
            "бокса (L = 4 … 20.723 при фиксированном шаге сетки) зондирует ёмкость бокса; сеточная "
            "развёртка (n = 150 … 2200) — сходимость по дискретизации; развёртка трёхчастичного "
            "параметра (R0 по трём порядкам, семь точек, фиксированная форма бокса) — роль "
            "стенки коротких расстояний. Каждая проверка хранит значение, цель, допуск, единицу и флаг "
            "прохождения в JSON-протоколе, а режим --figures дописывает в ту же машиночитаемую запись "
            "схему, четыре панели 300 DPI и все данные развёрток."
        ),
    ],
    "analysis_en": [
        (
            "**Universal numbers.** The transcendental root is s0 = 1.0062378251027817 against the "
            "literature target 1.0062458 — a deviation of 8·10⁻⁶, inside the 1e-5 acceptance "
            "tolerance. The derived factors follow: exp(π/s0) = 22.694382595366676 (target 22.7, "
            "tolerance 0.05) and exp(2π/s0) = 515.0350013848819 (target 515.03, tolerance 0.05). "
            "These three numbers are the entire nontrivial content of the Efimov effect, and they are "
            "produced here from a single bracketed root solve."
        ),
        (
            "**The ladder.** The 900-point symmetrized eigenproblem yields four negative levels: "
            "−4476.182276766936, −8.683035225538072, −0.01686144228867179 and −3.27·10⁻⁵ (units of "
            "1/R0²) — an energy span of |E0|/|E3| ≈ 1.37·10⁸. The ladder ratios are |E0/E1| = "
            "515.508939 (+0.092%), |E1/E2| = 514.963968 (−0.014%) and |E2/E3| = 514.962911 (−0.014%) "
            "against the universal 515.035001 — deviations of order one part in a thousand, three "
            "orders of magnitude inside the ±35% acceptance band. The corresponding scaling hyperradii "
            "run from 13.0518 to 152604 R0, a size span of 1.2·10⁴ per three rungs."
        ),
        (
            "**Stability.** The box-length sweep shows that wherever two rungs fit (L ≥ 8) the ratio "
            "|E0/E1| is pinned at 515.5089–515.5091 while the number of bound trimers grows 1 → 2 → 3 "
            "→ 4 with the box capacity; at L = 4 and 6 a single trimer fits and the ratio is "
            "undefined. The grid sweep converges monotonically: 512.9606/512.4146 at n = 150 → "
            "515.569/515.024 at n = 2200; the preset n = 900 sits at +0.09% of the universal value, "
            "and the refined continuum limit of this box at +0.10% — both honest readings of the "
            "residual wall effect."
        ),
        (
            "**Scale invariance of the wall.** Across three decades of the three-body parameter "
            "(R0 = 1e-5 … 1e-2, seven points) the deepest energy follows the exact power law |E0| ∝ "
            "R0⁻² with fitted slope −2.000000, dropping from 4.48·10⁷ to 44.76 in units of 1/R0², "
            "while the ladder ratio |E0/E1| stays invariant with spread 1.9·10⁻¹⁰. This is the clean "
            "separation predicted by universality: the wall fixes where the comb sits, the exponent "
            "s0 fixes how far apart the teeth are."
        ),
    ],
    "analysis_ru": [
        (
            "**Универсальные числа.** Трансцендентный корень s0 = 1.0062378251027817 против "
            "литературной цели 1.0062458 — отклонение 8·10⁻⁶, внутри допуска 1e-5. Далее следуют "
            "производные множители: exp(π/s0) = 22.694382595366676 (цель 22.7, допуск 0.05) и "
            "exp(2π/s0) = 515.0350013848819 (цель 515.03, допуск 0.05). Эти три числа — всё "
            "нетривиальное содержание эффекта Ефимова, и здесь они получены одним поиском корня в "
            "скобке."
        ),
        (
            "**Лестница.** Симметризованная задача 900 точек даёт четыре отрицательных уровня: "
            "−4476.182276766936, −8.683035225538072, −0.01686144228867179 и −3.27·10⁻⁵ (единицы "
            "1/R0²) — размах энергий |E0|/|E3| ≈ 1.37·10⁸. Лестничные отношения: |E0/E1| = 515.508939 "
            "(+0.092%), |E1/E2| = 514.963968 (−0.014%) и |E2/E3| = 514.962911 (−0.014%) против "
            "универсального 515.035001 — отклонения порядка одной тысячной, на три порядка внутри "
            "полосы допуска ±35%. Соответствующие масштабные гиперрадиусы тянутся от 13.0518 до "
            "152604 R0 — размах размеров 1.2·10⁴ на три ступени."
        ),
        (
            "**Устойчивость.** Развёртка по длине бокса показывает: всюду, где помещаются две ступени "
            "(L ≥ 8), отношение |E0/E1| закреплено на 515.5089–515.5091, а число связанных тримеров "
            "растёт 1 → 2 → 3 → 4 вместе с ёмкостью бокса; при L = 4 и 6 помещается один тример, и "
            "отношение не определено. Сеточная развёртка сходится монотонно: 512.9606/512.4146 при "
            "n = 150 → 515.569/515.024 при n = 2200; пресетные n = 900 дают +0.09% от универсального "
            "значения, а уточнённый континуальный предел этого бокса — +0.10%; оба числа — честные "
            "показания остаточного влияния стенки."
        ),
        (
            "**Масштабная инвариантность стенки.** По трём порядкам трёхчастичного параметра "
            "(R0 = 1e-5 … 1e-2, семь точек) глубочайшая энергия следует точному степенному закону "
            "|E0| ∝ R0⁻² с наклоном −2.000000, падая от 4.48·10⁷ до 44.76 в единицах 1/R0², тогда как "
            "лестничное отношение |E0/E1| остаётся инвариантным с разбросом 1.9·10⁻¹⁰. Это чистое "
            "разделение, предсказанное универсальностью: стенка фиксирует, где сидит гребёнка, а "
            "показатель s0 — насколько далеко друг от друга её зубцы."
        ),
    ],
    "discussion_en": [
        (
            "The model is deliberately minimal: a single adiabatic hyperradial channel, zero-range "
            "(unitary) two-body interactions, and the three-body parameter represented by the crudest "
            "possible device — a hard wall at R0. Within these assumptions the conclusions are exact "
            "statements about the governing equations rather than simulations of a specific atomic "
            "species. Real systems (caesium, potassium, helium trimers) carry finite-range "
            "corrections and a genuine short-distance three-body parameter E(3); these shift each "
            "rung along the logarithmic axis but — as the R0 sweep of fig04 demonstrates for the wall "
            "model — leave the universal ratios untouched."
        ),
        (
            "The numerical regime is stated honestly: only the four deepest levels are computed, and "
            "their number is box-limited (the sweep shows the trimer count growing 1 → 4 as L grows "
            "to 20.7233, which hosts about 3.3 Efimov oscillations). The measured ladder ratio at the "
            "preset grid (515.509, +0.09%) is a property of the discrete box; the grid-refined value "
            "(515.569 at n = 2200, +0.10%) is the continuum limit of this box. Both sit three orders "
            "of magnitude inside the ±35% acceptance band — a deliberate asymmetry between the "
            "strictness of the physics claim and the generosity of the gate, documented rather than "
            "hidden."
        ),
        (
            "Within the program, this study is the quantum sibling of TRX-06, whose classical CTMC "
            "helium lives in the same hyperradius language (Macek's adiabatic coordinate) and on the "
            "same Wannier-type three-body landscape; TRX-08 provides the opposite limit — a "
            "finite-range harmonic-plus-Coulomb trap whose spectrum is machine-precision but not "
            "universal; and TRX-02 shares the exponential signature, where tanh² amplitude laws and "
            "e^(2π/s0) ladders are both scale-invariant structures. Together with the classical "
            "vortex anchor TRX-09, the block demonstrates the thesis of the monograph: the three-body "
            "problem organizes itself around scale invariance, whether the bodies are classical "
            "vortices, atomic ions or quantum bosons."
        ),
    ],
    "discussion_ru": [
        (
            "Модель сознательно минимальна: один адиабатический гиперрадиальный канал, "
            "нуль-радиальные (унитарные) парные взаимодействия и трёхчастичный параметр, представленный "
            "простейшим устройством — жёсткой стенкой при R0. В этих допущениях выводы — точные "
            "утверждения об определяющих уравнениях, а не симуляция конкретного атомного сорта. "
            "Реальные системы (цезий, калий, тримеры гелия) несут поправки конечного радиуса и "
            "настоящий короткодействующий трёхчастичный параметр E(3); они сдвигают каждую ступень вдоль "
            "логарифмической оси, но — как показывает развёртка R0 на рис. 04 для стеночной модели — "
            "универсальные отношения не трогают."
        ),
        (
            "Численный режим заявлен честно: вычисляются только четыре глубочайших уровня, и их число "
            "ограничено боксом (развёртка показывает рост числа тримеров 1 → 4 по мере роста L до "
            "20.7233, вмещающего около 3.3 осцилляций Ефимова). Измеренное лестничное отношение на "
            "пресетной сетке (515.509, +0.09%) — свойство дискретного бокса; значение с уточнённой "
            "сеткой (515.569 при n = 2200, +0.10%) — континуальный предел этого бокса. Оба сидят на "
            "три порядка внутри полосы допуска ±35% — намеренная асимметрия между строгостью "
            "физического утверждения и щедростью гейта, задокументированная, а не спрятанная."
        ),
        (
            "В рамках программы данное исследование — квантовый собрат TRX-06, чей классический "
            "CTMC-гелий живёт в том же языке гиперрадиуса (адиабатическая координата Мачека) и на том "
            "же ванньеровском трёхчастичном ландшафте; TRX-08 даёт противоположный предел — "
            "гармонически-кулоновскую ловушку конечного радиуса, чей спектр машинно-точен, но не "
            "универсален; TRX-02 разделяет экспоненциальную подпись, где амплитудные законы tanh² и "
            "лестницы e^(2π/s0) — структуры одной масштабной инвариантности. Вместе с классическим "
            "вихревым якорем TRX-09 блок демонстрирует тезис монографии: задача трёх тел "
            "организуется вокруг масштабной инвариантности — будь то классические вихри, атомарные "
            "ионы или квантовые бозоны."
        ),
    ],
    "conclusions_en": [
        "The universal exponent is reproduced from a single bracketed root solve: s0 = 1.0062378 against the literature target 1.0062458 (deviation 8·10⁻⁶, tolerance 1e-5).",
        "The universal factors follow: exp(π/s0) = 22.694383 (target 22.7) for lengths and exp(2π/s0) = 515.035001 (target 515.03) for energies — both within tolerance.",
        "The numerically computed ladder of four trimers (energies −4476.18 … −3.27·10⁻⁵ in 1/R0² units, sizes 13.05 … 152604 R0) gives ratios 515.509 / 514.964 / 514.963 — within ±0.1% of the universal 515.035.",
        "The ladder is box-independent wherever two rungs fit (L ≥ 8): |E0/E1| pinned at 515.5089–515.5091 while the trimer count grows 1 → 4; grid refinement converges monotonically (512.96 → 515.57 over n = 150 → 2200).",
        "The three-body parameter R0 sets the scale only: across three decades the deepest energy follows the exact R0⁻² power law (fitted slope −2.000000) and the ladder ratio stays invariant (spread 1.9·10⁻¹⁰).",
        "The mapping to TRIVORTEX holds structurally: s0 ↔ circulation ratios Γ, the Efimov ladder ↔ the radial modulation ω = (2π/T)·e^(C_Ch/π), and the −1/R² attraction ↔ the scale-invariant binding of Theorem 3.1 — the quantum chapter of the same scale-invariance story.",
    ],
    "conclusions_ru": [
        "Универсальный показатель воспроизведён одним поиском корня в скобке: s0 = 1.0062378 против литературной цели 1.0062458 (отклонение 8·10⁻⁶, допуск 1e-5).",
        "Универсальные множители следуют далее: exp(π/s0) = 22.694383 (цель 22.7) для длин и exp(2π/s0) = 515.035001 (цель 515.03) для энергий — оба внутри допуска.",
        "Численно вычисленная лестница из четырёх тримеров (энергии −4476.18 … −3.27·10⁻⁵ в единицах 1/R0², размеры 13.05 … 152604 R0) даёт отношения 515.509 / 514.964 / 514.963 — в пределах ±0.1% от универсального 515.035.",
        "Лестница не зависит от бокса всюду, где помещаются две ступени (L ≥ 8): |E0/E1| закреплён на 515.5089–515.5091 при росте числа тримеров 1 → 4; сгущение сетки сходится монотонно (512.96 → 515.57 по n = 150 → 2200).",
        "Трёхчастичный параметр R0 задаёт только масштаб: по трём порядкам глубочайшая энергия следует точному закону R0⁻² (наклон −2.000000), а лестничное отношение остаётся инвариантным (разброс 1.9·10⁻¹⁰).",
        "Соответствие TRIVORTEX структурно: s0 ↔ отношения циркуляций Γ, лестница Ефимова ↔ радиальная модуляция ω = (2π/T)·e^(C_Ch/π), притяжение −1/R² ↔ масштабно-инвариантное связывание теоремы 3.1 — квантовая глава той же истории масштабной инвариантности.",
    ],
    "references": [
        "1. Efimov, V. (1970). *Energy levels arising from resonant two-body forces in a three-body system.* Phys. Lett. B 33, 563–564.",
        "2. Efimov, V. (1971). *Weakly bound states of three resonantly interacting particles.* Sov. J. Nucl. Phys. 12, 589–595.",
        "3. Faddeev, L. D. (1961). *Scattering theory for a three-particle system.* Sov. Phys. JETP 12, 1014–1019.",
        "4. Macek, J. H. (1968). *Properties of autoionizing states of He.* J. Phys. B 1, 831–843.",
        "5. Amado, R. D., Greenwood, F. C. (1977). *There is no Efimov effect for four or more particle systems.* Phys. Rev. D 15, 838–840.",
        "6. Braaten, E., Hammer, H.-W. (2006). *Universality in few-body systems with large scattering length.* Phys. Rep. 428, 259–390.",
        "7. Kraemer, T. et al. (2006). *Evidence for Efimov quantum states in an ultracold gas of caesium atoms.* Nature 440, 315–319.",
        "8. Zaccanti, M. et al. (2009). *Observation of an Efimov spectrum in an atomic system.* Nature Phys. 5, 586–591.",
        "9. Chin, C., Grimm, R., Julienne, P., Tiesinga, E. (2010). *Feshbach resonances in ultracold gases.* Rev. Mod. Phys. 82, 1225–1286.",
        "10. Kunitski, M. et al. (2015). *Three-body bound states in atomic helium trimers.* Science 348, 551–555.",
    ],
    "crosslinks_en": [
        "* **TRX-06** is the classical (CTMC) three-body benchmark in the same atomic setting — the same hyperradius coordinate, now on the Wannier threshold landscape.",
        "* **TRX-08** realizes controllable three-body crystals in a linear Paul trap whose harmonic-plus-Coulomb spectrum is verified to machine precision — the finite-range, non-universal counterpart of the Efimov ladder.",
        "* **TRX-02** shares the exponential (geometric) structure — tanh² amplitude laws and e^(2π/s0) ladders are both scale-invariant signatures.",
    ],
    "crosslinks_ru": [
        "* **TRX-06** — классический (CTMC) трёхчастичный бенчмарк в том же атомном окружении — тот же гиперрадиус, но на ландшафте порога Ваннье.",
        "* **TRX-08** реализует управляемые трёхчастичные кристаллы в линейной ловушке Пауля, чей гармонически-кулоновский спектр проверен с машинной точностью, — двойник лестницы Ефимова конечного радиуса, неуниверсальный.",
        "* **TRX-02** разделяет экспоненциальную (геометрическую) структуру — амплитудные законы tanh² и лестницы e^(2π/s0) суть подписи одной масштабной инвариантности.",
    ],
    "assumptions_en": [
        "Zero-range (unitary) limit: scattering length a → ∞; no finite-range corrections to the two-body interaction.",
        "A single adiabatic hyperradial channel is retained; coupling to other hyperangular channels is neglected.",
        "s-wave symmetry, identical bosons — no fermionic suppression, no mixed-sign statistics.",
        "The three-body parameter is modeled as a hard wall at R = R0; no other short-range physics.",
        "Only the four deepest levels are computed; the ladder continues indefinitely in principle but is box-limited here.",
        "Units ħ²/m = 1; only dimensionless ratios are treated as physical observables.",
    ],
    "assumptions_ru": [
        "Нуль-радиальный (унитарный) предел: длина рассеяния a → ∞; поправки конечного радиуса к парному взаимодействию отсутствуют.",
        "Сохраняется один адиабатический гиперрадиальный канал; связью с другими гиперугловыми каналами пренебрегаем.",
        "s-волновая симметрия, одинаковые бозоны — без фермионного подавления и смешанной статистики.",
        "Трёхчастичный параметр моделируется жёсткой стенкой при R = R0; иной короткодействующей физики нет.",
        "Вычисляются только четыре глубочайших уровня; в принципе лестница продолжается неограниченно, но здесь ограничена боксом.",
        "Единицы ħ²/m = 1; физическими наблюдаемыми считаются только безразмерные отношения.",
    ],
    "glance_en": [
        ["Block", "Quantum three-body — study 07 of 12"],
        [
            "Model",
            "three identical bosons at unitarity on the hyperradial −(s0² − ¼)/R² attraction",
        ],
        [
            "Key invariant",
            "universal exponent s0 = 1.0062378 (the ladder ratios are exact invariants)",
        ],
        [
            "Headline result",
            "measured ladder ratio E0/E1 = 515.509 vs universal e^(2π/s0) = 515.035 (+0.09%)",
        ],
        ["Verification", "6/6 checks PASS (full mode)"],
        ["Runtime", "5.77 s full (with --figures) · < 20 s smoke"],
    ],
    "glance_ru": [
        ["Блок", "Квантовые три тела — исследование 07 из 12"],
        [
            "Модель",
            "три одинаковых бозона в пределе унитарности на гиперрадиальном притяжении −(s0² − ¼)/R²",
        ],
        [
            "Ключевой инвариант",
            "универсальный показатель s0 = 1.0062378 (лестничные отношения — точные инварианты)",
        ],
        [
            "Главный результат",
            "измеренная лестница: отношение E0/E1 = 515.509 против универсального e^(2π/s0) = 515.035 (+0.09%)",
        ],
        ["Верификация", "6/6 проверок PASS (полный режим)"],
        ["Время выполнения", "5.77 с полный (с --figures) · < 20 с smoke"],
    ],
    "glossary": {
        "header_en": ["Term", "Definition"],
        "header_ru": ["Термин", "Определение"],
        "rows_en": [
            [
                "Efimov effect",
                "infinite series of bound three-body states for resonant two-body interactions; exists only at N = 3",
            ],
            ["Trimer", "a bound state of three particles; the rungs of the Efimov ladder"],
            [
                "Unitarity (unitary limit)",
                "scattering length a → ∞: maximal two-body cross-section, no two-body dimer",
            ],
            [
                "Scattering length a",
                "the low-energy two-body parameter sent to infinity in the unitary limit",
            ],
            [
                "Hyperradius R",
                "size of the triangle formed by the three particles; the collective radial coordinate",
            ],
            [
                "Three-body parameter",
                "short-distance input that breaks scale invariance; here the hard wall R0",
            ],
            [
                "Universal exponent s0",
                "root of s·cosh(πs/2) = (8/√3)·sinh(πs/6); fixes the hyperradial attraction −(s0² − ¼)/R²",
            ],
            [
                "Geometric (Efimov) ladder",
                "the spectrum E_n ∝ exp(−2πn/s0), R_n ∝ exp(πn/s0) produced by scale invariance",
            ],
            [
                "Log-periodicity",
                "equal spacing Δs = π/s0 = 3.1221 of the rungs in s = ln(R/R0) space",
            ],
            [
                "Faddeev equations",
                "splitting of the three-body wave function into pair amplitudes; the origin of (E1)",
            ],
            [
                "brentq",
                "bracketed root-finding algorithm (scipy) used for the transcendental equation",
            ],
        ],
        "rows_ru": [
            [
                "Эффект Ефимова",
                "бесконечная серия связанных трёхчастичных состояний при резонансном парном взаимодействии; существует только при N = 3",
            ],
            ["Тример", "связанное состояние трёх частиц; ступень лестницы Ефимова"],
            [
                "Унитарность (унитарный предел)",
                "длина рассеяния a → ∞: максимальное парное сечение, двухчастичного димера нет",
            ],
            [
                "Длина рассеяния a",
                "низкоэнергетический парный параметр, устремляемый к бесконечности в унитарном пределе",
            ],
            [
                "Гиперрадиус R",
                "размер треугольника, образуемого тремя частицами; коллективная радиальная координата",
            ],
            [
                "Трёхчастичный параметр",
                "короткодействующий вход, нарушающий масштабную инвариантность; здесь жёсткая стенка R0",
            ],
            [
                "Универсальный показатель s0",
                "корень уравнения s·cosh(πs/2) = (8/√3)·sinh(πs/6); задаёт притяжение −(s0² − ¼)/R²",
            ],
            [
                "Геометрическая лестница Ефимова",
                "спектр E_n ∝ exp(−2πn/s0), R_n ∝ exp(πn/s0), порождаемый масштабной инвариантностью",
            ],
            [
                "Лог-периодичность",
                "равный шаг Δs = π/s0 = 3.1221 между ступенями в пространстве s = ln(R/R0)",
            ],
            [
                "Уравнения Фаддеева",
                "разбиение волновой функции трёх тел на парные амплитуды; источник (E1)",
            ],
            [
                "brentq",
                "метод поиска корня в скобке (scipy), применённый к трансцендентному уравнению",
            ],
        ],
    },
    "notation": {
        "header_en": ["Symbol", "Meaning"],
        "header_ru": ["Символ", "Смысл"],
        "rows_en": [
            ["s0", "universal Efimov exponent, root of (E1); computed 1.0062378, target 1.0062458"],
            ["R", "hyperradius of the three-particle triangle"],
            ["R0", "three-body parameter: hard wall at short distance (value 1e-3)"],
            ["Rmax", "outer Dirichlet wall of the box (value 1e6)"],
            ["L", "box length in log space, L = ln(Rmax/R0) = 20.723266"],
            ["s", "logarithmic hyperradius, s = ln(R/R0) ∈ [0, L]"],
            ["u(R), v(s)", "hyperradial wave function and its log-grid image (u = e^(s/2)·v)"],
            ["E_n", "n-th trimer energy (units of 1/R0²); E0 = −4476.18 … E3 = −3.27·10⁻⁵"],
            ["Δs = π/s0", "ladder spacing in log space = 3.1221"],
            [
                "a_*",
                "scattering length at which the n-th trimer appears; a_* ladder factor exp(π/s0)",
            ],
            ["ħ²/m", "unit-setting quantum combination, set to 1"],
        ],
        "rows_ru": [
            [
                "s0",
                "универсальный показатель Ефимова, корень (E1); вычислен 1.0062378, цель 1.0062458",
            ],
            ["R", "гиперрадиус треугольника трёх частиц"],
            ["R0", "трёхчастичный параметр: жёсткая стенка на малых расстояниях (значение 1e-3)"],
            ["Rmax", "внешняя стенка Дирихле бокса (значение 1e6)"],
            ["L", "длина бокса в лог-пространстве, L = ln(Rmax/R0) = 20.723266"],
            ["s", "логарифмический гиперрадиус, s = ln(R/R0) ∈ [0, L]"],
            [
                "u(R), v(s)",
                "гиперрадиальная волновая функция и её образ на лог-сетке (u = e^(s/2)·v)",
            ],
            ["E_n", "n-я энергия тримера (единицы 1/R0²); E0 = −4476.18 … E3 = −3.27·10⁻⁵"],
            ["Δs = π/s0", "шаг лестницы в лог-пространстве = 3.1221"],
            [
                "a_*",
                "длина рассеяния, при которой появляется n-й тример; множитель лестницы exp(π/s0)",
            ],
            ["ħ²/m", "квантовая комбинация, задающая единицы, положена равной 1"],
        ],
    },
    "params_appendix": {
        "header_en": ["Symbol", "Value", "Role"],
        "header_ru": ["Символ", "Значение", "Роль"],
        "rows_en": [
            [
                "s0",
                "1.0062378 (target 1.0062458, tol 1e-5)",
                "universal exponent; strength of the hyperradial channel",
            ],
            [
                "brentq bracket",
                "[0.5, 3.0], xtol = 1e-13",
                "root isolation of the transcendental equation",
            ],
            ["R0", "1e-3", "three-body parameter (hard wall, short-distance phase)"],
            ["Rmax", "1e6", "outer Dirichlet wall"],
            ["L", "20.723266", "box length in s = ln(R/R0); ≈ 3.3 Efimov oscillations"],
            ["n_grid", "900", "uniform FD grid points in s"],
            ["Δs", "0.023051", "grid spacing in log space"],
            ["levels", "4", "deepest trimers computed (negative eigenvalues)"],
            ["exp(π/s0)", "22.694383", "universal size factor per rung"],
            [
                "exp(2π/s0)",
                "515.035001",
                "universal energy factor per rung; ladder acceptance band ±35%",
            ],
        ],
        "rows_ru": [
            [
                "s0",
                "1.0062378 (цель 1.0062458, допуск 1e-5)",
                "универсальный показатель; сила гиперрадиального канала",
            ],
            [
                "скобка brentq",
                "[0.5, 3.0], xtol = 1e-13",
                "локализация корня трансцендентного уравнения",
            ],
            ["R0", "1e-3", "трёхчастичный параметр (жёсткая стенка, фаза коротких расстояний)"],
            ["Rmax", "1e6", "внешняя стенка Дирихле"],
            ["L", "20.723266", "длина бокса в s = ln(R/R0); ≈ 3.3 осцилляции Ефимова"],
            ["n_grid", "900", "число равномерных точек конечно-разностной сетки в s"],
            ["Δs", "0.023051", "шаг сетки в лог-пространстве"],
            ["уровни", "4", "глубочайшие вычисляемые тримеры (отрицательные собственные значения)"],
            ["exp(π/s0)", "22.694383", "универсальный множитель размера за ступень"],
            [
                "exp(2π/s0)",
                "515.035001",
                "универсальный множитель энергии за ступень; полоса допуска лестницы ±35%",
            ],
        ],
    },
    "bibtex": [
        "@article{efimov1970,",
        "  author  = {Efimov, Vitaly},",
        "  title   = {Energy levels arising from resonant two-body forces in a three-body system},",
        "  journal = {Physics Letters B},",
        "  year    = {1970}, volume = {33}, pages = {563--564}}",
        "",
        "@article{braaten2006,",
        "  author  = {Braaten, Eric and Hammer, Hans-Werner},",
        "  title   = {Universality in few-body systems with large scattering length},",
        "  journal = {Physics Reports},",
        "  year    = {2006}, volume = {428}, pages = {259--390}}",
        "",
        "@article{kraemer2006,",
        "  author  = {Kraemer, Tobias and others},",
        "  title   = {Evidence for Efimov quantum states in an ultracold gas of caesium atoms},",
        "  journal = {Nature},",
        "  year    = {2006}, volume = {440}, pages = {315--319}}",
        "",
        "@article{chin2010,",
        "  author  = {Chin, Cheng and Grimm, Rudolf and Julienne, Paul and Tiesinga, Eite},",
        "  title   = {Feshbach resonances in ultracold gases},",
        "  journal = {Reviews of Modern Physics},",
        "  year    = {2010}, volume = {82}, pages = {1225--1286}}",
    ],
}
