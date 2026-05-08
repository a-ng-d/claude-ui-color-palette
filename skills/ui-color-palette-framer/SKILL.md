---
name: ui-color-palette-framer
description: Entry point for UI Color Palette workflows targeting Framer. Use to choose between color style synchronization and visual document preview generation.
argument-hint: <styles|tokens|preview>
---

# UI Color Palette Framer

Use this folder as the platform entry point for all **UI Color Palette → Framer** workflows.

## Folder structure

- `SKILL.md` at the root is the platform index
- `references/` contains the detailed operational sub-skills

## Reuse rule

**Before calling any MCP tool**, check whether `PaletteData` is already present in the conversation context.

If it is, use it directly — **never call `get_palette` again**. Confirm to the user:

> Using the palette already built in this session. Generating Framer artifacts now.

Only rebuild the palette if the user explicitly asks to change colors, preset, or themes.

---

## Structure-first rule

This platform skill is primarily a routing and orchestration layer.

The agent should:

1. identify whether the user needs styles or preview first
2. choose the matching file in `references/`
3. normalize the palette payload for that workflow
4. only then translate the workflow into MCP or plugin API operations

Do not start from raw API calls. Start from the workflow structure.

## Available sub-skills

- `references/generate-styles.md` — generate and update Framer local color styles
- `references/generate-tokens.md` — orchestrate color styles and document preview together

## Routing

Choose the sub-skill by user intent:

- “styles”, “color styles”, “sync Framer colors” → `references/generate-styles.md`
- “tokens”, “full Framer handoff”, “styles + preview” → `references/generate-tokens.md`
- “preview”, “palette board”, “sheet” → usually start with `references/generate-tokens.md`

## Platform API references

An agent should think in terms of the Framer Plugin API surface, not only the plugin wrapper:

- **Color styles API**
  - get color styles
  - create color style
  - set style attributes
  - remove color style
- **Canvas / node API**
  - frames and child nodes
  - set parent, set attributes, selection
  - create/update visual preview documents
- **Permissions API**
  - permission checks before create, update, or remove operations

## MCP usage strategy

Use MCP or direct API calls as the execution layer, not as the skill structure.

- The root skill chooses the workflow.
- The reference file defines the expected inputs, transformations, and outputs.
- MCP/API calls execute the chosen workflow.

## Agent rule

The plugin bridge files are reference implementations. If the plugin action is unavailable, the agent should reproduce the same behavior directly through Framer API requests.

---

## Recommended subagent

Delegate this skill to **`palette-transitioner`**.

The `palette-transitioner` agent normalizes `PaletteData` into the correct row model for Framer (`styleRows`, `previewRows`), then routes execution through the appropriate Framer sub-skill.
