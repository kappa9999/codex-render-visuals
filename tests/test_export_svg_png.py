from __future__ import annotations

import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "codex-visuals" / "scripts" / "export_svg_png.py"

spec = importlib.util.spec_from_file_location("export_svg_png", SCRIPT_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_extract_svg_dimensions_prefers_width_height(tmp_path: Path) -> None:
    svg_path = tmp_path / "sized.svg"
    svg_path.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" viewBox="0 0 10 10"/>',
        encoding="utf-8",
    )

    assert module.extract_svg_dimensions(svg_path) == (640, 360)


def test_extract_svg_dimensions_falls_back_to_viewbox(tmp_path: Path) -> None:
    svg_path = tmp_path / "viewbox.svg"
    svg_path.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 500"/>',
        encoding="utf-8",
    )

    assert module.extract_svg_dimensions(svg_path) == (1080, 500)


def test_choose_output_paths_uses_source_directory_by_default(tmp_path: Path) -> None:
    source = tmp_path / "diagram.svg"
    source.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"/>', encoding="utf-8")

    args = module.parse_args([str(source)])
    outputs = module.choose_output_paths([source], args)

    assert outputs == [tmp_path / "diagram.png"]
