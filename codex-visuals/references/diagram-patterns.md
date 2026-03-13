# Diagram Patterns

Pick the diagram mode by pattern, not by preference.

## Use Mermaid

Choose Mermaid when the request is primarily a graph:

- workflow
- lifecycle
- request path
- service interaction
- simple decision flow

Keep Mermaid compact. If the diagram needs custom geometry, dense annotation, or asymmetric layout, switch to SVG.

## Use SVG

Choose SVG when the request needs layout precision:

- structural or engineering load path
- side-by-side comparison board
- annotated mechanism diagram
- explainer with callouts, leader lines, or spatial relationships

SVG should be the default for any visual where text placement and spacing are part of the explanation.

## Pattern Notes

- Comparison boards: SVG only
- Load paths and building sections: SVG only
- API or software lifecycles: Mermaid first, SVG only when annotation density demands it
- Public README examples: favor the format that reads best inline with no extra tooling
