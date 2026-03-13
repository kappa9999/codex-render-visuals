from __future__ import annotations

import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "codex-visuals"
RENDER_SMOKE = SKILL_DIR / "scripts" / "render_smoke_svg.py"
VALIDATE_SVG = SKILL_DIR / "scripts" / "validate_svg.py"
SVG_NS = {"svg": "http://www.w3.org/2000/svg"}


def test_render_smoke_svg_produces_valid_svg(tmp_path: Path) -> None:
    assert RENDER_SMOKE.exists(), "render_smoke_svg.py must exist under codex-visuals/scripts/."
    result = subprocess.run(
        [sys.executable, str(RENDER_SMOKE), "--output-dir", str(tmp_path)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    svg_files = sorted(tmp_path.glob("*.svg"))
    assert len(svg_files) == 1, f"Expected exactly one SVG output, found: {[p.name for p in svg_files]}"

    root = ET.parse(svg_files[0]).getroot()
    assert root.tag.endswith("svg")
    assert root.attrib.get("viewBox"), "SVG output must define a viewBox."

    title = root.find("svg:title", SVG_NS)
    desc = root.find("svg:desc", SVG_NS)
    assert title is not None and (title.text or "").strip(), "SVG output must include a non-empty <title>."
    assert desc is not None and (desc.text or "").strip(), "SVG output must include a non-empty <desc>."


def test_generated_svg_passes_validator(tmp_path: Path) -> None:
    assert VALIDATE_SVG.exists(), "validate_svg.py must exist under codex-visuals/scripts/."
    render_result = subprocess.run(
        [sys.executable, str(RENDER_SMOKE), "--output-dir", str(tmp_path)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert render_result.returncode == 0, render_result.stdout + render_result.stderr

    svg_files = sorted(tmp_path.glob("*.svg"))
    assert svg_files, "Smoke renderer did not create an SVG file."

    validate_result = subprocess.run(
        [sys.executable, str(VALIDATE_SVG), str(svg_files[0])],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert validate_result.returncode == 0, validate_result.stdout + validate_result.stderr
