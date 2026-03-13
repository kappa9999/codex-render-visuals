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
