---
title: "Lemma F — the antipodal freeness"
subtitle: "PLANETVORTEX — the point monograph"
---

## Statement

The witness involution $a$ (order 2) acts on the 24 faces $gZ$ without fixed points; hence it pairs them into 12 antipodal pairs — one pair per gravimetric register of stage V2.

## Proof

Suppose $a$ fixes the face $gZ$: $agZ = gZ$, hence $g^{-1}ag \in Z = \langle ab\rangle$. The left side has order 2 (conjugation preserves order), the right side is a group of order 7 — an element of order 2 cannot lie in a group of order 7. Contradiction. A fixed-point-free involution on a 24-element set is a product of 12 transpositions. $\square$

## Computational certificate

Stage V2: the 12 antipodal pairs; face_fixed_points = 0 in the C99 kernel report as well.
