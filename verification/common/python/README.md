# 🧰 common · python — the Utility Package

> **Navigation:** [`verification`](../../README.md) › [`common`](../README.md) › **`python`**

![Python](https://img.shields.io/badge/Python-3.10–3.12-informational?style=flat-square&logo=python&logoColor=white) ![License](https://img.shields.io/badge/License-IPL--RP--1.0-red?style=flat-square)

The **utility package** itself: four modules totalling ~2 KB. `verifier_base.py` (the heart) implements the shared verifier protocol; `config.py` the settings; `main.py` the aggregate CLI; `__init__.py` the exports. The shared protocol for the TRIVORTEX verification sections — the working ladder in [`trivortex/`](../../trivortex/README.md) and every future language port.

## 📂 Contents — What Lives Here

| File | Size | Description |
|---|---|---|
| [`__init__.py`](__init__.py) | 48 B | package exports |
| [`config.py`](config.py) | 766 B | central configuration — section paths, tolerances, output options |
| [`main.py`](main.py) | 617 B | aggregate CLI — runs multiple sections through the shared base |
| [`verifier_base.py`](verifier_base.py) | 714 B | base verifier class — banner, assertion ledger, JSON verdict emission |

## 🔗 Cross-References

- [Framework root — verification/](../../README.md)
- [Working ladder — trivortex/](../../trivortex/README.md)

## 🇷🇺 Краткое резюме (Russian Summary)

Пакет утилит: verifier_base (протокол верификатора), config, main (агрегатор CLI), **init**.

---

<div align="center">

**[⬆ Back to top](#-common--python--the-utility-package)** ·
**[Repository root](../../README.md)**

*Part of [wild8highlander/research-papers](https://github.com/wild8highlander/research-papers) · Licensed under [IPL-RP-1.0](https://github.com/wild8highlander/research-papers/blob/main/LICENSE.md) — All Rights Reserved*

</div>
