---
name: scale-palette
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

**Returns**: A `PaletteData` object containing `name`, `description`, `themes` (with full color scales), and `type`.

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
3. Ask the user which format(s) and color space they want.
4. Call `generate_code` with the `PaletteData` from step 2 and the desired `format`/`colorSpace`.
5. Present the generated code in a fenced code block with the appropriate language tag.
6. Offer to write the output to a file in the project.

## Arguments

`$ARGUMENTS` can be a format, a format + color space, or a description of the target.

- `/ui-color-palette:scale-palette tailwind-v4`
- `/ui-color-palette:scale-palette css oklch`
- `/ui-color-palette:scale-palette dtcg-tokens P3`
- `/ui-color-palette:scale-palette scss variables for my design system`

## Tips

- When the user mentions a specific framework, pick the matching format automatically.
- For design token workflows, prefer `dtcg-tokens` for interoperability or `style-dictionary-v3` for Style Dictionary pipelines.
- Suggest `tailwind-v4` over `tailwind-v3` for new projects.
- Use `OKLCH` or `P3` color spaces for wide-gamut displays.
- The `paletteData` input to `generate_code` must be the full object from `get_full_palette` — it contains `name`, `description`, `themes` (with color scales), and `type`.
- This skill combines well with **generate-source-colors** (generate colors first, then build + export here) and **manage-palettes** (publish the palette after building).
