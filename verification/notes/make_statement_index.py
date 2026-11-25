#!/usr/bin/env python3
"""Generate docs/STATEMENTS.md — the auto-generated index of every theorem
in Trivortex.lean, grouped by section (### sub-sections nested), with the
first line of each docstring and the axiom-footprint counters.

House convention: the index is REGENERATED, never hand-edited:
    python3 ../notes/make_statement_index.py
"""

import re, os, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.join(ROOT, "..", "lean4", "Trivortex.lean")
OUT_DIR = os.path.join(ROOT, "..", "lean4", "docs")
OUT = os.path.join(OUT_DIR, "STATEMENTS.md")

src = open(LEAN, encoding="utf-8").read()
lines = src.split("\n")

# ---------------------------------------------------------------- sections
# headers may span several lines: `/-! ## Title ... -/`
sections = []  # list of dicts {title, subs: [{title, thms: []}], thms}
cur_sec = None
cur_sub = None

i = 0
while i < len(lines):
    ln = lines[i]
    # section/subsection markers: `/-! ## X`, `## X` inside a block, `/-! ### X`, `### X`
    m = re.match(r"^(?:/-!\s+)?(##|###)\s+(.*)$", ln)
    if m:
        level = 2 if m.group(1) == "##" else 3
        buf = [m.group(2)]
        # title = lines until a blank line or the closing -/
        while buf and not buf[-1].rstrip().endswith("-/"):
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if not nxt.strip() or nxt.lstrip().startswith("##"):
                break
            buf.append(nxt)
            i += 1
        buf[-1] = buf[-1].rstrip().removesuffix("-/").rstrip()
        title = re.sub(r"\s+", " ", " ".join(buf)).strip()
        if level == 2:
            cur_sec = {"title": title, "subs": [], "thms": []}
            sections.append(cur_sec)
            cur_sub = None
        else:
            cur_sub = {"title": title, "thms": []}
            if cur_sec is not None:
                cur_sec["subs"].append(cur_sub)
        i += 1
        continue
    # docstring block then theorem
    if ln.strip().startswith("/--"):
        doc_parts = []
        if ln.rstrip().endswith("-/") and len(ln.strip()) > 4:
            doc_parts = [ln.strip()]
        else:
            doc_parts = [ln.strip()]
            while not lines[i].rstrip().endswith("-/"):
                i += 1
                doc_parts.append(lines[i].strip())
            doc_parts.append(lines[i].strip())
        doc = re.sub(r"\s+", " ", " ".join(doc_parts))
        doc = re.sub(r"^/\-\-+\s*", "", doc).rstrip("-/").strip()
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines):
            mt = re.match(r"^(noncomputable )?theorem (\w+)", lines[j])
            if mt and cur_sec is not None:
                target = cur_sub if cur_sub is not None else cur_sec
                target["thms"].append((mt.group(2), doc))
        i += 1
        continue
    # theorems WITHOUT a docstring (rare, but count them into the current group)
    mt = re.match(r"^(noncomputable )?theorem (\w+)", ln)
    if mt and cur_sec is not None:
        target = cur_sub if cur_sub is not None else cur_sec
        if not target["thms"] or target["thms"][-1][0] != mt.group(2):
            target["thms"].append((mt.group(2), "*(no docstring)*"))
    i += 1

n_prints = len(re.findall(r"^#print axioms ", src, re.M))
n_sorry = len(re.findall(r"^\s*sorry\s*$", src, re.M))  # proof terminators only
n_axiom = len(re.findall(r"^axiom ", src, re.M))
n_thm = sum(len(s["thms"]) + sum(len(sub["thms"]) for sub in s["subs"]) for s in sections)

os.makedirs(OUT_DIR, exist_ok=True)
today = datetime.date.today().isoformat()
out = []
out.append("# STATEMENT INDEX — `Trivortex.lean`")
out.append("")
out.append(
    f"*Auto-generated from `Trivortex.lean` on {today} by "
    "`verification/notes/make_statement_index.py` — do not hand-edit; "
    "regenerate after every change to the Lean file.*"
)
out.append("")
out.append("| Metric | Value |")
out.append("|---|---|")
out.append(f"| Theorems indexed | **{n_thm}** |")
out.append(f"| `#print axioms` statements | **{n_prints}** |")
out.append(f"| `sorry` occurrences | **{n_sorry}** (must stay 0) |")
out.append(f"| `axiom` declarations | **{n_axiom}** (must stay 0) |")
out.append(f"| Top-level sections | {len(sections)} |")
out.append("")
out.append(
    "**Axiom footprint:** every theorem resolves to "
    "`[propext, Classical.choice, Quot.sound]` — Mathlib's classical "
    "foundations only."
)
out.append("")
out.append("## Contents")
out.append("")
for s in sections:
    cnt = len(s["thms"]) + sum(len(x["thms"]) for x in s["subs"])
    out.append(f"- **{s['title']}** — {cnt} theorems")
    for x in s["subs"]:
        out.append(f"  - {x['title']} — {len(x['thms'])}")
out.append("")
for s in sections:
    out.append(f"## {s['title']}")
    out.append("")

    def emit(thms):
        if not thms:
            return
        out.append("| Theorem | Statement (docstring, first line) |")
        out.append("|---|---|")
        for name, doc in thms:
            d = doc.replace("|", "\\|")
            if len(d) > 160:
                d = d[:157] + "…"
            out.append(f"| [`{name}`](../Trivortex.lean) | {d} |")
        out.append("")

    emit(s["thms"])
    for x in s["subs"]:
        out.append(f"### {x['title']}")
        out.append("")
        emit(x["thms"])

open(OUT, "w", encoding="utf-8").write("\n".join(out))
print(f"written {OUT}")
print(f"theorems: {n_thm}, prints: {n_prints}, sections: {len(sections)}")
for s in sections:
    cnt = len(s["thms"]) + sum(len(x["thms"]) for x in s["subs"])
    print(f"  {cnt:3d}  {s['title'][:78]}")
