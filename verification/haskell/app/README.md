<!-- markdownlint-disable-file MD041 -->
<div align="center">

# 🚪 The CLI Entry Point of the Haskell Port

![Haskell](https://img.shields.io/badge/Haskell-GHC%209.4-5E5061?style=flat-square&logo=haskell&logoColor=white)
![Type](https://img.shields.io/badge/Type-executable-2496ED?style=flat-square)
![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)

</div>

> **Navigation:** [`verification`](../../README.md) › [`haskell`](../README.md) › **`app`**

[`Main.hs`](Main.hs) — the executable `trivortex-lab` of the dual
(`Double` + exact ℚ(√3)) verification ladder: preset selection, the
V1–V4 registers, the bilingual report and the JSON protocol output.

## 📂 The File

| File | Size | Lines | Role |
|---|---|---|---|
| [`Main.hs`](Main.hs) | 12 277 B | 250 | the CLI entry point: the interactive menu (presets `quick` / `default` / `full` or custom parameters), the exact-rational dual, a convergence study, SVG/CSV/JSON export, the bilingual (EN/RU) interface; suite name `trivortex-verification-haskell`, default output directory `verification/outputs/haskell` |

## 🧭 The Module It Serves

All logic lives in the library module
[`../src/Trivortex/Verify.hs`](../src/Trivortex/Verify.hs); the entry
point only parses arguments, runs the ladder and renders the results.
The design contract — thin CLI, testable library — mirrors the other
language ports (the C++ `main.cpp` and the Rust `main.rs` follow the
same split). The executable the menu drives is pinned by the guard suite
[`../test/Ladder.hs`](../test/Ladder.hs).

## 🚀 Build and Run

```bash
cabal run -- --preset quick     # from verification/haskell/
echo 0 | cabal run trivortex-lab   # the interactive menu
```

or inside the pinned Docker toolchain
([`../../docker/haskell/`](../../docker/haskell/), image
`haskell:9.4-slim`). The Makefile targets are `make haskell` and
`make haskell-lab` (from `verification/`).

## 🔗 Cross-References

- [Haskell port overview](../README.md) — the dual ladder and its milestones
- [Library sources](../src/README.md) — where the logic lives
- [Guard suite](../test/README.md) — the suite that pins this executable
- [Verification framework](../../README.md) — tolerance bands, protocol schema
- [Lean 4 hub](../../lean4/README.md) — the statement layer behind the registers

## 🇷🇺 Краткое резюме (Russian Summary)

- `app/Main.hs` — исполняемый `trivortex-lab` двойной лестницы
  (`Double` + точный ℚ(√3)): пресеты, регистры V1–V4, двуязычный отчёт,
  JSON-протокол;
- тонкий CLI, проверяемая библиотека: вся логика — в
  `src/Trivortex/Verify.hs`, точка входа только парсит аргументы и
  рендерит результаты;
- меню: пресеты quick / default / full и свои параметры, точный dual,
  исследование сходимости, экспорт SVG/CSV/JSON, языки EN/RU;
- протоколы пишутся в `verification/outputs/haskell`; исполняемый пиннится
  защитным набором `test/Ladder.hs`.

---

<div align="center">

**[⬆ Back to top](#-the-cli-entry-point-of-the-haskell-port)** ·
**[Repository root](../../../README.md)**

*Part of [wild8highlander/Trivortex](https://github.com/wild8highlander/Trivortex) · Licensed under [IPL-RP-1.0](https://github.com/wild8highlander/Trivortex/blob/main/LICENSE.md) — All Rights Reserved*

</div>
