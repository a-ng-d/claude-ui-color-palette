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

**Returns**: A `PaletteData` object containing `name`, `description`, `themes` (with full color scales including contrast values), and `type`.

## Pre-computed contrast data

Each shade in the palette data includes pre-computed contrast scores. **Do NOT recalculate contrast — just read the values from the response.**

### `shade.contrast` — shade vs palette background

| Field | Path | Type | Description |
| ----- | ---- | ---- | ----------- |
| WCAG ratio | `contrast.wcag.ratio` | number | Contrast ratio (e.g. `4.52`) |
| WCAG score | `contrast.wcag.score` | `"A"` \| `"AA"` \| `"AAA"` | WCAG level |
| APCA Lc | `contrast.apca.lc` | number | Lightness contrast value |
| APCA usage | `contrast.apca.recommendedUsage` | string | `"FLUENT_TEXT"`, `"BODY_TEXT"`, `"CONTENT_TEXT"`, `"HEADLINES"`, `"SPOT_TEXT"`, `"NON_TEXT"`, `"AVOID"`, `"UNKNOWN"` |

### `shade.textContrast` — light & dark text on shade (optional, present when `textColorsTheme` is set)

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

## Standards

- **WCAG 2.1**: Contrast ratios — AA requires 4.5:1 for normal text, 3:1 for large text; AAA requires 7:1 / 4.5:1
- **APCA**: Lightness contrast (Lc) values — minimum Lc 60 for body text, Lc 45 for large text, Lc 30 for non-text

## Workflow

1. Collect the palette colors from the user or from a previous generation step.
2. Call `get_full_palette` with the palette configuration (ensure `textColorsTheme` is set in themes).
3. **Do NOT read the full `PaletteData` JSON.** Only extract from each shade: `name`, `hex`, `textContrast` (and `contrast` if needed). Skip all other color space values (`rgb`, `gl`, `lch`, `oklch`, `lab`, `oklab`, `hsl`, `hsluv`, `hsv`, `cmyk`).
4. For each shade, read the pre-computed scores directly — no need to recalculate:
   - `shade.textContrast.wcag.light` / `shade.textContrast.wcag.dark` — WCAG ratio & score
   - `shade.textContrast.apca.light` / `shade.textContrast.apca.dark` — APCA Lc & recommendation
5. Build the **data visualization** (see output format below).
6. Compute the **global contrast score** as a consolidated percentage:
   - **WCAG pass rate** = (shades where at least one of light/dark passes AA) / total shades × 100
   - **APCA pass rate** = (shades where at least one of light/dark has |Lc| ≥ 60) / total shades × 100
   - **Global score** = average of WCAG pass rate and APCA pass rate, displayed as `XX%`
7. Flag failing pairs and provide actionable recommendations.

## Arguments

`$ARGUMENTS` can be a list of hex colors to audit or a palette ID.

- `/ui-color-palette:audit-palette #1E293B #F8FAFC #3B82F6 #FFFFFF`
- `/ui-color-palette:audit-palette palette-id-abc123`

## Output format

Present results per color as a detailed table, one row per shade:

### Per-color table

**Color: `{colorName}`** `{sourceHex}`

| Shade | Hex | Light text WCAG | | Dark text WCAG | | Light text APCA | | Dark text APCA | | Best text |
| ----- | --- | --------------- | - | -------------- | - | --------------- | - | -------------- | - | --------- |
| | | Ratio | Score | Ratio | Score | Lc | Usage | Lc | Usage | |
| 50 | #F8FAFC | 1.07 | A | 17.58 | AAA | -4.2 | AVOID | 106.0 | FLUENT_TEXT | Dark |
| 100 | #E2E8F0 | 1.32 | A | 13.16 | AAA | -11.5 | AVOID | 95.2 | FLUENT_TEXT | Dark |
| ... | | | | | | | | | | |

- **Best text**: recommend `Light` or `Dark` based on the highest WCAG score (prioritize AAA > AA > A), then highest APCA |Lc| as tiebreaker.

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

- **Contrast data is pre-computed**: The `textContrast` field on each shade already contains WCAG and APCA scores for both light and dark text. Never instantiate `Contrast` yourself — just read the values.
- **Extract only what you need**: When parsing the `get_full_palette` response, skip `rgb`, `gl`, `lch`, `oklch`, `lab`, `oklab`, `hsl`, `hsluv`, `hsv`, `cmyk`. Only read `name`, `hex`, `contrast`, and `textContrast`.
- **Hex to rgb conversion**: Divide each 0–255 channel by 255 to get the 0–1 value. E.g. `#3B82F6` → `r: 59/255 = 0.23`, `g: 130/255 = 0.51`, `b: 246/255 = 0.96` → `{ r: 0.23, g: 0.51, b: 0.96 }`.
- Ensure `textColorsTheme` is set in each theme (e.g. `{ lightColor: "#FFFFFF", darkColor: "#000000" }`) — otherwise `textContrast` will be `undefined`.
- For quick audits of two colors, compute WCAG ratio locally instead of calling the full palette generation.
