# Client Compatibility

Use this file first to choose a rendering mode that the current client can actually display.

## Capability Ladder

1. Standalone SVG file embedded with a Markdown image tag
2. PNG file embedded with a Markdown image tag
3. Mermaid fence for simple graphs when Mermaid support is known
4. Raw source only when the user explicitly asks for source

Default to the highest reliable rung, not the fanciest one.

## Codex Desktop

Codex desktop should be treated as image-first unless proven otherwise.

- Best primary path: Markdown image tag to a local absolute path
- Preferred source artifact: SVG
- Safe fallback artifact: PNG
- Mermaid: likely available in some builds, but do not promise it unless verified in the current environment
- Custom fences such as `visualizer`: unsupported by default
- HTML widgets and iframe-based interactivity: do not assume support

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

### PNG + Markdown image

Use when:

- SVG rendering looks off
- you need a compatibility-first response
- you want the exact appearance frozen

Keep the SVG source alongside the PNG whenever possible.

### Mermaid

Use only when:

- the diagram is a simple flow or graph
- the current client is known to render Mermaid
- text layout is more important than custom geometry

Do not use Mermaid for dense engineering callouts, structural sections, or detailed comparison cards.

## Markdown Embedding

Use absolute paths:

```markdown
![Short alt text](C:/absolute/path/diagram.svg)
```

Alt text should describe the visual in one short phrase.
