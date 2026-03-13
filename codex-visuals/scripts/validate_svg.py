#!/usr/bin/env python3
"""Validate a standalone SVG for chat-safe rendering."""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


SVG_NAMESPACE = "{http://www.w3.org/2000/svg}"
DISALLOWED_TAGS = {"script", "foreignObject"}
REMOTE_VALUE_RE = re.compile(r"^(?:https?:)?//", re.IGNORECASE)


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_font_size(element: ET.Element) -> float:
    raw = element.attrib.get("font-size")
    if raw:
        try:
            return float(str(raw).replace("px", "").strip())
        except ValueError:
            pass
    style = element.attrib.get("style", "")
    match = re.search(r"font-size\s*:\s*([0-9.]+)px", style)
    if match:
        return float(match.group(1))
    return 14.0


def approximate_text_width(text: str, font_size: float) -> float:
    return len(text) * font_size * 0.56


def iter_text_lines(element: ET.Element) -> list[str]:
    tspans = [child for child in element if local_name(child.tag) == "tspan"]
    if tspans:
        lines = []
        for child in tspans:
            line = "".join(child.itertext()).strip()
            if line:
                lines.append(line)
        return lines
    line = "".join(element.itertext()).strip()
    return [line] if line else []


def validate_svg_file(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not path.exists():
        return [f"file not found: {path}"], warnings

    if path.suffix.lower() != ".svg":
        warnings.append("file does not use the .svg extension")

    if path.stat().st_size > 1_000_000:
        warnings.append("file size exceeds 1 MB")

    raw = path.read_text(encoding="utf-8")
    if "<svg" not in raw:
        errors.append("missing <svg root element")
        return errors, warnings

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        errors.append(f"XML parse error: {exc}")
        return errors, warnings

    if local_name(root.tag) != "svg":
        errors.append("root element is not <svg>")

    viewbox_width: float | None = None
    if not root.attrib.get("viewBox"):
        errors.append("missing viewBox attribute")
    else:
        parts = root.attrib["viewBox"].replace(",", " ").split()
        if len(parts) != 4:
            errors.append("viewBox must contain four numeric values")
        else:
            try:
                width = float(parts[2])
                height = float(parts[3])
            except ValueError:
                errors.append("viewBox values must be numeric")
            else:
                if width <= 0 or height <= 0:
                    errors.append("viewBox width and height must be positive")
                else:
                    viewbox_width = width

    if root.find(f"{SVG_NAMESPACE}title") is None and root.find("title") is None:
        errors.append("missing <title>")
    if root.find(f"{SVG_NAMESPACE}desc") is None and root.find("desc") is None:
        errors.append("missing <desc>")

    text_nodes = 0
    for element in root.iter():
        name = local_name(element.tag)
        if name in DISALLOWED_TAGS:
            errors.append(f"disallowed tag <{name}> present")
        if name == "text":
            text_nodes += 1
            if viewbox_width is not None and "x" in element.attrib:
                try:
                    x = float(element.attrib["x"])
                except ValueError:
                    x = None
                if x is not None:
                    font_size = parse_font_size(element)
                    anchor = element.attrib.get("text-anchor", "start").lower()
                    for line in iter_text_lines(element):
                        estimated_width = approximate_text_width(line, font_size)
                        if anchor == "middle":
                            right_edge = x + estimated_width / 2
                        elif anchor == "end":
                            right_edge = x
                        else:
                            right_edge = x + estimated_width
                        if right_edge > viewbox_width - 12:
                            warnings.append(
                                f"text may overflow right edge: '{line[:48]}'"
                            )
                        if len(line) > 54:
                            warnings.append(
                                f"text line is unusually long and may need wrapping: '{line[:48]}'"
                            )

        for key, value in element.attrib.items():
            normalized_key = key.lower()
            value_text = value.strip()
            if normalized_key in {"href", "{http://www.w3.org/1999/xlink}href"}:
                if value_text.startswith("#"):
                    continue
                if REMOTE_VALUE_RE.match(value_text) or value_text.startswith("http:") or value_text.startswith("https:"):
                    errors.append(f"external reference not allowed: {value_text}")
            if "url(" in value_text and ("http://" in value_text or "https://" in value_text):
                errors.append(f"remote url() reference not allowed: {value_text}")

    if text_nodes == 0:
        warnings.append("no <text> elements found")

    return sorted(set(errors)), sorted(set(warnings))


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an SVG file.")
    parser.add_argument("path", help="Path to the SVG file.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    path = Path(args.path).expanduser().resolve()
    errors, warnings = validate_svg_file(path)

    if args.json:
        print(json.dumps({"path": path.as_posix(), "errors": errors, "warnings": warnings}, indent=2))
    else:
        if errors:
            print("Errors:")
            for item in errors:
                print(f"- {item}")
        if warnings:
            print("Warnings:")
            for item in warnings:
                print(f"- {item}")
        if not errors and not warnings:
            print("SVG validation passed.")

    if errors:
        return 1
    if warnings and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
