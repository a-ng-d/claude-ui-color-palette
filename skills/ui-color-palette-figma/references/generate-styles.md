---
name: ui-color-palette-figma-generate-styles
description: Generate or sync Figma local paint styles from a UI Color Palette. Use when the user wants swatches or reusable paint styles created from the palette in Figma.
argument-hint: <palette-id|current-palette> [sync]
---

# Generate Figma Styles

Use this skill when the user wants a palette projected into **Figma local paint styles**.

Styles are useful for:

- visual swatch libraries
- fill style reuse in mockups
- quick inspection of palette output inside Figma
- compatibility with legacy style-based workflows

## Structure-first execution

Use this file as a workflow specification, not as an API catalog.

Execution order:

1. identify the target artifact: styles
2. reduce the palette to the minimum style payload
3. apply the sync workflow
4. only then map the workflow to MCP or plugin API calls

The API layer is secondary to the workflow structure.

## Input contract

Before synchronization, the agent should ensure:

- a palette is already available in the active plugin or MCP context
- the target palette is selected explicitly or can be inferred as the current palette
- palette data includes stable palette, theme, color, and shade naming
- each shade exposes RGBA plus optional description

If one of these conditions is missing, resolve that upstream before style sync.

## Normalized PaletteData projection

Reduce `PaletteData` to a style-ready row model before execution:

- `paletteName`
- `themeName`
- `colorName`
- `shadeName`
- `stylePath`: `paletteName/themeName/colorName/shadeName`
- `rgba`
- `alpha`
- `description`

This normalized row model is the actual handoff from palette structure to Figma paint style operations.

## Backing operations

This skill maps to the plugin bridge workflow:

- `SYNC_LOCAL_STYLES`
- internally: `createLocalStyles()` then `updateLocalStyles()`

These plugin operations are only a reference implementation. An agent should be able to perform the same work directly through Figma API requests.

## Equivalent agent-side API requests

When not relying on the plugin action, use the equivalent Figma API flow:

1. Read the palette data and flatten it to `paletteName`, `themeName`, `colorName`, `shadeName`, RGBA, alpha, and description.
2. Request local paint styles.
3. For each palette shade, build the canonical style path.
4. Find an existing style by ID or canonical path; otherwise create a new paint style.
5. Update style name, description, fill color, and opacity.
6. If deep sync is desired, remove orphan local paint styles.

Behavior supported by the plugin:

- creates missing local paint styles
- names styles using palette/theme/color/shade paths
- updates fill color, opacity, name, and description
- optionally removes orphan styles when deep sync is enabled

## Naming model

Styles are generated using a hierarchical path:

`paletteName/themeName/colorName/shadeName`

For palettes without explicit theme splitting, the theme segment may be omitted.

## Workflow

1. Ensure a palette exists in the current Figma plugin context.
2. Run local style sync for the selected/current palette.
3. Confirm the result in terms of:
   - styles created
   - styles updated
   - styles removed
4. If the user wants tokens as the main system, recommend generating variables as well.
5. If the user wants a visible board or sheet, route next to `CREATE_DOCUMENT`.

## When to use

Use this skill when the user asks for:

- Figma styles
- local paint styles
- palette swatches in Figma
- reusable fills from the palette
- color style library generation

## Variables vs styles

Prefer this distinction:

- **Variables**: token system and theme logic
- **Styles**: visual/application layer for fills

If the user says only “tokens”, use the variables skill first.
If the user says “I want swatches/styles in Figma”, use this skill.

## Output

Report a concise sync summary, for example:

- styles created: `18`
- styles updated: `12`
- styles removed: `0`

Do not print the full palette payload.

## Tips

- Styles are best for visual reuse, not as the primary token graph.
- Theme-heavy systems should usually generate variables first, then styles if needed.
- If the user wants to inspect the palette visually, pair this with a document preview.
