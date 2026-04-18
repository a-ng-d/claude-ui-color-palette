---
description: Audit color pairs for contrast compliance against WCAG 2.1 and APCA standards. Use when the user wants to check accessibility, validate color pairings, or compute a global contrast score for a palette.
---

# Audit Contrast

Use the **ui-color-palette** MCP tool `get_full_palette` to generate a palette with contrast data, then analyze the results for WCAG and APCA compliance.

## Standards

- **WCAG 2.1**: Contrast ratios (AA requires 4.5:1 for normal text, 3:1 for large text; AAA requires 7:1 / 4.5:1)
- **APCA**: Lightness contrast (Lc) values. Minimum Lc 60 for body text, Lc 45 for large text, Lc 30 for non-text.

## Workflow

1. Collect the palette colors from the user or from a previous generation.
2. Call `get_full_palette` with the palette configuration to get contrast data.
3. For each foreground/background pair, report:
   - WCAG contrast ratio and pass/fail for AA and AAA
   - APCA Lc value and minimum font size recommendation
4. Compute a **global contrast score** as a summary:
   - Percentage of pairs passing WCAG AA
   - Average APCA Lc across all pairs
   - Flag any failing pairs prominently
5. Provide actionable recommendations to fix failing pairs (suggest lighter/darker alternatives).

## Arguments

`$ARGUMENTS` can be a list of hex colors to audit.

- Example: `/ui-color-palette:audit-contrast #1E293B #F8FAFC #3B82F6 #FFFFFF`

## Output format

Present results as a table:

| Foreground | Background | WCAG Ratio | AA  | AAA | APCA Lc |
| ---------- | ---------- | ---------- | --- | --- | ------- |

End with the global score and recommendations.
