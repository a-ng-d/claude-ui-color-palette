---
name: generate-from-prompt
description: Generate a color palette from a natural language description using AI. Use when the user describes a mood, brand, theme, or aesthetic and wants matching colors.
argument-hint: <prompt>
---

# Generate Colors from Prompt

Use the **ui-color-palette** MCP tool `generate_colors_from_prompt`.

## MCP tool reference

**Tool**: `generate_colors_from_prompt`

**Input schema**:

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `prompt` | string | Yes | Natural language description of the desired palette (e.g. "a warm sunset palette with oranges and pinks") |

**Returns**: An AI-generated palette object with color names and hex values.

## Workflow

1. Take the user's description (mood, brand, theme, season, industry, etc.).
2. Call `generate_colors_from_prompt` with the `prompt` string.
3. Present the generated palette with hex values, names, and suggested usage roles (primary, secondary, accent, neutral).
4. Offer follow-ups:
   - Refine the prompt and regenerate
   - Feed the colors into `get_full_palette` to build a full theme with scales
   - Audit contrast with the `audit-contrast` skill
   - Export to code with the `generate-code` skill

## Arguments

`$ARGUMENTS` is the full prompt text.

- `/ui-color-palette:generate-from-prompt a warm sunset over the ocean, professional and calm`
- `/ui-color-palette:generate-from-prompt cyberpunk neon vibes for a dark UI`

## Tips

- Encourage descriptive prompts: mention mood, industry, temperature, and target audience.
- The prompt is sent to Mistral AI — be specific for better results.
- Suggest combining with `create_color_harmony` for exploring variations of a generated color.
