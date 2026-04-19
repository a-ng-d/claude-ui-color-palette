---
name: ui-color-palette-generate-source-colors
description: Generate source colors for a palette — extract dominant colors from an image, generate colors from a natural language prompt, or create color harmonies from a base color. Use when the user wants to produce starting colors before building a full palette.
argument-hint: <image-url|prompt|color> [options]
---

# Generate Source Colors

Use the **ui-color-palette** MCP tools to produce source colors from any input: an image, a text prompt, or a single base color.

---

## 1 · Extract dominant colors from an image

**Tool**: `extract_dominant_colors`

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `imageUrl` | string | Yes | Public URL of the image (JPEG or PNG only) |
| `colorCount` | number | No | Number of dominant colors to extract (default: 5) |
| `maxIterations` | number | No | Maximum iterations for k-means clustering (default: 10) |
| `tolerance` | number | No | Convergence tolerance — lower = more precise (default: 1) |
| `skipTransparent` | boolean | No | Skip transparent pixels in PNGs (default: true) |

**Supported formats**: `image/jpeg`, `image/png`

**Returns**: An array of dominant colors with RGB values and proportional weight.

### Tips

- The `imageUrl` must be publicly accessible (no auth headers are sent when fetching it).
- For complex images, increase `colorCount` to 8–10. For flat graphics, 3–5 usually suffice.
- Lower `tolerance` (e.g. 0.5) produces more accurate clusters but takes longer.
- Increase `maxIterations` (e.g. 20) for images with subtle color gradients.
- Enable `skipTransparent` for PNGs with transparency to avoid counting empty space.

---

## 2 · Generate colors from a prompt

**Tool**: `generate_colors_from_prompt`

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `prompt` | string | Yes | Natural language description of the desired palette (e.g. "a warm sunset palette with oranges and pinks") |

**Returns**: An AI-generated palette object with color names and hex values.

### Tips

- Encourage descriptive prompts: mention mood, industry, temperature, and target audience.
- The prompt is sent to Mistral AI — be specific for better results.

---

## 3 · Create color harmonies

**Tool**: `create_color_harmony`

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `baseColor` | `[number, number, number]` | Yes | RGB tuple, e.g. `[59, 130, 246]` for #3B82F6 |
| `type` | enum | No | `COMPLEMENTARY`, `SPLIT_COMPLEMENTARY`, `ANALOGOUS`, `TRIADIC`, `TETRADIC`, `SQUARE`, or `ALL` (default: `ALL`) |
| `analogousSpread` | number | No | Spread angle in degrees for analogous harmonies |
| `returnFormat` | enum | No | `rgb`, `hex`, or `both` (default: `both`) |

### Tips

- Convert hex/HSL/color-name input to an RGB tuple `[r, g, b]` (0–255 each) before calling.
- If no harmony type is given, use `ALL` to return every harmony.

---

## Workflow

1. Identify the user's input type:
   - **Image URL** → call `extract_dominant_colors`
   - **Text description** → call `generate_colors_from_prompt`
   - **Single color** → call `create_color_harmony`
2. Present the resulting colors as a table with hex values, RGB, and role/weight.
3. Offer follow-ups:
   - Feed the colors into `get_full_palette` to build a full theme with scales
   - Combine tools (e.g. extract from image → generate harmonies for each dominant color)
   - Audit contrast with **audit-palette**
   - Export to code with **scale-palette**

## Arguments

`$ARGUMENTS` can be an image URL, a text prompt, or a color value.

- `/ui-color-palette:generate-source-colors https://example.com/photo.jpg 8`
- `/ui-color-palette:generate-source-colors a warm sunset over the ocean, professional and calm`
- `/ui-color-palette:generate-source-colors #3B82F6 triadic`
- `/ui-color-palette:generate-source-colors rgb(30, 41, 59)`
