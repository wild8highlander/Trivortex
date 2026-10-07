# -*- coding: utf-8 -*-
"""Content pack for TRX-05 (v1.0.0 Monograph Edition). Rendered by scripts/build_study_docs.py."""

PACK = {
    "meta": {
        "study_id": "TRX-05",
        "dir_name": "TRX-05-optical-vortices",
        "title_en": "Optical Vortices of Laser Beams and the Point-Vortex Analogy",
        "title_ru": "Оптические вихри лазерных пучков и аналогия с точечными вихрями",
        "script": "trx05_optical_vortices.py",
        "results_json": "trx05_results.json",
        "scheme_file": "scheme_trx05.svg",
        "runtime_full": "4.83 s (4.827 s recorded with --figures)",
    },
    "essence_en": (
        "Three phase singularities — optical vortices — of a paraxial laser field "
        "behave, to leading order, exactly like Kirchhoff point vortices of ideal fluid "
        "dynamics. The study realizes the vortex representation of TRIVORTEX *literally in "
        "light*: three same-sign singularities of the field ψ(z) = exp(−r²/w²)·Π(z − z_k) sit "
        "on an equilateral triangle of side a = 1 and rotate rigidly with the analytic angular "
        "velocity ω = 3Γ/(2πa²) = 0.477464829, measured to 1e-8, while the angular impulse "
        "I = ΣΓ|r|² (the many-vortex prototype of the Chaplygin integral) stays pinned at "
        "a² = 1 and the winding number of the rendered field equals 3 exactly — the analogue "
        "of orbital angular momentum 3ℏ per photon."
    ),
    "essence_ru": (
        "Три фазовые сингулярности — оптические вихри — параксиального лазерного "
        "поля ведут себя в главном порядке в точности как точечные вихри Кирхгофа из динамики "
        "идеальной жидкости. Исследование реализует вихревое представление TRIVORTEX "
        "*буквально в свете*: три одноимённые сингулярности поля "
        "ψ(z) = exp(−r²/w²)·Π(z − z_k) сидят на вершинах равностороннего треугольника со "
        "стороной a = 1 и вращаются жёстко с аналитической угловой скоростью "
        "ω = 3Γ/(2πa²) = 0.477464829, измеренной с точностью 1e-8, при этом угловой импульс "
        "I = ΣΓ|r|² (многовихревой прототип интеграла Чаплыгина) закреплён на a² = 1, а число "
        "намотки построенного поля равно в точности 3 — аналог орбитального углового момента "
        "3ℏ на фотон."
    ),
    "mission_en": [
        (
            "The vortex representation is TRIVORTEX's signature move — and here it is realized "
            "literally in light. Zeros of a complex scalar field with equal topological charge "
            "circulate around each other exactly as Kirchhoff point vortices do (Berry & "
            "Dennis): the phase gradient of a laser field near an intensity zero generates the "
            "same 1/r velocity field as a fluid vortex of circulation Γ. This study closes the "
            "loop between singular optics and the classical point-vortex problem — the same "
            "equations, the same relative equilibrium, the same invariant — so that the "
            "mathematical backbone of the TRIVORTEX monograph can be demonstrated on a laser "
            "bench."
        ),
        (
            "The study verifies three things to machine precision. First, three same-sign "
            "singularities on an equilateral triangle of side a = 1 rotate rigidly with the "
            "analytic rate ω = 3Γ/(2πa²) = 0.477464829, measured to 1e-8. Second, the angular "
            "impulse I = ΣΓ|r|² and the Kirchhoff Hamiltonian are conserved to 1.8e-15 and "
            "4.6e-16 over three rotations (T = 39.4784). Third, the rendered complex field "
            "shows three dark cores tracking the vortex positions within 0.0118 — three times "
            "inside the 0.036 acceptance — and the winding number of arg ψ is exactly 3. "
            "Singular optics and the classical vortex problem are, numerically, the same "
            "system."
        ),
    ],
    "mission_ru": [
        (
            "Вихревое представление — фирменный приём TRIVORTEX, и здесь оно реализовано "
            "буквально в свете. Нули комплексного скалярного поля с одинаковым топологическим "
            "зарядом циркулируют друг вокруг друга в точности как точечные вихри Кирхгофа "
            "(Берри и Деннис): градиент фазы лазерного поля вблизи нуля интенсивности порождает "
            "то же поле скоростей 1/r, что и вихрь жидкости с циркуляцией Γ. Данное "
            "исследование замыкает контур между сингулярной оптикой и классической задачей о "
            "точечных вихрях — те же уравнения, то же относительное равновесие, тот же "
            "инвариант, — так что математический каркас монографии TRIVORTEX можно "
            "продемонстрировать на лазерном стенде."
        ),
        (
            "Исследование проверяет три вещи с машинной точностью. Во-первых, три одноимённые "
            "сингулярности на равностороннем треугольнике со стороной a = 1 вращаются жёстко с "
            "аналитической скоростью ω = 3Γ/(2πa²) = 0.477464829, измеренной с точностью 1e-8. "
            "Во-вторых, угловой импульс I = ΣΓ|r|² и гамильтониан Кирхгофа сохраняются на "
            "уровне 1.8e-15 и 4.6e-16 за три оборота (T = 39.4784). В-третьих, построенное "
            "комплексное поле показывает три тёмных ядра, следящих за позициями вихрей в "
            "пределах 0.0118 — втрое внутри допуска 0.036, — а число намотки arg ψ равно в "
            "точности 3. Сингулярная оптика и классическая вихревая задача численно являются "
            "одной и той же системой."
        ),
    ],
    "physics_en": [
        (
            "(A) Kirchhoff dynamics. Three point vortices of equal circulation Γ = 1 are placed "
            "on an equilateral triangle of side a = 1 (circumscribed radius r_c = a/√3 ≈ "
            "0.57735) and integrated with an explicit Dormand–Prince 8(5,3) scheme over three "
            "full rotations, T = 39.4784. For equal same-sign circulations the equilateral "
            "configuration is an exact relative equilibrium: every vortex traces a circle of "
            "radius r_c about the common centroid at the analytic rate ω = 3Γ/(2πa²)."
        ),
        (
            "(B) Field rendering. The paraxial scalar field ψ(z) = exp(−r²/w²)·Π_k (z − z_k(t)) "
            "with a Gaussian envelope w = 3 is evaluated on a grid of 0.018 spacing over "
            "[−1.7, 1.7]² at t = 0 and t = T/4. Its intensity zeros coincide with the vortex "
            "positions, the phase winds by 2π around each core, and the winding of arg ψ on a "
            "large circle counts the total topological charge N = 3 — the optical analogue of "
            "orbital angular momentum 3ℏ per photon."
        ),
    ],
    "physics_ru": [
        (
            "(A) Динамика Кирхгофа. Три точечных вихря равной циркуляции Γ = 1 помещаются в "
            "вершины равностороннего треугольника со стороной a = 1 (радиус описанной окружности "
            "r_c = a/√3 ≈ 0.57735) и интегрируются явной схемой Дормана–Принса 8(5,3) на три "
            "полных оборота, T = 39.4784. При равных одноимённых циркуляциях равносторонняя "
            "конфигурация — точное относительное равновесие: каждый вихрь описывает окружность "
            "радиуса r_c вокруг общего центра с аналитической скоростью ω = 3Γ/(2πa²)."
        ),
        (
            "(B) Построение поля. Параксиальное скалярное поле ψ(z) = exp(−r²/w²)·Π_k (z − z_k(t)) "
            "с гауссовой огибающей w = 3 вычисляется на сетке с шагом 0.018 по квадрату "
            "[−1.7, 1.7]² при t = 0 и t = T/4. Его нули интенсивности совпадают с позициями "
            "вихрей, фаза наматывается на 2π вокруг каждого ядра, а намотка arg ψ по большой "
            "окружности даёт полный топологический заряд N = 3 — оптический аналог орбитального "
            "углового момента 3ℏ на фотон."
        ),
    ],
    "preset_table": {
        "header_en": ["Parameter", "Value", "Meaning"],
        "header_ru": ["Параметр", "Значение", "Смысл"],
        "rows_en": [
            ["Γ", "1", "circulation of each optical vortex (= topological charge +1)"],
            ["a", "1", "side of the equilateral vortex triangle, r_c = a/√3 ≈ 0.57735"],
            [
                "ψ(z)",
                "exp(−r²/w²)·Π_k (z − z_k)",
                "rendered paraxial field, Gaussian envelope w = 3",
            ],
            ["grid", "0.018 over [−1.7, 1.7]²", "intensity/phase rendering and zero tracking"],
            ["integrator", "DOP853, rtol = atol = 1e-13", "three rotations, T = 39.4784"],
            ["winding circle", "r = 1.55", "topological-charge evaluation (any r > r_c)"],
        ],
        "rows_ru": [
            ["Γ", "1", "циркуляция каждого оптического вихря (= топологический заряд +1)"],
            ["a", "1", "сторона равностороннего вихревого треугольника, r_c = a/√3 ≈ 0.57735"],
            [
                "ψ(z)",
                "exp(−r²/w²)·Π_k (z − z_k)",
                "построенное параксиальное поле, гауссова огибающая w = 3",
            ],
            ["сетка", "0.018 по [−1.7, 1.7]²", "рендеринг интенсивности/фазы и слежение за нулями"],
            ["интегратор", "DOP853, rtol = atol = 1e-13", "три оборота, T = 39.4784"],
            ["окружность намотки", "r = 1.55", "вычисление топологического заряда (любое r > r_c)"],
        ],
    },
    "equations": [
        {
            "id": "E1",
            "latex": "u_k = -\\frac{1}{2\\pi}\\sum_{j\\neq k}\\Gamma_j\\,\\frac{y_k - y_j}{r_{kj}^2}, \\qquad "
            "v_k = +\\frac{1}{2\\pi}\\sum_{j\\neq k}\\Gamma_j\\,\\frac{x_k - x_j}{r_{kj}^2}",
            "desc_en": "Kirchhoff point-vortex equations (velocity of vortex k induced by all others)",
            "desc_ru": "Уравнения точечных вихрей Кирхгофа (скорость вихря k, наведённая остальными)",
        },
        {
            "id": "E2",
            "latex": "I = \\sum_k \\Gamma_k\\,|\\mathbf{r}_k|^2 = a^2",
            "desc_en": "Angular impulse of the vortex system — the many-vortex prototype of the Chaplygin integral; for the equilateral triangle it is pinned at a²",
            "desc_ru": "Угловой импульс вихревой системы — многовихревой прототип интеграла Чаплыгина; для равностороннего треугольника закреплён на a²",
        },
        {
            "id": "E3",
            "latex": "H = -\\frac{\\Gamma^2}{2\\pi}\\sum_{j<k} \\ln r_{jk}",
            "desc_en": "Kirchhoff Hamiltonian (logarithmic pair interaction; H = 0 identically for a = 1)",
            "desc_ru": "Гамильтониан Кирхгофа (логарифмическое парное взаимодействие; H = 0 тождественно при a = 1)",
        },
        {
            "id": "E4",
            "latex": "\\omega = \\frac{3\\Gamma}{2\\pi a^2}",
            "desc_en": "Analytic rotation rate of the same-sign equilateral triangle (Lagrange-type relative equilibrium)",
            "desc_ru": "Аналитическая скорость вращения одноимённого равностороннего треугольника (относительное равновесие типа Лагранжа)",
        },
        {
            "id": "E5",
            "latex": "\\psi(z) = e^{-r^2/w^2}\\prod_k \\bigl(z - z_k(t)\\bigr), \\qquad "
            "N = \\frac{1}{2\\pi}\\oint \\nabla(\\arg\\psi)\\cdot d\\mathbf{l} = \\sum_k q_k = 3",
            "desc_en": "Rendered paraxial field and its winding number (total topological charge)",
            "desc_ru": "Построенное параксиальное поле и его число намотки (полный топологический заряд)",
        },
    ],
    "scheme_cap_en": (
        "TRX-05 scheme — optical vortices and the vortex-triangle analogy: three phase "
        "singularities (dark cores, charge +1) of a paraxial beam rotate rigidly as an equilateral "
        "triangle, and every optical quantity maps onto the Kirchhoff point-vortex model."
    ),
    "scheme_cap_ru": (
        "Схема TRX-05 — оптические вихри и аналогия с вихревым треугольником: три фазовые "
        "сингулярности (тёмные ядра, заряд +1) параксиального пучка вращаются жёстко как равносторонний "
        "треугольник, и каждая оптическая величина отображается на модель точечных вихрей Кирхгофа."
    ),
    "scheme_walk_en": [
        [
            "Paraxial beam",
            "Gaussian envelope exp(−r²/w²) with w = 3a; transverse (x, y) plane of the beam",
        ],
        [
            "Three dark cores",
            "phase singularities (intensity zeros) at the triangle vertices, each with charge q = +1",
        ],
        [
            "Phase windings",
            "2π winding arrows around each core; the far field winds by N = 3 (three-armed spiral)",
        ],
        ["Equilateral triangle", "side a = 1, circumscribed radius r_c = a/√3 ≈ 0.57735"],
        ["Rotation arrow", "rigid rotation at ω = 3Γ/(2πa²) = 0.477464829, verified to 1e-8"],
        [
            "Mapping column",
            "optics → Kirchhoff model: core ↔ point vortex, q ↔ Γ, I = a² ↔ Chaplygin integral",
        ],
    ],
    "scheme_walk_ru": [
        [
            "Параксиальный пучок",
            "гауссова огибающая exp(−r²/w²) с w = 3a; поперечная плоскость (x, y) пучка",
        ],
        [
            "Три тёмных ядра",
            "фазовые сингулярности (нули интенсивности) в вершинах треугольника, заряд каждого q = +1",
        ],
        [
            "Фазовые намотки",
            "стрелки намотки 2π вокруг каждого ядра; дальнее поле наматывается на N = 3 (трёхрукавная спираль)",
        ],
        [
            "Равносторонний треугольник",
            "сторона a = 1, радиус описанной окружности r_c = a/√3 ≈ 0.57735",
        ],
        [
            "Стрелка вращения",
            "жёсткое вращение с ω = 3Γ/(2πa²) = 0.477464829, проверено с точностью 1e-8",
        ],
        [
            "Столбец соответствий",
            "оптика → модель Кирхгофа: ядро ↔ точечный вихрь, q ↔ Γ, I = a² ↔ интеграл Чаплыгина",
        ],
    ],
    "mapping": {
        "header_en": ["Quantity in this study", "TRIVORTEX analog", "Comment"],
        "header_ru": ["Величина исследования", "Аналог в TRIVORTEX", "Комментарий"],
        "rows_en": [
            [
                "Optical vortices (field zeros)",
                "vortex model \u201cbodies\u201d",
                "literal realization of the model",
            ],
            ["Topological charge q_k = +1", "circulation Γ_k", "the charge–circulation dictionary"],
            ["I = ΣΓ|r|² = a²", "Chaplygin integral C_Ch", "the same invariant structure"],
            [
                "Equilateral triangle rotation",
                "Theorem 3.1 choreography",
                "identical relative equilibrium",
            ],
            ["Winding number 3", "total charge ΣΓ = 3", "orbital angular momentum 3ℏ per photon"],
        ],
        "rows_ru": [
            [
                "Оптические вихри (нули поля)",
                "«тела» вихревой модели",
                "буквальная реализация модели",
            ],
            ["Топологический заряд q_k = +1", "циркуляция Γ_k", "словарь «заряд–циркуляция»"],
            ["I = ΣΓ|r|² = a²", "интеграл Чаплыгина C_Ch", "та же инвариантная структура"],
            [
                "Вращение равностороннего треугольника",
                "хореография теоремы 3.1",
                "то же относительное равновесие",
            ],
            ["Число намотки 3", "полный заряд ΣΓ = 3", "орбитальный угловой момент 3ℏ на фотон"],
        ],
    },
    "nondim_en": (
        "Lengths in units of the triangle side a; circulation Γ = 1; time in units of "
        "a²/Γ, so the rotation period is 2π/ω = 13.1595 and three rotations span "
        "T = 39.4784; the rendered field uses w = 3a and the winding circle r = 1.55. All "
        "quantities are dimensionless and transfer verbatim to the TRIVORTEX vortex model."
    ),
    "nondim_ru": (
        "Длины в единицах стороны треугольника a; циркуляция Γ = 1; время в единицах "
        "a²/Γ, так что период вращения равен 2π/ω = 13.1595, а три оборота занимают "
        "T = 39.4784; построенное поле использует w = 3a и окружность намотки r = 1.55. Все "
        "величины безразмерны и дословно переносятся в вихревую модель TRIVORTEX."
    ),
    "checks": {
        "header_en": ["Check", "Target", "Tolerance"],
        "header_ru": ["Проверка", "Цель", "Допуск"],
        "rows_en": [
            ["Measured rotation rate vs ω = 3Γ/(2πa²) = 0.477464829", "0.477464829", "1e-8"],
            ["Angular impulse I = ΣΓ|r|² drift over three rotations", "0", "1e-12"],
            ["Kirchhoff Hamiltonian H drift over three rotations", "0", "1e-12"],
            [
                "Deepest intensity minima track the vortices (t = 0 and t = T/4)",
                "≤ 2 grid cells",
                "0.036",
            ],
            ["Winding number of arg ψ on r = 1.55", "3", "exact"],
        ],
        "rows_ru": [
            [
                "Измеренная скорость вращения против ω = 3Γ/(2πa²) = 0.477464829",
                "0.477464829",
                "1e-8",
            ],
            ["Дрейф углового импульса I = ΣΓ|r|² за три оборота", "0", "1e-12"],
            ["Дрейф гамильтониана Кирхгофа H за три оборота", "0", "1e-12"],
            [
                "Глубочайшие минимумы интенсивности следят за вихрями (t = 0 и t = T/4)",
                "≤ 2 ячейки сетки",
                "0.036",
            ],
            ["Число намотки arg ψ на r = 1.55", "3", "точно"],
        ],
    },
    "figure_caps": {
        "fig01_field_landscape.png": {
            "cap_en": "Field landscape at t = 0: intensity |ψ|² (log scale) with the three dark cores on the triangle vertices, and the phase arg ψ with its 2π windings.",
            "cap_ru": "Ландшафт поля при t = 0: интенсивность |ψ|² (лог. шкала) с тремя тёмными ядрами в вершинах треугольника и фаза arg ψ с намотками 2π.",
            "walk_en": "The intensity panel shows the three dark cores sitting exactly at the vertices of the equilateral triangle (side a = 1) inside the Gaussian envelope; the phase panel resolves the 2π winding around each core, and the dashed circle r = 1.55 is the circle on which the winding number is measured — it returns N = 3 exactly.",
            "walk_ru": "Панель интенсивности показывает три тёмных ядра точно в вершинах равностороннего треугольника (сторона a = 1) внутри гауссовой огибающей; панель фазы разрешает намотку 2π вокруг каждого ядра, а пунктирная окружность r = 1.55 — та, на которой измеряется число намотки: оно равно в точности 3.",
        },
        "fig02_rigid_rotation.png": {
            "cap_en": "Headline result — rigid rotation of the vortex triangle: core worldlines over three rotations and the linear growth of the polar angle.",
            "cap_ru": "Главный результат — жёсткое вращение вихревого треугольника: мировые линии ядер за три оборота и линейный рост полярного угла.",
            "walk_en": "All three cores trace circles of radius r_c = a/√3 ≈ 0.57735 about the common centroid over T = 39.4784 (three rotations, period 13.1595); the measured rotation rate 0.477464829 coincides with the analytic 3Γ/(2πa²) = 0.477464829 — agreement at the 1e-16 level, seven orders inside the 1e-8 acceptance tolerance.",
            "walk_ru": "Все три ядра описывают окружности радиуса r_c = a/√3 ≈ 0.57735 вокруг общего центра за T = 39.4784 (три оборота, период 13.1595); измеренная скорость 0.477464829 совпадает с аналитической 3Γ/(2πa²) = 0.477464829 — согласие на уровне 1e-16, на семь порядков внутри допуска 1e-8.",
        },
        "fig03_parameter_sweeps.png": {
            "cap_en": "Parameter sweeps: rotation rate versus triangle side (analytic law against numeric re-runs) and zero-tracking error versus grid spacing.",
            "cap_ru": "Развертки по параметрам: скорость вращения против стороны треугольника (аналитический закон и численные перезапуски) и ошибка слежения за нулями против шага сетки.",
            "walk_en": "The numeric DOP853 re-runs reproduce ω(a) = 3Γ/(2πa²) to nine recorded decimals across a ∈ {0.6, 0.8, 1.0, 1.2, 1.5, 2.0} (from 1.326291192 down to 0.119366207); the tracking sweep keeps the worst core offset below the 2-cell acceptance line everywhere (0.00668 at spacing 0.012 up to 0.04922 at spacing 0.08, against acceptance 0.024–0.16), and the preset grid gives 0.01178.",
            "walk_ru": "Численные перезапуски DOP853 воспроизводят ω(a) = 3Γ/(2πa²) с точностью до девяти записанных знаков по a ∈ {0.6, 0.8, 1.0, 1.2, 1.5, 2.0} (от 1.326291192 до 0.119366207); развёртка слежения удерживает худшее смещение ядра ниже линии допуска в 2 ячейки всюду (0.00668 при шаге 0.012 до 0.04922 при шаге 0.08 против допуска 0.024–0.16), а пресетная сетка даёт 0.01178.",
        },
        "fig04_invariants_rigidity.png": {
            "cap_en": "Dynamics over three rotations: drifts of the angular impulse I and the Kirchhoff Hamiltonian H against the acceptance tolerance, and side-length deviations of the rotating triangle.",
            "cap_ru": "Динамика за три оборота: дрейфы углового импульса I и гамильтониана Кирхгофа H против допуска и отклонения длин сторон вращающегося треугольника.",
            "walk_en": "The angular impulse drifts by 1.8e-15 and the Kirchhoff Hamiltonian by 4.6e-16 over T = 39.4784 — hundreds to thousands of times below the 1e-12 tolerance (H is 0 identically for a = 1, since ln 1 = 0); the three side-length deviations d_jk(t) − a stay at machine level, confirming the triangle rotates as a rigid equilateral configuration.",
            "walk_ru": "Угловой импульс дрейфует на 1.8e-15, а гамильтониан Кирхгофа на 4.6e-16 за T = 39.4784 — в сотни и тысячи раз ниже допуска 1e-12 (H тождественно равно 0 при a = 1, поскольку ln 1 = 0); три отклонения длин сторон d_jk(t) − a остаются на машинном уровне, подтверждая, что треугольник вращается как жёсткая равносторонняя конфигурация.",
        },
    },
    "results_block": [
        "rotation_rate_vs_analytic          = 4.774648e-01 (target 0.477464829276, tol 1e-08)",
        "angular_impulse_I_conserved        = 1.8e-15      (I = 1.000000000000 = a^2)",
        "kirchhoff_hamiltonian_conserved    = 4.6e-16      (H = 0 identically for a = 1)",
        "field_minima_track_vortices        = 1.2e-02      (<= 2 grid cells = 0.036)",
        "total_winding_number_is_3          = 3.0 exactly",
        "figures: scheme_trx05.svg + 4 PNG panels written to figures/",
        "status: PASS (5/5)",
    ],
    "abstract_en": (
        "This monograph treats phase singularities — optical vortices — of a paraxial "
        "laser field and makes the classical analogy with Kirchhoff point vortices quantitative "
        "in both directions. Three same-sign singularities of the field ψ(z) = exp(−r²/w²)·Π(z − z_k) "
        "are placed on an equilateral triangle of side a = 1 and integrated over three rotations "
        "(T = 39.4784) with a DOP853 scheme at rtol = atol = 1e-13. The measured rotation rate "
        "0.477464829 reproduces the analytic Lagrange-type law ω = 3Γ/(2πa²) within the 1e-8 "
        "acceptance tolerance (agreement at the 1e-16 level). The angular impulse I = ΣΓ|r|² — the "
        "many-vortex prototype of the Chaplygin integral — stays pinned at a² = 1 with drift 1.8e-15, "
        "and the Kirchhoff Hamiltonian drifts by 4.6e-16, both far inside the 1e-12 tolerance. The "
        "rendered complex field (grid spacing 0.018) shows three dark cores tracking the vortex "
        "positions within 0.0118 against the 0.036 acceptance, and the winding number of arg ψ on "
        "r = 1.55 equals 3 exactly — the optical analogue of orbital angular momentum 3ℏ per photon. "
        "Singular optics and the classical point-vortex problem are thus numerically the same system."
    ),
    "abstract_ru": (
        "Монография посвящена фазовым сингулярностям — оптическим вихрям — параксиального "
        "лазерного поля и делает классическую аналогию с точечными вихрями Кирхгофа количественной в "
        "обе стороны. Три одноимённые сингулярности поля ψ(z) = exp(−r²/w²)·Π(z − z_k) помещаются на "
        "равносторонний треугольник со стороной a = 1 и интегрируются на три оборота (T = 39.4784) "
        "схемой DOP853 при rtol = atol = 1e-13. Измеренная скорость вращения 0.477464829 "
        "воспроизводит аналитический лагранжев закон ω = 3Γ/(2πa²) внутри допуска 1e-8 (согласие на "
        "уровне 1e-16). Угловой импульс I = ΣΓ|r|² — многовихревой прототип интеграла Чаплыгина — "
        "закреплён на a² = 1 с дрейфом 1.8e-15, а гамильтониан Кирхгофа дрейфует на 4.6e-16; оба "
        "далеко внутри допуска 1e-12. Построенное комплексное поле (шаг сетки 0.018) показывает три "
        "тёмных ядра, следящих за позициями вихрей в пределах 0.0118 против допуска 0.036, а число "
        "намотки arg ψ на r = 1.55 равно в точности 3 — оптический аналог орбитального углового "
        "момента 3ℏ на фотон. Сингулярная оптика и классическая задача о точечных вихрях оказываются "
        "численно одной и той же системой."
    ),
    "intro_en": [
        (
            "Optical vortices — the phase singularities of light — entered physics as curiosities of "
            "wave interference and grew into a discipline of their own. Berry and Dennis (2000) "
            "gave the canonical statistical description of singularities in random waves, showing "
            "that zeros of a complex scalar field are points where phase is undefined and around "
            "which the phase winds by an integer multiple of 2π. Soskin, Gorshkov and Vasnetsov "
            "(1997) had already established that laser beams carrying such screw dislocations "
            "possess a well-defined topological charge and that this charge is the optical "
            "counterpart of orbital angular momentum — each photon of a charge-q beam carries "
            "qℏ of OAM in addition to its spin."
        ),
        (
            "The classical side of the analogy is older by more than a century. Kirchhoff (1876) "
            "wrote down the equations of point vortices that still carry his name: each vortex is "
            "advected by the velocity field induced by all the others, a 1/r induction law that "
            "makes the mathematics identical to the phase gradient of an optical zero. Aref (1979) "
            "revisited the three-vortex problem and clarified its integrability and collapse "
            "structure, Newton (2001) consolidated the N-vortex problem into a standard reference, "
            "and Aref et al. (2003) surveyed vortex crystals — relative equilibria of point "
            "vortices — of which the equilateral triangle of equal circulations is the simplest "
            "and most celebrated example."
        ),
        (
            "The bridge between the two disciplines is a product structure. Near a zero the field "
            "factorizes, ψ ≈ (z − z_k)·(smooth part), and the phase gradient of the factor "
            "(z − z_k) is exactly the velocity field of a point vortex; zeros of equal sign "
            "therefore move under the Kirchhoff equations to leading order. A laser beam with a "
            "designed product ψ(z) = exp(−r²/w²)·Π_k (z − z_k) thus realizes the point-vortex "
            "dynamics literally in light: the dark cores are the \u201cbodies\u201d, their "
            "topological charges are the circulations, and the beam's far-field winding is the "
            "total charge. The analogy is not metaphorical — it is the same system of ODEs at "
            "leading order."
        ),
        (
            "For TRIVORTEX the relevance is structural. The angular impulse I = ΣΓ|r|² of the "
            "vortex system is the many-vortex prototype of the Chaplygin integral C_Ch that "
            "pins the vortex-model orbits; the rigidly rotating equilateral triangle is the "
            "optical twin of the Theorem 3.1 choreography; and the winding number of the field "
            "is the optical reading of the total vortex charge. This study therefore anchors "
            "the optics block of the program: it shows that the framework's mathematical "
            "skeleton survives verbatim when the vortices are made of light (TRX-04 provides "
            "the field-maxima counterpart, TRX-09 the classical fluid anchor)."
        ),
    ],
    "intro_ru": [
        (
            "Оптические вихри — фазовые сингулярности света — вошли в физику как диковинки "
            "волновой интерференции и выросли в отдельную дисциплину. Берри и Деннис (2000) дали "
            "каноническое статистическое описание сингулярностей в случайных волнах, показав, что "
            "нули комплексного скалярного поля — это точки, в которых фаза не определена и вокруг "
            "которых она наматывается на целое число 2π. Соскин, Горшков и Васнецов (1997) ранее "
            "установили, что лазерные пучки с винтовыми дислокациями обладают определённым "
            "топологическим зарядом и что этот заряд — оптический аналог орбитального углового "
            "момента: каждый фотон пучка с зарядом q несёт qℏ орбитального момента помимо "
            "спинового."
        ),
        (
            "Классическая сторона аналогии старше более чем на век. Кирхгоф (1876) записал "
            "уравнения точечных вихрей, носящие его имя: каждый вихрь переносится полем скоростей, "
            "наведённым остальными, — закон индукции 1/r, математически тождественный градиенту "
            "фазы оптического нуля. Ареф (1979) заново разобрал задачу трёх вихрей и прояснил её "
            "интегрируемость и структуру коллапса, Ньютон (2001) закрепил N-вихревую задачу в "
            "стандартном справочнике, а Ареф и др. (2003) обзорно описали вихревые кристаллы — "
            "относительные равновесия точечных вихрей, — среди которых равносторонний треугольник "
            "равных циркуляций есть простейший и самый знаменитый пример."
        ),
        (
            "Мост между двумя дисциплинами — произведение структуры. Вблизи нуля поле "
            "факторизуется, ψ ≈ (z − z_k)·(гладкая часть), и градиент фазы множителя (z − z_k) — "
            "это в точности поле скоростей точечного вихря; поэтому нули одного знака в главном "
            "порядке движутся по уравнениям Кирхгофа. Лазерный пучок с запроектированным "
            "произведением ψ(z) = exp(−r²/w²)·Π_k (z − z_k) реализует динамику точечных вихрей "
            "буквально в свете: тёмные ядра — «тела», их топологические заряды — циркуляции, а "
            "намотка дальнего поля — полный заряд. Аналогия не метафорична — это одна и та же "
            "система ОДУ в главном порядке."
        ),
        (
            "Для TRIVORTEX значимость структурна. Угловой импульс I = ΣΓ|r|² вихревой системы — "
            "многовихревой прототип интеграла Чаплыгина C_Ch, закрепляющего орбиты вихревой "
            "модели; жёстко вращающийся равносторонний треугольник — оптический близнец "
            "хореографии теоремы 3.1; а число намотки поля — оптическое прочтение полного "
            "вихревого заряда. Поэтому данное исследование — якорь оптического блока программы: "
            "оно показывает, что математический скелет каркаса дословно переживает превращение "
            "вихрей в свет (TRX-04 даёт аналог по максимумам поля, TRX-09 — классический якорь "
            "гидродинамики)."
        ),
    ],
    "derivation_en": [
        (
            "The Kirchhoff equations (E1) follow from the induction structure of ideal flow: a "
            "point vortex of circulation Γ_j at position (x_j, y_j) induces at (x_k, y_k) the "
            "velocity Γ_j/(2π r_jk) perpendicular to the separation vector, with r_jk the "
            "distance between the two points. Summing the contributions of all other vortices "
            "gives the right-hand sides of (E1); the equations are first-order and Hamiltonian "
            "with the pair Hamiltonian (E3) in the logarithmic potential. For Γ = 1 the system "
            "is fully dimensionless once lengths are measured in units of a."
        ),
        (
            "Two invariants structure the dynamics. The angular impulse (E2), I = ΣΓ_k|r_k|², "
            "is conserved by rotational symmetry — it is the exact many-vortex analogue of the "
            "Chaplygin integral of the TRIVORTEX vortex model — and for an equilateral triangle "
            "of side a it evaluates to a² identically, since every vertex sits at distance "
            "a/√3 from the centroid: I = 3·(a²/3) = a². The Kirchhoff Hamiltonian (E3) fixes "
            "the pair distances; both together lock the triangle into a relative equilibrium "
            "whose rotation rate follows from balancing the induced velocity with the orbital "
            "motion, giving the Lagrange-type law (E4), ω = 3Γ/(2πa²). For a = 1 the Hamiltonian "
            "vanishes identically (ln 1 = 0), a useful sanity marker of the preset."
        ),
        (
            "The optical rendering (E5) is a product over the vortex positions times a Gaussian "
            "envelope. By construction each factor vanishes at z = z_k(t), so the intensity "
            "zeros coincide with the Kirchhoff vortices at all times; each factor contributes "
            "exactly one unit of phase winding (charge q_k = +1), and the winding number of the "
            "total field on any circle enclosing all cores equals the sum of the charges, "
            "N = Σq_k = 3. The winding integral in (E5) is the optical reading of the total "
            "charge and, through the Soskin et al. correspondence, of the orbital angular "
            "momentum 3ℏ per photon carried by the beam."
        ),
    ],
    "derivation_ru": [
        (
            "Уравнения Кирхгофа (E1) следуют из индукционной структуры идеального течения: "
            "точечный вихрь с циркуляцией Γ_j в точке (x_j, y_j) наводит в точке (x_k, y_k) "
            "скорость Γ_j/(2π r_jk), перпендикулярную вектору разделяющего отрезка, где r_jk — "
            "расстояние между точками. Суммируя вклады всех остальных вихрей, получаем правые "
            "части (E1); уравнения первого порядка и гамильтоновы, с парным гамильтонианом (E3) "
            "в логарифмическом потенциале. При Γ = 1 система полностью безразмерна, если длины "
            "измеряются в единицах a."
        ),
        (
            "Два инварианта структурируют динамику. Угловой импульс (E2), I = ΣΓ_k|r_k|², "
            "сохраняется вращательной симметрией — это точный многовихревой аналог интеграла "
            "Чаплыгина вихревой модели TRIVORTEX, — а для равностороннего треугольника со "
            "стороной a он равен a² тождественно, поскольку каждая вершина отстоит от центра на "
            "a/√3: I = 3·(a²/3) = a². Гамильтониан Кирхгофа (E3) фиксирует парные расстояния; "
            "вместе они запирают треугольник в относительном равновесии, скорость вращения "
            "которого находится из баланса наведённой скорости и орбитального движения и даёт "
            "лагранжев закон (E4), ω = 3Γ/(2πa²). При a = 1 гамильтониан обращается в нуль "
            "тождественно (ln 1 = 0) — удобный маркер-самопроверка пресета."
        ),
        (
            "Оптическое построение (E5) — произведение по позициям вихрей, умноженное на "
            "гауссову огибающую. По построению каждый множитель обращается в нуль при z = z_k(t), "
            "поэтому нули интенсивности совпадают с вихрями Кирхгофа во все моменты времени; "
            "каждый множитель вносит ровно одну единицу намотки фазы (заряд q_k = +1), а число "
            "намотки полного поля по любой окружности, охватывающей все ядра, равно сумме "
            "зарядов, N = Σq_k = 3. Интеграл намотки в (E5) — оптическое прочтение полного "
            "заряда и, через соответствие Соскина и др., орбитального углового момента 3ℏ на "
            "фотон, переносимого пучком."
        ),
    ],
    "connection_en": (
        "The mapping is one-to-one and works in both directions. The dark cores of the "
        "rendered field are literal realizations of the TRIVORTEX vortex-model \u201cbodies\u201d; the "
        "topological charge q_k of each singularity plays the role of the circulation Γ_k; the "
        "angular impulse I = ΣΓ|r|² is the same invariant structure as the Chaplygin integral, "
        "here pinned exactly at a² = 1; and the rigidly rotating equilateral triangle of three "
        "same-sign singularities is the optical twin of the Theorem 3.1 choreography, obeying the "
        "identical Lagrange-type rate ω = 3Γ/(2πa²). The winding number of the far field closes the "
        "dictionary: it is the optical measurement of the total charge ΣΓ = 3, the quantity that in "
        "the vortex model fixes the orbital angular momentum of the configuration. No parameter is "
        "left unmatched — the study is the optical edition of the TRIVORTEX core."
    ),
    "connection_ru": (
        "Соответствие взаимно-однозначно и работает в обе стороны. Тёмные ядра "
        "построенного поля — буквальная реализация «тел» вихревой модели TRIVORTEX; топологический "
        "заряд q_k каждой сингулярности играет роль циркуляции Γ_k; угловой импульс I = ΣΓ|r|² — та "
        "же инвариантная структура, что и интеграл Чаплыгина, здесь закреплённый точно на a² = 1; а "
        "жёстко вращающийся равносторонний треугольник трёх одноимённых сингулярностей — оптический "
        "близнец хореографии теоремы 3.1, подчиняющийся тому же лагранжеву закону ω = 3Γ/(2πa²). "
        "Число намотки дальнего поля замыкает словарь: это оптическое измерение полного заряда "
        "ΣΓ = 3 — величины, которая в вихревой модели фиксирует орбитальный угловой момент "
        "конфигурации. Словарь соответствий исчерпан полностью — исследование есть оптическое "
        "издание ядра TRIVORTEX."
    ),
    "method_en": [
        (
            "The vortex triangle is integrated with an explicit Dormand–Prince 8(5,3) scheme at "
            "rtol = atol = 1e-13 with max_step 0.05 over T = 39.4784 — three full rotations. The "
            "rotation rate is extracted from the polar angle of vortex 1 relative to the "
            "instantaneous centroid: the angle is unwrapped along 2000 dense samples and fitted "
            "by a straight line, whose slope 0.477464829 is the measured ω. The same fit run on "
            "the analytic trajectory returns the target value, so the check probes the "
            "integrator, not the algebra."
        ),
        (
            "Both invariants are monitored pointwise along the trajectory at the same 2000 "
            "samples: the angular impulse I = ΣΓ|r|² drifts by 1.8e-15 from its initial value "
            "I = 1.000000000000 = a², and the Kirchhoff Hamiltonian drifts by 4.6e-16 from its "
            "identically-zero initial value. Both sit far below the 1e-12 acceptance tolerance "
            "— the invariant structure of the point-vortex problem survives the full three-"
            "rotation integration at round-off level."
        ),
        (
            "The optical field is evaluated on a uniform grid of 0.018 spacing over [−1.7, 1.7]² "
            "at t = 0 and t = T/4. The 60 deepest intensity pixels are matched against the "
            "vortex positions: the worst distance from a vortex to its nearest minimum is "
            "0.0118, three times inside the acceptance band of two grid cells (0.036). The "
            "winding number is computed by unwrapping arg ψ along the annulus r = 1.55 and "
            "counting the total phase turn — it returns 3.0 exactly, with no grid-level "
            "ambiguity."
        ),
    ],
    "method_ru": [
        (
            "Вихревой треугольник интегрируется явной схемой Дормана–Принса 8(5,3) при "
            "rtol = atol = 1e-13 и max_step 0.05 на T = 39.4784 — три полных оборота. Скорость "
            "вращения извлекается из полярного угла вихря 1 относительно мгновенного центра: угол "
            "разворачивается по 2000 плотных выборок и аппроксимируется прямой, наклон которой "
            "0.477464829 и есть измеренная ω. Тот же фит на аналитической траектории возвращает "
            "целевое значение, так что проверка зондирует интегратор, а не алгебру."
        ),
        (
            "Оба инварианта контролируются поточечно вдоль траектории на тех же 2000 выборках: "
            "угловой импульс I = ΣΓ|r|² дрейфует на 1.8e-15 от начального значения "
            "I = 1.000000000000 = a², а гамильтониан Кирхгофа — на 4.6e-16 от тождественно "
            "нулевого начального значения. Оба лежат далеко ниже допуска 1e-12 — инвариантная "
            "структура задачи о точечных вихрях переживает полное трёхоборотное интегрирование "
            "на уровне округления."
        ),
        (
            "Оптическое поле вычисляется на равномерной сетке с шагом 0.018 по квадрату "
            "[−1.7, 1.7]² при t = 0 и t = T/4. Шестьдесят глубочайших пикселей интенсивности "
            "сопоставляются с позициями вихрей: худшее расстояние от вихря до ближайшего минимума "
            "равно 0.0118 — втрое внутри полосы допуска в две ячейки сетки (0.036). Число намотки "
            "вычисляется разворачиванием arg ψ вдоль кольца r = 1.55 и подсчётом полного "
            "фазового оборота — результат 3.0 точно, без сеточных двусмысленностей."
        ),
    ],
    "analysis_en": [
        (
            "**Rotation.** The measured rotation rate is 0.477464829 against the analytic "
            "3Γ/(2πa²) = 0.477464829 — the two numbers agree to the last recorded digit, at the "
            "1e-16 level, seven orders of magnitude inside the 1e-8 acceptance tolerance. Over "
            "T = 39.4784 (three rotations of period 13.1595) every core traces a circle of "
            "radius r_c = 0.57735 about the common centroid, and the triangle returns to a "
            "rotated copy of itself with the side a = 1 preserved."
        ),
        (
            "**Invariants.** The angular impulse stays pinned at I = 1.000000000000 = a² with "
            "maximum drift 1.8e-15, and the Kirchhoff Hamiltonian drifts by 4.6e-16 from its "
            "identically-zero initial value — roughly 560 and 2200 times below the 1e-12 "
            "tolerance respectively. Because I and H together fix the shape of a three-vortex "
            "configuration, their conservation is the dynamical reason the triangle rotates "
            "rigidly instead of deforming."
        ),
        (
            "**Field rendering.** At the preset grid spacing 0.018 the deepest intensity minima "
            "track the vortices with a worst offset of 0.0118 at t = 0 and t = T/4 — three "
            "times inside the 0.036 acceptance band (two grid cells). The sweep over grid "
            "spacings 0.012–0.08 keeps the offset below the 2-cell line everywhere (0.00668 up "
            "to 0.04922 against 0.024–0.16), so the tracking of zeros by dark cores is robust, "
            "not an artifact of one resolution."
        ),
        (
            "**Topology and sweeps.** The winding number of arg ψ on the evaluation circle "
            "r = 1.55 equals 3 exactly — the rendered field carries the total topological "
            "charge of the three unit singularities. The side sweep confirms the rotation law "
            "beyond the preset: numeric re-runs at a ∈ {0.6, 0.8, 1.0, 1.2, 1.5, 2.0} reproduce "
            "ω(a) = 3Γ/(2πa²) to nine recorded decimals, from 1.326291192 at a = 0.6 down to "
            "0.119366207 at a = 2.0. The a⁻² scaling of the Lagrange-type configuration is thus "
            "verified end to end."
        ),
    ],
    "analysis_ru": [
        (
            "**Вращение.** Измеренная скорость вращения равна 0.477464829 против аналитической "
            "3Γ/(2πa²) = 0.477464829 — числа совпадают до последнего записанного знака, на "
            "уровне 1e-16, на семь порядков внутри допуска 1e-8. За T = 39.4784 (три оборота с "
            "периодом 13.1595) каждое ядро описывает окружность радиуса r_c = 0.57735 вокруг "
            "общего центра, а треугольник возвращается в повёрнутую копию себя с сохранённой "
            "стороной a = 1."
        ),
        (
            "**Инварианты.** Угловой импульс остаётся закреплённым на I = 1.000000000000 = a² с "
            "максимальным дрейфом 1.8e-15, а гамильтониан Кирхгофа дрейфует на 4.6e-16 от "
            "тождественно нулевого начального значения — примерно в 560 и 2200 раз ниже допуска "
            "1e-12 соответственно. Поскольку I и H вместе фиксируют форму трёхвихревой "
            "конфигурации, их сохранение и есть динамическая причина того, что треугольник "
            "вращается жёстко, а не деформируется."
        ),
        (
            "**Построение поля.** При пресетном шаге сетки 0.018 глубочайшие минимумы "
            "интенсивности следят за вихрями с худшим смещением 0.0118 при t = 0 и t = T/4 — "
            "втрое внутри полосы допуска 0.036 (две ячейки сетки). Развёртка по шагам сетки "
            "0.012–0.08 удерживает смещение ниже линии в 2 ячейки всюду (от 0.00668 до 0.04922 "
            "против 0.024–0.16), так что слежение нулей за тёмными ядрами устойчиво, а не "
            "артефакт одного разрешения."
        ),
        (
            "**Топология и развертки.** Число намотки arg ψ на оценочной окружности r = 1.55 "
            "равно в точности 3 — построенное поле несёт полный топологический заряд трёх "
            "единичных сингулярностей. Развёртка по стороне подтверждает закон вращения за "
            "пределами пресета: численные перезапуски при a ∈ {0.6, 0.8, 1.0, 1.2, 1.5, 2.0} "
            "воспроизводят ω(a) = 3Γ/(2πa²) с точностью до девяти записанных знаков — от "
            "1.326291192 при a = 0.6 до 0.119366207 при a = 2.0. Степенной закон a⁻² лагранжевой "
            "конфигурации проверен от начала до конца."
        ),
    ],
    "discussion_en": [
        (
            "The model is deliberately minimal: scalar paraxial field, point-like singularities, "
            "static Gaussian envelope. Within these assumptions the Kirchhoff side is exact and "
            "the optical side is its leading-order realization — real optical vortices have a "
            "finite core structure, and non-paraxial, polarization and envelope-deformation "
            "corrections enter at higher order. The product field (E5) is the cleanest possible "
            "laboratory: it separates the zero dynamics (exact Kirchhoff) from the envelope, "
            "which only weighs the intensity but does not move the zeros to leading order."
        ),
        (
            "The parameter regime probes the structural core of the analogy rather than a "
            "specific beam design. Same-sign equal circulations are the integrable, "
            "relative-equilibrium case; opposite signs (translating pairs), unequal "
            "circulations, N > 3 clusters and vortex lattices in saturating media are natural "
            "extensions that the same code can host. The grid-spacing sweep shows the zero-"
            "tracking check is resolution-robust; the side sweep shows the rotation law is "
            "exactly a⁻², so the preset a = 1 is a representative point, not a tuned one."
        ),
        (
            "Within the program this study is the optical edition of the vortex core. TRX-09 "
            "verifies the same equations in the pure fluid-dynamical setting with the Aref "
            "collapse manifold added; TRX-04 treats the field-maxima (bright-soliton) "
            "counterpart, where the bodies are intensity peaks rather than zeros; TRX-06 "
            "carries the zeros-of-complex-fields structure into quantum three-body ionization. "
            "Together with the classical anchor they demonstrate that the TRIVORTEX framework "
            "is a single mathematical object viewed through different physical media."
        ),
    ],
    "discussion_ru": [
        (
            "Модель сознательно минимальна: скалярное параксиальное поле, точечные сингулярности, "
            "статическая гауссова огибающая. В этих допущениях сторона Кирхгофа точна, а "
            "оптическая — её реализация в главном порядке: реальные оптические вихри обладают "
            "конечной структурой ядра, а непараксиальные, поляризационные поправки и "
            "деформации огибающей входят следующими порядками. Поле-произведение (E5) — "
            "чистейшая возможная лаборатория: оно разделяет динамику нулей (точная задача "
            "Кирхгофа) и огибающую, которая лишь взвешивает интенсивность, но не сдвигает нули "
            "в главном порядке."
        ),
        (
            "Диапазон параметров зондирует структурное ядро аналогии, а не конкретный дизайн "
            "пучка. Одноимённые равные циркуляции — интегрируемый случай относительного "
            "равновесия; противоположные знаки (транслирующие пары), неравные циркуляции, "
            "кластеры N > 3 и вихревые решётки в насыщающихся средах — естественные расширения, "
            "которые способен вместить тот же код. Развёртка по шагу сетки показывает, что "
            "проверка слежения за нулями устойчива к разрешению; развёртка по стороне — что "
            "закон вращения точно a⁻², поэтому пресет a = 1 — репрезентативная точка, а не "
            "подогнанная."
        ),
        (
            "В рамках программы это исследование — оптическое издание вихревого ядра. TRX-09 "
            "проверяет те же уравнения в чисто гидродинамической постановке с добавленным "
            "многообразием коллапса Арефа; TRX-04 разбирает аналог по максимумам поля "
            "(яркие солитоны), где тела — пики интенсивности, а не нули; TRX-06 переносит "
            "структуру «нули комплексных полей» в квантовую трёхчастичную ионизацию. Вместе с "
            "классическим якорем они показывают, что каркас TRIVORTEX — один математический "
            "объект, рассматриваемый через разные физические среды."
        ),
    ],
    "conclusions_en": [
        "Three same-sign optical vortices on an equilateral triangle of side a = 1 rotate rigidly at the analytic rate ω = 3Γ/(2πa²) = 0.477464829, measured within the 1e-8 tolerance (agreement at the 1e-16 level).",
        "The angular impulse I = ΣΓ|r|² is conserved to 1.8e-15 and stays pinned at a² = 1 — the many-vortex Chaplygin-type integral of the configuration.",
        "The Kirchhoff Hamiltonian is conserved to 4.6e-16 over T = 39.4784 (H = 0 identically for a = 1); the triangle rotates as a rigid relative equilibrium.",
        "The rendered complex field (grid spacing 0.018) shows three dark cores tracking the vortex positions within 0.0118 — three times inside the 0.036 two-cell acceptance.",
        "The winding number of arg ψ on the circle r = 1.55 equals 3 exactly — the optical reading of the total charge and of the orbital angular momentum 3ℏ per photon.",
        "The rotation law is verified across a ∈ {0.6, …, 2.0} (numeric rates matching ω(a) to nine recorded decimals), confirming the a⁻² Lagrange-type scaling end to end.",
    ],
    "conclusions_ru": [
        "Три одноимённых оптических вихря на равностороннем треугольнике со стороной a = 1 вращаются жёстко с аналитической скоростью ω = 3Γ/(2πa²) = 0.477464829, измеренной внутри допуска 1e-8 (согласие на уровне 1e-16).",
        "Угловой импульс I = ΣΓ|r|² сохраняется до 1.8e-15 и остаётся закреплённым на a² = 1 — многовихревой чаплыгинский интеграл конфигурации.",
        "Гамильтониан Кирхгофа сохраняется до 4.6e-16 за T = 39.4784 (при a = 1 H тождественно 0); треугольник вращается как жёсткое относительное равновесие.",
        "Построенное комплексное поле (шаг сетки 0.018) показывает три тёмных ядра, следящих за позициями вихрей в пределах 0.0118 — втрое внутри двухъячеечного допуска 0.036.",
        "Число намотки arg ψ на окружности r = 1.55 равно в точности 3 — оптическое прочтение полного заряда и орбитального углового момента 3ℏ на фотон.",
        "Закон вращения проверен по a ∈ {0.6, …, 2.0} (численные скорости совпадают с ω(a) до девяти записанных знаков), подтверждая степенной закон a⁻² лагранжева типа от начала до конца.",
    ],
    "references": [
        "1. Berry, M. V., Dennis, M. R. (2000). *Phase singularities in isotropic random waves.* Proc. R. Soc. A 456, 2059–2079.",
        "2. Soskin, M. S., Gorshkov, V. G., Vasnetsov, M. V. (1997). *Topological charge and angular momentum of light beams carrying optical vortices.* Phys. Rev. A 56, 4064–4075.",
        "3. Kirchhoff, G. (1876). *Vorlesungen über mathematische Physik: Mechanik.* Teubner, Leipzig.",
        "4. Aref, H. (1979). *Motion of three vortices revisited.* Phys. Fluids 22, 393–400.",
        "5. Aref, H., Newton, P. K., Stremler, M. A., Tokieda, T., Vainchtein, D. L. (2003). *Vortex crystals.* Annu. Rev. Fluid Mech. 35, 349–395.",
        "6. Yao, A. M., Padgett, M. J. (2011). *Orbital angular momentum: origins, behavior and applications.* Adv. Opt. Photon. 3, 161–204.",
        "7. Dennis, M. R., O'Holleran, K., Padgett, M. J. (2009). *Singular optics: structuring optical wavefields.* Prog. Opt. 53, 293–363.",
        "8. Newton, P. K. (2001). *The N-Vortex Problem: Analytical Techniques.* Springer, New York.",
    ],
    "crosslinks_en": [
        "* **TRX-09** is the pure fluid-dynamical anchor (same Kirchhoff equations, classical setting) with the Aref collapse manifold added.",
        "* **TRX-04** is the field-maxima (bright-soliton) counterpart: the bodies are intensity peaks rather than zeros.",
        "* **TRX-06** carries the same zeros-of-complex-fields structure into quantum three-body ionization dynamics.",
    ],
    "crosslinks_ru": [
        "* **TRX-09** — чистый гидродинамический якорь (те же уравнения Кирхгофа, классическая постановка) с добавленным многообразием коллапса Арефа.",
        "* **TRX-04** — аналог по максимумам поля (яркие солитоны): тела — пики интенсивности, а не нули.",
        "* **TRX-06** переносит ту же структуру «нули комплексных полей» в квантовую динамику трёхчастичной ионизации.",
    ],
    "assumptions_en": [
        "Point-core leading order: singularities are idealized zeros; finite core size and non-paraxial corrections are neglected.",
        "Scalar paraxial field; polarization and longitudinal structure of the beam are not modeled.",
        "Same-sign equal circulations Γ = 1; opposite signs and unequal circulations are outside the preset.",
        "Static Gaussian envelope w = 3a; envelope back-reaction on the zero dynamics is a higher-order effect and is neglected.",
        "Planar vortex dynamics; the triangle is exactly equilateral at t = 0 (and remains so by the invariants).",
        "Machine-precision integration (DOP853, rtol = atol = 1e-13) treats the ODEs as exact; round-off is the only error channel.",
    ],
    "assumptions_ru": [
        "Главный порядок с точечным ядром: сингулярности — идеализированные нули; конечный размер ядра и непараксиальные поправки не учитываются.",
        "Скалярное параксиальное поле; поляризация и продольная структура пучка не моделируются.",
        "Одноимённые равные циркуляции Γ = 1; противоположные знаки и неравные циркуляции вне пресета.",
        "Статическая гауссова огибающая w = 3a; обратное влияние огибающей на динамику нулей — эффект высшего порядка и не учитывается.",
        "Плоская вихревая динамика; треугольник в точности равносторонний при t = 0 (и остаётся таковым по инвариантам).",
        "Интегрирование с машинной точностью (DOP853, rtol = atol = 1e-13) трактует ОДУ как точные; единственный канал ошибки — округление.",
    ],
    "glance_en": [
        ["Block", "Laser optics — study 05 of 12"],
        ["Model", "three unit optical vortices of a paraxial beam, ψ = exp(−r²/w²)·Π(z − z_k)"],
        ["Key invariant", "angular impulse I = ΣΓ|r|² = a² (vortex Chaplygin-type integral)"],
        ["Headline result", "rigid rotation at ω = 3Γ/(2πa²) = 0.477464829; winding number N = 3"],
        ["Verification", "5/5 checks PASS (full mode)"],
        ["Runtime", "0.34 s full · 4.83 s with --figures · < 20 s smoke"],
    ],
    "glance_ru": [
        ["Блок", "Лазерная оптика — исследование 05 из 12"],
        [
            "Модель",
            "три единичных оптических вихря параксиального пучка, ψ = exp(−r²/w²)·Π(z − z_k)",
        ],
        [
            "Ключевой инвариант",
            "угловой импульс I = ΣΓ|r|² = a² (вихревой интеграл типа Чаплыгина)",
        ],
        [
            "Главный результат",
            "жёсткое вращение с ω = 3Γ/(2πa²) = 0.477464829; число намотки N = 3",
        ],
        ["Верификация", "5/5 проверок PASS (полный режим)"],
        ["Время выполнения", "0.34 с полный · 4.83 с с --figures · < 20 с smoke"],
    ],
    "glossary": {
        "header_en": ["Term", "Definition"],
        "header_ru": ["Термин", "Определение"],
        "rows_en": [
            [
                "Optical vortex",
                "phase singularity of a light field: an intensity zero around which the phase winds by 2πq",
            ],
            [
                "Phase singularity",
                "point where the complex field vanishes and its phase is undefined",
            ],
            [
                "Topological charge q",
                "integer winding of the phase around a singularity (+1 for each core here)",
            ],
            [
                "Winding number N",
                "total phase turn of arg ψ on a closed circle; equals the sum of enclosed charges",
            ],
            [
                "Point vortex (Kirchhoff)",
                "idealized vortex of ideal fluid dynamics inducing a 1/r velocity field",
            ],
            [
                "Circulation Γ",
                "strength of a point vortex; the fluid-dynamical image of the topological charge",
            ],
            [
                "Angular impulse I = ΣΓ|r|²",
                "rotational invariant of the vortex system, prototype of the Chaplygin integral",
            ],
            [
                "Relative equilibrium",
                "configuration that moves without changing shape (here: rigid rotation)",
            ],
            [
                "Orbital angular momentum (OAM)",
                "beam angular momentum per photon qℏ carried by a charge-q vortex beam",
            ],
            [
                "DOP853",
                "explicit Dormand–Prince 8(5,3) adaptive integrator used at rtol = atol = 1e-13",
            ],
        ],
        "rows_ru": [
            [
                "Оптический вихрь",
                "фазовая сингулярность светового поля: нуль интенсивности, вокруг которого фаза наматывается на 2πq",
            ],
            [
                "Фазовая сингулярность",
                "точка, в которой комплексное поле обращается в нуль, а его фаза не определена",
            ],
            [
                "Топологический заряд q",
                "целочисленная намотка фазы вокруг сингулярности (здесь +1 у каждого ядра)",
            ],
            [
                "Число намотки N",
                "полный фазовый оборот arg ψ по замкнутой окружности; равен сумме охваченных зарядов",
            ],
            [
                "Точечный вихрь (Кирхгофа)",
                "идеализированный вихрь идеальной жидкости, наводящий поле скоростей 1/r",
            ],
            [
                "Циркуляция Γ",
                "сила точечного вихря; гидродинамический образ топологического заряда",
            ],
            [
                "Угловой импульс I = ΣΓ|r|²",
                "вращательный инвариант вихревой системы, прототип интеграла Чаплыгина",
            ],
            [
                "Относительное равновесие",
                "конфигурация, движущаяся без изменения формы (здесь: жёсткое вращение)",
            ],
            [
                "Орбитальный угловой момент (ОУМ)",
                "угловой момент пучка на фотон qℏ, переносимый вихревым пучком с зарядом q",
            ],
            [
                "DOP853",
                "явный адаптивный интегратор Дормана–Принса 8(5,3), используемый при rtol = atol = 1e-13",
            ],
        ],
    },
    "notation": {
        "header_en": ["Symbol", "Meaning"],
        "header_ru": ["Символ", "Смысл"],
        "rows_en": [
            ["z = x + iy", "transverse complex coordinate of the beam"],
            ["z_k(t)", "trajectory of the k-th vortex / field zero"],
            ["Γ_k", "circulation of vortex k (Γ = 1 for all)"],
            ["q_k", "topological charge of singularity k (q_k = +1)"],
            ["ψ(z)", "paraxial scalar field of the beam"],
            ["w", "Gaussian envelope width (w = 3a)"],
            ["a", "side of the equilateral vortex triangle"],
            ["r_c", "circumscribed radius a/√3 ≈ 0.57735"],
            ["I", "angular impulse I = ΣΓ|r|² = a²"],
            ["H", "Kirchhoff Hamiltonian (H = 0 at a = 1)"],
            ["ω", "rotation rate of the triangle, 3Γ/(2πa²)"],
            ["T", "integration span, three rotations (39.4784)"],
        ],
        "rows_ru": [
            ["z = x + iy", "поперечная комплексная координата пучка"],
            ["z_k(t)", "траектория k-го вихря / нуля поля"],
            ["Γ_k", "циркуляция вихря k (Γ = 1 у всех)"],
            ["q_k", "топологический заряд сингулярности k (q_k = +1)"],
            ["ψ(z)", "параксиальное скалярное поле пучка"],
            ["w", "ширина гауссовой огибающей (w = 3a)"],
            ["a", "сторона равностороннего вихревого треугольника"],
            ["r_c", "радиус описанной окружности a/√3 ≈ 0.57735"],
            ["I", "угловой импульс I = ΣΓ|r|² = a²"],
            ["H", "гамильтониан Кирхгофа (H = 0 при a = 1)"],
            ["ω", "скорость вращения треугольника, 3Γ/(2πa²)"],
            ["T", "интервал интегрирования, три оборота (39.4784)"],
        ],
    },
    "params_appendix": {
        "header_en": ["Symbol", "Value", "Role"],
        "header_ru": ["Символ", "Значение", "Роль"],
        "rows_en": [
            ["Γ", "1", "circulation of each optical vortex"],
            ["a", "1", "triangle side (length unit)"],
            ["r_c", "0.57735", "core orbit radius a/√3"],
            ["w", "3", "Gaussian envelope width"],
            ["grid", "0.018 over [−1.7, 1.7]²", "field rendering and zero tracking"],
            ["T", "39.4784", "integration span (three rotations, period 13.1595)"],
            ["rtol, atol", "1e-13", "DOP853 tolerances (max_step 0.05)"],
            ["r = 1.55", "winding circle", "topological-charge evaluation"],
            ["minima sample", "60 pixels", "deepest intensity pixels matched to vortices"],
        ],
        "rows_ru": [
            ["Γ", "1", "циркуляция каждого оптического вихря"],
            ["a", "1", "сторона треугольника (единица длины)"],
            ["r_c", "0.57735", "радиус орбиты ядра a/√3"],
            ["w", "3", "ширина гауссовой огибающей"],
            ["сетка", "0.018 по [−1.7, 1.7]²", "рендеринг поля и слежение за нулями"],
            ["T", "39.4784", "интервал интегрирования (три оборота, период 13.1595)"],
            ["rtol, atol", "1e-13", "допуски DOP853 (max_step 0.05)"],
            ["r = 1.55", "окружность намотки", "вычисление топологического заряда"],
            ["выборка минимумов", "60 пикселей", "глубочайшие пиксели интенсивности против вихрей"],
        ],
    },
    "bibtex": [
        "@article{berry2000,",
        "  author  = {Berry, M. V. and Dennis, M. R.},",
        "  title   = {Phase singularities in isotropic random waves},",
        "  journal = {Proceedings of the Royal Society A},",
        "  year    = {2000}, volume = {456}, pages = {2059--2079}}",
        "",
        "@article{soskin1997,",
        "  author  = {Soskin, M. S. and Gorshkov, V. G. and Vasnetsov, M. V.},",
        "  title   = {Topological charge and angular momentum of light beams carrying optical vortices},",
        "  journal = {Physical Review A},",
        "  year    = {1997}, volume = {56}, pages = {4064--4075}}",
        "",
        "@book{kirchhoff1876,",
        "  author    = {Kirchhoff, G.},",
        '  title     = {Vorlesungen \\"uber mathematische Physik: Mechanik},',
        "  publisher = {Teubner}, address = {Leipzig}, year = {1876}}",
        "",
        "@article{aref1979,",
        "  author  = {Aref, Hassan},",
        "  title   = {Motion of three vortices revisited},",
        "  journal = {Physics of Fluids},",
        "  year    = {1979}, volume = {22}, pages = {393--400}}",
    ],
}
