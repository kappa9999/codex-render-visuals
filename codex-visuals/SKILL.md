---
name: codex-visuals
description: Create native Mermaid and SVG visuals for Codex-compatible clients. Use this skill when Codex needs to visualize a workflow, load path, system diagram, comparison, or annotated explanation that is clearer as a visual than as prose alone.
---

# Codex Visuals

Create visuals that stay on native Codex rendering paths.

Read these files before producing the first visual in a task:

- `references/client-compatibility.md`
- `references/design-system.md`
- `references/diagram-patterns.md`

Read `references/quality-checklist.md` before finalizing a public-facing SVG.

## Workflow

### 1. Choose The Diagram Type

Map the request to one of these patterns:

- workflow or lifecycle
- engineering or annotated structure
- comparison board
- system diagram

### 2. Choose The Native Output Mode

Use Mermaid for graph-style workflows, lifecycles, and simple request flows.

Use SVG for engineering diagrams, comparison boards, and annotated layouts that need precise geometry.

Do not introduce PNG, browser export, HTML widgets, or custom fences in v1.

### 3. Write The Artifact

Use `scripts/write_visual.py` for deterministic output paths.

SVG example:

```bash
python codex-visuals/scripts/write_visual.py --slug house-load-transfer --format svg --output-dir ./visuals --source-file ./draft.svg --print-markdown --alt "House load transfer diagram"
```

Mermaid example:

```bash
python codex-visuals/scripts/write_visual.py --slug api-request-lifecycle --format mmd --output-dir ./visuals --source-file ./draft.mmd --print-fence
```

### 4. Validate

Validate every user-facing SVG:

```bash
python codex-visuals/scripts/validate_svg.py /absolute/path/to/file.svg
```

For repo maintenance, also run:

```bash
python codex-visuals/scripts/quick_validate.py
python codex-visuals/scripts/render_smoke_svg.py --output ./tmp/smoke.svg
```

### 5. Respond Cleanly

- Use a short sentence of context.
- Show the Mermaid fence or Markdown image.
- Add one short note only when it helps interpretation.

Do not dump raw source unless the user explicitly asks for it.
