from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
README = REPO_ROOT / "README.md"
PROMPTS = REPO_ROOT / "examples" / "prompts.md"
CATALOG = REPO_ROOT / "examples" / "catalog.json"
VALIDATE_SVG = REPO_ROOT / "codex-visuals" / "scripts" / "validate_svg.py"


def _load_catalog() -> list[dict]:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def test_catalog_has_exactly_three_curated_examples() -> None:
    entries = _load_catalog()
    assert len(entries) == 3
    assert [entry["id"] for entry in entries] == [
        "house-load-transfer",
        "api-request-lifecycle",
        "sqlite-vs-postgres",
    ]


def test_readme_and_prompts_match_catalog() -> None:
    entries = _load_catalog()
    readme_text = README.read_text(encoding="utf-8")
    prompts_text = PROMPTS.read_text(encoding="utf-8")

    assert ".png" not in readme_text.lower()
    assert ".png" not in prompts_text.lower()
    assert "Rendered sample" not in readme_text
    assert "Reference SVG artifact" not in readme_text
    assert not (REPO_ROOT / "codex-visuals" / "scripts" / "export_svg_png.py").exists()

    for entry in entries:
        assert entry["readme_heading"] in readme_text
        assert entry["prompt"] in readme_text
        assert entry["prompt"] in prompts_text
        assert entry["primary_artifact"] in readme_text
        assert entry["primary_artifact"] in prompts_text

        artifact_paths = [entry["primary_artifact"], *entry["supporting_artifacts"]]
        for relative_path in artifact_paths:
            assert (REPO_ROOT / relative_path).exists(), f"Missing artifact: {relative_path}"

        if entry["mode"] == "svg":
            assert f"(./{entry['primary_artifact']})" in readme_text

    for entry in entries:
        assert readme_text.count(entry["readme_heading"]) == 1
    assert readme_text.count("```mermaid") == 1


def test_curated_svg_examples_validate() -> None:
    entries = _load_catalog()
    svg_paths = []
    for entry in entries:
        if entry["primary_artifact"].endswith(".svg"):
            svg_paths.append(REPO_ROOT / entry["primary_artifact"])
        for relative_path in entry["supporting_artifacts"]:
            if relative_path.endswith(".svg"):
                svg_paths.append(REPO_ROOT / relative_path)

    for path in svg_paths:
        result = subprocess.run(
            [sys.executable, str(VALIDATE_SVG), str(path)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stdout + result.stderr
