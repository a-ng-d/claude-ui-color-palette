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

## Standards

- **WCAG 2.1**: Contrast ratios — AA requires 4.5:1 for normal text, 3:1 for large text; AAA requires 7:1 / 4.5:1
- **APCA**: Lightness contrast (Lc) values — minimum Lc 60 for body text, Lc 45 for large text, Lc 30 for non-text

## Workflow

1. Collect the palette colors from the user or from a previous generation step.
2. Call `get_full_palette` with the palette configuration to get contrast data embedded in the result.
3. For each foreground/background pair, report:
   - WCAG contrast ratio and pass/fail for AA and AAA
   - APCA Lc value and minimum font size recommendation
4. Compute a **global contrast score** summary:
   - Percentage of pairs passing WCAG AA
   - Average APCA Lc across all pairs
   - Flag any failing pairs prominently
5. Provide actionable recommendations to fix failing pairs (suggest lighter/darker alternatives).

## Arguments

`$ARGUMENTS` can be a list of hex colors to audit or a palette ID.

- `/ui-color-palette:audit-palette #1E293B #F8FAFC #3B82F6 #FFFFFF`
- `/ui-color-palette:audit-palette palette-id-abc123`

## Output format

Present results as a table:

| Foreground | Background | WCAG Ratio | AA | AAA | APCA Lc |
| ---------- | ---------- | ---------- | -- | --- | ------- |

End with the global score and recommendations.

## Tips

- **Hex to rgb conversion**: Divide each 0–255 channel by 255 to get the 0–1 value. E.g. `#3B82F6` → `r: 59/255 = 0.23`, `g: 130/255 = 0.51`, `b: 246/255 = 0.96` → `{ r: 0.23, g: 0.51, b: 0.96 }`.
- Use `paletteBackground` in the theme to set the surface color that foreground colors are tested against.
- For quick audits of two colors, compute WCAG ratio locally instead of calling the full palette generation.
