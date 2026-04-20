---
name: ui-color-palette-framer-generate-tokens
description: Generate a Framer-ready color system from a UI Color Palette by syncing color styles and optionally creating or updating a visual document preview. Use when the user wants a complete Framer handoff.
argument-hint: <palette-id|current-palette> [styles|preview]
---

# Generate Framer Tokens

Use this skill when the user wants a complete **Framer handoff workflow**.

Important constraint: this Framer integration does **not** expose a dedicated native token or variable layer comparable to Figma Variables or Penpot Tokens. Here, “tokens” should be interpreted as a workflow based on:

- **Color styles** as the reusable color system
- **Document preview** as the visual review artifact

## Structure-first execution

Use this file as a workflow specification, not as an API catalog.

Execution order:

1. decide whether the request needs styles only or styles plus preview
2. structure the palette for each artifact layer
3. run the layers in the recommended order
4. only then map each layer to MCP or plugin API calls

The API layer is secondary to the workflow structure.

## Input contract

Before orchestration, the agent should ensure:

- a palette is already available in the active plugin or MCP context
- the target palette is selected explicitly or can be inferred as the current palette
- palette data includes stable theme, color, and shade naming
- each shade exposes the color data needed for styles and preview
- the user intent is classified as styles only or styles plus preview

If one of these conditions is missing, resolve that upstream before token orchestration.

## Normalized PaletteData projection

Reduce `PaletteData` to two reusable row models before execution:

- `styleRows`: `paletteName`, `themeName`, `colorName`, `shadeName`, `stylePath`, `light`, `dark`, `description`
- `previewRows`: `paletteName`, `themeName`, `colorName`, `shadeName`, `displayLabel`, `light`, `dark`, `description`

These normalized row models are the actual handoff from palette structure to Framer styles and preview generation.

## Recommended strategy

Default order:

1. sync **color styles** with `create + update`
2. optionally create or update a **document preview**

This order matters because styles are the reusable artifact and the preview is only for review.

## Backing operations

This skill orchestrates the available Framer bridge actions:

- `createLocalStyles()`
- `updateLocalStyles()`
- `createDocument()`
- `updateDocument()`

These plugin operations are only a reference implementation. An agent should be able to perform the same work directly through Framer API requests.

## Equivalent agent-side API requests

Interpret the complete workflow as 2 API layers:

1. **Color styles layer**
	- list color styles
	- create styles when missing and allowed
	- update style attributes (`name`, `path`, `light`, `dark`)
	- remove orphan styles when deep sync and permissions allow it
2. **Preview layer**
	- create or update frame-based palette previews
	- insert swatches, labels, and grouped theme sections
	- update node metadata when the preview already exists

## Use cases

Use this skill when the user asks for:

- Framer tokens
- Framer design system colors
- full Framer handoff
- palette styles plus preview in Framer
- generate and update palette artifacts in Framer

## Output modes

### 1. Styles only

Use style sync when the user wants the reusable Framer color system.

Result:

- color styles created or reused
- style attributes updated
- optional orphan cleanup

### 2. Styles + preview

Use style sync first, then create or update a document preview when the user wants to inspect the palette visually.

Preview expectations:

- palette or sheet view generated in Framer
- grouped by theme
- grouped by color family
- visible shade swatches for review

## Workflow

1. Ensure the palette exists in the Framer plugin state.
2. Sync local color styles using the `create + update` flow.
3. If the user wants a board, sheet, or visual preview, create or update a document.
4. Summarize what was generated and what remains optional.

## Decision rule

Choose the path that matches the user intent:

- “tokens” → styles first
- “styles” → styles first
- “update Framer styles” → run create + update style sync
- “preview”, “board”, “sheet”, “palette in document” → document preview after style sync
- “full Framer setup” → styles + preview

## Output

Return a compact handoff summary, for example:

- styles: synced
- preview: created
- shades: 24 styles

## Tips

- Be explicit that Framer here uses color styles as the closest reusable color-system primitive.
- The preview document is for review, not for storing token semantics.
- If the user asks specifically for ongoing sync, always include the update step, not just creation.
- If the user wants a stricter token abstraction, Figma or Penpot currently provides a stronger native model.
