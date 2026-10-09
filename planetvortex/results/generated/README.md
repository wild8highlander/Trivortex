# `results/generated/` — the monograph samples

The committed artifacts of the monograph generator — the same pipeline
you run with:

```bash
PYTHONPATH=python python3 -m planetvortex.cli monograph \
    --bodies "Sun,Earth,Mars" --lang en --format all
```

| file | what it is |
|------|-----------|
| `planetvortex-monograph-sun-jupiter-saturn-earth-en.*` | the sample monograph (EN) — md, docx, pdf |
| `planetvortex-monograph-sun-jupiter-saturn-earth-ru.*` | the same in Russian |
| `planetvortex-monograph-*kepler-452b*` | a custom-body monograph: the exoplanet Kepler-452b entered as `Name#mass_kg*radius_km` |

The docx carries the house navy-gold reference styles (the polyvortex
pipeline); the pdf is its LibreOffice render. Every number in the
monograph is computed live at generation time, and the verification
certificate inside is executed by the generator itself — not quoted.
