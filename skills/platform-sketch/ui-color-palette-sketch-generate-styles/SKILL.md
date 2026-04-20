---
name: ui-color-palette-sketch-generate-styles
description: Generate or sync Sketch shared layer styles from a UI Color Palette. Use when the user wants reusable local styles from the palette in Sketch.
argument-hint: <palette-id|current-palette> [sync]
---

# Generate Sketch Styles

Use this skill when the user wants a palette projected into **Sketch shared layer styles**.

Styles are useful for:

- reusable fills in mockups
- visual swatch/style libraries
- design review from applied color styles
- bridging palette data into existing Sketch style workflows

## Backing operations

This skill maps to the plugin bridge workflow:

- `createLocalStyles()`
- `updateLocalStyles()`

These plugin operations are only a reference implementation. An agent should be able to perform the same work directly through Sketch API requests.

## Equivalent agent-side API requests

When not relying on the plugin action, use the equivalent Sketch API flow:

1. Read and flatten the palette into canonical style paths and hex values.
2. Request shared layer styles from the current document.
3. For each palette shade, find or create the shared style.
4. Update shared style name and fill color when they changed.
5. If deep sync is desired, remove orphan shared styles.
6. Persist the document after synchronization.

Behavior supported by the plugin:

- creates missing shared layer styles
- names styles from the palette/theme/color/shade path
- updates style names and fill colors
- optionally removes orphan styles when deep sync is enabled

## Sketch mapping

| UI Color Palette data | Sketch target |
| --------------------- | ------------- |
| `paletteName/themeName/colorName/shadeName` | Shared style name |
| Shade hex | Style fill color |

## Workflow

1. Ensure a palette exists in the current Sketch document plugin state.
2. Run local style sync for the selected/current palette.
3. Confirm the result in terms of:
   - styles created
   - styles updated
   - styles removed
4. If the user wants the variable/swatch layer too, recommend using `ui-color-palette-sketch-generate-variables` first or next.
5. If the user wants a visible board or sheet, route next to document preview.

## Variables vs styles

Prefer this distinction:

- **Variables / swatches**: color source layer in this plugin
- **Styles**: reusable application layer for Sketch design surfaces

If the user says only “tokens” or “variables”, use the variables skill first.
If the user says “styles” or “shared styles”, use this skill.

## When to use

Use this skill when the user asks for:

- Sketch styles
- shared layer styles
- palette styles in Sketch
- reusable color styles

## Output

Report a concise sync summary, for example:

- styles created: `18`
- styles updated: `12`
- styles removed: `0`

Do not print the full palette payload.

## Tips

- Styles are the visual/application layer, not the main semantic token graph.
- If the user wants both maintainability and visual reuse, generate swatches first, then styles.
- Pair this with a document preview when the user wants an immediately reviewable artifact.
