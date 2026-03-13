from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "codex-visuals"
SKILL_MD = SKILL_DIR / "SKILL.md"
OPENAI_YAML = SKILL_DIR / "agents" / "openai.yaml"
QUICK_VALIDATE = SKILL_DIR / "scripts" / "quick_validate.py"


def _load_frontmatter() -> dict:
    text = SKILL_MD.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError("SKILL.md must start with YAML frontmatter.")
    _, frontmatter, _ = text.split("---", 2)
    return yaml.safe_load(frontmatter)


def _load_openai_yaml() -> dict:
    return yaml.safe_load(OPENAI_YAML.read_text(encoding="utf-8"))


def test_public_skill_layout_exists() -> None:
    required_paths = [
        SKILL_DIR,
        SKILL_MD,
        OPENAI_YAML,
        SKILL_DIR / "references",
        SKILL_DIR / "scripts",
        SKILL_DIR / "scripts" / "quick_validate.py",
        SKILL_DIR / "scripts" / "render_smoke_svg.py",
        SKILL_DIR / "scripts" / "validate_svg.py",
        SKILL_DIR / "scripts" / "export_svg_png.py",
        SKILL_DIR / "references" / "client-compatibility.md",
        SKILL_DIR / "references" / "design-system.md",
        SKILL_DIR / "references" / "diagram-patterns.md",
        SKILL_DIR / "references" / "quality-checklist.md",
    ]
    missing = [str(path.relative_to(REPO_ROOT)) for path in required_paths if not path.exists()]
    assert not missing, f"Missing expected public skill files: {missing}"


def test_skill_metadata_and_ui_contract() -> None:
    frontmatter = _load_frontmatter()
    ui_config = _load_openai_yaml()

    assert frontmatter["name"] == "codex-visuals"
    description = frontmatter["description"]
    assert "TODO" not in description
    assert "visual" in description.lower()
    assert "codex" in description.lower()

    interface = ui_config["interface"]
    assert interface["display_name"] == "Codex Visuals"
    assert interface["short_description"]
    assert 25 <= len(interface["short_description"]) <= 64
    assert "$codex-visuals" in interface["default_prompt"]


def test_quick_validate_script_passes_against_skill_dir() -> None:
    assert QUICK_VALIDATE.exists(), "quick_validate.py must exist under codex-visuals/scripts/."
    result = subprocess.run(
        [sys.executable, str(QUICK_VALIDATE), str(SKILL_DIR)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
