# -*- coding: utf-8 -*-
"""
TRIVORTEX — Orbital Animation Suite (v1.0.0)
======================================================================

Generates the four repository animations as GIF (universal playback) and
MP4 (compact H.264) into ``docs/animations/``:

    anim01_trivortex_ring        Theorem 3.1 breathing-ring choreography
    anim02_figure_eight          Chenciner–Montgomery free-fall figure eight
    anim03_lagrange_triangle     Lagrange (1772) rigidly rotating equilateral triangle
    anim04_laser_stationkeeping  Laser-damped libration at the photogravitational L4
                                 (TRX-01 + TRX-12 crossing)

Style follows the repository convention: navy background (#0A1730), gold /
cyan / rose body colors, English on-frame text (repository figure language),
bilingual prose lives in README.md / README_RU.md.

Run:
    python3 docs/animations/make_animations.py            # GIF + MP4
    python3 docs/animations/make_animations.py --gif-only # GIF only (no ffmpeg)
    python3 docs/animations/make_animations.py --preview  # also dump poster PNGs

Dependencies: numpy, scipy, matplotlib (>= 3.9); ffmpeg optional (MP4).
Every animation is a seamless closed loop built from the exact analytic
period of the underlying solution.
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
from matplotlib.patches import Circle

# ── Repository palette (docs/assets SVG convention) ────────────────────────
NAVY = "#0A1730"
NAVY2 = "#0E2145"
GOLD = "#D4AF37"
GOLD_L = "#F0D98C"
CYAN = "#59C2FF"
ROSE = "#FF7A9E"
INK = "#E9EEF8"
MUTED = "#8FA3C4"
BODY_COLORS = [GOLD, CYAN, ROSE]

HERE = os.path.dirname(os.path.abspath(__file__))
PREVIEW_DIR = os.environ.get("TRX_ANIM_PREVIEW", "/home/z/my-project/scripts/anim_preview")

FIGSIZE = (7.0, 7.0)
DPI = 100
FPS_GIF = 24
FRAMES = 144  # 6 s seamless loops at 24 fps
TRAIL_LEN = 56


def _style_axes(ax, lim: float) -> None:
    ax.set_facecolor(NAVY)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color(NAVY2)
        spine.set_linewidth(1.2)
    ax.grid(True, color=MUTED, alpha=0.10, linewidth=0.6)
    ax.set_axisbelow(True)


def _new_fig(title: str, subtitle: str):
    fig = plt.figure(figsize=FIGSIZE, dpi=DPI, facecolor=NAVY)
    ax = fig.add_axes([0.04, 0.06, 0.92, 0.80])
    fig.text(
        0.5, 0.955, title, ha="center", va="center", fontsize=14.5, fontweight="bold", color=GOLD
    )
    fig.text(0.5, 0.912, subtitle, ha="center", va="center", fontsize=8.5, color=MUTED)
    fig.text(
        0.5,
        0.014,
        "TRIVORTEX Research Program · v1.0.0 · three-body choreographies",
        ha="center",
        va="center",
        fontsize=7,
        color=MUTED,
    )
    return fig, ax


def _trail_points(hist, color):
    """Build color list with fading alpha for a trail history array."""
    n = len(hist)
    return [(*matplotlib.colors.to_rgb(color), a) for a in np.linspace(0.03, 0.5, n)]


# ═══════════════════════════════════════════════════════════════════════════
# Animation 1 — TRIVORTEX breathing ring (Theorem 3.1)
# ═══════════════════════════════════════════════════════════════════════════
def anim01_trivortex_ring(out_prefix: str, preview: bool):
    """r_k(t) = sqrt(C_Ch) (1 + eps cos(Omega t + 2 pi k / 3)),
    Omega = (2 pi / T) exp(C_Ch / pi); C_Ch = 1 => Omega = exp(1/pi)."""
    C_Ch = 1.0
    eps = 0.14
    Omega = np.exp(C_Ch / np.pi)  # vortex-model angular frequency
    T_loop = 2.0 * np.pi / Omega  # breathing period => seamless loop
    R = np.sqrt(C_Ch)

    theta = 2.0 * np.pi * np.arange(3) / 3.0

    def positions(t):
        r = R * (1.0 + eps * np.cos(Omega * t + theta))
        return np.stack([r * np.cos(theta), r * np.sin(theta)], axis=1)

    fig, ax = _new_fig(
        "TRIVORTEX · Theorem 3.1 — Breathing-Ring Choreography",
        r"$r_k(t)=\sqrt{C_{\mathrm{Ch}}}\,(1+\varepsilon\cos(\omega t+2\pi k/3)),"
        r"\ \ \omega=(2\pi/T)\,e^{C_{\mathrm{Ch}}/\pi},\ C_{\mathrm{Ch}}=1$",
    )

    _style_axes(ax, 1.45)
    for rr in (R * (1 - eps), R, R * (1 + eps)):
        ax.add_patch(
            Circle(
                (0, 0),
                rr,
                fill=False,
                edgecolor=MUTED,
                linestyle=":",
                linewidth=0.8,
                alpha=0.5,
                zorder=1,
            )
        )
    ax.add_patch(Circle((0, 0), 0.035, color=GOLD_L, alpha=0.9, zorder=3))

    dots = [ax.add_patch(Circle((0, 0), 0.055, color=c, zorder=4)) for c in BODY_COLORS]
    hists = [np.empty((0, 2)) for _ in range(3)]
    trail_artists = []

    t_vals = np.linspace(0.0, T_loop, FRAMES, endpoint=False)

    def update(i):
        nonlocal trail_artists
        for artist in trail_artists:
            artist.remove()
        trail_artists = []
        pos = positions(t_vals[i])
        for k in range(3):
            hists[k] = np.vstack([hists[k], pos[k]])[-TRAIL_LEN:]
            dots[k].center = pos[k]
            trail_artists.append(
                ax.scatter(
                    hists[k][:, 0],
                    hists[k][:, 1],
                    s=3.0,
                    c=_trail_points(hists[k], BODY_COLORS[k]),
                    edgecolors="none",
                    zorder=2,
                )
            )
        return []

    anim = FuncAnimation(
        fig, update, frames=FRAMES, interval=1000 / FPS_GIF, blit=False, repeat=True
    )
    _save(anim, out_prefix, preview, fig, poster_positions=positions(0.0))
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════
# Animation 2 — Chenciner–Montgomery figure eight
# ═══════════════════════════════════════════════════════════════════════════
def anim02_figure_eight(out_prefix: str, preview: bool):
    """Free-fall figure-eight choreography: equal masses chase each other
    along one curve; integrated with DOP853 at rtol = atol = 1e-12."""
    x1 = np.array([0.97000436, -0.24308753])
    v3 = np.array([-0.93240737, -0.86473146])
    y0 = np.array(
        [
            x1[0],
            x1[1],
            -x1[0],
            -x1[1],
            0.0,
            0.0,
            -v3[0] / 2,
            -v3[1] / 2,
            -v3[0] / 2,
            -v3[1] / 2,
            v3[0],
            v3[1],
        ]
    )
    T_period = 6.324090548

    def rhs(_t, y):
        pos = y[:6].reshape(3, 2)
        vel = y[6:].reshape(3, 2)
        acc = np.zeros((3, 2))
        for i in range(3):
            for j in range(3):
                if i != j:
                    d = pos[j] - pos[i]
                    acc[i] += d / (np.linalg.norm(d) ** 3 + 1e-14)
        return np.concatenate([vel.ravel(), acc.ravel()])

    sol = solve_ivp(
        rhs,
        (0.0, T_period),
        y0,
        method="DOP853",
        rtol=1e-12,
        atol=1e-12,
        dense_output=True,
        max_step=0.01,
    )

    fig, ax = _new_fig(
        "Figure-Eight Choreography — Chenciner & Montgomery (2000)",
        "equal masses in free fall chase each other along one closed curve ·"
        " DOP853, rtol = atol = 1e-12",
    )
    _style_axes(ax, 1.35)
    t_ghost = np.linspace(0.0, T_period, 1200)
    ghost = sol.sol(t_ghost)[:6].reshape(3, 2, -1)
    for k in range(3):
        ax.plot(ghost[k, 0], ghost[k, 1], color=MUTED, linewidth=0.7, alpha=0.30, zorder=1)

    dots = [ax.add_patch(Circle((0, 0), 0.06, color=c, zorder=4)) for c in BODY_COLORS]
    hists = [np.empty((0, 2)) for _ in range(3)]
    trail_artists = []

    t_vals = np.linspace(0.0, T_period, FRAMES, endpoint=False)

    def update(i):
        nonlocal trail_artists
        for artist in trail_artists:
            artist.remove()
        trail_artists = []
        pos = sol.sol(t_vals[i])[:6].reshape(3, 2)
        for k in range(3):
            hists[k] = np.vstack([hists[k], pos[k]])[-TRAIL_LEN:]
            dots[k].center = pos[k]
            trail_artists.append(
                ax.scatter(
                    hists[k][:, 0],
                    hists[k][:, 1],
                    s=3.0,
                    c=_trail_points(hists[k], BODY_COLORS[k]),
                    edgecolors="none",
                    zorder=2,
                )
            )
        return []

    anim = FuncAnimation(
        fig, update, frames=FRAMES, interval=1000 / FPS_GIF, blit=False, repeat=True
    )
    p0 = sol.sol(0.0)[:6].reshape(3, 2)
    _save(anim, out_prefix, preview, fig, poster_positions=p0)
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════
# Animation 3 — Lagrange rigidly rotating equilateral triangle
# ═══════════════════════════════════════════════════════════════════════════
def anim03_lagrange_triangle(out_prefix: str, preview: bool):
    """Lagrange's 1772 equilateral solution: three equal masses rotate
    rigidly, omega = sqrt(3 G m / a^3); here G = m = a = 1."""
    a = 1.0
    omega = np.sqrt(3.0 / a**3)
    r0 = a / np.sqrt(3.0)
    phi0 = np.pi / 2.0 + 2.0 * np.pi * np.arange(3) / 3.0
    T_loop = 2.0 * np.pi / omega

    fig, ax = _new_fig(
        "Lagrange Equilateral Solution — Rigid Rotation (1772)",
        r"three equal masses, side $a=1$, $\omega=\sqrt{3/a^{3}}$ — the celestial"
        r" twin of the TRIVORTEX vortex triangle",
    )
    _style_axes(ax, 0.95)
    ax.add_patch(
        Circle(
            (0, 0),
            r0,
            fill=False,
            edgecolor=MUTED,
            linestyle=":",
            linewidth=0.8,
            alpha=0.5,
            zorder=1,
        )
    )
    ax.add_patch(Circle((0, 0), 0.03, color=GOLD_L, alpha=0.9, zorder=3))

    dots = [ax.add_patch(Circle((0, 0), 0.05, color=c, zorder=4)) for c in BODY_COLORS]
    hists = [np.empty((0, 2)) for _ in range(3)]
    side_lines = [
        ax.plot([], [], color=GOLD, alpha=0.35, linewidth=0.9, zorder=2)[0] for _ in range(3)
    ]
    trail_artists = []

    t_vals = np.linspace(0.0, T_loop, FRAMES, endpoint=False)

    def update(i):
        nonlocal trail_artists
        for artist in trail_artists:
            artist.remove()
        trail_artists = []
        ph = phi0 + omega * t_vals[i]
        pos = np.stack([r0 * np.cos(ph), r0 * np.sin(ph)], axis=1)
        for k in range(3):
            hists[k] = np.vstack([hists[k], pos[k]])[-TRAIL_LEN:]
            dots[k].center = pos[k]
            trail_artists.append(
                ax.scatter(
                    hists[k][:, 0],
                    hists[k][:, 1],
                    s=2.5,
                    c=_trail_points(hists[k], BODY_COLORS[k]),
                    edgecolors="none",
                    zorder=2,
                )
            )
        for j in range(3):
            side_lines[j].set_data(
                [pos[j][0], pos[(j + 1) % 3][0]], [pos[j][1], pos[(j + 1) % 3][1]]
            )
        return []

    anim = FuncAnimation(
        fig, update, frames=FRAMES, interval=1000 / FPS_GIF, blit=False, repeat=True
    )
    p0 = np.stack([r0 * np.cos(phi0), r0 * np.sin(phi0)], axis=1)
    _save(anim, out_prefix, preview, fig, poster_positions=p0)
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════
# Animation 4 — laser-damped libration at the photogravitational L4
# ═══════════════════════════════════════════════════════════════════════════
def anim04_laser_stationkeeping(out_prefix: str, preview: bool):
    """Photogravitational CR3BP (Earth–Moon mu, beta = 0.05) in the rotating
    frame. Free sail librates around the displaced L4 star; the laser-guided
    sail (PD station-keeping, TRX-12 style) spirals into a hover at L4 star.
    The beam line from the radiating primary is drawn while thrust is on."""
    mu = 0.0121505856
    beta = 0.05
    kp, kd = 4.0, 4.0  # TRX-12 operating-point PD gains
    a_max = 0.244  # photon-thrust cap, 2P/(c m) dimensionless
    T_run = 40.0

    p1 = np.array([-mu, 0.0])
    p2 = np.array([1.0 - mu, 0.0])

    def grad_Omega(x, y):
        r1v = np.array([x, y]) - p1
        r2v = np.array([x, y]) - p2
        r1 = np.linalg.norm(r1v)
        r2 = np.linalg.norm(r2v)
        n1 = (1.0 - beta) * (1.0 - mu)
        n2 = mu
        dOx = x - n1 * r1v[0] / r1**3 - n2 * r2v[0] / r2**3
        dOy = y - n1 * r1v[1] / r1**3 - n2 * r2v[1] / r2**3
        return np.array([dOx, dOy])

    # displaced L4 star: 2-D Newton from the classical L4
    xs = np.array([0.5 - mu, np.sqrt(3.0) / 2.0])
    for _ in range(80):
        g = grad_Omega(xs[0], xs[1])
        h = 1e-8
        J = np.column_stack(
            [
                (grad_Omega(xs[0] + h, xs[1]) - g) / h,
                (grad_Omega(xs[0], xs[1] + h) - g) / h,
            ]
        )
        xs = xs - np.linalg.solve(J, g)

    def rhs(_t, y, controlled: bool):
        pos = np.array([y[0], y[1]])
        vel = np.array([y[2], y[3]])
        g = grad_Omega(pos[0], pos[1])
        acc = np.array([2.0 * vel[1], -2.0 * vel[0]]) + g
        if controlled:
            u = -kp * (pos - xs) - kd * vel
            nrm = np.linalg.norm(u)
            if nrm > a_max:  # photon-thrust saturation
                u *= a_max / nrm
            acc = acc + u
        return [vel[0], vel[1], acc[0], acc[1]]

    y0 = np.array([xs[0] + 0.012, xs[1] + 0.008, 0.0, 0.0])
    t_eval = np.linspace(0.0, T_run, 4 * FRAMES, endpoint=False)
    free = solve_ivp(
        rhs,
        (0.0, T_run),
        y0,
        args=(False,),
        method="DOP853",
        rtol=1e-11,
        atol=1e-11,
        t_eval=t_eval,
        max_step=0.05,
    )
    ctrl = solve_ivp(
        rhs,
        (0.0, T_run),
        y0,
        args=(True,),
        method="DOP853",
        rtol=1e-11,
        atol=1e-11,
        t_eval=t_eval,
        max_step=0.05,
    )

    fig, ax = _new_fig(
        "Laser Station-Keeping at the Photogravitational L4",
        r"Earth–Moon $\mu$, radiation $\beta=0.05$ · PD beam-steering (kp = kd = 4,"
        r" TRX-12) · free sail librates, guided sail hovers at $L_4^{\ast}$",
    )

    _style_axes(ax, 1.18)
    ax.scatter([p1[0]], [p1[1]], s=260, color=GOLD, edgecolors=GOLD_L, linewidth=1.0, zorder=4)
    ax.scatter([p2[0]], [p2[1]], s=90, color=CYAN, edgecolors=INK, linewidth=0.8, zorder=4)
    ax.text(p1[0], p1[1] - 0.055, "radiating primary", color=GOLD_L, fontsize=7.5, ha="center")
    ax.text(p2[0], p2[1] - 0.05, "secondary", color=CYAN, fontsize=7.5, ha="center")
    ax.scatter(
        [0.5 - mu],
        [np.sqrt(3) / 2],
        s=130,
        facecolors="none",
        edgecolors=MUTED,
        linewidths=1.2,
        zorder=3,
    )
    ax.text(0.5 - mu, np.sqrt(3) / 2 + 0.035, r"$L_4$", color=MUTED, fontsize=9, ha="center")
    ax.scatter([xs[0]], [xs[1]], marker="x", s=70, color=GOLD_L, linewidths=1.6, zorder=3)
    ax.text(xs[0] + 0.015, xs[1] + 0.028, r"$L_4^{\ast}$", color=GOLD_L, fontsize=9, ha="left")

    (sail_free,) = ax.plot([], [], "o", color=ROSE, markersize=6, zorder=5)
    (sail_ctrl,) = ax.plot([], [], "o", color=CYAN, markersize=6, zorder=5)
    (beam,) = ax.plot([], [], color=GOLD_L, alpha=0.85, linewidth=1.4, zorder=3)
    (trail_free,) = ax.plot([], [], color=ROSE, alpha=0.45, linewidth=0.9, zorder=2)
    (trail_ctrl,) = ax.plot([], [], color=CYAN, alpha=0.45, linewidth=0.9, zorder=2)
    txt = ax.text(0.03, -1.13, "", color=INK, fontsize=8.5)

    step = 4
    free_path = free.y[:2, ::step].T
    ctrl_path = ctrl.y[:2, ::step].T
    ctrl_state = ctrl.y[:, ::step].T
    t_frames = t_eval[::step]

    def update(i):
        trail_free.set_data(free_path[: i + 1, 0], free_path[: i + 1, 1])
        trail_ctrl.set_data(ctrl_path[: i + 1, 0], ctrl_path[: i + 1, 1])
        sail_free.set_data([free_path[i, 0]], [free_path[i, 1]])
        sail_ctrl.set_data([ctrl_path[i, 0]], [ctrl_path[i, 1]])
        pos = ctrl_state[i, :2]
        vel = ctrl_state[i, 2:]
        u = -kp * (pos - xs) - kd * vel
        th = min(float(np.linalg.norm(u)), a_max)
        if th > 1e-3:
            beam.set_data([p1[0], pos[0]], [p1[1], pos[1]])
        else:
            beam.set_data([], [])
        txt.set_text(f"t = {t_frames[i]:6.2f}   ·   laser thrust = {th:8.5f}")
        return []

    anim = FuncAnimation(
        fig, update, frames=FRAMES, interval=1000 / FPS_GIF, blit=False, repeat=True
    )
    _save(
        anim,
        out_prefix,
        preview,
        fig,
        poster_positions=None,
        poster_extra=(free_path, ctrl_path, xs, p1, p2),
    )
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════
# Saving
# ═══════════════════════════════════════════════════════════════════════════
def _save(anim, out_prefix: str, preview: bool, fig, poster_positions, poster_extra=None) -> None:
    gif_path = out_prefix + ".gif"
    anim.save(gif_path, writer=PillowWriter(fps=FPS_GIF))
    size_mb = os.path.getsize(gif_path) / (1024 * 1024)
    print(f"  GIF  {os.path.basename(gif_path):44s} {size_mb:6.2f} MB")

    try:
        mp4_path = out_prefix + ".mp4"
        anim.save(mp4_path, writer=FFMpegWriter(fps=FPS_GIF, bitrate=1800, codec="h264"))
        size_mb = os.path.getsize(mp4_path) / (1024 * 1024)
        print(f"  MP4  {os.path.basename(mp4_path):44s} {size_mb:6.2f} MB")
    except Exception as exc:  # ffmpeg missing — GIF alone is acceptable
        print(f"  MP4  skipped ({exc})")

    if preview:
        os.makedirs(PREVIEW_DIR, exist_ok=True)
        stem = os.path.basename(out_prefix)
        pv_path = os.path.join(PREVIEW_DIR, stem + "_poster.png")
        ax0 = fig.axes[0]
        if poster_positions is not None:
            for k, pos in enumerate(poster_positions):
                ax0.scatter([pos[0]], [pos[1]], s=48, color=BODY_COLORS[k], zorder=6)
        if poster_extra is not None:
            free_path, ctrl_path, xs, p1, p2 = poster_extra
            ax0.plot(free_path[:, 0], free_path[:, 1], color=ROSE, alpha=0.6, linewidth=0.9)
            ax0.plot(ctrl_path[:, 0], ctrl_path[:, 1], color=CYAN, alpha=0.6, linewidth=0.9)
            ax0.scatter([p1[0]], [p1[1]], s=260, color=GOLD)
            ax0.scatter([p2[0]], [p2[1]], s=90, color=CYAN)
            ax0.scatter([xs[0]], [xs[1]], marker="x", s=70, color=GOLD_L)
        fig.savefig(pv_path, facecolor=NAVY, dpi=DPI)
        print(f"  POST {os.path.basename(pv_path)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="TRIVORTEX animation suite")
    parser.add_argument(
        "--preview", action="store_true", help="also write poster PNGs for visual inspection"
    )
    parser.add_argument(
        "--outdir", default=HERE, help="output directory (default: script directory)"
    )
    args = parser.parse_args()

    jobs = [
        ("anim01_trivortex_ring", anim01_trivortex_ring),
        ("anim02_figure_eight", anim02_figure_eight),
        ("anim03_lagrange_triangle", anim03_lagrange_triangle),
        ("anim04_laser_stationkeeping", anim04_laser_stationkeeping),
    ]
    print("TRIVORTEX animation suite — 4 choreographies, " f"{FRAMES} frames @ {FPS_GIF} fps")
    for name, fn in jobs:
        prefix = os.path.join(args.outdir, name)
        print(f"[{name}]")
        fn(prefix, args.preview)
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
