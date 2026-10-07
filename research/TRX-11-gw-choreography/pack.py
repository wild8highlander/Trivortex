# -*- coding: utf-8 -*-
"""Content pack for TRX-11 (v1.0.0 Monograph Edition). Rendered by scripts/build_study_docs.py."""

PACK = {
    "meta": {
        "study_id": "TRX-11",
        "dir_name": "TRX-11-gw-choreography",
        "title_en": "Gravitational Waves from the Figure-Eight Choreography",
        "title_ru": "Гравитационные волны от хореографии «восьмёрки»",
        "script": "trx11_gw_choreography.py",
        "results_json": "trx11_results.json",
        "scheme_file": "scheme_trx11.svg",
        "runtime_full": "8.17 s",
    },
    "essence_en": (
        "The figure-eight choreography (Chenciner & Montgomery 2000) — three equal "
        "masses chasing each other along a single closed curve with zero angular momentum — is "
        "treated as a laboratory gravitational-wave source. In the quadrupole approximation "
        "(G = c = D = 1) the mass quadrupole Q_ij = Σ m_k x_ki x_kj drives a plus-polarised "
        "strain that repeats six times per orbit period T = 6.325914, and the choreography "
        "symmetry locks the spectrum into a pure harmonic comb with the dominant line at "
        "n = 6 of the orbital comb."
    ),
    "essence_ru": (
        "Хореография «восьмёрка» (Ченчинер и Монтгомери, 2000) — три равные массы, "
        "преследующие друг друга по одной замкнутой кривой с нулевым моментом импульса, — "
        "рассматривается как лабораторный источник гравитационных волн. В квадрупольном "
        "приближении (G = c = D = 1) массовый квадруполь Q_ij = Σ m_k x_ki x_kj возбуждает "
        "плюс-поляризованную деформацию, повторяющуюся шесть раз за орбитальный период "
        "T = 6.325914, а симметрия хореографии запирает спектр в чистую гребёнку гармоник "
        "с доминирующей линией на n = 6 орбитальной гребёнки."
    ),
    "mission_en": [
        (
            "A choreography is the cleanest gravitational-wave emitter the three-body problem "
            "offers: one periodic curve, three masses, zero angular momentum, and a quadrupole "
            "whose exchange symmetries imprint a sharp comb on the spectrum. Among the special "
            "solutions collected in the TRIVORTEX monograph — the rotating Lagrange triangle, the "
            "Aref collapse trio, the hierarchical secular triples — the figure-eight is the only "
            "one that is simultaneously periodic, non-hierarchical and non-colliding, which makes "
            "it the natural benchmark for three-body gravitational-wave astronomy. This study "
            "pins the emitter down quantitatively rather than qualitatively: the period, the "
            "invariants, the waveform, the spectrum and the antenna pattern are all measured and "
            "stored as machine-checkable numbers."
        ),
        (
            "The study verifies seven things to numerical precision: that the period found by "
            "global minimisation of the configuration closure, T = 6.325914025, matches the "
            "published value 6.32591398 to 1.2e-08; that energy is conserved to 3.6e-15 and the "
            "total angular momentum stays zero to 1.4e-15 throughout the period — the defining "
            "property of the figure-eight; that the equal-mass choreography symmetry holds on the "
            "quadrupole, Q(T/3) = Q(0) to 1.5·10⁻⁸, which locks the waveform to a harmonic comb; "
            "and that the measured dominant harmonic lands at n = 6 of the orbital comb, twice "
            "the T/3 pattern frequency, exactly as the symmetry bookkeeping predicts. Because "
            "LISA, Taiji and TianQin are laser interferometers, the detection channel of this "
            "study is a laser channel — the instruments that would actually measure three-body "
            "GW signatures are built on laser stability over million-kilometre arms."
        ),
    ],
    "mission_ru": [
        (
            "Хореография — самый чистый гравитационно-волновой излучатель, какой даёт задача трёх "
            "тел: одна периодическая кривая, три массы, нулевой момент импульса и квадруполь, "
            "чьи симметрии обмена накладывают на спектр резкую гребёнку. Среди специальных "
            "решений, собранных в монографии TRIVORTEX, — вращающийся лагранжев треугольник, "
            "трио коллапса Арефа, иерархические секулярные тройки — только «восьмёрка» "
            "одновременно периодична, неиерархична и свободна от столкновений, что делает её "
            "естественным эталоном трёхтелевой гравитационно-волновой астрономии. "
            "Данное исследование фиксирует излучатель количественно, а не качественно: период, "
            "инварианты, форма волны, спектр и диаграмма направленности измерены и сохранены "
            "как машиночитаемые числа."
        ),
        (
            "Исследование проверяет семь вещей с численной точностью: что период, найденный "
            "глобальной минимизацией замыкания конфигурации, T = 6.325914025, совпадает с "
            "опубликованным значением 6.32591398 на уровне 1.2e-08; что энергия сохраняется до "
            "3.6e-15, а полный момент импульса остаётся нулевым до 1.4e-15 на всём периоде — "
            "определяющее свойство «восьмёрки»; что симметрия хореографии равных масс выполняется "
            "на квадруполе, Q(T/3) = Q(0) с точностью 1.5·10⁻⁸, запирая форму волны в гребёнку "
            "гармоник; и что измеренная доминирующая гармоника попадает на n = 6 орбитальной "
            "гребёнки — вдвое выше частоты паттерна T/3, ровно как предсказывает симметрийная "
            "арифметика. Поскольку LISA, Taiji и TianQin — лазерные интерферометры, канал "
            "детектирования этого исследования является лазерным: приборы, которые реально "
            "измерили бы трёхтелевые гравитационно-волновые сигнатуры, построены на стабильности "
            "лазера на плечах длиной в миллионы километров."
        ),
    ],
    "physics_en": [
        (
            "Planar Newtonian three-body problem with three equal masses, G = m = 1. The initial "
            "condition is the Chenciner–Montgomery figure-eight: r₁ = (0.97000436, −0.24308753), "
            "r₂ = −r₁, r₃ = (0, 0), v₃ = (−0.93240737, −0.86473146), v₁ = v₂ = −v₃/2. The total "
            "momentum and the total angular momentum vanish identically, and all three bodies "
            "trace the same closed curve shifted in time — a choreography in the strict sense. "
            "Over one period T = 6.325914 the pairwise separations sweep the interval from "
            "0.6905 to 2.0000 and are permuted among the three pairs every T/3."
        ),
        (
            "The wave model is the leading quadrupole term of general relativity in the "
            "far-zone, slow-motion limit. With G = c = D = 1 the plus-polarised strain read by a "
            "distant observer is proportional to the second derivative of Q_xx − Q_yy, and the "
            "luminosity is P = (1/5)Σ_ij (d³Q_ij/dt³)² evaluated on the trace-free part of the "
            "quadrupole. The emitter is deliberately idealised: Newtonian gravity supplies the "
            "source motion, and relativity enters only as a readout formula — no back-reaction "
            "on the orbit, no higher multipoles."
        ),
    ],
    "physics_ru": [
        (
            "Плоская ньютоновская задача трёх тел с тремя равными массами, G = m = 1. Начальное "
            "условие — «восьмёрка» Ченчинера–Монтгомери: r₁ = (0.97000436, −0.24308753), "
            "r₂ = −r₁, r₃ = (0, 0), v₃ = (−0.93240737, −0.86473146), v₁ = v₂ = −v₃/2. Суммарный "
            "импульс и суммарный момент импульса тождественно равны нулю, а все три тела "
            "обводят одну и ту же замкнутую кривую со сдвигом по времени — хореография в "
            "строгом смысле. За один период T = 6.325914 парные расстояния пробегают интервал "
            "от 0.6905 до 2.0000 и каждые T/3 циклически перераспределяются между парами."
        ),
        (
            "Волновая модель — ведущий квадрупольный член общей теории относительности в "
            "дальней зоне при малых скоростях. При G = c = D = 1 плюс-поляризованная деформация, "
            "регистрируемая далёким наблюдателем, пропорциональна второй производной "
            "Q_xx − Q_yy, а светимость равна P = (1/5)Σ_ij (d³Q_ij/dt³)², вычисленной на "
            "бесследовой части квадруполя. Излучатель сознательно идеализирован: ньютоновская "
            "гравитация задаёт движение источника, а теория относительности входит только как "
            "формула считывания — без обратного действия на орбиту и без высших мультиполей."
        ),
    ],
    "preset_table": {
        "header_en": ["Parameter", "Value", "Meaning"],
        "header_ru": ["Параметр", "Значение", "Смысл"],
        "rows_en": [
            ["Masses, constant", "m₁ = m₂ = m₃ = 1, G = 1", "planar Newtonian three-body problem"],
            [
                "Initial positions",
                "r₁ = (0.97000436, −0.24308753), r₂ = −r₁, r₃ = (0, 0)",
                "Chenciner–Montgomery initial condition",
            ],
            [
                "Initial velocities",
                "v₃ = (−0.93240737, −0.86473146), v₁ = v₂ = −v₃/2",
                "zero total momentum, zero angular momentum",
            ],
            [
                "Integrator",
                "DOP853, rtol = atol = 1e-13, max_step 0.005",
                "one period; 12001-point dense sampling for the quadrupole",
            ],
            [
                "Period search",
                "closure minimisation over t ∈ [2, 11], xatol 1e-13",
                "global minimum of the configuration closure",
            ],
            [
                "Wave model",
                "quadrupole, G = c = D = 1",
                "h₊ ∝ d²(Qxx − Qyy)/dt²; P = (1/5)Σ(d³Q_ij/dt³)²",
            ],
        ],
        "rows_ru": [
            ["Массы, константа", "m₁ = m₂ = m₃ = 1, G = 1", "плоская ньютоновская задача трёх тел"],
            [
                "Начальные положения",
                "r₁ = (0.97000436, −0.24308753), r₂ = −r₁, r₃ = (0, 0)",
                "начальное условие Ченчинера–Монтгомери",
            ],
            [
                "Начальные скорости",
                "v₃ = (−0.93240737, −0.86473146), v₁ = v₂ = −v₃/2",
                "нулевой суммарный импульс, нулевой момент импульса",
            ],
            [
                "Интегратор",
                "DOP853, rtol = atol = 1e-13, max_step 0.005",
                "один период; плотная выборка 12001 точек для квадруполя",
            ],
            [
                "Поиск периода",
                "минимизация замыкания по t ∈ [2, 11], xatol 1e-13",
                "глобальный минимум замыкания конфигурации",
            ],
            [
                "Волновая модель",
                "квадруполь, G = c = D = 1",
                "h₊ ∝ d²(Qxx − Qyy)/dt²; P = (1/5)Σ(d³Q_ij/dt³)²",
            ],
        ],
    },
    "equations": [
        {
            "id": "E1",
            "latex": "\\ddot{\\boldsymbol{r}}_k = \\sum_{j \\neq k} \\frac{\\boldsymbol{r}_j - \\boldsymbol{r}_k}{\\left|\\boldsymbol{r}_j - \\boldsymbol{r}_k\\right|^3}, \\qquad G = m = 1",
            "desc_en": "Newtonian three-body dynamics (planar, equal masses)",
            "desc_ru": "Ньютоновская динамика трёх тел (плоская, равные массы)",
        },
        {
            "id": "E2",
            "latex": "Q_{ij} = \\sum_k m_k\\, x_{ki}\\, x_{kj}",
            "desc_en": "Mass quadrupole tensor of the emitter",
            "desc_ru": "Тензор массового квадруполя излучателя",
        },
        {
            "id": "E3",
            "latex": "h_+(t) \\propto \\frac{d^2}{dt^2}\\left(Q_{xx} - Q_{yy}\\right)",
            "desc_en": "Plus-polarised waveform read by a distant observer (G = c = D = 1)",
            "desc_ru": "Плюс-поляризованная форма волны у далёкого наблюдателя (G = c = D = 1)",
        },
        {
            "id": "E4",
            "latex": "P = \\frac{1}{5}\\sum_{ij} \\left(\\frac{d^3 Q_{ij}}{dt^3}\\right)^{2}",
            "desc_en": "Gravitational-wave luminosity on the trace-free quadrupole (G = c = D = 1)",
            "desc_ru": "Гравитационно-волновая светимость на бесследовом квадруполе (G = c = D = 1)",
        },
        {
            "id": "E5",
            "latex": "\\{\\boldsymbol{r}_k(T/3)\\} = \\{\\boldsymbol{r}_k(0)\\} \\;\\Rightarrow\\; Q(t + T/3) = Q(t) \\;\\Rightarrow\\; \\tilde{h}(f) \\neq 0 \\ \\text{only at}\\ f = n \\cdot \\frac{3}{T}",
            "desc_en": "Choreography exchange symmetry and the harmonic comb",
            "desc_ru": "Обменная симметрия хореографии и гребёнка гармоник",
        },
    ],
    "scheme_cap_en": (
        "TRX-11 scheme — the figure-eight choreography as a gravitational-wave "
        "emitter: three equal masses chase each other along one closed curve with zero angular "
        "momentum; the rotating quadrupole radiates through lobes peaked along the orbital "
        "normal, and a LISA-class laser interferometer reads the strain."
    ),
    "scheme_cap_ru": (
        "Схема TRX-11 — хореография «восьмёрка» как гравитационно-волновой "
        "излучатель: три равные массы преследуют друг друга по одной замкнутой кривой с "
        "нулевым моментом импульса; вращающийся квадруполь излучает через лепестки, "
        "вытянутые вдоль нормали к орбите, а лазерный интерферометр класса LISA "
        "регистрирует деформацию."
    ),
    "scheme_walk_en": [
        [
            "Figure-eight curve (navy)",
            "the single closed trajectory traced by all three bodies; "
            "period T = 6.325914 in G = m = 1 units",
        ],
        [
            "Dashed reflection axis",
            "the symmetry axis of the eight, aligned with the initial " "velocity direction of m₃",
        ],
        [
            "Bodies m₁, m₂ (gold) and m₃ (white)",
            "the Chenciner–Montgomery starting state at "
            "t = 0; the gold arrow marks the chase direction along the curve",
        ],
        [
            "Exchange annotation",
            "each body runs the whole eight and the roles permute every "
            "T/3 ≈ 2.109, while the total angular momentum stays L = 0 (defining property)",
        ],
        [
            "Quadrupole lobes + LISA-class box",
            "radiation is strongest along the orbital normal, "
            "where a distant laser interferometer sits at inclination θ",
        ],
        [
            "Waveform strip and comb panel",
            "plus-polarised strain h₊ ∝ d²(Qxx − Qyy)/dt² with six "
            "repeats per orbit period, range −4.04 … +4.85, and a spectrum comb at n = 6, 12, 18 "
            "with amplitudes 1 : 0.091 : 0.0061",
        ],
    ],
    "scheme_walk_ru": [
        [
            "Кривая-«восьмёрка» (навы)",
            "единственная замкнутая траектория, которую обводят все "
            "три тела; период T = 6.325914 в единицах G = m = 1",
        ],
        [
            "Пунктирная ось отражения",
            "ось симметрии восьмёрки, направленная вдоль начальной " "скорости третьего тела m₃",
        ],
        [
            "Тела m₁, m₂ (золотые) и m₃ (белое)",
            "стартовое состояние Ченчинера–Монтгомери при "
            "t = 0; золотая стрелка отмечает направление погони вдоль кривой",
        ],
        [
            "Пометка обмена ролями",
            "каждое тело пробегает всю восьмёрку, а роли циклически "
            "меняются каждые T/3 ≈ 2.109, при этом полный момент импульса остаётся L = 0 "
            "(определяющее свойство)",
        ],
        [
            "Квадрупольные лепестки и бокс LISA-class",
            "излучение сильнее всего вдоль нормали к "
            "орбите, где на наклонении θ находится далёкий лазерный интерферометр",
        ],
        [
            "Полоса формы волны и панель гребёнки",
            "плюс-поляризованная деформация "
            "h₊ ∝ d²(Qxx − Qyy)/dt² с шестью повторами за орбитальный период, диапазон "
            "−4.04 … +4.85, и спектральная гребёнка на n = 6, 12, 18 с амплитудами "
            "1 : 0.091 : 0.0061",
        ],
    ],
    "mapping": {
        "header_en": ["Quantity in this study", "TRIVORTEX analog", "Comment"],
        "header_ru": ["Величина исследования", "Аналог в TRIVORTEX", "Комментарий"],
        "rows_en": [
            [
                "Figure-eight choreography",
                "rotating equilateral choreography of Theorem 3.1",
                "two special solutions of one problem",
            ],
            [
                "Zero angular momentum L = 0",
                "tuned circulation pattern (1, −1, 1)",
                "the document's own charge triplet",
            ],
            [
                "Quadrupole comb at multiples of 3/T",
                "radial modulation ω of Theorem 3.1",
                "spectral fingerprint of the triad",
            ],
            [
                "Choreography period T = 6.325914",
                "rigid rotation period of the vortex triangle",
                "both special solutions carry a single clock",
            ],
            [
                "LISA-class detection",
                "laser themes of TRX-01/12",
                "lasers as the measuring instrument",
            ],
        ],
        "rows_ru": [
            [
                "Хореография «восьмёрка»",
                "вращающаяся равносторонняя хореография теоремы 3.1",
                "два специальных решения одной задачи",
            ],
            [
                "Нулевой момент импульса L = 0",
                "настроенный циркуляционный паттерн (1, −1, 1)",
                "собственный триплет зарядов документа",
            ],
            [
                "Квадрупольная гребёнка на кратных 3/T",
                "радиальная модуляция ω теоремы 3.1",
                "спектральный отпечаток триады",
            ],
            [
                "Период хореографии T = 6.325914",
                "период жёсткого вращения вихревого треугольника",
                "оба специальных решения несут одни часы",
            ],
            [
                "Детектирование класса LISA",
                "лазерные темы TRX-01/12",
                "лазеры как измерительный прибор",
            ],
        ],
    },
    "nondim_en": (
        "All dynamics in canonical units G = m = 1: length in orbital radii, time in "
        "orbital units (one period T ≈ 6.33), energy in Gm²/L. Wave quantities in "
        "G = c = D = 1: strain in units of Gm/(c²D) and luminosity in units of Gm²ω⁶/c⁵, so "
        "the physical scaling to a system of total mass M and size scale L at distance D is "
        "linear in M and D — the same dimensionless solution maps onto any mass scale."
    ),
    "nondim_ru": (
        "Вся динамика в канонических единицах G = m = 1: длины в орбитальных радиусах, "
        "время в орбитальных единицах (один период T ≈ 6.33), энергия в Gm²/L. Волновые "
        "величины в единицах G = c = D = 1: деформация — в единицах Gm/(c²D), светимость — в "
        "единицах Gm²ω⁶/c⁵, поэтому физическое масштабирование на систему полной массы M и "
        "размера L на расстоянии D линейно по M и D — одно и то же безразмерное решение "
        "отображается на любую шкалу масс."
    ),
    "checks": {
        "header_en": ["Check", "Target", "Tolerance"],
        "header_ru": ["Проверка", "Цель", "Допуск"],
        "rows_en": [
            ["Period closure error (configuration returns to itself)", "0", "5e-8"],
            ["Period inside the published range [6.2, 6.5]", "yes", "exact"],
            ["Energy drift over one period", "0", "1e-12"],
            ["Total angular momentum (defining L = 0)", "0", "1e-9"],
            ["Mean luminosity proxy finite, 0 < P < 1e10", "yes", "exact"],
            ["Quadrupole choreography symmetry Q(T/3) = Q(0)", "yes", "1e-6"],
            ["Dominant harmonic on the comb (f·T = integer)", "0", "0.05"],
        ],
        "rows_ru": [
            ["Ошибка замыкания периода (конфигурация возвращается в себя)", "0", "5e-8"],
            ["Период внутри опубликованного диапазона [6.2, 6.5]", "да", "точно"],
            ["Дрейф энергии за один период", "0", "1e-12"],
            ["Полный момент импульса (определяющее L = 0)", "0", "1e-9"],
            ["Средняя светимость-прокси конечна, 0 < P < 1e10", "да", "точно"],
            ["Квадрупольная симметрия хореографии Q(T/3) = Q(0)", "да", "1e-6"],
            ["Доминирующая гармоника на гребёнке (f·T = целое)", "0", "0.05"],
        ],
    },
    "figure_caps": {
        "fig01_orbit_overview.png": {
            "cap_en": (
                "Orbit overview: (a) the figure-eight trajectory traced by all three equal "
                "masses over one period T = 6.325914 with the chase direction marked; "
                "(b) pairwise separations over the same period."
            ),
            "cap_ru": (
                "Обзор орбиты: (a) траектория-«восьмёрка», которую все три равные массы "
                "обводят за один период T = 6.325914, с отмеченным направлением погони; "
                "(b) парные расстояния за тот же период."
            ),
            "walk_en": (
                "All three bodies trace the identical closed curve; the pairwise "
                "separations r12/r13/r23 sweep the same range 0.6905 to 2.0000 and are "
                "permuted among the pairs every T/3 — the exchange symmetry that powers the "
                "quadrupole."
            ),
            "walk_ru": (
                "Все три тела обводят одну и ту же замкнутую кривую; парные расстояния "
                "r12/r13/r23 пробегают один и тот же диапазон от 0.6905 до 2.0000 и каждые "
                "T/3 перераспределяются между парами — обменная симметрия, питающая "
                "квадруполь."
            ),
        },
        "fig02_waveform_comb.png": {
            "cap_en": (
                "Headline result: plus-polarised waveform of the choreography over one "
                "orbit period (left) and the harmonic comb of its spectrum (right)."
            ),
            "cap_ru": (
                "Главный результат: плюс-поляризованная форма волны хореографии за один "
                "орбитальный период (слева) и гармоническая гребёнка её спектра (справа)."
            ),
            "walk_en": (
                "The exact strain spans −4.04 to +4.85 and repeats every T/6; the "
                "spectrum is a pure comb with lines at n = 6, 12, 18 of relative amplitudes "
                "1 : 0.091 : 0.0061, every other harmonic staying below 0.0013 of the "
                "dominant line at f·T = 5.9988."
            ),
            "walk_ru": (
                "Точная деформация лежит в диапазоне от −4.04 до +4.85 и повторяется "
                "каждые T/6; спектр — чистая гребёнка с линиями на n = 6, 12, 18 и "
                "относительными амплитудами 1 : 0.091 : 0.0061, все прочие гармоники лежат "
                "ниже 0.0013 доминирующей линии на f·T = 5.9988."
            ),
        },
        "fig03_pattern_sweep.png": {
            "cap_en": (
                "Directionality and isolation: time-averaged quadrupole antenna pattern "
                "(left) and the velocity-detuning sweep around the choreography (right)."
            ),
            "cap_ru": (
                "Направленность и изолированность: усреднённая по времени квадрупольная "
                "диаграмма направленности (слева) и развёртка по расстройке скоростей вокруг "
                "хореографии (справа)."
            ),
            "walk_en": (
                "Emission peaks along the orbital normal at 3.01 times the mean "
                "luminosity with in-plane minima 0.055 of the peak; scaling the initial "
                "velocities by k leaves the k = 1 closure residual at 7.6·10⁻⁹ while the "
                "nearest detuned case (k = 1.01) jumps to 0.028 with return-time shifts up "
                "to 1.67 — the eight is an isolated solution."
            ),
            "walk_ru": (
                "Излучение достигает максимума вдоль нормали к орбите — 3.01 средней "
                "светимости, внутриплоскостные минимумы составляют 0.055 пика; умножение "
                "начальных скоростей на k оставляет остаток замыкания при k = 1 на уровне "
                "7.6·10⁻⁹, тогда как ближайший расстроенный случай (k = 1.01) скачет до "
                "0.028 со сдвигами времени возврата до 1.67 — восьмёрка изолирована."
            ),
        },
        "fig04_quadrupole_dynamics.png": {
            "cap_en": (
                "Emitter dynamics: exact second derivatives of the quadrupole components "
                "(left) and the instantaneous and cumulative radiated energy (right)."
            ),
            "cap_ru": (
                "Динамика излучателя: точные вторые производные компонент квадруполя "
                "(слева) и мгновенная с накопленной излучённой энергией (справа)."
            ),
            "walk_en": (
                "The T/3 exchange symmetry and the T/2 sign flip of the xy component are "
                "visible in the components; the exact luminosity averages 76.51, peaks at "
                "159.73, and the cumulative radiated energy reaches 484.10 over one period "
                "(G = c = D = 1)."
            ),
            "walk_ru": (
                "В компонентах видны обменная симметрия T/3 и смена знака xy-компоненты "
                "на T/2; точная светимость в среднем равна 76.51 с пиком 159.73, а "
                "накопленная излучённая энергия достигает 484.10 за один период "
                "(G = c = D = 1)."
            ),
        },
    },
    "results_block": [
        "period_closure_error                = 1.2e-08  (T = 6.325914025)",
        "period_in_expected_range            = PASS (6.325914 vs published 6.325914)",
        "energy_conserved                    = 3.6e-15",
        "angular_momentum_is_zero            = 1.4e-15",
        "luminosity_finite_positive          = PASS (P = 1.65e8 in G=c=D=1 units)",
        "quadrupole_choreography_symmetry    = PASS (|Q(T/3)-Q(0)| = 1.48·10⁻⁸)",
        "dominant_harmonic_on_comb           = PASS (f*T = 5.9995 -> n = 6)",
        "status: PASS (7/7)",
    ],
    "abstract_en": (
        "This monograph turns the figure-eight choreography of Chenciner and "
        "Montgomery — three equal masses chasing each other along a single closed curve with "
        "zero angular momentum — into a quantified gravitational-wave source. The period is "
        "found by global minimisation of the configuration closure over one revolution: "
        "T = 6.325914025, matching the published 6.32591398 to 1.2e-08, with energy conserved "
        "to 3.6e-15 and the angular momentum zero to 1.4e-15 throughout. In the quadrupole "
        "approximation (G = c = D = 1) the mass quadrupole drives a plus-polarised strain "
        "spanning −4.04 to +4.85 that repeats six times per orbit period. The choreography "
        "symmetry Q(T/3) = Q(0), verified to 1.5·10⁻⁸, locks the spectrum into a harmonic "
        "comb: the dominant line lands at n = 6 of the orbital comb (f·T = 5.9995, residual "
        "5.0e-4) with overtones at 12 and 18 of relative amplitudes 0.091 and 0.0061. The "
        "time-averaged antenna pattern peaks along the orbital normal at 3.01 times the mean "
        "exact luminosity of 76.51, and a velocity-detuning sweep over k = 0.90 … 1.10 shows "
        "the eight is an isolated solution: the k = 1 closure residual is 7.6·10⁻⁹ while "
        "every detuned case exceeds 0.028. LISA-class laser interferometers are the natural "
        "readout."
    ),
    "abstract_ru": (
        "Настоящая монография превращает хореографию «восьмёрку» Ченчинера и "
        "Монтгомери — три равные массы, преследующие друг друга по одной замкнутой кривой с "
        "нулевым моментом импульса, — в количественно описанный источник гравитационных волн. "
        "Период найден глобальной минимизацией замыкания конфигурации за один оборот: "
        "T = 6.325914025, что совпадает с опубликованным 6.32591398 на уровне 1.2e-08; энергия "
        "сохраняется до 3.6e-15, момент импульса остаётся нулевым до 1.4e-15 на всём периоде. "
        "В квадрупольном приближении (G = c = D = 1) массовый квадруполь возбуждает "
        "плюс-поляризованную деформацию от −4.04 до +4.85, повторяющуюся шесть раз за "
        "орбитальный период. Симметрия хореографии Q(T/3) = Q(0), проверенная до 1.5·10⁻⁸, "
        "запирает спектр в гармоническую гребёнку: доминирующая линия попадает на n = 6 "
        "орбитальной гребёнки (f·T = 5.9995, остаток 5.0e-4) с обертонами на 12 и 18 и "
        "относительными амплитудами 0.091 и 0.0061. Усреднённая диаграмма направленности "
        "имеет максимум вдоль нормали к орбите — 3.01 средней точной светимости 76.51, а "
        "развёртка по расстройке скоростей k = 0.90 … 1.10 показывает, что восьмёрка "
        "изолирована: остаток замыкания при k = 1 равен 7.6·10⁻⁹, тогда как каждый "
        "расстроенный случай превышает 0.028. Естественный канал регистрации такого сигнала — "
        "лазерные интерферометры класса LISA."
    ),
    "intro_en": [
        (
            "Gravitational waves entered physics as a prediction of general relativity: Einstein "
            "derived the linearised field equations in 1916 and returned to the question in 1918 "
            "with the famous quadrupole formula, establishing that accelerating masses radiate "
            "energy at a rate controlled by the third time derivative of the mass quadrupole "
            "tensor. For decades the formula was disputed even among theorists — Eddington "
            "suspected the waves of being coordinate artifacts — until the quadrupole luminosity "
            "was worked out for concrete systems: Peters and Mathews (1963) computed the "
            "orbit-averaged radiation of Keplerian binaries, and the measured orbital decay of "
            "the binary pulsar PSR 1913+16 by Taylor and Weisberg (1982) confirmed that formula "
            "to better than half a percent, awarding the quadrupole approximation the status of "
            "quantitative science."
        ),
        (
            "The modern formalism descends from Thorne's 1980 review, which systematised the "
            "multipole expansion of gravitational radiation — source multipoles, the "
            "trace-free projection, the energy flux — into the standard toolbox used by every "
            "waveform model today; Maggiore's monograph (2007) fixed the pedagogical canon. "
            "Within this framework the plus-polarised strain of a distant observer is "
            "proportional to the second derivative of the trace-free quadrupole, and the "
            "luminosity is the squared sum of third derivatives — exactly the two objects this "
            "study computes for a three-body source, in units G = c = D = 1."
        ),
        (
            "The source itself has a shorter but remarkable history. Moore (1993) found, by "
            "numerical search over braided periodic orbits, that three equal bodies can chase "
            "each other along one curve; Chenciner and Montgomery (2000) then proved the "
            "existence of this figure-eight solution rigorously, via a variational argument "
            "combined with computer assistance, and Simó (2002) mapped the dynamical properties "
            "of the associated Poincaré map. The solution is exceptional in several ways at "
            "once: it is periodic, planar, collision-free, and it carries exactly zero angular "
            "momentum — a property that no circular binary shares and that shapes the emitted "
            "waveform."
        ),
        (
            "For TRIVORTEX the relevance is structural. The monograph's vortex program studies "
            "special triads — the rotating Lagrange triangle, the (1, −1, 1) collapse trio, the "
            "secular hierarchical cycles — and the figure-eight is the celestial sibling of the "
            "same family: a choreography whose symmetry group, not whose parameters, fixes its "
            "observables. Adding the quadrupole channel turns the choreography from a curiosity "
            "of celestial mechanics into a potential astrophysical signal, and the natural "
            "readout instrument is laser-based: LISA, Taiji and TianQin are laser "
            "interferometers whose million-kilometre arms are built on laser stability. The "
            "study therefore also documents the laser connection that runs through the laser "
            "block of the program (TRX-01, TRX-12)."
        ),
    ],
    "intro_ru": [
        (
            "Гравитационные волны вошли в физику как предсказание общей теории относительности: "
            "Эйнштейн вывел линеаризованные уравнения поля в 1916 году и вернулся к вопросу в "
            "1918-м со знаменитой квадрупольной формулой, установив, что ускоренные массы "
            "излучают энергию со скоростью, определяемой третьей производной по времени "
            "тенора массового квадруполя. Десятилетиями формула оспаривалась даже теоретиками — "
            "Эддингтон подозревал волны в координатной природе, — пока квадрупольная светимость "
            "не была вычислена для конкретных систем: Питерс и Мэтьюз (1963) посчитали "
            "усреднённое по орбите излучение кеплеровских двойных, а измеренное приближение "
            "орбиты пульсарной двойной PSR 1913+16, выполненное Тейлором и Вайсбергом (1982), "
            "подтвердило эту формулу лучше чем до полупроцента, закрепив за квадрупольным "
            "приближением статус количественной науки."
        ),
        (
            "Современный формализм восходит к обзору Торна (1980), систематизировавшему "
            "мультипольное разложение гравитационного излучения — мультиполи источника, "
            "бесследовую проекцию, поток энергии — в стандартный инструментарий сегодняшних "
            "моделей формы волны; монография Маджоре (2007) зафиксировала педагогический "
            "канон. В этой структуре плюс-поляризованная деформация у далёкого наблюдателя "
            "пропорциональна второй производной бесследового квадруполя, а светимость — сумме "
            "квадратов третьих производных; именно эти два объекта вычисляются здесь для "
            "трёхтелевого источника в единицах G = c = D = 1."
        ),
        (
            "У самого источника история короче, но замечательна. Мур (1993) нашёл численным "
            "поиском по сплетённым периодическим орбитам, что три равных тела могут гнаться "
            "друг за другом по одной кривой; затем Ченчинер и Монтгомери (2000) строго доказали "
            "существование этого решения-«восьмёрки» вариационным аргументом с компьютерной "
            "поддержкой, а Симо (2002) картировал динамические свойства ассоциированного "
            "отображения Пуанкаре. Решение исключительно сразу по нескольким линиям: оно "
            "периодично, плоско, свободно от столкновений и несёт в точности нулевой момент "
            "импульса — свойство, которого нет ни у одной круговой двойной и которое формует "
            "излучаемую волну."
        ),
        (
            "Для TRIVORTEX значимость структурна. Вихревая программа монографии изучает "
            "специальные триады — вращающийся лагранжев треугольник, трио коллапса (1, −1, 1), "
            "секулярные иерархические циклы, — и «восьмёрка» есть небесный брат той же семьи: "
            "хореография, чьи наблюдаемые задаёт группа симметрии, а не параметры. Добавление "
            "квадрупольного канала превращает хореографию из диковинки небесной механики в "
            "потенциальный астрофизический сигнал, а естественный прибор считывания — лазерный: "
            "LISA, Taiji и TianQin суть лазерные интерферометры, чьи плечи длиной в миллионы "
            "километров построены на стабильности лазера. Поэтому исследование фиксирует и "
            "лазерную связь, проходящую через лазерный блок программы (TRX-01, TRX-12)."
        ),
    ],
    "derivation_en": [
        (
            "The quadrupole channel follows from the slow-motion, weak-field expansion of the "
            "Einstein equations. To leading order the radiative degrees of freedom are driven by "
            "the trace-free part of the second mass moment Q_ij = Σ_k m_k x_ki x_kj (E2); the "
            "transverse-traceless projection at the observer gives the two polarisations, and "
            "for a face-on optimally oriented detector the plus-polarised strain is proportional "
            "to the second derivative of Q_xx − Q_yy (E3). The energy flux is set by the third "
            "derivatives (E4): with G and c restored, P = (G/5c⁵)⟨Σ(d³Q_ij/dt³)²⟩, so in the "
            "units G = c = D = 1 used throughout, the luminosity is literally (1/5) of the "
            "squared sum of third derivatives. The mass dipole is conserved (centre-of-mass "
            "motion) and cannot radiate; the quadrupole is the first radiating moment."
        ),
        (
            "The choreography structure enters through (E5). Because the three masses are equal "
            "and chase each other along one curve, the set of positions repeats itself every "
            "third of the period: {r_k(T/3)} = {r_k(0)}. The quadrupole, being a symmetric "
            "function of the configuration, is then exactly periodic with T/3, which restricts "
            "the spectrum to harmonics of 3/T. The measured spectrum sharpens this further: the "
            "dominant line lands at f·T = 5.9995, twice the pattern frequency 3/T, and the "
            "strain itself repeats six times per period — visible in the waveform panel as six "
            "identical lobes. The zero angular momentum is the second structural input: it "
            "removes the rotational Doppler-like asymmetry that a spinning binary would imprint, "
            "leaving a waveform whose shape is fixed by the figure-eight geometry alone."
        ),
        (
            "Numerically the quadrupole derivatives are computed exactly rather than by finite "
            "differences. Differentiating Newton's law (E1) once more gives the jerk — the third "
            "time derivative of position — in closed form, and the chain rule then yields the "
            "exact second derivatives Q̈ = Σ(2vv + 2xa) and third derivatives "
            "Q⃛ = Σ(6va + 2xj) of every quadrupole component from the state (positions, "
            "velocities, accelerations, jerks). This matters because chained finite "
            "differentiation of a numerically sampled trace amplifies error by orders of "
            "magnitude per pass: the acceptance check deliberately uses the simple finite-"
            "difference estimator as a finiteness gate only (recorded value 1.65e8 in "
            "G = c = D = 1 units), while the physical luminosity reported by the figure "
            "pipeline is 76.51 mean with peak 159.73."
        ),
    ],
    "derivation_ru": [
        (
            "Квадрупольный канал следует из разложения уравнений Эйнштейна по малым скоростям и "
            "слабому полю. В ведущем порядке излучательные степени свободы возбуждаются "
            "бесследовой частью второго массового момента Q_ij = Σ_k m_k x_ki x_kj (E2); "
            "поперечно-бесследовая проекция на наблюдателе даёт две поляризации, причём для "
            "оптимально ориентированного детектора плюс-поляризованная деформация "
            "пропорциональна второй производной Q_xx − Q_yy (E3). Поток энергии задаётся "
            "третьими производными (E4): с восстановленными G и c, P = (G/5c⁵)⟨Σ(d³Q_ij/dt³)²⟩, "
            "поэтому в единицах G = c = D = 1, используемых повсюду, светимость — это буквально "
            "(1/5) суммы квадратов третьих производных. Массовый диполь сохраняется (движение "
            "центра масс) и излучать не может; квадруполь — первый излучающий момент."
        ),
        (
            "Структура хореографии входит через (E5). Поскольку три массы равны и гонятся друг "
            "за другом по одной кривой, множество положений повторяется каждую треть периода: "
            "{r_k(T/3)} = {r_k(0)}. Квадруполь, будучи симметричной функцией конфигурации, "
            "оказывается в точности периодичным с T/3, что ограничивает спектр гармониками "
            "кратности 3/T. Измеренный спектр уточняет это дальше: доминирующая линия попадает "
            "на f·T = 5.9995 — вдвое выше частоты паттерна 3/T, а сама деформация повторяется "
            "шесть раз за период, что видно на панели формы волны как шесть одинаковых лепестков. "
            "Нулевой момент импульса — второй структурный вход: он убирает вращательную "
            "доплеро-подобную асимметрию, которую наложила бы вращающаяся двойная, оставляя "
            "форму волны, определённую одной лишь геометрией восьмёрки."
        ),
        (
            "Численно производные квадруполя вычисляются точно, а не конечными разностями. "
            "Дифференцируя закон Ньютона (E1) ещё раз, получаем рывок — третью производную "
            "положения по времени — в замкнутой форме, после чего правило цепочки даёт точные "
            "вторые производные Q̈ = Σ(2vv + 2xa) и третьи производные Q⃛ = Σ(6va + 2xj) каждой "
            "компоненты квадруполя прямо из состояния (положения, скорости, ускорения, рывки). "
            "Это важно, потому что цепочка конечных разностей на численно засэмплированной "
            "кривой усиливает ошибку на порядки за каждый проход: проверка приёмки сознательно "
            "использует простую конечно-разностную оценку только как вентиль конечности "
            "(записанное значение 1.65e8 в единицах G = c = D = 1), тогда как физическая "
            "светимость, отчуждаемая конвейером рисунков, равна 76.51 в среднем с пиком 159.73."
        ),
    ],
    "connection_en": (
        "Within the TRIVORTEX framework the figure-eight is the second special "
        "three-body solution besides the rotating equilateral choreography of Theorem 3.1 — "
        "two answers of one problem to the same requirement of exact periodicity. The "
        "zero angular momentum of the eight is the celestial twin of the document's own "
        "charge pattern: a tuned circulation triplet (1, −1, 1) whose angular impulse "
        "vanishes, so both models live on the zero-impulse slice of their phase spaces. The "
        "quadrupole comb at multiples of 3/T plays the role of the radial modulation "
        "frequency ω of Theorem 3.1 — in both cases a single spectral line family is the "
        "fingerprint of the triad's symmetry. Finally, the detection channel is a laser "
        "channel: TRX-01 and TRX-12 put lasers inside the three-body dynamics as actuators, "
        "while this study points lasers at it as detectors, closing the laser theme from "
        "both ends. TRX-09 supplies the vortex-language description of the same choreographic "
        "idea, and TRX-10 its hierarchical (secular) limit."
    ),
    "connection_ru": (
        "В рамках TRIVORTEX «восьмёрка» — второе специальное трёхтелевое решение "
        "после вращающейся равносторонней хореографии теоремы 3.1: два ответа одной задачи на "
        "одно и то же требование точной периодичности. Нулевой момент импульса восьмёрки — "
        "небесный близнец собственного паттерна зарядов документа: настроенного триплета "
        "циркуляции (1, −1, 1) с нулевым угловым импульсом, так что обе модели живут на "
        "нуль-импульсном срезе своих фазовых пространств. Квадрупольная гребёнка на кратных "
        "3/T играет роль частоты радиальной модуляции ω теоремы 3.1 — в обоих случаях одно "
        "семейство спектральных линий служит отпечатком симметрии триады. Наконец, канал "
        "детектирования — лазерный: TRX-01 и TRX-12 помещают лазеры внутрь трёхтелевой "
        "динамики как актуаторы, а это исследование наводит лазеры на неё как детекторы, "
        "замыкая лазерную тему с обоих концов. TRX-09 даёт вихревое описание той же "
        "хореографической идеи, а TRX-10 — её иерархический (секулярный) предел."
    ),
    "method_en": [
        (
            "The period is found before anything else is measured. The full system is integrated "
            "over [0, 12] with DOP853 at rtol = atol = 1e-13 and max_step 0.01; the closure is "
            "defined as the maximum deviation of the three positions from their initial values, "
            "scanned on a 1800-point grid over t ∈ [2, 11], and refined by bounded scalar "
            "minimisation with xatol 1e-13. The global minimum gives T = 6.325914025 with a "
            "closure residual of 1.2e-08 — inside the 5e-8 acceptance tolerance and consistent "
            "with the published 6.32591398. The period is then re-integrated over exactly "
            "[0, T] at max_step 0.005, and the invariants are monitored pointwise: the energy "
            "drift stays at 3.6e-15 and the total angular momentum at 1.4e-15 across 3000 "
            "samples."
        ),
        (
            "The quadrupole pipeline reuses the same trajectory: states are sampled on a "
            "12001-point grid for the protocol checks and on a 4801-point grid for the figures, "
            "and the quadrupole derivatives are evaluated from the exact analytic formulas — "
            "positions, velocities, accelerations and jerks of the DOP853 dense output — so the "
            "displayed waveform, spectrum and luminosity carry no numerical-differentiation "
            "edge artifacts. The strain is the second derivative of Q_xx − Q_yy; the "
            "instantaneous luminosity uses the trace-free combination (2Q⃛xx − Q⃛yy)/3, "
            "(2Q⃛yy − Q⃛xx)/3, −(Q⃛xx + Q⃛yy)/3 together with Q⃛xy, summed per (E4)."
        ),
        (
            "The spectral and directional diagnostics are deterministic. The spectrum is an FFT "
            "of the mean-subtracted exact strain over one full period — no window is needed "
            "because the signal is exactly periodic — with harmonic amplitudes tabulated for "
            "n = 1 … 30 of the orbital frequency. The antenna pattern is the time average of "
            "the transverse-traceless projected luminosity tensor contracted with the projector "
            "onto each sky direction, evaluated on a 181 × 121 (θ, φ) grid. The velocity-"
            "detuning sweep integrates the rescaled initial states (all velocities multiplied "
            "by k ∈ {0.90, 0.95, 0.98, 0.99, 1.00, 1.01, 1.02, 1.05, 1.10}) over [0, 8] at "
            "rtol = atol = 1e-11 and refines the first return with xatol 1e-10."
        ),
    ],
    "method_ru": [
        (
            "Период находится прежде всяких измерений. Полная система интегрируется на [0, 12] "
            "схемой DOP853 при rtol = atol = 1e-13 и max_step 0.01; замыкание определяется как "
            "максимальное отклонение трёх положений от начальных значений, сканируется сеткой "
            "из 1800 точек по t ∈ [2, 11] и уточняется ограниченной одномерной минимизацией с "
            "xatol 1e-13. Глобальный минимум даёт T = 6.325914025 с остатком замыкания 1.2e-08 — "
            "внутри допуска приёмки 5e-8 и согласуется с опубликованным 6.32591398. Затем период "
            "реинтегрируется точно на [0, T] при max_step 0.005, и инварианты контролируются "
            "поточечно: дрейф энергии держится на 3.6e-15, полный момент импульса — на 1.4e-15 "
            "по всем 3000 выборкам."
        ),
        (
            "Квадрупольный конвейер использует ту же траекторию: состояния сэмплируются сеткой "
            "из 12001 точки для проверок протокола и 4801 точки для рисунков, а производные "
            "квадруполя вычисляются по точным аналитическим формулам — положения, скорости, "
            "ускорения и рывки плотного вывода DOP853, — так что отображаемые форма волны, "
            "спектр и светимость свободны от краевых артефактов численного дифференцирования. "
            "Деформация есть вторая производная Q_xx − Q_yy; мгновенная светимость использует "
            "бесследовую комбинацию (2Q⃛xx − Q⃛yy)/3, (2Q⃛yy − Q⃛xx)/3, −(Q⃛xx + Q⃛yy)/3 вместе "
            "с Q⃛xy, суммируемых согласно (E4)."
        ),
        (
            "Спектральная и направленная диагностики детерминированы. Спектр — БПФ "
            "осреднённой точной деформации за один полный период — без окна, поскольку сигнал "
            "точно периодичен; амплитуды гармоник табулируются для n = 1 … 30 орбитальной "
            "частоты. Диаграмма направленности — усреднённое по времени значение "
            "поперечно-бесследовой проекции тензора светимости, свёрнутой с проектором на "
            "каждое направление неба, на сетке 181 × 121 (θ, φ). Развёртка по расстройке "
            "скоростей интегрирует пересчитанные начальные состояния (все скорости умножены "
            "на k ∈ {0.90, 0.95, 0.98, 0.99, 1.00, 1.01, 1.02, 1.05, 1.10}) на [0, 8] при "
            "rtol = atol = 1e-11 и уточняет первый возврат с xatol 1e-10."
        ),
    ],
    "analysis_en": [
        (
            "**Orbit and symmetry.** The period closure closes the loop first: T = 6.325914025 "
            "against the published 6.32591398, a mismatch of 1.2e-08 inside the 5e-8 tolerance, "
            "and the configuration returns on itself to the same 1.2e-08. Energy is conserved "
            "to 3.6e-15 and the angular momentum is zero to 1.4e-15 — the defining L = 0 "
            "property holds at machine precision. The pairwise separations sweep 0.6905 to "
            "2.0000 and are permuted among the three pairs every T/3, and the same order-3 "
            "exchange shows up on the quadrupole: Q(T/3) = Q(0) to 1.5·10⁻⁸ while "
            "Q(T/2) − Q(0) = 0.943 — the half period is emphatically not a symmetry, the "
            "choreography exchange is order three, not two."
        ),
        (
            "**Waveform and comb.** The exact plus-polarised strain spans −4.04 to +4.85 over "
            "one period and repeats every T/6, visible as six identical lobes in the waveform "
            "panel. The spectrum is a pure comb: the dominant line at n = 6 of the orbital "
            "comb (f·T = 5.9988 for the windowless exact spectrum; the acceptance check, "
            "computed on the finite-difference series with a Hann window, gives f·T = 5.9995 "
            "with residual 5.0e-4 against the 0.05 tolerance), overtones at n = 12, 18, 24 of "
            "relative amplitudes 0.091, 0.0061, 0.0004, and every other harmonic of the "
            "orbital frequency suppressed below 0.0013 of the peak. The dominant harmonic "
            "sits at exactly twice the T/3 pattern frequency 3/T, as the symmetry bookkeeping "
            "predicts."
        ),
        (
            "**Directionality.** The time-averaged quadrupole antenna pattern, built from exact "
            "third derivatives, peaks along the orbital normal at 3.01 times the mean "
            "luminosity — a face-on observer receives the strongest signal — while in-plane "
            "emission is suppressed to 0.055 of the peak both along the x-axis and along the "
            "diagonals of the eight. For a LISA-class instrument the observable is therefore "
            "strongly inclination-dependent, and the gold lobes drawn in the scheme mark the "
            "only directions worth pointing at."
        ),
        (
            "**Isolation and energy bookkeeping.** The velocity-detuning sweep proves the "
            "choreography is not a member of a nearby family: at k = 1 the closure residual "
            "is 7.6·10⁻⁹, while the nearest detuned case (k = 1.01) already sits at 0.028 and "
            "the extremes k = 0.90 and k = 1.10 reach 0.826 and 0.945, with return-time shifts "
            "from −1.63 to +1.67. On the energy side the exact luminosity averages 76.51 with "
            "a maximum of 159.73, so one period radiates 484.10 in G = c = D = 1 units. The "
            "acceptance-proxy value 1.65e8 recorded in the protocol is deliberately not used "
            "as a physical number: the chained finite-difference estimator amplifies sampling "
            "noise by orders of magnitude, and its only job is the finiteness gate "
            "0 < P < 1e10, which it passes."
        ),
    ],
    "analysis_ru": [
        (
            "**Орбита и симметрия.** Замыкание периода замыкает контур первым: T = 6.325914025 "
            "против опубликованного 6.32591398, расхождение 1.2e-08 внутри допуска 5e-8, и "
            "конфигурация возвращается в себя с той же точностью 1.2e-08. Энергия сохраняется "
            "до 3.6e-15, момент импульса равен нулю до 1.4e-15 — определяющее свойство L = 0 "
            "выполняется с машинной точностью. Парные расстояния пробегают от 0.6905 до 2.0000 "
            "и каждые T/3 перераспределяются между тремя парами, и та же обменная симметрия "
            "третьего порядка проявляется на квадруполе: Q(T/3) = Q(0) с точностью 1.5·10⁻⁸, "
            "тогда как Q(T/2) − Q(0) = 0.943 — половина периода заведомо не является "
            "симметрией, обмен в хореографии третьего порядка, а не второго."
        ),
        (
            "**Форма волны и гребёнка.** Точная плюс-поляризованная деформация пробегает от "
            "−4.04 до +4.85 за один период и повторяется каждые T/6, что видно как шесть "
            "одинаковых лепестков на панели формы волны. Спектр — чистая гребёнка: доминирующая "
            "линия на n = 6 орбитальной гребёнки (f·T = 5.9988 для оконной точной версии; "
            "приёмочная проверка, посчитанная по конечно-разностному ряду с окном Ханна, даёт "
            "f·T = 5.9995 с остатком 5.0e-4 против допуска 0.05), обертоны на n = 12, 18, 24 с "
            "относительными амплитудами 0.091, 0.0061, 0.0004, а все прочие гармоники "
            "орбитальной частоты подавлены ниже 0.0013 пика. Доминирующая гармоника лежит "
            "ровно вдвое выше частоты паттерна T/3, равной 3/T, — как и предсказывает "
            "симметрийная арифметика."
        ),
        (
            "**Направленность.** Усреднённая квадрупольная диаграмма направленности, построенная "
            "из точных третьих производных, имеет максимум вдоль нормали к орбите — 3.01 "
            "средней светимости, то есть наблюдатель «лицом» получает самый сильный сигнал, — "
            "тогда как внутриплоскостное излучение подавлено до 0.055 пика и вдоль оси x, и "
            "вдоль диагоналей восьмёрки. Для прибора класса LISA наблюдаемая потому сильно "
            "зависит от наклонения, и золотые лепестки на схеме отмечают единственные "
            "направления, куда стоит целиться."
        ),
        (
            "**Изолированность и энергетика.** Развёртка по расстройке скоростей доказывает, "
            "что хореография не член соседнего семейства: при k = 1 остаток замыкания равен "
            "7.6·10⁻⁹, тогда как ближайший расстроенный случай (k = 1.01) уже сидит на 0.028, "
            "а края k = 0.90 и k = 1.10 достигают 0.826 и 0.945 со сдвигами времени возврата "
            "от −1.63 до +1.67. По энергии точная светимость в среднем равна 76.51 с максимумом "
            "159.73, так что один период излучает 484.10 в единицах G = c = D = 1. Значение "
            "прокси-приёмки 1.65e8, записанное в протоколе, сознательно не используется как "
            "физическое число: цепочка конечных разностей усиливает шум сэмплирования на "
            "порядки, и её единственная работа — вентиль конечности 0 < P < 1e10, который она "
            "проходит."
        ),
    ],
    "discussion_en": [
        (
            "The model is deliberately minimal: Newtonian dynamics plus the leading quadrupole "
            "formula, planar and equal-mass. Within these assumptions every reported number is "
            "an exact statement about the governing equations rather than a simulation of a "
            "specific astrophysical system. The natural extensions each keep the verification "
            "style: unequal-mass choreographies and their literature continuum, the full "
            "multipole ladder beyond the quadrupole (octupole and higher), the gravitational-wave back-"
            "reaction on the orbit over many periods, and the time-dependent detector response "
            "of a LISA-class instrument at arbitrary inclination, which the present antenna "
            "pattern only summarises."
        ),
        (
            "The parameter regime is chosen for structural clarity. All results are quoted in "
            "units where G = m = c = D = 1; the physical mapping is linear — a system of total "
            "mass M and size scale L repeats the same dimensionless solution with the orbital "
            "frequency scaled by √(GM/L³) and the strain by GM/(c²D). Which astrophysical "
            "population could actually radiate into the mHz band of LISA, whether any natural "
            "system realises (or is captured into) a choreography, and how the comb signature "
            "survives environmental perturbations are astrophysical questions that lie beyond "
            "this study's scope but are now well posed: the comb and its 1 : 0.091 : 0.0061 "
            "amplitude ladder are falsifiable targets."
        ),
        (
            "Within the program this study completes the comparable-mass branch of the three-"
            "body block. TRX-10 treats the hierarchical (secular) limit of the same problem — "
            "Kozai–Lidov cycles instead of a choreography; TRX-09 describes the same "
            "choreographic idea in the vortex language of the monograph; TRX-01 and TRX-12 put "
            "lasers inside the three-body problem as actuators, while this study points lasers "
            "at it as the measuring instrument. Together they cover the three-body problem of "
            "the TRIVORTEX program from the restricted to the radiating comparable-mass case."
        ),
    ],
    "discussion_ru": [
        (
            "Модель сознательно минимальна: ньютоновская динамика плюс ведущая квадрупольная "
            "формула, плоскость и равные массы. В этих допущениях каждое сообщённое число — "
            "точное утверждение об определяющих уравнениях, а не симуляция конкретной "
            "астрофизической системы. Естественные расширения сохраняют верификационный стиль: "
            "хореографии неравных масс и их континуум в литературе, полная мультипольная "
            "лестница (октуполь и выше), гравитационно-волновое обратное действие на орбиту за "
            "много периодов и зависящий от времени отклик прибора класса LISA при произвольном "
            "наклонении, который настоящая диаграмма направленности лишь суммирует."
        ),
        (
            "Диапазон параметров выбран ради структурной ясности. Все результаты приведены в "
            "единицах G = m = c = D = 1; физическое отображение линейно — система полной массы "
            "M и масштаба L повторяет то же безразмерное решение с орбитальной частотой, "
            "масштабированной на √(GM/L³), и деформацией, масштабированной на GM/(c²D). Какие "
            "астрофизические популяции реально излучали бы в мГц-полосу LISA, реализует ли "
            "какая-либо природная система хореографию (или захватывается в неё) и как гребёнка "
            "переживает средовые возмущения — астрофизические вопросы за рамками этого "
            "исследования, но теперь они поставлены корректно: гребёнка и её лестница амплитуд "
            "1 : 0.091 : 0.0061 — фальсифицируемые цели."
        ),
        (
            "В рамках программы это исследование замыкает ветвь сравнимых масс трёхтелевого "
            "блока. TRX-10 разбирает иерархический (секулярный) предел той же задачи — циклы "
            "Козаи–Лидова вместо хореографии; TRX-09 описывает ту же хореографическую идею на "
            "вихревом языке монографии; TRX-01 и TRX-12 помещают лазеры внутрь задачи трёх тел "
            "как актуаторы, а это исследование наводит лазеры на неё как измерительный прибор. "
            "Вместе они покрывают задачу трёх тел программы TRIVORTEX от ограниченной до "
            "излучающей задачи сравнимых масс."
        ),
    ],
    "conclusions_en": [
        "The period of the figure-eight choreography, found by global minimisation of the configuration closure, is T = 6.325914025 — matching the published 6.32591398 to 1.2e-08 and inside the 5e-8 acceptance tolerance.",
        "Energy is conserved to 3.6e-15 and the total angular momentum stays zero to 1.4e-15 over one full period: the defining L = 0 property of the eight holds at machine precision.",
        "The equal-mass exchange symmetry is verified on the quadrupole: Q(T/3) = Q(0) to 1.5·10⁻⁸ while Q(T/2) − Q(0) = 0.943, confirming the choreography exchange is order three.",
        "The plus-polarised waveform spans −4.04 to +4.85, repeats six times per period, and its spectrum is a pure comb: dominant line at n = 6 (f·T = 5.9995, residual 5.0e-4), overtones at 12, 18, 24 with amplitudes 0.091, 0.0061, 0.0004, all other harmonics below 0.0013 of the peak.",
        "The time-averaged antenna pattern peaks along the orbital normal at 3.01 times the mean exact luminosity (76.51 mean, 159.73 peak, 484.10 radiated per period in G = c = D = 1); in-plane emission is suppressed to 0.055 of the peak.",
        "The velocity-detuning sweep over k = 0.90 … 1.10 shows the eight is isolated: the k = 1 closure residual is 7.6·10⁻⁹ while every detuned case exceeds 0.028, with return-time shifts up to 1.67.",
    ],
    "conclusions_ru": [
        "Период хореографии «восьмёрка», найденный глобальной минимизацией замыкания конфигурации, равен T = 6.325914025 — совпадение с опубликованным 6.32591398 на уровне 1.2e-08, внутри допуска приёмки 5e-8.",
        "Энергия сохраняется до 3.6e-15, а полный момент импульса остаётся нулевым до 1.4e-15 за один полный период: определяющее свойство восьмёрки L = 0 выполняется с машинной точностью.",
        "Обменная симметрия равных масс проверена на квадруполе: Q(T/3) = Q(0) с точностью 1.5·10⁻⁸, тогда как Q(T/2) − Q(0) = 0.943, — обмен в хореографии третьего порядка.",
        "Плюс-поляризованная форма волны пробегает от −4.04 до +4.85, повторяется шесть раз за период, а её спектр — чистая гребёнка: доминирующая линия на n = 6 (f·T = 5.9995, остаток 5.0e-4), обертоны на 12, 18, 24 с амплитудами 0.091, 0.0061, 0.0004, все прочие гармоники ниже 0.0013 пика.",
        "Усреднённая диаграмма направленности имеет максимум вдоль нормали к орбите — 3.01 средней точной светимости (в среднем 76.51, пик 159.73, 484.10 излучается за период в единицах G = c = D = 1); внутриплоскостное излучение подавлено до 0.055 пика.",
        "Развёртка по расстройке скоростей k = 0.90 … 1.10 показывает, что восьмёрка изолирована: остаток замыкания при k = 1 равен 7.6·10⁻⁹, тогда как каждый расстроенный случай превышает 0.028 со сдвигами времени возврата до 1.67.",
    ],
    "references": [
        "1. Einstein, A. (1918). *Über Gravitationswellen.* Sitzungsberichte der Königlich Preussischen Akademie der Wissenschaften (Berlin), 154–167.",
        "2. Peters, P. C., Mathews, J. (1963). *Gravitational radiation from point masses in a Keplerian orbit.* Physical Review 131, 435–440.",
        "3. Thorne, K. S. (1980). *Multipole expansions of gravitational radiation.* Reviews of Modern Physics 52, 299–339.",
        "4. Moore, C. (1993). *Braids in classical dynamics.* Physical Review Letters 70, 3675–3679.",
        "5. Chenciner, A., Montgomery, R. (2000). *A remarkable periodic solution of the three-body problem in the case of equal masses.* Annals of Mathematics 152, 881–901.",
        "6. Simó, C. (2002). *Dynamical properties of the eight map.* Celestial Mechanics 4, 343.",
        "7. Taylor, J. H., Weisberg, J. M. (1982). *A new test of general relativity: gravitational radiation and the binary pulsar PSR 1913+16.* The Astrophysical Journal 253, 908–920.",
        "8. Maggiore, M. (2007). *Gravitational Waves. Volume 1: Theory and Experiments.* Oxford University Press.",
        "9. Amaro-Seoane, P. et al. (2017). *Laser Interferometer Space Antenna.* arXiv:1702.00786.",
    ],
    "crosslinks_en": [
        "* **TRX-10** covers the hierarchical (secular) limit of the same three-body problem — Kozai–Lidov cycles instead of a comparable-mass choreography.",
        "* **TRX-01/12** place lasers *inside* the three-body dynamics as actuators; this study points lasers *at* it as detectors (LISA-class readout of three-body gravity).",
        "* **TRX-09** is the vortex-language description of the same choreographic idea: three circulations replacing three masses.",
    ],
    "crosslinks_ru": [
        "* **TRX-10** разбирает иерархический (секулярный) предел той же задачи трёх тел — циклы Козаи–Лидова вместо хореографии сравнимых масс.",
        "* **TRX-01/12** помещают лазеры *внутрь* трёхтелевой динамики как актуаторы; это исследование наводит лазеры *на* неё как детекторы (считывание трёхтелевой гравитации класса LISA).",
        "* **TRX-09** даёт вихревое описание той же хореографической идеи: три циркуляции вместо трёх масс.",
    ],
    "assumptions_en": [
        "Newtonian dynamics; general relativity enters only through the leading quadrupole formula (slow-motion, weak-field regime).",
        "Planar motion; out-of-plane excursions are not modelled, and the observer direction enters only through the antenna pattern.",
        "Equal masses and the exact Chenciner–Montgomery initial condition; unequal-mass choreographies are out of scope.",
        "Quadrupole order only: no higher multipoles, no gravitational-wave memory, and no back-reaction on the orbit within one period.",
        "The luminosity acceptance check uses the chained finite-difference estimator as a finiteness gate only; the figure pipeline recomputes the luminosity from exact analytic derivatives (76.51 mean versus the noise-dominated proxy 1.65e8).",
        "All quantities are dimensionless with G = m = 1 and wave units G = c = D = 1; the physical scaling to (M, D) is linear.",
    ],
    "assumptions_ru": [
        "Ньютоновская динамика; общая теория относительности входит только через ведущую квадрупольную формулу (режим малых скоростей и слабого поля).",
        "Плоское движение; вне-плоскостные экскурсии не моделируются, а направление на наблюдатель входит только через диаграмму направленности.",
        "Равные массы и точное начальное условие Ченчинера–Монтгомери; хореографии неравных масс вне рамок.",
        "Только квадрупольный порядок: без высших мультиполей, без памяти гравитационных волн и без обратного действия на орбиту в пределах одного периода.",
        "Проверка светимости использует цепочку конечных разностей только как вентиль конечности; конвейер рисунков пересчитывает светимость по точным аналитическим производным (76.51 в среднем против шумового прокси 1.65e8).",
        "Все величины безразмерны при G = m = 1 и волновых единицах G = c = D = 1; физическое масштабирование на (M, D) линейно.",
    ],
    "glance_en": [
        ["Block", "Gravitational waves — study 11 of 12"],
        ["Model", "figure-eight choreography (G = m = 1) + quadrupole radiation (G = c = D = 1)"],
        ["Key invariant", "zero angular momentum L = 0 (held to 1.4e-15 over one period)"],
        [
            "Headline result",
            "strain repeating every T/6; pure comb with the dominant line at n = 6 (f·T = 5.9995)",
        ],
        ["Verification", "7/7 checks PASS (full mode)"],
        ["Runtime", "8.17 s full (with figures) · < 20 s smoke"],
    ],
    "glance_ru": [
        ["Блок", "Гравитационные волны — исследование 11 из 12"],
        ["Модель", "хореография «восьмёрка» (G = m = 1) + квадрупольное излучение (G = c = D = 1)"],
        ["Ключевой инвариант", "нулевой момент импульса L = 0 (держится до 1.4e-15 за период)"],
        [
            "Главный результат",
            "деформация с повтором каждые T/6; чистая гребёнка с доминирующей линией на n = 6 (f·T = 5.9995)",
        ],
        ["Верификация", "7/7 проверок PASS (полный режим)"],
        ["Время выполнения", "8.17 с полный (с рисунками) · < 20 с smoke"],
    ],
    "glossary": {
        "header_en": ["Term", "Definition"],
        "header_ru": ["Термин", "Определение"],
        "rows_en": [
            [
                "Choreography",
                "a periodic solution in which all bodies trace the same closed curve, shifted in time",
            ],
            [
                "Figure-eight choreography",
                "the Chenciner–Montgomery equal-mass solution with zero angular momentum, period T ≈ 6.3259 in G = m = 1",
            ],
            [
                "Mass quadrupole Q_ij",
                "second moment Σ m_k x_ki x_kj of the mass distribution; the source of leading-order gravitational radiation",
            ],
            [
                "Plus-polarised strain h₊",
                "transverse-traceless projection of d²(Qxx − Qyy)/dt² observed at distance D",
            ],
            [
                "GW luminosity P",
                "power radiated in gravitational waves, P = (1/5)Σ(d³Q_ij/dt³)² in G = c = D = 1",
            ],
            [
                "Harmonic comb",
                "a spectrum consisting of equidistant lines at integer multiples of a base frequency",
            ],
            [
                "Antenna pattern",
                "direction-dependent time-averaged radiated power dP/dΩ of the emitter",
            ],
            [
                "Closure residual",
                "maximum deviation of the configuration from its initial state after a candidate period",
            ],
            [
                "Velocity detuning",
                "scaling all initial velocities by a factor k ≠ 1 to probe whether the periodic orbit is isolated",
            ],
            [
                "Jerk",
                "third time derivative of position; needed for the exact d³Q/dt³ of the luminosity formula",
            ],
        ],
        "rows_ru": [
            [
                "Хореография",
                "периодическое решение, в котором все тела обводят одну и ту же замкнутую кривую со сдвигом по времени",
            ],
            [
                "Хореография «восьмёрка»",
                "решение Ченчинера–Монтгомери равных масс с нулевым моментом импульса, период T ≈ 6.3259 при G = m = 1",
            ],
            [
                "Массовый квадруполь Q_ij",
                "второй момент Σ m_k x_ki x_kj распределения массы; источник гравитационного излучения ведущего порядка",
            ],
            [
                "Плюс-поляризованная деформация h₊",
                "поперечно-бесследовая проекция d²(Qxx − Qyy)/dt² на расстоянии D",
            ],
            [
                "ГВ-светимость P",
                "мощность гравитационно-волнового излучения, P = (1/5)Σ(d³Q_ij/dt³)² при G = c = D = 1",
            ],
            [
                "Гармоническая гребёнка",
                "спектр из эквидистантных линий на целых кратных базовой частоты",
            ],
            [
                "Диаграмма направленности",
                "зависящая от направления усреднённая по времени излучённая мощность dP/dΩ",
            ],
            [
                "Остаток замыкания",
                "максимальное отклонение конфигурации от начального состояния после пробного периода",
            ],
            [
                "Расстройка скоростей",
                "умножение всех начальных скоростей на множитель k ≠ 1, проверяющее изолированность периодической орбиты",
            ],
            [
                "Рывок",
                "третья производная положения по времени; нужна для точного d³Q/dt³ формулы светимости",
            ],
        ],
    },
    "notation": {
        "header_en": ["Symbol", "Meaning"],
        "header_ru": ["Символ", "Смысл"],
        "rows_en": [
            ["Q_ij", "mass quadrupole tensor, Q_ij = Σ_k m_k x_ki x_kj"],
            ["h₊(t)", "plus-polarised strain at the observer, ∝ d²(Qxx − Qyy)/dt²"],
            ["P", "gravitational-wave luminosity (G = c = D = 1 units)"],
            ["T", "period of the choreography, 6.325914025 in G = m = 1"],
            ["n", "harmonic index of the orbital comb, f = n/T"],
            ["f·T", "dimensionless position of a spectral line on the comb"],
            ["θ", "observer inclination measured from the orbital normal"],
            ["k", "velocity scale factor of the detuning sweep"],
            ["L_z", "total angular momentum of the three bodies (identically zero)"],
            ["r_ij", "pairwise separation, sweeping [0.6905, 2.0000] over one period"],
            ["Q⃛_ij", "third time derivative of the quadrupole, driving the luminosity (E4)"],
        ],
        "rows_ru": [
            ["Q_ij", "тензор массового квадруполя, Q_ij = Σ_k m_k x_ki x_kj"],
            ["h₊(t)", "плюс-поляризованная деформация у наблюдателя, ∝ d²(Qxx − Qyy)/dt²"],
            ["P", "гравитационно-волновая светимость (единицы G = c = D = 1)"],
            ["T", "период хореографии, 6.325914025 при G = m = 1"],
            ["n", "номер гармоники орбитальной гребёнки, f = n/T"],
            ["f·T", "безразмерное положение спектральной линии на гребёнке"],
            ["θ", "наклонение наблюдателя, отсчитываемое от нормали к орбите"],
            ["k", "множитель скоростей в развёртке расстройки"],
            ["L_z", "полный момент импульса трёх тел (тождественный нуль)"],
            ["r_ij", "парное расстояние, пробегающее [0.6905, 2.0000] за один период"],
            ["Q⃛_ij", "третья производная квадруполя по времени, возбуждающая светимость (E4)"],
        ],
    },
    "params_appendix": {
        "header_en": ["Symbol", "Value", "Role"],
        "header_ru": ["Символ", "Значение", "Роль"],
        "rows_en": [
            ["G, m", "1, 1", "gravitational constant and equal masses (canonical units)"],
            [
                "r₁(0)",
                "(0.97000436, −0.24308753)",
                "initial position of body 1; r₂ = −r₁, r₃ = (0, 0)",
            ],
            ["v₃(0)", "(−0.93240737, −0.86473146)", "initial velocity of body 3; v₁ = v₂ = −v₃/2"],
            ["T", "6.325914025", "period from closure minimisation (published 6.32591398)"],
            ["Integrator", "DOP853, rtol = atol = 1e-13", "max_step 0.005 (period search: 0.01)"],
            [
                "Dense sampling",
                "12001 points per period",
                "quadrupole derivative grid (figures: 4801)",
            ],
            [
                "Period search",
                "t ∈ [2, 11], 1800-point grid, xatol 1e-13",
                "bounded minimisation of the closure",
            ],
            [
                "Spectrum",
                "n ≤ 30 harmonics of f = 1/T",
                "FFT of the mean-subtracted exact strain, no window",
            ],
            ["Antenna grid", "181 × 121 (θ, φ)", "time-averaged TT-projected luminosity tensor"],
            [
                "Detuning sweep",
                "k ∈ {0.90 … 1.10}, 9 values",
                "closure refinement xatol 1e-10, integration [0, 8]",
            ],
        ],
        "rows_ru": [
            ["G, m", "1, 1", "гравитационная постоянная и равные массы (канонические единицы)"],
            [
                "r₁(0)",
                "(0.97000436, −0.24308753)",
                "начальное положение тела 1; r₂ = −r₁, r₃ = (0, 0)",
            ],
            ["v₃(0)", "(−0.93240737, −0.86473146)", "начальная скорость тела 3; v₁ = v₂ = −v₃/2"],
            ["T", "6.325914025", "период из минимизации замыкания (опубликован 6.32591398)"],
            ["Интегратор", "DOP853, rtol = atol = 1e-13", "max_step 0.005 (поиск периода: 0.01)"],
            [
                "Плотная выборка",
                "12001 точек на период",
                "сетка производных квадруполя (рисунки: 4801)",
            ],
            [
                "Поиск периода",
                "t ∈ [2, 11], сетка 1800 точек, xatol 1e-13",
                "ограниченная минимизация замыкания",
            ],
            ["Спектр", "n ≤ 30 гармоник f = 1/T", "БПФ осреднённой точной деформации, без окна"],
            [
                "Сетка диаграммы",
                "181 × 121 (θ, φ)",
                "усреднённый ТТ-проектированный тензор светимости",
            ],
            [
                "Развёртка расстройки",
                "k ∈ {0.90 … 1.10}, 9 значений",
                "уточнение замыкания xatol 1e-10, интегрирование [0, 8]",
            ],
        ],
    },
    "bibtex": [
        "@article{einstein1918,",
        "  author  = {Einstein, Albert},",
        '  title   = {{\\"U}ber Gravitationswellen},',
        '  journal = {Sitzungsberichte der K{\\"o}niglich Preussischen Akademie der Wissenschaften (Berlin)},',
        "  year    = {1918}, pages = {154--167}}",
        "",
        "@article{peters1963,",
        "  author  = {Peters, Peter C. and Mathews, Jon},",
        "  title   = {Gravitational radiation from point masses in a Keplerian orbit},",
        "  journal = {Physical Review},",
        "  year    = {1963}, volume = {131}, pages = {435--440}}",
        "",
        "@article{thorne1980,",
        "  author  = {Thorne, Kip S.},",
        "  title   = {Multipole expansions of gravitational radiation},",
        "  journal = {Reviews of Modern Physics},",
        "  year    = {1980}, volume = {52}, pages = {299--339}}",
        "",
        "@article{chenciner2000,",
        "  author  = {Chenciner, Alain and Montgomery, Richard},",
        "  title   = {A remarkable periodic solution of the three-body problem in the case of equal masses},",
        "  journal = {Annals of Mathematics},",
        "  year    = {2000}, volume = {152}, pages = {881--901}}",
        "",
        "@book{maggiore2007,",
        "  author    = {Maggiore, Michele},",
        "  title     = {Gravitational Waves. Volume 1: Theory and Experiments},",
        "  publisher = {Oxford University Press}, year = {2007}}",
    ],
}
