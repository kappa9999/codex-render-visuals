#!/usr/bin/env python3
"""Generate a deterministic smoke-test SVG for codex-visuals."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_svg import validate_svg_file
from write_visual import write_text_artifact


SMOKE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="500" viewBox="0 0 1080 500" role="img" aria-labelledby="title desc">
  <title id="title">API request lifecycle</title>
  <desc id="desc">A polished left-to-right flow showing browser request, gateway routing, service execution, database query, and response return.</desc>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
  <rect x="24" y="24" width="1032" height="452" rx="24" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="2"/>
  <text x="52" y="68" font-family="Segoe UI, Arial, sans-serif" font-size="30" font-weight="600" fill="#1F2937">API request lifecycle</text>
  <text x="52" y="96" font-family="Segoe UI, Arial, sans-serif" font-size="15" fill="#4B5563">Reference flow for the codex-visuals smoke renderer.</text>

  <rect x="60" y="152" width="190" height="92" rx="16" fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>
  <rect x="300" y="152" width="190" height="92" rx="16" fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>
  <rect x="540" y="152" width="190" height="92" rx="16" fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>
  <rect x="780" y="152" width="190" height="92" rx="16" fill="#E5E7EB" stroke="#4B5563" stroke-width="2"/>

  <text x="155" y="186" font-family="Segoe UI, Arial, sans-serif" font-size="20" font-weight="600" fill="#1F2937" text-anchor="middle">Browser client</text>
  <text x="155" y="212" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#4B5563" text-anchor="middle">Sends authenticated</text>
  <text x="155" y="232" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#4B5563" text-anchor="middle">request to the API</text>

  <text x="395" y="186" font-family="Segoe UI, Arial, sans-serif" font-size="20" font-weight="600" fill="#1F2937" text-anchor="middle">Gateway</text>
  <text x="395" y="212" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#4B5563" text-anchor="middle">Applies auth, rate</text>
  <text x="395" y="232" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#4B5563" text-anchor="middle">limits, and routing</text>

  <text x="635" y="186" font-family="Segoe UI, Arial, sans-serif" font-size="20" font-weight="600" fill="#1F2937" text-anchor="middle">Application service</text>
  <text x="635" y="212" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#4B5563" text-anchor="middle">Runs domain logic and</text>
  <text x="635" y="232" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#4B5563" text-anchor="middle">builds a response</text>

  <text x="875" y="186" font-family="Segoe UI, Arial, sans-serif" font-size="20" font-weight="600" fill="#1F2937" text-anchor="middle">Database</text>
  <text x="875" y="212" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#4B5563" text-anchor="middle">Reads or writes</text>
  <text x="875" y="232" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#4B5563" text-anchor="middle">persistent state</text>

  <path d="M250 198 L300 198" fill="none" stroke="#D97706" stroke-width="3" stroke-linecap="round" marker-end="url(#arrow)"/>
  <path d="M490 198 L540 198" fill="none" stroke="#D97706" stroke-width="3" stroke-linecap="round" marker-end="url(#arrow)"/>
  <path d="M730 198 L780 198" fill="none" stroke="#D97706" stroke-width="3" stroke-linecap="round" marker-end="url(#arrow)"/>

  <path d="M875 244 L875 314 L635 314" fill="none" stroke="#4B5563" stroke-width="3" stroke-linecap="round" marker-end="url(#arrow)"/>
  <path d="M635 336 L395 336 L155 336" fill="none" stroke="#059669" stroke-width="3" stroke-linecap="round" marker-end="url(#arrow)"/>

  <text x="816" y="300" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#4B5563">query result</text>
  <text x="465" y="326" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#4B5563">JSON response returns to the caller</text>

  <rect x="60" y="388" width="910" height="74" rx="14" fill="#F9FAFB" stroke="#E5E7EB" stroke-width="1.5"/>
  <text x="84" y="418" font-family="Segoe UI, Arial, sans-serif" font-size="15" font-weight="600" fill="#1F2937">Why this sample exists</text>
  <text x="250" y="418" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#4B5563">
    <tspan x="250" dy="0">It exercises node layout, arrow routing,</tspan>
    <tspan x="250" dy="18">and a return path inside one</tspan>
    <tspan x="250" dy="18">compact artifact.</tspan>
  </text>
</svg>
"""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a deterministic smoke-test SVG.")
    parser.add_argument("--output", help="Exact output path.")
    parser.add_argument("--output-dir", help="Directory to write api-request-lifecycle.svg into.")
    return parser.parse_args(argv)


def choose_output_path(args: argparse.Namespace) -> tuple[Path, bool]:
    if args.output:
        path = Path(args.output).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        return path, False
    if args.output_dir:
        directory = Path(args.output_dir).expanduser().resolve()
        directory.mkdir(parents=True, exist_ok=True)
        return (directory / "api-request-lifecycle.svg").resolve(), False
    path = write_text_artifact(
        slug="api-request-lifecycle",
        fmt="svg",
        content=SMOKE_SVG,
        output_dir=str((Path.cwd() / "smoke-output").resolve()),
    )
    return path, True


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    target, already_written = choose_output_path(args)

    if not already_written:
        target.write_text(SMOKE_SVG, encoding="utf-8", newline="\n")

    errors, warnings = validate_svg_file(target)
    if errors:
        print("Smoke render failed validation:")
        for item in errors:
            print(f"- {item}")
        return 1

    print(target.as_posix())
    if warnings:
        print("Warnings:")
        for item in warnings:
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
