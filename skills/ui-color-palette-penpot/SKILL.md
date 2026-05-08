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

## Reuse rule

**Before calling any MCP tool**, check whether `PaletteData` is already present in the conversation context.

If it is, use it directly — **never call `get_palette` again**. Confirm to the user:

> Using the palette already built in this session. Generating Penpot artifacts now.

Only rebuild the palette if the user explicitly asks to change colors, preset, or themes.

---

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
- “preview”, “board”, “document review” → usually start with `references/generate-tokens.md`, then generate/update the document preview- "semantic tokens", "color system tokens", "system token set", `SystemData` present in context → `references/generate-tokens.md` — **new token set from `SystemData`**

When routing a `SystemData`-based workflow to `references/generate-tokens.md`, pass `SystemData` opaquely. The sub-skill maps it as follows:
- **First**: ensure the palette's primitive token sets exist — create them if missing (mandatory prerequisite before any binding)
- Create one semantic token set per theme, named after the system schema (or a user-supplied label)
- Add one **token** per entry in `SystemData.tokens`, named by joining `token.pathNames` with `.`
- Each token value references the primitive token as `{colorName_snake.shadeName}` (resolved via `token.refs[themeIndex].shadeId`)
- Excluded tokens (`isExcluded: true`) and unbound refs (`shadeId: null`) are skipped
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
