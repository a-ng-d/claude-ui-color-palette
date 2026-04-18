---
description: Generate design tokens and code from a color palette in various formats (CSS, SCSS, Less, Tailwind v3/v4, SwiftUI, UIKit, Compose, CSV, DTCG, etc.). Use when the user wants to export colors for development.
---

# Generate Code

Use the **ui-color-palette** MCP tool `generate_code` to export palette data as code or tokens.

## Supported formats

- **Web**: CSS custom properties, SCSS variables, Less variables, Tailwind v3 config, Tailwind v4 theme
- **Mobile**: SwiftUI, UIKit, Jetpack Compose
- **Interchange**: CSV, DTCG (Design Tokens Community Group)

## Workflow

1. Ensure a palette exists (generate one first if needed).
2. Ask the user which format(s) they want.
3. Call `generate_code` with the palette data and target format.
4. Present the generated code in a fenced code block.
5. Offer to write the output to a file in the project.

## Arguments

`$ARGUMENTS` can be: `<format>` or a description of the target.

- Example: `/ui-color-palette:generate-code tailwind-v4`
- Example: `/ui-color-palette:generate-code css variables for my theme`

## Tips

- When the user mentions a specific framework, pick the matching format automatically.
- For design token workflows, prefer DTCG format for interoperability.
- Suggest Tailwind v4 over v3 for new projects.
