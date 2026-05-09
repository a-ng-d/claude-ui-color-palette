---
name: ui-color-palette-scale-palette
description: Build a full color palette from source colors. Uses get_palette to generate scales and themes, then previews the result visually. Use when the user wants to create a complete palette before auditing, exporting, or deploying it.
argument-hint: <color-space>
---

# Build Palette

Use the **ui-color-palette** MCP tool `get_palette` to build a complete palette, then preview it visually.

Code export is handled by `ui-color-palette-generate-code`. Design tool deployment is handled by `ui-color-palette-figma`, `ui-color-palette-penpot`, `ui-color-palette-framer`, and `ui-color-palette-sketch`.

---

## Pre-flight — Check session state

Before asking any questions, check the conversation context for existing slots.

### If `PaletteData` is already in context

Inform the user of the existing palette (name, color space, preset) and ask: reuse, rebuild, or start from scratch. Wait for reply — if reuse, skip to visual preview.

### If `PublishedPaletteConfig` is already in context

**Skip Step 0 entirely** and go straight to Step 1. Inform the user: building from the loaded palette now.

Map the `PublishedPaletteConfig` fields to the `get_palette` input:

| `PublishedPaletteConfig` field | maps to |
| ------------------------------ | ------- |
| `name` | `base.name` |
| `description` | `base.description` |
| `preset` | `base.preset` |
| `shift` | `base.shift` |
| `are_source_colors_locked` | `base.areSourceColorsLocked` |
| `colors` | `base.colors` |
| `color_space` | `base.colorSpace` |
| `algorithm_version` | `base.algorithmVersion` |
| `themes` | `themes` |

Call `get_palette` immediately with these mapped values.

---

### If `SourceColors` is already in context

Skip question 2 of Step 0. Show the existing colors (name + hex) and ask the user to confirm or change them.

---

## Step 0 — Gather parameters

**Ask these questions before calling `get_palette`.** Do not call the tool until all required answers are collected. Stop after each question if the user hasn’t answered it yet.

### Required

**1. Palette name** — ask for a name.

**2. Source colors** — ask for role + hex per color (e.g. `primary #3B82F6`). Multiple colors allowed.

**3. Color space** — ask to choose: `OKLCH` (recommended), `LCH`, `OKLAB`, `HSL`, `P3`, or other.

**4. Scale preset** — ask to choose: `MATERIAL` (50–900, 10 stops), `TAILWIND` (50–950, 11 stops), `ANT` (1–10), `RADIX` (1–12).

**5. Themes** — ask: Light only, Light + Dark, or Custom.

### Optional (use defaults if not specified)

| Parameter | Default |
| --------- | ------- |
| Algorithm version | `v3` |
| Chroma shift | `100` (no change) |
| Hue shift | `0` (no rotation) |
| Source colors locked | `false` |

Once all required answers are collected, build the `get_palette` input and proceed to Step 1.

---

## Step 1 — Build the palette

**Tool**: `get_palette`

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
| `id` | string | Auto-generated by the server — **do not set** |
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

---

## Visual preview

After generating a palette, do not assume the next step is code export. A palette is often easier to validate visually first.

At minimum, produce a compact visual preview using the generated shades:

- one section per theme
- one row per color family
- one swatch per shade
- each swatch labeled with its `shade.name` and `hex`
- when `textColorsTheme` is available, show the preferred text color (`light` or `dark`) on top of each swatch

### Preview layout

Prefer this structure for a quick visual audit:

| Theme | Color | Swatches |
| ----- | ----- | -------- |
| Light | primary | `50 100 200 300 400 500 600 700 800 900` |

And render the swatches conceptually like this:

```text
Light / primary
[ 50  #F8FAFC ][ 100 #E2E8F0 ][ 200 #CBD5E1 ][ 300 #94A3B8 ]
[ 400 #64748B ][ 500 #475569 ][ 600 #334155 ][ 700 #1E293B ]
[ 800 #0F172A ][ 900 #020617 ]
```

The goal is not pixel-perfect rendering in chat, but a readable, visual summary of the generated palette.

### Design tool handoff

If the user wants the palette generated inside a design document, prefer routing to design tools instead of only exporting code:

- **Figma**: propose generating the palette in the current file as swatches, variables, or local styles
- **Penpot**: propose generating a palette board or style set for review
- **Sketch**: propose generating a palette page, symbol sheet, or token handoff artifact

When the user mentions Figma, FigJam, Penpot, Sketch, design board, palette board, style tiles, or visual preview in a document, treat that as a **design-generation** request first, not a code-export request.

If direct write-back tooling is available for the target design tool, use it. Otherwise:

1. build the palette with `get_palette`
2. extract only `theme.name`, `color.name`, `shade.name`, `shade.hex`, and preferred text color
3. create a compact swatch matrix spec
4. hand that spec off to the relevant design workflow/tool

### Example `get_palette` input

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

## Workflow

1. Collect source colors from the user or from a previous **generate-source-colors** step.
2. Call `get_palette` with a `BaseConfiguration` and at least one `ThemeConfiguration`. The response is a **flat array** of shade rows (compact mode is on by default).
3. **NEVER read, print, or reason from the full array.** Immediately apply the stream-extract below and discard everything else:
   ```
   for each row in response:
     keep: row.theme, row.color, row.shade, row.hex
     STOP — do not read any other field on this row
   ```
   Store the raw response opaquely as the `PaletteData` slot (passed as-is to downstream tools that need it). Reason only from the extracted swatch rows.
   If a downstream tool explicitly needs raw color space values (rgb, lch, etc.), recall `get_palette` with `compact: false` for that specific purpose.
4. If the user asks for a visual preview, design handoff, or document generation, extract only the fields needed for a swatch matrix:
  - `theme.name`
  - `color.name`
  - `shade.name`
  - `shade.hex`
  - preferred text color if it can be inferred from `textColorsTheme` or audit data
5. **Ask the user what to do next.** Building the palette is not the end. The user may want to:
  - **Preview the palette visually** first — render a swatch matrix grouped by theme and color
  - **Generate it in a design tool** — route to `ui-color-palette-figma`, `ui-color-palette-penpot`, `ui-color-palette-framer`, or `ui-color-palette-sketch`
  - **Audit the palette** first — use `ui-color-palette-audit-palette` to check contrast and accessibility
  - **Publish the palette** — use `ui-color-palette-manage-palettes` to save it to the platform
  - **Export as code** — hand off to `ui-color-palette-generate-code`

## Arguments

`$ARGUMENTS` can be a color space or a description of the palette context.

- `/ui-color-palette:scale-palette oklch`
- `/ui-color-palette:scale-palette tailwind stops for my design system`
- `/ui-color-palette:scale-palette material dark and light themes`

## Tips

- **PaletteData**: Never read, print, or summarize the full JSON — the response is huge. Immediately stream-extract to swatch rows (`theme.name`, `color.name`, `shade.name`, `shade.hex`) and pass the raw object opaquely to downstream skills.
- **Hex → rgb 0–1**: divide each 0–255 channel by 255. E.g. `#3B82F6` → `{ r: 0.23, g: 0.51, b: 0.96 }`.
- **Scale without user input**: distribute lightness between `min` (last stop) and `max` (first stop). First stop → `max`, last → `min`.
- **Design-first requests**: board, canvas, swatches, style tiles → route to design tool skill first.
- **Code**: `generate_code` takes `base`+`themes` directly; prefer `dtcg-tokens`, `tailwind-v4`; `OKLCH`/`P3` for wide-gamut.

---

## Recommended subagents

- **`palette-codegen`** — normalizes `PaletteData` and generates code/tokens; use after this skill when code export is needed
- **`palette-transitioner`** — converts `PaletteData` into `variableRows`, `tokenRows`, `styleRows`, or `swatchRows` before routing to a platform workflow
