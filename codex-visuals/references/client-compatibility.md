# Client Compatibility

Use this file first to choose a rendering mode that the current client can actually display.

## Capability Ladder

1. Mermaid fence for simple graphs and workflows
2. Standalone SVG file embedded with a Markdown image tag
3. Raw source only when the user explicitly asks for source

Default to the highest reliable rung, not the fanciest one.

## Codex Desktop

Codex desktop should be treated as native Mermaid plus SVG first.

- Best primary path for flows: Mermaid fence
- Best primary path for precise layouts: Markdown image tag to a local absolute SVG path
- Mermaid: preferred for simple flows and graphs in Codex desktop
- Custom fences such as `visualizer`: unsupported by default
- HTML widgets and iframe-based interactivity: do not assume support
- Raster export is outside the v1 runtime contract for this repo

## Output Rules By Mode

### SVG + Markdown image

Use when:

- you need precise layout or engineering-style labeling
- the client can render local images
- you want the source to remain editable

Requirements:

- standalone SVG
- embedded fonts avoided
- `title`, `desc`, `viewBox`
- no external `href`, `script`, or `foreignObject`

### Mermaid

Use as the first choice when:

- the diagram is a simple flow or graph
- the current client is Codex desktop or another known Mermaid-capable surface
- text layout is more important than custom geometry

Do not use Mermaid for dense engineering callouts, structural sections, or detailed comparison cards.

## Markdown Embedding

Use absolute paths:

```markdown
![Short alt text](C:/absolute/path/diagram.svg)
```

Alt text should describe the visual in one short phrase.
