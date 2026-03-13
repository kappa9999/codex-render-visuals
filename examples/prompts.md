# Example prompts

Use these prompts to verify that `codex-visuals` chooses a sensible output mode and produces a clean image artifact.

## 1. Structural explanation

Prompt:

```text
Use $codex-visuals to visualize load transfer in a house as a production SVG diagram with a PNG fallback if needed.
```

Expected mode:

- Primary: standalone SVG embedded as a Markdown image
- Fallback: PNG

Expected artifact:

- `examples/house-load-transfer.svg`
- `examples/house-load-transfer.png`

## 2. Process flow

Prompt:

```text
Use $codex-visuals to draw a flowchart of an API request lifecycle from browser to database and back.
```

Expected mode:

- SVG flowchart
- Mermaid only if the client is known to render Mermaid reliably

Expected artifact:

- `examples/api-request-lifecycle.svg`
- `examples/api-request-lifecycle.png`
- A single annotated diagram with arrows, retries if relevant, and clear failure/response branches

## 3. Comparison layout

Prompt:

```text
Use $codex-visuals to compare slab-on-grade versus crawlspace foundations for an early-stage residential design review.
```

Expected mode:

- SVG comparison board
- PNG fallback when typography or SVG rendering is inconsistent

Expected artifact:

- Two side-by-side visual columns with concise pros, constraints, and site-fit callouts

## Review checklist

- The output is embedded as an image, not a custom fence.
- Labels are readable at normal chat width.
- The diagram has an obvious title, hierarchy, and margins.
- There is no clipped content or overlapping annotation text.
