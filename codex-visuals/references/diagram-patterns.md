# Diagram Patterns

Pick the pattern that matches the user's request.

## Flow Diagram

Use for steps, lifecycles, or pipelines.

- Lay out left-to-right or top-to-bottom
- Keep 4 to 6 nodes in the primary path
- Use arrows with clear start and end points
- Keep node text short enough to fit on one or two lines

Good prompts:

- "Map out the API request lifecycle"
- "Show the steps in plan review"

## Structural Diagram

Use for parts, layers, containment, or support hierarchy.

- Large regions show containers or zones
- Smaller items show subcomponents
- External inputs and outputs sit outside the boundary
- Use callouts instead of stuffing dense text into the geometry

Good prompts:

- "Show the components of this system"
- "Visualize the load path in a house"

## Illustrative Mechanism Diagram

Use when the user asks how something works.

- Draw the object or system in simplified sectional form
- Use arrows to show movement, force, heat, flow, or transfer
- Put explanatory callouts on one side
- Use warm colors for active paths and neutral colors for passive structure

Good prompts:

- "Explain how load transfer works"
- "Show how water moves through the system"

## Comparison Layout

Use for side-by-side choices.

- Split into 2 or 3 balanced columns
- Keep the same categories in the same vertical order
- Use small metrics or pros/cons rows
- End with a short "best fit" row if appropriate

Good prompts:

- "Compare slab-on-grade vs crawlspace"
- "Compare steel framing and mass timber"

## Coordinate Guidance

For a single subject with callouts:

- Main geometry: left 55 percent
- Callouts: right 45 percent
- Title at top
- Keep a dedicated header zone so decorative arrows never pass behind the title or subtitle
- Summary note at bottom only if it adds value

For process visuals:

- Evenly space primary nodes
- Keep connector bends orthogonal when direct lines would cross boxes
- Prefer compact height so the figure still reads cleanly when scaled in a README or chat transcript

## Label Rules

- Prefer short noun phrases
- Explanations belong in callouts, not inside core geometry
- Wrap callout copy into short stacked lines when one sentence would run wider than the available column
- Every leader line must terminate clearly
- Every arrow should encode one meaning only
- If the figure becomes crowded, remove decorative arrows before shrinking text

## Common Failure Modes

- too many colors
- tiny text
- clipped labels
- decorative backgrounds
- callouts scattered on both sides with no reading order
- arrows passing through unrelated geometry
