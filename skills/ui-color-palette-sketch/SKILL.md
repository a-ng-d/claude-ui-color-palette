---
name: ui-color-palette-sketch
description: Entry point for UI Color Palette workflows targeting Sketch. Use to choose between swatches, shared styles, and document preview generation.
argument-hint: <variables|styles|tokens|preview>
---

# UI Color Palette Sketch

Use this folder as the platform entry point for all **UI Color Palette → Sketch** workflows.

## Folder structure

- `SKILL.md` at the root is the platform index
- `references/` contains the detailed operational sub-skills

## Structure-first rule

This platform skill is primarily a routing and orchestration layer.

The agent should:

1. identify whether the user needs swatches, shared styles, or preview first
2. choose the matching file in `references/`
3. normalize the palette payload for that workflow
4. only then translate the workflow into MCP or plugin API operations

Do not start from raw API calls. Start from the workflow structure.

## Available sub-skills

- `references/generate-variables.md` — generate or sync Sketch swatches as the variable-like layer
- `references/generate-styles.md` — generate or sync Sketch shared layer styles
- `references/generate-tokens.md` — orchestrate swatches, styles, and document preview together

## Routing

Choose the sub-skill by user intent:

- “variables”, “swatches”, “color variables” → `references/generate-variables.md`
- “styles”, “shared styles”, “reusable fills” → `references/generate-styles.md`
- “full Sketch setup”, “tokens”, “preview + styles + swatches” → `references/generate-tokens.md`

## Platform API references

An agent should think in terms of the Sketch plugin/document API surface, not only the plugin wrapper:

- **Document color API**
  - document swatches
  - add/remove/update swatches
- **Shared style API**
  - shared layer styles
  - style fills and names
- **Document structure API**
  - pages, layers, groups, artboards
  - document settings and layer settings
  - create/update preview boards or sheets

## MCP usage strategy

Use MCP or direct API calls as the execution layer, not as the skill structure.

- The root skill chooses the workflow.
- The reference file defines the expected inputs, transformations, and outputs.
- MCP/API calls execute the chosen workflow.

## Agent rule

The plugin bridge files are reference implementations. If the plugin action is unavailable, the agent should reproduce the same behavior directly through Sketch API requests.
