#!/usr/bin/env python3
"""Validate the codex-visuals skill layout and metadata."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/client-compatibility.md",
    "references/design-system.md",
    "references/diagram-patterns.md",
    "references/chart-patterns.md",
    "references/quality-checklist.md",
    "scripts/write_visual.py",
    "scripts/validate_svg.py",
    "scripts/render_smoke_svg.py",
    "scripts/install-skill-from-repo.ps1",
    "scripts/install-skill-from-repo.sh",
]


def skill_root(raw: str | None = None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    return Path(__file__).resolve().parents[1]


def validate_frontmatter(text: str) -> list[str]:
    errors: list[str] = []
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return ["SKILL.md must start with YAML frontmatter"]

    frontmatter = match.group(1)
    name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
    description_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
    if not name_match:
        errors.append("frontmatter missing name")
    elif name_match.group(1).strip() != "codex-visuals":
        errors.append("frontmatter name must be codex-visuals")
    if not description_match:
        errors.append("frontmatter missing description")
    return errors


def validate_openai_yaml(text: str) -> list[str]:
    errors: list[str] = []
    required_strings = [
        'display_name: "Codex Visuals"',
        'short_description: "Native Mermaid and SVG visuals for Codex"',
        'default_prompt: "Use $codex-visuals to turn this explanation into a Mermaid or SVG visual."',
    ]
    for value in required_strings:
        if value not in text:
            errors.append(f"agents/openai.yaml missing expected entry: {value}")
    return errors


def validate_references_exist(root: Path, skill_text: str) -> list[str]:
    errors: list[str] = []
    referenced_paths = re.findall(r"`((?:references|scripts)/[^`]+)`", skill_text)
    for relative_path in sorted(set(referenced_paths)):
        if not (root / relative_path).exists():
            errors.append(f"referenced path does not exist: {relative_path}")
    return errors


def validate_required_files(root: Path) -> list[str]:
    errors: list[str] = []
    for relative_path in REQUIRED_FILES:
        if not (root / relative_path).exists():
            errors.append(f"missing required file: {relative_path}")
    return errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the codex-visuals skill directory.")
    parser.add_argument("skill_dir", nargs="?", help="Optional path to the skill directory.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = skill_root(args.skill_dir)
    errors = validate_required_files(root)

    skill_text = (root / "SKILL.md").read_text(encoding="utf-8")
    errors.extend(validate_frontmatter(skill_text))
    errors.extend(validate_references_exist(root, skill_text))

    openai_text = (root / "agents" / "openai.yaml").read_text(encoding="utf-8")
    errors.extend(validate_openai_yaml(openai_text))

    if errors:
        print("Validation failed:")
        for item in errors:
            print(f"- {item}")
        return 1

    print("Skill layout validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
