<p align="center">
  <img src="../docs/assets/banner_realism.svg" alt="realism/" width="100%"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/modules-23-60A5FA?style=flat-square" alt="23 modules"/>
  <img src="https://img.shields.io/badge/LOC-~4k-60A5FA?style=flat-square" alt="4k LOC"/>
  <img src="https://img.shields.io/badge/exoplanets-440%20NASA%20TAP-60A5FA?style=flat-square" alt="440 TAP"/>
  <img src="https://img.shields.io/badge/offline-fallbacks%20everywhere-34D399?style=flat-square" alt="offline fallbacks"/>
</p>

**realism/** is the real-data layer: astrometry, catalogs, cosmology
and mission design. The layer rule (S3): `realism -> {core, lab}` —
data flows into the laboratory, but never drags the renderer or the
reports along.

## Data sources

```mermaid
flowchart TD
    subgraph EXT["external sources (network optional)"]
        TAP["NASA Exoplanet Archive<br/>TAP, table ps"]
        HORIZ["JPL Horizons API<br/>ephemerides"]
    end
    subgraph REALISM["realism/"]
        FETCH["data_fetchers/<br/>nasa_exoplanet - nasa_planetary"]
        CACHE["data_fetchers/cache.py<br/>sha256 + daily TTL"]
        STARS["bright_stars<br/>25 brightest, Hipparcos"]
        SKY["sky_coordinates<br/>precession - GMST - equ-to-horiz"]
        COSMO["cosmology<br/>Lambda-CDM, Planck-18"]
        TLE["tles<br/>NORAD + checksums"]
        ALM["almanac<br/>Saros - eclipse year"]
        WEATHER["space_weather<br/>Kp-to-Ap - Svalgaard - GCR"]
    end
    subgraph OUT["output"]
        CAT["data/catalog.json<br/>538 objects with URLs"]
        SCENES["lab/presets<br/>scenes from real systems"]
        SKYMAP["the sky map<br/>(via bind_astronomy)"]
    end
    TAP --> FETCH --> CACHE --> CAT
    HORIZ --> CACHE
    STARS --> SKYMAP
    SKY --> SKYMAP
    CAT --> SCENES
```

Every network source has an **honest offline fallback**: without a
network the complex runs on the cache and the static catalog core,
and the status is visible in the menu ("Help -> Engine status").

## Modules

| Group | Modules | References |
|---|---|---|
| Sky | `sky_coordinates`, `bright_stars`, `observatory`, `almanac`, `eclipse_predictor` | Sirius dec -39.61 deg; Saros; stereographic conformality |
| Catalogs | `planetary_systems`, `stellar`, `validator` | TRAPPIST-1e T_eq = 250 K (Gillon 2017: 249); Habets-81; Roche-Eggleton 0.3789 |
| Cosmos | `cosmology`, `space_weather`, `encounter`, `mission_design`, `jpl_horizons`, `tles` | Planck-18: age 13.80 Gyr, d_L(z=1) = 6.81 Gpc; Parker 47.3 deg |
| Adapters | `adapters/rebound_adapter`, `adapters/dedalus_adapter`, `adapters/custom_adapter` | injection via `register_engine` (S3-clean) |

## Real results

### TRAPPIST-1

<p align="center">
  <img src="../docs/assets/trappist_teq.png" alt="TRAPPIST-1: equilibrium temperatures" width="80%"/>
</p>

`planetary_systems.self_check()` verifies the resonance chain and the
equilibrium temperatures against Gillon 2017; Hill-stability scanners
(Gladman) and habitable-zone packing feed the presets.

### The Lambda-CDM distance ladder

<p align="center">
  <img src="../docs/assets/cosmology_ladder.png" alt="Lambda-CDM: distances and lookback" width="92%"/>
</p>

`cosmology.py` integrates the flat Lambda-CDM distances (Planck-18
parameters) in closed form: luminosity and comoving distances plus the
lookback time — the age of the universe (13.80 Gyr) is a self_check
reference.

### Stars: color from physics

`stellar.py` maps a blackbody temperature to CIE (Wyman 2013) and then
to sRGB: the Sun comes out **#FFF9F9** (white, as it actually looks from
space), M dwarfs red, O stars blue. Mass-luminosity-radius relations
and main-sequence lifetimes (an O star of 30 M_sun lives 1.4 Myr) are
covered by `self_check` (test S20).

### The 25 brightest stars

<p align="center">
  <img src="../docs/assets/bright_stars_hr.png" alt="The 25 brightest stars: color-magnitude" width="82%"/>
</p>

## The sky map: injection instead of import (fixed in v2.0.1)

Before v2.0.1 `render/ascii_sky.py` imported `realism.bright_stars` and
`realism.sky_coordinates`, breaking the S3 direction rule
(`render -> {core, lab}`). Now the catalog and the coordinate
transforms are **injected** by the top layer through
`bind_astronomy()` — the same pattern as `register_engine()` for the
engines:

```python
# modes_extra.py (top layer)
from render.ascii_sky import bind_astronomy
from realism.bright_stars import BRIGHT_STARS
from realism.sky_coordinates import equatorial_to_horizontal, angular_separation

bind_astronomy(lambda: BRIGHT_STARS, equatorial_to_horizontal, angular_separation)
```

The result is the same map, but the import graph is clean (S3 green):

<p align="center">
  <img src="../docs/assets/sky_map_terminal.png" alt="Sky map at 55.75N" width="42%"/>
</p>

## Quick start

```python
from realism.cosmology import self_check as cosmology_check
from realism.stellar import stellar_params

print(cosmology_check())            # age 13.80 Gyr, d_L(z=1) 6.81 Gpc
print(stellar_params(5778.0))       # the Sun: L, R, sRGB color #FFF9F9
```

## Related

- [data/](../data/README.md) — the TAP cache and the 538-object catalog
- [lab/](../lab/README.md) — presets built from real systems
- [render/](../render/README.md) — the sky map (the DI receiver)
