# TRIVORTEX MASTER v2.0.0 — справочник API

_Автогенерация из AST: всё, что здесь описано, существует в коде._

**96 модулей · 115 классов · 629 функций · документировано 687/1037 (66%)**

## Оглавление

- **analysis**: `api_reference.py`, `benchmark.py`, `corner_plots.py`, `entropy.py`, `field.py`, `fitting.py`, `lightcurves.py`, `lomb_scargle.py`, `mcmc.py`, `metrics.py`, `orbital_elements_fit.py`, `periodogram.py`, `pipeline.py`, `proper_elements.py`, `rmt.py`, `sandbox_physics.py`, `structure.py`, `tests.py`, `tests_extra.py`, `ttvs.py`, `wavelets.py`
- **core**: `bridge.py`, `config.py`, `registry.py`
- **entry**: `trivortex_master.py`
- **lab**: `body.py`, `chaos.py`, `choreography.py`, `collisions.py`, `engine_base.py`, `grid_fields.py`, `halo_orbits.py`, `hamiltonian_split.py`, `integrators.py`, `kepler.py`, `nbody_tree.py`, `observables.py`, `orbital_maneuvers.py`, `physics.py`, `presets.py`, `radiation.py`, `relativity.py`, `resonances.py`, `scene.py`, `solar_system_sim.py`, `spacecraft.py`, `tides.py`, `tissot.py`, `trajectory.py`, `trojan_points.py`, `units.py`
- **realism**: `almanac.py`, `bright_stars.py`, `cosmology.py`, `eclipse_predictor.py`, `encounter.py`, `jpl_horizons.py`, `mission_design.py`, `observatory.py`, `planetary_systems.py`, `sky_coordinates.py`, `space_weather.py`, `stellar.py`, `tles.py`, `validator.py`, `cache.py`, `nasa_exoplanet.py`, `nasa_planetary.py`, `custom_adapter.py`, `dedalus_adapter.py`, `rebound_adapter.py`
- **render**: `animator.py`, `ascii_sky.py`, `backend_ascii.py`, `backend_gl.py`, `backend_mpl.py`, `banners.py`, `camera.py`, `engine.py`, `font_5x7.py`, `frame_compositor.py`, `hud.py`, `particles.py`, `png_codec.py`, `pure_raster.py`, `raytracer.py`, `spectrum.py`
- **reports**: `bibliography.py`, `charts.py`, `engine.py`, `templates.py`, `docx_writer.py`, `odt_writer.py`, `pdf_writer.py`, `pptx_writer.py`, `xlsx_writer.py`

## Пакет `analysis`

### `analysis/api_reference.py`

**Функции:**

- `scan_module(path, package)` — Сканировать один файл: функции/классы/методы.
- `scan_all()` — Просканировать весь пакет.
- `to_markdown(infos, version='2.0.0')` — Markdown-справочник API.
- `write_api_doc(output=None, version='2.0.0')` — Сгенерировать docs/API.md.
- `stats()` — Сводка для меню «О комплексе».
- `self_check()` — Справочник сгенерирован и содержит реальные функции.

### `analysis/benchmark.py`

**Классы:**

- `Bench` — Один сценарий: замер + порог.

**Функции:**

- `bench_integrators()` — B1: двухтеловая орбита, 1000 шагов каждым интегратором.
- `bench_barnes_hut()` — B2: дерево на 400 телах.
- `bench_render()` — B3: кадры всеми бэкендами.
- `bench_codecs()` — B4: PNG и GIF-кодирование.
- `bench_vortex()` — B5: вихревой движок N=7, 200 шагов.
- `bench_mcmc()` — B6: MCMC 4×800 итераций.
- `bench_reports()` — B7: полный набор отчётов.
- `bench_wavelet()` — B8: CWT Морле на 600 точках, 24 частоты.
- `run_all(only=None)` — Прогнать бенчмарки; вернуть протокол.
- `save_protocol(result, path)`

### `analysis/corner_plots.py`

**Функции:**

- `marginal_histogram(samples, n_bins=20, weights=None)` — Гистограмма маргинального распределения (нормированная на пик).
- `hpd_levels(samples, levels=(0.68, 0.95))` — HPD-интервалы заданных уровней (плотнейший интервал).
- `two_dim_density(x, y, n_bins=16)` — 2D-гистограмма плотности (нормированная на пик, для corner).
- `corner_data(chains, labels)` — Полный набор для corner-диаграммы: маргиналы + пары + HPD.
- `render_corner_ascii(hist, width=46, height=9, label='')` — ASCII-гистограмма (столбики ▁▂▃▄▅▆▇█, 9 уровней).
- `render_corner_text(corner, width=46)` — Текстовая corner-диаграмма: все маргиналы подряд.
- `self_check()` — Гауссова цепь: пик гистограммы около μ; HPD68 покрывает ~68%;

### `analysis/entropy.py`

**Функции:**

- `shannon_entropy(x, n_bins=16)` — Энтропия по гистограмме значений (бит).
- `permutation_entropy(x, m=3, tau=1)` — Перестановочная энтропия (Bandt-Pompe): энтропия порядков
- `sample_entropy(x, m=2, r=None)` — Sample Entropy: −ln(B/A), B/A — совпадения длины m/m+1.
- `approximate_entropy(x, m=2, r=None)` — Approximate Entropy (Pincus 1991) — предшественник SampleEn.
- `phase_randomized_surrogates(x, n_surrogates=19, seed=1)` — Фазово-рандомизированные суррогаты: сохранить спектр мощности,
- `permutation_test(statistic, x, surrogates)` — Перестановочный тест (двусторонний): p-value против суррогатов.
- `self_check()` — Шум > синусоида по всем энтропиям; рост шума → рост PermEn;

### `analysis/field.py`

**Функции:**

- `classify_outcome(scene)` — Классификация судьбы прогона: escape/collision/regular/chaotic.
- `scan_mass_velocity(masses=None, v_factors=None, n_steps=200, progress=None, output_json=None)` — Сетка: масса P2 (в M⊕) × множитель круговой скорости P2.
- `scan_havelock(jitters=None, n_steps=400, progress=None, output_json=None)` — Кольца N=2..8 при шуме позиций: N≤7 держат форму, N=8 разваливается.
- `field_tables(results)` — Таблицы полевых исследований для ReportData.

### `analysis/fitting.py`

**Классы:**

- `LevenbergMarquardt` — Нелинейный МНК-фиттер.
  - `fit(self, theta0, max_iter=100, tol_chi2=1e-10, tol_theta=1e-10, lam0=0.001)` — Основной цикл LM. Возвращает θ̂, χ², ковариацию, историю.

**Функции:**

- `solve_linear(A, b)` — Решить A·x = b (Гаусс с главным элементом).
- `invert_matrix(A)` — Обратная матрица (Гаусс-Жордан).
- `gaussian_model(theta, x)` — A·exp(−(x−μ)²/2σ²) + c; theta = [A, mu, sigma, c].
- `exponential_decay(theta, x)` — A·exp(−t/τ) + c.
- `sine_model(theta, x)` — A·sin(2πft + φ) + c.
- `rv_model(theta, t)` — Кеплеровская RV: [K, P, e, omega, gamma] (через lab.kepler).
- `self_check()` — Гаусс: параметры в 3σ; RV: K в 2σ от истины.

### `analysis/lightcurves.py`

**Функции:**

- `limb_darkening(mu, u1=0.44, u2=0.26)` — Квадратичное затемнение к краю: I(μ)/I(1), μ = cos(угол).
- `transit_flux(t, period, r_planet, r_star, a_au=0.05, inclination_deg=88.0, u1=0.44, u2=0.26, n_grid=60)` — Нормированный поток (1.0 вне транзита) в момент t (сутки).
- `light_curve(t_obs, period, r_planet, r_star, **kw)` — Кривая блеска по сетке времён (с кэшем параметров).
- `measure_transit(t, f, period_hint, threshold=0.995)` — Измерить глубину, длительность, моменты ingress/egress.
- `fit_transit(t_obs, f_obs, period, guess_rp_rel=0.1, r_star_km=695700.0)` — Восстановить (r/R) из кривой блеска ЛМ-подгонкой.
- `inject_ttv(t_obs, period, amplitude_days, super_period)` — Внести TTV в сетку времён наблюдений (для синтетических тестов).
- `self_check()` — δ ≈ (r_p/r_*)² (u₁=u₂=0); fit восстанавливает r/R в 3σ;

### `analysis/lomb_scargle.py`

**Функции:**

- `lomb_scargle_at(t, y, dy, omega)` — Мощность LS на одной частоте (Press et al., Numerical Recipes §13.8).
- `frequency_grid(t, oversample=5.0, f_max=None)` — Сетка частот: [oversample/T, f_max] с шагом 1/(oversample·T).
- `lomb_scargle(t, y, dy, oversample=5.0, f_max=None)` — Полный LS-периодограмм: сетка, мощности, пик, FAP.
- `phase_fold(t, y, period, t0=0.0, n_bins=20)` — Сложить ряд по периоду; вернуть среднее y по фазовым бинам.
- `alias_report(t, ls, base_unit=1.0)` — Сильнейшие боковые пики: кандидаты в алиасы (f ± k·f_window).
- `self_check()` — Синусоида с пропусками: период восстановлен; шум не детектируется.

### `analysis/mcmc.py`

**Классы:**

- `ChainResult`
- `MetropolisSampler` — Адаптивный Метрополис-Гастингс.
  - `run(self, n_samples, burn_in=500)` — Прогнать цепь; вернуть пост-burn-in сэмплы.

**Функции:**

- `flat_prior(theta, bounds)` — Равномерный априор: log p = 0 внутри границ, −inf вне.
- `gaussian_prior(theta, means, sigmas)` — Гауссов априор: Σ log N(μ, σ).
- `gaussian_loglike(model, data, sigma, theta)` — Лог-правдоподобие гауссовых ошибок: −½Σ((d−m)/σ)².
- `gelman_rubin(chains)` — R̂ по каждому параметру (меж/внутри-цепная дисперсия).
- `autocorrelation_time(series, max_lag=50)` — Интегральное автокорреляционное время (оценка window-методом).
- `posterior_summary(samples, credible=0.9)` — Перцентили + среднее/σ + HPD-интервал по каждому параметру.
- `linear_model(theta, x)` — y = a + b·x.
- `kepler_rv_model(theta, t)` — RV кривая: v = K·cos(ν(t)+ω) + γ, ν из уравнения Кеплера.
- `self_check()` — Восстановить прямую y = 2 + 0.5x с шумом; истина в 90% HPD.

### `analysis/metrics.py`

**Функции:**

- `lyapunov_exponent(scene, n_steps=300, dt=None, perturbation=1e-08, renorm_every=10)` — Классическая схема Бенеттина: рядом с опорной траекторией живёт
- `integral_drifts(scene)` — Дрейф интегралов вдоль записанной истории сцены.
- `trajectory_distance(traj_a, traj_b)` — L2/Hausdorff-расстояния между двумя Trajectory (по общим временам).
- `dominant_periods(times, values, top=3)` — Доминирующие периоды через дискретное преобразование Фурье (простое,
- `scene_summary_metrics(scene)` — Сводный пакет метрик сцены для отчёта.

### `analysis/orbital_elements_fit.py`

**Функции:**

- `elements_to_state(a_au, e, i_deg, om_deg, w_deg, M_deg, mu=MU_SUN_KM)` — Элементы (а.е.) → (r, v) в км, км/с (перигей-ориентированная СК →
- `propagate_state(r, v, dt_days, mu=MU_SUN_KM)` — Численное продвижение состояния (RK4, шаг 0.5 сут).
- `geocentric_radec(r_helio_km, r_earth_km)` — Геоцентрические RA/Dec (градусы) объекта. Земля — гелиоцентрич.
- `earth_position_circular(t_days)` — Круговая модель Земли (1 а.е., 365.256 сут) в км — для демо.
- `fit_elements_lm(t_obs_days, ra_obs, dec_obs, ra_err_deg=0.01, guess=None)` — Определение элементов по трём+ наблюдениям.
- `self_check()` — Синтетический объект a=1.8, e=0.25: IOD восстанавливает a, e.

### `analysis/periodogram.py`

**Функции:**

- `bls_at_period(t, y, period, n_bins=200, duration_fracs=(0.015, 0.03, 0.05, 0.075))` — BLS-статистика SR на одном периоде: перебор фаз входа × длительностей.
- `bls(t, y, periods, n_bins=200)` — Полный BLS-периодограмм: SR по сетке периодов + SDE.
- `period_grid(t_min, t_span, p_min, p_max, n=2000)` — Лог-сетка периодов от p_min до p_max (n точек).
- `self_check()` — Синтетический транзит: период 3.5 сут, глубина 1%, SDE > 5.

### `analysis/pipeline.py`

**Классы:**

- `PipelineStep` — Один шаг: функция от словаря результатов входов.
  - `signature(self)` — Хэш имени+версии+входов — ключ кэша.
- `StepResult` — Результат шага: значение или ошибка + происхождение.
- `Pipeline` — DAG шагов с кэшированием и изоляцией сбоев.
  - `add(self, step)`
  - `topo_order(self)` — Сортировка Кана (1962): обнаруживает циклы.
  - `run(self, use_cache=True)` — Выполнить все шаги в топологическом порядке.
  - `summary(self)`

**Функции:**

- `self_check()` — DAG 5 шагов: порядок, кэш-хит, изоляция сбоя, цикл ловится,

### `analysis/proper_elements.py`

**Классы:**

- `AsteroidElements` — Оскулирующие элементы астероида (а.е., градусы).

**Функции:**

- `proper_semimajor_axis(a_series)` — Собственная полуось: медиана ряда a(t) (устойчива к выбросам).
- `proper_amplitude(series)` — Амплитуда свободной осцилляции: полуразмах центрированного ряда.
- `proper_elements_from_series(a_series, e_series, i_series)` — Комплект собственных элементов: a_p, e_p (центроид), I_p.
- `orbital_velocity(a_au, e)` — Средняя орбитальная скорость (км/с) по vis-viva на средней r.
- `asteroid_velocity_delta(e1, e2)` — Оценка Δv (км/с) между орбитами (практика HCM, Nesvorný 2015).
- `hcm_clustering(asteroids, cutoff_kms)` — Иерархическая кластеризация с одной связью (single-linkage).
- `synthetic_belt(seed=4)` — Пояс: 2 семьи (по 12 членов, Δv < 0.02 км/с) + 10 фоновых.
- `self_check()` — HCM при отсечке 0.05 км/с: ровно 2 крупных кластера ≥ 10 членов;

### `analysis/rmt.py`

**Функции:**

- `unfold_spacings(eigenvalues, degree=3)` — Полиномиальная развёртка спектра → нормированные интервалы.
- `r_statistic(spacings)` — Среднее r = min/max по соседним интервалам.
- `classify(r_value)` — Ближайший ансамбль по ⟨r⟩.
- `goe_cdf(s)` — GOE (β=1): P(s) = 1 − exp(−πs²/4).
- `gue_cdf(s)` — GUE (β=2): P(s) = 1 − exp(−4s²/π).
- `poisson_cdf(s)`
- `ks_test(spacings, cdf)` — KS-статистика D против заданной CDF.
- `analyze_spectrum(eigenvalues, degree=3)` — Развёртка → ⟨r⟩ → классификация → KS-тесты против всех ансамблей.
- `synthetic_ensemble(kind='gue', n=60, seed=42)` — Синтетический эталон: собственные значения случайной матрицы.
- `jacobi_eigenvalues(H, sweeps=40, tol=1e-10)` — Классический якобиев метод: вращения зануляют внедиагональ.
- `self_check()` — GOE-эталон должен классифицироваться близко к GOE.

### `analysis/sandbox_physics.py`

### `analysis/structure.py`

**Классы:**

- `ModuleInfo`

**Функции:**

- `analyze_module(path)`
- `analyze_all()`

### `analysis/tests.py`

**Классы:**

- `TestResult`
  - `ok(self, msg='')`
  - `fail(self, msg)`
  - `check(self, cond, ok_msg, fail_msg)`
  - `to_dict(self)`

**Функции:**

- `test_s1()`
- `test_s2()`
- `test_s3()`
- `test_s4()`
- `test_s5()`
- `test_s6()`
- `test_s7()`
- `test_s8()`
- `test_s9()`
- `test_s10()`
- `test_s11()`
- `test_s12()`
- `run_all(tests=None, verbose=True)` — Прогон выбранных (или всех) тестов; возвращает сводку.

### `analysis/tests_extra.py`

**Функции:**

- `test_s13()`
- `test_s14()`
- `test_s15()`
- `test_s16()`
- `test_s17()`
- `test_s18()`
- `test_s19()`
- `test_s20()`
- `test_s21()`
- `test_s22()`
- `test_s23()`
- `test_s24()`

### `analysis/ttvs.py`

**Функции:**

- `linear_ephemeris(t_obs)` — МНК-подгонка t_n = T0 + P·n: n — номер транзита (0-based).
- `oc_residuals(t_obs)` — O−C относительно линейной эфемериды (в сутках и в долях P).
- `ttv_amplitude(t_obs)` — Период и амплитуда TTV через LS-анализ O−C.
- `super_period(p_inner, p_outer, j)` — Сверхпериод TTV пары у резонанса j:j−1 (LXW12 eq. 2).
- `chopping_estimate(p_inner, mu_outer)` — Оценка амплитуды «chopping» TTV (LXW12): ~ (P/π)·μ —
- `self_check()` — Синтетическая TTV: период 3.5 сут, вариация 0.02 сут с периодом

### `analysis/wavelets.py`

**Функции:**

- `polyfit_least_squares(x, y, degree=1)` — Полиномиальная аппроксимация (нормальные уравнения, Гаусс).
- `polyval(coeffs, x)` — Значение полинома (coeffs от старшей степени).
- `detrend(y, degree=1)` — Удалить полиномиальный тренд; вернуть остатки.
- `morlet_psi_norm(t, w0=W_0)` — Нормированный Морле: (Re ψ, Im ψ) с ψ(0)=нормировка π^{-1/4}.
- `cwt_morlet(y, dt, freqs=None, w0=W_0)` — Continuous Wavelet Transform (Морле) на сетке частот.
- `scalogram_to_rows(cwt)` — Матрица мощностей для таблиц отчётов (freq × time).
- `dominant_ridge(cwt)` — (t, f) трек максимальной мощности по времени.
- `ridge_frequency_error(ridge, true_fn)` — Средняя относительная ошибка гребня против истинной частоты.
- `ar1_noise(n, alpha=0.7, seed=5)` — Красный шум AR(1): x_{t+1} = αx_t + ε.
- `significance_threshold(n, dt, alpha=0.7)` — Порог мощности 95% для AR(1)-шума (упрощённый χ²₁).
- `self_check()` — Chirp 2→5 Гц: гребень отслеживает частоту с ошибкой <15%;

## Пакет `core`

### `core/bridge.py`

**Классы:**

- `CoreStatus` — Снимок доступности ядра.
- `VerificationResult` — Результат прогона лестницы verify.py.

**Функции:**

- `find_trivortex()` — Поиск локальной копии репозитория Trivortex.
- `load_core()` — Импорт code/trivortex_core_en.py (или ru/общей версии) как модуля.
- `get_theorem31_reference()` — Эталонные значения (ω, ε) для валидации планировщика Теоремы 3.1.
- `get_havelock_reference()`
- `get_ladder_levels()`
- `health_check()` — Целостность ядра: пути, лестница, исследовательские протоколы.
- `run_verification(mode='quick', timeout=300.0)` — Прогон verification/trivortex/python/verify.py с парсингом JSON-протокола.
- `list_research_protocols()` — Список протоколов research/TRX-*/.
- `load_research_protocol(trx_id)` — Чтение протокола: README.md первых строк + список файлов.
- `theorem31_series(n_points=200, C_Ch=1.0, T=2 * 3.141592653589793)` — Замкнутая форма Теоремы 3.1 — собственная реализация моста

### `core/config.py`

**Классы:**

- `UnphysicalConfiguration` — Попытка создать конфигурацию вне физической вселенной модели.
- `MasterConfig` — Все настраиваемые параметры комплекса.
  - `validate(self)` — Возвращает список проблем конфигурации (пустой = всё хорошо).
  - `check_bodies(self, n)` — Лимит тел; кидает UnphysicalConfiguration.
  - `unphysical_note(self)` — Пометка о нефизичности для шапок отчётов (None если режим обычный).
  - `to_dict(self)`
  - `from_dict(cls, d)`
  - `save(self, path)`
  - `load(cls, path)`
  - `diff(self, other)` — Различия между двумя конфигурациями (для отчётов об изменениях).

**Функции:**

- `from_profile(name, **overrides)` — Собрать конфигурацию из профиля с переопределениями.
- `resolve_paths(config, root=None)` — Превращает относительные пути data/output в абсолютные от корня пакета.

### `core/registry.py`

**Классы:**

- `ModeEntry` — Один зарегистрированный режим (пункт меню).
- `Registry` — Хранилище режимов по категориям.
  - `register(self, entry)`
  - `capability(self, name, probe)` — Регистрация зонда возможности: (доступно ли, почему нет).
  - `get(self, name)`
  - `categories(self)`
  - `modes(self, category)`
  - `all_modes(self)`
  - `check_requirements(self, entry)` — Список причин недоступности (пустой = доступен).
  - `menu_spec(self)` — Спецификация меню для отрисовки: категории → пункты.

**Функции:**

- `register_mode(name, title, category, description='', requires=(), icon='•', order=50)` — Декоратор регистрации режима в глобальном реестре.
- `register_capabilities()` — Стандартные зонды возможностей (движки, пакеты, ядро).
- `engine_status_lines()` — Строки статуса движков для баннера и меню справки.

## Пакет `entry`

### `trivortex_master.py`

**Классы:**

- `App` — Сессия лаборатории: конфиг, сцена, последние результаты.
  - `new_run_dir(self, tag)`
  - `require_scene(self)`

**Функции:**

- `mode_scene_create(app)`
- `mode_scene_custom(app)`
- `mode_scene_info(app)`
- `mode_scene_catalog(app)`
- `mode_viz_render(app)`
- `mode_viz_ascii(app)`
- `mode_sim_run(app)`
- `mode_sim_trajectory(app)`
- `mode_anim_gif(app)`
- `mode_anim_mp4(app)`
- `mode_analysis_selftest(app)`
- `mode_analysis_metrics(app)`
- `mode_analysis_field(app)`
- `mode_analysis_rmt(app)`
- `mode_reports_generate(app)`
- `mode_settings_profile(app)`
- `mode_settings_physics(app)`
- `mode_settings_save(app)`
- `mode_help_engines(app)`
- `mode_help_literature(app)`
- `mode_help_about(app)`
- `print_menu()`
- `interactive()` — Главный интерактивный цикл; EOF-safe, Ctrl-C-safe.
- `cli(args)`
- `main()`

## Пакет `lab`

### `lab/body.py`

**Классы:**

- `Body` — Одно тело сцены.
  - `validate(self)`
  - `speed(self)`
  - `kinetic_energy(self)`
  - `potential_energy(self, other, G=6.6743e-11, softening=0.0)` — Ньютоновская взаимная потенциальная энергия (отрицательная).
  - `distance_to(self, other)`
  - `momentum(self)`
  - `angular_momentum_origin(self)`
  - `project_2d(self, plane='xy')`
  - `to_4d(self)`
  - `state_vector(self)` — [x, y, z, vx, vy, vz] — для интеграторов.
  - `to_dict(self)`
  - `from_dict(cls, d)`
  - `from_catalog(cls, obj_id, catalog)` — Создать тело из записи data/catalog.json.

**Функции:**

- `circular_orbit_velocity(central_mass, r, G=6.6743e-11)` — Скорость круговой орбиты v = √(GM/r).
- `place_on_orbit(central, satellite, orbit_radius, phase_deg=0.0, inclination_deg=0.0, G=6.6743e-11, retrograde=False)` — Поставить satellite на круговую орбиту вокруг central (в плоскости xy,

### `lab/chaos.py`

**Классы:**

- `PoincarePoint`
- `PoincareMap` — Сечение Пуанкаре для автономной системы с плоскостью q_i = q0.
  - `run(self, y0, t0, n_steps, max_points=500)` — Прогнать траекторию и собрать точки сечения.
  - `to_rows(self, n_axes=2)`

**Функции:**

- `fli(deriv, y0, t0, dt, n_steps=1000, delta0=1e-08, renorm_every=10)` — Fast Lyapunov Indicator: log‖Δ(t)‖ при фиксированных перенормировках.
- `fli_classify(fli_value, dt, n_steps)` — Грубая классификация по величине FLI относительно времени.
- `sliding_frequency(times, signal, window=128, n_windows=8)` — Основная частота в каждом окне (максимум |DFT| без нулевой).
- `frequency_drift(times, signal, window=128, n_windows=8)` — Относительный дрейф основной частоты по окнам.
- `henon_heiles_deriv(y, _t)` — Система Хеньона-Хейлеса (1964): классический эталон хаоса.
- `harmonic_deriv(y, _t)` — Регулярный осциллятор (контроль).
- `self_check()` — Хеньон-Хейлес: хаотические НУ против регулярной коробки.

### `lab/choreography.py`

**Функции:**

- `deriv_planar(y, n)`
- `rk4_planar(y, n, dt)`
- `initial_state(name)` — Начальное состояние по записи каталога.
- `closure_defect(y0, T, n, steps=400)` — ||y(T) − y(0)|| после steps шагов RK4.
- `polish(y0, T, n, steps=400, iters=3, h=1e-06)` — Гаусс-Ньютон: уменьшить дефект замыкания, шевеля x0/vy0 тела-1.
- `verify(name, steps=800)` — Верификация хореографии: полировка (при необходимости) + дефект.

### `lab/collisions.py`

**Классы:**

- `CollisionEvent` — Зарегистрированное столкновение/сближение.

**Функции:**

- `merge_bodies(a, b)` — Идеально неупругое слияние: масса/импульс сохраняются, энергия нет.
- `merge_energy_loss(a, b, G=6.6743e-11)` — Потеря кинетической энергии в системе ЦМ при слиянии.
- `bounce(a, b, restitution=1.0)` — Упругий (ε=1) или частично упругий отскок вдоль нормали (на месте).
- `fragment_on_impact(a, b, threshold_j_per_kg=100000.0, n_fragments=3, seed=42)` — Слияние или разрушение: если удельная энергия выше порога —
- `detect_collisions(bodies, extra_gap=0.0)` — Индексы пар с перекрытием (d < r1 + r2 + gap).
- `resolve_all(scene, restitution=0.0, merge=True)` — Обработать все столкновения сцены за шаг (события в scene.events).
- `self_check()` — Слияние сохраняет импульс; отскок — импульс и (ε=1) энергию.

### `lab/engine_base.py`

**Классы:**

- `EngineUnavailable` — Движок недоступен — диспетчер переключается на fallback.
- `BodyState` — Снимок состояния одного тела после шага движка.
- `PhysicsEngine` — Общий интерфейс всех движков (см. lab/physics.py для реализаций).
  - `step(self, dt)`
  - `get_states(self)`
  - `energy(self)`
  - `name(self)`
  - `apply_states(self)` — Записать состояния обратно в тела сцены (по умолчанию — никак).

### `lab/grid_fields.py`

**Функции:**

- `potential_at(point, bodies, G=6.6743e-11, softening=0.0)` — Потенциал Σ −Gm/max(r, soft).
- `potential_grid(bodies, half, n=32, G=6.6743e-11)` — Сетка n×n потенциала в плоскости xy: [(значение, x, y)].
- `roche_radius(primary_mass, satellite_mass, R_primary)` — Предел Роха (жидкий спутник): d ≈ 2.44·R·(M/m)^{1/3}.
- `hill_sphere(m_primary, m_perturber, a)` — Сфера Хилла: r ≈ a·(m/(3M))^{1/3}.
- `jeans_length(temperature, density, mass_per_particle=1.67e-27, G=6.6743e-11, k_B=1.381e-23)` — Длина Джинса: λ_J = c_s·√(π/(Gρ)).
- `escape_speed(mass, r, G=6.6743e-11)`
- `virial_radius(bodies, G=6.6743e-11)` — Оценка вириального радиуса: GM²/|E_pot| (однородная система).

### `lab/halo_orbits.py`

**Функции:**

- `cr3bp_deriv(mu)` — Правая часть: [ẋ, ẏ, ż, vẍ, vÿ, vz̈] во вращающейся СК.
- `jacobi_constant(state, mu)` — Интеграл Якоби: C = 2Ω − v².
- `lagrange_points(mu)` — Все пять точек Лагранжа (в нормированных единицах, барицентр 0).
- `jacobi_drift(mu, state0, dt=0.01, n_steps=1000)` — Дрейф интеграла Якоби вдоль интеграции (контроль точности).
- `linear_frequencies(mu, point)` — Частоты малых колебаний у точки Лагранжа (планарная, вертикальная).
- `lissajous_around_l2(mu, amplitude_xy=0.01, amplitude_z=0.02, dt=0.01, n_steps=2000)` — Квазипериодическая орбита вокруг L2 из линейного приближения.
- `self_check()` — Земля-Луна: L1 ≈ 0.837 от барицентра; L2 ≈ 1.156; L4 = 0.488/0.866;

### `lab/hamiltonian_split.py`

**Классы:**

- `SplitHamiltonian` — Гамильтониан в разделимой форме: T(p), V(q).
  - `kick(self, y, dt)`
  - `drift(self, y, dt)`
  - `step_kdk(self, y, dt)` — Kick-Drift-Kick (leapfrog), 2-й порядок.
  - `step_yoshida4(self, y, dt)` — Yoshida 4-го порядка: K(w₁)D(w₁)K(w₀)D(w₀)K(w₁)D(w₁)K(w₀)...
  - `step_suzuki6(self, y, dt)` — Suzuki 6-го порядка: композиция 15 секций.
  - `integrate(self, y0, dt, n_steps, method='kdk')` — Прогнать n_steps; вернуть траекторию.

**Функции:**

- `harmonic_h(omega=1.0)` — Осциллятор H = p²/2 + ω²q²/2 (точное решение известно).
- `energy_harmonic(y, omega=1.0)`
- `henon_heiles_h()` — Хеньон-Хейлес: T = (px²+py²)/2, V = (x²+y²)/2 + x²y − y³/3.
- `energy_henon_heiles(y)`
- `energy_drift_order(h, energy_fn, y0, dt, n_steps, method='kdk')` — Дрейф энергии |E(t) − E(0)|/E(0) после n_steps.
- `convergence_order(h, energy_fn, y0, dt=0.05, n_steps=2000)` — Порядок метода по скорости падения дрейфа при dt/2.
- `self_check()` — Осциллятор: kdk дрейф ~dt²; y4 дрейф ~dt⁴; период сохранён;

### `lab/integrators.py`

**Классы:**

- `LeapfrogStats` — Статистика прогона симплектического интегратора.
  - `energy_span(self)`
- `Leapfrog` — Kick–Drift–Kick: 2-й порядок, симплектический, энергия не дрейфует.
  - `step(self, y, t, dt)` — y = [x,y,z,vx,vy,vz]*N; KDK-схема.
- `VelocityVerlet` — Velocity Verlet — переупорядоченный leapfrog (позиции-первыми).
  - `step(self, y, t, dt)`
- `Yoshida4` — Симплектический интегратор 4-го порядка (Yoshida 1990).
  - `step(self, y, t, dt)`
- `AdaptiveStats`
  - `update(self, dt, ok)`
- `RK45Adaptive` — Адаптивный Рунге–Кутта 5(4): шаг подбирается под локальную ошибку.
  - `step(self, y, t, dt)` — Возвращает (y_new, t_new, err); err — оценка локальной ошибки.
  - `integrate(self, y, t, dt, duration, callback=None)` — Прогон с адаптацией шага до t+duration.
- `EnergyGuard` — Обёртка: откатывает шаг и режет dt при взрыве энергии.
  - `step(self, y, t, dt)` — Возвращает (y_new, t_new, dt_used).

**Функции:**

- `rk4_step(deriv, y, t, dt)` — Один шаг RK4; возвращает (новое y, новое t).
- `compare_integrators(deriv, accel, energy_of, y0, t0, dt, n_steps, n_bodies)` — Прогнать RK4/leapfrog/Yoshida4/RK45 на одной задаче.

### `lab/kepler.py`

**Классы:**

- `OrbitalElements` — Кеплеровы элементы (J2000-стиль).
  - `period(self, mu)` — Период обращения T = 2π√(a³/μ).
  - `energy(self, mu)` — Удельная энергия ε = −μ/(2a).
  - `r_peri(self)`
  - `r_apo(self)`

**Функции:**

- `kepler_E(M, e, tol=1e-12, max_iter=64)` — Решить уравнение Кеплера M = E − e·sin E для эксцентрической
- `true_anomaly(E, e)` — Истинная аномалия ν из эксцентрической E: tan(ν/2)=√((1+e)/(1−e))·tan(E/2).
- `radius_from_E(E, e, a)` — r = a(1 − e·cos E).
- `elements_to_state(el, mu)` — Кеплеровы элементы → (позиция, скорость) в плоскости экватора.
- `state_to_elements(pos, vel, mu)` — Вектор состояния → кеплеровы элементы (замкнутый обратный переход).
- `vis_viva_speed(mu, r, a)` — v = √(μ(2/r − 1/a)).
- `flight_time(el, mu, M0, M1)` — Время перелёта между двумя средними аномалиями (для эллипса).
- `apsides(el, mu)` — Перицентр/апоцентр: радиусы и скорости.
- `lambert(r1, r2, dt, mu, prograde=True, tol=1e-10, max_iter=200)` — Задача Ламберта: найти скорости v1/v2 на дуге r1→r2 за время dt.
- `hohmann_dv(r1, r2, mu)` — Двухимпульсный гоманов переход между круговыми орбитами.
- `self_check()` — Круговая проверка: элементы → состояние → элементы.

### `lab/nbody_tree.py`

**Классы:**

- `BodyLite` — Лёгкое тело для дерева (позиция, масса).
- `OctNode` — Узел октодерева: либо внутренний (8 детей), либо лист (1 тело).
  - `is_leaf(self)`
  - `is_empty(self)`
- `BarnesHutTree` — Октодерево с θ-критерием.
  - `build(self, bodies)`
  - `acceleration(self, b, eps2=None)` — Ускорение тела b от дерева (обход с θ-критерием).
  - `stats(self)`
- `BarnesHutEngineMixin` — Примесь: шаг интегрирования через дерево.
  - `step_all(self, bodies, dt, G=G_SI)` — Один leapfrog-шаг всех тел (на месте).
- `SimBody` — Тело с скоростями для полноценного прогона Barnes-Hut.

**Функции:**

- `direct_accelerations(bodies, G=G_SI, softening=0.0)` — O(N²) точные ускорения (эталон для сравнения точности).
- `benchmark(n_bodies=500, seed=42, theta=0.7)` — Сравнить Barnes-Hut с direct: время и относительная ошибка.
- `self_check()` — Плаккеровский кластер: сохранение энергии leapfrog на дереве.

### `lab/observables.py`

**Функции:**

- `radial_velocity(body_state, observer_dir=(1.0, 0.0, 0.0))` — Лучевая скорость: проекция скорости на направление наблюдателя.
- `transit_depth(r_planet, r_star)` — Глубина транзита (r_p/R_*)².
- `doppler_shift(f0, v_los, c=299800000.0)` — Релятивистский (1-й порядок) доплер: Δf/f = v/c.
- `light_curve_transit(phase, depth, width=0.1)` — Простая-box модель кривой блеска: единица вне, 1−depth внутри.
- `separation_history(traj, body_a=0, body_b=1)` — История расстояний между двумя телами по Trajectory.
- `closest_approach(traj, body_a=0, body_b=1)` — (минимальное расстояние, индекс кадра).

### `lab/orbital_maneuvers.py`

**Функции:**

- `circular_speed(r_km, mu=MU_EARTH_KM)`
- `tangential_burn(r_km, dv_kms, mu=MU_EARTH_KM)` — Тангенциальный импульс на круговой орбите → новые a, e, период.
- `inclination_change(v_kms, delta_i_deg)` — Чистое изменение наклонения: Δv = 2·v·sin(Δi/2) (км/с).
- `combined_plane_change(v1_kms, v2_kms, delta_i_deg)` — Комбинированный манёвр в узле: Δv = √(v₁²+v₂²−2v₁v₂cosΔi).
- `hohmann_total(r1_km, r2_km, mu=MU_EARTH_KM)` — Суммарный Δv гомановского перехода (км/с).
- `bielliptic_total(r1_km, r2_km, r_b_km, mu=MU_EARTH_KM)` — Биэллиптический переход: r₁ → r_b → r₂ (км/с, время в сутках).
- `bielliptic_threshold(r1_km=1.0)` — Порог выгодности биэллиптического: r₂/r₁ ≈ 11.94 при r_b → ∞.
- `phasing_angle(phase_deg, n_revs=1)` — Угол фазирования: дрейф (360·N ± Δφ) за N+1 витков (градусы).
- `phasing_period(drift_angle_deg, base_period_min, direction='ahead')` — Период фазирующей орбиты: P' = P·(1 ± Δφ/360·1/N).
- `drag_decay_time(h_km, ballistic_coef=100.0)` — Время жизни на круговой орбите при экспоненциальной атмосфере.
- `self_check()` — Биэллиптика выгоднее при r₂/r₁ = 15; Δv наклонения формула точна;

### `lab/physics.py`

**Классы:**

- `PhysicsEngine` — Нативный движок: общая логика для реализаций этого пакета.
  - `apply_states(self)` — Записать состояния обратно в тела сцены.
- `NewtonianEngine` — N тел, гравитация Ньютона, интегратор RK4.
  - `name(self)`
  - `step(self, dt)`
  - `get_states(self)`
  - `energy(self)`
- `VortexEngine` — Точечные вихри Кирхгофа в плоскости xy (z игнорируется).
  - `name(self)`
  - `hamiltonian(self)`
  - `integrals(self)`
  - `step(self, dt)`
  - `get_states(self)`
  - `energy(self)`

**Функции:**

- `register_engine(name, cls)` — Регистрация стороннего движка (вызывается realism/).
- `engine_registry()` — Все известные движки: нативные + инжектированные адаптеры.
- `resolve_auto(scene)` — Авто-выбор движка: REBOUND при наличии, иначе native.
- `get_engine(name, scene)` — Получить движок с fallback-цепочкой при недоступности.
- `run_simulation(scene, n_steps=None, dt=None, record_every=1, progress=None, stop_on_collision=False)` — Прогнать сцену вперёд. Возвращает сводку: шаги, время, энергия-дрейф,

### `lab/presets.py`

**Функции:**

- `load_catalog(path=None)`
- `catalog_objects(catalog=None)`
- `catalog_summary(catalog=None)`
- `search_catalog(query, catalog=None, limit=20)`
- `validate_catalog(catalog=None)`
- `load_presets(path=None)`
- `get_preset(preset_id, path=None)`
- `build_preset(preset_id, config, catalog=None)` — Собрать сцену из пресета по id.
- `preset_list_description()` — [(id, имя, N тел)] для меню.

### `lab/radiation.py`

**Классы:**

- `DustGrain` — Сферическая пылинка.
  - `mass(self)`
  - `cross_section(self)`

**Функции:**

- `flux_at(r, L=L_SUN)` — Поток излучения на расстоянии r: L/(4πr²).
- `beta_ratio(grain, L=L_SUN, M=M_SUN)` — Отношение радиационной силы к гравитации: β = 3LQ/(16πcGMρs).
- `pr_drag_acceleration(grain, r, v_orb, L=L_SUN)` — Тангенциальное замедление Пойнтинга-Робертсона.
- `pr_lifetime(grain, a, L=L_SUN, M=M_SUN)` — Время падения с орбиты a до звезды (Wyatt & Whipple 1950).
- `yarkovsky_drift_rate(radius, density=2000.0, thermal_inertia=300.0, emissivity=0.9, semi_major=1.126 * AU, L=L_SUN)` — Скорость da/dt эффекта Ярковского (м/год, сезонная+суточная оценка).
- `bennu_check()` — Бенну: OSIRIS-REx измерил da/dt = −281±5 м/год (2021).
- `sail_acceleration(area, mass, flux, reflectivity=0.9)` — Ускорение идеального паруса: a = (1+R)·F/c·A/m (R — отражение).
- `sail_gamma(time, area, mass, flux0=1000000000.0, reflectivity=0.9)` — Скорость (доля c) после разгона лазером с потоком flux0 (Вт/м²).
- `starshot_check()` — Breakthrough Starshot: грамм-зонд, 16 минут разгона до 0.2c.
- `radiation_force_on_body(r_body, mass, dist, L=L_SUN, Q_pr=1.0)` — Сила радиационного давления на сферическое тело (Н).
- `radiation_accel_expr(r_body, mass)` — Выражение ускорения для песочницы CustomEngine (радиальный драг).
- `self_check()` — Эталонные величины из первых принципов.

### `lab/relativity.py`

**Классы:**

- `TwoBodyPN` — Задача двух тел с постньютоновскими поправками (СИ).
  - `M(self)`
  - `eta(self)` — Симметричная массовая доля η = m1·m2/M².
  - `period(self)` — Кеплеров период (нулевой ПН-порядок).

**Функции:**

- `eih_acceleration(r, v, M, eta=0.0, G=G_SI)` — Относительное 1PN-ускорение (гармоническая калибровка, Wagoner-Will).
- `pn2_acceleration(r, v, M, eta, G=G_SI)` — 2PN-ускорение (порядок v⁴/c⁴), Blanchet & Iyer, CQG 20, 757 (2003).
- `total_pn_acceleration(r, v, M, eta, order=1, G=G_SI)` — Полное ПН-ускорение до заданного порядка (1 или 2).
- `perihelion_precession(tb, order=1)` — Прецессия перигелия в угловых секундах за столетие.
- `mercury_precession()` — Классический тест ОТО: Меркурий, 42.98″/век.
- `lense_thirring_precession(M, R, spin_period, a, e=0.0, incl=math.pi / 2)` — Прецессия Лензе-Тирринга узла орбиты (де Ситтер/оценка).
- `schwarzschild_radius(M)` — r_s = 2GM/c².
- `isco_radius(M, spin=0.0)` — ISCO Керра: r_isco/M = 3+Z2−sgn(a)√((3−Z1)(3+Z1+2Z2)) (Bardeen 1972).
- `tidal_disruption_radius(m_bh, m_star, r_star)` — Радиус приливного разрушения: r_t ≈ R_star·(M_bh/m_star)^{1/3}.
- `gw_quadrupole_loss(m1, m2, a, e=0.0)` — Потеря энергии и слияние по Питерсону (1964).
- `hubble_luminosity_distance_gw(f_gw)` — Грубая оценка характерной струны амплитуды h ~ 1e-21·(источник).
- `self_check()` — Меркурий: 1PN ≈ 42.98″/век; ISCO Шварцшильда = 6GM/c².

### `lab/resonances.py`

**Функции:**

- `resonance_location(a_planet, p, q)` — Большая полуось p:q-резонанса с планетой (а.е. → та же единица).
- `kirkwood_check(a_jupiter=5.2038)` — Положения промежутков Кирквуда против опубликованных значений.
- `wisdom_chaotic_zone(m_planet, m_star, a_planet)` — Полуширина хаотической зоны: δa/a ≈ 1.5·μ^{2/7}, μ = m_p/(3M).
- `jupiter_zone_check()` — Хаотическая зона Юпитера: δa ∈ [0.5, 1.3] а.е. — литература.
- `laplace_ratios()` — Отношения периодов тройного лапласова резонанса (2:1, 4:1).
- `resonance_angle(lam_body, lam_perturber, varpi_body, p, q)` — Критический аргумент резонанса p:q: φ = p·λ_q − q·λ_p + (q−p)·ϖ.
- `is_librating(angles_deg, tol=60.0)` — Грубая проверка либрации: разброс φ меньше tol градусов
- `ttv_super_period(p_inner, p_outer, j)` — Сверхпериод TTV пары у резонанса j:j−1.
- `ttv_pair_report(p_inner, p_outer)` — Диагностика пары: ближайший резонанс и ожидаемый сверхпериод.
- `kepler_9_check()` — Kepler-9 b/c (Holman et al. 2010): P=19.24/38.91 сут, у 2:1.
- `first_order_width(mu, e, j)` — Полуширина резонанса j:j−1 в единицах a (Murray & Dermott 1999).
- `self_check()` — Кирквуд + Лаплас + Wisdom + LXW12 super-period.

### `lab/scene.py`

**Классы:**

- `BoundingBox` — Границы сцены (м или единицы модели).
  - `from_scene(cls, bodies, margin=1.5)`
  - `contains(self, p)`
- `ValidationReport` — Отчёт валидации сцены.
  - `to_dict(self)`
- `Scene` — Сцена N тел.
  - `add_body(self, body)` — Добавить тело; здесь живёт механика порога Хавелока.
  - `remove_body(self, body_id)`
  - `body(self, body_id)`
  - `n(self)`
  - `validate(self)`
  - `total_mass(self)`
  - `total_energy(self, G=None)`
  - `total_momentum(self)`
  - `total_angular_momentum(self)`
  - `center_of_mass(self)`
  - `apply_engine(self, name)` — Выбор и инициализация физического движка (лениво, чтобы не тянуть
  - `clone(self)`
  - `summary(self)`
  - `record_frame(self)`
  - `to_dict(self, include_history=False)`
  - `from_dict(cls, d)`
  - `save(self, path)`
  - `load(cls, path)`

### `lab/solar_system_sim.py`

**Функции:**

- `build_solar_system(config=None)` — Собрать Солнце + 8 планет из каталога (позиции на J2000+Δt).
- `kepler_period_check(system=None)` — Численный период против табличного (интеграция одного оборота).
- `synodic_periods_check()` — Синодический период: P_syn = 1/|1/P_p − 1/P_e| против таблицы.
- `angular_momentum_budget(system=None)` — Бюджет момента: орбитальный Л = m·√(μa(1−e²)); спиновой.
- `escape_velocity_check(system=None)` — Вторая космическая скорость: v = √(2GM/R) против факт-листа.
- `system_summary_table(system=None)` — Таблица для отчётов: тело, масса, радиус, период, скорость.
- `self_check()` — Периоды, синодика, escape-скорости, бюджет момента.

### `lab/spacecraft.py`

**Классы:**

- `Quaternion` — Единичный кватернион ориентации (w, x, y, z).
  - `conjugate(self)`
  - `norm(self)`
  - `normalize(self)`
  - `from_axis_angle(cls, axis, angle_rad)`
  - `rotate(self, v)` — Повернуть вектор: v' = q ⊗ v ⊗ q*.
  - `angle_to(self, other)` — Угловое расстояние между ориентациями (рад).
  - `to_dict(self)`
- `PIDController` — ПИД с анти-виндапом (clamping интегральной части).
  - `update(self, error, dt)`
  - `reset(self)`
- `ReactionWheel` — Маховик: ось (в СК корпуса), макс. момент, макс. кинет. момент.
  - `apply_torque(self, torque_body, dt)` — Запросить момент вдоль оси; вернуть фактический.
- `ReactionWheelArray` — Набор маховиков: распределение 3-осевого запроса по осям колёс.
  - `apply_torque(self, torque_body, dt)` — Спроецировать запрос на оси колёс (псевдоинверсия 3×N).
  - `total_momentum(self)`
  - `saturation_fraction(self)`
- `Spacecraft` — Жёсткий КА: инерции (диагональ), кватернион, ω, маховики.
  - `angular_momentum_total(self)` — H корпуса + H колёс (сохраняется без внешних моментов).
  - `derivatives(self, state, ext_torque, wheel_torque=(0.0, 0.0, 0.0))` — Правая часть: [ω̇, q̇] из уравнений Эйлера + кинематики.
- `AttitudePropagator` — Интегратор ориентации: RK4 по (ω, q) с перенормировкой q.
  - `step(self, ext_torque=(0.0, 0.0, 0.0))`

**Функции:**

- `slew_single_axis(sc, prop, target, kp=0.8, kd=2.2, max_time=60.0)` — Разворот к целевой ориентации (момент только колёсами).
- `self_check()` — 90° разворот сходится; |q| = 1; H сохраняется при свободном

### `lab/tides.py`

**Классы:**

- `TidalSystem` — Планета + спутник (или звезда + планета).
  - `orbital_period(self)`
  - `mu_primary(self)`

**Функции:**

- `tidal_bulge_height(ts, k2=0.3)` — Высота равновесного прилива: h ≈ (M_s/M_p)(R_p/a)³·k2·R_p.
- `tidal_potential_amplitude(ts)` — Амплитуда приливного потенциала на поверхности: GM_s R_p²/a³.
- `tidal_da_dt(ts, Q=12.0, k2=0.3)` — Скорость миграции орбиты из-за приливов в первичном теле.
- `synchronous_radius(ts, spin_period=86400.0)` — Радиус синхронной орбиты: a_sync = (GM_p·(T_spin/2π)²)^{1/3}.
- `moon_recession_check()` — Тест: Луна удаляется ~3.8 см/год (лазерная локация, LLR).
- `synchronization_timescale(ts, spin_period, k2=0.3, Q=100.0)` — t_sync по Гладману (1996): масштаб захвата в спин-орбитальный резонанс.
- `moon_lock_check()` — Луна захвачена; оценка времени захвата ~1e7–1e8 лет.
- `kozai_critical_inclination(retrograde=False)` — Критический наклон Козаи: i_crit из √(1−e²)cos i = const, e=0.
- `kozai_max_eccentricity(inclination_deg)` — Максимальный эксцентриситет цикла Козаи-Лидова.
- `kozai_timescale(a_inner, a_outer, M_central, M_perturber, e_outer=0.0)` — Характерное время циклов К-Л: t_KL ≈ n_out^{-1}·(M_c/M_p)(a_out/a_in)³(1−e²)^{3/2}.
- `kozai_example()` — Илон-Спутник-стиль пример: астероид под Юпитером.
- `tidal_heating(M_primary, M_satellite, R_satellite, a, e, k2=0.015, Q=100.0)` — Приливная мощность (ПВт/Вт): P = (21/2)·(k2/Q)·(G·M_p²·R_s^5·n·e²/a⁶).
- `io_heating_check()` — Ио: наблюдаемая приливная мощность ~10¹⁴ Вт (вулканизм).
- `self_check()` — Луна: 3.8 см/год (±допуск ×2); Ио: 10¹⁴ Вт (порядок); Козаи 39.23°.

### `lab/tissot.py`

**Классы:**

- `SmallBody` — Элементы малой планеты/кометы (а.е., градусы).

**Функции:**

- `tisserand(a, e, i_deg, a_planet=5.2038)` — Параметр Тиссерана относительно планеты (а.е.).
- `classify_jupiter(T_j)` — Динамический класс по T_J (Levison 1996, in: Completing the
- `halley_check()` — 1P/Галлея: T_J ≈ −0.61 (ретроградная, i>90° → cos i < 0).
- `jfc_check()` — 67P: T_J ≈ 2.75 — типичная комета семейства Юпитера.
- `encke_check()` — 2P/Энке: T_J ≈ 3.03 — «комета-астроид», на границе.
- `tisserand_under_pr(a0, t_pr_s, t_s, a_planet=5.2038)` — Эволюция Тиссерана пылинки под Пойнтингом-Робертсоном.
- `self_check()` — Формула подтверждена двумя независимыми фактами:

### `lab/trajectory.py`

**Классы:**

- `Trajectory` — Траектория: моменты времени × состояния тел.
  - `sample(self, t)` — Ближайшее состояние к моменту t (линейная интерполяция).
  - `positions_xy(self, body_index)`
  - `to_dict(self)`
  - `to_json(self, path)`
  - `to_csv(self, path)`
  - `from_dict(cls, d)`
- `TrajectoryPlanner` — Базовый планировщик: строит Trajectory по сцене/параметрам.
  - `plan(self, n_steps=500, dt=0.01, **params)` — Универсальная точка входа: перенаправляет на конкретный метод
  - `validate(self, traj)` — Предупреждения о траектории (NaN, разрывы, вылеты).
- `AnalyticPlanner` — Замкнутые формы: Теорема 3.1 (дышащее кольцо), Лагранж (жёсткий
  - `theorem31(self, C_Ch=1.0, T=2 * math.pi, n_steps=500, n_periods=1.0)`
  - `lagrange(self, side=1.0, gamma_total=3.0, n_steps=500, n_periods=1.0)` — Три равных вихря на равностороннем треугольнике; жёсткое вращение
  - `figure_eight(self, mass=1.0, G=1.0, n_steps=600, n_periods=1.0)`
- `KirchhoffPlanner` — Правильное N-кольцо вихрей: ω_N = Γ(N−1)/(4πR²).
  - `ring(self, N=5, R=1.0, gamma=1.0, n_steps=400, n_periods=1.0, jitter=0.0, seed=42)`
- `KeplerPlanner` — Задача двух тел: круговая или эллиптическая орбита.
  - `orbit(self, central_mass=1.989e+30, r0=149597870700.0, eccentricity=0.0, G=6.6743e-11, n_steps=500, n_periods=1.0)`
- `ScriptedPlanner` — Траектория из waypoints: каждый тел — список контрольных точек,
  - `waypoints(self, points_per_body, n_steps=400, duration=1.0, closed=True)`

**Функции:**

- `catmull_rom(p0, p1, p2, p3, t)` — Кубический сплайн Катмулла-Рома на чистом Python (без scipy).
- `get_planner(name)`

### `lab/trojan_points.py`

**Функции:**

- `rabe_mu(mu_ratio)` — Проверка критерия Рабе для массовой доли μ = m₂/(m₁+m₂).
- `libration_frequency(mu, orbital_period_years)` — Период длиннопериодической либрации (лет): T/√(27μ/4).
- `jupiter_trojans_check()` — Троянцы Юпитера: устойчивость, либрация ~150 лет, зона ±12°.
- `earth_trojans_check()` — Земные троянцы (2010 TK₇): μ Земли мала → устойчивость есть.
- `unstable_pair_check()` — Контрпример: пара с μ > 0.03852 → L4/L5 неустойчивы.
- `trojan_zone_report(l4_count=1.6, l5_count=1.0)` — Наблюдательное неравенство L4/L5 (Szabó 2007): L4 ≈ 1.6×L5.
- `self_check()` — Порог Рабе; Юпитер/Земля устойчивы; контрпример неустойчив;

### `lab/units.py`

**Функции:**

- `si_to_model(pos, vel, mass, time_scale=YEAR_S)`
- `model_to_si(pos, vel, mass, time_scale=YEAR_S)`
- `to_astronomical_units(meters)`
- `format_si(value, unit='м')` — Человекочитаемая запись с приставками СИ.

## Пакет `realism`

### `realism/almanac.py`

**Функции:**

- `moon_phase(age_days)` — Фаза Луны по возрасту цикла (0 = новолуние).
- `synodic_month_check()` — Два новолуния подряд: интервал = 29.530588 сут (определение).
- `elongation_to_phase(elongation_deg)` — Обратная задача: элонгация Луны от Солнца → возраст цикла (сут).
- `rise_set_hour_angle(dec_deg, lat_deg, horizon_deg=-0.833)` — Часовой угол восхода/захода (радианы); None — не восходит.
- `day_length_hours(dec_deg, lat_deg, horizon_deg=-0.833)` — Длительность светового дня (часы); None — полярный день/ночь.
- `is_polar_day(dec_deg, lat_deg)` — Полярный день: tan φ · tan δ > 1 (на полярном круге ровно 1).
- `is_polar_night(dec_deg, lat_deg)` — Полярная ночь: tan φ · tan δ < −1 (Солнце не встаёт).
- `twilight_hours(dec_deg, lat_deg, kind='civil')` — Длительность сумерек (часы) данного типа.
- `solar_declination(day_of_year)` — Склонение Солнца по дню года (грубая синус-модель).
- `equinox_day()` — День весеннего равноденствия (δ = 0 в марте): численно.
- `solstice_days()` — Дни солнцестояний (δ = ±ε).
- `self_check()` — Синодический месяц; полярный день на 90°; день 80 ≈ равноденствие;

### `realism/bright_stars.py`

**Классы:**

- `Star` — Яркая звезда (J2000, Hipparcos).

**Функции:**

- `find_brightest(ra_deg, dec_deg, radius_deg)` — Ярчайшая звезда в конусе (ra, dec, radius).
- `all_brighter_than(mag)`
- `is_circumpolar(star, lat_deg)` — Незаходящая звезда: tan φ · tan δ > 1 (см. realism.almanac).
- `is_never_visible(star, lat_deg)` — Невидимая с широты (никогда не восходит).
- `constellation_guess(star)` — Грубая привязка к созвездиям по RA-диапазонам (шутливая
- `self_check()` — Сириус ярчайшая; координаты сходятся с эфемеридными справками;

### `realism/cosmology.py`

**Функции:**

- `hubble_parameter(z, Omega_m=PLANCK18['Omega_m'], Omega_L=PLANCK18['Omega_L'], Omega_r=PLANCK18['Omega_r'], Omega_k=PLANCK18['Omega_k'])` — E(z) = H(z)/H₀ — безразмерный параметр расширения.
- `comoving_distance(z, **cosmo)` — Сопутствующее расстояние (Мпк): c/H₀·∫dz/E(z).
- `luminosity_distance(z, **cosmo)` — Световое расстояние (Мпк): d_L = (1+z)·d_C.
- `angular_diameter_distance(z, **cosmo)` — Угловое расстояние (Мпк): d_A = d_C/(1+z).
- `lookback_time(z, **cosmo)` — Время с момента z до сейчас (Гир): ∫dz/((1+z)E(z))/H₀.
- `age_of_universe(**cosmo)` — Возраст Вселенной (Гир): ∫dz/((1+z)E(z)) от 0 до ∞.
- `critical_density(z=0.0)` — Критическая плотность ρ_c = 3H(z)²/(8πG) в кг/м³.
- `hubble_law(d_mpc, H0=PLANCK18['H0'])` — Закон Хаббла: скорость убегания (км/с) на расстоянии d (Мпк).
- `deceleration_parameter(Omega_m=PLANCK18['Omega_m'], Omega_L=PLANCK18['Omega_L'], Omega_r=PLANCK18['Omega_r'])` — q₀ = Ωr + Ωm/2 − ΩΛ (при a=1).
- `hubble_tension_note()` — Честная справка о напряжении Хаббла (H0 Tension).
- `self_check()` — Planck-18: возраст 13.80 Gyr (±0.1); d_L(z=1) ≈ 6.69 Gpc (±0.1);

### `realism/eclipse_predictor.py`

**Функции:**

- `eclipse_year_days()` — Затменный год: 1/T = 1/T_троп + 1/T_узлов → 346.62 сут.
- `saros_days()` — Сарос: 223 синодических месяца (6585.32 сут).
- `eclipse_season_spacing()` — Интервал между затменными сезонами: половина затменного года.
- `shadow_cone_length(r_body_km, d_body_sun_km, r_sun_km=695700.0)` — Длина конуса тени: L = R_b·D/(R_s − R_b) (км).
- `moon_shadow_check()` — Тень Луны при среднем расстоянии: ~375 000 км.
- `eclipse_width_beta(kind='solar')` — Предельная широта Луны от узла для затмения (β-лимит, градусы).
- `upcoming_window(days_since_new_moon, beta_deg)` — Оценка окна затмения: фаза близка к новолунию и |β| в лимите.
- `self_check()` — Сарос точен; затменный год 346.62; сезон 173.31; тень Луны.

### `realism/encounter.py`

**Функции:**

- `flyby_turning_angle(v_inf_kms, rp_km, mu=MU_JUPITER_KM)` — Угол поворота v∞ (радианы): δ = 2·arcsin(1/(1+e)), e = 1 + rp·v∞²/μ.
- `flyby_delta_v(v_inf_kms, rp_km, mu=MU_JUPITER_KM)` — Максимальный прирост скорости от пролёта (км/с): Δv ≤ 2v∞sin(δ/2).
- `oberth_effect(v_peri_kms, dv_burn_kms)` — Oberth-эффект: burn на перицентре.
- `voyager_jupiter_example()` — Вояджер-2 у Юпитера: v∞ ≈ 10 км/с, r_p ≈ 721 570 км (10.3 R_J).
- `self_check()` — Физическая логика: мельче пролёт — больше поворот (монотонность);

### `realism/jpl_horizons.py`

**Функции:**

- `fetch_ephemeris(body_id, start, stop, step='1d', format='json', use_cache=True, timeout=30.0)` — Запросить вектор состояния тела из Horizons.
- `parse_vector_table(payload)` — Разобрать CSV VECTOR-блок ответа Horizons.
- `build_body_from_horizons(name, rows, at_index=0)` — Собрать Body лаборатории из строки эфемерид (м, м/с).
- `synthetic_circular_orbit(name, reference_date=None)` — Offline-замена: круговая орбита по средним элементам (J2000).
- `fetch_planets_today(names=None, use_cache=True)` — Собрать текущие векторы планет: онлайн Horizons или offline-режим.
- `self_check()` — Онлайн: Земля на ~1 а.е. от Солнца; offline: круговая орбита валидна.

### `realism/mission_design.py`

**Классы:**

- `Stage` — Ступень ракеты.

**Функции:**

- `hohmann_delta_v(r1_km, r2_km, mu=MU_SUN)` — Δv двухимпульсного гоманова перехода (км/с).
- `earth_to_mars_check()` — Классика: Земля→Марс Hohmann Δv ≈ 5.6 км/с, полёт ~259 сут.
- `launch_window_c3(r_earth_km=149600000.0, r_target_km=1.524 * 149600000.0, mu=MU_SUN)` — C3 = v∞² (км²/с²) на выходе из сферы действия Земли.
- `porkchop_grid(r_earth_km, r_target_km, launch_offsets_days, tof_days_list, phase_rate_deg_day, mu=MU_SUN)` — Матрица Δv (км/с) по (смещение вылета × время полёта).
- `tsiolkovsky(isp_s, mass_ratio)` — Δv ступени: Isp·g₀·ln(m₀/m_f) (м/с).
- `multi_stage_delta_v(stages)` — Суммарный Δv многоступенчатой ракеты (м/с).
- `delta_v_budget(dv_required_m_s, isp_s=450.0)` — Доля топлива: m_f/m₀ = exp(−Δv/(Isp·g₀)).
- `self_check()` — Гоманн Земля→Марс (5.6 км/с, 259 сут); Циолковский; C3.

### `realism/observatory.py`

**Классы:**

- `ObservatorySite` — Площадка: широта, долгота (вост. +), высота (м).
  - `lst(self, jd)` — Местное звёздное время (рад) на юлианскую дату.
- `ObservationTarget` — Цель наблюдения.
  - `alt_az(self, site, jd)`
- `VisibilityWindow` — Окно видимости цели (по сетке JD).
- `PlannedSlot` — Назначенный слот наблюдения.
- `SessionPlanner` — Жадный планировщик: цели по приоритету, слоты без пересечений.
  - `plan(self, targets)` — Назначить слоты: сортировка по (priority, −экспозиция).
  - `total_science_time_h(self)`
  - `conflicts(self)` — Пары слотов, пересекающихся по времени.

**Функции:**

- `airmass(alt_deg)` — Воздушная масса: X ≈ 1/sin(alt) (Rozenberg 1966).
- `airmass_kasten_young(alt_deg)` — Кастен-Янг (1989): X = 1/(sin h + 0.50572·(6.07995+h)^(−1.6364)).
- `simulate_photometry(counts_per_s, sky_per_s, exposure_s, read_noise=5.0, dark_per_s=0.01)` — SNR CCD-наблюдения: N√t/√(N t + B t + D t + R²).
- `visibility_scan(site, target, jd_start, jd_end, n_samples=200)` — Сканирование ночи: найти лучший непрерывный отрезок над min_alt.
- `self_check()` — Airmass монотонен; Кастен-Янг ≈ Rozenberg выше 30°; план без

### `realism/planetary_systems.py`

**Классы:**

- `PlanetLite` — Планета для архитектурного анализа.
  - `mu(self)`

**Функции:**

- `hill_radius(planet, m_star)` — r_H = a(1−e)(m/(3M))^{1/3}.
- `mutual_hill_separation(p1, p2, m_star)` — Δ = (a2−a1)/R_H,mut — разделение в взаимных сфер Хилла.
- `gladman_hill_stable(p1, p2, m_star)` — Критерий Гладмана (1993, Icarus 106, 247): пара устойчива, если
- `solar_system_hill_check()` — Все соседние пары Солнечной системы — Hill-устойчивы.
- `habitable_zone(m_star, L_star=None)` — ЗЖЗ по Kopparapu et al. 2013 (упрощённые коэффициенты).
- `pack_habitable_zone(m_star, planet_mass, spacing_hill=3.5, L_star=None)` — Сколько планет массы planet_mass помещается в ЗЖЗ звезды.
- `period_ratio(p1, p2, m_star)` — P2/P1 = (a2/a1)^{3/2}.
- `nearest_resonances(p1, p2, m_star, max_q=6)` — Ближайшие p:q-резонансы к отношению периодов (|Δ|<0.05).
- `resonance_width(p1, p2, m_star, p, q)` — Ширина резонанса p:q в единицах a (Murray & Dermott, упрощ.).
- `trappist_chain_check(semis_au, masses_earth, m_star)` — Проверка лапласовой цепочки TRAPPIST-1-подобной системы.
- `equilibrium_temperature(a_m, L_star, albedo=0.3, emissivity=1.0)` — T_eq = [L(1−A)/(16πεσa²)]^{1/4}.
- `insolation_in_earth_units(a_m, L_star)` — Инсоляция в единицах земной: S = (L/L☉)/(a/а.е.)².
- `trappist_like_hz_check()` — TRAPPIST-1e: T_eq ≈ 249 К (Gillon 2017, A=0), S ≈ 0.66 S⊕.
- `self_check()` — Солнечная система + TRAPPIST-1 + упаковка ЗЖЗ.

### `realism/sky_coordinates.py`

**Функции:**

- `parse_ra(text)` — '10h 23m 45.6s' | '10 23 45.6' | '10:23:45.6' → градусы.
- `parse_dec(text)` — '+12d 34m 56s' | '-12° 34′ 56″' | '+12 34 56' → градусы.
- `julian_date(dt)` — Юлианская дата (UTC); алгоритм Fliegel-Van Flandern.
- `gmst_radians(jd)` — Гринвичское среднее звёздное время (IAU 1982).
- `lst_radians(jd, longitude_deg)` — Местное звёздное время (восточная долгота +).
- `equatorial_to_ecliptic(ra_deg, dec_deg)` — Экваториальные → эклиптические (λ, β).
- `ecliptic_to_equatorial(lam_deg, beta_deg)` — Эклиптические → экваториальные (RA, Dec): обратный поворот R_x(−ε).
- `equatorial_to_horizontal(ra_deg, dec_deg, latitude_deg, lst_r)` — (RA, Dec) → (Az, Alt) для LST в радианах (Восток от севера).
- `angular_separation(ra1, dec1, ra2, dec2)` — Угловое расстояние (градусы) между двумя точками неба.
- `precess_ra_dec(ra_deg, dec_deg, jd)` — Прецессия координат от J2000 к эпохе jd (z-метод, точность ~1″).
- `rise_set_hour_angle(dec_deg, latitude_deg, horizon_deg=0.0)` — Часовой угол восхода (радианы); None — незаходящее/невосходящее.
- `is_circumpolar(dec_deg, latitude_deg)` — Незаходящее светило: |φ| + δ > 90° (северное полушарие).
- `self_check()` — Полюс → Alt=широта; экв.↔экл. roundtrip; Полярная циркумполярна.

### `realism/space_weather.py`

**Классы:**

- `SolarWindModel` — Режим солнечного ветра.
  - `dynamic_pressure_nPa(self)` — ρv² в нПа (1 nPa = 1e-9 Па).
  - `alfven_speed_kms(self)` — Альвеновская скорость: v_A = B/√(μ₀ρ).
  - `magnetopause_standoff(self)` — Подсолнечная точка магнитопаузы (Re): баланс давлений.
- `GeomagneticStorm` — Геомагнитная буря по шкале NOAA.
  - `category(self)`
  - `dst_estimate(self)` — Эмпирическая оценка Dst по Kp (Burton et al. 1975; грубо):

**Функции:**

- `parker_spiral_angle(r_au, v_sw_kms=400.0)` — Угол поля к радиусу: tan ψ = ω r / v (рад).
- `kp_to_ap(kp)` — Kp (0–9 в третьах) → Ap-эквивалент (USGS таблица).
- `daily_ap(kp_three_hourly)` — Суточный Ap: среднее восьми 3-часовых Ap.
- `cosmic_ray_cutoff_rigidity(lat_deg)` — Жёсткость обрезания ГКЛ: R_c ≈ 15·cos⁴λ ГВ (Smart & Shea 2008).
- `cosmic_ray_flux_ratio(lat_a, lat_b)` — Отношение потоков >R_cutoff: широты с меньшей R_c пропускают
- `flare_class(peak_watts_m2)` — Класс вспышки: A/B/C/M/X × 10-цепочка (GOES 1–8 Å).
- `self_check()` — Паркер ~45° у Земли; давление ветра ~1-3 нПа; Kp→Ap шкала;

### `realism/stellar.py`

**Классы:**

- `MainSequenceStar` — Звезда главной последовательности (параметризация по массе).
  - `luminosity(self)` — L/L☉: α=1.5 (M<0.43), 4 (0.43–2), 3.25 (2–20), 1 (M>55).
  - `radius(self)` — R/R☉: ~M^0.8 (M<1), ~M^0.57 (M>1).
  - `teff(self)` — T_eff = T☉·(L/R²)^{1/4}.
  - `main_sequence_lifetime_gyr(self)` — τ_MS ≈ 10·M/L Gyr (топливо/светимость), насыщение для малых M.
  - `spectral_class(self)`
  - `summary(self)`

**Функции:**

- `habets81(mass_solar)` — Соотношения Habets & Heintze (1981, A&AS 46, 193) для M<0.9.
- `roche_lobe_eggleton(q)` — Доля лба Роша (от разделения): Eggleton 1983, ApJ 268, 368.
- `mass_transfer_stability(q_donor, donor_convective=True)` — Устойчивость переноса массы по ζ-критерию (Hurley et al. 2002).
- `isochrone_age_gyr(L_solar, teff)` — Грубая оценка возраста по положению на ГП (ZAMS-метод).
- `skumanich_spin_down(age_gyr, saturation_gyr=0.1)` — Скорость вращения v ∝ t^{1/2} (Skumanich 1972).
- `gyrochrone_age(v_eq_kms)` — Обратная задача: возраст по скорости вращения (гирохронология).
- `self_check()` — Солнце: L=R=T=1; жизнь 10 Gyr; красный карлик — триллионы лет.

### `realism/tles.py`

**Классы:**

- `Tle` — Разобранный TLE.

**Функции:**

- `tle_epoch_jd(epoch_str)` — 'YYDDD.fraction' → JD (UTC). 57 → 1957-2057 по конвенции NORAD.
- `mean_motion_to_a(n_rev_day)` — n (об/сут) → большая полуось (км) по Кеплеру III.
- `orbital_period_minutes(n_rev_day)`
- `parse_tle(line1, line2, name='')` — Разбор TLE с валидацией контрольных сумм (ValueError при сбое).
- `make_tle(name, norad_id, epoch_yyddd, incl, raan, ecc, argp, mean_anom, n_motion, bstar=0.0, ndot=0.0, nddot=0.0)` — Собрать две строки TLE по спеке фиксированных колонок (68+контр.сумма).
- `propagate_keplerian(tle, dt_days)` — Кеплерово распространение средних элементов (упрощение SGP4).
- `self_check()` — Синтетический TLE: контрольные суммы, разбор, период ~92.9 мин.

### `realism/validator.py`

**Классы:**

- `Warning_` — Предупреждение валидации: severity = info|warn|error.

**Функции:**

- `validate_body(body, catalog_record=None)` — Проверка одного тела; при наличии записи каталога — сверка масс.
- `validate_scene(scene, catalog=None)` — Полная проверка сцены: тела, пересечения, скорости, вылеты.
- `is_physical(scene)` — True, если нет ошибок уровня error и N в допустимом диапазоне.
- `realism_report(scene, catalog=None)` — Сводка для HUD/отчётов: сколько тел сверено, предупреждения.

### `realism/data_fetchers/cache.py`

**Классы:**

- `TTLCache`
  - `put(self, key, data, ttl=None)`
  - `get(self, key, max_age=None)` — None, если записи нет или она протухла.
  - `get_stale(self, key)` — Запись без проверки свежести (fallback при недоступной сети).
  - `invalidate(self, key)`
  - `clear(self)`
  - `keys(self)`
  - `status(self)`

### `realism/data_fetchers/nasa_exoplanet.py`

**Функции:**

- `get_cache()`
- `build_query(limit)` — ADQL-запрос: ближайшие подтверждённые планеты.
- `fetch_confirmed_planets(limit=100, timeout=30.0, use_cache=True)` — Сырые строки TAP; при недоступной сети — последний кэш, иначе [].
- `validate_schema(rows)` — Проверка ожидаемых колонок в TAP-ответе.
- `to_body(record)` — TAP-строка → Body (масса кг, радиус м, орбита м).
- `fetch_bodies(limit=20)` — Удобная обёртка: сразу список Body.
- `nearest_systems(limit=15)` — Ближайшие планетные системы (для меню справки).

### `realism/data_fetchers/nasa_planetary.py`

**Функции:**

- `planetary_bodies()` — Солнце + 8 планет + 8 крупных лун как Body (радиусы в метрах).
- `update_cache(path=None)` — Опциональное обновление снимка факт-шита (сеть может быть закрыта —
- `fact_sheet_table()` — Таблица факт-шита для отчётов и меню.

### `realism/adapters/custom_adapter.py`

**Классы:**

- `CustomEngine` — Ньютоновская гравитация + пользовательское ускорение.
  - `name(self)`
  - `step(self, dt)`
  - `get_states(self)`
  - `energy(self)`
  - `to_dict(self)`

**Функции:**

- `compile_force(force_expr)` — Скомпилировать выражение ускорения ax, ay, az (или словарь).

### `realism/adapters/dedalus_adapter.py`

**Классы:**

- `DedalusAdapter` — Поле завихренности на сетке через Dedalus; fallback — нативные
  - `name(self)`
  - `step(self, dt)` — Движение тел по полю скоростей (квазистатическое приближение:
  - `get_states(self)`
  - `energy(self)`
  - `to_dict(self)`

**Функции:**

- `availability()`

### `realism/adapters/rebound_adapter.py`

**Классы:**

- `REBOUNDAdapter` — N-body через REBOUND (ias15 по умолчанию, whfast для скорости).
  - `name(self)`
  - `warmup(self)`
  - `step(self, dt)`
  - `get_states(self)`
  - `energy(self)`
  - `apply_states(self)`
  - `to_dict(self)` — Сериализация для воспроизводимости в отчётах.

**Функции:**

- `availability()` — Статус адаптера для HUD.

## Пакет `render`

### `render/animator.py`

**Классы:**

- `_LZWWriter` — Кодер GIF-LZW, побитно синхронный со стандартным декодером.
  - `compress(self, data)` — Кодер, зеркальный каноническому декодеру.

**Функции:**

- `build_palette()`
- `nearest_index(color)` — Ближший индекс палитры (быстрый: квантование 6-6-6 + перебор серых).
- `lzw_compress(data)` — Управляемая обёртка: корректный алгоритм GIF-LZW.
- `write_gif(path, frames, width, height, delay_cs=5, loop=0, palette=None)` — frames: список индексированных кадров (len = w*h, значения — индексы
- `frame_rgb_to_indices(pixels, width, height, bg=(13, 22, 40))` — RGB-кадр (w*h*3) → индексы палитры; фон квантуется в индекс 0.
- `animate_scene(scene, output, n_frames=48, fps=12, backend='pure', width=480, height=360, progress=True, format='gif')` — Анимировать историю сцены в GIF (собственный LZW) или MP4.

### `render/ascii_sky.py`

**Функции:**

- `stereographic_project(alt_deg, az_deg, k=1.0)` — (alt, az) → (x, y) в единицах радиуса карты (зенит = (0,0)).
- `visible_stars(lat_deg, lst_rad)` — Звёзды над горизонтом: (звезда, alt, az) для широты и LST.
- `constellation_lengths(lat_deg, lst_rad)` — Угловые длины линий созвездий (для проверки масштаба).
- `sky_map_ascii(lat_deg, lst_rad, width=41, height=21)` — ASCII-карта полусферы: стереографическая проекция, зенит в центре.
- `self_check()` — Зенит в центре; конформность: круг высоты 30° — окружность;

### `render/backend_ascii.py`

**Классы:**

- `AsciiCanvas` — Символьный кадр с z-буфером и цветом.
  - `plot(self, x, y, z, ch, color)`
  - `line(self, x0, y0, z0, x1, y1, z1, ch, color)` — Линия Брезенхэма с z-интерполяцией.
  - `to_lines(self, use_color=True)`

**Функции:**

- `render_ascii(bodies, width=78, height=28, trails=None, eye=None, target=(0.0, 0.0, 0.0), fov=50.0, use_color=True, axes=True)` — bodies: [{position, radius, color, label}]. Возвращает строки кадра.
- `print_ascii(lines, stream=None)`

### `render/backend_gl.py`

**Функции:**

- `availability()` — Статус для HUD.
- `sphere_mesh(radius, seg=24, rings=16)` — Вершины (x,y,z,nx,ny,nz) и индексы UV-сферы для GL.
- `render_gl(bodies, width=640, height=480, output='frame_gl.png', bg=(0.05, 0.09, 0.16))` — Рендер сфер через moderngl (offscreen) → PNG (через собственный кодер).

### `render/backend_mpl.py`

**Функции:**

- `plot_2d(traj, output, style='neon_dark', plane='xy', title='', dpi=150, body_names=None, body_colors=None)` — traj: lab.trajectory.Trajectory (или dict с times/states).
- `plot_3d(traj, output, style='neon_dark', title='', dpi=150, elev=22, azim=36, body_names=None, body_colors=None, sphere_scale=None)`
- `plot_4d(traj, w_values, output, style='neon_dark', title='', dpi=150, body_names=None)` — w_values[t][body] — четвёртая координата каждого тела в каждый момент.
- `plot_energy(times, energies, output, style='neon_dark', title='Сохранение энергии', dpi=150)`
- `plot_distances(traj, output, style='neon_dark', reference_index=0, dpi=150, names=None)` — Расстояния всех тел до опорного (индекс) по времени.
- `plot_havelock_scan(output, style='neon_dark', dpi=150)` — Иллюстрация порога Хавелока N≤7/N=8 (значения POLYVORTEX W4).

### `render/banners.py`

**Функции:**

- `title_bar(frame, title, width_frac=1.0)` — Титульная плашка сверху кадра: тёмная панель + золотой текст.
- `status_bar(frame, fraction, y=None)` — Полоса прогресса в кадре: заполнение ICE на тёмном треке.
- `legend(frame, bodies, x=6, y=16)` — Легенда тел: цветной квадратик + имя (латиницей, шрифт 5×7).
- `warn_banner(frame, text)` — Красная плашка предупреждения (N=8 и т.п.).
- `decorate_frame(frame, title, bodies, fraction=1.0, warn=None)` — Полный AURORA-декор кадра: титул + легенда + прогресс + плашка.

### `render/camera.py`

**Классы:**

- `OrbitCamera` — Камера на орбите вокруг цели.
  - `orbit(self, d_yaw, d_pitch)` — Повернуть орбиту (накапливается с плавностью).
  - `zoom(self, factor)` — Приблизить (factor<1) / отдалить (factor>1).
  - `pan(self, dx, dy)` — Сдвиг цели в плоскости экрана.
  - `update(self, dt)` — Сглаживание к целевым значениям (кадровая динамика).
  - `eye(self)` — Позиция камеры на орбите.
  - `view_params(self)` — Параметры для mat_look_at.
- `FollowCamera` — Слежение за движущимся телом со сглаживанием.
  - `update(self, dt, body_pos, body_vel)` — Обновить по позиции/скорости сопровождаемого тела.
  - `eye(self)`
- `CameraKey` — Ключевой кадр: позиция, цель, fov.
- `PathCamera` — Кинематографический пролёт по ключевым кадрам.
  - `sample(self, t)` — Состояние камеры в момент t (Катмулл-Ром по всем полям).
  - `duration(self)`
- `ShakeCamera` — Обёртка над любой камерой: затухающая случайная тряска.
  - `kick(self, strength)` — Импульс тряски (взрыв/удар).
  - `update(self, dt)`
  - `eye(self)`
  - `view_params(self)`

**Функции:**

- `cinematic_sequence(kind='flyby', radius=3.0)` — Готовые движения камеры (пресеты раскадровки).
- `self_check()` — Орбита держит дистанцию; путь проходит через ключи; тряска гаснет.

### `render/engine.py`

**Классы:**

- `RenderEngine` — Базовый движок рендера.
  - `setup(self, scene)`
  - `draw_frame(self, t)` — Нарисовать состояние на момент t; вернуть метаданные кадра.
  - `save_frame(self, path)`
  - `teardown(self)`
- `AsciiEngine` — Кадры в терминал и текстовые файлы (.txt с ANSI-цветами).
  - `setup(self, scene)`
  - `draw_frame(self, t)`
  - `save_frame(self, path)`
  - `print_frame(self)`
- `PureEngine` — Собственный программный 3D-рендер (png_codec + pure_raster).
  - `setup(self, scene)`
  - `draw_frame(self, t)`
  - `draw_4d(self, t, w_values)` — 4D-кадр: w кодируется свечением (смешение с фиолетовым).
  - `save_frame(self, path)`
- `MplEngine` — matplotlib: 2D-проекции, 3D-траектории, 4D-цветокодирование.
  - `setup(self, scene)`
  - `draw_frame(self, t)` — Кадр = 2D-срез на момент t (для анимаций); полный прогон —
  - `save_frame(self, path)`
  - `render_trajectory(self, output_dir, prefix='traj', mode='all')` — Построить 2D/3D/4D графики траектории сцены.
- `GLEngine`
  - `setup(self, scene)`
  - `draw_frame(self, t)`
  - `save_frame(self, path)`

**Функции:**

- `is_available(name)` — Проверка доступности бэкенда без его создания.
- `get_backend(name, config)` — Получить бэкенд; auto — каскад по доступности.
- `available_backends()`

### `render/font_5x7.py`

**Функции:**

- `draw_text(frame, x, y, text, color, scale=1)` — Нарисовать текст в кадр pure_raster. x,y — левый верхний угол.
- `text_width(text, scale=1)`

### `render/frame_compositor.py`

**Классы:**

- `Layer` — Слой кадра.
- `FrameComposer` — Композитор: стоп слоёв → итоговый кадр.
  - `add(self, layer)`
  - `compose(self)` — Наложить все слои на фон (в порядке z).

**Функции:**

- `solid_layer(name, w, h, color, z=0)` — Сплошной цвет.
- `body_layer(w, h, positions, radius_px=6, color=(79, 209, 197), z=10)` — Слой тел: круги в экранных координатах.
- `starfield_layer(w, h, n_stars=120, seed=5, z=-10)` — Слой звёздного фона (детерминированный хэш-рандом).
- `grid_layer(w, h, spacing=40, color=(35, 52, 74), z=-5)` — Слой координатной сетки.
- `vignette_layer(w, h, strength=0.4, z=50)` — Постэффект: затемнение краёв (multiply).
- `compose_to_png(compositor, path)` — Собрать кадр и сохранить PNG.
- `self_check()` — Аддитивное смешение не насыщается сверх 255; альфа 0.5 = полусумма;

### `render/hud.py`

**Классы:**

- `Spinner` — Символьный спиннер для неопределённых ожиданий.
  - `frame(self, elapsed=None)`
  - `step(self)`
- `Monitor` — Лёгкий системный монитор: /proc напрямую, psutil — опционально.
  - `cpu_pct(self)`
  - `ram(self)`
  - `temp_c()`
  - `inline(self)`
- `ProgressBar` — Однострочный динамический прогресс-бар (STDERR, репейнт через \r).
  - `update(self, value, tag='')`
  - `narrow(self, lo, hi, value, tag='')` — Диапазонная шкала (двухпроходные прогоны делят один бар).
  - `heartbeat(self)` — Прогресса нет, но время идёт — обновляем up/ETA в кадре.
  - `pause(self)`
  - `resume(self)`
  - `finish(self, message='')`
- `BarQueue` — Ограниченная очередь косметических кадров: замёрзший терминал
  - `put(self, fn)`
  - `start(self)`
  - `stop(self)`

**Функции:**

- `detect_color_mode(stream=None)` — Автоопределение возможностей терминала.
- `color_on()`
- `color_off()`
- `cyn(bold=False)`
- `grn(bold=False)`
- `red(bold=False)`
- `ylw(bold=False)`
- `mag(bold=False)`
- `blu(bold=False)`
- `gry(bold=False)`
- `wht(bold=False)`
- `org(bold=False)`
- `gold(bold=False)`
- `reset()`
- `colorize(text, rgb, bold=False)`
- `gradient_text(text, rgb_a, rgb_b)` — Позначная градиентная интерполяция цвета (баннер).
- `visible_width(s)`
- `pad_to(s, width)`
- `trunc_to(s, width)`
- `orn(width=72)` — Орнаментальная линия ✦—❄—✦.
- `hr(char='─', width=72)`
- `box(lines, title='', color=ICE, width=74)` — Рамочный бокс ╔═╗ вокруг уже готовых (может быть раскрашенных) строк.
- `banner(version='1.0.0', subtitle='')` — Баннер ACLL: truecolor-градиент лёд→золото, при Non-TTY — плоский.
- `print_banner(version='1.0.0', subtitle='', stream=None)`
- `verdict_icon(ok)`
- `warn_plate(text, width=74)` — Красная плашка (N=8 вне физической вселенной и т.п.).
- `kv(key, value, key_w=22)`
- `ctl_command(run_dir)` — Читает команды pause/resume/snapshot из <run_dir>/.tv_ctl.

### `render/particles.py`

**Классы:**

- `Particle`
- `EmitterConfig` — Настройки эмиттера.
- `ParticleSystem` — Контейнер частиц + обновление.
  - `emit(self, cfg)` — Выбросить cfg.rate частиц по режиму эмиттера.
  - `step(self, dt)` — Продвинуть все частицы; мёртвые удалить.
  - `alive_count(self)`
  - `total_energy(self)` — Суммарная кинетическая энергия (диагностика).

**Функции:**

- `fire_palette(life)` — Жёлтый → оранжевый → красный → тёмный по мере угасания.
- `plasma_palette(life)` — Белый → голубой → фиолетовый.
- `smoke_palette(life)` — Светло-серый → тёмный.
- `draw_particles(frame, ps, palette='fire', scale=40.0, size_scale=1.0)` — Нарисовать частицы в Frame (render.pure_raster.Frame), аддитивно.
- `render_frames(ps_list, width, height, palette='fire', bg=(13, 22, 40), paths=None)` — Сохранить последовательность кадров в PNG (возвращает размеры).
- `explosion(origin=(0.0, 0.0, 0.0), n=150, speed=2.0)` — Взрыв: изотропный выброс с гравитацией и drag.
- `comet_tail(comet_pos=(0.0, 0.0, 0.0), velocity=(-1.0, 0.0, 0.0))` — Хвост кометы: эмиттер против скорости + лёгкий отталкивание.
- `accretion_disk(center=(0.0, 0.0, 0.0), gm=3.0)` — Аккреционный диск: кольцо частиц с притяжением к центру.
- `jet(origin=(0.0, -0.5, 0.0), direction=(0.0, 1.0, 0.0))` — Релятивистский джет: конус вдоль направления.
- `self_check()` — Взрыв: частицы рождаются, живут, умирают; энергия падает с drag.

### `render/png_codec.py`

**Классы:**

- `_BitWriter`
  - `write_bits(self, value, count)`
  - `write_bits_rev(self, value, count)` — Huffman-коды пишутся MSB-first (перевёрнутые).
  - `flush(self, pad_bit=0)`
  - `bytes(self)`

**Функции:**

- `crc32(data, crc=0)`
- `adler32(data, a=1, b=0)`
- `deflate_fixed(data)` — DEFLATE-блок с fixed-Huffman (LZ77 с хэш-цепочкой, окно 32 КБ).
- `zlib_wrap(deflated, original=None)` — zlib-обёртка: заголовок 0x78 0x01 + adler32(ИСХОДНЫХ данных!).
- `write_png(path, pixels, width, height, alpha=False, level_filter=True)` — Записать PNG. pixels — плоский список/bytes RGB(A): len = w*h*bpp.
- `write_ppm(path, pixels, width, height)` — PPM P6 — дешёвый растровый вывод без кодирования.

### `render/pure_raster.py`

**Классы:**

- `Frame` — RGB-кадр с z-буфером.
  - `clear(self)`
  - `set_pixel(self, x, y, z, color)`
  - `draw_line(self, x0, y0, x1, y1, color, z=0.0)` — Линия Брезенхэма.
  - `shade(self, normal, base, light_dir, ambient=0.25, specular=0.0, view_dir=(0.0, 0.0, 1.0))` — Ламберт + ambient (+ Блинн-Фонг опционально).
  - `draw_triangle(self, p0, p1, p2, c0, c1, c2)` — Вершины в экранных координатах (x, y, z-глубина).
  - `save_png(self, path)`
  - `save_ppm(self, path)`

**Функции:**

- `mat_identity()`
- `mat_mul(a, b)`
- `mat_translate(tx, ty, tz)`
- `mat_scale(sx, sy, sz)`
- `mat_rotate_x(deg)`
- `mat_rotate_y(deg)`
- `mat_rotate_z(deg)`
- `mat_look_at(eye, target, up)` — Видовая матрица (правосторонняя, смотрим вдоль -z).
- `mat_perspective(fov_y_deg, aspect, near, far)` — Перспективная проекция (OpenGL-стиль, z в [-1,1]).
- `mat_apply(m, v)`
- `uv_sphere(radius, seg=12, rings=8)` — Вершины и треугольники UV-сферы (полюса по y).
- `render_bodies(bodies_state, width=320, height=240, trails=None, eye=None, target=(0.0, 0.0, 0.0), fov=50.0, seg=10, rings=6, bg=(13, 22, 40), show_axes=True, title='')` — bodies_state: [{position: (x,y,z), radius: float, color: '#rrggbb',

### `render/raytracer.py`

**Классы:**

- `Sphere`
- `Plane` — Бесконечная плоскость y = height (шахматная клетка).
- `Light`
- `Camera`
- `RaytraceScene`
- `Hit`

**Функции:**

- `v_add(a, b)`
- `v_sub(a, b)`
- `v_scale(a, s)`
- `v_dot(a, b)`
- `v_cross(a, b)`
- `v_norm(a)`
- `v_reflect(d, n)` — Отражение падающего направления d от нормали n.
- `hit_sphere(origin, direction, s)` — Ближайший положительный t пересечения луча со сферой (или None).
- `hit_plane(origin, direction, p)` — Пересечение с y = p.height (только сверху или снизу — любое).
- `nearest_hit(origin, direction, scene)`
- `in_shadow(point, light, scene)` — Есть ли объект между точкой и источником.
- `shade(hit, direction, scene, depth, max_bounce=3)` — Освещение точки + рекурсивные отражения.
- `render(scene, camera, width, height, antialias=1, gamma=2.2, tonemap=True)` — Кадр RGB (bytes) размером width×height×3.
- `render_to_png(scene, camera, path, width=160, height=120, antialias=1)` — Отрендерить и сохранить PNG (собственный кодер).
- `demo_scene()` — Классическая сцена: 3 сферы (матовая/глянцевая/зеркало) + пол.
- `solar_scene()` — Солнце (излучающая) + планеты (матовые) — стилизация.
- `self_check()` — Рендер демо-сцены: непустой кадр, тени есть, файл валиден.

### `render/spectrum.py`

**Функции:**

- `planck_curve(T, wavelengths_nm)` — B_λ(λ, T) в Вт/м²/ср/нм (вход нм → перевод в СИ внутри).
- `wien_peak(T)` — Длина волны максимума излучения (нм).
- `cie_xyz(lam_nm)` — Функции сложения цветов x̄, ȳ, z̄ на длине волны λ (нм).
- `blackbody_rgb(T)` — Цвет чёрного тела: B_λ × CIE → XYZ → sRGB (0..1), нормировка по max.
- `spectral_class_color(cls)` — RGB цвет звезды спектрального класса O–M.
- `rgb_to_hex(rgb)` — RGB 0..1 → '#RRGGBB'.
- `self_check()` — Солнце — белый; M-карлик красный (r−b > 0.2); O — голубой (b−r > 0.15);

## Пакет `reports`

### `reports/bibliography.py`

**Функции:**

- `load_entries()` — [(номер, текст, url)] — по строкам вида «N. **...**».
- `as_table_rows()` — Строки для ReportData.add_table.
- `count()`

### `reports/charts.py`

**Функции:**

- `summary_bar(values, labels, output, title='', style='neon_dark', ylabel='')` — Столбчатая сводка (например, метрики по телам).
- `ascii_table(headers, rows, widths=None)` — Текстовая таблица с рамками (fallback без matplotlib).
- `correlation_heatmap(matrix, labels, output, title='Корреляции метрик', style='neon_dark')`

### `reports/engine.py`

**Классы:**

- `ReportData` — Всё, что попадает в отчёты: сцена, метрики, графики, генеалогия.
  - `add_card(self, key, value, cls='info')`
  - `add_table(self, name, headers, rows)`
  - `add_chart(self, path, caption='')`
  - `fill_from_scene(self)`
  - `to_dict(self)`

**Функции:**

- `write_txt(data, path)`
- `write_md(data, path)`
- `write_html(data, path, theme='aurora')`
- `write_csv(data, path)`
- `write_json(data, path)`
- `write_docx(data, path)`
- `write_pdf(data, path)`
- `write_odt(data, path)` — Отчёт ODT (OpenDocument): cards, таблицы, секции — как в docx.
- `generate_reports(data, output_dir, formats=None, theme='aurora', stem='report')` — Сгенерировать отчёт во всех запрошенных форматах.
- `validate_outputs(written)` — Проверка файлов: существование, размер, валидность docx/pdf.

### `reports/templates.py`

**Функции:**

- `html_table(headers, rows, classes=None)`
- `html_cards(items)` — items: [(ключ, значение, css-класс good/warn/bad/info)].
- `html_section(heading, content)`
- `html_image(png_path, alt='график')`
- `html_page(title, subtitle, body, theme='aurora', version='1.0.0', banner='')`
- `html_plate(title, text)` — Красная плашка (N=8 вне физической вселенной и т.п.).

### `reports/writers/docx_writer.py`

**Классы:**

- `DocxBuilder` — Сборка документа: абзацы, заголовки, таблицы, картинки.
  - `heading(self, text, level=1)`
  - `paragraph(self, text, bold=False, italic=False, color=None, size_half_pt=22)`
  - `bullet(self, text)`
  - `table(self, headers, rows, widths=None)` — Таблица с заливкой шапки и зеброй строк.
  - `image(self, png_path, width_emu=5200000)` — Вставить PNG. width_emu — ширина в EMU (914400 = 1 дюйм).
  - `spacer(self)`
  - `save(self, path)`

**Функции:**

- `validate_docx(path)` — Проверка структуры: zip-целостность + обязательные части.

### `reports/writers/odt_writer.py`

**Классы:**

- `OdtBuilder` — Сборка ODT-документа: заголовки, абзацы, списки, таблицы.
  - `heading(self, text, level=1)`
  - `paragraph(self, text, style='Standard')`
  - `bullet(self, text)`
  - `table(self, header, rows)` — Таблица с шапкой; числа форматируются как строки.
  - `save(self, path)` — Сохранить .odt; mimetype — первая запись БЕЗ сжатия (спека).

**Функции:**

- `validate_odt(path)` — Структурная валидация: mimetype первым и без сжатия + XML.
- `self_check()` — Собрать документ с таблицей и заголовками, валидировать.

### `reports/writers/pdf_writer.py`

**Классы:**

- `_Page`
  - `text(self, x, y, s, size=10.5, bold=False, color=DARK)`
  - `text_right(self, x_right, y, s, size=10.5, bold=False, color=DARK)`
  - `heading(self, text, y, level=1)` — Заголовок с полосой-акцентом; возвращает новую позицию y.
  - `rect(self, x, y, w, h, fill=None, stroke=None)`
  - `line(self, x0, y0, x1, y1, color=GREY, width=0.6)`
  - `table(self, headers, rows, y, x=56, col_w=None, font_size=8.5)`
  - `wrap_text(self, text, x, y, width_chars=92, size=10, color=DARK, line_gap=13.5)` — Абзац с переносом по словам; возвращает новый y.
- `PDFBuilder`
  - `page(self)`
  - `new_page(self)`
  - `save(self, path)`

**Функции:**

- `translit(text)`
- `validate_pdf(path)` — Проверка: заголовок, xref, EOF.

### `reports/writers/pptx_writer.py`

**Классы:**

- `SlideBuilder` — Один слайд: список шейпов (текст/картинка).
  - `title(self, text, subtitle='')`
  - `bullets(self, items, start_y=3200000, size=1600)`
  - `image(self, png_path, x=1800000, y=2600000, width=8500000)` — Вставить PNG по пути: media-часть + rel.
  - `caption(self, text, y=SLIDE_H - 800000)`
  - `note(self, text)`
- `PptxBuilder` — Сборка презентации: слайды, мастер, тема, сохранение.
  - `slide(self, layout=1)`
  - `save(self, path)`

**Функции:**

- `validate_pptx(path)` — Структурная валидация PPTX.
- `self_check()` — Собрать 3-слайдовую презентацию и валидировать (pptx при наличии).

### `reports/writers/xlsx_writer.py`

**Классы:**

- `Worksheet` — Один лист: сетка ячеек + параметры.
  - `header(self, values)`
  - `row(self, values, style='normal', fmt=None)`
  - `formula_row(self, formulas, style='normal')`
  - `autosize(self, samples=200)` — Оценить ширины столбцов по содержимому.
  - `to_xml(self)`
- `XlsxBuilder` — Сборка книги: листы, стили, сохранение.
  - `sheet(self, name, freeze_header=True)`
  - `save(self, path)`

**Функции:**

- `validate_xlsx(path)` — Структурная валидация (zip + обязательные части + parse XML).
- `self_check()` — Собрать книгу, валидировать, прочитать openpyxl (если есть).
