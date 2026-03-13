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
