---
name: ui-color-palette-framer-generate-preview
description: Draw a palette swatch board directly on the Framer canvas as a visual preview. Uses Stack layouts. Not a style/token export — canvas rendering only.
---

# Generate Palette Preview — Framer

Draw a palette swatch board directly on the canvas using the Framer MCP API. This is a **canvas rendering**, not a style or token export.

---

## Target visual structure

```
╔══════════════════════════════════════════════════════╗
║ Light                                                ║
║  Primary  [ 50 ][ 100 ][ 200 ][ 300 ][ 400 ][ 500 ] ║
║  Neutral  [ 50 ][ 100 ][ 200 ][ 300 ][ 400 ][ 500 ] ║
╚══════════════════════════════════════════════════════╝
```

Each swatch cell:

```
╔════════════╗
║  500        ║  ← shade name, 10px bold, contrasted text color
║  #3b5bdb    ║  ← hex, 8px, contrasted text color, 70% opacity
║             ║
║ W 4.6 AA    ║  ← WCAG light text ratio + score (if scores requested)
║ W 4.5 AA    ║  ← WCAG dark text ratio + score
║ Lc 47 BODY  ║  ← APCA light Lc + usage (if APCA requested)
║ Lc 48 BODY  ║  ← APCA dark Lc + usage
╚════════════╝
```

Scores are only added if the user requested them in Step 3. If no scores, the cell contains only shade name and hex.

---

## Framer layer hierarchy

```
Frame "Palette Preview"          ← root, Stack vertical, gap 24, padding 24, background #F5F5F5
  Frame "<theme name>"           ← Stack vertical, gap 4, padding 16, background #FFFFFF, radius 8
    Text "<theme name>"          ← 14px, bold, #111111
    Frame "<color name>"         ← Stack horizontal, align center, gap 0, no background
      Text "<color name>"        ← 88px wide, 10px, medium, #555555, truncate
      Frame "50"                 ← swatch, see below
      Frame "100"
      …
  Frame "<next theme>"
  …
```

### Swatch frame

| Property | Value |
|---|---|
| Width | 64 px |
| Height | 80 px (no scores) / 120 px (with scores) |
| Background | shade hex |
| Layout | Stack vertical, align center, gap 4, padding 8 |

### Text layers inside swatch

| Layer | Content | Size | Weight | Fill | Opacity |
|---|---|---|---|---|---|
| Shade name | e.g. `500` | 10 px | 600 | contrasted color | 100% |
| Hex | e.g. `#3B5BDB` | 8 px | 400 | contrasted color | 70% |
| WCAG light | e.g. `W 4.6 AA` | 7 px | 400 | contrasted color | 80% |
| WCAG dark | e.g. `W 4.5 AA` | 7 px | 400 | contrasted color | 80% |
| APCA light | e.g. `Lc 47 BODY` | 7 px | 400 | contrasted color | 80% |
| APCA dark | e.g. `Lc 48 BODY` | 7 px | 400 | contrasted color | 80% |

**Contrasted color**: use `#FFFFFF` if the shade luminance is below 0.179 (relative luminance), otherwise `#000000`.

---

## Framer MCP API sequence

1. Create root frame with vertical Stack layout
2. For each theme:
   a. Create a theme frame with vertical Stack layout, white background
   b. Add theme name text
   c. For each color in that theme:
      - Create a row frame with horizontal Stack layout, no background
      - Add color name text (fixed 88px width)
      - For each shade:
        - Create swatch frame (64×80 or 64×120), background = shade hex
        - Add shade name text (white or black based on luminance)
        - Add hex text
        - If scores requested: add WCAG and/or APCA text layers
3. Place root frame at a clear position on the canvas

---

## Naming convention

- Root frame: `Palette Preview — <palette name>`
- Theme frame: `<theme name>`
- Color row frame: `<color name>`
- Swatch frame: `<shade>` (e.g. `500`)
