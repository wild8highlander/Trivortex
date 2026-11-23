#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — аниматор: GIF89a (собственный LZW) и MP4 (ffmpeg/imageio).
GIF-писатель — полностью свой: LZW-сжатие по спецификации GIF89a (переменный
размер кода 8→9→…, clear/end коды, sub-blocks ≤255 байт), фиксированная
web-палитра 6-6-6 + серая рампа (как в AB-CLOUD). Без imageio/ffmpeg GIF
работает всегда; MP4 — через ffmpeg (subprocess) или imageio при наличии.
Пресеты: orbit.gif, choreography.mp4, macro.gif, micro.gif — со своим
прогресс-баром на каждом кадре.
"""
from __future__ import annotations
import os
import shutil
import struct
import subprocess
from typing import Callable, Sequence
from render.hud import ProgressBar
# ═══════════════════════════════════════════════════════════════════════════
# Палитра: 6×6×6 web-safe + 40 оттенков серого = 256 цветов
# ═══════════════════════════════════════════════════════════════════════════
def build_palette() -> list[tuple[int, int, int]]:
    pal = []
    levels = [0, 51, 102, 153, 204, 255]
    for r in levels:
        for g in levels:
            for b in levels:
                pal.append((r, g, b))
    for i in range(40):
        v = int(i * 255 / 39)
        pal.append((v, v, v))
    # индекс 0 = фон (тёмно-синий AURORA)
    pal[0] = (13, 22, 40)
    return pal
PALETTE = build_palette()
def nearest_index(color: tuple[int, int, int]) -> int:
    """Ближший индекс палитры (быстрый: квантование 6-6-6 + перебор серых)."""
    r, g, b = color
    # сначала быстрый путь: web-safe
    def lev(c):
        return min(5, (c * 6 + 127) // 256)
    idx = 36 * lev(r) + 6 * lev(g) + lev(b)
    if idx == 0:
        return 0
    best, best_d = idx, (r - PALETTE[idx][0]) ** 2 + \
        (g - PALETTE[idx][1]) ** 2 + (b - PALETTE[idx][2]) ** 2
    # проверим ближайшие серые (216 + i)
    grey = (r + g + b) // 3
    gi = 216 + min(39, grey * 40 // 256)
    gcol = PALETTE[gi]
    d = (r - gcol[0]) ** 2 + (g - gcol[1]) ** 2 + (b - gcol[2]) ** 2
    if d < best_d:
        best, best_d = gi, d
    return best
# ═══════════════════════════════════════════════════════════════════════════
# LZW GIF (переменная длина кода)
# ═══════════════════════════════════════════════════════════════════════════
class _LZWWriter:
    """Кодер GIF-LZW, побитно синхронный со стандартным декодером.

    Ключ синхронизации (спецификация GIF89a, Appendix F): размер кода
    растёт в ТОЙ ЖЕ точке потока, где его увеличивает декодер — сразу
    ПОСЛЕ добавления нового кода, когда next_code достиг 2^size.
    """

    def __init__(self, min_code_size: int = 8):
        self.min_size = min_code_size
        self.clear_code = 1 << min_code_size
        self.end_code = self.clear_code + 1

    def compress(self, data: bytes) -> bytes:
        """Кодер, зеркальный каноническому декодеру.

        Декодер при чтении каждого кода (начиная со второго после clear)
        добавляет запись prev_entry + entry[0]. Кодер обязан добавлять
        РОВНО ТУ ЖЕ запись в той же точке потока: prev_prefix + prefix[0].
        """
        out = bytearray()
        acc = 0
        nbits = 0
        size = self.min_size + 1
        table: dict[tuple[int, ...], int] = {}
        next_code = self.end_code + 1

        def emit(code: int):
            nonlocal acc, nbits
            acc |= code << nbits
            nbits += size
            while nbits >= 8:
                out.append(acc & 0xFF)
                acc >>= 8
                nbits -= 8

        emit(self.clear_code)
        if not data:
            emit(self.end_code)
            if nbits:
                out.append(acc & 0xFF)
            return bytes(out)
        prefix: tuple[int, ...] = (data[0],)
        prev_prefix: tuple[int, ...] | None = None
        for ch in data[1:]:
            key = prefix + (ch,)
            if key in table:
                prefix = key
                continue
            emit(table.get(prefix, prefix[0]))
            # словарная запись — как у декодера: prev_prefix + prefix[0]
            if prev_prefix is not None and next_code < 4096:
                table[prev_prefix + (prefix[0],)] = next_code
                next_code += 1
                # рост ширины: следующий свободный код не помещается
                # в size бит (канон giflib/PIL: при 512/1024/2048)
                if next_code == (1 << size) and size < 12:
                    size += 1
            prev_prefix = prefix
            prefix = (ch,)
        emit(table.get(prefix, prefix[0]))
        if prev_prefix is not None and next_code < 4096:
            table[prev_prefix + (prefix[0],)] = next_code  # noqa: F841 — полнота
        emit(self.end_code)
        if nbits:
            out.append(acc & 0xFF)
        return bytes(out)


def lzw_compress(data: bytes) -> bytes:
    """Управляемая обёртка: корректный алгоритм GIF-LZW."""
    w = _LZWWriter(8)
    return w.compress(data)
# ═══════════════════════════════════════════════════════════════════════════
# GIF89a-писатель
# ═══════════════════════════════════════════════════════════════════════════
def write_gif(path: str, frames: Sequence[bytes], width: int, height: int,
              delay_cs: int = 5, loop: int = 0,
              palette: list[tuple[int, int, int]] | None = None) -> int:
    """
    frames: список индексированных кадров (len = w*h, значения — индексы
    палитры). delay_cs — задержка в сотых секунды, loop=0 — бесконечно.
    """
    pal = palette or PALETTE
    out = bytearray()
    out += b"GIF89a"
    out += struct.pack("<HH", width, height)
    out += bytes([0xF7, 0, 0])          # GCT flag, 256 цветов
    for r, g, b in pal:
        out += bytes((r, g, b))
    # NETSCAPE-расширение цикла
    out += b"\x21\xFF\x0BNETSCAPE2.0\x03\x01"
    out += struct.pack("<H", loop & 0xFFFF)
    out += b"\x00"
    for frame in frames:
        out += b"\x21\xF9\x04"          # Graphic Control Extension
        out += bytes([0x04])            # disposal = 1 (не стирать)? — 0x04 = без удаления фона
        out += struct.pack("<H", delay_cs)
        out += bytes([0, 0])            # transparent index, terminator
        # дескриптор изображения
        out += b"\x2C"
        out += struct.pack("<HHHH", 0, 0, width, height)
        out += bytes([0])               # без локальной палитры
        out += bytes([8])               # LZW min code size
        data = lzw_compress(bytes(frame))
        # sub-blocks ≤ 255
        for off in range(0, len(data), 255):
            chunk = data[off:off + 255]
            out += bytes([len(chunk)]) + chunk
        out += bytes([0])               # конец sub-blocks
    out += b"\x3B"                      # trailer
    with open(path, "wb") as fh:
        fh.write(out)
    return len(out)
def frame_rgb_to_indices(pixels: bytes, width: int, height: int,
                         bg: tuple[int, int, int] = (13, 22, 40)) -> bytes:
    """RGB-кадр (w*h*3) → индексы палитры; фон квантуется в индекс 0."""
    n = width * height
    out = bytearray(n)
    bg_idx = nearest_index(bg)
    for i in range(n):
        o = i * 3
        r, g, b = pixels[o], pixels[o + 1], pixels[o + 2]
        if (r, g, b) == bg:
            out[i] = bg_idx
        else:
            out[i] = nearest_index((r, g, b))
    return bytes(out)
# ═══════════════════════════════════════════════════════════════════════════
# Аниматор сцен
# ═══════════════════════════════════════════════════════════════════════════
def animate_scene(scene, output: str, n_frames: int = 48, fps: int = 12,
                  backend: str = "pure", width: int = 480, height: int = 360,
                  progress: bool = True, format: str = "gif"
                  ) -> dict:
    """
    Анимировать историю сцены в GIF (собственный LZW) или MP4.
    Кадры берутся из scene.trajectory_history (равномерно n_frames штук),
    рисуются выбранным бэкендом и собираются:
      gif — write_gif (всегда, без зависимостей);
      mp4 — imageio если есть, иначе ffmpeg -f image2.
    """
    if not scene.trajectory_history:
        raise ValueError("у сцены нет истории: прогоните симуляцию")
    from core.config import MasterConfig
    cfg = scene.config
    cfg.image_width, cfg.image_height = width, height
    from render.engine import get_backend
    eng = get_backend(backend, cfg)
    eng.setup(scene)
    total = len(scene.trajectory_history)
    step = max(1, total // n_frames)
    indices = list(range(0, total, step))[:n_frames]
    if indices[-1] != total - 1:
        indices.append(total - 1)
    bar = ProgressBar(f"анимация {os.path.basename(output)}",
                      len(indices)) if progress else None
    # GIF: индексированные кадры
    gif_frames: list[bytes] = []
    png_files: list[str] = []
    tmp_dir = os.path.dirname(os.path.abspath(output)) or "."
    stem = os.path.splitext(os.path.basename(output))[0]
    
    scale = None
    from render.engine import _scene_scale
    scale = _scene_scale(scene)
    for i, idx in enumerate(indices):
        t = scene.time_history[idx]
        state = scene.trajectory_history[idx]
        bodies = [dict(position=tuple(s[:3]),
                       radius=max(scene.bodies[j].radius / scale, 0.04),
                       color=scene.bodies[j].color,
                       label=scene.bodies[j].name)
                  for j, s in enumerate(state)]
        # трейл до момента t
        trails = []
        for j in range(len(scene.bodies)):
            trail = [(scene.trajectory_history[k][j][0],
                      scene.trajectory_history[k][j][1],
                      scene.trajectory_history[k][j][2])
                     for k in range(0, idx + 1, max(1, idx // 12 or 1))]
            trails.append(trail)
        from render.pure_raster import render_bodies
        frame = render_bodies(bodies, width=width, height=height,
                              trails=trails)
        if format == "gif":
            gif_frames.append(frame_rgb_to_indices(bytes(frame.pixels),
                                                   width, height,
                                                   bg=frame.bg))
        else:
            p = os.path.join(tmp_dir, f"{stem}_frame_{i:04d}.png")
            frame.save_png(p)
            png_files.append(p)
        if bar:
            bar.update(i + 1, tag=f"кадр {i + 1}/{len(indices)}")
    result = dict(frames=len(indices), backend=backend, width=width,
                  height=height)
    if format == "gif":
        size = write_gif(output, gif_frames, width, height,
                         delay_cs=max(2, 100 // fps))
        result["path"] = output
        result["bytes"] = size
    else:
        size = _encode_mp4(png_files, output, fps)
        result["path"] = output
        result["bytes"] = size
        # убрать временные кадры
        for p in png_files:
            try:
                os.remove(p)
            except OSError:
                pass
    if bar:
        bar.finish(f"{result['bytes']} байт")
    return result
def _encode_mp4(png_files: list[str], output: str, fps: int) -> int:
    """MP4 через imageio (если есть) или ffmpeg."""
    try:
        import imageio.v2 as imageio
        frames = [imageio.imread(p) for p in png_files]
        imageio.mimsave(output, frames, fps=fps, codec="libx264",
                        quality=8, macro_block_size=8)
        return os.path.getsize(output)
    except Exception:
        pass
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        first = png_files[0]
        pattern = first.replace("_frame_0000", "_frame_%04d")
        cmd = [ffmpeg, "-y", "-framerate", str(fps), "-i", pattern,
               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
               output]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode == 0 and os.path.exists(output):
            return os.path.getsize(output)
        raise RuntimeError(f"ffmpeg не смог собрать MP4: "
                           f"{proc.stderr[-400:]}")
    raise RuntimeError("MP4 недоступен: нет ни imageio, ни ffmpeg "
                       "(GIF работает всегда)")
# ── пресеты анимаций ──
ANIMATION_PRESETS = {
    "orbit": dict(n_frames=48, fps=12, backend="pure", width=480,
                  height=360, format="gif"),
    "choreography": dict(n_frames=64, fps=16, backend="pure", width=480,
                         height=360, format="mp4"),
    "macro": dict(n_frames=40, fps=10, backend="pure", width=420,
                  height=315, format="gif"),
    "micro": dict(n_frames=40, fps=10, backend="mpl", width=420,
                  height=315, format="gif"),
}
