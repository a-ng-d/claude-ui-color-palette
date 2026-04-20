---
name: ui-color-palette-penpot-generate-styles
description: Generate or sync Penpot local color styles from a UI Color Palette. Use when the user wants reusable local styles or swatches in Penpot.
argument-hint: <palette-id|current-palette> [sync]
---

# Generate Penpot Styles

Use this skill when the user wants a palette projected into **Penpot local color styles**.

Styles are useful for:

- visual swatch libraries
- reusable local colors in mockups
- quick inspection of palette output inside Penpot
- design review workflows based on visible style libraries

## Backing operations

This skill maps to the plugin bridge workflow:

- `createLocalStyles()`
- `updateLocalStyles()`

These plugin operations are only a reference implementation. An agent should be able to perform the same work directly through Penpot API requests.

## Equivalent agent-side API requests

When not relying on the plugin action, use the equivalent Penpot API flow:

1. Read and flatten the palette into `paletteName`, `themeName`, `colorName`, `shadeName`, `hex`, and alpha.
2. Request local library colors/styles.
3. Build the canonical `path` and terminal style `name`.
4. Find or create the local style.
5. Update style path, style name, color, and opacity.
6. If deep sync is desired, remove orphan local styles.

Behavior supported by the plugin:

- creates missing local styles
- names styles using palette/theme/color/shade paths
- updates style color and opacity
- updates style path and style name
- optionally removes orphan styles when deep sync is enabled

## Naming model

Styles are stored with:

- `path`: `paletteName / themeName / colorName`
- `name`: `shadeName`

This gives Penpot a cleaner split between folder path and terminal style name.

## Workflow

1. Ensure a palette exists in the current Penpot plugin context.
2. Run local style sync for the selected/current palette.
3. Confirm the result in terms of:
   - styles created
   - styles updated
   - styles removed
4. If the user wants the semantic token layer as well, recommend using `ui-color-palette-penpot-generate-tokens` first or next.
5. If the user wants a visible palette board, route next to a document preview workflow.

## Tokens vs styles

Prefer this distinction:

- **Tokens**: semantic color system
- **Styles**: visual/application layer for local colors

If the user says only “Penpot tokens”, use the tokens skill first.
If the user says “styles”, “local colors”, or “swatches”, use this skill.

## When to use

Use this skill when the user asks for:

- Penpot styles
- Penpot local colors
- swatches in Penpot
- reusable local color styles
- color style library generation in Penpot

## Output

Report a concise sync summary, for example:

- styles created: `18`
- styles updated: `12`
- styles removed: `0`

Do not print the full palette payload.

## Tips

- Styles are for visual reuse, not the primary token graph.
- For theme-heavy systems, generate tokens first, then styles if the user also needs a style library.
- If the user wants an actual review artifact in the file, pair this with a document/board preview.
