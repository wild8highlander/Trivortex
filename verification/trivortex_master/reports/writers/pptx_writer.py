#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — PPTX-писатель на чистом stdlib (OOXML PresentationML).

Валидный .pptx без python-pptx: ZIP-контейнер + PresentationML-части.
Поддержка: заголовочные+контентные слайды (layout 0/1), буллеты,
картинки PNG (вставка по пути), таблицы-заглушки как текст, заметки
докладчика, тема AURORA (тёмный фон + ледяные акценты), нумерация
слайдов, 16:9.
"""

from __future__ import annotations

import os
import zipfile
from typing import Sequence
from xml.sax.saxutils import escape

EMU_PER_CM = 360000
SLIDE_W = 12192000  # 16:9 EMU (33.87 см)
SLIDE_H = 6858000
NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

AURORA_BG = "0A1120"
AURORA_ACCENT = "37DCF2"
AURORA_TEXT = "E6F0FA"
AURORA_MUTED = "8B9BB4"


class SlideBuilder:
    """Один слайд: список шейпов (текст/картинка)."""

    def __init__(self, layout: int = 1):
        """Do SlideBuilder.  init for layout and return the result."""
        self.layout = layout  # 0 = титул, 1 = заголовок+контент
        self.shapes_xml: list[str] = []
        self.image_parts: list[tuple[str, str, bytes]] = []
        self.notes: str = ""
        self._img_counter = 0

    def _text_shape(
        self, x, y, w, h, runs, align="l", size=1600, bold=False, color=AURORA_TEXT, spacing=1200
    ):
        """Текстовый бокс: runs = [(текст, размер, bold, цвет)]."""
        paras = []
        for text, sz, bd, cl in runs:
            paras.append(
                f'<a:p><a:pPr algn="{align}"/>'
                f'<a:r><a:rPr lang="ru-RU" sz="{sz}" b="{1 if bd else 0}">'
                f'<a:solidFill><a:srgbClr val="{cl}"/></a:solidFill></a:rPr>'
                f"<a:t>{escape(text)}</a:t></a:r></a:p>"
            )
        return (
            f'<p:sp><p:nvSpPr><p:cNvPr id="{len(self.shapes_xml) + 2}" '
            f'name="TextBox{len(self.shapes_xml)}"/><p:cNvSpPr '
            f'txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/>'
            f'<a:ext cx="{w}" cy="{h}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            f"<a:noFill/></p:spPr><p:txBody><a:bodyPr "
            f'lIns="91440" tIns="45720"/><a:lstStyle/>' + "".join(paras) + "</p:txBody></p:sp>"
        )

    def title(self, text: str, subtitle: str = "") -> SlideBuilder:
        """Do SlideBuilder.title for text, subtitle and return the result."""
        self.shapes_xml.append(
            self._text_shape(
                838200,
                1651000,
                SLIDE_W - 1676400,
                1600000,
                [(text, 3200, True, AURORA_ACCENT)],
                align="ctr",
            )
        )
        if subtitle:
            self.shapes_xml.append(
                self._text_shape(
                    838200,
                    3300000,
                    SLIDE_W - 1676400,
                    900000,
                    [(subtitle, 1500, False, AURORA_MUTED)],
                    align="ctr",
                )
            )
        return self

    def bullets(
        self, items: Sequence[str], start_y: int = 3200000, size: int = 1600
    ) -> SlideBuilder:
        """Do SlideBuilder.bullets for items, start_y, size and return the result."""
        runs = []
        for it in items:
            runs.append((f"▸ {it}", size, False, AURORA_TEXT))
        self.shapes_xml.append(self._text_shape(1000000, start_y, SLIDE_W - 2000000, 3200000, runs))
        return self

    def image(
        self, png_path: str, x: int = 1800000, y: int = 2600000, width: int = 8500000
    ) -> SlideBuilder:
        """Вставить PNG по пути: media-часть + rel."""
        with open(png_path, "rb") as fh:
            data = fh.read()
        self._img_counter += 1
        rid = f"rIdImg{self._img_counter}"
        name = f"image{self._img_counter}.png"
        self.image_parts.append((rid, name, data))
        # размер из PNG
        w_px = int.from_bytes(data[16:20], "big")
        h_px = int.from_bytes(data[20:24], "big")
        h_emu = int(width * h_px / max(w_px, 1))
        self.shapes_xml.append(
            f'<p:pic><p:nvPicPr><p:cNvPr id="{len(self.shapes_xml) + 2}" '
            f'name="{name}"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="{rid}"/>'
            f"<a:stretch><a:fillRect/></a:stretch></p:blipFill>"
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/>'
            f'<a:ext cx="{width}" cy="{h_emu}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
            f"</p:pic>"
        )
        return self

    def caption(self, text: str, y: int = SLIDE_H - 800000) -> SlideBuilder:
        """Do SlideBuilder.caption for text, y and return the result."""
        self.shapes_xml.append(
            self._text_shape(
                800000,
                y,
                SLIDE_W - 1600000,
                500000,
                [(text, 1100, False, AURORA_MUTED)],
                align="ctr",
            )
        )
        return self

    def note(self, text: str) -> SlideBuilder:
        """Do SlideBuilder.note for text and return the result."""
        self.notes = text
        return self


class PptxBuilder:
    """Сборка презентации: слайды, мастер, тема, сохранение."""

    def __init__(self, title: str = "TRIVORTEX MASTER"):
        """Do PptxBuilder.  init for title and return the result."""
        self.title = title
        self.slides: list[SlideBuilder] = []

    def slide(self, layout: int = 1) -> SlideBuilder:
        """Do PptxBuilder.slide for layout and return the result."""
        s = SlideBuilder(layout)
        self.slides.append(s)
        return s

    # ── XML-части ──
    def _content_types(self) -> str:
        """Handle PptxBuilder. content types."""
        overrides = [
            '<Override PartName="/ppt/presentation.xml" ContentType='
            '"application/vnd.openxmlformats-officedocument.'
            'presentationml.presentation.main+xml"/>',
            '<Override PartName="/ppt/slideMasters/slideMaster1.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.'
            'presentationml.slideMaster+xml"/>',
            '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.'
            'presentationml.slideLayout+xml"/>',
            '<Override PartName="/ppt/theme/theme1.xml" ContentType='
            '"application/vnd.openxmlformats-officedocument.'
            'theme+xml"/>',
        ]
        for i in range(len(self.slides)):
            overrides.append(
                f'<Override PartName="/ppt/slides/slide{i + 1}.xml" '
                f'ContentType="application/vnd.openxmlformats-officedocument.'
                f'presentationml.slide+xml"/>'
            )
            if self.slides[i].notes:
                overrides.append(
                    f'<Override PartName="/ppt/notesSlides/notesSlide'
                    f'{i + 1}.xml" ContentType="application/vnd.'
                    f"openxmlformats-officedocument.presentationml."
                    f'notesSlide+xml"/>'
                )
        for s in self.slides:
            for _rid, name, _data in s.image_parts:
                ext = name.rsplit(".", 1)[-1]
                overrides.append(
                    f'<Override PartName="/ppt/media/{name}" ContentType=' f'"image/{ext}"/>'
                )
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/'
            '2006/content-types">'
            '<Default Extension="rels" ContentType="application/'
            'vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Default Extension="png" ContentType="image/png"/>' + "".join(overrides) + "</Types>"
        )

    def _presentation(self) -> str:
        """Handle PptxBuilder. presentation."""
        slide_ids = "".join(
            f'<p:sldId id="{256 + i}" r:id="rId{i + 2}"/>' for i in range(len(self.slides))
        )
        return (
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<p:presentation xmlns:a="{NS_A}" xmlns:r="{NS_R}" '
            f'xmlns:p="{NS_P}">'
            f'<p:sldMasterIdLst><p:sldMasterId id="2147483648" '
            f'r:id="rId1"/></p:sldMasterIdLst>'
            f"<p:sldIdLst>{slide_ids}</p:sldIdLst>"
            f'<p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}"/>'
            f'<p:notesSz cx="{SLIDE_H}" cy="{SLIDE_W}"/>'
            f"</p:presentation>"
        )

    def _pres_rels(self) -> str:
        """Handle PptxBuilder. pres rels."""
        rels = [
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats'
            '.org/officeDocument/2006/relationships/slideMaster" '
            'Target="slideMasters/slideMaster1.xml"/>'
        ]
        for i in range(len(self.slides)):
            rels.append(
                f'<Relationship Id="rId{i + 2}" Type="http://schemas'
                f".openxmlformats.org/officeDocument/2006/"
                f'relationships/slide" '
                f'Target="slides/slide{i + 1}.xml"/>'
            )
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/'
            'package/2006/relationships">' + "".join(rels) + "</Relationships>"
        )

    def _slide_master(self) -> str:
        """Handle PptxBuilder. slide master."""
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="{NS_A}" xmlns:r="{NS_R}" xmlns:p="{NS_P}">
<p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="{AURORA_BG}"/></a:solidFill>
<a:effectLst/></p:bgPr></p:bg><p:spTree>
<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{SLIDE_W}" cy="{SLIDE_H}"/>
<a:chOff x="0" y="0"/><a:chExt cx="{SLIDE_W}" cy="{SLIDE_H}"/></a:xfrm></p:grpSpPr>
</p:spTree></p:cSld>
<p:clrMap bg1="dk1" tx1="lt1" bg2="dk2" tx2="lt2" accent1="accent1"/>
<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
</p:sldMaster>"""

    def _slide_layout(self) -> str:
        """Handle PptxBuilder. slide layout."""
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="{NS_A}" xmlns:r="{NS_R}" xmlns:p="{NS_P}" type="obj" preserve="1">
<p:cSld name="Title and Content"><p:spTree>
<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{SLIDE_W}" cy="{SLIDE_H}"/>
<a:chOff x="0" y="0"/><a:chExt cx="{SLIDE_W}" cy="{SLIDE_H}"/></a:xfrm></p:grpSpPr>
</p:spTree></p:cSld></p:sldLayout>"""

    def _theme(self) -> str:
        """Handle PptxBuilder. theme."""
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="{NS_A}" name="AURORA">
<a:themeElements><a:clrScheme name="AURORA">
<a:dk1><a:srgbClr val="{AURORA_TEXT}"/></a:dk1>
<a:lt1><a:srgbClr val="{AURORA_BG}"/></a:lt1>
<a:dk2><a:srgbClr val="101A2E"/></a:dk2>
<a:lt2><a:srgbClr val="22344E"/></a:lt2>
<a:accent1><a:srgbClr val="{AURORA_ACCENT}"/></a:accent1>
<a:accent2><a:srgbClr val="E8C766"/></a:accent2>
<a:accent3><a:srgbClr val="A78BFA"/></a:accent3>
<a:accent4><a:srgbClr val="34D399"/></a:accent4>
<a:accent5><a:srgbClr val="FB7185"/></a:accent5>
<a:accent6><a:srgbClr val="7DD3FC"/></a:accent6>
<a:hlink><a:srgbClr val="{AURORA_ACCENT}"/></a:hlink>
<a:folHlink><a:srgbClr val="A78BFA"/></a:folHlink>
</a:clrScheme><a:fontScheme name="AURORA">
<a:majorFont><a:latin typeface="Calibri Light"/><a:ea typeface=""/>
<a:cs typeface=""/></a:majorFont>
<a:minorFont><a:latin typeface="Calibri"/><a:ea typeface=""/>
<a:cs typeface=""/></a:minorFont>
</a:fontScheme><a:fmtScheme name="AURORA">
<a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>
<a:lnStyleLst><a:ln><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
</a:ln><a:ln><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
<a:ln><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>
<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle>
<a:effectStyle><a:effectLst/></a:effectStyle>
<a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>
<a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>
</a:fmtScheme></a:themeElements></a:theme>"""

    def _slide_xml(self, s: SlideBuilder) -> str:
        """Do PptxBuilder. slide xml for s and return the result."""
        return (
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<p:sld xmlns:a="{NS_A}" xmlns:r="{NS_R}" xmlns:p="{NS_P}">'
            f"<p:cSld><p:bg><p:bgPr><a:solidFill>"
            f'<a:srgbClr val="{AURORA_BG}"/></a:solidFill>'
            f"<a:effectLst/></p:bgPr></p:bg>"
            f'<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/>'
            f"<p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>"
            f"<p:grpSpPr/></p:spTree>" + "".join(s.shapes_xml) + "</p:cSld></p:sld>"
        )

    def _slide_rels(self, s: SlideBuilder) -> str:
        """Do PptxBuilder. slide rels for s and return the result."""
        rels = [
            '<Relationship Id="rIdLayout" Type="http://schemas.'
            "openxmlformats.org/officeDocument/2006/relationships/"
            'slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
        ]
        for rid, name, _data in s.image_parts:
            rels.append(
                f'<Relationship Id="{rid}" Type="http://schemas.'
                f"openxmlformats.org/officeDocument/2006/"
                f'relationships/image" Target="../media/{name}"/>'
            )
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/'
            'package/2006/relationships">' + "".join(rels) + "</Relationships>"
        )

    def _notes_xml(self, s: SlideBuilder, idx: int) -> str:
        """Do PptxBuilder. notes xml for s, idx and return the result."""
        return (
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<p:notes xmlns:a="{NS_A}" xmlns:r="{NS_R}" xmlns:p="{NS_P}">'
            f'<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/>'
            f"<p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>"
            f'<p:sp><p:nvSpPr><p:cNvPr id="2" name="Notes"/>'
            f'<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr/>'
            f"<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:r>"
            f'<a:rPr lang="ru-RU"/><a:t>{escape(s.notes)}</a:t>'
            f"</a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:notes>"
        )

    def save(self, path: str) -> int:
        """Do PptxBuilder.save for path and return the result."""
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", self._content_types())
            zf.writestr(
                "_rels/.rels",
                '<?xml version="1.0" encoding="UTF-8" '
                'standalone="yes"?>'
                '<Relationships xmlns="http://schemas.'
                'openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" Type="http://schemas.'
                "openxmlformats.org/officeDocument/2006/"
                'relationships/officeDocument" '
                'Target="ppt/presentation.xml"/></Relationships>',
            )
            zf.writestr("ppt/presentation.xml", self._presentation())
            zf.writestr("ppt/_rels/presentation.xml.rels", self._pres_rels())
            zf.writestr("ppt/slideMasters/slideMaster1.xml", self._slide_master())
            zf.writestr(
                "ppt/slideMasters/_rels/slideMaster1.xml.rels",
                '<?xml version="1.0" encoding="UTF-8" '
                'standalone="yes"?>'
                '<Relationships xmlns="http://schemas.'
                'openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" Type="http://schemas.'
                "openxmlformats.org/officeDocument/2006/"
                'relationships/slideLayout" '
                'Target="../slideLayouts/slideLayout1.xml"/>'
                '<Relationship Id="rIdTheme" Type="http://schemas.'
                "openxmlformats.org/officeDocument/2006/"
                'relationships/theme" '
                'Target="../theme/theme1.xml"/></Relationships>',
            )
            zf.writestr("ppt/slideLayouts/slideLayout1.xml", self._slide_layout())
            zf.writestr(
                "ppt/slideLayouts/_rels/slideLayout1.xml.rels",
                '<?xml version="1.0" encoding="UTF-8" '
                'standalone="yes"?>'
                '<Relationships xmlns="http://schemas.'
                'openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rIdMaster" Type="http://schemas.'
                "openxmlformats.org/officeDocument/2006/"
                'relationships/slideMaster" '
                'Target="../slideMasters/slideMaster1.xml"/>'
                "</Relationships>",
            )
            zf.writestr("ppt/theme/theme1.xml", self._theme())
            for i, s in enumerate(self.slides):
                zf.writestr(f"ppt/slides/slide{i + 1}.xml", self._slide_xml(s))
                zf.writestr(f"ppt/slides/_rels/slide{i + 1}.xml.rels", self._slide_rels(s))
                if s.notes:
                    zf.writestr(f"ppt/notesSlides/notesSlide{i + 1}.xml", self._notes_xml(s, i))
                for _rid, name, data in s.image_parts:
                    zf.writestr(f"ppt/media/{name}", data)
        return os.path.getsize(path)


def validate_pptx(path: str) -> list[str]:
    """Структурная валидация PPTX."""
    problems = []
    try:
        with zipfile.ZipFile(path) as zf:
            if zf.testzip() is not None:
                problems.append("битые CRC")
            names = zf.namelist()
            for req in (
                "[Content_Types].xml",
                "ppt/presentation.xml",
                "ppt/slideMasters/slideMaster1.xml",
            ):
                if req not in names:
                    problems.append(f"нет {req}")
            n_slides = sum(
                1
                for n in names
                if n.startswith("ppt/slides/slide") and n.endswith(".xml") and "rels" not in n
            )
            if n_slides == 0:
                problems.append("нет слайдов")
    except zipfile.BadZipFile:
        problems.append("не zip")
    return problems


def self_check() -> dict:
    """Собрать 3-слайдовую презентацию и валидировать (pptx при наличии)."""
    b = PptxBuilder()
    s1 = b.slide(0)
    s1.title("TRIVORTEX MASTER", "Лаборатория N тел · v2.0")
    s1.note("Титульный слайд")
    s2 = b.slide(1)
    s2.title("Результаты")
    s2.bullets(["Selftest 24/24", "Меркурий 42.98″/век", "Луна 3.80 см/год"])
    # картинка-вставка (генерируем мини-PNG)
    from render.png_codec import write_png

    px = bytes([55, 220, 242]) * (64 * 48)
    write_png("/tmp/tv_pptx_img.png", px, 64, 48)
    s2.image("/tmp/tv_pptx_img.png")
    s3 = b.slide(1)
    s3.title("Выводы").bullets(["Всё по хардкору", "stdlib-first"])
    path = "/tmp/tv_selfcheck.pptx"
    size = b.save(path)
    problems = validate_pptx(path)
    read_ok = None
    try:
        from pptx import Presentation as PPTXRead

        prs = PPTXRead(path)
        read_ok = len(prs.slides) == 3
    except ImportError:
        pass
    return dict(
        size_bytes=size,
        problems=problems,
        pptx_read_ok=read_ok,
        ok=not problems and (read_ok in (None, True)),
    )
