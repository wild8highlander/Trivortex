<!-- markdownlint-disable-file MD041 -->
<div align="center">

# 🧰 verification · common — Shared Python Utilities

</div>

> **Navigation:** [`verification`](../README.md) › **`common`**

![Python](https://img.shields.io/badge/Python-3.10%E2%80%933.12-informational?style=flat-square&logo=python&logoColor=white) ![Type](https://img.shields.io/badge/Type-Python%20package-informational?style=flat-square&logo=python&logoColor=white) ![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)

The **shared utility layer** of the Python side of the framework: the pieces that every composed TRIVORTEX verification front-end reuses instead of re-implementing. `python/verifier_base.py` defines the common verifier behaviour — the template method `verify()` that times a section's `run_verification()` and `compute_metrics()` calls and returns a `results / metrics / elapsed` dict, so all front-ends speak the same output contract as the standalone ports; `config.py` centralises the presets and the section registry; `main.py` provides the CLI entry point; `__init__.py` marks the package surface.

The layer is intentionally tiny (2 162 B across its four modules, pure standard library) and matches the framework's "no hidden dependencies" rule. The working ladder in [`trivortex/python/`](../trivortex/README.md) is single-file by design and does **not** import it — the independence of the checker from shared helpers is the whole point (see [§1 of the framework hub](../README.md#1-what-this-framework-is-for)); this layer exists for composed front-ends and future sections that want the shared protocol.

## 📂 Contents — What Lives Here

| File | Size | Description |
|---|---|---|
| [`python/`](python/README.md) | — | the package itself — 4 modules, 2 162 B: base verifier, config, CLI, package marker |

## 🗂 Directory Layout

```text
common/
├── python/            # the utility package (4 modules + its own README)
│   ├── __init__.py        48 B   package marker
│   ├── config.py         745 B   presets + section registry
│   ├── main.py           621 B   CLI entry point
│   ├── verifier_base.py  748 B   BaseVerifier template class
│   └── README.md         (module-level guide)
└── README.md          (this file)
```

## ▶️ How to Run

The sanity entry of the kept package (the `make common` target of the
[verification Makefile](../Makefile)):

```bash
cd verification
python3 common/python/main.py --section 1 --preset default
```

prints the section name, the preset and the resolved configuration —
the shared-protocol sanity check quoted in [§9 of the hub](../README.md#9-how-to-reproduce-everything).

## ✅ What This Layer Guarantees

- a **uniform output contract**: every front-end built on `BaseVerifier`
  reports `results`, `metrics` and `elapsed` from one timed `verify()`
  call — the same "bound to a run" discipline as the JSON protocols;
- a **registered preset table**: `quick` / `default` / `full` /
  `extreme` with explicit `N`, `tolerance`, `max_iter` — no unnamed
  magic numbers;
- a **section registry**: sections 1–4 are named after the checked
  objects of the document (Theorem 3.1 closed form, the Chaplygin
  integral, Lagrange rigid rotation, the vortex integrals `H, P, Q, I`).

## 🔗 Cross-References

- [Framework root — verification/](../README.md)
- [Package detail — common/python/](python/README.md)
- [Working ladder — trivortex/](../trivortex/README.md)
- [Lean 4 hub — the formalization this protocol feeds](../lean4/README.md)

## 🇷🇺 Краткое резюме (Russian Summary)

**verification/common/** — общий слой утилит Python-стороны: базовый класс верификатора (`verifier_base.py`: шаблонный метод `verify()` с таймером, возвращает `results / metrics / elapsed`), конфиг (`config.py`: пресеты `quick/default/full/extreme` и реестр разделов 1–4), CLI-агрегатор (`main.py`) и маркер пакета (`__init__.py`). Всего 2 162 B, чистая стандартная библиотека. Рабочая лестница `trivortex/python/` сознательно однофайловая и этот пакет не импортирует — независимость проверяющего кода превыше повторного использования.

---

<div align="center">

**[⬆ Back to top](#-verification--common--shared-python-utilities)** ·
**[Repository root](../README.md)**

*Part of [wild8highlander/Trivortex](https://github.com/wild8highlander/Trivortex) · Licensed under [IPL-RP-1.0](https://github.com/wild8highlander/Trivortex/blob/main/LICENSE.md) — All Rights Reserved*

</div>
