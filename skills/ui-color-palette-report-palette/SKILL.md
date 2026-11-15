---
name: ui-color-palette-report-palette
description: Generate a shareable readability report for a palette — a self-contained HTML document listing every shade with its hex, its value in the palette's color space (OKLCH, LCH…), WCAG 2.2 and APCA scores for light and dark text, a readability score, and a global readability synthesis. Use when the user wants to see, review, share, or archive a palette, asks for a palette document, report, spec sheet or accessibility summary, or after building a palette when a visual preview is offered.
argument-hint: [output-path]
---

# Palette Readability Report

Turn a palette into one document a designer can read, share, or print: every color, every score, one verdict.

The document is rendered by `scripts/render_report.py` (Python 3, standard library only) from the compact rows that `get_palette` already returns. Contrast values come from the API and are never recomputed. Color-space values are derived from the hex with the same formulas as the palette engine (chroma-js).

## Pre-flight — reuse what is in context

1. **Compact rows** (`get_palette` output with `compact: true`) already in context → skip to Step 2. No API call.
2. **`base` + `themes`** in context but no rows → Step 1.
3. **Nothing** → build the palette first with `ui-color-palette-scale-palette`, or retrieve it with `ui-color-palette-manage-palettes`.

## Step 1 — Fetch the rows (only if missing)

Call `get_palette` with:

- the `base` configuration in context, unchanged
- **all themes** the user wants in the report (the report covers every theme passed)
- `textColorsTheme` set on every theme (default `{ lightColor: "#FFFFFF", darkColor: "#000000" }`). Without it `textContrast` is missing and the report cannot score the shades
- `compact: true`. Never `compact: false`: the report does not need the raw color-space values, it derives them

## Step 2 — Write the report data file

Write `report-data.json` in the session's scratch or working directory. Do not show it to the user.

### Report data contract

```json
{
  "palette": {
    "name": "Brand System",
    "description": "",
    "colorSpace": "OKLCH",
    "preset": { "id": "TAILWIND", "name": "Tailwind" },
    "algorithmVersion": "v3"
  },
  "themes": [
    { "name": "Light", "paletteBackground": "#FFFFFF", "textColors": { "light": "#FFFFFF", "dark": "#000000" } }
  ],
  "rows": [],
  "synthesis": {
    "headline": "optional — one sentence",
    "recommendations": ["optional — actionable fixes"]
  }
}
```

| Field | Source | Notes |
| ----- | ------ | ----- |
| `palette.colorSpace` | `base.colorSpace` | Picks the color-space column. `OKLCH`, `LCH`, `LAB`, `OKLAB`, `HSL`, `HSV`, `RGB`, `CMYK` are rendered natively. `HSLUV`, `P3` and `HEX` are rendered in OKLCH, and the document says so |
| `palette.preset` | `base.preset` | `id` + `name` are enough |
| `themes[]` | `themes` passed to `get_palette` | `textColors` mirrors `textColorsTheme` (`lightColor` → `light`, `darkColor` → `dark`); `name` must match the rows' `theme` |
| `rows` | `get_palette` output, verbatim | Paste the array as returned, including the `source` rows. If the tool output was saved to a file, put that **file path** (a string) here instead of copying the array |
| `synthesis` | optional | Omit it and the script writes a rule-based synthesis. Fill `recommendations` only with fixes you actually derived (for example from a `palette-auditor` run) |

## Step 3 — Render

Run the script from this skill's base directory:

```bash
python3 "<skill-base-dir>/scripts/render_report.py" report-data.json "<output>.html"
```

- `<output>`: `$ARGUMENTS` if given, otherwise `<palette-name-kebab-case>-readability-report.html` in the current working directory.
- The script prints a JSON summary on stdout: `verdict`, `overall` scores, `byColor` scores, and `noTextShades`. Use it for the recap. Do not read the HTML back.

If `python3` is not available, say so in one line and fall back to the inline preview of `ui-color-palette-scale-palette` Step 2.

## Step 4 — Deliver

1. **Publishing tool available** (an Artifact or page-publishing tool is listed in the session): publish the generated HTML file as is and give the link.
2. **Otherwise**: give the file path as a clickable link and offer to open it (`open <file>` on macOS, `xdg-open <file>` on Linux).

Then recap in the conversation, in 3 to 5 lines, from the stdout summary:

- verdict and global contrast score
- WCAG 2.2 AA and APCA body-text pass rates
- the weakest color and any shade unusable for text
- one next step: audit and fix (`palette-auditor`), build a color system, or deploy

Never paste the HTML or the raw rows into the conversation.

## What the document contains

| Section | Content |
| ------- | ------- |
| Header | Palette name, description, color space, preset, algorithm version, number of themes, date |
| Synthesis | Verdict, global contrast score, WCAG 2.2 AA rate, APCA Lc 60 rate, readability index, shades reaching AAA, shades unusable for text, findings, recommendations |
| By color | One row per theme × color with the same scores and a verdict |
| Per theme × color | One row per shade: swatch with its best text color, hex, color-space value, WCAG ratio and level for light and dark text, APCA Lc and recommended usage for light and dark text, readability at weight 400 and 700, best text color, contrast against the theme background |
| Method | How each score is computed, so the document stands on its own |

## Scoring rules

Shared with `ui-color-palette-audit-palette`, so a report and an audit of the same palette give the same numbers.

| Score | Rule |
| ----- | ---- |
| WCAG 2.2 level | From the ratio: AAA ≥ 7, AA ≥ 4.5, AA large ≥ 3 (text ≥ 24px or ≥ 18.66px bold, SC 1.4.3 / 1.4.6), Fail below. The API's `score` field labels everything under 4.5 as `A`, so the level is derived from `ratio` instead |
| UI vs background | `contrast.wcag.ratio` (shade against the theme background), checked against SC 1.4.11 non-text contrast ≥ 3:1 |
| APCA | `textContrast.apca.*.lc` and `recommendedUsage` from the API |
| Readability | `min(100, |Lc| / 108 × 100 × weight factor)`, factor 0.85 under 400, 1.15 over 500, 1 otherwise. Same formula as the plugin's contrast report |
| Shade passes | At least one text color reaches WCAG AA (4.5:1), and at least one reaches APCA Lc 60 |
| Global contrast score | Average of the WCAG AA pass rate and the APCA Lc 60 pass rate. Source rows are listed but not counted |
| Verdict | Excellent ≥ 90 %, Good ≥ 75 %, Fair ≥ 50 %, Poor below |

WCAG 2.2 did not change the contrast criteria of WCAG 2.1. APCA is the method drafted for WCAG 3 and is not yet a W3C standard: present it as guidance, not as compliance.

## Tips

- One `get_palette` call feeds the preview, the audit and the report. Never call it twice for the same palette.
- With pure white and black text colors, one of the two always reaches 4.5:1, so the WCAG rate is often 100 %. APCA and the readability index carry the signal for mid-tones; say so in the recap if the WCAG rate is 100 %.
- Keep the file name stable for a palette: re-running the report overwrites the previous version instead of piling up files.

## Recommended subagent

The orchestrator can run this skill directly. When the user also wants remediation, run `palette-auditor` first and pass its fixes in `synthesis.recommendations`.
