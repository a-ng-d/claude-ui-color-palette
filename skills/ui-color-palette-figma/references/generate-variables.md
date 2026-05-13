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
- `shadeName` — includes `"source"` (the source/reference shade for each color family)
- `variableName`: `colorName/shadeName` (slash-separated, empty segments filtered out)
- `gl`: OpenGL-normalized RGB triple `[r, g, b]` in `[0, 1]` range (from `shade.gl`)
- `alpha`: opacity in `[0, 1]`
- `description`

This normalized row model is the actual handoff from palette structure to Figma variable operations.

## Sync behaviour

- **Collection**: one per palette, named `paletteName`. Find by stored `collectionId` or create.
- **No-theme palette**: single default mode, left as `'Mode 1'`. No-theme detection: all shade IDs contain `'00000000000'`.
- **Themed palette**: rename default mode to first theme name; `collection.addMode(themeName)` for each subsequent theme. Figma limits modes per plan — warn and stop if `addMode` throws.
- **Variables**: named `colorName/shadeName` (`/`-separated, `'None'`/empty filtered). Includes the `"source"` shade.
- **Values**: `{ r: gl[0], g: gl[1], b: gl[2], a: alpha }` per mode.
- Optionally removes orphan variables and modes when deep sync is enabled.

## SystemData workflow (semantic variable collection)

When `SystemData` is present in the conversation context, use this section instead of the standard palette workflow above.

### Step 0 — ensure primitives exist

Semantic variables alias existing primitive variables. Check that the palette's primitive collection exists (by stored `collectionId`). If not, run the full primitive sync first — **mandatory**.

### Step 1 — semantic collection

Create or find a collection named after the system schema or user label.

### Step 2 — modes

Mirror the primitive collection: leave default mode as `'Mode 1'` for no-theme; rename + add modes for themed. Track each `modeId` in theme order — must match `token.refs` index order.

### Step 3 — semantic variables with binding

For each token in `SystemData.tokens`:

1. **Skip** if `token.isExcluded === true`.
2. Variable name: `token.pathNames.filter(n => n !== '' && n !== 'None').join('/')`.
3. For each mode at theme index `i`:
   - **Skip** if `token.refs[i].shadeId === null` (unbound).
   - Find the primitive variable in the primitive collection whose id matches `ref.shadeId`. Skip with warning if not found.
   - Set value as alias: `{ type: 'VARIABLE_ALIAS', id: primitiveVariable.id }`.
4. Set `variable.description` if defined.

### SystemData Figma mapping

| `SystemData` field | Figma target |
| ------------------------------------------ | ------------------------------------------------------- |
| Schema name or user label | Semantic variable collection name |
| `token.pathNames.filter(...).join('/')` | Semantic variable name |
| One mode per theme | Collection mode (mirroring primitive collection) |
| `token.refs[i].shadeId` → primitive var id | `{ type: 'VARIABLE_ALIAS', id: primitiveVariable.id }` |
| `token.isExcluded === true` | Skip token entirely |
| `ref.shadeId === null` | Skip this mode's value (leave unset) |
| `token.description` | Variable description |

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

| UI Color Palette data | Figma target |
| --------------------- | ------------ |
| `palette.base.name` | Variable collection name |
| No-theme palette | Default mode (renamed `'Mode 1'` → left as-is) |
| Themed palette | One mode per theme; first theme renames default mode, subsequent themes add new modes |
| `colorName/shadeName` | Variable name (empty / `'None'` segments filtered) |
| `shade.gl` + `shade.alpha` | Variable value: `{ r: gl[0], g: gl[1], b: gl[2], a: alpha }` |
| `shade.description` | Variable description |

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
