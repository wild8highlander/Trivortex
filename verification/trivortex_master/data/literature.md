# TRIVORTEX MASTER — список литературы и источников данных

Каждый объект `data/catalog.json` ссылается на источник полем `source`.
Ниже — аннотированный перечень всех источников плана и каталога.

## Ядро Trivortex (наследуемый репозиторий)

1. **Isaev I. Kh. TRIVORTEX — The Three-Body (and N-Body) Problem in the
   Vortex Model, v1.0–1.1 (2026).** Ядро: `code/trivortex_core_en.py`,
   22 секции; Теорема 3.1 (замкнутая форма), топологический интеграл
   Чаплыгина, RMT-анализ, квантовый блок.
   <https://github.com/wild8highlander/Trivortex>
2. **Isaev I. Kh. Verification ladder V1–V4.**
   `verification/trivortex/python/verify.py` — независимая проверка Теоремы 3.1:
   хореография 2π/3 (остаток 6.9e-14), периодичность (9.4e-14), сохранение
   интегралов H, P, Q, I (2.9e-14). JSON-протоколы каждого прогона.
   <https://github.com/wild8highlander/Trivortex/tree/main/verification>
3. **Isaev I. Kh. POLYVORTEX — N-vortex bench, W-ladder W1–W7.**
   Порог Хевелока N ≤ 7 устойчиво / N ≥ 8 неустойчиво (стадия W4,
   max Re λ = +0.4502 при N=8); граница допустимости C_Ch > π·ln 2 (W5);
   ω_N = Γ(N−1)/(4πR²) (W2). Обоснование лимита тел 3–7 в TRIVORTEX MASTER.
   <https://github.com/wild8highlander/Trivortex/tree/main/polyvortex>
4. **Isaev I. Kh. CYCLORING.** Γ-периоды правильного кольца, W1–W7, 37 тестов.
   <https://github.com/wild8highlander/Trivortex/tree/main/cycloring>
5. **Isaev I. Kh. PLANETVORTEX.** PSL(2,7)-гравифигура Солнечной системы,
   Кеплер III с точностью 6.2e-13, прецессия Меркурия 42.982″/век (X6).
   <https://github.com/wild8highlander/Trivortex/tree/main/planetvortex>
6. **Isaev I. Kh. Research program TRX-01…TRX-12.** Двенадцать спутных
   исследований: лазерное давление, трёхволновое смешение, солитонные
   молекулы, фотонная жидкость, оптические вихри, гелий, эффект Эфимова,
   ионная ловушка, вихревое трио, Козаи–Лидов, ГВ-хореография, лазерный парус.
   <https://github.com/wild8highlander/Trivortex/tree/main/research>

## Физические движки (опциональные)

7. **Rein H., Liu S.-F. REBOUND: an open-source multi-purpose N-body code
   for collisional dynamics.** Astronomy & Astrophysics 537, A128 (2012).
   DOI: 10.1051/0004-6361/201118085. Интеграторы IAS15
   (Rein & Spiegel 2015, MNRAS 446, 1424), WHFast (Rein & Tamayo 2015),
   MERCURIUS. Лицензия GPL-3.0. <https://github.com/hannorein/rebound>
8. **Burns K. J., Vasil G. M., Oishi J. S., Lecoanet D., Brown B. P.
   Dedalus: A Flexible Framework for Numerically Solving Partial Differential
   Equations.** Physical Review Research 2, 023068 (2020).
   DOI: 10.1103/PhysRevResearch.2.023068.
   <https://github.com/DedalusProject/dedalus>

## Данные

9. **NASA Exoplanet Archive. Planetary Systems (ps) table.** TAP-сервис
   (sync/async), форматы VOTable/CSV/JSON. Источник экзопланетной части
   каталога; снимок кэшируется в `data/cache/exoplanets_<дата>.json`.
   <https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html>
10. **NASA NSSDC Planetary Fact Sheets.** Массы, радиусы, орбитальные
    параметры планет и их спутников.
    <https://nssdc.gsfc.nasa.gov/planetary/factsheet/>
11. **NASA NSSDC Asteroid / Comet Fact Sheets.**
    <https://nssdc.gsfc.nasa.gov/planetary/factsheet/asteroidfact.html>,
    <https://nssdc.gsfc.nasa.gov/planetary/factsheet/cometfact.html>
12. **SIMBAD astronomical database (CDS).** Параметры ближайших звёзд.
    <https://simbad.cds.unistra.fr/simbad/>
13. **JPL Small-Body Database Lookup.** Параметры астероидов.
    <https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html>

## Классика небесной механики и вихревой динамики

14. **Lagrange J. L. Essai sur le problème des trois corps.** Œuvres t. 6
    (1772). Равностороннее решение — основа Теоремы 3.1.
15. **Havelock T. H. The stability of motion of rectilinear vortices
    (ring of vortices).** Philosophical Magazine 11, 617–633 (1931).
    Классификация устойчивости N-вихревого кольца: порог N = 7/8.
16. **Chenciner A., Montgomery R. A remarkable periodic solution of the
    three-body problem in the case of equal masses.** Annals of Mathematics
    152, 881–901 (2000). DOI: 10.2307/2661357. Figure-eight хореография —
    пресет планировщика AnalyticPlanner.
17. **Aref H. Point vortex dynamics: a classical mathematics playground.**
    Journal of Mathematical Physics 48, 065401 (2007).
    DOI: 10.1063/1.2425100. Интегралы Кирхгофа H, P, Q, I.
18. **Šuvakov M., Dmitrašinović V. Three Classes of Newtonian Three-Body
    Planar Periodic Orbits.** PRL 110, 114301 (2013).
    DOI: 10.1103/PhysRevLett.110.114301. Атлас хореографий:
    бабочка, пряжа, очки и др.
19. **Murray C. D., Dermott S. F. Solar System Dynamics.** Cambridge
    University Press (1999). Возмущения, резонансы, механизм Козаи–Лидова.
20. **Chaplygin S. A. Об одном случае вихревого движения в жидкости.**
    Труды Отделения Физических Наук ОЛЕ (1903). Топологический интеграл.

## Прототип интерфейса

21. **AB-CLOUD Verification Suite · AURORA Edition (приложение к плану).**
    Прототип визуального языка: модули ABUI (truecolor ANSI, градиенты),
    ABMon (системный монитор из /proc), однострочный динамический
    прогресс-бар с EMA-ETA и очередью кадров, байтовые писатели
    PNG/GIF89a/PDF/DOCX на stdlib (собственные DEFLATE и LZW).
