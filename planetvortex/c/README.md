# `c/` — the C99 cross-language oracle

**The independent re-implementation of the load-bearing registers in
plain C99** — the same discipline as the parent framework's language
ports: the committed numbers bind the languages, the code shares
nothing.

| file | what it is |
|------|-----------|
| [`gravikernel.c`](gravikernel.c) | the oracle: PSL(2,7) from nothing (2401 matrices), the coset geometry of the Klein map, the 12-body register algebra (double **and** long double), the SO(3) tilt registers, the 3D two-body Kepler anchor — one JSON report |
| [`Makefile`](Makefile) | `make -C c` builds (`cc -O2 -std=c99 -Wall -Wextra`) |

```bash
make -C c && ./c/gravikernel        # the report on stdout
make crosslang                      # + the Python diff (8/8 registers)
```

The committed cross-language report lives in
[`results/crosslang/`](../results/crosslang/) — the tolerance is
$10^{-9}$ relative on every shared float register, and the C
long-double shadow of the budget closure $\sum\alpha = 8\pi$ lands at
**exactly 0.0**.
