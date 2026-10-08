# TRX-11 — the executable study

[`trx11_gw_choreography.py`](trx11_gw_choreography.py) is the single-script study of
**Gravitational Waves from the Figure-Eight Choreography** — a deterministic `numpy/scipy` program that computes
every register of the study, checks it against its registered tolerance
bands and writes the committed JSON protocol into
[`../results/`](../results/).

## The three modes

```bash
python3 code/trx11_gw_choreography.py                # the full run: statistics + JSON protocol
python3 code/trx11_gw_choreography.py --smoke        # the CI smoke: seconds, status PASS required
python3 code/trx11_gw_choreography.py --figures      # the full run + the 300-dpi figure set
```

- **default** — the complete computation; every registered check is
  evaluated and the protocol (`../results/`) is written;
- **`--smoke`** — the CI mode: the same code paths at coarse
  resolution, deterministic, seconds of wall time; CI asserts
  `status: PASS` on every push (see the root
  [`ci.yml`](../../../.github/workflows/ci.yml) via
  `make research-smoke`);
- **`--figures`** — the full run plus the regeneration of
  [`../figures/`](../figures/) at 300 dpi.

## What the script computes

The study's registers, the acceptance checks (6 registered, all
PASS in the committed
protocol) and the plotted series. The physical formulation, the
governing equations, the dimensionless mapping and the numerical method
are documented in the study README
([§3–§8](../README.md)); the protocol is annotated in
[`../results/`](../results/).

## The discipline

- **registered before recorded** — the check targets and tolerances
  were committed before the reference run; the script never tunes a
  band to make a check pass;
- **protocol or it did not happen** — any number the script prints is
  carried by the JSON protocol; a run without a protocol has no
  standing;
- **deterministic** — fixed seeds, fixed grids; re-running reproduces
  the committed protocol byte-for-byte (the wall-time field is a stamp,
  not a register).
