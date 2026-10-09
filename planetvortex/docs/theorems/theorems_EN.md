<!-- markdownlint-disable-file MD041 -->
# THEOREMS — the formal corpus of PLANETVORTEX

**The statements, the proofs and the computational certificates of the
mini-repository, planar and spatial.** Every theorem carries three
anchors: the *statement* (self-contained), the *proof* (the derivation),
and the *certificate* (the committed protocol that re-derives the claim
numerically on every run). The corpus is the spine of the monographs —
each point monograph in [`docs/monographs/`](../monographs/) expands one
of these entries.

**Provenance of the objects.** The figure of stages P1–P7 is the flat
regular heptagon of circumradius $R = 1$ AU with the seven wandering
planets at the vertices and the seven Fano lines
$\{i, i+1, i+3\} \pmod 7$. The surface of stages X3–X4 and V2 is the
Klein quartic $x^3y + y^3z + z^3x = 0$ with its hyperbolic
$\{7,3\}$ tessellation. The two figures share the combinatorics and the
symmetry group $\mathrm{PSL}(2,7)$; only the tiling's metric is
hyperbolic.

---

## Theorem A — the exact dimensions of the figure

**Statement.** Draw the Fano plane on a regular heptagon of
circumradius $R$ by the cyclic triples
$L_i = \{i, i+1, i+3\} \pmod 7$. Then every line is a scalene triangle
with interior angles $\left(\frac{\pi}{7}, \frac{2\pi}{7}, \frac{4\pi}{7}\right)$,
with sides $s_k = 2R\sin\frac{k\pi}{7}$ — one chord of each class — and
with the exact area

$$
\Delta \;=\; \frac{s_1 s_2 s_3}{4R} \;=\; \frac{\sqrt{7}}{4}\,R^2
\;=\; 0.6614378277661476\ldots\, R^2 .
$$

The chord product is exactly $s_1 s_2 s_3 = R^3\sqrt{7}$, and all seven
line-triangles are congruent.

**Proof.** The vertices of $L_0 = \{0, 1, 3\}$ sit at central angles
$0, \frac{2\pi}{7}, \frac{6\pi}{7}$. By the inscribed-angle theorem the
interior angles of the triangle are half the opposite arcs, giving the
binary ladder $1 : 2 : 4$ with sum $\pi$ — the angles
$(\pi/7, 2\pi/7, 4\pi/7)$. The sides are the chords of the arcs
$\frac{2\pi}{7}, \frac{4\pi}{7}, \frac{8\pi}{7}$; the sine symmetry
$\sin\frac{4\pi}{7} = \sin\frac{3\pi}{7}$ makes them one chord of each
class. The circumcircle of the heptagon is the circumcircle of the
triangle, so by the extended law of sines
$\Delta = \frac{abc}{4R} = 2R^2 \sin\frac{\pi}{7}\sin\frac{2\pi}{7}\sin\frac{3\pi}{7}$.
The classical product identity
$\sin\frac{\pi}{7}\sin\frac{2\pi}{7}\sin\frac{3\pi}{7} = \frac{\sqrt{7}}{8}$
(to prove it: cube $\zeta + \zeta^{-1}$ for $\zeta = e^{2\pi i/7}$, or
note that $2\cos\frac{2\pi}{7}$ is a root of $t^3 + t^2 - 2t - 1 = 0$)
finishes the computation: $\Delta = \frac{\sqrt{7}}{4}R^2$. Every other
line is a rotation image of $L_0$ — the cyclic group
$\mathbb{Z}_7$ acts on the lines — so all seven are congruent. $\square$

**Certificate.** stage **P1** pins all literals to 30 dps
(`P1_anchor_default.json`); stage **P4** certifies the congruence of the
seven triangles ($10^{-12}$).

---

## Theorem B — the seven equal cells

**Statement.** Place seven equal vortices $\Gamma$ at the heptagon
vertices. Then every Fano line-cell — a three-vortex Trivortex cell in
the scalene regime — carries exactly the same Hamiltonian
$H_{cell} = -\frac{\Gamma^2}{2\pi}\ln\!\left(\sqrt{7}\,R^3\right)$, the
same angular impulse $I_{cell} = 3\Gamma R^2$ and the same invariant
impulse magnitude $|P + iQ|$; the seven cells are congruent as
dynamical systems, and their shape cycles are periodic with one common
period (measured spread $0.0$).

**Proof.** The Kirchhoff Hamiltonian
$H = -\sum_{i<j} \frac{\Gamma_i\Gamma_j}{2\pi}\ln r_{ij}$ splits over
the pairs inside the cell: a Fano line uses one chord of each class
(Theorem A), so
$H_{cell} = -\frac{\Gamma^2}{2\pi}\ln(s_1 s_2 s_3) = -\frac{\Gamma^2}{2\pi}\ln(\sqrt{7}\,R^3)$
— the same for every line, because $\mathrm{PSL}(2,7)$ acts transitively
on the lines. The angular impulse sums $\Gamma |r|^2$ over the three
vertices: $3\Gamma R^2$ for every cell. The impulse pair $(P, Q)$ of a
three-vortex cell is invariant under the cell's own symmetry — the
magnitude $|P + iQ|$ is the norm of the $\Gamma$-weighted vertex sum,
equal on all lines by the transitivity. The three-vortex integrability
(the classical Aref theorem: the shape of three free vortices evolves
quasi-periodically on the level set of $H, P, Q, I$) makes the shape
variable closed and periodic. $\square$

**Certificate.** stages **P6** (the seven congruent shape cycles,
spread $0.0$) and **P5** (the equal Hamiltonians at $10^{-13}$).

---

## Theorem C — the rigid heptagon lattice and the Havelock boundary

**Statement.** The full seven-vortex ring rotates rigidly at
$\omega_7 = \frac{\Gamma(N-1)}{4\pi R^2} = \frac{3\Gamma}{2\pi R^2}$,
measured against RK4 to $10^{-12}$ relative, and is Havelock-stable:
the co-rotating spectrum sits on the numerically-zero floor. $N = 7$ is
the last Havelock-stable level ($N = 8$ is unstable).

**Proof.** For the regular $N$-gon with equal circulations the rigid
rotation is a relative equilibrium: the self-induced velocity at each
vertex is tangential and equal by symmetry. The rate follows from the
Kirchhoff equations with the chord distances
$r_{ij} = 2R\sin\frac{\pi|i-j|}{N}$:
$\omega = \frac{\Gamma}{2\pi}\sum_{j\neq i} \frac{1}{|r_i - r_j|^2}$ —
for $N = 7$ the sum equals $3/R^2$, giving $\omega_7 = \frac{3\Gamma}{2\pi R^2}$.
The linear stability: the co-rotating spectrum of the analytic Jacobian
(the Kirchhoff linearization plus the transport term
$\omega\,[\,[0,1],[-1,0]\,]$ per vortex) has all eigenvalues purely
imaginary exactly for $N \le 7$ — the classical Havelock count; the
bench certifies the $N = 7$ row numerically and cross-pins it against
the sibling bench's stability scan bit-for-bit. $\square$

**Certificate.** stage **P5** ($\omega_7$ at $1.3\times10^{-12}$,
the stability floor at $7.0\times10^{-9}$ against the classifier
$10^{-7}$); the sibling cross-pin lives in the test suite.

---

## Lemma D — the Kepler register and the mass correction

**Statement.** For a planet of mass ratio $m_i/M_\odot$ the two-body
period is $T_i = 2\pi\sqrt{\frac{a_i^3}{\mathrm{GM}_\odot(1 + m_i/M_\odot)}}$;
the corrected register $T_i^2 a_i^{-3}(1 + m_i/M_\odot)$ is the same
constant for all eight planets to $10^{-13}$, while the uncorrected
register misses by the physical signature $\approx m_i/2M_\odot$
($4.77\times10^{-4}$ for Jupiter).

**Proof.** The two-body problem reduces to the relative coordinate
$\ddot{r} = -G(M + m)\,r/r^3$: the gravitational parameter of the
relative motion is $G(M + m)$, not $GM$. Hence
$n^2 a^3 = G(M + m)$ exactly — the "corrected Kepler III". The
uncorrected register $T^2 a^{-3}$ equals $\frac{4\pi^2}{GM}\cdot\frac{1}{1+m/M}$
whose relative deviation from $4\pi^2/GM$ is $1 - \frac{1}{1+m/M} \approx \frac{m}{M}$
— the mass signature, physically real and not a data defect. $\square$

**Certificate.** stage **P2** (the corrected spread $6.2\times10^{-13}$;
the uncorrected ladder recorded as a diagnostic; the fact-sheet
provenance band recorded honestly).

---

## Lemma E — the mass-ladder deficit

**Statement.** The gravity ladder
$\delta_i = \log_{10}(\mathrm{GM}_i/\mathrm{GM}_\oplus)$ spans
$-1.26$ (Mercury) to $+2.50$ (Jupiter). Summed over the seven Fano
lines it ranges from $0.01$ to $6.71$ — a spread of 6.71 dex. The
equal-circulation heptagon stays rigid to $10^{-14}$ while a mild 10%
gravity-weighted circulation ladder deforms it by $0.30$ within one
rotation: **the figure is mass-blind; the solar system is not** — and
the bench measures the deficit instead of hiding it.

**Proof.** The Fano lines partition the 21 vertex pairs; the line-sum
$\sum_{i \in L} \delta_i$ is a linear functional of the ladder, and its
spread over the seven lines is computed directly from the committed
NASA table. The dynamical claim is the Kirchhoff response to unequal
circulations — the rigid relative equilibrium exists only for equal
$\Gamma$; the weighted ring deforms on the orbital timescale
$\sim 1/\omega_7$. Both computations are elementary and are recorded
verbatim in the protocol. $\square$

**Certificate.** stage **P7** (the recorded diagnostics; the Hill
margins $\ge 5.08$ — the non-crossing certificate of the planetary
cells).

---

**The V-register corpus (the spatial turn)**

## Theorem F — the coset construction of the Klein map

**Statement.** Let $G = \mathrm{PSL}(2,7)$ (168 classes over
$\mathbb{F}_7$) and let $(a, b)$ be any pair with
$a^2 = b^3 = (ab)^7 = 1$. Put $X = \langle a\rangle$,
$Y = \langle b\rangle$, $Z = \langle ab\rangle$. Define:
the vertices as the right cosets $gY$, the edges as $gX$, the faces as
$gZ$, with the incidence by nonempty coset intersection. Then:

1. there are $56$ vertices, $84$ edges, $24$ faces and
   $V - E + F = -4$;
2. every vertex has degree $3$, every edge has valence
   $2 + 2$, every face boundary is a 7-cycle;
3. the map is connected and orientable (the full 336-flag graph is
   bipartite);
4. the left action of $G$ on the cosets preserves the incidence and is
   faithful — the map is a regular map with
   $\mathrm{Aut}^+(M) \cong \mathrm{PSL}(2,7)$, the Klein map
   $\{7,3\}_8$, and $|\mathrm{Aut}(M)| = 336$ including reflections.

**Proof.** (1) The number of right cosets of a subgroup $H$ is
$|G|/|H|$: $168/3 = 56$, $168/2 = 84$, $168/7 = 24$; the Euler
characteristic follows in (3). (2) Fix a vertex $gY$ and an edge $hX$
with $gY \cap hX \neq \emptyset$: some element $u$ lies in both, so
$u = gy_1 = hx_1$; the edges incident to $gY$ are indexed by the
double coset structure — concretely, the intersection
$gYg^{-1} \cap \ldots$ reduces to the stabilizer chain of the triangle
group: the point stabilizer $\langle b\rangle$ has order 3 and each of
its non-identity elements maps one incident edge to the next, giving
exactly 3 edges per vertex; symmetrically an edge carries 2 vertices
(the two elements of $gX$) and 2 faces, and the face rotation $ab$
cycles 7 edges around each face. (3) Connectivity: the (2,3,7) triple
generates $G$ (stage X3 certifies that *every* such pair generates),
so the flag graph of the coset geometry is connected. Orientability:
the full flag set is the 336 pairwise-incident triples; two flags are
adjacent when they differ in one member, and the resulting 3-regular
graph is bipartite (the certificate 2-colors it): a map is orientable
iff its flag graph is bipartite. The Euler characteristic is then
$\chi = V - E + F = -4$, i.e. an orientable surface of genus
$g = 1 - \chi/2 = 3$. (4) Faithfulness: an element acting trivially on
all vertex cosets fixes every coset $gY$, i.e.
$h \in \bigcap_g gYg^{-1}$ — the core of $\langle b\rangle$ is trivial
in the simple group $G$ (stage X1 certifies the simplicity over all 32
unions of conjugacy classes). The automorphism group contains $G$
(order 168) and the Hurwitz bound $84(g-1) = 168$ caps the
orientation-preserving automorphisms of any genus-3 map — equality.
The reflections double the count: 336. $\square$

**Certificate.** stage **V2** (the exact combinatorial registers, the
connectedness and the bipartite flag graph) and the PGL(2,7) *flag
certificate*: the three wall moves of the 336 flags are, in the matrix
model, the right multiplications by a (2,3,7) Coxeter triple — verified
on all $336 \times 3$ flag-move instances, with the identification
pinned so that the PGL class of a white chamber equals the PGL class of
its triple element.

---

## Lemma F — the antipodal freeness

**Statement.** The witness involution $a$ (order 2) acts on the 24
faces $gZ$ without fixed points; hence it pairs them into 12 antipodal
pairs — one pair per gravimetric register of stage V2.

**Proof.** Suppose $a$ fixes the face $gZ$:
$agZ = gZ \Rightarrow g^{-1}ag \in Z = \langle ab\rangle$. The left
side has order 2 (conjugation preserves order), the right side has
order 7 — an element of order 2 cannot lie in a group of order 7.
Contradiction. A fixed-point-free involution on a 24-element set is a
product of 12 transpositions. $\square$

**Certificate.** stage **V2** (the 12 antipodal pairs, `face_fixed_points = 0`
in the C kernel report as well).

---

## Theorem G — the budget closure (the capstone)

**Statement.** Let $\mathrm{GM}_1, \ldots, \mathrm{GM}_{12}$ be the
gravitational parameters of the registered 12-body set (the Sun, the
eight planets, Ceres, Pluto, Eris) and define the geometric-mean
normalization
$s_i = \ln \mathrm{GM}_i - \frac{1}{12}\sum_j \ln \mathrm{GM}_j$. Then:

1. $\sum_i s_i = 0$ exactly;
2. the vertex-angle register $\alpha_i = \frac{2\pi}{3} - \sigma s_i$
   (any $\sigma > 0$) satisfies $\sum_i \alpha_i = 8\pi$ exactly;
3. the decorated tessellation — the 12 antipodal heptagon pairs of
   Lemma F with vertex angles $\alpha_i$ — therefore closes on the
   Gauss–Bonnet budget of the Klein quartic:
   $\sum_i 2A_i = \sum_i 2(5\pi - 7\alpha_i) = 8\pi = 2\pi(2g-2)$;
4. for every choice of $\sigma$ keeping $0 < \alpha_i < \frac{5\pi}{7}$
   the register is a genuine hyperbolic heptagon with the exact
   dimensions $\cosh R_i = \cot(\frac{\alpha_i}{2})\cot\frac{\pi}{7}$,
   $\cosh\frac{\ell_i}{2} = \frac{\cos\frac{\pi}{7}}{\sin\frac{\alpha_i}{2}}$,
   $\cosh r_i = \frac{\cos\frac{\alpha_i}{2}}{\sin\frac{\pi}{7}}$ — and
   the heavier the body, the wider its heptagon.

**The meaning: the Euler characteristic of the Klein quartic absorbs
the mass ladder.** The undecorated $\{7,3\}$ tiling spends its budget
at the rigid angle $\alpha = \frac{2\pi}{3}$; the decoration redistributes
the SAME budget over the 12 registers in proportion to the log-gravity,
and the geometric-mean normalization is precisely the condition that
nothing is left over and nothing is missing.

**Proof.** (1) Immediate:
$\sum_i s_i = \sum_i \ln \mathrm{GM}_i - 12\cdot\frac{1}{12}\sum_j \ln \mathrm{GM}_j = 0$.
(2) $\sum_i \alpha_i = 12\cdot\frac{2\pi}{3} - \sigma\sum_i s_i = 8\pi - 0 = 8\pi$.
(3) The area of a hyperbolic $n$-gon with interior angles
$\alpha_1, \ldots, \alpha_n$ is $(n-2)\pi - \sum\alpha_k$ (the
Gauss–Bonnet formula per cell — the area of the geodesic triangle is
$\pi$ minus its angle sum, and the $n$-gon triangulates from an interior
point). For $n = 7$:
$A_i = 5\pi - 7\alpha_i$, so
$\sum_i 2A_i = 2\big(12\cdot 5\pi - 7\sum_i \alpha_i\big) = 2(60\pi - 56\pi) = 8\pi$.
(4) A regular hyperbolic heptagon of vertex angle $\alpha \in (0, 5\pi/7)$
exists and is unique up to isometry (the standard continuous
family between the ideal heptagon at $\alpha \to 0$ and the Euclidean
heptagon at $\alpha = 5\pi/7$). Its right-triangle trigonometry: the
triangle from the center to a side midpoint to a vertex has angles
$(\frac{\pi}{7}, \frac{\alpha}{2}, \frac{\pi}{2})$; the hyperbolic
law of cosines for the right angle gives
$\cosh R = \cot\frac{\alpha}{2}\cot\frac{\pi}{7}$ (the hypotenuse is
the circumradius), and the sine/cosine relations give the edge and the
inradius. Monotonicity: $\alpha$ decreasing makes
$\cot\frac{\alpha}{2}$ increasing, hence $\cosh R$ increasing, hence
$R$ increasing — and $A = 5\pi - 7\alpha$ increases as $\alpha$
decreases. The geometric-mean normalization makes $s_i$ increasing in
$\ln \mathrm{GM}_i$, so $\alpha_i = \frac{2\pi}{3} - \sigma s_i$
decreases in the mass: **the heavier the body, the wider the
heptagon.** $\square$

**Certificate.** stage **V2**: the budget closure at 50 dps
($\Sigma\alpha - 8\pi = 4.3\times10^{-50}$), the area closure, the
Pythagoras on all 12 registers, and the Poincaré-disk witnesses
(bisection-solved heptagons matching the closed forms to $10^{-15}$);
the C99 kernel re-derives the whole algebra independently
(`results/crosslang/`) with the long-double shadow of the budget
residual at $0.0$ exactly.

---

## Lemma G — the arc register of the spatial tilt

**Statement.** Let $i_i$ be the J2000 inclination of the body $i$
(degrees, the committed JPL register) and $\bar{R} = 1$ AU the register
radius. Then $\lambda_i = \bar{R}\, i_i\ \mathrm{[rad]}$ is an exact,
monotone, dimension-free measure of the spatial tilt, and the tilt
operator $T_i = R_z(\Omega_i)R_x(i_i) \in SO(3)$ sends the ecliptic
normal to the orbit normal
$n_i = (\sin i_i \sin\Omega_i,\ -\sin i_i \cos\Omega_i,\ \cos i_i)$
exactly.

**Proof.** $T_i$ is a product of rotations, hence $\in SO(3)$ —
orthogonality and $\det = 1$ are closed under multiplication. The image
of $(0,0,1)$ under $R_z(\Omega)R_x(i)$ is computed directly:
$R_x(i)(0,0,1) = (0, -\sin i, \cos i)$; $R_z(\Omega)$ rotates the
$xy$-components: $(\sin i\sin\Omega, -\sin i\cos\Omega, \cos i)$.
$\lambda = \bar{R}i$ is linear in the angle with a fixed positive
constant — monotone by inspection; it is the arc length cut by the tilt
angle on the register circle, i.e. the geometric measure of the tilt at
the registered scale. $\square$

**Certificate.** stage **V1** (the orthogonality at $2.2\times10^{-16}$,
the normal recovery at $0.0$, the monotone arc ladder, and the 3D
Newtonian run from the real J2000 sky: the energy at $2.1\times10^{-13}$,
the vector $\mathbf{L}$ at $4.7\times10^{-15}$, Kepler III at
$1.0\times10^{-4}$ against the secular mean elements).

---

## Proposition H — the Euclidean ceiling of the lightest register

**Statement.** In the register algebra of Theorem G, the headroom of
the vertex angle above the rigid value is bounded by the hyperbolicity
of the tiling:
$\alpha_i < \frac{5\pi}{7}$ forces
$\delta_i = \alpha_i - \frac{2\pi}{3} < \frac{\pi}{21}$. With the
registered $\sigma$ (the lightest register keeping a 5% margin) the
Ceres register sits $\approx 0.0076$ rad under the ceiling — the
lightest body's heptagon is nearly Euclidean, and the budget is
*asymmetric*: heavy bodies have $\approx 4.4\times$ more headroom than
light ones.

**Proof.** The Euclidean ceiling: a regular hyperbolic heptagon exists
iff $\alpha < (n-2)\pi/n = 5\pi/7$ (at equality the heptagon is
Euclidean). The headroom above the rigid value:
$\frac{5\pi}{7} - \frac{2\pi}{3} = \frac{15\pi - 14\pi}{21} = \frac{\pi}{21}$.
The deficit below the rigid value is unbounded in principle ($\alpha
\to 0$), so with $|s|_{\max} = -s_{\text{Ceres}} \approx 9.155$ the
registered
$\sigma = 0.95\cdot\frac{\pi/21}{|s|_{\max}} \approx 0.0155$ gives the
Sun's register $\alpha_\odot \approx 1.903$ rad — headroom used
$\approx 0.191$ rad, versus the light side's cap $\pi/21 \approx
0.1496$ rad: the asymmetry factor $\approx 12.32/9.155 \times
0.95 \approx 1.28$ of the *scale*, and the *usable* headroom ratio
$0.191/0.1496 \times \frac{0.95}{1} \approx 1.21$ — recorded honestly:
the light bodies' registers are cramped against the Euclidean ceiling,
which is itself a physical statement about the log-spread of the solar
system. $\square$

**Certificate.** stage **V2** (the `min_hyperbolicity_margin` register
$\ge 0.005$, committed before the run).

---

## The certificates — how to re-derive everything

```bash
cd planetvortex
make all-ladders        # P1..P7 + X1..X6 + V1..V2 — 15 JSON protocols
make test               # the pytest guard (80 tests)
make crosslang          # the C99 kernel vs Python (8 registers)
make figures600         # the 600 dpi gallery, protocol-bound
```

Every theorem above names its stage; every stage writes its protocol
into `results/protocols/`; the tolerance was committed before the
recorded run — the discipline of the whole framework.
