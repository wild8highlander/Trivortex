# -*- coding: utf-8 -*-
"""Content pack for TRX-03 (v1.0.0 Monograph Edition). Rendered by scripts/build_study_docs.py."""

PACK = {
    "meta": {
        "study_id": "TRX-03",
        "dir_name": "TRX-03-soliton-molecule",
        "title_en": "Three-Soliton Molecule in a Mode-Locked Fiber Laser",
        "title_ru": "Молекула из трёх солитонов в волоконном лазере с синхронизацией мод",
        "script": "trx03_soliton_molecule.py",
        "results_json": "trx03_results.json",
        "scheme_file": "scheme_trx03.svg",
        "runtime_full": "1.2 s (4.7 s with --figures)",
    },
    "essence_en": (
        "Three ultrashort pulses circulating in a passively mode-locked fiber laser form a "
        'phase-locked "soliton molecule": in the reduced particle picture each pulse is a body with '
        "the conservative, phase-dependent pair interaction "
        "**V(r, Δφ) = C₁e^(−2r/L) − C₂e^(−r/L)cos 2Δφ**. The phase-locked triplet is a genuine "
        "optical three-body choreography: its equilibrium spacing s* is fixed by the three-body "
        "balance F(s*) + F(2s*) = 0, is compressed ≈ 30 % below the pair value r₀ = ln(4/3), and "
        "supports a breathing normal mode verified by FFT against the Hessian prediction to 0.21 %."
    ),
    "essence_ru": (
        "Три ультракоротких импульса, циркулирующие в волоконном лазере с пассивной "
        "синхронизацией мод, образуют синхронизованную по фазе «солитонную молекулу»: в "
        "редуцированном частичном представлении каждый импульс — тело с консервативным, зависящим от фазы "
        "парным взаимодействием **V(r, Δφ) = C₁e^(−2r/L) − C₂e^(−r/L)cos 2Δφ**. Синхронизованный "
        "триплет — настоящая оптическая трёхтельная хореография: равновесное расстояние s* "
        "фиксируется трёхтельным балансом F(s*) + F(2s*) = 0, сжато примерно на 30 % ниже парного "
        "значения r₀ = ln(4/3) и поддерживает дыхательную нормальную моду, подтверждённую Фурье-"
        "анализом против гессиановского предсказания с точностью 0.21 %."
    ),
    "mission_en": [
        (
            "Soliton molecules are the closest optical cousins of the three-body choreographies at the "
            "heart of TRIVORTEX. The monograph's Theorem 3.1 binds three vortices into a rigid rotating "
            "triangle; a mode-locked fiber laser binds three light pulses into an equally spaced "
            "temporal molecule by exactly the same mechanism — a pair-wise attractive balance in which "
            "every member feels all the others. This study makes that analogy quantitative and "
            'verifiable: the pulses become "bodies", their evanescent tails become the interaction '
            "law, and the cavity provides the environment in which the molecule assembles, relaxes and "
            "breathes."
        ),
        (
            "The study verifies four things to machine precision: that the pair binding law reproduces "
            "its analytic equilibrium r₀ = L·ln(2C₁/C₂) = ln(4/3) to 5.6e-17; that the anti-phase "
            "lock (Δφ = π/2) is purely repulsive over the whole tested range, so binding is a "
            "phase-selection effect; that a random triplet under overdamped damping relaxes into an "
            "equally spaced molecule whose spacing equals the three-chain equilibrium s* — the root of "
            "F(s) + F(2s) = 0, a genuinely three-body quantity compressed below the pair value; and "
            "that the conservative molecule conserves energy to 1.8e-15 while its breathing mode "
            "frequency matches the analytic Hessian spectrum to 0.21 %. Together these checks turn a "
            "qualitative optics story into a controlled three-body experiment in software."
        ),
    ],
    "mission_ru": [
        (
            "Солитонные молекулы — ближайшие оптические родственники трёхтельных хореографий, лежащих "
            "в основе TRIVORTEX. Теорема 3.1 монографии связывает три вихря в жёсткий вращающийся "
            "треугольник; волоконный лазер с синхронизацией мод связывает три световых импульса в "
            "равноотстоящую временную молекулу тем же самым механизмом — парным притягательным "
            "балансом, в котором каждый участник чувствует всех остальных. Данное исследование делает "
            "эту аналогию количественной и проверяемой: импульсы становятся «телами», их "
            "эванесцентные хвосты — законом взаимодействия, а резонатор — средой, в которой молекула "
            "собирается, релаксирует и дышит."
        ),
        (
            "Исследование проверяет четыре вещи с машинной точностью: что парной закон связывания "
            "воспроизводит аналитическое равновесие r₀ = L·ln(2C₁/C₂) = ln(4/3) с точностью 5.6e-17; "
            "что противофазная синхронизация (Δφ = π/2) чисто отталкивающая во всём испытанном "
            "диапазоне, так что связывание — эффект выбора фазы; что случайный триплет при "
            "сверхвязком демпфировании релаксирует в равноотстоящую молекулу, расстояние в которой "
            "равно равновесию трёхзвенной цепочки s* — корню уравнения F(s) + F(2s) = 0, подлинно "
            "трёхтельной величине, сжатой ниже парного значения; и что консервативная молекула "
            "сохраняет энергию на уровне 1.8e-15, а частота её дыхательной моды совпадает с "
            "аналитическим гессиановским спектром с точностью 0.21 %. Вместе эти проверки превращают "
            "качественную оптическую историю в контролируемый трёхтельный эксперимент в программе."
        ),
    ],
    "physics_en": [
        (
            "In a passively mode-locked fiber laser the circulating field breaks into ultrashort "
            "soliton pulses. When two pulses overlap, their phases and envelopes exchange work through "
            "the Kerr nonlinearity and the gain/loss balance of the cavity; in the reduced "
            "Gordon–Mollenauer picture this continuous exchange is equivalent to a conservative force "
            "between point-like particles with an exponential (evanescent-tail) profile. The force "
            "depends on the phase difference Δφ between the pulses: in-phase pulses (Δφ = 0) attract, "
            "quadrature pulses (Δφ = π/2) repel. A triplet locked in phase therefore behaves as three "
            "bodies on a line, bound by a soft exponential tail and free to pass through one another "
            "as real solitons do."
        ),
        (
            "The equilibrium of such a chain is a true three-body configuration. For a pair, attraction "
            "and the repulsive exponential core balance at r₀ = L·ln(2C₁/C₂). In the symmetric "
            "three-pulse molecule every pulse also feels the far pair at distance 2s, so the end-pulse "
            "balance reads F(s*) + F(2s*) = 0 and the spacing s* is compressed below r₀ — the same "
            "collective compression that the Lagrange triangle shows relative to an isolated two-body "
            "pair. Small displacements around the equilibrium decompose into normal modes of a "
            "generalized eigenproblem; the low mode is the breathing oscillation of the molecule, "
            "directly observable in real-time spectroscopy experiments."
        ),
    ],
    "physics_ru": [
        (
            "В волоконном лазере с пассивной синхронизацией мод циркулирующее поле распадается на "
            "ультракороткие солитонные импульсы. При перекрытии двух импульсов их фазы и огибающие "
            "обмениваются работой через нелинейность Керра и баланс усиления и потерь резонатора; в "
            "редуцированном представлении Гордона–Молленауэра этот непрерывный обмен эквивалентен "
            "консервативной силе между точечными частицами с экспоненциальным (эванесцентным) "
            "профилем. Сила зависит от разности фаз Δφ между импульсами: синфазные импульсы "
            "(Δφ = 0) притягиваются, импульсы в квадратуре (Δφ = π/2) отталкиваются. Поэтому "
            "синхронизованный по фазе триплет ведёт себя как три тела на прямой, связанные мягким "
            "экспоненциальным хвостом и свободно проходящие друг сквозь друга, как и настоящие "
            "солитоны."
        ),
        (
            "Равновесие такой цепочки — подлинная трёхтельная конфигурация. Для пары притяжение и "
            "отталкивающее экспоненциальное ядро уравновешиваются на r₀ = L·ln(2C₁/C₂). В симметричной "
            "трёхимпульсной молекуле каждый импульс чувствует также дальнюю пару на расстоянии 2s, "
            "поэтому баланс концевого импульса имеет вид F(s*) + F(2s*) = 0, а расстояние s* сжато "
            "относительно r₀ — то же коллективное сжатие, которое лагранжев треугольник демонстрирует "
            "по отношению к изолированной двухтельной паре. Малые смещения вокруг равновесия "
            "раскладываются на нормальные моды обобщённой задачи на собственные значения; низшая "
            "мода — дыхательное колебание молекулы, непосредственно наблюдаемое в экспериментах по "
            "спектроскопии реального времени."
        ),
    ],
    "preset_table": {
        "header_en": ["Parameter", "Value", "Meaning"],
        "header_ru": ["Параметр", "Значение", "Смысл"],
        "rows_en": [
            ["C₁, C₂", "2, 3", "exponential coefficients: repulsive core / attractive overlap"],
            ["L", "1", "evanescent-tail length (unit of length)"],
            ["m", "1", 'pulse "mass" (kinetic coefficient)'],
            ["Δφ", "0 (locked)", "phase difference between adjacent pulses"],
            [
                "pair equilibrium",
                "r₀ = L·ln(2C₁/C₂) = ln(4/3) ≈ 0.287682",
                "analytic two-body balance",
            ],
            ["relaxation start", "{1.0, 2.0, 3.5}, γ_d = 1 (overdamped)", "random triplet, T = 90"],
            [
                "conservative probe",
                "middle pulse +0.01, γ_d = 0, T = 100",
                "breathing-mode run, DOP853 1e-12",
            ],
        ],
        "rows_ru": [
            [
                "C₁, C₂",
                "2, 3",
                "экспоненциальные коэффициенты: отталкивающее ядро / притягивающее перекрытие",
            ],
            ["L", "1", "длина эванесцентного хвоста (единица длины)"],
            ["m", "1", "«масса» импульса (кинетический коэффициент)"],
            ["Δφ", "0 (синхронизация)", "разность фаз соседних импульсов"],
            [
                "парное равновесие",
                "r₀ = L·ln(2C₁/C₂) = ln(4/3) ≈ 0.287682",
                "аналитический двухтельный баланс",
            ],
            [
                "старт релаксации",
                "{1.0, 2.0, 3.5}, γ_d = 1 (сверхвязкий режим)",
                "случайный триплет, T = 90",
            ],
            [
                "консервативная проба",
                "средний импульс +0.01, γ_d = 0, T = 100",
                "прогон дыхательной моды, DOP853 1e-12",
            ],
        ],
    },
    "equations": [
        {
            "id": "E1",
            "latex": "V(r,\\Delta\\varphi) = C_1\\,e^{-2r/L} - C_2\\,e^{-r/L}\\cos(2\\Delta\\varphi)",
            "desc_en": "Phase-dependent pair potential of two solitons",
            "desc_ru": "Фазозависимый парный потенциал двух солитонов",
        },
        {
            "id": "E2",
            "latex": "F(r,\\Delta\\varphi) = -\\frac{\\partial V}{\\partial r} = \\frac{2C_1}{L}e^{-2r/L} - \\frac{C_2}{L}e^{-r/L}\\cos(2\\Delta\\varphi)",
            "desc_en": "Pair force along increasing separation (F < 0 — attraction)",
            "desc_ru": "Парная сила вдоль роста расстояния (F < 0 — притяжение)",
        },
        {
            "id": "E3",
            "latex": "m\\,\\ddot{x}_k = -\\sum_{l\\neq k}\\frac{\\partial V(|x_k-x_l|)}{\\partial x_k} - \\gamma_d\\,\\dot{x}_k, \\qquad k=1,2,3",
            "desc_en": "Chain dynamics with all-pairs interaction and damping",
            "desc_ru": "Динамика цепочки с взаимодействием всех пар и демпфированием",
        },
        {
            "id": "E4",
            "latex": "r_0 = L\\ln\\!\\frac{2C_1}{C_2\\cos 2\\Delta\\varphi}; \\qquad F(s^*) + F(2s^*) = 0",
            "desc_en": "Pair equilibrium r0 and three-chain equilibrium s* (end-pulse balance)",
            "desc_ru": "Парное равновесие r0 и равновесие трёхзвенной цепочки s* (баланс концевого импульса)",
        },
        {
            "id": "E5",
            "latex": "H\\,v = \\omega^2 M_g\\,v, \\quad H = \\begin{pmatrix} V''(s)+V''(2s) & V''(2s)\\\\ V''(2s) & V''(s)+V''(2s) \\end{pmatrix}, \\quad M_g = m\\begin{pmatrix} 2/3 & 1/3\\\\ 1/3 & 2/3 \\end{pmatrix}",
            "desc_en": "Generalized eigenproblem for the chain normal modes (breathing spectrum)",
            "desc_ru": "Обобщённая задача на собственные значения для нормальных мод цепочки (дыхательный спектр)",
        },
    ],
    "scheme_cap_en": (
        "TRX-03 scheme — soliton molecule: a phase-locked triplet circulating in a "
        "mode-locked fiber ring, bound by the phase-dependent exponential pair interaction; the "
        "potential well with minimum r₀ = ln(4/3) holds an equally spaced molecule at s*, fixed by "
        "the three-body balance F(s*) + F(2s*) = 0."
    ),
    "scheme_cap_ru": (
        "Схема TRX-03 — солитонная молекула: синхронизованный триплет, циркулирующий "
        "в волоконном кольце с синхронизацией мод, связанный фазозависимым экспоненциальным парным "
        "взаимодействием; потенциальная яма с минимумом r₀ = ln(4/3) удерживает равноотстоящую "
        "молекулу на расстоянии s*, зафиксированном трёхтельным балансом F(s*) + F(2s*) = 0."
    ),
    "scheme_walk_en": [
        [
            "Fiber ring",
            "mode-locked fiber laser cavity; circulating pulses pass through one another",
        ],
        ["Three gold pulses", "phase-locked at Δφ = 0 — an optical three-body choreography"],
        ["Potential well", "V(r, 0) with minimum at the pair equilibrium r₀ = ln(4/3) ≈ 0.2877"],
        ["Repulsive branch", "anti-phase Δφ = π/2 curve: binding is a phase-selection effect"],
        ["Equally spaced molecule", "spacing s* = 0.2019 from the balance F(s*) + F(2s*) = 0"],
        ["Compression note", "far-pair attraction holds the spacing ≈ 30 % below the pair value"],
    ],
    "scheme_walk_ru": [
        [
            "Волоконное кольцо",
            "резонатор лазера с синхронизацией мод; импульсы проходят друг сквозь друга",
        ],
        [
            "Три золотых импульса",
            "синхронизованы по фазе Δφ = 0 — оптическая трёхтельная хореография",
        ],
        ["Потенциальная яма", "V(r, 0) с минимумом в парном равновесии r₀ = ln(4/3) ≈ 0.2877"],
        ["Отталкивающая ветвь", "кривая противофазы Δφ = π/2: связывание — эффект выбора фазы"],
        ["Равноотстоящая молекула", "расстояние s* = 0.2019 из баланса F(s*) + F(2s*) = 0"],
        [
            "Примечание о сжатии",
            "притяжение дальней пары удерживает расстояние ≈ 30 % ниже парного значения",
        ],
    ],
    "mapping": {
        "header_en": ["Quantity in this study", "TRIVORTEX analog", "Comment"],
        "header_ru": ["Величина исследования", "Аналог в TRIVORTEX", "Комментарий"],
        "rows_en": [
            [
                "Three phase-locked pulses",
                "three bodies of Theorem 3.1",
                "both are choreographic triads",
            ],
            ["Phase locking Δφ = 0", "equal circulations Γ", "symmetric special solution"],
            [
                "Molecule spacing s*",
                "Lagrange-triangle side a",
                "fixed by collective force balance",
            ],
            [
                "Balance F(s*) + F(2s*) = 0",
                "every vortex feels the other two",
                "the three-body compression mechanism",
            ],
            [
                "Breathing mode ω₂",
                "radial modulation of the choreography",
                "small oscillations about the central configuration",
            ],
        ],
        "rows_ru": [
            [
                "Три синхронизованных импульса",
                "три тела теоремы 3.1",
                "обе системы — хореографические триады",
            ],
            ["Синхронизация фаз Δφ = 0", "равные циркуляции Γ", "симметричное специальное решение"],
            [
                "Расстояние в молекуле s*",
                "сторона лагранжева треугольника a",
                "фиксируется коллективным балансом сил",
            ],
            [
                "Баланс F(s*) + F(2s*) = 0",
                "каждый вихрь чувствует два других",
                "механизм трёхтельного сжатия",
            ],
            [
                "Дыхательная мода ω₂",
                "радиальная модуляция хореографии",
                "малые колебания около центральной конфигурации",
            ],
        ],
    },
    "nondim_en": (
        "All quantities are dimensionless in cavity units: lengths in units of the "
        "evanescent-tail length L, energies in units of C₁, time in units of (m L²/C₁)^(1/2); the "
        "pulse mass m = 1. Damping γ_d = 1.0 in the relaxation runs (overdamped regime of a "
        "mode-locked laser) and γ_d = 0 in the conservative runs."
    ),
    "nondim_ru": (
        "Все величины безразмерны в единицах резонатора: длины — в единицах длины "
        "эванесцентного хвоста L, энергии — в единицах C₁, время — в единицах (m L²/C₁)^(1/2); "
        "масса импульса m = 1. Демпфирование γ_d = 1.0 в релаксационных прогонах (сверхвязкий "
        "режим лазера с синхронизацией мод) и γ_d = 0 в консервативных прогонах."
    ),
    "checks": {
        "header_en": ["Check", "Target", "Tolerance"],
        "header_ru": ["Проверка", "Цель", "Допуск"],
        "rows_en": [
            ["Pair equilibrium: brentq root vs r₀ = ln(4/3)", "0", "1e-10"],
            ["Δφ = π/2 purely repulsive (min force over r ∈ [0.05, 20])", "> 0", "exact"],
            ["Final spacings equal (sorted positions after relaxation)", "0", "1e-8"],
            ["Final spacing equals s* (root of F(s) + F(2s) = 0)", "0", "1e-6"],
            ["Conservative energy drift over t = 100", "0", "1e-10"],
            ["Breathing frequency: FFT peak vs Hessian eigenfrequency", "equal", "1%"],
        ],
        "rows_ru": [
            ["Парное равновесие: корень brentq против r₀ = ln(4/3)", "0", "1e-10"],
            ["Δφ = π/2 чисто отталкивающее (мин. сила по r ∈ [0.05, 20])", "> 0", "точно"],
            ["Равенство конечных расстояний (сортированные позиции)", "0", "1e-8"],
            ["Конечное расстояние равно s* (корень F(s) + F(2s) = 0)", "0", "1e-6"],
            ["Дрейф консервативной энергии за t = 100", "0", "1e-10"],
            ["Дыхательная частота: пик Фурье против гессиановской моды", "равны", "1%"],
        ],
    },
    "figure_caps": {
        "fig01_potential_landscape.png": {
            "cap_en": "Interaction landscape: phase-dependent pair potential and the three-chain force balance.",
            "cap_ru": "Ландшафт взаимодействия: фазозависимый парный потенциал и силовой баланс трёхзвенной цепочки.",
            "walk_en": "Panel (a) shows V(r, Δφ) for four lockings: the binding well exists only for |Δφ| < π/4, has its minimum at r₀ = 0.287682, and degenerates into pure repulsion for the anti-phase case. Panel (b) shows the end-pulse balance F(s) + F(2s) = 0: the root s* = 0.201893 lies 29.8 % below the pair value r₀ — a genuine three-body compression.",
            "walk_ru": "Панель (а) показывает V(r, Δφ) для четырёх синхронизаций: связывающая яма существует лишь при |Δφ| < π/4, имеет минимум в r₀ = 0.287682 и вырождается в чистое отталкивание в противофазном случае. Панель (б) показывает баланс концевого импульса F(s) + F(2s) = 0: корень s* = 0.201893 лежит на 29.8 % ниже парного значения r₀ — подлинное трёхтельное сжатие.",
        },
        "fig02_molecule_formation.png": {
            "cap_en": "Headline result: relaxation of a random triplet into the equally spaced soliton molecule.",
            "cap_ru": "Главный результат: релаксация случайного триплета в равноотстоящую солитонную молекулу.",
            "walk_en": "Starting from positions {1.0, 2.0, 3.5} under overdamped damping, the three worldlines settle within T = 90 into an equally spaced triplet; the sorted spacings d₁(t) and d₂(t) converge to the chain equilibrium s* = 0.201893 (final mismatch 2.2e-16, offset from s* 2.8e-17), visibly below the pair value r₀ = 0.2877 marked for comparison.",
            "walk_ru": "Стартуя с позиций {1.0, 2.0, 3.5} при сверхвязком демпфировании, три мировые линии за T = 90 приходят к равноотстоящему триплету; сортированные расстояния d₁(t) и d₂(t) сходятся к равновесию цепочки s* = 0.201893 (конечное расхождение 2.2e-16, отклонение от s* 2.8e-17), заметно ниже парного значения r₀ = 0.2877, нанесённого для сравнения.",
        },
        "fig03_phase_sweep.png": {
            "cap_en": "Parameter sweep over the locking phase: equilibrium geometry and mode softening.",
            "cap_ru": "Развёртка по фазе синхронизации: равновесная геометрия и размягчение мод.",
            "walk_en": "Both equilibria diverge as the binding threshold Δφ = π/4 is approached: s* grows from 0.201893 at Δφ = 0 through 0.719380 at Δφ = 0.5 rad to 2.885 at Δφ = 0.75 rad, tracking the pair value. The chain modes soften in response — from 2.4536 and 2.9453 rad at the preset down to 0.1092 and 0.1982 rad — producing a complete stability map of the phase-locked molecule.",
            "walk_ru": "Оба равновесия расходятся при приближении к порогу связывания Δφ = π/4: s* растёт от 0.201893 при Δφ = 0 через 0.719380 при Δφ = 0.5 рад до 2.885 при Δφ = 0.75 рад, следя за парным значением. Цепочечные моды в ответ размягчаются — от 2.4536 и 2.9453 рад в пресете до 0.1092 и 0.1982 рад — давая полную карту устойчивости синхронизованной молекулы.",
        },
        "fig04_breathing_dynamics.png": {
            "cap_en": "Dynamics of the conservative molecule: breathing time series and spectrum against the Hessian prediction.",
            "cap_ru": "Динамика консервативной молекулы: временной ряд дыхания и спектр против гессиановского предсказания.",
            "walk_en": "With the middle pulse displaced by 0.01 and damping removed, the molecule breathes over T = 100 while the total energy drifts by only 1.8e-15 (DOP853, rtol = atol = 1e-12). The FFT spectrum of the middle-pulse displacement peaks at f = 0.469765 against the analytic Hessian modes 0.468766 and 0.390507 — agreement to 0.21 %, an order of magnitude inside the 1 % tolerance.",
            "walk_ru": "При смещении среднего импульса на 0.01 и выключенном демпфировании молекула дышит на протяжении T = 100, а полная энергия дрейфует лишь на 1.8e-15 (DOP853, rtol = atol = 1e-12). Спектр Фурье смещения среднего импульса имеет пик на f = 0.469765 против аналитических гессиановских мод 0.468766 и 0.390507 — согласие 0.21 %, на порядок внутри допуска 1 %.",
        },
    },
    "results_block": [
        "pair_equilibrium_numeric_vs_analytic   = 5.551115e-17  (r0 = L*ln(2C1/C2) = ln(4/3))",
        "antiphase_pi2_purely_repulsive         = PASS (min pair force +6e-9 > 0 over r in [0.05, 20])",
        "molecule_final_spacings_equal          = 2.220446e-16  (d1 = d2 = 0.2018926516)",
        "molecule_final_spacing_equals_s_star   = 2.775558e-17  (s* = 0.2018926516; pair r0 = 0.287682)",
        "conservative_energy_drift              = 1.776357e-15  (damping-free molecule, t = 100)",
        "breathing_mode_frequency               = 0.469765 vs 0.468766 (Hessian), error 0.21%",
        "status: PASS (6/6)",
    ],
    "abstract_en": (
        "This monograph treats a phase-locked triplet of ultrashort pulses in a "
        "passively mode-locked fiber laser as an optical three-body system. Each pulse is a body "
        "with the conservative pair interaction V(r, Δφ) = C₁e^(−2r/L) − C₂e^(−r/L)cos 2Δφ, whose "
        "in-phase well has the analytic minimum r₀ = L·ln(2C₁/C₂) = ln(4/3) ≈ 0.287682, reproduced "
        "numerically to 5.6e-17, while the anti-phase lock Δφ = π/2 is proved purely repulsive. "
        "Relaxation of a random triplet {1.0, 2.0, 3.5} under overdamped damping converges to an "
        "equally spaced molecule whose spacing equals the three-chain equilibrium s* = 0.2018927, "
        "the root of F(s) + F(2s) = 0 — compressed 29.8 % below the pair value by the far-pair "
        "attraction, a genuine three-body effect. The conservative molecule conserves energy to "
        "1.8e-15 over t = 100 and breathes at f = 0.469765 against the analytic Hessian mode "
        "0.468766 (agreement 0.21 %); a sweep of the locking phase yields the full stability map, "
        "with both equilibria diverging and both modes softening to zero at the binding threshold "
        "Δφ = π/4. The soliton molecule thus stands verified as the optical twin of the TRIVORTEX "
        "three-body choreographies."
    ),
    "abstract_ru": (
        "Монография рассматривает синхронизованный триплет ультракоротких импульсов в "
        "волоконном лазере с пассивной синхронизацией мод как оптическую трёхтельную систему. "
        "Каждый импульс — тело с консервативным парным взаимодействием "
        "V(r, Δφ) = C₁e^(−2r/L) − C₂e^(−r/L)cos 2Δφ, синфазная яма которого имеет аналитический "
        "минимум r₀ = L·ln(2C₁/C₂) = ln(4/3) ≈ 0.287682, воспроизводимый численно с точностью "
        "5.6e-17, а противофазная синхронизация Δφ = π/2 доказуемо чисто отталкивающая. "
        "Релаксация случайного триплета {1.0, 2.0, 3.5} при сверхвязком демпфировании сходится к "
        "равноотстоящей молекуле, расстояние в которой равно равновесию трёхзвенной цепочки "
        "s* = 0.2018927 — корню уравнения F(s) + F(2s) = 0, сжатому на 29.8 % ниже парного "
        "значения притяжением дальней пары, подлинным трёхтельным эффектом. Консервативная "
        "молекула сохраняет энергию на уровне 1.8e-15 за t = 100 и дышит на частоте f = 0.469765 "
        "против аналитической гессиановской моды 0.468766 (согласие 0.21 %); развёртка по фазе "
        "синхронизации даёт полную карту устойчивости: оба равновесия расходятся, а обе моды "
        "размягчаются до нуля на пороге связывания Δφ = π/4. Тем самым солитонная молекула "
        "верифицирована как оптический близнец трёхтельных хореографий TRIVORTEX."
    ),
    "intro_en": [
        (
            'The word "soliton" was coined by Zabusky and Kruskal in 1965, when numerical '
            "experiments on the Korteweg–de Vries equation showed that nonlinear pulses collide and "
            "re-emerge with their identity intact. Optical solitons followed: Hasegawa and Tappert "
            "predicted in 1973 that the nonlinear Schrödinger equation admits shape-preserving pulses "
            "in fibers with anomalous dispersion, and Mollenauer, Stolen and Gordon observed them in "
            "1980. From the very beginning it was clear that two solitons are not merely two "
            "particles — their overlapping tails make them interact, and the interaction is the "
            "optical analog of a force."
        ),
        (
            "The quantitative theory of soliton interactions was built by Karpman and Solov'ev in 1981 "
            "through perturbation theory around the exact two-soliton solution, and by Gordon in 1983 "
            "through the discrete spectral picture; both approaches yield an exponential force whose "
            "sign is set by the relative phase. Malomed (1991) extended the analysis to multi-soliton "
            "bound states and their cyclic dynamics. Experimentally, Stratmann, Pagel and Mitschke "
            "(2005) directly observed temporal soliton molecules in a fiber laser, and Herink and "
            "colleagues (2017) filmed their internal dynamics in real time by spectral "
            "interferometry — including the breathing mode that this study computes analytically and "
            "numerically."
        ),
        (
            "A soliton molecule is therefore a genuine bound state of N bodies, not a metaphor: its "
            "geometry is fixed by a force balance in which every pulse feels every other pulse, its "
            "stability is read off a normal-mode spectrum, and its assembly is a relaxation problem. "
            "For N = 3 all of these ingredients are exactly what the three-body problem means in the "
            "TRIVORTEX program — three agents, pairwise interactions, a collective equilibrium and a "
            "choreography of motion. The fiber laser simply replaces gravity or vortex circulation by "
            "an exponential-cosine law that can be switched by phase control."
        ),
        (
            "Within the program this study is the optics-block anchor of the choreography family. It "
            'verifies, in a setting where "passing through one another" is physical rather than '
            "singular, the same structural sequence used everywhere in TRIVORTEX: analytic pair "
            "law, collective equilibrium, linearized spectrum, conservation of the invariant. The "
            "phase-locked triplet is the optical sibling of the Lagrange triangle of Theorem 3.1, and "
            "the compression of s* below r₀ is the spectral sibling of the collective force balance "
            "that fixes the equilateral configuration."
        ),
    ],
    "intro_ru": [
        (
            "Слово «солитон» придумали Забуски и Крускал в 1965 году, когда численные эксперименты с "
            "уравнением Кортевега–де Фриза показали, что нелинейные импульсы сталкиваются и "
            "воспроизводятся с сохранением индивидуальности. Оптические солитоны не заставили себя "
            "ждать: Хасэгава и Тапперт предсказали в 1973 году, что нелинейное уравнение Шрёдингера "
            "допускает импульсы, сохраняющие форму, в волокнах с аномальной дисперсией, а Молленауэр, "
            "Столен и Гордон наблюдали их в 1980-м. С самого начала было ясно, что два солитона — не "
            "просто две частицы: их перекрывающиеся хвосты заставляют их взаимодействовать, и это "
            "взаимодействие — оптический аналог силы."
        ),
        (
            "Количественную теорию взаимодействия солитонов построили Карпман и Соловьёв в 1981 году "
            "методом теории возмущений вокруг точного двухсолитонного решения, и Гордон в 1983 году "
            "через дискретную спектральную картину; оба подхода дают экспоненциальную силу, знак "
            "которой задаётся относительной фазой. Маломед (1991) расширил анализ на многосолитонные "
            "связанные состояния и их циклическую динамику. Экспериментально Стратман, Пагель и "
            "Мишке (2005) непосредственно наблюдали временные солитонные молекулы в волоконном "
            "лазере, а Херинк с соавторами (2017) засняли их внутреннюю динамику в реальном времени "
            "методом спектральной интерферометрии — включая дыхательную моду, которую данное "
            "исследование вычисляет аналитически и численно."
        ),
        (
            "Итак, солитонная молекула — подлинное связанное состояние N тел, а не метафора: её "
            "геометрия фиксируется силовым балансом, в котором каждый импульс чувствует каждый "
            "другой импульс, её устойчивость считывается с нормального спектра, а её сборка — "
            "релаксационная задача. Для N = 3 все эти ингредиенты — ровно то, что означает задача "
            "трёх тел в программе TRIVORTEX: три участника, парные взаимодействия, коллективное "
            "равновесие и хореография движения. Волоконный лазер лишь заменяет гравитацию или "
            "циркуляцию вихрей на экспоненциально-косинусный закон, управляемый фазой."
        ),
        (
            "В рамках программы это исследование — оптический якорь семейства хореографий. Оно "
            "проверяет в условиях, где «прохождение друг сквозь друга» физично, а не сингулярно, ту "
            "же структурную последовательность, что используется везде в TRIVORTEX: аналитический "
            "парный закон, коллективное равновесие, линеаризованный спектр, сохранение инварианта. "
            "Синхронизованный триплет — оптический брат лагранжева треугольника теоремы 3.1, а сжатие "
            "s* ниже r₀ — спектральный брат коллективного силового баланса, фиксирующего "
            "равностороннюю конфигурацию."
        ),
    ],
    "derivation_en": [
        (
            "The reduced model starts from the pair interaction. Overlapping soliton envelopes in the "
            "anomalous-dispersion fiber exchange energy and momentum through the Kerr term; keeping "
            "the leading tail-overlap terms gives the Gordon–Mollenauer potential (E1): a repulsive "
            "exponential core C₁e^(−2r/L) and an attractive overlap C₂e^(−r/L) whose strength is "
            "modulated by cos 2Δφ. The sign of the force therefore follows the phase: attraction for "
            "|Δφ| < π/4, repulsion beyond, and exact cancellation of the attractive term at Δφ = π/4 "
            "— the binding threshold. The pair equilibrium solves F(r₀, Δφ) = 0 and yields the "
            "closed form r₀ = L·ln(2C₁/(C₂ cos 2Δφ)); at the preset Δφ = 0 it is ln(4/3)."
        ),
        (
            "The three-body structure enters through the all-pairs chain dynamics (E3). Soliton tails "
            "act at any separation and solitons pass through one another, so the equations are "
            "invariant under particle exchange and the physically meaningful geometry of a "
            "configuration is read from the sorted positions. For the symmetric molecule with "
            "spacings (s, s) the end pulse feels the near pair F(s) and the far pair F(2s), giving "
            "the balance F(s*) + F(2s*) = 0. Because F(2s*) < 0 is attractive, the root s* is "
            "necessarily below the pair root r₀ — the chain is compressed by the third body. This is "
            "the same logical step that produces the collective geometry of the Lagrange triangle "
            "from pairwise Newtonian attraction."
        ),
        (
            "Small oscillations follow from the Hessian of the total potential in the spacing "
            "coordinates (d₁, d₂) with the center of mass removed; the kinetic energy is not diagonal "
            "in these coordinates, so the normal modes solve the generalized eigenproblem (E5) with "
            "mass matrix M_g = m·[[2/3, 1/3], [1/3, 2/3]]. At the preset spacing s* the two "
            "eigenfrequencies are 2.4536 and 2.9453 rad (cyclic 0.390507 and 0.468766); the higher "
            "one is the breathing mode in which the middle pulse moves against the outer pair. The "
            "same Hessian evaluated along the phase sweep softens continuously to zero at the "
            "binding threshold, providing the stability map of the molecule."
        ),
    ],
    "derivation_ru": [
        (
            "Редуцированная модель начинается с парного взаимодействия. Перекрывающиеся огибающие "
            "солитонов в волокне с аномальной дисперсией обмениваются энергией и импульсом через "
            "керровский член; удержание главных членов перекрытия хвостов даёт потенциал "
            "Гордона–Молленауэра (E1): отталкивающее экспоненциальное ядро C₁e^(−2r/L) и "
            "притягивающее перекрытие C₂e^(−r/L), глубина которого модулируется множителем cos 2Δφ. "
            "Знак силы, следовательно, следует за фазой: притяжение при |Δφ| < π/4, отталкивание "
            "далее и точное сокращение притягивающего члена при Δφ = π/4 — пороге связывания. Парное "
            "равновесие решает F(r₀, Δφ) = 0 и даёт замкнутую форму r₀ = L·ln(2C₁/(C₂ cos 2Δφ)); в "
            "пресете Δφ = 0 это ln(4/3)."
        ),
        (
            "Трёхтельная структура входит через динамику цепочки со всеми парами (E3). Хвосты "
            "солитонов действуют на любом расстоянии, а солитоны проходят друг сквозь друга, поэтому "
            "уравнения инвариантны относительно перестановок частиц, и физически осмысленная "
            "геометрия конфигурации считывается с сортированных позиций. Для симметричной молекулы с "
            "расстояниями (s, s) концевой импульс чувствует ближнюю пару F(s) и дальнюю пару F(2s), "
            "откуда баланс F(s*) + F(2s*) = 0. Поскольку F(2s*) < 0 притягивает, корень s* "
            "обязательно лежит ниже парного корня r₀ — цепочка сжата третьим телом. Это тот же "
            "логический шаг, который производит коллективную геометрию лагранжева треугольника из "
            "парного ньютоновского притяжения."
        ),
        (
            "Малые колебания следуют из гессиана полного потенциала в координатах расстояний (d₁, d₂) "
            "при удалённом центре масс; кинетическая энергия в этих координатах не диагональна, "
            "поэтому нормальные моды решают обобщённую задачу на собственные значения (E5) с матрицей "
            "масс M_g = m·[[2/3, 1/3], [1/3, 2/3]]. В пресетном расстоянии s* две собственные "
            "частоты равны 2.4536 и 2.9453 рад (циклические 0.390507 и 0.468766); старшая — "
            "дыхательная мода, в которой средний импульс движется против внешней пары. Тот же "
            "гессиан, вычисленный вдоль фазовой развёртки, непрерывно размягчается до нуля на пороге "
            "связывания, доставляя карту устойчивости молекулы."
        ),
    ],
    "connection_en": (
        "The mapping to the TRIVORTEX core is structural, one-to-one and already "
        "visible in the equations. The three phase-locked pulses are the optical realization of "
        "the three agents of Theorem 3.1: a symmetric, phase-locked special solution of a "
        "three-body system, exactly as the rotating vortex triangle is the equal-circulation "
        "special solution of the vortex problem. The molecule spacing s* plays the role of the "
        "Lagrange-triangle side a: both are fixed not by a two-body law but by the requirement "
        "that every member be in equilibrium under the combined pull of the other two — "
        "F(s*) + F(2s*) = 0 here, the central-configuration equations there. The breathing mode "
        "ω₂ is the analog of the radial modulation of the choreography, and the phase difference "
        "Δφ controls binding exactly as the circulation ratio controls the vortex triangle: "
        "changing it moves the system through symmetric and asymmetric configurations until "
        "binding is lost (Δφ = π/4, the analog of leaving the stability island). The same "
        "exponential-cosine structure reappears in TRX-09 vortices and TRX-04 photon-fluid beams, "
        "which makes this study the reusable optical template of the program."
    ),
    "connection_ru": (
        "Соответствие ядру TRIVORTEX структурно, взаимно-однозначно и видно уже в "
        "уравнениях. Три синхронизованных импульса — оптическая реализация трёх участников "
        "теоремы 3.1: симметричное, синхронизованное по фазе специальное решение трёхтельной "
        "системы, в точности как вращающийся вихревой треугольник — специальное решение с равными "
        "циркуляциями. Расстояние в молекуле s* играет сторону лагранжева треугольника a: оба "
        "фиксируются не двухтельным законом, а требованием равновесия каждого участника под "
        "совместным действием двух других — здесь F(s*) + F(2s*) = 0, там уравнения центральной "
        "конфигурации. Дыхательная мода ω₂ — аналог радиальной модуляции хореографии, а разность "
        "фаз Δφ управляет связыванием так же, как отношение циркуляций управляет вихревым "
        "треугольником: её изменение проводит систему через симметричные и несимметричные "
        "конфигурации вплоть до потери связывания (Δφ = π/4 — аналог выхода из острова "
        "устойчивости). Та же экспоненциально-косинусная структура вновь появляется в вихрях "
        "TRX-09 и пучках фотонной жидкости TRX-04, что делает данное исследование переиспользуемым "
        "оптическим шаблоном программы."
    ),
    "method_en": [
        (
            "Equilibria are computed by bracketed root finding. The pair equilibrium solves F(r) = 0 "
            "and the chain equilibrium solves F(s) + F(2s) = 0, both by Brent's method with "
            "xtol = 1e-15 and machine-level rtol on sign-stable brackets; the numeric pair root "
            "agrees with the closed form ln(4/3) to 5.6e-17. The repulsive character of the "
            "anti-phase lock is established exhaustively rather than by sampling: the minimum of "
            "F(r, π/2) over the range r ∈ [0.05, 20] on a 4000-point grid is +6e-9 > 0, i.e. the "
            "force never turns attractive."
        ),
        (
            "Dynamics are integrated with the explicit Dormand–Prince 8(5,3) scheme (DOP853). The "
            "relaxation run starts from positions {1.0, 2.0, 3.5} with zero velocities under damping "
            "γ_d = 1.0 (overdamped, the Doppler-cooled regime of a mode-locked laser) and runs to "
            "T = 90 with rtol = 1e-11, atol = 1e-12 and max_step = 0.2. The conservative run holds "
            "γ_d = 0, displaces the middle pulse by +0.01 from the perfect molecule and integrates "
            "to T = 100 with rtol = atol = 1e-12 and max_step = 0.05, sampling 2000 points; the "
            "energy drift over the whole run is 1.776357e-15 against the 1e-10 acceptance tolerance."
        ),
        (
            "The breathing frequency is extracted twice, independently. Numerically, the "
            "middle-pulse displacement relative to the center of mass is Hann-windowed and Fourier-"
            "transformed; the spectral peak lies at f = 0.469765. Analytically, the generalized "
            "eigenproblem (E5) at s* gives cyclic modes 0.390507 and 0.468766; the measured peak "
            "matches the nearest analytic mode to 0.21 %, comfortably inside the 1 % acceptance "
            "tolerance. Every check stores its value, target, tolerance, unit and pass flag in the "
            "JSON protocol, so the study reproduces from a single command with no network access and "
            "no stochastic seeds."
        ),
    ],
    "method_ru": [
        (
            "Равновесия вычисляются методом скобок. Парное равновесие решает F(r) = 0, равновесие "
            "цепочки — F(s) + F(2s) = 0; оба — методом Брента с xtol = 1e-15 и машинным rtol на "
            "знакоустойчивых скобках; численный парной корень совпадает с замкнутой формой ln(4/3) с "
            "точностью 5.6e-17. Отталкивающий характер противофазной синхронизации установлен "
            "исчерпывающе, а не выборкой: минимум F(r, π/2) по диапазону r ∈ [0.05, 20] на сетке из "
            "4000 точек равен +6e-9 > 0, то есть сила нигде не становится притягивающей."
        ),
        (
            "Динамика интегрируется явной схемой Дормана–Принса 8(5,3) (DOP853). Релаксационный прогон "
            "стартует с позиций {1.0, 2.0, 3.5} с нулевыми скоростями при демпфировании γ_d = 1.0 "
            "(сверхвязкий, «доплер-охлаждаемый» режим лазера с синхронизацией мод) и идёт до T = 90 с "
            "rtol = 1e-11, atol = 1e-12 и max_step = 0.2. Консервативный прогон держит γ_d = 0, "
            "смещает средний импульс на +0.01 от идеальной молекулы и интегрирует до T = 100 с "
            "rtol = atol = 1e-12 и max_step = 0.05, снимая 2000 точек; дрейф энергии за весь прогон "
            "равен 1.776357e-15 против допуска 1e-10."
        ),
        (
            "Дыхательная частота извлекается дважды и независимо. Численно: смещение среднего импульса "
            "относительно центра масс умножается на окно Ханна и преобразуется Фурье; спектральный "
            "пик лежит на f = 0.469765. Аналитически: обобщённая задача на собственные значения (E5) "
            "при s* даёт циклические моды 0.390507 и 0.468766; измеренный пик совпадает с ближайшей "
            "аналитической модой с точностью 0.21 %, с запасом внутри допуска 1 %. Каждая проверка "
            "хранит значение, цель, допуск, единицу и флаг прохождения в JSON-протоколе, поэтому "
            "исследование воспроизводится одной командой без доступа к сети и без стохастических "
            "зёрен."
        ),
    ],
    "analysis_en": [
        (
            "**Equilibria.** The numeric pair root reproduces the closed form r₀ = L·ln(2C₁/C₂) = "
            "ln(4/3) ≈ 0.287682 to 5.6e-17 — machine zero. The exhaustive anti-phase test returns "
            "min F(r, π/2) = +6e-9 > 0 over r ∈ [0.05, 20], confirming that binding is controlled by "
            "the phase factor cos 2Δφ and disappears entirely at and beyond Δφ = π/4. The curvature "
            "of the well at the pair minimum is V″(r₀) = 2.25, which fixes the pair breathing scale "
            "√(3V″(r₀)) ≈ 2.5981 against which the chain spectrum is compared."
        ),
        (
            "**Molecule formation.** Under overdamped relaxation from {1.0, 2.0, 3.5}, the sorted "
            "spacings converge to d₁ = d₂ = 0.2018926516; their final mismatch is 2.2e-16 and their "
            "offset from the independently computed chain equilibrium s* = 0.2018926516 is 2.8e-17 — "
            "both machine-level, against tolerances of 1e-8 and 1e-6. The spacing sits 29.8 % below "
            "the pair value r₀ = 0.287682: the far pair F(2s) pulls the molecule together, a clean, "
            "quantified three-body effect visible in fig02."
        ),
        (
            "**Stability map.** Sweeping the locking phase Δφ from 0 to 0.75 rad shows both "
            "equilibria diverging as the binding threshold π/4 ≈ 0.7854 is approached: s* grows from "
            "0.201893 through 0.719380 (Δφ = 0.5 rad) to 2.885 (Δφ = 0.75 rad). The chain modes "
            "soften in the same direction, from 2.4536 and 2.9453 rad at the preset to 0.1092 and "
            "0.1982 rad at the far end of the sweep — the soft-mode behavior expected as the well "
            "flattens into pure repulsion (fig03)."
        ),
        (
            "**Breathing and invariants.** The conservative molecule breathes stably over T = 100 "
            "(fig04a) with total energy conserved to 1.776357e-15 — five orders of magnitude inside "
            "the 1e-10 tolerance. The FFT spectrum of the middle-pulse displacement peaks at "
            "f = 0.469765 against the analytic Hessian modes 0.468766 and 0.390507 (fig04b): "
            "agreement 0.21 %, an order of magnitude inside the 1 % acceptance tolerance. The "
            "dynamics, the spectrum and the Hessian thus triangulate the same breathing physics from "
            "three independent directions."
        ),
    ],
    "analysis_ru": [
        (
            "**Равновесия.** Численный парной корень воспроизводит замкнутую форму r₀ = L·ln(2C₁/C₂) = "
            "ln(4/3) ≈ 0.287682 с точностью 5.6e-17 — машинный нуль. Исчерпывающий противофазный тест "
            "возвращает min F(r, π/2) = +6e-9 > 0 по r ∈ [0.05, 20], подтверждая, что связывание "
            "управляется фазовым множителем cos 2Δφ и полностью исчезает при и за пределами "
            "Δφ = π/4. Кривизна ямы в парном минимуме V″(r₀) = 2.25 фиксирует парной дыхательный "
            "масштаб √(3V″(r₀)) ≈ 2.5981, с которым сравнивается цепочечный спектр."
        ),
        (
            "**Сборка молекулы.** При сверхвязкой релаксации из {1.0, 2.0, 3.5} сортированные "
            "расстояния сходятся к d₁ = d₂ = 0.2018926516; конечное расхождение между ними 2.2e-16, а "
            "отклонение от независимо вычисленного равновесия цепочки s* = 0.2018926516 — 2.8e-17: "
            "оба на машинном уровне, против допусков 1e-8 и 1e-6. Расстояние лежит на 29.8 % ниже "
            "парного значения r₀ = 0.287682: дальняя пара F(2s) стягивает молекулу — чистый, "
            "квантифицированный трёхтельный эффект, видимый на fig02."
        ),
        (
            "**Карта устойчивости.** Развёртка фазы синхронизации Δφ от 0 до 0.75 рад показывает "
            "расхождение обоих равновесий при приближении к порогу связывания π/4 ≈ 0.7854: s* растёт "
            "от 0.201893 через 0.719380 (Δφ = 0.5 рад) до 2.885 (Δφ = 0.75 рад). Цепочечные моды "
            "размягчаются в том же направлении — от 2.4536 и 2.9453 рад в пресете до 0.1092 и "
            "0.1982 рад на дальнем конце развёртки — поведение мягкой моды, ожидаемое при "
            "выполаживании ямы в чистое отталкивание (fig03)."
        ),
        (
            "**Дыхание и инварианты.** Консервативная молекула стабильно дышит на протяжении T = 100 "
            "(fig04a), а полная энергия сохраняется до 1.776357e-15 — на пять порядков внутри допуска "
            "1e-10. Спектр Фурье смещения среднего импульса имеет пик на f = 0.469765 против "
            "аналитических гессиановских мод 0.468766 и 0.390507 (fig04b): согласие 0.21 %, на "
            "порядок внутри допуска 1 %. Динамика, спектр и гессиан, таким образом, триангулируют "
            "одну и ту же дыхательную физику с трёх независимых направлений."
        ),
    ],
    "discussion_en": [
        (
            "The reduced model is deliberately minimal: point-like pulses, a pair potential without "
            "retardation or gain dynamics, and damping treated as a switchable term. Within these "
            "assumptions every conclusion is an exact statement about the governing equations rather "
            "than a simulation of a specific laser. The natural extensions — third-order dispersion "
            "and self-frequency shift (which make the force asymmetric and non-conservative), "
            "continuous cw backgrounds, larger molecules N > 3 with defect modes, and full NLSE "
            "integration of the same scenario — each preserve the verification style established "
            "here."
        ),
        (
            "The parameter regime covers the generic regime of the Gordon–Mollenauer law rather than "
            "a specific cavity: C₁/C₂ = 2/3 places the pair well at r₀ ≈ 0.29 tail lengths with "
            "depth 0.25, comfortably resolved on the integration grid. The phase sweep deliberately "
            "approaches the binding threshold Δφ = π/4, where the equilibrium diverges and the "
            "Hessian develops a zero mode; exactly at threshold the brentq brackets fail, which the "
            "sweep code reports as a hard boundary rather than hiding with a regularized formula. "
            "Realistic cavities would add noise-driven phase diffusion, slowly destroying the lock — "
            "a physics question outside the conservative scope of this study."
        ),
        (
            "Within the program, this study feeds TRX-04, which lifts the pair interaction into the "
            "transverse plane and recovers a rotating Lagrange triangle of beams in the Kerr photon "
            "fluid; TRX-08, which exchanges optical pulses for laser-cooled ions and reproduces the "
            "same spacing/breathing structure with a Coulomb tail; and TRX-09, the fluid-dynamical "
            "anchor where phases become circulations. Together with the celestial block (TRX-01, "
            "TRX-11) they demonstrate that the choreography sequence — pair law, collective "
            "equilibrium, normal spectrum, invariant — is portable across optics, fluids and "
            "celestial mechanics."
        ),
    ],
    "discussion_ru": [
        (
            "Редуцированная модель сознательно минимальна: точечные импульсы, парный потенциал без "
            "запаздывания и динамики усиления, демпфирование в виде переключаемого члена. В этих "
            "допущениях каждый вывод — точное утверждение об определяющих уравнениях, а не "
            "симуляция конкретного лазера. Естественные расширения — дисперсия третьего порядка и "
            "самосдвиг частоты (делающие силу несимметричной и неконсервативной), непрерывные cw-"
            "фоны, более крупные молекулы N > 3 с дефектными модами и полное интегрирование НУШ для "
            "того же сценария — каждое сохраняет установленный здесь верификационный стиль."
        ),
        (
            "Диапазон параметров покрывает общий режим закона Гордона–Молленауэра, а не конкретный "
            "резонатор: C₁/C₂ = 2/3 помещает парную яму на r₀ ≈ 0.29 длины хвоста глубиной 0.25, с "
            "запасом разрешённой на сетке интегрирования. Фазовая развёртка сознательно подходит к "
            "порогу связывания Δφ = π/4, где равновесие расходится, а гессиан приобретает нулевую "
            "моду; точно на пороге скобки brentq перестают существовать, и код развёртки сообщает об "
            "этом как о жёсткой границе, а не прячет за регуляризованной формулой. Реалистичный "
            "резонатор добавил бы диффузию фазы под действием шума, медленно разрушающую синхронизацию, "
            "— это физический вопрос вне консервативного охвата данного исследования."
        ),
        (
            "В рамках программы это исследование питает TRX-04, переносящее парное взаимодействие в "
            "поперечную плоскость и получающее вращающийся лагранжев треугольник пучков в керровской "
            "фотонной жидкости; TRX-08, заменяющее оптические импульсы лазерно-охлаждёнными ионами и "
            "воспроизводящее ту же структуру «расстояние/дыхание» с кулоновским хвостом; и TRX-09 — "
            "гидродинамический якорь, где фазы становятся циркуляциями. Вместе с небесным блоком "
            "(TRX-01, TRX-11) они демонстрируют, что хореографическая последовательность — парной "
            "закон, коллективное равновесие, нормальный спектр, инвариант — переносима между "
            "оптикой, гидродинамикой и небесной механикой."
        ),
    ],
    "conclusions_en": [
        "The pair binding law is exact: the numeric equilibrium reproduces r₀ = L·ln(2C₁/C₂) = ln(4/3) ≈ 0.287682 to 5.6e-17.",
        "Binding is a phase-selection effect: the anti-phase lock Δφ = π/2 is purely repulsive over r ∈ [0.05, 20] (min force +6e-9 > 0), and the well exists only for |Δφ| < π/4.",
        "A random triplet relaxes into an equally spaced molecule: d₁ = d₂ = 0.2018926516 with mismatch 2.2e-16 and offset from the analytic chain equilibrium s* only 2.8e-17.",
        "The molecule is compressed 29.8 % below the pair spacing by the far-pair attraction (F(s*) + F(2s*) = 0) — a quantified genuine three-body effect.",
        "The conservative molecule is a clean invariant system: energy drift 1.8e-15 over t = 100 at DOP853 rtol = atol = 1e-12.",
        "The breathing spectrum is verified: FFT peak f = 0.469765 against the Hessian mode 0.468766 (agreement 0.21 %, tolerance 1 %), and the phase sweep yields the full stability map with both modes softening to zero at Δφ = π/4.",
    ],
    "conclusions_ru": [
        "Парной закон связывания точен: численное равновесие воспроизводит r₀ = L·ln(2C₁/C₂) = ln(4/3) ≈ 0.287682 с точностью 5.6e-17.",
        "Связывание — эффект выбора фазы: противофазная синхронизация Δφ = π/2 чисто отталкивающая на r ∈ [0.05, 20] (мин. сила +6e-9 > 0), а яма существует лишь при |Δφ| < π/4.",
        "Случайный триплет релаксирует в равноотстоящую молекулу: d₁ = d₂ = 0.2018926516 с расхождением 2.2e-16 и отклонением от аналитического равновесия цепочки s* всего 2.8e-17.",
        "Молекула сжата на 29.8 % ниже парного расстояния притяжением дальней пары (F(s*) + F(2s*) = 0) — квантифицированный подлинный трёхтельный эффект.",
        "Консервативная молекула — чистая инвариантная система: дрейф энергии 1.8e-15 за t = 100 при DOP853 rtol = atol = 1e-12.",
        "Дыхательный спектр верифицирован: пик Фурье f = 0.469765 против гессиановской моды 0.468766 (согласие 0.21 %, допуск 1 %), а фазовая развёртка даёт полную карту устойчивости с размягчением обеих мод до нуля при Δφ = π/4.",
    ],
    "references": [
        '1. Zabusky, N. J., Kruskal, M. D. (1965). *Interaction of "solitons" in a collisionless plasma and the recurrence of initial states.* Phys. Rev. Lett. 15, 240–243.',
        "2. Hasegawa, A., Tappert, F. (1973). *Transmission of stationary nonlinear optical pulses in dispersive dielectric fibers. I. Anomalous dispersion.* Appl. Phys. Lett. 23, 142–144.",
        "3. Mollenauer, L. F., Stolen, R. H., Gordon, J. P. (1980). *Experimental observation of picosecond pulse narrowing and solitons in optical fibers.* Phys. Rev. Lett. 45, 1095–1098.",
        "4. Karpman, V. I., Solov'ev, V. V. (1981). *A perturbational approach to the two-soliton systems with third-order dispersion.* Physica D 3, 487–502.",
        "5. Gordon, J. P. (1983). *Interaction forces among solitons in optical fibers.* Optics Letters 8, 596–598.",
        "6. Malomed, B. A. (1991). *Multistability and cyclic dynamics of solitons in dispersive media.* Phys. Rev. A 44, 6954.",
        "7. Stratmann, M., Pagel, T., Mitschke, F. (2005). *Experimental observation of temporal soliton molecules.* Phys. Rev. Lett. 95, 143902.",
        "8. Herink, G., Kurtz, F., Jalali, B., Solli, D. R., Ropers, C. (2017). *Real-time spectral interferometry probes the internal dynamics of femtosecond soliton molecules.* Science 356, 50–54.",
    ],
    "crosslinks_en": [
        "* **TRX-04** lifts the pair interaction into the transverse plane (Kerr photon fluid) and recovers a rotating Lagrange beam triangle.",
        "* **TRX-08** exchanges optical pulses for laser-cooled ions — the same spacing/breathing structure with a Coulomb tail.",
        "* **TRX-09** is the fluid-dynamical anchor with circulations instead of phases (Kirchhoff–Chaplygin vortex pair/triplet).",
    ],
    "crosslinks_ru": [
        "* **TRX-04** переносит парное взаимодействие в поперечную плоскость (керровская фотонная жидкость) и получает вращающийся лагранжев треугольник пучков.",
        "* **TRX-08** заменяет оптические импульсы лазерно-охлаждёнными ионами — та же структура «расстояние/дыхание» с кулоновским хвостом.",
        "* **TRX-09** — гидродинамический якорь с циркуляциями вместо фаз (вихревая пара/триплет Кирхгофа–Чаплыгина).",
    ],
    "assumptions_en": [
        "Point-particle reduction: pulses are described by positions and phases only; their shape is assumed rigid (fundamental solitons).",
        "The pair interaction is conservative and instantaneous; retardation, third-order dispersion and self-frequency shift are neglected.",
        "Phase locking Δφ = 0 is imposed as the operating point; the sweep treats Δφ as a static parameter, not a dynamical variable.",
        "Equal pulses: identical amplitude, mass m = 1 and tail length L for all three members.",
        "Damping is a switchable linear term (γ_d = 1 relaxation, γ_d = 0 conservative); no noise-driven phase diffusion is modeled.",
        "Solitons pass through one another; molecular geometry is therefore judged by sorted positions.",
    ],
    "assumptions_ru": [
        "Точечно-частичное приближение: импульсы описываются только позициями и фазами; их форма считается жёсткой (фундаментальные солитоны).",
        "Парное взаимодействие консервативно и мгновенно; запаздывание, дисперсия третьего порядка и самосдвиг частоты не учитываются.",
        "Синхронизация фаз Δφ = 0 задана как рабочая точка; развёртка трактует Δφ как статический параметр, а не динамическую переменную.",
        "Одинаковые импульсы: равные амплитуда, масса m = 1 и длина хвоста L у всех трёх участников.",
        "Демпфирование — переключаемый линейный член (γ_d = 1 релаксация, γ_d = 0 консервативный режим); шумовая диффузия фазы не моделируется.",
        "Солитоны проходят друг сквозь друга; поэтому геометрия молекулы оценивается по сортированным позициям.",
    ],
    "glance_en": [
        ["Block", "Laser optics — study 03 of 12"],
        [
            "Model",
            "three-pulse chain with phase-dependent exponential pair potential (C₁ = 2, C₂ = 3, L = 1)",
        ],
        ["Key invariant", "total energy of the conservative molecule (drift 1.8e-15)"],
        [
            "Headline result",
            "molecule at s* = 0.2018927 — 29.8 % below the pair r₀ = ln(4/3) ≈ 0.287682",
        ],
        ["Verification", "6/6 checks PASS (full mode)"],
        ["Runtime", "1.2 s full · 4.7 s with figures · < 20 s smoke"],
    ],
    "glance_ru": [
        ["Блок", "Лазерная оптика — исследование 03 из 12"],
        [
            "Модель",
            "цепочка трёх импульсов с фазозависимым экспоненциальным парным потенциалом (C₁ = 2, C₂ = 3, L = 1)",
        ],
        ["Ключевой инвариант", "полная энергия консервативной молекулы (дрейф 1.8e-15)"],
        [
            "Главный результат",
            "молекула на s* = 0.2018927 — на 29.8 % ниже парного r₀ = ln(4/3) ≈ 0.287682",
        ],
        ["Верификация", "6/6 проверок PASS (полный режим)"],
        ["Время выполнения", "1.2 с полный · 4.7 с с графиками · < 20 с smoke"],
    ],
    "glossary": {
        "header_en": ["Term", "Definition"],
        "header_ru": ["Термин", "Определение"],
        "rows_en": [
            [
                "Soliton molecule",
                "a bound state of several solitons held by tail-overlap forces, with fixed internal spacing",
            ],
            [
                "Phase locking Δφ",
                "constant phase difference between pulses; Δφ = 0 binds, π/2 repels",
            ],
            [
                "Evanescent tail L",
                "exponential decay length of the soliton overlap; the length unit of the study",
            ],
            [
                "Pair potential V(r, Δφ)",
                "Gordon–Mollenauer law: repulsive core C₁e^(−2r/L) plus phase-gated attraction",
            ],
            ["Pair equilibrium r₀", "root of F(r) = 0; r₀ = L·ln(2C₁/C₂) = ln(4/3) at Δφ = 0"],
            ["Chain equilibrium s*", "symmetric three-pulse spacing: root of F(s) + F(2s) = 0"],
            ["Three-body compression", "s* < r₀ because the far pair attracts; here 29.8 %"],
            [
                "Breathing mode",
                "normal oscillation in which the middle pulse moves against the outer pair",
            ],
            [
                "Generalized eigenproblem",
                "H v = ω² M_g v with the non-diagonal spacing-coordinate mass matrix",
            ],
            [
                "Overdamped relaxation",
                "assembly under strong damping γ_d = 1, the Doppler-cooled analog for lasers",
            ],
        ],
        "rows_ru": [
            [
                "Солитонная молекула",
                "связанное состояние нескольких солитонов, удерживаемое силами перекрытия хвостов, с фиксированным внутренним расстоянием",
            ],
            [
                "Синхронизация фаз Δφ",
                "постоянная разность фаз между импульсами; Δφ = 0 связывает, π/2 отталкивает",
            ],
            [
                "Эванесцентный хвост L",
                "экспоненциальная длина затухания перекрытия солитонов; единица длины исследования",
            ],
            [
                "Парный потенциал V(r, Δφ)",
                "закон Гордона–Молленауэра: отталкивающее ядро C₁e^(−2r/L) плюс притяжение, управляемое фазой",
            ],
            ["Парное равновесие r₀", "корень F(r) = 0; r₀ = L·ln(2C₁/C₂) = ln(4/3) при Δφ = 0"],
            [
                "Равновесие цепочки s*",
                "симметричное расстояние трёх импульсов: корень F(s) + F(2s) = 0",
            ],
            ["Трёхтельное сжатие", "s* < r₀ из-за притяжения дальней пары; здесь 29.8 %"],
            [
                "Дыхательная мода",
                "нормальное колебание, в котором средний импульс движется против внешней пары",
            ],
            [
                "Обобщённая задача на собственные значения",
                "H v = ω² M_g v с недиагональной матрицей масс в координатах расстояний",
            ],
            [
                "Сверхвязкая релаксация",
                "сборка при сильном демпфировании γ_d = 1, «доплер-охлаждающий» аналог для лазеров",
            ],
        ],
    },
    "notation": {
        "header_en": ["Symbol", "Meaning"],
        "header_ru": ["Символ", "Смысл"],
        "rows_en": [
            ["x_k", "position of pulse k on the cavity axis"],
            ["r", "pair separation"],
            ["Δφ", "phase difference between adjacent pulses"],
            ["V, F", "pair potential and pair force (F = −∂V/∂r)"],
            ["C₁, C₂", "exponential coefficients of the potential (2 and 3)"],
            ["L", "evanescent-tail length (length unit)"],
            ["m", "pulse mass (kinetic coefficient)"],
            ["γ_d", "damping coefficient (1.0 relaxation, 0 conservative)"],
            ["r₀, s*", "pair equilibrium and chain equilibrium spacing"],
            ["H, M_g", "Hessian of the chain potential and mass matrix in spacing coordinates"],
            ["ω_i, f", "angular and cyclic normal-mode frequencies"],
        ],
        "rows_ru": [
            ["x_k", "позиция импульса k на оси резонатора"],
            ["r", "парное расстояние"],
            ["Δφ", "разность фаз соседних импульсов"],
            ["V, F", "парный потенциал и парная сила (F = −∂V/∂r)"],
            ["C₁, C₂", "экспоненциальные коэффициенты потенциала (2 и 3)"],
            ["L", "длина эванесцентного хвоста (единица длины)"],
            ["m", "масса импульса (кинетический коэффициент)"],
            ["γ_d", "коэффициент демпфирования (1.0 релаксация, 0 консервативный режим)"],
            ["r₀, s*", "парное равновесие и равновесное расстояние цепочки"],
            ["H, M_g", "гессиан потенциала цепочки и матрица масс в координатах расстояний"],
            ["ω_i, f", "угловые и циклические частоты нормальных мод"],
        ],
    },
    "params_appendix": {
        "header_en": ["Symbol", "Value", "Role"],
        "header_ru": ["Символ", "Значение", "Роль"],
        "rows_en": [
            ["C₁, C₂", "2, 3", "potential coefficients: core repulsion / tail attraction"],
            ["L", "1", "tail length; unit of all lengths"],
            ["m", "1", "pulse mass; unit of mass"],
            ["Δφ", "0 (preset); sweep 0 … 0.75 rad", "locking phase; binding threshold π/4"],
            ["r₀", "ln(4/3) ≈ 0.287682", "pair equilibrium at Δφ = 0"],
            ["s*", "0.2018926516", "chain equilibrium, root of F(s) + F(2s) = 0"],
            ["V″(r₀)", "2.25", "curvature of the pair well at the minimum"],
            ["relaxation", "{1.0, 2.0, 3.5}, γ_d = 1, T = 90", "assembly run, DOP853 rtol = 1e-11"],
            [
                "conservative run",
                "+0.01 on the middle pulse, γ_d = 0, T = 100",
                "breathing run, DOP853 rtol = atol = 1e-12",
            ],
            [
                "chain modes",
                "2.4536, 2.9453 rad (0.390507, 0.468766 cyclic)",
                "normal-mode spectrum at s*",
            ],
        ],
        "rows_ru": [
            ["C₁, C₂", "2, 3", "коэффициенты потенциала: отталкивание ядра / притяжение хвостов"],
            ["L", "1", "длина хвоста; единица всех длин"],
            ["m", "1", "масса импульса; единица массы"],
            [
                "Δφ",
                "0 (пресет); развёртка 0 … 0.75 рад",
                "фаза синхронизации; порог связывания π/4",
            ],
            ["r₀", "ln(4/3) ≈ 0.287682", "парное равновесие при Δφ = 0"],
            ["s*", "0.2018926516", "равновесие цепочки, корень F(s) + F(2s) = 0"],
            ["V″(r₀)", "2.25", "кривизна парной ямы в минимуме"],
            [
                "релаксация",
                "{1.0, 2.0, 3.5}, γ_d = 1, T = 90",
                "сборочный прогон, DOP853 rtol = 1e-11",
            ],
            [
                "консервативный прогон",
                "+0.01 среднему импульсу, γ_d = 0, T = 100",
                "дыхательный прогон, DOP853 rtol = atol = 1e-12",
            ],
            [
                "цепочечные моды",
                "2.4536, 2.9453 рад (0.390507, 0.468766 циклические)",
                "спектр нормальных мод при s*",
            ],
        ],
    },
    "bibtex": [
        "@article{gordon1983,",
        "  author  = {Gordon, J. P.},",
        "  title   = {Interaction forces among solitons in optical fibers},",
        "  journal = {Optics Letters},",
        "  year    = {1983}, volume = {8}, pages = {596--598}}",
        "",
        "@article{karpman1981,",
        "  author  = {Karpman, V. I. and Solov'ev, V. V.},",
        "  title   = {A perturbational approach to the two-soliton systems with third-order dispersion},",
        "  journal = {Physica D},",
        "  year    = {1981}, volume = {3}, pages = {487--502}}",
        "",
        "@article{stratmann2005,",
        "  author  = {Stratmann, M. and Pagel, T. and Mitschke, F.},",
        "  title   = {Experimental observation of temporal soliton molecules},",
        "  journal = {Physical Review Letters},",
        "  year    = {2005}, volume = {95}, pages = {143902}}",
        "",
        "@article{herink2017,",
        "  author  = {Herink, G. and Kurtz, F. and Jalali, B. and Solli, D. R. and Ropers, C.},",
        "  title   = {Real-time spectral interferometry probes the internal dynamics of femtosecond soliton molecules},",
        "  journal = {Science},",
        "  year    = {2017}, volume = {356}, pages = {50--54}}",
    ],
}
