---
name: ui-color-palette-sketch-generate-variables
description: Generate or sync Sketch local variables from a UI Color Palette. Use when the user wants palette colors turned into Sketch swatches/variables.
argument-hint: <palette-id|current-palette> [sync]
---

# Generate Sketch Variables

Use this skill when the user wants to push a generated palette into **Sketch local variables**, implemented in this plugin through **document swatches**.

In this Sketch workflow, variables are represented by swatches. For UI Color Palette, this creates or updates:

- one swatch per `palette/theme/color/shade`
- swatch names derived from the palette path
- updated swatch colors when the palette changes

## Source of truth

Treat **Sketch swatches** as the variable layer in this plugin.

- Swatches act as local variables
- Swatch names encode palette structure
- Color values come from palette shade hex values

If the user asks for “Sketch variables” or “Sketch color variables”, use this skill first.

## Structure-first execution

Use this file as a workflow specification, not as an API catalog.

Execution order:

1. identify the target artifact: swatches/variables
2. reduce the palette to the minimum swatch payload
3. apply the sync workflow
4. only then map the workflow to MCP or plugin API calls

The API layer is secondary to the workflow structure.

## Input contract

Before synchronization, the agent should ensure:

- a palette is already available in the active plugin or MCP context
- the target palette is selected explicitly or can be inferred as the current palette
- palette data includes stable palette, theme, color, and shade naming
- each shade exposes a usable `hex` value

If one of these conditions is missing, resolve that upstream before swatch sync.

## Normalized PaletteData projection

Reduce `PaletteData` to a swatch-ready row model before execution:

- `paletteName`
- `themeName`
- `colorName`
- `shadeName`
- `swatchName` (full path, used as the single `name` field): segments joined with `/` (no spaces)
  - no themes: `paletteName/colorName/shadeName`
  - with themes: `paletteName/themeName/colorName/shadeName` (theme name falls back to localized default if empty)
  - empty segments are filtered out
- `hex`: raw hex string from `shade.hex`

> Note: unlike Figma variables (which use GL + alpha + a collection/mode model) or Penpot tokens (sets + themes), Sketch swatches are simple name/hex pairs with no theme grouping or mode concept. Each themed shade becomes a separately named swatch.

This normalized row model is the actual handoff from palette structure to Sketch swatch operations.

## Backing operations

This skill maps to the plugin bridge workflow:

- `createLocalVariables()`
- `updateLocalVariables()`

These plugin operations are only a reference implementation. An agent should be able to perform the same work directly through Sketch API requests.

## Equivalent agent-side API requests

When not relying on the plugin action, use the equivalent Sketch API flow:

**Case A — palette with no themes** (all shades have `id.includes('00000000000')`):

1. Flatten the palette into shade rows (`colorName`, `shadeName`, `hex`).
2. Request `Document.swatches`.
3. For each shade row:
   - Skip if `hex` is undefined.
   - Compute `swatchName`: `[paletteName, colorName, shadeName].filter(s => s !== '').join('/')`
   - Find an existing swatch by **name** (not by id): `localSwatches.find(s => s.name === swatchName)`. If not found, create: `new LocalVariable({ name: swatchName, hex })`.
   - **No id is stored** — swatches are matched by name on every sync.
4. Call `Settings.setDocumentSettingForKey(Document, 'ui_color_palettes', currentPalettes)` then `Document.save()`.

**Case B — palette with themes** (shades without `'00000000000'` in id):

1. Flatten the palette into theme rows (`themeName`, `colorName`, `shadeName`, `hex`).
2. For each shade row:
   - Skip if `hex` is undefined.
   - Compute `swatchName`: `[paletteName, themeName, colorName, shadeName].filter(s => s !== '').join('/')` (theme name falls back to localized default if empty)
   - Find or create as above (match by name).
3. Persist as above.

Behavior supported by the plugin:

- deduplicates by swatch **name** (not by id — no id is persisted)
- creates missing swatches
- names swatches with `/` as group separator
- sets color from `hex` only
- skips shades where `hex` is undefined
- persists palette state to document settings and calls `Document.save()`

## Sketch mapping

| UI Color Palette data | Sketch target |
| --------------------- | ------------- |
| No-theme palette | `paletteName/colorName/shadeName` as swatch name |
| Themed palette | `paletteName/themeName/colorName/shadeName` as swatch name |
| `shade.hex` | Swatch color |
| (no id stored) | Matched by name on each sync |

## Workflow

1. Ensure the palette exists in the current Sketch document plugin state.
2. Prefer the current palette unless the user specifies a palette ID.
3. Sync local variables/swatches.
4. Confirm the result in terms of:
   - swatches created
   - swatches updated
   - swatches removed
5. If the user also wants reusable layer styles, route next to `ui-color-palette-sketch-generate-styles`.
6. If the user wants a visible board or sheet, route next to document preview.

## When to use

Use this skill when the user asks for:

- Sketch variables
- Sketch swatches
- Sketch color variables
- syncing palette colors to swatches

## Output

Report a concise operational summary, for example:

- swatches created: `24`
- swatches updated: `12`
- swatches removed: `3`

Do not dump the full palette JSON.

## Tips

- In this plugin, Sketch “variables” are implemented via document swatches.
- Theme-heavy palettes still flatten into named swatch paths.
- If the user wants a semantic design-token workflow, explain that Sketch here does not expose a separate token API like Penpot or Figma variables.
- If strict cleanup is required, ensure deep sync for variables is enabled.
