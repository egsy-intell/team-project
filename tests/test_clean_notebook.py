import pathlib
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLKIT_SCRIPT = REPO_ROOT / "scripts" / "toolkit.py"

# A minimal stand-in for a marimo HTML export: just enough structure
# (<head>/<body> boundaries) for the patch to anchor on. clean-notebook
# doesn't touch anything else, so it doesn't need to look like real marimo
# output.
FIXTURE_HTML = """<!DOCTYPE html>
<html lang="en">
  <head>
    <title>fixture</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
"""


def _run_clean_notebook(*args, cwd=None):
    return subprocess.run(
        [sys.executable, str(TOOLKIT_SCRIPT), "clean-notebook", *args],
        capture_output=True,
        text=True,
        check=False,
        cwd=cwd,
    )


def test_clean_notebook_patches_local_file(tmp_path):
    fixture = tmp_path / "notebook.html"
    fixture.write_text(FIXTURE_HTML)

    result = _run_clean_notebook(str(fixture), "--output-dir", str(tmp_path))
    assert result.returncode == 0, result.stderr

    output_path = tmp_path / "notebook_clean.html"
    assert output_path.exists()

    cleaned = output_path.read_text()
    assert 'id="print-fixes"' in cleaned
    assert 'id="print-shadow-fix"' in cleaned
    # The patch must land inside <head>/<body>, not appended after them.
    assert cleaned.index('id="print-fixes"') < cleaned.index("</head>")
    assert cleaned.index('id="print-shadow-fix"') < cleaned.index("</body>")
    # Everything from the original document should still be present.
    assert '<div id="root"></div>' in cleaned


def test_clean_notebook_default_name_is_derived_from_input(tmp_path):
    fixture = tmp_path / "index.html"
    fixture.write_text(FIXTURE_HTML)

    result = _run_clean_notebook(str(fixture), "--output-dir", str(tmp_path))
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "index_clean.html").exists()


def test_clean_notebook_custom_name_and_dir(tmp_path):
    fixture = tmp_path / "index.html"
    fixture.write_text(FIXTURE_HTML)
    out_dir = tmp_path / "out"

    result = _run_clean_notebook(
        str(fixture), "--name", "report.html", "--output-dir", str(out_dir)
    )
    assert result.returncode == 0, result.stderr
    assert (out_dir / "report.html").exists()


def test_clean_notebook_rejects_already_patched_input(tmp_path):
    fixture = tmp_path / "notebook.html"
    fixture.write_text(FIXTURE_HTML)

    first = _run_clean_notebook(str(fixture), "--output-dir", str(tmp_path))
    assert first.returncode == 0, first.stderr

    already_clean = tmp_path / "notebook_clean.html"
    second = _run_clean_notebook(str(already_clean), "--output-dir", str(tmp_path))
    assert second.returncode != 0
    assert "already contains" in second.stderr
