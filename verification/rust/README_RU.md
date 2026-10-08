# TRIVORTEX — числовой двойник на Rust (веха M1)

> Русскоязычный обзор. Полный документ — в [README.md](README.md).

**Статус: реализовано — v1.1.** Крейт `trivortex-verify` — построчный
f64-порт лестницы верификации V1–V4 (`verify.py`) без единой внешней
зависимости: путь с плавающей точкой — ровно платформенный.

## Состав

- `src/verify.rs` — ядро-двойник (аналитический слой, уравнения
  Кирхгофа, RK4, четыре проверки, JSON-совместимое дерево значений);
- `src/main.rs` — интерактивная лаборатория `trivortex-lab`:
  пресеты, свои параметры, исследование сходимости, экспорт
  JSON/CSV/SVG, двуязычный интерфейс (EN/RU);
- `src/report.rs` — JSON-протокол, CSV и векторные SVG-графики
  (без зависимостей);
- `src/i18n.rs` — двуязычные строки;
- `tests/ladder.rs` — интеграционные тесты;
- `protocol_quick.json` — эталонный протокол реального запуска.

## Проверено локально

`cargo test` — 14/14: опорные значения ω = 1.3748022274393588,
ε, ω_Лагранж = 3/(2π), форма Чаплыгина, модуль-ветки python_mod,
быстрая лестница 4/4; дрейфы инвариантов V4 совпали с Python
бит-в-бит в напечатанном представлении.

## Запуск

```bash
cargo test --release --manifest-path verification/rust/Cargo.toml
cargo run --release --manifest-path verification/rust/Cargo.toml          # меню
cargo run --release --manifest-path verification/rust/Cargo.toml -- \
    --preset quick --no-menu --lang ru --plots --csv                       # CI
```

CI: `verification-ports.yml`, задание *rust-numeric-twin* (non-blocking).
