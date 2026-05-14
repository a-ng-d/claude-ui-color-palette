# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-14

### Added

- Initial release: plugin configuration, `plugin.json`, MCP server wiring, and LICENSE

#### Skills

- `generate-source-colors` — generate source colors from an image URL (k-means), a natural language prompt (Mistral AI), or a base color (harmony type)
- `scale-palette` — build a full palette via `get_palette` and export as code/tokens (CSS, SCSS, Tailwind v3/v4, SwiftUI, UIKit, Compose, DTCG, CSV, Style Dictionary, …)
- `build-color-system` — build a semantic color system (`SystemData`) from a taxonomy schema and bind it to palette primitives
- `audit-palette` — audit color pairs for WCAG 2.1 and APCA compliance with a global contrast score and remediation guidance
- `manage-palettes` — browse, publish, share, update, and delete palettes on the platform
- `help` — command list and usage guide

#### Platform integration skills

- `ui-color-palette-figma` — sync palette variables, styles, and swatch board previews to Figma via MCP; includes color extraction from Figma selections
- `ui-color-palette-framer` — sync palette styles and generate previews in Framer via MCP; includes color extraction from Framer components
- `ui-color-palette-penpot` — sync palette tokens and generate swatch previews in Penpot via MCP; includes color extraction from Penpot layers
- `ui-color-palette-sketch` — sync palette variables and generate previews in Sketch via MCP; includes color extraction from Sketch layers

#### Agents

- `color-systemer` — top-level orchestrator for multi-step workflows (generate → audit → export, generate → sync to design tool, retrieve → publish → export). Configured as the default agent
- `palette-auditor` — WCAG/APCA audits, risk detection, and remediation guidance
- `palette-codegen` — normalized palette projection and code/token generation
- `palette-publisher` — published palette retrieval, publication, update, visibility management, and deletion
- `palette-transitioner` — transition from `PaletteData` to variables, tokens, styles, swatches, and preview/document artifacts in design tools

#### Community skills (bundled)

- `figma-variables-tokens-generator` — generate a fully connected Figma design token system from a chat prompt
- `penpot-uiux-design` — create professional UI/UX designs in Penpot using MCP tools
- `sketch-implement-design` — translate Sketch layers into production-ready code
- `gh-cli` — GitHub CLI comprehensive reference
- `gitlab-cli-skills` — GitLab CLI command reference and workflows

#### MCP servers

- UI Color Palette (`https://mcp-uicp.yelbolt.workers.dev/mcp`) — core palette engine
- Figma remote (`https://mcp.figma.com/mcp`)
- Figma Desktop (`http://127.0.0.1:3845/mcp`)
- Penpot (`npx mcp-remote http://localhost:4401/sse`)
- Sketch (`http://localhost:31126/mcp`)
- Framer (user-specific URL)
- GitHub (`https://api.githubcopilot.com/mcp/`)
- GitLab (user-specific instance URL)

[1.0.0]: https://github.com/a-ng-d/claude-ui-color-palette/releases/tag/v1.0.0
