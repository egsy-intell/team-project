import pathlib
import subprocess
import sys
import zipfile

import pytest

pytest.importorskip("pypandoc")

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD_SCRIPT = REPO_ROOT / "scripts" / "build_presentation.py"


def test_build_presentation(tmp_path):
    output_dir = tmp_path / "dist"
    result = subprocess.run(
        [sys.executable, str(BUILD_SCRIPT), "--output-dir", str(output_dir)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"build_presentation.py failed:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )

    output_path = output_dir / "checkpoint2_deck.pptx"
    assert output_path.exists()
    assert output_path.stat().st_size > 10_000

    with output_path.open("rb") as f:
        assert f.read(4) == b"PK\x03\x04"

    with zipfile.ZipFile(output_path) as zf:
        names = zf.namelist()
        assert any(name.startswith("ppt/slides/slide") for name in names)
