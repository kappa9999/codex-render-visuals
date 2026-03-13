#!/usr/bin/env python3
"""Write a visual artifact to a deterministic output path."""

from __future__ import annotations

import argparse
import shutil
import re
import sys
from pathlib import Path


IMAGE_EXTENSIONS = {"svg", "png", "jpg", "jpeg", "webp"}
TEXT_EXTENSIONS = {"svg", "html", "md", "mmd", "mermaid", "txt", "json"}


def slugify(raw: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", raw.strip().lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if not slug:
        raise ValueError("slug must contain at least one letter or digit")
    return slug


def resolve_output_dir(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    return (Path.cwd() / "visuals").resolve()


def write_text_artifact(
    *,
    slug: str,
    fmt: str,
    content: str,
    output_dir: str | None = None,
) -> Path:
    target_dir = resolve_output_dir(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    path = (target_dir / f"{slugify(slug)}.{fmt}").resolve()
    path.write_text(content, encoding="utf-8", newline="\n")
    return path


def copy_artifact_from_file(*, slug: str, fmt: str, source_file: str, output_dir: str | None = None) -> Path:
    target_dir = resolve_output_dir(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    path = (target_dir / f"{slugify(slug)}.{fmt}").resolve()
    shutil.copyfile(source_file, path)
    return path


def markdown_embed(path: Path, alt_text: str) -> str:
    return f"![{alt_text}]({path.as_posix()})"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write a visual artifact and print its path.")
    parser.add_argument("--slug", required=True, help="Hyphen-friendly filename stem.")
    parser.add_argument("--format", default="svg", help="Artifact extension, such as svg or png.")
    parser.add_argument("--output-dir", help="Output directory. Defaults to ./visuals")
    parser.add_argument("--source-file", help="Read artifact content from a file instead of stdin.")
    parser.add_argument("--alt", default="Generated visual", help="Alt text when printing Markdown.")
    parser.add_argument(
        "--print-markdown",
        action="store_true",
        help="Print a Markdown image tag for image formats instead of only the path.",
    )
    return parser.parse_args(argv)


def read_content(source_file: str | None) -> str:
    if source_file:
        return Path(source_file).read_text(encoding="utf-8")
    return sys.stdin.read()


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    fmt = args.format.lower().strip(".")

    if fmt not in TEXT_EXTENSIONS and args.source_file:
        path = copy_artifact_from_file(
            slug=args.slug,
            fmt=fmt,
            source_file=args.source_file,
            output_dir=args.output_dir,
        )
    else:
        content = read_content(args.source_file)
        if not content.strip():
            print("error: no content provided", file=sys.stderr)
            return 1
        path = write_text_artifact(
            slug=args.slug,
            fmt=fmt,
            content=content,
            output_dir=args.output_dir,
        )

    if args.print_markdown and path.suffix.lower().lstrip(".") in IMAGE_EXTENSIONS:
        print(markdown_embed(path, args.alt))
    else:
        print(path.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
