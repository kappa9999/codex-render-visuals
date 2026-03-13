# Quality Checklist

Run this checklist before sending a user-facing visual.

## Technical

- file writes successfully
- SVG parses cleanly
- `title`, `desc`, and `viewBox` are present
- no external URLs, scripts, or `foreignObject`
- output path is absolute before embedding

## Visual

- title is concise
- labels are readable at normal chat width
- long callouts are wrapped into short lines instead of one clipped sentence
- color count is limited
- the main subject is obvious within one second
- whitespace is sufficient
- arrows and leader lines do not create confusion

## Communication

- the visual answers the user's actual question
- the caption does not restate the entire figure
- any limitation or assumption is stated plainly
- the chosen mode matches the client's known capabilities

## Release Readiness

- install works on a fresh Codex profile
- quick validation passes
- smoke render passes
- example outputs are current
- PNG fallbacks are regenerated from SVG with `scripts/export_svg_png.py`
- README screenshots match current behavior
