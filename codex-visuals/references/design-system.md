# Design System

This skill targets production static visuals inside chat, not decorative illustrations.

## Principles

- Flat over flashy
- Clear hierarchy over novelty
- Compact over sprawling
- Accurate labeling over ornament
- Readable at chat width

## Typography

- Sans serif only by default
- Title: 22px to 28px
- Primary labels: 14px to 18px
- Secondary labels: 12px to 14px
- Minimum text size: 11px
- Use sentence case
- Use bold sparingly for structure, not emphasis noise

Good font stack for standalone SVG:

```text
"Segoe UI", Arial, sans-serif
```

## Color

Limit each visual to 2 to 4 semantic groups.

- Neutral structure: `#E5E7EB` fill, `#4B5563` stroke
- Information / framing: `#DBEAFE` fill, `#2563EB` stroke
- Warning / load path: `#FEF3C7` fill, `#D97706` stroke
- Emphasis / bearing or critical load path: `#FEE2E2` fill, `#DC2626` stroke
- Success / support medium or accepted state: `#D1FAE5` fill, `#059669` stroke
- Primary text: `#1F2937`
- Secondary text: `#4B5563`
- Light border: `#E5E7EB`

Avoid gradients, shadows, blur, glow, textures, and glassmorphism.

## Layout

- Give the visual a 32px to 48px safe margin
- Reserve a clear title band at the top; arrows, leaders, and geometry should not pass through title or subtitle copy
- Keep the main subject on the left or center, callouts on one side
- Leave enough whitespace between callouts to read each one independently
- Avoid crossing arrows whenever possible
- Prefer one clear reading direction
- Scale for README width first, then add detail only if it still reads cleanly when reduced

## SVG Structure

Every production SVG should include:

- `viewBox`
- `title`
- `desc`
- a small internal stylesheet or repeated presentation attributes
- transparent or white background

Recommended:

- rounded corners: 4px to 12px
- border width: 1px to 2.5px
- leader lines: dashed neutral gray
- load arrows: warm color with consistent marker

## Accessibility

- Do not rely on color alone to distinguish meaning
- Use labels or patterns when categories could be confused
- Keep contrast strong enough for light backgrounds
- Prefer short labels over wrapped paragraphs inside the figure
