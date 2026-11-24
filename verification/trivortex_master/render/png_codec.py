#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — собственный PNG-кодер на stdlib.

Полный конвейер по спецификации PNG (ISO/IEC 15948), без PIL/Pillow:
  * CRC32 (собственная таблица, полином 0xEDB88320);
  * фильтр строк (Sub/Up/Average/Paeth — эвристика минимальной суммы);
  * DEFLATE: fixed-Huffman блоки + жадный LZ77 (собственная реализация
    по образцу байтовых писателей AB-CLOUD; zlib-обёртка с adler32);
  * чанки IHDR/IDAT/IEND, 8-бит RGB/RGBA.

Именно этот кодер используется pure_raster и аниматором — изображение
можно собрать и записать без единого внешнего пакета.
"""

from __future__ import annotations

import struct
from typing import Sequence


# ═══════════════════════════════════════════════════════════════════════════
# CRC32 (PNG, полином 0xEDB88320)
# ═══════════════════════════════════════════════════════════════════════════
def _build_crc_table() -> list[int]:
    """Handle build crc table."""
    table = []
    for n in range(256):
        c = n
        for _ in range(8):
            c = (0xEDB88320 ^ (c >> 1)) if (c & 1) else (c >> 1)
        table.append(c)
    return table


_CRC_TABLE = _build_crc_table()


def crc32(data: bytes, crc: int = 0) -> int:
    """Do crc32 for data, crc and return the result."""
    c = crc ^ 0xFFFFFFFF
    for b in data:
        c = _CRC_TABLE[(c ^ b) & 0xFF] ^ (c >> 8)
    return c ^ 0xFFFFFFFF


def adler32(data: bytes, a: int = 1, b: int = 0) -> int:
    """Do adler32 for data, a, b and return the result."""
    for x in data:
        a = (a + x) % 65521
        b = (b + a) % 65521
    return (b << 16) | a


# ═══════════════════════════════════════════════════════════════════════════
# DEFLATE: fixed-Huffman + LZ77 (жадный), битуровень вручную
# ═══════════════════════════════════════════════════════════════════════════
class _BitWriter:
    """Handle BitWriter."""
    def __init__(self):
        """Handle BitWriter.  init."""
        self.buf = bytearray()
        self.acc = 0
        self.nbits = 0

    def write_bits(self, value: int, count: int) -> None:
        """Do BitWriter.write bits for value, count and return the result."""
        self.acc |= (value & ((1 << count) - 1)) << self.nbits
        self.nbits += count
        while self.nbits >= 8:
            self.buf.append(self.acc & 0xFF)
            self.acc >>= 8
            self.nbits -= 8

    def write_bits_rev(self, value: int, count: int) -> None:
        """Huffman-коды пишутся MSB-first (перевёрнутые)."""
        v = 0
        for i in range(count):
            v = (v << 1) | ((value >> i) & 1)
        self.write_bits(v, count)

    def flush(self, pad_bit: int = 0) -> None:
        """Do BitWriter.flush for pad_bit and return the result."""
        if self.nbits:
            self.write_bits(pad_bit, 8 - self.nbits)

    def bytes(self) -> bytes:
        """Handle BitWriter.bytes."""
        return bytes(self.buf)


# ── литеральные коды fixed-Huffman ──
def _fixed_lit_code(sym: int) -> tuple[int, int]:
    """(код, длина) для литерала/длины по RFC 1951 §3.2.6."""
    if sym <= 143:
        return 0x30 + sym, 8
    if sym <= 255:
        return 0x190 + sym - 144, 9
    if sym <= 279:
        return sym - 256, 7
    return 0xC0 + sym - 280, 8


_LENGTH_BASE = [
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    13,
    15,
    17,
    19,
    23,
    27,
    31,
    35,
    43,
    51,
    59,
    67,
    83,
    99,
    115,
    131,
    163,
    195,
    227,
    258,
]
_LENGTH_EXTRA = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    1,
    1,
    1,
    2,
    2,
    2,
    2,
    3,
    3,
    3,
    3,
    4,
    4,
    4,
    4,
    5,
    5,
    5,
    5,
    0,
]
_DIST_BASE = [
    1,
    2,
    3,
    4,
    5,
    7,
    9,
    13,
    17,
    25,
    33,
    49,
    65,
    97,
    129,
    193,
    257,
    385,
    513,
    769,
    1025,
    1537,
    2049,
    3073,
    4097,
    6145,
    8193,
    12289,
    16385,
    24577,
]
_DIST_EXTRA = [
    0,
    0,
    0,
    0,
    1,
    1,
    2,
    2,
    3,
    3,
    4,
    4,
    5,
    5,
    6,
    6,
    7,
    7,
    8,
    8,
    9,
    9,
    10,
    10,
    11,
    11,
    12,
    12,
    13,
    13,
]


def _match_length_code(length: int) -> tuple[int, int, int]:
    """(код длины, доп. биты, значение доп. битов)."""
    for i in range(len(_LENGTH_BASE) - 1, -1, -1):
        if length >= _LENGTH_BASE[i]:
            extra = length - _LENGTH_BASE[i]
            return 257 + i, _LENGTH_EXTRA[i], extra
    return 257, 0, 0


def _match_dist_code(dist: int) -> tuple[int, int, int]:
    """Do match dist code for dist and return the result."""
    for i in range(len(_DIST_BASE) - 1, -1, -1):
        if dist >= _DIST_BASE[i]:
            extra = dist - _DIST_BASE[i]
            return i, _DIST_EXTRA[i], extra
    return 0, 0, 0


def deflate_fixed(data: bytes) -> bytes:
    """DEFLATE-блок с fixed-Huffman (LZ77 с хэш-цепочкой, окно 32 КБ).

    Хэш-цепочка (head/tail по 3-байтовому хэшу) даёт O(n)-поиск вместо
    полного сканирования окна — без неё кадр 320×240 шумной текстуры
    сжимался бы ~80 с, с ней — доли секунды.
    """
    bw = _BitWriter()
    bw.write_bits(1, 1)  # BFINAL = 1
    bw.write_bits(1, 2)  # BTYPE = 01 (fixed)
    n = len(data)
    if n == 0:
        c, clen = _fixed_lit_code(256)
        bw.write_bits_rev(c, clen)
        bw.flush()
        return bw.bytes()

    # хэш-цепочка: head[hash] — последняя позиция, tail[pos&mask] — предыдущая
    HASH_SIZE = 1 << 15
    WMASK = 0x7FFF
    head = [-1] * HASH_SIZE
    tail = [-1] * (WMASK + 1)

    def h3(pos: int) -> int:
        return ((data[pos] << 10) ^ (data[pos + 1] << 5) ^ data[pos + 2]) & (HASH_SIZE - 1)

    def insert(pos: int) -> None:
        hv = h3(pos)
        tail[pos & WMASK] = head[hv]
        head[hv] = pos

    i = 0
    MAX_CHAIN = 32  # глубина цепочки (компромисс скорость/сжатие)
    while i < n:
        best_len = 0
        best_dist = 0
        if i + 3 <= n:
            limit = min(258, n - i)
            hv = h3(i)
            cand = head[hv]
            chain = 0
            while cand >= 0 and chain < MAX_CHAIN:
                dist = i - cand
                if dist > 32768:
                    break
                # быстрый отказ по первому байту
                if data[cand] == data[i]:
                    l = 1
                    while l < limit and data[cand + l] == data[i + l]:
                        l += 1
                    if l > best_len:
                        best_len = l
                        best_dist = dist
                        if l >= limit:
                            break
                cand = tail[cand & WMASK]
                chain += 1
        if best_len >= 3:
            # вставить позиции матча в цепочку
            for k in range(best_len):
                if i + k + 3 <= n:
                    insert(i + k)
            code, extra_bits, extra_val = _match_length_code(best_len)
            c, clen = _fixed_lit_code(code)
            bw.write_bits_rev(c, clen)
            if extra_bits:
                bw.write_bits(extra_val, extra_bits)
            dcode, dbits, dval = _match_dist_code(best_dist)
            bw.write_bits_rev(dcode, 5)
            if dbits:
                bw.write_bits(dval, dbits)
            i += best_len
        else:
            insert(i) if i + 3 <= n else None
            c, clen = _fixed_lit_code(data[i])
            bw.write_bits_rev(c, clen)
            i += 1
    # EOB (код 256)
    c, clen = _fixed_lit_code(256)
    bw.write_bits_rev(c, clen)
    bw.flush()
    return bw.bytes()


def zlib_wrap(deflated: bytes, original: bytes | None = None) -> bytes:
    """zlib-обёртка: заголовок 0x78 0x01 + adler32(ИСХОДНЫХ данных!).

    adler32 в zlib считается по несжатым данным (RFC 1950 §2.2),
    поэтому обязателен параметр original.
    """
    src = original if original is not None else deflated
    return b"\x78\x01" + deflated + struct.pack(">I", adler32(src))


# ═══════════════════════════════════════════════════════════════════════════
# PNG-писатель
# ═══════════════════════════════════════════════════════════════════════════
def _paeth(a: int, b: int, c: int) -> int:
    """Do paeth for a, b, c and return the result."""
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def _filter_rows(raw: bytes, width: int, height: int, bpp: int) -> bytes:
    """Выбор фильтра на строку: минимум суммы |байт| (эвристика PNG)."""
    stride = width * bpp
    out = bytearray()
    prev = bytes(stride)
    for row in range(height):
        base = row * stride
        cur = raw[base : base + stride]
        # все 5 фильтров, берём минимальную сумму
        best_type, best_sum, best_row = 0, 1 << 62, None
        for ftype in range(5):
            filtered = bytearray(stride)
            s = 0
            for x in range(stride):
                a = cur[x - bpp] if x >= bpp else 0
                b = prev[x]
                c = prev[x - bpp] if x >= bpp else 0
                if ftype == 0:
                    v = cur[x]
                elif ftype == 1:
                    v = (cur[x] - a) & 0xFF
                elif ftype == 2:
                    v = (cur[x] - b) & 0xFF
                elif ftype == 3:
                    v = (cur[x] - (a + b) // 2) & 0xFF
                else:
                    v = (cur[x] - _paeth(a, b, c)) & 0xFF
                filtered[x] = v
                s += v if v < 128 else 256 - v
            if s < best_sum:
                best_sum, best_type, best_row = s, ftype, filtered
        out.append(best_type)
        out.extend(best_row)
        prev = cur
    return bytes(out)


def write_png(
    path: str,
    pixels: Sequence[int],
    width: int,
    height: int,
    alpha: bool = False,
    level_filter: bool = True,
) -> int:
    """
    Записать PNG. pixels — плоский список/bytes RGB(A): len = w*h*bpp.
    Возвращает размер файла.
    """
    bpp = 4 if alpha else 3
    expected = width * height * bpp
    if len(pixels) < expected:
        raise ValueError(f"мало пикселей: {len(pixels)} < {expected}")
    raw = bytes(pixels[:expected])
    color_type = 6 if alpha else 2

    if level_filter:
        filtered = _filter_rows(raw, width, height, bpp)
    else:
        stride = width * bpp
        filtered = b"".join(b"\x00" + raw[r * stride : (r + 1) * stride] for r in range(height))

    compressed = zlib_wrap(deflate_fixed(filtered), original=filtered)

    def chunk(tag: bytes, payload: bytes) -> bytes:
        crc = crc32(tag + payload)
        return struct.pack(">I", len(payload)) + tag + payload + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, color_type, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    # IDAT порционно по 64 КБ
    step = 65536
    for off in range(0, len(compressed), step):
        png += chunk(b"IDAT", compressed[off : off + step])
    png += chunk(b"IEND", b"")

    with open(path, "wb") as fh:
        fh.write(png)
    return len(png)


def write_ppm(path: str, pixels: Sequence[int], width: int, height: int) -> int:
    """PPM P6 — дешёвый растровый вывод без кодирования."""
    raw = bytes(pixels[: width * height * 3])
    with open(path, "wb") as fh:
        fh.write(f"P6\n{width} {height}\n255\n".encode("ascii"))
        fh.write(raw)
    return width * height * 3 + 15
