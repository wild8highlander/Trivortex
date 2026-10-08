# Support — how to get help with TRIVORTEX

Thank you for using TRIVORTEX. This document explains where to ask questions,
where to report problems, and how quickly you can expect a response. Please
read it before opening an issue — choosing the right channel gets you a
better answer faster, and keeps the issue tracker useful for everyone.

## TL;DR — which channel do I use?

| Situation | Channel |
|---|---|
| «How do I run the document / the ladder?» | [Documentation site](https://wild8highlander.github.io/Trivortex/) and the [README §16](README.md#16-quick-start--reproduction) |
| Something is broken (crash, wrong number, dead link) | [Bug report](https://github.com/wild8highlander/Trivortex/issues/new?template=bug_report.yml) |
| You want a feature, preset, study or format | [Feature request](https://github.com/wild8highlander/Trivortex/issues/new?template=feature_request.yml) |
| Questions about the physics, the model or Theorem 3.1 | A **Question** issue via the [issue chooser](https://github.com/wild8highlander/Trivortex/issues/new/choose) |
| Security vulnerability | **Do not open a public issue** — see [SECURITY.md](SECURITY.md) |
| Citation, DOI, Zenodo, licensing | [CITATION.cff](CITATION.cff), [README §19](README.md#19-citation-doi--zenodo), [NOTICE.md](NOTICE.md) |

## Before you ask

Many questions are already answered by the repository itself:

1. **The README** covers the model, the verification ladder V1–V4, the twelve
   studies, the quick-start commands and the full repository structure.
2. **The documentation site** mirrors the README as browsable pages —
   including the [verification page](https://wild8highlander.github.io/Trivortex/verification.html)
   and the [system presets](https://wild8highlander.github.io/Trivortex/system-presets.html).
3. **`make help`** lists every supported command (run, verify, test, docs,
   research smoke runs, animations, PDF library).
4. **Existing issues** may already describe your problem — search before
   opening a new one.

## Running things the supported way

```bash
git clone https://github.com/wild8highlander/Trivortex.git
cd Trivortex
make install          # numpy, scipy, matplotlib, mpmath, pytest, ruff
make run              # the 22-section executable document (interactive menu)
make verify-quick     # the independent ladder V1–V4, quick preset
make test             # the 27-test pytest guard
```

If a command fails, include the following in your report: OS and Python
version (`python3 --version`), the exact command, and the full output
including the traceback. For wrong-number reports, please attach the JSON
protocol produced by the ladder or the study — every check emits a full
parameter snapshot precisely so that failures are reproducible.

## Response expectations

This is a solo, independent-research project, maintained in the author's
spare time. There is no SLA. Typical response time is measured in days, not
hours; complex physics questions may take longer because they deserve
considered answers. Issues that arrive with reproduction steps, JSON
protocols and expected-vs-actual behaviour get answered first — a report
that can be reproduced is already half solved.

## A note on scope

TRIVORTEX is a research artifact: the executable document, its independent
verification ladder, and the twelve companion studies are published as they
are, with their certified and recorded results explicitly separated. The
project does not provide bespoke numerical investigations on request, but
well-grounded extensions — a new preset, a new check, a new language mirror
of the verifier — are welcome via the standard
[contribution process](CONTRIBUTING.md).
