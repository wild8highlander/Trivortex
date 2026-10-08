# The Python ladder and the interactive laboratory

The reference implementation of the verification program: `verify.py`
is the independent V1–V4 ladder the whole repository's CI keys on, and
`lab.py` is the interactive laboratory that walks the same registers
step by step.

## `verify.py` — the independent ladder

Re-implements — **from scratch, sharing no code with the document** —
everything it checks: the closed form, the Chaplygin combination, the
Kirchhoff right-hand side, its own RK4 stepper. numpy-only, three
presets:

| preset | wall time | used by |
|--------|-----------|---------|
| `quick` | ≈ 0.5 s | CI (every push) |
| `default` | ≈ 2 s | local checks |
| `full` | ≈ 35 s | release validation |

```bash
python3 verify.py --preset quick --out-dir ../../outputs/trivortex
```

Every run writes a JSON protocol with the recorded residuals and the
full parameter snapshot; CI archives it as an artifact. The registered
criteria (V1 choreography + periodicity, V2 rigid rotation, V3/V4
integral conservation) and the honesty boundary of the Chaplygin
diagnostic are documented in the [verification
README](../../README.md).

## `lab.py` — the interactive laboratory

A 22-section executable walk through the same registers: closed form,
choreography, integrals, the diagnostic window — each section prints the
register, the band and the verdict. EOF-safe (Ctrl-D exits cleanly);
runs with no arguments and needs only numpy.

## `sample-figures/` — the committed samples

Three committed PNGs ([`choreography.png`](sample-figures/choreography.png),
[`closed_form.png`](sample-figures/closed_form.png),
[`dashboard.png`](sample-figures/dashboard.png)) — what the ladder and
the lab render, committed so the repository shows its outputs without
running anything. They are documentation artifacts, not registers; the
numeric truth lives in the JSON protocols.
