# -*- coding: utf-8 -*-
"""Content pack for TRX-01 (v1.0.0 Monograph Edition). Rendered by scripts/build_study_docs.py."""

PACK = {
    "meta": {
        "study_id": "TRX-01",
        "dir_name": "TRX-01-laser-radiation-pressure",
        "title_en": "Radiation-Pressure Restricted Three-Body Problem (Laser on Dust)",
        "title_ru": "Фотогравитационная ограниченная задача трёх тел (лазер на пылевую частицу)",
        "script": "trx01_laser_radiation_pressure.py",
        "results_json": "trx01_results.json",
        "scheme_file": "scheme_trx01.svg",
        "runtime_full": "0.10 s",
    },
    "essence_en": (
        "The circular restricted three-body problem (CR3BP) in which primary 1 is "
        "illuminated by an intense laser beam. Photon radiation pressure reduces the effective "
        "pull of that primary on a massless particle by the factor **(1 − β)**, with "
        'β = F_rad / F_grav — the "laser-dressed" CR3BP. The laser acts as a third physical '
        "agent that reshapes the libration-point landscape without adding a mass."
    ),
    "essence_ru": (
        "Ограниченная круговая задача трёх тел (ОКЗТТ), в которой первое тело "
        "освещается мощным лазерным пучком. Давление фотонного излучения ослабляет эффективное "
        "притяжение этого тела к безмассовой частице множителем **(1 − β)**, где "
        "β = F_изл / F_грав, — «лазерно-одетая» ОКЗТТ. Лазер действует как третье физическое "
        "начало, перестраивающее ландшафт точек либрации без добавления массы."
    ),
    "mission_en": [
        (
            "The Lagrange points are the celestial anchor of TRIVORTEX: the equilateral points are "
            "the celestial twin of the same-sign vortex triangle, and their vortex-model counterpart "
            "is the rotating choreography of Theorem 3.1. This study asks a modern question about "
            "that classical landscape — what happens when a laser is pointed at one of the primaries? "
            "Photon pressure is weak per photon, but a laser delivers it directionally and "
            "indefinitely: dust grains, debris fragments and light sails feel a steady (1 − β) "
            "renormalization of gravity."
        ),
        (
            "The study verifies three things to machine precision: that the classical libration "
            "points are recovered at β = 0 against a published reference; that the triangular points "
            "migrate monotonically and toward the radiating primary as β grows; and that the Jacobi "
            "integral — the invariant that structures the whole problem — is conserved along an orbit "
            "near the displaced L4 to ≤ 1e-10. The result is a controlled, verifiable model of "
            '"laser-augmented" three-body dynamics, the foundation of the laser-highway application '
            "pursued in TRX-12."
        ),
    ],
    "mission_ru": [
        (
            "Точки Лагранжа — небесный якорь TRIVORTEX: равносторонние точки являются небесным "
            "близнецом одноимённого вихревого треугольника, а их аналог в вихревой модели — "
            "вращающаяся хореография теоремы 3.1. Данное исследование задаёт современный вопрос об "
            "этом классическом ландшафте: что происходит, если навести лазер на одно из массивных "
            "тел? Давление фотонов мало в расчёте на один фотон, но лазер доставляет его "
            "направленно и неограниченно долго: пылевые зёрна, фрагменты мусора и солнечные паруса "
            "испытывают стационарную перенормировку гравитации (1 − β)."
        ),
        (
            "Исследование проверяет три вещи с машинной точностью: что классические точки либрации "
            "восстанавливаются при β = 0 по опубликованному эталону; что треугольные точки "
            "мигрируют монотонно и в сторону светящегося тела при росте β; и что интеграл Якоби — "
            "инвариант, структурирующий всю задачу, — сохраняется вдоль орбиты возле смещённой L4 "
            "на уровне ≤ 1e-10. Результат — контролируемая, проверяемая модель «лазерно-усиленной» "
            "динамики трёх тел, фундамент лазерной трассы, развиваемой в TRX-12."
        ),
    ],
    "physics_en": [
        (
            "Planar CR3BP in the rotating frame. The two primaries move on circular orbits about "
            "their common barycenter; a massless particle responds to their gravity and to the "
            "radiation field of primary 1. In the rotating frame the particle is described by two "
            "coordinates and two velocities, and the entire stationkeeping problem reduces to the "
            "topography of one scalar function — the effective potential Ω."
        ),
        (
            "The radiation field enters through a single dimensionless coefficient. Photon momentum "
            "flux from the laser adds an outward force on illuminated particles that scales exactly "
            "like gravity in 1/r², so its only effect on the CR3BP structure is the renormalization "
            "(1 − β) of the gravitational parameter of primary 1. All geometry of the libration "
            "landscape is then controlled by the pair (μ, β)."
        ),
    ],
    "physics_ru": [
        (
            "Плоская ОКЗТТ во вращающейся системе отсчёта. Два массивных тела движутся по круговым "
            "орбитам вокруг общего барицентра; безмассовая частица откликается на их гравитацию и "
            "на поле излучения первого тела. Во вращающейся системе частица описывается двумя "
            "координатами и двумя скоростями, а вся задача удержания сводится к топографии одной "
            "скалярной функции — эффективного потенциала Ω."
        ),
        (
            "Поле излучения входит через один безразмерный коэффициент. Поток импульса фотонов "
            "лазера создаёт выталкивающую силу, масштабирующуюся в точности как гравитация по "
            "закону 1/r², поэтому единственный эффект на структуру ОКЗТТ — перенормировка (1 − β) "
            "гравитационного параметра первого тела. Вся геометрия ландшафта либрации управляется "
            "парой (μ, β)."
        ),
    ],
    "preset_table": {
        "header_en": ["Parameter", "Value", "Meaning"],
        "header_ru": ["Параметр", "Значение", "Смысл"],
        "rows_en": [
            ["μ", "0.0121505856", "Earth–Moon mass parameter"],
            ["β", "{0, 0.01, 0.05, 0.1}", "radiation coefficient of primary 1"],
            ["m₁, m₂", "1 − μ, μ", "primaries at (−μ, 0) and (1 − μ, 0)"],
            ["λ, D, Δ", "1 µm, 1 m, 1 AU", "diffraction-limited beam: waist w ≈ 1.82e5 m"],
            ["grain", "ρ = 3000 kg/m³, R = 1 µm, Q_pr = 1.3", "silicate dust test particle"],
            ["laser power", "10 kW … 10 MW", "gives β ≈ 1.7e-11 … 1.7e-8 at 1 AU (honest table)"],
        ],
        "rows_ru": [
            ["μ", "0.0121505856", "массовый параметр Земля–Луна"],
            ["β", "{0, 0.01, 0.05, 0.1}", "коэффициент излучения первого тела"],
            ["m₁, m₂", "1 − μ, μ", "тела в точках (−μ, 0) и (1 − μ, 0)"],
            [
                "λ, D, Δ",
                "1 мкм, 1 м, 1 а.е.",
                "дифракционно-ограниченный пучок: перетяжка w ≈ 1.82e5 м",
            ],
            [
                "частица",
                "ρ = 3000 кг/м³, R = 1 мкм, Q_pr = 1.3",
                "пылевая пробная частица (силикат)",
            ],
            [
                "мощность лазера",
                "10 кВт … 10 МВт",
                "даёт β ≈ 1.7e-11 … 1.7e-8 на 1 а.е. (честная таблица)",
            ],
        ],
    },
    "equations": [
        {
            "id": "E1",
            "latex": "\\Omega(x,y) = \\tfrac{1}{2}(x^2+y^2) + (1-\\beta)\\,\\frac{1-\\mu}{r_1} + \\frac{\\mu}{r_2}",
            "desc_en": "Effective potential",
            "desc_ru": "Эффективный потенциал",
        },
        {
            "id": "E2",
            "latex": "\\ddot{x} - 2\\dot{y} = \\partial_x\\Omega, \\qquad \\ddot{y} + 2\\dot{x} = \\partial_y\\Omega",
            "desc_en": "Equations of motion in the rotating frame",
            "desc_ru": "Уравнения движения во вращающейся системе",
        },
        {
            "id": "E3",
            "latex": "C_J = 2\\Omega - (\\dot{x}^2 + \\dot{y}^2)",
            "desc_en": "Jacobi constant",
            "desc_ru": "Интеграл Якоби",
        },
        {
            "id": "E4",
            "latex": "\\nabla\\Omega = 0",
            "desc_en": "Libration points (collinear roots by bracketed bisection, triangular by 2-D Newton)",
            "desc_ru": "Точки либрации (коллинеарные — бисекцией в скобках, треугольные — 2-D Ньютоном)",
        },
        {
            "id": "E5",
            "latex": "\\begin{pmatrix} 0 & 0 & 1 & 0\\\\ 0 & 0 & 0 & 1\\\\ \\Omega_{xx} & \\Omega_{xy} & 0 & 2\\\\ \\Omega_{xy} & \\Omega_{yy} & -2 & 0 \\end{pmatrix}",
            "desc_en": "Linear-stability matrix at a libration point",
            "desc_ru": "Матрица линейной устойчивости в точке либрации",
        },
    ],
    "scheme_cap_en": (
        "TRX-01 scheme — laser-dressed CR3BP: photon pressure renormalizes the pull of "
        "primary 1 by (1 − β); the triangular point migrates toward the radiating mass."
    ),
    "scheme_cap_ru": (
        "Схема TRX-01 — лазерно-одетая ОКЗТТ: давление фотонов перенормирует притяжение "
        "первого тела множителем (1 − β); треугольная точка мигрирует к светящейся массе."
    ),
    "scheme_walk_en": [
        ["Laser beam", "power P, λ = 1 µm, aperture 1 m, thrown across Δ = 1 AU onto primary 1"],
        [
            "Primary 1 (radiating)",
            "m₁ = 1 − μ; its gravity on the particle is multiplied by (1 − β)",
        ],
        ["Primary 2", "m₂ = μ, unperturbed Newtonian gravity"],
        ["Equilateral configuration", "side 1 (canonical unit) — the Lagrange triangle skeleton"],
        ["Classical L4 / displaced L4", "the gold marker slides toward primary 1 as β grows"],
        ["Shift arrow", "monotone displacement verified over β ∈ {0.01, 0.05, 0.1}"],
    ],
    "scheme_walk_ru": [
        [
            "Лазерный пучок",
            "мощность P, λ = 1 мкм, апертура 1 м, брошен через Δ = 1 а.е. на первое тело",
        ],
        ["Первое тело (светящееся)", "m₁ = 1 − μ; его гравитация на частицу умножается на (1 − β)"],
        ["Второе тело", "m₂ = μ, невозмущённая ньютоновская гравитация"],
        [
            "Равносторонняя конфигурация",
            "сторона 1 (каноническая единица) — скелет треугольника Лагранжа",
        ],
        ["Классическая L4 / смещённая L4", "золотой маркер скользит к первому телу с ростом β"],
        ["Стрелка сдвига", "монотонность смещения проверена по β ∈ {0.01, 0.05, 0.1}"],
    ],
    "mapping": {
        "header_en": ["Quantity in this study", "TRIVORTEX analog", "Comment"],
        "header_ru": ["Величина исследования", "Аналог в TRIVORTEX", "Комментарий"],
        "rows_en": [
            [
                "L4/L5 equilateral points",
                "Lagrange triangle of Theorem 3.1",
                "same central configuration",
            ],
            ["Jacobi constant C_J", "Chaplygin integral C_Ch", "the invariant that pins the orbit"],
            [
                "β (radiation renormalization)",
                "effective circulation Γ renormalization",
                'both weaken one "body" without moving it',
            ],
            [
                "Marginal L4 stability (μ < μ_Routh)",
                "rotating vortex triangle stability",
                "shared Routh-type criterion",
            ],
        ],
        "rows_ru": [
            [
                "Равносторонние точки L4/L5",
                "лагранжев треугольник теоремы 3.1",
                "та же центральная конфигурация",
            ],
            ["Интеграл Якоби C_J", "интеграл Чаплыгина C_Ch", "инвариант, закрепляющий орбиту"],
            [
                "β (радиационная перенормировка)",
                "перенормировка эффективной циркуляции Γ",
                "оба ослабляют одно «тело», не двигая его",
            ],
            [
                "Нейтральная устойчивость L4 (μ < μ_Routh)",
                "устойчивость вращающегося вихревого треугольника",
                "общий критерий типа Рауса",
            ],
        ],
    },
    "nondim_en": (
        "All dynamics in canonical CR3BP units: length = Earth–Moon distance, "
        "time = 1/n, mass = m₁ + m₂, GM = 1. Velocities in normalized units "
        "(1 unit ≈ 1.018 km/s for Earth–Moon)."
    ),
    "nondim_ru": (
        "Вся динамика в канонических единицах ОКЗТТ: длина — расстояние Земля–Луна, "
        "время — 1/n, масса — m₁ + m₂, GM = 1. Скорости в нормированных единицах "
        "(1 единица ≈ 1.018 км/с для системы Земля–Луна)."
    ),
    "checks": {
        "header_en": ["Check", "Target", "Tolerance"],
        "header_ru": ["Проверка", "Цель", "Допуск"],
        "rows_en": [
            ["L1 abscissa at β = 0 vs published Earth–Moon value", "0.8369151", "5e-6"],
            [
                "L4 displacement monotone in β over {0, 0.01, 0.05, 0.1}",
                "strictly increasing",
                "exact",
            ],
            [
                "L4 displacement directed toward the radiating primary",
                "positive projection test",
                "exact",
            ],
            ["max |Re(eigenvalue)| of L4 at β = 0", "0", "1e-8"],
            ["L1 abscissa decreases with β (toward primary 1)", "sign test", "exact"],
            ["Jacobi drift along L4-region orbit (β = 0.05, DOP853 1e-12)", "0", "1e-10"],
        ],
        "rows_ru": [
            [
                "Абсцисса L1 при β = 0 против опубликованного значения Земля–Луна",
                "0.8369151",
                "5e-6",
            ],
            ["Смещение L4 монотонно по β на {0, 0.01, 0.05, 0.1}", "строго возрастает", "точно"],
            ["Смещение L4 направлено к светящемуся телу", "тест проекции", "точно"],
            ["max |Re(собств. знач.)| в L4 при β = 0", "0", "1e-8"],
            ["Абсцисса L1 убывает с ростом β (к первому телу)", "знаковый тест", "точно"],
            ["Дрейф Жакоби вдоль орбиты у L4 (β = 0.05, DOP853 1e-12)", "0", "1e-10"],
        ],
    },
    "figure_caps": {
        "fig01_landscape.png": {
            "cap_en": "Libration-point landscape of the laser-dressed CR3BP: geometry at β = 0 versus β = 0.1.",
            "cap_ru": "Ландшафт точек либрации лазерно-одетой ОКЗТТ: геометрия при β = 0 и β = 0.1.",
            "walk_en": "The panel pair shows the primaries, the five libration points and the zero-velocity topology; at β = 0.1 the triangular markers have visibly slid toward the radiating primary while the collinear roots drift along the x-axis.",
            "walk_ru": "Пара панелей показывает массивные тела, пять точек либрации и топологию нулевых скоростей; при β = 0.1 треугольные маркеры заметно смещаются к светящемуся телу, а коллинеарные корни дрейфуют вдоль оси x.",
        },
        "fig02_l4_shift.png": {
            "cap_en": "Headline result: migration of the triangular point L4 toward the radiating primary as β grows.",
            "cap_ru": "Главный результат: миграция треугольной точки L4 к светящемуся телу с ростом β.",
            "walk_en": "The displacement norm grows monotonically from 0 to ≈ 4.1e-2 over β ∈ {0, 0.01, 0.05, 0.1}, and the direction test confirms the shift points at primary 1 (projection −0.035 < 0).",
            "walk_ru": "Норма смещения монотонно растёт от 0 до ≈ 4.1e-2 по β ∈ {0, 0.01, 0.05, 0.1}, а тест направления подтверждает сдвиг к первому телу (проекция −0.035 < 0).",
        },
        "fig03_stability_scan.png": {
            "cap_en": "Linear-stability characteristics of the displaced L4 versus the radiation coefficient β.",
            "cap_ru": "Характеристики линейной устойчивости смещённой L4 в зависимости от коэффициента излучения β.",
            "walk_en": "At β = 0 the spectral radius of the L4 fixed point is 1.86e-16 — marginal stability of the classical equilateral solution; the scan tracks how the eigenbranches respond to the radiation renormalization.",
            "walk_ru": "При β = 0 спектральный радиус положения равновесия L4 равен 1.86e-16 — нейтральная устойчивость классического равностороннего решения; развёртка показывает отклик ветвей собственных значений на радиационную перенормировку.",
        },
        "fig04_jacobi_drift.png": {
            "cap_en": "Orbit integrated near the displaced L4 (β = 0.05) and conservation of the Jacobi integral.",
            "cap_ru": "Орбита, интегрированная возле смещённой L4 (β = 0.05), и сохранение интеграла Якоби.",
            "walk_en": "Over T = 20 (about three revolutions) the DOP853 integration at rtol = atol = 1e-12 conserves C_J to 8.88e-16 — machine-level invariance for the structure-setting integral.",
            "walk_ru": "За T = 20 (около трёх оборотов) интегрирование DOP853 с rtol = atol = 1e-12 сохраняет C_J с точностью 8.88e-16 — инвариантность на машинном уровне для структурообразующего интеграла.",
        },
    },
    "results_block": [
        "L1_abscissa_beta0                   = 0.836915126  (reference 0.8369151)",
        "L4_shift_monotone_in_beta           = PASS (shifts 0 -> 4.6e-3 -> 2.1e-2 -> 4.1e-2)",
        "L4_shift_toward_radiating_primary   = PASS (projection -0.035 < 0)",
        "L4_max_Re_eigenvalue_beta0          = 1.9e-16      (marginally stable)",
        "L1_shifts_toward_radiating_primary  = PASS (x: 0.8369151 -> 0.8369149)",
        "Jacobi_drift_L4_orbit_beta0.05      = 8.9e-16      (T = 20, DOP853 1e-12)",
        "status: PASS (6/6)",
    ],
    "abstract_en": (
        "This monograph treats the circular restricted three-body problem in which the "
        "primary of mass 1 − μ is continuously illuminated by a laser, so that a massless particle "
        "feels the renormalized attraction (1 − β)·G(1 − μ)/r² with β the photon-to-gravity force "
        "ratio. The study establishes the machine-precision baseline of the laser-dressed problem "
        "for the Earth–Moon mass parameter μ = 0.0121505856: (i) at β = 0 the computed L1 abscissa "
        "0.836915126 reproduces the published reference 0.8369151 within 5e-6; (ii) the triangular "
        "point L4 migrates monotonically toward the radiating primary, reaching a displacement of "
        "≈ 4.1e-2 at β = 0.1, with the direction confirmed by projection onto the primary line; "
        "(iii) the displaced L4 remains linearly marginally stable over the scanned range, the "
        "β = 0 spectral radius being 1.86e-16; (iv) the Jacobi integral is conserved along an "
        "orbit near the displaced point to 8.88e-16 over T = 20 at integrator tolerance 1e-12. "
        "The laser thus appears as a massless actuator on the libration landscape, the foundation "
        "on which the stationkeeping application of TRX-12 is built."
    ),
    "abstract_ru": (
        "Монография посвящена ограниченной круговой задаче трёх тел, в которой массивное "
        "первичное тело массой 1 − μ непрерывно освещается лазером, так что безмассовая частица "
        "испытывает перенормированное притяжение (1 − β)·G(1 − μ)/r², где β — отношение "
        "фотонной силы к гравитационной. Работа устанавливает базовую линию лазерно-одетой задачи "
        "с машинной точностью для массового параметра Земля–Луна μ = 0.0121505856: (i) при β = 0 "
        "вычисленная абсцисса L1 0.836915126 воспроизводит опубликованный эталон 0.8369151 с "
        "точностью 5e-6; (ii) треугольная точка L4 мигрирует монотонно к светящемуся телу, "
        "достигая смещения ≈ 4.1e-2 при β = 0.1, направление подтверждено проекцией на линию тел; "
        "(iii) смещённая L4 остаётся линейно нейтрально устойчивой во всём сканируемом диапазоне, "
        "спектральный радиус при β = 0 равен 1.86e-16; (iv) интеграл Якоби сохраняется вдоль "
        "орбиты возле смещённой точки на уровне 8.88e-16 за T = 20 при допуске интегратора 1e-12. "
        "Лазер выступает безмассовым актуатором ландшафта либрации — фундаментом, на котором "
        "строится приложение удержания в TRX-12."
    ),
    "intro_en": [
        (
            "The equilateral solutions of the three-body problem were found by Joseph-Louis Lagrange "
            "in his 1772 *Essai sur le problème des trois corps*, and for more than a century they "
            "were regarded as mathematical curiosities. The discovery of the Trojan asteroids at the "
            "Sun–Jupiter L4 and L5 turned the Lagrange triangle into a real object of celestial "
            "mechanics, and Szebehely's 1967 monograph consolidated the restricted problem into the "
            "standard reference frame that every modern libration-point mission still uses. The "
            "triangular points are precisely the celestial twin of the same-sign vortex triangle "
            "studied in the TRIVORTEX monograph."
        ),
        (
            "The idea that radiation modifies gravity is equally classical. Radzievskii (1950) "
            "formulated the restricted problem with radiating masses, replacing the gravitational "
            "parameter of a luminous body by Gm(1 − β). Burns, Lamy and Soter (1979) systematized "
            "the radiation forces on small particles — radiation pressure, Poynting–Robertson drag "
            "and the Yarkovsky effect — creating the standard toolkit of dust dynamics. Simmons, "
            "McDonald and Ward (1985) then mapped the stability structure of the photogravitational "
            "restricted problem, showing that radiation pressure moves and destabilizes the "
            "equilibrium points in a fully predictable way."
        ),
        (
            "Lasers add a qualitatively new element to this classical story: coherence and "
            "directivity. A diffraction-limited beam delivers photon momentum to a chosen target "
            "indefinitely, which is the operating principle of proposed laser light sails, of "
            "laser debris-sweeping concepts and of laser-trapped dust dynamics. In all of these the "
            "illuminated object behaves as if the gravity of the source had been reduced by the "
            "factor (1 − β) — exactly the model studied here, with β treated as a free parameter "
            "because realistic AU-scale values (≈ 1.7e-11 … 1.7e-8 for our table) are tiny for dust "
            "but decisive for thin light sails."
        ),
        (
            "For TRIVORTEX the relevance is structural rather than technological. The Jacobi "
            "integral of the restricted problem plays the same organizing role as the Chaplygin "
            "integral C_Ch = r²(θ̇ − qA_θ) of the vortex model: both pin the orbit to a reduced "
            "phase space in which the choreography becomes solvable. Establishing that this "
            "integral survives laser dressing to machine precision is therefore the correct first "
            "step of the laser block of the research program (TRX-01, TRX-10, TRX-11, TRX-12)."
        ),
    ],
    "intro_ru": [
        (
            "Равносторонние решения задачи трёх тел нашёл Жозеф-Луи Лагранж в «Essai sur le "
            "problème des trois corps» (1772), и более века они считались математическими "
            "диковинками. Открытие троянских астероидов в точках L4 и L5 Солнце–Юпитер превратило "
            "лагранжев треугольник в реальный объект небесной механики, а монография Себехея (1967) "
            "закрепила ограниченную задачу в стандартной системе отсчёта, которой пользуются все "
            "современные миссии к точкам либрации. Треугольные точки — точный небесный близнец "
            "одноимённого вихревого треугольника из монографии TRIVORTEX."
        ),
        (
            "Идея о том, что излучение модифицирует гравитацию, столь же классична. Радзиевский "
            "(1950) сформулировал ограниченную задачу со светящимися массами, заменив "
            "гравитационный параметр светящегося тела на Gm(1 − β). Бернс, Лэми и Сотер (1979) "
            "систематизировали радиационные силы на малых частицах — давление света, "
            "Пойнтинга–Робертсона и Ярковского — создав стандартный инструментарий динамики пыли. "
            "Симмонс, Макдональд и Уорд (1985) картировали структуру устойчивости "
            "фотогравитационной ограниченной задачи, показав, что давление излучения сдвигает и "
            "дестабилизирует положения равновесия полностью предсказуемым образом."
        ),
        (
            "Лазеры добавляют к этой классической истории качественно новый элемент: когерентность "
            "и направленность. Дифракционно-ограниченный пучок доставляет импульс фотонов выбранной "
            "цели неограниченно долго — так работают концепции лазерных парусов, лазерной уборки "
            "мусора и динамики лазерно-захваченной пыли. Во всех этих задачах освещённый объект "
            "ведёт себя так, будто гравитация источника уменьшена множителем (1 − β) — именно эта "
            "модель изучается здесь, причём β рассматривается как свободный параметр, поскольку "
            "реалистичные значения на шкале а.е. (≈ 1.7e-11 … 1.7e-8 из нашей таблицы) ничтожны "
            "для пыли, но решающие для тонких парусов."
        ),
        (
            "Для TRIVORTEX значимость структурна, а не технологична. Интеграл Якоби ограниченной "
            "задачи играет ту же организующую роль, что и интеграл Чаплыгина "
            "C_Ch = r²(θ̇ − qA_θ) вихревой модели: оба закрепляют орбиту в редуцированном фазовом "
            "пространстве, где хореография становится разрешимой. Поэтому установление того, что "
            "этот инвариант переживает лазерную «одежду» с машинной точностью, — правильный первый "
            "шаг лазерного блока программы (TRX-01, TRX-10, TRX-11, TRX-12)."
        ),
    ],
    "derivation_en": [
        (
            "In the rotating frame the two primaries are fixed at (−μ, 0) and (1 − μ, 0). Summing "
            "the Newtonian attractions, the centrifugal term and the Coriolis term yields the "
            "equations of motion (E2) with the effective potential (E1); the Coriolis force does no "
            "work, which immediately produces the Jacobi integral (E3) by multiplying the equations "
            "of motion by the velocity and integrating. C_J is the single constant of the planar "
            "unperturbed restricted problem, and its level sets bound the accessible region — the "
            "zero-velocity curves."
        ),
        (
            "The laser enters only through (E1): the term (1 − μ)/r₁ becomes (1 − β)(1 − μ)/r₁. "
            "Nothing else changes — in particular the Coriolis structure and the existence of the "
            "Jacobi integral are untouched, because radiation pressure is conservative here (no "
            "ablation, no drag). The libration points solve ∇Ω = 0; the collinear roots are found "
            "by bracketed bisection on sign-stable intervals, the triangular roots by a two-dimensional "
            "Newton iteration seeded at the classical configuration."
        ),
        (
            "Linear stability follows from the Jacobian of the first-order system at the fixed "
            "point, the 4 × 4 matrix (E5). For the classical problem the triangular point is "
            "linearly stable iff μ < μ_Routh = ½(1 − √(23/27)) ≈ 0.03852; the Earth–Moon value "
            "0.01215 sits comfortably inside the stable island, and the study tracks how the "
            "eigenbranches deform as the radiation renormalization grows."
        ),
    ],
    "derivation_ru": [
        (
            "Во вращающейся системе оба массивных тела неподвижны в точках (−μ, 0) и (1 − μ, 0). "
            "Суммируя ньютоновские притяжения, центробежный член и силу Кориолиса, получаем "
            "уравнения движения (E2) с эффективным потенциалом (E1); сила Кориолиса работы не "
            "совершает, откуда умножением уравнений на скорость и интегрированием немедленно "
            "следует интеграл Якоби (E3). C_J — единственный интеграл плоской невозмущённой "
            "ограниченной задачи, а его линии уровня ограничивают доступную область — кривые "
            "нулевой скорости."
        ),
        (
            "Лазер входит только через (E1): член (1 − μ)/r₁ превращается в (1 − β)(1 − μ)/r₁. "
            "Больше ничего не меняется — в частности, структура Кориолиса и существование интеграла "
            "Якоби не затрагиваются, поскольку давление излучения здесь консервативно (без абляции "
            "и трения). Точки либрации решают ∇Ω = 0; коллинеарные корни находятся бисекцией в "
            "знакоустойчивых скобках, треугольные — двумерной итерацией Ньютона со стартом в "
            "классической конфигурации."
        ),
        (
            "Линейная устойчивость следует из якобиана системы первого порядка в положении "
            "равновесия — матрицы (E5) размера 4 × 4. Для классической задачи треугольная точка "
            "линейно устойчива тогда и только тогда, когда μ < μ_Routh = ½(1 − √(23/27)) ≈ 0.03852; "
            "значение Земля–Луна 0.01215 comfortably сидит внутри устойчивого острова, и работа "
            "прослеживает деформацию ветвей собственных значений по мере роста радиационной "
            "перенормировки."
        ),
    ],
    "connection_en": (
        "The mapping is one-to-one at the structural level. The equilateral points L4/L5 "
        "are the celestial realization of the same central configuration that underlies the "
        "vortex triangle of Theorem 3.1; the Jacobi integral plays the role of the Chaplygin "
        "integral as the invariant that pins the orbit; and the radiation coefficient β acts on "
        "the restricted problem exactly as an effective circulation renormalization acts on the "
        "vortex triangle — both weaken one agent of the configuration without displacing it. The "
        "Routh-type marginal stability of L4 for μ < μ_Routh has its direct counterpart in the "
        "stability of the rotating vortex triangle, which is why this study is the correct "
        "celestial anchor for the laser block of the program."
    ),
    "connection_ru": (
        "Соответствие взаимно-однозначно на структурном уровне. Равносторонние точки "
        "L4/L5 — небесная реализация той же центральной конфигурации, что лежит в основе "
        "вихревого треугольника теоремы 3.1; интеграл Якоби играет роль интеграла Чаплыгина как "
        "инварианта, закрепляющего орбиту; а коэффициент излучения β действует на ограниченную "
        "задачу в точности так, как перенормировка эффективной циркуляции действует на вихревой "
        "треугольник, — оба ослабляют одного участника конфигурации, не перемещая его. "
        "Нейтральная устойчивость L4 типа Рауса при μ < μ_Routh имеет прямой аналог в "
        "устойчивости вращающегося вихревого треугольника, поэтому данное исследование — "
        "правильный небесный якорь лазерного блока программы."
    ),
    "method_en": [
        (
            "Collinear libration points are roots of a scalar equation ∂Ω/∂x = 0 with ∂Ω/∂y = 0 "
            "automatically satisfied on the x-axis; each root is bracketed on a sign-stable interval "
            "and refined by bisection to machine precision. The triangular points are obtained by a "
            "two-dimensional Newton iteration on (∂Ω/∂x, ∂Ω/∂y) seeded at the classical "
            "configuration, converging quadratically for every scanned β."
        ),
        (
            "Stability is diagnosed through the eigenvalues of the 4 × 4 matrix (E5); the reported "
            "quantity is the spectral radius max|Re λ|. Orbits near the displaced L4 are integrated "
            "with an explicit Dormand–Prince 8(5,3) scheme at rtol = atol = 1e-12 over T = 20, and "
            "the Jacobi integral is monitored pointwise along the trajectory — the drift 8.88e-16 "
            "reported in the results is two orders below the stated acceptance tolerance 1e-10."
        ),
        (
            "Every quantity is dimensionless and every check stores its target, tolerance, unit and "
            "pass flag in the JSON protocol, so the entire study is reproducible from a single "
            "command with no network access and no stochastic seeds."
        ),
    ],
    "method_ru": [
        (
            "Коллинеарные точки либрации — корни скалярного уравнения ∂Ω/∂x = 0 при автоматическом "
            "∂Ω/∂y = 0 на оси x; каждый корень окружается знакоустойчивой скобкой и уточняется "
            "бисекцией до машинной точности. Треугольные точки находятся двумерной итерацией "
            "Ньютона по (∂Ω/∂x, ∂Ω/∂y) со стартом в классической конфигурации; сходимость "
            "квадратична для всех сканируемых β."
        ),
        (
            "Устойчивость диагностируется через собственные значения матрицы (E5) 4 × 4; "
            "отчётная величина — спектральный радиус max|Re λ|. Орбиты возле смещённой L4 "
            "интегрируются явной схемой Дормана–Принса 8(5,3) с rtol = atol = 1e-12 на T = 20, а "
            "интеграл Якоби контролируется поточечно вдоль траектории — reported дрейф 8.88e-16 на "
            "два порядка ниже заявленного допуска 1e-10."
        ),
        (
            "Каждая величина безразмерна, и каждая проверка хранит цель, допуск, единицу и флаг "
            "прохождения в JSON-протоколе, так что всё исследование воспроизводится одной командой "
            "без доступа к сети и без стохастических зёрен."
        ),
    ],
    "analysis_en": [
        (
            "**Baseline.** At β = 0 the computed L1 abscissa is 0.836915126 against the published "
            "Earth–Moon value 0.8369151 — agreement to 2.6e-8, two orders of magnitude inside the "
            "5e-6 acceptance tolerance. The β = 0 triangular point reproduces the classical "
            "configuration to 1e-14, and its spectral radius is 1.86e-16, confirming the marginal "
            "(neutral) stability expected for μ = 0.01215 < μ_Routh ≈ 0.03852."
        ),
        (
            "**Migration.** The displacement of L4 grows strictly monotonically over the scanned "
            "grid β ∈ {0, 0.01, 0.05, 0.1}: 0 → 4.6e-3 → 2.1e-2 → 4.1e-2. The direction test is "
            "passed at every β: the projection of the shift onto the line from L4 to the radiating "
            "primary is negative (−0.035 at β = 0.1), i.e. the triangular point slides toward the "
            "illuminated mass, in agreement with the perturbative prediction of Simmons et al. "
            "(1985). The collinear roots move as well: L1 shifts from 0.8369151 to 0.8369149 as β "
            "grows, toward primary 1."
        ),
        (
            "**Invariant.** Along an orbit integrated near the displaced L4 (β = 0.05) over T = 20 "
            "with DOP853 at rtol = atol = 1e-12, the Jacobi constant drifts by only 8.88e-16 — "
            "machine-level conservation. This is the structural guarantee that the zero-velocity "
            "topology, and with it the accessibility of the displaced libration point, is preserved "
            "under laser dressing."
        ),
        (
            "**Engineering honesty.** The laser scenario table shows that at Δ = 1 AU a "
            "diffraction-limited beam has waist w ≈ 1.82e5 m, and realistic powers (10 kW … 10 MW) "
            "give β ≈ 1.7e-11 … 1.7e-8 on silicate dust — far below the scanned range. The model "
            "therefore treats β as the free operational parameter; closing the gap is an exercise "
            "in beam engineering (larger apertures, shorter distances, thinner sails), not in "
            "physics."
        ),
    ],
    "analysis_ru": [
        (
            "**Базовая линия.** При β = 0 вычисленная абсцисса L1 равна 0.836915126 против "
            "опубликованного значения Земля–Луна 0.8369151 — согласие на уровне 2.6e-8, на два "
            "порядка внутри допуска 5e-6. Треугольная точка при β = 0 воспроизводит классическую "
            "конфигурацию с точностью 1e-14, её спектральный радиус 1.86e-16 подтверждает "
            "нейтральную устойчивость, ожидаемую при μ = 0.01215 < μ_Routh ≈ 0.03852."
        ),
        (
            "**Миграция.** Смещение L4 строго монотонно растёт по сканируемой сетке "
            "β ∈ {0, 0.01, 0.05, 0.1}: 0 → 4.6e-3 → 2.1e-2 → 4.1e-2. Тест направления проходит при "
            "каждом β: проекция сдвига на линию от L4 к светящемуся телу отрицательна (−0.035 при "
            "β = 0.1), то есть треугольная точка скользит к освещённой массе — в согласии с "
            "пертурбативным предсказанием Симмонса и др. (1985). Коллинеарные корни тоже движутся: "
            "L1 смещается с 0.8369151 до 0.8369149 с ростом β, к первому телу."
        ),
        (
            "**Инвариант.** Вдоль орбиты, интегрированной возле смещённой L4 (β = 0.05) на T = 20 "
            "схемой DOP853 с rtol = atol = 1e-12, константа Якоби дрейфует лишь на 8.88e-16 — "
            "сохранение на машинном уровне. Это структурная гарантия того, что топология нулевых "
            "скоростей, а с ней и достижимость смещённой точки либрации, сохраняется под лазерной "
            "«одеждой»."
        ),
        (
            "**Инженерная честность.** Таблица лазерного сценария показывает, что при Δ = 1 а.е. "
            "дифракционно-ограниченный пучок имеет перетяжку w ≈ 1.82e5 м, а реалистичные мощности "
            "(10 кВт … 10 МВт) дают β ≈ 1.7e-11 … 1.7e-8 на силикатной пыли — далеко ниже "
            "сканируемого диапазона. Поэтому модель трактует β как свободный операционный "
            "параметр; закрытие разрыва — задача инженерии пучка (большие апертуры, меньшие "
            "дистанции, более тонкие паруса), а не физики."
        ),
    ],
    "discussion_en": [
        (
            "The model is deliberately minimal: planar, circular, single radiating primary, and "
            "radiation pressure without ablation or drag. Within these assumptions all conclusions "
            "are exact statements about the governing equations rather than simulations of a "
            "specific mission. The natural extensions — elliptic orbit, both primaries radiating "
            "(the full Radzievskii problem), three-dimensional halo families around the displaced "
            "collinear points, and Poynting–Robertson drag as a dissipative channel — each preserve "
            "the verification style established here."
        ),
        (
            "The parameter regime is chosen for structural clarity rather than engineering "
            "realism: β up to 0.1 probes the far response of the landscape, while realistic dust "
            "values are many orders smaller. The honest laser table bridges the two regimes and "
            "shows that the relevant lever is the beam waist; a 10× larger aperture or a 10× "
            "shorter throw moves the achievable β by three orders of magnitude."
        ),
        (
            "Within the program, this study feeds TRX-12 (the same CR3BP with the laser as an "
            "actuator for stationkeeping), provides the displaced-point background for TRX-11 "
            "(unrestricted three-body dynamics) and pairs with TRX-05/TRX-09, which verify the "
            "vortex-side twin of the equilateral configuration. Together they close the loop "
            "between the celestial and the vortex formulation of TRIVORTEX."
        ),
    ],
    "discussion_ru": [
        (
            "Модель сознательно минимальна: плоская, круговая, одно светящееся тело, давление "
            "излучения без абляции и трения. В этих допущениях все выводы — точные утверждения об "
            "определяющих уравнениях, а не симуляция конкретной миссии. Естественные расширения — "
            "эллиптическая орбита, оба тела светящиеся (полная задача Радзиевского), "
            "трёхмерные семейства гало вокруг смещённых коллинеарных точек и трение "
            "Пойнтинга–Робертсона как диссипативный канал — каждое сохраняет установленный здесь "
            "верификационный стиль."
        ),
        (
            "Диапазон параметров выбран ради структурной ясности, а не инженерного реализма: β до "
            "0.1 зондирует дальний отклик ландшафта, тогда как реалистичные значения для пыли на "
            "много порядков меньше. Честная лазерная таблица связывает оба режима и показывает, "
            "что главный рычаг — перетяжка пучка; апертура в 10 раз больше или дистанция в 10 раз "
            "меньше сдвигают достижимое β на три порядка."
        ),
        (
            "В рамках программы это исследование питает TRX-12 (та же ОКЗТТ с лазером как "
            "актуатором удержания), даёт фон смещённых точек для TRX-11 (неограниченная динамика "
            "трёх тел) и парным образом связан с TRX-05/TRX-09, которые проверяют вихревого "
            "близнеца равносторонней конфигурации. Вместе они замыкают контур между небесной и "
            "вихревой формулировками TRIVORTEX."
        ),
    ],
    "conclusions_en": [
        "The laser-dressed CR3BP reproduces the classical libration landscape at β = 0 to machine precision (L1 = 0.836915126 vs reference 0.8369151).",
        "The triangular point L4 migrates monotonically toward the radiating primary: 0 → 4.6e-3 → 2.1e-2 → 4.1e-2 over β ∈ {0, 0.01, 0.05, 0.1}.",
        "The migration direction is confirmed by projection (−0.035 at β = 0.1): the shift points at the illuminated mass.",
        "The displaced L4 remains linearly marginally stable over the scanned range; the β = 0 spectral radius is 1.86e-16.",
        "The Jacobi integral is conserved to 8.88e-16 over T = 20 at DOP853 rtol = atol = 1e-12 — the structural invariant survives laser dressing.",
        "Realistic AU-scale laser powers give tiny dust β (1.7e-11 … 1.7e-8); β is therefore treated as a free operational parameter, with the beam-engineering gap stated openly.",
    ],
    "conclusions_ru": [
        "Лазерно-одетая ОКЗТТ воспроизводит классический ландшафт либрации при β = 0 с машинной точностью (L1 = 0.836915126 против эталона 0.8369151).",
        "Треугольная точка L4 мигрирует монотонно к светящемуся телу: 0 → 4.6e-3 → 2.1e-2 → 4.1e-2 по β ∈ {0, 0.01, 0.05, 0.1}.",
        "Направление миграции подтверждено проекцией (−0.035 при β = 0.1): сдвиг указывает на освещённую массу.",
        "Смещённая L4 остаётся линейно нейтрально устойчивой во всём сканируемом диапазоне; спектральный радиус при β = 0 равен 1.86e-16.",
        "Интеграл Якоби сохраняется на уровне 8.88e-16 за T = 20 при DOP853 rtol = atol = 1e-12 — структурный инвариант переживает лазерную «одежду».",
        "Реалистичные лазерные мощности на шкале а.е. дают ничтожную β для пыли (1.7e-11 … 1.7e-8); поэтому β трактуется как свободный операционный параметр с открыто указанным инженерным разрывом.",
    ],
    "references": [
        "1. Lagrange, J.-L. (1772). *Essai sur le problème des trois corps.* Prix de l'Académie Royale des Sciences de Paris, tome IX.",
        "2. Radzievskii, V. V. (1950). *The restricted problem of three bodies taking account of light pressure.* Astron. Zh. 27, 250.",
        "3. Simmons, J. F. L., McDonald, A. J. C., Ward, J. C. (1985). *The restricted three-body problem with radiation pressure.* Celestial Mechanics 35, 145–187.",
        "4. Szebehely, V. (1967). *Theory of Orbits: The Restricted Problem of Three Bodies.* Academic Press.",
        "5. Murray, C. D., Dermott, S. F. (1999). *Solar System Dynamics.* Cambridge University Press.",
        "6. Burns, J. A., Lamy, P. L., Soter, S. (1979). *Radiation forces on small particles in the solar system.* Icarus 40, 1–48.",
    ],
    "crosslinks_en": [
        "* **TRX-12** uses the same Earth–Moon CR3BP with the laser as an actuator instead of a perturbation (stationkeeping at L4).",
        "* **TRX-09/05** verify the vortex-side twin of the equilateral configuration.",
        "* **TRX-11** integrates the full three-body problem without restriction.",
    ],
    "crosslinks_ru": [
        "* **TRX-12** использует ту же ОКЗТТ Земля–Луна, но с лазером как актуатором, а не возмущением (удержание у L4).",
        "* **TRX-09/05** проверяют вихревого близнеца равносторонней конфигурации.",
        "* **TRX-11** интегрирует полную задачу трёх тел без ограничений.",
    ],
    "assumptions_en": [
        "Planar motion; the out-of-plane dimension is not modeled.",
        "Circular primary orbits; eccentricity of the binary is neglected.",
        "Radiation pressure only — no ablation, no Poynting–Robertson drag, so the Jacobi integral remains exact.",
        "Only primary 1 radiates; the second primary is treated as a dark body.",
        "The particle is massless and does not perturb the primaries.",
        "β is a free parameter; the honest SI laser table maps it to achievable powers at 1 AU.",
    ],
    "assumptions_ru": [
        "Плоское движение; вне-плоскостное измерение не моделируется.",
        "Круговые орбиты массивных тел; эксцентриситет двойной системы не учитывается.",
        "Только давление излучения — без абляции и трения Пойнтинга–Робертсона, поэтому интеграл Якоби остаётся точным.",
        "Светится только первое тело; второе считается тёмным.",
        "Частица безмассова и не возмущает массивные тела.",
        "β — свободный параметр; честная таблица СИ отображает его в достижимые мощности на 1 а.е.",
    ],
    "glance_en": [
        ["Block", "Laser optics — study 01 of 12"],
        ["Model", "laser-dressed planar CR3BP (Earth–Moon, μ = 0.0121505856)"],
        ["Key invariant", "Jacobi constant C_J"],
        ["Headline result", "L4 migrates 4.1e-2 toward the radiating primary at β = 0.1"],
        ["Verification", "6/6 checks PASS (full mode)"],
        ["Runtime", "0.10 s full · < 20 s smoke"],
    ],
    "glance_ru": [
        ["Блок", "Лазерная оптика — исследование 01 из 12"],
        ["Модель", "лазерно-одетая плоская ОКЗТТ (Земля–Луна, μ = 0.0121505856)"],
        ["Ключевой инвариант", "интеграл Якоби C_J"],
        ["Главный результат", "L4 мигрирует на 4.1e-2 к светящемуся телу при β = 0.1"],
        ["Верификация", "6/6 проверок PASS (полный режим)"],
        ["Время выполнения", "0.10 с полный · < 20 с smoke"],
    ],
    "glossary": {
        "header_en": ["Term", "Definition"],
        "header_ru": ["Термин", "Определение"],
        "rows_en": [
            [
                "CR3BP",
                "circular restricted three-body problem: two primaries on circular orbits plus a massless particle",
            ],
            ["β", "ratio of photon radiation force to gravitational force on the particle"],
            [
                "Libration point",
                "equilibrium of the effective potential in the rotating frame (L1…L5)",
            ],
            ["L4/L5", "triangular (equilateral) libration points"],
            [
                "Jacobi constant C_J",
                "the single integral of the planar restricted problem, C_J = 2Ω − v²",
            ],
            ["Zero-velocity curves", "level sets of C_J bounding the accessible region"],
            ["μ", "mass parameter m₂/(m₁ + m₂)"],
            ["μ_Routh ≈ 0.03852", "classical linear-stability threshold of the triangular points"],
            ["DOP853", "explicit Dormand–Prince 8(5,3) adaptive integrator"],
            ["Rotating frame", "frame co-rotating with the primaries, in which they are fixed"],
        ],
        "rows_ru": [
            [
                "ОКЗТТ",
                "ограниченная круговая задача трёх тел: два массивных тела на круговых орбитах плюс безмассовая частица",
            ],
            ["β", "отношение силы светового давления к гравитационной силе на частицу"],
            [
                "Точка либрации",
                "положение равновесия эффективного потенциала во вращающейся системе (L1…L5)",
            ],
            ["L4/L5", "треугольные (равносторонние) точки либрации"],
            [
                "Интеграл Якоби C_J",
                "единственный интеграл плоской ограниченной задачи, C_J = 2Ω − v²",
            ],
            ["Кривые нулевой скорости", "линии уровня C_J, ограничивающие доступную область"],
            ["μ", "массовый параметр m₂/(m₁ + m₂)"],
            ["μ_Routh ≈ 0.03852", "классический порог линейной устойчивости треугольных точек"],
            ["DOP853", "явный адаптивный интегратор Дормана–Принса 8(5,3)"],
            [
                "Вращающаяся система",
                "система, вращающаяся вместе с массивными телами, в которой они неподвижны",
            ],
        ],
    },
    "notation": {
        "header_en": ["Symbol", "Meaning"],
        "header_ru": ["Символ", "Смысл"],
        "rows_en": [
            ["x, y", "particle coordinates in the rotating frame"],
            ["ẋ, ẏ", "particle velocities in the rotating frame"],
            ["Ω", "effective potential"],
            ["r₁, r₂", "distances to primary 1 (radiating) and primary 2"],
            ["μ", "mass parameter, Earth–Moon: 0.0121505856"],
            ["β", "radiation coefficient, β = F_rad/F_grav"],
            ["C_J", "Jacobi constant"],
            ["λ", "eigenvalue of the linear-stability matrix"],
            ["T", "integration span"],
            ["w", "beam waist at target distance"],
            ["Q_pr", "radiation-pressure efficiency of the grain"],
        ],
        "rows_ru": [
            ["x, y", "координаты частицы во вращающейся системе"],
            ["ẋ, ẏ", "скорости частицы во вращающейся системе"],
            ["Ω", "эффективный потенциал"],
            ["r₁, r₂", "расстояния до первого (светящегося) и второго тела"],
            ["μ", "массовый параметр, Земля–Луна: 0.0121505856"],
            ["β", "коэффициент излучения, β = F_изл/F_грав"],
            ["C_J", "интеграл Якоби"],
            ["λ", "собственное значение матрицы линейной устойчивости"],
            ["T", "интервал интегрирования"],
            ["w", "перетяжка пучка на дистанции цели"],
            ["Q_pr", "эффективность давления излучения на частицу"],
        ],
    },
    "params_appendix": {
        "header_en": ["Symbol", "Value", "Role"],
        "header_ru": ["Символ", "Значение", "Роль"],
        "rows_en": [
            ["μ", "0.0121505856", "mass parameter (Earth–Moon)"],
            ["β", "{0, 0.01, 0.05, 0.1}", "radiation coefficient of primary 1"],
            ["r₁, r₂", "(x+μ, y), (x−1+μ, y)", "distances to the primaries"],
            ["C_J", "2Ω − v²", "Jacobi constant"],
            ["μ_Routh", "≈ 0.03852", "classical triangular-stability threshold"],
            ["T", "20", "integration span for the invariant check"],
            ["rtol, atol", "1e-12", "DOP853 tolerances"],
        ],
        "rows_ru": [
            ["μ", "0.0121505856", "массовый параметр (Земля–Луна)"],
            ["β", "{0, 0.01, 0.05, 0.1}", "коэффициент излучения первого тела"],
            ["r₁, r₂", "(x+μ, y), (x−1+μ, y)", "расстояния до массивных тел"],
            ["C_J", "2Ω − v²", "константа Якоби"],
            ["μ_Routh", "≈ 0.03852", "классический порог устойчивости треугольника"],
            ["T", "20", "интервал интегрирования для проверки инварианта"],
            ["rtol, atol", "1e-12", "допуски DOP853"],
        ],
    },
    "bibtex": [
        "@article{radzievskii1950,",
        "  author  = {Radzievskii, V. V.},",
        "  title   = {The restricted problem of three bodies taking account of light pressure},",
        "  journal = {Astronomicheskii Zhurnal},",
        "  year    = {1950}, volume = {27}, pages = {250}}",
        "",
        "@article{simmons1985,",
        "  author  = {Simmons, J. F. L. and McDonald, A. J. C. and Ward, J. C.},",
        "  title   = {The restricted three-body problem with radiation pressure},",
        "  journal = {Celestial Mechanics},",
        "  year    = {1985}, volume = {35}, pages = {145--187}}",
        "",
        "@book{szebehely1967,",
        "  author    = {Szebehely, V.},",
        "  title     = {Theory of Orbits: The Restricted Problem of Three Bodies},",
        "  publisher = {Academic Press}, year = {1967}}",
    ],
}
