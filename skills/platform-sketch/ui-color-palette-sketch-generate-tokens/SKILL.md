---
name: ui-color-palette-sketch-generate-tokens
description: Generate a Sketch-ready color system from a UI Color Palette by syncing swatches first, then optionally shared styles and a document preview. Use when the user wants a complete Sketch handoff.
argument-hint: <palette-id|current-palette> [variables|styles|preview]
---

# Generate Sketch Tokens

Use this skill when the user wants a complete **Sketch handoff workflow**.

Important constraint: in this plugin, Sketch does **not** expose a separate native token API comparable to Figma Variables or Penpot Tokens. Here, “tokens” should be interpreted as a composed workflow using:

- **Swatches** as the variable/token-like layer
- **Shared layer styles** as the reusable visual layer
- **Document preview** as the human-readable board/sheet

## Recommended strategy

Default order:

1. sync **variables/swatches** first
2. optionally sync **shared styles**
3. optionally create or update a **document preview**

This order matters because swatches are the closest thing to the source color system in this Sketch plugin.

## Backing operations

This skill orchestrates the available Sketch bridge actions:

- `createLocalVariables()`
- `updateLocalVariables()`
- `createLocalStyles()`
- `updateLocalStyles()`
- `createDocument()`
- `updateDocument()`

These plugin operations are only a reference implementation. An agent should be able to perform the same work directly through Sketch API requests.

## Equivalent agent-side API requests

Interpret the complete workflow as 3 API layers:

1. **Swatch layer**
	- list document swatches
	- create or reuse swatches
	- update swatch colors
	- remove orphan swatches when deep sync is requested
2. **Shared style layer**
	- list shared layer styles
	- create or reuse shared styles
	- update style fills and names
3. **Preview layer**
	- create or update an artboard/group-based document preview
	- insert swatches and labels grouped by theme and color family

## Use cases

Use this skill when the user asks for:

- Sketch tokens
- full Sketch handoff
- swatches + styles + preview
- a palette board in Sketch
- a design-ready palette setup in Sketch

## Output modes

### 1. Tokens only

Use variable/swatch sync when the user wants the closest Sketch equivalent to tokens.

Result:

- swatches created from palette shades
- palette path encoded in swatch names

### 2. Tokens + styles

Use swatch sync first, then shared styles when the user also wants reusable styles.

Result:

- source color layer in swatches
- reusable visual layer in shared styles

### 3. Tokens + visual preview

Use swatch sync first, then create or update a document preview when the user wants to inspect the palette visually.

Preview expectations:

- grouped by theme
- grouped by color family
- visible shade swatches
- readable board/sheet artifact in the Sketch document

## Workflow

1. Ensure the palette exists in the Sketch document plugin state.
2. Sync local variables/swatches.
3. If the user wants reusable styles, sync shared layer styles.
4. If the user wants a board/sheet/preview, create or update a document.
5. Summarize what was generated and what remains optional.

## Decision rule

Choose the path that matches the user intent:

- “tokens” → swatches first
- “variables” → swatches first
- “styles” or “shared styles” → styles, usually after swatches
- “preview”, “board”, “sheet”, “palette in document” → document preview
- “full Sketch setup” → swatches + styles + preview

## Output

Return a compact handoff summary, for example:

- swatches: synced
- styles: synced
- preview: created
- shades: 24 swatches, 24 styles

## Tips

- Be explicit that Sketch here uses swatches as the token-like primitive.
- Shared styles are derived artifacts, not the source semantic system.
- A document preview is useful for review and handoff, not for storage of token semantics.
- If the user wants a stricter token model, Figma or Penpot currently offers a stronger native abstraction.
