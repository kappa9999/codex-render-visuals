#!/usr/bin/env python3
"""Optional docs-publishing helper for exporting standalone SVG files to PNG."""

from __future__ import annotations

import argparse
import math
import os
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


WINDOWS_CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
]

POSIX_CHROME_CANDIDATES = [
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
    Path("/usr/bin/google-chrome"),
    Path("/usr/bin/chromium"),
    Path("/usr/bin/chromium-browser"),
    Path("/snap/bin/chromium"),
]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export standalone SVG files to PNG.")
    parser.add_argument("svg_paths", nargs="+", help="One or more SVG files to export.")
    parser.add_argument("--output", help="Exact PNG path. Valid only with a single SVG input.")
    parser.add_argument("--output-dir", help="Directory for generated PNG files.")
    parser.add_argument("--chrome", help="Exact Chrome or Chromium executable path.")
    parser.add_argument("--background", default="#ffffff", help="HTML wrapper background color.")
    parser.add_argument("--padding", type=int, default=0, help="Padding in pixels around the SVG.")
    return parser.parse_args(argv)


def _parse_svg_length(value: str | None) -> float | None:
    if not value:
        return None
    stripped = value.strip()
    if not stripped:
        return None
    number_chars: list[str] = []
    seen_decimal = False
    for char in stripped:
        if char.isdigit():
            number_chars.append(char)
            continue
        if char in {"+", "-"} and not number_chars:
            number_chars.append(char)
            continue
        if char == "." and not seen_decimal:
            number_chars.append(char)
            seen_decimal = True
            continue
        break
    if not number_chars or number_chars in (["+"], ["-"], ["."]):
        return None
    try:
        return float("".join(number_chars))
    except ValueError:
        return None


def extract_svg_dimensions(svg_path: Path) -> tuple[int, int]:
    root = ET.fromstring(svg_path.read_text(encoding="utf-8"))

    width = _parse_svg_length(root.attrib.get("width"))
    height = _parse_svg_length(root.attrib.get("height"))
    if width and height:
        return math.ceil(width), math.ceil(height)

    view_box = root.attrib.get("viewBox", "").replace(",", " ").split()
    if len(view_box) == 4:
        box_width = _parse_svg_length(view_box[2])
        box_height = _parse_svg_length(view_box[3])
        if box_width and box_height:
            return math.ceil(box_width), math.ceil(box_height)

    raise ValueError(f"Unable to determine SVG dimensions for {svg_path}")


def find_chrome_executable(explicit_path: str | None) -> Path:
    candidates: list[Path] = []
    if explicit_path:
        candidates.append(Path(explicit_path).expanduser())

    for env_name in ("CHROME_PATH", "CHROMIUM_PATH", "BROWSER"):
        env_value = os.environ.get(env_name)
        if env_value:
            candidates.append(Path(env_value).expanduser())

    if os.name == "nt":
        candidates.extend(WINDOWS_CHROME_CANDIDATES)
    else:
        candidates.extend(POSIX_CHROME_CANDIDATES)

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        "Could not find Chrome or Chromium. Pass --chrome or set CHROME_PATH."
    )


def choose_output_paths(svg_paths: list[Path], args: argparse.Namespace) -> list[Path]:
    if args.output and len(svg_paths) != 1:
        raise ValueError("--output can only be used with a single SVG input.")

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return [output_path]

    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else None
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    outputs: list[Path] = []
    for svg_path in svg_paths:
        target_dir = output_dir if output_dir else svg_path.parent
        target_path = (target_dir / f"{svg_path.stem}.png").resolve()
        target_path.parent.mkdir(parents=True, exist_ok=True)
        outputs.append(target_path)
    return outputs


def build_wrapper_document(svg_text: str, background: str, padding: int) -> str:
    return (
        "<!doctype html><html><head><meta charset=\"utf-8\"></head>"
        f"<body style=\"margin:0;background:{background};\">"
        f"<div style=\"padding:{padding}px;display:inline-block;line-height:0;\">"
        f"{svg_text}</div>"
        "</body></html>"
    )


def render_svg_to_png(
    svg_path: Path,
    output_path: Path,
    chrome_path: Path,
    background: str,
    padding: int,
) -> None:
    width, height = extract_svg_dimensions(svg_path)
    svg_text = svg_path.read_text(encoding="utf-8")
    wrapper_html = build_wrapper_document(svg_text, background=background, padding=padding)

    with tempfile.TemporaryDirectory(prefix="codex-visuals-render-") as temp_dir:
        wrapper_path = Path(temp_dir) / f"{svg_path.stem}.html"
        wrapper_path.write_text(wrapper_html, encoding="utf-8", newline="\n")

        window_width = width + (padding * 2)
        window_height = height + (padding * 2)
        command = [
            str(chrome_path),
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--window-size={window_width},{window_height}",
            f"--screenshot={output_path}",
            wrapper_path.resolve().as_uri(),
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            raise RuntimeError(
                "Chrome screenshot export failed.\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    svg_paths = [Path(item).expanduser().resolve() for item in args.svg_paths]

    for svg_path in svg_paths:
        if svg_path.suffix.lower() != ".svg":
            print(f"Expected an .svg input: {svg_path}", file=sys.stderr)
            return 2
        if not svg_path.exists():
            print(f"Missing input SVG: {svg_path}", file=sys.stderr)
            return 2

    try:
        chrome_path = find_chrome_executable(args.chrome)
        output_paths = choose_output_paths(svg_paths, args)
        for svg_path, output_path in zip(svg_paths, output_paths, strict=True):
            render_svg_to_png(
                svg_path=svg_path,
                output_path=output_path,
                chrome_path=chrome_path,
                background=args.background,
                padding=args.padding,
            )
            print(output_path.as_posix())
    except Exception as exc:  # pragma: no cover - surfaced to CLI caller
        print(str(exc), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
