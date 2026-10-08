# POLYVORTEX — results

The output tree of the mini-repository: deterministic, protocol-bound,
nothing hand-written.

```text
results/
└── protocols/   ← the committed W1–W7 JSON protocols (default preset)
```

## What belongs here

- **`protocols/`** — one deterministic JSON per ladder stage, bound to a
  run by a full parameter snapshot and keyed to the preset. The
  committed set is the `default` preset; `quick` and `full` runs
  reproduce the same numbers with different integration effort.

## What does NOT belong here

- non-deterministic fields inside the *numbers* — the protocols are
  re-derivable, that is their point;
- figures (they live in [`figures/`](../figures/) and are generated
  *from* these protocols);
- ad-hoc experiment outputs — a new experiment becomes part of the bench
  only when it has a registered stage, a tolerance committed before the
  run, and a protocol.

## How the protocols flow

```bash
make ladder      # regenerate all seven protocols (default preset)
make test        # the pytest guard re-derives the preset-independent numbers
make figures     # the figure factory READS these protocols
```

The chain is strict: the ladder writes, the tests pin, the figures read,
the READMEs and monographs quote. See
[`protocols/README.md`](protocols/README.md) for the per-file index and
the schema.
