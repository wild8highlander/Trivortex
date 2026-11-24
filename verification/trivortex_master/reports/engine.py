#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — движок отчётов: 7 форматов из одного ReportData.

TXT · MD · HTML · CSV · JSON · DOCX · PDF

Один прогон — один набор отчётов: ReportData собирает снимок конфигурации,
сводку сцены, таблицы тел, метрики, пути к графикам (PNG в base64 для HTML),
генеалогию прогона. Каждый формат пишет честно: DOCX/PDF — собственные
stdlib-писатели (writers/), HTML — темы AURORA/ICE/MINIMAL.
"""

from __future__ import annotations

import datetime as _dt
import html as _html
import json
import os
from typing import Any

from reports import templates
from reports.charts import ascii_table


# ═══════════════════════════════════════════════════════════════════════════
# ReportData
# ═══════════════════════════════════════════════════════════════════════════
class ReportData:
    """Всё, что попадает в отчёты: сцена, метрики, графики, генеалогия."""

    def __init__(
        self,
        title: str,
        scene=None,
        sim_summary: dict | None = None,
        config=None,
        extra_sections: list[tuple[str, str]] | None = None,
    ):
        """Do ReportData.  init for title, scene, sim_summary, config and return the result."""
        self.title = title
        self.generated = _dt.datetime.now().isoformat(timespec="seconds")
        self.scene = scene
        self.sim_summary = sim_summary or {}
        self.config = config
        self.extra_sections = extra_sections or []
        self.charts: list[tuple[str, str]] = []  # (путь к PNG, подпись)
        self.cards: list[tuple[str, str, str]] = []  # (ключ, значение, класс)
        self.tables: list[tuple[str, list[str], list[list]]] = []  # (имя, headers, rows)
        self.unphysical_note: str | None = None
        self.run_dir: str | None = None
        self.versions = dict(master="2.0.0")

    def add_card(self, key: str, value: str, cls: str = "info") -> ReportData:
        """Do ReportData.add card for key, value and return the result."""
        self.cards.append((key, value, cls))
        return self

    def add_table(self, name: str, headers: list[str], rows: list[list]) -> ReportData:
        """Do ReportData.add table for name, headers, rows and return the result."""
        self.tables.append((name, headers, rows))
        return self

    def add_chart(self, path: str, caption: str = "") -> ReportData:
        """Do ReportData.add chart for path, caption and return the result."""
        if os.path.isfile(path):
            self.charts.append((path, caption))
        return self

    # ── сводка сцены ──
    def fill_from_scene(self) -> ReportData:
        """Handle ReportData.fill from scene."""
        if self.scene is None:
            return self
        sc = self.scene
        self.add_card("тел в сцене", str(sc.n), "bad" if sc.unphysical_flag else "info")
        self.add_card("движок", sc.engine_name or "—")
        self.add_card("t конечное", f"{sc.t:.4g}")
        if sc.unphysical_flag:
            self.unphysical_note = (
                "N=8: конфигурация вне физической вселенной модели. "
                "Порог Хавелока (POLYVORTEX W4): вихревое кольцо устойчиво "
                "при N≤7, при N=8 max Re λ = +0.4502 — резкий скачок "
                "неустойчивости."
            )
        # таблица тел
        rows = [
            [b.name, b.type, f"{b.mass:.3g}", f"{b.radius:.3g}", b.source[:44]] for b in sc.bodies
        ]
        self.add_table("Тела сцены", ["Имя", "Тип", "Масса, кг", "Радиус, м", "Источник"], rows)
        # события
        if sc.events:
            ev_rows = [
                [e["kind"], f"{e.get('t', 0):.3g}", e["detail"][:60]] for e in sc.events[-15:]
            ]
            self.add_table("События прогонов", ["Тип", "t", "Детали"], ev_rows)
        return self

    def to_dict(self) -> dict[str, Any]:
        """Handle ReportData.to dict."""
        return dict(
            title=self.title,
            generated=self.generated,
            versions=self.versions,
            sim_summary=self.sim_summary,
            cards=[dict(k=k, v=v, cls=c) for k, v, c in self.cards],
            tables=[dict(name=n, headers=h, rows=r) for n, h, r in self.tables],
            unphysical_note=self.unphysical_note,
            charts=[dict(path=p, caption=c) for p, c in self.charts],
            extra_sections=self.extra_sections,
            run_dir=self.run_dir,
        )


# ═══════════════════════════════════════════════════════════════════════════
# Писатели форматов
# ═══════════════════════════════════════════════════════════════════════════
def write_txt(data: ReportData, path: str) -> str:
    """Write write txt to the given target."""
    L = []
    L.append("=" * 72)
    L.append(" TRIVORTEX MASTER — " + data.title)
    L.append(" сгенерировано: " + data.generated)
    L.append("=" * 72)
    if data.unphysical_note:
        L.append("\n!! ВНИМАНИЕ: " + data.unphysical_note)
    L.append("")
    L.append("СВОДКА")
    for k, v, _c in data.cards:
        L.append(f"  {k:<28} {v}")
    if data.sim_summary:
        L.append("")
        L.append("ПАРАМЕТРЫ ПРОГОНА")
        for k, v in data.sim_summary.items():
            L.append(f"  {k:<28} {v}")
    for name, headers, rows in data.tables:
        L.append("")
        L.append(name.upper())
        L.append(ascii_table(headers, rows))
    for heading, content in data.extra_sections:
        L.append("")
        L.append(heading.upper())
        L.append(content)
    L.append("")
    L.append("TRIVORTEX MASTER v" + data.versions["master"])
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    return path


def write_md(data: ReportData, path: str) -> str:
    """Write write md to the given target."""
    L = [f"# TRIVORTEX MASTER — {data.title}", "", f"*сгенерировано: {data.generated}*", ""]
    if data.unphysical_note:
        L += [f"> ⚠️ **{data.unphysical_note}**", ""]
    L.append("## Сводка")
    L.append("| Параметр | Значение |")
    L.append("|---|---|")
    for k, v, _c in data.cards:
        L.append(f"| {k} | {v} |")
    if data.sim_summary:
        L += [
            "",
            "## Прогон",
            "```json",
            json.dumps(data.sim_summary, ensure_ascii=False, indent=1, default=str),
            "```",
        ]
    for name, headers, rows in data.tables:
        L += ["", f"## {name}", "| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
        for r in rows:
            L.append("| " + " | ".join(str(c) for c in r) + " |")
    for p, cap in data.charts:
        rel = os.path.relpath(p, os.path.dirname(path)) if data.run_dir else os.path.basename(p)
        L += ["", f"![{cap}]({rel})", f"*{cap}*" if cap else ""]
    for heading, content in data.extra_sections:
        L += ["", f"## {heading}", content]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    return path


def write_html(data: ReportData, path: str, theme: str = "aurora") -> str:
    """Write write html to the given target."""
    sections = []
    # карточки
    if data.cards:
        sections.append(templates.html_section("Сводка", templates.html_cards(data.cards)))
    # плашка N=8
    if data.unphysical_note:
        sections.append(
            templates.html_plate("Вне физической вселенной модели", data.unphysical_note)
        )
    # таблицы
    for name, headers, rows in data.tables:
        sections.append(templates.html_section(name, templates.html_table(headers, rows)))
    # графики в base64
    if data.charts:
        imgs = []
        for p, cap in data.charts:
            imgs.append(templates.html_image(p, cap))
            if cap:
                imgs.append(f'<div class="meta">{_html.escape(cap)}</div>')
        sections.append(templates.html_section("Графики", "".join(imgs)))
    # параметры прогона
    if data.sim_summary:
        rows = [[k, str(v)] for k, v in data.sim_summary.items()]
        sections.append(
            templates.html_section(
                "Параметры прогона", templates.html_table(["Параметр", "Значение"], rows)
            )
        )
    for heading, content in data.extra_sections:
        sections.append(templates.html_section(heading, f"<p>{_html.escape(content)}</p>"))
    banner = (
        "████████╗██╗ ██████╗ ████████╗\n"
        "╚══██╔══╝██║██╔════╝ ╚══██╔══╝\n"
        "   ██║   ██║██║        ██║\n"
        "   ██║   ██║██║        ██║\n"
        "   ██║   ██║╚██████╗   ██║\n"
        "   ╚═╝   ╚═╝ ╚═════╝   ╚═╝"
    )
    page = templates.html_page(
        title=_html.escape(data.title),
        subtitle=f"сгенерировано {data.generated} · " f"движок отчётов v{data.versions['master']}",
        body="\n".join(sections),
        theme=theme,
        version=data.versions["master"],
        banner=banner,
    )
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(page)
    return path


def write_csv(data: ReportData, path: str) -> str:
    """Write write csv to the given target."""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("section,key,value\n")
        for k, v, _c in data.cards:
            fh.write(f'summary,"{k}","{v}"\n')
        for k, v in data.sim_summary.items():
            fh.write(f'run,"{k}","{v}"\n')
        for name, headers, rows in data.tables:
            for r in rows:
                fh.write(f'{name},"' + '","'.join(str(c) for c in r) + '"\n')
    return path


def write_json(data: ReportData, path: str) -> str:
    """Write write json to the given target."""
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data.to_dict(), fh, ensure_ascii=False, indent=1, default=str)
    return path


def write_docx(data: ReportData, path: str) -> str:
    """Write write docx to the given target."""
    from reports.writers.docx_writer import DocxBuilder

    doc = DocxBuilder(title=data.title)
    doc.paragraph(f"сгенерировано: {data.generated}", italic=True, color="5A6B7D", size_half_pt=18)
    if data.unphysical_note:
        doc.paragraph("ВНИМАНИЕ: " + data.unphysical_note, bold=True, color="C25B6A")
    doc.heading("Сводка", 1)
    for k, v, _c in data.cards:
        doc.bullet(f"{k}: {v}")
    if data.sim_summary:
        doc.heading("Параметры прогона", 1)
        doc.table(["Параметр", "Значение"], [[k, str(v)] for k, v in data.sim_summary.items()])
    for name, headers, rows in data.tables:
        doc.heading(name, 2)
        doc.table(headers, rows)
    for p, _cap in data.charts:
        doc.image(p)
    for heading, content in data.extra_sections:
        doc.heading(heading, 2)
        doc.paragraph(content)
    doc.save(path)
    return path


def write_pdf(data: ReportData, path: str) -> str:
    """Write write pdf to the given target."""
    from reports.writers.pdf_writer import PDFBuilder, A4_W

    pdf = PDFBuilder(title=data.title)
    y = pdf.page.heading(data.title, A4_W and 780, level=1)
    y = pdf.page.wrap_text(f"generated: {data.generated}", 56, y, size=9, color=(0.35, 0.42, 0.49))
    if data.unphysical_note:
        pdf.page.rect(56, y - 16, A4_W - 112, 34, fill=(0.24, 0.07, 0.13))
        y = pdf.page.wrap_text(
            "ATTENTION: " + data.unphysical_note, 62, y - 6, size=8.5, color=(0.98, 0.79, 0.83)
        )
    y -= 10
    pdf.page.text(56, y, "Summary", size=12.5, bold=True)
    y -= 18
    for k, v, _c in data.cards:
        pdf.page.text(62, y, f"- {k}: {v}", size=9.5)
        y -= 13
        if y < 70:
            y = pdf.new_page().heading("", 800, 2) and 780
    if data.sim_summary:
        y -= 8
        pdf.page.text(56, y, "Run parameters", size=12.5, bold=True)
        y -= 16
        rows = [[k, str(v)] for k, v in data.sim_summary.items()]
        y = pdf.page.table(["Parameter", "Value"], rows, y, col_w=[220, A4_W - 112 - 220])
    for name, headers, rows in data.tables:
        y -= 10
        if y < 160:
            y = pdf.new_page().heading(name, 780, 2)
        else:
            pdf.page.text(56, y, name, size=12.5, bold=True)
            y -= 16
        y = pdf.page.table(headers, rows, y)
    for heading, content in data.extra_sections:
        y -= 8
        if y < 120:
            y = pdf.new_page().heading(heading, 780, 2) or 750
            y = 750
        else:
            pdf.page.text(56, y, heading, size=12.5, bold=True)
            y -= 16
        y = pdf.page.wrap_text(content, 56, y, width_chars=98, size=9.5)
    pdf.save(path)
    return path


def write_odt(data: ReportData, path: str) -> str:
    """Отчёт ODT (OpenDocument): cards, таблицы, секции — как в docx."""
    from reports.writers.odt_writer import OdtBuilder

    b = OdtBuilder(title=data.title)
    b.heading(data.title, 1)
    b.paragraph(f"generated: {data.generated}")
    if data.unphysical_note:
        b.paragraph("ATTENTION: " + data.unphysical_note, style="H3")
    b.heading("Сводка", 2)
    b.table(["Параметр", "Значение"], [[k, v] for k, v, _cls in data.cards])
    for name, headers, rows in data.tables:
        b.heading(name, 3)
        b.table(headers, rows)
    for title, text in data.extra_sections:
        b.heading(title, 2)
        for paragraph in text.split("\n\n"):
            if paragraph.strip():
                b.paragraph(paragraph.strip())
    for _path, caption in data.charts:
        b.paragraph(f"[график: {caption or _path}]", style="Bullet")
    b.save(path)
    return path


# ═══════════════════════════════════════════════════════════════════════════
# Оркестратор
# ═══════════════════════════════════════════════════════════════════════════
WRITERS = {
    "txt": write_txt,
    "md": write_md,
    "html": write_html,
    "csv": write_csv,
    "json": write_json,
    "docx": write_docx,
    "pdf": write_pdf,
    "odt": write_odt,
}


def generate_reports(
    data: ReportData,
    output_dir: str,
    formats: list[str] | None = None,
    theme: str = "aurora",
    stem: str = "report",
) -> dict[str, str]:
    """Сгенерировать отчёт во всех запрошенных форматах."""
    formats = formats or ["md", "html", "json"]
    os.makedirs(output_dir, exist_ok=True)
    data.run_dir = output_dir
    written: dict[str, str] = {}
    for fmt in formats:
        fmt = fmt.lower()
        writer = WRITERS.get(fmt)
        if writer is None:
            continue
        path = os.path.join(output_dir, f"{stem}.{fmt}")
        try:
            if fmt == "html":
                writer(data, path, theme=theme)
            else:
                writer(data, path)
            written[fmt] = path
        except Exception as exc:  # один формат не должен валить остальные
            written[fmt] = f"ОШИБКА: {exc}"
    return written


def validate_outputs(written: dict[str, str]) -> list[str]:
    """Проверка файлов: существование, размер, валидность docx/pdf."""
    from reports.writers.docx_writer import validate_docx
    from reports.writers.pdf_writer import validate_pdf

    problems = []
    for fmt, path in written.items():
        if path.startswith("ОШИБКА"):
            problems.append(f"[{fmt}] {path}")
            continue
        if not os.path.isfile(path) or os.path.getsize(path) == 0:
            problems.append(f"[{fmt}] файл пуст или отсутствует: {path}")
            continue
        if fmt == "docx":
            problems += [f"[docx] {p}" for p in validate_docx(path)]
        if fmt == "odt":
            from reports.writers.odt_writer import validate_odt

            problems += [f"[odt] {p}" for p in validate_odt(path)]
        if fmt == "pdf":
            problems += [f"[pdf] {p}" for p in validate_pdf(path)]
    return problems
