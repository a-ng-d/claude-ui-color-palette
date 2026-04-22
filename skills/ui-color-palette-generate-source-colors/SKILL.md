---
name: ui-color-palette-generate-source-colors
description: Generate source colors to seed a palette. Supports three modes — extract dominant colors from an image, generate from a natural language prompt, or derive harmonies from a base color. Output is a set of ColorConfiguration objects ready to pass to ui-color-palette-scale-palette.
argument-hint: <image|prompt|harmony> [input]
---

# Generate Source Colors

Use the **ui-color-palette** MCP tools to produce source colors before building a full palette.

The output of this skill is a set of `ColorConfiguration` objects (role name + hex) ready to be passed to `ui-color-palette-scale-palette`.

---

## Step 0 — Choose a source mode

If the mode is not already clear from context, send:

> How do you want to generate source colors?
> - **Image** — extract dominant colors from a photo or logo (requires a public image URL)
> - **Prompt** — describe the mood, brand, or context in plain language
> - **Harmony** — derive a color set from a single base color using color theory

Stop and wait for the user's answer before proceeding.

---

## Mode A — Image extraction

**Tool**: `extract_dominant_colors`

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `imageUrl` | string | Yes | Public URL of a JPEG or PNG image |
| `colorCount` | number | No | Number of dominant colors to extract (default: 5) |
| `maxIterations` | number | No | Max iterations for k-means clustering |
| `tolerance` | number | No | Convergence tolerance |
| `skipTransparent` | boolean | No | Skip transparent pixels (default: true) |

### Step A1 — Collect the image URL

If the user hasn't provided a URL, send:

> Please share a public URL to the image (JPEG or PNG).

### Step A2 — Ask for color count (optional)

> How many dominant colors do you want to extract? (default: 5)

### Step A3 — Call `extract_dominant_colors`

Call the tool with the URL and parameters. The tool returns colors as hex and/or RGB (0–255 per channel).

### Step A4 — Show results and ask for role names

Present the extracted colors as swatches (hex + a small color preview if possible).

Then send:

> Here are the extracted colors. Assign a role name to each one you want to keep — for example `primary`, `neutral`, `accent`, `error`.
> Remove any colors you don't want in the palette.

### Step A5 — Normalize to ColorConfiguration

Convert each kept color to a `ColorConfiguration` object:
- `id` and `name` = the role name the user provided
- `rgb` = divide each 0–255 channel by 255 → `{ r: R/255, g: G/255, b: B/255 }`
- Apply defaults: `hue: { shift: 0, isLocked: false }`, `chroma: { shift: 100, isLocked: false }`, `alpha: { isEnabled: false, backgroundColor: "#FFFFFF" }`

---

## Mode B — Prompt generation

**Tool**: `generate_colors_from_prompt`

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `prompt` | string | Yes | Natural language description of the desired palette |

### Step B1 — Collect the prompt

If not already provided, send:

> Describe the palette you have in mind. You can mention a mood, a brand, a context, or specific colors.
> Example: *"a calm fintech app with deep blues and warm neutrals"*

### Step B2 — Call `generate_colors_from_prompt`

Call the tool with the prompt string. The tool uses AI (Mistral) to return a set of colors.

### Step B3 — Show results and ask for role names

Present the generated colors as swatches. Then send:

> Here are the suggested colors. Assign a role to each one you want to keep — for example `primary`, `neutral`, `accent`, `error`.
> Feel free to adjust or discard any.

### Step B4 — Normalize to ColorConfiguration

Convert each kept color to a `ColorConfiguration` object using the same mapping as Step A5.

---

## Mode C — Harmony derivation

**Tool**: `create_color_harmony`

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `baseColor` | object | Yes | A Channel object: `{ hue: number, saturation: number, lightness: number }` — HSL, hue 0–360, saturation and lightness 0–100 |
| `type` | enum | No | `ALL`, `COMPLEMENTARY`, `SPLIT_COMPLEMENTARY`, `ANALOGOUS`, `TRIADIC`, `TETRADIC`, `SQUARE` (default: `ALL`) |
| `analogousSpread` | number | No | Spread angle in degrees for analogous harmonies (default: 30) |
| `returnFormat` | enum | No | `rgb`, `hex`, or `both` (default: `both`) |

### Step C1 — Collect the base color

If not already provided, send:

> What is your base color? Provide a hex value (e.g. `#3B82F6`).

Convert the hex to HSL to build the `baseColor` Channel object:
- Parse hex → RGB (0–255)
- Convert RGB → HSL using standard formula
- Round to integers: `{ hue: H, saturation: S, lightness: L }`

### Step C2 — Choose harmony type

Send:

> Which harmony type do you want?
> - **Complementary** — opposite on the color wheel (2 colors)
> - **Split-complementary** — base + two colors adjacent to its complement (3 colors)
> - **Analogous** — neighboring hues (3 colors)
> - **Triadic** — evenly spaced by 120° (3 colors)
> - **Tetradic** — two complementary pairs (4 colors)
> - **Square** — four evenly spaced hues (4 colors)
> - **All** — return all harmony types at once

### Step C3 — Call `create_color_harmony`

Call the tool with the Channel object, selected type, and `returnFormat: "both"`.

### Step C4 — Show results and ask for role names

Present the harmony colors as swatches, grouped by harmony type if `ALL` was selected.

Then send:

> Here are the harmony colors. Pick the ones you want and assign a role name to each — for example `primary`, `secondary`, `accent`.

### Step C5 — Normalize to ColorConfiguration

Convert each kept color to a `ColorConfiguration` object using the same mapping as Step A5.

---

## Output

Once role names are confirmed, present the final source color set as a readable list:

```
Source colors ready:

  primary   #3B82F6
  neutral   #6B7280
  accent    #F59E0B
```

Then hand off to `ui-color-palette-scale-palette` to build the full palette.

---

## Tips

- **Multiple modes**: You can combine modes — for example, extract from an image and then generate a harmony from one of the extracted colors.
- **Hex to HSL**: When converting for `baseColor`, use the standard formula. Round hue to nearest integer, saturation and lightness to one decimal.
- **Hex to RGB 0–1**: Divide each 0–255 channel by 255. E.g. `#3B82F6` → `r: 59/255 ≈ 0.231`, `g: 130/255 ≈ 0.510`, `b: 246/255 ≈ 0.965`.
- **Color count**: For most design systems, 2–5 source colors is ideal — one primary, one neutral, and up to three accents/semantics.
- **Image URL**: The URL must be publicly accessible (no auth, no CORS restriction). Ask the user to upload the image somewhere public if needed.

## Arguments

`$ARGUMENTS` can specify the source mode directly:

- `/ui-color-palette:generate-source-colors image` — jump straight to image URL prompt
- `/ui-color-palette:generate-source-colors prompt warm sunset palette` — use the rest as the prompt
- `/ui-color-palette:generate-source-colors harmony #3B82F6` — use the hex as the base color
