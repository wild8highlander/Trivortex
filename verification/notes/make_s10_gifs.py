#!/usr/bin/env python3
"""Generate the two Section-10 GIF assets for the Lean4 package:

  assets/lyapunov_stability.gif      — §10.1: perturbed Lagrange triangle,
                                       RK4 of the TRUE Kirchhoff ODE, the
                                       certified bound sum (d2-1)^2 <=
                                       (12 pi / G^2) H(0) held for all t;
  assets/collinear_bifurcation.gif   — §10.2/10.3: the chart equation
                                       N(s, gamma) = 0, the pitchfork at
                                       gamma = -5/4, the degenerate
                                       circulations, and the rigidly
                                       rotating collinear configurations.

Palette = the repository traffic-light palette (TL_*, GOLD_B, INK, PAPER).
English labels only. Output frames are quantized to a fixed 256-color
adaptive palette so the GIF stays flat-color and small.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from PIL import Image
import io, os

OUT = "/home/z/my-project/work-lean7/lean4/assets"

# ---------------------------------------------------------------- palette
INK = "#0F0F14"
INK_SOFT = "#282832"
PAPER = "#F0F4F8"
GRY = "#8B98B2"
TL_GREEN = "#34D399"
TL_DIM_G = "#195A3C"
TL_AMBER = "#FACC15"
TL_RED = "#DC323C"
GOLD_B = "#E8C766"

plt.rcParams.update({
    "figure.facecolor": INK, "axes.facecolor": INK,
    "savefig.facecolor": INK, "text.color": PAPER,
    "axes.edgecolor": GRY, "axes.labelcolor": PAPER,
    "xtick.color": GRY, "ytick.color": GRY,
    "font.size": 11, "axes.titlecolor": GOLD_B,
})

# ------------------------------------------------------- Kirchhoff machinery
def field(gam, pos):
    vel = np.zeros((3, 2))
    for k in range(3):
        for j in range(3):
            if j == k:
                continue
            dx, dy = pos[k] - pos[j]
            r2 = dx * dx + dy * dy
            vel[k] += np.array([-gam[j] * dy, gam[j] * dx]) / (2 * np.pi * r2)
    return vel

def hamiltonian(gam, pos):
    h = 0.0
    for i, j in ((0, 1), (0, 2), (1, 2)):
        r = np.sqrt(np.sum((pos[i] - pos[j]) ** 2))
        h += -gam[i] * gam[j] / (2 * np.pi) * np.log(r)
    return h

def rk4_step(pos, dt, gam):
    k1 = field(gam, pos)
    k2 = field(gam, pos + dt / 2 * k1)
    k3 = field(gam, pos + dt / 2 * k2)
    k4 = field(gam, pos + dt * k3)
    return pos + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

def lin_solve(gam, pos, vel, eps=1e-9):
    omegas = []
    for k in range(3):
        num = vel[k, 0] * (-pos[k, 1]) + vel[k, 1] * pos[k, 0]
        den = pos[k, 0] ** 2 + pos[k, 1] ** 2
        if den > eps:
            omegas.append(num / den)
    return float(np.mean(omegas))

VORT_COLORS = [TL_GREEN, GOLD_B, TL_RED]

def quantize(img, palette_img):
    return img.convert("RGB").quantize(palette=palette_img, dither=Image.NONE)

def save_gif(frames_pil, path, duration_ms):
    palette_img = frames_pil[0].convert("RGB").quantize(colors=255)
    q = [quantize(f, palette_img) for f in frames_pil]
    q[0].save(path, save_all=True, append_images=q[1:],
              duration=duration_ms, loop=0, optimize=True)
    print(f"saved {path}: {len(q)} frames, {os.path.getsize(path) / 1e6:.2f} MB")

# =================================================================
# GIF 1 — Lyapunov stability (Section 10.1)
# =================================================================
def make_lyapunov():
    G = 1.0
    gam = [G] * 3
    p0 = np.array([[1 / np.sqrt(3), 0],
                   [-1 / (2 * np.sqrt(3)), 0.5],
                   [-1 / (2 * np.sqrt(3)), -0.5]])
    rho, amp = 1 / 16, 0.22
    u = np.array([0.9, 0.35, -1.25])
    u = u - u.mean()
    pos0 = p0.copy()
    for k in range(3):
        pos0[k] = pos0[k] + amp * rho * u[k] * np.array(
            [np.cos(2 * np.pi * k / 3), np.sin(2 * np.pi * k / 3)])
    pos0 = pos0 - pos0.mean(axis=0)
    pos0 = pos0 / np.sqrt(np.sum(pos0 ** 2))     # I = Gamma exactly
    H0 = hamiltonian(gam, pos0)

    dt, steps = 2e-3, 6000
    traj = np.zeros((steps + 1, 3, 2))
    dev = np.zeros(steps + 1)
    ham = np.zeros(steps + 1)
    traj[0], dev[0], ham[0] = pos0, 0.0, H0
    pos = pos0.copy()
    for s in range(steps):
        pos = rk4_step(pos, dt, gam)
        traj[s + 1] = pos
        d2s = [np.sum((pos[i] - pos[j]) ** 2) for i, j in ((0, 1), (0, 2), (1, 2))]
        dev[s + 1] = sum((d - 1) ** 2 for d in d2s)
        ham[s + 1] = hamiltonian(gam, pos)
    bound = (12 * np.pi / G ** 2) * H0
    T = steps * dt
    omega = 3 / (2 * np.pi)          # Lagrange rate at G=3, a=1
    period = 2 * np.pi / omega

    # circular tracks of the UNperturbed Lagrange triangle (reference)
    ang = np.linspace(0, 2 * np.pi, 200)
    ref_circ = (1 / np.sqrt(3)) * np.stack([np.cos(ang), np.sin(ang)], axis=1)

    n_frames, fps = 88, 12
    idx = np.linspace(0, steps, n_frames).astype(int)
    frames = []
    dev_max = max(dev.max(), bound) * 1.45

    for f in range(n_frames):
        i = idx[f]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.6, 6.15),
                                       gridspec_kw={"width_ratios": [1.25, 1]})
        fig.subplots_adjust(left=0.05, right=0.97, top=0.86, bottom=0.10, wspace=0.18)
        # ---- left: trajectories
        ax1.set_facecolor(INK)
        for k in range(3):
            xs, ys = traj[: i + 1, k, 0], traj[: i + 1, k, 1]
            pts = np.stack([xs, ys], axis=1)
            segs = np.stack([pts[:-1], pts[1:]], axis=1)
            segs = segs[-420:]
            alpha = np.linspace(0.12, 0.95, len(segs))
            lc = LineCollection(segs, colors=[(matplotlib.colors.to_rgba(VORT_COLORS[k], a)) for a in alpha],
                                linewidths=1.7)
            ax1.add_collection(lc)
            ax1.plot(traj[i, k, 0], traj[i, k, 1], "o", ms=11,
                     color=VORT_COLORS[k], mec="white", mew=1.2, zorder=5)
        ax1.plot(ref_circ[:, 0], ref_circ[:, 1], "--", color=GRY, lw=0.8, alpha=0.45)
        for k in range(3):
            ax1.plot(traj[0, k, 0], traj[0, k, 1], "x", ms=7, color=GRY, alpha=0.8)
        ax1.set_xlim(-0.95, 0.95)
        ax1.set_ylim(-0.95, 0.95)
        ax1.set_aspect("equal")
        ax1.grid(alpha=0.15, color=GRY)
        ax1.set_title("perturbed triangle · true Kirchhoff flow (RK4)", fontsize=11.5)
        ax1.text(0.02, 0.02, f"t = {i * dt:5.2f}  ·  {(i * dt) / period:4.2f} periods",
                 transform=ax1.transAxes, color=GRY, fontsize=9.5)
        # ---- right: the certified bound
        tt = np.arange(i + 1) * dt
        ax2.set_facecolor(INK)
        ax2.plot(tt, dev[: i + 1], color=PAPER, lw=1.6,
                 label=r"$\sum_{i<j}(d^2_{ij}-1)^2(t)$")
        ax2.axhline(bound, color=TL_AMBER, ls="--", lw=1.6,
                    label=rf"bound $(12\pi/\Gamma^2)\,H(0) = {bound:.4f}$")
        ax2.fill_between(tt, dev[: i + 1], bound,
                         where=dev[: i + 1] <= bound, color=TL_DIM_G, alpha=0.35)
        ax2.set_xlim(0, T)
        ax2.set_ylim(0, dev_max)
        ax2.grid(alpha=0.15, color=GRY)
        ax2.set_xlabel("t")
        ax2.legend(loc="upper right", fontsize=8.6, framealpha=0.12,
                   facecolor=INK, edgecolor=GRY, labelcolor=PAPER)
        ax2.set_title("Lyapunov certificate vs time", fontsize=11.5)
        ax2.text(0.02, 0.80, rf"$H(0) = {H0:.3e} \leq \frac{{\Gamma^2}}{{12\pi}}\,(1/16)^2$",
                 transform=ax2.transAxes, color=TL_GREEN, fontsize=9.5)
        ax2.text(0.02, 0.73, rf"max drift $H(t)-H(0)$ = {np.abs(ham[:i+1]-H0).max():.1e}",
                 transform=ax2.transAxes, color=GRY, fontsize=9)
        fig.suptitle("TRIVORTEX §10.1 · nonlinear Lyapunov stability via H/I "
                     "(s10_coercive → s10_lyapunov_stab)", color=GOLD_B,
                     fontsize=13, y=0.965)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=110)
        plt.close(fig)
        buf.seek(0)
        frames.append(Image.open(buf).copy())
    save_gif(frames, os.path.join(OUT, "lyapunov_stability.gif"), 1000 // fps)

# =================================================================
# GIF 2 — collinear bifurcation (Sections 10.2/10.3)
# =================================================================
def chart_roots(gamma):
    """Real roots of N(s, gamma) = 0 (numpy), excluding the collision s = 1.
    N = s(s-1)(a s^2 + b s + c) is a QUARTIC: coefficients
    [a, b-a, c-b, -c, 0] (the constant term is 0 -> s = 0 is an exact root)."""
    a = (gamma + 1) ** 2 * (gamma - 1)
    b = gamma * (4 * gamma + 5)
    c = 4 * gamma + 5
    coef = [a, b - a, c - b, -c, 0.0]
    roots = np.roots(coef)
    real = sorted(r.real for r in roots if abs(r.imag) < 1e-7)
    return real

def make_bifurcation():
    gam_lo, gam_hi = -2.55, 0.55
    s_lo, s_hi = -3.6, 2.4
    ggrid = np.linspace(gam_lo, gam_hi, 420)
    curves_sym, curves_asym = [], []
    for g in ggrid:
        rs = chart_roots(float(g))
        for r in rs:
            if abs(r) < 1e-6:
                curves_sym.append((g, r))
            elif abs(r - 1) > 1e-6 and s_lo <= r <= s_hi:
                curves_asym.append((g, r))
    curves_sym = np.array(curves_sym)
    curves_asym = np.array(curves_asym)

    # exact rational anchors
    anchors = [(-1 / 4, 16 / 9), (-1 / 4, -16 / 5)]
    anchors2 = [(1.0, -1.0)]

    def config_from_root(gamma, s):
        x = np.array([1.0, -1.0 - gamma * s, s])
        return x

    def omega_of(gamma, x):
        pos = np.stack([x, np.zeros(3)], axis=1)
        vel = field([1.0, 1.0, gamma], pos)
        return lin_solve([1.0, 1.0, gamma], pos, vel)

    n_frames, fps = 96, 12
    us = np.linspace(0.0, 1.0, n_frames)
    # sweep 0.45 -> -2.45 with soft hold at both ends
    gammas = 0.45 - 2.9 * (np.sin(np.pi * (us - 0.5)) * 0.5 + 0.5) * 0 + \
        (0.45 - 2.9 * us)
    gammas[0] = 0.45
    thetas = np.zeros((n_frames, 3))
    frames = []

    for f in range(n_frames):
        g = float(gammas[f])
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.6, 6.15),
                                       gridspec_kw={"width_ratios": [1.25, 1]})
        fig.subplots_adjust(left=0.06, right=0.97, top=0.84, bottom=0.15, wspace=0.16)
        # ---- left: the chart equation
        ax1.set_facecolor(INK)
        if len(curves_asym):
            ax1.plot(curves_asym[:, 0], curves_asym[:, 1], "o", ms=2.2,
                     color=TL_GREEN, alpha=0.75, rasterized=True)
        ax1.plot(curves_sym[:, 0], curves_sym[:, 1], "o", ms=2.6,
                 color=TL_AMBER, alpha=0.95, rasterized=True)
        ax1.axhline(1.0, color=GRY, ls=":", lw=1.0, alpha=0.7)
        ax1.text(gam_hi - 0.03, 1.08, "collision s = 1 (excluded)", color=GRY,
                 fontsize=8.6, ha="right")
        for gg, lbl in [(-2.0, r"$\gamma=-2$ disc$=0$ (s10_col_count_neg2)"),
                        (-1.0, r"$\gamma=-1$ quad$\to$lin (s10_col_count_neg1)"),
                        (-1.25, r"$\gamma=-5/4$ PITCHFORK (triple root)")]:
            ax1.axvline(gg, color=TL_RED if gg != -1.25 else TL_AMBER,
                        ls="--", lw=1.0, alpha=0.55)
            ax1.text(gg + 0.03, s_hi - 0.25, lbl, color=GRY, fontsize=8.2,
                     rotation=90, va="top")
        ax1.axvline(-0.25, color=TL_GREEN, ls="--", lw=1.1, alpha=0.8)
        ax1.text(-0.22, s_lo + 0.15, r"$\gamma_0=-1/4$: two exact rational REs",
                 color=TL_GREEN, fontsize=8.4, rotation=90, va="bottom")
        for gg, ss in anchors:
            ax1.plot(gg, ss, "D", ms=8, color=GOLD_B, mec="white", mew=1.0, zorder=6)
            ax1.annotate(f"s = {ss:.4g}" if ss != int(ss) else f"s = {ss}",
                         (gg, ss), textcoords="offset points", xytext=(10, -12),
                         color=GOLD_B, fontsize=8.6)
        for gg, ss in anchors2:
            ax1.plot(gg, ss, "D", ms=8, color=PAPER, mec="white", mew=1.0, zorder=6)
        # sweep line + live roots
        rs = chart_roots(g)
        ax1.axvline(g, color=PAPER, lw=1.6, alpha=0.85)
        for r in rs:
            if s_lo <= r <= s_hi:
                col = TL_AMBER if abs(r) < 1e-6 else TL_GREEN
                ax1.plot(g, r, "o", ms=9, color=col, mec="white", mew=1.2, zorder=7)
        n_re = len([r for r in rs if abs(r - 1) > 1e-6 and s_lo <= r <= s_hi])
        ax1.set_xlim(gam_lo, gam_hi)
        ax1.set_ylim(s_lo, s_hi)
        ax1.grid(alpha=0.13, color=GRY)
        ax1.set_xlabel(r"$\gamma$  (circulation of vortex 3)", fontsize=10)
        ax1.set_ylabel("s = x$_3$/x$_1$", fontsize=10)
        ax1.set_title(r"chart equation  $N(s,\gamma)=s(s{-}1)\,\tilde M(s,\gamma)=0$",
                      fontsize=11.5)
        ax1.text(0.02, 0.03, rf"$\gamma = {g:+.3f}$   ·   collinear REs: {n_re}",
                 transform=ax1.transAxes, color=PAPER, fontsize=10.5,
                 bbox=dict(facecolor=INK_SOFT, edgecolor=GRY, boxstyle="round,pad=0.35"))
        # ---- right: rotating collinear configurations
        ax2.set_facecolor(INK)
        ax2.set_xlim(-1.7, 1.7)
        ax2.set_ylim(-1.7, 1.7)
        ax2.set_aspect("equal")
        ax2.axis("off")
        ax2.set_title("rigid rotation of each relative equilibrium", fontsize=11.5)
        k = 0
        for r in rs:
            if abs(r - 1) < 1e-6 or not (s_lo <= r <= s_hi):
                continue
            x = config_from_root(g, r)
            if np.max(np.abs(x)) < 1e-9:
                continue
            x = x / np.max(np.abs(x)) * 1.05
            om = omega_of(g, x)
            theta = om * (f / fps) * 7.0      # accelerated showcase rotation
            col, sn = np.cos(theta), np.sin(theta)
            R = np.array([[col, -sn], [sn, col]])
            posk = (R @ np.vstack([x, np.zeros(3)])).T   # 3x2: rows are points
            gamk = [1.0, 1.0, g]
            gmax = max(abs(v) for v in gamk) or 1.0
            for kk in range(3):
                rr = 0.085 + 0.06 * abs(gamk[kk]) / gmax
                circ = plt.Circle(posk[kk, :], rr, facecolor=VORT_COLORS[kk],
                                  ec="white", lw=1.0, alpha=0.95, zorder=6)
                ax2.add_patch(circ)
                orbit = plt.Circle((0, 0), float(np.hypot(posk[kk, 0], posk[kk, 1])),
                                   fill=False, color=GRY, ls=":", lw=0.7, alpha=0.4)
                ax2.add_patch(orbit)
            ax2.text(0, -1.52 + 0.13 * k,
                     rf"root s $= {r:+.4g}$   $\omega$ = {om:+.4f}",
                     color=PAPER if abs(r) > 1e-6 else TL_AMBER, fontsize=9,
                     ha="center")
            k += 1
        zone = ("γ > −5/4 · asymmetric branch born — up to THREE collinear REs"
                if g > -1.25 + 1e-9 else
                "γ = −5/4 · PITCHFORK — triple root s = 0 (s10_pitchfork_double)"
                if abs(g + 1.25) < 0.03 else
                "γ < −5/4 · ONE relative equilibrium — branch merged "
                "(s10_col_count_neg1 / neg2)")
        ax2.text(0, 1.56, zone, color=GOLD_B, fontsize=9.6, ha="center")
        fig.suptitle("TRIVORTEX §10.2/10.3 · collinear bifurcation across the "
                     "pitchfork γ = −5/4", color=GOLD_B, fontsize=13, y=0.955)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=110)
        plt.close(fig)
        buf.seek(0)
        frames.append(Image.open(buf).copy())
    save_gif(frames, os.path.join(OUT, "collinear_bifurcation.gif"), 1000 // fps)


if __name__ == "__main__":
    make_lyapunov()
    make_bifurcation()
    print("done")
