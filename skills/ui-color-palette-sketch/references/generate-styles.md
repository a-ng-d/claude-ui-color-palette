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

## Structure-first execution

Use this file as a workflow specification, not as an API catalog.

Execution order:

1. identify the target artifact: shared styles
2. reduce the palette to the minimum style payload
3. apply the sync workflow
4. only then map the workflow to MCP or plugin API calls

The API layer is secondary to the workflow structure.

## Input contract

Before synchronization, the agent should ensure:

- a palette is already available in the active plugin or MCP context
- the target palette is selected explicitly or can be inferred as the current palette
- palette data includes stable palette, theme, color, and shade naming
- each shade exposes a usable `hex` value

If one of these conditions is missing, resolve that upstream before style sync.

## Normalized PaletteData projection

Reduce `PaletteData` to a style-ready row model before execution:

- `paletteName`
- `themeName`
- `colorName`
- `shadeName`
- `styleName` (full path, used as the single `name` field): segments joined with `/` (no spaces)
  - no themes: `paletteName/colorName/shadeName`
  - with themes: `paletteName/themeName/colorName/shadeName` (theme name falls back to localized default if empty)
  - empty segments are filtered out
- `hex`: raw hex string from `shade.hex`

> Note: Sketch styles have no separate `alpha` field — only `hex` is used. This differs from Figma (GL + alpha) and Penpot (hex + alpha).

This normalized row model is the actual handoff from palette structure to Sketch shared style operations.

## Backing operations

This skill maps to the plugin bridge workflow:

- `createLocalStyles()`
- `updateLocalStyles()`

These plugin operations are only a reference implementation. An agent should be able to perform the same work directly through Sketch API requests.

## Equivalent agent-side API requests

When not relying on the plugin action, use the equivalent Sketch API flow:

**Case A — palette with no themes** (all shades have `id.includes('00000000000')`):

1. Flatten the palette into shade rows (`colorName`, `shadeName`, `hex`).
2. Request `Document.sharedLayerStyles`.
3. For each shade row:
   - Skip if `hex` is undefined.
   - Compute `styleName`: `[paletteName, colorName, shadeName].filter(s => s !== '').join('/')`
   - Find the existing style by stored `styleId` via `localStyles.find(s => s.id === styleId)`. If not found, create: `new LocalStyle({ name: styleName, hex })`.
   - Track the returned `sharedColorStyle.id`.
4. Call `Settings.setDocumentSettingForKey(Document, 'ui_color_palettes', currentPalettes)` then `Document.save()`.

**Case B — palette with themes** (shades without `'00000000000'` in id):

1. Flatten the palette into theme rows (`themeName`, `colorName`, `shadeName`, `hex`).
2. For each shade row:
   - Skip if `hex` is undefined.
   - Compute `styleName`: `[paletteName, themeName, colorName, shadeName].filter(s => s !== '').join('/')` (theme name falls back to localized default if empty)
   - Find or create as above.
3. Persist as above.

Behavior supported by the plugin:

- deduplicates by `styleId` (looks up existing styles by stored id)
- creates missing shared layer styles
- names styles with `/` as group separator (Sketch parses this as a folder hierarchy)
- sets fill color from `hex` only (no alpha)
- skips shades where `hex` is undefined
- persists palette state to document settings and calls `Document.save()`

## Sketch mapping

| UI Color Palette data | Sketch target |
| --------------------- | ------------- |
| No-theme palette | `paletteName/colorName/shadeName` as shared style name |
| Themed palette | `paletteName/themeName/colorName/shadeName` as shared style name |
| `shade.hex` | Style fill color (no alpha channel) |

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
