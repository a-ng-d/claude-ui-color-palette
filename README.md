# UI Color Palette — Claude Code Plugin

A [Claude Code](https://code.claude.com/) plugin that brings color palette design, contrast auditing, code generation, and design tool synchronization directly into your AI-assisted workflow.

## Features

| Skill                      | Description                                                                        |
| -------------------------- | ---------------------------------------------------------------------------------- |
| `generate-harmony`         | Create color harmonies (complementary, analogous, triadic, etc.) from a base color |
| `generate-from-prompt`     | Generate a palette from a natural language description via AI                      |
| `extract-dominant-colors`  | Extract dominant colors from a JPEG/PNG image using k-means clustering             |
| `manage-palettes`          | Browse, publish, share, and manage palettes on the platform                        |
| `generate-code`            | Export palettes as CSS, SCSS, Tailwind, SwiftUI, Compose, DTCG, etc.               |
| `audit-contrast`           | Audit color pairs for WCAG 2.1 and APCA compliance with a global contrast score    |
| `sync-design-variables`    | Push palette colors to Figma, Penpot, Sketch, or Framer as variables/tokens/styles |

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
# Generate a triadic harmony from a blue
/ui-color-palette:generate-harmony #3B82F6 triadic

# Create a palette from a mood description
/ui-color-palette:generate-from-prompt a warm sunset over the ocean

# Audit contrast of a color set
/ui-color-palette:audit-contrast #1E293B #F8FAFC #3B82F6 #FFFFFF

# Export to Tailwind v4
/ui-color-palette:generate-code tailwind-v4

# Extract colors from an image
/ui-color-palette:extract-dominant-colors https://example.com/photo.jpg

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
