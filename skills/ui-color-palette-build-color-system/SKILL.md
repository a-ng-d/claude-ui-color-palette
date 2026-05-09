---
name: ui-color-palette-build-color-system
description: Define a semantic color system taxonomy and resolve bindings against a palette using get_color_system. Use when the user wants to map semantic token names (role, prominence, state…) to primitive color shades. Produces a SystemData object for use in semantic code generation or design tool deployment.
argument-hint: <schema-description>
---

# Build Color System

Use the **ui-color-palette** MCP tool `get_color_system` to resolve a semantic token taxonomy against a generated palette and produce a `SystemData` object.

Semantic code export from the system is handled by `ui-color-palette-generate-semantic-code`.

---

## Pre-flight — Check session state

Before asking any questions, check the conversation context for existing slots.

### If `SystemData` is already in context

Show a summary (token count, bound / unbound / excluded). Ask: reuse, rebuild, or adjust bindings.

### If `SystemConfiguration` is already in context

Skip Step 0. Call `get_color_system` directly with the existing `base`, `themes`, and `system` values.

### If `PaletteData` or `base` + `themes` are already in context

Skip the palette questions in Step 0.

---

## Step 0 — Gather parameters

Do not call the tool until all required answers are collected.

### Required

**1. Palette inputs** — confirm `base` and `themes` are available. If not, run `ui-color-palette-scale-palette` first.

**2. Taxonomy groups** — ask for the semantic dimensions that structure the token names.

Each group has an `id`, a `name`, and `members` (each with `id` and `name`). The system generates the **cartesian product** of all groups: 2 groups × 3 members each = 6 tokens; 3 groups × 3 members = 27 tokens.

Common patterns:

| Pattern | Groups | Typical members |
| ------- | ------ | --------------- |
| Role × State | `role`, `state` | brand / neutral / danger ; default / hover / active / disabled |
| Role × Prominence × State | `role`, `prominence`, `state` | — ; default / subtle / strong ; — |
| Surface × Content | `surface`, `content` | background / border ; primary / secondary / inverse |

**3. Bindings** (iterative — start with the most important ones) — map token paths to primitive shade refs.

Format: `[memberId, memberId, …] → colorId:shadeName` (e.g. `[brand, default] → blue:500`).

Optional per-binding fields:

| Field | Description |
| ----- | ----------- |
| `description` | Optional label for the token |
| `overrides` | Per-theme alternative ref when the shade **index** differs: `{ darkId: "blue:300" }` |
| `isExcluded` | `true` → token stays in SystemData but is skipped during code generation |

> **When to use `overrides`**: only when the shade index (e.g. 500 → 300) must change between themes. If the primitive palette already produces different hex values per theme for the same stop, overrides are not needed — the primitive cascade handles it.

---

## Step 1 — Call `get_color_system`

**Tool**: `get_color_system`

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `base` | object | Yes | `BaseConfiguration` — same schema as `get_palette` |
| `themes` | array | Yes | Array of `ThemeConfiguration` objects |
| `system` | object | Yes | `SystemConfiguration` — schema + optional bindings |

### `system.schema`

| Field | Type | Description |
| ----- | ---- | ----------- |
| `groups` | array | Ordered list of taxonomy groups (order defines the path depth) |

Each group:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `id` | string | Group identifier (e.g. `"role"`) |
| `name` | string | Display name (e.g. `"Role"`) |
| `members` | array | List of `{ id: string, name: string }` |

### `system.bindings` (optional)

Each binding:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `path` | `string[]` | Ordered member ids (one per group), e.g. `["brand", "default"]` |
| `description` | string | Optional token description |
| `ref` | string | Default primitive ref: `"colorId:shadeName"` (e.g. `"blue:500"`) |
| `overrides` | `Record<string, string>` | Per-theme overrides: `{ themeId: "colorId:shadeName" }` |
| `isExcluded` | boolean | `true` → present in SystemData, excluded from code generation |

**Returns**: a `SystemData` object with `schema`, `tokens`, and `type: "system"`.

Each token in `tokens`:

| Field | Description |
| ----- | ----------- |
| `path` | Member id path (e.g. `["brand", "default"]`) |
| `pathNames` | Display name path (e.g. `["Brand", "Default"]`) |
| `description` | Optional description from the binding |
| `isExcluded` | Whether excluded from code generation |
| `refs` | `{ themeId, shadeId }[]` — `shadeId` is `"themeId:colorId:shadeName"` or `null` if unbound |

---

## Step 2 — Display the token matrix

After calling `get_color_system`, produce a readable token matrix. **Do not display raw `SystemData` JSON.** Store the raw response opaquely as the `SystemData` slot — never read, print, or reason from the raw object. The only purpose of `SystemData` is to be passed as-is to downstream tools (semantic code generation, design tool deployment).

Format — one row per token, one column per theme:

```text
Token                           | Light              | Dark
--------------------------------|--------------------|--------------------
brand / default                 | blue:500           | blue:400
brand / subtle                  | blue:200           | blue:700
neutral / default               | slate:600          | slate:300
neutral / subtle                | — unbound —        | — unbound —
neutral / disabled   [excluded] | —                  | —
```

Legend:
- `colorId:shadeName` → resolved ref for this theme
- `— unbound —` → no binding or ref not found in palette
- `[excluded]` → binding has `isExcluded: true`

Finish with a one-line summary: e.g. `12 tokens — 9 bound, 2 unbound, 1 excluded`.

---

## Workflow

1. Confirm `base` and `themes` are available (from context or `ui-color-palette-scale-palette`).
2. Gather taxonomy groups and members from the user.
3. Gather bindings (iterative — start with a subset, refine after preview).
4. Call `get_color_system`.
5. **Session state**: store result as `SystemData` slot, store the input `system` config as `SystemConfiguration` slot.
6. Display the token matrix.
7. Ask what to do next:
   - **Adjust bindings** — add, change, or exclude specific tokens, then rebuild
   - **Generate semantic code** → `ui-color-palette-generate-semantic-code`
   - **Export to Figma as a variable collection** → `ui-color-palette-figma` — pass `SystemData` and `PaletteData` opaquely. The sub-skill creates a new Figma variable collection (one mode per theme), one variable per token path, with per-mode values resolved from the token `refs`.
   - **Export to Penpot as a token set** → `ui-color-palette-penpot` — pass `SystemData` and `PaletteData` opaquely. The sub-skill creates a new Penpot token set (one set per theme), one token per path, with values resolved from the token `refs`.

---

## Arguments

`$ARGUMENTS` can describe the taxonomy structure or the project context.

- `/ui-color-palette:build-color-system role × state for a design system`
- `/ui-color-palette:build-color-system brand + neutral × prominence × interaction`

## Tips

- **ref format**: `colorId` is the color's `id` field from `PaletteData`, **not** its display name.
- **partial bindings are fine**: unbound tokens appear in SystemData with `shadeId: null`. They show as `— unbound —` in the matrix.
- **isExcluded vs unbound**: `isExcluded` is an explicit design decision (token exists but is intentionally disabled); unbound is a missing binding.
- **overrides vs primitive cascade**: if the primitive palette already outputs different hex values per theme for the same shade stop, no override is needed — the cascade in CSS/SCSS handles it automatically.

---

## Recommended subagents

- **`color-systemer`** — orchestrates the full source → palette → system → deploy workflow
- **`palette-codegen`** — generates semantic code files from `base` + `themes` + `system`
