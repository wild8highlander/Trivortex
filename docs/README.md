# TRIVORTEX — Documentation (`docs/`)

> **Navigation:** [repository root](../README.md) › **`docs/`**
>
> Everything behind the GitHub Pages site at
> **[wild8highlander.github.io/research-papers](https://wild8highlander.github.io/research-papers)**
> — plus the SVG source assets of the repository's visual identity.

---

## Table of contents

1. [What lives here](#1-what-lives-here)
2. [The site — page map](#2-the-site--page-map)
3. [How deployment works](#3-how-deployment-works)
4. [Local preview](#4-local-preview)
5. [The SVG identity assets](#5-the-svg-identity-assets)
6. [Editing guidelines](#6-editing-guidelines)

---

## 1. What lives here

| Path | Contents |
|---|---|
| `site/` | the static documentation site — 9 plain-HTML pages + shared CSS + site copies of the SVG assets |
| `site/assets/css/style.css` | the single stylesheet: navy-and-gold identity, cards, tables, badges |
| `site/assets/*.svg` | banner, title page, orbit showcase, divider (site copies) |
| `assets/*.svg` | the canonical SVG assets referenced by the root README and these pages |

There is **no build step**: the pages are hand-shaped HTML, and the static upload deployment (`deploy-docs.yml`) publishes them as-is. This is a
deliberate dependency-zero choice — the site cannot break because a generator
was updated on the same day as a conference deadline.

---

## 2. The site — page map

| Page | Content |
|---|---|
| [`index.html`](site/index.html) | hero + badges, the document in 60 seconds, headline results, quick start, abstract (EN + RU summary), site map |
| [`vortex-model.html`](site/vortex-model.html) | bodies → vortices, the Hofstadter-type Hamiltonian, the Chaplygin integral, observable families, literature context |
| [`theorem-3-1.html`](site/theorem-3-1.html) | statement, reference values (`ω = 1.3748022274393588` for C_Ch = 1), certified vs recorded, the Lagrange numerical twin |
| [`code.html`](site/code.html) | the three mirrors, the full 22-section map, the 15 menu modes, the report engine |
| [`system-presets.html`](site/system-presets.html) | Sun–Earth–Moon, α Centauri, Pluto–Charon–Nix — how the presets are (and are not) used |
| [`verification.html`](site/verification.html) | the V1–V4 table with registered criteria, JSON protocols, roadmap M0–M3, honesty notes |
| [`citation.html`](site/citation.html) | DOI infrastructure, CITATION.cff, BibTeX, reproducibility note |
| [`license.html`](site/license.html) | IPL-RP-1.0, REUSE/SPDX, contact |

---

## 3. How deployment works

The workflow [`.github/workflows/deploy-docs.yml`](../.github/workflows/deploy-docs.yml):

1. triggers on pushes that touch `docs/site/**` (and on releases);
2. builds the site with `actions/jekyll-build-pages` (source: `docs/site`);
3. deploys the artifact with `actions/deploy-pages` to the
   `github-pages` environment.

The URL is configured in the repository settings (Pages → deploy from the
`github-pages` environment); the canonical address is
`https://wild8highlander.github.io/research-papers`.

---

## 4. Local preview

```bash
python3 -m http.server 8080 -d docs/site
# → http://localhost:8080
```

or `make docs` from the repository root. No toolchain, no install.

---

## 5. The SVG identity assets

The assets are generated (scripted in the repository's tooling history, not
hand-drawn) and share one palette — deep navy `#0A1730`/`#0E2145`, gold
`#D4AF37`, ink `#E9EEF8`, with the three-body accent colours gold/cyan/rose for
the three vortices:

| Asset | Used by |
|---|---|
| `banner-hero.svg` | root README header, site index hero |
| `title-page.svg` | the book's title document: TRIVORTEX, subtitle, author, DOI, MMXXVI |
| `orbits-showcase.svg` | root README §1, site index — three honest panels (figure-eight choreography, Lagrange triangle, unequal circulations) |
| `divider-gold.svg` | section dividers in README and pages |

The orbit artwork is an **artistic rendering** — the exact Lagrange rotation is
the thing verified numerically by ladder check V2; the panels are labelled
accordingly.

---

## 6. Editing guidelines

1. **Keep the stylesheet single.** New visual elements extend
   `site/assets/css/style.css`; inline styles only for one-off geometry.
2. **Numbers must match the ladder.** Any residual, tolerance or reference
   value quoted on a page must be the same one registered in
   [`verification/README.md`](../verification/README.md) — if you update one,
   update both in the same PR.
3. **Validate structure.** Tag-balance the HTML before committing (the pages
   were validated for version 1.0.0; keep them that way).
4. **Honesty is layout-relevant.** The certified-vs-recorded separation and the
   "artistic rendering" labels are part of the content, not decoration — do not
   shorten them away.

---

## 7. Deployment contract

The Pages deployment is a **pure static upload** — no Jekyll, no generator:

- [`deploy-docs.yml`](../.github/workflows/deploy-docs.yml) triggers on every
  push touching `docs/site/**`, on published releases, and manually
  (`workflow_dispatch`);
- the job configures Pages, uploads `docs/site/` verbatim via
  `actions/upload-pages-artifact` and deploys with `actions/deploy-pages`;
- a committed [`site/.nojekyll`](site/.nojekyll) keeps GitHub's Jekyll
  processing out of the way — what is committed is what is served;
- the deployment is concurrency-locked (`group: "pages"`), so rapid pushes
  cancel stale builds instead of racing them;
- a [`site/404.html`](site/404.html) renders the branded not-found page for
  broken deep links.

## 8. Page anatomy

Every page shares the same skeleton — this is why the site stays consistent
with zero templating:

| Element | Implementation |
|---|---|
| Header | `.site` bar: brand + 10-link navigation, active page highlighted |
| Hero | banner SVG + live badge strip + lead paragraph |
| Cards | `.grid` of `.card` blocks with KPI numbers for headline stats |
| Tables | striped navy-gold tables mirroring the README tables |
| Footer | edition line (version 1.0.0), DOI, ORCID, license link |
| CSS | single `assets/css/style.css`, CSS variables for the palette, no frameworks |

## 9. Editing checklist

1. Edit the page or the stylesheet — plain HTML/CSS, no build.
2. Keep the navigation list identical on all pages (10 links, same order).
3. Update the version references in the footer and the badges together.
4. Check every new link with `python3 -m http.server -d docs/site 8080` —
   or rely on the `link-checker.yml` workflow on the next push.
5. Commit — the Pages workflow deploys automatically.
