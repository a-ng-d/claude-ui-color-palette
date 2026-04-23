---
name: ui-color-palette-audit-palette
description: Audit color pairs for contrast compliance against WCAG 2.1 and APCA standards. Use when the user wants to check accessibility, validate color pairings, or compute a global contrast score for a palette.
argument-hint: <hex-colors...>
---

# Audit Contrast

Use the **ui-color-palette** MCP tool `get_full_palette` to generate a palette with contrast data, then analyze the results for WCAG and APCA compliance.

## MCP tool reference

**Tool**: `get_full_palette`

**Input schema**:

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `base` | object | Yes | `BaseConfiguration` — palette base settings |
| `themes` | array | Yes | Array of `ThemeConfiguration` objects (light/dark modes) |

### `base` (BaseConfiguration) fields

| Field | Type | Description |
| ----- | ---- | ----------- |
| `name` | string | Palette name |
| `description` | string | Palette description |
| `preset` | object | `PresetConfiguration` — see below |
| `shift` | object | `ShiftConfiguration` — see below |
| `areSourceColorsLocked` | boolean | Whether source colors are pinned (default: `false`) |
| `colors` | array | Array of `ColorConfiguration` objects |
| `colorSpace` | string | One of: `LCH`, `OKLCH`, `LAB`, `OKLAB`, `HSL`, `HSLUV`, `HSV`, `CMYK`, `RGB`, `HEX`, `P3` |
| `algorithmVersion` | string | `"v1"`, `"v2"`, or `"v3"` |

### `PresetConfiguration`

Controls the lightness scale distribution.

| Field | Type | Description |
| ----- | ---- | ----------- |
| `id` | string | Preset identifier (e.g. `"MATERIAL"`, `"TAILWIND"`, `"CUSTOM_10_100"`) |
| `name` | string | Display name |
| `stops` | `number[]` | Scale stop labels (e.g. `[50, 100, 200, 300, 400, 500, 600, 700, 800, 900]`) |
| `min` | number | Minimum lightness (darkest stop), 0–100 |
| `max` | number | Maximum lightness (lightest stop), 0–100 |
| `easing` | string | Distribution curve: `LINEAR`, `NONE`, `EASEIN_SINE`, `EASEOUT_SINE`, `EASEINOUT_SINE`, `EASEIN_QUAD`, `EASEOUT_QUAD`, `EASEINOUT_QUAD`, `EASEIN_CUBIC`, `EASEOUT_CUBIC`, `EASEINOUT_CUBIC` |

**Common presets**:

| id | stops | min | max | easing |
| -- | ----- | --- | --- | ------ |
| `MATERIAL` | `[50,100,200,300,400,500,600,700,800,900]` | 24 | 96 | `LINEAR` |
| `TAILWIND` | `[50,100,200,300,400,500,600,700,800,900,950]` | 16 | 96 | `LINEAR` |
| `ANT` | `[1,2,3,4,5,6,7,8,9,10]` | 24 | 96 | `LINEAR` |
| `RADIX` | `[1,2,3,4,5,6,7,8,9,10,11,12]` | 5 | 95 | `LINEAR` |

### `ShiftConfiguration`

| Field | Type | Description |
| ----- | ---- | ----------- |
| `chroma` | number | Global chroma multiplier — 100 = no change, <100 = desaturate, >100 = saturate |
| `hue` | number | Global hue rotation in degrees — 0 = no shift |

### `ColorConfiguration` (each entry in `base.colors`)

| Field | Type | Description |
| ----- | ---- | ----------- |
| `id` | string | Unique color ID |
| `name` | string | Color name (e.g. `"primary"`, `"neutral"`) |
| `description` | string | Color description |
| `rgb` | `{ r, g, b }` | RGB object, each value **0–1** (e.g. `{ r: 0.23, g: 0.51, b: 0.96 }` for #3B82F6) |
| `hue` | object | `{ shift: number, isLocked: boolean }` — per-color hue shift (default: `{ shift: 0, isLocked: false }`) |
| `chroma` | object | `{ shift: number, isLocked: boolean }` — per-color chroma shift (default: `{ shift: 100, isLocked: false }`) |
| `alpha` | object | `{ isEnabled: boolean, backgroundColor: string }` — alpha blending (default: `{ isEnabled: false, backgroundColor: "#FFFFFF" }`) |

### `ThemeConfiguration` (each entry in `themes`)

| Field | Type | Description |
| ----- | ---- | ----------- |
| `id` | string | Unique theme ID |
| `name` | string | Theme name (e.g. `"Light"`, `"Dark"`) |
| `description` | string | Theme description |
| `scale` | `Record<string, number>` | Map of stop label → lightness value (0–100). Keys must match `preset.stops`. E.g. `{ "50": 96, "100": 88, "200": 80, ..., "900": 24 }` |
| `paletteBackground` | string | Background hex color (e.g. `"#FFFFFF"`) |
| `visionSimulationMode` | string | `"NONE"`, `"PROTANOMALY"`, `"PROTANOPIA"`, `"DEUTERANOMALY"`, `"DEUTERANOPIA"`, `"TRITANOMALY"`, `"TRITANOPIA"`, `"ACHROMATOMALY"`, `"ACHROMATOPSIA"` |
| `textColorsTheme` | object | `{ lightColor: string, darkColor: string }` — hex colors for text on dark/light backgrounds (default: `{ lightColor: "#FFFFFF", darkColor: "#000000" }`) |
| `isEnabled` | boolean | Whether the theme is active |
| `type` | string | `"default theme"` or `"custom theme"` |

**Returns**: A `PaletteData` object — large payload. **Read only the paths listed in the extraction budget below.** Discard all other fields immediately.

## Pre-computed contrast data

Each shade includes pre-computed scores. **Do NOT recalculate contrast — just read the values.**

**Do NOT read `shade.contrast`** (shade vs palette background) — this skill only uses `shade.textContrast` (light/dark text on shade).

### `shade.textContrast` — light & dark text on shade (requires `textColorsTheme` set in theme)

| Field | Path | Type | Description |
| ----- | ---- | ---- | ----------- |
| WCAG light ratio | `textContrast.wcag.light.ratio` | number | White text on shade |
| WCAG light score | `textContrast.wcag.light.score` | `"A"` \| `"AA"` \| `"AAA"` | WCAG level |
| WCAG dark ratio | `textContrast.wcag.dark.ratio` | number | Black text on shade |
| WCAG dark score | `textContrast.wcag.dark.score` | `"A"` \| `"AA"` \| `"AAA"` | WCAG level |
| APCA light Lc | `textContrast.apca.light.lc` | number | White text Lc |
| APCA light usage | `textContrast.apca.light.recommendedUsage` | string | Recommended usage |
| APCA dark Lc | `textContrast.apca.dark.lc` | number | Black text Lc |
| APCA dark usage | `textContrast.apca.dark.recommendedUsage` | string | Recommended usage |

## Simplified audit dataset

`PaletteData` is rich but too verbose for audit rendering. For this skill, always transform it into a **flattened audit dataset** before analysis.

Do not keep nested theme/color/shade objects in the reasoning context once the useful fields have been extracted. Convert each shade into one compact row.

### Flattened row schema

Use one row per shade with these fields only:

| Column | Source path | Description |
| ------ | ----------- | ----------- |
| `theme` | `theme.name` | Theme label |
| `color` | `color.name` | Color family name |
| `shade` | `shade.name` | Shade label |
| `hex` | `shade.hex` | Display color |
| `wcag_light_ratio` | `shade.textContrast.wcag.light.ratio` | White text ratio |
| `wcag_light_score` | `shade.textContrast.wcag.light.score` | White text WCAG level |
| `wcag_dark_ratio` | `shade.textContrast.wcag.dark.ratio` | Black text ratio |
| `wcag_dark_score` | `shade.textContrast.wcag.dark.score` | Black text WCAG level |
| `apca_light_lc` | `shade.textContrast.apca.light.lc` | White text APCA |
| `apca_light_usage` | `shade.textContrast.apca.light.recommendedUsage` | White text recommendation |
| `apca_dark_lc` | `shade.textContrast.apca.dark.lc` | Black text APCA |
| `apca_dark_usage` | `shade.textContrast.apca.dark.recommendedUsage` | Black text recommendation |
| `best_text` | derived | `LIGHT` or `DARK` |
| `wcag_pass` | derived | `true` if light or dark passes AA |
| `apca_pass` | derived | `true` if light or dark has `|Lc| >= 60` |
| `global_pass` | derived | `true` if `wcag_pass` and `apca_pass` |

### CSV-like representation

Prefer producing or reasoning from a compact CSV-like block instead of the original nested JSON:

```csv
theme,color,shade,hex,wcag_light_ratio,wcag_light_score,wcag_dark_ratio,wcag_dark_score,apca_light_lc,apca_light_usage,apca_dark_lc,apca_dark_usage,best_text,wcag_pass,apca_pass,global_pass
Light,primary,50,#F8FAFC,1.07,A,17.58,AAA,-4.2,AVOID,106.0,FLUENT_TEXT,DARK,true,true,true
Light,primary,100,#E2E8F0,1.32,A,13.16,AAA,-11.5,AVOID,95.2,FLUENT_TEXT,DARK,true,true,true
```

This flattened representation is the preferred input for audit reasoning, summary statistics, and visualization.

## Extraction budget

**Maximum 6 fields read per shade. All other fields must be skipped.**

| Field to read | JSON path |
| ------------- | --------- |
| Shade name | `shade.name` |
| Shade hex | `shade.hex` |
| Light WCAG ratio + score | `shade.textContrast.wcag.light.{ratio,score}` |
| Dark WCAG ratio + score | `shade.textContrast.wcag.dark.{ratio,score}` |
| Light APCA Lc + usage | `shade.textContrast.apca.light.{lc,recommendedUsage}` |
| Dark APCA Lc + usage | `shade.textContrast.apca.dark.{lc,recommendedUsage}` |

**Explicitly skip — do not read, do not store in context:**
`shade.rgb` · `shade.lch` · `shade.oklch` · `shade.lab` · `shade.oklab` · `shade.hsl` · `shade.hsluv` · `shade.hsv` · `shade.cmyk` · `shade.p3` · `shade.gl` · `shade.contrast`

## Standards

- **WCAG 2.1**: Contrast ratios — AA requires 4.5:1 for normal text, 3:1 for large text; AAA requires 7:1 / 4.5:1
- **APCA**: Lightness contrast (Lc) values — minimum Lc 60 for body text, Lc 45 for large text, Lc 30 for non-text

## Workflow

### Step 0 — Check session state (free)

**Before calling any tool**, check whether a `PaletteData` slot is already populated in the conversation context (e.g. produced by `ui-color-palette-scale-palette` in the same session).

- If `PaletteData` is present → **skip to Step 3** (flatten directly). No API call needed.
- If only `base` + `themes` are present (no `PaletteData`) → continue to Step 1.
- If nothing is present → ask the user for the source (palette config, hex colors, or palette ID).

### Step 1 — Scope the audit (before calling the API)

Determine the minimum configuration required. Do not pass more themes than necessary.

Ask (or infer from context):

> Which theme do you want to audit?
> - **Light** (recommended)
> - **Dark**
> - **Both**
> If you do not answer, I will audit **Light** only.

If the user has multiple color families and only cares about a subset, ask which ones — otherwise include all.

**Important**: Pass only the scoped themes in the `themes` array. Removing unused themes significantly reduces the `get_full_palette` response size.

### Step 2 — Call `get_full_palette` (targeted)

Call `get_full_palette` with:
- The full `base` configuration (unchanged)
- Only the **selected theme(s)** in `themes` (not the full list if more exist)
- Ensure every theme has `textColorsTheme` set (e.g. `{ lightColor: "#FFFFFF", darkColor: "#000000" }`) — required for `textContrast` to be populated

### Step 3 — Stream-extract and flatten

Do **not** load the full `PaletteData` into context. Traverse the response path by path and emit one CSV row per shade, then discard the raw data.

Extraction pseudo-path:
```
for each theme in response.themes:
  theme_name = theme.name
  for each color in theme.colors:
    color_name = color.name
    for each shade in color.shades:
      emit row: theme_name, color_name,
                shade.name, shade.hex,
                shade.textContrast.wcag.light.{ratio,score},
                shade.textContrast.wcag.dark.{ratio,score},
                shade.textContrast.apca.light.{lc,recommendedUsage},
                shade.textContrast.apca.dark.{lc,recommendedUsage}
      → compute best_text, wcag_pass, apca_pass, global_pass
      → STOP reading this shade. Do not access any other field.
```

Once all rows are emitted, the raw response is no longer needed — reason only from the CSV rows.

### Step 4 — Analyze and output

1. Build the **data visualization** from the flattened rows (see output format below).
2. Compute the **global contrast score** as a consolidated percentage:
   - **WCAG pass rate** = (shades where at least one of light/dark passes AA) / total shades × 100
   - **APCA pass rate** = (shades where at least one of light/dark has |Lc| ≥ 60) / total shades × 100
   - **Global score** = average of WCAG pass rate and APCA pass rate, displayed as `XX%`
3. Flag failing pairs and provide actionable recommendations.

## Arguments

`$ARGUMENTS` can be a list of hex colors to audit or a palette ID.

- `/ui-color-palette:audit-palette #1E293B #F8FAFC #3B82F6 #FFFFFF`
- `/ui-color-palette:audit-palette palette-id-abc123`

## Output format

The response should have 3 layers: compact dataset, visual audit table, and global score.

### 1. Compact audit dataset

Start with a short CSV-like block or markdown table containing only the flattened audit rows needed for interpretation.

```csv
theme,color,shade,hex,wcag_light_ratio,wcag_dark_ratio,apca_light_lc,apca_dark_lc,best_text,wcag_pass,apca_pass
Light,primary,50,#F8FAFC,1.07,17.58,-4.2,106.0,DARK,true,true
Light,primary,100,#E2E8F0,1.32,13.16,-11.5,95.2,DARK,true,true
```

### 2. Visual audit table

Then present results per color as a visual table, one row per shade:

### Per-color table

**Color: `{colorName}`** `{sourceHex}`

| Shade | Swatch | Hex | Light WCAG | Dark WCAG | Light APCA | Dark APCA | Best text | Status |
| ----- | ------ | --- | ---------- | --------- | ---------- | --------- | --------- | ------ |
| 50 | `[#F8FAFC]` | #F8FAFC | 1.07 / A | 17.58 / AAA | -4.2 / AVOID | 106.0 / FLUENT_TEXT | Dark | Pass |
| 100 | `[#E2E8F0]` | #E2E8F0 | 1.32 / A | 13.16 / AAA | -11.5 / AVOID | 95.2 / FLUENT_TEXT | Dark | Pass |
| ... | | | | | | | | |

- **Best text**: recommend `Light` or `Dark` based on the highest WCAG score (prioritize AAA > AA > A), then highest APCA |Lc| as tiebreaker.
- **Status**: `Pass` if the shade has at least one readable text color for both WCAG AA and APCA body text; otherwise `Fail`.

### Global contrast score

```
╔══════════════════════════════════════════╗
║          GLOBAL CONTRAST SCORE           ║
║                                          ║
║              85%                         ║
║                                          ║
║  WCAG AA pass rate:  90% (27/30 shades)  ║
║  APCA body text:     80% (24/30 shades)  ║
║                                          ║
║  Failing shades: 3                       ║
╚══════════════════════════════════════════╝
```

### Failing shades summary

List every shade that fails both light and dark text for WCAG AA (ratio < 4.5) or APCA body text (|Lc| < 60):

| Color | Shade | Hex | Issue | Recommendation |
| ----- | ----- | --- | ----- | -------------- |
| primary | 400 | #60A5FA | Neither text passes AA | Darken to 500 or lighten to 300 |

End with the global score and recommendations.

## Tips

- **6 fields max per shade**: Follow the extraction budget strictly. Never read `shade.contrast`, `shade.rgb`, `shade.lch`, `shade.oklch`, `shade.lab`, `shade.oklab`, `shade.hsl`, `shade.hsluv`, `shade.hsv`, `shade.cmyk`, `shade.gl` — they are not needed and inflate context size.
- **Discard raw data immediately**: As soon as a shade's CSV row is produced, release the raw shade object. Reason exclusively from the flattened rows.
- **Scope before calling**: Pass only the required theme(s) in the `themes` array. Each extra theme multiplies the response size.
- **Re-use session state**: If `PaletteData` is already in context from a prior step, skip the API call entirely (Step 0).
- **`textColorsTheme` is required**: Ensure every theme has `textColorsTheme` set (e.g. `{ lightColor: "#FFFFFF", darkColor: "#000000" }`) — otherwise `textContrast` will be absent and the audit cannot proceed.
- **Hex to rgb conversion** (for `ColorConfiguration.rgb`): divide each 0–255 channel by 255. E.g. `#3B82F6` → `{ r: 0.23, g: 0.51, b: 0.96 }`.

---

## Recommended subagent

Delegate this skill to **`palette-auditor`**.

The `palette-auditor` agent is optimized for WCAG/APCA contrast audits, global contrast scoring, risky pair detection, and remediation proposals. It knows the audit dataset schema defined in this skill and works from the flattened row representation rather than traversing full `PaletteData`.
