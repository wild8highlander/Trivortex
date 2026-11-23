#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIVORTEX MASTER — шаблоны отчётов: string.Template.

Три темы: AURORA (тёмная, градиенты, карточки — по умолчанию), ICE (светлая,
голубые акценты, печать), MINIMAL (ч/б, архивация). PNG-графики встраиваются
в base64 — HTML самодостаточен для отправки.
"""

from __future__ import annotations

import base64
import datetime as _dt
from string import Template

# ═══════════════════════════════════════════════════════════════════════════
# Общие CSS-темы
# ═══════════════════════════════════════════════════════════════════════════
_CSS = {
    "aurora": """
    :root {
      --bg: #0A1120; --panel: #101A2E; --panel2: #0E1B2E;
      --text: #E6F0FA; --muted: #8B9BB4; --accent: #37DCF2;
      --gold: #E8C766; --green: #34D399; --red: #FB7185; --violet: #A78BFA;
      --border: #22344E;
    }
    body { background: var(--bg); color: var(--text);
           font-family: 'Segoe UI', system-ui, sans-serif; margin: 0;
           padding: 24px; line-height: 1.55; }
    .wrap { max-width: 1060px; margin: 0 auto; }
    header { text-align: center; padding: 28px 16px;
             background: linear-gradient(135deg, #101A2E 0%, #16263D 55%, #1B2B45 100%);
             border: 1px solid var(--border); border-radius: 14px; margin-bottom: 22px; }
    header h1 { margin: 0 0 6px; font-size: 26px;
                background: linear-gradient(90deg, #7DD3FC, #E8C766);
                -webkit-background-clip: text; background-clip: text;
                color: transparent; }
    header .sub { color: var(--muted); font-size: 13px; }
    .banner { font-family: 'Courier New', monospace; white-space: pre;
              color: #37DCF2; font-size: 11px; line-height: 1.15;
              text-align: left; display: inline-block; margin: 8px 0; }
    section { background: var(--panel); border: 1px solid var(--border);
              border-radius: 12px; padding: 18px 20px; margin-bottom: 18px; }
    h2 { color: var(--accent); font-size: 17px; margin: 0 0 10px;
         border-bottom: 1px solid var(--border); padding-bottom: 6px; }
    h3 { color: var(--violet); font-size: 14px; margin: 14px 0 6px; }
    table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
    th { background: #1B6B7A; color: #fff; text-align: left;
         padding: 7px 9px; }
    td { padding: 6px 9px; border-bottom: 1px solid var(--border); }
    tr:nth-child(even) td { background: #0E1B2E; }
    .cards { display: flex; flex-wrap: wrap; gap: 12px; margin: 10px 0; }
    .card { flex: 1 1 180px; background: var(--panel2);
            border: 1px solid var(--border); border-radius: 10px;
            padding: 12px 14px; }
    .card .k { color: var(--muted); font-size: 11px; text-transform: uppercase;
               letter-spacing: 0.5px; }
    .card .v { font-size: 21px; font-weight: 600; margin-top: 2px; }
    .v.good { color: var(--green); } .v.warn { color: var(--gold); }
    .v.bad { color: var(--red); } .v.info { color: var(--accent); }
    .plate { background: #3B1220; border: 1px solid var(--red);
             border-radius: 10px; padding: 12px 16px; color: #FFC9D4;
             margin: 12px 0; }
    .ok { color: var(--green); } .warn { color: var(--gold); }
    .err { color: var(--red); }
    img.chart { max-width: 100%; border-radius: 8px; margin: 8px 0;
                border: 1px solid var(--border); }
    .meta { color: var(--muted); font-size: 12px; }
    footer { text-align: center; color: var(--muted); font-size: 11px;
             padding: 14px; }
    code { background: #0A1424; border: 1px solid var(--border);
           border-radius: 4px; padding: 1px 5px; font-size: 12px; }
    """,
    "ice": """
    body { background: #FFFFFF; color: #1A2B40; font-family: 'Segoe UI',
           system-ui, sans-serif; margin: 0; padding: 24px; line-height: 1.55; }
    .wrap { max-width: 1000px; margin: 0 auto; }
    header { border-bottom: 3px solid #1B6B7A; padding: 14px 0 12px;
             margin-bottom: 20px; }
    header h1 { color: #134252; margin: 0 0 4px; font-size: 24px; }
    section { margin-bottom: 16px; }
    h2 { color: #1B6B7A; font-size: 17px; border-bottom: 1px solid #C8DDE2;
         padding-bottom: 5px; }
    table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
    th { background: #EDF3F5; color: #134252; text-align: left; padding: 7px 9px;
         border-bottom: 2px solid #1B6B7A; }
    td { padding: 6px 9px; border-bottom: 1px solid #E4EDEF; }
    .cards { display: flex; flex-wrap: wrap; gap: 12px; }
    .card { flex: 1 1 180px; border: 1px solid #C8DDE2; border-radius: 8px;
            padding: 10px 12px; }
    .card .k { color: #5A6B7D; font-size: 11px; }
    .card .v { font-size: 20px; font-weight: 600; color: #134252; }
    .plate { border: 1px solid #C25B6A; background: #FDF1F3; padding: 10px 14px;
             border-radius: 8px; }
    img.chart { max-width: 100%; }
    footer { color: #5A6B7D; font-size: 11px; text-align: center;
             padding: 12px; }
    """,
    "minimal": """
    body { background: #fff; color: #000; font-family: Georgia, serif;
           margin: 0; padding: 24px; max-width: 900px; }
    header { border-bottom: 2px solid #000; padding-bottom: 10px;
             margin-bottom: 18px; }
    h1 { font-size: 22px; } h2 { font-size: 16px; }
    table { width: 100%; border-collapse: collapse; font-size: 12px; }
    th, td { border: 1px solid #999; padding: 5px 8px; text-align: left; }
    .card { border: 1px solid #999; padding: 8px; margin: 4px; display:
             inline-block; }
    footer { border-top: 1px solid #999; margin-top: 20px; font-size: 11px; }
    """,
}


def _b64(png_path: str) -> str:
    with open(png_path, "rb") as fh:
        return base64.b64encode(fh.read()).decode("ascii")


# ═══════════════════════════════════════════════════════════════════════════
# Каркас страницы
# ═══════════════════════════════════════════════════════════════════════════
PAGE = Template("""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title — TRIVORTEX MASTER</title>
<style>$css
@media print { body { background: #fff; color: #000; } }
</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="banner">$banner</div>
  <h1>$title</h1>
  <div class="sub">$subtitle</div>
</header>
$body
<footer>
  TRIVORTEX MASTER v$version · сгенерировано $generated ·
  формат: HTML/$theme
</footer>
</div>
</body>
</html>""")

SECTION = Template("""<section>
<h2>$heading</h2>
$content
</section>""")

CARDS = Template("""<div class="cards">
$cards
</div>""")

CARD = Template("""<div class="card">
<div class="k">$key</div>
<div class="v $cls">$value</div>
</div>""")

TABLE = Template("""<table>
<thead><tr>$heads</tr></thead>
<tbody>
$rows
</tbody>
</table>""")

PLATE = Template("""<div class="plate">
⚠ <b>$title</b><br>$text
</div>""")

IMG = Template("""<img class="chart" src="data:image/png;base64,$b64" alt="$alt">""")


# ═══════════════════════════════════════════════════════════════════════════
# Сборщики
# ═══════════════════════════════════════════════════════════════════════════
def html_table(headers: list[str], rows: list[list], classes: list[str] | None = None) -> str:
    heads = "".join(f"<th>{h}</th>" for h in headers)
    body_rows = []
    for i, row in enumerate(rows):
        cls = f' class="{classes[i]}"' if classes and i < len(classes) and classes[i] else ""
        body_rows.append(f"<tr{cls}>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>")
    return TABLE.substitute(heads=heads, rows="\n".join(body_rows))


def html_cards(items: list[tuple[str, str, str]]) -> str:
    """items: [(ключ, значение, css-класс good/warn/bad/info)]."""
    cards = "\n".join(CARD.substitute(key=k, value=v, cls=c or "info") for k, v, c in items)
    return CARDS.substitute(cards=cards)


def html_section(heading: str, content: str) -> str:
    return SECTION.substitute(heading=heading, content=content)


def html_image(png_path: str, alt: str = "график") -> str:
    return IMG.substitute(b64=_b64(png_path), alt=alt)


def html_page(
    title: str,
    subtitle: str,
    body: str,
    theme: str = "aurora",
    version: str = "1.0.0",
    banner: str = "",
) -> str:
    css = _CSS.get(theme, _CSS["aurora"])
    return PAGE.substitute(
        title=title,
        subtitle=subtitle,
        css=css,
        body=body,
        theme=theme,
        version=version,
        generated=_dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        banner=banner,
    )


def html_plate(title: str, text: str) -> str:
    """Красная плашка (N=8 вне физической вселенной и т.п.)."""
    return PLATE.substitute(title=title, text=text)
