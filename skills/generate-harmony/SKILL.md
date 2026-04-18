---
name: generate-harmony
description: Generate color harmonies (complementary, analogous, triadic, tetradic, split-complementary, square) from a base color. Use when the user wants to explore color relationships or build a harmonious palette from a single color.
argument-hint: <color> [harmony-type]
---

# Generate Color Harmony

Use the **ui-color-palette** MCP tool `create_color_harmony`.

## MCP tool reference

**Tool**: `create_color_harmony`

**Input schema**:

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `baseColor` | `[number, number, number]` | Yes | RGB tuple, e.g. `[59, 130, 246]` for #3B82F6 |
| `type` | enum | No | `COMPLEMENTARY`, `SPLIT_COMPLEMENTARY`, `ANALOGOUS`, `TRIADIC`, `TETRADIC`, `SQUARE`, or `ALL` (default: `ALL`) |
| `analogousSpread` | number | No | Spread angle in degrees for analogous harmonies |
| `returnFormat` | enum | No | `rgb`, `hex`, or `both` (default: `both`) |

## Workflow

1. Convert the user's color input (hex, RGB, HSL, color name) to an **RGB tuple** `[r, g, b]` where each value is 0–255.
2. Call `create_color_harmony` with `baseColor` and the desired `type`.
3. Present the resulting colors with hex values and their role in the harmony (base, complement, triad 1, etc.).
4. Suggest follow-ups: generate a full palette (`get_full_palette`), export to code (`generate_code`), or audit contrast.

## Arguments

Parse `$ARGUMENTS` as: `<color> [harmony-type]`.

- `/ui-color-palette:generate-harmony #3B82F6 triadic` → `baseColor: [59, 130, 246]`, `type: TRIADIC`
- `/ui-color-palette:generate-harmony rgb(30, 41, 59)` → `baseColor: [30, 41, 59]`, `type: ALL`
- If no harmony type is given, use `ALL` to return every harmony.
