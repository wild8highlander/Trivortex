# -*- coding: utf-8 -*-
"""Content pack for TRX-04 (v1.0.0 Monograph Edition). Rendered by scripts/build_study_docs.py."""

PACK = {
    "meta": {
        "study_id": "TRX-04",
        "dir_name": "TRX-04-photon-fluid",
        "title_en": "Photon Fluid: Three Kerr Solitons (Spatial, 2-D)",
        "title_ru": "Фотонная жидкость: три керровских солитона (пространственные, 2-D)",
        "script": "trx04_photon_fluid.py",
        "results_json": "trx04_results.json",
        "scheme_file": "scheme_trx04.svg",
        "runtime_full": "9.4 s (9.415 s recorded with --figures)",
    },
    "essence_en": (
        "Three laser beams co-propagating in a focusing Kerr medium behave as a "
        "**photon fluid**: each beam is a spatial soliton of the nonlinear Schrödinger equation, "
        "and pairs of beams exchange conservative two-body forces whose sign is set by the "
        "relative phase — in-phase beams attract, anti-phase beams repel — with the exponential "
        "profile **V(r) = ∓U·e^(−r/w)**. The in-phase triplet realizes an optical Lagrange central "
        "configuration: an equilateral beam triangle of side a = 3 rotates rigidly at "
        "**ω = e^(−3/2) = 0.223130160**, the exponential-force counterpart of the Newtonian "
        "ω² = 3Gm/a³ of Theorem 3.1. The study verifies the choreography to machine precision: "
        "the triangle stays equilateral to 1.8e-08 over three full rotations, the measured "
        "rotation rate matches the analytic law to 1.1×10⁻¹¹, energy and angular momentum are "
        "conserved to 4.7e-16 and 2.2e-15, the anti-phase trio expands cleanly to 23.476, and an "
        "in-phase binary stays bound with a precessing orbit — an optical three-body scattering "
        "table closed by 9/9 checks PASS."
    ),
    "essence_ru": (
        "Три лазерных пучка, распространяющихся совместно в среде с фокусирующей "
        "керровской нелинейностью, ведут себя как **фотонная жидкость**: каждый пучок — "
        "пространственный солитон нелинейного уравнения Шрёдингера, а пары пучков обмениваются "
        "консервативными двухтельными силами, знак которых задаёт относительная фаза — синфазные "
        "пучки притягиваются, противофазные отталкиваются — с экспоненциальным профилем "
        "**V(r) = ∓U·e^(−r/w)**. Синфазный триплет реализует оптическую лагранжеву центральную "
        "конфигурацию: равносторонний треугольник пучков со стороной a = 3 жёстко вращается с "
        "**ω = e^(−3/2) = 0.223130160** — экспоненциальным аналогом ньютоновской ω² = 3Gm/a³ из "
        "теоремы 3.1. Исследование верифицирует хореографию с машинной точностью: треугольник "
        "остаётся равносторонним до 1.8e-08 на протяжении трёх полных оборотов, измеренная "
        "угловая скорость совпадает с аналитическим законом до 1.1×10⁻¹¹, энергия и момент "
        "импульса сохраняются до 4.7e-16 и 2.2e-15, противофазное трио чисто разлетается до "
        "23.476, а синфазная бинарная пара остаётся связанной с прецессирующей орбитой — "
        "оптическая таблица трёхтельного рассеяния, замкнутая 9/9 проверками PASS."
    ),
    "mission_en": [
        (
            "Spatial solitons turn a nonlinear optical medium into a collisionless photon gas with "
            "genuine two-body forces. This makes optics a unique laboratory for the three-body "
            'problem: the "bodies" are beams of light, the force law is written by the medium, and '
            "the sign of every pairwise force is set by a phase dial. This study asks whether the "
            "crown jewel of the classical three-body problem — the rigidly rotating equilateral "
            "triangle of Lagrange — survives in this optical setting, and answers it quantitatively: "
            "the equilateral configuration is a central configuration for the exponential Kerr force "
            "exactly as it is for Newtonian gravity, with the rotation law "
            "ω² = 3Ue^(−a/w)/(maw) = 0.049787 at the preset side a = 3."
        ),
        (
            "The verification program is deliberately strict. The rotating triangle must stay "
            "equilateral to 1e-6 over three full turns (achieved 1.8e-08) and its measured rotation "
            "rate must reproduce the analytic ω = 0.223130160 within 1e-8 (achieved agreement to "
            "1.1×10⁻¹¹). Energy must be conserved in all three runs — rotation, repulsion, binary — "
            "to 1e-10, and angular momentum to the same level (achieved 4.7e-16, 3.6e-16, 3.0e-12 "
            "and 2.2e-15). The anti-phase trio must not collapse and must expand (final separation "
            "23.476 from initial 3.000), and the in-phase binary must remain inside the bound window "
            "separation ∈ [0.5, 6] over t = 80 (observed range [0.635, 3.000]). All nine checks PASS "
            "in the recorded full run, so the optical three-body table can be quoted as verified "
            "fact rather than simulation folklore."
        ),
    ],
    "mission_ru": [
        (
            "Пространственные солитоны превращают нелинейную оптическую среду в бесстолкновительный "
            "фотонный газ с настоящими двухтельными силами. Это делает оптику уникальной лабораторией "
            "задачи трёх тел: «телами» служат световые пучки, закон силы записан самой средой, а знак "
            "каждой парной силы задаётся «ручкой фазы». Данное исследование спрашивает, переживает ли "
            "эту оптическую среду жемчужина классической задачи трёх тел — жёстко вращающийся "
            "равносторонний треугольник Лагранжа, — и отвечает количественно: равносторонняя "
            "конфигурация является центральной конфигурацией для экспоненциальной керровской силы "
            "ровно так же, как и для ньютоновской гравитации, с законом вращения "
            "ω² = 3Ue^(−a/w)/(maw) = 0.049787 при пресетной стороне a = 3."
        ),
        (
            "Верификационная программа нарочито строга. Вращающийся треугольник обязан оставаться "
            "равносторонним до 1e-6 на протяжении трёх полных оборотов (достигнуто 1.8e-08), а его "
            "измеренная угловая скорость обязана воспроизвести аналитическую ω = 0.223130160 с "
            "точностью 1e-8 (достигнуто согласие 1.1×10⁻¹¹). Энергия должна сохраняться во всех "
            "трёх прогонах — вращение, отталкивание, бинарная пара — до 1e-10, момент импульса — до "
            "того же уровня (достигнуто 4.7e-16, 3.6e-16, 3.0e-12 и 2.2e-15). Противофазное трио не "
            "должно коллапсировать и должно разлетаться (конечное расстояние 23.476 против "
            "начального 3.000), а синфазная бинарная пара обязана оставаться в связанном окне "
            "расстояний [0.5, 6] на протяжении t = 80 (наблюдаемый диапазон [0.635, 3.000]). Все "
            "девять проверок PASS в записанном полном прогоне, поэтому оптическую трёхтельную "
            "таблицу можно цитировать как проверенный факт, а не фольклор моделирования."
        ),
    ],
    "physics_en": [
        (
            "In a medium with a focusing Kerr nonlinearity the refractive index grows with "
            "intensity, so a bright beam digs its own waveguide and propagates without diffracting — "
            "a spatial soliton of the equation iA_z + ½∇²A + |A|²A = 0. Two such beams whose tails "
            "overlap exert forces on one another through the shared nonlinear index: coherent, "
            "in-phase beams interfere constructively in the overlap region and attract, while "
            "anti-phase beams interfere destructively and repel. In the particle approximation — the "
            "working horse of this study — each beam is replaced by a point body of mass m moving in "
            "the transverse plane, and the pair interaction is the exponential law "
            "V_pm(r) = −Ue^(−r/w) (in phase) and V_ap(r) = +Ue^(−r/w) (anti-phase), with force "
            "magnitude (U/w)·e^(−r/w). The length w is the interaction scale (beam-waist unit) and U "
            "the potential depth."
        ),
        (
            "The equilateral triangle is special for any central force between equal members. At the "
            "vertices of an equilateral triangle of side a each beam feels two edge forces of "
            "magnitude F = (U/w)e^(−a/w) directed along the sides; their resultant is √3·F and points "
            "exactly at the centroid, at distance r_c = a/√3. The balance √3·F = mω²r_c then fixes "
            "the rigid rotation rate ω² = 3Ue^(−a/w)/(maw) — the same central-configuration balance "
            "that produces the Lagrange equilateral solution in the Newtonian problem, where "
            "ω² = 3Gm/a³. Sign flips matter as much as magnitudes: switching one phase to anti-phase "
            "converts one edge force from attraction to repulsion, the resultant no longer points at "
            "the centroid, and the rigid rotation is destroyed — the anti-phase trio simply expands. "
            "A pair of in-phase beams with negative relative energy forms a bound binary whose orbit "
            "precesses, because the exponential force is not inverse-square."
        ),
    ],
    "physics_ru": [
        (
            "В среде с фокусирующей керровской нелинейностью показатель преломления растёт с "
            "интенсивностью, поэтому яркий пучок выкапывает собственный волновод и распространяется "
            "без дифракционного расплывания — это пространственный солитон уравнения "
            "iA_z + ½∇²A + |A|²A = 0. Два таких пучка с перекрывающимися хвостами действуют друг на "
            "друга через общую нелинейную добавку к показателю: когерентные синфазные пучки "
            "интерферируют конструктивно в области перекрытия и притягиваются, а противофазные "
            "интерферируют деструктивно и отталкиваются. В частичном приближении — рабочем инструменте "
            "данного исследования — каждый пучок заменяется точечным телом массы m, движущимся в "
            "поперечной плоскости, а парное взаимодействие задаётся экспоненциальным законом "
            "V_pm(r) = −Ue^(−r/w) (синфазно) и V_ap(r) = +Ue^(−r/w) (в противофазе) с величиной силы "
            "(U/w)·e^(−r/w). Длина w — масштаб взаимодействия (единица перетяжки пучка), U — глубина "
            "потенциала."
        ),
        (
            "Равносторонний треугольник выделен для любой центральной силы между равными участниками. "
            "В вершинах равностороннего треугольника со стороной a каждый пучок чувствует две "
            "силы вдоль сторон величиной F = (U/w)e^(−a/w); их равнодействующая равна √3·F и "
            "направлена точно в центроид, находящийся на расстоянии r_c = a/√3. Баланс "
            "√3·F = mω²r_c фиксирует скорость жёсткого вращения ω² = 3Ue^(−a/w)/(maw) — тот же "
            "баланс центральной конфигурации, что даёт лагранжево равностороннее решение в "
            "ньютоновской задаче, где ω² = 3Gm/a³. Смены знака важны не меньше величин: перевод "
            "одной фазы в противофазу превращает одну краевую силу из притяжения в отталкивание, "
            "равнодействующая перестаёт указывать в центроид, и жёсткое вращение разрушается — "
            "противофазное трио просто разлетается. Пара синфазных пучков с отрицательной "
            "относительной энергией образует связанную бинарную систему с прецессирующей орбитой, "
            "поскольку экспоненциальная сила не является обратно-квадратичной."
        ),
    ],
    "preset_table": {
        "header_en": ["Parameter", "Value", "Meaning"],
        "header_ru": ["Параметр", "Значение", "Смысл"],
        "rows_en": [
            [
                "U, w, m",
                "1, 1, 1",
                "potential depth, interaction scale, soliton mass (natural units)",
            ],
            ["a", "3", "triangle side of the rotation run; operating point"],
            ["r_c", "a/√3 = 1.732051", "orbit radius of each beam about the centroid"],
            ["ω", "e^(−3/2) = 0.223130160", "analytic rotation rate (ω² = e^(−3) = 0.049787)"],
            ["T_rotation", "84.4778 = 3·2π/ω", "rotation run: three full turns"],
            [
                "anti-phase run",
                "same geometry, zero velocities, T = 40",
                "repulsive expansion test",
            ],
            ["binary", "r₀ = 3, v_b = ±0.15, E_rel = −0.027, T = 80", "in-phase bound-pair run"],
            ["integrator", "DOP853, rtol = atol = 1e-12, max_step = 0.1", "all runs, dense output"],
        ],
        "rows_ru": [
            [
                "U, w, m",
                "1, 1, 1",
                "глубина потенциала, масштаб взаимодействия, масса солитона (естественные единицы)",
            ],
            ["a", "3", "сторона треугольника во вращательном прогоне; рабочая точка"],
            ["r_c", "a/√3 = 1.732051", "радиус орбиты каждого пучка вокруг центроида"],
            [
                "ω",
                "e^(−3/2) = 0.223130160",
                "аналитическая скорость вращения (ω² = e^(−3) = 0.049787)",
            ],
            ["T_rotation", "84.4778 = 3·2π/ω", "вращательный прогон: три полных оборота"],
            [
                "противофазный прогон",
                "та же геометрия, нулевые скорости, T = 40",
                "тест отталкивающего разлёта",
            ],
            [
                "бинарная пара",
                "r₀ = 3, v_b = ±0.15, E_rel = −0.027, T = 80",
                "прогон синфазной связанной пары",
            ],
            [
                "интегратор",
                "DOP853, rtol = atol = 1e-12, max_step = 0.1",
                "все прогоны, плотный вывод",
            ],
        ],
    },
    "equations": [
        {
            "id": "E1",
            "latex": "i\\,\\frac{\\partial A}{\\partial z} + \\tfrac{1}{2}\\nabla_\\perp^2 A + |A|^2 A = 0",
            "desc_en": "Focusing nonlinear Schrödinger equation — the underlying field equation (documented context)",
            "desc_ru": "Фокусирующее нелинейное уравнение Шрёдингера — исходное полевое уравнение (контекст)",
        },
        {
            "id": "E2",
            "latex": "V_{\\rm pm}(r) = -U\\,e^{-r/w}, \\qquad V_{\\rm ap}(r) = +U\\,e^{-r/w}",
            "desc_en": "Pair potentials of two spatial solitons: in phase (attraction) and anti-phase (repulsion)",
            "desc_ru": "Парные потенциалы двух пространственных солитонов: синфазно (притяжение) и в противофазе (отталкивание)",
        },
        {
            "id": "E3",
            "latex": "m\\,\\ddot{\\mathbf{r}}_k = \\sum_{l\\neq k} s\\,\\frac{U}{w}\\,e^{-r_{kl}/w}\\,\\frac{\\mathbf{r}_k-\\mathbf{r}_l}{r_{kl}}, \\quad s=-1\\ \\text{(in phase)},\\ s=+1\\ \\text{(anti-phase)}",
            "desc_en": "Planar equations of motion of the N photon-fluid bodies with all-pairs forces",
            "desc_ru": "Плоские уравнения движения N тел фотонной жидкости с силами всех пар",
        },
        {
            "id": "E4",
            "latex": "\\omega^2 = \\frac{3U\\,e^{-a/w}}{m\\,a\\,w} \\;\\left(= e^{-3} = 0.049787\\ \\text{at the preset}\\right)",
            "desc_en": "Rotation rate of the rigidly rotating equilateral beam triangle (Lagrange central configuration)",
            "desc_ru": "Скорость вращения жёсткого равностороннего треугольника пучков (лагранжева центральная конфигурация)",
        },
        {
            "id": "E5",
            "latex": "E = \\sum_k \\tfrac{1}{2}m\\,|\\dot{\\mathbf{r}}_k|^2 + \\sum_{k<l} s\\,U\\,e^{-r_{kl}/w}, \\qquad L_z = \\sum_k m\\,(x_k\\dot{y}_k - y_k\\dot{x}_k)",
            "desc_en": "Conserved invariants of the planar model: total energy and angular momentum",
            "desc_ru": "Сохраняющиеся инварианты плоской модели: полная энергия и момент импульса",
        },
        {
            "id": "E6",
            "latex": "E_{\\rm rel} = m\\,v_b^2 - U\\,e^{-r_0/w} < 0 \\;\\Leftrightarrow\\; v_b < \\sqrt{U\\,e^{-r_0/w}} = e^{-3/2} \\approx 0.223130",
            "desc_en": "Bound-state condition of the in-phase binary at launch separation r₀ (preset: 0.0225 − 0.049787 = −0.027)",
            "desc_ru": "Условие связанности синфазной бинарной пары при стартовом расстоянии r₀ (пресет: 0.0225 − 0.049787 = −0.027)",
        },
    ],
    "scheme_cap_en": (
        "TRX-04 scheme — photon fluid: three in-phase Kerr solitons in a focusing medium "
        "(left): the attractive pair forces along the triangle edges supply the centripetal balance "
        "mω²r_c of the rigidly rotating Lagrange beam triangle; the pair interaction (right): "
        "in-phase attraction V = −U·exp(−r/w), anti-phase repulsion V = +U·exp(−r/w), the operating "
        "point a = 3 and the binary bound-state condition."
    ),
    "scheme_cap_ru": (
        "Схема TRX-04 — фотонная жидкость: три синфазных керровских солитона в фокусирующей "
        "среде (слева): притягивающие парные силы вдоль сторон треугольника обеспечивают "
        "центростремительный баланс mω²r_c жёстко вращающегося лагранжева треугольника пучков; "
        "парное взаимодействие (справа): синфазное притяжение V = −U·exp(−r/w), противофазное "
        "отталкивание V = +U·exp(−r/w), рабочая точка a = 3 и условие связанности бинарной пары."
    ),
    "scheme_walk_en": [
        [
            "Focusing Kerr medium (left panel)",
            "top view of the nonlinear medium; the beams propagate along z, out of the page",
        ],
        [
            "Three beam spots",
            "in-phase spatial solitons at the vertices of an equilateral triangle of side a = 3",
        ],
        [
            "Gold arrows along the edges",
            "attractive pair forces that supply the centripetal balance mω²r_c about the centroid",
        ],
        [
            "Rotation arrow, ω = 0.2231",
            "rigid rotation of the Lagrange beam triangle; the dashed radius marks r_c = a/√3",
        ],
        [
            "Pair-energy curves (right panel)",
            "in-phase attraction V = −U·exp(−r/w) against anti-phase repulsion V = +U·exp(−r/w) above the zero line V = 0 (free beams)",
        ],
        [
            "Operating point a = 3 and info boxes",
            "force (U/w)·exp(−3) = 0.0498, rotation law ω² = 3U·exp(−a/w)/(maw), and the binary note with escape threshold 0.2231 for the preset v_b = 0.15",
        ],
    ],
    "scheme_walk_ru": [
        [
            "Фокусирующая керровская среда (левая панель)",
            "вид сверху на нелинейную среду; пучки распространяются вдоль z, из плоскости рисунка",
        ],
        [
            "Три пятна пучков",
            "синфазные пространственные солитоны в вершинах равностороннего треугольника со стороной a = 3",
        ],
        [
            "Золотые стрелки вдоль сторон",
            "притягивающие парные силы, создающие центростремительный баланс mω²r_c вокруг центроида",
        ],
        [
            "Стрелка вращения, ω = 0.2231",
            "жёсткое вращение лагранжева треугольника пучков; пунктирный радиус отмечает r_c = a/√3",
        ],
        [
            "Кривые парной энергии (правая панель)",
            "синфазное притяжение V = −U·exp(−r/w) против противофазного отталкивания V = +U·exp(−r/w) над нулевой линией V = 0 (свободные пучки)",
        ],
        [
            "Рабочая точка a = 3 и информационные блоки",
            "сила (U/w)·exp(−3) = 0.0498, закон вращения ω² = 3U·exp(−a/w)/(maw) и заметка о бинарной паре с порогом убегания 0.2231 для пресета v_b = 0.15",
        ],
    ],
    "mapping": {
        "header_en": ["Quantity in this study", "TRIVORTEX analog", "Comment"],
        "header_ru": ["Величина исследования", "Аналог в TRIVORTEX", "Комментарий"],
        "rows_en": [
            [
                "Three Kerr solitons",
                "three gravitating bodies",
                "same central-configuration problem",
            ],
            [
                "Exponential attraction e^(−r/w)",
                "Newtonian 1/r attraction",
                "force law changes, geometry does not",
            ],
            [
                "Rotating beam triangle",
                "Lagrange equilateral solution",
                "identical balance structure, Theorem 3.1",
            ],
            [
                "Relative phase (in/anti)",
                "circulation sign in the vortex model",
                "attraction ↔ repulsion switch",
            ],
            [
                "Rotation law ω² = 3Ue^(−a/w)/(maw)",
                "ω² = 3Gm/a³ for point masses",
                "third-law-type verification target",
            ],
            [
                "In-phase binary with precession",
                "eccentric two-body orbit",
                "non-Kepler force, same invariant bookkeeping",
            ],
        ],
        "rows_ru": [
            [
                "Три керровских солитона",
                "три гравитирующих тела",
                "та же задача центральной конфигурации",
            ],
            [
                "Экспоненциальное притяжение e^(−r/w)",
                "ньютоновское притяжение 1/r",
                "закон силы меняется, геометрия — нет",
            ],
            [
                "Вращающийся треугольник пучков",
                "лагранжево равностороннее решение",
                "идентичная структура баланса, теорема 3.1",
            ],
            [
                "Относительная фаза (синфазно/противофазно)",
                "знак циркуляции в вихревой модели",
                "переключатель притяжение ↔ отталкивание",
            ],
            [
                "Закон вращения ω² = 3Ue^(−a/w)/(maw)",
                "ω² = 3Gm/a³ для точечных масс",
                "проверочная цель «третьего закона»",
            ],
            [
                "Синфазная бинарная пара с прецессией",
                "эксцентрическая двухтельная орбита",
                "некеплерова сила, тот же учёт инвариантов",
            ],
        ],
    },
    "nondim_en": (
        "All quantities are dimensionless in beam units: lengths in units of the interaction "
        "scale w (the beam-waist unit), energies in units of the potential depth U, masses in units "
        "of the soliton mass m, and times in units of w·√(m/U). At the preset U = w = m = 1 every "
        "quantity is a plain number: the rotation rate ω = 0.223130160 is dimensionless, the "
        "triangle side is a = 3, and the binary launch velocity is v_b = 0.15."
    ),
    "nondim_ru": (
        "Все величины безразмерны в пучковых единицах: длины — в единицах масштаба "
        "взаимодействия w (единица перетяжки пучка), энергии — в единицах глубины потенциала U, "
        "массы — в единицах массы солитона m, время — в единицах w·√(m/U). В пресете "
        "U = w = m = 1 каждая величина — обычное число: скорость вращения ω = 0.223130160 "
        "безразмерна, сторона треугольника a = 3, стартовая скорость бинарной пары v_b = 0.15."
    ),
    "checks": {
        "header_en": ["Check", "Target", "Tolerance"],
        "header_ru": ["Проверка", "Цель", "Допуск"],
        "rows_en": [
            ["Equilateral deviation over 3 rotations (max rel. side change)", "0", "1e-6"],
            ["Measured rotation rate vs analytic ω = 0.223130160", "equal", "1e-8"],
            ["Energy drift, rotation run (t = 84.4778)", "0", "1e-10"],
            ["Angular-momentum drift, rotation run", "0", "1e-10"],
            ["Anti-phase trio: min pairwise distance ≥ 0.95a", "yes", "exact"],
            ["Anti-phase trio expands (final > initial separation)", "yes", "exact"],
            ["Energy drift, anti-phase run (t = 40)", "0", "1e-10"],
            ["Binary: separation within [0.5, 6] over t = 80", "yes", "exact"],
            ["Energy drift, binary run (t = 80)", "0", "1e-10"],
        ],
        "rows_ru": [
            [
                "Отклонение от равносторонности за 3 оборота (макс. относительное изменение стороны)",
                "0",
                "1e-6",
            ],
            ["Измеренная скорость вращения против аналитической ω = 0.223130160", "равны", "1e-8"],
            ["Дрейф энергии, вращательный прогон (t = 84.4778)", "0", "1e-10"],
            ["Дрейф момента импульса, вращательный прогон", "0", "1e-10"],
            ["Противофазное трио: мин. парное расстояние ≥ 0.95a", "да", "точно"],
            ["Противофазное трио разлетается (конец > начала)", "да", "точно"],
            ["Дрейф энергии, противофазный прогон (t = 40)", "0", "1e-10"],
            ["Бинарная пара: расстояние в [0.5, 6] на протяжении t = 80", "да", "точно"],
            ["Дрейф энергии, бинарный прогон (t = 80)", "0", "1e-10"],
        ],
    },
    "figure_caps": {
        "fig01_photon_fluid_landscape.png": {
            "cap_en": "Model landscape: photon-fluid pair interaction and the initial beam triangle of the rotation run.",
            "cap_ru": "Ландшафт модели: парное взаимодействие фотонной жидкости и стартовый треугольник пучков вращательного прогона.",
            "walk_en": "Panel (a) shows the pair interaction landscape: in-phase attraction V = −U·e^(−r/w) (gold) against anti-phase repulsion V = +U·e^(−r/w) (red dashed) — the phase acts as an attractive/repulsive charge; the operating point a = 3 sits at force (U/w)·e^(−a/w) = 0.0498. Panel (b) shows the initial condition of the rotation run: the equilateral beam triangle with side a = 3, orbit radius r_c = a/√3 = 1.732051, and pair forces supplying the centripetal balance mω²r_c at the preset rate ω = 0.223130.",
            "walk_ru": "Панель (а) показывает ландшафт парного взаимодействия: синфазное притяжение V = −U·e^(−r/w) (золотое) против противофазного отталкивания V = +U·e^(−r/w) (красный пунктир) — фаза действует как притягивающий/отталкивающий заряд; рабочая точка a = 3 лежит при силе (U/w)·e^(−a/w) = 0.0498. Панель (б) показывает начальное условие вращательного прогона: равносторонний треугольник пучков со стороной a = 3, радиус орбиты r_c = a/√3 = 1.732051 и парные силы, создающие центростремительный баланс mω²r_c при пресетной скорости ω = 0.223130.",
        },
        "fig02_triangle_rotation.png": {
            "cap_en": "Headline result: rigid rotation of the photon-fluid triangle over three full turns and its equilateral rigidity.",
            "cap_ru": "Главный результат: жёсткое вращение треугольника фотонной жидкости за три полных оборота и его равносторонняя жёсткость.",
            "walk_en": "Panel (a) shows the worldlines of the three beams over three full turns (T = 84.4778): circular orbits about the common centroid, the triangle carried rigidly like a solid body. Panel (b) plots the relative side deviations |d(t) − a|/a on a log scale: they never exceed 1.8e-08, a factor of about 56 inside the 1e-6 acceptance tolerance, while the measured rotation rate 0.223130160 matches the analytic ω = 0.223130160 — the optical Lagrange configuration confirmed dynamically.",
            "walk_ru": "Панель (а) показывает мировые линии трёх пучков за три полных оборота (T = 84.4778): круговые орбиты вокруг общего центроида, треугольник переносится жёстко, как твёрдое тело. Панель (б) откладывает относительные отклонения сторон |d(t) − a|/a в логарифмическом масштабе: они не превышают 1.8e-08 — примерно в 56 раз внутри допуска 1e-6, — а измеренная скорость вращения 0.223130160 совпадает с аналитической ω = 0.223130160: оптическая лагранжева конфигурация подтверждена динамически.",
        },
        "fig03_parameter_sweeps.png": {
            "cap_en": "Parameter sweeps: rotation rate versus triangle side and the binary bound/unbound map versus launch velocity.",
            "cap_ru": "Развёртки параметров: скорость вращения в зависимости от стороны треугольника и карта связанности бинарной пары в зависимости от стартовой скорости.",
            "walk_en": "Panel (a) sweeps the triangle side: the analytic Kerr law ω(a) = √(3Ue^(−a/w)/(maw)) runs from 0.450558 at a = 2 through the preset 0.223130 at a = 3 down to 0.011216 at a = 8, numeric DOP853 re-runs sit on the curve at all seven grid sides, and the Newtonian 1/r reference (0.333333 at the preset) decays markedly slower — 0.076547 at a = 8 against the Kerr 0.011216. Panel (b) maps the binary outcome versus launch velocity: max separation stays at 3.0 for v_b ≤ 0.26 and grows to 7.7515, 13.2491, 16.4935 and 19.1521 for v_b = 0.28–0.34 over T = 40, bracketing the analytic escape threshold v_b* = e^(−3/2) = 0.223130.",
            "walk_ru": "Панель (а) развёртывает сторону треугольника: аналитический керровский закон ω(a) = √(3Ue^(−a/w)/(maw)) идёт от 0.450558 при a = 2 через пресет 0.223130 при a = 3 до 0.011216 при a = 8, численные повторные прогоны DOP853 ложатся на кривую во всех семи точках сетки, а ньютоновская эталонная кривая 1/r (0.333333 в пресете) спадает заметно медленнее — 0.076547 при a = 8 против керровских 0.011216. Панель (б) картирует исход для бинарной пары в зависимости от стартовой скорости: максимальное расстояние остаётся 3.0 при v_b ≤ 0.26 и растёт до 7.7515, 13.2491, 16.4935 и 19.1521 при v_b = 0.28–0.34 за T = 40, обрамляя аналитический порог убегания v_b* = e^(−3/2) = 0.223130.",
        },
        "fig04_binary_dynamics_invariants.png": {
            "cap_en": "Dynamics and invariants: precessing bound orbit of the in-phase binary and the energy-drift bookkeeping of all three runs.",
            "cap_ru": "Динамика и инварианты: прецессирующая связанная орбита синфазной бинарной пары и учёт дрейфа энергии во всех трёх прогонах.",
            "walk_en": "Panel (a) shows the precessing bound orbit of the in-phase binary (launch separation 3, transverse velocity 0.15, E_rel = −0.027 < 0, T = 80): the separation breathes inside [0.635, 3.000] while the orbit axis slowly rotates — the signature of a non-inverse-square force. Panel (b) tracks the energy drift |E(t) − E(0)| of the three runs on a log scale: 4.7e-16 (rotation), 3.6e-16 (anti-phase trio) and 3.0e-12 (binary), all far below the 1e-10 acceptance tolerance.",
            "walk_ru": "Панель (а) показывает прецессирующую связанную орбиту синфазной бинарной пары (стартовое расстояние 3, поперечная скорость 0.15, E_rel = −0.027 < 0, T = 80): расстояние дышит внутри [0.635, 3.000], а ось орбиты медленно поворачивается — подпись не обратно-квадратичной силы. Панель (б) отслеживает дрейф энергии |E(t) − E(0)| трёх прогонов в логарифмическом масштабе: 4.7e-16 (вращение), 3.6e-16 (противофазное трио) и 3.0e-12 (бинарная пара) — всё далеко ниже допуска 1e-10.",
        },
    },
    "results_block": [
        "triangle_equilateral_deviation   = 1.8e-08",
        "measured_rotation_rate           = 2.231302e-01 (target 0.22313016014842985)",
        "energy_conservation_rotation     = 4.7e-16",
        "angular_momentum_conservation    = 2.2e-15",
        "antiphase_no_collapse            = PASS (min distance 3.0000 >= 0.95 a)",
        "antiphase_expands                = PASS (final separation 23.476 > initial 3.000)",
        "energy_conservation_repulsion    = 3.6e-16",
        "binary_stays_bound               = PASS (separation range [0.635, 3.000])",
        "binary_energy_conservation       = 3.0e-12",
        "status: PASS (9/9)",
    ],
    "abstract_en": (
        "This monograph treats three laser beams propagating through a focusing Kerr medium "
        "as a photon fluid whose members — spatial solitons of the nonlinear Schrödinger equation — "
        "interact through phase-dependent two-body forces: in-phase beams attract with "
        "V = −Ue^(−r/w), anti-phase beams repel with V = +Ue^(−r/w). In the particle approximation "
        "the in-phase triplet forms a Lagrange central configuration: an equilateral beam triangle "
        "of side a = 3 rotating rigidly at ω = 0.223130160, fixed by the force balance "
        "ω² = 3Ue^(−a/w)/(maw) — the optical sibling of Newton's Lagrange solution. The numerical "
        "experiment verifies the choreography to machine precision: the triangle stays equilateral "
        "to 1.8e-08 over three full rotations (T = 84.4778), the measured rotation rate matches the "
        "analytic value to 1.1×10⁻¹¹, energy and angular momentum are conserved to 4.7e-16 and "
        "2.2e-15, the anti-phase trio expands to 23.476 without collapse, and an in-phase binary "
        "with E_rel = −0.027 stays bound (separation within [0.635, 3.000], energy drift 3.0e-12) "
        "over t = 80. All nine acceptance checks PASS."
    ),
    "abstract_ru": (
        "Монография рассматривает три лазерных пучка, распространяющихся в фокусирующей "
        "керровской среде, как фотонную жидкость, участники которой — пространственные солитоны "
        "нелинейного уравнения Шрёдингера — взаимодействуют через фазозависимые двухтельные силы: "
        "синфазные пучки притягиваются с V = −Ue^(−r/w), противофазные отталкиваются с "
        "V = +Ue^(−r/w). В частичном приближении синфазный триплет образует лагранжеву центральную "
        "конфигурацию: равносторонний треугольник пучков со стороной a = 3 жёстко вращается с "
        "ω = 0.223130160, что фиксируется силовым балансом ω² = 3Ue^(−a/w)/(maw) — оптический брат "
        "лагранжева решения Ньютона. Численный эксперимент верифицирует хореографию с машинной "
        "точностью: треугольник остаётся равносторонним до 1.8e-08 на протяжении трёх полных "
        "оборотов (T = 84.4778), измеренная скорость вращения совпадает с аналитической до "
        "1.1×10⁻¹¹, энергия и момент импульса сохраняются до 4.7e-16 и 2.2e-15, противофазное трио "
        "разлетается до 23.476 без коллапса, а синфазная бинарная пара с E_rel = −0.027 остаётся "
        "связанной (расстояние в [0.635, 3.000], дрейф энергии 3.0e-12) на протяжении t = 80. "
        "Развёртка по стороне треугольника подтверждает закон вращения именно как закон: численные "
        "повторные прогоны DOP853 ложатся на аналитическую кривую во всех семи точках сетки "
        "a = 2.0…8.0. Все девять контрольных проверок PASS."
    ),
    "intro_en": [
        (
            "Self-trapping of light is as old as nonlinear optics. Askar'yan proposed in 1962 that an "
            "intense beam could raise the refractive index enough to guide itself, and Chiao, Garmire "
            "and Townes demonstrated self-trapping of optical beams in 1964 — the experiment that "
            'made "a beam of light behaving as a particle of light" concrete. The pure Kerr '
            "nonlinearity, however, makes the two-dimensional self-trapping problem critical (the "
            "Townes collapse), so stable spatial solitons in real media rely on saturation — "
            "photorefractive crystals, nematic liquid crystals, atomic vapors. The concept that "
            "survives in every such medium is the same: a beam that carries itself like a particle."
        ),
        (
            "The next step was the realization that two such light particles exert forces on each "
            "other. Reynaud and Barthelemy (1990) demonstrated optically controlled interaction "
            "between two fundamental soliton beams, and Aitchison and colleagues (1991) observed "
            "spatial soliton interactions directly in a nonlinear glass waveguide. The decisive "
            "control knob is the relative phase: coherent in-phase beams attract, anti-phase beams "
            "repel, and quadrature beams pass through — the phase acts as a switchable gravitational "
            "charge. Stegeman and Segev (1999) consolidated this physics in their review of optical "
            "spatial solitons and their interactions, the founding literature of beam-by-beam "
            "collision experiments."
        ),
        (
            "The collective picture — many beams as a gas or fluid of mutually attracting particles — "
            "was pushed by Snyder, Mitchell and Kivshar (1995), who unified the self-trapping of "
            "light and matter waves, and by Bialynicki-Birula's photon-wave description of light as a "
            "many-body wave system. Today the umbrella term is quantum fluids of light, reviewed by "
            "Carusotto and Ciuti (2013); nematicons in nematic liquid crystals (Assanto and "
            "Peccianti, 2012) remain the cleanest classical realization of long-range, "
            "phase-tunable beam forces. Within this literature the three-beam triangle is the "
            "simplest genuinely collective object: every member feels both others, and no pairwise "
            "subproblem predicts the outcome."
        ),
        (
            "That is precisely the situation Lagrange analyzed in 1772, when he found that three "
            "bodies placed at the vertices of an equilateral triangle and given the right velocities "
            "rotate rigidly forever — the only non-collinear central configuration of the Newtonian "
            "three-body problem and the content of Theorem 3.1 in the TRIVORTEX monograph. This study "
            "transplants that construction into the photon fluid: the exponential Kerr force replaces "
            "the Newtonian 1/r force, the phase replaces the mass sign, and the equilateral beam "
            "triangle replaces the celestial one. The siblings are already in place — TRX-03 in the "
            "temporal (fiber-laser) domain, TRX-05 with field zeros instead of maxima, TRX-08 with "
            "ions in a trap — making TRX-04 the spatial-optics anchor of the choreography family."
        ),
    ],
    "intro_ru": [
        (
            "Самозахват света ровесник нелинейной оптики. Аскарьян предположил в 1962 году, что "
            "интенсивный пучок способен поднять показатель преломления настолько, чтобы направлять "
            "сам себя, а Чио, Гармир и Таунс продемонстрировали в 1964 году самозахват оптических "
            "пучков — эксперимент, сделавший осязаемой формулу «пучок света ведёт себя как частица "
            "света». Однако чистая керровская нелинейность делает двумерную задачу самозахвата "
            "критической (коллапс Таунса), поэтому устойчивые пространственные солитоны в реальных "
            "средах опираются на насыщение — фоторефрактивные кристаллы, нематические жидкие "
            "кристаллы, атомные пары. Понятие, которое переживает каждую такую среду, одно: пучок, "
            "несущий сам себя, как частица."
        ),
        (
            "Следующим шагом стало осознание, что две такие световые частицы действуют друг на друга "
            "с силой. Рено и Бартелеми (1990) продемонстрировали оптически управляемое взаимодействие "
            "двух фундаментальных солитонных пучков, а Айтчисон с соавторами (1991) наблюдали "
            "взаимодействие пространственных солитонов непосредственно в нелинейном стеклянном "
            "волноводе. Решающая ручка управления — относительная фаза: когерентные синфазные пучки "
            "притягиваются, противофазные отталкиваются, пучки в квадратуре проходят насквозь — фаза "
            "действует как переключаемый гравитационный заряд. Стегеман и Сегев (1999) свели эту "
            "физику воедино в обзоре оптических пространственных солитонов и их взаимодействий — "
            "основополагающей литературе пучок-к-пучку столкновительных экспериментов."
        ),
        (
            "Коллективную картину — много пучков как газ или жидкость взаимно притягивающихся частиц — "
            "продвинули Снайдер, Митчелл и Кившар (1995), объединившие самозахват света и волн материи, "
            "и Бялыницкий-Бируля, описавший свет как волновую систему многих тел. Сегодня зонтичный термин — квантовые жидкости света, обзор Карузотто и Чути "
            "(2013); нематиконы в нематических жидких кристаллах (Ассанто и Печчанти, 2012) остаются "
            "чистейшей классической реализацией дальнодействующих, настраиваемых фазой пучковых сил. "
            "В этой литературе треугольник из трёх пучков — простейший подлинно коллективный объект: "
            "каждый участник чувствует двух других, и ни одна парная подзадача не предсказывает "
            "исход."
        ),
        (
            "Это в точности ситуация, которую проанализировал Лагранж в 1772 году: три тела в "
            "вершинах равностороннего треугольника с подходящими скоростями вращаются жёстко вечно — "
            "единственная неколлинеарная центральная конфигурация ньютоновской задачи трёх тел и "
            "содержание теоремы 3.1 монографии TRIVORTEX. Данное исследование пересаживает эту "
            "конструкцию в фотонную жидкость: экспоненциальная керровская сила заменяет ньютоновскую "
            "1/r, фаза заменяет знак массы, а равносторонний треугольник пучков — небесный. Братья "
            "уже на местах — TRX-03 во временной (волоконно-лазерной) области, TRX-05 с нулями поля "
            "вместо максимумов, TRX-08 с ионами в ловушке, — что делает TRX-04 пространственно-"
            "оптическим якорем семейства хореографий."
        ),
    ],
    "derivation_en": [
        (
            "From field to particles. The focusing NLS (E1) admits the fundamental spatial soliton, "
            "and for well-separated beams the overlap of their exponential tails reduces the field "
            "problem to pairwise forces. Keeping the leading tail-overlap term gives the potentials "
            "(E2): V_pm(r) = −Ue^(−r/w) for coherent in-phase beams and V_ap(r) = +Ue^(−r/w) for "
            "anti-phase beams, with radial force magnitude (U/w)e^(−r/w). The equations of motion "
            "(E3) are then Newtonian mechanics on the transverse plane with N = 3 bodies and a soft, "
            "everywhere-regular interaction; the sign s = ±1 per pair encodes the optical phase. The "
            "model conserves the total energy E and the angular momentum L_z exactly, Eq. (E5), which "
            "provides the two invariants monitored by the acceptance checks."
        ),
        (
            "The Lagrange balance. For the equilateral triangle of side a, each beam feels two edge "
            "forces of magnitude F = (U/w)e^(−a/w) whose directions meet at 60°; their resultant is "
            "√3·F along the median, aimed at the centroid at distance r_c = a/√3. Uniform rotation "
            "with angular rate ω requires √3·F = mω²r_c, which solves to the rotation law (E4), "
            "ω² = 3Ue^(−a/w)/(maw). At the preset a = 3, w = U = m = 1 this gives ω² = e^(−3) = "
            "0.049787 and ω = e^(−3/2) = 0.223130160 — numerically the same constant as the binary "
            "escape threshold of (E6), a coincidence specific to the preset a = 3. The Newtonian "
            "counterpart ω² = 3Gm/a³ differs only in the force law: the geometry of the central "
            "configuration is universal, its rotation rate is not."
        ),
        (
            "The binary energetics. Two equal in-phase beams launched at separation r₀ with "
            "transverse velocities ±v_b carry relative energy (E6): E_rel = m·v_b² − Ue^(−r₀/w) with "
            "the reduced-mass factors absorbed into the equal-mass normalization. At the preset "
            "r₀ = 3, v_b = 0.15: E_rel = 0.0225 − 0.049787 = −0.027 < 0, bound. The escape threshold "
            "is v_b* = √(Ue^(−r₀/w)) = e^(−3/2) = 0.223130. Because the exponential force is not "
            "inverse-square, the bound orbit is not a closed Kepler ellipse: the separation oscillates "
            "between fixed turning points while the orbit axis precesses, and the angular-momentum "
            "barrier even traps launches slightly above v_b* for finite observation times — the "
            "boundary structure the velocity sweep of fig03 exposes."
        ),
    ],
    "derivation_ru": [
        (
            "От поля к частицам. Фокусирующее НУШ (E1) допускает фундаментальный пространственный "
            "солитон, и для хорошо разделённых пучков перекрытие их экспоненциальных хвостов сводит "
            "полевую задачу к парным силам. Удержание главного члена перекрытия хвостов даёт "
            "потенциалы (E2): V_pm(r) = −Ue^(−r/w) для когерентных синфазных пучков и "
            "V_ap(r) = +Ue^(−r/w) для противофазных с радиальной величиной силы (U/w)e^(−r/w). "
            "Уравнения движения (E3) — это ньютоновская механика на поперечной плоскости с N = 3 "
            "телами и мягким, всюду регулярным взаимодействием; знак s = ±1 для каждой пары "
            "кодирует оптическую фазу. Модель в точности сохраняет полную энергию E и момент "
            "импульса L_z, уравнение (E5), — это два инварианта, отслеживаемых контрольными "
            "проверками."
        ),
        (
            "Лагранжев баланс. Для равностороннего треугольника со стороной a каждый пучок чувствует "
            "две силы вдоль сторон величиной F = (U/w)e^(−a/w), направления которых сходятся под "
            "углом 60°; их равнодействующая равна √3·F вдоль медианы и нацелена в центроид на "
            "расстоянии r_c = a/√3. Равномерное вращение с угловой скоростью ω требует "
            "√3·F = mω²r_c, откуда закон вращения (E4): ω² = 3Ue^(−a/w)/(maw). В пресете "
            "a = 3, w = U = m = 1 это даёт ω² = e^(−3) = 0.049787 и ω = e^(−3/2) = 0.223130160 — "
            "численно ту же константу, что и порог убегания бинарной пары из (E6), совпадение, "
            "специфичное для пресета a = 3. Ньютоновский аналог ω² = 3Gm/a³ отличается только "
            "законом силы: геометрия центральной конфигурации универсальна, её скорость вращения — "
            "нет."
        ),
        (
            "Энергетика бинарной пары. Два равных синфазных пучка, запущенные на расстоянии r₀ с "
            "поперечными скоростями ±v_b, несут относительную энергию (E6): "
            "E_rel = m·v_b² − Ue^(−r₀/w) с факторами приведённой массы, поглощёнными нормировкой "
            "равных масс. В пресете r₀ = 3, v_b = 0.15: E_rel = 0.0225 − 0.049787 = −0.027 < 0 — "
            "связанное состояние. Порог убегания v_b* = √(Ue^(−r₀/w)) = e^(−3/2) = 0.223130. Поскольку "
            "экспоненциальная сила не обратно-квадратична, связанная орбита не является замкнутым "
            "кеплеровым эллипсом: расстояние колеблется между фиксированными поворотными точками, "
            "пока ось орбиты прецессирует, а центробежный барьер даже запирает запуски слегка выше "
            "v_b* на конечные времена наблюдения — граничная структура, которую обнажает развёртка "
            "по скорости на fig03."
        ),
    ],
    "connection_en": (
        "Within the TRIVORTEX program this study is the spatial-optics realization of "
        "Theorem 3.1. The three Kerr solitons play the three gravitating bodies; the rotating beam "
        "triangle is the Lagrange equilateral solution; and the measured rotation rate checks the "
        "central-configuration balance exactly as the Newtonian ω² = 3Gm/a³ does, with the "
        "exponential force ω² = 3Ue^(−a/w)/(maw) = 0.049787 at the preset. The relative optical "
        "phase plays the role of the circulation sign in the vortex model: in-phase is the "
        "equal-circulation, mutually attracting case that supports the choreography, anti-phase is "
        "the repulsive sign that destroys it — the same sign hierarchy that separates bound from "
        "unbound vortex pairs. The precessing binary adds the two-body layer of the same mapping: "
        "eccentric orbits, fixed turning points, conserved E and L_z, but a non-Kepler force law. "
        "TRX-03 repeats this structure on a line with temporal solitons, TRX-05 replaces field "
        "maxima by field zeros and recovers Kirchhoff's vortex equations, and TRX-08 trades "
        "photons for ions; together they demonstrate that the choreography sequence — pair law, "
        "central configuration, invariants — is portable across optics, fluids and celestial "
        "mechanics."
    ),
    "connection_ru": (
        "В рамках программы TRIVORTEX данное исследование — пространственно-оптическая "
        "реализация теоремы 3.1. Три керровских солитона играют три гравитирующих тела; "
        "вращающийся треугольник пучков — лагранжево равностороннее решение; а измеренная скорость "
        "вращения проверяет баланс центральной конфигурации в точности так, как это делает "
        "ньютоновская ω² = 3Gm/a³, с экспоненциальной силой ω² = 3Ue^(−a/w)/(maw) = 0.049787 в "
        "пресете. Относительная оптическая фаза играет знак циркуляции в вихревой модели: синфазный "
        "случай — равные циркуляции, взаимное притяжение, поддерживающее хореографию; "
        "противофазный — отталкивающий знак, её разрушающий, — та же иерархия знаков, что разделяет "
        "связанные и несвязанные вихревые пары. Прецессирующая бинарная пара добавляет двухтельный "
        "слой того же соответствия: эксцентрические орбиты, фиксированные поворотные точки, "
        "сохранённые E и L_z, но некеплеров закон силы. TRX-03 повторяет эту структуру на прямой с "
        "временными солитонами, TRX-05 заменяет максимумы поля нулями и восстанавливает уравнения "
        "Кирхгофа, TRX-08 меняет фотоны на ионы; вместе они демонстрируют, что "
        "хореографическая последовательность — парной закон, центральная конфигурация, инварианты — "
        "переносима между оптикой, гидродинамикой и небесной механикой."
    ),
    "method_en": [
        (
            "The model is a planar N-body system with the interleaved state layout "
            "[x₁, y₁, vx₁, vy₁, …]. At the preset U = w = m = 1 the triangle side is a = 3, the "
            "initial positions sit on the circle r_c = a/√3 = 1.732051, and the initial velocities are "
            "the rigid-rotation field ω·r_c with the analytic rate ω = √(3Ue^(−a/w)/(maw)) = "
            "0.22313016014842985. All runs integrate the equations of motion (E3) with the explicit "
            "Dormand–Prince 8(5,3) scheme (scipy DOP853, rtol = atol = 1e-12, max_step = 0.1, dense "
            "output for uniform sampling). The rotation run lasts T = 3·2π/ω = 84.4778 — three full "
            "turns — sampled at 2400 points."
        ),
        (
            "Diagnostics are exact and independent of the integrator's internal steps. The equilateral "
            "rigidity is the maximum over time of |d(t) − a|/a for all three pairwise distances. The "
            "rotation rate is measured by unwrapping the polar angle of beam 1 about the instantaneous "
            "centroid and fitting a straight line in time — the slope is the recorded rotation rate. "
            "The total energy (E5) and the angular momentum L_z are evaluated on ~300 uniformly spaced "
            "samples per run. The anti-phase run starts from the same triangle at rest and integrates "
            "to T = 40; the binary run launches two beams at (±1.5, 0) with transverse velocities "
            "∓0.15 and integrates to T = 80, both at the same tolerances."
        ),
        (
            "Every acceptance check is registered in the JSON protocol with its value, target, "
            "tolerance, unit and pass flag; the recorded full run passes 9/9. The --figures mode adds "
            "the scheme SVG and four 300-DPI PNG panels together with two parameter sweeps stored in "
            "the protocol: the side sweep (seven sides a = 2.0…8.0, each with a full re-integration "
            "over one rotation period and a fresh slope measurement) and the binary velocity sweep "
            "(sixteen launch velocities v_b = 0.06…0.34 over T = 40). No network access and no "
            "stochastic seeds are used; the run is bit-reproducible on the reference machine."
        ),
    ],
    "method_ru": [
        (
            "Модель — плоская система N тел с чередующейся раскладкой состояния "
            "[x₁, y₁, vx₁, vy₁, …]. В пресете U = w = m = 1 сторона треугольника a = 3, начальные "
            "позиции лежат на окружности r_c = a/√3 = 1.732051, а начальные скорости — поле жёсткого "
            "вращения ω·r_c с аналитической скоростью ω = √(3Ue^(−a/w)/(maw)) = 0.22313016014842985. "
            "Все прогоны интегрируют уравнения движения (E3) явной схемой Дормана–Принса 8(5,3) "
            "(scipy DOP853, rtol = atol = 1e-12, max_step = 0.1, плотный вывод для равномерной "
            "выборки). Вращательный прогон длится T = 3·2π/ω = 84.4778 — три полных оборота — и "
            "снимается в 2400 точек."
        ),
        (
            "Диагностика точна и не зависит от внутренних шагов интегратора. Равносторонняя жёсткость "
            "— это максимум по времени величины |d(t) − a|/a по всем трём парным расстояниям. "
            "Скорость вращения измеряется разворачиванием полярного угла пучка 1 относительно "
            "мгновенного центроида и подгонкой прямой по времени — наклон и есть записанная скорость "
            "вращения. Полная энергия (E5) и момент импульса L_z вычисляются на ~300 равномерно "
            "расставленных выборках каждого прогона. Противофазный прогон стартует из того же "
            "треугольника в покое и интегрируется до T = 40; бинарный прогон запускает два пучка в "
            "(±1.5, 0) с поперечными скоростями ∓0.15 и интегрируется до T = 80 — оба с теми же "
            "допусками."
        ),
        (
            "Каждая контрольная проверка регистрируется в JSON-протоколе со значением, целью, "
            "допуском, единицей и флагом прохождения; записанный полный прогон проходит 9/9. Режим "
            "--figures добавляет схему SVG и четыре PNG-панели 300 DPI вместе с двумя развёртками "
            "параметров, сохранёнными в протоколе: развёртка по стороне (семь сторон a = 2.0…8.0, "
            "каждая с полным повторным интегрированием на один период вращения и свежим измерением "
            "наклона) и развёртка бинарной пары по скорости (шестнадцать стартовых скоростей "
            "v_b = 0.06…0.34 за T = 40). Сетевой доступ и стохастические зёрна не используются; "
            "прогон бит-в-бит воспроизводим на референсной машине."
        ),
    ],
    "analysis_en": [
        (
            "**Rigid rotation.** Over three full turns (T = 84.4778) the triangle stays equilateral "
            "to 1.8e-08 in relative side deviation — a factor of about 56 inside the 1e-6 acceptance "
            "tolerance (fig02b). The measured rotation rate 0.223130160 reproduces the analytic "
            "ω = 0.223130160 to 1.1×10⁻¹¹ in absolute terms, versus a tolerance of 1e-8 — the "
            "central-configuration balance (E4) is not merely satisfied but satisfied at round-off "
            "level. The invariants confirm the cleanliness of the run: energy drift 4.7e-16 and "
            "angular-momentum drift 2.2e-15, both orders of magnitude below the 1e-10 gate."
        ),
        (
            "**Side sweep.** The rotation law is verified as a law, not a point: re-integrating one "
            "full period at each of the seven grid sides a = 2.0, 2.5, 3.0, 4.0, 5.0, 6.5, 8.0 "
            "reproduces the analytic curve everywhere — ω from 0.450558 at a = 2 through 0.313850 "
            "(a = 2.5), 0.223130 (a = 3), 0.117204 (a = 4), 0.063583 (a = 5), 0.026342 (a = 6.5) down "
            "to 0.011216 at a = 8. The Newtonian 1/r reference rotates systematically faster at large "
            "separations: 0.333333 against the Kerr 0.223130 at the preset, and 0.076547 against "
            "0.011216 at a = 8 — the exponential tail dies out, and the choreography slows down "
            "correspondingly (fig03a)."
        ),
        (
            "**Anti-phase expansion.** With all phases flipped, the same triangle at rest expands "
            "monotonically: the minimum pairwise distance never drops below 3.0000 (the initial "
            "value; the 0.95a = 2.85 floor is never approached), and the final separation reaches "
            "23.476 at T = 40 — a clean repulsive scattering event with energy conserved to 3.6e-16. "
            "This is the sign-flip control experiment: identical geometry, identical integrator, "
            "opposite outcome — the phase, not the geometry, decides the fate of the triplet."
        ),
        (
            "**Binary and bound/unbound map.** The in-phase binary with v_b = 0.15 breathes inside "
            "[0.635, 3.000] over the whole t = 80 window (fig04a) with energy drift 3.0e-12 — the "
            "largest of the three runs yet still a factor of about 33 below the 1e-10 tolerance. The "
            "velocity sweep turns the single trajectory into a map (fig03b): max separation stays at "
            "the initial 3.0 for all v_b ≤ 0.26 and jumps to 7.7515, 13.2491, 16.4935 and 19.1521 for "
            "v_b = 0.28–0.34 over T = 40. The analytic threshold v_b* = e^(−3/2) = 0.223130 sits "
            "inside the trapped band: the angular-momentum barrier keeps near-threshold launches "
            "bound for the whole observation window, so the numerically observed escape edge lies "
            "between 0.26 and 0.28 rather than exactly at v_b*."
        ),
    ],
    "analysis_ru": [
        (
            "**Жёсткое вращение.** За три полных оборота (T = 84.4778) треугольник остаётся "
            "равносторонним до 1.8e-08 относительного изменения стороны — примерно в 56 раз внутри "
            "допуска 1e-6 (fig02b). Измеренная скорость вращения 0.223130160 воспроизводит "
            "аналитическую ω = 0.223130160 с абсолютной точностью 1.1×10⁻¹¹ против допуска 1e-8 — "
            "баланс центральной конфигурации (E4) не просто выполнен, а выполнен на уровне машинного "
            "округления. Инварианты подтверждают чистоту прогона: дрейф энергии 4.7e-16 и дрейф "
            "момента импульса 2.2e-15, на порядки ниже рубежа 1e-10."
        ),
        (
            "**Развёртка по стороне.** Закон вращения верифицирован как закон, а не точка: повторное "
            "интегрирование одного полного периода на каждой из семи сторон сетки a = 2.0, 2.5, 3.0, "
            "4.0, 5.0, 6.5, 8.0 воспроизводит аналитическую кривую всюду — ω от 0.450558 при a = 2 "
            "через 0.313850 (a = 2.5), 0.223130 (a = 3), 0.117204 (a = 4), 0.063583 (a = 5), 0.026342 "
            "(a = 6.5) до 0.011216 при a = 8. Ньютоновская эталонная кривая 1/r вращается систематически "
            "быстрее на больших расстояниях: 0.333333 против керровских 0.223130 в пресете и 0.076547 "
            "против 0.011216 при a = 8 — экспоненциальный хвост вымирает, и хореография замедляется "
            "соответственно (fig03a)."
        ),
        (
            "**Противофазный разлёт.** При смене всех фаз тот же треугольник в покое разлетается "
            "монотонно: минимальное парное расстояние никогда не опускается ниже 3.0000 (начального "
            "значения; пол 0.95a = 2.85 не приближается ни разу), а конечное расстояние достигает "
            "23.476 при T = 40 — чистое отталкивающее событие рассеяния с сохранением энергии до "
            "3.6e-16. Это контрольный эксперимент по смене знака: та же геометрия, тот же "
            "интегратор, противоположный исход — судьбу триплета решает фаза, а не геометрия."
        ),
        (
            "**Бинарная пара и карта связанности.** Синфазная бинарная пара с v_b = 0.15 дышит внутри "
            "[0.635, 3.000] на всём окне t = 80 (fig04a) с дрейфом энергии 3.0e-12 — наибольшим из "
            "трёх прогонов, но всё ещё примерно в 33 раза ниже допуска 1e-10. Развёртка по скорости "
            "превращает единственную траекторию в карту (fig03b): максимальное расстояние остаётся на "
            "начальном 3.0 для всех v_b ≤ 0.26 и скачет к 7.7515, 13.2491, 16.4935 и 19.1521 при "
            "v_b = 0.28–0.34 за T = 40. Аналитический порог v_b* = e^(−3/2) = 0.223130 лежит внутри "
            "запертой полосы: центробежный барьер удерживает околопороговые запуски связанными всё "
            "время наблюдения, поэтому численно наблюдаемая граница убегания лежит между 0.26 и 0.28, "
            "а не ровно на v_b*."
        ),
    ],
    "discussion_en": [
        (
            "The model is deliberately minimal: point-like beams, an isotropic exponential pair force, "
            "no retardation, no absorption, and the optical phase entering only as the sign s = ±1 of "
            "each pair. Within these assumptions every statement in this study is an exact property of "
            "the governing equations rather than a simulation of a particular experiment. The "
            "particle approximation is the standard reduction for well-separated solitons; its "
            "breakdown at near-field overlap (where beams deform, fuse or shed radiation) is outside "
            "the conservative scope here, and the natural extensions — full NLS integration of the "
            "same triangle, saturating media, unequal beams, three-dimensional geometries — would "
            "each preserve the verification style established above."
        ),
        (
            "The parameter regime is chosen where the physics is clean. At the preset a = 3 the edge "
            "force is (U/w)e^(−3) = 0.049787 — weak, so the beams are well separated in units of the "
            "interaction scale and the particle picture is self-consistent — and the rotation is "
            "correspondingly slow, ω = 0.223130. The binary preset v_b = 0.15 sits at 67 % of the "
            "escape threshold 0.223130, comfortably inside the bound region but far enough from zero "
            "to give a visibly precessing orbit. The velocity sweep shows the interesting boundary "
            "structure: the escape edge observed numerically (between 0.26 and 0.28) lies above the "
            "two-body threshold 0.223130 because the centrifugal barrier temporarily traps "
            "marginally supercritical launches — a genuinely three-dimensional-in-time effect that a "
            "static energy argument alone would miss."
        ),
        (
            "Within the program, TRX-04 plays the role of the spatial optics bridge. Upstream, TRX-03 "
            "verifies the same molecular physics in the temporal domain of a fiber laser, where the "
            "force law carries an additional phase-cosine modulation; downstream, TRX-05 moves from "
            "field maxima to field zeros — optical vortices — and recovers Kirchhoff's vortex "
            "equations, while TRX-08 replaces photons by laser-cooled ions with a harmonic trap and "
            "Coulomb tail. Together with the celestial block (TRX-01, TRX-11) these studies show that "
            "the equilateral central configuration is a form, not an accident: it re-emerges in every "
            "medium whose two-body law is central, conservative and pair-additive, with only the "
            "rotation law changing."
        ),
    ],
    "discussion_ru": [
        (
            "Модель нарочито минимальна: точечные пучки, изотропная экспоненциальная парная сила, без "
            "запаздывания, без поглощения, а оптическая фаза входит только как знак s = ±1 каждой "
            "пары. В этих допущениях каждое утверждение данного исследования — точное свойство "
            "определяющих уравнений, а не симуляция конкретного эксперимента. Частичное приближение — "
            "стандартная редукция для хорошо разделённых солитонов; его разрушение при ближнеполевом "
            "перекрытии (где пучки деформируются, сливаются или сбрасывают излучение) остаётся вне "
            "консервативного охвата, а естественные расширения — полное интегрирование НУШ для того же "
            "треугольника, насыщающиеся среды, неравные пучки, трёхмерные геометрии — каждое сохранит "
            "установленный выше верификационный стиль."
        ),
        (
            "Диапазон параметров выбран там, где физика чиста. В пресете a = 3 краевая сила равна "
            "(U/w)e^(−3) = 0.049787 — слабая, поэтому пучки хорошо разделены в единицах масштаба "
            "взаимодействия и частичная картина самосогласованна, — а вращение соответственно "
            "медленное, ω = 0.223130. Пресет бинарной пары v_b = 0.15 составляет 67 % порога убегания "
            "0.223130 — с запасом внутри связанной области, но достаточно далеко от нуля, чтобы дать "
            "заметно прецессирующую орбиту. Развёртка по скорости обнаруживает интересную граничную "
            "структуру: численно наблюдаемая граница убегания (между 0.26 и 0.28) лежит выше "
            "двухтельного порога 0.223130, потому что центробежный барьер временно запирает "
            "маргинально закритические запуски — подлинно динамический эффект, который статический "
            "энергетический аргумент в одиночку пропустил бы."
        ),
        (
            "В рамках программы TRX-04 играет роль пространственно-оптического моста. Выше по течению "
            "TRX-03 верифицирует ту же молекулярную физику во временной области волоконного лазера, "
            "где закон силы несёт дополнительную фазово-косинусную модуляцию; ниже по течению TRX-05 "
            "переходит от максимумов поля к нулям поля — оптическим вихрям — и восстанавливает "
            "уравнения вихрей Кирхгофа, а TRX-08 меняет фотоны на лазерно-охлаждённые ионы с "
            "гармонической ловушкой и кулоновским хвостом. Вместе с небесным блоком (TRX-01, TRX-11) "
            "эти исследования показывают, что равносторонняя центральная конфигурация — форма, а не "
            "случайность: она возникает заново в каждой среде, чей двухтельный закон централен, "
            "консервативен и парно-аддитивен, и меняется только закон вращения."
        ),
    ],
    "conclusions_en": [
        "The equilateral beam triangle is a genuine optical central configuration: it rotates rigidly over three full turns (T = 84.4778) with the side staying equilateral to 1.8e-08, versus the 1e-6 acceptance gate.",
        "The measured rotation rate 0.223130160 reproduces the analytic Lagrange law ω² = 3Ue^(−a/w)/(maw) (ω = e^(−3/2) = 0.223130160 at the preset) to 1.1×10⁻¹¹ — the balance is confirmed at round-off level.",
        "The rotation law is verified as a law across the side sweep a = 2.0…8.0: numeric re-runs sit on the analytic curve at all seven sides (ω from 0.450558 down to 0.011216), while the Newtonian 1/r reference decays markedly slower (0.076547 at a = 8).",
        "Invariants are conserved at machine level in all runs: energy drift 4.7e-16 (rotation), 3.6e-16 (anti-phase trio), 3.0e-12 (binary), angular-momentum drift 2.2e-15 — all below the 1e-10 tolerance.",
        "The phase sign controls the outcome: the anti-phase trio never collapses (min pairwise distance 3.0000 ≥ 0.95a) and expands to 23.476, while the in-phase binary with E_rel = −0.027 stays bound with its separation inside [0.635, 3.000] over t = 80.",
        "The bound/unbound map is established: max separation stays 3.0 for v_b ≤ 0.26 and escape follows for v_b = 0.28–0.34 (7.7515 → 19.1521 over T = 40); the observed escape edge lies above the two-body threshold v_b* = e^(−3/2) = 0.223130 because the centrifugal barrier temporarily traps near-threshold launches.",
    ],
    "conclusions_ru": [
        "Равносторонний треугольник пучков — подлинная оптическая центральная конфигурация: он жёстко вращается три полных оборота (T = 84.4778) со стороной, остающейся равносторонней до 1.8e-08 против рубежа 1e-6.",
        "Измеренная скорость вращения 0.223130160 воспроизводит аналитический лагранжев закон ω² = 3Ue^(−a/w)/(maw) (ω = e^(−3/2) = 0.223130160 в пресете) с точностью 1.1×10⁻¹¹ — баланс подтверждён на уровне машинного округления.",
        "Закон вращения верифицирован как закон на развёртке по сторонам a = 2.0…8.0: численные повторные прогоны ложатся на аналитическую кривую во всех семи точках (ω от 0.450558 до 0.011216), а ньютоновская эталонная кривая 1/r спадает заметно медленнее (0.076547 при a = 8).",
        "Инварианты сохраняются на машинном уровне во всех прогонах: дрейф энергии 4.7e-16 (вращение), 3.6e-16 (противофазное трио), 3.0e-12 (бинарная пара), дрейф момента импульса 2.2e-15 — всё ниже допуска 1e-10.",
        "Знак фазы решает исход: противофазное трио никогда не коллапсирует (мин. парное расстояние 3.0000 ≥ 0.95a) и разлетается до 23.476, а синфазная бинарная пара с E_rel = −0.027 остаётся связанной с расстоянием внутри [0.635, 3.000] на протяжении t = 80.",
        "Карта связанности построена: максимальное расстояние остаётся 3.0 при v_b ≤ 0.26, а убегание наступает при v_b = 0.28–0.34 (7.7515 → 19.1521 за T = 40); наблюдаемая граница убегания лежит выше двухтельного порога v_b* = e^(−3/2) = 0.223130, поскольку центробежный барьер временно запирает околопороговые запуски.",
    ],
    "references": [
        "1. Chiao, R. Y., Garmire, E., Townes, C. H. (1964). *Self-trapping of optical beams.* Phys. Rev. Lett. 13, 479–482.",
        "2. Snyder, A. W., Mitchell, D. J., Kivshar, Y. S. (1995). *Unification of self-trapping of light and matter waves.* Phys. Rev. E 51, 3061–3066.",
        "3. Stegeman, G. I., Segev, M. (1999). *Optical spatial solitons and their interactions.* Science 286, 1518–1523.",
        "4. Reynaud, F., Barthelemy, A. (1990). *Optically controlled interaction between two fundamental soliton beams.* Europhys. Lett. 12, 401–405.",
        "5. Aitchison, J. S., Weiner, A. M., Silberberg, Y., Oliver, M. K., Jackel, J. L., Leaird, D. E., Vogel, E. M., Smith, P. W. E. (1991). *Experimental observation of spatial soliton interactions.* Opt. Lett. 16, 15–17.",
        "6. Assanto, G., Peccianti, M. (2012). *Nematicons: spatial optical solitons in nematic liquid crystals.* Phys. Rep. 516, 147–208.",
        "7. Carusotto, I., Ciuti, C. (2013). *Quantum fluids of light.* Rev. Mod. Phys. 85, 291–315.",
        "8. Bialynicki-Birula, I. (2006). *Photon waves.* Acta Phys. Pol. A 109, 20–32.",
        "9. Lagrange, J.-L. (1772). *Essai sur le problème des trois corps.* In: Œuvres de Lagrange, Vol. 6. Gauthier-Villars, Paris (1873).",
    ],
    "crosslinks_en": [
        "* **TRX-03** is the 1-D fiber-laser version of the same molecular physics: temporal solitons with a phase-cosine force law and a breathing bound state.",
        "* **TRX-05** replaces the field maxima by field *zeros* (optical vortices) and recovers Kirchhoff's vortex equations — the same triangle with circulations instead of phases.",
        "* **TRX-08** trades photons for ions — the trap harmonic force plus the Coulomb tail, with the same central-configuration and invariant bookkeeping.",
    ],
    "crosslinks_ru": [
        "* **TRX-03** — одномерная волоконно-лазерная версия той же молекулярной физики: временные солитоны с фазово-косинусным законом силы и дышащим связанным состоянием.",
        "* **TRX-05** заменяет максимумы поля *нулями* поля (оптические вихри) и восстанавливает уравнения Кирхгофа — тот же треугольник с циркуляциями вместо фаз.",
        "* **TRX-08** меняет фотоны на ионы — гармоническая сила ловушки плюс кулоновский хвост с тем же учётом центральных конфигураций и инвариантов.",
    ],
    "assumptions_en": [
        "Particle approximation: each beam is a point body in the transverse plane; its transverse profile is assumed rigid (fundamental solitons, no deformation or radiation shedding).",
        "The pair force is the isotropic exponential law ∓(U/w)e^(−r/w) — conservative and instantaneous; retardation, absorption and medium dynamics are neglected.",
        "Planar 2-D model: all motion is in the transverse plane; propagation along z is uniform and does not couple back into the dynamics.",
        "Equal members: identical potential depth U, interaction scale w and mass m for all beams; the optical phase enters only as the pair sign s = ±1 (fixed in phase or anti-phase, not a dynamical variable).",
        "The focusing NLS (E1) is documented context; the dynamics are integrated at the particle level, and the particle approximation is assumed valid for well-separated beams (r ≳ 2w).",
        "Integrator precision: DOP853 with rtol = atol = 1e-12 and max_step = 0.1; conservation errors reported are those of the recorded runs on the reference machine.",
    ],
    "assumptions_ru": [
        "Частичное приближение: каждый пучок — точечное тело в поперечной плоскости; его поперечный профиль считается жёстким (фундаментальные солитоны, без деформации и сброса излучения).",
        "Парная сила — изотропный экспоненциальный закон ∓(U/w)e^(−r/w): консервативная и мгновенная; запаздывание, поглощение и динамика среды не учитываются.",
        "Плоская 2-D модель: всё движение происходит в поперечной плоскости; распространение вдоль z однородно и не возвращается в динамику.",
        "Равные участники: одинаковые глубина потенциала U, масштаб взаимодействия w и масса m у всех пучков; оптическая фаза входит только как знак пары s = ±1 (фиксированные синфазность или противофазность, не динамическая переменная).",
        "Фокусирующее НУШ (E1) — документированный контекст; динамика интегрируется на частичном уровне, и частичное приближение считается справедливым для хорошо разделённых пучков (r ≳ 2w).",
        "Точность интегратора: DOP853 с rtol = atol = 1e-12 и max_step = 0.1; приведённые ошибки сохранения — ошибки записанных прогонов на референсной машине.",
    ],
    "glance_en": [
        ["Block", "Laser optics — study 04 of 12"],
        [
            "Model",
            "three spatial Kerr solitons with phase-signed exponential pair force (U = w = m = 1)",
        ],
        ["Key invariant", "total energy of all three runs (drift ≤ 3.0e-12; rotation 4.7e-16)"],
        [
            "Headline result",
            "rigid rotation of the beam triangle at ω = 0.223130160 vs analytic to 1.1×10⁻¹¹; rigidity 1.8e-08",
        ],
        ["Verification", "9/9 checks PASS (full mode)"],
        ["Runtime", "9.4 s recorded full run (with --figures) · smoke < 20 s"],
    ],
    "glance_ru": [
        ["Блок", "Лазерная оптика — исследование 04 из 12"],
        [
            "Модель",
            "три пространственных керровских солитона с экспоненциальной парной силой, подписанной фазой (U = w = m = 1)",
        ],
        [
            "Ключевой инвариант",
            "полная энергия всех трёх прогонов (дрейф ≤ 3.0e-12; вращение 4.7e-16)",
        ],
        [
            "Главный результат",
            "жёсткое вращение треугольника пучков с ω = 0.223130160 против аналитики до 1.1×10⁻¹¹; жёсткость 1.8e-08",
        ],
        ["Верификация", "9/9 проверок PASS (полный режим)"],
        ["Время выполнения", "9.4 с записанный полный прогон (с --figures) · smoke < 20 с"],
    ],
    "glossary": {
        "header_en": ["Term", "Definition"],
        "header_ru": ["Термин", "Определение"],
        "rows_en": [
            [
                "Photon fluid",
                "an ensemble of light beams behaving as a gas of mutually interacting particles with tunable two-body forces",
            ],
            [
                "Spatial soliton",
                "a beam that propagates in a focusing nonlinear medium without diffracting, carrying its own waveguide",
            ],
            [
                "Kerr nonlinearity",
                "refractive-index change proportional to intensity; the field equation is the focusing NLS (E1)",
            ],
            [
                "Relative phase",
                "the optical phase difference between beams: in phase attracts, anti-phase repels",
            ],
            [
                "Particle approximation",
                "reduction of well-separated beams to point bodies with pair forces",
            ],
            [
                "Central configuration",
                "positions where the net force on each body points at the centroid proportional to its radius; the equilateral triangle is one",
            ],
            [
                "Lagrange triangle",
                "the rigidly rotating equilateral three-body solution found in 1772; here its optical realization",
            ],
            [
                "Binary",
                "a bound in-phase pair whose separation oscillates between turning points while the orbit precesses",
            ],
            [
                "Escape threshold v_b*",
                "launch velocity separating bound from unbound pair orbits; here √(Ue^(−r₀/w)) = e^(−3/2) = 0.223130",
            ],
            [
                "Beam-waist unit w",
                "the exponential interaction scale; the length unit of the study",
            ],
        ],
        "rows_ru": [
            [
                "Фотонная жидкость",
                "ансамбль световых пучков, ведущий себя как газ взаимно взаимодействующих частиц с настраиваемыми двухтельными силами",
            ],
            [
                "Пространственный солитон",
                "пучок, распространяющийся в фокусирующей нелинейной среде без дифракционного расплывания и несущий собственный волновод",
            ],
            [
                "Керровская нелинейность",
                "изменение показателя преломления, пропорциональное интенсивности; полевое уравнение — фокусирующее НУШ (E1)",
            ],
            [
                "Относительная фаза",
                "оптическая разность фаз между пучками: синфазность притягивает, противофазность отталкивает",
            ],
            [
                "Частичное приближение",
                "редукция хорошо разделённых пучков к точечным телам с парными силами",
            ],
            [
                "Центральная конфигурация",
                "позиции, в которых равнодействующая на каждое тело указывает в центроид пропорционально радиусу; равносторонний треугольник — одна из них",
            ],
            [
                "Лагранжев треугольник",
                "жёстко вращающееся равностороннее трёхтельное решение, найденное в 1772 году; здесь его оптическая реализация",
            ],
            [
                "Бинарная пара",
                "связанная синфазная пара, расстояние в которой колеблется между поворотными точками при прецессии орбиты",
            ],
            [
                "Порог убегания v_b*",
                "стартовая скорость, разделяющая связанные и несвязанные орбиты пары; здесь √(Ue^(−r₀/w)) = e^(−3/2) = 0.223130",
            ],
            [
                "Единица перетяжки w",
                "экспоненциальный масштаб взаимодействия; единица длины исследования",
            ],
        ],
    },
    "notation": {
        "header_en": ["Symbol", "Meaning"],
        "header_ru": ["Символ", "Смысл"],
        "rows_en": [
            [
                "A",
                "slowly varying beam envelope; A_z, ∇²⊥ are the z-derivative and transverse Laplacian",
            ],
            [
                "U, w, m",
                "potential depth, interaction scale (beam-waist unit) and soliton mass; all 1 at the preset",
            ],
            ["s", "pair sign: −1 in phase (attraction), +1 anti-phase (repulsion)"],
            ["r, r_kl", "pair separation between beams k and l"],
            ["a, r_c", "triangle side and centroid orbit radius a/√3"],
            ["ω", "rotation rate of the rigid triangle; ω² = 3Ue^(−a/w)/(maw)"],
            ["v_b", "binary transverse launch velocity (preset 0.15)"],
            ["E_rel", "relative energy of the binary pair, m·v_b² − Ue^(−r₀/w)"],
            ["E, L_z", "total energy and angular momentum, the conserved invariants (E5)"],
            ["T", "duration of a run (rotation 84.4778; anti-phase 40; binary 80)"],
            ["V_pm, V_ap", "in-phase and anti-phase pair potentials (E2)"],
        ],
        "rows_ru": [
            [
                "A",
                "медленно меняющаяся огибающая пучка; A_z, ∇²⊥ — производная по z и поперечный лапласиан",
            ],
            [
                "U, w, m",
                "глубина потенциала, масштаб взаимодействия (единица перетяжки) и масса солитона; в пресете все равны 1",
            ],
            ["s", "знак пары: −1 синфазно (притяжение), +1 в противофазе (отталкивание)"],
            ["r, r_kl", "парное расстояние между пучками k и l"],
            ["a, r_c", "сторона треугольника и радиус орбиты вокруг центроида a/√3"],
            ["ω", "скорость вращения жёсткого треугольника; ω² = 3Ue^(−a/w)/(maw)"],
            ["v_b", "поперечная стартовая скорость бинарной пары (пресет 0.15)"],
            ["E_rel", "относительная энергия бинарной пары, m·v_b² − Ue^(−r₀/w)"],
            ["E, L_z", "полная энергия и момент импульса — сохраняющиеся инварианты (E5)"],
            ["T", "длительность прогона (вращение 84.4778; противофаза 40; бинарная пара 80)"],
            ["V_pm, V_ap", "синфазный и противофазный парные потенциалы (E2)"],
        ],
    },
    "params_appendix": {
        "header_en": ["Symbol", "Value", "Role"],
        "header_ru": ["Символ", "Значение", "Роль"],
        "rows_en": [
            ["U, w, m", "1, 1, 1", "natural units: energy, length, mass"],
            ["a", "3", "triangle side; operating point of the rotation run"],
            ["r_c", "a/√3 = 1.732051", "beam orbit radius about the centroid"],
            ["(U/w)e^(−a/w)", "0.049787", "edge force at the operating point (= ω²)"],
            ["ω", "e^(−3/2) = 0.22313016014842985", "analytic rotation rate at the preset"],
            ["T_rotation", "84.4778", "rotation run: three full turns, 2400 samples"],
            ["anti-phase run", "same triangle at rest, T = 40", "repulsive expansion control"],
            [
                "binary preset",
                "r₀ = 3, v_b = ±0.15, E_rel = −0.027, T = 80",
                "in-phase bound-pair run",
            ],
            ["v_b*", "e^(−3/2) = 0.223130", "analytic escape threshold of the binary"],
            [
                "velocity sweep",
                "16 launches, v_b = 0.06…0.34, T = 40",
                "bound/unbound map of fig03b",
            ],
            ["integrator", "DOP853, rtol = atol = 1e-12, max_step = 0.1", "all runs, dense output"],
        ],
        "rows_ru": [
            ["U, w, m", "1, 1, 1", "естественные единицы: энергия, длина, масса"],
            ["a", "3", "сторона треугольника; рабочая точка вращательного прогона"],
            ["r_c", "a/√3 = 1.732051", "радиус орбиты пучков вокруг центроида"],
            ["(U/w)e^(−a/w)", "0.049787", "краевая сила в рабочей точке (= ω²)"],
            ["ω", "e^(−3/2) = 0.22313016014842985", "аналитическая скорость вращения в пресете"],
            ["T_rotation", "84.4778", "вращательный прогон: три полных оборота, 2400 выборок"],
            [
                "противофазный прогон",
                "тот же треугольник в покое, T = 40",
                "контроль отталкивающего разлёта",
            ],
            [
                "пресет бинарной пары",
                "r₀ = 3, v_b = ±0.15, E_rel = −0.027, T = 80",
                "прогон синфазной связанной пары",
            ],
            ["v_b*", "e^(−3/2) = 0.223130", "аналитический порог убегания бинарной пары"],
            [
                "развёртка по скорости",
                "16 запусков, v_b = 0.06…0.34, T = 40",
                "карта связанности fig03b",
            ],
            [
                "интегратор",
                "DOP853, rtol = atol = 1e-12, max_step = 0.1",
                "все прогоны, плотный вывод",
            ],
        ],
    },
    "bibtex": [
        "@article{chiao1964,",
        "  author  = {Chiao, R. Y. and Garmire, E. and Townes, C. H.},",
        "  title   = {Self-trapping of optical beams},",
        "  journal = {Physical Review Letters},",
        "  year    = {1964}, volume = {13}, pages = {479--482}}",
        "",
        "@article{snyder1995,",
        "  author  = {Snyder, A. W. and Mitchell, D. J. and Kivshar, Y. S.},",
        "  title   = {Unification of self-trapping of light and matter waves},",
        "  journal = {Physical Review E},",
        "  year    = {1995}, volume = {51}, pages = {3061--3066}}",
        "",
        "@article{aitchison1991,",
        "  author  = {Aitchison, J. S. and Weiner, A. M. and Silberberg, Y. and Oliver, M. K. and Jackel, J. L. and Leaird, D. E. and Vogel, E. M. and Smith, P. W. E.},",
        "  title   = {Experimental observation of spatial soliton interactions},",
        "  journal = {Optics Letters},",
        "  year    = {1991}, volume = {16}, pages = {15--17}}",
        "",
        "@article{carusotto2013,",
        "  author  = {Carusotto, Iacopo and Ciuti, Cristiano},",
        "  title   = {Quantum fluids of light},",
        "  journal = {Reviews of Modern Physics},",
        "  year    = {2013}, volume = {85}, pages = {291--315}}",
        "",
        "@misc{lagrange1772,",
        "  author  = {Lagrange, Joseph-Louis},",
        "  title   = {Essai sur le probl{\\`e}me des trois corps},",
        "  year    = {1772},",
        "  note    = {In: Œuvres de Lagrange, Vol. 6, Gauthier-Villars, Paris, 1873}}",
    ],
}
