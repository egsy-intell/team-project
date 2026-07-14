import pathlib
import subprocess
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"
NOTEBOOKS = sorted(NOTEBOOKS_DIR.glob("*.py"))


@pytest.mark.parametrize("notebook", NOTEBOOKS, ids=lambda p: p.name)
def test_notebook_executes(notebook, tmp_path):
    output = tmp_path / f"{notebook.stem}.html"
    result = subprocess.run(
        [sys.executable, "-m", "marimo", "export", "html", str(notebook), "-o", str(output)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"marimo failed to execute {notebook.name}:\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert output.exists()


def test_notebooks_spelling():
    result = subprocess.run(
        [sys.executable, "-m", "codespell_lib", str(NOTEBOOKS_DIR)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"codespell found issues:\n{result.stdout}{result.stderr}"
