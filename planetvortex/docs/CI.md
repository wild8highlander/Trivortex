# How CI re-derives this bench

The parent repository's workflows (`ci.yml`, `lint.yml`) run the
planetvortex guard on every push. The complete discipline:

```bash
cd planetvortex
make all-ladders      # 15 stages: P1..P7, X1..X6, V1..V2 — exit 1 on any FAIL
make test             # the pytest guard (80 tests)
make crosslang        # the C99 oracle vs Python (8 registers) — needs cc
```

The ladders are deterministic (fixed grids, no randomness), so a green
run regenerates the committed protocols in `results/protocols/` with
identical numbers. Suggested CI snippet:

```yaml
- name: planetvortex ladders
  run: cd planetvortex && make quick        # the smoke preset (~8 s)
- name: planetvortex guard
  run: cd planetvortex && make test
- name: planetvortex cross-language
  run: cd planetvortex && make crosslang
```

The `quick` preset keeps CI under 15 s; the `default` preset (~35 s)
is what the committed protocols were recorded at; `full` (~130 s) is
for release validation.
