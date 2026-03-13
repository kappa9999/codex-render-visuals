# Quality Checklist

Run this pass before shipping a user-facing visual.

## Preview Readiness

- The title is obvious within one second.
- The main structure reads correctly at normal README or chat scale.
- No text overlaps geometry, leader lines, or card borders.
- Callout spacing is even and deliberate.

## Contract Integrity

- The output is Mermaid or SVG only.
- SVG includes `viewBox`, `<title>`, and `<desc>`.
- No `script`, `foreignObject`, or external asset references are present.
- The chosen mode matches the request type.

## Repo Hygiene

- The artifact exists at the documented path.
- `README.md`, `examples/prompts.md`, and `examples/catalog.json` describe the same example set.
- No stale `.png` references or removed preview labels remain.
- The SVG validates successfully.

## Scale Safety

- The visual still reads when scaled down in a GitHub README.
- Long sentences are wrapped before they collide with margins.
- Footnotes stay short or are omitted entirely.
