#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
PLANETVORTEX — THE PSL(2,7) STRUCTURE AND THE EXACT FIGURE (Layer F)
============================================================================
The geometric layer of the bench. One structure, two equivalent models,
one figure:

Model Z (cyclic, primary). The points are the residues Z_7 = {0..6} —
the seven heptagon vertices in orbital order (station i = the i-th
wandering planet: Mercury, Venus, Mars, Jupiter, Saturn, Uranus,
Neptune). The lines are the seven cyclic triples

    {i, i+1, i+3}  (mod 7),   i = 0..6,

each carrying three points, every pair of points on exactly one line —
the Fano plane PG(2,2). The automorphism group is the 168
line-preserving permutations of Z_7 — PSL(2,7) in its natural action.

Model B (binary, algebraic). The points are the seven nonzero vectors
of F_2^3; the lines are the triples {u, v, u+v}; the automorphism
group is GL(3,2) of order 168. P4 certifies an explicit line-preserving
bijection Z_7 -> F_2^3 and the conjugacy of the two group copies
inside S_7 — the two models are one structure.

THE FIGURE. A regular heptagon of circumradius R: the Sun at the
centre, the seven stations at the vertices. Every line is a scalene
triangle with interior angles (pi/7, 2pi/7, 4pi/7) — the binary ladder
1 : 2 : 4 — with sides

    s_1 = 2R sin(pi/7),  s_2 = 2R sin(2pi/7),  s_3 = 2R sin(3pi/7),

(one chord of each class) and area

    Delta = s_1 s_2 s_3 / (4R) = R^2 sqrt(7)/4,

by the classical identity sin(pi/7) sin(2pi/7) sin(3pi/7) = sqrt(7)/8.
All seven lines are congruent, and the chord product s_1 s_2 s_3 =
R^3 sqrt(7) fixes the vortex Hamiltonians exactly (Theorems A, B).

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import math
from itertools import permutations
from typing import Dict, List, Optional, Tuple

import numpy as np

TWO_PI = 2.0 * math.pi

STATION_NAMES: Tuple[str, ...] = (
    "Mercury",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
)

N_POINTS = 7


# ---------------------------------------------------------------------------
# Model Z — the cyclic Fano plane on Z_7
# ---------------------------------------------------------------------------


def cyclic_line_triples() -> List[Tuple[int, int, int]]:
    """The seven lines of the cyclic model: {i, i+1, i+3} (mod 7)."""
    return [tuple(sorted((i, (i + 1) % 7, (i + 3) % 7))) for i in range(7)]


def fano_lines() -> List[Tuple[int, int, int]]:
    """The lines of the figure (sorted triples of vertex indices 0..6)."""
    return sorted(cyclic_line_triples())


def line_of_pair(i: int, j: int) -> Tuple[int, int, int]:
    """The unique line through two distinct points of Z_7."""
    for line in cyclic_line_triples():
        if i in line and j in line:
            return line
    raise ValueError(f"no line through {i} and {j}")


def incidence_matrix() -> np.ndarray:
    """The 7x7 point-line incidence matrix (rows: vertices 0..6)."""
    lines = fano_lines()
    mat = np.zeros((7, 7), dtype=int)
    for j, line in enumerate(lines):
        for i in line:
            mat[i, j] = 1
    return mat


def automorphism_group() -> List[Tuple[int, ...]]:
    """PSL(2,7) as the 168 line-preserving permutations of Z_7.

    Built by filtering S_7 (5040 candidates) against the line set —
    exhaustive, deterministic, and free of representation choices.
    Each automorphism is the tuple (sigma(0), ..., sigma(6)).
    """
    lines = {line for line in cyclic_line_triples()}
    group: List[Tuple[int, ...]] = []
    for perm in permutations(range(7)):
        ok = True
        for line in cyclic_line_triples():
            image = tuple(sorted(perm[i] for i in line))
            if image not in lines:
                ok = False
                break
        if ok:
            group.append(perm)
    return group


# ---------------------------------------------------------------------------
# Model B — the binary Fano plane over F_2^3
# ---------------------------------------------------------------------------

Label = Tuple[int, int, int]


def _label_index(lab: Label) -> int:
    """Nonzero vector -> 1..7 (LSB first)."""
    return lab[0] | (lab[1] << 1) | (lab[2] << 2)


def binary_labels() -> List[Label]:
    """The seven nonzero vectors of F_2^3."""
    return [(k & 1, (k >> 1) & 1, (k >> 2) & 1) for k in range(1, 8)]


def binary_lines() -> List[Tuple[Label, Label, Label]]:
    """The seven lines {u, v, u+v} of the binary model."""
    lines = set()
    labels = binary_labels()
    for i, u in enumerate(labels):
        for v in labels[i + 1 :]:
            w = tuple((a + b) & 1 for a, b in zip(u, v))
            lines.add(tuple(sorted((u, v, w))))
    return sorted(lines)  # type: ignore[return-value]


def _mat_mul(a, b):
    """3x3 matrix product over F_2."""
    return tuple(
        tuple((a[i][0] * b[0][j] + a[i][1] * b[1][j] + a[i][2] * b[2][j]) & 1 for j in range(3))
        for i in range(3)
    )


def _is_invertible(a) -> bool:
    """Invertibility over F_2 by Gaussian elimination."""
    m = [list(row) for row in a]
    for col in range(3):
        pivot = next((r for r in range(col, 3) if m[r][col]), None)
        if pivot is None:
            return False
        m[col], m[pivot] = m[pivot], m[col]
        for r in range(3):
            if r != col and m[r][col]:
                m[r] = [(m[r][c] + m[col][c]) & 1 for c in range(3)]
    return True


def gl3_2() -> List[Mat3]:
    """All invertible 3x3 matrices over F_2 — GL(3,2), 168 elements."""
    mats: List[Mat3] = []
    seen = set()
    for bits in range(512):
        rows = tuple(tuple((bits >> (3 * i + j)) & 1 for j in range(3)) for i in range(3))
        if rows in seen:
            continue
        seen.add(rows)
        if _is_invertible(rows):
            mats.append(rows)  # type: ignore[arg-type]
    return mats


Mat3 = Tuple[Tuple[int, int, int], Tuple[int, int, int], Tuple[int, int, int]]


def gl3_2_action(m: Mat3, lab: Label) -> Label:
    """The action of GL(3,2) on the nonzero vectors of F_2^3."""
    return tuple(
        (m[i][0] * lab[0] + m[i][1] * lab[1] + m[i][2] * lab[2]) & 1 for i in range(3)
    )  # type: ignore[return-value]


def find_isomorphism() -> Dict[int, Label] | None:
    """An explicit line-preserving bijection Z_7 -> the nonzero vectors.

    Backtracking over the 6! completions after fixing phi(0) = (1,0,0)
    (the group is transitive, so fixing one image loses no generality).
    Returns None if no isomorphism exists (it does — P4 certifies it).
    """
    z_lines = [tuple(sorted(line)) for line in cyclic_line_triples()]
    b_lines = set(tuple(sorted(line)) for line in binary_lines())
    labels = binary_labels()
    assign: Dict[int, Label] = {0: (1, 0, 0)}
    used = {(1, 0, 0)}

    def consistent() -> bool:
        # every fully-assigned z-line must map onto a binary line
        for line in z_lines:
            if all(i in assign for i in line):
                image = tuple(sorted(assign[i] for i in line))
                if image not in b_lines:
                    return False
        # every fully-assigned PAIR lies on exactly one line of each model
        return True

    def backtrack(next_idx: int) -> Dict[int, Label] | None:
        if next_idx == 7:
            return dict(assign) if consistent() else None
        for lab in labels:
            if lab in used:
                continue
            assign[next_idx] = lab
            used.add(lab)
            if consistent():
                found = backtrack(next_idx + 1)
                if found is not None:
                    return found
            del assign[next_idx]
            used.discard(lab)
        return None

    return backtrack(1)


# ---------------------------------------------------------------------------
# THE FIGURE — the regular heptagon and the seven congruent line-triangles
# ---------------------------------------------------------------------------


def heptagon_angles() -> np.ndarray:
    """Central angles of the seven stations: 2*pi*i/7, i = 0..6."""
    return np.array([TWO_PI * i / 7.0 for i in range(7)])


def heptagon_coordinates(big_r: float = 1.0) -> np.ndarray:
    """Vertex coordinates of the figure: station i at angle 2*pi*i/7.

    Row i holds station i (0-based): Mercury at angle 0, then Venus,
    Mars, Jupiter, Saturn, Uranus, Neptune counter-clockwise. The Sun
    sits at the origin — the centre of the figure, not a vertex.
    """
    ang = heptagon_angles()
    return big_r * np.stack([np.cos(ang), np.sin(ang)], axis=1)


def chord_classes(big_r: float = 1.0) -> Tuple[float, float, float]:
    """The three chord classes of the heptagon: s_1, s_2, s_3.

    s_k = 2R sin(k*pi/7): the side, the short diagonal, the long
    diagonal. Every line of the figure uses one chord of each class.
    """
    return (
        2.0 * big_r * math.sin(math.pi / 7.0),
        2.0 * big_r * math.sin(TWO_PI / 7.0),
        2.0 * big_r * math.sin(3.0 * math.pi / 7.0),
    )


def line_triangle_geometry(verts: Tuple[int, int, int], big_r: float = 1.0) -> Dict[str, object]:
    """Exact planar geometry of one line-triangle of the figure.

    Returns the three sides (sorted ascending), the three interior
    angles (sorted ascending) and the area. For every line the sides
    are (s_1, s_2, s_3) and the angles (pi/7, 2pi/7, 4pi/7) — the
    congruence certified by stage P4.
    """
    xy = heptagon_coordinates(big_r)
    pts = [xy[i] for i in verts]
    sides = []
    for a, b in ((0, 1), (1, 2), (2, 0)):
        sides.append(float(np.hypot(*(pts[a] - pts[b]))))
    sides_sorted = sorted(sides)
    angles = []
    for i in range(3):
        opp = sides[i]
        adj1 = sides[(i + 1) % 3]
        adj2 = sides[(i + 2) % 3]
        cosv = (adj1**2 + adj2**2 - opp**2) / (2.0 * adj1 * adj2)
        angles.append(math.acos(max(-1.0, min(1.0, cosv))))
    area = 0.0
    for i in range(3):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % 3]
        area += x1 * y2 - x2 * y1
    return {
        "sides": sides_sorted,
        "angles": sorted(angles),
        "area": abs(area) / 2.0,
    }


def exact_literals(dps: int = 40) -> Dict[str, str]:
    """The exact dimensions of the figure at `dps` decimal digits.

    Computed with mpmath straight from the closed forms — the pinned
    literals of stage P1 and of the monograph's Theorem A table.
    """
    from mpmath import mp, mpf, sin, pi, sqrt

    mp.dps = dps
    r = mpf(1)
    s1 = 2 * r * sin(pi / 7)
    s2 = 2 * r * sin(2 * pi / 7)
    s3 = 2 * r * sin(3 * pi / 7)
    return {
        "s1": mp.nstr(s1, dps),
        "s2": mp.nstr(s2, dps),
        "s3": mp.nstr(s3, dps),
        "product_s1s2s3": mp.nstr(s1 * s2 * s3, dps),
        "cell_area": mp.nstr(s1 * s2 * s3 / 4, dps),
        "omega7": mp.nstr(3 / (2 * pi), dps),
        "angle1": mp.nstr(pi / 7, dps),
        "angle2": mp.nstr(2 * pi / 7, dps),
        "angle3": mp.nstr(4 * pi / 7, dps),
        "sqrt7": mp.nstr(sqrt(7), dps),
    }


# ---------------------------------------------------------------------------
# The exact vortex registers of the figure (Theorem B)
# ---------------------------------------------------------------------------


def cell_hamiltonian(gamma: float = 1.0, big_r: float = 1.0) -> float:
    """The Hamiltonian of every line-cell, exactly.

    H_cell = -(Gamma^2/2pi) ln(s_1 s_2 s_3 R^3) = -(Gamma^2/2pi)
    ln(sqrt(7) R^3) — the same value for all seven cells (the product
    identity sin(pi/7) sin(2pi/7) sin(3pi/7) = sqrt(7)/8 at work).
    """
    s1, s2, s3 = chord_classes(big_r)
    return -(gamma * gamma / TWO_PI) * math.log(s1 * s2 * s3 * big_r**3)


def ring_hamiltonian(gamma: float = 1.0, big_r: float = 1.0) -> float:
    """The Hamiltonian of the full heptagon ring, exactly.

    The 21 pairwise distances are seven of each chord class, so
    H_ring = -(Gamma^2/2pi) * 7 * ln(sqrt(7) R^3) = 7 * H_cell.
    """
    return 7.0 * cell_hamiltonian(gamma, big_r)


def ring_omega(gamma: float = 1.0, big_r: float = 1.0) -> float:
    """The rigid rotation rate of the heptagon: Gamma*(N-1)/(4 pi R^2).

    At Gamma = R = 1 this is 3/(2*pi) = 0.4774648292756860...  — the
    N = 7 row of the parent polyvortex register (the last Havelock-
    stable level), cross-pinned by the test suite.
    """
    return gamma * 6.0 / (4.0 * math.pi * big_r * big_r)
