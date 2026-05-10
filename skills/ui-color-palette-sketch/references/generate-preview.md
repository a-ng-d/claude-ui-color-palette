---
name: ui-color-palette-sketch-generate-preview
description: Draw a palette swatch board directly on the Sketch canvas as a visual preview. Uses Stack groups. Not a style/variable/token export — canvas rendering only.
---

# Generate Palette Preview — Sketch

Draw a palette swatch board directly on the canvas using the Sketch MCP API. This is a **canvas rendering**, not a style, variable, or token export.

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

## Sketch layer hierarchy

```
Group "Palette Preview"          ← root, Stack vertical, gap 24, padding 24, background #F5F5F5
  Group "<theme name>"           ← Stack vertical, gap 4, padding 16, background #FFFFFF, corner 8
    Text "<theme name>"          ← 14px, bold, #111111
    Group "<color name>"         ← Stack horizontal, align middle, gap 0, no background
      Text "<color name>"        ← 88px wide, 10px, medium, #555555, truncate
      Rectangle "50"             ← swatch, see below
      Rectangle "100"
      …
  Group "<next theme>"
  …
```

### Swatch

Sketch does not support nested text inside a rectangle natively — use a **Group** containing a rectangle (fill) and text layers on top:

```
Group "<shade>"                  ← Stack vertical, gap 4, padding 8
  Rectangle                      ← 64×80 (or 64×120 with scores), fill = shade hex
  Text (shade name)              ← 10px, bold, contrasted color
  Text (hex)                     ← 8px, contrasted color, 70% opacity
  Text (WCAG light)              ← 7px, contrasted color, 80% opacity (if requested)
  Text (WCAG dark)               ← 7px, contrasted color, 80% opacity (if requested)
  Text (APCA light)              ← 7px, contrasted color, 80% opacity (if requested)
  Text (APCA dark)               ← 7px, contrasted color, 80% opacity (if requested)
```

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

## Sketch MCP API sequence

1. Create root group with vertical Stack
2. For each theme:
   a. Create a theme group with vertical Stack, white background
   b. Add theme name text
   c. For each color in that theme:
      - Create a row group with horizontal Stack, no background
      - Add color name text (fixed 88px width)
      - For each shade:
        - Create a swatch group with vertical Stack
        - Add background rectangle (64×80 or 64×120), fill = shade hex
        - Add shade name text
        - Add hex text
        - If scores requested: add WCAG and/or APCA text layers
3. Place root group on a dedicated page named `Palette Preview` (create if it doesn't exist)

---

## Naming convention

- Root group: `Palette Preview — <palette name>`
- Theme group: `<theme name>`
- Color row group: `<color name>`
- Swatch group: `<shade>` (e.g. `500`)
