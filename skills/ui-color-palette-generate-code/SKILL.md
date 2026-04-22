---
name: ui-color-palette-generate-code
description: Export a PaletteData object as code or design tokens via the generate_code MCP tool. Supports CSS, SCSS, Less, Tailwind v3/v4, SwiftUI, UIKit, Compose, Android resources, DTCG, Style Dictionary, CSV, and more.
argument-hint: <format> [color-space]
---

# Export Palette as Code

Use the **ui-color-palette** MCP tool `generate_code` to export a `PaletteData` JSON into the requested format.

The `PaletteData` JSON comes from a previous `get_full_palette` call. It must be passed **as-is** — do not read, summarize, or transform it.

---

## Tool — `generate_code`

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `paletteData` | object | Yes | The `PaletteData` JSON from `get_full_palette` |
| `format` | enum | No | Output format (default: `css`) |
| `colorSpace` | enum | No | Color space for output values (default: `RGB`) |

### `format` values

| Value | Description | `colorSpace` used? |
| ----- | ----------- | ------------------ |
| `css` | CSS custom properties | Yes |
| `scss` | SCSS variables | Yes |
| `less` | Less variables | Yes |
| `tailwind-v3` | Tailwind CSS v3 config | No |
| `tailwind-v4` | Tailwind CSS v4 `@theme` block | No |
| `swift-ui` | SwiftUI `Color` extensions | No |
| `ui-kit` | UIKit `UIColor` extensions | No |
| `compose` | Jetpack Compose constants | No |
| `resources` | Android XML color resources | No |
| `csv` | CSV spreadsheet | No |
| `native-tokens` | Native JSON token format | No |
| `dtcg-tokens` | DTCG JSON | Yes |
| `style-dictionary-v3` | Style Dictionary v3 | No |
| `universal-json` | Universal JSON flat key/value | No |

`colorSpace` applies only to `css`, `scss`, `less`, and `dtcg-tokens`. Values: `RGB` · `LCH` · `LAB` · `HSL` · `OKLCH` · `OKLAB` · `P3`

---

## Workflow

1. Ask which `format` (and `colorSpace` if applicable) if not already specified.
2. Call `generate_code` with the `PaletteData` and chosen parameters.
3. Present the output in a fenced code block, then offer to write it to a file or open a PR via `gh-cli` / `gitlab-cli-skills`.

**Format hints**: prefer `tailwind-v4` over v3 for new projects — prefer `dtcg-tokens` for token interoperability.

Delegate this skill to **`palette-codegen`** for multi-format or normalized projection workflows.

- **`palette-codegen`** — normalizes `PaletteData`, selects the right projection, and generates code in the requested format
