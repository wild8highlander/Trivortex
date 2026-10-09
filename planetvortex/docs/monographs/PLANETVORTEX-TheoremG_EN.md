---
title: "Theorem G — the budget closure (the capstone)"
subtitle: "PLANETVORTEX — the point monograph"
---

## Statement

Let $\mathrm{GM}_1, \ldots, \mathrm{GM}_{12}$ be the gravitational parameters of the registered 12-body set and $s_i = \ln \mathrm{GM}_i - \frac{1}{12}\sum_j \ln \mathrm{GM}_j$ the geometric-mean normalization. Then: $\sum_i s_i = 0$ exactly; the vertex-angle register $\alpha_i = \frac{2\pi}{3} - \sigma s_i$ (any $\sigma > 0$) satisfies $\sum_i \alpha_i = 8\pi$ exactly; the decorated tessellation of the 12 antipodal heptagon pairs therefore closes on the Gauss–Bonnet budget of the Klein quartic, $\sum_i 2A_i = \sum_i 2(5\pi - 7\alpha_i) = 8\pi = 2\pi(2g-2)$; and the heavier the body, the wider its heptagon. The Euler characteristic absorbs the mass ladder.

## Proof

(1) $\sum_i s_i = \sum_i \ln \mathrm{GM}_i - 12 \cdot \frac{1}{12} \sum_j \ln \mathrm{GM}_j = 0$. (2) $\sum_i \alpha_i = 12 \cdot \frac{2\pi}{3} - \sigma \sum_i s_i = 8\pi$. (3) The area of a hyperbolic $n$-gon with interior angles $\alpha_1, \ldots, \alpha_n$ is $(n-2)\pi - \sum \alpha_k$ (Gauss–Bonnet per cell), so for $n = 7$: $\sum_i 2A_i = 2(60\pi - 7 \cdot 8\pi) = 8\pi$. (4) A regular hyperbolic heptagon of vertex angle $\alpha \in (0, 5\pi/7)$ exists and is unique; its right-triangle trigonometry gives the closed forms $\cosh R = \cot(\alpha/2)\cot(\pi/7)$, $\cosh(\ell/2) = \cos(\pi/7)/\sin(\alpha/2)$, $\cosh r = \cos(\alpha/2)/\sin(\pi/7)$; the monotonicity chain $\ln \mathrm{GM} \uparrow \Rightarrow s \uparrow \Rightarrow \alpha \downarrow \Rightarrow A \uparrow$ finishes the claim. $\square$

## Computational certificate

Stage V2 at 50 dps: the budget closure Σα − 8π = 4.3e−50, the area closure, the Pythagoras on all 12 registers, the Poincaré-disk witnesses; the C99 kernel re-derives the algebra independently (long-double residual 0.0).
