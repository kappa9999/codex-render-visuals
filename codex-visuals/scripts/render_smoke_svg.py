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


SMOKE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="960" height="420" viewBox="0 0 960 420" role="img" aria-labelledby="title desc">
  <title id="title">API request lifecycle</title>
  <desc id="desc">A simple left-to-right flow showing client request, gateway, service, database, and response.</desc>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
  <rect x="20" y="20" width="920" height="380" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="2" rx="18"/>
  <text x="40" y="58" font-family="Segoe UI, Arial, sans-serif" font-size="28" font-weight="600" fill="#1F2937">API request lifecycle</text>
  <text x="40" y="84" font-family="Segoe UI, Arial, sans-serif" font-size="15" fill="#4B5563">Smoke render for codex-visuals.</text>
  <rect x="60" y="170" width="150" height="74" fill="#DBEAFE" stroke="#2563EB" stroke-width="2" rx="12"/>
  <rect x="260" y="170" width="150" height="74" fill="#DBEAFE" stroke="#2563EB" stroke-width="2" rx="12"/>
  <rect x="460" y="170" width="150" height="74" fill="#DBEAFE" stroke="#2563EB" stroke-width="2" rx="12"/>
  <rect x="660" y="170" width="150" height="74" fill="#E5E7EB" stroke="#4B5563" stroke-width="2" rx="12"/>
  <text x="135" y="200" font-family="Segoe UI, Arial, sans-serif" font-size="18" font-weight="600" fill="#1F2937" text-anchor="middle">Client</text>
  <text x="135" y="222" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#4B5563" text-anchor="middle">sends request</text>
  <text x="335" y="200" font-family="Segoe UI, Arial, sans-serif" font-size="18" font-weight="600" fill="#1F2937" text-anchor="middle">Gateway</text>
  <text x="335" y="222" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#4B5563" text-anchor="middle">routes traffic</text>
  <text x="535" y="200" font-family="Segoe UI, Arial, sans-serif" font-size="18" font-weight="600" fill="#1F2937" text-anchor="middle">Service</text>
  <text x="535" y="222" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#4B5563" text-anchor="middle">executes logic</text>
  <text x="735" y="200" font-family="Segoe UI, Arial, sans-serif" font-size="18" font-weight="600" fill="#1F2937" text-anchor="middle">Database</text>
  <text x="735" y="222" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#4B5563" text-anchor="middle">stores state</text>
  <path d="M210 207 L260 207" fill="none" stroke="#D97706" stroke-width="3" stroke-linecap="round" marker-end="url(#arrow)"/>
  <path d="M410 207 L460 207" fill="none" stroke="#D97706" stroke-width="3" stroke-linecap="round" marker-end="url(#arrow)"/>
  <path d="M610 207 L660 207" fill="none" stroke="#D97706" stroke-width="3" stroke-linecap="round" marker-end="url(#arrow)"/>
  <path d="M660 254 L610 310 L460 310" fill="none" stroke="#D97706" stroke-width="3" stroke-linecap="round" marker-end="url(#arrow)"/>
  <text x="635" y="294" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#4B5563">query result</text>
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
