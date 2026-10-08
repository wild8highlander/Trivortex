# The HTML sources — 14 files, 1:1 with the study PDFs

The editable HTML renditions of the twelve study monographs plus the two
special volumes, produced by the build system
([`../build/`](../build/)) on the way from Markdown to PDF. The HTML is
the exact styling source the Chromium printer turns into the navy-gold
PDF bodies — committed so every styling decision is inspectable and
diffable.

## The inventory

- **12 study HTML files** — `TRX-01` … `TRX-12`, each in the RU and EN
  pair → 12 of the 14 (the language pairing follows the study monograph
  sources in `research/TRX-*/monograph/`);
- **2 special volumes** — the core monograph and the research
  compendium, whose HTML comes from [`../src/`](../src/).

Naming: `<document>_<RU|EN>.html`, mirroring the PDF names in
[`../pdf/`](../pdf/) one-to-one.

## What the files contain

Each HTML file is a self-styled single page: the navy-gold design
system inlined (no external CSS), MathML equations rendered offline,
300-dpi figures embedded as base64 or referenced assets, striped tables
with repeating headers. They open correctly from a plain file:// URL —
no server, no build step, no network.

## When to edit

Never by hand: the HTML is a build product. Edit the Markdown sources
(`research/TRX-*/monograph/` or [`../src/`](../src/)) and rebuild via
`make pdf-library`; the HTML, PDF and DOCX renditions regenerate
together and stay in sync by construction.
