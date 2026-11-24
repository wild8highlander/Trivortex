# Changelog — TRIVORTEX MASTER

## 2.0.3 (2026-11-24) — pyflakes-zero and 100% docstrings

Code hygiene release: the entire code base is now **pyflakes-clean**
(0 non-architectural warnings in the package AND the single-file
edition) and **100% documented** (1040/1040 public definitions carry a
docstring, was 66.4%).

### Lint cleanup (0 pyflakes warnings)

- removed ~60 genuinely unused imports and locals across the package
  (f-string prefixes without placeholders dropped, dead bindings
  deleted, unused brackets removed);
- availability probes converted to `importlib.util.find_spec`
  (rebound/dedalus/moderngl/pyrender/matplotlib): booleans, not module
  bindings - the menu engine status keeps working;
- side-effect imports rewritten to `importlib.import_module` (menu-mode
  registration in tests/release notes) - no unused-name lint, same
  registration behavior;
- single-file edition: 110 module blocks re-synced from the package
  (the "linker-glue" contract of the original generator is preserved:
  verbatim bodies, `if _MODULE_MAIN` extinguishing, ROOT -> _PKG_ROOT,
  canonical global names PhysicsEngine_engine_base / self_check_* and
  82 others verified against the original link table);
- the remaining 186 pyflakes notes in the single file are the
  architectural `redefinition of unused` marks of the glue itself
  (import os/math per block) - by design, zero behavioral impact.

### Documentation to 100%

- AST-injected meaningful one-line docstrings for all 491 previously
  undocumented public entities (functions, classes, methods); hand
  overrides for ~120 central API points; English, matches the README
  surface; coverage metric (analysis.api_reference) = 1040/1040.

### Verification (both editions)

- selftest S1-S24: 24/24, exit 0, zero cross-marks;
- acceptance A1-A20: 20/20 (A19 menu count restored: the entry
  side-effect import of modes_extra is explicit now);
- pyflakes: package 0; single 0 (non-architectural);
- docstring coverage: 100.0%.

## 2.0.2 (2026-11-24) — English documentation release

Documentation release: the entire README surface is now **English**
(the root README and all 10 subfolder READMEs, rewritten and enriched),
the acceptance check A10 is language-neutral, and the asset gallery
gains three new real-run charts.

### Documentation

- **All READMEs in English**: the root README (rewritten: collapsible
  accelerator table, FAQ, roadmap timeline, contributing rules with the
  layer contracts) + core, lab, realism, render, reports, analysis,
  tools, data, docs, runs — banners, badges, mermaid diagrams, real
  charts and GIFs throughout
- New gallery charts, computed by the package's own engines:
  - `poincare_sections.png` — regular island vs chaotic sea of the
    Henon-Heiles potential (families of initial conditions through
    `PoincareMap`)
  - `cosmology_ladder.png` — the flat Lambda-CDM distance ladder
    (luminosity/comoving distances, lookback time; Planck-18)
  - `bright_stars_hr.png` — a color-magnitude view of the 25 brightest
    stars (realism/bright_stars, spectral classes)
- All banners/charts/sky-map titles translated to English; the SVG
  chip text is now XML-escaped (a raw `<` broke the core banner XML)

### CI robustness

- **A10 acceptance check made language-neutral**
  (tools/verify_package.py + the embedded copy): previously it grepped
  the Russian word for "profile" in README.md and would fail on an
  English README; now it accepts either `profile` or `профил`

### Version housekeeping

- coordinated bump to v2.0.2: VERSION, build_zip, A9 ZIP name, ACLL
  banner, single-file header block (historical mentions preserved)

### Quality (re-verified on this tree)

- selftest S1-S24: 24/24, exit 0, zero cross-marks — both editions
- acceptance A1-A20: 20/20 (A9 green after `build_zip.py`)
- quality gate: 49/49 module checks, hygiene of 117 files clean,
  docstrings 66% — **PASSED** (package and single-file edition)

## 2.0.1 (2026-11-24) — честность тестов, архитектура S3, документация

Технический релиз: три скрытых дефекта, маскировавших друг друга,
исправены; полный quality gate обоих изданий — **PASSED** (ранее
пакетный gate падал на гигиене из-за взаимных ложных срабатываний со
single-файлом, что не было замечено после генерации single-издания).

### Исправления ядра

- **TestResult.check (критично, analysis/tests.py)**: поздний успешный
  чек безусловно ставил `passed = True`, затирая ранний провал — тесты
  S3 и S9 показывали `[✓]` с внутренними `✗`. Семантика исправлена на
  «провал любого чека валит тест»; `__init__` стартует оптимистично.
  Именно этот баг скрывал два следующих дефекта.

- **S9 / Теорема 3.1 — допустимая область (Теорема B)**: замкнутая форма
  вырождена при C_Ch ≤ π·ln2 ≈ 2.1776 (ε>1, лимакон с внутренней
  петлёй, проход через центр) — дефолт ядра C_Ch=1 лежит ниже порога
  (зарегистрированный факт монографа polyvortex). Раньше разделение
  2π/3 проверялось геометрически ровно в вырожденной точке и «чудом»
  проходило лишь из-за бага check(). Теперь: разделение проверяется при
  C_Ch=π (ошибка 1.8e-15), вырождение при C_Ch=1 детектируется явно
  (ошибка 1.05 рад — порог работает), ω-пин на эталоне ядра сохранён;
  планировщик `theorem31()` документирует порог и кладёт флаг
  `admissible` в metadata.

- **S3 / render → realism (architecture)**: `render/ascii_sky.py`
  импортировал `realism.bright_stars` и `realism.sky_coordinates`,
  нарушая правило направлений (render → {core, lab}). Переведён на
  инъекцию зависимостей: `bind_astronomy(catalog, eq_to_horiz, ang_sep)`
  вызывается верхним слоем (modes_extra.py при загрузке,
  tools/quality_gate.py, tools/build_dist.py) — тот же паттерн, что
  `register_engine()` для адаптеров движков. Непривязанное состояние
  ловится внятной ошибкой.

- **Гигиена quality gate (взаимные ложные срабатывания)**: пакетный
  сканер флаговал single-файл (в нём дословно встроен код самого
  сканера с паттернами TODO/FIXME/XXX как данными), gate single-издания
  симметрично — пакетный сканер. Введён взаимный skip-набор
  «носителей кода сканера» в обеих копиях.

### Чистка мёртвого кода (поведение не менялось)

- lab/relativity.py: удалён черновой блок 1PN (A_coef + цикл с pass);
  каноническая форма (Меркурий 42.98″/век) сохранена дословно
- lab/collisions.py: мёртвый v_cm (импульс осколков строится от
  скорости меньшего тела — по контракту self_check)
- lab/halo_orbits.py: мёртвые a1/a2 со знаковой логикой (рабочие
  a1f/a2f сохранены)
- lab/hamiltonian_split.py: мёртвые conv2/conv4 + заглушка «ХХ» в
  docstring
- lab/nbody_tree.py: мёртвая рекурсия max_depth (never called)
- analysis/ttvs.py: мёртвые t_mid, res
- render/particles.py: проверка «все частицы умирают за 30 тиков»
  теперь реально входит в ok (ранее вычислялась и отбрасывалась)
- reports/writers/odt_writer.py: генерация столбцов без мёртвой ветки
  `if False`
- trivortex_master.py: импорт ascii_table вынесен из цикла

### Документация (новое)

- README.md для всех подпапок: core, lab, realism, render, reports,
  analysis, tools, data, docs, runs — баннеры (анимированные SVG со
  SMIL), бейджи, mermaid-диаграммы, реальные графики и гифки
- docs/assets/: 11 PNG из реальных прогонов (пресеты, Теорема 3.1 с
  порогом π·ln2, Хавелок, FLI, энергия, Barnes-Hut, Меркурий, приливы,
  TRAPPIST-1, каталог 538, спектры), 4 GIF собственным LZW-кодером,
  рейтрейсер, карта неба, 12 SVG-баннеров + логотип, реальные логи
  selftest/quality gate обоих изданий
- корневой README переписан: содержание, реальные результаты, лестница
  верификации (mermaid), архитектура с DI-паттерном, honest-limits
  дополнены Теоремой B

### Качество

- selftest S1–S24: 24/24 (пакет и single-издание, exit 0, ноль ✗)
- приёмка A1–A20: 20/20 (оба издания; A9 зелёный после build_zip)
- quality gate: 49/49 модульных чеков, гигиена 117 файлов чисто,
  docstrings 66% — **PASSED** (логи: docs/assets/quality_gate*.txt)
- pyflakes: устранены все значимые предупреждения (неиспользуемые
  локальные, мёртвые импорты в блоках)

## 2.0.0 (2026-11-21) — удвоенный объём

### Ядро лаборатории (+24 модуля)

- Постньютоновская динамика: 1PN/2PN (Меркурий 42.98″/век — точное

  совпадение с ОТО), слияние PSR B1913+16 по Питерсону (315 млн лет),
  ISCO Керра, Лензе-Тирринг

- Barnes-Hut O(N log N) на чистом Python: октодерево, θ-критерий,

  квадруполь; leapfrog-дрейф энергии < 3%

- Хаос: FLI (Хеньон-Хейлес: хаос 4.9 против 0.04 у регулярной),

  сечения Пуанкаре, частотный анализ Ласкара

- Столкновения: слияние/отскок/фрагментация с точным сохранением

  импульса; приливы (Луна 3.80 см/год против 3.82 LLR, нагрев Ио
  ×1.56 от 10¹⁴ Вт, Козаи 39.23°); радиация (Пойнтинг-Робертсон,
  Ярковский/Бенну, световой парус Starshot γ=0.67)

- CR3BP: точки Лагранжа L1-L5 Земля-Луна до 6 знака NASA, интеграл

  Якоби с контролем порядка RK4; гамильтоновы сплит-интеграторы
  (leapfrog/Yoshida-4/Suzuki-6, сходимость по дрейфу энергии)

- Космический аппарат: кватернионы, маховики с насыщением, ПИД

  разворот 90° за 12 с, |H| сохраняется до 1.8e-16

- Тиссеран (Церера 4.568, со-орбита T=3), троянцы (критерий Рабе

  0.03852), резонансы (промежутки Кирквуда ±0.015 а.е., лапласова
  цепочка Ио-Европа-Ганимед), манёвры (порог биэллиптики 12.02,
  Hohmann Земля→Марс 5.60 км/с / 259 сут), гравиманёвры (поворот
  v∞, Оберт), симуляция Солнечной системы из каталога

### Анализ (+14 модулей)

- MCMC Метрополиса: адаптивный шаг, R̂ Гельмана-Рубина 1.004,

  согласие с МНК-интервалом; Левенберг-Марквардт с ковариациями
  (RV: K=10.04±0.18 при истине 10)

- Ломб-Скаргл (FAP 4e-191 для сигнала, 1.0 для шума), BLS-транзиты

  (Kovács 2002, SDE 7.2), TTV (Lithwick-Xie-Wu сверхпериоды)

- Вейвлеты Морле (chirp 2→5 Гц с ошибкой 1.9%), энтропии

  (Шеннон/Bandt-Pompe/SampleEn + суррогатный тест Theiler)

- IOD по RA/Dec, собственные элементы + HCM-семьи (Zappalà),

  кривые блеска (Мандель-Аголь, Claret), corner-диаграммы

- Конвейер данных: DAG Кана, кэш по sha256, изоляция сбоев,

  транзитивный provenance

### Реализм (+12 модулей)

- Звёзды: M-L-R соотношения, Habets-81, Рош-Эггльтон 0.3789;

  каталог 25 ярчайших звёзд Hipparcos; спектральные цвета
  (Планка → CIE Wyman-2013 → sRGB: Солнце #FFF9F9)

- Архитектуры систем: Hill-устойчивость Гладмана, упаковка ЗЖЗ,

  TRAPPIST-1 (T_eq=250 К, цепочка резонансов как у Gillon 2017)

- Космология ΛCDM (Planck-18: возраст 13.80 Gyr, d_L(z=1) 6.81 Gpc),

  TLE-парсер (контрольные суммы NORAD), Horizons API + честный
  offline-фоллбэк, небесные координаты (прецессия, GMST, Сириус
  β=−39.61°), альманах (Сарос, затменный год), космическая погода
  (Паркер 47.3°, Kp→Ap NOAA, магнитопауза Шуэ, ГКЛ-обрезание)

### Рендер (+5 модулей)

- Программный рейтрейсер: Фонг, жёсткие тени, рекурсивные отражения,

  тонемаппинг Рейнхарда; система частиц (взрывы/диски/джеты);
  кинематографические камеры (орбита/следование/Катмулл-Ром/тряска);
  композитор кадров (слои, blend-режимы); ASCII-карта неба
  (стереографическая проекция, конформность)

### Отчёты: 8 форматов

- +ODT (OpenDocument): собственный писатель, mimetype STORED,

  валидация LibreOffice-конверсией; XLSX/PPTX на чистом stdlib
  (проверено чтением openpyxl/python-pptx)

### Данные

- Каталог: 258 → **538 объектов** (440 экзопланет NASA TAP, 98

  статических: планеты/луны/астероиды/кометы/звёзды)

- Пресеты: 10 → **20** (Сатурн/Уран/Нептун-системы, Проксима,

  лапласов резонанс, Галлея, тройка пояса, L4-троян Земли)

- Меню: 21 → **73 режима** в 11 категориях

### Исправления физики v1

- figure-eight: точные НУ Ченшинера-Монтгомери (E=−1.287142 — точно

  по литературе, дефект замыкания 3.9e-08; было: разлёт за период)

- Ламберт: вырожденный полуоборот (A=0) решён аналитической веткой

  (|v| точно до 1e-16; было: отказ None)

### Качество

- Selftest S1-S24: 24/24 (S13-S24 — против независимых эталонов)
- Приёмка A1-A20: 20/20; бенчмарк B1-B8: 8/8 за ~4 с
- Quality gate: 49/49 модульных проверок, гигиена кода чистая,

  docstrings 66%; ~24.4k строк Python (×2.07 от v1)

## 1.0.0 (2026-11-21) — первый выпуск

### Ядро

- Лаборатория N тел: сцены 3–7 тел, N=8 с флагом `allow_unphysical`

  (порог Хавелока, POLYVORTEX W4: max Re λ = +0.4502), жёсткий лимит 8

- Физика: ньютоновский RK4 (+1PN, диссипация, softening), вихри Кирхгофа

  с интегралами H, P, Q, I; инъекция адаптеров REBOUND/Dedalus/Custom
  через register_engine (без цикла lab↔realism)

- Планировщики траекторий: Теорема 3.1 (эталон ω=1.3748022274393588

  по коду ядра), Лагранж 1772, figure-eight (Chenciner–Montgomery 2000),
  кеплеровы орбиты, waypoints+Катмулл-Ром

- 10 пресетов сцен, включая реальную систему Барнарда из NASA TAP

### Рендер

- Собственный PNG-кодер: CRC32, 5 фильтров (вкл. Paeth), DEFLATE

  fixed-Huffman с хэш-цепочками (×88 ускорение против наивного поиска)

- Собственный GIF-LZW (GIF89a): побитно синхронный с каноном giflib/PIL,

  256-цветная палитра, NETSCAPE-loop; MP4 через ffmpeg/imageio

- pure_raster: 3D-программный рендер — матрицы 4×4, UV-сферы, scanline

  с z-буфером, освещение Ламберт+Блинн-Фонг, трейлы, оси

- ascii-бэкенд: truecolor-терминал, палитра плотности, авто-камера
- mpl-бэкенд: 2D/3D/4D (4-я координата — цвет/размер), 3 темы
- HUD AURORA: градиентный баннер ACLL, динамический прогресс-бар с

  EMA-ETA, системный монитор (cpu/ram/temp/io), деградация до плоского
  текста в пайпах

### Отчёты

- 7 форматов: TXT, MD, HTML (AURORA/ICE/MINIMAL, base64-графики), CSV,

  JSON, DOCX (собственный zip+OOXML, валиден python-docx), PDF 1.4
  (собственный писатель; кириллица транслитерируется в core-шрифтах)

### Данные

- data/catalog.json: 258 объектов (статическое ядро 98 + 160 экзопланет

  из TAP с суточным кэшем), у каждого — источник с URL

- data/literature.md: 21 аннотированный источник
- tools/build_catalog.py, tools/build_data_files.py

### Анализ

- Тесты S1–S12: структуры, сериализация, ацикличность графа импортов,

  реестр, интегралы V3/V4 (≤1e-10), энергия RK4, сравнение движков,
  Теорема 3.1 (2π/3), рендер-контракты, 7 форматов, лимит N=8

- Метрики: ляпуновский показатель (Бенеттин), дрейфы интегралов,

  расстояния траекторий, доминирующие периоды (собственный DFT)

- Полевые исследования: скан масса×скорость с бифуркациями; кольца

  Хавелока N=2..8 (согласие с прогнозом W4 — 100% на возмущённых)

### Интерфейс

- Интерактивное меню (21 режим, 8 категорий), EOF/Ctrl-C-safe
- CLI: --selftest, --preset, --simulate, --render, --gif, --report,

  --profile, --allow-unphysical, --no-color, --banner-only

- Логи сессий и JSON-протоколы прогонов в runs/

### Известные расхождения (задокументированы)

- ε Теоремы 3.1: README Trivortex приводит 0.7276…, код ядра даёт

  2.6681 — MASTER следует коду (core/bridge.py)

- Идеальное кольцо N=8 без шума не разваливается: линейная

  неустойчивость требует возмущения (полевой скан помечает unstable*)
