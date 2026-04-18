---
name: audit-contrast
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
| `preset` | object | `PresetConfiguration` — preset settings |
| `shift` | object | `ShiftConfiguration` — hue/saturation/lightness shifts |
| `areSourceColorsLocked` | boolean | Whether source colors are pinned |
| `colors` | array | Array of `ColorConfiguration` objects |
| `colorSpace` | string | One of: `LCH`, `OKLCH`, `LAB`, `OKLAB`, `HSL`, `HSLUV`, `HSV`, `CMYK`, `RGB`, `HEX`, `P3` |
| `algorithmVersion` | string | Algorithm version (e.g. `"v2"`) |

### `ColorConfiguration` (each entry in `base.colors`)

| Field | Type | Description |
| ----- | ---- | ----------- |
| `name` | string | Color name (e.g. `"primary"`, `"neutral"`) |
| `rgb` | `[r, g, b]` | RGB tuple, each value 0–255 |
| `source` | string | Source identifier (e.g. `"CANVAS"`) |
| `id` | string | Unique color ID |
| `isRemovable` | boolean | Whether the color can be removed |

### `ThemeConfiguration` (each entry in `themes`)

| Field | Type | Description |
| ----- | ---- | ----------- |
| `name` | string | Theme name (e.g. `"Light"`, `"Dark"`) |
| `description` | string | Theme description |
| `scale` | object | Scale configuration |
| `paletteBackground` | `[r, g, b]` | Background color as RGB tuple |
| `isEnabled` | boolean | Whether the theme is active |
| `id` | string | Unique theme ID |
| `type` | string | Theme type |

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

- `/ui-color-palette:audit-contrast #1E293B #F8FAFC #3B82F6 #FFFFFF`
- `/ui-color-palette:audit-contrast palette-id-abc123`

## Output format

Present results as a table:

| Foreground | Background | WCAG Ratio | AA | AAA | APCA Lc |
| ---------- | ---------- | ---------- | -- | --- | ------- |

End with the global score and recommendations.

## Tips

- When the user provides raw hex colors, convert them to `[r, g, b]` tuples for the API (e.g. `#3B82F6` → `[59, 130, 246]`).
- Use `paletteBackground` in the theme to set the surface color that foreground colors are tested against.
- For quick audits of two colors, compute WCAG ratio locally instead of calling the full palette generation.
