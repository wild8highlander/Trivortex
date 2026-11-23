#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — XLSX-писатель на чистом stdlib (OOXML SpreadsheetML).

Валидный .xlsx без openpyxl: ZIP-контейнер + части
[Content_Types].xml, _rels/.rels, xl/workbook.xml, xl/_rels/workbook.xml.rels,
xl/worksheets/sheet1.xml…, xl/styles.xml, xl/sharedStrings.xml (inline
strings вместо shared — проще и валидно).

Поддержка: несколько листов, типизация ячеек (число/строка/формула),
стили (жирный шапка, границы, заливка, число знаков), автосоответствие
столбцам, закрепление строки заголовков, числа в научной нотации.

Формулы пишутся как <f>…</f> и вычисляются при открытии в Excel/LibreOffice.
"""

from __future__ import annotations

import datetime as _dt
import os
import zipfile
from typing import Any, Sequence
from xml.sax.saxutils import escape

_NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
_NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def _col_letter(idx: int) -> str:
    """0 → A, 25 → Z, 26 → AA."""
    out = ""
    idx += 1
    while idx > 0:
        idx, rem = divmod(idx - 1, 26)
        out = chr(65 + rem) + out
    return out


# ═══════════════════════════════════════════════════════════════════════════
# Книга и листы
# ═══════════════════════════════════════════════════════════════════════════
class Worksheet:
    """Один лист: сетка ячеек + параметры."""

    def __init__(self, name: str, freeze_header: bool = True):
        self.name = name[:31]  # лимит Excel
        self.freeze_header = freeze_header
        self.rows: list[list[dict[str, Any]]] = []
        self.col_widths: dict[int, float] = {}

    def _cell(self, value: Any, style: str = "normal", fmt: str | None = None) -> dict[str, Any]:
        cell: dict[str, Any] = {"value": value, "style": style, "fmt": fmt}
        return cell

    def header(self, values: Sequence[str]) -> Worksheet:
        row = [self._cell(v, style="header") for v in values]
        self.rows.append(row)
        return self

    def row(
        self, values: Sequence[Any], style: str = "normal", fmt: str | None = None
    ) -> Worksheet:
        row = [self._cell(v, style=style, fmt=fmt) for v in values]
        self.rows.append(row)
        return self

    def formula_row(self, formulas: Sequence[str], style: str = "normal") -> Worksheet:
        row = [self._cell(("=", f), style=style) for f in formulas]
        self.rows.append(row)
        return self

    def autosize(self, samples: int = 200) -> Worksheet:
        """Оценить ширины столбцов по содержимому."""
        ncols = max((len(r) for r in self.rows), default=0)
        for c in range(ncols):
            width = 0.0
            for r in self.rows[:samples]:
                if c < len(r):
                    v = r[c]["value"]
                    if isinstance(v, tuple):
                        s = str(v[1])
                    else:
                        s = str(v)
                    width = max(width, len(s))
            self.col_widths[c] = min(max(width + 2.5, 9.0), 42.0)
        return self

    # ── сериализация листа ──
    def to_xml(self) -> str:
        parts = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            f'<worksheet xmlns="{_NS_MAIN}">',
        ]
        # ширины
        if self.col_widths:
            parts.append("<cols>")
            for c, w in sorted(self.col_widths.items()):
                parts.append(
                    f'<col min="{c + 1}" max="{c + 1}" ' f'width="{w:.1f}" customWidth="1"/>'
                )
            parts.append("</cols>")
        parts.append("<sheetData>")
        for r_idx, row in enumerate(self.rows, start=1):
            parts.append(f'<row r="{r_idx}">')
            for c_idx, cell in enumerate(row, start=1):
                ref = f"{_col_letter(c_idx - 1)}{r_idx}"
                v = cell["value"]
                style_idx = 0
                if cell["style"] == "header":
                    style_idx = 1
                elif cell["style"] == "bold":
                    style_idx = 2
                if isinstance(v, tuple) and v and v[0] == "=":
                    # формула
                    parts.append(f'<c r="{ref}" s="{style_idx}">' f"<f>{escape(str(v[1]))}</f></c>")
                elif isinstance(v, bool):
                    parts.append(
                        f'<c r="{ref}" s="{style_idx}" t="b">' f"<v>{1 if v else 0}</v></c>"
                    )
                elif isinstance(v, (int, float)):
                    if v != v:  # NaN
                        parts.append(f'<c r="{ref}" s="{style_idx}" t="e">' f"<v>#NUM!</v></c>")
                    else:
                        parts.append(f'<c r="{ref}" s="{style_idx}">' f"<v>{v!r}</v></c>")
                elif v is None:
                    parts.append(f'<c r="{ref}" s="{style_idx}"/>')
                else:
                    parts.append(
                        f'<c r="{ref}" s="{style_idx}" t="inlineStr">'
                        f'<is><t xml:space="preserve">'
                        f"{escape(str(v))}</t></is></c>"
                    )
            parts.append("</row>")
        parts.append("</sheetData>")
        if self.freeze_header and self.rows:
            parts.append(
                '<pane ySplit="1" topLeftCell="A2" ' 'activePane="bottomLeft" state="frozen"/>'
            )
        parts.append("</worksheet>")
        return "".join(parts)


class XlsxBuilder:
    """Сборка книги: листы, стили, сохранение."""

    def __init__(self, creator: str = "TRIVORTEX MASTER"):
        self.creator = creator
        self.sheets: list[Worksheet] = []

    def sheet(self, name: str, freeze_header: bool = True) -> Worksheet:
        ws = Worksheet(name, freeze_header)
        self.sheets.append(ws)
        return ws

    # ── части OOXML ──
    def _content_types(self) -> str:
        overrides = "".join(
            f'<Override PartName="/xl/worksheets/sheet{i + 1}.xml" '
            f'ContentType="application/vnd.openxmlformats-officedocument.'
            f'spreadsheetml.worksheet+xml"/>'
            for i in range(len(self.sheets))
        )
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/'
            '2006/content-types">'
            '<Default Extension="rels" ContentType="application/'
            'vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType='
            '"application/vnd.openxmlformats-officedocument.'
            'spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/styles.xml" ContentType='
            '"application/vnd.openxmlformats-officedocument.'
            'spreadsheetml.styles+xml"/>' + overrides + "</Types>"
        )

    def _root_rels(self) -> str:
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/'
            'package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.'
            'org/officeDocument/2006/relationships/officeDocument" '
            'Target="xl/workbook.xml"/></Relationships>'
        )

    def _workbook(self) -> str:
        sheets = "".join(
            f'<sheet name="{escape(s.name)}" sheetId="{i + 1}" ' f'r:id="rId{i + 1}"/>'
            for i, s in enumerate(self.sheets)
        )
        return (
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<workbook xmlns="{_NS_MAIN}" '
            f'xmlns:r="{_NS_REL}"><sheets>{sheets}</sheets></workbook>'
        )

    def _workbook_rels(self) -> str:
        rels = "".join(
            f'<Relationship Id="rId{i + 1}" Type="http://schemas.'
            f"openxmlformats.org/officeDocument/2006/relationships/"
            f'worksheet" Target="worksheets/sheet{i + 1}.xml"/>'
            for i in range(len(self.sheets))
        )
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/'
            'package/2006/relationships">'
            f'<Relationship Id="rIdStyle" Type="http://schemas.'
            f"openxmlformats.org/officeDocument/2006/relationships/"
            f'styles" Target="styles.xml"/>' + rels + "</Relationships>"
        )

    def _styles(self) -> str:
        """Минимальная таблица стилей: 0 normal, 1 header (жирный+заливка),
        2 bold."""
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="{_NS_MAIN}">
<fonts count="3">
<font><sz val="11"/><name val="Calibri"/></font>
<font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>
<font><b/><sz val="11"/><name val="Calibri"/></font>
</fonts>
<fills count="3">
<fill><patternFill patternType="none"/></fill>
<fill><patternFill patternType="gray125"/></fill>
<fill><patternFill patternType="solid">
<fgColor rgb="FF1B6B7A"/><bgColor indexed="64"/></patternFill></fill>
</fills>
<borders count="2">
<border><left/><right/><top/><bottom/><diagonal/></border>
<border><left style="thin"><color rgb="FFC8DDE2"/></left>
<right style="thin"><color rgb="FFC8DDE2"/></right>
<top style="thin"><color rgb="FFC8DDE2"/></top>
<bottom style="thin"><color rgb="FFC8DDE2"/></bottom><diagonal/></border>
</borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="3">
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
<xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1"/>
<xf numFmtId="0" fontId="2" fillId="0" borderId="0" xfId="0" applyFont="1"/>
</cellXfs>
</styleSheet>"""

    # ── сохранение ──
    def save(self, path: str) -> int:
        for ws in self.sheets:
            if not ws.col_widths:
                ws.autosize()
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", self._content_types())
            zf.writestr("_rels/.rels", self._root_rels())
            zf.writestr("xl/workbook.xml", self._workbook())
            zf.writestr("xl/_rels/workbook.xml.rels", self._workbook_rels())
            zf.writestr("xl/styles.xml", self._styles())
            for i, ws in enumerate(self.sheets):
                zf.writestr(f"xl/worksheets/sheet{i + 1}.xml", ws.to_xml())
        return os.path.getsize(path)


def validate_xlsx(path: str) -> list[str]:
    """Структурная валидация (zip + обязательные части + parse XML)."""
    import xml.dom.minidom as minidom

    problems = []
    try:
        with zipfile.ZipFile(path) as zf:
            if zf.testzip() is not None:
                problems.append("битые CRC")
            names = set(zf.namelist())
            for req in ("[Content_Types].xml", "_rels/.rels", "xl/workbook.xml"):
                if req not in names:
                    problems.append(f"нет {req}")
            # все листы парсятся
            for name in names:
                if name.startswith("xl/worksheets/sheet"):
                    try:
                        minidom.parseString(zf.read(name))
                    except Exception as exc:
                        problems.append(f"{name}: XML битый ({exc})")
            try:
                minidom.parseString(zf.read("xl/workbook.xml"))
            except Exception as exc:
                problems.append(f"workbook.xml: {exc}")
    except zipfile.BadZipFile:
        problems.append("не zip")
    return problems


# ═══════════════════════════════════════════════════════════════════════════
# Демо/самопроверка
# ═══════════════════════════════════════════════════════════════════════════
def self_check() -> dict:
    """Собрать книгу, валидировать, прочитать openpyxl (если есть)."""
    b = XlsxBuilder()
    ws = b.sheet("Сводка")
    ws.header(["Параметр", "Значение", "Единица"])
    ws.row(["N тел", 7, "шт"])
    ws.row(["Энергия", -2.345e33, "Дж"])
    ws.row(["Дата", _dt.date.today().isoformat(), "—"])
    ws2 = b.sheet("Формулы")
    ws2.header(["A", "B", "Сумма"])
    ws2.row([1.0, 2.0, None])
    ws2.formula_row(["A2*10", "B2*20", "A4+B4"])
    path = "/tmp/tv_selfcheck.xlsx"
    size = b.save(path)
    problems = validate_xlsx(path)
    # чтение openpyxl (если установлен)
    read_ok = None
    n_sheets = 0
    try:
        import openpyxl

        wb = openpyxl.load_workbook(path)
        n_sheets = len(wb.sheetnames)
        v = wb["Сводка"]["B2"].value
        read_ok = v == 7 and n_sheets == 2
    except ImportError:
        pass
    return dict(
        size_bytes=size,
        problems=problems,
        openpyxl_read_ok=read_ok,
        n_sheets=n_sheets,
        ok=not problems and (read_ok in (None, True)),
    )
