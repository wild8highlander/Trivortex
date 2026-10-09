#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
PLANETVORTEX — THE KLEIN QUARTIC TESSELLATION (Layer K, stage V2)
============================================================================
The closed gravifigure. Where stage P4 certified the Fano/PSL(2,7)
algebra and stages X3–X4 certified the (2,3,7) triangle generation, the
Klein quartic's smoothness and the exact hyperbolic {7,3} dimensions of
ONE heptagon, stage V2 assembles the FULL 24-heptagon tessellation
{7,3}_8 — the Klein map — as a closed gravitational figure and carries
the mass ladder of the solar system in its register algebra.

Construction (everything from certified models):

    1. G = PSL(2,7) = SL(2,7)/{+-I}, 168 classes of 2x2 matrices
       over F_7 (hardcore.psl_elements — the X1 oracle).
    2. The (2,3,7) witness: involutions a (order 2) x order-3 b with
       |ab| = 7 — the X3 generation search, deterministic first hit.
    3. The coset geometry of the regular map:
           vertices  = right cosets of <b>   (order 3)   -> 56
           edges     = right cosets of <a>   (order 2)   -> 84
           faces     = right cosets of <ab>  (order 7)   -> 24
       with incidence by coset intersection: 3-regular, 7-gonal
       faces, V - E + F = -4 (genus 3).
    4. The flag certificate: the 336 flags of the map (white = the
       168 nonempty triple intersections, black = the 168 empty ones)
       carry the wall moves rho_f, rho_v, rho_e (change face / vertex
       / edge, each an involution). In the PGL(2,7) model (336 classes
       over F_7, the full automorphism group) the moves are the RIGHT
       MULTIPLICATIONS by the three involutions of a (2,3,7) Coxeter
       triple — verified on all 336 x 3 flag-move instances. The full
       flag action of the map is simply transitive: the map is regular.
    5. The chamber patch: the barycentric (2,3,7) chambers of the
       Poincare-disk tiling are grown by reflection, each tracked by
       its PGL class (crossing a wall = right multiplication by the
       wall's involution). The patch closes after exactly 336
       chambers — one per PGL class, all geometric positions distinct
       — forming 24 heptagons whose 168 sides pair onto 84 map edges:
       the classical Klein quartic fundamental domain.
    6. The antipodal pairing: the witness involution a acts on the 24
       faces WITHOUT fixed points (an order-2 element cannot lie in a
       conjugate of the order-7 face stabilizer) -> 12 antipodal
       pairs — one per gravimetric register.
    7. The gravimetric register algebra: 12 bodies (the Sun, the
       eight planets, Ceres, Pluto, Eris) with the committed GM
       table; s_i = ln GM_i - mean(ln GM) — the geometric-mean
       normalization, summing to ZERO exactly; the vertex-angle
       register
           alpha_i = 2*pi/3 - sigma * s_i,
       sigma scaled so the lightest register keeps a registered
       margin under the Euclidean ceiling 5*pi/7 (the {7,3}
       hyperbolicity bound). Per-register exact dimensions (the X4
       closed forms at variable vertex angle):
           cosh R_i    = cot(alpha_i/2) cot(pi/7)
           cosh(l_i/2) = cos(pi/7) / sin(alpha_i/2)
           cosh r_i    = cos(alpha_i/2) / sin(pi/7)
           A_i         = 5*pi - 7*alpha_i     (Gauss-Bonnet per cell)
       THE BUDGET CLOSURE (Theorem G): sum(alpha_i) = 8*pi exactly,
       because sum(s_i) = 0 exactly — the decorated tessellation of
       12 antipodal pairs closes on the Gauss-Bonnet area
       2*pi*(2g-2) = 8*pi of the Klein quartic. The Euler
       characteristic absorbs the mass ladder.

License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
Year: 2026
============================================================================
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from itertools import product
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

import numpy as np

from . import classical as cl
from .hardcore import Mat2, _psl_mult_table, _psl_order, psl_elements, psl_rep

TWO_PI = 2.0 * math.pi

# ---------------------------------------------------------------------------
# Registered tolerances of the V2 stage (committed before the recorded runs)
# ---------------------------------------------------------------------------

V2_TOLERANCES: Dict[str, float] = {
    "witness_abs": 1e-9,  # the Poincare-disk witness vs the closed forms
    "witness_angle_abs": 1e-12,  # the witness vertex angle vs alpha_i
    "s_sum_rel": 1e-9,  # the float geometric-mean normalization
    "float_budget": 1e-9,  # the float64 budget residuals
    "float_pythagoras": 1e-12,  # the float64 Pythagoras residual
    "hyperbolicity_margin": 0.005,  # min margin under the ceiling 5*pi/7
}

V2_PRESETS: Dict[str, Dict[str, Any]] = {
    "quick": {"dps": 30, "ceiling_margin": 0.05},
    "default": {"dps": 50, "ceiling_margin": 0.05},
    "full": {"dps": 60, "ceiling_margin": 0.05},
}

# ---------------------------------------------------------------------------
# The gravimetric register: 12 bodies of the solar system (committed table)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Body:
    """One row of the V2 gravimetric register.

    gm: G*M, m^3/s^2 (NASA NSSDC / JPL SBDB, committed verbatim);
    kind: 'star' | 'planet' | 'dwarf'.
    """

    name: str
    gm: float
    kind: str


BODIES: Tuple[Body, ...] = (
    Body("Sun", cl.GM_SUN, "star"),
    Body("Mercury", 2.2032e13, "planet"),
    Body("Venus", 3.24859e14, "planet"),
    Body("Earth", 3.986004418e14, "planet"),
    Body("Mars", 4.282837e13, "planet"),
    Body("Jupiter", 1.26686534e17, "planet"),
    Body("Saturn", 3.7931187e16, "planet"),
    Body("Uranus", 5.793939e15, "planet"),
    Body("Neptune", 6.836529e16, "planet"),
    Body("Ceres", 6.26325e10, "dwarf"),
    Body("Pluto", 8.696e11, "dwarf"),
    Body("Eris", 1.108e12, "dwarf"),
)

N_BODIES = len(BODIES)  # 12 — one antipodal pair of heptagons per body

EUCLIDEAN_CEILING = 5.0 * math.pi / 7.0  # the {7,3} hyperbolicity bound
REGULAR_ANGLE = TWO_PI / 3.0  # the undecorated vertex angle of {7,3}
TOTAL_AREA = 8.0 * math.pi  # 2*pi*(2g-2), g = 3 — the Gauss-Bonnet budget


def body_names() -> Tuple[str, ...]:
    """The 12 registered body names in table order."""
    return tuple(b.name for b in BODIES)


# ---------------------------------------------------------------------------
# The exact register algebra (mpmath) and its float shadow
# ---------------------------------------------------------------------------


def _sigma_scale(s_values: Sequence[float], ceiling_margin: float = 0.05) -> float:
    """sigma of the angle register: the lightest register keeps
    `ceiling_margin` of the headroom (2*pi/3 -> 5*pi/7) untouched."""
    headroom = EUCLIDEAN_CEILING - REGULAR_ANGLE  # pi/21
    worst_negative = max(-s for s in s_values)
    return (1.0 - ceiling_margin) * headroom / worst_negative


def register_dims(alpha: float) -> Tuple[float, float, float, float]:
    """The exact closed-form dimensions of one regular register
    heptagon of vertex angle alpha (the X4 forms at variable angle):
    returns (circumradius R, edge l, inradius r, area A)."""
    big_r = math.acosh((1.0 / math.tan(alpha / 2.0)) * (1.0 / math.tan(math.pi / 7.0)))
    half_edge = math.acosh(math.cos(math.pi / 7.0) / math.sin(alpha / 2.0))
    inradius = math.acosh(math.cos(alpha / 2.0) / math.sin(math.pi / 7.0))
    area = 5.0 * math.pi - 7.0 * alpha
    return big_r, 2.0 * half_edge, inradius, area


def register_algebra_float(ceiling_margin: float = 0.05) -> Dict[str, Any]:
    """The float64 register algebra of the 12 bodies.

    Returns the normalized log-gravity ladder s_i (summing to zero),
    the sigma scale, the vertex angles alpha_i, the per-register
    closed-form dimensions and the budget residuals.
    """
    ln_gm = np.array([math.log(b.gm) for b in BODIES])
    mean_ln = float(np.mean(ln_gm))
    s = ln_gm - mean_ln  # sums to zero up to float roundoff
    sigma = _sigma_scale(s, ceiling_margin)
    alpha = REGULAR_ANGLE - sigma * s

    rows = []
    pyth = 0.0
    for body, s_i, a_i in zip(BODIES, s, alpha):
        big_r, edge, inr, area = register_dims(float(a_i))
        # the hyperbolic Pythagoras: cosh R = cosh(edge/2) * cosh r
        resid = abs(math.cosh(big_r) - math.cosh(edge / 2.0) * math.cosh(inr))
        pyth = max(pyth, resid / max(math.cosh(big_r), 1.0))
        rows.append(
            {
                "body": body.name,
                "kind": body.kind,
                "gm": body.gm,
                "s": float(s_i),
                "alpha": float(a_i),
                "circumradius": big_r,
                "edge": edge,
                "inradius": inr,
                "area": area,
                "pythagoras_residual": resid,
            }
        )
    alpha_sum = float(np.sum(alpha))
    area_sum = float(np.sum(2.0 * np.array([r["area"] for r in rows])))
    return {
        "bodies": rows,
        "sigma": sigma,
        "s_sum": float(np.sum(s)),
        "alpha_sum": alpha_sum,
        "alpha_sum_residual": abs(alpha_sum - TOTAL_AREA),
        "total_area": area_sum,
        "total_area_residual": abs(area_sum - TOTAL_AREA),
        "worst_pythagoras_residual": pyth,
        "min_hyperbolicity_margin": float(EUCLIDEAN_CEILING - alpha.max()),
        "ceiling_margin_setting": ceiling_margin,
    }


def register_algebra_exact(dps: int = 50, ceiling_margin: float = 0.05) -> Dict[str, Any]:
    """The register algebra at `dps` decimal digits (mpmath, strings).

    Every quantity is computed straight from the closed forms — the
    budget closure sum(alpha) - 8*pi and the area closure
    sum(2*A_i) - 8*pi are pinned to O(10^(2-dps)).
    """
    from mpmath import mp, mpf, acosh, cos, log, pi as mpi, sin, tan

    mp.dps = dps
    ln_gm = [log(mpf(repr(b.gm))) for b in BODIES]
    mean_ln = sum(ln_gm) / len(ln_gm)
    s = [v - mean_ln for v in ln_gm]
    s_sum = sum(s)
    headroom = mpi * 5 / 7 - mpi * 2 / 3
    worst_neg = max(-v for v in s)
    sigma = (mpf(1) - mpf(repr(ceiling_margin))) * headroom / worst_neg
    a_pi7 = mpi / 7

    rows = []
    alpha_sum = mpf(0)
    area_sum = mpf(0)
    pyth = mpf(0)
    for body, s_i in zip(BODIES, s):
        alpha = mpi * 2 / 3 - sigma * s_i
        ch_r = (1 / tan(alpha / 2)) * (1 / tan(a_pi7))
        ch_half = cos(a_pi7) / sin(alpha / 2)
        ch_r_in = cos(alpha / 2) / sin(a_pi7)
        area = mpi * 5 - 7 * alpha
        pyth = max(pyth, abs(ch_r - ch_half * ch_r_in))
        alpha_sum += alpha
        area_sum += 2 * area
        rows.append(
            {
                "body": body.name,
                "s": mp.nstr(s_i, dps),
                "alpha": mp.nstr(alpha, dps),
                "cosh_circumradius": mp.nstr(ch_r, dps),
                "circumradius": mp.nstr(acosh(ch_r), dps),
                "edge": mp.nstr(2 * acosh(ch_half), dps),
                "inradius": mp.nstr(acosh(ch_r_in), dps),
                "area": mp.nstr(area, dps),
            }
        )
    id_tol = mpf(10) ** (2 - dps)
    return {
        "dps": dps,
        "bodies": rows,
        "s_sum": mp.nstr(s_sum, dps),
        "sigma": mp.nstr(sigma, dps),
        "alpha_sum": mp.nstr(alpha_sum, dps),
        "alpha_sum_residual": mp.nstr(abs(alpha_sum - 8 * mpi), dps),
        "total_area_residual": mp.nstr(abs(area_sum - 8 * mpi), dps),
        "worst_pythagoras_residual": mp.nstr(pyth, dps),
        "identity_tolerance": mp.nstr(id_tol, dps),
        "budget_ok": bool(abs(alpha_sum - 8 * mpi) <= id_tol),
        "area_ok": bool(abs(area_sum - 8 * mpi) <= id_tol),
        "pythagoras_ok": bool(pyth <= id_tol),
        "s_sum_ok": bool(abs(s_sum) <= id_tol),
    }


# ---------------------------------------------------------------------------
# The (2,3,7) witness and the coset geometry of the Klein map
# ---------------------------------------------------------------------------


@dataclass
class KleinMap:
    """The Klein map {7,3}_8 as the coset geometry of PSL(2,7).

    vertices/edges/faces: the right cosets of <b>, <a>, <ab> (each a
    frozenset of group-element indices, canonically ordered by the min
    index). Incidence lists are index-based and separated by kind.
    """

    witness_a: int
    witness_b: int
    product_c: int
    elements: List[Mat2] = field(repr=False, default_factory=list)
    table: List[List[int]] = field(repr=False, default_factory=list)
    vertices: List[frozenset] = field(default_factory=list)
    edges: List[frozenset] = field(default_factory=list)
    faces: List[frozenset] = field(default_factory=list)
    vertex_edges: List[Tuple[int, int]] = field(default_factory=list)
    edge_vertices: List[Tuple[int, int]] = field(default_factory=list)
    edge_faces: List[Tuple[int, int]] = field(default_factory=list)
    face_edges: List[Tuple[int, ...]] = field(default_factory=list)
    antipodal_pairs: List[Tuple[int, int]] = field(default_factory=list)

    # -- construction ------------------------------------------------------

    @classmethod
    def build(cls) -> KleinMap:
        """The deterministic construction from the certified X1 model."""
        elems = psl_elements()
        table = _psl_mult_table(elems)
        identity = elems.index((1, 0, 0, 1))
        orders = [_psl_order(table, i, identity) for i in range(len(elems))]
        involutions = [i for i, n in enumerate(orders) if n == 2]
        order3 = [i for i, n in enumerate(orders) if n == 3]
        witness: Tuple[int, int] | None = None
        for a in involutions:
            for b in order3:
                if orders[table[a][b]] == 7:
                    witness = (a, b)
                    break
            if witness:
                break
        if witness is None:  # pragma: no cover — X3 certifies existence
            raise RuntimeError("no (2,3,7) witness in PSL(2,7)")
        a, b = witness
        c = table[a][b]

        def right_cosets(gen: int) -> List[frozenset]:
            """{g·h : h in <gen>} for all g — the canonical coset list."""
            cyc = [identity]
            nxt = gen
            while nxt != identity:
                cyc.append(nxt)
                nxt = table[nxt][gen]
            member_coset: Dict[int, frozenset] = {}
            for g in range(len(elems)):
                if g in member_coset:
                    continue
                cell = frozenset(table[g][h] for h in cyc)
                for m in cell:
                    member_coset[m] = cell
            return sorted(set(member_coset.values()), key=lambda fs: min(fs))

        km = cls(witness_a=a, witness_b=b, product_c=c, elements=elems, table=table)
        km.vertices = right_cosets(b)
        km.edges = right_cosets(a)
        km.faces = right_cosets(c)

        # incidence by coset intersection, separated by kind
        n_v, n_e, n_f = len(km.vertices), len(km.edges), len(km.faces)
        ve: List[Set[int]] = [set() for _ in range(n_v)]
        ev: List[Set[int]] = [set() for _ in range(n_e)]
        ef: List[Set[int]] = [set() for _ in range(n_e)]
        fe: List[Set[int]] = [set() for _ in range(n_f)]
        for ei, edge in enumerate(km.edges):
            for vi, vert in enumerate(km.vertices):
                if edge & vert:
                    ve[vi].add(ei)
                    ev[ei].add(vi)
            for fi, face in enumerate(km.faces):
                if edge & face:
                    ef[ei].add(fi)
                    fe[fi].add(ei)
        km.vertex_edges = [tuple(sorted(s)) for s in ve]
        km.edge_vertices = [tuple(sorted(s)) for s in ev]
        km.edge_faces = [tuple(sorted(s)) for s in ef]
        km.face_edges = [tuple(sorted(s)) for s in fe]
        km.antipodal_pairs = km._antipodal_pairs(a)
        return km

    def _antipodal_pairs(self, involution: int) -> List[Tuple[int, int]]:
        """The witness involution acts on the face cosets by left
        multiplication; no face is fixed (an order-2 element cannot sit
        in a conjugate of the order-7 stabilizer), so the action is a
        perfect pairing into 12 antipodal pairs."""
        f_index = {fs: i for i, fs in enumerate(self.faces)}
        action: Dict[int, int] = {}
        for face in self.faces:
            moved = frozenset(self.table[involution][m] for m in face)
            action[f_index[face]] = f_index[moved]
        pairs: List[Tuple[int, int]] = []
        seen: Set[int] = set()
        for f in sorted(action):
            if f in seen:
                continue
            other = action[f]
            if other == f:  # pragma: no cover — the lemma forbids it
                raise RuntimeError("the antipodal action has a fixed face")
            pairs.append((f, other))
            seen.add(f)
            seen.add(other)
        return sorted(pairs)

    # -- registers ---------------------------------------------------------

    def register_summary(self) -> Dict[str, Any]:
        """The exact combinatorial registers of the map."""
        v, e, f = len(self.vertices), len(self.edges), len(self.faces)
        degrees = sorted({len(x) for x in self.vertex_edges})
        face_lens = sorted({len(x) for x in self.face_edges})
        valences = sorted({len(x) for x in self.edge_faces} | {len(x) for x in self.edge_vertices})
        return {
            "V": v,
            "E": e,
            "F": f,
            "euler": v - e + f,
            "vertex_degrees": degrees,
            "face_lengths": face_lens,
            "edge_valences": valences,
            "n_antipodal_pairs": len(self.antipodal_pairs),
            "incidence_products": {"3V": 3 * v, "2E": 2 * e, "7F": 7 * f},
        }

    def is_connected(self) -> bool:
        """BFS over the vertex-edge adjacency."""
        adj: List[Set[int]] = [set() for _ in range(len(self.vertices))]
        for vi, eis in enumerate(self.vertex_edges):
            for ei in eis:
                adj[vi].update(self.edge_vertices[ei])
        seen = {0}
        frontier = [0]
        while frontier:
            nxt = []
            for u in frontier:
                for w in adj[u]:
                    if w not in seen:
                        seen.add(w)
                        nxt.append(w)
            frontier = nxt
        return len(seen) == len(self.vertices)

    def is_orientable(self) -> bool:
        """A map is orientable iff its full flag graph is bipartite.

        The 336 pairwise-incident (v, e, f) triples form the flag set;
        two flags are adjacent when they differ in exactly one member.
        Bipartiteness is checked by 2-coloring BFS.
        """
        flags = self.all_flags()
        n = len(flags)
        adjacency: List[Set[int]] = [set() for _ in range(n)]
        groups: List[Dict[Tuple[int, int], List[int]]] = [{}, {}, {}]
        for i, (v, e, f) in enumerate(flags):
            for slot, key in ((0, (v, e)), (1, (e, f)), (2, (v, f))):
                groups[slot].setdefault(key, []).append(i)
        for bucket in groups:
            for members in bucket.values():
                if len(members) != 2:  # pragma: no cover — polyhedral map
                    raise RuntimeError("flag adjacency corrupted")
                x, y = members
                adjacency[x].add(y)
                adjacency[y].add(x)
        color = [-1] * n
        color[0] = 0
        frontier = [0]
        while frontier:
            nxt = []
            for u in frontier:
                for w in adjacency[u]:
                    if color[w] == -1:
                        color[w] = 1 - color[u]
                        nxt.append(w)
                    elif color[w] == color[u]:
                        return False
            frontier = nxt
        return all(c >= 0 for c in color)

    # -- flags -------------------------------------------------------------

    def all_flags(self) -> List[Tuple[int, int, int]]:
        """The 336 flags: the pairwise-incident (v, e, f) triples."""
        out: List[Tuple[int, int, int]] = []
        for ei in range(len(self.edges)):
            for vi in self.edge_vertices[ei]:
                for fi in self.edge_faces[ei]:
                    out.append((vi, ei, fi))
        return sorted(out)

    def flag_triple_element(self, flag: Tuple[int, int, int]) -> int | None:
        """The unique PSL element of the flag's triple intersection
        (None for the black flags — the empty intersections)."""
        v, e, f = flag
        common = self.vertices[v] & self.edges[e] & self.faces[f]
        if len(common) == 1:
            return next(iter(common))
        return None

    def element_face(self, elem_index: int) -> int:
        """The face coset containing the given PSL element."""
        for fi, fs in enumerate(self.faces):
            if elem_index in fs:
                return fi
        raise RuntimeError("element not in any face")  # pragma: no cover

    def element_edge(self, elem_index: int) -> int:
        """The edge coset containing the given PSL element."""
        for ei, fs in enumerate(self.edges):
            if elem_index in fs:
                return ei
        raise RuntimeError("element not in any edge")  # pragma: no cover


# ---------------------------------------------------------------------------
# PGL(2,7) — the full automorphism model (336 classes over F_7)
# ---------------------------------------------------------------------------

_F7_INV = {1: 1, 2: 4, 3: 5, 4: 2, 5: 3, 6: 6}


def _pgl_canon(a: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
    """The canonical representative of the PGL class: scale so the
    first nonzero entry (row-major) becomes 1."""
    s = 1
    for x in a:
        if x:
            s = _F7_INV[x]
            break
    return tuple((v * s) % 7 for v in a)


def _pgl_mul(
    a: Tuple[int, int, int, int], b: Tuple[int, int, int, int]
) -> Tuple[int, int, int, int]:
    return (
        (a[0] * b[0] + a[1] * b[2]) % 7,
        (a[0] * b[1] + a[1] * b[3]) % 7,
        (a[2] * b[0] + a[3] * b[2]) % 7,
        (a[2] * b[1] + a[3] * b[3]) % 7,
    )


def _pgl_det(a: Tuple[int, int, int, int]) -> int:
    return (a[0] * a[3] - a[1] * a[2]) % 7


class PGLModel:
    """PGL(2,7): the 336 classes, the multiplication table, the PSL
    index-2 subset (square determinants) and the (2,3,7) Coxeter
    triple of wall involutions."""

    def __init__(self) -> None:
        elems = sorted({_pgl_canon(m) for m in product(range(7), repeat=4) if _pgl_det(m)})
        self.elements = elems
        self.index = {m: i for i, m in enumerate(elems)}
        n = len(elems)
        self.table = [
            [self.index[_pgl_canon(_pgl_mul(elems[i], elems[j]))] for j in range(n)]
            for i in range(n)
        ]
        self.identity = self.index[_pgl_canon((1, 0, 0, 1))]
        self.is_psl = [_pgl_det(m) in (1, 2, 4) for m in elems]

    def order(self, i: int) -> int:
        p = i
        for n in range(1, 50):
            if p == self.identity:
                return n
            p = self.table[p][i]
        raise RuntimeError("PGL element order > 49")  # pragma: no cover

    _SQRT_F7 = {1: 1, 2: 3, 4: 2}  # the square roots of the quadratic residues

    def psl_to_hardcore(self, i: int) -> Mat2:
        """The PSL class i (square determinant) as a hardcore
        psl_elements() representative: scale by lambda with
        lambda^2 * det = 1."""
        m = self.elements[i]
        d = _pgl_det(m)
        lam = _F7_INV[self._SQRT_F7[d]]
        scaled = tuple((v * lam) % 7 for v in m)  # determinant 1
        return psl_rep(scaled)

    def find_coxeter_triple(self, face_class: int | None = None) -> Tuple[int, int, int]:
        """The deterministic (2,3,7) wall-involution triple (x, y, z):
        (y z)^7 = 1, (x z)^3 = 1, (x y)^2 = 1, generating all 336 —
        x = the (v,m)-wall, y = the (m,c)-wall, z = the (c,v)-wall.

        When `face_class` (the PGL class of the witness face rotation
        c) is given, the triple is additionally pinned to the UNtwisted
        identification: y z must lie in <face_class> — the radial
        reflections y, z then belong to the base face's own D7
        stabilizer, the tile of the identity chamber carries exactly
        the face coset <c>, and the PGL class of a white chamber equals
        the PGL class of its triple element (the bridge is the
        identity on matrices).
        """
        involutions = [i for i in range(336) if self.order(i) == 2 and i != self.identity]
        face_powers: Set[int] | None = None
        if face_class is not None:
            inverse = next(j for j in range(336) if self.table[face_class][j] == self.identity)
            face_powers = {face_class, inverse}

        def close_enough(y: int, z: int) -> bool:
            yz = self.table[y][z]
            if self.order(yz) != 7:
                return False
            if face_powers is not None and yz not in face_powers:
                return False
            return True

        for x in involutions:
            for y in involutions:
                for z in involutions:
                    if not close_enough(y, z):
                        continue
                    if self.order(self.table[x][z]) != 3:
                        continue
                    if self.order(self.table[x][y]) != 2:
                        continue
                    if self.closure_size((x, y, z)) == 336:
                        return (x, y, z)
        raise RuntimeError("no (2,3,7) Coxeter triple in PGL(2,7)")  # pragma: no cover

    def closure_size(self, gens: Sequence[int]) -> int:
        seen = {self.identity, *gens}
        frontier = list(gens)
        while frontier:
            u = frontier.pop()
            for w in gens:
                uw = self.table[u][w]
                if uw not in seen:
                    seen.add(uw)
                    frontier.append(uw)
        return len(seen)


# ---------------------------------------------------------------------------
# Poincare-disk primitives
# ---------------------------------------------------------------------------


def _geodesic_circle(u: complex, v: complex) -> Tuple[complex, float] | None:
    """Center w and radius rho of the geodesic circle through u, v
    (orthogonal to the unit circle); None when the geodesic is a
    diameter (u, v, 0 collinear)."""
    det = u.real * v.imag - u.imag * v.real
    if abs(det) < 1e-13:
        return None
    m = np.array([[u.real, u.imag], [v.real, v.imag]])
    rhs = np.array([(1.0 + abs(u) ** 2) / 2.0, (1.0 + abs(v) ** 2) / 2.0])
    wx, wy = np.linalg.solve(m, rhs)
    w = complex(wx, wy)
    rho = math.sqrt(max(abs(w) ** 2 - 1.0, 0.0))
    return w, rho


def _reflect(p: complex, u: complex, v: complex) -> complex:
    """Reflect the disk point p across the geodesic through u, v."""
    circ = _geodesic_circle(u, v)
    if circ is None:
        # the geodesic is the diameter through u and v: reflection in
        # that line — the direction must come from the NONZERO endpoint
        w = u if abs(u) >= abs(v) else v
        theta = math.atan2(w.imag, w.real)
        return complex(math.cos(2.0 * theta), math.sin(2.0 * theta)) * p.conjugate()
    w, rho = circ
    z = p - w
    return w + rho * rho / z.conjugate()


def _disk_midpoint(u: complex, v: complex) -> complex:
    """The hyperbolic midpoint of the geodesic segment (u, v): the
    Euclidean midpoint of the Klein-model image."""
    ku = 2.0 * u / (1.0 + abs(u) ** 2)
    kv = 2.0 * v / (1.0 + abs(v) ** 2)
    kmid = (ku + kv) / 2.0
    return kmid / (1.0 + math.sqrt(max(0.0, 1.0 - abs(kmid) ** 2)))


def central_heptagon() -> List[complex]:
    """The canonical regular {7,3} heptagon centered at the disk center:
    the X4 closed forms put the vertices at the Euclidean radius
    t = tanh(R/2), R = arccosh(cot(pi/3) cot(pi/7))."""
    big_r = math.acosh((1.0 / math.tan(math.pi / 3.0)) * (1.0 / math.tan(math.pi / 7.0)))
    t = math.tanh(big_r / 2.0)
    return [
        complex(
            t * math.cos(TWO_PI * k / 7.0 + math.pi / 7.0),
            t * math.sin(TWO_PI * k / 7.0 + math.pi / 7.0),
        )
        for k in range(7)
    ]


def _grid(p: complex) -> Tuple[int, int]:
    """The geometric grid key (absorbs the float64 reflection noise)."""
    return (int(round(p.real * 1e8)), int(round(p.imag * 1e8)))


# ---------------------------------------------------------------------------
# The chamber patch: 336 barycentric chambers <-> PGL(2,7)
# ---------------------------------------------------------------------------


@dataclass
class HeptagonCell:
    """One of the 24 tessellation cells, extracted from the chambers."""

    face_coset: int  # the Klein-map face index
    vertices: List[complex]  # 7 disk positions, CCW
    midpoints: List[complex]  # 7 edge midpoints, aligned with the edges
    center: complex
    psl_images: List[int]  # the 7 PSL classes of its white chambers
    side_edges: List[int]  # the 7 map-edge ids of its sides


@dataclass
class ChamberPatch:
    """The fundamental domain: 336 chambers, 24 heptagons, 84 map
    edges (interior sides + boundary pairs) — plus the flag
    certificate of the PGL action."""

    chambers: int = 0
    heptagons: List[HeptagonCell] = field(default_factory=list)
    interior_sides: int = 0
    boundary_pairs: List[Tuple[Tuple[int, int], Tuple[int, int]]] = field(default_factory=list)
    flag_certificate: bool = False
    coxeter_triple: Tuple[int, int, int] = (0, 0, 0)
    errors: List[str] = field(default_factory=list)

    def summary(self) -> Dict[str, Any]:
        return {
            "chambers": self.chambers,
            "n_heptagons": len(self.heptagons),
            "interior_sides": self.interior_sides,
            "n_boundary_pairs": len(self.boundary_pairs),
            "n_map_edges": self.interior_sides + len(self.boundary_pairs),
            "heptagon_sides": 7 * len(self.heptagons),
            "flag_certificate": self.flag_certificate,
            "coxeter_triple": self.coxeter_triple,
            "errors": self.errors,
        }


def _other_member(pair: Tuple[int, ...], x: int) -> int:
    """The other member of a 2-tuple."""
    a, b = pair
    return b if x == a else a


def _corner_partner_edge(km: KleinMap, v: int, f: int, e: int) -> int:
    """The other edge of the corner (v, f): the edge != e incident to
    both the vertex v and the face f."""
    for ei in km.vertex_edges[v]:
        if ei != e and fi_in_edge_face(km, ei, f):
            return ei
    raise RuntimeError("no partner edge at the corner")  # pragma: no cover


def fi_in_edge_face(km: KleinMap, ei: int, fi: int) -> bool:
    return fi in km.edge_faces[ei]


def flag_certificate(
    km: KleinMap, pgl: PGLModel, triple: Tuple[int, int, int]
) -> Tuple[Dict[Tuple[int, int, int], int] | None, int]:
    """The PGL flag certificate: the quotient map's three wall moves
    are the right multiplications by (x, y, z) on the 336 flags.

    Returns (phi, n_flags): phi maps every flag to its PGL class (the
    simply transitive identification), or (None, n) on inconsistency.
    """
    x, y, z = triple
    flags = km.all_flags()
    base = None
    for flag in flags:
        elem = km.flag_triple_element(flag)
        if elem is not None and km.elements[elem] == (1, 0, 0, 1):
            base = flag
            break
    if base is None:
        return None, 0
    phi: Dict[Tuple[int, int, int], int] = {base: pgl.identity}
    queue = [base]
    consistent = True
    while queue and consistent:
        w = queue.pop(0)
        v, e, f = w
        moves = (
            ((v, e, _other_member(km.edge_faces[e], f)), x),  # rho_f
            ((_other_member(km.edge_vertices[e], v), e, f), y),  # rho_v
            ((v, _corner_partner_edge(km, v, f, e), f), z),  # rho_e
        )
        for w2, sigma in moves:
            if w2 not in phi:
                phi[w2] = pgl.table[phi[w]][sigma]
                queue.append(w2)
            elif phi[w2] != pgl.table[phi[w]][sigma]:
                consistent = False
                break
    if not (consistent and len(phi) == 336):
        return None, len(phi)
    return phi, 336


def build_chamber_patch(km: KleinMap) -> ChamberPatch:
    """Grow the fundamental domain heptagon by heptagon.

    The barycentric chamber (v, m, c) — vertex, edge midpoint, face
    center — carries its PGL class phi(flag); crossing a wall
    multiplies the class by the wall's Coxeter involution (the simply
    transitive chamber action, certified by flag_certificate). Each
    tessellation heptagon is the right coset iH, H = <y, z> (the D7
    stabilizer): its 14 chambers are placed CO-LOCATED by the y/z-walk
    (the radial walls keep the chamber inside its tile). The BFS over
    tiles closes after exactly 24 tiles = 336 chambers. The quotient
    flag of every placed chamber is recovered as phi^{-1}(image), so
    the face and edge cosets of the extracted cells come straight from
    the certified flag correspondence.
    """
    patch = ChamberPatch()
    pgl = PGLModel()
    c_class = pgl.index[_pgl_canon(km.elements[km.product_c])]
    x, y, z = pgl.find_coxeter_triple(c_class)
    patch.coxeter_triple = (x, y, z)

    phi, n_phi = flag_certificate(km, pgl, (x, y, z))
    if phi is None:
        patch.flag_certificate = False
        patch.errors.append(f"the PGL flag certificate failed at {n_phi} flags")
        return patch
    patch.flag_certificate = True
    inv_phi = {img: flag for flag, img in phi.items()}
    flag_face = {flag: flag[2] for flag in inv_phi.values()}

    # the tile stabilizer H = <y, z> (order 14, the D7 of the tile)
    h_set = {pgl.identity}
    frontier = [y, z]
    while frontier:
        u = frontier.pop()
        for w in (y, z):
            uw = pgl.table[u][w]
            if uw not in h_set:
                h_set.add(uw)
                frontier.append(uw)
    h_list = sorted(h_set)
    if len(h_list) != 14:
        patch.errors.append("the tile stabilizer is not 14")
        return patch
    coset_rep: Dict[int, int] = {}
    for i in range(336):
        cell = frozenset(pgl.table[i][h] for h in h_list)
        r = min(cell)
        for m_idx in cell:
            coset_rep[m_idx] = r

    # -- geometry helpers (a chamber is a triple (v, m, c)) --------------
    def cross_vm(pos):
        v, m, c = pos
        return (v, m, _reflect(c, v, m))

    def cross_mc(pos):
        v, m, c = pos
        return (_reflect(v, m, c), m, c)

    def cross_cv(pos):
        v, m, c = pos
        return (v, _reflect(m, c, v), c)

    placed_tiles: Dict[int, Dict[int, Tuple[complex, complex, complex]]] = {}
    placed_images: Set[int] = set()

    def grow_tile(enter_image: int, enter_pos):
        """Place the whole 14-chamber tile of the coset of enter_image,
        co-located, by the y/z-walk from the entering chamber."""
        tile = {enter_image: enter_pos}
        queue = [enter_image]
        while queue:
            img = queue.pop(0)
            pos = tile[img]
            for sigma, cross in ((y, cross_mc), (z, cross_cv)):
                across = pgl.table[img][sigma]
                if across in tile:
                    continue
                if across in placed_images:
                    return None
                tile[across] = cross(pos)
                queue.append(across)
        if len(tile) != 14:
            return None
        # every chamber of the tile must project into ONE face
        faces = {flag_face[inv_phi[img]] for img in tile}
        if len(faces) != 1:
            return None
        return tile

    # -- the base tile ----------------------------------------------------
    verts = central_heptagon()
    v0 = verts[0]
    m0 = _disk_midpoint(verts[0], verts[1])
    c0 = complex(0.0, 0.0)
    base_img = pgl.identity
    base_rep = coset_rep[base_img]
    base_tile = {base_img: (v0, m0, c0)}
    queue = [base_img]
    while queue:
        img = queue.pop(0)
        pos = base_tile[img]
        for sigma, cross in ((y, cross_mc), (z, cross_cv)):
            across = pgl.table[img][sigma]
            if across not in base_tile:
                base_tile[across] = cross(pos)
                queue.append(across)
    if len(base_tile) != 14:
        patch.errors.append("the base tile did not grow to 14 chambers")
        return patch
    if len({flag_face[inv_phi[i]] for i in base_tile}) != 1:
        patch.errors.append("the base tile spans 2+ faces")
        return patch
    placed_tiles[base_rep] = base_tile
    placed_images.update(base_tile)

    # -- the tile BFS ------------------------------------------------------
    entry_queue = []
    for img, pos in base_tile.items():
        across_img = pgl.table[img][x]
        across_rep = coset_rep[across_img]
        if across_rep != base_rep:
            entry_queue.append((across_rep, across_img, cross_vm(pos)))
    while entry_queue:
        rep, enter_image, enter_pos = entry_queue.pop(0)
        if rep in placed_tiles:
            continue
        tile = grow_tile(enter_image, enter_pos)
        if tile is None:
            patch.errors.append("a tile conflicted or spanned 2+ faces")
            return patch
        placed_tiles[rep] = tile
        placed_images.update(tile)
        for img, pos in tile.items():
            across_img = pgl.table[img][x]
            across_rep = coset_rep[across_img]
            if across_rep not in placed_tiles:
                entry_queue.append((across_rep, across_img, cross_vm(pos)))

    if len(placed_tiles) != 24:
        patch.errors.append(f"tiles={len(placed_tiles)} != 24")
        return patch
    all_chambers = [i for t in placed_tiles.values() for i in t]
    if len(all_chambers) != 336 or len(set(all_chambers)) != 336:
        patch.errors.append("the tiles do not partition the 336 chambers")
        return patch
    patch.chambers = 336
    pos_keys = set()
    for tile in placed_tiles.values():
        for v, m, c in tile.values():
            gk = (_grid(v), _grid(m), _grid(c))
            if gk in pos_keys:
                patch.errors.append("two chambers share a geometric position")
                return patch
            pos_keys.add(gk)

    # -- extract the 24 cells (face/edge cosets straight from the flags) --
    for rep in sorted(placed_tiles):
        tile = placed_tiles[rep]
        faces = {flag_face[inv_phi[img]] for img in tile}
        face_coset = faces.pop()
        center = next(iter(tile.values()))[2]
        chambers = [(img, tile[img][0], tile[img][1], inv_phi[img]) for img in tile]
        # group the 14 chambers by their midpoint corner: 7 groups of 2,
        # each group = one side carrying one map edge (the shared E)
        mids: List[Tuple[complex, List[Tuple[int, complex, complex, Tuple[int, int, int]]]]] = []
        for img, vv, mm, fl in chambers:
            hit = None
            for entry in mids:
                if abs(entry[0] - mm) < 1e-9:
                    hit = entry
                    break
            if hit is None:
                mids.append((mm, [(img, vv, mm, fl)]))
            else:
                hit[1].append((img, vv, mm, fl))
        if len(mids) != 7 or any(len(g) != 2 for _, g in mids):
            patch.errors.append("the tile midpoint grouping is not 7x2")
            return patch
        sides: List[Tuple[int, int, int, complex, complex]] = []
        for mm, group in mids:
            (i1, v1, _, f1), (i2, v2, _, f2) = group
            if f1[1] != f2[1]:
                patch.errors.append("a side's two chambers disagree on E")
                return patch
            sides.append((f1[1], v1, v2, mm, center))
        # walk the sides into a cycle by shared vertices (sides are
        # unordered vertex pairs; the walk tracks the current vertex)
        ordered: List[Tuple[int, int, int, complex, complex]] = []
        used = [False] * 7
        cur = sides[0]
        used[0] = True
        start_v = cur[1]
        end_v = cur[2]
        ordered.append(cur)
        ok_cycle = True
        for _ in range(6):
            nxt = None
            for j, s in enumerate(sides):
                if used[j]:
                    continue
                if abs(s[1] - end_v) < 1e-9:
                    nxt = (j, s, s[2])
                    break
                if abs(s[2] - end_v) < 1e-9:
                    nxt = (j, s, s[1])
                    break
            if nxt is None:
                ok_cycle = False
                break
            j, s, other = nxt
            used[j] = True
            ordered.append(s)
            end_v = other
        if not ok_cycle or abs(end_v - start_v) > 1e-9:
            patch.errors.append("the side cycle is broken or open")
            return patch
        # the CCW vertex cycle: one vertex per side (the side's entry
        # vertex along the walk)
        verts_c: List[complex] = []
        side_edges: List[int] = []
        cur_v = start_v
        for s in ordered:
            va, vb = s[1], s[2]
            start = va if abs(va - cur_v) < 1e-9 else vb
            verts_c.append(start)
            side_edges.append(s[0])
            cur_v = vb if abs(va - start) < 1e-9 else va
        # close the cycle: the last side's second vertex = the first vertex
        # (the polygon is complete; the vertex list has 7 entries)
        if len(verts_c) != 7:
            patch.errors.append("the vertex cycle is not 7")
            return patch
        # orient CCW around the center
        area2 = sum(
            (
                verts_c[k].real * verts_c[(k + 1) % 7].imag
                - verts_c[(k + 1) % 7].real * verts_c[k].imag
            )
            for k in range(7)
        )
        if area2 < 0:
            verts_c.reverse()
            side_edges.reverse()
            side_edges.insert(0, side_edges.pop())
        mids_aligned = [_disk_midpoint(verts_c[k], verts_c[(k + 1) % 7]) for k in range(7)]
        patch.heptagons.append(
            HeptagonCell(
                face_coset=face_coset,
                vertices=verts_c,
                midpoints=mids_aligned,
                center=center,
                psl_images=sorted(i for i in tile if pgl.is_psl[i]),
                side_edges=side_edges,
            )
        )
    patch.heptagons.sort(key=lambda h: h.face_coset)
    face_list = [h.face_coset for h in patch.heptagons]
    if sorted(face_list) != list(range(24)):
        patch.errors.append("the tiles do not cover the 24 faces")
        return patch

    # -- the side accounting: 168 sides -> 84 map edges, 2 sides each ----
    by_edge: Dict[int, List[Tuple[int, int]]] = {}
    for hi, hept in enumerate(patch.heptagons):
        for k in range(7):
            by_edge.setdefault(hept.side_edges[k], []).append((hi, k))
    if len(by_edge) != 84 or any(len(v) != 2 for v in by_edge.values()):
        patch.errors.append("the sides do not pair onto 84 map edges")
        return patch
    interior = 0
    boundary: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
    seg_of_side: Dict[Tuple[int, int], Tuple[Tuple[int, int], Tuple[int, int]]] = {}
    for hi, hept in enumerate(patch.heptagons):
        for k in range(7):
            a, b = hept.vertices[k], hept.vertices[(k + 1) % 7]
            seg_of_side[(hi, k)] = (min(_grid(a), _grid(b)), max(_grid(a), _grid(b)))
    for edge_id, owners in sorted(by_edge.items()):
        (h1, k1), (h2, k2) = owners
        if seg_of_side[(h1, k1)] == seg_of_side[(h2, k2)]:
            interior += 1
        else:
            boundary.append(((h1, k1), (h2, k2)))
    patch.interior_sides = interior
    patch.boundary_pairs = sorted(boundary)
    return patch


# ---------------------------------------------------------------------------
# The gravimetric assignment: 12 bodies <-> 12 antipodal face pairs
# ---------------------------------------------------------------------------


def assign_bodies(km: KleinMap) -> List[Dict[str, Any]]:
    """The deterministic body-to-pair assignment.

    The 12 bodies are ordered by descending GM (the Sun leads, ties by
    name); the 12 antipodal pairs are ordered canonically (by the
    smaller face index of the pair); body i receives pair i.
    """
    order = sorted(range(len(BODIES)), key=lambda i: (-BODIES[i].gm, BODIES[i].name))
    rows = []
    for slot, body_idx in enumerate(order):
        f1, f2 = km.antipodal_pairs[slot]
        rows.append(
            {
                "body": BODIES[body_idx].name,
                "kind": BODIES[body_idx].kind,
                "face_pair": (f1, f2),
            }
        )
    return rows


# ---------------------------------------------------------------------------
# The V2 stage: the closed gravifigure, certified
# ---------------------------------------------------------------------------


def _disk_witness_for(alpha: float) -> Dict[str, float]:
    """Solve the Poincare-disk heptagon with interior angle `alpha` by
    bisection over the vertex radius t; return the numeric circumradius,
    edge and angle — the independent witness of the closed forms."""
    from .hardcore import _disk_heptagon_angle

    lo, hi = 0.02, 0.98
    for _ in range(120):
        mid = 0.5 * (lo + hi)
        if _disk_heptagon_angle(mid) > alpha:
            lo = mid
        else:
            hi = mid
    t = 0.5 * (lo + hi)
    r_num = 2.0 * math.atanh(t)
    u = complex(t, 0.0)
    v = complex(t * math.cos(TWO_PI / 7.0), t * math.sin(TWO_PI / 7.0))
    diff2 = abs(u - v) ** 2
    cosh_l = 1.0 + 2.0 * diff2 / ((1.0 - abs(u) ** 2) * (1.0 - abs(v) ** 2))
    return {
        "t_vertex": t,
        "circumradius": r_num,
        "edge": math.acosh(cosh_l),
        "angle": _disk_heptagon_angle(t),
    }


def check_v2_klein_tiling(dps: int = 50, ceiling_margin: float = 0.05) -> Dict[str, Any]:
    """V2: the closed gravifigure — the full 24-heptagon Klein map as
    the coset geometry of the certified PSL(2,7), the PGL flag
    certificate, the chamber-grown disk patch (336 chambers, 24
    heptagons, 84 map edges), the antipodal pairing of the 24 faces
    into 12 body registers, the gravimetric angle register with its
    EXACT budget closure sum(alpha) = 8*pi, and the per-register
    closed forms with their disk witnesses."""
    tol = V2_TOLERANCES
    km = KleinMap.build()
    comb = km.register_summary()

    exact_geom = (
        comb["V"] == 56
        and comb["E"] == 84
        and comb["F"] == 24
        and comb["euler"] == -4
        and comb["vertex_degrees"] == [3]
        and comb["face_lengths"] == [7]
        and comb["edge_valences"] == [2]
        and comb["incidence_products"] == {"3V": 168, "2E": 168, "7F": 168}
        and comb["n_antipodal_pairs"] == 12
        and km.is_connected()
        and km.is_orientable()
    )

    algebra = register_algebra_float(ceiling_margin)
    exact = register_algebra_exact(dps, ceiling_margin)

    s_scale = sum(abs(r["s"]) for r in algebra["bodies"])
    float_ok = (
        algebra["alpha_sum_residual"] <= tol["float_budget"]
        and algebra["total_area_residual"] <= tol["float_budget"]
        and abs(algebra["s_sum"]) / max(s_scale, 1.0) <= tol["s_sum_rel"]
        and algebra["worst_pythagoras_residual"] <= tol["float_pythagoras"]
        and algebra["min_hyperbolicity_margin"] >= tol["hyperbolicity_margin"]
    )
    budget_ok = bool(
        exact["budget_ok"] and exact["area_ok"] and exact["pythagoras_ok"] and exact["s_sum_ok"]
    )

    rows = algebra["bodies"]
    witnesses: Dict[str, Any] = {}
    witness_ok = True
    for tag, row in (
        ("heaviest", max(rows, key=lambda r: r["s"])),
        ("lightest", min(rows, key=lambda r: r["s"])),
    ):
        wit = _disk_witness_for(row["alpha"])
        err_r = abs(wit["circumradius"] - row["circumradius"])
        err_e = abs(wit["edge"] - row["edge"])
        err_a = abs(wit["angle"] - row["alpha"])
        witnesses[tag] = {
            "body": row["body"],
            "alpha": row["alpha"],
            "circumradius_closed": row["circumradius"],
            "circumradius_witness": wit["circumradius"],
            "edge_closed": row["edge"],
            "edge_witness": wit["edge"],
            "error_circumradius": err_r,
            "error_edge": err_e,
            "error_angle": err_a,
        }
        witness_ok = (
            witness_ok
            and err_r <= tol["witness_abs"]
            and err_e <= tol["witness_abs"]
            and err_a <= tol["witness_angle_abs"]
        )

    patch = build_chamber_patch(km)
    psum = patch.summary()
    patch_ok = (
        not patch.errors
        and psum["chambers"] == 336
        and psum["n_heptagons"] == 24
        and psum["heptagon_sides"] == 168
        and psum["n_map_edges"] == 84
        and psum["flag_certificate"]
    )

    assignment = assign_bodies(km)

    passed = bool(exact_geom and float_ok and budget_ok and witness_ok and patch_ok)
    return {
        "check": (
            "V2 the closed gravifigure: the Klein map {7,3}_8 built as the coset "
            "geometry of the certified PSL(2,7) — V=56, E=84, F=24, Euler -4, "
            "3-regular, 7-gonal, connected, orientable; the PGL(2,7) flag "
            "certificate (the 336 flag wall-moves are the right "
            "multiplications by the (2,3,7) Coxeter involutions — the full "
            "flag action is simply transitive); the chamber patch grows in "
            "the Poincare disk to exactly 336 chambers = 24 heptagons with "
            "168 sides pairing onto 84 map edges; the witness involution "
            "pairs the 24 faces into 12 antipodal registers; the 12-body "
            "gravimetric angle register alpha_i = 2pi/3 - sigma*s_i with the "
            "geometric-mean normalization sum(s_i) = 0 closes the curvature "
            "budget EXACTLY: sum(alpha_i) = 8pi = 2pi(2g-2) — the Euler "
            "characteristic absorbs the mass ladder; the per-register closed "
            "forms hold with the Poincare-disk witnesses"
        ),
        "combinatorics": comb,
        "connected": km.is_connected(),
        "orientable": km.is_orientable(),
        "witness_triple": {
            "a_index": km.witness_a,
            "b_index": km.witness_b,
            "c_index": km.product_c,
        },
        "register_algebra": {
            "sigma": algebra["sigma"],
            "s_sum": algebra["s_sum"],
            "alpha_sum": algebra["alpha_sum"],
            "alpha_sum_residual": algebra["alpha_sum_residual"],
            "total_area": algebra["total_area"],
            "total_area_residual": algebra["total_area_residual"],
            "worst_pythagoras_residual": algebra["worst_pythagoras_residual"],
            "min_hyperbolicity_margin": algebra["min_hyperbolicity_margin"],
            "bodies": algebra["bodies"],
        },
        "exact_registers": exact,
        "disk_witnesses": witnesses,
        "chamber_patch": psum,
        "body_assignment": assignment,
        "params": {"dps": dps, "ceiling_margin": ceiling_margin, "tiling": "{7,3}_8"},
        "passed": passed,
    }


def run_v2(preset: str = "default") -> Dict[str, Any]:
    """The V2 stage entry point (preset dispatch, the house discipline)."""
    cfg = V2_PRESETS[preset]
    return check_v2_klein_tiling(cfg["dps"], cfg["ceiling_margin"])
