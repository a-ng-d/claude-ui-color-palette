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
- `styleName` (full Figma style path, used as both path and name): `paletteName/colorName/shadeName` (no themes) or `paletteName/themeName/colorName/shadeName` (with themes) — empty segments filtered out
- `gl`: OpenGL-normalized RGB triple `[r, g, b]` in `[0, 1]` range (from `shade.gl`)
- `alpha`: opacity in `[0, 1]`
- `description`

This normalized row model is the actual handoff from palette structure to Figma paint style operations.

## Backing operations

This skill maps to the plugin bridge workflow:

- `SYNC_LOCAL_STYLES`
- internally: `createLocalStyles()` then `updateLocalStyles()`

These plugin operations are only a reference implementation. An agent should be able to perform the same work directly through Figma API requests.

## Equivalent agent-side API requests

When not relying on the plugin action, use the equivalent Figma API flow:

**Case A — palette with no themes** (all shades identified by `id.includes('00000000000')`):

1. List all local paint styles.
2. For each shade row, compute `styleName`:
   ```
   [paletteName, colorName, shadeName].filter(s => s !== '').join('/')
   ```
3. Skip the shade if `gl` is undefined.
4. Find the existing paint style by stored `styleId`; if not found, create a new one: `figma.createPaintStyle()`.
5. Set `style.name = styleName`.
6. Set `style.description`.
7. Set fills: `[{ type: 'SOLID', color: { r: gl[0], g: gl[1], b: gl[2] }, opacity: alpha }]`.
8. Track the returned `style.id`.

**Case B — palette with themes** (shades without `'00000000000'` in id):

1. Same as Case A but compute `styleName` as:
   ```
   [paletteName, themeName, colorName, shadeName].filter(s => s !== '').join('/')
   ```
   where `themeName` falls back to a default label when empty.
2. Otherwise identical to Case A.

3. If deep sync is desired, remove orphan local paint styles.

Behavior supported by the plugin:

- creates missing local paint styles
- names styles using the full hierarchical path as a single `style.name` string (Figma parses `/` as groups)
- sets fill color from `gl` (OpenGL normalized) + `alpha`
- skips shades where `gl` is undefined
- optionally removes orphan styles when deep sync is enabled

## Naming model

Figma interprets `/` in a paint style name as a group separator. The full style path is set as a single `style.name` string:

- no themes: `paletteName/colorName/shadeName`
- with themes: `paletteName/themeName/colorName/shadeName`

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
