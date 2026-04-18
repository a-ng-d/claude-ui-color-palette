---
description: Browse, publish, share, update, and delete palettes on the UI Color Palette platform. Use when the user wants to manage their published palettes or explore community palettes.
---

# Manage Palettes

Use the **ui-color-palette** MCP tools for palette lifecycle management.

## Available tools

| Tool                         | Auth | Description                                    |
| ---------------------------- | ---- | ---------------------------------------------- |
| `list_published_palettes`    | No   | Browse public palettes (paginated, searchable) |
| `list_my_published_palettes` | Yes  | List the user's own palettes                   |
| `get_published_palette`      | No   | Get a specific palette by ID                   |
| `publish_palette`            | Yes  | Publish a new palette                          |
| `share_published_palette`    | Yes  | Make a palette public                          |
| `unshare_published_palette`  | Yes  | Make a palette private                         |
| `update_published_palette`   | Yes  | Update an existing palette                     |
| `unpublish_palette`          | Yes  | Delete a palette                               |

## Workflow

### Browse palettes

1. Call `list_published_palettes` with optional search query and pagination.
2. Present results as a table with name, creator, and color previews.

### Publish a palette

1. Ensure the user is authenticated (call `start_authentication` if needed).
2. Collect palette data (name, colors, description).
3. Call `publish_palette` with the palette payload.
4. Confirm publication and provide the palette ID.

## Arguments

`$ARGUMENTS` can be:

- A search query: `/ui-color-palette:manage-palettes sunset warm`
- An action: `/ui-color-palette:manage-palettes list mine`
- A palette ID: `/ui-color-palette:manage-palettes get abc123`
