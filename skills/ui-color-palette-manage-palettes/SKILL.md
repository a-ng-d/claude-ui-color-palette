---
name: manage-palettes
description: Browse, publish, share, update, and delete palettes on the UI Color Palette platform. Use when the user wants to manage their published palettes or explore community palettes.
argument-hint: <action|search-query|palette-id>
---

# Manage Palettes

Use the **ui-color-palette** MCP tools for palette lifecycle management.

## Authentication

Tools marked **Auth: Yes** require a JWT access token. Obtain one by calling `start_authentication` first — it returns an `auth_url` the user must open in their browser plus tokens upon completion.

Pass the `accessToken` as a parameter to every authenticated tool call.

---

## Browse palettes

### `list_published_palettes` (Auth: No)

Browse public community palettes.

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `page` | number | No | Page number (default: 1) |
| `limit` | number | No | Results per page, max 50 (default: 20) |
| `search` | string | No | Filter palettes by name |

### `get_published_palette` (Auth: No)

Fetch a specific palette by ID.

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `paletteId` | string | Yes | Unique palette identifier |

---

## Manage your palettes

### `list_my_published_palettes` (Auth: Yes)

List the authenticated user's own palettes.

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `accessToken` | string | Yes | JWT from `start_authentication` |
| `page` | number | No | Page number (default: 1) |
| `limit` | number | No | Results per page, max 50 (default: 20) |
| `search` | string | No | Filter palettes by name |

### `publish_palette` (Auth: Yes)

Publish a new palette.

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `accessToken` | string | Yes | JWT from `start_authentication` |
| `name` | string | Yes | Palette name |
| `description` | string | No | Palette description |
| `preset` | object | Yes | `PresetConfiguration` object |
| `shift` | object | Yes | `ShiftConfiguration` object (hue/saturation/lightness adjustments) |
| `are_source_colors_locked` | boolean | Yes | Whether source colors are pinned |
| `colors` | array | Yes | Array of color definition objects |
| `themes` | array | Yes | Array of `ThemeConfiguration` objects |
| `color_space` | string | Yes | Color space (e.g. `"LCH"`, `"OKLCH"`, `"RGB"`) |
| `algorithm_version` | string | Yes | Algorithm version (e.g. `"v2"`) |
| `is_shared` | boolean | No | Whether publicly visible (default: false) |

### `update_published_palette` (Auth: Yes)

Update an existing palette. All fields except `accessToken` and `paletteId` are optional — only send fields to change.

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `accessToken` | string | Yes | JWT from `start_authentication` |
| `paletteId` | string | Yes | Unique palette identifier |
| `name` | string | No | Updated name |
| `description` | string | No | Updated description |
| `preset` | object | No | Updated preset configuration |
| `shift` | object | No | Updated shift configuration |
| `are_source_colors_locked` | boolean | No | Updated lock state |
| `colors` | array | No | Updated color definitions |
| `themes` | array | No | Updated theme configurations |
| `color_space` | string | No | Updated color space |
| `algorithm_version` | string | No | Updated algorithm version |
| `is_shared` | boolean | No | Updated sharing visibility |

---

## Share & visibility

### `share_published_palette` (Auth: Yes)

Make a palette publicly visible.

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `accessToken` | string | Yes | JWT from `start_authentication` |
| `paletteId` | string | Yes | Palette to share |

### `unshare_published_palette` (Auth: Yes)

Make a palette private (remove from community listing).

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `accessToken` | string | Yes | JWT from `start_authentication` |
| `paletteId` | string | Yes | Palette to unshare |

---

## Delete

### `unpublish_palette` (Auth: Yes)

Permanently delete a palette.

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `accessToken` | string | Yes | JWT from `start_authentication` |
| `paletteId` | string | Yes | Palette to delete |

---

## Workflow

### Browse palettes

1. Call `list_published_palettes` with optional `search` and `page`/`limit`.
2. Present results as a table with name, creator, and color preview swatches.

### Publish a palette

1. Call `start_authentication` if no token is available — instruct the user to open the returned `auth_url`.
2. Collect palette data (name, colors, themes, preset, shift, etc.).
3. Call `publish_palette` with the full payload.
4. Confirm publication and provide the palette ID.
5. Optionally call `share_published_palette` to make it publicly visible.

### Update a palette

1. Authenticate if needed.
2. Call `update_published_palette` with `paletteId` and only the fields to change.

## Arguments

`$ARGUMENTS` can be:

- A search query: `/ui-color-palette:manage-palettes sunset warm`
- An action: `/ui-color-palette:manage-palettes list mine`
- A palette ID: `/ui-color-palette:manage-palettes get abc123`

## Tips

- Palettes are private by default after publication — the user must explicitly `share_published_palette` to make them public.
- Use `list_my_published_palettes` to find palette IDs for update/delete operations.
- The `preset`, `shift`, `colors`, and `themes` fields match the structures used by `get_full_palette`.
