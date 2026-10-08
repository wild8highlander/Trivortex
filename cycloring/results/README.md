# CYCLORING — results

The output tree of the mini-research. Everything deterministic and
protocol-bound lives here; nothing in this folder is hand-written.

```text
results/
└── protocols/   ← the committed W1–W7 JSON protocols (default preset)
```

## What belongs here

- **`protocols/`** — one deterministic JSON per ladder stage, bound to a
  run by a full parameter snapshot. The committed set is keyed to the
  `default` preset; `quick` and `full` runs of the same stages produce
  the same numbers with different integration effort (their protocols
  are not committed unless a release decision says otherwise).

## What does NOT belong here

- wall-clock timings, machine fingerprints or any non-deterministic
  fields inside the *numbers* — the protocols are re-derivable
  byte-for-byte, that is their point;
- figures (they live in [`figures/`](../figures/) and are generated
  *from* these protocols);
- ad-hoc experiment outputs — a new experiment becomes part of the
  mini-research only when it has a registered stage, a tolerance band
  committed before the run, and a protocol.

## How the protocols are produced and consumed

```bash
make ladder      # regenerate all seven protocols (default preset)
make test        # the pytest guard re-derives the preset-independent numbers
make figures     # the figure factory READS these protocols
```

The consumer chain is strict: the ladder writes, the tests pin, the
figures read, the READMEs and monographs quote. A number that does not
originate from a file in `protocols/` has no standing anywhere in the
mini-research.

See [`protocols/README.md`](protocols/README.md) for the per-file index
and the schema.
