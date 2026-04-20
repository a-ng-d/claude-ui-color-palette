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

## Backing operations

This skill maps to the plugin bridge workflow:

- `createLocalTokens()`
- `updateLocalTokens()`
- optionally `createDocument()` or `updateDocument()` for preview

These plugin operations are only a reference implementation. An agent should be able to perform the same work directly through Penpot API requests.

## Equivalent agent-side API requests

When not relying on the plugin action, use the equivalent Penpot API flow:

1. Read and flatten the palette into `themeName`, `colorName`, `shadeName`, `hex`, and description rows.
2. Request the local token catalog.
3. Find or create token sets for the palette and per-theme sets when themes exist.
4. Find or create theme groups for themed palettes.
5. For each shade, find or create the token and update its name, value, and description.
6. If deep sync is desired, remove orphan tokens, orphan themed sets, and orphan themes.
7. If the user wants a preview, create or update a board/document with grouped swatches.

Behavior supported by the plugin:

- creates token sets when missing
- creates theme groups when themes exist
- creates tokens from `colorName.shadeName`
- updates token names, values, descriptions, themes, and sets
- optionally removes orphan tokens/themes when deep sync is enabled

## Penpot mapping

| UI Color Palette data | Penpot target |
| --------------------- | ------------- |
| `palette.base.name` | Token set base name / theme group |
| Theme | Penpot theme + themed set |
| `colorName.shadeName` | Token name |
| Shade hex | Token value |
| Shade description | Token description |

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
