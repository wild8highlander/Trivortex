# TRIVORTEX — порт на C++17 с бенчмарком -O2 (веха M3)

> Русскоязычный обзор. Полный документ — в [README.md](README.md).

**Статус: реализовано — v1.1.** CMake/CTest-порт лестницы V1–V4 без
зависимостей плюс измерение производительности, ради которого и была
запланирована веха M3.

## Состав

- `src/verify.hpp` / `src/verify.cpp` — ядро-двойник (те же формулы и
  допуски, что в `verify.py`); дерево значений JSON, писатели CSV/SVG;
- `src/main.cpp` — интерактивная лаборатория `trivortex-lab` (EN/RU):
  пресеты, свои параметры, исследование сходимости, экспорт графиков;
- `src/tests.cpp` — защита CTest из 21 утверждения (опорные значения
  «pinned, not assumed»);
- `CMakeLists.txt` — Release/-O2, цель `trivortex-tests` для CTest;
- `protocol_quick.json` — эталонный протокол реального запуска.

## Проверено локально

g++ 14.2 (-O2 -Wall -Wextra): все 21 утверждения защиты прошли,
включая пин ω = 0.477464829275686; бенчмарк ≈ 1.7·10⁷ вычислений
правой части RK4 в секунду.

## Запуск

```bash
cmake -S verification/cpp -B verification/cpp/build -DCMAKE_BUILD_TYPE=Release
cmake --build verification/cpp/build -j
ctest --test-dir verification/cpp/build --output-on-failure
./verification/cpp/build/trivortex-lab        # интерактивное меню
```

CI: `verification-ports.yml`, задание *cpp-ctest* (non-blocking).
