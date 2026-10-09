# PLANETVORTEX — A Research Monograph

## The Solar System as a PSL(2,7) Figure: Exact Heptagonal Geometry, the Vortex Lattice and the Newtonian Planetary Registers

*Mini-repository `planetvortex/` of the TRIVORTEX framework — version
1.0.0. Every number quoted below is bound to a committed run protocol
in `results/protocols/`; the tables quote recorded values, the proofs
reference registered tolerances, and the figures are the output of the
protocol-bound factory.*

---

## Abstract

This monograph develops the planetary gravity–geometry bench: the
construction of a geometric figure — a regular heptagon with the Sun
at the centre and the seven wandering planets at its vertices, with
the seven Fano lines $\{i, i+1, i+3\} \pmod 7$ drawn on it — whose
symmetry group is $\mathrm{PSL}(2,7)$, the smallest non-abelian simple
group, and whose exact dimensions are computed in closed form and
bound to the gravitational registers of the solar system. Three
theorems and two lemmas organize the payload. Theorem A computes the
exact dimensions of the figure: every Fano line is the congruent
triangle with angles $(\pi/7, 2\pi/7, 4\pi/7)$ and area
$\sqrt{7}/4\,R^2$, by the classical product identity
$\sin(\pi/7)\sin(2\pi/7)\sin(3\pi/7) = \sqrt{7}/8$. Theorem B shows
that the seven three-vortex Trivortex cells hosted by the lines carry
exactly equal Hamiltonians $-(\Gamma^2/2\pi)\ln(\sqrt{7}R^3)$ and
congruent shape cycles — the dynamical shadow of $\mathrm{PSL}(2,7)$,
measured with spread 0.0. Theorem C certifies the heptagon lattice as
a Havelock-stable relative equilibrium at
$\omega_7 = 3\Gamma/2\pi R^2$ — the $N = 7$ row of the sibling
bench's scan, cross-pinned bit-for-bit. Lemma D certifies Kepler's
third law dynamically across the eight planets — the mass-corrected
periods match to $6.2\times10^{-13}$ while the uncorrected formula
misses by the physical signature $m_i/2M_\odot$ up to
$4.77\times10^{-4}$ (Jupiter). Lemma E measures the honest distance
between the figure and the sky: the gravity ladder
$\log_{10}(\mathrm{GM}_i/\mathrm{GM}_\oplus)$ summed over the seven
lines spans $6.71$ dex, and a mild gravity-weighted circulation
ladder deforms the vortex figure by $0.30$ within one rotation while
the equal-circulation ring stays rigid to $9.8\times10^{-15}$. The
bench runs the full Newtonian Sun + 8-planets simulation (energy drift
$2.1\times10^{-13}$ over 12 years) and registers everything in a
seven-stage P-ladder of committed JSON protocols.

---

## 1. Scope and provenance

The parent framework anchors on Theorem 3.1 — the closed-form
choreography of three point vortices with the Chaplygin topological
integral — and verifies the classical layer of its model with the
V1–V4 ladder. The sibling bench `polyvortex` lifted the picture to
$N$ equal vortices and located the Havelock stability boundary exactly
between $N = 7$ and $N = 8$. This mini-repository takes the $N = 7$
object — the heptagon, the last stable ring — and asks what it becomes
when its vertices are labeled by the seven wandering planets of the
solar system and its centre by the Sun.

The provenance discipline is the framework's own: a committed data
table (the NASA register of Section 4), a committed structure (the
Fano plane of Section 3), tolerances registered before the recorded
runs, deterministic integration, and one JSON protocol per stage —
seven stages, P1 through P7. Nothing in this volume quotes a number
that no protocol carries. The mini-repository never imports the parent
framework or the sibling bench at runtime; the sibling ladder appears
only in the test suite as the reference oracle.

The units are astronomical: length in AU (exactly
$149\,597\,870\,700$ m), time in Julian years, mass in solar masses;
$\mathrm{GM}_\odot = 4\pi^2$ in these units by construction, and the
planetary masses come from the committed GM register as
$m_i = \mathrm{GM}_i/\mathrm{GM}_\odot$.

---

## 2. The two layers

The bench keeps two layers of the model honestly separated, exactly as
the parent and the sibling do.

**Layer N + P — the Newtonian planetary dynamics (numeric).** The
planets are point masses in the planar heliocentric idealization; the
equations are the full pairwise Newtonian system

$$\ddot{\mathbf{r}}_i = \sum_{j \ne i} 4\pi^2\, m_j\,
\frac{\mathbf{r}_j - \mathbf{r}_i}{|\mathbf{r}_j - \mathbf{r}_i|^3},
\qquad i = 0, \ldots, 8,$$

integrated by classical RK4. The registers are the conservation of
energy and angular momentum, the osculating elements $(a, e)$ against
the committed table, Kepler's third law measured from the integrated
motion, and the classical perturbation hierarchy.

**Layer F + V — the exact figure and its vortices (analytic +
numeric).** The figure is the regular heptagon of circumradius $R$
with the Fano plane on it; its dimensions are closed forms (Theorem
A). The vortices are the Kirchhoff point-vortex flow

$$\dot{x}_i = -\frac{1}{2\pi}\sum_{j \ne i} \Gamma_j
\frac{y_i - y_j}{r_{ij}^2}, \qquad
\dot{y}_i = +\frac{1}{2\pi}\sum_{j \ne i} \Gamma_j
\frac{x_i - x_j}{r_{ij}^2},$$

with the invariants $H = -\sum_{i<j} \Gamma_i\Gamma_j \ln r_{ij}/2\pi$,
$P = \sum \Gamma_i x_i$, $Q = \sum \Gamma_i y_i$,
$I = \sum \Gamma_i |\mathbf{r}_i|^2$. The connection between the layers
is the gravity ladder
$\delta_i = \log_{10}(\mathrm{GM}_i/\mathrm{GM}_\oplus)$ carried by the
vertices — and, honestly, the deficit of that connection (Lemma E).

---

## 3. The structure and the exact figure (Theorem A)

### 3.1 The Fano plane in two models

The Fano plane $\mathrm{PG}(2,2)$ is the unique projective plane on
seven points: seven lines, three points per line, every pair of points
on exactly one line. The bench builds it twice.

**Model Z (cyclic).** The points are the residues
$\mathbb{Z}_7 = \{0, \ldots, 6\}$ — the heptagon vertices in orbital
order. The lines are the seven triples

$$L_i = \{i,\ i+1,\ i+3\} \pmod 7, \qquad i = 0, \ldots, 6.$$

**Model B (binary).** The points are the seven nonzero vectors of
$\mathbb{F}_2^3$; the lines are the triples $\{u, v, u+v\}$; the
automorphism group is $\mathrm{GL}(3,2)$.

The automorphism group of either model has order 168 and is isomorphic
to $\mathrm{PSL}(2,7)$ — the smallest non-abelian simple group, the
group of orientation-preserving automorphisms of the Klein quartic.
Stage P4 certifies, exhaustively: 168 line-preserving permutations of
$\mathbb{Z}_7$ (closed, all inverses present, transitive on points,
stabilizers of orders $168/7 = 24$ both on points and on lines, the
pair axiom on all 21 pairs); 168 invertible $3\times3$ matrices over
$\mathbb{F}_2$; and an explicit line-preserving bijection
$\varphi: \mathbb{Z}_7 \to \mathbb{F}_2^3$ whose conjugation
$\varphi\sigma\varphi^{-1}$ maps the cyclic group copy onto the
$\mathrm{GL}(3,2)$ copy inside $S_7$ — the two models are one
structure, and the certificate is constructive, not existential.

### 3.2 The exact dimensions

**Theorem A.** *Draw the Fano plane on a regular heptagon of
circumradius $R$ by the triples $\{i, i+1, i+3\}$. Then every line is
a scalene triangle with interior angles $(\pi/7, 2\pi/7, 4\pi/7)$,
with sides $s_1 = 2R\sin(\pi/7)$, $s_2 = 2R\sin(2\pi/7)$,
$s_3 = 2R\sin(3\pi/7)$ — one chord of each class — and with area*

$$\Delta = \frac{s_1 s_2 s_3}{4R} = \frac{\sqrt{7}}{4} R^2 = 0.6614378277661476\ldots\, R^2.$$

*Proof sketch.* The vertices of the line $L_0 = \{0, 1, 3\}$ sit at
central angles $0$, $2\pi/7$, $6\pi/7$. The inscribed-angle theorem
gives the interior angles as half the opposite arcs:
$\pi/7$ at the vertex $\{3\}$-side, $2\pi/7$ and $4\pi/7$ — the binary
ladder $1:2:4$, summing to $\pi$. The sides are the chords of arcs
$2\pi/7$, $4\pi/7$, $8\pi/7$, i.e. $2R\sin(\pi/7)$,
$2R\sin(2\pi/7)$, $2R\sin(4\pi/7) = 2R\sin(3\pi/7)$ — one chord of
each class, by the sine symmetry $\sin(4\pi/7) = \sin(3\pi/7)$. The
three vertices lie on the circumcircle of radius $R$, which is
therefore the triangle's circumcircle, and the area of any triangle is
$abc/4R_{circum}$:

$$\Delta = \frac{2R\sin\frac{\pi}{7}\cdot 2R\sin\frac{2\pi}{7}\cdot 2R\sin\frac{3\pi}{7}}{4R}
= 2R^2 \sin\frac{\pi}{7}\sin\frac{2\pi}{7}\sin\frac{3\pi}{7}
= 2R^2 \cdot \frac{\sqrt{7}}{8} = \frac{\sqrt{7}}{4}R^2,$$

by the classical identity $\sin(\pi/7)\sin(2\pi/7)\sin(3\pi/7) =
\sqrt{7}/8$. Every line is a rotation image of $L_0$, so the seven
triangles are congruent. $\square$

The chord product carries the same cubic field:
$s_1 s_2 s_3 = 8R^3 \cdot \sqrt{7}/8 = R^3\sqrt{7}$. At the registered
scale $R = 1$ AU the figure's dimensions in the sky are:

| quantity | closed form | value (30 digits) |
|----------|-------------|-------------------|
| side $s_1$ | $2\sin(\pi/7)$ | $0.867767478235116240951536743604$ |
| short diagonal $s_2$ | $2\sin(2\pi/7)$ | $1.56366296493605961741688916157$ |
| long diagonal $s_3$ | $2\sin(3\pi/7)$ | $1.94985582436364721403626316285$ |
| product $s_1 s_2 s_3$ | $\sqrt{7}$ | $2.64575131106459059050161575194$ |
| cell area $\Delta$ | $\sqrt{7}/4$ | $0.661437827766147647625403937985$ |
| lattice rate $\omega_7$ | $3/2\pi$ | $0.477464829275686007306651290118$ |
| angle ladder | $\pi/7 : 2\pi/7 : 4\pi/7$ | $1 : 2 : 4$ |

Stage P1 pins these literals at `mp.dps = 30` and certifies the
float64 layer against them to $4.9\times10^{-16}$; stage P4 re-derives
the congruence of all seven line-triangles to $6.7\times10^{-16}$
absolute.

---

## 4. The Kepler register and the mass correction (Lemma D)

### 4.1 The committed register

The data layer commits the NASA register verbatim: the GM of the Sun
($1.32712440018 \times 10^{20}$ m³ s⁻²) and of the eight planets, the
equatorial radii, the semi-major axes and eccentricities (JPL J2000
mean elements), the sidereal periods and the surface gravities. The
two-body constant of planet $i$ is
$\mu_i = 4\pi^2 (1 + m_i/M_\odot)$.

### 4.2 The dynamic certification

**Lemma D.** *The two-body period of every planet, measured from
interpolated perihelion passages of the RK4 flow, matches
$T_i = 2\pi\sqrt{a_i^3/\mu_i}$ to $6.2\times10^{-13}$ relative; the
uncorrected formula $2\pi\sqrt{a_i^3/4\pi^2}$ misses by the exact
signature $\sqrt{1 + m_i/M_\odot} - 1 = m_i/2M_\odot + O(m_i^2)$, up to
$4.77\times10^{-4}$ for Jupiter.*

*Proof sketch.* The two-body relative flow is exactly Keplerian, so
the measured period converges to $T_i$ at the integrator's phase
accuracy — the parabolic interpolation of the perihelion minima cancels
its bias between successive minima to $(n\,\mathrm{dt})^4$. The
uncorrected ratio is
$T_{uncorr}/T_i = \sqrt{\mu_i/4\pi^2} = \sqrt{1 + m_i/M_\odot}$
exactly, whence the signature. $\square$

The recorded separation between the corrected and uncorrected
registers is a factor $7.7\times10^{8}$ — the mass correction is not a
refinement but the difference between physics and its spherical-cow
approximation. The committed fact-sheet periods are recorded as a
provenance diagnostic: they disagree with the Kepler-implied periods
at up to $4.8\times10^{-4}$ (Neptune worst) because they are rounded
and epoch-mixed; the bench measures Kepler III in the dynamics instead
of quoting the tables, and records the table inconsistency honestly.

---

## 5. The planetary simulation (stage P3)

The full system — the Sun and the eight planets, all pairwise Newtonian
terms, barycentric momentum nulled exactly — is integrated for 12 years
at $\mathrm{dt} = 2\times10^{-4}$ yr (the quick preset: 4 years at
$10^{-3}$; the full preset: 40 years at $10^{-4}$). The committed
initial condition places every planet at perihelion of its committed
$(a, e)$ orbit, all perihelia aligned, with the barycentric frame
shift applied along the motion axis so that the heliocentric relative
states are exact and the total momentum is machine-zero.

The recorded registers of the default run:

| register | recorded value | registered band |
|----------|----------------|-----------------|
| energy drift (12 yr) | $2.07\times10^{-13}$ | $\le 10^{-9}$ |
| angular-momentum drift | $0.0$ (bit-identical) | $\le 10^{-10}$ |
| worst osculating $\Delta a/a$ | $4.9\times10^{-3}$ | $\le 10^{-2}$ |
| worst osculating $\Delta e$ | $4.8\times10^{-3}$ | $\le 10^{-2}$ |
| Kepler III of the integrated motion | $2.5\times10^{-5}$ | $\le 10^{-4}$ |
| perturbation hierarchy | $2.2\times10^{-3}$ | recorded |

The measured periods over integer revolutions — Mercury 87.968 d,
Venus 224.689 d, Earth 365.243 d, Mars 686.917 d — differ from the
committed table by $10^{-5}$–$10^{-4}$: the mutual perturbations plus
the table's epoch mixing, both honest physics-and-provenance effects.
The perturbation hierarchy record of $2.2\times10^{-3}$ quantifies the
classical smallness of the planetary problem: even the most perturbed
body feels the rest of the system at two parts in a thousand of the
solar pull.

---

## 6. The heptagon lattice (Theorem C)

**Theorem C.** *The seven-vortex regular heptagon ($\Gamma_i = \Gamma$,
$R$) is a relative equilibrium rotating rigidly at*

$$\omega_7 = \frac{\Gamma (N-1)}{4\pi R^2} = \frac{3\Gamma}{2\pi R^2}
= 0.4774648292756860\ldots$$

*at $N = 7$; its co-rotating spectrum is Havelock-stable with
$\max \mathrm{Re}\,\lambda$ on the numerically-zero floor
($7.0\times10^{-9}$, classifier $10^{-7}$); and its Hamiltonian is
exactly $H_{ring} = -\frac{7\Gamma^2}{2\pi}\ln(\sqrt{7}\,R^3)$.*

*Proof sketch.* The rotation formula is the roots-of-unity register of
the sibling bench at $N = 7$; the stability classification is the
Havelock register — $N = 7$ is the last stable level, $N = 8$ the
first unstable one. The Hamiltonian: the 21 pairwise distances of the
ring are seven of each chord class, so
$\sum_{i<j} \ln d_{ij} = 7\ln s_1 + 7\ln s_2 + 7\ln s_3 =
7\ln(R^3\sqrt{7})$ by Theorem A's product identity, giving
$H_{ring} = -\frac{7\Gamma^2}{2\pi}\ln(\sqrt{7}\,R^3) = 7\,H_{cell}$.
$\square$

Stage P5 measures the rotation to $1.35\times10^{-12}$ relative over
two revolutions, holds the invariants to $1.25\times10^{-14}$, and
records the exact-Hamiltonian identity at error $0.0$ — the closed
form $-1.08395426662194$ at $\Gamma = R = 1$ equals the numeric
Kirchhoff register bit-for-bit in float64.

---

## 7. The seven cells (Theorem B)

### 7.1 The exact cell registers

**Theorem B.** *Place seven equal vortices at the heptagon vertices.
Then every Fano line-cell carries the same Hamiltonian, angular
impulse and moment of inertia,* $H_{cell} =
-\frac{\Gamma^2}{2\pi}\ln(\sqrt{7}R^3)$, $I_{cell} = 3\Gamma R^2$, *and
the same rotation-invariant impulse magnitude $|P + iQ|$; the seven
cells are congruent as dynamical systems, and their shape cycles are
periodic with one common period.*

*Proof sketch.* Each line is a rotation image of $L_0$, so the cells
are congruent — equal invariants follow. The Hamiltonian of one cell
is $-\frac{\Gamma^2}{2\pi}(\ln s_1 + \ln s_2 + \ln s_3) =
-\frac{\Gamma^2}{2\pi}\ln(R^3\sqrt{7})$ by Theorem A's product
identity — the same for all seven. The moment of inertia is
$\Gamma\sum|z_k|^2 = 3\Gamma R^2$: every vertex sits on the
circumcircle. The shape periodicity is the classical integrability of
the three-vortex problem: the shape variable moves on the closed
level curve of $H$ inside the fixed-$I$ shape domain. $\square$

### 7.2 The measurement

Stage P6 integrates all seven cells concurrently (one batched RK4 over
the $(7,3,2)$ position array) and records:

- the seven Hamiltonians equal to $1.79\times10^{-16}$ relative of the
  closed form, with spread $5.6\times10^{-17}$ (absolute);
- the invariant drifts along the shape cycle below $9.2\times10^{-14}$;
- the seven shape periods $T_{shape} = 9.3814\ldots$ agreeing with
  spread **exactly 0.0** (the same integration, the same grid, congruent
  initial data);
- the return residual $3.9\times10^{-7}$;
- the honest obstruction: the maximal shape departure is $0.288$ — a
  scalene Fano cell is **not** a relative equilibrium, the shape
  genuinely leaves and returns.

The last register is the bench's honesty anchor: the figure does not
pretend its cells are rigid. What PSL(2,7) buys is not rigidity of the
cells but the *equality of their cycles* — a dynamical symmetry, not a
static one.

---

## 8. The gravity bridge and the mass-ladder deficit (Lemma E)

### 8.1 Gravity as exact geometry

Stage P7 binds the committed register to exact closed forms in three
registers.

**The Schwarzschild ladder.** $r_s = 2\mathrm{GM}/c^2$: the Sun
$2953.25$ m, Jupiter $2.82$ m, Saturn $0.84$ m, Neptune $0.46$ m,
Uranus $0.39$ m, Earth $8.87$ mm, Venus $7.23$ mm, Mars $0.95$ mm,
Mercury $0.49$ mm. The arithmetic is certified against mpmath at
$1.0\times10^{-16}$ — gravity rendered as literal, exact figure
dimensions, nine orders of magnitude from the Sun's horizon to
Mercury's millimetre.

**The Hill margins.** For adjacent planet pairs the ratio
$\Delta a / (r_{H,i} + r_{H,j})$ never drops below $5.08$ (the pair
Jupiter–Saturn) — the non-crossing certificate of the planetary
cells, registered at $\ge 3$.

**The figure dimensions in the sky.** The chords $s_1, s_2, s_3$ of
Theorem A at $R = 1$ AU: $1.298\times10^{11}$ m,
$2.339\times10^{11}$ m, $2.917\times10^{11}$ m.

### 8.2 The deficit

**Lemma E.** *The gravity ladder
$\delta_i = \log_{10}(\mathrm{GM}_i/\mathrm{GM}_\oplus)$ summed over
the seven Fano lines ranges from $0.008$ (Mercury+Mars+Neptune) to
$6.715$ (Jupiter+Saturn+Neptune) — a spread of $6.71$ dex; and a
circulation ladder $\Gamma_i$ built from the same weights deforms the
heptagon lattice by $0.298$ within one rotation while the
equal-circulation ring stays rigid to $9.8\times10^{-15}$.*

The interpretation is the bench's headline honesty: the figure is
mass-blind by construction — $\mathrm{PSL}(2,7)$ treats its seven
points equally — while the solar system spans eight orders of
magnitude in gravitational strength. The bench does not tune the
figure to hide this; it measures the deficit twice, statically (the
line sums) and dynamically (the weighted lattice), and records both.
The mean-motion ladder of the planets spans $684.1$ from Mercury to
Neptune against the figure's chord ladder of $2.247$ — recorded in the
same diagnostics block: the figure is a register of symmetry, not a
metric model of the sky.

---

## 9. The numerical protocol summary

| stage | register | tolerance | recorded | wall (default) |
|:-----:|----------|-----------|----------|:------:|
| P1 | figure literals + Kepler–Earth anchor | $10^{-15}$ / $10^{-4}$ | $4.9\times10^{-16}$ / $9.7\times10^{-6}$ | 0.2 s |
| P2 | Kepler III, two-body, 8 planets | $10^{-9}$ | $6.2\times10^{-13}$ | 1.2 s |
| P3 | N-body conservation + elements | $10^{-9}$ / $10^{-2}$ / $10^{-4}$ | $2.1\times10^{-13}$ / $4.9\times10^{-3}$ / $2.5\times10^{-5}$ | 5.3 s |
| P4 | PSL(2,7) algebra | exact / $10^{-12}$ | exact / $6.7\times10^{-16}$ | 0.04 s |
| P5 | the lattice | $10^{-9}$ / $10^{-12}$ / $10^{-7}$ | $1.3\times10^{-12}$ / $1.2\times10^{-14}$ / $7.0\times10^{-9}$ | 0.8 s |
| P6 | the seven cells | $10^{-12}$ / $10^{-6}$ | $9.1\times10^{-14}$ / $0.0$ | 7.7 s |
| P7 | the bridge | $10^{-12}$ / $\ge 3$ | $1.0\times10^{-16}$ / $5.08$ | 0.4 s |
| X1 | PSL(2,7) from first principles | exact integers | exact; simple | 0.03 s |
| X2 | the two natural actions + the Sylow census | exact integers | exact; bridge found | 0.15 s |
| X3 | the (2,3,7) generation + Hurwitz + Klein | exact integers | exact; 0 non-generating | 1.6 s |
| X4 | the hyperbolic $\{7,3\}$ figure + the disk witness | $10^{-48}$ / $10^{-9}$ | $3.2\times10^{-29}$; witness $0.0$ / $1.1\times10^{-16}$ | 0.2 s |
| X5 | the integrator certification | slopes $\pm 0.2$; trend $\le 0.1$ | $2.0004$ / $3.995$; $0.006$ vs $0.99$ | 3.3 s |
| X6 | the 1PN GR bridge | $5\times10^{-3}$ / $5\times10^{-8}$ | $4.6\times10^{-4}$; Mercury $42.982''$/century | 7.0 s |

Presets: `quick` (≈ 8 s smoke of both suites), `default` (≈ 33 s, the
committed protocols), `full` (≈ 120 s, release validation: 40 years of
N-body at $\mathrm{dt} = 10^{-4}$, 60-digit mpmath literals, four ring
revolutions, 60-orbit 1PN windows). The protocols are deterministic; a
`git diff` on `results/protocols/` after a re-run must be empty (the
run stamp excepted). The X-register records into the same envelope
with `suite = planetvortex-hardcore`.

---

## 10. Honesty notes

- The figure is a **register of symmetry, not a metric model of the
  sky**. No claim of physical vortex-planet identity is made; the
  direction of every quantitative statement is from the registers
  toward the figure, measuring the distance, never from the figure
  toward predictions about the planets.
- The mass ladder **breaks** the figure's symmetry; the bench
  quantifies the deficit (6.71 dex static, 0.298 dynamic) instead of
  tuning it away.
- The planetary simulation is a **planar idealization** with aligned
  perihelia; its registers certify the dynamics against the committed
  initial condition, not the calendar ephemeris.
- The fact-sheet periods are **rounded and epoch-mixed** at
  $4.8\times10^{-4}$; the Kepler register is dynamic, and the table
  inconsistency is recorded, not absorbed.
- Stability is **spectral (linear)**; nothing beyond the linearized
  classification is claimed.
- The three-vortex cells are **integrable but not rigid**; the
  scalene cell is not a relative equilibrium, and the shape cycles are
  the honest substitute.
- The measured planetary periods differ from the committed table at
  $10^{-5}$–$10^{-4}$ — mutual perturbations plus provenance, quoted
  as physics, not dismissed as error.

---

## 11. Резюме (RU)

Мини-репозиторий `planetvortex` строит «гравитационную фигуру»
Солнечной системы: правильный семиугольник радиуса $R = 1$ а.е. с
Солнцем в центре и семью планетами-блуждающими в вершинах (Меркурий,
Венера, Марс, Юпитер, Сатурн, Уран, Нептун — в порядке периодов), на
котором начерчены семь прямых Фано $\{i, i+1, i+3\}$ — точечно-линейная
структура с группой автоморфизмов $\mathrm{PSL}(2,7)$ порядка 168.

Теорема A вычисляет точные размеры фигуры: каждая прямая Фано —
конгруэнтный разносторонний треугольник с углами $(\pi/7, 2\pi/7,
4\pi/7)$, сторонами $2R\sin(k\pi/7)$ и площадью $\sqrt{7}R^2/4$ — по
классическому тождеству произведения синусов. Теорема B показывает,
что семь трёхвихревых ячеек Тривортекса несут в точности одинаковые
гамильтонианы $-(\Gamma^2/2\pi)\ln(\sqrt{7}R^3)$ и конгруэнтные
шейп-циклы с периодом $9{,}3814$ и разбросом ровно ноль — динамическая
тень $\mathrm{PSL}(2,7)$. Теорема C сертифицирует семиугольную
решётку как устойчивое по Хавелоку относительное равновесие с
$\omega_7 = 3\Gamma/2\pi R^2$ — строка $N = 7$ скана соседнего стенда,
запинненная бит-в-бит. Лемма D сертифицирует третий закон Кеплера
динамически: с поправкой на массу — до $6{,}2\times10^{-13}$ по всем
восьми планетам, без неё — промах на физическую сигнатуру
$m_i/2M_\odot$ до $4{,}77\times10^{-4}$ (Юпитер). Лемма E честно
измеряет дистанцию между фигурой и небом: лестница гравитаций даёт
разброс сумм по прямым $6{,}71$ dex, а мягкая гравитационно-взвешенная
лестница циркуляций деформирует вихревую фигуру на $0{,}30$ за одно
вращение при жёсткости равноциркуляционного кольца до
$9{,}8\times10^{-15}$.

Полное ньютоновское моделирование «Солнце + 8 планет» (12 лет, RK4)
даёт дрейф энергии $2{,}1\times10^{-13}$; все семь ступеней P-лестницы
закоммичены как детерминированные JSON-протоколы, и каждый протокол
перевыверяется CI на каждый пуш. Фигура — регистр симметрии, а не
метрическая модель неба: стенд измеряет дефицит связки, а не прячет
его.

---

## Appendix X — the hardcore register (X1–X6)

The P-ladder registers; the X-register attacks. Where a ladder stage
asserts a claim with a committed tolerance, the corresponding X stage
re-derives the same claim by a second, independent route — brute-force
enumeration where the objects are finite, exact integer arithmetic
where the statement is arithmetic, and a numerical construction where
a closed form could be quietly wrong. The appendix records the six
stages; the committed protocols carry the full parameter snapshots.

**X1 — the group from nothing.** All $49^2 = 2401$ matrices over
$\mathbb{F}_7$ are enumerated and classified: $2016$ invertible
(exactly $(7^2-1)(7^2-7)$), $336$ of determinant one (exactly
$7(7^2-1)$), and — quotienting by $\pm I$ — $168$ classes, each with
exactly two lifts. The centre of $\mathrm{SL}(2,7)$ is $\{\pm I\}$;
the centre of the quotient is trivial. The conjugacy computation
partitions the group into classes of sizes
$1, 21, 24, 24, 42, 56$ — the classical class equation — and the
element-order census reads $1 + 21 + 56 + 42 + 48 = 168$. Simplicity
is certified exhaustively: every normal subgroup is a union of
conjugacy classes containing the identity, and all $2^5 = 32$ such
unions are checked against Lagrange — none of the intermediate sizes
divides $168$.

**X2 — the two actions.** Conjugation on the Sylow subgroups yields
the two natural permutation representations. The Sylow census is
computed, not quoted: $n_7 = 8$ (the projective line
$\mathbb{P}^1(\mathbb{F}_7)$), $n_3 = 28$, $n_2 = 21$ with the
self-normalizing dihedral Sylow-2 of order 8. The $8$-point action is
certified 2-transitive (one orbit on the $56$ ordered pairs) and
3-homogeneous (one orbit on the $56$ triples); the point stabilizer is
the Frobenius group of order $21$ with the exact census
$(1, 14, 6)$. The $7$-point action lives on one of the two conjugacy
classes of $S_4$ subgroups (both are computed, $7 + 14$ total
counting the second class); the stabilizer carries the signature
$(1, 9, 8, 6)$ of $S_4$. The bridge: a permutation
$\sigma \in S_7$ exists conjugating the action image onto the
research model of `fano.py` — the Fano points of the figure are
*proven* to be the seven conjugate $S_4$ subgroups.

**X3 — the triangle generation and the Hurwitz arithmetic.** Every
one of the $336$ pairs $(a, b)$ with $|a| = 2$, $|b| = 3$,
$|ab| = 7$ generates the whole group (the product-order distribution
over all $21 \times 56 = 1176$ pairs reads $\{2{:}\,168,\ 3{:}\,336,\
4{:}\,336,\ 7{:}\,336\}$; a subgroup carrying orders $2, 3, 7$ has
order divisible by $42$, and orders $42$ and $84$ are excluded by the
coset action and simplicity). The Klein relations
$a^2 = b^3 = (ab)^7 = [a,b]^4 = 1$ hold on the witness. The Hurwitz
bound $84(g-1) = 168$ and the Riemann–Hurwitz arithmetic
$42(2g-2) = 168$ are exact integers; the orbifold curvature of the
$(2,3,7)$ signature is $-1/42$. The Klein quartic
$x^3y + y^3z + z^3x = 0$ is proven smooth without any symbolic
dependency: multiplying the three gradient equations gives
$27(xyz)^3 = -(xyz)^3$, hence $28(xyz)^3 = 0$ — impossible over
$\mathbb{C}$; every coordinate-zero branch collapses to the trivial
vector. A smooth plane quartic has genus $(4-1)(4-2)/2 = 3$.

**X4 — the hyperbolic figure and its witness.** The fundamental right
triangle of the $\{7,3\}$ tiling (angles $\pi/7$ at the heptagon
centre, $\pi/3$ at the vertex, $\pi/2$ at the edge midpoint) has the
exact dimensions
$\cosh(\ell/2) = \cos(\pi/7)/\sin(\pi/3)$,
$\cosh r = \cos(\pi/3)/\sin(\pi/7)$,
$\cosh R = \cot(\pi/7)\cot(\pi/3)$, verified against the
hyperbolic Pythagoras $\cosh R = \cosh(\ell/2)\cosh r$ at 50 dps
(residual $3.2\times10^{-29}$, the rounding floor of $\pi$ itself).
The area ladder is exact: triangle $\pi/42$, heptagon $\pi/3$, total
$8\pi = 2\pi(2g-2)$ — Gauss–Bonnet on the genus-3 surface. The
combinatorial closure $3V = 7F = 2E = 168$ and
$14F = 4E = 6V = 336$ holds with $V = 56$, $E = 84$, $F = 24$,
$\chi = -4$. As the independent witness, a regular heptagon is
constructed directly in the Poincaré disk and its interior angle is
solved to $2\pi/3$ by bisection: the resulting circumradius matches
the closed form to $0.0$ and the edge to $1.1\times10^{-16}$ — two
routes, one number.

**X5 — the integrators certified.** The convergence order is
*measured*, not asserted: regressing $\log$(error) on $\log(\mathrm{dt})$
over the committed grids gives slope $2.0004$ for the leapfrog and
$3.995$ for the Yoshida composition on a Kepler orbit with $e = 0.4$.
Forward–backward integration recovers the initial state to $7.5\times10^{-12}$
(self-adjointness at roundoff). The symplectic energy envelope is
bounded with no secular trend — the linear-trend ratio over an
80-period window is $0.006$ (leapfrog) and $0.0002$ (Yoshida) against
$0.99$ for the RK4 control on the same window — the drift signature
that separates the two families. Along a Yoshida orbit the
Laplace–Runge–Lenz vector drifts at $5.5\times10^{-11}$, the vis-viva
law holds to $2.3\times10^{-12}$ and the exact orbit equation
$r = p/(1 + e\cos\theta)$ to $7.3\times10^{-11}$.

**X6 — the GR bridge.** The 1PN acceleration (Schwarzschild test
particle, harmonic gauge) is integrated for Mercury, Venus and Earth;
the perihelion advance is measured from interpolated perihelion
passages and compared with the closed form
$\Delta\varpi = 6\pi\mathrm{GM}/(a(1-e^2)c^2)$. The worst
measured-over-formula deviation is $4.6\times10^{-4}$; the Newtonian
control run advances $1.9\times10^{-10}$ rad/orbit — integrator zero,
as it must before the PN measurement means anything. Mercury's
precession integrates to $42.982''$ per century against the textbook
$42.98''$ (relative error $5.3\times10^{-5}$), computed from the same
committed register the figure binds; the full eight-planet formula
ladder descends monotonically from $42.98''$ to $0.0008''$.

The layer adds no physics and removes none: it is the same bench
attacked from the sides the P-ladder leaves open. Its protocols live
in the same folder, under the same envelope, behind the same discipline
— every tolerance committed before the recorded run.

---

## References

1. Trivortex — the parent framework: Theorem 3.1, the V1–V4 ladder,
   the mini-research program. Repository root README, DOI
   10.5281/zenodo.21825394.
2. Polyvortex — the N-vortex extension bench: the W-ladder, the
   Havelock threshold at $N = 7\,|\,8$, the $\pi\ln 2$ admissibility
   boundary. `polyvortex/` of the same repository.
3. Cycloring — the ring laboratory: the Gamma-period registers and the
   W-ladder. `cycloring/` of the same repository.
4. NASA NSSDC planetary fact sheets — the GM, radii, periods and
   surface gravities of the committed register.
   https://nssdc.gsfc.nasa.gov/planetary/factsheet/
5. JPL, Keplerian elements for approximate positions of the major
   planets — the J2000 mean elements of the committed register.
   https://ssd.jpl.nasa.gov/planets/approx_pos.html
6. H. Aref, Motion of three vortices — the classical integrability and
   the shape periodicity of the three-vortex problem.
7. J. J. Thomson, A Treatise on the Motion of Vortex Rings — the
   N-vortex ring and its relative equilibria.
8. H. S. M. Coxeter, Twelve Geometric Essays — the Fano plane, the
   Klein quartic and the group of order 168.
