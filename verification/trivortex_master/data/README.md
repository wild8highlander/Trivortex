<!-- markdownlint-disable-file MD041 -->
<div align="center">

<img src="../docs/assets/banner_data.svg" alt="data/" width="100%"/>

# 🗂 data — the Catalog and the Presets

</div>

> **Navigation:** [`verification`](../../README.md) › [`trivortex_master`](../README.md) › **`data`**

<p align="center">
  <img src="https://img.shields.io/badge/catalog.json-538%20objects-2DD4BF?style=flat-square" alt="538 objects"/>
  <img src="https://img.shields.io/badge/sources-URL%20per%20entry-34D399?style=flat-square" alt="sources with URL"/>
  <img src="https://img.shields.io/badge/TAP%20cache-daily%20TTL-2DD4BF?style=flat-square" alt="daily TAP cache"/>
</p>

**data/** holds the complex's data: the 538-object catalog (every entry
with a source URL), 20 scene presets, annotated literature, the NASA
TAP exoplanet cache, and the launch ASCII banners.

## 📂 Contents — What Lives Here

| File | Size | Description |
|---|---:|---|
| [`catalog.json`](catalog.json) | 239,479 B | **538 objects**: 98 static entries (planets, moons, asteroids, comets, stars) + 440 NASA TAP exoplanets; each with mass, radius, orbit, color, and a `source` with a URL |
| [`presets_scenes.json`](presets_scenes.json) | 12,758 B | 20 scene presets (19 physical + 1 unphysical) |
| [`literature.md`](literature.md) | 6,714 B | 21 annotated sources: from Lagrange 1772 to Gillon 2017 |
| [`trajectories.json`](trajectories.json) | 2,526 B | stored trajectories for the menu |
| [`cache/exoplanets_latest.json`](cache/exoplanets_latest.json) | 1,561,663 B | the TAP cache (daily TTL, offline fallback) |
| [`cache/exoplanets_2026-11-21.json`](cache/exoplanets_2026-11-21.json) | 1,561,607 B | a dated snapshot of the same cache |
| [`banners/acll.txt`](banners/acll.txt) | 691 B | the ACLL ASCII banner (truecolor) |
| [`banners/acll_plain.txt`](banners/acll_plain.txt) | 239 B | the plain banner variant (for pipes) |

## The catalog: mass-radius (real data)

<p align="center">
  <img src="../docs/assets/catalog_mass_radius.png" alt="Catalog: mass-radius, 538 objects" width="74%"/>
</p>

Test A6 verifies: **538 objects, 538 with a `source`** — not a single
record without a source. The exoplanet part is assembled from the NASA
Exoplanet Archive (TAP, table `ps`, `default_flag=1`) with a daily
cache; the static core is NSSDC/checked literature values.

```python
import json
cat = json.load(open("data/catalog.json"))
entries = cat if isinstance(cat, list) else cat["objects"]
by_type = {}
for e in entries:
    by_type[e["type"]] = by_type.get(e["type"], 0) + 1
# {'exoplanet': 440, 'planet': 8, 'moon': 29, 'asteroid': 20, ...}
```

## Honest estimate flags

Comet-nucleus masses are literature estimates, not measurements: those
entries carry `"mass_estimated": true`, and the presets inherit the
flag honestly.

## Rebuilding

```bash
python3 tools/build_catalog.py             # full (network + static core)
python3 tools/build_catalog.py --limit 50  # cap the TAP sample
python3 tools/build_catalog.py --offline   # the static 98 only
```

## Related

- [realism/](../realism/README.md) — the TAP loaders and the validator
- [lab/](../lab/README.md) — presets turn the catalog into scenes
- [tools/](../tools/README.md) — the catalog build

## 🇷🇺 Краткое резюме (Russian Summary)

- Данные комплекса: каталог из 538 объектов (98 статических записей + 440 экзопланет NASA TAP), у каждой — источник с URL; тест A6 проверяет, что без источника не осталось ни одной записи;
- 20 пресетов сцен (19 физических + 1 нефизический), аннотированная литература из 21 источника (от Лагранжа 1772 до Gillon 2017), сохранённые траектории для меню;
- TAP-кэш с дневным TTL и честным офлайн-фолбэком (`data/cache/`);
- массы ядер комет — литературные оценки: такие записи честно несут флаг `"mass_estimated": true`;
- пересборка каталога: `tools/build_catalog.py` с ключами `--limit N` и `--offline` (только статические 98).

---

<div align="center">

**[⬆ Back to top](#-data--the-catalog-and-the-presets)** ·
**[trivortex_master](../README.md)** ·
**[Repository root](../../../README.md)**

*Part of [wild8highlander/Trivortex](https://github.com/wild8highlander/Trivortex) · Licensed under [IPL-RP-1.0](https://github.com/wild8highlander/Trivortex/blob/main/LICENSE.md) — All Rights Reserved*

</div>
