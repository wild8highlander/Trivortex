# -*- coding: utf-8 -*-
"""Content pack for TRX-02 (v1.0.0 Monograph Edition). Rendered by scripts/build_study_docs.py."""

PACK = {
    "meta": {
        "study_id": "TRX-02",
        "dir_name": "TRX-02-three-wave-mixing",
        "title_en": "Resonant Three-Wave Interaction (Manley–Rowe, χ⁽²⁾ Optics)",
        "title_ru": "Резонансное трёхволновое взаимодействие (Мэнли–Роу, χ⁽²⁾-оптика)",
        "script": "trx02_three_wave_mixing.py",
        "results_json": "trx02_results.json",
        "scheme_file": "scheme_trx02.svg",
        "runtime_full": "0.6 s",
    },
    "essence_en": (
        "Resonant three-wave mixing in a lossless, phase-matched χ⁽²⁾ crystal — the "
        'canonical "three-body problem of nonlinear optics". A pump wave at ω₃ = ω₁ + ω₂ '
        "exchanges photons with a signal–idler pair; the Manley–Rowe relations keep the photon "
        "bookkeeping exact, and the equal-coupling amplitude equations are canonically equivalent "
        "to the Euler top — the same integrable family as the Kirchhoff three-vortex problem that "
        "underlies Theorem 3.1 of TRIVORTEX."
    ),
    "essence_ru": (
        "Резонансное трёхволновое взаимодействие в кристалле χ⁽²⁾ без потерь и с "
        "идеальным фазовым согласованием — каноническая «задача трёх тел нелинейной оптики». "
        "Волна накачки на частоте ω₃ = ω₁ + ω₂ обменивается фотонами с парой «сигнал — холостая "
        "волна»; соотношения Мэнли–Роу ведут точную фотонную бухгалтерию, а уравнения амплитуд с "
        "равными связями канонически эквивалентны волчку Эйлера — тому же интегрируемому семейству, "
        "что и задача Кирхгофа о трёх вихрях, лежащая в основе теоремы 3.1 TRIVORTEX."
    ),
    "mission_en": [
        (
            "Optical parametric processes are, photon-for-photon, a three-body problem: one pump "
            "photon is converted into a signal photon and an idler photon, and the three complex "
            "amplitudes obey first-order equations whose exact invariants are the optical "
            "Manley–Rowe relations. TRIVORTEX is built on an integrable triad — three vortices with "
            "quadratic conservation laws — so the resonant three-wave system is its optical twin: "
            "the same structure of quadratic invariants, the same periodic choreography, the same "
            "Euler-top backbone. This study establishes that correspondence quantitatively, on the "
            "shared ground of machine-precision verification rather than analogy alone."
        ),
        (
            "The study verifies four things to machine precision: that the Manley–Rowe invariants "
            "hold to ≤ 5.3e-15 over fifty time units of full pump depletion and revival; that the "
            "exchange is exactly periodic with a repeatable period T_ex = 5.650961242 (consecutive "
            "periods agreeing to 8.7e-8); that the pump collapses to 6.3e-5 of its flux — genuine "
            "full depletion, 99.994% of the peak removed — and revives with error 2.4e-15; and that "
            "the degenerate channel reproduces the textbook closed form η(t) = tanh²(At) to "
            "2.2e-16 — a closed-form anchor in the same spirit as the closed form of Theorem 3.1."
        ),
    ],
    "mission_ru": [
        (
            "Оптические параметрические процессы — это, фотон-за-фотоном, задача трёх тел: один "
            "фотон накачки превращается в фотон сигнала и фотон холостой волны, а три комплексные "
            "амплитуды подчиняются уравнениям первого порядка, точные инварианты которых — оптические "
            "соотношения Мэнли–Роу. TRIVORTEX построен на интегрируемой триаде — трёх вихрях с "
            "квадратичными законами сохранения, — поэтому резонансная трёхволновая система является "
            "его оптическим близнецом: та же структура квадратичных инвариантов, та же периодическая "
            "хореография, тот же остов волчка Эйлера. Данное исследование устанавливает это "
            "соответствие количественно — на общем грунте верификации с машинной точностью, а не "
            "только по аналогии."
        ),
        (
            "Исследование проверяет четыре вещи с машинной точностью: что инварианты Мэнли–Роу "
            "выполняются на уровне ≤ 5.3e-15 на протяжении пятидесяти единиц времени полного "
            "истощения и возрождения накачки; что обмен строго периодичен с повторяющимся периодом "
            "T_ex = 5.650961242 (соседние периоды совпадают с точностью 8.7e-8); что накачка "
            "проседает до 6.3e-5 своего потока — подлинное полное истощение, снято 99.994% пика — и "
            "возрождается с ошибкой 2.4e-15; и что вырожденный канал воспроизводит учебниковую "
            "замкнутую формулу η(t) = tanh²(At) с точностью 2.2e-16 — якорь в виде замкнутого "
            "решения в том же духе, что и замкнутая форма теоремы 3.1."
        ),
    ],
    "physics_en": [
        (
            "The physical system is a χ⁽²⁾ nonlinear crystal (e.g. MgO:LiNbO₃) supporting three "
            "collinear plane waves: the pump at ω₃, the signal at ω₁ and the idler at ω₂, with the "
            "resonance conditions ω₃ = ω₁ + ω₂ (energy matching) and k₃ = k₁ + k₂, i.e. Δk = 0 "
            "(momentum matching). In the photon picture the nonlinear polarization converts one "
            "pump photon into a signal–idler pair and back; in the classical picture the three "
            "complex amplitudes are coupled by the second-order susceptibility and exchange flux "
            "while the medium itself stays passive and lossless."
        ),
        (
            "With equal normalized couplings the flux exchange becomes the exact optical image of "
            "torque-free rigid-body rotation (the Euler top): the photon fluxes |a_k|² play the role "
            "of squared angular-momentum components, the Manley–Rowe invariants fix the invariant "
            "planes, and the trajectory is a closed periodic cycle on their intersection. The pump "
            "empties into the signal–idler pair and refills again — the exchange period T_ex is the "
            "period of that choreography — and the degenerate channel a₁ = a₂ (second-harmonic "
            "generation) reduces to a one-line closed form used as the verification anchor."
        ),
    ],
    "physics_ru": [
        (
            "Физическая система — нелинейный кристалл χ⁽²⁾ (например, MgO:LiNbO₃), в котором "
            "распространяются три коллинеарные плоские волны: накачка на ω₃, сигнал на ω₁ и холостая "
            "волна на ω₂ с резонансными условиями ω₃ = ω₁ + ω₂ (согласование энергий) и "
            "k₃ = k₁ + k₂, то есть Δk = 0 (согласование импульсов). На фотонном языке нелинейная "
            "поляризация превращает один фотон накачки в пару «сигнал — холостая волна» и обратно; "
            "на классическом языке три комплексные амплитуды связаны восприимчивостью второго порядка "
            "и обмениваются потоком, оставаясь в пассивной среде без потерь."
        ),
        (
            "При равных нормированных связях обмен потоком становится точным оптическим образом "
            "вращения свободного твёрдого тела (волчок Эйлера): потоки фотонов |a_k|² играют роль "
            "квадратов компонент момента импульса, инварианты Мэнли–Роу фиксируют инвариантные "
            "плоскости, а траектория — замкнутый периодический цикл на их пересечении. Накачка "
            "выливается в пару «сигнал — холостая волна» и вновь наполняется — период обмена T_ex и "
            "есть период этой хореографии, — а вырожденный канал a₁ = a₂ (генерация второй гармоники) "
            "сводится к однострочной замкнутой формуле, служащей верификационным якорем."
        ),
    ],
    "preset_table": {
        "header_en": ["Parameter", "Value", "Meaning"],
        "header_ru": ["Параметр", "Значение", "Смысл"],
        "rows_en": [
            ["a₁(0), a₂(0)", "0.2, 0.3 (real)", "signal and idler seed amplitudes"],
            ["a₃(0)", "1.0·i (phase π/2)", "pump seed; phase chosen so Im(Z) ≠ 0"],
            ["couplings γ₁, γ₂, γ₃", "1, 1, 1 (normalized)", "equal lossless χ⁽²⁾ coupling"],
            ["phase matching", "Δk = 0", "perfect collinear matching, no detuning"],
            ["integration", "T = 50, DOP853, rtol = atol = 1e-13", "max_step 0.02, dense output"],
            ["SHG channel", "s(0) = A = 1, p(0) = 0", "degenerate limit for the tanh² anchor"],
        ],
        "rows_ru": [
            [
                "a₁(0), a₂(0)",
                "0.2, 0.3 (вещественные)",
                "затравочные амплитуды сигнала и холостой волны",
            ],
            ["a₃(0)", "1.0·i (фаза π/2)", "затравка накачки; фаза выбрана так, что Im(Z) ≠ 0"],
            [
                "коэффициенты связи γ₁, γ₂, γ₃",
                "1, 1, 1 (нормированные)",
                "равная связь, среда без потерь",
            ],
            [
                "фазовое согласование",
                "Δk = 0",
                "идеальное коллинеарное согласование, без расстройки",
            ],
            [
                "интегрирование",
                "T = 50, DOP853, rtol = atol = 1e-13",
                "max_step 0.02, плотный вывод",
            ],
            ["SHG-канал", "s(0) = A = 1, p(0) = 0", "вырожденный предел для эталона tanh²"],
        ],
    },
    "equations": [
        {
            "id": "E1",
            "latex": "\\frac{da_1}{dt} = i\\,a_2^{*}a_3, \\qquad \\frac{da_2}{dt} = i\\,a_1^{*}a_3, \\qquad \\frac{da_3}{dt} = i\\,a_1 a_2",
            "desc_en": "Resonant three-wave amplitude equations (equal couplings, Δk = 0)",
            "desc_ru": "Резонансные уравнения трёх волн (равные связи, Δk = 0)",
        },
        {
            "id": "E2",
            "latex": "I_1 = |a_1|^2 + |a_3|^2, \\qquad I_2 = |a_2|^2 + |a_3|^2, \\qquad I_3 = |a_1|^2 - |a_2|^2",
            "desc_en": "Manley–Rowe invariants (photon-pair bookkeeping)",
            "desc_ru": "Инварианты Мэнли–Роу (фотонная бухгалтерия пар)",
        },
        {
            "id": "E3",
            "latex": "\\eta(t) = \\tanh^2(At), \\qquad s = A\\,\\mathrm{sech}(At), \\qquad p = iA\\,\\tanh(At)",
            "desc_en": "Degenerate (SHG) channel: closed-form plane-wave conversion",
            "desc_ru": "Вырожденный (SHG) канал: замкнутая формула плосковолновой конверсии",
        },
    ],
    "scheme_cap_en": (
        "TRX-02 scheme — resonant three-wave mixing: a pump wave (ω₃, k₃) enters a "
        "lossless phase-matched χ⁽²⁾ crystal and exchanges photons with the signal (ω₁, k₁) and "
        "idler (ω₂, k₂) waves; energy and momentum matching close the resonance, and the "
        "Manley–Rowe relations keep the photon bookkeeping exact."
    ),
    "scheme_cap_ru": (
        "Схема TRX-02 — резонансное трёхволновое взаимодействие: волна накачки "
        "(ω₃, k₃) входит в кристалл χ⁽²⁾ без потерь и с фазовым согласованием и обменивается "
        "фотонами с волнами сигнала (ω₁, k₁) и холостой (ω₂, k₂); согласование энергий и импульсов "
        "замыкает резонанс, а соотношения Мэнли–Роу ведут точную фотонную бухгалтерию."
    ),
    "scheme_walk_en": [
        [
            "Pump wave",
            "gold sinusoid (ω₃, k₃, amplitude a₃) entering the crystal; its flux |a₃|² depletes into the pair and revives periodically",
        ],
        [
            "χ⁽²⁾ crystal",
            "lossless, perfectly phase-matched (Δk = 0) medium; inside it one pump photon splits into a signal–idler pair",
        ],
        [
            "Signal / idler waves",
            "blue and green sinusoids (ω₁, k₁) and (ω₂, k₂) leaving the crystal, seeded by a₁(0) = 0.2 and a₂(0) = 0.3",
        ],
        [
            "Energy matching",
            "ω₃ = ω₁ + ω₂: one pump photon ↔ one signal + one idler (down-conversion and its reverse, SFG)",
        ],
        [
            "Momentum matching",
            "k₃ = k₁ + k₂ in the co-propagating geometry, so Δk = 0 and the coupling accumulates over the medium",
        ],
        [
            "Manley–Rowe bookkeeping",
            "I₁ = |a₁|² + |a₃|², I₂ = |a₂|² + |a₃|², I₃ = |a₁|² − |a₂|² stay constant — the optical twin of vortex circulation bookkeeping",
        ],
    ],
    "scheme_walk_ru": [
        [
            "Волна накачки",
            "золотая синусоида (ω₃, k₃, амплитуда a₃) входит в кристалл; её поток |a₃|² выливается в пару и периодически возрождается",
        ],
        [
            "Кристалл χ⁽²⁾",
            "среда без потерь с идеальным фазовым согласованием (Δk = 0); внутри неё один фотон накачки распадается на пару «сигнал — холостая волна»",
        ],
        [
            "Сигнал / холостая волна",
            "синяя и зелёная синусоиды (ω₁, k₁) и (ω₂, k₂) на выходе из кристалла с затравками a₁(0) = 0.2 и a₂(0) = 0.3",
        ],
        [
            "Согласование энергий",
            "ω₃ = ω₁ + ω₂: один фотон накачки ↔ одна пара «сигнал + холостая» (параметрическая расщепка и обратная генерация суммарной частоты)",
        ],
        [
            "Согласование импульсов",
            "k₃ = k₁ + k₂ в сонаправленной геометрии, поэтому Δk = 0 и связь накапливается по всей длине среды",
        ],
        [
            "Бухгалтерия Мэнли–Роу",
            "I₁ = |a₁|² + |a₃|², I₂ = |a₂|² + |a₃|², I₃ = |a₁|² − |a₂|² постоянны — оптический близнец бухгалтерии циркуляций в вихрях",
        ],
    ],
    "mapping": {
        "header_en": ["Quantity in this study", "TRIVORTEX analog", "Comment"],
        "header_ru": ["Величина исследования", "Аналог в TRIVORTEX", "Комментарий"],
        "rows_en": [
            [
                "Three complex amplitudes a₁, a₂, a₃",
                "three vortices Γ₁, Γ₂, Γ₃",
                "both are integrable triads with quadratic invariants",
            ],
            [
                "Manley–Rowe invariants I₁, I₂, I₃",
                "vortex integrals H, P, Q, I",
                "quadratic conservation laws that fix the orbit",
            ],
            [
                "Pump depletion / revival cycle T_ex",
                "choreographic exchange of the vortex triangle",
                'periodic circulation of the "energy" around the triad',
            ],
            [
                "Euler-top equivalence",
                "Kirchhoff three-vortex equivalence",
                "the same integrable family; shared elliptic solutions",
            ],
            [
                "SHG closed form tanh²(At)",
                "closed form of Theorem 3.1",
                "an exact solution anchoring the numerics",
            ],
        ],
        "rows_ru": [
            [
                "Три комплексные амплитуды a₁, a₂, a₃",
                "три вихря Γ₁, Γ₂, Γ₃",
                "обе триады интегрируемы с квадратичными инвариантами",
            ],
            [
                "Инварианты Мэнли–Роу I₁, I₂, I₃",
                "интегралы вихрей H, P, Q, I",
                "квадратичные законы сохранения, закрепляющие орбиту",
            ],
            [
                "Цикл истощения/возрождения накачки T_ex",
                "хореографический обмен вихревого треугольника",
                "периодическая циркуляция «энергии» по триаде",
            ],
            [
                "Эквивалентность волчку Эйлера",
                "эквивалентность Кирхгофа для трёх вихрей",
                "одно интегрируемое семейство; общие эллиптические решения",
            ],
            [
                "Замкнутая форма SHG tanh²(At)",
                "замкнутая форма теоремы 3.1",
                "точное решение, заякоривающее численную схему",
            ],
        ],
    },
    "nondim_en": (
        "Time is measured in units of 1/(γA₀) with equal coupling γ and pump scale A₀; "
        "amplitudes are normalized so that |a_k|² is the photon-flux bookkeeping variable. "
        "Physical units map back through the standard χ⁽²⁾ coupled-wave normalization "
        "(Boyd, *Nonlinear Optics*, ch. 2); all results below are stated in these "
        "dimensionless units."
    ),
    "nondim_ru": (
        "Время измеряется в единицах 1/(γA₀) при равной связи γ и масштабе накачки A₀; "
        "амплитуды нормированы так, что |a_k|² — учётная переменная потока фотонов. Физические "
        "единицы восстанавливаются стандартной нормировкой связанных волн для χ⁽²⁾ "
        "(Boyd, *Nonlinear Optics*, гл. 2); все результаты ниже приведены в этих "
        "безразмерных единицах."
    ),
    "checks": {
        "header_en": ["Check", "Target", "Tolerance"],
        "header_ru": ["Проверка", "Цель", "Допуск"],
        "rows_en": [
            ["Drift of I₁ = |a₁|² + |a₃|² over t ∈ [0, 50]", "0", "1e-10"],
            ["Drift of I₂ = |a₂|² + |a₃|² over t ∈ [0, 50]", "0", "1e-10"],
            ["Drift of I₃ = |a₁|² − |a₂|² over t ∈ [0, 50]", "0", "1e-10"],
            ["Repeatability |T_ex,2 − T_ex,1| of the exchange period", "0", "1e-6"],
            ["Pump revival error |a₃(T_ex)|² − |a₃(0)|²", "0", "1e-8"],
            ["Full depletion: min |a₃|² < 5% of its peak", "yes", "exact"],
            ["SHG conversion vs η(t) = tanh²(At)", "0", "1e-8"],
        ],
        "rows_ru": [
            ["Дрейф I₁ = |a₁|² + |a₃|² на t ∈ [0, 50]", "0", "1e-10"],
            ["Дрейф I₂ = |a₂|² + |a₃|² на t ∈ [0, 50]", "0", "1e-10"],
            ["Дрейф I₃ = |a₁|² − |a₂|² на t ∈ [0, 50]", "0", "1e-10"],
            ["Повторяемость периода обмена |T_ex,2 − T_ex,1|", "0", "1e-6"],
            ["Ошибка возрождения накачки |a₃(T_ex)|² − |a₃(0)|²", "0", "1e-8"],
            ["Полное истощение: min |a₃|² < 5% пика", "да", "точно"],
            ["SHG-конверсия против η(t) = tanh²(At)", "0", "1e-8"],
        ],
    },
    "figure_caps": {
        "fig01_resonance_geometry.png": {
            "cap_en": "Overview of the model: resonance geometry of the wave triad and the initial photon-flux bookkeeping.",
            "cap_ru": "Обзор модели: резонансная геометрия триады волн и начальная фотонная бухгалтерия потоков.",
            "walk_en": "Panel (a) shows the photon-energy diagram of the resonant triad: the pump photon at ω₃ = ω₁ + ω₂ splits into a signal–idler pair (down-conversion) with the reverse sum-frequency channel; panel (b) stacks the initial fluxes |a₁|² = 0.04, |a₂|² = 0.09, |a₃|² = 1.00 into the Manley–Rowe pairs I₁ = 1.04 and I₂ = 1.09.",
            "walk_ru": "Панель (a) показывает фотонно-энергетическую диаграмму резонансной триады: фотон накачки при ω₃ = ω₁ + ω₂ распадается на пару «сигнал — холостая волна» (параметрическая расщепка) с обратным каналом суммарной частоты; панель (b) складывает начальные потоки |a₁|² = 0.04, |a₂|² = 0.09, |a₃|² = 1.00 в пары Мэнли–Роу I₁ = 1.04 и I₂ = 1.09.",
        },
        "fig02_pump_depletion.png": {
            "cap_en": "Headline result: periodic pump depletion and revival over T = 50, with one exchange cycle enlarged.",
            "cap_ru": "Главный результат: периодическое истощение и возрождение накачки на T = 50 с увеличенным циклом обмена.",
            "walk_en": "Over T = 50 the pump makes about 8.8 full cycles (T_ex = 5.650961242): it collapses to |a₃|² = 6.3e-5 — 99.994% of its peak 1.04 removed — and revives with error 2.4e-15; the zoom shows the refined maxima and the exchange period arrow.",
            "walk_ru": "За T = 50 накачка совершает около 8.8 полных циклов (T_ex = 5.650961242): она проседает до |a₃|² = 6.3e-5 — снято 99.994% пика 1.04 — и возрождается с ошибкой 2.4e-15; на увеличении видны уточнённые максимумы и стрелка периода обмена.",
        },
        "fig03_parameter_sweep.png": {
            "cap_en": "Parameter sweep over the initial pump amplitude |a₃(0)| ∈ [0.4, 2.0]: exchange period and depletion depth.",
            "cap_ru": "Развёртка по начальной амплитуде накачки |a₃(0)| ∈ [0.4, 2.0]: период обмена и глубина истощения.",
            "walk_en": "Across 17 runs (T = 50, rtol = 1e-10) the exchange period decreases monotonically from 9.028821 to 3.556606, while the depletion depth min/max of |a₃|² stays below 5.2e-6 — every regime of the sweep is pumped to essentially complete conversion.",
            "walk_ru": "По 17 прогонам (T = 50, rtol = 1e-10) период обмена монотонно убывает от 9.028821 до 3.556606, а глубина истощения min/max величины |a₃|² не превышает 5.2e-6 — весь диапазон развёртки прокачан до практически полной конверсии.",
        },
        "fig04_invariants_shg.png": {
            "cap_en": "Dynamics diagnostics: Manley–Rowe residuals along the orbit and the SHG closed-form comparison.",
            "cap_ru": "Диагностика динамики: остатки Мэнли–Роу вдоль орбиты и сравнение с замкнутой формулой SHG.",
            "walk_en": "The invariant residuals stay at the 1e-15 level (max 5.3e-15 against the 1e-10 tolerance), and the degenerate channel tracks η(t) = tanh²(At) to 2.220446e-16 — one unit in the last place of double precision.",
            "walk_ru": "Остатки инвариантов держатся на уровне 1e-15 (максимум 5.3e-15 против допуска 1e-10), а вырожденный канал следует за η(t) = tanh²(At) с точностью 2.220446e-16 — одна единица последнего разряда двойной точности.",
        },
    },
    "results_block": [
        "ManleyRowe_I13_drift                = 5.329071e-15   (tol 1e-10)",
        "ManleyRowe_I23_drift                = 4.218847e-15   (tol 1e-10)",
        "ManleyRowe_I12diff_drift            = 4.496403e-15   (tol 1e-10)",
        "Pump_period_repeatability           = 8.743724e-08   (T_ex1=5.650961242, T_ex2=5.650961155)",
        "Pump_revival_error                  = 2.442491e-15   (tol 1e-8)",
        "Pump_full_depletion_occurs          = PASS (pump drops below 5% of its peak)",
        "SHG_tanh2_conversion_error          = 2.220446e-16   (tol 1e-8)",
        "status: PASS (7/7)",
    ],
    "abstract_en": (
        "This monograph treats the resonant three-wave interaction in a lossless, "
        "perfectly phase-matched χ⁽²⁾ crystal — the canonical three-body problem of nonlinear "
        "optics. Three complex amplitudes (pump, signal, idler) obey the equal-coupling amplitude "
        "equations, a Hamiltonian system canonically equivalent to the Euler top and hence to the "
        "Kirchhoff three-vortex problem at the core of TRIVORTEX. The study verifies the "
        "integrable structure to machine precision: over T = 50 — roughly 8.8 full exchange "
        "cycles — the Manley–Rowe invariants drift by at most 5.329071e-15, more than four "
        "orders below the "
        "1e-10 acceptance tolerance; the exchange is exactly periodic with T_ex = 5.650961242, "
        "consecutive periods agreeing to 8.7e-8; the pump undergoes genuine full depletion, "
        "collapsing to |a₃|² = 6.3e-5 (99.994% of its peak 1.04 removed) and reviving with error "
        "2.4e-15; and the degenerate channel reproduces the closed-form conversion law "
        "η(t) = tanh²(At) to 2.220446e-16 — one unit in the last place of double precision. A "
        "sweep over the initial pump amplitude shows the exchange period monotonically tunable "
        "from 9.03 to 3.56. All seven acceptance checks pass."
    ),
    "abstract_ru": (
        "Монография посвящена резонансному трёхволновому взаимодействию в кристалле "
        "χ⁽²⁾ без потерь и с идеальным фазовым согласованием — канонической задаче трёх тел "
        "нелинейной оптики. Три комплексные амплитуды (накачка, сигнал, холостая волна) подчиняются "
        "уравнениям с равными связями — гамильтоновой системе, канонически эквивалентной волчку "
        "Эйлера и, следовательно, задаче Кирхгофа о трёх вихрях, составляющей ядро TRIVORTEX. "
        "Исследование верифицирует интегрируемую структуру с машинной точностью: за T = 50 — около "
        "8.8 полных циклов обмена — инварианты Мэнли–Роу дрейфуют не более чем на 5.329071e-15, "
        "более чем на четыре порядка ниже допуска 1e-10; обмен строго периодичен с T_ex = 5.650961242, "
        "соседние периоды совпадают с точностью 8.7e-8; накачка испытывает подлинное полное "
        "истощение, проседая до |a₃|² = 6.3e-5 (снято 99.994% пика 1.04) и возрождаясь с ошибкой "
        "2.4e-15; вырожденный канал воспроизводит замкнутый закон конверсии η(t) = tanh²(At) с "
        "точностью 2.220446e-16 — одна единица последнего разряда двойной точности. Развёртка по "
        "начальной амплитуде накачки показывает монотонную перестройку периода обмена от 9.03 до "
        "3.56. Все семь контрольных проверок проходят."
    ),
    "intro_en": [
        (
            "The story begins with the laser itself: in 1961 Franken, Hill, Peters and Weinreich "
            "observed second-harmonic generation — light emerging from a quartz crystal at exactly "
            "twice the ruby laser frequency — and founded nonlinear optics. Within a year, Armstrong, "
            "Bloembergen, Ducuing and Pershan (1962) wrote down the coupled-wave equations that "
            "remain the working language of the field, and Kroll (1962) proposed parametric "
            "amplification in extended media. The first optical parametric oscillator of Giordmaine "
            "and Miller (1965) in LiNbO₃ turned the three-wave interaction into a practical, tunable "
            "light source, a role parametric devices still play today."
        ),
        (
            "The conservation laws of the field are older than the optical realization. Manley and "
            "Rowe (1956) derived their general energy relations for nonlinear elements in the "
            "microwave era, and they transfer verbatim to optics: combinations of the photon fluxes "
            "in the interacting waves stay constant. In the resonant three-wave system these "
            "Manley–Rowe relations are not merely bookkeeping — they are the exact invariants that "
            "make the dynamics integrable, the direct analogue of the circulation integrals of "
            "ideal-fluid vortex motion."
        ),
        (
            "The integrability itself became a classical subject. Kaup, Reiman and Bers (1979) "
            "systematized the space-time evolution of nonlinear three-wave interactions in their "
            "Reviews of Modern Physics survey, exhibiting the soliton solutions and the reduction of "
            "the system to integrable canonical forms; the equal-coupling case is canonically "
            "equivalent to the Euler top, the torque-free rigid body. Modern relevance is easy to "
            "list: optical parametric oscillators and amplifiers, squeezed-light sources for "
            "gravitational-wave detectors, terahertz generation and frequency-comb technology all "
            "run on precisely this three-wave engine."
        ),
        (
            "For TRIVORTEX the relevance is structural. The program's core is an integrable triad — "
            "three Kirchhoff vortices with quadratic conservation laws and a periodic choreography "
            "(Theorem 3.1, with its closed form). The resonant three-wave system is that triad's "
            "optical twin: quadratic invariants (Manley–Rowe), a periodic choreography (pump "
            "depletion and revival with period T_ex), and a closed-form anchor (the tanh² law of "
            "second-harmonic generation). Verifying this twin to machine precision is the natural "
            "second step of the program, immediately after the celestial twin of TRX-01."
        ),
    ],
    "intro_ru": [
        (
            "История начинается с самого лазера: в 1961 году Франкен, Хилл, Питерс и Вайнрайх "
            "наблюдали генерацию второй гармоники — свет, выходящий из кварцевого кристалла ровно на "
            "удвоенной частоте рубинового лазера, — и основали нелинейную оптику. Уже через год "
            "Армстронг, Блумберген, Дюкюэн и Першан (1962) записали уравнения связанных волн, которые "
            "до сих пор остаются рабочим языком области, а Кролл (1962) предложил параметрическое "
            "усиление в протяжённых средах. Первый оптический параметрический генератор Джордмейна и "
            "Миллера (1965) на LiNbO₃ превратил трёхволновое взаимодействие в практический "
            "перестраиваемый источник света — роль, которую параметрические приборы играют и сегодня."
        ),
        (
            "Законы сохранения этой области старше её оптической реализации. Мэнли и Роу (1956) "
            "вывели свои общие энергетические соотношения для нелинейных элементов ещё в "
            "микроволновую эпоху, и на оптику они переносятся дословно: комбинации потоков фотонов во "
            "взаимодействующих волнах остаются постоянными. В резонансной трёхволновой системе "
            "соотношения Мэнли–Роу — не просто бухгалтерия: это точные инварианты, делающие динамику "
            "интегрируемой, прямой аналог интегралов циркуляции вихревого движения идеальной "
            "жидкости."
        ),
        (
            "Сама интегрируемость стала классической темой. Кауп, Рейман и Берс (1979) "
            "систематизировали пространственно-временную эволюцию нелинейных трёхволновых "
            "взаимодействий в обзоре Reviews of Modern Physics, выписав солитонные решения и сведение "
            "системы к интегрируемым каноническим формам; случай равных связей канонически "
            "эквивалентен волчку Эйлера — свободному вращению твёрдого тела. Современная значимость "
            "перечисляется легко: оптические параметрические генераторы и усилители, источники "
            "сжатого света для гравитационно-волновых детекторов, генерация терагерца и технология "
            "частотных гребёнок работают ровно на этом трёхволновом двигателе."
        ),
        (
            "Для TRIVORTEX значимость структурна. Ядро программы — интегрируемая триада: три вихря "
            "Кирхгофа с квадратичными законами сохранения и периодической хореографией (теорема 3.1 "
            "с её замкнутой формой). Резонансная трёхволновая система — оптический близнец этой "
            "триады: квадратичные инварианты (Мэнли–Роу), периодическая хореография (истощение и "
            "возрождение накачки с периодом T_ex) и якорь в виде замкнутого решения (закон tanh² "
            "генерации второй гармоники). Верификация этого близнеца с машинной точностью — "
            "естественный второй шаг программы, сразу вслед за небесным близнецом TRX-01."
        ),
    ],
    "derivation_en": [
        (
            "Starting from Maxwell's equations with the second-order nonlinear polarization "
            "P_NL = ε₀χ⁽²⁾E², one inserts the three monochromatic waves and applies the "
            "slowly-varying-envelope approximation. Under perfect phase matching Δk = 0 the "
            "backward and third-order terms drop, and after the standard flux normalization each "
            "wave is described by a complex amplitude a_k with |a_k|² proportional to the photon "
            "flux; the coupling strengths become equal integers that scale out to 1. The result is "
            "the resonant system (E1), which is Hamiltonian with energy "
            "H = a₁a₂a₃* + a₁*a₂*a₃ — the optical image of a rigid body whose rotation axes are "
            "exchanged one photon pair at a time."
        ),
        (
            "The invariants (E2) follow by direct substitution: differentiating |a₁|² + |a₃|² with "
            "the equations (E1) gives 2Re(a₁*·ia₂*a₃) + 2Re(a₃*·ia₁a₂), and since a₃*a₁a₂ is the "
            "conjugate of a₁a₂a₃* the two terms cancel identically — likewise for I₂ and I₃. "
            "Geometrically, the trajectory is confined to the intersection of three invariant "
            "surfaces in the six real-dimensional amplitude space, which reduces the dynamics to a "
            "single periodic degree of freedom: closed orbits, exact period T_ex, and no chaos."
        ),
        (
            "The degenerate channel fixes a₁ = a₂ = s and a₃ = p. The system collapses to "
            "ds/dt = i p s*, dp/dt = i s² with the single invariant |s|² + |p|² = const, and with "
            "s(0) = A, p(0) = 0 it integrates in elementary functions to "
            "s = A sech(At), p = iA tanh(At), giving the plane-wave conversion law η = tanh²(At) of "
            "(E3). This closed form plays the role of the exact anchor: any integrator, coupling "
            "normalization or phase convention must reproduce it, and the study uses it exactly so."
        ),
    ],
    "derivation_ru": [
        (
            "Отправляясь от уравнений Максвелла с нелинейной поляризацией второго порядка "
            "P_NL = ε₀χ⁽²⁾E², подставляем три монохроматические волны и применяем приближение "
            "медленно меняющихся огибающих. При идеальном фазовом согласовании Δk = 0 обратные волны "
            "и члены третьего порядка выпадают, а после стандартной нормировки потоков каждая волна "
            "описывается комплексной амплитудой a_k, где |a_k|² пропорционален потоку фотонов; "
            "коэффициенты связи становятся равными целыми числами, которые масштабом сводятся к "
            "единице. Получается резонансная система (E1) — гамильтонова, с энергией "
            "H = a₁a₂a₃* + a₁*a₂*a₃: оптический образ твёрдого тела, меняющего оси вращения по одному "
            "фотонному паре за раз."
        ),
        (
            "Инварианты (E2) следуют прямой подстановкой: дифференцируя |a₁|² + |a₃|² по уравнениям "
            "(E1), получаем 2Re(a₁*·ia₂*a₃) + 2Re(a₃*·ia₁a₂), а поскольку a₃*a₁a₂ сопряжено к "
            "a₁a₂a₃*, члены сокращаются тождественно — аналогично для I₂ и I₃. Геометрически "
            "траектория удерживается на пересечении трёх инвариантных поверхностей в "
            "шестимерном вещественном пространстве амплитуд, что сводит динамику к одной периодической "
            "степени свободы: замкнутые орбиты, точный период T_ex и никакого хаоса."
        ),
        (
            "Вырожденный канал фиксирует a₁ = a₂ = s, a₃ = p. Система сворачивается к "
            "ds/dt = i p s*, dp/dt = i s² с единственным инвариантом |s|² + |p|² = const, а при "
            "s(0) = A, p(0) = 0 интегрируется в элементарных функциях: s = A sech(At), "
            "p = iA tanh(At), откуда плосковолновый закон конверсии η = tanh²(At) формулы (E3). Эта "
            "замкнутая форма играет роль точного якоря: любой интегратор, нормировка связи или "
            "фазовая конвенция обязаны её воспроизводить — исследование использует её именно так."
        ),
    ],
    "connection_en": (
        "The mapping to TRIVORTEX is one-to-one at the structural level. The three "
        "complex amplitudes form an integrable triad exactly as three Kirchhoff vortices do: the "
        "Manley–Rowe relations I₁, I₂, I₃ play the role of the vortex integrals H, P, Q, I, the "
        "periodic pump depletion–revival cycle is the optical choreography that mirrors the "
        "vortex triangle's rotation, and the Euler-top equivalence of the equal-coupling case is "
        "the same integrable family that gives the Kirchhoff problem its elliptic solutions. "
        "Even the verification style is shared: the tanh² law anchors the numerics with a closed "
        "form, in the same spirit as the closed form of Theorem 3.1, and the photon-pair "
        "bookkeeping of the Manley–Rowe relations is the precise optical analogue of circulation "
        "bookkeeping in the vortex model. TRX-02 therefore serves as the optics-side twin of the "
        "program core and feeds the Kerr extension (TRX-04), the vortex verification (TRX-09) and "
        "the radiating three-body dynamics (TRX-11)."
    ),
    "connection_ru": (
        "Соответствие TRIVORTEX взаимно-однозначно на структурном уровне. Три "
        "комплексные амплитуды образуют интегрируемую триаду в точности как три вихря Кирхгофа: "
        "соотношения Мэнли–Роу I₁, I₂, I₃ играют роль интегралов вихрей H, P, Q, I, периодический "
        "цикл «истощение — возрождение» накачки — это оптическая хореография, зеркальная вращению "
        "вихревого треугольника, а эквивалентность случая равных связей волчку Эйлера относит "
        "обе задачи к одному интегрируемому семейству, дарящему кирхгофовской задаче её "
        "эллиптические решения. Общим оказывается и стиль верификации: закон tanh² заякоривает "
        "численную схему замкнутой формой — в том же духе, что и замкнутая форма теоремы 3.1, а "
        "фотонная бухгалтерия пар в соотношениях Мэнли–Роу — точный оптический аналог бухгалтерии "
        "циркуляций в вихревой модели. Поэтому TRX-02 служит оптическим близнецом ядра программы и "
        "питает керровское расширение (TRX-04), вихревую верификацию (TRX-09) и динамику трёх тел "
        "с излучением (TRX-11)."
    ),
    "method_en": [
        (
            "The three complex amplitudes are split into six real ODEs (real and imaginary parts) "
            "and integrated with an explicit Dormand–Prince 8(5,3) scheme at rtol = atol = 1e-13, "
            "max_step = 0.02, over t ∈ [0, 50] with dense output. The Manley–Rowe invariants are "
            "evaluated pointwise on 2500 samples along the trajectory, and their maximal excursion "
            "from the initial values (I₁ = 1.04, I₂ = 1.09, I₃ = −0.05) is recorded as the drift "
            "check; the same dense solution supplies the photon-flux series used by the figures."
        ),
        (
            "The exchange period is extracted from the pump flux |a₃|²: local maxima are detected "
            "on a dense grid of 20001 samples, then refined by bounded scalar minimization with "
            "xatol = 1e-13. Two consecutive refined maxima give T_ex1 = 5.650961242 and "
            "T_ex2 = 5.650961155 — repeatability 8.7e-8 against the 1e-6 tolerance — and the flux "
            "at those maxima differs by 2.4e-15 (the revival check). Full depletion is tested "
            "against the 5% threshold: the pump minimum on the dense grid reaches 6.3e-5 of the "
            "peak flux 1.04."
        ),
        (
            "The degenerate channel is integrated at the same tolerance from s(0) = 1, p(0) = 0 and "
            "compared with η(t) = tanh²(At) on 60 points over t ∈ [0.05, 3]; the maximal deviation "
            "is the SHG check. The fig03 parameter sweep (17 initial pump amplitudes in "
            "[0.4, 2.0], T = 50, rtol = 1e-10) is computed only in --figures mode and stored in the "
            "figures block of the JSON protocol. Every check stores value, target, tolerance, unit "
            "and pass flag; runs are deterministic, need no network access and no random seeds."
        ),
    ],
    "method_ru": [
        (
            "Три комплексные амплитуды расщепляются на шесть вещественных ОДУ (вещественные и "
            "мнимые части) и интегрируются явной схемой Дормана–Принса 8(5,3) с rtol = atol = 1e-13, "
            "max_step = 0.02 на t ∈ [0, 50] с плотным выводом. Инварианты Мэнли–Роу вычисляются "
            "поточечно на 2500 выборках вдоль траектории, а их максимальное отклонение от начальных "
            "значений (I₁ = 1.04, I₂ = 1.09, I₃ = −0.05) записывается как проверка дрейфа; то же "
            "плотное решение поставляет ряды потоков фотонов для рисунков."
        ),
        (
            "Период обмена извлекается из потока накачки |a₃|²: локальные максимумы находятся на "
            "плотной сетке из 20001 выборки и уточняются ограниченной одномерной минимизацией с "
            "xatol = 1e-13. Два соседних уточнённых максимума дают T_ex1 = 5.650961242 и "
            "T_ex2 = 5.650961155 — повторяемость 8.7e-8 при допуске 1e-6, — а потоки в этих "
            "максимумах различаются на 2.4e-15 (проверка возрождения). Полное истощение проверяется "
            "против порога 5%: минимум накачки на плотной сетке достигает 6.3e-5 от пикового потока "
            "1.04."
        ),
        (
            "Вырожденный канал интегрируется с тем же допуском из s(0) = 1, p(0) = 0 и сравнивается "
            "с η(t) = tanh²(At) на 60 точках по t ∈ [0.05, 3]; максимальное отклонение — SHG-проверка. "
            "Развёртка для fig03 (17 начальных амплитуд накачки в [0.4, 2.0], T = 50, rtol = 1e-10) "
            "вычисляется только в режиме --figures и сохраняется в блок figures JSON-протокола. "
            "Каждая проверка хранит значение, цель, допуск, единицу и флаг прохождения; прогоны "
            "детерминированы, без доступа к сети и без случайных зёрен."
        ),
    ],
    "analysis_en": [
        (
            "**Invariants.** Over the full run T = 50 (about 8.8 exchange cycles) the Manley–Rowe "
            "drifts are 5.329071e-15 for I₁, 4.218847e-15 for I₂ and 4.496403e-15 for I₃ — more "
            "than four orders of magnitude below the 1e-10 acceptance tolerance and at the round-off level of "
            "double precision. The orbit is therefore exactly confined to the intersection of the "
            "invariant surfaces, which is the geometric content of integrability for the three-wave "
            "triad."
        ),
        (
            "**Periodic exchange.** The pump flux oscillates with the refined exchange period "
            "T_ex = 5.650961242; consecutive periods agree to 8.743724e-08, and the flux at successive "
            "maxima reproduces itself to 2.442491e-15. Between maxima the pump collapses to "
            "|a₃|² = 6.32941e-05 — 99.994% of its peak value 1.04 removed — so the cycle is a genuine "
            "full-depletion–revival choreography, not a shallow modulation."
        ),
        (
            "**Parameter sweep.** Sweeping the initial pump amplitude over [0.4, 2.0] in 17 runs, "
            "the exchange period decreases monotonically from 9.028821 to 3.556606: stronger pumps "
            "exchange photons faster. The depletion depth (min/max of |a₃|² over each run) stays "
            "between 4.2e-10 and 5.2e-6 across the whole grid — every regime of the sweep reaches "
            "essentially complete conversion, and the sweep invariant drift (≤ 1.5e-9 at the looser "
            "sweep tolerance 1e-10) confirms that the map itself is clean."
        ),
        (
            "**Closed-form anchor.** In the degenerate channel the numerical conversion efficiency "
            "follows η(t) = tanh²(At) with maximal deviation 2.220446e-16 over the 60 sample points — "
            "one unit in the last place of double precision. The exact solution validates the "
            "normalization, the phase convention and the integrator in one shot; it is the optical "
            "counterpart of anchoring the vortex choreography on the closed form of Theorem 3.1."
        ),
    ],
    "analysis_ru": [
        (
            "**Инварианты.** За полный прогон T = 50 (около 8.8 циклов обмена) дрейфы Мэнли–Роу "
            "составляют 5.329071e-15 для I₁, 4.218847e-15 для I₂ и 4.496403e-15 для I₃ — более чем "
            "на четыре порядка ниже допуска 1e-10 и на уровне округления двойной точности. Орбита, таким "
            "образом, точно удерживается на пересечении инвариантных поверхностей — в этом "
            "геометрическое содержание интегрируемости трёхволновой триады."
        ),
        (
            "**Периодический обмен.** Поток накачки колеблется с уточнённым периодом обмена "
            "T_ex = 5.650961242; соседние периоды совпадают с точностью 8.743724e-08, а поток в "
            "последовательных максимумах воспроизводится с точностью 2.442491e-15. Между максимумами "
            "накачка проседает до |a₃|² = 6.32941e-05 — снято 99.994% пикового значения 1.04, — так "
            "что цикл представляет собой подлинную хореографию «полное истощение — возрождение», а не "
            "мелкую модуляцию."
        ),
        (
            "**Развёртка параметров.** При развёртке начальной амплитуды накачки по [0.4, 2.0] в 17 "
            "прогонах период обмена монотонно убывает от 9.028821 до 3.556606: более сильная накачка "
            "обменивается фотонами быстрее. Глубина истощения (min/max величины |a₃|² в каждом "
            "прогоне) держится между 4.2e-10 и 5.2e-6 по всей сетке — каждый режим развёртки достигает "
            "практически полной конверсии, а дрейф инвариантов развёртки (≤ 1.5e-9 при более слабом "
            "допуске прогонов 1e-10) подтверждает чистоту самой карты."
        ),
        (
            "**Якорь в виде замкнутой формы.** В вырожденном канале численная эффективность конверсии "
            "следует за η(t) = tanh²(At) с максимальным отклонением 2.220446e-16 на 60 выборках — одна "
            "единица последнего разряда двойной точности. Точное решение одним выстрелом проверяет "
            "нормировку, фазовую конвенцию и интегратор; это оптический аналог заякоривания вихревой "
            "хореографии на замкнутой форме теоремы 3.1."
        ),
    ],
    "discussion_en": [
        (
            "The model is deliberately minimal: equal couplings, plane waves, perfect phase matching "
            "and no losses. Within these assumptions every conclusion is an exact statement about "
            "the governing equations rather than a simulation of a specific crystal. The natural "
            "extensions each preserve the verification style established here: detuning (Δk ≠ 0 adds "
            "a linear phase term and breaks the strict periodicity), group-velocity mismatch for "
            "pulses, unequal couplings (the asymmetric Euler top), cavity boundary conditions "
            "(the driven OPO), and quantum seeding by spontaneous parametric down-conversion."
        ),
        (
            "The numerical regime is stated honestly. The verification numbers come exclusively from "
            "rtol = atol = 1e-13 runs; the fig03 sweep uses the looser 1e-10 because the deep pump "
            "minima are sharp features that dominate integration cost, and its outputs are stored as "
            "figure data rather than acceptance checks. Physical units map back through the standard "
            "χ⁽²⁾ normalization (for MgO:LiNbO₃, |χ⁽²⁾| ≈ 4 pm/V at 1 µm), so T_ex can be translated "
            "into a crystal length once the input intensities are fixed."
        ),
        (
            "Within the program, this study anchors the integrable-triad block of the optics line: "
            "TRX-04 extends the pair interaction to spatial Kerr solitons (the soliton molecule), "
            "TRX-09 verifies the vortex twin of the same integrable family, and TRX-11 keeps the "
            "Hamiltonian three-body core but adds radiation. Together with TRX-01 and TRX-12 they "
            "close the loop between the celestial, the optical and the vortex formulations of "
            "TRIVORTEX."
        ),
    ],
    "discussion_ru": [
        (
            "Модель сознательно минимальна: равные связи, плоские волны, идеальное фазовое "
            "согласование, отсутствие потерь. В этих допущениях каждый вывод — точное утверждение об "
            "определяющих уравнениях, а не симуляция конкретного кристалла. Естественные расширения "
            "сохраняют установленный здесь верификационный стиль: расстройка (Δk ≠ 0 добавляет "
            "линейный фазовый член и ломает строгую периодичность), рассогласование групповых "
            "скоростей для импульсов, неравные связи (несимметричный волчок Эйлера), граничные "
            "условия резонатора (параметрический генератор с накачкой) и квантовое затравливание "
            "спонтанным параметрическим рассеянием."
        ),
        (
            "Численный режим указан честно. Верификационные числа получены исключительно при "
            "rtol = atol = 1e-13; развёртка fig03 использует более слабый допуск 1e-10, поскольку "
            "глубокие минимумы накачки — резкие особенности, доминирующие в стоимости интегрирования, "
            "и её результаты хранятся как данные рисунков, а не контрольные проверки. Физические "
            "единицы восстанавливаются стандартной нормировкой χ⁽²⁾ (для MgO:LiNbO₃ |χ⁽²⁾| ≈ 4 пм/В "
            "на 1 мкм), так что T_ex переводится в длину кристалла при фиксированных входных "
            "интенсивностях."
        ),
        (
            "В рамках программы это исследование заякоривает блок интегрируемых триад оптической "
            "линии: TRX-04 расширяет парное взаимодействие на пространственные керровские солитоны "
            "(«солитонная молекула»), TRX-09 проверяет вихревого близнеца того же интегрируемого "
            "семейства, а TRX-11 сохраняет гамильтоново трёхчастное ядро, добавляя излучение. Вместе "
            "с TRX-01 и TRX-12 они замыкают контур между небесной, оптической и вихревой "
            "формулировками TRIVORTEX."
        ),
    ],
    "conclusions_en": [
        "The equal-coupling three-wave system conserves the Manley–Rowe invariants to ≤ 5.329071e-15 over T = 50 (tolerance 1e-10) — machine-level photon bookkeeping.",
        "Pump depletion and revival is exactly periodic: T_ex = 5.650961242, consecutive periods agreeing to 8.743724e-08 and the revival flux reproduced to 2.442491e-15.",
        "The pump undergoes genuine full depletion, collapsing to |a₃|² = 6.32941e-05 — 99.994% of its peak flux 1.04 removed — before reviving.",
        "The exchange period is tunable by the pump amplitude: T_ex decreases monotonically from 9.028821 to 3.556606 over |a₃(0)| ∈ [0.4, 2.0], with depletion depth ≤ 5.2e-6 across the sweep.",
        "The degenerate (SHG) channel reproduces the closed form η(t) = tanh²(At) to 2.220446e-16 — one unit in the last place of double precision.",
        "The system is canonically equivalent to the Euler top and hence to the Kirchhoff three-vortex problem, making TRX-02 the optical twin of the TRIVORTEX core.",
    ],
    "conclusions_ru": [
        "Трёхволновая система с равными связями сохраняет инварианты Мэнли–Роу на уровне ≤ 5.329071e-15 за T = 50 (допуск 1e-10) — фотонная бухгалтерия машинного уровня.",
        "Истощение и возрождение накачки строго периодичны: T_ex = 5.650961242, соседние периоды совпадают с точностью 8.743724e-08, поток возрождения воспроизводится с точностью 2.442491e-15.",
        "Накачка испытывает подлинное полное истощение, проседая до |a₃|² = 6.32941e-05 — снято 99.994% пикового потока 1.04 — прежде чем возродиться.",
        "Период обмена перестраивается амплитудой накачки: T_ex монотонно убывает от 9.028821 до 3.556606 по |a₃(0)| ∈ [0.4, 2.0], глубина истощения ≤ 5.2e-6 по всей развёртке.",
        "Вырожденный (SHG) канал воспроизводит замкнутую форму η(t) = tanh²(At) с точностью 2.220446e-16 — одна единица последнего разряда двойной точности.",
        "Система канонически эквивалентна волчку Эйлера и, следовательно, задаче Кирхгофа о трёх вихрях — TRX-02 является оптическим близнецом ядра TRIVORTEX.",
    ],
    "references": [
        "1. Manley, J. M., Rowe, H. E. (1956). *Some general properties of nonlinear elements — Part I. General energy relations.* Proc. IRE 44, 904–913.",
        "2. Franken, P. A., Hill, A. E., Peters, C. W., Weinreich, G. (1961). *Generation of optical harmonics.* Phys. Rev. Lett. 7, 118–119.",
        "3. Armstrong, J. A., Bloembergen, N., Ducuing, J., Pershan, P. S. (1962). *Interactions between light waves in a nonlinear dielectric.* Phys. Rev. 127, 1918–1939.",
        "4. Kroll, N. M. (1962). *Parametric amplification in spatially extended media and application to the design of tunable oscillators.* Phys. Rev. 127, 1207–1213.",
        "5. Giordmaine, J. A., Miller, R. C. (1965). *Tunable coherent parametric oscillation in LiNbO₃ at optical frequencies.* Phys. Rev. Lett. 14, 973–976.",
        "6. Kaup, D. J., Reiman, A., Bers, A. (1979). *Space-time evolution of nonlinear three-wave interactions. I. Interactions in a homogeneous medium.* Rev. Mod. Phys. 51, 275–309.",
        "7. Boyd, R. W. (2008). *Nonlinear Optics*, 3rd ed., Academic Press.",
    ],
    "crosslinks_en": [
        "* **TRX-09** verifies the vortex twin of the same integrable family.",
        "* **TRX-04** extends the pair interaction to spatial Kerr solitons.",
        "* **TRX-11** keeps the Hamiltonian three-body core but adds radiation.",
        "* **TRX-01** shares the verification culture: closed-form and invariant-based acceptance checks at machine precision.",
    ],
    "crosslinks_ru": [
        "* **TRX-09** проверяет вихревого близнеца того же интегрируемого семейства.",
        "* **TRX-04** расширяет парное взаимодействие на пространственные керровские солитоны.",
        "* **TRX-11** сохраняет гамильтоново ядро трёх тел, но добавляет излучение.",
        "* **TRX-01** разделяет культуру верификации: контрольные проверки на замкнутых формах и инвариантах с машинной точностью.",
    ],
    "assumptions_en": [
        "Lossless medium: no linear or nonlinear absorption, so the Manley–Rowe relations hold exactly.",
        "Perfect phase matching Δk = 0; detuning and group-velocity mismatch are not modeled.",
        "Plane-wave, collinear interaction; diffraction and transverse effects are neglected.",
        "Equal normalized couplings γ₁ = γ₂ = γ₃ — the isotropic (Euler-top) case.",
        "Classical mean-field amplitudes; quantum noise and spontaneous parametric seeding are not modeled beyond the deterministic idler seed.",
        "Pump depletion is fully retained — no fixed-pump approximation is made.",
        "The exchange period is measured between refined pump-flux maxima; no analytic period formula is assumed anywhere.",
        "The fig03 sweep is a diagnostics artifact stored in the JSON figures block, not an acceptance check.",
    ],
    "assumptions_ru": [
        "Среда без потерь: нет линейного и нелинейного поглощения, поэтому соотношения Мэнли–Роу выполняются точно.",
        "Идеальное фазовое согласование Δk = 0; расстройка и рассогласование групповых скоростей не моделируются.",
        "Плосковолное коллинеарное взаимодействие; дифракция и поперечные эффекты не учитываются.",
        "Равные нормированные связи γ₁ = γ₂ = γ₃ — изотропный (эйлеров) случай.",
        "Классические амплитуды среднего поля; квантовый шум и спонтанное параметрическое затравливание не моделируются — кроме детерминированной затравки холостой волны.",
        "Истощение накачки удержано полностью — приближение заданной накачки не используется.",
        "Период обмена измеряется между уточнёнными максимумами потока накачки; аналитическая формула периода нигде не предполагается.",
        "Развёртка fig03 — диагностический артефакт, хранимый в блоке figures JSON-протокола, а не контрольная проверка.",
    ],
    "glance_en": [
        ["Block", "Nonlinear optics — study 02 of 12"],
        ["Model", "resonant three-wave mixing in a χ⁽²⁾ crystal (equal couplings, Δk = 0)"],
        ["Key invariant", "Manley–Rowe invariants I₁, I₂, I₃"],
        ["Headline result", "invariant drift ≤ 5.4e-15 over T = 50; SHG closed-form error 2.2e-16"],
        ["Verification", "7/7 checks PASS (full mode)"],
        ["Runtime", "0.6 s full · < 20 s smoke"],
    ],
    "glance_ru": [
        ["Блок", "Нелинейная оптика — исследование 02 из 12"],
        [
            "Модель",
            "резонансное трёхволновое взаимодействие в кристалле χ⁽²⁾ (равные связи, Δk = 0)",
        ],
        ["Ключевой инвариант", "инварианты Мэнли–Роу I₁, I₂, I₃"],
        ["Главный результат", "дрейф инвариантов ≤ 5.4e-15 за T = 50; ошибка SHG-формулы 2.2e-16"],
        ["Верификация", "7/7 проверок PASS (полный режим)"],
        ["Время выполнения", "0.6 с полный · < 20 с smoke"],
    ],
    "glossary": {
        "header_en": ["Term", "Definition"],
        "header_ru": ["Термин", "Определение"],
        "rows_en": [
            [
                "Three-wave mixing",
                "resonant nonlinear-optical process in which waves at ω₁, ω₂ and ω₃ = ω₁ + ω₂ exchange photons through a χ⁽²⁾ nonlinearity",
            ],
            [
                "Pump / signal / idler",
                "the high-frequency wave a₃ and the generated pair a₁, a₂ of a down-conversion triad",
            ],
            [
                "Manley–Rowe relations",
                "quadratic conservation laws for photon fluxes, originally derived for nonlinear microwave elements (1956)",
            ],
            [
                "Photon flux |a_k|²",
                "normalized intensity proportional to the photon flow carried by wave k",
            ],
            [
                "Pump depletion",
                "transfer of pump flux into the signal–idler pair until the pump is (almost) emptied",
            ],
            [
                "Exchange period T_ex",
                "time between successive pump maxima — one full choreographic cycle of the triad",
            ],
            ["SHG", "second-harmonic generation: the degenerate channel ω₁ = ω₂ = ω₃/2"],
            [
                "Conversion efficiency η",
                "share of the total flux carried by the second harmonic, η = |p|²/(|p|² + |s|²)",
            ],
            [
                "Phase matching",
                "condition k₃ = k₁ + k₂ (Δk = 0) letting the coupling accumulate over the medium",
            ],
            [
                "Euler top",
                "torque-free rigid-body rotation; the canonical integrable equivalent of the equal-coupling three-wave system",
            ],
        ],
        "rows_ru": [
            [
                "Трёхволновое взаимодействие",
                "резонансный нелинейно-оптический процесс, в котором волны на ω₁, ω₂ и ω₃ = ω₁ + ω₂ обмениваются фотонами через нелинейность χ⁽²⁾",
            ],
            [
                "Накачка / сигнал / холостая волна",
                "высокочастотная волна a₃ и порождаемая пара a₁, a₂ в триаде параметрической расщепки",
            ],
            [
                "Соотношения Мэнли–Роу",
                "квадратичные законы сохранения потоков фотонов, изначально выведенные для нелинейных микроволновых элементов (1956)",
            ],
            [
                "Поток фотонов |a_k|²",
                "нормированная интенсивность, пропорциональная потоку фотонов в волне k",
            ],
            [
                "Истощение накачки",
                "перекачка потока накачки в пару «сигнал — холостая волна» вплоть до (почти) полного опустошения",
            ],
            [
                "Период обмена T_ex",
                "время между соседними максимумами накачки — один полный хореографический цикл триады",
            ],
            ["SHG", "генерация второй гармоники: вырожденный канал ω₁ = ω₂ = ω₃/2"],
            [
                "Эффективность конверсии η",
                "доля полного потока, унесённая второй гармоникой, η = |p|²/(|p|² + |s|²)",
            ],
            [
                "Фазовое согласование",
                "условие k₃ = k₁ + k₂ (Δk = 0), позволяющее связи накопиться по всей среде",
            ],
            [
                "Волчок Эйлера",
                "свободное вращение твёрдого тела; канонический интегрируемый эквивалент трёхволновой системы с равными связями",
            ],
        ],
    },
    "notation": {
        "header_en": ["Symbol", "Meaning"],
        "header_ru": ["Символ", "Смысл"],
        "rows_en": [
            ["a₁, a₂, a₃", "complex amplitudes of signal, idler and pump"],
            ["a*", "complex conjugate"],
            ["|a_k|²", "photon flux in wave k (dimensionless)"],
            ["I₁, I₂, I₃", "Manley–Rowe invariants"],
            ["γ_k", "coupling coefficients (all 1 after normalization)"],
            ["Δk", "phase mismatch k₃ − k₁ − k₂"],
            ["T_ex", "exchange period between successive pump maxima"],
            ["η", "SHG conversion efficiency"],
            ["A", "initial amplitude of the SHG channel"],
            ["t, T", "time and integration span (dimensionless)"],
        ],
        "rows_ru": [
            ["a₁, a₂, a₃", "комплексные амплитуды сигнала, холостой волны и накачки"],
            ["a*", "комплексное сопряжение"],
            ["|a_k|²", "поток фотонов в волне k (безразмерный)"],
            ["I₁, I₂, I₃", "инварианты Мэнли–Роу"],
            ["γ_k", "коэффициенты связи (после нормировки все равны 1)"],
            ["Δk", "фазовая расстройка k₃ − k₁ − k₂"],
            ["T_ex", "период обмена между соседними максимумами накачки"],
            ["η", "эффективность SHG-конверсии"],
            ["A", "начальная амплитуда SHG-канала"],
            ["t, T", "время и интервал интегрирования (безразмерные)"],
        ],
    },
    "params_appendix": {
        "header_en": ["Symbol", "Value", "Role"],
        "header_ru": ["Символ", "Значение", "Роль"],
        "rows_en": [
            ["a₁(0), a₂(0)", "0.2, 0.3", "signal/idler seeds (real)"],
            ["a₃(0)", "1.0·i", "pump seed, phase π/2"],
            ["γ₁, γ₂, γ₃", "1, 1, 1", "normalized couplings"],
            ["Δk", "0", "phase mismatch"],
            ["T", "50", "integration span of the main run"],
            ["rtol, atol", "1e-13", "DOP853 tolerances (main run)"],
            ["max_step", "0.02", "integrator step cap (main run)"],
            ["dense samples", "20001", "pump-maximum detection grid"],
            ["A", "1", "SHG seed amplitude"],
            [
                "sweep",
                "|a₃(0)| ∈ [0.4, 2.0], 17 pts, rtol 1e-10",
                "fig03 parameter sweep (--figures mode)",
            ],
        ],
        "rows_ru": [
            ["a₁(0), a₂(0)", "0.2, 0.3", "затравки сигнала и холостой волны (вещественные)"],
            ["a₃(0)", "1.0·i", "затравка накачки, фаза π/2"],
            ["γ₁, γ₂, γ₃", "1, 1, 1", "нормированные коэффициенты связи"],
            ["Δk", "0", "фазовая расстройка"],
            ["T", "50", "интервал интегрирования основного прогона"],
            ["rtol, atol", "1e-13", "допуски DOP853 (основной прогон)"],
            ["max_step", "0.02", "ограничение шага интегратора (основной прогон)"],
            ["плотные выборки", "20001", "сетка поиска максимумов накачки"],
            ["A", "1", "затравочная амплитуда SHG-канала"],
            [
                "развёртка",
                "|a₃(0)| ∈ [0.4, 2.0], 17 точек, rtol 1e-10",
                "развёртка fig03 (режим --figures)",
            ],
        ],
    },
    "bibtex": [
        "@article{manley1956,",
        "  author  = {Manley, J. M. and Rowe, H. E.},",
        "  title   = {Some general properties of nonlinear elements. Part {I}: General energy relations},",
        "  journal = {Proceedings of the IRE},",
        "  year    = {1956}, volume = {44}, number = {7}, pages = {904--913}}",
        "",
        "@article{armstrong1962,",
        "  author  = {Armstrong, J. A. and Bloembergen, N. and Ducuing, J. and Pershan, P. S.},",
        "  title   = {Interactions between light waves in a nonlinear dielectric},",
        "  journal = {Physical Review},",
        "  year    = {1962}, volume = {127}, pages = {1918--1939}}",
        "",
        "@article{kaup1979,",
        "  author  = {Kaup, D. J. and Reiman, A. and Bers, A.},",
        "  title   = {Space-time evolution of nonlinear three-wave interactions. {I}: Interactions in a homogeneous medium},",
        "  journal = {Reviews of Modern Physics},",
        "  year    = {1979}, volume = {51}, pages = {275--309}}",
        "",
        "@book{boyd2008,",
        "  author    = {Boyd, R. W.},",
        "  title     = {Nonlinear Optics},",
        "  edition   = {3rd},",
        "  publisher = {Academic Press}, year = {2008}}",
    ],
}
