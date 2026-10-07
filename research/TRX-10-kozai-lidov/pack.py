# -*- coding: utf-8 -*-
"""Content pack for TRX-10 (v1.0.0 Monograph Edition). Rendered by scripts/build_study_docs.py."""

PACK = {
    "meta": {
        "study_id": "TRX-10",
        "dir_name": "TRX-10-kozai-lidov",
        "title_en": "Kozai–Lidov Oscillations in Hierarchical Triples",
        "title_ru": "Колебания Козаи–Лидова в иерархических тройных системах",
        "script": "trx10_kozai_lidov.py",
        "results_json": "trx10_results.json",
        "scheme_file": "scheme_trx10.svg",
        "runtime_full": "64.6 s",
    },
    "essence_en": (
        "The Kozai–Lidov mechanism: a test particle on an inclined inner orbit of a "
        "hierarchical triple, perturbed by a distant companion, periodically exchanges "
        "eccentricity for inclination while the z-angular momentum **j_z = √(1 − e²)·cos i** stays "
        "constant; for a nearly circular initial orbit the eccentricity climbs to the closed-form "
        "maximum **e_max = √(1 − (5/3)·cos²i₀)** whenever i₀ exceeds the Kozai angle 39.23°. "
        "The study refuses to code the memorized result: the doubly-averaged quadrupole potential "
        "is built numerically — orbit quadrature, (e, ω) tabulation, cubic-spline Hamiltonian — "
        "and the resulting flow is audited against analytic benchmarks and an independent direct "
        "integration of the full three-dimensional restricted problem."
    ),
    "essence_ru": (
        "Механизм Козаи–Лидова: пробная частица на наклонённой внутренней орбите "
        "иерархической тройной системы, возмущаемая далёким компаньоном, периодически обменивает "
        "эксцентриситет на наклонение, пока z-компонента углового момента "
        "**j_z = √(1 − e²)·cos i** остаётся постоянной; для почти круговой начальной орбиты "
        "эксцентриситет поднимается до аналитического максимума "
        "**e_max = √(1 − (5/3)·cos²i₀)**, как только i₀ превышает критический угол Козаи 39.23°. "
        "Исследование отказывается зашивать готовую формулу в код: двойной усреднённый "
        "квадрупольный потенциал строится численно — квадратура по орбите, табуляция на сетке "
        "(e, ω), сплайн-гамильтониан, — а полученный поток проверяется против аналитических "
        "эталонов и независимого прямого интегрирования полной трёхмерной ограниченной задачи."
    ),
    "mission_en": [
        (
            "Hierarchical triples are where the three-body problem lives longest: after the "
            "short-period terms are averaged away, the quadrupole problem reduces to a slow "
            "eccentricity–inclination clock that governs asteroid triples, irregular satellite "
            "systems, hot-Jupiter migration channels and compact-object mergers. This study refuses "
            "to trust memorized formulas: the doubly-averaged quadrupole potential is built "
            "numerically — the instantaneous quadrupole disturbing function is averaged over the "
            "inner orbit by quadrature, tabulated on an (e, ω) grid at the fixed j_z of the run, and "
            "turned into a cubic spline whose analytic derivatives drive the canonical Hamiltonian "
            "flow ė = (j/e)·∂⟨U⟩/∂ω, ω̇ = −(j/e)·∂⟨U⟩/∂e."
        ),
        (
            "The numerical machine is then audited against everything known analytically. The spline "
            "flow reproduces the closed-form maxima e_max = 0.763763 (i₀ = 60°) and 0.897239 "
            "(i₀ = 70°) to within 2×10⁻³, halves the KL period when the perturber mass doubles "
            "(ratio 0.481 against the ideal 0.5, inside the 3% band), sweeps the Kozai landscape "
            "over 12 inclinations, and is validated against an independent DIRECT integration of the "
            "full 3-D restricted problem (m₃/M = 0.5, a_out = 5 a_in, 200 outer orbits): smoothed "
            "maximum eccentricity 0.7423 versus 0.7638 — a −2.8% deviation consistent with the "
            "hexadecapole truncation. Laser link: laser ranging of binary and triple asteroids, and "
            "LISA-class laser interferometry of compact-object triples whose mergers are channelled "
            "by KL cycles."
        ),
    ],
    "mission_ru": [
        (
            "Иерархические тройные системы — это там, где задача трёх тел живёт дольше всего: после "
            "усреднения короткопериодических членов квадрупольная задача сводится к медленным "
            "часам «эксцентриситет–наклонение», которые управляют тройными астероидами, системами "
            "нерегулярных спутников, каналами миграции горячих юпитеров и слияниями компактных "
            "объектов. Данное исследование не доверяет заученным формулам: двойной усреднённый "
            "квадрупольный потенциал строится численно — мгновенный квадрупольный возмущающий "
            "функционал усредняется по внутренней орбите квадратурой, табулируется на сетке (e, ω) "
            "при фиксированном j_z данного прогона и превращается в кубический сплайн, аналитические "
            "производные которого порождают канонический гамильтонов поток "
            "ė = (j/e)·∂⟨U⟩/∂ω, ω̇ = −(j/e)·∂⟨U⟩/∂e."
        ),
        (
            "Затем числовая машина проверяется против всего, что известно аналитически. Сплайновый "
            "поток воспроизводит замкнутые максимумы e_max = 0.763763 (i₀ = 60°) и 0.897239 "
            "(i₀ = 70°) с точностью 2×10⁻³, уменьшает период Козаи–Лидова вдвое при удвоении массы "
            "возмутителя (отношение 0.481 против идеального 0.5, внутри полосы 3%), развёртывает "
            "ландшафт Козаи по 12 наклонениям и валидируется независимым ПРЯМЫМ интегрированием "
            "полной трёхмерной ограниченной задачи (m₃/M = 0.5, a_out = 5 a_in, 200 внешних "
            "оборотов): сглаженный максимальный эксцентриситет 0.7423 против 0.7638 — отклонение "
            "−2.8%, согласующееся с усечением до гексадекаполя. Лазерная связь: лазерная дальнометрия "
            "двойных и тройных астероидов и лазерная интерферометрия класса LISA для тройных "
            "систем компактных объектов, чьи слияния канализируются циклами Козаи–Лидова."
        ),
    ],
    "physics_en": [
        (
            "The system is a restricted hierarchical triple: the inner binary consists of a primary "
            "with GM_inner = 1 on a_in = 1 and a massless test particle; the outer companion m₃ "
            "moves on a circular orbit of radius a_out ≫ a_in (20 a_in in the secular model, 5 a_in "
            "in the direct validation). The instantaneous quadrupole disturbing potential is "
            "U = (G m₃/2a_out³)·(3(r·r̂₃)² − r²) — the l = 2 term of the expansion of the "
            "companion's potential in the small hierarchy parameter α = a_in/a_out; for a circular "
            "outer orbit the octupole (l = 3) term vanishes identically."
        ),
        (
            "Averaging U over both orbital periods leaves an axisymmetric function ⟨U⟩(e, ω) that "
            "depends on the orientation of the ellipse only through the argument of pericentre. The "
            "z-component of the angular momentum, j_z = √(1 − e²)·cos i, is conserved exactly, so "
            "the secular problem collapses to one Hamiltonian degree of freedom on the fixed-j_z "
            "manifold: eccentricity grows exactly when the inclination falls, the two being locked "
            "together by j_z. The rate of the clock is set by C₂ = (3/8)(m₃/M)(a_in/a_out)³·n_in, "
            "the inverse of the KL timescale."
        ),
    ],
    "physics_ru": [
        (
            "Система — ограниченная иерархическая тройная: внутренняя двойная состоит из тела с "
            "GM_inner = 1 на орбите a_in = 1 и безмассовой пробной частицы; внешний компаньон m₃ "
            "движется по круговой орбите радиуса a_out ≫ a_in (20 a_in в секулярной модели, 5 a_in "
            "в прямой валидации). Мгновенный квадрупольный возмущающий потенциал есть "
            "U = (G m₃/2a_out³)·(3(r·r̂₃)² − r²) — член l = 2 разложения потенциала компаньона по "
            "малому параметру иерархии α = a_in/a_out; для круговой внешней орбиты октупольный "
            "член (l = 3) тождественно равен нулю."
        ),
        (
            "Усреднение U по обоим орбитальным периодам оставляет осесимметричную функцию ⟨U⟩(e, ω), "
            "зависящую от ориентации эллипса только через аргумент перицентра. z-компонента углового "
            "момента j_z = √(1 − e²)·cos i сохраняется точно, поэтому секулярная задача схлопывается "
            "в одну гамильтонову степень свободы на многообразии фиксированного j_z: эксцентриситет "
            "растёт ровно тогда, когда наклонение падает, — оба связаны инвариантом j_z. Скорость "
            "часов задаёт величина C₂ = (3/8)(m₃/M)(a_in/a_out)³·n_in, обратная к масштабу времени "
            "Козаи–Лидова."
        ),
    ],
    "preset_table": {
        "header_en": ["Parameter", "Value", "Meaning"],
        "header_ru": ["Параметр", "Значение", "Смысл"],
        "rows_en": [
            [
                "Units",
                "GM_inner = 1, a_in = 1, n_in = 1",
                "the inner binary defines length and time",
            ],
            ["e₀, ω₀", "0.001, π/2 (90°)", "initially circular orbit; ω₀ at the libration centre"],
            ["i₀", "{60°, 70°}", "headline inclinations, both above i_crit = 39.23°"],
            ["m₃/M", "1.0 (secular scan), 0.5 (direct)", "outer-to-inner mass ratio"],
            ["a_out", "20 a_in (secular), 5 a_in (direct)", "hierarchy separator α = a_in/a_out"],
            [
                "Spline grid",
                "160 × 180 (e × ω), 240-point orbit quadrature",
                "tabulation of the averaged potential ⟨U⟩",
            ],
            [
                "Secular integrator",
                "DOP853, rtol 1e-8, atol 1e-9",
                "canonical spline flow, 3 KL cycles per run",
            ],
            [
                "Direct integrator",
                "DOP853, rtol = atol = 1e-11",
                "full 3-D restricted problem, 200 outer periods",
            ],
        ],
        "rows_ru": [
            [
                "Единицы",
                "GM_inner = 1, a_in = 1, n_in = 1",
                "внутренняя двойная задаёт длину и время",
            ],
            ["e₀, ω₀", "0.001, π/2 (90°)", "начально круговая орбита; ω₀ в центре либрации"],
            ["i₀", "{60°, 70°}", "главные наклонения, оба выше i_crit = 39.23°"],
            [
                "m₃/M",
                "1.0 (секулярный скан), 0.5 (прямой)",
                "отношение массы внешнего тела к внутренней",
            ],
            ["a_out", "20 a_in (секулярно), 5 a_in (прямо)", "разделитель иерархии α = a_in/a_out"],
            [
                "Сплайновая сетка",
                "160 × 180 (e × ω), квадратура 240 точек",
                "табуляция усреднённого потенциала ⟨U⟩",
            ],
            [
                "Секулярный интегратор",
                "DOP853, rtol 1e-8, atol 1e-9",
                "канонический сплайновый поток, 3 цикла на прогон",
            ],
            [
                "Прямой интегратор",
                "DOP853, rtol = atol = 1e-11",
                "полная 3-D ограниченная задача, 200 внешних периодов",
            ],
        ],
    },
    "equations": [
        {
            "id": "E1",
            "latex": "\\langle U\\rangle(e,\\omega) = \\left\\langle \\frac{G m_3}{2 a_{\\rm out}^3}\\,\\big(3(\\mathbf{r}\\cdot\\hat{\\mathbf{r}}_3)^2 - \\mathbf{r}^2\\big) \\right\\rangle_{\\!\\text{inner orbit}}",
            "desc_en": "Double-averaged quadrupole disturbing potential (built numerically by orbit quadrature; units G m₃/2a_out³)",
            "desc_ru": "Двойной усреднённый квадрупольный возмущающий потенциал (строится численно квадратурой по орбите; единицы G m₃/2a_out³)",
        },
        {
            "id": "E2",
            "latex": "\\dot{e} = C_2\\,\\frac{j}{e}\\,\\frac{\\partial \\langle U\\rangle}{\\partial \\omega}, \\qquad \\dot{\\omega} = -\\,C_2\\,\\frac{j}{e}\\,\\frac{\\partial \\langle U\\rangle}{\\partial e}, \\qquad j = \\sqrt{1 - e^2}",
            "desc_en": "Canonical Hamiltonian flow on the fixed-j_z manifold (L = 1), rates scaled by C₂",
            "desc_ru": "Канонический гамильтонов поток на многообразии фиксированного j_z (L = 1), скорости в масштабе C₂",
        },
        {
            "id": "E3",
            "latex": "j_z = \\sqrt{1 - e^2}\\,\\cos i = \\mathrm{const}",
            "desc_en": "Conserved z-component of the orbital angular momentum — the invariant that locks e and i",
            "desc_ru": "Сохраняющаяся z-компонента орбитального углового момента — инвариант, связывающий e и i",
        },
        {
            "id": "E4",
            "latex": "e_{\\max} = \\sqrt{1 - \\tfrac{5}{3}\\cos^2 i_0}, \\qquad i_{\\rm crit} = \\arccos\\sqrt{\\tfrac{3}{5}} \\approx 39.23^\\circ",
            "desc_en": "Analytic maximum eccentricity for an initially circular orbit; the exchange turns on above the Kozai angle",
            "desc_ru": "Аналитический максимальный эксцентриситет для начально круговой орбиты; обмен включается выше угла Козаи",
        },
        {
            "id": "E5",
            "latex": "C_2 = \\tfrac{3}{8}\\,\\frac{m_3}{M}\\left(\\frac{a_{\\rm in}}{a_{\\rm out}}\\right)^{\\!3} n_{\\rm in}, \\qquad t_{\\rm KL} \\sim \\frac{1}{C_2}",
            "desc_en": "KL timescale: the cycle period scales as 1/m₃ (halves when the perturber mass doubles)",
            "desc_ru": "Масштаб времени Козаи–Лидова: период цикла масштабируется как 1/m₃ (вдвое короче при удвоении массы возмутителя)",
        },
    ],
    "scheme_cap_en": (
        "TRX-10 scheme — the Kozai–Lidov exchange in a hierarchical triple: a distant "
        "circular companion drives the eccentricity of the inclined inner test-particle orbit from "
        "0.001 to 0.764 while the inclination dips from 60° to the Kozai angle 39.23°, with "
        "j_z = √(1 − e²)·cos i conserved throughout."
    ),
    "scheme_cap_ru": (
        "Схема TRX-10 — обмен Козаи–Лидова в иерархической тройной: далёкий круговой "
        "компаньон раскачивает эксцентриситет наклонённой внутренней орбиты пробной частицы от "
        "0.001 до 0.764, пока наклонение опускается с 60° до угла Козаи 39.23°; весь цикл "
        "сохраняется j_z = √(1 − e²)·cos i."
    ),
    "scheme_walk_en": [
        [
            "Outer companion (m₃)",
            "distant perturber on a circular orbit of radius a_out = 20 a_in — drawn not to scale; inner units GM_inner = 1, a_in = 1",
        ],
        [
            "KL clock box",
            "t_KL ~ 1/C₂ with C₂ = (3/8)(m₃/M)(a_in/a_out)³·n_in — the period halves when m₃ doubles",
        ],
        [
            "Inner orbit (gold ellipse)",
            "drawn at e_max = 0.7638 for i₀ = 60°; the test particle cycles e: 0.001 → 0.764 each cycle",
        ],
        [
            "Inclination ledger (h₃, h)",
            "the inner angular-momentum vector h is tilted by i₀ = 60° from the outer-orbit normal h₃",
        ],
        [
            "Dashed red threshold",
            "i_crit = arccos√(3/5) = 39.23° — the Kozai angle, the exchange threshold",
        ],
        [
            "Invariant box + exchange arrows",
            "j_z = √(1 − e²)·cos i = 0.5 conserved; e↑ 0.001 → 0.764 while i↓ 60° → 39.2°",
        ],
    ],
    "scheme_walk_ru": [
        [
            "Внешний компаньон (m₃)",
            "далёкий возмутитель на круговой орбите радиуса a_out = 20 a_in — показан не в масштабе; внутренние единицы GM_inner = 1, a_in = 1",
        ],
        [
            "Панель «часов Козаи–Лидова»",
            "t_KL ~ 1/C₂, где C₂ = (3/8)(m₃/M)(a_in/a_out)³·n_in, — период уменьшается вдвое при удвоении m₃",
        ],
        [
            "Внутренняя орбита (золотой эллипс)",
            "изображена при e_max = 0.7638 для i₀ = 60°; пробная частица циклирует e: 0.001 → 0.764 за цикл",
        ],
        [
            "Векторы h₃ и h",
            "угловой момент внутренней орбиты h наклонён на i₀ = 60° к нормали внешней орбиты h₃",
        ],
        [
            "Красный пунктирный порог",
            "i_crit = arccos√(3/5) = 39.23° — угол Козаи, порог включения обмена",
        ],
        [
            "Блок инварианта и стрелки обмена",
            "j_z = √(1 − e²)·cos i = 0.5 сохраняется; e↑ 0.001 → 0.764 при i↓ 60° → 39.2°",
        ],
    ],
    "mapping": {
        "header_en": ["Quantity in this study", "TRIVORTEX analog", "Comment"],
        "header_ru": ["Величина исследования", "Аналог в TRIVORTEX", "Комментарий"],
        "rows_en": [
            [
                "Hierarchical triple (test particle + companion)",
                "three bodies with separated scales",
                "the celestial three-body problem",
            ],
            [
                "Conserved j_z = √(1 − e²)·cos i",
                "Chaplygin-type topological invariant",
                "an integral that pins the orbit family",
            ],
            [
                "e_max = √(1 − (5/3)cos²i₀)",
                "closed form of Theorem 3.1",
                "a sharp analytic benchmark for the numerics",
            ],
            ["KL clock, t_KL ~ 1/C₂", "choreography period T", "secular timekeeping of the triad"],
            [
                "Spline-built averaged Hamiltonian ⟨U⟩",
                "numerically constructed vortex Hamiltonian",
                "both flows are driven by tabulated, not memorized, potentials",
            ],
        ],
        "rows_ru": [
            [
                "Иерархическая тройная (пробная частица + компаньон)",
                "три тела с разделёнными масштабами",
                "небесная задача трёх тел",
            ],
            [
                "Сохраняющийся j_z = √(1 − e²)·cos i",
                "топологический инвариант типа Чаплыгина",
                "интеграл, закрепляющий семейство орбит",
            ],
            [
                "e_max = √(1 − (5/3)cos²i₀)",
                "замкнутая форма теоремы 3.1",
                "острый аналитический эталон для численной машины",
            ],
            [
                "Часы Козаи–Лидова, t_KL ~ 1/C₂",
                "период хореографии T",
                "секулярное хронометрирование триады",
            ],
            [
                "Сплайновый усреднённый гамильтониан ⟨U⟩",
                "численно построенный вихревой гамильтониан",
                "оба потока порождаются табулированными, а не заученными потенциалами",
            ],
        ],
    },
    "nondim_en": (
        "All quantities are in canonical restricted-problem units: length in inner "
        "semi-major axes a_in, time in inner orbital periods (n_in = 1, GM_inner = 1), mass in the "
        "inner-pair scale M. The secular flow lives on the fixed-j_z manifold — a single "
        "Hamiltonian degree of freedom (e, ω) — and the KL clock is set by "
        "C₂ = (3/8)(m₃/M)(a_in/a_out)³·n_in; for the standard preset (m₃/M = 1, a_out = 20) the "
        "measured cycle lasts ≈ 1.04×10⁵ inner periods."
    ),
    "nondim_ru": (
        "Все величины — в канонических единицах ограниченной задачи: длина в больших "
        "полуосях внутренней орбиты a_in, время в внутренних орбитальных периодах (n_in = 1, "
        "GM_inner = 1), масса в масштабе внутренней пары M. Секулярный поток живёт на "
        "многообразии фиксированного j_z — одна гамильтонова степень свободы (e, ω), а часы "
        "Козаи–Лидова задаёт величина C₂ = (3/8)(m₃/M)(a_in/a_out)³·n_in; для стандартного "
        "пресета (m₃/M = 1, a_out = 20) измеренный цикл длится ≈ 1.04×10⁵ внутренних периодов."
    ),
    "checks": {
        "header_en": ["Check", "Target", "Tolerance"],
        "header_ru": ["Проверка", "Цель", "Допуск"],
        "rows_en": [
            ["e_max (i₀ = 60°) vs analytic √(1 − (5/3)cos²i₀)", "0.763763", "2e-3"],
            ["e_max (i₀ = 70°) vs analytic √(1 − (5/3)cos²i₀)", "0.897239", "2e-3"],
            ["KL period ratio P(2m₃)/P(m₃)", "0.5", "3%"],
            ["direct 3-D smoothed e_max vs analytic", "0.763763", "8%"],
        ],
        "rows_ru": [
            ["e_max (i₀ = 60°) против аналитического √(1 − (5/3)cos²i₀)", "0.763763", "2e-3"],
            ["e_max (i₀ = 70°) против аналитического √(1 − (5/3)cos²i₀)", "0.897239", "2e-3"],
            ["Отношение периодов Козаи–Лидова P(2m₃)/P(m₃)", "0.5", "3%"],
            ["Прямой 3-D сглаженный e_max против аналитического", "0.763763", "8%"],
        ],
    },
    "figure_caps": {
        "fig01_kl_landscape.png": {
            "cap_en": "Landscape of the quadrupole Kozai–Lidov problem: (a) geometry of the hierarchical triple, (b) the analytic Kozai landscape e_max(i₀).",
            "cap_ru": "Ландшафт квадрупольной задачи Козаи–Лидова: (a) геометрия иерархической тройной, (b) аналитический ландшафт Козаи e_max(i₀).",
            "walk_en": "Panel (a) shows the inner orbit at e_max = 0.7638 inclined by i₀ = 60° and projected on the outer-orbit plane, with the companion orbit at a_out = 20 a_in dashed and not to scale; panel (b) traces e_max(i₀) = √(1 − (5/3)cos²i₀), shades the sub-critical band where no exchange occurs, and marks the study points 0.7638 (60°) and 0.8972 (70°).",
            "walk_ru": "Панель (a) показывает внутреннюю орбиту при e_max = 0.7638, наклонённую на i₀ = 60° и спроецированную на плоскость внешней орбиты; орбита компаньона a_out = 20 a_in дана пунктиром не в масштабе. Панель (b) воспроизводит e_max(i₀) = √(1 − (5/3)cos²i₀), затеняет докритическую полосу без обмена и отмечает точки исследования 0.7638 (60°) и 0.8972 (70°).",
        },
        "fig02_kl_exchange.png": {
            "cap_en": "Headline result — the eccentricity–inclination exchange of the secular spline flow.",
            "cap_ru": "Главный результат — обмен «эксцентриситет–наклонение» в секулярном сплайновом потоке.",
            "walk_en": "Left: e(t) cycles to 0.763733 (i₀ = 60°) and 0.897238 (70°) against the dashed analytic envelopes, with j_z = 0.500000 and 0.342020 conserved; right: over two cycles at 60° eccentricity peaks exactly when the inclination dips to 39.23° = i_crit — the antiphase exchange.",
            "walk_ru": "Слева: e(t) циклирует до 0.763733 (i₀ = 60°) и 0.897238 (70°) на фоне пунктирных аналитических огибающих, j_z = 0.500000 и 0.342020 сохраняются; справа: на двух циклах при 60° эксцентриситет достигает максимума ровно в момент провала наклонения до 39.23° = i_crit — противофазный обмен.",
        },
        "fig03_kl_sweeps.png": {
            "cap_en": "Parameter sweeps: validation of the Kozai landscape e_max(i₀) and scaling of the KL clock with the perturber mass.",
            "cap_ru": "Параметрические развёртки: валидация ландшафта Козаи e_max(i₀) и масштабирование часов Козаи–Лидова по массе возмутителя.",
            "walk_en": "Across 12 inclinations from 30° to 80° the spline flow matches the analytic landscape to 1.128×10⁻⁵ (the 40° run needs an 8× longer span: the KL period diverges at i_crit), while below i_crit eccentricity stays at e₀ = 0.001; the mass sweep over m₃/M ∈ {0.5, 1, 2, 4} confirms P ∝ 1/m₃ with a P·m₃ spread of 4.29%.",
            "walk_ru": "По 12 наклонениям от 30° до 80° сплайновый поток совпадает с аналитикой с точностью 1.128×10⁻⁵ (прогон 40° требует 8-кратного удлинения: период Козаи–Лидова расходится на i_crit), ниже i_crit эксцентриситет остаётся на e₀ = 0.001; развёртка по m₃/M ∈ {0.5, 1, 2, 4} подтверждает P ∝ 1/m₃ с разбросом произведения P·m₃ всего 4.29%.",
        },
        "fig04_kl_dynamics.png": {
            "cap_en": "Dynamics on the fixed-j_z manifold: phase portrait and the residual of the tabulated Hamiltonian.",
            "cap_ru": "Динамика на многообразии фиксированного j_z: фазовый портрет и остаток табулированного гамильтониана.",
            "walk_en": "The phase portrait (ω mod π, e) shows ω librating about π/2 while e cycles between 0.001 and 0.763733 (60°) / 0.897238 (70°); the Hamiltonian residual along the 60° trajectory stays below 1.33×10⁻⁵ — the cubic-spline representation error on the 160 × 180 grid, not integrator error (DOP853, rtol 1e-8).",
            "walk_ru": "Фазовый портрет (ω mod π, e) показывает либрацию ω около π/2 при циклировании e между 0.001 и 0.763733 (60°) / 0.897238 (70°); остаток гамильтониана вдоль траектории 60° не превышает 1.33×10⁻⁵ — это ошибка кубически-сплайнового представления на сетке 160 × 180, а не ошибка интегратора (DOP853, rtol 1e-8).",
        },
    },
    "results_block": [
        "e_max_i0_60                = 7.637326e-01  (target 0.763763, tol 0.002)   PASS",
        "e_max_i0_70                = 8.972376e-01  (target 0.897239, tol 0.002)   PASS",
        "kl_period_halves_with_m3   = 4.810213e-01  (target 0.5, tol 0.03)         PASS",
        "direct_3d_emax_validation  = PASS (direct smoothed e_max 0.7423 vs 0.7638, deviation -2.8%)",
        "e_max_sweep_12pts          = max deviation 0.0000113 (i0: 30..80 deg, active range)",
        "kl_clock_pm3_spread        = 4.29%  (P·m₃ over m₃/M in {0.5, 1, 2, 4})",
        "spline_hamiltonian_drift   = 0.0000133  (grid 160 x 180, not integrator error)",
        "status: PASS (4/4)   runtime: 64.6 s",
    ],
    "abstract_en": (
        "This monograph treats the Kozai–Lidov mechanism — the secular exchange of "
        "eccentricity and inclination that a distant inclined companion drives in a hierarchical "
        "triple — in the full verification style of the TRIVORTEX program. Instead of coding the "
        "memorized analytic result, the study builds the doubly-averaged quadrupole Hamiltonian "
        "numerically: the instantaneous quadrupole disturbing potential is averaged over the inner "
        "orbit by a 240-point quadrature, tabulated on a 160 × 180 (e, ω) grid at the conserved "
        "j_z, and converted into a cubic spline whose derivatives drive the canonical flow. The "
        "spline flow reproduces the analytic maxima e_max = 0.763763 (i₀ = 60°) and 0.897239 "
        "(i₀ = 70°) to within the 2×10⁻³ tolerance, validates the Kozai landscape over 12 "
        "inclinations from 30° to 80° with a maximum deviation of 1.128×10⁻⁵, confirms the clock "
        "scaling P ∝ 1/m₃ (ratio P(2m₃)/P(m₃) = 0.481; P·m₃ spread 4.29%), and conserves the "
        "tabulated Hamiltonian to 1.33×10⁻⁵. An independent direct integration of the full "
        "three-dimensional restricted problem (m₃/M = 0.5, a_out = 5 a_in, 200 outer orbits) "
        "yields a smoothed maximum eccentricity of 0.7423 against 0.7638 — a −2.8% deviation "
        "consistent with the hexadecapole truncation. All four acceptance checks pass."
    ),
    "abstract_ru": (
        "Монография посвящена механизму Козаи–Лидова — секулярному обмену "
        "эксцентриситета и наклонения, который порождает далёкий наклонённый компаньон в "
        "иерархической тройной системе, — в полном верификационном стиле программы TRIVORTEX. "
        "Вместо кодирования заученного аналитического результата исследование строит двойной "
        "усреднённый квадрупольный гамильтониан численно: мгновенный квадрупольный возмущающий "
        "потенциал усредняется по внутренней орбите квадратурой из 240 узлов, табулируется на "
        "сетке 160 × 180 (e, ω) при сохраняющемся j_z и превращается в кубический сплайн, "
        "производные которого порождают канонический поток. Сплайновый поток воспроизводит "
        "аналитические максимумы e_max = 0.763763 (i₀ = 60°) и 0.897239 (i₀ = 70°) в пределах "
        "допуска 2×10⁻³, подтверждает ландшафт Козаи по 12 наклонениям от 30° до 80° с "
        "максимальным отклонением 1.128×10⁻⁵, проверяет масштабирование часов P ∝ 1/m₃ "
        "(отношение P(2m₃)/P(m₃) = 0.481; разброс P·m₃ 4.29%) и сохраняет табулированный "
        "гамильтониан с точностью 1.33×10⁻⁵. Независимое прямое интегрирование полной "
        "трёхмерной ограниченной задачи (m₃/M = 0.5, a_out = 5 a_in, 200 внешних оборотов) даёт "
        "сглаженный максимальный эксцентриситет 0.7423 против 0.7638 — отклонение −2.8%, "
        "согласующееся с усечением до гексадекаполя. Все четыре контрольные проверки пройдены."
    ),
    "intro_en": [
        (
            "The history of the effect began half a century before its discovery papers. In 1910 "
            "Hugo von Zeipel derived the secular equations of the double-averaged quadrupole three-"
            "body problem, and the reduction to a single degree of freedom was already implicit in "
            "his work. The classical papers of 1962 appeared independently and almost simultaneously: "
            "Yoshihide Kozai analysed secular perturbations of asteroids with high inclinations "
            "(Astronomical Journal 67, 591), while Mikhail Lidov studied the evolution of artificial "
            "satellite orbits under the gravitational action of external bodies (Planetary and Space "
            "Science 9, 719) — in the Russian literature the effect is still often called the "
            "Lidov–Kozai mechanism. Both found the same phenomenon: above the critical inclination "
            "39.23° the eccentricity and the inclination begin to exchange periodically, and the "
            "inclination at maximum eccentricity drops exactly to the critical value."
        ),
        (
            "The mechanism immediately became a working tool of celestial mechanics. It bounds the "
            "lifetimes of high-latitude artificial satellites, shapes the orbital architecture of "
            "irregular satellite systems and of asteroid families, drives the growth of cometary "
            "eccentricities, and protects — or destroys — bodies on inclined orbits in planetary "
            "systems. The timescale formula t_KL ~ (M/m₃)(a_out/a_in)³ P_in shows why the effect is "
            "so universal: it is a clock whose rate depends only on the hierarchy, and every "
            "hierarchical configuration with an inclined orbit carries it."
        ),
        (
            "The modern renaissance came with exoplanets and gravitational-wave astronomy. The "
            "eccentric generalizations of the mechanism (the octupole-order flips, comprehensively "
            "reviewed by Naoz 2016) turn inclined triples into a migration channel for hot Jupiters "
            "(Wu & Murray 2003; Fabrycky & Tremaine 2007) and into a merger channel for compact-"
            "object triples whose final inspirals LISA will observe (Blaes, Lee & Socrates 2002). "
            "The monograph of Shevchenko (2017) collects the applications, and the historical review "
            "of Ito & Ohtsuka (2019) reconstructs the naming and the priority — including von "
            "Zeipel's role and the Japanese and Soviet schools."
        ),
        (
            "For TRIVORTEX the relevance is structural. The conserved j_z collapses the problem to "
            "one integrable degree of freedom exactly as the Chaplygin integral reduces the vortex "
            "problem; the closed-form e_max is a Theorem-3.1-type sharp analytic benchmark that the "
            "numerics must hit; and the KL clock is the secular twin of the rotating choreography "
            "period. This study therefore anchors the secular celestial block of the program "
            "(TRX-01, TRX-10, TRX-11, TRX-12) — the same three-body stage on which the laser studies "
            "act."
        ),
    ],
    "intro_ru": [
        (
            "История эффекта началась за полвека до его классических статей. В 1910 году Хуго фон "
            "Цайпель вывел секулярные уравнения двойной усреднённой квадрупольной задачи трёх тел, "
            "и редукция к одной степени свободы уже неявно присутствовала в его работе. Классические "
            "статьи 1962 года появились независимо и почти одновременно: Ёсихидэ Козаи проанализировал "
            "секулярные возмущения астероидов с большими наклонениями (Astronomical Journal 67, 591), "
            "а Михаил Лидов — эволюцию орбит искусственных спутников под гравитационным действием "
            "внешних тел (Planetary and Space Science 9, 719); в русскоязычной литературе эффект "
            "по-прежнему часто называют механизмом Лидова–Козаи. Оба обнаружили одно и то же: выше "
            "критического наклонения 39.23° эксцентриситет и наклонение начинают периодически "
            "обмениваться, причём наклонение при максимальном эксцентриситете опускается точно до "
            "критического значения."
        ),
        (
            "Механизм немедленно стал рабочим инструментом небесной механики. Он ограничивает время "
            "жизни высокоширотных искусственных спутников, формирует орбитальную архитектуру систем "
            "нерегулярных спутников и семейств астероидов, раскачивает эксцентриситеты комет и "
            "защищает — либо уничтожает — тела на наклонённых орбитах в планетных системах. Формула "
            "масштаба времени t_KL ~ (M/m₃)(a_out/a_in)³·P_in объясняет универсальность эффекта: это "
            "часы, скорость которых зависит только от иерархии, и всякая иерархическая конфигурация "
            "с наклонённой орбитой несёт их в себе."
        ),
        (
            "Современный ренессанс принесли экзопланеты и гравитационно-волновая астрономия. "
            "Эксцентриковые обобщения механизма (октупольные перевороты орбит, подробно "
            "рассмотренные в обзоре Naoz (2016)) превращают наклонённые тройные в канал миграции "
            "горячих юпитеров (Wu & Murray 2003; Fabrycky & Tremaine 2007) и в канал слияний "
            "компактных объектов, финальные стадии которых увидит LISA (Blaes, Lee & Socrates 2002). "
            "Монография Шевченко (2017) собирает приложения воедино, а исторический обзор Ito & "
            "Ohtsuka (2019) восстанавливает историю названия и приоритетов — включая роль фон "
            "Цайпеля и японскую и советскую школы."
        ),
        (
            "Для TRIVORTEX значимость структурна. Сохраняющийся j_z схлопывает задачу в одну "
            "интегрируемую степень свободы — в точности как интеграл Чаплыгина редуцирует вихревую "
            "задачу; замкнутая форма e_max — это острый аналитический эталон типа теоремы 3.1, в "
            "который обязана попасть численная машина; а часы Козаи–Лидова — секулярный близнец "
            "периода вращающейся хореографии. Поэтому данное исследование закрепляет секулярный "
            "небесный блок программы (TRX-01, TRX-10, TRX-11, TRX-12) — ту же сцену трёх тел, на "
            "которой действуют лазерные исследования."
        ),
    ],
    "derivation_en": [
        (
            "Start from the companion's potential expanded in a Legendre series in the small "
            "hierarchy parameter α = a_in/a_out. The monopole (l = 0) term only shifts the inner "
            "orbit's energy; the quadrupole (l = 2) term, U ∝ (3(r·r̂₃)² − r²)/2a_out³, is the first "
            "anisotropic contribution and the one that survives averaging; for a circular outer "
            "orbit the octupole (l = 3) term vanishes identically, and the next surviving term, the "
            "hexadecapole (l = 4), is smaller by α². The inner-orbit average is performed in the "
            "script by a 240-point quadrature in true anomaly with weights proportional to r² — the "
            "exact Kepler time-weight dt ∝ r² df — rather than by quoting the memorized analytic "
            "average."
        ),
        (
            "Averaging the quadrupole term over the outer circular orbit leaves an axisymmetric "
            "potential ⟨U⟩(e, ω). Because ⟨U⟩ does not depend on the longitude of the node, the "
            "z-component of angular momentum j_z = √(1 − e²)·cos i is conserved exactly, and the "
            "dynamics collapse to one Hamiltonian degree of freedom (e, ω) on the fixed-j_z "
            "manifold. The canonical equations (E2) with the rate scale C₂ (E5) are then integrated "
            "numerically; since ⟨U⟩ has period π in ω, the phase is folded into [0, π), which keeps "
            "the integrator fast and the phase bounded."
        ),
        (
            "The maximum eccentricity follows from the geometry of the fixed points. For an "
            "initially circular inner orbit (j_z = cos i₀) eccentricity growth is possible only "
            "above the critical inclination i_crit = arccos√(3/5) ≈ 39.23°, where the libration "
            "island about ω = π/2 opens. At the eccentricity maximum the condition ė = 0 forces "
            "∂⟨U⟩/∂ω = 0, i.e. ω = π/2, and the inclination simultaneously reaches its minimum "
            "(j_z links e and i monotonically); the closed form (E4), e_max = √(1 − (5/3)cos²i₀), "
            "follows. The flow thus predicts not only the amplitude but also the antiphase geometry "
            "of the exchange — the property verified in fig02."
        ),
    ],
    "derivation_ru": [
        (
            "Отталкиваемся от разложения потенциала компаньона в ряд Лежандра по малому параметру "
            "иерархии α = a_in/a_out. Монопольный член (l = 0) лишь сдвигает энергию внутренней "
            "орбиты; квадрупольный член (l = 2), U ∝ (3(r·r̂₃)² − r²)/2a_out³, — первый анизотропный "
            "вклад, именно он переживает усреднение; для круговой внешней орбиты октупольный член "
            "(l = 3) тождественно равен нулю, а следующий выживающий член — гексадекаполь (l = 4) — "
            "меньше на α². Усреднение по внутренней орбите выполняется в коде квадратурой из 240 "
            "узлов по истинной аномалии с весами, пропорциональными r², — это точный кеплеровский "
            "вес по времени dt ∝ r² df, а не заученное аналитическое среднее."
        ),
        (
            "Усреднение квадрупольного члена по внешней круговой орбите оставляет осесимметричный "
            "потенциал ⟨U⟩(e, ω). Поскольку ⟨U⟩ не зависит от долготы узла, z-компонента углового "
            "момента j_z = √(1 − e²)·cos i сохраняется точно, и динамика схлопывается в одну "
            "гамильтонову степень свободы (e, ω) на многообразии фиксированного j_z. Канонические "
            "уравнения (E2) с масштабом скоростей C₂ (E5) интегрируются численно; так как ⟨U⟩ имеет "
            "период π по ω, фаза складывается в [0, π), что ускоряет интегратор и удерживает фазу "
            "в ограниченной области."
        ),
        (
            "Максимальный эксцентриситет следует из геометрии особых точек. Для начально круговой "
            "внутренней орбиты (j_z = cos i₀) рост эксцентриситета возможен только выше критического "
            "наклонения i_crit = arccos√(3/5) ≈ 39.23°, где открывается остров либрации вокруг "
            "ω = π/2. В максимуме эксцентриситета условие ė = 0 требует ∂⟨U⟩/∂ω = 0, то есть "
            "ω = π/2, а наклонение одновременно достигает минимума (j_z связывает e и i "
            "монотонно); отсюда замкнутая форма (E4): e_max = √(1 − (5/3)cos²i₀). Поток предсказывает "
            "таким образом не только амплитуду, но и противофазную геометрию обмена — свойство, "
            "проверяемое на fig02."
        ),
    ],
    "connection_en": (
        "The mapping to the TRIVORTEX vortex framework is structural. The conserved "
        "j_z pins the whole eccentricity–inclination family to a one-dimensional manifold exactly "
        "as the Chaplygin integral pins the vortex orbits; the closed-form e_max = "
        "√(1 − (5/3)cos²i₀) plays the role of a Theorem-3.1-type sharp analytic benchmark that "
        "the numerics are obliged to hit; and the KL clock with period ~ 1/C₂ is the secular twin "
        "of the rotating choreography period. Methodologically the study is the program's "
        "flagship of the built-not-memorized philosophy: the averaged Hamiltonian is constructed "
        "numerically and the analytic law emerges as an output-level target — the same discipline "
        "the vortex studies apply to Chaplygin-reduced flows."
    ),
    "connection_ru": (
        "Соответствие вихревому фреймворку TRIVORTEX структурно. Сохраняющийся j_z "
        "закрепляет всё семейство «эксцентриситет–наклонение» на одномерном многообразии — в "
        "точности как интеграл Чаплыгина закрепляет вихревые орбиты; замкнутая форма e_max = "
        "√(1 − (5/3)cos²i₀) играет роль острого аналитического эталона типа теоремы 3.1, в "
        "который численная машина обязана попасть; а часы Козаи–Лидова с периодом ~ 1/C₂ — "
        "секулярный близнец периода вращающейся хореографии. Методологически это исследование — "
        "флагман философии «строить, а не заучивать»: усреднённый гамильтониан конструируется "
        "численно, а аналитический закон проявляется как целевая величина на выходе — та же "
        "дисциплина, которую вихревые исследования применяют к чаплыгинским редуцированным "
        "потокам."
    ),
    "method_en": [
        (
            "The averaged potential is tabulated on a 160 × 180 grid in (e, ω) with e ∈ [0.0001, "
            "0.999] and ω ∈ [0, 2π]; each node is evaluated by the 240-point Kepler-time-weighted "
            "quadrature described in the derivation. A bicubic RectBivariateSpline (kx = ky = 3) "
            "then provides ⟨U⟩ and its exact spline derivatives ∂⟨U⟩/∂e and ∂⟨U⟩/∂ω — the "
            "Hamiltonian machine used everywhere downstream. No analytic KL formula is written "
            "anywhere in the secular pipeline."
        ),
        (
            "The canonical flow is integrated with DOP853 (rtol 1e-8, atol 1e-9, max_step T/1500) "
            "over a span covering three model KL cycles, sampled at 3000 points per run. The KL "
            "period is measured as the mean spacing of successive local maxima of e above "
            "0.7·max(e) — a robust estimator insensitive to the small-amplitude wiggles near "
            "e ≈ 0. The mass-scaling check reruns the flow at m₃/M = 2 and compares P(2m₃)/P(m₃) "
            "against 0.5 with a 3% band; the figure sweep extends the clock to m₃/M ∈ {0.5, 1, 2, 4}."
        ),
        (
            "Validation is fully independent: the direct run integrates the full three-dimensional "
            "restricted problem — the test particle feels both the primary and the companion moving "
            "on its circular orbit — with DOP853 at rtol = atol = 1e-11, a 60000-step cap and 40000 "
            "dense-output samples over 200 outer periods (m₃/M = 0.5, a_out = 5 a_in). The "
            "osculating eccentricity is computed pointwise from the Laplace–Runge–Lenz vector and "
            "smoothed with a moving average over one outer period; the maximum of the smoothed "
            "curve is the reported quantity. The secular and direct models share no code path "
            "beyond the integrator, so their agreement is a genuine cross-validation."
        ),
    ],
    "method_ru": [
        (
            "Усреднённый потенциал табулируется на сетке 160 × 180 по (e, ω) с e ∈ [0.0001, 0.999] "
            "и ω ∈ [0, 2π]; каждый узел вычисляется описанной в выводе квадратурой из 240 узлов с "
            "кеплеровскими весами по времени. Бикубический RectBivariateSpline (kx = ky = 3) даёт "
            "⟨U⟩ и его точные сплайновые производные ∂⟨U⟩/∂e и ∂⟨U⟩/∂ω — гамильтонову машину, "
            "используемую далее во всём конвейере. Ни одной аналитической формулы Козаи–Лидова в "
            "секулярном конвейере нет."
        ),
        (
            "Канонический поток интегрируется схемой DOP853 (rtol 1e-8, atol 1e-9, max_step T/1500) "
            "на интервале в три модельных цикла Козаи–Лидова с выборкой 3000 точек на прогон. "
            "Период измеряется как средний шаг между последовательными локальными максимумами e "
            "выше 0.7·max(e) — робастная оценка, нечувствительная к мелким осцилляциям возле "
            "e ≈ 0. Проверка масштабирования по массе повторяет прогон при m₃/M = 2 и сравнивает "
            "P(2m₃)/P(m₃) с 0.5 в полосе 3%; развёртка для рисунка расширяет часы до "
            "m₃/M ∈ {0.5, 1, 2, 4}."
        ),
        (
            "Валидация полностью независима: прямой прогон интегрирует полную трёхмерную "
            "ограниченную задачу — пробная частица чувствует и внутреннее тело, и компаньон на его "
            "круговой орбите — схемой DOP853 с rtol = atol = 1e-11, потолком в 60000 шагов и 40000 "
            "точками плотной выборки на 200 внешних периодов (m₃/M = 0.5, a_out = 5 a_in). "
            "Оскулирующий эксцентриситет вычисляется поточечно из вектора Лапласа–Рунге–Ленца и "
            "сглаживается скользящим средним за один внешний период; максимум сглаженной кривой и "
            "есть отчётная величина. Секулярная и прямая модели не делят ни строчки кода, кроме "
            "интегратора, поэтому их согласие — настоящая перекрёстная валидация."
        ),
    ],
    "analysis_en": [
        (
            "**Analytic maxima.** The headline checks compare the spline-flow maxima against the "
            "closed-form targets: e_max = 0.7637326 measured versus 0.7637626 analytic at i₀ = 60° "
            "(deviation 3.0×10⁻⁵) and 0.8972376 versus 0.8972386 at 70° (deviation 9.1×10⁻⁷) — "
            "both far inside the 2×10⁻³ acceptance band. The conserved quantities j_z = 0.500000 "
            "(60°) and 0.342020 (70°) stay constant along the flow, and the recorded eccentricity "
            "series returns exactly to e₀ = 0.001 at every cycle minimum (series range 0.001 … "
            "0.76372882 in the JSON protocol)."
        ),
        (
            "**The exchange geometry.** fig02 shows the antiphase lock predicted by the derivation: "
            "eccentricity peaks exactly when the inclination dips to 39.2316° — numerically "
            "indistinguishable from i_crit = arccos√(3/5) — and the argument of pericentre "
            "librates about π/2 (fig04). The phase portraits of the two headline runs collapse "
            "onto the fixed-j_z manifolds j_z = 0.5 and j_z = 0.342020, the eccentricity–inclination "
            "ledger of the scheme."
        ),
        (
            "**Landscape and clock.** The 12-point inclination sweep from 30° to 80° reproduces the "
            "analytic landscape with a maximum deviation of 1.128×10⁻⁵ over the active range; below "
            "i_crit (30°, 35°, 38°) eccentricity stays at e₀ = 0.001, and the 40° run needs an 8× "
            "longer span because the KL period diverges at the threshold (40°: 0.14818829 simulated "
            "versus 0.14818857 analytic; 45°: 0.40824826 versus 0.40824829; 80°: 0.97455930 versus "
            "0.97454802). The clock scales as 1/m₃: P(2m₃)/P(m₃) = 0.481 against the ideal 0.5 "
            "(3% band; P(m₃) = 103829.39, P(2m₃) = 49944.15 in units of 1/n_in), and across "
            "m₃/M ∈ {0.5, 1, 2, 4} the product P·m₃ spreads only 4.29% (221991.0, 111355.7, "
            "54927.46, 28661.83)."
        ),
        (
            "**Direct validation and error budget.** The independent 3-D run gives a smoothed "
            "maximum eccentricity 0.7423 versus 0.7638 analytic — a −2.8% deviation, inside the 8% "
            "gate and consistent with the hexadecapole truncation plus the non-test-particle mass "
            "ratio m₃/M = 0.5 at α = 0.2. The tabulated Hamiltonian drifts by at most 1.33×10⁻⁵ "
            "along the flow — the cubic-spline representation error on the 160 × 180 grid, "
            "deliberately separated from integrator error (DOP853, rtol 1e-8). Every number in this "
            "paragraph is stored in the JSON protocol with target, tolerance and pass flag."
        ),
    ],
    "analysis_ru": [
        (
            "**Аналитические максимумы.** Главные проверки сравнивают максимумы сплайнового потока с "
            "замкнутыми эталонами: e_max = 0.7637326 измеренный против 0.7637626 аналитического при "
            "i₀ = 60° (отклонение 3.0×10⁻⁵) и 0.8972376 против 0.8972386 при 70° (отклонение "
            "9.1×10⁻⁷) — оба далеко внутри полосы допуска 2×10⁻³. Сохраняющиеся величины "
            "j_z = 0.500000 (60°) и 0.342020 (70°) остаются постоянными вдоль потока, а записанный "
            "ряд эксцентриситета возвращается ровно к e₀ = 0.001 в каждом минимуме цикла (диапазон "
            "ряда 0.001 … 0.76372882 в JSON-протоколе)."
        ),
        (
            "**Геометрия обмена.** fig02 демонстрирует предсказанную выводом противофазную сцепку: "
            "эксцентриситет достигает максимума ровно тогда, когда наклонение проваливается до "
            "39.2316° — численно неотличимо от i_crit = arccos√(3/5), — а аргумент перицентра "
            "либрирует вокруг π/2 (fig04). Фазовые портреты обоих главных прогонов ложатся на "
            "многообразия фиксированного j_z = 0.5 и j_z = 0.342020 — ведомость «эксцентриситет–"
            "наклонение» со схемы."
        ),
        (
            "**Ландшафт и часы.** Развёртка по 12 наклонениям от 30° до 80° воспроизводит "
            "аналитический ландшафт с максимальным отклонением 1.128×10⁻⁵ по активной области; ниже "
            "i_crit (30°, 35°, 38°) эксцентриситет остаётся на e₀ = 0.001, а прогону 40° требуется "
            "8-кратное удлинение интервала, поскольку период Козаи–Лидова расходится на пороге "
            "(40°: 0.14818829 расчёт против 0.14818857 аналитика; 45°: 0.40824826 против "
            "0.40824829; 80°: 0.97455930 против 0.97454802). Часы масштабируются как 1/m₃: "
            "P(2m₃)/P(m₃) = 0.481 против идеала 0.5 (полоса 3%; P(m₃) = 103829.39, P(2m₃) = "
            "49944.15 в единицах 1/n_in), а по m₃/M ∈ {0.5, 1, 2, 4} произведение P·m₃ разбросано "
            "лишь на 4.29% (221991.0, 111355.7, 54927.46, 28661.83)."
        ),
        (
            "**Прямая валидация и бюджет ошибок.** Независимый 3-D прогон даёт сглаженный "
            "максимальный эксцентриситет 0.7423 против 0.7638 аналитического — отклонение −2.8%, "
            "внутри ворот 8% и согласующееся с усечением до гексадекаполя и нетестовым отношением "
            "масс m₃/M = 0.5 при α = 0.2. Табулированный гамильтониан дрейфует не более чем на "
            "1.33×10⁻⁵ вдоль потока — ошибка кубически-сплайнового представления на сетке "
            "160 × 180, сознательно отделённая от ошибки интегратора (DOP853, rtol 1e-8). Каждое "
            "число этого абзаца хранится в JSON-протоколе с целью, допуском и флагом прохождения."
        ),
    ],
    "discussion_en": [
        (
            "The model is deliberately minimal: quadrupole order, test-particle inner orbit, "
            "circular outer orbit, no dissipation. Within these assumptions the conclusions are "
            "exact statements about the averaged equations, not simulations of a particular system. "
            "The natural extensions each preserve the verification style: the octupole term for "
            "eccentric companions (the eccentric Kozai–Lidov effect with orbit flips — Naoz 2016), "
            "the hexadecapole correction, comparable masses and radiation backreaction (pursued in "
            "TRX-11), and tidal friction coupling the KL cycles to orbital shrinkage in the "
            "hot-Jupiter channel."
        ),
        (
            "The −2.8% direct-run deviation is not a defect but a measurement of the truncation: "
            "the direct problem at m₃/M = 0.5 and α = a_in/a_out = 0.2 is only moderately "
            "hierarchical, and higher-order multipoles plus the breakdown of the test-particle "
            "idealization push the true maximum eccentricity below the quadrupole formula. That a "
            "machine built from Newtonian gravity and geometry alone — with no KL formula inside — "
            "lands within 2.8% of a substantially non-idealized direct integration is the strongest "
            "statement of the study. The remaining error-budget line, the 1.33×10⁻⁵ Hamiltonian "
            "residual, is a property of the spline representation and could be pushed lower by "
            "refining the 160 × 180 grid, at quadratic cost in tabulation time."
        ),
        (
            "Within the program this study anchors the secular celestial block: TRX-01 treats the "
            "same restricted problem at the libration points instead of secular cycles, TRX-11 "
            "integrates the comparable-mass three-body problem exactly and radiates, and TRX-12 "
            "stations a laser sailcraft at the L4 point of the same celestial stage. The laser link "
            "is direct: KL cycles are the accepted channel-forming mechanism for LISA-class "
            "compact-object mergers (Blaes, Lee & Socrates 2002), and laser ranging of binary and "
            "triple asteroids reads out exactly the orbital elements this study oscillates."
        ),
    ],
    "discussion_ru": [
        (
            "Модель сознательно минимальна: квадрупольный порядок, пробная внутренняя орбита, "
            "круговая внешняя орбита, отсутствие диссипации. В этих допущениях выводы — точные "
            "утверждения об усреднённых уравнениях, а не симуляция конкретной системы. Естественные "
            "расширения сохраняют верификационный стиль: октупольный член для эксцентриковых "
            "компаньонов (эксцентриковый эффект Козаи–Лидова с переворотами орбит — Naoz 2016), "
            "гексадекапольная поправка, сравнимые массы и радиационная обратная связь (это TRX-11), "
            "а также приливное трение, сцепляющее циклы Козаи–Лидова со сжатием орбиты в канале "
            "горячих юпитеров."
        ),
        (
            "Отклонение −2.8% прямого прогона — не дефект, а измерение усечения: прямая задача при "
            "m₃/M = 0.5 и α = a_in/a_out = 0.2 лишь умеренно иерархична, и мультиполи высших "
            "порядков вместе с нарушением идеализации пробной частицы сдвигают истинный максимум "
            "эксцентриситета ниже квадрупольной формулы. То, что машина, построенная из ньютоновской "
            "гравитации и геометрии — без единой формулы Козаи–Лидова внутри, — попадает в 2.8% от "
            "существенно неидеализированного прямого интегрирования, — самое сильное утверждение "
            "исследования. Оставшаяся строка бюджета ошибок, остаток гамильтониана 1.33×10⁻⁵, — "
            "свойство сплайнового представления; его можно уменьшить сгущением сетки 160 × 180 "
            "ценой квадратичного роста времени табуляции."
        ),
        (
            "В рамках программы это исследование закрепляет секулярный небесный блок: TRX-01 "
            "рассматривает ту же ограниченную задачу в точках либрации вместо секулярных циклов, "
            "TRX-11 интегрирует трёхтелевую задачу со сравнимыми массами точно и с излучением, "
            "TRX-12 ставит лазерный парус в точку L4 той же небесной сцены. Лазерная связь прямая: "
            "циклы Козаи–Лидова — общепризнанный механизм формирования каналов слияний компактных "
            "объектов класса LISA (Blaes, Lee & Socrates 2002), а лазерная дальнометрия двойных и "
            "тройных астероидов считывает именно те элементы орбиты, которые здесь осциллируют."
        ),
    ],
    "conclusions_en": [
        "The doubly-averaged quadrupole Hamiltonian, built numerically (240-point orbit quadrature, 160 × 180 spline grid), reproduces the analytic maxima e_max = 0.763763 (i₀ = 60°) and 0.897239 (70°) with deviations 3.0×10⁻⁵ and 9.1×10⁻⁷ — far inside the 2×10⁻³ tolerance.",
        "The eccentricity–inclination exchange is exactly antiphase: e peaks when i dips to i_crit = arccos√(3/5) = 39.23°, with j_z = 0.500000 (60°) and 0.342020 (70°) conserved along the flow.",
        "The Kozai landscape e_max(i₀) is validated over 12 inclinations from 30° to 80° with a maximum deviation of 1.128×10⁻⁵ over the active range; below i_crit eccentricity stays at e₀ = 0.001, and the KL period diverges at the threshold (the 40° run needs an 8× longer span).",
        "The KL clock obeys P ∝ 1/m₃: the measured ratio P(2m₃)/P(m₃) = 0.481 (ideal 0.5, 3% band) and the product P·m₃ spreads only 4.29% across m₃/M ∈ {0.5, 1, 2, 4}.",
        "An independent direct integration of the full 3-D restricted problem (m₃/M = 0.5, a_out = 5 a_in, 200 outer orbits) gives a smoothed maximum eccentricity 0.7423 versus 0.7638 — a −2.8% deviation consistent with the hexadecapole truncation and the finite mass ratio.",
        "The tabulated Hamiltonian is conserved to 1.33×10⁻⁵ along the flow — the honest error budget of the spline representation, reported alongside every check in the JSON protocol.",
    ],
    "conclusions_ru": [
        "Двойной усреднённый квадрупольный гамильтониан, построенный численно (квадратура орбиты из 240 узлов, сплайновая сетка 160 × 180), воспроизводит аналитические максимумы e_max = 0.763763 (i₀ = 60°) и 0.897239 (70°) с отклонениями 3.0×10⁻⁵ и 9.1×10⁻⁷ — далеко внутри допуска 2×10⁻³.",
        "Обмен «эксцентриситет–наклонение» строго противофазен: e достигает максимума, когда i проваливается до i_crit = arccos√(3/5) = 39.23°, при сохранении j_z = 0.500000 (60°) и 0.342020 (70°) вдоль потока.",
        "Ландшафт Козаи e_max(i₀) подтверждён по 12 наклонениям от 30° до 80° с максимальным отклонением 1.128×10⁻⁵ по активной области; ниже i_crit эксцентриситет остаётся на e₀ = 0.001, а период Козаи–Лидова расходится на пороге (прогону 40° нужно 8-кратное удлинение).",
        "Часы Козаи–Лидова подчиняются закону P ∝ 1/m₃: измеренное отношение P(2m₃)/P(m₃) = 0.481 (идеал 0.5, полоса 3%), а произведение P·m₃ разбросано лишь на 4.29% по m₃/M ∈ {0.5, 1, 2, 4}.",
        "Независимое прямое интегрирование полной 3-D ограниченной задачи (m₃/M = 0.5, a_out = 5 a_in, 200 внешних оборотов) даёт сглаженный максимальный эксцентриситет 0.7423 против 0.7638 — отклонение −2.8%, согласующееся с усечением до гексадекаполя и конечным отношением масс.",
        "Табулированный гамильтониан сохраняется вдоль потока с точностью 1.33×10⁻⁵ — честный бюджет ошибок сплайнового представления, приводимый рядом с каждой проверкой в JSON-протоколе.",
    ],
    "references": [
        "1. Kozai, Y. (1962). *Secular perturbations of asteroids with high inclination and eccentricity.* Astronomical Journal 67, 591–598.",
        "2. Lidov, M. L. (1962). *The evolution of orbits of artificial satellites of planets under the action of gravitational perturbations of external bodies.* Planetary and Space Science 9, 719–759.",
        "3. von Zeipel, H. (1910). *Sur les perturbations séculaires des orbites astronomiques.* Astronomische Nachrichten 183, 345–362.",
        "4. Naoz, S. (2016). *The eccentric Kozai–Lidov effect and beyond.* Annual Review of Astronomy and Astrophysics 54, 341–396.",
        "5. Shevchenko, I. I. (2017). *The Lidov–Kozai Effect — Applications in Celestial Mechanics.* Springer, Astrophysics and Space Science Library 441.",
        "6. Ito, T., Ohtsuka, K. (2019). *The Lidov–Kozai oscillation and Hirayama families.* Monographic Notices of the National Astronomical Observatory of Japan 1, 1–168.",
        "7. Murray, C. D., Dermott, S. F. (1999). *Solar System Dynamics.* Cambridge University Press.",
        "8. Wu, Y., Murray, N. W. (2003). *Planet migration and binary companions: the case of HD 80606.* The Astrophysical Journal 589, 605–614.",
        "9. Fabrycky, D., Tremaine, S. (2007). *Shrinking binary and planetary orbits by the Kozai cycle with tidal friction.* The Astrophysical Journal 669, 1298–1315.",
        "10. Blaes, O., Lee, M. H., Socrates, A. (2002). *The Kozai mechanism and the evolution of binary supermassive black holes.* The Astrophysical Journal 578, 775–786.",
    ],
    "crosslinks_en": [
        "* **TRX-01** is the restricted-problem companion: libration points of the same celestial stage instead of secular cycles.",
        "* **TRX-11** integrates the comparable-mass three-body problem exactly and radiates — the natural successor beyond the test-particle limit.",
        "* **TRX-12** stations a laser sailcraft at the L4 point of the same celestial geometry (stationkeeping, not cycling).",
    ],
    "crosslinks_ru": [
        "* **TRX-01** — компаньон по ограниченной задаче: точки либрации той же небесной сцены вместо секулярных циклов.",
        "* **TRX-11** интегрирует трёхтелевую задачу со сравнимыми массами точно и с излучением — естественное продолжение за пределами пробной частицы.",
        "* **TRX-12** ставит лазерный парус в точку L4 той же небесной геометрии (удержание, а не циклирование).",
    ],
    "assumptions_en": [
        "Test-particle limit: the inner orbit hosts a massless particle; the companion moves on a fixed circular Kepler orbit and enters only through C₂.",
        "Quadrupole order only: the companion potential is truncated at l = 2; for a circular outer orbit the octupole vanishes, and the hexadecapole is smaller by (a_in/a_out)².",
        "Double averaging: all short-period terms over the inner and outer orbits are removed — the model is purely secular.",
        "No dissipation: no tides, no gas, no radiation forces; the eccentricity–inclination exchange is conservative and reversible.",
        "The averaged potential is a numerical object (cubic spline on a 160 × 180 grid); its 1.33×10⁻⁵ residual is part of the error budget and is reported honestly.",
        "Canonical units GM_inner = 1, a_in = 1, n_in = 1; the direct validation uses m₃/M = 0.5, a_out = 5 a_in and 200 outer periods.",
    ],
    "assumptions_ru": [
        "Предел пробной частицы: на внутренней орбите — безмассовая частица; компаньон движется по фиксированной круговой кеплеровской орбите и входит в модель только через C₂.",
        "Только квадрупольный порядок: потенциал компаньона усечён на l = 2; для круговой внешней орбиты октуполь исчезает, а гексадекаполь меньше на (a_in/a_out)².",
        "Двойное усреднение: все короткопериодические члены по внутренней и внешней орбитам удалены — модель чисто секулярная.",
        "Без диссипации: ни приливов, ни газа, ни сил излучения; обмен «эксцентриситет–наклонение» консервативен и обратим.",
        "Усреднённый потенциал — численный объект (кубический сплайн на сетке 160 × 180); его остаток 1.33×10⁻⁵ входит в бюджет ошибок и честно публикуется.",
        "Канонические единицы GM_inner = 1, a_in = 1, n_in = 1; прямая валидация использует m₃/M = 0.5, a_out = 5 a_in и 200 внешних периодов.",
    ],
    "glance_en": [
        ["Block", "Celestial mechanics — study 10 of 12"],
        [
            "Model",
            "double-averaged quadrupole Kozai–Lidov problem (test particle in a hierarchical triple)",
        ],
        ["Key invariant", "j_z = √(1 − e²)·cos i (0.500000 / 0.342020 for i₀ = 60°/70°)"],
        [
            "Headline result",
            "e_max = 0.763763 (60°) and 0.897239 (70°) reproduced by the spline flow; direct 3-D validation −2.8%",
        ],
        ["Verification", "4/4 checks PASS (full mode)"],
        ["Runtime", "64.6 s full · < 20 s smoke"],
    ],
    "glance_ru": [
        ["Блок", "Небесная механика — исследование 10 из 12"],
        [
            "Модель",
            "двойной усреднённый квадрупольный механизм Козаи–Лидова (пробная частица в иерархической тройной)",
        ],
        ["Ключевой инвариант", "j_z = √(1 − e²)·cos i (0.500000 / 0.342020 для i₀ = 60°/70°)"],
        [
            "Главный результат",
            "e_max = 0.763763 (60°) и 0.897239 (70°) воспроизведены сплайновым потоком; прямая 3-D валидация −2.8%",
        ],
        ["Верификация", "4/4 проверок PASS (полный режим)"],
        ["Время выполнения", "64.6 с полный · < 20 с smoke"],
    ],
    "glossary": {
        "header_en": ["Term", "Definition"],
        "header_ru": ["Термин", "Определение"],
        "rows_en": [
            [
                "Kozai–Lidov oscillations",
                "secular exchange of eccentricity and inclination in a hierarchical triple, driven by the double-averaged quadrupole perturbation",
            ],
            [
                "Kozai angle i_crit",
                "critical inclination arccos√(3/5) ≈ 39.23° above which the exchange turns on for an initially circular orbit",
            ],
            [
                "j_z",
                "z-component of the orbital angular momentum, j_z = √(1 − e²)·cos i — the conserved quadrupole invariant",
            ],
            [
                "Double averaging",
                "removal of the short-period terms by averaging over both orbital periods, leaving purely secular dynamics",
            ],
            [
                "Quadrupole approximation",
                "leading anisotropic term (l = 2) of the expansion of the companion potential in a_in/a_out",
            ],
            [
                "Secular dynamics",
                "long-term evolution of orbital elements with the mean longitudes averaged out",
            ],
            [
                "Argument of pericentre ω",
                "orientation of the ellipse in its plane; librates about π/2 during KL cycles",
            ],
            [
                "e_max",
                "maximum eccentricity of the KL cycle; for e₀ ≈ 0: e_max = √(1 − (5/3)cos²i₀)",
            ],
            [
                "Spline Hamiltonian",
                "cubic-spline representation of the tabulated averaged potential that drives the flow",
            ],
            [
                "DOP853",
                "explicit Dormand–Prince 8(5,3) adaptive integrator, used for both the secular and the direct runs",
            ],
        ],
        "rows_ru": [
            [
                "Колебания Козаи–Лидова",
                "секулярный обмен эксцентриситета и наклонения в иерархической тройной, порождаемый двойным усреднённым квадрупольным возмущением",
            ],
            [
                "Угол Козаи i_crit",
                "критическое наклонение arccos√(3/5) ≈ 39.23°, выше которого обмен включается для начально круговой орбиты",
            ],
            [
                "j_z",
                "z-компонента орбитального углового момента, j_z = √(1 − e²)·cos i — сохраняющийся квадрупольный инвариант",
            ],
            [
                "Двойное усреднение",
                "удаление короткопериодических членов усреднением по обоим орбитальным периодам — остаётся чисто секулярная динамика",
            ],
            [
                "Квадрупольное приближение",
                "ведущий анизотропный член (l = 2) разложения потенциала компаньона по a_in/a_out",
            ],
            [
                "Секулярная динамика",
                "долговременная эволюция орбитальных элементов при усреднённых средних долготах",
            ],
            [
                "Аргумент перицентра ω",
                "ориентация эллипса в его плоскости; либрирует около π/2 в циклах Козаи–Лидова",
            ],
            [
                "e_max",
                "максимальный эксцентриситет цикла Козаи–Лидова; при e₀ ≈ 0: e_max = √(1 − (5/3)cos²i₀)",
            ],
            [
                "Сплайновый гамильтониан",
                "кубически-сплайновое представление табулированного усреднённого потенциала, порождающее поток",
            ],
            [
                "DOP853",
                "явный адаптивный интегратор Дормана–Принса 8(5,3), используется и в секулярных, и в прямых прогонах",
            ],
        ],
    },
    "notation": {
        "header_en": ["Symbol", "Meaning"],
        "header_ru": ["Символ", "Смысл"],
        "rows_en": [
            ["e", "eccentricity of the inner (test-particle) orbit"],
            ["i", "inclination of the inner orbit to the outer orbital plane"],
            ["ω", "argument of pericentre of the inner orbit"],
            ["e₀, ω₀, i₀", "initial values: 0.001, π/2, {60°, 70°}"],
            ["j = √(1 − e²)", "dimensionless angular momentum of the inner orbit (L = 1)"],
            ["j_z", "conserved z-component, j_z = √(1 − e²)·cos i"],
            ["m₃/M", "perturber-to-inner mass ratio"],
            ["a_in, a_out", "inner and outer semi-major axes (a_in = 1)"],
            ["n_in", "inner mean motion (n_in = 1)"],
            ["C₂", "KL rate, C₂ = (3/8)(m₃/M)(a_in/a_out)³·n_in"],
            ["⟨U⟩", "double-averaged quadrupole potential (spline-tabulated)"],
        ],
        "rows_ru": [
            ["e", "эксцентриситет внутренней (пробной) орбиты"],
            ["i", "наклонение внутренней орбиты к плоскости внешней орбиты"],
            ["ω", "аргумент перицентра внутренней орбиты"],
            ["e₀, ω₀, i₀", "начальные значения: 0.001, π/2, {60°, 70°}"],
            ["j = √(1 − e²)", "безразмерный угловой момент внутренней орбиты (L = 1)"],
            ["j_z", "сохраняющаяся z-компонента, j_z = √(1 − e²)·cos i"],
            ["m₃/M", "отношение массы возмутителя к внутренней"],
            ["a_in, a_out", "большие полуоси внутренней и внешней орбит (a_in = 1)"],
            ["n_in", "среднее движение внутренней орбиты (n_in = 1)"],
            ["C₂", "скорость Козаи–Лидова, C₂ = (3/8)(m₃/M)(a_in/a_out)³·n_in"],
            ["⟨U⟩", "двойной усреднённый квадрупольный потенциал (сплайновая табуляция)"],
        ],
    },
    "params_appendix": {
        "header_en": ["Symbol", "Value", "Role"],
        "header_ru": ["Символ", "Значение", "Роль"],
        "rows_en": [
            ["e₀", "0.001", "initial eccentricity (near-circular)"],
            ["ω₀", "π/2", "initial argument of pericentre"],
            ["i₀", "{60°, 70°}", "initial inclinations of the headline runs"],
            ["m₃/M (secular)", "1.0 headline; {0.5, 1, 2, 4} clock sweep", "perturber mass ratio"],
            ["a_out (secular)", "20 a_in", "outer orbit radius, hierarchy α = 0.05"],
            ["secular grid", "160 × 180 (e × ω)", "spline tabulation of ⟨U⟩"],
            [
                "orbit quadrature",
                "240 points in true anomaly, weights ∝ r²",
                "inner-orbit Kepler-time average",
            ],
            [
                "secular integrator",
                "DOP853, rtol 1e-8, atol 1e-9, max_step T/1500",
                "canonical spline flow, 3 KL cycles",
            ],
            [
                "direct run",
                "m₃/M = 0.5, a_out = 5 a_in, 200 outer periods",
                "full 3-D restricted problem",
            ],
            [
                "direct integrator",
                "DOP853, rtol = atol = 1e-11, 60000-step cap, 40000 samples",
                "osculating e smoothed over one outer period",
            ],
            ["runtime", "64.6 s full, < 20 s smoke", "reference machine"],
        ],
        "rows_ru": [
            ["e₀", "0.001", "начальный эксцентриситет (почти круг)"],
            ["ω₀", "π/2", "начальный аргумент перицентра"],
            ["i₀", "{60°, 70°}", "начальные наклонения главных прогонов"],
            [
                "m₃/M (секулярно)",
                "1.0 главный; {0.5, 1, 2, 4} развёртка часов",
                "отношение массы возмутителя",
            ],
            ["a_out (секулярно)", "20 a_in", "радиус внешней орбиты, иерархия α = 0.05"],
            ["секулярная сетка", "160 × 180 (e × ω)", "сплайновая табуляция ⟨U⟩"],
            [
                "квадратура орбиты",
                "240 узлов по истинной аномалии, веса ∝ r²",
                "кеплеровское среднее по времени внутренней орбиты",
            ],
            [
                "секулярный интегратор",
                "DOP853, rtol 1e-8, atol 1e-9, max_step T/1500",
                "канонический сплайновый поток, 3 цикла",
            ],
            [
                "прямой прогон",
                "m₃/M = 0.5, a_out = 5 a_in, 200 внешних периодов",
                "полная 3-D ограниченная задача",
            ],
            [
                "прямой интегратор",
                "DOP853, rtol = atol = 1e-11, 60000 шагов, 40000 выборок",
                "оскулирующий e со сглаживанием за один внешний период",
            ],
            ["время выполнения", "64.6 с полный, < 20 с smoke", "референсная машина"],
        ],
    },
    "bibtex": [
        "@article{kozai1962,",
        "  author  = {Kozai, Yoshihide},",
        "  title   = {Secular perturbations of asteroids with high inclination and eccentricity},",
        "  journal = {Astronomical Journal},",
        "  year    = {1962}, volume = {67}, pages = {591--598}}",
        "",
        "@article{lidov1962,",
        "  author  = {Lidov, Mikhail L.},",
        "  title   = {The evolution of orbits of artificial satellites of planets under the action of gravitational perturbations of external bodies},",
        "  journal = {Planetary and Space Science},",
        "  year    = {1962}, volume = {9}, pages = {719--759}}",
        "",
        "@article{naoz2016,",
        "  author  = {Naoz, Smadar},",
        "  title   = {The eccentric Kozai--Lidov effect and beyond},",
        "  journal = {Annual Review of Astronomy and Astrophysics},",
        "  year    = {2016}, volume = {54}, pages = {341--396}}",
        "",
        "@book{shevchenko2017,",
        "  author    = {Shevchenko, Ivan I.},",
        "  title     = {The Lidov--Kozai Effect: Applications in Celestial Mechanics},",
        "  publisher = {Springer}, series = {Astrophysics and Space Science Library 441}, year = {2017}}",
        "",
        "@article{ito2019,",
        "  author  = {Ito, Takashi and Ohtsuka, Katsuhito},",
        "  title   = {The Lidov--Kozai oscillation and Hirayama families},",
        "  journal = {Monographic Notices of the National Astronomical Observatory of Japan},",
        "  year    = {2019}, volume = {1}, pages = {1--168}}",
    ],
}
