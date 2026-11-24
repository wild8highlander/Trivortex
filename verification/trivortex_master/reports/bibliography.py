#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Программный доступ к списку литературы data/literature.md.

Парсит 21 позицию по заголовкам-номерам, отдаёт структурированно для
отчётов (раздел «Источники») и меню справки.
"""

from __future__ import annotations

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data", "literature.md")


def load_entries() -> list[dict]:
    """[(номер, текст, url)] — по строкам вида «N. **...**»."""
    if not os.path.isfile(PATH):
        return []
    entries = []
    current = None
    with open(PATH, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"^(\d+)\.\s+\*\*(.+?)\*\*\s*(.*)$", line.strip())
            if m:
                if current:
                    entries.append(current)
                current = dict(num=int(m.group(1)), text=m.group(2), rest=m.group(3), url=None)
                continue
            if current is not None:
                mu = re.search(r"<(https?://[^>]+)>", line)
                if mu and current["url"] is None:
                    current["url"] = mu.group(1)
    if current:
        entries.append(current)
    return entries


def as_table_rows() -> list[list[str]]:
    """Строки для ReportData.add_table."""
    return [[str(e["num"]), e["text"][:60], e["url"] or "—"] for e in load_entries()]


def count() -> int:
    """Handle count."""
    return len(load_entries())
