---
name: ui-color-palette-framer-generate-styles
description: Generate and update Framer local color styles from a UI Color Palette. Use when the user wants reusable Framer color styles created and kept in sync.
argument-hint: <palette-id|current-palette> [sync]
---

# Generate Framer Styles

Use this skill when the user wants a palette projected into **Framer color styles**.

In this plugin, the Framer integration supports a full `create + update` workflow for local color styles.

## Structure-first execution

Use this file as a workflow specification, not as an API catalog.

Execution order:

1. identify the target artifact: color styles
2. reduce the palette to the minimum style payload
3. apply the sync workflow
4. only then map the workflow to MCP or plugin API calls

The API layer is secondary to the workflow structure.

## Input contract

Before synchronization, the agent should ensure:

- a palette is already available in the active plugin or MCP context
- the target palette is selected explicitly or can be inferred as the current palette
- palette data includes stable palette, theme, color, and shade naming
- each shade exposes the color data needed to derive `light` and optional `dark` values

If one of these conditions is missing, resolve that upstream before style sync.

## Normalized PaletteData projection

Reduce `PaletteData` to a style-ready row model before execution:

- `paletteName`
- `themeName`
- `colorName`
- `shadeName`
- `stylePath`: `paletteName/themeName/colorName/shadeName`
- `light`
- `dark`
- `description`

This normalized row model is the actual handoff from palette structure to Framer color style operations.

## Backing operations

This skill maps to the plugin bridge workflow:

- `createLocalStyles()`
- `updateLocalStyles()`
- UI action: `SYNC_LOCAL_STYLES`

These plugin operations are only a reference implementation. An agent should be able to perform the same work directly through Framer API requests.

## Equivalent agent-side API requests

When not relying on the plugin action, use the equivalent Framer API flow:

1. Read and flatten the palette into canonical style paths plus `light` and `dark` color values.
2. Request local color styles.
3. For each palette shade, find or create the style when permissions allow it.
4. Update style name, path, `light`, and `dark` values.
5. If deep sync is desired, remove orphan color styles when permissions allow it.
6. Treat synchronization as `create + update`, not creation only.

Behavior supported by the plugin:

- creates missing color styles
- updates style name, path, light value, and dark value
- optionally removes orphan styles when deep sync is enabled
- respects Framer permission checks such as:
  - `createColorStyle`
  - `ColorStyle.setAttributes`
  - `ColorStyle.remove`

## Framer mapping

| UI Color Palette data | Framer target |
| --------------------- | ------------- |
| `paletteName/themeName/colorName/shadeName` | Style path + name |
| Shade RGB/RGBA | `light` style value |
| Opposite shade in same family | `dark` style value when available |

## Important note

This Framer implementation does not expose a separate variables/tokens layer in the same way as Figma Variables or Penpot Tokens.

For Framer, the practical reusable color layer is **color styles**.

## Workflow

1. Ensure the palette exists in the current Framer plugin state.
2. Prefer the selected/current palette unless the user specifies a palette ID.
3. Run the Framer style sync workflow.
4. Always think of the sync as `create + update`, not only creation.
5. Confirm the result in terms of:
   - styles created
   - styles updated
   - styles removed
6. If the user also wants a visible artifact, route next to document preview generation.

## When to use

Use this skill when the user asks for:

- Framer color styles
- local styles in Framer
- reusable palette styles
- keep Framer styles in sync
- generate and update styles in Framer

## Output

Return a concise sync summary, for example:

- styles created: `18`
- styles updated: `12`
- styles removed: `2`

Do not dump the full palette payload.

## Tips

- For Framer, styles are the main reusable color artifact.
- Always include the update step after creation when the intent is synchronization.
- If the user wants a visual review artifact, pair style sync with document preview generation.
- If deep cleanup is required, ensure deep sync for styles is enabled.
