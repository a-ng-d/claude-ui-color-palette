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

## Backing operations

This skill maps to the plugin bridge workflow:

- `createLocalVariables()`
- `updateLocalVariables()`

These plugin operations are only a reference implementation. An agent should be able to perform the same work directly through Sketch API requests.

## Equivalent agent-side API requests

When not relying on the plugin action, use the equivalent Sketch API flow:

1. Read and flatten the palette into canonical swatch paths and hex values.
2. Request the document swatches.
3. For each shade path, find or create the swatch.
4. Update swatch color when it changed.
5. If deep sync is desired, remove orphan swatches.
6. Persist document state after synchronization.

Behavior supported by the plugin:

- creates missing swatches
- updates swatch colors when values change
- optionally removes orphan swatches when deep sync is enabled
- stores palette state in document settings

## Sketch mapping

| UI Color Palette data | Sketch target |
| --------------------- | ------------- |
| `paletteName/themeName/colorName/shadeName` | Swatch name |
| Shade hex | Swatch color |

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
