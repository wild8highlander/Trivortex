#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — HUD: палитра AURORA, баннер ACLL, динамический
прогресс-бар, системный монитор.

Перенос идей AB-CLOUD AURORA Edition на Python:
  * truecolor ANSI (256/16 — деградация по TERM/COLORTERM), чистый текст в пайпах;
  * однострочный прогресс-бар: репейнт через \\r на STDERR, ширина от
    displaysize c клампом 30–100, EMA-оценка ETA, спиннер;
  * порядок усечения хвоста справа налево: timestamp → up → ETA → статус → тег;
  * монитор: cpu · ram · temp · io-lat из /proc (psutil — опционально).

Любой вывод в отчёты идёт через color_off() / с COLOR=False — чистый текст.
"""

from __future__ import annotations

import math
import os
import shutil
import sys
import threading
import time

# ═══════════════════════════════════════════════════════════════════════════
# 1. Палитра AURORA (адаптация под бренд ACLL: лёд + золото)
# ═══════════════════════════════════════════════════════════════════════════
ICE = (125, 211, 252)  # ледяной голубой — заголовки, прогресс
SKY = (91, 141, 255)  # синь — вторичный
GOLD = (232, 199, 102)  # золото — акценты, ETA, WARN
GRN = (52, 211, 153)  # полярная зелень — PASS
RED = (255, 95, 110)  # алый — FAIL, плашка N=8
VIO = (167, 139, 250)  # фиолетовое сияние — категории, 4D
GRY = (139, 152, 178)  # серый — вторичный текст
WHT = (235, 240, 255)  # белый — основной текст
ORG = (255, 159, 90)  # оранжевый — предупреждения

PALETTE_RGB = dict(
    ice=ICE, sky=SKY, gold=GOLD, grn=GRN, red=RED, vio=VIO, gry=GRY, wht=WHT, org=ORG
)

# 16-цветные аналоги (деградация)
PALETTE_16 = dict(ice=6, sky=4, gold=3, grn=2, red=1, vio=5, gry=7, wht=7, org=3)

_COLOR_MODE = "truecolor"  # truecolor | 256 | 16 | none
COLOR = True  # цветовой шлюз: отчёты всегда получают чистый текст


def detect_color_mode(stream=None) -> str:
    """Автоопределение возможностей терминала."""
    global _COLOR_MODE
    if os.environ.get("NO_COLOR"):
        _COLOR_MODE = "none"
        return _COLOR_MODE
    stream = stream or sys.stderr
    if not hasattr(stream, "isatty") or not stream.isatty():
        _COLOR_MODE = "none"
        return _COLOR_MODE
    term = os.environ.get("TERM", "")
    colorterm = os.environ.get("COLORTERM", "").lower()
    if colorterm in ("truecolor", "24bit") or "truecolor" in colorterm:
        _COLOR_MODE = "truecolor"
    elif "256color" in term:
        _COLOR_MODE = "256"
    elif term:
        _COLOR_MODE = "16"
    else:
        _COLOR_MODE = "none"
    return _COLOR_MODE


def color_on() -> None:
    """Handle color on."""
    global COLOR
    COLOR = True


def color_off() -> None:
    """Handle color off."""
    global COLOR
    COLOR = False


def _rgb_to_256(r: int, g: int, b: int) -> int:
    """Ближший цвет xterm-256."""
    best, best_d = 0, 1 << 30
    for i in range(256):
        if i < 16:
            rr, gg, bb = 0, 0, 0
        elif i < 232:
            n = i - 16
            rr = (n // 36) * 51
            gg = ((n // 6) % 6) * 51
            bb = (n % 6) * 51
        else:
            v = (i - 232) * 10 + 8
            rr = gg = bb = v
        d = (r - rr) ** 2 + (g - gg) ** 2 + (b - bb) ** 2
        if d < best_d:
            best, best_d = i, d
    return best


def _p3(rgb: tuple) -> str:
    """Do p3 for rgb and return the result."""
    if not COLOR or _COLOR_MODE == "none":
        return ""
    if _COLOR_MODE == "truecolor":
        return f"\x1b[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
    if _COLOR_MODE == "256":
        return f"\x1b[38;5;{_rgb_to_256(*rgb)}m"
    return ""


def _c(rgb: tuple, bold: bool = False) -> str:
    """Do c for rgb, bold and return the result."""
    if not COLOR or _COLOR_MODE == "none":
        return ""
    if _COLOR_MODE == "16":
        return f"\x1b[1m\x1b[3{rgb and 0}m" if False else f"\x1b[{';'.join(['1'] if bold else [])}m"
    s = _p3(rgb)
    return f"\x1b[1m{s}" if bold else s


RESET = "\x1b[0m" if COLOR else ""


def _col(rgb, bold=False):
    """Общая обёртка: код цвета или пустая строка."""
    if not COLOR or _COLOR_MODE == "none":
        return ""
    if _COLOR_MODE == "16":
        return ""
    s = _p3(rgb)
    if bold and s:
        s = "\x1b[1m" + s
    return s


def cyn(bold=False):
    """Colorize text cyan (AURORA palette)."""
    return _col(ICE, bold)


def grn(bold=False):
    """Colorize text green (AURORA palette)."""
    return _col(GRN, bold)


def red(bold=False):
    """Colorize text red (AURORA palette)."""
    return _col(RED, bold)


def ylw(bold=False):
    """Do ylw for bold and return the result."""
    return _col(GOLD, bold)


def mag(bold=False):
    """Do mag for bold and return the result."""
    return _col(VIO, bold)


def blu(bold=False):
    """Do blu for bold and return the result."""
    return _col(SKY, bold)


def gry(bold=False):
    """Do gry for bold and return the result."""
    return _col(GRY, bold)


def wht(bold=False):
    """Do wht for bold and return the result."""
    return _col(WHT, bold)


def org(bold=False):
    """Do org for bold and return the result."""
    return _col(ORG, bold)


def gold(bold=False):
    """Do gold for bold and return the result."""
    return _col(GOLD, bold)


def reset() -> str:
    """Handle reset."""
    return "\x1b[0m" if (COLOR and _COLOR_MODE != "none") else ""


def colorize(text: str, rgb: tuple, bold: bool = False) -> str:
    """Wrap text with an ANSI truecolor escape for the given RGB."""
    code = _col(rgb, bold)
    if not code:
        return text
    return f"{code}{text}{reset()}"


def gradient_text(text: str, rgb_a: tuple, rgb_b: tuple) -> str:
    """Позначная градиентная интерполяция цвета (баннер)."""
    if not COLOR or _COLOR_MODE == "none":
        return text
    n = max(len(text) - 1, 1)
    out = []
    for i, ch in enumerate(text):
        t = i / n
        rgb = tuple(int(a + (b - a) * t) for a, b in zip(rgb_a, rgb_b))
        out.append(_p3(rgb) + ch)
    out.append(reset())
    return "".join(out)


# ═══════════════════════════════════════════════════════════════════════════
# 2. Видимая ширина строки (пропуск ANSI-кодов)
# ═══════════════════════════════════════════════════════════════════════════
_ANSI_RE = None


def _strip_ansi(s: str) -> str:
    """Do strip ansi for s and return the result."""
    global _ANSI_RE
    if _ANSI_RE is None:
        import re

        _ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
    return _ANSI_RE.sub("", s)


def visible_width(s: str) -> int:
    """Do visible width for s and return the result."""
    return len(_strip_ansi(s))


def pad_to(s: str, width: int) -> str:
    """Do pad to for s, width and return the result."""
    vis = visible_width(s)
    if vis >= width:
        return s
    return s + " " * (width - vis)


def trunc_to(s: str, width: int) -> str:
    """Do trunc to for s, width and return the result."""
    if visible_width(s) <= width:
        return s
    return _strip_ansi(s)[: max(width - 1, 0)] + "…"


# ═══════════════════════════════════════════════════════════════════════════
# 3. Орнаменты, рамки, баннеры
# ═══════════════════════════════════════════════════════════════════════════
def orn(width: int = 72) -> str:
    """Орнаментальная линия ✦—❄—✦."""
    if width < 8:
        return "─" * width
    seg = "─" * ((width - 4) // 2)
    return f"{seg}✦──❄──✦{seg}"


def hr(char: str = "─", width: int = 72) -> str:
    """Do hr for char, width and return the result."""
    return char * width


def box(lines: list[str], title: str = "", color: tuple = ICE, width: int = 74) -> list[str]:
    """Рамочный бокс ╔═╗ вокруг уже готовых (может быть раскрашенных) строк."""
    w = width - 2
    top = (
        "╔" + ("═" * (w + 2)) + "╗"
        if not title
        else "╔═" + f" {title} " + "═" * max(w - len(title) - 1, 0) + "╗"
    )
    out = [colorize(top, color, True)]
    for ln in lines:
        for piece in (ln if isinstance(ln, list) else [ln]):
            vis = visible_width(piece)
            pad = " " * max(w - vis + 1, 0)
            out.append("║ " + piece + pad + "║")
    out.append(colorize("╚" + "═" * (w + 2) + "╝", color, True))
    return out


BANNER_ACLL = [
    " █████╗ ██╗      █████╗ ██╗     ██╗      ██████╗",
    "██╔══██╗██║     ██╔══██╗██║     ██║     ██╔════╝",
    "███████║██║     ███████║██║     ██║     ██║     ",
    "██╔══██║██║     ██╔══██║██║     ██║     ██║     ",
    "██║  ██║███████╗██║  ██║███████╗███████╗╚██████╗",
    "╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝",
]

BANNER_PLAIN = [
    "+=====================================================+",
    "|   A C L L   ·   T R I V O R T E X   M A S T E R    |",
    "|            лаборатория N тел · v{version}              |",
    "+=====================================================+",
]


def banner(version: str = "2.0.0", subtitle: str = "") -> list[str]:
    """Баннер ACLL: truecolor-градиент лёд→золото, при Non-TTY — плоский."""
    if _COLOR_MODE == "none" or not COLOR:
        lines = [ln.format(version=version) for ln in BANNER_PLAIN]
    else:
        lines = [gradient_text(ln, ICE, GOLD) for ln in BANNER_ACLL]
    title = f"T R I V O R T E X   M A S T E R   ·   v{version}   ·   AURORA EDITION"
    lines.append(colorize(title, GOLD, True) if COLOR else title)
    sub = subtitle or "лаборатория N тел · траектории · 2D/3D/4D · отчёты 7 форматов"
    lines.append(colorize(sub, GRY) if COLOR else sub)
    return lines


def print_banner(version: str = "2.0.0", subtitle: str = "", stream=None) -> None:
    """Do print banner for version, subtitle, stream and return the result."""
    stream = stream or sys.stdout
    for ln in banner(version, subtitle):
        stream.write(ln + "\n")
    stream.write(colorize(orn(74), SKY) + "\n" if COLOR else orn(74) + "\n")


def verdict_icon(ok: bool) -> str:
    """Return the verdict icon for a status word."""
    return colorize("✓", GRN, True) if ok else colorize("✗", RED, True)


def warn_plate(text: str, width: int = 74) -> str:
    """Красная плашка (N=8 вне физической вселенной и т.п.)."""
    edge = colorize("═" * (width - 2), RED, True)
    body = colorize(f" ⚠ {text} ", RED, True)
    return f"╔{edge}╗\n║{body:<72}║\n╚{edge}╝"


def kv(key: str, value: str, key_w: int = 22) -> str:
    """Return a key-value HUD line in the AURORA palette."""
    return f"  {colorize(pad_to(key, key_w), GRY)} {colorize(value, WHT)}"


# ═══════════════════════════════════════════════════════════════════════════
# 4. Спиннер
# ═══════════════════════════════════════════════════════════════════════════
SPIN_FRAMES = "◐◓◑◒"
SPIN_BRAILLE = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"


class Spinner:
    """Символьный спиннер для неопределённых ожиданий."""

    def __init__(self, label: str = "", stream=None, braille: bool = True):
        """Do Spinner.  init for label, stream, braille and return the result."""
        self.label = label
        self.stream = stream or sys.stderr
        self.frames = SPIN_BRAILLE if braille else SPIN_FRAMES
        self._i = 0
        self._t0 = time.time()
        self._active = False

    def frame(self, elapsed: float | None = None) -> str:
        """Do Spinner.frame for elapsed and return the result."""
        ch = self.frames[self._i % len(self.frames)]
        self._i += 1
        el = elapsed if elapsed is not None else time.time() - self._t0
        s = f"{colorize(ch, ICE, True)} {self.label} … {el:5.1f} с"
        return s if COLOR else f"[{ch}] {self.label} … {el:5.1f} с"

    def step(self) -> None:
        """Handle Spinner.step."""
        if _COLOR_MODE == "none" or not self.stream.isatty():
            return
        self.stream.write("\r" + pad_to(self.frame(), 78))
        self.stream.flush()


# ═══════════════════════════════════════════════════════════════════════════
# 5. Системный монитор (cpu · ram · temp · io-lat)
# ═══════════════════════════════════════════════════════════════════════════
class Monitor:
    """Лёгкий системный монитор: /proc напрямую, psutil — опционально."""

    def __init__(self):
        """Handle Monitor.  init."""
        self._cpu_prev = None
        self._psutil = None
        try:
            import psutil  # noqa: F401

            self._psutil = psutil
        except ImportError:
            pass
        self.io_lat_us = None
        self._probe_io_latency()

    # ── cpu из /proc/stat ──
    @staticmethod
    def _read_proc_stat() -> tuple[int, int] | None:
        """Handle Monitor. read proc stat."""
        try:
            with open("/proc/stat", encoding="utf-8") as fh:
                parts = fh.readline().split()[1:]
            vals = [int(x) for x in parts]
            idle = vals[3] + (vals[4] if len(vals) > 4 else 0)
            return sum(vals), idle
        except (OSError, ValueError, IndexError):
            return None

    def cpu_pct(self) -> float:
        """Handle Monitor.cpu pct."""
        if self._psutil is not None:
            try:
                return self._psutil.cpu_percent(interval=None)
            except Exception:
                pass
        cur = self._read_proc_stat()
        if cur is None:
            return float("nan")
        if self._cpu_prev is None:
            self._cpu_prev = cur
            return 0.0
        dt = cur[0] - self._cpu_prev[0]
        di = cur[1] - self._cpu_prev[1]
        self._cpu_prev = cur
        if dt <= 0:
            return 0.0
        return max(0.0, min(100.0, 100.0 * (dt - di) / dt))

    # ── ram из /proc/meminfo ──
    @staticmethod
    def _read_meminfo() -> tuple[float, float]:
        """Handle Monitor. read meminfo."""
        try:
            info = {}
            with open("/proc/meminfo", encoding="utf-8") as fh:
                for line in fh:
                    k, _, v = line.partition(":")
                    info[k.strip()] = float(v.split()[0])  # кБ
            total = info.get("MemTotal", 0.0)
            avail = info.get("MemAvailable", info.get("MemFree", 0.0))
            return total / 1e6, avail / 1e6  # ГБ
        except (OSError, ValueError, IndexError):
            return 0.0, 0.0

    def ram(self) -> tuple[float, float]:
        """Handle Monitor.ram."""
        if self._psutil is not None:
            try:
                vm = self._psutil.virtual_memory()
                return vm.total / 1e9, vm.available / 1e9
            except Exception:
                pass
        return self._read_meminfo()

    # ── температура ──
    @staticmethod
    def temp_c() -> float:
        """Handle Monitor.temp c."""
        for zone in sorted(_list_dir("/sys/class/thermal")):
            try:
                with open(f"/sys/class/thermal/{zone}/temp") as fh:
                    return int(fh.read().strip()) / 1000.0
            except (OSError, ValueError):
                continue
        for hw in sorted(_list_dir("/sys/class/hwmon")):
            try:
                with open(f"/sys/class/hwmon/{hw}/temp1_input") as fh:
                    return int(fh.read().strip()) / 1000.0
            except (OSError, ValueError):
                continue
        return float("nan")

    # ── латентность пустого I/O-цикла ──
    def _probe_io_latency(self) -> None:
        """Handle Monitor. probe io latency."""
        import tempfile

        try:
            t0 = time.perf_counter()
            with tempfile.NamedTemporaryFile(mode="w+", delete=True) as fh:
                fh.write("x")
                fh.flush()
                fh.seek(0)
                fh.read()
            self.io_lat_us = (time.perf_counter() - t0) * 1e6
        except OSError:
            self.io_lat_us = None

    # ── строка для встраивания в бар ──
    def inline(self) -> str:
        """Handle Monitor.inline."""
        cpu = self.cpu_pct()
        tot, avail = self.ram()
        parts = [f"cpu {cpu:4.0f}%"]
        if tot > 0:
            parts.append(f"ram {tot - avail:.1f}/{tot:.1f}G")
        t = self.temp_c()
        if not math.isnan(t):
            parts.append(f"{t:.1f}°C")
        if self.io_lat_us is not None:
            parts.append(f"io {self.io_lat_us:.0f}мкс")
        return " · ".join(parts)


def _list_dir(path: str) -> list[str]:
    """Do list dir for path and return the result."""
    try:
        return [d for d in os.listdir(path) if d.startswith(("thermal_zone", "hwmon"))]
    except OSError:
        return []


# ═══════════════════════════════════════════════════════════════════════════
# 6. Прогресс-бар — одна строка, динамический, EMA-ETA
# ═══════════════════════════════════════════════════════════════════════════
def _term_width() -> int:
    """Handle term width."""
    try:
        w = shutil.get_terminal_size((80, 24)).columns
    except OSError:
        w = 80
    return max(30, min(w - 2, 100))


class ProgressBar:
    """
    Однострочный динамический прогресс-бар (STDERR, репейнт через \\r).

        ◐ Label ▰▰▰▰▱▱▱▱ 42,1% · статус · cpu 87% · ETA 00:01:23 · up 00:00:12

    * EMA по скорости прогресса — устойчив к неравномерным фазам расчёта;
    * при Non-TTY бары гаснут, каждые 10% печатается milestone-строка;
    * thread-safe: один фоновый поток-насос на все обновления.
    """

    def __init__(
        self,
        label: str = "",
        total: float = 100.0,
        stream=None,
        monitor: Monitor | None = None,
        eta_alpha: float = 0.22,
    ):
        """Do ProgressBar.  init for label, total, stream, monitor and return the result."""
        self.label = label
        self.total = max(total, 1e-12)
        self.stream = stream or sys.stderr
        self.monitor = monitor
        self.eta_alpha = eta_alpha
        self.enabled = (
            os.environ.get("TRIVORTEX_NO_PROGRESS", "") not in ("1", "true", "yes")
            and self.stream.isatty()
        )
        self.frac = 0.0
        self.tag = ""
        self._t0 = time.time()
        self._last_t = self._t0
        self._ema_rate = None  # доли/сек, EMA
        self._last_w = 0
        self._spin = Spinner("", stream=self.stream, braille=False)
        self._last_milestone = -1
        self._paused = False
        self._lock = threading.Lock()

    # ── публичное API ──
    def update(self, value: float, tag: str = "") -> None:
        """Do ProgressBar.update for value, tag and return the result."""
        with self._lock:
            now = time.time()
            frac = max(0.0, min(1.0, value / self.total))
            dt = now - self._last_t
            if dt > 0.01 and frac > self.frac:
                rate = (frac - self.frac) / dt
                if self._ema_rate is None:
                    self._ema_rate = rate
                else:
                    self._ema_rate = self.eta_alpha * rate + (1 - self.eta_alpha) * self._ema_rate
            self.frac = frac
            if tag:
                self.tag = tag
            self._last_t = now
            self._repaint(now)

    def narrow(self, lo: float, hi: float, value: float, tag: str = "") -> None:
        """Диапазонная шкала (двухпроходные прогоны делят один бар)."""
        span = max(hi - lo, 1e-12)
        self.update(lo + span * max(0.0, min(1.0, value)), tag)

    def heartbeat(self) -> None:
        """Прогресса нет, но время идёт — обновляем up/ETA в кадре."""
        with self._lock:
            self._repaint(time.time())

    def pause(self) -> None:
        """Handle ProgressBar.pause."""
        self._paused = True

    def resume(self) -> None:
        """Handle ProgressBar.resume."""
        self._paused = False

    def finish(self, message: str = "") -> None:
        """Do ProgressBar.finish for message and return the result."""
        with self._lock:
            if self.enabled:
                line = colorize(f"  ✓ {self.label}", GRN, True) if COLOR else f"  [ok] {self.label}"
                if message:
                    line += " — " + message
                line += f"  ({self._fmt(time.time() - self._t0)})"
                self.stream.write("\r" + " " * self._last_w + "\r" + line + "\n")
                self.stream.flush()
            else:
                pass  # (unused local removed)
                if message:
                    print(f"  {self.label}: {message}")

    # ── внутреннее ──
    def _eta(self) -> float | None:
        """Handle ProgressBar. eta."""
        if self._ema_rate is None or self._ema_rate <= 1e-12:
            return None
        return max(0.0, (1.0 - self.frac) / self._ema_rate)

    @staticmethod
    def _fmt(sec: float) -> str:
        """Do ProgressBar. fmt for sec and return the result."""
        sec = int(sec)
        return f"{sec // 3600:02d}:{(sec % 3600) // 60:02d}:{sec % 60:02d}"

    def _repaint(self, now: float) -> None:
        """Do ProgressBar. repaint for now and return the result."""
        if not self.enabled or self._paused:
            return
        w = _term_width()
        pct = self.frac * 100.0
        spin = "◐◓◑◒"[int(now * 8) % 4] if COLOR else "*"
        head = f"{colorize(spin, ICE, True)} {self.label}"
        bar_w = max(8, min(22, w // 4))
        filled = int(bar_w * self.frac)
        bar = colorize("▰" * filled, ICE, True) + colorize("▱" * (bar_w - filled), GRY)
        line = f"{head} {bar} {pct:5.1f}%"
        # хвост: статус → монитор → ETA → up (усекается справа налево)
        tail_parts = []
        if self.tag:
            tail_parts.append(self.tag)
        if self.monitor is not None:
            try:
                tail_parts.append(self.monitor.inline())
            except Exception:
                pass
        eta = self._eta()
        if eta is not None:
            tail_parts.append("ETA " + self._fmt(eta))
        tail_parts.append("up " + self._fmt(now - self._t0))
        tail = " · ".join(p for p in tail_parts if p)
        budget = w - visible_width(line) - 3
        if tail:
            tail = trunc_to(tail, max(budget, 0))
            line = f"{line} · {tail}"
        line = trunc_to(line, w)
        self.stream.write("\r" + " " * self._last_w + "\r" + pad_to(line, w))
        self._last_w = visible_width(line)
        self.stream.flush()


class BarQueue:
    """Ограниченная очередь косметических кадров: замёрзший терминал
    не дедлокает расчёт — старые кадры просто отбрасываются."""

    def __init__(self, maxsize: int = 256):
        """Do BarQueue.  init for maxsize and return the result."""
        import queue

        self.q: queue.Queue = queue.Queue(maxsize=maxsize)
        self._thread = None

    def put(self, fn) -> None:
        """Do BarQueue.put for fn and return the result."""
        try:
            self.q.put_nowait(fn)
        except Exception:
            pass  # очередь полна — выбрасываем самый старый кадр

    def start(self) -> None:
        """Handle BarQueue.start."""
        if self._thread is not None:
            return

        def pump():
            while True:
                fn = self.q.get()
                if fn is None:
                    return
                try:
                    fn()
                except Exception:
                    pass

        self._thread = threading.Thread(target=pump, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Handle BarQueue.stop."""
        self.put(None)


# ═══════════════════════════════════════════════════════════════════════════
# 7. Контрольный файл .tv_ctl (внешнее управление баром)
# ═══════════════════════════════════════════════════════════════════════════
def ctl_command(run_dir: str) -> str | None:
    """Читает команды pause/resume/snapshot из <run_dir>/.tv_ctl."""
    path = os.path.join(run_dir, ".tv_ctl")
    try:
        with open(path, encoding="utf-8") as fh:
            cmd = fh.read().strip().lower()
        if cmd in ("pause", "resume", "snapshot"):
            os.remove(path)
            return cmd
    except OSError:
        pass
    return None


# ═══════════════════════════════════════════════════════════════════════════
# 8. Инициализация при импорте
# ═══════════════════════════════════════════════════════════════════════════
detect_color_mode(sys.stdout)
