![GitHub last commit](https://img.shields.io/github/last-commit/a-ng-d/claude-ui-color-palette?color=informational) ![GitHub](https://img.shields.io/github/license/a-ng-d/claude-ui-color-palette?color=informational)

# UI Color Palette on Claude Code

A [Claude Code](https://code.claude.com/) plugin that brings color palette design, contrast auditing, code generation, and design tool synchronization directly into your AI-assisted workflow.

## Features

### Core skills

| Skill                        | Description                                                                                               |
| ---------------------------- | --------------------------------------------------------------------------------------------------------- |
| `generate-source-colors`     | Generate source colors from an image (k-means), a text prompt (AI), or a base color (harmony)             |
| `scale-palette`              | Build a full palette with `get_palette` and export as code/tokens (CSS, Tailwind, SwiftUI, DTCG, …)      |
| `build-color-system`         | Define a semantic token taxonomy and bind it to palette primitives via `get_color_system`                 |
| `manage-palettes`            | Browse, publish, share, update, and delete palettes on the platform                                       |
| `audit-palette`              | Audit color pairs for WCAG 2.2 and APCA compliance with a global contrast score                           |
| `report-palette`             | Render a shareable readability report (HTML): every shade, hex, OKLCH/LCH value, WCAG 2.2 and APCA scores, global synthesis |

## MCP Servers

The plugin connects to the following MCP servers:

| Server               | Transport | URL                                    | Notes                                                    |
| -------------------- | --------- | -------------------------------------- | -------------------------------------------------------- |
| **UI Color Palette** | HTTP      | `https://mcp.ui-color-palette.com/mcp` | Core palette engine                                      |
| **Figma**            | HTTP      | `https://mcp.figma.com/mcp`            | Remote Figma API                                         |
| **Penpot**           | HTTP      | `https://design.penpot.app/mcp/stream` | Penpot Cloud; MCP key via `penpot_token`, sent as a header |
| **Framer**           | HTTP      | `https://mcp.framer.com/mcp`           | Official Framer server, sign in with OAuth               |
| **GitHub**           | HTTP      | `https://api.githubcopilot.com/mcp/`   | Issues, PRs, repos                                       |

Servers that run on your own machine or network are added by hand: the Figma desktop app (Dev Mode MCP server enabled), the Sketch app (MCP enabled in preferences), self-hosted Penpot and GitLab.

```bash
claude mcp add --transport http figma-desktop http://127.0.0.1:3845/mcp
claude mcp add --transport http sketch http://localhost:31126/mcp
claude mcp add --transport http penpot "https://<your-penpot-domain>/mcp/stream?userToken=<your-mcp-key>"
claude mcp add --transport http gitlab https://<your-instance>/api/v4/mcp
```

### User configuration

| Key | Sensitive | Description |
|---|---|---|
| `penpot_token` | Yes (keychain) | Your Penpot Cloud MCP key — Penpot → Your account → Integrations → MCP Server. Sent only to `design.penpot.app` |

Update it at any time with `/plugin config`.

## Agent

**uicper** is the plugin's orchestrator. Claude hands palette workflows to it, and you can call it directly. It acts as the top-level orchestrator for multi-step workflows such as:

- generate → readability report → export
- generate → audit → export
- generate → transition → sync to design tools
- retrieve/publish → audit → export

The orchestrator delegates specialized work to focused sub-agents:

- `palette-color-systemer` — guided semantic color system design: taxonomy pattern suggestion, intelligent binding proposals, iterative refinement, and `get_color_system` submission
- `palette-auditor` — WCAG/APCA audits, risk detection, remediation guidance
- `palette-codegen` — normalized projection and code/token generation
- `palette-publisher` — published palette retrieval, publication, update, visibility, deletion
- `palette-transitioner` — transition from `PaletteData` to variables, tokens, styles, swatches, and preview/document artifacts

To make it your default agent, add this to your own Claude Code settings:

```json
{
  "agent": "ui-color-palette:uicper"
}
```

## Installation

### From the Yelbolt marketplace

**Step 1 — Add the marketplace** (once per machine):

```bash
/plugin marketplace add yelbolt/claude-marketplace
```

**Step 2 — Install the plugin:**

```bash
/plugin install ui-color-palette@yelbolt
```

### Update

```bash
/plugin marketplace update yelbolt
```

### Alternative — direct GitHub install

```bash
/plugin install github:a-ng-d/claude-ui-color-palette
```

### From a local directory (development)

```bash
claude --plugin-dir ./claude-ui-color-palette
```

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

# Readability report of the palette in context (HTML document)
/ui-color-palette:report-palette

# Audit contrast of a color set
/ui-color-palette:audit-palette #1E293B #F8FAFC #3B82F6 #FFFFFF

# Browse community palettes
/ui-color-palette:manage-palettes sunset warm
```

## License

MIT
