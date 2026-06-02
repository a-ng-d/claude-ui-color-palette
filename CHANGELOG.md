# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2026-06-02

### Fixed

- `figma/generate-variables`: arc and dark theme `gl` values are now correctly applied per mode — the normalized row model and sync behaviour explicitly state that `gl` is taken from the matching theme row, preventing light theme values from silently overwriting arc/dark mode values
- `figma/generate-styles`: same fix for paint styles — each themed style now uses the `gl` from its own theme row instead of the first row found
- `penpot/generate-tokens`: arc and dark theme `hex` values are now correctly applied per token set — each themed set uses only the rows where `themeName` matches, preventing flat hex values across all themes
- `penpot/generate-styles`: same fix for local color styles — each themed style now uses the `hex` from the matching theme row
- `palette-color-systemer` agent: clarified "primitive cascade handles it" for arc themes — shade-index overrides are only needed when the stop label must change across themes, not when the hex value already differs per mode

### Changed

- README: installation flow now leads with the Yelbolt marketplace (`/plugin marketplace add yelbolt/claude-marketplace` → `/plugin install ui-color-palette@yelbolt`); direct GitHub install moved to "Alternative"; added explicit `Update` command
- MCP Servers table: Penpot entry updated from `stdio / npx mcp-remote localhost:4401` to `HTTP / design.penpot.app/mcp/stream?userToken=…` to match actual plugin configuration
- Prerequisites: Penpot entry updated — references `/plugin config` for token setup instead of the removed penpot-mcp local install requirement

## [1.0.2] - 2026-05-23

### Added

- `palette-color-systemer` agent: new specialized agent for guided semantic color system design — suggests taxonomy patterns (Role × State, Role × Prominence × State, Surface × Content, Custom), proposes intelligent default bindings derived from palette color ids and shade stops, flags unresolvable tokens, batches adjustments before calling `get_color_system`, and displays the token matrix
- `color-systemer` orchestrator: Phase 2.5 now enforces a hard primitive gate — `PaletteData` or `base` + `themes` must be in context before entering the color system phase; delegates immediately to `palette-color-systemer` instead of handling taxonomy inline
- `color-systemer` orchestrator: added `palette-color-systemer` to the specialized sub-agents list and delegation rules

### Changed

- `figma/generate-semantic-variables`: the skill now asks whether the semantic collection should use **one mode per theme** (mirrors primitive structure, enables standalone theme switching) or a **single flat mode** (theme adaptation handled entirely at the primitive level) before creating the collection
- `penpot/generate-semantic-tokens`: the skill now asks whether to create **one set per theme** (`systemName/themeName`, enables Penpot theme switching) or a **single flat set** (`systemName`, theme adaptation handled entirely at the primitive level) before generating token sets
- `build-color-system` skill: Step 7 next-action descriptions for Figma and Penpot updated to inform the user of the mode/set strategy question they will encounter at deploy time
- `palette-color-systemer` agent: Step 7 next-action descriptions for Figma and Penpot updated to match

## [1.0.1] - 2026-05-23

### Fixed

- `palette-codegen` agent: added explicit file modification permission and step-by-step GitHub/GitLab workflow (branch → commit → push → PR/MR) via `gh-cli` and `gitlab-cli-skills`
- `color-systemer` agent: added overflow rule — when `get_palette` response exceeds the token limit, `base` and `themes` are used directly for downstream tools instead of reading the overflow file
- `scale-palette` skill: added overflow handling table (code export, display, audit, design tool push) with targeted `grep` extraction strategy; removed sequential chunk-reading
- `scale-palette` skill: fixed theme configuration — `"default theme"` is now reserved exclusively for the base theme (`id: "00000000000"`, `name: "None"`); all named themes (Light, Dark, etc.) correctly use `"custom theme"` and the base theme is always included in the array
- MCP schema (`schemas.ts`): clarified `id`, `name`, and `type` descriptions for `ThemeConfiguration` to match the correct default/custom theme rules

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

[1.0.3]: https://github.com/a-ng-d/claude-ui-color-palette/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/a-ng-d/claude-ui-color-palette/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/a-ng-d/claude-ui-color-palette/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/a-ng-d/claude-ui-color-palette/releases/tag/v1.0.0
