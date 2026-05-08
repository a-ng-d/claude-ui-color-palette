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

## Structure-first execution

Use this file as a workflow specification, not as an API catalog.

Execution order:

1. identify the target artifact: local styles
2. reduce the palette to the minimum style payload
3. apply the sync workflow
4. only then map the workflow to MCP or plugin API calls

The API layer is secondary to the workflow structure.

## Input contract

Before synchronization, the agent should ensure:

- a palette is already available in the active plugin or MCP context
- the target palette is selected explicitly or can be inferred as the current palette
- palette data includes stable palette, theme, color, and shade naming
- each shade exposes `hex`, `alpha`, and optional description

If one of these conditions is missing, resolve that upstream before style sync.

## Normalized PaletteData projection

Reduce `PaletteData` to a style-ready row model before execution:

- `paletteName`
- `themeName`
- `colorName`
- `shadeName`
- `styleName` (full Penpot color name, used as-is): segments joined with ` / ` (space-slash-space)
  - no themes: `paletteName / colorName / shadeName`
  - with themes: `paletteName / themeName / colorName / shadeName` (theme name falls back to localized default if empty)
  - empty segments are filtered out
- `hex`: 6-character hex string (first 7 chars of `shade.hex`, e.g. `'#RRGGBB'`)
- `alpha`: opacity in `[0, 1]`

This normalized row model is the actual handoff from palette structure to Penpot local style operations.

## Backing operations

This skill maps to the plugin bridge workflow:

- `createLocalStyles()`
- `updateLocalStyles()`

These plugin operations are only a reference implementation. An agent should be able to perform the same work directly through Penpot API requests.

## Equivalent agent-side API requests

When not relying on the plugin action, use the equivalent Penpot API flow:

**Case A — palette with no themes** (all shades have `id.includes('00000000000')`):

1. Flatten the palette into shade rows (`colorName`, `shadeName`, `hex`, `alpha`).
2. For each shade row:
   - Skip the shade if `hex` is undefined.
   - Compute `styleName`: `[paletteName, colorName, shadeName].filter(s => s !== '').join(' / ')`
   - Find the existing style by stored `styleId` via `penpot.library.local.colors.find(s => s.id === styleId)`. If not found, create: `new LocalStyle({ name: styleName, hex: hex.substring(0, 7), alpha })`.
   - Track the returned `libraryColor.id`.

**Case B — palette with themes** (shades without `'00000000000'` in id):

1. Flatten the palette into theme rows (`themeName`, `colorName`, `shadeName`, `hex`, `alpha`).
2. For each shade row:
   - Skip the shade if `hex` is undefined.
   - Compute `styleName`: `[paletteName, themeName, colorName, shadeName].filter(s => s !== '').join(' / ')` (theme name falls back to localized default if empty)
   - Find or create the style as above.

Behavior supported by the plugin:

- creates missing local styles
- names styles using ` / ` (space-slash-space) as group separator
- the full path including shade name is stored as the single `name` field on the color
- color is set from `hex.substring(0, 7)` (strips alpha channel from 8-char hex if present)
- opacity is set from `alpha` separately
- skips shades where `hex` is undefined
- saves palette back to plugin data directly (no size limit check for styles)

## Naming model

Styles are stored as a single `name` string in Penpot, using ` / ` (space-slash-space) as the group separator:

- no themes: `paletteName / colorName / shadeName`
- with themes: `paletteName / themeName / colorName / shadeName`

This is different from Figma which uses `/` without spaces. Penpot parses ` / ` to build the folder hierarchy.

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
