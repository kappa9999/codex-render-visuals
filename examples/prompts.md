# Example Prompts

Use these prompts to confirm that `codex-visuals` chooses the correct native output mode and writes the expected artifact set.

## Engineering SVG: House Load Transfer

Prompt:

```text
Use $codex-visuals to visualize gravity load transfer in a typical house as a clean structural engineering SVG.
```

Expected mode: `svg`

Primary artifact:

- `examples/house-load-transfer.svg`

## Workflow Mermaid: API Request Lifecycle

Prompt:

```text
Use $codex-visuals to draw an API request lifecycle from browser to database and back as a native Mermaid flowchart.
```

Expected mode: `mmd`

Primary artifact:

- `examples/api-request-lifecycle.mmd`

Supporting artifact:

- `examples/api-request-lifecycle.svg`

## Comparison SVG: SQLite vs PostgreSQL

Prompt:

```text
Use $codex-visuals to compare SQLite and PostgreSQL as a clean two-column SVG decision board for engineering teams.
```

Expected mode: `svg`

Primary artifact:

- `examples/sqlite-vs-postgres.svg`

## Review Checklist

- The output mode matches the prompt type.
- Mermaid examples stay graph-like and compact.
- SVG examples stay readable at README scale without text collisions.
- Every public artifact exists and validates cleanly.
