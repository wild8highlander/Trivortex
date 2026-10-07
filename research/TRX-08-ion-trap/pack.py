# -*- coding: utf-8 -*-
"""Content pack for TRX-08 (v1.0.0 Monograph Edition). Rendered by scripts/build_study_docs.py."""

PACK = {
    "meta": {
        "study_id": "TRX-08",
        "dir_name": "TRX-08-ion-trap",
        "title_en": "Three Laser-Cooled Ions in a Linear Paul Trap: the Table-Top Lagrange Triangle",
        "title_ru": "Три лазерно-охлаждённых иона в линейной ловушке Пауля: настольный треугольник Лагранжа",
        "script": "trx08_ion_trap.py",
        "results_json": "trx08_results.json",
        "scheme_file": "scheme_trx08.svg",
        "runtime_full": "6.79 s (6.794 s recorded with --figures)",
    },
    "essence_en": (
        "Three laser-cooled ions in the transverse plane of a linear Paul trap form a "
        "table-top three-body problem: a two-dimensional harmonic rf pseudopotential confines "
        "them, their mutual Coulomb repulsion pushes them apart, and Doppler cooling — modelled "
        "as a linear drag −γ_d·v — dissipates energy until the ions crystallize into the "
        "equilateral **Lagrange triangle** of side a = (3κ/ω₀²)^(1/3) = 3^(1/3) = 1.4422495703. "
        "The study verifies the whole chain to machine precision: sides equal to 4.4e-16, "
        "central angles 2π/3 to 4.4e-16, the normal-mode ladder {0, ω₀ (×2), √(3/2)ω₀ (×2), "
        "√3ω₀} confirmed to 1.4·10⁻⁸, and a conservative hold at the exact equilibrium that "
        "keeps the crystal static to 3.9e-15 over fifty time units with energy drift 8.9e-16 — "
        "the trapped-ion twin of the Lagrange relative equilibrium behind TRIVORTEX Theorem 3.1 "
        "and the smallest ion-crystal quantum simulator."
    ),
    "essence_ru": (
        "Три лазерно-охлаждённых иона в поперечной плоскости линейной ловушки Пауля "
        "образуют настольную задачу трёх тел: двумерный гармонический радиочастотный "
        "псевдопотенциал удерживает их, кулоновское отталкивание расталкивает, а доплеровское "
        "охлаждение — в модели линейного трения −γ_d·v — рассеивает энергию, пока ионы не "
        "кристаллизуются в равносторонний **треугольник Лагранжа** со стороной "
        "a = (3κ/ω₀²)^(1/3) = 3^(1/3) = 1.4422495703. Исследование проверяет всю цепочку с "
        "машинной точностью: стороны равны с точностью 4.4e-16, центральные углы 2π/3 с "
        "точностью 4.4e-16, лестница нормальных мод {0, ω₀ (×2), √(3/2)ω₀ (×2), √3ω₀} "
        "подтверждена на уровне 1.4·10⁻⁸, а консервативный прогон, стартующий точно в "
        "положении равновесия, держит кристалл статичным на уровне 3.9e-15 на протяжении "
        "пятидесяти единиц времени с дрейфом энергии 8.9e-16 — ионно-ловушечный близнец "
        "лагранжева относительного равновесия, лежащего в основе теоремы 3.1 TRIVORTEX, "
        "и наименьший ионно-кристаллический квантовый симулятор."
    ),
    "mission_en": [
        (
            "Ion traps turn the three-body problem into an afternoon experiment. Three laser-cooled "
            "ions spontaneously arrange into an equilateral triangle whose size is fixed by one "
            "algebraic force balance, a³ = 3κ/ω₀², and whose vibrational spectrum is pure group "
            "theory: one zero mode, two centre-of-mass translations, two quadrupole deformations "
            "and one breathing mode. For TRIVORTEX this is a new realization of the central-"
            "configuration logic: two competing scales — harmonic confinement versus Coulomb "
            "repulsion here, vortex attraction versus Abel–Hertz flux there — fix the size of the "
            "same equilateral triad, and the trapped crystal is the table-top twin of the Lagrange "
            "relative equilibrium of Theorem 3.1."
        ),
        (
            "The study verifies that chain end to end. A damped inertial relaxation from a seeded "
            "random start (with a documented finite-wavepacket softening ε_relax = 0.05) is "
            "Newton-polished on the strict unsoftened force balance and lands on the exact triangle "
            "a = 3^(1/3) = 1.44224957 — sides equal to 4.4e-16, central angles 2π/3 to 4.4e-16, and "
            "the potential equal to the analytic triangle energy U* = 3.120125734578 exactly. The "
            "finite-difference Hessian confirms the full mode ladder to 1.4·10⁻⁸, and a "
            "conservative run started exactly at equilibrium holds it statically to 3.9e-15 over "
            "fifty time units with energy drift 8.9e-16: the ion crystal is a frozen choreography. "
            "Independent re-runs additionally reproduce the scaling law a(κ) = (3κ/ω₀²)^(1/3) and "
            "map the crystallization time across the Doppler-drag range."
        ),
    ],
    "mission_ru": [
        (
            "Ионные ловушки превращают задачу трёх тел в эксперимент одного дня. Три "
            "лазерно-охлаждённых иона самопроизвольно выстраиваются в равносторонний треугольник, "
            "размер которого задаёт один алгебраический баланс сил a³ = 3κ/ω₀², а вибрационный "
            "спектр — чистая теория групп: одна нулевая мода, два трансляционных движения центра "
            "масс, две квадрупольные деформации и одна дыхательная мода. Для TRIVORTEX это новая "
            "реализация логики центральных конфигураций: две конкурирующие шкалы — гармоническое "
            "удержание против кулоновского отталкивания здесь, вихревое притяжение против потока "
            "Абеля–Хертца там — фиксируют размер одной и той же равносторонней триады, а "
            "захваченный кристалл — настольный близнец лагранжева относительного равновесия из "
            "теоремы 3.1."
        ),
        (
            "Исследование проверяет эту цепочку от начала до конца. Демпфированная инерциальная "
            "релаксация из засеянного случайного старта (с документированным смягчением конечного "
            "волнового пакета ε_relax = 0.05) полируется методом Ньютона на строгом несмягчённом "
            "балансе сил и приходит в точный треугольник a = 3^(1/3) = 1.44224957 — стороны равны "
            "с точностью 4.4e-16, центральные углы 2π/3 с точностью 4.4e-16, а потенциал в точности "
            "равен аналитической энергии треугольника U* = 3.120125734578. Конечно-разностный "
            "гессиан подтверждает полную лестницу мод на уровне 1.4·10⁻⁸, а консервативный прогон, "
            "стартующий точно в равновесии, держит его статичным на уровне 3.9e-15 на протяжении "
            "пятидесяти единиц времени с дрейфом энергии 8.9e-16: ионный кристалл — замороженная "
            "хореография. Дополнительные независимые прогоны воспроизводят закон масштабирования "
            "a(κ) = (3κ/ω₀²)^(1/3) и картируют время кристаллизации по диапазону доплеровского "
            "трения."
        ),
    ],
    "physics_en": [
        (
            "Three equal ions move in the transverse (x, y) plane of a linear Paul trap. The "
            "time-averaged rf pseudopotential is harmonic in the plane, U_trap = mω₀²r²/2; the "
            "mutual Coulomb repulsion κ/rij pushes the ions apart; the Doppler-cooling lasers are "
            "modelled by a linear drag −γ_d·v. The dynamics is two-dimensional and dimensionless "
            "with ω₀ = κ = m = 1, the state interleaved as [x₁, y₁, v₁ˣ, v₁ʸ, …] for the three "
            "ions, and the Coulomb force is softened as κ·r/(r² + ε²)^(3/2) with a documented "
            "ε during the relaxation stage."
        ),
        (
            "Two competing length scales leave a single dimensionless combination κ/ω₀² that fixes "
            "the crystal size: at the equilateral configuration each ion feels a radially outward "
            "Coulomb push √3κ/a² and an inward trap pull ω₀²a/√3, so the balance gives "
            "a = (3κ/ω₀²)^(1/3) — 3^(1/3) = 1.4422495703 for the preset. Because the trap is "
            "isotropic, the orientation of the triangle is free — this is exactly the zero Hessian "
            "mode. During cooling the energy is dissipated, but the trap is static in the lab "
            "frame, so the crystal is a static equilibrium: with γ_d = 0 and zero initial velocity "
            "the conservative dynamics K + U keeps it frozen."
        ),
    ],
    "physics_ru": [
        (
            "Три одинаковых иона движутся в поперечной плоскости (x, y) линейной ловушки Пауля. "
            "Усреднённый по времени радиочастотный псевдопотенциал в плоскости гармоничен, "
            "U_лов = mω₀²r²/2; кулоновское отталкивание κ/rij расталкивает ионы; лазеры "
            "доплеровского охлаждения моделируются линейным трением −γ_d·v. Динамика двумерная и "
            "безразмерная, ω₀ = κ = m = 1, состояние чередуется как [x₁, y₁, v₁ˣ, v₁ʸ, …] для трёх "
            "ионов, а кулоновская сила смягчается как κ·r/(r² + ε²)^(3/2) с документированным ε на "
            "стадии релаксации."
        ),
        (
            "Две конкурирующие шкалы длины оставляют одну безразмерную комбинацию κ/ω₀², задающую "
            "размер кристалла: в равносторонней конфигурации каждый ион испытывает радиально "
            "наружу кулоновский толчок √3κ/a² и внутрь гармоническую тягу ω₀²a/√3, поэтому баланс "
            "даёт a = (3κ/ω₀²)^(1/3) — 3^(1/3) = 1.4422495703 для пресета. Поскольку ловушка "
            "изотропна, ориентация треугольника свободна — это и есть нулевая мода гессиана. При "
            "охлаждении энергия рассеивается, но ловушка статична в лабораторной системе, поэтому "
            "кристалл — статическое равновесие: при γ_d = 0 и нулевой начальной скорости "
            "консервативная динамика сохраняет энергию K + U и держит его замороженным."
        ),
    ],
    "preset_table": {
        "header_en": ["Parameter", "Value", "Meaning"],
        "header_ru": ["Параметр", "Значение", "Смысл"],
        "rows_en": [
            ["ω₀, κ, m", "1, 1, 1", "dimensionless trap frequency, Coulomb strength, ion mass"],
            [
                "state",
                "interleaved [x₁, y₁, v₁ˣ, v₁ʸ, …]",
                "three ions in the transverse trap plane",
            ],
            ["initial condition", "seeded random in [−1, 1]², zero velocities", "rng seed 3"],
            [
                "cooling",
                "γ_d = 0.8, linear drag −γ_d·v",
                "Doppler-cooling model, relaxation stage only",
            ],
            [
                "softening",
                "ε_relax = 0.05, polish at ε = 1e-12",
                "finite cooled wavepacket → strict force balance",
            ],
            [
                "time spans",
                "T_relax = 60, T_hold = 50",
                "crystallization window and conservative hold",
            ],
            [
                "Ca⁺ mapping",
                "m = 40 amu, trap 1 MHz",
                "physical scale; κ sets the trap length scale",
            ],
        ],
        "rows_ru": [
            ["ω₀, κ, m", "1, 1, 1", "безразмерные частота ловушки, кулоновская сила, масса иона"],
            [
                "состояние",
                "чередование [x₁, y₁, v₁ˣ, v₁ʸ, …]",
                "три иона в поперечной плоскости ловушки",
            ],
            [
                "начальное условие",
                "засеянный случай в [−1, 1]², нулевые скорости",
                "зерно генератора 3",
            ],
            [
                "охлаждение",
                "γ_d = 0.8, линейное трение −γ_d·v",
                "модель доплеровского охлаждения, только стадия релаксации",
            ],
            [
                "смягчение",
                "ε_relax = 0.05, полировка при ε = 1e-12",
                "конечный охлаждённый волновой пакет → строгий баланс сил",
            ],
            [
                "интервалы времени",
                "T_relax = 60, T_hold = 50",
                "окно кристаллизации и консервативное удержание",
            ],
            [
                "отображение на Ca⁺",
                "m = 40 а.е.м., ловушка 1 МГц",
                "физический масштаб; κ задаёт масштаб длины ловушки",
            ],
        ],
    },
    "equations": [
        {
            "id": "E1",
            "latex": (
                "m\\ddot{\\mathbf{r}}_k = -m\\omega_0^2\\,\\mathbf{r}_k - \\gamma_d\\dot{\\mathbf{r}}_k "
                "+ \\kappa\\sum_{l\\ne k}\\frac{\\mathbf{r}_k-\\mathbf{r}_l}"
                "{\\bigl(|\\mathbf{r}_k-\\mathbf{r}_l|^2+\\epsilon^2\\bigr)^{3/2}}"
            ),
            "desc_en": "Dynamics of the three-ion crystal (harmonic trap + softened Coulomb repulsion + Doppler drag)",
            "desc_ru": "Динамика трёхионного кристалла (гармоническая ловушка + смягчённое кулоновское отталкивание + доплеровское трение)",
        },
        {
            "id": "E2",
            "latex": (
                "\\omega_0^2\\,\\frac{a}{\\sqrt{3}} = \\sqrt{3}\\,\\frac{\\kappa}{a^2}"
                "\\quad\\Longrightarrow\\quad a = \\left(\\frac{3\\kappa}{\\omega_0^2}\\right)^{1/3}"
                " = 3^{1/3} = 1.4422495703"
            ),
            "desc_en": "Equilateral force balance: the crystal side",
            "desc_ru": "Равновесие сил в равносторонней конфигурации: сторона кристалла",
        },
        {
            "id": "E3",
            "latex": "U(a) = \\tfrac{1}{2}\\omega_0^2 a^2 + \\frac{3\\kappa}{a},\\qquad U_* = \\tfrac{3}{2}\\cdot 3^{2/3} = 3.120125734578",
            "desc_en": "Energy along the equilateral family; its minimum is the force-balance side",
            "desc_ru": "Энергия вдоль равностороннего семейства; её минимум — сторона из баланса сил",
        },
        {
            "id": "E4",
            "latex": (
                "\\omega^2 = \\mathrm{eig}\\,\\frac{\\partial^2 U}{\\partial x_i\\,\\partial x_j},\\qquad "
                "\\omega \\in \\{0,\\ \\omega_0\\ (\\times 2),\\ \\sqrt{\\tfrac{3}{2}}\\,\\omega_0\\ (\\times 2),"
                "\\ \\sqrt{3}\\,\\omega_0\\}"
            ),
            "desc_en": "Normal-mode ladder: eigenvalues of the 6×6 position Hessian at the crystal",
            "desc_ru": "Лестница нормальных мод: собственные значения позиционного гессиана 6×6 в кристалле",
        },
        {
            "id": "E5",
            "latex": "\\mathbf{r}_k(0) = \\mathbf{r}_k^{*},\\ \\dot{\\mathbf{r}}_k(0) = 0,\\ \\gamma_d = 0\\ \\Longrightarrow\\ \\mathbf{r}_k(t) = \\mathbf{r}_k^{*}",
            "desc_en": "Static hold: the equilibrium is an exact solution of the conservative dynamics",
            "desc_ru": "Статическое удержание: равновесие — точное решение консервативной динамики",
        },
    ],
    "scheme_cap_en": (
        "TRX-08 scheme — three laser-cooled ions in the transverse plane of a linear Paul trap "
        "crystallize into the equilateral Lagrange triangle under Coulomb repulsion, harmonic "
        "confinement and Doppler drag; the normal-mode ladder and the mapping to the TRIVORTEX "
        "vortex model are shown on the right."
    ),
    "scheme_cap_ru": (
        "Схема TRX-08 — три лазерно-охлаждённых иона в поперечной плоскости линейной ловушки "
        "Пауля кристаллизуются в равносторонний треугольник Лагранжа под действием кулоновского "
        "отталкивания, гармонического удержания и доплеровского трения; справа показаны лестница "
        "нормальных мод и соответствие вихревой модели TRIVORTEX."
    ),
    "scheme_walk_en": [
        [
            "Four rf rods",
            "quadrupole electrode cross-section generating the harmonic pseudopotential U = mω₀²r²/2 (dashed equipotentials)",
        ],
        [
            "Three gold ions",
            "the equilateral crystal of side a = 3^(1/3) = 1.442249570 (trap length units)",
        ],
        [
            "Coulomb push vs trap pull",
            "force balance on an ion: two Coulomb pushes plus the harmonic pull sum to zero",
        ],
        [
            "Doppler-cooling beams (−γv)",
            "the laser drag that dissipates the binding energy ΔU = 1.7609 during crystallization",
        ],
        [
            "Normal-mode ladder",
            "0 (rigid rotation), ω₀ (×2, centre of mass), √(3/2)ω₀ (×2, quadrupole), √3ω₀ = 1.732051 (breathing)",
        ],
        [
            "Mapping strip",
            "crystal → Lagrange relative equilibrium; breathing → radial modulation of Theorem 3.1; zero mode → continuous choreography family",
        ],
    ],
    "scheme_walk_ru": [
        [
            "Четыре rf-стержня",
            "квадрупольное сечение электродов, создающее гармонический псевдопотенциал U = mω₀²r²/2 (пунктирные эквипотенциали)",
        ],
        [
            "Три золотых иона",
            "равносторонний кристалл со стороной a = 3^(1/3) = 1.442249570 (единицы длины ловушки)",
        ],
        [
            "Кулоновский толчок против тяги ловушки",
            "баланс сил на ионе: два кулоновских толчка плюс гармоническая тяга в сумме дают нуль",
        ],
        [
            "Пучки доплеровского охлаждения (−γv)",
            "лазерное трение, рассеивающее энергию связи ΔU = 1.7609 при кристаллизации",
        ],
        [
            "Лестница нормальных мод",
            "0 (жёсткое вращение), ω₀ (×2, центр масс), √(3/2)ω₀ (×2, квадруполь), √3ω₀ = 1.732051 (дыхательная)",
        ],
        [
            "Полоса соответствия",
            "кристалл → лагранжево относительное равновесие; дыхательная мода → радиальная модуляция теоремы 3.1; нулевая мода → непрерывное семейство хореографий",
        ],
    ],
    "mapping": {
        "header_en": ["Quantity in this study", "TRIVORTEX analog", "Comment"],
        "header_ru": ["Величина исследования", "Аналог в TRIVORTEX", "Комментарий"],
        "rows_en": [
            ["Ion crystal triangle", "Lagrange equilateral solution", "same central configuration"],
            [
                "Coulomb repulsion + harmonic trap",
                "vortex attractions + AH flux",
                "competing scales fix the size",
            ],
            [
                "Breathing mode √3ω₀",
                "radial modulation of Theorem 3.1",
                "collective breathing of the triad",
            ],
            [
                "Zero rotation mode",
                "continuous choreography family",
                "free orientation of the relative equilibrium",
            ],
        ],
        "rows_ru": [
            [
                "Треугольник ионного кристалла",
                "лагранжево равностороннее решение",
                "та же центральная конфигурация",
            ],
            [
                "Кулоновское отталкивание + гармоническая ловушка",
                "вихревые притяжения + поток АХ",
                "конкурирующие шкалы фиксируют размер",
            ],
            [
                "Дыхательная мода √3ω₀",
                "радиальная модуляция теоремы 3.1",
                "коллективное дыхание триады",
            ],
            [
                "Нулевая вращательная мода",
                "непрерывное семейство хореографий",
                "свободная ориентация относительного равновесия",
            ],
        ],
    },
    "nondim_en": (
        "Time in units of 1/ω₀, lengths in units of ℓ = (κ/mω₀²)^(1/3), energies in units "
        "of mω₀²ℓ² = κ/ℓ. The preset sets ω₀ = κ = m = 1, so the crystal side is a = 3^(1/3) = "
        "1.4422495703 and its energy U* = 1.5·3^(2/3) = 3.120125734578. The trap is isotropic, "
        "so the crystal orientation is free (the zero mode); for a Ca⁺ ion (m = 40 amu) in a "
        "1 MHz trap the Coulomb parameter κ = q²/(4πε₀)/(mω₀²ℓ³) sets the physical length scale."
    ),
    "nondim_ru": (
        "Время в единицах 1/ω₀, длины в единицах ℓ = (κ/mω₀²)^(1/3), энергии в единицах "
        "mω₀²ℓ² = κ/ℓ. Пресет задаёт ω₀ = κ = m = 1, поэтому сторона кристалла a = 3^(1/3) = "
        "1.4422495703, а его энергия U* = 1.5·3^(2/3) = 3.120125734578. Ловушка изотропна, "
        "поэтому ориентация кристалла свободна (нулевая мода); для иона Ca⁺ (m = 40 а.е.м.) в "
        "ловушке 1 МГц кулоновский параметр κ = q²/(4πε₀)/(mω₀²ℓ³) задаёт физический масштаб "
        "длины."
    ),
    "checks": {
        "header_en": ["Check", "Target", "Tolerance"],
        "header_ru": ["Проверка", "Цель", "Допуск"],
        "rows_en": [
            ["Global minimum reached: U_final − U_triangle", "0", "1e-9"],
            ["Binding energy released during cooling", "> 0", "exact"],
            ["Crystal side vs a = 3^(1/3)", "a", "1e-8"],
            ["Sides equal (equilateral)", "0", "1e-8"],
            ["Central angles 2π/3", "0", "1e-6"],
            ["Exactly one zero Hessian eigenvalue (rotation)", "1", "1e-6"],
            ["Exactly two COM modes at ω₀", "2", "5e-6"],
            ["Breathing mode at √3ω₀", "1", "5e-6"],
            ["Static equilibrium hold over t = 50", "0", "1e-9"],
            ["Conservative energy drift", "0", "1e-10"],
        ],
        "rows_ru": [
            ["Достигнут глобальный минимум: U_финал − U_треугольника", "0", "1e-9"],
            ["Высвобожденная при охлаждении энергия связи", "> 0", "точно"],
            ["Сторона кристалла против a = 3^(1/3)", "a", "1e-8"],
            ["Равенство сторон (равносторонность)", "0", "1e-8"],
            ["Центральные углы 2π/3", "0", "1e-6"],
            ["Ровно одно нулевое собственное значение гессиана (вращение)", "1", "1e-6"],
            ["Ровно две моды центра масс на ω₀", "2", "5e-6"],
            ["Дыхательная мода на √3ω₀", "1", "5e-6"],
            ["Статическое удержание равновесия на t = 50", "0", "1e-9"],
            ["Дрейф консервативной энергии", "0", "1e-10"],
        ],
    },
    "figure_caps": {
        "fig01_crystal_landscape.png": {
            "cap_en": "Model landscape of the three-ion crystal: (a) potential slice with ions 2 and 3 held at the equilibrium vertices and ion 1 scanned over the trap plane; (b) potential energy along the equilateral family U(a) = ω₀²a²/2 + 3κ/a.",
            "cap_ru": "Ландшафт модели трёхионного кристалла: (а) срез потенциала при зафиксированных во 2-й и 3-й вершинах равновесия ионах и сканируемом по плоскости ловушки ионе 1; (б) потенциальная энергия вдоль равностороннего семейства U(a) = ω₀²a²/2 + 3κ/a.",
            "walk_en": "The scanned-ion minimum lands exactly on the third vertex of the triangle, and the one-dimensional energy profile has its minimum at a* = 3^(1/3) = 1.442249570 with U* = 3.120125735 (trap energy units) — the force balance (E2) is the minimizer of the energy (E3).",
            "walk_ru": "Минимум при сканировании иона 1 попадает точно в третью вершину треугольника, а одномерный профиль энергии имеет минимум при a* = 3^(1/3) = 1.442249570 с U* = 3.120125735 (энергетические единицы ловушки) — баланс сил (E2) является минимизатором энергии (E3).",
        },
        "fig02_crystal_and_modes.png": {
            "cap_en": "Headline result: (a) the Newton-polished crystal with the exact force balance on each ion; (b) the six Hessian normal-mode frequencies against the analytic ladder.",
            "cap_ru": "Главный результат: (а) отполированный методом Ньютона кристалл с точным балансом сил на каждом ионе; (б) шесть собственных частот гессиана против аналитической лестницы.",
            "walk_en": "The polished triangle has side a = 1.442249570 with all three sides equal to 4.4e-16, and the measured finite-difference spectrum {0, 1.0, 1.0, 1.2247449, 1.2247449, 1.7320508} deviates from the analytic ladder {0, ω₀ (×2), √(3/2)ω₀ (×2), √3ω₀} by at most 1.4·10⁻⁸ against the 5e-6 tolerance.",
            "walk_ru": "Отполированный треугольник имеет сторону a = 1.442249570, все три стороны равны с точностью 4.4e-16, а измеренный конечно-разностный спектр {0, 1.0, 1.0, 1.2247449, 1.2247449, 1.7320508} отклоняется от аналитической лестницы {0, ω₀ (×2), √(3/2)ω₀ (×2), √3ω₀} не более чем на 1.4·10⁻⁸ при допуске 5e-6.",
        },
        "fig03_scaling_sweeps.png": {
            "cap_en": "Parameter sweeps: (a) crystal side versus Coulomb strength κ — relaxation + Newton re-runs against the analytic cubic law; (b) crystallization settle time versus Doppler drag γ_d.",
            "cap_ru": "Развертки параметров: (а) сторона кристалла против кулоновской силы κ — прогоны релаксации с полировкой Ньютона против аналитического кубического закона; (б) время кристаллизации против доплеровского трения γ_d.",
            "walk_en": "Independent re-runs reproduce a(κ) = (3κ/ω₀²)^(1/3) exactly at all five κ ∈ {0.25, 0.5, 1, 2, 4} — a from 0.908560296 to 2.289428485 — while the settle time decreases monotonically from 24.341 to 5.609 (1/ω₀ units) over γ_d ∈ [0.4, 2.4], with no overdamped upturn inside the scanned window.",
            "walk_ru": "Независимые прогоны воспроизводят a(κ) = (3κ/ω₀²)^(1/3) точно во всех пяти точках κ ∈ {0.25, 0.5, 1, 2, 4} — a от 0.908560296 до 2.289428485, — а время кристаллизации монотонно убывает от 24.341 до 5.609 (единицы 1/ω₀) по γ_d ∈ [0.4, 2.4] без передемпфированного подъёма внутри сканируемого окна.",
        },
        "fig04_crystallization_dynamics.png": {
            "cap_en": "Crystallization dynamics: (a) worldlines of the three ions from the seeded random start into the crystal (γ_d = 0.8, T = 60); (b) cooling decay |U(t) − U_min| versus the conservative hold |E(t) − E(0)|.",
            "cap_ru": "Динамика кристаллизации: (а) мировые линии трёх ионов от засеянного случайного старта до кристалла (γ_d = 0.8, T = 60); (б) спад при охлаждении |U(t) − U_min| против консервативного удержания |E(t) − E(0)|.",
            "walk_en": "Cooling at γ_d = 0.8 releases the binding energy ΔU = 1.7609 and settles the triangle within the T = 60 window, while the conservative run started at the exact equilibrium keeps the energy drift at 8.9e-16 over t = 50 — the crystal is a frozen choreography.",
            "walk_ru": "Охлаждение при γ_d = 0.8 высвобождает энергию связи ΔU = 1.7609 и успокаивает треугольник внутри окна T = 60, а консервативный прогон из точного равновесия держит дрейф энергии на уровне 8.9e-16 на протяжении t = 50 — кристалл является замороженной хореографией.",
        },
    },
    "results_block": [
        "global_minimum_reached           = 0.0        (U_final = U_triangle = 3.120125734578)",
        "crystallization_energy_released  = PASS       (binding energy 1.7609 released)",
        "crystal_side_equals_analytic     = 1.442249570 (a = 3^(1/3) = 1.4422495703)",
        "crystal_equilateral              = 4.4e-16    (max side - min side)",
        "crystal_angles_120deg            = 4.4e-16    (2*pi/3 = 2.0943951 rad each)",
        "zero_rotation_mode               = PASS",
        "two_com_modes_at_omega0          = PASS",
        "breathing_mode_sqrt3             = PASS (omega_b = 1.7320508 = sqrt(3))",
        "static_equilibrium_holds         = 3.9e-15    (positions after t = 50)",
        "conservative_energy_conserved    = 8.9e-16    (damping-free crystal, t = 50)",
        "status: PASS (10/10)",
    ],
    "abstract_en": (
        "This monograph treats three laser-cooled ions in the transverse plane of a linear "
        "Paul trap as a table-top three-body problem: a two-dimensional harmonic rf pseudopotential "
        "confines the ions, their mutual Coulomb repulsion pushes them apart, and Doppler cooling — "
        "modelled as a linear drag −γ_d·v — dissipates energy until the ions crystallize. The study "
        "establishes, end to end and to machine precision, that the attractor of the cooled dynamics "
        "is the equilateral Lagrange triangle of side a = (3κ/ω₀²)^(1/3) = 3^(1/3) = 1.4422495703: a "
        "seeded relaxation with a documented wavepacket softening ε = 0.05, Newton-polished on the "
        "strict force balance, reproduces the analytic crystal energy U* = 3.120125734578 exactly, "
        "with all three sides equal to 4.4e-16 and central angles 2π/3 to 4.4e-16. The "
        "finite-difference Hessian confirms the full normal-mode ladder {0, ω₀ (×2), √(3/2)ω₀ (×2), "
        "√3ω₀} — one rigid-rotation zero mode, two centre-of-mass modes, one breathing mode — to "
        "1.4·10⁻⁸ against the 5e-6 tolerance. Started exactly at equilibrium, the conservative "
        "dynamics holds the crystal statically to 3.9e-15 over fifty time units with energy drift "
        "8.9e-16: the ion crystal is a frozen choreography, the trapped-ion twin of the Lagrange "
        "relative equilibrium."
    ),
    "abstract_ru": (
        "Монография рассматривает три лазерно-охлаждённых иона в поперечной плоскости "
        "линейной ловушки Пауля как настольную задачу трёх тел: двумерный гармонический "
        "радиочастотный псевдопотенциал удерживает ионы, кулоновское отталкивание расталкивает их, "
        "а доплеровское охлаждение — в модели линейного трения −γ_d·v — рассеивает энергию, пока "
        "ионы не кристаллизуются. Исследование устанавливает сквозным образом и с машинной "
        "точностью, что аттрактором охлаждаемой динамики служит равносторонний треугольник "
        "Лагранжа со стороной a = (3κ/ω₀²)^(1/3) = 3^(1/3) = 1.4422495703: засеянная релаксация с "
        "документированным смягчением волнового пакета ε = 0.05, отполированная методом Ньютона на "
        "строгом балансе сил, в точности воспроизводит аналитическую энергию кристалла "
        "U* = 3.120125734578, все три стороны равны с точностью 4.4e-16, центральные углы 2π/3 — с "
        "точностью 4.4e-16. Конечно-разностный гессиан подтверждает полную лестницу нормальных "
        "мод {0, ω₀ (×2), √(3/2)ω₀ (×2), √3ω₀} — одну нулевую моду жёсткого вращения, две моды "
        "центра масс, одну дыхательную — на уровне 1.4·10⁻⁸ при допуске 5e-6. Запущенная точно в "
        "равновесии консервативная динамика держит кристалл статичным на уровне 3.9e-15 на "
        "протяжении пятидесяти единиц времени с дрейфом энергии 8.9e-16: ионный кристалл — "
        "замороженная хореография, ионно-ловушечный близнец лагранжева относительного равновесия."
    ),
    "intro_en": [
        (
            "The quadrupole ion trap was invented by Wolfgang Paul and Helmut Steinwedel in 1953 as "
            "a mass spectrometer without a magnetic field; the radiofrequency pseudopotential they "
            "introduced lets charged particles float in a nearly harmonic well far from any "
            "material surface. Half a century of refinement — recognized by the 1989 Nobel Prize "
            "shared by Paul and Hans Dehmelt — turned the trap into the workhorse of atomic "
            "spectroscopy, frequency standards and, later, quantum information. Paul's 1990 Nobel "
            "lecture in the Reviews of Modern Physics remains the canonical introduction to the "
            "pseudopotential picture used throughout this study."
        ),
        (
            "Laser cooling supplied the second ingredient. The 1975 proposals of Hänsch and Schawlow "
            "(free atoms) and of Wineland and Dehmelt (trapped ions) showed that red-detuned light "
            "slows an absorber toward the Doppler limit; Itano and Wineland (1982) worked out the "
            "full theory for ions in harmonic and Penning traps. Cooling removes kinetic energy "
            "order by order, and in a harmonic confinement the coldest state of a cloud is no cloud "
            "at all: the competition between the confining force and the mutual Coulomb repulsion "
            "has a crystalline ground state."
        ),
        (
            "That phase transition was observed in 1987: Diedrich and colleagues in Garching saw "
            "laser-cooled stored ions jump from a disordered cloud to an ordered crystal, and "
            "Dubin and O'Neil's 1999 review consolidated the whole field — trapped nonneutral "
            "plasmas, liquids and crystals — into a single statistical-mechanics framework with "
            "the Coulomb coupling parameter as the control variable. For a handful of ions the "
            "crystal geometry is dictated by elementary force balance: two ions line up, three "
            "form an equilateral triangle, larger ensembles arrange in rings and shells — the "
            "finite-N precursors of Wigner crystals."
        ),
        (
            "The small crystals then became quantum technology. Cirac and Zoller's 1995 proposal "
            "used the collective vibrational modes of a trapped-ion string as a data bus for "
            "quantum gates, and James (1998) computed the exact normal-mode spectrum of small "
            "ion crystals — precisely the object this study verifies classically. Three ions form "
            "the smallest ion-crystal quantum simulator (Blatt and Roos 2012), and their mode "
            "ladder — zero, centre-of-mass, breathing — is the table-top counterpart of the "
            "TRIVORTEX triad: the equilateral configuration of Theorem 3.1, realized in an "
            "afternoon experiment with a linear Paul trap and a pair of cooling lasers."
        ),
    ],
    "intro_ru": [
        (
            "Квадрупольную ионную ловушку изобрели Вольфганг Пауль и Хельмут Штайнведель в 1953 году "
            "как масс-спектрометр без магнитного поля; введённый ими радиочастотный псевдопотенциал "
            "позволяет заряженным частицам парить в почти гармонической яме вдали от какой-либо "
            "материальной поверхности. Полвека доводки — отмеченное Нобелевской премией 1989 года, "
            "разделённой между Паулем и Гансом Демельтом, — превратили ловушку в рабочий инструмент "
            "атомной спектроскопии, стандартов частоты, а позднее и квантовой информации. "
            "Нобелевская лекция Пауля 1990 года в Reviews of Modern Physics остаётся каноническим "
            "введением в картину псевдопотенциала, используемую в этом исследовании."
        ),
        (
            "Вторым ингредиентом стало лазерное охлаждение. Предложения 1975 года Хенса и Шавлова "
            "(свободные атомы) и Винеленда и Демельта (захваченные ионы) показали, что "
            "красно-расстроенный свет замедляет поглотитель к доплеровскому пределу; Итано и "
            "Винеленд (1982) разработали полную теорию для ионов в гармонических ловушках и "
            "ловушках Пеннинга. Охлаждение убирает кинетическую энергию шаг за шагом, и в "
            "гармоническом удержании самое холодное состояние облака — вовсе не облако: "
            "конкуренция удерживающей силы и взаимного кулоновского отталкивания имеет "
            "кристаллическое основное состояние."
        ),
        (
            "Этот фазовый переход наблюдали в 1987 году: Дидерих и коллеги в Гархинге наблюдали, как "
            "как лазерно-охлаждённые захваченные ионы перескакивают из неупорядоченного облака в "
            "упорядоченный кристалл, а обзор Дубина и О’Нила 1999 года свёл всю область — "
            "захваченные ненейтральные плазмы, жидкости и кристаллы — к единой "
            "статистико-механической рамке с кулоновским параметром связи в качестве управляющей "
            "переменной. Для горстки ионов геометрию кристалла диктует элементарный баланс сил: "
            "два иона выстраиваются в линию, три образуют равносторонний треугольник, более "
            "крупные ансамбли — кольца и оболочки, конечные предшественники кристаллов Вигнера."
        ),
        (
            "Затем малые кристаллы стали квантовой технологией. Предложение Цирака и Цоллера 1995 "
            "года использовало коллективные вибрационные моды цепочки ионов как шину данных для "
            "квантовых вентилей, а Джеймс (1998) вычислил точный спектр нормальных мод малых "
            "ионных кристаллов — ровно тот объект, который данное исследование проверяет "
            "классически. Три иона образуют наименьший ионно-кристаллический квантовый симулятор "
            "(Блатт и Рос 2012), а их лестница мод — нулевая, центра масс, дыхательная — является "
            "настольным двойником триады TRIVORTEX: равносторонней конфигурации теоремы 3.1, "
            "воплощённой в эксперименте одного дня с линейной ловушкой Пауля и парой "
            "охлаждающих лазеров."
        ),
    ],
    "derivation_en": [
        (
            "The dynamics (E1) contains two length scales — the trap length (κ/mω₀²)^(1/3) fixed by "
            "the competition of harmonic confinement and Coulomb repulsion, and the softening ε — "
            "and no other parameter. The equilateral configuration is the central configuration of "
            "the problem: by the three-fold symmetry the net Coulomb push on each ion is radial, of "
            "magnitude √3κ/a², while the trap pulls inward with ω₀²a/√3. Equating the two gives the "
            "algebraic force balance (E2), a³ = 3κ/ω₀², whose preset root is a = 3^(1/3) = "
            "1.4422495703 in trap length units."
        ),
        (
            "The same side follows from energy minimization. Along the equilateral family the "
            "potential is U(a) = ω₀²a²/2 + 3κ/a (three trap terms plus three pair terms), and "
            "dU/da = ω₀²a − 3κ/a² vanishes exactly at the force-balance side; the minimum value is "
            "U* = 1.5·3^(2/3) = 3.120125734578 (E3). During cooling the drag dissipates this "
            "potential downhill, so the released binding energy ΔU = U(random start) − U* = 1.7609 "
            "measures how far above the crystal the run began. The documented softening ε_relax = "
            "0.05 — a stand-in for the finite size of the cooled ion wavepacket — regularizes the "
            "Coulomb singularity during the relaxation stage; the acceptance numbers are then "
            "Newton-polished on the strict ε = 1e-12 balance, so they refer to the ideal model."
        ),
        (
            "Small oscillations follow from the 6×6 position Hessian H of U at the equilibrium; its "
            "eigenvalues divided by the mass are the squared mode frequencies (E4). Translation "
            "symmetry makes the centre-of-mass pair exact: ω = ω₀ twice. Rotational symmetry of the "
            "isotropic trap makes the orientation free: one zero mode — the rigid-rotation "
            "nullspace, the analogue of the continuous choreography family. The remaining pair "
            "splits into two quadrupole deformations at √(3/2)ω₀ and the breathing mode at "
            "√3ω₀ = 1.7320508, where the triangle breathes in and out. Finally, because the trap is "
            "static in the lab frame, the equilibrium is an exact solution of the conservative "
            "dynamics (E5): started at the crystal with zero velocities and γ_d = 0, the ions stay "
            "there — the static hold verified to 3.9e-15 over t = 50."
        ),
    ],
    "derivation_ru": [
        (
            "Динамика (E1) содержит две шкалы длины — длину ловушки (κ/mω₀²)^(1/3), задаваемую "
            "конкуренцией гармонического удержания и кулоновского отталкивания, и смягчение ε — и "
            "никаких других параметров. Равносторонняя конфигурация — центральная конфигурация "
            "задачи: в силу тройной симметрии суммарный кулоновский толчок на каждый ион радиален "
            "и равен √3κ/a², тогда как ловушка тянет внутрь с силой ω₀²a/√3. Приравнивая их, "
            "получаем алгебраический баланс сил (E2), a³ = 3κ/ω₀², корень которого для пресета — "
            "a = 3^(1/3) = 1.4422495703 в единицах длины ловушки."
        ),
        (
            "Та же сторона следует из минимизации энергии. Вдоль равностороннего семейства "
            "потенциал равен U(a) = ω₀²a²/2 + 3κ/a (три ловушечных слагаемых плюс три парных), и "
            "dU/da = ω₀²a − 3κ/a² обращается в нуль ровно при стороне из баланса сил; минимальное "
            "значение U* = 1.5·3^(2/3) = 3.120125734578 (E3). При охлаждении трение рассеивает "
            "энергию, скатывая систему под гору по этому потенциалу, так что высвобожденная "
            "энергия связи ΔU = U(случайный "
            "старт) − U* = 1.7609 показывает, насколько выше кристалла начался прогон. "
            "Документированное смягчение ε_relax = 0.05 — заместитель конечного размера "
            "охлаждённого волнового пакета иона — регуляризует кулоновскую сингулярность на стадии "
            "релаксации; контрольные числа затем полируются методом Ньютона на строгом балансе "
            "при ε = 1e-12, так что они относятся к идеальной модели."
        ),
        (
            "Малые колебания описываются позиционным гессианом H размера 6×6 потенциала U в "
            "равновесии; его собственные значения, делённые на массу, — квадраты частот мод (E4). "
            "Трансляционная симметрия делает пару центра масс точной: дважды ω = ω₀. Вращательная "
            "симметрия изотропной ловушки делает ориентацию свободной: одна нулевая мода — "
            "нуль-мода — ядро гессиана, отвечающее свободному жёсткому вращению, — аналог непрерывного семейства хореографий. "
            "Оставшаяся пара распадается на две квадрупольные деформации на √(3/2)ω₀ и "
            "дыхательную моду на √3ω₀ = 1.7320508, при которой треугольник дышит. Наконец, "
            "поскольку ловушка статична в лабораторной системе, равновесие — точное решение "
            "консервативной динамики (E5): стартовав в кристалле с нулевыми скоростями и γ_d = 0, "
            "ионы остаются на месте — статическое удержание, проверенное на уровне 3.9e-15 на "
            "t = 50."
        ),
    ],
    "connection_en": (
        "The three-ion crystal is the table-top member of the same central-configuration "
        "family that anchors TRIVORTEX. The equilateral triangle is literally the Lagrange solution: "
        "one algebraic force balance fixes its size, just as the balance of vortex attractions and "
        "Abel–Hertz flux fixes the size of the same-sign vortex triangle of Theorem 3.1 — in both "
        "problems two competing scales leave a single dimensionless combination that sets the "
        "geometry. The mode correspondence is equally direct: the breathing mode √3ω₀ is the radial "
        "modulation of the Theorem 3.1 triangle, the two centre-of-mass modes reflect the shared "
        "translational symmetry, and the zero rigid-rotation mode — the free orientation of the "
        "crystal in the isotropic trap — is the continuous family of relative equilibria, the same "
        "degeneracy that makes the vortex triangle a rotating choreography rather than a static "
        "figure. What the ion trap adds is dissipation as a selection mechanism: cooling drives the "
        "configuration downhill to the central configuration and freezes it there, which is exactly "
        "how the monograph's rotating triads are realized in laboratory matter."
    ),
    "connection_ru": (
        "Трёхионный кристалл — настольный член того же семейства центральных конфигураций, "
        "на котором стоит TRIVORTEX. Равносторонний треугольник — буквально лагранжево решение: один "
        "алгебраический баланс сил фиксирует его размер, точно так же, как баланс вихревых "
        "притяжений и потока Абеля–Хертца фиксирует размер одноимённого вихревого треугольника "
        "теоремы 3.1, — в обеих задачах две конкурирующие шкалы оставляют одну безразмерную "
        "комбинацию, задающую геометрию. Соответствие мод столь же прямое: дыхательная мода √3ω₀ — "
        "радиальная модуляция треугольника теоремы 3.1, две моды центра масс отражают общую "
        "трансляционную симметрию, а нулевая мода жёсткого вращения — свободная ориентация "
        "кристалла в изотропной ловушке — это непрерывное семейство относительных равновесий, та же "
        "вырожденность, которая делает вихревой треугольник вращающейся хореографией, а не статичной "
        "фигурой. Ловушка ионов добавляет диссипацию как механизм отбора: охлаждение гонит "
        "конфигурацию под гору к центральной конфигурации и замораживает её там — ровно так "
        "вращающиеся триады монографии воплощаются в лабораторном веществе."
    ),
    "method_en": [
        (
            "Crystallization stage: the three ions start from a seeded random configuration in "
            "[−1, 1]² with zero velocities (rng seed 3) and relax under the damped inertial dynamics "
            "(E1) with γ_d = 0.8 and the documented softening ε_relax = 0.05, integrated with the "
            "explicit Dormand–Prince 8(5,3) scheme at rtol = atol = 1e-11, max_step 0.05, over "
            "T_relax = 60. The end state is the softened equilibrium — the stand-in for the finite "
            "cooled wavepacket."
        ),
        (
            "Polish and spectrum stage: the relaxed configuration seeds a Newton root-find (scipy "
            "hybr, tol 1e-14) of the strict force balance at ε = 1e-12, with the analytic triangle "
            "as a documented fallback; the polished crystal is compared against a = 3^(1/3) "
            "(sides, equality, 2π/3 angles) and against the analytic energy U* = 3.120125734578. "
            "Normal modes come from a finite-difference Hessian (central fourth-order stencil, "
            "h = 1e-4) diagonalized with eigvalsh; the zero, COM and breathing mode counts are "
            "accepted in 5e-6 frequency windows."
        ),
        (
            "Invariant and sweeps stage: the static hold integrates the conservative dynamics (γ_d = 0) "
            "from the analytic equilibrium with rtol = atol = 1e-12 over t = 50, recording the "
            "position drift and the total-energy drift. Two sweeps close the protocol: five Coulomb "
            "strengths κ ∈ {0.25, 0.5, 1, 2, 4} are re-relaxed and re-polished against the cubic law "
            "a(κ) = (3κ/ω₀²)^(1/3), and six Doppler drags γ_d ∈ {0.4, 0.6, 0.8, 1.2, 1.6, 2.4} are "
            "scored by the settle time — the first moment the side spread stays below 0.01 within the "
            "600-sample window. Every check stores value, target, tolerance, unit and pass flag in "
            "the JSON protocol; the run is deterministic, offline and bit-reproducible."
        ),
    ],
    "method_ru": [
        (
            "Стадия кристаллизации: три иона стартуют из засеянной случайной конфигурации в "
            "[−1, 1]² с нулевыми скоростями (зерно генератора 3) и релаксируют в рамках "
            "демпфированной инерциальной динамики (E1) с γ_d = 0.8 и документированным смягчением "
            "ε_relax = 0.05, интегрируемой явной схемой Дормана–Принса 8(5,3) при rtol = atol = "
            "1e-11, max_step 0.05, на T_relax = 60. Конечное состояние — смягчённое равновесие, "
            "заместитель конечного охлаждённого волнового пакета."
        ),
        (
            "Стадия полировки и спектра: релаксированная конфигурация засевает поиск корня Ньютона "
            "(scipy hybr, tol 1e-14) строгого баланса сил при ε = 1e-12 с аналитическим "
            "треугольником в качестве документированного резервного старта; отполированный "
            "кристалл сверяется с a = 3^(1/3) (стороны, равенство, углы 2π/3) и с аналитической "
            "энергией U* = 3.120125734578. Нормальные моды берутся из конечно-разностного гессиана "
            "(центральный шаблон четвёртого порядка, h = 1e-4), диагонализуемого eigvalsh; счётчики "
            "нулевой моды, мод центра масс и дыхательной принимаются в частотных окнах 5e-6."
        ),
        (
            "Стадия инварианта и разверток: статическое удержание интегрирует консервативную "
            "динамику (γ_d = 0) из аналитического равновесия при rtol = atol = 1e-12 на t = 50, "
            "записывая дрейф положений и дрейф полной энергии. Протокол замыкают две развертки: "
            "пять кулоновских сил κ ∈ {0.25, 0.5, 1, 2, 4} заново релаксируются и полируются "
            "против кубического закона a(κ) = (3κ/ω₀²)^(1/3), а шесть доплеровских трений "
            "γ_d ∈ {0.4, 0.6, 0.8, 1.2, 1.6, 2.4} оцениваются временем успокоения — первым "
            "моментом, когда разброс сторон остаётся ниже 0.01 внутри окна из 600 выборок. Каждая "
            "проверка хранит значение, цель, допуск, единицу и флаг прохождения в JSON-протоколе; "
            "прогон детерминирован, автономен и бит-в-бит воспроизводим."
        ),
    ],
    "analysis_en": [
        (
            "**Crystallization and global minimum.** From the seeded random start the damped "
            "relaxation releases the binding energy ΔU = 1.7609 and descends into the crystal well; "
            "after the Newton polish on the strict balance the potential equals the analytic "
            "triangle energy exactly — the recorded U_final − U_triangle is 0.0 against the 1e-9 "
            "tolerance, with U* = 3.120125734578. The two-stage design is what makes the check "
            "honest: the softened relaxation provides a robust landscape, and the strict polish "
            "ties the reported numbers to the ideal force balance (E2) rather than to the softening."
        ),
        (
            "**Geometry of the crystal.** The polished triangle has mean side 1.4422495703074085 "
            "against the analytic 3^(1/3) = 1.4422495703074083 (agreement far inside the 1e-8 "
            "tolerance); the three sides are equal to 4.4e-16 and the three central angles equal "
            "2π/3 = 2.0943951 rad each to 4.4e-16. The crystal recorded in the protocol sits on the "
            "canonical orientation with circumradius 0.8326832 = a/√3, but the orientation itself is "
            "a free zero mode of the isotropic trap."
        ),
        (
            "**Mode ladder and invariants.** The finite-difference Hessian (h = 1e-4) returns "
            "frequencies {0.0, 0.999999997, 1.000000014, 1.224744867, 1.224744882, 1.732050810}: "
            "exactly one zero mode, two COM modes at ω₀ and one breathing mode at √3ω₀ = 1.7320508, "
            "with the maximum deviation from the analytic ladder of 1.4·10⁻⁸ against the 5e-6 "
            "tolerance. The conservative hold started exactly at the equilibrium keeps the positions "
            "fixed to 3.9e-15 over t = 50 and the total energy to 8.9e-16 — both round-off level, "
            "confirming that the crystal is a static exact solution of the damping-free dynamics."
        ),
        (
            "**Scaling and drag response.** Five independent re-runs reproduce the cubic law "
            "a(κ) = (3κ/ω₀²)^(1/3) with no free fitting: the numeric sides 0.908560296, 1.144714243, "
            "1.442249570, 1.817120593, 2.289428485 coincide with the analytic values at all five "
            "κ ∈ {0.25, 0.5, 1, 2, 4}. The drag sweep shows the settle time falling monotonically "
            "from 24.341 to 5.609 (1/ω₀ units) as γ_d grows over [0.4, 2.4] — the underdamped "
            "transient penalty dominates the scanned window and the overdamped upturn lies beyond "
            "γ_d = 2.4, so the preset γ_d = 0.8 sits in the transient-dominated regime with settle "
            "time 11.720."
        ),
    ],
    "analysis_ru": [
        (
            "**Кристаллизация и глобальный минимум.** Из засеянного случайного старта "
            "демпфированная релаксация высвобождает энергию связи ΔU = 1.7609 и спускается в "
            "кристаллическую яму; после полировки Ньютона на строгом балансе потенциал в точности "
            "равен аналитической энергии треугольника — записанное U_финал − U_треугольника равно "
            "0.0 при допуске 1e-9, с U* = 3.120125734578. Двухстадийная схема делает проверку "
            "честной: смягчённая релаксация даёт устойчивый ландшафт, а строгая полировка привязывает "
            "отчётные числа к идеальному балансу сил (E2), а не к смягчению."
        ),
        (
            "**Геометрия кристалла.** Отполированный треугольник имеет среднюю сторону "
            "1.4422495703074085 против аналитической 3^(1/3) = 1.4422495703074083 (согласие много "
            "внутри допуска 1e-8); три стороны равны с точностью 4.4e-16, три центральных угла "
            "равны 2π/3 = 2.0943951 рад с точностью 4.4e-16. Кристалл, записанный в протоколе, "
            "стоит в канонической ориентации с радиусом описанной окружности 0.8326832 = a/√3, но "
            "сама ориентация — свободная нулевая мода изотропной ловушки."
        ),
        (
            "**Лестница мод и инварианты.** Конечно-разностный гессиан (h = 1e-4) возвращает "
            "частоты {0.0, 0.999999997, 1.000000014, 1.224744867, 1.224744882, 1.732050810}: ровно "
            "одна нулевая мода, две моды центра масс на ω₀ и одна дыхательная на √3ω₀ = 1.7320508, "
            "с максимальным отклонением от аналитической лестницы 1.4·10⁻⁸ при допуске 5e-6. "
            "Консервативное удержание, стартовавшее точно в равновесии, держит положения с "
            "точностью 3.9e-15 на t = 50, а полную энергию — 8.9e-16; оба уровня — округление, что "
            "подтверждает: кристалл — статическое точное решение динамики без трения."
        ),
        (
            "**Масштабирование и отклик на трение.** Пять независимых прогонов воспроизводят "
            "кубический закон a(κ) = (3κ/ω₀²)^(1/3) без подгоночных параметров: численные стороны "
            "0.908560296, 1.144714243, 1.442249570, 1.817120593, 2.289428485 совпадают с "
            "аналитическими во всех пяти точках κ ∈ {0.25, 0.5, 1, 2, 4}. Развертка по трению "
            "показывает монотонное падение времени успокоения от 24.341 до 5.609 (единицы 1/ω₀) с "
            "ростом γ_d по [0.4, 2.4] — штраф недодемпфированного переходного режима доминирует в "
            "сканируемом окне, а передемпфированный подъём лежит за γ_d = 2.4, поэтому пресет "
            "γ_d = 0.8 сидит в переходном режиме со временем успокоения 11.720."
        ),
    ],
    "discussion_en": [
        (
            "The model is deliberately minimal: two-dimensional, harmonic pseudopotential, identical "
            "ions, and cooling reduced to a linear drag. Within these assumptions every reported "
            "number is an exact statement about the governing equations rather than a simulation of "
            "a specific apparatus. The natural extensions each preserve the verification style: "
            "photon-recoil heating added to the drag (a Fokker–Planck rather than deterministic "
            "cooling model), axial degrees of freedom and the full 3-D crystal, anharmonic and "
            "segmented trap geometries, and the micromotion corrections beyond the pseudopotential "
            "approximation — valid whenever the rf drive frequency greatly exceeds ω₀."
        ),
        (
            "The parameter regime couples to real hardware through one scale. The dimensionless "
            "preset (ω₀ = κ = m = 1) maps to a Ca⁺ ion (m = 40 amu) in a 1 MHz trap through "
            "κ = q²/(4πε₀)/(mω₀²ℓ³), which sets the trap length scale ℓ and with it the crystal "
            "size a·ℓ; the drag γ_d = 0.8 encodes the Doppler cooling rate in units of ω₀. The "
            "softening ε_relax = 0.05 is the one effective parameter of the relaxation stage, and "
            "its role is documented and then removed: all acceptance checks are evaluated on the "
            "strict unsoftened balance, so the reported machine-precision agreement is not an "
            "artifact of the regularization."
        ),
        (
            "Within the program this study is the matter-wave anchor of the Lagrange block. It "
            "shares the harmonic-balance logic with TRX-01, where the same equilateral configuration "
            "appears as the celestial libration points under a laser-renormalized gravity; it is "
            "the optical twin of TRX-03, where three solitons play the same central configuration "
            "with the same breathing-mode logic; and it hands the exact three-ion geometry and mode "
            "ladder to TRX-07, where quantum correlations are layered onto the same three-body "
            "skeleton. Together the three studies show the Lagrange triad operating across optics, "
            "celestial mechanics and laboratory quantum matter."
        ),
    ],
    "discussion_ru": [
        (
            "Модель сознательно минимальна: два измерения, гармонический псевдопотенциал, "
            "одинаковые ионы, охлаждение сведено к линейному трению. В этих допущениях каждое "
            "отчётное число — точное утверждение об определяющих уравнениях, а не симуляция "
            "конкретной установки. Естественные расширения сохраняют верификационный стиль: "
            "добавленный к трению нагрев фотонной отдачей (фоккеровско-планковская, а не "
            "детерминированная модель охлаждения), аксиальные степени свободы и полный 3-D "
            "кристалл, ангармоничные и сегментированные геометрии ловушек и поправки на "
            "микродвижение за пределами приближения псевдопотенциала — корректные всякий раз, "
            "когда частота радиочастотного драйва много больше ω₀."
        ),
        (
            "Параметрический режим связывается с реальным оборудованием через одну шкалу. "
            "Безразмерный пресет (ω₀ = κ = m = 1) отображается на ион Ca⁺ (m = 40 а.е.м.) в "
            "ловушке 1 МГц через κ = q²/(4πε₀)/(mω₀²ℓ³), задающее масштаб длины ловушки ℓ и вместе "
            "с ним размер кристалла a·ℓ; трение γ_d = 0.8 кодирует скорость доплеровского "
            "охлаждения в единицах ω₀. Смягчение ε_relax = 0.05 — единственный эффективный "
            "параметр стадии релаксации, его роль документирована и затем устранена: все "
            "контрольные проверки вычисляются на строгом несмягчённом балансе, поэтому "
            "машинно-точное согласие не является артефактом регуляризации."
        ),
        (
            "В рамках программы это исследование — материально-волновой якорь лагранжева блока. "
            "Оно разделяет логику гармонического баланса с TRX-01, где та же равносторонняя "
            "конфигурация выступает небесными точками либрации при лазерно-перенормированной "
            "гравитации; оно — оптический близнец TRX-03, где три солитона играют ту же "
            "центральную конфигурацию с той же логикой дыхательной моды; и оно передаёт точную "
            "геометрию трёх ионов и лестницу мод исследованию TRX-07, где квантовые корреляции "
            "надстраиваются над тем же трёхтелесным скелетом. Вместе три исследования показывают "
            "лагранжеву триаду, работающую в оптике, небесной механике и лабораторной квантовой "
            "материи."
        ),
    ],
    "conclusions_en": [
        "Damped Doppler cooling crystallizes three ions into the equilateral Lagrange triangle; the two-stage protocol (softened relaxation, Newton polish on the strict balance) reaches the analytic crystal energy U* = 3.120125734578 with the recorded difference exactly 0.0 (tolerance 1e-9).",
        "The crystal geometry is machine-exact: side a = 3^(1/3) = 1.4422495703, sides equal to 4.4e-16, central angles 2π/3 = 2.0943951 rad each to 4.4e-16.",
        "The normal-mode ladder is confirmed by the finite-difference Hessian: exactly one zero mode (rigid rotation), two COM modes at ω₀, one breathing mode at √3ω₀ = 1.7320508; maximum deviation from the analytic ladder 1.4·10⁻⁸ against the 5e-6 tolerance.",
        "Started exactly at equilibrium, the conservative dynamics holds the crystal statically to 3.9e-15 over t = 50 with total-energy drift 8.9e-16 — the ion crystal is a frozen choreography.",
        "The scaling law a(κ) = (3κ/ω₀²)^(1/3) is reproduced without free parameters by independent relaxation + Newton re-runs at all five κ ∈ {0.25, 0.5, 1, 2, 4} (a from 0.908560296 to 2.289428485).",
        "The crystallization (settle) time decreases monotonically from 24.341 to 5.609 (1/ω₀ units) over the Doppler-drag window γ_d ∈ [0.4, 2.4]; the underdamped transient penalty dominates and the preset γ_d = 0.8 settles in 11.720.",
    ],
    "conclusions_ru": [
        "Демпфированное доплеровское охлаждение кристаллизует три иона в равносторонний треугольник Лагранжа; двухстадийный протокол (смягчённая релаксация, полировка Ньютона на строгом балансе) достигает аналитической энергии кристалла U* = 3.120125734578 с записанной разностью ровно 0.0 (допуск 1e-9).",
        "Геометрия кристалла машинно-точна: сторона a = 3^(1/3) = 1.4422495703, стороны равны с точностью 4.4e-16, центральные углы 2π/3 = 2.0943951 рад каждый с точностью 4.4e-16.",
        "Лестница нормальных мод подтверждена конечно-разностным гессианом: ровно одна нулевая мода (жёсткое вращение), две моды центра масс на ω₀, одна дыхательная на √3ω₀ = 1.7320508; максимальное отклонение от аналитической лестницы 1.4·10⁻⁸ при допуске 5e-6.",
        "Запущенная точно в равновесии консервативная динамика держит кристалл статичным с точностью 3.9e-15 на t = 50 с дрейфом полной энергии 8.9e-16 — ионный кристалл является замороженной хореографией.",
        "Закон масштабирования a(κ) = (3κ/ω₀²)^(1/3) воспроизводится без подгоночных параметров независимыми прогонами релаксации с полировкой Ньютона во всех пяти точках κ ∈ {0.25, 0.5, 1, 2, 4} (a от 0.908560296 до 2.289428485).",
        "Время кристаллизации (успокоения) монотонно убывает от 24.341 до 5.609 (единицы 1/ω₀) в окне доплеровского трения γ_d ∈ [0.4, 2.4]; штраф недодемпфированного переходного режима доминирует, а пресет γ_d = 0.8 успокаивается за 11.720.",
    ],
    "references": [
        "1. Paul, W., Steinwedel, H. (1953). *Ein neues Massenspektrometer ohne Magnetfeld.* Zeitschrift für Naturforschung A 8, 448–450.",
        "2. Paul, W. (1990). *Electromagnetic traps for charged and neutral particles.* Reviews of Modern Physics 62, 531–540.",
        "3. Itano, W. M., Wineland, D. J. (1982). *Laser cooling of ions stored in harmonic and Penning traps.* Physical Review A 25, 35–54.",
        "4. Diedrich, F., Peik, E., Chen, J. M., Quint, W., Walther, H. (1987). *Observation of a phase transition of stored laser-cooled ions.* Physical Review Letters 59, 2931–2934.",
        "5. Cirac, J. I., Zoller, P. (1995). *Quantum computations with cold trapped ions.* Physical Review Letters 74, 4091–4094.",
        "6. James, D. F. V. (1998). *Quantum dynamics of cold trapped ions with application to quantum computation.* Applied Physics B 66, 181–190.",
        "7. Dubin, D. H. E., O'Neil, T. M. (1999). *Trapped nonneutral plasmas, liquids, and crystals.* Reviews of Modern Physics 71, 87–172.",
        "8. Blatt, R., Roos, C. F. (2012). *Quantum simulations with trapped ions.* Nature Physics 8, 277–284.",
    ],
    "crosslinks_en": [
        "* **TRX-03** is the optical twin: three solitons in a mode-locked fibre play the same central configuration with the same breathing-mode logic.",
        "* **TRX-07** adds quantum correlations (Efimov physics) to the same three-body geometry this study fixes classically.",
        "* **TRX-01** uses the same harmonic-trap-like balance in the celestial setting of the libration points.",
    ],
    "crosslinks_ru": [
        "* **TRX-03** — оптический близнец: три солитона в модово-синхронизованном волокне играют ту же центральную конфигурацию с той же логикой дыхательной моды.",
        "* **TRX-07** добавляет квантовые корреляции (физика Эфимова) к той же геометрии трёх тел, которую это исследование фиксирует классически.",
        "* **TRX-01** использует тот же баланс гармонического удержания в небесной постановке точек либрации.",
    ],
    "assumptions_en": [
        "Two-dimensional dynamics in the transverse plane; axial motion and rf micromotion are not modeled (pseudopotential approximation, valid when the drive frequency greatly exceeds ω₀).",
        "Doppler cooling is reduced to a linear drag −γ_d·v; photon recoil heating and saturation physics are omitted.",
        "The relaxation uses a documented softening ε_relax = 0.05 (finite cooled wavepacket); all acceptance numbers are Newton-polished on the strict ε = 1e-12 force balance.",
        "Three identical ions; no species mix, stray charges or trap anisotropy in the plane (orientation is a free zero mode).",
        "The crystal is a static equilibrium of the lab-frame dynamics, so the conservative hold with γ_d = 0 is an exact invariant test.",
        "A single seeded run (rng seed 3) per stage; the protocol is deterministic, offline and bit-reproducible.",
    ],
    "assumptions_ru": [
        "Двумерная динамика в поперечной плоскости; аксиальное движение и радиочастотное микродвижение не моделируются (приближение псевдопотенциала, корректное при частоте драйва, много большей ω₀).",
        "Доплеровское охлаждение сведено к линейному трению −γ_d·v; нагрев фотонной отдачей и физика насыщения опущены.",
        "Релаксация использует документированное смягчение ε_relax = 0.05 (конечный охлаждённый волновой пакет); все контрольные числа полируются методом Ньютона на строгом балансе сил при ε = 1e-12.",
        "Три одинаковых иона; без смеси сортов, паразитных зарядов и анизотропии ловушки в плоскости (ориентация — свободная нулевая мода).",
        "Кристалл — статическое равновесие динамики в лабораторной системе, поэтому консервативное удержание с γ_d = 0 есть точный инвариантный тест.",
        "Один засеянный прогон (зерно 3) на стадию; протокол детерминирован, автономен и бит-в-бит воспроизводим.",
    ],
    "glance_en": [
        ["Block", "Quantum three-body — study 08 of 12"],
        [
            "Model",
            "three ions in a 2-D harmonic rf pseudopotential + Coulomb repulsion (ω₀ = κ = m = 1)",
        ],
        [
            "Key structure",
            "equilateral Lagrange triangle, a = 3^(1/3) = 1.4422495703, U* = 3.120125734578",
        ],
        [
            "Headline result",
            "mode ladder {0, ω₀×2, √(3/2)ω₀×2, √3ω₀} confirmed to 1.4·10⁻⁸; static hold 3.9e-15 over t = 50",
        ],
        ["Verification", "10/10 checks PASS (full mode)"],
        ["Runtime", "6.79 s full · < 20 s smoke"],
    ],
    "glance_ru": [
        ["Блок", "Квантовые задачи трёх тел — исследование 08 из 12"],
        [
            "Модель",
            "три иона в двумерном гармоническом радиочастотном псевдопотенциале + кулоновское отталкивание (ω₀ = κ = m = 1)",
        ],
        [
            "Ключевая структура",
            "равносторонний треугольник Лагранжа, a = 3^(1/3) = 1.4422495703, U* = 3.120125734578",
        ],
        [
            "Главный результат",
            "лестница мод {0, ω₀×2, √(3/2)ω₀×2, √3ω₀} подтверждена на уровне 1.4·10⁻⁸; статическое удержание 3.9e-15 на t = 50",
        ],
        ["Верификация", "10/10 проверок PASS (полный режим)"],
        ["Время выполнения", "6.79 с полный · < 20 с smoke"],
    ],
    "glossary": {
        "header_en": ["Term", "Definition"],
        "header_ru": ["Термин", "Определение"],
        "rows_en": [
            [
                "Paul trap",
                "radiofrequency quadrupole trap confining charged particles in an oscillating inhomogeneous field",
            ],
            [
                "rf pseudopotential",
                "time-averaged effective potential of the rf drive; harmonic (mω₀²r²/2) in the trap plane",
            ],
            [
                "Doppler cooling",
                "laser cooling by red-detuned light; modelled here as a linear drag −γ_d·v",
            ],
            [
                "Ion crystal",
                "ordered configuration of trapped ions fixed by the balance of confinement and Coulomb repulsion",
            ],
            [
                "Lagrange triangle",
                "the equilateral central configuration of the three-body problem; here the three-ion crystal",
            ],
            [
                "Normal modes",
                "small-oscillation eigenmodes of the Hessian; here 0, ω₀ (×2), √(3/2)ω₀ (×2), √3ω₀",
            ],
            [
                "Breathing mode",
                "the √3ω₀ mode in which the triangle expands and contracts radially",
            ],
            [
                "Zero mode",
                "the Hessian nullspace direction — free rigid rotation (orientation) of the crystal in the isotropic trap",
            ],
            [
                "Softening ε",
                "regularization κ·r/(r² + ε²)^(3/2) of the Coulomb singularity; 0.05 in relaxation, 1e-12 in the polish",
            ],
            [
                "Settle time",
                "first moment the side spread of the relaxing triangle stays below 0.01",
            ],
        ],
        "rows_ru": [
            [
                "Ловушка Пауля",
                "радиочастотная квадрупольная ловушка, удерживающая заряженные частицы в осциллирующем неоднородном поле",
            ],
            [
                "Радиочастотный псевдопотенциал",
                "усреднённый по времени эффективный потенциал rf-драйва; в плоскости ловушки гармонический (mω₀²r²/2)",
            ],
            [
                "Доплеровское охлаждение",
                "лазерное охлаждение красно-расстроенным светом; здесь моделируется линейным трением −γ_d·v",
            ],
            [
                "Ионный кристалл",
                "упорядоченная конфигурация захваченных ионов, фиксируемая балансом удержания и кулоновского отталкивания",
            ],
            [
                "Треугольник Лагранжа",
                "равносторонняя центральная конфигурация задачи трёх тел; здесь — кристалл трёх ионов",
            ],
            [
                "Нормальные моды",
                "собственные малые колебания гессиана; здесь 0, ω₀ (×2), √(3/2)ω₀ (×2), √3ω₀",
            ],
            [
                "Дыхательная мода",
                "мода √3ω₀, при которой треугольник радиально расширяется и сжимается",
            ],
            [
                "Нулевая мода",
                "направление ядра гессиана — свободное жёсткое вращение (ориентация) кристалла в изотропной ловушке",
            ],
            [
                "Смягчение ε",
                "регуляризация κ·r/(r² + ε²)^(3/2) кулоновской сингулярности; 0.05 в релаксации, 1e-12 в полировке",
            ],
            [
                "Время успокоения",
                "первый момент, когда разброс сторон релаксирующего треугольника остаётся ниже 0.01",
            ],
        ],
    },
    "notation": {
        "header_en": ["Symbol", "Meaning"],
        "header_ru": ["Символ", "Смысл"],
        "rows_en": [
            ["r_k = (x_k, y_k)", "position of ion k in the transverse plane"],
            ["ω₀", "trap pseudopotential frequency (preset 1)"],
            ["κ", "Coulomb strength (preset 1)"],
            ["γ_d", "Doppler-drag coefficient (preset 0.8)"],
            ["ε, ε_relax", "Coulomb softening; 1e-12 in the polish, 0.05 in the relaxation"],
            ["a", "equilateral crystal side, a = (3κ/ω₀²)^(1/3) = 3^(1/3)"],
            ["U", "total potential energy (trap + Coulomb)"],
            ["H", "6×6 position Hessian of U at the crystal"],
            ["ΔU", "binding energy released during cooling (= 1.7609)"],
            ["T_relax, T_hold", "relaxation (60) and static-hold (50) time spans"],
            ["t_s", "settle time from the drag sweep"],
        ],
        "rows_ru": [
            ["r_k = (x_k, y_k)", "положение иона k в поперечной плоскости"],
            ["ω₀", "частота псевдопотенциала ловушки (пресет 1)"],
            ["κ", "кулоновская сила (пресет 1)"],
            ["γ_d", "коэффициент доплеровского трения (пресет 0.8)"],
            ["ε, ε_relax", "кулоновское смягчение; 1e-12 в полировке, 0.05 в релаксации"],
            ["a", "сторона равностороннего кристалла, a = (3κ/ω₀²)^(1/3) = 3^(1/3)"],
            ["U", "полная потенциальная энергия (ловушка + кулон)"],
            ["H", "позиционный гессиан U размера 6×6 в кристалле"],
            ["ΔU", "высвобожденная при охлаждении энергия связи (= 1.7609)"],
            ["T_relax, T_hold", "интервалы релаксации (60) и статического удержания (50)"],
            ["t_s", "время успокоения из развертки по трению"],
        ],
    },
    "params_appendix": {
        "header_en": ["Symbol", "Value", "Role"],
        "header_ru": ["Символ", "Значение", "Роль"],
        "rows_en": [
            ["ω₀, κ, m", "1, 1, 1", "dimensionless trap frequency, Coulomb strength, ion mass"],
            ["γ_d", "0.8", "Doppler drag during relaxation"],
            [
                "ε_relax → ε",
                "0.05 → 1e-12",
                "softening in relaxation, strict balance in the polish",
            ],
            ["T_relax, T_hold", "60, 50", "relaxation and static-hold spans"],
            [
                "initial condition",
                "seeded random in [−1, 1]², v = 0 (seed 3)",
                "crystallization start",
            ],
            ["settle criterion", "side spread below 0.01", "gamma-sweep settle time"],
            [
                "sweeps",
                "κ ∈ {0.25, 0.5, 1, 2, 4}; γ_d ∈ {0.4, 0.6, 0.8, 1.2, 1.6, 2.4}",
                "scaling and drag-response re-runs",
            ],
            ["Ca⁺ scale", "m = 40 amu, trap 1 MHz", "physical mapping; κ sets the length scale"],
        ],
        "rows_ru": [
            ["ω₀, κ, m", "1, 1, 1", "безразмерные частота ловушки, кулоновская сила, масса иона"],
            ["γ_d", "0.8", "доплеровское трение при релаксации"],
            ["ε_relax → ε", "0.05 → 1e-12", "смягчение в релаксации, строгий баланс в полировке"],
            ["T_relax, T_hold", "60, 50", "интервалы релаксации и статического удержания"],
            [
                "начальное условие",
                "засеянный случай в [−1, 1]², v = 0 (зерно 3)",
                "старт кристаллизации",
            ],
            [
                "критерий успокоения",
                "разброс сторон ниже 0.01",
                "время успокоения в развертке по γ",
            ],
            [
                "развертки",
                "κ ∈ {0.25, 0.5, 1, 2, 4}; γ_d ∈ {0.4, 0.6, 0.8, 1.2, 1.6, 2.4}",
                "прогоны масштабирования и отклика на трение",
            ],
            [
                "шкала Ca⁺",
                "m = 40 а.е.м., ловушка 1 МГц",
                "физическое отображение; κ задаёт масштаб длины",
            ],
        ],
    },
    "bibtex": [
        "@article{paul1990,",
        "  author  = {Paul, W.},",
        "  title   = {Electromagnetic traps for charged and neutral particles},",
        "  journal = {Reviews of Modern Physics},",
        "  year    = {1990}, volume = {62}, pages = {531--540}}",
        "",
        "@article{itano1982,",
        "  author  = {Itano, W. M. and Wineland, D. J.},",
        "  title   = {Laser cooling of ions stored in harmonic and Penning traps},",
        "  journal = {Physical Review A},",
        "  year    = {1982}, volume = {25}, pages = {35--54}}",
        "",
        "@article{diedrich1987,",
        "  author  = {Diedrich, F. and Peik, E. and Chen, J. M. and Quint, W. and Walther, H.},",
        "  title   = {Observation of a phase transition of stored laser-cooled ions},",
        "  journal = {Physical Review Letters},",
        "  year    = {1987}, volume = {59}, pages = {2931--2934}}",
        "",
        "@article{dubin1999,",
        "  author  = {Dubin, D. H. E. and O'Neil, T. M.},",
        "  title   = {Trapped nonneutral plasmas, liquids, and crystals},",
        "  journal = {Reviews of Modern Physics},",
        "  year    = {1999}, volume = {71}, pages = {87--172}}",
    ],
}
