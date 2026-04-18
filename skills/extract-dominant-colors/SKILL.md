---
name: extract-dominant-colors
description: Extract dominant colors from an image using k-means clustering. Use when the user wants to derive a color palette from a photo, illustration, screenshot, or any image.
argument-hint: <image-url> [color-count]
---

# Extract Dominant Colors

Use the **ui-color-palette** MCP tool `extract_dominant_colors`.

## MCP tool reference

**Tool**: `extract_dominant_colors`

**Input schema**:

| Parameter         | Type    | Required | Description                                               |
| ----------------- | ------- | -------- | --------------------------------------------------------- |
| `imageUrl`        | string  | Yes      | Public URL of the image (JPEG or PNG only)                |
| `colorCount`      | number  | No       | Number of dominant colors to extract (default: 5)         |
| `maxIterations`   | number  | No       | Maximum iterations for k-means clustering (default: 10)   |
| `tolerance`       | number  | No       | Convergence tolerance — lower = more precise (default: 1) |
| `skipTransparent` | boolean | No       | Skip transparent pixels in PNGs (default: true)           |

**Supported formats**: `image/jpeg`, `image/png`

**Returns**: An array of dominant colors with RGB values and proportional weight.

## Workflow

1. Get the image URL from the user — it must be a publicly accessible JPEG or PNG.
2. Call `extract_dominant_colors` with the `imageUrl` and optional tuning parameters.
3. Present the extracted colors as a visual table:
   - Color swatch (hex), RGB values, weight/proportion
4. Offer follow-up actions:
   - Feed the colors into `get_full_palette` to build a full theme with scales
   - Generate color harmonies with `create_color_harmony` using each dominant color as a base
   - Audit contrast between the dominant colors with the `audit-contrast` skill
   - Export to code with the `generate-code` skill
   - Sync to a design tool with the `sync-design-variables` skill

## Arguments

`$ARGUMENTS` is the image URL, optionally followed by a color count.

- `/ui-color-palette:extract-dominant-colors https://example.com/photo.jpg`
- `/ui-color-palette:extract-dominant-colors https://example.com/photo.png 8`

## Tips

- The `imageUrl` must be publicly accessible (no auth headers are sent when fetching it).
- For better results on complex images, increase `colorCount` to 8–10.
- For illustrations or flat graphics, 3–5 colors usually suffice.
- Lower `tolerance` (e.g. 0.5) produces more accurate clusters but takes longer.
- Increase `maxIterations` (e.g. 20) for images with subtle color gradients.
- Enable `skipTransparent` for PNGs with transparency to avoid counting empty space.
- The MCP tool only accepts `imageUrl` — direct file upload (multipart/form-data) is supported by the API but not exposed through the MCP layer.
