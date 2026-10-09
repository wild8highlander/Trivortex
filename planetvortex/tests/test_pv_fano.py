#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
PLANETVORTEX — TESTS: THE PSL(2,7) STRUCTURE AND THE EXACT FIGURE
============================================================================
The exact registers of Layer F: the Fano-plane axioms on Z_7, the two
group models (cyclic permutations and GL(3,2)), the isomorphism, the
geometric congruence of the seven line-triangles and the mpmath-pinned
closed forms of Theorem A.

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from planetvortex import fano as fn

TOL = 1e-12


def test_incidence_axioms() -> None:
    """7 lines of 3 points; every pair of the 21 pairs on exactly one
    line; every point on exactly 3 lines; the {i, i+1, i+3} triples."""
    lines = fn.fano_lines()
    cyclic = [tuple(sorted(l)) for l in fn.cyclic_line_triples()]
    assert len(lines) == 7
    for line in lines:
        assert len(set(line)) == 3
        assert tuple(sorted(line)) in cyclic
    for i in range(7):
        for j in range(i + 1, 7):
            through = [l for l in lines if i in l and j in l]
            assert len(through) == 1
    for i in range(7):
        assert sum(1 for l in lines if i in l) == 3
    assert np.array_equal(fn.incidence_matrix().sum(axis=0), np.full(7, 3))


def test_cyclic_group_order_and_axioms() -> None:
    """PSL(2,7) as 168 line-preserving permutations: closure, identity,
    inverses, point transitivity, stabilizer orders 24."""
    group = fn.automorphism_group()
    assert len(group) == 168
    identity = tuple(range(7))
    assert identity in group
    gset = set(group)
    for a in group:
        for b in group:
            comp = tuple(a[b[i]] for i in range(7))
            assert comp in gset
    for a in group:
        assert any(tuple(a[b[i]] for i in range(7)) == identity for b in group)
    orbit = {perm[0] for perm in group}
    assert orbit == set(range(7))
    assert sum(1 for perm in group if perm[0] == 0) == 24
    lines = fn.fano_lines()
    assert sum(1 for perm in group if tuple(sorted(perm[i] for i in lines[0])) == lines[0]) == 24


def test_gl3_2_model() -> None:
    """The binary model: 168 invertible matrices over F_2, the action
    preserves the line set, and the group is permutation-isomorphic to
    the cyclic copy (the conjugacy register of P4)."""
    group_b = fn.gl3_2()
    assert len(group_b) == 168
    labels = fn.binary_labels()
    lines_b = {tuple(sorted(line)) for line in fn.binary_lines()}
    for m in group_b:
        for line in fn.binary_lines():
            image = tuple(sorted(fn.gl3_2_action(m, lab) for lab in line))
            assert image in lines_b
    # the two groups are the same abstract permutation group
    label_idx = {lab: u for u, lab in enumerate(labels)}
    perms_b = {tuple(label_idx[fn.gl3_2_action(m, lab)] for lab in labels) for m in group_b}
    assert len(perms_b) == 168


def test_isomorphism_cyclic_to_binary() -> None:
    """An explicit line-preserving bijection Z_7 -> F_2^3 exists and
    maps the line set ONTO the binary line set (P4's bridge register)."""
    phi = fn.find_isomorphism()
    assert phi is not None
    labels = fn.binary_labels()
    label_idx = {lab: u for u, lab in enumerate(labels)}
    lines_b_idx = {tuple(sorted(label_idx[lab] for lab in line)) for line in fn.binary_lines()}
    mapped = {tuple(sorted(label_idx[phi[z]] for z in line)) for line in fn.fano_lines()}
    assert mapped == lines_b_idx
    assert len(set(phi.values())) == 7


def test_seven_line_triangles_congruent() -> None:
    """All seven line-triangles: the same sorted sides (s1, s2, s3),
    the same angles (pi/7, 2pi/7, 4pi/7), the same area sqrt(7)/4."""
    ref_sides = None
    ref_angles = None
    for line in fn.fano_lines():
        geom = fn.line_triangle_geometry(line, 1.0)
        sides = np.array(geom["sides"])
        angles = np.array(geom["angles"])
        if ref_sides is None:
            ref_sides = sides
            ref_angles = angles
        assert np.allclose(sides, ref_sides, atol=TOL, rtol=0.0)
        assert np.allclose(angles, ref_angles, atol=TOL, rtol=0.0)
        assert abs(geom["area"] - math.sqrt(7.0) / 4.0) < TOL
    s1, s2, s3 = fn.chord_classes(1.0)
    assert np.allclose(ref_sides, [s1, s2, s3], atol=TOL, rtol=0.0)
    assert np.allclose(ref_angles, [math.pi / 7, 2 * math.pi / 7, 4 * math.pi / 7], atol=TOL)


def test_exact_closed_form_literals() -> None:
    """The float64 figure agrees with the mpmath closed forms at the
    1e-15 band, and the product identity holds: s1*s2*s3 = sqrt(7) R^3."""
    exact = fn.exact_literals(dps=40)
    s1, s2, s3 = fn.chord_classes(1.0)
    assert abs(s1 - float(exact["s1"])) / s1 < 1e-15
    assert abs(s2 - float(exact["s2"])) / s2 < 1e-15
    assert abs(s3 - float(exact["s3"])) / s3 < 1e-15
    assert abs(s1 * s2 * s3 - math.sqrt(7.0)) < 1e-14
    assert abs(s1 * s2 * s3 / 4.0 - float(exact["cell_area"])) < 1e-15
    assert abs(fn.ring_omega(1.0, 1.0) - float(exact["omega7"])) < 1e-15


def test_ring_hamiltonian_closed_form() -> None:
    """The sqrt(7) Hamiltonian identities: H_cell = -(1/2pi)ln(sqrt(7)),
    H_ring = 7 H_cell, both against the numeric Kirchhoff register."""
    from planetvortex import model as md

    gamma = np.ones(7)
    state = md.ring_state(1.0)
    inv = md.invariants(state, gamma)
    assert abs(inv["H"] - fn.ring_hamiltonian(1.0, 1.0)) < 1e-13
    assert abs(fn.ring_hamiltonian(1.0, 1.0) - 7.0 * fn.cell_hamiltonian(1.0, 1.0)) < 1e-15
    # the angular impulse of the ring: sum Gamma |z|^2 = 7
    assert abs(inv["I"] - 7.0) < 1e-12


@pytest.mark.parametrize("k,name", [(0, "Mercury"), (1, "Venus"), (2, "Mars"), (6, "Neptune")])
def test_station_order(k: int, name: str) -> None:
    """The station order is the orbital-period order of the wanderers."""
    assert fn.STATION_NAMES[k] == name
