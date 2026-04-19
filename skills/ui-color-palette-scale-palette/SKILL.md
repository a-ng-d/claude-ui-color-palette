---
name: ui-color-palette-scale-palette
description: Build a full color palette from source colors and export it as code or design tokens. Uses get_full_palette to generate scales and themes, then generate_code to output in any format (CSS, SCSS, Tailwind, SwiftUI, Compose, DTCG, etc.). Use when the user wants to create a complete palette and export it for development.
argument-hint: <format> [color-space]
---

# Create & Deploy Palette

Use the **ui-color-palette** MCP tools `get_full_palette` and `generate_code` to build a complete palette and export it as code.

---

## Step 1 — Build the palette

**Tool**: `get_full_palette`

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

**Returns**: A `PaletteData` object containing `name`, `description`, `themes` (with full color scales), and `type`.

### Example `get_full_palette` input

```json
{
  "base": {
    "name": "My Palette",
    "description": "",
    "preset": {
      "id": "MATERIAL",
      "name": "Material Design",
      "stops": [50, 100, 200, 300, 400, 500, 600, 700, 800, 900],
      "min": 24,
      "max": 96,
      "easing": "LINEAR"
    },
    "shift": { "chroma": 100, "hue": 0 },
    "areSourceColorsLocked": false,
    "colors": [
      {
        "id": "primary",
        "name": "primary",
        "description": "",
        "rgb": { "r": 0.23, "g": 0.51, "b": 0.96 },
        "hue": { "shift": 0, "isLocked": false },
        "chroma": { "shift": 100, "isLocked": false },
        "alpha": { "isEnabled": false, "backgroundColor": "#FFFFFF" }
      }
    ],
    "colorSpace": "OKLCH",
    "algorithmVersion": "v3"
  },
  "themes": [
    {
      "id": "light",
      "name": "Light",
      "description": "",
      "scale": { "50": 96, "100": 88, "200": 80, "300": 72, "400": 64, "500": 56, "600": 48, "700": 40, "800": 32, "900": 24 },
      "paletteBackground": "#FFFFFF",
      "visionSimulationMode": "NONE",
      "textColorsTheme": { "lightColor": "#FFFFFF", "darkColor": "#000000" },
      "isEnabled": true,
      "type": "default theme"
    }
  ]
}
```

---

## Step 2 — Export as code

**Tool**: `generate_code`

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `paletteData` | object | Yes | The `PaletteData` object returned by `get_full_palette` |
| `format` | enum | No | Output format (default: `css`) — see table below |
| `colorSpace` | enum | No | Color space for output values (default: `RGB`) |

### `format` values

| Value | Description | `colorSpace` used? |
| ----- | ----------- | ------------------ |
| `css` | CSS custom properties (`--color-name: value`) | Yes |
| `scss` | SCSS variables (`$color-name: value`) | Yes |
| `less` | Less variables (`@color-name: value`) | Yes |
| `tailwind-v3` | Tailwind CSS v3 `theme.extend.colors` config | No |
| `tailwind-v4` | Tailwind CSS v4 `@theme` block | No |
| `swift-ui` | SwiftUI `Color` extensions | No |
| `ui-kit` | UIKit `UIColor` extensions | No |
| `compose` | Jetpack Compose `Color()` constants | No |
| `resources` | Android XML color resources | No |
| `csv` | CSV spreadsheet (name, hex, rgb columns) | No |
| `native-tokens` | Native JSON token format | No |
| `dtcg-tokens` | DTCG (Design Tokens Community Group) JSON | Yes |
| `style-dictionary-v3` | Style Dictionary v3 token format | No |
| `universal-json` | Universal JSON (flat key/value) | No |

### `colorSpace` values

`RGB` · `LCH` · `LAB` · `HSL` · `OKLCH` · `OKLAB` · `P3`

Only applies to `css`, `scss`, `less`, and `dtcg-tokens`. Other formats use their own fixed color representation.

---

## Workflow

1. Collect source colors from the user or from a previous **generate-source-colors** step.
2. Call `get_full_palette` with a `BaseConfiguration` and at least one `ThemeConfiguration` to generate the full palette with scales.
3. **Do NOT read, summarize, or display the `PaletteData` result.** The response is a large JSON object with many color values — reading it wastes tokens.
4. **Ask the user what to do next.** Exporting as code is not the only option. The user may want to:
   - **Audit the palette** first — use the **audit-palette** skill to check contrast and accessibility before exporting.
   - **Publish the palette** — use the **manage-palettes** skill to save it to the database and optionally share it with the community.
   - **Export as code** — continue to step 5.
5. Ask the user which format(s) and color space they want.
6. Call `generate_code` with the raw `PaletteData` from step 2 and the desired `format`/`colorSpace`.
7. Present the generated code in a fenced code block with the appropriate language tag.
8. Offer to write the output to a file in the project.

## Arguments

`$ARGUMENTS` can be a format, a format + color space, or a description of the target.

- `/ui-color-palette:scale-palette tailwind-v4`
- `/ui-color-palette:scale-palette css oklch`
- `/ui-color-palette:scale-palette dtcg-tokens P3`
- `/ui-color-palette:scale-palette scss variables for my design system`

## Tips

- **Token efficiency**: Never read, print, or summarize the `PaletteData` JSON. It contains dozens of color shades with multiple color space values each. Always pass it opaquely to `generate_code`.
- **Hex to rgb conversion**: Divide each 0–255 channel by 255 to get the 0–1 value. E.g. `#3B82F6` → `r: 59/255 = 0.23`, `g: 130/255 = 0.51`, `b: 246/255 = 0.96` → `{ r: 0.23, g: 0.51, b: 0.96 }`.
- **Scale computation**: If the user doesn't provide a `scale` object, compute it from the preset: distribute lightness values between `min` (darkest) and `max` (lightest) across `stops` using the `easing` function. First stop → `max`, last stop → `min`.
- When the user mentions a specific framework, pick the matching format automatically.
- For design token workflows, prefer `dtcg-tokens` for interoperability or `style-dictionary-v3` for Style Dictionary pipelines.
- Suggest `tailwind-v4` over `tailwind-v3` for new projects.
- Use `OKLCH` or `P3` color spaces for wide-gamut displays.
- The `paletteData` input to `generate_code` must be the full object from `get_full_palette` — it contains `name`, `description`, `themes` (with color scales), and `type`.
- This skill combines well with **generate-source-colors** (generate colors first, then build + export here) and **manage-palettes** (publish the palette after building).
