---
name: ui-color-palette-figma-generate-variables
description: Generate or sync Figma local variables from a UI Color Palette. Use when the user wants palette colors turned into Figma Variables collections and modes.
argument-hint: <palette-id|current-palette> [sync]
---

# Generate Figma Variables

Use this skill when the user wants to push a generated palette into **Figma local variables**.

In Figma, variables are the primary token system. For UI Color Palette, this workflow creates or updates:

- one local variable collection for the palette
- one mode per theme when themes exist
- one variable per `color/shade`
- variable descriptions from palette metadata when available

## Source of truth

Treat **Figma variables** as the source of truth for tokens.

- Variables represent the token system
- Modes represent themes
- Variable names map to `colorName/shadeName`
- Collection name maps to the palette name

If the user asks for “Figma tokens”, prefer this skill first.

## Structure-first execution

Use this file as a workflow specification, not as an API catalog.

Execution order:

1. identify the target artifact: variables
2. reduce the palette to the minimum variable payload
3. apply the sync workflow
4. only then map the workflow to MCP or plugin API calls

The API layer is secondary to the workflow structure.

## Input contract

Before synchronization, the agent should ensure:

- a palette is already available in the active plugin or MCP context
- the target palette is selected explicitly or can be inferred as the current palette
- palette data includes stable color, shade, and theme naming
- each shade exposes a usable color value and optional description

If one of these conditions is missing, resolve that upstream before variable sync.

## Normalized PaletteData projection

Reduce `PaletteData` to a variable-ready row model before execution:

- `paletteName`
- `themeName`
- `colorName`
- `shadeName`
- `variableName`: `colorName/shadeName`
- `rgba`
- `alpha`
- `description`

This normalized row model is the actual handoff from palette structure to Figma variable operations.

## Backing operations

This skill maps to the plugin bridge workflow:

- `SYNC_LOCAL_VARIABLES`
- internally: `createLocalVariables()` then `updateLocalVariables()`

These plugin operations are only a reference implementation. An agent should be able to perform the same work directly through Figma API requests.

## Equivalent agent-side API requests

When not relying on the plugin action, use the equivalent Figma API flow:

1. Read the palette data and flatten it to the minimal variable payload: `themeName`, `colorName`, `shadeName`, RGBA, and description.
2. Request local variable collections.
3. Find the collection matching the palette name or create it.
4. For each theme, find or create the corresponding mode.
5. Request local variables scoped to that collection.
6. For each `colorName/shadeName`, find or create the variable.
7. Set or update the variable value for the target mode using RGBA.
8. Update variable name and description when they changed.
9. If deep sync is desired, remove orphan variables and orphan modes.

Behavior supported by the plugin:

- creates the collection if missing
- creates variables if missing
- creates/renames modes from theme names
- updates variable values, names, and descriptions
- optionally removes orphan variables and modes when deep sync is enabled

## Expected input

This skill assumes a palette already exists in the plugin state for the current Figma page.

Typical upstream flow:

1. generate or load a palette
2. store/select that palette in the plugin
3. run variable sync

If no palette exists, first use the palette creation flow before attempting variable generation.

## Workflow

1. Ensure the target palette exists in the current Figma context.
2. Prefer the selected/current palette unless the user specifies a palette ID.
3. Run the Figma variable sync flow.
4. Confirm the outcome in terms of:
   - collection created or reused
   - modes created, renamed, or removed
   - variables created, updated, or removed
5. If the user also wants visual artifacts, route next to:
   - `ui-color-palette-figma-generate-styles` for local paint styles
   - `CREATE_DOCUMENT` for a palette board/document preview

## Figma mapping

| UI Color Palette data | Figma target             |
| --------------------- | ------------------------ |
| `palette.base.name`   | Variable collection name |
| Theme                 | Variable mode            |
| `colorName/shadeName` | Variable name            |
| Shade RGBA            | Variable value           |
| Shade description     | Variable description     |

## When to use

Use this skill when the user asks for:

- Figma variables
- Figma color variables
- Figma token collection
- theme modes in Figma
- syncing a palette to variables

## Output

Report a concise operational summary, for example:

- collection: created or reused
- modes: `+2`, `~1`, `-0`
- variables: `+24`, `~24`, `-3`

Do not dump the full palette JSON.

## Tips

- In Figma, tokens should generally start as variables, not styles.
- When multiple themes exist, expect one mode per theme.
- If the user wants a strict cleanup of removed shades/themes, ensure deep sync behavior is enabled before sync.
- If the user wants a human-readable board, generate a document preview after syncing variables.
