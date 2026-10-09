---
title: "Theorem F — the coset construction of the Klein map"
subtitle: "PLANETVORTEX — the point monograph"
---

## Statement

Let $G = \mathrm{PSL}(2,7)$ (168 classes over $\mathbb{F}_7$) and let $(a, b)$ be any pair with $a^2 = b^3 = (ab)^7 = 1$. With $X = \langle a\rangle$, $Y = \langle b\rangle$, $Z = \langle ab\rangle$, define the vertices as the right cosets $gY$, the edges as $gX$, the faces as $gZ$, with the incidence by nonempty coset intersection. Then there are 56 vertices, 84 edges, 24 faces and $V - E + F = -4$; every vertex has degree 3, every face is a 7-cycle; the map is connected and orientable; the left action of $G$ is faithful — the Klein map $\{7,3\}_8$ with $\mathrm{Aut}^+ \cong \mathrm{PSL}(2,7)$ and $|\mathrm{Aut}| = 336$ including reflections.

## Proof

The number of right cosets of $H$ is $|G|/|H|$: $168/3 = 56$, $168/2 = 84$, $168/7 = 24$. The stabilizer chain of the triangle group gives exactly 3 edges per vertex, 2 vertices and 2 faces per edge, and a 7-cycle of edges per face. The (2,3,7) triple generates $G$, so the flag graph is connected; the full flag set of 336 pairwise-incident triples has a bipartite adjacency graph (two flags adjacent iff they differ in one member) — orientability. Hence $\chi = V - E + F = -4$, genus $g = 1 - \chi/2 = 3$. Faithfulness: the core of $\langle b\rangle$ is trivial in the simple group $G$. The Hurwitz bound $84(g-1) = 168$ caps the orientation-preserving automorphisms at the certified 168; the reflections double the count. $\square$

## Computational certificate

Stage V2 (V2_klein_tiling_default.json): the exact combinatorial registers, the connected and bipartite flag graph, and the PGL(2,7) flag certificate on all 336 × 3 flag moves.
