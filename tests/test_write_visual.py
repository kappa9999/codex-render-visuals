from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
WRITE_VISUAL = REPO_ROOT / "codex-visuals" / "scripts" / "write_visual.py"


def test_write_visual_prints_mermaid_fence_and_writes_file(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(WRITE_VISUAL),
            "--slug",
            "api-request-lifecycle",
            "--format",
            "mmd",
            "--output-dir",
            str(tmp_path),
            "--print-fence",
        ],
        cwd=REPO_ROOT,
        input="flowchart LR\n  A[Browser] --> B[Gateway]\n",
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.startswith("```mermaid\nflowchart LR\n")
    assert result.stdout.rstrip().endswith("```")
    assert (tmp_path / "api-request-lifecycle.mmd").exists()


def test_write_visual_prints_svg_markdown_and_writes_file(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(WRITE_VISUAL),
            "--slug",
            "house-load-transfer",
            "--format",
            "svg",
            "--output-dir",
            str(tmp_path),
            "--print-markdown",
            "--alt",
            "House load transfer diagram",
        ],
        cwd=REPO_ROOT,
        input="<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 10 10\"><title>x</title><desc>y</desc></svg>\n",
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip().startswith("![House load transfer diagram](")
    assert (tmp_path / "house-load-transfer.svg").exists()


def test_write_visual_rejects_print_markdown_for_non_svg(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(WRITE_VISUAL),
            "--slug",
            "api-request-lifecycle",
            "--format",
            "mmd",
            "--output-dir",
            str(tmp_path),
            "--print-markdown",
        ],
        cwd=REPO_ROOT,
        input="flowchart LR\n  A --> B\n",
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "--print-markdown only supports svg output" in result.stderr


def test_write_visual_rejects_print_fence_for_non_mermaid(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(WRITE_VISUAL),
            "--slug",
            "diagram",
            "--format",
            "svg",
            "--output-dir",
            str(tmp_path),
            "--print-fence",
        ],
        cwd=REPO_ROOT,
        input="<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 10 10\"></svg>\n",
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "--print-fence only supports mmd or mermaid outputs" in result.stderr


def test_write_visual_rejects_unsupported_format(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(WRITE_VISUAL),
            "--slug",
            "diagram",
            "--format",
            "png",
            "--output-dir",
            str(tmp_path),
        ],
        cwd=REPO_ROOT,
        input="not-used\n",
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "unsupported format for v1. Use svg, mmd, or mermaid." in result.stderr
