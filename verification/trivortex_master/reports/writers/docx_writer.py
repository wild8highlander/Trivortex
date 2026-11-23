#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — DOCX-писатель на чистом stdlib.

Валидный .docx без python-docx: ZIP-контейнер + пять XML-частей
([Content_Types].xml, _rels/.rels, word/document.xml, word/styles.xml,
word/_rels/document.xml.rels). Экранирование — xml.sax.saxutils.escape.

Поддержка: заголовки (стили Heading1/2), абзацы (жирный/курсив/цвет),
таблицы, изображения PNG (base64 → media/), метаданные.
"""

from __future__ import annotations

import base64
import hashlib
import os
import zipfile
from typing import Any, Sequence
from xml.sax.saxutils import escape

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

_CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="png" ContentType="image/png"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

_RELS_ROOT = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

_STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="%s">
<w:docDefaults><w:rPrDefault><w:rPr>
<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri"/>
<w:sz w:val="22"/>
</w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>
<w:pPr><w:spacing w:before="280" w:after="140"/></w:pPr>
<w:rPr><w:b/><w:color w:val="0A1628"/><w:sz w:val="32"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>
<w:pPr><w:spacing w:before="220" w:after="110"/></w:pPr>
<w:rPr><w:b/><w:color w:val="134252"/><w:sz w:val="27"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Normal"><w:name w:val="normal"/></w:style>
</w:styles>""" % W_NS


class DocxBuilder:
    """Сборка документа: абзацы, заголовки, таблицы, картинки."""

    def __init__(self, title: str = "Отчёт TRIVORTEX MASTER"):
        self.title = title
        self.body: list[str] = []
        self.rels: list[str] = []  # rId изображений
        self.media: list[tuple[str, bytes]] = []
        self._img_counter = 0

    # ── элементы ──
    def heading(self, text: str, level: int = 1) -> DocxBuilder:
        style = f"Heading{min(level, 2)}"
        self.body.append(
            f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'
        )
        return self

    def paragraph(
        self,
        text: str,
        bold: bool = False,
        italic: bool = False,
        color: str | None = None,
        size_half_pt: int = 22,
    ) -> DocxBuilder:
        rpr = ""
        if bold:
            rpr += "<w:b/>"
        if italic:
            rpr += "<w:i/>"
        if color:
            rpr += f'<w:color w:val="{color.lstrip("#")}"/>'
        rpr += f'<w:sz w:val="{size_half_pt}"/>'
        self.body.append(
            f"<w:p><w:r><w:rPr>{rpr}</w:rPr>"
            f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'
        )
        return self

    def bullet(self, text: str) -> DocxBuilder:
        self.body.append(
            '<w:p><w:pPr><w:ind w:left="360" w:hanging="180"/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">• {escape(text)}</w:t></w:r></w:p>'
        )
        return self

    def table(
        self,
        headers: Sequence[str],
        rows: Sequence[Sequence[str]],
        widths: Sequence[int] | None = None,
    ) -> DocxBuilder:
        """Таблица с заливкой шапки и зеброй строк."""
        ncols = len(headers)
        if widths is None:
            widths = [int(9000 / ncols)] * ncols
        # границы
        borders = (
            "<w:tblBorders>"
            '<w:top w:val="single" w:sz="4" w:color="1B6B7A"/>'
            '<w:left w:val="none" w:sz="0" w:color="auto"/>'
            '<w:bottom w:val="single" w:sz="4" w:color="1B6B7A"/>'
            '<w:right w:val="none" w:sz="0" w:color="auto"/>'
            '<w:insideH w:val="single" w:sz="2" w:color="C8DDE2"/>'
            '<w:insideV w:val="none" w:sz="0" w:color="auto"/>'
            "</w:tblBorders>"
        )
        xml = [f"<w:tbl><w:tblPr>{borders}" f'<w:tblW w:w="9000" w:type="dxa"/></w:tblPr>']
        # шапка
        xml.append("<w:tr><w:trPr><w:tblHeader/></w:trPr>")
        for h, w in zip(headers, widths):
            xml.append(
                f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>'
                f'<w:shd w:val="clear" w:fill="1B6B7A"/></w:tcPr>'
                f'<w:p><w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="19"/></w:rPr>'
                f'<w:t xml:space="preserve">{escape(str(h))}</w:t></w:r></w:p></w:tc>'
            )
        xml.append("</w:tr>")
        # строки
        for i, row in enumerate(rows):
            fill = "EDF3F5" if i % 2 else "FFFFFF"
            xml.append("<w:tr>")
            for cell in row:
                xml.append(
                    f'<w:tc><w:tcPr><w:tcW w:w="0" w:type="auto"/>'
                    f'<w:shd w:val="clear" w:fill="{fill}"/></w:tcPr>'
                    f'<w:p><w:r><w:rPr><w:sz w:val="19"/></w:rPr>'
                    f'<w:t xml:space="preserve">{escape(str(cell))}</w:t></w:r></w:p></w:tc>'
                )
            xml.append("</w:tr>")
        xml.append("</w:tbl>")
        # пустой абзац после таблицы (иначе Word склеивает)
        xml.append("<w:p/>")
        self.body.append("".join(xml))
        return self

    def image(self, png_path: str, width_emu: int = 5200000) -> DocxBuilder:
        """Вставить PNG. width_emu — ширина в EMU (914400 = 1 дюйм)."""
        with open(png_path, "rb") as fh:
            data = fh.read()
        self._img_counter += 1
        rid = f"rIdImg{self._img_counter}"
        name = f"image{self._img_counter}.png"
        self.media.append((name, data))
        self.rels.append(
            f'<Relationship Id="{rid}" '
            f'Type="http://schemas.openxmlformats.org/drawingml/2006/relationships/image" '
            f'Target="media/{name}"/>'
        )
        # размер: читаем из PNG-заголовка
        w_px = int.from_bytes(data[16:20], "big")
        h_px = int.from_bytes(data[20:24], "big")
        h_emu = int(width_emu * h_px / max(w_px, 1))
        self.body.append(f"""<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>
<wp:inline xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" distT="0" distB="0" distL="0" distR="0">
<wp:extent cx="{width_emu}" cy="{h_emu}"/>
<wp:docPr id="{self._img_counter}" name="{name}"/>
<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
<pic:nvPicPr><pic:cNvPr id="{self._img_counter}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>
<pic:blipFill><a:blip r:embed="{rid}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{width_emu}" cy="{h_emu}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>""")
        return self

    def spacer(self) -> DocxBuilder:
        self.body.append('<w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>')
        return self

    # ── сборка ──
    def _document_xml(self) -> str:
        core_props = (
            f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
            f'<w:r><w:rPr><w:b/><w:sz w:val="40"/><w:color w:val="0A1628"/></w:rPr>'
            f'<w:t xml:space="preserve">{escape(self.title)}</w:t></w:r></w:p>'
        )
        return (
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<w:document xmlns:w="{W_NS}">'
            f'<w:body>{core_props}{"".join(self.body)}'
            f'<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
            f'<w:pgMar w:top="1440" w:right="1417" w:bottom="1440" w:left="1701"/>'
            f"</w:sectPr></w:body></w:document>"
        )

    def _document_rels(self) -> str:
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(self.rels)
            + "</Relationships>"
        )

    def save(self, path: str) -> int:
        doc_rels_needed = bool(self.rels)
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", _CONTENT_TYPES)
            zf.writestr("_rels/.rels", _RELS_ROOT)
            zf.writestr("word/document.xml", self._document_xml())
            zf.writestr("word/styles.xml", _STYLES)
            if doc_rels_needed:
                zf.writestr("word/_rels/document.xml.rels", self._document_rels())
            for name, data in self.media:
                zf.writestr(f"word/media/{name}", data)
        return os.path.getsize(path)


def validate_docx(path: str) -> list[str]:
    """Проверка структуры: zip-целостность + обязательные части."""
    problems = []
    try:
        with zipfile.ZipFile(path) as zf:
            if zf.testzip() is not None:
                problems.append("битые CRC в zip")
            names = set(zf.namelist())
            for req in ("[Content_Types].xml", "_rels/.rels", "word/document.xml"):
                if req not in names:
                    problems.append(f"нет части {req}")
            doc = zf.read("word/document.xml").decode("utf-8")
            if "<w:document" not in doc or "<w:body>" not in doc:
                problems.append("document.xml без w:document/w:body")
    except zipfile.BadZipFile:
        problems.append("не zip-архив")
    return problems
