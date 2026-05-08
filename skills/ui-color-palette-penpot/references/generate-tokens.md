---
name: ui-color-palette-penpot-generate-tokens
description: Generate or sync Penpot local tokens from a UI Color Palette, and optionally create a visual board/document preview. Use when the user wants a Penpot-native token workflow.
argument-hint: <palette-id|current-palette> [tokens|preview]
---

# Generate Penpot Tokens

Use this skill when the user wants a palette pushed into **Penpot local tokens**.

In Penpot, tokens are the main semantic representation for a palette. For UI Color Palette, this workflow can generate:

- local token sets
- local themes grouped by palette name
- one token per `color/shade`
- an optional board/document preview for visual review

## Source of truth

Treat **Penpot tokens** as the source of truth.

- Tokens represent color design tokens
- Sets represent palette or theme partitions
- Themes group themed token sets
- A board/document is only a visual artifact, not the token source

If the user asks for “Penpot tokens”, use this skill first.

## Structure-first execution

Use this file as a workflow specification, not as an API catalog.

Execution order:

1. identify the target artifact: token catalog first, preview second if requested
2. reduce the palette to the minimum token payload
3. apply token synchronization before any visual artifact
4. only then map the workflow to MCP or plugin API calls

The API layer is secondary to the workflow structure.

## Input contract

Before orchestration, the agent should ensure:

- a palette is already available in the active plugin or MCP context
- the target palette is selected explicitly or can be inferred as the current palette
- palette data includes stable theme, color, and shade naming
- each shade exposes `hex` and optional description
- the user intent is classified as token sync only or token sync plus preview

If one of these conditions is missing, resolve that upstream before token orchestration.

## Normalized PaletteData projection

Reduce `PaletteData` to two reusable row models before execution:

- `tokenRows`: `paletteName`, `themeName`, `colorName`, `shadeName`, `tokenSetName`, `tokenName`, `hex`, `description`
- `previewRows`: `paletteName`, `themeName`, `colorName`, `shadeName`, `displayLabel`, `hex`, `description`

Token name encoding (exact logic from implementation):
1. Apply `doSnakeCase()` to `colorName` (e.g. `Primary Blue` → `primary_blue`)
2. On each segment (`[colorNameSnake, shadeName]`), replace remaining spaces with `-`
3. Filter out empty strings and `'None'`
4. Join with `.` → `colorName_snake.shadeName`
5. Replace `・` with `_` on the resulting string
6. Fallback: if `colorName` is empty, use the localized default color name (snake-cased)

Example: color `Primary Blue`, shade `500` → `primary_blue.500`

Set name encoding:
- **no themes**: one set named `palette.base.name` (falls back to localized default if empty)
- **with themes**: one set per theme named `palette.base.name/themeName` (theme name falls back to localized default if empty)

Token value: `shade.hex ?? '#000000'` (raw hex string; fallback to black if undefined)

These normalized row models are the actual handoff from palette structure to Penpot token and preview generation.

## Backing operations

This skill maps to the plugin bridge workflow:

- `createLocalTokens()`
- `updateLocalTokens()`
- optionally `createDocument()` or `updateDocument()` for preview

These plugin operations are only a reference implementation. An agent should be able to perform the same work directly through Penpot API requests.

## Equivalent agent-side API requests

When not relying on the plugin action, use the equivalent Penpot API flow:

**Case A — palette with no themes** (all shades belong to a single base group):

1. Flatten the palette into shade rows (`colorName`, `shadeName`, `hex`, `description`).
2. Get or create one token set: `catalog.addSet({ name: paletteName })`.
3. For each shade row:
   - Compute `tokenName`: `Case(colorName).doSnakeCase().replace(/\s+/g, '-') + '.' + shadeName`
   - Call `tokenSet.addToken({ type: 'color', name: tokenName, value: hex, description })`
   - Track the returned `token.id` for future updates.

**Case B — palette with themes**:

1. Flatten the palette into theme rows (`themeName`, `colorName`, `shadeName`, `hex`, `description`).
2. For each unique theme:
   - Get or create a token set: `catalog.addSet({ name: paletteName + '/' + themeName })`
   - Get or create a theme group: `catalog.addTheme({ group: paletteName, name: themeName })`
   - Track returned `set.id` and `theme.id` for future updates.
3. For each shade row within a theme:
   - Compute `tokenName` as above.
   - Call `themeSet.addToken({ type: 'color', name: tokenName, value: hex, description })`
   - Track the returned `token.id`.
4. If deep sync is desired, remove orphan tokens, orphan themed sets, and orphan themes.
5. If the user wants a preview, create or update a board/document with grouped swatches.

Behavior supported by the plugin:

- creates token sets when missing
- creates theme groups when themes exist
- creates tokens from `colorName_snake.shadeName`
- updates token names, values, descriptions, themes, and sets
- optionally removes orphan tokens/themes when deep sync is enabled

## Penpot mapping

| UI Color Palette data | Penpot target |
| --------------------- | ------------- |
| `palette.base.name` | Token set name (no themes) / set prefix + theme group name (with themes) |
| No-theme palette | Single set: `paletteName` |
| Themed palette | One set per theme: `paletteName/themeName` + one theme: `{ group: paletteName, name: themeName }` |
| `colorName` (snake_case, spaces → `-`) | First segment of token name (before `.`) |
| `shadeName` | Second segment of token name (after `.`) |
| `shade.hex` | Token value |
| `shade.description` | Token description |
| Shade description     | Token description                 |

## Workflow

1. Ensure a palette exists in the current Penpot plugin context.
2. Prefer the selected/current palette unless the user provides a palette ID.
3. Sync local tokens.
4. Confirm the result in terms of:
   - token sets created or reused
   - themes created, updated, or removed
   - tokens created, updated, or removed
5. If the user wants a visual deliverable, create or update a board/document preview after token sync.
6. If the user also wants reusable local color styles, route next to `ui-color-palette-penpot-generate-styles`.

## Visual preview option

If the user asks for a board, sheet, document, or palette preview in Penpot:

- sync tokens first
- then create or update a document preview

Preview expectations:

- one board/document per generated view
- grouped by theme
- grouped by color family
- visible shade swatches for review

## When to use

Use this skill when the user asks for:

- Penpot tokens
- Penpot color tokens
- token sets in Penpot
- theme tokens in Penpot
- full token sync in Penpot

## Output

Return a concise operational summary, for example:

- token sets: `2`
- themes: `+2`, `~1`, `-0`
- tokens: `+24`, `~24`, `-3`
- preview: created

Do not dump the full palette payload.

## Tips

- In Penpot, tokens should be preferred over styles for semantic design tokens.
- Theme-aware palettes should usually create themes and token sets before any visual board work.
- If the user wants a readable artifact for review, generate a board/document after syncing tokens.
- If strict cleanup is needed, ensure deep sync for tokens is enabled.
