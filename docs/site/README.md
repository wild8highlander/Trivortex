# The documentation site — 9 static pages on GitHub Pages

The browser-facing front of the repository, published verbatim by
[`deploy-docs.yml`](../../.github/workflows/deploy-docs.yml) to
**[wild8highlander.github.io/Trivortex](https://wild8highlander.github.io/Trivortex)**.
No build step, no Jekyll (a committed `.nojekyll` keeps GitHub's
generator out of the way), no external dependencies — plain HTML.

## The pages

| page | content |
|------|---------|
| [`index.html`](index.html) | hero, badges, 60-second summary, headline results, abstract |
| [`vortex-model.html`](vortex-model.html) | bodies→vortices, the Hamiltonian, observables, literature context |
| [`theorem-3-1.html`](theorem-3-1.html) | statement, reference values, certified vs recorded, the Lagrange twin |
| [`code.html`](code.html) | the 22 sections, menu modes, report engine |
| [`system-presets.html`](system-presets.html) | Sun–Earth–Moon, α Centauri, Pluto–Charon–Nix |
| [`verification.html`](verification.html) | V1–V4, criteria, roadmap, honesty notes |
| [`research.html`](research.html) | the twelve studies with key results and direct links |
| [`publications.html`](publications.html) | the reading room: every PDF/DOCX rendition |
| [`citation.html`](citation.html) | CFF, BibTeX, DOI |
| [`license.html`](license.html) | IPL-RP-1.0, REUSE, contact |

`assets/` holds the shared CSS and imagery; `site-assets` referenced by
the pages live in [`assets/`](assets/) one level deep.

## Local preview

```bash
python3 -m http.server -d docs/site 8080     # from the repository root
# → http://localhost:8080
```

## Editing

The pages mirror the READMEs' content in browser form; keep the numbers
protocol-bound exactly as the READMEs do. The deploy workflow publishes
verbatim on every change to this folder — there is no staging
environment, so review renders locally before pushing. Links across the
site are checked by the repository's link checker workflow.
