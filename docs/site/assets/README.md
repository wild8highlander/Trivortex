# Site assets — the shared CSS and imagery of the documentation site

The static assets referenced by the HTML pages in [`../`](../): the
single stylesheet and the page imagery. Everything is committed,
dependency-free and served verbatim by GitHub Pages.

| asset | role |
|-------|------|
| `css/` | the shared stylesheet (the navy-gold site design) |
| page imagery | the figures and diagrams embedded by the site pages |

## Conventions

- **no external CDNs** — the pages and this folder are fully
  self-contained; the site renders identically offline;
- relative paths only — the pages reference assets as `assets/…`, so
  the folder layout is part of the contract;
- new assets belong here only if more than one page uses them;
  page-specific imagery stays inline or next to its page.
