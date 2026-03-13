# Design System

Optimize every public visual for README scale and normal chat width.

## Typography

- Use a system sans stack: `"Segoe UI", Roboto, Helvetica, Arial, sans-serif`
- Keep titles between `34px` and `42px`
- Keep section labels between `18px` and `24px`
- Keep body copy between `14px` and `18px`
- Wrap long copy into short lines instead of stretching one sentence across the canvas

## Layout

- Reserve a dedicated header band; no arrows or geometry may cross it
- Use generous outer margins
- Keep clear gutters between the main graphic and callout cards
- Prefer one dominant panel instead of many small disconnected boxes
- Leave at least `24px` vertical breathing room between stacked cards

## SVG Rules

- Include `viewBox`, `<title>`, and `<desc>`
- Keep backgrounds white or very light
- Avoid external fonts, scripts, or network references
- Prefer simple gradients and restrained shadows over decorative effects
- Use consistent stroke weights within the same diagram family

## Preview-Safe Rules

- Do not let leader lines pass through body text
- Do not rely on tiny legends or dense footnotes
- Keep all meaningful text readable without zooming
- Stop copy before the last safe margin; never let it touch a card edge
- Design for a single quick glance before the user reads the details
