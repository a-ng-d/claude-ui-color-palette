---
name: ui-color-palette-generate-code
description: Export a PaletteData object as code or design tokens. Uses generate_code to output in any format (CSS, SCSS, Less, Tailwind v3/v4, SwiftUI, UIKit, Compose, Android resources, DTCG, Style Dictionary, CSV, etc.). Use when the user wants to export a built palette for development.
argument-hint: <format> [color-space]
---

# Export Palette as Code

Use the **ui-color-palette** MCP tool `generate_code` to export a built `PaletteData` object into the requested code or token format.

This skill covers code export only. To build a palette first, use `ui-color-palette-scale-palette`.

---

## Tool — `generate_code`

| Parameter     | Type   | Required | Description                                             |
| ------------- | ------ | -------- | ------------------------------------------------------- |
| `paletteData` | object | Yes      | The `PaletteData` object returned by `get_full_palette` |
| `format`      | enum   | No       | Output format (default: `css`) — see table below        |
| `colorSpace`  | enum   | No       | Color space for output values (default: `RGB`)          |

### `format` values

| Value                 | Description                                   | `colorSpace` used? |
| --------------------- | --------------------------------------------- | ------------------ |
| `css`                 | CSS custom properties (`--color-name: value`) | Yes                |
| `scss`                | SCSS variables (`$color-name: value`)         | Yes                |
| `less`                | Less variables (`@color-name: value`)         | Yes                |
| `tailwind-v3`         | Tailwind CSS v3 `theme.extend.colors` config  | No                 |
| `tailwind-v4`         | Tailwind CSS v4 `@theme` block                | No                 |
| `swift-ui`            | SwiftUI `Color` extensions                    | No                 |
| `ui-kit`              | UIKit `UIColor` extensions                    | No                 |
| `compose`             | Jetpack Compose `Color()` constants           | No                 |
| `resources`           | Android XML color resources                   | No                 |
| `csv`                 | CSV spreadsheet (name, hex, rgb columns)      | No                 |
| `native-tokens`       | Native JSON token format                      | No                 |
| `dtcg-tokens`         | DTCG (Design Tokens Community Group) JSON     | Yes                |
| `style-dictionary-v3` | Style Dictionary v3 token format              | No                 |
| `universal-json`      | Universal JSON (flat key/value)               | No                 |

### `colorSpace` values

`RGB` · `LCH` · `LAB` · `HSL` · `OKLCH` · `OKLAB` · `P3`

Only applies to `css`, `scss`, `less`, and `dtcg-tokens`. Other formats use their own fixed color representation.

---

## Workflow

1. Confirm the `PaletteData` is available from a previous `get_full_palette` call.
2. Ask the user which format(s) and color space they want if not already specified.
3. Call `generate_code` with the raw `PaletteData` and the desired `format`/`colorSpace`.
4. Present the generated code in a fenced code block with the appropriate language tag.
5. Offer to write the output to a file in the project.
6. If the user wants to commit or open a PR, hand off to `gh-cli` or `gitlab-cli-skills`.

## Arguments

`$ARGUMENTS` can be a format, a format + color space, or a description of the target.

- `/ui-color-palette:generate-code tailwind-v4`
- `/ui-color-palette:generate-code css oklch`
- `/ui-color-palette:generate-code dtcg-tokens P3`
- `/ui-color-palette:generate-code scss variables for my design system`

## Tips

- **Token efficiency**: Never read, print, or summarize the `PaletteData` JSON. It contains dozens of color shades with multiple color-space values each. Always pass it opaquely to `generate_code`.
- The `paletteData` input must be the full object from `get_full_palette` — it contains `name`, `description`, `themes` (with color scales), and `type`.
- When the user mentions a specific framework, pick the matching format automatically.
- For design token workflows, prefer `dtcg-tokens` for interoperability or `style-dictionary-v3` for Style Dictionary pipelines.
- Suggest `tailwind-v4` over `tailwind-v3` for new projects.
- Use `OKLCH` or `P3` color spaces for wide-gamut displays.

---

## Recommended subagent

Delegate this skill to **`palette-codegen`** for multi-format or normalized projection workflows.

- **`palette-codegen`** — normalizes `PaletteData`, selects the right projection, and generates code in the requested format
