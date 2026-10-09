/*
 * ============================================================================
 * PLANETVORTEX — GRAVIKERNEL.C — the C99 cross-language oracle
 * ============================================================================
 * The independent C re-implementation of the load-bearing registers of
 * the bench, used by tools/crosslang_diff.py to pin the Python layer
 * against a second language (the same discipline as the polyvortex
 * sibling's C port):
 *
 *   part 1  PSL(2,7) from nothing: all 2401 2x2 matrices over F_7,
 *           |GL| = 2016, |SL| = 336, |PSL| = 168 (canonical +- reps);
 *           the (2,3,7) witness search; the coset geometry of the
 *           Klein map {7,3}_8: V = 56, E = 84, F = 24, Euler = -4,
 *           the antipodal freeness of the witness involution
 *   part 2  the gravimetric register algebra of the 12 bodies: the
 *           geometric-mean normalization sum(s_i) = 0, the vertex
 *           angles alpha_i = 2pi/3 - sigma*s_i, the exact closed
 *           forms cosh R = cot(a/2)cot(pi/7), cosh(l/2) =
 *           cos(pi/7)/sin(a/2), cosh r = cos(a/2)/sin(pi/7),
 *           A = 5pi - 7a, and the budget closure sum(alpha) = 8pi
 *           in double AND long double
 *   part 3  the V1 spatial registers: the SO(3) tilt operators
 *           T = R_z(Om) R_x(i) with their orthogonality residuals,
 *           the arc registers lambda = i (R_bar = 1 AU), and the 3D
 *           two-body Kepler anchor: one Earth period integrated with
 *           RK4, measured against the closed form
 *
 * Build:  make -C c          (cc -O2 -std=c99 -Wall -Wextra)
 * Run:    c/gravikernel      (writes one JSON object to stdout)
 *
 * License: LicenseRef-Proprietary-Wild8Highlander-1.0 (see LICENSE.md)
 * Year: 2026
 * ============================================================================
 */

#include <math.h>
#include <stdio.h>

#define F7 7
#define N_PSL 168
#define N_BODIES 12
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

/* ---------------------------------------------------------------- */
/* F_7 arithmetic on 2x2 matrices (rows m[0], m[1])                  */
/* ---------------------------------------------------------------- */

typedef struct { int m[2][2]; } Mat;

static Mat mat_mul(Mat a, Mat b) {
    Mat r;
    for (int i = 0; i < 2; i++)
        for (int j = 0; j < 2; j++)
            r.m[i][j] = (a.m[i][0] * b.m[0][j] + a.m[i][1] * b.m[1][j]) % F7;
    return r;
}

static int mat_det(Mat a) {
    int d = (a.m[0][0] * a.m[1][1] - a.m[0][1] * a.m[1][0]) % F7;
    return (d + F7) % F7;
}

static Mat mat_neg(Mat a) {
    Mat r;
    for (int i = 0; i < 2; i++)
        for (int j = 0; j < 2; j++)
            r.m[i][j] = (F7 - a.m[i][j]) % F7;
    return r;
}

static int mat_less(Mat a, Mat b) {
    for (int i = 0; i < 2; i++)
        for (int j = 0; j < 2; j++)
            if (a.m[i][j] != b.m[i][j]) return a.m[i][j] < b.m[i][j];
    return 0;
}

static Mat mat_canon(Mat a) { /* the PSL class: lexicographic min of +-A */
    Mat n = mat_neg(a);
    return mat_less(a, n) ? a : n;
}

static int mat_eq(Mat a, Mat b) {
    for (int i = 0; i < 2; i++)
        for (int j = 0; j < 2; j++)
            if (a.m[i][j] != b.m[i][j]) return 0;
    return 1;
}

/* ---------------------------------------------------------------- */
/* part 1 — the group and the map                                    */
/* ---------------------------------------------------------------- */

static Mat g_psl[N_PSL];
static unsigned char g_mult[N_PSL][N_PSL];
static int g_identity = 0;

static void build_psl(int *out_gl, int *out_sl) {
    int gl = 0, sl = 0, n = 0;
    for (int a = 0; a < F7; a++)
    for (int b = 0; b < F7; b++)
    for (int c = 0; c < F7; c++)
    for (int d = 0; d < F7; d++) {
        Mat m = {{{a, b}, {c, d}}};
        if (mat_det(m) == 0) continue;
        gl++;
        if (mat_det(m) != 1) continue;
        sl++;
        Mat canon = mat_canon(m);
        int seen = 0;
        for (int k = 0; k < n; k++)
            if (mat_eq(g_psl[k], canon)) { seen = 1; break; }
        if (!seen) g_psl[n++] = canon;
    }
    *out_gl = gl;
    *out_sl = sl;
}

static int psl_find(Mat m) {
    for (int i = 0; i < N_PSL; i++)
        if (mat_eq(g_psl[i], m)) return i;
    return -1;
}

static void build_table(void) {
    for (int i = 0; i < N_PSL; i++)
        for (int j = 0; j < N_PSL; j++)
            g_mult[i][j] = (unsigned char)psl_find(mat_canon(mat_mul(g_psl[i], g_psl[j])));
}

static int psl_order(int i) {
    int p = i;
    for (int n = 1; n <= 7; n++) {
        if (p == g_identity) return n;
        p = g_mult[p][i];
    }
    return -1;
}

static int right_cosets(int gen, int *coset_of) {
    int cyc[8], len = 0;
    int cur = gen;
    cyc[len++] = cur;
    while (1) {
        cur = g_mult[cur][gen];
        if (cur == gen) break;
        cyc[len++] = cur;
    }
    int member_coset[N_PSL];
    for (int i = 0; i < N_PSL; i++) member_coset[i] = -1;
    int n_cosets = 0;
    for (int g = 0; g < N_PSL; g++) {
        if (member_coset[g] >= 0) continue;
        int id = n_cosets++;
        for (int k = 0; k < len; k++)
            member_coset[g_mult[g][cyc[k]]] = id;
    }
    for (int i = 0; i < N_PSL; i++) coset_of[i] = member_coset[i];
    return n_cosets;
}

/* ---------------------------------------------------------------- */
/* part 2 — the gravimetric register algebra                         */
/* ---------------------------------------------------------------- */

static const double G_GM[N_BODIES] = {
    1.32712440018e20, 2.2032e13, 3.24859e14, 3.986004418e14, 4.282837e13,
    1.26686534e17, 3.7931187e16, 5.793939e15, 6.836529e16,
    6.26325e10, 8.696e11, 1.108e12
};
static const char *G_NAMES[N_BODIES] = {
    "Sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter",
    "Saturn", "Uranus", "Neptune", "Ceres", "Pluto", "Eris"
};

static double d_cot(double x) { return cos(x) / sin(x); }

/* ---------------------------------------------------------------- */
/* part 3 — the spatial registers                                    */
/* ---------------------------------------------------------------- */

static const double G_INCL[N_BODIES - 1] = {
    7.00497902, 3.39467605, 0.00001531, 1.84969142, 1.30439695,
    2.48599187, 0.77263783, 1.77004347, 10.5876, 17.14001206, 44.040
};
static const double G_NODE[N_BODIES - 1] = {
    48.33076593, 76.67984255, -11.26064, 49.55953891, 100.47390909,
    113.66242448, 74.01692503, 131.78422574, 80.393, 110.30393684, 35.951
};
static const char *G_SPATIAL_NAMES[N_BODIES - 1] = {
    "Mercury", "Venus", "Earth", "Mars", "Jupiter",
    "Saturn", "Uranus", "Neptune", "Ceres", "Pluto", "Eris"
};

static void tilt_matrix(double i_deg, double o_deg, double T[3][3]) {
    double i = i_deg * M_PI / 180.0, w = o_deg * M_PI / 180.0;
    double ci = cos(i), si = sin(i), co = cos(w), so = sin(w);
    double rz[3][3] = {{co, -so, 0}, {so, co, 0}, {0, 0, 1}};
    double rx[3][3] = {{1, 0, 0}, {0, ci, -si}, {0, si, ci}};
    for (int r = 0; r < 3; r++)
        for (int c = 0; c < 3; c++) {
            double s = 0.0;
            for (int k = 0; k < 3; k++) s += rz[r][k] * rx[k][c];
            T[r][c] = s;
        }
}

/* the 3D two-body Kepler anchor: two Earth revolutions, RK4, the
   period measured from the first perihelion (t = 0) to the next local
   minimum of r(t) (3-point detection) */
static double earth_period_anchor(int steps_per_revolution) {
    double mu = 4.0 * M_PI * M_PI * (1.0 + 3.986004418e14 / 1.32712440018e20);
    double a = 1.00000261, e = 0.01671123;
    double dt = 2.0 * M_PI * sqrt(a * a * a / mu) / steps_per_revolution;
    double x = a * (1.0 - e), y = 0.0, vx = 0.0, vy = sqrt(mu * (1.0 + e) / (a * (1.0 - e)));
    double r_pprev = sqrt(x * x + y * y); /* t = 0: the perihelion */
    double r_prev = r_pprev;
    double t_next_min = 0.0;
    int found = 0;
    double t = 0.0;
    int total = steps_per_revolution * 2 + 10;
    for (int s = 1; s <= total && !found; s++) {
        double k1x = vx, k1y = vy;
        double r1 = sqrt(x * x + y * y), f1 = -mu / (r1 * r1 * r1);
        double k1vx = f1 * x, k1vy = f1 * y;
        double x2 = x + 0.5 * dt * k1x, y2 = y + 0.5 * dt * k1y;
        double vx2 = vx + 0.5 * dt * k1vx, vy2 = vy + 0.5 * dt * k1vy;
        double r2 = sqrt(x2 * x2 + y2 * y2), f2 = -mu / (r2 * r2 * r2);
        double k2x = vx2, k2y = vy2, k2vx = f2 * x2, k2vy = f2 * y2;
        double x3 = x + 0.5 * dt * k2x, y3 = y + 0.5 * dt * k2y;
        double vx3 = vx + 0.5 * dt * k2vx, vy3 = vy + 0.5 * dt * k2vy;
        double r3 = sqrt(x3 * x3 + y3 * y3), f3 = -mu / (r3 * r3 * r3);
        double k3x = vx3, k3y = vy3, k3vx = f3 * x3, k3vy = f3 * y3;
        double x4 = x + dt * k3x, y4 = y + dt * k3y;
        double vx4 = vx + dt * k3vx, vy4 = vy + dt * k3vy;
        double r4 = sqrt(x4 * x4 + y4 * y4), f4 = -mu / (r4 * r4 * r4);
        double k4x = vx4, k4y = vy4, k4vx = f4 * x4, k4vy = f4 * y4;
        x += dt / 6.0 * (k1x + 2 * k2x + 2 * k3x + k4x);
        y += dt / 6.0 * (k1y + 2 * k2y + 2 * k3y + k4y);
        vx += dt / 6.0 * (k1vx + 2 * k2vx + 2 * k3vx + k4vx);
        vy += dt / 6.0 * (k1vy + 2 * k2vy + 2 * k3vy + k4vy);
        t += dt;
        double r = sqrt(x * x + y * y);
        if (s >= 2 && r_pprev > r_prev && r > r_prev) {
            t_next_min = t - dt; /* r_prev sat at t - dt */
            found = 1;
        }
        r_pprev = r_prev;
        r_prev = r;
    }
    if (!found) return 0.0;
    return t_next_min;
}

/* ---------------------------------------------------------------- */

int main(void) {
    int gl = 0, sl = 0;
    build_psl(&gl, &sl);
    g_identity = psl_find(mat_canon((Mat){{{1, 0}, {0, 1}}}));
    build_table();
    if (g_identity < 0) { fprintf(stderr, "identity not found\n"); return 1; }

    int orders[N_PSL];
    int n_inv = 0, n_ord3 = 0;
    for (int i = 0; i < N_PSL; i++) {
        orders[i] = psl_order(i);
        if (orders[i] == 2) n_inv++;
        if (orders[i] == 3) n_ord3++;
    }
    int wit_a = -1, wit_b = -1;
    for (int a = 0; a < N_PSL && wit_a < 0; a++)
        for (int b = 0; b < N_PSL; b++)
            if (orders[a] == 2 && orders[b] == 3 && orders[g_mult[a][b]] == 7) {
                wit_a = a; wit_b = b; break;
            }
    int c_elem = g_mult[wit_a][wit_b];

    int coset_v[N_PSL], coset_e[N_PSL], coset_f[N_PSL];
    int n_v = right_cosets(wit_b, coset_v);
    int n_e = right_cosets(wit_a, coset_e);
    int n_f = right_cosets(c_elem, coset_f);

    int face_fixed = 0;
    for (int g = 0; g < N_PSL; g++)
        if (coset_f[g_mult[wit_a][g]] == coset_f[g]) face_fixed++;

    /* part 2 */
    double ln_gm[N_BODIES], mean_ln = 0.0;
    for (int i = 0; i < N_BODIES; i++) {
        ln_gm[i] = log(G_GM[i]);
        mean_ln += ln_gm[i] / N_BODIES;
    }
    double s[N_BODIES], alpha[N_BODIES];
    double s_sum = 0.0, worst_neg = 0.0;
    for (int i = 0; i < N_BODIES; i++) {
        s[i] = ln_gm[i] - mean_ln;
        s_sum += s[i];
        if (-s[i] > worst_neg) worst_neg = -s[i];
    }
    double headroom = 5.0 * M_PI / 7.0 - 2.0 * M_PI / 3.0;
    double sigma = 0.95 * headroom / worst_neg;
    double alpha_sum = 0.0, area_sum = 0.0, pyth = 0.0;
    for (int i = 0; i < N_BODIES; i++) {
        alpha[i] = 2.0 * M_PI / 3.0 - sigma * s[i];
        alpha_sum += alpha[i];
        area_sum += 2.0 * (5.0 * M_PI - 7.0 * alpha[i]);
        double ch_r = d_cot(alpha[i] / 2.0) * d_cot(M_PI / 7.0);
        double ch_h = cos(M_PI / 7.0) / sin(alpha[i] / 2.0);
        double ch_i = cos(alpha[i] / 2.0) / sin(M_PI / 7.0);
        double resid = fabs(ch_r - ch_h * ch_i);
        if (resid > pyth) pyth = resid;
    }
    /* the long double shadow */
    long double ld_ln[N_BODIES], ld_mean = 0.0L;
    for (int i = 0; i < N_BODIES; i++) {
        ld_ln[i] = logl((long double)G_GM[i]);
        ld_mean += ld_ln[i] / N_BODIES;
    }
    long double ld_s_sum = 0.0L, ld_worst = 0.0L;
    for (int i = 0; i < N_BODIES; i++) {
        long double si = ld_ln[i] - ld_mean;
        ld_s_sum += si;
        if (-si > ld_worst) ld_worst = -si;
    }
    long double ld_headroom = 5.0L * M_PI / 7.0L - 2.0L * M_PI / 3.0L;
    long double ld_sigma = 0.95L * ld_headroom / ld_worst;
    long double ld_alpha_sum = 0.0L;
    for (int i = 0; i < N_BODIES; i++)
        ld_alpha_sum += 2.0L * M_PI / 3.0L - ld_sigma * (ld_ln[i] - ld_mean);

    /* part 3 */
    double worst_orth = 0.0;
    for (int b = 0; b < N_BODIES - 1; b++) {
        double T[3][3];
        tilt_matrix(G_INCL[b], G_NODE[b], T);
        for (int r = 0; r < 3; r++)
            for (int c = 0; c < 3; c++) {
                double dot = 0.0;
                for (int k = 0; k < 3; k++) dot += T[k][r] * T[k][c];
                double resid = fabs(dot - (r == c ? 1.0 : 0.0));
                if (resid > worst_orth) worst_orth = resid;
            }
    }
    double kepler_T = earth_period_anchor(6000);
    double mu_e = 4.0 * M_PI * M_PI * (1.0 + 3.986004418e14 / 1.32712440018e20);
    double kepler_expect = 2.0 * M_PI * sqrt(pow(1.00000261, 3.0) / mu_e);
    double kepler_rel = fabs(kepler_T - kepler_expect) / kepler_expect;

    /* ---------------- the JSON ---------------- */
    printf("{\n");
    printf("  \"kernel\": \"gravikernel.c\",\n");
    printf("  \"language\": \"C99\",\n");
    printf("  \"group\": {\"gl2_7\": %d, \"sl2_7\": %d, \"psl2_7\": %d, ", gl, sl, N_PSL);
    printf("\"involutions\": %d, \"order3\": %d, ", n_inv, n_ord3);
    printf("\"witness_ab_order\": %d},\n", orders[c_elem]);
    printf("  \"map\": {\"V\": %d, \"E\": %d, \"F\": %d, \"euler\": %d, ", n_v, n_e, n_f, n_v - n_e + n_f);
    printf("\"face_fixed_points\": %d},\n", face_fixed);
    printf("  \"register_algebra\": {\n");
    printf("    \"sigma\": %.17g,\n", sigma);
    printf("    \"s_sum\": %.17g,\n", s_sum);
    printf("    \"alpha_sum\": %.17g,\n", alpha_sum);
    printf("    \"alpha_sum_residual\": %.17g,\n", fabs(alpha_sum - 8.0 * M_PI));
    printf("    \"total_area\": %.17g,\n", area_sum);
    printf("    \"total_area_residual\": %.17g,\n", fabs(area_sum - 8.0 * M_PI));
    printf("    \"worst_pythagoras_residual\": %.17g,\n", pyth);
    printf("    \"ld_s_sum\": %.21Lg,\n", ld_s_sum);
    printf("    \"ld_alpha_sum_residual\": %.21Lg,\n", fabsl(ld_alpha_sum - 8.0L * M_PI));
    printf("    \"bodies\": [\n");
    for (int i = 0; i < N_BODIES; i++) {
        double ch_r = d_cot(alpha[i] / 2.0) * d_cot(M_PI / 7.0);
        double edge = 2.0 * acosh(cos(M_PI / 7.0) / sin(alpha[i] / 2.0));
        double inr = acosh(cos(alpha[i] / 2.0) / sin(M_PI / 7.0));
        printf("      {\"body\": \"%s\", \"gm\": %.17g, \"s\": %.17g, \"alpha\": %.17g, ",
               G_NAMES[i], G_GM[i], s[i], alpha[i]);
        printf("\"circumradius\": %.17g, \"edge\": %.17g, \"inradius\": %.17g, \"area\": %.17g}%s\n",
               acosh(ch_r), edge, inr, 5.0 * M_PI - 7.0 * alpha[i], i == N_BODIES - 1 ? "" : ",");
    }
    printf("    ]\n  },\n");
    printf("  \"spatial\": {\"worst_orthogonality\": %.3g, \"earth_period_anchor_rel\": %.3g},\n",
           worst_orth, kepler_rel);
    printf("  \"inclination_register\": [\n");
    for (int b = 0; b < N_BODIES - 1; b++) {
        printf("      {\"body\": \"%s\", \"inclination_deg\": %.8f, \"node_deg\": %.8f, \"arc\": %.17g}%s\n",
               G_SPATIAL_NAMES[b], G_INCL[b], G_NODE[b], G_INCL[b] * M_PI / 180.0,
               b == N_BODIES - 2 ? "" : ",");
    }
    printf("    ]\n}\n");
    return 0;
}
