---
description: Generate color harmonies (complementary, analogous, triadic, tetradic, split-complementary, square) from a base color. Use when the user wants to explore color relationships or build a harmonious palette from a single color.
---

# Generate Color Harmony

Use the **ui-color-palette** MCP tool `create_color_harmony` to produce a set of harmonious colors from a base color.

## Workflow

1. Ask the user for a **base color** (hex, RGB, HSL, or color name) and the desired **harmony type** (complementary, analogous, triadic, tetradic, split-complementary, square).
2. Call `create_color_harmony` with the base color and harmony type.
3. Present the resulting colors as a list with hex values, names, and a visual description.
4. Optionally suggest generating a full palette (`get_full_palette`) or exporting to code (`generate_code`).

## Arguments

If the user provides `$ARGUMENTS`, parse it as: `<color> [harmony-type]`.

- Example: `/ui-color-palette:generate-harmony #3B82F6 triadic`
- If no harmony type is given, default to **complementary**.

## Output format

Display each color with:

- Hex value
- Descriptive name (if available)
- Relative position in the harmony (e.g. "base", "complement", "triad 1")
