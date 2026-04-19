# UI Color Palette — Claude Code Plugin

A [Claude Code](https://code.claude.com/) plugin that brings color palette design, contrast auditing, code generation, and design tool synchronization directly into your AI-assisted workflow.

## Features

| Skill                        | Description                                                                                               |
| ---------------------------- | --------------------------------------------------------------------------------------------------------- |
| `generate-source-colors`     | Generate source colors from an image (k-means), a text prompt (AI), or a base color (harmony)             |
| `scale-palette`              | Build a full palette with `get_full_palette` and export as code/tokens (CSS, Tailwind, SwiftUI, DTCG, …)  |
| `manage-palettes`            | Browse, publish, share, update, and delete palettes on the platform                                       |
| `audit-palette`              | Audit color pairs for WCAG 2.1 and APCA compliance with a global contrast score                           |
| `sync-design-variables`      | Push palette colors to Figma, Penpot, Sketch, or Framer as variables/tokens/styles                        |

## MCP Servers

The plugin connects to the following MCP servers:

| Server               | Transport | URL                                        | Notes                         |
| -------------------- | --------- | ------------------------------------------ | ----------------------------- |
| **UI Color Palette** | HTTP      | `https://mcp-uicp.yelbolt.workers.dev/mcp` | Core palette engine           |
| **Figma**            | HTTP      | `https://mcp.figma.com/mcp`                | Remote Figma API              |
| **Figma Desktop**    | HTTP      | `http://127.0.0.1:3845/mcp`                | Local Figma app               |
| **Penpot**           | stdio     | `npx mcp-remote http://localhost:4401/sse` | Self-hosted, requires setup   |
| **Sketch**           | HTTP      | `http://localhost:31126/mcp`               | Requires activation in Sketch |
| **Framer**           | HTTP      | User-specific URL                          | Requires Framer MCP plugin    |
| **GitHub**           | HTTP      | `https://api.githubcopilot.com/mcp/`       | Issues, PRs, repos            |
| **GitLab**           | HTTP      | `https://<instance>/api/v4/mcp`            | User-specific instance URL    |

## Agent

The plugin includes a **color-system** agent — a design system color expert that orchestrates all MCPs for multi-step workflows (generate → audit → export → sync).

## Installation

### From a local directory (development)

```bash
claude --plugin-dir ./claude-ui-color-palette
```

### User configuration

On first enable, the plugin prompts for optional config:

- **`gitlab_url`** — Your GitLab instance URL (leave empty if not using GitLab)
- **`framer_mcp_url`** — Your Framer MCP URL from the [Framer marketplace](https://www.framer.com/marketplace/plugins/mcp/)

## Usage

```bash
# Generate source colors from an image
/ui-color-palette:generate-source-colors https://example.com/photo.jpg 8

# Generate source colors from a mood description
/ui-color-palette:generate-source-colors a warm sunset over the ocean

# Generate source colors from a base color (harmony)
/ui-color-palette:generate-source-colors #3B82F6 triadic

# Build a palette and export to Tailwind v4
/ui-color-palette:scale-palette tailwind-v4

# Build a palette and export to CSS with OKLCH
/ui-color-palette:scale-palette css oklch

# Audit contrast of a color set
/ui-color-palette:audit-palette #1E293B #F8FAFC #3B82F6 #FFFFFF

# Browse community palettes
/ui-color-palette:manage-palettes sunset warm

# Sync to Figma
/ui-color-palette:sync-design-variables figma
```

## Prerequisites

| Server        | Requirement                                                                         |
| ------------- | ----------------------------------------------------------------------------------- |
| Penpot        | Install and run [penpot-mcp](https://github.com/penpot/penpot-mcp) locally          |
| Sketch        | Enable MCP in Sketch preferences                                                    |
| Framer        | Install the [MCP plugin](https://www.framer.com/marketplace/plugins/mcp/) in Framer |
| Figma Desktop | Run Figma desktop with MCP enabled                                                  |

## License

MIT
