#!/usr/bin/env python3
"""Render a UI Color Palette readability report as a self-contained HTML file.

Usage:
    python3 render_report.py <report-data.json> <output.html>

Input: a JSON object (see SKILL.md, "Report data contract"):
    {
      "palette": {"name", "description?", "colorSpace", "preset?", "algorithmVersion?"},
      "themes":  [{"name", "paletteBackground?", "textColors": {"light", "dark"}}],
      "rows":    [ ...rows returned verbatim by get_palette (compact: true)... ],
      "synthesis": {"headline?", "recommendations?": [str]}   # optional
    }

Output: the HTML file, plus a JSON summary on stdout (scores, verdict, weak
shades) so the caller can recap the report in the conversation without
re-reading the file.

Standard library only. Contrast values are read from the API rows, never
recomputed. Color-space values are derived from the hex with the same formulas
as chroma-js, the library used by the palette engine.
"""

import html
import json
import math
import sys
from datetime import date

# --------------------------------------------------------------------------
# Color-space conversions (chroma-js parity: Lab/LCH use D65, Xn=0.950470,
# Zn=1.088830; OKLab follows Björn Ottosson's reference matrices)
# --------------------------------------------------------------------------

def hex_to_rgb(hex_value):
    h = hex_value.lstrip("#")
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _linear(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _lab_f(t):
    t0, t1 = 4 / 29, 6 / 29
    t2, t3 = 3 * t1 * t1, t1 ** 3
    return t ** (1 / 3) if t > t3 else t / t2 + t0


def rgb_to_lab(rgb):
    r, g, b = (_linear(c) for c in rgb)
    x = _lab_f((0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.950470)
    y = _lab_f((0.2126729 * r + 0.7151522 * g + 0.0721750 * b) / 1.0)
    z = _lab_f((0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.088830)
    lightness = max(0.0, 116 * y - 16)
    return lightness, 500 * (x - y), 200 * (y - z)


def rgb_to_oklab(rgb):
    r, g, b = (_linear(c) for c in rgb)
    l_ = math.copysign(abs(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3), 1)
    m_ = math.copysign(abs(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3), 1)
    s_ = math.copysign(abs(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3), 1)
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )


def _to_polar(lightness, a, b):
    chroma = math.hypot(a, b)
    hue = (math.degrees(math.atan2(b, a)) + 360) % 360
    return lightness, chroma, (None if round(chroma * 10000) == 0 else hue)


def _hue(h):
    return "none" if h is None else f"{h:.1f}°"


def rgb_to_hsl_hsv(rgb):
    r, g, b = (c / 255 for c in rgb)
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    if d == 0:
        h = None
    elif mx == r:
        h = (60 * ((g - b) / d) + 360) % 360
    elif mx == g:
        h = 60 * ((b - r) / d) + 120
    else:
        h = 60 * ((r - g) / d) + 240
    lightness = (mx + mn) / 2
    s_hsl = 0 if d == 0 else d / (1 - abs(2 * lightness - 1))
    s_hsv = 0 if mx == 0 else d / mx
    return h, s_hsl, lightness, s_hsv, mx


SPACE_LABELS = {
    "OKLCH": "OKLCH (L C H)",
    "LCH": "LCH (L C H)",
    "LAB": "Lab (L a b)",
    "OKLAB": "OKLab (L a b)",
    "HSL": "HSL",
    "HSV": "HSV",
    "RGB": "RGB",
    "CMYK": "CMYK",
}
FALLBACK_SPACE = "OKLCH"  # HSLUV, P3 and HEX are rendered as OKLCH


def color_space_value(hex_value, space):
    rgb = hex_to_rgb(hex_value)
    if space == "OKLCH":
        lightness, c, h = _to_polar(*rgb_to_oklab(rgb))
        return f"{lightness * 100:.1f}% {c:.3f} {_hue(h)}"
    if space == "LCH":
        lightness, c, h = _to_polar(*rgb_to_lab(rgb))
        return f"{lightness:.1f} {c:.1f} {_hue(h)}"
    if space == "LAB":
        lightness, a, b = rgb_to_lab(rgb)
        return f"{lightness:.1f} {a:.1f} {b:.1f}"
    if space == "OKLAB":
        lightness, a, b = rgb_to_oklab(rgb)
        return f"{lightness * 100:.1f}% {a:.3f} {b:.3f}"
    if space in ("HSL", "HSV"):
        h, s_hsl, lightness, s_hsv, v = rgb_to_hsl_hsv(rgb)
        if space == "HSL":
            return f"{_hue(h)} {s_hsl * 100:.0f}% {lightness * 100:.0f}%"
        return f"{_hue(h)} {s_hsv * 100:.0f}% {v * 100:.0f}%"
    if space == "RGB":
        return " ".join(str(c) for c in rgb)
    if space == "CMYK":
        r, g, b = (c / 255 for c in rgb)
        k = 1 - max(r, g, b)
        if k >= 1:
            return "0% 0% 0% 100%"
        c, m, y = ((1 - ch - k) / (1 - k) for ch in (r, g, b))
        return " ".join(f"{v * 100:.0f}%" for v in (c, m, y, k))
    return color_space_value(hex_value, FALLBACK_SPACE)


# --------------------------------------------------------------------------
# Scoring — thresholds shared with ui-color-palette-audit-palette
# --------------------------------------------------------------------------

APCA_MAX = 108  # same constant as the plugin's contrast report


def wcag_level(ratio):
    """WCAG 2.2 level for normal text (SC 1.4.3 / 1.4.6), derived from the ratio."""
    if ratio >= 7:
        return "AAA"
    if ratio >= 4.5:
        return "AA"
    if ratio >= 3:
        return "AA18"  # large text (≥ 24px, or ≥ 18.66px bold) and non-text UI
    return "FAIL"


WCAG_LABELS = {"AAA": "AAA", "AA": "AA", "AA18": "AA large", "FAIL": "Fail"}

USAGE_LABELS = {
    "FLUENT_TEXT": "Fluent text",
    "CONTENT_TEXT": "Content text",
    "BODY_TEXT": "Body text",
    "HEADLINES": "Headlines",
    "SPOT_TEXT": "Spot text",
    "NON_TEXT": "Non-text",
    "AVOID": "Avoid",
    "UNKNOWN": "Unknown",
}


def readability(lc, weight=400):
    """Plugin formula: |Lc| rescaled to 100, weighted by font weight, capped."""
    factor = 0.85 if weight < 400 else 1.15 if weight > 500 else 1.0
    return round(min(100, abs(lc) / APCA_MAX * 100 * factor))


def verdict(score):
    if score >= 90:
        return "Excellent"
    if score >= 75:
        return "Good"
    if score >= 50:
        return "Fair"
    return "Poor"


def analyze_row(row):
    tc = row.get("textContrast") or {}
    wcag = tc.get("wcag") or {}
    apca = tc.get("apca") or {}
    sides = {}
    for side in ("light", "dark"):
        ratio = float((wcag.get(side) or {}).get("ratio") or 0)
        lc = float((apca.get(side) or {}).get("lc") or 0)
        sides[side] = {
            "ratio": ratio,
            "level": wcag_level(ratio),
            "lc": lc,
            "usage": (apca.get(side) or {}).get("recommendedUsage", "UNKNOWN"),
            "read400": readability(lc, 400),
            "read700": readability(lc, 700),
        }
    best = "dark" if abs(sides["dark"]["lc"]) > abs(sides["light"]["lc"]) else "light"
    if sides["dark"]["ratio"] != sides["light"]["ratio"]:
        best_wcag = "dark" if sides["dark"]["ratio"] > sides["light"]["ratio"] else "light"
        if wcag_level(sides[best_wcag]["ratio"]) != wcag_level(sides[best]["ratio"]):
            best = best_wcag
    wcag_pass = max(sides["light"]["ratio"], sides["dark"]["ratio"]) >= 4.5
    apca_pass = max(abs(sides["light"]["lc"]), abs(sides["dark"]["lc"])) >= 60
    bg = row.get("contrast") or {}
    ui_ratio = float(((bg.get("wcag") or {}).get("ratio")) or 0)
    return {
        "sides": sides,
        "best": best,
        "wcag_pass": wcag_pass,
        "apca_pass": apca_pass,
        "global_pass": wcag_pass and apca_pass,
        "readability": max(sides["light"]["read400"], sides["dark"]["read400"]),
        "dead_zone": max(sides["light"]["ratio"], sides["dark"]["ratio"]) < 3,
        "ui_ratio": ui_ratio,
        "ui_pass": ui_ratio >= 3,
    }


def pct(part, total):
    return round(part / total * 100) if total else 0


def score_block(analyses):
    total = len(analyses)
    wcag = sum(a["wcag_pass"] for a in analyses)
    apca = sum(a["apca_pass"] for a in analyses)
    wcag_rate, apca_rate = pct(wcag, total), pct(apca, total)
    return {
        "shades": total,
        "wcag_pass": wcag,
        "wcag_rate": wcag_rate,
        "apca_pass": apca,
        "apca_rate": apca_rate,
        "aaa": sum(max(a["sides"]["light"]["ratio"], a["sides"]["dark"]["ratio"]) >= 7 for a in analyses),
        "global_score": round((wcag_rate + apca_rate) / 2),
        "readability_index": round(sum(a["readability"] for a in analyses) / total) if total else 0,
        "dead_zone": sum(a["dead_zone"] for a in analyses),
        "ui_pass": sum(a["ui_pass"] for a in analyses),
    }


# --------------------------------------------------------------------------
# HTML
# --------------------------------------------------------------------------

CSS = """
:root{--bg:#fbfbfa;--surface:#fff;--ink:#1d1d1f;--muted:#6b6b70;--line:#e4e4e7;
--ok:#1f7a4d;--ok-bg:#e6f4ec;--warn:#8a5a00;--warn-bg:#fdf3dc;--bad:#b42318;--bad-bg:#fde8e7;}
@media (prefers-color-scheme:dark){:root{--bg:#161618;--surface:#1f1f22;--ink:#ededef;
--muted:#a0a0a8;--line:#323236;--ok:#6fd39c;--ok-bg:#16301f;--warn:#f0c46b;--warn-bg:#33280f;
--bad:#ff8a80;--bad-bg:#3a1714;}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 -apple-system,BlinkMacSystemFont,
"Segoe UI",Inter,Roboto,sans-serif}
main{max-width:1180px;margin:0 auto;padding:40px 16px 64px}
h1{font-size:28px;margin:0 0 4px;letter-spacing:-.01em}
h2{font-size:20px;margin:40px 0 12px}
h3{font-size:15px;margin:28px 0 8px;display:flex;align-items:center;gap:8px}
p{margin:0 0 8px}.muted{color:var(--muted)}
.meta{display:flex;flex-wrap:wrap;gap:6px 18px;color:var(--muted);margin-top:8px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:16px 0}
.kpi{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px}
.kpi b{display:block;font-size:26px;font-variant-numeric:tabular-nums}
.kpi span{color:var(--muted);font-size:12px}
.verdict{display:inline-block;padding:2px 10px;border-radius:99px;font-weight:600;font-size:13px}
.v-Excellent,.v-Good{background:var(--ok-bg);color:var(--ok)}
.v-Fair{background:var(--warn-bg);color:var(--warn)}.v-Poor{background:var(--bad-bg);color:var(--bad)}
.card{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px 18px}
.card ul{margin:6px 0 0;padding-left:18px}.card li{margin:3px 0}
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--surface)}
table{border-collapse:collapse;width:100%;min-width:980px;font-variant-numeric:tabular-nums}
th,td{padding:7px 10px;text-align:left;border-bottom:1px solid var(--line);white-space:nowrap}
th{font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);font-weight:600}
tr:last-child td{border-bottom:0}
.sw{display:inline-flex;align-items:center;justify-content:center;width:64px;height:30px;
border-radius:6px;font-weight:600;font-size:12px;border:1px solid rgba(127,127,127,.25)}
.dot{width:14px;height:14px;border-radius:4px;display:inline-block;border:1px solid rgba(127,127,127,.3)}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px}
.tag{display:inline-block;padding:1px 7px;border-radius:5px;font-size:11.5px;font-weight:600}
.t-AAA,.t-AA,.t-ok{background:var(--ok-bg);color:var(--ok)}
.t-AA18,.t-mid{background:var(--warn-bg);color:var(--warn)}.t-FAIL,.t-bad{background:var(--bad-bg);color:var(--bad)}
.src td{font-weight:600}
footer{margin-top:40px;color:var(--muted);font-size:12px}
@media print{body{background:#fff}.scroll{overflow:visible}table{min-width:0;font-size:10px}
h2{break-after:avoid}.card,.kpi{break-inside:avoid}}
"""


def esc(value):
    return html.escape(str(value), quote=True)


def lc_tag(lc):
    a = abs(lc)
    cls = "ok" if a >= 60 else "mid" if a >= 45 else "bad"  # body text / headlines / below
    return f'<span class="tag t-{cls}">Lc {a:.1f}</span>'


def wcag_tag(side):
    level = side["level"]
    return f'<span class="tag t-{level}">{side["ratio"]:.2f}:1 · {WCAG_LABELS[level]}</span>'


def read_tag(score):
    cls = "ok" if score >= 56 else "mid" if score >= 42 else "bad"  # ≈ Lc 60 / Lc 45 at weight 400
    return f'<span class="tag t-{cls}">{score}%</span>'


def render_table(rows, analyses, space, text_colors):
    head = (
        "<tr><th>Shade</th><th>Swatch</th><th>Hex</th>"
        f"<th>{esc(SPACE_LABELS.get(space, SPACE_LABELS[FALLBACK_SPACE]))}</th>"
        "<th>WCAG · light text</th><th>WCAG · dark text</th>"
        "<th>APCA · light text</th><th>APCA · dark text</th>"
        "<th>Readability 400 / 700</th><th>Best text</th><th>UI vs bg</th></tr>"
    )
    body = []
    for row, a in zip(rows, analyses):
        best = a["sides"][a["best"]]
        fg = text_colors[a["best"]]
        is_source = row.get("type") == "source color"
        body.append(
            f'<tr class="{"src" if is_source else ""}">'
            f'<td>{esc(row.get("shade", ""))}{" ★" if is_source else ""}</td>'
            f'<td><span class="sw" style="background:{esc(row["hex"])};color:{esc(fg)}">Aa</span></td>'
            f'<td class="mono">{esc(row["hex"].upper())}</td>'
            f'<td class="mono">{esc(color_space_value(row["hex"], space))}</td>'
            f'<td>{wcag_tag(a["sides"]["light"])}</td><td>{wcag_tag(a["sides"]["dark"])}</td>'
            f'<td>{lc_tag(a["sides"]["light"]["lc"])} <span class="muted">'
            f'{esc(USAGE_LABELS.get(a["sides"]["light"]["usage"], ""))}</span></td>'
            f'<td>{lc_tag(a["sides"]["dark"]["lc"])} <span class="muted">'
            f'{esc(USAGE_LABELS.get(a["sides"]["dark"]["usage"], ""))}</span></td>'
            f'<td>{read_tag(best["read400"])} {read_tag(best["read700"])}</td>'
            f'<td><span class="dot" style="background:{esc(fg)}"></span> {a["best"].capitalize()}</td>'
            f'<td><span class="tag t-{"ok" if a["ui_pass"] else "bad"}">{a["ui_ratio"]:.2f}:1</span></td>'
            "</tr>"
        )
    return f'<div class="scroll"><table><thead>{head}</thead><tbody>{"".join(body)}</tbody></table></div>'


def auto_findings(per_color, overall):
    findings = []
    ranked = sorted(per_color, key=lambda c: c["score"]["global_score"], reverse=True)
    if len(ranked) > 1 and ranked[0]["score"]["global_score"] != ranked[-1]["score"]["global_score"]:
        def label(c):
            return f'{esc(c["theme"])} · {esc(c["name"])}'
        findings.append(
            f'Strongest color: <b>{label(ranked[0])}</b> ({ranked[0]["score"]["global_score"]}%) — '
            f'weakest: <b>{label(ranked[-1])}</b> ({ranked[-1]["score"]["global_score"]}%).'
        )
    for c in per_color:
        mid = [str(r["shade"]) for r, a in c["items"] if a["wcag_pass"] and not a["apca_pass"]]
        if mid:
            findings.append(
                f'<b>{esc(c["theme"])} · {esc(c["name"])}</b>: shades {esc(", ".join(mid))} pass WCAG AA '
                "but stay under APCA Lc 60 — keep them for headlines, large or bold text."
            )
        dead = [r["shade"] for r, a in c["items"] if a["dead_zone"]]
        if dead:
            findings.append(
                f'<b>{esc(c["theme"])} · {esc(c["name"])}</b>: shades {esc(", ".join(map(str, dead)))} '
                "stay below 3:1 with both text colors — reserve them for decoration or large surfaces "
                "without text."
            )
        light = [str(r["shade"]) for r, a in c["items"] if a["best"] == "light" and a["global_pass"]]
        dark = [str(r["shade"]) for r, a in c["items"] if a["best"] == "dark" and a["global_pass"]]
        if light or dark:
            parts = []
            if dark:
                parts.append(f'dark text on {esc(", ".join(dark))}')
            if light:
                parts.append(f'light text on {esc(", ".join(light))}')
            findings.append(f'<b>{esc(c["theme"])} · {esc(c["name"])}</b> — body text safe with ' + "; ".join(parts) + ".")
    if overall["shades"] and overall["aaa"] == 0:
        findings.append("No shade reaches WCAG AAA (7:1) with either text color.")
    return findings


def build(data):
    palette = data.get("palette") or {}
    space = (palette.get("colorSpace") or "LCH").upper()
    rendered_space = space if space in SPACE_LABELS else FALLBACK_SPACE
    themes = {t["name"]: t for t in data.get("themes") or [] if t.get("name")}
    rows = data.get("rows") or []
    if not rows:
        raise SystemExit("report data has no rows — pass the compact get_palette output")

    groups, order = {}, []
    for row in rows:
        key = (row.get("theme", "None"), row.get("color", ""))
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(row)

    per_color, all_shades, sections = [], [], []
    current_theme = None
    for key in order:
        theme_name, color_name = key
        theme = themes.get(theme_name, {})
        tcols = theme.get("textColors") or {}
        text_colors = {"light": tcols.get("light", "#FFFFFF"), "dark": tcols.get("dark", "#000000")}
        crow = groups[key]
        analyses = [analyze_row(r) for r in crow]
        shade_items = [(r, a) for r, a in zip(crow, analyses) if r.get("type") != "source color"]
        score = score_block([a for _, a in shade_items])
        all_shades.extend(a for _, a in shade_items)
        per_color.append({"theme": theme_name, "name": color_name, "items": shade_items, "score": score})
        if theme_name != current_theme:
            current_theme = theme_name
            bg = theme.get("paletteBackground", "#FFFFFF")
            sections.append(
                f'<h2>Theme · {esc(theme_name)}</h2><p class="muted">Background '
                f'<span class="dot" style="background:{esc(bg)}"></span> <span class="mono">{esc(bg)}</span> · '
                f'light text <span class="mono">{esc(text_colors["light"])}</span> · dark text '
                f'<span class="mono">{esc(text_colors["dark"])}</span></p>'
            )
        source = next((r for r in crow if r.get("type") == "source color"), None)
        dot = f'<span class="dot" style="background:{esc(source["hex"])}"></span>' if source else ""
        sections.append(
            f'<h3>{dot}{esc(color_name)} <span class="verdict v-{verdict(score["global_score"])}">'
            f'{score["global_score"]}% · {verdict(score["global_score"])}</span></h3>'
            + render_table(crow, analyses, rendered_space, text_colors)
        )

    overall = score_block(all_shades)
    synthesis = data.get("synthesis") or {}
    v = verdict(overall["global_score"])
    headline = synthesis.get("headline") or (
        f'{v} overall readability: {overall["wcag_pass"]} of {overall["shades"]} shades carry WCAG AA body '
        f'text and {overall["apca_pass"]} reach APCA Lc 60 with at least one text color.'
    )
    findings = auto_findings(per_color, overall)
    recos = synthesis.get("recommendations") or []

    meta = [f"Color space · {esc(space)}"]
    if space != rendered_space:
        meta.append(f"values shown in {rendered_space}")
    preset = palette.get("preset")
    if isinstance(preset, dict):
        preset = preset.get("name") or preset.get("id")
    if preset:
        meta.append(f"Preset · {esc(preset)}")
    if palette.get("algorithmVersion"):
        meta.append(f"Algorithm · {esc(palette['algorithmVersion'])}")
    meta.append(f"Themes · {len({k[0] for k in order})}")
    meta.append(f"Generated · {date.today().isoformat()}")

    kpis = [
        (f'{overall["global_score"]}%', "Global contrast score"),
        (f'{overall["wcag_rate"]}%', f'WCAG 2.2 AA · {overall["wcag_pass"]}/{overall["shades"]} shades'),
        (f'{overall["apca_rate"]}%', f'APCA body text · {overall["apca_pass"]}/{overall["shades"]} shades'),
        (f'{overall["readability_index"]}%', "Readability index (400)"),
        (str(overall["aaa"]), "Shades reaching AAA"),
        (str(overall["dead_zone"]), "Shades unusable for text"),
    ]
    color_rows = "".join(
        f'<tr><td>{esc(c["theme"])}</td><td>{esc(c["name"])}</td><td>{c["score"]["global_score"]}%</td>'
        f'<td>{c["score"]["wcag_rate"]}%</td><td>{c["score"]["apca_rate"]}%</td>'
        f'<td>{c["score"]["readability_index"]}%</td><td>{c["score"]["dead_zone"]}</td>'
        f'<td><span class="verdict v-{verdict(c["score"]["global_score"])}">'
        f'{verdict(c["score"]["global_score"])}</span></td></tr>'
        for c in per_color
    )
    name = palette.get("name") or "Untitled palette"
    description = palette.get("description") or ""

    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(name)} — Readability report</title><style>{CSS}</style></head><body><main>
<p class="muted">UI Color Palette · Readability report</p>
<h1>{esc(name)}</h1>{f'<p class="muted">{esc(description)}</p>' if description else ''}
<div class="meta">{''.join(f'<span>{m}</span>' for m in meta)}</div>
<h2>Synthesis <span class="verdict v-{v}">{v}</span></h2>
<div class="kpis">{''.join(f'<div class="kpi"><b>{k}</b><span>{esc(l)}</span></div>' for k, l in kpis)}</div>
<div class="card"><p><b>{esc(headline)}</b></p><ul>{''.join(f'<li>{f}</li>' for f in findings)}</ul>
{('<p style="margin-top:12px"><b>Recommendations</b></p><ul>' + ''.join(f'<li>{esc(r)}</li>' for r in recos) + '</ul>') if recos else ''}
</div>
<h2>By color</h2><div class="scroll"><table style="min-width:640px"><thead><tr><th>Theme</th><th>Color</th>
<th>Global</th><th>WCAG AA</th><th>APCA Lc 60</th><th>Readability</th><th>No-text shades</th><th>Verdict</th>
</tr></thead><tbody>{color_rows}</tbody></table></div>
{''.join(sections)}
<h2>Method</h2><div class="card muted">
<p><b>WCAG 2.2</b> — contrast ratio of the light and dark text colors on each shade (SC 1.4.3 / 1.4.6:
AA ≥ 4.5:1, AAA ≥ 7:1, “AA large” ≥ 3:1 for text ≥ 24px or ≥ 18.66px bold). “UI vs bg” is the shade
against the theme background, checked against SC 1.4.11 (non-text contrast ≥ 3:1). These thresholds are
unchanged from WCAG 2.1.</p>
<p><b>APCA</b> — lightness contrast Lc (0.0.98G, the method drafted for WCAG 3, not yet a W3C standard)
with the engine’s recommended usage: fluent text ≥ 90, content text ≥ 75, body text ≥ 60, headlines ≥ 45,
spot text ≥ 30, non-text ≥ 15.</p>
<p><b>Readability</b> — |Lc| rescaled to 100 (Lc 108 = 100%), × 0.85 below weight 400, × 1.15 above 500,
capped at 100%, for the best text color. Same formula as the plugin’s contrast report.</p>
<p><b>Global contrast score</b> — average of the WCAG AA pass rate and the APCA Lc 60 pass rate; a shade
passes when at least one of the two text colors meets the threshold. Source colors (★) are listed but not
counted. Verdict: Excellent ≥ 90%, Good ≥ 75%, Fair ≥ 50%, Poor below.</p>
<p>Contrast values come from the UI Color Palette API. Color-space values are derived from the hex.</p>
</div><footer>Generated with the UI Color Palette plugin for Claude.</footer></main></body></html>"""

    summary = {
        "palette": name,
        "colorSpace": space,
        "verdict": v,
        "overall": overall,
        "byColor": [{"theme": c["theme"], "color": c["name"], **c["score"]} for c in per_color],
        "noTextShades": [
            {"theme": c["theme"], "color": c["name"], "shade": r["shade"], "hex": r["hex"]}
            for c in per_color for r, a in c["items"] if a["dead_zone"]
        ],
    }
    return doc, summary


def main(argv):
    if len(argv) != 3:
        raise SystemExit("usage: render_report.py <report-data.json> <output.html>")
    with open(argv[1], encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data.get("rows"), str):  # path to a saved get_palette output
        with open(data["rows"], encoding="utf-8") as fh:
            rows = json.load(fh)
        data["rows"] = rows if isinstance(rows, list) else rows.get("rows", [])
    doc, summary = build(data)
    with open(argv[2], "w", encoding="utf-8") as fh:
        fh.write(doc)
    summary["output"] = argv[2]
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv)
