---
name: ui-color-palette-figma
description: Entry point for UI Color Palette workflows targeting Figma. Use to choose between variables, styles, and document preview generation.
argument-hint: <variables|styles|tokens|preview>
---

# UI Color Palette Figma

Use this folder as the platform entry point for all **UI Color Palette → Figma** workflows.

## Folder structure

- `SKILL.md` at the root is the platform index
- `references/` contains the detailed operational sub-skills

## Structure-first rule

This platform skill is primarily a routing and orchestration layer.

The agent should:

1. identify which artifact the user wants first
2. choose the matching file in `references/`
3. normalize the palette payload for that workflow
4. only then translate the workflow into MCP or plugin API operations

Do not start from raw API calls. Start from the workflow structure.

## Available sub-skills

- `references/generate-variables.md` — generate or sync Figma local variables and modes
- `references/generate-styles.md` — generate or sync Figma local paint styles
- `references/generate-tokens.md` — orchestrate variables, styles, and document preview together

## Routing

Choose the sub-skill by user intent:

- “variables”, “tokens”, “modes”, “theme variables” → `references/generate-variables.md`
- “paint styles”, “local styles”, “style library”, “swatches” → `references/generate-styles.md`
- “full handoff”, “everything in Figma”, “variables + styles + preview” → `references/generate-tokens.md`

## Platform API references

An agent should think in terms of the Figma Plugin API surface, not only the plugin wrapper:

- **Variables API**
  - local variable collections
  - collection modes
  - local variables
  - set value for mode
- **Styles API**
  - local paint styles
  - style name and description
  - solid paint fills and opacity
- **Document / node API**
  - frames, sections, groups, text nodes
  - plugin data on nodes
  - create/update preview boards

## MCP usage strategy

Use MCP or direct API calls as the execution layer, not as the skill structure.

- The root skill chooses the workflow.
- The reference file defines the expected inputs, transformations, and outputs.
- MCP/API calls execute the chosen workflow.

## Agent rule

The plugin bridge files are reference implementations. If the plugin action is unavailable, the agent should reproduce the same behavior directly through Figma API requests.
