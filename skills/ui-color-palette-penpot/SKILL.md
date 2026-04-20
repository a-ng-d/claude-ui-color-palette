---
name: ui-color-palette-penpot
description: Entry point for UI Color Palette workflows targeting Penpot. Use to choose between tokens, styles, and board/document preview generation.
argument-hint: <tokens|styles|preview>
---

# UI Color Palette Penpot

Use this folder as the platform entry point for all **UI Color Palette → Penpot** workflows.

## Folder structure

- `SKILL.md` at the root is the platform index
- `references/` contains the detailed operational sub-skills

## Structure-first rule

This platform skill is primarily a routing and orchestration layer.

The agent should:

1. identify whether the user needs tokens, styles, or preview first
2. choose the matching file in `references/`
3. normalize the palette payload for that workflow
4. only then translate the workflow into MCP or plugin API operations

Do not start from raw API calls. Start from the workflow structure.

## Available sub-skills

- `references/generate-tokens.md` — generate or sync Penpot local tokens and themed sets
- `references/generate-styles.md` — generate or sync Penpot local color styles

## Routing

Choose the sub-skill by user intent:

- “tokens”, “semantic colors”, “theme tokens”, “Penpot token sets” → `references/generate-tokens.md`
- “styles”, “local colors”, “style library”, “swatches” → `references/generate-styles.md`
- “preview”, “board”, “document review” → usually start with `references/generate-tokens.md`, then generate/update the document preview

## Platform API references

An agent should think in terms of the Penpot plugin/API surface, not only the plugin wrapper:

- **Local token catalog API**
  - token sets
  - tokens
  - themes and theme groups
- **Local style/color API**
  - local library colors
  - style path, name, color, opacity
- **Document API**
  - boards/documents
  - node creation and update
  - plugin data on current page/document

## MCP usage strategy

Use MCP or direct API calls as the execution layer, not as the skill structure.

- The root skill chooses the workflow.
- The reference file defines the expected inputs, transformations, and outputs.
- MCP/API calls execute the chosen workflow.

## Agent rule

The plugin bridge files are reference implementations. If the plugin action is unavailable, the agent should reproduce the same behavior directly through Penpot API requests.

---

## Recommended subagent

Delegate this skill to **`palette-transitioner`**.

The `palette-transitioner` agent normalizes `PaletteData` into the correct row model for Penpot (`tokenRows`, `styleRows`, `previewRows`), then routes execution through the appropriate Penpot sub-skill.
