#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — PDF-писатель 1.4 на чистом stdlib.

Минимальный валидный PDF: каталог, страницы, шрифты (Helvetica, Helvetica-Bold),
текстовые операторы (Tj, TD), линии/прямоугольники (re, m/l/S), заливка RGB,
несколько страниц, xref-таблица. Кириллица — через WinAnsi невозможна в
стандартных шрифтах: текст транслитерируется (honest fallback), а при
наличии fpdf2/fpdf используется настоящий Unicode-ридер.
"""
from __future__ import annotations

import math
import os
from typing import Sequence

# ═══════════════════════════════════════════════════════════════════════════
# Транслитерация кириллицы → латиница (шрифты PDF core — WinAnsi)
# ═══════════════════════════════════════════════════════════════════════════
_TRANS = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ъ': '"', 'ы': 'y', 'ь': "'", 'э': 'e', 'ю': 'yu', 'я': 'ya',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO',
    'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'J', 'К': 'K', 'Л': 'L', 'М': 'M',
    'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
    'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SCH',
    'Ъ': '"', 'Ы': 'Y', 'Ь': "'", 'Э': 'E', 'Ю': 'YU', 'Я': 'YA',
}


def translit(text: str) -> str:
    return "".join(_TRANS.get(c, c) for c in text)


def _esc(text: str) -> str:
    return (text.replace("\\", r"\\").replace("(", r"\(")
            .replace(")", r"\)"))


# ═══════════════════════════════════════════════════════════════════════════
# Класс страницы: поток операций
# ═══════════════════════════════════════════════════════════════════════════
A4_W, A4_H = 595.28, 841.89  # пункты

ACCENT = (0.106, 0.42, 0.478)     # #1B6B7A
DARK = (0.04, 0.086, 0.157)       # #0A1628
GREY = (0.35, 0.42, 0.49)
LIGHT = (0.93, 0.95, 0.96)


class _Page:
    def __init__(self):
        self.ops: list[str] = []

    # ── текст ──
    def text(self, x: float, y: float, s: str, size: float = 10.5,
             bold: bool = False, color: tuple = DARK) -> None:
        font = "F2" if bold else "F1"
        r, g, b = color
        self.ops.append(
            f"BT /{font} {size:.1f} Tf {r:.3f} {g:.3f} {b:.3f} rg "
            f"{x:.1f} {y:.1f} Td ({_esc(s)}) Tj ET")

    def text_right(self, x_right: float, y: float, s: str, size: float = 10.5,
                   bold: bool = False, color: tuple = DARK) -> None:
        # ширина по эмпирической метрике Helvetica (~0.5 em в среднем)
        width = len(s) * size * 0.5
        self.text(x_right - width, y, s, size, bold, color)

    def heading(self, text: str, y: float, level: int = 1) -> float:
        """Заголовок с полосой-акцентом; возвращает новую позицию y."""
        size = 16 if level == 1 else 12.5
        color = DARK if level == 1 else ACCENT
        self.text(56, y, translit(text), size=size, bold=True, color=color)
        self.rect(56, y - 5, 60, 2, fill=ACCENT)
        return y - (26 if level == 1 else 20)

    # ── графика ──
    def rect(self, x: float, y: float, w: float, h: float,
             fill: tuple | None = None, stroke: tuple | None = None) -> None:
        parts = [f"{x:.1f} {y:.1f} {w:.1f} {h:.1f} re"]
        if fill is not None:
            r, g, b = fill
            parts.append(f"{r:.3f} {g:.3f} {b:.3f} rg")
        if stroke is not None:
            r, g, b = stroke
            parts.append(f"{r:.3f} {g:.3f} {b:.3f} RG")
        op = "B" if (fill is not None and stroke is not None) else \
             ("f" if fill is not None else "S")
        parts.append(op)
        self.ops.append(" ".join(parts))

    def line(self, x0: float, y0: float, x1: float, y1: float,
             color: tuple = GREY, width: float = 0.6) -> None:
        r, g, b = color
        self.ops.append(f"{r:.3f} {g:.3f} {b:.3f} RG {width:.1f} w "
                        f"{x0:.1f} {y0:.1f} m {x1:.1f} {y1:.1f} l S")

    # ── таблица ──
    def table(self, headers: Sequence[str], rows: Sequence[Sequence[str]],
              y: float, x: float = 56, col_w: Sequence[float] | None = None,
              font_size: float = 8.5) -> float:
        ncols = len(headers)
        if col_w is None:
            total = A4_W - 2 * x
            col_w = [total / ncols] * ncols
        row_h = 15
        # шапка
        self.rect(x, y - row_h + 3, sum(col_w), row_h, fill=ACCENT)
        cx = x
        for i, h in enumerate(headers):
            self.text(cx + 4, y - row_h + 8, translit(str(h))[:40],
                      size=font_size, bold=True, color=(1, 1, 1))
            cx += col_w[i]
        y -= row_h
        # строки с зеброй
        for ridx, row in enumerate(rows):
            if ridx % 2 == 0:
                self.rect(x, y - row_h + 3, sum(col_w), row_h, fill=LIGHT)
            cx = x
            for i, cell in enumerate(row):
                s = translit(str(cell))
                # обрезка по ширине колонки
                max_chars = max(int(col_w[i] / (font_size * 0.5)) - 1, 4)
                if len(s) > max_chars:
                    s = s[:max_chars - 1] + "…"
                self.text(cx + 4, y - row_h + 8, s, size=font_size)
                cx += col_w[i]
            y -= row_h
            if y < 60:      # защита от переполнения — обрезаем (упрощённо)
                break
        self.line(x, y + 5, x + sum(col_w), y + 5, color=ACCENT)
        return y - 8

    def wrap_text(self, text: str, x: float, y: float, width_chars: int = 92,
                  size: float = 10, color: tuple = DARK,
                  line_gap: float = 13.5) -> float:
        """Абзац с переносом по словам; возвращает новый y."""
        words = translit(text).split()
        line = ""
        for word in words:
            if len(line) + len(word) + 1 > width_chars:
                self.text(x, y, line, size=size, color=color)
                y -= line_gap
                line = word
            else:
                line = word if not line else line + " " + word
        if line:
            self.text(x, y, line, size=size, color=color)
            y -= line_gap
        return y - 4


# ═══════════════════════════════════════════════════════════════════════════
# Сборка PDF
# ═══════════════════════════════════════════════════════════════════════════
class PDFBuilder:
    def __init__(self, title: str = "TRIVORTEX MASTER Report"):
        self.title = title
        self.pages: list[_Page] = [self._new_page()]

    def _new_page(self) -> _Page:
        page = _Page()
        # верхний колонтитул
        page.rect(0, A4_H - 30, A4_W, 30, fill=DARK)
        page.text(56, A4_H - 20, translit(self.title)[:70], size=9,
                  color=(0.9, 0.95, 1.0))
        return page

    @property
    def page(self) -> _Page:
        return self.pages[-1]

    def new_page(self) -> _Page:
        self.pages.append(self._new_page())
        return self.page

    def save(self, path: str) -> int:
        objs: list[bytes] = []

        def add(data: bytes) -> int:
            objs.append(data)
            return len(objs)  # 1-based номер

        # 1: каталог, 2: pages — зарезервированы
        add(b"")  # placeholder каталога
        add(b"")  # placeholder pages
        # шрифты: 3, 4
        add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
            b"/Encoding /WinAnsiEncoding >>")
        add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold "
            b"/Encoding /WinAnsiEncoding >>")
        font_refs = {1: "3 0 R", 2: "4 0 R"}
        # страницы и контент
        page_ids = []
        for pg in self.pages:
            content = ("\n".join(pg.ops)).encode("latin-1", errors="replace")
            cid = add(b"<< /Length " + str(len(content)).encode()
                      + b" >>\nstream\n" + content + b"\nendstream")
            pid = add(("<< /Type /Page /Parent 2 0 R /MediaBox "
                       f"[0 0 {A4_W} {A4_H}] /Resources << /Font << "
                       f"/F1 {font_refs[1]} /F2 {font_refs[2]} >> >> "
                       f"/Contents {cid} 0 R >>").encode())
            page_ids.append(pid)
        # каталог
        kids = " ".join(f"{p} 0 R" for p in page_ids)
        objs[0] = (f"<< /Type /Catalog /Pages 2 0 R >>").encode()
        objs[1] = (f"<< /Type /Pages /Count {len(page_ids)} "
                   f"/Kids [{kids}] >>").encode()

        # файл
        out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0] * (len(objs) + 1)
        for i, data in enumerate(objs, start=1):
            offsets[i] = len(out)
            out += f"{i} 0 obj\n".encode() + data + b"\nendobj\n"
        xref_pos = len(out)
        out += f"xref\n0 {len(objs) + 1}\n".encode()
        out += b"0000000000 65535 f \n"
        for i in range(1, len(objs) + 1):
            out += f"{offsets[i]:010d} 00000 n \n".encode()
        out += (f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R "
                f"/Title ({_esc(translit(self.title))}) >>\n"
                f"startxref\n{xref_pos}\n%%EOF").encode()
        with open(path, "wb") as fh:
            fh.write(bytes(out))
        return len(out)


def validate_pdf(path: str) -> list[str]:
    """Проверка: заголовок, xref, EOF."""
    problems = []
    try:
        with open(path, "rb") as fh:
            data = fh.read()
        if not data.startswith(b"%PDF-1.4"):
            problems.append("нет заголовка %PDF-1.4")
        if b"startxref" not in data:
            problems.append("нет startxref")
        if not data.rstrip().endswith(b"%%EOF"):
            problems.append("нет %%EOF")
        if b"/Type /Catalog" not in data:
            problems.append("нет каталога")
    except OSError as exc:
        problems.append(str(exc))
    return problems
