---
description: Sync palette colors to a design tool as variables, tokens, or styles. Supports Figma, Penpot, Sketch, and Framer. Use when the user wants to push colors into their design tool.
---

# Sync Design Variables

Orchestrate the **ui-color-palette** MCP with a design tool MCP to push palette colors as design tokens, variables, or styles.

## Supported design tools

| Tool       | MCP server                 | Variable type                | Notes                                                   |
| ---------- | -------------------------- | ---------------------------- | ------------------------------------------------------- |
| **Figma**  | `figma` or `figma-desktop` | Variables & styles           | Use `figma-desktop` for local Figma, `figma` for remote |
| **Penpot** | `penpot`                   | Tokens & styles              | Requires self-hosted MCP (`npx mcp-remote`)             |
| **Sketch** | `sketch`                   | Variables & styles           | Requires Sketch MCP enabled in app                      |
| **Framer** | `framer`                   | Styles & themes (dark/light) | Requires Framer MCP plugin installed                    |

## Workflow

1. Ensure a palette is available (generate one or fetch from published palettes).
2. Ask the user which design tool to target.
3. Use the **ui-color-palette** tools to get the palette data.
4. Use the target design tool's MCP to:
   - Create a color variable collection (Figma) / token set (Penpot) / variable group (Sketch)
   - Create individual color variables/tokens/styles for each palette color
   - For Framer: create color styles and optionally set up light/dark themes
5. Confirm the sync and list all created variables.

## Arguments

`$ARGUMENTS` can be: `<design-tool>` or `<design-tool> <palette-id>`.

- Example: `/ui-color-palette:sync-design-variables figma`
- Example: `/ui-color-palette:sync-design-variables penpot my-palette-id`

## Tips

- For Figma, prefer `figma-desktop` when working locally for faster response.
- For Framer, always create both light and dark theme variants when the palette supports it.
- Name variables consistently: `color/primary/500`, `color/neutral/100`, etc.
