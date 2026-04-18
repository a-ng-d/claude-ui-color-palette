---
description: Generate a color palette from a natural language description using AI. Use when the user describes a mood, brand, theme, or aesthetic and wants matching colors.
---

# Generate Colors from Prompt

Use the **ui-color-palette** MCP tool `generate_colors_from_prompt` to create a palette from a text description.

## Workflow

1. Take the user's natural language description (mood, brand, theme, season, etc.).
2. Call `generate_colors_from_prompt` with the description.
3. Present the generated palette with hex values, names, and usage suggestions (primary, secondary, accent, neutral, etc.).
4. Offer follow-up actions:
   - Refine the prompt and regenerate
   - Generate a full palette with `get_full_palette`
   - Audit contrast with `audit-contrast` skill
   - Export to code with `generate-code` skill

## Arguments

`$ARGUMENTS` is the full prompt text.

- Example: `/ui-color-palette:generate-from-prompt a warm sunset over the ocean, professional and calm`

## Tips

- Encourage descriptive prompts: mention mood, industry, temperature, and target audience.
- Suggest combining with harmony generation for richer palettes.
