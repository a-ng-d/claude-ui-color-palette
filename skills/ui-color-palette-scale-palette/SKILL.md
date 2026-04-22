---
name: ui-color-palette-scale-palette
description: Build a full color palette from source colors. Uses get_full_palette to generate scales and themes, then previews the result visually. Use when the user wants to create a complete palette before auditing, exporting, or deploying it.
argument-hint: <color-space>
---

# Build Palette

Use the **ui-color-palette** MCP tool `get_full_palette` to build a complete palette, then preview it visually.

Code export is handled by `ui-color-palette-generate-code`. Design tool deployment is handled by `ui-color-palette-figma`, `ui-color-palette-penpot`, `ui-color-palette-framer`, and `ui-color-palette-sketch`.

---

## Step 0 — Gather parameters

**Ask these questions before calling `get_full_palette`.** Do not call the tool until all required answers are collected. Stop after each question if the user hasn’t answered it yet.

### Required

**1. Palette name**
> What should this palette be called?

**2. Source colors**
> List the colors to include. For each one, provide:
> - A role name (e.g. `primary`, `neutral`, `accent`, `error`)
> - A hex value (e.g. `#3B82F6`)
>
> You can add as many colors as you like.

**3. Color space**
> Which color space should be used to compute the shades?
> - **OKLCH** — perceptually uniform, recommended for modern systems
> - **LCH** — perceptually uniform, wider browser support
> - **OKLAB** — perceptually uniform, no hue rotation
> - **HSL** — classic HSL (not perceptually uniform)
> - **P3** — wide-gamut Display P3

**4. Scale preset**
> Which stop structure should be used?
> - **Material** — 50–1000, 10 stops
> - **Tailwind** — 50–950, 11 stops
> - **Ant Design** — 1–10, 10 stops
> - **Radix** — 1–12, 12 stops

**5. Themes**
> How many themes do you need?
> - **Light only**
> - **Light + Dark**
> - **Custom** — describe the themes you want

### Optional (use defaults if not specified)

| Parameter | Default |
| --------- | ------- |
| Algorithm version | `v3` |
| Chroma shift | `100` (no change) |
| Hue shift | `0` (no rotation) |
| Source colors locked | `false` |

Once all required answers are collected, build the `get_full_palette` input and proceed to Step 1.

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

1. build the palette with `get_full_palette`
2. extract only `theme.name`, `color.name`, `shade.name`, `shade.hex`, and preferred text color
3. create a compact swatch matrix spec
4. hand that spec off to the relevant design workflow/tool

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

## Workflow

1. Collect source colors from the user or from a previous **generate-source-colors** step.
2. Call `get_full_palette` with a `BaseConfiguration` and at least one `ThemeConfiguration` to generate the full palette with scales.
3. **Do NOT read or summarize the full `PaletteData` result.** The response is a large JSON object with many color values — reading it wastes tokens.
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

- **Token efficiency**: Never read, print, or summarize the `PaletteData` JSON. It contains dozens of color shades with multiple color-space values each. Pass it opaquely to downstream skills.
- **Visual preview efficiency**: For previews, extract only `theme.name`, `color.name`, `shade.name`, and `shade.hex`, plus preferred text color when available.
- **Hex to rgb conversion**: Divide each 0–255 channel by 255 to get the 0–1 value. E.g. `#3B82F6` → `r: 59/255 = 0.23`, `g: 130/255 = 0.51`, `b: 246/255 = 0.96` → `{ r: 0.23, g: 0.51, b: 0.96 }`.
- **Scale computation**: If the user doesn't provide a `scale` object, compute it from the preset: distribute lightness values between `min` (darkest) and `max` (lightest) across `stops` using the `easing` function. First stop → `max`, last stop → `min`.
- **Design-first requests**: If the user asks for a board, canvas, style tiles, swatches, or a document preview, prioritize the visual/design-tool route before code export.
- When the user mentions a specific framework, pick the matching format automatically.
- For design token workflows, prefer `dtcg-tokens` for interoperability or `style-dictionary-v3` for Style Dictionary pipelines.
- Suggest `tailwind-v4` over `tailwind-v3` for new projects.
- Use `OKLCH` or `P3` color spaces for wide-gamut displays.
- The `paletteData` input to `generate_code` must be the full object from `get_full_palette` — it contains `name`, `description`, `themes` (with color scales), and `type`.
- This skill combines well with `ui-color-palette-generate-source-colors` (generate colors first, then build here), `ui-color-palette-audit-palette` (check readability after building), `ui-color-palette-generate-code` (export as code), and `ui-color-palette-manage-palettes` (publish after building).

---

## Recommended subagents

- **`palette-codegen`** — normalizes `PaletteData` and generates code/tokens; use after this skill when code export is needed
- **`palette-transitioner`** — converts `PaletteData` into `variableRows`, `tokenRows`, `styleRows`, or `swatchRows` before routing to a platform workflow
