# Example prompts

Use these prompts to verify that `codex-visuals` chooses a sensible native output mode without introducing a raster step.

## 1. Structural explanation

Prompt:

```text
Use $codex-visuals to visualize load transfer in a house as a production SVG diagram.
```

Expected mode:

- Primary: standalone SVG embedded as a Markdown image

Expected artifact:

- `examples/house-load-transfer.svg`

## 2. Process flow

Prompt:

```text
Use $codex-visuals to draw a flowchart of an API request lifecycle from browser to database and back.
```

Expected mode:

- Mermaid fence in Codex desktop
- SVG only when the flow needs custom geometry or annotation density Mermaid cannot handle

Expected artifact:

- `examples/api-request-lifecycle.mmd`
- `examples/api-request-lifecycle.svg`
- A single annotated diagram with arrows, retries if relevant, and clear failure/response branches

## 3. Comparison layout

Prompt:

```text
Use $codex-visuals to compare slab-on-grade versus crawlspace foundations for an early-stage residential design review.
```

Expected mode:

- SVG comparison board

Expected artifact:

- Two side-by-side visual columns with concise pros, constraints, and site-fit callouts

## Review checklist

- The output is Mermaid or SVG, not a raster screenshot.
- Labels are readable at normal chat width.
- The diagram has an obvious title, hierarchy, and margins.
- There is no clipped content or overlapping annotation text.
