---
name: ui-color-palette-figma-generate-tokens
description: Generate a Figma-ready token system from a UI Color Palette by syncing variables first, then optionally styles and a visual document preview. Use when the user wants a complete Figma handoff.
argument-hint: <palette-id|current-palette> [variables|styles|preview]
---

# Generate Figma Tokens

Use this skill when the user wants a complete **Figma token workflow**.

In Figma, “tokens” should be interpreted as:

- **Variables** for the real token system
- **Modes** for themes
- **Optional local styles** for visual/application reuse
- **Optional document preview** for a visible palette board inside the file

## Recommended strategy

Default order:

1. sync **variables** first
2. optionally sync **styles**
3. optionally create/update a **document preview**

This order matters because variables are the semantic source of truth.

## Backing operations

This skill orchestrates the available Figma bridge actions:

- `SYNC_LOCAL_VARIABLES`
- `SYNC_LOCAL_STYLES`
- `CREATE_DOCUMENT`
- `UPDATE_DOCUMENT`

These plugin operations are only a reference implementation. An agent should be able to perform the same work directly through Figma API requests.

## Equivalent agent-side API requests

Interpret the complete workflow as 3 API layers:

1. **Variables layer**
	- list collections
	- create or reuse collection
	- list variables
	- create or reuse variables
	- create, rename, or reuse modes
	- set values for each mode
2. **Styles layer**
	- list local paint styles
	- create or reuse paint styles
	- update style fills, names, and descriptions
3. **Preview layer**
	- create or update a frame/section-based document
	- insert swatches, labels, and theme grouping
	- update node metadata when the preview already exists

## Use cases

Use this skill when the user asks for:

- Figma tokens
- full Figma handoff
- palette in variables + styles
- design-ready palette generation in Figma
- a palette board plus token sync

## Output modes

### 1. Tokens only

Use only variable sync when the user wants the semantic system.

Result:

- variable collection
- modes from themes
- variables from shades

### 2. Tokens + styles

Use variable sync first, then local styles when the user also wants reusable fills.

Result:

- semantic token system in variables
- visual projection in styles

### 3. Tokens + visual preview

Use variable sync first, then create or update a document preview when the user wants to inspect the palette visually in Figma.

Preview expectations:

- one board or document per palette view
- grouped by theme
- grouped by color family
- visible swatches for shades
- readable palette review artifact in the file

## Workflow

1. Ensure the palette exists in the Figma plugin context.
2. Sync local variables.
3. If the user wants visual reuse, sync local styles.
4. If the user wants a board/sheet/preview, create or update a document.
5. Summarize what was generated and what remains optional.

## Decision rule

Choose the path that matches the user intent:

- “tokens” → variables first
- “styles” or “swatches” → styles, usually after variables
- “preview”, “board”, “sheet”, “palette in document” → document preview
- “full Figma setup” → variables + styles + preview

## Output

Return a compact handoff summary, for example:

- variables: synced
- styles: synced
- preview: created
- themes: 2 modes
- shades: 24 variables, 24 styles

## Tips

- In Figma, variables are the best representation of tokens.
- Styles should be treated as secondary artifacts derived from the same palette.
- A document preview is useful for review, not for token storage.
- If the user later asks for accessibility review, route to the audit skill after the palette is generated.
