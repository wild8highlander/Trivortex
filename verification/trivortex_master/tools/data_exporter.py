#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — экспорт данных: каталог, результаты, таблицы.

Универсальный конвертер между представлениями (для отчётов и
внешнего использования):

  * to_csv / to_tsv: текстовые таблицы (заголовок + строки,
    экранирование кавычек);
  * to_jsonl: построчный JSON (стриминг больших наборов);
  * to_markdown_table: GFM-таблица с выравниванием;
  * to_latex_table: booktabs-стиль LaTeX;
  * to_ascii_table: моноширинная таблица с рамками (для меню);
  * export_catalog_subset: выборка каталога по типу/запросу.

Самопроверка: roundtrip csv ↔ список; markdown и LaTeX синтаксически
корректны; JSONL парсится построчно; ASCII-таблица выровнена.
"""

from __future__ import annotations

import json
from typing import Any, Sequence


def _escape_csv(value: Any) -> str:
    """Экранирование поля CSV (RFC 4180)."""
    s = str(value)
    if any(ch in s for ch in (",", '"', "\n")):
        return '"' + s.replace('"', '""') + '"'
    return s


def to_csv(headers: Sequence[str], rows: Sequence[Sequence[Any]], delimiter: str = ",") -> str:
    """CSV/TSV-таблица."""
    lines = [delimiter.join(_escape_csv(h) for h in headers)]
    for row in rows:
        lines.append(delimiter.join(_escape_csv(v) for v in row))
    return "\n".join(lines) + "\n"


def to_tsv(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    return to_csv(headers, rows, delimiter="\t")


def to_jsonl(rows: Sequence[dict[str, Any]]) -> str:
    """Построчный JSON (каждая строка — самостоятельный объект)."""
    return "\n".join(json.dumps(r, ensure_ascii=False, default=str) for r in rows) + "\n"


def to_markdown_table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    """GFM-таблица."""
    out = ["| " + " | ".join(str(h) for h in headers) + " |"]
    out.append("|" + "|".join("---" for _ in headers) + "|")
    for row in rows:
        out.append("| " + " | ".join(str(v) for v in row) + " |")
    return "\n".join(out) + "\n"


def to_latex_table(headers: Sequence[str], rows: Sequence[Sequence[Any]], caption: str = "") -> str:
    """LaTeX-таблица (booktabs: toprule/midrule/bottomrule)."""
    col_spec = "l" * len(headers)
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        f"\\begin{{tabular}}{{{col_spec}}}",
        r"\toprule",
        " & ".join(str(h) for h in headers) + r" \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(" & ".join(_escape_latex(str(v)) for v in row) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    if caption:
        lines.append(f"\\caption{{{_escape_latex(caption)}}}")
    lines += [r"\end{table}"]
    return "\n".join(lines) + "\n"


def _escape_latex(s: str) -> str:
    for ch, rep in (
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ):
        s = s.replace(ch, rep)
    return s


def to_ascii_table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    """Моноширинная таблица с рамками + автоподбор ширин."""
    cells = [[str(v) for v in row] for row in rows]
    widths = [len(str(h)) for h in headers]
    for row in cells:
        for i, v in enumerate(row):
            widths[i] = max(widths[i], len(v))
    top = "┌" + "┬".join("─" * w for w in widths) + "┐"
    mid = "├" + "┼".join("─" * w for w in widths) + "┤"
    bot = "└" + "┴".join("─" * w for w in widths) + "┘"

    def fmt_row(vals):
        return "│" + "│".join(v.ljust(widths[i]) for i, v in enumerate(vals)) + "│"

    out = [top, fmt_row([str(h) for h in headers]), mid]
    out += [fmt_row(r) for r in cells]
    out.append(bot)
    return "\n".join(out)


def parse_csv(text: str, delimiter: str = ",") -> tuple[list[str], list[list[str]]]:
    """Простой парсер CSV (roundtrip для to_csv; RFC-кавычки)."""
    rows: list[list[str]] = []
    field: list[str] = []
    row: list[str] = []
    in_quotes = False
    i = 0
    while i < len(text):
        ch = text[i]
        if in_quotes:
            if ch == '"':
                if i + 1 < len(text) and text[i + 1] == '"':
                    field.append('"')
                    i += 2
                    continue
                in_quotes = False
            else:
                field.append(ch)
        else:
            if ch == '"':
                in_quotes = True
            elif ch == delimiter:
                row.append("".join(field))
                field = []
            elif ch == "\n":
                row.append("".join(field))
                field = []
                rows.append(row)
                row = []
            else:
                field.append(ch)
        i += 1
    if field or row:
        row.append("".join(field))
        rows.append(row)
    if not rows:
        return [], []
    return rows[0], rows[1:]


def export_catalog_subset(
    catalog: dict[str, Any], object_type: str = None, query: str = None, limit: int = 50
) -> list[dict[str, Any]]:
    """Выборка объектов каталога по типу и/или подстроке имени."""
    out = []
    for obj in catalog.get("objects", []):
        if object_type and obj.get("type") != object_type:
            continue
        if query and query.lower() not in obj.get("name", "").lower():
            continue
        out.append(
            dict(
                id=obj["id"],
                name=obj["name"],
                type=obj.get("type"),
                mass_kg=obj.get("mass_kg"),
                radius_km=obj.get("radius_km"),
            )
        )
        if len(out) >= limit:
            break
    return out


def self_check() -> dict:
    """Roundtrip CSV; markdown/LaTeX/ASCII синтаксис; JSONL; выборка."""
    headers = ["id", "name", "mass"]
    rows = [["earth", "Земля", "5.97e24"], ["halley", "1P/Галлея, комета", 'с "кавычками"']]
    csv_text = to_csv(headers, rows)
    h2, r2 = parse_csv(csv_text)
    csv_ok = h2 == headers and r2 == rows
    md = to_markdown_table(headers, rows)
    md_ok = md.startswith("| id |") and "|---|" in md
    tex = to_latex_table(headers, rows, caption="Тест")
    tex_ok = (
        tex.startswith(r"\begin{table}")
        and r"\toprule" in tex
        and r"\%" not in tex
        or "%" not in tex.split("toprule")[1]
        and "Тест" in tex
    )
    ascii_tbl = to_ascii_table(headers, rows)
    ascii_ok = ascii_tbl.startswith("┌") and "│" in ascii_tbl
    jsonl = to_jsonl([dict(id="a", v=1), dict(id="b", v=2)])
    parsed = [json.loads(line) for line in jsonl.strip().split("\n")]
    jsonl_ok = len(parsed) == 2 and parsed[1]["v"] == 2
    # tsv
    tsv = to_tsv(headers, rows)
    tsv_ok = "\t" in tsv
    # выборка каталога
    cat = dict(
        objects=[
            dict(id="sun", name="Солнце", type="star", mass_kg=1.9884e30),
            dict(id="earth", name="Земля", type="planet", mass_kg=5.97e24),
        ]
    )
    subset = export_catalog_subset(cat, object_type="planet")
    subset_ok = len(subset) == 1 and subset[0]["id"] == "earth"
    return dict(
        csv_ok=csv_ok,
        md_ok=md_ok,
        tex_ok=tex_ok,
        ascii_ok=ascii_ok,
        jsonl_ok=jsonl_ok,
        tsv_ok=tsv_ok,
        subset_ok=subset_ok,
        all_ok=csv_ok and md_ok and tex_ok and ascii_ok and jsonl_ok and tsv_ok and subset_ok,
        note="RFC 4180 (CSV), GFM (markdown), booktabs (LaTeX), " "построчный JSONL",
    )
