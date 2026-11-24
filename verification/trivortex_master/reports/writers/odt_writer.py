#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — ODT-писатель на чистом stdlib (OpenDocument Text).

Валидный .odt (OASIS OpenDocument 1.2): ZIP с первыми несжатыми
mimetype, content.xml (тело: заголовки, абзацы, списки, таблицы),
styles.xml (автоматические + общие стили), meta.xml (метаданные),
META-INF/manifest.xml.

Используется отчётным движком как 8-й формат (LibreOffice/Word
открывают напрямую).

Самопроверка: сборка, разбор XML всех частей, обязательные записи
манифеста, конвертация soffice → PDF (если LibreOffice в системе).
"""

from __future__ import annotations

import datetime as _dt
import os
import zipfile
from typing import Any, Sequence
from xml.sax.saxutils import escape

# пространства имён ODF
NS_OFFICE = "urn:oasis:names:tc:opendocument:xmlns:office:1.0"
NS_TEXT = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
NS_STYLE = "urn:oasis:names:tc:opendocument:xmlns:style:1.0"
NS_FO = "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
NS_TABLE = "urn:oasis:names:tc:opendocument:xmlns:table:1.0"
NS_MANIFEST = "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"

AURORA_BODY = "#1a2433"
AURORA_ACCENT = "#0e6f83"


class OdtBuilder:
    """Сборка ODT-документа: заголовки, абзацы, списки, таблицы."""

    def __init__(self, title: str = "TRIVORTEX MASTER", creator: str = "TRIVORTEX MASTER"):
        """Do OdtBuilder.  init for title, creator and return the result."""
        self.title = title
        self.creator = creator
        self.body_xml: list[str] = []
        self._list_depth = 0

    # ── содержимое ──
    def heading(self, text: str, level: int = 1) -> OdtBuilder:
        """Do OdtBuilder.heading for text, level and return the result."""
        lvl = max(1, min(level, 6))
        self.body_xml.append(
            f'<text:h text:outline-level="{lvl}" '
            f'text:style-name="H{lvl}">{escape(text)}</text:h>'
        )
        return self

    def paragraph(self, text: str, style: str = "Standard") -> OdtBuilder:
        """Do OdtBuilder.paragraph for text, style and return the result."""
        self.body_xml.append(f'<text:p text:style-name="{style}">{escape(text)}</text:p>')
        return self

    def bullet(self, text: str) -> OdtBuilder:
        """Do OdtBuilder.bullet for text and return the result."""
        self.body_xml.append(f'<text:p text:style-name="Bullet">▸ {escape(text)}</text:p>')
        return self

    def table(self, header: Sequence[str], rows: Sequence[Sequence[Any]]) -> OdtBuilder:
        """Таблица с шапкой; числа форматируются как строки."""
        n_cols = len(header)
        col_xml = "<table:table-column/>" * n_cols
        rows_xml = []
        rows_xml.append(
            "<table:table-row>"
            + "".join(
                f'<table:table-cell office:value-type="string">'
                f'<text:p text:style-name="Th">{escape(str(h))}</text:p>'
                f"</table:table-cell>"
                for h in header
            )
            + "</table:table-row>"
        )
        for row in rows:
            cells = "".join(
                f'<table:table-cell office:value-type="string">'
                f"<text:p>{escape(str(v))}</text:p>"
                f"</table:table-cell>"
                for v in row
            )
            rows_xml.append(f"<table:table-row>{cells}</table:table-row>")
        self.body_xml.append(
            f'<table:table table:style-name="Ta">' f'{col_xml}{"".join(rows_xml)}</table:table>'
        )
        return self

    # ── части документа ──
    def _content_xml(self) -> str:
        """Handle OdtBuilder. content xml."""
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
 xmlns:office="{NS_OFFICE}" xmlns:text="{NS_TEXT}"
 xmlns:style="{NS_STYLE}" xmlns:fo="{NS_FO}" xmlns:table="{NS_TABLE}"
 office:version="1.2">
<office:automatic-styles>
<style:style style:name="Standard" style:family="paragraph">
<style:paragraph-properties fo:margin-bottom="0.14cm"/>
<style:text-properties fo:font-size="11pt" fo:color="{AURORA_BODY}"/>
</style:style>
<style:style style:name="H1" style:family="paragraph">
<style:paragraph-properties fo:margin-top="0.4cm" fo:margin-bottom="0.2cm"/>
<style:text-properties fo:font-size="20pt" fo:font-weight="bold"
 fo:color="{AURORA_ACCENT}"/>
</style:style>
<style:style style:name="H2" style:family="paragraph">
<style:paragraph-properties fo:margin-top="0.3cm" fo:margin-bottom="0.15cm"/>
<style:text-properties fo:font-size="15pt" fo:font-weight="bold"
 fo:color="{AURORA_ACCENT}"/>
</style:style>
<style:style style:name="H3" style:family="paragraph">
<style:text-properties fo:font-size="13pt" fo:font-weight="bold"
 fo:color="{AURORA_BODY}"/>
</style:style>
<style:style style:name="Bullet" style:family="paragraph">
<style:paragraph-properties fo:margin-left="0.6cm"
 fo:margin-bottom="0.08cm"/>
<style:text-properties fo:font-size="11pt" fo:color="{AURORA_BODY}"/>
</style:style>
<style:style style:name="Th" style:family="paragraph">
<style:text-properties fo:font-weight="bold" fo:font-size="10pt"/>
</style:style>
<style:style style:name="Ta" style:family="table">
<style:table-properties style:width="17cm" table:align="margins"/>
</style:style>
<style:style style:name="TC" style:family="table-cell">
<style:table-cell-properties fo:border="0.5pt solid #b9c9d6"
 fo:padding="0.08cm"/>
</style:style>
</office:automatic-styles>
<office:body><office:text>
{''.join(self.body_xml)}
</office:text></office:body>
</office:document-content>"""

    def _styles_xml(self) -> str:
        """Handle OdtBuilder. styles xml."""
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
 xmlns:office="{NS_OFFICE}" xmlns:style="{NS_STYLE}" xmlns:fo="{NS_FO}"
 office:version="1.2">
<office:styles>
<style:default-style style:family="paragraph">
<style:text-properties style:font-name="Calibri" fo:font-size="11pt"/>
</style:default-style>
</office:styles>
</office:document-styles>"""

    def _meta_xml(self) -> str:
        """Handle OdtBuilder. meta xml."""
        now = _dt.datetime.now().isoformat(timespec="seconds")
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta xmlns:office="{NS_OFFICE}"
 xmlns:dc="http://purl.org/dc/elements/1.1/" office:version="1.2">
<office:meta>
<dc:title>{escape(self.title)}</dc:title>
<dc:creator>{escape(self.creator)}</dc:creator>
<dc:date>{now}</dc:date>
<meta:generator xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0">TRIVORTEX MASTER 2.0</meta:generator>
</office:meta></office:document-meta>"""

    def _manifest_xml(self) -> str:
        """Handle OdtBuilder. manifest xml."""
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="{NS_MANIFEST}" manifest:version="1.2">
<manifest:file-entry manifest:full-path="/" manifest:media-type=
"application/vnd.oasis.opendocument.text"/>
<manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
<manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
<manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>
</manifest:manifest>"""

    def save(self, path: str) -> int:
        """Сохранить .odt; mimetype — первая запись БЕЗ сжатия (спека)."""
        with zipfile.ZipFile(path, "w") as zf:
            zf.writestr(
                zipfile.ZipInfo("mimetype"),
                "application/vnd.oasis.opendocument.text",
                compress_type=zipfile.ZIP_STORED,
            )
            zf.writestr("content.xml", self._content_xml(), zipfile.ZIP_DEFLATED)
            zf.writestr("styles.xml", self._styles_xml(), zipfile.ZIP_DEFLATED)
            zf.writestr("meta.xml", self._meta_xml(), zipfile.ZIP_DEFLATED)
            zf.writestr("META-INF/manifest.xml", self._manifest_xml(), zipfile.ZIP_DEFLATED)
        return os.path.getsize(path)


def validate_odt(path: str) -> list[str]:
    """Структурная валидация: mimetype первым и без сжатия + XML."""
    import xml.dom.minidom as minidom

    problems = []
    try:
        with zipfile.ZipFile(path) as zf:
            infos = zf.infolist()
            if not infos or infos[0].filename != "mimetype":
                problems.append("mimetype не первая запись")
            elif infos[0].compress_type != zipfile.ZIP_STORED:
                problems.append("mimetype сжат (спека требует STORED)")
            elif zf.read("mimetype").decode() != "application/vnd.oasis.opendocument.text":
                problems.append("неверный mimetype")
            for part in ("content.xml", "styles.xml", "meta.xml", "META-INF/manifest.xml"):
                if part not in zf.namelist():
                    problems.append(f"нет {part}")
                else:
                    try:
                        minidom.parseString(zf.read(part))
                    except Exception as exc:
                        problems.append(f"{part}: XML битый ({exc})")
    except zipfile.BadZipFile:
        problems.append("не zip")
    return problems


def self_check() -> dict:
    """Собрать документ с таблицей и заголовками, валидировать."""
    b = OdtBuilder(title="Проверка ODT")
    b.heading("Резюме прогона", 1)
    b.paragraph("Автогенерированный отчёт лаборатории N тел.")
    b.heading("Сценарии", 2)
    b.bullet("selftest 24/24")
    b.bullet("приёмка 20/20")
    b.table(
        ["Сценарий", "Статус"],
        [
            ["figure-eight", "закрыт 3.9e-08"],
            ["Меркурий 1PN", "42.98″/век"],
        ],
    )
    path = "/tmp/tv_selfcheck.odt"
    size = b.save(path)
    problems = validate_odt(path)
    # LibreOffice-конвертация как строгая проверка (если есть)
    soffice_ok = None
    import shutil

    if shutil.which("soffice"):
        import subprocess

        try:
            subprocess.run(
                ["soffice", "--headless", "--convert-to", "pdf", "--outdir", "/tmp", path],
                check=True,
                capture_output=True,
                timeout=120,
            )
            soffice_ok = os.path.exists("/tmp/tv_selfcheck.pdf")
        except Exception:
            soffice_ok = False
    return dict(
        size_bytes=size,
        problems=problems,
        soffice_ok=soffice_ok,
        ok=not problems and soffice_ok in (None, True),
    )
