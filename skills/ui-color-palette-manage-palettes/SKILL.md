---
name: ui-color-palette-manage-palettes
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
2. Generate an HTML card list (see **Visual display** below) — never show raw JSON.

### Load a palette for reuse

1. Call `get_published_palette` with the `paletteId`.
2. Generate an HTML detail card (see **Visual display** below).
3. **Session state**: store the result as the `PublishedPaletteConfig` slot. It contains `colors`, `preset`, `shift`, `themes`, `color_space`, and `algorithm_version` — all the parameters needed to call `get_full_palette`.
4. Confirm to the user:

   > Palette **"Name"** loaded. You can now scale it, export code, or push it to a design tool — I'll use this configuration automatically.

`ui-color-palette-scale-palette` will detect the `PublishedPaletteConfig` slot and skip its Step 0 questions, going straight to the palette build.

### Publish a palette

1. Call `start_authentication` if no token is available — instruct the user to open the returned `auth_url`.
2. Collect palette data (name, colors, themes, preset, shift, etc.).
3. Call `publish_palette` with the full payload.
4. Confirm publication and provide the palette ID.
5. Optionally call `share_published_palette` to make it publicly visible.

### Update a palette

1. Authenticate if needed.
2. Call `update_published_palette` with `paletteId` and only the fields to change.

---

## Visual display

Never show raw JSON for any palette response. Always generate an HTML artifact.

The source colors in published palettes are the **seed colors** (not the full shade ramp). Display them as color chips using `colors[i].name` as the label and the closest hex field as the background.

### After `list_published_palettes` or `list_my_published_palettes`

One card per palette. Cards are stacked vertically. Each card shows:

- palette name
- color space, preset name, theme count, and visibility badge
- one color chip per source color
- palette ID

```html
<div style="font-family:sans-serif;padding:16px;display:flex;flex-direction:column;gap:12px">

  <div style="border:1px solid #e5e7eb;border-radius:8px;padding:12px">
    <div style="font-weight:600;font-size:14px;margin-bottom:2px">Ocean Breeze</div>
    <div style="font-size:11px;color:#888;margin-bottom:8px">OKLCH &middot; Material &middot; 2 themes &middot; [public]</div>
    <div style="display:flex;gap:6px;flex-wrap:wrap">
      <div style="text-align:center">
        <div style="width:40px;height:40px;background:#2563EB;border-radius:4px"></div>
        <div style="font-size:9px;color:#555;margin-top:2px">primary</div>
      </div>
      <div style="text-align:center">
        <div style="width:40px;height:40px;background:#6B7280;border-radius:4px"></div>
        <div style="font-size:9px;color:#555;margin-top:2px">neutral</div>
      </div>
      <!-- repeat per colors[] entry -->
    </div>
    <div style="font-size:10px;color:#bbb;margin-top:8px">ID: abc123</div>
  </div>

  <!-- repeat per palette -->

</div>
```

### After `get_published_palette`

A single detail card with larger chips and the palette description. Render this **before** the session state confirmation message.

```html
<div style="font-family:sans-serif;padding:16px;max-width:520px">
  <h2 style="margin:0 0 4px;font-size:18px">Ocean Breeze</h2>
  <p style="margin:0 0 10px;color:#555;font-size:13px">A cool ocean-inspired palette.</p>
  <div style="font-size:11px;color:#888;margin-bottom:14px">
    OKLCH &middot; Material &middot; Light + Dark &middot; v3 &middot; [private]
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap">
    <div style="text-align:center">
      <div style="width:56px;height:56px;background:#2563EB;border-radius:6px"></div>
      <div style="font-size:10px;margin-top:4px">primary</div>
      <div style="font-size:9px;color:#888">#2563EB</div>
    </div>
    <div style="text-align:center">
      <div style="width:56px;height:56px;background:#6B7280;border-radius:6px"></div>
      <div style="font-size:10px;margin-top:4px">neutral</div>
      <div style="font-size:9px;color:#888">#6B7280</div>
    </div>
    <!-- repeat per colors[] entry -->
  </div>
  <div style="margin-top:14px;font-size:10px;color:#bbb">ID: abc123</div>
</div>
```

#### Text fallback

If HTML cannot be rendered, show a compact list:

```
Ocean Breeze -- OKLCH - Material - Light + Dark - v3 - [private]
  primary   #2563EB
  neutral   #6B7280
  success   #16A34A
ID: abc123
```

---

## Arguments

`$ARGUMENTS` can be:

- A search query: `/ui-color-palette:manage-palettes sunset warm`
- An action: `/ui-color-palette:manage-palettes list mine`
- A palette ID: `/ui-color-palette:manage-palettes get abc123`

## Tips

- Palettes are private by default after publication — the user must explicitly `share_published_palette` to make them public.
- Use `list_my_published_palettes` to find palette IDs for update/delete operations.
- The `preset`, `shift`, `colors`, and `themes` fields match the structures used by `get_full_palette`.

---

## Recommended subagent

Delegate this skill to **`palette-publisher`**.

The `palette-publisher` agent handles all palette lifecycle operations: browse, retrieve, publish, update, share, unshare, and delete. It resolves authentication before any authenticated call and applies minimal update payloads.
